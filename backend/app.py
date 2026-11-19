from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class BackendHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = {
            "service": "backend",
            "status": "healthy",
            "message": "Hello from Backend!"
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

server = HTTPServer(("0.0.0.0", 5000), BackendHandler)

print("Backend server listening on port 5000")

server.serve_forever()
