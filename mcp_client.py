import requests
import json
import uuid

MCP_SERVER_URL = "https://vipfapwm3x.us-east-1.awsapprunner.com/mcp"

def call_mcp(payload: dict):
    """
    Call MCP server using JSON-RPC 2.0 format
    """
    try:
        # Convert your simple payload to JSON-RPC format
        jsonrpc_request = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),  # Unique request ID
            "method": "tools/call",   # MCP standard method
            "params": {
                "name": payload.get("action"),  # tool name
                "arguments": {k: v for k, v in payload.items() if k != "action"}
            }
        }
        
        response = requests.post(
            MCP_SERVER_URL,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json=jsonrpc_request,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")  # Debug
        print(f"Response: {response.text}\n")  # Debug
        
        if response.status_code != 200:
            return {"error": f"MCP error {response.status_code}: {response.text}"}
        
        result = response.json()
        
        # Extract the actual result from JSON-RPC response
        if "result" in result:
            return result["result"]
        elif "error" in result:
            return {"error": result["error"]}
        
        return result
        
    except Exception as e:
        return {"error": str(e)}