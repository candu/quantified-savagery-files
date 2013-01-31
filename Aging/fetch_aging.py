import json
import sys
import urllib2

data = json.loads(sys.stdin.read())
images = data[0]['sequences'][0]['images']
for image in images:
  url = urllib2.urlopen(image['uri'])
  path = 'age{0}.jpg'.format(image['age'])
  with open(path, 'w') as f:
    f.write(url.read())
