# Agents and Tools

For engineers building or reviewing agentic systems in customer environments. An agent is
an LLM that decides which tools to call and when: powerful, expensive per task, and the
wrong answer surprisingly often. The hiring market confirms the skill is core - AI agents
appear in 42.0% of FDE postings (146 postings scraped February-July 2026,
[independent job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)),
and Anthropic's FDE role lists MCP servers, sub-agents, and agent skills among its
deliverables ([Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008),
viewed 2026). This document covers the loop, tool design, MCP, when not to build an
agent, and the guardrails that make agents shippable.

## The agent loop

The loop is simple to state: the model plans, calls a tool, observes the result, and
repeats until it judges the task done. The engineering is in the boundaries. Every step
is a model call, so cost and latency scale with steps, and errors compound - a misread
tool result at step two becomes a confident wrong action at step five.

What actually ships in enterprises (industry pattern, not the demo shape):

- Bounded loops - a step limit and a wall-clock limit per run, with a defined give-up
  behavior: hand the partial state to a human, not to the void
- Human approval gates - risky or external actions (payments, emails, deletions) wait
  for a named person to approve
- Deterministic scaffolding - a workflow engine or state machine owns the control flow
  and the model fills in decisions inside it, so a confused model cannot wander the
  whole state space

We recommend defining "done" before the first run: what artifact the run produces, how it
is verified, and what stops it. An agent without a written stop condition is an unbounded
cost with a language model attached.

A concrete shape helps. A support agent with three tools - look up order, check refund
eligibility, draft reply - runs as: classify the request, call `get_order`, call
`check_refund_policy`, generate the draft, stop. Every step lands in a trace with its
inputs and outputs ([monitoring and reliability](04-monitoring-and-reliability.md)), so
when the draft is wrong you can see which step misled it. That trace-per-step visibility
is the minimum bar for running agents anywhere near customers.

## Tool design

Tools are APIs for a non-deterministic caller, and that changes API design. The caller
does not read your code - it reads names, descriptions, and parameter schemas, and it
improvises against them. What works:

- Small surface - few tools, one purpose each. Overlapping tools ("search tickets"
  versus "find tickets") produce coin-flip selection
- Names and descriptions written for a stranger - the description is the model's only
  documentation; state what it returns, what it does not cover, and when not to call it
- Typed parameters with explicit formats - "date in ISO 8601", "account ID as string, not
  number"; ambiguity here becomes runtime improvisation
- Actionable errors - "date must be ISO 8601, you sent 03/04/2025" lets the model recover
  in one step; "validation failed" triggers thrashing: retries, tool-switching, invented
  workarounds
- Idempotency for write tools - the loop retries, so writes must tolerate it; the same
  idempotency keys and deduplication rules as any integration
  ([APIs and integrations](../engineering/02-apis-and-integrations.md))
- Bounded results - paginate, cap result counts, and set timeouts on the tool itself, so
  one call cannot return ten thousand rows or hang the loop while the model waits
- Names in the customer's vocabulary - name tools after the customer's verbs and objects
  (`get_claim`, not `fetch_record_v2`), because the model reasons better about terms that
  match the domain language it was asked about

The error message is a prompt: that is the highest-leverage sentence in tool design, in
our experience. Models recover from good errors and thrash on bad ones, so write tool
errors the way you would write validation messages for a capable junior engineer you
cannot talk to.

## MCP

