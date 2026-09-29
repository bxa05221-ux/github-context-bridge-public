# GitHub Context Bridge

**GitHubを「読む」ことから、GitHubを「対話で扱う」ことへ。**

GitHub Context Bridge は、GitHub の repository state（リポジトリの状態）を、会話を通して人間が理解しやすくするための Public Prototype です。

このPrototypeは、GitHubを単に日本語へ翻訳するのではなく、**誰が何を観測し、何を根拠として言えるのか**を保ったまま、GitHubの情報を日本語で読み解けるようにすることを目指しています。

## 5分で試す

まず試してみたい方は、[QUICKSTART.md](QUICKSTART.md) を参照してください。

最短の流れは次のとおりです。

```
GitHub
  ↓
役割別観測
  ↓
Evidence（根拠）
  ↓
ThreadRPG
  ↓
Semantic Handoff
  ↓
人間
  ↓
必要ならGitHub操作
```

このPrototypeは**読み取り専用**です。GitHubの状態を観測・整理・説明しますが、merge、release、publishなどのrepository変更を自動で実行するものではありません。

## このPrototypeで見えるもの

### 1. 役割別に読む

GitHub上の情報を、役割ごとの観測として整理します。

- **問題・要望担当** — Issues / requests
- **プログラム担当** — Code / implementation
- **変更担当** — Pull Requests / proposed changes
- **自動テスト担当** — CI / workflow results
- **作業履歴担当** — Commits / change history
- **事実確認担当** — Evidence / unknowns
- **ルール担当** — Protocol / specification
- **最終判断** — Human

複数の役割から得られた観測は、Evidenceとして保持されます。

### 2. Evidenceを残す

「そう見える」ことと「GitHub上の根拠がある」ことを分けます。

GitHubから明示的に確認できる関係は `CONFIRMED` として扱い、根拠が足りない関係は `UNKNOWN` のまま残します。

つまり、

> 分からないものを、分かったことにしない。

これがこのPrototypeの重要な境界です。

### 3. ThreadRPGで読む

ThreadRPGは、複数の観測を横方向につなげて読むための公開Perspective Layerです。

ここで重要なのは、ThreadRPGが最終判断をするわけではないことです。

**観測を読みやすくすることと、判断することを分離します。**

### 4. 説明の深さを変える

同じContextを、必要に応じて異なる深さで読むことができます。

```
Level 1  plain       → 普通の日本語で理解
Level 2  contextual  → なぜそう言えるか
Level 3  technical   → Evidence / 技術構造
Level 4  protocol    → 担当者構造 / Evidence
Level 5  deep        → Context / Protocol / Human Gate
```

説明の深さや言語を変えても、EvidenceやHuman Gateの意味は変わりません。

これは**表示方法の変更であって、権限の変更ではありません。**

## 言語について

現在のPrototypeでは、日本語（`ja`）と英語（`en`）を扱えます。

ここでの言語切り替えは、あくまでPresentation Layerです。

```
Repository
   ↓
Evidence / Context
   ↓
言語 + 説明レベル
   ↓
人間向けの説明
```

日本語にしたからといって、Evidenceが変わったり、repositoryを変更する権限が発生したりすることはありません。

## Change Lineage（変更の流れ）

GitHub上で確認できる情報から、変更に関係するartifactのつながりを読み取ります。

```
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

明示的な根拠がある関係は `CONFIRMED`、根拠が足りない関係は `UNKNOWN` として扱います。

このPrototypeは、artifactの並びから因果関係を勝手に推測しません。

## Human Gate

GitHub Context Bridgeでは、

**AIが情報を整理しても、決定権は人間に残ります。**

AIは観測・説明・比較・整理を支援できます。

しかし、説明したこと自体がmerge、release、publishなどの許可になることはありません。

## Public Boundary

このrepositoryは、GitHub Context Bridgeの**Public Prototype / 体験版**です。

公開版では、GitHubを読み、Evidenceを保持し、ThreadRPGで体験するところまでを公開します。

より深いShirakami processingや内部Coreは、このrepositoryの公開範囲には含めません。

これは「内部Coreが存在しない」という意味ではなく、**公開範囲を意図的に分けている**ということです。

## Shirakamiとの関係

GitHub Context Bridgeは、白神モデルの考え方をGitHubという具体的な環境に適用する独立したアプリケーション実験です。

白神モデル側のContext、Evidence、Protocol、Semantic Handoff、Verification、Human Gateなどの考え方を、GitHubの観測・説明・引き継ぎに適用しています。

## Self-observation

このPrototypeには、GitHub Actionsを含むGitHubの状態を読み取るためのadapterと、自己観測runnerがあります。

```
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
```

GitHub Context Bridge自身を、GitHub Context Bridgeで観測することもできます。

Actionsの情報が確認できない場合、それを「成功」とは解釈せず、Evidenceが不足している状態として扱います。

## 開発状況

**Early-stage prototype / specification work**

このrepositoryは、まず「実際に触ってみる」ための公開入口です。

実験的・内部向けの開発は別repositoryで行い、このrepositoryには公開対象だけを置きます。

---

# English

**From “reading” GitHub to “working with GitHub” through conversation.**

GitHub Context Bridge is a Public Prototype for making GitHub repository state easier for people to understand through conversation.

The goal is not simply to translate GitHub into another language. The Prototype preserves **who observed what, what evidence supports a statement, and what remains unknown**, so that repository state can be explained without silently turning interpretation into fact.

## Try it in 5 minutes

Start with [QUICKSTART.md](QUICKSTART.md).

The shortest path is:

```
GitHub
  ↓
