#!/usr/bin/env python3
"""
Simple HTTP Server for Stripe M2 Reader Setup
Run this to serve the HTML file from a proper web server
"""

import http.server
import socketserver
import webbrowser
import os
import sys

# Configuration
PORT = 8000
HOSTNAME = "localhost"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        # Customize log format
        print(f"[{self.address_string()}] {format % args}")

def main():
    # Change to the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check if HTML file exists
    html_file = "index.html"
    if not os.path.exists(html_file):
        print(f"❌ Error: {html_file} not found in {script_dir}")
        print("Make sure this script is in the same directory as the HTML file.")
        sys.exit(1)
    
    # Create server
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            url = f"http://{HOSTNAME}:{PORT}/{html_file}"
            
            print("🚀 Stripe M2 Reader Setup Server")
            print("=" * 40)
            print(f"Server running at: http://{HOSTNAME}:{PORT}/")
            print(f"Reader setup page: {url}")
            print("=" * 40)
            print("📱 Test URL examples:")
            print(f"{url}?restaurant=Test%20Restaurant&location_id=tml_test123&row_id=ROW-1&regemail=test%40test.com")
            print()
            print("Press Ctrl+C to stop the server")
            print()
            
            # Try to open browser
            try:
                webbrowser.open(url)
                print(f"🌐 Opened {url} in your default browser")
            except Exception as e:
                print(f"⚠️ Could not open browser automatically: {e}")
                print(f"Please manually open: {url}")
            
            # Start server
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} is already in use")
            print(f"Try a different port: python3 serve.py --port 8001")
        else:
            print(f"❌ Server error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    # Simple command line argument parsing
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Usage: python3 serve.py [--port PORT]")
            print("Default port: 8000")
            sys.exit(0)
        elif sys.argv[1] == "--port" and len(sys.argv) > 2:
            try:
                PORT = int(sys.argv[2])
            except ValueError:
                print("❌ Invalid port number")
                sys.exit(1)
    
    main()
