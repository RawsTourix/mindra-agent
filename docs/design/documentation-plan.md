# План проектирования документации MINDRA

## Статус документа

Этот документ является каноническим владельцем **порядка design-обновлений** MINDRA до появления version roadmap.

Он не является roadmap реализации и не определяет software versions.

Каждый идентификатор вида `DU-xx` означает самостоятельное **Design Update**: ограниченный documentation patch, который должен закрыть один связный набор архитектурных вопросов, пройти review и только после этого стать основанием для следующего обновления.

Главный принцип:

```text
не проектировать следующий слой через предположения
о ещё не определённом предыдущем слое
```

Version roadmap появляется только после того, как canonical architecture, training/evaluation boundaries и exact internal contracts достаточно сформированы.

---

# 1. Что считается самостоятельным Design Update

Каждый `DU` должен иметь:

1. чёткую цель;
2. обязательные prerequisites;
3. список вопросов, которые именно этот update обязан закрыть;
4. список вопросов, которые в него **не входят**;
5. research pass по существующим подходам, если выбор не тривиален;
6. рассмотренные варианты и trade-offs;
7. canonical design owner;
8. ADR, если существует несколько реалистичных архитектурных вариантов;
9. consistency patch для glossary/index/current/contracts, если они затронуты;
10. явный completion gate.

Design Update не должен одновременно:

- проектировать несколько независимых подсистем «заодно»;
- фиксировать library/API раньше semantic requirements;
- смешивать architecture design с implementation versioning;
- превращать exploratory идею в accepted invariant без сравнения альтернатив;
- добавлять будущий scope только потому, что он тесно связан по тематике.

---

# 2. Типовой workflow одного Design Update

Рекомендуемый порядок:

```text
1. восстановить repository context
2. сформулировать design questions
3. провести targeted research
4. сравнить candidate approaches
5. определить invariants / responsibilities / non-goals
6. решить open choices через ADR при необходимости
7. записать canonical design
8. определить будущие exact contracts, если semantic boundary уже стабилен
9. определить testing/evaluation implications
10. consistency review
11. обновить current.md
```

Research pass должен использовать в первую очередь:

- исходные научные статьи;
- официальную документацию framework/library;
- официальные model cards;
- reference implementations авторов/maintainers;
- только затем качественные вторичные обзоры для навигации.

Конкретные ресурсы не закрепляются этим планом: они выбираются заново при выполнении соответствующего `DU`, чтобы не зафиксировать устаревшее состояние области.

---

# 3. Общий dependency graph design-обновлений

```text
DU-00 Documentation Foundation [готово]
        ↓
DU-01 System Context
        ↓
DU-02 Dependency & Composition Rules
        ↓
DU-03 Runtime / Temporal Model
        ↓
DU-04 CognitiveState Semantics
        ↓
DU-05 Module Protocol & Scheduling
        ↓
DU-06 Observability & Intervention
        ↓
DU-07 Environment / MicroWorld Contract
        ↓
DU-08 Perception / Canonical Representation
        ↓
DU-09 Goal System
        ↓
DU-10 Cortex Boundary
        ↓
DU-11 Memory Core
        ↓
DU-12 World Model
        ↓
DU-13 Self Model
        ↓
DU-14 Intrinsic Signals
        ↓
DU-15 Drives
        ↓
DU-16 Appraisal
        ↓
DU-17 Affect Dynamics
        ↓
DU-18 Valuation
        ↓
DU-19 Salience / Attention
        ↓
DU-20 Memory Regulation / Consolidation
        ↓
DU-21 Workspace
        ↓
DU-22 Metacognitive / Executive Control
        ↓
DU-23 Policy / Planner
        ↓
DU-24 Action Boundary
        ↓
DU-25 Experience / Data / Replay
        ↓
DU-26 Training Lifecycle
        ↓
DU-27 Checkpoint / Reproducibility / Compute
        ↓
DU-28 Evaluation Harness
        ↓
DU-29 Engineering Testing
        ↓
DU-30 Research Claims / Limitations
        ↓
DU-31 Contract + ADR Consistency Freeze
        ↓
DU-32 Version Roadmap
```

