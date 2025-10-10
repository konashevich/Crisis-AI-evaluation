# Batch Model Selection - All Variants Fix

## Problem
The batch test script was showing models with "(X variants)" notation but not expanding them into individual selectable items. For example:
- `google/gemma-3-12b (3 variants)` was shown as one item
- You couldn't select individual quantizations like Q4_K_M, Q6_K, or Q8_0

## Solution
Updated `get_available_models()` function to:

1. **Detect variant groups** - Models showing "(X variants)" in `lms ls` output
2. **Query each variant group** - Run `lms ls <model-name>` to get all variants
3. **Parse individual variants** - Extract each quantization (e.g., `@q4_k_m`, `@q6_k`, `@q8_0`)
4. **List all separately** - Each variant becomes a selectable item

## Result

### Before (32 models):
```
google/gemma-3-12b (3 variants)   ← Only 1 selectable item
qwen3-4b@q4_k_m                   ← Individual variants still shown
qwen3-4b@q6_k
qwen3-4b@q8_0
```

### After (42 models):
```
google/gemma-3-12b@q4_k_m         ← All 3 individually selectable
google/gemma-3-12b@q6_k
google/gemma-3-12b@q8_0
qwen3-4b@q4_k_m
qwen3-4b@q6_k
qwen3-4b@q8_0
```

## Examples of Expanded Models

Models that now show all variants:
- **google/gemma-3-12b** → 3 variants (Q4_K_M, Q6_K, Q8_0)
- **google/gemma-3n-e4b** → 3 variants (Q4_K_M, Q6_K, Q8_0)
- **microsoft/phi-4** → 1 variant (Q6_K)
- **microsoft/phi-4-mini-reasoning** → 2 variants (Q4_K_M, Q8_0)
- **microsoft/phi-4-reasoning-plus** → 2 variants (Q4_K_M, Q6_K)
- **qwen/qwen3-4b-2507** → 3 variants (Q4_K_M, Q6_K, Q8_0)
- **qwen/qwen3-4b-thinking-2507** → 3 variants (Q4_K_M, Q6_K, Q8_0)
- **deepseek/deepseek-r1-0528-qwen3-8b** → 1 variant (Q4_K_M)
- **mistralai/mistral-7b-instruct-v0.3** → 1 variant (Q4_K_M)

## Usage

When you run the batch test script now:

```bash
python batch_test_models.py
```

You'll see a checkbox list with ALL quantization variants:

```
Select models to test (use Space to select, Enter to confirm):
 ❯ ○ deepseek-r1-0528-qwen3-8b@q4_k_s
   ○ deepseek-r1-0528-qwen3-8b@q6_k
   ○ deepseek/deepseek-r1-0528-qwen3-8b@q4_k_m
   ○ google/gemma-3-12b@q4_k_m        ← Now individually selectable
   ○ google/gemma-3-12b@q6_k
   ○ google/gemma-3-12b@q8_0
   ○ qwen/qwen3-4b-2507@q4_k_m
   ○ qwen/qwen3-4b-2507@q6_k
   ○ qwen/qwen3-4b-2507@q8_0
   ...
```

Each variant can be checked/unchecked independently!

## Technical Details

The function now:
1. Parses `lms ls` output line by line
2. Detects regex pattern: `^([a-zA-Z0-9/_.-]+)\s+\((\d+)\s+variants?\)`
3. For each variant group, runs: `lms ls <base-model-name>`
4. Filters out headers ("Listing variants", "PARAMS", etc.)
5. Extracts model names with `@quantization` suffixes
6. Returns complete list with all variants expanded

## Benefits

✅ **Full control** - Select exactly which quantizations to test
✅ **Compare quantizations** - Test Q4 vs Q6 vs Q8 of same model
✅ **Save disk space** - Don't test all variants if you only need one
✅ **Accurate counts** - Shows true number of available models (42 vs 32)
