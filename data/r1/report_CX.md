# R1 enrichment report — CX

- Agent: codex/gpt-6; run date: 2026-10-31; seed: `/home/nguyenletuan/Desktop/IBM_AI_builder_challenge/data/r1/seeds_CX.csv`.
- Rows: 29; HTTP requests including robots.txt: 119; initial automated pass runtime: 71.5 s. Total time including DOI follow-up and semantic review was not recorded.
- **R1 source found within 2 hops:** 21/29 (72.4%).
- Has link: 29/29 (100.0%).
- Among linked posts, hop-1 blocked/broken/paywalled: 7/29 (24.1%).
- Observed hyperlink or DOI to primary: 7/29 (24.1%).
- Primary open or abstract-only: 5/29 (17.2%).
- Human impression (not a label): {'blank': 29}; n=29.
- Model impression (not a label): {'unsure': 28, 'distorted': 1}; n=29.
- Human seed time: not recorded; median agent seconds: 1.81 s; n=29.
- Image/video-only exclusions: 0 among 78 listing positions; see `seeds_CX_skips.md`.

## Rows needing human attention

CX-002, CX-003, CX-006, CX-007, CX-008, CX-009, CX-013, CX-014, CX-015, CX-018, CX-020, CX-021, CX-026, CX-027, CX-028

## Audit sample

CX-010, CX-014, CX-017, CX-018, CX-019, CX-022

## Limitations

- The sample used a signed-in Reddit account with explicit human permission, not the planned logged-out condition.
- Passages were mechanically checked against cached text and semantically reviewed by the agent. The R1 metric is provisional until the human audit.
- Per-row `agent_seconds` measures automated fetching and extraction; it excludes the later semantic review time.
- Bot-check signals appeared on CX-015 and CX-020. The initial script marked them blocked but continued; this missed the Phase 0 stop rule. No check was solved or retried. Treat T4 as partial and review the rows before reuse.
- No Crossref title search was used; primary sources without observed links or DOIs remain unresolved.
- HTTP blocks, robots disallows, and short pages may lower the source-found rate.
