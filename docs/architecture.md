# Agent Architecture

## Overview

```
observation (dict)
      │
      ▼
 parse_observation()     — src/orbit_wars/observation.py
      │
      ▼
  GameState              — typed: planets, fleets, player_id
      │
      ▼
 baseline_orders()       — src/orbit_wars/strategy.py
      │  uses physics helpers (distance, travel_time, ships_needed)
      ▼
  orders (list of dicts)
      │
      ▼
 build_action()          — src/orbit_wars/actions.py
      │
      ▼
 action (dict)           — returned to Kaggle environment
```

## Submission Entrypoint

`submission/main.py` contains a self-contained copy of the agent.
The last `def agent(obs)` is the Kaggle entrypoint.
It must have zero external dependencies beyond the Python standard library.

## Strategy: Baseline

Greedy heuristic:
- For each owned planet with ships > 1:
  - Score all non-owned planets by: `growth_rate / (ships_needed * (1 + turns * 0.1))`
  - Send 60% of available ships to the highest-scoring target.

## Planned Improvements

- [ ] Multi-step lookahead
- [ ] Fleet interception
- [ ] Defensive reinforcement under attack
- [ ] Growth-rate prioritization
- [ ] RL self-play (experimental)

## Files

| File | Role |
|---|---|
| `src/orbit_wars/observation.py` | Parse obs dict → GameState |
| `src/orbit_wars/actions.py` | Build action dicts |
| `src/orbit_wars/physics.py` | Distance, travel time, projections |
| `src/orbit_wars/strategy.py` | Strategy decisions → orders |
| `src/orbit_wars/agent.py` | Combine all into decide() |
| `src/orbit_wars/evaluation.py` | Local tournament runner |
| `submission/main.py` | Self-contained Kaggle submission |
