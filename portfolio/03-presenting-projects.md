# Presenting Portfolio Projects

For candidates who have built, or are building, a deployment-shaped project. Hiring
managers spend minutes on a portfolio, not hours, so the presentation layer - the write-up,
the demo, the metrics - decides whether your depth is visible at all. This file gives a
write-up structure, demo rules, the metrics worth reporting, a repo hygiene checklist, and
the 90-second interview version of the story.

## The write-up structure

We recommend every project write-up uses this shape, in this order:

1. Problem - the ambiguous brief as given, close to verbatim, before you cleaned it up
2. Constraints discovered - the ones you did not choose: data quality, access, budget, latency, PII, an unmigratable stack
3. What you built - an architecture sketch and the components, named in the operator's vocabulary rather than the vendor's
4. Decisions and trade-offs - three to five, each one line: the option rejected, the reason, the cost you accepted
5. Evaluation - dataset size and provenance, metrics, thresholds, and the failures you could not fix
6. Deployment and operations - where it runs, how it is monitored, what an incident looks like, who gets paged
7. Outcomes - the numbers you defined as success before building, reported after
8. What you would do differently - specific and technical, not "I would plan better"

### Why the decisions section matters most

FDE interviewers read the decisions and trade-offs section first, because the job is
judgment under constraints and decisions are the only section that exhibits judgment. A
project with no visible decisions is indistinguishable from a tutorial with extra steps:
anyone can describe what they built; the reason the second-best option lost is what proves
an engineer was present. The professional version of this habit is the decision record; see
[trade-offs and decision records](../system-design/03-trade-offs-and-decision-records.md)
for the format teams actually use, and borrow its fields for the portfolio.

## The demo

We recommend these rules over the instinctive "here is a link, try it":

- Record a 2-minute walkthrough instead of relying on a live link - the recording is always up, always fast, and you control the narrative; a live link that 404s or takes 90 seconds to cold-start undoes the write-up
- Show the failure path on purpose - feed it a broken input, show the recovery: the exception queue filling, the fallback answering, the honest error message; reviewers trust failure behavior they have seen, and an FDE demo that never fails reads as untested
- Ship a one-command run - a `curl`-able endpoint or a fixture script (`make demo`) so a reviewer can reproduce your best moment in one command without your secrets or your data
- Date the recording - if the repo evolved past the video, say so; a stale demo with a note reads as honesty, an undated one reads as drift

The recorded failure path is the highest-leverage ninety seconds in the whole portfolio. It
is the portfolio equivalent of the "what broke and how you fixed it" question that
practitioner accounts of FDE interviews report being asked. A reviewer who has watched your
system recover starts from a different assumption about everything else you claim.

## The metrics that matter

Report the numbers an operator or a budget owner would ask for:

- Eval scores with dataset size - "88% correct extraction on 412 real invoices" is evidence; "high accuracy" is decoration; the dataset size is what makes the score falsifiable
- Latency p95 - the number operators care about, because the tail is where users live; a mean without a tail hides the cold starts
- Error taxonomy counts - how the failures split by type; this is what drives the next iteration and what a customer's team will ask about first
- Cost per day - even an estimate, in the units a budget owner thinks in; portfolios that report cost read as written by someone who has met a finance department

Two honesty rules. Never round failures away: report the failing classes, the unanswered
queries, and the retries that did not help. And never report a perfect score without a
dataset-size caveat, because a flawless run on twelve examples reads as a cherry-picked
eval, and a reviewer who spots a cherry-picked eval stops trusting every other number in
the write-up. [Evaluation and testing](../ai/03-evaluation-and-testing.md) is the practice
behind these numbers.

## The repo hygiene checklist

Run this before you send the link to anyone:

- [ ] The README's first screen passes the "what is this" test: one paragraph, one architecture sketch, one demo link
- [ ] Setup works from a clean clone with one documented command, on a machine that is not yours
- [ ] Tests run and pass, and the eval suite runs offline on committed fixtures
- [ ] No secrets in the git history - check before publishing, and rewrite the history if any leaked
- [ ] Decisions are documented where a reviewer can find them without reading every commit
- [ ] Known issues and past incidents are written down, not hidden in closed issues
- [ ] All data is synthetic or licensed; no real customer, user, or personal data anywhere
- [ ] A license file is present, and dependency versions are pinned enough to reproduce
- [ ] The write-up links to the repo and the repo links back to the write-up

The checklist is deliberately boring. Boring is the point: a reviewer who sees operational
hygiene extends you the benefit of the doubt on everything they cannot check in five
minutes.

## How to talk about it in interviews

Prepare the 90-second version and rehearse it until it is boring to you: the problem in one
sentence, the constraint that mattered most, what you shipped, the number that proves it,
and the one thing that broke. Then prepare the follow-up depth, because the 90 seconds buys
the questions, and the depth is what you are being scored on:

- Why this chunking, threshold, or model? - name the alternative and the evaluation that decided, not just the choice
- What broke? - have a real incident story: the symptom, the diagnosis, the fix, and what changed in monitoring afterward
- What would the customer's operator say about it? - describe the daily experience of running your system, not just its architecture

Many loops skip the portfolio conversation and hand you a take-home instead; the same
presentation rules apply there, compressed - see [take-home assignments](../interviews/06-take-homes.md)
for the formats and rubrics. If your portfolio project and your take-home share a domain,
expect deeper follow-ups, and treat that as an opportunity rather than a trap.

## Related documents

- [What to build](01-what-to-build.md) - the principles that make the underlying project worth presenting
- [Project ideas](02-project-ideas.md) - the twelve briefs to build from
- [Take-home assignments](../interviews/06-take-homes.md) - the same presentation rules inside an interview loop
- [Trade-offs and decision records](../system-design/03-trade-offs-and-decision-records.md) - the professional format behind the decisions section
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - how to produce metrics a reviewer trusts
- [Communication and storytelling](../skills/03-communication-and-storytelling.md) - the written-first habits behind a good write-up

## Further reading

- [Chip Huyen](https://huyenchip.com) - writing on evaluation and observability for LLM systems in production; the deeper practice behind the metrics section
