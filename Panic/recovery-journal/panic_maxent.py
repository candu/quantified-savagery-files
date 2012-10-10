import csv
from nltk.classify.maxent import MaxentClassifier

def dateMap(L):
  return dict((row['date'], row) for row in L)

with open('exercise-record', 'r') as f:
  reader = csv.DictReader(f)
  E = dateMap(reader)

with open('food-diary', 'r') as f:
  reader = csv.DictReader(f)
  F = dateMap(reader)

with open('panic-log', 'r') as f:
  reader = csv.DictReader(f)
  P = dateMap(reader)

with open('weekly-practice-record', 'r') as f:
  reader = csv.DictReader(f)
  W = dateMap(reader)

train_set = []
dates = set(W).intersection(F)
for ds in dates:
  try:
    ds_data = {
      'relaxation' : bool(int(W[ds]['relaxation'])),
      'exercise' : bool(int(W[ds]['exercise'])),
      'caffeine' : int(F[ds]['caffeine']) > 0,
      'sweets' : int(F[ds]['sweets']) > 1,
      'alcohol' : int(F[ds]['alcohol']) > 4,
      'supplements' : bool(int(F[ds]['supplements']))
    }
  except (ValueError, KeyError):
    continue
  had_panic = P.get(ds) and 'panic' or 'no-panic'
  train_set.append((ds_data, had_panic))

classifier = MaxentClassifier.train(
  train_set,
  algorithm='IIS',
  max_iter=100,
  min_lldelta=0.0001)
classifier.show_most_informative_features()
