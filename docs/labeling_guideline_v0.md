# Labeling Guideline v0 — Post ↔ Source Differences

**Status:** `RECOMMENDED`. Drafted by Claude on 2026-10-31 for team review. It is not yet agreed. Change it through the team and log changes in §11.

**Scope:** MVP domain D-001, social posts that report a scientific or health finding and cite a source. Text only, English only.

**Related:** `Journal.md` §5 (label system) and §10 (data contract); `data/r1/README.md` (R1 collection).

---

## 1. What we label and why

We do **not** label whether a post is "true". We label **where and how a post differs from the source it relies on**, with verbatim evidence from both sides. Every label must be checkable by another person who reads the two quotes.

These labels serve three purposes:

- the dev set, for building prompts;
- the held-out set, for honest evaluation;
- the explanation text shown in the hover card.

The type list is our own. It was inspired by the four distortion dimensions in [Wührl et al. 2024](https://arxiv.org/abs/2402.12431): causal claim strength, certainty, generality and sensationalism. It is **not** identical to their annotation scheme, so do not compare numbers directly.

## 2. Units

| Unit | Definition |
|---|---|
| **Post** | The visible post text, with title + body expanded. Comments are not included. |
| **Claim** | One checkable statement in the post about what research found. A claim has slots: *subject/exposure, outcome, relation, population, quantity, conditions, time, attribution*. |
| **Reference source** | The claim-appropriate source the claim is compared against (§3). |
| **Finding** | One typed difference between a post span and a source quote. A claim can have 0..n findings. |
| **Verdict** | The claim-level summary, relative to the named reference source (§6). |

### What not to annotate

- The poster's own opinions, jokes, questions, calls to action and personal advice, unless the post presents them as what the research shows.
- Text that appears only in images or video.
- Hashtags, emojis, links and @mentions.
- Comments.
- Non-English text.

## 3. Choosing the reference source

1. The reference for "what the study found" is the **primary research output**: the paper, abstract, preprint, or official dataset or report. Use it whenever any part of it is accessible.
2. If only the abstract is accessible, compare against the abstract. A claim about details that are not in the abstract gets `not_in_source` with the note `abstract_only`.
3. If the primary source is not accessible at all, use the hop-1 page (news article or press release). Set `reference_level: secondary`.
4. For a claim about what an organization said (e.g. "WHO recommends…"), the reference is that organization's own page.
5. Record the hop where a difference first appears (`lost_at_hop`) whenever you can compare more than one level. See §8, case 9.

## 4. Procedure for one post

1. Read the whole post. Note `post_date` if it is visible.
2. Mark each **claim** by copying its exact text (`post_quote`). Split compound sentences into atomic claims only when they have different subjects or outcomes.
3. Open the reference source and find the closest passage. Copy a **verbatim** quote of at most 40 words.
   - Prefer one contiguous sentence.
   - Never stitch quotes together silently. If you must join two parts, mark the gap with `[...]`.
4. Compare the claim **slot by slot**:

   | Slot | What to compare |
   |---|---|
   | Population / scope | humans? animals? cells? which group? |
   | Relation | association or causation? |
   | Certainty | hedged ("may", "suggests") or definitive ("proves")? |
   | Quantity | number, unit, relative vs absolute, maximum vs typical |
   | Conditions | dose, duration, comparison group, subgroup, baseline risk |
   | Time | when the study was published vs "new" framing |
   | Attribution | who found it; peer-reviewed or preprint; study type |

5. Create one **finding** per material difference (§5). Use the span rules in §7.
6. Assign the claim **verdict** (§6).
7. If you are not sure, set `confidence: low` and write a note. Do **not** force a label; adjudication will resolve it.

## 5. Finding types

Each type maps to one highlight colour. The colour shows **the relation to the source**, not universal truth.

### Amber — "Changed from source"

The source supports only a weaker, narrower or more qualified version of the claim. Nothing in the source explicitly contradicts the post.

| Type | Definition | Positive example (`MOCK`) | Not this type |
|---|---|---|---|
| `causality_strengthened` | The source reports an association, or causation only under conditions. The post states direct causation. Typical markers: *causes, prevents, cures, boosts, makes you, leads to*. | Source: "associated with lower incidence". Post: "**prevents**". | Source itself says "caused" in a randomized trial → no finding. |
| `certainty_strengthened` | The source is hedged ("may", "suggests", "preliminary", "small pilot") or is a single study. The post presents the finding as settled. | Source: "results suggest a possible benefit". Post: "Scientists **confirm**…". | Post keeps the hedge ("may help") → no finding. |
| `scope_broadened` | The post names a broader subject, population or setting than the source, without the source explicitly excluding it. | Source: "adults over 65 in Japan". Post: "**people** who drink tea…". | Post says "in humans" but the source says "in mice" → Coral `population_contradicted`. |
| `population_omitted` | The source population is non-human (animals, cells) or a narrow group, **and** the post names no population at all. A reader would assume people in general. | Source: "in aged mice". Post: "Coffee prevents Alzheimer's". | The post names a population → use `scope_broadened` or `population_contradicted`. |
| `condition_omitted` | A qualifier needed to interpret the result is dropped: dose, duration, comparison group, subgroup-only result, absolute baseline risk, "only in combination with X". | Source: "at doses equivalent to 8 cups per day". Post omits the dose. | A minor methodological detail that does not change the meaning → no finding. |
| `quantity_altered` | The number is reframed rather than changed: a maximum becomes typical ("up to 30%" → "30%"), relative becomes absolute, or a subgroup's result is presented as the overall result. | Source: "reduced relative risk by 50% (2% → 1%)". Post: "**half of people** avoided it". | A different number for the same quantity → Coral `quantity_contradicted`. Ordinary rounding (48% → "about half") → no finding. |

### Coral — "Contradicts source"

The source **explicitly** states something incompatible with what the post **explicitly** states. If the incompatibility is only implied, use Amber instead.

| Type | Definition | Positive example (`MOCK`) |
|---|---|---|
| `quantity_contradicted` | A different value for the same measured quantity. | Source: "15% reduction". Post: "**50%** reduction". |
| `population_contradicted` | The post names a population that the source explicitly says it did not study. | Source: "in mice". Post: "**in humans**". |
| `direction_contradicted` | Opposite direction, or effect vs no effect. | Source: "no significant difference". Post: "**improves** memory". |
| `fact_contradicted` | Another explicit factual mismatch: study type, publication status, institution or author, or an explicitly stated date. | Source: preprint, not peer-reviewed. Post: "**published in a peer-reviewed journal**". |

### Lavender — "Time mismatch"

| Type | Definition | Positive example (`MOCK`) |
|---|---|---|
| `stale_presented_as_new` | The post frames the finding as new or recent ("new study", "just published", "this week"), but the primary source was published **more than 12 months** before the post date. The 12-month threshold is a v0 choice. | Post (2026): "**New** study…". Study published 2019. |
| `superseded_presented_as_current` | The post presents a finding or recommendation as current, and an accessible source **we already have** shows it was revised or retracted (e.g. a retraction notice on the article page). Do not go searching the open web for newer versions in v0. | Article page shows "This paper was retracted"; the post cites it as current. |

Citing an old study **without** "new" framing is legitimate and gets no time finding. If a post explicitly states the wrong publication date, use Coral `fact_contradicted`.

### Slate — "Not found in source"

| Type | Definition |
|---|---|
| `not_in_source` | The claim, or a key slot of it, cannot be found in the accessible reference source. Includes conclusions the post adds and attributes to the research. |
| `source_unavailable` | The reference source is paywalled, broken or blocked, so no comparison is possible. Make no judgment. |

### Mint — "Matches source"

No finding. The claim's main span is shown as Mint when the verdict is `supported`. A faithful paraphrase is a match: "linked to lower risk" for "associated with reduced incidence" is Mint.

### Colour priority on one span

When findings of different colours fall on the same span, the span takes the highest-priority colour:

**Coral > Amber > Lavender > Slate > Mint**

The card lists every finding.

## 6. Claim verdicts

The verdict is always relative to the reference source named in the record.

| Verdict | Rule |
|---|---|
| `supported` | The reference states the same finding (paraphrase allowed), with no Amber, Coral or Slate findings. Lavender findings are allowed: the finding may be accurate while the "new" framing is not. |
| `contradicted` | At least one Coral finding on the claim. |
| `not_established` | No Coral, but at least one Amber or Slate finding. The source supports only a weaker or narrower version, or does not contain the claim. |
| `conflicting` | Two claim-appropriate sources **at the same level** (e.g. two studies) disagree. Rare. A news article disagreeing with the study it cites is **not** conflicting: use the study and record `lost_at_hop`. |

## 7. Span rules

- Mark the **minimal contiguous phrase** that carries the difference:
  - the verb for causality ("prevents");
  - the certainty marker ("confirm", "proves");
  - the subject or quantifier for scope ("people", "all adults");
  - the number with its unit ("50%");
  - the time word ("new").
- Include a determiner or quantifier when it creates the problem ("**all** adults"). Exclude trailing punctuation, emojis and hashtags.
- **Omissions** have no span of their own. Anchor them to the phrase whose meaning the omission changes, usually the outcome or the subject. Then:
  - set `anchor_reason: omission`;
  - write a `context_note` that restores the missing context, e.g. "Study population: mice."
- If the same phrase occurs more than once in the post, record `occurrence` (1 = first).
- Two findings may share a span if their types differ.

## 8. Edge cases

1. **Faithful paraphrase** → no finding, `supported`. These are our hard negatives. Label them as carefully as the distortions.
2. **Hedge dropped** ("may reduce" → "reduces") → `certainty_strengthened`.
3. **Single study → "science says" / "scientists confirm"** → `certainty_strengthened`.
4. **Mice → people.** If the post says "in people", use `population_contradicted` (Coral). If the post names no population, use `population_omitted` (Amber).
5. **Relative vs absolute risk.** "Cuts risk by 50%" for a 2% → 1% change is technically accurate as relative risk, so it gets no finding. Optionally add `condition_omitted` with the context note "absolute risk 2% → 1%" if the baseline is needed to interpret the result. If the post states the number as absolute, use `quantity_altered`.
6. **"Up to X"** → "X" → `quantity_altered`.
7. **Odds ratio vs risk** ("triples risk" for OR = 3.0). Do not flag in v0. Set `confidence: low` and add a note.
8. **Preprint called "published" or "peer-reviewed"** → `fact_contradicted` if the post explicitly says so. "New research" alone → no finding.
9. **Upstream distortion.** The post faithfully repeats the news article, but the article overstated the study. Record the finding against the primary source with `lost_at_hop: primary→hop1`. The card will say the change happened upstream, not in the post. This is the core of our provenance feature.
10. **Abstract-only access.** If a claim depends on full-text details → `not_in_source` with the note `abstract_only`.
11. **Several studies linked.** Compare each claim to the study it refers to. If that is unclear, note it and set `confidence: low`.
12. **Retraction or correction notice** seen on a source page → `superseded_presented_as_current` if the post presents the finding as valid. Always note it.
13. **Sensational wording** without a factual change ("shocking", "miracle"). Not labeled in v0 (see §11).
14. **Satire, questions, jokes** → skip the post.

## 9. Writing explanations and context notes

- **One neutral sentence:** "The source reports `<X>`; the post states `<Y>`."
- **Never** use words that judge intent: *misleading, lie, fake, hoax, scam*.
- **No medical advice.** Describe what the study reported, not what the reader should do.
- A context note states the missing fact only: "Study population: mice." / "Dose: about 8 cups per day." / "Published: 2019."

## 10. Annotation record

One JSON object per post per annotator. Field names follow `Journal.md` §10 so that labels can be compared directly with pipeline output. Labels are stored as JSONL (one object per line); the file location will be decided when the dev set is built.

```json
{
  "item_id": "LT-000",
  "annotator": "LT",
  "post_date": "2026-11-10",
  "reference": {"url": "https://journal.example/abs/123", "level": "primary", "access": "abstract_only", "published_at": "2026-10-29"},
  "hop1_url": "https://news.example/coffee-study",
  "claims": [
    {
      "claim_id": "c1",
      "post_quote": "Coffee prevents Alzheimer's",
      "occurrence": 1,
      "verdict": "not_established",
      "findings": [
        {"type": "causality_strengthened", "post_quote": "prevents", "occurrence": 1,
         "source_quote": "was associated with a lower incidence of amyloid pathology",
         "explanation": "The source reports an association; the post states prevention.",
         "lost_at_hop": "hop1→post", "confidence": "high"},
        {"type": "population_omitted", "post_quote": "Alzheimer's", "occurrence": 1,
         "anchor_reason": "omission", "source_quote": "in aged mice",
         "context_note": "Study population: mice.", "lost_at_hop": "primary→hop1", "confidence": "high"}
      ]
    }
  ],
  "notes": "MOCK example, fictional."
}
```

### Process for dev and held-out sets

- **Dev set:** one annotator labels each item, a second member reviews it, and disagreements go to a short discussion.
- **Held-out set:**
  - **Two members label each item independently**, without seeing each other's labels or any model output.
  - The third member adjudicates.
  - Report agreement on (a) claim verdict and (b) finding presence per type, using Cohen's kappa, and span overlap.
- Freeze held-out labels **before** final prompt tuning. Never use held-out items to develop prompts.

## 11. Open questions and changelog

### Open questions for team review

- Should `population_omitted` merge into `scope_broadened`? It is kept separate in v0 because it may be the most frequent case.
- Is a 12-month threshold right for `stale_presented_as_new`?
- Should sensationalism get a type? It is excluded in v0 because it is tone rather than a factual change, and agreement is likely to be low.
- What materiality rule should apply to numbers beyond "ordinary rounding"?
- After R1/R2, merge or drop types that are rare or have low agreement.

### Changelog

- **v0 (2026-10-31):** drafted by Claude for team review.
