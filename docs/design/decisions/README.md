# Architecture Decision Records MINDRA

## Назначение

Этот каталог предназначен для значимых архитектурных решений MINDRA.

ADR создаётся, когда существует несколько реалистичных вариантов, а выбор влияет на module boundaries, internal contracts, state ownership, training semantics, reproducibility, evaluation validity, runtime topology или future version design.

ADR не нужен для каждой локальной implementation detail.

---

# Статусы

- `proposed` — решение подготовлено для review;
- `accepted` — решение принято и является частью текущего design;
- `superseded` — полностью заменено более новым ADR;
- `superseded in part` — частично заменено/уточнено;
- `rejected` — вариант рассмотрен и явно не принят.

---

# Обязательная структура ADR

1. Контекст.
2. Проблема/decision scope.
3. Требования и constraints.
4. Рассмотренные варианты.
5. Evidence/references, если применимо.
6. Принятое решение.
7. Последствия и trade-offs.
8. Что решение намеренно не определяет.
9. Какие canonical design/contracts/version docs должны быть обновлены.

---

# Правила

Если ADR меняет ранее принятый design:

```text
ADR
→ canonical design owner
→ exact internal contracts
→ version plans/status
→ implementation
```

Не оставлять два одновременно действующих противоречащих решения.

Rejected/superseded ADR сохраняются как история reasoning проекта.

Research experiment сам по себе не становится ADR: сначала проводится interpretation/design review.

---

# Реестр

## Accepted

- [`ADR-0001 — Логические границы независимы от deployment topology`](ADR-0001-logical-boundaries-independent-of-deployment.md) — архитектурная принадлежность определяется responsibility/state ownership, а не процессом, устройством или compute provider.
- [`ADR-0002 — Явная композиция и запрет runtime Service Locator`](ADR-0002-explicit-composition-no-runtime-service-locator.md) — concrete implementations разрешаются в Composition Root; потребители получают зависимости явно и не ищут их через глобальный runtime container/registry.
- [`ADR-0003 — Иерархическое логическое время и причинные commit boundaries`](ADR-0003-hierarchical-logical-time.md) — MINDRA различает внешнее и внутреннее логическое время, допускает несколько Cognitive Cycle на одно действие и отделяет causal order от wall-clock/physical concurrency.
- [`ADR-0004 — Версионированный committed CognitiveState вместо общего mutable bus`](ADR-0004-versioned-committed-cognitive-state.md) — canonical shared state представлен committed snapshots; изменения публикуются через owner-scoped staged updates и новую state revision, а hidden inplace mutation/`last-write-wins` запрещены.
- [`ADR-0005 — DAG scheduling с execution waves и атомарным module commit`](ADR-0005-wave-scheduled-module-protocol.md) — module dependencies компилируются в DAG/waves; modules одной wave читают одну committed revision, а public/private effects становятся видимыми только через согласованный atomic commit.
- [`ADR-0006 — Разделить passive Evidence Plane и explicit Intervention Gateway`](ADR-0006-separated-evidence-plane-and-intervention-gateway.md) — observability остаётся однонаправленной passive evidence boundary, а active research mutation проходит только через отдельный explicit Intervention Gateway с target/base/provenance и experimental lineage.
- [`ADR-0007 — Разделить agent-visible Environment interaction и research-only world control`](ADR-0007-two-plane-environment-boundary.md) — общий Environment contract имеет отдельные Agent Interaction Plane и Research Plane; `MicroWorld` является reference family, а privileged world state/snapshot/intervention не становятся обычным Agent input.
- [`ADR-0008 — Гибридный Canonical Percept: structured semantic core + optional feature views`](ADR-0008-hybrid-canonical-percept.md) — Perception публикует structured Semantic Core с provenance/missingness и optional revisioned Feature Views; один universal latent и Cortex hidden space не являются canonical inter-module representation.
- [`ADR-0009 — Committed Goal Graph с явной proposal/adoption boundary`](ADR-0009-committed-goal-graph.md) — внешние, внутренние, planner и research sources создают Goal Proposal; только Goal System принимает committed Goal state и владеет lifecycle/Goal Graph, не смешивая цель с reward/value/policy.
- [`ADR-0010 — Capability-negotiated Cortex Gateway с backend-specific adapter boundary`](ADR-0010-capability-negotiated-cortex-gateway.md) — consumers используют backend-neutral semantic Cortex request/result boundary; model-specific prompt/tokenizer/provider и optional research capabilities изолированы за adapter/provider layer.
- [`ADR-0011 — Canonical Memory Records отдельно от derived representations/indexes`](ADR-0011-canonical-memory-records-derived-indexes.md) — Memory Store хранит stable source-preserving records; embeddings и retrieval indexes являются versioned derived structures и не определяют semantic identity памяти.
- [`ADR-0012 — Belief-state World Model с раздельными assimilation, prediction и imagination semantics`](ADR-0012-belief-state-world-model.md) — partial observability выражается через World Belief; actual evidence update отделён от action-conditioned prediction/imagination, а backend latent не становится universal representation.
- [`ADR-0013 — Гибридная функциональная Self Model: capability facts + learned competence + calibrated predictions`](ADR-0013-hybrid-functional-self-model.md) — self-observable capability facts отделены от learned context-conditioned competence; Self Prediction имеет explicit target/calibration semantics и не заменяется Cortex self-report.
- [`ADR-0014 — Многопровайдерный Intrinsic Signal Layer без обязательной scalarization`](ADR-0014-multi-provider-intrinsic-signal-layer.md) — novelty, prediction discrepancy, information gain, competence change и другие signal families остаются typed independent outputs; общий intrinsic reward не является canonical boundary.
- [`ADR-0015 — Typed stateful Drive System без global motivation scalar`](ADR-0015-typed-stateful-drive-system.md) — persistent typed drive states имеют единый owner, homeostatic и adaptive dynamics остаются разными semantics, cross-drive coupling explicit, а Drive не scalarize мотивацию и не получает Goal/Policy authority.
- [`ADR-0016 — Event-centered multidimensional Appraisal без обязательной emotion/utility scalarization`](ADR-0016-multidimensional-event-centered-appraisal.md) — Appraisal оценивает causally identified target относительно revisioned Agent context через typed dimensions; emotion label/global valence/utility не являются canonical output.

## Proposed

Нет.

## Rejected

Нет самостоятельных ADR со статусом `rejected`.

Отклонённые альтернативы сохранены внутри соответствующих ADR.

## Superseded

Нет.
