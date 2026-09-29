"""Read-only Shirakami perspective layers for GitHub Context Bridge.

The layers preserve Evidence rather than replacing it with a conclusion.
ThreadRPG expands observations horizontally while preserving evidence and
decision boundaries. The deeper Shirakami perspective layers are outside the
public GitHub bridge runtime.

The 3D phase-rotation / 歪天球 layer is represented as an explicit boundary
until the canonical mathematical specification is imported. No invented
formula is applied here.
"""

from __future__ import annotations

from typing import Any


def thread_rpg(evidence: list[dict]) -> dict:
    """Expand evidence horizontally by role while preserving evidence IDs."""
    threads = []
    for item in evidence:
        threads.append(
            {
                "evidence_id": item.get("evidence_id"),
                "role": item.get("role"),
                "source": item.get("source"),
                "type": item.get("type"),
                "observation": item.get("observation"),
            }
        )
    return {
        "layer": "ThreadRPG",
        "direction": "horizontal",
        "threads": threads,
        "authority": {"decision": "HUMAN", "repository_mutation": False},
    }


def phase_rotation_eisenhower(evidence: list[dict]) -> dict:
    """Declare the 3D phase-rotation boundary without inventing its formula."""
    return {
        "layer": "3D位相回転アイゼンハワーマトリクス",
        "status": "boundary_only",
        "input_evidence_ids": [item.get("evidence_id") for item in evidence],
        "canonical_formula_required": True,
        "output": None,
        "authority": {"decision": "HUMAN", "repository_mutation": False},
    }


def distorted_sphere(phase_context: dict) -> dict:
    """Declare 歪天球 as the downstream phase-space boundary."""
    return {
        "layer": "歪天球",
        "status": "boundary_only",
        "source_layer": phase_context.get("layer"),
        "source_status": phase_context.get("status"),
        "geometry": None,
        "canonical_formula_required": True,
        "authority": {"decision": "HUMAN", "repository_mutation": False},
    }


def build_perspectives(evidence: list[dict]) -> dict:
    """Build the complete read-only perspective stack."""
    phase = phase_rotation_eisenhower(evidence)
    thread = thread_rpg(evidence)
    sphere = distorted_sphere(phase)
    return {
        "perspective_stack": {
            "thread_rpg": thread,
            "phase_rotation_eisenhower": phase,
            "distorted_sphere": sphere,
        },
        "order": [
            "3D位相回転アイゼンハワーマトリクス",
            "歪天球",
            "ThreadRPG",
        ],
        "authority": {
            "decision": "HUMAN",
            "repository_mutation": False,
        },
    }
