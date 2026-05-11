"""General utilities for Orbit Wars."""

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: dict, path: str, indent: int = 2) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)


def timestamp() -> str:
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)
