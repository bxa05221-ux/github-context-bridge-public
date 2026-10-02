# Nine-Model External Observation Protocol v0.1

Status: Public Prototype / non-normative

## Purpose

Provide a deterministic recording format for comparing an externally observed GitHub repository with the Shirakami nine-model overlay.

This protocol records observations. It does not determine authorship, intent, influence, causality, quality, or superiority.

## Nine models

1. Landscape
2. Language Protocol
3. Context
4. Evidence
5. Human Judgment
6. AI Runtime
7. FSM
8. DAG / Agent Runtime
9. Durable Execution

## Required separation

Every observation should distinguish:

- observed — directly supported by an inspected GitHub artifact;
- interpreted — structural interpretation of observed material;
- UNKNOWN — not established by available evidence.

Authorship and causality are independent fields:

- repository_ownership
- fork_status
- upstream_reference
- architecture_authorship
- direct_reference_to_shirakami
- influence
- causal_relationship

UNKNOWN is a valid result and must not be promoted to confirmed by inference.

## Evidence record

Each model observation should retain:

- repository
- ref / commit when available
- path or artifact
- observation
- evidence excerpt or locator
- confidence
- model
- status

## Human review

Automated analysis may organize evidence and propose structural matches.

It may not:

- declare another author's intent;
- declare influence without evidence;
- convert interpretation into fact;
- authorize repository-changing operations.

Final acceptance of an observation remains a Human Gate.

## Minimal flow

GitHub artifact → Observation → Evidence → Nine-model interpretation → UNKNOWN preservation → Human review → Observation record

CONFIRMED means that the underlying relationship is explicitly supported by the retained evidence. It does not mean that the interpretation is necessarily complete.
