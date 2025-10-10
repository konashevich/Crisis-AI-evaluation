# Fixes Applied to Batch Testing Script

## Issue Encountered

When running `batch_test_models.py`, you encountered a **UnicodeDecodeError**:

```
UnicodeDecodeError: 'charmap' codec can't decode byte 0x8f in position 21: 
character maps to <undefined>
```

## Root Cause

The `lms` CLI outputs special Unicode characters (like progress bars, emojis, or extended characters) that Python's default Windows encoding (`cp1252`) couldn't decode when capturing subprocess output.

## Fixes Applied

### 1. **Unicode Error Fix**

Changed from:
```python
result = subprocess.run(
    ["lms", "load", model_path, "--yes", "--quiet"],
    capture_output=True,
    text=True,
    timeout=180
)
```

To:
```python
process = subprocess.Popen(
    ["lms", "load", model_path, "--yes"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    errors='ignore',  # ← Key fix: ignore Unicode errors
    encoding='utf-8'
)
```

**Key changes:**
- Added `errors='ignore'` to handle Unicode decode errors gracefully
- Switched to `Popen` for better control
- Specified `encoding='utf-8'` explicitly

### 2. **Model Loading Verification**

Added new function to verify model is actually ready:

```python
def verify_model_loaded() -> bool:
    """Send a test request to verify model is responding"""
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
```

**Benefits:**
- Confirms model is actually loaded and responding
- Prevents race conditions where model isn't ready yet
- Adds retry logic with longer wait if needed

### 3. **Improved Wait Logic**

```python
if returncode == 0:
    print("    Waiting for model to initialize...")
    time.sleep(5)  # Initial wait
    
    if verify_model_loaded():
        return True
    else:
        print_warning("Model loaded via CLI but not responding. Waiting longer...")
        time.sleep(10)  # Extended wait
        return verify_model_loaded()
```

**Benefits:**
- Waits 5 seconds initially
- Verifies model is ready
- If not ready, waits additional 10 seconds
- Prevents starting questions before model is ready

### 4. **Applied Same Fix to Unload**

```python
process = subprocess.Popen(
    ["lms", "unload", "--all"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    errors='ignore',  # Same Unicode fix
    encoding='utf-8'
)
```

## Testing Results

After fixes:
- ✅ No more Unicode errors
- ✅ Model loads successfully
- ✅ Script verifies model is ready before proceeding
- ✅ Questions execute properly

## Why This Happened

LM Studio's `lms` CLI likely outputs:
- Progress bars with special characters
- Colored terminal output
- Unicode symbols (✓, ⚠, etc.)
- Loading animations

Windows PowerShell uses `cp1252` encoding by default, which doesn't support all these characters. By adding `errors='ignore'`, Python skips characters it can't decode instead of crashing.

## Alternative Solutions Considered

1. **Set environment variable:**
   ```python
   env = os.environ.copy()
   env['PYTHONIOENCODING'] = 'utf-8'
   ```

2. **Use different encoding:**
   ```python
   encoding='cp1252', errors='replace'  # Replace bad chars with ?
   ```

3. **Suppress CLI output entirely:**
   ```python
   ["lms", "load", model_path, "--yes", "--quiet"]
   ```

We went with `errors='ignore'` + `encoding='utf-8'` as the most robust solution.

## Recommendations

1. **Keep using the fixed script** - It now handles Unicode properly
2. **Monitor first model load** - Ensure verification logic works
3. **Adjust timeouts if needed** - If you have very large models:
   - Increase `timeout=180` to `timeout=300` (5 minutes)
   - Increase final wait from `sleep(10)` to `sleep(20)`

## Summary

The error was **NOT** a timing issue - the model actually loaded fine. It was a **character encoding issue** in capturing the CLI output. The fix ensures:

✅ Unicode characters are handled gracefully  
✅ Model readiness is verified before proceeding  
✅ Better error messages if loading fails  
✅ Proper wait times for model initialization  

Your batch testing should now work smoothly! 🚀
