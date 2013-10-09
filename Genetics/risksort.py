import json
import sys

def W(p, a):
  return (p ** a) / ((p ** a + (1 - p) ** a) ** (1 / a))

def R(p0, p):
  a = (p0 < p) and 0.61 or 0.69
  return W(p0, a) / W(p, a)

data = json.loads(sys.stdin.read())[0]
order_key = sys.argv[1]
for r in data['risks']:
  p0, p = r['risk'], r['population_risk']
  if p == 0:
    r['relative_risk'] = 0
    r['perceived_relative_risk'] = 0
  else:
    r['relative_risk'] = p0 / p
    r['perceived_relative_risk'] = R(p0, p)
sorted_risks = sorted(data['risks'], key=lambda r: r[order_key], reverse=True)
for i, r in enumerate(sorted_risks):
  print '%2d %50s %.4f' % (i + 1, r['description'], r[order_key])
