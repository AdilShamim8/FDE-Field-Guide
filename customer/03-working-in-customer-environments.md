# Working in Customer Environments

For any engineer about to be embedded with a customer, physically or virtually. Half the
FDE's technical difficulty is not the code - it is everything around the code: getting
access, working an unknown stack, security rules, and the politics of a company you do
not run. The role definition makes this structural: an FDE "develops and deploys software
within a client company, often working alongside the client's employees for a defined
period of time" ([Wikipedia: Forward deployed engineer](https://en.wikipedia.org/wiki/Forward_deployed_engineer)).
The employer side says the same thing differently: Anthropic's FDE posting describes
building production applications with Claude models inside customer systems, white-glove
deployment support, and long-term customer relationships
([Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008)).
The white-glove language is the tell: the customer experiences you, not just your code.

## The first week playbook

What you do in week one sets the ceiling for the whole engagement. Work the checklist;
the items are boring and all of them are load-bearing.

- [ ] Access inventory: list every system you need - repos, clouds, data warehouses,
      ticketing, dashboards, build systems - and file a request for each one
- [ ] Who-is-who map: sponsor, operators, security reviewers, data owners, and the admin
      who can actually grant permissions
- [ ] Security training and device rules: complete mandatory training, confirm what you
      may install, and whether personal devices may touch customer data (usually no)
- [ ] Find the real experts: the operators who run the systems daily, not only the
      managers who present them
- [ ] Read existing runbooks and postmortems: postmortems tell you how the system
      actually fails, which beats any architecture diagram
- [ ] Request data access early: approvals take longer than building, so a data request
      filed on day 3 that takes 2 weeks is a schedule you planned; filed on day 15, it is
      a crisis
- [ ] Agree your demo cadence and status format with the sponsor
- [ ] Prove the build works end to end on mock data in your own environment, so the first
      real blocker is a single blocker, not ten

## Access friction

The friction is not a bug; it is their security posture working as designed. Expect some
mix of:

- VPNs and VDIs - some customers route all work through virtual desktops where your
  usual tools do not exist
- Bastions and jump hosts - production access funneled through audited chokepoints
- Ticket-queue approvals - a 10-minute permission grant that lives behind a 3-day ticket
- Separated environments - dev, stage, and prod with different rules, different
  approvers, and different data

Pattern-tier advice, from how most teams describe operating:

- File every access request in week 1, even for things you might not need; withdrawing a
  request costs nothing, waiting 2 weeks for one costs a sprint
- Design work to progress on mock data while approvals queue; the walking skeleton does
  not care whether the data is real
- Keep a blocked-on-access list visible in every status update - access friction is a
  shared problem between your company and theirs, not your secret to absorb

The last one matters most. FDEs burn out quietly absorbing friction their sponsor could
dissolve with one email, and the sponsor never finds out until the demo slips.

## Unfamiliar stacks

You will meet systems nobody fully understands: a decade-old service, a homegrown
scheduler, tribal knowledge held by two people. Reverse-engineer respectfully:

- Pair with the owners - read the code together; their narration is the real
  documentation
- Read the runbooks first - they encode what breaks, not just how it is supposed to work
- Ask "what breaks often" - the answer is a map of where the real complexity lives

The recurring temptation is rewriting instead of integrating: the legacy thing looks bad,
and you can clearly do better in a week. Occasionally that is true. Most of the time the
legacy thing is load-bearing in ways nobody can enumerate, and the rewrite becomes the
engagement's failure story. We recommend integrating first, and proposing rewrites as a
scoped option only once you own production evidence.

When to adapt to their stack versus proposing yours: adapt by default - their language,
their cloud, their deploy pipeline - because you leave and they stay. Propose your own
stack only where there is a gap, not a preference. The trade-offs are covered in
[cloud and infrastructure](../engineering/04-cloud-and-infrastructure.md).

