param(
  [Parameter(Mandatory = $true)]
  [string]$Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
  throw "Video file not found: $Path"
}
if (-not (Get-Command ffprobe -ErrorAction SilentlyContinue)) {
  throw "ffprobe is required. Install FFmpeg and ensure ffprobe is on PATH."
}

$resolved = (Resolve-Path -LiteralPath $Path).Path
$metadataJson = & ffprobe -v error -show_entries format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels -of json "$resolved"
if ($LASTEXITCODE -ne 0) { throw "ffprobe failed." }
$metadata = $metadataJson | ConvertFrom-Json

Write-Host "File: $resolved"
Write-Host ("Size: {0:N2} MiB" -f ((Get-Item -LiteralPath $resolved).Length / 1MB))
Write-Host ("Duration: {0:N2} seconds" -f [double]$metadata.format.duration)
$metadata.streams | Format-Table codec_type, codec_name, width, height, r_frame_rate, sample_rate, channels -AutoSize

if ([double]$metadata.format.duration -le 0) { throw "Invalid duration." }
if (-not ($metadata.streams | Where-Object { $_.codec_type -eq "video" })) { throw "No video stream found." }
Write-Host "Basic MP4 validation passed." -ForegroundColor Green
