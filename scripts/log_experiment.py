"""
Create or update an experiment log entry in experiments/results/.
"""

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path


TEMPLATE = """\
# Experiment: {experiment_id}

- Date: {date}
- Human owner: {owner}
- Agent assistant: {assistant}
- Branch: {branch}
- Commit: {commit}
- Config: {config}
- Seeds: {seeds}
- Command: {command}
- Hypothesis: {hypothesis}
- Change: {change}
- Local validation: pending
- Kaggle submission: pending
- Result: pending
- Risks: pending
- Conclusion: pending
- Next action: pending
"""


def get_git_info() -> tuple:
    try:
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True,
        ).stdout.strip()
        commit = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True,
        ).stdout.strip()
        return branch, commit
    except Exception:
        return "unknown", "unknown"


def main():
    parser = argparse.ArgumentParser(description="Create experiment log.")
    parser.add_argument("--id", required=True, help="Experiment ID, e.g. EXP001")
    parser.add_argument("--owner", default="human")
    parser.add_argument("--assistant", default="Claude/Codex")
    parser.add_argument("--config", default="")
    parser.add_argument("--seeds", default="42")
    parser.add_argument("--hypothesis", default="")
    parser.add_argument("--change", default="")
    parser.add_argument("--command", default="")
    parser.add_argument("--force", action="store_true", help="Overwrite if exists.")
    args = parser.parse_args()

    output_dir = Path("experiments/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{args.id}.md"

    if output_path.exists() and not args.force:
        print(f"ERROR: {output_path} already exists. Use --force to overwrite.")
        return

    branch, commit = get_git_info()
    date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    content = TEMPLATE.format(
        experiment_id=args.id,
        date=date,
        owner=args.owner,
        assistant=args.assistant,
        branch=branch,
        commit=commit,
        config=args.config,
        seeds=args.seeds,
        command=args.command,
        hypothesis=args.hypothesis,
        change=args.change,
    )

    output_path.write_text(content, encoding="utf-8")
    print(f"Created: {output_path}")


if __name__ == "__main__":
    main()
