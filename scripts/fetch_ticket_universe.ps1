# Fetches the ticket universe for the pre-registered selection rule (rule item 1 + recency window).
# Requires: gh CLI authenticated. Run from the repo root. Output: data/ticket_universe_raw.json
# The GraphQL query lives in scripts/ticket_universe_query.graphql (passed via @file: inline
# multiline args are mangled on Windows command lines).
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path data | Out-Null

$all = New-Object System.Collections.ArrayList
$cursor = $null
$page = 0
do {
  if ($cursor) {
    $resp = gh api graphql -F "query=@scripts/ticket_universe_query.graphql" -F "cursor=$cursor"
  } else {
    $resp = gh api graphql -F "query=@scripts/ticket_universe_query.graphql"
  }
  $obj = ($resp | Out-String) | ConvertFrom-Json
  $s = $obj.data.search
  if (-not $s) { Write-Output "ERROR: no search payload on page $($page+1); raw response follows"; Write-Output ($resp | Out-String); break }
  foreach ($n in $s.nodes) { [void]$all.Add($n) }
  $cursor = $s.pageInfo.endCursor
  $page++
  Write-Output ("page {0}: {1} collected of {2} reported" -f $page, $all.Count, $s.issueCount)
  Start-Sleep -Milliseconds 500
} while ($s.pageInfo.hasNextPage -and $page -lt 60)

if ($s -and $s.issueCount -gt 1000) { Write-Output "WARNING: issueCount exceeds the 1000-node search cap; window splitting required" }
$all | ConvertTo-Json -Depth 10 | Set-Content -Path data\ticket_universe_raw.json -Encoding UTF8
Write-Output ("DONE: {0} issues written" -f $all.Count)
