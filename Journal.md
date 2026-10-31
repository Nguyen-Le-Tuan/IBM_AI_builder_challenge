# Project Journal — Inline Evidence Highlights

**IBM AI Builders Challenge — North America 2026**
Team: **Le Tuan**, **Lok Sang**, **Truyen Anh**

This file is the team's shared source of truth. Humans and each member's Claude sessions should use it to see what was discussed, what was decided, and what is still open. Read §0–§2 before doing anything else, then check [`HUMAN_TODO.md`](HUMAN_TODO.md) for current progress.

---

## How to use this file

### Status tags

Every claim or plan item should carry one of these tags. Never present one kind as another.

| Tag | Meaning |
|---|---|
| `DECIDED` | Agreed by the team. Record who decided it and when. |
| `RECOMMENDED` | Proposed, usually by Claude. Not yet agreed by the team. |
| `OPEN` | Needs a decision. |
| `HYPOTHESIS` | A belief that needs evidence before we rely on it. |
| `VERIFIED` | Checked against a primary source. Give the date and link. |
| `MOCK` | Illustrative or fictional data. Never present it as a real result. |

### Editing rules (humans and Claude sessions)

1. Run `git pull` before editing.
2. When a decision changes, update the table in §1 in place and add a row to §2. Never delete old rows in §2; mark them `SUPERSEDED by D-xxx`.
3. Record discussions as new entries at the **end** of §15, newest last, with the heading `### YYYY-MM-DD — <who> (+ Claude) — <topic>`.
4. §3–§14 hold the current plan. If you change one of them, say what changed in your §15 entry.
5. Make small commits with messages like `journal: <what changed>`. If two people append at the same time and hit a merge conflict, keep both entries.
6. Do not invent metrics, citations, provenance chains, independent-source counts, competitor gaps, or "first in market" claims.

### Background

The original handoff (full prior discussion, competitor notes, design philosophy) is `IBM_AI_Challenge_Context_Prompt.txt`, kept by Le Tuan. It may not be committed. This journal summarizes the parts that matter.

---

## 0. Summary

We are building a Chrome extension. A reader clicks **Check** on a social-media post that cites a scientific or health finding. The extension then:

- highlights the exact phrases where the post differs from the source it relies on;
- shows a compact evidence card next to the cursor on hover, with the post wording and the source wording side by side;
- shows the chain post → article → study, but only along links we can actually observe.

The system does not claim to decide universal truth. It shows **where** the post differs from its evidence and **what** the evidence says, so the reader can check it themselves.

**Central question.** Can we help a reader SEE exactly how a social-media claim differs from its evidence, inspect that evidence immediately, and recover the missing context, without turning an uncertain AI judgment into another misleading authority?

---

## 1. Current state (as of 2026-10-31)

On 2026-10-31, Le Tuan endorsed the overall plan in §5–§12 as the working direction. Items marked `RECOMMENDED` still need team agreement.

| Item | Status | Value / notes |
|---|---|---|
| Team | `DECIDED` 2026-10-31 (Le Tuan) | Le Tuan, Lok Sang, Truyen Anh. Roles are `OPEN` (see §12.1). |
| MVP domain | `DECIDED` 2026-10-31 (Le Tuan) | Social posts that cite a **scientific/health finding**. Scholarship/job ads move to v2. |
| Human vs agent work split | `DECIDED` 2026-10-31 (team) | Agents (Claude Code / Codex) do automatable work from detailed prompts in `prompts/`. Humans do sampling decisions, credentials, audits and held-out gold labels (D-004). Exception D-005: Codex with computer use may capture R1 seeds from public Reddit pages (logged out, read only). |
| Core framing | `RECOMMENDED` (endorsed) | Claim-to-source **diff**, not truth classification (§5). |
| Label system | `RECOMMENDED` (endorsed) | Two layers: span relation colour + claim-level verdict (§5). |
| Track | `RECOMMENDED` | AI for Good. Not registered yet. |
| Content class | `RECOMMENDED` | Posts with a link or explicit citation. Text only. |
| Platform | `OPEN` (was `RECOMMENDED`) | Own fixture feed page + one real-platform adapter. The Reddit DOM was checked: `shreddit-post` exposes `content-href`, `post-title`, `created-timestamp` and `permalink`; old Reddit uses different markup. **But** Reddit's primary policy texts conflict with research collection (see the next row), so the real-platform choice is reopened (D-006). |
| Platform policy | `VERIFIED` 2026-10-31 (Codex T1) | Reddit Responsible Builder Policy: "Any research that uses Reddit data collected outside of the RFR Program is in violation of this policy." Reddit User Agreement: no collecting data "by any means (automated or otherwise)" except as permitted. X ToS prohibits crawling or scraping without written consent. None of these documents addresses a user-click extension reading the page being viewed. See `docs/research/platform_policies.md`. |
| R1 pilot | `VERIFIED` mechanically; semantics provisional (audit pending) | 29 Reddit seeds (target 36; r/nutrition yielded 1/8). Source passage found within 2 hops: **21/29 (72%)**, almost all at hop 1. Primary reachable: only **5/29**. Hop 1 blocked or paywalled: 7/29. All quotes were re-verified independently by Claude. Details in §15. |
| Trigger | `RECOMMENDED` | User clicks Check. No automatic feed scanning in the MVP. |
| Language | `RECOMMENDED` | English (the submission must be in English). |
| Model training | `RECOMMENDED` | No training or fine-tuning in the MVP. |
| LLM provider | `OPEN` | Choose by dev-set results. Include an IBM Granite model (watsonx.ai) in the comparison. |
| API budget | `OPEN` | Unknown as of 2026-10-31. |
| Search API | `OPEN` | Less critical, since sources come from links. Only needed as a fallback. |
| Deployment | `OPEN` | Single small backend container. Host not chosen. |
| Eligibility (F-1) | `OPEN` | Le Tuan is emailing BeMyApp (drafted 2026-10-31). Each member must confirm their own eligibility. |
| Product code before Bob access | `RECOMMENDED` | Do not write any (see §3). |

