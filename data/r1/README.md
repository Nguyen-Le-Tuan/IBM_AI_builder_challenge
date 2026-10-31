# R1 — Source-acquisition experiment

**Question.** For real social posts that report a scientific or health finding, can we find the source sentence behind the post within **2 hops**? The two hops are the page the post links to (hop 1) and the study it relies on (primary).

If not, the pipeline will mostly output Slate ("not found in source"), and we need to change the content class or add a search fallback. See `Journal.md` §7.

**Status:** protocol v1, 2026-10-31. Under D-004, humans do only what needs a human; an agent does the rest.

---

## Workflow

| Step | Who | Time | What |
|---|---|---|---|
| 1. Seeds | Human | ~30 min / 12 posts | Browse normally, then copy each qualifying post into `data/r1/seeds_<XX>.csv`. |
| 2. Enrichment | Agent (Claude Code or Codex) | Unattended | Run `prompts/r1_enrichment_agent.md`. The agent writes `r1_<XX>.csv` and `report_<XX>.md`. |
| 3. Audit | Human | ~15 min | Check the rows marked `audit_selected=yes` and fill in `audit_result`, `audit_notes` and `auditor`. |
| 4. Combine | Agent or human | — | Merge the three reports. Record the R1 numbers in `Journal.md` §15 and any decision in §2. |

### Why step 1 stays human

Platform terms restrict automated access to Reddit, X and Facebook. Reddit's 2025 Responsible Builder Policy reportedly names AI agents explicitly; this comes from secondary sources and has not been verified against Reddit's own pages. A person reading posts in a browser and copying them by hand is ordinary use. The agent never touches a social platform.

### Why step 3 stays human

The agent's output is only trustworthy once someone measures its error rate. A 20% audit gives us that estimate.

---

> **Update (D-005, 2026-10-31):**
> - Codex with computer use may do step 1 for Reddit. It browses logged out and read only, using a fixed sampling frame, via `prompts/phase0_codex_agent.md` (T3). The output is `seeds_CX.csv` with `collector=CX`.
> - Human capture below remains the method for other platforms, and the fallback if Codex is blocked.
> - "Why step 1 stays human" above therefore applies to API access and to other platforms. For Reddit browsing, the team accepted the terms risk; see Journal D-005.

## Step 1 — capturing seeds (human)

Each member captures **12 posts** into their own file, which avoids merge conflicts:

- `data/r1/seeds_LT.csv`
- `data/r1/seeds_LS.csv`
- `data/r1/seeds_TA.csv`

Copy `seeds_template.csv` to start. You can edit in Google Sheets or Excel, but export as **CSV (UTF-8)**. Record your total capture time in your `HUMAN_TODO.md` row.

### What counts as a post

**Include** a post if:

- it reports a scientific, medical, health or nutrition **finding** ("study finds…", "researchers discovered…", "X linked to Y");
- it is in English;
- the key claim is in text (post body or link-post title).

A post **without a link** is fine if it names a source ("a Harvard study…"). These posts show how often link-following fails.

**Exclude:**

- posts whose key claim exists only in an image or video (count them in `seed_notes` of your next row);
- pure opinion, jokes, questions and ads;
- comments (use top-level posts only).

### Sampling rules (avoid cherry-picking)

We need **both faithful and distorted** posts. Otherwise false alarms are impossible to measure.

1. Pick a venue and a listing first, for example "r/science, Top, This Week" or "X search `study finds`, Latest".
2. Take qualifying posts **in the order they appear**. Don't skip a post because it looks boring or accurate.
3. Record the venue and listing in `how_found`.
4. Across the team, aim for:
   - **~1/3 from strict-title venues** such as r/science (likely faithful; good hard negatives);
   - **~2/3 from general venues**: r/Health, r/nutrition, r/Futurology, r/EverythingScience, X, public Facebook pages, Threads.
5. Cover at least 2 platforms across the team.

### Privacy and IP

- Capture seeds by hand. No scraping scripts and no browser automation on social platforms.
- Do not record usernames or profile links; `post_url` is enough.
- These real posts are for **internal research only**. Never show them in the demo video, slides or project page. The demo uses our own fixture posts (rules §10, `Journal.md` §3).
- Fetched article and paper texts stay in `data/r1/cache/`, which is gitignored. Never commit them.

---

## Column dictionary

### Seed columns (human, step 1)

