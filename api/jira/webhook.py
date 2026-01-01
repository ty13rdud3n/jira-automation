from http.server import BaseHTTPRequestHandler
from datetime import datetime
import json

class handler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        # Read the request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            data = {}
        
        # Log the received data (visible in Vercel logs)
        print("=" * 60)
        print(f"🎫 JIRA ISSUE RECEIVED at {datetime.now()}")
        print("=" * 60)
        
        if 'issueKey' in data:
            # Custom payload format
            print(f"Issue Key:   {data.get('issueKey', 'N/A')}")
            print(f"Summary:     {data.get('summary', 'N/A')}")
            print(f"Issue Type:  {data.get('issueType', 'N/A')}")
            print(f"Priority:    {data.get('priority', 'N/A')}")
            print(f"Reporter:    {data.get('reporter', 'N/A')}")
        elif 'key' in data:
            # Jira automation format
            print(f"Issue Key:   {data.get('key', 'N/A')}")
            fields = data.get('fields', {})
            print(f"Summary:     {fields.get('summary', 'N/A')}")
            print(f"Issue Type:  {fields.get('issuetype', {}).get('name', 'N/A')}")
            print(f"Priority:    {fields.get('priority', {}).get('name', 'N/A')}")
            print(f"Reporter:    {fields.get('reporter', {}).get('displayName', 'N/A')}")
        else:
            print("Raw payload received:")
            print(data)
        
        print("=" * 60)
        
        # Send response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "success",
            "message": "Issue received successfully",
            "timestamp": datetime.now().isoformat()
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {"message": "Send POST request with Jira data"}
        self.wfile.write(json.dumps(response).encode('utf-8'))