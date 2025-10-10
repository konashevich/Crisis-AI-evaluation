# Evaluation Script Auto-Detection Update

## Overview
The `test-evaluation.py` script now automatically detects and uses the latest batch folder in `test_results/` for evaluation, matching the new batch organization structure created by `batch_test_models.py`.

## Changes Made

### 1. New Function: `get_latest_batch_folder()`
- Automatically finds the most recent subfolder in `test_results/`
- Uses modification time to determine the latest folder
- Returns the full path to the latest batch folder

### 2. Updated `aggregate_answers_by_question(batch_folder)`
- Now accepts a `batch_folder` parameter
- Looks for JSON files in the specified folder instead of a hardcoded pattern
- Provides clearer error messages showing which folder was searched

### 3. Enhanced `main()` Function
The script now uses the following priority order to determine which folder to evaluate:

1. **Command-line argument** (`--batch-folder`): Explicit user specification
2. **Environment variable** (`BATCH_FOLDER`): For programmatic control
3. **Auto-detection**: Finds the latest subfolder in `test_results/`
4. **Fallback**: Uses `test_results/` directory directly (for backward compatibility)

### 4. New Command-Line Argument
```bash
--batch-folder <path>
```
Allows you to explicitly specify which batch folder to evaluate.

## Usage Examples

### Default Behavior (Auto-detect Latest)
```bash
python test-evaluation.py
```
Output:
```
Using latest batch folder: test_results/2025-10-10_2
Found 2 model result files in test_results/2025-10-10_2
```

### Specify a Specific Batch
```bash
python test-evaluation.py --batch-folder test_results/2025-10-09-1
```

### Using Environment Variable
```powershell
$env:BATCH_FOLDER="test_results/2025-10-10_2"
python test-evaluation.py
```

### With Other Options
```bash
python test-evaluation.py --batch-folder test_results/2025-10-10_2 --limit 5 --mock-eval
```

## Benefits

1. **Automatic**: No need to manually specify folders for the latest batch
2. **Flexible**: Can still override with specific folder when needed
3. **Compatible**: Works with the new batch folder structure from `batch_test_models.py`
4. **Backward Compatible**: Falls back to old behavior if no subfolders exist
5. **Clear Feedback**: Shows which folder is being used

## Folder Detection Logic

The script looks for subfolders in `test_results/` and selects the one with the most recent modification time. This works with any folder naming convention, including:

- `2025-10-10_1`
- `2025-10-10_2`
- `2025-10-09-1`
- Custom named folders

## Integration with Batch Testing

After running batch tests with `batch_test_models.py`, you can immediately run evaluation without specifying a folder:

```bash
# Run batch tests (creates test_results/2025-10-10_2/)
python batch_test_models.py

# Evaluate latest batch automatically
python test-evaluation.py
```

The evaluation script will automatically find and use the batch folder that was just created.
