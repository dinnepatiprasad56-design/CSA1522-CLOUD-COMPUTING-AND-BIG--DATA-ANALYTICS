#!/usr/bin/env python3
"""
Hadoop Streaming Humidity Reducer
Aggregates relative humidity readings by city to calculate Average, Min, and Max humidity.

Input (stdin, sorted by city):
    city<TAB>humidity
Output (stdout):
    city<TAB>avg_humidity<TAB>min_humidity<TAB>max_humidity<TAB>record_count
"""

import sys


def reduce_humidity():
    current_city = None
    humidity_sum = 0.0
    humidity_min = float("inf")
    humidity_max = float("-inf")
    count = 0

    for line in sys.stdin:
        clean_line = line.strip()
        if not clean_line:
            continue

        parts = clean_line.split("\t")
        if len(parts) != 2:
            continue

        city, humidity_str = parts[0].strip(), parts[1].strip()

        try:
            humidity = float(humidity_str)
        except ValueError:
            continue

        if current_city and current_city != city:
            avg_humidity = humidity_sum / count if count > 0 else 0.0
            print(f"{current_city}\t{avg_humidity:.2f}\t{humidity_min:.2f}\t{humidity_max:.2f}\t{count}")

            humidity_sum = 0.0
            humidity_min = float("inf")
            humidity_max = float("-inf")
            count = 0

        current_city = city
        humidity_sum += humidity
        humidity_min = min(humidity_min, humidity)
        humidity_max = max(humidity_max, humidity)
        count += 1

    if current_city and count > 0:
        avg_humidity = humidity_sum / count
        print(f"{current_city}\t{avg_humidity:.2f}\t{humidity_min:.2f}\t{humidity_max:.2f}\t{count}")


if __name__ == "__main__":
    reduce_humidity()
