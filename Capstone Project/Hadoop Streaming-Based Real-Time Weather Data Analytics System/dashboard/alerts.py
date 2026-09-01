"""
Weather Anomaly Detection and Alert Evaluation Module
Evaluates meteorological thresholds and formats visual alert banners for the Streamlit dashboard.
"""

from typing import List, Dict, Any
from dashboard.data_loader import load_thresholds


def evaluate_weather_alerts(raw_data: Any, summary_data: Any) -> List[Dict[str, Any]]:
    """
    Scans the latest meteorological observations and aggregated metrics
    to detect abnormal weather conditions against configured thresholds.
    Accepts both Pandas DataFrames and Python dictionary lists.
    """
    threshold_config = load_thresholds()
    t_limits = threshold_config.get("thresholds", {})

    alerts = []

    # Convert to list of dicts if DataFrame
    raw_rows = []
    if hasattr(raw_data, "to_dict"):
        raw_rows = raw_data.to_dict(orient="records")
    elif isinstance(raw_data, list):
        raw_rows = raw_data

    summary_rows = []
    if hasattr(summary_data, "to_dict"):
        summary_rows = summary_data.to_dict(orient="records")
    elif isinstance(summary_data, list):
        summary_rows = summary_data

    # 1. Evaluate from Latest Observations per City
    if raw_rows:
        latest_by_city: Dict[str, Dict[str, Any]] = {}
        for row in raw_rows:
            city = row.get("city")
            if city:
                latest_by_city[city] = row

        for city, row in latest_by_city.items():
            temp = float(row.get("temperature", 0.0))
            hum = float(row.get("humidity", 0.0))
            rain = float(row.get("rainfall", 0.0))
            wind = float(row.get("wind_speed", 0.0))
            press = float(row.get("pressure", 1013.25))

            # Severe Heatwave Alert
            if temp >= t_limits.get("temperature", {}).get("critical_high", 42.0):
                alerts.append({
                    "city": city,
                    "type": "HEATWAVE",
                    "severity": "CRITICAL",
                    "metric": f"Temperature: {temp}°C (Limit: ≥42°C)",
                    "advisory": "Dangerous heat index. Ensure adequate hydration and avoid prolonged sun exposure."
                })
            elif temp >= t_limits.get("temperature", {}).get("warning_high", 38.0):
                alerts.append({
                    "city": city,
                    "type": "HIGH_HEAT",
                    "severity": "WARNING",
                    "metric": f"Temperature: {temp}°C (Limit: ≥38°C)",
                    "advisory": "Elevated thermal conditions. Limit strenuous midday outdoor activity."
                })

            # Coldwave Alert
            if temp <= t_limits.get("temperature", {}).get("critical_low", 8.0):
                alerts.append({
                    "city": city,
                    "type": "COLDWAVE",
                    "severity": "CRITICAL",
                    "metric": f"Temperature: {temp}°C (Limit: ≤8°C)",
                    "advisory": "Severe cold wave. Vulnerable populations require heating protection."
                })

            # Torrential Rainfall / Flood Risk
            if rain >= t_limits.get("rainfall", {}).get("critical_high", 50.0):
                alerts.append({
                    "city": city,
                    "type": "FLASH_FLOOD_RISK",
                    "severity": "CRITICAL",
                    "metric": f"Precipitation: {rain} mm/h (Limit: ≥50mm)",
                    "advisory": "Extreme downpour reported. High probability of urban waterlogging and flash floods."
                })
            elif rain >= t_limits.get("rainfall", {}).get("warning_high", 30.0):
                alerts.append({
                    "city": city,
                    "type": "HEAVY_RAIN",
                    "severity": "WARNING",
                    "metric": f"Precipitation: {rain} mm/h (Limit: ≥30mm)",
                    "advisory": "Heavy localized showers. Exercise caution on transit routes."
                })

            # High Wind / Gale Warning
            if wind >= t_limits.get("wind_speed", {}).get("critical_high", 50.0):
                alerts.append({
                    "city": city,
                    "type": "GALE_WARNING",
                    "severity": "CRITICAL",
                    "metric": f"Wind Velocity: {wind} km/h (Limit: ≥50 km/h)",
                    "advisory": "Gale force gusts detected. Secure loose outdoor fixtures and structures."
                })

            # Cyclonic Depression
            if press <= t_limits.get("pressure", {}).get("critical_low", 975.0) and (wind >= 40.0 or rain >= 25.0):
                alerts.append({
                    "city": city,
                    "type": "CYCLONIC_DEPRESSION",
                    "severity": "CRITICAL",
                    "metric": f"Barometric Pressure: {press} hPa & Wind: {wind} km/h",
                    "advisory": "Severe cyclonic depression signature detected by MapReduce anomaly models."
                })

    # 2. Add Aggregated Anomalies from Summary Table if no immediate raw alert triggered
    if summary_rows and not alerts:
        for row in summary_rows:
            if row.get("anomalies_count", 0) > 0:
                alerts.append({
                    "city": row["city"],
                    "type": "HISTORICAL_ANOMALIES",
                    "severity": "WARNING",
                    "metric": f"{int(row['anomalies_count'])} cumulative anomaly events detected in HDFS dataset",
                    "advisory": f"Max temp: {row['max_temperature']}°C | Max Rain: {row['max_rainfall']}mm | Max Wind: {row['max_wind_speed']}km/h"
                })

    return alerts
