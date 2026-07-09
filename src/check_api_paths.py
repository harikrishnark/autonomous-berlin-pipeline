import urllib.request
import json

try:
    response = urllib.request.urlopen("http://localhost:8011/openapi.json")
    data = json.loads(response.read().decode())
    print("API Paths:")
    for path in sorted(data.get("paths", {}).keys()):
        print(f"  {path}")
except Exception as e:
    print(f"Error checking API paths: {e}")
