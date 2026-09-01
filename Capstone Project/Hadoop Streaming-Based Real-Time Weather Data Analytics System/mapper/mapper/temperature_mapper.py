#!/usr/bin/env python3
"""
Hadoop Streaming Temperature Mapper
Extracts city and temperature readings from raw CSV weather records.

Input (stdin):
    timestamp,city,temperature,humidity,rainfall,wind_speed,pressure
    Example: 2026-08-18T08:00:00,Chennai,32.5,76,2.4,12.5,1008.2

Output (stdout):
    city<TAB>temperature
    Example: Chennai\t32.5
"""

import sys


def parse_and_map():
    """
    Reads lines from standard input, parses CSV format, validates fields,
    and emits key-value pairs of (city, temperature) to standard output.
    """
    for line in sys.stdin:
        # Strip trailing newline and whitespace
        clean_line = line.strip()
        if not clean_line:
            continue

        # Split comma-delimited record
        fields = [field.strip() for field in clean_line.split(",")]

        # Skip CSV Header row
        if len(fields) >= 3 and fields[0].lower() == "timestamp" and fields[1].lower() == "city":
            continue

        # Verify sufficient column count (at least timestamp, city, temperature)
        if len(fields) < 7:
            # Malformed record with insufficient columns - skip safely
            continue

        city = fields[1]
        temp_str = fields[2]

        if not city:
            continue

        # Numeric conversion with safety checks
        try:
            temp_val = float(temp_str)
            # Physical boundary validation (-50°C to 65°C)
            if -50.0 <= temp_val <= 65.0:
                # Emit Key-Value pair tab-separated for Hadoop Shuffle & Sort
                print(f"{city}\t{temp_val:.2f}")
        except (ValueError, TypeError):
            # Non-numeric or corrupt temperature field - skip record
            continue


if __name__ == "__main__":
    parse_and_map()
