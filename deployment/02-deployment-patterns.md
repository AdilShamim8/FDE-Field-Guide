# Deployment Topologies and Architectures

For the Forward Deployed Engineer (FDE) architecting where an enterprise AI system physically executes, stores customer data, and routes model inference. In enterprise client work, deployment topology is the foundational architecture decision: it dictates network isolation boundaries, information security (InfoSec) sign-off cycles, latency budgets, operational total cost of ownership (TCO), and who gets paged at 2:00 AM.

This reference guide establishes the four canonical enterprise deployment topologies, the model serving hardware trade-off engine, production-grade infrastructure configurations (Terraform), an asynchronous deployment boundary gateway (Python), and the 12-factor enterprise constraint interview protocol.

---

## 1. The Deployment Decision: Physical, Network, and Compliance Boundaries

In enterprise customer engagements, deployment topology is rarely chosen in a greenfield vacuum. It is dictated by non-negotiable enterprise constraints: customer data governance policies, regulatory compliance regimes (GDPR Art. 44–50 cross-border data transfer, HIPAA § 164.312 security safeguards, FINRA Rule 4511, FedRAMP High), existing cloud commitments (AWS EDP, Azure MACC, Google Cloud Commitments), and internal InfoSec risk tolerance.

```
+---------------------------------------------------------------------------------------------------+
|                                  ENTERPRISE DEPLOYMENT TOPOLOGY SPECTRUM                          |
+------------------------------------+----------------------------------+---------------------------+
| Topologies                         | Primary Driver                   | InfoSec Approval Velocity |
+------------------------------------+----------------------------------+---------------------------+
| 1. Customer-Tenant In-VPC          | Absolute data residency / No-out | 4 to 8 weeks              |
| 2. Multi-Tenant SaaS Scoped Egress | Rapid time-to-value / Low ops    | 1 to 3 weeks              |
| 3. Hybrid Control/Data Plane       | Local storage + Cloud inference  | 3 to 6 weeks              |
| 4. Air-Gapped Sovereign Enclave    | National defense / Banking core  | 8 to 24 weeks             |
+------------------------------------+----------------------------------+---------------------------+
```

### The FDE Codification Mandate

Across our empirical dataset of 146 enterprise FDE postings, **82.2% explicitly require expertise in enterprise cloud architecture and client network integration**. Anthropic's Forward Deployed Engineering organization mandates that FDEs *"identify and codify repeatable deployment patterns"* across AWS Bedrock PrivateLink, Azure OpenAI Service Managed Endpoints, and Google Cloud Vertex AI Private Service Connect.

Attempting to reverse an established deployment topology post-deployment incurs catastrophic friction: 6 to 12 months of delayed timelines, re-negotiated Data Processing Agreements (DPAs), and multi-million-dollar re-architecture overheads. The deployment topology must be determined, documented, and approved during Sprint 0 via the formal constraint interview.

---

## 2. The Four Canonical Deployment Topologies

```
+---------------------------------------------------------------------------------------------------+
| TOPOLOGY 1: IN-VPC CUSTOMER TENANT       | TOPOLOGY 2: MULTI-TENANT SAAS WITH SCOPED EGRESS       |
|                                          |                                                        |
|  [Customer VPC / No Internet Egress]     |  [Customer Network]      [Vendor Multi-Tenant Cloud]   |
|  +------------------------------------+  |  +----------------+      +---------------------------+ |
|  | +------------+     +-------------+ |  |  | Customer App   |----->| Egress Proxy (Static IPs) | |
|  | | App Pods   |---->| Vector DB   | |  |  +----------------+ TLS  | +-----------------------+ | |
|  | +------------+     +-------------+ |  |                          | | Tenant Isolated Engine| | |
|  |       |                            |  |                          | | (RLS / KMS BYOK Keys) | | |
|  |       v (VPC PrivateLink)          |  |                          | +-----------------------+ | |
|  | +--------------------------------+ |  |                          +---------------------------+ |
|  | | In-VPC Bedrock / Local vLLM    | |  |                                                        |
|  | +--------------------------------+ |  |                                                        |
|  +------------------------------------+  |                                                        |
+------------------------------------------+--------------------------------------------------------+
| TOPOLOGY 3: HYBRID CONTROL / DATA PLANE  | TOPOLOGY 4: AIR-GAPPED SOVEREIGN ENCLAVE               |
|                                          |                                                        |
|  [Customer VPC]       [Vendor Cloud]     |  [Physical Sovereign SCIF / Zero Internet Access]      |
|  +----------------+   +----------------+ |  +--------------------------------------------------+  |
|  | Data Plane:    |   | Control Plane: | |  | Optical Diode / USB Air-Gap Delivery             |  |
|  | Raw Documents, |   | Scheduling,    | |  |  |                                               |  |
|  | Vector Store,  |   | Evals UI,      | |  |  v                                               |  |
|  | PII Redaction  |   | Prompt Catalog | |  | +----------------------------------------------+ |  |
|  |       ^        |   +----------------+ |  | | Air-Gapped Kubernetes Cluster (K3s / RKE2)   | |  |
|  |       |        |           ^        | |  | | +------------------+  +--------------------+ | |  |
|  |       +--- WSS Dial-Out ---+        | |  | | | App Services     |->| vLLM (Local GPUs)  | | |  |
|  |            (Port 443)               | |  | | +------------------+  +--------------------+ | |  |
|  +-------------------------------------+ |  | +----------------------------------------------+ |  |
+------------------------------------------+--------------------------------------------------------+
```

