# Customer brief and handover worksheet

Copy this worksheet into `learning-artifacts/customer-brief.md` and fill it in with your own evidence. Reviewed 2026-10-11. Unfilled fields are missing information, not permission to invent a customer or result. A peer role-play is practice; label it accordingly.

## The decision

- Intended user and actual source of this information:
- Workflow today, including waiting, handoffs, and exceptions:
- Evidence observed directly:
- Statements reported by someone else:
- Assumptions that still need a user interview:
- Smallest useful change and why it needs software:
- Conditions under which a deterministic query would be enough:

## Data and permissions

- Source URL, record identifiers, and observation window:
- Retrieval date and response/file digest:
- Fields retained, transformations, and excluded fields:
- Rights and privacy review status:
- What the sample cannot establish:
- Label source and adjudication, if any; otherwise write “no outcome labels”:

## Acceptance and evidence

| Requirement | Reproduction command or artifact | Actual result | Remaining gap |
|---|---|---|---|
| Read valid input and reject invalid input | Fill in | Fill in | Fill in |
| Repeated import avoids duplicate records | Fill in | Fill in | Fill in |
| A conflicting update is visible and contained | Fill in | Fill in | Fill in |
| A reviewer can reproduce the summary | Fill in | Fill in | Fill in |
| User outcome improves against an observed baseline | Fill in | Fill in | Usually unmeasured in this exercise |

## Operation and handover

- Python/tool versions and working directory:
- Install and run commands:
- One successful request and one rejected request:
- State that survives a restart and state that is lost:
- Recovery steps actually tested:
- Owner of the next action and the evidence needed to proceed:
- Recommendation: continue, change, or stop, and why:

For the foundations project, the CFPB records have no ETISE severity/routing labels. A source category count is not model accuracy. The local API has caller-supplied role simulation and in-memory state. Do not fill those gaps with a deployment claim.

## Related documents

- [Beginner path](../beginner-to-fde.md) - progression and readiness checks
- [Specification exercise](../../customer/02-requirements-to-spec.md) - turn an observation into an acceptance contract
- [Expert practicum](../expert-fde-practicum.md) - evidence needed beyond local practice
