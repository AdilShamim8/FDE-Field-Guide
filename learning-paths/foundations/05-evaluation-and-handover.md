# Lesson 5: test a boundary and hand the work over

[Beginner path](../beginner-to-fde.md). Prerequisites: read a Python function, run the data project, understand HTTP status codes, and explain why a retrieved quote may be irrelevant. Reviewed 2026-10-11.

You will reproduce an observed result, show a failure, and write instructions another person can use. Keep a test report and a filled customer brief. Completing these lessons demonstrates local practice, not production or hiring readiness.

## Work through the reference

From the repository root, using the environment prepared in the API lesson:

```bash
.venv/bin/python -m pytest learning-paths/foundations/code/ research/tests/ -q
.venv/bin/python -m pytest portfolio/reference-project/tests/ -q
.venv/bin/python portfolio/reference-project/evals/run_evals.py --report /tmp/etise-regression.json
.venv/bin/python research/validate_evidence.py
```

The foundations tests exercise unchanged-ID replay, conflicting updates, transaction rollback, SQL parameters, and invalid inputs. The API tests exercise requests and failures. The regression runner reports category, severity, routing, required documents, exact quotes, and failures, then exits nonzero if its gates fail.

Expected: tests execute with nonzero counts and pass; the regression report has `cases: 25` and `passed: true`. The source check includes both dated ledgers and reports failed retrievals explicitly. A failed source retrieval is different from a failing local accounting check. Check the report's evidence-status and latency-scope fields before interpreting a score.

## Understand what those results prove

| Observation | Valid conclusion | Conclusion it cannot establish |
|---|---|---|
| Five source metadata records import twice without doubling | This local import handles an unchanged replay | Distributed exactly-once effects |
| All five records have one product category | This selected sample has narrow coverage | All consumers have the same problem |
| Twenty-five known contracts pass | These known regression behaviors pass | Unseen customer accuracy or an independent holdout result |
| A sample-policy quote matches exactly | The cited text exists in that sample section | Legal authority, answer completeness, or a true statement about a company |

The test inputs that deliberately corrupt a record are authored contract tests. They do not increase the real dataset size or become new observations.

## Try it yourself

1. Write a test for your own counting function from Lesson 1, using the actual retained records. Do not merely run tests for the worked reference and claim your implementation passed.
2. Temporarily change your scratch function to count an item twice. Confirm that your assertion fails. Repair it and keep the rerun result. Leave the repository reference unchanged.
3. Copy the [customer brief worksheet](customer-brief-template.md) into `learning-artifacts/customer-brief.md`. Fill in source dates, limitations, actual commands/results, and missing user evidence.
4. Ask a peer to reproduce the import and explain the repeat behavior. Label the walkthrough as peer practice; record one confusing step and improve it.

## Debugging check

If pytest reports zero tests, check the directory and the `test_` filenames; zero is not a passing exercise. If an evaluation fails, inspect its failure list. If you changed an expectation, explain the intended behavior first; changing a label only to get green checks defeats the evaluation.

If you stop the API, its queue, feedback, metrics, and replay cache disappear. SQLite data survives in its file, but this exercise supplies no backup, restore service, or retention policy. State those differences in your handover.

## Exit check

- [ ] A peer can run your own script, repeat the import, and understand one rejected input.
- [ ] A deliberate defect makes a check fail; the repaired version passes.
- [ ] Your brief separates actual observations, assumptions, and unrun production work.
- [ ] You can explain why a customer holdout and authenticated authority are still missing.

Next: use the [software-engineer route](../from-software-engineer.md) when your programming foundations are comfortable, or the [expert practicum](../expert-fde-practicum.md) when you can already ship and operate services.

## Related documents

- [Reference runbook](../../portfolio/reference-project/docs/SLA_RUNBOOK.md) - available local recovery behavior
- [Presenting projects](../../portfolio/03-presenting-projects.md) - communicate the result without expanding its guarantee
- [Interview practice](../../interviews/README.md) - preparation material with declared provenance limits

## Further reading

- [Pinned pytest getting-started source](https://github.com/pytest-dev/pytest/blob/cf470ec0bf7eb89cd97dd56df4859eae5db46447/doc/en/getting-started.rst) - assertion-based testing, inspected 2026-10-11
