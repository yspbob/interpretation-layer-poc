param(
    [ValidateSet('starting', 'feature', 'later-qa', 'all')]
    [string]$Revision = 'all'
)
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$composeFile = Join-Path $PSScriptRoot 'compose.yaml'
$pins = [ordered]@{
    'starting' = 'd13c98b9ea8c55dafdcdecbf3058a731814a7ead'
    'feature' = '6068f417876e79b6d588bd8b05a7a4e515378b51'
    'later-qa' = '3793160eba4d54070552eacfc1502027a7e042c1'
}
$runId = (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0,8)
$oldRevision = $env:NETBOX_REVISION
$oldResults = $env:NB_BULK_RESULTS
function Invoke-DockerChecked {
    param([string[]]$DockerArgs)
    & docker @DockerArgs
    if ($LASTEXITCODE -ne 0) { throw "Docker failed with exit code $LASTEXITCODE" }
}
try {
    Invoke-DockerChecked -DockerArgs @('info', '--format', '{{.ServerVersion}}')
    foreach ($label in $pins.Keys) {
        if ($Revision -ne 'all' -and $label -ne $Revision) { continue }
        $env:NETBOX_REVISION = $pins[$label]
        $env:NB_BULK_RESULTS = Join-Path $repoRoot "local-runs/netbox-runtime/$runId/$label"
        New-Item -ItemType Directory -Path $env:NB_BULK_RESULTS -Force | Out-Null
        $projectName = "nb-bulk-$runId-$label"
        $baseArgs = @('compose', '-f', $composeFile, '-p', $projectName)
        Write-Output "Checking $label; results: $env:NB_BULK_RESULTS"
        try {
            Invoke-DockerChecked -DockerArgs ($baseArgs + @('build', 'probe'))
            Invoke-DockerChecked -DockerArgs ($baseArgs + @('up', '--abort-on-container-exit', '--exit-code-from', 'probe'))
            & docker image inspect "nb-bulk-reproduction:$($pins[$label])" postgres:17 redis:7 |
                Set-Content -LiteralPath (Join-Path $env:NB_BULK_RESULTS 'images.json') -Encoding UTF8
            if ($LASTEXITCODE -ne 0) { throw 'Unable to record runtime images' }
        }
        finally {
            & docker compose -f $composeFile -p $projectName logs --no-color |
                Set-Content -LiteralPath (Join-Path $env:NB_BULK_RESULTS 'container-log.txt') -Encoding UTF8
            # This unique project owns only this attempt's disposable containers and volumes.
            & docker compose -f $composeFile -p $projectName down --volumes
            if ($LASTEXITCODE -ne 0) { Write-Warning "Cleanup needs attention for $projectName" }
        }
    }
}
finally {
    $env:NETBOX_REVISION = $oldRevision
    $env:NB_BULK_RESULTS = $oldResults
}
