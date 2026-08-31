# Builds the fail-then-pass screen matrix (rule item 5a) from the prescreen survivors.
# Primary-tier survivors only, newest first. Output: data/failpass_matrix.json
# Each entry: issue, pr, merge commit, semicolon-joined test file paths from the fixing PR's diff.
$ErrorActionPreference = "Stop"
$raw = Get-Content data\ticket_universe_raw.json -Raw | ConvertFrom-Json
$surv = Get-Content data\prescreen_survivors.json -Raw | ConvertFrom-Json
$byIssue = @{}
foreach ($i in $raw) { $byIssue[$i.number] = $i }

$matrix = New-Object System.Collections.ArrayList
$primary = $surv | Where-Object { $_.floorTier -eq 'primary' } | Sort-Object { [datetime]$_.closedAt } -Descending
foreach ($sv in $primary) {
  $pr = ($byIssue[$sv.issue].closedByPullRequestsReferences.nodes | Where-Object { $_.merged })[0]
  $testPaths = @($pr.files.nodes | ForEach-Object { $_.path } | Where-Object { $_ -match '(^|/)tests/' })
  [void]$matrix.Add([pscustomobject]@{
    issue = $sv.issue
    pr = $sv.pr
    merge = $sv.mergeCommit
    tests = ($testPaths -join ';')
  })
}
ConvertTo-Json @($matrix) -Depth 4 -Compress | Set-Content -Path data\failpass_matrix.json -Encoding UTF8
Write-Output ("Matrix written: {0} primary-tier tickets" -f $matrix.Count)
