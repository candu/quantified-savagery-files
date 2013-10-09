import httplib2
import urllib
import time
import json
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run

class GoogleLatitudeTailer(object):
  def __init__(self, key, secret, freq=15):
    self._flow = OAuth2WebServerFlow(
      client_id=key,
      client_secret=secret,
      scope='https://www.googleapis.com/auth/latitude.all.best',
      redirect_uri='http://localhost:8080/oauth2callback'
    )
    self._storage = Storage('creds_glatitude')
    self._credentials = run(self._flow, self._storage)
    self._freq = freq
    self._since = int(time.time() * 1000)

  def _poll(self):
    http = httplib2.Http()
    self._credentials.authorize(http)
    url = 'https://www.googleapis.com/latitude/v1/location?%s' % urllib.urlencode({
      'max-results': 10,
      'min-time': self._since,
      'max-time': self._since + 10 * (self._freq * 1000),
      'granularity': 'best'
    })
    resp, content = http.request(url)
    data = json.loads(content)
    if data.get('error') is not None:
      return None
    return data['data'].get('items', [])

  def _maybeSleep(self):
    elapsed = time.time() - self._since / 1000.0
    wait = self._freq - elapsed
    if wait <= 0:
      return
    time.sleep(wait)

  def run(self):
    while True:
      self._maybeSleep()
      positions = self._poll()
      if not positions:
        self._since += 10 * (self._freq * 1000)
        continue
      for p in positions:
        p['timestampMs'] = int(p['timestampMs'])
        print '({0}, {1}, {2}) @ {3}'.format(
          p['latitude'],
          p['longitude'],
          p.get('altitude', '[altitude unknown]'),
          p['timestampMs'] / 1000)
      self._since = positions[-1]['timestampMs'] + 1


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
  tailer = GoogleLatitudeTailer(FLAGS.key, FLAGS.secret)
  tailer.run()
