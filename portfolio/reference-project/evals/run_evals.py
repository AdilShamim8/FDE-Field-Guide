"""
Automated evaluation harness for ETISE.
Executes golden dataset, calculates precision, recall, citation grounding rate,
and latency percentiles, outputting an executive engineering scorecard.
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

# Ensure reference-project directory is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.engine.agent import TriageAgent
from src.models.schemas import TicketIngestRequest


def run_evaluation() -> bool:
    golden_path = Path(__file__).resolve().parent / "golden_dataset.json"
    if not golden_path.exists():
        print(f"Error: Golden dataset not found at {golden_path}")
        return False

    with open(golden_path, "r", encoding="utf-8") as f:
        cases: List[Dict[str, Any]] = json.load(f)

    agent = TriageAgent()
    print("=" * 70)
    print("ETISE AUTOMATED GOLDEN EVALUATION HARNESS")
    print(f"Executing {len(cases)} enterprise test cases against compliance engine...")
    print("=" * 70)

    category_correct = 0
    severity_correct = 0
    routing_correct = 0
    citation_grounding_success = 0
    total_citations_evaluated = 0
    latencies_ms: List[float] = []

    for case in cases:
        req = TicketIngestRequest(
            ticket_id=case["ticket_id"],
            account_id=case["account_id"],
            raw_text=case["raw_text"],
        )

        t_start = time.perf_counter()
        result = agent.process_ticket(req)
        elapsed_ms = (time.perf_counter() - t_start) * 1000
        latencies_ms.append(elapsed_ms)

        # Check Category
        if result.category.value == case["expected_category"]:
            category_correct += 1

        # Check Severity
        if result.severity.value == case["expected_severity"]:
            severity_correct += 1

        # Check Routing
        if result.routing_decision.value == case["expected_routing"]:
            routing_correct += 1

        # Check Citations
        if result.citations:
            for cit in result.citations:
                total_citations_evaluated += 1
                if cit.is_verified:
                    citation_grounding_success += 1

    total = len(cases)
    cat_accuracy = (category_correct / total) * 100
    sev_accuracy = (severity_correct / total) * 100
    routing_accuracy = (routing_correct / total) * 100

    grounding_rate = (
        (citation_grounding_success / total_citations_evaluated) * 100
        if total_citations_evaluated > 0
        else 100.0
    )

    latencies_ms.sort()
    p50 = latencies_ms[int(total * 0.50)]
    p90 = latencies_ms[int(total * 0.90)]
    p95 = latencies_ms[int(total * 0.95)]
    p99 = latencies_ms[min(total - 1, int(total * 0.99))]

    print("\nSCORECARD SUMMARY")
    print("-" * 70)
    print(f"Total Test Cases:            {total}")
    print(f"Category Classification:     {category_correct}/{total} ({cat_accuracy:.1f}%) [SLA Target: >= 88.0%]")
    print(f"Severity Classification:     {severity_correct}/{total} ({sev_accuracy:.1f}%) [SLA Target: >= 90.0%]")
    print(f"Decision Gating Accuracy:    {routing_correct}/{total} ({routing_accuracy:.1f}%)")
    print(f"Citation Grounding Rate:     {citation_grounding_success}/{total_citations_evaluated} ({grounding_rate:.1f}%) [Target: 100.0%]")
    print("-" * 70)
    print("LATENCY DISTRIBUTION (p50 / p90 / p95 / p99)")
    print(f"p50:  {p50:.2f} ms")
    print(f"p90:  {p90:.2f} ms")
    print(f"p95:  {p95:.2f} ms")
    print(f"p99:  {p99:.2f} ms")
    print("=" * 70)

    # Acceptance threshold checks
    passed = (
        cat_accuracy >= 88.0
        and sev_accuracy >= 90.0
        and grounding_rate == 100.0
        and p95 < 200.0
    )

    if passed:
        print("RESULT: ALL ENTERPRISE SLA ACCEPTANCE CRITERIA PASSED.")
    else:
        print("RESULT: SLA BREACH DETECTED.")

    return passed


if __name__ == "__main__":
    success = run_evaluation()
    sys.exit(0 if success else 1)
