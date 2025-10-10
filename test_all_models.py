from batch_test_models import get_available_models

models = get_available_models()

# Test different categories
categories = {
    'Standalone models with @quant': [],
    'Simple models (no @, no /)': [],
    'Variant models (with / and @)': [],
}

for m in models:
    display = m['display_name']
    if '/' in display and '@' in display:
        categories['Variant models (with / and @)'].append(m)
    elif '@' in display and '/' not in display:
        categories['Standalone models with @quant'].append(m)
    else:
        categories['Simple models (no @, no /)'].append(m)

print("="*70)
print("MODEL MAPPING VERIFICATION - ALL MODELS")
print("="*70)

for category, model_list in categories.items():
    print(f"\n{category}: {len(model_list)} models")
    print("-" * 70)
    
    if not model_list:
        print("  (none)")
        continue
    
    mapped_count = 0
    unmapped = []
    
    for m in model_list:
        is_mapped = '/' in m['id'] and '.gguf' in m['id']
        if is_mapped:
            mapped_count += 1
        else:
            unmapped.append(m)
    
    print(f"  ✓ Mapped: {mapped_count}/{len(model_list)}")
    
    if unmapped:
        print(f"  ✗ Unmapped: {len(unmapped)}")
        for m in unmapped[:5]:  # Show first 5 unmapped
            print(f"    • {m['display_name']} → {m['id']}")
        if len(unmapped) > 5:
            print(f"    ... and {len(unmapped) - 5} more")

print("\n" + "="*70)
print("OVERALL SUMMARY")
print("="*70)

total = len(models)
mapped = sum(1 for m in models if '/' in m['id'] and '.gguf' in m['id'])
simple = len(categories['Simple models (no @, no /)'])
print(f"Total models: {total}")
print(f"Mapped to full paths: {mapped}")
print(f"Simple models (LM Studio resolves): {simple}")
print(f"Coverage: {(mapped + simple)/total*100:.1f}%")

# The critical ones are variant and @quant models
critical = len(categories['Variant models (with / and @)']) + len(categories['Standalone models with @quant'])
critical_mapped = sum(1 for m in categories['Variant models (with / and @)'] + categories['Standalone models with @quant'] if '/' in m['id'] and '.gguf' in m['id'])

print(f"\nCritical models (variants + @quant): {critical}")
print(f"Critical models mapped: {critical_mapped}")

if critical_mapped == critical:
    print("\n✅ SUCCESS! All critical models (variants and @quant) are mapped!")
    print("   Simple models will be resolved by LM Studio automatically.")
else:
    print(f"\n⚠ WARNING: {critical - critical_mapped} critical models are not mapped!")
