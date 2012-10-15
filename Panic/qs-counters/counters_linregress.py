import csv
import numpy
import scipy.stats
import pylab

def linregress(X, Y, msg=''):
  result = scipy.stats.linregress(X, Y)
  print '[{0}] {1}'.format(msg, result)
  return result

def _normalized_text(X, Y, rx, ry, msg, **kwargs):
  pylab.text(
    min(X) * (1.0 - rx) + max(X) * rx,
    min(Y) * (1.0 - ry) + max(Y) * ry,
    msg,
    **kwargs)

def best_fit_equation_text(X, Y, m, b, r, p):
  _normalized_text(
    X, Y, 0.01, 0.05,
    r'$y = %.4f x + %.4f$' % (m, b),
    color=DARK_GREY)
  _normalized_text(
    X, Y, 0.01, 0.01,
    r'$(R, p) = (%.4f, %.4f)$' % (r, p),
    color=DARK_GREY)

def setup_plot(xlabel, ylabel, title):
  pylab.xlabel(xlabel)
  pylab.ylabel(ylabel)
  pylab.title(title)
  pylab.legend()
  pylab.grid(True, color=LIGHT_GREY, linestyle='-')

with open('counter-dump-normalized', 'r') as f:
  reader = csv.DictReader(f)
  L = filter(lambda row: row['alcohol'] and row['sweets'], list(reader))

RED = '#ff0000'
BLUE = '#0000ff'
MAGENTA = '#ff00ff'
DARK_GREY = '#666666'
GREY = '#999999'
LIGHT_GREY = '#d7d7d7'

X = numpy.array(range(len(L)))
Y1 = numpy.array(map(lambda row: int(row['alcohol']), L))
m1, b1, r1, p1, err1 = linregress(X, Y1, 'alcohol')

pylab.plot(X, Y1, color=RED, label='Raw Data')
pylab.plot(X, m1 * X + b1, color=GREY, label='Best Fit')
setup_plot('Time (days)', 'Drinks', 'Alcohol Consumption')
best_fit_equation_text(X, Y1, m1, b1, r1, p1)
pylab.savefig('qs-counters-alcohol.png')
pylab.close()

Y2 = numpy.array(map(lambda row: int(row['sweets']), L))
m2, b2, r2, p2, err2 = linregress(X, Y2, 'sweets')
pylab.plot(X, Y2, color=BLUE, label='Raw Data')
pylab.plot(X, m2 * X + b2, color=GREY, label='Best Fit')
setup_plot('Time (days)', 'Sweets', 'Sugar Consumption')
best_fit_equation_text(X, Y2, m2, b2, r2, p2)
pylab.savefig('qs-counters-sweets.png')
pylab.close()

pylab.plot(X, Y1, color=RED, label='Alcohol')
pylab.plot(X, Y2, color=BLUE, label='Sugar')
setup_plot('Time (days)', 'Amount', 'Alcohol and Sugar Consumption')
pylab.savefig('qs-counters-alcohol-and-sugar.png')
pylab.close()

Y = numpy.array(map(lambda row: int(row['exercise_raw']), L))
m, b, r, p, err = linregress(X, Y, 'exercise_raw')
pylab.plot(X, Y, color=BLUE, label='Raw Data')
pylab.plot(X, m * X + b, color=GREY, label='Best Fit')
setup_plot('Time (days)', 'Seconds', 'Amount of Exercise')
best_fit_equation_text(X, Y, m, b, r, p)
pylab.savefig('qs-counters-exercise-raw.png')
pylab.close()

m, b, r, p, err = linregress(Y1, Y2, 'alcohol vs. sweets')
X = numpy.arange(min(Y1), max(Y1) + 1)
pylab.plot(Y1, Y2, color=MAGENTA, marker='x', linestyle='None', label='Raw Data')
pylab.plot(X, m * X + b, color=GREY, label='Best Fit')
setup_plot('Drinks', 'Sweets', 'Alcohol vs. Sugar Consumption')
best_fit_equation_text(Y1, Y2, m, b, r, p)
pylab.savefig('qs-counters-alcohol-vs-sugar.png')
pylab.close()

m, b, r, p, err = linregress(Y1[:-1], Y1[1:], 'alcohol previous vs. current')
pylab.plot(Y1[:-1], Y1[1:], color=RED, marker='x', linestyle='None', label='Raw Data')
pylab.plot(X, m * X + b, color=GREY, label='Best Fit')
setup_plot('Drinks Yesterday', 'Drinks Today', 'Alcohol Consumption: Today vs. Yesterday')
best_fit_equation_text(Y1[:-1], Y1[1:], m, b, r, p)
pylab.savefig('qs-counters-alcohol-today-vs-yesterday.png')
pylab.close()
