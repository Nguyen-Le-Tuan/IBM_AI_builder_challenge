# Source candidates — LT (2026-11-02)

40 source pages were fetched as raw HTML and retained as extracted text in the ignored `data/sources/cache/` directory. Every CSV finding quote is 40 words or fewer and passed the specified normalized substring check against its cached page. All 40 candidate URLs returned HTTP 200, with at least 150 words of extracted main-page text. The team has not approved a held-out/dev split.

## Counts

- Rights: A 1, B 31, C 8. Demo eligible (A/B): 32; internal-only (C): 8.
- Source type: US government page 9, CC paper 31, press release 0, other 0.
- Domain: health/medicine/nutrition/public health 39, other science 1 (healthcare emissions).

**Study types** (grouped from the more specific CSV labels):

| Group | Count |
|---|---:|
| Animal / in-vitro | 6 |
| Randomized trial / crossover | 6 |
| Cohort / other observational / case-control | 16 |
| Survey / surveillance | 4 |
| Systematic review / meta-analysis | 2 |
| Model / time series / environmental analysis | 6 |

**Topics** (broad reporting categories; distinct narrow questions within a category):

| Topic | Count |
|---|---:|
| ageing and cognition | 4 |
| ageing and metabolism | 2 |
| air pollution | 2 |
| alcohol and health | 1 |
| climate and heat | 3 |
| common medicines | 4 |
| diet and nutrition | 8 |
| exercise | 3 |
| healthcare emissions | 1 |
| infections | 2 |
| mental health | 2 |
| mental health policy | 1 |
| mental health services | 1 |
| pain | 1 |
| screen time | 1 |
| sleep | 1 |
| sleep and exercise | 1 |
| smoking | 1 |
| social connection | 1 |

## Coverage checks

| Check | Count | Result | IDs used for targeted checks |
|---|---:|---|---|
| Animal or in-vitro ≥ 5 | 6 | Met | SRC-002, SRC-005, SRC-006, SRC-007, SRC-008, SRC-009 |
| Range or relative-risk number ≥ 5 | 9 | Met | SRC-013, SRC-015, SRC-019, SRC-023, SRC-029, SRC-034, SRC-036, SRC-039, SRC-040 |
| Explicitly hedged finding ≥ 5 | 6 | Met | SRC-005, SRC-008, SRC-014, SRC-025, SRC-027, SRC-033 |
| Published before 2024-11-02 ≥ 4 | 12 | Met | SRC-001, SRC-003, SRC-004, SRC-011, SRC-012, SRC-025, SRC-035, SRC-036, SRC-037, SRC-038, SRC-039, SRC-040 |
| Tier A + B ≥ 24 | 32 | Met | — |
| Health / medicine / nutrition / public health ≥ 32 | 39 | Met | — |

The numeric coverage check counts quoted risk ratios, relative probabilities, or reported ranges/confidence intervals. The hedge check counts substantive qualifiers such as “may,” “points to,” “potential,” and “suggest.”

## Rights evidence by site

