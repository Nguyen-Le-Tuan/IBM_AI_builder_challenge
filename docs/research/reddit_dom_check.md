# Reddit DOM check — 2026-10-31

**Conditions:** Observed in the user's signed-in Brave session, with explicit user permission. This differs from the logged-out condition in the Phase 0 prompt. All actions were read-only. T2 used five Reddit page loads: the r/science listing, a new Reddit link post, the same post on old Reddit, a new Reddit self post, and the r/nutrition listing.

**Link post inspected:** https://www.reddit.com/r/science/comments/1wxemcr/study_of_25_million_children_finds_no_link/

| Question | Observed result |
|---|---|
| `shreddit-post` present? | Yes, on the current Reddit post page and listing. |
| Attribute names | `permalink`, `content-href`, `created-timestamp`, `post-title`, `post-language`, `post-type`, `is-link-post`, `subreddit-prefixed-name`, `id`, plus state, count, and author attributes. Do not rely on author attributes for the adapter. |
| External link | `shreddit-post[content-href]`; this link post held `https://www.psypost.org/study-of-2-5-million-children-finds-no-link-between-mmr-vaccine-and-autism/`. |
| Title | `shreddit-post[post-title]`; the visible title is also in `[slot="title"]`. |
| Timestamp | `shreddit-post[created-timestamp]`; observed `2026-10-04T12:34:02.206000+0000`. |
| Permalink | `shreddit-post[permalink]`; observed `/r/science/comments/1wxemcr/study_of_25_million_children_finds_no_link/`. |
| Body text | This link post had no self-text body. On the inspected self post, `shreddit-post [slot="text-body"] #t3_1x36lob-post-rtjson-content` held the rendered body. A general selector is `shreddit-post [slot="text-body"] [id$="-post-rtjson-content"]`. |
| Truncation / read more | The self-post feed card used `shreddit-post-text-body[slot="text-body"][max-text-body-height="253"]` and CSS `overflow-hidden`; opening its permalink showed the full body. No explicit “Read more” control was observed for that post. Other layouts may differ. |
| `old.reddit.com` | The same link post had **no** `shreddit-post`. It used a `.thing.link` with `data-permalink`, `data-url`, `a.title`, and `time[datetime]`. An adapter would need a separate markup path. |

**Limits:** One link post and one self post are insufficient to establish DOM stability across Reddit views, responsive widths, deleted posts, or future deployments. The observations were made while signed in and may differ while logged out. No comments or usernames were saved.
