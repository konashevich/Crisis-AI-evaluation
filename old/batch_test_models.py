"""
Batch Model Tester for Crisis-AI Evaluation
Provides an interactive terminal interface to select and test multiple LM Studio models.
"""
import json
import os
import sys
import time
import re
import requests
from datetime import datetime
from typing import List, Dict, Any

# Try to import questionary for better UI, fall back to simple input
try:
    import questionary
    HAS_QUESTIONARY = True
except ImportError:
    HAS_QUESTIONARY = False
    print("⚠️  For better UI, install questionary: pip install questionary")
    print()

# Import the main testing function from the existing script
import importlib.util
spec = importlib.util.spec_from_file_location("test_script", "llm-crisis-questions-test.py")
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)

# Configuration
LM_STUDIO_BASE_URL = os.environ.get("LM_STUDIO_API_URL", "http://localhost:1234").rstrip('/v1/chat/completions').rstrip('/v1')
MODELS_CONFIG_FILE = "models_config.json"

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str):
    """Print a colored header"""
    print(f"\n{Colors.BOLD}{Colors.OKCYAN}{text}{Colors.ENDC}")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def get_available_models() -> List[Dict[str, Any]]:
    """
    Fetch available models from LM Studio using CLI.
    Returns a list of model dictionaries with 'id' and 'display_name' keys.
    """
    import subprocess
    import re
    
    try:
        result = subprocess.run(
            ["lms", "ls"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            print_error("Failed to list models with 'lms ls'")
            return []
        
        # Parse the output to extract model names
        # Looking for lines like: "deepseek/deepseek-r1-0528-qwen3-8b (1 variant)"
        models = []
        lines = result.stdout.split('\n')
        
        for line in lines:
            line = line.strip()
            # Skip headers, empty lines, and embedding models
            if not line or 'PARAMS' in line or 'EMBEDDING' in line or line.startswith('You have'):
                continue
            
            # Extract model name (everything before whitespace or params)
            # Format: "model-name PARAMS ARCH SIZE" or "model-name (X variants) PARAMS ARCH SIZE"
            match = re.match(r'^([a-zA-Z0-9/_.-]+(?:\s*\([^)]+\))?)\s+', line)
            if match:
                model_id = match.group(1).strip()
                # Remove variant info for cleaner display
                display_name = re.sub(r'\s*\(\d+\s+variants?\)', '', model_id)
                models.append({
                    'id': model_id,
                    'display_name': display_name
                })
        
        return models
        
    except FileNotFoundError:
        print_error("'lms' CLI not found. Install with: npx lmstudio install-cli")
        print_info("Falling back to empty model list")
        return []
    except Exception as e:
        print_error(f"Failed to fetch models: {e}")
        return []

def load_model(model_path: str) -> bool:
    """
    Load a model in LM Studio using CLI.
    Returns True if successful, False otherwise.
    """
    import subprocess
    try:
        print(f"    Loading via CLI: lms load '{model_path}' --yes")
        
        # Use PIPE with errors='ignore' to avoid Unicode decode issues
        process = subprocess.Popen(
            ["lms", "load", model_path, "--yes"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors='ignore',  # Ignore Unicode decode errors
            encoding='utf-8'
        )
        
        # Wait for process to complete with timeout
        try:
            stdout, stderr = process.communicate(timeout=180)
            returncode = process.returncode
        except subprocess.TimeoutExpired:
            process.kill()
            print_error("Model loading timed out (>3 minutes)")
            return False
        
        if returncode == 0:
            # Wait for model to fully initialize and verify it's ready
            print("    Waiting for model to initialize...")
            time.sleep(5)
            
            # Verify model is actually loaded by checking API
            if verify_model_loaded():
                return True
            else:
                print_warning("Model loaded via CLI but not responding on API. Waiting longer...")
                time.sleep(10)
                return verify_model_loaded()
        else:
            print_error(f"CLI load failed with code {returncode}")
            if stderr:
                print_error(f"Error: {stderr[:200]}")  # First 200 chars
            return False
            
    except FileNotFoundError:
        print_error("'lms' CLI not found. Install with: npx lmstudio install-cli")
        return False
    except Exception as e:
        print_error(f"Failed to load model: {e}")
        return False

def verify_model_loaded() -> bool:
    """
    Verify a model is actually loaded and responding by sending a test request.
    Returns True if model responds, False otherwise.
    """
    try:
        response = requests.post(
            f"{LM_STUDIO_BASE_URL}/v1/chat/completions",
            json={
                "model": "local-model",
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 1
            },
            timeout=10
        )
        return response.status_code == 200
    except:
        return False

def unload_model() -> bool:
    """
    Unload all loaded models in LM Studio using CLI.
    Returns True if successful, False otherwise.
    """
    import subprocess
    try:
        process = subprocess.Popen(
            ["lms", "unload", "--all"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors='ignore',  # Ignore Unicode decode errors
            encoding='utf-8'
        )
        
        try:
            stdout, stderr = process.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            process.kill()
            print_warning("Unload timed out, continuing anyway")
            
        time.sleep(2)  # Brief wait for cleanup
        return True  # Don't fail on unload errors
    except Exception as e:
        print_warning(f"Failed to unload model (may not be critical): {e}")
        return False

def save_model_selection(models: List[Dict[str, str]]):
    """Save selected models to config file for future use"""
    config = {
        "last_updated": datetime.now().isoformat(),
        "models": [{"id": m['id'], "display_name": m['display_name']} for m in models]
    }
    with open(MODELS_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    print_success(f"Saved selection to {MODELS_CONFIG_FILE}")

def load_model_selection() -> List[Dict[str, str]]:
    """Load previously selected models from config file"""
    if os.path.exists(MODELS_CONFIG_FILE):
        try:
            with open(MODELS_CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('models', [])
        except Exception as e:
            print_warning(f"Could not load previous selection: {e}")
    return []

def select_models_interactive(available_models: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Interactive model selection using questionary (if available) or simple input.
    Returns list of selected model dicts with 'id' and 'display_name'.
    """
    if not available_models:
        print_error("No models available to select!")
        return []
    
    if HAS_QUESTIONARY:
        # Use questionary for nice checkbox interface
        # Create choices with display names
        choices = [m['display_name'] for m in available_models]
        selected_names = questionary.checkbox(
            "Select models to test (use Space to select, Enter to confirm):",
            choices=choices
        ).ask()
        
        if not selected_names:
            return []
        
        # Map back to full model objects
        return [m for m in available_models if m['display_name'] in selected_names]
    else:
        # Fallback to simple numbered selection
        print_header("Available Models:")
        for idx, model in enumerate(available_models, 1):
            print(f"  {idx}. {model['display_name']}")
        
        print("\nEnter model numbers to test (comma-separated, e.g., 1,3,5):")
        print("Or press Enter to select all models")
        
        user_input = input("> ").strip()
        
        if not user_input:
            return available_models
        
        try:
            indices = [int(x.strip()) - 1 for x in user_input.split(',')]
            selected = [available_models[i] for i in indices if 0 <= i < len(available_models)]
            return selected
        except (ValueError, IndexError):
            print_error("Invalid input. Please try again.")
            return select_models_interactive(available_models)

def create_batch_folder() -> str:
    """
    Create a new batch folder in test_results with format YYYY-MM-DD_N
    where N is incremental for same-day runs.
    Returns the full path to the created folder.
    """
    base_dir = test_module.RESULTS_DIR
    os.makedirs(base_dir, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Find existing folders for today
    existing = []
    for item in os.listdir(base_dir):
        if os.path.isdir(os.path.join(base_dir, item)) and item.startswith(today):
            # Extract the number from YYYY-MM-DD_N
            match = re.match(rf"{today}_(\d+)", item)
            if match:
                existing.append(int(match.group(1)))
    
    # Get next number
    next_num = max(existing) + 1 if existing else 1
    
    batch_folder_name = f"{today}_{next_num}"
    batch_folder_path = os.path.join(base_dir, batch_folder_name)
    os.makedirs(batch_folder_path, exist_ok=True)
    
    print_success(f"Created batch folder: {batch_folder_name}")
    return batch_folder_path

def extract_model_name(model_id: str) -> str:
    """
    Extract a clean model name from the model ID/path.
    Handles both full paths and simple names.
    """
    # If it's a path, get the filename without extension
    if '/' in model_id or '\\' in model_id:
        name = os.path.basename(model_id)
        name = os.path.splitext(name)[0]  # Remove .gguf extension
        return name
    return model_id

def run_batch_tests(selected_models: List[Dict[str, str]]):
    """
    Run the crisis questions test for each selected model.
    """
    total_models = len(selected_models)
    overall_start = datetime.now()
    
    # Create batch folder for this run
    batch_folder = create_batch_folder()
    
    print_header(f"🚀 Starting Batch Test Run - {total_models} model(s)")
    print(f"Started at: {overall_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Results folder: {os.path.basename(batch_folder)}\n")
    
    results_summary = []
    
    for idx, model in enumerate(selected_models, 1):
        model_id = model['id']
        model_display_name = model['display_name']
        # Use display name for file output (cleaner)
        model_name = extract_model_name(model_display_name)
        
        print_header(f"[{idx}/{total_models}] Testing: {model_display_name}")
        print(f"Loading: {model_id}")
        
        # Unload any previously loaded model
        print("  → Unloading previous model...")
        unload_model()
        
        # Load the new model
        print(f"  → Loading model...")
        if not load_model(model_id):
            print_error(f"Failed to load model. Skipping...")
            results_summary.append({
                "model": model_name,
                "status": "FAILED_TO_LOAD",
                "error": "Could not load model via CLI"
            })
            continue
        
        print_success(f"Model loaded: {model_display_name}")
        
        # Run the test
        try:
            print(f"  → Running crisis questions test...")
            
            # Call the main testing function with the model name and batch folder
            test_module.main(model_name=model_name, results_dir=batch_folder)
            
            # Read the accurate timing from the runinfo file
            # The runinfo file has timing that starts from first question, not from file loading
            import glob
            runinfo_pattern = os.path.join(batch_folder, f"{model_name}_*_runinfo.json")
            runinfo_files = glob.glob(runinfo_pattern)
            
            if runinfo_files:
                # Get the most recent runinfo file
                latest_runinfo = max(runinfo_files, key=os.path.getmtime)
                with open(latest_runinfo, 'r', encoding='utf-8') as f:
                    runinfo = json.load(f)
                    duration = runinfo.get('duration_seconds', 0)
                    duration_mmss = runinfo.get('duration_mmss', '00:00')
            else:
                # Fallback: calculate from our timer (less accurate)
                model_end = datetime.now()
                duration = (model_end - datetime.now()).total_seconds()  # This won't work well
                duration_mmss = f"{int(duration//60):02d}:{int(duration%60):02d}"
            
            print_success(f"Completed {model_name} in {duration:.0f} seconds ({duration_mmss})")
            
            results_summary.append({
                "model": model_name,
                "status": "SUCCESS",
                "duration_seconds": duration
            })
            
        except Exception as e:
            print_error(f"Error testing {model_name}: {e}")
            results_summary.append({
                "model": model_name,
                "status": "ERROR",
                "error": str(e)
            })
        
        print()  # Blank line between models
    
    # Unload the last model
    print("  → Cleaning up...")
    unload_model()
    
    # Print summary
    overall_end = datetime.now()
    overall_duration = (overall_end - overall_start).total_seconds()
    
    print_header("📊 Batch Test Summary")
    print(f"Total time: {overall_duration:.0f} seconds ({overall_duration/60:.1f} minutes)")
    print(f"\nResults:")
    
    success_count = sum(1 for r in results_summary if r['status'] == 'SUCCESS')
    
    for result in results_summary:
        status_icon = "✓" if result['status'] == 'SUCCESS' else "✗"
        status_color = Colors.OKGREEN if result['status'] == 'SUCCESS' else Colors.FAIL
        
        model_info = result['model']
        if result['status'] == 'SUCCESS':
            duration = result.get('duration_seconds', 0)
            model_info += f" ({duration:.0f}s)"
        elif 'error' in result:
            model_info += f" - {result['error']}"
        
        print(f"{status_color}{status_icon} {model_info}{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}Success rate: {success_count}/{total_models}{Colors.ENDC}")

def main():
    """Main entry point for the batch tester"""
    print_header("🤖 Crisis-AI Batch Model Tester")
    
    # Check if we can connect to LM Studio
    print(f"Connecting to LM Studio at: {LM_STUDIO_BASE_URL}")
    
    # Fetch available models
    print("🔍 Discovering models from LM Studio...")
    available_models = get_available_models()
    
    if not available_models:
        print_error("No models found or unable to connect to LM Studio.")
        print_info("Please ensure:")
        print("  1. LM Studio is running")
        print("  2. The API server is started (in LM Studio → Developer → Start Server)")
        print(f"  3. The server is accessible at: {LM_STUDIO_BASE_URL}")
        sys.exit(1)
    
    print_success(f"Found {len(available_models)} model(s)")
    
    # Check for previous selection
    previous_selection = load_model_selection()
    use_previous = False
    
    if previous_selection and HAS_QUESTIONARY:
        use_previous = questionary.confirm(
            f"Use previous selection? ({len(previous_selection)} models)",
            default=False
        ).ask()
    
    # Select models
    if use_previous and previous_selection:
        selected_models = previous_selection
        print_info(f"Using {len(selected_models)} previously selected models")
    else:
        selected_models = select_models_interactive(available_models)
    
    if not selected_models:
        print_warning("No models selected. Exiting.")
        sys.exit(0)
    
    print_success(f"{len(selected_models)} model(s) selected")
    
    # Show selected models
    print("\nSelected models:")
    for model in selected_models:
        name = model['display_name'] if isinstance(model, dict) else model
        print(f"  • {name}")
    
    # Save selection
    if HAS_QUESTIONARY:
        save_choice = questionary.confirm(
            "Save this selection for next time?",
            default=True
        ).ask()
        if save_choice:
            save_model_selection(selected_models)
    else:
        save_input = input("\nSave this selection for next time? (y/N): ").strip().lower()
        if save_input == 'y':
            save_model_selection(selected_models)
    
    # Confirm start
    print()
    if HAS_QUESTIONARY:
        start = questionary.confirm(
            "Start batch testing?",
            default=True
        ).ask()
        if not start:
            print_warning("Cancelled by user.")
            sys.exit(0)
    else:
        input("Press Enter to start batch testing (Ctrl+C to cancel)...")
    
    # Run the tests
    run_batch_tests(selected_models)
    
    print_header("✨ All done!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + Colors.WARNING + "⚠ Interrupted by user" + Colors.ENDC)
        sys.exit(130)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
