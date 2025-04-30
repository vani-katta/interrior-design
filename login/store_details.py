from http.server import BaseHTTPRequestHandler, HTTPServer
from pymongo import MongoClient
from bson.binary import Binary
import cgi
import json
import base64

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
        if self.path == "/":
            self._set_headers("text/html")
            with open("login.html", "rb") as f:
                self.wfile.write(f.read())
        elif self.path == "/designers":
            self._set_headers("application/json")
            designers = list(collection.find({"role": "designer"}))
            for designer in designers:
                designer["_id"] = str(designer["_id"])
                if designer.get("image"):
                    designer["image"] = base64.b64encode(designer["image"]).decode('utf-8')
            self.wfile.write(json.dumps(designers).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/register':
            content_type, pdict = cgi.parse_header(self.headers['Content-Type'])
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])

            fields = cgi.parse_multipart(self.rfile, pdict)
            name = fields.get('name', [None])[0]
            email = fields.get('email', [None])[0]
            password = fields.get('password', [None])[0]
            role = fields.get('role', [None])[0]

            if not all([name, email, password, role]):
                self._set_headers()
                response = {"status": "error", "message": "Missing required fields."}
                self.wfile.write(json.dumps(response).encode())
                return

            if role == "designer":
                phone = fields.get('phone', [None])[0]
                image = fields.get('image', [None])[0]
                collection.insert_one({
                    'name': name,
                    'email': email,
                    'password': password,
                    'role': role,
                    'phone': phone,
                    'image': Binary(image) if image else None
                })
            else:
                collection.insert_one({
                    'name': name,
                    'email': email,
                    'password': password,
                    'role': role
                })

            self._set_headers()
            response = {"status": "success", "message": "Registration successful."}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running at http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