Whatever you learn, write it into their runbooks, not just yours. Leaving the
documentation better than you found it is how the next engineer - and the next
engagement - will be judged.

## Security and behavior norms

The specifics vary by customer; the direction never does:

- Approved tool lists - check before installing anything; "it worked at my last customer"
  is not an argument
- No customer data on personal devices - assume this is absolute unless told otherwise in
  writing
- Data boundaries - know which environments may talk to which, and never move data across
  them to be helpful
- Screen-sharing discipline - close the other dashboards before you demo; shared screens
  leak production rows
- Installation rules - if the tenant restricts packages, use their mirror and their
  versions, not the public internet

One more norm, and it is the big one: you are the product as far as the customer is
concerned. Their lasting impression of your company's engineering quality is the code you
commit, the incidents you handle, and whether you did what the ticket said. Security
reviews come later; behavior is the pre-screen.

## Culture and politics

Mechanics first, because they are cheap to learn: meeting norms (agendas or none, cameras
or not, decisions in chat or in the room), escalation culture (some customers treat an
escalation as partnership, others as an attack), and timezone overlap (agree your
protected overlap hours in week 1, then defend them).

Then the layer nobody diagrams. You are arriving with budget and attention that someone
else wanted:

- Incumbent vendors - a systems integrator or contractor whose future billings shrink if
  your project succeeds
- Internal teams who wanted to build it - the engineers who proposed doing this in-house
  and were overruled; their skepticism is rational, not hostile
- Shadow organizations - the real decision network, which rarely matches the org chart

Practical moves, from repeated pattern:

- Find the champion - the person whose career improves if you succeed, and align your
  milestones with theirs
- Make the operators heroes - the automation that makes the support lead's week easier
  is a success story they will tell for you; credit them by name in every demo
- Never bad-mouth the customer's systems in writing - your comments in their repos are
  readable, exportable, and permanent; write criticism as trade-offs in a decision
  record, or not at all

The mapping and alignment work behind these moves is covered in
[stakeholder management](../skills/04-stakeholder-management.md).

## Onsite vs remote

Pattern tier. Travel expectations vary widely: an independent job-scrape analysis of 146
FDE postings (February-July 2026) found travel or onsite work explicitly mentioned in
only 9% of listings, while Anthropic's FDE posting estimates roughly 25% travel (posting,
2026). Most teams appear to run a hybrid: onsite for specific weeks, remote the rest.

What onsite weeks are actually for:

- Integration crunches - the week your service meets their identity provider, when being
  in the room saves days
- Go-lives - the launch window, when decisions need to happen in minutes
- Trust building - the first week, executive reviews, and the first visit after a bad
  incident, when presence is the apology

What is fine remote: status updates, spec reviews, normal development, evaluation
analysis, and most demo cycles. We recommend defaulting to remote and spending onsite
time on the three categories above, because travel that produces no decision is a cost
to both sides. If you do go hybrid, make the onsite weeks land next to the events that
need decisions - a trip for its own calendar slot rarely pays for itself.

## Related documents

- [The engagement lifecycle](01-engagement-lifecycle.md) - the phase map that this
  environment work runs inside
- [Security and compliance](../engineering/05-security-and-compliance.md) - the technical
  half of the rules described here: reviews, data boundaries, secrets
- [Stakeholder management](../skills/04-stakeholder-management.md) - champion mapping,
  skeptics, and escalation patterns in depth
- [Debugging customer systems](../troubleshooting/02-debugging-customer-systems.md) -
  what unfamiliar stacks look like when they break at 2 a.m.
- [Managing expectations](04-managing-expectations.md) - access friction and bad news
  both land better with expectations already managed

## Further reading

- [Wikipedia: Forward deployed engineer](https://en.wikipedia.org/wiki/Forward_deployed_engineer) -
  the neutral definition, role history, and overlap with solutions architects and
  consultants
- [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) -
  a primary source for the employer's view: customer-system work, white-glove support,
  and the ~25% travel estimate
