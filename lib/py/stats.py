import math

class RollingMeanVar(object):
  """
  Constant-time online rolling exponential mean/variance implementation.
  """
  def __init__(self, alpha):
    self._alpha = alpha
    self._prev = float('-inf')
    self._mean = 0.0
    self._var = 0.0

  def update(self, x, t):
    assert t > self._prev
    beta = math.pow(1.0 - self._alpha, t - self._prev)
    # TODO: different strategies for alpha (sparse vs. dense)
    delta = self._alpha * x - (1.0 - beta) * self._mean
    self._mean += delta
    self._var = \
      beta * (self._var + delta * delta) + \
      (1.0 - (self._alpha + beta)) * self._mean * self._mean + \
      self._alpha * (x - self._mean) * (x - self._mean)
    self._prev = t

  def mean(self):
    return self._mean

  def var(self):
    return max(self._var, 0.0)

  def std(self):
    return math.sqrt(self.var())

  def z(self, x):
    std = self.std()
    if std == 0:
      return 0
    return (x - self._mean) / std

def histogram(L, w=1):
  """
  Given a list of values, computes a sorted list

  [(x_1, freq_1), ..., (x_n, freq_n)]

  of value-frequency pairs. The values are bucketed into buckets of
  width w.
  """
  d = {}
  for x in L:
    xb = int(math.floor(x / w)) * w
    if xb not in d:
      d[xb] = 0
    d[xb] += 1
  return sorted(d.iteritems())
