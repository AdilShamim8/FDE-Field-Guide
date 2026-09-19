# Real-World FDE Interview Dataset

A machine-readable, double-verified repository of real-world Forward Deployed Engineer (FDE) interview questions, evaluation signals, candidate playbooks, red flags, and scoring rubrics.

Inspired by the empirical data-first approach of [alexeygrigorev/ai-engineering-field-guide](https://github.com/alexeygrigorev/ai-engineering-field-guide), every question in this dataset is curated directly from real practitioner experiences, interview loops at top frontier labs and enterprise AI companies, and published practitioner guides.

---

## Provenance & Verification Methodology

Unlike traditional software engineering interview banks that use synthetic leetcode puzzles or generic LLM-generated prompts, FDE interview loops are deeply grounded in production realities, messy customer data, and high-stakes stakeholder simulations.

Each question in [fde_interview_questions.json](fde_interview_questions.json) has been compiled and double-verified across six primary practitioner authorities:

| Source Authority | Focus Area / Provenance | Verified URL Reference |
|---|---|---|
| **Nehal Vyas** | Knowledge hub on FDE hiring, real 5-round loop questions, customer simulation dynamics, production triage | [fde.hinehal.com/blogs/fde-interview-questions](https://fde.hinehal.com/blogs/fde-interview-questions) |
| **Om Bharatiya** | Breakout AI role guides, problem decomposition ("decomp") rounds, 48-hour executive demo scoping, hospital COO scenarios | [github.com/ombharatiya/AI-Engineer-Interview-Questions](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md) |
| **Dr. Sundeep Teki** | Frontier AI lab interview coaching (OpenAI, Anthropic, Google DeepMind), "Ambiguity by default" frameworks | [sundeepteki.org/advice/the-definitive-guide-to-forward-deployed-engineer-interviews-in-2026](https://www.sundeepteki.org/advice/the-definitive-guide-to-forward-deployed-engineer-interviews-in-2026) |
| **Dr. Sanjay Kumar, PhD** | Top 25 FDE questions, least-privilege agent tool risks, air-gapped VPC data residency, drift mitigation | [skphd.medium.com/top-25-forward-deployed-engineer-fde-interview-questions-and-answers-ad9ac4a6ad7f](https://skphd.medium.com/top-25-forward-deployed-engineer-fde-interview-questions-and-answers-ad9ac4a6ad7f) |
| **YagyanshB** | Google Forward Deployed Engineering interview preparation, timeline, "Vibe Coding" practical round, ML system design | [github.com/YagyanshB/google-fde-interview-guide](https://github.com/YagyanshB/google-fde-interview-guide) |
| **Alexey Grigorev** | AI Engineering Field Guide, analysis of 146 deduplicated FDE listings, empirical responsibilities and interview patterns | [github.com/alexeygrigorev/ai-engineering-field-guide](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md) |

---

## Dataset Schema

The dataset is stored in `fde_interview_questions.json` as an array of objects conforming to the following schema:

```json
{
  "id": "FDE-DISC-001",
  "stage": "Discovery & Decomposition",
  "question": "Full verbatim question text",
  "tested_at": ["Company A", "Company B"],
  "core_signal": "Underlying engineering capability or behavioral instinct being evaluated",
  "senior_response_playbook": "Verbatim senior practitioner response strategy",
  "red_flag_response": "Specific flawed response or mindset that triggers candidate rejection",
  "scoring_rubric": {
    "strong_hire": "Criteria for top-tier evaluation",
    "hire": "Criteria for competent pass",
    "no_hire": "Criteria for rejection"
  },
  "primary_source": {
    "author": "Practitioner Author Name",
    "title": "Document or Guide Title",
    "url": "Direct clickable URL reference",
    "verified_date": "YYYY-MM-DD"
  }
}
```

---

## Interview Stages Covered

1. **Discovery & Decomposition**: Decomposing vague mandates ("make reporting smarter", "reduce ER wait times") into scoped v1 vertical slices.
2. **Coding & Practical Integration**: Rapid prototyping on dirty data, idempotent API endpoints, streaming SSE, and structured schema error loops ("Vibe Coding").
3. **System Design & Architecture**: Enterprise compliance boundaries, AWS PrivateLink / Azure Private Link, customer-managed KMS keys, and multi-tenant scaling.
4. **LLM & Applied AI Engineering**: Prompt vs. RAG vs. Fine-tuning decision trees, context budgeting, and AI agent least-privilege tool design.
5. **Live Debugging**: Bisection methodology (retrieval vs. generation), time-patterned anomalies, and silent schema drift triage.
6. **Customer Simulation & Role-play**: De-escalating furious executive stakeholders, handling delayed deliverables, and disagreeing and committing with dignity.
7. **Behavioral & Ownership**: End-to-end operational ownership, postmortem discipline, and permanent regression prevention.

---

## Automated Validation

To verify the integrity of the dataset, run the validation script:

```bash
python interviews/dataset/validate_dataset.py
```

The script ensures:
- All required schema fields are present and non-empty.
- Question IDs are unique and follow the `FDE-<STAGE>-<NUM>` convention.
- Scoring rubrics contain explicit `strong_hire`, `hire`, and `no_hire` guidelines.
- Source URLs are syntactically valid and direct citations are intact.
