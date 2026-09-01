#!/usr/bin/env python3
"""
Hadoop Streaming Rainfall Reducer
Aggregates precipitation metrics by city to calculate Total Rainfall, Max Rainfall Event,
Average Rainfall, and Wet Period Frequency.

Input (stdin, sorted by city):
    city<TAB>rainfall
Output (stdout):
    city<TAB>total_rainfall<TAB>max_rainfall<TAB>avg_rainfall<TAB>rain_events_count<TAB>total_records
"""

import sys


def reduce_rainfall():
    current_city = None
    total_rainfall = 0.0
    max_rainfall = 0.0
    rain_events = 0
    total_records = 0

    for line in sys.stdin:
        clean_line = line.strip()
        if not clean_line:
            continue

        parts = clean_line.split("\t")
        if len(parts) != 2:
            continue

        city, rain_str = parts[0].strip(), parts[1].strip()

        try:
            rainfall = float(rain_str)
        except ValueError:
            continue

        if current_city and current_city != city:
            avg_rain = total_rainfall / total_records if total_records > 0 else 0.0
            print(f"{current_city}\t{total_rainfall:.2f}\t{max_rainfall:.2f}\t{avg_rain:.2f}\t{rain_events}\t{total_records}")

            total_rainfall = 0.0
            max_rainfall = 0.0
            rain_events = 0
            total_records = 0

        current_city = city
        total_rainfall += rainfall
        max_rainfall = max(max_rainfall, rainfall)
        if rainfall > 0.0:
            rain_events += 1
        total_records += 1

    if current_city and total_records > 0:
        avg_rain = total_rainfall / total_records
        print(f"{current_city}\t{total_rainfall:.2f}\t{max_rainfall:.2f}\t{avg_rain:.2f}\t{rain_events}\t{total_records}")


if __name__ == "__main__":
    reduce_rainfall()
