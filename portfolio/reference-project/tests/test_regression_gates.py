"""Adversarial regression inputs test code contracts, not real-world accuracy."""

import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from evals.run_evals import evaluate_cases
from src.config import settings
from src.engine.agent import TriageAgent
from src.models.schemas import RoutingDecision, TicketIngestRequest
from src.pipeline.ingestion import HybridKnowledgeIndex

CASES = json.loads((PROJECT_ROOT / "evals/golden_dataset.json").read_text())[:2]


class MutatedAgent(TriageAgent):
    def __init__(self, mutate):
        super().__init__()
        self.mutate = mutate

    def process_ticket(self, *args, **kwargs):
        return self.mutate(super().process_ticket(*args, **kwargs))


def test_current_regression_cases_pass():
    report = evaluate_cases(CASES)
    assert report["passed"]
    assert report["required_documents_correct"] == 2


def test_routing_error_fails_acceptance():
    agent = MutatedAgent(lambda r: r.model_copy(update={"routing_decision": RoutingDecision.HUMAN_REVIEW_REQUIRED}))
    report = evaluate_cases(CASES, agent)
    assert report["category_correct"] == report["severity_correct"] == 2
    assert report["routing_correct"] == 0
    assert not report["passed"]


def test_zero_citations_cannot_receive_perfect_grounding():
    report = evaluate_cases(CASES, MutatedAgent(lambda r: r.model_copy(update={"citations": []})))
    assert report["grounding_rate"] is None
    assert report["empty_automated_dispatches"] == 1
    assert not report["passed"]


def test_forged_verification_flag_does_not_authenticate_quote():
    def forge(result):
        result.citations = [c.model_copy(update={"verbatim_quote": "This fabricated policy is not in the source.", "is_verified": True}) for c in result.citations]
        return result
    report = evaluate_cases(CASES, MutatedAgent(forge))
    assert report["citations_verified"] == 0
    assert not report["passed"]


def test_wrong_required_document_fails_even_with_valid_quotes():
    cases = [dict(CASES[1], expected_citation_doc="APEX-COMPLIANCE-DOC")]
    report = evaluate_cases(cases)
    assert report["grounding_rate"] == 1
    assert report["required_documents_correct"] == 0
    assert not report["passed"]


@pytest.mark.parametrize("cases", [[], [CASES[0], CASES[0]]])
def test_empty_and_duplicate_evaluations_rejected(cases):
    with pytest.raises(ValueError):
        evaluate_cases(cases)


def request(text):
    return TicketIngestRequest(ticket_id="BOUNDARY", account_id="ACC", raw_text=text)


def test_strict_grounding_requires_evidence(monkeypatch):
    monkeypatch.setattr(settings, "strict_grounding_refusal", True)
    result = TriageAgent(index=HybridKnowledgeIndex([])).process_ticket(request("Requesting credit for invoice"))
    assert result.citations == []
    assert result.routing_decision == RoutingDecision.HUMAN_REVIEW_REQUIRED


def test_p0_escalates_even_when_evidence_is_unavailable():
    result = TriageAgent(index=HybridKnowledgeIndex([])).process_ticket(request("Total outage on production payment service"))
    assert result.routing_decision == RoutingDecision.ESCALATED_P0


def test_unrelated_input_does_not_gain_dispatch_confidence():
    result = TriageAgent().process_ticket(request("Orbital spectroscopy measurements of distant nebulae"))
    assert result.confidence < settings.confidence_threshold
    assert result.routing_decision == RoutingDecision.HUMAN_REVIEW_REQUIRED
    assert result.repair_attempts == 0


def test_quote_must_match_exact_text_and_cited_section():
    index = HybridKnowledgeIndex()
    chunk = index.chunks[0]
    quote = chunk.content.split(". ")[1]
    assert index.verify_quote(chunk.document_id, quote, section=chunk.section)
    assert not index.verify_quote(chunk.document_id, quote.upper(), section=chunk.section)
    assert not index.verify_quote(chunk.document_id, quote, section="wrong section")
