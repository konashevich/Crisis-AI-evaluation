import re

test_filenames = [
    "DeepSeek-R1-0528-Qwen3-8B-Q4_K_S.gguf",
    "DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf",
    "DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf",
    "gemma-2-2b-it-Q5_K_S.gguf",
]

patterns = [
    r'-([QK][0-9]+[_-][KMS]+)\.gguf$',  # Original
    r'-([QK]\d+_[KMS](_[KMS])?)\.gguf$',  # New attempt
    r'-(Q\d+_K(_[MS])?|K\d+)\.gguf$',  # Another attempt
]

for pattern in patterns:
    print(f"\nPattern: {pattern}")
    for filename in test_filenames:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            print(f"  ✓ {filename} -> {match.group(1)}")
        else:
            print(f"  ✗ {filename} -> NO MATCH")
