# ADR-0025 — Append-only causal Experience Journal + derived projections

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-25 — Experience / Data / Replay`

---

# 1. Контекст

После `DU-24` MINDRA имеет богатую причинную историю:

```text
observation
→ cognition
→ candidate / Policy selection
→ authorization
→ Action Commit
→ dispatch
→ execution / Environment Transition
→ outcome
```

Кроме обычных interaction steps существуют:

- несколько Cognitive Cycle на одно действие;
- module/wave attempts;
- Executive decisions;
- planning/imagination;
- intervention/counterfactual branches;
- `Action Commit` без Environment Transition;
- `execution_unknown` и partial execution;
- changing `agent_revision`;
- Agent Memory Replay;
- future Training Replay/Learning Updates.

Нужно выбрать canonical source data representation, не мешая при этом обычному RL/sequence training.

---

# 2. Требования

Решение должно:

- сохранять полную causal history без принудительного `(s,a,r,s')`;
- позволять action commit без next state;
- поддерживать actual/imagined/replayed/counterfactual/intervened provenance;
- разделять agent-visible и evaluator-only data;
- поддерживать derived RL/sequence datasets;
- сохранять revision provenance;
- не смешивать Agent Memory и Training Replay;
- поддерживать hindsight/relabeling без rewrite source;
- позволять storage/backend evolution;
- быть практически реализуемым на домашнем/Colab prototype.

---

# 3. Вариант A — Transition table как source of truth

Conceptually:

```text
observation_t
action_t
reward_t
next_observation
terminated
truncated
```

## Плюсы

- очень просто;
- совместимо с большинством RL tooling;
- удобно для offline RL.

## Минусы

- теряет Policy candidate/intent/authorization/commit distinctions;
- плохо выражает несколько Cognitive Cycle;
- не представляет action commit без Environment transition;
- `execution_unknown` приходится fabricatе как fake transition или удалять;
- imagination/replay/intervention provenance быстро превращается в дополнительные ad-hoc columns;
- hidden evaluator annotations легко смешиваются с `info`;
- derived relabeling начинает выглядеть как source history.

**Решение:** отклонён как canonical source of truth.

Transition representation остаётся важным derived view.

---

# 4. Вариант B — Только event log, без materialized projections

Conceptually:

```text
append-only events
→ каждый consumer самостоятельно собирает нужные sequences/transitions
```

## Плюсы

- максимальная причинная точность;
- удобно хранить failure/reconciliation;
- легко расширять event kinds;
- source immutable.

## Минусы

- каждый training/evaluation consumer повторяет сложную reconstruction логику;
- трудно добиться единой semantics windowing/relabeling;
- offline RL tooling ожидает episodes/transitions;
- риск разных трактовок одного и того же event stream;
- дорого читать full journal для каждого minibatch.

**Решение:** отклонён как полный data architecture.

Event Journal принят только вместе с canonical derived projections/manifests.

---

# 5. Вариант C — Append-only causal journal + versioned derived projections

Conceptually:

```text
Experience Journal
        ↓
ProjectionSpec
        ↓
Episode / Decision / Interaction views
        ↓
SampleTransformationRecord
        ↓
TrainingSample
        ↓
Training Replay
```

## Плюсы

- source causal history сохраняется;
- обычные RL/sequence formats остаются доступны;
- hindsight/relabeling явно derived;
- action without transition поддерживается естественно;
- schema evolution локализована;
- privileged annotations можно держать отдельной веткой;
- replay buffer не становится archival truth;
- разные training tasks получают разные projections из одного source.

## Минусы

- больше IDs/manifests;
- нужен projection builder;
- storage/index implementation сложнее простого transition buffer;
- consistency source ↔ projection нужно тестировать.

**Решение:** принято.

---

# 6. Вариант D — Общий Agent Memory / Experience / Replay buffer

Conceptually:

```text
one big buffer
├── Agent recalls from it
├── Trainer samples from it
└── Evaluator reads it
```

## Плюсы

- минимальное число storage abstractions;
- простая ранняя реализация.

## Минусы

- Training Replay начинает менять/определять Agent Memory;
- evaluator-only fields рискуют стать agent-visible;
- eviction training buffer становится cognitive forgetting;
- Memory retrieval count и training sample frequency смешиваются;
- трудно делать чистые ablations Memory;
- нарушает `DU-11/20` ownership.

**Решение:** отклонён.

Физически разные logical stores могут позже использовать один backend, но ownership/semantics остаются разными.

---

# 7. Принятое решение

MINDRA использует:

> **append-only causal `Experience Journal` как source of truth для записанного опыта и versioned derived projections/samples для training/evaluation/tool compatibility.**

Дополнительно:

1. `TraceEvent ≠ ExperienceEvent`;
2. source event immutable по смыслу;
3. physical append order не определяет causal order;
4. primary experience и evaluator-only annotations разделены;
5. derived sample всегда имеет transformation lineage;
6. hindsight/relabeling никогда не переписывает source;
7. Training Replay sampling работает поверх source/derived samples, а не становится source history;
8. Agent Memory Replay остаётся отдельной agent-owned причинной линией;
9. unresolved execution сохраняется без fake transition;
10. storage implementation остаётся открытой.

---

# 8. Почему не просто RLDS/Minari schema

Episode/step datasets являются полезным interoperability target.

Но MINDRA должна дополнительно выразить:

```text
policy candidates
selected intent
authorization
action commit
dispatch attempts
execution_unknown
multiple cognitive cycles
executive/planner evidence
interventions
revision bundles
```

Поэтому standard episode/step structure подходит как projection/export, но не как полный canonical journal.

---

# 9. Data Plane и runtime

Этот ADR **не принимает event sourcing как runtime architecture Agent**.

```text
Experience Journal
→ external evidence/data plane

CognitiveState / private state
→ normal Agent runtime state
```

Полный restore/checkpoint определяется `DU-27`, а не reconstruction всего Agent из journal с нуля.

---

# 10. Privileged annotations

Evaluator/Environment Research Plane outputs не кладутся в primary agent-visible payload «для удобства».

Используется отдельный `ResearchAnnotationRecord`.

Dataset builder включает такие данные только при explicit privileged `DataVisibilityPolicy`.

Это делает leakage detectable и auditable.

---

# 11. Replay

Replay buffer/table является:

```text
derived / mutable training infrastructure
```

а не:

```text
source Experience Store
```

Удаление replay item не удаляет original experience.

Replay priority не становится Memory salience/Valuation автоматически.

---

# 12. Consequences

Положительные:

- можно честно хранить full MINDRA causal chain;
- один source dataset поддерживает разные training views;
- transition-only tooling остаётся возможным;
- raw history защищена от relabeling;
- data leakage легче анализировать;
- failure/unknown states не теряются;
- schema evolution и re-encoding становятся explicit transformations.

Цена:

- больше metadata и manifests;
- требуется tooling для projections/validation;
- version design должен выбрать простой practical storage backend;
- тесты должны проверять lineage/integrity.

---

# 13. Falsification / review conditions

ADR должен быть пересмотрен, если implementation evidence покажет, что:

- journal overhead делает prototype непрактичным даже при минимальной core schema;
- projections невозможно стабильно воспроизводить;
- event semantics не дают дополнительной диагностической/causal ценности против более простой representation;
- выбранная граница создаёт больше ambiguity, чем устраняет.

Однако упрощение должно сохранять ключевые invariants:

```text
source history immutable
privileged data separate
relabeling derived
unknown execution expressible
Memory Replay ≠ Training Replay
revision provenance preserved
```

---

# 14. Связанные документы

- [`../experience-data-replay.md`](../experience-data-replay.md)
- [`../contracts/experience-data-replay.md`](../contracts/experience-data-replay.md)
- [`../execution-model.md`](../execution-model.md)
- [`../observability-and-intervention.md`](../observability-and-intervention.md)
- [`../modules/memory-regulation.md`](../modules/memory-regulation.md)
- [`../modules/action-boundary.md`](../modules/action-boundary.md)
