from http.server import BaseHTTPRequestHandler, HTTPServer
from pymongo import MongoClient
import json
import base64
import os

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["interrior_db"]
collection = db["designers"]

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        # Serve static files from the 'static' folder
        if self.path.startswith("/static/"):
            self._serve_static_file()
            return

        if self.path == "/":
            self._set_headers("text/html")
            with open("designers.html", "rb") as f:
                self.wfile.write(f.read())
        elif self.path == "/designers":
            self._set_headers("application/json")
            designers = list(collection.find({"role": "designer"}))
            for designer in designers:
                designer["_id"] = str(designer["_id"])
                if designer.get("image"):
                    designer["image"] = base64.b64encode(designer["image"]).decode('utf-8')
                # Keep only relevant fields
                designer = {key: designer[key] for key in ("_id", "name", "phone", "image")}
            self.wfile.write(json.dumps(designers).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def _serve_static_file(self):
        # Serve the static file by reading from the 'static' folder
        file_path = self.path[7:]  # Remove '/static/' from path
        if os.path.exists(file_path):
            self._set_headers("application/octet-stream")
            with open(file_path, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=9000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running at http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
