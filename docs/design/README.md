# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, границы модулей, internal contracts, архитектурные решения и будущие version plans.

На текущем этапе сформирован documentation foundation и приняты `DU-01` … `DU-06`. Детальные subsystem design добавляются последовательно после отдельного исследования вариантов.

---

# 1. Иерархия

```text
Concept
→ Design semantics / invariants
→ ADR
→ Exact internal contracts
→ Version specification
→ Implementation sequence
→ Engineering/research acceptance evidence
```

Research evidence не переписывает design напрямую: противоречащий результат инициирует design review.

---

# 2. Текущая навигация

## Foundation

- [`principles.md`](principles.md) — устойчивые инженерные и исследовательские принципы;
- [`glossary.md`](glossary.md) — канонические значения терминов;
- [`documentation-plan.md`](documentation-plan.md) — канонический порядок `DU-00` … `DU-32`;
- [`current.md`](current.md) — фактический статус и следующий допустимый шаг.

## Canonical system design

- [`system-context.md`](system-context.md) — `DU-01`: логические границы Agent, Environment, training/evaluation infrastructure, artifact/storage/compute и разрешённые потоки данных;
- [`dependency-rules.md`](dependency-rules.md) — `DU-02`: dependency directions, Composition Root, dependency inversion, backend isolation и запрет runtime Service Locator/shared mutable globals;
- [`execution-model.md`](execution-model.md) — `DU-03`: иерархическое логическое время, Agent Session/Episode/Decision Window/Cognitive Cycle, causal commit boundaries, async semantics и replay requirements;
- [`cognitive-state.md`](cognitive-state.md) — `DU-04`: committed state snapshots, namespaces/ownership, availability/freshness, temporal scopes, provenance, private-state boundary и clone/counterfactual requirements;
- [`module-lifecycle.md`](module-lifecycle.md) — `DU-05`: module descriptors, declared reads/writes, DAG/wave scheduling, transactional public/private effects, lifecycle/failure semantics и граница будущего Executive Control;
- [`observability-and-intervention.md`](observability-and-intervention.md) — `DU-06`: passive Evidence Plane, causal tracing, private-state probes, observability depth, explicit Intervention Gateway, branch/provenance semantics и counterfactual requirements.

## Карта модулей

- [`modules/README.md`](modules/README.md) — предварительная карта архитектурных областей, их responsibilities, различий и зависимостей.

Наличие области в карте не означает, что отдельный модуль уже принят. Соответствующий Design Update может объединить, разделить, отложить или отвергнуть кандидатную ответственность.

## Decision records

- [`decisions/README.md`](decisions/README.md);
- [`ADR-0001`](decisions/ADR-0001-logical-boundaries-independent-of-deployment.md) — logical responsibility boundary independent of deployment topology;
- [`ADR-0002`](decisions/ADR-0002-explicit-composition-no-runtime-service-locator.md) — explicit Composition Root и запрет runtime Service Locator;
- [`ADR-0003`](decisions/ADR-0003-hierarchical-logical-time.md) — hierarchical logical time и causal commit boundaries;
- [`ADR-0004`](decisions/ADR-0004-versioned-committed-cognitive-state.md) — versioned committed CognitiveState, staged owner-scoped updates и запрет hidden mutable bus semantics;
- [`ADR-0005`](decisions/ADR-0005-wave-scheduled-module-protocol.md) — declared DAG scheduling, execution waves и atomic public/private module commit;
- [`ADR-0006`](decisions/ADR-0006-separated-evidence-plane-and-intervention-gateway.md) — passive Evidence Plane отдельно от privileged Intervention Gateway.

## Exact internal contracts

- [`contracts/README.md`](contracts/README.md).

Semantic `CognitiveState`, module lifecycle и research observability/intervention boundaries уже определены, но exact machine-facing Python contracts намеренно не фиксируются до появления module-specific design pressure и дальнейшего contract freeze.

## Versions

- [`versions/README.md`](versions/README.md).

---

# 3. Design Update discipline

`DU-xx` — идентификатор самостоятельного архитектурного documentation update, а не software version.

Каждый update должен:

