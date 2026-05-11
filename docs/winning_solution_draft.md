# Winning Solution Draft

Keep this document updated throughout the competition.
If the solution wins, this becomes the basis for the required public writeup.

---

## Summary

`<FILL: brief description of the final approach>`

## Environment Setup

```bash
# Python version
python --version  # e.g. Python 3.10.x

# Install dependencies
pip install -r requirements.txt
```

## Reproducing the Final Submission

```bash
# 1. Clone the repo at the winning commit
git checkout <WINNING_COMMIT_HASH>

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Re-train if a learned component
# python scripts/<train_script>.py --config configs/final/<config>.yaml

# 4. Validate
python scripts/validate_submission.py --path submission/

# 5. Package
python scripts/package_submission.py --no-dry-run --output submission/submission.tar.gz
```

## Agent Strategy

`<FILL: describe the final agent logic>`

## Key Design Decisions

`<FILL: what worked and why>`

## What Did NOT Work

`<FILL: record failed experiments for reproducibility>`

## External Data / Models

| Asset | Source | License | Version | Used for |
|---|---|---|---|---|
| `<FILL>` | `<FILL>` | `<FILL>` | `<FILL>` | `<FILL>` |

## Compute Used

`<FILL: hardware, runtime, cost if any>`

## License Notes

This solution is intended to be released under CC-BY 4.0 as required by Kaggle competition rules.

Exceptions:
- `<FILL: list any third-party assets with different license>`

## Experiment Log Summary

See `experiments/results/` for full details.

| Experiment | Result | Key insight |
|---|---|---|
| EXP001 | `<FILL>` | `<FILL>` |