Role-based observation
  ↓
Evidence
  ↓
ThreadRPG
  ↓
Semantic Handoff
  ↓
Human
  ↓
GitHub operation, if needed
```

The Prototype is **read-only**. It observes, organizes, and explains GitHub state, but it does not automatically perform repository-changing operations such as merge, release, or publish.

## What the Prototype shows

### 1. Read GitHub through roles

GitHub information is organized as observations associated with different roles.

- **Problem / Request role** — Issues and requests
- **Program role** — Code and implementation
- **Change role** — Pull Requests and proposed changes
- **Automation / Test role** — CI and workflow results
- **Work History role** — Commits and change history
- **Fact-checking role** — Evidence and unknowns
- **Rules role** — Protocol and specification
- **Final decision** — Human

Observations from multiple roles are preserved as Evidence.

### 2. Preserve Evidence

The Prototype separates “this appears to be the case” from “there is evidence for this in GitHub.”

Relationships explicitly supported by GitHub evidence are represented as `CONFIRMED`. When the available evidence is insufficient, the relationship remains `UNKNOWN`.

In other words:

> Do not turn what is unknown into what is known.

This is one of the Prototype's fundamental boundaries.

### 3. Read through ThreadRPG

ThreadRPG is the public Perspective Layer for reading multiple observations horizontally as connected threads.

It does not make the final decision.

**Making observations easier to read and making decisions are deliberately separated.**

### 4. Change explanation depth

The same Context can be presented at different levels of explanation.

```
Level 1  plain       → Understand the state in ordinary language
Level 2  contextual  → Understand why the statement can be made
Level 3  technical   → Evidence / technical structure
Level 4  protocol    → Role structure / Evidence
Level 5  deep        → Context / Protocol / Human Gate
```

Changing language or explanation depth does not change the Evidence or the Human Gate.

This is a **presentation change, not an authorization change**.

## Language

The current Prototype supports Japanese (`ja`) and English (`en`).

Language selection belongs to the Presentation Layer.

```
Repository
   ↓
Evidence / Context
   ↓
Language + explanation level
   ↓
Human-readable explanation
```

Changing the language does not change the Evidence or grant permission to modify the repository.

## Change Lineage

The Prototype reads relationships among GitHub artifacts when those relationships can be established from available evidence.

```
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

Relationships supported by explicit evidence are `CONFIRMED`. Relationships for which the available evidence is insufficient remain `UNKNOWN`.

The Prototype does not infer causality merely from the sequence of artifacts.

## Human Gate

In GitHub Context Bridge:

**AI may organize information, but decision authority remains with the human.**

AI can help observe, explain, compare, and organize evidence.

However, explaining an operation does not authorize a merge, release, publish, or other repository-changing action.

## Public Boundary

This repository is the **Public Prototype / experience version** of GitHub Context Bridge.

The public version exposes the experience of reading GitHub, preserving Evidence, and reading the result through ThreadRPG.

Deeper Shirakami processing and internal Core are outside the publication boundary of this repository.

This does **not** mean that the internal Core does not exist. It means that the publication boundary is intentional.

## Relationship to Shirakami

GitHub Context Bridge is an independent application experiment applying ideas from the Shirakami model to a concrete GitHub environment.

It applies concepts such as Context, Evidence, Protocol, Semantic Handoff, Verification, and Human Gate to GitHub observation, explanation, and handoff.

## Self-observation

The Prototype includes an adapter for reading GitHub state, including GitHub Actions, and a self-observation runner.

```
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
```

GitHub Context Bridge can observe GitHub Context Bridge itself.

When workflow information cannot be established, the system does not interpret that absence as success. The Evidence remains insufficient.

## Status

**Early-stage prototype / specification work**

This repository is intended as the public entry point for people who want to try the Prototype.

Experimental and internal development remains in a separate repository so that internal development history is not exposed through this public repository.

---

**GitHub Context Bridge — Readable. Evidence preserved. Decisions remain human.**