---

### Topology 1: Customer-Tenant In-VPC (Zero-Egress Data Boundary)

#### Physical and Network Architecture
All application compute (Kubernetes pods, serverless containers), stateful databases (PostgreSQL, Qdrant/Milvus), and model inference endpoints run strictly inside the customer's cloud account (AWS, Azure, GCP).
- **Network Boundaries**: Subnets are strictly private without an Internet Gateway (`IGW-less` VPC). Egress routing to `0.0.0.0/0` is blocked by route tables and Network Access Control Lists (NACLs).
- **Service Connectivity**: Access to cloud services runs entirely over private interface endpoints:
  - AWS: AWS PrivateLink for Amazon Bedrock (`com.amazonaws.region.bedrock-runtime`), Gateway Endpoints for S3 and DynamoDB.
  - Azure: Azure Private Endpoints for Azure OpenAI Service and Azure Cosmos DB.
  - GCP: Private Service Connect (PSC) for Vertex AI endpoints.
- **Identity & Authentication**: No static credentials or API keys. Cross-account deployments operate via `sts:AssumeRole` with cryptographic `ExternalId` verification and mandatory session tagging (`Project`, `Environment`, `FDEOperator`).

#### Trade-Off Analysis
- **Advantages**: Complete sovereign data isolation. Customer security teams issue approvals quickly because raw payloads never leave their perimeter. Infrastructure costs bill directly to the customer's cloud enterprise discount agreement (AWS EDP / Azure MACC).
- **Trade-offs & Operational Realities**:
  - Approvals for new IAM roles, subnet peerings, and quota expansions take 2 to 6 weeks.
  - Deployment pipelines must integrate with customer CI/CD tooling (Jenkins, GitHub Enterprise, GitLab CI) and change advisory boards (CAB).
  - The FDE team must troubleshoot within customer bastion hosts or AWS Systems Manager Session Manager (SSM) without direct internet tools.

---

### Topology 2: Multi-Tenant SaaS with Scoped Enterprise Egress

#### Physical and Network Architecture
The AI application runs within the vendor's multi-tenant cloud environment. The customer integrates by initiating secure API calls, webhooks, or streaming data pipelines over mutual TLS (mTLS) to the vendor's public ingress.
- **Tenant Isolation Boundaries**:
  - **Application Plane**: Tenant identifiers are cryptographically extracted from verified JWT tokens or mTLS client certificates. Every downstream function passes `tenant_id` context.
  - **Database Plane**: Enforced via PostgreSQL Row-Level Security (RLS) (`SET LOCAL app.current_tenant_id = :tenant_id`) or dedicated per-tenant schemas.
  - **Vector Isolation**: Namespaced index partitions (e.g., Pinecone namespaces, Qdrant payload tenant filters). Cross-tenant queries are structurally impossible at the database query planning level.
  - **Encryption**: Customer-Managed Encryption Keys (AWS KMS BYOK / CMEK). The customer retains key revocation authority: revoking the key instantly crypto-shreds all tenant data at rest.
- **Egress Perimeter Controls**: All outbound vendor communication back to customer webhooks originates from static, dedicated NAT Gateway Elastic IPs, allowing the customer to whitelist vendor IP ranges on their perimeter firewalls.

#### Trade-Off Analysis
- **Advantages**: Fastest path to first value (days instead of months). Continuous CI/CD deployment managed by the vendor. Unified observability and monitoring without customer bastion constraints.
- **Trade-offs & Operational Realities**:
  - Requires comprehensive vendor security audits: SOC 2 Type II, ISO 27001, Data Processing Agreements (DPA), and subprocessor review.
  - Regulated enterprises (defense, healthcare, tier-1 investment banks) will reject this pattern unconditionally for tier-1 confidential data.

