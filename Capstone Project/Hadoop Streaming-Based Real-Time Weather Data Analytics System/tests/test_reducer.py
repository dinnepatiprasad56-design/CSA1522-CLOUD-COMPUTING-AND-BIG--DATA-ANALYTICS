"""
Unit Tests for Hadoop Streaming Python Reducers
"""

import io
import sys
from reducer.temperature_reducer import reduce_temperatures
from reducer.humidity_reducer import reduce_humidity
from reducer.rainfall_reducer import reduce_rainfall
from reducer.wind_reducer import reduce_wind
from reducer.pressure_reducer import reduce_pressure
from reducer.weather_reducer import reduce_all_metrics


def run_reducer(reducer_func, input_text):
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(input_text)
    sys.stdout = io.StringIO()
    try:
        reducer_func()
        lines = sys.stdout.getvalue().strip().split("\n")
        return [line for line in lines if line]
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout


def test_temperature_reducer():
    sorted_input = """Bengaluru\t20.00
Bengaluru\t25.00
Bengaluru\t30.00
Chennai\t30.00
Chennai\t34.00
"""
    output = run_reducer(reduce_temperatures, sorted_input)
    assert len(output) == 2
    # Bengaluru: avg=25.00, min=20.00, max=30.00, count=3
    bengaluru = output[0].split("\t")
    assert bengaluru[0] == "Bengaluru"
    assert bengaluru[1] == "25.00"
    assert bengaluru[2] == "20.00"
    assert bengaluru[3] == "30.00"
    assert bengaluru[4] == "3"

    # Chennai: avg=32.00, min=30.00, max=34.00, count=2
    chennai = output[1].split("\t")
    assert chennai[0] == "Chennai"
    assert chennai[1] == "32.00"
    assert chennai[2] == "30.00"
    assert chennai[3] == "34.00"
    assert chennai[4] == "2"


def test_humidity_reducer():
    sorted_input = """Delhi\t40.00
Delhi\t60.00
Mumbai\t80.00
Mumbai\t90.00
"""
    output = run_reducer(reduce_humidity, sorted_input)
    assert len(output) == 2
    delhi = output[0].split("\t")
    assert delhi[0] == "Delhi"
    assert delhi[1] == "50.00"
    assert delhi[2] == "40.00"
    assert delhi[3] == "60.00"
    assert delhi[4] == "2"


def test_rainfall_reducer():
    sorted_input = """Mumbai\t0.00
Mumbai\t25.00
Mumbai\t75.00
Pune\t0.00
Pune\t0.00
"""
    output = run_reducer(reduce_rainfall, sorted_input)
    assert len(output) == 2
    # Mumbai: total=100.00, max=75.00, avg=33.33, rain_events=2, total_records=3
    mumbai = output[0].split("\t")
    assert mumbai[0] == "Mumbai"
    assert mumbai[1] == "100.00"
    assert mumbai[2] == "75.00"
    assert mumbai[3] == "33.33"
    assert mumbai[4] == "2"
    assert mumbai[5] == "3"

    # Pune: total=0.00, max=0.00, avg=0.00, rain_events=0, total_records=2
    pune = output[1].split("\t")
    assert pune[0] == "Pune"
    assert pune[1] == "0.00"
    assert pune[4] == "0"
    assert pune[5] == "2"


def test_wind_reducer():
    sorted_input = """Chennai\t10.00
Chennai\t30.00
"""
    output = run_reducer(reduce_wind, sorted_input)
    assert len(output) == 1
    chennai = output[0].split("\t")
    assert chennai[0] == "Chennai"
    assert chennai[1] == "20.00"  # avg
    assert chennai[2] == "10.00"  # min
    assert chennai[3] == "30.00"  # max
    assert chennai[4] == "2"      # count


def test_pressure_reducer():
    sorted_input = """Kolkata\t1000.00
Kolkata\t1010.00
"""
    output = run_reducer(reduce_pressure, sorted_input)
    assert len(output) == 1
    kolkata = output[0].split("\t")
    assert kolkata[0] == "Kolkata"
    assert kolkata[1] == "1005.00"
    assert kolkata[2] == "1000.00"
    assert kolkata[3] == "1010.00"
    assert kolkata[4] == "2"


def test_weather_reducer_with_anomalies():
    # Record 1: Normal (temp=30, hum=70, rain=0, wind=10, press=1008)
    # Record 2: Heatwave anomaly (temp=44, hum=20, rain=0, wind=15, press=1000)
    sorted_input = """Delhi\t2026-08-18T08:00:00,30.00,70.00,0.00,10.00,1008.00
Delhi\t2026-08-18T09:00:00,44.00,20.00,0.00,15.00,1000.00
"""
    output = run_reducer(reduce_all_metrics, sorted_input)
    assert len(output) == 1
    delhi = output[0].split("\t")
    assert delhi[0] == "Delhi"
    assert delhi[1] == "2"       # total records
    assert delhi[2] == "37.00"   # avg temp
    assert delhi[3] == "30.00"   # min temp
    assert delhi[4] == "44.00"   # max temp
    assert delhi[14] == "1"      # anomalies count (1 heatwave)
