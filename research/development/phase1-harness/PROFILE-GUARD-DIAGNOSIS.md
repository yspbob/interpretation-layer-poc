# Profile guard diagnosis and bounded repair

16 September 2026. Artificial local checks only. No model calls or new reserved exposure.

## Finding

A Windows directory-notification trace observed `skills/desktop.ini` created and deleted three times, beginning about 6.94 seconds after the first profile directory event. Similar names appeared inside bundled skill directories. The earlier guard rejected every root entry except `.system`, so catching this name during a poll would produce `Unexpected profile skill`.

This supplies a concrete possible explanation for the second qualification stop. It does **not** identify the original offending entry or the process that created the observed entries. The original collector did not save the name; the retained log database contained no log rows. The first notification trace records names, not file types or contents. Do not report the old failure as conclusively diagnosed or retrospectively successful.

Ten short startups showed only permitted paths. The longer stream exposed the transient name. Two initial delayed fixtures hit the simulator's idle timeout; both are retained. The successful long fixture used a recorded 15-second local stream timeout and a 12-second response delay. Live transport settings were not changed.

Three subsequent long probes attempted to inspect transient entry types, but no such entry appeared. Their clean results do not establish the type of the earlier natural entry. The regular-file exception below is supported by deliberate canary tests, not an assumption about that missing observation.

## Change and evidence

Rejected skill listings now preserve the checked directory, all observed names, rejected names and observation time in `failure.json`. This uses the listing that triggered rejection, rather than a later inspection. A test removes an entry after listing and verifies that its name survives in the failure observation.

The guard now permits only a **regular file** named exactly `desktop.ini` directly inside `home/skills` or `home/skills/.system`. A directory, symbolic link, Windows reparse point, unknown type or additional skill still fails. Workspace additions and instruction checks are unchanged. A file that disappears before its type can be checked remains a conservative rejection; this repair does not promise to eliminate every race.

The [official skill documentation](https://learn.chatgpt.com/docs/build-skills) describes skills as directories containing `SKILL.md` and notes that linked skill folders can be followed. That motivates the type distinction; the installed-client tests supply the evidence for this particular exception.

Seven actual-client canary cases passed their declared checks. A regular `desktop.ini` containing artificial skill front matter and an instruction marker was placed in both checked directories for each of the three roles. The marker did not appear in any captured request. A file added during collection also did not change the request. Same-named directories containing `SKILL.md`, and another added profile skill, were refused before dispatch. Four preceding capture checks also passed, including an added skill during a request that stopped collection and retained its name.

All **132 offline harness tests passed**, including the allowance boundary, first-answer retention, identity, stop and denial checks, plus rejection logging, disappearing entries, regular-file limits, simulated link/reparse types and uncertain types. These are local transport and control observations, not model reasoning or complete operating-system containment. No authenticated wire capture is claimed.

## Preservation and next step

Original collections, approvals, scores and freezes remain unchanged. No role prompt, scoring key, acceptance requirement, drafter instruction or live timeout changed. The collector bytes did change, so the closed allocation's configuration and approval cannot authorise another run.

The private archive preserves all 27 artificial cases, including failures, under commitment `4d7a6ca1dfaa982bb4fe826d8ed22a59440b946204211c09b7e3879dd3a8e213` (659 records). An exclusion inventory identifies generated local profiles. Final collector SHA-256: `f2d2c6c12476733f58ad4aa36cc0acd301e6063b9efe8e706df1aece37b2de7d`.

Next review the six exposed positions and specify the next qualification allocation under the repaired execution configuration. Preserve the original outcomes and do not select material based on the five favourable scores. Bind the exact runtime and protocol, then obtain explicit approval before any new reserved request. Both prior allocations remain closed; zero experimental guidance runs have been completed.
