# Strip list, applied at every checkout, every arm (plan v1.2, F1)

Historical pre-fix checkouts carry maintainer-written agent instructions: upstream added `CLAUDE.md` on 3 Mar 2026 (#21559, commit `b11cc31f9`) and `AGENTS.md` plus `.claude/skills/` on 6 May 2026 (CAP-100, #22120, commit `b3bc4f8ef`). Of the 25 selected tickets, 20 pre-fix checkouts contain `CLAUDE.md` and 17 of those also contain `AGENTS.md` and `.claude/` (verified 3 Sep 2026 by `git ls-tree` at each first-parent commit; the five clean checkouts are #21129, #20670, #20389, #18900, #19806). Nothing runs on an unstripped tree.

## Paths removed by the harness before the agent starts

Applied with `git rm -rq --ignore-unmatch` (or an equivalent that leaves no file behind) on the checked-out tree, then the working tree is verified clean of every pattern:

```
CLAUDE.md
AGENTS.md
GEMINI.md
.claude/
.cursor/
.cursorrules
.cursorignore
.windsurfrules
.github/copilot-instructions.md
.github/workflows/claude*.yml
.github/workflows/claude-code-review.yml
```

Pattern matching is case-insensitive and applies at the repository root only, except `.github/workflows/claude*.yml`, which is matched inside that directory. Any additional file matching `(?i)^(claude|agents|gemini|copilot)[-_]?.*\.md$` at the root is also removed and its name is logged: the list above is what upstream history contains as of 3 Sep 2026; the pattern guards against later additions in the feature stratum.

Arms B and D then receive `preregistration/served/AGENTS.md` (the trimmed copy) written to the repository root as `AGENTS.md` after the strip; arms A and C receive nothing.

## Per-run log

Every run's JSON log carries a `strip` object: the checkout commit, the list of paths removed (with blob hashes), the list of paths added afterwards (arms B and D: the served `AGENTS.md` with its sha256), and the result of a post-strip scan for the patterns above (must be empty). A run whose scan is non-empty is void and is re-run.

## Not stripped

Upstream's `docs/development/` (human contributor guide), `CONTRIBUTING.md`, `pyproject.toml` lint configuration and `.pre-commit-config.yaml` stay: they are part of the codebase every arm sees and contain no agent-directed instruction. This is a deliberate choice, recorded here so it cannot be revisited after results.
