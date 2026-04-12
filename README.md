# Cycling Route Viewer

Lightweight cycling route embeds for Squarespace travel log pages. Each ride is an HTML file hosted on GitHub Pages and embedded via an iframe.

## How it works

- Each HTML file references a GPX file in the trip's `gpx/` subfolder
- A stats bar shows Distance, Moving Time, Elevation Gain, and Weather (from Open-Meteo)
- Files are hosted on GitHub Pages and embedded in Squarespace via an Embed Block
- A merged `full_trip.html` shows all days on one map (no stats bar)

## Folder structure

```
cycling-ripplet/
  template.html                  ← master template (do not edit directly)
  generate.py                    ← script to create HTML files from GPX files
  merge_gpx.py                   ← script to merge all GPX files and create full_trip.html
  2025_Western_Alps/
    D1_Annecy_to_Le_Grand_Bornand.html
    D2_...html
    full_trip.html
    gpx/
      D1_Annecy_to_Le_Grand_Bornand.gpx
      D2_...gpx
      full_trip.gpx
  2026_Some_Trip/
    D1_...html
    gpx/
      D1_...gpx
```

## Adding a new trip

1. Create the trip folder and a `gpx/` subfolder inside it
2. Export GPX files from Strava (Activity → Export GPX) and put them in `gpx/`
3. Optionally, run the merge script to create the full-trip overview map:
   ```bash
   python3 merge_gpx.py 2025_Western_Alps
   ```
   This creates `gpx/full_trip.gpx` and `full_trip.html`
4. Run the generate script:
   ```bash
   python3 generate.py 2025_Western_Alps
   ```
   This creates an HTML file for each day's GPX and writes `embed_codes.txt`
5. For any ride where you missed the Strava start, open the HTML file and set `EXTRA_KM`
6. Commit and push — GitHub Pages publishes automatically:
   ```bash
   git add . && git commit -m "Add 2025_Western_Alps" && git push
   ```
7. Open `embed_codes.txt` — copy each iframe code into the corresponding Squarespace Embed Block

## CONFIG options (top of each HTML file)

| Variable | Description |
|---|---|
| `GPX_FILE` | Path to the GPX file — set automatically by `generate.py` |
| `ROUTE_COLOR` | Hex colour of the route line |
| `EXTRA_KM` | Extra distance to add if you missed the Strava start (default `0`) |
