window.addEvent('domready', function() {
  var N = 200, d = 0.1;
  var S1 = Array.range(0, N).map(function(x) {
    return Math.sin(x * 2.0 * Math.PI / N) + d * Math.randgauss();
  });
  var S2 = Array.range(0, N).map(function(x) {
    return Math.sin((x - 42) * 2.0 * Math.PI / N) + d * Math.randgauss();
  });

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

  var w = 640, h = 160;
  var x = d3.scale.linear().domain([0, N]).range([0, w]);
  var y1 = d3.scale.linear().domain([-1.5, 1.5]).range([h, 0]);

  var vis = d3.select('#chart')
    .append('svg:svg')
    .attr('width', w + 100)
    .attr('height', h);

  var rawData = vis.append('svg:g')
    .attr('transform', 'translate(0, 0)');
 
  var A = d3.svg.area()
    .x(function(d, i) { return x(i); })
    .y0(h)
    .y1(y1)
    .interpolate('linear');

  rawData.append('svg:path')
    .attr('d', A(S1))
    .attr('class', 's1');

  var dragBehavior = d3.behavior.drag().on('drag', function(d, i) {
    console.log([d3.event.dx, d3.event.dy]);
  });

  var activeArea = rawData.append('svg:path')
    .attr('d', A(S2))
    .attr('class', 's2')
    .call(dragBehavior);

  var ticks = vis.selectAll('.tick')
    .data(x.ticks(10))
    .enter().append('svg:g')
      .attr('transform', function(d) { return 'translate(' + x(d) + ', 0)'; })
      .attr('class', 'tick');

  ticks.append('svg:line')
    .attr('x1', 0).attr('y1', 0)
    .attr('x2', 0).attr('y2', h);
  
  ticks.append('svg:text')
    .text(function(d) { return d; })
    .attr('dx', 5)
    .attr('dy', h);
});
