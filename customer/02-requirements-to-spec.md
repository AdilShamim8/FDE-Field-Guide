# From Requirements to Spec

For the FDE turning discovery notes into an agreed document. The spec is where discovery
becomes a contract with the future: it is the artifact every later argument about scope,
quality, and dates gets settled against. Bad specs are the root cause of most failed
deliveries - and they fail quietly, weeks later, as rework, missed acceptance criteria,
and disputes with no reference document.

## Why specs fail

Four killers account for most spec failures. None announces itself at review time; all
surface during build, when they are expensive.

- **Ambiguity** - words that mean different things to different teams. "Handle the obvious
  errors" is a plan for a dispute: your engineer hears "retry and log", their QA lead
  hears "a documented recovery path per error class". Replace every such phrase with a
  number or a named example.
- **Invisible assumptions** - the ones you imported. Your spec says "nightly batch" because
  your last engagement was a nightly batch; their data team assumes streaming.
  Assumptions you do not write down cannot be corrected, only discovered.
- **Moving stakeholders** - the sponsor who signed the spec changes roles, and the successor
  reopens settled decisions. A spec without named sign-offs and a change process gives
  the successor nothing to inherit except an argument.
- **Unbounded scope** - "phase 1 should probably also..." with no non-goals section. Scope
  without explicit exclusions expands to fill the calendar; the non-goals list is the
  only sentence in the spec that buys you time.

## The four-tier enterprise specification chain

In mature enterprise engagements, a single informal document is insufficient to govern engineering delivery across business sponsors, enterprise architects, and implementation engineers. Forward deployed engineering teams structure specifications across four discrete tiers:

1. Business Requirement Document (BRD) - Defines the commercial and operational context. Answers what the business needs, why, what problems (P-1, P-2) are being solved, and what measurable criteria determine commercial acceptance. Signed off by the client executive sponsor (such as the Chief Operating Officer or VP of Operations).
2. Solution Design Document (SDD) - Defines the system boundaries, runtime component models, and cross-cutting architectural concerns. Answers what the system is made of, where components run (cloud VPC versus on-premise depot edge), why specific technologies were selected over rejected alternatives, and how security and data residency regulations are met. Signed off by enterprise architecture and InfoSec leadership.
3. Technical Design Document (TDD) - Defines the low-level implementation contracts. Answers how the software behaves at the API and schema level, detailing input validation rules, state machines, severity decision tables, technician ranking algorithms, error handling, and traceability matrices mapping every code function back to BRD requirement IDs. Signed off by the lead forward deployed engineer.
4. Production Code and Automated Test Suite - Implements the verified contracts and proves mathematical conformance against the traceability matrix.

## The one-page spec skeleton

Use this skeleton when there is nothing heavier to justify:

```markdown
# <Project> - Phase 1 Spec - v<n> - <date>

## Problem statement
<One paragraph: the measurable problem, the current baseline,
and where the numbers came from.>

## Goals
- <Outcome with metric and target, e.g. "routing accuracy at
  least 90.0% on the pilot dataset, measured weekly">

## Non-goals
- <What this phase explicitly will not do>

## Scope
- In - <capabilities, systems, user groups, environments>
- Out - <neighboring systems and features we will not touch>

## User stories and acceptance criteria
- As a <role>, I need <capability>, so that <outcome>.
  - Given <state>, when <action>, then <observable result>
  - Given <edge case>, when <action>, then <observable result>

## Non-functional requirements
- Latency - <budget at stated load>
- Data handling - <what may be read, stored, logged, sent externally>
- Audit - <what must be reconstructable, and for how long>
- Rollout control - <flags, phased groups, kill switch>
- Cost - <ceiling per unit at stated volume>

## Architecture sketch
<One diagram or five lines: components, where they run, data flows.>

## Rollout plan
<Phases, user groups, success bar per phase, abort criteria.>

## Open questions
- <Question> - owner <name> - due <date>

## Glossary
- <Customer term> - <definition in the customer's words>

## Sign-off
- <Name, role, customer> - <date>
- <Name, role, vendor> - <date>
```

When is one page enough? The rule we recommend: the document grows when the blast radius
grows. A pilot inside one team, on mock data, with no external data flows is fine at one
page. A spec that touches production customer data, a second system of record, or a
compliance boundary needs every section expanded, plus decision records and a rollback
plan. Length follows consequence, not the seniority of the audience.

## Acceptance criteria that survive contact with QA

Write behavior criteria in given/when/then form:

```gherkin
Given a ticket classified as billing with confidence 0.85 or higher,
when it enters the routing queue,
then it lands in the billing queue within 60 seconds,
and the routing decision is logged with model version and timestamp.
```

Three rules make criteria survive QA:

- **Measure, do not adjective** - "accurate" is a mood; "at least 90.0% of routed tickets
  reach the correct queue on the pilot set" is a criterion. Attach the dataset, the
  threshold, and the measurement method.
- **Edge cases are first-class citizens** - empty inputs, expired tokens, tickets in a
  language the model handles badly, and the customer's own top failure cases from last
  year. Criteria covering only the happy path are marketing.
- **Name the validator and the data** - who signs off, on what dataset, by when. A criterion
  nobody has agreed to verify is a wish.

## Non-functional requirements that matter in customer environments

Customers rarely ask for these and always notice their absence:

- **Latency budgets** - a suggestion needed in 200 milliseconds is a different system than
  one needed in 8 seconds; interactive means interactive at their peak load, not yours.
