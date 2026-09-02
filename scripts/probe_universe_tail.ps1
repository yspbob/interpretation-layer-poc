# Plan v1.2 item F7: probe the universe tail truncated by GitHub's 1,000-result search cap.
# Splits the nominal window into date slices so no slice exceeds 1,000, fetches each with the
# same GraphQL query (closed:RANGE substituted), and reports issues NOT present in
# data/ticket_universe_raw.json. Output: data/universe_tail_probe_raw.json and a summary the owner
# copies into data/universe_tail_probe.md. Requires gh CLI authenticated. Run from the repo root.
$ErrorActionPreference = "Stop"
$raw = Get-Content data\ticket_universe_raw.json -Raw | ConvertFrom-Json
$known = @{}; foreach ($i in $raw) { $known[$i.number] = $true }
$q = Get-Content scripts\ticket_universe_query.graphql -Raw
$slices = @("2024-08-01..2024-12-31", "2025-01-01..2025-06-30", "2025-07-01..2025-12-31", "2026-01-01..2026-12-31")
$found = New-Object System.Collections.ArrayList
foreach ($s in $slices) {
  $qs = $q -replace 'closed:>=2024-08-01', "closed:$s"
  Set-Content -Path scripts\_probe_query.graphql -Value $qs -Encoding UTF8
  $cursor = $null; $page = 0
  do {
    if ($cursor) { $resp = gh api graphql -F "query=@scripts/_probe_query.graphql" -F "cursor=$cursor" }
    else { $resp = gh api graphql -F "query=@scripts/_probe_query.graphql" }
    $obj = ($resp | Out-String) | ConvertFrom-Json
    $r = $obj.data.search
    if (-not $r) { Write-Output "ERROR on slice $s page $($page+1)"; break }
    foreach ($n in $r.nodes) { if (-not $known.ContainsKey($n.number)) { [void]$found.Add($n) } }
    $cursor = $r.pageInfo.endCursor; $page++
    Write-Output ("slice {0} page {1}: issueCount={2} new-so-far={3}" -f $s, $page, $r.issueCount, $found.Count)
    if ($r.issueCount -gt 1000) { Write-Output "WARNING: slice $s exceeds the cap; split it further" }
    Start-Sleep -Milliseconds 500
  } while ($r.pageInfo.hasNextPage -and $page -lt 60)
}
Remove-Item scripts\_probe_query.graphql -ErrorAction SilentlyContinue
$found | ConvertTo-Json -Depth 10 | Set-Content -Path data\universe_tail_probe_raw.json -Encoding UTF8
Write-Output ("DONE: {0} issues outside the committed universe written to data/universe_tail_probe_raw.json" -f $found.Count)
# Apply the prescreen clauses to the new issues only (same logic as prescreen.ps1, primary tier >=5 files):
$windowStart = [datetime]'2024-09-01'; $n = 0
foreach ($i in $found) {
  $mergedPrs = @($i.closedByPullRequestsReferences.nodes | Where-Object { $_.merged })
  if ($i.stateReason -ne 'COMPLETED' -or $mergedPrs.Count -ne 1) { continue }
  $pr = $mergedPrs[0]; $paths = @($pr.files.nodes | ForEach-Object { $_.path })
  $testFiles = @($paths | Where-Object { $_ -match '(^|/)tests/' })
  $srcPy = @($paths | Where-Object { $_ -match '\.py$' -and $_ -notmatch '(^|/)tests/' -and $_ -notmatch '/migrations/' })
  if ([datetime]$pr.mergedAt -lt $windowStart -or $pr.files.totalCount -gt 20 -or $pr.title -match '^\s*(Revert|Release v)') { continue }
  if ($testFiles.Count -eq 0 -or $srcPy.Count -eq 0 -or $pr.files.totalCount -lt 5) { continue }
  $n++; Write-Output ("WOULD-QUALIFY (prescreen, primary tier): issue #{0} PR {1} merged {2} files {3}" -f $i.number, $pr.number, $pr.mergedAt, $pr.files.totalCount)
}
Write-Output ("Prescreen-qualifying issues in the truncated tail: {0} (disclosed, not added; see rule v1.3 item 1)" -f $n)
