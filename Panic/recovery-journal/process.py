import csv
import sys

def dateMap(L):
  return dict((row['date'], row) for row in L)

with open('food-diary', 'r') as f:
  reader = csv.DictReader(f)
  F = dateMap(reader)

with open('weekly-practice-record', 'r') as f:
  reader = csv.DictReader(f)
  W = dateMap(reader)

writer = csv.DictWriter(sys.stdout, [
  'date',
  'caffeine',
  'sweets',
  'alcohol',
  'relaxation',
  'exercise'
])
writer.writeheader()
dates = sorted(set(W).intersection(F))
for ds in dates:
  try:
    writer.writerow({
      'date': ds,
      'caffeine': int(F[ds]['caffeine']),
      'sweets': int(F[ds]['sweets']),
      'alcohol': int(F[ds]['alcohol']),
      'relaxation': int(W[ds]['relaxation']),
      'exercise': int(W[ds]['exercise'])
    })
  except (ValueError, KeyError):
    continue
