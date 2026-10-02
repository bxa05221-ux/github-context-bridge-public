# Third-Party Repository Observations

ここは、GitHub Context Bridgeを第三者リポジトリの観測・文脈保持・引き継ぎに使った記録を保存する領域です。

## Boundary

- Observation is read-only.
- Evidence and interpretation are separated.
- CONFIRMED and UNKNOWN are kept distinct.
- Similarity does not imply identity or causality.
- Fork ownership and parent-project ownership are kept distinct.
- Repository mutation and final decisions remain outside the observation layer.

## Current observations

- `observations/ecc-2026-09-29.yaml` — Everything Claude Code (ECC) observation.
- `observations/follower-repository-landscape-2026-10-02.yaml` — Initial follower-derived repository landscape.
- `observations/vasuquantdev-octus-bridge-2026-10-02.yaml` — Cross-chain relay; bridge-name similarity explicitly separated from context-bridge similarity.
- `observations/AbSomeone-openspec-moltbot-2026-10-02.yaml` — Fork provenance and AI-coding/spec-driven observations.
- `observations/dbunt1tled-local-rag-2026-10-02.yaml` — Local RAG observation and relation to the same-owner ECC ecosystem.

## Observation rule

The observation layer records what is publicly observable. It does not infer why an author built a project, whether one project influenced another, or whether similar structures share an origin.

The intended handoff unit is:

`Landscape → Observation → Evidence → Comparison → UNKNOWN → Human Gate`

The observation files are records, not authoritative claims about the observed project's intent or runtime behavior.
