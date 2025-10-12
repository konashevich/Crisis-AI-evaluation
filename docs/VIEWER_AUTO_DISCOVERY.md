# HTML Evaluation Viewer - Auto-Discovery System

## How It Works Now ✅

The evaluation viewer now **automatically discovers and loads all evaluation reports** using an index file system.

### Architecture

```
eval_results/
├── reports_index.json                              ← Index of all reports (auto-generated)
├── gemini_evaluation_report_2025-10-12_08-07-40.json
├── gemini_evaluation_report_2025-10-10_20-37-59.json
└── gemini_evaluation_report_2025-10-10_12-31-53.json
```

### Flow

1. **HTML loads** → Fetches `eval_results/reports_index.json`
2. **Index contains** → List of all available report files
3. **HTML loads each report** → Creates tabs with date/time from filename
4. **User switches tabs** → Views different evaluation runs

### Why We Need the Index File

**Browser Security Restriction:** JavaScript in a webpage cannot list directory contents for security reasons. The only way to discover files is through an index file that lists them.

### Auto-Update

The index is **automatically regenerated** whenever you:
- Run `python test-evaluation.py` (evaluation script auto-updates index at end)
- Run `python generate_reports_index.py` (manual update)

### Files Modified

✅ **evaluation-viewer.html**
- Changed from hardcoded single file to index-based discovery
- Loads all reports listed in `reports_index.json`
- Creates tabs sorted by date/time (newest first)

✅ **test-evaluation.py**
- Added imports: `sys`, `subprocess`
- Calls `generate_reports_index.py` after saving report
- Auto-updates index so HTML viewer sees new reports immediately

✅ **generate_reports_index.py** (NEW)
- Scans `eval_results/` for all `gemini_evaluation_report_*.json` files
- Creates `reports_index.json` with list of all reports
- Sorts by filename (newest first due to timestamp format)

### Usage

#### Viewing Reports
1. Open `evaluation-viewer.html` in a browser
2. It automatically loads all available reports
3. Switch between reports using the date/time tabs

#### After Running New Evaluation
```powershell
python eval_batch.py  # or python test-evaluation.py
```
The index is automatically updated - just refresh the HTML page!

#### Manual Index Update (if needed)
```powershell
python generate_reports_index.py
```

### Current Reports Available

According to the index:
- 📊 3 evaluation reports
- 📅 Latest: 2025-10-12 08:07:40
- 📅 Previous: 2025-10-10 20:37:59
- 📅 Previous: 2025-10-10 12:31:53

### Error Handling

If you see "Error loading reports" in the HTML:
1. Make sure `eval_results/reports_index.json` exists
2. Run `python generate_reports_index.py` to create it
3. Refresh the HTML page

### Technical Details

**Filename Parsing:**
```javascript
// Pattern: gemini_evaluation_report_YYYY-MM-DD_HH-MM-SS.json
parseReportDateTime('gemini_evaluation_report_2025-10-12_08-07-40.json')
// Returns: { date: '2025-10-12', time: '08:07:40', timestamp: ... }
```

**Tab Display:**
- Date on first line
- Time on second line
- Sorted newest first
- Active tab highlighted in blue

**Data Structure:**
```json
{
  "reports": [
    "gemini_evaluation_report_2025-10-12_08-07-40.json",
    "gemini_evaluation_report_2025-10-10_20-37-59.json"
  ],
  "count": 2,
  "generated_at": 1760254531.786493
}
```
