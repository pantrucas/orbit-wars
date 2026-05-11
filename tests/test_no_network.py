"""Verify that the agent makes no network calls when executed."""

import importlib.util
import socket
import sys
import unittest.mock
from pathlib import Path

MAIN_PY = Path("submission/main.py")


def load_agent():
    spec = importlib.util.spec_from_file_location("submission", MAIN_PY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fns = [(k, v) for k, v in vars(module).items()
           if callable(v) and not k.startswith("_")]
    last_fn = max(fns, key=lambda kv: getattr(getattr(kv[1], "__code__", None), "co_firstlineno", 0))
    return last_fn[1]


def test_agent_makes_no_socket_connection():
    agent = load_agent()
    obs = {
        "step": 1,
        "player": 1,
        "planets": [
            {"x": 10.0, "y": 10.0, "owner": 1, "ships": 20.0, "growth_rate": 2.0},
            {"x": 90.0, "y": 90.0, "owner": 2, "ships": 5.0, "growth_rate": 1.0},
        ],
        "fleets": [],
    }

    original_connect = socket.socket.connect

    def patched_connect(self, *args, **kwargs):
        raise AssertionError(
            f"Agent attempted network connection: {args}. "
            "Network calls are forbidden during Kaggle evaluation."
        )

    with unittest.mock.patch.object(socket.socket, "connect", patched_connect):
        action = agent(obs)

    assert isinstance(action, dict), "Agent must return a dict."
