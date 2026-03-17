#!/usr/bin/env python3
"""
Usage: python3 generate.py <trip_folder>
Example: python3 generate.py 2025_Western_Alps

Creates an HTML file for each GPX in <trip_folder>/gpx/ that doesn't
already have one. Skips existing HTML files so it's safe to re-run.
"""

import sys
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 generate.py <trip_folder>")
        print("Example: python3 generate.py 2025_Western_Alps")
        sys.exit(1)

    trip = sys.argv[1].rstrip('/')
    gpx_dir = os.path.join(trip, 'gpx')

    if not os.path.isdir(trip):
        print(f"Error: folder '{trip}' not found")
        sys.exit(1)

    if not os.path.isdir(gpx_dir):
        print(f"Error: no gpx/ subfolder found in '{trip}'")
        sys.exit(1)

    gpx_files = sorted(f for f in os.listdir(gpx_dir) if f.endswith('.gpx'))

    if not gpx_files:
        print(f"No GPX files found in {gpx_dir}/")
        sys.exit(0)

    with open('template.html', 'r') as f:
        template = f.read()

    created = 0
    skipped = 0

    for gpx_filename in gpx_files:
        html_filename = os.path.splitext(gpx_filename)[0] + '.html'
        html_path = os.path.join(trip, html_filename)

        if os.path.exists(html_path):
            print(f"  skip    {html_path}")
            skipped += 1
            continue

        html = template.replace(
            "var GPX_FILE    = 'gpx/YOUR_RIDE_FILENAME.gpx';",
            f"var GPX_FILE    = 'gpx/{gpx_filename}';"
        )

        with open(html_path, 'w') as f:
            f.write(html)

        print(f"  created {html_path}")
        created += 1

    print(f"\n{created} created, {skipped} skipped.")

    # Write embed codes for all HTML files in the trip folder
    all_html = sorted(f for f in os.listdir(trip) if f.endswith('.html'))
    embed_path = os.path.join(trip, 'embed_codes.txt')
    with open(embed_path, 'w') as f:
        for html_filename in all_html:
            url = f"https://tomomiq.github.io/cycling-ripplet/{trip}/{html_filename}"
            f.write(f"{html_filename}\n")
            f.write(f'<iframe src="{url}" width="100%" height="480" frameborder="0" scrolling="no" style="display:block"></iframe>\n')
            f.write("\n")
    print(f"  wrote   {embed_path}")

if __name__ == '__main__':
    main()
