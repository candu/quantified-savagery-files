import httplib
import urllib
import time
import json

class InstamapperTailer(object):
  API_HOST = 'www.instamapper.com'

  def __init__(self, key, freq=15):
    self._key = key
    self._freq = freq
    self._since = int(time.time())

  def _poll(self):
    params = {
      'action': 'getPositions',
      'key': self._key,
      'num': 10,
      'from_ts': self._since,
      'format': 'json',
    }
    url = 'http://{0}/api?{1}'.format(self.API_HOST, urllib.urlencode(params))
    conn = httplib.HTTPConnection(self.API_HOST)
    conn.request('GET', url)
    resp = conn.getresponse()
    if resp.status != 200:
      raise Exception('HTTP {0} {1}'.format(resp.status, resp.reason))
    data = json.loads(resp.read())
    conn.close()
    return data['positions']

  def _maybeSleep(self):
    elapsed = time.time() - self._since
    wait = self._freq - elapsed
    if wait <= 0:
      return
    time.sleep(wait)

  def run(self):
    while True:
      self._maybeSleep()
      positions = self._poll()
      if not positions:
        continue
      for p in positions:
        print '({0}, {1}, {2}) @ {3}'.format(
          p['latitude'],
          p['longitude'],
          p['altitude'],
          p['timestamp'])
      self._since = positions[-1]['timestamp'] + 1

if __name__ == '__main__':
  import sys
  tailer = InstamapperTailer(sys.argv[1])
  tailer.run()
