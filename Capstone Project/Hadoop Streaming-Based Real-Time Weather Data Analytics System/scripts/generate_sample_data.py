"""
Sample Weather Dataset Generator
Generates realistic multi-city, time-series meteorological records for Hadoop Streaming processing.
"""

import os
import csv
import math
import random
from datetime import datetime, timedelta

# Target Cities and their climatological base attributes
# (Elevation/geography influences baseline pressure, temp, and humidity)
CITY_PROFILES = {
    "Chennai": {
        "base_temp": 32.0, "temp_range": 4.5, "base_humidity": 76.0, "humidity_range": 12.0,
        "base_pressure": 1008.5, "wind_base": 14.0, "rain_prob": 0.25, "rain_scale": 15.0
    },
    "Bengaluru": {
        "base_temp": 24.5, "temp_range": 5.0, "base_humidity": 62.0, "humidity_range": 18.0,
        "base_pressure": 915.0, "wind_base": 12.0, "rain_prob": 0.30, "rain_scale": 12.0
    },
    "Hyderabad": {
        "base_temp": 29.5, "temp_range": 6.0, "base_humidity": 58.0, "humidity_range": 16.0,
        "base_pressure": 955.0, "wind_base": 11.0, "rain_prob": 0.20, "rain_scale": 10.0
    },
    "Mumbai": {
        "base_temp": 30.5, "temp_range": 3.5, "base_humidity": 82.0, "humidity_range": 10.0,
        "base_pressure": 1010.0, "wind_base": 16.0, "rain_prob": 0.40, "rain_scale": 25.0
    },
    "Delhi": {
        "base_temp": 35.0, "temp_range": 8.5, "base_humidity": 45.0, "humidity_range": 22.0,
        "base_pressure": 982.0, "wind_base": 10.0, "rain_prob": 0.15, "rain_scale": 8.0
    },
    "Kolkata": {
        "base_temp": 31.5, "temp_range": 4.0, "base_humidity": 80.0, "humidity_range": 14.0,
        "base_pressure": 1006.5, "wind_base": 13.0, "rain_prob": 0.35, "rain_scale": 18.0
    },
    "Pune": {
        "base_temp": 27.0, "temp_range": 5.5, "base_humidity": 64.0, "humidity_range": 15.0,
        "base_pressure": 950.0, "wind_base": 13.5, "rain_prob": 0.28, "rain_scale": 12.0
    }
}


def generate_record(city: str, dt: datetime, inject_anomaly: bool = False) -> dict:
    """Generate a single weather record with realistic diurnal patterns and optional anomalies."""
    profile = CITY_PROFILES[city]
    hour = dt.hour + (dt.minute / 60.0)

    # Diurnal solar cycle simulation (peak temp ~ 14:00, lowest ~ 05:00)
    solar_factor = math.sin(math.radians((hour - 8) * 15))

    # Base values with diurnal oscillation
    temp = profile["base_temp"] + (solar_factor * profile["temp_range"]) + random.uniform(-1.0, 1.0)
    # Humidity has inverse relationship with temperature
    humidity = profile["base_humidity"] - (solar_factor * profile["humidity_range"]) + random.uniform(-3.0, 3.0)
    humidity = max(10.0, min(100.0, humidity))

    # Wind variation
    wind = profile["wind_base"] + (solar_factor * 3.0) + random.uniform(-3.0, 4.0)
    wind = max(1.0, wind)

    # Pressure variation (subtle tidal barometric oscillation)
    pressure = profile["base_pressure"] + (math.cos(math.radians(hour * 30)) * 1.5) + random.uniform(-0.5, 0.5)

    # Rainfall simulation
    rainfall = 0.0
    if random.random() < profile["rain_prob"]:
        rainfall = round(random.expovariate(1.0 / profile["rain_scale"]), 1)
        if rainfall < 0.2:
            rainfall = 0.0

    # Inject specific anomalies for capstone demonstration / testing
    if inject_anomaly:
        anomaly_type = random.choice(["HEATWAVE", "CYCLONE", "FLOOD_RAIN", "COLDWAVE", "GALE_WIND"])
        if anomaly_type == "HEATWAVE":
            temp = random.uniform(43.0, 47.5)
            humidity = random.uniform(15.0, 30.0)
            rainfall = 0.0
        elif anomaly_type == "CYCLONE":
            pressure = profile["base_pressure"] - random.uniform(25.0, 40.0)
            wind = random.uniform(55.0, 75.0)
            rainfall = random.uniform(35.0, 80.0)
            humidity = random.uniform(92.0, 99.0)
        elif anomaly_type == "FLOOD_RAIN":
            rainfall = random.uniform(65.0, 110.0)
            humidity = random.uniform(90.0, 100.0)
        elif anomaly_type == "COLDWAVE":
            temp = random.uniform(4.0, 9.5)
        elif anomaly_type == "GALE_WIND":
            wind = random.uniform(50.0, 68.0)

    return {
        "timestamp": dt.strftime("%Y-%m-%dT%H:%M:%S"),
        "city": city,
        "temperature": round(temp, 1),
        "humidity": round(humidity, 1),
        "rainfall": round(rainfall, 1),
        "wind_speed": round(wind, 1),
        "pressure": round(pressure, 1)
    }


def generate_dataset(output_path: str, days: int = 7, interval_hours: int = 1, anomaly_ratio: float = 0.05) -> int:
    """Generate a full historical sample dataset spanning multiple days across all cities."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    start_time = datetime(2026, 8, 11, 0, 0, 0)
    total_steps = (days * 24) // interval_hours

    records = []
    for step in range(total_steps):
        current_dt = start_time + timedelta(hours=step * interval_hours)
        for city in CITY_PROFILES.keys():
            is_anomaly = random.random() < anomaly_ratio
            record = generate_record(city, current_dt, inject_anomaly=is_anomaly)
            records.append(record)

    fieldnames = ["timestamp", "city", "temperature", "humidity", "rainfall", "wind_speed", "pressure"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    return len(records)


if __name__ == "__main__":
    random.seed(42)  # Deterministic seed for reproducible sample dataset
    out_file = os.path.join("data", "sample", "sample_weather_data.csv")
    count = generate_dataset(out_file, days=7, interval_hours=1, anomaly_ratio=0.06)
    print(f"Successfully generated {count} weather records in '{out_file}'.")
