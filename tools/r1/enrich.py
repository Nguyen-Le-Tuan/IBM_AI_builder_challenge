"""Enrich R1 seed posts from their non-social source links, without creating labels."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import re
import statistics
import time
from collections import Counter
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from urllib.parse import quote, urljoin, urlparse
from urllib.robotparser import RobotFileParser

import httpx
import trafilatura
from bs4 import BeautifulSoup

from verify import normalize, verify_file

ROOT = Path(__file__).resolve().parents[2]
SOCIAL = {
    "reddit.com", "redd.it", "x.com", "twitter.com", "t.co", "facebook.com",
    "fb.com", "instagram.com", "threads.net", "tiktok.com", "bsky.app",
}
FORBIDDEN = {"web.archive.org", "archive.ph", "archive.is"}
SCHOLARLY = (
    "doi.org", "pubmed.ncbi.nlm.nih.gov", "pmc.ncbi.nlm.nih.gov", "arxiv.org",
    "biorxiv.org", "medrxiv.org", "nature.com/articles/", "plos.org/article",
    "frontiersin.org/journals/", "sciencedirect.com/science/article",
    "springer.com/article", "link.springer.com/article", "onlinelibrary.wiley.com/doi/",
)
STOP = set("a an and are as at be but by can for from had has have in into is it of on or our that the their these this to was were what who with within".split())
DOI = re.compile(r"10\.\d{4,9}/[^\s<>\"'&?#]+", re.I)


def host(url: str) -> str:
    return (urlparse(url).hostname or "").lower().removeprefix("www.")


def prohibited(url: str) -> bool:
    h = host(url)
    return h in FORBIDDEN or any(h == d or h.endswith("." + d) for d in SOCIAL)


def words(s: str) -> list[str]:
    return [w for w in re.findall(r"[\w']+", s.lower()) if len(w) > 2 and w not in STOP]


def quote_passage(text: str, claim: str) -> tuple[str, float]:
    """Pick one short contiguous passage by shared non-stop words."""
    tokens = set(words(claim))
    if not text or not tokens:
        return "", 0.0
    candidates = re.split(r"(?<=[.!?])\s+|\n+", text)
    ranked = []
    for sentence in candidates:
        sentence = sentence.strip()
        if len(sentence) < 25:
            continue
        overlap = len(tokens & set(words(sentence)))
        ranked.append((overlap, sentence))
    if not ranked:
        return "", 0.0
    overlap, sentence = max(ranked, key=lambda x: x[0])
    if overlap < 2:
        return "", overlap / max(1, len(tokens))
    parts = sentence.split()
    if len(parts) > 40:
        positions = [i for i, p in enumerate(parts) if words(p) and words(p)[0] in tokens]
        start = max(0, min(positions or [0]) - 5)
        start = min(start, len(parts) - 40)
        sentence = " ".join(parts[start:start + 40])
    return sentence, overlap / max(1, len(tokens))


class Fetcher:
    """Bounded HTTP fetcher with per-domain robots checks and request logs."""

    last_request: dict[str, float] = {}

    def __init__(self, cache: Path, email: str, append_log: bool = False):
        self.cache = cache
        self.cache.mkdir(parents=True, exist_ok=True)
        self.log_path = cache / "fetch_log.jsonl"
        if not append_log:
            self.log_path.write_text("", encoding="utf-8")
        self.count = 0
        self.robots: dict[str, RobotFileParser | None] = {}
        self.client = httpx.Client(
            follow_redirects=False,
            timeout=20,
            headers={"User-Agent": f"IBM-AIBC-R1-research/0.1 (+mailto:{email})"},
        )

    def _record(self, url: str, status: str | int, kind: str) -> None:
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"url": url, "status": status, "kind": kind}, ensure_ascii=False) + "\n")

    def _get(self, url: str, kind: str) -> httpx.Response | None:
        if self.count >= 12 or prohibited(url):
            self._record(url, "prohibited_or_budget", kind)
            return None
        h = host(url)
        elapsed = time.monotonic() - self.last_request.get(h, 0)
        if elapsed < 1:
            time.sleep(1 - elapsed)
        try:
            response = self.client.get(url)
            self.last_request[h] = time.monotonic()
            self.count += 1
            self._record(url, response.status_code, kind)
            return response
        except (httpx.HTTPError, ValueError) as e:
            self.last_request[h] = time.monotonic()
            self.count += 1
            self._record(url, type(e).__name__, kind)
            return None

    def allowed(self, url: str) -> bool:
        h = host(url)
        if prohibited(url) or not h:
            self._record(url, "prohibited", "target")
            return False
        if h not in self.robots:
            # Preserve `www`: many sites redirect the bare host's robots file.
            parsed = urlparse(url)
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
            response = None
            for _ in range(6):
                response = self._get(robots_url, "robots")
                if response is None or response.status_code not in (301, 302, 303, 307, 308):
                    break
                robots_url = urljoin(robots_url, response.headers.get("location", ""))
                if prohibited(robots_url):
                    response = None
                    break
            if response is None or response.status_code in (401, 403, 429):
                self.robots[h] = None
            elif response.status_code == 404:
                parser = RobotFileParser()
                parser.parse([])
                self.robots[h] = parser
            elif response.status_code == 200:
                parser = RobotFileParser()
                parser.parse(response.text.splitlines())
                self.robots[h] = parser
            else:
                self.robots[h] = None
        parser = self.robots[h]
        if parser is None:
            self._record(url, "robots_unavailable", "target")
            return False
        if not parser.can_fetch(self.client.headers["User-Agent"], url):
            self._record(url, "robots_disallow", "target")
            return False
        return True

    def fetch(self, url: str, stem: str) -> tuple[str, str, int | None, str]:
        """Return final URL, HTML, status, and access class."""
        current = url
        for _ in range(6):
            if not self.allowed(current):
                return current, "", None, "blocked"
            response = None
            for attempt in range(3):
                response = self._get(current, "page")
                if response is None or response.status_code >= 500:
                    if attempt < 2:
                        time.sleep(2 ** attempt)
                        continue
                break
            if response is None:
                return current, "", None, "broken"
            if response.status_code in (301, 302, 303, 307, 308):
                location = response.headers.get("location", "")
                if not location:
                    return current, "", response.status_code, "broken"
                next_url = urljoin(current, location)
                if prohibited(next_url):
                    self._record(next_url, "social_redirect", "target")
                    return current, "", response.status_code, "blocked"
                current = next_url
                continue
            status = response.status_code
            if status == 402:
                return current, "", status, "paywalled"
            if status in (401, 403, 429):
                return current, "", status, "blocked"
            if status in (404, 410) or status >= 500:
                return current, "", status, "broken"
            html = response.text
            if re.search(r"captcha|blocked by network security|verify you are human", html[:4000], re.I):
                raise RuntimeError(f"Bot-check signal at {current}; stop the current task without retrying")
            (self.cache / f"{stem}.html").write_text(html, encoding="utf-8")
            extracted = trafilatura.extract(html, url=current, include_links=False) or ""
            if not extracted:
                soup = BeautifulSoup(html, "lxml")
                for node in soup(["script", "style", "nav", "footer"]):
                    node.decompose()
                extracted = soup.get_text(" ", strip=True)
            (self.cache / f"{stem}.txt").write_text(extracted, encoding="utf-8")
            if len(extracted.split()) >= 150:
                return current, html, status, "open"
            if re.search(r"subscribe to continue|already a subscriber|sign in to read|subscription required", html, re.I):
                return current, html, status, "paywalled"
            return current, html, status, "open"
        return current, "", None, "broken"


def kind(url: str, html: str) -> str:
    h = host(url)
    if prohibited(url):
        return "social_post"
    if h in ("eurekalert.org", "newswise.com") or h.startswith("news.") or "press release" in html[:3000].lower():
        return "press_release"
    if "arxiv.org" in h or "biorxiv.org" in h or "medrxiv.org" in h:
        return "preprint"
    if "youtube.com" in h or "youtu.be" in h:
        return "video"
    if any(s in url for s in SCHOLARLY) or "citation_doi" in html.lower():
        return "paper"
    return "news_article"


def primary_candidate(html: str, final_url: str) -> tuple[str, str, str]:
    """Return observed candidate URL, DOI, and basis, never inferred from title."""
    soup = BeautifulSoup(html, "lxml")
    meta = soup.find("meta", attrs={"name": re.compile(r"^citation_doi$", re.I)})
    doi = (meta.get("content") if meta else "") or ""
    if not doi:
        for a in soup.find_all("a", href=True):
            href = urljoin(final_url, a["href"])
            if host(href) == "doi.org":
                m = DOI.search(href)
                if m:
                    doi = unescape(m.group(0)).rstrip(".,;)")
                    break
    if doi and DOI.fullmatch(doi):
        return "https://doi.org/" + doi, doi, "doi"
    for a in soup.find_all("a", href=True):
        href = urljoin(final_url, a["href"])
        context = (a.get_text(" ", strip=True) + " " + (a.parent.get_text(" ", strip=True) if a.parent else ""))[:300].lower()
        if any(s in href for s in SCHOLARLY) and not prohibited(href) and re.search(r"study|journal|research|paper|published|pubmed|abstract", context):
            return href, "", "hyperlink"
    return "", "", "none"


def crossref_date_and_abstract(fetcher: Fetcher, doi: str) -> tuple[str, str, str]:
    if not doi:
        return "", "", ""
    url = "https://api.crossref.org/works/" + quote(doi, safe="") + "?mailto=" + quote(EMAIL)
    final, html, status, access = fetcher.fetch(url, "crossref")
    if not html or status != 200:
        return "", "", ""
    try:
        message = json.loads(html)["message"]
    except (ValueError, KeyError):
        return "", "", ""
    dates = []
    for label, typ in (("published-online", "online"), ("published-print", "print"), ("issued", "issued")):
        parts = (message.get(label) or {}).get("date-parts", [[]])[0]
        if parts:
            dates.append((tuple(parts + [1] * (3 - len(parts))), "-".join(str(x).zfill(2) if i else str(x) for i, x in enumerate(parts)), typ))
    dates.sort()
    abstract = BeautifulSoup(message.get("abstract", ""), "lxml").get_text(" ", strip=True)
    if abstract:
        (fetcher.cache / "crossref.txt").write_text(abstract, encoding="utf-8")
    return (dates[0][1], dates[0][2], abstract) if dates else ("", "", abstract)


def enrich(seed: dict[str, str], columns: list[str], email: str) -> tuple[dict[str, str], int]:
    start = time.monotonic()
    row = {c: seed.get(c, "") for c in columns}
    row.update(agent_name="codex/gpt-6", agent_run_at=datetime.now(timezone.utc).isoformat(), relevance_confidence="low",
               model_impression="unsure", row_status="partial", source_found_within_2_hops="no", primary_link_basis="none",
               primary_access="not_found", hop1_contains_finding="n/a")
    fetcher = Fetcher(ROOT / "data/r1/cache" / seed["item_id"], email)
    if not all(seed.get(k) for k in ("item_id", "collector", "platform", "post_text")):
        row["row_status"] = "seed_invalid"
        row["agent_seconds"] = f"{time.monotonic() - start:.2f}"
        return row, fetcher.count
    claim = seed["post_text"].split("\n", 1)[0].strip()
    row["main_claim_quote"] = claim
    link = seed.get("linked_url", "").strip()
    if not link:
        m = re.search(r"https?://\S+", seed["post_text"])
        link = m.group(0) if m and not prohibited(m.group(0)) else ""
    row["has_link"] = "yes" if link else "no"
    if not link:
        row["hop1_access"] = "n/a"
        row["model_notes"] = "No external source link was present in the seed."
    elif prohibited(link):
        row.update(linked_kind="social_post", hop1_access="n/a", model_notes="The seed link points to a social platform; it was not fetched.")
    else:
        final, html, status, access = fetcher.fetch(link, "hop1")
        row.update(linked_final_url=final, linked_kind=kind(final, html),
                   hop1_http_status=str(status or ""), hop1_access=access)
        text = (fetcher.cache / "hop1.txt").read_text(encoding="utf-8") if (fetcher.cache / "hop1.txt").exists() else ""
        hop_quote, score = quote_passage(text, claim)
        if hop_quote and access == "open":
            row.update(hop1_finding_quote=hop_quote, hop1_contains_finding="yes" if score >= .35 else "partial")
        elif access == "open":
            row["hop1_contains_finding"] = "no"
        candidate, doi, basis = primary_candidate(html, final) if html else ("", "", "none")
        if row["linked_kind"] in ("paper", "abstract", "preprint") and access == "open":
            candidate, doi, basis = final, doi, "hyperlink"
        row.update(primary_doi=doi, primary_link_basis=basis)
        primary_text = ""
        if candidate:
            if candidate == final:
                primary_final, paccess = final, access
                primary_text = text
                (fetcher.cache / "primary.txt").write_text(text, encoding="utf-8")
            else:
                primary_final, phtml, _, paccess = fetcher.fetch(candidate, "primary")
                primary_text = (fetcher.cache / "primary.txt").read_text(encoding="utf-8") if (fetcher.cache / "primary.txt").exists() else ""
            row["primary_url"] = primary_final
            row["primary_access"] = "open" if paccess == "open" and len(primary_text.split()) >= 150 else "paywalled"
            row["primary_text_origin"] = "fulltext_html" if row["primary_access"] == "open" else ""
        date, date_type, abstract = crossref_date_and_abstract(fetcher, doi) if doi else ("", "", "")
        row.update(primary_date=date, primary_date_type=date_type)
        if abstract and (not primary_text or row["primary_access"] != "open"):
            primary_text = abstract
            (fetcher.cache / "primary.txt").write_text(abstract, encoding="utf-8")
            row.update(primary_access="abstract_only", primary_text_origin="abstract_crossref")
        primary_quote, primary_score = quote_passage(primary_text, claim)
        if primary_quote:
            row["primary_finding_quote"] = primary_quote
        row["source_found_within_2_hops"] = "yes" if (hop_quote and score >= .35) or (primary_quote and primary_score >= .35) else "no"
        row["relevance_confidence"] = "high" if row["source_found_within_2_hops"] == "yes" and max(score, primary_score) >= .5 else "low"
        if primary_quote and primary_score >= .5:
            row["model_impression"] = "faithful" if normalize(claim) == normalize(primary_quote) else "unsure"
        row["row_status"] = "ok" if row["source_found_within_2_hops"] == "yes" else "partial"
        if access in ("blocked", "broken", "paywalled"):
            row["model_notes"] = f"Hop-1 access was {access}."
        elif row["primary_access"] == "abstract_only":
            row["model_notes"] = "Only the primary abstract was accessible."
        elif not candidate:
            row["model_notes"] = "No observed link to a primary source was found."
    row["agent_seconds"] = f"{time.monotonic() - start:.2f}"
    return row, fetcher.count


def report(rows: list[dict[str, str]], requests: int, runtime: float, seed_path: Path) -> str:
    n = len(rows)
    yes = lambda field, value: sum(r[field] == value for r in rows)
    pct = lambda a, b: f"{a}/{b} ({a / b:.1%})" if b else f"{a}/{b} (n/a)"
    linked = yes("has_link", "yes")
    hop_bad = sum(r["hop1_access"] in ("paywalled", "broken", "blocked") for r in rows if r["has_link"] == "yes")
    access = sum(r["primary_access"] in ("open", "abstract_only") for r in rows)
    auto = sum(r["primary_link_basis"] in ("hyperlink", "doi") for r in rows)
    attention = [r["item_id"] for r in rows if r["row_status"] != "ok" or r["relevance_confidence"] == "low" or r["primary_resolved_via"] == "crossref_search" or r["verification"] != "pass"]
    audit = [r["item_id"] for r in rows if r["audit_selected"] == "yes"]
    return "\n".join([
        "# R1 enrichment report — CX", "",
        f"- Agent: codex/gpt-6; run date: 2026-10-31; seed: `{seed_path}`.",
        f"- Rows: {n}; HTTP requests including robots.txt: {requests}; initial automated pass runtime: {runtime:.1f} s. Total time including DOI follow-up and semantic review was not recorded.",
        f"- **R1 source found within 2 hops:** {pct(yes('source_found_within_2_hops', 'yes'), n)}.",
        f"- Has link: {pct(linked, n)}.",
        f"- Among linked posts, hop-1 blocked/broken/paywalled: {pct(hop_bad, linked)}.",
        f"- Observed hyperlink or DOI to primary: {pct(auto, n)}.",
        f"- Primary open or abstract-only: {pct(access, n)}.",
        f"- Human impression (not a label): {dict(Counter(r['human_impression'] or 'blank' for r in rows))}; n={n}.",
        f"- Model impression (not a label): {dict(Counter(r['model_impression'] for r in rows))}; n={n}.",
        f"- Human seed time: not recorded; median agent seconds: {statistics.median(float(r['agent_seconds']) for r in rows):.2f} s; n={n}.",
        f"- Image/video-only exclusions: 0 among 78 listing positions; see `seeds_CX_skips.md`.",
        "", "## Rows needing human attention", "",
        ", ".join(attention) if attention else "None.",
        "", "## Audit sample", "",
        ", ".join(audit), "",
        "## Limitations", "",
        "- The sample used a signed-in Reddit account with explicit human permission, not the planned logged-out condition.",
        "- Passages were mechanically checked against cached text and semantically reviewed by the agent. The R1 metric is provisional until the human audit.",
        "- Per-row `agent_seconds` measures automated fetching and extraction; it excludes the later semantic review time.",
        "- Bot-check signals appeared on CX-015 and CX-020. The initial script marked them blocked but continued; this missed the Phase 0 stop rule. No check was solved or retried. Treat T4 as partial and review the rows before reuse.",
        "- No Crossref title search was used; primary sources without observed links or DOIs remain unresolved.",
        "- HTTP blocks, robots disallows, and short pages may lower the source-found rate.",
        "",
    ])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", required=True, type=Path)
    args = parser.parse_args()
    global EMAIL
    EMAIL = os.environ.get("R1_CONTACT_EMAIL", "")
    if not EMAIL:
        raise SystemExit("R1_CONTACT_EMAIL is required")
    start = time.monotonic()
    with args.seeds.open(newline="", encoding="utf-8") as f:
        seeds = list(csv.DictReader(f))
    with (ROOT / "data/r1/r1_template.csv").open(newline="", encoding="utf-8") as f:
        columns = next(csv.reader(f))
    if not seeds or list(seeds[0]) != columns[:12]:
        raise SystemExit("Seed file missing or malformed")
    rows = []
    requests = 0
    for seed in seeds:
        row, count = enrich(seed, columns, EMAIL)
        requests += count
        rows.append(row)
        print(seed["item_id"], row["hop1_access"], row["source_found_within_2_hops"], flush=True)
    rng = random.Random(sum(ord(c) for c in "CX"))
    selected = set(rng.sample([r["item_id"] for r in rows], max(3, math.ceil(.2 * len(rows)))))
    for row in rows:
        row["audit_selected"] = "yes" if row["item_id"] in selected else "no"
    output = ROOT / "data/r1/r1_CX.csv"
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    verify_file(args.seeds, output, ROOT / "data/r1/cache")
    with output.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    (ROOT / "data/r1/report_CX.md").write_text(report(rows, requests, time.monotonic() - start, args.seeds), encoding="utf-8")
    print(f"wrote {output}; requests={requests}; seconds={time.monotonic()-start:.1f}", flush=True)


if __name__ == "__main__":
    main()
