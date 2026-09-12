# Managing Expectations

For FDEs and engagement leads. Expectations are set in week 1 and paid for in week 12.
Most unhappy customers were not lied to - they were left to assume. This document covers
the four places assumptions form - kickoff, demos, timelines, and bad news - and gives
working scripts for the conversations FDEs tend to avoid.

## Setting expectations at kickoff

The kickoff meeting sets the default for everything after it. Four things belong in
writing before it ends:

- What success means - the metric, the baseline, the target, the date, and the owner.
  "Improve routing" is a wish; "routing accuracy from 60% to 90.0% on the pilot dataset
  by March 31, owned by their ops lead, measured weekly" is an expectation
- Demo cadence and channels - what gets demoed, to whom, how often, and where the status
  lives between demos
- What happens when things break - who is called, within what time, and who decides to
  roll back. Agree on this while nothing is broken; renegotiating incident response
  mid-incident is the worst version of both
- The pilot-to-production path - what happens if the pilot works, what the production
  checklist requires, and who signs. The path itself is covered in
  [prototype to production](../deployment/01-prototype-to-production.md); the point here
  is that the customer should be able to recite it

Pilots that end in "so... now what?" failed here, in week 1, not at the pilot review.

## Demo expectations

Every demo of a prototype carries one obligation: say what it does not do yet. Every
time, out loud, even if you said it last time. The parts audiences remember are the
parts that looked automatic.

- Disclose the wizard-of-oz elements - anything you drove by hand: the script you ran
  manually, the data you pre-cleaned, the approval you simulated. Disclosed, it is a
  scoping insight; discovered later, it is a broken promise
- Close with the same line every time: "here is what this proves, and what it does not
  prove yet." It feels repetitive by the fourth demo. That is the point - it survives
  being repeated secondhand to the sponsor's boss
- Separate proof from polish - a demo that proves the risky part with an ugly interface
  beats a beautiful demo of the easy part

## Timeline honesty

Two buffer rules, and they coexist:

- Carry buffers you do not advertise - your internal estimate with everything going
  right is the customer's worst case, not their expected case
- Never advertise the buffer - a padded date announced as a commitment invites work to
  expand into it, and you spend credibility without buying anything

Commit to dates you control versus dates you do not:

- You control - your build, your demos, your internal reviews. "First demo on the 14th"
  is a commitment; make it and hit it
- They control - their SSO approval, their data access sign-off, their security review.
  Never commit their dates on their behalf. "The pilot starts after your SSO approval -
  we filed it on the 3rd and their team typically takes 2 weeks" keeps the dependency
  visible without owning it

The mechanics of under-promising without sandbagging: commit to checkpoints, not
endgames. "Working integration against your staging environment by the 21st" is
checkable every week; "production in Q3" is checkable never. Checkpoints make slippage
visible early, when it is a conversation, instead of late, when it is a betrayal.

## Saying no

The scripts below are recommendations - adapt the wording, keep the structure:
acknowledge, trade, decide.

Scope creep:

"We can add X to this phase if we move Y to phase 2 - which do you prefer?"

Not "no", and not a silent yes. The customer gets a real decision, and you get a scope
boundary with their fingerprints on it.

Timelines:

"We can hit that date with the current scope, or add this with a two-week slip - your
call."

And its harder variant, when the date is truly fixed: "The date holds if we cut these two
features. If all three ship, the date moves. Which matters more?"

Unsafe requests - asked to put customer records into an external tool, or to route around
a security control:

"We cannot put customer records into that external tool. Here is what we can do inside
your tenant that gets most of the value."

The refusal is paired, always, with a compliant alternative. A bare "no" to a security
request sounds obstructionist; a refusal plus an alternative sounds like you did the
work.

## Delivering bad news

Structure every piece of bad news the same way: facts, impact, plan, next update time.
Illustrative example, numbers fictional:

```
Facts:  The evaluation run on 2026-05-14 scored 84.2% routing
        accuracy, below the 90.0% phase-1 bar.
Impact: Phase 1 does not pass this week. Misses concentrate in
        the 3 categories added on the 12th.
Plan:   Retrain on the expanded dataset by Thursday and re-run.
        If the second run misses, we propose cutting the 3
        categories from phase 1 scope.
Next:   Results by Friday 15:00, in the status doc and on the call.
```

Two timing rules:

- Incidents get reported within the first hour, not when solved - the first hour is when
  silence starts writing the story for you, and it writes it as "hiding something"
- Quality misses come with data and a remediation path, never vibes - "it feels worse
  this week" creates anxiety; "84.2% versus the 90.0% bar, misses concentrated here,
  plan attached" creates a decision

## The trust ledger

Interpretation tier: a judgment from practice, not a measured law. Treat trust as a
ledger. Small kept promises compound - the demo that happened on the day it said it
would, the status that went out on Friday even with nothing new to report. One hidden
miss undoes ten kept ones, because it converts every past promise into a question: what
else was not heard about?

This suggests an operational rule: visibility beats perfection. A customer who watches
an 84.2% score get reported, diagnosed, and fixed trusts the system more than a customer
who was told everything was fine until it was not.

The repair pattern when an expectation has been broken:

1. Acknowledge - name the miss plainly, without defending it first
2. Fix - the actual correction, with a date
3. Prevent - the process change that stops recurrence
4. Follow through visibly - all three steps confirmed in writing and checked off in
   public

Skipping step 4 is the common failure: the fix lands, the prevention is promised, and
the follow-through never gets demonstrated, so the ledger stays negative.

## Related documents

- [The engagement lifecycle](01-engagement-lifecycle.md) - the kickoff phase is where
  this document's promises get made, and the checklist keeps them alive weekly
- [Prototype to production](../deployment/01-prototype-to-production.md) - the
  pilot-to-production path that kickoff must make explicit
- [Communication and storytelling](../skills/03-communication-and-storytelling.md) - the
  demo craft and narrative discipline behind the rules here
- [Stakeholder management](../skills/04-stakeholder-management.md) - the escalation and
  alignment patterns this document assumes
- [Common failure modes](../troubleshooting/03-common-failure-modes.md) - the failures
  that bad news delivery is usually about

## Further reading

- [Site Reliability Engineering](https://sre.google) - Google's SRE book; the incident
  management practice behind the first-hour reporting rule
- The Trusted Advisor (David Maister) - the trust-building framework behind the trust
  ledger, applied to professional services
- Never Split the Difference (Chris Voss) - negotiation scripts and the calibrated
  questions pattern the saying-no section borrows from
