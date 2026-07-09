import urllib.request
import re

url = "https://omniverse-content-production.s3-us-west-2.amazonaws.com/?prefix=Assets/Isaac/6.0/"
keys = []
last_key = ""

while True:
    fetch_url = url
    if last_key:
        # URL encode the marker (spaces to + or %20, slash to %2F, etc.)
        import urllib.parse
        fetch_url += f"&marker={urllib.parse.quote(last_key)}"
    
    print(f"Fetching S3 page... marker={last_key[:25] if last_key else 'None'}")
    try:
        req = urllib.request.Request(fetch_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            xml_data = response.read().decode('utf-8')
            
        page_keys = re.findall(r"<Key>([^<]+)</Key>", xml_data)
        if not page_keys:
            break
            
        keys.extend(page_keys)
        print(f"Added {len(page_keys)} keys. Total={len(keys)}")
        
        is_truncated = "<IsTruncated>true</IsTruncated>" in xml_data
        if is_truncated:
            last_key = page_keys[-1]
        else:
            break
    except Exception as e:
        print("Error fetching S3 list:", e)
        break

print(f"\nTotal keys found: {len(keys)}")

# Let's search!
print("\n--- Cones ---")
for k in keys:
    if "cone" in k.lower() and k.endswith(".usd"):
        print(k)

print("\n--- Barrier / Barricade ---")
for k in keys:
    if ("barrier" in k.lower() or "barricade" in k.lower()) and k.endswith(".usd"):
        print(k)

print("\n--- Pedestrian / Police / People ---")
for k in keys:
    if ("police" in k.lower() or "character" in k.lower() or "people" in k.lower()) and k.endswith(".usd"):
        print(k)

print("\n--- Carter / Vehicles ---")
for k in keys:
    if "carter" in k.lower() and k.endswith(".usd"):
        print(k)
