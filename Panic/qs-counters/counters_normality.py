import csv
import math
import numpy
import pylab
import scipy.stats

def _normalized_text(X, Y, rx, ry, msg, **kwargs):
  pylab.text(
    min(X) * (1.0 - rx) + max(X) * rx,
    min(Y) * (1.0 - ry) + max(Y) * ry,
    msg,
    **kwargs)

def normal_fit_equation_text(X, Y, mu, std):
  _normalized_text(
    X, Y, 0.01, 0.01,
    r'$(\mu, \sigma^2) = (%.4f, %.4f)$' % (mu, std * std),
    color=DARK_GREY)

def histogram(L):
  d = {}
  for x in L:
    if x not in d:
      d[x] = 0
    d[x] += 1
  return sorted(d.iteritems())

def normal_fit(L, res=100):
  mu, std = numpy.mean(L), numpy.std(L)
  N, xmin, xmax = len(L), min(L), max(L)
  X = numpy.arange(xmin, xmax, 1.0 * (xmax - xmin) / res)
  def pdf(x):
    f = N / (std * math.sqrt(2.0 * math.pi))
    k = (x - mu) / std
    return f * math.exp(-k * k / 2.0)
  return X, map(pdf, X), mu, std

def setup_plot(xlabel, ylabel, title):
  pylab.xlabel(xlabel)
  pylab.ylabel(ylabel)
  pylab.title(title)
  pylab.legend()
  pylab.grid(True, color=LIGHT_GREY, linestyle='-')

with open('recovery-dump-normalized', 'r') as f:
  reader = csv.DictReader(f)
  recovery_journal_dataset = list(reader)

with open('counter-dump-normalized', 'r') as f:
  reader = csv.DictReader(f)
  qs_counters_dataset = list(reader)

RED = '#ff0000'
BLUE = '#0000ff'
MAGENTA = '#ff00ff'
DARK_GREY = '#666666'
GREY = '#999999'
LIGHT_GREY = '#d7d7d7'

alcohol_A = map(lambda row: float(row['alcohol']), recovery_journal_dataset[:31])
hist_A = histogram(alcohol_A)
X = map(lambda h: h[0], hist_A)
Y = map(lambda h: h[1], hist_A)
pylab.plot(X, Y, color=RED, label='Histogram Data')
NX, NY, mu, std = normal_fit(alcohol_A)
pylab.plot(NX, NY, color=GREY, label='Normal Fit')
setup_plot('Drinks', 'Frequency', 'Alcohol Histogram (recovery-journal)')
normal_fit_equation_text(NX, NY, mu, std)
pylab.savefig('recovery-journal-alcohol-histogram.png')
pylab.close()

alcohol_B = map(lambda row: float(row['alcohol']), qs_counters_dataset)
hist_B = histogram(alcohol_B)
X = map(lambda h: h[0], hist_B)
Y = map(lambda h: h[1], hist_B)
pylab.plot(X, Y, color=RED, label='Histogram Data')
NX, NY, mu, std = normal_fit(alcohol_B)
pylab.plot(NX, NY, color=GREY, label='Normal Fit')
setup_plot('Drinks', 'Frequency', 'Alcohol Histogram (qs-counters)')
normal_fit_equation_text(NX, NY, mu, std)
pylab.savefig('qs-counters-alcohol-histogram.png')
pylab.close()

print 'alcohol, recovery-journal: ', scipy.stats.shapiro(alcohol_A)
print 'alcohol, qs-counters: ', scipy.stats.shapiro(alcohol_B)

sweets_A = map(lambda row: float(row['sweets']), recovery_journal_dataset[:31])
hist_A = histogram(sweets_A)
X = map(lambda h: h[0], hist_A)
Y = map(lambda h: h[1], hist_A)
pylab.plot(X, Y, color=BLUE, label='Histogram Data')
NX, NY, mu, std = normal_fit(sweets_A)
pylab.plot(NX, NY, color=GREY, label='Normal Fit')
setup_plot('Sweets', 'Frequency', 'Sugar Histogram (recovery-journal)')
normal_fit_equation_text(NX, NY, mu, std)
pylab.savefig('recovery-journal-sweets-histogram.png')
pylab.close()

sweets_B = map(lambda row: float(row['sweets']), qs_counters_dataset)
hist_B = histogram(sweets_B)
X = map(lambda h: h[0], hist_B)
Y = map(lambda h: h[1], hist_B)
pylab.plot(X, Y, color=BLUE, label='Histogram Data')
NX, NY, mu, std = normal_fit(sweets_B)
pylab.plot(NX, NY, color=GREY, label='Normal Fit')
setup_plot('Sweets', 'Frequency', 'Sugar Histogram (qs-counters)')
normal_fit_equation_text(NX, NY, mu, std)
pylab.savefig('qs-counters-sweets-histogram.png')
pylab.close()

print 'sugar, recovery-journal: ', scipy.stats.shapiro(sweets_A)
print 'sugar, qs-counters: ', scipy.stats.shapiro(sweets_B)
