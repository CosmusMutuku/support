from mcp_client import call_mcp

print("=== Test 1: Search for monitors ===")
result1 = call_mcp({"action": "search_products", "query": "monitor"})
print(f"Result: {result1}\n")

print("="*60 + "\n")

print("=== Test 2: List all products ===")
result2 = call_mcp({"action": "list_products"})
print(f"Result: {result2}\n")

print("="*60 + "\n")

print("=== Test 3: Verify customer PIN ===")
result3 = call_mcp({
    "action": "verify_customer_pin",
    "email": "donaldgarcia@example.net",
    "pin": "7912"
})
print(f"Result: {result3}\n")

print("="*60 + "\n")

print("=== Test 4: Get specific product by SKU ===")
result4 = call_mcp({"action": "get_product", "sku": "MON-0054"})
print(f"Result: {result4}\n")