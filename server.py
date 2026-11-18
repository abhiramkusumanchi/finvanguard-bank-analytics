"""
FinVanguard 360 - Production Web Server for Railway Deployment
Serves the interactive banking intelligence dashboard and REST assets.
Binds dynamically to Railway's $PORT environment variable.
"""

import os
import sys
import http.server
import socketserver

PORT = int(os.environ.get("PORT", 8080))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DASHBOARD_DIR, **kwargs)
        
    def end_headers(self):
        # Enable CORS and caching headers for optimal performance
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

def run_server():
    print("==================================================")
    print("  FINVANGUARD 360° - PRODUCTION HTTP WEB SERVER   ")
    print("==================================================")
    print(f"[*] Serving Directory: {DASHBOARD_DIR}")
    print(f"[*] Binding to Port:   {PORT}")
    print(f"[*] Host Address:      0.0.0.0")
    print("==================================================")
    
    # Allow socket address reuse on restart
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("0.0.0.0", PORT), CustomHandler) as httpd:
        print(f"[+] Server live! Listening at http://0.0.0.0:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[-] Shutting down server...")
            httpd.shutdown()

if __name__ == "__main__":
    run_server()
