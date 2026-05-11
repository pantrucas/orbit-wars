# PROJECT_MEMORY.md — Orbit Wars Project Memory

Shared persistent memory for human contributors, Claude Code, Codex, and other development agents.
Update whenever project direction, datasets, models, experiments, submissions, or compliance status changes.

---

## 1. Competition Summary

- **Name:** Orbit Wars
- **Platform:** Kaggle
- **URL:** https://www.kaggle.com/competitions/orbit-wars
- **Type:** Simulation / game agent / bot programming
- **Objective:** Build an agent that plays Orbit Wars episodes competitively against other agents.
- **Evaluation:** Ladder-style simulation episodes; rating modeled as Gaussian distribution.

## 2. Verified Submission Format

- **Format:** Single `main.py` OR `zip`/`gz`/`7z` archive with `main.py` at top level.
- **Entrypoint:** Last `def` in the file. Must accept observation, return action.
- **No internet** during evaluation. No exfiltration.

---

## 3. Key Rules

| Rule | Understanding | Verified? |
|---|---|---|
| One Kaggle account | Only one account allowed | Yes |
| Team size | Max 5 people | Yes |
| Daily submissions | Max 5/day | Yes |
| Final submissions | Latest 2 used for finals | Yes (verify exact mechanism) |
| Data license | Apache 2.0 | Yes |
| Data redistribution | Do not share outside accepted rules | Yes |
| External data/models | Allowed if accessible and not excessive cost | Yes |
| Private code sharing | Not allowed with other teams | Yes |
| Open-source code | Must allow commercial use | Yes |
| Winner docs | Reproducible documentation required | Yes |
| Winner license | CC-BY 4.0, except documented exceptions | Yes |
| Evaluation internet | Forbidden | Yes |
| Replays | May be public | Yes |

---

## 4. Current Objective

```
<FILL: e.g. Build robust baseline agent and local validation harness>
```

Current target: `<FILL>`
Current risk level: `<FILL: Low / Medium / High>`

---

## 5. Project State

| Area | Status | Notes |
|---|---|---|
| Repo structure | Initialized | All dirs and files created |
| Baseline agent | Stub created | See src/orbit_wars/agent.py |
| Local environment | `<FILL>` | |
| Local simulator | `<FILL>` | |
| Packaging | Stub created | See scripts/package_submission.py |
| Kaggle API | `<FILL>` | |
| Tests | Stubs created | See tests/ |
| Compliance docs | Initialized | See COMPLIANCE.md |
| Winning-solution draft | Stub created | See docs/winning_solution_draft.md |

---

## 6. Technical Decisions

| Date | Decision | Reason | Owner | Reversible? |
|---|---|---|---|---|
| 2026-05-10 | Heuristic baseline before RL | Low risk, fast iteration | Human | Yes |
| 2026-05-10 | Last `def` in main.py is agent function | Kaggle submission contract | Verified rule | No |
| 2026-05-10 | Require human confirmation for Kaggle submit | Limit daily submissions, avoid accidents | Safety policy | No |

---

## 7. Datasets Used

| Dataset | Source | License | Access date | Used for | In submission? |
|---|---|---|---|---|---|
| Competition data | Kaggle Orbit Wars | Apache 2.0 | `<FILL>` | Development/evaluation | No |

---

## 8. External Code / Models / Tools Used

| Asset | Type | Source | License | Commercial use? | In final? |
|---|---|---|---|---|---|
| `<FILL>` | `<FILL>` | `<FILL>` | `<FILL>` | `<FILL>` | `<FILL>` |

---

## 9. Experiments Performed

| Experiment ID | Date | Branch | Commit | Config | Seeds | Local result | Kaggle result | Conclusion |
|---|---|---|---|---|---|---|---|---|
| EXP001 | `<FILL>` | `<FILL>` | `<FILL>` | baseline.yaml | `<FILL>` | `<FILL>` | `<FILL>` | `<FILL>` |

---

## 10. Best Kaggle Submissions

| Rank | Date | Submission ID | File | Commit | Rating/Score | Notes |
|---|---|---|---|---|---|---|
| 1 | `<FILL>` | `<FILL>` | `<FILL>` | `<FILL>` | `<FILL>` | `<FILL>` |

Full history: `SUBMISSION_LOG.md`

---

## 11. Known Risks

| Risk | Severity | Status | Mitigation |
|---|---|---|---|
| Exceeding 5 submissions/day | High | Controlled | check_submission_limit.py + human confirmation |
| Network/exfiltration in submitted code | High | Controlled | Static scan + test_no_network.py |
| Overfitting to public ladder | Medium | Open | Local tournament + prior agent opponents |
| External asset license incompatibility | Medium | Open | Track in COMPLIANCE.md |
| Winning-solution reproducibility gap | Medium | Open | Maintain docs continuously |

---

## 12. Pending Tasks

| Priority | Task | Owner | Status |
|---|---|---|---|
| P0 | Verify local environment setup | Human | Open |
| P0 | Download competition data | Human | Open |
| P1 | Implement observation parser | Agent | Open |
| P1 | Set up local tournament | Agent | Open |
| P1 | Create first safe submission package | Agent | Open |
| P2 | Draft winning solution docs | Agent | Open |
