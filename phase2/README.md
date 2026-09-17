# Phase 2 draft corpus, batch 1 (plan v1.2), 17 September 2026

Status: DRAFT, Gate 3 pending. Nothing here is served or verified.

- Batch rule (fixed before dispatch): every subsystem with >= 5,000 code LOC in the fact graph, nine of seventeen: dcim, extras, ipam, netbox, utilities, circuits, vpn, core, virtualization. The remaining eight follow as batch 2.
- Inputs per subsystem: `slices/<sub>.json` (all fact-graph rows for the subsystem, both edge kinds, with row ids) and `slices/<sub>.digest.md`; a read-only source tree at T0 ea4c205 with no agent-instruction files. Drafters never saw the ticket list or AGENTS.md.
- Brief: `DRAFTER-BRIEF.md` (identical for all nine; sha256 81fafa03...). Checker: `check_citations.py` (sha256 563d5924...), rules fixed and self-tested before drafting.
- Drafting: nine fresh subagents in parallel, 07:35 to 07:45 UTC; 1.99 million subagent tokens in total (range 181k to 274k per subsystem).
- Mechanical evidence check: 781 cited claims, 0 removed, 0 citations dropped (`corpus/<sub>/check_report.json`). The check certifies that every cited row and line exists; it does not certify that the evidence supports the sentence. That is Gate 3 (owner sample: `gate3_sample.html`, 20 claims, seed 20260917) and Phase 3.
- Not in the graph at T0 and therefore absent from the corpus by construction: any behaviour introduced after 2 July 2025.
