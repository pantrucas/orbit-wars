# Submission Notes

## Format

- **File:** `main.py` (single file submission) or archive with `main.py` at top level.
- **Entrypoint:** Last `def` in file — `agent(obs) -> action`.

## Agent Description

Greedy heuristic baseline. Each owned planet evaluates all capturable targets and dispatches 60% of available ships to the highest-value target (growth rate / ships cost, penalized by distance).

## Reproduction

```bash
# Validate before packaging
python scripts/validate_submission.py --path submission/

# Package as archive
python scripts/package_submission.py --output submission/submission.tar.gz

# Check limit before uploading
python scripts/check_submission_limit.py
```

## Dependencies

None beyond Python standard library (`math`, `random`).

## Commit

See `MANIFEST.json` for exact commit hash and validation timestamp.
