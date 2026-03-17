# Cycling Route Viewer — Claude context

## What this project is

A collection of HTML files, one per cycling ride, hosted on GitHub Pages at `https://tomomiq.github.io/cycling-ripplet/`. Each file is embedded in a Squarespace travel log page via an iframe Embed Block.

## Stack

- **Leaflet.js 1.9.4** (cdnjs) — map rendering
- **leaflet-gpx 1.7.0** (jsDelivr) — GPX parsing and stats
- **OpenStreetMap** tiles — free, no API key
- **Open-Meteo archive API** — historical hourly weather, no API key

## Architecture decisions

- GPX files live in a `gpx/` subfolder within each trip folder. The HTML references the GPX by relative path (`gpx/filename.gpx`)
- No build step, no backend, no API keys
- Weather is fetched client-side from Open-Meteo using the ride's start coordinates and date parsed from the GPX timestamps
- Map height is fixed at `420px`
- `generate.py` creates HTML files from GPX files and outputs `embed_codes.txt` — this file is gitignored

## Per-ride workflow

Drop GPX files into the trip's `gpx/` folder. Run `python3 generate.py <trip_folder>`. Set `EXTRA_KM` in any file where the Strava start was missed. Commit and push. Use `embed_codes.txt` for Squarespace embed codes.

## Squarespace embed

Personal plan — uses Embed Block with raw `<iframe>` tag (not URL, as Squarespace tries oEmbed and rejects non-oEmbed URLs). Recommended iframe height: 480px. Include `style="display:block"` on the iframe to avoid inline spacing gaps.
