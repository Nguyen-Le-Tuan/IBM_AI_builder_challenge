# HUMAN_TODO — Progress Tracker

This file tracks what the team still has to do. The reasoning behind each task lives in [`Journal.md`](Journal.md); section numbers below point there.

**Status:** `[ ]` todo · `[~]` in progress · `[x]` done · `[!]` blocked
**Owners:** LT = Le Tuan · LS = Lok Sang · TA = Truyen Anh · ALL = every member · TBD = not assigned yet

**Update rules**
- `git pull` before editing.
- Change the status box when you start or finish a task, and add the date in the Notes column.
- Claude sessions may update a task's status only after the human confirms it.
- New tasks go at the end of the right phase.

**Hard deadline:** project page published by **Wed Dec 2, 2026, 5:00 PM ET**. Internal target: **Dec 1**.

---

## Blockers / waiting on

| Item | Waiting for | Owner | Notes |
|---|---|---|---|
| Eligibility for F-1 status | Reply from BeMyApp (logistics@bemyapp.com) | LT | Draft written 2026-10-31 |
| API budget ceiling | Team decision | ALL | Needed before choosing an LLM provider |
| IBM Bob access | Trial link at kickoff (~Nov 5) | ALL | Write no product code before this (Journal §3, §12.2) |

---

## Phase 0 — Before Nov 2 (no product code)

| Status | Task | Owner | Notes |
|---|---|---|---|
| [~] | Complete the SkillsBuild course "How IBM Bob and AI Tools Are Changing the Way Solutions Are Built" and download the certificate | LT | Required for submission. Course completed 2026-10-31 (LT confirmed); certificate PDF download not yet confirmed |
| [ ] | Same course and certificate | LS | |
| [ ] | Same course and certificate | TA | |
| [ ] | Send the eligibility email to BeMyApp; save the reply | LT | Draft in the chat of 2026-10-31 |
| [ ] | Each member checks their own eligibility: student, 18+, legal residency (rules §3) | ALL | Journal §3 |
| [ ] | Read the official rules PDF (7 pages) | ALL | Link in Journal §3 |
| [ ] | Read Journal.md §0–§12 | LS, TA | |
| [ ] | Agree on workstream owners (A backend/NLP, B extension/UI, C data/eval/pitch) and weekly hours | ALL | Journal §12.1; record the decision in Journal §2 |
| [ ] | Agree on an API budget ceiling (even a rough tier) | ALL | Record in Journal §2 |
| [ ] | **Run the Codex Phase 0 agent** (`prompts/phase0_codex_agent.md`, T1–T8): policies, Reddit DOM, 36 Reddit seeds, enrichment, dataset licences, service limits, Bob details, summary | LT | Launch with `ALLOW_SOCIAL_BROWSING=reddit-logged-out` and `R1_CONTACT_EMAIL`. Commit the current state first so `git diff` shows only Codex's changes |
| [ ] | Review Codex output (`git diff`, `docs/research/phase0_summary.md`), then commit | LT | Do not commit `data/r1/cache/` or `data/external/` (they are gitignored) |
| [ ] | Confirm D-005 (Codex browsing public Reddit pages, logged out) | LS, TA | Journal §2 |
| [ ] | (Optional) Human seeds from X or Facebook for platform diversity, 6 each → `seeds_LS.csv`, `seeds_TA.csv` | LS, TA | Rules in `data/r1/README.md`. Codex T4, or a re-run of `r1_enrichment_agent.md`, enriches them |
| [ ] | **R1 step 3:** audit the `audit_selected=yes` rows of `r1_CX.csv` (~15 min) | LS or TA | Not LT, who ran the agent. Fill `audit_result`, `audit_notes`, `auditor` |
| [ ] | **R1 step 4:** combine the R1 reports (`report_CX.md` plus any human-seed reports), record the numbers in Journal §15 and any decision in §2 | TBD (C), agent can draft | If >20% of audited rows are `wrong`, fix the prompt and re-run before trusting the numbers. Below ~50% source-found → revisit the content class |
| [ ] | Decide whether to add an automated open-platform sample (e.g. the Bluesky API) | ALL | Optional. Needs a human-created app password. Journal §14 |
| [~] | Write labeling guideline v0: finding types, Coral vs Amber rule, omissions, abstain | TBD (C) | Draft by Claude 2026-10-31 at `docs/labeling_guideline_v0.md` |
| [ ] | Review guideline v0 and answer its §11 open questions; record agreed changes | ALL | Do this before labeling the dev set |
| [ ] | Verify the Reddit DOM in DevTools (does `shreddit-post` have `content-href`, `post-title`, `created-timestamp`?) | Codex T2 | Output: `docs/research/reddit_dom_check.md` |
| [ ] | Check the licences of the Wührl et al. dataset and SPICED for evaluation use | Codex T5 | Output: `docs/research/datasets.md` |
| [ ] | Check free tiers and terms: watsonx.ai (Granite), Code Engine, Crossref / OpenAlex / PubMed | Codex T6 | Output: `docs/research/services.md` |

