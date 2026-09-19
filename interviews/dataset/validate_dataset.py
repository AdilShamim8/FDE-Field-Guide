#!/usr/bin/env python3
"""
Validation script for FDE real-world interview dataset.
Ensures JSON integrity, schema conformance, ID uniqueness, and source citation completeness.
"""

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

REQUIRED_ROOT_KEYS = [
    "id",
    "stage",
    "question",
    "tested_at",
    "core_signal",
    "senior_response_playbook",
    "red_flag_response",
    "scoring_rubric",
    "primary_source",
]

REQUIRED_RUBRIC_KEYS = ["strong_hire", "hire", "no_hire"]
REQUIRED_SOURCE_KEYS = ["author", "title", "url", "verified_date"]

VALID_STAGES = [
    "Discovery & Decomposition",
    "Coding & Practical Integration",
    "System Design & Architecture",
    "LLM & Applied AI Engineering",
    "Customer Simulation & Role-play",
    "Live Debugging",
    "Behavioral & Ownership",
]


def validate_dataset(filepath: Path) -> bool:
    print(f"[*] Validating dataset: {filepath}")
    if not filepath.exists():
        print(f"[!] File not found: {filepath}", file=sys.stderr)
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[!] Invalid JSON: {e}", file=sys.stderr)
            return False

    if not isinstance(data, list):
        print("[!] Root structure must be a JSON list", file=sys.stderr)
        return False

    seen_ids = set()
    errors = []
    stages_count = {}
    sources_count = {}

    for idx, item in enumerate(data):
        item_id = item.get("id", f"INDEX_{idx}")

        # Check required root keys
        for k in REQUIRED_ROOT_KEYS:
            if k not in item or not item[k]:
                errors.append(f"[{item_id}] Missing or empty required key: '{k}'")

        # Check ID uniqueness and format
        if item.get("id"):
            if item["id"] in seen_ids:
                errors.append(f"[{item_id}] Duplicate question ID detected: '{item['id']}'")
            seen_ids.add(item["id"])
            if not item["id"].startswith("FDE-"):
                errors.append(f"[{item_id}] ID must start with prefix 'FDE-'")

        # Check Stage
        stage = item.get("stage")
        if stage:
            if stage not in VALID_STAGES:
                errors.append(f"[{item_id}] Invalid stage: '{stage}'. Allowed: {VALID_STAGES}")
            stages_count[stage] = stages_count.get(stage, 0) + 1

        # Check Rubric
        rubric = item.get("scoring_rubric")
        if isinstance(rubric, dict):
            for rk in REQUIRED_RUBRIC_KEYS:
                if rk not in rubric or not rubric[rk]:
                    errors.append(f"[{item_id}] scoring_rubric missing tier: '{rk}'")
        else:
            errors.append(f"[{item_id}] scoring_rubric must be a dictionary")

        # Check Primary Source & URL
        source = item.get("primary_source")
        if isinstance(source, dict):
            for sk in REQUIRED_SOURCE_KEYS:
                if sk not in source or not source[sk]:
                    errors.append(f"[{item_id}] primary_source missing key: '{sk}'")
            url = source.get("url", "")
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                errors.append(f"[{item_id}] Invalid citation URL format: '{url}'")
            author = source.get("author", "Unknown")
            sources_count[author] = sources_count.get(author, 0) + 1
        else:
            errors.append(f"[{item_id}] primary_source must be a dictionary")

    if errors:
        print(f"[!] Validation failed with {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return False

    print(f"[+] Dataset successfully validated: {len(data)} questions verified.")
    print("\n--- Breakdown by Interview Stage ---")
    for s, c in sorted(stages_count.items()):
        print(f"  - {s}: {c} question(s)")

    print("\n--- Breakdown by Verified Primary Source ---")
    for a, c in sorted(sources_count.items()):
        print(f"  - {a}: {c} citation(s)")

    return True


if __name__ == "__main__":
    dataset_path = Path(__file__).resolve().parent / "fde_interview_questions.json"
    success = validate_dataset(dataset_path)
    sys.exit(0 if success else 1)
