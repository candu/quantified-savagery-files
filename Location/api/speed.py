import json
import sys

with_speed, total = 0, 0
for line in sys.stdin:
  data = json.loads(line)
  if 'speed' in data:
    with_speed += 1
  total += 1
print 'found {0} speed values among {1} readings'.format(with_speed, total)
