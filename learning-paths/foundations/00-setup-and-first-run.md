# Lesson 0: set up and run your first command

[Beginner path](../beginner-to-fde.md). Prerequisites: none beyond a computer, a terminal, Git, and Python 3.12. Reviewed 2026-10-11. Linux and Python 3.12 are the verified environment; on Windows use WSL, and on macOS use the equivalent Python commands after installing the same interpreter version.

You will locate the repository, create an isolated Python environment, and read a real metadata sample without API keys, a GPU, Docker, or paid services. Keep a note containing the working directory and Python version.

## Get the repository

If you already have the cloud checkout, use it. Otherwise clone the guide; use your own fork if you plan to publish your practice work:

```bash
git clone https://github.com/AdilShamim8/FDE-Field-Guide.git
cd FDE-Field-Guide
```

All lesson commands start in this root folder. In a prepared cloud checkout, use `cd /workspace/FDE-Field-Guide` instead of cloning again.

```bash
pwd
git status --short
python3 --version
python3 -m venv .venv
mkdir -p learning-artifacts
.venv/bin/python --version
.venv/bin/python learning-paths/foundations/code/complaint_pipeline.py
```

`pwd` prints your folder. `git status` shows local changes. `venv` creates an isolated package environment; `.venv/bin/python` explicitly chooses it. `learning-artifacts` is an ignored folder for your scripts, database, and notes. The first data command uses the standard library and requires no package installation.

Expected: the JSON report has `records_read: 5`, `received_date_utc: 2026-10-09`, and one product group with count 5. This is a retained historical sample reviewed today, not a fresh worldwide dataset. No database is created without `--db`.

## Try it yourself

Run `git diff` and explain why reading data has not changed source files. In your editor, create `learning-artifacts/first_run.py` with `print("I can run a Python script")`, then run it with `.venv/bin/python learning-artifacts/first_run.py`. Keep your note and output locally.

When you publish your own original lesson work, review the diff and select individual files rather than blindly staging all generated outputs. Never place credential values in scripts, source history, or a public question.

## Debugging check

- `python3` not found: install the stated interpreter before continuing.
- `ensurepip` unavailable: install your distribution's Python venv support, then retry environment creation. Keep package/TLS verification enabled.
- Can't open the script: confirm you are in the repository root and copied the relative path exactly.
- A report has a different source date: inspect its metadata; don't change the date to match today's clock.

Package installation is introduced in Lesson 3 when the API needs it. The data exercises do not require the rest of the reference stack.

## Exit check

- [ ] You can explain the terminal, working directory, file path, and virtual environment.
- [ ] The real-data summary runs and you can name its observation date.
- [ ] You can run your own scratch script and identify its location.

Next: [Lesson 1 - Python and real data](01-python-and-real-data.md).

## Related documents

- [Glossary](glossary.md) - vocabulary you will meet next
- [Reference setup](../../portfolio/reference-project/README.md) - the later API environment and its boundaries
- [Evidence discipline](../../STYLING.md) - dates, source status, and honest claims

## Further reading

- [Versioned venv documentation source](https://github.com/python/cpython/blob/2abcf904b8dac8c999d2b3aac76681abb333798a/Doc/library/venv.rst) - environment isolation
- [Pinned Pro Git chapter](https://github.com/progit/progit2/blob/a013e3230a1207cfa5ae94d28ba7d2021063c337/book/02-git-basics/sections/recording-changes.asc) - inspect, stage, and record selected changes
