#!/usr/bin/env bash
# Wrapper redirecting to jobs/run_weather_analytics.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
bash "$PROJECT_ROOT/jobs/run_weather_analytics.sh" "$@"
