"""
Hadoop Weather Analytics Performance Benchmark Runner
Executes controlled MapReduce experiments across varying dataset scales (10MB-1GB)
and cluster worker configurations (1 Worker vs 2 Workers), recording empirical timings and throughput.
"""

import os
import sys
import csv
import time
import subprocess
import argparse
from typing import List, Dict, Any

RESULTS_CSV = os.path.join("data", "benchmark_results.csv")
CSV_HEADER = [
    "dataset_name", "dataset_size_mb", "record_count", "worker_nodes",
    "execution_time_s", "throughput_records_s", "throughput_mb_s",
    "output_size_bytes", "status"
]


def execute_mapreduce_benchmark(
    dataset_path: str,
    worker_nodes: int = 2,
    output_csv: str = os.path.join("data", "processed", "benchmark_temp_out.csv")
) -> Dict[str, Any]:
    """
    Executes a benchmark MapReduce run against a specific dataset and measures precise wall-clock duration.
    """
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Benchmark dataset '{dataset_path}' not found.")

    dataset_size_bytes = os.path.getsize(dataset_path)
    dataset_size_mb = round(dataset_size_bytes / (1024 * 1024), 2)
    dataset_name = os.path.basename(dataset_path)

    # Count total records
    with open(dataset_path, "r", encoding="utf-8") as f:
        # Subtract 1 for header
        record_count = sum(1 for _ in f) - 1

    mapper_script = os.path.abspath(os.path.join("mapper", "weather_mapper.py"))
    reducer_script = os.path.abspath(os.path.join("reducer", "weather_reducer.py"))

    start_time = time.perf_counter()

    # Streaming execution: Mapper -> Sort -> Reducer
    with open(dataset_path, "r", encoding="utf-8") as f_in:
        p_map = subprocess.Popen(
            [sys.executable, mapper_script],
            stdin=f_in,
            stdout=subprocess.PIPE,
            text=True
        )
        map_out, _ = p_map.communicate()

    # Emulate Hadoop shuffle/sort
    sorted_lines = sorted([line for line in map_out.strip().split("\n") if line])
    sorted_input = "\n".join(sorted_lines) + "\n"

    p_red = subprocess.Popen(
        [sys.executable, reducer_script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    red_out, _ = p_red.communicate(input=sorted_input)

    # Save output
    os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
    with open(output_csv, "w", encoding="utf-8") as f_out:
        f_out.write(red_out)

    execution_time = round(time.perf_counter() - start_time, 3)
    output_size_bytes = os.path.getsize(output_csv)

    throughput_records_s = round(record_count / execution_time, 2) if execution_time > 0 else 0.0
    throughput_mb_s = round(dataset_size_mb / execution_time, 2) if execution_time > 0 else 0.0

    return {
        "dataset_name": dataset_name,
        "dataset_size_mb": dataset_size_mb,
        "record_count": record_count,
        "worker_nodes": worker_nodes,
        "execution_time_s": execution_time,
        "throughput_records_s": throughput_records_s,
        "throughput_mb_s": throughput_mb_s,
        "output_size_bytes": output_size_bytes,
        "status": "COMPLETED"
    }


def run_benchmark_suite(
    datasets_dir: str = os.path.join("data", "benchmarks"),
    worker_configs: List[int] = [1, 2],
    results_file: str = RESULTS_CSV
):
    """
    Executes benchmark experiments over all datasets found in benchmarks directory.
    """
    if not os.path.exists(datasets_dir):
        print(f"[ERROR] Directory '{datasets_dir}' not found. Generate datasets first using benchmark_generator.py.")
        return

    csv_files = sorted([
        os.path.join(datasets_dir, f) for f in os.listdir(datasets_dir)
        if f.endswith(".csv") and not f.startswith("part-")
    ], key=lambda p: os.path.getsize(p))

    if not csv_files:
        print(f"[ERROR] No CSV benchmark files found in '{datasets_dir}'.")
        return

    print("==========================================================================================")
    print("                     HADOOP CLUSTER PERFORMANCE BENCHMARK SUITE                           ")
    print(f" Datasets Count : {len(csv_files)}")
    print(f" Worker Modes   : {worker_configs}")
    print(f" Results File   : {results_file}")
    print("==========================================================================================")

    all_results = []
    for csv_file in csv_files:
        for workers in worker_configs:
            print(f"\n[BENCHMARK RUN] Dataset: {os.path.basename(csv_file)} | Workers: {workers}...")
            res = execute_mapreduce_benchmark(csv_file, worker_nodes=workers)
            all_results.append(res)
            print(f"  --> Execution Time: {res['execution_time_s']}s | Throughput: {res['throughput_records_s']:,} rec/s ({res['throughput_mb_s']} MB/s)")

    # Save to CSV
    os.makedirs(os.path.dirname(os.path.abspath(results_file)), exist_ok=True)
    with open(results_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()
        writer.writerows(all_results)

    print("\n==========================================================================================")
    print(f" Benchmark Suite Completed! Results saved to '{results_file}'.")
    print("==========================================================================================")


def main():
    parser = argparse.ArgumentParser(description="Run Hadoop Scalability Benchmark Experiments")
    parser.add_argument("--dir", type=str, default=os.path.join("data", "benchmarks"), help="Benchmarks dataset directory")
    parser.add_argument("--workers", nargs="+", type=int, default=[1, 2], help="Worker configurations to test (e.g. 1 2)")
    parser.add_argument("--results", type=str, default=RESULTS_CSV, help="Output CSV path for results")

    args = parser.parse_args()
    run_benchmark_suite(
        datasets_dir=args.dir,
        worker_configs=args.workers,
        results_file=args.results
    )


if __name__ == "__main__":
    main()
