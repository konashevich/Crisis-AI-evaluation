import json
import requests
import os

# --- Configuration ---
# The name of the JSON file containing the questions.
INPUT_FILE = 'crisis_questions.json'
# The name of the file where the questions and answers will be saved.
OUTPUT_FILE = 'crisis_qa_results.json'
# The API endpoint for your LM Studio server.
LM_STUDIO_API_URL = "http://localhost:1234/v1/chat/completions"

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
        "stream": False
    }

    try:
        response = requests.post(LM_STUDIO_API_URL, headers=headers, json=payload, timeout=300) # 5-minute timeout
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        response_json = response.json()
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

# --- Main Script Logic ---
def main():
    """
    Main function to load questions, query the LLM, and save the results.
    """
    # Check if the input file exists
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file '{INPUT_FILE}' not found. Please make sure it's in the same directory as this script.")
        return

    # Load the questions from the JSON file
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        categories = json.load(f)

    print("--- Starting Crisis Question & Answer Generation ---")
    print(f"Loaded questions from: {INPUT_FILE}")
    print(f"Connecting to model via: {LM_STUDIO_API_URL}\n")

    # Initialize a dictionary to store the results
    qa_results = {}

    # Iterate through each category, subcategory, and question
    for category, subcategories in categories.items():
        print(f"Processing Category: {category}")
        qa_results[category] = {}
        for subcategory, questions in subcategories.items():
            print(f"  -> Subcategory: {subcategory}")
            qa_results[category][subcategory] = []
            for i, question in enumerate(questions):
                print(f"    - Sending question {i+1}/{len(questions)}: '{question[:70]}...'")
                
                # Get the answer from the language model
                answer = get_llm_response(question)
                
                # Store the question-answer pair
                qa_results[category][subcategory].append({
                    "question": question,
                    "answer": answer
                })

    # Save the consolidated results to the output file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(qa_results, f, indent=2, ensure_ascii=False)

    print("\n--- Processing Complete ---")
    print(f"Successfully saved all questions and answers to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
