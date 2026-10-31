# Phase 0 handoff — 2026-10-31

## Task table

| Task | Status | Output |
|---|---|---|
| T1 Platform policies | done | `docs/research/platform_policies.md` |
| T2 Reddit DOM | partial | `docs/research/reddit_dom_check.md`; inspected in the user's signed-in Brave session by explicit later instruction, rather than logged out |
| T3 Reddit seeds | partial | `data/r1/seeds_CX.csv`, `data/r1/seeds_CX_skips.md`; 29 of target 36, because r/nutrition's listing ended after 24 positions |
| T4 R1 enrichment | partial, pending human audit | `data/r1/r1_CX.csv`, `data/r1/report_CX.md`, `tools/r1/enrich.py`, `tools/r1/verify.py`, `tools/r1/review.py`, `tools/r1/refetch_doi.py`; fetched text/logs in ignored `data/r1/cache/`. Bot-check signals at CX-015 and CX-020 should have stopped the initial run; the script continued. No check was solved or retried. |
| T5 Dataset licences | done | `docs/research/datasets.md`; Wührl licence not found, so no download |
| T6 Services and limits | partial | `docs/research/services.md`; stopped on an NCBI browser check/reCAPTCHA during a later documentation reopening |
| T7 IBM Bob details | done | `docs/research/ibm_bob.md` |

No other populated `data/r1/seeds_*.csv` existed at run time. No account was created, no social API was contacted, and no commit was made.

## Key facts

- `VERIFIED` [Reddit Responsible Builder Policy](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy), accessed 2026-10-31: research data collection outside its approved researcher program conflicts with the policy; its apps section names bots and AI agents. The [User Agreement](https://redditinc.com/policies/user-agreement) also restricts collection by automated or other means. The team's policy choice needs review despite user authorization for this browser session.
- `VERIFIED` [X Terms](https://x.com/en/tos), accessed 2026-10-31: crawling and scraping without written consent are prohibited.
- `VERIFIED` Reddit's current post markup exposed `shreddit-post` title, timestamp, permalink and external-link attributes in the signed-in view; old Reddit used `.thing.link`. See the [DOM note](reddit_dom_check.md).
- `VERIFIED` [Wührl dataset page](https://www.uni-bamberg.de/en/nlproc/resources/sciencecommdistortion/) lists 1,600 pairs and four distortion characteristics, but no licence was found on that page. [SPICED card](https://huggingface.co/datasets/copenlu/spiced) lists MIT, 6,025 rows, and paper/news/tweet pairs. Licence reach over third-party source text remains unverified.
- `VERIFIED` [IBM watsonx.ai pricing](https://www.ibm.com/products/watsonx-ai/pricing) currently advertises a free playground up to 300,000 foundation-model tokens/month; [IBM Bob pricing](https://bob.ibm.com/pricing) lists a 30-day/50-Bobcoin trial. Neither entitlement was activated here.

## R1 headline numbers

From [`report_CX.md`](../../data/r1/report_CX.md), **n=29** seeds: a verified supporting passage within two hops was found for **21/29 (72.4%)**. A link was present for **29/29**; the linked page was blocked, broken, or paywalled for **7/29**; an observed primary hyperlink or DOI was recorded for **7/29**; primary full text or abstract was accessible for **5/29**. Human impressions are blank for **29/29**. Model impressions are unsure **28/29** and distorted **1/29**. Median agent time was **1.81 s/row** (n=29); human seed time was not recorded. Image/video-only exclusions were **0/78 listing positions**. All 29 output rows passed mechanical verification. These are agent judgments, not gold labels; the audit is still pending.

## Needs human

1. Audit the deterministic R1 sample **CX-010, CX-014, CX-017, CX-018, CX-019, CX-022**, ideally by a teammate who did not run enrichment. Complete `audit_result`, `audit_notes`, and `auditor`; adjudicate any incorrect source match before trusting the metrics. The report also lists 15 rows needing attention for partial access or low confidence.
2. Decide whether the 29 signed-in Reddit seeds are acceptable for internal R1 use given the original logged-out D-005 constraint and verified Reddit policy conflict. r/nutrition yielded 1 of 8 target posts. If 36 is required, define and approve a new sampling frame; do not silently fill the gap from another venue. Collect X or Facebook seeds manually if platform diversity is wanted.
3. Check the Wührl dataset licence and any form/gate before use; review third-party news/tweet rights before redistributing SPICED text.
4. Complete any desired accounts or trials: IBM Bob, watsonx.ai, IBM Cloud Code Engine, and optional OpenAlex/PubMed keys. Verify actual regional model availability, budget, and eligibility. The NCBI reCAPTCHA was left untouched. Recheck PubMed limits in an authorized browser session if needed.
5. Review four HTTP 403 linked pages, two bot-check signals (CX-015 and CX-020), one HTTP 402 paywall, the malformed CX-015 link, and unresolved primary sources only through allowed access. Contest registration and individual eligibility remain human work.

## Decisions the team must make

- Keep Reddit as the real-platform MVP adapter, seek a permission path, or change platforms after the policy review.
- Accept the 29-row R1 sample as a pilot, or run a revised sampling frame to reach the planned 36; set the threshold for proceeding after the human audit.
- Choose whether SPICED is only a research/evaluation aid, and whether Wührl can be used once its licence is clarified.
- Choose provider, model, deployment host, and spending cap after checking actual account entitlements. Confirm the Bob usage plan before product coding.

## Proposed Journal updates (for human review; do not paste as decisions without team agreement)

### §1 Current state

Add an `R1 pilot` row: `VERIFIED` 2026-10-31 — 29 Reddit seeds from the fixed frame, 21/29 source matches by agent review, all 29 mechanically verified, six-row human audit pending. Mark enrichment partial because the initial script continued after two bot-check signals. r/nutrition listing ended at 24 positions; one seed qualified. Add a `Platform policy` row: `OPEN` — Reddit primary policy restricts research/agent collection; the team must review D-005. Update the `Platform` note to say that a signed-in Reddit DOM sample was observed, with old Reddit markup differing. Keep model/provider and deployment rows `OPEN` until account entitlements and dev-set results exist.

### §2 Decision log

Proposed discussion item, **not a decision yet**: `D-006 | 2026-10-31 | Review D-005 after primary Reddit policy check and signed-in capture: retain the 29 pilot rows, seek permission, or change the real-platform plan; decide whether a new frame is needed for the seven missing r/nutrition rows. | Team | OPEN`. Do not mark `DECIDED` or supersede D-005 until the team acts.

### §15 Session log

`### 2026-10-31 — Le Tuan (+ Codex) — Phase 0 research and R1 pilot`

`Codex completed the primary platform-policy check, a read-only Reddit DOM inspection, 29 fixed-frame seed records, a partial R1 enrichment with cached quotes and a deterministic six-row audit sample, dataset/licence research, a partial service-limit check, and Bob documentation research. Le Tuan explicitly allowed the existing signed-in Brave session, replacing the prompt's logged-out condition for this run. T4's initial script detected bot-check signals on CX-015 and CX-020 and continued, missing the stop rule; it did not solve or retry either check. T6 browsing stopped at an NCBI reCAPTCHA. The agent found supporting passages for 21/29 seeds, a provisional result pending human audit. See docs/research/phase0_summary.md and data/r1/report_CX.md. Proposed plan changes: review Reddit policy/D-005, decide how to handle the r/nutrition shortfall, and check actual IBM account entitlements before implementation.`