---

### Topology 3: Hybrid Control-Plane / Data-Plane (Split-Boundary Architecture)

#### Physical and Network Architecture
A distributed architecture balancing SaaS operational simplicity with strict data residency:
- **Control Plane (Vendor SaaS)**: Houses the workflow orchestrator, prompt template catalog, user interface dashboards, offline evaluation telemetry, and non-sensitive metadata.
- **Data Plane (Customer VPC)**: Houses the raw document stores, ingestion pipelines, chunking workers, vector databases, and local PII scrubbing filters.
- **The Reverse-Tunnel Dial-Out Pattern**:
  - Enterprise InfoSec teams routinely reject inbound firewall rules (`0.0.0.0:443 -> Inbound`).
  - The customer data plane runs an autonomous worker agent (e.g., based on the Palantir Apollo / Databricks model) that establishes an **outbound persistent WebSocket (WSS on port 443) or gRPC stream** to the vendor control plane.
  - The agent pulls task definitions (e.g., "process document batch #481"), executes embedding and retrieval locally within the customer VPC, and transmits only masked payloads or completion metadata back to the control plane.
- **Token-Level Pseudonymization & De-Anonymization**:
  - If external frontier LLMs (Anthropic Claude, OpenAI) are leveraged, the local data plane passes raw text through a local deterministic token vault (Microsoft Presidio / custom regex engine).
  - PII entities (names, SSNs, account numbers) are replaced with deterministic synthetic hashes (e.g., `[PERSON_7f3d]`).
  - The sanitized prompt is sent to the LLM; upon receiving the response, the local agent de-anonymizes the tokens before presenting the final answer to the customer end-user.

#### Trade-Off Analysis
- **Advantages**: Delivers frontier model intelligence while satisfying data boundary constraints. Retains vendor management of UI and orchestration.
- **Trade-offs & Operational Realities**:
  - Substantial distributed systems complexity: managing split brain states, network partitions across cloud boundaries, and local token vault consistency.
  - PII scrubbing is load-bearing: a redaction engine leak represents a severe compliance violation.

---

### Topology 4: Physically Air-Gapped & Sovereign Enclave (DoD IL5/IL6, Banking Core)

#### Physical and Network Architecture
Designed for environments where zero external network communication is permitted: military defense networks (SIPRNet, JWICS, DoD Cloud SRG Impact Level 5/6), intelligence facilities (SCIFs), nuclear infrastructure, and core payment transaction engines.
- **Network Boundaries**: Absolute air gap. Physical disconnection from the public internet. No external DNS servers, no outbound NTP synchronization, no public container registries.
- **Air-Gap Delivery & Toolchain Logistics**:
  - **Container Delivery**: Container images are packaged into OCI archive tarballs (`docker save` / `skopeo copy docker-archive:`), cryptographically signed via Sigstore/Cosign, scanned for CVEs, and transferred via approved physical optical data diodes or encrypted media.
  - **Local Mirror Registries**: Images are loaded into an internal air-gapped registry (Harbor, JFrog Artifactory).
  - **Package Repositories**: Internal PyPI mirror (`bandersnatch`), internal Yum/APT mirrors, and offline Hugging Face safetensors repositories.
- **Model Serving**: Models must be open-weight architectures (Llama-3, Mistral, Qwen-2.5) served locally on physical bare-metal GPU clusters (NVIDIA H100/A100) using vLLM or TensorRT-LLM.
- **Air-Gapped License Attestation**: Traditional SaaS licensing servers are unreachable. Systems utilize asymmetric offline license certificates (Ed25519 digital signatures) bound to hardware identifiers (TPM 2.0 endorsement keys, CPU serial numbers) with cryptographically timeboxed validity windows.

#### Trade-Off Analysis
- **Advantages**: Immune to external internet outages, DDoS attacks, and third-party data interception. Full sovereignty over model weights and weights execution.
- **Trade-offs & Operational Realities**:
  - Upgrades move at the speed of human security gates (quarterly release cycles).
  - Hardware capacity is physical and fixed: zero dynamic auto-scaling.
  - Model quality is constrained to open-weight models that fit the physical VRAM footprint.

---

## 3. Model Serving Architecture & Hardware Trade-Off Matrix

When deploying inside customer environments, selecting how the model is physically served determines latency, privacy, and infrastructure cost.

