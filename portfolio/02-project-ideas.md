# Portfolio Project Ideas

Twelve project specs written the way real customer briefs arrive: deliberately ambiguous on
the surface, with the hard problems hidden underneath. Each spec gives you the brief as a
customer would say it, the ambiguity you must resolve before building, the skills it proves,
the depth markers that separate a pass from a strong build, and the hidden depth that makes
it FDE-shaped. All twelve are fictional composites; none describes a real company's system.

## How to use these briefs

- The brief is written as a customer would say it - vague on purpose; resist cleaning it up before writing it down, because the cleaning is the work
- The ambiguity line names the decisions you must resolve first - resolving them with interviews, notes, and a spec is the FDE demonstration
- The skills line maps to the guide sections that teach the techniques
- The depth markers line is what a strong build shows over a passing one; treat the markers as the definition of done
- The hidden depth line is the part that makes the project deployment-shaped rather than a demo

These twelve specs are recommendations, not requirements: swap the domain, keep the
structure. Pick one project, not six, and walk it through the
[FDE loop](../role/05-the-fde-loop.md) end to end.

## The twelve briefs

### 1. Support-ticket triage for a mid-size SaaS

- Brief - "Our support queue is a firehose and everything lands in one pile. Make tickets route themselves and the urgent ones jump the line."
- Ambiguity - nobody has defined "urgent" or the routing classes, and nobody has said what happens when the classifier is unsure
- Skills - classification, confidence thresholds, human review queues, feedback capture
- Depth markers - per-class routing accuracy on a golden set, a review queue a human actually works, and a written threshold decision with the trade-off named
- Hidden depth - the review queue and the threshold are the product; the classifier is a component, and misrouting feedback is what makes it improve

### 2. Document Q&A over a messy public corpus

- Brief - "People keep asking us questions our documents already answer. Build something that answers them, with the receipt attached."
- Ambiguity - which documents count as the corpus, how to treat amended and superseded versions, and what citation satisfies a skeptical reader
- Skills - RAG, ingestion over dirty corpora, citation grounding, retrieval-versus-generation evaluation
- Depth markers - a retrieval failure analysis on real queries, handling for amended documents, and honest "I don't know" behavior when retrieval comes up empty
- Hidden depth - retrieval quality over dirty, duplicated, contradictory documents is the whole project; the model is incidental and swappable

### 3. Invoice-extraction pipeline for a bookkeeping firm

- Brief - "We retype supplier invoices into ledgers all day. Read the invoices and fill the ledger."
- Ambiguity - the accuracy bar per field, what counts as an exception, and who fixes exceptions and how fast
- Skills - structured outputs, schema validation, exception queues, idempotent ingestion
- Depth markers - per-field accuracy numbers, a working exception queue with a human workflow, and a schema that survived twenty vendors' formats
- Hidden depth - a silent 3% error rate is worse than a loud one; the exception queue, not the extraction, is what makes it deployable

### 4. Meeting-notes-to-CRM updater

- Brief - "After every customer call the notes never make it into the CRM. Update the CRM from the notes automatically."
- Ambiguity - which fields an automated writer may touch, what requires human approval, and how to avoid duplicating or overwriting edits made by hand
- Skills - agents with tools, approval gates, idempotency, audit trails
- Depth markers - a write-policy matrix of field against confidence against approval, updates that are safe to replay, and a working undo path
- Hidden depth - write discipline, not extraction, is the hard problem; unconditional CRM write access is a liability no customer accepts

### 5. Data-warehouse enrichment pipeline

- Brief - "Our account table is a graveyard of free-text sales notes. Enrich it so marketing can actually segment."
- Ambiguity - which fields to enrich, how backfills interact with live rows, and what happens when enrichment disagrees with a human-entered value
- Skills - batch LLM enrichment, idempotent backfills, data-quality checks, cost control
- Depth markers - a backfill you ran twice with identical results, quality checks with a quarantine path, and a cost-per-row figure you can defend
- Hidden depth - re-runs and backfills dominate the engineering; the model call is the easy 10%, and idempotency is what separates a pipeline from a script

### 6. Compliance-review assistant for a nonprofit grant process

- Brief - "Volunteers review grant applications against a 90-page rulebook and things slip through. Help them check."
- Ambiguity - whether the system assists or decides, what the audit trail must reconstruct, and what to do when the rulebook contradicts itself
- Skills - RAG over policy text, audit trails, citation-grounded answers, designing for non-technical users
- Depth markers - an audit trail that reconstructs every recommendation, citations on every claim, and a documented assistive-only boundary
- Hidden depth - auditability and the assistive-only boundary are what let the system near a compliance process; capability alone gets it rejected

### 7. Multi-source dashboard ingest

