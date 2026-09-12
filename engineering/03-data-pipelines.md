# Data Pipelines in Customer Environments

This is for engineers whose engagement depends on customer data flowing, which is most engagements. It covers the first data milestone, ingestion patterns, quality triage, minimization, transform design, and the failure modes that show up on every project. In most deployments the majority of engineering time goes to moving and cleaning data rather than to the model or the interface - this is interpretation, but it matches the evidence. Paul Farnsworth, president of Dice, told Fortune (September 2026) that companies struggle to turn models into something that works inside the business because connecting them to "proprietary data, existent systems and specific workflows" is a big roadblock, and that forward-deployed engineers "can help fill that gap."

## Getting data in

### The first data milestone

The first real milestone is read access to sample data. Not a schema PDF, not an architecture slide - actual rows. Until someone has run a query against production-shaped data, the engagement is running on imagination. Ask for a representative sample, not a convenient one: the last 30 days rather than "some test rows", and all the columns rather than a curated view. The convenient extract hides exactly the defects you need to see.

Build the data inventory as a formal document while access is being granted:

- Source system - name, environment, and whether it is system of record or a replica
- Owner - the person who can answer questions and approve access
- Volume - rows per day, total size, and growth rate
- PII flags - which fields are personal, sensitive, or regulated
- Refresh cadence - real-time, daily, weekly, or never
- Access path - direct database read, export drop, API, or manual request

The inventory matters because it becomes the shared reference for scope, the security review, and pipeline design. Verbal inventories rot; when someone asks in week 8 whether you are using the HR system, the document answers.

### Ingestion patterns

- Batch exports - CSV or parquet drops into shared storage. Use when latency needs are low, customer ops maturity is limited, or the source system cannot be queried directly. Simple and debuggable; stale by definition.
- API pulls - scheduled pulls from the customer's or a vendor's APIs. Use when volumes are modest, records are individually addressable, and warehouse access is unavailable. Watch rate limits and pagination; see [APIs and integrations](02-apis-and-integrations.md).
- Change data capture - read the source database's change log so inserts, updates, and deletes arrive continuously. Use when freshness matters and the source team can enable it. Heavier setup, and it needs source DBA cooperation.
- Event streams - consume from the customer's event bus when events already flow or several downstream consumers exist. Efficient, but you inherit their stream ops.

Four decision factors, in the order that usually decides it: who owns the source system, what latency the use case actually needs, what volume it runs at, and what infrastructure the customer is willing to operate. The first factor decides most cases - you build around what the source owner is willing to support.

## Making it usable

### Data quality triage

Profile before you build. Null counts, cardinality, min and max ranges, and value distributions per column - a few `pandas` or SQL summaries take an hour and save weeks. Agree with the customer what "good enough" means per pipeline: row counts within a tolerance, freshness within a window, no orphaned foreign keys. Written thresholds turn data quality from a feeling into a check. The defects you will find, in rough order of frequency:

- Nulls with meaning - the null in `discount_code` means "no discount", not "unknown". Nulls are overloaded; ask what each one means before you impute.
- Duplicate identities - the same customer exists three times with different IDs because two source systems each minted their own. Deduplication rules are a business decision, not a technical one.
- Encodings - latin-1 remnants, byte-order marks, and trailing whitespace that make `"gold "` and `"gold"` different join keys.
- Schema drift - columns added, renamed, or retyped upstream with no notice; numeric fields widened to strings.
- Semantic mismatches - a `closed` flag that means "case closed" in the ticketing system and "account closed" in the CRM. Same column name, different facts.
- Timezone bugs - timestamps without offsets, mixed UTC and local times, daylight-saving seams in historical ranges. Store UTC, convert at display, and verify which one the source actually means.
- The deprecated-but-load-bearing column - "that column is deprecated, do not use it" - except everything still uses it and the replacement is half-populated. Plan around reality, not the data dictionary.

### Data minimization

Fields you do not need are liabilities. Every unnecessary PII field expands the security review, the compliance scope, and the blast radius of an incident. We recommend scoping PII with the customer's security team in week 1: list the fields the use case actually requires, get the list approved, and exclude everything else at ingestion. "We will filter it later" is not a plan, because later never comes and the data has already landed.

For development and testing, use synthetic or tokenized data so engineers never have production personal data on local machines. The data boundary questions this raises are covered in [security and compliance](05-security-and-compliance.md).

### Transform layers

- ELT inside their warehouse versus transforms outside - transforms running inside the customer warehouse use their compute, their access controls, and their monitoring, and stay visible to their analysts. Transforms in your own runtime give you version control, tests, and library access, at the cost of copying data out - exactly what their security team scrutinizes. Engagements commonly end up hybrid: heavy SQL in the warehouse, glue logic outside.
- SQL versus Python jobs - SQL for set-based transforms close to the data; Python when the logic needs parsing, model inference, or API calls that SQL does not express well.
- Idempotent, re-runnable jobs - every job must be safe to run twice and produce the same result. Design for "rerun yesterday's load" as a normal operation, because it will become one.
- Watermarks and incremental loads - track a high-water mark (maximum timestamp or ID processed) per source so each run picks up only new or changed rows. Store the watermark transactionally with the output so a partial run cannot lose or double-count data.

### Vector prep for RAG

If the engagement includes retrieval-augmented generation, the pipeline grows a vector branch: chunking documents (chunk size and overlap are tuning choices with real quality effects), running embedding models as batch jobs over the corpus, and keeping the index fresh as sources change. Treat embeddings as a pipeline artifact with its own incremental-update problem: re-embed changed chunks only, and be explicit about the freshness guarantee, because stale data does not sit quietly - it reappears as confident wrong answers. Put the freshness guarantee in writing; "the index is current" is a claim someone will eventually test. The application-side patterns live in [LLM application patterns](../ai/01-llm-application-patterns.md).

## Operating the pipeline

### Failure modes

- Silent upstream schema change - a column renamed or retyped with no notice; ingestion breaks, or worse, keeps "succeeding" while loading nulls. Prevention: schema validation at ingestion with alerts on drift, plus scheduled checks against the live source schema.
- Duplicate ingestion - the same batch loaded twice inflates counts and metrics, and nobody notices until the numbers look suspiciously good. Prevention: idempotent loads keyed on batch or event ID, and monitoring of row-count deltas per run for sudden jumps.
- Success that means "ran", not "landed" - the job exited 0 and the data never arrived. Prevention: post-load checks on row counts, freshness (maximum source timestamp), and spot-checkable invariants, not just process exit codes.
- Stale-dimension joins - fact rows joined against dimension data that has since changed, silently attributing events to the wrong segment. Prevention: snapshot dimensions as of event time or version them, and test joins against known examples.

## Related documents

- [APIs and integrations](02-apis-and-integrations.md) - API pulls, rate limits, and schema validation at boundaries
- [Security and compliance](05-security-and-compliance.md) - PII scoping, data boundaries, and the review your pipeline design must pass
- [LLM application patterns](../ai/01-llm-application-patterns.md) - what the pipeline feeds: RAG, retrieval, and context construction
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - data quality problems surface as evaluation failures; trace them back to the source
- [Working in customer environments](../customer/03-working-in-customer-environments.md) - getting access and cooperation inside someone else's organization

## Further reading

- [PostgreSQL documentation](https://postgresql.org) - the warehouse engine many customer estates already run
- [pgvector](https://github.com/pgvector/pgvector) - vector storage inside the customer's existing Postgres
- [Independent FDE job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md) - posting data on how dominant integration work is
