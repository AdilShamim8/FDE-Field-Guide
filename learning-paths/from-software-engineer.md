# From Software Engineer to FDE

The most common transition into FDE work, and structurally the cheapest: you already
have the production half, and the FDE job adds the customer arc - discovery,
requirements, stakeholder work, and delivering inside someone else's environment instead
of your own. An independent job-scrape analysis of 146 FDE postings from 94 companies
(February-July 2026) found building production systems in 90.0% of postings and direct
customer work in 88.0% (observed evidence). You arrive native in the first and trainable
in the second; most other candidates have it the other way around.

## What You Already Have

- Production coding - the core of the 90.0%; you write code that survives review and
  operates in real environments, not just demos
- Testing and CI/CD - 34.0% of postings name CI/CD explicitly and every posting assumes
  it silently; this is assumed baseline, not differentiator
- Deployment experience - services shipped into environments with real failure modes,
  real users, and real consequences
- Debugging under pressure - on-call or its equivalent: finding root causes without
  perfect information, sometimes at inconvenient hours
- Written incident communication - the status update you write during an outage is, in
  structure, the customer status update FDEs send weekly; you have written more of them
  than you give yourself credit for
- Code review and technical writing for engineers - the dialect of specs and decision
  records is closer to this than you expect

## What You Need to Learn

- Discovery and requirements gathering - the biggest gap; 52.0% of postings list scoping
  and discovery as FDE work, and most engineers have only ever received requirements,
  never extracted them (see [discovery and requirements](../skills/02-discovery-and-requirements.md))
- Stakeholder and expectation management - sponsors, skeptics, and approvers who do not
  read pull requests; a slipping demo is an engineering moment, not a social one
- Customer-facing documents - specs, status updates, and postmortems a non-engineer can
  act on; shorter and more decisive than internal design docs
- The AI/LLM layer, if you do not have it - LLM APIs with structured outputs, RAG
  (52.0% of postings), and evaluation discipline (49.0%); see
  [LLM application patterns](../ai/01-llm-application-patterns.md) and
  [evaluation and testing](../ai/03-evaluation-and-testing.md)
- Integration craft in unfamiliar environments - 64.0% of postings list integration,
  which in practice means auth flows you did not design, schemas you did not model, and
  rate limits you did not set (see
  [APIs and integrations](../engineering/02-apis-and-integrations.md))

Two engineer reflexes need retraining rather than new knowledge. The first is jumping
to solutions: when a customer describes a problem, the engineer reflex is to open an
editor, while the FDE reflex is to ask what happened the last three times and who owns
the workaround today. The second is debating requirements in the abstract - "that does
not make sense" - instead of writing down the disagreement, its cost, and the cheapest
experiment that would resolve it. The discovery and ambiguity documents in the skills
section cover both.

## What to Skip

- Another web framework - you can already learn frameworks on demand; a third one adds
  no signal an interviewer cares about
- Advanced algorithm study - practitioner reports describe FDE loops as reasoning about
  real systems, not collecting puzzles
- Deep infrastructure specialization - FDEs operate and extend infrastructure inside
  customer environments; they rarely build platforms, and a certification farm does not
  move the needle
- Side projects that duplicate your day-job stack - a greenfield to-do app proves
  nothing new; ambiguous requirements and a real user are the point

## Projects to Build

The theme across all three is integration, not greenfield: the FDE delta is delivering
inside constraints you did not choose. For twelve full specs, see
[project ideas](../portfolio/02-project-ideas.md).

### An LLM feature inside an existing system

Build and deploy a working LLM feature into an existing open-source project you use, or
a friend's business system. Their stack, their constraints, their users, their review.
It is FDE-shaped because delivering inside a codebase and organization you do not
control is the daily condition of the job. It proves you can add a probabilistic feature
to a deterministic system without breaking either. Scope it to one workflow and
instrument it from day one - the monitoring is part of the deliverable, not a later
phase.

### A mini-engagement for a real small client

