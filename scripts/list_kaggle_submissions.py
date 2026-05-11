"""List recent Kaggle submissions for Orbit Wars. Read-only."""

import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="List Kaggle submissions.")
    parser.add_argument("--competition", default="orbit-wars")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print command without running.")
    args = parser.parse_args()

    cmd = ["kaggle", "competitions", "submissions", args.competition]
    print(f"Command: {' '.join(cmd)}")

    if args.dry_run:
        print("[DRY RUN] Not executing.")
        sys.exit(0)

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
