function setup_axes(chart, w, h, x, y) {
  chart.append('svg:line')
    .attr('x1', x(0)).attr('y1', 0)
    .attr('x2', x(0)).attr('y2', h)
    .attr('class', 'tick');

  chart.append('svg:line')
    .attr('x1', 0).attr('y1', y(0))
    .attr('x2', w).attr('y2', y(0))
    .attr('class', 'tick');
}

window.addEvent('domready', function() {
  var N = 200, d = 0.1;
  var S1, S2;
  var s1Funcs = {
    sine : Array.range(0, N + 1).map(function(x) {
      return Math.sin(x * 2.0 * Math.PI / N) + d * Math.randgauss();
    }),
    noise : Array.range(0, N + 1).map(function(x) {
      return d * Math.randgauss();
    }),
    impulse : Array.range(0, N + 1).map(function(x) {
      return Math.max(0, Math.min(Math.randgauss() - 0.5, 1.5));
    })
  };
  var s2Funcs = {
    sine: Array.range(0, 2 * N + 1).map(function(x) {
      return Math.sin((x - 42) * 2.0 * Math.PI / N) + d * Math.randgauss();
    }),
    noise : Array.range(0, 2 * N + 1).map(function(x) {
      return d * Math.randgauss();
    }),
    impulse : Array.range(0, 2 * N + 1).map(function(x) {
      var t = (x - 42) % N;
      if (t < 0) t += N;
      return s1Funcs['impulse'][t] + d * Math.randgauss();
    })
  };
  function update_s1(funcName) {
    S1 = s1Funcs[funcName];
  }
  function update_s2(funcName) {
    S2 = s2Funcs[funcName];
  }
  update_s1('sine');
  update_s2('sine');

  var crossCorrelation = function(t) {
    t = t % N;
    if (t < 0) {
      t += N;
    }
    var C = 0;
    for (var tau = 0; tau < N; tau++) {
      C += S1[tau] * S2[(tau + t) % N];
    }
    return C / N;
  }

  for (var t = 30; t < 50; t++) {
    console.log([t, crossCorrelation(t)]);
  }

  var C, cMin, cMax;
  function update_c() {
    C = Array.range(0, N + 1).map(function(t) {
      return crossCorrelation(t);
    });
    cMin = d3.min(C);
    cMax = d3.max(C);
  }
  update_c();

  var w = 640, h = 160;
  var x = d3.scale.linear().domain([0, 2 * N]).range([0, 2 * w]);
  var y = d3.scale.linear().domain([-1.5, 1.5]).range([h, 0]);

  var datasetsChart = d3.select('#datasets')
    .append('svg:svg')
    .attr('width', w + 10)
    .attr('height', h + 10);

  var crossCorrelationChart = d3.select('#cross-correlation')
    .append('svg:svg')
    .attr('width', w + 10)
    .attr('height', h + 10);

  var rawData = datasetsChart.append('svg:g')
    .attr('transform', 'translate(5, 5)');
  
  var crossCorrelationData = crossCorrelationChart.append('svg:g')
    .attr('transform', 'translate(5, 5)');
 
  var A = d3.svg.area()
    .x(function(d, i) { return x(i); })
    .y0(h)
    .y1(y)
    .interpolate('linear');

  var s1Area = rawData.append('svg:path')
    .attr('d', A(S1))
    .attr('class', 's1');

  var s2Area = rawData.append('svg:path')
    .attr('d', A(S2))
    .attr('class', 's2')

  var tLine = crossCorrelationData.append('svg:line')
    .attr('x1', 0).attr('y1', 0)
    .attr('x2', 0).attr('y2', h)
    .attr('class', 't');

  var dx = 0;
  var textColor = d3.scale.linear()
    .domain([0, 1])
    .range(['#000', '#606']);
  function update_t(t) {
    var tx = Math.floor(x(t)) + 0.5;
    tLine.attr('x1', tx).attr('x2', tx);
    var tf = crossCorrelation(t);
    var clr = textColor((tf - cMin) / (cMax - cMin));
    if (tf == cMax) {
      clr = '#f0f';
    }
    d3.select('#status')
      .text('(t, f(t)) == (' + t + ', ' + tf + ')')
      .style('color', clr);
  }

  var dragBehavior = d3.behavior.drag().on('drag', function(d, i) {
    dx += d3.event.dx;
    dx = Math.max(-w, Math.min(dx, 0));
    s2Area.attr('transform', 'translate(' + dx + ', 0)');
    update_t(Math.floor(-N * dx / w));
  });

  function reset_t() {
    dx = 0;
    update_t(0);
  }

  datasetsChart.call(dragBehavior);
  setup_axes(rawData, w, h, x, y);
  setup_axes(crossCorrelationData, w, h, x, y);

  var cArea = crossCorrelationData.append('svg:path')
    .attr('d', A(C))
    .attr('class', 'c');
  
  function update_area(area, dataset) {
    area.attr('d', A(dataset));
  }
  
  d3.select('#s1-picker').on('change', function() {
    update_s1(this.value);
    update_c();
    update_area(s1Area, S1);
    update_area(cArea, C);
    reset_t();
  });

  d3.select('#s2-picker').on('change', function() {
    update_s2(this.value);
    update_c();
    update_area(s2Area, S2);
    update_area(cArea, C);
    reset_t();
  });

  reset_t();
});