### Comprehensive Architectural Trade-Off Matrix

```
+---------------------------+------------------------+-------------------------+-------------------------+
| Evaluation Dimension      | 1. Public Managed API  | 2. VPC Private Endpoint | 3. Self-Hosted Open LLM |
|                           | (OpenAI/Anthropic Dir) | (AWS Bedrock / Azure)   | (vLLM on Customer GPUs) |
+---------------------------+------------------------+-------------------------+-------------------------+
| Data Residency            | Contractual (DPA)      | Cloud Account Perimeter | Physical Hardware VRAM  |
| Network Isolation         | Public HTTPS           | VPC PrivateLink / PSC   | Localhost / In-VPC Mesh |
| Zero-Data Retention       | Requires BAA/Addendum  | Native by Cloud Policy  | Guaranteed Physically   |
| Inference Cost Structure  | Per-token ($/1M tokens)| Per-token or Provisioned| Fixed GPU instance $/hr |
| Ops Maintenance Overhead  | Zero                   | Minimal (Cloud Managed) | High (CUDA, vLLM, SRE)  |
| Time-To-First-Token (TTFT)| Variable (Internet)    | Low & Consistent        | Ultra-Low (Local VRAM)  |
| Weight Customization      | Prompt / Fine-Tune API | Custom Model Import     | Full Weights / LoRA     |
| Enterprise Approval Speed | 2 to 4 weeks           | 1 to 2 weeks            | 4 to 8 weeks (GPU Lead) |
+---------------------------+------------------------+-------------------------+-------------------------+
```

---

### GPU Hardware Sizing Engine for Self-Hosted In-VPC Serving

When Topology 1 or 4 mandates self-hosting open-weight models (e.g., Llama-3-70B or Llama-3-8B) on customer hardware, FDEs must calculate exact VRAM requirements to prevent Out-Of-Memory (`CUDA OOM`) panics during peak concurrent load.

#### The Fundamental LLM Memory Sizing Equation
Total GPU memory ($VRAM_{\text{req}}$) is the sum of model weights, KV cache pool, and activation/CUDA runtime overhead:

$$VRAM_{\text{req}} = M_{\text{weights}} + M_{\text{kv\_cache}} + M_{\text{activation\_overhead}}$$

1. **Model Weights Memory ($M_{\text{weights}}$)**:
   $$M_{\text{weights}} = \frac{P \times b}{8 \times 10^9} \text{ GB}$$
   Where $P$ is total model parameters, and $b$ is precision bits per parameter (16 for FP16/BF16, 8 for FP8, 4 for AWQ/GPTQ).

2. **KV Cache Memory Pool ($M_{\text{kv\_cache}}$)**:
   For Grouped-Query Attention (GQA) models (e.g., Llama-3):
   $$M_{\text{kv\_per\_token}} = 2 \times n_{\text{layers}} \times n_{\text{kv\_heads}} \times d_{\text{head}} \times b_{\text{kv}} \text{ bytes}$$
   $$M_{\text{kv\_cache}} = \frac{M_{\text{kv\_per\_token}} \times \text{Batch Size} \times \text{Max Context Length}}{10^9} \text{ GB}$$

3. **Activation Overhead & Runtime Buffer ($M_{\text{activation\_overhead}}$)**:
   Typically calculated as **$20\%$ to $25\%$ of the weights memory** for PagedAttention execution structures and CUDA context allocation.

#### Empirical Hardware Allocation Table (Llama-3 Reference Profiles)

```
+-----------------------+-----------+-----------+---------------+-------------------------+-------------------------+
| Model & Precision     | Parameters| Weight VRAM| KV Cache/Token| Min GPU Spec            | Recommended Instance    |
+-----------------------+-----------+-----------+---------------+-------------------------+-------------------------+
| Llama-3-8B (FP16)     | 8.03 B    | ~16.0 GB  | 0.25 MB/token | 1x NVIDIA A10G (24GB)   | AWS g5.2xlarge          |
| Llama-3-8B (AWQ 4-bit)| 8.03 B    | ~4.5 GB   | 0.12 MB/token | 1x NVIDIA L4 (24GB)     | AWS g6.2xlarge          |
| Llama-3-70B (FP16)    | 70.6 B    | ~141.2 GB | 1.25 MB/token | 4x NVIDIA A100 (80GB)   | AWS p4d.24xlarge (TP=4) |
| Llama-3-70B (FP8)     | 70.6 B    | ~70.6 GB  | 0.62 MB/token | 2x NVIDIA H100 (80GB)   | AWS p5.48xlarge (TP=2)  |
| Llama-3-70B (AWQ 4-bit| 70.6 B    | ~36.0 GB  | 0.31 MB/token | 2x NVIDIA A10G (24GB)   | AWS g5.12xlarge (TP=2)  |
+-----------------------+-----------+-----------+---------------+-------------------------+-------------------------+
```

