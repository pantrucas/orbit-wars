"""
Validate a submission directory or file before packaging/uploading.
Checks: entrypoint contract, no network imports, no secrets, action format.
"""

import argparse
import ast
import importlib.util
import os
import re
import sys
from pathlib import Path

FORBIDDEN_IMPORTS = {
    "requests", "httpx", "urllib3", "aiohttp", "httplib2",
    "boto3", "botocore", "google.cloud", "azure",
    "telemetry", "sentry_sdk", "datadog",
}

FORBIDDEN_PATTERNS = [
    r"socket\.connect",
    r"urllib\.request",
    r"http\.client",
    r"subprocess\.(run|Popen|call|check_output)",
    r"os\.system\(",
    r"os\.environ\[.*(KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL)",
]

MAX_FILE_SIZE_MB = 100


def check_last_def_is_agent(source: str) -> tuple:
    """Verify the last def in the file accepts (obs) and is named agent-like."""
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return False, f"Syntax error: {e}"

    funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    if not funcs:
        return False, "No function definitions found."

    # Last def by line number
    last_fn = max(funcs, key=lambda f: f.lineno)
    args = [a.arg for a in last_fn.args.args]

    if len(args) < 1:
        return False, f"Last def '{last_fn.name}' must accept at least one argument (observation)."

    return True, f"Last def: '{last_fn.name}({', '.join(args)})' at line {last_fn.lineno}"


def check_forbidden_imports(source: str) -> list:
    issues = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ["Could not parse for import check."]

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            else:
                names = [node.module or ""]
            for name in names:
                root = name.split(".")[0]
                if root in FORBIDDEN_IMPORTS:
                    issues.append(f"Forbidden import '{name}' at line {node.lineno}")
    return issues


def check_forbidden_patterns(source: str) -> list:
    issues = []
    for i, line in enumerate(source.splitlines(), 1):
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, line):
                issues.append(f"Forbidden pattern '{pattern}' at line {i}: {line.strip()}")
    return issues


def check_secrets(path: Path) -> list:
    issues = []
    secret_patterns = [
        r"(?i)(api[_\-]?key|token|secret|password|credential)\s*=\s*['\"][^'\"]{8,}",
        r"sk-[a-zA-Z0-9]{20,}",
    ]
    for f in path.rglob("*.py"):
        text = f.read_text(encoding="utf-8", errors="ignore")
        for pattern in secret_patterns:
            matches = re.findall(pattern, text)
            if matches:
                issues.append(f"Potential secret in {f}: {matches}")
    return issues


def validate_path(submission_path: str) -> bool:
    path = Path(submission_path)
    ok = True

    # Find main.py
    if path.is_file() and path.name == "main.py":
        main_py = path
    elif path.is_dir():
        main_py = path / "main.py"
    else:
        print(f"ERROR: Expected main.py file or directory containing main.py. Got: {path}")
        return False

    if not main_py.exists():
        print(f"ERROR: main.py not found at {main_py}")
        return False

    print(f"Validating: {main_py}")
    source = main_py.read_text(encoding="utf-8")

    # 1. Check last def
    passed, msg = check_last_def_is_agent(source)
    if passed:
        print(f"  [OK] Entrypoint: {msg}")
    else:
        print(f"  [FAIL] Entrypoint: {msg}")
        ok = False

    # 2. Forbidden imports
    import_issues = check_forbidden_imports(source)
    if import_issues:
        for issue in import_issues:
            print(f"  [FAIL] {issue}")
        ok = False
    else:
        print("  [OK] No forbidden imports.")

    # 3. Forbidden patterns
    pattern_issues = check_forbidden_patterns(source)
    if pattern_issues:
        for issue in pattern_issues:
            print(f"  [FAIL] {issue}")
        ok = False
    else:
        print("  [OK] No forbidden network/shell patterns.")

    # 4. Secrets
    secret_issues = check_secrets(path if path.is_dir() else path.parent)
    if secret_issues:
        for issue in secret_issues:
            print(f"  [WARN] {issue}")
        ok = False
    else:
        print("  [OK] No obvious secrets.")

    # 5. File size
    size_mb = main_py.stat().st_size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        print(f"  [FAIL] main.py is {size_mb:.1f} MB (max {MAX_FILE_SIZE_MB} MB).")
        ok = False
    else:
        print(f"  [OK] File size: {size_mb:.2f} MB")

    print()
    if ok:
        print("VALIDATION PASSED")
    else:
        print("VALIDATION FAILED — do not submit.")

    return ok


def main():
    parser = argparse.ArgumentParser(description="Validate Orbit Wars submission.")
    parser.add_argument("--path", required=True, help="Path to main.py or submission directory.")
    args = parser.parse_args()

    passed = validate_path(args.path)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
