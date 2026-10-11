# Vocabulary for the first project

Use this page when a new term interrupts your lesson. Reviewed 2026-10-11. Definitions describe the concepts; the reference project only implements the boundaries stated in its README.

| Term | Plain meaning | Example in this guide |
|---|---|---|
| FDE | An engineer working with customers to discover, build, evaluate, and hand over a useful system | Explain an integration and its failure behavior to its operator |
| Terminal | A program where you enter commands | Run Python or inspect Git status |
| Working directory | The folder relative file paths start from | Run lesson commands from the repository root |
| Virtual environment | An isolated set of Python packages | `.venv/bin/python` uses the project's packages |
| Dependency | A package your code needs | FastAPI for the reference API; the data exercise uses the standard library |
| JSON | A text format for objects, lists, numbers, and other values | The preserved CFPB metadata file |
| Schema | A contract for which fields and values are allowed | A ticket must have a nonblank ID |
| API | An interface another program can call | Submit a ticket through an HTTP endpoint |
| HTTP request/response | The message sent to a service and the message returned | `POST` a JSON body; receive a status and JSON result |
| Validation | Checking whether input satisfies its contract | Reject a missing field with HTTP 422 |
| Authentication | Establishing who the caller is | Missing from the local role-header simulation |
| Authorization | Deciding what an authenticated caller may do | Required before real customer review actions |
| SQL | A language for querying structured data | Count complaints grouped by product |
| Primary key | The identifier a table keeps unique | `complaint_id` in the local SQLite exercise |
| Transaction | A group of database changes committed or rolled back together | A conflict rolls back earlier inserts from that import |
| Idempotency | Repeating the same operation avoids an additional intended effect | Import the same record IDs twice without doubling the rows |
| Provenance/lineage | The record of where data came from and how it changed | Source URL, date, response digest, and field projection |
| Hash/digest | A content fingerprint | Compare the SHA-256 of two files; a hash alone does not authenticate their author |
| LLM | A model that generates tokens from context | The local ETISE reference does not call one |
| Token | A unit a model tokenizer processes | Regex word chunks are not a model-token count |
| Embedding | A numeric representation used for comparison | ETISE uses feature hashing, not a learned embedding model |
| Retrieval | Selecting material relevant to a request | Search the permitted sample-policy chunks |
| RAG | Retrieve material and put it in a model's context before generation | A later extension needs a real generator; retrieval alone is not full RAG |
| Evaluation | Compare behavior with a declared acceptance rule | Check routing, required policies, and exact quotes |
| Regression fixture | A known example used to catch changed behavior | ETISE's 25 legacy examples have unverified origins |
| Holdout | Cases kept untouched while developing the system | A representative customer holdout remains missing |
| Handover/runbook | Instructions and ownership for operating the system | Start it, reproduce a failure, recover, and name the next owner |

## Related documents

- [Beginner path](../beginner-to-fde.md) - learning order
- [Reference boundaries](../../portfolio/reference-project/README.md) - implemented behavior and missing controls
- [Evidence discipline](../../STYLING.md) - source and claim requirements

## Further reading

- [Python tutorial](https://docs.python.org/3.12/tutorial/) - language concepts; selected versioned source chapters were inspected for this review
