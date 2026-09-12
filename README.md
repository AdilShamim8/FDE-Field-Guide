# FDE Field Guide

A practical field guide to becoming and working as a Forward Deployed Engineer (FDE) - the
engineer who gets embedded with customers to turn ambiguous business problems into working,
production-ready systems.

This is an engineering field guide, not a career brochure. The focus is the full arc of
customer-facing engineering: problem, discovery, requirements, architecture, prototype,
integration, deployment, evaluation, iteration, production, customer impact.

Everything here follows an evidence discipline. Sourced facts carry a source and a date;
patterns are labeled as patterns; recommendations are labeled as recommendations. See
[STYLING.md](STYLING.md) for the writing contract used across the repository.

## Is this guide for you?

- Learning engineering from scratch - start with [the FDE loop](role/05-the-fde-loop.md), then [what an FDE is](role/01-what-is-an-fde.md)
- A software engineer curious about the transition - [From Software Engineer](learning-paths/from-software-engineer.md)
- An existing FDE who wants to get better - [troubleshooting](troubleshooting/README.md), [system design](system-design/README.md), and [evaluation](ai/03-evaluation-and-testing.md)
- Preparing for FDE interviews - start with [the interview process](interviews/01-interview-process.md)
- A hiring manager defining the role - [responsibilities](role/02-responsibilities.md) and [how the role differs from its neighbors](role/03-fde-vs-other-roles.md)
- Trying to understand how customer-facing engineering actually works - [case studies](case-studies/README.md) and [working in customer environments](customer/03-working-in-customer-environments.md)


## The FDE Role

- [What is an FDE](role/01-what-is-an-fde.md) - definition, Palantir origins, the modern AI-era role, common misconceptions
- [Responsibilities](role/02-responsibilities.md) - what FDEs actually do, from job-posting evidence to the weekly rhythm
- [FDE vs other roles](role/03-fde-vs-other-roles.md) - against AI engineer, software engineer, solutions engineer, ML engineer, consultant, and sales engineer
- [Where FDEs work](role/04-where-fdes-work.md) - AI labs, enterprises, startups, and systems integrators, and how the job changes in each
- [The FDE loop](role/05-the-fde-loop.md) - the core mental model: how FDEs move from a vague customer problem to measurable production impact


## Skills

- [Core technical skills](skills/01-core-technical-skills.md) - the technical baseline, evidence-weighted by what employers actually ask for
- [Discovery and requirements](skills/02-discovery-and-requirements.md) - interview frameworks, question banks, and turning conversations into requirements
- [Communication and storytelling](skills/03-communication-and-storytelling.md) - executive summaries, demos, technical narrative, written artifacts
- [Stakeholder management](skills/04-stakeholder-management.md) - mapping stakeholders, aligning incentives, escalating without burning trust
- [Ambiguity and prioritization](skills/05-ambiguity-and-prioritization.md) - deciding under partial information and cutting scope without killing value


## Engineering

- [Prototyping and PoCs](engineering/01-prototyping-and-pocs.md) - how to run a proof of concept that produces a decision, not just a demo
- [APIs and integrations](engineering/02-apis-and-integrations.md) - designing against systems you do not own, auth patterns, rate limits, contracts
- [Data pipelines](engineering/03-data-pipelines.md) - getting customer data flowing: ingestion, quality, schemas, and the unglamorous 80%
- [Cloud and infrastructure](engineering/04-cloud-and-infrastructure.md) - deploying into AWS, Azure, or GCP environments that already exist
- [Security and compliance](engineering/05-security-and-compliance.md) - customer security reviews, data boundaries, secrets, and audit expectations


## Customer Work

- [The engagement lifecycle](customer/01-engagement-lifecycle.md) - kickoff to handover, phase by phase, with exit criteria
- [Requirements to spec](customer/02-requirements-to-spec.md) - converting ambiguous asks into documents that engineers and customers both accept
- [Working in customer environments](customer/03-working-in-customer-environments.md) - unfamiliar stacks, restricted access, security theater, and culture
- [Managing expectations](customer/04-managing-expectations.md) - scope, demo expectations, delivering bad news, and saying no without losing the room


## AI and LLM Engineering

- [LLM application patterns](ai/01-llm-application-patterns.md) - the pattern catalog FDEs reach for: extraction, RAG, structured output, context engineering
- [Agents and tools](ai/02-agents-and-tools.md) - tool calling, agent loops, MCP, and when agents are the wrong answer
- [Evaluation and testing](ai/03-evaluation-and-testing.md) - golden datasets, LLM-as-judge, regression testing, and proving quality to a skeptical customer
- [Monitoring and reliability](ai/04-monitoring-and-reliability.md) - tracing, dashboards, alerting, and drift for systems whose behavior is probabilistic


