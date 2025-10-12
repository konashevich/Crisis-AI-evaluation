# FREE Solution: Add Model Sizes to HTML Viewer

## The Problem

You want to see model sizes in the HTML evaluation viewer, but:
- Re-running the Gemini API evaluation costs $50 💸
- The existing evaluation reports don't have model size data
- The runinfo files HAVE the size data already

## The Solution (3 Options - All FREE!)

### Option 1: Enrich Existing Report (RECOMMENDED) ✅

Use the new script to add size data to an existing evaluation report:

```bash
# Future evaluations will automatically include batch_folder field
python eval_batch.py --batch 2025-10-11_1

# Then view in browser:
python serve_viewer.py
```

**Cost: $50** (because it calls Gemini API)

### Option 2: Add Sizes Without Re-Evaluation (FREE!) 🆓

If you already have an evaluation report but it's missing size data:

```bash
# This reads runinfo files and adds sizes to the report
python enrich_report_with_sizes.py eval_results/gemini_evaluation_report_2025-10-12_08-07-40.json
```

**Requirements:**
- Report must have `batch_folder` field (added in latest test-evaluation.py)
- The batch folder must still exist with runinfo files

**Cost: $0.00** ✅

### Option 3: Update test-evaluation.py (Already Done!)

The `test-evaluation.py` script has been updated to:
1. Include `batch_folder` in the evaluation report JSON
2. This allows the viewer to find runinfo files

**Next time you run evaluation:**
```bash
python eval_batch.py --batch 2025-10-11_1
```

The report will include:
```json
{
  "batch_folder": "test_results/2025-10-11_1",
  "model_metadata": { ... },
  "evaluations": { ... }
}
```

**Cost: $50** (Gemini API call)

## What Changed

### 1. test-evaluation.py
- Now saves `batch_folder` field in evaluation reports
- This field points to the test_results folder with runinfo files

### 2. enrich_report_with_sizes.py (NEW)
- Reads existing evaluation report
- Loads size data from runinfo files in batch_folder
- Updates model_metadata with sizes
- **Saves updated report - $0 cost!**

### 3. evaluation-viewer.html (UPDATED)
- Can now fetch runinfo files directly when batch_folder is present
- Falls back to model_metadata if runinfo not available
- Shows "Size: N/A" for models without size data

## For Your Current Situation

You have:
- ✅ `test_results/2025-10-11_1/` with 40 runinfo files (all with size data)
- ❓ Evaluation report (might not have batch_folder field yet)

**Best approach:**

**If you have a recent evaluation report WITH batch_folder:**
```bash
python enrich_report_with_sizes.py eval_results/gemini_evaluation_report_YYYY-MM-DD_HH-MM-SS.json
python serve_viewer.py
```

**If your evaluation report doesn't have batch_folder:**
You have 2 choices:
1. **Free but no evaluation**: Just view individual runinfo files
2. **$50 but complete**: Re-run evaluation with updated script:
   ```bash
   python eval_batch.py --batch 2025-10-11_1
   ```

## Summary

| Method | Cost | Time | Result |
|--------|------|------|--------|
| Enrich existing report | **$0** | 5 seconds | Adds sizes to existing report |
| Re-run evaluation | $50 | ~30 min | New report with all data |
| Future evaluations | $50 | ~30 min | Automatic size inclusion |

**Recommendation:** If you have a report with `batch_folder`, use `enrich_report_with_sizes.py` - it's FREE and instant! ✅
