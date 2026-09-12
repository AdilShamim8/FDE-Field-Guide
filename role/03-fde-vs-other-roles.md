# FDE vs Other Roles

For candidates comparing offers, hiring managers calibrating titles, and anyone who has tried to explain the difference between an FDE and a solutions engineer and come up short. You get four comparison axes, one compact table, and a sharp distinction for each of the closest role pairs.

## Why the title tells you almost nothing

Wikipedia notes that FDE responsibilities overlap with solutions architects, sales engineers, customer engineers, professional services engineers, systems integrators, and IT consultants (observed evidence, [Wikipedia](https://en.wikipedia.org/wiki/Forward_deployed_engineer)). An independent scrape of 146 FDE-shaped postings found the same work advertised as Applied AI Engineer, Solutions Engineer, and Deployment Engineer (observed evidence). Two companies can post the same title for different jobs, and two companies can post different titles for the same job.

So compare responsibilities, not titles. We recommend four axes.

The confusion has consequences. The adjacent roles differ in pay structure, career ceiling, travel, and daily stress, so a mislabeled offer is not a cosmetic problem: accepting a pre-sale job while expecting post-sale production work is the most common bad match in customer-facing engineering. The axes below are how you catch it before signing.

## Four axes for comparing customer-facing engineering roles

This framework is the guide's own (recommendation), built to separate roles that job titles blur:

- Engagement timing - does the work happen before the sale, after the sale, or embedded across the whole relationship
- What you ship - a demo, a scoped deliverable, or a production system running in the customer's environment
- Who owns the outcome long-term - your product team, the customer's team, a project office, or you until handover
- Whether you write production code inside customer systems - always, partly, or never

Two roles can share a title and differ on all four axes; two roles with different titles can be identical on all four. The table compresses the result, and the pairs below earn the nuance.

One worked example. A posting that says you will run discovery workshops with customer executives, build integrations against their internal APIs, and stay through production launch and iteration scores as embedded timing, production system, owner-until-handover, and always-writes-production-code: an FDE role. A posting that says you will deliver product demos, maintain demo environments, and support proof-of-concept evaluations until contract close scores as pre-sale, demo, hands-off-at-signature, and partly: a solutions engineer, whatever the title says.

## The comparison at a glance

| Role | Engagement timing | Ships | Long-term outcome owner |
| --- | --- | --- | --- |
| FDE | Embedded, mostly post-sale, discovery included | Production code in customer systems | FDE until handover, customer after |
| AI engineer | Product-internal | LLM features for many customers | Product team |
| Software engineer | Product-internal | Product code | Product team |
| Solutions engineer | Mostly pre-sale | Demos, PoCs, reference architectures | Hands off at signature |
| Sales engineer | Pre-sale | Demos, RFP responses, technical validation | Quota owner; hands off at close |
| ML engineer | Product-internal | Models, training and serving pipelines | Product team |
| Consultant | Project-scoped | Deliverables defined in a statement of work | Hands off at project end |
| Deployment strategist or TPM | Across the lifecycle | Plans, processes, enablement | The engagement process, not the code |

## The close pairs

### FDE vs AI engineer

Both build LLM applications, which is why the titles get confused. The difference is where the code runs and who you sit with. An AI engineer improves a product for many customers from inside the company; an FDE makes the product work for one demanding customer at a time, inside that customer's systems, data boundaries, and compliance rules. The AI engineer's enemy is roadmap sprawl; the FDE's enemy is a customer environment that refuses to behave like the documentation.

In practice the skills overlap heavily - prompt engineering, RAG, agents, evaluation - so posting data cannot separate the two roles; the environment can. Ask where the system runs in eighteen months, and who pages when it breaks.

### FDE vs software engineer

A software engineer works in one codebase the team controls, with stable tooling, shared on-call, and years of accumulated context. An FDE works in customer systems nobody on your team controls: unfamiliar stacks, restricted access, change processes owned by someone else, and timelines set by the customer's urgency. The engineering skills transfer directly; the working conditions do not. This is the most common transition into the role, and it fails on the customer-facing half more often than the coding half (see [from software engineer](../learning-paths/from-software-engineer.md)).

### FDE vs solutions engineer

The solutions engineer proves the product can work; the FDE makes it work. Solutions engineering is mostly pre-sale - demos, PoCs, technical validation, a reference architecture the customer could build. FDE work is post-sale production ownership: the integration actually built, deployed, evaluated, and handed over. The handoff is the tell: a solutions engineer celebrates the signature, an FDE treats the signature as the start. Many strong FDEs started as solutions engineers and added production depth (see [from solutions engineer](../learning-paths/from-solutions-engineer.md)).

### FDE vs sales engineer

The sales engineer carries a quota; the FDE does not (the consistent practitioner account across 2026 role comparisons). That single difference explains most of the behavioral gap. A sales engineer is optimized for the close: whatever gets the contract signed is the right demo. An FDE is optimized for the deployment: whatever gets the system into production and keeps it there is the right build. When a company puts a quota on an FDE, expect the work to drift toward demos, and expect production outcomes to drift away with it.

### FDE vs ML engineer

ML engineers work on model weights: training, fine-tuning, serving infrastructure. FDEs work on model APIs and application patterns: retrieval, structured output, agents, evaluation, and the surrounding system. The scraped skill data matches the split - the most demanded skills across the 146 postings were Python (91.0%), prompt engineering (55.0%), RAG (52.0%), and cloud platforms, with no model-training skill in the top twelve (observed evidence). If a posting wants you to train models, it is an ML role; if it wants you to make models work inside someone's business, it is FDE work.

### FDE vs consultant

Consultants deliver against a statement of work: scoped deliverables, a defined endpoint, then roll off to the next project. FDEs own outcomes across the lifecycle - through integration, deployment, evaluation, and iteration - and feed lessons back into the product they deploy (the consistent practitioner account across 2026 role comparisons). The billing model drives the behavioral difference: a consultant is paid for hours and deliverables, an FDE is paid, in effect, for the system working. Consultants also rarely shape product direction; a good FDE engagement changes the product for every future customer.

The statement of work is the tell in interviews: ask what happens when the customer's goal changes mid-project. A consultant re-scopes the contract; an FDE absorbs the change into the same outcome.

### FDE vs deployment strategist and TPM

Palantir hires Deployment Strategists as an explicitly non-engineering track (observed evidence, 2026), and many FDE teams pair the two roles. The strategist or technical program manager owns the process: stakeholder alignment, rollout plans, training, enablement, the calendar. The FDE owns the code that makes the process possible. The roles interlock - the strategist runs the room while the FDE builds the thing - and confusing them produces either an expensive meeting attendee or a system nobody was trained to use.

## The gray zone

Real roles blur. Some employers put pre-sale PoC work inside the FDE role; some put production code inside the solutions engineer role; systems integrators now run FDE-titled positions that look like classic statement-of-work delivery with a modern title. The title is marketing; the axes are the substance. The same week can produce one posting titled Forward Deployed Engineer that is a pre-sale demo role at a startup, and another titled Applied AI Engineer that is a genuine embedded production role at an enterprise vendor. Reading both against the four axes takes five minutes and settles it.

When you evaluate a posting, read for three signals (recommendation): whether it names production code in customer environments, whether the engineer is embedded with customer teams, and whether ownership continues after go-live. [The market overview](../job-market/01-market-overview.md) lists the title variants worth searching and how to read them. In interviews, ask who owns the system after handover - the answer separates FDE roles from everything else faster than any title will.

## Related documents

- [What is an FDE](01-what-is-an-fde.md) - the baseline definition the comparisons start from
- [Responsibilities](02-responsibilities.md) - the posting evidence behind the four axes
- [Market overview](../job-market/01-market-overview.md) - title variants and how to read postings
- [From software engineer](../learning-paths/from-software-engineer.md) - the most common transition into the role
- [From solutions engineer](../learning-paths/from-solutions-engineer.md) - the adjacent pre-sale role, and the bridge to FDE
- [From consultant](../learning-paths/from-consultant.md) - the transition for statement-of-work delivery backgrounds

## Further reading

- [Wikipedia: Forward deployed engineer](https://en.wikipedia.org/wiki/Forward_deployed_engineer) - the overlap list with adjacent roles, stated neutrally
- [Job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md) - similar-title evidence and the skill distribution cited above
