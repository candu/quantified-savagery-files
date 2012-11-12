function buildChart(data) {
  var cs = {};
  data.each(function(tx) {
    var c = tx['Category'];
    if (!(c in cs)) {
      cs[c] = 0.0;
    }
    cs[c] += +(tx['Amount']);
  });
  var w = 960,
      h = 640,
      fill = d3.scale.category10(),
      nodes = [];
  for (var i in cs) {
    nodes.push({
      R: Math.sqrt(cs[i])
    });
  }

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
    .style('fill', function(d, i) { return fill(i % 10); })
    .style('stroke', function(d, i) { return d3.rgb(fill(i % 10)).darker(2); })
    .style('stroke-width', function(d) { return Math.max(1.0, d.R / 50); })
    .call(force.drag);
  
  force
    .gravity(0.1)
    .friction(0.9)
    .charge(function(d) { return -d.R * d.R / 8; });

  force.on('tick', function(e) {
    node
      .attr('cx', function(d) { return d.x; })
      .attr('cy', function(d) { return d.y; });
  });
}

window.addEvent('domready', function() {
  $('files').addEvent('change', function(evt) {
    var files = evt.target.files;
    if (files.length == 0) {
      alert('no files');
      return;
    }
    var f = files[0];
    if (f.type != 'text/csv') {
      alert('invalid file type: ' + f.type);
      return;
    }
    div = new Element('div', {
      'text': escape(f.name) + ' [' + f.type + ']: ' + f.size + ' bytes'
    });
    div.inject($('description'));
    var reader = new FileReader();
    reader.onloadstart = function(e) {
      if (e.lengthComputable) {
        $('progress').set('value', 0);
        $('progress').set('max', e.total);
        $('progress_pct').set('text', '0%');
      }
    };
    reader.onprogress = function(e) {
      if (e.lengthComputable) {
        $('progress').value = e.loaded;
        var pct = Math.floor(100 * e.loaded / e.total);
        $('progress_pct').set('text', pct + '%');
      }
    };
    reader.onload = function(e) {
      buildChart(d3.csv.parse(e.target.result));
    };
    reader.onabort = function(e) {

    };
    reader.onerror = function(e) {

    };
    reader.onloadend = function(e) {
      $('progress_pct').set('text', 'done.');
    };
    reader.readAsText(f);
  });
});
