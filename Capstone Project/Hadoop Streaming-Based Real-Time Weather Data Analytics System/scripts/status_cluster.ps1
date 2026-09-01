# ==============================================================================
# Status Cluster Shortcut (PowerShell)
# ==============================================================================
$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
& "$PSScriptRoot\docker_status_cluster.ps1"
