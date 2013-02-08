import csv
import json
import sys
import os
import os.path
import urllib2

class SkipComments(object):
  def __init__(self, f):
    self._f = f
  def next(self):
    line = self._f.next()
    while line.startswith('#'):
      line = self._f.next()
    return line
  def __iter__(self):
    return self

SNPS_INDEX_PATH = '.snps-index'

if os.path.isfile(SNPS_INDEX_PATH):
  with open(SNPS_INDEX_PATH) as f:
    snps_index = json.loads(f.read())
else:
  snps_data = urllib2.urlopen('https://api.23andme.com/res/txt/snps.data')
  reader = csv.DictReader(SkipComments(snps_data), dialect='excel-tab')
  sys.stderr.write('building SNP index')
  snps_index = {}
  for i, row in enumerate(reader):
    snps_index[row['snp']] = int(row['index']) * 2
    if i % 10000 == 0:
      sys.stderr.write('.')
  sys.stderr.write('done.\n')
  with open(SNPS_INDEX_PATH, 'w') as f:
    json.dump(snps_index, f)

data = json.loads(sys.stdin.read())
for snp in sys.argv[1:]:
  pos = snps_index.get(snp)
  if pos is None:
    continue
  bases = data['genome'][pos:pos+2]
  print '\t'.join([snp, bases])
