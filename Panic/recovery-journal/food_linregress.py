import csv
import numpy
import scipy.stats
import pylab

def linregress(X, Y, msg=''):
  result = scipy.stats.linregress(X, Y)
  print '[{0}] {1}'.format(msg, result)
  return result

with open('food-diary', 'r') as f:
  reader = csv.DictReader(f)
  L = filter(lambda row: row['alcohol'] and row['sweets'], list(reader))
X = numpy.array(range(len(L)))

Y1 = numpy.array(map(lambda row: int(row['alcohol']), L))
m1, b1, r1, p1, err1 = linregress(X, Y1, 'alcohol')
pylab.plot(X, Y1)
pylab.plot(X, m1 * X + b1)
pylab.show()

Y2 = numpy.array(map(lambda row: int(row['sweets']), L))
m2, b2, r2, p2, err2 = linregress(X, Y2, 'sweets')
pylab.plot(X, Y2)
pylab.plot(X, m2 * X + b2)
pylab.show()

pylab.plot(X, Y1)
pylab.plot(X, Y2)
pylab.show()

m, b, r, p, err = linregress(Y1, Y2, 'alcohol vs. sweets')
X = numpy.arange(min(Y1), max(Y1) + 1)
pylab.plot(Y1, Y2, 'x')
pylab.plot(X, m * X + b)
pylab.show()

m, b, r, p, err = linregress(Y1[:-1], Y1[1:], 'alcohol previous vs. current')
pylab.plot(Y1[:-1], Y1[1:], 'x')
pylab.plot(X, m * X + b)
pylab.show()
