# Evaluation and Testing for LLM Systems

For FDEs who have to answer the customer's hardest question: how do we know it works?
Evaluation is the most transferable AI skill you can bring to the role, because it is
what turns a demo into a deployable system. The evidence is consistent: evaluation,
testing, and monitoring appear in 49.0% of FDE postings (146 postings scraped
February-July 2026,
[independent job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)),
Anthropic lists evaluation frameworks among its required production LLM experience
([Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008),
viewed 2026), and a MIT NANDA study found roughly 95% of enterprise GenAI pilots delivered
no measurable P&L impact (MIT NANDA, The GenAI Divide: State of AI in Business 2025, via
[Fortune](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo),
August 2025). This suggests most failed pilots never defined "good" as a number. This
document gives you the dataset, the metrics, the judge, the regression harness, and the
report.

## The golden dataset

Build it during discovery, from the customer's real data, anonymized. Synthetic data
fills gaps and covers hostile cases, but it cannot be the foundation: the input
distribution is the hard part of the task, and only real data carries it. The shape we
recommend:

- 50 to 200 real cases beats 5,000 synthetic ones early - a small set you can label,
  defend, and rerun in minutes outperforms a large one nobody trusts. Grow it from
  production later (see [monitoring and reliability](04-monitoring-and-reliability.md))
- Include the weird tail - empty inputs, hostile inputs (prompt-injection attempts,
  gibberish), bilingual or mixed-language records, broken encodings, edge formats.
  Reserve roughly a tenth of the set for these; launches fail here, not on the happy path
- Pull in the customer's own historical failures - last year's misrouted tickets and
  wrong answers are the most valuable cases in the set, and requesting them signals
  seriousness
- Label every case - source, difficulty, expected result or rubric. Labels turn aggregate
  scores into slices, and slices are how you find the failure the average hides
- Keep a held-out slice - cases the team never optimizes against, run at milestones.
  Overfitting to your own evaluation set is real and invisible from the inside

Version the dataset like code: a changelog, dated additions, and a note on why each case
was added. The set is an artifact the engagement argues with for months - acceptance
thresholds reference it, change requests touch it, and the customer's auditors may ask
where the numbers came from. An unversioned set makes all of that unverifiable.

## Task metrics

Pick metrics per pattern. A single score hides exactly what the customer will feel:

| Pattern | Core metrics | What the average hides |
| --- | --- | --- |
| Extraction | field-level exact match, error taxonomy | hallucinated fields in rare formats |
| Classification | per-class precision and recall | the expensive rare class |
| RAG | retrieval hit rate, groundedness, answer correctness | retrieval misses posing as generation errors |
| Summarization | rubric scores, human edit distance | fluent text that missed the point |
| Agents | task completion, steps and cost per task | budget creep |

Two wrong-metric shapes to refuse. First, "it looks good": no number, no dataset, no
rerun - a mood, and moods do not survive staff changes or handovers. Second, accuracy on
an imbalanced dataset: if 95% of tickets are not escalations, a router that never
predicts escalation scores 95% accuracy while catching zero escalations. The honest
baseline is per-class metrics plus an error taxonomy - every failure assigned a cause
category - and the taxonomy doubles as the backlog: each category with material volume
becomes a fix with a name.

Two practical additions. For RAG, evaluate the retrieval step on its own: label which
chunks should have been retrieved, measure hit rate, and only then score the generated
answer - otherwise a wrong answer tells you nothing about whether retrieval or generation
failed, and the two have opposite fixes. For anything with a confidence score, route by
it: high confidence flows to automation, low confidence flows to a human, and the
customer sees the threshold as a dial they can turn, which makes the launch conversation
shorter.

## LLM-as-judge

Exact match runs out of road for open text: a summary and a RAG answer each have many
defensible forms. An LLM judge scores them at scale, but only after calibration.

