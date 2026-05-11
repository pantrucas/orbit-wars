# Experiments Methodology

## Principles

1. Every experiment is reproducible: config, seed, commit, command.
2. Never overwrite previous results without explicit intent.
3. Local validation before Kaggle submission.
4. Record hypothesis before running, not after.

## Workflow

```
Hypothesis → Config YAML → Run locally → Record results → Compare to baseline → Decide on submission
```

## Experiment Lifecycle

1. Create config in `experiments/configs/<EXP_ID>.yaml`.
2. Log experiment scaffold:
   ```bash
   python scripts/log_experiment.py --id EXP001 --hypothesis "..." --config experiments/configs/EXP001.yaml
   ```
3. Run tournament:
   ```bash
   python scripts/run_local_tournament.py --config experiments/configs/EXP001.yaml
   ```
4. Update `experiments/results/EXP001.md` with results and conclusion.
5. If promising: run `validate_submission.py`, then consider packaging.
6. If submitting: follow full pre-submission checklist in `CLAUDE.md`.

## Metrics

- Win rate vs. random opponent.
- Win rate vs. prior best agent.
- Average steps per episode.
- Action validity rate (no crashes).

## Anti-Patterns to Avoid

- Reporting results without recording the commit hash.
- Tuning hyperparameters to match a single Kaggle result.
- Selecting submissions based on a single lucky episode.
- Submitting without local validation.
