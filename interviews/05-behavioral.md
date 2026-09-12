# Behavioral Rounds

This file is for candidates preparing for FDE behavioral deep-dives, which weight ownership, judgment, and customer empathy more heavily than generic software loops. You get the scored traits, an eight-story inventory to build before the loop, a story format, a trait-by-trait question bank, and the quality signals and red flags interviewers watch for.

## What these rounds probe

The clearest published signal of what behavioral rounds score comes from Anthropic's FDE posting ([greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5302966008), 2026, observed evidence), which lists the fit criteria as high agency in ambiguity, a cooperation mindset, and strong communication for discovery. This suggests the questions are engineered to surface those three traits, and that answers are scored against them rather than against generic "culture fit".

Mechanically, the round is 45 minutes with one or two interviewers, usually an engineering lead plus someone customer-facing (pattern). Expect probing follow-ups rather than a fixed list: interviewers pick one story and keep asking until they can tell what you personally did. Vague answers get drilled; precise ones move the conversation forward.

## The story inventory

We recommend arriving with eight stories ready, each mapped to the trait it proves:

- A project you owned end to end - the agency story: you carried it, and you can name the moment it nearly failed
- A time requirements changed badly - ambiguity and reprioritization: what you re-planned and what you told the customer
- A production incident you debugged - ownership of something you did not build, under time pressure
- A disagreement with a customer or stakeholder - conflict without casualties: how you disagreed, and what the relationship looked like after
- A time you said no - judgment: what you refused, what you offered instead, and what it cost
- A deliverable under ambiguity - the agency-in-ambiguity trait verbatim: partial information, a decision, an outcome
- A failure you repaired - honesty plus postmortem habits: what broke, what it cost, what you changed
- A time you made someone else successful - the cooperation trait: an operator, teammate, or customer left better off by your work

Eight stories cover nearly every behavioral question an FDE loop asks (pattern); most questions are one of these stories with different lighting.

Mine them from real material rather than inventing them: past engagements and incidents, times a customer pushed back, work you did beyond your title. Candidates early in their career can source several of these from portfolio projects and open-source maintenance; the story about keeping a deployed system healthy for a stranger counts as ownership even if the deployment was your own.

## The story format

We recommend a four-beat format, STAR-adjacent without the ceremony:

1. Context in two sentences - the system, the customer, the stakes, and nothing more
2. Your specific actions - what you did, decided, built, or said, in the first person for the parts you did
3. The outcome with numbers where honest - hours saved, defect rates, dates; invented precision is worse than an honest range
4. What you changed afterward - the habit, checklist, or design that changed because of the story

The fourth beat is the one most candidates skip and interviewers notice: it converts an anecdote into evidence of judgment.

Prepare two lengths of each story: a two-minute version and a four-minute version with one layer of detail added. Write both down, then rehearse them aloud until the structure holds without the script. Memorized phrasing collapses under a follow-up question; a memorized structure survives one.

An example of the format, compressed: a customer's nightly sync failed three nights in a row (context). I traced the failures to an upstream schema change nobody announced, wrote a contract test against their export, and added an alert on row-count deltas (actions). The sync stayed green for the rest of the engagement, and the customer's ops team adopted the alert (outcome). I stopped trusting silent upstreams: every integration I ship now opens with a schema check (what changed). Eight sentences, four beats, one story.

## Question bank by trait

Pattern-based questions; exact wording varies by company. Answer each with a story from the inventory.

### Ownership

- Tell me about a project you owned end to end. What did owning it mean when it went wrong?
- Describe a time you picked up work outside your job description because it needed doing.
- What is the longest you have maintained something after shipping it?

### Ambiguity

- Tell me about a deliverable you produced when the requirements were genuinely unclear.
- Describe a decision you made with incomplete information. What would you decide differently now?
- When did you under-deliver, and what did you do next?

### Conflict

- Tell me about a requirement you pushed back on. What happened?
- Describe a disagreement with a customer or stakeholder that got tense. How did it end?

### Customer empathy

- Tell me about a time a customer changed your mind about something technical.
- Describe explaining a technical trade-off to a non-technical audience under time pressure.

### Failure

- Describe debugging something you did not build.
- Tell me about a failure of yours that cost the team or the customer something. What did you change afterward?

## Answer quality signals

This is our interpretation of how the traits map onto answers:

- The "I" and "we" balance - credit the team, but be specific about what you did; all-"we" answers hide whether you have ever carried anything
- Actions over context - the middle of the story should be verbs you performed, not circumstances that happened to you
- Reflection over heroics - what you would do differently now scores higher than how hard you fought
- No badmouthing - customers, employers, and colleagues get neutral descriptions even in conflict stories; the interviewer assumes they are next

## Red flags interviewers watch for

Our interpretation of the failure patterns:

- Blaming customers - "the client was impossible" ends more FDE interviews than any technical answer
- Vagueness about your own role - if the interviewer cannot tell what you did after ten minutes, the story scores zero regardless of outcome
- Casualties-free failure - a failure story where nothing actually went wrong reads as evasive
- Hero narratives without prevention - saving the day twice from the same root cause reads as manufacturing your own drama

One signal candidates miss: the questions you ask at the end of the round are also scored, because they reveal what you think the job is. Questions about how handovers work, how field lessons reach the product team, and what the last FDE in this seat got wrong land better than questions about on-site perks. This is our interpretation, but it follows directly from the traits the loop scores.

## Related documents

- [The interview process](01-interview-process.md) - where behavioral rounds sit and why they weight differently
- [Customer scenario rounds](04-customer-scenarios.md) - the same traits tested live, not as stories
- [The FDE loop](../role/05-the-fde-loop.md) - a map for filing your stories by engagement stage
- [The engagement lifecycle](../customer/01-engagement-lifecycle.md) - source material for ownership and conflict stories
- [Debugging methodology](../troubleshooting/01-debugging-methodology.md) - the structure that makes incident stories hold up
- [Getting hired](../job-market/03-getting-hired.md) - the same stories, repurposed for applications and screens

## Further reading

- [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) - the fit criteria these rounds probe (2026)
