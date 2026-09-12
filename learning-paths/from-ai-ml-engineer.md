# From AI/ML Engineer to FDE

You have the model skills the market asks about: LLM APIs, RAG, agents, evaluation. The
FDE job adds the delivery arc - discovery, requirements, stakeholder management, and
deployment inside customer environments. Your AI stack transfers directly; what is new
is the organization around it. In the independent job-scrape analysis of 146 FDE
postings used across this guide, the applied AI skills you already hold are the
differentiators - prompt engineering 55.0%, RAG 52.0%, agents 42.0% - while production
systems (90.0%) and direct customer work (88.0%) are the bundle around them (observed
evidence). Your gap is that bundle.

## What You Already Have

- The AI application stack - LLM APIs, prompt engineering, RAG, and tool-calling agents:
  the skills at 55.0%, 52.0%, and 42.0% in postings, which most candidates lack; you
  will not need interview-preparation hours for the skills half of the loop
- Evaluation discipline - your superpower; 49.0% of postings list evaluation, testing,
  and monitoring, and few candidates can actually build a golden set and defend a rubric
  to a skeptical room
- Model-selection judgment - knowing when RAG is the wrong answer, when a larger model
  is wasted cost, and when a deterministic script beats an agent; this is the judgment
  that saves customers money, and they remember who saved it
- Probabilistic-system intuition - you reason fluently about outputs that vary, which
  engineers from deterministic backgrounds find genuinely hard; explaining variance
  without panic is a customer-facing skill you already own

## What You Need to Learn

- Discovery - interviewing operators and shadowing workflows; model-centric work assumes
  the problem arrives on a plate, and FDE work starts before the problem is known (see
  [discovery and requirements](../skills/02-discovery-and-requirements.md))
- Customer environment realities - their clouds, their identity providers, their
  security review, and their politics; the demo environment is a lie and the real one
  has SSO (see
  [working in customer environments](../customer/03-working-in-customer-environments.md))
- Production delivery discipline - CI/CD, monitoring, runbooks, and the difference
  between demo-grade and handover-grade (see
  [prototype to production](../deployment/01-prototype-to-production.md))
- Writing specs and decision records - the artifacts that let a customer team own your
  system after you leave
- The engagement lifecycle - phases, exit criteria, and the handover problem; the arc is
  the job, not overhead (see
  [the engagement lifecycle](../customer/01-engagement-lifecycle.md))

Three model-centric habits need retraining rather than new knowledge. The first is
defaulting to the most sophisticated architecture on the whiteboard when a deterministic
script would survive handover better. The second is treating customer data as an
afterthought - in your world the dataset is clean and split; in theirs it is duplicated,
owned by three teams, and partially living in spreadsheets. The third is quoting
accuracy from a public benchmark, which customers hear as a promise; the only numbers
that count are from an evaluation set built on their workflow.

## What to Skip

- Deeper model internals - another fine-tuning course or a train-from-scratch project
  adds little; FDEs apply and evaluate models, they rarely train them
- Benchmark chasing - leaderboard movements rarely change a customer outcome; an
  evaluation set built on the customer's workflow beats a public benchmark every time
- Collecting more frameworks - `LangChain` appears in 33.0% of postings, which means
  two-thirds name no framework at all; concepts transfer, collections do not
- Research-oriented portfolio items - a novel-architecture repository has less FDE
  signal than one deployed system with a runbook and an evaluation report

## Projects to Build

The theme is taking what you already have and dragging it into someone else's world. For
twelve full specs, see [project ideas](../portfolio/02-project-ideas.md).

### Productionize one of your existing AI projects for a specific organization

Pick your best existing project and rebuild it for a named external organization:
written spec, deployment under their constraints, monitoring, and a handover document.
The delta between your notebook and a handover-grade system is exactly the gap this path
closes. It proves you can deliver something a stranger can own, which is the FDE test.
Reuse what exists deliberately - the point is the delivery layer, so keep the model
part boring.

### An integration into a real customer system

Add a real enterprise integration to a system you built: SSO through an identity
provider, a connection to their data warehouse, or their audit-logging requirements. It
is FDE-shaped because the environment, not the model, is where deployments actually get
hard. It proves you can deploy into constraints you did not choose. Expect the
environment, not the model, to consume most of the calendar; that ratio is the lesson.

### An evaluation report and runbook for someone else's system

Take an AI system a peer built and write the evaluation report and operational runbook
as if you were taking it over on Monday. It is FDE-shaped because FDEs inherit, extend,
and hand over systems constantly; inherited code is the default condition. It proves you
can bring rigor to a system you did not write, including at least one finding the author
did not want to hear. Deliver it as a document the owner could act on without you in
the room.

## Suggested Path

1. Map the delivery arc you are missing - read
   [the engagement lifecycle](../customer/01-engagement-lifecycle.md) and
   [the FDE loop](../role/05-the-fde-loop.md) to see what "done" means beyond the model
2. Practice discovery on real operators - three interviews, one shadowing session, and a
   problem statement written in the operator's own words
3. Productionize your best project - CI/CD, monitoring, secrets handling, runbook, and
   handover doc, deployed somewhere that is not your laptop
4. Practice on inherited code - the evaluation report and runbook for a peer's system,
   delivered as a document they could act on
5. Write the engineering artifacts - a spec and two decision records for your
   productionized project; the system-design section has the formats
6. Prepare for the customer-scenario interview rounds - your technical answers are
   already strong; rehearse discovery and expectation conversations out loud, where they
   are weaker than you think

## Timeline

1-3 months for the delivery layer, at 5-10 hours per week, with access to at least one
real organization or peer project to practice on. This is the shortest estimate in this
section because the AI skills transfer directly - you are not relearning the stack, you
are wrapping it in an engagement. Expect the upper end if you have never worked outside
a research or platform team, since the customer-politics layer takes practice that books
do not provide (expert estimate, not a promise). If you are between roles you can
compress toward the low end with double hours, but the practice still needs real
organizations more than it needs hours.

## Your Advantage

Evaluation skill is rare and customer-visible. AI deployments stall where quality cannot
be proven: the MIT NANDA report found roughly 95% of enterprise GenAI pilots deliver no
measurable P&L impact (via Fortune, August 2025), and the failure mode is mostly
unproven, unintegrated deployments rather than bad models. You can prove quality to a
skeptical room, which is precisely where AI engagements get stuck. You are also the
candidate who will not be seduced by a demo - you know exactly what it would take to
test one. The same skill makes you the engineer who catches the doomed pilot before the
budget is spent, which is among the most commercially valuable sentences anyone can say
in this market.

## Related documents

- [Working in customer environments](../customer/03-working-in-customer-environments.md) -
  the realities your lab or platform team insulated you from
- [Prototype to production](../deployment/01-prototype-to-production.md) - the
  discipline that turns your projects into handover-grade systems
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - your superpower,
  sharpened for customer contexts
- [Requirements to spec](../customer/02-requirements-to-spec.md) - the artifact format
  for the writing practice above
- [The FDE loop](../role/05-the-fde-loop.md) - the full arc your model skills currently
  cover only part of
- [From Data Engineer](from-data-engineer.md) - the closest sibling path if your AI work
  is data-heavy
