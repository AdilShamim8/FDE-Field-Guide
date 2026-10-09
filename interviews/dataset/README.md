# Curated interview practice dataset

Reviewed 2026-10-09. [fde_interview_questions.json](fde_interview_questions.json) contains 17 authored practice records with stages, suggested responses, red flags, and proposed rubrics. Published practitioner references informed the collection. Event-level transcripts, participant permission, source quotations, and company-approved rubrics are absent.

## Evidence status

Each record is `curated_practice_company_attribution_unverified`. Preserve the historical `tested_at` and `verified_date` declarations for traceability; neither establishes that the named company asked that exact question. Suggested responses are synthesized preparation material, not verbatim testimony. The new `audited_on` date records this status review, not a new interview collection.

The dataset cites Om Bharatiya, Nehal Vyas, Dr. Sundeep Teki, Dr. Sanjay Kumar PhD, YagyanshB, Startup.jobs, and Alexey Grigorev. These declared author names and links require source-specific review. An allowlisted author or domain is not provenance authentication.

## Validation

```bash
python interviews/dataset/validate_dataset.py
python interviews/dataset/ten_pass_verification.py
```

Run from the repository root. These checks cover fields, unique IDs, stage taxonomy, declared names, response lengths, and document cross-references. They do not fetch sources or establish company usage, predictive validity, or hiring outcomes.

## Admission of future observed interviews

Keep practice and observed records separate. An observed record needs an event date, source artifact, permission and redistribution basis, quotation boundaries, transformation history, and a reviewer. Remove company attribution when those artifacts are unavailable; never promote a practice rubric into a claimed hiring policy.

## Related documents

- [Question bank](../07-question-bank.md) - preparation examples
- [Audit](../../AUDIT.md) - evidence limitations
- [Evidence discipline](../../STYLING.md) - contribution contract

## Further reading

- [Nehal Vyas interview guide](https://fde.hinehal.com/blogs/fde-interview-questions) - practitioner preparation guidance
- [AI Engineering Field Guide](https://github.com/alexeygrigorev/ai-engineering-field-guide) - source-based research approach
