# R1 Cross-Model Audit — TA

- **Input:** `data/r1/r1_CX.csv` (29 rows, enriched by Codex)
- **Prompt:** `prompts/r1_crossmodel_audit.md` v1
- **Auditor:** TA (launched the run)
- **Auditor model:** Claude Code, `claude-opus-5-5`
- **Run date:** 2026-10-31
- **Row-level output:** `data/r1/audit_xm_TA.csv`

Everything below compares **two model judgments**. None of it is ground truth. The rows listed in the human review list need a person to decide.

## Method in brief

- **Phase A (blind).** For every row I looked only at `item_id`, `post_date`, `post_text` and `linked_url`. I fetched each link with a script (research User-Agent, ≤1 request/s per domain, 20 s timeout) and kept the text in `data/r1/cache/xm/`, which is gitignored. Then I chose a quote. Every quote was checked in code as a substring of the fetched text after normalization: 21/21 verified, no chat-only rows.
- **Phase B.** Only after Phase A was finished for every row did I read Codex's columns and grade them.
- **Codex quote check.** I also checked Codex's `hop1_finding_quote` against my fetched text. All 20 Codex quotes on pages I could read were found verbatim. The other 2 (CX-005, CX-024) were on pages that showed me a bot check, so they could not be checked.

## Codex grades (n = 29)

| Grade | Count | Share |
|---|---|---|
| correct | 16 | 55% |
| partly | 11 | 38% |
| wrong | 2 | 7% |

- **`partly` comes mostly from missed study links.** In 7 rows the page hyperlinks the study but Codex recorded `primary_link_basis = none`: CX-004, -009, -010, -013, -019, -022, -025. In CX-010 the CMAJ DOI is even printed in the page text. The other `partly` grades are `contains_finding` differing by one step (`yes` vs `partial`), or a quote that covers only part of the post's claim.
- **Wrong rate: 2/29 (7%).** This is below the ~20% threshold in `data/r1/README.md`, metric 9. Both `wrong` rows are escalated.

## Agreement on "source found" (yes/no)

**Found rate.** These are two model judgments:

| Model | Found yes |
|---|---|
| Codex (`source_found_within_2_hops`) | 21/29 (72%) |
| Claude XM (`xm_found`) | 21/29 (72%) |

**Agreement.** The two models agree on **25/29** rows: 19 yes/yes and 6 no/no. **Cohen's kappa = 0.66** (p_o = 0.862, p_e = 0.600).

- The rates are equal, but they come from different rows. 2 rows are yes only for Codex and 2 are yes only for XM.
- Three of the four disagreements are caused by the page opening for one model and not the other. The fourth (CX-027) is a definitional question.
- On the 20 rows that both models could open, they agree on 19.

## Access differences (4 rows)

These are not counted against Codex: the networks differ, and pages change.

| Row | Codex | XM |
|---|---|---|
| CX-005 (nature.com, Sci Rep) | open | blocked: Nature "Client Challenge" bot check (HTTP 200) |
| CX-024 (nature.com, news) | open | blocked: same Nature bot check |
| CX-020 (time.com) | blocked | open (200, 1,339 words) |
| CX-014 (telegraph.co.uk) | paywalled | blocked: 402 Akamai/TollBit "unusual activity" page, not a subscription wall |

Other blocked rows for XM:

- **Cloudflare "Just a moment" (403):** CX-002, -006, -008, -028.
- **CX-015 (406, empty body).** The seed's `linked_url` has a Reddit tracking string glued onto the Time URL. Both that URL and the cleaned time.com URL returned 406, so I classed it `blocked` (it could also be `broken`).

No bot check or paywall was worked around. No archive or cache sites were used, and no social-platform URL was fetched.

## Human review list

Each row is marked `escalate=yes` or `spot_check` in the CSV.

| Row | Flag | Question for the human |
|---|---|---|
| CX-005 | yes | Open the Nature link in a normal browser. Does the page contain Codex's quote ("We report phenotypic and genomic features of a PDR C. auris isolate from Kenya, the second globally."), and does it state the post's finding? I could not load the page. |
| CX-018 | yes | Codex's quote ("…continuing to show its potential to treat a wide range of other conditions") never mentions Alzheimer's. Should it be replaced by "Patients prescribed semaglutide had a 40% to 70% reduced risk of first-time Alzheimer's diagnosis, compared to other antidiabetic medications."? |
| CX-020 | yes | Codex was blocked; I could read the Time page. Should found change to `yes`, using the quote "…researchers from Life Biosciences reported that the treatment appears safe, and two of the recipients show early signs of improved vision."? |
| CX-024 | yes | Same as CX-005. Does the Nature news page contain Codex's quote ("A personalized mRNA vaccine reduced the risk of skin cancer returning or the recipient dying by 42%…")? I could not load the page. |
| CX-027 | yes | The page headline states the post's claim, but the body contradicts it: Gemini only extended solutions, and a different team with a different AI contradicted the conjecture. Does a source that contradicts the post count as "source found" for R1? Codex says no, XM says yes. The team may want to fix this definition. |
| CX-004 | spot_check | Confirm that Codex's quote states the finding. Also confirm the missed study link: the journals.sagepub.com DOI link on the Cornell page. |
| CX-012 | spot_check | Confirm the quote. It matches the post almost word for word. |
| CX-019 | spot_check | Confirm the quote. Also confirm the missed study link: the Nature paper is hyperlinked on the Scientific American page. |

Spot-check rows were drawn from the 24 rows marked `escalate=no` using `random.Random(2026).sample(sorted(ids), 3)`.

## Candidate distortion types (XM, open pages only)

These are **candidates, not labels**, from comparing each post with my quote and its page (guideline v0 §5).

| Type | Count | Rows |
|---|---|---|
| `certainty_strengthened` | 2 | CX-010, CX-017 |
| `quantity_altered` | 2 | CX-013, CX-022 |
| `condition_omitted` | 1 | CX-016 |
| `population_omitted` | 1 | CX-018 |
| `stale_presented_as_new` | 1 | CX-018 |
| `not_in_source` | 1 | CX-021 |
| `fact_contradicted` | 1 | CX-027 (Codex proposed the same type) |

13 of the 21 open rows got no candidate type. Codex proposed a type only for CX-027.

## Limitations

- **Pages may have changed** since Codex fetched them, and the two runs used different networks. Access results therefore differ for 4 rows.
- **Two Codex quotes were graded on plausibility.** For CX-005 and CX-024 I could not verify the quotes.
- **I judged hop 1 and whether a study link is present.** I did not fetch any primary study, because none was needed to decide `xm_found`. So this audit does not re-check Codex's hop-2 work beyond the link itself.
- **Quote choice involves judgment.** "Same finding" and `yes` vs `partial` are judgment calls. Several `partly` grades come from one-step `contains_finding` differences that are defensible either way.
- **This is a two-model agreement check.** It does not replace the human check of the rows above. An earlier Claude session reviewed Codex's output (Journal §1). I did not read that review, but it may have used the same model family.
- **The posts come from a narrow sample.** All 29 are Reddit posts collected under D-005, whose status is under review in D-006 (`OPEN`).
