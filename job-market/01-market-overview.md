# FDE Market Overview

If you are deciding whether to spend months moving toward this role, benchmarking a hiring plan, or sizing the market before a negotiation, this file collects the demand evidence in one place. The FDE title went from a Palantir specialty to one of the fastest-growing job categories in tech in about two years. Every claim below carries a source and a date; the figures move fast, so re-check any of them before relying on it.

## Growth evidence

Four independent measurements point in the same direction.

Lightcast data, reported by Fortune on September 3, 2026: FDE job postings rose more than 1,000% year over year between January and August 2026, and more than 4,600% against 2023. For scale, postings across tech overall rose 13% over the same period (observed evidence, [Fortune](https://fortune.com/2026/09/03/forward-deployed-engineers-fast-growing-six-figure-silicon-valley-job-integrate-ai-with-customers-tech-careers-palantir)).

Indeed data, reported by Business Insider on May 16, 2026: FDE postings on Indeed were 543% higher in April 2025 than in January 2025, and the article's headline cites growth above 700% across a one-year window. The windows differ; the direction does not (observed evidence, [Business Insider](https://www.businessinsider.com/forward-deployed-engineer-jobs-in-demand-2026-5)).

An independent job-scrape analysis, published in the AI Engineering Field Guide repository and preserved in our machine-readable [market dataset](dataset/fde_market_data.json), collected FDE postings in repeated monthly scrapes across builtin.com between February and July 2026 ([the analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)). Across the 7 scrapes:

| Scrape Date | Total AI Engineering Listings | Live FDE Listings | FDE Market Share |
|---|---:|---:|---:|
| **2026-02-04** | 1,416 | 28 | 2.0% |
| **2026-02-27** | 2,057 | 41 | 2.0% |
| **2026-03-27** | 2,341 | 58 | 2.5% |
| **2026-04-22** | 2,473 | 65 | 2.6% |
| **2026-05-29** | 2,751 | 80 | 2.9% |
| **2026-06-25** | 3,024 | 108 | 3.6% |
| **2026-07-22** | 3,320 | 118 | 3.6% |

Headline FDE listings grew by **321%** (from 28 to 118), while the broader AI engineering market grew by 134% (from 1,416 to 3,320). FDE hiring expanded approximately **1.8 times faster** than the overall AI market in the scrape dataset. After deduplicating by unique job ID, the scrape yielded **146 unique FDE positions across 94 companies**.

Plank, a hiring platform tracking the enterprise AI startup market, counted 982 live FDE postings across 462 companies in 2026 (observed evidence, [joinplank.com](https://joinplank.com)).

### What each source actually measures

The four sources are not interchangeable, and reading one as another is how market myths start:

- Lightcast via Fortune - aggregate advertised postings across the market; measures growth rates and advertised salaries, not hires and not headcount
- Indeed via Business Insider - one job board's postings; sensitive to reposting behavior and to that board's employer mix
- The scrape analysis - live listings found at scrape time; measures share-of-AI-listings, the most churn-resistant signal here, but from small per-scrape samples
- Plank - one platform's collection of live postings; broad coverage with unknown deduplication

Two cautions apply before quoting any of these numbers. First, base effects: 4,600% growth against 2023 comes off a small 2023 denominator, which is what any early-stage category looks like. Second, the share measure - 2.0% to 3.6% of AI listings - is the hardest to inflate, because reposting inflates the numerator and the denominator together. This suggests the growth story is real even where specific percentages will be revised.

## Who is hiring

The employers behind the growth numbers fall into six groups. The day-to-day differences between them are covered in [where FDEs work](../role/04-where-fdes-work.md); this section stays at the level of who is posting.

- Frontier labs - OpenAI runs healthcare and government FDE teams ([OpenAI careers](https://openai.com/careers)); Anthropic hires FDEs for its Applied AI team ([the posting](https://job-boards.greenhouse.io/anthropic/jobs/5302966008)) and lists a Head of Forward Deployed Engineering role (observed evidence, 2026)
- Enterprise platforms - Palantir popularized the role and had roughly four dozen open forward-deployed positions as of September 2026, including client-specific roles for Intel, NATO, and the Norwegian government; it also hires Forward Deployed Infrastructure Engineers and non-engineering Deployment Strategists (observed evidence, Fortune)
- Hyperscalers - AWS hires the title, and Amazon posts Principal FDE roles that describe defining technical strategy across multiple strategic enterprise customers (observed evidence, [amazon.jobs](https://www.amazon.jobs))
- Data platforms - Databricks carried the most listings of any single company in the scrape analysis, at five; the Perspective AI survey of about 1,500 FDEs also draws respondents from Databricks, Scale AI, Cohere, and Sierra, which confirms the org type well beyond the labs (observed evidence)
### Top Employers in Empirical Scrape Sample

| Company | Unique FDE Postings | Industry / Sector | Focus Area |
|---|---:|---|---|
| **Databricks** | 5 | Data & AI Platform | Lakehouse AI and GenAI application deployments |
| **Mistral AI** | 4 | Frontier AI Lab | Enterprise model integration (Le Chat, Mistral Large) |
| **Stord** | 4 | Supply Chain & Logistics | Automated warehouse and fulfillment pipeline AI |
| **Thomson Reuters** | 4 | Legal & Tax Tech | Specialized regulatory AI and document workflows |
| **Truelogic Software** | 4 | Systems Integration | Nearshore FDE embedding for enterprise clients |
| **Anthropic** | 3 | Frontier AI Lab | Applied AI customer deployments and Claude integration |
| **Invisible Technologies** | 3 | AI Operations & Automation | Process automation and model operations embedding |
| **NewRocket** | 3 | IT Service Management | Enterprise ServiceNow AI workflows |
| **OneStream Software** | 3 | Financial Analytics | Enterprise CPM planning and financial modeling |
| **Turing** | 3 | AI Engineering Services | Managed forward deployed talent for Fortune 500s |

Reading the list as a whole: the top names are stable, but no single company accounts for even 4.0% of the scraped sample. Demand is broad, which matters for risk - the role does not depend on one employer's strategy. For the complete machine-readable breakdown, see our [market dataset](dataset/fde_market_data.json).

## Seniority and level

The scraped sample carried almost no entry-level signal. Of the 146 postings, 107 had no level marker, 19 were Senior, 8 Principal, 6 Staff, 5 Lead, and 1 Founding. None were junior (observed evidence).

The absence of a marker is not evidence of a junior bar. Primary postings state the bar explicitly: Anthropic requires 4+ years in a technical customer-facing role, or software engineering with consulting experience (observed evidence, 2026 posting). Practitioner career guides commonly describe ladders of about five levels from FDE to Director, and the top of the range exists at several employers: Amazon hires Principal FDEs, and Anthropic lists a Head of Forward Deployed Engineering (industry pattern from practitioner sites, confirmed by 2026 postings).

This suggests FDE is a second role, not a first job. Employers are buying a combination - production engineering plus customer ownership - that most people acquire on someone else's payroll first. The learning paths are built around that assumption ([learning paths overview](../learning-paths/README.md)), and [the beginner path](../learning-paths/beginner-to-fde.md) is honest about what the market currently expects and how long the route takes.

One counterweight belongs next to the growth numbers. Wikipedia notes the role's travel requirements and short-timeline pressure, and that some engineers consider the role undesirable for those reasons (observed evidence). Demand data tells you the market exists; it does not tell you the job suits you. That question is better answered by [the responsibilities evidence](../role/02-responsibilities.md) than by any posting count.

## Variants and adjacent titles

The title is fragmenting faster than job-board taxonomies track. Names observed for the same or near-same work:

- Forward Deployed Engineer - the standard title
- Forward Deployed Software Engineer - listed by Wikipedia as an alternate name for the same role
- Applied AI Engineer - observed in the scrape analysis as a near-equivalent
- Deployment Engineer - observed in the same analysis
- Solutions Engineer - adjacent rather than equivalent, with a pre-sale weighting; the boundary is mapped in [FDE vs other roles](../role/03-fde-vs-other-roles.md)
- Forward Deployed Infrastructure Engineer and Deployment Strategist - Palantir specializations, the latter non-engineering (observed evidence)

We recommend searching all of these titles when surveying the market, because a search on "FDE" alone misses a material share of the postings. The practical mechanics - alerts, filters, and where each title concentrates - are in [getting hired](03-getting-hired.md).

## Limitations of this data

A methodology note, so the numbers above get quoted honestly:

- Posting counts overcount churn - a role reposted after a failed search appears more than once, and some boards refresh listings in ways that reset their age
- Posting counts undercount quiet hiring - roles filled through networks, referrals, or internal transfer never appear as postings, and senior field roles skew toward exactly those channels
- Title matching misses renames - the variants above mean any count keyed to "Forward Deployed Engineer" alone is a floor; the share-of-AI-listings denominator also depends on the scraper's classification of what counts as an AI listing
- Scraped samples skew - the scrape reaches what is publicly reachable: companies with public career pages and postings in English; regional and referral-heavy markets are underrepresented (interpretation, not a measured property of the sample)
- Surveys are self-selected - the Perspective AI compensation survey (about 1,500 respondents) draws from the large labs and platforms it names; its medians do not describe the whole market
- Small bases - per-scrape counts of 28 and 118 listings are small samples; growth percentages computed on them are directionally useful, not precise
- Advertised is not paid - Lightcast's salary median comes from posting text; equity, bonus, and actual offers are absent from it

We recommend treating the growth story as directionally solid - four sources, one direction, across two years - and treating every specific number as a dated snapshot that will be revised.

## Related documents

- [Where FDEs work](../role/04-where-fdes-work.md) - how the job differs across the employer types listed above
- [Compensation](02-compensation.md) - the pay evidence, with sources and months attached
- [Getting hired](03-getting-hired.md) - converting this demand into applications and offers
- [What is an FDE](../role/01-what-is-an-fde.md) - the definition, origins, and the full list of role criticisms
- [The interview process](../interviews/01-interview-process.md) - what the loop looks like once you apply

## Further reading

- [Fortune, September 2026](https://fortune.com/2026/09/03/forward-deployed-engineers-fast-growing-six-figure-silicon-valley-job-integrate-ai-with-customers-tech-careers-palantir) - the Lightcast growth and salary analysis and the Palantir position count
- [Business Insider, May 2026](https://www.businessinsider.com/forward-deployed-engineer-jobs-in-demand-2026-5) - the Indeed posting data behind the 543% figure
- [The job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md) - the 146-posting dataset behind the table above
- [Plank](https://joinplank.com) - the 982-posting, 462-company market collection (2026)
- [Wikipedia: Forward deployed engineer](https://en.wikipedia.org/wiki/Forward_deployed_engineer) - definition, history, and the criticisms of the role
