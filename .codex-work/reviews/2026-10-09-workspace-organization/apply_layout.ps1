param([switch]$Apply)
$ErrorActionPreference = 'Stop'
$workRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
$workspaceRoot = [IO.Path]::GetFullPath((Join-Path $workRoot '..'))
$plan = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'migration.json') -Raw | ConvertFrom-Json
$moves = foreach ($entry in $plan.mapping.PSObject.Properties) {
    $source = [IO.Path]::GetFullPath((Join-Path $workRoot $entry.Name))
    $destination = [IO.Path]::GetFullPath((Join-Path $workRoot $entry.Value))
    foreach ($target in @($source, $destination)) {
        if (-not $target.StartsWith($workRoot + '\', [StringComparison]::OrdinalIgnoreCase) -or
            -not $target.StartsWith($workspaceRoot + '\', [StringComparison]::OrdinalIgnoreCase)) {
            throw "Move target escapes workspace: $target"
        }
    }
    if (-not (Test-Path -LiteralPath $source)) { throw "Missing source: $source" }
    if (Test-Path -LiteralPath $destination) { throw "Destination already exists: $destination" }
    [pscustomobject]@{Source=$source; Destination=$destination}
}
if (-not $Apply) {
    $moves | Select-Object Source,Destination
    return
}
foreach ($move in $moves) {
    $parent = Split-Path $move.Destination -Parent
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    Move-Item -LiteralPath $move.Source -Destination $move.Destination
}
Write-Output "Moved $($moves.Count) entries within $workRoot."
