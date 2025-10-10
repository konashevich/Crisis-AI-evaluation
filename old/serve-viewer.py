#!/usr/bin/env python3
"""
Simple HTTP server to serve the CrisisAI evaluation viewer.
This allows the HTML viewer to access JSON files from the eval_results folder.
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        super().end_headers()

    def do_GET(self):
        # Handle requests for eval_results folder
        if self.path.startswith('/eval_results/'):
            file_path = self.path[1:]  # Remove leading slash
            if os.path.exists(file_path) and os.path.isfile(file_path):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_error(404, "File not found")
                return

        # Handle directory listing for eval_results
        if self.path == '/eval_results' or self.path == '/eval_results/':
            if os.path.exists('eval_results') and os.path.isdir('eval_results'):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                files = []
                for file in os.listdir('eval_results'):
                    if file.endswith('.json'):
                        file_path = os.path.join('eval_results', file)
                        if os.path.isfile(file_path):
                            # Parse filename for date/time
                            date_time = self.parse_filename(file)
                            files.append({
                                'filename': file,
                                'path': f'/eval_results/{file}',
                                'dateTime': date_time
                            })

                # Sort by timestamp (newest first)
                files.sort(key=lambda x: x['dateTime']['timestamp'] if x['dateTime'] else 0, reverse=True)

                import json
                self.wfile.write(json.dumps({'files': files}).encode('utf-8'))
                return
            else:
                self.send_error(404, "eval_results directory not found")
                return

        # Default behavior for other files
        return super().do_GET()

    def parse_filename(self, filename):
        """Parse filename to extract date and time"""
        import re
        match = re.match(r'gemini_evaluation_report_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})\.json$', filename)
        if match:
            date, time = match.groups()
            return {
                'date': date,
                'time': time.replace('-', ':'),
                'timestamp': int(__import__('time').mktime(__import__('time').strptime(f'{date} {time.replace("-", ":")}', '%Y-%m-%d %H:%M:%S')))
            }
        return None

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
    print(f"Open your browser to: http://localhost:{port}/evaluation-viewer.html")
    print("Press Ctrl+C to stop the server")

    with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            httpd.shutdown()

if __name__ == "__main__":
    main()