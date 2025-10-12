# Test Run Analysis: 2025-10-10_11

## Summary

**Total Models in Config:** 38  
**Models Tested:** 34  
**Successfully Completed:** 32  
**Failed with Timeout Errors:** 2  
**Not Tested Yet:** 21  
**Models for Next Run:** 23  

---

## 1. Models with Timeout Errors (Fixed with recent code update)

These 2 models failed due to the **5-minute timeout** issue that has been addressed:

1. **phi-4-reasoning-plus@q4_k_m** - 30/32 questions timed out
2. **phi-4-reasoning-plus@q6_k** - 32/32 questions timed out

**Root Cause:** These are reasoning models that generate extensive `<think>` tags with internal reasoning, causing responses to take >5 minutes per question.

**Fix Applied:** 
- Increased timeout from 300s (5min) → 600s (10min)
- Reduced max_tokens from 4096 → 2048 to limit excessive reasoning chains

---

## 2. Models Not Tested Yet (21 models)

These models weren't included in the previous test run:

### Gemma Variants (6 models)
- google/gemma-3-12b@q4_k_m
- google/gemma-3-12b@q6_k
- google/gemma-3-12b@q8_0
- google/gemma-3n-e4b@q4_k_m
- google/gemma-3n-e4b@q6_k
- google/gemma-3n-e4b@q8_0

### Phi Variants (5 models)
- microsoft/phi-4@q6_k
- microsoft/phi-4-mini-reasoning@q4_k_m
- microsoft/phi-4-mini-reasoning@q8_0
- microsoft/phi-4-reasoning-plus@q4_k_m
- microsoft/phi-4-reasoning-plus@q6_k

### Qwen Variants (7 models)
- qwen/qwen3-4b-2507@q4_k_m
- qwen/qwen3-4b-2507@q6_k
- qwen/qwen3-4b-2507@q8_0
- qwen/qwen3-4b-thinking-2507@q4_k_m
- qwen/qwen3-4b-thinking-2507@q6_k
- qwen/qwen3-4b-thinking-2507@q8_0
- qwen3-8b@q8_0

### SmolLM Variants (3 models)
- smollm2-1.7b-instruct@q4_k_m
- smollm2-1.7b-instruct@q8_0
- smollm2-360m-instruct

---

## 3. Successfully Completed Models (32 models)

✓ deepseek-r1-0528-qwen3-8b@q4_k_s
✓ deepseek-r1-0528-qwen3-8b@q6_k
✓ gemma-2-2b-it
✓ gemma-3-12b@q4_k_m
✓ gemma-3-12b@q6_k
✓ gemma-3-12b@q8_0
✓ gemma-3n-e4b@q4_k_m
✓ gemma-3n-e4b@q6_k
✓ gemma-3n-e4b@q8_0
✓ llama-3.2-3b-instruct
✓ phi-3.5-mini-instruct@q4_k_m
✓ phi-3.5-mini-instruct@q8_0
✓ phi-4-mini-reasoning@q4_k_m
✓ phi-4-mini-reasoning@q8_0
✓ phi-4@q6_k
✓ qwen2-500m-instruct
✓ qwen2.5-1.5b-instruct
✓ qwen2.5-coder-1.5b-instruct
✓ qwen2.5-coder-3b-instruct-ts
✓ qwen3-0.6b
✓ qwen3-1.7b
✓ qwen3-4b-2507@q4_k_m
✓ qwen3-4b-2507@q6_k
✓ qwen3-4b-2507@q8_0
✓ qwen3-4b@q4_k_m
✓ qwen3-4b@q6_k
✓ qwen3-4b@q8_0
✓ qwen3-4b-thinking-2507@q4_k_m
✓ qwen3-4b-thinking-2507@q6_k
✓ qwen3-4b-thinking-2507@q8_0
✓ qwen3-8b@q4_k_m
✓ qwen3-8b@q6_k

---

## Next Steps

A new config file has been generated: **`models_config_rerun.json`**

This contains 23 models:
- 2 models that failed (to rerun with new timeout settings)
- 21 models that weren't tested yet

### To run the next batch:

```powershell
# Backup current config
mv models_config.json models_config_backup.json

# Use the rerun config
mv models_config_rerun.json models_config.json

# Run the batch test with the updated code
python batch_test_models.py
```

The updated `llm-crisis-questions-test.py` now has:
- ✅ 10-minute timeout (up from 5 minutes)
- ✅ 2048 max_tokens (down from 4096)

This should handle the reasoning models properly.
