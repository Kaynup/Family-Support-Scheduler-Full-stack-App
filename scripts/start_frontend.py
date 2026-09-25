#!/usr/bin/env python3
"""
Start a simple static HTTP server on the first available port in 8001..8010.
This avoids failing when 8001 is already in use.
"""

import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

START = 8001
END = 8010

for port in range(START, END + 1):
    try:
        server = ThreadingHTTPServer(("", port), SimpleHTTPRequestHandler)
    except OSError:
        continue
    print(f"Serving frontend at http://127.0.0.1:{port} (press CTRL+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down server")
        server.server_close()
        sys.exit(130)

print(f"No available ports in range {START}-{END}.")
sys.exit(1)
