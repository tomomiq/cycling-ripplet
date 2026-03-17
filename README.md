# Cycling Route Viewer

Lightweight cycling route embeds for Squarespace travel log pages. Each ride is a self-contained HTML file hosted on GitHub Pages and embedded via an iframe.

## How it works

- Each HTML file contains an interactive Leaflet.js map + inline GPX data
- A stats bar shows Distance, Moving Time, Elevation Gain, and Weather (from Open-Meteo)
- Files are hosted on GitHub Pages and embedded in Squarespace via an Embed Block

## Folder structure

```
cycling-ripplet/
  template.html                  ← copy this for each new ride
  2025_Western_Alps/
    D1_Annecy_to_Le_Grand_Bornand.html
    gpx/
      D1_Annecy_to_Le_Grand_Bornand.gpx
  2026_Some_Trip/
    D1_...html
    gpx/
      D1_...gpx
```

## Adding a new ride

1. Export GPX from Strava (Activity → Export GPX)
2. Copy `template.html` into the trip folder, rename it for the ride
3. Add the GPX file into the trip's `gpx/` folder
4. Open the HTML file and update the CONFIG section at the top:
   - Update `GPX_FILE` to match the GPX filename
   - Set `EXTRA_KM` if you missed the start (default `0`)
5. Commit and push — GitHub Pages publishes automatically
6. In Squarespace, add an Embed Block and paste:
   ```html
   <iframe src="https://tomomiq.github.io/cycling-ripplet/TRIP/RIDE.html" width="100%" height="480" frameborder="0" scrolling="no"></iframe>
   ```

## CONFIG options (top of each HTML file)

| Variable | Description |
|---|---|
| `ROUTE_COLOR` | Hex colour of the route line |
| `EXTRA_KM` | Extra distance to add if you missed the Strava start |
