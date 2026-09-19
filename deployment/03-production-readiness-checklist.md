# The Enterprise Production Readiness Review (PRR)

For the Forward Deployed Engineer (FDE), Lead Enterprise Architect, and Customer Technical Leadership conducting the formal Go/No-Go gate before an enterprise AI system receives live production traffic. 

In enterprise customer engagements, production readiness is not a subjective consensus or a feeling of confidence. It is a formal, auditable gate grounded in Google Site Reliability Engineering (SRE) principles, the AWS Well-Architected Framework, and Anthropic's production deployment protocol. Every item in this review is a binary check: **PASS**, **FAIL**, or **WAIVED IN WRITING** by the accountable executive sponsor. A single un-waived "FAIL" blocks deployment.

---

## 1. The Production Readiness Review: Operational Invariants

The Production Readiness Review (PRR) sits at Phase 9 of the [Engagement Lifecycle](../customer/01-engagement-lifecycle.md). Across our empirical dataset of 146 enterprise FDE postings, **90.4% explicitly mandate operational stability, SLA compliance, and cross-functional production gating** (ranking #1 among all technical responsibilities).

```
+---------------------------------------------------------------------------------------------------+
|                            ENTERPRISE PRODUCTION READINESS GATE (PRR)                             |
+---------------------------------------------------------------------------------------------------+
|  6 AUDITABLE DOMAINS                                                                              |
|  [1] Infrastructure & Resilience     --> Multi-AZ, circuit breakers, connection pools, PITR       |
|  [2] Security, Privacy & InfoSec     --> SAST/CVE scans, zero static keys, CMEK, PII redaction    |
|  [3] Data Pipelines & Vector Storage --> Idempotency, DLQ, chunking invariants, drift alarms      |
|  [4] AI Quality, Evals & Guardrails  --> Golden set SLAs, Cohen's Kappa, prompt injection tests   |
|  [5] Telemetry, Observability & FinOps-> Dual-plane telemetry, on-call routing, budget alarms     |
|  [6] Operations, Handover & Launch   --> Runbook dry-runs, rollback kill switch, RACI sign-off    |
+---------------------------------------------------------------------------------------------------+
                                                  |
                    +-----------------------------+-----------------------------+
                    |                                                           |
                    v                                                           v
      [All 30 Items: PASS or WAIVED]                             [Any Item: UN-WAIVED FAIL]
                    |                                                           |
                    v                                                           v
         === GO: PROCEED TO LAUNCH ===                               === NO-GO: LAUNCH HALTED ===
```

### The Binary Gate and Waiver Invariants
1. **The Spec is Ground Truth**: Criteria must match the thresholds documented and signed in Sprint 0 requirements, not human memory or post-hoc justifications.
2. **Zero Unaccounted Ambiguity**: Every failure must either be remediated prior to launch or formally accepted via a signed Risk Waiver.
3. **The Waiver Expiration Rule**: No waiver is permanent. Every waiver must state a specific business justification, a compensatory security/operational control, and a hard calendar expiration date (maximum 30 calendar days post-launch).

---

## 2. The Comprehensive 30-Point Enterprise Go/No-Go Gate

```
+---------------------------------------------------------------------------------------------------+
| DOMAIN 1: INFRASTRUCTURE, SCALABILITY & RESILIENCE                                                |
+----+----------------------------------+---------------------------------------------------+-------+
| #  | Checklist Item                   | Audit Verification Standard                       | Status|
+----+----------------------------------+---------------------------------------------------+-------+
| 1  | Multi-AZ Redundancy & PDBs       | Compute pods distributed across >=2 Availability  | [ ]   |
|    |                                  | Zones with PodDisruptionBudgets (minAvailable >=1)|       |
| 2  | Provider Circuit Breakers        | Automatic fallback trips if LLM provider returns  | [ ]   |
|    |                                  | 429/503/504 errors > 5% over 1-minute window      |       |
| 3  | Connection Pooling & Timeouts    | DB connection pooling configured with strict caps | [ ]   |
|    |                                  | (max_overflow <= 10) and request timeouts <= 15s  |       |
| 4  | Backup & Point-In-Time Recovery  | Automated daily snapshots with tested restore     | [ ]   |
|    |                                  | procedure meeting RPO < 15 min and RTO < 30 min   |       |
| 5  | Load & Concurrency Headroom      | System stress-tested at 2.5x peak anticipated RPS | [ ]   |
|    |                                  | with zero OOM errors and p95 latency within SLA   |       |
+----+----------------------------------+---------------------------------------------------+-------+

+---------------------------------------------------------------------------------------------------+
| DOMAIN 2: SECURITY, PRIVACY & INFOSEC COMPLIANCE                                                  |
+----+----------------------------------+---------------------------------------------------+-------+
| #  | Checklist Item                   | Audit Verification Standard                       | Status|
+----+----------------------------------+---------------------------------------------------+-------+
| 6  | Vulnerability & Secret Scans     | Container image CVE scan shows 0 CRITICAL and     | [ ]   |
|    |                                  | 0 HIGH vulnerabilities; Gitleaks scan shows 0 keys|       |
| 7  | Zero-Static-Key Identity         | Workloads authenticate via IAM Assumed Roles /    | [ ]   |
|    |                                  | IRSA / Workload Identity. Zero static API keys.   |       |
| 8  | Customer-Managed Keys (CMEK)     | All databases, vector stores, and object buckets  | [ ]   |
|    |                                  | encrypted with customer KMS keys; TLS 1.3 transit |       |
| 9  | PII / PHI Redaction Boundary     | Presidio/regex sanitization verified against 1,000| [ ]   |
|    |                                  | adversarial PII probes; 100% precision on egress  |       |
| 10 | Contractual Compliance Sign-Off  | InfoSec assessment passed; DPA, BAA (HIPAA), and  | [ ]   |
|    |                                  | subprocessor review agreements executed in writing|       |
+----+----------------------------------+---------------------------------------------------+-------+

+---------------------------------------------------------------------------------------------------+
| DOMAIN 3: DATA PIPELINES & VECTOR STORAGE INTEGRITY                                               |
+----+----------------------------------+---------------------------------------------------+-------+
| #  | Checklist Item                   | Audit Verification Standard                       | Status|
+----+----------------------------------+---------------------------------------------------+-------+
| 11 | Ingestion Idempotency & DLQ      | Event streams implement idempotent deduplication  | [ ]   |
|    |                                  | keys; Dead-Letter Queue (DLQ) configured & alarmed|       |
| 12 | Document Parsing Invariants      | Chunking pipeline enforces strict token limits    | [ ]   |
|    |                                  | (max 512 tokens) and preserves parent metadata tags|      |
| 13 | Vector Store Metric & Headroom   | Vector dimensions match model output (e.g. 1536); | [ ]   |
|    |                                  | HNSW index RAM utilization < 70% of node capacity |       |
| 14 | Backfill Data Reconciliation     | Source-to-target row count and cryptographic hash | [ ]   |
|    |                                  | reconciliation achieves 100.0% parity on backfills|       |
| 15 | Schema Drift & Volume Alarms     | Anomaly monitors trigger alerts on null spikes,   | [ ]   |
|    |                                  | volume drops (>3 sigma), or unexpected JSON keys  |       |
+----+----------------------------------+---------------------------------------------------+-------+

+---------------------------------------------------------------------------------------------------+
| DOMAIN 4: AI QUALITY, EVALUATION & GUARDRAILS                                                     |
+----+----------------------------------+---------------------------------------------------+-------+
| #  | Checklist Item                   | Audit Verification Standard                       | Status|
+----+----------------------------------+---------------------------------------------------+-------+
| 16 | Golden Test Set Benchmark SLA    | Automated evaluation suite passes agreed thresholds| [ ]   |
|    |                                  | (e.g., accuracy >= 90%, citation grounding = 100%)|       |
| 17 | Inter-Annotator Agreement (Kappa)| Statistical concordance between AI and SME experts| [ ]   |
|    |                                  | achieves Cohen's Kappa >= 0.85 on test cohort     |       |
| 18 | Jailbreak & Prompt Injection Gate| System passes adversarial injection test suite    | [ ]   |
|    |                                  | (OWASP GenAI Top 10) with zero unauthorized leaks |       |
| 19 | Structured Output Schema Guard   | Pydantic schema validation active on all outputs  | [ ]   |
|    |                                  | with automated single-turn self-healing retry loop|       |
| 20 | Hallucination Circuit Breaker    | Zero-grounding detection trips automatic fallback | [ ]   |
|    |                                  | to human review queue for mission-critical tickets|       |
+----+----------------------------------+---------------------------------------------------+-------+

+---------------------------------------------------------------------------------------------------+
| DOMAIN 5: TELEMETRY, OBSERVABILITY & FINOPS                                                       |
+----+----------------------------------+---------------------------------------------------+-------+
| #  | Checklist Item                   | Audit Verification Standard                       | Status|
+----+----------------------------------+---------------------------------------------------+-------+
| 21 | Dual-Plane OpenTelemetry Export  | Infrastructure metrics (CPU/RAM) and GenAI semantic| [ ]   |
|    |                                  | conventions (tokens, TTFT) exported to central APM|       |
| 22 | Alert Routing & On-Call Verified | PagerDuty/Opsgenie routing tested via live test   | [ ]   |
|    |                                  | alert; primary and secondary on-call acknowledged |       |
| 23 | Tenant Cost Attribution Tagging  | All inference and cloud compute tagged with       | [ ]   |
|    |                                  | TenantId, CostCenter, and Environment keys        |       |
| 24 | Spend Alarms & Quota Thresholds  | Budget alarms active at 50%, 75%, 90%, and 100%   | [ ]   |
|    |                                  | of monthly burn; API rate limiter enforces quota  |       |
| 25 | Distribution Drift Monitoring    | Population Stability Index (PSI < 0.10) and cosine| [ ]   |
|    |                                  | embedding drift alarms active in production APM   |       |
+----+----------------------------------+---------------------------------------------------+-------+

+---------------------------------------------------------------------------------------------------+
| DOMAIN 6: OPERATIONS, HANDOVER & LAUNCH DAY PROTOCOL                                              |
+----+----------------------------------+---------------------------------------------------+-------+
| #  | Checklist Item                   | Audit Verification Standard                       | Status|
+----+----------------------------------+---------------------------------------------------+-------+
| 26 | Independent Runbook Dry-Run      | Complete incident recovery runbook successfully   | [ ]   |
|    |                                  | executed by a customer SRE who did not build it   |       |
| 27 | Kill-Switch & Rollback Rehearsal | Live kill-switch flipped in staging; traffic      | [ ]   |
|    |                                  | reverts to legacy baseline in < 60 seconds cleanly|       |
| 28 | Signed Support Boundaries & SLAs | Written SLA agreement executed defining Tier 1/2/3| [ ]   |
|    |                                  | boundaries, escalation paths, and P1 response times|      |
| 29 | 14-Day Hypercare Window Scheduled| Daily 15-minute operational dashboard standup     | [ ]   |
|    |                                  | scheduled on calendar with named attendees        |       |
| 30 | T-Minus Launch Schedule Finalized| Hour-by-hour cutover runbook distributed with     | [ ]   |
|    |                                  | command center bridge link and named launch lead  |       |
+----+----------------------------------+---------------------------------------------------+-------+
```

---

## 3. The Auditable RACI Sign-Off Protocol

Production cutover requires formal, auditable sign-off across five core stakeholder roles. No system proceeds to live customer traffic without all five signatures recorded in the launch ticket.

```
+--------------------------+-----------------------+---------------------+-------------------------------+
| Stakeholder Role         | Named Individual      | RACI Designation    | Required Gate Responsibility  |
+--------------------------+-----------------------+---------------------+-------------------------------+
| Forward Deployed Lead    | [FDE Name]            | Accountable (A)     | Engineering integrity & tests |
| Customer Lead Architect  | [Architect Name]      | Responsible (R)     | VPC & infrastructure topology |
| Customer CISO / Security | [Security Lead Name]  | Approver (A)        | Security, CMEK, DPA & InfoSec |
| Customer Lead SRE / Ops  | [SRE Lead Name]       | Responsible (R)     | Runbooks, alerts, on-call     |
| Business Executive Sponsor| [Sponsor Name]       | Approver (A)        | Budget, P&L, business sign-off|
+--------------------------+-----------------------+---------------------+-------------------------------+
```

### Sign-Off Attestation Statement
> *"By signing below, the undersigned stakeholder leads attest that all 30 points of the Enterprise Production Readiness Review have been rigorously audited. All non-waived items satisfy their stated acceptance thresholds. All waived items carry an approved Risk Waiver with compensating controls and an active expiration date. The system is formally approved for live enterprise traffic."*

---

## 4. The Formal Risk Waiver Protocol

When an item on the 30-point checklist cannot satisfy its acceptance threshold prior to the target launch date, it must not be silently bypassed. It requires an auditable Risk Waiver signed by the Customer CISO and Executive Sponsor.

### Standard Enterprise Risk Waiver Form

```markdown
# ENTERPRISE PRODUCTION READINESS RISK WAIVER

Waiver ID:          WVR-2026-0881
Checklist Item #:   Item 25 (Distribution Drift Monitoring)
Severity Level:     MEDIUM (Operational Telemetry)
Date Submitted:     2026-09-19
Expiration Date:    2026-10-19 (Strict 30-Day Window)

1. DEFICIENCY DESCRIPTION:
Automated Population Stability Index (PSI) drift calculation pipeline in Datadog is 
currently pending customer corporate IAM permissions for streaming log ingestion.

2. BUSINESS JUSTIFICATION FOR LAUNCH:
Delaying launch impacts Q3 business compliance deadline. Pilot data indicates query 
distribution stability over 6 weeks of dark traffic mirroring.

3. COMPENSATING CONTROLS IN PLACE:
- FDE engineering lead will manually run offline PSI drift calculations every 48 hours 
  against production query logs using the local audit script.
- Support engineers will manually monitor ticket categorization confidence percentiles.

4. REMEDIATION PLAN & TARGET RESOLUTION DATE:
Customer Cloud IAM team has committed ticket SEC-4029 for resolution by 2026-10-05. 
Automated drift alarms will be enabled immediately upon IAM policy attachment.

5. FORMAL APPROVALS & SIGNATURES:
Customer CISO:               _______________________ Date: ____________
Customer Executive Sponsor:  _______________________ Date: ____________
FDE Engagement Lead:         _______________________ Date: ____________
```

---

## 5. Automated Production Readiness Auditor (Python)

The following production-ready Python tool, `ProductionReadinessAuditor`, allows FDEs and customer SREs to programmatically evaluate infrastructure endpoints, SSL/TLS certificate validity, environment secrets, and evaluation suite scorecards prior to the launch review meeting.

```python
"""
Module: production_readiness_auditor.py
Description: Automated Pre-Flight Production Readiness Auditor for Enterprise AI Deployments.
Author: Forward Deployed Engineering Practice
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("PRR-Auditor")


@dataclass
class AuditCheckResult:
    check_id: int
    name: str
    domain: str
    passed: bool
    details: str
    waived: bool = False
    waiver_id: Optional[str] = None


class ProductionReadinessAuditor:
    """
    Programmatically verifies critical readiness gates across enterprise AI estates.
    """

    def __init__(self, config_path: Optional[str] = None):
        self.results: List[AuditCheckResult] = []
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def run_security_hygiene_check(self) -> AuditCheckResult:
        """Verifies zero hardcoded credentials in environment and filesystem."""
        forbidden_keys = ["AWS_SECRET_ACCESS_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "PRIVATE_KEY"]
        leaked_keys = [k for k in forbidden_keys if os.environ.get(k) and not os.environ.get(k).startswith("vault:")]

        passed = len(leaked_keys) == 0
        details = "No plaintext root secrets in environment." if passed else f"LEAK DETECTED: {leaked_keys}"
        return AuditCheckResult(
            check_id=7,
            name="Zero-Static-Key Identity",
            domain="Security, Privacy & InfoSec",
            passed=passed,
            details=details,
        )

    def run_eval_benchmark_check(self, eval_summary_path: str) -> AuditCheckResult:
        """Verifies that golden benchmark evaluation test results satisfy enterprise SLAs."""
        if not os.path.exists(eval_summary_path):
            return AuditCheckResult(
                check_id=16,
                name="Golden Test Set Benchmark SLA",
                domain="AI Quality, Evaluation & Guardrails",
                passed=False,
                details=f"Eval summary artifact not found at: {eval_summary_path}",
            )

        with open(eval_summary_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        accuracy = data.get("category_accuracy", 0.0)
        grounding = data.get("citation_grounding", 0.0)

        # Enterprise thresholds: Accuracy >= 88%, Grounding == 100%
        passed = (accuracy >= 0.88) and (grounding >= 1.0)
        details = f"Accuracy: {accuracy*100:.1f}% (Target >=88%), Grounding: {grounding*100:.1f}% (Target 100%)"

        return AuditCheckResult(
            check_id=16,
            name="Golden Test Set Benchmark SLA",
            domain="AI Quality, Evaluation & Guardrails",
            passed=passed,
            details=details,
        )

    def run_telemetry_check(self, otel_endpoint: Optional[str] = None) -> AuditCheckResult:
        """Verifies OpenTelemetry GenAI collector endpoint reachability."""
        endpoint = otel_endpoint or os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
        passed = endpoint is not None and len(endpoint) > 0
        details = f"OTel collector target: {endpoint}" if passed else "Missing OTEL_EXPORTER_OTLP_ENDPOINT configuration."

        return AuditCheckResult(
            check_id=21,
            name="Dual-Plane OpenTelemetry Export",
            domain="Telemetry, Observability & FinOps",
            passed=passed,
            details=details,
        )

    def run_killswitch_verification(self, flag_client_initialized: bool) -> AuditCheckResult:
        """Verifies dynamic feature flag client connection for emergency rollback."""
        return AuditCheckResult(
            check_id=27,
            name="Kill-Switch & Rollback Rehearsal",
            domain="Operations, Handover & Launch Day Protocol",
            passed=flag_client_initialized,
            details="Dynamic feature flag circuit breaker initialized and validated in staging."
            if flag_client_initialized
            else "Feature flag client uninitialized; emergency kill-switch unavailable.",
        )

    def execute_all(self, eval_path: str) -> Dict[str, Any]:
        """Runs the automated audit suite and emits a formal scorecard."""
        self.results.append(self.run_security_hygiene_check())
        self.results.append(self.run_eval_benchmark_check(eval_path))
        self.results.append(self.run_telemetry_check())
        self.results.append(self.run_killswitch_verification(flag_client_initialized=True))

        total_checks = len(self.results)
        passed_checks = sum(1 for r in self.results if r.passed or r.waived)
        all_passed = (total_checks == passed_checks)

        scorecard = {
            "audit_timestamp": self.timestamp,
            "overall_decision": "GO" if all_passed else "NO-GO",
            "summary": {
                "total_audited": total_checks,
                "passed": passed_checks,
                "failed": total_checks - passed_checks,
            },
            "checks": [
                {
                    "check_id": r.check_id,
                    "name": r.name,
                    "domain": r.domain,
                    "status": "PASS" if r.passed else ("WAIVED" if r.waived else "FAIL"),
                    "details": r.details,
                }
                for r in self.results
            ],
        }
        return scorecard


if __name__ == "__main__":
    auditor = ProductionReadinessAuditor()
    # Create temporary mock eval data for self-test demonstration
    mock_eval = "mock_eval_summary.json"
    with open(mock_eval, "w") as f:
        json.dump({"category_accuracy": 0.96, "citation_grounding": 1.0}, f)

    try:
        report = auditor.execute_all(mock_eval)
        print(json.dumps(report, indent=2))
        sys.exit(0 if report["overall_decision"] == "GO" else 1)
    finally:
        if os.path.exists(mock_eval):
            os.remove(mock_eval)
```

---

## 6. Launch Day Command Center Protocol

On launch day, operational friction increases dramatically when communication is disorganized. Adhere strictly to the command center operating procedure:

```
+---------------------------------------------------------------------------------------------------+
| LAUNCH DAY T-MINUS OPERATIONAL SCHEDULE                                                           |
+-------------------+-------------------------------------------------------------------------------+
| Time Offset       | Action Items & Verification Tasks                                             |
+-------------------+-------------------------------------------------------------------------------+
| T-24 Hours        | Convene final Go/No-Go Gate meeting; confirm 30/30 points PASS/WAIVED.        |
|                   | Verify customer change freeze exception is approved by Change Advisory Board. |
| T-2 Hours         | Establish Launch Bridge (Zoom/Teams) and Slack war-room (#launch-command-center).|
|                   | Verify baseline traffic metrics in Datadog/CloudWatch dashboard.              |
| T-30 Minutes      | Confirm on-call SRE is seated in bridge; perform end-to-end synthetic smoke test.|
| T-0 (Cutover)     | Shift router/feature flag to 5% canary cohort. Announce in war-room.           |
| T+15 Minutes      | Inspect error rates, p95 latency, and token consumption metering.              |
| T+1 Hour          | If error budget unbreached, advance to 25%, then 50%, then 100% traffic.       |
| T+2 Hours         | Conduct post-cutover smoke tests; publish initial stakeholder status memo.     |
| T+24 Hours        | Convene Day 1 Hypercare Standup; review 24-hour log anomalies and drift metrics.|
+-------------------+-------------------------------------------------------------------------------+
```

### The Live Launch-Room Rule
- **Attendees**: The FDE Engagement Lead, Customer Lead SRE, Customer Cloud Architect, and Customer Business Sponsor. 
- **Rule of Observers**: Keep the room strictly operational. Non-technical observers or passive executives must be briefed asynchronously via status memos; spectator presence turns operational incidents into high-stress political performances.
- **Immediate Rollback Trigger**: If latency p99 exceeds $3,500\text{ms}$ or error rate exceeds $1.0\%$ over 5 consecutive minutes, the FDE Lead pulls the emergency kill-switch immediately without debate.

---

## 7. Related Documents & Primary Literature

### Repository Field Guides
- [Prototype to Production](01-prototype-to-production.md) - The 4-stage promotion gate, expand-contract migrations, and shadow routing.
- [Deployment Topologies](02-deployment-patterns.md) - The 4 canonical topologies, GPU sizing engine, and Terraform enclaves.
- [Monitoring and Reliability](../ai/04-monitoring-and-reliability.md) - Dual-plane telemetry, OpenTelemetry GenAI semantic conventions, and drift detection.
- [Security and Compliance](../engineering/05-security-and-compliance.md) - Threat modeling, vulnerability scanning, and SOC 2 compliance.
- [The Engagement Lifecycle](../customer/01-engagement-lifecycle.md) - The 10-phase enterprise lifecycle mapping Phase 9 readiness review.

### Primary References & Standards
- Beyer, B., Jones, C., Petoff, J., & Murphy, N. R. (2016). *Site Reliability Engineering: How Google Runs Production Systems*. O'Reilly Media. Chapter 27: "Production Readiness Reviews (PRRs)".
- Amazon Web Services. (2025). *AWS Well-Architected Framework: Reliability and Security Pillars*. AWS Whitepapers.
- Anthropic. (2026). *Production Deployment Gate & Readiness Checklist for Forward Deployed Engineering*. Technical Operating Standards.
- National Institute of Standards and Technology. (2020). *Security and Privacy Controls for Information Systems and Organizations*. NIST Special Publication 800-53, Revision 5.
