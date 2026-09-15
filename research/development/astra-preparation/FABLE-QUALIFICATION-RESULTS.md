# Fable guidance assessor qualification result

15 September 2026. Configuration: Fable 5.1, High effort, direct delivery through interactive Claude Code using included Max allowance.

**The assessor did not pass qualification.** All 48 answers chose the expected verdicts, but only 35 also gave correct explanations. The frozen criteria require both. This result concerns the supplementary guidance assessor. It does not measure the interpretation layer's benefit, and no experimental guidance run has taken place.

## What was checked

The batch contained six challenges in each of four decision families. Each challenge ran twice in a separate session. Every original response was retained. None was retried or corrected.

Before scoring, we checked the saved inputs, transcripts, response identities and collection records against their committed hashes. All 48 responses passed those checks. Codex then read every answer against the frozen expected decisions and source evidence. A deterministic check verified answer structure, verdicts, the predefined serious error conditions and the final counts. This was an investigator review supported by source evidence, without independent human certification.

## The four qualification requirements

All four requirements had to pass. The [frozen scoring definitions](QUALIFICATION.md) were applied without changing the expected answers or error severity.

| Requirement | Result | Outcome |
|---|---|---|
| No errors in the predefined serious categories | 0 of 48 responses | Passed |
| At least 44 fully correct responses, including 10 in every family | 35 of 48; family counts below | Failed |
| At least 22 repeated pairs with acceptable decisions and correct reasons in both answers | 16 of 24 | Failed |
| At least 7 baseline versus valid alternative comparisons with matching decisions and no serious rejection | 8 of 8 | Passed |

The verdict labels matched in all 24 repeated pairs. That consistency concealed repeated explanation errors. The last requirement concerns decision agreement; it does not add the explicit reason requirement used by the preceding one. As a supplementary measure, both complete answers passed in 6 of the 8 baseline comparisons.

| Family | Fully correct responses |
|---|---|
| Q01 | 12 of 12 |
| Q02 | 11 of 12 |
| Q03 | 10 of 12 |
| Q04 | 2 of 12 |

| Challenge | Fully correct responses |
|---|---|
| Supported guidance | 7 of 8 |
| Equally valid alternative | 7 of 8 |
| Unsupported claim | 6 of 8 |
| Missed exception | 6 of 8 |
| Omitted information | 6 of 8 |
| Evidence that cannot settle a claim | 3 of 8 |

## What went wrong

Three responses correctly said that a claim lacked evidence, then incorrectly described it as contradicting another claim. The claims concerned different conditions or different stages of processing. Both could have been true. Missing evidence justified withholding approval; it did not establish a contradiction.

Ten responses in the fourth family overstated what the supplied code did or misread the saved test observations. Inspection of the pinned implementation and a local behaviour check confirmed a relevant side effect that several explanations denied. Four responses also gave incorrect interpretations of the observations. These categories overlap within that family.

The input material had weaknesses too. Some observations were supplied as arrays without named fields, and the supplied wrapper code did not show the implementation it called. The expected central recommendation remained valid, but those details were absent from the packet. This batch cannot tell us how much clearer inputs would improve the result.

Some of the broad statements could be read more generously as describing only explicit calls in the wrapper. We therefore also calculated the outcome if all six failures depending solely on that wording were accepted. The score would rise to 41 of 48, with 8 of 12 in the fourth family and 19 of 24 correct repeated pairs. Qualification would still fail. This alternative calculation does not replace the recorded score.

The mistakes in explanations did not trigger the item specific serious conditions frozen before collection. We have retained that severity classification rather than changing it after seeing the answers.

## What happens next

Keep this result and the original answers. Prepare a small development revision that makes observations readable and distinguishes missing evidence from evidence of a contradiction. Do not repeat these answers until they pass. Any family used to develop a repair becomes development material; a revised assessor must qualify on fresh applicable families.

Fable remains an unqualified supplementary reviewer. Its evidence based objections may still be investigated, but its scores cannot yet be relied on for the trial. Astra's controlled qualification remains outstanding. No further model call or paid spending was used for this scoring step.

The four related families and their repeated attempts do not establish a population accuracy rate. In particular, zero errors in the predefined serious categories does not prove that serious errors are absent elsewhere.

## Audit record

The private audit retains every response decision, the source based review, exact failure passages, the diagnostic, tally code and a manifest of their hashes. Four synthetic checks passed, covering incorrect reasons, allowed alternatives, duplicate decisions, serious error conditions and threshold boundaries. All 48 committed bank files and 492 collection files still matched their hashes. Sealed inputs, answers and keys remain outside this public repository.

| Commitment | SHA256 |
|---|---|
| Original bank freeze | `bc256b1d390f2f595c0212d157892572fd64226701200236ffcf28add0ef8ae9` |
| Completed collection before scoring | `7a1bd142f53736f0cfa865c2ec0993f0af370c2251131c9b5ca1123b0ae6f123` |
| Completed scoring record | `6e3afe66f58a0b13599735d1b986396e5ae3810078dd53e7b565941ab24f55c4` |

Website wording and progress changes remain banked for the next requested release. This report and the shared project state record the current result.
