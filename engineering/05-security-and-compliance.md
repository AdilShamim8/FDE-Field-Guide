# Security and Compliance

This is for engineers shipping into customer environments, where the security review gates production. Plan for the review in week 1, not week 12, because security teams move on their own calendar and their calendar does not compress for your launch date. The review is part of the job, not an obstacle beside it: Anthropic's FDE job description centers on building production applications inside customer systems and maintaining high standards for how they run (Anthropic, greenhouse posting, viewed 2026) - and in practice, "high standards" means clearing the customer's security review before anything ships.

## Passing the review

### The standard review pack

What customer security teams commonly ask for (industry pattern: the exact list varies, the shape rarely does):

- Data flow diagram - where data enters, where it is processed, where it leaves, including every subprocessor and model provider
- PII inventory - fields collected, purpose, retention period, and the deletion path
- Threat model summary - trust boundaries, top risks, mitigations; one page is usually enough
- Authentication design - how your service and your humans authenticate, with identity federation where possible
- Encryption - TLS in transit, encryption at rest, and who holds the keys
- Logging and access audit - what is logged, where it goes, who can read it, how long it is kept
- Vendor certifications - SOC 2 Type II is the recurring ask for SaaS vendors; FedRAMP for United States government work
- Penetration test status - last test date and whether findings were remediated

Produce these as artifacts during the engagement rather than as homework after the request. Keep the data flow diagram and PII inventory alive from week 1, and answering the review becomes assembling documents instead of doing archaeology. Also ask the security team for their own checklist in week 1: most teams have a standard list, and handing it over is easier for them than answering your questions one by one.

## Data and credentials

### Data boundaries

The central question your design must answer precisely: what leaves the customer's tenant, in what form, and to which subprocessors. Draw the boundary on the data flow diagram itself, with every crossing marked. A diagram that shows the boundary is far easier to review than a paragraph claiming that nothing leaves.

- Model providers - if the system calls an external model API, data is leaving the tenant. Check the provider's retention and training-use policies (see the [Anthropic documentation](https://docs.anthropic.com) and [OpenAI documentation](https://platform.openai.com/docs)) and quote them in the review pack. Security teams will ask, and "we believe they do not retain anything" is not an answer.
- Embeddings as derived personal data - an embedding computed from a customer record is derived from personal data, and reviews commonly treat it as personal data in its own right. Scope, store, and delete it with the same discipline as the source fields.
- Logging inputs and outputs - application logs that capture prompts, documents, or generated text turn your log store into a second copy of sensitive data. Log metadata by default and capture content only behind explicit, reviewed exceptions.
- Regional data residency - some customers require data to stay in a region or jurisdiction. This constrains model choice, storage region, and even support access, so settle it before anything else is designed.

### Secrets and credentials

- No secrets in code, in committed config files, in tickets, or in chat - a secret pasted into a ticket is a secret distributed to every future reader of the ticket
- Per-environment credentials - development, staging, and production never share an identity, so a development mistake cannot touch production
- Managed secret stores - use the customer's secrets manager or vault rather than introducing your own; their auditors know how to audit theirs
- Rotation stories - know how each credential rotates and what breaks during rotation. "We would have to redeploy everything" is a review finding, so design rotation to be a non-event
- The shared-credential anti-pattern - one team login survives from 2010 and fails reviews instantly: no attribution, no revocation, no audit trail. If the customer hands you one, ask for individual accounts early and in writing

## Newer risks and sector regimes

### LLM-specific security

Generative AI adds attack surface that most review checklists do not yet cover, so raise it yourself:

- Prompt injection is an untrusted-input problem - text from documents, emails, web pages, or user fields is attacker-controlled input, and treating it as instructions is the vulnerability. Architect so that injected instructions cannot change what the system is allowed to do.
- Scope tools and agents to least privilege - an agent that can read the CRM does not need write access to the data warehouse. Use per-tool scopes, per-action allowlists, and human approval for destructive or external actions; the build-side detail is in [agents and tools](../ai/02-agents-and-tools.md).
- Filter outputs before actions execute - validate model output against schemas and allowlists before it drives an API call, a database query, or an outbound email.
- Control egress for anything that fetches - anything that can retrieve URLs, including agents and retrieval crawlers, can be pointed at internal metadata endpoints. Restrict destinations explicitly.
- The "agent with database credentials" conversation - expect it in the review. The reviewer will ask what the agent's database user may do, and "everything the application may do" is the wrong answer. A scoped read-only role with row limits is the shape that passes.

### Compliance regimes by sector

Name which regimes apply during discovery, not after the build:

- HIPAA - United States healthcare data; expect business associate agreements and strict handling of protected health information
- PCI DSS - payment card data; most designs should avoid touching cardholder data at all, which is a design decision rather than a compliance afterthought
- FedRAMP and StateRAMP - United States federal and state work; authorization is a long process, and the practical path is usually deploying inside an authorized enclave rather than certifying your own stack
- GDPR - European Union personal data; lawful basis, data minimization, deletion rights, and transfer rules all shape the data boundaries above

You are not the compliance officer, but you are the person whose design either fits the regime or does not. Asking "which of these apply to this project?" in discovery is a credibility signal; discovering one in week 10 is a re-architecture.

## Evidence and audit

### Audit trails

- Who accessed what and when - access logs for your system, correlated with the customer's identity provider where possible
- Immutable and retained - audit logs go to storage the application cannot rewrite, with retention agreed in writing
- Access reviews - expect periodic reviews of who has access, so keep the access list small enough to defend line by line
- Reconstructable actions - when your system writes, the record should answer what changed, what triggered it, and on whose behalf; "the agent did it" must trace back to an input, a decision, and an action

Test the trail before the reviewer does: pick a recent action and reconstruct it end to end from the logs. If you cannot, neither can they, and that is the finding.

### Pre-review checklist

- [ ] Data flow diagram is current, including subprocessors and model providers
- [ ] PII inventory lists every personal field with purpose and retention
- [ ] Data boundary decision is written: what leaves the tenant, in what form, to whom
- [ ] Model provider retention and training-use policies are quoted with sources in the review pack
- [ ] Logs exclude sensitive content by default; every exception is reviewed and documented
- [ ] Secrets live in a managed store with per-environment credentials; nothing in code or tickets
- [ ] Credential rotation has been tested at least once before the review
- [ ] Agent and tool permissions are scoped per tool, with human approval on destructive actions
- [ ] Model outputs are validated before driving any action
- [ ] Encryption in transit and at rest is documented, with key ownership stated
- [ ] Audit logs are immutable, retained, and correlated with customer identities
- [ ] Certifications and penetration test status are gathered, current, and dated

## Related documents

- [APIs and integrations](02-apis-and-integrations.md) - auth patterns and secrets handling for the integration layer
- [Data pipelines](03-data-pipelines.md) - data minimization and PII scoping in practice
- [Cloud and infrastructure](04-cloud-and-infrastructure.md) - IAM, least privilege, and the network rules the review assumes
- [Agents and tools](../ai/02-agents-and-tools.md) - tool scoping and agent-loop safeguards behind the LLM security section
- [Production readiness checklist](../deployment/03-production-readiness-checklist.md) - where the security review sits in the go/no-go decision

## Further reading

- [Anthropic documentation](https://docs.anthropic.com) - model data usage policies and safety guidance
- [OpenAI platform documentation](https://platform.openai.com/docs) - model data retention and usage policies
