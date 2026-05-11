"""
Run a local tournament to evaluate the agent.
Imports the agent from submission/main.py and runs it against opponents.
"""

import argparse
import importlib.util
import json
import sys
from pathlib import Path


def load_agent(path: str = "submission/main.py"):
    """Load the agent function (last def) from a Python file."""
    spec = importlib.util.spec_from_file_location("submission_agent", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Find the last defined function (the submission contract)
    fns = [v for k, v in vars(module).items() if callable(v) and not k.startswith("_")]
    if not fns:
        raise ValueError(f"No callable functions found in {path}")

    # Return the last one by inspecting __code__.co_firstlineno
    last_fn = max(fns, key=lambda f: getattr(getattr(f, "__code__", None), "co_firstlineno", 0))
    print(f"Loaded agent function: '{last_fn.__name__}' from {path}")
    return last_fn


def random_agent(obs: dict) -> dict:
    """Simple random baseline opponent."""
    import random
    planets = obs.get("planets", [])
    player = obs.get("player", 1)
    my_planets = [i for i, p in enumerate(planets) if p.get("owner") == player and p.get("ships", 0) > 1]
    other_planets = [i for i, p in enumerate(planets) if p.get("owner") != player]

    if not my_planets or not other_planets:
        return {"orders": []}

    src = random.choice(my_planets)
    dst = random.choice(other_planets)
    ships = max(1, int(planets[src].get("ships", 1) * 0.5))
    return {"orders": [{"type": "fleet", "source": src, "destination": dst, "ships": ships}]}


def simulate_match(agent_fn, opponent_fn, num_steps: int = 50, seed: int = 42) -> dict:
    """
    Stub match simulator. Replace with real environment when available.
    Returns a plausible result structure for testing the pipeline.
    """
    import random
    rng = random.Random(seed)

    agent_score = 0
    opponent_score = 0

    # Stub: generate fake observations and count valid responses
    for step in range(num_steps):
        obs = {
            "step": step,
            "player": 1,
            "planets": [
                {"x": rng.uniform(0, 100), "y": rng.uniform(0, 100),
                 "owner": rng.choice([0, 1, 2]), "ships": rng.uniform(5, 50),
                 "growth_rate": rng.uniform(1, 5)}
                for _ in range(8)
            ],
            "fleets": [],
        }
        try:
            action = agent_fn(obs)
            if action and "orders" in action:
                agent_score += 1
        except Exception as e:
            print(f"  Agent error at step {step}: {e}")

    winner = 1 if agent_score >= opponent_score else 2
    return {"winner": winner, "agent_score": agent_score, "opponent_score": opponent_score, "seed": seed}


def main():
    parser = argparse.ArgumentParser(description="Run local tournament.")
    parser.add_argument("--config", default="configs/local_eval.yaml")
    parser.add_argument("--agent", default="submission/main.py")
    parser.add_argument("--episodes", type=int, default=10)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    print(f"Loading agent from: {args.agent}")
    agent_fn = load_agent(args.agent)

    opponents = [random_agent]
    results = []

    for ep in range(args.episodes):
        opp = opponents[ep % len(opponents)]
        seed = args.seed + ep
        r = simulate_match(agent_fn, opp, seed=seed)
        results.append(r)
        status = "WIN" if r["winner"] == 1 else "LOSS"
        print(f"  Episode {ep+1:3d}: {status}  (seed={seed})")

    wins = sum(1 for r in results if r["winner"] == 1)
    print(f"\nResults: {wins}/{len(results)} wins ({100*wins/len(results):.1f}%)")

    output = Path("experiments/results/local_tournament_latest.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"wins": wins, "total": len(results), "results": results}, indent=2))
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
