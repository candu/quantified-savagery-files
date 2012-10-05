import csv
import sys
import datetime
import json

dt = datetime.datetime.now()
stats = {}
min_date, max_date = '9999-12-31', '0001-01-01'
last_pressed = None
for row in csv.reader(sys.stdin):
  cid, cname, ctype, ts, pressed = (
    int(row[0]),
    row[1],
    row[2],
    dt.strptime(row[3], '%Y-%m-%d %H:%M:%S.%f'),
    bool(int(row[4]))
  )
  date = ts.strftime('%Y-%m-%d')
  min_date = min(min_date, date)
  max_date = max(max_date, date)
  value = stats.setdefault(cname, {}).setdefault(date, 0)
  if ctype == 'count':
    value += 1
    stats[cname][date] = value
  elif pressed:
    last_pressed = ts
  else:
    delta = ts - last_pressed
    value += delta.seconds
    stats[cname][date] = value
cur_date = dt.strptime(min_date, '%Y-%m-%d')
max_date = dt.strptime(max_date, '%Y-%m-%d')
while cur_date <= max_date:
  cur_date_str = cur_date.strftime('%Y-%m-%d')
  date_stats = dict((cname, stats[cname].get(cur_date_str, 0)) for cname in stats)
  """
  for cname in stats:
    date_stats[cname] = stats[cname].get(cur_date_str, 0)
  """
  print json.dumps({
    'date': cur_date_str,
    'stats': date_stats
  })
  cur_date += datetime.timedelta(days=1)
