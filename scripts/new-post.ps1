param(
    [Parameter(Mandatory = $true)]
    [string]$Title,

    [string]$Slug,

    [string]$Date = (Get-Date -Format "yyyy-MM-dd"),

    [string]$Description = "One-sentence summary.",

    [ValidateSet("english", "spanish")]
    [string]$Language = "english"
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
$templatePath = Join-Path $repoRoot "_templates\blog-post.qmd"
if (-not (Test-Path -LiteralPath $templatePath)) {
    throw "Missing template file: $templatePath"
}

$year = $parsedDate.ToString("yyyy")
$month = $parsedDate.ToString("MM")
$postDir = Join-Path $repoRoot ("blog\{0}\{1}\{2}" -f $year, $month, $Slug)
$postFile = Join-Path $postDir "index.qmd"

if (Test-Path -LiteralPath $postFile) {
    throw "Post already exists at $postFile"
}

New-Item -ItemType Directory -Path $postDir -Force | Out-Null

$content = Get-Content -LiteralPath $templatePath -Raw
$replacements = @{
    "{{TITLE}}" = $Title
    "{{DATE}}" = $parsedDate.ToString("yyyy-MM-dd")
    "{{DESCRIPTION}}" = $Description
    "{{LANGUAGE_CATEGORY}}" = $Language
}

foreach ($token in $replacements.Keys) {
    $content = $content.Replace($token, $replacements[$token])
}

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($postFile, $content, $utf8NoBom)

Write-Output ("Created blog post: {0}" -f $postFile)
