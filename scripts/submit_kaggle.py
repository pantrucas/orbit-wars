"""
Safe wrapper for kaggle competitions submit.
Requires explicit --confirm flag and passes all pre-submit checks.
Runs in --dry-run mode by default.
"""

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Submit to Kaggle Orbit Wars.")
    parser.add_argument("--file", required=True, help="Path to submission file.")
    parser.add_argument("--message", required=True, help="Submission message.")
    parser.add_argument("--competition", default="orbit-wars")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Print command without executing (default).")
    parser.add_argument("--no-dry-run", action="store_true",
                        help="Actually submit. Requires --confirm.")
    parser.add_argument("--confirm", default="",
                        help='Must equal "CONFIRMO SUBIR A KAGGLE" to submit.')
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"ERROR: File not found: {args.file}")
        sys.exit(1)

    if not args.message.strip():
        print("ERROR: --message cannot be empty.")
        sys.exit(1)

    # Check limit
    print("Checking daily submission limit...")
    limit_check = subprocess.run(
        [sys.executable, "scripts/check_submission_limit.py", "--no-api"],
        capture_output=True, text=True,
    )
    print(limit_check.stdout)
    if limit_check.returncode != 0:
        print("ERROR: Submission limit check failed. Aborting.")
        sys.exit(1)

    cmd = [
        "kaggle", "competitions", "submit",
        args.competition,
        "-f", str(file_path),
        "-m", args.message,
    ]

    print(f"\nCommand: {' '.join(cmd)}")
    print(f"File: {file_path} ({file_path.stat().st_size / 1024:.1f} KB)")
    print(f"Message: {args.message}")

    dry = args.dry_run and not args.no_dry_run
    if dry:
        print("\n[DRY RUN] Not submitting. Pass --no-dry-run --confirm 'CONFIRMO SUBIR A KAGGLE' to submit.")
        sys.exit(0)

    if args.confirm != "CONFIRMO SUBIR A KAGGLE":
        print('\nERROR: --confirm must equal exactly: CONFIRMO SUBIR A KAGGLE')
        print("This safeguard prevents accidental submissions.")
        sys.exit(1)

    print("\nSubmitting...")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"\nSubmission sent at {datetime.now(timezone.utc).isoformat()}")
        print("Record this submission in SUBMISSION_LOG.md immediately.")
    else:
        print("\nERROR: Submission failed. Check output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
