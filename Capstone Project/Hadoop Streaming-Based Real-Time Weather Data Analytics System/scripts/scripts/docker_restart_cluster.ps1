# ==============================================================================
# Restart 3-Node Local Docker Hadoop Cluster (PowerShell)
# ==============================================================================

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Restarting Local 3-Node Docker Hadoop Cluster            " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

docker compose restart

Write-Host "[OK] Cluster containers restarted." -ForegroundColor Green
docker compose ps
