# Common Failure Modes

For FDEs operating customer-facing deployments and for engineers on call for them. This
is a short catalog of the failures that recur across engagements, each with the tell
(how it presents), the cause, and the fix or prevention. Reading it costs twenty
minutes; recognizing one of these in production saves days. The catalog is practitioner
knowledge (industry pattern tier), not measured frequencies - base rates vary by
industry and stack.

## The catalog

### Data failures

- Stale corpus - the tell is answers that reference old reality: last quarter's prices,
  retired policies, departed people. The cause is a refresh job that stopped, slowed, or
  silently shrank. The fix is a freshness check on the maximum source timestamp, with an
  alarm tied to the expected cadence; the pipeline-side design is in
  [data pipelines](../engineering/03-data-pipelines.md).
- Upstream schema drift - the tell is fields that are suddenly empty, or a metric that
  drops to zero overnight with no deploy. The cause is a column renamed, retyped, or
  moved upstream with no notice. The fix is schema validation at ingestion that rejects
  and alerts, plus a scheduled check against the live source schema.
- Duplicate ingestion - the tell is inflated metrics, or the assistant giving the same
  answer twice on one page. The cause is a batch loaded twice, usually after a rerun
  without idempotency. The fix is idempotent loads keyed on batch or event ID, plus a
  row-count delta alarm that catches sudden jumps.
- Encoding and timezone corruption - the tell is timestamps off by a fixed number of
  hours, or joins that silently miss. The cause is mixed UTC and local times, or
  encoding remnants that make `"gold "` and `"gold"` different join keys. The fix is
  store UTC and convert at display, validate encodings at the boundary, and test joins
  against known rows.

### Integration failures

- Expired credentials and quotas - the tell is intermittent 401s or 429s that cluster at
  busy hours or after weekends. The cause is a token lifetime nobody calendared, or a
  quota the workload outgrew. The fix is rotation tested until it is a non-event, plus
  client-side pacing against the granted quota.
- Webhook silence - the tell is a queue that starves with no error anywhere. The cause
  is delivery that is best-effort on their side and unmonitored on yours. The fix is a
  reconciliation poll that measures webhook lag, and an alarm when lag exceeds the
  window.
- Pagination truncation - the tell is results that quietly stop early, with everything
  looking healthy at half the volume. The cause is a cursor treated as an offset, or a
  page limit assumed instead of read from the response. The fix is a boundary test that
  walks every page until the API says stop, run on a schedule.
- Staging-versus-production confusion - the tell is a fix that works in testing and
  changes nothing in production, or a resource "missing" that everyone can see. The
  cause is config pointing at the wrong tenant, environment, or region. The fix is the
  environment stamped into every log line, and per-environment credentials so the wrong
  tenant fails loudly.

### LLM failures

- Retrieval misses - the tell is the model being confidently, fluently wrong, and right
  again when the answer is pasted into the prompt. The cause is the context: chunks
  missing, stale, ranked badly, or crowded out. The fix is debugging retrieval first,
  separately from the model; the model is usually the last suspect.
- Format regressions after prompt edits - the tell is a parser failure spike hours after
  a prompt change. The cause is an edit that fixed one example and broke the output
  contract. The fix is evals in CI: no prompt reaches production without a golden-set
  run; the eval design is in [evaluation and testing](../ai/03-evaluation-and-testing.md).
