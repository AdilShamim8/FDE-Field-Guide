# Discovery and Requirements Engineering

In enterprise technology, the most catastrophic engineering failures do not occur during deployment;
they occur during the first two weeks of discovery. Building an architecturally flawless, highly scalable,
and mathematically sophisticated system for the wrong business problem is the single most expensive error
a Forward Deployed Engineer (FDE) can commit. Once code is written and infrastructure is provisioned, reversing
bad architectural assumptions costs weeks of schedule slip and erodes stakeholder credibility.

The empirical data reflects this reality: in an independent analysis of 146 deduplicated enterprise FDE job
postings across 94 employers ([`job-market/dataset/fde_market_data.json`](../job-market/dataset/fde_market_data.json)),
**scoping requirements and technical discovery appears in 52.0% of postings**—matching RAG (52.0%) and outpacing
Kubernetes (35.0%). OpenAI's enterprise FDE role specification explicitly places discovery first in its core
mandate: *"lead technical discovery, architecture, implementation, evaluation, productionization, and handoff"*
([OpenAI Careers, 2026](https://openai.com/careers)).

Furthermore, the **MIT NANDA Initiative** (Fortune, August 2025) revealed that roughly **95% of enterprise
generative AI pilots fail to deliver measurable P&L impact**. The small 5% that succeed do not succeed because
of superior foundational models; they succeed because they are surgically integrated into concrete operational
workflows discovered on the ground.

This guide provides the field manual for technical discovery: the 5-phase discovery lifecycle, the 8-theme
practitioner interview protocol, forensic SQL data auditing techniques, an empirical financial dispute case
study backed by CFPB data, and direct codebase defenses.

---

## 1. The 5-Phase Discovery Engineering Lifecycle

Technical discovery is not casual conversation or pre-sales relationship building; it is a structured,
forensic engineering process that converts vague executive aspirations into binding, testable technical contracts:

```mermaid
graph TD
    subgraph Discovery Engineering Lifecycle
        P1["<b>Phase 1: Executive Intent Decoding</b><br/>• Translate 'we need AI' into quantified P&L pain<br/>• Identify economic sponsor & strategic KPIs"] --> P2["<b>Phase 2: Operator Shadowing</b><br/>• Reverse-engineer actual ground-truth workflow<br/>• Map human screens, clicks, exports & workarounds"]
        P2 --> P3["<b>Phase 3: Forensic Data & Schema Audit</b><br/>• Inspect raw database schemas (information_schema)<br/>• Profile null rates, skew, encoding & edge cases"]
        P3 --> P4["<b>Phase 4: Non-Functional Negotiation</b><br/>• Establish P99 latency, throughput & VPC boundaries<br/>• Define RBAC, data egress & compliance fences"]
        P4 --> P5["<b>Phase 5: Executable Specification Gating</b><br/>• Author Given/When/Then acceptance criteria<br/>• Assemble Golden Evaluation set & sign Go/No-Go"]
    end

    P3 -.-> Parser["Defensive Parsing<br/>interviews/code/parser.py"]
    P5 -.-> Spec["ETISE Engineering Spec<br/>customer/02-requirements-to-spec.md"]
    P5 -.-> Evals["Golden Evaluation Harness<br/>portfolio/reference-project/evals/"]

    classDef phase fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef tool fill:#0f172a,stroke:#64748b,stroke-width:1px,color:#cbd5e1;
    class P1,P2,P3,P4,P5 phase;
    class Parser,Spec,Evals tool;
```

---

## 2. The 8-Theme Technical Discovery Protocol

Run discovery interviews as disciplined 45-minute sessions. Pair two engineers: one leads the questioning
while the other captures technical transcripts and architecture notes. Record sessions with explicit client
permission. Close every interview by reading back key takeaways and resolving contradictions in the room.

### Theme 1: Current-State Workflow Mechanics
*Objective: Uncover how the work actually happens, not how the executive manual claims it happens.*
- "Walk me through the lifecycle of the last concrete ticket or case handled yesterday, from arrival to closure."
- "What exact tools, browser tabs, terminal windows, spreadsheets, and internal Slack/Teams channels were open?"
- "If an engineer sat silently beside your team for an entire shift, what would be the most surprising manual workaround?"

### Theme 2: Quantified Pain & Financial Cost
*Objective: Attach dollar amounts, operator hours, or customer churn numbers to the problem.*
- "What does this operational bottleneck cost per week in human hours, direct customer credits, or delayed SLA penalties?"
- "Which failure hurts the organization more: slow turnaround time or inaccurate decisions that require manual rework?"
- "What happens to the business unit if this system remains completely unchanged for the next twelve months?"

### Theme 3: Volume, Velocity & Edge-Case Distributions
*Objective: Size the system and detect distribution skews before architecting ingestion pipelines.*
- "How many events, tickets, or records pass through this pipeline daily, and what does the peak-to-median ratio look like?"
- "What percentage of cases are considered 'routine,' and what were the three weirdest edge cases encountered last month?"
- "Which classes of cases must *never* be handled autonomously and must always divert to human operators?"

### Theme 4: Measurable Success Metrics & 90-Day P&L Objectives
*Objective: Define the exact scorecard used to judge the project at steering committee reviews.*
- "Ninety days after production deployment, what single metric tells executive leadership that this investment succeeded?"
- "What is the current empirical baseline for that metric, and who is the official source of truth for measuring it?"
- "What outcome would cause leadership to label this project a failure, even if the software ships on time with zero bugs?"

### Theme 5: Enclave, Security & Regulatory Constraints
*Objective: Identify VPC isolation, data classification, and compliance barriers before writing code.*
- "What classification does this data hold (PII, PHI, PCI-DSS, MNPI), and does customer data ever have permission to leave your VPC?"
- "Are we deploying inside an air-gapped AWS enclave, Azure GovCloud, or on-premise OpenShift cluster?"
- "What corporate proxy, egress filtering, and TLS interception appliances sit between our runtime and external APIs?"

### Theme 6: Decision Structure & Hidden Approvers
*Objective: Prevent week-six project vetos by identifying every governance stakeholder on Day 1.*
- "Who has the authority to formally sign off on production cutover? Who holds operational veto power?"
- "Whose approval was required on the last major technical initiative that surprised the project team late in the cycle?"
- "Who represents InfoSec, Legal, and Data Governance, and have they reviewed our preliminary data flow diagram?"

### Theme 7: Prior Attempts & Deceased Vendor Post-Mortems
*Objective: Avoid repeating historical failures and understand organizational antibodies.*
- "What has been attempted before to solve this problem, whether through internal engineering or external vendors?"
- "Why did the previous attempt stall, lose executive sponsorship, or fail in production?"
- "May we review the post-mortem, architecture spec, or ticket export from that previous project?"

### Theme 8: Boundary Invariants & Scope Exclusions
*Objective: Establish explicit non-goals to prevent insidious sprint-over-sprint scope creep.*
- "What related upstream and downstream systems are explicitly *out of scope* for this engagement?"
- "What capabilities are nice-to-have aspirational features that must not gate the Phase 1 production release?"

---

## 3. Forensic Data Walkthrough & Schema Auditing

Never accept a curated demo dataset or synthetic CSV export as representative of customer production reality.
Curated demo environments lie: they feature clean UTF-8 text, zero missing fields, balanced categorical distributions,
and negligible concurrency. Production enterprise databases contain 15 years of schema migrations, corrupted encodings,
and unindexed join keys.

### Essential Discovery SQL Profiling Queries

When granted read-only access to customer data stores, execute these non-destructive profiling queries
immediately to discover data rot:

#### 1. Schema Introspection Without DBA Intervention
```sql
-- Map all tables and column types across the target customer schema
SELECT 
    table_name, 
    column_name, 
    data_type, 
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'customer_production'
ORDER BY table_name, ordinal_position;
```

#### 2. Null Rate and Cardinality Distribution
```sql
-- Audit missing data, unique cardinality, and record volume in critical fields
SELECT 
    COUNT(*) AS total_records,
    COUNT(customer_id) AS non_null_ids,
    COUNT(DISTINCT customer_id) AS unique_ids,
    ROUND(100.0 * (COUNT(*) - COUNT(issue_category)) / COUNT(*), 2) AS category_null_pct,
    ROUND(100.0 * (COUNT(*) - COUNT(dispute_amount)) / COUNT(*), 2) AS amount_null_pct,
    ROUND(100.0 * (COUNT(*) - COUNT(narrative_text)) / COUNT(*), 2) AS narrative_null_pct
FROM customer_production.disputes;
```

#### 3. Timestamp Skew and Format Fragmentation
```sql
-- Detect timestamp nulls, unparseable formats, and timezone anomalies
SELECT 
    MIN(created_at) AS earliest_record,
    MAX(created_at) AS latest_record,
    COUNT(*) FILTER (WHERE created_at > NOW()) AS future_dated_anomalies,
    COUNT(*) FILTER (WHERE created_at IS NULL) AS unversioned_records
FROM customer_production.disputes;
```

#### 4. Categorical Class Imbalance
```sql
-- Identify rare edge-case categories vs dominant classes
SELECT 
    COALESCE(issue_category, 'MISSING') AS category,
    COUNT(*) AS frequency,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) AS share_percentage
FROM customer_production.disputes
GROUP BY issue_category
ORDER BY frequency DESC;
```

---

## 4. Source-backed discovery exercise: what the current records actually establish

Reviewed on 2026-10-09. The former narrative of a deployed financial institution, fines, analyst observations, and a 25-case customer sign-off had no reproducible supporting artifacts. It is replaced with an exercise using actual [CFPB categorical metadata](../portfolio/reference-project/evals/real_data/cfpb_metadata_2026-10-09.json) and the [market source audit](../job-market/dataset/README.md).

1. Identify the decision the customer needs to make before proposing automation. Ask for workflow ownership and an observed baseline; the public records do not provide either.
2. Inspect the actual source schema and permission. The five CFPB records have product/issue labels but no retained narrative or ETISE severity. Keep missing labels missing.
3. Record the sampling rule and collection date. Five recent complaints are not a population sample or proof of company fault; a source retrieval today does not redate older records.
4. Review legal requirements with the responsible customer owner. [Regulation E §1005.11](https://www.consumerfinance.gov/rules-policy/regulations/1005/11/) has conditional business-day investigation and provisional-credit provisions; it does not establish a blanket $1,000 or $5,000 escalation threshold with a universal ten-day final-resolution duty.
5. Agree a labeled customer holdout and an acceptance measurement before building a classifier. Bitext is publisher-described hybrid synthetic data, and the old ETISE cases are unverified regression fixtures.
6. Write down source limitations, unresolved access, the next measurable deliverable, and the owner who can resolve each unknown. Do not invent interview quotes or customer outcomes to complete a discovery document.

## 5. Executable references and remaining work

- [Source ledger](../research/source_checks_2026-10-09.json) records selected primary-source checks and failures.
- [Evidence validator](../research/validate_evidence.py) checks the retained metadata projection and date/ID accounting.
- [ETISE](../portfolio/reference-project/README.md) implements local triage and review mechanics; it does not implement statutory deadline clocks or authenticated customer boundaries.
- [Expert practicum](../learning-paths/expert-fde-practicum.md) defines the real data, decision, and handover artifacts required to proceed.

## 6. Primary Practitioner Literature & Citations

1. **OpenAI**: *Forward Deployed Engineer, Enterprise & Applied Engineering Role Standards* (2026). [openai.com/careers](https://openai.com/careers)
2. **Anthropic**: *Forward Deployed Engineer - Enterprise Deployments & Customer Discovery Rigor* (2026). [job-boards.greenhouse.io/anthropic/jobs/5302966008](https://job-boards.greenhouse.io/anthropic/jobs/5302966008)
3. **MIT NANDA Initiative / Fortune**: *The GenAI Divide: Why 95% of Enterprise AI Pilots Fail* (August 2025). [fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo)
4. **Consumer Financial Protection Bureau (CFPB)**: *Consumer Complaint Database Public API & Schema Specifications*. [consumerfinance.gov/data-research/consumer-complaints](https://www.consumerfinance.gov/data-research/consumer-complaints/)
5. Bitext: hybrid synthetic training data, excluded from real-world-only evidence. [huggingface.co/datasets/bitext](https://huggingface.co/datasets/bitext)
6. **Alexander Karp & Shyam Sankar**: *The Palantir Forward Deployed Engineering Methodology: Direct Ground-Truth Discovery* (Palantir Technologies, 2024).
