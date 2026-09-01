"""
Unit Tests for Near-Real-Time Continuous Weather Analytics Controller
"""

import os
import csv
import tempfile
import pytest
from unittest.mock import patch, MagicMock

from ingestion.continuous_pipeline import ContinuousPipelineController, JOB_HISTORY_HEADER, HISTORICAL_ANALYTICS_HEADER


@pytest.fixture
def temp_workspace():
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_dir = os.path.join(tmp_dir, "processed")
        yield tmp_dir, output_dir


def test_controller_initialization(temp_workspace):
    tmp_dir, output_dir = temp_workspace
    controller = ContinuousPipelineController(
        output_dir=output_dir,
        hdfs_root="/weather"
    )

    assert os.path.exists(controller.history_csv)
    assert os.path.exists(controller.historical_analytics_csv)
    with open(controller.history_csv, "r", encoding="utf-8") as f:
        assert f.readline() == JOB_HISTORY_HEADER


def test_ingest_single_cycle(temp_workspace):
    tmp_dir, output_dir = temp_workspace
    controller = ContinuousPipelineController(
        output_dir=output_dir,
        hdfs_root="/weather"
    )

    batch_path = controller.ingest_single_cycle()
    assert batch_path is not None
    assert os.path.exists(batch_path)
    assert controller._total_records_ingested == 7


def test_execute_hadoop_job_cycle_and_logging(temp_workspace):
    tmp_dir, output_dir = temp_workspace
    controller = ContinuousPipelineController(
        output_dir=output_dir,
        hdfs_root="/weather"
    )

    # Ingest one batch first
    controller.ingest_single_cycle()

    # Execute Job Cycle
    metrics = controller.execute_hadoop_job_cycle()
    assert metrics is not None
    assert metrics["status"] == "SUCCESS"
    assert metrics["cities_count"] >= 1
    assert metrics["duration_seconds"] >= 0.0

    # Verify Job History file has been updated
    with open(controller.history_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["job_id"].startswith("JOB_")
        assert rows[0]["status"] == "SUCCESS"

    # Verify Historical Analytics file has snapshots
    with open(controller.historical_analytics_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
        # Header + at least 1 city row
        assert len(rows) >= 2


def test_prevent_overlapping_jobs(temp_workspace):
    tmp_dir, output_dir = temp_workspace
    controller = ContinuousPipelineController(
        output_dir=output_dir,
        hdfs_root="/weather"
    )

    # Artificially acquire lock
    assert controller._job_lock.acquire(blocking=False) is True

    # Try triggering job while locked
    metrics = controller.execute_hadoop_job_cycle()
    assert metrics is None  # Should return None and skip

    # Release lock
    controller._job_lock.release()

    # Now it should succeed
    metrics = controller.execute_hadoop_job_cycle()
    assert metrics is not None
    assert metrics["status"] == "SUCCESS"


def test_controller_max_cycles_execution(temp_workspace):
    tmp_dir, output_dir = temp_workspace
    controller = ContinuousPipelineController(
        ingestion_interval=0.01,
        processing_interval=0.02,
        output_dir=output_dir,
        hdfs_root="/weather"
    )

    controller.run_continuous(max_cycles=3)
    assert controller._total_records_ingested == 21  # 3 cycles * 7 cities
    assert controller._job_counter >= 1
