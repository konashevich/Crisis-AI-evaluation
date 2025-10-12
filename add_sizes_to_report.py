#!/usr/bin/env python3
"""
Add model sizes to existing evaluation reports WITHOUT re-running expensive Gemini API calls.
Reads size data from runinfo files and updates the evaluation report JSON.
"""

import json
import sys
from pathlib import Path
from typing import Optional

def find_runinfo_file(batch_folder: Path, model_name: str) -> Optional[Path]:
    """Find the runinfo file for a given model name."""
    # Model names in reports are like "gemma-3-12b-it-q8_0"
    # Runinfo files are like "gemma-3-12b-it-q8_0_2025-10-11_10-35-39_runinfo.json"
    
    pattern = f"{model_name}_*_runinfo.json"
    matches = list(batch_folder.glob(pattern))
    
    if matches:
        return matches[0]  # Return first match
    
    return None

def add_sizes_to_report(report_path: str, batch_folder: str):
    """Add model sizes to an existing evaluation report."""
    
    report_file = Path(report_path)
    batch_path = Path(batch_folder)
    
    if not report_file.exists():
        print(f"❌ Error: Report file not found: {report_path}")
        return False
    
    if not batch_path.exists():
        print(f"❌ Error: Batch folder not found: {batch_folder}")
        return False
    
    # Load the evaluation report
    print(f"📖 Loading evaluation report: {report_file.name}")
    with open(report_file, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    # Check if model_metadata exists
    if 'model_metadata' not in report:
        print("❌ Error: No model_metadata found in report")
        return False
    
    models = report['model_metadata']
    print(f"📊 Found {len(models)} models in report")
    
    # Update each model with size data
    updated_count = 0
    already_had_count = 0
    not_found_count = 0
    
    for model_name, metadata in models.items():
        # Check if already has size data
        if metadata.get('model_size_gb') is not None:
            already_had_count += 1
            continue
        
        # Find the runinfo file
        runinfo_file = find_runinfo_file(batch_path, model_name)
        
        if not runinfo_file:
            print(f"⚠️  Warning: No runinfo file found for {model_name}")
            not_found_count += 1
            continue
        
        # Load the runinfo file
        with open(runinfo_file, 'r', encoding='utf-8') as f:
            runinfo = json.load(f)
        
        # Add size data to metadata
        if runinfo.get('model_size_gb') is not None:
            metadata['model_size_gb'] = runinfo['model_size_gb']
            metadata['model_size_bytes'] = runinfo['model_size_bytes']
            metadata['model_file_path'] = runinfo['model_file_path']
            print(f"  ✅ {model_name}: {runinfo['model_size_gb']:.2f} GB")
            updated_count += 1
        else:
            print(f"  ⚠️  {model_name}: runinfo has no size data")
            not_found_count += 1
    
    # Save the updated report
    print(f"\n💾 Saving updated report...")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"✅ Updated: {updated_count} models")
    print(f"ℹ️  Already had data: {already_had_count} models")
    print(f"⚠️  Not found/missing: {not_found_count} models")
    print(f"📊 Total: {len(models)} models")
    print(f"{'='*60}")
    print(f"\n🎉 Report updated successfully!")
    print(f"📄 File: {report_file}")
    print(f"\n💰 Cost: $0.00 (no API calls needed!)")
    
    return True

def main():
    """Main entry point."""
    
    if len(sys.argv) < 2:
        print("Usage: python add_sizes_to_report.py <report_file> [batch_folder]")
        print("\nExample:")
        print("  python add_sizes_to_report.py eval_results/gemini_evaluation_report.json test_results/2025-10-11_1")
        print("\nIf batch_folder is not provided, will try to infer from report metadata.")
        sys.exit(1)
    
    report_path = sys.argv[1]
    
    # Try to infer batch folder if not provided
    if len(sys.argv) >= 3:
        batch_folder = sys.argv[2]
    else:
        # Try to read batch folder from report metadata
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                report = json.load(f)
                batch_folder = report.get('batch_folder', 'test_results/2025-10-11_1')
                print(f"ℹ️  Using batch folder from report: {batch_folder}")
        except:
            print("❌ Error: Could not determine batch folder. Please provide it as second argument.")
            sys.exit(1)
    
    success = add_sizes_to_report(report_path, batch_folder)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
