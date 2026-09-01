"""
Dashboard Data Loader Module
Reads and caches processed Hadoop analytics results, raw time-series, and job execution logs.
Supports both standard Python dictionary lists and Pandas DataFrames.
"""

import os
import csv
import glob
import yaml
from datetime import datetime
from typing import Dict, List, Any, Optional

SUMMARY_CSV = os.path.join("data", "processed", "analytics_summary.csv")
HISTORY_CSV = os.path.join("data", "processed", "job_history.csv")
HISTORICAL_ANALYTICS_CSV = os.path.join("data", "processed", "historical_analytics.csv")
SAMPLE_RAW_CSV = os.path.join("data", "sample", "sample_weather_data.csv")
CONFIG_YAML = os.path.join("config", "config.yaml")
THRESHOLDS_YAML = os.path.join("config", "thresholds.yaml")

# Check if pandas is available in runtime
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


def load_raw_summary_rows() -> List[Dict[str, Any]]:
    """Reads processed Hadoop analytics summary CSV using standard csv.DictReader."""
    if not os.path.exists(SUMMARY_CSV) or os.path.getsize(SUMMARY_CSV) < 10:
        return []

    rows = []
    with open(SUMMARY_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            parsed = {
                "city": r["city"],
                "record_count": int(r.get("record_count", 0)),
                "avg_temperature": float(r.get("avg_temperature", 0.0)),
                "min_temperature": float(r.get("min_temperature", 0.0)),
                "max_temperature": float(r.get("max_temperature", 0.0)),
                "avg_humidity": float(r.get("avg_humidity", 0.0)),
                "min_humidity": float(r.get("min_humidity", 0.0)),
                "max_humidity": float(r.get("max_humidity", 0.0)),
                "total_rainfall": float(r.get("total_rainfall", 0.0)),
                "max_rainfall": float(r.get("max_rainfall", 0.0)),
                "avg_wind_speed": float(r.get("avg_wind_speed", 0.0)),
                "max_wind_speed": float(r.get("max_wind_speed", 0.0)),
                "avg_pressure": float(r.get("avg_pressure", 0.0)),
                "min_pressure": float(r.get("min_pressure", 0.0)),
                "anomalies_count": int(r.get("anomalies_count", 0))
            }
            rows.append(parsed)
    return rows


def load_analytics_summary() -> Any:
    """Loads processed Hadoop analytics summary as DataFrame (if pandas available) or dict list."""
    rows = load_raw_summary_rows()
    if HAS_PANDAS:
        if rows:
            return pd.DataFrame(rows)
        columns = [
            "city", "record_count", "avg_temperature", "min_temperature", "max_temperature",
            "avg_humidity", "min_humidity", "max_humidity", "total_rainfall", "max_rainfall",
            "avg_wind_speed", "max_wind_speed", "avg_pressure", "min_pressure", "anomalies_count"
        ]
        return pd.DataFrame(columns=columns)
    return rows


def load_job_history() -> Any:
    """Loads historical Hadoop Streaming job run duration, timestamps, and execution status."""
    rows = []
    if os.path.exists(HISTORY_CSV) and os.path.getsize(HISTORY_CSV) > 10:
        with open(HISTORY_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append({
                    "job_id": r.get("job_id", ""),
                    "timestamp": r.get("timestamp", ""),
                    "duration_seconds": float(r.get("duration_seconds", 0.0)),
                    "records_processed": int(r.get("records_processed", 0)),
                    "cities_count": int(r.get("cities_count", 0)),
                    "status": r.get("status", "SUCCESS"),
                    "engine": r.get("engine", "LOCAL_STREAMING")
                })
    if HAS_PANDAS:
        if rows:
            return pd.DataFrame(rows)
        return pd.DataFrame(columns=["job_id", "timestamp", "duration_seconds", "records_processed", "cities_count", "status", "engine"])
    return rows


def load_raw_timeseries_data() -> Any:
    """
    Loads raw observation records from sample dataset and any newly generated batches.
    """
    rows = []
    source_files = []
    if os.path.exists(SAMPLE_RAW_CSV):
        source_files.append(SAMPLE_RAW_CSV)

    generated_files = glob.glob(os.path.join("data", "generated", "*.csv"))
    source_files.extend(generated_files[-20:])

    seen_keys = set()
    for sfile in source_files:
        try:
            with open(sfile, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    key = (r.get("timestamp"), r.get("city"))
                    if key not in seen_keys and r.get("city"):
                        seen_keys.add(key)
                        rows.append({
                            "timestamp": r.get("timestamp"),
                            "city": r.get("city"),
                            "temperature": float(r.get("temperature", 0.0)),
                            "humidity": float(r.get("humidity", 0.0)),
                            "rainfall": float(r.get("rainfall", 0.0)),
                            "wind_speed": float(r.get("wind_speed", 0.0)),
                            "pressure": float(r.get("pressure", 1013.25))
                        })
        except Exception:
            continue

    if HAS_PANDAS:
        if rows:
            df = pd.DataFrame(rows)
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df.sort_values(by="timestamp", inplace=True)
            return df
        return pd.DataFrame(columns=["timestamp", "city", "temperature", "humidity", "rainfall", "wind_speed", "pressure"])
    return rows


def load_thresholds() -> Dict[str, Any]:
    """Loads meteorological anomaly thresholds configuration from YAML."""
    if os.path.exists(THRESHOLDS_YAML):
        try:
            with open(THRESHOLDS_YAML, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception:
            pass
    return {}


def get_pipeline_metadata() -> Dict[str, Any]:
    """Retrieves high-level cluster analytics status and timestamp information."""
    last_mod = "N/A"
    if os.path.exists(SUMMARY_CSV):
        mtime = os.path.getmtime(SUMMARY_CSV)
        last_mod = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")

    df_jobs = load_job_history()
    total_jobs = len(df_jobs)
    if HAS_PANDAS and isinstance(df_jobs, pd.DataFrame) and not df_jobs.empty:
        last_job_id = df_jobs.iloc[-1]["job_id"]
        last_duration = df_jobs.iloc[-1]["duration_seconds"]
    elif isinstance(df_jobs, list) and df_jobs:
        last_job_id = df_jobs[-1]["job_id"]
        last_duration = df_jobs[-1]["duration_seconds"]
    else:
        last_job_id = "None"
        last_duration = 0.0

    return {
        "last_updated": last_mod,
        "total_jobs_run": total_jobs,
        "last_job_id": last_job_id,
        "last_job_duration_s": last_duration,
        "cluster_engine": "Hadoop Streaming (YARN/MapReduce)"
    }