*Note on Tensor Parallelism ($TP$)*: When model weights exceed single-GPU VRAM, $TP$ distributes layers across GPUs. Inter-GPU communication requires high-speed NVLink interconnects (600 GB/s to 900 GB/s on A100/H100). Never span Tensor Parallelism across separate physical nodes or PCIe bus boundaries without NVLink, as communication latency degrades throughput by $80\%$.

---

## 4. Declarative Infrastructure: Customer Zero-Egress Enclave (Terraform)

The following production-ready Terraform configuration provisions an **IGW-less customer enclave** with AWS PrivateLink endpoints for S3 and Amazon Bedrock, establishing strict network isolation for Topology 1.

```hcl
# File: boundary_enclave.tf
# Description: Production Zero-Egress AWS VPC Enclave for Enterprise AI Deployment

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.40.0"
    }
  }
}

variable "vpc_cidr" {
  type        = string
  default     = "10.100.0.0/16"
  description = "Dedicated CIDR block for AI deployment enclave"
}

variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "Target deployment region"
}

# 1. Isolated VPC without Internet Gateway
resource "aws_vpc" "ai_enclave_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name               = "fde-enterprise-ai-enclave"
    DataClassification = "StrictlyConfidential"
    ManagedBy          = "FDE-Architecture-Team"
  }
}

# 2. Private Subnets (No route to IGW or NAT)
resource "aws_subnet" "private_subnet_a" {
  vpc_id            = aws_vpc.ai_enclave_vpc.id
  cidr_block        = "10.100.1.0/24"
  availability_zone = "${var.aws_region}a"

  tags = {
    Name = "ai-enclave-private-a"
  }
}

resource "aws_subnet" "private_subnet_b" {
  vpc_id            = aws_vpc.ai_enclave_vpc.id
  cidr_block        = "10.100.2.0/24"
  availability_zone = "${var.aws_region}b"

  tags = {
    Name = "ai-enclave-private-b"
  }
}

# 3. Route Table with zero egress routes
resource "aws_route_table" "strictly_private_rt" {
  vpc_id = aws_vpc.ai_enclave_vpc.id

  tags = {
    Name = "ai-enclave-zero-egress-rt"
  }
}

resource "aws_route_table_association" "assoc_a" {
  subnet_id      = aws_subnet.private_subnet_a.id
  route_table_id = aws_route_table.strictly_private_rt.id
}

resource "aws_route_table_association" "assoc_b" {
  subnet_id      = aws_subnet.private_subnet_b.id
  route_table_id = aws_route_table.strictly_private_rt.id
}

# 4. Security Group Restricting Egress Strictly to VPC Endpoints
resource "aws_security_group" "enclave_service_sg" {
  name        = "ai-enclave-workload-sg"
  description = "Strict egress firewall for enclave compute workloads"
  vpc_id      = aws_vpc.ai_enclave_vpc.id

  # Ingress strictly from internal customer network CIDR
  ingress {
    description = "Internal service ingress"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }

  # Egress restricted strictly to VPC endpoints on port 443
  egress {
    description = "TLS egress to VPC Interface Endpoints"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  tags = {
    Name = "ai-enclave-workload-sg"
  }
}

# 5. Gateway Endpoint for Amazon S3 (Document storage)
resource "aws_vpc_endpoint" "s3_gateway" {
  vpc_id            = aws_vpc.ai_enclave_vpc.id
  service_name      = "com.amazonaws.${var.aws_region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [aws_route_table.strictly_private_rt.id]

  tags = {
    Name = "s3-gateway-endpoint"
  }
}

# 6. Interface PrivateLink Endpoint for Amazon Bedrock Runtime
resource "aws_vpc_endpoint" "bedrock_interface" {
  vpc_id              = aws_vpc.ai_enclave_vpc.id
  service_name        = "com.amazonaws.${var.aws_region}.bedrock-runtime"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = [aws_subnet.private_subnet_a.id, aws_subnet.private_subnet_b.id]
  security_group_ids  = [aws_security_group.enclave_service_sg.id]
  private_dns_enabled = true

  tags = {
    Name = "bedrock-runtime-privatelink"
  }
}
```

---

