# CrisisAI: GGUF Model Evaluation Framework# CrisisAI: GGUF Model Evaluation Framework



## Documentation## 1. Problem Statement



All documentation has been moved to the [`docs/`](./docs/) directory for better organization.In an emergency or crisis situation where communication infrastructure (internet, cellular networks) is unavailable, access to reliable information can be critical. The advent of small, efficient Large Language Models (LLMs) in formats like GGUF makes it possible to run a helpful AI assistant entirely offline on a device like a smartphone or laptop.



### Quick StartHowever, with a multitude of open-source models available, a key challenge arises: How do we select the most effective and reliable GGUF model for providing safe, practical, and clear advice to a non-expert user under stress?

- **[Quick Start Guide](./docs/QUICK_START.md)** - Get started in 5 minutes

- **[README](./docs/README.md)** - Complete project overview and setup instructionsAn ideal model must not only be accurate but also avoid dangerous "hallucinations," correct common misconceptions, and present information in a simple, step-by-step manner. This project provides a systematic framework to test, evaluate, and compare different GGUF models for this specific, high-stakes use case.



### Documentation## 2. The Solution: A Systematic Evaluation Pipeline

- **[Batch Organization](./docs/BATCH_ORGANIZATION.md)** - How batch testing and results organization works

- **[Automated Batch Testing](./docs/AUTOMATED_BATCH_TESTING.md)** - Complete automation guideThis project implements a multi-stage pipeline to rigorously evaluate and compare LLMs. It uses a powerful online model (Google's Gemini) as an objective "expert" to score the performance of smaller, offline models, moving from subjective impressions to data-driven analysis.

- **[Evaluation Viewer Guide](./docs/EVALUATION_VIEWER_GUIDE.md)** - Interactive HTML viewer documentation

- **[Architecture](./docs/ARCHITECTURE.md)** - System architecture and workflow diagramsThe workflow is managed by a series of scripts:



### Development- **Question Generation**: We start with a curated list of plausible, non-expert questions covering various off-grid crisis scenarios (crisis_questions.json).

- **[System Ready](./docs/SYSTEM_READY.md)** - Feature summary and status- **Automated Testing**: A Python script (run_crisis_test.py) connects to a local GGUF model (served via LM Studio) and records its answers to every question. This is repeated for each model being tested.

- **[Timing Improvements](./docs/TIMING_IMPROVEMENTS.md)** - Performance measurement details- **Expert Assessment**: A second script (evaluate_models.py) aggregates all the answers and sends them, one question at a time, to the Gemini API. Gemini is prompted to provide its own "ideal" answer and then score each of the smaller models' answers on a comparative scale of 0-10, providing a justification for each score.

- **[Fixes Applied](./docs/FIXES_APPLIED.md)** - Technical fixes and solutions- **Visual Reporting**: The final script (generate_report.py) processes the evaluation data and generates a single, self-contained, interactive HTML report (evaluation_report.html) for easy analysis and comparison.



## Code Files## 3. How to Use This Framework



- `batch_test_models.py` - Automated batch testing scriptFollow these steps to evaluate your own GGUF models.

- `llm-crisis-questions-test.py` - Core testing script

- `test-evaluation.py` - Gemini evaluation script### Prerequisites

- `eval_batch.py` - Batch evaluation helper

- `evaluation-viewer.html` - Interactive HTML viewer (requires local server)- **Python 3.7+**: Ensure Python and Pip are installed.

- `html-report-generator.py` - Static HTML report generator- **LM Studio**: Download and install from lmstudio.ai. This is used to easily serve GGUF models via a local server.

- **GGUF Models**: Download the GGUF model files you wish to test.

## Quick Start- **Gemini API Key**: Obtain an API key from Google AI Studio.



1. **Automated Testing**: `python batch_test_models.py`### Step 1: Initial Setup

2. **Evaluate Results**: `python eval_batch.py`

3. **View Results**: Run `python serve-viewer.py` and open the displayed URLClone or download this project's files into a single directory.



See [`docs/QUICK_START.md`](./docs/QUICK_START.md) for detailed instructions.Install the required Python library:

```bash
pip install requests
```

Customize the questions in crisis_questions.json if desired.

### Step 2: Test Your Local GGUF Models

#### 🚀 RECOMMENDED: Automated Batch Testing

Test multiple models automatically in one run:

```bash
python batch_test_models.py
```

This will:
1. List all available models in LM Studio
2. Let you select models using checkboxes (Space to select, Enter to confirm)
3. Create a timestamped batch folder (e.g., `test_results/2025-10-09_1/`)
4. Automatically load, test, and unload each model
5. Save all results to the batch folder

**See [AUTOMATED_BATCH_TESTING.md](AUTOMATED_BATCH_TESTING.md) for complete automation guide.**

#### Manual Testing (Alternative)

For testing individual models manually:

##### Load Model in LM Studio
Open LM Studio, load a GGUF model, and navigate to the Local Server tab (<-->).

##### Start Server
Click Start Server.

##### Run Test Script
Open a terminal in the project directory and run the script:

```bash
# Test/Dry-Run
python .\llm-crisis-questions-test.py

# Or specify model name (for result file naming)
python .\llm-crisis-questions-test.py --model-name "Mistral-7B-Instruct-v0.3.Q4_K_M"
```

### Step 3: Evaluate Results

#### Automated Batch Evaluation

After running batch tests, evaluate the results:

```bash
# List available batches
python eval_batch.py --list

# Evaluate latest batch (default)
python eval_batch.py

# Evaluate specific batch
python eval_batch.py --batch 2025-10-09_1
```

**See [BATCH_ORGANIZATION.md](BATCH_ORGANIZATION.md) for batch folder organization guide.**

#### Manual Evaluation (Alternative)

For manually collected results:

##### Set API Key
Set your Gemini API key as an environment variable.

- **macOS/Linux**: `export GEMINI_API_KEY="YOUR_API_KEY"`
- **Windows (CMD)**: `set GEMINI_API_KEY="YOUR_API_KEY"`
- **Windows (PowerShell)**: `$env:GEMINI_API_KEY="YOUR_API_KEY"`

##### Run Evaluation Script
With all your *_results.json files in the directory, run the evaluation script:

```bash
python test-evaluation.py
```

### Step 4: View the Visual Report

### Step 4: View Interactive Results

Start a local web server and open the viewer:

```bash
# Start Python's built-in web server
python -m http.server 8000

# Then open in your browser:
# http://localhost:8000/evaluation-viewer.html
```

This will:
- Serve the HTML viewer at `http://localhost:8000/evaluation-viewer.html`
- Automatically load all evaluation reports from `eval_results/`
- Display chronological tabs for each evaluation report
- Provide interactive analysis and comparison tools

**Features:**
- Automatic loading of all evaluation reports
- Chronological tab navigation (newest first)
- Performance summary with model rankings
- Detailed question-by-question analysis
- Interactive score breakdowns

#### Alternative: Generate Static HTML Report

If you prefer a pre-generated static report:

```bash
python html-report-generator.py
```

This creates `evaluation_report.html` with embedded data.

## 4. File Descriptions

### Core Scripts

- **`batch_test_models.py`**: 🚀 **[RECOMMENDED]** Automated batch testing script. Lists models, provides checkbox selection UI, automatically loads/unloads models via LM Studio CLI, creates timestamped batch folders, and runs tests sequentially.
  
- **`llm-crisis-questions-test.py`**: Core testing script that sends crisis questions to a loaded LLM and records answers. Can be run standalone or called by batch script.

- **`test-evaluation.py`**: Uses Gemini API to evaluate and score model answers. Supports both flat structure and batch folders via `BATCH_FOLDER` environment variable.

- **`eval_batch.py`**: Helper script for batch evaluation. Lists available batches, auto-detects latest, and wraps `test-evaluation.py` with proper environment setup.

- **`html-report-generator.py`**: Generates static HTML report with embedded evaluation data (legacy approach).

### Viewer

- **`evaluation-viewer.html`**: 🚀 **[RECOMMENDED]** Interactive standalone HTML viewer. Open in any browser, drag & drop JSON report files, view results instantly. Works completely offline - no Python or server needed!

### Data Files

- **`Crisis-Questions.json`**: Structured JSON file containing crisis scenario questions used for testing.

- **`test_results/YYYY-MM-DD_N/`**: Batch folders containing test results (format: `model-name_timestamp.json` and `*_runinfo.json`).

- **`gemini_evaluation_report.json`**: Generated master file with Gemini's expert answers and comparative scores.

- **`evaluation_report.html`**: Generated interactive report for analysis.

### Documentation

- **`AUTOMATED_BATCH_TESTING.md`**: Complete guide for automated batch testing with LM Studio CLI integration.

- **`BATCH_ORGANIZATION.md`**: Comprehensive guide for batch folder organization, evaluation workflows, and examples.

- **`TIMING_IMPROVEMENTS.md`**: Documentation of timing accuracy improvements (excludes file I/O overhead).

- **`FIXES_APPLIED.md`**: Record of Unicode encoding fixes for Windows subprocess handling.

### Utility Scripts

- **`list_gemini_models.py`**: Lists available Gemini models for evaluation.

- **`check_test_status.py`**: Monitors running batch tests and shows progress.
