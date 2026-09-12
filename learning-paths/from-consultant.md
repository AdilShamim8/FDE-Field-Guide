# From Consultant to FDE

You can run the room: discovery, stakeholder management, delivery under statements of
work, and executive communication. The FDE job adds hands-on engineering ownership - you
write the production code yourself, instead of specifying it, delegating it, and
reviewing it. The engagement arc is native to you; the engineering ownership is the
lift, and it is the biggest lift of the six paths in this section. Practitioner
comparisons put the difference crisply: consultants deliver on scoped SOWs with a
deliverable handoff, while FDEs own outcomes across the lifecycle, including the code
(industry pattern, from 2026 practitioner write-ups).

## What You Already Have

- Discovery and requirements elicitation - your core craft maps directly; 52.0% of the
  146 FDE postings in the job-scrape analysis used across this guide list discovery and
  scoping as the engineer's own job (observed evidence)
- Expectation management - scoped promises, early bad news, and sponsors who trust the
  next commitment because the last one held
- Commercial instincts - you know what an engagement costs and what a sponsor needs to
  justify it, which helps you scope FDE work to what survives a budget review
- Stakeholder mapping - sponsors, blockers, skeptics, and approvers are people you
  already work with by name
- Navigating client organizations - you know how decisions actually travel inside a
  company you do not work for
- Delivering bad news professionally - the skill that keeps engagements alive when the
  demo fails and the timeline slips

## What You Need to Learn

- Real production coding - `Python` (91.0% of postings) and services built with
  `fastapi`; not prototype scripts, but code that survives someone else's review (see
  [core technical skills](../skills/01-core-technical-skills.md))
- Version control discipline and CI/CD - branches, pull requests, and pipelines (34.0%
  of postings name CI/CD); the daily rhythm engineering trust is built on
- Cloud deployment basics - one cloud end to end, from container to bill; `AWS` appears
  in 47.0% of postings (see
  [cloud and infrastructure](../engineering/04-cloud-and-infrastructure.md))
- The AI/LLM application layer with evaluation - LLM APIs, RAG (52.0% of postings), and
  the evaluation sets that let you prove quality rather than promise it
- Engineering artifacts from the engineer's side - decision records, runbooks, and
  postmortems, which are the deliverables your decks used to be

A note on what "production" means, because consulting blurs it: a production system is
one a stranger depends on tomorrow morning without you in the room - deployed somewhere
persistent, monitored, documented, and revertible. A script you ran for a workshop is
not production, no matter how well it landed in the room. Hold your own projects to that
definition from the first commit.

## What to Skip

- More methodology certifications - the next framework rollout adds no engineering
  signal, and nobody will hire you for knowing it
- Deck engineering - slides are your old weapon; the new artifacts are specs and
  runbooks judged by whether a stranger can act on them
- Business-school reading lists - you have the business half; more of it is comfort
  spending that delays the coding practice
- Managing by deck - practice managing by artifact instead: code, tests, dashboards,
  and written decisions
- Engagement-economics study - scoping and selling the SOW is not the FDE's job; owning
  the outcome after the signature is

## Projects to Build

The theme is your name on the commits. For twelve full specs, see
[project ideas](../portfolio/02-project-ideas.md).

### A small, real production system for an actual client

Build and deploy a small but real production system for an actual client, with your name
on every commit. Small scope is fine - a booking flow, a reporting service, a document
tool - but production reality is not: tests, deployment, monitoring, and a handover
document. It is FDE-shaped because it is personal engineering output inside a client
organization, which is the FDE job in miniature. It proves you personally ship, not just
specify. A service one person relies on weekly beats a platform nobody uses; resistance
to scope inflation is part of the test.

### A manual process automated end to end

Take a client's manual process and automate it end to end, with monitoring and alerts,
and stay through the first month of real usage. It is FDE-shaped because outcomes, not
deliverables, are what FDEs own - the system has to survive contact with operations. It
proves you deliver into someone's daily work, not just against a statement of work. The
month of real usage is where the engagement skills you already have meet the reliability
skills you are building.

### The technical half of your last engagement

Write the spec, evaluation report, and runbook for your most recent engagement as if you
had engineered it yourself. It is FDE-shaped because it converts your consulting memory
into engineering artifacts - the exact dialect shift this path requires. It also
diagnoses you honestly: every section you cannot write is a skill gap with a name and a
document in this guide. Time-box it to a weekend; its purpose is diagnosis, not
delivery.

## Suggested Path

1. Baseline your coding honestly - run the self-audit in
   [core technical skills](../skills/01-core-technical-skills.md); expect it to be
   humbling and treat the result as your study plan
2. Rebuild coding fundamentals - `Python` with `pytest`, Git discipline on every
   project, then small services with `fastapi`; daily practice beats weekend marathons
   at this stage
3. Learn one cloud end to end - containerize a service with `Docker` and deploy it until
   you have a URL, a database, and a bill you understand
4. Add the AI layer with evaluation - structured outputs, a small RAG build, and an
   evaluation set; your consulting instinct for "what would the client accept as proof"
   is an asset here
5. Ship the client project - your name on every commit, a runbook, and a follow-up
   review after a month of real usage
6. Convert your artifacts - rewrite the decks and deliverables of your last engagement
   as a spec, two decision records, and a runbook
7. Prepare for the coding interview gate - your discovery and stakeholder rounds will go
   well; the coding round does not bend, so practice under time pressure, weekly

## Timeline

4-8 months depending on coding baseline, and be honest with yourself about the baseline:
this is the biggest lift in this section (expert estimate). The range assumes 8-12 hours
per week, a client or organization willing to take real software from you, and enough
weekly hours that momentum survives your day job. If you coded seriously in the past -
even years ago - expect 4-5 months for the rust to come off. If you have never written
production code, expect 8 months or more, and treat the client project as non-negotiable
evidence. Your engagement skills will carry most interview rounds; the coding round is
the gate, and it does not care about your facilitation skills.

## Your Advantage

The engagement arc is native to you. Engineers spend years learning what you already do
every week: running a kickoff, hearing what is not said, managing a sponsor's
expectations, and delivering bad news without losing the room. The posting evidence says
that half is not optional - direct customer work appears in 88.0% of FDE postings, and
discovery in 52.0% (observed evidence). You need the engineering half, which is
learnable on a schedule; the room-running half is not, and every other candidate on this
list has to go learn it from someone like you.

## Related documents

- [Discovery and requirements](../skills/02-discovery-and-requirements.md) - your core
  craft, formalized into engineering evidence
- [Managing expectations](../customer/04-managing-expectations.md) - the skills you
  already have, named and sharpened
- [Requirements to spec](../customer/02-requirements-to-spec.md) - the first artifact
  dialect to learn
- [Core technical skills](../skills/01-core-technical-skills.md) - the self-audit that
  becomes your study plan
- [Coding and technical interviews](../interviews/02-coding-and-technical.md) - the gate
  this path must plan for explicitly
- [From Solutions Engineer](from-solutions-engineer.md) - the closest sibling path;
  compare your gaps before committing
