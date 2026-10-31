"""Apply a documented semantic review to the CX run using cached source text."""

from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path

from enrich import ROOT, report
from verify import verify_file


CLAIMS = {
    "CX-003": "Trump has taken more control of federal spending than any president in modern history by freezing funds Congress approved and imposing tariffs on his own",
    "CX-004": 'Republicans liked the exact same workplace diversity training more when it skipped buzzwords like "diversity" and "privilege" and used plain words like "differences" and "unfair advantages" instead.',
    "CX-005": "A fungus resistant to all 4 types of antifungal drugs has been found in a hospital patient in Kenya, only the 2nd case ever recorded worldwide after New York in 2022.",
    "CX-007": "1 in 3 American boys aged 13 to 17 follows Andrew Tate at least a little, and those who do are more likely to believe men should hide their emotions, be dominant and reject anything feminine.",
    "CX-008": "Scientists have confirmed that silver diamine fluoride, an inexpensive liquid can stop tooth decay in seconds without drilling or anesthesia, potentially transforming cavity treatment for millions.",
    "CX-009": "Researchers posing as patients called 5,822 in-network mental health providers: most calls hit voicemails, over half the listings were wrong, and just 24% of real calls ended with an appointment.",
    "CX-010": "Research shows permanent standard time is the preferred choice for health, as it preserves morning light and aligns with human circadian biology.",
    "CX-011": "Creatine, the cheap gym supplement, protected the brain from gut inflammation in rats with chronic colitis.",
    "CX-021": "95% of Americans don't get our recommended amount of fiber",
    "CX-027": "Google Gemini 4 Argon shatters 59-year-old nuclear fusion conjecture in just a few hours",
}

# Literal passages, selected by reading the cached page. Every value is checked
# again by verify.py, including quote length and source identity.
HOP_QUOTES = {
    "CX-005": "We report phenotypic and genomic features of a PDR C. auris isolate from Kenya, the second globally.",
    "CX-009": "A successful call (meaning someone picked up the phone) resulted in an appointment with the health care provider only 24% of the time.",
    "CX-013": "Even with aggressive treatment, 60 to 70 percent of patients have historically died.",
    "CX-016": "Patients who got the experimental vaccine, along with the approved drug Keytruda, had a 42% lower risk of their cancer coming back after surgery or of dying than if they got Keytruda alone",
    "CX-017": "Younger patients sometimes had more aggressive, treatment-resistant forms of colon cancer.",
    "CX-019": "The new study provides a possible mechanism for this, showing that plastic-water interfaces can perturb proteins, cell membranes, and more.",
    "CX-021": "an estimated 95% of American adults and children do not consume recommended amounts of fiber.",
    "CX-023": "Marine populations in the deep waters of the Gulf of Mexico plummeted by roughly 60 percent in the years following the 2010 Deepwater Horizon explosion, with little evidence of recovery",
    "CX-025": "In our tests, sandbags provided less effective protection against leakage through tested doorways compared to the tape-based sealing methods.",
    "CX-027": "Google’s Gemini 4 Argon has helped researchers extend mathematical solutions to a problem involving magnetic fields inside experimental fusion reactors, building on research that challenged a longstanding scientific conjecture.",
    "CX-029": "Analysis of English, US and Dutch cancer data by World Cancer Research Fund identified “significant increases” in early onset cancers for seven cancer types in England, five types in the US and four in the Netherlands.",
}

PRIMARY_QUOTES = {
    "CX-001": "In this large US cohort of over 2.5 million children, we found no association between the first MMR vaccination administered before 24 months of age and the subsequent diagnosis of childhood autism.",
    "CX-005": HOP_QUOTES["CX-005"],
    "CX-018": "These findings support further studies to assess semaglutide's potential in preventing AD.",
}

FINDING = {
    "CX-001": "yes", "CX-003": "partial", "CX-004": "yes", "CX-005": "yes",
    "CX-007": "partial", "CX-009": "partial", "CX-010": "yes", "CX-011": "yes",
    "CX-012": "yes", "CX-013": "partial", "CX-016": "yes", "CX-017": "yes",
    "CX-018": "partial", "CX-019": "yes", "CX-021": "yes", "CX-022": "yes",
    "CX-023": "yes", "CX-024": "yes", "CX-025": "yes", "CX-026": "partial",
    "CX-029": "yes",
}

