# Quick Start: Batch Testing Multiple Models

## Two Scripts Available

### 1. `batch_test_simple.py` - **RECOMMENDED** ⭐
Manual model loading - you switch models in LM Studio UI between tests.

**Best for:** Most users, guaranteed compatibility with LM Studio

### 2. `batch_test_models.py` - Automatic (Experimental)
Attempts to load/unload models via API (may not work with all LM Studio versions).

---

## Using `batch_test_simple.py` (Recommended)

### Quick Start

```bash
python batch_test_simple.py
```

### How It Works

1. **First Run**: Enter model names you want to test:
   ```
   Model 1: Phi-4-mini-reasoning-Q4_K_M
   Model 2: Qwen3-4B-Instruct-2507-Q4_K_M  
   Model 3: Mistral-7B-Instruct-v0.3.Q4_K_M
   Model 4: (press Enter to finish)
   ```
   
   Your list is saved to `models_to_test.txt` for next time.

2. **Script Prompts**: For each model, you'll see:
   ```
   ======================================================================
   Please load model in LM Studio: Phi-4-mini-reasoning-Q4_K_M
   Steps:
     1. Open LM Studio
     2. Click on the model you want to test
     3. Wait for it to load completely
   ======================================================================
   
   Press Enter when the model is loaded and ready...
   ```

3. **Load in LM Studio**: 
   - Click the model in LM Studio
   - Wait for "Model loaded" message
   - Return to terminal and press Enter

4. **Test Runs**: Script runs all questions, saves results, then asks for next model

5. **Repeat**: Load next model, press Enter, repeat

### Example Session

```
🤖 Crisis-AI Batch Model Tester (Manual Loading)
✓ Connected to LM Studio

Found saved list with 3 models:
  1. Phi-4-mini-reasoning-Q4_K_M
  2. Qwen3-4B-Instruct-2507-Q4_K_M
  3. Mistral-7B-Instruct-v0.3.Q4_K_M

Use this list? Yes

Will test 3 models:
  1. Phi-4-mini-reasoning-Q4_K_M
  2. Qwen3-4B-Instruct-2507-Q4_K_M
  3. Mistral-7B-Instruct-v0.3.Q4_K_M

Start testing? Yes

[1/3] Model: Phi-4-mini-reasoning-Q4_K_M
Please load model in LM Studio: Phi-4-mini-reasoning-Q4_K_M
...
(load model in LM Studio, press Enter)
✓ Detected model
→ Running crisis questions test...
✓ Completed in 245 seconds

[2/3] Model: Qwen3-4B-Instruct-2507-Q4_K_M
...
```

### Tips

- **Edit `models_to_test.txt`** anytime to change your list
- **Comments allowed**: Lines starting with `#` are ignored
- **Resume after interruption**: Just re-run the script, skip completed models
- **Overnight testing**: Perfect for unattended runs - check back in the morning!

---

## Model Names

Use the names exactly as they appear in your `test_results/` folder from previous tests, for example:

```
Phi-4-mini-reasoning-Q4_K_M
Qwen3-4B-Instruct-2507-Q4_K_M
gemma-2-2b-it-Q5_K_S
Mistral-7B-Instruct-v0.3.Q4_K_M
smollm2-1.7b-instruct
```

The name is just used for the output filename - doesn't need to match LM Studio's internal name.

---

## Troubleshooting

**"Cannot connect to LM Studio"**
- Start LM Studio
- Go to Developer tab → Start Server

**Want to skip a model?**
- Press Ctrl+C when prompted
- Choose "Skip this model and continue"

**Change model list?**
- Edit `models_to_test.txt` OR
- Delete `models_to_test.txt` and re-run script

---

## Output

Results saved to `test_results/`:
- `<model-name>_<timestamp>.json` - Full Q&A
- `<model-name>_<timestamp>_runinfo.json` - Metadata

Use with other scripts:
- `test-evaluation.py` - Evaluate answers
- `html-report-generator.py` - Generate HTML reports
