"""
Retroactively add model size information to existing runinfo files.
Scans a batch folder and updates all *_runinfo.json files with model sizes.
"""
import json
import os
import sys
from pathlib import Path
import re

def find_model_file_size(model_id, model_name=None, publisher=None):
    """
    Enhanced model file finder with better pattern matching.
    Returns tuple (file_path, size_bytes) or (None, None) if not found.
    """
    # Common LM Studio model directories on Windows
    home = Path.home()
    possible_paths = [
        home / ".cache" / "lm-studio" / "models",
        home / ".lmstudio" / "models",
        Path("C:/Users") / os.environ.get("USERNAME", "") / ".cache" / "lm-studio" / "models",
    ]
    
    # Extract model name parts for better matching
    model_parts = []
    
    # Add model_name if provided (from runinfo)
    if model_name:
        model_parts.append(model_name.lower())
        # Remove @quantization if present
        if '@' in model_name:
            base = model_name.split('@')[0]
            model_parts.append(base.lower())
    
    # Add model_id (from API)
    if model_id:
        # Remove publisher prefix if present
        if '/' in model_id:
            publisher_part, model_part = model_id.split('/', 1)
            model_parts.append(model_part.lower())
            model_parts.append(model_id.lower())
            
            # Special handling for qwen models with -2507
            # qwen3-4b-2507 -> qwen3-4b-instruct-2507
            if '-2507' in model_part.lower():
                instruct_variant = model_part.lower().replace('-2507', '-instruct-2507')
                model_parts.append(instruct_variant)
                thinking_variant = model_part.lower().replace('-2507', '-thinking-2507')
                model_parts.append(thinking_variant)
        else:
            model_parts.append(model_id.lower())
        
        # Remove @quantization suffix if present
        if '@' in model_id:
            base = model_id.split('@')[0]
            if '/' in base:
                _, model_part = base.split('/', 1)
                model_parts.append(model_part.lower())
            else:
                model_parts.append(base.lower())
    
    # Remove duplicates
    model_parts = list(set(model_parts))
    
    print(f"  Searching for patterns: {model_parts[:3]}...")
    
    # Try to find files matching the model name
    for base_path in possible_paths:
        if not base_path.exists():
            continue
        
        # Search recursively for .gguf files
        try:
            for gguf_file in base_path.rglob("*.gguf"):
                gguf_str = str(gguf_file).lower()
                gguf_name = gguf_file.name.lower()
                
                # Try matching against various model name patterns
                for model_part in model_parts:
                    # Clean up the model name for comparison
                    clean_model = model_part.replace('/', '-').replace('@', '-').replace('_', '-')
                    clean_filename = gguf_name.replace('_', '-').replace('.gguf', '')
                    
                    # Strategy 1: Exact match in filename or path
                    if clean_model in clean_filename or clean_model in gguf_str.replace('\\', '/'):
                        size_bytes = gguf_file.stat().st_size
                        return str(gguf_file), size_bytes
                    
                    # Strategy 2: Fuzzy match (remove all hyphens)
                    fuzzy_model = clean_model.replace('-', '')
                    fuzzy_filename = clean_filename.replace('-', '')
                    if len(fuzzy_model) > 5 and fuzzy_model in fuzzy_filename:
                        size_bytes = gguf_file.stat().st_size
                        return str(gguf_file), size_bytes
        except Exception as e:
            continue
    
    return None, None


def update_runinfo_file(runinfo_path):
    """
    Update a single runinfo file with model size data.
    Returns True if updated, False if skipped or failed.
    """
    try:
        # Load the runinfo file
        with open(runinfo_path, 'r', encoding='utf-8') as f:
            runinfo = json.load(f)
        
        # Check if already has size data
        if runinfo.get('model_size_bytes') is not None:
            print(f"  ✓ Already has size data ({runinfo.get('model_size_gb', 0):.2f} GB)")
            return False
        
        # Try to find the model file
        model_id = runinfo.get('model_id')
        model_name = runinfo.get('model_name')
        publisher = runinfo.get('model_publisher')
        
        model_file_path, model_size_bytes = find_model_file_size(model_id, model_name, publisher)
        
        if model_size_bytes:
            model_size_gb = model_size_bytes / (1024 ** 3)
            
            # Update the runinfo
            runinfo['model_file_path'] = model_file_path
            runinfo['model_size_bytes'] = model_size_bytes
            runinfo['model_size_gb'] = model_size_gb
            
            # Save back to file
            with open(runinfo_path, 'w', encoding='utf-8') as f:
                json.dump(runinfo, f, indent=2)
            
            print(f"  ✅ Updated with size: {model_size_gb:.2f} GB ({model_size_bytes:,} bytes)")
            return True
        else:
            print(f"  ❌ Could not find model file")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def update_batch_folder(batch_folder):
    """
    Update all runinfo files in a batch folder.
    """
    batch_path = Path(batch_folder)
    
    if not batch_path.exists():
        print(f"Error: Batch folder not found: {batch_folder}")
        return
    
    # Find all runinfo files
    runinfo_files = sorted(batch_path.glob('*_runinfo.json'))
    
    if not runinfo_files:
        print(f"No runinfo files found in {batch_folder}")
        return
    
    print(f"\n{'='*70}")
    print(f"Updating {len(runinfo_files)} runinfo files in: {batch_path.name}")
    print(f"{'='*70}\n")
    
    updated_count = 0
    already_had_count = 0
    failed_count = 0
    
    for runinfo_file in runinfo_files:
        model_name = runinfo_file.name.replace('_runinfo.json', '').split('_2025-')[0]
        print(f"\n{model_name}:")
        
        result = update_runinfo_file(runinfo_file)
        
        if result is True:
            updated_count += 1
        elif result is False:
            # Check if it already had data
            with open(runinfo_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if data.get('model_size_bytes') is not None:
                already_had_count += 1
            else:
                failed_count += 1
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"Summary:")
    print(f"{'='*70}")
    print(f"✅ Updated: {updated_count}")
    print(f"ℹ️  Already had data: {already_had_count}")
    print(f"❌ Failed to find: {failed_count}")
    print(f"📊 Total: {len(runinfo_files)}")
    print()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Retroactively add model sizes to runinfo files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update latest batch folder
  python update_model_sizes.py
  
  # Update specific batch folder
  python update_model_sizes.py --batch test_results/2025-10-11_1
        """
    )
    
    parser.add_argument('--batch', '-b', type=str,
                       help='Batch folder path (default: test_results/2025-10-11_1)')
    
    args = parser.parse_args()
    
    # Default to the batch folder we know has missing data
    batch_folder = args.batch or 'test_results/2025-10-11_1'
    
    update_batch_folder(batch_folder)


if __name__ == "__main__":
    main()