Run a two-to-four-week engagement for a real client - a local business, a nonprofit:
discovery interviews, a written spec, delivery, a handover document, and a follow-up
review two weeks later. Charge nothing if you have to; do not skip the paperwork. It is
FDE-shaped because it exercises the full customer arc, including the parts engineers
usually delegate to someone else. It proves you can turn an ambiguous ask into a signed
spec and a working deliverable. Write the follow-up review as a before-and-after
comparison; that single document is your strongest interview artifact.

### An integration feature in a product you use

Contribute a connector, webhook handler, or import/export feature to a product you use,
with tests and documentation. It is FDE-shaped because it means working against APIs you
do not own, with code review from strangers who owe you nothing. It proves your code
survives review by people with no reason to be kind. Publish the design notes next to
the code; the notes are often what interviewers actually read.

## Suggested Path

1. Point yourself at the right destination - read
   [responsibilities](../role/02-responsibilities.md) and
   [the FDE loop](../role/05-the-fde-loop.md) so you practice the job, not an imagined
   version of it
2. Close the AI layer if it is missing - 4-6 weeks on LLM APIs, structured outputs, RAG,
   and a first evaluation harness, using the engineering habits you already have;
   resist the urge to build infrastructure before you can evaluate outputs
3. Practice discovery deliberately - run three interviews with real people about real
   workflows using the question bank in the skills section, and write a one-page problem
   statement from each; the interviews feel awkward the first two times, which is the
   point of doing them before a customer is paying
4. Build the integration project - the LLM feature inside an existing system, with
   monitoring and a runbook, deployed somewhere that is not your laptop
5. Run the mini-engagement - spec, delivery, handover, follow-up; treat the client as a
   customer, including the uncomfortable conversations about scope and slippage
6. Convert everything to evidence - write-ups following
   [presenting projects](../portfolio/03-presenting-projects.md), then prepare for the
   interview loop's customer-scenario rounds

## Timeline

2-4 months of focused preparation on top of a real engineering background. Estimates for
software engineers picking up the AI engineering layer commonly run 2-3 months (industry
pattern); the customer-skill layer is what turns that into FDE readiness, and it needs
practice you cannot cram. Assumptions: 5-10 hours per week, existing production
experience, and the AI layer genuinely new to you. If you already work with LLMs at
work, expect 1-2 months; if your current role has zero customer exposure, lean toward 4
and make the mini-engagement non-negotiable. One warning: reading about discovery feels
like progress and is not - the hours only count when spent on real interviews and the
real mini-engagement. This is an expert estimate, not a promise.

## Your Advantage

Production depth is the scarce half. The customer-facing market is full of people who
can run a demo and a meeting but have never carried a pager, written a test that caught
a real bug, or operated a service at 3 a.m. You hold the half that postings demand at
90.0% and that is hardest to fake in an interview. The direction of your learning also
works in your favor: engineering habits transfer into customer situations more readily
than customer instincts transfer into production engineering (expert interpretation).
You are also the profile postings name directly - Anthropic's FDE posting lists software
engineers with consulting experience among its fit criteria (observed evidence, 2026).
Your risk is the opposite of most candidates: underpricing the customer half because it
looks soft. It is not soft; it is merely untested for you until you run the interviews.

## Related documents

- [Responsibilities](../role/02-responsibilities.md) - the work you are adding, backed by
  the same posting evidence cited above
- [Discovery and requirements](../skills/02-discovery-and-requirements.md) - your biggest
  gap, with a question bank you can use tomorrow
- [APIs and integrations](../engineering/02-apis-and-integrations.md) - integration craft
  in environments you do not own
- [The engagement lifecycle](../customer/01-engagement-lifecycle.md) - the customer arc
  you are adding, phase by phase
- [FDE vs other roles](../role/03-fde-vs-other-roles.md) - where FDE sits relative to the
  adjacent roles you may be offered along the way
- [Customer scenarios](../interviews/04-customer-scenarios.md) - the interview round that
  tests the half you are building
