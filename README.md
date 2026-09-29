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

## Design principle

> Do not translate only the words. Preserve the context that makes the words meaningful.

言葉だけを翻訳するのではなく、**その言葉が意味を持つためのContextを保つ。**

---

**GitHub Context Bridge — 読める。根拠が残る。判断は人間にある。**
