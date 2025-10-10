# 🎉 Fully Automated Batch Testing - NOW AVAILABLE!

## You Were Right!

After reviewing the LM Studio documentation, I discovered that **LM Studio has a powerful CLI** that supports automated model loading/unloading!

## What Changed

✅ **Now FULLY AUTOMATED** - No manual model switching needed!  
✅ **Uses `lms` CLI** - Programmatically loads and unloads models  
✅ **Interactive terminal UI** - Beautiful checkbox selection with questionary  
✅ **Discovers models automatically** - Reads from your LM Studio installation  

## Prerequisites

1. **Install LM Studio CLI:**
   ```bash
   npx lmstudio install-cli
   ```

2. **LM Studio must be running:**
   - Open LM Studio application
   - Go to Developer tab → Start Server
   - Leave it running in the background

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### Run the Automated Batch Tester

```bash
python batch_test_models.py
```

### What Happens:

1. **Auto-discovers models** from LM Studio:
   ```
   🔍 Discovering models from LM Studio...
   ✓ Found 19 model(s)
   ```

2. **Interactive selection** with checkboxes:
   ```
   ? Select models to test (Space=select, Enter=confirm):
    ❯◯ smollm2-360m-instruct
     ◯ smollm2-1.7b-instruct@q4_k_m
     ◉ phi-3.5-mini-instruct
     ◉ qwen2.5-1.5b-instruct
     ◯ microsoft/phi-4-mini-reasoning
   ```

3. **Fully automated testing:**
   ```
   [1/2] Testing: phi-3.5-mini-instruct
     → Unloading previous model...
     → Loading model...
     Loading via CLI: lms load 'phi-3.5-mini-instruct' --yes
     ✓ Model loaded
     → Running crisis questions test...
     ✓ Completed in 245 seconds
   
   [2/2] Testing: qwen2.5-1.5b-instruct
     → Unloading previous model...
     → Loading model...
     Loading via CLI: lms load 'qwen2.5-1.5b-instruct' --yes
     ✓ Model loaded
     → Running crisis questions test...
     ✓ Completed in 180 seconds
   ```

4. **Summary report:**
   ```
   📊 Batch Test Summary
   Total time: 425 seconds (7.1 minutes)
   
   Results:
   ✓ phi-3.5-mini-instruct (245s)
   ✓ qwen2.5-1.5b-instruct (180s)
   
   Success rate: 2/2
   ✨ All done!
   ```

## Features

### 🤖 Automatic Model Management
- Loads models via `lms load` CLI
- Unloads models via `lms unload --all` CLI
- No manual intervention required!

### 💾 Save & Reuse Selections
- Your model selection is saved to `models_config.json`
- On next run, you can reuse previous selection
- Skip models you've already tested

### 📊 Progress Tracking
- Real-time progress for each model
- Time tracking per model
- Success/failure status
- Error handling with continue option

### 🎨 Beautiful Terminal UI
- Colored output for easy reading
- Checkbox selection interface
- Progress indicators
- Clear status messages

## Example Workflow

### 1. First Run - Select Models

```bash
$ python batch_test_models.py

🤖 Crisis-AI Batch Model Tester
Connecting to LM Studio at: http://localhost:1234
🔍 Discovering models from LM Studio...
✓ Found 19 model(s)

? Select models to test:
 ❯◉ smollm2-360m-instruct
  ◉ smollm2-1.7b-instruct@q4_k_m
  ◉ qwen2.5-1.5b-instruct

✓ 3 model(s) selected

? Save this selection for next time? Yes
✓ Saved selection to models_config.json

? Start batch testing? Yes

🚀 Starting Batch Test Run - 3 model(s)
...
```

### 2. Subsequent Runs - Reuse Selection

```bash
$ python batch_test_models.py

? Use previous selection? (3 models) Yes
ℹ Using 3 previously selected models

Selected models:
  • smollm2-360m-instruct
  • smollm2-1.7b-instruct@q4_k_m
  • qwen2.5-1.5b-instruct

? Start batch testing? Yes
...
```

## Comparison: Old vs New

### ❌ Old Manual Way
1. Run script
2. Script prompts: "Load model X in LM Studio"
3. You click model in LM Studio
4. You press Enter
5. Script runs questions
6. **Repeat for each model** 😴

### ✅ New Automated Way
1. Run script **once**
2. Select models with checkboxes
3. Press Enter
4. **Go get coffee** ☕
5. Come back to completed results! 🎉

## Advanced Usage

### Environment Variables

```bash
# Custom LM Studio URL
LM_STUDIO_API_URL=http://localhost:5000 python batch_test_models.py

# Custom questions file
CRISIS_QUESTIONS_FILE=my_questions.json python batch_test_models.py
```

### Command Line Options

The script uses `lms` CLI with these options:
- `lms load <model> --yes` - Auto-confirm model loading
- `lms load <model> --quiet` - Suppress verbose output
- `lms unload --all` - Unload all models before loading next

### Model Loading Options

You can customize model loading by modifying the `load_model()` function:

```python
# In batch_test_models.py, modify the subprocess.run call:
result = subprocess.run(
    ["lms", "load", model_path, 
     "--yes",
     "--gpu", "max",              # Use max GPU
     "--context-length", "8192",  # Custom context
     "--quiet"],
    ...
)
```

## Troubleshooting

### "lms: command not found"

Install the CLI:
```bash
npx lmstudio install-cli
```

Then restart your terminal.

### "Failed to load model"

Possible causes:
1. LM Studio not running - Start it
2. API server not started - Enable in Developer tab
3. Not enough RAM/VRAM - Try smaller models
4. Model name mismatch - Check `lms ls` for correct names

### "No models found"

Run `lms ls` to verify models are installed:
```bash
lms ls
```

### Models take too long to load

The script has a 3-minute timeout for loading. If your models take longer:
1. Increase timeout in `load_model()` function
2. Use smaller quantized models (Q4_K_M instead of Q8_0)
3. Reduce context length with `--context-length`

## Performance Tips

### Run Overnight
Perfect for testing many models:
```bash
# Select all models you want to test
# Start before bed
# Wake up to completed results!
```

### Group by Size
Test models in size order:
- Small models (360M-2B) - ~5-15 mins each
- Medium models (3B-7B) - ~10-30 mins each  
- Large models (8B+) - ~30-60 mins each

### Monitor Resources
Use Task Manager / htop to watch:
- RAM usage (unload helps prevent OOM)
- GPU usage (shows when model is loaded)
- Disk usage (results files)

## Next Steps

After batch testing completes:

1. **Check test status:**
   ```bash
   python check_test_status.py
   ```

2. **Evaluate responses:**
   ```bash
   python test-evaluation.py
   ```

3. **Generate HTML reports:**
   ```bash
   python html-report-generator.py
   ```

4. **Compare models:**
   - Open generated HTML reports
   - See which models performed best
   - Identify strengths and weaknesses

## Files

### Created/Modified
- `batch_test_models.py` - **Now fully automated with CLI!**
- `models_config.json` - Saved model selections
- `test_results/` - Output directory with timestamped results

### Also Available
- `batch_test_simple.py` - Manual fallback (if CLI doesn't work)
- `check_test_status.py` - Progress tracker
- `models_to_test.txt` - Simple text file approach

## Credits

Thanks for pushing me to check the documentation! The LM Studio CLI makes this **so much better** than manual model switching.

🚀 Happy automated testing!