---

## 2. Decision log

| ID | Date | Decision | By | Status |
|---|---|---|---|---|
| D-001 | 2026-10-31 | MVP domain = scientific/health findings cited in social posts | Le Tuan | `DECIDED` |
| D-002 | 2026-10-31 | Team = Le Tuan, Lok Sang, Truyen Anh | Le Tuan | `DECIDED` |
| D-003 | 2026-10-31 | `Journal.md` is the shared source of truth; `HUMAN_TODO.md` tracks progress | Le Tuan | `DECIDED` |
| D-004 | 2026-10-31 | Delegate automatable work (fetching, link-following, metadata lookup, quote extraction, normalization, metrics, reports) to coding agents via detailed prompts in `prompts/`. Humans do only: actions on social platforms (terms), sampling decisions, credential setup, audits of agent output, and gold labels. Dev labels may be agent-pre-annotated and human-corrected; held-out labels must be human and independent of model output. | Team (Le Tuan, Lok Sang, Truyen Anh) | `DECIDED`. The "humans capture social posts" clause is superseded by D-005 for Reddit only. |
| D-005 | 2026-10-31 | Codex with computer use may capture R1 seeds from **public Reddit pages, logged out and read only**, through `prompts/phase0_codex_agent.md` with `ALLOW_SOCIAL_BROWSING=reddit-logged-out`. Constraints: a fixed sampling frame, ≤150 page loads, no CAPTCHA or bot-check workarounds, no use of personal accounts. Le Tuan accepts the platform-terms risk that Claude flagged: Reddit's terms reportedly restrict automated access whatever the interface. Verifying this on Reddit's own pages is Codex task T1. API access to social platforms stays forbidden. | Le Tuan (teammates to confirm) | `DECIDED`. Under review in D-006: the run used a signed-in session, and the primary policy conflicts. |
| D-006 | 2026-10-31 | **To decide:** after the verified Reddit policy conflict, (a) keep, quarantine or delete the 29 Reddit pilot rows; (b) build dev and held-out data from non-Reddit sources (e.g. SPICED, our own fixture posts, a permissive platform); (c) choose the real-platform adapter, if any; (d) whether D-005 stays in force. | Team | `OPEN` |

---

## 3. Verified competition facts

