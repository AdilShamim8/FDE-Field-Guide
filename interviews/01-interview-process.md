# The FDE Interview Process

This file is for engineers preparing for FDE interviews at AI labs, platform companies, and startups hiring forward-deployed roles. You get the shape of the loop stage by stage, what the evidence says each stage tests, how FDE loops differ from software engineering loops, and a preparation strategy that maps effort to rounds.

## What the evidence shows

Far fewer FDE interview processes are publicly documented than software engineering loops, so expect less certainty here than in generic interview prep. What is documented converges on the same shape, from three independent source types:

- Practitioner guides summarize FDE interviews as testing three things: technical depth, real-world deployment thinking, and client-facing communication ([fde.academy](https://fde.academy), 2026)
- Exponent's interview guides describe the ElevenLabs FDE loop as "a compressed loop that runs from coding to conversation, testing technical range and customer instinct" ([tryexponent.com](https://tryexponent.com), July 2026)
- A practitioner account of the Cohere FDE process expects candidates to talk through system context, scale assumptions, reliability decisions, security constraints, and "what broke and how you fixed it" ([gaijineer.co](https://gaijineer.co), April 2026)

The Anthropic FDE job description ([greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5302966008), 2026) tells you what the loop must select for even where the loop itself is not published: 4+ years in a technical customer-facing role, production LLM experience, Python plus ideally TypeScript or Java, and strong communication for discovery. Reddit practitioner threads (2026, anecdotal) add that FDE interviews "care less about textbook distributed systems and more about whether you can reason about real-world" customer systems.

This suggests the loop is the job compressed: the same discovery, design, debugging, and communication work the role performs daily, arranged into hour-long rounds.

## The typical loop

The sequence below is an industry pattern assembled from the documented loops above and practitioner reports, not a published standard, and the durations are pattern estimates. Order varies: startup loops compress stages, and some loops replace a live round with a take-home.

1. Recruiter screen - 30 minutes: role fit, motivation, logistics, travel tolerance, and salary band. Expect a direct question about appetite for customer-facing work.
2. Technical screen - 45-60 minutes: practical coding or a small exercise, often with an AI-flavored task such as parsing structured output or handling a rate limit.
3. System design or deployment-design round - 45-60 minutes: design a system for a described customer with real constraints, not an abstract scale puzzle.
4. Customer scenario or role-play round - 45-60 minutes: the interviewer plays a customer or stakeholder and you run the engagement conversation.
5. Behavioral deep-dive - 45 minutes: ownership, judgment, and customer stories, probed harder than in generic software loops.
6. Take-home - in some loops, 3-8 hours: a small working system against a provided brief or dataset, replacing or preceding the live rounds.
7. Final conversation - 45-60 minutes with the hiring manager or field lead: engagement philosophy, lessons from past deployments, and mutual fit.

Two to three weeks between stages is common (pattern). Ask the recruiter for the round list early; most will tell you, and knowing the shape changes how you prepare.

## What the loop tests

Map the three tested axes from the practitioner guides onto the rounds:

- Technical depth - the coding screen and design round: production Python, boundary handling, LLM API fluency, and design under constraints
- Real-world deployment thinking - the design round, the take-home, and the "what broke and how you fixed it" conversation: rollout, rollback, monitoring, security, and who operates the thing
- Client-facing communication - the customer scenario round and behavioral deep-dive: discovery, expectation setting, and composure under pushback

The Cohere account's list doubles as a self-check: can you talk through system context, scale assumptions, reliability decisions, security constraints, and a specific thing that broke and how you fixed it? Any of those five without a story behind it is where preparation goes.

Anthropic's fit criteria read as the scored traits: high agency in ambiguity, a cooperation mindset, and communication strong enough to run discovery. The loop is engineered to surface all three.

Note what the loop does not test, according to the same sources: pure algorithmic speed, framework trivia, and whiteboard statistics. The rare technical questions that look academic usually resolve into a customer context when you answer them, which is the intended move.

## How FDE loops differ from SWE loops

Four differences, drawn from the sources above and labeled accordingly:

- Less textbook distributed systems - practitioner reports describe loops that probe reasoning about a specific customer's mess over abstract scaling trivia (Reddit threads, 2026, anecdotal)
- Communication is scored, not assumed - the customer scenario round has no equivalent in most software loops, and it is weighted, not decorative
- Ownership stories beat puzzle speed - "what broke and how you fixed it" asks for an incident narrative, not an algorithm
- No junior ramp - an analysis of 146 FDE postings found no junior titles ([the scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md), February-July 2026), so loops expect end-to-end evidence from the first conversation

This suggests preparing as someone who has shipped into a customer's environment, or who can show the closest honest equivalent through portfolio work.

## A preparation strategy

We recommend mapping preparation to the loop stages rather than grinding generic interview material:

1. Build or refurbish the portfolio first, because it is evidence for every round at once; projects that walk the loop end to end beat polished tutorials ([what to build](../portfolio/01-what-to-build.md))
2. Write the story inventory next, since behavioral rounds and "what broke" probes draw on the same material ([behavioral rounds](05-behavioral.md))
3. Practice customer role-plays with a peer, the round candidates most often underprepare ([customer scenario rounds](04-customer-scenarios.md))
4. Drill the customer-flavored design framework ([system design rounds](03-system-design.md)) and practical coding ([coding and technical rounds](02-coding-and-technical.md))
5. Finish with the [question bank](07-question-bank.md) as a source of mock-interview prompts

Plan around a focused 3-6 weeks of preparation (a pattern-based recommendation): roughly one week for stories and portfolio, two to three for scenario and design practice, the remainder for mock loops. Candidates transitioning from adjacent roles can adapt the timelines in the [learning paths](../learning-paths/README.md).

Two habits make the weeks count. Schedule mock loops under real conditions: a timer, a peer you do not know well, and no notes on the table. And keep a written list of what each mock exposed; the list, not the calendar, decides what the next practice session covers. Candidates who prepare this way walk into the loop having already failed safely several times, which is what the loop is designed to test.

## Signal mismatches to avoid

FDE loops predictably reject three profiles. We recommend checking yourself against each:

- The champion coder who cannot ask a discovery question - solves the stated problem flawlessly without noticing it is the wrong problem; fails the scenario and design rounds, which score questions before answers
- The polished talker who cannot debug live - narrates beautifully until the exercise breaks, then improvises; fails the coding round and the "what broke" probe, which score method under failure
- The consultant who does not code - runs discovery excellently but cannot produce the artifact; fails the technical screen, because the role is engineering, not advisory

The loop is designed so that all three fail somewhere. Prepare to be credible on both halves of the coding-to-conversation arc, because that is exactly what the ElevenLabs description says the loop exists to test.

The honest self-check is uncomfortable but cheap: run one mock coding round and one mock role-play, back to back, and notice which half you dreaded. That half is your signal mismatch. Every candidate has one; the loops exist to find it before the customer does.

## Related documents

- [Coding and technical rounds](02-coding-and-technical.md) - the round where practical fluency is measured
- [System design rounds](03-system-design.md) - the customer-flavored design round in depth
- [Customer scenario rounds](04-customer-scenarios.md) - the role-play formats and scoring rubrics
- [Behavioral rounds](05-behavioral.md) - the story inventory these rounds draw from
- [What to build](../portfolio/01-what-to-build.md) - portfolio principles that double as loop evidence
- [Getting hired](../job-market/03-getting-hired.md) - finding loops worth preparing for

## Further reading

- [Exponent FDE interview guides](https://tryexponent.com) - documented loops, including the ElevenLabs description quoted above
- [fde.academy](https://fde.academy) - practitioner guides on the three tested axes
- [gaijineer.co](https://gaijineer.co) - the Cohere process practitioner account
- [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) - the fit criteria the loop selects against (2026)
- [Reddit practitioner threads](https://www.reddit.com) - anecdotal FDE interview reports across r/cscareerquestions and adjacent subreddits
