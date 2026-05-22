param(
    [Parameter(Mandatory = $true)]
    [string]$Title,

    [string]$Slug,

    [string]$Date = (Get-Date -Format "yyyy-MM-dd"),

    [string]$Doi = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Remove-Diacritics {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Value
    )

    $normalized = $Value.Normalize([Text.NormalizationForm]::FormD)
    $builder = New-Object Text.StringBuilder
    foreach ($char in $normalized.ToCharArray()) {
        if ([Globalization.CharUnicodeInfo]::GetUnicodeCategory($char) -ne [Globalization.UnicodeCategory]::NonSpacingMark) {
            [void]$builder.Append($char)
        }
    }

    return $builder.ToString().Normalize([Text.NormalizationForm]::FormC)
}

function New-Slug {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Value
    )

    $ascii = Remove-Diacritics -Value $Value
    $clean = [regex]::Replace($ascii.ToLowerInvariant(), "[^a-z0-9]+", "-").Trim("-")
    if ([string]::IsNullOrWhiteSpace($clean)) {
        throw "Could not create a slug from the title. Pass -Slug explicitly."
    }

    return $clean
}

try {
    $parsedDate = [datetime]::ParseExact($Date, "yyyy-MM-dd", [Globalization.CultureInfo]::InvariantCulture)
}
catch {
    throw "Date must use yyyy-MM-dd format (example: 2026-02-11)."
}

if (-not $Slug) {
    $Slug = New-Slug -Value $Title
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$templatePath = Join-Path $repoRoot "_templates\research-item.qmd"
if (-not (Test-Path -LiteralPath $templatePath)) {
    throw "Missing template file: $templatePath"
}

$researchDir = Join-Path $repoRoot ("research\articles\{0}" -f $Slug)
$researchFile = Join-Path $researchDir "index.qmd"

if (Test-Path -LiteralPath $researchFile) {
    throw "Research entry already exists at $researchFile"
}

New-Item -ItemType Directory -Path $researchDir -Force | Out-Null

$content = Get-Content -LiteralPath $templatePath -Raw
$replacements = @{
    "{{TITLE}}" = $Title
    "{{DATE}}" = $parsedDate.ToString("yyyy-MM-dd")
    "{{YEAR}}" = $parsedDate.ToString("yyyy")
    "{{DOI}}" = $Doi
}

foreach ($token in $replacements.Keys) {
    $content = $content.Replace($token, $replacements[$token])
}

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($researchFile, $content, $utf8NoBom)

Write-Output ("Created research entry: {0}" -f $researchFile)
