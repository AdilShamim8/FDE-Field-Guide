# Communication and Technical Storytelling

This document is for FDEs who can build the thing but keep watching it get misread in
meetings and inboxes. FDEs are judged by their documents and their demos: the call ends,
the code review closes, and the writing is the deliverable that survives. You get the
weekly writing patterns, a demo structure that ends in decisions, ways to explain
probabilistic systems without lying, and the anti-patterns that make smart engineers
sound unreliable.

## Written-first communication

The artifacts an FDE writes every week: status emails, spec summaries, decision docs, and
postmortems. None of them are overhead. Each one is the version of you that keeps talking
when you are not in the room, and a typical engagement has more readers than listeners.

The workhorse pattern is bottom line up front: trajectory first, evidence second, asks
last. A five-line weekly status email:

```
Subject: <project> - week of <date> - <on track | at risk | blocked>
Bottom line: one sentence on trajectory and the next milestone.
Done: one or two items, each with a link or a number as proof.
Next: one or two items, each with an owner and a date.
Asks: what you need, from whom, by when - or "nothing this week".
```

We recommend this shape for every recurring update, because readers learn where to look.
The discipline lives in the "Done" line: every item carries evidence, so status never
becomes a vibe. Longer documents follow the same principle at section level - the point
first, then the support.

Matching the artifact to the moment:

- Status email - the weekly rhythm; bottom line up front, evidence attached
- Spec summary - before scope decisions; the two-page version people actually read
- Decision doc - when two options are both defensible; forces the trade-offs into prose
- Postmortem - after incidents; the durable record of what broke and what changed

## Demo storytelling

A demo is a story with a UI in it. Five moves:

1. Set the problem before the feature. Thirty seconds of context: whose pain, what it
   costs, what you are about to show. The audience cannot value what it cannot place.
2. Use realistic data. Lorem ipsum and `test_user_1` tell the audience nothing. Use
   anonymized customer records with permission, or a faithful synthetic set that has
   nulls, duplicates, and long tails.
3. Narrate what they are seeing. Say what just happened and why it matters. Do not make
   people decode a screen while you wait in silence.
4. Rehearse failure recovery. Know what you will say and do when the demo breaks: the
   fallback screenshots or recording, the sentence "this is exactly why we also built the
   batch path", and the clean move to the next point. The recovery is often more
   convincing than the demo.
5. End with the decision you want. "Here is what this proves. Here is what we need to
   proceed." A demo without an ask is a movie.

If the demo is a proof of concept rather than a feature walkthrough, the design rules
change - see [prototyping and PoCs](../engineering/01-prototyping-and-pocs.md) for
building one that produces a decision instead of applause.

## Explaining probabilistic systems

LLM systems do not return the same answer twice, and most stakeholders have no frame for
that. Three habits keep you honest and understood:

- Show examples, not percentages. Instead of "the classifier is 92% accurate", show three
  outputs it got right and two it got wrong, then say what the wrong ones cost and who
  catches them. Executives remember the examples; a bare number without them is noise.
- Define the error budget in business terms. "You can absorb about ten wrong suggestions
  per day without anyone noticing. We measured three per day on last week's data." This
  turns an abstract quality bar into something the customer can verify itself.
- Never promise 100%. Promise detection, fallback, and a human path instead: "it will be
  wrong sometimes; here is what happens when it is, and here is who sees it." A promise
  of perfection is the fastest way to lose the room in week six.

Concretely: "the model is 92% accurate" becomes "here are two tickets it routed wrong
last week; both were caught by the review queue; clearing them took one person ten
minutes." The second version survives skepticism because it contains the failure path,
not just the success rate.

Calibrate by audience: sponsors need the trajectory and the error budget; operators need
to know exactly what to do with a wrong answer. Give each audience its own version rather
than one sanitized deck for both.

## Technical narrative for engineers

Engineers smell marketing. Architecture walkthroughs land when they run in this order:

1. The constraint that shaped the design - data cannot leave the customer VPC, the source
   system has no webhooks, the p95 budget is 200 milliseconds. Every real design is a
   hostage to its constraints; start there and everything after sounds like reasoning
   instead of taste.
2. The diagram, walked along the request path - not the boxes-first tour, but the story
   of one request from screen to storage.
3. The decisions and the alternatives rejected - recorded in a decision record so the
   next engineer does not relitigate them (see
   [trade-offs and decision records](../system-design/03-trade-offs-and-decision-records.md)).

A design narrative with no alternatives reads as advertising. The sentence "we considered
X and rejected it because Y" is what earns trust with a technical audience.

## Meetings

- Agenda in the invite - including the decision to be made, not just the topics. People
  who cannot affect the decision can decline, which is useful information.
- Decision capture in the room - who, what, by when, said out loud and written down
  before anyone leaves the call.
- Follow-up notes within 24 hours - decisions, owners, dates, open questions. This is
  the artifact the stakeholder who skipped the meeting actually reads.
- Treat silence as a signal to ask, not to conclude. "I have not heard a concern yet -
  what am I missing?" surfaces the objection in the room instead of in the approval
  meeting you cannot attend.

## Anti-patterns

- Jargon walls - if a sentence only works with your internal acronyms, it does not work.
  Translate once, then adopt the customer's vocabulary.
- Burying the lede - the ask belongs in the first two lines, not the last paragraph. Busy
  readers decide in ten seconds whether to keep reading.
- Live-coding without a script - typing is not a demo. The audience watches your typos
  and your failing imports, not your design thinking.
- Hedging every claim - "it depends" without naming the dependencies is noise. Name the
  condition, pick the branch, and say what would change your mind.
- Reading slides aloud - the audience reads faster than you speak. Send the deck and take
  questions instead.
- Demoing at 100% abstraction - block diagrams with no product leave executives unable
  to picture what they are buying. Show the real screen at least once.
- The wall-of-numbers status - forty metrics with no bottom line make you look busy and
  lost at the same time. Pick the three that matter and lead with them.
- Answering the question nobody asked - impressive and useless. Check what decision the
  audience is trying to make and answer that one first.

## Related documents

- [Managing expectations](../customer/04-managing-expectations.md) - the hard conversations this skill has to carry
- [Requirements to spec](../customer/02-requirements-to-spec.md) - the highest-stakes document an FDE writes
- [Trade-offs and decision records](../system-design/03-trade-offs-and-decision-records.md) - the durable written form of the technical narrative
- [Prototyping and PoCs](../engineering/01-prototyping-and-pocs.md) - demos that are designed to end in a decision
- [Presenting projects](../portfolio/03-presenting-projects.md) - the same skill pointed at getting hired

## Further reading

- [Google SRE book](https://sre.google) - the postmortem chapters are the best available template for written incident communication
- [The Pragmatic Engineer](https://newsletter.pragmaticengineer.com) - consistently clear examples of engineering writing aimed at decisions
