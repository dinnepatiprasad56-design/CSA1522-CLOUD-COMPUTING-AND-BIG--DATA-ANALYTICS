"""
Unit Tests for Hadoop Streaming Python Mappers
"""

import io
import sys
from mapper.temperature_mapper import parse_and_map as map_temp
from mapper.humidity_mapper import parse_and_map as map_hum
from mapper.rainfall_mapper import parse_and_map as map_rain
from mapper.wind_mapper import parse_and_map as map_wind
from mapper.pressure_mapper import parse_and_map as map_press
from mapper.weather_mapper import parse_and_map as map_weather

SAMPLE_CSV = """timestamp,city,temperature,humidity,rainfall,wind_speed,pressure
2026-08-18T08:00:00,Chennai,32.5,76.0,2.4,12.5,1008.2
2026-08-18T08:00:00,Bengaluru,24.5,60.0,0.0,10.0,915.0
2026-08-18T08:00:00,Mumbai,corrupt_temp,85.0,15.0,20.0,1010.0
2026-08-18T08:00:00,Delhi,38.0,-10.0,0.0,15.0,980.0
2026-08-18T08:00:00,Kolkata,31.0,80.0,-5.0,14.0,1006.0
2026-08-18T08:00:00,Pune,26.0,65.0,0.0,350.0,950.0
2026-08-18T08:00:00,Hyderabad,29.0,55.0,0.0,12.0,600.0
"""


def run_mapper(mapper_func, input_text):
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(input_text)
    sys.stdout = io.StringIO()
    try:
        mapper_func()
        return sys.stdout.getvalue().strip().split("\n")
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout


def test_temperature_mapper():
    output = run_mapper(map_temp, SAMPLE_CSV)
    # Header and corrupt line should be skipped
    assert "Chennai\t32.50" in output
    assert "Bengaluru\t24.50" in output
    assert not any("Mumbai" in line for line in output)


def test_humidity_mapper():
    output = run_mapper(map_hum, SAMPLE_CSV)
    # Delhi has invalid humidity (-10.0) -> skipped
    assert "Chennai\t76.00" in output
    assert "Bengaluru\t60.00" in output
    assert not any("Delhi" in line for line in output)


def test_rainfall_mapper():
    output = run_mapper(map_rain, SAMPLE_CSV)
    # Kolkata has negative rainfall (-5.0) -> skipped
    assert "Chennai\t2.40" in output
    assert "Bengaluru\t0.00" in output
    assert not any("Kolkata" in line for line in output)


def test_wind_mapper():
    output = run_mapper(map_wind, SAMPLE_CSV)
    # Pune has wind > 300 km/h (350.0) -> skipped
    assert "Chennai\t12.50" in output
    assert "Bengaluru\t10.00" in output
    assert not any("Pune" in line for line in output)


def test_pressure_mapper():
    output = run_mapper(map_press, SAMPLE_CSV)
    # Hyderabad has pressure < 850 hPa (600.0) -> skipped
    assert "Chennai\t1008.20" in output
    assert "Bengaluru\t915.00" in output
    assert not any("Hyderabad" in line for line in output)


def test_weather_mapper():
    clean_csv = """timestamp,city,temperature,humidity,rainfall,wind_speed,pressure
2026-08-18T08:00:00,Chennai,32.5,76.0,2.4,12.5,1008.2
"""
    output = run_mapper(map_weather, clean_csv)
    assert len(output) == 1
    parts = output[0].split("\t")
    assert parts[0] == "Chennai"
    assert parts[1] == "2026-08-18T08:00:00,32.50,76.00,2.40,12.50,1008.20"
