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

For each GGUF model you want to test, repeat the following process:

#### Load Model in LM Studio
Open LM Studio, load a GGUF model, and navigate to the Local Server tab (<-->).

#### Start Server
Click Start Server.

#### Run Test Script
Open a terminal in the project directory and run the script:

```bash
Test/Dry-Run
python .\llm-crisis-questions-test.py
python .\llm-crisis-questions-test.py
or (model name is only for the name of the result file)
python .\llm-crisis-questions-test.py --model-name "Mistral-7B-Instruct-v0.3.Q4_K_M"
```

#### Rename the Output
The script will create crisis_qa_results.json. Immediately rename this file to reflect the model you just tested. For example:
- llama3_results.json
- mistral-7b_results.json
- phi-2_results.json

### Step 3: Run the Gemini Evaluation

#### Set API Key
Set your Gemini API key as an environment variable.

- **macOS/Linux**: `export GEMINI_API_KEY="YOUR_API_KEY"`
- **Windows (CMD)**: `set GEMINI_API_KEY="YOUR_API_KEY"`
- **Windows (PowerShell)**: `$env:GEMINI_API_KEY="YOUR_API_KEY"`

#### Run Evaluation Script
With all your renamed *_results.json files in the directory, run the evaluation script:

```bash
python evaluate_models.py
```

This script will find all model result files, query the Gemini API for each question, and create gemini_evaluation_report.json.

### Step 4: Generate the Visual Report

#### Run Report Script
Once the evaluation is complete, run the final script:

```bash
python generate_report.py
```

#### View Report
The script will generate evaluation_report.html. Open this file in any web browser to see the full, interactive comparison of your models. Click on any score to see a detailed breakdown and justification.

## 4. File Descriptions

- `off_grid_crisis_scenarios.md`: An editable Markdown file for brainstorming potential crisis scenarios.
- `crisis_questions.json`: A structured JSON file containing the non-expert questions used for testing.
- `run_crisis_test.py`: Python script to send questions to a local model via the LM Studio API and save the answers.
- `evaluate_models.py`: Python script that uses the Gemini API to score the answers from all tested models.
- `generate_report.py`: Python script that creates a final, interactive HTML report from the evaluation data.
- `*_results.json` (User-generated): Output files from run_crisis_test.py, each containing the Q&A pairs for one model.
- `gemini_evaluation_report.json` (Generated): The master JSON file containing Gemini's expert answers and comparative scores.
- `evaluation_report.html` (Generated): The final, self-contained, interactive report for analysis.
