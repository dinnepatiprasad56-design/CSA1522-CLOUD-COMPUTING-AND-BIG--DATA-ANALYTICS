# ==============================================================================
# Verify Cluster Shortcut (PowerShell)
# ==============================================================================
$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
& "$PSScriptRoot\docker_verify_cluster.ps1"
