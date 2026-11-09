# Inline Evidence Highlights

A browser extension that shows **exactly where** a social post differs from the source it cites, with the evidence one hover away.

Team **Le Tuan · Lok Sang · Truyen Anh** · IBM AI Builders Challenge — North America 2026 · Track: AI for Good (planned)

> **Living document.** The sections below evolve as we build. Decisions, reasons and history live in [`Journal.md`](Journal.md); tasks and owners live in [`HUMAN_TODO.md`](HUMAN_TODO.md).

---

## Inspiration

Health and science posts often keep the headline and drop what matters:

- "in mice";
- "may";
- "compared with inactive people";
- "published in 2019".

Fact-check tools usually deliver a verdict *about* a post. We want readers to **see the gap themselves**: the post's words next to the source's words, at the moment they are reading.

## What it does

*Spec as of 2026-11-09. Nothing is built yet.*

1. The user **selects** a post's text on any page and clicks **Check**.
2. The extension reads the link in that post (or asks the user to paste one) and compares the post with that page.
3. Phrases that differ are **highlighted inline**. Hovering opens a card with:
   - the post quote and the source quote side by side;
   - the type of difference;
   - the source and its date;
   - an "open evidence" link.
4. A small strip shows **post → article → study** when the links can actually be observed, as metadata only.

**Highlight colours** describe the relation to the source, not universal truth:

| Colour | Meaning | Example |
|---|---|---|
| Mint | Matches source | faithful paraphrase |
| Amber | Changed from source | "may reduce" → "prevents" |
| Coral | Contradicts source | "50%" when the source says 15% |
| Lavender | Time mismatch | a 2019 study called "new" |
| Slate | Not found / not judged | paywalled or missing |

Every highlight colour comes with an icon and a text label. We show no "% true" scores. Full rules: [`docs/labeling_guideline_v0.md`](docs/labeling_guideline_v0.md).

## How we built this

*Planned. Details in Journal §9.*

- **IBM Bob** is the primary development tool for all product code, as the rules require. We log its use in `BOB_LOG.md`.
- **Extension:** Chrome MV3 + TypeScript.
  - We anchor highlights to the exact text the user selected and draw them with the CSS Custom Highlight API.
  - The hover card lives in a Shadow DOM.
- **Backend:** Python, FastAPI and Pydantic. The pipeline:
  1. resolve sources;
  2. extract claims;
  3. select evidence;
  4. compare;
  5. **validate quotes mechanically**;
  6. assemble the result.
- **Models and tools:**
  - one LLM with structured output; the provider is open, and an IBM Granite model will be in the comparison;
  - Docling or trafilatura for page text;
  - Crossref or OpenAlex for study metadata.
- **Privacy:** we process only the text the user selects, and only transiently. We store no post text.
- **Agents for non-product work:** Claude and Codex handle research and data tasks from versioned prompts in [`prompts/`](prompts/). Humans keep what must stay human: sampling decisions, audits, held-out posts and gold labels.

## Challenges we ran into

| Challenge | What we did |
|---|---|
| "AI fact-check + coloured highlights" already exists. | We focus on **typed, phrase-level differences against the cited source**, with verifiable quote pairs. |
| Social platforms restrict automated data collection. | The extension is selection-first and needs no platform adapters. Our evaluation posts are written by us on public-domain and CC-BY sources (D-006). |
| Many publisher pages block server-side fetching, and studies are often paywalled. | We compare the post with the page it links to first. The original study is shown when it is reachable. *Where to fetch pages is still open (D-008).* |
| An agent grading its own data looks better than it is. | A different model audits the work, and humans settle the disagreements. |
| Measuring an LLM detector on LLM-written posts would inflate the score. | Held-out posts are human-written, labeled blind, and adjudicated. |
| Demo content must be free of third-party rights. | Our own feed page, our own posts, and only public-domain or CC-BY source text (D-009). |

---

## Scope (MVP)

