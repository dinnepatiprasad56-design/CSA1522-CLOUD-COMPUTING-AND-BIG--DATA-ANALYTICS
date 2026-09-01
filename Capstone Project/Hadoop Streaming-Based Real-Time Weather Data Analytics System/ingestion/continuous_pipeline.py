"""
Near-Real-Time Continuous Weather Analytics Pipeline Controller
Orchestrates continuous meteorological ingestion, HDFS partitioning, periodic Hadoop
Streaming MapReduce execution, non-overlapping job locking, and execution metrics logging.
"""

import os
import sys
import time
import signal
import logging
import argparse
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any

from ingestion.weather_generator import WeatherDataGenerator
from ingestion.weather_api import WeatherAPIClient
from ingestion.validator import WeatherRecordValidator
from ingestion.hdfs_uploader import HDFSUploader
from ingestion.pipeline_orchestrator import PipelineOrchestrator

# Setup Logging
logger = logging.getLogger("weather_pipeline.continuous")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

JOB_HISTORY_HEADER = "job_id,timestamp,duration_seconds,records_processed,cities_count,status,engine\n"
HISTORICAL_ANALYTICS_HEADER = "snapshot_time,city,record_count,avg_temp,min_temp,max_temp,avg_hum,min_hum,max_hum,total_rain,max_rain,avg_wind,max_wind,avg_press,min_press,anomalies_count\n"


