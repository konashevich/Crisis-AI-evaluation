# 🎉 NEW: Interactive Evaluation Viewer

## What's New?

A **completely standalone HTML viewer** that lets you explore evaluation results without any Python scripts or server setup!

## Quick Demo

### Before (Old Way)
```bash
# Generate evaluation
python test-evaluation.py

# Generate static HTML
python html-report-generator.py

# View (embedded data, can't change files)
start evaluation_report.html
```

### After (New Way) ✨
```bash
# Generate evaluation  
python test-evaluation.py

# Just open viewer
start evaluation-viewer.html

# Drag & drop ANY JSON file
# Instantly see results!
```

## Key Features

### 🎯 Zero Dependencies
- No Python required
- No server needed
- No build process
- Just open in browser!

### 📁 Drag & Drop Interface
- Drop JSON file onto page
- Or click to browse
- Instant processing
- Visual feedback

### 🔍 Interactive Exploration
- Click any score to see details
- Compare ideal vs actual answers
- Read score justifications
- Beautiful responsive UI

### 🔒 Privacy First
- Files never leave your computer
- No uploads, no tracking
- Works completely offline
- Data only in memory

### 📱 Responsive Design
- Works on desktop, tablet, mobile
- Clean modern interface
- Smooth animations
- Color-coded scores

## How It Works

### 1. Open in Browser
```bash
start evaluation-viewer.html
```

### 2. Load Data
- **Drag & drop** JSON file onto drop zone
- **Or click** to browse and select

### 3. Explore Results
- **Performance summary** - Model rankings
- **Detailed tables** - Question-by-question
- **Interactive scores** - Click to expand

## File Structure

```
Crisis-AI-evaluation/
├── evaluation-viewer.html          ← 🆕 New standalone viewer
├── html-report-generator.py        ← Legacy static generator
├── test-evaluation.py              ← Generates JSON reports
├── eval_batch.py                   ← Batch evaluation helper
│
├── gemini_evaluation_report_*.json ← Drag these into viewer!
├── gemini_evaluation_report.json
│
└── test_results/
    └── 2025-10-09_1/
        └── *.json                  ← Or drag batch results
```

## Comparison

| Feature | evaluation-viewer.html | html-report-generator.py |
|---------|----------------------|--------------------------|
| **Python needed** | ❌ No | ✅ Yes |
| **Setup time** | 0 seconds | Install dependencies |
| **File switching** | Drag & drop anytime | Re-run script |
| **Portability** | Single HTML file | Script + templates |
| **Best for** | Interactive exploration | Embedded reports |

## Use Cases

### Use Case 1: Quick Results Check
```
After running eval_batch.py:

Old way:
1. python html-report-generator.py
2. start evaluation_report.html
3. Can't easily compare other batches

New way:
1. start evaluation-viewer.html
2. Drag latest JSON
3. Drag another JSON to compare
   (in new tab)
```

### Use Case 2: Sharing Results
```
Old way:
1. Generate static HTML (includes data)
2. Send large HTML file
3. Recipient sees fixed snapshot

New way:
1. Send evaluation-viewer.html (once)
2. Send any JSON files you want
3. Recipient loads any file they want
```

### Use Case 3: Historical Analysis
```
Old way:
1. Keep many static HTML files
2. Hard to find specific test
3. No easy comparison

New way:
1. Keep JSON files organized
2. One viewer for all
3. Load different files side-by-side
```

## Technical Details

### Technologies Used
- **Pure JavaScript** - No frameworks
- **Tailwind CSS** - Via CDN for styling
- **FileReader API** - Read local files
- **DOM Manipulation** - Dynamic content

### Browser Support
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+

### Code Highlights

#### Drag & Drop
```javascript
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
});
```

#### JSON Processing
```javascript
const reader = new FileReader();
reader.onload = (e) => {
    const data = JSON.parse(e.target.result);
    processReportData(data);
};
reader.readAsText(file);
```

#### Dynamic UI
```javascript
generateSummaryCards(data);
generateDetailedReport(data);
toggleDetails(detailsId);
```

## Workflow Integration

### Recommended Workflow

```bash
# 1. Batch test models
python batch_test_models.py

# 2. Evaluate results
python eval_batch.py

# 3. View with interactive viewer ⭐
start evaluation-viewer.html
# Drag: gemini_evaluation_report_2025-10-09_15-30-00.json

# 4. (Optional) Generate static HTML for archiving
python html-report-generator.py
```

### Alternative Workflows

#### Quick Single Model Test
```bash
python llm-crisis-questions-test.py --model-name "test-model"
python test-evaluation.py
start evaluation-viewer.html  # Drag the JSON
```

#### Batch Comparison
```bash
# Test batch 1
python batch_test_models.py  # Select set A
python eval_batch.py

# Test batch 2  
python batch_test_models.py  # Select set B
python eval_batch.py

# Compare
start evaluation-viewer.html  # Tab 1: batch 1 JSON
start evaluation-viewer.html  # Tab 2: batch 2 JSON
```

## Documentation

### Complete Guide
See **`EVALUATION_VIEWER_GUIDE.md`** for:
- Detailed feature explanations
- Troubleshooting guide
- Customization options
- Advanced use cases

### Quick Reference
See **`QUICK_START.md`** for:
- Getting started
- Basic workflows
- Common tasks

## Benefits

### ✅ User Experience
- **Instant gratification** - No waiting for generation
- **Flexible** - Load any file anytime
- **Interactive** - Click to explore
- **Fast** - No Python overhead

### ✅ Developer Experience
- **No maintenance** - Single HTML file
- **No dependencies** - Works anywhere
- **Easy sharing** - Send one file
- **Version control friendly** - Track JSON + HTML separately

### ✅ System Integration
- **Complements existing tools** - Doesn't replace
- **Works with batch system** - Load batch results
- **Legacy compatible** - Still works with old JSONs
- **Future proof** - Pure web standards

## Migration Guide

### From Static HTML Generator

**You don't need to migrate!** Both tools coexist:

- **Use `evaluation-viewer.html`** for:
  - Interactive exploration
  - Quick checks
  - Comparing multiple files
  - Mobile viewing

- **Use `html-report-generator.py`** for:
  - Archival (self-contained)
  - Email attachments
  - Offline sharing (single file with data)
  - Automated workflows

### Workflow Changes

**Before:**
```bash
test → evaluate → generate HTML → view
```

**After (Recommended):**
```bash
test → evaluate → view (drag JSON)
                ↓
        (optional) generate static HTML for archive
```

## Summary

### 🎊 What You Get

✅ **Interactive viewer** - Drag & drop JSON files  
✅ **Zero dependencies** - Just open in browser  
✅ **Completely offline** - No server needed  
✅ **Privacy focused** - Data stays local  
✅ **Beautiful UI** - Responsive design  
✅ **Easy sharing** - Single HTML file  
✅ **Full documentation** - Complete guide included  

### 🚀 Getting Started

```bash
# Just open it!
start evaluation-viewer.html

# Then drag any evaluation JSON file
```

That's it! No installation, no configuration, no complications. 🎉

---

**See `EVALUATION_VIEWER_GUIDE.md` for complete documentation.**

**Ready to explore your results?** Open `evaluation-viewer.html` now! 🚀