Это порядок **semantic design**, а не утверждение о линейном runtime. Фактическая когнитивная система будет содержать feedback loops.

---

# 4. DU-00 — Documentation Foundation

**Статус:** завершён.

Зафиксированы:

- `project-concept.md`;
- `architecture-concept.md`;
- `research-methodology.md`;
- `design/principles.md`;
- `design/glossary.md`;
- `design/current.md`;
- `AGENTS.md`;
- реестры ADR/contracts/versions;
- карта проектирования модулей.

## Gate

Следующий update не должен возвращаться к общему brainstorming без необходимости. Новые идеи либо ложатся в конкретный `DU`, либо оформляются как open question.

---

# 5. DU-01 — System Context

## Цель

Определить MINDRA как систему в окружении внешних runtime, storage, compute и исследовательских компонентов.

## Обязательные вопросы

- что находится внутри agent boundary;
- что является Environment;
- где проходит Cortex boundary;
- где живёт training runtime;
- где живёт evaluation runtime;
- чем online execution отличается от offline training/consolidation;
- что считается внешним artifact/checkpoint storage;
- какие роли могут выполнять локальная машина, Colab/remote GPU и future compute providers;
- какие внешние системы считаются trusted/untrusted;
- где находятся experiment runner и artifact collector;
- какие данные могут пересекать system boundary.

## Результат

`system-context.md`.

## Не входит

- конкретная библиотека;
- конкретный GPU;
- точный process graph;
- точный `CognitiveState`;
- module protocol.

## Gate

Любой следующий документ должен однозначно понимать, **в какой системе и в каком runtime context существует обсуждаемый объект**.

---

# 6. DU-02 — Dependency & Composition Rules

## Цель

Не допустить превращения модульной архитектуры в сеть скрытых Python-зависимостей.

## Обязательные вопросы

- допустимые import directions;
- место shared contracts;
- composition root;
- registry/plugin mechanism на semantic уровне;
- запрет прямой зависимости от concrete Cortex backend;
- взаимодействие runtime modules и training code;
- взаимодействие evaluator и internal state;
- правила доступа к module-private state;
- как модуль объявляет зависимость, не импортируя concrete implementation;
- как disabled/control implementation подменяет обычный модуль;
- как предотвращается circular hidden coupling.

## Результат

`dependency-rules.md`.

## Возможный ADR

Если потребуется выбор между DI/registry/graph composition подходами.

## Gate

Можно нарисовать разрешённый dependency graph и автоматически проверить значительную часть правил в будущих architecture tests.

---

# 7. DU-03 — Runtime / Temporal Model

## Цель

Определить **временную семантику** MINDRA до проектирования state и lifecycle.

## Обязательные вопросы

Различить:

```text
environment tick
cognitive step
module compute phase
action dispatch
outcome observation
runtime state update
online learning update
replay step
consolidation step
evaluation-only execution
```

Также определить:

- синхронность/асинхронность на semantic уровне;
- clock/step identity;
- episode/session identity;
- что может переживать episode reset;
- какие state изменения должны быть causal/order-aware;
- что означает deterministic replay;
- может ли один environment tick содержать несколько внутренних cognitive cycles;
- чем fixed runtime scheduler отличается от будущего learned Executive Control.

## Результат

`runtime-topology.md` или отдельный `execution-model.md` — точное имя выбирается в update.

## Gate

Следующий `CognitiveState` design может однозначно описать, **к какому моменту времени относится каждое значение**.

---

# 8. DU-04 — Canonical CognitiveState Semantics

## Цель

Спроектировать каноническую модель внутреннего состояния без привязки к конкретному framework.

## Обязательные вопросы

