# Experiments

Each experiment must be fully traceable: config, seed, commit, results.

## Naming

Experiment IDs follow the pattern: `EXP001`, `EXP002`, etc.

## Structure

```
experiments/
  configs/   — YAML configs for each experiment
  results/   — One .md log per experiment, plus JSON result files
  reports/   — Summary reports comparing multiple experiments
```

## Creating a New Experiment

```bash
python scripts/log_experiment.py \
  --id EXP001 \
  --hypothesis "Greedy baseline beats random" \
  --config configs/baseline.yaml \
  --seeds 42
```

## Running

```bash
python scripts/run_local_tournament.py --config configs/local_eval.yaml
```

## Rules

- Never overwrite a result without `--force` and human approval.
- Record Kaggle submission ID if experiment leads to an upload.
- Update `PROJECT_MEMORY.md` when an experiment changes project direction.
