#!/usr/bin/env python3
"""
Simple HTTP server to serve the CrisisAI evaluation viewer.
This allows the HTML viewer to access JSON files from the eval_results folder.
"""

import http.server
import socketserver
import os
from pathlib import Path

def main():
    # Change to the directory containing this script
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    port = 8000

    # Check if eval_results directory exists
    if not os.path.exists('eval_results'):
        print("Warning: eval_results directory not found. Creating it...")
        os.makedirs('eval_results', exist_ok=True)

    print(f"Starting server on port {port}")
    print(f"Open your browser to: http://localhost:8000/evaluation-viewer.html")
    print("Press Ctrl+C to stop the server")

    # Use Python's built-in server
    with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            httpd.shutdown()

if __name__ == "__main__":
    main()