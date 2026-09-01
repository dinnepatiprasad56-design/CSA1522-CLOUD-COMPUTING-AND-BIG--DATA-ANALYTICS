"""
Interactive Plotly Visualization Charts Module
Generates production-grade analytical charts for meteorological metrics and Hadoop job metrics.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Optional

DARK_THEME_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,23,42,0.6)",
    font=dict(family="Inter, Roboto, sans-serif", color="#e2e8f0"),
    xaxis=dict(gridcolor="#334155", showgrid=True, zerolinecolor="#475569"),
    yaxis=dict(gridcolor="#334155", showgrid=True, zerolinecolor="#475569"),
    margin=dict(l=40, r=20, t=40, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)


def create_temperature_range_chart(df: pd.DataFrame) -> go.Figure:
    """Generates a multi-bar chart comparing Min, Average, and Max temperatures across cities."""
    fig = go.Figure()
    if df.empty:
        return fig

    fig.add_trace(go.Bar(
        name="Min Temp (°C)",
        x=df["city"],
        y=df["min_temperature"],
        marker_color="#38bdf8"
    ))
    fig.add_trace(go.Bar(
        name="Avg Temp (°C)",
        x=df["city"],
        y=df["avg_temperature"],
        marker_color="#f59e0b"
    ))
    fig.add_trace(go.Bar(
        name="Max Temp (°C)",
        x=df["city"],
        y=df["max_temperature"],
        marker_color="#ef4444"
    ))

    fig.update_layout(
        title="<b>Temperature Range Analysis by City (Hadoop Processed)</b>",
        barmode="group",
        yaxis_title="Temperature (°C)",
        **DARK_THEME_LAYOUT
    )
    return fig


def create_humidity_chart(df: pd.DataFrame) -> go.Figure:
    """Generates average humidity bars with min-max spread indicator."""
    fig = go.Figure()
    if df.empty:
        return fig

    fig.add_trace(go.Bar(
        x=df["city"],
        y=df["avg_humidity"],
        marker=dict(
            color=df["avg_humidity"],
            colorscale="Tealgrn",
            showscale=True,
            colorbar=dict(title="Avg Humidity %")
        ),
        text=df["avg_humidity"].apply(lambda v: f"{v:.1f}%"),
        textposition="auto"
    ))

    fig.update_layout(
        title="<b>Average Relative Humidity (%) by City</b>",
        yaxis_title="Humidity (%)",
        yaxis_range=[0, 100],
        **DARK_THEME_LAYOUT
    )
    return fig


def create_rainfall_chart(df: pd.DataFrame) -> go.Figure:
    """Generates total accumulated rainfall and max single downpour event."""
    fig = go.Figure()
    if df.empty:
        return fig

    fig.add_trace(go.Bar(
        name="Total Rainfall (mm)",
        x=df["city"],
        y=df["total_rainfall"],
        marker_color="#0284c7"
    ))
    fig.add_trace(go.Scatter(
        name="Max Downpour Event (mm)",
        x=df["city"],
        y=df["max_rainfall"],
        mode="markers+lines",
        marker=dict(size=10, color="#f43f5e")
    ))

    fig.update_layout(
        title="<b>Total Accumulated Rainfall & Max Precipitation Spikes (mm)</b>",
        yaxis_title="Precipitation (mm)",
        **DARK_THEME_LAYOUT
    )
    return fig


def create_wind_speed_chart(df: pd.DataFrame) -> go.Figure:
    """Generates average wind speed and maximum gust velocity comparisons."""
    fig = go.Figure()
    if df.empty:
        return fig

    fig.add_trace(go.Bar(
        name="Average Wind Speed",
        x=df["city"],
        y=df["avg_wind_speed"],
        marker_color="#10b981"
    ))
    fig.add_trace(go.Bar(
        name="Max Gust Velocity",
        x=df["city"],
        y=df["max_wind_speed"],
        marker_color="#8b5cf6"
    ))

    fig.update_layout(
        title="<b>Wind Speed vs Peak Gust Velocity (km/h)</b>",
        barmode="group",
        yaxis_title="Velocity (km/h)",
        **DARK_THEME_LAYOUT
    )
    return fig


def create_pressure_chart(df: pd.DataFrame) -> go.Figure:
    """Generates atmospheric pressure comparison across cities."""
    fig = go.Figure()
    if df.empty:
        return fig

    fig.add_trace(go.Bar(
        x=df["city"],
        y=df["avg_pressure"],
        marker_color="#6366f1",
        text=df["avg_pressure"].apply(lambda v: f"{v:.1f} hPa"),
        textposition="auto"
    ))

    fig.update_layout(
        title="<b>Atmospheric Pressure Distribution (hPa)</b>",
        yaxis_title="Pressure (hPa)",
        yaxis_range=[880, 1030],
        **DARK_THEME_LAYOUT
    )
    return fig


def create_city_comparison_radar(df: pd.DataFrame) -> go.Figure:
    """Generates normalized radar / spider comparison chart across all weather parameters."""
    fig = go.Figure()
    if df.empty:
        return fig

    categories = ["Temperature (°C)", "Humidity (%)", "Rainfall (scaled)", "Wind Speed (km/h)", "Pressure (offset)"]

    for _, row in df.iterrows():
        # Normalized metrics for spider chart visualization
        t_val = row["avg_temperature"]
        h_val = row["avg_humidity"]
        r_val = min(100.0, (row["total_rainfall"] / max(1.0, df["total_rainfall"].max())) * 100.0)
        w_val = row["avg_wind_speed"] * 2.0
        p_val = max(0.0, row["avg_pressure"] - 900.0)

        values = [t_val, h_val, r_val, w_val, p_val]
        values.append(values[0])  # Close loop

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill="toself",
            name=row["city"]
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 110], gridcolor="#334155"),
            bgcolor="rgba(15,23,42,0.8)"
        ),
        title="<b>Multi-City Meteorological Comparison Radar</b>",
        **DARK_THEME_LAYOUT
    )
    return fig


def create_timeseries_trend_chart(df_raw: pd.DataFrame, metric: str, selected_cities: Optional[List[str]] = None) -> go.Figure:
    """Generates interactive time-series line chart for historical and live streaming trends."""
    if df_raw.empty or metric not in df_raw.columns:
        return go.Figure()

    filtered = df_raw.copy()
    if selected_cities:
        filtered = filtered[filtered["city"].isin(selected_cities)]

    fig = px.line(
        filtered,
        x="timestamp",
        y=metric,
        color="city",
        title=f"<b>Time-Series Evolution: {metric.replace('_', ' ').title()}</b>",
        template="plotly_dark"
    )
    fig.update_layout(**DARK_THEME_LAYOUT)
    return fig


def create_job_performance_chart(df_jobs: pd.DataFrame) -> go.Figure:
    """Plots Hadoop Streaming MapReduce execution duration and records processed."""
    fig = go.Figure()
    if df_jobs.empty:
        return fig

    fig.add_trace(go.Bar(
        name="Records Ingested",
        x=df_jobs["job_id"],
        y=df_jobs["records_processed"],
        marker_color="#3b82f6",
        yaxis="y"
    ))
    fig.add_trace(go.Scatter(
        name="Duration (s)",
        x=df_jobs["job_id"],
        y=df_jobs["duration_seconds"],
        mode="lines+markers",
        marker=dict(size=8, color="#f59e0b"),
        yaxis="y2"
    ))

    layout = DARK_THEME_LAYOUT.copy()
    layout["yaxis2"] = dict(
        title="Duration (seconds)",
        overlaying="y",
        side="right",
        showgrid=False
    )
    fig.update_layout(
        title="<b>Hadoop Streaming Execution Performance & Duration (s)</b>",
        yaxis=dict(title="Records Processed", gridcolor="#334155"),
        **layout
    )
    return fig
