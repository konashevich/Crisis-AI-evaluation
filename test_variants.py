from batch_test_models import get_available_models

models = get_available_models()
variant_models = [m for m in models if '/' in m['display_name'] and '@' in m['display_name']]

print(f'Found {len(variant_models)} variant models:\n')
for m in variant_models:  # Show ALL, not just first 10
    mapped = '✓' if '/' in m['id'] and '.gguf' in m['id'] else '✗'
    print(f"{mapped} {m['display_name']}")
    if mapped == '✗':
        print(f"  → {m['id']}")

# Summary
total = len(variant_models)
mapped = sum(1 for m in variant_models if '/' in m['id'] and '.gguf' in m['id'])
print(f"\n{'='*60}")
print(f"Summary: {mapped}/{total} variant models mapped successfully")
if mapped < total:
    print(f"⚠ WARNING: {total - mapped} variant models NOT mapped!")
    unmapped = [m for m in variant_models if not ('/' in m['id'] and '.gguf' in m['id'])]
    print("\nUnmapped models:")
    for m in unmapped:
        print(f"  ✗ {m['display_name']} → {m['id']}")
else:
    print("✓ All variant models mapped correctly!")