NOT_PRIMARY = {"CX-013", "CX-019", "CX-024", "CX-025"}


def main() -> None:
    output = ROOT / "data/r1/r1_CX.csv"
    seeds = ROOT / "data/r1/seeds_CX.csv"
    with output.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        rows = list(reader)
    for row in rows:
        item = row["item_id"]
        cache = ROOT / "data/r1/cache" / item
        if item == "CX-001":
            shutil.copyfile(cache / "doi_probe.txt", cache / "primary.txt")
            row["primary_url"] = "https://www.ovid.com/jnls/pidj/fulltext/10.1097/inf.0000000000005349~association-between-first-mmr-vaccination-before-age-2-years"
            row["primary_access"] = "open"
            row["primary_text_origin"] = "fulltext_html"
            row["model_notes"] = "The DOI resolved to readable publisher full text."
        if item in CLAIMS:
            assert CLAIMS[item] in row["post_text"], item
            row["main_claim_quote"] = CLAIMS[item]
        for mapping, prefix in ((HOP_QUOTES, "hop1"), (PRIMARY_QUOTES, "primary")):
            if item in mapping:
                quote = mapping[item]
                assert len(quote.split()) <= 40, item
                assert quote in (cache / f"{prefix}.txt").read_text(encoding="utf-8"), item
                row[f"{prefix}_finding_quote"] = quote
        if item in NOT_PRIMARY:
            for key in ("primary_url", "primary_doi", "primary_resolved_via", "primary_text_origin", "primary_date", "primary_date_type", "primary_finding_quote"):
                row[key] = ""
            row["primary_access"] = "not_found"
            row["primary_link_basis"] = "none"
            row["model_notes"] = "The observed candidate was not the study behind this report. Primary source unresolved."
        if item in ("CX-007", "CX-011"):
            row["primary_access"] = "not_found"
            row["primary_text_origin"] = ""
            row["model_notes"] = "The DOI publisher disallowed fetching in robots.txt." if item == "CX-007" else "The DOI landing page returned redirect-only text. Primary source unresolved."
        if item == "CX-018":
            row["model_notes"] = "The DOI publisher blocked access; a Crossref abstract was available."
        if item in ("CX-007", "CX-011", "CX-018"):
            # The DOI was observed, but its destination did not return an HTTP
            # status. Keep the DOI string, not an unvisited primary URL.
            row["primary_url"] = ""
        if item == "CX-027":
            row["model_notes"] = "The article says Gemini extended existing solutions; it attributes the earlier contradiction of the conjecture to a different project."
        if item == "CX-014":
            row["hop1_access"] = "paywalled"
            row["model_notes"] = "Hop-1 returned HTTP 402 Payment Required."
        finding = FINDING.get(item, "no")
        if row["hop1_access"] == "open":
            row["hop1_contains_finding"] = finding if item != "CX-018" else "partial"
        row["source_found_within_2_hops"] = "yes" if item in FINDING else "no"
        row["relevance_confidence"] = "high" if finding == "yes" and row["hop1_finding_quote"] else "low"
        row["row_status"] = "ok" if item in FINDING else "partial"
        row["model_impression"] = "unsure"
        if item == "CX-027":
            row["model_impression"] = "distorted"
            row["model_candidate_types"] = "fact_contradicted"
        if item in ("CX-003", "CX-007", "CX-009", "CX-013", "CX-018", "CX-021", "CX-026"):
            row["relevance_confidence"] = "low"
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    verify_file(seeds, output, ROOT / "data/r1/cache")
    with output.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    old = (ROOT / "data/r1/report_CX.md").read_text(encoding="utf-8")
    import re
    runtime = float(re.search(r"(?:initial automated pass )?runtime: ([\d.]+) s", old).group(1))
    requests = sum(
        isinstance(json.loads(line)["status"], int)
        for row in rows
        for line in (ROOT / "data/r1/cache" / row["item_id"] / "fetch_log.jsonl").read_text(encoding="utf-8").splitlines()
    )
    (ROOT / "data/r1/report_CX.md").write_text(report(rows, requests, runtime, seeds), encoding="utf-8")


if __name__ == "__main__":
    main()
