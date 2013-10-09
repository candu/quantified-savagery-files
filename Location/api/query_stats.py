import sys
import json
import datetime

raw = sys.stdin.read()
print 'Response size: {0} B'.format(len(raw))
data = json.loads(raw)
error = data.get('error')
if error:
  print 'Error: {0}'.format(json.dumps(error))
  sys.exit(1)
items = data['data'].get('items', [])
print 'Number of items: {0}'.format(len(items))
acc_count = sum(int(bool(item.get('accuracy'))) for item in items)
spd_count = sum(int(bool(item.get('speed'))) for item in items)
print 'Items with accuracy: {0}'.format(acc_count)
print 'Items with speed: {0}'.format(spd_count)
tss = [int(item['timestampMs']) for item in items]
min_ts = min(tss)
min_dt = datetime.datetime.fromtimestamp(min_ts / 1000.0)
max_ts = max(tss)
max_dt = datetime.datetime.fromtimestamp(max_ts / 1000.0)
print 'Earliest item: {0} [{1}]'.format(min_dt, min_ts)
print 'Latest item: {0} [{1}]'.format(max_dt, max_ts)
