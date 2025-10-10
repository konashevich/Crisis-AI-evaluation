# Model Loading Fix - Complete Solution

## Problem
The batch testing script was failing to load models with the error:
```
Model not found

No model found that matches path "deepseek-r1-0528-qwen3-8b@q4_k_s".
No model found that matches path "google/gemma-3-12b@q6_k".
```

This affected **ALL models with @ quantization suffixes** and **ALL variant models** (models shown with "N variants" in `lms ls`).

## Root Cause
The `lms ls` command shows **display aliases** for models, but the `lms load` command requires **full file paths**:

| What `lms ls` shows | What `lms load` needs |
|---------------------|----------------------|
| `deepseek-r1-0528-qwen3-8b@q4_k_s` | `unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF/DeepSeek-R1-0528-Qwen3-8B-Q4_K_S.gguf` |
| `google/gemma-3-12b@q6_k` | `lmstudio-community/gemma-3-12b-it-GGUF/gemma-3-12b-it-Q6_K.gguf` |

### Additional Complexity for Variants
Variant models have naming mismatches:
- `lms ls google/gemma-3-12b` shows variant: `google/gemma-3-12b@q6_k`
- But the actual file is: `gemma-3-12b-it-Q6_K.gguf` (note the added `-it`)

## Solution

1. **Scans the LM Studio models directory** (`~/.lmstudio/models`) to find all `.gguf` files
2. **Creates a mapping** from display aliases to actual loadable paths
3. **Handles multiple alias formats**:
   - Full filename alias: `deepseek-r1-0528-qwen3-8b-q4-k-s`
   - Quantization suffix alias: `deepseek-r1-0528-qwen3-8b@q4_k_s`
   - Publisher/model variants: `deepseek/deepseek-r1-0528-qwen3-8b@q4_k_m`

### Key regex for quantization detection:
```python
r'-([QK]\d+_[KMS](_[KMS])?)\.gguf$'
```

This correctly matches patterns like:
- `Q4_K_S` → `q4_k_s`
- `Q4_K_M` → `q4_k_m`
- `Q6_K` → `q6_k`
- `Q5_K_S` → `q5_k_s`

## Changes Made

### 1. New function: `build_model_path_map()`
Scans the models directory and builds alias → path mappings.

### 2. Updated: `get_available_models()`
Now uses the path map to convert display aliases to loadable paths:
```python
loadable_path = path_map.get(model_name.replace('/', '-').replace('_', '-').lower(), model_name)
models.append({
    'id': loadable_path,  # Full path for loading
    'display_name': model_name  # User-friendly name
})
```

### 3. Improved error messages in `load_model()`
Now shows the first 5 lines of errors instead of just 200 characters.

## Testing
```bash
# Test 1: Verify path mappings work
python test_path_map.py

# Test 2: Verify models get correct IDs
python test_model_mapping.py

# Test 3: Verify variant resolution
python test_variants.py

# Test 4: Verify specific model resolution
python test_resolve.py
```

### Expected Results:

**test_resolve.py output:**
```
✓ google/gemma-3-12b@q6_k
  → lmstudio-community/gemma-3-12b-it-GGUF/gemma-3-12b-it-Q6_K.gguf

✓ deepseek-r1-0528-qwen3-8b@q4_k_s
  → unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF/DeepSeek-R1-0528-Qwen3-8B-Q4_K_S.gguf
```

**test_variants.py output:**
```
Found 19 variant models:

  Display: google/gemma-3-12b@q6_k
  ID:      lmstudio-community/gemma-3-12b-it-GGUF/gemma-3-12b-it-Q6_K.gguf
  Mapped:  ✓
```

## Result
✅ DeepSeek models (and all other models with @ quantization suffixes) can now be loaded successfully
✅ The batch testing script will correctly map display names to loadable paths
✅ Users will see clearer error messages if loading still fails

## Files Modified
- `batch_test_models.py` - Added path mapping and improved error handling
- `test_path_map.py` - Created test script to verify path mappings
- `test_model_mapping.py` - Created test script to verify models get correct paths
- `test_regex.py` - Created regex testing script
- `docs/DEEPSEEK_LOAD_FIX.md` - This documentation file
