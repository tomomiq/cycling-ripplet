#!/usr/bin/env python3
"""
Usage: python3 merge_gpx.py <trip_folder>
Example: python3 merge_gpx.py 2025_Western_Alps

Merges all GPX files in <trip_folder>/gpx/ into a single full_trip.gpx
and writes full_trip.html (map only, no stats bar).
Skips full_trip.gpx itself if it already exists. Safe to re-run.
"""

import sys
import os
import re

FULL_TRIP_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Full Trip</title>
  <link rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"
    integrity="sha512-h9FcoyWjHcOcmEVkxOfTLnmZFWIH0iZhZT1H2TbOq55xssQGEJHEaIm+PgoUaZbRvQTNTluNOEfb1ZRy6D3BOw=="
    crossorigin="anonymous" />
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: system-ui, sans-serif; background: #fff; }
    #map-wrap { position: relative; }
    #map { width: 100%; height: 420px; }
    #touch-overlay {
      display: none; position: absolute; inset: 0;
      background: rgba(0,0,0,0.45); color: #fff; font-size: 1rem;
      align-items: center; justify-content: center;
      pointer-events: none; z-index: 1000;
    }
    #map-wrap.show-overlay #touch-overlay { display: flex; }
  </style>
</head>
<body>
<div id="map-wrap">
  <div id="map"></div>
  <div id="touch-overlay">Use two fingers to move the map</div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"
  integrity="sha512-puJW3E/qXDqYp9IfhAI54BJEaWIfloJ7JWs7OeD5i6ruC9JZL1gERT1wjtwXFlh7CjE7ZJ+/vcRZRkIYIb6p4g=="
  crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/leaflet-gpx@1.7.0/gpx.js"
  integrity="sha512-FatQYmF8k/KuvOgmwfRGRqlyzbG13etWz1GOO+JO6YQyhGgw5tVl9ihC9RS8S6iiS18CZAnZBvUoKHlGI6BTPQ=="
  crossorigin="anonymous"></script>
<script>
  var map = L.map('map', { zoomControl: false });
  var initialBounds;

  L.Control.MapButtons = L.Control.extend({
    options: { position: 'topright' },
    onAdd: function(map) {
      var c = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
      var zi = L.DomUtil.create('a', 'leaflet-control-zoom-in', c);
      zi.innerHTML = '+'; zi.title = 'Zoom in'; zi.href = '#';
      L.DomEvent.on(zi, 'click', function(e) {
        L.DomEvent.stopPropagation(e); L.DomEvent.preventDefault(e); map.zoomIn();
      });
      var zo = L.DomUtil.create('a', 'leaflet-control-zoom-out', c);
      zo.innerHTML = '−'; zo.title = 'Zoom out'; zo.href = '#';
      L.DomEvent.on(zo, 'click', function(e) {
        L.DomEvent.stopPropagation(e); L.DomEvent.preventDefault(e); map.zoomOut();
      });
      var r = L.DomUtil.create('a', '', c);
      r.innerHTML = '⊙'; r.title = 'Reset view'; r.href = '#';
      r.style.fontSize = '16px'; r.style.lineHeight = '26px';
      L.DomEvent.on(r, 'click', function(e) {
        L.DomEvent.stopPropagation(e); L.DomEvent.preventDefault(e);
        if (initialBounds) { map.invalidateSize(); map.fitBounds(initialBounds, { padding: [20, 20] }); }
      });
      return c;
    }
  });
  new L.Control.MapButtons().addTo(map);
  map.attributionControl.setPrefix('');

  L.tileLayer('https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://www.cyclosm.org/">CyclOSM</a> | © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 20
  }).addTo(map);

  var wrap = document.getElementById('map-wrap');
  wrap.addEventListener('touchstart', function(e) {
    if (e.touches.length === 1) wrap.classList.add('show-overlay');
  }, { passive: true });
  wrap.addEventListener('touchend', function() {
    wrap.classList.remove('show-overlay');
  }, { passive: true });
  wrap.addEventListener('touchmove', function(e) {
    if (e.touches.length >= 2) wrap.classList.remove('show-overlay');
  }, { passive: true });

  new L.GPX('gpx/full_trip.gpx', {
    async: true,
    polyline_options: { color: '#1565C0', weight: 3, opacity: 0.9 },
    marker_options: { startIconUrl: null, endIconUrl: null, shadowUrl: null, wptIconUrls: { '': null } }
  })
  .on('loaded', function(e) {
    var gpx = e.target;
    initialBounds = gpx.getBounds();
    map.invalidateSize();
    map.fitBounds(initialBounds, { padding: [20, 20] });
    map.zoomOut(2);
  })
  .on('error', function(e) { console.error('GPX load error', e); })
  .addTo(map);
</script>
</body>
</html>'''


def extract_trk_blocks(content):
    return re.findall(r'<trk>.*?</trk>', content, re.DOTALL)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 merge_gpx.py <trip_folder>")
        sys.exit(1)

    trip = sys.argv[1].rstrip('/')
    gpx_dir = os.path.join(trip, 'gpx')

    if not os.path.isdir(gpx_dir):
        print(f"Error: no gpx/ subfolder found in '{trip}'")
        sys.exit(1)

    gpx_files = sorted(
        f for f in os.listdir(gpx_dir)
        if f.endswith('.gpx') and f != 'full_trip.gpx'
    )

    if not gpx_files:
        print(f"No GPX files found in {gpx_dir}/")
        sys.exit(0)

    all_trk_blocks = []
    for gpx_filename in gpx_files:
        path = os.path.join(gpx_dir, gpx_filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        blocks = extract_trk_blocks(content)
        if blocks:
            all_trk_blocks.extend(blocks)
            print(f"  read    {gpx_filename} ({len(blocks)} track)")
        else:
            print(f"  warning: no <trk> found in {gpx_filename}, skipping")

    output = '<?xml version="1.0" encoding="UTF-8"?>\n'
    output += '<gpx version="1.1" creator="merge_gpx.py" xmlns="http://www.topografix.com/GPX/1/1">\n'
    for block in all_trk_blocks:
        output += block + '\n'
    output += '</gpx>\n'

    out_path = os.path.join(gpx_dir, 'full_trip.gpx')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"\n  wrote   {out_path}  ({len(all_trk_blocks)} tracks total)")

    html_path = os.path.join(trip, 'full_trip.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(FULL_TRIP_HTML)
    print(f"  wrote   {html_path}")

if __name__ == '__main__':
    main()