- категории state;
- persistent/ephemeral;
- observed/derived/predicted;
- owner каждого field namespace;
- read/write permissions;
- immutable snapshot vs mutable bus;
- version/timestamp/step semantics;
- `unknown`/`missing`/`stale`;
- provenance;
- batch dimensions;
- device/dtype independence на semantic уровне;
- serialization requirements;
- clone/counterfactual requirements;
- checkpoint/replay compatibility;
- model-specific hidden state isolation.

## Результаты

- `cognitive-state.md`;
- при необходимости ADR по representation strategy;
- позднее exact contract.

## Не входит

Точные dimensions и concrete TensorDict/dataclass/Pydantic choice, пока requirements не сформированы.

## Gate

Каждый будущий модуль может объявить собственные input/output namespaces без знания concrete реализации соседей.

---

# 9. DU-05 — Module Protocol & Scheduling

## Цель

Определить единый lifecycle заменяемого cognitive module.

## Обязательные вопросы

Conceptual lifecycle:

```text
initialize
reset
read state
compute
publish state
observe outcome
update runtime state
learn
checkpoint
restore
shutdown
```

Нужно решить:

- какие методы обязательны/опциональны;
- deterministic mode;
- train/eval mode;
- dependency declaration;
- ordering;
- error/degradation semantics;
- `NoOp`/disabled behavior;
- control implementation behavior;
- trainable vs stateless modules;
- module-local private state;
- scheduler graph;
- cycle prevention;
- batch/vectorized environments.

## Результаты

- `module-lifecycle.md`;
- первое semantic описание `ModuleProtocol`;
- возможный ADR по scheduler/composition model.

## Gate

Любой будущий module design обязан вписываться в единый lifecycle без ad-hoc специальных вызовов из main loop.

---

# 10. DU-06 — Observability & Intervention

## Цель

Сделать исследовательскую диагностируемость частью архитектуры до появления сложных модулей.

## Обязательные вопросы

- module input/output tracing;
- state snapshots;
- trajectory tracing;
- intervention hooks;
- force/override конкретного state;
- module disable/substitution;
- counterfactual clone;
- debug metadata vs agent-visible state;
- metrics/event emission;
- privacy/size boundaries для Cortex activations;
- deterministic capture;
- causal intervention без скрытого изменения остальных переменных.

## Результат

`observability-and-intervention.md`.

## Gate

Новый модуль нельзя считать research-ready, если его невозможно наблюдать, отключить и причинно вмешаться в его outputs там, где это требуется гипотезой.

---

# 11. DU-07 — Environment / MicroWorld Contract

## Цель

Спроектировать контролируемый исследовательский мир и общий Environment boundary.

## Обязательные вопросы

- observation space;
- action space;
- objective external feedback отдельно от internal utility;
- reset/step/clone/restore;
- procedural generation;
- hidden rules;
- train/validation/test world distributions;
- deterministic seeds;
- counterfactual branching;
- environment versioning;
- task families;
- failure/termination/truncation;
- intervention API;
- minimal baseline tasks;
- отсутствие скрытой помощи агенту через evaluator.

## Результаты

- `modules/environment.md`;
- exact Environment contract candidate.

## Research focus

Сравнить подходы Gymnasium-подобных сред, benchmark design для model-based/RL agents и требования собственных causal experiments.

## Gate

Можно специфицировать одинаковый внешний мир для baseline и любой MINDRA configuration.

---

# 12. DU-08 — Perception / Canonical Representation

## Цель

Отделить raw Environment/Cortex input от внутреннего representation space остальных модулей.

## Обязательные вопросы

- structured vs learned encoding;
- canonical representation semantics;
- modality metadata;
- missing observations;
- normalization;
- representation versioning;
- reversible provenance;
- trainable encoder boundary;
- representation drift;
- Cortex embedding adapter;
- no-Cortex mode;
- representation compatibility across backends.

## Результат

`modules/perception.md`.

## Gate

World Model, Memory и Policy больше не обязаны знать raw environment schema или hidden size конкретной LLM.

---

# 13. DU-09 — Goal System

## Цель

Явно отделить цели от reward, drives, appraisal и policy.