Source: [Official Rules PDF](https://res.cloudinary.com/ideation/image/upload/q_100,f_pdf,dpr_auto/id-ai-builders-ch-2b8138/k1oxs4lhvebv8a8awv7n), titled "[FINAL] AI Builders Challenge - North America Official Rules". Read 2026-10-30. Rules may be amended during the contest (§9 of the rules), so re-check the Event Platform before relying on these.

### Dates and registration (`VERIFIED`)

- **Contest Period:** 2026-11-02 to 2026-12-02. Entries are due by **5:00 PM ET on December 2** (rules §4–5).
- **Registration:** "Individuals must complete registration on the Event Platform during the Contest Period. You must register individually." So each member registers from Nov 2 onward.
- **Team rules:** teams have 1–5 participants, and nobody can be on more than one team. One submission per individual. The submission must be in English.

### Submission requirements (rules §5, `VERIFIED`)

- "A functioning prototype or proof of concept developed primarily using IBM Bob."
- A published project page that includes:
  - the problem;
  - the AI/technical approach "and how you used IBM Bob";
  - a **3-minute max** video;
  - presentation slides;
  - all team member details;
  - SkillsBuild certificates for **every** team member.
- A repository link is **not** listed as required.

### Judging (rules §6, `VERIFIED`)

There are four criteria. Each judge scores each criterion **1–5**, for a maximum of 20, so the criteria carry **equal weight**:

- **Technical Execution** — "Effective use of IBM and open source technologies, with a functional and well-structured solution."
- **Innovation** — "Creativity, originality, and unique application of AI."
- **Challenge Fit** — "Relevance to the challenge and ability to address real-world problems."
- **Implementation & Feasibility** — "Practicality, scalability, and potential for real-world use."

Scores are never made public.

### Prizes (rules §7, `VERIFIED`)

- The pool is $15,000: 1st $10,000, Runner-up $3,000, Best AI for Good Project $1,000, Best Wildcard Solution $1,000.
- There is no Business-specific prize.
- Whether one project can win more than one prize is **not addressed**.

### Prior work and IP

- **Pre-existing code is not addressed** in the rules. Because the prototype must be "developed primarily using IBM Bob", we recommend writing **no product code before Bob access**. Planning, the labeling guideline, schema design, UI design and manual dataset collection are fine.
- **IP** (rules §10): use only materials "clear of any intellectual property or other third party rights". For the demo this means:
  - do not show other people's real posts or copyrighted article screenshots casually;
  - do not use Facebook logos or branding in our feed page.
- **Not confidential** (rules §10): "Solutions are not confidential", and IBM may work on similar ideas. Anything we put on the project page is effectively public. With mentors, share only what is needed.

### Eligibility (rules §3)

- Rule text (`VERIFIED`): the entrant must be "a student enrolled at an institution of higher education", 18+, and "a legal resident of the United States of America OR Canada (excluding the province of Quebec)". They must also be eligible under the [BeMyApp Eligibility Policy](https://eligibility.bemyapp.com/), last updated May 24, 2022.
- **"Legal resident" is not defined** in either document. Prize payment may require a W-9 or **W-8BEN** (rules §8). That hints the organizers expect non-US tax filers, but it is an inference, not an answer.
- **Action:** ask BeMyApp in writing at logistics@bemyapp.com. Each member must check their own eligibility.

### IBM Bob (`VERIFIED` from [docs](https://bob.ibm.com/docs/ide), 2026-10-30)

- Bob is an IDE with Agent, Plan and Ask [modes](https://bob.ibm.com/docs/ide/features/modes), plus a terminal variant (Bob Shell).
- It has per-task [rollback snapshots](https://bob.ibm.com/docs/ide/features/rollback) and supports MCP, rules and skills.
- It runs on Linux (Debian package listed), Windows and macOS.
- [Bobalytics](https://bob.ibm.com/docs/ide/features/bobalytics), which reports "Bob factor" (the % of committed lines Bob created), is **Enterprise-only**. On the trial we must keep our own record of Bob's contribution (see §12.3).
- From Codex T7 (`VERIFIED` 2026-10-31; see `docs/research/ibm_bob.md`):
  - The trial is 30 days with 50 Bobcoins; usage per action varies.
  - No full chat or task export was found, and unpinned task history is deleted after 30 days idle. Copy key Bob outputs into `BOB_LOG.md` as you go.
  - Bob loads a workspace `AGENTS.md` by default, so it will follow our `AGENTS.md` → `CLAUDE.md` rules.

---

## 4. Product vision (Le Tuan's core idea — preserve)

People browsing social media encounter several kinds of problem content:

- misleading posts;
- claims stripped of their conditions;
- old information presented as current;
- scam-like ads.

The extension annotates content **where the user is already reading it**.

**Core interaction loop.** Read a post → notice a precise highlight → hover → understand exactly what is supported, contradicted, missing or uncertain → open the evidence if desired.

**Design principles** (Le Tuan's preferences, `DECIDED`):

- A strong first visual impression, then real working functionality and technical substance.
- Flat, restrained colours with **no gradients**. Pastel inline highlights, readable text, subtle borders and shadows.
- A familiar social-feed layout, not a generic analytics dashboard.
- The hover card sits near the pointer, anchored to the phrase, and never covers it.
- Colour is always paired with an icon and status text.
- **No fake live results, no fabricated citations.**
- The original post must stay distinguishable from our annotations. We never silently rewrite it.
- This is not "paste text into a chatbot". A paste box is acceptable only as a dev harness or fallback.

**Earlier "wow" features**, now mapped onto the MVP:

- **A. Pinpoint the exact distortion.** Span-level typed findings (§5).
- **B. Path of information.** `ProvenanceEdge` and `lost_at_hop` (§10), built only from observed links or DOIs.
- **C. Collapse repeated reporting** ("6 articles → 1 original"). Stretch goal, and only via observed links or attributions.
- **D. Restore missing context.** Context notes on omission findings (§5).

---

## 5. Framing and label system

### Reframe (`RECOMMENDED`, endorsed)

The system answers **"Where does this post differ from the source it relies on?"**, not "Is this post true?".

The output is a **pair of quotations side by side** plus a difference type, for example `"prevents"` ↔ `"was associated with a lower incidence of"`. The reader can verify it in seconds, so authority moves from the model to the evidence pair. The model can still be wrong, for instance by picking the wrong source sentence or misreading it, but its mistakes are **visible**.

### Two-layer labels

**Layer 1 — highlight colour.** This describes the relation between one post span and one source, not universal truth.

| Colour | Label (UI copy) | Meaning | Example finding types |
|---|---|---|---|
| Mint | Matches source | The source says the equivalent | — |
| Amber | Changed from source | The source differs in degree, scope or conditions | `scope_broadened`, `certainty_strengthened`, `causality_strengthened`, `condition_omitted`, `population_omitted`, `quantity_altered` |
| Coral | Contradicts source | The source **explicitly** states something incompatible | `quantity_contradicted`, `population_contradicted`, `direction_contradicted`, `fact_contradicted` |
| Lavender | Time mismatch | A source date makes the "current" framing wrong | `stale_presented_as_new`, `superseded_presented_as_current` |
| Slate | Not found in source | Not in the source, or the source is inaccessible | no judgment made |

The full v0 type list (6 Amber, 4 Coral, 2 Lavender, 2 Slate), verdict rules, span rules and edge cases are in [`docs/labeling_guideline_v0.md`](docs/labeling_guideline_v0.md) (`RECOMMENDED`, awaiting team review).

**Layer 2 — claim verdict.** Shown in the card: `supported`, `contradicted`, `not_established` or `conflicting`. It always states which source(s) it is relative to.

### Policy rules

1. **Coral requires an explicit source statement.** If the conflict is only implied (e.g. "every international student" vs "selected applicants"), it is Amber with type `scope_broadened`. False accusations are the most costly error.
2. **Several flags on one span.** The colour follows the priority Coral > Amber > Lavender > Slate > Mint, and the card lists every flag.
3. **Omissions have no span.** If a post drops "in mice", there is no text to highlight. Anchor the finding to the affected phrase (the subject, outcome or verb) and show a context-restoration note, e.g. "Study population: mice."
4. **No numeric truth scores.** No "72% true". Show the evidence basis instead, e.g. "1 source: study abstract, retrieved 2026-11-10".
5. **Lack of evidence is not falsity.** A source containing a claim does not prove it. "Official" means authority for a specific fact, not immunity from error.
6. **No authority without inspection.** If a source is paywalled or unreachable, show Slate ("Source unavailable — not judged").

---

## 6. Assessment against the judging criteria (Claude, 2026-10-30)

**Technical Execution.**
- **Risk:** looking like "an extension that calls an LLM and colours text".
- **Where the points come from:** the non-LLM parts, namely exact DOM span anchoring, verbatim quote verification, link-based provenance, and measured results.
- **IBM levers** (use only if measured to help):
  - [Docling](https://arxiv.org/abs/2408.09869) (IBM Research, MIT licence) for HTML/PDF source extraction.
  - [Granite Guardian](https://arxiv.org/abs/2412.07724) groundedness detection as a secondary check.
  - A Granite model on watsonx.ai as an LLM candidate.

**Innovation.**
- "AI fact-check + coloured highlights + sources" is **not novel**. Factiverse already highlights claims.
- **What could be novel** (`HYPOTHESIS`): a typed, phrase-level diff between a post and the source it cites, plus showing *which hop* dropped a condition.
- Research confirms this is a real and hard problem:
  - [Wührl et al., Findings of ACL 2024](https://arxiv.org/abs/2402.12431) annotated 1,600 finding pairs (paper ↔ news/tweets) for causal claim strength, certainty, generality and sensationalism. They found **few-shot LLM prompting underperformed fine-tuned task-specific models**.
  - [SPICED, EMNLP 2022](https://aclanthology.org/2022.emnlp-main.117) has 6,000 finding pairs with an information-matching score.
- This cuts both ways. It validates the problem, but warns that prompting alone may give mediocre accuracy. Those were 2024 models; current models must be measured.

**Challenge Fit.**
- AI for Good fits (health and science misinformation).
- **Weakness:** "people reading social media" is too broad. We need one concrete user making one concrete decision, e.g. "should I believe or share this health post?"

**Implementation & Feasibility.**
- Open-web verification of arbitrary claims in four weeks is **not feasible** at trustworthy quality.
- A narrow scope with measured latency and cost per check **is** feasible, and that is exactly what this criterion asks for.

---

## 7. Biggest risks and the smallest experiment for each

**R0 — Eligibility (non-technical, potentially fatal).**
Email BeMyApp now (see `HUMAN_TODO.md`). Each member checks their own status.

**R1 — Can we get the right source text?**
If a post has no link, or the link is paywalled, everything falls back to Slate.
- **Experiment (no code, allowed before kickoff):** manually collect ~36 posts (12 per member) in the domain into a shared spreadsheet. For each post, record:
  - whether it has a link;
  - whether the link is reachable or paywalled;
  - whether that page contains the underlying finding sentence;
  - whether it links onward to a primary source (DOI or press release).
- **Metric:** the % of posts where a human can find the source sentence within 2 hops.
- **Threshold** (judgment, not a standard): below ~50%, change the content class or add a search fallback.
- **Protocol v1 (hybrid, D-004):**
  - Humans capture ~12 seed posts each, about 30 minutes, by hand.
  - An agent runs [`prompts/r1_enrichment_agent.md`](prompts/r1_enrichment_agent.md) to follow links, fetch metadata, extract and mechanically verify quotes, and compute metrics.
  - Humans audit a 20% sample.
  - Details: [`data/r1/README.md`](data/r1/README.md).
- **Update (D-005):** Codex captures 36 Reddit seeds itself (`seeds_CX.csv`), using the fixed frame in [`prompts/phase0_codex_agent.md`](prompts/phase0_codex_agent.md) T3. That makes the R1 sample Reddit-only and logged-out. Human seeds from X or Facebook stay optional, for platform diversity.

**R2 — Is the span-level diff accurate, and does it avoid false alarms?**
- **Experiment:** 20 hand-labeled (post, source passage) dev pairs, including **6–8 faithful paraphrases** as hard negatives. Run one prompt with structured output.
- **Metrics:** precision per finding type, false-alarm rate on faithful pairs, % of source quotes that match verbatim, latency per stage.
- **Gate:** if false alarms are high, narrow the taxonomy before building the UI.

**R3 — Anchoring and hover on a real page.**
Feeds re-render, "See more" expands text, and the DOM nests deeply.
- **Experiment (1-day spike):** given character offsets, paint highlights with the [CSS Custom Highlight API](https://developer.mozilla.org/en-US/docs/Web/API/CSS_Custom_Highlight_API). It does not mutate the site's DOM, which matters for React feeds. Detect hover by hit-testing `caretPositionFromPoint` against our `Range`s.
- **Note:** `::highlight()` supports only a few properties (background and text colour, text-decoration). It has **no borders**. A subtle border needs an overlay drawn from `Range.getClientRects()`.
- **Pass:** correct spans on 20/20 fixture posts, surviving scroll and expand.

---

## 8. MVP scope

**One sentence.** The user clicks Check on **one post that cites a scientific/health finding**. The extension highlights the phrases distorted relative to the source and shows the chain post → article → study, along observed links/DOIs only, with at most 2 hops.

**Why this domain** (D-001):
- The source chain is often observable through links and DOIs. Structured metadata is available from Crossref, OpenAlex and PubMed, though their terms and rate limits still need checking.
- The distortion taxonomy has a research basis (causality, certainty, generality, sensationalism), so our labels are defensible.
- Public datasets exist for an independent evaluation:
  - SPICED is MIT-licensed per its [HF card](https://huggingface.co/datasets/copenlu/spiced).
  - The [Wührl et al. dataset](https://www.uni-bamberg.de/en/nlproc/resources/sciencecommdistortion/) licence still needs checking.
- The AI for Good impact is clear.
- **Constraint:** we say what the study says. We give **no medical advice**.

**Trade-off vs scholarship/job ads.**
- Ads are closer to students and testers are easier to recruit.
- But ads usually carry no source link, calling something a "scam" is risky, and there is no dataset.
- The same "diff the post against the official page" pipeline can serve scholarship ads in v2.

**Platform** (`RECOMMENDED`).
- **Facebook is the hardest first target:** login wall, obfuscated classes, a virtualized feed, and hard for judges to reproduce.
- **(a) Our own fixture feed page.** Social-feed look, no Facebook branding. Posts are written by us from real distortion patterns and link to real open-access sources. It serves as the dev environment, the regression tests and the video's opening scene. The video must say clearly that it is a test page.
- **(b) One real-platform adapter.** Leaning Reddit: viewable without login, and link posts carry the source URL. Our belief that `shreddit-post` exposes attributes like `content-href` is **unverified**; check it in DevTools.
- Both share one `PlatformAdapter` interface.
- **Data-access constraint** (reported, `HYPOTHESIS` until checked against Reddit's own pages): Reddit's Responsible Builder Policy (announced on r/redditdev, Nov 2025) requires approval for Data API access and names AI agents.
  - Datasets therefore come from human-captured posts, not API or agent scraping.
  - The extension reads the DOM of a page the user is viewing, on user click. It does not use the Data API.
  - Whether the policy affects such extensions is `OPEN`.

**Out of MVP scope:**
- automatic feed checking;
- images, OCR, video;
- multiple platforms;
- "N articles → 1 origin" (stretch goal);
- Vietnamese or other languages (a possible later differentiator, `HYPOTHESIS`);
- fine-tuning.

---

## 9. Architecture (`RECOMMENDED`)

```
Content script ──PostSnapshot──▶ Service worker ──POST /checks──▶ FastAPI + SQLite
 (platform adapter, anchoring,    (network relay, no secrets,     in-process job runner,
  hover card in Shadow DOM)        state in chrome.storage.session) docs cache, results
       ▲                                  │ poll GET /checks/{id}
       └──────────── Annotation ◀─────────┘
```

### Backend pipeline

Each stage is a pure function with Pydantic I/O.

| # | Stage | Input → output | Notes |
|---|---|---|---|
| 1 | `resolve_sources` | PostSnapshot → SourceDoc[] + ProvenanceEdge[] | httpx + Docling or trafilatura (compare on ~20 pages). At most 2 hops, links/DOIs only. |
| 2 | `extract_claims` | post text → Claim[] | The LLM returns **quotes**; **code** computes the offsets, using an occurrence index for repeats. A quote not found in the post is dropped. |
| 3 | `select_evidence` | Claim × SourceDoc → Passage[] | Short documents go in whole; long ones use BM25 top-k. |
| 4 | `compare` | Claim + Passage[] → Finding[] | LLM structured output, no tools. Source text is wrapped and treated as **untrusted data**, never as instructions. |
| 5 | `validate` | Finding[] → Finding[] | `source_quote` must match verbatim after normalization. Dates and numbers are checked deterministically. A failure downgrades the finding to Slate or hides it. |
| 6 | `assemble` | → Annotation | Spans, colours, cards, provenance. |

### Principles

- Stage 5 proves a quote **exists**. It does not prove the **interpretation** is correct; the evaluation in §11 covers that.
- No vector DB, no agent framework, no local GPU in the MVP.
- API secrets live only on the backend, never in the extension.
- Chrome service workers can be stopped at any time, so persist state rather than assume a long-lived background process. The backend owns the job and its recoverable status.
- Bounded work: maximum document size, maximum hops, maximum LLM calls per check, timeouts, and a cache keyed by URL + content hash.

---

## 10. Data contract — `MOCK` example (fictional)

```json
{
  "check_id": "chk_01",
  "status": "complete",
  "post": {"platform": "fixture", "post_id": "p7", "created_at": "2026-11-10T14:02:00Z"},
  "sources": [
    {"doc_id": "d1", "url": "https://news.example/coffee-study", "kind": "news_article", "published_at": "2026-11-08", "retrieved_at": "2026-11-10T14:02:05Z"},
    {"doc_id": "d2", "url": "https://journal.example/abs/123", "kind": "paper_abstract", "published_at": "2026-10-29"}
  ],
  "provenance": [
    {"from": "post", "to": "d1", "basis": "post_link"},
    {"from": "d1", "to": "d2", "basis": "hyperlink", "anchor_text": "published in Journal Example"}
  ],
  "claims": [{
    "claim_id": "c1",
    "post_quote": "Coffee prevents Alzheimer's",
    "span": {"start": 0, "end": 27},
    "verdict": "not_established",
    "relative_to": ["d2"],
    "findings": [
      {"type": "causality_strengthened", "color": "changed",
       "post_quote": "prevents", "post_span": {"start": 7, "end": 15},
       "source_doc": "d2", "source_quote": "was associated with a lower incidence of",
       "source_quote_verified": true,
       "explanation": "Observational association reported; the post states causation."},
      {"type": "population_omitted", "color": "changed", "anchor_reason": "omission",
       "post_span": {"start": 16, "end": 27},
       "source_doc": "d2", "source_quote": "in aged mice", "source_quote_verified": true,
       "lost_at_hop": "d1→post", "context_note": "Study population: mice."}
    ]
  }],
  "trace": {"prompt_version": "compare-v1"}
}
```

- `lost_at_hop` turns feature B from a slogan into data. We compare post↔d1 and d1↔d2, then record at which hop a condition disappeared.
- **Minimum source record:** URL, title, publisher, `published_at` where available, `retrieved_at`, an exact evidence excerpt, and its relation to the claim. Add a content hash for reproducibility.

---

## 11. Three deliverables, not one

|   | Engineering experiment | 3-minute demo | Defensible evaluation |
|---|---|---|---|
| Purpose | Decide continue / narrow / pivot | Let judges *feel* the value | Show it works, and where it fails |
| Form | CLI: post + URL → JSON + per-stage latency | Recording of the real system running | Numbers + method on slides and the project page |
| Data | 20 dev pairs | 3–4 curated posts, including one abstain case | Held-out set frozen **before** prompt tuning |
| Done when | Rough precision / false-alarm numbers exist | The whole story fits in 3:00 | Fair baseline, n, and confidence intervals reported |

### Demo storyboard (draft)

| Time | Scene |
|---|---|
| 0:00–0:12 | A feed with the post "Coffee prevents Alzheimer's, new study shows". Click **Check**. |
| 0:12–0:50 | Highlights appear progressively. Hover "prevents" to show the Amber card: both quotes side by side, the difference type, source and date, and an "Open evidence" button. |
| 0:50–1:20 | Provenance strip post → article → abstract, showing at which hop "in mice" was lost, with the context-restoration note. |
| 1:20–1:45 | Honesty: a faithful post shows Mint; a paywalled source shows Slate, "Source unavailable — not judged". |
| 1:45–2:25 | Evidence it works: held-out results vs baseline, latency p50/p95, cost per check. |
| 2:25–2:50 | How it was built: Bob Plan → Agent workflow, IBM and open-source technologies, one architecture slide. |
| 2:50–3:00 | Impact and next steps. |

If we replay a cached result, label it on screen.

### Evaluation protocol

**Held-out set.**
- ~40 posts, frozen before final prompt tuning, kept separate from the dev set.
- With three members, **double-annotate** every held-out item, have the third member adjudicate disagreements, and report inter-annotator agreement (e.g. Cohen's kappa).

**Metrics**, each reported separately:
- finding precision/recall by type;
- false-alarm rate on faithful posts;
- % of source quotes verified verbatim;
- span exact/overlap match;
- abstention rate;
- provenance-edge correctness.

**Baseline.**
- The strongest search-enabled chatbot we can access gets the same post + URL and is asked to "list where the post differs from the source, with verbatim quotes".
- Score both systems with the same rubric. Ideally the scorer is a member who did not write the prompts and does not know which output came from which system.

**External check.** A subset of the Wührl et al. data for the certainty / causality / generality classifier, if the licence allows.

**Mini user test.**
- 6–10 people, 4 posts each, with and without the extension.
- Measure whether they correctly identify the distortion, and how long it takes.
- Report descriptively only. n is small, so make no significance claims.

**Resources and cost.**
- Measure client RAM/CPU delta (Chrome Task Manager, DevTools Performance/Memory).
- Measure backend latency per stage (median and p95, with n and environment) and tokens/cost per check.
- Report cold vs cached runs. Never estimate in place of measuring.

---

## 12. Roadmap and team process (`RECOMMENDED`)

Calendar notes:
- Nov 2 is a Monday; kickoff webinars are Thu Nov 5.
- Per the event description, the Bob trial link arrives at kickoff.
- **Thanksgiving is Thu Nov 26.** Plan the feature freeze for ~Nov 24 and aim to publish by Dec 1.

| Phase | Dates (approx.) | Goal |
|---|---|---|
| 0 | until Nov 1 | No product code. SkillsBuild certificates, eligibility email, R1 data collection, labeling guideline v0. |
| 1 | Nov 2–4 | Each member registers individually; form the team; choose the track. |
| W1 | Nov 5–11 | With Bob: repo skeleton, Pydantic schemas, CLI pipeline, validators. Run R2 on 20 dev pairs. **Gate.** |
| W2 | Nov 12–18 | Fixture feed, content script (R3 anchoring and hover), hover card, backend wiring, then the real-platform adapter. |
| W3 | Nov 19–24 | Hop-2 provenance, held-out evaluation and baseline, resource and cost measurements. **Feature freeze ~Nov 24.** |
| W4 | Nov 25–Dec 2 | Mini user test, video, slides, project page. Publish by Dec 1; the hard deadline is Dec 2, 5 PM ET. |

### 12.1 Workstreams (`OPEN` — owners not assigned)

| Workstream | Scope | Owner |
|---|---|---|
| A — Backend & NLP | sources, claims, compare, validate, provenance, caching, cost | TBD |
| B — Extension & UI | adapter, anchoring, hover card, fixture feed, design system | TBD |
| C — Data, evaluation & pitch | dataset, guideline, annotation, baseline, user test, video, slides, project page | TBD |

Everyone labels data; that is required for double annotation.

### 12.2 Tooling rule

- The rules require the prototype to be "developed primarily using IBM Bob". **Product code should be written primarily with Bob.**
- Claude sessions are for planning, research, documentation and review, unless the team decides otherwise.
- Any product code written outside Bob must be noted honestly in `BOB_LOG.md`.
- **Data tooling is not product code.** Scripts in `tools/` that agents write for data collection and evaluation are not part of the product (D-004). Keep them out of `backend/` and `extension/`.
- **Agent prompts** live in `prompts/` and are versioned like code. A good prompt states:
  - goal, inputs and outputs;
  - hard rules;
  - stop conditions;
  - a mechanical verification step;
  - a human audit sample.

### 12.3 Recording Bob's contribution

Create `BOB_LOG.md` when Bob access starts. One entry per Bob session:
- date and member;
- mode (Plan, Agent or Ask);
- goal;
- what Bob produced;
- what the human changed or rejected;
- commit hash.

Bob's rollback snapshots are not a contribution record.

---

## 13. Background reference

### Research

- FEVER — https://aclanthology.org/N18-1074/ (Supported / Refuted / NotEnoughInfo with evidence)
- AVeriTeC — https://arxiv.org/abs/2305.13117 (real-world claims, web evidence)
- Multi-hop Evidence Pursuit Meets the Web — https://aclanthology.org/2024.fever-1.2/
- RAG — https://arxiv.org/abs/2005.11401
- Wührl et al. 2024, fine-grained distortions — https://arxiv.org/abs/2402.12431 (ACL Anthology 2024.findings-acl.369)
- SPICED (Wright et al., EMNLP 2022) — https://aclanthology.org/2022.emnlp-main.117
- Full Fact process — https://fullfact.org/about/how-we-fact-check/

These are references only. They do not prove that any method will work on our posts.

### Task framing

- This is evidence-based claim verification and source comparison, **not sentiment analysis**. Tone does not establish truth.
- Keep three levels separate:
  - **task:** extraction, evidence selection, comparison, span localization;
  - **architecture:** retrieval, validation, UI;
  - **training strategy:** prompting first, fine-tuning only after diagnosing errors it can fix.

### Competitors

Read from official pages in an earlier discussion, not tested by us. Availability and features may have changed. Never claim a competitor lacks a feature just because we did not see it.

- **Factiverse** (claim-level red/green highlights + sources — closest) — https://www.factiverse.ai/
- **Originality.ai Fact Checker** — https://originality.ai/automated-fact-checker
- **Factually** — https://www.factually-ai.com/
- **NewsGuard** (source ratings, not claim-level) — https://www.newsguardtech.com/how-it-works/
- **Ground News** (coverage comparison) — https://ground.news/about
- **Google Fact Check Explorer** (existing fact checks only) — https://toolbox.google.com/factcheck/explorer
- **Full Fact AI** — https://fullfact.org/ai/
- **InVID–WeVerify** (media verification toolkit) — https://weverify.eu/verification-plugin/
- **Red-Flag** (hackathon extension precedent) — https://devpost.com/software/red-flag-extension
- **scite.ai** classifies citation statements in papers as supporting/contrasting. It targets a different audience, but is worth checking for overlap (`OPEN`).

### Self-check question

"If someone pasted the same post into a search-enabled chatbot, what concrete value would we still provide?"

Our intended answers are:
- exact inline localization;
- verbatim, verified quote pairs;
- context restoration;
- observed provenance hops;
- lower friction.

These must be **demonstrated** (§11), not asserted.

---

## 14. Open questions

- API budget ceiling (even a rough tier).
- Workstream owners and weekly hours per member.
- LLM provider. Is a watsonx.ai Granite model adequate on the dev set?
- Docling vs trafilatura for source extraction (measure).
- Reddit DOM attributes (verify), or choose X instead.
- Dataset licences (Wührl et al.).
- Eligibility answer from BeMyApp, for each member.
- Deployment host.
- Is work done before Nov 2 (manual dataset, documents) acceptable? We believe yes since it is not code, but it is not addressed in the rules. We may ask the organizers.
- Should we add a fully automated sample from an open platform (e.g. the Bluesky API)? It needs a human-created app password, and it measures a different platform than our demo.
- Does Reddit's Responsible Builder Policy affect browser extensions that read pages the user is viewing? Check Reddit's own pages.

---

## 15. Session log

### 2026-10-30 — Le Tuan (+ Claude) — Handoff review, rules verification, MVP proposal

- **Input.** Le Tuan provided the master handoff context (`IBM_AI_Challenge_Context_Prompt.txt`).
- **Verified by Claude:** the official rules PDF (§3), the BeMyApp eligibility policy, and the IBM Bob docs.
- **Research found** (relevant to the reframe): Wührl et al. 2024, SPICED 2022, Docling, Granite Guardian.
- **Could not verify:** the Reddit DOM, because Claude's browser blocks reddit.com.
- **Claude proposed:**
  - the claim-to-source diff reframe and the two-layer labels (§5);
  - the assessment (§6), risks and experiments (§7) and MVP scope (§8);
  - the architecture and data contract (§9–§10);
  - the three-deliverable split (§11) and the roadmap (§12).

### 2026-10-31 — Le Tuan (+ Claude) — Decisions and repo setup

- Le Tuan endorsed the overall structure and plan.
- **Decided:**
  - D-001: domain = science/health findings cited in posts;
  - D-002: team = Le Tuan, Lok Sang, Truyen Anh;
  - D-003: `Journal.md` + `HUMAN_TODO.md` as shared tracking.
- **API budget:** unknown.
- **Created:** `Journal.md`, `HUMAN_TODO.md`, and `CLAUDE.md` (instructions for every member's Claude).
- **Plan updates for a 3-person team:** double annotation with adjudication, blind baseline scoring, three workstreams (§12.1).
- **Eligibility:** email to BeMyApp drafted for Le Tuan to send. An F-1 question to UB ISSS is deferred.

### 2026-10-31 — Le Tuan (+ Claude) — R1 protocol and labeling guideline v0

- Le Tuan completed the SkillsBuild course. Certificate download not yet confirmed.
- **Created** `data/r1/README.md` and `data/r1/r1_template.csv`:
  - manual collection, 12 posts per member, one CSV per member;
  - sampling rules that take posts in listing order (to avoid cherry-picking) and keep ~1/3 from strict-title venues as hard negatives;
  - privacy and IP rules;
  - the column dictionary and how to compute the R1 metric.
- **Created** `docs/labeling_guideline_v0.md` (`RECOMMENDED`, not yet reviewed by the team):
  - 14 finding types across Amber, Coral, Lavender and Slate;
  - claim-verdict rules and span rules;
  - 14 edge cases;
  - an annotation JSON record aligned with §10;
  - the double-annotation process.
- **Changes vs §5:**
  - Added Coral types `quantity_contradicted`, `population_contradicted`, `direction_contradicted`, `fact_contradicted`.
  - `quantity_altered` now covers reframing only (max→typical, relative→absolute, subgroup→overall).
  - `date_omitted` was replaced by `superseded_presented_as_current`. It is limited to evidence already in our sources.
  - Lavender-only claims can still be `supported`.
- **Open for team review:** see guideline §11.

### 2026-10-31 — Le Tuan, Lok Sang, Truyen Anh (+ Claude) — Automate data work with agents (D-004)

- **Team principle:** humans do only what needs a human; automatable work goes to coding agents with detailed prompts.
- **Claude's caveats, accepted into D-004:**
  - Social platforms restrict automated access, so seed capture stays human. Reddit's 2025 Responsible Builder Policy reportedly names AI agents; this is from secondary sources and not verified.
  - Agent output needs a measured error rate, hence a 20% human audit.
  - Held-out gold labels must be human and independent of model output. Otherwise the evaluation only measures agreement between models.
- **Created:**
  - `prompts/r1_enrichment_agent.md` (v1). Hard rules: no social platforms, no fabrication, mechanical quote verification, robots.txt and rate limits, no paywall circumvention, no commits. It also defines a deterministic audit sample and a report.
  - `data/r1/seeds_template.csv`.
- **Rewritten:**
  - `data/r1/README.md` as protocol v1.
  - `data/r1/r1_template.csv` with seed + enrichment + audit columns.
- **`.gitignore`:** `data/r1/cache/` (fetched third-party text) and `.venv-tools/`.
- **Rule:** prompts live in `prompts/`; data tooling in `tools/` is not product code (§12.2).

### 2026-10-31 — Le Tuan (+ Claude) — Codex computer use for Phase 0 (D-005)

- Le Tuan's Codex can operate a browser through computer use, with full access. Le Tuan asked for one prompt that lets Codex finish the agent-doable Phase 0 work before app design.
- **Claude's caveat:** the interface does not change platform terms. An AI agent operating a browser is still automated access, and Reddit's policy reportedly names AI agents. The recommended alternative was ~30 minutes of human capture.
- **Decision:** Le Tuan accepted the risk with constraints → D-005, which teammates should confirm.
- **Created:**
  - `prompts/phase0_codex_agent.md` (v1), tasks T1–T8:
    - T1 — platform policy check on primary pages;
    - T2 — Reddit DOM check;
    - T3 — 36 Reddit seeds via a fixed sampling frame;
    - T4 — enrichment through `r1_enrichment_agent.md`;
    - T5 — dataset licences;
    - T6 — service tiers and limits;
    - T7 — IBM Bob details;
    - T8 — handoff summary with proposed Journal edits.
  - `AGENTS.md`, so that Codex follows `CLAUDE.md`.
- **Updated:** `CLAUDE.md` now records the D-005 exception. `.gitignore` adds `data/external/`.
- **Still human:** the R1 audit, preferably by Lok Sang or Truyen Anh, since Le Tuan ran the agent; account sign-ups; held-out gold labels.

### 2026-10-31 — Le Tuan (+ Codex, reviewed by Claude) — Phase 0 run results

**Run (Codex, `prompts/phase0_codex_agent.md`).**
- T1, T5 and T7 done; T2, T3, T4 and T6 partial.
- **Outputs:**
  - `docs/research/` — `platform_policies.md`, `reddit_dom_check.md`, `datasets.md`, `services.md`, `ibm_bob.md`, `phase0_summary.md`;
  - `data/r1/` — `seeds_CX.csv`, `seeds_CX_skips.md`, `r1_CX.csv`, `report_CX.md`;
  - `tools/r1/`.
- No tracked files were modified and nothing was committed. No accounts were created.

**Deviations, recorded honestly:**
- Le Tuan explicitly allowed Codex to use the **signed-in** Brave session for T2/T3. D-005 specified logged-out.
- T4's script continued after bot-check signals on CX-015 and CX-020. It did not solve or retry them, but it missed the stop rule.
- T6 stopped at an NCBI reCAPTCHA, as required.
- T3 yielded 29 of 36 seeds: the r/nutrition listing ended at 24 positions with only 1 qualifying post. Codex did not silently fill the gap.

**Claude's independent review:**
- Re-checked all 29 rows with a separate script:
  - columns match the template;
  - seed columns are unchanged;
  - every `main_claim_quote` is in `post_text`;
  - every hop-1 and primary quote is a verbatim substring of the cached source;
  - all quotes are ≤ 40 words.
  - **0 problems.**
- No usernames in the seeds.
- Source-found decisions came from Codex reading the cached pages, hardcoded in `tools/r1/review.py`. They are agent judgments, and the audit is pending.

**R1 numbers (n = 29, provisional):**
- Source found within 2 hops: 21/29 (72%). This is above the ~50% threshold.
- Hop 1: open 22, blocked 6, paywalled 1.
- Primary: open 4, abstract-only 1, not found 24.
- Linked kind: news 19, press release 5, paper 5.
- Interpretation: **the post ↔ linked-page comparison is feasible; the article ↔ study hop is rarely reachable automatically.**

**Candidate distortions Claude noticed** (`HYPOTHESIS`, not labels):
- CX-013 "70% fatality rate" vs "60 to 70 percent historically died" → `quantity_altered` (top of a range presented as the rate).
- CX-016 / CX-024: the vaccine effect is reported without "along with Keytruda" → `condition_omitted`.
- CX-018 "breakthrough in Alzheimer's prevention" vs the abstract's "support further studies" → `certainty_strengthened`.
- CX-027 "shatters ... conjecture" vs "helped researchers extend" → flagged by Codex as the only `distorted` item.
- Codex left 28/29 impressions as `unsure`.
- The guideline types do occur in real posts. This motivates, but does not prove, the taxonomy.

**Domain drift:** some seeds are science but not health (CX-003 politics/law, CX-023 ecology, CX-025 engineering, CX-026 wildlife, CX-027 AI/math, CX-028 history of science). Decide whether "scientific" in D-001 includes these.

**Services and datasets** (`VERIFIED` by Codex):
- watsonx.ai's pricing page advertises a free tier of up to 300,000 tokens/month. An older FAQ says 50,000, so check the real account.
- Code Engine has a monthly free allowance.
- Crossref and OpenAlex work without a key, with stated rate limits.
- SPICED is MIT (6,025 rows, CSV). No licence was found for the Wührl dataset, so do not use it until clarified.

**Design implications to discuss next (Claude):**
1. Make **post ↔ hop-1** the core comparison. Show hop 2 (study) as a bonus only when reachable.
2. 6/29 hop-1 pages blocked server-side fetching. Consider fetching hop 1 in the user's browser on click, weighing privacy and terms.
3. Platform and evaluation-data sourcing must change or be justified after the Reddit policy check (D-006).

### 2026-10-31 — Le Tuan (+ Claude) — R1 audit becomes cross-model + human check

- Le Tuan asked whether Codex could do the audit too.
  - **Claude's answer:** no. A self-audit is circular.
  - A **different** model can re-check every row; this yields agreement, not ground truth. Humans then decide only the disagreements plus 3 random agreements.
- Lok Sang is busy. Truyen Anh (Claude Pro) will run the new prompt `prompts/r1_crossmodel_audit.md` (v1) in Claude Code with the strongest model.
- **Design of the prompt:**
  - Phase A is blind: it uses only the post text and link, and must not read Codex's columns, Journal §15, `report_CX.md`, `phase0_summary.md` or `review.py`.
  - Phase B grades Codex. Access differences are recorded but not counted against Codex.
  - The prompt escalates rows to a human.
  - Because `data/r1/cache/` is gitignored, Truyen Anh's run re-fetches pages. Pages may have changed since Codex's fetch.
- `data/r1/README.md` step 3 and `HUMAN_TODO.md` updated to match.
