# Lesson 1: read real data with Python

[Beginner path](../beginner-to-fde.md). Prerequisites: use the terminal, repository root, and virtual environment from Lesson 0. Reviewed 2026-10-11.

You will read a JSON file, use lists and dictionaries, write a function, and check what the data actually contains. Keep your own counting script and a short data note. Use the worked pipeline only after trying the small task yourself.

## Understand the input

The [preserved CFPB sample](../../portfolio/reference-project/evals/real_data/cfpb_metadata_2026-10-09.json) contains five actual categorical complaint records received and captured on October 9. Its `metadata` describes acquisition and limits; `records` is a list of dictionaries. It has no narratives, ETISE severity/routing labels, or independently adjudicated company findings.

Today's exact October 11 API query returned zero records at capture time, with no timeout or failed shards. That response is recorded in the [October 11 ledger](../../research/source_checks_2026-10-11.json); it is not a reason to fabricate new examples or relabel the October 9 sample as today-received data.

## Work through the small task

From the repository root, create `learning-artifacts/count_products.py` in your editor with this code:

```python
import json
from pathlib import Path

path = Path("portfolio/reference-project/evals/real_data/cfpb_metadata_2026-10-09.json")
snapshot = json.loads(path.read_text(encoding="utf-8"))
records = snapshot["records"]

def count_products(rows):
    counts = {}
    for row in rows:
        product = row["product"]
        counts[product] = counts.get(product, 0) + 1
    return counts

print(len(records))
print(count_products(records))
assert len(records) == 5
assert sum(count_products(records).values()) == len(records)
```

Run it:

```bash
.venv/bin/python learning-artifacts/count_products.py
```

Expected:

```text
5
{'Credit reporting or other personal consumer reports': 5}
```

`json.loads` turns text into Python values. `snapshot["records"]` selects one value from a dictionary. The function loops through rows and accumulates counts. The assertions compare the result with the actual file; parsing alone does not verify the source's authenticity.

Now compare your work with the validated reference:

```bash
.venv/bin/python learning-paths/foundations/code/complaint_pipeline.py
```

It prints record count, source date, category counts, the captured response digest, and the local snapshot digest. A file digest and a source-response digest refer to different byte sequences. Neither proves that the underlying consumer assertion is true.

## Try it yourself

Print the first record's ID, product, and receipt timestamp. Write a function returning the set of unique complaint IDs. Check that the set has five IDs, and explain why all five records having one category tells you about sample selection rather than worldwide prevalence.

Create `learning-artifacts/data-note.md` with the source, collection date, retrieval date, fields, selection method, and two limitations. Ask which decision an operator could make from these fields. If you have no operator interview, mark the proposed use as an assumption.

## Debugging check

A missing file usually means the wrong working directory or path. A `KeyError` names a missing dictionary key; inspect the schema rather than inventing a default label. A JSON decode error means the text is not valid JSON. Learn to read the final error line and the line in your own script that produced it.

## Exit check

- [ ] You can explain a list, dictionary, loop, function, and assertion in your script.
- [ ] Your script counts the retained records without editing the source dataset.
- [ ] Your data note separates observation, retrieval, and review dates.

Next: [Lesson 2 - SQL and replay](02-sql-and-replay.md).

## Related documents

- [Dataset provenance](../../portfolio/reference-project/evals/DATASET_PROVENANCE.md) - admitted data and excluded claims
- [Customer brief worksheet](customer-brief-template.md) - turn an unknown into a question instead of an invented result
- [Glossary](glossary.md) - JSON, schema, lineage, and holdout

## Further reading

- [Pinned Python control-flow tutorial](https://github.com/python/cpython/blob/2abcf904b8dac8c999d2b3aac76681abb333798a/Doc/tutorial/controlflow.rst) - loops and functions
- [Pinned Python data-structures tutorial](https://github.com/python/cpython/blob/2abcf904b8dac8c999d2b3aac76681abb333798a/Doc/tutorial/datastructures.rst) - lists and dictionaries
