Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "Nolane Video Studio - environment check" -ForegroundColor Cyan

function Test-Command([string]$Name) {
  $cmd = Get-Command $Name -ErrorAction SilentlyContinue
  if ($cmd) {
    Write-Host ("[OK] {0}: {1}" -f $Name, $cmd.Source) -ForegroundColor Green
  } else {
    Write-Host ("[MISSING] {0}" -f $Name) -ForegroundColor Yellow
  }
}

Test-Command "node"
Test-Command "npm"
Test-Command "git"
Test-Command "ffmpeg"
Test-Command "ffprobe"
Test-Command "blender"
Test-Command "krita"

if (Get-Command node -ErrorAction SilentlyContinue) {
  $nodeVersion = (& node --version).Trim()
  Write-Host ("Node version: {0}" -f $nodeVersion)
  if ($nodeVersion -notmatch '^v(2[2-9]|[3-9]\d)\.') {
    Write-Warning "Use Node.js 22 LTS or newer for this project."
  }
}

Write-Host ""
Write-Host "Remotion setup:"
Write-Host "  cd video-projects/remotion"
Write-Host "  npm install"
Write-Host "  npm run dev"
Write-Host ""
Write-Host "Optional artist tools:"
Write-Host "  Blender: https://www.blender.org/download/"
Write-Host "  Krita:   https://krita.org/en/download/"