| Column | Format | Notes |
|---|---|---|
| `item_id` | `LT-001`, `LS-001`, `TA-001`… | Your initials + a running number |
| `collector` | `LT` / `LS` / `TA` | |
| `collected_at` | `YYYY-MM-DD` | |
| `platform` | `reddit` / `x` / `facebook` / `threads` / `other` | |
| `how_found` | free text | Venue + listing, e.g. `r/science top week` |
| `post_url` | URL | Permalink to the post |
| `post_date` | `YYYY-MM-DD` or empty | If visible |
| `post_text` | text | Visible text **verbatim**: title + expanded body |
| `linked_url` | URL or empty | The source link in the post. Copy the real destination if the platform shows a shortlink. |
| `claim_in_image` | `yes` / `no` | `yes` if important parts of the claim are only in an image |
| `human_impression` | `faithful` / `distorted` / `unsure` / empty | Optional quick gut call. **Not a label.** |
| `seed_notes` | free text | Optional |

### Enrichment columns (agent, step 2)

| Column | Allowed values |
|---|---|
| `main_claim_quote` | Verbatim span of `post_text` |
| `has_link` | `yes` / `no` |
| `linked_final_url` | URL after redirects |
| `linked_kind` | `news_article` / `press_release` / `paper` / `abstract` / `preprint` / `video` / `social_post` / `other` |
| `hop1_http_status` | Integer or empty |
| `hop1_access` | `open` / `paywalled` / `broken` / `blocked` / `n/a` |
| `hop1_contains_finding` | `yes` / `partial` / `no` / `n/a` |
| `hop1_finding_quote` | ≤ 40 words, verbatim |
| `hop1_quote_verified` | `true` / `false` / empty |
| `primary_url` | URL |
| `primary_doi` | DOI or empty |
| `primary_link_basis` | `hyperlink` / `doi` / `named_only` / `none` |
| `primary_resolved_via` | `crossref_search` or empty |
| `primary_access` | `open` / `abstract_only` / `paywalled` / `not_found` / `n/a` |
| `primary_text_origin` | `fulltext_html` / `abstract_crossref` / `abstract_pubmed` / `abstract_openalex_reconstructed` / `abstract_landing_page` / `press_release` / empty |
| `primary_date` | `YYYY-MM-DD`, `YYYY-MM` or `YYYY` |
| `primary_date_type` | `online` / `print` / `issued` |
| `primary_finding_quote` | ≤ 40 words, verbatim |
| `primary_quote_verified` | `true` / `false` / empty |
| `source_found_within_2_hops` | `yes` / `no` — **the R1 metric** |
| `relevance_confidence` | `high` / `low` |
| `model_impression` | `faithful` / `distorted` / `unsure` — **model output, not a label** |
| `model_candidate_types` | Guideline §5 type names, separated by `;` |
| `model_notes` | ≤ 2 neutral sentences |
| `agent_name` | e.g. `claude-code/claude-opus-5-5`, `codex/<model>` |
| `agent_run_at` | ISO 8601 UTC |
| `agent_seconds` | Number |
| `row_status` | `ok` / `partial` / `seed_invalid` / `error` |
| `verification` | `pass` / `fail:<reasons>` |

### Audit columns (human, step 3)

| Column | Values |
|---|---|
| `audit_selected` | `yes` / `no` (set by the agent) |
| `audit_result` | `correct` / `partly` / `wrong` |
| `audit_notes` | What was wrong: wrong source, a quote that doesn't support the finding, wrong access class, … |
| `auditor` | Initials. Ideally audit someone else's file. |

---

## Metrics (report with n)

1. **R1 metric:** % of rows with `source_found_within_2_hops = yes`.
   - **Decision threshold** (a judgment, not a standard): below ~50%, revisit the content class or plan a search fallback. Record the decision in Journal §2.
2. % of rows with `has_link = yes`.
3. Among posts with links: % of hop-1 pages that are `paywalled`, `broken` or `blocked`.
4. % with `primary_link_basis` = `hyperlink` or `doi` (can hop 2 be automated?).
5. % with `primary_access` = `open` or `abstract_only`.
6. `human_impression` distribution and `model_impression` distribution, reported **separately**.
7. Human seed time (from `HUMAN_TODO.md`) and median `agent_seconds`.
8. Count of posts excluded because the claim was only in an image or video.
9. **Agent audit:** % `correct` / `partly` / `wrong` among audited rows. **If more than ~20% are `wrong`, do not trust metrics 1–5.** Fix the prompt and re-run.

---

## Later use of these posts

R1 posts can seed the dev and held-out sets, but labels follow D-004:

- **Dev set:** may be pre-annotated by an agent, then corrected by a human.
- **Held-out set:** must be labeled by humans independently, **without seeing any model output**. Otherwise the evaluation only measures agreement between models.
