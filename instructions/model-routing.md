# Match Effort to Task Complexity and Risk

**Triggers:** deciding how much verification, double-checking, or up-front analysis a piece of work warrants before you act on it.

Not every task deserves the same depth of scrutiny. Spending heavy verification effort on a trivial, reversible change wastes time; spending too little on a judgment-heavy, high-blast-radius one is how mistakes ship. Calibrate deliberately instead of applying one fixed level of care to everything.

## Higher effort — verify more before acting

- Architecture/security-sensitive decisions, anything hard to reverse (schema changes, destructive operations, production pushes).
- Work where a wrong answer is expensive to discover later (a subtle logic bug in a financial calculation, a race condition, a security boundary).
- Anything the user has flagged as high-stakes, or that touches code you don't have strong context on yet.

For these: read more surrounding context before editing, check your own reasoning against edge cases, verify assumptions against the actual code/data rather than trusting memory, and consider a second look (your own re-read, or an explicit review pass) before calling it done.

## Lower effort — move quickly

- Mechanical, low-risk work: formatting, renames, boilerplate, a change whose correctness is obvious on inspection.
- Exploration/research where the cost of being slightly wrong is just re-checking, not a shipped defect.
- Anything easily reversible with a fast feedback loop (a local script, a draft, a throwaway experiment).

For these: don't over-verify. Extra ceremony on trivial work is itself a cost — it slows down everything else and doesn't make the trivial thing more correct.

## When unsure which bucket

Err toward the higher-effort side for anything hard to reverse, and toward moving quickly for anything cheap to redo.

## Why

There's no formula that outputs a number here — the actual skill is noticing which bucket a task falls into *before* you start, not partway through when you've already over- or under-invested.
