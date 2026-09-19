# Working in Customer Environments

For any engineer about to be embedded with a customer, physically or virtually. Half the
FDE's technical difficulty is not the code - it is everything around the code: getting
access, working an unknown stack, navigating corporate proxies and bastions, security compliance,
and the politics of an enterprise you do not run.

The role definition makes this structural: an FDE "develops and deploys software within a client
company, often working alongside the client's employees for a defined period of time"
([Wikipedia: Forward deployed engineer](https://en.wikipedia.org/wiki/Forward_deployed_engineer)).
The employer side confirms this: Anthropic's FDE posting describes building production applications
inside customer systems, white-glove deployment support, and long-term customer relationships
([Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008)).
The white-glove language is the key: the customer experiences your operating discipline, not just your code.

---

## The first-week playbook (Day 1 to Day 5)

What you execute in week one sets the schedule ceiling for the entire engagement. Work this
structured operational schedule; every item is load-bearing.

```
+-----------------------------------------------------------------------------------+
|                           FIRST-WEEK ONBOARDING SCHEDULE                          |
+-----------------------------------------------------------------------------------+
| Day 1: Identity & Compliance                                                      |
|   - Complete mandatory customer infosec training; provision corporate hardware.  |
|   - Establish password vault, hardware MFA tokens, and SSO identity.              |
+-----------------------------------------------------------------------------------+
| Day 2: Network & Access Inventory                                                 |
|   - File all access requests across repos, clouds, registries, and data stores.   |
|   - Establish Access Dependency Log; agree on ticket approvers and escalation.    |
+-----------------------------------------------------------------------------------+
| Day 3: Local Walking Skeleton & Tooling                                           |
|   - Configure corporate TLS/SSL certs, custom pip/npm mirrors, and bastion keys.  |
|   - Run end-to-end integration pipeline locally against mock contract data.       |
+-----------------------------------------------------------------------------------+
| Day 4: Stakeholder Mapping & System Archaeology                                   |
|   - Conduct 30-minute introductory pairing sessions with primary sysadmins.       |
|   - Read production runbooks, incident post-mortems, and deployment logs.         |
+-----------------------------------------------------------------------------------+
| Day 5: Governance Alignment & Demo Cadence                                        |
|   - Review RACI governance matrix with the executive champion.                    |
|   - Lock in weekly milestone demo time and published status dashboard format.     |
+-----------------------------------------------------------------------------------+
```

### The Access Dependency Log

Approvals take longer than building. A data access request filed on Day 2 that takes 10 business
days is a milestone you planned; the same request filed on Day 15 is an avoidable project crisis.
Maintain an explicit, shared Access Dependency Log updated in every daily standup:

| System / Asset | Access Type | Environment | Request Ticket | Approver / Owner | Status | Mock Workaround |
|---|---|---|---|---|---|---|
| Customer GitHub | `read/write` | Dev / Staging | `SEC-4401` | @dave-infosec | **Approved** | Local git repository |
| AWS VPC Bastion | SSH Jump Host | Staging | `NET-8921` | @sarah-netops | **Pending** (Day 3) | Local Docker Compose |
| Redshift DW | Read Replica | Analytics | `DATA-1092` | @raj-analytics | **Pending** (Day 2) | Synthetic Bitext/CFPB JSON stubs |
| Artifactory NPM | Read Token | Internal Mirror | `IT-3012` | @triage-ops | **Approved** | Corporate `.npmrc` configured |
| Slack / Teams | Guest User | General Tenant | `HR-5501` | @hr-onboarding | **Approved** | Direct email updates |

> [!IMPORTANT]
> Keep the blocked-on-access list visible in every executive status broadcast. Access friction
> is an enterprise operational reality, not a personal failure to absorb in silence. FDEs burn out
> quietly absorbing friction their executive champion could dissolve with a single Slack message.

---

## Tactical bastion, VDI, and network navigation

Enterprise customer environments rarely offer direct public internet egress. You will routinely
operate across bastions, jump hosts, corporate TLS-inspecting proxies, and Virtual Desktop
Infrastructures (VDIs). Master these exact configuration recipes.

### 1. SSH ProxyJump and Bastion Navigation

When accessing private customer subnets through an audited bastion host, never store your private
keys on the bastion. Configure OpenSSH ProxyJump in `~/.ssh/config`:

```sshconfig
# Client Bastion Host (Public Facing DMZ)
Host customer-bastion
    HostName bastion.customer-enterprise.internal
    User fde-contractor
    IdentityFile ~/.ssh/id_ed25519_customer
    ForwardAgent no
    ServerAliveInterval 60
    ServerAliveCountMax 3

# Target Production / Staging Compute Node
Host customer-app-node-01
    HostName 10.240.12.45
    User ec2-user
    IdentityFile ~/.ssh/id_ed25519_customer
    ProxyJump customer-bastion
    StrictHostKeyChecking accept-new
```

To establish a local port-forwarded tunnel to a private PostgreSQL or Redis instance through the bastion:

```bash
# Forward local port 5433 to private RDS instance 10.240.14.88:5432
ssh -N -L 5433:10.240.14.88:5432 customer-bastion
```

### 2. AWS SSM Session Manager Port-Forwarding

Modern enterprise infrastructure frequently disables SSH entirely (port 22 closed), routing
all administrative access through AWS Systems Manager (SSM) Session Manager over IAM:

```bash
# Start an interactive shell session without open ingress ports
aws ssm start-session \
    --target i-0a1b2c3d4e5f67890 \
    --region us-east-1

# Open an encrypted tunnel to a private RDS cluster via SSM
aws ssm start-session \
    --target i-0a1b2c3d4e5f67890 \
    --document-name AWS-StartPortForwardingSessionToRemoteHost \
    --parameters '{"host":["aurora-cluster.internal.vpc"],"portNumber":["5432"],"localPortNumber":["5432"]}'
```

### 3. Corporate TLS Interception & CA Certificate Bundles

Enterprise firewalls (e.g. Zscaler, Palo Alto Networks) inspect outbound HTTPS traffic by
dynamically re-signing SSL certificates with an internal corporate Root Certificate Authority (CA).
Standard tools (`curl`, `pip`, `npm`, `python-requests`) will fail immediately with
`SSL: CERTIFICATE_VERIFY_FAILED`.

Resolve this systematically by obtaining the corporate CA bundle (`corp-ca-bundle.crt`) from internal IT:

```bash
# Set system-wide environment variables for Python, Node, and AWS CLI
export REQUESTS_CA_BUNDLE="/etc/ssl/certs/corp-ca-bundle.crt"
export SSL_CERT_FILE="/etc/ssl/certs/corp-ca-bundle.crt"
export NODE_EXTRA_CA_CERTS="/etc/ssl/certs/corp-ca-bundle.crt"
export AWS_CA_BUNDLE="/etc/ssl/certs/corp-ca-bundle.crt"

# Configure pip to trust the corporate CA bundle permanently
pip config set global.cert /etc/ssl/certs/corp-ca-bundle.crt

# Configure npm / yarn to trust the internal CA
npm config set cafile /etc/ssl/certs/corp-ca-bundle.crt
```

### 4. Custom Internal Artifact Registries (Artifactory / Nexus)

Air-gapped and regulated customer environments block direct access to `pypi.org` and `registry.npmjs.org`,
routing package installs through scanned internal mirrors:

```ini
# ~/.config/pip/pip.conf
[global]
index-url = https://artifactory.customer-enterprise.internal/artifactory/api/pypi/pypi-virtual/simple
trusted-host = artifactory.customer-enterprise.internal
cert = /etc/ssl/certs/corp-ca-bundle.crt
```

```ini
# ~/.npmrc
registry=https://artifactory.customer-enterprise.internal/artifactory/api/npm/npm-virtual/
strict-ssl=true
cafile=/etc/ssl/certs/corp-ca-bundle.crt
```

---

## Reverse-engineering unfamiliar customer stacks

You will frequently encounter systems nobody fully understands: a 12-year-old monolithic service,
a homegrown batch job scheduler, or database schemas held only in tribal memory.
Reverse-engineer respectfully using observational forensics rather than destructive poking.

### 1. Schema Archaeology via System Catalogs

Never execute broad table dumps or run `SELECT * FROM large_table` in unfamiliar databases. Query
system catalogs to map primary keys, foreign keys, and indexes:

```sql
-- PostgreSQL: Extract column types, nullability, and default expressions safely
SELECT 
    table_name, column_name, data_type, is_nullable, column_default
FROM 
    information_schema.columns 
WHERE 
    table_schema = 'public' 
ORDER BY 
    table_name, ordinal_position;

-- PostgreSQL: Identify index bloat and unindexed foreign keys
SELECT
    relname AS table_name,
    indexrelname AS index_name,
    idx_scan AS number_of_scans
FROM
    pg_stat_user_indexes
ORDER BY
    idx_scan ASC;
```

```bash
# Redis: NEVER run 'KEYS *' in production (blocks the single-threaded event loop)
# Always use non-blocking cursor-based scanning:
redis-cli --scan --pattern "tenant:*:session" --count 100 | head -n 20
```

### 2. Tracing Live REST Contracts with OpenAPI / cURL Inspections

When internal APIs lack up-to-date documentation, extract the live JSON contracts:

```bash
# 1. Probe for automated documentation endpoints
curl -s -k -H "Authorization: Bearer $TOKEN" https://internal-service.local/openapi.json | jq '.paths | keys'

# 2. Inspect response headers and latency breakdown
curl -w "\nHTTP: %{http_code} | DNS: %{time_namelookup}s | Connect: %{time_connect}s | TTFB: %{time_starttransfer}s | Total: %{time_total}s\n" \
     -H "Content-Type: application/json" \
     -X POST https://internal-service.local/api/v1/triage \
     -d '{"test": true}'
```

### 3. The "Walking Skeleton" Bypass

When customer security tickets take days to approve, never sit idle waiting for credentials. Build
against the **Walking Skeleton** pattern proven in [`portfolio/reference-project/`](../portfolio/reference-project/README.md):
1. Write interface contracts using Pydantic / TypeScript matching the expected schema.
2. Implement mock adapters that return realistic synthetic payloads (e.g. using public CFPB/Bitext data schemas).
3. Validate the entire business logic, retrieval pipeline, and error handling locally.
4. When production credentials finally clear, replacing the mock adapter with the live client takes less than 30 minutes.

---

## Security and behavioral norms in regulated enclaves

Security officers evaluate your personal operating discipline before they review your code.
Violating an enterprise infosec norm will get your account revoked and your engagement terminated.

```
+-----------------------------------------------------------------------------------+
|                        SECURITY & COMPLIANCE GUARDRAILS                           |
+-----------------------------------------------------------------------------------+
| [!] ZERO Customer Data on Personal Hardware: Never copy prod rows to local disk.  |
| [!] ZERO Unvetted SaaS Extensions: Do not install unapproved AI browser plugins.   |
| [!] Screen-Sharing Discipline: Close all customer tabs/Slack before presenting.   |
| [!] Assume Session Recording: All bastion/VDI terminals are audited and recorded. |
| [!] Strict Tenant Isolation: Never reuse tokens or configs across customers.      |
+-----------------------------------------------------------------------------------+
```

- **Data Loss Prevention (DLP) Tripwires**: Enterprise endpoints run DLP agents (e.g. CrowdStrike,
  Symantec, Microsoft Defender for Cloud). Copying customer data to personal cloud storage (Google Drive,
  Dropbox), personal GitHub repos, or plugging in an unapproved USB drive will trigger an automated
  Sev-1 infosec alert.
- **Audit Logging and Telemetry**: Assume every command executed on jump hosts or inside VDIs is
  logged by audit daemons (e.g. `auditd`, Teleport session recording, CyberArk). Do not test syntax
  interactively with sensitive customer credentials in bash arguments (which leak to `history`). Pass
  credentials via environment variables or secret vaults.
- **Clean-Screen Protocol**: Before sharing your screen in any cross-functional meeting:
  1. Close all email, Slack, and messaging clients.
  2. Open an isolated incognito browser window dedicated solely to the demo.
  3. Verify that zero internal customer identifiers or unredacted PII appear in bookmarks or history.

---

## Enterprise politics and stakeholder alignment

You are arriving with budget, executive attention, and executive expectations that affect
existing organizational dynamics. Navigate internal dynamics with intentional empathy and rigor.

### The Enterprise RACI Matrix

Establish clear ownership boundaries across teams during Week 1 to avoid contested decisions:

| Engagement Workstream | Lead FDE | Customer Sponsor (VP) | Customer Tech Lead | InfoSec Reviewer | Support Operations |
|---|---|---|---|---|---|
| **Architecture Specification** | **Accountable** | Informed | Consulted | Consulted | Consulted |
| **IAM & Network Provisioning** | Consulted | Informed | **Accountable** | Consulted | Informed |
| **Security & Compliance Sign-Off**| Consulted | Informed | Informed | **Accountable** | Informed |
| **Pipeline & Service Deployment** | **Accountable** | Informed | Consulted | Informed | Informed |
| **User Acceptance Testing (UAT)** | Consulted | Accountable | Informed | Informed | **Responsible** |
| **Production Rollback Authority** | Responsible | **Accountable** | Responsible | Consulted | Informed |

*Legend*: **A** = Accountable (Final decision maker); **R** = Responsible (Does the work); **C** = Consulted (Provides two-way input); **I** = Informed (Kept updated).

### Overcoming the "Not-Invented-Here" (NIH) Syndrome

Internal engineering teams frequently wanted to build your project in-house and were overruled by
leadership. Their initial skepticism is rational and defensive. Win them over:
1. **Never criticize their legacy code in writing**: Code comments and pull request reviews in customer
   repositories are permanent enterprise artifacts. Frame limitations as historical trade-offs:
   *"This design made total sense under the 2022 throughput constraints; here is how we scale it for 2026."*
2. **Make the internal engineers co-authors**: Invite their senior engineer to co-design the boundary
   interface. Feature their name prominently on the architecture specification sign-off block.
3. **Automate their operational toil**: If your pipeline eliminates their late-night triage pager shifts,
   they will become your strongest advocates.

---

## Onsite vs remote allocation

Empirical analysis of 146 Forward-Deployed Engineer job postings reveals that travel requirements
are highly concentrated: only 9.0% of general market listings require continuous travel, while
frontier AI labs (such as Anthropic) benchmark onsite travel at approximately 25% for high-touch
enterprise deployments.

Spend onsite travel budgets strategically on the three phases where physical presence alters the outcome:

```
                  THE HIGH-IMPACT ONSITE DECISION MATRIX
+--------------------------------------------------------------------------+
|  TRAVEL JUSTIFIED (Onsite Essential)    |  REMOTE PREFERRED (Default)     |
+-----------------------------------------+--------------------------------+
| 1. Kickoff & Discovery Week             | 1. Routine sprint development  |
|    - High-bandwidth whiteboarding       | 2. Spec drafts & PR reviews    |
|    - Direct face-to-face trust building | 3. Automated eval benchmark runs|
| 2. Identity & Network Integration Crunch| 4. Weekly status dashboards    |
|    - Co-located debugging with NetOps   | 5. Standard async maintenance  |
| 3. Production Go-Live War Room          |                                |
|    - Real-time decision gating          |                                |
| 4. Sev-0 Post-Mortem De-escalation      |                                |
|    - Physical presence demonstrates care|                                |
+--------------------------------------------------------------------------+
```

---

## Related documents

- [The engagement lifecycle](01-engagement-lifecycle.md) - the 10-phase sequence governing customer onboarding
- [Requirements to spec](02-requirements-to-spec.md) - converting discovery interviews into executable acceptance criteria
- [Managing expectations](04-managing-expectations.md) - calibrated de-escalation and trust equation protocols
- [Security and compliance](../engineering/05-security-and-compliance.md) - in-depth analysis of SOC 2, HIPAA, and data fencing
- [Debugging customer systems](../troubleshooting/02-debugging-customer-systems.md) - hands-on diagnostic runbooks for production VPCs
- [Reference Project Implementation](../portfolio/reference-project/README.md) - working walking-skeleton implementation with RBAC filtering

## Further reading

- [Anthropic Forward Deployed Engineer Guide](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) -
  canonical employer specification outlining customer-embedded engineering expectations
- [Wikipedia: Forward Deployed Engineer](https://en.wikipedia.org/wiki/Forward_deployed_engineer) -
  foundational role taxonomy, origins at Palantir, and modern industry adoption
- [AWS Systems Manager Session Manager Documentation](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html) -
  port forwarding and keyless bastion access architecture