- иметь prerequisites;
- закрывать ограниченный набор design questions;
- проводить targeted research там, где есть реальный выбор;
- фиксировать responsibilities/non-goals/invariants;
- создавать ADR при значимом выборе между вариантами;
- обновлять canonical owner темы;
- не протаскивать downstream decisions раньше времени;
- завершаться consistency review и обновлением `current.md`.

Канонический порядок: [`documentation-plan.md`](documentation-plan.md).

Текущий следующий update: `DU-07 — Environment / MicroWorld Contract`.

---

# 4. Canonical owner

У значимой архитектурной темы должен быть один основной canonical owner.

Общий документ может ссылаться на тему, но не должен независимо определять вторую конкурирующую семантику.

Если ADR меняет принятое решение:

1. обновляется ADR registry;
2. обновляется canonical design owner;
3. обновляются exact contracts;
4. обновляются затронутые version plans/status;
5. только затем implementation следует новому решению.

---

# 5. Design для coding agents

Implementation-ready design должен минимизировать архитектурные догадки.

Для каждой будущей подсистемы желательно определить:

- назначение;
- responsibilities;
- non-goals;
- inputs/outputs;
- owned state;
- dependencies;
- lifecycle/update semantics;
- training signals;
- persistence/checkpoint semantics;
- observability;
- failure/degradation behavior;
- ablation/control strategy;
- evaluation metrics;
- open questions.

Если существенное решение ещё не принято, оно должно быть обозначено как open question/blocker, а не оставлено на усмотрение Codex.

---

# 6. Правило существования отдельного модуля

Когнитивная аналогия сама по себе не является основанием для нового module boundary.

Отдельный модуль должен иметь:

1. самостоятельную вычислительную ответственность;
2. явные input/output/state semantics;
3. независимый lifecycle или значимую границу обновления;
4. возможность отключения/подмены;
5. собственную diagnostic/evaluation strategy;
6. функциональную роль, не дублирующую соседний модуль.

Если эти условия не выполняются, design должен рассмотреть объединение ответственности.

---

# 7. Текущая граница

Приняты `DU-01` … `DU-06`, но пока не существует accepted detailed cognitive module design, exact module contract или version roadmap.

Канонически уже зафиксированы:

- logical architecture boundary не равна deployment topology;
- hidden concrete dependencies/runtime Service Locator запрещены;
- runtime feedback cycle не равен static dependency cycle;
- logical causal time не равно wall-clock;
- Environment Episode не равно Agent Session;
- Cognitive Cycle не равно Environment Transition;
- runtime state update не равно Learning Update;
- causal replay является архитектурной целью, а bitwise replay — best-effort свойством runtime;
- `CognitiveState` является canonical shared runtime state, а не всем `Agent-owned state`;
- committed state revision семантически неизменяема;
- canonical writes имеют однозначного semantic owner;
- state availability/freshness и provenance являются частью семантики;
- private causally relevant state не должно скрываться от будущих snapshot/reproducibility requirements;
- module execution order выводится из declared dependencies/freshness/phase constraints;
- instantaneous scheduler graph является DAG;
- independent ready modules исполняются через snapshot-consistent execution waves;
- public и causally relevant private effects согласуются через atomic commit semantics;
- scheduler mechanics принадлежат Agent runtime core, но не являются когнитивным модулем;
- future Executive Control не сможет обходить scheduler/contracts/commit boundaries;
- passive observability отделена от active intervention;
- trace обязан различать computation attempt и committed effect;
- private-state inspection проходит через declared research probe, а не mutable object access;
- intervention имеет отдельные target/base/provenance semantics и не меняет semantic owner;
- confirmatory causal experiments по умолчанию предпочитают fork от committed base;
- raw/backend activation access является opt-in research capability, а не универсальным контрактом;
- intervened data не смешивается с natural experience без явного design.

Обсуждавшиеся ранее Qwen, TensorDict, PPO, Dreamer, RND, ICM, FAISS, PEFT/LoRA, Colab, OpenTelemetry, pyvene и другие технологии являются кандидатами для будущего анализа, но не каноническими требованиями.

Фактический статус: [`current.md`](current.md).
