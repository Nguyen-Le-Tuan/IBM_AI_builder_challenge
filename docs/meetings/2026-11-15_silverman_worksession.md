# Work session — Sunday, Nov 15, 2026 — Silverman Library

**Who:** Le Tuan, Lok Sang, Truyen Anh, Brian (in person).
**Status:** `RECOMMENDED` (drafted by Claude on 2026-11-12). The team may change any block.
**Where:** Oscar A. Silverman Library, second and third floors of Capen Hall, North Campus.
**Proposed time:** 12:00–18:30, provisional; the team will confirm it. Silverman is open 24 hours every day this fall, and Nov 15 is not among the listed exceptions ([Silverman hours page](https://cms.lib.buffalo.edu/use/hours/silverman.html), read 2026-11-12).

## Goal of the day

Leave with a **walking skeleton**: on our fixture page, select a post, click Check, and see highlights painted from a backend response. Everything the team must decide together is decided and recorded.

## Done when (exit checklist)

- [ ] All Block 1 decisions are rows in Journal §2.
- [ ] `BOB_LOG.md` exists with at least one entry, including the Bobcoin cost of one task.
- [ ] `backend/` and `extension/` skeletons are committed, with `.env.example` and no secrets.
- [ ] One fixture post shows highlights from a backend response. A `MOCK` response is a pass; real pipeline output on one dev post is the stretch.
- [ ] At least 12 held-out posts are written (3 writers × 2 sources × 2 posts).
- [ ] Every member has named tasks with dates through Nov 19, and the next meeting is set.

## Before Sunday

**Today (Thu Nov 12) — room.** Group study rooms can be reserved up to 3 days ahead, one reservation per person per day, 2 hours at most ([policy](https://library.buffalo.edu/about/policies/use-security/study-rooms.html)). We need to talk, so a quiet floor will not work.

- [ ] Each member books one 2-hour slot in the same room, back to back (12–2, 2–4, 4–6), under "Group Study Rooms (Silverman)" at [booking.lib.buffalo.edu](https://booking.lib.buffalo.edu/reserve/silverman). Whether the system accepts back-to-back bookings by different people is not verified.

**Everyone, by Saturday night:**

- [ ] `git pull`; read Journal §0–§2 and the §15 entry of 2026-11-12. Brian also reads §5, §8–§11 and `README.md`.
- [ ] IBM Bob installed, trial active, signed in. Write down your Bobcoin balance.
- [ ] Registered on the Event Platform and joined the team. SkillsBuild certificate saved as a PDF.
- [ ] A recent Python 3, Node LTS, Chrome and git installed.
- [ ] Bring a charger. One person brings a power strip.

**Le Tuan:**

- [ ] Review and commit the Journal change of Nov 12.
- [ ] At home, run `ollama pull granite3-guardian:2b` and `ollama pull granite4:micro` (the second is 2.1 GB). Library Wi-Fi may be slow.
- [ ] Have one working LLM API key in a local `.env`. Never commit it.
- [ ] Check what the watsonx.ai account actually gives (the free tier is listed as 300k or 50k tokens per month, see `docs/research/services.md`).

**Writers (Le Tuan, Lok Sang, Truyen Anh):**

- [ ] Read `data/heldout/README.md` and open two of your assigned sources in `data/heldout/assignments.csv`.

**Brian:**

- [ ] Read `docs/labeling_guideline_v0.md`. Do not open anyone's `posts_*.csv` or `findings_*.csv`: you may be the blind labeler.

## Roles for the day

| Role | Job | Who |
|---|---|---|
| Timekeeper | Ends each block on time | TBD |
| Scribe | Writes decisions into Journal §2 as they are made | TBD |
| Bob driver | Shares the screen in Block 2; starts the screen recording | TBD |

## Schedule

| Time | Block | Output |
|---|---|---|
| 12:00–12:15 | 0. Setup and roll call | The roll-call table below is filled |
| 12:15–13:15 | 1. Decisions | Rows in Journal §2 |
| 13:15–14:00 | 2. Bob kickoff, together on one screen | Skeleton plan, frozen contract, first `BOB_LOG.md` entry |
| 14:00–14:20 | Break | |
| 14:20–16:20 | 3. Parallel build | Tracks A, B, C below |
| 16:20–16:50 | 4. Integration | Fixture post highlighted from the backend |
| 16:50–17:35 | 5. Held-out writing sprint | At least 12 posts |
| 17:35–18:00 | 6. Wrap-up | Commits, Journal §15 entry, tasks through Nov 19 |
| 18:00–18:30 | Buffer | |

If the day runs late, shorten Block 5 first. Do not shorten Blocks 3 and 4.

### Block 0 — Roll call (15 min)

| | Registered + in team | Certificate PDF | Eligibility checked | Bob trial active | Bobcoins |
|---|---|---|---|---|---|
| Le Tuan | | | | | |
| Lok Sang | | | | | |
| Truyen Anh | | | | | |
| Brian | | | | | |

Update `HUMAN_TODO.md` from this table.

### Block 1 — Decisions (60 min)

Each item has a timebox and a suggested default from Claude. A default is a suggestion, not a decision.

| # | Min | Decision | Suggested default |
|---|---|---|---|
| 1 | 15 | Scope re-assessment and limitations review (both in Journal §15, 2026-11-12): yes, no or later for each of the 7 additions, 4 cuts and 3 mitigations | Yes to additions 1–3 and 6–7; 4–5 if time allows; yes to all cuts; yes to all three mitigations |
| 2 | 10 | Workstream owners (A backend, B extension, C data/eval/pitch) and weekly hours | The split in "Proposed way of working" below. Brian stays out of pipeline code and prompts until blind labeling is done, so the person who backs up A is the C owner, not Brian |
| 3 | 10 | D-008: where hop 1 is fetched | Backend fetch for the MVP. A blocked page shows Slate. Reading the open article tab is a stretch goal |
| 4 | 10 | LLM provider and a budget ceiling in dollars | The provider we already hold a key for, plus Granite Guardian 2b locally as the second check |
| 5 | 5 | Held-out freeze date and minimum size; Brian's role | Freeze Nov 17 with at least 20 posts. Brian writes no posts; Brian is the blind labeler and baseline scorer |
| 6 | 10 | Guideline §11 open questions | Keep v0 unchanged until R2; agree only a one-line rule for when a number change is material |

### Block 2 — Bob kickoff (45 min)

- [ ] Start the screen recording and note the Bobcoin balance.
- [ ] In Plan mode, give Bob Journal §9 (architecture) and §10 (data contract) and ask for a repo skeleton plan.
- [ ] Review the plan together, then run it in Agent mode.
- [ ] **Freeze the contract:** save the §10 example as a `MOCK` fixture that both tracks build against.
- [ ] Note the Bobcoin balance again and write the first `BOB_LOG.md` entry (Journal §12.3).

### Block 3 — Parallel build (120 min)

All product code is written with Bob and logged in `BOB_LOG.md`.

**Track A — backend**

- [ ] FastAPI app with Pydantic schemas from the contract.
- [ ] `POST /checks` and `GET /checks/{id}` return the `MOCK` fixture.
- [ ] Verbatim-quote validator with tests.
- [ ] Stretch: a CLI that runs `extract_claims` and `compare` on one dev post.

**Track B — extension**

- [ ] MV3 + TypeScript skeleton that loads in Chrome.
- [ ] Fixture feed page with three placeholder posts, marked `MOCK`.
- [ ] Select text → floating Check button → service worker → backend.
- [ ] Paint highlights with the CSS Custom Highlight API from the response.
- [ ] Stretch: a minimal hover card.

**Track C — data and demo (no product code)**

- [ ] From the `dev` rows of `data/sources/source_candidates.csv`, shortlist 6–8 demo sources. At least two need an open-access study for the "lost at which hop" scene.
- [ ] List candidate real pages for the "works anywhere" moment. Only real, existing discrepancies count.
- [ ] Draft the project-page outline against the rules §5 checklist in `HUMAN_TODO.md`.

### Block 4 — Integration (30 min)

- [ ] The extension calls the local backend and paints the returned spans on a fixture post.
- [ ] Each track shows its result to the others.
- [ ] Write down what broke; these become Monday's first tasks.

### Block 5 — Held-out writing sprint (45 min)

- [ ] Le Tuan, Lok Sang and Truyen Anh each write 2 sources × 2 posts, by hand, with **no AI tools** (D-006).
- [ ] Brian works apart from the writers and does not see the posts. Brian continues Track C.
- [ ] Writers save to their own `posts_*.csv` and `findings_*.csv`.

### Block 6 — Wrap-up (25 min)

- [ ] Each member reviews and commits their own work. No secrets, no post text in product code.
- [ ] The scribe adds a §15 entry to the Journal and confirms the §2 rows.
- [ ] Update `HUMAN_TODO.md` with owners and dates through Nov 19.
- [ ] Set the next meeting.

## Proposed way of working (`RECOMMENDED`, for decision 2)

Drafted by Claude on 2026-11-13. Claude knows only Le Tuan's strengths (Python, ML), so rows 2 and 3 may swap. Nothing here is decided until it is a row in Journal §2.

**Owners**

| Member | Main job | Owns |
|---|---|---|
| Le Tuan | A — backend and pipeline; integration of both ends | `backend/` |
| Lok Sang or Truyen Anh (whoever knows web/TypeScript better) | B — extension, hover card, fixture feed | `extension/` |
| The other of the two | C — dataset, demo sources, held-out coordination, project page | `data/`, `docs/` |
| Brian | Blind evaluation (held-out labels, baseline scoring), then video and slides | evaluation files, submission materials |

**Rules**

1. **Contract first.** The Journal §10 example is saved as a `MOCK` fixture in Block 2. Backend and extension both build against it, so neither waits for the other.
2. **One owner per directory.** Only the owner commits there. Others ask the owner or open a pull request. With four people writing code, use short branches and a pull request with one reviewer instead of committing straight to `main`.
3. **Each member drives Bob in their own area** and writes their own `BOB_LOG.md` entries. Bobcoins are per account; measure the cost of one task on Sunday.
4. **Journal conflicts.** `git pull` before editing, add new entries only at the end of §15, and one scribe writes §2 during a meeting.
5. **Held-out wall.** The three writers use no AI tools and do not show posts to Brian. Brian does not open `posts_*.csv` or `findings_*.csv`.

**Rhythm**

- **Daily:** each member posts three lines in the team chat: done yesterday, doing today, blocked on.
- **Integration days:** Nov 16 (CLI turns a post + URL into JSON with verified quotes) and Nov 19 (extension shows real pipeline output on the fixture feed). The A and B owners work together on those days; online is fine.
- **Fallback:** workstream A has one person and the whole demo depends on it. If the Nov 16 milestone is missed, the C owner moves to A (tests and validators) and dataset work pauses.

## Rules to keep in mind

- Product code comes from Bob and is logged; anything written outside Bob is noted honestly in `BOB_LOG.md`.
- Mock data is labeled `MOCK`.
- API keys stay in a gitignored backend `.env`.
- Held-out posts and gold labels are human-only.
