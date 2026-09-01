# ==============================================================================
# Docker Hadoop Cluster Status and Diagnostics Script (PowerShell)
# ==============================================================================

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "      DOCKER HADOOP CLUSTER DIAGNOSTICS REPORT            " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

Write-Host "`n--- 1. CONTAINER STATUS ---" -ForegroundColor Yellow
docker compose ps

Write-Host "`n--- 2. MASTER NODE DAEMONS (hadoop-master) ---" -ForegroundColor Yellow
docker exec hadoop-master jps

Write-Host "`n--- 3. WORKER 1 DAEMONS (hadoop-worker1) ---" -ForegroundColor Yellow
docker exec hadoop-worker1 jps

Write-Host "`n--- 4. WORKER 2 DAEMONS (hadoop-worker2) ---" -ForegroundColor Yellow
docker exec hadoop-worker2 jps

Write-Host "`n--- 5. HDFS DFSADMIN REPORT ---" -ForegroundColor Yellow
docker exec hadoop-master hdfs dfsadmin -report

Write-Host "`n--- 6. YARN ACTIVE NODE LIST ---" -ForegroundColor Yellow
docker exec hadoop-master yarn node -list

Write-Host "`n--- 7. HDFS /weather DIRECTORY LISTING ---" -ForegroundColor Yellow
docker exec hadoop-master hdfs dfs -ls -R /weather

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Diagnostics Report Completed.                            " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
