from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen
from urllib.error import URLError
import json
import os

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend:5000"
)

class FrontendHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with urlopen(BACKEND_URL, timeout=5) as response:
                backend_data = json.loads(response.read().decode())

            result = {
                "service": "frontend",
                "backend_response": backend_data
            }

            self.send_response(200)

        except Exception as error:
            result = {
                "service": "frontend",
                "error": str(error)
            }

            self.send_response(502)

        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

server = HTTPServer(("0.0.0.0", 8080), FrontendHandler)

print("Frontend listening on port 8080")
print(f"Backend URL: {BACKEND_URL}")

server.serve_forever()
