# What FDEs Actually Do: Responsibilities

If you are deciding whether the FDE role fits you, or writing a job description for one, this file shows the actual work. It is built on an independent scrape of 146 real FDE postings, read against two primary-source job descriptions, then translated into a weekly rhythm and a hiring checklist.

## What 146 job postings say

The best available measurement of the role is an [independent job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md) of 146 unique FDE postings from 94 companies, collected between February and July 2026 (observed evidence). Responsibilities mentioned across postings:

| Responsibility | Share of postings |
| --- | --- |
| Building production systems | 90.0% |
| Direct customer work | 88.0% |
| Integrating systems, APIs, and data | 64.0% |
| Scoping requirements and discovery | 52.0% |
| Evaluation, testing, and monitoring | 49.0% |
| Feeding field lessons back to product | 31.0% |
| Prototypes, PoCs, and demos | 29.0% |
| Travel or onsite work | 9.0% |

Read the top and bottom rows together. Nine in ten postings demand production systems, and nearly nine in ten demand direct customer work - the role sits on both at once. The middle rows are the daily texture: integration is the most common concrete engineering task, and half the postings treat discovery and evaluation as FDE work rather than handing them to separate teams. This suggests employers see discovery and evaluation as engineering activities, not pre-sales or QA activities.

Also from the same analysis: 91.0% of postings were classified customer-facing, 11.0% were management roles, and none were junior titles (observed evidence).

The travel number deserves a caveat. Only 9.0% of postings list travel as a responsibility, but postings systematically understate it: Anthropic's posting states approximately 25% travel outright. Treat 9.0% as a floor, not an expectation.

For candidates, the table doubles as an offer-evaluation tool. If an interviewer cannot describe the top five rows from their own last quarter, you are interviewing for a role adjacent to FDE work, not FDE work itself. The checklist at the bottom of this file turns that test into questions you can ask directly.

Market growth for these postings (listings grew 4.2x over the scrape window) is covered in [the market overview](../job-market/01-market-overview.md). This file is about the work, not the demand.

## Anatomy of a real posting

Averages say what FDEs do; full postings show how employers phrase it. Two primary sources are worth reading in full.

### Anthropic, Forward Deployed Engineer, Applied AI team

From the [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) (observed evidence; details as listed in 2026 and they change fast):

- Build production applications with Claude models inside customer systems
- Deliver MCP (Model Context Protocol) servers, sub-agents, and agent skills for production workflows
- Provide white-glove deployment support for strategic enterprise customers
- Identify and codify repeatable deployment patterns, and feed insights back to Product and Engineering
- Maintain current knowledge of the latest LLM capabilities
- Build long-term customer relationships and identify new deployment opportunities
- Approximately 25% travel; locations New York, San Francisco, and Seattle
- Annual salary listed at $280,000 to $320,000 USD as posted (2026)

The requirements side is equally specific: 4+ years in a technical customer-facing role (FDE, or software engineer with consulting experience), production LLM experience including prompt engineering, agent development, and evaluation frameworks, Python plus ideally TypeScript or Java, high agency in ambiguity, and a vertical background in financial services or healthcare as a plus.

Every clause maps to a stage of [the FDE loop](05-the-fde-loop.md): discovery sits inside the relationship-building clauses, implementation in the MCP servers and sub-agents, deployment in the white-glove support, iteration and scale in the codify-repeatable-patterns clause that feeds Product and Engineering.

### OpenAI, Forward Deployed Engineer

OpenAI's FDE postings (healthcare and government, 2026) compress the role into one line: lead "technical discovery, architecture, implementation, evaluation, productionization, and handoff, translating complex customer workflows" (observed evidence, [OpenAI careers](https://openai.com/careers)). The government variant adds "technical thought partner" for defense, intelligence, and federal stakeholders.

That sentence is [the FDE loop](05-the-fde-loop.md) with the nouns stripped out. When a job description and a mental model agree this closely, the mental model is useful.

## The weekly rhythm

No two weeks match, and any week containing a go-live looks nothing like a quiet week. That said, most FDE teams converge on a rhythm that looks something like the following (industry pattern; the split is illustrative, not measured data):

- Customer conversations - 15-25% of the week: discovery interviews, status reviews, and unblocking decisions only the customer can unblock
- Writing production code - 30-40%: the integration, the pipeline, the agent, the eval harness
- Integration debugging - 10-20%: auth flows, rate limits, schemas, environments, and the customer's staging quirks
- Evaluation runs and analysis - 10-15%: golden sets, regression runs, judging outputs, arguing about rubrics
- Write-ups and internal sync - 10-15%: engagement notes, decision records, and the feedback that goes back to the product team

Two habits separate strong weeks from weak ones. First, the write-ups are not overhead: they are how field lessons reach the product, which 31.0% of postings list as a responsibility. Second, customer conversations appear in every strong week even when there is nothing to demo; engineers who go quiet between milestones are the ones who get surprised by requirements.

## How responsibilities shift with seniority

The responsibilities stay constant; the scope you hold them over changes (industry pattern, drawn from practitioner career-ladder write-ups and 2026 postings):

- Early-career FDEs ship components - an integration, an eval harness, one agent inside a larger engagement, reviewed by a senior
- Senior FDEs own engagements - scope, deliver, deploy, hand over, and keep the customer relationship intact while doing it
- Staff and principal FDEs set patterns others reuse - the codify-and-feed-back clause in Anthropic's posting is this job; Amazon's Principal FDE posting describes defining technical strategy across multiple strategic enterprise customers

This suggests a simple self-check: ask which stages of [the FDE loop](05-the-fde-loop.md) you could run alone today, and which you could teach. Ladders commonly run about five levels from FDE to Director, and both Amazon (Principal FDE) and Anthropic (Head of Forward Deployed Engineering) hire at the top of that range (observed evidence, 2026 postings and practitioner guides).

## If your job description does not include these, it is not an FDE role

Hiring managers: a posting can carry the FDE title and still be one of the adjacent roles described in [FDE vs other roles](03-fde-vs-other-roles.md). Run this checklist against your own description; call the role what it is:

- [ ] Writing production code that runs inside customer environments, not only demos
- [ ] Regular direct conversations with customer engineers and executives, without a chaperone
- [ ] Discovery and scoping owned by the engineer, not delegated entirely to pre-sales
- [ ] Integration with customer data, systems, and identity providers
- [ ] Ownership through deployment, evaluation, and iteration after go-live
- [ ] A named path for field lessons to reach the product roadmap

A posting with four or more of these is an FDE role. A posting with only the demo and relationship lines is a solutions or sales engineering role. A posting with none of them is a support or services role wearing the title.

## Related documents

- [What is an FDE](01-what-is-an-fde.md) - the definition these responsibilities add up to
- [The FDE loop](05-the-fde-loop.md) - the same work organized as a sequence you can run
- [Core technical skills](../skills/01-core-technical-skills.md) - the skill base these responsibilities assume
- [The engagement lifecycle](../customer/01-engagement-lifecycle.md) - how the responsibilities map onto engagement phases
- [Market overview](../job-market/01-market-overview.md) - demand data and where the posting sample came from

## Further reading

- [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) - the most detailed primary-source FDE posting available (2026)
- [OpenAI careers](https://openai.com/careers) - search "Forward Deployed Engineer" for the discovery-through-handoff framing
- [Job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md) - the 146-posting dataset behind the table above
- [Amazon jobs](https://www.amazon.jobs) - search "Principal Forward Deployed Engineer" for the senior end of the role
