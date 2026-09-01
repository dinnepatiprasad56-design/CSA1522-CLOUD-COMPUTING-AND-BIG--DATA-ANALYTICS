#!/usr/bin/env python3
"""
Hadoop Streaming Master Weather Analytics Mapper
Parses full meteorological records, validates all 5 core weather metrics,
and emits tab-separated city partitions with complete parameter payloads.

Input (stdin):
    timestamp,city,temperature,humidity,rainfall,wind_speed,pressure
Output (stdout):
    city<TAB>timestamp,temperature,humidity,rainfall,wind_speed,pressure
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

        if len(fields) != 7:
            continue

        ts, city, temp_s, hum_s, rain_s, wind_s, press_s = fields

        if not city or not ts:
            continue

        # Strict multi-attribute numeric parsing and physical bound validation
        try:
            temp = float(temp_s)
            hum = float(hum_s)
            rain = float(rain_s)
            wind = float(wind_s)
            press = float(press_s)

            if not (-50.0 <= temp <= 65.0):
                continue
            if not (0.0 <= hum <= 100.0):
                continue
            if not (0.0 <= rain <= 500.0):
                continue
            if not (0.0 <= wind <= 300.0):
                continue
            if not (850.0 <= press <= 1100.0):
                continue

            # Emit clean city key and formatted metric tuple
            print(f"{city}\t{ts},{temp:.2f},{hum:.2f},{rain:.2f},{wind:.2f},{press:.2f}")

        except (ValueError, TypeError):
            continue


if __name__ == "__main__":
    parse_and_map()
