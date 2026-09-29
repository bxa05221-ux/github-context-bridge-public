"""Minimal read-only GitHub API adapter.

Authentication is supplied through GITHUB_TOKEN.
No write endpoint is used by this module.
"""

import json
import os
import re
import urllib.request
from typing import Any


API_ROOT = "https://api.github.com"


def github_get(path: str, token: str | None = None) -> Any:
    request = urllib.request.Request(
        f"{API_ROOT}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def snapshot(owner: str, repo: str, token: str | None = None) -> dict:
    """Read repository state and return a neutral snapshot."""
    base = f"/repos/{owner}/{repo}"

    repository = github_get(base, token)
    tree = github_get(f"{base}/git/trees/{repository.get('default_branch')}?recursive=1", token)
    issues = github_get(f"{base}/issues?state=all&per_page=100", token)
    pulls = github_get(f"{base}/pulls?state=all&per_page=100", token)
    commits = github_get(f"{base}/commits?per_page=20", token)

    pull_details = [github_get(f"{base}/pulls/{item.get('number')}", token) for item in pulls]
    pull_files = {
        item.get("number"): github_get(
            f"{base}/pulls/{item.get('number')}/files?per_page=100", token
        )
        for item in pull_details
    }
    pull_reviews = {
        item.get("number"): github_get(
            f"{base}/pulls/{item.get('number')}/reviews?per_page=100", token
        )
        for item in pull_details
    }
    issue_links = []
    for item in pull_details:
        body = item.get("body") or ""
        matches = re.findall(r"(?i)(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)", body)
        for number in matches:
            issue_links.append({
                "relation": "Issue→PR",
                "status": "CONFIRMED",
                "issue": int(number),
                "pr": item.get("number"),
                "source": item.get("html_url"),
            })
    branches = github_get(f"{base}/branches?per_page=100", token)

    return {
        "repository": {
            "full_name": repository.get("full_name"),
            "private": repository.get("private"),
            "default_branch": repository.get("default_branch"),
        },
        "files": [
            item.get("path") for item in tree.get("tree", []) if item.get("type") == "blob"
        ],
        "issues": [
            {"number": item.get("number"), "title": item.get("title")}
            for item in issues if "pull_request" not in item
        ],
        "pull_requests": [
            {
                "number": item.get("number"),
                "title": item.get("title"),
                "state": item.get("state"),
                "merged": item.get("merged"),
                "head_sha": item.get("head", {}).get("sha"),
                "base_sha": item.get("base", {}).get("sha"),
                "merge_commit_sha": item.get("merge_commit_sha"),
                "body": item.get("body"),
                "html_url": item.get("html_url"),
                "changed_files": [
                    {
                        "filename": file.get("filename"),
                        "status": file.get("status"),
                        "additions": file.get("additions"),
                        "deletions": file.get("deletions"),
                    }
                    for file in pull_files.get(item.get("number"), [])
                ],
                "reviews": [
                    {"state": review.get("state"), "submitted_at": review.get("submitted_at")}
                    for review in pull_reviews.get(item.get("number"), [])
                ],
            }
            for item in pull_details
        ],
        "branches": [
            {"name": item.get("name"), "protected": item.get("protected")} for item in branches
        ],
        "commits": [
            {"sha": item.get("sha"), "message": (item.get("commit") or {}).get("message")}
            for item in commits
        ],
        "workflow_runs": None,
        "evidence_sources": [
            f"{API_ROOT}{base}", f"{API_ROOT}{base}/contents", f"{API_ROOT}{base}/issues",
            f"{API_ROOT}{base}/pulls", f"{API_ROOT}{base}/commits",
        ],
        "protocol": "github-japanese-context-bridge-v0.1",
        "causal_chain": {
            "issue_to_pr": "CONFIRMED" if issue_links else "UNKNOWN",
            "pr_to_commit": "CONFIRMED" if any(item.get("head", {}).get("sha") for item in pull_details) else "UNKNOWN",
            "commit_to_workflow": "UNKNOWN",
            "pr_to_merge": "CONFIRMED" if any(
                item.get("merged") is True and item.get("merge_commit_sha") for item in pull_details
            ) else "UNKNOWN",
            "workflow_to_merge": "UNKNOWN",
            "evidence": issue_links + [
                {
                    "relation": "PR→Commit",
                    "status": "CONFIRMED" if item.get("head", {}).get("sha") else "UNKNOWN",
                    "pr": item.get("number"),
                    "commit_sha": item.get("head", {}).get("sha"),
                    "source": item.get("html_url"),
                }
                for item in pull_details
            ],
        },
    }


if __name__ == "__main__":
    repository = os.environ.get(
        "GITHUB_CONTEXT_REPOSITORY",
        "bxa05221-ux/github-context-bridge-public",
    )
    owner, repo = repository.split("/", 1)
    data = snapshot(owner, repo, os.environ.get("GITHUB_TOKEN"))
    print(json.dumps(data, ensure_ascii=False, indent=2))
