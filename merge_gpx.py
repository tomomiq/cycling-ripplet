#!/usr/bin/env python3
"""
Usage: python3 merge_gpx.py <trip_folder>
Example: python3 merge_gpx.py 2025_Western_Alps

Merges all GPX files in <trip_folder>/gpx/ into a single full_trip.gpx.
Skips full_trip.gpx itself if it already exists. Safe to re-run.
"""

import sys
import os
import re

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

if __name__ == '__main__':
    main()
