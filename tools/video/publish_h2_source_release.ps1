param(
    [Parameter(Mandatory = $true)]
    [string]$AssetsDir,
    [string]$ReleaseTag = "h2-production-assets-v1"
)

$ErrorActionPreference = "Stop"
$Repository = "Nolane-x/video"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$AssetsDir = (Resolve-Path $AssetsDir).Path

# The hash allow-list protects against uploading a different render/source under a familiar name.
$Expected = @(
    @{ Name = "one-more-scroll-h2-final.mp4"; Required = $true;  Size = 31547778;  Sha = "be0608239a374cf10c89b2c9b16e642de962cdd8f1b177de1a173219413a940f"; Role = "canonical H2 Canvas/Chromium master" },
    @{ Name = "one-more-scroll-h2-source.zip"; Required = $true; Size = 115875783; Sha = "f6f8bed7179c166800b9ba2c79dbd53e12e24050645cee83b44d3ce27c11c42b"; Role = "H2 renderer/source package" },
    @{ Name = "one-more-scroll-h2-source-v2-scene-fixes.zip"; Required = $false; Size = 115856962; Sha = "b8db965db214bf0e37b307d3fe1aa663c55f29ee753fd9103a5972b5fe633014"; Role = "H2 source package with additional, not fully rerender-verified scene fixes" },
    @{ Name = "one-more-scroll-h2-preview-30s.mp4"; Required = $false; Size = 3987339; Sha = "1df4a41e408b8729eca2c9f481a1ed9c38e9d89715adb56bfa5a3a6163603168"; Role = "30-second H2 motion preview" },
    @{ Name = "one-more-scroll-h2-thumbnail.png"; Required = $false; Size = $null; Sha = "dbb11a7096a6a904386a60148b6ea6e457674e10fb1d51dbc7a4826559d90747"; Role = "H2 master thumbnail" },
    @{ Name = "one-more-scroll-h2-contact-sheet-1.jpg"; Required = $false; Size = $null; Sha = "affe02514ddc1c930aff1fa248a438186ae00af05689b329d35d953a7629799e"; Role = "H2 master contact sheet, shots 1–16" },
    @{ Name = "one-more-scroll-h2-contact-sheet-2.jpg"; Required = $false; Size = $null; Sha = "791aba77a97671d98e7a7738f42ca19702d97770e9cf2eb3b2fac2c0dfa652b5"; Role = "H2 master contact sheet, shots 17–31" },
    @{ Name = "one-more-scroll-h2-QA-report.md"; Required = $false; Size = $null; Sha = "ab6408184c668612ccdd914d27c15ab73d042f12f84d9d57784b128a3a07d889"; Role = "H2 render and known-issues report" },
    @{ Name = "h2-selfimprove-studio.plugin"; Required = $false; Size = 188342; Sha = "339b410a0535cd51525df9679e774e72515b483733e70c08be4f379a25b41bf3"; Role = "H2 SelfImprove Studio plugin package" }
)

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI 'gh' is required. Install it and run 'gh auth login' first."
}
gh auth status --hostname github.com
if ($LASTEXITCODE -ne 0) { throw "GitHub CLI is not authenticated." }

$Files = [System.Collections.Generic.List[string]]::new()
$Published = [System.Collections.Generic.List[object]]::new()
foreach ($Item in $Expected) {
    $Path = Join-Path $AssetsDir $Item.Name
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        if ($Item.Required) { throw "Required file is missing: $Path" }
        Write-Host "Skipping optional asset not found: $($Item.Name)"
        continue
    }
    $File = Get-Item -LiteralPath $Path
    if ($Item.Size -ne $null -and $File.Length -ne [long]$Item.Size) {
        throw "Size mismatch for $($Item.Name): $($File.Length) bytes, expected $($Item.Size)."
    }
    $ActualHash = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($ActualHash -ne $Item.Sha) {
        throw "SHA-256 mismatch for $($Item.Name): $ActualHash. Refusing to publish."
    }
    $Files.Add($Path)
    $Published.Add([pscustomobject]@{
        filename = $Item.Name
        role = $Item.Role
        size_bytes = $File.Length
        sha256 = $ActualHash
        release_asset_url = "https://github.com/$Repository/releases/download/$ReleaseTag/$($Item.Name)"
    })
}

if ($Files.Count -lt 2) { throw "At least the original H2 master and source ZIP are required." }

# Never overwrite an existing release/tag silently. Use a fresh version tag for another package.
gh release view $ReleaseTag --repo $Repository *> $null
if ($LASTEXITCODE -eq 0) {
    throw "Release '$ReleaseTag' already exists. Choose a new -ReleaseTag to preserve immutable provenance."
}
$Notes = @"
This release stores the original H2 Canvas/Chromium production master and source assets.
All uploaded files were checked against the known SHA-256 allow-list by tools/video/publish_h2_source_release.ps1.

IMPORTANT:
- The H2 master is distinct from the repository's Remotion render.
- The source-v2 package contains scene fixes that were not confirmed by a full fresh render in the prior session.
- The complete upstream Remotion, Blender and Krita application sources are not part of this release.
"@
gh release create $ReleaseTag --repo $Repository --target main --title "ONE MORE SCROLL — H2 source and reference assets" --notes $Notes
if ($LASTEXITCODE -ne 0) { throw "Failed to create GitHub Release." }

gh release upload $ReleaseTag @Files --repo $Repository
if ($LASTEXITCODE -ne 0) { throw "GitHub Release was created, but one or more asset uploads failed. Inspect the release before retrying." }

$Manifest = [pscustomobject]@{
    project_id = "one-more-scroll"
    status = "uploaded to GitHub Release; verify all URLs before marking complete"
    release_tag = $ReleaseTag
    release_url = "https://github.com/$Repository/releases/tag/$ReleaseTag"
    created_from_repository = $Repository
    published_at = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    assets = @($Published)
    notes = @(
        "H2 Canvas/Chromium master and source archives; not the Remotion build.",
        "The source-v2 ZIP has additional fixes but was not fully rerender-verified.",
        "Keep upstream Remotion/Blender/Krita application source archives separate and follow their official licenses."
    )
}
$ManifestPath = Join-Path $Root "video-library/one-more-scroll/h2-source-release.json"
$Manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ManifestPath -Encoding utf8
git -C $Root add "video-library/one-more-scroll/h2-source-release.json"
if ($LASTEXITCODE -ne 0) { throw "Release is uploaded, but could not stage the release manifest." }

Write-Host ""
Write-Host "Uploaded and SHA-256-verified $($Files.Count) asset(s):"
Write-Host "  https://github.com/$Repository/releases/tag/$ReleaseTag"
Write-Host "Release manifest staged: video-library/one-more-scroll/h2-source-release.json"
Write-Host "Next: review the manifest and commit/push it; do not mark the original H2 source archives present in the portable ZIP until that package workflow completes."
