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
    print(f"Total keys found: {len(keys)}")
    print("\nFirst 100 keys:")
    for key in keys[:100]:
        print(key)

except Exception as e:
    print("Error:", e)
