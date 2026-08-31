# Fetches the ticket universe for the pre-registered selection rule (rule item 1 + recency window).
# Requires: gh CLI authenticated. Run from the repo root. Output: data/ticket_universe_raw.json
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path data | Out-Null

$query = @'
query($cursor: String) {
  search(query: "repo:netbox-community/netbox is:issue label:\"type: bug\" state:closed closed:>=2024-08-01 sort:created-desc", type: ISSUE, first: 25, after: $cursor) {
    issueCount
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on Issue {
        number title closedAt stateReason
        closedByPullRequestsReferences(first: 5, includeClosedPrs: true) {
          totalCount
          nodes { number title merged mergedAt baseRefName mergeCommit { oid }
            files(first: 100) { totalCount nodes { path } }
          }
        }
      }
    }
  }
}
'@

$all = New-Object System.Collections.ArrayList
$cursor = $null
$page = 0
do {
  if ($cursor) { $resp = gh api graphql -f query=$query -f cursor=$cursor } else { $resp = gh api graphql -f query=$query }
  $obj = $resp | ConvertFrom-Json
  $s = $obj.data.search
  foreach ($n in $s.nodes) { [void]$all.Add($n) }
  $cursor = $s.pageInfo.endCursor
  $page++
  Write-Output ("page {0}: {1} collected of {2} reported" -f $page, $all.Count, $s.issueCount)
  Start-Sleep -Milliseconds 500
} while ($s.pageInfo.hasNextPage -and $page -lt 60)

if ($s.issueCount -gt 1000) { Write-Output "WARNING: issueCount exceeds the 1000-node search cap; window splitting required" }
$all | ConvertTo-Json -Depth 10 | Set-Content -Path data\ticket_universe_raw.json -Encoding UTF8
Write-Output ("DONE: {0} issues written" -f $all.Count)
