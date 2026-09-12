# Documented LLM Deployment Cases

Public, documented evidence is the closest thing the AI industry publishes to case studies.
This file walks that evidence in three layers - the pilot-failure statistics, the
production-motion descriptions from AI labs, and the platform-vendor record - and extracts
the lessons for practitioners, with every claim sourced. Cases are described only at the
level the sources support; where the evidence stops, the file says so.

## The pilot-failure evidence base

The largest documented fact about enterprise LLM deployment is a failure rate. The MIT
NANDA report "The GenAI Divide: State of AI in Business 2025" found that approximately 95%
of enterprise GenAI pilots deliver no measurable P&L impact, while roughly 5% achieve rapid
revenue acceleration (Fortune coverage, August 18, 2025,
[Fortune](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo)).
The finding is based on 150 leadership interviews, a survey of 350 employees, and analysis
of 300 public AI deployments - it is a study of deployments, not a poll of opinions.

The same research attributes the successes to three factors: the system is integrated into
real workflows, it is domain-specific, and it is commonly bought and adapted rather than
built internally. Read as a failure analysis, the ~95% stall where those factors are
missing: pilots die on the gap between what the tool does and what the workflow requires,
on missing domain fit, and on custom builds that never converge.

Why this matters for FDEs: the role is the industry's structural answer to the gap the
report measures. The New Stack (May 2026) describes FDE teams as the mechanism for
integrating systems, launching in production, and improving deployments as issues appear
([The New Stack](https://thenewstack.io/forward-deployed-engineers-ai)). Fortune's
September 2026 coverage of the FDE job market quotes Paul Farnsworth, president of Dice,
on the same roadblock from the buyer's side: companies are "struggling to turn those models
into something that actually works inside of their business", and forward-deployed
engineers "can help fill that gap"
([Fortune](https://fortune.com/2026/09/03/forward-deployed-engineers-fast-growing-six-figure-silicon-valley-job-integrate-ai-with-customers-tech-careers-palantir)).
This suggests the 95% figure is not just a warning; it is the demand curve for the role.

## The production-motion evidence

The second layer is what AI labs document about their own deployment motion. Anthropic's
FDE job description lists the deliverables explicitly: production applications with Claude
models inside customer systems, MCP servers, sub-agents, and agent skills for production
workflows, plus white-glove deployment support
([Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008)).
One line deserves special attention: identifying and codifying repeatable deployment
patterns and feeding insights back to product and engineering. That line says the
engagement is not complete when the customer's system ships; it is complete when the next
engagement gets faster because of what this one produced.

The external descriptions match. The New Stack frames the cycle as integrate, launch in
production, improve as issues appear - a continuous motion rather than a project with an
end date. LangChain's "State of Agent Engineering" survey (2026) reports that organizations
have shifted from debating whether to deploy agents to how to deploy them reliably
([LangChain](https://langchain.com)); as a vendor survey it has an interest in the answer,
but the direction it describes matches the posting evidence: 49.0% of FDE postings in the
independent scrape mention evaluation, testing, or monitoring
([scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)).

This suggests the industry conversation has moved past the pilot question. The open problem
the evidence points at is reliability: keeping quality measurable and stable in production,
which is where the FDE skill set concentrates and where
[monitoring and reliability](../ai/04-monitoring-and-reliability.md) goes deep.

## The platform-vendor evidence

The third layer is the oldest documented deployment motion. Palantir popularized the FDE
title ([Wikipedia](https://en.wikipedia.org/wiki/Forward_deployed_engineer)) and runs it at
scale two decades in: Fortune (September 2026) counted roughly four dozen open
forward-deployed positions, including client-specific roles for Intel, NATO, and Norway.
The FDSE listing describes ownership, not tasks: "your responsibilities look similar to
those of a startup CTO: you'll work in small teams with minimal supervision and own
end-to-end execution of high stakes projects" (via Fortune, September 2026).

What two decades of this model show is interpretation, but it is grounded: the pattern
generalizes beyond AI. Embedding senior engineers with customers to ship inside their
constraints predates LLMs and has outlived at least one hype cycle, which suggests the
pattern is structural rather than fashionable. The current wave is AI-specific tooling on
an old skeleton - the deliverables are now MCP servers and agent skills instead of data
integrations, but the ownership structure, the small-team autonomy, and the
end-to-end accountability are the ones Palantir normalized. The durable lesson is that
whoever owns the deployment owns the outcome, and job titles follow the ownership.

## Lessons for practitioners

These are the guide's lessons from the documented evidence (interpretation tier, each tied
to the document that turns it into practice):

1. The deployment that ships is the one with a named owner on the customer side. Every
   documented motion - lab, bootcamp, integrator, startup - assigns end-to-end ownership
   explicitly, and the 95% finding is what happens when nobody owns the system after the
   demo. Plan the owner before the launch: [prototype to production](../deployment/01-prototype-to-production.md).
2. Evaluation is the contract between you and the customer. The success factors in the
   NANDA research are unfalsifiable without a quality bar, so agree on the golden set and
   the thresholds before the prototype exists, not after the first dispute:
   [evaluation and testing](../ai/03-evaluation-and-testing.md).
3. Workflow integration beats model quality. The documented failure factor is the gap
   between the tool and the workflow, not the model's capability, so spend the integration
   budget before the prompt budget: [the FDE loop](../role/05-the-fde-loop.md), stages 6
   and 8.
4. Discovery is engineering, not pre-sales. The postings treat scoping as an engineering
   responsibility (52.0% mention discovery or requirements), and the documented motions
   fold requirements work into the build rather than front-loading a sales phase:
   [discovery and requirements](../skills/02-discovery-and-requirements.md).
5. Buy and adapt when the workflow is standard; build when it is the differentiator. The
   NANDA research ties success to buying external tools, and the FDE's judgment call is
   which side of that line each component falls on:
   [trade-offs and decision records](../system-design/03-trade-offs-and-decision-records.md).
6. Codify what repeats. The Anthropic mandate to feed deployment patterns back to product
   is what separates a deployment motion that scales from a services business that cannot,
   and the same habit helps any team: [deployment patterns](../deployment/02-deployment-patterns.md).
7. Handover decides the P&L. A system that works but has no operator produces no measurable
   impact - which is precisely the failure the 95% figure counts. Build the runbook, the
   owner, and the support boundary before go-live:
   [the engagement lifecycle](../customer/01-engagement-lifecycle.md).
8. Reliability is the current frontier. The shift from whether-to-deploy to how-to-deploy,
   visible in both the survey evidence and the posting data, moves the hard problem from
   capability to dependable operation: [monitoring and reliability](../ai/04-monitoring-and-reliability.md).

## A note on sourcing

Public case studies skew toward successes. Vendors publish deployments that went well;
customers almost never publish postmortems of pilots that died, and the MIT NANDA finding
implies most pilots - roughly 95% - leave no public trace at all. This means every
documented deployment in this file is a survivor, and the documented record systematically
under-represents the failure modes that the statistics describe. Read every published
deployment with that discount applied, and read [failure stories](03-failure-stories.md)
for the counterweight: the failure modes the record does not publish.

## Related documents

- [Deployment patterns in the wild](01-deployment-patterns-in-the-wild.md) - the engagement shapes behind these cases
- [Failure stories](03-failure-stories.md) - the counterweight to the success bias in public sources
- [Prototype to production](../deployment/01-prototype-to-production.md) - the crossing the evidence says most pilots never complete
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - the practice behind the evaluation lesson
- [The FDE loop](../role/05-the-fde-loop.md) - the motion the evidence describes, stage by stage
- [The engagement lifecycle](../customer/01-engagement-lifecycle.md) - handover and impact measurement in practice

## Further reading

- [Fortune: MIT report on GenAI pilots](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo) - the pilot-failure evidence base (August 2025)
- [The New Stack on FDE teams](https://thenewstack.io/forward-deployed-engineers-ai) - the integrate-launch-improve motion (May 2026)
- [Fortune on the FDE job market](https://fortune.com/2026/09/03/forward-deployed-engineers-fast-growing-six-figure-silicon-valley-job-integrate-ai-with-customers-tech-careers-palantir) - the demand-side and Palantir evidence (September 2026)
- [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) - the deliverables of the lab deployment motion, in the vendor's own words
- [LangChain](https://langchain.com) - the State of Agent Engineering survey (2026), read with the vendor-interest caveat above
