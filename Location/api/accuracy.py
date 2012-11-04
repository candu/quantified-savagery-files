import json
import operator
import pylab
import sys

from stats import histogram
from pylabutils import setupPlot

prev = None
A = []
for line in sys.stdin:
  data = json.loads(line)
  acc = data.get('accuracy')
  if acc:
    A.append(min(999, acc))
w = 10.0
XY = histogram(A, w)
X = map(operator.itemgetter(0), XY)
Y = map(operator.itemgetter(1), XY)
pylab.bar(X, Y, width=w)
setupPlot(
  'Accuracy (m)',
  'Frequency',
  'Accuracy Radius'
)
pylab.savefig('accuracy-histogram.png')
