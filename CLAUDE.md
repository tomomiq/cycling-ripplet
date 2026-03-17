# Cycling Route Viewer — Claude context

## What this project is

A collection of self-contained HTML files, one per cycling ride, hosted on GitHub Pages at `https://tomomiq.github.io/cycling-ripplet/`. Each file is embedded in a Squarespace travel log page via an iframe Embed Block.

## Stack

- **Leaflet.js 1.9.4** (cdnjs) — map rendering
- **leaflet-gpx 1.7.0** (jsDelivr) — GPX parsing and stats
- **OpenStreetMap** tiles — free, no API key
- **Open-Meteo archive API** — historical hourly weather, no API key

## Architecture decisions

- GPX data is embedded inline in each HTML file (not a separate file) to keep the repo to HTML-only files
- No build step, no backend, no API keys
- Weather is fetched client-side from Open-Meteo using the ride's start coordinates and date parsed from the GPX timestamps
- Map height uses `calc(100vh - 60px)` so it fills the iframe exactly regardless of height set in Squarespace

## Per-ride workflow

Copy `template.html`, update the `<title>`, paste GPX content into `var GPX_DATA`, set `EXTRA_KM` if needed, commit and push.

## Squarespace embed

Personal plan — uses Embed Block with raw `<iframe>` tag (not URL, as Squarespace tries oEmbed and rejects non-oEmbed URLs). Recommended iframe height: 480px.
