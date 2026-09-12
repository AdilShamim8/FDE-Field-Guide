# Customer Scenario Rounds

This file is for candidates preparing the round that most distinguishes FDE loops: a role-play where the interviewer plays the customer and you run the engagement conversation. You get the round's formats, the signals interviewers score, a discovery playbook, three fully worked practice scenarios with hidden goals and failure responses, and a practice method.

## Why this round exists

FDE loops test the conversation, not just the code. Two published anchors:

- Exponent's interview guides describe the ElevenLabs FDE loop as "a compressed loop that runs from coding to conversation, testing technical range and customer instinct" ([tryexponent.com](https://tryexponent.com), July 2026, observed evidence) - the conversation half is this round
- Anthropic's FDE posting lists strong communication for discovery among its fit criteria ([greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5302966008), 2026, observed evidence) - this round tests it under pressure

This suggests the round exists because the job does: the FDE loop opens with problem and discovery stages ([the FDE loop](../role/05-the-fde-loop.md)), so the interview opens there too.

## The five formats

Practitioner reports converge on five role-play shapes (pattern):

- Discovery role-play - the interviewer is a vague sponsor ("we want AI in our reporting") and expects you to find the real problem
- Angry-stakeholder role-play - something broke or disappointed, the room starts upset, and you stabilize it
- Demo-and-pushback - you present a design or demo, then defend cost, accuracy, and risk against challenge
- Prioritization trap - everything is urgent, resources are fixed, and the test is what you cut and how you say it
- Scope-creep probe - mid-engagement requests keep arriving, and the test is whether you absorb, deflect, or renegotiate

Most loops run one of these for 45-60 minutes; the discovery role-play is the most common opener (pattern).

## What interviewers score

This rubric is our interpretation, consistent across practitioner accounts:

- Questions before answers - did the first third of the conversation contain questions rather than a pitch
- Who-owns-what probing - did you find who decides, who operates, and who can veto
- Expectation setting - did you leave promises the customer could hold you to, and avoid ones they could not
- Composure under pushback - did the challenge make you sharper or defensive
- Concrete next steps - did the conversation end with a dated action rather than a vibe
- Honesty about unknowns - did you say what you do not know yet and how you will find out
- Protecting the customer's time - did you drive to decisions, or fill air

Expect the interviewer to interrupt, redirect, and occasionally disagree badly on purpose. The interruptions are the test: each one checks whether you absorb new information without losing the thread of the conversation. We recommend treating every interruption as data about the customer rather than as an obstacle to your plan.

## The discovery role-play playbook

We recommend this arc inside any discovery scenario. It is the compressed version of the full framework in [discovery and requirements](../skills/02-discovery-and-requirements.md).

1. Open with context, not a pitch - "before I propose anything, I want to understand how this works today"
2. Run the funnel - situation (walk me through the last time this happened), pain (what does it cost you), success metric (what number tells you this worked), constraints (systems, compliance, deadline), decision process (who decides and who can veto)
3. Capture and replay - read back what you heard in two sentences and ask what you got wrong; the correction is where the truth lives
4. Close with a summary and a next step - a one-line problem statement, a proposed next meeting with an agenda, and a date

Practice the funnel until it survives interruption, because in the round it will be interrupted.

## Practice scenarios

All three are fictional. Each lists the setup, the interviewer's hidden goals, a strong response outline, and the common failure responses. Practice aloud with a peer playing the interviewer; keep the hidden goals hidden from the candidate.

### Scenario 1: "Our CEO saw a demo at a conference and wants AI everywhere by Q3"

