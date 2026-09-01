"""
Weather API Ingestion Module
Fetches real-time meteorological observations from public Weather APIs (e.g. OpenWeatherMap)
and normalizes records into the standardized Hadoop analytics CSV schema.
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

import requests
from ingestion.validator import WeatherRecordValidator

logger = logging.getLogger("weather_ingestion.api")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Default City Coordinates for accurate API querying
CITY_COORDINATES: Dict[str, Dict[str, float]] = {
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Bengaluru": {"lat": 12.9716, "lon": 77.5946},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639},
    "Pune": {"lat": 18.5204, "lon": 73.8567}
}


class WeatherAPIClient:
    """
    Client for acquiring live meteorological observations from external REST APIs
    and normalizing payloads to the project schema.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.openweathermap.org/data/2.5/weather",
        validator: Optional[WeatherRecordValidator] = None
    ):
        self.api_key = api_key or os.getenv("WEATHER_API_KEY", "")
        self.base_url = base_url
        self.validator = validator or WeatherRecordValidator()

    def is_configured(self) -> bool:
        """Check whether a valid API key is present."""
        return bool(self.api_key and self.api_key.strip() and self.api_key != "your_openweather_api_key_here")

    def fetch_city_weather(self, city_name: str) -> Optional[Dict[str, Any]]:
        """
        Fetches current weather for a specific city and maps response to project schema.
        """
        if not self.is_configured():
            logger.warning("Weather API key not configured. Set WEATHER_API_KEY environment variable.")
            return None

        coords = CITY_COORDINATES.get(city_name)
        params = {
            "appid": self.api_key,
            "units": "metric"
        }
        if coords:
            params["lat"] = coords["lat"]
            params["lon"] = coords["lon"]
        else:
            params["q"] = f"{city_name},IN"

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            if response.status_code != 200:
                logger.error("API error for %s: Status %d - %s", city_name, response.status_code, response.text)
                return None

            data = response.json()
            # Normalize OpenWeatherMap response payload
            normalized = self._parse_openweathermap_response(city_name, data)
            is_valid, sanitized, errors = self.validator.validate_record(normalized)
            if not is_valid:
                logger.error("API record validation failed for %s: %s", city_name, "; ".join(errors))
                return None
            return sanitized

        except requests.RequestException as exc:
            logger.error("Network exception querying Weather API for %s: %s", city_name, str(exc))
            return None

    def fetch_all_cities(self, cities: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Fetches observations for all specified cities.
        """
        target_cities = cities or list(CITY_COORDINATES.keys())
        results = []
        for city in target_cities:
            record = self.fetch_city_weather(city)
            if record:
                results.append(record)
        return results

    def _parse_openweathermap_response(self, city_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Maps OpenWeatherMap JSON schema to project schema."""
        main_data = data.get("main", {})
        wind_data = data.get("wind", {})
        rain_data = data.get("rain", {})

        # OpenWeather returns wind speed in m/s (metric) -> convert to km/h (* 3.6)
        wind_speed_ms = float(wind_data.get("speed", 0.0))
        wind_speed_kmh = round(wind_speed_ms * 3.6, 2)

        # Rainfall in last 1 hour if available
        rainfall_mm = float(rain_data.get("1h", rain_data.get("3h", 0.0)))

        return {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
            "city": city_name,
            "temperature": round(float(main_data.get("temp", 0.0)), 2),
            "humidity": round(float(main_data.get("humidity", 0.0)), 2),
            "rainfall": round(rainfall_mm, 2),
            "wind_speed": wind_speed_kmh,
            "pressure": round(float(main_data.get("pressure", 1013.25)), 2)
        }
