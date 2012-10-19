import json
import sys
import numpy
import scipy.stats
import pylab

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

data = json.loads(sys.stdin.read())

RED = '#ff0000'
GREEN = '#00ff00'
BLUE = '#0000ff'
DARK_GREY = '#666666'
GREY = '#999999'
LIGHT_GREY = '#d7d7d7'

X = map(lambda P: P[0], data['Sleep Quality'])
Y = map(lambda P: P[1], data['Sleep Quality'])
m, b, r, p, err = scipy.stats.linregress(X, Y)
pylab.plot(X, Y, color=BLUE, marker='o', linestyle='None', label='Raw Data')
LX = numpy.arange(0, 100)
pylab.plot(LX, m * LX + b, color=GREY, label='Best Fit')
setup_plot('Sleep Quality', 'Happiness', 'Sleep Quality')
best_fit_equation_text(LX, LX, m, b, r, p)
pylab.axis([0, 100, 0, 100])
pylab.savefig('happiness-sleep-quality.png')
pylab.close()

X = map(lambda P: P[0], data['Productivity'])
Y = map(lambda P: P[1], data['Productivity'])
m, b, r, p, err = scipy.stats.linregress(X, Y)
pylab.plot(X, Y, color=RED, marker='o', linestyle='None', label='Raw Data')
LX = numpy.arange(0, 100)
pylab.plot(LX, m * LX + b, color=GREY, label='Best Fit')
setup_plot('Productivity', 'Happiness', 'Productivity')
best_fit_equation_text(LX, LX, m, b, r, p)
pylab.axis([0, 100, 0, 100])
pylab.savefig('happiness-productivity.png')
pylab.close()

X = map(lambda P: P[0], data['Focused'])
Y = map(lambda P: P[1], data['Focused'])
m, b, r, p, err = scipy.stats.linregress(X, Y)
pylab.plot(X, Y, color=GREEN, marker='o', linestyle='None', label='Raw Data')
LX = numpy.arange(0, 100)
pylab.plot(LX, m * LX + b, color=GREY, label='Best Fit')
setup_plot('Focus', 'Happiness', 'Focus')
best_fit_equation_text(LX, LX, m, b, r, p)
pylab.axis([0, 100, 0, 100])
pylab.savefig('happiness-focus.png')
pylab.close()
