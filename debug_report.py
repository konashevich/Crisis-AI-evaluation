import json

# Load and inspect the evaluation report structure
with open('eval_results/gemini_evaluation_report_2025-10-12_08-07-40.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Top-level keys:", list(data.keys()))
print("\nHas model_metadata:", 'model_metadata' in data)

if 'model_metadata' in data:
    metadata = data['model_metadata']
    print(f"\nNumber of models with metadata: {len(metadata)}")
    
    # Show first 3 models
    print("\nFirst 3 models with metadata:")
    for i, (model_name, meta) in enumerate(list(metadata.items())[:3]):
        print(f"\n{i+1}. {model_name}")
        print(f"   Size GB: {meta.get('model_size_gb')}")
        print(f"   Size Bytes: {meta.get('model_size_bytes')}")
        print(f"   Quantization: {meta.get('model_quantization')}")
        print(f"   Duration: {meta.get('duration_seconds')}s")
        print(f"   All keys: {list(meta.keys())}")
