# A Debugging Methodology for FDEs

For FDEs and any engineer fixing a production system they did not build while the
customer watches. In an FDE engagement, debugging happens on systems you did not write,
in environments where you cannot see everything, with the sponsor reading over your
shoulder. A structured method is what separates calm resolution from flailing, and
flailing in front of a customer is expensive in trust (interpretation from practice;
the trust mechanics are covered in
[managing expectations](../customer/04-managing-expectations.md)).

The method is seven moves, run roughly in order. Most bad incident responses are order
failures: hypothesizing before bounding impact, fixing before reproducing, root-causing
while customers bleed.

- Stabilize first - stop the bleeding before the analysis
- Build the timeline - turn "it randomly breaks" into dated events
- Narrow the surface - binary search the request path
- Form hypotheses, test cheaply - top three candidates, cheapest test first
- The LLM-specific debug loop - treat quality regressions like code regressions
- Communicating during the incident - updates on a clock, facts labeled as facts
- After the fire - postmortem, evals, runbooks, and the pattern library

## The first hour

### Stabilize first

Do four things before any analysis:

1. Reproduce the failure, or classify it as unreproducible and say so out loud. An
   intermittent bug you cannot reproduce is a different project from one you can, and
   pretending otherwise burns hours you will later have to explain.
2. Bound the impact. Who is affected, how many, since when, and what data is wrong.
   "The assistant gives wrong answers" and "3 of 40 pilot users see stale refund
   policies since Sunday" are different incidents with different audiences.
3. Decide whether to mitigate or root-cause first. The rule we recommend: mitigate when
   customers bleed. Restore from backup, roll back the deploy, disable the feature, or
   fall back to the manual process, and only then investigate. Root-causing a live
   incident that mitigation could have stopped is heroics, not engineering.
4. Apply the rollback bias. If a recent change is suspect, reverting is evidence. A
   revert that fixes the problem proves the change caused it; a revert that does not
   eliminates a hypothesis. Either way, you learned it faster than by reading code.

Write the answers down as you go; under stress, memory is the first casualty, and the
timeline below depends on timestamps.

## Reconstructing history

### Build the timeline

Every incident gets an event table: what changed, when, who noticed, and what else
happened around then. Keep it in the shared incident document, not in your head. A
typical early version:

| When | What changed | Who noticed | What else happened |
| --- | --- | --- | --- |
| Sun 23:40 | Weekly data refresh ran | Job dashboard | Refresh job config edited Thursday |
| Mon 06:15 | First user complaints | Support lead | Monday peak load started |
| Mon 09:02 | Incident declared | FDE | No deploys since Friday |

"It randomly breaks" almost always means an undated timeline. Once every relevant event
has a timestamp, randomness usually collapses into correlation: the breakage started
when the refresh job changed, when the provider shipped a model update, or when the
warehouse moved region.

Correlation discipline: time overlap is not causation, but deploy-to-incident ordering
is strong evidence. A deploy that precedes the first failure by minutes is a suspect;
one that has been in production for two weeks while failures started this morning is a
weaker one. Rank suspects by how tightly they bracket the first bad event, and check
what else moved in the same window: config changes, upstream releases, provider model
updates, data refreshes.

## Finding the failing stage

### Narrow the surface

Deployments fail in stages, so debug in stages. Binary search the request path: did
input parsing fail, did retrieval return the wrong context, did the model call fail or
hallucinate, did post-processing mangle the output, or did the downstream system reject
the write? Each answered question cuts the search space in half.

