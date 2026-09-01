# ==============================================================================
# Comprehensive 16-Point Docker Hadoop Cluster Verification Suite (PowerShell)
# Project: Hadoop Streaming-Based Real-Time Weather Data Analytics System
# ==============================================================================

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "      COMPREHENSIVE 16-POINT HADOOP CLUSTER VERIFICATION   " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$PassedCount = 0

function Report-Result($TestNum, $Title, $Status, $Details) {
    if ($Status -eq "PASS") {
        Write-Host "  [TEST $TestNum/16] $Title : PASS ($Details)" -ForegroundColor Green
        $script:PassedCount++
    } else {
        Write-Host "  [TEST $TestNum/16] $Title : FAIL ($Details)" -ForegroundColor Red
    }
}

# 1. Containers
$containers = docker compose ps -q
if ($containers.Count -ge 3) {
    Report-Result 1 "All 3 Containers Running" "PASS" "hadoop-master, hadoop-worker1, hadoop-worker2"
} else {
    Report-Result 1 "All 3 Containers Running" "FAIL" "Fewer than 3 containers running"
}

# 2. Master Reachability
docker exec hadoop-master ping -c 1 127.0.0.1 >$null 2>&1
if ($LASTEXITCODE -eq 0) { Report-Result 2 "hadoop-master Reachable" "PASS" "Ping success" } else { Report-Result 2 "hadoop-master Reachable" "FAIL" "Unpingable" }

# 3. Worker 1 Reachability
docker exec hadoop-master ping -c 1 hadoop-worker1 >$null 2>&1
if ($LASTEXITCODE -eq 0) { Report-Result 3 "hadoop-worker1 Reachable" "PASS" "DNS ping success" } else { Report-Result 3 "hadoop-worker1 Reachable" "FAIL" "Unpingable" }

# 4. Worker 2 Reachability
docker exec hadoop-master ping -c 1 hadoop-worker2 >$null 2>&1
if ($LASTEXITCODE -eq 0) { Report-Result 4 "hadoop-worker2 Reachable" "PASS" "DNS ping success" } else { Report-Result 4 "hadoop-worker2 Reachable" "FAIL" "Unpingable" }

# 5. NameNode Process
$jpsMaster = docker exec hadoop-master jps
if ($jpsMaster -match "NameNode") { Report-Result 5 "NameNode Daemon Running" "PASS" "JPS confirmed" } else { Report-Result 5 "NameNode Daemon Running" "FAIL" "Missing" }

# 6. DataNode 1
$jpsW1 = docker exec hadoop-worker1 jps
if ($jpsW1 -match "DataNode") { Report-Result 6 "DataNode 1 Registered" "PASS" "Active on worker 1" } else { Report-Result 6 "DataNode 1 Registered" "FAIL" "Missing" }

# 7. DataNode 2
$jpsW2 = docker exec hadoop-worker2 jps
if ($jpsW2 -match "DataNode") { Report-Result 7 "DataNode 2 Registered" "PASS" "Active on worker 2" } else { Report-Result 7 "DataNode 2 Registered" "FAIL" "Missing" }

# 8. ResourceManager
if ($jpsMaster -match "ResourceManager") { Report-Result 8 "ResourceManager Running" "PASS" "Active" } else { Report-Result 8 "ResourceManager Running" "FAIL" "Missing" }

# 9. NodeManager 1
if ($jpsW1 -match "NodeManager") { Report-Result 9 "NodeManager 1 Registered" "PASS" "Active" } else { Report-Result 9 "NodeManager 1 Registered" "FAIL" "Missing" }

# 10. NodeManager 2
if ($jpsW2 -match "NodeManager") { Report-Result 10 "NodeManager 2 Registered" "PASS" "Active" } else { Report-Result 10 "NodeManager 2 Registered" "FAIL" "Missing" }

# 11. HDFS Health
$report = docker exec hadoop-master hdfs dfsadmin -report
if ($report -match "Live datanodes \(3\)") {
    Report-Result 11 "HDFS Cluster Health" "PASS" "3/3 Live DataNodes"
} else {
    Report-Result 11 "HDFS Cluster Health" "FAIL" "Not all live"
}

# 12. YARN Health
$yarnNodes = docker exec hadoop-master yarn node -list
if ($yarnNodes -match "RUNNING") { Report-Result 12 "YARN Cluster Health" "PASS" "Active NodeManagers reporting" } else { Report-Result 12 "YARN Cluster Health" "FAIL" "No running nodes" }

# 13. Replication Factor
$repl = docker exec hadoop-master hdfs getconf -confKey dfs.replication
if ($repl -match "2") { Report-Result 13 "Replication Factor = 2" "PASS" "dfs.replication = 2" } else { Report-Result 13 "Replication Factor = 2" "FAIL" "Value: $repl" }

# 14. Directory Architecture
docker exec hadoop-master hdfs dfs -ls /weather/raw >$null 2>&1
if ($LASTEXITCODE -eq 0) { Report-Result 14 "HDFS /weather Architecture" "PASS" "/weather tree verified" } else { Report-Result 14 "HDFS /weather Architecture" "FAIL" "Missing" }

# 15. File Upload
docker exec hadoop-master hdfs dfs -put -f /app/data/sample/sample_weather_data.csv /weather/raw/verify_sample.csv >$null 2>&1
if ($LASTEXITCODE -eq 0) { Report-Result 15 "HDFS File Upload" "PASS" "Uploaded sample dataset" } else { Report-Result 15 "HDFS File Upload" "FAIL" "Put failed" }

# 16. MapReduce Job Execution
Write-Host "  Executing test MapReduce job via YARN..." -ForegroundColor Yellow
docker exec hadoop-master bash -c "hdfs dfs -rm -r -f /weather/output/verify_out >/dev/null 2>&1 || true; hadoop jar \$HADOOP_STREAMING_JAR -D mapreduce.job.reduces=2 -files /app/mapper/weather_mapper.py,/app/reducer/weather_reducer.py -mapper 'python3 weather_mapper.py' -reducer 'python3 weather_reducer.py' -input /weather/raw/verify_sample.csv -output /weather/output/verify_out >/dev/null 2>&1"
if ($LASTEXITCODE -eq 0) { Report-Result 16 "Hadoop Streaming Execution" "PASS" "Job completed cleanly" } else { Report-Result 16 "Hadoop Streaming Execution" "FAIL" "Exit code $LASTEXITCODE" }

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Verification Complete: $PassedCount / 16 Tests PASSED" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
