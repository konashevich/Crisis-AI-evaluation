"""
Generate an index of all evaluation reports in eval_results/ folder.
This allows the HTML viewer to discover and load all reports.
"""
import json
import os
from pathlib import Path

EVAL_RESULTS_DIR = 'eval_results'
INDEX_FILE = os.path.join(EVAL_RESULTS_DIR, 'reports_index.json')

def generate_reports_index():
    """
    Scan eval_results/ directory for all gemini_evaluation_report_*.json files
    and create an index file listing them.
    """
    eval_dir = Path(EVAL_RESULTS_DIR)
    
    if not eval_dir.exists():
        print(f"Error: {EVAL_RESULTS_DIR} directory not found!")
        return False
    
    # Find all evaluation report files
    report_files = []
    for file in eval_dir.glob('gemini_evaluation_report_*.json'):
        # Exclude the index file itself
        if file.name != 'reports_index.json':
            report_files.append(file.name)
    
    # Sort by filename (which sorts by date/time due to naming convention)
    report_files.sort(reverse=True)  # Newest first
    
    # Create index
    index = {
        "reports": report_files,
        "count": len(report_files),
        "generated_at": Path(__file__).stat().st_mtime if Path(__file__).exists() else None
    }
    
    # Write index file
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)
    
    print(f"✅ Generated reports index: {INDEX_FILE}")
    print(f"   Found {len(report_files)} evaluation report(s)")
    for report in report_files:
        print(f"   • {report}")
    
    return True

if __name__ == "__main__":
    generate_reports_index()
