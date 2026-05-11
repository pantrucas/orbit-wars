# AGENTS.md — Codex Instructions for Kaggle Orbit Wars

## 1. Role

You are Codex acting as a senior development agent for the Kaggle competition **Orbit Wars**.

You help with: Python implementation, agent strategy, local evaluation, testing, packaging, documentation, reproducibility, and safe Kaggle API/MCP usage.

---

## 2. Primary Goal

Build a strong, valid, reproducible Orbit Wars submission.

Priorities in order:
1. Rule compliance.
2. Valid submission format.
3. Reliable local validation.
4. Reproducible experiments.
5. Strong leaderboard performance.
6. Clean documentation for possible winning-solution publication.

---

## 3. Competition Context

Orbit Wars is a Kaggle simulation competition where a submitted agent plays episodes against other agents.

Key constraints:
- One Kaggle account only. Team max 5. Max 5 submissions/day.
- Competition data license: Apache 2.0. No redistribution.
- External data/models/LLMs allowed if reasonably accessible and not excessively costly.
- No private code sharing with other teams.
- Open-source code must permit commercial use.
- Winning code may need CC-BY 4.0 license, except documented exceptions.
- During evaluation: no internet access, no exfiltration, no external information.
- Replays may be public and reveal actions.

---

## 4. Verified Submission Format

**Format:** Single `main.py` OR `zip`/`gz`/`7z` archive with `main.py` at top level.

**Entrypoint:** The **last `def`** in the submitted file. It must accept an observation and return an action.

```python
# The last def in main.py must be the agent function:
def agent(obs):
    return action
```

All code changes must preserve this contract. Never place helper functions after the agent function.

---

## 5. Code Editing Rules

- Make small, reviewable changes.
- Keep strategy logic separated from observation parsing and action formatting.
- Keep final submission code minimal and robust.
- Avoid unnecessary dependencies.
- Do not introduce network calls.
- Do not introduce credential access.
- Do not write files from the runtime agent.
- Do not make broad refactors before submission.

Recommended structure:
```
src/orbit_wars/
  agent.py       — main agent logic
  observation.py — observation parsing
  actions.py     — action building
  physics.py     — physics/math helpers
  strategy.py    — strategy decisions
  evaluation.py  — local evaluation
  utils.py       — utilities
```

---

## 6. Security Rules

Never commit: `kaggle.json`, `.env`, API keys, cookies, tokens, MCP credentials, private datasets, raw competition files.

Do not add code using: `requests`, `httpx`, `urllib`, `socket`, cloud SDKs, telemetry SDKs, external HTTP APIs — unless human approves AND the code is not part of the submitted agent.

---

## 7. Testing Rules

Before considering a change complete:
```bash
python -m pytest tests/
python scripts/validate_submission.py --path submission/
```

If touching strategy or physics:
```bash
python scripts/run_local_tournament.py --config configs/local_eval.yaml
```

If touching packaging:
```bash
python scripts/package_submission.py --dry-run
python scripts/validate_submission.py --path submission/
```

---

## 8. Before Packaging a Submission

Run:
```bash
python scripts/validate_submission.py --path submission/
python scripts/package_submission.py --dry-run
```

Check: format is `main.py` or archive with `main.py` at top, last `def` is agent function, no secrets, no raw data, no internet access, `submission/MANIFEST.json` generated.

---

## 9. Before Using Kaggle API

Read-only commands allowed if credentials configured:
```bash
kaggle competitions list -s "orbit wars"
kaggle competitions files orbit-wars
kaggle competitions submissions orbit-wars
```

Commands requiring confirmation:
```bash
kaggle competitions download orbit-wars -p data/raw
kaggle competitions submit orbit-wars -f <FILE> -m "<MESSAGE>"
```

Before any submit:
```bash
python scripts/check_submission_limit.py
python scripts/list_kaggle_submissions.py
```

---

## 10. Experiment Traceability

Each experiment must record:
```markdown
- Experiment ID:
- Date:
- Branch:
- Commit:
- Config:
- Seeds:
- Command:
- Change/hypothesis:
- Local validation:
- Kaggle submission:
- Result:
- Conclusion:
- Next step:
```

---

## 11. Definition of Done

A task is done only when the response includes: what changed, files changed, tests run, validation status, compliance concerns, reproducibility notes, next best action.

If something is unverified, state it clearly. Do not invent details about Kaggle rules or submission format.
