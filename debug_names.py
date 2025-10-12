import json

# Load the report
with open('eval_results/gemini_evaluation_report_2025-10-12_08-07-40.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

metadata = data.get('model_metadata', {})
evaluations = data.get('evaluations', {})

# Get model names from evaluations
eval_model_names = set()
for category, subcats in evaluations.items():
    for subcat, entries in subcats.items():
        for entry in entries:
            if 'gemini_evaluation' in entry and 'evaluations' in entry['gemini_evaluation']:
                for eval_item in entry['gemini_evaluation']['evaluations']:
                    if 'model_name' in eval_item:
                        eval_model_names.add(eval_item['model_name'])

print("Model names in metadata:", len(metadata))
print("Model names in evaluations:", len(eval_model_names))

print("\nFirst 5 model names from evaluations:")
for i, name in enumerate(list(sorted(eval_model_names))[:5]):
    print(f"  {i+1}. '{name}'")
    print(f"     In metadata: {name in metadata}")
    if name in metadata:
        print(f"     Size: {metadata[name].get('model_size_gb')} GB")

print("\nFirst 5 model names from metadata:")
for i, name in enumerate(list(sorted(metadata.keys()))[:5]):
    print(f"  {i+1}. '{name}'")
    print(f"     In evaluations: {name in eval_model_names}")

# Check for name mismatches
print("\n=== Checking for name differences ===")
eval_not_in_meta = eval_model_names - set(metadata.keys())
meta_not_in_eval = set(metadata.keys()) - eval_model_names

if eval_not_in_meta:
    print(f"\nModels in evaluations but NOT in metadata ({len(eval_not_in_meta)}):")
    for name in sorted(list(eval_not_in_meta)[:5]):
        print(f"  - '{name}'")
        
if meta_not_in_eval:
    print(f"\nModels in metadata but NOT in evaluations ({len(meta_not_in_eval)}):")
    for name in sorted(list(meta_not_in_eval)[:5]):
        print(f"  - '{name}'")
