# FDE glossary

Use this glossary to understand customer delivery, integrations, AI evaluation, access control, and operations. Each term has a plain meaning and an example or boundary relevant to this guide. Reviewed 2026-10-11; definitions are explanations, not claims that the local reference implements every capability.

For terminal commands, Python environments, and your first project, use the shorter [foundation vocabulary](learning-paths/foundations/glossary.md). For learning order, use the [learning-path selector](learning-paths/README.md).

## Contents

- [Customer and delivery](#customer-and-delivery)
- [Software and integration](#software-and-integration)
- [AI and retrieval](#ai-and-retrieval)
- [Evaluation and failure handling](#evaluation-and-failure-handling)
- [Trust and data](#trust-and-data)
- [Operations and handover](#operations-and-handover)

## Customer and delivery

| Term | Plain meaning | Example or boundary |
|---|---|---|
| FDE | An engineer who works with customers to discover, build, evaluate, and hand over useful software. | Own an integration and explain its operating limits to the customer. |
| Stakeholder | A person affected by a system or able to influence its requirements and operation. | Distinguish the sponsor, end user, security reviewer, and support owner. |
| Discovery | Investigating the actual problem, workflow, constraints, and desired outcome before deciding what to build. | Ask an operator how a ticket is handled today before selecting a model. |
| Workflow | The sequence of people, decisions, data, and actions used to complete work. | Map intake, validation, review, and the final approved action. |
| Thin slice | A small end-to-end piece of useful behavior that can be tested and reviewed. | Import one permitted source and produce a reviewable summary. |
| Acceptance criteria | Specific conditions used to decide whether a deliverable meets its agreed purpose. | Specify what a duplicate request should return and who verifies the result. |
| BRD | Business requirements document: the problem, scope, requirements, and intended business outcome. | Describe the current process and measurable acceptance criteria; do not invent ROI. |
| TDD | Technical design document: the contracts, components, data flows, and failure behavior needed to implement the requirements. | Define payload fields, validation rules, and the response to a failed write. |
| UAT | User acceptance testing: intended users check whether the delivered workflow meets agreed needs. | Record actual user feedback and acceptance; a peer role-play remains practice. |
| ADR | Architecture decision record: a decision, its context, considered alternatives, and consequences. | Explain why a deterministic lookup was chosen instead of a generator. |

## Software and integration

| Term | Plain meaning | Example or boundary |
|---|---|---|
| API | Application programming interface: a contract through which software requests a capability from another component. | The ticket endpoint accepts a defined request and returns a structured result. |
| HTTP | A request/response protocol with methods, headers, status codes, and optional message bodies. | Distinguish a successful response from validation failure or a replay conflict. |
| JSON | A text format for objects, arrays, strings, numbers, booleans, and null. | The retained metadata sample is JSON; valid syntax does not prove factual truth. |
| Schema | A contract describing the expected structure and allowed values of data. | Require a nonblank account identifier rather than silently guessing one. |
| ETL | Extract, transform, load: acquire source data, apply declared transformations, and load a destination. | Retain the source digest and explain which fields enter SQLite. |
| CDC | Change data capture: identify and process source changes such as inserts, updates, and deletions. | Define revision order and replay behavior before applying customer updates. |
| Idempotency | Repeating an operation avoids an additional intended effect under its stated key, scope, and retention rules. | An unchanged local import replays; changed facts raise a conflict. |
| Transaction | A unit of database work committed together or rolled back when it cannot complete. | A conflicting existing row rolls back earlier inserts in that import. |
| DLQ | Dead-letter queue: a place for work that could not be processed under the retry policy and needs investigation or controlled replay. | Keep the reason, source reference, and next owner; the foundation importer has no DLQ. |

## AI and retrieval

| Term | Plain meaning | Example or boundary |
|---|---|---|
| LLM | Large language model: a trained model that processes and generates tokens using context. | A later model integration needs measured behavior; ETISE does not call a model. |
| Token | A unit produced by a particular tokenizer, which may be a word part, punctuation, or another encoded unit. | A regex word count is not a provider token budget. |
| Tokenizer | The model-specific process that maps input into token identifiers and may decode them back. | Use the selected model tokenizer when checking its context limit. |
| Embedding | A numeric representation used to compare or process inputs; its usefulness depends on the representation and task. | ETISE uses feature hashing rather than a learned embedding model. |
| RAG | Retrieval-augmented generation: retrieve source material and put it into a generator context to help produce a response. | Test retrieval and generation separately; retrieval alone is not a full RAG system. |
| Grounding | Checking whether a response or action is supported by the applicable evidence for the task. | An exact quote may exist but still come from a policy that does not apply. |
| Tool call | A model or controller request to execute a defined capability through an interface. | Validate arguments and authority before any external side effect. |
| MCP | Model Context Protocol: a protocol for exposing capabilities such as tools, resources, and prompts through client/server interfaces. | A protocol connection does not automatically grant safe access to customer systems. |

## Evaluation and failure handling

| Term | Plain meaning | Example or boundary |
|---|---|---|
| Evaluation set | Cases used to assess behavior against an explicit question, labeling rule, and acceptance criterion. | Keep lineage, selection, and reviewer decisions visible. |
| Regression fixture | A known input and expected behavior used to detect unintended changes. | The 25 ETISE cases are known contracts with unverified origins, not a customer holdout. |
| Holdout | Data kept outside development and tuning so it can assess behavior on cases not used to improve the system. | Do not tune against the holdout and then report it as untouched. |
| Precision | True positives divided by all predicted positives for a defined class and labeled population. | For a review flag, ask how many flagged cases were actually positive. |
| Recall | True positives divided by all actual positives for a defined class and labeled population. | For the same flag, ask how many positive cases were found. |
| Calibration | Agreement between predicted probabilities and observed outcome frequencies across a suitable labeled population. | A generated confidence score is not calibrated merely because it is between zero and one. |
| Abstention | Explicitly declining to decide or act when the system cannot meet the required evidence or authority conditions. | Missing applicable policy evidence routes the local reference to human review. |
| Prompt injection | Instructions in untrusted content that attempt to redirect a model or its tool use away from the intended task. | Retrieved text is data, not permission to run a command or expose a secret. |

## Trust and data

| Term | Plain meaning | Example or boundary |
|---|---|---|
| Authentication | Establishing the identity of a caller using an appropriate verified mechanism. | Caller-supplied role headers in ETISE do not authenticate identity. |
| Authorization | Deciding whether a caller or principal is permitted to perform an action on a resource. | Check allowed documents and write permissions using verified identity and scope. |
| RBAC | Role-based access control: permissions are assigned to roles and principals receive the roles they are entitled to. | A simulated role-filter test is useful but is not a production login boundary. |
| Least privilege | Grant only the access required for the stated work, with suitable scope and duration. | A read-only source import should not require permission to dispatch a response. |
| Tenant isolation | Keeping one customer or organizational scope from accessing or changing another scope data and state. | Include tenant scope in queries, caches, and mutation checks; a supplied account ID alone is insufficient. |
| PII | Personally identifiable information: information that identifies a person or can be linked to a person in context; applicable definitions vary. | Review permitted fields and retention; removing a name does not prove anonymity. |
| Provenance | Evidence of where an artifact originated, including source identity, acquisition, and relevant rights. | Preserve the source URL, capture date, and response hash without claiming the hash authenticates the author. |
| Lineage | The recorded path from source data through transformations to a derived artifact or decision. | Explain the restricted source-to-SQL field projection and retain its digest. |

## Operations and handover

| Term | Plain meaning | Example or boundary |
|---|---|---|
| SLI | Service-level indicator: a defined measurement of service behavior over a stated window. | Measure the success ratio or request latency for the actual API path. |
| SLO | Service-level objective: a target for an SLI over a stated window. | Define the acceptable latency distribution and workload before measuring it. |
| SLA | Service-level agreement: an agreement on service commitments and their contractual consequences. | A local engine timing is not evidence that an agreed customer SLA is met. |
| Error budget | The allowed unreliability implied by an SLO during its specified window. | Use measured budget consumption to inform release and reliability decisions. |
| Observability | The ability to investigate system behavior using signals such as logs, metrics, and traces. | Record enough context to diagnose a failure while respecting privacy and retention. |
| Rollback | A planned action to return a release or change to a known acceptable state. | Specify what happens to data and in-flight work rather than assuming a code rollback reverses every effect. |
| Runbook | Instructions for an operator to execute and verify a defined operating or recovery task. | Include actual commands, expected results, failure paths, and escalation contacts. |
| Handover | Transfer of operating knowledge and responsibility with explicit ownership and acceptance. | Have another person reproduce the instructions and record remaining limits. |

## How to use the terms

When you describe a project, name the implemented mechanism and the evidence you retained. Distinguish authentication from a role header, a regression result from an independent holdout, and a measured operating target from a contractual commitment. Define unfamiliar acronyms in a customer document instead of assuming the reader knows them.

## Related documents

- [Foundations](learning-paths/foundations/README.md) - practice the first concepts in a working project
- [Customer specifications](customer/02-requirements-to-spec.md) - connect terms to testable requirements
- [Expert practicum](learning-paths/expert-fde-practicum.md) - acceptance gates for experienced delivery
- [Reference implementation](portfolio/reference-project/README.md) - actual capabilities and missing controls
- [Evidence discipline](STYLING.md) - source, dataset, and claim requirements

## Further reading

- [Pinned Python tutorial](https://github.com/python/cpython/tree/2abcf904b8dac8c999d2b3aac76681abb333798a/Doc/tutorial) - language concepts for the tested interpreter version
- [Pinned FastAPI tutorial](https://github.com/fastapi/fastapi/blob/f5c6e9b4f9cadc1bf0f9a1fd672e621206b63007/docs/en/docs/tutorial/first-steps.md) - request and service concepts
- [Google SRE book](https://sre.google/sre-book/table-of-contents/) - service objectives, measurement, and operation
