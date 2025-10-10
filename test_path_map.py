"""Test the model path mapping"""
import os
import pathlib
import re

def build_model_path_map():
    """Build a mapping of model aliases to their actual file paths."""
    models_dir = pathlib.Path(os.path.expanduser("~/.lmstudio/models"))
    if not models_dir.exists():
        # Try Windows path
        models_dir = pathlib.Path(os.path.expanduser(r"~\.lmstudio\models"))
    
    if not models_dir.exists():
        print(f"Models directory not found: {models_dir}")
        return {}
    
    print(f"Scanning: {models_dir}\n")
    path_map = {}
    
    # Scan all .gguf files
    for gguf_file in models_dir.rglob("*.gguf"):
        # Build the loadable path: publisher/repo/filename.gguf
        relative_path = gguf_file.relative_to(models_dir)
        parts = relative_path.parts
        
        if len(parts) >= 2:
            # Create the full path for lms load
            full_path = str(relative_path).replace('\\', '/')
            
            # Create alias from filename (lowercase, remove .gguf)
            filename = parts[-1]
            # Convert to alias format: remove .gguf, lowercase, replace _ with -
            alias = filename.replace('.gguf', '').lower().replace('_', '-')
            
            # Also try with just the quantization as @suffix
            # e.g., DeepSeek-R1-0528-Qwen3-8B-Q4_K_S.gguf -> deepseek-r1-0528-qwen3-8b@q4_k_s
            quant_match = re.search(r'-([QK]\d+_[KMS](_[KMS])?)\.gguf$', filename, re.IGNORECASE)
            if quant_match:
                base_name = filename[:quant_match.start()].lower().replace('_', '-')
                quant = quant_match.group(1).lower()  # Keep underscores in quantization
                alias_with_quant = f"{base_name}@{quant}"
                path_map[alias_with_quant] = full_path
            
            path_map[alias] = full_path
    
    return path_map

if __name__ == "__main__":
    path_map = build_model_path_map()
    
    print(f"Found {len(path_map)} model path mappings\n")
    
    # Show deepseek models specifically
    print("DeepSeek models:")
    for alias, path in path_map.items():
        if 'deepseek' in alias.lower():
            print(f"  {alias} -> {path}")
    
    print("\nTesting specific aliases:")
    test_aliases = [
        "deepseek-r1-0528-qwen3-8b@q4_k_s",
        "deepseek-r1-0528-qwen3-8b@q6_k",
    ]
    for alias in test_aliases:
        if alias in path_map:
            print(f"  ✓ {alias} -> {path_map[alias]}")
        else:
            print(f"  ✗ {alias} NOT FOUND")
