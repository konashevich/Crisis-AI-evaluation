"""
Helper script to run test-evaluation.py on a specific batch folder.
Temporarily modifies the INPUT_FILE_PATTERN before running evaluation.
"""
import os
import sys
import subprocess
import re
from datetime import datetime

RESULTS_DIR = 'test_results'


def get_latest_batch_folder() -> str:
    """Find the most recent batch folder"""
    if not os.path.exists(RESULTS_DIR):
        print(f"Error: {RESULTS_DIR} directory not found!")
        return None
    
    batch_folders = []
    for item in os.listdir(RESULTS_DIR):
        item_path = os.path.join(RESULTS_DIR, item)
        if os.path.isdir(item_path) and re.match(r'\d{4}-\d{2}-\d{2}_\d+$', item):
            batch_folders.append((item, item_path))
    
    if not batch_folders:
        print("No batch folders found in test_results/")
        print("Run 'python batch_test_models.py' first to create batch results")
        return None
    
    # Sort by folder name (which sorts by date_number)
    batch_folders.sort(key=lambda x: x[0], reverse=True)
    return batch_folders[0]


def list_batch_folders():
    """List all available batch folders"""
    if not os.path.exists(RESULTS_DIR):
        print(f"Error: {RESULTS_DIR} directory not found!")
        return []
    
    batch_folders = []
    for item in os.listdir(RESULTS_DIR):
        item_path = os.path.join(RESULTS_DIR, item)
        if os.path.isdir(item_path) and re.match(r'\d{4}-\d{2}-\d{2}_\d+$', item):
            # Count JSON files (excluding _runinfo.json)
            json_files = [f for f in os.listdir(item_path) 
                         if f.endswith('.json') and not f.endswith('_runinfo.json')]
            batch_folders.append((item, len(json_files)))
    
    batch_folders.sort(key=lambda x: x[0], reverse=True)
    return batch_folders


def run_evaluation_on_batch(batch_folder_name: str):
    """
    Run test-evaluation.py on a specific batch folder.
    Modifies INPUT_FILE_PATTERN temporarily via environment variable.
    """
    batch_path = os.path.join(RESULTS_DIR, batch_folder_name)
    
    if not os.path.exists(batch_path):
        print(f"Error: Batch folder '{batch_folder_name}' not found!")
        return False
    
    # Count files in batch
    json_files = [f for f in os.listdir(batch_path) 
                  if f.endswith('.json') and not f.endswith('_runinfo.json')]
    
    print(f"\n{'='*70}")
    print(f"Evaluating Batch: {batch_folder_name}")
    print(f"Location: {batch_path}")
    print(f"Models: {len(json_files)}")
    print(f"{'='*70}\n")
    
    # Set environment variable to tell test-evaluation.py where to look
    env = os.environ.copy()
    env['BATCH_FOLDER'] = batch_path
    
    # Run test-evaluation.py
    try:
        result = subprocess.run(
            [sys.executable, 'test-evaluation.py'],
            env=env,
            check=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error running evaluation: {e}")
        return False
    except FileNotFoundError:
        print("Error: test-evaluation.py not found!")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run test evaluation on batch folders",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Evaluate latest batch
  python eval_batch.py
  
  # Evaluate specific batch
  python eval_batch.py --batch 2025-10-09_1
  
  # List all batches
  python eval_batch.py --list
        """
    )
    
    parser.add_argument('--batch', '-b', type=str,
                       help='Specific batch folder to evaluate (e.g., 2025-10-09_1)')
    parser.add_argument('--list', '-l', action='store_true',
                       help='List all available batch folders')
    
    args = parser.parse_args()
    
    if args.list:
        print("\n📊 Available Batch Folders:\n")
        batches = list_batch_folders()
        if batches:
            for folder_name, count in batches:
                print(f"  {folder_name} ({count} models)")
        else:
            print("  No batch folders found")
        print()
        return
    
    if args.batch:
        # Use specified batch
        batch_name = args.batch
    else:
        # Use latest batch
        latest = get_latest_batch_folder()
        if not latest:
            sys.exit(1)
        batch_name, _ = latest
        print(f"Using latest batch: {batch_name}")
    
    success = run_evaluation_on_batch(batch_name)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
