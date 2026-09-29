"""Evidence records for GitHub Context Bridge.

Evidence IDs are deterministic over the observed role/source/type/payload.
They identify a handoff unit; they do not grant authority.
"""

import hashlib
import json
from typing import Any


PROTOCOL_VERSION = "github-japanese-context-bridge-v0.1"


def evidence_id(role: str, source: str, evidence_type: str, observation: Any) -> str:
    payload = {
        "role": role,
        "source": source,
        "type": evidence_type,
        "observation": observation,
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"ev-{digest[:16]}"


def build_evidence_record(role: str, source: str, evidence_type: str, observation: Any) -> dict:
    return {
        "evidence_id": evidence_id(role, source, evidence_type, observation),
        "protocol_version": PROTOCOL_VERSION,
        "role": role,
        "source": source,
        "type": evidence_type,
        "observation": observation,
    }


def semantic_handoff(context: dict) -> dict:
    """Create a read-only Context handoff envelope.

    The envelope identifies evidence and preserves the Human Gate.
    It is not an authorization object.
    """
    return {
        "handoff_type": "semantic_context",
        "protocol_version": PROTOCOL_VERSION,
        "evidence_ids": [
            item["evidence_id"]
            for item in context.get("evidence", [])
            if item.get("evidence_id")
        ],
        "context": context,
        "authority": {
            "decision": "HUMAN",
            "repository_mutation": False,
        },
    }
