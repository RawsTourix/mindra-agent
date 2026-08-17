# ADR-0021 — Bounded broadcast Workspace overlay с falsifiable module gate

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-21 — Workspace`

---

# 1. Контекст

После `DU-04` MINDRA уже имеет versioned `CognitiveState`, а после `DU-19` — explicit Salience/Attention boundary.

Поэтому отдельный Workspace нельзя обосновать только необходимостью shared state или attention.

Нужно определить, существует ли самостоятельная функция ограниченной temporary global availability/broadcast между специализированными modules.

---

# 2. Рассмотренные варианты

1. не создавать Workspace и использовать только `CognitiveState + declared reads`;
2. сделать Workspace alias/синонимом `CognitiveState`;
3. сделать giant global prompt/context для Cortex;
4. сделать event bus/pub-sub router;
5. принять Global Workspace Theory буквально как модель сознания;
6. bounded source-preserving shared broadcast overlay с explicit candidate/admission/budget semantics и отрицательным module gate.

---

# 3. Требования

Решение должно:

- давать функцию сверх обычного published state;
- иметь реальный capacity/bandwidth bottleneck;
- поддерживать dynamic admission/competition;
- поддерживать temporary multi-cycle persistence;
- делать admitted content доступным нескольким declared consumers;
- не нарушать dependency/scheduler discipline;
- не становиться Memory;
- не становиться Cortex prompt;
- не передавать ownership source content;
- поддерживать branch-local imagination;
- иметь first-class `NoWorkspace` и matched controls;
- иметь заранее определённый отрицательный критерий;
- не делать claims о subjective consciousness.

---

# 4. Вариант A — Без Workspace

```text
CognitiveState + declared dependencies
```

## Плюсы

- минимальная архитектура;
- уже поддерживает shared current state;
- меньше metadata и routing.

## Минусы

- нет отдельного bounded competition layer;
- dynamic many-to-many integration требует либо широких static reads, либо множества прямых dependencies;
- отсутствует explicit temporary shared focus subset;
- трудно отдельно lesion/intervene в broadcast capacity.

**Решение:** остаётся обязательным `NoWorkspace` baseline, но не принимается как единственная architecture до эмпирической проверки Workspace hypothesis.

---

# 5. Вариант B — Workspace = CognitiveState

## Плюсы

- простота терминов;
- всё уже versioned/shared.

## Минусы

- исчезает bounded capacity;
- невозможно отличить published state от dynamically admitted focus content;
- module gate становится нефальсифицируемым;
- Salience/admission/broadcast невозможно исследовать отдельно.

**Решение:** отклонён.

---

# 6. Вариант C — Workspace как giant Cortex context

```text
all selected items
→ concatenate
→ LLM prompt
```

## Плюсы

- легко реализовать;
- непосредственно полезно LLM.

## Минусы

- Cortex становится центральным consumer;
- Workspace перестаёт быть shared inter-module mechanism;
- token budget конкретной LLM становится архитектурой Workspace;
- remote/local backend differences протекают наружу;
- другие modules не получают общей surface.

**Решение:** отклонён. Cortex context builder может быть одним declared consumer Workspace.

---

# 7. Вариант D — Event bus / pub-sub

## Плюсы

- динамическая many-to-many коммуникация;
- producers не обязаны знать consumers.

## Минусы

- callback/order semantics могут обойти scheduler;
- сложнее snapshot/replay;
- легко получить hidden module invocation;
- конфликт с запретом runtime Service Locator/event-like orchestration как cognitive semantics.

**Решение:** отклонён как canonical runtime. Workspace broadcast означает availability, а не push callback.

---

# 8. Вариант E — Literal Global Workspace Theory

## Плюсы

- исторически разработанная cognitive hypothesis;
- selection + limited capacity + broadcast имеют ясные мотивирующие аналоги.

## Минусы

- neuroscientific theory consciousness не является software requirement;
- её эмпирические claims остаются спорными и развивающимися;
- перенос biological claims на AI создаёт anthropomorphic overclaim;
- MINDRA исследует функциональные механизмы, а не объявляет сознание.

**Решение:** отклонён как canonical theory claim.

MINDRA заимствует только инженерно проверяемые свойства: limited capacity, competition, temporary persistence и shared availability.

---

# 9. Вариант F — Bounded broadcast overlay

Conceptually:

```text
explicit producers
→ WorkspaceCandidateSet
→ optional Salience evidence
→ Workspace admission under budget
→ bounded WorkspaceSnapshot
→ declared multiple consumers
```

## Плюсы

- добавляет функцию сверх `CognitiveState`;
- separate measurable bottleneck;
- dynamic many-to-many integration без direct producer-consumer coupling;
- source provenance сохраняется;
- Cortex/Memory/Policy boundaries не нарушаются;
- natural interventions capacity/broadcast/admission;
- можно удалить subsystem при отрицательном результате.

## Минусы

- дополнительный state/metadata;
- риск дублирования `CognitiveState`;
- risk central bottleneck becoming harmful;
- routing/admission policy добавляет сложности;
- Workspace может превратиться в decorative buffer без carefully designed tasks.

**Решение:** принято условно/falsifiably.

---

# 10. Принятое решение

MINDRA принимает **bounded source-preserving Workspace overlay**, который:

- работает только с explicit proposals/candidates;
- имеет explicit capacity/budget;
- использует отдельную admission policy;
- может использовать Salience как evidence, но не подчиняется ей автоматически;
- хранит temporary `WorkspaceItem` с source revision/provenance;
- делает items доступными нескольким declared consumers;
- не запускает consumers push способом;
- может жить как owner-controlled namespace в `CognitiveState` или отдельный storage-backed snapshot;
- сохраняет real/imagined/branch provenance;
- не является обязательным путем всех module communications.

---

# 11. Functional hypothesis

Workspace считается функционально обоснованным, если при ограниченном processing/communication budget он даёт специфический вклад в:

- cross-module integration;
- coordination;
- dynamic task switching;
- multi-source information binding;
- generalization/compositionality;
- temporary maintenance shared content;

который нельзя объяснить просто дополнительным state/parameters/compute.

---

# 12. Falsification / negative gate

Решение подлежит пересмотру, если на специально designed coordination tasks:

```text
Full Workspace ≈ NoWorkspace/DirectReads
Full Workspace ≈ MatchedSharedBuffer
Full Workspace ≈ MatchedRecurrentBuffer
```

и одновременно:

- capacity interventions не дают осмысленной degradation curve;
- broadcast lesion не нарушает cross-module integration;
- correct admission не лучше random/shuffled matched admission.

В таком случае Workspace следует удалить/слить с существующей shared-state architecture.

---

# 13. Evaluation obligations

Минимальные comparisons:

```text
Full Workspace
NoWorkspace
DirectReadsControl
FixedLatestK
RandomAdmission
ShuffledAdmission
UnboundedWorkspace
WorkspaceWithoutBroadcast
MatchedSharedBufferControl
MatchedRecurrentBufferControl
```

Отдельно варьировать capacity.

Измерять не только task reward/success, но и:

- actual cross-module use;
- item admission/read provenance;
- communication/budget efficiency;
- information bottleneck effects;
- robustness to irrelevant candidates;
- generalization;
- latency/compute overhead;
- failure amplification/noise broadcasting.

---

# 14. Consequences

## Положительные

- появляется отдельная testable working/global-access mechanism;
- можно исследовать selection/broadcast отдельно от Salience;
- dynamic producer-consumer coordination не требует N×M direct dependencies;
- Workspace content легко lesion/intervene;
- Cortex не становится центральной шиной cognition.

## Отрицательные

- дополнительный subsystem state;
- необходимость admission/replacement policy;
- возможный coordination bottleneck;
- риск amplification плохого/ошибочного content;
- требуется строгий matched-control design.

---

# 15. Что ADR не определяет

Не выбраны:

- slot count;
- capacity units;
- top-K/softmax/winner-take-all;
- Transformer/cross-attention;
- neural workspace latent;
- exact persistence duration;
- exact producer/consumer set;
- concrete admission router;
- Cortex packing;
- training loss;
- exact API/checkpoint format.

---

# 16. Research claim boundary

Даже успешный Workspace experiment позволяет утверждать только функциональные свойства bounded shared access/broadcast.

Он **не является evidence сам по себе** наличия:

- consciousness;
- subjective experience;
- phenomenal awareness;
- человеческого Global Neuronal Workspace.