class ContinuousPipelineController:
    """
    Manages continuous near-real-time ingestion and periodic Hadoop Streaming MapReduce jobs.
    Ensures safe concurrency with non-overlapping execution locks and maintains historical audit logs.
    """

    def __init__(
        self,
        ingestion_interval: float = 3.0,
        processing_interval: float = 15.0,
        source_mode: str = "SIMULATOR",  # "SIMULATOR" or "API"
        hdfs_root: str = "/weather",
        output_dir: str = os.path.join("data", "processed"),
        anomaly_ratio: float = 0.05
    ):
        self.ingestion_interval = ingestion_interval
        self.processing_interval = processing_interval
        self.source_mode = source_mode
        self.hdfs_root = hdfs_root
        self.output_dir = output_dir
        self.anomaly_ratio = anomaly_ratio

        # Synchronization and state
        self._stop_event = threading.Event()
        self._job_lock = threading.Lock()
        self._total_records_ingested = 0
        self._job_counter = 0
        self._is_processing = False

        # Initialize Subsystems
        self.validator = WeatherRecordValidator()
        self.generator = WeatherDataGenerator(anomaly_ratio=self.anomaly_ratio, validator=self.validator)
        self.api_client = WeatherAPIClient(validator=self.validator)
        self.uploader = HDFSUploader(hdfs_root=self.hdfs_root)
        self.orchestrator = PipelineOrchestrator(hdfs_root=self.hdfs_root)

        # Ensure output directories exist
        os.makedirs(self.output_dir, exist_ok=True)
        self.history_csv = os.path.join(self.output_dir, "job_history.csv")
        self.historical_analytics_csv = os.path.join(self.output_dir, "historical_analytics.csv")
        self.analytics_summary_csv = os.path.join(self.output_dir, "analytics_summary.csv")

        self._init_history_files()

    def _init_history_files(self):
        """Initializes job audit and historical tracking CSV files if not present."""
        if not os.path.exists(self.history_csv):
            with open(self.history_csv, "w", encoding="utf-8") as f:
                f.write(JOB_HISTORY_HEADER)

        if not os.path.exists(self.historical_analytics_csv):
            with open(self.historical_analytics_csv, "w", encoding="utf-8") as f:
                f.write(HISTORICAL_ANALYTICS_HEADER)

    def ingest_single_cycle(self) -> Optional[str]:
        """
        Generates or fetches a micro-batch of weather records, validates them,
        saves to local batch CSV, and commits to partitioned HDFS.
        """
        try:
            records: List[Dict[str, Any]] = []
            if self.source_mode == "API" and self.api_client.is_configured():
                records = self.api_client.fetch_all_cities()
            else:
                records = self.generator.generate_city_batch()

            if not records:
                logger.warning("No records acquired during ingestion cycle.")
                return None

            # Write batch file
            now = datetime.now()
            batch_filename = f"batch_{now.strftime('%Y%m%d_%H%M%S_%f')[:19]}.csv"
            batch_local_path = os.path.join("data", "generated", batch_filename)
            self.generator.write_batch_to_csv(records, batch_local_path)

            # Upload to HDFS partition /weather/raw/YYYY/MM/DD
            upload_res = self.uploader.upload_file(batch_local_path, dt=now)
            self._total_records_ingested += len(records)
            logger.info("Ingested %d records -> HDFS: %s (Total Ingested: %d)", len(records), upload_res["target_hdfs_path"], self._total_records_ingested)
            return batch_local_path

        except Exception as exc:
            logger.error("Error in ingestion cycle: %s", str(exc), exc_info=True)
            return None

    def execute_hadoop_job_cycle(self) -> Optional[Dict[str, Any]]:
        """
        Executes a periodic Hadoop Streaming analytics cycle across all accumulated HDFS records.
        Employs non-blocking mutex lock to prevent concurrent/overlapping MapReduce jobs.
        """
        # Acquire lock without blocking; if already running, skip this trigger cycle
        acquired = self._job_lock.acquire(blocking=False)
        if not acquired:
            logger.warning("[CONCURRENCY NOTICE] A Hadoop Streaming job is already running. Skipping overlapping trigger.")
            return None

        job_start_time = time.time()
        self._job_counter += 1
        job_id = f"JOB_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self._job_counter:04d}"
        self._is_processing = True

        logger.info(">>> [%s] Initiating Periodic Hadoop Streaming Analytics Job...", job_id)
        job_metrics = {
            "job_id": job_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "duration_seconds": 0.0,
            "records_processed": self._total_records_ingested,
            "cities_count": 0,
            "status": "FAILED",
            "engine": "YARN" if self.orchestrator.streaming_jar else "LOCAL_STREAMING"
        }

        try:
            # Combine sample base data and generated batches for analytics processing
            source_candidates = [
                os.path.join("data", "sample", "sample_weather_data.csv"),
                os.path.join("data", "generated")
            ]
            primary_source = source_candidates[0] if os.path.exists(source_candidates[0]) else "data/generated"

            # Execute MapReduce pipeline
            res = self.orchestrator.run_pipeline(
                raw_source_file=primary_source,
                output_csv_path=self.analytics_summary_csv
            )

            duration = round(time.time() - job_start_time, 2)
            job_metrics["duration_seconds"] = duration
            job_metrics["cities_count"] = res.get("cities_count", 0)
            job_metrics["status"] = res.get("status", "SUCCESS")
            job_metrics["engine"] = res.get("mode", job_metrics["engine"])

            # Record metrics to job history CSV
            with open(self.history_csv, "a", encoding="utf-8") as hf:
                hf.write(
                    f"{job_metrics['job_id']},{job_metrics['timestamp']},{job_metrics['duration_seconds']},"
                    f"{job_metrics['records_processed']},{job_metrics['cities_count']},{job_metrics['status']},"
                    f"{job_metrics['engine']}\n"
                )

            # Append historical timeseries analytics snapshots for trend charting
            self._append_historical_snapshot(job_metrics["timestamp"])

            logger.info("<<< [%s] Completed successfully in %.2fs (Cities Analyzed: %d)", job_id, duration, job_metrics["cities_count"])
            return job_metrics

        except Exception as exc:
            duration = round(time.time() - job_start_time, 2)
            job_metrics["duration_seconds"] = duration
            job_metrics["status"] = f"ERROR: {str(exc)}"
            logger.error("[%s] MapReduce execution failed: %s", job_id, str(exc), exc_info=True)
            return job_metrics

        finally:
            self._is_processing = False
            self._job_lock.release()

    def _append_historical_snapshot(self, snapshot_timestamp: str):
        """Appends the latest analytics summary to the persistent historical trend log."""
        if not os.path.exists(self.analytics_summary_csv):
            return

        with open(self.analytics_summary_csv, "r", encoding="utf-8") as sf:
            lines = [line.strip() for line in sf.readlines() if line.strip()]

        if len(lines) <= 1:
            return

        # Skip header
        data_rows = lines[1:]
        with open(self.historical_analytics_csv, "a", encoding="utf-8") as hf:
            for row in data_rows:
                hf.write(f"{snapshot_timestamp},{row}\n")

    def run_continuous(self, max_cycles: Optional[int] = None):
        """
        Runs the near-real-time dual-loop controller until interrupted or max_cycles reached.
        """
        logger.info("==========================================================")
        logger.info(" Starting Near-Real-Time Weather Analytics Controller     ")
        logger.info(" Ingestion Interval  : %.1f seconds", self.ingestion_interval)
        logger.info(" Processing Interval : %.1f seconds", self.processing_interval)
        logger.info(" Source Mode         : %s", self.source_mode)
        logger.info(" Output Directory    : %s", self.output_dir)
        logger.info("==========================================================")

        last_processing_time = 0.0
        cycle_count = 0

        # Handle SIGINT and SIGTERM gracefully
        def signal_handler(signum, frame):
            logger.info("Signal %d received. Initiating graceful shutdown...", signum)
            self.stop()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        try:
            while not self._stop_event.is_set():
                cycle_count += 1
                current_time = time.time()

                # 1. Continuous Ingestion Cycle
                self.ingest_single_cycle()

                # 2. Check if Processing Interval Elapsed
                if current_time - last_processing_time >= self.processing_interval:
                    self.execute_hadoop_job_cycle()
                    last_processing_time = time.time()

                if max_cycles and cycle_count >= max_cycles:
                    logger.info("Reached configured max_cycles (%d). Stopping.", max_cycles)
                    break

                # Sleep ingestion interval or until stop event
                self._stop_event.wait(timeout=self.ingestion_interval)

        except KeyboardInterrupt:
            logger.info("Controller interrupted by user keyboard.")
        finally:
            self.stop()
            logger.info("Controller stopped. Total records ingested: %d. Total jobs: %d", self._total_records_ingested, self._job_counter)

    def stop(self):
        """Signals background controller loops to stop cleanly."""
        self._stop_event.set()


def main():
    parser = argparse.ArgumentParser(description="Near-Real-Time Weather Analytics Pipeline Controller")
    parser.add_argument("--ingest-interval", type=float, default=2.0, help="Ingestion interval in seconds")
    parser.add_argument("--proc-interval", type=float, default=6.0, help="Hadoop MapReduce processing interval in seconds")
    parser.add_argument("--source", type=str, default="SIMULATOR", choices=["SIMULATOR", "API"], help="Data source mode")
    parser.add_argument("--max-cycles", type=int, default=None, help="Maximum ingestion cycles (default: run indefinitely)")
    parser.add_argument("--anomaly-ratio", type=float, default=0.08, help="Anomaly injection probability")

    args = parser.parse_args()
    controller = ContinuousPipelineController(
        ingestion_interval=args.ingest_interval,
        processing_interval=args.proc_interval,
        source_mode=args.source,
        anomaly_ratio=args.anomaly_ratio
    )
    controller.run_continuous(max_cycles=args.max_cycles)


if __name__ == "__main__":
    main()
