# Selected ticket set and T0 - rule v1.2, selection re-executed 31 Aug 2026, awaiting owner ratification

Walk (v1.2): prescreen survivors (primary tier, >=5 files); excluded by screen 5a: 22982, 22768, 21542 (tests fail post-fix in harness) and 18555 (harness job error, logs kept); excluded by 5b under amendment v1.2: 22531, 20759, 20497, 19633 (PARTIAL grades - see data/symptom_audit.md). Sample = all 25 fully-matching qualifiers. No spares remain: any dry-run flake exclusion shrinks N and is reported as actual N.

T0 = `ea4c205a37baa3e58e6e481158c15c6154cceeff` (parent of the earliest-merged selected fixing PR: issue #19806, PR #19807, merged 2025-07-02T19:02:49Z). The fact graph and corpus are built at T0 and never see anything later.

| # | Issue | PR | Closed | Merged | Files | Audit | Merge commit |
|---|---|---|---|---|---|---|---|
| 1 | #23043 | 23055 | 2026-08-27 | 2026-08-27 | 5 | MATCH | f657bcb78a9862c0e20196e696dcadb77114d71f |
| 2 | #22990 | 23002 | 2026-08-25 | 2026-08-25 | 7 | MATCH | 1077ff4a3321f350082d12abfc9bcab58bc9e345 |
| 3 | #22985 | 22986 | 2026-08-20 | 2026-08-20 | 7 | MATCH | e49e6afbbe092f69dbfac0a8bdeebc4182d03795 |
| 4 | #22922 | 22928 | 2026-08-18 | 2026-08-18 | 13 | MATCH | c2d39b12d8b675c1442204a136b4abc448bbe08f |
| 5 | #22812 | 22867 | 2026-08-11 | 2026-08-11 | 7 | MATCH | a08d9f13fceeab9fc5bf8f998ddc0997e867eab8 |
| 6 | #22745 | 22777 | 2026-08-11 | 2026-08-11 | 6 | MATCH | a94878aa08cf425866f56850e5d35996bf292cc3 |
| 7 | #22852 | 22870 | 2026-08-10 | 2026-08-10 | 5 | MATCH | ae8fa4c0746a8646d86993f22825be03abd3d82f |
| 8 | #22588 | 22684 | 2026-07-22 | 2026-07-22 | 5 | MATCH | 3e3d36cc2dcc0d4c558d3868ab39b09eca303944 |
| 9 | #22682 | 22693 | 2026-07-18 | 2026-07-18 | 8 | MATCH | 0eb1fcc09c1df3ccee3f10026a1e0763b819b814 |
| 10 | #22644 | 22645 | 2026-07-14 | 2026-07-14 | 8 | MATCH | c1d8ff1216758a599786f96f752b46ca1aaf6e15 |
| 11 | #22578 | 22606 | 2026-07-03 | 2026-07-03 | 7 | MATCH | 6edb5ec8b7da022794b2bf95daf9177250a6c7cf |
| 12 | #22429 | 22424 | 2026-06-11 | 2026-06-11 | 6 | MATCH | d1919627cefc93ba5104f327df0f2959396d129f |
| 13 | #22273 | 22401 | 2026-06-10 | 2026-06-10 | 5 | MATCH | b4116f2532b1d1308668f05e7c03e62a3dfe2b11 |
| 14 | #22237 | 22385 | 2026-06-04 | 2026-06-04 | 8 | MATCH | 86ea67d6400aa1300d00b047090c8b7d54bb2dac |
| 15 | #22324 | 22366 | 2026-06-03 | 2026-06-03 | 11 | MATCH | 2e50fc3d97e81f6bac394547415853c00a7950f7 |
| 16 | #22301 | 22323 | 2026-05-28 | 2026-05-28 | 5 | MATCH | 4eb0e727b9bb35e78e91102c0b8a1c2b988dd842 |
| 17 | #22228 | 22244 | 2026-05-21 | 2026-05-21 | 9 | MATCH | e15b7bd8ac43ed531c1fc1b30d1477250de807d5 |
| 18 | #21498 | 21815 | 2026-04-02 | 2026-04-02 | 5 | MATCH | b4ee2cf447a351bbacb5b19cf9182fb25a2e83ac |
| 19 | #20474 | 21740 | 2026-04-01 | 2026-04-01 | 5 | MATCH | c7bbfb24c5f6ad1891d7e261a05a72f97c5e320c |
| 20 | #21763 | 21778 | 2026-03-30 | 2026-03-30 | 6 | MATCH | e54ed878632309cb988bb44bb761f5c671d9af08 |
| 21 | #21129 | 21309 | 2026-01-29 | 2026-01-29 | 8 | MATCH | c44e8606f7b240fe0b6955208056ae21f001d346 |
| 22 | #20670 | 20717 | 2025-11-06 | 2025-11-06 | 17 | MATCH | 730d73042d5ee34b31f16e2c978cb65718eb794e |
| 23 | #20389 | 20672 | 2025-10-27 | 2025-10-27 | 12 | MATCH | aa4571b61f7482ae7a521738c6e0030d75336a69 |
| 24 | #18900 | 19943 | 2025-07-29 | 2025-07-29 | 8 | MATCH | c736ce3179a8bb7bbcbf29324a08a62efa8747b6 |
| 25 | #19806 | 19807 | 2025-07-02 | 2025-07-02 | 6 | MATCH | 3b8841ee3b0210b286dd62ca0b4810d0d6b72365 |
