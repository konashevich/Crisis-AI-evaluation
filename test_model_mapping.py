from batch_test_models import get_available_models

models = get_available_models()
deepseek_models = [m for m in models if 'deepseek' in m['display_name'].lower() and '@' in m['display_name']]

print(f'Found {len(deepseek_models)} DeepSeek models with @ suffix:\n')
for m in deepseek_models[:5]:
    print(f"  Display: {m['display_name']}")
    print(f"  ID:      {m['id']}")
    print(f"  Mapped:  {'✓' if '/' in m['id'] else '✗'}")
    print()
