# Held-Out Set — Writing Guide v0

**Status:** v0, 2026-11-02. Follows D-006 and D-010 in `Journal.md` §2 and the evaluation protocol in §11.
**Who:** Le Tuan (LT), Lok Sang (LS), Truyen Anh (TA).
**Time:** about 5–8 minutes per post, so roughly 1.5–2 hours per person.

This set is the **final exam** for our system. We report its numbers to the judges, so it has to be clean.

---

## The three rules that matter most

1. **Write every post yourself. No ChatGPT, Claude, Codex, Bob, or grammar AI**, not even for editing. LLM-written posts leave patterns that an LLM detector finds too easily, which would make our score look better than it really is (D-006). Imperfect English is fine; real posts are imperfect.
2. **Never show your answers to the person who labels your posts.** Your `variant`, `intended_verdict` and findings are the answer key. Labelers work only from the blind packets described under "What happens next".
3. **Only use the source page assigned to you.** Every claim in a distorted post must relate to that page, so a reader can compare the two.

---

## Your assignment

Open `assignments.csv`. Each row is one source. Your rows are the ones where `writer` is your initials.

| Writer | Sources | Your posts are labeled by | Adjudicated by |
|---|---|---|---|
| LT | SRC-004, 009, 012, 049, 015, 027, 033 (7) | LS | TA |
| LS | SRC-005, 044, 054, 003, 019, 025, 029 (7) | TA | LT |
| TA | SRC-007, 052, 055, 026, 031, 040 (6) | LT | LS |

If someone is unavailable, swap roles and add a note in `Journal.md` §15. Never label or adjudicate your own posts.

**For each source, write two posts:**

- **one faithful post**: true to the source, but paraphrased;
- **one distorted post**: containing **1 or 2** deliberate differences of the guideline types.

`suggested_primary_type` and `optional_secondary_type` spread the types across all 20 distorted posts. You may choose a different type if the suggestion does not fit naturally. Say so in `notes`.

## Files you create

Copy the templates and name them with your initials, so nobody gets a merge conflict:

- `posts_template.csv` → `posts_<XX>.csv`
- `findings_template.csv` → `findings_<XX>.csv`

You can edit them in Google Sheets or Excel. Export as **CSV (UTF-8)**.

### `posts_<XX>.csv`: one row per post

| Column | What to write |
|---|---|
| `post_id` | `HO-<XX>-01`, `HO-<XX>-02`, … **Number your posts in a mixed order**, so the faithful post is not always the odd number. |
| `source_id` | e.g. `SRC-004` |
| `writer` | Your initials |
| `variant` | `faithful` or `distorted` |
| `post_text` | The post, in English, 1–4 sentences, ≤ 60 words. End with the source URL, as people do when sharing a link. |
| `post_date` | The date the post pretends to be published. Default `2026-11-15`. |
| `main_claim_quote` | Copy-paste the part of `post_text` that states the main finding. It must match exactly. |
| `intended_verdict` | `supported`, `not_established`, `contradicted` or `conflicting`, using the rules in the table below |
| `written_at` | Today's date |
| `minutes_spent` | Rough minutes |
| `notes` | Anything worth knowing, e.g. "changed the suggested type because…" |

**Verdict rules** (guideline §6):

| Post | `intended_verdict` |
|---|---|
| Faithful post | `supported` |
| Distorted post with any Coral type | `contradicted` |
| Distorted post with Amber or Slate types only | `not_established` |
| Distorted post with Lavender types only (e.g. an old study called "new") | `supported`, because the finding itself is still right |

### `findings_<XX>.csv`: one row per deliberate difference

- **Distorted posts:** one row per difference (1–2 rows).
- **Faithful posts:** no rows. That is the point: the system should find nothing.

| Column | What to write |
|---|---|
| `post_id` | The distorted post's ID |
| `finding_no` | 1, 2 |
| `type` | A type name from `docs/labeling_guideline_v0.md` §5, e.g. `population_omitted` |
| `post_quote` | Copy-paste the **shortest** phrase in your post that carries the difference, e.g. the verb "prevents" or the number "50%". It must match the post exactly. For an omission, use the phrase the omission affects (guideline §7). |
| `occurrence` | `1`, unless the same phrase appears twice before it |
| `anchor_reason` | `omission` for omission types; otherwise leave it empty |
| `source_quote` | Copy-paste the sentence from the **source page** that shows the difference. Keep it to ≤ 40 words, verbatim. |
| `context_note` | Required for omissions only: the missing fact, e.g. `Study population: mice.` |
| `explanation` | One neutral sentence: "The source reports X; the post states Y." Never use "misleading", "fake" or "lie". |

