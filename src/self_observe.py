"""Run GitHub Context Bridge against its own repository.

This is a read-only self-observation proof. It produces Context; it does not
create issues, PRs, commits, merges, releases, or other GitHub mutations.
"""

import json
import os

from .github_actions import workflow_runs
from .github_snapshot import snapshot
from .context_bridge import build_context


def main() -> None:
    repository = os.environ.get(
        "GITHUB_CONTEXT_REPOSITORY",
        "bxa05221-ux/github-context-bridge-public",
    )
    owner, repo = repository.split("/", 1)
    token = os.environ.get("GITHUB_TOKEN")

    state = snapshot(owner, repo, token)
    state["workflow_runs"] = workflow_runs(owner, repo, token)

    runs_by_sha = {
        run.get("head_sha"): run
        for run in state["workflow_runs"].get("workflow_runs", [])
        if run.get("head_sha")
    }
    chain = state.setdefault("causal_chain", {})
    evidence = chain.setdefault("evidence", [])
    for pr in state.get("pull_requests", []):
        sha = pr.get("head_sha")
        if sha and sha in runs_by_sha:
            chain["commit_to_workflow"] = "CONFIRMED"
            evidence.append({
                "relation": "Commit→Workflow",
                "status": "CONFIRMED",
                "commit_sha": sha,
                "workflow_run_id": runs_by_sha[sha].get("id"),
                "source": runs_by_sha[sha].get("html_url"),
            })
    if chain.get("commit_to_workflow") != "CONFIRMED":
        chain["commit_to_workflow"] = "UNKNOWN"

    context = build_context(state)
    print(json.dumps(context, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
