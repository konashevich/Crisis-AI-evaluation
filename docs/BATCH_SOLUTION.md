# Batch Testing - Complete Solution

## ✨ What's Been Created

You now have a complete batch testing system with 3 new scripts:

### 1. `batch_test_simple.py` - **Main Testing Script** ⭐
**Use this to test multiple models sequentially**

```bash
python batch_test_simple.py
```

- Prompts you to load each model in LM Studio
- Runs all crisis questions
- Saves results automatically
- Works with ANY LM Studio version

### 2. `check_test_status.py` - **Progress Tracker**
**See which models are done and which still need testing**

```bash
python check_test_status.py
```

Shows:
- ✓ Tested models with dates
- ⚠ Models still needing tests
- Extra test results not in your plan

### 3. `models_to_test.txt` - **Your Test Plan**
**Edit this file to control which models to test**

```
# Comments start with #
smollm2-360m-instruct-q8_0
Phi-4-mini-reasoning-Q4_K_M
Mistral-7B-Instruct-v0.3.Q4_K_M
```

---

## 🚀 Quick Workflow

### First Time Setup

1. **Edit your model list:**
   ```bash
   notepad models_to_test.txt
   ```
   Add model names, one per line

2. **Check status:**
   ```bash
   python check_test_status.py
   ```
   See what needs testing

3. **Start batch testing:**
   ```bash
   python batch_test_simple.py
   ```

### For Each Model

The script will show:
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

**You do:**
1. Click the model in LM Studio
2. Wait for "Model loaded"
3. Press Enter in terminal
4. Script runs all questions automatically
5. Repeat for next model

### Check Progress Anytime

```bash
python check_test_status.py
```

---

## 📊 Example Session

```bash
# Check what needs testing
PS> python check_test_status.py
📊 Test Status Report
Models in test list: 11
Models with results: 3

3 model(s) still need testing:
  • Phi-4-mini-reasoning-Q4_K_M
  • Qwen3-4B-Instruct-2507-Q4_K_M  
  • Mistral-7B-Instruct-v0.3.Q4_K_M

# Start batch testing
PS> python batch_test_simple.py

🤖 Crisis-AI Batch Model Tester
✓ Connected to LM Studio

Found saved list with 3 models
Use this list? Yes

[1/3] Model: Phi-4-mini-reasoning-Q4_K_M
Please load model in LM Studio...
(you load model, press Enter)
✓ Running crisis questions test...
✓ Completed in 245 seconds

[2/3] Model: Qwen3-4B-Instruct-2507-Q4_K_M
Please load model in LM Studio...
(you load model, press Enter)
✓ Running crisis questions test...
✓ Completed in 280 seconds

[3/3] Model: Mistral-7B-Instruct-v0.3.Q4_K_M
Please load model in LM Studio...
(you load model, press Enter)
✓ Running crisis questions test...
✓ Completed in 210 seconds

📊 Batch Test Summary
Total time: 735 seconds (12.3 minutes)

Results:
✓ Phi-4-mini-reasoning-Q4_K_M (245s)
✓ Qwen3-4B-Instruct-2507-Q4_K_M (280s)
✓ Mistral-7B-Instruct-v0.3.Q4_K_M (210s)

Completed: 3/3
✨ All done!
```

---

## 💡 Pro Tips

### Overnight Testing
Perfect for testing many models while you sleep:

1. Add all models to `models_to_test.txt`
2. Start `batch_test_simple.py`
3. Script pauses at each model
4. You can wake up, load next model, go back to sleep
5. OR set an alarm every ~30 mins to load next model

### Partial Runs
You can Ctrl+C and resume:

- Script asks "Skip this model and continue?"
- Answer 'y' to skip to next model
- Answer 'n' to stop completely
- Re-run script later to continue

### Model Name Format
The model name in `models_to_test.txt` is just for output filenames.
It doesn't need to match LM Studio's exact model name.

Use consistent names like:
```
Phi-4-mini-reasoning-Q4_K_M
```

Not:
```
phi_4_mini_reasoning.gguf
```

### Organizing Results
Results go to `test_results/`:
```
Phi-4-mini-reasoning-Q4_K_M_2025-10-09_15-30-00.json
Phi-4-mini-reasoning-Q4_K_M_2025-10-09_15-30-00_runinfo.json
```

Each model gets timestamped files, so you can test the same model multiple times.

---

## 🔧 Troubleshooting

### "Cannot connect to LM Studio"
- Make sure LM Studio is running
- Go to Developer tab → Start Server
- Server should show "Running on http://localhost:1234"

### Model name doesn't match
That's OK! The name in `models_to_test.txt` is just for output files.
Load whatever model you want in LM Studio.

### Want better UI?
Install questionary (already in requirements.txt):
```bash
pip install questionary
```
Gets you nice checkbox selection instead of typing numbers.

### Resume after crash?
Just run `batch_test_simple.py` again.
When it asks to load a model you already tested, just skip it (Ctrl+C → skip).

---

## 🎯 Next Steps After Testing

Once you have test results for all models:

1. **Evaluate responses:**
   ```bash
   python test-evaluation.py
   ```

2. **Generate HTML reports:**
   ```bash
   python html-report-generator.py
   ```

3. **Compare models:**
   Check the generated reports to see which model performed best!

---

## Files Created

- ✅ `batch_test_simple.py` - Main batch testing script
- ✅ `check_test_status.py` - Progress checker
- ✅ `models_to_test.txt` - Your model list (edit this!)
- ✅ `QUICK_START_BATCH.md` - Quick reference guide
- ✅ `BATCH_TESTING.md` - Full documentation
- ✅ `requirements.txt` - Updated with questionary

---

## Summary

You can now:
- ✅ Test multiple models in one session
- ✅ Track progress easily
- ✅ Resume after interruptions
- ✅ Run overnight/unattended
- ✅ Avoid manual file management

**Start now:**
```bash
python batch_test_simple.py
```

Happy testing! 🚀
