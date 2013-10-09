import math

class Location(object):
  # Earth's radius, in meters
  R = 6371009

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
