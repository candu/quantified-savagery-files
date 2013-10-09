import json
import math
import pylab
import sys

from location import Location
from pylabutils import RED, setupPlot

prev, X, Y = None, [], []
for line in sys.stdin:
  data = json.loads(line)
  cur = (
    int(data['timestampMs']) / 1000,
    Location(data['latitude'], data['longitude'])
  )
  if prev is not None:
    acc = data.get('accuracy')
    if acc is None:
      continue
    dx = prev[1].dist(cur[1])
    dt = cur[0] - prev[0]
    X.append(dx / dt)
    Y.append(acc)
  prev = cur
pylab.plot(X, Y, color=RED, linestyle='None', marker='o')
setupPlot(
  'Speed (m/s)',
  'Accuracy (m)',
  'Accuracy vs. Speed'
)
pylab.savefig('accuracy-vs-speed.png')
