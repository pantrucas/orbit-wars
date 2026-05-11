# Orbit Wars — Kaggle Competition

Agent solution for the [Kaggle Orbit Wars](https://www.kaggle.com/competitions/orbit-wars) competition.

## Submission Format

- Single `main.py` OR a `zip`/`gz`/`7z` archive with `main.py` at the top level.
- The **last `def`** in the file must accept an observation and return an action.

## Quick Start

```bash
pip install -r requirements.txt

# Validate submission
python scripts/validate_submission.py --path submission/

# Run local tournament
python scripts/run_local_tournament.py --config configs/local_eval.yaml

# Check submission limit before uploading
python scripts/check_submission_limit.py
```

## Key Files

| File | Purpose |
|---|---|
| `CLAUDE.md` | Claude Code instructions |
| `AGENTS.md` | Codex instructions |
| `PROJECT_MEMORY.md` | Shared project memory |
| `SUBMISSION_LOG.md` | All Kaggle submission records |
| `COMPLIANCE.md` | Rule compliance matrix |
| `submission/main.py` | Final agent (last def = entrypoint) |

## Structure

```
src/orbit_wars/   — core agent and game logic
submission/       — Kaggle submission artifacts
scripts/          — validation, packaging, submission tools
tests/            — safety and reproducibility tests
experiments/      — configs and results
configs/          — YAML configuration files
docs/             — architecture and strategy docs
```

## Development Rules

- Never submit to Kaggle without explicit human approval.
- Max 5 submissions/day — always run `check_submission_limit.py` first.
- No internet access in submitted agent code.
- Record every experiment in `experiments/results/`.
- Keep `COMPLIANCE.md` up to date.