Traces and structured logs answer these questions in seconds when they exist and in
hours when they do not. The instrumentation that makes this work - spans per stage,
request IDs propagated end to end, structured log fields instead of prose - is covered
in [monitoring and reliability](../ai/04-monitoring-and-reliability.md) and the
[OpenTelemetry documentation](https://opentelemetry.io). If the customer's system lacks
it, do not wait for a platform project: instrument your side and log the boundary
contracts - exactly what you sent, exactly what you received, with IDs. Half of all
cross-system bugs surrender to two logs that face each other.

### Form hypotheses, test cheaply

Once the surface is narrow, write down the top three hypotheses. For each, name the
cheapest test that would discriminate it from the others:

- Hypothesis: the retrieval index is stale - cheapest test: query the index directly for
  a fact you know changed last week
- Hypothesis: the model version changed under you - cheapest test: pin the previous
  version and replay one failing case
- Hypothesis: a prompt edit broke output parsing - cheapest test: diff the prompt
  against the last known-good revision

Run the cheapest test first, not the most likely one. Two cheap tests often beat one
expensive one, and cheap tests keep you gathering evidence instead of performing
conviction.

Two disciplines keep this honest. First, the log-and-assert sweep: before running new
experiments, re-read the logs and assertions you already have; the answer is already on
disk more often than anyone expects. Second, resist the fix-first instinct. Shotgun
fixes - change the prompt, bump the temperature, restart the pod, all at once - sometimes
work, and when they do, they destroy the evidence trail. You will not know which change
fixed it, the bug will come back, and the next incident starts from zero.

## Debugging probabilistic systems

### The LLM-specific debug loop

LLM failures rarely crash; they degrade. The loop adjusts accordingly:

1. Pull failing examples - not "accuracy dropped", but the twenty actual requests that
   went wrong this week
2. Classify them into an error taxonomy - bad retrieval, wrong format, wrong reasoning,
   stale data, prompt regression. Different categories have different owners and
   different fixes; a mixed pile is undiagnosable
3. Check whether the golden-set eval reproduces the failure - if the eval catches it,
   you have a reproducible bug and a regression test for free; if it does not, the eval
   set is missing a category, which is itself a finding. Building that eval set is
   covered in [evaluation and testing](../ai/03-evaluation-and-testing.md)
4. Bisect the context - remove retrieved chunks, strip conversation history, swap the
   model version, until the failure appears or disappears
5. Fix at the source the bisection found, not at the symptom

Treat a quality regression like a code regression: bisect the diff. Something changed -
the prompt, the model version, the chunking parameters, the data, the retrieval config -
and each of those has a last known-good version to diff against. "The model got worse"
is a hypothesis, not a diagnosis; "quality dropped the day the provider swapped the
served model version behind the same endpoint" is one you can act on.

## People and process

### Communicating during the incident

Send updates on a clock, even with no news: "still narrowing, next update in 30 minutes"
is a real update. Silence reads as hiding, and the customer fills it with worse
assumptions than the facts would have given them - the same first-hour rule as
[managing expectations](../customer/04-managing-expectations.md). Label everything:
"fact: requests since 09:02 are failing" versus "speculation: the weekend refresh is
involved, unconfirmed". Speculation labeled as speculation is useful; speculation dressed
as fact costs you the room when it breaks.

End every incident with a write-up. The five-section template we recommend:

```
Impact:     Who was affected, for how long, and what data was wrong.
Timeline:   Key events with timestamps, in one table.
Root cause: The technical cause, in two sentences.
Fix:        What was done, and when it was verified.
Prevention: What changes so this class of failure cannot recur.
```

Aim for half a page. The test: the sponsor can forward it to their boss without a
translation call.

### After the fire

The postmortem is an engagement artifact, not an internal chore. Run it blameless - the
question is why the system allowed the failure, not who typed the wrong command - and
share a customer-appropriate version with the sponsor. A customer who receives an honest
half-page postmortem trusts the next launch more; a customer who receives silence treats
every later wobble as a cover-up. This is interpretation, but it is the cheapest trust
purchase available after an incident.

Then feed the failure into the system that should have caught it:

- Add the failing cases to the eval set, so the same regression is caught before
  customers see it
- Write or update the runbook entry, so the next responder starts at step four instead
  of step one
- Check the failure against the [common failure modes](03-common-failure-modes.md)
  catalog - most incidents are a known pattern wearing a new costume

Finally, the pattern-library habit: keep a running list of incident patterns across
engagements. The first incident of a kind is tuition;
the second is reinforcement; the third should end in a permanent fix - a guardrail, an
alarm, a design change - not a fourth. This suggests the real measure of debugging
maturity is not how fast you resolve incident one; it is whether incident three happens
at all.

## Related documents

- [Debugging customer systems](02-debugging-customer-systems.md) - what this method
  looks like inside someone else's organization: opaque systems, tickets, shared on-call
- [Common failure modes](03-common-failure-modes.md) - the catalog to check before
  forming fresh hypotheses
- [Monitoring and reliability](../ai/04-monitoring-and-reliability.md) - the traces,
  dashboards, and drift alarms that make the narrowing step fast
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - the golden-set eval
  that turns quality regressions into reproducible bugs
- [Managing expectations](../customer/04-managing-expectations.md) - the communication
  contract that incident updates feed into

## Further reading

- [Site Reliability Engineering](https://sre.google) - Google's SRE book; the postmortem
  and incident management culture behind the write-up template
- [OpenTelemetry](https://opentelemetry.io) - the tracing standard behind the
  stage-by-stage narrowing described here
