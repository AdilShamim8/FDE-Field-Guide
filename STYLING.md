# Styling Guide

This guide defines how every document in the FDE Field Guide is written. It keeps the
repository consistent, readable, and easy to maintain. Read it before writing or editing
any content file.

## Evidence discipline

Every factual claim falls into one of four tiers. Label it when the tier is not obvious:

1. Observed evidence - a sourced fact with a date, e.g. "median advertised FDE salary
   above $188,000 (Lightcast data, via Fortune, September 2026)". Always link or name the
   source.
2. Industry pattern - a widely reported practice, e.g. "most FDE teams run weekly
   customer-facing demos". Phrase as a pattern, not a law.
3. Expert interpretation - a judgment drawn from evidence, e.g. "this suggests employers
   treat discovery as part of engineering, not pre-sales". Say "this suggests".
4. Recommendation - the guide's own advice. Say "we recommend" or use imperative mood in
   checklists.

Do not invent statistics, salary figures, company names, or quotes. Salary figures always
carry the source and the date because they change fast. Never fabricate URLs: if unsure of
an exact page, link the domain root or drop the link and keep the descriptive text.

## Formatting

DO NOT use:

- Bold formatting (no `**text**`)
- Italic formatting (no `*text*`)
- Horizontal rules (no `---` between sections)
- ALL CAPS for emphasis
- Emoji

DO use:

- Code ticks for filenames, commands, tools, and code-related terms: `docker compose up`,
  `requirements.md`, `pgvector`
- Plain declarative sentences for emphasis
- Blank lines before and after lists

## Headings

H1 (`#`) appears exactly once, at the top of each document, as the title.

H2 (`##`) marks main sections.

H3 (`###`) marks subsections when it makes logical sense.

Do not skip levels and do not use headings as decorative separators.

## Lists

Use lists for genuinely list-shaped content. For simple items:

- Item one
- Item two

For numbered sequences (order matters):

1. First step
2. Second step
3. Third step

For items with descriptions, use the dash format:

- Item one - description here
- Item two - description here

Nest sub-items with two spaces. Prefer lists over tables for anything that would need more
than four columns or more than ten rows.

## Tables

Use tables sparingly, only when rows genuinely benefit from tabular comparison:

- Small comparison tables, 2-4 columns, 10 or fewer rows
- Data with aligned numeric values

Everything else goes in lists. A table that needs a legend to be readable is too big.

## Links

Use descriptive link text, never bare URLs or "click here":

- [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) - full responsibilities and requirements

For multiple links, use a list, one resource per line with a short description:

- [Wikipedia: Forward deployed engineer](https://en.wikipedia.org/wiki/Forward_deployed_engineer) - neutral definition and role history
- [The New Stack on FDE teams](https://thenewstack.io/forward-deployed-engineers-ai) - why AI labs hire FDEs

Cross-link related documents inside the guide with relative paths:

- See [discovery and requirements](skills/02-discovery-and-requirements.md) for the full interview framework.

Every content file ends with two short sections: "Related documents" (3-6 internal links
with a reason for each) and "Further reading" (0-5 external links, only if they add value).

## Numbers

Use percentages with one decimal place when they come from data: 91.0%, 3.6%. Use raw
counts with percentages for context: "133 postings (91.0%)". Keep units attached to
numbers: $280,000, 25% travel, 4+ years.

## Tone

Direct, concrete, engineering-first. Short sentences win. No motivational filler, no
"as we all know", no restating the obvious. Write to a practicing engineer who is busy.

First person plural ("we") for recommendations, first person singular only in quoted
practitioner voices. Avoid bureaucratic phrasing ("utilize", "leverage" as a verb,
"in order to" when "to" works).

## Structure conventions

- Numbered files (`01-`, `02-`) mark a recommended reading order inside a section;
  unnumbered files stand alone.
- Every content file opens with 2-4 sentences that answer: who this is for and what you
  will get out of it. No "Introduction to the introduction".
- Scenarios are written in a fixed format: Situation, Constraints, What good looks like,
  Move-by-move walkthrough, Failure modes. This makes scenarios comparable and reusable.
- Checklists use `- [ ]` syntax so they work as GitHub task lists.

## Maintenance rules

- One idea per document. If two documents repeat each other, merge them and link instead.
- Prefer updating an existing document over creating a near-duplicate.
- Every claim that will go stale (salaries, headcounts, model names, market share) gets a
  date attached at write time.
