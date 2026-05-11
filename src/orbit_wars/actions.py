"""Action building utilities for Orbit Wars."""

from typing import List, Optional


def send_fleet(source_id: int, destination_id: int, ships: int) -> dict:
    """Build a fleet dispatch action."""
    return {
        "type": "fleet",
        "source": source_id,
        "destination": destination_id,
        "ships": ships,
    }


def no_op() -> dict:
    """Build a no-operation action."""
    return {"type": "noop"}


def build_action(orders: List[dict]) -> dict:
    """Wrap a list of fleet orders into the submission action format."""
    return {"orders": orders}


def clamp_ships(ships: float, available: float, min_ships: int = 1) -> Optional[int]:
    """Return integer ship count clamped to available, or None if not enough."""
    n = int(min(ships, available))
    return n if n >= min_ships else None
