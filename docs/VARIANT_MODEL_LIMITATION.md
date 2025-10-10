# LM Studio Variant Model Limitation

## Issue Discovered
LM Studio CLI has a **fundamental limitation** where variant models cannot have specific quantizations loaded programmatically.

### What are Variant Models?
Models that appear in `lms ls` with "(N variants)" suffix:
- `google/gemma-3-12b (3 variants)`
- `google/gemma-3n-e4b (3 variants)`
- `deepseek/deepseek-r1-0528-qwen3-8b (1 variant)`
- `microsoft/phi-4-mini-reasoning (2 variants)`

When you list these with `lms ls google/gemma-3-12b`, you see:
```
google/gemma-3-12b@q4_k_m
google/gemma-3-12b@q6_k
google/gemma-3-12b@q8_0
```

### The Problem
**None of these commands work:**
- ✗ `lms load "google/gemma-3-12b@q6_k" --yes` → "Model not found"
- ✗ `lms load "lmstudio-community/gemma-3-12b-it-GGUF/gemma-3-12b-it-Q6_K.gguf" --yes` → "Model not found"
- ✗ `lms load "gemma-3-12b-it-Q6_K.gguf" --yes` → "Model not found"

**Only this works:**
- ✓ `lms load "google/gemma-3-12b" --yes` → Loads **default/first variant** (Q4_K_M)

### Root Cause
1. **CLI limitation**: `lms load` doesn't accept `@quantization` suffix for variant models
2. **Publisher limitation**: Full paths don't work for `lmstudio-community` publisher models
3. **API limitation**: The `/v1/models` API endpoint only shows base model IDs, not variant-specific IDs

### Workaround Implemented
For variant models, the batch tester will:
1. Use the base model name (without `@quant`)
2. Display a warning that the default quantization will be loaded
3. Note which quantization was requested but couldn't be guaranteed

### What Works
**Standalone @quant models** (no "N variants" suffix) work perfectly:
- ✓ `deepseek-r1-0528-qwen3-8b@q4_k_s` → Maps to full path → Loads specific quant
- ✓ `qwen3-8b@q6_k` → Maps to full path → Loads specific quant
- ✓ `smollm2-1.7b-instruct@q8_0` → Maps to full path → Loads specific quant

### Recommendation
For users who need **specific quantization control**, download models from publishers that offer standalone @quant versions:
- `unsloth/*` - Often provides standalone quantizations
- `bartowski/*` - Provides standalone quantizations
- Avoid `lmstudio-community/*` variant models if you need quant control

### Example
```bash
# This works - standalone @quant model
lms ls | grep "deepseek-r1.*@q4_k_s"
# Output: deepseek-r1-0528-qwen3-8b@q4_k_s    8B    qwen3    4.80 GB
# Can load specific quant: ✓

# This doesn't work - variant model
lms ls | grep "google/gemma-3-12b"
# Output: google/gemma-3-12b (3 variants)    12B    gemma3    8.15 GB
# Cannot load specific quant from variants: ✗
```

## Solution Status
✅ Standalone @quant models: 100% working with specific quantization control
⚠️  Variant models: Working but loads default quantization only (LM Studio limitation)
