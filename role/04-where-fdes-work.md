# Where FDEs Work

For candidates targeting employers, and readers who want to know how much the job varies. The title spans at least seven employer types; this file walks each with evidence, then shows how the job changes by context and what to ask before accepting an offer.

## One title, many employers

An independent scrape of 146 FDE postings from 94 companies (February-July 2026) found the title at frontier model labs, data platforms, enterprise software vendors, consultancies, logistics companies, and healthcare companies (observed evidence, [scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)). Plank, tracking the same market in 2026, counted 982 live FDE postings across 462 companies (observed evidence, [joinplank.com](https://joinplank.com)).

The work behind the title shares one skeleton - [the FDE loop](05-the-fde-loop.md) - but the employer changes the travel, the autonomy, the stack, and the customer profile. Those differences are the content of this file.

### Frontier AI labs

OpenAI and Anthropic both hire FDEs (observed evidence: Wikipedia, plus the primary postings). The lab job is bringing the newest models into the most demanding enterprise systems: Anthropic's posting describes production applications with Claude models inside customer systems, white-glove deployment support for strategic enterprise customers, and a plus for vertical depth in financial services or healthcare; OpenAI runs healthcare and government FDE teams. Expect explicit travel (approximately 25% in Anthropic's posting), a high production-LLM bar, and a short feedback loop into the model and product teams.

### Enterprise platforms: Palantir

Palantir popularized the role and still runs the largest such organization. As of September 2026, Fortune counted roughly four dozen open forward-deployed positions there, including client-specific roles for Intel, NATO, and the Norwegian government (observed evidence). Palantir also hires Forward Deployed Infrastructure Engineers and non-engineering Deployment Strategists, which tells you the organization has specialized. Expect long engagements, sovereign and classified contexts, and heavy platform work mixed with custom builds.

### Hyperscalers

AWS hires the FDE title (observed evidence: Wikipedia). An Amazon Principal FDE posting describes an engineer who "embeds across multiple strategic enterprise customers to define the technical strategy and engineering [approach]" (observed evidence, amazon.jobs). Expect breadth over depth: many accounts, the full cloud service surface, and engagement running through enterprise and partner motions rather than a single embedded team.

### Data platforms

Data-platform companies featured prominently in the scrape sample, with Databricks accounting for the most listings of any company in the analysis (observed evidence). The job sits close to the customer's data estate: lakehouses, pipelines, and notebooks that must become production systems. If you enjoy the data-engineering half of [the FDE loop](05-the-fde-loop.md), this is where it dominates.

### Startups hiring their first FDE

Plank's 2026 collection highlights growth-stage AI products hiring their first FDE (observed evidence). The first-FDE job is different in kind: no playbook exists, the engagement model is yours to define, and the feedback loop to the founders is one conversation long. The trade is autonomy versus infrastructure - there is usually no support organization behind you, so you are also the support organization.

### Systems integrators and consultancies

Deloitte posts "Anthropic Forward Deployed Engineer - GPS" roles that embed with clients to translate high-value GenAI use cases into deployed solutions (observed evidence, 2026). This is the FDE motion being resold: the integrator embeds engineers to deploy another vendor's AI products at scale. Expect multi-client rotation, the integrator's delivery methodology layered on top of the vendor's technology, and less influence over the product itself.

### Defense and government

OpenAI's government FDE posting frames the job as "technical thought partner" for defense, intelligence, and federal stakeholders (observed evidence, 2026), and Palantir's client-specific NATO and government roles sit in the same territory. Practitioner commentary also reports steady demand for clearance-eligible FDEs - treat that as industry pattern rather than measured data, and verify clearance requirements before applying, because they gate the entire hiring process.

## How the job changes by context

The skeleton stays; the dials move (industry patterns drawn from the employer types above):

- Travel share - roughly 25% at frontier labs per Anthropic's posting; posting text understates travel generally (9.0% of the 146 postings mention it, yet the same sample includes postings at 25%); Palantir-lineage and government work is the most onsite-heavy
- Custom-versus-product ratio - first-FDE startups are mostly custom work on a thin product; platform vendors are mostly product configuration plus glue; labs mix both, with the custom side feeding the product
- Support maturity - startups: you are tier one through three; enterprises: a real support organization exists, and your job is to stay out of its way unless something is genuinely broken
- Autonomy - the first FDE defines the playbook; lab and platform FDEs inherit patterns that staff FDEs codified
- Stack variety - hyperscalers and integrators rotate across many stacks; lab FDEs go deep on their own SDKs and model APIs

None of these dials is good or bad on its own. Heavy onsite work suits people who like immersion and burns people who do not; low support maturity means high autonomy and no safety net. The point of the list is to make the trade explicit before you accept it, not after.

## Questions to ask before you take the job

The employer type sets the defaults, but individual teams vary widely. Ask these during the interview process (recommendation):

- [ ] What share of the team's revenue or roadmap depends on the top three customers?
- [ ] Who owns the system after handover - a named team, or nobody?
- [ ] Is there a named path for field lessons to reach the product roadmap, and can you point to something that shipped because of it?
- [ ] What is the actual travel expectation for this team, in weeks per month, over the last quarter?
- [ ] Who is on-call for customer deployments, and what does escalation look like at 2am?
- [ ] How many engagements has this team run end to end, and what happened to each?

The last question does double duty: teams that can answer it have a working feedback loop, and teams that cannot are still improvising the role.

## Related documents

- [FDE vs other roles](03-fde-vs-other-roles.md) - the same employer variety applies to the adjacent titles
- [Responsibilities](02-responsibilities.md) - what stays constant across employers
- [Compensation](../job-market/02-compensation.md) - how pay varies by employer type, with sources
- [Deployment patterns in the wild](../case-studies/01-deployment-patterns-in-the-wild.md) - engagements shaped by employer context
- [The interview process](../interviews/01-interview-process.md) - how interview loops differ by employer

## Further reading

- [Fortune on the FDE boom](https://fortune.com/2026/09/03/forward-deployed-engineers-fast-growing-six-figure-silicon-valley-job-integrate-ai-with-customers-tech-careers-palantir) - Lightcast data and the Palantir position count (September 2026)
- [Palantir careers](https://www.palantir.com/careers/) - the largest single FDE organization, including the infrastructure and strategist variants
- [OpenAI careers](https://openai.com/careers) - healthcare and government FDE postings
- [Plank](https://joinplank.com) - the 982-posting, 462-company collection, with first-FDE startups called out (2026)
- [Deloitte careers](https://apply.deloitte.com) - search for the "Anthropic Forward Deployed Engineer" roles
