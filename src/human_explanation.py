"""Human-facing explanation layer for GitHub Context Bridge.

Presentation depth changes the explanation, not the evidence.
The user may move between levels without changing repository authority.
"""

from typing import Any


LANGUAGES = {
    "ja": "日本語",
    "en": "English",
}

LEVELS = {
    1: "plain",
    2: "contextual",
    3: "technical",
    4: "protocol",
    5: "deep",
}


def _count(snapshot: dict[str, Any], key: str) -> int:
    value = snapshot.get(key, [])
    return len(value) if isinstance(value, list) else 0


def _repository_name(snapshot: dict[str, Any]) -> tuple[str, Any, Any]:
    repository = snapshot.get("repository") or {}
    if isinstance(repository, dict):
        return (
            repository.get("full_name") or repository.get("name") or "このプロジェクト",
            repository.get("default_branch"),
            repository.get("private"),
        )
    return str(repository) if repository else "このプロジェクト", None, None


def explain_context(snapshot: dict[str, Any], level: int = 1, language: str = "ja") -> str:
    """Render a read-only snapshot at a user-selected explanation depth.

    Levels affect presentation only. They never change evidence, authority,
    or the Human Gate.
    """
    level = max(1, min(5, int(level)))
    if language == "en":
        return _explain_context_en(snapshot, level)
    name, branch, private = _repository_name(snapshot)

    files = snapshot.get("files", [])
    implementation_present = any(
        isinstance(path, str) and path.startswith(("src/", "app/"))
        for path in files
    )
    issues = _count(snapshot, "issues")
    prs = _count(snapshot, "pull_requests")
    commits = _count(snapshot, "commits")
    workflow_runs = snapshot.get("workflow_runs")

    chain = snapshot.get("causal_chain", {})
    lines = [f"{name} の現在の状態です。"]

    status = []
    if branch:
        status.append(f"基本の作業先は {branch} です")
    if private is True:
        status.append("現在は非公開です")
    elif private is False:
        status.append("現在は公開されています")
    if status:
        lines.append("、".join(status) + "。")

    progress = []
    if implementation_present:
        progress.append("基本的なプログラムは入っています")
    elif files:
        progress.append("ファイルはありますが、実装が入っているかはまだ確認できません")
    if commits:
        progress.append(f"変更履歴は {commits} 件あります")
    if progress:
        lines.append(" ".join(progress) + "。")

    activity = []
    if issues == 0:
        activity.append("問題や要望は、現在確認できる範囲ではありません")
    else:
        activity.append(f"問題や要望が {issues} 件あります")
    if prs == 0:
        activity.append("変更提案は、現在確認できる範囲ではありません")
    else:
        activity.append(f"変更提案が {prs} 件あります")
    lines.append("。".join(activity) + "。")

    if workflow_runs is None:
        lines.append("自動テストの結果は、まだ確認できていません。")
    elif isinstance(workflow_runs, dict):
        total = workflow_runs.get("total_count")
        if total == 0:
            lines.append("自動テストの実行記録は、現在確認できません。")
        else:
            lines.append(f"自動処理の実行記録は {total} 件確認できます。")
    else:
        lines.append("自動テストの状態は、まだ確認できていません。")

    if level >= 2:
        lines.append("変更のつながりは、確認できた範囲と未確認の範囲を分けて扱っています。")
        lines.append(
            "ここまでの説明は、確認できた情報から現在の状態を整理したものです。"
            "確認できていない情報は、推測で補っていません。"
        )

    if level >= 3:
        lines.append(
            "関係: Issue→PR=%s / PR→Commit=%s / Commit→Workflow=%s / PR→Merge=%s / Workflow→Merge=%s" % (
                chain.get("issue_to_pr", "UNKNOWN"),
                chain.get("pr_to_commit", "UNKNOWN"),
                chain.get("commit_to_workflow", "UNKNOWN"),
                chain.get("pr_to_merge", "UNKNOWN"),
                chain.get("workflow_to_merge", "UNKNOWN"),
            )
        )
        lines.append(
            "技術的には、GitHubの観測結果をEvidenceとして扱い、"
            "事実と解釈を分けてContextにまとめます。"
        )
        lines.append(
            "自動テストの記録がない場合は、成功したとは扱わず「UNKNOWN」とします。"
        )

    if level >= 4:
        lines.append(
            "内部では、問題・要望、プログラム、変更、自動テスト、作業履歴、"
            "事実確認、ルールという役割ごとに観測を分けています。"
        )
        lines.append(
            "それらを照合して、人間が確認できるContextにまとめます。"
        )

    if level >= 5:
        lines.append(
            "白神の構造では、LandscapeとしてのGitHubからEvidenceを取り出し、"
            "Protocolに沿ってContextを組み立てます。"
        )
        lines.append(
            "説明の深さが変わっても、Evidenceや権限は変わりません。"
            "変更・公開・マージなどの判断はHuman Gateを通り、人が行います。"
        )

    lines.append(
        f"説明レベル: {level}（{LEVELS[level]}）。"
        "「簡単に」「詳しく」「Evidenceを見せて」などの指定で戻したり深くしたりできます。"
    )
    lines.append(
        "この説明は、確認できたGitHubの状態をまとめたものです。"
        "最終的な変更や公開などの判断は人が行います。"
    )
    return "\n".join(lines)



