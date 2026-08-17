# ADR-0026 — Candidate revisions + validation + atomic activation для Training Lifecycle

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-26 — Training Lifecycle`

---

# 1. Контекст

После `DU-25` MINDRA имеет воспроизводимую data boundary:

```text
Experience Journal
→ DatasetManifest
→ TrainingSample
→ ReplaySelection
```

Нужно определить, как training изменяет trainable parameters Agent.

Критические требования:

- Training Runtime не должен стать частью ordinary cognition;
- optimizer state не должен жить в `CognitiveState`;
- online learning не должен менять параметры посреди Decision Window;
- source behavior revision должна сохраняться;
- representation-breaking update должен быть видимым;
- joint component updates должны активироваться совместимо;
- failed update не должен портить live Agent;
- rollback должен сохранять causal history.

---

# 2. Вариант A — In-place optimizer внутри live modules

Conceptually:

```text
module.compute()
→ loss
→ backward
→ optimizer.step()
→ те же weights сразу изменены
```

## Плюсы

- максимально просто для prototype;
- мало revision/artifact machinery;
- близко к обычному training loop.

## Минусы

- cognition и training смешиваются;
- optimizer state получает скрытый ownership внутри modules;
- невозможно надёжно установить, какая revision породила конкретный action;
- mid-decision mutation разрушает causal replay;
- rollback/validation сложны;
- joint updates могут создавать несовместимые промежуточные состояния;
- training failures способны напрямую повредить live Agent.

**Решение:** отклонён как canonical architecture.

---

# 3. Вариант B — Training Runtime обновляет live parameters напрямую между steps

Conceptually:

```text
external Trainer
→ optimizer.step(live_model.parameters)
→ новая версия становится активной немедленно
```

## Плюсы

- Training Runtime уже отделён от cognition;
- проще distributed actor/learner;
- меньше candidate/activation infrastructure.

## Минусы

- граница между candidate и active отсутствует;
- validation выполняется постфактум;
- asynchronous update может попасть внутрь in-flight Decision Window;
- трудно атомарно обновить несколько coupled components;
- rollback всё ещё сложен;
- representation migration может запоздать относительно активации.

**Решение:** отклонён как canonical default.

Допустим лишь как concrete optimization implementation **внутри isolated candidate model**, не как live activation semantics.

---

# 4. Вариант C — Candidate revision → validation → atomic activation

Conceptually:

```text
Active Agent A17
        │
        └── pinned base
                ↓
          Training Runtime
                ↓
      CandidateRevisionBundle C18
                ↓
           Validation
           /        \
        reject      accept
                      ↓
             LearningUpdateRecord
                      ↓
             RevisionActivation
                      ↓
               Active Agent A18
```

## Плюсы

- live cognition отделена от training mutation;
- можно отклонить плохой candidate без повреждения Agent;
- source/base revisions однозначны;
- joint component update можно активировать атомарно;
- representation migration/compatibility можно проверить заранее;
- online learner и actor могут иметь разные revisions без ambiguity;
- rollback становится явной revision activation, а не rewrite history;
- TrainingSample → LearningUpdate lineage сохраняется.

## Минусы

- больше manifests/artifacts;
- требуется candidate storage/model copy или эквивалентная staging semantics;
- больше lifecycle machinery;
- hot activation требует version-compatible runtime design.

**Решение:** принято.

---

# 5. Вариант D — Полная retrain/restart Agent после каждого update

Conceptually:

```text
collect data
→ train offline
→ stop Agent
→ restart from new checkpoint
```

## Плюсы

- очень чистая revision boundary;
- легко реализовать в раннем prototype;
- нет mid-decision mutation.

## Минусы

- не выражает будущий online/interleaved learning;
- restart становится обязательным architecture invariant;
- плохо поддерживает long-lived sessions;
- не решает общую semantics candidate/validation/rollback.

**Решение:** не принят как canonical architecture.

Это допустимый **ранний implementation mode** поверх варианта C: safe activation boundary может оказаться restart/episode boundary.

---

# 6. Принятое решение

MINDRA использует:

> **Training Runtime вне cognition, который обучает pinned base revisions в staging/candidate state, создаёт `CandidateRevisionBundle`, проходит explicit validation и только затем атомарно активирует совместимый `AgentRevisionManifest` на допустимой causal boundary.**

Дополнительно:

1. `LearningUpdate ≠ RuntimeStateUpdate ≠ ConsolidationEvent ≠ ReplayStep`;
2. optimizer/trainer state принадлежит Training Runtime;
3. `TrainingPlan` явно определяет trainable groups, objective, data visibility, optimizer/gradient policy и validation;
4. runtime dependency graph не определяет gradient graph;
5. candidate revision не является active revision;
6. in-flight cognition pin'ит старую active revision;
7. mixed behavior/learner revisions разрешены и явно описываются;
8. privileged supervision требует отдельной маркировки;
9. representation-breaking update не активируется скрыто;
10. rollback создаёт новый causal activation, не стирая предыдущий update.

---

# 7. Training objective и internal motivation

ADR отдельно фиксирует:

```text
Training Objective
≠ Agent Goal
≠ ValueProfile
≠ Intrinsic Signal
≠ Drive
≠ External Feedback автоматически
```

Любой mapping внутренних/внешних сигналов в loss/target является explicit training configuration.

---

# 8. Joint optimization

Если несколько components обучаются совместно и их revisions взаимозависимы:

```text
Component A candidate
+
Component B candidate
→ one CandidateRevisionBundle
→ atomic activation group
```

Не допускается промежуточная live composition, если compatibility manifest считает её недопустимой.

---

# 9. Online actor/learner

Decoupled online architecture разрешена.

Она обязана сохранять:

```text
behavior_revision
learner_revision
policy lag / compatibility
source sample provenance
```

Конкретная off-policy correction определяется algorithm/version design, а не этим ADR.

---

# 10. Cortex adaptation

ADR не выбирает full fine-tuning или adapters.

Допустимы:

```text
frozen base
adapter-only
partial/full trainable Cortex
```

при соблюдении одной lifecycle semantics candidate → validation → activation.

---

# 11. Consequences

Положительные:

- causally clean online learning;
- reproducible attribution revisions;
- safe validation/rollback;
- compatible joint updates;
- явный representation drift;
- Training Runtime остаётся внешним Agent cognition;
- concrete ML stack может меняться.

Цена:

- больше manifests/revisions;
- candidate artifacts требуют storage;
- activation/compatibility tooling нужно реализовать;
- ранний prototype может использовать упрощённый stop-train-restart режим.

---

# 12. Falsification / review conditions

ADR следует пересмотреть, если implementation evidence покажет, что staging/candidate revision overhead непрактичен даже для минимального prototype и более простая граница может сохранить все ключевые invariants.

Упрощение не может терять:

```text
no hidden optimizer in cognition
base revision provenance
no mid-decision mutation
failed update does not corrupt live Agent
privileged supervision explicit
representation compatibility explicit
rollback history preserved
```

---

# 13. Связанные документы

- [`../training-lifecycle.md`](../training-lifecycle.md)
- [`../contracts/training-lifecycle.md`](../contracts/training-lifecycle.md)
- [`../experience-data-replay.md`](../experience-data-replay.md)
- [`../execution-model.md`](../execution-model.md)
- [`../cognitive-state.md`](../cognitive-state.md)
