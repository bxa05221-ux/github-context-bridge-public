"""Read-only GitHub Actions adapter.

Workflow state is evidence only. It never authorizes a repository change.
"""

from typing import Any

from .github_snapshot import github_get


def workflow_runs(owner: str, repo: str, token: str | None = None) -> dict[str, Any]:
    """Return recent workflow runs as neutral evidence."""
    data = github_get(
        f"/repos/{owner}/{repo}/actions/runs?per_page=20",
        token,
    )
    runs = []
    for item in data.get("workflow_runs", []):
        runs.append(
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "status": item.get("status"),
                "conclusion": item.get("conclusion"),
                "head_branch": item.get("head_branch"),
                "head_sha": item.get("head_sha"),
                "run_number": item.get("run_number"),
                "html_url": item.get("html_url"),
            }
        )
    return {
        "total_count": data.get("total_count", len(runs)),
        "workflow_runs": runs,
    }
