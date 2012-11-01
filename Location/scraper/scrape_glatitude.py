import httplib2
import urllib
import time
import datetime
import json
from glatitude import auth

class GoogleLatitudeScraper(object):
  def __init__(self, key, secret):
    self._credentials = auth(key, secret)

  def _poll(self, since, until):
    http = httplib2.Http()
    self._credentials.authorize(http)
    url = 'https://www.googleapis.com/latitude/v1/location?%s' % urllib.urlencode({
      'min-time': since,
      'max-time': until,
      'granularity': 'best'
    })
    resp, content = http.request(url)
    data = json.loads(content)
    if data.get('error') is not None:
      print content
      return None
    return data['data'].get('items', [])

  def _datetimeToTimestampMs(self, dt):
    return int(time.mktime(dt.timetuple()) * 1000)

  def scrape(self, since, until=datetime.datetime.now()):
    since = self._datetimeToTimestampMs(since)
    until = self._datetimeToTimestampMs(until)
    cur = until
    while cur >= since:
      time.sleep(1)
      positions = self._poll(since, cur)
      if positions is None:
        continue
      if not positions:
        break
      for position in positions:
        print json.dumps(position)
      cur = int(positions[-1]['timestampMs']) - 1

if __name__ == '__main__':
  import sys
  import gflags
  FLAGS = gflags.FLAGS
  gflags.DEFINE_string('key', None, 'OAuth client ID')
  gflags.DEFINE_string('secret', None, 'OAuth secret')
  gflags.MarkFlagAsRequired('key')
  gflags.MarkFlagAsRequired('secret')
  try:
    sys.argv = FLAGS(sys.argv)
  except gflags.FlagsError, e:
    print '''\
%s

Usage: %s ARGS
%s''' % (e, sys.argv[0], FLAGS)
    sys.exit(1)
  scraper = GoogleLatitudeScraper(FLAGS.key, FLAGS.secret)
  scraper.scrape(datetime.datetime.fromtimestamp(0), datetime.datetime.now())
