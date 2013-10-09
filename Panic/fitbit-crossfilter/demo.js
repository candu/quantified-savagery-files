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

Array.range = function(start, end) {
  var L = [];
  for (var i = start; i < end; i++) {
    L.push(i);
  }
  return L;
}

function build_dataset(N, M, dM) {
  var R = Array.range(0, N);
  var L = R.map(function(x) {
    return M * (Math.randgauss() + 3);
  }).sort(function(x1, x2) { return x1 - x2; });
  return R.map(function(x, i) {
    var b =  5 * M * (0.1 + i / N + dM * Math.randgauss());
    return {a: L[i], b: b};
  });
}

window.onload = function() {
  var M = 10;
  var filter = crossfilter(build_dataset(10000, M, 0.05));
  var dim = function(k) {
    return filter.dimension(function (d) {
      return Math.max(0, Math.min(6 * M, d[k]));
    });
  }
  var def = function(k) {
    var dimK = dim(k);
    return barChart()
      .dimension(dimK)
      .group(dimK.group(Math.round))
      .x(d3.scale.linear()
        .domain([0, 6 * M])
        .rangeRound([0, 10 * (6 * M + 1)]));
  }
  var chartDefs = [def('a'), def('b')];
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
