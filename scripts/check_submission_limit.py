"""
Check how many Kaggle submissions have been used today.
Fails with exit code 1 if the daily limit (5) has been reached.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

LIMIT = 5
LOG_PATH = Path("SUBMISSION_LOG.md")


def count_local_today() -> int:
    """Count submissions recorded in SUBMISSION_LOG.md for today (UTC)."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if not LOG_PATH.exists():
        return 0
    text = LOG_PATH.read_text(encoding="utf-8")
    return text.count(today)


def count_kaggle_api(competition: str) -> int:
    """Query Kaggle API for today's submission count. Returns -1 on failure."""
    try:
        result = subprocess.run(
            ["kaggle", "competitions", "submissions", competition, "--csv"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            return -1
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        lines = result.stdout.strip().splitlines()
        return sum(1 for line in lines[1:] if today in line)
    except Exception:
        return -1


def main():
    parser = argparse.ArgumentParser(description="Check daily Kaggle submission limit.")
    parser.add_argument("--competition", default="orbit-wars")
    parser.add_argument("--no-api", action="store_true", help="Skip Kaggle API check.")
    args = parser.parse_args()

    local_count = count_local_today()
    print(f"Local SUBMISSION_LOG count today: {local_count}")

    if not args.no_api:
        api_count = count_kaggle_api(args.competition)
        if api_count >= 0:
            print(f"Kaggle API count today: {api_count}")
            effective = max(local_count, api_count)
        else:
            print("Kaggle API unavailable. Using local count only.")
            effective = local_count
    else:
        effective = local_count

    remaining = LIMIT - effective
    print(f"Submissions used today: {effective} / {LIMIT}")
    print(f"Remaining: {remaining}")

    if effective >= LIMIT:
        print("ERROR: Daily submission limit reached. Do not submit today.")
        sys.exit(1)

    print("OK: Submission limit not reached.")
    return 0


if __name__ == "__main__":
    main()
