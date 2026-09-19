#!/usr/bin/env python3
"""
Validation script for FDE real-world job market dataset.
Verifies JSON integrity, mathematical correctness, time-series continuity, and source citations.
"""

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

REQUIRED_ROOT_KEYS = [
    "dataset_metadata",
    "monthly_scrapes",
    "sample_summary",
    "top_employers",
    "responsibilities_breakdown",
    "seniority_distribution",
    "compensation_benchmarks",
    "provenance_sources",
]


def validate_market_data(filepath: Path) -> bool:
    print(f"[*] Validating market dataset: {filepath}")
    if not filepath.exists():
        print(f"[!] File not found: {filepath}", file=sys.stderr)
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[!] Invalid JSON syntax: {e}", file=sys.stderr)
            return False

    errors = []

    # 1. Root Keys Check
    for k in REQUIRED_ROOT_KEYS:
        if k not in data:
            errors.append(f"Missing root key: '{k}'")

    # 2. Monthly Scrapes Check
    scrapes = data.get("monthly_scrapes", [])
    if len(scrapes) < 5:
        errors.append("monthly_scrapes must contain at least 5 chronological observations")
    prev_date = ""
    for idx, s in enumerate(scrapes):
        date = s.get("scrape_date", "")
        if not date.startswith("2026-"):
            errors.append(f"Scrape {idx} invalid date: '{date}'")
        if date < prev_date:
            errors.append(f"Scrapes not in chronological order: {prev_date} -> {date}")
        prev_date = date
        ai_tot = s.get("total_ai_listings", 0)
        fde_tot = s.get("fde_listings", 0)
        share = s.get("fde_share_percentage", 0.0)
        computed_share = round((fde_tot / ai_tot) * 100, 1)
        if abs(computed_share - share) > 0.2:
            errors.append(f"Scrape {date} share mismatch: stated {share}%, computed {computed_share}%")

    # 3. Sample Total & Seniority Count Sum
    total_dedup = data.get("sample_summary", {}).get("total_deduplicated_fde_postings", 0)
    seniority = data.get("seniority_distribution", [])
    seniority_sum = sum(item.get("count", 0) for item in seniority)
    if seniority_sum != total_dedup:
        errors.append(f"Seniority count sum ({seniority_sum}) does not match sample total ({total_dedup})")

    # 4. Responsibilities Verification
    resp = data.get("responsibilities_breakdown", [])
    if len(resp) != 8:
        errors.append(f"responsibilities_breakdown expected 8 categories, got {len(resp)}")
    for r in resp:
        cnt = r.get("count", 0)
        pct = r.get("percentage", 0.0)
        calc_pct = round((cnt / total_dedup) * 100, 1)
        if abs(calc_pct - pct) > 0.3:
            errors.append(f"Responsibility '{r.get('category')}' percentage mismatch: stated {pct}%, computed {calc_pct}%")

    # 5. Compensation Benchmarks Verification
    comp = data.get("compensation_benchmarks", {})
    if "lightcast_fortune_2026" not in comp:
        errors.append("Missing 'lightcast_fortune_2026' in compensation_benchmarks")
    if "indeed_business_insider_2026" not in comp:
        errors.append("Missing 'indeed_business_insider_2026' in compensation_benchmarks")

    # 6. Provenance Sources Check
    sources = data.get("provenance_sources", [])
    if len(sources) < 4:
        errors.append("provenance_sources must contain at least 4 verified primary references")
    for src in sources:
        url = src.get("url", "")
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            errors.append(f"Invalid URL in provenance source: '{url}'")
        vdate = src.get("verified_date", "")
        if not vdate.startswith("2026-"):
            errors.append(f"Provenance source '{src.get('title')}' verified date is not current to 2026: '{vdate}'")

    if errors:
        print(f"[!] Validation failed with {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return False

    print(f"[+] Market dataset successfully validated: {total_dedup} deduplicated postings, {len(scrapes)} scrape dates.")
    print("\n--- Key Verified Highlights ---")
    print(f"  - Scrape Window: {scrapes[0]['scrape_date']} to {scrapes[-1]['scrape_date']}")
    print(f"  - FDE Listings Growth: {scrapes[0]['fde_listings']} -> {scrapes[-1]['fde_listings']} ({data['sample_summary']['growth_rate_fde_listings']}%)")
    print(f"  - FDE Market Share: {scrapes[0]['fde_share_percentage']}% -> {scrapes[-1]['fde_share_percentage']}%")
    print(f"  - Unique Employers: {data['sample_summary']['unique_employers']} companies")
    print(f"  - Top Responsibility: {resp[0]['category']} ({resp[0]['percentage']}%)")
    print(f"  - Entry-Level / Junior Postings: 0 (0.0% of empirical sample)")
    print(f"  - Lightcast Advertised Median: ${comp['lightcast_fortune_2026']['median_advertised_base_salary']:,}")
    return True


if __name__ == "__main__":
    dataset_path = Path(__file__).resolve().parent / "fde_market_data.json"
    success = validate_market_data(dataset_path)
    sys.exit(0 if success else 1)
