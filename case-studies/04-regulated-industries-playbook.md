# Regulated Industries Deployment Playbook

This playbook provides an authoritative guide for forward deployed engineers embedding inside highly regulated enterprise environments: Healthcare and Life Sciences, Financial Services and Banking, and Defense and National Security. In these sectors, compliance constraints dictate architecture, networking, data retention, and operational procedures before a single line of model logic executes.

## Healthcare and Life Sciences: HIPAA and BAA Compliance

Deploying AI systems in clinical workflows, health insurance claims, or pharmaceutical research requires adherence to the Health Insurance Portability and Accountability Act (HIPAA) and Health Information Technology for Economic and Clinical Health (HITECH) Act.

### 1. Business Associate Agreement (BAA) requirements

- You cannot send Protected Health Information (PHI) to any third-party cloud provider, LLM API, or SaaS telemetry vendor unless a countersigned BAA is in place.
- Major model providers (such as Anthropic, OpenAI, AWS Bedrock, and Microsoft Azure OpenAI) provide BAA addendums, but only under enterprise agreements.
- Zero data retention mandate: the BAA must legally bind the vendor to zero-day data retention (ZDR), prohibiting the provider from logging prompts or completions to disk or using customer traffic for model training.

### 2. De-identification boundaries

Before data enters an AI pipeline, evaluate whether PHI can be removed using one of two HIPAA standards:

- Safe Harbor method: requires the removal of eighteen specific personal identifiers (including patient names, geographic data below state level, all dates directly related to an individual except year, telephone and fax numbers, email addresses, Social Security numbers, medical record numbers, account numbers, certificate/license numbers, vehicle identifiers, device identifiers and serial numbers, URLs, IP addresses, biometric identifiers, full-face photos, and any unique identifying characteristic).
- Expert Determination method: a qualified statistical expert applies scientific principles to demonstrate that the risk of identifying an individual is very small, documenting the risk assessment in an official compliance report.

### 3. Architecture for clinical and claims systems

- Local inference alternative: where cloud BAA negotiation is blocked by customer legal teams, deploy quantized open-weight models (such as Llama 3 or Mistral) on customer-managed GPU nodes within their isolated clinical network.
- Scrubbing gateway: implement a deterministic PII/PHI redaction proxy using regex patterns and local named-entity recognition (NER) models (such as Microsoft Presidio) before forwarding text to authorized retrieval indices.
- Audit trail: log all user access to patient records with user identity, timestamp, patient ID, and access justification, retaining audit logs for a minimum of six years.

## Financial Services and Banking: SOX, GLBA, and Model Risk Management

Deploying AI within tier-1 banks, investment firms, and fintechs requires navigating strict regulatory perimeters established by the SEC, FINRA, the Federal Reserve, and the OCC.

### 1. Model Risk Management (SR 11-7 / OCC 2011-12)

The Federal Reserve Board's Supervisory Letter SR 11-7 on Model Risk Management requires rigorous governance over any quantitative method or system that applies statistical techniques to process input data into quantitative estimates. In banking, an LLM generating credit assessments or compliance reports is classified as a model subject to SR 11-7:

- Conceptual soundness: you must produce a written design document explaining why the chosen model architecture is mathematically appropriate for the business task.
- Rigorous benchmarking: you must compare model outputs against traditional deterministic baselines (such as gradient-boosted trees or heuristic rule engines) to prove incremental value.
- Outcomes analysis: continuous production monitoring of prediction stability, drift, and error distributions with scheduled quarterly model re-validation.

### 2. SEC Rule 17a-4 and FINRA recordkeeping

- All communications and decision logs concerning securities transactions, customer advisory messages, or trade execution must be preserved in write-once-read-many (WORM) compliant electronic storage.
- If an agent assists in drafting customer communications, the prompt, the retrieved knowledge chunks, the generated response, and the human supervisor's review timestamp must be archived in immutable storage for a minimum of three to six years depending on asset class.

### 3. Private network transit without internet egress

- Zero public internet transit: financial institutions prohibit customer data from traversing the public internet. Deploy connections using AWS PrivateLink, Azure Private Link, or Google Cloud Private Service Connect.
- Customer-Managed Encryption Keys (CMEK): all data at rest within databases and vector stores must be encrypted using keys stored in the customer's Hardware Security Module (HSM) or Key Management Service (KMS), allowing the customer to revoke encryption keys instantly to sever data access.

## Defense, Intelligence, and National Security: Air-Gapped Operations

Deploying AI systems for defense agencies, national security organizations, and aerospace contractors requires compliance with the Department of Defense (DoD) Cloud Computing Security Requirements Guide (SRG) and federal authorization frameworks.

### 1. Authorization impact levels