## Обязательные вопросы

- external goal;
- internally generated goal;
- subgoal;
- priority;
- commitment;
- persistence;
- completion/failure/abandonment;
- progress representation;
- conflict;
- goal stack/graph;
- goal provenance;
- кто имеет право создавать/изменять goal;
- связь natural-language instruction с canonical goal;
- связь goals с future valuation.

## Результат

`modules/goals.md`.

## Gate

Остальные модули могут ссылаться на canonical goal semantics, не придумывая собственное понимание «цели».

---

# 14. DU-10 — Cortex Boundary

## Цель

Спроектировать заменяемую pretrained «кору» как capability backend, а не как центр архитектуры.

## Обязательные вопросы

- required capabilities;
- text generation;
- hidden/embedding access;
- canonical adapter;
- multilingual requirements;
- reasoning mode;
- context construction;
- tool/action proposal boundary;
- soft/latent bridge;
- text fallback;
- frozen/adapted modes;
- `DummyCortex`;
- `NoCortex`;
- backend switching;
- transfer testing;
- resource reporting;
- backend identity in checkpoint/experiment record.

## Research focus

При выполнении update провести свежий model comparison по model cards, multilingual benchmarks, memory/VRAM requirements, licensing и доступности hidden-state interfaces.

## Результаты

- `modules/cortex.md`;
- Cortex contract;
- ADR по baseline backend только если выбор действительно нужен на design уровне.

## Gate

Ни один non-Cortex module не зависит от конкретной model family.

---

# 15. DU-11 — Memory Core

## Цель

Спроектировать нейтральное episodic storage/retrieval до эмоционально/мотивационно регулируемой памяти.

## Обязательные вопросы

- episodic record;
- temporal identity;
- provenance;
- canonical representation for retrieval;
- indexing;
- similarity/relevance;
- retrieval query source;
- capacity;
- exact vs approximate retrieval;
- raw trajectory vs summarized memory;
- semantic/procedural memory necessity;
- working memory boundary с `CognitiveState`/Workspace;
- deterministic replay;
- storage backend abstraction.

## Не входит

- salience-based retention;
- forgetting policy;
- consolidation scheduling.

## Результат

`modules/memory.md` с первой частью Memory Core semantics.

## Gate

Appraisal/Self Model/Policy могут читать прошлый опыт через стабильный retrieval contract.

---

# 16. DU-12 — World Model

## Цель

Определить predictive model окружающей среды.

## Обязательные вопросы

- prediction target;
- latent/observable predictions;
- action conditioning;
- one-step/multi-step rollout;
- uncertainty;
- prediction error;
- stochasticity;
- imagined trajectories;
- training source;
- leakage prevention;
- planning interface;
- no-op/control implementation;
- module-specific evaluation.

## Research focus

World-model/model-based RL, recurrent state-space models, Transformer world models и минимальные модели для малых сред.

## Результат

`modules/world-model.md`.

## Gate

Prediction signal имеет точную семантику и может использоваться следующими модулями без знания architecture internals World Model.

---

# 17. DU-13 — Self Model

## Цель

Определить, какие свойства собственных возможностей агент моделирует отдельно от World Model.

## Обязательные вопросы

- success probability;
- competence;
- capability boundary;
- uncertainty/calibration;
- action cost/resource estimate;
- own-state prediction;
- history dependence;
- task/domain specificity;
- calibration targets;
- distinction from Cortex verbal self-report;
- distinction from metacognitive control.

## Результат

`modules/self-model.md`.

## Gate

Self Model имеет measurable predictive targets и calibration metrics, а не описательный personality state.

---

# 18. DU-14 — Intrinsic Signal Providers

## Цель

Развести objective-derived intrinsic signals и собственно Drives/Valuation.

## Обязательные вопросы

Кандидатные сигналы:

- novelty;
- surprise;
- prediction error;
- epistemic uncertainty;
- information gain;
- uncertainty reduction;
- competence progress;
- visitation rarity.

