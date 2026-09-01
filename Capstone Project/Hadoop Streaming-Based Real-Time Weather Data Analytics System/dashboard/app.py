"""
Main Streamlit Application: Real-Time Weather Analytics Dashboard
Capstone Project: Hadoop Streaming-Based Real-Time Weather Data Analytics System on Cloud Infrastructure
"""

import time
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from dashboard.data_loader import (
    load_analytics_summary,
    load_job_history,
    load_raw_timeseries_data,
    get_pipeline_metadata,
    load_thresholds
)
from dashboard.alerts import evaluate_weather_alerts
from dashboard.charts import (
    create_temperature_range_chart,
    create_humidity_chart,
    create_rainfall_chart,
    create_wind_speed_chart,
    create_pressure_chart,
    create_city_comparison_radar,
    create_timeseries_trend_chart,
    create_job_performance_chart
)
from ingestion.pipeline_orchestrator import PipelineOrchestrator

# ------------------------------------------------------------------------------
# 1. Page Configuration & Custom CSS Styling
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Hadoop Cloud Weather Analytics Dashboard",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    /* Dark Theme Core Typography and Palette */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95));
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        margin-bottom: 12px;
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .metric-caption {
        color: #38bdf8;
        font-size: 0.8rem;
        margin-top: 4px;
    }
    .alert-card-critical {
        background: rgba(239, 68, 68, 0.15);
        border-left: 4px solid #ef4444;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 10px;
        color: #fecaca;
    }
    .alert-card-warning {
        background: rgba(245, 158, 11, 0.15);
        border-left: 4px solid #f59e0b;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 10px;
        color: #fef3c7;
    }
    .status-badge {
        display: inline-block;
        background: #0284c7;
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. Sidebar Filters, Navigation & Controls
# ------------------------------------------------------------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/0e/Apache_Hadoop_logo.svg", width=180)
st.sidebar.title("🌦️ Weather Analytics")
st.sidebar.caption("Cloud Computing & Big Data Analytics Capstone")

# Data Reloading
df_summary = load_analytics_summary()
df_raw = load_raw_timeseries_data()
df_jobs = load_job_history()
metadata = get_pipeline_metadata()

# City Filter
all_cities = sorted(df_summary["city"].unique().tolist()) if not df_summary.empty else ["Chennai", "Bengaluru", "Delhi", "Hyderabad", "Kolkata", "Mumbai", "Pune"]
selected_cities = st.sidebar.multiselect(
    "📍 Filter by Cities:",
    options=all_cities,
    default=all_cities
)

# Date Filter if raw time-series available
if not df_raw.empty and "timestamp" in df_raw.columns:
    min_date = df_raw["timestamp"].min().date()
    max_date = df_raw["timestamp"].max().date()
    date_range = st.sidebar.date_input(
        "📅 Date Range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
else:
    date_range = None

# Real-Time Refresh Settings
st.sidebar.markdown("---")
st.sidebar.subheader("🔄 Real-Time Engine")
auto_refresh = st.sidebar.checkbox("Auto-Refresh Dashboard", value=False)
refresh_interval = st.sidebar.slider("Refresh Interval (s)", min_value=5, max_value=60, value=15, step=5)

# On-Demand Hadoop Job Trigger Button
st.sidebar.markdown("---")
if st.sidebar.button("⚡ Run Hadoop MapReduce Job Now", use_container_width=True):
    with st.spinner("Submitting Hadoop Streaming Job to Cluster..."):
        try:
            orchestrator = PipelineOrchestrator()
            sample_source = "data/sample/sample_weather_data.csv"
            res = orchestrator.run_pipeline(raw_source_file=sample_source)
            st.sidebar.success(f"Job finished in {res['elapsed_seconds']}s!")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Job failed: {str(e)}")

# Cluster Metadata Footer in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Engine**: `{metadata['cluster_engine']}`")
st.sidebar.markdown(f"**Last Sync**: `{metadata['last_updated']}`")
st.sidebar.markdown(f"**Total MapReduce Jobs**: `{metadata['total_jobs_run']}`")

# ------------------------------------------------------------------------------
# 3. Main Dashboard Header & KPI Metrics
# ------------------------------------------------------------------------------
st.title("☁️ Cloud-Based Real-Time Weather Analytics System")
st.markdown(
    "**Hadoop Streaming MapReduce Analytics Engine** | High-Throughput Meteorological Aggregation & Anomaly Detection"
)

# Filter Data according to user selection
filtered_summary = df_summary[df_summary["city"].isin(selected_cities)] if not df_summary.empty else df_summary
filtered_raw = df_raw[df_raw["city"].isin(selected_cities)] if not df_raw.empty else df_raw

if date_range and len(date_range) == 2 and not filtered_raw.empty:
    start_d, end_d = date_range
    filtered_raw = filtered_raw[
        (filtered_raw["timestamp"].dt.date >= start_d) & (filtered_raw["timestamp"].dt.date <= end_d)
    ]

# KPI Metric Cards Row
total_records = int(filtered_summary["record_count"].sum()) if not filtered_summary.empty else len(filtered_raw)
total_anomalies = int(filtered_summary["anomalies_count"].sum()) if not filtered_summary.empty else 0
avg_cluster_temp = filtered_summary["avg_temperature"].mean() if not filtered_summary.empty else 0.0
total_precip = filtered_summary["total_rainfall"].sum() if not filtered_summary.empty else 0.0

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">HDFS Ingested Records</div>
        <div class="metric-value">{total_records:,}</div>
        <div class="metric-caption">Processed via MapReduce</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Monitored Metros</div>
        <div class="metric-value">{len(selected_cities)}</div>
        <div class="metric-caption">Indian City Partitions</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Mean Temperature</div>
        <div class="metric-value">{avg_cluster_temp:.1f} °C</div>
        <div class="metric-caption">Across Target Cities</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Cumulative Rainfall</div>
        <div class="metric-value">{total_precip:.1f} mm</div>
        <div class="metric-caption">Aggregated Precipitation</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Detected Anomalies</div>
        <div class="metric-value" style="color: {'#ef4444' if total_anomalies > 0 else '#10b981'};">{total_anomalies}</div>
        <div class="metric-caption">Extreme Weather Events</div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 4. Main Navigation Tabs
# ------------------------------------------------------------------------------
tab_overview, tab_analytics, tab_comparison, tab_trends, tab_cluster = st.tabs([
    "🌐 Overview & Alerts",
    "📊 Meteorological Analytics",
    "🧭 City Comparison",
    "📈 Historical Trends",
    "⚙️ Hadoop Cluster & Job Logs"
])

# ------------------------------------------------------------------------------
# TAB 1: Overview & Active Alerts
# ------------------------------------------------------------------------------
with tab_overview:
    col_alerts, col_table = st.columns([1, 2])

    with col_alerts:
        st.subheader("🚨 Active Weather Alerts")
        alerts = evaluate_weather_alerts(filtered_raw, filtered_summary)
        if alerts:
            for alert in alerts[:6]:
                css_class = "alert-card-critical" if alert["severity"] == "CRITICAL" else "alert-card-warning"
                st.markdown(f"""
                <div class="{css_class}">
                    <b>[{alert['severity']}] {alert['city']} - {alert['type']}</b><br>
                    <small>{alert['metric']}</small><br>
                    <span>{alert['advisory']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ All meteorological parameters within normal operating thresholds across active cities.")

    with col_table:
        st.subheader("📋 Processed Hadoop Analytics Summary")
        if not filtered_summary.empty:
            display_df = filtered_summary[[
                "city", "record_count", "avg_temperature", "min_temperature", "max_temperature",
                "avg_humidity", "total_rainfall", "avg_wind_speed", "avg_pressure", "anomalies_count"
            ]].rename(columns={
                "city": "City",
                "record_count": "Records",
                "avg_temperature": "Avg Temp (°C)",
                "min_temperature": "Min Temp",
                "max_temperature": "Max Temp",
                "avg_humidity": "Humidity (%)",
                "total_rainfall": "Rain (mm)",
                "avg_wind_speed": "Wind (km/h)",
                "avg_pressure": "Pressure (hPa)",
                "anomalies_count": "Anomalies"
            })
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("No processed summary records found in HDFS output.")

    # High level chart
    st.plotly_chart(create_temperature_range_chart(filtered_summary), use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 2: Deep-Dive Meteorological Analytics
# ------------------------------------------------------------------------------
with tab_analytics:
    st.subheader("Detailed Hadoop MapReduce Analytics")

    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(create_humidity_chart(filtered_summary), use_container_width=True)
    with col_b:
        st.plotly_chart(create_rainfall_chart(filtered_summary), use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        st.plotly_chart(create_wind_speed_chart(filtered_summary), use_container_width=True)
    with col_d:
        st.plotly_chart(create_pressure_chart(filtered_summary), use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 3: City Comparison & Radar Matrix
# ------------------------------------------------------------------------------
with tab_comparison:
    st.subheader("Multi-City Climatological Comparison")
    st.plotly_chart(create_city_comparison_radar(filtered_summary), use_container_width=True)

    st.markdown("### Detailed Metric Breakdowns")
    if not filtered_summary.empty:
        st.dataframe(filtered_summary.set_index("city"), use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 4: Historical Time-Series Trends
# ------------------------------------------------------------------------------
with tab_trends:
    st.subheader("Temporal Evolution & Ingestion Streams")
    metric_choice = st.selectbox(
        "Select Parameter to Plot:",
        options=["temperature", "humidity", "rainfall", "wind_speed", "pressure"],
        format_func=lambda x: x.replace("_", " ").title()
    )
    if not filtered_raw.empty:
        st.plotly_chart(create_timeseries_trend_chart(filtered_raw, metric_choice, selected_cities), use_container_width=True)
    else:
        st.info("No raw observation records available for time-series display.")

# ------------------------------------------------------------------------------
# TAB 5: Hadoop Cluster Diagnostics & Job Performance
# ------------------------------------------------------------------------------
with tab_cluster:
    st.subheader("YARN & Hadoop MapReduce Execution Metrics")
    col_perf, col_info = st.columns([2, 1])

    with col_perf:
        if not df_jobs.empty:
            st.plotly_chart(create_job_performance_chart(df_jobs), use_container_width=True)
        else:
            st.info("No job execution history recorded yet.")

    with col_info:
        st.markdown("### Cluster Topology")
        st.markdown("""
        - **Master Node**: `hadoop-master` (NameNode, ResourceManager)
        - **Worker 1**: `hadoop-worker-1` (DataNode, NodeManager)
        - **Worker 2**: `hadoop-worker-2` (DataNode, NodeManager)
        - **MapReduce Framework**: Hadoop Streaming 3.3.6
        - **HDFS Root**: `/weather`
        """)

    st.markdown("### Job Execution Audit History")
    if not df_jobs.empty:
        st.dataframe(df_jobs.sort_values(by="timestamp", ascending=False), use_container_width=True, hide_index=True)

# ------------------------------------------------------------------------------
# 5. Auto-Refresh Logic
# ------------------------------------------------------------------------------
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()
