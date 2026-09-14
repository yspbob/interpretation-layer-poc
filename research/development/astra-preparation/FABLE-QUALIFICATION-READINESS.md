# Fable qualification inputs are frozen

14 September 2026. The existing 24 guidance assessment challenges are ready for 48 scheduled responses through Claude Desktop at High effort. No qualification call has run. No reviewer has passed and no experimental guide has been assessed.

## What is fixed

The private package preserves the original role prompt, candidate guides, source excerpts, permitted references and response schema. It uses the existing Astra schedule filtered to the guidance assessor role, without rearranging it. Each challenge appears twice with identical attachment bytes, in separate scheduled chats.

The [operating and scoring procedure](FABLE-QUALIFICATION.md) fixes the delivery wrapper, settings, capture requirements, failure handling and criteria for proceeding. It adopts the existing numerical gates without changing the bank's expected answers or severity. Those keys remain in the original private bank and are linked through its freeze hash. The desktop package builder does not read them.

The freeze covers 61 files: the 48 scheduled attachments, common wrapper, private schedule, protocol and implementation snapshots, and preparation summary. A later audit is stored separately so it cannot rewrite that freeze. Private input paths and expected answers are not published.

Desktop freeze SHA256:

`d1d52bddd42290ff8459a0c827611f066cab57cda1dd6ff3acb8635c56c30fa4`

Original bank freeze SHA256:

`bc256b1d390f2f595c0212d157892572fd64226701200236ffcf28add0ef8ae9`

## What was checked

All 48 scheduled attachments were parsed back and compared with the original permitted inputs. The instructions, schema, source text, candidate identity and references matched. There are 24 distinct packet hashes, each repeated exactly twice. The schedule retains all four families and both repetitions. All 48 files covered by the original bank freeze remain unchanged.

The largest attachment is 23,555 bytes. Its common wrapper adds 353 bytes, for 23,908 bytes in total, below the 32,768 byte public reading diagnostic. Each item asks for at most five claim decisions and four reference coverage decisions. These checks establish content preservation and byte fit, not provider token accounting, guaranteed absence of truncation or complete capture of a future answer.

Seven software checks passed. They cover complete packaging without reading hidden keys, schedule preservation, changed files and identities, forbidden extra input fields, oversized packets, refusal to overwrite a package, and refusal to place private output in public Git. They also exercise the existing answer validator against missing, duplicated and mismatched decisions. The first invocation could not access Windows temporary folders; the unchanged checks passed with the required filesystem access. No network call was allowed in those tests.

The private audit also passed a synthetic answer for every scheduled packet through the existing structure and identity validator. Those are fabricated transport examples, not correct model answers or semantic qualification. Full desktop answer capture still needs checking on each actual attempt. Raw output must remain available when parsing fails.

The [machine readable audit](fable-qualification-readiness.json) records the totals and commitments. These are investigator preparation checks, not independent certification that every reference is correct.

## What happens next

Reapply the recorded desktop restrictions, verify the app version, model, High effort and included allowance, then start at position one of the frozen schedule. The temporary feature settings were restored after the earlier diagnostic. Preserve the first response and stop on any access deviation or displayed model change. Normal breaks resume at the next never submitted position using the same freeze.

Use only included Max allowance. No API calls or paid credits are authorised. Keep qualification results separate from the four earlier Fable development calls. Score the completed or formally stopped schedule against the frozen criteria before relying on this assessor. Astra's controlled connection and spending gates remain separate work.

The private package currently exists only on the preparation PC. GitHub makes the public procedure available on both machines; it does not transfer sealed inputs or raw captures.
