"""
Weather Data Generator Module
Generates realistic multi-city meteorological time-series records for cloud HDFS ingestion
and Hadoop Streaming MapReduce processing.
"""

import os
import csv
import time
import math
import random
import logging
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Generator, Any

from ingestion.validator import WeatherRecordValidator

# Setup Module Logging
logger = logging.getLogger("weather_ingestion.generator")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Meteorological Climate Profiles for Indian Metros
CITY_PROFILES: Dict[str, Dict[str, float]] = {
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

CSV_FIELDNAMES = ["timestamp", "city", "temperature", "humidity", "rainfall", "wind_speed", "pressure"]


class WeatherDataGenerator:
    """
    Simulates real-world weather sensor streams across target cities with
    realistic diurnal cycles, elevation-adjusted barometric pressure, and stochastic anomaly injection.
    """

    def __init__(
        self,
        cities: Optional[List[str]] = None,
        anomaly_ratio: float = 0.05,
        validator: Optional[WeatherRecordValidator] = None
    ):
        self.cities = cities or list(CITY_PROFILES.keys())
        self.anomaly_ratio = anomaly_ratio
        self.validator = validator or WeatherRecordValidator()
        logger.info("WeatherDataGenerator initialized for cities: %s (Anomaly ratio: %.2f)", self.cities, self.anomaly_ratio)

    def generate_single_record(self, city: str, dt: Optional[datetime] = None, force_anomaly: bool = False) -> Dict[str, Any]:
        """
        Synthesizes a single meteorological observation record.
        """
        if city not in CITY_PROFILES:
            raise ValueError(f"City '{city}' not recognized in CITY_PROFILES")

        dt = dt or datetime.now()
        profile = CITY_PROFILES[city]
        hour_fraction = dt.hour + (dt.minute / 60.0) + (dt.second / 3600.0)

        # Diurnal solar cycle calculation (Peak heat ~14:00, Minimum ~05:00)
        solar_factor = math.sin(math.radians((hour_fraction - 8) * 15))

        # Base calculations
        temp = profile["base_temp"] + (solar_factor * profile["temp_range"]) + random.uniform(-0.8, 0.8)
        # Humidity inverse variation with diurnal temperature
        humidity = profile["base_humidity"] - (solar_factor * profile["humidity_range"]) + random.uniform(-2.5, 2.5)
        humidity = max(10.0, min(99.0, humidity))

        # Wind variations
        wind = profile["wind_base"] + (solar_factor * 2.5) + random.uniform(-2.5, 3.5)
        wind = max(0.5, wind)

        # Barometric pressure (Semi-diurnal atmospheric tidal wave)
        pressure = profile["base_pressure"] + (math.cos(math.radians(hour_fraction * 30)) * 1.2) + random.uniform(-0.4, 0.4)

        # Precipitation model
        rainfall = 0.0
        if random.random() < profile["rain_prob"]:
            rainfall = round(random.expovariate(1.0 / profile["rain_scale"]), 1)
            if rainfall < 0.2:
                rainfall = 0.0

        # Optional Anomaly Injection
        is_anomaly = force_anomaly or (random.random() < self.anomaly_ratio)
        if is_anomaly:
            anomaly_type = random.choice(["HEATWAVE", "CYCLONE", "FLOOD_RAIN", "COLDWAVE", "GALE_WIND"])
            if anomaly_type == "HEATWAVE":
                temp = random.uniform(42.5, 47.0)
                humidity = random.uniform(15.0, 28.0)
                rainfall = 0.0
            elif anomaly_type == "CYCLONE":
                pressure = profile["base_pressure"] - random.uniform(25.0, 38.0)
                wind = random.uniform(55.0, 75.0)
                rainfall = random.uniform(30.0, 75.0)
                humidity = random.uniform(92.0, 98.0)
            elif anomaly_type == "FLOOD_RAIN":
                rainfall = random.uniform(65.0, 105.0)
                humidity = random.uniform(90.0, 99.0)
            elif anomaly_type == "COLDWAVE":
                temp = random.uniform(5.0, 10.0)
            elif anomaly_type == "GALE_WIND":
                wind = random.uniform(50.0, 65.0)

        record = {
            "timestamp": dt.strftime("%Y-%m-%dT%H:%M:%S"),
            "city": city,
            "temperature": round(temp, 2),
            "humidity": round(humidity, 2),
            "rainfall": round(rainfall, 2),
            "wind_speed": round(wind, 2),
            "pressure": round(pressure, 2)
        }
        return record

    def generate_city_batch(self, dt: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Generates one observation record for every configured city simultaneously.
        """
        current_time = dt or datetime.now()
        raw_records = [self.generate_single_record(city, current_time) for city in self.cities]
        valid_records, quarantined = self.validator.sanitize_and_filter(raw_records)
        if quarantined:
            logger.warning("%d records quarantined during batch generation", len(quarantined))
        return valid_records

    def write_batch_to_csv(self, records: List[Dict[str, Any]], output_filepath: str) -> str:
        """
        Writes a list of weather records to a target CSV file with headers.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
        with open(output_filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()
            writer.writerows(records)
        logger.info("Saved %d weather records to '%s'", len(records), output_filepath)
        return output_filepath

    def stream_batches(
        self,
        interval_seconds: float = 5.0,
        total_batches: Optional[int] = None,
        output_dir: str = os.path.join("data", "generated")
    ) -> Generator[str, None, None]:
        """
        Continuously yields and saves micro-batches of weather data at configurable intervals.
        """
        os.makedirs(output_dir, exist_ok=True)
        batch_idx = 0

        logger.info(
            "Starting weather data streaming: interval=%.1fs, total_batches=%s, output_dir=%s",
            interval_seconds, str(total_batches) if total_batches else "INFINITE", output_dir
        )

        try:
            while total_batches is None or batch_idx < total_batches:
                batch_idx += 1
                now = datetime.now()
                batch_records = self.generate_city_batch(now)
                
                timestamp_str = now.strftime("%Y%m%d_%H%M%S")
                filename = f"weather_batch_{timestamp_str}_{batch_idx:04d}.csv"
                filepath = os.path.join(output_dir, filename)
                
                self.write_batch_to_csv(batch_records, filepath)
                yield filepath

                if total_batches is None or batch_idx < total_batches:
                    time.sleep(interval_seconds)

        except KeyboardInterrupt:
            logger.info("Weather streaming generation interrupted by user.")


def main():
    """Command Line Interface for Weather Data Ingestion Generator."""
    parser = argparse.ArgumentParser(description="Weather Data Generator for Cloud Hadoop Ingestion")
    parser.add_argument("--interval", type=float, default=2.0, help="Interval between batches in seconds")
    parser.add_argument("--batches", type=int, default=5, help="Total number of micro-batches to generate")
    parser.add_argument("--records", type=int, default=None, help="Generate a single static dataset with N records")
    parser.add_argument("--output-dir", type=str, default=os.path.join("data", "generated"), help="Directory for batch CSVs")
    parser.add_argument("--output-file", type=str, default=None, help="Specific file path for single dataset generation")
    parser.add_argument("--anomaly-ratio", type=float, default=0.08, help="Anomaly injection probability (0.0 - 1.0)")

    args = parser.parse_args()
    generator = WeatherDataGenerator(anomaly_ratio=args.anomaly_ratio)

    if args.records and args.records > 0:
        # Static bulk dataset generation mode
        logger.info("Generating static dataset with %d records...", args.records)
        records = []
        base_time = datetime.now() - timedelta(hours=args.records // len(generator.cities))
        for i in range(args.records):
            city = generator.cities[i % len(generator.cities)]
            record_time = base_time + timedelta(minutes=i * 5)
            records.append(generator.generate_single_record(city, record_time))
        
        valid_recs, _ = generator.validator.sanitize_and_filter(records)
        target_file = args.output_file or os.path.join(args.output_dir, "weather_bulk_dataset.csv")
        generator.write_batch_to_csv(valid_recs, target_file)
        print(f"Generated {len(valid_recs)} records in '{target_file}'")
    else:
        # Streaming batch mode
        logger.info("Generating %d streaming micro-batches at %.1fs intervals...", args.batches, args.interval)
        for saved_path in generator.stream_batches(
            interval_seconds=args.interval,
            total_batches=args.batches,
            output_dir=args.output_dir
        ):
            print(f"Generated Batch: {saved_path}")


if __name__ == "__main__":
    main()
