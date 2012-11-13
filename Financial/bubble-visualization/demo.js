function buildChart(data) {
  var cs = {};
  data.each(function(tx) {
    if (tx['Transaction Type'] != 'debit') {
      return;
    }
    var c = tx['Category'];
    if (c == 'Transfer') {
      return;
    }
    if (!(c in cs)) {
      cs[c] = 0.0;
    }
    cs[c] += +(tx['Amount']);
  });
  var w = 640,
      h = 480,
      nodes = [];
  for (var c in cs) {
    nodes.push({
      R: Math.max(2, Math.sqrt(cs[c])),
      category: c,
      weight: cs[c]
    });
  }
  var Rs = nodes.map(function(d) { return d.R; });
  var fill = d3.scale.linear()
    .domain([d3.min(Rs), d3.max(Rs)])
    .range(['#7EFF77', '#067500']);

  var vis = d3.select('#chart').append('svg:svg')
    .attr('width', w)
    .attr('height', h);

  var force = d3.layout.force()
    .nodes(nodes)
    .links([])
    .size([w, h])
    .start();

  var node = vis.selectAll('circle.node')
    .data(nodes)
    .enter().append('svg:circle')
    .attr('class', 'node')
    .attr('cx', function(d) { return d.x; })
    .attr('cy', function(d) { return d.y; })
    .attr('r', function(d) { return d.R; })
    .style('fill', function(d) { return fill(d.R); })
    .style('stroke', function(d) { return d3.rgb(fill(d.R)).darker(1); })
    .style('stroke-width', function(d) { return Math.max(1.0, d.R / 50); })
    .on('mouseover', function(d) {
      console.log(d.category);
    })
    .on('mouseout', function(d) {
    })
    .call(force.drag);
  
  force
    .gravity(0.05)
    .friction(0.9)
    .charge(function(d) { return -d.R * d.R / 8; });

  force.on('tick', function(e) {
    nodes.each(function(d1, i) {
      nodes.each(function(d2, j) {
        if (i >= j) {
          return;
        }
        var dx = d2.x - d1.x;
        var dy = d2.y - d1.y;
        var sr = d1.R + d2.R;
        var dr = sr - Math.sqrt(dx * dx + dy * dy);
        if (dr > 0) {
          var ux = dr * dx / sr;
          var uy = dr * dy / sr;
          d2.x += ux / 2;
          d2.y += uy / 2;
          d1.x -= ux / 2;
          d1.y -= uy / 2;
        }
      });
    });
    node
      .attr('cx', function(d) { return d.x; })
      .attr('cy', function(d) { return d.y; });
  });
}

window.addEvent('domready', function() {
  function handleFileSelect(evt) {
    console.log(evt);
    evt.stopPropagation();
    evt.preventDefault();

    var files = evt.dataTransfer.files;
    if (files.length == 0) {
      alert('no files');
      return;
    }
    var f = files[0];
    if (f.type != 'text/csv') {
      alert('invalid file type: ' + f.type);
      return;
    }
    var reader = new FileReader();
    reader.onloadstart = function(e) {
      if (e.lengthComputable) {
        $('progress').removeClass('hidden');
        $('progress_bar').set('value', 0);
        $('progress_bar').set('max', e.total);
      }
    };
    reader.onprogress = function(e) {
      if (e.lengthComputable) {
        $('progress_bar').value = e.loaded;
      }
    };
    reader.onload = function(e) {
      buildChart(d3.csv.parse(e.target.result));
    };
    reader.onloadend = function(e) {
      $('progress').addClass('hidden');
      $('drop_zone').addClass('hidden');
    };
    reader.readAsText(f);
  }

  var dropZone = $('drop_zone');
  dropZone.addEventListener('dragenter', function(evt) {
    evt.stopPropagation();
    evt.preventDefault();
  }, false);
  dropZone.addEventListener('dragexit', function(evt) {
    evt.stopPropagation();
    evt.preventDefault();
  }, false);
  dropZone.addEventListener('dragover', function(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    evt.dataTransfer.dropEffect = 'copy';
  }, false);
  dropZone.addEventListener('drop', handleFileSelect, false);
});
