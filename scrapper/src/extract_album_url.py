import xml.etree.ElementTree as ET
root = ET.parse('../../data/albums-1.xml').getroot()

i = 0
for child in root:
    i += 1
    print(child[0].text)

print(i)