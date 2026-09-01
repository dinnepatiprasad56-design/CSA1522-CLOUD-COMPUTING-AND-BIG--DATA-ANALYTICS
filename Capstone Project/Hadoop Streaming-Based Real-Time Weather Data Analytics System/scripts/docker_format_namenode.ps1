# ==============================================================================
# Explicit NameNode Re-formatting Script for Local Docker Cluster (PowerShell)
# WARNING: Clears HDFS metadata and re-initializes filesystem
# ==============================================================================

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "==========================================================" -ForegroundColor Red
Write-Host "      HDFS NAMENODE EXPLICIT FORMATTING SCRIPT            " -ForegroundColor Red
Write-Host " WARNING: This will purge and reset all HDFS metadata.    " -ForegroundColor Red
Write-Host "==========================================================" -ForegroundColor Red

Write-Host "`n[1/4] Stopping cluster containers..." -ForegroundColor Yellow
docker compose stop

Write-Host "`n[2/4] Removing HDFS data volumes..." -ForegroundColor Yellow
docker volume rm namenode_data datanode1_data datanode2_data hadoop_logs 2>$null

Write-Host "`n[3/4] Re-launching cluster containers..." -ForegroundColor Yellow
docker compose up -d

Write-Host "Waiting 15 seconds for NameNode initialization..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host "`n[4/4] Verifying HDFS initialization..." -ForegroundColor Yellow
docker exec hadoop-master hdfs dfs -ls /weather

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " NameNode re-formatting and directory setup complete!     " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
