import json
import requests
import os
import argparse
import sys
import re
from datetime import datetime

# --- Configuration ---
# The name of the JSON file containing the questions. You can override with env var
# CRISIS_QUESTIONS_FILE or INPUT_FILE. We'll also fall back to 'Crisis-Questions.json'.
INPUT_FILE = 'crisis_questions.json'
# The name of the file where the questions and answers will be saved.
OUTPUT_FILE = 'crisis_qa_results.json'
# Directory to store all test result files
RESULTS_DIR = 'test_results'
# The API endpoint for your LM Studio server. You can override with env var LM_STUDIO_API_URL.
LM_STUDIO_API_URL = os.environ.get("LM_STUDIO_API_URL", "http://localhost:1234/v1/chat/completions")

# The system prompt that guides the AI's persona and response style.
SYSTEM_PROMPT = """You are CrisisAI, an AI assistant designed to provide clear, simple, and safe advice for people in emergency situations without access to experts.
Assume the user is under stress, has no special training, and needs practical, step-by-step instructions.
Prioritize safety above all else. Do not give medical advice that should come from a doctor, but provide correct and established first aid information.
If a common 'myth' or dangerous misconception is part of the user's question, directly and gently correct it with the safe alternative."""

# --- Helper Function to Get Model Response ---
def get_llm_response(question):
    """
    Sends a question to the LM Studio API and returns the model's response.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "local-model",  # This is a placeholder, LM Studio uses the model loaded in the UI
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        "temperature": 0.7, # A balanced value for creativity vs. determinism.
        "max_tokens": 4096,
        "stream": False
    }

    try:
        response = requests.post(LM_STUDIO_API_URL, headers=headers, json=payload, timeout=300) # 5-minute timeout
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        response_json = response.json()

        # Handle OpenAI-compatible error envelope
        if isinstance(response_json, dict) and response_json.get("error"):
            err = response_json["error"]
            return f"ERROR: API error: {err.get('message', str(err))}"

        if response_json.get("choices") and len(response_json["choices"]) > 0:
            answer = response_json["choices"][0]["message"]["content"]
            return answer.strip()
        else:
            return "ERROR: Received an empty or invalid response from the model."

    except requests.exceptions.RequestException as e:
        print(f"\nAPI Call Error: {e}")
        return f"ERROR: Could not connect to the LM Studio API at {LM_STUDIO_API_URL}. Please ensure LM Studio is running and the server is started."
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        return "ERROR: An unexpected error occurred while processing the request."

# --- Utilities ---
def resolve_input_file():
    """Resolve the input file path, considering env vars and common filename variants."""
    # Env var override
    env_path = os.environ.get("CRISIS_QUESTIONS_FILE") or os.environ.get("INPUT_FILE")
    if env_path and os.path.exists(env_path):
        return env_path

    # Common filename variants to try
    candidates = [
        INPUT_FILE,
        'Crisis-Questions.json',
        'crisis-questions.json',
        'Crisis_questions.json',
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return None


def run_test_prompt(prompt: str) -> int:
    """Send a quick test prompt to the model and print the response."""
    print("--- CrisisAI Model Test ---")
    print(f"Connecting to model via: {LM_STUDIO_API_URL}")
    print(f"Sending test prompt: {prompt!r}\n")

    answer = get_llm_response(prompt)
    print("--- Model Response ---")
    print(answer)
    print("-----------------------")

    # Return non-zero exit code if clear error marker is present
    return 1 if isinstance(answer, str) and answer.startswith("ERROR:") else 0


# --- Main Script Logic ---
def main(model_name: str | None = None, results_dir: str | None = None):
    """
    Main function to load questions, query the LLM, and save the results.
    
    Args:
        model_name: Name to use for the model in output files
        results_dir: Directory to save results in (defaults to RESULTS_DIR)
    """
    # Use provided results_dir or default
    output_dir = results_dir if results_dir else RESULTS_DIR
    
    # Resolve the input file (supports env var override and common variants)
    input_file = resolve_input_file()
    if not input_file:
        print(
            "Error: Could not find a questions file. Looked for 'crisis_questions.json', 'Crisis-Questions.json', and env var CRISIS_QUESTIONS_FILE."
        )
        return

    # Load the questions from the JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        categories = json.load(f)

    if not isinstance(categories, dict):
        print("Error: The questions JSON must be an object mapping categories to subcategories.")
        return

    print("--- Starting Crisis Question & Answer Generation ---")
    print(f"Loaded questions from: {input_file}")
    print(f"Connecting to model via: {LM_STUDIO_API_URL}\n")

    # Initialize a dictionary to store the results
    qa_results = {}

    # We'll start timing when the FIRST question is actually sent
    run_start = None
    total_questions = 0

    # Iterate through each category, subcategory, and question
    for category, subcategories in categories.items():
        print(f"Processing Category: {category}")
        qa_results[category] = {}
        for subcategory, questions in subcategories.items():
            print(f"  -> Subcategory: {subcategory}")
            qa_results[category][subcategory] = []
            for i, question in enumerate(questions):
                print(f"    - Sending question {i+1}/{len(questions)}: '{question[:70]}...'")
                
                # Start timing on the FIRST question only
                if run_start is None:
                    run_start = datetime.now()
                
                # Get the answer from the language model
                answer = get_llm_response(question)
                
                # Store the question-answer pair
                qa_results[category][subcategory].append({
                    "question": question,
                    "answer": answer
                })
                total_questions += 1

    # Determine output filename (use end time). If model_name is provided, name it '<model>_<YYYY-MM-DD_HH-MM-SS>.json'
    end_time = datetime.now()
    end_time_str = end_time.strftime("%Y-%m-%d_%H-%M-%S")

    # Compute duration and pretty format MM:SS
    # If run_start is None, it means no questions were processed
    if run_start is not None:
        duration_s = int((end_time - run_start).total_seconds())
        mm = duration_s // 60
        ss = duration_s % 60
        duration_mmss = f"{mm:02d}:{ss:02d}"
    else:
        duration_s = 0
        duration_mmss = "00:00"

    def _sanitize(name: str) -> str:
        # Replace any disallowed filename chars with '-'
        cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-._ ")
        return cleaned or "model"

    if model_name:
        safe_model = _sanitize(model_name)
        output_file = f"{safe_model}_{end_time_str}.json"
    else:
        output_file = OUTPUT_FILE

    # Ensure results directory exists and save to it
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)

    # Save the consolidated results to the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(qa_results, f, indent=2, ensure_ascii=False)

    # Also save run info as a sidecar JSON (does not change main results schema)
    runinfo = {
        "model_name": model_name or "local-model",
        "lm_studio_api_url": LM_STUDIO_API_URL,
        "questions_count": total_questions,
        "started_at": run_start.isoformat(timespec='seconds') if run_start else None,
        "finished_at": end_time.isoformat(timespec='seconds'),
        "duration_seconds": duration_s,
        "duration_mmss": duration_mmss,
        "results_file": output_path,
    }
    runinfo_path = os.path.splitext(output_path)[0] + "_runinfo.json"
    with open(runinfo_path, 'w', encoding='utf-8') as f:
        json.dump(runinfo, f, indent=2, ensure_ascii=False)

    print("\n--- Processing Complete ---")
    print(f"Successfully saved all questions and answers to: {output_path}")
    print(f"Run time: {duration_mmss} ({duration_s} seconds) | Details: {runinfo_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CrisisAI Q&A generator for LM Studio-served GGUF models")
    parser.add_argument("--test", action="store_true", help="Send a small test prompt to the model and exit.")
    parser.add_argument("--dry-run", action="store_true", help="Alias for --test; do not process the questions JSON.")
    parser.add_argument("--prompt", "-p", type=str, default="Hi", help="Prompt to use with --test/--dry-run (default: 'Hi').")
    parser.add_argument("--model-name", "--model", dest="model_name", type=str, help="Model name to include in the output filename, e.g., 'smollm2-1.7b-instruct'. Output file becomes '<model>_<YYYY-MM-DD_HH-MM-SS>.json'.")

    args = parser.parse_args()

    if args.test or args.dry_run:
        sys.exit(run_test_prompt(args.prompt))
    else:
        main(args.model_name)
