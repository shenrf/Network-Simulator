import json;
from link import Link
jsonobject = json.load(file('testcase0.json'))  
print jsonobject['links'][0]['id']