- **PII handling** - which fields the system may read, store, log, and send to external
  APIs; it is the first question their security team asks, so answer it in the spec.
- **Audit requirements** - who must be able to reconstruct what happened, and for how long
  the records must live.
- **Uptime and support windows** - what "down" means, who gets called, and whether your
  on-call covers their Monday morning.
- **Rollout control** - feature flags, phased user groups, and a kill switch; the customer
  wants the system turn-off-able faster than it was turned on.
- **Cost ceilings** - a cap per ticket or per query, because a system that works brilliantly
  at $4 per ticket is a failed project at their volume.

## The review ritual

The review meeting is part of the spec. We recommend this shape:

1. **Send the spec 24 hours ahead**, and state clearly that formal sign-off is the meeting's sole output.
2. **Open with 10 to 15 minutes of silent reading** - the objections people write in the
   margins are not the ones they raise in the room.
3. **Walk the scope-out list first** - that is where the hidden disagreements and misaligned expectations live.
4. **Capture every objection as an open question with an owner and a date** - tracked but
   open beats resolved by silence.
5. **Close with named sign-offs and dates in the document itself**.

An emailed "looks good, let's go" from the sponsor is a signature in practice: paste it
into the spec with the name and date attached. Do not wait for a formal signature process
to appear.

## Change management

The spec is versioned: `requirements.md` in the shared repo with a changelog at the top,
or a dated document ID if the customer lives in a document system. Changes after sign-off
go through a change request with three fields: what changes, why, and the impact
statement. Impact statements speak in the schedule's own language: "adds roughly 2 weeks
and moves the pilot start past the December change freeze, so first results land in
mid-January." That sentence lets a busy sponsor make a real decision; "it's a small
change" does not.

No silent scope: work agreed verbally in a corridor is work that will be contested at
acceptance. If you build it, write it into the spec first.

---

## Worked specification using current repository evidence

This is a specification exercise, not a customer kickoff transcript or a deployed financial system. Reviewed 2026-10-09 against the current reference. The earlier customer volumes, misclassification rates, financial losses, approvals, and privacy incidents had no artifacts in this repository and are withdrawn as observed evidence.

### Available inputs

The [CFPB snapshot](../portfolio/reference-project/evals/real_data/cfpb_metadata_2026-10-09.json) contains five actual categorical complaint records received today. It supplies stable IDs and source category fields, not complaint narratives or ETISE severity/routing labels. Bitext's publisher describes its dataset as hybrid synthetic; it is excluded from the real-world-only evidence set.

The [reference application](../portfolio/reference-project/README.md) supplies local typed intake, sample retrieval, exact quote checks, replay behavior, and operator review. It does not supply authenticated service tokens, customer SLA terms, automatic credits, Prometheus integration, PII sanitization, durable audit logs, a shadow-mode switch, or measured 50-RPS performance.

### Reviewable requirements and current evidence

- Given an unchanged ticket and the same declared account, role, and key, a replay returns the cached result. Changing the payload returns 409. Existing API tests exercise both behaviors.
- Given concurrent identical deliveries to one local process, classification executes once and subsequent requests replay. This is not a claim about multiple workers or durable effects.
- Given absent verified evidence in strict mode, dispatch is withheld and the ticket routes to review. P0 escalation remains separate.
- Given a caller omits roles, the default filter is `support_tier1`. Caller-supplied `admin` remains possible, so production authentication and tenant authorization are required work.
- Given a field exceeds the schema limit or an operator action is invalid, validation rejects it. An ingress byte limit and queue retention are still missing.

### Open acceptance decisions

A real customer must supply the baseline workflow, approved policies, representative labeled holdout, loss function, operator capacity, identity mapping, retention requirements, and workload measurements. Numeric quality and latency targets are proposals until agreed with those inputs. A local fixture score is not a customer acceptance signature.

Keep legal obligations distinct from sample Apex section numbers. GDPR Article 11 is not the sample policy's Section 11.3. Regulatory deadlines and jurisdiction-specific requirements need source-level review rather than a generic rule based on ticket dollar amount.

## Related documents

- [The engagement lifecycle](01-engagement-lifecycle.md) - where this document sits:
  Phase 4 (Architecture & Spec), with Phases 6 through 9 standing on it
- [Working in customer environments](03-working-in-customer-environments.md) - how to navigate
  customer infrastructure, bastions, and security reviews during spec execution
- [Managing expectations](04-managing-expectations.md) - how to handle scope pushback, trade-offs,
  and stakeholder alignment around spec commitments
- [Discovery and requirements](../skills/02-discovery-and-requirements.md) - how to
  gather the raw material and metrics this spec is written from
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - how the acceptance
  thresholds get measured once the pilot starts
- [Trade-offs and decision records](../system-design/03-trade-offs-and-decision-records.md) -
  where the architecture constraints behind the spec get recorded and challenged
- [Reference Project Implementation](../portfolio/reference-project/README.md) - full working code,
  test suite, and dataset provenance backing this specification

## Further reading

- [Anthropic Forward Deployed Engineer Guide](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) -
  emphasizes rigorous discovery and technical translation as core competencies
- [AWS Service Level Agreements](https://aws.amazon.com/legal/service-level-agreements/) -
  reference framework for enterprise SLA definitions and credit calculation formulas
- [CFPB Consumer Complaint Database API](https://www.consumerfinance.gov/data-research/consumer-complaints/) -
  public empirical repository of enterprise consumer disputes and compliance disclosures
