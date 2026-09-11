#!/usr/bin/env python3
"""
LectureMind Local Server
Serves the LectureMind application locally.
"""
import http.server
import socketserver
import os
import sys

DEFAULT_PORT = 3000 if len(sys.argv) < 2 else int(sys.argv[1])
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    port = DEFAULT_PORT
    httpd = None

    for p in range(port, port + 10):
        try:
            httpd = ReusableTCPServer(("", p), Handler)
            port = p
            break
        except OSError:
            continue

    if not httpd:
        print("Error: Could not bind to any port from 3000 to 3010.")
        sys.exit(1)

    print(f"==================================================")
    print(f"  LectureMind App running at: http://localhost:{port}")
    print(f"  Serving files from: {DIRECTORY}")
    print(f"==================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")