# GitHub Context Bridge Public Protocol v0.1

## 1. Purpose

GitHub Context Bridge presents GitHub repository state as human-readable context.
It does not mechanically translate words; it preserves evidence, uncertainty,
and the boundary between explanation and human decision.

```text
GitHub
  ↓
Observation
  ↓
Evidence
  ↓
ThreadRPG
  ↓
Semantic Handoff
  ↓
Human Gate
```

The human remains the decision authority.

## 2. Scope

The public prototype is read-only. It may observe:

- repository metadata;
- files and implementation;
- issues;
- pull requests;
- commits;
- workflow / CI results;
- reviews and changed files where available.

It produces explanations and structured Context without changing repository state.

## 3. Evidence boundary

Observations are classified so that the bridge does not silently turn one kind
of information into another:

- FACT — directly observed information;
- INTERPRETATION — contextual explanation;
- UNKNOWN — not established by available evidence;
- ACTION — an operation that may exist, not permission to perform it;
- HUMAN_GATE — a decision reserved for the human.

If evidence is missing, the public runtime keeps the state as UNKNOWN.

## 4. Evidence IDs and Semantic Handoff

Each observation is materialized as an Evidence record with a deterministic
evidence_id. The identifier tracks the observation across the handoff; it
does not grant authority.

The handoff envelope preserves:

```yaml
handoff_type: semantic_context
protocol_version: github-context-bridge-public-v0.1
evidence_ids:
  - "ev-..."
authority:
  decision: HUMAN
  repository_mutation: false
```

## 5. Public perspective boundary

The public runtime exposes ThreadRPG as its current perspective layer.

ThreadRPG keeps observations visible in parallel while preserving their
Evidence IDs and uncertainty.

```text
Evidence
   ↓
ThreadRPG
   ↓
Semantic Handoff
   ↓
Human Gate
```

The public protocol intentionally stops at this layer. Deeper processing is
outside the public runtime and is not required to use this bridge.

## 6. Human Gate

The bridge may explain repository state and describe available operations.
It does not turn explanation into authorization.

```text
Observed GitHub state
       ↓
Evidence
       ↓
ThreadRPG
       ↓
Semantic Handoff
       ↓
Human judgment
       ↓
Optional repository operation
```

The current public runtime declares:

```yaml
mode: read_only
action_boundary:
  repository_mutation: false
  human_gate_required: true
```

## 7. Presentation

Language and explanation depth are presentation choices. Changing them must not
change Evidence, UNKNOWN states, or Human Gate requirements.

Current prototype languages:

- ja — 日本語
- en — English

Additional languages can be added as presentation profiles without changing
the underlying Evidence or authority boundary.

The prototype supports progressive explanation levels from plain status to
technical/protocol detail. The level is user-controlled and reversible.

## 8. Change lineage

The bridge may reconstruct descriptive relationships among GitHub artifacts:

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

A relationship is recorded as CONFIRMED only when available evidence
establishes it. Otherwise it remains UNKNOWN. The sequence is descriptive;
it is not approval or causal speculation.

## 9. Non-goals

The public protocol does not attempt to:

- replace GitHub or its documentation;
- become a general-purpose translation system;
- grant AI authority over repository decisions;
- conceal uncertainty behind fluent language;
- execute repository-changing operations from the read-only runtime.

## 10. Core principle

> Do not translate only the words. Preserve the context that makes the words meaningful.

The public bridge is a practical GitHub entry point: lightweight to try,
explicit about evidence, and bounded by human authority.