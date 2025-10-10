from batch_test_models import get_available_models

models = get_available_models()
gemma_variant = [m for m in models if 'google/gemma-3n-e4b@q4_k_m' == m['display_name']]

if gemma_variant:
    m = gemma_variant[0]
    print(f"Display: {m['display_name']}")
    print(f"ID: {m['id']}")
    print(f"Same? {m['display_name'] == m['id']}")
