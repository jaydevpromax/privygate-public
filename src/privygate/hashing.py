"""Hash helpers used by the PrivyGate prototype."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> str:
    """Return deterministic JSON for hashing and audit IDs."""

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_hex(*parts: Any) -> str:
    hasher = hashlib.sha256()
    for part in parts:
        if isinstance(part, bytes):
            data = part
        else:
            data = canonical_json(part).encode("utf-8")
        hasher.update(len(data).to_bytes(8, "big"))
        hasher.update(data)
    return hasher.hexdigest()


def hash_scalar(order: int, *parts: Any) -> int:
    value = int(digest_hex(*parts), 16) % order
    return value or 1


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