- Brief - "We pay for two data tools and neither shows the numbers we need together. Pull both into one dashboard."
- Ambiguity - the rate limits differ per source, the numbers disagree between sources, and someone has to decide whose figures are authoritative
- Skills - third-party API integration, rate-limit pacing, reconciliation, scheduled ingestion
- Depth markers - a reconciliation report that surfaces discrepancies, backoff that survived a real quota window, and a written tie-breaking rule
- Hidden depth - the integration is easy once; the project is surviving schema drift, quota resets, and sources that disagree about the same metric

### 8. Voice-of-customer classifier over public app reviews

- Brief - "Read the app-store reviews and tell us what users actually complain about, by app version."
- Ambiguity - nobody has defined the complaint taxonomy, reviews mix several issues at once, and some classes will have almost no examples
- Skills - classification, per-class metrics, drift monitoring, taxonomy design
- Depth markers - per-class precision and recall with the weak classes named, a drift alarm that fired on a real change, and version-sliced trends
- Hidden depth - the class distribution is imbalanced and partly junk; per-class honesty, not headline accuracy, is the deliverable

### 9. Internal-wiki RAG with freshness checks

- Brief - "Our wiki is huge and half of it is out of date. Answers need a freshness guarantee."
- Ambiguity - nobody can say how to measure staleness, what should happen to stale pages, or which of three overlapping pages is authoritative
- Skills - incremental ingestion, staleness alarms, RAG over evolving corpora
- Depth markers - incremental ingestion that updates without a full rebuild, staleness surfaced in the answers themselves, and an alarm that caught a real freeze
- Hidden depth - freshness is a data-engineering property, not a prompt; the incremental pipeline and its alarms are the project, the chat is the interface

### 10. Order-email parser for a small e-commerce operation

- Brief - "Orders arrive as emails in six different formats. Turn them into clean records and tell me which ones need a human."
- Ambiguity - the record schema, the trigger for human review, and the handling of partial or self-contradicting emails
- Skills - extraction, structured output, human-in-the-loop design, daily digests
- Depth markers - an exception queue with a named owner and turnaround, a daily digest the owner actually reads, and replay-safe ingestion
- Hidden depth - the workflow of queue, digest, and replay is the product; the parser is one component that must fail loudly into it

### 11. Self-hosted model deployment in a locked-down environment

- Brief - "Security says nothing leaves the building, and the AI tooling all assumes internet. Run it inside our network anyway."
- Ambiguity - no egress means no package or model downloads, so updates, artifacts, and evaluation all need a new answer
- Skills - self-hosted inference, `docker compose`, artifact mirrors, offline evaluation, air-gapped operations
- Depth markers - a documented offline install from a mirror you stood up, an eval suite that runs with egress blocked, and a tested rollback procedure
- Hidden depth - the constraint changes every habit: since you likely cannot borrow a locked-down network, simulate it - block egress at the network layer, host the mirror locally, and prove the system under the rules a customer would impose

### 12. Monitoring and eval harness for someone else's LLM feature

- Brief - "Another team shipped an AI feature. It works, mostly. We need to know the moment it stops."
- Ambiguity - you do not own the feature, so you must negotiate what you can instrument, which quality metric its owner accepts, and who gets paged
- Skills - evaluation harness design, dashboards and alerting, incident runbooks, working with an owner who did not ask for you
- Depth markers - a golden set built from their real traffic, dashboards someone else checks weekly, and a runbook another person has executed
- Hidden depth - negotiating instrumentation with an uninterested owner is the FDE skill; the harness is the artifact, and the agreement is the deployment

## How to pick

- Pick the brief closest to a domain you already know - domain knowledge turns a demo into a credible deployment story, and it is the one input you cannot fake
- Two projects done deeply beat six started - the depth signals accumulate inside a project, and interviewers find them with two questions
- The workflow-embedded briefs (1, 3, 4, 10) exercise the integration dimension the MIT NANDA research ties to success ([Fortune, August 2025](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo))
- If you come from infrastructure, briefs 11 and 12 differentiate strongly, because operations-shaped portfolios are rare

Whichever you pick, read [what to build](01-what-to-build.md) first and hold the project to
its six principles.

## Related documents

- [What to build](01-what-to-build.md) - the principles these briefs are engineered around
- [Presenting projects](03-presenting-projects.md) - how to write up whichever brief you pick
- [The FDE loop](../role/05-the-fde-loop.md) - walk your chosen brief through every stage
- [Discovery and requirements](../skills/02-discovery-and-requirements.md) - resolving the ambiguity line is this skill in practice
- [Agents and tools](../ai/02-agents-and-tools.md) - the tool and agent design behind briefs 4 and 12
- [Data pipelines](../engineering/03-data-pipelines.md) - the ingestion and idempotency work behind briefs 5, 7, 9, and 10

## Further reading

- [Independent job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md) - the posting evidence behind the skills lines (February-July 2026)
