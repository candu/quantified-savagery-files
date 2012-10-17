Math.randgauss = function() {
  var U, V, S, X, Y;
  while (true) {
    U = 2 * Math.random() - 1;
    V = 2 * Math.random() - 1;
    S = U * U + V * V;
    if (0 < S && S < 1) {
      return U * Math.sqrt(-2.0 * Math.log(S) / S);
    }
  }
}

function build_dataset(N, M, dM) {
  var L = [];
  for (var i = 0; i < N; i++) {
    L.push(M * (Math.randgauss() + 3));
  }
  L.sort(function(x1, x2) { return x1 - x2; });
  var D = [];
  for (var i = 0; i < N; i++) {
    D.push({
      a: L[i],
      b: 5 * M * (0.1 + i / N + dM * Math.randgauss())
    });
  }
  return D;
}

window.onload = function() {
  var M = 10;
  var D = build_dataset(10000, M, 0.05);
  var filter = crossfilter(D);
  var dim = function(k) {
    return filter.dimension(function (d) {
      return Math.max(0, Math.min(6 * M, d[k]));
    });
  }
  var dimA = dim('a');
  var dimB = dim('b');

  var scale = d3.scale.linear()
        .domain([0, 6 * M])
        .rangeRound([0, 10 * (6 * M + 1)]);
  var chartDefs = [
    barChart()
        .dimension(dimA)
        .group(dimA.group(Math.round))
        .x(scale),
    barChart()
        .dimension(dimB)
        .group(dimB.group(Math.round))
        .x(scale)
  ]
  
  var chartDivs = d3.selectAll(".chart")
    .data(chartDefs)
    .each(function(chartDiv) {
      chartDiv.on("brush", renderAll).on("brushend", renderAll);
    });
  
  function renderAll() {
    chartDivs.each(function(method) {
      d3.select(this).call(method);
    });
  }
  
  window.reset = function(i) {
    chartDefs[i].filter(null);
    renderAll();
  };
  
  renderAll();
};