- Provider model silent upgrade - the tell is quality that shifts with no deploy, no
  config change, and no data change. The cause is the provider changing the served model
  version behind the same endpoint. The fix is version pinning where offered, a
  changelog subscription, and a scheduled eval run that catches drift independently of
  your own release cadence; provider release notes live at
  [Anthropic documentation](https://docs.anthropic.com) and
  [OpenAI documentation](https://platform.openai.com/docs).
- Context overflow after data growth - the tell is failures that start when the
  customer's data grows past a threshold, or answers that degrade as conversation
  history lengthens. The cause is a context window treated as infinite during the pilot.
  The fix is token budgets with written truncation rules, and an alarm on p99 prompt
  size before it reaches the limit.
- Prompt injection surfacing as weird answers - the tell is responses that follow
  instructions no user gave, usually traceable to retrieved content. The cause is
  untrusted text treated as instructions. The fix is architectural: treat retrieved
  content as data, never as directions; the review-facing guidance is in
  [security and compliance](../engineering/05-security-and-compliance.md).

### Infrastructure failures

- Egress blocked by org policy - the tell is a model API call that times out only inside
  the customer's network. The cause is a default-deny egress policy nobody mentioned,
  because it is someone else's normal. The fix is listing every external destination
  during architecture review, not at integration time.
- DNS and firewall asymmetry between environments - the tell is a service that resolves
  and connects in staging and fails in production with identical config. The cause is
  different network rules per environment, which is normal and undocumented. The fix is
  a connectivity probe per environment in the readiness checklist.
- Cold-start timeouts at low traffic - the tell is the first request after an idle
  period failing or crawling, while everything under load is fine. The cause is
  serverless scaling meeting an impatient timeout. The fix is a warmer, a provisioned
  floor, or latency numbers that honestly include the cold path.
- Cost alarms firing at 3am - the tell is a budget alert rather than an outage. The
  cause is a backfill, a retry storm, or an embedding job with no cost ceiling. The fix
  is budgets and alerts per environment from day 1, and scheduled heavy jobs run with
  the budget owner aware.

### Human-system failures

- Nobody owns the on-call - the tell is an alert firing into a void, discovered by the
  customer before the vendor. The cause is an alerting owner left implicit at launch.
  The fix is a named owner per component - yours until handover, theirs after - with the
  date the baton passes written down.
- The runbook never rehearsed - the tell is a recovery that takes four hours for a
  four-minute procedure. The cause is a runbook written once and never executed by
  anyone who did not author it. The fix is a rehearsal calendar: run the runbook
  quarterly, with a different person each time.
- The temporary manual step - the tell is an incident that only happens when one
  specific person is on leave. The cause is a "temporary" manual step that became
  load-bearing and undocumented. The fix is auditing for these during handover, then
  automating or deleting them before the engagement ends.
- The departed champion - the tell is questions that used to take one message now taking
  a week. The cause is the one person who knew the pipeline leaving with the knowledge
  in their head. The fix is writing decisions down while they are being made, and
  keeping the data inventory and runbooks current enough that no single departure is an
  outage.

## The meta-fixes

Four permanent defenses prevent most of the catalog. Install them during the
prototype-to-production crossing, not after the first incident
([prototype to production](../deployment/01-prototype-to-production.md)):

1. Evals in CI - catches format regressions, provider drift, and retrieval misses before
   customers do, and turns "quality feels off" into a diff
2. Freshness checks - catches the stale corpus and most silent data failures at the
   pipeline layer, where they are cheap
3. Boundary logging - catches schema drift, webhook silence, pagination truncation, and
   every cross-organization dispute, because the evidence of what crossed the boundary
   is already on disk
4. Named ownership - catches the on-call void, the unrehearsed runbook, and the manual
   step, because every component having a person turns the rest of the catalog into a
   checklist instead of archaeology

We recommend treating these four as the minimum production bar for any customer-facing
deployment: each is cheap to install and pays for itself the first time it fires.

## Related documents

- [A debugging methodology](01-debugging-methodology.md) - the method that turns a
  recognized failure into a confirmed cause and fix
- [Debugging customer systems](02-debugging-customer-systems.md) - what half of these
  look like from inside someone else's process
- [Data pipelines](../engineering/03-data-pipelines.md) - the ingestion and validation
  design that prevents the data failures
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - the eval practice
  behind the LLM defenses
- [Prototype to production](../deployment/01-prototype-to-production.md) - the crossing
  where the four meta-fixes get installed

## Further reading

- [Prometheus](https://prometheus.io) - the alerting model behind the freshness, lag,
  and budget alarms in this catalog
- [Anthropic documentation](https://docs.anthropic.com) - provider release notes; the
  subscription habit that defangs silent model upgrades
