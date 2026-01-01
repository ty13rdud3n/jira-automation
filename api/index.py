from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
from urllib.parse import urlparse

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        path = urlparse(self.path).path
        
        if path == '/api' or path == '/api/':
            self._send_response(200, {
                "service": "Jira Webhook API",
                "endpoints": {
                    "webhook": "POST /api/jira/webhook",
                    "health": "GET /api/health"
                }
            })
        elif path == '/api/health':
            self._send_response(200, {"status": "healthy"})
        else:
            self._send_response(404, {"error": "Not found"})
    
    def do_POST(self):
        path = urlparse(self.path).path
        
        if path == '/api/jira/webhook':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                data = json.loads(body) if body else {}
            except:
                data = {}
            
            # Log the received data
            print(f"🎫 JIRA ISSUE RECEIVED at {datetime.now()}")
            
            if 'issueKey' in data:
                print(f"Issue Key: {data.get('issueKey')}")
                print(f"Summary: {data.get('summary')}")
            elif 'key' in data:
                print(f"Issue Key: {data.get('key')}")
                fields = data.get('fields', {})
                print(f"Summary: {fields.get('summary')}")
            else:
                print(f"Raw payload: {data}")
            
            self._send_response(200, {
                "status": "success",
                "message": "Issue received successfully",
                "timestamp": datetime.now().isoformat(),
                "received": data
            })
        else:
            self._send_response(404, {"error": "Not found"})
    
    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())