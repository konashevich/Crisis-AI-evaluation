import re

test_filenames = [
    "gemma-3-12b-it-Q8_0.gguf",
    "gemma-3-12b-it-Q4_K_M.gguf",
    "gemma-3-12b-it-Q6_K.gguf",
]

patterns = {
    "Old": r'-([QK]\d+_[KMS](_[KMS])?)\.gguf$',
    "New": r'-(Q\d+_(?:K(?:_[MS])?|\d))\.gguf$',
}

for pattern_name, pattern in patterns.items():
    print(f"\n{pattern_name} pattern: {pattern}")
    for filename in test_filenames:
        match = re.search(pattern, filename, re.IGNORECASE)
        print(f"  {filename}: {match.group(1) if match else 'NO MATCH'}")
