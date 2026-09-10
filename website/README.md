# Study website

This directory is the editable source for the GitHub Pages website. It is self-contained within the POC repository; do not copy from an old Sites workspace or sibling repository.

From this directory, install dependencies once with `npm ci --no-audit --no-fund`. Use Node.js 22.13 or newer. Run `npm run dev` for a local preview.

To publish an edit, run these steps in order:

1. From the repository root, `node scripts/sync-plan.mjs` copies the canonical plan and change register into the evidence downloads.
2. From `website/`, run `npx tsc --noEmit` and `npx oxlint app` when application code changed.
3. Run `npm run build:pages`. This exports the current phase plan, progress, roadmap and complete method reference routes and checks the local links and assets for the GitHub Pages subpath.
4. Run `node scripts/update-pages.mjs`. This copies the checked build into `../docs/` while preserving the historical pages.
5. From the repository root, run `node scripts/sync-plan.mjs --check`, review and commit the source and generated changes together, then use the project's normal publish routine.

GitHub Pages serves `docs/` from main. It may take a short time to rebuild after the commit arrives. Verify the affected live route after publication. A successful push alone is not proof that the public page has updated.

The explanation lives in `app/page.tsx` and `app/experiment-details.tsx`; progress lives in `app/progress/progress-view.tsx`. Keep their meaning aligned with the working plan. Plain anchors and `sitePath` support the project subpath and avoid the previous client navigation failure. Keep the two views separate and place optional detail beside the part it explains.

The opening route remains the current phase plan, as requested by the user. `app/phase-line.tsx` supplies the station map in the sticky header. `app/phases/` describes one roadmap phase at a time and responds to `#phase-1`, `#phase-2` and `#phase-3`. Phase 1 remains the actual current phase regardless of which future description a reader selects. Future phase proposals do not appear as progress in the current status view.

The three roadmap stops are now the functional phases of the first trial: reconstruct guidance, test its use, then test interaction. `/` focuses on guidance reconstruction; `/progress/` records its current work. `/trial-method/` preserves the full preparation, coding and interaction specification without making it the Phase 1 workload. Confirmation and possible production studies sit under “What could follow the first trial” on the roadmap.
