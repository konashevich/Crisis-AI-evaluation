# Batch Model Testing Guide

## Overview

The `batch_test_models.py` script allows you to automatically test multiple LLM models sequentially with an interactive terminal interface.

## Features

✨ **Interactive Model Selection** - Checkbox interface to select which models to test  
🔄 **Automatic Model Loading** - Loads and unloads models via LM Studio API  
💾 **Save Selections** - Remember your model selection for next run  
📊 **Progress Tracking** - Real-time progress for each model and question  
📝 **Summary Report** - See success/failure status and timing for all models  

## Prerequisites

1. **LM Studio** must be running with API server enabled:
   - Open LM Studio
   - Go to **Developer** tab
   - Click **Start Server**
   - Server should be at `http://localhost:1234`

2. **Python dependencies** installed:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
python batch_test_models.py
```

This will:
1. Connect to LM Studio
2. Discover available models
3. Show interactive checkbox list
4. Let you select models to test
5. Run all crisis questions for each model
6. Save results to `test_results/` folder

### Example Session

```
🤖 Crisis-AI Batch Model Tester

Connecting to LM Studio at: http://localhost:1234
🔍 Discovering models from LM Studio...
✓ Found 8 model(s)

? Select models to test (use Space to select, Enter to confirm):
 ❯◉ Phi-4-mini-reasoning-Q4_K_M
  ◉ Qwen3-4B-Instruct-2507-Q4_K_M
  ◯ gemma-2-2b-it-Q5_K_S
  ◉ Mistral-7B-Instruct-v0.3.Q4_K_M
  ◯ smollm2-1.7b-instruct

✓ 3 model(s) selected

? Save this selection for next time? Yes
✓ Saved selection to models_config.json

? Start batch testing? Yes

🚀 Starting Batch Test Run - 3 model(s)
Started at: 2025-10-09 15:30:00

[1/3] Testing: Phi-4-mini-reasoning-Q4_K_M
  → Unloading previous model...
  → Loading Phi-4-mini-reasoning-Q4_K_M...
  ✓ Model loaded
  → Running crisis questions test...
  ...
  ✓ Completed in 245 seconds

[2/3] Testing: Qwen3-4B-Instruct-2507-Q4_K_M
  ...

📊 Batch Test Summary
Total time: 738 seconds (12.3 minutes)

Results:
✓ Phi-4-mini-reasoning-Q4_K_M (245s)
✓ Qwen3-4B-Instruct-2507-Q4_K_M (280s)
✓ Mistral-7B-Instruct-v0.3.Q4_K_M (210s)

Success rate: 3/3

✨ All done!
```

## Configuration

### Environment Variables

- `LM_STUDIO_API_URL` - Override LM Studio API URL (default: `http://localhost:1234`)
- `CRISIS_QUESTIONS_FILE` - Custom questions file path

### Saved Selections

Your model selections are saved to `models_config.json`. On the next run, you'll be asked if you want to reuse the previous selection.

## Output Files

Results are saved to the `test_results/` directory:

- `<model-name>_<timestamp>.json` - Full Q&A results
- `<model-name>_<timestamp>_runinfo.json` - Run metadata (timing, model info)

## Troubleshooting

### "No models found"
- Ensure LM Studio is running
- Check that the API server is started (Developer → Start Server)
- Verify the server is at `http://localhost:1234`

### "Failed to load model"
- Make sure the model exists in LM Studio
- Check that you have enough RAM/VRAM for the model
- Try loading the model manually in LM Studio first

### Models not appearing in list
- Refresh LM Studio's model list
- Restart LM Studio
- Check that models are properly downloaded

## Tips

- **Start small**: Test with 1-2 models first to ensure everything works
- **Monitor resources**: Watch RAM/VRAM usage, especially with large models
- **Overnight runs**: Perfect for testing many models - just select all and let it run
- **Review logs**: Each model's output is saved independently for later analysis

## Integration with Other Scripts

The batch tester uses your existing `llm-crisis-questions-test.py` script, so all your configuration (system prompt, temperature, etc.) is respected.

After batch testing, use:
- `test-evaluation.py` - To evaluate model responses
- `html-report-generator.py` - To generate HTML reports from results

## Advanced Usage

### Without Interactive UI (headless)

If `questionary` is not installed, the script falls back to numbered selection:

```
Available Models:
  1. Phi-4-mini-reasoning-Q4_K_M
  2. Qwen3-4B-Instruct-2507-Q4_K_M
  3. gemma-2-2b-it-Q5_K_S

Enter model numbers (comma-separated, e.g., 1,3):
> 1,2
```

### Custom API URL

```bash
LM_STUDIO_API_URL=http://192.168.1.100:1234 python batch_test_models.py
```

## Support

For issues or questions, check:
- LM Studio documentation
- This repository's issues
- The main README.md