- **NIH:** Its [FAQ](https://www.nih.gov/about-nih/frequently-asked-questions) says most site information is public domain and notes exceptions for third-party images. One cached article had no detected third-party credit (A); eight credited Shutterstock or Adobe (C, internal only). The article images are outside this text-only candidate set.
- **PLOS Medicine:** Each paper page includes an article-level CC BY or CC0 statement. Examples: [CC BY article](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004613) and [CC0 article](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004435).
- **PLOS Biology:** The [brown-fat mouse paper](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3003534) states its article-level CC BY terms. Exact evidence URLs and short rights quotes appear in the CSV.

## Suggested held-out shortlist (20; team approval required)

These cover government text, CC BY/CC0 papers, animal work, quantified associations, trials, surveillance, modeling, and meta-analysis. Tier C entries are internal-only.

- **[SRC-002](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3003534) — Tier B:** CC BY mouse experiment; retains a clear nonhuman population and feeding condition.
- **[SRC-003](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004395) — Tier B:** CC BY cohort; separates particulate components and pregnancy outcomes.
- **[SRC-004](https://www.nih.gov/news-events/nih-research-matters/lower-sodium-could-reduce-blood-pressure-most-people) — Tier A:** Tier A crossover diet trial; includes a 75% figure, comparator, and blood-pressure change.
- **[SRC-005](https://www.nih.gov/news-events/nih-research-matters/sleep-exercise-may-reduce-mutation-driven-inflammation) — Tier C:** Tier C internal-only source; human-and-mouse evidence with an explicit “may” hedge.
- **[SRC-007](https://www.nih.gov/news-events/nih-research-matters/weakened-gut-brain-connection-may-contribute-memory-loss) — Tier C:** Tier C internal-only mouse experiment; aging, gut changes, and memory provide distinct slots.
- **[SRC-009](https://www.nih.gov/news-events/nih-research-matters/glp-1-drug-slows-aging-mice) — Tier C:** Tier C internal-only animal study; older female mice prevent an easy scope error.
- **[SRC-013](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004613) — Tier B:** CC BY observational study; exposure increment and several disease-specific ranges.
- **[SRC-015](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004561) — Tier B:** CC BY pooled cohort; low-intensity smoking and hazard ratios supply quantified associations.
- **[SRC-016](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004737) — Tier B:** CC0 model; screen-use projections test attribution to a simulation rather than observed cases.
- **[SRC-018](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004633) — Tier B:** CC BY cohort; links a diet measure with diabetes incidence and emissions.
- **[SRC-019](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004731) — Tier B:** CC BY cohort; contrasts absolute fall-risk ranges for people with and without dementia.
- **[SRC-023](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004577) — Tier B:** CC BY cohort; a five-year, 20% probability difference after an exercise program.
- **[SRC-025](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004358) — Tier B:** CC BY policy model; explicit conditional effect and uncertainty about employment.
- **[SRC-026](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004632) — Tier B:** CC BY pilot RCT; telehealth is compared with clinic care for hypertension control.
- **[SRC-027](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004735) — Tier B:** CC BY case-control model; under-five population, exposure window, and uncertainty interval.
- **[SRC-031](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004682) — Tier B:** CC BY surveillance; 2023 bed rate and geographic difference.
- **[SRC-033](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004435) — Tier B:** CC0 trial follow-up; explicitly hedged null cognitive finding.
- **[SRC-035](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004463) — Tier B:** CC BY time-series study; policy phase and measured food purchases.
- **[SRC-038](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004460) — Tier B:** CC BY refugee RCT; app and usual-care groups differ on distress and functioning.
- **[SRC-040](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1000316) — Tier B:** CC BY meta-analysis; 148 studies and an odds ratio on social relationships.

## Limitations

- Tier C NIH pages credit third-party images; their full-page rights are unclear. Do not use them in a public demo without a separate rights review.
- The study links were taken from DOI text on the source page. They were recorded for provenance but the linked studies were not separately checked in this run.
- Broad topic counts do not prove narrow-topic diversity; the team should review that during source approval. Several PLOS findings are model estimates or observational associations, as marked in the CSV.
- Exploratory fetches were not consistently spaced one second apart; the candidate-page batches were paced at roughly one request per second per domain. The exact total request count was not logged. No account, key, archive, paywall, CAPTCHA, or social-platform page was used.

## Addendum — 2026-11-02 (LT decision D-009, edited by Claude)

These edits were made after the Codex run. All other content above is unchanged.

- **NIH re-tiering.** SRC-005 to SRC-012 changed from Tier C to **Tier A**, with `demo_ok=yes`, for **text-only use**.
  - The NIH FAQ restriction applies to third-party **images**.
  - The FAQ states: "Most of the information on our site is in the public domain and can be used without charge or restriction."
  - Never reuse page images.
- **New tier totals:** A 9, B 31, C 0.
- **Self-referencing study links.** For the 31 CC papers, `study_link` pointed to the paper's own DOI. Those rows now read `study_link=self`, `study_link_basis=self`. Only the 9 NIH pages link to a separate underlying study.
- **Imbalance.** 31/40 candidates are research papers (30 from PLOS Medicine), while R1 showed most real hop-1 pages are news-style. A supplement run (`prompts/source_candidates_agent.md` v1.1) will add ~15 plain-language US government pages before the held-out split is chosen.
- **Logging.** Claude's independent re-check found 0 problems: every quote verbatim in the cache, all statuses 200, human columns empty, no excluded topics. The run did not log a request count, and some exploratory fetches were spaced under 1 s.
