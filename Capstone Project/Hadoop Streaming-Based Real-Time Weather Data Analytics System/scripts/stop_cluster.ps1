# ==============================================================================
# Stop Cluster Shortcut (PowerShell)
# ==============================================================================
$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
& "$PSScriptRoot\docker_stop_cluster.ps1"
