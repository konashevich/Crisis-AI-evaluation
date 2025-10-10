"""
Simple Batch Model Tester for Crisis-AI Evaluation
Tests models one at a time - prompts you to load each model manually in LM Studio.
"""
import json
import os
import sys
import requests
from datetime import datetime

# Try to import questionary for better UI
try:
    import questionary
    HAS_QUESTIONARY = True
except ImportError:
    HAS_QUESTIONARY = False

# Import the main testing function
import importlib.util
spec = importlib.util.spec_from_file_location("test_script", "llm-crisis-questions-test.py")
if spec and spec.loader:
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)
else:
    print("Error: Could not load llm-crisis-questions-test.py")
    sys.exit(1)

# Configuration
LM_STUDIO_BASE_URL = os.environ.get("LM_STUDIO_API_URL", "http://localhost:1234").rstrip('/v1/chat/completions').rstrip('/v1')
MODELS_LIST_FILE = "models_to_test.txt"

# Color codes
class Colors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'

def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{text}{Colors.ENDC}")

def print_success(text: str):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text: str):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text: str):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def get_currently_loaded_model() -> str:
    """Check which model is currently loaded in LM Studio"""
    try:
        # Try to get a response to see what model is loaded
        response = requests.get(f"{LM_STUDIO_BASE_URL}/v1/models", timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # LM Studio doesn't clearly indicate which model is loaded,
        # so we'll try a test request
        test_response = requests.post(
            f"{LM_STUDIO_BASE_URL}/v1/chat/completions",
            json={
                "model": "local-model",
                "messages": [{"role": "user", "content": "hi"}],
                "max_tokens": 5
            },
            timeout=10
        )
        
        if test_response.status_code == 200:
            result = test_response.json()
            model_name = result.get("model", "unknown")
            return model_name if model_name != "local-model" else "a model (unknown name)"
        return "unknown"
        
    except:
        return "none"

def wait_for_model_load(expected_name: str = None):
    """Wait for user to load a model in LM Studio"""
    print(f"\n{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    if expected_name:
        print(f"{Colors.BOLD}Please load model in LM Studio: {Colors.WARNING}{expected_name}{Colors.ENDC}")
    else:
        print(f"{Colors.BOLD}Please load the next model in LM Studio{Colors.ENDC}")
    
    print(f"{Colors.BOLD}Steps:{Colors.ENDC}")
    print("  1. Open LM Studio")
    print("  2. Click on the model you want to test")
    print("  3. Wait for it to load completely")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")
    
    if HAS_QUESTIONARY:
        questionary.confirm("Is the model loaded and ready?", default=False).ask()
    else:
        input("Press Enter when the model is loaded and ready...")
    
    # Verify a model is loaded
    current = get_currently_loaded_model()
    if current == "none":
        print_warning("Could not detect a loaded model. Make sure LM Studio has a model loaded.")
        retry = input("Try again? (y/N): ").strip().lower()
        if retry == 'y':
            return wait_for_model_load(expected_name)
    else:
        print_success(f"Detected model: {current}")

def load_models_list() -> list:
    """Load list of model names from text file"""
    if os.path.exists(MODELS_LIST_FILE):
        with open(MODELS_LIST_FILE, 'r', encoding='utf-8') as f:
            models = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
            return models
    return []

def save_models_list(models: list):
    """Save list of model names to text file"""
    with open(MODELS_LIST_FILE, 'w', encoding='utf-8') as f:
        f.write("# List of models to test - one per line\n")
        f.write("# Lines starting with # are comments\n\n")
        for model in models:
            f.write(f"{model}\n")
    print_success(f"Saved to {MODELS_LIST_FILE}")

def get_models_from_user() -> list:
    """Get list of models to test from user"""
    print_header("Model List Setup")
    
    # Check if we have a saved list
    saved_models = load_models_list()
    if saved_models:
        print(f"Found saved list with {len(saved_models)} models:")
        for i, model in enumerate(saved_models, 1):
            print(f"  {i}. {model}")
        
        if HAS_QUESTIONARY:
            use_saved = questionary.confirm("Use this list?", default=True).ask()
            if use_saved:
                return saved_models
        else:
            use = input("\nUse this list? (Y/n): ").strip().lower()
            if use != 'n':
                return saved_models
    
    # Get new list from user
    print("\nEnter model names (one per line, empty line to finish):")
    print("Example: Phi-4-mini-reasoning-Q4_K_M")
    print()
    
    models = []
    while True:
        model = input(f"Model {len(models) + 1}: ").strip()
        if not model:
            break
        models.append(model)
    
    if models:
        save_models_list(models)
    
    return models

def run_batch_tests(model_names: list):
    """Run tests for each model in the list"""
    total = len(model_names)
    overall_start = datetime.now()
    
    print_header(f"🚀 Starting Batch Test - {total} model(s)")
    print(f"Started: {overall_start.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = []
    completed = 0
    
    for idx, model_name in enumerate(model_names, 1):
        print_header(f"[{idx}/{total}] Model: {model_name}")
        
        # Ask user to load the model
        wait_for_model_load(model_name)
        
        # Run the test
        try:
            print(f"\n  → Running crisis questions test...")
            model_start = datetime.now()
            
            test_module.main(model_name=model_name)
            
            model_end = datetime.now()
            duration = (model_end - model_start).total_seconds()
            
            print_success(f"Completed in {duration:.0f} seconds ({duration/60:.1f} minutes)")
            
            results.append({
                "model": model_name,
                "status": "SUCCESS",
                "duration_seconds": duration
            })
            completed += 1
            
        except KeyboardInterrupt:
            print_warning("\nTest interrupted by user")
            skip = input("Skip this model and continue? (y/N): ").strip().lower()
            if skip != 'y':
                raise
            results.append({"model": model_name, "status": "SKIPPED"})
            
        except Exception as e:
            print_error(f"Error: {e}")
            results.append({"model": model_name, "status": "ERROR", "error": str(e)})
        
        print()
    
    # Summary
    overall_end = datetime.now()
    overall_duration = (overall_end - overall_start).total_seconds()
    
    print_header("📊 Batch Test Summary")
    print(f"Total time: {overall_duration:.0f} seconds ({overall_duration/60:.1f} minutes)")
    print(f"\nResults:")
    
    for result in results:
        status = result['status']
        if status == 'SUCCESS':
            dur = result.get('duration_seconds', 0)
            print(f"{Colors.OKGREEN}✓ {result['model']} ({dur:.0f}s){Colors.ENDC}")
        elif status == 'SKIPPED':
            print(f"{Colors.WARNING}⊘ {result['model']} (skipped){Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}✗ {result['model']} - {result.get('error', 'failed')}{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}Completed: {completed}/{total}{Colors.ENDC}")

def main():
    """Main entry point"""
    print_header("🤖 Crisis-AI Batch Model Tester (Manual Loading)")
    print("This script will prompt you to load each model in LM Studio\n")
    
    # Check LM Studio connection
    try:
        requests.get(f"{LM_STUDIO_BASE_URL}/v1/models", timeout=5)
        print_success(f"Connected to LM Studio at {LM_STUDIO_BASE_URL}")
    except:
        print_error(f"Cannot connect to LM Studio at {LM_STUDIO_BASE_URL}")
        print("Make sure LM Studio is running with the API server started")
        sys.exit(1)
    
    # Get models to test
    models = get_models_from_user()
    
    if not models:
        print_warning("No models to test")
        sys.exit(0)
    
    print(f"\n{Colors.BOLD}Will test {len(models)} models:{Colors.ENDC}")
    for i, m in enumerate(models, 1):
        print(f"  {i}. {m}")
    
    if HAS_QUESTIONARY:
        start = questionary.confirm("\nStart testing?", default=True).ask()
        if not start:
            sys.exit(0)
    else:
        input("\nPress Enter to start (Ctrl+C to cancel)...")
    
    run_batch_tests(models)
    print_header("✨ All done!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}⚠ Cancelled by user{Colors.ENDC}")
        sys.exit(130)
