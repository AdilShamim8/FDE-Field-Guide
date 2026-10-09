"""Offline regression checks; legacy fixtures are not a production quality estimate."""

import argparse
import json
import math
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.engine.agent import TriageAgent
from src.models.schemas import DefectCategory, RoutingDecision, SeverityLevel, TicketIngestRequest


def wilson_interval(successes, total):
    """Descriptive 95% Wilson interval; nonrandom fixtures do not support inference."""
    if not total:
        return None
    z = 1.959963984540054
    p = successes / total
    denominator = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denominator
    radius = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    return [max(0.0, center - radius), min(1.0, center + radius)]


def evaluate_cases(cases, agent=None):
    if not isinstance(cases, list) or not cases:
        raise ValueError("Evaluation requires a nonempty case list")
    agent = agent or TriageAgent()
    ids = set()
    results = []
    latencies = []
    category_correct = severity_correct = routing_correct = 0
    grounded = citation_total = document_correct = document_total = 0
    empty_dispatches = 0
    failures = []
    for case in cases:
        if case["id"] in ids:
            raise ValueError("Duplicate evaluation case ID")
        ids.add(case["id"])
        DefectCategory(case["expected_category"])
        SeverityLevel(case["expected_severity"])
        RoutingDecision(case["expected_routing"])
        request = TicketIngestRequest(ticket_id=case["ticket_id"], account_id=case["account_id"], raw_text=case["raw_text"])
        start = time.perf_counter()
        # Full corpus access here is a local benchmark setting, not an authenticated role.
        result = agent.process_ticket(request, user_roles=["admin"])
        latencies.append((time.perf_counter() - start) * 1000)
        cat_ok = result.category.value == case["expected_category"]
        sev_ok = result.severity.value == case["expected_severity"]
        route_ok = result.routing_decision.value == case["expected_routing"]
        category_correct += cat_ok
        severity_correct += sev_ok
        routing_correct += route_ok
        verified = [c for c in result.citations if c.is_verified and agent.index.verify_quote(
            c.document_id, c.verbatim_quote, section=c.section
        )]
        citation_total += len(result.citations)
        grounded += len(verified)
        expected_doc = case.get("expected_citation_doc")
        doc_ok = True
        if expected_doc:
            document_total += 1
            doc_ok = any(c.document_id == expected_doc for c in verified)
            document_correct += doc_ok
        empty_dispatch = result.routing_decision == RoutingDecision.AUTOMATED_DISPATCH and not verified
        empty_dispatches += empty_dispatch
        if not (cat_ok and sev_ok and route_ok and doc_ok) or len(verified) != len(result.citations) or empty_dispatch:
            failures.append({"id": case["id"], "category": cat_ok, "severity": sev_ok,
                             "routing": route_ok, "required_document": doc_ok,
                             "empty_dispatch": empty_dispatch})
        results.append((case["expected_category"], result.category.value))

    total = len(cases)
    per_class = {}
    for category in DefectCategory:
        name = category.value
        tp = sum(expected == predicted == name for expected, predicted in results)
        fp = sum(predicted == name and expected != name for expected, predicted in results)
        fn = sum(expected == name and predicted != name for expected, predicted in results)
        precision = tp / (tp + fp) if tp + fp else None
        recall = tp / (tp + fn) if tp + fn else None
        f1 = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else None
        per_class[name] = {"support": tp + fn, "precision": precision, "recall": recall, "f1": f1}
    supported_f1 = [v["f1"] for v in per_class.values() if v["support"] > 0]
    ordered = sorted(latencies)
    p95 = ordered[max(0, math.ceil(0.95 * total) - 1)]
    grounding_rate = grounded / citation_total if citation_total else None
    passed = (category_correct / total >= 0.88 and severity_correct / total >= 0.90
              and routing_correct == total and document_total > 0 and document_correct == document_total
              and citation_total > 0 and grounded == citation_total and empty_dispatches == 0 and p95 < 200)
    return {
        "scope": "known regression fixtures; not an independent customer holdout or production SLA",
        "cases": total, "category_correct": category_correct, "severity_correct": severity_correct,
        "routing_correct": routing_correct, "citations_verified": grounded, "citations_evaluated": citation_total,
        "grounding_rate": grounding_rate, "required_documents_correct": document_correct,
        "required_documents_evaluated": document_total, "empty_automated_dispatches": empty_dispatches,
        "per_class": per_class, "macro_f1_supported_classes": sum(supported_f1) / len(supported_f1),
        "category_accuracy_wilson_95_descriptive": wilson_interval(category_correct, total),
        "interval_limit": "Known nonrandom fixtures cannot estimate deployment or worldwide accuracy.",
        "engine_cpu_p95_ms": p95, "latency_scope": "single-process local engine timing, excluding HTTP and external dependencies",
        "evidence_statuses": sorted({c.get("evidence_status", "unspecified") for c in cases}),
        "failures": failures, "passed": passed,
    }


def run_evaluation(dataset_path=None, agent=None, report_path=None):
    path = Path(dataset_path) if dataset_path else PROJECT_ROOT / "evals/golden_dataset.json"
    cases = json.loads(path.read_text(encoding="utf-8"))
    report = evaluate_cases(cases, agent=agent)
    output = json.dumps(report, indent=2)
    print(output)
    if report_path:
        Path(report_path).write_text(output + "\n", encoding="utf-8")
    print("RESULT: REGRESSION CHECKS PASSED." if report["passed"] else "RESULT: REGRESSION CHECKS FAILED.")
    return report["passed"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        success = run_evaluation(args.dataset, report_path=args.report)
    except (KeyError, ValueError, OSError) as error:
        print(f"Evaluation failed: {error}", file=sys.stderr)
        success = False
    sys.exit(0 if success else 1)
