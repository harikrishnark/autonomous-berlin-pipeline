import urllib.request
import re

url = "https://omniverse-content-production.s3-us-west-2.amazonaws.com/?prefix=Assets/Isaac/6.0"
print(f"Fetching S3 listing from: {url}")
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        xml = response.read().decode('utf-8')
    
    print("S3 data retrieved! Searching for keys...")
    keys = re.findall(r"<Key>([^<]+)</Key>", xml)
    
    print("\n--- Cones ---")
    for key in keys:
        if "cone" in key.lower():
            print(key)
            
    print("\n--- Barrier/Barricade ---")
    for key in keys:
        if "barrier" in key.lower() or "barricade" in key.lower():
            print(key)
            
    print("\n--- Police/Pedestrian ---")
    for key in keys:
        if "police" in key.lower() or "character" in key.lower() or "people" in key.lower():
            print(key)
            
    print("\n--- Carter/Robot ---")
    for key in keys:
        if "carter" in key.lower():
            print(key)

except Exception as e:
    print("Error:", e)
