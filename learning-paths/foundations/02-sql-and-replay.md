# Lesson 2: store records and repeat the import safely

[Beginner path](../beginner-to-fde.md). Prerequisites: read the real JSON sample and count its products. Reviewed 2026-10-11.

You will put the records in a small database, query them with SQL, and rerun the import without doubling the rows. Keep your query and the two import results. The database is local practice data, not an authoritative complaint-resolution system.

## Learn the storage rule

A table stores rows with named columns. A primary key keeps an identifier unique. A transaction groups changes so they can commit together or roll back after a conflict. SQL placeholders pass values as data rather than inserting them into the SQL text.

The [worked pipeline](code/complaint_pipeline.py) retains complaint ID, receipt timestamp, product, and issue, plus the source response digest. Other source fields are excluded from its database projection. Repeating the same selected facts replays safely; changing selected facts for an existing ID raises a conflict. It preserves the first capture digest rather than silently changing lineage.

## Work through the reference

From the repository root, choose a new database filename if the example already exists:

```bash
.venv/bin/python learning-paths/foundations/code/complaint_pipeline.py --db learning-artifacts/complaints.sqlite
.venv/bin/python learning-paths/foundations/code/complaint_pipeline.py --db learning-artifacts/complaints.sqlite
```

Expected on a fresh database: the JSON report's `database` object has `inserted: 5`, `replayed: 0`, and `total_stored: 5`. On the second run, that object has `inserted: 0`, `replayed: 5`, and `total_stored: 5`. If you reuse an existing database, state that instead of claiming a fresh import.

Inspect the rows with Python's built-in SQLite library; no database server is required:

```bash
.venv/bin/python - <<'PY'
import sqlite3
from contextlib import closing
with closing(sqlite3.connect("learning-artifacts/complaints.sqlite")) as connection:
    for row in connection.execute("SELECT product, COUNT(*) FROM complaints GROUP BY product"):
        print(row)
    complaint_id = "29496093"
    row = connection.execute(
        "SELECT complaint_id, issue FROM complaints WHERE complaint_id = ?",
        (complaint_id,),
    ).fetchone()
    print(row)
PY
```

Expected: one product group with count 5, and the selected ID with its source issue text. These are selected records, not a count of all complaints or a finding about company behavior.

## Try it yourself

Write a query that returns all five IDs in receipt-time order. Explain the difference between `COUNT(*)`, `COUNT(DISTINCT complaint_id)`, and grouping by product. Then read the transaction in `store_snapshot`: find what happens when an existing row changes after an earlier new row was inserted.

In your brief, state the behavior of a changed official record. This teaching importer raises a conflict instead of merging it. A real update pipeline needs an explicit revision/history policy; do not delete records just to make the conflict disappear.

## Debugging check

If the second run inserts five again, confirm both commands use the same database path. If SQL fails near an apostrophe, use placeholders instead of concatenating values into the statement. If the summary has more than five stored rows, check what previous imports are already in the file before interpreting the count.

The project's [tests](code/test_complaint_pipeline.py) include an authored change that inserts a new row before a conflict. The transaction must roll back that new row. Those mutated inputs test a contract and do not create real observations.

## Exit check

- [ ] You can explain why the second import inserts zero rows.
- [ ] You can write a parameterized query and interpret its count.
- [ ] You can explain rollback and the limits of the four-field projection.

Next: [Lesson 3 - HTTP and validation](03-http-and-validation.md).

## Related documents

- [Data pipelines](../../engineering/03-data-pipelines.md) - later ingestion and drift concepts
- [Customer brief worksheet](customer-brief-template.md) - preserve the source and operating assumptions
- [Glossary](glossary.md) - SQL, primary key, transaction, and lineage

## Further reading

- [Versioned SQLite documentation source](https://github.com/python/cpython/blob/2abcf904b8dac8c999d2b3aac76681abb333798a/Doc/library/sqlite3.rst) - placeholders, connections, and transaction behavior
