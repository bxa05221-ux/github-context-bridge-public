# Quickstart

GitHub Context Bridge の Public Prototype を、まず5分で試すための最短手順です。

## 1. Clone

```bash
git clone https://github.com/bxa05221-ux/github-context-bridge-public.git
cd github-context-bridge-public
```

## 2. Python

Python 3.10 以降を用意してください。

このPrototypeは、基本的にPython標準ライブラリだけで動く構成です。

## 3. GitHub Token

読み取り専用の GitHub token を `GITHUB_TOKEN` に設定します。

Token には、対象repositoryを読み取るために必要な最小限の権限だけを与えてください。

## 4. 対象repositoryを指定

自分のrepositoryを観測する場合：

```bash
export GITHUB_CONTEXT_REPOSITORY=OWNER/REPOSITORY
```

PowerShell:

```powershell
$env:GITHUB_CONTEXT_REPOSITORY="OWNER/REPOSITORY"
```

## 5. 観測

```bash
python -m src.github_snapshot
```

この段階では GitHub の状態を**読むだけ**です。

Issues / Pull Requests / Commits / files / branches などを取得し、Evidenceへ渡せるsnapshotを作ります。

## 6. Contextを見る

```bash
python -m src.context_bridge
```

Contextでは、役割別観測、Evidence、ThreadRPG、Semantic Handoff、Human Gateまでの公開境界を確認できます。

## 7. 自己観測

```bash
python -m src.self_observe
```

GitHub Context Bridge自身をGitHub Context Bridgeが観測します。

## 5分で見るポイント

1. GitHubの状態が役割別に分かれる
2. EvidenceにIDが付く
3. 根拠がない関係は `UNKNOWN` のまま残る
4. ThreadRPGで複数の観測を横方向に読む
5. 最終判断とrepository変更権限は人間に残る

## 公開境界

このrepositoryはPublic Prototype / 体験版です。

公開ランタイムはThreadRPGのPerspective Layerまでです。より深いShirakami processingや内部Coreは、このrepositoryの公開範囲には含めません。

## 注意

このPrototypeはGitHubを変更する操作を実装していません。

`merge`、`release`、`publish` その他のrepository変更はHuman Gateの外側に置かれます。