Нужно определить:

- semantic units;
- normalization;
- stationarity;
- noisy-TV/pathological curiosity risks;
- dependence on World/Self Model;
- learnable vs deterministic signal;
- control baselines;
- logging/evaluation.

## Результат

`modules/intrinsic-signals.md`.

## Gate

Можно говорить «событие ново/неожиданно» отдельно от «агент сейчас хочет новизны».

---

# 19. DU-15 — Drives

## Цель

Спроектировать внутренние регулируемые variables, которые изменяют относительную значимость событий во времени.

## Обязательные вопросы

- список категорий на semantic уровне;
- state dynamics;
- target/range/homeostasis;
- decay/recovery;
- saturation;
- interaction;
- update sources;
- initial conditions;
- learned vs fixed dynamics;
- persistence между episodes;
- relation to goals;
- relation to intrinsic signals;
- causal intervention protocol.

## Результат

`modules/drives.md`.

## Gate

Разное Drive state может быть независимо установлено/измерено и не является просто другим названием reward weight.

---

# 20. DU-16 — Appraisal

## Цель

Спроектировать контекстную оценку значения конкретного события для текущего агента.

## Обязательные вопросы

- event boundary;
- input context;
- relation to goals/drives/world/self/memory;
- multidimensional output;
- learnable targets;
- rule-derived targets;
- online/offline update;
- calibration;
- causal effect requirements;
- distinction from Valuation;
- distinction from Affect state.

## Результат

`modules/appraisal.md`.

## Gate

Appraisal имеет собственную многомерную responsibility и не сводится к scalar reward prediction.

---

# 21. DU-17 — Affect Dynamics

## Цель

Проверить необходимость отдельного persistent affective state, который интегрирует оценку событий во времени.

## Обязательные вопросы

- какие appraisal outputs интегрируются;
- decay/inertia/recovery;
- short/medium-term persistence;
- saturation;
- interaction with Drives;
- downstream modulation;
- episode/reset semantics;
- intervention;
- gate отделения от Appraisal;
- control implementation.

## Результат

`modules/affect.md` либо ADR/решение объединить эту ответственность с другим модулем.

## Gate

Отдельный Affect сохраняется только если у него есть самостоятельная функциональная роль.

---

# 22. DU-18 — Valuation

## Цель

Спроектировать центральную внутреннюю систему ценности — ключевой предмет исходной гипотезы MINDRA.

## Обязательные вопросы

Развести:

```text
external feedback
intrinsic signal
drive state
goal progress
appraisal
affect
immediate utility
future value
risk/uncertainty
```

Нужно решить:

- vector-valued representation;
- scalarization, если требуется;
- context-dependent weights;
- learned vs structured aggregation;
- state/action value;
- critic boundary;
- temporal discounting;
- risk sensitivity;
- conflicts между criteria;
- stability/identifiability;
- causal evaluation;
- relation to Policy.

## Результат

`modules/valuation.md` + возможный ключевой ADR.

## Gate

Policy получает decision-relevant value через явный contract; внутренняя ценность не растворена в непрозрачной общей loss-функции.

---

# 23. DU-19 — Salience / Attention Control

## Цель

Спроектировать приоритетность информации и распределение ограниченного cognitive processing.

## Обязательные вопросы

- salience inputs;
- event/item granularity;
- attention priority;
- memory write priority;
- replay priority;
- Workspace admission;
- optional compute allocation;
- normalization/competition;
- persistence;
- future-utility target;
- off-target effects;
- intervention.

## Результат

`modules/salience.md`.

## Gate

Salience обязательно имеет downstream causal effects; декоративный score не считается модулем.

---

# 24. DU-20 — Memory Regulation / Consolidation

## Цель

Добавить к Memory Core управляемое сохранение, забывание, replay и consolidation.

## Обязательные вопросы

- retention;
- eviction;
- forgetting;
- replay selection;
- prioritized replay;
- salience integration;
- memory aging;
- consolidation target;
- slow weight updates;
- semantic abstraction;
- catastrophic forgetting;
- provenance влияния memory на future learning;
- shuffled/no-memory controls.