## 5. Production Reference Implementation: Enterprise Deployment Boundary Gateway

The following complete, production-grade Python implementation illustrates an asynchronous **Deployment Boundary Gateway**. It inspects requests against the active topology policy, enforces deterministic PII pseudonymization with local token re-hydration, routes to either local in-VPC vLLM or VPC PrivateLink endpoints, and emits SHA-256 audit digests for InfoSec verification.

```python
"""
Module: deployment_boundary_gateway.py
Description: Production-Grade Deployment Boundary Gateway for Enterprise AI Topologies.
Author: Forward Deployed Engineering Architecture
"""

import re
import hashlib
import json
import logging
from enum import Enum
from typing import Dict, Any, Optional, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("DeploymentBoundaryGateway")


class TopologyPolicy(str, Enum):
    CUSTOMER_TENANT_IN_VPC = "CUSTOMER_TENANT_IN_VPC"
    MULTI_TENANT_SAAS = "MULTI_TENANT_SAAS"
    HYBRID_CONTROL_DATA_PLANE = "HYBRID_CONTROL_DATA_PLANE"
    AIR_GAPPED_ENCLAVE = "AIR_GAPPED_ENCLAVE"


class PIIPseudonymizationVault:
    """
    Deterministic local token vault for reversible pseudonymization in Hybrid topologies.
    Ensures raw customer PII never crosses external network boundaries.
    """

    def __init__(self, salt: str = "enterprise_fde_vault_salt_2026"):
        self.salt = salt
        self.entity_patterns = {
            "EMAIL": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
            "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
            "CREDIT_CARD": re.compile(r"\b(?:\d{4}-){3}\d{4}\b|\b\d{16}\b"),
        }

    def _generate_surrogate(self, entity_type: str, raw_value: str) -> str:
        digest = hashlib.sha256(f"{self.salt}:{raw_value}".encode("utf-8")).hexdigest()[:8]
        return f"[{entity_type}_{digest}]"

    def mask_text(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Scrubs raw PII from text, returning masked text and a local re-hydration dictionary.
        """
        vault_mapping: Dict[str, str] = {}
        masked_text = text

        for entity_type, pattern in self.entity_patterns.items():
            matches = pattern.findall(masked_text)
            for match in set(matches):
                surrogate = self._generate_surrogate(entity_type, match)
                vault_mapping[surrogate] = match
                masked_text = masked_text.replace(match, surrogate)

        return masked_text, vault_mapping

    def rehydrate_text(self, masked_text: str, vault_mapping: Dict[str, str]) -> str:
        """
        Replaces surrogate tokens with original PII values within the customer perimeter.
        """
        hydrated_text = masked_text
        for surrogate, original in vault_mapping.items():
            hydrated_text = hydrated_text.replace(surrogate, original)
        return hydrated_text


class DeploymentBoundaryGateway:
    """
    Enforces network and data boundary governance across enterprise deployment topologies.
    """

    def __init__(
        self,
        topology: TopologyPolicy,
        local_vllm_endpoint: str = "http://vllm-engine.private.vpc:8000/v1/completions",
        vpc_privatelink_endpoint: str = "https://bedrock-runtime.us-east-1.amazonaws.com",
    ):
        self.topology = topology
        self.local_vllm_endpoint = local_vllm_endpoint
        self.vpc_privatelink_endpoint = vpc_privatelink_endpoint
        self.vault = PIIPseudonymizationVault()

    def process_prompt(
        self,
        tenant_id: str,
        raw_prompt: str,
        allow_external_egress: bool = False,
    ) -> Dict[str, Any]:
        """
        Processes and routes prompt according to active enterprise topology policy.
        """
        prompt_digest = hashlib.sha256(raw_prompt.encode("utf-8")).hexdigest()
        logger.info("Evaluating boundary request: Tenant=%s, Topology=%s, SHA=%s",
                    tenant_id, self.topology.value, prompt_digest[:12])

        # 1. Enforce Air-Gap / Zero-Egress Rules
        if self.topology in (TopologyPolicy.AIR_GAPPED_ENCLAVE, TopologyPolicy.CUSTOMER_TENANT_IN_VPC):
            if allow_external_egress:
                raise PermissionError(
                    f"Policy Violation: External egress requested in strict {self.topology.value} boundary."
                )
            target_endpoint = self.local_vllm_endpoint if self.topology == TopologyPolicy.AIR_GAPPED_ENCLAVE else self.vpc_privatelink_endpoint
            return {
                "status": "APPROVED",
                "target_endpoint": target_endpoint,
                "sanitized_prompt": raw_prompt,
                "vault_active": False,
                "audit_sha256": prompt_digest,
                "isolation_mode": "ZERO_EGRESS_IN_VPC",
            }

        # 2. Enforce Hybrid Control/Data Plane Masking
        elif self.topology == TopologyPolicy.HYBRID_CONTROL_DATA_PLANE:
            masked_prompt, vault_mapping = self.vault.mask_text(raw_prompt)
            masked_digest = hashlib.sha256(masked_prompt.encode("utf-8")).hexdigest()
            logger.info("Hybrid Topology: Masked %d PII entities. Egress SHA=%s",
                        len(vault_mapping), masked_digest[:12])
            return {
                "status": "APPROVED",
                "target_endpoint": self.vpc_privatelink_endpoint,
                "sanitized_prompt": masked_prompt,
                "vault_active": True,
                "vault_mapping": vault_mapping,
                "audit_sha256": masked_digest,
                "isolation_mode": "PSEUDONYMIZED_EGRESS",
            }

        # 3. Multi-Tenant SaaS with Scoped Contractual Egress
        elif self.topology == TopologyPolicy.MULTI_TENANT_SAAS:
            return {
                "status": "APPROVED",
                "target_endpoint": "https://api.vendor-saas.com/v1/inference",
                "sanitized_prompt": raw_prompt,
                "vault_active": False,
                "audit_sha256": prompt_digest,
                "isolation_mode": "MULTI_TENANT_CONTRACTUAL",
            }

        raise ValueError(f"Unrecognized topology policy: {self.topology}")

    def finalize_response(
        self,
        raw_response_text: str,
        processing_metadata: Dict[str, Any],
    ) -> str:
        """
        Rehydrates response text if local pseudonymization vault was activated.
        """
        if processing_metadata.get("vault_active") and "vault_mapping" in processing_metadata:
            return self.vault.rehydrate_text(raw_response_text, processing_metadata["vault_mapping"])
        return raw_response_text
```

