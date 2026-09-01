"""
HDFS Uploader Module
Orchestrates uploading raw weather batches from the local filesystem to HDFS partitions
following the hierarchical structure /weather/raw/YYYY/MM/DD.
"""

import os
import shutil
import logging
import subprocess
from datetime import datetime
from typing import Optional, List, Dict, Any

logger = logging.getLogger("weather_ingestion.hdfs_uploader")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class HDFSUploader:
    """
    Manages HDFS directory creation, file transfers, and partition tracking.
    Falls back gracefully to local simulated HDFS mirroring when running in development mode.
    """

    def __init__(
        self,
        hdfs_root: str = "/weather",
        hadoop_home: Optional[str] = None,
        dry_run: bool = False,
        mock_local_dir: Optional[str] = None
    ):
        self.hdfs_root = hdfs_root.rstrip("/")
        self.hadoop_home = hadoop_home or os.getenv("HADOOP_HOME")
        self.dry_run = dry_run
        self.mock_local_dir = mock_local_dir or os.path.join("data", "hdfs_mock")
        self.hdfs_bin = self._find_hdfs_binary()
        
        if not self.hdfs_bin:
            logger.info("Hadoop CLI not detected in system PATH. Enabling local simulated HDFS mode at '%s'", self.mock_local_dir)

    def _find_hdfs_binary(self) -> Optional[str]:
        """Locates the 'hdfs' executable from PATH or HADOOP_HOME."""
        # 1. Check system PATH
        hdfs_path = shutil.which("hdfs")
        if hdfs_path:
            return hdfs_path
        
        # 2. Check HADOOP_HOME/bin
        if self.hadoop_home:
            candidate = os.path.join(self.hadoop_home, "bin", "hdfs")
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                return candidate
            candidate_win = os.path.join(self.hadoop_home, "bin", "hdfs.cmd")
            if os.path.isfile(candidate_win):
                return candidate_win

        return None

    def get_partition_path(self, dt: Optional[datetime] = None) -> str:
        """
        Computes the target HDFS directory partition: /weather/raw/YYYY/MM/DD
        """
        dt = dt or datetime.now()
        year = dt.strftime("%Y")
        month = dt.strftime("%m")
        day = dt.strftime("%d")
        return f"{self.hdfs_root}/raw/{year}/{month}/{day}"

    def make_hdfs_directory(self, hdfs_dir: str) -> bool:
        """
        Creates directory in HDFS if it does not already exist (equivalent to hdfs dfs -mkdir -p).
        """
        if self.dry_run or not self.hdfs_bin:
            simulated_path = os.path.join(self.mock_local_dir, hdfs_dir.lstrip("/"))
            os.makedirs(simulated_path, exist_ok=True)
            logger.info("[MOCK HDFS] Created directory: %s", simulated_path)
            return True

        cmd = [self.hdfs_bin, "dfs", "-mkdir", "-p", hdfs_dir]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if res.returncode == 0:
                logger.debug("HDFS mkdir success: %s", hdfs_dir)
                return True
            else:
                logger.error("HDFS mkdir failed: %s (Error: %s)", hdfs_dir, res.stderr.strip())
                return False
        except Exception as exc:
            logger.error("Exception executing HDFS mkdir: %s", str(exc))
            return False

    def upload_file(self, local_filepath: str, custom_hdfs_dir: Optional[str] = None, dt: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Uploads a local CSV file to the corresponding partitioned HDFS directory.
        """
        if not os.path.isfile(local_filepath):
            raise FileNotFoundError(f"Local file '{local_filepath}' does not exist.")

        filename = os.path.basename(local_filepath)
        target_dir = custom_hdfs_dir or self.get_partition_path(dt)
        target_hdfs_path = f"{target_dir}/{filename}"

        self.make_hdfs_directory(target_dir)

        result: Dict[str, Any] = {
            "local_file": local_filepath,
            "target_hdfs_path": target_hdfs_path,
            "success": False,
            "mode": "REAL_HDFS" if (self.hdfs_bin and not self.dry_run) else "SIMULATED_HDFS"
        }

        if self.dry_run or not self.hdfs_bin:
            # Simulate HDFS storage locally
            dest_dir = os.path.join(self.mock_local_dir, target_dir.lstrip("/"))
            os.makedirs(dest_dir, exist_ok=True)
            dest_file = os.path.join(dest_dir, filename)
            shutil.copy2(local_filepath, dest_file)
            result["success"] = True
            result["simulated_path"] = dest_file
            logger.info("[SIMULATED HDFS] Uploaded '%s' -> '%s'", local_filepath, target_hdfs_path)
            return result

        # Genuine HDFS CLI invocation
        cmd = [self.hdfs_bin, "dfs", "-put", "-f", local_filepath, target_hdfs_path]
        try:
            logger.info("Uploading '%s' to HDFS '%s'...", local_filepath, target_hdfs_path)
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if res.returncode == 0:
                result["success"] = True
                logger.info("Successfully uploaded '%s' to HDFS '%s'", local_filepath, target_hdfs_path)
            else:
                result["error"] = res.stderr.strip()
                logger.error("Failed to upload '%s' to HDFS: %s", local_filepath, res.stderr.strip())
        except Exception as exc:
            result["error"] = str(exc)
            logger.error("Exception during HDFS upload of '%s': %s", local_filepath, str(exc))

        return result

    def list_hdfs_files(self, hdfs_dir: str) -> List[str]:
        """
        Lists files in an HDFS directory.
        """
        if self.dry_run or not self.hdfs_bin:
            simulated_path = os.path.join(self.mock_local_dir, hdfs_dir.lstrip("/"))
            if not os.path.exists(simulated_path):
                return []
            return [os.path.join(hdfs_dir, f).replace("\\", "/") for f in os.listdir(simulated_path)]

        cmd = [self.hdfs_bin, "dfs", "-ls", hdfs_dir]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if res.returncode != 0:
                return []
            lines = res.stdout.strip().split("\n")
            files = []
            for line in lines:
                parts = line.split()
                if len(parts) >= 8:
                    files.append(parts[-1])
            return files
        except Exception as exc:
            logger.error("Exception listing HDFS directory '%s': %s", hdfs_dir, str(exc))
            return []


def main():
    """Command Line Interface for HDFS Ingestion Uploader."""
    import argparse
    parser = argparse.ArgumentParser(description="HDFS Ingestion Uploader for Weather Records")
    parser.add_argument("--file", type=str, help="Path to single local CSV file to upload")
    parser.add_argument("--dir", type=str, help="Directory containing CSV batches to upload")
    parser.add_argument("--hdfs-root", type=str, default="/weather", help="HDFS root directory")
    parser.add_argument("--dry-run", action="store_true", help="Force local simulated HDFS mode")

    args = parser.parse_args()
    uploader = HDFSUploader(hdfs_root=args.hdfs_root, dry_run=args.dry_run)

    if args.file:
        res = uploader.upload_file(args.file)
        print(f"Uploaded File: {res}")
    elif args.dir:
        if not os.path.isdir(args.dir):
            print(f"Error: Directory '{args.dir}' not found.")
            return
        files = [os.path.join(args.dir, f) for f in os.listdir(args.dir) if f.endswith(".csv")]
        print(f"Found {len(files)} CSV files to upload in '{args.dir}'...")
        for f in files:
            res = uploader.upload_file(f)
            print(f" - {res['local_file']} -> {res['target_hdfs_path']} ({res['mode']})")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

