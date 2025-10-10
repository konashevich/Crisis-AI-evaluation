"""
Quick script to show which models have already been tested
"""
import os
import json
from datetime import datetime

RESULTS_DIR = 'test_results'
MODELS_FILE = 'models_to_test.txt'

def get_tested_models():
    """Get list of models that have test results"""
    if not os.path.exists(RESULTS_DIR):
        return {}
    
    tested = {}
    for filename in os.listdir(RESULTS_DIR):
        if filename.endswith('.json') and not filename.endswith('_runinfo.json'):
            # Extract model name and timestamp
            parts = filename.rsplit('_', 3)
            if len(parts) >= 4:
                model_name = parts[0]
                # Get file modification time
                filepath = os.path.join(RESULTS_DIR, filename)
                mtime = os.path.getmtime(filepath)
                date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
                
                if model_name not in tested or mtime > tested[model_name]['timestamp']:
                    tested[model_name] = {
                        'timestamp': mtime,
                        'date': date,
                        'file': filename
                    }
    
    return tested

def get_models_to_test():
    """Get list of models from models_to_test.txt"""
    if not os.path.exists(MODELS_FILE):
        return []
    
    with open(MODELS_FILE, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

def main():
    print("📊 Test Status Report\n")
    
    tested = get_tested_models()
    planned = get_models_to_test()
    
    if not planned:
        print("No models in models_to_test.txt")
        return
    
    print(f"Models in test list: {len(planned)}")
    print(f"Models with results: {len(tested)}\n")
    
    print("Status:")
    print("-" * 80)
    
    for model in planned:
        if model in tested:
            info = tested[model]
            print(f"✓ {model}")
            print(f"  Last tested: {info['date']}")
            print(f"  File: {info['file']}")
        else:
            print(f"⚠ {model} - NOT TESTED YET")
        print()
    
    untested = [m for m in planned if m not in tested]
    
    print("-" * 80)
    if untested:
        print(f"\n{len(untested)} model(s) still need testing:")
        for model in untested:
            print(f"  • {model}")
    else:
        print("\n✨ All models have been tested!")
    
    # Show any extra test results not in the plan
    tested_names = set(tested.keys())
    planned_names = set(planned)
    extra = tested_names - planned_names
    
    if extra:
        print(f"\n\nExtra test results (not in current plan):")
        for model in sorted(extra):
            print(f"  • {model} - {tested[model]['date']}")

if __name__ == "__main__":
    main()
