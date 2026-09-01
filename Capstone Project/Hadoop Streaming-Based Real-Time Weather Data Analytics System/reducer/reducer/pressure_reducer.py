#!/usr/bin/env python3
"""
Hadoop Streaming Atmospheric Pressure Reducer
Aggregates barometric pressure readings by city to calculate Average, Minimum,
and Maximum Pressure (hPa).

Input (stdin, sorted by city):
    city<TAB>pressure
Output (stdout):
    city<TAB>avg_pressure<TAB>min_pressure<TAB>max_pressure<TAB>record_count
"""

import sys


def reduce_pressure():
    current_city = None
    pressure_sum = 0.0
    pressure_min = float("inf")
    pressure_max = float("-inf")
    count = 0

    for line in sys.stdin:
        clean_line = line.strip()
        if not clean_line:
            continue

        parts = clean_line.split("\t")
        if len(parts) != 2:
            continue

        city, press_str = parts[0].strip(), parts[1].strip()

        try:
            pressure = float(press_str)
        except ValueError:
            continue

        if current_city and current_city != city:
            avg_press = pressure_sum / count if count > 0 else 0.0
            print(f"{current_city}\t{avg_press:.2f}\t{pressure_min:.2f}\t{pressure_max:.2f}\t{count}")

            pressure_sum = 0.0
            pressure_min = float("inf")
            pressure_max = float("-inf")
            count = 0

        current_city = city
        pressure_sum += pressure
        pressure_min = min(pressure_min, pressure)
        pressure_max = max(pressure_max, pressure)
        count += 1

    if current_city and count > 0:
        avg_press = pressure_sum / count
        print(f"{current_city}\t{avg_press:.2f}\t{pressure_min:.2f}\t{pressure_max:.2f}\t{count}")


if __name__ == "__main__":
    reduce_pressure()
