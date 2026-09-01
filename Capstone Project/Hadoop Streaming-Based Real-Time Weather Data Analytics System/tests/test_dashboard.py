"""
Unit Tests for Streamlit Dashboard Data Loader, Alert Engine, and Plotly Charts
"""

import os
import pytest

from dashboard.data_loader import (
    load_raw_summary_rows,
    load_thresholds,
    get_pipeline_metadata
)
from dashboard.alerts import evaluate_weather_alerts


def test_data_loader_raw_summary_rows():
    rows = load_raw_summary_rows()
    assert isinstance(rows, list)
    assert len(rows) >= 1
    assert "city" in rows[0]
    assert "avg_temperature" in rows[0]


def test_load_thresholds():
    config = load_thresholds()
    assert isinstance(config, dict)
    assert "thresholds" in config
    assert "temperature" in config["thresholds"]


def test_get_pipeline_metadata():
    meta = get_pipeline_metadata()
    assert isinstance(meta, dict)
    assert "last_updated" in meta
    assert "cluster_engine" in meta


def test_evaluate_weather_alerts_critical_trigger():
    raw_anomaly = [{
        "timestamp": "2026-08-18T12:00:00",
        "city": "Delhi",
        "temperature": 45.5,  # Heatwave
        "humidity": 20.0,
        "rainfall": 0.0,
        "wind_speed": 15.0,
        "pressure": 980.0
    }]
    summary = [{
        "city": "Delhi",
        "record_count": 10,
        "avg_temperature": 35.0,
        "min_temperature": 25.0,
        "max_temperature": 45.5,
        "avg_humidity": 45.0,
        "min_humidity": 20.0,
        "max_humidity": 70.0,
        "total_rainfall": 0.0,
        "max_rainfall": 0.0,
        "avg_wind_speed": 12.0,
        "max_wind_speed": 18.0,
        "avg_pressure": 980.0,
        "min_pressure": 978.0,
        "anomalies_count": 1
    }]

    alerts = evaluate_weather_alerts(raw_anomaly, summary)
    assert len(alerts) >= 1
    assert alerts[0]["city"] == "Delhi"
    assert alerts[0]["type"] == "HEATWAVE"
    assert alerts[0]["severity"] == "CRITICAL"
