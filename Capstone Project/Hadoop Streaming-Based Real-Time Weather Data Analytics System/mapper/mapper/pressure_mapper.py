#!/usr/bin/env python3
"""
Hadoop Streaming Atmospheric Pressure Mapper
Extracts city and barometric pressure (hPa) from raw CSV weather records.

Input (stdin):
    timestamp,city,temperature,humidity,rainfall,wind_speed,pressure
Output (stdout):
    city<TAB>pressure
"""

import sys


def parse_and_map():
    for line in sys.stdin:
        clean_line = line.strip()
        if not clean_line:
            continue

        fields = [f.strip() for f in clean_line.split(",")]

        # Header skip
        if len(fields) >= 7 and fields[0].lower() == "timestamp" and fields[1].lower() == "city":
            continue

        if len(fields) < 7:
            continue

        city = fields[1]
        pressure_str = fields[6]

        if not city:
            continue

        try:
            pressure_val = float(pressure_str)
            # Physical boundary validation (850.0 to 1100.0 hPa)
            if 850.0 <= pressure_val <= 1100.0:
                print(f"{city}\t{pressure_val:.2f}")
        except (ValueError, TypeError):
            continue


if __name__ == "__main__":
    parse_and_map()
