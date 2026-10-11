# Beginner to FDE

Start here if you are learning to program or have not yet delivered software for other people. Forward deployed engineering combines building software with understanding a customer's workflow, constraints, and operating needs. Begin with a small working system and expand the responsibility you can demonstrate.

Beginner learning sequence reviewed 2026-10-11. The recommendations below are practice gates, not employer requirements or a hiring timeline.

## Your first ten minutes

Open [Lesson 0: setup and first run](foundations/00-setup-and-first-run.md). Run the supplied Python command against the retained real complaint metadata. You do not need a model API key, a cloud account, a vector database, or paid tools for this first exercise.

Continue through the [six foundations lessons](foundations/README.md). They use one project so you can see how each new concept changes a system you already understand. Look up unfamiliar terms in the [glossary](foundations/glossary.md).

| Step | What you practice | Evidence to keep before advancing |
|---|---|---|
| 0. Setup | Terminal, working directory, Python environment, Git | Successful first run and a note explaining the command |
| 1. Python and JSON | Lists, dictionaries, functions, loops, source dates | Your own product-count function and a five-record data note |
| 2. SQL | Tables, keys, parameters, transactions, replay | First import, safe second import, and an explanation of conflict rollback |
| 3. HTTP | Request bodies, schemas, status codes, replay keys | A successful request plus reproduced 409 and 422 failures |
| 4. Retrieval and AI | Evidence selection, role filtering, generation choices | Two search responses and a design note explaining when a model helps |
| 5. Evaluation and handover | Assertions, regression limits, debugging, operator instructions | A test of your own code, a corrected defect, and a peer walkthrough |

The complaint input is actual categorical metadata received and captured on 2026-10-09. The official API query for 2026-10-11 returned zero records at capture time. Retain both dates; the sample has no narratives or independently judged routing labels. API tickets and deliberately invalid inputs in the lessons are authored test cases. See the [dated source checks](../research/source_checks_2026-10-11.json).

## Build the engineering foundations

After the guided lessons, write a small service yourself rather than presenting the reference implementation as your work. You should be able to:

- Write and test a function without copying its answer from the reference.
- Read JSON, reject invalid input, and account for every accepted or rejected record.
- Query joined tables, explain a primary key, and recover from a failed transaction.
- Send and debug an HTTP request, including timeout and retry behavior.
- Review a Git diff and keep credentials and local artifacts out of commits.
- Explain a failed test and demonstrate that your repair changes its result.

Use the [coding exercises](../interviews/code/) when you need more practice with parsing, retries, chunking, or ingestion. The reference project's passing tests demonstrate its behavior; tests for your independent implementation must exercise your implementation.

## Add customer responsibility from the beginning

Choose a process you can observe with permission: for example, how a support team checks a ticket before routing it. Ask who uses the result, how work happens now, what errors cost, and who owns recovery. Use the [customer brief worksheet](foundations/customer-brief-template.md). Mark unconfirmed requirements as assumptions. A role-play is practice, not customer acceptance.

Keep the first deliverable small: an import, a searchable record, or a draft for human review. A deterministic script may solve the problem. Add retrieval or generation only when its benefit and failure test are clear. Never upload private customer data to a provider without approved use.

Then study [requirements to specification](../customer/02-requirements-to-spec.md), [APIs and integrations](../engineering/02-apis-and-integrations.md), and [evaluation](../ai/03-evaluation-and-testing.md). For each feature, retain the decision, the input lineage, a failure case, and instructions someone else can follow.

## Progress toward real delivery

The [90-day roadmap](90-day-fde-roadmap.md) and [24-week roadmap](24-week-enterprise-fde-roadmap.md) are planning options after the fundamentals. Adjust their pace to your demonstrated skills and available time. Completing a calendar does not establish production experience.

Look for opportunities to own work with review and supervision: a support automation, an implementation integration, a junior software role, an internship, or an internal operations tool. Titles and entry requirements differ by employer. Use the [dated market methodology](../job-market/dataset/README.md) and current individual vacancies rather than treating an old title sample as a rule that junior work never exists.

When you already ship software, use the [software-engineer route](from-software-engineer.md). When you can demonstrate reliable delivery, the [expert practicum](expert-fde-practicum.md) adds independent evaluation, authenticated authority, durable recovery, cost accounting, and operator acceptance.

## Readiness check

- [ ] Another person can run your project from its README.
- [ ] Your report distinguishes observed data, authored tests, assumptions, and recommendations.
- [ ] You can demonstrate a failure, explain the root cause, and verify recovery.
- [ ] You can identify what the system cannot safely do and who handles exceptions.
- [ ] You describe practice honestly and retain evidence for any real delivery claim.

## Related documents

- [Learning paths](README.md) - choose a route for your current background
- [Foundations](foundations/README.md) - the working beginner sequence
- [Portfolio evidence](../portfolio/README.md) - present work and its limitations

## Further reading

- [Pinned AI Engineering From Scratch](https://github.com/rohitg00/ai-engineering-from-scratch/tree/1c8e62b526e78b8773559594aab3a3487d9998ac) - inspiration for shared foundations followed by specialist practice; inspected 2026-10-11
