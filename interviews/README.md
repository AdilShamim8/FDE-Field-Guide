# Interview preparation

Practice engineering decisions, customer discovery, and clear explanations of work you can defend. Reviewed 2026-10-09. This collection contains authored practice questions and rubrics informed by published guides; it is not a set of authenticated company interview transcripts. Previously asserted hiring conversion rates had no traceable measurement and are withdrawn.

## Reading order

1. [Interview process](01-interview-process.md) - preparation framework; confirm the actual loop with your recruiter
2. [Coding and technical rounds](02-coding-and-technical.md) - constrained engineering exercises
3. [System design](03-system-design.md) - architecture and trade-off discussion
4. [Customer scenarios](04-customer-scenarios.md) - authored role-play scripts
5. [Behavioral rounds](05-behavioral.md) - practice story structures; use your own events and measurements
6. [Take-homes](06-take-homes.md) - proposed deliverables and acceptance checks
7. [Question bank](07-question-bank.md) - synthesized prompts and suggested responses
8. [Coding solutions](08-coding-solutions.md) - runnable exercises and their limits

## Dataset and checks

The [question dataset](dataset/fde_interview_questions.json) contains 17 curated practice records. Its historical `tested_at` lists are unverified company attributions, and `verified_date` is a legacy declaration, not an event record. Read the [dataset status](dataset/README.md) before reusing it as research.

From the repository root, with the reference dependencies installed:

```bash
.venv/bin/python -m pytest interviews/code -q
.venv/bin/python interviews/dataset/validate_dataset.py
.venv/bin/python interviews/dataset/ten_pass_verification.py
```

The JSON checks validate structure, declarations, and cross-references. They do not verify that a company asked a question or approved a rubric. Unit tests validate the exercised code paths, not production deployment readiness.

## Related documents

- [Expert practicum](../learning-paths/expert-practicum.md) - build evidence you can defend
- [Reference project](../portfolio/reference-project/README.md) - bounded implementation and executable checks
- [Evidence discipline](../STYLING.md) - source and claim requirements

## Further reading

- [Nehal Vyas](https://fde.hinehal.com/blogs/fde-interview-questions) - published preparation guidance
- [Sundeep Teki](https://www.sundeepteki.org/advice/the-definitive-guide-to-forward-deployed-engineer-interviews-in-2026) - practitioner guide; not a company scoring policy