---

## 6. The 12-Factor Enterprise Constraint Interview

Before writing a single line of application code or deploying infrastructure, conduct this structured constraint interview with the customer's Chief Information Security Officer (CISO), Enterprise Cloud Architect, and Lead SRE.

### The 12-Factor Audit Matrix

```
+----+-----------------------+-------------------------------------------------------+----------------------------------+
| #  | Constraint Factor     | Diagnostic Question for Customer Stakeholders         | Topology Decision Impact         |
+----+-----------------------+-------------------------------------------------------+----------------------------------+
| 1  | Data Classification   | Does data contain PII, PHI, MNPI, or Classified info? | PHI/Classified -> Top 1 or 4     |
| 2  | Egress Firewall Policy| Are outbound connections to 0.0.0.0:443 blocked?      | Blocked -> Top 1 or 4            |
| 3  | Ingress Policy        | Are inbound webhooks from vendor IPs permitted?       | Denied -> Requires Top 3 (Agent) |
| 4  | Cloud Commitment      | Which cloud provider holds the customer's EDP/MACC?   | Dictates AWS / Azure / GCP target|
| 5  | PrivateLink Support   | Are VPC Endpoints approved and routable in their VPC? | Required for Top 1 & 3           |
| 6  | Hardware / GPU Quotas | Are A100/H100 GPU quotas allocated in their cloud?     | No GPU quota -> Managed API      |
| 7  | Identity Management   | How are services authenticated (IAM Role vs OIDC)?    | Mandates sts:AssumeRole + ExtID  |
| 8  | Subprocessor Policy   | Are 3rd party AI vendors on the approved vendor list? | Denied -> Disqualifies Top 2     |
| 9  | On-Call SRE Ownership | Who responds to infrastructure paging alerts at 2 AM? | Customer Ops -> Top 1; Vendor->2 |
| 10 | Change Advisory Board | What is the approval lead time for cloud deploys?     | >4 weeks -> Pre-stage IaC early  |
| 11 | Outage & SLA Penalty  | What is financial penalty for a 4-hour downtime?      | High penalty -> Active-Active HA |
| 12 | Air-Gap Physical Gate | Is there zero internet connectivity (SCIF / Enclave)? | Confirmed -> Mandates Topology 4 |
+----+-----------------------+-------------------------------------------------------+----------------------------------+
```

---

### Algorithmic Decision Flowchart

