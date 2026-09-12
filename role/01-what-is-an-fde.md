# What Is a Forward Deployed Engineer

If you have seen the title "forward deployed engineer" in a job list and want a straight answer, start here. You will get the sourced definition, the Palantir origin story, the AI-era version that is driving current hiring, and the misconceptions that cause people to misjudge the role.

## The definition

[Wikipedia defines the role](https://en.wikipedia.org/wiki/Forward_deployed_engineer) as follows (observed evidence, retrieved 2026):

> A forward-deployed engineer (FDE), also called a forward-deployed software engineer (FDSE), is a customer-facing software engineer who develops and deploys software within a client company, often working alongside the client's employees for a defined period of time.

Three parts of that sentence carry the whole job:

- Customer-facing - the engineer talks directly to the people whose problem is being solved, regularly, not through an intermediary
- Develops and deploys software - this is engineering, not advisory work; the output is running code in production
- Within a client company - the work happens inside the customer's systems, constraints, and culture, which changes how engineering gets done

## Where the role came from

### Palantir built the playbook

Palantir popularized the role (Wikipedia). The clearest statements of the original intent come from Palantir itself, quoted in Fortune's September 2026 analysis of the FDE boom:

> We hired the best software engineers in the world, ejected them from the comfort of a Palo Alto office, and dropped them in remote locations to spend their days in the service of incredibly skilled but non-technical [customers].

And from a Palantir FDSE job listing quoted in the same article:

> As an FDSE, your responsibilities look similar to those of a startup CTO: you'll work in small teams with minimal supervision and own end-to-end execution of high stakes projects. Your day might span discussing architecture with fellow engineers, wrangling massive-scale data, coding a custom web app, speaking with customer executives, or establishing strategy for your team.

Both quotes describe the same design: end-to-end engineering ownership, in direct contact with the customer, with as little organizational insulation as possible. The startup-CTO comparison is the most reusable shorthand for the role that exists.

### The AI era made it a mainstream hiring category

Wikipedia notes that AWS, OpenAI, and Anthropic all hire the title, and that openings grew significantly in 2024-2025. Fortune's September 2026 analysis, citing Lightcast data, put numbers on the surge: FDE postings up more than 1000% year over year, against broader tech posting growth of 13% (observed evidence; the full market data lives in [the market overview](../job-market/01-market-overview.md)).

The New Stack (May 2026) gives the reasoning: large customers need AI systems integrated, launched in production, and improved as issues appear, and that work does not fit a normal product engineering schedule (observed evidence). The motion has also spread beyond the labs themselves: Deloitte now posts "Anthropic Forward Deployed Engineer" roles that embed with Deloitte's clients to turn GenAI use cases into deployed solutions (observed evidence, 2026). When systems integrators start reselling a role, the role has become infrastructure.

## The one-sentence mental model

An FDE is the bridge between the customer problem, the product capability, and the engineering implementation: the person who turns an ambiguous business problem into a working production system.

Everything else in this guide expands that sentence. Remove one anchor and the role collapses into a neighbor: remove the customer problem and you have a product engineer; remove the product capability and you have a consultant; remove the engineering implementation and you have a sales engineer.

## What makes the role distinct

The distinct property is end-to-end ownership across the whole engagement lifecycle. Most engineering roles own a slice: a codebase, a model, a roadmap quarter, a demo. The FDE owns the arc from "we have a problem" to "the system is in production and moving a business metric".

Postings back this up. An independent analysis of 146 FDE postings from 94 companies (scraped February-July 2026) found that 90.0% mention building production systems and 88.0% mention direct customer work (observed evidence, [scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)). Many roles require one of the two. Very few require both, and almost none require both at once, inside the customer's environment. That combination is the job.

## Common misconceptions

### It is basically a sales engineer

No. Sales engineers work pre-sale: demos, PoCs, RFP responses, quota-adjacent targets. FDEs work after the sale, write production code inside customer systems, and carry deployment outcomes instead of revenue targets (the consistent practitioner account; see [FDE vs other roles](03-fde-vs-other-roles.md) for the sharp version).

### It is consulting with a laptop

Close, and wrong in one specific way. Consultants deliver scoped deliverables against a statement of work and then roll off. FDEs own the outcome across the lifecycle - through integration, deployment, evaluation, and iteration - and are expected to feed lessons back into the product. The deliverable is a working system, not a document.

### It is a support role with a better title

Support engineers react to tickets on systems someone else built. FDEs build the system, then live with the consequences of their own design decisions, then fix the design. The escalation path points at you.

### It is a junior travel job

The evidence says the opposite. The 146-posting analysis found no junior titles among FDE listings; 91.0% of postings were classified customer-facing and 11.0% were management roles (observed evidence). Anthropic's posting asks for 4+ years in a technical customer-facing role. Travel exists but is smaller than the stereotype: only 9.0% of postings list travel or onsite work as a responsibility, though postings understate it - Anthropic states approximately 25% travel explicitly in the same market.

### It is demo work

Only 29.0% of the 146 postings mention prototypes, PoCs, or demos, against 90.0% that mention production systems. The ratio tells you where the center of gravity is: the demo is a tool inside the job, not the job.

### The honest downsides

Wikipedia is blunt about the criticisms: travel requirements and pressure to solve problems on short timelines make the role undesirable to some engineers. Both are real. Travel is manageable at most employers, but the timeline pressure is structural - customers buy FDE engagements because something is urgent, and the urgency does not pause because you find it inconvenient. If you need long, protected refactoring horizons, this is the wrong role. If you like being the person who closes things, it is hard to beat.

## The title landscape

The same work appears under several names: the scrape analysis lists Applied AI Engineer, Solutions Engineer, and Deployment Engineer as titles observed on FDE-shaped postings, and Wikipedia adds forward-deployed software engineer (FDSE) as a direct synonym (observed evidence). Adjacent titles are not the same job: Palantir's Deployment Strategist is explicitly non-engineering, and Amazon's Principal FDE reads as an embedded chief architect.

We recommend reading responsibilities, not titles. [FDE vs other roles](03-fde-vs-other-roles.md) gives you the axes for that, and [where FDEs work](04-where-fdes-work.md) shows how the same title shifts by employer.

## Related documents

- [Responsibilities](02-responsibilities.md) - the concrete work behind the definition, weighted by 146 postings
- [FDE vs other roles](03-fde-vs-other-roles.md) - if this definition sounds like a role you know, check the sharp differences
- [Where FDEs work](04-where-fdes-work.md) - how the same title changes across labs, platforms, startups, and integrators
- [The FDE loop](05-the-fde-loop.md) - the mental model that makes the definition concrete
- [Market overview](../job-market/01-market-overview.md) - the hiring data behind the role's rise

## Further reading

- [Wikipedia: Forward deployed engineer](https://en.wikipedia.org/wiki/Forward_deployed_engineer) - neutral definition, role history, and the overlap with adjacent roles
- [The New Stack: why AI labs hire FDE teams](https://thenewstack.io/forward-deployed-engineers-ai) - the rationale for the 2025-2026 hiring wave (May 2026)
- [Fortune on the FDE boom](https://fortune.com/2026/09/03/forward-deployed-engineers-fast-growing-six-figure-silicon-valley-job-integrate-ai-with-customers-tech-careers-palantir) - Lightcast growth data and the Palantir quotes (September 2026)
- [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) - a complete real posting, useful as the concrete reference for the role
