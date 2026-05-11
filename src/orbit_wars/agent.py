"""Main agent for Orbit Wars."""

from .observation import parse_observation
from .strategy import baseline_orders
from .actions import build_action, no_op


def decide(obs: dict) -> dict:
    """
    Parse observation, run strategy, return action.
    This is the core agent logic — keep it offline-safe (no network, no file I/O).
    """
    try:
        game = parse_observation(obs)
        orders = baseline_orders(game)
        if not orders:
            return no_op()
        return build_action(orders)
    except Exception:
        return no_op()
