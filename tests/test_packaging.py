"""Tests for submission packaging integrity."""

import ast
import json
from pathlib import Path

SUBMISSION_DIR = Path("submission")
MAIN_PY = SUBMISSION_DIR / "main.py"
MANIFEST = SUBMISSION_DIR / "MANIFEST.json"

FORBIDDEN_FILES = {"kaggle.json", ".env", ".env.local", "credentials.json"}


def test_main_py_present():
    assert MAIN_PY.exists(), "submission/main.py must exist."


def test_manifest_present():
    assert MANIFEST.exists(), "submission/MANIFEST.json must exist."


def test_manifest_has_required_keys():
    with open(MANIFEST) as f:
        data = json.load(f)
    required = {"format", "entrypoint"}
    missing = required - set(data.keys())
    assert not missing, f"MANIFEST.json missing keys: {missing}"


def test_no_credentials_in_submission():
    for path in SUBMISSION_DIR.rglob("*"):
        if path.is_file():
            assert path.name not in FORBIDDEN_FILES, (
                f"Forbidden file found in submission: {path}"
            )


def test_no_data_files_in_submission():
    data_extensions = {".csv", ".parquet", ".jsonl", ".pkl", ".pt", ".pth", ".ckpt"}
    for path in SUBMISSION_DIR.rglob("*"):
        if path.suffix in data_extensions:
            assert False, f"Data/model file found in submission: {path}. Remove before packaging."


def test_main_py_valid_syntax():
    source = MAIN_PY.read_text(encoding="utf-8")
    try:
        ast.parse(source)
    except SyntaxError as e:
        assert False, f"Syntax error in submission/main.py: {e}"


def test_last_def_is_agent_function():
    source = MAIN_PY.read_text(encoding="utf-8")
    tree = ast.parse(source)
    funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    assert funcs, "No function definitions in main.py."
    last_fn = max(funcs, key=lambda f: f.lineno)
    assert len(last_fn.args.args) >= 1, (
        f"Last def '{last_fn.name}' must accept at least one argument (observation)."
    )