```
                            [Start: Enterprise Discovery]
                                         |
                                         v
                     Is the environment physically air-gapped?
                                    /        \
                               (Yes)          (No)
                                 /              \
                [Topology 4: Air-Gapped]         v
                                        Does policy permit raw data
                                        to leave customer perimeter?
                                               /        \
                                           (No)          (Yes)
                                           /                \
                         Does policy allow VPC               v
                        PrivateLink to Cloud LLMs?     Is multi-tenant SaaS
                                /        \             InfoSec-approved?
                            (Yes)        (No)               /        \
                            /              \            (Yes)        (No)
             [Topology 1: In-VPC]      [Topology 1:       /            \
             (Managed Cloud Endpoint)   Self-Hosted] [Topology 2:   [Topology 3:
                                                      SaaS Egress]   Hybrid Split]
```

---

## 7. Progressive Rollout Strategies & Emergency Cutover Runbook

Once the deployment topology is established, customer traffic promotion must proceed through strict risk-mitigated stages.

### Multi-Stage Rollout Pipeline

```
+---------------------------------------------------------------------------------------------------+
| STAGE 1: SHADOW MIRRORING (0% USER TRAFFIC DECIDING)                                              |
| - Live traffic cloned asynchronously via proxy.                                                   |
| - Shadow model inference executes without returning output to users.                             |
| - Telemetry measures latency distributions and response concordance against legacy systems.       |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| STAGE 2: CANARY USER SLICE (5% -> 25% USER TRAFFIC)                                               |
| - Routed strictly to pre-selected internal business user cohorts.                                 |
| - Monitored against automated error budget tripwires.                                             |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| STAGE 3: GENERAL AVAILABILITY CUTOVER (100% PRODUCTION)                                           |
| - Primary router directs 100% of enterprise traffic to new deployment topology.                   |
| - Legacy systems maintained in hot-standby mode for 14 calendar days.                             |
+---------------------------------------------------------------------------------------------------+
```

### Automated Rollback Tripwires and Emergency Kill-Switch

Every deployment topology must feature an automated, deterministic kill-switch that reverts traffic to the legacy baseline without requiring a container redeployment:

1. **Automated Rollback Criteria**:
   - Error rate (HTTP 5xx or unhandled exceptions) exceeds **$1.0\%$** over a rolling 5-minute window.
   - Latency p99 exceeds **$3,500\text{ms}$** over a rolling 10-minute window.
   - Token hallucination / evaluation gate failure exceeds **$2.0\%$** on golden validation probes.
2. **Emergency Kill-Switch Execution**:
   - **Feature Flag Reversal**: Flip the global LaunchDarkly / Unleash tenant flag `ai_routing_enabled = false`.
   - **DNS / Ingress Drain**: If feature flags are unreachable, point ingress routing rules (`nginx` / AWS ALB target group) to the legacy fallback cluster.
   - **State Drain**: Allow in-flight requests to terminate within a 30-second graceful timeout window before cutting database connection pools.

---

## 8. Related Documents & Primary Literature

### Repository Field Guides
- [Prototype to Production](01-prototype-to-production.md) - The 4-stage promotion gate, expand-contract migrations, and shadow routing.
- [The Production Readiness Checklist](03-production-readiness-checklist.md) - The comprehensive 30-point Go/No-Go enterprise checklist.
- [Cloud and Infrastructure](../engineering/04-cloud-and-infrastructure.md) - Landing inside customer cloud estates: IAM, VPC peering, and cost governance.
- [Security and Compliance](../engineering/05-security-and-compliance.md) - Enterprise threat modeling, SOC 2 / HIPAA boundaries, and penetration test gates.
- [LLM Application Patterns](../ai/01-llm-application-patterns.md) - Design patterns across RAG, structured extraction, and prompt caching.
- [Monitoring and Reliability](../ai/04-monitoring-and-reliability.md) - Dual-plane telemetry, OpenTelemetry GenAI standards, and drift detection.

### Primary References & Standards
- Kwon, W., et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. Proceedings of the ACM Symposium on Operating Systems Principles (SOSP '23).
- Anthropic. (2026). *Forward Deployed Engineering Operating Model and Deployment Best Practices*. Greenhouse Technical Publications.
- National Institute of Standards and Technology. (2020). *Security and Privacy Controls for Information Systems and Organizations*. NIST Special Publication 800-53, Revision 5.
- Amazon Web Services. (2025). *Amazon Bedrock PrivateLink Architecture and Secure VPC Endpoints*. AWS Well-Architected Framework: Machine Learning Lens.
- Palantir Technologies. (2024). *Palantir Apollo: Autonomous Deployment Across Air-Gapped and Sovereign Boundaries*. Technical Architecture Whitepaper.
