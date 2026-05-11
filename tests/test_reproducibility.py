"""Tests that the agent produces deterministic outputs given the same observation."""

import importlib.util
from pathlib import Path

MAIN_PY = Path("submission/main.py")


def load_agent():
    spec = importlib.util.spec_from_file_location("submission", MAIN_PY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fns = [(k, v) for k, v in vars(module).items()
           if callable(v) and not k.startswith("_")]
    return max(fns, key=lambda kv: getattr(getattr(kv[1], "__code__", None), "co_firstlineno", 0))[1]


SAMPLE_OBS = {
    "step": 5,
    "player": 1,
    "planets": [
        {"x": 10.0, "y": 10.0, "owner": 1, "ships": 30.0, "growth_rate": 2.0},
        {"x": 50.0, "y": 50.0, "owner": 0, "ships": 8.0, "growth_rate": 3.0},
        {"x": 90.0, "y": 90.0, "owner": 2, "ships": 15.0, "growth_rate": 2.0},
    ],
    "fleets": [],
}


def test_agent_is_deterministic():
    agent = load_agent()
    results = [agent(SAMPLE_OBS) for _ in range(5)]
    first = results[0]
    for i, r in enumerate(results[1:], 2):
        assert r == first, (
            f"Agent produced different output on run {i}. "
            "Agent must be deterministic for reproducibility."
        )


def test_agent_same_output_across_instances():
    agent1 = load_agent()
    agent2 = load_agent()
    r1 = agent1(SAMPLE_OBS)
    r2 = agent2(SAMPLE_OBS)
    assert r1 == r2, "Agent output differs between instances with same input."
