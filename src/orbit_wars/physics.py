"""Physics and geometry helpers for Orbit Wars."""

import math
from typing import Tuple

from .observation import Planet


def distance(a: Planet, b: Planet) -> float:
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def travel_time(a: Planet, b: Planet, speed: float = 1.0) -> int:
    """Turns needed for a fleet to travel from a to b."""
    return max(1, math.ceil(distance(a, b) / speed))


def ships_after_growth(planet: Planet, turns: int) -> float:
    """Estimate ships on a planet after N turns (no battles)."""
    return planet.ships + planet.growth_rate * turns


def ships_needed_to_capture(target: Planet, turns: int, safety_margin: float = 1.1) -> int:
    """Minimum ships to capture a planet after `turns` travel, with safety margin."""
    projected = ships_after_growth(target, turns)
    return max(1, math.ceil(projected * safety_margin) + 1)


def net_production(planets, player_id: int) -> float:
    """Total growth rate for all planets owned by player."""
    return sum(p.growth_rate for p in planets if p.owner == player_id)


def total_ships(planets, player_id: int) -> float:
    """Total ships on all planets owned by player."""
    return sum(p.ships for p in planets if p.owner == player_id)
