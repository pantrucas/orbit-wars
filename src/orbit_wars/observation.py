"""Observation parsing utilities for Orbit Wars."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Planet:
    id: int
    x: float
    y: float
    owner: int  # 0 = neutral, 1 = player, 2 = opponent
    ships: float
    growth_rate: float


@dataclass
class Fleet:
    id: int
    owner: int
    ships: float
    source: int
    destination: int
    turns_remaining: int


@dataclass
class GameState:
    step: int
    player_id: int
    planets: List[Planet] = field(default_factory=list)
    fleets: List[Fleet] = field(default_factory=list)

    @property
    def my_planets(self) -> List[Planet]:
        return [p for p in self.planets if p.owner == self.player_id]

    @property
    def enemy_planets(self) -> List[Planet]:
        enemy_id = 2 if self.player_id == 1 else 1
        return [p for p in self.planets if p.owner == enemy_id]

    @property
    def neutral_planets(self) -> List[Planet]:
        return [p for p in self.planets if p.owner == 0]

    @property
    def my_fleets(self) -> List[Fleet]:
        return [f for f in self.fleets if f.owner == self.player_id]


def parse_observation(obs: dict) -> GameState:
    """Parse the raw observation dict into a typed GameState."""
    step = obs.get("step", 0)
    player_id = obs.get("player", 1)

    planets = []
    for i, p in enumerate(obs.get("planets", [])):
        planets.append(Planet(
            id=i,
            x=float(p.get("x", 0)),
            y=float(p.get("y", 0)),
            owner=int(p.get("owner", 0)),
            ships=float(p.get("ships", 0)),
            growth_rate=float(p.get("growth_rate", 1)),
        ))

    fleets = []
    for i, f in enumerate(obs.get("fleets", [])):
        fleets.append(Fleet(
            id=i,
            owner=int(f.get("owner", 0)),
            ships=float(f.get("ships", 0)),
            source=int(f.get("source", 0)),
            destination=int(f.get("destination", 0)),
            turns_remaining=int(f.get("turns_remaining", 0)),
        ))

    return GameState(step=step, player_id=player_id, planets=planets, fleets=fleets)