## Результат

Обновление `modules/memory.md` + `memory-consolidation.md`, если область окажется достаточно самостоятельной.

## Gate

Память может доказуемо выбирать/сохранять опыт полезнее случайного или purely recent baseline.

---

# 25. DU-21 — Workspace

## Цель

Определить ограниченный общий интеграционный механизм и доказать, что он отличается от обычного state bus.

## Обязательные вопросы

- candidate admission;
- capacity;
- competition/gating;
- broadcast/read semantics;
- persistence;
- consumers;
- relation to Salience;
- relation to Cortex;
- relation to Memory;
- intervention;
- no-workspace baseline;
- exact distinction from `CognitiveState`.

## Research focus

Global Workspace Theory как функциональная гипотеза, современные workspace-like neural mechanisms и engineering alternatives без антропоморфного предположения.

## Результат

`modules/workspace.md` либо аргументированное решение не выделять отдельный Workspace.

## Gate

Отдельный Workspace имеет measurable role сверх общего state exchange.

---

# 26. DU-22 — Metacognitive / Executive Control

## Цель

Определить, нужен ли отдельный механизм, который регулирует **сам процесс вычисления**, используя Self Model/uncertainty/goals/value.

## Обязательные вопросы

- strategy selection;
- memory retrieval decision;
- planner depth;
- Cortex invocation;
- compute budget;
- uncertainty-triggered verification;
- exploration/exploitation mode;
- goal focus switching;
- self-monitoring;
- relation to fixed scheduler;
- relation to Self Model;
- relation to Policy/Workspace.

## Результат

`modules/executive-control.md` либо ADR о распределении ответственности между существующими модулями.

## Gate

Executive Control сохраняется отдельным только при самостоятельной causal responsibility.

---

# 27. DU-23 — Policy / Planner

## Цель

Определить границу выбора действия после того, как уже известны representations, goals, value, memory и predictive state.

## Обязательные вопросы

- model-free policy;
- model-based planner;
- hierarchical planning;
- subgoals;
- candidate action generation;
- action distribution;
- exploration;
- World Model rollouts;
- Cortex reasoning contribution;
- critic coupling;
- deterministic evaluation;
- conflict resolution;
- fallback/degradation;
- no-Cortex mode.

## Результат

`modules/policy.md`.

## Gate

Policy отвечает за action selection, но не владеет скрытыми копиями Goals/Valuation/Memory.

---

# 28. DU-24 — Action Boundary

## Цель

Отделить candidate/selected action от фактического исполнения и наблюдаемого outcome.

## Обязательные вопросы

- action validation;
- feasibility;
- constraint/safety hooks;
- action identity;
- dispatch;
- failure;
- timeout;
- unknown outcome;
- cancellation, если применимо;
- executed vs requested action;
- outcome attribution;
- trajectory linkage;
- future external-tool boundary.

## Результат

`modules/action.md` или `action-boundary.md`.

## Gate

Research trace может однозначно связать решение, фактическое действие и последствие.

---

# 29. DU-25 — Experience / Data / Replay

## Цель

Определить каноническую запись опыта после того, как все основные module outputs известны.

## Обязательные вопросы

Trajectory record должен рассмотреть:

- observation;
- canonical representation;
- internal state snapshot/reference;
- active goals;
- module outputs;
- action proposal/selection/execution;
- prediction;
- outcome;
- external feedback;
- intrinsic signals;
- appraisal/affect/value/salience;
- memory reads/writes;
- timestamps/steps;
- provenance;
- seed/world/version;
- leakage controls.

Также:

- replay sampling;
- train/eval split;
- dataset versioning;
- retention;
- synthetic/human annotations;
- schema evolution.

## Результат

`data-and-replay.md` + experiment/trajectory contract candidate.

## Gate

Training и evaluation могут работать с одним reproducible experience representation.

---

