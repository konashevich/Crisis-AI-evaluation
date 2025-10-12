import json
import os
from pathlib import Path

# Load the models config
with open('models_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

all_models = [m['display_name'] for m in config['models']]

# Get ALL tested models from the folder (from actual files)
base_dir = Path('test_results/2025-10-10_11')
tested_models_from_files = set()
models_with_errors = []

# Get from actual result files
for result_file in sorted(base_dir.glob('*.json')):
    if '_runinfo' in result_file.name:
        continue
    
    # Extract model name from filename
    model_name = result_file.name.replace('.json', '')
    # Remove timestamp: _2025-10-11_HH-MM-SS
    import re
    model_name = re.sub(r'_2025-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$', '', model_name)
    tested_models_from_files.add(model_name)
    
    # Check for errors
    results = json.load(open(result_file, encoding='utf-8'))
    total_q = 0
    err_q = 0
    
    for category, subcats in results.items():
        for subcat_name, qa_list in subcats.items():
            total_q += len(qa_list)
            for qa in qa_list:
                answer = qa.get('answer', '')
                if answer.startswith('ERROR') or answer.startswith('API Call Error'):
                    err_q += 1
    
    if err_q > 0:
        models_with_errors.append({
            'name': model_name,
            'errors': err_q,
            'total': total_q
        })

print("=" * 70)
print("DETAILED ANALYSIS OF TEST RUN 2025-10-10_11")
print("=" * 70)

print(f"\n📁 Files found in test_results/2025-10-10_11:")
print(f"   Total result files: {len(list(base_dir.glob('*.json'))) // 2}")  # Divide by 2 because of runinfo files

print(f"\n📋 Models in config: {len(all_models)}")
print(f"✅ Models tested: {len(tested_models_from_files)}")
print(f"❌ Models with errors: {len(models_with_errors)}")

# Now let's do a SMART comparison
# The config has names like "google/gemma-3-12b@q4_k_m" 
# But files are named "gemma-3-12b-q4_k_m"

def normalize_name(name):
    """Normalize model name for comparison"""
    # Remove publisher prefix
    if '/' in name:
        name = name.split('/')[-1]
    # Replace @ with - for file comparison
    name = name.replace('@', '-')
    # Replace _ with - for consistency
    name = name.replace('_', '-')
    return name.lower()

# Create normalized sets
config_normalized = {normalize_name(m): m for m in all_models}
tested_normalized = {normalize_name(m): m for m in tested_models_from_files}

# Find what's actually missing
truly_not_tested = []
for config_norm, config_orig in config_normalized.items():
    if config_norm not in tested_normalized:
        truly_not_tested.append(config_orig)

print("\n" + "=" * 70)
print("❌ MODELS WITH TIMEOUT ERRORS:")
print("=" * 70)
if models_with_errors:
    for model in models_with_errors:
        print(f"  • {model['name']}: {model['errors']}/{model['total']} errors")
else:
    print("  None!")

print("\n" + "=" * 70)
print("⏸️  MODELS NOT TESTED YET:")
print("=" * 70)
if truly_not_tested:
    for model in truly_not_tested:
        print(f"  • {model}")
else:
    print("  None! All models have been tested!")

print("\n" + "=" * 70)
print("✅ ALL TESTED MODELS (from actual files):")
print("=" * 70)
for model in sorted(tested_models_from_files):
    # Check if it has errors
    is_error = any(m['name'] == model for m in models_with_errors)
    status = "❌" if is_error else "✅"
    print(f"  {status} {model}")

# Generate new config ONLY for models that need rerun
models_to_rerun_names = [m['name'] for m in models_with_errors] + truly_not_tested

print("\n" + "=" * 70)
print(f"🔄 MODELS FOR NEXT RUN ({len(models_to_rerun_names)} total):")
print("=" * 70)

if models_to_rerun_names:
    for model_name in models_to_rerun_names:
        print(f"  • {model_name}")
    
    # Create new config
    new_config = {
        "last_updated": "2025-10-11T00:00:00",
        "models": []
    }
    
    # Add models that need rerun
    for model_name in models_to_rerun_names:
        # Find in original config - need to match normalized names
        model_norm = normalize_name(model_name)
        for orig_model in config['models']:
            if normalize_name(orig_model['display_name']) == model_norm:
                new_config['models'].append(orig_model)
                break
    
    with open('models_config_rerun.json', 'w', encoding='utf-8') as f:
        json.dump(new_config, f, indent=2)
    
    print("\n✅ Saved new config to: models_config_rerun.json")
else:
    print("  🎉 NONE! All models completed successfully!")
    print("\n  Your test run is COMPLETE!")
