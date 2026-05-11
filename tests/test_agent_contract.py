"""Tests that submission/main.py satisfies the Kaggle submission contract."""

import ast
import importlib.util
import inspect
from pathlib import Path

MAIN_PY = Path("submission/main.py")


def load_submission_module():
    spec = importlib.util.spec_from_file_location("submission", MAIN_PY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_last_def(source: str):
    tree = ast.parse(source)
    funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    return max(funcs, key=lambda f: f.lineno) if funcs else None


def test_main_py_exists():
    assert MAIN_PY.exists(), "submission/main.py must exist."


def test_last_def_accepts_observation():
    source = MAIN_PY.read_text(encoding="utf-8")
    fn = get_last_def(source)
    assert fn is not None, "No function definitions found in main.py."
    assert len(fn.args.args) >= 1, (
        f"Last def '{fn.name}' must accept at least one argument (observation)."
    )


def test_last_def_returns_action_on_empty_obs():
    module = load_submission_module()
    fns = [(k, v) for k, v in vars(module).items()
           if callable(v) and not k.startswith("_")]
    assert fns, "No callable functions in submission module."

    last_fn = max(fns, key=lambda kv: getattr(getattr(kv[1], "__code__", None), "co_firstlineno", 0))
    fn_name, fn = last_fn

    obs = {
        "step": 0,
        "player": 1,
        "planets": [
            {"x": 10.0, "y": 20.0, "owner": 1, "ships": 10.0, "growth_rate": 1.0},
            {"x": 80.0, "y": 80.0, "owner": 0, "ships": 3.0, "growth_rate": 2.0},
        ],
        "fleets": [],
    }
    action = fn(obs)
    assert isinstance(action, dict), f"Agent '{fn_name}' must return a dict, got {type(action)}."


def test_last_def_handles_empty_observation():
    module = load_submission_module()
    fns = [(k, v) for k, v in vars(module).items()
           if callable(v) and not k.startswith("_")]
    last_fn = max(fns, key=lambda kv: getattr(getattr(kv[1], "__code__", None), "co_firstlineno", 0))
    _, fn = last_fn

    action = fn({})
    assert isinstance(action, dict), "Agent must handle empty observation without crashing."


def test_no_network_imports():
    source = MAIN_PY.read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden = {"requests", "httpx", "urllib3", "aiohttp", "socket", "boto3"}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
            else:
                names = [(node.module or "").split(".")[0]]
            for name in names:
                assert name not in forbidden, (
                    f"Forbidden network import '{name}' found in submission/main.py."
                )
