# Batch Results Organization - Complete Guide

## Overview

Test results are now organized in timestamped batch folders for better management and tracking.

## Folder Structure

```
test_results/
├── 2025-10-09_1/     ← First batch run on Oct 9
│   ├── smollm2-360m-instruct_2025-10-09_22-30-00.json
│   ├── smollm2-360m-instruct_2025-10-09_22-30-00_runinfo.json
│   ├── phi-3.5-mini-instruct_2025-10-09_22-35-15.json
│   └── phi-3.5-mini-instruct_2025-10-09_22-35-15_runinfo.json
├── 2025-10-09_2/     ← Second batch run on Oct 9
│   ├── qwen2.5-1.5b-instruct_2025-10-09_23-15-00.json
│   └── ...
└── 2025-10-10_1/     ← First batch run on Oct 10
    └── ...
```

**Format**: `YYYY-MM-DD_N` where N is incremental for same-day runs

## Workflows

### 1. Run Batch Tests

```bash
python batch_test_models.py
```

**Output:**
```
🚀 Starting Batch Test Run - 3 model(s)
Started at: 2025-10-09 22:30:00
Results folder: 2025-10-09_1         ← Auto-created batch folder

[1/3] Testing: smollm2-360m-instruct
  → Unloading previous model...
  → Loading model...
  ✓ Model loaded
  → Running crisis questions test...
  ✓ Completed in 180 seconds

...

✨ All done!
```

Results saved to: `test_results/2025-10-09_1/`

### 2. List Available Batches

```bash
python eval_batch.py --list
```

**Output:**
```
📊 Available Batch Folders:

  2025-10-10_1 (5 models)
  2025-10-09_2 (3 models)
  2025-10-09_1 (8 models)
```

### 3. Evaluate Latest Batch

```bash
python eval_batch.py
```

**Output:**
```
Using latest batch: 2025-10-10_1

======================================================================
Evaluating Batch: 2025-10-10_1
Location: test_results\2025-10-10_1
Models: 5
======================================================================

Using batch folder from environment: test_results\2025-10-10_1
Found 5 model result files
...
```

### 4. Evaluate Specific Batch

```bash
python eval_batch.py --batch 2025-10-09_1
```

**Output:**
```
======================================================================
Evaluating Batch: 2025-10-09_1
Location: test_results\2025-10-09_1
Models: 8
======================================================================

...
```

## Modified Scripts

### `batch_test_models.py`

**New Function:**
```python
def create_batch_folder() -> str:
    """
    Create a new batch folder in test_results with format YYYY-MM-DD_N
    where N is incremental for same-day runs.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Find existing folders for today
    existing = [...]
    
    # Get next number
    next_num = max(existing) + 1 if existing else 1
    
    batch_folder_name = f"{today}_{next_num}"
    ...
```

**Usage:**
- Creates batch folder at start of run
- Passes folder path to `llm-crisis-questions-test.py`
- All results saved to that batch folder

### `llm-crisis-questions-test.py`

**Updated Signature:**
```python
def main(model_name: str | None = None, results_dir: str | None = None):
    """
    Args:
        model_name: Name to use for the model in output files
        results_dir: Directory to save results in (defaults to RESULTS_DIR)
    """
    output_dir = results_dir if results_dir else RESULTS_DIR
    ...
```

**Change:**
- Accepts optional `results_dir` parameter
- Saves to specified directory instead of default

### `test-evaluation.py`

**New Support:**
```python
BATCH_FOLDER = os.getenv('BATCH_FOLDER')
if BATCH_FOLDER:
    INPUT_FILE_PATTERN = os.path.join(BATCH_FOLDER, '*.json')
    print(f"Using batch folder from environment: {BATCH_FOLDER}")
else:
    INPUT_FILE_PATTERN = os.path.join('test_results', '*.json')
```

**Changes:**
- Checks for `BATCH_FOLDER` environment variable
- Filters out `_runinfo.json` files automatically
- Can be controlled via `eval_batch.py` wrapper

### `eval_batch.py` (NEW)

**Purpose:** Helper script to easily evaluate batch folders

**Features:**
- List all available batches
- Auto-detect latest batch
- Evaluate specific batch
- Sets environment variable for `test-evaluation.py`

## Benefits

### ✅ Organization
- Each batch test run is isolated
- Easy to identify when tests were run
- Multiple runs per day supported

### ✅ Comparison
- Compare different batch runs easily
- Keep historical results
- Track model improvements over time

### ✅ Clean Structure
- No mixed results in one folder
- Easy to delete old batches
- Clear naming convention

### ✅ Automation Friendly
- Scripts auto-create folders
- Automatic incrementing
- No manual folder creation needed

## Examples

### Example 1: Testing 3 Models

```bash
# Select and test models
python batch_test_models.py
# Select: smollm2-360m, phi-3.5-mini, qwen2.5-1.5b

# Results saved to: test_results/2025-10-09_1/

# Evaluate the batch
python eval_batch.py
# Uses latest: 2025-10-09_1
```

### Example 2: Running Multiple Batches

```bash
# Morning batch - small models
python batch_test_models.py
# Select: smollm2-360m, gemma-2-2b
# → Saved to: test_results/2025-10-09_1/

# Afternoon batch - larger models  
python batch_test_models.py
# Select: phi-4-reasoning-plus, qwen3-4b
# → Saved to: test_results/2025-10-09_2/

# List all batches
python eval_batch.py --list
# Shows both: 2025-10-09_1 and 2025-10-09_2

# Evaluate specific batch
python eval_batch.py --batch 2025-10-09_1
```

### Example 3: Historical Comparison

```bash
# Evaluate yesterday's batch
python eval_batch.py --batch 2025-10-08_1

# Evaluate today's batch
python eval_batch.py --batch 2025-10-09_1

# Compare the generated reports
```

## Backward Compatibility

**Old flat structure still works!**

If you have old results in `test_results/*.json` (not in batch folders):
- `test-evaluation.py` still finds them when run directly
- `eval_batch.py` only looks at batch folders
- You can move old files into a batch folder manually:

```bash
# Create a batch folder for old results
mkdir test_results/2025-10-08_1

# Move old files
move test_results/*.json test_results/2025-10-08_1/
```

## Quick Reference

| Task | Command |
|------|---------|
| **Run batch tests** | `python batch_test_models.py` |
| **List batches** | `python eval_batch.py --list` |
| **Eval latest** | `python eval_batch.py` |
| **Eval specific** | `python eval_batch.py --batch 2025-10-09_1` |
| **Check test status** | `python check_test_status.py` |

## Troubleshooting

### "No batch folders found"
**Solution:** Run `python batch_test_models.py` first to create batch results.

### "Error: Batch folder '2025-10-09_1' not found!"
**Solution:** Check folder name with `python eval_batch.py --list`

### Want to evaluate old flat structure results?
**Solution:** Run `python test-evaluation.py` directly (without `eval_batch.py`)

## Summary

✅ **Organized** - Each batch run in its own folder  
✅ **Automatic** - Folders created automatically with incrementing numbers  
✅ **Easy Evaluation** - Simple commands to evaluate any batch  
✅ **Historical** - Keep and compare multiple test runs  
✅ **Backward Compatible** - Old results still work  

Your test results are now much better organized! 🎯

