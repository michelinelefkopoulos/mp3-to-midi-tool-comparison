#!/usr/bin/env python3
"""Read-only structural checks for the dated comparison CSV. No network access."""
# SPDX-License-Identifier: CC0-1.0
import argparse
import csv
import datetime
import json
from pathlib import Path
from urllib.parse import urlparse

COLUMNS = (
    "google_organic_position", "result_kind", "domain", "page_title", "page_url",
    "supported_formats", "size_or_duration_limit", "processing_mode", "output_format",
    "account_requirement", "accuracy_or_quality", "pricing", "checked_at",
)
FEATURES = COLUMNS[5:12]


def inspect_csv(handle):
    """Validate structure only; never verify quotations or current search ranking."""
    reader = csv.DictReader(handle, skipinitialspace=True, strict=True)
    errors, positions, urls, dates = [], set(), set(), set()
    counts = {"converter": 0, "discussion": 0}
    if reader.fieldnames != list(COLUMNS):
        return {"valid": False, "errors": ["Unexpected or missing CSV columns."]}
    total = 0
    for number, row in enumerate(reader, 2):
        total += 1
        prefix = f"CSV row {number}: "
        if None in row or any(row.get(column) is None for column in COLUMNS):
            errors.append(prefix + "wrong number of fields.")
            continue
        if any(not row[column].strip() for column in COLUMNS):
            errors.append(prefix + "empty field; use not stated for unstated features.")
        try:
            position = int(row["google_organic_position"])
            if position < 1 or position in positions:
                raise ValueError
            positions.add(position)
        except ValueError:
            errors.append(prefix + "position must be a unique positive integer.")
        kind = row["result_kind"].strip()
        if kind not in counts:
            errors.append(prefix + "result_kind must be converter or discussion.")
        else:
            counts[kind] += 1
        url = row["page_url"].strip()
        parsed = urlparse(url)
        if parsed.scheme not in ("https", "http") or not parsed.hostname:
            errors.append(prefix + "page_url must be an absolute HTTP(S) URL.")
        elif parsed.hostname.removeprefix("www.") != row["domain"].strip().removeprefix("www."):
            errors.append(prefix + "domain does not match page_url.")
        if url in urls:
            errors.append(prefix + "duplicate page_url.")
        urls.add(url)
        try:
            value = row["checked_at"]
            if datetime.date.fromisoformat(value).isoformat() != value:
                raise ValueError
            dates.add(value)
        except ValueError:
            errors.append(prefix + "checked_at must be an ISO calendar date.")
        if kind == "discussion" and any(row[column].strip() != "not stated" for column in FEATURES):
            errors.append(prefix + "discussion feature cells must remain not stated.")
    if not total:
        errors.append("The CSV has no data rows.")
    return {"valid": not errors, "rows": total, "result_kinds": counts,
            "snapshot_dates": sorted(dates), "errors": errors,
            "checks": "local schema, row shape, identifiers, URL syntax and dates only",
            "quotes_verified": False, "current_search_rankings_verified": False,
            "source_pages_requested": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", nargs="?", type=Path,
                        default=Path(__file__).with_name("mp3-to-midi-tool-comparison.csv"))
    args = parser.parse_args()
    try:
        with args.csv_path.open(encoding="utf-8-sig", newline="") as handle:
            result = inspect_csv(handle)
    except (OSError, UnicodeError, csv.Error) as error:
        result = {"valid": False, "errors": [str(error)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