---

## How to write good posts

### Faithful posts are hard negatives

Make them **sound different** from the source while keeping every important detail:

- Keep the **population**. If the study was in mice, say mice.
- Keep the **hedge**. If the source says "may", don't say "does".
- Keep **association vs cause**.
- Keep **key conditions**: dose, comparison group, subgroup.
- Keep the **numbers**. Ordinary rounding is fine: 48% → "about half".
- Casual tone, emojis, hashtags and opinions about *why it matters* are fine. **No new factual claims.**

### Distorted posts should look like real social posts

- Make the change look like something a real person might write: a punchy headline, a dropped condition, a confident verb. **Avoid cartoonish lies.**
- Mix obvious and subtle distortions across your posts.
- Change only what you list in `findings_<XX>.csv`. Everything else must stay faithful.
- **Lavender `stale_presented_as_new`:** use words like "new study" or "just published", with a source published more than 12 months before `post_date`.
- **Slate `not_in_source`:** add a claim the post attributes to the research, but which the page does not contain.

### Never

- Give medical advice ("you should stop taking…").
- Name or invent real private people.
- Write hateful or stigmatising text.
- Use the rejected or flagged sources. Your assignments do not include any.

---

## Example — `MOCK` (fictional source, do not copy)

**Source (fictional):** "In a 12-week trial of 60 adults with mild insomnia, drinking chamomile tea nightly **may modestly improve** self-reported sleep quality compared with a placebo drink."

**Faithful post** (`HO-XX-01`, `supported`):

> Small 12-week study: adults with mild insomnia who drank chamomile tea every night *might* sleep a bit better than a placebo group 🍵 Not a miracle, but interesting. https://example.org/chamomile

**Distorted post** (`HO-XX-02`, `not_established`):

> Chamomile tea cures insomnia, scientists confirm 😴 https://example.org/chamomile

| post_id | finding_no | type | post_quote | anchor_reason | source_quote | context_note | explanation |
|---|---|---|---|---|---|---|---|
| HO-XX-02 | 1 | certainty_strengthened | scientists confirm | | may modestly improve self-reported sleep quality | | The source reports a possible modest improvement; the post states it is confirmed. |
| HO-XX-02 | 2 | scope_broadened | cures insomnia | | adults with mild insomnia | | The source studied a modest change in mild insomnia; the post claims a cure for insomnia in general. |

---

## What happens next

1. **Validate (agent).** An agent mechanically checks that every `post_quote` and `main_claim_quote` is in the post, and that every `source_quote` is on the source page. It reports problems; it never edits your text.
2. **Blind packets (agent).** An agent writes `blind_<labeler>.md` with only `post_id`, URL, date and post text, shuffled. It contains no variant, verdict or findings.
3. **Blind labeling (human).** The assigned labeler labels each post using `docs/labeling_guideline_v0.md`, without seeing the answer key, and saves the results to `labels_<labeler>.csv` (same columns as findings, plus one verdict per post).
4. **Adjudication (human).** The adjudicator compares the writer's intent with the labeler's labels and writes the final `gold.csv`. Disagreements are useful: they show where the guideline is unclear.
5. **Agreement (agent).** An agent computes Cohen's kappa on verdicts and on finding presence per type.

Before step 3, the team should answer the open questions in guideline §11. Writing can start now.

## Checklist before you commit

- [ ] Two posts per assigned source: one `faithful`, one `distorted`.
- [ ] Every distorted post has 1–2 rows in `findings_<XX>.csv`; faithful posts have none.
- [ ] Every `post_quote` and `main_claim_quote` is copy-pasted from the post.
- [ ] Every `source_quote` is copy-pasted from the source page.
- [ ] No AI tools were used to write or edit posts.
- [ ] Files saved as `posts_<XX>.csv` and `findings_<XX>.csv`, CSV (UTF-8).
