# Architecture Decision Records MINDRA

## Назначение

Этот каталог хранит значимые архитектурные решения MINDRA. ADR создаётся, когда выбор влияет на module boundaries, contracts, ownership, runtime/training/evaluation semantics или исследовательскую валидность.

Статусы: `proposed`, `accepted`, `superseded`, `superseded in part`, `rejected`.

Research result не меняет design автоматически: сначала interpretation/design review.

---

# Реестр

## Accepted

- [`ADR-0001`](ADR-0001-logical-boundaries-independent-of-deployment.md) — логические границы независимы от deployment topology.
- [`ADR-0002`](ADR-0002-explicit-composition-no-runtime-service-locator.md) — explicit Composition Root; runtime Service Locator запрещён.
- [`ADR-0003`](ADR-0003-hierarchical-logical-time.md) — иерархическое logical time и causal commit boundaries.
- [`ADR-0004`](ADR-0004-versioned-committed-cognitive-state.md) — versioned committed `CognitiveState` вместо mutable bus.
- [`ADR-0005`](ADR-0005-wave-scheduled-module-protocol.md) — DAG scheduling, execution waves и atomic module commit.
- [`ADR-0006`](ADR-0006-separated-evidence-plane-and-intervention-gateway.md) — passive Evidence Plane отдельно от Intervention Gateway.
- [`ADR-0007`](ADR-0007-two-plane-environment-boundary.md) — Agent Interaction Plane отдельно от Environment Research Plane.
- [`ADR-0008`](ADR-0008-hybrid-canonical-percept.md) — hybrid Canonical Percept: structured semantic core + optional feature views.
- [`ADR-0009`](ADR-0009-committed-goal-graph.md) — committed Goal Graph с proposal/adoption boundary.
- [`ADR-0010`](ADR-0010-capability-negotiated-cortex-gateway.md) — capability-negotiated Cortex Gateway и backend adapters.
- [`ADR-0011`](ADR-0011-canonical-memory-records-derived-indexes.md) — canonical Memory Records отдельно от derived representations/indexes.
- [`ADR-0012`](ADR-0012-belief-state-world-model.md) — belief-state World Model с раздельными assimilation/prediction/imagination.
- [`ADR-0013`](ADR-0013-hybrid-functional-self-model.md) — functional Self Model: capability facts + competence + calibrated predictions.
- [`ADR-0014`](ADR-0014-multi-provider-intrinsic-signal-layer.md) — multi-provider Intrinsic Signals без mandatory scalarization.
- [`ADR-0015`](ADR-0015-typed-stateful-drive-system.md) — typed stateful Drive System без global motivation scalar.
- [`ADR-0016`](ADR-0016-multidimensional-event-centered-appraisal.md) — event-centered multidimensional Appraisal.
- [`ADR-0017`](ADR-0017-typed-persistent-affect-state.md) — typed persistent Affect с explicit history-dependent dynamics.
- [`ADR-0018`](ADR-0018-typed-multi-objective-valuation.md) — typed multi-objective Valuation с explicit comparison/scalarization boundary.
- [`ADR-0019`](ADR-0019-budgeted-contextual-salience-allocation.md) — contextual Salience Profiles + explicit budgeted Attention Allocation.
- [`ADR-0020`](ADR-0020-source-preserving-budget-aware-memory-regulation.md) — source-preserving budget-aware Memory Regulation с gated consolidation.
- [`ADR-0021`](ADR-0021-bounded-broadcast-workspace-overlay.md) — bounded source-preserving broadcast Workspace overlay с first-class `NoWorkspace`, matched controls и explicit negative module gate.
- [`ADR-0022`](ADR-0022-proposal-driven-budget-aware-executive-control.md) — proposal-driven budget-aware Executive Control поверх invariant Scheduler, с explicit MetaAction proposals, resource envelope и equal-compute negative gate.
- [`ADR-0023`](ADR-0023-policy-owned-selection-optional-planner.md) — Policy-owned final behavioral selection с optional/falsifiable Planner provider и explicit selected-intent boundary перед Action Gate.
- [`ADR-0024`](ADR-0024-post-authorization-pre-dispatch-action-commit.md) — mandatory Action authorization boundary и `Action Commit` после финальной authorization, но до dispatch; explicit override provenance и retry/idempotency semantics.
- [`ADR-0025`](ADR-0025-causal-experience-journal-derived-projections.md) — append-only causal `Experience Journal` как source of truth записанного опыта + versioned derived trajectory/dataset/training projections.
- [`ADR-0026`](ADR-0026-candidate-revision-validated-activation-training-lifecycle.md) — external Training Runtime обучает pinned base revisions в candidate state; validation предшествует атомарной activation совместимого Agent revision bundle.
- [`ADR-0027`](ADR-0027-manifest-driven-causal-checkpoint-restore.md) — manifest-driven causal checkpoint: explicit capture boundary, content/integrity artifacts, restore profiles и scoped reproducibility guarantees.

## Proposed

Нет.

## Rejected

Нет самостоятельных ADR со статусом `rejected`; отклонённые альтернативы сохранены внутри соответствующих ADR.

## Superseded

Нет.

---

# Правило изменения design

```text
research evidence
→ interpretation/design review
→ ADR
→ canonical design owner
→ contracts/status/version plans
→ implementation
```

Не оставлять два одновременно действующих противоречащих решения.
