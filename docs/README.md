# CrisisAI: GGUF Model Evaluation Framework

## 1. Problem Statement

In an emergency or crisis situation where communication infrastructure (internet, cellular networks) is unavailable, access to reliable information can be critical. The advent of small, efficient Large Language Models (LLMs) in formats like GGUF makes it possible to run a helpful AI assistant entirely offline on a device like a smartphone or laptop.

However, with a multitude of open-source models available, a key challenge arises: How do we select the most effective and reliable GGUF model for providing safe, practical, and clear advice to a non-expert user under stress?

An ideal model must not only be accurate but also avoid dangerous "hallucinations," correct common misconceptions, and present information in a simple, step-by-step manner. This project provides a systematic framework to test, evaluate, and compare different GGUF models for this specific, high-stakes use case.

## 2. The Solution: A Systematic Evaluation Pipeline

This project implements a multi-stage pipeline to rigorously evaluate and compare LLMs. It uses a powerful online model (Google's Gemini) as an objective "expert" to score the performance of smaller, offline models, moving from subjective impressions to data-driven analysis.

The workflow is managed by a series of scripts:

- **Question Generation**: We start with a curated list of plausible, non-expert questions covering various off-grid crisis scenarios (crisis_questions.json).
- **Automated Testing**: A Python script (run_crisis_test.py) connects to a local GGUF model (served via LM Studio) and records its answers to every question. This is repeated for each model being tested.
- **Expert Assessment**: A second script (evaluate_models.py) aggregates all the answers and sends them, one question at a time, to the Gemini API. Gemini is prompted to provide its own "ideal" answer and then score each of the smaller models' answers on a comparative scale of 0-10, providing a justification for each score.
- **Visual Reporting**: The final script (generate_report.py) processes the evaluation data and generates a single, self-contained, interactive HTML report (evaluation_report.html) for easy analysis and comparison.

## 3. How to Use This Framework

Follow these steps to evaluate your own GGUF models.

### Prerequisites

- **Python 3.7+**: Ensure Python and Pip are installed.
- **LM Studio**: Download and install from lmstudio.ai. This is used to easily serve GGUF models via a local server.
- **GGUF Models**: Download the GGUF model files you wish to test.
- **Gemini API Key**: Obtain an API key from Google AI Studio.

### Step 1: Initial Setup

Clone or download this project's files into a single directory.

Install the required Python library:

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

#### 🚀 RECOMMENDED: Interactive HTML Viewer

Simply open the standalone viewer in your browser:

```bash
# Open the viewer
start evaluation-viewer.html
```

Then:
1. **Drag & drop** your JSON evaluation file, or
2. **Click to browse** and select the file

The viewer will instantly display:
- Performance summary with model rankings
- Detailed question-by-question analysis
- Interactive score breakdowns

**Works completely offline - no server needed!**

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
