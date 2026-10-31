"""Mechanically verify cached R1 quotes, URLs, enums, and unchanged seed cells."""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path


ENUMS = {
    "has_link": {"yes", "no"}, "claim_in_image": {"yes", "no"},
    "linked_kind": {"", "news_article", "press_release", "paper", "abstract", "preprint", "video", "social_post", "other"},
    "hop1_access": {"", "open", "paywalled", "broken", "blocked", "n/a"},
    "hop1_contains_finding": {"", "yes", "partial", "no", "n/a"},
    "primary_link_basis": {"", "hyperlink", "doi", "named_only", "none"},
    "primary_resolved_via": {"", "crossref_search"},
    "primary_access": {"", "open", "abstract_only", "paywalled", "not_found", "n/a"},
    "primary_text_origin": {"", "fulltext_html", "abstract_crossref", "abstract_pubmed", "abstract_openalex_reconstructed", "abstract_landing_page", "press_release"},
    "primary_date_type": {"", "online", "print", "issued"},
    "source_found_within_2_hops": {"yes", "no"},
    "relevance_confidence": {"high", "low"},
    "model_impression": {"faithful", "distorted", "unsure"},
    "row_status": {"ok", "partial", "seed_invalid", "error"},
    "audit_selected": {"yes", "no"},
}


def normalize(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = s.translate(str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", "–": "-", "—": "-", "\u00a0": " "}))
    return re.sub(r"\s+", " ", s).strip()


def verify_file(seed_path: Path, output: Path, cache_root: Path) -> None:
    """Rewrite verification fields and clear quotes that fail cached-text checks."""
    with seed_path.open(newline="", encoding="utf-8") as f:
        seeds = {r["item_id"]: r for r in csv.DictReader(f)}
    with output.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        rows = list(reader)
    if set(seeds) != {r["item_id"] for r in rows} or len(seeds) != len(rows):
        raise ValueError("Output item IDs do not match seeds one-to-one")
    seed_columns = list(next(iter(seeds.values())))
    for row in rows:
        problems = []
        seed = seeds[row["item_id"]]
        if any(row[k] != seed[k] for k in seed_columns):
            problems.append("seed_cells_changed")
        if row["main_claim_quote"] and row["main_claim_quote"] not in row["post_text"]:
            problems.append("main_claim_not_verbatim")
        for key, allowed in ENUMS.items():
            if row[key] not in allowed:
                problems.append(f"bad_enum:{key}")
        cache = cache_root / row["item_id"]
        log = [json.loads(line) for line in (cache / "fetch_log.jsonl").read_text(encoding="utf-8").splitlines()]
        logged = {entry["url"] for entry in log if isinstance(entry["status"], int)}
        for key in ("linked_final_url", "primary_url"):
            if row[key] and row[key] not in logged:
                problems.append(f"url_not_logged:{key}")
        for prefix, stem in (("hop1", "hop1"), ("primary", "primary")):
            quote = row[f"{prefix}_finding_quote"]
            text_path = cache / f"{stem}.txt"
            valid = bool(quote and text_path.exists() and normalize(quote) in normalize(text_path.read_text(encoding="utf-8")))
            row[f"{prefix}_quote_verified"] = "true" if valid else ("false" if quote else "")
            if quote and not valid:
                row[f"{prefix}_finding_quote"] = ""
                row["row_status"] = "partial"
                problems.append(f"{prefix}_quote_not_cached")
        if row["source_found_within_2_hops"] == "yes" and not (row["hop1_quote_verified"] == "true" or row["primary_quote_verified"] == "true"):
            row["source_found_within_2_hops"] = "no"
            row["row_status"] = "partial"
            problems.append("source_found_without_quote")
        row["verification"] = "pass" if not problems else "fail:" + ";".join(problems)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--cache", required=True, type=Path)
    args = parser.parse_args()
    verify_file(args.seeds, args.output, args.cache)
