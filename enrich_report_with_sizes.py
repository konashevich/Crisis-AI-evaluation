#!/usr/bin/env python3
"""
Add model size data to existing evaluation reports by reading runinfo files.
This is a FREE alternative to re-running expensive Gemini API evaluations.
"""

import json
import sys
from pathlib import Path
from typing import Optional

def add_sizes_from_batch(report_path: str, batch_folder: Optional[str] = None):
    """
    Add model sizes to evaluation report by reading from runinfo files.
    Can use batch_folder from report or accept it as a parameter.
    """
    
    report_file = Path(report_path)
    
    if not report_file.exists():
        print(f"❌ Error: Report file not found: {report_path}")
        return False
    
    # Load the evaluation report
    print(f"📖 Loading evaluation report: {report_file.name}")
    with open(report_file, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    # Get batch folder from parameter or report
    if not batch_folder:
        batch_folder = report.get('batch_folder')
        if not batch_folder:
            print("❌ Error: No batch_folder provided and report doesn't have batch_folder field")
            print("Please provide batch folder as second argument:")
            print(f"  python enrich_report_with_sizes.py {report_path} test_results/2025-10-11_1")
            return False
        print(f"📁 Using batch folder from report: {batch_folder}")
    else:
        print(f"📁 Using specified batch folder: {batch_folder}")
    
    batch_path = Path(batch_folder)
    if not batch_path.exists():
        print(f"❌ Error: Batch folder not found: {batch_folder}")
        return False
    
    # Get model_metadata (or create it)
    if 'model_metadata' not in report:
        report['model_metadata'] = {}
    
    model_metadata = report['model_metadata']
    
    # Find all runinfo files
    runinfo_files = list(batch_path.glob('*_runinfo.json'))
    print(f"📊 Found {len(runinfo_files)} runinfo files")
    
    # Create a mapping of model names to runinfo data
    runinfo_map = {}
    for runinfo_file in runinfo_files:
        # Extract model name from filename: {model_name}_{timestamp}_runinfo.json
        filename = runinfo_file.stem  # removes .json
        # Remove _runinfo suffix
        if filename.endswith('_runinfo'):
            filename = filename[:-8]
        
        # Remove timestamp (format: _YYYY-MM-DD_HH-MM-SS)
        # Find the last occurrence of pattern _YYYY-MM-DD_HH-MM-SS
        import re
        # Match _YYYY-MM-DD_HH-MM-SS at the end
        match = re.search(r'_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})$', filename)
        if match:
            model_name = filename[:match.start()]
        else:
            model_name = filename
        
        # Load runinfo
        try:
            with open(runinfo_file, 'r', encoding='utf-8') as f:
                runinfo = json.load(f)
                if runinfo.get('model_size_gb') is not None:
                    runinfo_map[model_name] = {
                        'model_size_gb': runinfo['model_size_gb'],
                        'model_size_bytes': runinfo['model_size_bytes'],
                        'model_file_path': runinfo['model_file_path']
                    }
        except Exception as e:
            print(f"  ⚠️  Could not load {runinfo_file.name}: {e}")
    
    print(f"✅ Loaded size data for {len(runinfo_map)} models\n")
    
    # Update model_metadata
    updated = 0
    already_had = 0
    not_found = 0
    
    # Get all unique model names from the evaluations
    model_names = set()
    evaluations = report.get('evaluations', {})
    for category in evaluations.values():
        for subcategory in category.values():
            for question in subcategory:
                if 'gemini_evaluation' in question and 'evaluations' in question['gemini_evaluation']:
                    for eval_item in question['gemini_evaluation']['evaluations']:
                        if 'model_name' in eval_item:
                            model_names.add(eval_item['model_name'])
    
    print(f"📝 Found {len(model_names)} unique models in evaluation\n")
    
    for model_name in sorted(model_names):
        # Skip mistral (usually excluded)
        if 'mistral-7b' in model_name.lower():
            continue
        
        # Ensure model has entry in metadata
        if model_name not in model_metadata:
            model_metadata[model_name] = {}
        
        # Check if already has size
        if model_metadata[model_name].get('model_size_gb') is not None:
            already_had += 1
            continue
        
        # Try to find matching runinfo
        if model_name in runinfo_map:
            model_metadata[model_name].update(runinfo_map[model_name])
            print(f"  ✅ {model_name}: {runinfo_map[model_name]['model_size_gb']:.2f} GB")
            updated += 1
        else:
            print(f"  ⚠️  {model_name}: No runinfo file found")
            not_found += 1
    
    # Save updated report
    if updated > 0:
        print(f"\n💾 Saving updated report...")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"✅ Report updated successfully!")
    else:
        print(f"\nℹ️  No updates needed")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"✅ Updated: {updated} models")
    print(f"ℹ️  Already had data: {already_had} models")
    print(f"⚠️  Not found: {not_found} models")
    print(f"📊 Total: {len(model_names)} models")
    print(f"{'='*60}")
    print(f"\n💰 Cost: $0.00 (no API calls!)")
    print(f"📄 Report: {report_file}")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python enrich_report_with_sizes.py <report_file> [batch_folder]")
        print("\nExamples:")
        print("  # If report has batch_folder field:")
        print("  python enrich_report_with_sizes.py eval_results/gemini_evaluation_report_2025-10-12_08-07-40.json")
        print("")
        print("  # If report doesn't have batch_folder field, specify it:")
        print("  python enrich_report_with_sizes.py eval_results/gemini_evaluation_report_2025-10-12_08-07-40.json test_results/2025-10-11_1")
        print("\nThis script reads runinfo files from the batch folder and adds size data to the report.")
        sys.exit(1)
    
    report_path = sys.argv[1]
    batch_folder = sys.argv[2] if len(sys.argv) >= 3 else None
    
    success = add_sizes_from_batch(report_path, batch_folder)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
