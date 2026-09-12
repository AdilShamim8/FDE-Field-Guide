# Beginner to FDE

This path is for people with little or no professional engineering experience: students,
career switchers coming from operations, support, teaching, or any non-engineering job,
and self-taught programmers without a first role yet. The honest summary is that FDE
hiring in 2025-2026 skews senior - an independent job-scrape analysis of 146 FDE postings
from 94 companies (February-July 2026) found no junior titles at all (observed evidence) -
so this is the longest path in this section. The goal is not to jump straight to an FDE
title. The goal is to become an employable engineer with FDE-shaped evidence, land an
adjacent first role, and let real work carry you the rest of the way.

## What You Already Have

Probably more than you think. Engineering experience is the gap, but half of FDE work is
customer work, and that half gets learned in ordinary jobs earlier than most engineers
believe:

- Customer and workplace experience - retail, hospitality, support desks, healthcare
  administration, teaching, logistics: all of it taught you how organizations actually
  behave, how to talk to a frustrated person, and how work really gets done when the
  process document is wrong
- Tolerance for ambiguity - non-engineering work rarely hands you a written spec either;
  you are used to figuring out what someone actually wants from what they say
- General technical literacy - spreadsheets, maybe some scripting, and the ability to
  learn a tool from its documentation instead of a training course
- A concrete reason to want this role - you will need it, because this path is measured
  in quarters, not weekends

## What You Need to Learn

In this order, because each stage unblocks the next. The most important item is the first
one - everything else sits on it:

1. Programming fundamentals with `Python` - `Python` appears in 91.0% of FDE postings,
   the highest of any skill; learn functions, data structures, and tests with `pytest`,
   not just notebook scripts
2. Building small web services - APIs with `fastapi`, because FDE deliverables are
   usually services that other systems call, not scripts that run once
3. Databases and SQL - most customer data lives in a relational database somebody else
   designed; learn joins, aggregations, and how to navigate an unfamiliar schema
4. Git and code hygiene - branches, pull requests, review, and readable commits; FDE
   code becomes the customer's code after handover, so it has to survive their review
5. One cloud's basics - `AWS` shows up in 47.0% of postings; learn to deploy a
   containerized service end to end, including storage, a managed database, and IAM
   basics
6. `Docker` basics - 40.0% of postings; build images, read container logs, and glue a
   local stack together with `docker compose`
7. The AI layer - LLM APIs with structured outputs and function calling first, then RAG
   (52.0% of postings); learn the concepts framework-free before picking up whichever
   framework a job happens to use
8. The FDE layer - discovery interviewing, writing a one-page spec, building an
   evaluation set, and writing handover documentation

The FDE layer is not a graduation gift you add after the technical stack is done. Weave
it into every project from the start: interview the user, write the spec, ship, hand
over. It costs about a day per project, and it is what turns a practice project into FDE
evidence.

## What to Skip

- Computer science theory deep-dives - compilers, automata, and advanced algorithm
  analysis almost never decide FDE hiring or FDE work; shipping does
- Multiple clouds at once - one cloud well beats three clouds badly; add reading fluency
  in the others later, on the job
- Kubernetes, for now - 35.0% of postings mention it, but debugging a broken
  `docker compose` stack comes before debugging a cluster, and most FDE roles operate
  clusters rather than build them
- LeetCode as a lifestyle - practitioner reports consistently describe FDE interviews as
  testing real-world reasoning over puzzle collection; practice some, but do not live
  there
- Front-end framework specialization - learn to ship a usable interface, not to become a
  framework expert; FDEs borrow UIs, they do not build design systems

## Projects to Build

Pick projects with real users and ambiguous requirements; tutorials do not count as
evidence. For twelve full specs with built-in constraints, see
[project ideas](../portfolio/02-project-ideas.md). The three shapes below matter most at
this stage.

### A document question-answering tool for a real organization

