from lxml import etree
import sys
import dateutil.parser
import time
import json
import math
import pylab

class Location(object):
  R = 6371009   # meters

  def __init__(self, lat, lng):
    self.lat = lat
    self.lng = lng

  def __str__(self):
    return '<Location ({0}, {1})>'.format(self.lat, self.lng)

  def dist(self, other):
    """
    Distance (in meters) between two Locations. Uses the Haversine formula.

    See http://www.movable-type.co.uk/scripts/latlong.html for corresponding
    JavaScript implementation.
    """
    dLat = math.radians(other.lat - self.lat)
    dLon = math.radians(other.lng - self.lng)
    lat1 = math.radians(self.lat)
    lat2 = math.radians(other.lat)
    sLat = math.sin(dLat / 2.0)
    sLon = math.sin(dLon / 2.0)
    a = sLat * sLat + sLon * sLon * math.cos(lat1) * math.cos(lat2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return self.R * c

  def bearing(self, other):
    """
    Bearing (in degrees) between two Locations. Uses the great circle initial
    bearing.

    See http://www.movable-type.co.uk/scripts/latlong.html for corresponding
    JavaScript implementation.
    """
    dLat = math.radians(other.lat - self.lat)
    dLon = math.radians(other.lng - self.lng)
    lat1 = math.radians(self.lat)
    lat2 = math.radians(other.lat)
    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
    return math.degrees(math.atan2(y, x))

def getRawLocations(f):
  root = etree.parse(f).getroot()
  document = root.getchildren()[-1]
  placemark = document.getchildren()[-1]
  track = placemark.getchildren()[-1]
  when = None
  for child in track.iterchildren():
    if child.tag.endswith('altitudeMode'):
      continue
    if child.tag.endswith('when'):
      ts = dateutil.parser.parse(child.text)
      when = int(time.mktime(ts.timetuple()))
    else:
      coords = map(float, child.text.split())
      yield (when, Location(coords[0], coords[1]))

class RollingMeanVar(object):
  """
  Constant-time online rolling exponential mean/variance implementation.
  """
  def __init__(self, alpha):
    self._alpha = alpha
    self._prev = float('-inf')
    self._mean = 0.0
    self._var = 0.0

  def update(self, x, t):
    assert t > self._prev
    beta = math.pow(1.0 - self._alpha, t - self._prev)
    alpha = 1.0 - beta
    delta = alpha * x - (1.0 - beta) * self._mean
    self._mean += delta
    self._var = \
      beta * (self._var + delta * delta) + \
      (1.0 - (alpha + beta)) * self._mean * self._mean + \
      alpha * (x - self._mean) * (x - self._mean)
    self._prev = t

  def mean(self):
    return self._mean

  def var(self):
    return max(self._var, 0.0)

  def std(self):
    return math.sqrt(self.var())

  def z(self, x):
    std = self.std()
    if std == 0:
      return 0
    return (x - self._mean) / std

def filterLocations(f):
  prev = None
  Q = RollingMeanVar(1 - math.pow(1 - 0.15, 1 / 60.0))
  for cur in getRawLocations(f):
    if prev is not None:
      yield cur[0] - prev[0]
      """
      v = prev[1].dist(cur[1]) / (cur[0] - prev[0])
      if v > 100.0:
        continue
      if abs(Q.z(v)) >= 10 and Q.std() >= 0.25:
        continue
      Q.update(v, cur[0])
      yield cur
      """
    prev = cur

dts = list(filterLocations(sys.stdin))

t, mu = 0, 0
Y = []
k = 0.001
for dt in dts:
  t += 1
  mu += k * (dt - mu)
  Y.append(mu)
  if t % 1000 == 0:
    print Y[-1]
pylab.plot(range(len(Y)), Y, color="#ff0000")
pylab.show()

d = {}
for dt in dts:
  mdt = dt % 60
  if mdt not in d:
    d[mdt] = 0
  d[mdt] += 1
X, Y = [], []
for x, y in sorted(d.iteritems()):
  X.append(x)
  Y.append(y)
pylab.plot(X, Y, color="#0000ff", linestyle='None', marker='o')
pylab.show()
