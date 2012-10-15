import csv
from nltk.classify.maxent import MaxentClassifier

def dateMap(L):
  return dict((row['date'], row) for row in L)

with open('counter-dump-normalized', 'r') as f:
  reader = csv.DictReader(f)
  W = dateMap(reader)

train_set = []
dates = set(W)
for ds in dates:
  try:
    ds_data = {}
    if bool(int(W[ds]['relaxation'])):
      ds_data['relaxation'] = True
    if int(W[ds]['caffeine']) > 0:
      ds_data['caffeine'] = True
    if int(W[ds]['sweets']) > 1:
      ds_data['sweets'] = True
    if int(W[ds]['alcohol']) > 4:
      ds_data['alcohol'] = True
  except (ValueError, KeyError):
    continue
  exercised = bool(int(W[ds]['exercise'])) and 'exercise' or 'no-exercise'
  train_set.append((ds_data, exercised))

classifier = MaxentClassifier.train(
  train_set,
  algorithm='IIS',
  max_iter=100,
  min_lldelta=0.0001)
classifier.show_most_informative_features()
