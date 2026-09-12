# FDE Compensation

If you are benchmarking an offer, preparing a negotiation, or deciding whether the move pays, this file collects the sourced compensation evidence for FDE roles from 2025-2026 and explains how to read ranges that look contradictory. The evidence is fragmented and moves fast: every figure below carries a source and a month, and the ranges differ by method, not just by market. Treat cross-source deltas as method artifacts first and market truth second.

## The sourced snapshot

| Source | Figure | Date | Method |
| --- | --- | --- | --- |
| Lightcast, via Fortune | median advertised FDE salary above $188,000; traditional software engineers at about $145,000 | Sep 2026 | salary text in advertised postings |
| Anthropic posting | $280,000 to $320,000 annual salary band (NYC, SF, Seattle) | 2026 | posted salary band |
| Fortune, on Anthropic roles | some FDE roles reach $400,000 | Sep 2026 | reporting on lab compensation |
| levels.fyi | Palantir FDE average total comp about $352,833; base about $193,029 | 2026, undated | self-reported |
| Perspective AI survey | total comp from about $215,000 median at Palantir to $785,000+ for senior FDEs at Anthropic and OpenAI | May 2026 | self-reported survey, about 1,500 FDEs |
| Exponent, citing levels.fyi | FDSE median total comp about $211,000; base $135,000-$200,000; Deployment Strategist base $110,000-$170,000 | 2026, undated | self-reported |
| fde.academy | Palantir FDE total comp $135,000 to $750,000+ depending on level | Aug 2026 | practitioner analysis |
| Glassdoor, via GSDC Council | Palantir FDE average base $155,477, 90th percentile $243,492 (423 salaries); industry FDE total comp averaging $238,000, range $205,000-$486,000 | 2026 | self-reported |

Entries marked undated were collected during 2026 research for this guide; the sources do not state an as-of month. Read the table with six observations:

- Every source agrees the FDE market clears the general software market. The cleanest apples-to-apples number is the Lightcast comparison: an advertised median above $188,000 against about $145,000 for traditional software engineers (September 2026).
- The Palantir base-salary conflict is instructive. levels.fyi's self-reported base averages about $193,029; Glassdoor's 423-salary sample averages $155,477. Both are self-reported, and the samples, periods, and level mixes differ. We cannot adjudicate between them, and you should not have to - the posted band for the specific role beats both.
- Averages are pulled by the top of the distribution. levels.fyi reports averages; Exponent and the Perspective AI survey report medians. A handful of senior lab packages at $785,000+ move an average far more than a median.
- The senior premium is the largest single variable in the data - larger than employer type or geography across the survey's ranges.
- The non-engineering variant pays less on the evidence available: Deployment Strategist base of $110,000 to $170,000 (Exponent, citing levels.fyi, 2026, undated) sits below every engineering median in the table. Check which role you are actually interviewing for before anchoring on any of these numbers.
- Survey coverage concentrates where the title is densest. The Perspective AI survey draws its roughly 1,500 respondents from Anthropic, OpenAI, Palantir, Scale AI, Databricks, Cohere, and Sierra (May 2026), so its medians describe the lab-and-platform segment, not the 462-company long tail Plank tracks.

## How to read the ranges

### Advertised versus total compensation

Lightcast counts the salary line in postings: no equity, no bonus, no sign-on. levels.fyi, Glassdoor, and the Perspective AI survey count realized total compensation. That is why an advertised median of $188,000 and a total-comp median of about $211,000 can both be true without contradiction. When you compare an offer against this table, convert everything to one basis first: base plus bonus plus equity, valued at your own vesting and valuation assumptions, not the recruiter's.

### Equity and employer type

Employer type sets the equity weight; the taxonomy is in [where FDEs work](../role/04-where-fdes-work.md). At frontier labs, the $400,000 outcomes Fortune reports include packages where equity and bonus carry real weight. At platforms like Palantir, fde.academy's $135,000-$750,000+ spread is mostly level spread across a long ladder rather than negotiation spread within a level. At the first-FDE startups in Plank's long tail, equity is a larger fraction of a smaller and less certain number. We recommend valuing startup equity near zero until the company's next funding round prices it, and negotiating on cash accordingly.

### Geography and level

Advertised medians blend every market and remote policy in the sample. Posted bands do not: Anthropic's $280,000-$320,000 band is tied to New York, San Francisco, and Seattle, and the same role elsewhere would carry a different band. Within any single employer, level is the biggest multiplier. One source spanning $135,000 to $750,000+ at one company is a statement about levels, not about negotiating skill.

### The software engineer baseline

The Lightcast comparison implies roughly a 30% advertised-salary premium over traditional software engineering (September 2026). This suggests employers are pricing the combination, not the parts: production engineering plus customer ownership in one person is scarce, and the market pays for scarcity. The work that combination performs is [the FDE loop](../role/05-the-fde-loop.md). Note the premium is measured on advertised salary only; whether it widens at the total-comp level depends almost entirely on equity, which the advertised data cannot see.

## Negotiation notes

Recommendations, offered carefully because negotiation advice ages faster than salary data:

- Ask for the band first. Posted bands are increasingly public - Anthropic's is printed on the posting itself - and many employers state ranges by policy. Asking is normal, not aggressive, and it ends the guessing before you name a number.
- Spend leverage on the scarce combination. The requirements employers print are the leverage map: production systems shipped into customer environments, vertical expertise (Anthropic names financial services and healthcare as pluses), and production AI experience covering evaluations, agents, and deployment at scale. A generic senior-engineer record negotiates like a generic senior engineer.
- Anchor on level, not average. The averages in the table mix levels. Find the band for your level and negotiate inside it; you will sound informed rather than demanding.
- Weigh equity risk explicitly at startups. First-FDE roles trade cash certainty for equity volume. Decide the cash floor you need, treat everything above it as upside, and read [where FDEs work](../role/04-where-fdes-work.md) before accepting the trade.
- Price the burden, not just the band. The role's travel requirements and short-timeline pressure are documented criticisms (Wikipedia), and they are part of what the premium over general software engineering pays for. A band that looks thin against the premium may be thin because the burden is lighter; a band that looks rich may be compensating for 25% travel. Ask what the number includes.

## A staleness warning

Every figure in this file is dated because every figure will go stale; the sources above already disagree with each other, which is the normal condition of a young market, and none of them is the final word. Before you negotiate, re-check three things in the week that matters: your target employer's current postings, because bands move; levels.fyi for the specific company and level; and the practitioner trackers such as fde.academy and the Perspective AI reports. If a figure in this file and a live posting disagree, trust the posting.

## Related documents

- [Market overview](01-market-overview.md) - the demand context behind the pay
- [Where FDEs work](../role/04-where-fdes-work.md) - how employer type drives equity, travel, and level structure
- [Getting hired](03-getting-hired.md) - converting positioning into the offer you will negotiate
- [The FDE loop](../role/05-the-fde-loop.md) - why the scarce combination commands the premium

## Further reading

- [Fortune, September 2026](https://fortune.com/2026/09/03/forward-deployed-engineers-fast-growing-six-figure-silicon-valley-job-integrate-ai-with-customers-tech-careers-palantir) - the Lightcast advertised-salary data and the $400,000 lab figure
- [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) - the posted band verbatim, with locations
- [levels.fyi](https://www.levels.fyi) - self-reported totals by company and level
- [Perspective AI](https://getperspective.ai) - the State of Forward Deployed Engineering 2026 compensation report (May 2026)
- [fde.academy](https://fde.academy) - the by-level Palantir compensation analysis (August 2026)