- Setup - you are three weeks into a new engagement. The VP of engineering relays that the CEO returned from a conference demo and wants AI "everywhere" by end of Q3. The VP is half-embarrassed, half-serious, and watching how you handle it.
- Hidden goals - can you find a real use case under the hype without deflating the sponsor; will you commit to a delivery date before discovery; do you push back while preserving the CEO's momentum
- A strong response outline - treat the enthusiasm as fuel and convert it to structure. Congratulate the ambition, then propose a two-week discovery sprint across the three noisiest workflows, with explicit selection criteria: a measurable baseline, reachable data, and contained blast radius. Offer one candidate workflow to make it concrete. Set the expectation that Q3 delivers a ranked shortlist and one pilot, not "everywhere". End with a dated next step: the discovery schedule.
- Common failure responses - pitching before asking anything; promising the Q3 timeline to be agreeable; lecturing the room about AI hype and killing the sponsor's energy; accepting "everywhere" as a requirement and designing for it

### Scenario 2: "Your pilot's outputs are fine, but the ops team will not support it"

- Setup - the pilot works and the business sponsor calls the outputs fine. Then the ops team lead says flatly: "my team will not support this. It fails silently and we find out from users."
- Hidden goals - do you treat ops as a blocker or as a design constraint; can you fix the ownership and failure-mode design rather than the mood; will you throw the sponsor or ops under the bus
- A strong response outline - take the objection as requirements. Ask what "fails silently" looked like, twice, with specifics. Commit to the fixes that address it: structured logging with alerts on symptoms, a kill switch, a runbook, and a named on-call arrangement with a response window. Offer a weekly ops review for the pilot's duration. Then reset expectations with the sponsor separately: go-live moves until the ownership design exists, and that is what makes the system dependable. End with a joint session to sign off the runbook.
- Common failure responses - escalating to the sponsor to overrule ops; promising to fix everything without asking what specifically failed; defending the pilot's accuracy when accuracy was never the objection; agreeing with everything and leaving with no artifact

### Scenario 3: "We go live before the audit in six weeks, and security has not reviewed anything"

- Setup - a compliance audit lands in six weeks. The sponsor wants the system live before it. Security review has not started, and the data includes customer PII.
- Hidden goals - will you sequence honestly under deadline pressure; can you say no to a plan while saying yes to a revised one; do you treat security review as an obstacle or as a dependency to manage
- A strong response outline - name the dependency out loud and sequence around it. Start the security review this week with a minimal review pack: data flows, model and vendor retention terms, secrets handling, audit logging. Propose a phased scope: a read-only, no-PII slice live in three weeks, the PII-touching slice after security sign-off, and pre-agreed rollback for both. Give the sponsor the audit-relevant win, the no-PII slice plus documentation, rather than the full ask. End with the review pack as the dated next step.
- Common failure responses - promising the date and hoping security moves fast; going around security as "an engineering decision"; scoping to everything and delivering nothing by the audit; refusing the deadline without offering a revised plan

## How to practice

We recommend three practices, in order of return:

- Peer role-plays - run each scenario twice, once as candidate and once as interviewer; playing the interviewer teaches the hidden goals faster than any write-up
- Record yourself - the gap between how you think you sound and how you sound is widest under pushback
- The five-question self-review rubric - score every practice round:

1. Were my first three exchanges questions rather than answers or a pitch?
2. Did I get the success metric and the decision process before proposing anything?
3. Did I replay what I heard and invite correction?
4. Did I leave at least one expectation the customer could hold me to?
5. Did the conversation end with a concrete, dated next step?

## Related documents

- [Discovery and requirements](../skills/02-discovery-and-requirements.md) - the full discovery framework this playbook compresses
- [Managing expectations](../customer/04-managing-expectations.md) - saying no and delivering bad news, the scenario 3 skill set
- [Stakeholder management](../skills/04-stakeholder-management.md) - who decides, who vetoes, who operates
- [Debugging customer systems](../troubleshooting/02-debugging-customer-systems.md) - the shared on-call reality behind scenario 2
- [System design rounds](03-system-design.md) - the design conversation that pairs with this one
- [The interview process](01-interview-process.md) - where this round sits in the loop

## Further reading

- [Exponent](https://tryexponent.com) - FDE interview guides with role-play descriptions
- Never Split the Difference (Chris Voss) - negotiation moves that translate directly to pushback handling
