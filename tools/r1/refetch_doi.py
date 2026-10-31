"""Probe observed DOI links after fixing canonical robots-file redirects."""

import csv
import os

from enrich import Fetcher, ROOT


def main() -> None:
    email = os.environ["R1_CONTACT_EMAIL"]
    with (ROOT / "data/r1/r1_CX.csv").open(newline="", encoding="utf-8") as f:
        rows = {r["item_id"]: r for r in csv.DictReader(f)}
    for item in ("CX-001", "CX-007", "CX-011", "CX-018"):
        doi = rows[item]["primary_doi"]
        fetcher = Fetcher(ROOT / "data/r1/cache" / item, email, append_log=True)
        final, _, status, access = fetcher.fetch("https://doi.org/" + doi, "doi_probe")
        print(item, final, status, access, fetcher.count, flush=True)


if __name__ == "__main__":
    main()
