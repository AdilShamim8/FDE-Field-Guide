# Repository evidence and engineering audit

This audit is for contributors taking the guide from useful learning material to defensible engineering work. The initial findings refer to repository commit `ff473e3`; remediation and source checks were completed on 2026-10-09. Recommendations are engineering judgments, not claims about a real customer deployment.

## October 11 beginner follow-up

The [2026-10-11 beginner review](research/beginner_review_2026-10-11.md) documents the new foundations sequence, corrected learning-path claims, pinned inspiration, selected source checks, and executed exercises. The suite now has 89 passing tests, including local ingestion failures and discovery of every saved dated ledger. All 25 known regression contracts continue to pass.

The October 11 official CFPB query returned zero hits at capture time. The five-record teaching input retains its October 9 receipt and retrieval dates. No worldwide dataset, independent customer benchmark, or blanket source recertification is claimed. Initial inventory and remediation details below retain their October 9 scope.

## Scope and verification limits

The repository inventory contains 128 tracked project files across all fourteen guide sections, runnable interview exercises, ETISE, and three data collections. Structural checks cover the whole inventory: links, portability, dataset schema, claim patterns, and correspondence between documented controls and code. Functional investigation covers the runnable Python workflows. This does not certify every external citation or claim in every paragraph.

The current market source was fetched today at [AI Engineering Field Guide commit ed590319](https://github.com/alexeygrigorev/ai-engineering-field-guide/tree/ed590319553252e2b8275486597b144ac55a4f3c). Its raw CSVs extend through 2026-09-23, although its FDE article still describes February–July. Retrieval date is not collection date. No source accessed here establishes an October 9 job-board scrape or the entire worldwide FDE labor market.

Initial proxy denials were resolved and the affected selected sources were rechecked. The [source ledger](research/source_checks_2026-10-09.json) preserves sixteen successful retrievals, response hashes, scoped observations, and one failed retrieval of a guessed Fortune URL. It covers CFPB, the Bitext publisher card, upstream extraction notes, NIST, current OWASP guidance, selected provider documentation, and practitioner/secondary reporting. Existing timestamps, reachable URLs, author allowlists, and passing JSON assertions do not authenticate every adjacent quotation, interview, license, or customer outcome.

## Why the initial guide did not establish an expert bar

The issue is the gap between assertions and evidence. More diagrams, named frameworks, or larger checklists cannot establish production experience. An expert deliverable states which controls run, tests their failure boundaries, preserves data lineage, quantifies uncertainty, and gives an operator a recovery procedure that works.

The findings below describe the initial state. The remediation section identifies the changes actually implemented; unresolved production requirements remain separate.

### Data and claims

- The market JSON contains aggregates, not 146 raw postings. The current upstream deduplicated CSV contains 8,051 job IDs; the original `FDE|forward deploy` title filter matches 212 IDs across 125 employer names. This is a dated, board-specific sample, not a census.
- Per-scrape CSV rows contain repeated job IDs across locations. September has 127 matching rows but 91 unique matching IDs; August has 140 rows but 103 unique IDs. Raw rows and distinct vacancies must have separate labels. A decline between these two observations also contradicts an uninterrupted-growth narrative.
- Matching hyphenated titles and word-bounded `FDE` changes the cumulative result to 220. Report this sensitivity; changing a title definition changes the measured market.
- Monthly title matches contain 237 distinct IDs, versus 212 cumulative matches. Twenty-five IDs appear only in the monthly matching union. The source artifact preserves this membership/title discrepancy instead of forcing agreement.
- The upstream extraction audit explicitly reports problems with management and company-stage labels and warns that a known evaluation seed is burned. Existing source-derived skill and responsibility aggregates are historical estimates, not newly verified measurements of the 212-role sample.
- ETISE's 25-case file has no original record hashes, immutable source revisions, transformation artifacts, or annotator records. The claimed CFPB complaint IDs and Bitext intent mappings cannot be reproduced from `curate_eval_dataset.py`, which only counts fields. Keep these cases as legacy regression fixtures with unverified provenance; exclude them from real-world quality claims.
- The Apex knowledge corpus is locally authored sample policy text. Substring matching against that corpus does not verify AWS, Stripe, Datadog, GDPR, factual answer support, or legal compliance.
- Interview `tested_at` company lists and authored response rubrics have no event-level evidence. They are preparation material, not authenticated company interview transcripts.
- Claimed salaries, conversion rates, fines, ROI, and production case-study outcomes need dated artifacts before they can be treated as observed evidence. A source link alone does not support every number near it.

### Code and evaluation

- ETISE classification uses keyword overrides and feature hashing with hand-written word clusters. It has no model inference, learned embedding model, BM25 term-frequency model, or extraction repair loop.
- The fallback classifier raises confidence to at least 0.85 even for unrelated input. The strict-grounding setting does not prevent dispatch when retrieval returns no evidence.
- Caller-supplied roles are not authenticated identity. Omitting the roles header bypasses document filtering. A stronger local default must not be described as production authorization.
- The API replays a key across accounts, ignores payload conflicts and configured expiry, and has no atomic protection against concurrent retries. Queues and feedback are process-local, without durability or tenant-authenticated access.
- The original evaluation acceptance gate ignores routing accuracy and required citation document IDs. Zero emitted citations can receive 100% grounding. Neither a 25/25 score on known examples nor a sub-millisecond local CPU timing proves production accuracy or API latency.
- The retry exercise's default sleep callback does nothing. The chunking exercise can exceed its advertised token limit on long sentences and after adding overlap.
- The ten-pass interview audit hard-codes a Windows checkout path. It validates content conventions, not provenance authenticity.

### Operations and maintenance

- The reference architecture describes authentication, Redis, payload ceilings, PII telemetry sanitization, and model settings that are absent from the service.
- The runbook invokes nonexistent admin endpoints, mode variables, and rebuild commands. These are unsafe instructions for an operator to rely on.
- Several cross-links point to missing files, and embedded Windows `file:///` links are unusable on GitHub.
- There is no CI workflow to keep the runnable examples, dataset validators, and evaluation acceptance gate from regressing.

## Improvement sequence

1. Publish a dated, reproducible market snapshot with immutable source paths, SHA-256 hashes, explicit title matching, deduplication rules, and raw-versus-unique counts. Preserve the historical dataset with an explicit status instead of overwriting its observation window.
2. Correct the reference project and provenance documents so readers can distinguish implemented behavior, unverified fixtures, and future production requirements.
3. Repair confirmed runtime defects and add regression coverage for conflicts, account and role scopes, expiry, concurrent replay, empty evidence, routing failures, chunk budgets, and actual retry delay.
4. Replace unsupported production stories and numeric outcomes with clearly labeled design exercises or remove them. Keep statutory obligations separate from illustrative customer policies.
5. Add an expert practicum with reproducible evidence, holdout discipline, adversarial boundaries, reliability and cost measurement, and a customer handover acceptance gate.
6. Run these checks in CI. Keep failure counts, skipped checks, and external access limits visible.

## Remediation verified on 2026-10-09

- Published a source-pinned market snapshot, deterministic refresh tool, accounting validator, mutation tests, hashes, record references, sensitivity analysis, and the 212-versus-237 reconciliation. Full reproduction against the immutable upstream Git objects passed. The 146-role aggregates remain explicitly historical.
- Retained five actual CFPB categorical metadata records received today, with acquisition parameters and a source-response hash. No narratives, invented ETISE labels, or asserted customer outcomes were added. The sample is not random or representative. Bitext's publisher describes hybrid synthetic generation and `cdla-sharing-1.0`; the old real-interaction and CC BY 4.0 claims were withdrawn.
- Removed the classifier's artificial confidence floor and fictitious repair attempts. Missing applicable sample-policy evidence routes to review in strict mode. Live testing also exposed unrelated SLA quotations replacing an inaccessible compliance policy; an explicit local category/document map now prevents that dispatch. This is narrower than semantic entailment or legal verification.
- Corrected account/role replay context, payload conflict detection, configured TTL, bounded cache size, default role filtering, request-field limits, and single-process concurrent replay. Caller roles remain unauthenticated and queues remain process-local. These changes do not establish production tenant isolation or durable exactly-once effects.
- Repaired retry delay, chunk budgets and overlap, and Linux audit portability. Strengthened evaluation to gate routing, required documents, exact section quotations, nonempty grounding, and explicit failures. Interview checks now report declaration and structure validity rather than source authentication.
- Replaced unsupported customer stories, production scorecards, interview conversion rates, and provenance assertions with observed cases or labeled practice material. Reviewed indices and portfolio pitches now link to actual artifacts. The official Regulation E section supports conditional investigation/provisional-credit rules, not a universal dollar trigger or ten-day final-resolution guarantee.
- Added the [expert practicum](learning-paths/expert-fde-practicum.md) with baseline, lineage, holdout, authority, recovery, economics, platform, and handover gates. Rewrote architecture, scope, and runbook documents around actual local behavior and missing acceptance inputs.
- Verified constrained Python 3.12 installation and dependency consistency, 75 passing tests, all 25 known regression contracts, declaration/accounting validators, and 977 local Markdown links with zero failures. The Starlette TestClient deprecation warning remains visible; there were no skipped tests. Docker packaging and real-cloud deployment were not run.
- Restarted the corrected API and verified health/index, billing intake, applicable quotes, replay, 409 conflict, unknown-input review, denied-policy review, simulated compliance access, knowledge search, and metrics. Restart still clears in-memory state.
- Added [CI](.github/workflows/verify.yml) with full-SHA actions, read-only repository permissions, and retained regression reports. [GitHub run 37928424895](https://github.com/AdilShamim8/FDE-Field-Guide/actions/runs/37928424895) passed on commit `f4ae8fc` before this audit update. Later pushes receive their own checks.

TC-006, TC-015, TC-020, and TC-025 routing expectations were explicitly changed to review to match the corrected safety contracts. These are regression expectation changes, not newly adjudicated real-world labels. The source refresh's initial premature validation claim is documented in the [observed failure investigation](case-studies/03-failure-stories.md); subsequent full source reproduction passed.

All repository changes were committed one file at a time and each push was verified before proceeding to the next file. Git authentication temporarily failed during the CI push; the existing GitHub CLI credential binding restored access without storing a new token.

## What remains outside a verified production claim

Production deployment still needs authenticated tenant identity, durable storage and audit events, bounded retention and request resources, distributed concurrency control, operational telemetry, restore drills, and an independently collected and adjudicated customer evaluation set. Public datasets require a dataset-specific legal and privacy review. PII regexes alone cannot establish anonymization.

## Related documents

- [Evidence discipline](STYLING.md) - contribution and source requirements
- [Market dataset](job-market/dataset/README.md) - measurement scope and reproducibility
- [Reference project](portfolio/reference-project/README.md) - executable development workflow
- [Work in progress](_work-in-progress/README.md) - remaining work and ownership gaps

## Further reading

- [Upstream market extraction audit](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/ed590319553252e2b8275486597b144ac55a4f3c/job-market/_internal/eval/README.md) - measurement drift, unsupported labels, and holdout limits; accessed 2026-10-09
- [OpenAI Evals](https://github.com/openai/evals/tree/8eac7a7de5215c907fbddc30efdaf316913eccdd) - evaluation framework and data practices; repository accessed 2026-10-09
- [OWASP GenAI LLM Top 10](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/tree/9253e38ade58e959b531c0c5c9a4842272c9cd0e) - current security project identified through OWASP's maintained entry point on 2026-10-09; threat details require review against the pinned release
