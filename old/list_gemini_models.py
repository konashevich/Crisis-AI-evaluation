import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('GEMINI_API_KEY')
if not key:
    print('GEMINI_API_KEY not set in environment or .env')
    raise SystemExit(1)

url = f'https://generativelanguage.googleapis.com/v1beta/models?key={key}'
print(f'Calling ListModels endpoint...')
resp = requests.get(url, timeout=30)
print(f'Status: {resp.status_code}')
try:
    print(json.dumps(resp.json(), indent=2))
except Exception:
    print(resp.text)
