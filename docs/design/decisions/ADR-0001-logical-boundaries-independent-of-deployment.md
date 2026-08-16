# ADR-0001 — Логические границы независимы от deployment topology

## Статус

`accepted`

## Контекст

MINDRA должна работать как исследовательская модульная когнитивная архитектура на существенно разных вычислительных конфигурациях:

- локальная машина;
- один процесс;
- несколько процессов;
- временная notebook VM;
- Google Colab;
- удалённый GPU;
- будущая распределённая инфраструктура.

Одновременно некоторые логические компоненты могут физически исполняться вне основного процесса. Наиболее очевидный пример — Cortex backend.

Если architecture boundary напрямую привязать к process/device/provider boundary, смена deployment начнёт менять архитектурную семантику и усложнит:

- замену Cortex;
- локальное и удалённое execution;
- тестирование;
- controlled evaluation;
- переносимость checkpoint/runtime;
- сравнение конфигураций;
- будущую оптимизацию compute topology.

---

# Проблема / decision scope

Нужно определить, что считается основанием для принадлежности компонента к MINDRA Agent:

1. физическое размещение;
2. процесс/worker boundary;
3. владение кодом/weights;
4. логическая когнитивная ответственность.

Также нужно решить, являются ли Training/Evaluation Runtime частью Agent только потому, что они могут находиться в одном процессе и обращаться к его state.

---

# Требования и constraints

Решение должно:

- сохранять модульность;
- позволять заменять compute provider;
- позволять запускать простой local prototype;
- не запрещать distributed execution;
- сохранять единый meaning модулей при разном deployment;
- отделять cognition от research/training control plane;
- позволять удалённое физическое выполнение Cortex;
- не требовать конкретного framework;
- не фиксировать process/thread graph раньше `DU-03`.

---

# Рассмотренные варианты

## Вариант A — Deployment-coupled boundary

Компонент считается частью Agent, если находится в том же процессе/VM/device.

### Плюсы

- очень простая mental model для первого prototype;
- минимум абстракций.

### Минусы

- изменение процесса меняет architecture boundary;
- удалённый Cortex автоматически становится «внешним», хотя его функциональная роль не изменилась;
- Training Runtime в одном процессе ошибочно становится частью cognition;
- local и distributed configurations описывают фактически разные архитектуры;
- ухудшается transferability design и evaluation.

**Решение:** rejected.

---

## Вариант B — Service-centric boundary

Все ресурсоёмкие или внешне хостимые компоненты считаются отдельными внешними services.

Cortex, Memory backend, Training и Evaluation описываются прежде всего через service boundaries.

### Плюсы

- хорошо соответствует distributed deployment;
- явные сетевые интерфейсы.

### Минусы

- преждевременно навязывает service architecture;
- усложняет простой local prototype;
- смешивает физическое размещение с semantic responsibility;
- Cortex capability становится внешней только из-за способа запуска;
- может привести к unnecessary serialization/network assumptions.

**Решение:** rejected как canonical system model; допустимо как будущий deployment pattern.

---

## Вариант C — Logical responsibility boundary

Принадлежность определяется **семантической ответственностью и ownership state**, а физическое выполнение рассматривается отдельно.

Следствия:

- Cortex capability находится внутри Agent boundary;
- remote Cortex execution provider может физически находиться снаружи;
- Training Runtime остаётся внешним даже в том же процессе;
- Evaluation Runtime остаётся внешним даже на том же GPU;
- active Memory может использовать внешний storage backend, оставаясь agent-owned state;
- local/distributed deployment должны сохранять одинаковые logical contracts.

### Плюсы

- соответствует модульной архитектуре;
- не привязывает design к hardware;
- поддерживает простой и distributed runtime;
- улучшает заменяемость и evaluation isolation;
- позволяет позднее проектировать process topology независимо.

### Минусы

- требует всегда различать logical и physical diagrams;
- одна физическая система может содержать несколько logical trust domains;
- implementation должна не допускать случайного coupling только из-за co-location.

**Решение:** accepted.

---

# Evidence / references

Решение не зависит от конкретного framework, но существующие системы показывают практичность такой независимости.

- Gymnasium отделяет Environment dynamics от Agent через `reset()` / `step(action)`: [Gymnasium — Env](https://gymnasium.farama.org/api/env/).
- TorchRL поддерживает direct, process и distributed collectors через один conceptual collection layer: [TorchRL — collectors](https://docs.pytorch.org/rl/main/reference/collectors.html).
- TorchRL допускает отдельную evaluation runtime и device/process placement: [TorchRL — Evaluation](https://docs.pytorch.org/rl/main/reference/collectors_eval.html).
- Google Colab использует VM с ограниченным lifetime, что делает привязку durable semantic state к конкретной VM нежелательной: [Google Colab — FAQ](https://research.google.com/colaboratory/intl/en-GB/faq.html).

Эти источники используются как engineering evidence, а не как обязательные зависимости MINDRA.

---

# Принятое решение

MINDRA принимает **logical responsibility boundary independent of deployment topology**.

Канонические правила:

1. Архитектурная принадлежность определяется responsibility/state ownership, а не process/device/provider.
2. Physical co-location не объединяет логические компоненты.
3. Physical separation не разделяет логический компонент автоматически.
4. Cortex является внутренней capability Agent; внешний runtime Cortex может быть infrastructure provider.
5. Training Runtime и Evaluation Runtime являются внешними по отношению к Agent.
6. Storage location не меняет владельца state.
7. Future dependency/runtime contracts должны сохранять эти semantics.

---

# Последствия и trade-offs

## Положительные

- можно начинать с одного process prototype;
- можно позже переносить отдельные блоки на remote GPU без redesign cognition;
- Cortex можно менять независимо от остальной архитектуры;
- evaluation/training isolation становится явной;
- system context не зависит от Colab или домашней GPU;
- проще сравнивать конфигурации на разных compute topologies.

## Отрицательные

- design diagrams должны явно указывать, являются ли они logical или deployment diagrams;
- нельзя считать Python object ownership достаточным описанием architecture ownership;
- shared memory/process globals могут случайно нарушать логические границы;
- будущие architecture tests должны проверять не только import graph, но и запрещённые data paths.

---

# Что решение намеренно не определяет

ADR не определяет:

- конкретные процессы;
- RPC/API;
- network protocol;
- concrete storage backend;
- concrete Cortex backend;
- scheduler;
- sync/async semantics;
- exact `CognitiveState`;
- checkpoint format;
- конкретный cloud/Colab workflow.

---

# Затронутые canonical documents

Прямой canonical owner:

- `docs/design/system-context.md`.

Должны учитывать решение в следующих updates:

- `DU-02 — Dependency & Composition Rules`;
- `DU-03 — Runtime / Temporal Model`;
- `DU-04 — CognitiveState Semantics`;
- `DU-05 — Module Protocol & Scheduling`;
- `DU-06 — Observability & Intervention`;
- `DU-10 — Cortex Boundary`;
- `DU-27 — Checkpoint / Reproducibility / Compute`.
