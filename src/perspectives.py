"""Public read-only perspective layer for GitHub Context Bridge.

The public runtime exposes ThreadRPG only. Deeper Shirakami processing stays
in the separate development repository and is not part of this public code.
"""

from __future__ import annotations


def thread_rpg(evidence: list[dict]) -> dict:
    """Expand evidence horizontally while preserving evidence IDs."""
    return {
        "layer": "ThreadRPG",
        "direction": "horizontal",
        "threads": [
            {
                "evidence_id": item.get("evidence_id"),
                "role": item.get("role"),
                "source": item.get("source"),
                "type": item.get("type"),
                "observation": item.get("observation"),
            }
            for item in evidence
        ],
        "authority": {"decision": "HUMAN", "repository_mutation": False},
    }


def build_perspectives(evidence: list[dict]) -> dict:
    """Build the public read-only perspective stack."""
    thread = thread_rpg(evidence)
    return {
        "perspective_stack": {"thread_rpg": thread},
        "order": ["ThreadRPG"],
        "authority": {"decision": "HUMAN", "repository_mutation": False},
    }
