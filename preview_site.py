import http.server
import socketserver
import os
import webbrowser

PORT = 8001
DIRECTORY = r"c:\Users\since\新しいフォルダー\trend_arbitrage_project\whiskey_blog\docs"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

print(f"Serving local preview at http://localhost:{PORT}")
print("Opening browser...")

# Open browser automatically
webbrowser.open(f"http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Server started. Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()
