import urllib.request
import re
import urllib.parse

url = "https://omniverse-content-production.s3-us-west-2.amazonaws.com/?prefix=Assets/Isaac/6.0/"
keys = []
last_key = ""

print("Fetching all keys from S3 to find city/street environments...")
while True:
    fetch_url = url
    if last_key:
        fetch_url += f"&marker={urllib.parse.quote(last_key)}"
    
    try:
        req = urllib.request.Request(fetch_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            xml_data = response.read().decode('utf-8')
            
        page_keys = re.findall(r"<Key>([^<]+)</Key>", xml_data)
        if not page_keys:
            break
            
        keys.extend(page_keys)
        
        is_truncated = "<IsTruncated>true</IsTruncated>" in xml_data
        if is_truncated:
            last_key = page_keys[-1]
        else:
            break
    except Exception as e:
        print("Error:", e)
        break

print(f"Total keys fetched: {len(keys)}")

search_terms = ["city", "street", "road", "outdoor", "town", "track", "highway", "rivermark"]
found = {term: [] for term in search_terms}

for key in keys:
    if key.endswith(".usd") and "thumbs" not in key.lower() and "payloads" not in key.lower() and "materials" not in key.lower() and "textures" not in key.lower():
        for term in search_terms:
            if term in key.lower():
                found[term].append(key)

for term, matches in found.items():
    print(f"\n--- Matches for '{term}' ({len(matches)}) ---")
    # print up to 50 matches
    for match in matches[:50]:
        print(match)
