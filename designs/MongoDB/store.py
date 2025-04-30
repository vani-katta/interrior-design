from http.server import BaseHTTPRequestHandler, HTTPServer
from pymongo import MongoClient
from bson.binary import Binary
from bson.objectid import ObjectId
import cgi
import base64
import json

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["image_db"]
collection = db["images"]

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type="text/html"):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        # Enable CORS
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
        self.end_headers()

    def do_GET(self):
        if self.path == "/gallery":
            self._set_headers("application/json")
            items = collection.find()
            result = []

            for item in items:
                image_base64 = base64.b64encode(item['image']).decode('utf-8')
                result.append({
                    "text": item['text'],
                    "image": f"data:image/jpeg;base64,{image_base64}"
                })

            self.wfile.write(json.dumps(result).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/upload':
            content_type, pdict = cgi.parse_header(self.headers['Content-Type'])
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])

            fields = cgi.parse_multipart(self.rfile, pdict)
            text = fields.get('text')[0]
            image = fields.get('image')[0]

            collection.insert_one({'text': text, 'image': Binary(image)})

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Upload successful.")
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
