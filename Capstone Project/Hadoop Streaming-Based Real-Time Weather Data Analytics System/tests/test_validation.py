"""
Unit Tests for Weather Record Validation and Sanitization Module
"""

import pytest
from ingestion.validator import WeatherRecordValidator, METEOROLOGICAL_BOUNDS, ALLOWED_CITIES


@pytest.fixture
def validator():
    return WeatherRecordValidator(strict_city_check=True)


@pytest.fixture
def valid_record():
    return {
        "timestamp": "2026-08-18T08:00:00",
        "city": "Chennai",
        "temperature": 32.5,
        "humidity": 76.0,
        "rainfall": 2.4,
        "wind_speed": 12.5,
        "pressure": 1008.2
    }


def test_valid_record_passes(validator, valid_record):
    is_valid, sanitized, errors = validator.validate_record(valid_record)
    assert is_valid is True
    assert errors == []
    assert sanitized is not None
    assert sanitized["city"] == "Chennai"
    assert sanitized["temperature"] == 32.5
    assert sanitized["humidity"] == 76.0
    assert sanitized["rainfall"] == 2.4
    assert sanitized["wind_speed"] == 12.5
    assert sanitized["pressure"] == 1008.2


def test_missing_timestamp(validator, valid_record):
    del valid_record["timestamp"]
    is_valid, sanitized, errors = validator.validate_record(valid_record)
    assert is_valid is False
    assert sanitized is None
    assert any("Timestamp is missing" in err for err in errors)


def test_invalid_timestamp_format(validator, valid_record):
    valid_record["timestamp"] = "invalid-date-string"
    is_valid, sanitized, errors = validator.validate_record(valid_record)
    assert is_valid is False
    assert any("Invalid timestamp format" in err for err in errors)


def test_empty_city(validator, valid_record):
    valid_record["city"] = "   "
    is_valid, sanitized, errors = validator.validate_record(valid_record)
    assert is_valid is False
    assert any("City name is empty" in err for err in errors)


def test_strict_city_check_unallowed_city(validator, valid_record):
    valid_record["city"] = "Tokyo"
    is_valid, sanitized, errors = validator.validate_record(valid_record)
    assert is_valid is False
    assert any("not in configured allowed cities" in err for err in errors)


def test_non_numeric_temperature(validator, valid_record):
    valid_record["temperature"] = "hot_day"
    is_valid, sanitized, errors = validator.validate_record(valid_record)
    assert is_valid is False
    assert any("cannot be converted to float" in err for err in errors)


def test_temperature_out_of_bounds_high(validator, valid_record):
    valid_record["temperature"] = 72.0  # Plausible max is 65°C
    is_valid, sanitized, errors = validator.validate_record(valid_record)
    assert is_valid is False
    assert any("outside plausible bounds" in err for err in errors)


def test_temperature_out_of_bounds_low(validator, valid_record):
    valid_record["temperature"] = -60.0  # Plausible min is -50°C
    is_valid, sanitized, errors = validator.validate_record(valid_record)
    assert is_valid is False
    assert any("outside plausible bounds" in err for err in errors)


def test_humidity_out_of_bounds(validator, valid_record):
    valid_record["humidity"] = 115.0  # Max is 100%
    is_valid, sanitized, errors = validator.validate_record(valid_record)
    assert is_valid is False
    assert any("outside plausible bounds" in err for err in errors)


def test_negative_rainfall(validator, valid_record):
    valid_record["rainfall"] = -5.0
    is_valid, sanitized, errors = validator.validate_record(valid_record)
    assert is_valid is False
    assert any("outside plausible bounds" in err for err in errors)


def test_negative_wind_speed(validator, valid_record):
    valid_record["wind_speed"] = -10.0
    is_valid, sanitized, errors = validator.validate_record(valid_record)
    assert is_valid is False
    assert any("outside plausible bounds" in err for err in errors)


def test_pressure_out_of_bounds(validator, valid_record):
    valid_record["pressure"] = 500.0  # Min plausible pressure is 850 hPa
    is_valid, sanitized, errors = validator.validate_record(valid_record)
    assert is_valid is False
    assert any("outside plausible bounds" in err for err in errors)


def test_validate_csv_line_valid(validator):
    line = "2026-08-18T08:00:00,Bengaluru,24.5,60.0,0.0,12.0,915.0"
    is_valid, sanitized, err = validator.validate_csv_line(line)
    assert is_valid is True
    assert err is None
    assert sanitized["city"] == "Bengaluru"
    assert sanitized["temperature"] == 24.5


def test_validate_csv_line_header(validator):
    line = "timestamp,city,temperature,humidity,rainfall,wind_speed,pressure"
    is_valid, sanitized, err = validator.validate_csv_line(line)
    assert is_valid is False
    assert err == "HEADER_ROW"


def test_validate_csv_line_malformed_columns(validator):
    line = "2026-08-18T08:00:00,Bengaluru,24.5"
    is_valid, sanitized, err = validator.validate_csv_line(line)
    assert is_valid is False
    assert "Malformed line: expected 7 columns, got 3" in err


def test_sanitize_and_filter_quarantine(validator, valid_record):
    malformed_record = {
        "timestamp": "2026-08-18T08:00:00",
        "city": "Mumbai",
        "temperature": "corrupt_data",
        "humidity": 80.0,
        "rainfall": 0.0,
        "wind_speed": 10.0,
        "pressure": 1010.0
    }
    batch = [valid_record, malformed_record]
    valid_recs, quarantined = validator.sanitize_and_filter(batch)
    
    assert len(valid_recs) == 1
    assert len(quarantined) == 1
    assert valid_recs[0]["city"] == "Chennai"
    assert quarantined[0]["raw_record"]["city"] == "Mumbai"
    assert any("cannot be converted to float" in err for err in quarantined[0]["errors"])