- FedRAMP High: the federal baseline for civilian agencies handling sensitive, unclassified data in cloud environments.
- DoD Impact Level 4 (IL4): covers Controlled Unclassified Information (CUI) and mission-critical systems.
- DoD Impact Level 5 (IL5): covers higher-sensitivity CUI, unclassified National Security Systems (NSS), and tactical defense operations.
- DoD Impact Level 6 (IL6): covers classified information up to Secret level. Systems at IL6 and above operate in physically isolated, air-gapped enclaves with zero connection to the public internet.

### 2. Air-gapped deployment mechanics

When embedding as an FDE in an air-gapped facility or Sensitive Compartmented Information Facility (SCIF), standard developer habits are completely invalidated:

- Zero egress and ingress: no `pip install`, no `docker pull`, no `git clone`, and no remote API calls. All software dependencies, base container images, and model weights must be pre-approved, cryptographically signed, scanned for vulnerabilities, and transferred via approved physical media (such as write-locked optical media or hardened data transfer appliances) through a formal security review.
- On-premise artifact mirrors: you must deploy and operate local mirrors within the enclave, including a private container registry (such as Harbor) and local package repositories (such as devpi or local PyPI mirrors).
- Local model weights: models are deployed entirely on air-gapped GPU clusters (e.g. NVIDIA vLLM, TensorRT-LLM, or Triton Inference Server) loading verified model weight checkpoints from encrypted local disk volumes.

### 3. Operational clearance and personnel discipline

- Personnel security: engineers operating in defense environments must hold active security clearances (Secret, Top Secret, or TS/SCI with polygraph).
- Hardware separation: engineers use dedicated customer-issued government furnish equipment (GFE) with cameras, microphones, and Bluetooth physically disabled or removed. Personal devices and unapproved electronics are prohibited from the SCIF perimeter.

## Cross-Sector Compliance Comparison Matrix

| Sector | Primary Regulations | Data Residency Requirement | Model Egress Allowed? | Audit Trail Standard |
| --- | --- | --- | --- | --- |
| Healthcare | HIPAA, HITECH, FDA SaMD | Regional / US or EU boundary | Yes, with BAA and Zero Data Retention | 6 years minimum; access and disclosure logs |
| Financial Services | SOX, GLBA, FINRA, SEC 17a-4, SR 11-7 | Strict tenant isolation | Only via PrivateLink / VPC endpoints | 3 to 6 years; WORM immutable storage |
| Defense & Intelligence | FedRAMP High, DoD IL4/IL5/IL6 | Air-gapped enclave or sovereign cloud | Strictly prohibited at IL6; isolated enclave | Permanent cryptographic operational audit |

## The Regulated Deployment Checklist

Before moving any AI workload from prototype to production in a regulated environment, verify every item on this checklist:

- [ ] Legal instrument executed: countersigned BAA (Healthcare) or Data Processing Agreement with Zero Retention Addendum (Finance).
- [ ] Network perimeter isolation: all API traffic routed through private VPC endpoints; public internet egress disabled at the subnet route table.
- [ ] Customer-managed encryption: all vector indices, relational stores, and backups encrypted at rest with customer-controlled KMS keys.
- [ ] PII and sensitive data scrubbing: automated redaction proxy active in the ingestion pipeline with deterministic failure boundaries.
- [ ] Deterministic citation verification: model forbidden from returning ungrounded assertions; all claims verified verbatim against authorized internal records.
- [ ] Immutable audit logging: structured events (user ID, document chunks retrieved, output trace, human sign-off) emitted to tamper-proof storage.
- [ ] Model risk documentation: Architecture Decision Record (ADR) and validation report documenting conceptual soundness and benchmark comparisons against heuristic baselines.
- [ ] Human supervisor sign-off gate: high-risk actions or low-confidence outputs routed to human operators with explicit review workflows.

## Related documents

- [Security and compliance](../engineering/05-security-and-compliance.md) - technical security patterns and controls
- [Architecture for customer systems](../system-design/01-architecture-for-customer-systems.md) - enterprise topology and VPC design
- [Reference architectures](../system-design/02-reference-architectures.md) - multi-tenant RAG and operational ontologies
- [Documented LLM deployment cases](02-llm-deployment-cases.md) - public evidence on enterprise AI deployments
- [FDE project selection masterclass](../portfolio/04-project-selection-masterclass.md) - designing permission-aware enterprise systems

## Further reading

- [Federal Reserve SR 11-7: Guidance on Model Risk Management](https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm) - the regulatory standard for model validation in banking
- [HHS HIPAA Guidelines for Professionals](https://www.hhs.gov/hipaa/for-professionals/index.html) - official rules for PHI handling and Business Associate Agreements
- [DoD Cloud Computing Security Requirements Guide](https://public.cyber.mil/devsecops/) - authorization criteria for IL4, IL5, and IL6 national security deployments
- [AWS PrivateLink Documentation](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html) - private connectivity between VPCs and services
