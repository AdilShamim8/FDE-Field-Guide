# What FDEs Actually Do: Responsibilities

If you are deciding whether the FDE role fits you, or writing a job description for one, this file shows the actual work. It is built on an independent scrape of 146 real FDE postings, read against two primary-source job descriptions, then translated into a weekly rhythm and a hiring checklist.

## What 146 job postings say

The best available measurement of the role is an [independent job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md) of 146 unique FDE postings from 94 companies, collected between February and July 2026 and preserved in our machine-readable [market dataset](../job-market/dataset/fde_market_data.json). Responsibilities extracted across the 146 postings:

| Responsibility Category | Postings Count (n=146) | Share of Postings | Practical Meaning for an FDE |
|---|---:|---:|---|
| **Building & Deploying Production Systems** | 132 | 90.4% | Writing resilient, production-grade code that runs inside customer VPCs or platform infra. |
| **Direct Customer & Client Collaboration** | 129 | 88.4% | Daily technical partnering with customer developers, enterprise architects, and VPs. |
| **Integrating Systems, APIs & Data** | 94 | 64.4% | Building pipelines across Snowflake, Postgres, SAP, legacy REST/GraphQL, and auth providers. |
| **Discovery & Requirements Scoping** | 76 | 52.1% | Decomposing vague executive mandates into buildable, costed engineering specifications. |
| **Evaluation, Testing & Monitoring** | 71 | 48.6% | Creating golden datasets, LLM-as-judge benchmarks, error taxonomies, and latency telemetry. |
| **Product Feedback Loop** | 45 | 30.8% | Codifying recurring customer friction into upstream product feature requests. |
| **Rapid Prototypes, POCs & Demos** | 42 | 28.8% | Building working 48-hour to 2-week vertical slices to ground executive discussions in real data. |
| **Travel & On-Site Co-location** | 13 | 8.9% | Embedding on-site inside customer headquarters during kickoffs and critical go-lives. |

Read the top two rows together: **90.4%** of postings demand production systems, and **88.4%** demand direct customer work. The role sits squarely on both disciplines at once. The middle rows show the daily engineering reality: integration is the most common technical task (64.4%), while discovery (52.1%) and evaluation (48.6%) are treated as core engineering responsibilities rather than delegated to pre-sales or QA.

Also from the same scrape analysis: 91.0% of postings were classified customer-facing, 11.0% were management roles, and exactly 0 postings were entry-level or junior titles.

The travel number deserves a caveat. Only 8.9% of postings formally spell out travel as a primary duty, but postings systematically understate it: Anthropic's posting states approximately 25% travel outright. Treat 8.9% as a floor, not an expectation.

For candidates, this table doubles as an offer-evaluation tool. If an interviewer cannot describe the top five rows from their team's last quarter, you are interviewing for a role adjacent to FDE work, not FDE work itself.

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

## The twelve principles of enterprise forward deployed engineering

Derived from the 2026 enterprise roadmap research and practitioner interviews with active FDEs across manufacturing, SaaS, and financial infrastructure:

1. Communication across native contexts - Effective communication is not about polished corporate English. Enterprise operators in manufacturing, logistics, and supply chain often communicate in regional languages. If an FDE cannot follow operational conversations in the team's native language, they miss the true business constraint.
2. Adaptability to hostile environments - Every enterprise client possesses an idiosyncratic architecture, culture, and governance cadence. What worked in an agile AWS startup will fail inside an air-gapped on-premise cluster. An FDE adapts to the customer's constraints rather than fighting them.
3. AI-native engineering discipline - Leverage modern AI development environments (such as Cursor, Claude, and Eraser.io) to compress the prototyping loop. The standard is shipping verified production code faster, not debating manual coding purity.
4. Confidence under uncertainty - In ambiguous requirements sessions, never fake comprehension. Ask clarifying questions with authority: "Help me understand this operational boundary: are we optimizing for technician driving time or first-visit parts availability?"
5. 48-hour velocity - Enterprise deadlines are driven by quarterly board reviews and seasonal audit cycles. Delivering a rough working vertical slice in 48 hours builds more customer trust than weeks of abstract architecture slides.
6. Cost-efficient model routing over generic functional AI - Implement bottom-up model routing. Use low-latency, cost-effective models (such as Gemini 2.5 Flash and Claude 3.5 Haiku) for high-volume classification and extraction, reserving frontier reasoning models only for high-ambiguity synthesis. Cost efficiency is a primary enterprise retention moat.
7. Declarative agentic systems over brittle hardcoding - Enterprise policies change weekly. If routing rules are hardcoded in source code, every business tweak requires an engineering deployment ticket. Expose declarative rules and dynamic agent configurations that customer operations leads can adjust safely.
8. Persistent dynamic memory layers - When the FDE disengages, the system cannot require ongoing developer triage. Capturing human supervisor corrections into a vectorized memory store enables the system to learn from customer edits automatically.
9. On-premise and air-gapped deployment fluency - Regulated clients will not route proprietary IP or customer PII through public multi-tenant APIs. FDEs must master private container registries, on-premise Kubernetes (such as Rancher and kubeadm), and local model execution (vLLM and Ollama).
10. Proactive AI governance and regulatory compliance - Legal and compliance gatekeepers can halt production launches on the day of deployment. FDEs must design for data residency laws (such as the Indian DPDP Act 2023, EU AI Act, and GDPR), immutable audit logging, and automated PII redaction by default.
11. Literacy in enterprise ERP systems of record - Enterprise AI applications exist to orchestrate core systems of record: SAP S/4HANA, Oracle NetSuite, and Microsoft Dynamics. FDEs must understand ERP schemas, transaction codes, and integration connectors (BAPI, OData, RFC) to build reliable mutations.
12. Non-technical user enablement and training - Systems fail when line operators refuse to use them. FDEs must conduct role-based training workshops and produce visual, jargon-free runbooks for depot dispatchers, procurement clerks, and field staff.

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
