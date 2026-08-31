# Selected ticket set and T0 - selection rule executed 31 Aug 2026, awaiting owner ratification

Walk: prescreen survivors (primary tier, >=5 files), newest first; excluded by screen 5a: issues 22982, 22768, 21542 (tests fail post-fix in harness) and 18555 (harness job error, logs kept); symptom audit 5b excluded none (0 MISMATCH; 4 PARTIAL recorded in data/symptom_audit.md, of which 22531 is in the selected set). First 20 qualifying selected.

T0 = `e98e5e11a733a6d45a7ac78cc25809605239af6d` (parent of the earliest-merged selected fixing PR: issue #20474, PR #21740, merged 2026-04-01T23:19:43Z). The fact graph and corpus are built at T0.

| # | Issue | PR | Closed | Merged | Files | Merge commit |
|---|---|---|---|---|---|---|
| 1 | #23043 | 23055 | 2026-08-27 | 2026-08-27 | 5 | f657bcb78a9862c0e20196e696dcadb77114d71f |
| 2 | #22990 | 23002 | 2026-08-25 | 2026-08-25 | 7 | 1077ff4a3321f350082d12abfc9bcab58bc9e345 |
| 3 | #22985 | 22986 | 2026-08-20 | 2026-08-20 | 7 | e49e6afbbe092f69dbfac0a8bdeebc4182d03795 |
| 4 | #22922 | 22928 | 2026-08-18 | 2026-08-18 | 13 | c2d39b12d8b675c1442204a136b4abc448bbe08f |
| 5 | #22812 | 22867 | 2026-08-11 | 2026-08-11 | 7 | a08d9f13fceeab9fc5bf8f998ddc0997e867eab8 |
| 6 | #22745 | 22777 | 2026-08-11 | 2026-08-11 | 6 | a94878aa08cf425866f56850e5d35996bf292cc3 |
| 7 | #22852 | 22870 | 2026-08-10 | 2026-08-10 | 5 | ae8fa4c0746a8646d86993f22825be03abd3d82f |
| 8 | #22588 | 22684 | 2026-07-22 | 2026-07-22 | 5 | 3e3d36cc2dcc0d4c558d3868ab39b09eca303944 |
| 9 | #22682 | 22693 | 2026-07-18 | 2026-07-18 | 8 | 0eb1fcc09c1df3ccee3f10026a1e0763b819b814 |
| 10 | #22644 | 22645 | 2026-07-14 | 2026-07-14 | 8 | c1d8ff1216758a599786f96f752b46ca1aaf6e15 |
| 11 | #22578 | 22606 | 2026-07-03 | 2026-07-03 | 7 | 6edb5ec8b7da022794b2bf95daf9177250a6c7cf |
| 12 | #22531 | 22542 | 2026-06-25 | 2026-06-25 | 6 | 9c73c7a8aef8687d97f82c87212db9f9ec24fc67 |
| 13 | #22429 | 22424 | 2026-06-11 | 2026-06-11 | 6 | d1919627cefc93ba5104f327df0f2959396d129f |
| 14 | #22273 | 22401 | 2026-06-10 | 2026-06-10 | 5 | b4116f2532b1d1308668f05e7c03e62a3dfe2b11 |
| 15 | #22237 | 22385 | 2026-06-04 | 2026-06-04 | 8 | 86ea67d6400aa1300d00b047090c8b7d54bb2dac |
| 16 | #22324 | 22366 | 2026-06-03 | 2026-06-03 | 11 | 2e50fc3d97e81f6bac394547415853c00a7950f7 |
| 17 | #22301 | 22323 | 2026-05-28 | 2026-05-28 | 5 | 4eb0e727b9bb35e78e91102c0b8a1c2b988dd842 |
| 18 | #22228 | 22244 | 2026-05-21 | 2026-05-21 | 9 | e15b7bd8ac43ed531c1fc1b30d1477250de807d5 |
| 19 | #21498 | 21815 | 2026-04-02 | 2026-04-02 | 5 | b4ee2cf447a351bbacb5b19cf9182fb25a2e83ac |
| 20 | #20474 | 21740 | 2026-04-01 | 2026-04-01 | 5 | c7bbfb24c5f6ad1891d7e261a05a72f97c5e320c |

Spares (qualifying, unselected, newest first - used only under the pre-registered flake-exclusion rule at the Gate 5 dry run): #21763, #21129, #20759, #20670, #20389, #20497, #18900, #19633, #19806.
