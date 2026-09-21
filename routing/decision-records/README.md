# Routing Decision Records

Record **significant delegated** executor choices only. Do **not** create records
for trivial/simple SELF work or routine self-handled tasks.

## When required

- External executor chosen for bounded/complex/critical work
- Fallback switched executor mid-task
- Cold-start / evidence-insufficient path taken with Owner-configured exception
- Recursive delegation (if ever Owner-permitted)

## Location

`routing/decision-records/<YYYYMMDD>-<short-slug>.md` using `TEMPLATE.md`.

Keep records compact. Cite registry evidence or mark uncertainty; never invent scores.
