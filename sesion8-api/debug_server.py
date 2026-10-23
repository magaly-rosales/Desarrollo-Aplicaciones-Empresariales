from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys

class DebugHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        content_type = self.headers.get('Content-Type', '')
        accept = self.headers.get('Accept', '')
        auth = self.headers.get('Authorization', '')
        
        print(f"METHOD: {self.command}", file=sys.stderr)
        print(f"PATH: {self.path}", file=sys.stderr)
        print(f"Content-Type: {content_type}", file=sys.stderr)
        print(f"Accept: {accept}", file=sys.stderr)
        print(f"Authorization: {auth[:30]}...", file=sys.stderr)
        print(f"Content-Length: {content_length}", file=sys.stderr)
        
        body = self.rfile.read(content_length)
        print(f"RAW BODY: {body}", file=sys.stderr)
        print(f"RAW BODY TYPE: {type(body)}", file=sys.stderr)
        print(f"RAW BODY LENGTH: {len(body)}", file=sys.stderr)
        
        try:
            data = json.loads(body)
            print(f"PARSED JSON: {data}", file=sys.stderr)
        except Exception as e:
            print(f"JSON PARSE ERROR: {e}", file=sys.stderr)
        
        self.send_response(201)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok", "received": len(body)}).encode())
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())
    
    def log_message(self, format, *args):
        pass  # suppress default logging

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8003), DebugHandler)
    print("Server listening on port 8003", file=sys.stderr)
    server.serve_forever()
