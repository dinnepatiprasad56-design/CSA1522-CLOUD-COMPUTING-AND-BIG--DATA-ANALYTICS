#!/usr/bin/env python3
"""
Hadoop Streaming Temperature Reducer
Aggregates temperature readings by city to calculate Average, Min, and Max temperatures.

Input (stdin, sorted by key from Hadoop Shuffle & Sort):
    city<TAB>temperature
    Example:
        Bengaluru\t18.8
        Bengaluru\t24.5
        Chennai\t27.2
        Chennai\t32.5

Output (stdout):
    city<TAB>avg_temperature<TAB>min_temperature<TAB>max_temperature<TAB>record_count
    Example:
        Bengaluru\t21.65\t18.80\t24.50\t2
        Chennai\t29.85\t27.20\t32.50\t2
"""

import sys


def reduce_temperatures():
    """
    Reads sorted (city, temperature) pairs from stdin, performs key-transition
    aggregation, and emits statistical summaries per city.
    """
    current_city = None
    temp_sum = 0.0
    temp_min = float("inf")
    temp_max = float("-inf")
    count = 0

    for line in sys.stdin:
        clean_line = line.strip()
        if not clean_line:
            continue

        parts = clean_line.split("\t")
        if len(parts) != 2:
            continue

        city, temp_str = parts[0].strip(), parts[1].strip()

        try:
            temp = float(temp_str)
        except ValueError:
            continue

        # Key transition: If city changes, emit aggregated summary for previous city
        if current_city and current_city != city:
            avg_temp = temp_sum / count if count > 0 else 0.0
            print(f"{current_city}\t{avg_temp:.2f}\t{temp_min:.2f}\t{temp_max:.2f}\t{count}")

            # Reset aggregators for new city
            temp_sum = 0.0
            temp_min = float("inf")
            temp_max = float("-inf")
            count = 0

        current_city = city
        temp_sum += temp
        temp_min = min(temp_min, temp)
        temp_max = max(temp_max, temp)
        count += 1

    # Emit final accumulated city after EOF
    if current_city and count > 0:
        avg_temp = temp_sum / count
        print(f"{current_city}\t{avg_temp:.2f}\t{temp_min:.2f}\t{temp_max:.2f}\t{count}")


if __name__ == "__main__":
    reduce_temperatures()
