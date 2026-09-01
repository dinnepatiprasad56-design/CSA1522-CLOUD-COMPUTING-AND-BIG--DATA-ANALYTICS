#!/usr/bin/env python3
"""
Hadoop Streaming Rainfall Mapper
Extracts city and precipitation/rainfall (mm) from raw CSV weather records.

Input (stdin):
    timestamp,city,temperature,humidity,rainfall,wind_speed,pressure
Output (stdout):
    city<TAB>rainfall
"""

import sys


def parse_and_map():
    for line in sys.stdin:
        clean_line = line.strip()
        if not clean_line:
            continue

        fields = [f.strip() for f in clean_line.split(",")]

        # Header skip
        if len(fields) >= 5 and fields[0].lower() == "timestamp" and fields[1].lower() == "city":
            continue

        if len(fields) < 7:
            continue

        city = fields[1]
        rainfall_str = fields[4]

        if not city:
            continue

        try:
            rainfall_val = float(rainfall_str)
            # Physical boundary validation (0.0 to 500.0 mm)
            if 0.0 <= rainfall_val <= 500.0:
                print(f"{city}\t{rainfall_val:.2f}")
        except (ValueError, TypeError):
            continue


if __name__ == "__main__":
    parse_and_map()
