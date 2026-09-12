# Getting Hired as an FDE

If you have read the market overview and want to convert that demand into applications and offers, this file is the bridge between the market data and the interview preparation. It covers where the roles actually post, the signals employers print in their own job descriptions, how to position each background, and the artifacts your application needs. The interview loop itself lives in [the interview process](../interviews/01-interview-process.md); this file gets you to the loop in good shape.

## Where to look

### Titles to search

The title is fragmenting, so we recommend searching all of these, not just one:

- Forward Deployed Engineer - the standard title
- Forward Deployed Software Engineer - Wikipedia lists this as an alternate name for the same role; Palantir's variant
- FDE - used in posting titles as an abbreviation
- Applied AI Engineer - observed in the 146-posting scrape analysis as a near-equivalent
- Deployment Engineer - observed in the same analysis
- Solutions Engineer - adjacent rather than equivalent, with pre-sale weighting; worth watching because some teams use the titles loosely

A search on "FDE" alone misses a material share of postings, because boards lag the renames.

### Where the postings concentrate

- Aggregators and boards - Indeed data showed FDE postings 543% higher in April 2025 than January 2025 (Business Insider, May 2026), so board alerts on the title list above work; expect the volume there
- Company career pages - labs and platforms post first on their own pages: [Anthropic](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) via its board, [OpenAI careers](https://openai.com/careers), [Palantir careers](https://www.palantir.com/careers/), and [amazon.jobs](https://www.amazon.jobs)
- The systems-integrator route - Deloitte posts "Anthropic Forward Deployed Engineer - GPS" roles ([Deloitte careers](https://apply.deloitte.com)); search integrator career sites for the vendor name plus FDE, because the posting titles embed it
- The first-FDE startup angle - Plank's 2026 collection (982 postings, 462 companies) highlights growth-stage AI products hiring their first FDE ([joinplank.com](https://joinplank.com)); the autonomy is real and so is the absence of a support organization, a trade described in [where FDEs work](../role/04-where-fdes-work.md)

## What signals employers actually ask for

The strongest evidence is what employers themselves print. Three primary sources cover the range:

- Anthropic, Forward Deployed Engineer, Applied AI team (2026 posting) - 4+ years in a technical customer-facing role; production LLM experience spanning prompt engineering, agent development, and evaluation frameworks; Python plus ideally TypeScript or Java; high agency in ambiguity; communication strong enough to run discovery; a vertical background in financial services or healthcare as a plus. The full anatomy is in [responsibilities](../role/02-responsibilities.md).
- OpenAI (2026 postings, healthcare and government) - ownership of the whole arc: lead technical discovery, architecture, implementation, evaluation, productionization, and handoff
- Amazon, Principal FDE (2026 posting) - defining the technical strategy and engineering approach across multiple strategic enterprise customers

Translate each signal into resume language rather than echoing the posting (recommendation). The signals map to five kinds of evidence:

- Systems shipped with real users - name the system, the environment it ran in, and your specific slice of it
- Integrations built - name the systems you connected and the failure modes you had to handle; 64.0% of scraped postings list integration work
- Incidents survived - the on-call story, the diagnosis, and the fix that stuck
- Metrics moved - eval pass rates, latency, adoption, cost, or revenue, with numbers
- Field lessons fed back - 31.0% of scraped postings list codifying repeatable patterns and feeding them to product; an internal tooling, runbook, or pattern-library line demonstrates the same instinct

If a signal has no corresponding evidence in your history, build the evidence before applying; [what to build](../portfolio/01-what-to-build.md) is the plan for that.

## Positioning by background

Six backgrounds cover most candidates. Each entry is one line of strength and one gap to close; the learning paths carry the full plans.

### From software engineering

You have the production half that 90.0% of postings demand, and it is the scarcer half in the applicant pool. The gap is customer-facing ownership: discovery, expectation management, and shipping in someone else's environment. Start at [from software engineer](../learning-paths/from-software-engineer.md).

### From AI or ML engineering

You have the model and evaluation fluency the labs screen for. The gap is delivery: getting a system through integration, deployment, and iteration inside a customer's constraints. Start at [from AI/ML engineer](../learning-paths/from-ai-ml-engineer.md).

### From data engineering

Pipelines and integration are the unglamorous majority of real engagements, and you already do them under production constraints. The gap is the LLM application layer and executive-facing communication. Start at [from data engineer](../learning-paths/from-data-engineer.md).

### From solutions engineering

You have the customer instinct, the discovery skills, and the demo craft. The gap is post-sale production ownership: code that runs after the contract is signed. Start at [from solutions engineer](../learning-paths/from-solutions-engineer.md).

### From consulting

You can run the room, scope the work, and manage stakeholders. The gap is engineering ownership: shipping and maintaining the system yourself rather than delivering a deck. Start at [from consultant](../learning-paths/from-consultant.md).

### From the beginning

Be honest about the evidence: the scrape found zero junior titles in 146 postings, and Anthropic requires 4+ years. Target an adjacent first role - junior software engineering, support engineering, implementation consulting - while building deployment evidence. [The beginner path](../learning-paths/beginner-to-fde.md) maps the route without pretending it is short.

## The application artifacts

### Resume rules

Run every posting against the five-evidence list above and mirror its nouns: if the posting says evaluation frameworks, your eval work should use that phrase in its bullet. Tailoring is reading, not rewriting.

- Outcomes with numbers, not responsibilities - "cut ticket triage from 4 hours to 20 minutes" beats "responsible for support tooling"
- Customer-facing scope visible - who you embedded with, what you shipped into their environment, and what you owned after go-live
- Production systems named - real systems with real users; tutorials and coursework go in a separate line or nowhere
- The second language on the page - Python plus TypeScript or Java is a stated requirement at Anthropic, so a single-language resume undersells you against a stated bar

### The cover note

One deployment story in five lines works: the customer's problem, the constraint that made it hard, what you shipped, what broke, and the number that improved afterward. Specific beats comprehensive; a hiring manager screening FDE applications is looking for evidence you have stood in the room. If the story is from an adjacent role - support, consulting, internal tooling - say so plainly and let the specifics carry it.

### What not to do

- Title-only claims - "worked closely with customers" with nothing shipped does not survive one interview question
- Unquantified "led" bullets - led what, for whom, to what result
- A portfolio of tutorials wearing production language - evaluators check; [presenting projects](../portfolio/03-presenting-projects.md) shows how to present honestly and well

## Interview preparation map

The loop - stages, evidence, and scoring - is documented in [the interview process](../interviews/01-interview-process.md). A four-week outline for preparation, assuming nights-and-weekends hours alongside a job (recommendation):

1. Week 1 - process and positioning: read the interview-process file, draft your six ownership stories ([behavioral rounds](../interviews/05-behavioral.md)), and rebuild the resume around outcomes
2. Week 2 - technical depth: coding and technical rounds ([coding and technical](../interviews/02-coding-and-technical.md)), with emphasis on Python, APIs, and integration reasoning
3. Week 3 - design and scenarios: customer-flavored system design ([system design rounds](../interviews/03-system-design.md)) and discovery role-plays ([customer scenarios](../interviews/04-customer-scenarios.md))
4. Week 4 - live fire: take-home practice ([take-homes](../interviews/06-take-homes.md)), drill the [question bank](../interviews/07-question-bank.md), run two mock loops with a peer, and keep one portfolio project demoable ([project ideas](../portfolio/02-project-ideas.md))

If you have more than four weeks, extend weeks 2 and 3 rather than adding new topics; depth on the same material is what loops reward.

## Related documents

- [Market overview](01-market-overview.md) - where demand sits before you spend the effort
- [Compensation](02-compensation.md) - know the band before the recruiter call
- [What to build](../portfolio/01-what-to-build.md) - closing evidence gaps before you apply
- [The interview process](../interviews/01-interview-process.md) - the loop this file prepares you for
- [Learning paths overview](../learning-paths/README.md) - picking the path that matches your background

## Further reading

- [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) - the requirements translated above, in full
- [OpenAI careers](https://openai.com/careers) - the discovery-through-handoff posting language
- [Plank](https://joinplank.com) - first-FDE startup listings and market collection (2026)
- [The job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md) - titles and signals across 146 postings
