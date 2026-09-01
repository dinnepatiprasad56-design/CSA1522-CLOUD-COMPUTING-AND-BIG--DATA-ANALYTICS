"""
Weather Analytics Pipeline Orchestrator
Cross-platform pipeline manager orchestrating ingestion, HDFS uploads,
Hadoop Streaming MapReduce execution, and processed output exports.
"""

import os
import sys
import time
import shutil
import logging
import argparse
import subprocess
from datetime import datetime
from typing import Dict, Any, Optional

from ingestion.validator import WeatherRecordValidator
from ingestion.hdfs_uploader import HDFSUploader

logger = logging.getLogger("weather_pipeline.orchestrator")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

ANALYTICS_CSV_HEADER = [
    "city", "record_count", "avg_temperature", "min_temperature", "max_temperature",
    "avg_humidity", "min_humidity", "max_humidity", "total_rainfall", "max_rainfall",
    "avg_wind_speed", "max_wind_speed", "avg_pressure", "min_pressure", "anomalies_count"
]


class PipelineOrchestrator:
    """
    Coordinates the end-to-end meteorological analytics pipeline:
    Raw Data -> Validator -> HDFS Partition -> Hadoop Streaming -> Processed Analytics CSV.
    """

    def __init__(
        self,
        hdfs_root: str = "/weather",
        hadoop_home: Optional[str] = None,
        streaming_jar: Optional[str] = None
    ):
        self.hdfs_root = hdfs_root
        self.hadoop_home = hadoop_home or os.getenv("HADOOP_HOME")
        self.streaming_jar = streaming_jar or os.getenv("HADOOP_STREAMING_JAR")
        self.validator = WeatherRecordValidator()
        self.uploader = HDFSUploader(hdfs_root=self.hdfs_root, hadoop_home=self.hadoop_home)

    def run_pipeline(
        self,
        raw_source_file: str,
        hdfs_output_dir: str = "/weather/output/analytics_summary",
        output_csv_path: str = os.path.join("data", "processed", "analytics_summary.csv"),
        num_reducers: int = 2
    ) -> Dict[str, Any]:
        """
        Executes the full pipeline workflow.
        """
        start_time = time.time()
        logger.info("=== Starting Weather Analytics Pipeline Execution ===")
        logger.info("Source Raw File : %s", raw_source_file)
        logger.info("HDFS Output Dir : %s", hdfs_output_dir)
        logger.info("Export CSV Path : %s", output_csv_path)

        if not os.path.isfile(raw_source_file):
            raise FileNotFoundError(f"Raw source data file '{raw_source_file}' does not exist.")

        # Step 1: Upload to HDFS
        logger.info("[1/4] Ingesting & Uploading Raw Data to HDFS...")
        upload_res = self.uploader.upload_file(raw_source_file)
        logger.info("Data uploaded successfully (Mode: %s)", upload_res["mode"])

        # Step 2: Execute Hadoop Streaming MapReduce
        logger.info("[2/4] Executing Hadoop Streaming MapReduce...")
        mapper_script = os.path.abspath(os.path.join("mapper", "weather_mapper.py"))
        reducer_script = os.path.abspath(os.path.join("reducer", "weather_reducer.py"))

        is_cluster_mode = bool(self.uploader.hdfs_bin and self.hadoop_home and self.streaming_jar)
        tsv_lines = []

        if is_cluster_mode:
            logger.info("Submitting distributed job to YARN...")
            # Clean old output
            subprocess.run([self.uploader.hdfs_bin, "dfs", "-rm", "-r", "-f", hdfs_output_dir], capture_output=True)
            
            cmd = [
                "hadoop", "jar", self.streaming_jar,
                "-D", f"mapreduce.job.reduces={num_reducers}",
                "-D", "mapreduce.job.name=Weather_Analytics_Pipeline",
                "-files", f"{mapper_script},{reducer_script}",
                "-mapper", f"python3 {os.path.basename(mapper_script)}",
                "-reducer", f"python3 {os.path.basename(reducer_script)}",
                "-input", self.uploader.get_partition_path(),
                "-output", hdfs_output_dir
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                logger.error("Hadoop Streaming job failed: %s", res.stderr)
                raise RuntimeError(f"Hadoop job execution failed: {res.stderr}")

            # Fetch output from HDFS
            cat_cmd = [self.uploader.hdfs_bin, "dfs", "-cat", f"{hdfs_output_dir}/part-*"]
            cat_res = subprocess.run(cat_cmd, capture_output=True, text=True)
            tsv_lines = cat_res.stdout.strip().split("\n")
        else:
            logger.info("Executing streaming pipeline locally (development emulation mode)...")
            # Local Stream Map -> Sort -> Reduce
            with open(raw_source_file, "r", encoding="utf-8") as rf:
                raw_data = rf.read()

            p_map = subprocess.Popen([sys.executable, mapper_script], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
            map_out, _ = p_map.communicate(input=raw_data)

            # Sort keys
            sorted_lines = sorted([line for line in map_out.strip().split("\n") if line])
            sorted_data = "\n".join(sorted_lines) + "\n"

            p_red = subprocess.Popen([sys.executable, reducer_script], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
            red_out, _ = p_red.communicate(input=sorted_data)
            tsv_lines = [line.strip() for line in red_out.strip().split("\n") if line.strip()]

        # Step 3: Format and Export CSV
        logger.info("[3/4] Formatting & Exporting Processed Analytics to CSV...")
        os.makedirs(os.path.dirname(os.path.abspath(output_csv_path)), exist_ok=True)

        csv_rows = [",".join(ANALYTICS_CSV_HEADER)]
        for line in tsv_lines:
            tokens = line.split("\t")
            if len(tokens) == len(ANALYTICS_CSV_HEADER):
                csv_rows.append(",".join(tokens))

        with open(output_csv_path, "w", encoding="utf-8") as out_f:
            out_f.write("\n".join(csv_rows) + "\n")

        elapsed_time = round(time.time() - start_time, 2)
        logger.info("[4/4] Pipeline completed in %.2fs. Saved %d city analytics records to '%s'", elapsed_time, len(csv_rows) - 1, output_csv_path)

        return {
            "status": "SUCCESS",
            "elapsed_seconds": elapsed_time,
            "cities_count": len(csv_rows) - 1,
            "output_file": output_csv_path,
            "mode": "CLUSTER_YARN" if is_cluster_mode else "LOCAL_EMULATION"
        }


def main():
    parser = argparse.ArgumentParser(description="Master Weather Analytics Pipeline Orchestrator")
    parser.add_argument("--source", type=str, default=os.path.join("data", "sample", "sample_weather_data.csv"), help="Raw input CSV dataset")
    parser.add_argument("--hdfs-output", type=str, default="/weather/output/analytics_summary", help="HDFS output directory")
    parser.add_argument("--export-csv", type=str, default=os.path.join("data", "processed", "analytics_summary.csv"), help="Target CSV file for dashboard")
    parser.add_argument("--reducers", type=int, default=2, help="Number of MapReduce reducers")

    args = parser.parse_args()
    orchestrator = PipelineOrchestrator()
    res = orchestrator.run_pipeline(
        raw_source_file=args.source,
        hdfs_output_dir=args.hdfs_output,
        output_csv_path=args.export_csv,
        num_reducers=args.reducers
    )
    print("\n--- Pipeline Execution Summary ---")
    for k, v in res.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
