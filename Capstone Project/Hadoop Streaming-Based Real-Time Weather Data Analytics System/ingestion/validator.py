"""
Weather Record Validation and Sanitization Module
Provides schema validation, range checks, and quarantine handling for raw weather records.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

# Configure logger for ingestion module
logger = logging.getLogger("weather_ingestion.validator")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Physical plausible meteorological boundaries for validation
METEOROLOGICAL_BOUNDS = {
    "temperature": {"min": -50.0, "max": 65.0, "unit": "°C"},
    "humidity": {"min": 0.0, "max": 100.0, "unit": "%"},
    "rainfall": {"min": 0.0, "max": 500.0, "unit": "mm"},
    "wind_speed": {"min": 0.0, "max": 300.0, "unit": "km/h"},
    "pressure": {"min": 850.0, "max": 1100.0, "unit": "hPa"},
}

ALLOWED_CITIES = {
    "Chennai", "Bengaluru", "Hyderabad", "Mumbai", "Delhi", "Kolkata", "Pune"
}

EXPECTED_FIELDS = [
    "timestamp", "city", "temperature", "humidity", "rainfall", "wind_speed", "pressure"
]


class WeatherValidationError(Exception):
    """Custom exception raised when a weather record violates schema or range checks."""
    pass


class WeatherRecordValidator:
    """
    Validates meteorological time-series records against schema, data types,
    and physical meteorological bounds.
    """

    def __init__(self, strict_city_check: bool = False):
        self.strict_city_check = strict_city_check

    def validate_timestamp(self, ts_str: Any) -> Tuple[bool, Optional[str]]:
        """Validate timestamp format (supports ISO-8601 and standard datetime formats)."""
        if not ts_str or not isinstance(ts_str, str):
            return False, "Timestamp is missing or not a string"
        
        # Supported format variations
        formats = [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d"
        ]
        for fmt in formats:
            try:
                datetime.strptime(ts_str.strip(), fmt)
                return True, None
            except ValueError:
                continue
        return False, f"Invalid timestamp format '{ts_str}'. Expected ISO-8601 (e.g. YYYY-MM-DDTHH:MM:SS)"

    def validate_city(self, city: Any) -> Tuple[bool, Optional[str]]:
        """Validate city name string and optionally check against supported city registry."""
        if not city or not isinstance(city, str) or not city.strip():
            return False, "City name is empty or not a string"
        
        cleaned_city = city.strip()
        if self.strict_city_check and cleaned_city not in ALLOWED_CITIES:
            return False, f"City '{cleaned_city}' is not in configured allowed cities: {sorted(list(ALLOWED_CITIES))}"
        return True, None

    def validate_numeric_field(self, field_name: str, value: Any) -> Tuple[bool, Optional[float], Optional[str]]:
        """Validate numeric conversions and physical meteorological boundaries."""
        if value is None or (isinstance(value, str) and not value.strip()):
            return False, None, f"Field '{field_name}' is missing or empty"
        
        try:
            num_val = float(value)
        except (ValueError, TypeError):
            return False, None, f"Field '{field_name}' value '{value}' cannot be converted to float"
        
        # Check meteorological bounds
        bounds = METEOROLOGICAL_BOUNDS.get(field_name)
        if bounds:
            if num_val < bounds["min"] or num_val > bounds["max"]:
                return False, None, (
                    f"Field '{field_name}' value {num_val}{bounds['unit']} is outside plausible bounds "
                    f"[{bounds['min']}, {bounds['max']}]"
                )
        
        return True, num_val, None

    def validate_record(self, record: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]], List[str]]:
        """
        Validate a single dictionary weather record.
        Returns (is_valid, sanitized_record, list_of_errors).
        """
        errors: List[str] = []
        if not isinstance(record, dict):
            return False, None, ["Record must be a dictionary"]

        sanitized: Dict[str, Any] = {}

        # 1. Validate Timestamp
        ts_valid, ts_err = self.validate_timestamp(record.get("timestamp"))
        if not ts_valid:
            errors.append(ts_err or "Invalid timestamp")
        else:
            sanitized["timestamp"] = str(record["timestamp"]).strip()

        # 2. Validate City
        city_valid, city_err = self.validate_city(record.get("city"))
        if not city_valid:
            errors.append(city_err or "Invalid city")
        else:
            sanitized["city"] = str(record["city"]).strip()

        # 3. Validate Numeric Weather Metrics
        numeric_fields = ["temperature", "humidity", "rainfall", "wind_speed", "pressure"]
        for field in numeric_fields:
            is_valid, num_val, num_err = self.validate_numeric_field(field, record.get(field))
            if not is_valid:
                errors.append(num_err or f"Invalid {field}")
            else:
                sanitized[field] = round(num_val, 2)

        if errors:
            return False, None, errors
        return True, sanitized, []

    def validate_csv_line(self, csv_line: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Parses and validates a raw comma-delimited CSV record line.
        """
        if not csv_line or not csv_line.strip():
            return False, None, "Empty CSV line"

        parts = [p.strip() for p in csv_line.strip().split(",")]
        
        # Skip header line if encountered
        if parts[0].lower() == "timestamp" and parts[1].lower() == "city":
            return False, None, "HEADER_ROW"

        if len(parts) != len(EXPECTED_FIELDS):
            return False, None, f"Malformed line: expected {len(EXPECTED_FIELDS)} columns, got {len(parts)} (Raw: '{csv_line.strip()}')"

        raw_dict = {
            "timestamp": parts[0],
            "city": parts[1],
            "temperature": parts[2],
            "humidity": parts[3],
            "rainfall": parts[4],
            "wind_speed": parts[5],
            "pressure": parts[6]
        }

        is_valid, sanitized, errors = self.validate_record(raw_dict)
        if not is_valid:
            return False, None, "; ".join(errors)
        return True, sanitized, None

    def sanitize_and_filter(
        self, records: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Process a batch of records, separating valid clean records from quarantined malformed records.
        """
        valid_records: List[Dict[str, Any]] = []
        quarantined: List[Dict[str, Any]] = []

        for idx, rec in enumerate(records):
            is_valid, sanitized, errors = self.validate_record(rec)
            if is_valid and sanitized is not None:
                valid_records.append(sanitized)
            else:
                quarantine_entry = {
                    "index": idx,
                    "raw_record": rec,
                    "errors": errors,
                    "quarantine_timestamp": datetime.utcnow().isoformat()
                }
                quarantined.append(quarantine_entry)
                logger.warning("Quarantined malformed record #%d: %s (Record: %s)", idx, "; ".join(errors), rec)

        return valid_records, quarantined
