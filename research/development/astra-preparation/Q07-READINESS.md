# Third replacement family prepared

**Later update, 15 September:** [The combined batch has now been rehearsed](ASTRA-BATCH-READINESS.md), including the completed Q01 audit. Live execution gates remain.

15 September 2026. Q07 is prepared and audited. It has not been sent to a model for qualification.

All three replacement families are now ready. They provide examples for checking whether the reviewers recognise supported guidance, mistakes and missing evidence. These are authored test materials, not guidance produced by the interpretation layer.

## What is ready

Q07 contains six challenges for each of the three Phase 1 roles, giving 18 distinct items. Its four reference rules concern a different decision from the earlier families. The examples include correct guidance, a valid alternative, a false claim, a missed exception, a partly complete guide and a claim the evidence cannot settle.

The expected answers allow more than one cautious verdict where the evidence is missing. They also require the explanation to be correct. A reviewer cannot pass merely by choosing the expected label.

Role instructions and acceptance requirements remain unchanged. The expected answers and investigator notes stay separate from each role's permitted inputs.

## What the checks established

The installed implementation matched its pinned upstream source. Eighteen authored behaviour checks passed, and four deliberate code faults were detected. No upstream test suite was run. These observations support the scoped reference rules; they do not demonstrate model accuracy.

All 18 items passed source, citation, input separation, identity and format checks. The request builder rejected an altered instruction, changed source and injected answer key. The largest serialized request plus development padding was 31,288 against the existing allowance of 32,768. Actual provider token accounting remains unverified.

Review of the answers found one rule whose wording extended beyond the branch its evidence supported. The rule was narrowed and two boundary examples were added before any model responses. The final source pack also includes the helper needed to establish a called operation's effect. The investigator review is recorded, without independent human certification.

Preparation initially encountered a Windows text encoding error. The next packet version was too large for 11 requests. Both are preserved. The final packets remove repeated metadata while retaining all source passages and observations. No role instruction or expected verdict label changed during these corrections.

## What remains

Q01 still needs its final retention and input audit, with its earlier Fable evaluation disclosed. Then the four families need one combined freeze, the revised runtime instructions and a rehearsal of that exact configuration. Actual model access, account controls and an authorised allocation remain gates before qualification.

The [drafter learning record](DRAFTER-LEARNINGS.md) remains separate. No Q07 case details or answers were added to it, and no drafter prompt changed.

Private preparation commitment: `f4ffe575d3e34b228a1a016636823eb5b1d06c393973e93233406d65c4ba4211`. All 60 committed files matched after copying to private storage. The active version is prepared-v5. Earlier versions preserve the preparation history. Private test material does not transfer to the laptop through public project sync.

**Astra remains unqualified. No new model calls or experimental guidance runs occurred.**
