"""
Jira Webhook API for Vercel
"""

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/api/jira/webhook', methods=['POST'])
def receive_jira_issue():
    """Endpoint to receive Jira issue data"""
    
    data = request.json
    
    # Log the received data (visible in Vercel logs)
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
    
    return jsonify({
        "status": "success",
        "message": "Issue received successfully",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


# Root endpoint
@app.route('/api', methods=['GET'])
def root():
    return jsonify({
        "service": "Jira Webhook API",
        "endpoints": {
            "webhook": "POST /api/jira/webhook",
            "health": "GET /api/health"
        }
    }), 200