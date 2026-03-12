<#
.SYNOPSIS
    Install or uninstall linkedin-cli on Windows.
.DESCRIPTION
    Downloads the latest linkedin-cli release from GitHub and installs it
    to %LOCALAPPDATA%\linkedin-cli. Adds the directory to the user PATH.
.PARAMETER Uninstall
    Remove linkedin-cli and clean up PATH.
.EXAMPLE
    irm https://raw.githubusercontent.com/sabania/linkedin-cli/master/install.ps1 | iex
#>
param([switch]$Uninstall)

$ErrorActionPreference = "Stop"
$repo = "sabania/linkedin-cli"
$installDir = "$env:LOCALAPPDATA\linkedin-cli"

function Remove-FromPath($dir) {
    $current = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($current -like "*$dir*") {
        $parts = $current -split ";" | Where-Object { $_ -ne $dir -and $_ -ne "" }
        [Environment]::SetEnvironmentVariable("Path", ($parts -join ";"), "User")
    }
}

if ($Uninstall) {
    if (Test-Path $installDir) {
        Remove-Item $installDir -Recurse -Force
        Write-Host "Removed $installDir"
    }
    Remove-FromPath $installDir
    Write-Host "linkedin-cli uninstalled. Restart your terminal."
    return
}

# Get latest release
Write-Host "Fetching latest release..."
$release = Invoke-RestMethod "https://api.github.com/repos/$repo/releases/latest"
$version = $release.tag_name
$asset = $release.assets | Where-Object { $_.name -eq "linkedin-cli-windows.zip" }
if (-not $asset) {
    Write-Error "No Windows binary found in release $version"
    return
}
$url = $asset.browser_download_url

# Download
$zip = "$env:TEMP\linkedin-cli-windows.zip"
Write-Host "Downloading linkedin-cli $version..."
Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing

# Clean previous install
if (Test-Path $installDir) {
    Remove-Item $installDir -Recurse -Force
}

# Extract
Write-Host "Installing to $installDir..."
New-Item -ItemType Directory -Path $installDir -Force | Out-Null
Expand-Archive -Path $zip -DestinationPath $installDir -Force
Remove-Item $zip -Force

# Add to PATH (persistent + current session)
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$installDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$installDir", "User")
    $env:Path = "$env:Path;$installDir"
    Write-Host "Added to PATH."
}

Write-Host ""
Write-Host "linkedin-cli $version installed successfully!" -ForegroundColor Green
Write-Host "Restart your terminal, then run: linkedin-cli --help"
Write-Host ""
Write-Host "Prerequisite: Google Chrome must be installed."
