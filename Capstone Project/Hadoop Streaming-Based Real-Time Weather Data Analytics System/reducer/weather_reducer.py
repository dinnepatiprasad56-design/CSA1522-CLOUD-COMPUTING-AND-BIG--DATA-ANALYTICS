#!/usr/bin/env python3
"""
Hadoop Streaming Master Weather Analytics & Anomaly Reducer
Performs multi-metric statistical aggregation and anomaly event detection across all weather variables.

Input (stdin, sorted by city):
    city<TAB>timestamp,temperature,humidity,rainfall,wind_speed,pressure
Output (stdout):
    city<TAB>records<TAB>avg_temp<TAB>min_temp<TAB>max_temp<TAB>avg_hum<TAB>min_hum<TAB>max_hum<TAB>total_rain<TAB>max_rain<TAB>avg_wind<TAB>max_wind<TAB>avg_press<TAB>min_press<TAB>anomalies_count
"""

import sys


def is_anomaly(temp: float, hum: float, rain: float, wind: float, press: float) -> bool:
    """Evaluates whether a single meteorological observation meets extreme weather criteria."""
    if temp >= 42.0 or temp <= 8.0:
        return True
    if rain >= 50.0:
        return True
    if wind >= 50.0:
        return True
    if press <= 980.0 and (wind >= 40.0 or rain >= 25.0):
        return True
    return False


def reduce_all_metrics():
    current_city = None
    records_count = 0
    temp_sum = 0.0
    temp_min = float("inf")
    temp_max = float("-inf")

    hum_sum = 0.0
    hum_min = float("inf")
    hum_max = float("-inf")

    rain_sum = 0.0
    rain_max = 0.0

    wind_sum = 0.0
    wind_max = 0.0

    press_sum = 0.0
    press_min = float("inf")
    press_max = float("-inf")

    anomalies_count = 0

    def emit_summary(city: str):
        avg_temp = temp_sum / records_count
        avg_hum = hum_sum / records_count
        avg_wind = wind_sum / records_count
        avg_press = press_sum / records_count
        print(
            f"{city}\t{records_count}\t{avg_temp:.2f}\t{temp_min:.2f}\t{temp_max:.2f}\t"
            f"{avg_hum:.2f}\t{hum_min:.2f}\t{hum_max:.2f}\t{rain_sum:.2f}\t{rain_max:.2f}\t"
            f"{avg_wind:.2f}\t{wind_max:.2f}\t{avg_press:.2f}\t{press_min:.2f}\t{anomalies_count}"
        )

    for line in sys.stdin:
        clean_line = line.strip()
        if not clean_line:
            continue

        parts = clean_line.split("\t")
        if len(parts) != 2:
            continue

        city, payload = parts[0].strip(), parts[1].strip()
        tokens = payload.split(",")
        if len(tokens) != 6:
            continue

        ts, temp_s, hum_s, rain_s, wind_s, press_s = tokens

        try:
            temp = float(temp_s)
            hum = float(hum_s)
            rain = float(rain_s)
            wind = float(wind_s)
            press = float(press_s)
        except ValueError:
            continue

        # Key Transition
        if current_city and current_city != city:
            emit_summary(current_city)

            # Reset aggregators
            records_count = 0
            temp_sum = 0.0
            temp_min = float("inf")
            temp_max = float("-inf")
            hum_sum = 0.0
            hum_min = float("inf")
            hum_max = float("-inf")
            rain_sum = 0.0
            rain_max = 0.0
            wind_sum = 0.0
            wind_max = 0.0
            press_sum = 0.0
            press_min = float("inf")
            press_max = float("-inf")
            anomalies_count = 0

        current_city = city
        records_count += 1
        temp_sum += temp
        temp_min = min(temp_min, temp)
        temp_max = max(temp_max, temp)

        hum_sum += hum
        hum_min = min(hum_min, hum)
        hum_max = max(hum_max, hum)

        rain_sum += rain
        rain_max = max(rain_max, rain)

        wind_sum += wind
        wind_max = max(wind_max, wind)

        press_sum += press
        press_min = min(press_min, press)
        press_max = max(press_max, press)

        if is_anomaly(temp, hum, rain, wind, press):
            anomalies_count += 1

    if current_city and records_count > 0:
        emit_summary(current_city)


if __name__ == "__main__":
    reduce_all_metrics()
