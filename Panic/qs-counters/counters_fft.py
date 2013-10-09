import csv
import math
import numpy
import scipy.fftpack
import pylab

def setup_plot(xlabel, ylabel, title):
  pylab.xlabel(xlabel)
  pylab.ylabel(ylabel)
  pylab.title(title)
  pylab.grid(True, color=LIGHT_GREY, linestyle='-')

with open('counter-dump-normalized', 'r') as f:
  reader = csv.DictReader(f)
  L = list(reader)

RED = '#ff0000'
LIGHT_GREY = '#d7d7d7'

X = map(lambda row: int(row['alcohol']), L)
F = scipy.fftpack.fft(X)
N = F.size
Q = scipy.fftpack.fftfreq(N)
FS = map(numpy.abs, F / math.sqrt(N))
FP = map(lambda z: math.atan2(z.imag, z.real), F)
pylab.plot(Q, FS, color=RED, marker='o', linestyle='None')
setup_plot('Frequency (1/days)', 'Amplitude', 'Frequency Strengths')
pylab.savefig('qs-counters-fft-frequencies.png')
pylab.close()

for strength, phase, period in sorted(zip(FS, FP, 1.0 / Q))[-5:]:
  phase_days = period * (phase / (2.0 * math.pi))
  print '[%.2f days] %.4f (phase=%.2f days)' % (period, strength, phase_days)
