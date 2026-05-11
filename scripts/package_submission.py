"""
Package submission/main.py into a .tar.gz archive.
Runs in --dry-run mode by default to prevent accidental packaging.
"""

import argparse
import hashlib
import json
import os
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

SUBMISSION_DIR = Path("submission")
MANIFEST_PATH = SUBMISSION_DIR / "MANIFEST.json"

EXCLUDE_PATTERNS = {
    ".env", ".env.local", "kaggle.json", "*.secret", "*.key", "*.token",
    "*.log", "__pycache__", "*.pyc", "*.pyo", "*.tar.gz", "*.zip",
}


def should_exclude(name: str) -> bool:
    for pat in EXCLUDE_PATTERNS:
        if pat.startswith("*"):
            if name.endswith(pat[1:]):
                return True
        elif name == pat:
            return True
    return False


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def package(output_path: str, dry_run: bool = True) -> bool:
    main_py = SUBMISSION_DIR / "main.py"
    if not main_py.exists():
        print(f"ERROR: {main_py} not found.")
        return False

    source = main_py.read_text(encoding="utf-8")
    sha = sha256_bytes(source.encode())

    if dry_run:
        print("[DRY RUN] Would create:", output_path)
        print(f"  main.py SHA256: {sha}")
        print(f"  Size: {len(source.encode())} bytes")
        print("  No files written. Pass --no-dry-run to package.")
        return True

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with tarfile.open(out, "w:gz") as tar:
        for f in sorted(SUBMISSION_DIR.rglob("*")):
            if f.is_dir():
                continue
            if should_exclude(f.name):
                print(f"  Skipping: {f}")
                continue
            arcname = f.relative_to(SUBMISSION_DIR)
            print(f"  Adding: {arcname}")
            tar.add(f, arcname=str(arcname))

    # Update manifest
    manifest = {}
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH) as fp:
            manifest = json.load(fp)

    manifest["packaged"] = datetime.now(timezone.utc).isoformat()
    manifest["output"] = str(out)
    manifest["main_sha256"] = sha
    manifest["validation_passed"] = False  # reset; must re-validate

    with open(MANIFEST_PATH, "w") as fp:
        json.dump(manifest, fp, indent=2)

    size_mb = out.stat().st_size / (1024 * 1024)
    print(f"\nPackaged: {out} ({size_mb:.2f} MB)")
    print("NOTE: Run validate_submission.py before uploading.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Package Orbit Wars submission.")
    parser.add_argument("--output", default="submission/submission.tar.gz")
    parser.add_argument("--no-dry-run", action="store_true", help="Actually write output.")
    args = parser.parse_args()

    dry_run = not args.no_dry_run
    if dry_run:
        print("Running in --dry-run mode. Use --no-dry-run to produce output.")

    ok = package(args.output, dry_run=dry_run)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
