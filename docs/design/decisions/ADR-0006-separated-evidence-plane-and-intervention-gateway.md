# ADR-0006 — Разделить passive Evidence Plane и explicit Intervention Gateway

## Статус

`accepted`

## Контекст

MINDRA должна одновременно:

- позволять глубоко наблюдать внутреннее исполнение;
- поддерживать causal intervention;
- сохранять модульную изоляцию;
- не превращать evaluator/logger в скрытую часть cognition;
- обеспечивать воспроизводимую provenance natural и intervened trajectories.

`DU-01` уже отделил Evaluation Runtime и Artifact infrastructure от Agent. `DU-04` ввёл committed state revisions и provenance. `DU-05` ввёл module attempts, execution waves и atomic commit.

Теперь требуется определить, каким образом исследователь получает evidence и каким образом активное вмешательство может изменять систему.

---

## Проблема

Наивный общий hook/event механизм способен смешать две совершенно разные операции:

```text
«посмотреть значение»
```

и

```text
«заменить значение»
```

Если один callback API одновременно выполняет tracing, debugging и mutation:

- passive observation перестаёт быть гарантированно passive;
- сложно доказать отсутствие evaluator leakage;
- write authority становится неявным;
- natural и treatment trajectories могут смешиваться;
- backend hooks начинают определять архитектуру;
- causal intervention трудно отличить от случайного debug-side effect.

---

## Требования

Решение должно:

1. сохранять однонаправленную observability boundary;
2. позволять фиксировать module/wave/state causal events;
3. поддерживать private-state research probes без ambient mutable access;
4. поддерживать controlled intervention в canonical/private/backend targets;
5. сохранять provenance intervention;
6. не менять semantic owner target;
7. позволять counterfactual branch/fork;
8. не требовать конкретного telemetry framework;
9. не делать raw Cortex activations обязательными;
10. позволять отличить instrumentation failure от Agent failure.

---

## Рассмотренные варианты

### Вариант A — единый универсальный callback/hook bus

Observer регистрирует callbacks на module/state событиях; callbacks могут как читать, так и изменять значения.

Плюсы:

- простая реализация;
- гибкость;
- похоже на распространённые framework hooks.

Минусы:

- observation и mutation имеют одну boundary;
- легко получить скрытый side effect;
- сложно контролировать write authority;
- backend-specific hooks протекают в research architecture;
- intervention provenance становится дисциплиной пользователя, а не invariant системы.

**Отклонено как каноническая модель.**

---

### Вариант B — глобальный event bus с подписчиками

Все runtime события публикуются в общий bus, а evaluator/logger/intervention handlers подписываются на них.

Плюсы:

- слабая связанность producers/consumers;
- удобно подключать diagnostics.

Минусы:

- при bidirectional handlers bus легко превращается в hidden Service Locator/control plane;
- порядок подписчиков может начать влиять на semantics;
- difficult-to-audit side effects;
- конфликтует с `DU-02`, если cognitive/runtime code начинает искать/вызывать dynamic subscribers.

**Отклонено как единая execution/intervention модель.** Event-like export внутри Evidence Plane остаётся допустимой implementation detail.

---

### Вариант C — passive Evidence Plane + отдельный explicit Intervention Gateway

Agent/runtime публикует read-only evidence outward. Evaluation Runtime выполняет mutation только через отдельный privileged gateway с target/base revision/provenance.

Плюсы:

- observation по умолчанию гарантированно passive;
- intervention очевидно отличается от logging;
- естественно сочетается с committed state revisions;
- natural/treatment provenance является частью architecture semantics;
- private/backend intervention можно расширять через explicit capabilities;
- telemetry backend остаётся заменяемым.

Минусы:

- больше типов контрактов;
- нужно отдельно проектировать probes и intervention adapters;
- некоторые framework hooks придётся оборачивать, а не использовать напрямую как архитектурный API.

**Принято.**

---

### Вариант D — полное event sourcing всего Agent как единственный observation/intervention mechanism

Любое внутреннее изменение представляется event, а intervention — вставкой/заменой event в журнале.

Плюсы:

- очень богатая causal history;
- потенциально сильный replay.

Минусы:

- чрезмерно тяжёлый fundamental constraint;
- module-private neural/backend state плохо укладывается в полное event sourcing;
- не заменяет full snapshot stochastic state;
- заставляет research logging определять runtime representation.

**Отклонено как обязательная архитектура.** Event logs могут использоваться как evidence artifact.

---

## Принятое решение

MINDRA использует две различные logical boundaries.

### 1. Passive Evidence Plane

```text
Agent/runtime
    ↓ copies/events/probes
Evidence Plane
    ↓
Artifact Collector / Evaluation analysis
```

Характеристики:

- однонаправленный normal flow;
- отсутствие write authority;
- structured causal tracing;
- metrics/diagnostic artifacts;
- declared private-state probes;
- opt-in backend/raw observability.

### 2. Explicit Intervention Gateway

```text
Evaluation Runtime
      ↓
Intervention Gateway
      ↓ validated target/base/provenance
Agent experimental boundary
      ↓
intervened revision / branch
```

Intervention:

- имеет explicit identity;
- применяется на declared causal boundary;
- не меняет semantic owner target;
- маркирует resulting lineage;
- по умолчанию для confirmatory causal experiments выполняется на fork/branch от identifiable committed base;
- не маскируется под natural module result.

---

## Последствия

### Положительные

- tracing можно включать без предоставления evaluator mutation rights;
- research code не становится runtime Service Locator;
- natural и treatment data можно фильтровать по provenance;
- observability backend можно менять независимо;
- backend-specific activation interventions остаются локальными adapters;
- появляется основа для causal MINDRA-Eval.

### Отрицательные

- потребуется отдельный probe/intervention contract;
- exact counterfactual fork всё равно зависит от будущего полного `Agent Snapshot` и Environment clone/restore;
- large activation capture потребует специальных storage/capture policies;
- passive instrumentation всё равно может иметь physical overhead, который нужно учитывать в real-time experiments.

---

## Evidence и существующие подходы

При проектировании учитывались следующие факты:

- OpenTelemetry разделяет traces, metrics и logs и использует correlation context для восстановления распределённого выполнения;
- PyTorch module hooks позволяют наблюдать intermediate execution, но forward/pre-forward hooks способны модифицировать input/output, а global hooks добавляют global state и документированы как debugging/profiling mechanism;
- библиотека pyvene демонстрирует отдельный abstraction layer для конфигурируемых interventions во внутренние состояния PyTorch models;
- современные исследования causal intervention указывают, что сильные internal interventions могут создавать divergent/out-of-distribution representations, поэтому intervention validity должна быть частью interpretation.

Эти источники подтверждают реализуемость выбранных требований, но не фиксируют конкретную зависимость проекта.

---

## Что решение намеренно не определяет

- OpenTelemetry dependency;
- concrete tracing library;
- exact event/span schema;
- exact private probe interface;
- exact intervention Python API;
- concrete raw activation adapter;
- full Agent Snapshot format;
- Environment fork API;
- statistical estimator causal effect;
- artifact storage backend.

---

## Обновляемые канонические документы

Принятие ADR требует согласованности с:

- `docs/design/observability-and-intervention.md`;
- `docs/design/current.md`;
- `docs/design/README.md`;
- `docs/design/glossary.md`;
- `docs/design/decisions/README.md`;
- `AGENTS.md`;
- `docs/design/contracts/README.md`.
