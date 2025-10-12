"""
Simple HTTP server to serve the evaluation viewer.
Resolves CORS issues when viewing evaluation-viewer.html
"""
import http.server
import socketserver
import webbrowser
import os

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    # Change to the script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        url = f"http://localhost:{PORT}/evaluation-viewer.html"
        print(f"╔═══════════════════════════════════════════════════════════╗")
        print(f"║  CrisisAI Evaluation Viewer Server                       ║")
        print(f"╚═══════════════════════════════════════════════════════════╝")
        print(f"\n✅ Server running at: {url}")
        print(f"\n🌐 Opening browser...")
        print(f"\n💡 Press Ctrl+C to stop the server\n")
        
        # Open browser
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print(f"   Please open this URL manually: {url}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped")

if __name__ == "__main__":
    main()
