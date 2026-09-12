# Prototyping and Proof of Concepts

This is for engineers about to run a proof of concept inside a customer engagement. It covers how to scope a PoC so it can only succeed or fail on evidence, how to build it without wasting the work, and how to turn the result into a decision. The operating principle throughout: a PoC is an experiment that produces a decision, not a demo that produces applause.

Prototype and demo work is named explicitly in 29.0% of FDE job postings (146 postings from 94 companies scraped February-July 2026, independent job-scrape analysis), and it appears in far more engagements than the postings admit, because most enterprise AI purchases start with a PoC. That makes it the first time your engineering judgment becomes visible to the customer, and the first place an engagement quietly goes wrong.

## Scoping the experiment

### Before you build

Write down the question the PoC answers before writing any code. Good PoC questions are falsifiable and metric-shaped:

- "Can a retrieval-based answerer hit 90.0% grounded answers on our FAQ corpus, judged against our rubric?"
- "Does model X meet our p95 latency budget of 800 milliseconds inside our VPC?"
- "Can extraction reach 95.0% field-level accuracy on real invoices from the last 90 days?"

If you cannot phrase the question like that, you are not ready to build; go back to discovery and sharpen it.

Then agree the success criteria in writing with the customer: the metric, the threshold, the dataset, and who judges. An agreed criteria document converts a later disagreement into a reading exercise. Set a hard timebox - most teams run PoCs in 2-4 weeks (industry pattern) - because a PoC without a deadline starts competing with the production build it was supposed to justify. Finally, name the decision and the decider: what happens on a pass, on a fail, and on a partial result. "We will review the results" is not a decision process.

Instrument the PoC from the first run. Log inputs, outputs, latencies, and failures from day one: you will need that telemetry for the evaluation in week 3 and the decision memo in week 4, and retrofitting logging into a throwaway script is more work than writing it in.

### Throwaway vs scaffold

Two honest extremes exist:

- Pure throwaway code - the fastest route to an answer, with no maintenance pretense and no tests you will never need. The risk: the PoC succeeds and now someone wants it in production on Friday.
- Production skeleton from day one - nothing to rewrite later, integration risk found early. The risk: you carefully build the wrong thing slowly, because the question was still moving.

Most teams take the middle path: a production-shaped repository with disposable experiments inside it. The repo structure, deployment path, and configuration are real from week 1; the experiments (notebooks, scratch services, prompt variants) are throwaway files that never block a rewrite.

Separate what must be real early from what can be fake:

- Must be real - the auth path (it always takes longer than scheduled), the shape of the real data, and the deployment constraints of their network and runtime
- Can be fake - the user interface, scale, resilience, polish, and anything the decision does not depend on

### Real data early

The demo dataset lies. It is small, clean, and biased toward the easy cases, which is exactly why it was chosen. The first week on real customer data usually resets every assumption: fields are missing, distributions are skewed, and the "documents" turn out to be scanned faxes. Building on the demo set therefore answers a question nobody asked.

Anonymized and synthetic data both have a place, with trade-offs:

- Anonymized real data - preserves distribution and messiness, but tokenization can distort string shapes (lengths, formats) that downstream parsing depends on
- Synthetic data - fine for volume and pipeline tests, dangerous for realism because it encodes the assumptions of whoever generated it

Start the data access request in week 1 regardless of when you think you need the data. Access approvals, data protection addenda, and security reviews commonly take longer than the build itself. Treat data access as a dependency with its own critical path, not as an environment detail. And profile whatever arrives before building on it - see [data pipelines](03-data-pipelines.md) for the profiling triage.

## Running and reporting

### A 4-week PoC playbook

We recommend the following shape as a template, not a law. Compress or stretch it to fit the engagement.

1. Week 1 - access, data, walking skeleton. Get accounts, credentials, and the first real data extract. Deploy a walking skeleton end to end: a trivial version of the pipeline plus one endpoint, running in their environment. The goal is to surface integration and access risk while there is still time to escalate.
2. Week 2 - core loop on real data. Implement the core capability against real data and get a first crude metric, even if quality is poor. A working loop with a bad score is a PoC; a beautiful notebook without one is a risk.
3. Week 3 - evaluation and edge cases. Build the evaluation set with the customer, run it systematically, and log every failure with a concrete example. This is the week the PoC becomes an experiment instead of a demo.
4. Week 4 - hardening and the decision write-up. Fix what the evaluation exposed, re-run, and write the decision memo. Present it to the decider named before week 1.

Each week has an exit criterion. If week 2 ends without a working core loop on real data, cut scope rather than extend the timebox - the deadline is what makes the result decision-grade.

### Presenting the results

Present findings as a decision memo, not as a screen recording. The structure that works:

- What we tested - the question, success criteria, dataset, and timebox, restated from the week 1 agreement
- What we found - the numbers against each criterion, including negative results; a PoC report with only good news is advertising
- Options - build, buy, or drop, with trade-offs and a rough effort band for each
- Residual risks - what the PoC did not test and what could still invalidate the result
- Recommended next phase - scope, duration, cost band, and the date of the next decision

Apply the audience test before you present: the sponsor should be able to repeat your finding to their boss in one sentence. If they cannot, the memo is not done. For example: "A retrieval-based answerer reached 92.0% grounded answers on our FAQ corpus within the agreed rubric, and the team recommends a six-week production pilot."

Brief the decider before the meeting. A short pre-read conversation surfaces objections while you can still address them; a hostile question in the meeting itself is a failed PoC regardless of the numbers.

### Failure modes

- The vaporware PoC - works only on the curated demo set and falls apart on anything else. Prevention: agree the evaluation set before building, sample it from real customer data, and report metrics on that set only.
- The infinite PoC - no decision date, so it absorbs work indefinitely and slowly becomes an unmaintained production system. Prevention: schedule the decision meeting before the first commit; if the question changes, restart the scoping conversation instead of silently extending the calendar.
- The demo overfit - prompts, thresholds, and retrieval settings tuned until the demo passes, then broken by live data. Prevention: hold out a slice of data the demo is never tuned against, and freeze the configuration before the final evaluation run.
- The moving-target PoC - requirements changed mid-run, so the result answers a question nobody asks anymore. Prevention: changes to success criteria go through the same written agreement as the original criteria, and every scope change visibly consumes the timebox.

## Related documents

- [Discovery and requirements](../skills/02-discovery-and-requirements.md) - where the PoC question, criteria, and dataset come from
- [Data pipelines](03-data-pipelines.md) - real data access and profiling are usually the critical path of a PoC
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - how to build the evaluation set the PoC is judged on
- [Prototype to production](../deployment/01-prototype-to-production.md) - what changes when the PoC becomes a production build
- [Managing expectations](../customer/04-managing-expectations.md) - demo expectations, and the gap between a demo and a result
- [Communication and storytelling](../skills/03-communication-and-storytelling.md) - writing the decision memo so executives act on it

## Further reading

- [Independent FDE job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md) - source of the 29.0% prototype and demo figure
- [Fortune: MIT report on GenAI pilot failures](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo) - why pilots without a production path fail (August 2025)
