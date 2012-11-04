import pylab

RED = '#ff0000'
BLUE = '#0000ff'
MAGENTA = '#ff00ff'
DARK_GREY = '#666666'
GREY = '#999999'
LIGHT_GREY = '#d7d7d7'

def setupPlot(xlabel, ylabel, title):
  pylab.xlabel(xlabel)
  pylab.ylabel(ylabel)
  pylab.title(title)
  pylab.legend()
  pylab.grid(True, color=LIGHT_GREY, linestyle='-')
