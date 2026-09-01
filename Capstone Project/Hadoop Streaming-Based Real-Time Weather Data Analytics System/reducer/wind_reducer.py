#!/usr/bin/env python3
"""
Hadoop Streaming Wind Speed Reducer
Aggregates wind velocity metrics by city to calculate Average Wind Speed, Min Wind Speed,
and Maximum Gust Velocity.

Input (stdin, sorted by city):
    city<TAB>wind_speed
Output (stdout):
    city<TAB>avg_wind_speed<TAB>min_wind_speed<TAB>max_wind_speed<TAB>record_count
"""

import sys


def reduce_wind():
    current_city = None
    wind_sum = 0.0
    wind_min = float("inf")
    wind_max = float("-inf")
    count = 0

    for line in sys.stdin:
        clean_line = line.strip()
        if not clean_line:
            continue

        parts = clean_line.split("\t")
        if len(parts) != 2:
            continue

        city, wind_str = parts[0].strip(), parts[1].strip()

        try:
            wind = float(wind_str)
        except ValueError:
            continue

        if current_city and current_city != city:
            avg_wind = wind_sum / count if count > 0 else 0.0
            print(f"{current_city}\t{avg_wind:.2f}\t{wind_min:.2f}\t{wind_max:.2f}\t{count}")

            wind_sum = 0.0
            wind_min = float("inf")
            wind_max = float("-inf")
            count = 0

        current_city = city
        wind_sum += wind
        wind_min = min(wind_min, wind)
        wind_max = max(wind_max, wind)
        count += 1

    if current_city and count > 0:
        avg_wind = wind_sum / count
        print(f"{current_city}\t{avg_wind:.2f}\t{wind_min:.2f}\t{wind_max:.2f}\t{count}")


if __name__ == "__main__":
    reduce_wind()
