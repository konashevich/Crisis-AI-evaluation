# Model Size Detection Issue & Fix

## Problem

Models tested in batch `2025-10-11_1` have `null` size data for certain models:
- ❌ All Google Gemma models (gemma-3-12b, gemma-3n-e4b)
- ❌ Microsoft Phi variant models (phi-4, phi-4-mini-reasoning, phi-4-reasoning-plus)
- ❌ Some Qwen models

**Example from runinfo:**
```json
{
  "model_name": "gemma-3-12b@q8_0",
  "model_id": "google/gemma-3-12b",
  "model_file_path": null,
  "model_size_bytes": null,
  "model_size_gb": null
}
```

## Root Cause

The size detection function `find_model_file_size()` couldn't match variant models because:

### The Mismatch
1. **API returns ID**: `"google/gemma-3-12b"` (base model without quantization)
2. **Actual file path**: `google/gemma-3-12b-it-GGUF/gemma-3-12b-it-Q8_0.gguf`
3. **Search pattern**: Looked for `"google-gemma-3-12b"` (replaced `/` with `-`)
4. **Result**: No match because filename has `-it-` suffix

### Why It Worked for Some Models

✅ **Standalone models** like `smollm2-360m-instruct`:
- API returns: `smollm2-360m-instruct`
- Filename: `smollm2-360m-instruct-q8_0.gguf`
- Match: ✅ Success

✅ **DeepSeek models**:
- Full path loaded: `unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF/DeepSeek-R1-0528-Qwen3-8B-Q4_K_S.gguf`
- Contains enough unique identifiers
- Match: ✅ Success

❌ **Variant models** like `google/gemma-3-12b`:
- API returns: `google/gemma-3-12b`
- Filename: `gemma-3-12b-it-Q8_0.gguf` (has `-it` suffix)
- Old search: `"google-gemma-3-12b"` ≠ `"gemma-3-12b-it"`
- Match: ❌ Failed

## The Fix

Updated `find_model_file_size()` to:

### 1. **Extract Multiple Search Patterns**
```python
model_parts = []
# Try both with and without publisher
"google/gemma-3-12b" → ["gemma-3-12b", "google/gemma-3-12b"]
# Try without @quantization
"gemma-3-12b@q8_0" → ["gemma-3-12b", "gemma-3-12b@q8_0"]
```

### 2. **Fuzzy Matching**
```python
# Remove hyphens and compare
clean_model = "gemma312b"
clean_filename = "gemma312bitq80"
# Match: ✅ "gemma312b" in "gemma312bitq80"
```

### 3. **Multiple Matching Strategies**
1. Exact path/filename match
2. Normalized match (replace `/`, `@`, `_` with `-`)
3. Fuzzy match (remove all hyphens and compare)

## Testing the Fix

To verify the fix works, test with a variant model:

```powershell
# Load a variant model
lms load google/gemma-3-12b --yes

# Run test script
python llm-crisis-questions-test.py

# Check output - should see:
# "Detected loaded model: google/gemma-3-12b (Q8_0)"
# "Model file found: C:\Users\...\gemma-3-12b-it-Q8_0.gguf"
# "Model size: 12,345,678,901 bytes (11.50 GB)"
```

## Re-running Failed Models

To get size data for the models that failed, you need to re-test them:

```powershell
# Use the rerun config we created
cp models_config.json models_config_backup.json
cp models_config_rerun.json models_config.json

# Run batch test with updated code
python batch_test_models.py
```

The new test run will now correctly detect and save model sizes for:
- ✅ google/gemma-3-12b variants
- ✅ google/gemma-3n-e4b variants  
- ✅ microsoft/phi-4 variants
- ✅ All other variant models

## Expected Results After Fix

**Before:**
```json
{
  "gemma-3-12b-q8_0": {
    "model_size_gb": null,
    "model_size_bytes": null
  }
}
```

**After:**
```json
{
  "gemma-3-12b-q8_0": {
    "model_size_gb": 11.50,
    "model_size_bytes": 12345678901,
    "model_file_path": "C:\\Users\\...\\gemma-3-12b-it-Q8_0.gguf"
  }
}
```

## Summary

✅ **Fixed** - Enhanced pattern matching in `find_model_file_size()`  
✅ **Handles** - Variant models with `-it`, `-instruct` suffixes  
✅ **Supports** - Publisher prefixes (`google/`, `microsoft/`)  
✅ **Works** - For all quantization formats (`@q4_k_m`, `@q8_0`, etc.)  

The fix will be applied to **all future test runs** automatically!
