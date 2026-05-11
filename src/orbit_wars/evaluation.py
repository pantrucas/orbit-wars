"""Local evaluation helpers for Orbit Wars."""

from typing import Callable, Dict, List, Optional
import random


def run_episode(
    agent_fn: Callable,
    opponent_fn: Callable,
    env_fn: Callable,
    seed: Optional[int] = None,
) -> Dict:
    """
    Run a single episode between agent_fn and opponent_fn in env_fn.
    Returns a result dict with winner, steps, and scores.

    env_fn must return an object with:
        reset(seed) -> (obs1, obs2)
        step(action1, action2) -> (obs1, obs2, done, info)
    """
    if seed is not None:
        random.seed(seed)

    env = env_fn()
    obs1, obs2 = env.reset(seed=seed)
    done = False
    step = 0

    while not done:
        action1 = agent_fn(obs1)
        action2 = opponent_fn(obs2)
        obs1, obs2, done, info = env.step(action1, action2)
        step += 1

    return {
        "winner": info.get("winner"),
        "steps": step,
        "score_agent": info.get("score_1", 0),
        "score_opponent": info.get("score_2", 0),
        "seed": seed,
    }


def run_tournament(
    agent_fn: Callable,
    opponents: List[Callable],
    env_fn: Callable,
    episodes_per_opponent: int = 10,
    base_seed: int = 42,
) -> Dict:
    """Run agent against a list of opponents. Return aggregate win rate and stats."""
    results = []
    for opp_idx, opp_fn in enumerate(opponents):
        for ep in range(episodes_per_opponent):
            seed = base_seed + opp_idx * 1000 + ep
            r = run_episode(agent_fn, opp_fn, env_fn, seed=seed)
            r["opponent_idx"] = opp_idx
            results.append(r)

    wins = sum(1 for r in results if r["winner"] == 1)
    total = len(results)
    return {
        "win_rate": wins / total if total > 0 else 0.0,
        "wins": wins,
        "total": total,
        "results": results,
    }
