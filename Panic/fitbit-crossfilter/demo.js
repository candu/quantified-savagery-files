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
      b: 4 * M * (i / N + dM * Math.randgauss() + 0.25)
    });
  }
  return D;
}

window.onload = function() {
  var M = 10;
  var D = build_dataset(50000, M, 0.05);
  var filter = crossfilter(D);
  var dimA = filter.dimension(function (d) {
    return Math.max(0, Math.min(6 * M, d.a));
  });
  var grpA = dimA.group(function (a) {
    return Math.round(a);
  });
  var dimB = filter.dimension(function (d) {
    return Math.max(0, Math.min(6 * M, d.b));
  });
  var grpB = dimB.group(function (b) {
    return Math.floor(b);
  });
  
  var chartDefs = [
    barChart()
        .dimension(dimA)
        .group(grpA)
      .x(d3.scale.linear()
        .domain([0, 6 * M])
        .rangeRound([0, 10 * (6 * M + 1)])),
    barChart()
        .dimension(dimB)
        .group(grpB)
      .x(d3.scale.linear()
        .domain([0, 6 * M])
        .rangeRound([0, 10 * (6 * M + 1)]))
  ]
  
  var chartDivs = d3.selectAll(".chart")
    .data(chartDefs)
    .each(function(chartDiv) {
      chartDiv.on("brush", renderAll).on("brushend", renderAll);
    });
  
  function render(method) {
    d3.select(this).call(method);
  }
  
  function renderAll() {
    chartDivs.each(render);
  }
  
  window.filter = function(filters) {
    filters.forEach(function(d, i) { chartDefs[i].filter(d); });
    renderAll();
  };
  
  window.reset = function(i) {
    chartDefs[i].filter(null);
    renderAll();
  };
  
  window.resetAll = function() {
    for (var i = 0; i < chartDefs.length; i++) {
      chartDefs[i].filter(null);
    }
    renderAll();
  }
  
  renderAll();
};
