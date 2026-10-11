# Lesson 4: understand retrieval before adding a model

[Beginner path](../beginner-to-fde.md). Prerequisites: complete the HTTP lesson and read a request/response body. Reviewed 2026-10-11.

You will inspect the evidence a service selects and explain why a correct quotation can still support the wrong decision. Keep two search responses and a short design note. This lesson uses the existing local reference; it makes no paid model calls.

## Learn the distinction

An LLM generates tokens from context. Retrieval selects material to put in that context. RAG combines retrieval with a generation step. A schema controls output shape; it does not prove the content is true. A learned embedding represents text with a trained model; feature hashing deterministically maps features into numeric buckets.

ETISE uses keyword rules, feature hashing, token overlap, and a response template over authored Apex policies. It has no LLM, learned embeddings, BM25, or extraction-repair loop. Use it to inspect the boundaries before attempting a larger system.

## Work through the reference

Keep the API from Lesson 3 running on port 8011. From a second terminal:

```bash
curl --fail --silent --show-error 'http://127.0.0.1:8011/api/v1/knowledge/search?q=Section%203.1%20critical%20outage'
curl --fail --silent --show-error 'http://127.0.0.1:8011/api/v1/knowledge/search?q=GDPR%20data%20residency%20Section%2011.3'
curl --fail --silent --show-error -H 'X-User-Roles: compliance' 'http://127.0.0.1:8011/api/v1/knowledge/search?q=GDPR%20data%20residency%20Section%2011.3'
```

Expected: the outage search includes `APEX-SLA-2026`. The default-role compliance search excludes `APEX-COMPLIANCE-DOC`; declaring the simulated compliance role makes it eligible. Headers are caller-supplied simulation, not authentication.

A search may still return unrelated permitted text. The ticket processor separately requires an applicable category/document mapping before strict-mode dispatch. Without the compliance policy, the compliance request routes to review rather than quoting an unrelated SLA. P0 escalation remains a separate path.

Read [the local agent](../../portfolio/reference-project/src/engine/agent.py) and find the category-to-document map, quote verification, and review decision. Explain each in your own words before changing anything.

## Try it yourself

Write a design note in `learning-artifacts/ai-design.md` with three choices: a deterministic category count, retrieval over permissioned documents, and model generation from retrieved evidence. State the user outcome, data needed, failure risk, and test for each. For the current CFPB categorical sample, an LLM is unnecessary to count products and cannot create authoritative severity labels from absent narratives.

For a later real-model experiment, obtain permitted documents and approved use of a selected provider first. Preserve model/version, inputs, outputs, latency, token usage, and review outcomes. Compare a deterministic baseline on the same cases. Add schema validation, bounded retries, missing-evidence review, and an independent labeled evaluation set. Never paste credentials into lesson scripts or publish them with a report.

The broader [LLM applications chapter](../../ai/01-llm-application-patterns.md) explains prompting, structured outputs, and application patterns. The [evaluation chapter](../../ai/03-evaluation-and-testing.md) explains the acceptance work that must accompany a generator. Local reference scores do not verify an external model integration you have not run.

## Debugging check

If a denied document appears, check the requested role and the filtering path; do not call a forged role header a secure login. If a retrieved quote is exact but irrelevant, inspect document applicability. If a chunk count is described as “tokens,” check whether it uses a model tokenizer or a regex word count.

## Exit check

- [ ] You can distinguish retrieval, generation, and a deterministic rule.
- [ ] You can reproduce the two role-filtered searches and describe the missing authentication boundary.
- [ ] Your design note gives a reason to add a model and a test for its failure behavior.

Next: [Lesson 5 - evaluation and handover](05-evaluation-and-handover.md).

## Related documents

- [Reference architecture](../../portfolio/reference-project/docs/ARCHITECTURE.md) - actual data and authority boundaries
- [Agents and tools](../../ai/02-agents-and-tools.md) - later tool-use concepts; diagrams are proposals
- [Glossary](glossary.md) - vocabulary for embeddings, RAG, holdout, and authority

## Further reading

- [Pinned inspiration RAG lesson](https://github.com/rohitg00/ai-engineering-from-scratch/blob/1c8e62b526e78b8773559594aab3a3487d9998ac/phases/11-llm-engineering/06-rag/docs/en.md) - a deeper learning reference; measure architecture claims on your own workload
