"""
Unit Tests for Weather Data Ingestion, Generator, and HDFS Uploader Modules
"""

import os
import csv
import tempfile
import pytest
from unittest.mock import MagicMock, patch

from ingestion.weather_generator import WeatherDataGenerator, CITY_PROFILES, CSV_FIELDNAMES
from ingestion.hdfs_uploader import HDFSUploader
from ingestion.weather_api import WeatherAPIClient


@pytest.fixture
def generator():
    return WeatherDataGenerator(anomaly_ratio=0.0)


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


def test_generator_single_record_fields_and_types(generator):
    for city in CITY_PROFILES.keys():
        record = generator.generate_single_record(city)
        assert set(record.keys()) == set(CSV_FIELDNAMES)
        assert record["city"] == city
        assert isinstance(record["temperature"], float)
        assert isinstance(record["humidity"], float)
        assert isinstance(record["rainfall"], float)
        assert isinstance(record["wind_speed"], float)
        assert isinstance(record["pressure"], float)
        assert 0.0 <= record["humidity"] <= 100.0
        assert record["rainfall"] >= 0.0
        assert record["wind_speed"] >= 0.0


def test_generator_all_seven_indian_cities(generator):
    expected_cities = {"Chennai", "Bengaluru", "Hyderabad", "Mumbai", "Delhi", "Kolkata", "Pune"}
    batch = generator.generate_city_batch()
    generated_cities = {rec["city"] for rec in batch}
    assert generated_cities == expected_cities
    assert len(batch) == 7


def test_generator_force_anomaly():
    gen = WeatherDataGenerator(anomaly_ratio=1.0)
    record = gen.generate_single_record("Delhi", force_anomaly=True)
    # Check that record is still formatted correctly and passes schema
    assert set(record.keys()) == set(CSV_FIELDNAMES)
    is_valid, _, errors = gen.validator.validate_record(record)
    assert is_valid is True


def test_write_batch_to_csv(generator, temp_dir):
    batch = generator.generate_city_batch()
    target_csv = os.path.join(temp_dir, "test_batch.csv")
    generator.write_batch_to_csv(batch, target_csv)

    assert os.path.exists(target_csv)
    with open(target_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 7
        assert reader.fieldnames == CSV_FIELDNAMES
        assert rows[0]["city"] in CITY_PROFILES


def test_stream_batches_generator(generator, temp_dir):
    batches_gen = generator.stream_batches(interval_seconds=0.01, total_batches=3, output_dir=temp_dir)
    generated_files = list(batches_gen)
    assert len(generated_files) == 3
    for filepath in generated_files:
        assert os.path.exists(filepath)


def test_hdfs_uploader_partition_path():
    uploader = HDFSUploader(hdfs_root="/weather", dry_run=True)
    partition = uploader.get_partition_path()
    assert partition.startswith("/weather/raw/")
    parts = partition.split("/")
    # Expected: ['', 'weather', 'raw', 'YYYY', 'MM', 'DD']
    assert len(parts) == 6
    assert parts[1] == "weather"
    assert parts[2] == "raw"


def test_hdfs_uploader_simulated_upload(temp_dir):
    mock_hdfs_dir = os.path.join(temp_dir, "hdfs_store")
    uploader = HDFSUploader(hdfs_root="/weather", dry_run=True, mock_local_dir=mock_hdfs_dir)

    # Create dummy local file
    local_csv = os.path.join(temp_dir, "batch_001.csv")
    with open(local_csv, "w", encoding="utf-8") as f:
        f.write("timestamp,city,temperature,humidity,rainfall,wind_speed,pressure\n")
        f.write("2026-08-18T08:00:00,Chennai,32.5,76,2.4,12.5,1008.2\n")

    result = uploader.upload_file(local_csv)
    assert result["success"] is True
    assert result["mode"] == "SIMULATED_HDFS"
    assert os.path.exists(result["simulated_path"])

    # Test file listing
    files = uploader.list_hdfs_files(uploader.get_partition_path())
    assert len(files) == 1
    assert "batch_001.csv" in files[0]


def test_weather_api_not_configured():
    client = WeatherAPIClient(api_key="")
    assert client.is_configured() is False
    assert client.fetch_city_weather("Chennai") is None


@patch("ingestion.weather_api.requests.get")
def test_weather_api_mock_response(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "main": {"temp": 31.5, "humidity": 70.0, "pressure": 1005.0},
        "wind": {"speed": 4.5}, # 4.5 m/s = 16.2 km/h
        "rain": {"1h": 1.2}
    }
    mock_get.return_value = mock_resp

    client = WeatherAPIClient(api_key="dummy_valid_key")
    record = client.fetch_city_weather("Chennai")
    assert record is not None
    assert record["city"] == "Chennai"
    assert record["temperature"] == 31.5
    assert record["humidity"] == 70.0
    assert record["wind_speed"] == 16.2
    assert record["rainfall"] == 1.2
    assert record["pressure"] == 1005.0


def test_pipeline_orchestrator_execution(temp_dir):
    from ingestion.pipeline_orchestrator import PipelineOrchestrator
    # Create sample CSV
    source_csv = os.path.join(temp_dir, "sample.csv")
    with open(source_csv, "w", encoding="utf-8") as f:
        f.write("timestamp,city,temperature,humidity,rainfall,wind_speed,pressure\n")
        f.write("2026-08-18T08:00:00,Chennai,32.0,75.0,0.0,15.0,1008.0\n")
        f.write("2026-08-18T09:00:00,Chennai,34.0,70.0,0.0,12.0,1008.0\n")

    export_csv = os.path.join(temp_dir, "analytics_output.csv")
    orchestrator = PipelineOrchestrator()
    res = orchestrator.run_pipeline(
        raw_source_file=source_csv,
        output_csv_path=export_csv
    )

    assert res["status"] == "SUCCESS"
    assert res["cities_count"] == 1
    assert os.path.exists(export_csv)
    with open(export_csv, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Chennai" in content
        assert "33.00" in content  # avg temp (32+34)/2