# 30. DU-26 — Training Lifecycle

## Цель

Спроектировать обучение всей композиции без требования end-to-end update каждого параметра на каждом шаге.

## Обязательные вопросы

- module pretraining;
- frozen/trainable sets;
- online learning;
- offline replay;
- consolidation;
- alternating updates;
- joint training;
- optimizer ownership;
- gradient boundaries;
- stop-gradient;
- Cortex adaptation;
- curriculum;
- catastrophic forgetting;
- stability;
- resume semantics;
- stopping criteria;
- evaluation isolation;
- compute-aware scheduling.

## Результат

`training.md`.

## Gate

Для каждого trainable module понятно: **что, когда, на каких данных и каким signal его обучает**.

---

# 31. DU-27 — Checkpoint / Reproducibility / Compute

## Цель

Сделать experiment resumable и воспроизводимым на неоднородном compute.

## Обязательные вопросы

- versioned checkpoint composition;
- module states;
- optimizer states;
- random generators;
- environment state;
- replay/data cursor;
- Cortex identity;
- adapter identity;
- configuration hash;
- repository commit;
- artifact manifest;
- CPU/GPU device mapping;
- local/Colab/remote compute profiles;
- interruption/resume;
- storage atomicity;
- checkpoint compatibility.

## Результаты

- `checkpointing.md`;
- `reproducibility.md`;
- exact checkpoint/experiment-record contracts.

## Gate

Значимый experiment можно восстановить без зависимости от исходной transient VM.

---

# 32. DU-28 — MINDRA-Eval

## Цель

Превратить общую research methodology в точный evaluation harness.

## Обязательные вопросы

- baseline matrix;
- Cortex-only/no-Cortex;
- module ablations;
- random/constant/shuffled controls;
- parameter/compute-matched controls;
- factorial interactions;
- causal interventions;
- counterfactual branching;
- transfer between Cortex backends;
- generalization;
- adaptation speed;
- module-specific metrics;
- seed policy;
- uncertainty/confidence intervals;
- primary/secondary endpoints;
- experiment registry;
- negative result acceptance;
- composite score policy или осознанный отказ от одного score.

## Результат

`evaluation.md` + future MINDRA-Eval contract.

## Gate

Для каждой ключевой архитектурной гипотезы существует тест, который способен не только подтвердить, но и ослабить/опровергнуть её.

---

# 33. DU-29 — Engineering Testing

## Цель

Отделить software correctness от research evaluation.

## Обязательные классы

- static/lint/type;
- architecture dependency tests;
- unit;
- contract;
- component integration;
- environment determinism;
- state clone/restore;
- checkpoint roundtrip;
- CPU/GPU compatibility;
- failure injection;
- resume/recovery;
- serialization/version compatibility;
- smoke experiment;
- optional long/full profiles.

## Результат

`testing.md`.

## Gate

Green research metric не может маскировать broken engineering contract.

---

# 34. DU-30 — Research Claims / Limitations

## Цель

Зафиксировать допустимые уровни интерпретации результатов до публикации серьёзных experiment claims.

## Обязательные вопросы

- functional vs phenomenal claims;
- anthropomorphic terminology;
- what evidence supports what wording;
- known confounders;
- model-size dependence;
- environment artificiality;
- biological analogy limits;
- external validity;
- safety/agent autonomy boundaries;
- negative evidence;
- unsupported consciousness claims.

## Результаты

- `research-claims.md`;
- `limitations.md`.

## Gate

Ни design, ни README, ни experiment report не могут делать более сильный вывод, чем позволяет evidence class.

---

# 35. DU-31 — Contract + ADR Consistency Freeze

## Цель

Перед version roadmap закрыть архитектурную неоднозначность, которая иначе будет передана Codex как implementation guess.

## Проверить

- у каждой темы один canonical owner;
- все значимые choices имеют accepted ADR или явно остаются deferred;
- superseded решения не выглядят активными;
- module inputs/outputs/lifecycle согласованы;
- `CognitiveState` namespaces согласованы;
- exact internal contracts отражают semantic design;
- training/evaluation/checkpoint contracts совместимы;
- glossary не конфликтует с module docs;
- никаких hidden TODO, требующих архитектурного решения во время coding.

