"""Tests that the agent produces deterministic outputs."""

import importlib.util
from pathlib import Path

MAIN_PY = Path("submission/main.py")

SAMPLE_OBS = {
    "planets": [
        [0, 0, 20.0, 50.0, 3.0, 30.0, 2.0],
        [1, 1, 80.0, 50.0, 3.0, 20.0, 2.0],
        [2, -1, 50.0, 20.0, 2.0, 5.0, 1.0],
    ],
    "fleets": [],
    "player": 0,
    "angular_velocity": 0.035,
    "remainingOverageTime": 60,
}


def _load_agent():
    spec = importlib.util.spec_from_file_location("submission", MAIN_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fns = [(k, v) for k, v in vars(mod).items() if callable(v) and not k.startswith("_")]
    return max(fns, key=lambda kv: getattr(getattr(kv[1], "__code__", None), "co_firstlineno", 0))[1]


def test_agent_is_deterministic():
    agent = _load_agent()
    results = [agent(SAMPLE_OBS) for _ in range(5)]
    first = results[0]
    for i, r in enumerate(results[1:], 2):
        assert r == first, f"Agent non-deterministic on run {i}: {first} vs {r}"


def test_agent_same_output_across_instances():
    a1, a2 = _load_agent(), _load_agent()
    assert a1(SAMPLE_OBS) == a2(SAMPLE_OBS)
