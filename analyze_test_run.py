import json
import os
from pathlib import Path

# Load the models config
with open('models_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

all_models = [m['display_name'] for m in config['models']]

# Get tested models from the folder
base_dir = Path('test_results/2025-10-10_11')
tested_models = set()
models_with_errors = []

for runinfo_file in sorted(base_dir.glob('*_runinfo.json')):
    runinfo = json.load(open(runinfo_file, encoding='utf-8'))
    model_name = runinfo['model_name']
    tested_models.add(model_name)
    
    results_file = runinfo['results_file'].replace('\\', '/')
    if os.path.exists(results_file):
        results = json.load(open(results_file, encoding='utf-8'))
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
            models_with_errors.append(model_name)

# Find models not tested
not_tested = [m for m in all_models if m not in tested_models]

print("=" * 70)
print("ANALYSIS OF TEST RUN 2025-10-10_11")
print("=" * 70)
print(f"\nTotal models in config: {len(all_models)}")
print(f"Models tested: {len(tested_models)}")
print(f"Models with errors (timeout): {len(models_with_errors)}")
print(f"Models not tested yet: {len(not_tested)}")

print("\n" + "=" * 70)
print("MODELS WITH TIMEOUT ERRORS (need rerun with new settings):")
print("=" * 70)
for model in models_with_errors:
    print(f"  • {model}")

print("\n" + "=" * 70)
print("MODELS NOT TESTED YET:")
print("=" * 70)
for model in not_tested:
    print(f"  • {model}")

# Create the new models list for rerun
models_to_rerun = models_with_errors + not_tested

print("\n" + "=" * 70)
print(f"NEW CONFIG FOR RERUN ({len(models_to_rerun)} models total):")
print("=" * 70)
for model in models_to_rerun:
    print(f"  • {model}")

# Generate the new models_config.json for the rerun
new_config = {
    "last_updated": "2025-10-11T00:00:00",
    "models": []
}

# Add models with errors first
for model_name in models_with_errors:
    # Find the original entry
    for m in config['models']:
        if m['display_name'] == model_name:
            new_config['models'].append(m)
            break

# Add models not tested
for model_name in not_tested:
    for m in config['models']:
        if m['display_name'] == model_name:
            new_config['models'].append(m)
            break

# Save the new config
with open('models_config_rerun.json', 'w', encoding='utf-8') as f:
    json.dump(new_config, f, indent=2)

print("\n✓ Saved new config to: models_config_rerun.json")
print(f"\nTo use it, run:")
print(f"  mv models_config.json models_config_backup.json")
print(f"  mv models_config_rerun.json models_config.json")
print(f"  python batch_test_models.py")
