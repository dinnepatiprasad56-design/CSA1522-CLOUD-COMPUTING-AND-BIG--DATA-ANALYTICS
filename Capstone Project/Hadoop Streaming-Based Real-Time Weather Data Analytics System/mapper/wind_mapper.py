#!/usr/bin/env python3
"""
Hadoop Streaming Wind Speed Mapper
Extracts city and wind speed (km/h) from raw CSV weather records.

Input (stdin):
    timestamp,city,temperature,humidity,rainfall,wind_speed,pressure
Output (stdout):
    city<TAB>wind_speed
"""

import sys


def parse_and_map():
    for line in sys.stdin:
        clean_line = line.strip()
        if not clean_line:
            continue

        fields = [f.strip() for f in clean_line.split(",")]

        # Header skip
        if len(fields) >= 6 and fields[0].lower() == "timestamp" and fields[1].lower() == "city":
            continue

        if len(fields) < 7:
            continue

        city = fields[1]
        wind_str = fields[5]

        if not city:
            continue

        try:
            wind_val = float(wind_str)
            # Physical boundary validation (0.0 to 300.0 km/h)
            if 0.0 <= wind_val <= 300.0:
                print(f"{city}\t{wind_val:.2f}")
        except (ValueError, TypeError):
            continue


if __name__ == "__main__":
    parse_and_map()