The Model Context Protocol (MCP) is an open standard for exposing tools and context to
models in a uniform way: a server advertises tools, resources, and prompts, and any
compliant client can discover and call them
([Anthropic documentation](https://docs.anthropic.com)). Instead of hand-wiring every
model application into every internal system, the customer wraps each system once.

MCP servers are now a concrete FDE deliverable, not a concept: Anthropic's FDE job
description lists MCP servers, sub-agents, and agent skills among its production
deliverables ([greenhouse posting](https://job-boards.greenhouse.io/anthropic/jobs/5302966008),
viewed 2026). The practical shape we see in engagements: a customer-internal MCP server
wrapping their systems - ticketing, CRM, warehouse - with permissions scoped at the
server. Permissions enforced in the server survive every client and every prompt;
permissions described in a prompt are suggestions.

What the server typically exposes:

- Tools - the actions the agent may take, each with typed parameters and actionable
  errors, designed by the rules above
- Resources - read-only context such as policy documents or record lookups the model can
  load without an action
- Scoped authentication - one credential set per upstream system, least privilege, with
  the audit trail landing in the customer's logging stack

Treat the server as production infrastructure: it inherits the customer's uptime
expectations, security review, and on-call, not the lighter standard of a prototype.

## When agents are the wrong answer

Most proposed agent projects fail one of these:

- Fixed workflow, no branching - use a pipeline with model calls at fixed steps; the
  control flow was never uncertain, so do not rent a model to guess it
- One structured call suffices - use extraction; if a single prompt plus a schema solves
  the task, the loop is overhead
- Untrusted environment without egress control - an agent that reads attacker-influenced
  text and can fetch URLs is an injection waiting for a target; the boundary design is in
  [security and compliance](../engineering/05-security-and-compliance.md)
- The customer cannot tolerate non-deterministic runtimes - regulated or safety-critical
  paths need deterministic behavior; put the model behind fixed steps or leave it out
- Nobody can say when it should stop - the one-line test: if you cannot describe when the
  agent should stop, it will not stop when it should

Cost is the quiet argument. An agent run is a bundle of model calls, so a task that costs
one call as extraction costs twenty as an agent. If the branching is imaginary, you paid
twenty times for nothing.

The design that usually wins is hybrid: deterministic pipelines carry the trunk of the
workflow, and the agent handles the ambiguous edges - the requests that do not match a
template, need three systems reconciled, or require judgment about which rule applies.
That shape gives the customer determinism where the volume is and flexibility where the
exceptions are, and it keeps the agent's cost and blast radius proportional to the share
of work that is genuinely unpredictable.

## Guardrails and permissioning

Guardrails are what make agents shippable; without them, the customer's security review
will. Build-side rules we recommend:

- Least privilege per tool - scoped database credentials, read-only defaults, per-action
  allowlists. The agent's database user is not the application's database user
- Output filtering before side effects - validate model output against schema and
  allowlist before it drives an API call, a write, or an outbound message
- Prompt injection treated as untrusted input - tool results and retrieved documents are
  attacker-controllable text; the enforcement boundary lives in the architecture, and the
  review-side detail is in
  [security and compliance](../engineering/05-security-and-compliance.md)
- Approval gates that log who approved - a gate without an audit record is theater; log
  approver, action, payload, and timestamp
- Egress control for anything that fetches - allowlisted destinations only, because a
  fetched URL is both an instruction channel and an exfiltration channel

## Agent evaluation

Agents need their own evaluation shape on top of output checks:

- Trajectory evals - did it call the right tools, in a sane order, without thrashing or
  redundant calls
- Outcome evals - did the task complete correctly, against the pre-agreed definition of
  done
- Cost and step budgets as regression metrics - steps per task and dollars per task drift
  upward silently; track them like quality, because they are quality

Run these on recorded trajectories, not just live traffic: capture real runs (with
sensitive content redacted), replay them against every agent, tool, or model change, and
diff the tool-call sequences. A change that alters trajectories but not outcomes is worth
a second look - it usually means the agent found a different, more expensive route to the
same answer.

The datasets, judge calibration, and regression harness behind these live in
[evaluation and testing](03-evaluation-and-testing.md); traces, the raw material for
trajectory debugging, live in
[monitoring and reliability](04-monitoring-and-reliability.md).

## Related documents

- [LLM application patterns](01-llm-application-patterns.md) - where agents sit in the pattern catalog, and the cheaper patterns to try first
- [Evaluation and testing](03-evaluation-and-testing.md) - trajectory and outcome evaluation in full
- [Security and compliance](../engineering/05-security-and-compliance.md) - the security review these guardrails have to pass
- [APIs and integrations](../engineering/02-apis-and-integrations.md) - idempotency, retries, and error taxonomy for the tools agents call
- [Debugging methodology](../troubleshooting/01-debugging-methodology.md) - tracing agent runs to root causes when they misbehave

## Further reading

- [Anthropic documentation](https://docs.anthropic.com) - tool use, MCP, and agent design guidance
- [OpenAI platform documentation](https://platform.openai.com/docs) - function calling and tools reference
