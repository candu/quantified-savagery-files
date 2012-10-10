import csv
import numpy
import scipy.fftpack
import pylab

def getFFTFrequencyStrengths(X, dt=1.0):
  F = scipy.fftpack.fft(X)
  Q = scipy.fftpack.fftfreq(F.size)
  return map(numpy.abs, F), Q

with open('food-diary', 'r') as f:
  reader = csv.DictReader(f)
  L = list(reader)[:31]

X = map(lambda row: int(row['alcohol']), L)
F, Q = getFFTFrequencyStrengths(X)
pylab.plot(Q, F, 'o')
pylab.show()

pylab.plot(1.0 / Q, F, 'o')
pylab.show()
