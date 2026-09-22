# Communities and People

If you want to know where FDE-adjacent practitioners actually talk, this file maps the communities worth joining and the habit of building your own public signal. The honest framing first: the FDE community is young, and most conversations happen in adjacent communities - solutions engineering, MLOps, AI engineering - plus company-specific alumni networks, rather than in venues named after the title. Practically, that means two things: follow the adjacent rooms, and expect the FDE-specific venues to be thin and to change names often.

## Communities

### Reddit

Four subreddits carry most of the role-adjacent discussion:

- [r/salesengineers](https://www.reddit.com/r/salesengineers) - the solutions-engineering community; pre-sale weighted, but the customer-conversation craft overlaps heavily with FDE discovery work, and the demo and objection-handling threads are directly reusable
- [r/cscareerquestions](https://www.reddit.com/r/cscareerquestions) - general career discussion; FDE threads appear whenever posting counts spike, and interview and offer anecdotes accumulate there
- [r/OfferEngineering](https://www.reddit.com/r/OfferEngineering) - offer and compensation discussion; useful for calibration against the sourced figures in [compensation](../job-market/02-compensation.md), not for market sizing
- [r/mlops](https://www.reddit.com/r/mlops) - production machine learning practice; the monitoring, evaluation, and drift topics FDEs own get their most technical discussion here

The standing caveat: role-specific threads are anecdotal. A dozen vivid stories are not a market survey, and the most confident voices in a thread are rarely the most representative; selection bias runs toward the extreme outcomes. We recommend using these communities for texture and question preparation, and the sourced figures in this guide for numbers.

### Practitioner sites and their communities

- [fde.academy](https://fde.academy) - courses and analyses aimed at the title, including the August 2026 Palantir compensation breakdown by level; useful for interview framing and ladder expectations
- [FDE Academy YouTube](https://www.youtube.com/@fdeacademy) - masterclasses, project breakdowns, and practitioner video discussions
- [joinplank.com](https://joinplank.com) - tracks the FDE market (982 postings across 462 companies in 2026); its collection doubles as a market map of who is hiring first FDEs
- [fdepulse.com](https://fdepulse.com) - practitioner career write-ups; the commonly cited five-level ladder model comes from sites of this kind
- [tryexponent.com](https://tryexponent.com) - interview-prep community with FDE guides; its write-ups document lab and platform loops, including the compressed ElevenLabs loop and the Palantir FDSE guide

The same discount applies here as in [the reading list](02-reading.md): several of these sites sell courses or placements, so treat their claims as experience reports and verify any figure you plan to rely on. The practical test: use them to learn what questions to ask, and use primary sources - postings, bands, and surveys - for the answers.

### The reference repository

- [The AI Engineering Field Guide](https://github.com/alexeygrigorev/ai-engineering-field-guide) - the repository whose job-scrape analysis this guide cites ([the analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)); beyond the data, it aggregates AI-engineering learning resources in the same field-guide format, and its issues and updates are where the underlying analysis evolves

## Conferences and events

The FDE-specific conference circuit does not really exist yet; what does exist is adjacent (industry pattern, stated conservatively). None of the venues below are FDE-branded, and that is the point - go where the engineering conversation already is:

- AI engineering meetups - the local scenes where deployment war stories outnumber model papers; the closest thing to FDE shop talk outside employers
- Lab developer events - the frontier labs run developer conferences and streamed launches where deployment patterns and tooling get announced; watching them is how you track the platform side of the job without working at one
- Platform vendor conferences - the cloud and data-platform events carry the integration and architecture content FDEs actually use, and the customer teams you embed with watch them too

We recommend treating events as acquisition of specific conversations - one integration question answered, one practitioner met - rather than as attendance achievements. Before any event, write down the one integration problem you actually want an answer to; after it, send the two follow-ups you promised. That loop, repeated, is most of what people mistake for networking.

## Building your own signal

Community presence is a portfolio multiplier: the work is the same, but doing it in public means recruiters and hiring managers find it without being shown. Recommendations:

- Write anonymized deployment postmortems - what broke, what it cost, what changed. The write-up format in [debugging methodology](../troubleshooting/01-debugging-methodology.md) doubles as a public artifact; anonymize the customer, keep the engineering. Two paragraphs and an incident timeline are enough; this is not a conference talk.
- Answer integration questions in public repositories - reading contracts, reproducing problems with partial information, and writing the fix clearly is the exact FDE skill, demonstrated where engineers actually look.
- Run practice engagements - a friend's side project, a nonprofit's workflow, an internal tool nobody owns. Treat them with real discovery, real handover artifacts, and real deadlines; they generate the stories interviews ask for.
- Publish the portfolio properly - the projects in [what to build](../portfolio/01-what-to-build.md) become posts, threads, and talks through the presentation practices in [presenting projects](../portfolio/03-presenting-projects.md).
- Keep a sustainable cadence - one postmortem or integration write-up per quarter is enough. A slow, verifiable trail beats a burst of enthusiasm followed by silence, because hiring managers check whether the signal is recent.

One caution from the market data: with zero junior titles across 146 scraped postings, hiring managers are buying evidence of experience. Public signal is how you show the experience you have and the judgment you are building, without waiting for permission from a title. It is also how the adjacent communities above get to know your name before a posting does - which, in a referral-heavy corner of the market, is worth more than another application.

## Verified FDE practitioners (September 2026)

These practitioners are directly named as sources in the Codebasics FDE Roadmap 2026 (September 2026) and the five verified YouTube masterclasses. Each entry includes the verified LinkedIn or YouTube URL and the context in which they are cited.

Kevin Bai — founding Forward Deployed Engineer at Anthropic, previously Palantir and Rippling. Published "Forward Deployed Engineering 101" ([youtube.com/watch?v=KwhgfwOSToQ](https://www.youtube.com/watch?v=KwhgfwOSToQ)). Source of the FDE Flywheel concept (customer deployments generating platform primitives for core SWE) and the Auditing-Evals-Deployment loop documented in [the FDE loop](../role/05-the-fde-loop.md).

Aishwarya Srinivasan — published "Forward Deployed Engineer: The Hottest AI Job of 2026" ([youtube.com/watch?v=w-Z4QYK1QL4](https://www.youtube.com/watch?v=w-Z4QYK1QL4)). Covers market positioning of the FDE role in 2026, dual skill stack (applied AI engineering plus domain translation), and enterprise adoption dynamics.

Piyush Garg — published "What is Forward Deployed Engineer (FDE) Role?" ([youtube.com/watch?v=7JlEs6zyB_U](https://www.youtube.com/watch?v=7JlEs6zyB_U)). Covers granular operational boundaries between FDE, Solutions Architect, and Core SWE in rapid enterprise delivery cycles.

AI LABS — published "This Is How Forward Deployed Engineering Is Actually Done" ([youtube.com/watch?v=AD-EmZ3v6-g](https://www.youtube.com/watch?v=AD-EmZ3v6-g)). Source of the 5-step operational methodology: Observation and AS-IS auditing, Strategic Automation Triage, Failure-oriented building, Rigorous ground-truth evals, and Quantifiable business ROI metrics.

Dhaval Patel — co-founder of Codebasics and AtliQ Technologies, published the FDE Roadmap video ([youtube.com/watch?v=uE4HTkDtp48](https://www.youtube.com/watch?v=uE4HTkDtp48)) and the Codebasics FDE Roadmap 2026 PDF. Follow at [codebasics.io](https://codebasics.io). Listed in the Codebasics roadmap as LinkedIn contact to follow: Colin Jarvis (OpenAI), Joe Schmidt (a16z), Andrej Karpathy.

Hemanand Vadivel — co-creator of the Codebasics FDE Roadmap 2026, AtliQ Technologies. Co-presenter of the FDE Roadmap video.

Pankaj Jaiswal — FDE working in SAP-heavy manufacturing and field service environments. Source of the Bonus SAP Integration section in the Codebasics FDE Roadmap 2026. LinkedIn: [linkedin.com/in/pankaj29](https://www.linkedin.com/in/pankaj29/).

Rushi Gandhi — FDE practitioner interviewed for the Codebasics FDE Roadmap 2026. LinkedIn: [linkedin.com/in/rushi0508](https://www.linkedin.com/in/rushi0508/).

Pranav Modh — FDE practitioner interviewed for the Codebasics FDE Roadmap 2026. LinkedIn: [linkedin.com/in/modhpranav](https://www.linkedin.com/in/modhpranav/).

Daksh Trehan — FDE practitioner interviewed for the Codebasics FDE Roadmap 2026. LinkedIn: [linkedin.com/in/dakshtrehan](https://www.linkedin.com/in/dakshtrehan/).

## Related documents

- [Reading](02-reading.md) - the sources worth your reading time, with the same verification caveats
- [Presenting projects](../portfolio/03-presenting-projects.md) - turning project work into public evidence
- [What to build](../portfolio/01-what-to-build.md) - the projects worth talking about in public
- [Market overview](../job-market/01-market-overview.md) - the demand context that makes signal-building worth the effort

## Further reading

- [The AI Engineering Field Guide](https://github.com/alexeygrigorev/ai-engineering-field-guide) - the reference repository and its evolving analyses
- [fde.academy](https://fde.academy) - practitioner analyses and courses for the title
- [joinplank.com](https://joinplank.com) - the FDE market tracker and its hiring collection

