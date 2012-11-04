import httplib2
import urllib
import time
import datetime
import json
from glatitude import auth

class GoogleLatitudeScraper(object):
  def __init__(self, key, secret):
    self._credentials = auth(key, secret)

  def _poll(self, until):
    http = httplib2.Http()
    self._credentials.authorize(http)
    url = 'https://www.googleapis.com/latitude/v1/location?%s' % urllib.urlencode({
      'fields': 'items(latitude,longitude,accuracy,speed,timestampMs)',
      'max-results': 1000,
      'granularity': 'best',
      'max-time': until
    })
    resp, content = http.request(url)
    data = json.loads(content)
    if data.get('error') is not None:
      print content
      return None
    return data['data'].get('items', [])

  def scrape(self):
    cur = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
    while True:
      positions = self._poll(cur)
      if not positions:
        break
      for position in positions:
        print json.dumps(position)
      cur = int(positions[-1]['timestampMs']) - 1
      time.sleep(2)

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
  scraper.scrape()
