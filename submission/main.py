"""
Orbit Wars — Kaggle submission entrypoint.

Rules:
- No internet access.
- No file I/O.
- No credentials.
- The LAST def in this file must accept observation and return action.
"""

import math
import random
from typing import List, Optional, Dict


# --- Observation parsing ---

def _parse_obs(obs: dict) -> dict:
    step = obs.get("step", 0)
    player_id = obs.get("player", 1)
    planets = obs.get("planets", [])
    fleets = obs.get("fleets", [])
    return {
        "step": step,
        "player": player_id,
        "planets": planets,
        "fleets": fleets,
    }


# --- Physics helpers ---

def _dist(a: dict, b: dict) -> float:
    return math.sqrt((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2)


def _travel_time(a: dict, b: dict, speed: float = 1.0) -> int:
    return max(1, math.ceil(_dist(a, b) / speed))


def _ships_after_growth(planet: dict, turns: int) -> float:
    return planet["ships"] + planet.get("growth_rate", 1) * turns


# --- Strategy ---

def _score_target(source: dict, target: dict) -> float:
    turns = _travel_time(source, target)
    projected = _ships_after_growth(target, turns)
    needed = math.ceil(projected * 1.1) + 1
    if source["ships"] <= needed:
        return -1.0
    return target.get("growth_rate", 1) / (needed * (1 + turns * 0.1))


def _pick_orders(state: dict) -> List[dict]:
    player = state["player"]
    enemy = 2 if player == 1 else 1
    planets = state["planets"]

    my_planets = [p for p in planets if p.get("owner") == player]
    targets = [p for p in planets if p.get("owner") != player]

    if not targets:
        return []

    orders = []
    for src_idx, src in enumerate(my_planets):
        if src["ships"] < 2:
            continue

        best_score = -1.0
        best_tgt_idx = None
        for tgt_idx, tgt in enumerate(targets):
            s = _score_target(src, tgt)
            if s > best_score:
                best_score = s
                best_tgt_idx = tgt_idx

        if best_tgt_idx is None:
            continue

        tgt = targets[best_tgt_idx]
        ships = int(src["ships"] * 0.6)
        if ships < 1:
            continue

        # Find original planet index in full list
        src_global = next((i for i, p in enumerate(planets) if p is src), None)
        tgt_global = next((i for i, p in enumerate(planets) if p is tgt), None)
        if src_global is None or tgt_global is None:
            continue

        orders.append({
            "type": "fleet",
            "source": src_global,
            "destination": tgt_global,
            "ships": ships,
        })

    return orders


# --- Submission entrypoint (MUST be the last def in this file) ---

def agent(obs: dict) -> dict:
    """
    Kaggle Orbit Wars agent entrypoint.
    Accepts observation dict, returns action dict.
    This is the last def in the file as required by the submission contract.
    """
    try:
        state = _parse_obs(obs)
        orders = _pick_orders(state)
        if not orders:
            return {"orders": []}
        return {"orders": orders}
    except Exception:
        return {"orders": []}
