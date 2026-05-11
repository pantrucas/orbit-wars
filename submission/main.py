"""
Orbit Wars — Kaggle submission entrypoint.

Observation format (obs dict):
  obs["planets"]: list of [id, owner, x, y, radius, ships, production]
  obs["fleets"]:  list of [id, owner, x, y, angle, from_planet_id, ships]
  obs["player"]:  int — player ID (0-3)
  obs["angular_velocity"]: float — radians/turn
  obs["remainingOverageTime"]: float

Action format (return value):
  [[from_planet_id, angle_radians, num_ships], ...]
  Return [] for no action.

No internet. No file I/O. No credentials.
Last def in this file is the Kaggle entrypoint.
"""

import math

# Planet list indices
_PID = 0; _POWN = 1; _PX = 2; _PY = 3; _PRAD = 4; _PSHIPS = 5; _PPROD = 6

# Fleet list indices
_FID = 0; _FOWN = 1; _FX = 2; _FY = 3; _FANGLE = 4; _FFROM = 5; _FSHIPS = 6

_MAX_SPEED = 6.0
_BOARD = 100.0


def _dist(ax, ay, bx, by):
    return math.sqrt((bx - ax) ** 2 + (by - ay) ** 2)


def _angle_to(sx, sy, tx, ty):
    return math.atan2(ty - sy, tx - sx)


def _fleet_speed(ships):
    """Speed = 1 + (maxSpeed-1) * (log(ships)/log(1000))^1.5"""
    if ships <= 1:
        return 1.0
    return 1.0 + (_MAX_SPEED - 1.0) * (math.log(ships) / math.log(1000)) ** 1.5


def _travel_turns(dist, ships):
    speed = _fleet_speed(ships)
    return max(1, math.ceil(dist / speed))


def _incoming_enemy_ships(planet_id, fleets, player):
    """Sum ships in enemy fleets heading toward this planet (approximate by from_planet)."""
    total = 0
    for f in fleets:
        if f[_FOWN] != player and f[_FFROM] != planet_id:
            # We can't know exact destination from angle alone cheaply;
            # use a rough heuristic: ignore for now
            pass
    return total


def _score_target(src, tgt, player):
    """Return score for sending a fleet from src to tgt. Higher = better."""
    if tgt[_POWN] == player:
        return -1.0

    sx, sy = src[_PX], src[_PY]
    tx, ty = tgt[_PX], tgt[_PY]
    d = _dist(sx, sy, tx, ty)
    ships_available = src[_PSHIPS]
    ships_to_send = max(1, int(ships_available * 0.6))
    turns = _travel_turns(d, ships_to_send)

    # Project how many ships target will have when fleet arrives
    projected = tgt[_PSHIPS] + tgt[_PPROD] * turns
    needed = math.ceil(projected * 1.1) + 1

    if ships_to_send <= needed:
        return -1.0

    # Score: production gained per ship invested, discounted by distance
    return tgt[_PPROD] / (needed * (1.0 + d * 0.02))


def _reinforce_threatened(my_planets, fleets, player):
    """
    Detect own planets under threat (enemy fleets nearby) and reinforce
    from the richest adjacent friendly planet.
    Returns list of [source_id, angle, ships] orders.
    """
    orders = []
    if len(my_planets) < 2:
        return orders

    # Planets with very few ships relative to production are exposed
    exposed = [p for p in my_planets if p[_PSHIPS] < p[_PPROD] * 3]
    rich = [p for p in my_planets if p[_PSHIPS] > 20]

    for tgt in exposed:
        if not rich:
            break
        # Pick closest rich planet that isn't the target itself
        donors = sorted(
            [p for p in rich if p[_PID] != tgt[_PID]],
            key=lambda p: _dist(p[_PX], p[_PY], tgt[_PX], tgt[_PY])
        )
        if not donors:
            continue
        src = donors[0]
        ships = int(src[_PSHIPS] * 0.3)
        if ships < 2:
            continue
        angle = _angle_to(src[_PX], src[_PY], tgt[_PX], tgt[_PY])
        orders.append([src[_PID], angle, ships])
        rich = [p for p in rich if p[_PID] != src[_PID]]  # don't reuse same donor

    return orders


def _attack_orders(my_planets, all_planets, player):
    """Greedy attack: each planet with enough ships attacks best target."""
    targets = [p for p in all_planets if p[_POWN] != player]
    if not targets:
        return []

    orders = []
    for src in my_planets:
        if src[_PSHIPS] < 4:
            continue

        best_score = -1.0
        best_tgt = None
        for tgt in targets:
            s = _score_target(src, tgt, player)
            if s > best_score:
                best_score = s
                best_tgt = tgt

        if best_tgt is None:
            continue

        ships = max(1, int(src[_PSHIPS] * 0.6))
        angle = _angle_to(src[_PX], src[_PY], best_tgt[_PX], best_tgt[_PY])
        orders.append([src[_PID], angle, ships])

    return orders


def _merge_orders(attack, reinforce):
    """Combine orders; skip reinforce if source already scheduled an attack."""
    used = {o[0] for o in attack}
    merged = list(attack)
    for o in reinforce:
        if o[0] not in used:
            merged.append(o)
    return merged


def agent(obs):
    """
    Orbit Wars agent entrypoint.
    Receives observation dict, returns list of [planet_id, angle_rad, ships].
    This is the last def in the file as required by the Kaggle submission contract.
    """
    try:
        planets = obs["planets"]
        fleets = obs["fleets"]
        player = obs["player"]

        my_planets = [p for p in planets if p[_POWN] == player]
        if not my_planets:
            return []

        attack = _attack_orders(my_planets, planets, player)
        reinforce = _reinforce_threatened(my_planets, fleets, player)
        return _merge_orders(attack, reinforce)

    except Exception:
        return []
