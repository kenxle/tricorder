(function () {
  // The expert-read sections' charts, drawn with plotly.js from the file beside the page. The data is the
  // script's (scans/memo/charts.py); this only draws it. Colours are tricorder.css's, read from the page.
  var R = document.getElementById('report-data'); if (!R) return;
  var reports = JSON.parse(R.textContent);
  var root = document.documentElement;
  function css(el, name) { return getComputedStyle(el).getPropertyValue(name).trim(); }
  function money(n) {
    var a = Math.abs(n), s;
    if (a >= 1e6) s = '$' + (a / 1e6).toFixed(2).replace(/\.?0+$/, '') + 'M';
    else if (a >= 1e4) s = '$' + Math.round(a / 1e3) + 'K';
    else s = '$' + Math.round(a).toLocaleString('en-US');
    return (n < 0 ? '-' : '') + s;
  }
  function where(src) { return src ? src.file + ', ' + src.locator : ''; }
  function draw() {
    if (!window.Plotly) {
      document.querySelectorAll('.xr-plot').forEach(function (el) { el.hidden = true; var d = el.parentNode.querySelector('.xr-data'); if (d) d.open = true; });
      return;
    }
    reports.forEach(function (r) {
      var c = r.chart; if (!c) return;
      var el = document.getElementById('xr-plot-' + r.piece); if (!el) return;
      var col = {metric: css(el, '--xc-1'), plan: css(el, '--xc-1'), rebuilt: css(el, '--xc-2'), found: css(el, '--xc-3'),
                 stated: css(el, '--xc-3'), baseline: css(el, '--xc-4')};
      var ink = css(el, '--xc-ink'), grid = css(el, '--xc-grid'), font = css(el, '--xc-font');
      var traces = [], shapes = [], notes = [];
      c.series.forEach(function (s) {
        var src = (s.sources || [s.source]).map(where).join('; ');
        traces.push({type: 'scatter', mode: 'lines', name: s.name, x: s.x, y: s.y,
          line: {color: col[s.role] || col.metric, width: s.role === 'found' || s.role === 'rebuilt' ? 2.5 : 3, dash: s.role === 'rebuilt' ? 'dot' : 'solid'},
          hovertemplate: '%{x}<br><b>%{customdata}</b><extra>' + s.name + '<br>' + src + '</extra>',
          customdata: s.y.map(money)});
      });
      c.markers.forEach(function (m) {
        traces.push({type: 'scatter', mode: 'markers+text', name: m.name + ' states ' + money(m.y), x: [m.x], y: [m.y],
          marker: {color: col.stated, size: 13, symbol: 'diamond', line: {color: css(el, '--xc-bg'), width: 1.5}},
          text: [m.name], textposition: 'middle left', textfont: {color: col.stated, family: font, size: 12},
          hovertemplate: '%{x}<br><b>' + money(m.y) + '</b><extra>' + m.name + '<br>' + where(m.source) + '</extra>'});
      });
      c.lines.forEach(function (ln, i) {
        var color = col[ln.role] || ink;
        shapes.push({type: 'line', xref: 'x', yref: 'paper', x0: ln.x, x1: ln.x, y0: 0, y1: 1,
          line: {color: color, width: 1.5, dash: ln.role === 'baseline' ? 'dash' : 'dot'}});
        notes.push({x: ln.x, y: 1 - i * 0.09, xref: 'x', yref: 'paper', xanchor: 'left', yanchor: 'top', showarrow: false,
          text: ln.name + (ln.months ? ': ' + ln.x + ', ' + ln.months + ' months' : ': ' + ln.x),
          font: {color: color, family: font, size: 11.5}, bgcolor: css(el, '--xc-bg'), borderpad: 3});
      });
      if (c.kind === 'cash_and_runway') shapes.push({type: 'line', xref: 'paper', x0: 0, x1: 1, y0: 0, y1: 0, line: {color: ink, width: 1}});
      var layout = {
        height: 380, margin: {l: 64, r: 16, t: 12, b: 8}, paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
        font: {family: font, color: ink, size: 12}, hovermode: 'closest', showlegend: true,
        legend: {orientation: 'h', x: 0, y: -0.14, yanchor: 'top', font: {size: 12}},
        xaxis: {type: 'category', gridcolor: grid, linecolor: grid, tickangle: 0, nticks: 10, automargin: true},
        yaxis: {gridcolor: grid, zerolinecolor: grid, tickformat: '$~s', automargin: true},
        shapes: shapes, annotations: notes
      };
      Plotly.react(el, traces, layout, {displaylogo: false, responsive: true,
        modeBarButtonsToRemove: ['select2d', 'lasso2d', 'autoScale2d', 'toggleSpikelines']});
    });
  }
  draw();
  // Redraw in the reader's theme when it changes.
  new MutationObserver(draw).observe(root, {attributes: true, attributeFilter: ['data-theme']});
  if (window.matchMedia) { var mq = matchMedia('(prefers-color-scheme: dark)'); if (mq.addEventListener) mq.addEventListener('change', draw); }
})();
