# Model Size Tracking Implementation

## Overview
The Crisis-AI evaluation system now automatically tracks and displays model sizes in GB throughout the entire pipeline.

## How It Works

### 1. Test Script (`llm-crisis-questions-test.py`)
When you run a test on a model:

1. **Auto-detects loaded model** via LM Studio API (`/api/v0/models`)
2. **Finds the .gguf file** on disk in LM Studio's cache directories
3. **Reads the file size** in bytes
4. **Saves metadata** to `_runinfo.json` including:
   - `model_size_bytes` - Exact file size
   - `model_size_gb` - Size in GB (decimal)
   - `model_quantization` - e.g., Q4_K_M, Q8_0
   - `model_arch` - e.g., llama, qwen3
   - `model_publisher` - e.g., HuggingFaceTB
   - `model_file_path` - Full path to the .gguf file

**Example runinfo:**
```json
{
  "model_name": "smollm2-360m-instruct",
  "model_size_bytes": 386404992,
  "model_size_gb": 0.36,
  "model_quantization": "Q8_0",
  "model_arch": "llama",
  "model_publisher": "HuggingFaceTB"
}
```

### 2. Batch Test Script (`batch_test_models.py`)
When running batch tests:

1. **Loads each model** in sequence
2. **Calls main test script** which auto-detects and saves size
3. **Reads runinfo** after each test completes
4. **Displays size** during execution
5. **Shows in summary** with format: `✓ model-name (45s, 0.98 GB)`

### 3. Evaluation Script (`test-evaluation.py`)
When evaluating test results:

1. **Loads all test result files** from batch folder
2. **Reads corresponding `_runinfo.json`** files
3. **Extracts model metadata** including size
4. **Includes in evaluation report** with new structure:

```json
{
  "model_metadata": {
    "smollm2-360m-instruct": {
      "model_size_gb": 0.36,
      "model_size_bytes": 386404992,
      "model_quantization": "Q8_0",
      "model_arch": "llama",
      "model_publisher": "HuggingFaceTB"
    }
  },
  "evaluations": {
    "Natural Disasters": { ... }
  }
}
```

### 4. HTML Viewer (`evaluation-viewer.html`)
The web viewer displays model sizes:

1. **Reads both old and new report formats**
   - Old: Just evaluations at root
   - New: `model_metadata` + `evaluations`

2. **Shows size in summary cards**:
   ```
   ┌─────────────────────────┐
   │ smollm2-360m-instruct #1│
   │ 7.85                    │
   │ Average Score (32 qs)   │
   │ 0.36 GB (Q8_0)         │
   └─────────────────────────┘
   ```

3. **Backwards compatible** - works with old reports that don't have metadata

## Usage

### Running Tests
```bash
# Single model test (auto-detects size)
python llm-crisis-questions-test.py

# Batch test (auto-detects all sizes)
python batch_test_models.py
```

### Viewing Results
```bash
# Evaluate batch and generate report with metadata
python eval_batch.py --batch 2025-10-10_1

# View in browser
python -m http.server 8000
# Open: http://localhost:8000/evaluation-viewer.html
```

## File Locations

### Model Size Detection
The script searches these directories for .gguf files:
- `~/.cache/lm-studio/models/`
- `~/.lmstudio/models/`
- `C:/Users/{USERNAME}/.cache/lm-studio/models/`

### Output Files
- **Test results**: `test_results/YYYY-MM-DD_N/model-name_timestamp.json`
- **Runinfo**: `test_results/YYYY-MM-DD_N/model-name_timestamp_runinfo.json`
- **Evaluation**: `eval_results/gemini_evaluation_report_timestamp.json`

## Troubleshooting

### "Model size: None" in runinfo
- Model file not found in expected directories
- Check LM Studio's model directory settings
- File search uses lowercase model ID matching

### Missing sizes in HTML viewer
- Old evaluation report format (before this update)
- Re-run evaluation with updated `test-evaluation.py`
- Or manually add `model_metadata` section to JSON

### Incorrect sizes
- File may be split or symlinked
- Verify actual .gguf file location
- Check `model_file_path` in runinfo

## Benefits

1. **No manual input** - Everything is automatic
2. **Accurate sizes** - Reads from actual files on disk
3. **Full metadata** - Quantization, architecture, publisher
4. **Persistent tracking** - Saved in runinfo and evaluation reports
5. **Visual comparison** - Easy to compare model size vs performance

## Example Output

**Batch Summary:**
```
📊 Batch Test Summary
Total time: 305 seconds (5.1 minutes)

Results:
✓ smollm2-360m-instruct (102s, 0.36 GB)
✓ gemma-2-2b-it (156s, 2.48 GB)
✓ qwen3-4b (245s, 4.12 GB)

Success rate: 3/3
```

**HTML Viewer:**
- Model cards show size below score
- Format: `X.XX GB (QUANTIZATION)`
- Sorted by score, not size
