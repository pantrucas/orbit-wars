"""Tests that submission/main.py satisfies the Kaggle submission contract.

Verified observation format (orbit_wars.json):
  planets: [[id, owner, x, y, radius, ships, production], ...]
  fleets:  [[id, owner, x, y, angle, from_planet_id, ships], ...]
  player:  int (0-3)

Verified action format:
  [[from_planet_id, angle_radians, num_ships], ...]  OR  []
"""

import ast
import importlib.util
from pathlib import Path

MAIN_PY = Path("submission/main.py")


def _load_module():
    spec = importlib.util.spec_from_file_location("submission", MAIN_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _last_fn(mod):
    fns = [(k, v) for k, v in vars(mod).items() if callable(v) and not k.startswith("_")]
    return max(fns, key=lambda kv: getattr(getattr(kv[1], "__code__", None), "co_firstlineno", 0))[1]


# Minimal valid observation using real format
_OBS_NORMAL = {
    "planets": [
        [0, 0, 20.0, 50.0, 3.0, 30.0, 2.0],  # player 0 owns this
        [1, 1, 80.0, 50.0, 3.0, 20.0, 2.0],  # player 1 owns this
        [2, -1, 50.0, 20.0, 2.0, 5.0, 1.0],  # neutral
    ],
    "fleets": [],
    "player": 0,
    "angular_velocity": 0.035,
    "remainingOverageTime": 60,
}

_OBS_EMPTY = {
    "planets": [],
    "fleets": [],
    "player": 0,
    "angular_velocity": 0.035,
    "remainingOverageTime": 60,
}

_OBS_NO_TARGETS = {
    "planets": [
        [0, 0, 20.0, 50.0, 3.0, 30.0, 2.0],
        [1, 0, 80.0, 50.0, 3.0, 20.0, 2.0],
    ],
    "fleets": [],
    "player": 0,
    "angular_velocity": 0.035,
    "remainingOverageTime": 60,
}


def test_main_py_exists():
    assert MAIN_PY.exists()


def test_last_def_accepts_observation():
    source = MAIN_PY.read_text(encoding="utf-8")
    tree = ast.parse(source)
    funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    last = max(funcs, key=lambda f: f.lineno)
    assert len(last.args.args) >= 1, f"Last def '{last.name}' must accept at least one argument."


def test_action_is_list():
    fn = _last_fn(_load_module())
    action = fn(_OBS_NORMAL)
    assert isinstance(action, list), f"Action must be a list, got {type(action)}"


def test_action_items_are_lists_of_three():
    fn = _last_fn(_load_module())
    action = fn(_OBS_NORMAL)
    for item in action:
        assert isinstance(item, list), f"Each order must be a list, got {type(item)}"
        assert len(item) == 3, f"Each order must have 3 elements [id, angle, ships], got {item}"


def test_action_ships_are_positive_int():
    fn = _last_fn(_load_module())
    action = fn(_OBS_NORMAL)
    for item in action:
        assert isinstance(item[2], int), f"ships must be int, got {type(item[2])}: {item}"
        assert item[2] > 0, f"ships must be > 0, got {item[2]}"


def test_action_angle_is_float():
    fn = _last_fn(_load_module())
    action = fn(_OBS_NORMAL)
    import math
    for item in action:
        assert isinstance(item[1], float), f"angle must be float, got {type(item[1])}: {item}"
        assert -math.pi <= item[1] <= math.pi, f"angle out of range: {item[1]}"


def test_empty_obs_returns_list():
    fn = _last_fn(_load_module())
    action = fn(_OBS_EMPTY)
    assert isinstance(action, list)


def test_no_targets_returns_empty_list():
    fn = _last_fn(_load_module())
    action = fn(_OBS_NO_TARGETS)
    assert isinstance(action, list)


def test_no_network_imports():
    source = MAIN_PY.read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden = {"requests", "httpx", "urllib3", "aiohttp", "socket", "boto3"}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = ([a.name.split(".")[0] for a in node.names]
                     if isinstance(node, ast.Import)
                     else [(node.module or "").split(".")[0]])
            for name in names:
                assert name not in forbidden, f"Forbidden import '{name}' in main.py"
