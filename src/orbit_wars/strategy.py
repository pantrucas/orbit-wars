"""Strategy decision-making for Orbit Wars."""

from typing import List, Optional, Tuple

from .observation import GameState, Planet
from .physics import distance, travel_time, ships_needed_to_capture, net_production
from .actions import send_fleet, clamp_ships


def score_target(source: Planet, target: Planet, game: GameState, speed: float = 1.0) -> float:
    """Score a potential capture target. Higher is better."""
    turns = travel_time(source, target, speed)
    needed = ships_needed_to_capture(target, turns)
    if source.ships <= needed:
        return -1.0
    # Reward: growth rate per ship spent, penalised by distance
    return target.growth_rate / (needed * (1 + turns * 0.1))


def pick_best_target(source: Planet, candidates: List[Planet], game: GameState) -> Optional[Planet]:
    """Return the highest-scoring capture target from source."""
    scored = [(score_target(source, t, game), t) for t in candidates]
    scored = [(s, t) for s, t in scored if s > 0]
    if not scored:
        return None
    return max(scored, key=lambda x: x[0])[1]


def dispatch_order(source: Planet, target: Planet, game: GameState, send_ratio: float = 0.6) -> Optional[dict]:
    """Build a fleet dispatch order from source to target, sending send_ratio of available ships."""
    ships_to_send = clamp_ships(source.ships * send_ratio, source.ships)
    if ships_to_send is None:
        return None
    return send_fleet(source.id, target.id, ships_to_send)


def baseline_orders(game: GameState) -> List[dict]:
    """
    Greedy baseline strategy:
    - Each owned planet with enough ships attacks the best available target.
    Targets include neutral and enemy planets.
    """
    orders = []
    all_targets = game.neutral_planets + game.enemy_planets

    if not all_targets:
        return orders

    for planet in game.my_planets:
        if planet.ships < 2:
            continue
        target = pick_best_target(planet, all_targets, game)
        if target is None:
            continue
        order = dispatch_order(planet, target, game)
        if order is not None:
            orders.append(order)

    return orders
