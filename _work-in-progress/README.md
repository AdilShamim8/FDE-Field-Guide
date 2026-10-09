# Work in progress

Reviewed 2026-10-09. The [audit](../AUDIT.md) distinguishes corrected local defects from work required before making production or customer-quality claims. Contributions should follow [evidence discipline](../STYLING.md) and provide reproducible artifacts.

## Required production work

- Authenticate caller and tenant identity; authorize every intake, review, and feedback action. Role headers in the reference are caller declarations.
- Replace process-local queues and replay state with durable, tenant-isolated transactions; prove behavior across restarts and multiple workers.
- Bound request bytes, queue growth, retention, and downstream tool effects; collect privacy-reviewed telemetry.
- Acquire a permissioned, representative, independently annotated holdout. The 25 known legacy fixtures are regression checks, not customer evaluation evidence.
- Exercise backup restoration, failure injection, operator rollback, load, and cost under a declared workload. Set objectives with the customer before promotion.

## Evidence still needed

- Interview event artifacts and permission before presenting company question usage or verbatim transcripts.
- Practitioner deployment reports, architecture artifacts, and outcome measurements before publishing manufacturing or other customer success claims.
- Current salary surveys and posting captures with defined coverage, observation windows, and deduplication.
- Dataset-specific permissions and retention review before redistributing raw text. The current market snapshot distributes factual metadata; the CFPB sample excludes narratives.

## Expansion opportunities

International deployment and residency, engagement pricing and margin measurement, scope negotiation, staffing, and domain-specific operational playbooks remain useful topics. Prefer documented cases and measured trade-offs over invented customer stories.

## Related documents

- [Expert practicum](../learning-paths/expert-fde-practicum.md) - reviewable delivery gates
- [Reference project](../portfolio/reference-project/README.md) - implemented local behavior
- [Source ledger](../research/source_checks_2026-10-09.json) - dated checks and failed retrievals