def _explain_context_en(snapshot: dict[str, Any], level: int) -> str:
    level = max(1, min(5, int(level)))
    name, branch, private = _repository_name(snapshot)
    issues = _count(snapshot, "issues")
    prs = _count(snapshot, "pull_requests")
    commits = _count(snapshot, "commits")
    chain = snapshot.get("causal_chain", {})
    lines = [f"This is the current state of {name}."]
    if branch: lines.append(f"The default branch is {branch}.")
    if private is True: lines.append("The repository is currently private.")
    elif private is False: lines.append("The repository is currently public.")
    lines.append(f"There are {issues} issue(s), {prs} pull request(s), and {commits} recorded commit(s) in the observed snapshot.")
    if snapshot.get("workflow_runs") is None: lines.append("Workflow results have not been confirmed.")
    if level >= 2: lines.append("Confirmed information is separated from unknown information; unknowns are not guessed.")
    if level >= 3:
        lines.append("Lineage: Issue→PR=%s / PR→Commit=%s / Commit→Workflow=%s / PR→Merge=%s / Workflow→Merge=%s." % (chain.get("issue_to_pr", "UNKNOWN"), chain.get("pr_to_commit", "UNKNOWN"), chain.get("commit_to_workflow", "UNKNOWN"), chain.get("pr_to_merge", "UNKNOWN"), chain.get("workflow_to_merge", "UNKNOWN")))
        lines.append("GitHub observations are treated as Evidence and assembled into Context.")
    if level >= 4: lines.append("Observations are separated by role and reconciled into a human-readable Context.")
    if level >= 5: lines.append("In Shirakami terms: GitHub as Landscape → Evidence → Protocol → Context → Human Gate.")
    lines.append(f"Explanation level: {level} ({LEVELS[level]}). Repository-changing decisions remain with a human.")
    return "\n".join(lines)


def build_user_profile(language: str = "ja", explanation_level: int = 1) -> dict[str, Any]:
    """Create a user-controlled presentation profile.

    This profile changes presentation only. It grants no repository authority.
    """
    language = language if language in LANGUAGES else "ja"
    level = max(1, min(5, int(explanation_level)))
    return {
        "language": language,
        "explanation_level": level,
        "level": level,
        "name": LEVELS[level],
        "user_controlled": True,
        "reversible": True,
        "transparent": True,
        "evidence_invariant": True,
        "authority_invariant": True,
    }
