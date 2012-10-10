import csv
import math
import numpy
import scipy.fftpack
import pylab

def getFFTFrequencyStrengths(X, dt=1.0):
  F = scipy.fftpack.fft(X)
  N = F.size
  Q = scipy.fftpack.fftfreq(N)
  return map(numpy.abs, F / math.sqrt(N)), Q

def setup_plot(xlabel, ylabel, title):
  pylab.xlabel(xlabel)
  pylab.ylabel(ylabel)
  pylab.title(title)
  pylab.grid(True, color=LIGHT_GREY, linestyle='-')

with open('food-diary', 'r') as f:
  reader = csv.DictReader(f)
  L = list(reader)[:31]

RED = '#ff0000'
LIGHT_GREY = '#d7d7d7'

X = map(lambda row: int(row['alcohol']), L)
F, Q = getFFTFrequencyStrengths(X)
pylab.plot(Q, F, color=RED, marker='o', linestyle='None')
setup_plot('Frequency (1/days)', 'Amplitude', 'Frequency Strengths')
pylab.savefig('fft-frequencies.png')
pylab.close()

for f, p in sorted(zip(F, 1.0 / Q))[-5:]:
  print '[%.2f days] %.4f' % (p, f)
