# Quick Start Guide

## 🚀 Fastest Way to Test Multiple Models

### 1. Run Batch Tests

```bash
python batch_test_models.py
```

**What happens:**
- Shows list of available models in LM Studio
- Use arrow keys to navigate, Space to select, Enter to confirm
- Creates batch folder (e.g., `test_results/2025-10-09_1/`)
- Automatically tests each selected model
- Saves results to batch folder

**Example output:**
```
? Select models to test:
  ◉ smollm2-360m-instruct-q8_0
  ◉ phi-3.5-mini-instruct-Q4_K_M
  ◯ qwen2.5-coder-1.5b-instruct-q8_0
  ◉ gemma-2-2b-it-Q5_K_S

🚀 Starting Batch Test Run - 3 model(s)
Results folder: 2025-10-09_1

[1/3] Testing: smollm2-360m-instruct
  ✓ Completed in 180 seconds
...
```

### 2. Evaluate Results

```bash
# See what batches you have
python eval_batch.py --list

# Evaluate latest batch
python eval_batch.py

# Or evaluate specific batch
python eval_batch.py --batch 2025-10-09_1
```

**Example output:**
```
📊 Available Batch Folders:

  2025-10-09_2 (5 models)
  2025-10-09_1 (3 models)
  2025-10-08_1 (8 models)

Using latest batch: 2025-10-09_2
...
```

### 3. View Report

#### 🚀 Interactive Viewer (Recommended)

```bash
# Just open it in your browser
start evaluation-viewer.html
```

Then **drag & drop** your JSON evaluation file or click to browse.

**Features:**
- ✅ No Python needed
- ✅ Works completely offline
- ✅ Load any evaluation JSON file
- ✅ Interactive score breakdowns
- ✅ Beautiful responsive design

#### Alternative: Generate Static HTML

```bash
# Generate static report with embedded data
python html-report-generator.py

# Open in browser
start evaluation_report.html
```

## 📋 Prerequisites

### Required

1. **Python 3.7+** with pip installed
2. **LM Studio** from [lmstudio.ai](https://lmstudio.ai)
3. **Gemini API Key** from [Google AI Studio](https://aistudio.google.com)

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key (Windows PowerShell)
$env:GEMINI_API_KEY="your-api-key-here"
```

## 🔧 Common Tasks

### Check Running Tests

```bash
python check_test_status.py
```

Shows progress of currently running batch tests.

### List Available Models

Models are auto-detected from LM Studio. The batch script will show all loaded models when you run it.

### Manual Single Model Test

If you want to test just one model manually:

```bash
# 1. Load model in LM Studio
# 2. Start the local server
# 3. Run test script
python llm-crisis-questions-test.py --model-name "model-name"
```

## 🎯 Best Practices

### Model Selection
- Start with smaller models (< 2GB) for quick testing
- Group similar models in one batch
- Run larger models separately or in small batches

### Naming Conventions
- Results: `model-name_YYYY-MM-DD_HH-MM-SS.json`
- Batches: `YYYY-MM-DD_N` (auto-generated)

### Batch Organization
- Each day starts with `_1`
- Multiple runs same day increment: `_2`, `_3`, etc.
- Keep batch folders for comparison
- Delete old batches when not needed

## 📊 Understanding Results

### Test Output Files

Each model test creates 2 files in the batch folder:

1. **`model-name_timestamp.json`** - Q&A results
   ```json
   {
     "model_name": "smollm2-360m-instruct",
     "questions_and_answers": [...]
   }
   ```

2. **`model-name_timestamp_runinfo.json`** - Metadata
   ```json
   {
     "model_name": "smollm2-360m-instruct",
     "test_duration_seconds": 180,
     "start_time": "2025-10-09 22:30:00"
   }
   ```

### Evaluation Report

The Gemini evaluation creates:
- **`gemini_evaluation_report_YYYY-MM-DD_HH-MM-SS.json`** - Raw scores
- **`evaluation_report.html`** - Interactive visual report

## 🐛 Troubleshooting

### "No models found in LM Studio"

**Solution:** Load at least one model in LM Studio first. The CLI (`lms ls`) lists loaded models, not all available models.

### Unicode errors in terminal

**Fixed:** The script now handles Unicode characters automatically with `errors='ignore'`.

### Timing seems off

**Fixed:** Timing now measures only model inference time, excluding file I/O overhead.

### Batch folder not found

**Solution:** Run `python eval_batch.py --list` to see available batches and their exact names.

### API key not recognized

**Solution:**
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-api-key-here"

# Windows CMD
set GEMINI_API_KEY=your-api-key-here

# Linux/Mac
export GEMINI_API_KEY="your-api-key-here"
```

## 📚 Documentation

For more details, see:
- [README.md](README.md) - Full project overview
- [AUTOMATED_BATCH_TESTING.md](AUTOMATED_BATCH_TESTING.md) - Complete automation guide
- [BATCH_ORGANIZATION.md](BATCH_ORGANIZATION.md) - Batch folder structure and workflows
- [TIMING_IMPROVEMENTS.md](TIMING_IMPROVEMENTS.md) - Timing accuracy details
- [FIXES_APPLIED.md](FIXES_APPLIED.md) - Technical fixes and solutions

## 💡 Tips

1. **Start Small**: Test 2-3 small models first to verify everything works
2. **Monitor Progress**: Use `check_test_status.py` for long-running batches
3. **Compare Batches**: Keep multiple batch folders to track improvements
4. **Save Reports**: Rename HTML reports to indicate what batch they're for
5. **Clean Up**: Delete old batch folders you don't need anymore

---

**Ready to start?** Just run:
```bash
python batch_test_models.py
```

That's it! 🎉
