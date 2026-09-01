# ==============================================================================
# Stop 3-Node Local Docker Hadoop Cluster (PowerShell)
# ==============================================================================

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Stopping Local 3-Node Docker Hadoop Cluster              " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

docker compose stop

Write-Host "[OK] Cluster containers stopped safely. Persistent HDFS data volumes preserved." -ForegroundColor Green
