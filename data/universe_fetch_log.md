# Universe fetch log (reconstructed, 3 Sep 2026)

The fetch on 31 Aug 2026 (`scripts/fetch_ticket_universe.ps1`) printed its page log to the console; that console output was not captured to a file. What the committed artifact shows:

- `data/ticket_universe_raw.json` holds exactly 1,000 issues, the GitHub search result cap. The script's own guard (`if issueCount -gt 1000 ... WARNING`) would have fired if `issueCount` exceeded 1,000; whether it did is not recorded.
- Search query: `repo:netbox-community/netbox is:issue label:"type: bug" state:closed closed:>=2024-08-01 sort:created-desc`, 25 per page, paginated to 40 pages.
- Closed-date range in the file: 2024-10-18 to 2026-08-31. Monthly counts fall off at the old end (Oct 2024: 8, Nov 2024: 19, Dec 2024: 25), consistent with truncation of the oldest-created issues.
- Universe as executed is therefore: the 1,000 most recently created closed `type: bug` issues matching the query, as of 31 Aug 2026. The selection rule text (v1.3) states this.

Future fetches capture the console log to `data/universe_fetch_<date>.log`.
