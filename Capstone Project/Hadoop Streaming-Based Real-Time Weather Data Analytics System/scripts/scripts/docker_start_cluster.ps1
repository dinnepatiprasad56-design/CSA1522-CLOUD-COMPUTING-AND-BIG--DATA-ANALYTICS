# ==============================================================================
# Start 3-Node Local Docker Hadoop Cluster (PowerShell)
# ==============================================================================

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Starting Local 3-Node Docker Hadoop Cluster              " -ForegroundColor Cyan
Write-Host " Network: weather-hadoop-network                          " -ForegroundColor Cyan
Write-Host " Master:  hadoop-master                                   " -ForegroundColor Cyan
Write-Host " Workers: hadoop-worker1, hadoop-worker2                  " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

docker info >$null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Docker daemon is not running. Please start Docker Desktop and retry." -ForegroundColor Red
    exit 1
}

docker compose up -d --build

Write-Host "`n[OK] Docker containers launched!" -ForegroundColor Green
Write-Host "Waiting for cluster services to initialize (15 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

docker compose ps

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Hadoop Web UIs:" -ForegroundColor Green
Write-Host "  - HDFS NameNode      : http://localhost:9870" -ForegroundColor White
Write-Host "  - YARN ResourceMgr   : http://localhost:8088" -ForegroundColor White
Write-Host "  - JobHistory Server  : http://localhost:19888" -ForegroundColor White
Write-Host "  - Weather Dashboard  : http://localhost:8501" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Cyan
