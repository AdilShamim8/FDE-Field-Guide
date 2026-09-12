# Deployment Patterns in the Wild

Real engagements take recurring shapes, and the shape you are in decides what good looks
like. This document describes the five engagement patterns observable in public evidence
and practitioner reporting, each with its evidence trail, what makes it work, and what
breaks it. It complements [reference architectures](../system-design/02-reference-architectures.md),
which is the engineering view of the same deployments; this is the engagement view - who
owns what, who pays, and where the motion breaks.

## The patterns

### The embedded lab engagement

The shape: an AI lab's FDE team embeds with a strategic enterprise customer to ship a
production LLM application inside that customer's systems. The evidence trail is direct
(observed evidence): Anthropic's FDE job description centers on building production
applications with Claude models inside customer systems, delivering MCP servers, sub-agents,
and agent skills for production workflows, with white-glove deployment support and roughly
25% travel ([Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008)).
The New Stack (May 2026) describes the same motion externally: FDE teams integrate systems,
launch in production, and improve the deployment as issues appear
([The New Stack](https://thenewstack.io/forward-deployed-engineers-ai)).

What makes it work is the white-glove ratio: small senior teams, few customers, direct
access to executives, and end-to-end ownership from discovery through handover. The most
instructive line in the job description is the one about identifying and codifying
repeatable deployment patterns and feeding them back to product and engineering - the
engagement is designed to produce reusable assets, not just one deployment. What breaks it
is the economics of attention: a model that scales by seniority and focus hits a ceiling
fast, and it inverts when a customer treats the embedded team as extra headcount for a
backlog the customer's own engineers declined.

### The platform-bootcamp pattern

The shape: a platform vendor embeds engineers who build alongside customer teams, in
intensive sprints, so the customer learns to build on the platform rather than receiving a
finished system. This pattern is documented mainly through Palantir, which popularized the
FDE title ([Wikipedia](https://en.wikipedia.org/wiki/Forward_deployed_engineer)) and
describes dropping "the best software engineers in the world" out of a comfortable office
"to spend their days in the service of incredibly skilled but non-technical [customers]"
(via Fortune, September 2026). The same coverage quotes the FDSE listing: "your
responsibilities look similar to those of a startup CTO: you'll work in small teams with
minimal supervision and own end-to-end execution of high stakes projects."

What makes it work is the transfer: because the customer's people build with you, the
capability and the system both stay behind at handover, which is why this pattern survives
vendor rotation better than a delivery engagement. What breaks it is bench depth on the
customer side - when the customer has no engineers to pair with, the bootcamp silently
becomes a fully-resourced delivery engagement priced as a training one. The startup-CTO
mandate also collides with the customer's procurement, security review, and change
processes, and the FDE eats that collision personally.

### The SI-resold deployment

The shape: a systems integrator runs the FDE motion on a vendor's behalf, embedding its own
engineers to deliver the vendor's technology into enterprise clients. The evidence is
observed: Deloitte posts roles titled "Anthropic Forward Deployed Engineer - GPS",
embedding with clients to translate high-value GenAI use cases into solutions
([Deloitte careers](https://apply.deloitte.com), 2026). Wikipedia lists systems integrators
and IT consultants among the roles FDE work overlaps with, which makes the boundary the
interesting part.

What changes in this pattern is management and scope discipline. The FDE now serves two
masters: the customer day to day, and the integrator's engagement economics - billable
scope, utilization, and statement-of-work boundaries - the rest of the time. FDE logic says
own the outcome; SOW logic says do what the contract says. Where the pattern works, the
integrator contributes what a lab cannot staff: procurement muscle, a compliance bench, and
scale across accounts. Where it breaks, outcome ownership goes fuzzy at the contract
boundary, and the codify-patterns feedback loop weakens because the field team and the
product team sit in different companies with different incentives.

### The first-FDE startup motion

The shape: a growth-stage AI product company hires its first FDE to unblock enterprise
deals the product cannot close on its own. The evidence is observed: Plank collected 982
live FDE postings across 462 companies in 2026 and notes growth-stage AI products hiring
their first FDE ([Plank](https://joinplank.com)). The independent scrape of 146 postings
found no junior titles, which says the first FDE hire is a senior hire expected to operate
without a support structure
([scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)).

What makes it work is proximity: the FDE sits inside the deal cycle, converts logos the
product cannot close with a layer of custom work, and feeds discovery straight into the
roadmap with no organizational distance. What breaks it is custom-work sprawl: every deal
gets bespoke engineering, the product never absorbs the patterns, margins erode, and the
FDE becomes a one-person professional-services department. Where this motion survives, the
company keeps a written bar for what must be generalized into the product - the same
codify instinct the lab engagement mandates, enforced by a team that cannot afford to
rebuild the same integration twice.

### The government and defense deployment

The shape: long procurement cycles, cleared personnel, restricted or air-gapped
environments, and a bespoke deployment per agency or program. Treat this pattern as mostly
an industry pattern - public evidence is thinner because the work is less publishable. The
traceable evidence: Palantir's government business is the reference case, and Fortune
(September 2026) counted roughly four dozen open forward-deployed positions including
client-specific roles for Intel, NATO, and Norway
([Fortune](https://fortune.com/2026/09/03/forward-deployed-engineers-fast-growing-six-figure-silicon-valley-job-integrate-ai-with-customers-tech-careers-palantir)).
OpenAI's government FDE posting describes a "technical thought partner" for defense,
intelligence, and federal stakeholders ([OpenAI careers](https://openai.com/careers), 2026).

What makes it work is patience and compliance-as-design: accreditation, not code, is the
critical path, and engineers who treat the security constraints as requirements rather than
obstacles are the ones who ship. What breaks it is the gap between demo speed and approval
speed, staff rotation on the customer side that resets relationships mid-engagement, and
environments that forbid the cloud tooling the team's habits were built on. Wikipedia also
notes the role's documented criticisms - travel burden and pressure on short timelines -
which are acute in this pattern.

## Cross-cutting lessons

Across all five patterns, the same three things decide outcomes (interpretation, drawn from
the evidence above and the guide's engineering sections):

- Data access - every pattern lives or dies on whether the system can reach real data under real permissions; the bootcamp pattern hides this least, the government pattern hides it most
- Named ownership - someone on the customer side owns the system after the vendor leaves, or the deployment decays regardless of how well it shipped
- The evaluation bar - a number both sides agreed on in advance, or every quality conversation reverts to taste and the loudest stakeholder wins

This suggests pattern recognition is a week-1 skill: the tells are visible early if you look.

- Embedded lab - you have a named executive sponsor, a narrow strategic scope, and a mandate to codify what you learn
- Platform bootcamp - you are pairing with customer engineers who will keep the system after you leave
- SI-resold - there is a statement of work behind you and a delivery manager who is not your customer
- First-FDE startup - sales is in your standup and there is no product feedback loop yet
- Government and defense - accreditation, clearances, and procurement, not code, are the long pole

We recommend naming your pattern out loud in week 1, because each pattern fails differently
and the failure you should be watching for is the one your pattern specializes in. The
failure catalog itself lives in [failure stories](03-failure-stories.md).

## Related documents

- [Reference architectures](../system-design/02-reference-architectures.md) - the engineering view of the same deployments
- [Deployment patterns](../deployment/02-deployment-patterns.md) - the tenant, SaaS, hybrid, and on-prem shapes these engagements produce
- [The engagement lifecycle](../customer/01-engagement-lifecycle.md) - the phase model every pattern walks, phase by phase
- [Where FDEs work](../role/04-where-fdes-work.md) - the employer types behind each pattern
- [Prototype to production](../deployment/01-prototype-to-production.md) - the crossing every pattern has to manage deliberately
- [Failure stories](03-failure-stories.md) - what these patterns look like when they stall

## Further reading

- [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) - the embedded-lab pattern in the vendor's own words
- [The New Stack on FDE teams](https://thenewstack.io/forward-deployed-engineers-ai) - integrate, launch, improve: the lab motion described externally (May 2026)
- [Fortune on the FDE job market](https://fortune.com/2026/09/03/forward-deployed-engineers-fast-growing-six-figure-silicon-valley-job-integrate-ai-with-customers-tech-careers-palantir) - Palantir's model, clients, and the platform-bootcamp evidence (September 2026)
- [Plank](https://joinplank.com) - the posting data behind the first-FDE startup motion (2026)
- [Wikipedia: Forward deployed engineer](https://en.wikipedia.org/wiki/Forward_deployed_engineer) - role history and the overlap with integrators and consultants
