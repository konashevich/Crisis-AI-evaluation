import json

with open('eval_results/gemini_evaluation_report_2025-10-12_08-07-40.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

metadata = data.get('model_metadata', {})

# Check which models have None for size
models_with_none = []
models_with_size = []

for name, meta in metadata.items():
    if meta.get('model_size_gb') is None:
        models_with_none.append((name, meta))
    else:
        models_with_size.append((name, meta.get('model_size_gb')))

print(f"Models WITH size data: {len(models_with_size)}")
print(f"Models WITHOUT size data: {len(models_with_none)}")

if models_with_none:
    print("\n=== Models with NULL size ===")
    for name, meta in models_with_none[:10]:
        print(f"\n{name}:")
        print(f"  Metadata: {meta}")
