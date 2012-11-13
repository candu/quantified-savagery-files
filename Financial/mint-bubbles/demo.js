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
      cs[c] = {
        amount: 0,
        txs: []
      };
    }
    cs[c].amount += +(tx['Amount']);
    cs[c].txs.push(tx);
  });
  var w = 960,
      h = 480,
      nodes = [];
  for (var c in cs) {
    nodes.push({
      R: Math.max(2, Math.sqrt(cs[c].amount)),
      category: c,
      amount: cs[c].amount,
      txs: cs[c].txs
    });
  }
  var Rs = nodes.map(function(d) { return d.R; });
  var minR = d3.min(Rs),
      maxR = d3.max(Rs);
  var fill = d3.scale.linear()
    .domain([minR, maxR])
    .range(['#7EFF77', '#067500']);
  var floatPoint = d3.scale.linear()
    .domain([minR, maxR])
    .range([h * 0.65, h * 0.35]);

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
    .on('click', function(d) {
      document.id('prompt').addClass('hidden');
      document.id('total').removeClass('hidden');
      document.id('transactions').removeClass('hidden');
      d3.selectAll('circle').attr('class', '');
      d3.select(this).attr('class', 'circle-active');
      var total = Math.round(d.amount * 100);
      var cents = total % 100;
      var dollars = (total - cents) / 100;
      if (cents < 10) {
        cents = '0' + cents;
      }
      var text = d.category + ': $' + dollars + '.' + cents;
      document.id('total').set('text', text);
      document.id('transactions_tbody').empty();
      d.txs.each(function(tx) {
        var tr = new Element('tr');
        var fields = ['Date', 'Amount', 'Description'];
        for (var i = 0; i < fields.length; i++) {
          tr.grab(new Element('td', {
            text: tx[fields[i]]
          }));
        }
        document.id('transactions_tbody').grab(tr);
      });
    })
    .call(force.drag);
  
  force
    .gravity(0.05)
    .friction(0.95)
    .charge(function(d) { return -d.R * d.R / 8; });

  force.on('tick', function(e) {
    // vertical size sorting
    nodes.each(function(d) {
      var dy = floatPoint(d.R) - d.y;
      d.y += 0.25 * dy * e.alpha;
    });

    // collision detection
    var q = d3.geom.quadtree(nodes);
    nodes.each(function(d1) {
      q.visit(function(quad, x1, y1, x2, y2) {
        var d2 = quad.point;
        if (d2 && (d2 !== d1)) {
          var x = d1.x - d2.x,
              y = d1.y - d2.y,
              L = Math.sqrt(x * x + y * y),
              R = d1.R + d2.R;
          if (L < R) {
            L = (L - R) / L * 0.5;
            var Lx = L * x,
                Ly = L * y;
            d1.x -= Lx; d1.y -= Ly; 
            d2.x += Lx; d2.y += Ly; 
          }
        }
        return
          x1 > (d1.x + d1.R) ||
          x2 < (d1.x - d1.R) ||
          y1 > (d1.y + d1.R) ||
          y2 < (d1.y - d1.R);
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
        document.id('progress').removeClass('hidden');
        document.id('progress_bar').set('value', 0);
        document.id('progress_bar').set('max', e.total);
      }
    };
    reader.onprogress = function(e) {
      if (e.lengthComputable) {
        document.id('progress_bar').value = e.loaded;
      }
    };
    reader.onload = function(e) {
      buildChart(d3.csv.parse(e.target.result));
    };
    reader.onloadend = function(e) {
      document.id('caption').removeClass('hidden').addClass('chart-active');
      document.id('progress').addClass('hidden');
      document.id('drop_zone').addClass('hidden');
      document.id('chart').addClass('chart-active');
    };
    reader.readAsText(f);
  }

  var dropZone = document.id('drop_zone');
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
