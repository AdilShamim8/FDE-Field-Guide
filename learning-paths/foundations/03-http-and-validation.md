# Lesson 3: send a request and understand a rejection

[Beginner path](../beginner-to-fde.md). Prerequisites: Python dictionaries, the JSON lesson, and a repeatable local import. Reviewed 2026-10-11.

You will start the reference service, send JSON, and inspect success, validation failure, and replay conflict. Keep one request and your explanation of its response. The authored ticket below tests an API contract; it is not another real CFPB record.

## Learn the contract

An HTTP request has a method, path, headers, and sometimes a body. The service returns a status code and a body. `GET` reads an available resource. Here, `POST` submits a ticket. JSON formatting and a valid domain schema are separate checks.

| Status here | Meaning | What to inspect |
|---|---|---|
| 200 | Request completed successfully | Routing and citations in the body |
| 422 | Input failed validation | The named field and error details |
| 409 | Same replay key, changed content | The caller's key and payload contract |

A 200 response does not mean an AI answer is correct or a customer action happened. ETISE only returns a routing label and draft.

## Work through the reference

From the repository root, install the already-tested Python 3.12 constraints:

```bash
.venv/bin/python -m pip install -r portfolio/reference-project/requirements.txt -c portfolio/reference-project/requirements.lock
.venv/bin/python -m pip check
.venv/bin/python -m uvicorn src.api.server:app --app-dir portfolio/reference-project --host 127.0.0.1 --port 8011
```

The final command stays running. Open a second terminal in the repository root and use the following commands there:

```bash
curl --fail --silent --show-error http://127.0.0.1:8011/health
cat > learning-artifacts/ticket.json <<'JSON'
{
  "ticket_id": "LEARN-BILLING-1",
  "account_id": "LEARN-ACCOUNT",
  "raw_text": "Requesting fee waiver and credit on invoice INV-9901 as per Section 5.4 billing policy.",
  "idempotency_key": "learn-billing-1"
}
JSON
curl --fail --silent --show-error -H 'Content-Type: application/json' --data-binary @learning-artifacts/ticket.json http://127.0.0.1:8011/api/v1/tickets/process
```

Expected: health is `healthy` with an indexed corpus; intake returns `BILLING`, `P2`, `AUTOMATED_DISPATCH`, and a verified `APEX-BILLING-POLICY` quotation. No customer message is sent. Repeat the last command: the same payload/key returns its cached result within the local replay window.

The [schemas](../../portfolio/reference-project/src/models/schemas.py) define bounded IDs, ticket text, enums, and review actions. The [API](../../portfolio/reference-project/src/api/server.py) applies those contracts and local replay behavior.

## Try it yourself

Copy the request into a second local file. Change `raw_text` but keep the same account, role, and key, then send it with `curl -i`: expect 409. Remove `account_id` and send again: expect 422 and a field error. These are deliberate authored failures, not additional observed complaint data.

Then send a new ticket/key with `Need assistance with GDPR data residency compliance under Section 11.3.` as its text. With the default role, expect `HUMAN_REVIEW_REQUIRED` and no compliance citation. The next lesson explains why access to an applicable policy matters.

## Debugging check

- Connection refused: start the server and confirm the port matches. A completed install does not start a service.
- Address already in use: inspect the owner or choose another port and update every request. Stop only a process you started.
- 422: read the response body before editing; a valid JSON document can still fail its field contract.
- Import error: use `.venv/bin/python`, the repository root, and the stated `--app-dir`.

When finished with the API lessons, stop your foreground process with Ctrl-C. In-memory queues, metrics, and replay state are lost. Role headers do not authenticate a caller; this local service is not a production tenant boundary.

## Exit check

- [ ] You can explain method, path, header, body, and status in your own request.
- [ ] You can reproduce 200, 409, and 422 without weakening the input contract.
- [ ] You can describe the state lost on restart and the missing identity control.

Next: [Lesson 4 - retrieval and AI](04-retrieval-and-ai.md).

## Related documents

- [Reference README](../../portfolio/reference-project/README.md) - supported workflow and boundaries
- [Local runbook](../../portfolio/reference-project/docs/SLA_RUNBOOK.md) - available recovery commands
- [Glossary](glossary.md) - HTTP, schema, authentication, and idempotency

## Further reading

- [Pinned FastAPI first steps](https://github.com/fastapi/fastapi/blob/f5c6e9b4f9cadc1bf0f9a1fd672e621206b63007/docs/en/docs/tutorial/first-steps.md) - route and server concepts
- [Pinned FastAPI request-body documentation](https://github.com/fastapi/fastapi/blob/f5c6e9b4f9cadc1bf0f9a1fd672e621206b63007/docs/en/docs/tutorial/body.md) - typed input contracts
