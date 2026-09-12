# From Solutions Engineer to FDE

You have the customer instincts: discovery-adjacent questioning, demo craft, technical
validation, and conversations with buyers. The FDE job adds production engineering
ownership - after the deal closes, you stay and ship. Practitioner comparisons draw the
boundary simply: solutions engineers work pre-sale with demos, validation, and quota;
FDEs work post-sale, embedding with the customer and shipping production code with no
quota (industry pattern, from 2026 practitioner write-ups). The posting evidence agrees
on the weight: direct customer work appears in 88.0% of FDE postings and building
production systems in 90.0% (observed evidence, from the 146-posting scrape analysis
used across this guide). You arrive native in the first and trainable in the second.

## What You Already Have

- Customer communication - with executives and operators, in their language, at their
  pace
- Discovery-adjacent questioning - you already ask "what are you trying to achieve" for
  a living; FDE discovery formalizes it into evidence rather than qualification
- Pre-sale technical validation - you have already tested whether a product fits a real
  environment with real constraints; production ownership extends that instinct from
  judging to building
- Demo craft - including honest demos, which is rarer than it sounds (see
  [managing expectations](../customer/04-managing-expectations.md) for where the line is)
- Multi-stakeholder navigation - champions, skeptics, procurement, and the person who
  can veto quietly
- Product-technical fluency - you can explain how the thing works and where it breaks,
  which is the raw material for engineering conversations

## What You Need to Learn

- Production engineering depth - testing, CI/CD (34.0% of postings), deployment, and
  monitoring, to the level where you own a service rather than describe one (see
  [prototype to production](../deployment/01-prototype-to-production.md))
- Systems fundamentals at real depth - databases, APIs, and one cloud, to debuggable
  depth rather than demo depth (see
  [core technical skills](../skills/01-core-technical-skills.md))
- The AI application layer with evaluation discipline - LLM APIs, RAG, and the
  evaluation sets that prove they work to a skeptical customer (49.0% of postings list
  evaluation, testing, and monitoring)
- Engineering artifacts - specs, decision records, and postmortems, judged by whether a
  stranger can act on them rather than by whether a room applauds; in practice this
  means rewriting your demo follow-up emails as engineering notes: what was tested, what
  was observed, what happens next

The honest test for "real depth" is not whether you can configure a tool but whether you
can debug it at the log level. Demo depth is knowing what a tool does; debug depth is
knowing what it does when it is broken, which is the only state customers call you
about. Structure every fundamentals hour so it ends with something broken and you
fixing it.

## What to Skip

- More demo polish - your demos already work; the gap is everything that happens after
  the demo
- Another sales-process certification - it deepens the half that is already strong, and
  no FDE posting asks for it
- Slide-deck perfectionism - engineering artifacts are read, not presented; optimize for
  the reader, not the room
- CRM workflow mastery - tooling depth here adds no engineering signal
- Studying closing techniques - FDE work has no quota and no close; the relationship
  continues past the signature instead of ending at it

## Projects to Build

The theme is your demo becoming a system. For twelve full specs, see
[project ideas](../portfolio/02-project-ideas.md).

### A working integration, end to end

Build the integration you have demoed a hundred times, as real code: tests, CI,
authentication, retries, monitoring, and error messages a user can act on. It is
FDE-shaped because it is the pre-sale to post-sale delta compressed into one artifact.
It proves you can cross from showing software to shipping it. Use the stack you would
defend in an interview, not the one that demos fastest.

### A PoC hardened to production readiness

Take a proof of concept you built - or one from the portfolio section - and drive it
through a production-readiness checklist: observability, secrets handling, rollback,
load behavior, runbook, and a support story. It is FDE-shaped because the
demo-to-production gap is the single most common place AI engagements stall. It proves
you know what handover-grade means and can get there (see the
[production readiness checklist](../deployment/03-production-readiness-checklist.md)).
Write down what the checklist finds; the gap list is your study plan for the remaining
months.

### A deployment case study with metrics

Document one deployment - yours, or one you supported in a pre-sale role - as a proper
case study: requirements, architecture decisions, failure modes hit and fixed, and
outcome metrics. It is FDE-shaped because feeding field lessons back into the product is
a named FDE responsibility, appearing in 31.0% of postings. It proves you can write the
engineering story, not the sales story. Include what went wrong and what it cost; the
honesty is what separates an engineering case study from marketing.

## Suggested Path

1. Audit your engineering depth honestly - run the self-audit in
   [core technical skills](../skills/01-core-technical-skills.md) and expect it to sting
   in the deployment rows
2. Close systems fundamentals - SQL beyond `SELECT`, `Docker` fluency, one cloud end to
   end; build, break, and debug your own stack until recovery is boring
3. Build the working integration - with tests and CI from the first commit, not bolted
   on at the end
4. Add the AI layer with evaluation - structured outputs, a small RAG build, and an
   evaluation set; your customer instinct makes the "prove it" half feel natural, but
   let the metrics win when demo instincts and evaluation discipline disagree
5. Harden your own PoC - run the
   [production readiness checklist](../deployment/03-production-readiness-checklist.md)
   against it and fix everything it finds
6. Write the case study - one deployment, written as engineering evidence with metrics,
   not as a win story
7. Prepare for the coding interview rounds - the round solutions engineers most often
   underestimate; practice coding under time pressure, out loud, weekly

## Timeline

3-6 months depending on engineering depth, at 5-10 hours per week (expert estimate). If
you write real code weekly and have deployed something you owned, expect the low end; if
your technical work has been mostly demos, configuration, and guided PoCs, expect the
high end or more. Assumptions behind the range: a real integration target available to
you, and at least one PoC of your own to harden. Budget interview preparation separately
from the learning: the coding round is a gate, and reading about it does not substitute
for practicing it. This is an estimate, not a promise; the audit in step one will tell
you which end of the range you are on.

## Your Advantage

You already speak customer, and most engineers do not. The customer half of the role -
88.0% of postings - is the half engineers fear and avoid, and you do it daily: reading
the room, hearing the unsaid objection, managing a skeptical stakeholder. That half is
slow to teach and fast to recognize in an interview. The engineering half is the
opposite: learnable on a schedule with deliberate practice. You are converting a
strength into a missing skill rather than the reverse, and hiring managers who have
watched both directions happen tend to bet on yours (expert interpretation). Practical
first move: volunteer for the engineering half inside your current role - own the
PoC-to-pilot handover, write the integration, sit in the incident channel. It converts
work hours into transition hours.

## Related documents

- [FDE vs other roles](../role/03-fde-vs-other-roles.md) - the boundary you are crossing,
  and the gray zones inside postings
- [Prototype to production](../deployment/01-prototype-to-production.md) - the
  discipline this path exists to build
- [Production readiness checklist](../deployment/03-production-readiness-checklist.md) -
  the hardening checklist for project two
- [Managing expectations](../customer/04-managing-expectations.md) - the half you know,
  formalized so you can teach it
- [Coding and technical interviews](../interviews/02-coding-and-technical.md) - the gate
  this path must plan for explicitly
- [Presenting projects](../portfolio/03-presenting-projects.md) - turning your case study
  into interview-ready evidence
