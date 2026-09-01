"""
Hadoop Weather Analytics Scalability Dataset Generator
Generates precise benchmark datasets (10MB, 50MB, 100MB, 500MB, 1GB)
for cluster performance evaluation.
"""

import os
import time
import math
import random
import argparse
from datetime import datetime, timedelta

CITIES = ["Chennai", "Bengaluru", "Hyderabad", "Mumbai", "Delhi", "Kolkata", "Pune"]


def generate_benchmark_file(target_mb: float, output_path: str, chunk_size: int = 10000) -> dict:
    """
    Streams realistic CSV weather records to disk until reaching the target file size in MB.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    target_bytes = int(target_mb * 1024 * 1024)
    start_time = time.time()

    base_dt = datetime(2026, 8, 1, 0, 0, 0)
    record_count = 0
    bytes_written = 0

    header = "timestamp,city,temperature,humidity,rainfall,wind_speed,pressure\n"
    header_bytes = len(header.encode("utf-8"))

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        f.write(header)
        bytes_written += header_bytes

        buffer = []
        while bytes_written < target_bytes:
            for _ in range(chunk_size):
                record_count += 1
                dt = base_dt + timedelta(minutes=record_count * 2)
                city = CITIES[record_count % len(CITIES)]
                
                # Synthetic realistic variation
                hour = dt.hour + (dt.minute / 60.0)
                solar = math.sin(math.radians((hour - 8) * 15))
                temp = round(28.0 + (solar * 6.0) + random.uniform(-1.0, 1.0), 2)
                hum = round(max(15.0, min(95.0, 65.0 - (solar * 15.0) + random.uniform(-3.0, 3.0))), 2)
                rain = round(random.expovariate(0.1) if random.random() < 0.25 else 0.0, 2)
                wind = round(max(2.0, 12.0 + (solar * 3.0) + random.uniform(-2.0, 3.0)), 2)
                press = round(995.0 + (math.cos(math.radians(hour * 30)) * 1.5) + random.uniform(-0.5, 0.5), 2)

                line = f"{dt.strftime('%Y-%m-%dT%H:%M:%S')},{city},{temp:.2f},{hum:.2f},{rain:.2f},{wind:.2f},{press:.2f}\n"
                buffer.append(line)

            chunk_text = "".join(buffer)
            chunk_bytes = len(chunk_text.encode("utf-8"))

            if bytes_written + chunk_bytes > target_bytes and bytes_written > 0:
                # Trim excess rows to meet size precisely
                for line in buffer:
                    line_b = len(line.encode("utf-8"))
                    if bytes_written + line_b > target_bytes:
                        break
                    f.write(line)
                    bytes_written += line_b
                break

            f.write(chunk_text)
            bytes_written += chunk_bytes
            buffer.clear()

    elapsed = round(time.time() - start_time, 2)
    actual_mb = round(os.path.getsize(output_path) / (1024 * 1024), 2)

    return {
        "file_path": output_path,
        "target_mb": target_mb,
        "actual_mb": actual_mb,
        "record_count": record_count,
        "generation_time_s": elapsed
    }


def main():
    parser = argparse.ArgumentParser(description="Generate Benchmark Datasets for Hadoop Evaluation")
    parser.add_argument("--sizes", nargs="+", type=float, default=[10, 50, 100], help="Sizes in MB (e.g. 10 50 100 500 1000)")
    parser.add_argument("--out-dir", type=str, default=os.path.join("data", "benchmarks"), help="Output directory")

    args = parser.parse_args()
    print("==========================================================")
    print("      HADOOP WEATHER BENCHMARK DATASET GENERATOR          ")
    print("==========================================================")
    for size in args.sizes:
        filename = f"weather_{int(size) if size.is_integer() else size}MB.csv"
        out_file = os.path.join(args.out_dir, filename)
        print(f"[GENERATING] Target: {size} MB -> '{out_file}'...")
        res = generate_benchmark_file(target_mb=size, output_path=out_file)
        print(f"  [DONE] Size: {res['actual_mb']} MB | Records: {res['record_count']:,} | Time: {res['generation_time_s']}s")
    print("==========================================================")


if __name__ == "__main__":
    main()
