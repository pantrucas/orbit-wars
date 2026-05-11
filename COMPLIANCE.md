# COMPLIANCE.md — Orbit Wars Compliance Matrix

Status values: Green (compliant), Yellow (needs review), Red (blocked), Unknown (must verify)

---

## Compliance Matrix

| Rule | Status | Evidence | Owner | Last checked | Notes |
|---|---|---|---|---|---|
| One Kaggle account only | Green | Account: pantrucas | Human | 2026-05-10 | Solo esta cuenta |
| Team size max 5 | Green | Solo miembro: pantrucas | Human | 2026-05-10 | Equipo de 1 |
| Max 5 submissions/day | Yellow | check_submission_limit.py planned | Agent/Human | 2026-05-10 | Enforce before submit |
| Up to 2 final submissions | Unknown | | Human | | Verify exact final mechanism |
| Data license Apache 2.0 | Green | Kaggle rules | Human | 2026-05-10 | |
| No data redistribution | Yellow | .gitignore excludes data/ | Human/Agent | 2026-05-10 | Verify no public data files |
| External data allowed if accessible | Yellow | Asset table required | Human/Agent | | Review each asset |
| External models allowed if accessible | Yellow | Asset table required | Human/Agent | | Review license/cost |
| LLMs/AutoML allowed if accessible | Yellow | Must log usage | Human/Agent | | |
| No private code sharing | Unknown | | Human | | Human process |
| Open-source code commercial use | Yellow | Asset license table | Agent | | Verify every dependency |
| Winner must document reproducible solution | Yellow | docs/winning_solution_draft.md | Agent | | Keep updated |
| Winner license CC-BY 4.0 | Yellow | License review needed | Human | | Document exceptions |
| No internet during evaluation | Yellow | test_no_network.py planned | Agent | | Static scan required |
| No information sent out during evaluation | Yellow | Static scan required | Agent | | |
| Replays may reveal actions | Green | Strategy not secret-dependent | Human/Agent | 2026-05-10 | |
| Submission format correct | Green | main.py or archive with main.py at top | Agent | 2026-05-10 | Last def = agent function |
| Runtime/dependencies valid | Unknown | | Agent | | Verify Kaggle environment |

---

## External Assets Register

| Asset | Source | License | Commercial use? | Cost/accessibility | In submission? | Status |
|---|---|---|---|---|---|---|
| (none yet) | | | | | | |

---

## Pre-Submission Compliance Gate

Do not submit unless all are true:
- [ ] No Red items.
- [ ] Yellow/Unknown items resolved or explicitly accepted by human.
- [ ] Daily submission count checked.
- [ ] External assets reviewed.
- [ ] Submission package scanned for secrets and network calls.
- [ ] Format verified: main.py or archive with main.py at top; last def is agent function.
- [ ] Human approval recorded in SUBMISSION_LOG.md.