| In | Out (for now) |
|---|---|
| English text posts that cite a science or health finding | Images, OCR, video |
| User-selected text, one post at a time | Automatic feed scanning |
| Comparing the post with its linked page, plus study metadata | Platform-specific adapters |
| Our own demo feed page, plus a "works anywhere" moment on a real page | Model training or fine-tuning |

## Where things are

| Path | What |
|---|---|
| [`Journal.md`](Journal.md) | Source of truth: current state (§1), decisions D-001…D-010 (§2), plan, session log |
| [`HUMAN_TODO.md`](HUMAN_TODO.md) | Tasks, owners, status |
| [`CLAUDE.md`](CLAUDE.md), [`AGENTS.md`](AGENTS.md) | Rules for every AI agent working in this repo |
| [`docs/labeling_guideline_v0.md`](docs/labeling_guideline_v0.md) | Difference types, verdicts, span rules (needs team review, §11) |
| [`docs/research/`](docs/research/) | Verified notes on rules, platform policies, services, datasets, IBM Bob |
| [`data/sources/`](data/sources/) | 55 vetted source pages (20 held-out, 32 dev, 3 reject) |
| [`data/heldout/`](data/heldout/) | **Held-out writing guide, assignments and templates — start here if you are writing posts** |
| [`prompts/`](prompts/) | Agent prompts (versioned) |
| `data/r1/` | Closed pilot, frozen. Do not reuse (D-006) |

---

## 4-week plan (Nov 5 → Dec 2)

Hard deadline: **Wed Dec 2, 5:00 PM ET**. Internal target: **Dec 1**. Feature freeze **Nov 24** (Thanksgiving is Nov 26).

| Week | Dates | Goal | Done when |
|---|---|---|---|
| Prep | Oct 30 – Nov 4 | Rules, scope, research, sources | ✅ Decisions D-001…D-010; 55 sources vetted; guide and templates ready |
| **W1 ← we are here** | Nov 5 – 11 | Bob set up; **pipeline vertical slice**; held-out writing starts | A CLI turns a post + URL into verified JSON on ~20 dev posts; R2 numbers logged; D-008 decided |
| W2 | Nov 12 – 18 | **Extension**: selection, highlight, hover card, fixture feed, backend wiring | Highlights are correct on fixture posts after scrolling; the card shows real pipeline output |
| W3 | Nov 19 – 24 | **Evaluation**: blind labels, adjudication, held-out + SPICED runs, baseline, latency and cost | Numbers with n and kappa; **freeze Nov 24** |
| W4 | Nov 25 – Dec 2 | **Pitch**: mini user test, 3-min video, slides, project page | Project page published by Dec 1 |

**Week-1 checklist** (details in `HUMAN_TODO.md`):

- [ ] Everyone registered on the Event Platform, and SkillsBuild certificates downloaded.
- [ ] Bob trial active; `BOB_LOG.md` started.
- [ ] Held-out posts: LT 14, LS 14, TA 12. **Write them by hand, without AI.**
- [ ] D-008: where hop-1 pages are fetched.
- [ ] Team review of guideline §11 open questions.

## Open questions to research next

- **D-008:** fetch the linked page in the backend, in the user's browser, or from the article tab the user opens? Weigh blocking, privacy, terms and paywalls.
- **LLM provider** under an unknown API budget. Does a watsonx.ai Granite model hold up on the dev set?
- **Guideline v0 §11:** merge `population_omitted` into `scope_broadened`? Is 12 months the right threshold for "old"? What counts as a material change in numbers?
- **Fair baseline:** a search-enabled chatbot given the same post + URL and the same rubric.

## Working together

1. `git pull`, then read Journal §0–§2 and `HUMAN_TODO.md`.
2. **Product code is written with IBM Bob.** Use Claude and Codex for research, data, docs and review (see `CLAUDE.md`).
3. Record decisions in Journal §2 and discussions in §15. Small commits. Never commit secrets.
