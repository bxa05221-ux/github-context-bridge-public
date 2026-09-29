# GitHub Context Bridge

**GitHubを「読む」ことから、GitHubを「対話で扱う」ことへ。**

GitHub Context Bridge is an application experiment for making GitHub repository state understandable through conversation.

It is designed around role-based observation, evidence separation, a public perspective layer called **ThreadRPG**, and a Human Gate that keeps final decisions with the human.

## Core flow

```
GitHub
  ↓
役割別観測
  ↓
Evidence
  ↓
ThreadRPG
  ↓
Semantic Handoff
  ↓
人間
  ↓
必要ならGitHub操作
```

This repository is the **clean public entry point** for GitHub Context Bridge. Experimental and heavy-use development remains in the separate development repository.

## Design principle

> Do not translate only the words. Preserve the context that makes the words meaningful.

This project is not intended to replace GitHub, its documentation, or human judgment.

AI may observe, explain, compare, and organize evidence. It does not become the decision authority.

## Human-readable roles

- **問題・要望担当** — Issues and requests
- **プログラム担当** — Code and implementation
- **変更担当** — Pull Requests and proposed changes
- **自動テスト担当** — CI / workflow results
- **作業履歴担当** — Commits and change history
- **事実確認担当** — Evidence and unknowns
- **ルール担当** — Protocol and specification alignment
- **最終判断** — Human decision

When several roles are involved, their observations are preserved as parallel evidence in **ThreadRPG**. Agreement, disagreement, missing evidence, and items requiring human confirmation remain visible.

## Progressive explanation

The same Context can be presented at different depths without changing its evidence or authority.

```
Level 1  plain       → 状態を普通の日本語で理解
Level 2  contextual  → なぜそう言えるか
Level 3  technical   → Evidence / 技術構造
Level 4  protocol    → 担当者構造 / Evidence
Level 5  deep        → Context / Protocol / Human Gate
```

The user controls the depth and can move back and forth. A change in explanation depth is a **presentation handoff**, not an authorization handoff.

For example:

- 「簡単に」 → Level 1
- 「もう少し詳しく」 → Level 2
- 「Evidenceを見せて」 → Level 3
- 「担当者の構造を見せて」 → Level 4
- 「内部構造まで見せて」 → Level 5

The bridge records this distinction explicitly so that learning the system does not accidentally grant the system authority.

## User presentation profile

The bridge keeps a user-controlled presentation profile separate from repository state.

```yaml
language: ja
explanation_level: 1
user_controlled: true
evidence_invariant: true
authority_invariant: true
```

The profile is a UI preference, not a permission model. It may change language or explanation depth, but it cannot authorize merge, release, publication, or other repository-changing actions.

## Language-aware explanation

The bridge treats language as a presentation choice, not an evidence boundary.

```text
Repository
   ↓
Evidence / Context
   ↓
User-selected language + explanation depth
   ↓
Human-readable explanation
```

The same Context can be presented in different languages without changing Evidence, UNKNOWN states, role observations, or Human Gate requirements.

Current prototype languages:
- `ja` — 日本語
- `en` — English

Additional languages can be added as presentation profiles without changing the underlying Evidence or Human Gate.

This is intentionally modeled as a presentation handoff. Changing language or explanation depth does not grant repository-changing authority.

## Change lineage

The bridge also reconstructs a read-only **change lineage** from GitHub evidence.

```text
Issue
  ↓
Pull Request
  ↓
Commit
  ↓
Workflow
  ↓
Merge
```

Where GitHub provides explicit evidence, the relationship is recorded as `CONFIRMED`. When the available evidence does not establish the relationship, it remains `UNKNOWN`.

For pull requests, the bridge can preserve evidence such as:

- explicit Issue references in the PR description;
- PR head and base commits;
- changed files;
- review states;
- workflow runs matched by commit SHA;
- merge state and merge commit.

The lineage is descriptive, not causal speculation. It does not turn a sequence of GitHub artifacts into an approval or recommendation.

## Public boundary

The public runtime intentionally stops at the ThreadRPG perspective layer.

```text
Evidence
   ↓
ThreadRPG
   ↓
Semantic Handoff
   ↓
Human Gate
```

Deeper Shirakami processing remains outside this public repository. This is a publication boundary, not a claim about the broader Shirakami model.

## Relationship to Shirakami

This repository is an independent application experiment derived from the Shirakami model.

Shirakami provides the broader concepts of Context, Evidence, Protocol, Semantic Handoff, Verification, and Human Gate. This repository applies those ideas specifically to GitHub.

## Status

Early-stage prototype / specification work.

The development repository remains separate so experimental/internal history is not exposed through this public repository's Git history.


## Self-observation proof

The bridge now contains a read-only GitHub Actions adapter and a self-observation runner.

The intended execution is:

    GITHUB_TOKEN=... python -m src.self_observe

The runner reads the repository, issues, pull requests, commits, and recent GitHub Actions workflow runs, then passes those observations through the role layer into a read-only Context.

It does not create or modify GitHub state.

The repository can therefore begin testing the bridge against itself: **GitHub Context Bridge observes GitHub Context Bridge.**

### Implementation boundary

    GitHub API
       ↓
    github_snapshot.py / github_actions.py
       ↓
    Role Observation
       ↓
    ThreadRPG
       ↓
    Semantic Handoff
       ↓
    Context
       ↓
    Human Gate

The Actions adapter is intentionally separate from the base snapshot adapter so that absence of workflow evidence remains `UNKNOWN` rather than being interpreted as a passing state.
