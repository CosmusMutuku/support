import requests
import json
import uuid

MCP_SERVER_URL = "https://vipfapwm3x.us-east-1.awsapprunner.com/mcp"

# Try to list available tools
jsonrpc_request = {
    "jsonrpc": "2.0",
    "id": str(uuid.uuid4()),
    "method": "tools/list",
    "params": {}
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

print(f"Status: {response.status_code}")
print(f"Available tools:\n{json.dumps(response.json(), indent=2)}")