Volunteer to build a retrieval-backed question-answering tool over the real documents of
an organization you actually know: a club, a nonprofit, a small business. A real corpus
means real mess - scans, duplicates, stale versions - and real users mean real feedback
about what "good" means. It is FDE-shaped because the requirements are ambiguous, the
data belongs to someone else, and success is measured by whether people keep using it.
It proves you can take an unclear ask to a deployed system that survives contact with
users.

### An integration between two existing services

Glue two services that do not talk to each other - a form tool and a database, a booking
system and a messaging app. Handle authentication, retries, and rate limits, and make it
survive one of the APIs changing underneath you. It is FDE-shaped because integrating
systems you do not own is the most common concrete engineering task in the postings
(64.0%). It proves you can work against someone else's contract, not just your own code.

### A small data pipeline with tests

Move data from a source, clean it, land it in a database, run it on a schedule, and
alert when it breaks - with tests covering the transformations. It is FDE-shaped because
data plumbing is where AI deployments stall, and because "it works on my machine" is not
a deliverable. It proves reliability discipline: logging, idempotency, and failures you
find before your users do.

## Suggested Path

1. Learn `Python` fundamentals - about three months of exercises and small tools you
   actually use; add `pytest` early so testing is a habit rather than a retrofit
2. Build and ship a small web service - `fastapi` plus a database, with Git history on
   every project, and get at least one stranger to review your code
3. Deploy something real - containerize the service with `Docker`, deploy it to one
   cloud, and give it a URL you can send to someone; do not move on until this works
4. Add the AI layer - call an LLM API with structured outputs, then build a small RAG
   system over documents you care about
5. Do the document Q&A project for a real organization - interview the users, write a
   one-page spec, build, deploy, and hand it over with a runbook; this single project
   exercises the entire FDE layer
6. Study the FDE layer deliberately - work through the discovery question bank, write
   specs for everything you build, and build a small evaluation set for the AI features
7. Apply to adjacent roles while the evidence compounds - junior software engineer,
   support engineering, implementation consultant, solutions engineer; each one is a
   step toward customer-facing production work, which is the soil FDE roles grow from

## Timeline

Expect 18-30 months to employable-with-evidence. This is an expert estimate, not a
promise. Assumptions behind it:

- 10-15 hours per week of consistent study around a job or coursework
- Starting from no programming experience; the AI layer itself is only 2-3 months of
  the total
- Full-time study compresses the estimate toward 12 months; weekends-only can stretch it
  past 30

The first role will probably be adjacent rather than FDE itself: the same posting
analysis found no junior FDE titles, and a typical posting asks for 4+ years in a
technical customer-facing role, as Anthropic's does (observed evidence, 2026). From an
adjacent first role, reaching an FDE title commonly takes another 1-3 years (expert
interpretation from posting requirements and practitioner career notes).

## Your Advantage

You have no habits to unlearn - no framework tribalism, no "that is not my job" reflex,
and no assumption that discovery belongs to someone else's department. The customer
instincts from non-tech work count more than they look like they do: de-escalating an
angry customer, reading a room, and explaining a delay without excuses are skills
engineers spend years acquiring on the job, and you may already do them daily. And
because you are building the stack from scratch, you get to learn it in the order the
posting evidence rewards, instead of retrofitting fundamentals around habits you already
have.

## Related documents

- [What is an FDE](../role/01-what-is-an-fde.md) - confirm the destination before
  committing 18-30 months to it
- [Core technical skills](../skills/01-core-technical-skills.md) - the full stack this
  path builds toward, with depth calibration for each skill
- [Market overview](../job-market/01-market-overview.md) - the demand data behind the
  seniority warning
- [What to build](../portfolio/01-what-to-build.md) - the principles that make a project
  count as evidence rather than practice
- [Getting hired](../job-market/03-getting-hired.md) - converting your evidence into an
  adjacent first role
- [From Software Engineer](from-software-engineer.md) - the path you will most likely
  merge onto after your first engineering role