## Deployment

- [Prototype to production](deployment/01-prototype-to-production.md) - why pilots die at the production cliff and how to cross it deliberately
- [Deployment patterns](deployment/02-deployment-patterns.md) - VPC-embedded, SaaS-adjacent, edge, and hybrid patterns with trade-offs
- [Production readiness checklist](deployment/03-production-readiness-checklist.md) - the go/no-go checklist to run before any customer goes live


## System Design

- [Architecture for customer systems](system-design/01-architecture-for-customer-systems.md) - designing under constraints you did not choose
- [Reference architectures](system-design/02-reference-architectures.md) - four repeatable architectures that cover most FDE engagements
- [Trade-offs and decision records](system-design/03-trade-offs-and-decision-records.md) - making architecture decisions legible to customers and your own team


## Troubleshooting

- [Debugging methodology](troubleshooting/01-debugging-methodology.md) - a structured approach for systems where you cannot read every line
- [Debugging customer systems](troubleshooting/02-debugging-customer-systems.md) - opaque environments, shared on-call, and working through someone else's process
- [Common failure modes](troubleshooting/03-common-failure-modes.md) - the recurring failures of customer-facing deployments and their fixes


## Learning Paths

- [Learning path overview](learning-paths/README.md) - how the paths fit together and how to judge your own readiness
- [Beginner to FDE](learning-paths/beginner-to-fde.md) - the longest path: engineering fundamentals plus the FDE skill set
- [From Software Engineer](learning-paths/from-software-engineer.md) - the most common transition: add customer work on top of production skills
- [From AI/ML Engineer](learning-paths/from-ai-ml-engineer.md) - you have the model skills; add delivery, discovery, and ownership
- [From Data Engineer](learning-paths/from-data-engineer.md) - your pipeline skills are the hard part of most deployments
- [From Solutions Engineer](learning-paths/from-solutions-engineer.md) - you have the customer instincts; add production depth
- [From Consultant](learning-paths/from-consultant.md) - you can run the room; add engineering ownership


## Interviews

- [The interview process](interviews/01-interview-process.md) - loop structure, stage-by-stage evidence from 2025-2026 hiring
- [Coding and technical rounds](interviews/02-coding-and-technical.md) - what FDE coding interviews actually test and how to prepare
- [System design rounds](interviews/03-system-design.md) - customer-flavored system design and how interviewers score it
- [Customer scenario rounds](interviews/04-customer-scenarios.md) - role-plays, discovery exercises, and practice scenarios with rubrics
- [Behavioral rounds](interviews/05-behavioral.md) - the ownership and judgment stories you need ready
- [Take-home assignments](interviews/06-take-homes.md) - typical formats, evaluation rubrics, and how to stand out
- [Question bank](interviews/07-question-bank.md) - real question patterns organized by round type


## Portfolio

- [What to build](portfolio/01-what-to-build.md) - the portfolio principles that separate deployment-shaped projects from tutorials
- [Project ideas](portfolio/02-project-ideas.md) - twelve customer-style project specs with built-in ambiguity and constraints
- [Presenting projects](portfolio/03-presenting-projects.md) - write-ups, demos, and metrics that make hiring managers believe you shipped


## Case Studies

- [Deployment patterns in the wild](case-studies/01-deployment-patterns-in-the-wild.md) - recurring shapes of real customer engagements
- [LLM deployment cases](case-studies/02-llm-deployment-cases.md) - documented enterprise LLM deployments and what they teach
- [Failure stories](case-studies/03-failure-stories.md) - the pilot-to-production cliff, documented failures, and the lessons each one teaches


## Job Market

- [Market overview](job-market/01-market-overview.md) - growth data, who is hiring, and role variants, with sources
- [Compensation](job-market/02-compensation.md) - sourced 2025-2026 figures and how to read them
- [Getting hired](job-market/03-getting-hired.md) - titles to search, signals that matter, and how to position your experience


## Resources

- [Tools](resources/01-tools.md) - the FDE toolbox: build, deploy, evaluate, observe
- [Reading](resources/02-reading.md) - books, blogs, and newsletters worth the time
- [Communities and people](resources/03-communities-and-people.md) - where FDEs and adjacent practitioners talk shop


## Work in progress

The repository is intentionally incomplete. Topics we know belong here but are not yet
written are tracked in [_work-in-progress/README.md](_work-in-progress/README.md).
Contributions welcome - read [STYLING.md](STYLING.md) first so your document matches the
rest of the guide.


## License

MIT - see [LICENSE](LICENSE).
