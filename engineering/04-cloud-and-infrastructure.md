# Cloud and Infrastructure

This is for engineers deploying into customer cloud estates. The customer already has a cloud, a network layout, and opinions about all of it, so the FDE question is never "which cloud should we use" but "how do we live inside theirs". The spread is real: AWS appears in 47.0% of FDE postings, GCP in 38.0%, and Azure in 34.0% (146 postings scraped February-July 2026, independent job-scrape analysis). The numbers overlap because the same role meets all three - you will not pick the cloud; you will meet the customer's.

## The customer estate

### Deploying into their estate

Enterprises run landing zones: standardized account structures, guardrails, and pre-approved patterns. What you will actually hit:

- Account and subscription structure - workloads are pinned to specific accounts, projects, or subscriptions with their own billing and policies, and "just create a new one" is not your call
- Existing VPCs and private subnets - your workload usually must live inside their network, peered or segmented, often with no public ingress
- Organization policies - egress restrictions, allowed regions, and blocked services; some tenants block all internet egress by default, which changes your model-provider options immediately
- Mandatory tagging - cost-allocation tags required on every resource, with automation that deletes untagged ones
- Approval gates - new service types may need an architecture review board sign-off with lead times measured in weeks

Access requests are the true critical path. Fire the requests for accounts, roles, network paths, and data reads in week 1, and track them in the engagement tracker with owners and dates. Infrastructure access in an enterprise is a paperwork queue, and paperwork queues do not respond to engineering urgency.

One question saves weeks, and it belongs in the first infrastructure conversation: "Show me where the last vendor deployed." The answer hands you a pre-approved pattern - network path, identity approach, tagging scheme, and the approvers who already said yes. This suggests that reusing the beaten path usually beats designing the ideal one. If the answer is "nobody has deployed a vendor here before", that is also useful information: it predicts a longer approval path, and the engagement plan should price that in.

### Identity and least privilege

- IAM roles and service accounts - your workload runs as a cloud identity, not as a human's account. Request one identity per service rather than one shared role for everything you ship.
- Workload identity - every cloud has a pattern for authenticating workloads without stored keys: IAM roles for service accounts (IRSA) on AWS EKS, Workload Identity Federation on GCP, managed identities on Azure. Use the native pattern; long-lived cloud keys are how incidents and audit findings start.
- Scoped-down policies - start from the minimum list of actions the service needs, not from a copy of a similar role. Expanding a permission later is a request; retracting it after an incident is a meeting.
- The permanence problem - admin access granted "just for now" during setup becomes permanent, because removing it is nobody's ticket. We recommend requesting the least privilege that works from the start; you rarely get a second chance to shrink it quietly.

Ask for a named contact on the customer's platform or cloud team early. Every permission request goes faster when someone on their side recognizes your name.

## Building and shipping

### Infrastructure as code in customer environments

`Terraform` is the common denominator across clouds and the tool most enterprises have standardized on, which cuts both ways. See the [Terraform documentation](https://terraform.io) for the basics; the FDE-specific issues are organizational:

- Their modules first - read the customer's existing modules and use them where possible. They encode the tagging, networking, and compliance decisions the organization already approved. Writing parallel modules makes you the second standard.
- State backend politics - who owns the state, where it lives, and who can run an apply are organizational questions. In many enterprises the FDE proposes the plan and a customer engineer applies it with their credentials.
- Plan and apply discipline - every apply against customer infrastructure goes through a reviewed plan. Keep plans small and separable so a review does not become a week.
- When IaC is not possible - restricted accounts, manual gates, and air-gapped sites exist. Document the manual steps as a runbook anyway: hand-built environments without documentation are unrepeatable, and unrepeatable is worse than slow.

Watch for gaps between their modules and your needs. If a required resource type has no internal module, ask whether building one is in scope or whether an exception process exists. Both answers are workable; discovering it during apply is not.

### Compute choices

| Compute option | Good fit | Watch out for |
| --- | --- | --- |
| Serverless functions | spiky or low traffic, event-driven triggers | cold starts, VPC and egress constraints, execution timeouts |
| Containers on managed runtimes | steady traffic, custom runtimes, long-lived processes | you own sizing, scaling, and image supply chain |
| Managed Kubernetes | an existing cluster with a platform team behind it | operational overhead, and you inherit their cluster politics |

Decision factors: cold-start sensitivity, VPC and egress needs, customer ops maturity, and existing standards. The default recommendation is to match the customer's existing compute pattern unless there is a strong reason not to. If they run everything on `Kubernetes` with a platform team, your service lands there; if they are a serverless shop, fighting for a cluster is a fight you do not need. Reserve deviations for when the requirement genuinely demands it, and write down why - see [trade-offs and decision records](../system-design/03-trade-offs-and-decision-records.md).

GPU workloads are their own decision. Capacity, quota, and hourly cost differ by region and account, and enterprises ration them. If the use case needs inference hardware, ask about GPU availability in the first infrastructure conversation, not the week of launch.

## Operating over time

### Environments

Full dev, staging, and production parity is the textbook; customer reality is often a production and a nearly-production. Aim for this instead:

- One environment you can break - even a sandbox tenant or a dev account where you control restarts and data, so you can test destructive paths without a change window
- Sandbox tenants for external dependencies - third-party SaaS usually offers sandboxes; use them in dev so test data never flows toward production systems
- On-prem realities - bastion hosts for access, air-gapped clusters needing artifact mirrors and internal registries, and hardware you cannot resize. Estimate transfer and install times generously; moving artifacts into restricted networks is slower than anyone expects
- The "works in our cloud" trap - your demo environment proves your code, not the deployment. Latency, egress rules, DNS, and identity all differ inside their estate. Rehearse the deployment in their environment before you promise a date.

Keep environment differences in configuration, not in code branches. A branch per environment guarantees that the staging code is not the production code.

### Cost visibility

- Agree who pays before deploying - your cloud account with reimbursement, or their account against their budget. Both arrangements are common; ambiguity is the problem, because it surfaces as a surprise invoice.
- Set budgets and alerts from day 1 - even for a PoC. A surprise bill is the kind of conversation that can end an engagement, and the fix costs minutes.
- Estimate before deploying - a rough monthly cost per environment, written down and shared with the sponsor. If the estimate is wrong in either direction, make that a shared discovery, not a unilateral one.
- Watch the known spikes - load tests, embedding backfills, and GPU nodes are the classic cost explosions; schedule them with the budget owner aware.

Reuse what exists before provisioning anything: a shared logging stack, an existing database, the customer's monitoring. New infrastructure is a cost conversation; existing infrastructure is a configuration conversation, and only one of those needs a budget owner.

## Related documents

- [Deployment patterns](../deployment/02-deployment-patterns.md) - where in their estate the system lands: VPC-embedded, SaaS-adjacent, hybrid
- [Security and compliance](05-security-and-compliance.md) - IAM scope, secrets, and the review gates attached to the infrastructure
- [APIs and integrations](02-apis-and-integrations.md) - how egress and network rules constrain your integrations
- [Architecture for customer systems](../system-design/01-architecture-for-customer-systems.md) - designing under constraints you did not choose
- [Working in customer environments](../customer/03-working-in-customer-environments.md) - the organizational reality behind the approval gates

## Further reading

- [Terraform documentation](https://terraform.io) - infrastructure as code basics and workflow
- [Kubernetes documentation](https://kubernetes.io) - for estates where managed Kubernetes is the landing zone
