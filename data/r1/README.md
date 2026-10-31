# R1 — Source-acquisition experiment (manual, no code)

**Question.** For real social posts that report a scientific or health finding, can a human find the source sentence behind the post within **2 hops**? The hops are post → linked page → primary study.

If not, the pipeline will mostly output Slate ("not found in source"), and we need to change the content class or add a search fallback. See `Journal.md` §7.

**Status:** protocol v0, drafted 2026-10-31. Allowed before kickoff because it is manual data collection, not code.

---

## Who collects what

- Each member collects **12 posts**, so ~36 in total.
- Each member works in their **own file** to avoid merge conflicts:
  - `data/r1/r1_LT.csv` (Le Tuan)
  - `data/r1/r1_LS.csv` (Lok Sang)
  - `data/r1/r1_TA.csv` (Truyen Anh)
- To start, copy `r1_template.csv` and rename it. You can edit it in Google Sheets or Excel, but export as **CSV (UTF-8)**.
- **Time box:** about 2–3 hours per person. If a post takes more than 15 minutes, stop, record what you found, and move on. The time spent is data too.

## What counts as a post

**Include** a post if it:
- reports a scientific, medical, health or nutrition **finding** ("study finds…", "researchers discovered…", "X linked to Y");
- is in English;
- has its key claim in text: the post body or a link-post title.

Posts **with no link** are allowed if they name a source ("a Harvard study…"). Record `has_link = no`; those show how often our link-following approach fails.

