# ==============================================================================
# Start Cluster Shortcut (PowerShell)
# ==============================================================================
$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
& "$PSScriptRoot\docker_start_cluster.ps1"
