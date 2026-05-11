# Rules Snapshot — Orbit Wars

Snapshot taken: 2026-05-10
Source: https://www.kaggle.com/competitions/orbit-wars/rules

## Verified Rules

- One Kaggle account per participant.
- Team size: maximum 5 members.
- Daily submission limit: 5 per day.
- Final submissions: latest 2 are used.
- Competition data license: Apache 2.0.
- External data/models/LLMs/AutoML: allowed if reasonably accessible and not excessively costly.
- Private code sharing with other teams: forbidden.
- Open-source dependencies: must allow commercial use.
- Winning solution must be reproducible and documented.
- Winning code license: CC-BY 4.0 (except documented third-party exceptions).
- During evaluation: no internet, no external info, no exfiltration.
- Replays: may become public and reveal agent actions.

## Verified Submission Format

**Format:** Single `main.py` OR a `zip`/`gz`/`7z` archive with `main.py` at the top level.

**Entrypoint:** The **last `def`** in the submitted file must accept an observation and return an action.

```python
def agent(obs):
    return action
```

## Notes

Always verify current rules on the official Kaggle competition page before final submissions.
Rules may be updated during the competition.
