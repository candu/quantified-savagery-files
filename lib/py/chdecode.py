"""
chdecode.py - simple decoder for Google Charts API chd values

This allows you to extract your data from tools that only display it via the
Google Charts API.
"""

import unittest

def _clamp(x, xmin, xmax):
  if x < xmin:
    return None
  return min(x, xmax)

def _get_text_value(s):
  if s == '_':
    return None
  return float(s)

def _decode_series(s, xminmax=None):
  xs = map(_get_text_value, s.split(','))
  if xminmax is None:
    return xs
  xmin, xmax = xminmax
  return map(lambda x: _clamp(x, xmin, xmax), xs)

def _decode_text(chd, chds=None):
  ss = chd[2:].split('|')
  if chds is None:
    return [_decode_series(s, (0, 100)) for s in ss]
  if chds == 'a':
    return [_decode_series(s) for s in ss]
  limits = map(float, chds.split(','))
  xminmaxs = [limits[i:i+2] for i in range(0, len(limits), 2)]
  missing = len(ss) - len(xminmaxs)
  if missing > 0:
    xminmaxs += [xminmaxs[-1]] * missing
  return [_decode_series(s, xminmax) for s, xminmax in zip(ss, xminmaxs)]

def _get_simple_value(c):
  if c == '_':
    return None
  if 'A' <= c <= 'Z':
    return ord(c) - ord('A')
  if 'a' <= c <= 'z':
    return 26 + ord(c) - ord('a')
  if '0' <= c <= '9':
    return 52 + ord(c) - ord('0')
  raise ValueError('invalid character for simple encoding: {0}'.format(c))

def _decode_simple(chd):
  return [map(_get_simple_value, s) for s in chd[2:].split(',')]

def _get_extended_single_char_value(c):
  if c == '_':
    return None
  if 'A' <= c <= 'Z':
    return ord(c) - ord('A')
  if 'a' <= c <= 'z':
    return 26 + ord(c) - ord('a')
  if '0' <= c <= '9':
    return 52 + ord(c) - ord('0')
  if c == '-':
    return 62
  if c == '.':
    return 63
  raise ValueError('invalid character for simple encoding: {0}'.format(c))

def _get_extended_value(cc):
  x1 = _get_extended_single_char_value(cc[0])
  x2 = _get_extended_single_char_value(cc[1])
  if x1 is None or x2 is None:
    if not (x1 is None and x2 is None):
      raise ValueError('invalid characters for extended encoding: {0}'.format(cc))
    return None
  return (x1 << 6) | x2

def _decode_extended_series(s):
  return [_get_extended_value(s[i:i+2]) for i in range(0, len(s), 2)]

def _decode_extended(chd):
  return [_decode_extended_series(s) for s in chd[2:].split(',')]

def chdecode(chd, chds=None):
  if chd.startswith('t:'):
    return _decode_text(chd, chds)
  if chds is not None:
    raise ValueError('chds can only be used with text format')
  if chd.startswith('s:'):
    return _decode_simple(chd)
  if chd.startswith('e:'):
    return _decode_extended(chd)
  raise ValueError('invalid chd: {0}'.format(chd))

class TestChdecode(unittest.TestCase):
  """
  Testing on samples from the data formats documentation:

  https://developers.google.com/chart/image/docs/data_formats
  """

  def test_text(self):
    chd = 't:_,30,-30,50,80,200'
    self.assertEquals(chdecode(chd), [
      [None, 30, None, 50, 80, 100]
    ])

    chd = 't:-5,30,-30,50,80,200'
    chds = 'a'
    self.assertEquals(chdecode(chd, chds), [
      [-5, 30, -30, 50, 80, 200]
    ])

    chd = 't:30,-60,50,140,80,-90'
    chds = '-80,140'
    self.assertEquals(chdecode(chd, chds), [
      [30, -60, 50, 140, 80, None]
    ])

  def test_simple(self):
    chd = 's:BTb19_,Mn5tzb'
    self.assertEquals(chdecode(chd), [
      [1, 19, 27, 53, 61, None],
      [12, 39, 57, 45, 51, 27]
    ])

  def test_extended(self):
    chd = 'e:BaPoqM2s,-A__RMD6'
    self.assertEquals(chdecode(chd), [
      [90, 1000, 2700, 3500],
      [3968, None, 1100, 250]
    ])

if __name__ == '__main__':
  unittest.main()
