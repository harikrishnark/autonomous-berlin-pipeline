import urllib.request
import re

import urllib.request
import re
import xml.etree.ElementTree as ET

url = "https://omniverse-content-production.s3-us-west-2.amazonaws.com/?prefix=Assets/Isaac/6.0/Isaac/"
keys = []
continuation_token = ""

while True:
    fetch_url = url
    if continuation_token:
        fetch_url += f"&continuation-token={continuation_token}"
    
    print(f"Fetching S3 page... {fetch_url[:80]}")
    try:
        req = urllib.request.Request(fetch_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        # S3 uses namespaces
        ns = {'s3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
        
        for contents in root.findall('s3:Contents', ns):
            key = contents.find('s3:Key', ns).text
            keys.append(key)
            
        is_truncated = root.find('s3:IsTruncated', ns)
        if is_truncated is not None and is_truncated.text == 'true':
            next_token = root.find('s3:NextContinuationToken', ns)
            if next_token is not None:
                continuation_token = next_token.text
            else:
                break
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
