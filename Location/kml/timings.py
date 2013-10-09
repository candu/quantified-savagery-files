import dateutil.parser
from lxml import etree
import operator
import pylab
import sys
import time

from stats import RollingMeanVar, histogram
from pylabutils import RED, BLUE, setupPlot

root = etree.parse(sys.stdin).getroot()
document = root.getchildren()[-1]
placemark = document.getchildren()[-1]
track = placemark.getchildren()[-1]
dts = []
prev_when = None
for child in track.iterchildren():
  if child.tag.endswith('when'):
    ts = dateutil.parser.parse(child.text)
    when = int(time.mktime(ts.timetuple()))
    if prev_when is not None:
      dts.append(when - prev_when)
    prev_when = when

rmv = RollingMeanVar(0.001)
Y = []
for i, dt in enumerate(dts):
  rmv.update(dt, i)
  Y.append(rmv.mean())
pylab.plot(range(len(Y)), Y, color=RED)
setupPlot(
  'Sample Index',
  'Interval (s)',
  'Polling Interval - Rolling Average'
)
pylab.savefig('timings-frequency.png')
pylab.close()

Y = map(operator.itemgetter(1), histogram(dt % 60 for dt in dts))
pylab.bar(range(len(Y)), Y, width=1.0)
setupPlot(
  'Interval (s, mod 60)',
  'Frequency',
  'Polling Interval - Seconds mod 60'
)
pylab.savefig('timings-second-histogram.png')
pylab.close()
