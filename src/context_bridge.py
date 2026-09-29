"""GitHub Context Bridge: read-only role observation builder.

This module deliberately stops at Context generation.
It does not approve, merge, publish, or mutate GitHub state.
"""

from dataclasses import dataclass, asdict
from typing import Any

from src.human_explanation import explain_context, LEVELS, build_user_profile
from src.evidence import build_evidence_record, semantic_handoff
from src.perspectives import build_perspectives


@dataclass
class Observation:
    role: str
    source: str
    type: str
    observation: Any

    def to_evidence(self) -> dict:
        return build_evidence_record(self.role, self.source, self.type, self.observation)


ROLES = {
    "問題・要望担当": "GitHub Issues",
    "プログラム担当": "repository files",
    "変更担当": "GitHub Pull Requests",
    "自動テスト担当": "GitHub Actions",
    "作業履歴担当": "GitHub Commits",
    "事実確認担当": "cross-source verification",
    "ルール担当": "repository protocols",
}


def observe_repository(snapshot: dict) -> list[Observation]:
    """Convert a read-only GitHub snapshot into role observations."""
    return [
        Observation(
            role="問題・要望担当",
            source=ROLES["問題・要望担当"],
            type="FACT",
            observation={
                "issues": snapshot.get("issues", []),
                "count": len(snapshot.get("issues", [])),
            },
        ),
        Observation(
            role="プログラム担当",
            source=ROLES["プログラム担当"],
            type="FACT",
            observation={
                "files": snapshot.get("files", []),
                "implementation_present": any(
                    path.startswith(("src/", "app/"))
                    for path in snapshot.get("files", [])
                ),
            },
        ),
        Observation(
            role="変更担当",
            source=ROLES["変更担当"],
            type="FACT",
            observation={
                "pull_requests": snapshot.get("pull_requests", []),
                "count": len(snapshot.get("pull_requests", [])),
            },
        ),
        Observation(
            role="自動テスト担当",
            source=ROLES["自動テスト担当"],
            type="UNKNOWN",
            observation={
                "workflow_runs": snapshot.get("workflow_runs"),
                "note": "Absent workflow evidence must remain UNKNOWN.",
            },
        ),
        Observation(
            role="作業履歴担当",
            source=ROLES["作業履歴担当"],
            type="FACT",
            observation={
                "commits": snapshot.get("commits", []),
                "count": len(snapshot.get("commits", [])),
            },
        ),
        Observation(
            role="事実確認担当",
            source=ROLES["事実確認担当"],
            type="FACT",
            observation={
                "repository": snapshot.get("repository"),
                "evidence_sources": snapshot.get("evidence_sources", []),
            },
        ),
        Observation(
            role="ルール担当",
            source=ROLES["ルール担当"],
            type="FACT",
            observation={
                "protocol": snapshot.get("protocol"),
            },
        ),
    ]


def hold_maintenance_conference(observations: list[Observation]) -> dict:
    """Assemble 保守安価 without making a decision."""
    return {
        "name": "保守安価",
        "purpose": "integrate observations into human-readable Context",
        "observations": [asdict(item) for item in observations],
        "decision_authority": "HUMAN",
        "human_gate_required": True,
    }


def build_context(snapshot: dict, explanation_level: int = 1, language: str = "ja") -> dict:
    """Build the read-only Context boundary.

    explanation_level changes presentation depth only.
    """
    observations = observe_repository(snapshot)
    conference = hold_maintenance_conference(observations)
    level = max(1, min(5, int(explanation_level)))
    profile = build_user_profile(language=language, explanation_level=level)

    context = {
        "mode": "read_only",
        "runtime_boundary": {
            "profile": "lightweight_core",
            "heavy_use_boundary": True,
            "heavy_use_tasks": [
                "3D位相回転アイゼンハーワーマトリクス",
                "歪天球の数学・幾何処理",
                "大規模Context再構成",
                "深いEvidence比較・検証",
            ],
            "handoff": "semantic_handoff",
            "authority": "HUMAN",
            "repository_mutation": False,
        },
        "action_boundary": {
            "observed_capabilities": [
                "repository_inspection",
                "issue_inspection",
                "pull_request_inspection",
                "workflow_inspection",
                "evidence_comparison",
            ],
            "repository_mutation": False,
            "human_gate_required": True,
        },
        "change_lineage": {
            "pull_requests": snapshot.get("pull_requests", []),
            "causal_chain": snapshot.get("causal_chain", {}),
        },
        "causal_chain": snapshot.get("causal_chain", {
            "issue_to_pr": "UNKNOWN",
            "pr_to_commit": "UNKNOWN",
            "commit_to_workflow": "UNKNOWN",
            "pr_to_merge": "UNKNOWN",
            "workflow_to_merge": "UNKNOWN",
        }),
        "roles": [asdict(item) for item in observations],
        "evidence": [item.to_evidence() for item in observations],
        "保守安価": conference,
        "human_gate": {
            "required": True,
            "authority": "HUMAN",
        },
        "explanation_profile": profile,
        "language": language if language in ("ja", "en") else "ja",
        "human_explanation": explain_context(snapshot, level=level, language=language),
    }
    context["perspectives"] = build_perspectives(context["evidence"])
    context["semantic_handoff"] = semantic_handoff(context)
    return context


if __name__ == "__main__":
    example = {
        "repository": "bxa05221-ux/github-context-bridge",
        "files": ["README.md", "protocols/github-japanese-context-bridge-v0.1.md"],
        "issues": [],
        "pull_requests": [],
        "commits": [],
        "workflow_runs": None,
        "evidence_sources": [],
        "protocol": "github-japanese-context-bridge-v0.1",
    }

    import json
    print(json.dumps(build_context(example), ensure_ascii=False, indent=2))
