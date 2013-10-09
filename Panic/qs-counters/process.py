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
writer = csv.DictWriter(sys.stdout, [
  'date',
  'caffeine',
  'sweets',
  'alcohol',
  'relaxation',
  'relaxation_raw',
  'exercise',
  'exercise_raw'
])
writer.writeheader()
while cur_date <= max_date:
  cur_date_str = cur_date.strftime('%Y-%m-%d')
  date_stats = dict((cname, stats[cname].get(cur_date_str, 0)) for cname in stats)
  writer.writerow({
    'date': cur_date_str,
    'caffeine': date_stats['caffeine'],
    'sweets': date_stats['sweets'],
    'alcohol': date_stats['alcohol'],
    'relaxation': int(date_stats['relaxation'] >= 300),
    'relaxation_raw': date_stats['relaxation'],
    'exercise': int(date_stats['exercise'] >= 1800),
    'exercise_raw': date_stats['exercise']
  })
  cur_date += datetime.timedelta(days=1)