## Phase 1 — Nov 2–4: Registration

| Status | Task | Owner | Notes |
|---|---|---|---|
| [ ] | Register individually on the Event Platform (registration must happen during the Contest Period) | LT | From Nov 2 |
| [ ] | Register individually | LS | |
| [ ] | Register individually | TA | |
| [ ] | Form the team on the platform | ALL | |
| [ ] | Choose the track (AI for Good recommended) | ALL | Record in Journal §2 |
| [ ] | Attend the kickoff webinars (Thu Nov 5) | ALL | |
| [ ] | Activate the Bob trial when the link arrives | ALL | |
| [ ] | Create `BOB_LOG.md` and start logging every Bob session | ALL | Journal §12.3 |

## Week 1 — Nov 5–11: Pipeline vertical slice + R2

| Status | Task | Owner | Notes |
|---|---|---|---|
| [ ] | Repo skeleton: backend (FastAPI), extension (MV3 TS), `.env.example`, no secrets committed | A | With Bob |
| [ ] | Pydantic schemas following the Journal §10 data contract | A | |
| [ ] | CLI pipeline: post + URL → JSON (stages 1–6) | A | |
| [ ] | Validators: verbatim quote match, offset computation, dates, numbers | A | |
| [ ] | Label 20 dev pairs, including 6–8 faithful paraphrases | C + ALL | Dev set only, never reused for held-out |
| [ ] | **R2 run:** precision per type, false-alarm rate, % of quotes verified, per-stage latency | A + C | |
| [ ] | **GATE:** continue, or narrow the taxonomy | ALL | Record the decision in Journal §2 |

## Week 2 — Nov 12–18: Extension

| Status | Task | Owner | Notes |
|---|---|---|---|
| [ ] | Fixture feed page: social-feed look, no Facebook branding, our own posts linking to real open-access sources | B | Journal §8 |
| [ ] | **R3 spike:** Custom Highlight API + hover hit-testing; 20/20 fixture posts correct after scroll and expand | B | Journal §7 |
| [ ] | Hover card UI (Shadow DOM, flat colours, icon + text per label, side-by-side quotes) | B | Journal §4–§5 |
| [ ] | Service worker relay + backend job polling | A + B | |
| [ ] | Real-platform adapter (Reddit, or X if the DOM check fails) | B | |

## Week 3 — Nov 19–24: Provenance + evaluation (feature freeze ~Nov 24)

| Status | Task | Owner | Notes |
|---|---|---|---|
| [ ] | Hop-2 provenance (post → article → study) with `lost_at_hop` | A | |
| [ ] | Freeze the held-out set (~40) **before** final prompt tuning | C | |
| [ ] | Double-annotate the held-out set, adjudicate, and report agreement (kappa) | ALL | |
| [ ] | Baseline run: search-enabled chatbot, same rubric, blind scoring | C | Journal §11 |
| [ ] | Resource / latency / cost measurements (p50/p95, n, environment; cold vs cached) | A + B | |
| [ ] | External check on the Wührl et al. subset (if the licence allows) | C | |
| [ ] | **Feature freeze** | ALL | ~Nov 24 (Thanksgiving is Nov 26) |

## Week 4 — Nov 25–Dec 2: Pitch and submission

| Status | Task | Owner | Notes |
|---|---|---|---|
| [ ] | Mini user test: 6–10 people, with and without the extension | C | Report descriptively |
| [ ] | Record the demo video (≤ 3:00); label any cached replays | C + ALL | Storyboard in Journal §11 |
| [ ] | Presentation slides | C | |
| [ ] | Project page: problem, AI/technical approach, **how we used IBM Bob**, video, slides, team details, certificates | C + ALL | |
| [ ] | Final check against rules §5 (submission checklist below) | ALL | |
| [ ] | **Publish the project page** | LT | Target Dec 1; hard deadline Dec 2, 5 PM ET |

---

## Submission checklist (rules §5)

- [ ] A functioning prototype developed primarily using IBM Bob
- [ ] Project page: the problem we solve
- [ ] Project page: AI/technical approach and how we used IBM Bob
- [ ] Video presentation, 3 minutes max
- [ ] Presentation slides
- [ ] All team member details
- [ ] SkillsBuild certificate: Le Tuan
- [ ] SkillsBuild certificate: Lok Sang
- [ ] SkillsBuild certificate: Truyen Anh
- [ ] Everything in English
- [ ] Project page **published**, not left as a draft
