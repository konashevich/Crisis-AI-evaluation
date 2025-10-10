from batch_test_models import build_model_path_map, resolve_model_path

path_map = build_model_path_map()

test_cases = [
    "google/gemma-3-12b@q6_k",
    "google/gemma-3-12b@q4_k_m",
    "google/gemma-3-12b@q8_0",
    "deepseek-r1-0528-qwen3-8b@q4_k_s",
    "deepseek-r1-0528-qwen3-8b@q6_k",
    "deepseek/deepseek-r1-0528-qwen3-8b@q4_k_m",
]

print("Testing resolve_model_path():\n")
for variant_name in test_cases:
    resolved = resolve_model_path(variant_name, path_map)
    status = "✓" if "/" in resolved and ".gguf" in resolved else "✗"
    print(f"{status} {variant_name}")
    print(f"  → {resolved}")
    print()