- Rubric design - explicit criteria, a small scale (1 to 5) with named anchors ("5 =
  answers the question with correct citations; 3 = answers but cites nothing"), and
  few-shot anchor answers at each score level. A judge without anchors scores vibes
- Calibration - run the judge against a human-labeled sample and measure agreement
  before trusting it, then re-measure periodically. Report the agreement rate; a judge
  nobody calibrated is a random number generator with good prose
- Known failures - judges drift as prompts and models change, and self-preference is
  commonly observed: judges favor outputs from their own model family or style. Watch
  for both when the judge and the system share a provider

The practical rule we recommend: judges triage, humans certify. Use the judge to score
every run and flag the worst decile for human review; use human review as the acceptance
gate for anything the customer signs off on.

## Regression testing

An LLM change is a code change and gets the same discipline: every prompt change, model
change, retrieval-configuration change, or context-construction change runs the golden
set before it merges. Wire the set into CI so the harness runs like any other test
suite, and treat a red evaluation run exactly like a failed build.

- Version pinning - pin model versions and prompt versions, and record both with every
  result. Unpinned, your evaluation history is uninterpretable
- Provider upgrades - a provider silently updating a served model is a production
  incident vector, not an automatic improvement. Run the golden set before accepting an
  upgrade, and put the runs on a schedule, because upgrades arrive whether you watch or
  not (the operating loop is in
  [monitoring and reliability](04-monitoring-and-reliability.md))
- The pre/post table - every accepted change carries a before-and-after table of
  metrics, and that table goes into the decision record, so "why did we change this" has
  an answer months later (see
  [trade-offs and decision records](../system-design/03-trade-offs-and-decision-records.md))
- Keep the artifacts - store each run's scores and failing cases so regressions are
  comparable across months, not just across branches

One caveat: the system itself is stochastic. Fix temperature at zero or its equivalent
where the provider allows, and where sampling still varies, run the set twice and treat
the range - not the single score - as the result. A change that moves the score by less
than the run-to-run range is noise, and calling it a win is how teams talk themselves
into regressions.

## Proving quality to a skeptical customer

The deliverable is not a score; it is a report a skeptical reviewer can interrogate.
Shape it like this:

- Dataset description - where the cases came from, how many, how they were labeled, and
  what the held-out slice is
- Metrics with sample sizes - scores sliced by category, not one aggregate number
- Error taxonomy with real examples - every major failure category with two or three
  anonymized cases; showing failures is what builds trust, because a report with no
  failures reads as marketing
- Known limitations - what the system does badly today, in writing. You will be asked;
  answering first is cheaper

Two moves make the numbers land. Co-own the dataset with the customer's subject-matter
experts: they contribute edge cases, review labels, and consequently trust the scores -
numbers people helped build are numbers people accept. And pre-agree the acceptance
thresholds in the spec, with the dataset and measurement method named
([requirements to spec](../customer/02-requirements-to-spec.md)). When the threshold was
signed during requirements, launch is a measurement; when it was not, launch is a
debate, and debates at launch are lost by the builder.

## A starter evaluation checklist

- [ ] 50 to 200 golden cases built from anonymized customer data, historical failures included
- [ ] Roughly a tenth of cases are hostile, empty, bilingual, or otherwise weird
- [ ] Every case has an expected result or a rubric a human can apply
- [ ] Metrics are per pattern: field exact match, per-class precision and recall, retrieval hit rate, groundedness, task completion
- [ ] A held-out slice exists that nobody optimizes against
- [ ] Any LLM judge is calibrated against human labels, with agreement rates reported
- [ ] The golden set runs in CI on every prompt, model, retrieval, or context change
- [ ] Model and prompt versions are pinned and recorded with every run
- [ ] Acceptance thresholds are pre-agreed in the spec, with dataset and measurement method named
- [ ] An evaluation report exists: dataset description, metrics with sample sizes, error taxonomy with examples, known limitations

## Related documents

- [LLM application patterns](01-llm-application-patterns.md) - the patterns these metrics measure, and the simplest-pattern rule
- [Agents and tools](02-agents-and-tools.md) - trajectory and outcome evaluation for agent systems
- [Requirements to spec](../customer/02-requirements-to-spec.md) - where acceptance thresholds and measurement methods get signed
- [Trade-offs and decision records](../system-design/03-trade-offs-and-decision-records.md) - where pre/post evaluation tables live
- [Prototyping and PoCs](../engineering/01-prototyping-and-pocs.md) - success criteria written before the PoC starts
- [Monitoring and reliability](04-monitoring-and-reliability.md) - what happens to the golden set after launch

## Further reading

- [AI Engineering Field Guide](https://github.com/alexeygrigorev/ai-engineering-field-guide) - the reference field guide this repo follows; treats evaluation as the most important new skill in AI engineering
- [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) - evaluation frameworks named among required production LLM experience
- [MLflow](https://mlflow.org) - experiment and evaluation run tracking, useful when the customer wants a platform
- [Fortune on the MIT NANDA report](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo) - the pilot-failure finding behind the define-good-numerically argument (August 2025)
