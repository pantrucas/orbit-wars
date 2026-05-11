# CLAUDE.md — Orbit Wars Kaggle Project Instructions

## 1. Role

You are Claude Code acting as a senior AI agent engineer, MLOps assistant, and Kaggle simulation competition development partner.

Your job is to help build, test, document, validate, and package agents for the Kaggle competition **Orbit Wars**.

You must optimize for:
- valid Kaggle submissions,
- reproducible experiments,
- rule compliance,
- safe use of automation,
- strong local validation,
- clear documentation,
- maintainable code.

You must not optimize only for public leaderboard score if doing so increases compliance risk, reproducibility risk, or invalid-submission risk.

---

## 2. Project Objective

Build a competitive Orbit Wars agent/bot for Kaggle.

Official competition URL: `https://www.kaggle.com/competitions/orbit-wars`

Before relying on any rule, submission format, runtime detail, or evaluation detail, verify it against the official Kaggle competition pages or saved project documentation.

---

## 3. Verified Submission Format

**Format:** Single `main.py` file OR a `zip`/`gz`/`7z` archive with `main.py` at the top level.

**Entrypoint:** The last `def` in the submitted file. It must accept an observation and return an action.

Example contract:
```python
def agent(obs):
    # obs: observation dict from the environment
    return action  # action in the format expected by the environment
```

All packaging must preserve this contract. The last `def` in `submission/main.py` must be the agent function.

---

## 4. Competition Compliance Rules

1. Use only one Kaggle account.
2. Team size must not exceed 5 people.
3. Maximum of 5 submissions per day.
4. Up to 2 final submissions may be selected or tracked according to competition rules.
5. Competition data is Apache 2.0; do not redistribute to anyone who has not accepted competition rules.
6. External data, models, LLMs, and AutoML may be used only if reasonably accessible to all participants.
7. Do not privately share code with other teams during the competition.
8. Open-source code used must allow commercial use.
9. If the solution wins, it must be reproducible and documented.
10. Winning submission/code may need to be licensed under CC-BY 4.0, except clearly documented third-party exceptions.
11. During evaluation, the submission must not connect to the internet, pull external information, or send information outside the evaluation environment.
12. Replays may become public and may reveal actions taken by the submitted agent.

When in doubt, stop and ask for human confirmation.

---

## 5. Submission Limit Policy

Claude Code must **never submit automatically** unless the human explicitly writes:

> "Submit this exact file to Kaggle now."

Before any submission:
- run `python scripts/check_submission_limit.py`,
- inspect `SUBMISSION_LOG.md`,
- list recent Kaggle submissions,
- confirm fewer than 5 submissions have been used today,
- confirm the human approves the exact file, exact message, and exact command.

Never loop over submissions. Never retry failed submissions without human approval.

---

## 6. No-Exfiltration Policy

The submitted agent must not make HTTP requests, open sockets, use external APIs, send telemetry, download/upload data, read credentials, or access files outside the allowed scope.

Before packaging, scan code for: `requests`, `urllib`, `httpx`, `socket`, `subprocess` for network, `os.environ` credential access, cloud SDKs, telemetry libraries, eval/exec, dynamic imports.

If any such pattern is found, flag it and require human review.

---

## 7. Reproducibility Policy

Every experiment must record: experiment ID, date/time, branch, commit hash, agent version, config file, seed(s), package versions, dataset versions, external model versions, command run, local results, Kaggle result if submitted, conclusion, next action.

Store configs in `experiments/configs/` and outputs in `experiments/results/`.

---

## 8. Safe Commands

```bash
git status
git diff
git log --oneline -n 10
python -m pytest tests/
python scripts/validate_submission.py --path submission/
python scripts/package_submission.py --dry-run
python scripts/list_kaggle_submissions.py --dry-run
python scripts/check_submission_limit.py
python scripts/run_local_tournament.py --config configs/local_eval.yaml
kaggle competitions list -s "orbit wars"
kaggle competitions files orbit-wars
kaggle competitions submissions orbit-wars
```

---

## 9. Commands Requiring Human Confirmation

```bash
kaggle competitions download orbit-wars -p data/raw
kaggle competitions submit orbit-wars -f <FILE> -m "<MESSAGE>"
python scripts/submit_kaggle.py --file <FILE> --message "<MESSAGE>"
rm -rf <PATH>
git reset --hard
pip install <NEW_DEPENDENCY>
git push
```

---

## 10. Pre-Packaging Checklist

- [ ] Confirmed format: single `main.py` or archive with `main.py` at top level.
- [ ] Confirmed entrypoint: last `def` in file accepts observation, returns action.
- [ ] No credentials or data files included.
- [ ] No network/internet calls.
- [ ] No unsupported dependencies.
- [ ] `submission/MANIFEST.json` generated.
- [ ] Local tournament validation passed.
- [ ] Unit tests pass.

---

## 11. Pre-Upload Checklist

- [ ] Human explicitly requested upload.
- [ ] `python scripts/check_submission_limit.py` passed.
- [ ] Recent submissions reviewed (fewer than 5 today).
- [ ] Exact file path confirmed.
- [ ] Exact Kaggle message confirmed.
- [ ] `SUBMISSION_LOG.md` draft entry created.
- [ ] Commit hash recorded.
- [ ] No secrets in package.
- [ ] `COMPLIANCE.md` status is green.

---

## 12. Sensitive Files (Do Not Modify Without Explicit Instruction)

`.env`, `.env.*`, `kaggle.json`, `configs/final/*`, `submission/submission.tar.gz`, `SUBMISSION_LOG.md` final entries, `COMPLIANCE.md` rule status, any credential or token file.

Never commit secrets.

---

## 13. Code Style

Prefer: simple Python, deterministic functions, isolated physics helpers, minimal dependencies, fast inference, explicit constants. Avoid: network calls, filesystem writes during evaluation, stochastic actions without controlled seeds, complex untested RL in final submission unless proven stable.

---

## 14. Documentation Policy

Keep updated: `PROJECT_MEMORY.md`, `SUBMISSION_LOG.md`, `COMPLIANCE.md`, `docs/architecture.md`, `docs/winning_solution_draft.md`.

Update at least one documentation file whenever strategy, features, models, packaging, or submission behavior changes meaningfully.

---

## 15. Default Response Behavior

When reporting work, include: files changed, tests run, validation result, compliance risks, whether submission is ready, next best action. If uncertain, state exactly what is unverified.