## Результат

Design line получает статус `ready for version planning`.

## Gate

Codex не должен быть вынужден самостоятельно выбирать архитектуру для первого implementation milestone.

---

# 36. DU-32 — Version Roadmap

## Цель

Только теперь разбить принятую архитектуру на implementation milestones.

## Принципы разбиения

Каждая версия должна:

- быть вертикально проверяемой;
- иметь dependency-complete scope;
- не требовать заведомого rewrite следующей версией;
- иметь baseline/acceptance evidence;
- соответствовать доступному compute;
- не добавлять слишком много новых learning dynamics одновременно;
- иметь чёткие non-goals.

После roadmap для каждой версии отдельно проектируются:

```text
versions/vX.Y/README.md
versions/vX.Y/implementation-sequence.md
```

И только затем появляются прямые задания Codex на реализацию.

---

# 37. Почему некоторые области специально разделены

## 37.1 Appraisal ≠ Affect ≠ Valuation

```text
Appraisal
→ что текущее событие означает для агента

Affect
→ какое сохраняющееся внутреннее состояние сформировалось во времени

Valuation
→ какую decision-relevant ценность имеют состояния/действия
```

Их можно позже объединить, но сначала семантики должны быть разведены, чтобы не создать один непрозрачный «эмоциональный reward module».

## 37.2 Intrinsic Signal ≠ Drive

```text
novelty = свойство опыта
novelty drive = текущая внутренняя потребность в исследовании
```

Это разные причины изменения поведения.

## 37.3 Self Model ≠ Executive Control

Self Model может оценивать собственную компетентность, но Executive Control — если он нужен — использует такие оценки для изменения **самой стратегии вычисления**.

## 37.4 Salience ≠ Workspace

Salience определяет приоритет; Workspace определяет ограниченную общую доступность выбранной информации.

## 37.5 CognitiveState ≠ Workspace

`CognitiveState` — инженерный канонический state exchange. Workspace — потенциальный функциональный механизм cognition. Их смешение сделало бы исследовательскую гипотезу непроверяемой.

## 37.6 Scheduler ≠ Executive Control

Scheduler обеспечивает deterministic correctness runtime graph. Executive Control, если будет принят, является агентным механизмом, способным выбирать, какие cognitive операции выполнять.

## 37.7 Memory Core ≠ Memory Regulation

Сначала существует нейтральное storage/retrieval. Потом Salience/Appraisal/Valuation могут регулировать retention/replay/consolidation. Это уменьшает циклические design dependencies.

---

# 38. Параллельность design-работ

По умолчанию `DU` выполняются последовательно.

Допускается параллельный research без принятия решений, если темы независимы. Например, можно заранее собирать literature notes по World Model и Cortex.

Но canonical update не должен приниматься, если его inputs ещё не определены предыдущими prerequisites.

Пример:

```text
можно заранее исследовать Dreamer-подходы
нельзя зафиксировать World Model contract
до принятия Environment/Representation semantics
```

---

# 39. Правило изменения порядка

Этот план не является догмой.

Если при выполнении `DU-N` выясняется, что следующий update требует нового фундаментального вопроса:

1. зафиксировать blocker;
2. определить новый/переставленный Design Update;
3. обновить dependency graph;
4. обновить `current.md`;
5. только потом продолжать.

Нельзя решать фундаментальный blocker внутри downstream module document как локальный implementation detail.

---

# 40. Текущий следующий шаг

После завершения `DU-00` следующий допустимый update:

```text
DU-01 — System Context
```

После него:

```text
DU-02 — Dependency & Composition Rules
→ DU-03 — Runtime / Temporal Model
→ DU-04 — CognitiveState Semantics
```

Детальный design когнитивных модулей до завершения этого фундамента считается преждевременным.
