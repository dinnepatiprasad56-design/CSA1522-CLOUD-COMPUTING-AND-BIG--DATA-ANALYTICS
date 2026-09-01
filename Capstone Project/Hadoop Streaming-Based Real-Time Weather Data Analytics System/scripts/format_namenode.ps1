# ==============================================================================
# Format NameNode Shortcut (PowerShell)
# ==============================================================================
$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
& "$PSScriptRoot\docker_format_namenode.ps1"
