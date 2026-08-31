# Applies the pre-registered selection rule's mechanical pre-screens (items 1-4) to the fetched universe.
# Input: data/ticket_universe_raw.json. Outputs: data/prescreen_log.csv, data/prescreen_survivors.json
# Screens 5a (fail-then-pass) and 5b (symptom-test audit) run separately; this script never selects, only screens.
$ErrorActionPreference = "Stop"
$raw = Get-Content data\ticket_universe_raw.json -Raw | ConvertFrom-Json
$windowStart = [datetime]'2024-09-01'

$rows = New-Object System.Collections.ArrayList
$survivors = New-Object System.Collections.ArrayList

foreach ($i in ($raw | Sort-Object { [datetime]$_.closedAt } -Descending)) {
  $fate = ''; $clause = ''; $prNum = $null
  $mergedPrs = @($i.closedByPullRequestsReferences.nodes | Where-Object { $_.merged })
  if ($i.stateReason -ne 'COMPLETED') { $fate = 'EXCLUDED'; $clause = '4d not closed-as-completed' }
  elseif ($mergedPrs.Count -ne 1) { $fate = 'EXCLUDED'; $clause = "1 no single merged fixing PR (count=$($mergedPrs.Count))" }
  else {
    $pr = $mergedPrs[0]; $prNum = $pr.number
    $paths = @($pr.files.nodes | ForEach-Object { $_.path })
    $testFiles = @($paths | Where-Object { $_ -match '(^|/)tests/' })
    $srcPy = @($paths | Where-Object { $_ -match '\.py$' -and $_ -notmatch '(^|/)tests/' -and $_ -notmatch '/migrations/' })
    if ([datetime]$pr.mergedAt -lt $windowStart) { $fate = 'EXCLUDED'; $clause = '4e merged before 1 Sep 2024' }
    elseif ($pr.files.totalCount -gt 20) { $fate = 'EXCLUDED'; $clause = "4a more than 20 files ($($pr.files.totalCount))" }
    elseif ($pr.title -match '^\s*(Revert|Release v)') { $fate = 'EXCLUDED'; $clause = '4b revert or release merge' }
    elseif ($testFiles.Count -eq 0) { $fate = 'EXCLUDED'; $clause = '2a no test file in diff' }
    elseif ($srcPy.Count -eq 0) { $fate = 'EXCLUDED'; $clause = '2b/4c no non-test non-migration python source in diff' }
    else {
      $fate = 'SURVIVOR'
      [void]$survivors.Add([pscustomobject]@{
        issue = $i.number; issueTitle = $i.title; closedAt = $i.closedAt
        pr = $pr.number; prTitle = $pr.title; mergedAt = $pr.mergedAt
        mergeCommit = $pr.mergeCommit.oid; baseRef = $pr.baseRefName
        fileCount = $pr.files.totalCount; testFiles = $testFiles.Count; srcPyFiles = $srcPy.Count
      })
    }
  }
  [void]$rows.Add([pscustomobject]@{ issue = $i.number; closedAt = $i.closedAt; pr = $prNum; fate = $fate; clause = $clause; title = $i.title })
}

$rows | Export-Csv -Path data\prescreen_log.csv -NoTypeInformation -Encoding UTF8
$survivors | ConvertTo-Json -Depth 5 | Set-Content -Path data\prescreen_survivors.json -Encoding UTF8
Write-Output ("Universe: {0}. Survivors of mechanical pre-screens: {1}." -f $rows.Count, $survivors.Count)
$rows | Group-Object clause | Sort-Object Count -Descending | ForEach-Object { Write-Output ("{0,5}  {1}" -f $_.Count, ($_.Name -replace '^$','(survivor)')) }