**Exclude:**
- posts whose key claim exists only in an image or video (count them in your notes, but don't fill a row);
- pure opinion, jokes, questions and ads;
- comments (top-level posts only).

## Sampling rules (to avoid cherry-picking)

We need **both faithful and distorted** posts. A dataset of only juicy distortions would make our false-alarm rate impossible to measure.

1. Pick a venue and a listing first, e.g. "r/science, Top, This Week" or "X search: `study finds`, Latest".
2. Take qualifying posts **in the order they appear**. Don't skip a post because it looks boring or accurate.
3. Record the venue and listing in `how_found`.
4. Across the team, aim for roughly:
   - **~1/3 from strict-title venues**, e.g. r/science, which requires titles that reflect the source; likely faithful, and good hard negatives;
   - **~2/3 from general venues**, e.g. r/Health, r/nutrition, r/Futurology, r/EverythingScience, X, public Facebook pages, Threads.
5. Cover at least 2 platforms across the team.

## Privacy and IP rules

- **Collect by hand only.** No scraping scripts or browser automation: it is too early for code, and platform terms apply.
- **Do not record usernames or profile links.** `post_url` is enough.
- These real posts are for **internal research only**. Never show them in the demo video, slides or project page; the demo uses our own fixture posts (rules §10, `Journal.md` §3).
- Quotes from sources should stay short, ≤ 40 words.

---

## Column dictionary

| Column | Allowed values / format | How to fill |
|---|---|---|
| `item_id` | `LT-001`, `LS-001`, `TA-001`… | Your initials + a running number. |
| `collector` | `LT` / `LS` / `TA` | |
| `collected_at` | `YYYY-MM-DD` | The date you recorded the row. |
| `platform` | `reddit` / `x` / `facebook` / `threads` / `other` | |
| `how_found` | free text | Venue + listing, e.g. `r/science top week`. |
| `post_url` | URL | Permalink to the post. |
| `post_date` | `YYYY-MM-DD` or empty | If visible. |
| `post_text` | text | Copy the visible post text **verbatim**: title + body, expanded ("See more"). Remove line breaks if your editor struggles; otherwise keep them. |
| `claim_in_image` | `yes` / `no` | `yes` if important parts of the claim are only in an image. |
| `has_link` | `yes` / `no` | Does the post link to a source? |
| `linked_url` | URL or empty | The first source link in the post (hop 1). |
| `linked_kind` | `news_article` / `press_release` / `paper` / `abstract` / `preprint` / `video` / `social_post` / `other` | Type of the hop-1 page. |
| `hop1_access` | `open` / `paywalled` / `broken` / `blocked` / `n/a` | Could you read the page? |
| `hop1_contains_finding` | `yes` / `partial` / `no` / `n/a` | Does hop 1 contain the finding the post states? |
| `hop1_finding_quote` | ≤ 40 words, verbatim | The hop-1 sentence closest to the post's claim. |
| `primary_url` | URL or empty | The study, preprint, dataset or press release that hop 1 relies on. |
| `primary_link_basis` | `hyperlink` / `doi` / `named_only` / `none` | How hop 1 points to it: a clickable link, a DOI, only a name ("published in JAMA"), or nothing. |
| `primary_access` | `open` / `abstract_only` / `paywalled` / `not_found` / `n/a` | What you could read of the primary source. |
| `primary_date` | `YYYY-MM-DD` or `YYYY` | Publication date of the primary source. |
| `primary_finding_quote` | ≤ 40 words, verbatim | The primary sentence closest to the post's claim, usually from the abstract. |
| `source_found_within_2_hops` | `yes` / `no` | **The R1 metric.** `yes` if you found a sentence in hop 1 or the primary source that the post's claim can be compared against. |
| `initial_impression` | `faithful` / `distorted` / `unsure` | Your quick judgment **before** careful labeling. It is not a label. |
| `distortion_notes` | free text | Short notes using guideline type names where possible, e.g. `causality_strengthened (linked→prevents); population_omitted (mice)`. See `docs/labeling_guideline_v0.md`. |
| `minutes_spent` | integer | Rough minutes for this row. |
| `notes` | free text | Anything odd: retraction notice, multiple studies, etc. |

### Filled example — `MOCK` (fictional, do not copy into data files)

| Column | Example value |
|---|---|
| `item_id` | `LT-000` |
| `platform` | `reddit` |
| `how_found` | `r/Health new` |
| `post_text` | `Coffee prevents Alzheimer's, new study shows` |
| `has_link` | `yes` |
| `linked_url` | `https://news.example/coffee-study` |
| `linked_kind` | `news_article` |
| `hop1_access` | `open` |
| `hop1_contains_finding` | `partial` |
| `hop1_finding_quote` | `Coffee drinkers had a lower rate of Alzheimer's-like changes, researchers said.` |
| `primary_url` | `https://journal.example/abs/123` |
| `primary_link_basis` | `hyperlink` |
| `primary_access` | `abstract_only` |
| `primary_date` | `2026-10-29` |
| `primary_finding_quote` | `Caffeine intake was associated with a lower incidence of amyloid pathology in aged mice.` |
| `source_found_within_2_hops` | `yes` |
| `initial_impression` | `distorted` |
| `distortion_notes` | `causality_strengthened (associated→prevents); population_omitted (mice)` |

---

## Computing the result (after all three files are in)

Report these numbers in `Journal.md` §15 with **n** stated:

1. **R1 metric:** % of rows with `source_found_within_2_hops = yes`.
   - **Decision threshold** (judgment, not a standard): below ~50%, revisit the content class or plan a search fallback. Record the decision in Journal §2.
2. % of rows with `has_link = yes`.
3. Of the posts with links: % where hop 1 is `paywalled` / `broken` / `blocked`.
4. % with `primary_link_basis` = `hyperlink` or `doi`. This tells us whether hop 2 can be automated.
5. % with `primary_access` = `open` or `abstract_only`.
6. Distribution of `initial_impression`. This gives a rough faithful-vs-distorted mix, but it is not a label.
7. Median `minutes_spent`. This lets us estimate the cost of building the dev and held-out sets.
8. Count of posts skipped because the claim was only in an image or video. This sizes the text-only limitation.

The R1 posts can seed the dev and held-out sets later. Decide the split **before** any prompt tuning, and keep held-out items out of prompt development.
