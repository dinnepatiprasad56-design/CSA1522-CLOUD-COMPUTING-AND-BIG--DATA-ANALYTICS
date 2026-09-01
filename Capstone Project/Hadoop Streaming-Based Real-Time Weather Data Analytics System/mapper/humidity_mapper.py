#!/usr/bin/env python3
"""
Hadoop Streaming Humidity Mapper
Extracts city and relative humidity (%) from raw CSV weather records.

Input (stdin):
    timestamp,city,temperature,humidity,rainfall,wind_speed,pressure
Output (stdout):
    city<TAB>humidity
"""

import sys


def parse_and_map():
    for line in sys.stdin:
        clean_line = line.strip()
        if not clean_line:
            continue

        fields = [f.strip() for f in clean_line.split(",")]

        # Header skip
        if len(fields) >= 4 and fields[0].lower() == "timestamp" and fields[1].lower() == "city":
            continue

        if len(fields) < 7:
            continue

        city = fields[1]
        humidity_str = fields[3]

        if not city:
            continue

        try:
            humidity_val = float(humidity_str)
            # Physical boundary validation (0% to 100%)
            if 0.0 <= humidity_val <= 100.0:
                print(f"{city}\t{humidity_val:.2f}")
        except (ValueError, TypeError):
            continue


if __name__ == "__main__":
    parse_and_map()
