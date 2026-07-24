import urllib.request
import xml.etree.ElementTree as ET

url = 'https://omniverse-content-production.s3-us-west-2.amazonaws.com/?prefix=Assets/Isaac/5.1/Isaac/Environments/'
response = urllib.request.urlopen(url)
xml_data = response.read()
root = ET.fromstring(xml_data)

ns = {'s3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
for obj in root.findall('s3:Contents', ns):
    key = obj.find('s3:Key', ns).text
    if key.endswith('.usd'):
        print(key)
