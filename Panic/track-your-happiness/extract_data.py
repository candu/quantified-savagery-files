from lxml import etree
import sys
import urlparse
import json
import chdecode

def getChartURL(chart_div):
  key = chart_div.find('h2').text
  imgs = chart_div.findall('img')
  for img in imgs:
    src = img.attrib['src']
    if src.startswith('https://chart.googleapis.com'):
      return key, src
  raise Exception('could not find gcharts URL')

def fitSimpleToRange(x, xmin, xmax):
  if x is None:
    return None
  nx = x / 61.0
  return (1.0 - nx) * xmin + nx * xmax

def extractData(url):
  """
  See https://developers.google.com/chart/image/docs/data_formats for details
  on chd encoding.
  """
  parsed_url = urlparse.urlparse(url)
  params = urlparse.parse_qs(parsed_url.query)
  data = chdecode.chdecode(params['chd'][0])
  rs = []
  for r in params['chxr'][0].split('|'):
    axis, xmin, xmax = r.split(',')
    axis = int(axis)
    xmin, xmax = float(xmin), float(xmax)
    rs.append((axis, xmin, xmax))
  if len(data) == 1:
    labels = reversed(params['chxl'][0][3:].split('|'))
    axis, xmin, xmax = rs[0]
    return zip(labels, [fitSimpleToRange(x, xmin, xmax) for x in data[0]])
  for r in rs:
    axis, xmin, xmax = r
    data[axis] = [fitSimpleToRange(x, xmin, xmax) for x in data[axis]]
  return zip(*data)

def main():
  parser = etree.HTMLParser()
  root = etree.parse(sys.stdin, parser)
  chart_divs = root.xpath("//div[@class='chart']|//div[@class='chart long']")
  charts = {}
  for chart_div in chart_divs:
    key, url = getChartURL(chart_div)
    data = extractData(url)
    charts[key] = data
  print json.dumps(charts)

if __name__ == '__main__':
  main()
