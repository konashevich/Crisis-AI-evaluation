import json
import os
from pathlib import Path

base_dir = Path('test_results/2025-10-10_11')
models_with_errors = []
models_completed = []

for runinfo_file in sorted(base_dir.glob('*_runinfo.json')):
    runinfo = json.load(open(runinfo_file, encoding='utf-8'))
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
            models_with_errors.append({
                'name': runinfo['model_name'],
                'errors': err_q,
                'total': total_q,
                'display_name': runinfo.get('model_name', 'unknown')
            })
        else:
            models_completed.append(runinfo['model_name'])

print("=" * 70)
print("MODELS WITH ERRORS (need to be rerun):")
print("=" * 70)
for model in models_with_errors:
    print(f"  {model['name']}: {model['errors']}/{model['total']} errors")

print(f"\n{len(models_with_errors)} models had errors")
print(f"{len(models_completed)} models completed successfully")

print("\n" + "=" * 70)
print("SUCCESSFULLY COMPLETED MODELS:")
print("=" * 70)
for model in models_completed:
    print(f"  ✓ {model}")
