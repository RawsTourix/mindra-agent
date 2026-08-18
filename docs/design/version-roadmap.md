# Version Roadmap MINDRA

## Статус документа

**Design Update:** `DU-32 — Version Roadmap`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ разбивает semantic-frozen architecture `F31` на последовательность software milestones, которые можно реализовывать и проверять независимо, не заставляя implementation agent заново выбирать архитектуру.

`DU-32` **не меняет** semantic contracts `F31`, не выбирает окончательные neural algorithms и не разрешает начинать coding до принятия version-specific design/implementation sequence соответствующего milestone.

Главный результат:

> MINDRA реализуется как **вертикальная capability ladder**: от deterministic contract/runtime kernel к минимальному agent loop, затем к памяти/моделям/внутренней динамике, adaptive cognition, training и research-grade evaluation.

Решение дополнительно зафиксировано в `ADR-0032`.

---

# 1. Почему roadmap не повторяет порядок DU

Порядок `DU-07 … DU-30` был порядком **архитектурного проектирования зависимостей**, а не оптимальным порядком coding.

Если реализовывать буквально:

```text
Environment
→ Perception
→ Goals
→ Cortex
→ Memory
→ ...
→ Policy только почти в конце
```

то значительная часть ранних версий не сможет выполнить ни одного end-to-end Environment interaction.

Поэтому software roadmap использует другой принцип:

```text
вертикальный runnable slice
+
No*/Dummy/control implementations
+
semantic-frozen F31 contracts
        ↓
следующая версия заменяет/расширяет только нужные implementations
```

Например минимальная `Policy` появляется уже в `v0.2`, хотя полноценный Planner/Executive integration проектируется только к `v0.9`.

Это **не нарушение F31**: semantic boundary Policy уже frozen; ранняя версия использует простую reference/control implementation этой boundary.

---

# 2. Общие правила всех software milestones

Каждая версия обязана:

1. быть запускаемой и вертикально проверяемой;
2. сохранять semantic baseline `F31`;
3. не требовать intentional rewrite уже принятого public/internal meaning следующей версией;
4. иметь explicit scope и non-goals;
5. иметь version-specific `VerificationObligation`/acceptance gate;
6. сохранять provenance/revision semantics с момента появления соответствующей boundary;
7. добавлять snapshot/checkpoint support одновременно с causally relevant state, а не задним числом;
8. добавлять observability одновременно с mechanism;
9. иметь честный `No*`/Dummy/control path для optional/conditional boundaries;
10. не вводить learned mechanism до существования deterministic/reference test oracle для его responsibility, где это practically возможно.

Переход к следующему milestone запрещён, если текущая версия требует semantic deviation от F31, не оформленную новым ADR.

---

# 3. Cross-cutting infrastructure развивается с первой версии

Некоторые DU не откладываются до одного позднего milestone, а расширяются **кумулятивно**.

## Engineering Verification

Начинается в `v0.1` и расширяется каждой версией.

## Evidence / Experience

Trace foundation появляется в `v0.1`; causal `Experience Journal` — с первого Environment interaction в `v0.2`.

## Checkpoint / Restore

Минимальная state capture появляется вместе с первым stateful Agent; полноценный persistent Agent checkpoint — в `v0.4`; training-resume semantics — в `v0.10`.

## Evaluation

Каждая версия имеет acceptance metrics. Полный generic `MINDRA-Eval` harness становится отдельной завершённой capability в `v0.11`.

## Research Claims

До research-grade harness результаты считаются development/exploratory evidence. Полный versioned Claim lifecycle подключается в `v0.11`.

---

# 4. Reference compute profiles

Roadmap обязан оставаться пригодным для ограниченного consumer compute.

Эти profiles — **planning budgets**, не архитектурные свойства Agent.

## `C0 — CPU Core`

Цель:

- deterministic runtime;
- contracts;
- MicroWorld;
- control implementations;
- unit/property/integration tests.

Core correctness MINDRA не должна требовать GPU.

## `C1 — Consumer GPU`

Ориентир:

```text
~8 GB VRAM class
~16 GB host RAM class
```

Используется для:

- небольшого Cortex inference;
- небольших neural providers;
- ограниченных local training experiments.

Milestone не должен считаться engineering-correct только потому, что доступен C1.

## `C2 — Burst Accelerator / Notebook Runtime`

Например hosted notebook/Colab-like runtime.

Используется для:

- более тяжёлого Cortex inference;
- PEFT/adapters;
- repeated training/evaluation runs.

Из-за переменной доступности hardware version design обязан поддерживать:

- checkpoint/resume;
- device discovery;
- отсутствие hardcoded GPU model;
- explicit compute provenance.

## `C3 — Optional larger compute`

Более мощный accelerator/remote provider разрешён для масштабных comparisons, но **не является обязательным условием engineering completeness MINDRA 1.0**.

---

# 5. Сводный roadmap

| Версия | Название | Главный результат | Основной compute |
|---|---|---|---|
| `v0.1` | Core Kernel | exact runtime/contracts substrate | C0 |
| `v0.2` | MicroWorld Interaction | первый end-to-end Agent loop | C0 |
| `v0.3` | Cortex Gateway | сменный Cortex без coupling | C0 + optional C1/C2 |
| `v0.4` | Memory & Restore | persistent Memory + causal restore | C0 |
| `v0.5` | World & Self | explicit World/Self models | C0 + optional C1 |
| `v0.6` | Intrinsic / Drives / Appraisal | event meaning + regulatory dynamics | C0 |
| `v0.7` | Affect / Valuation / Salience | persistent modulation → decision evidence | C0 |
| `v0.8` | Memory Regulation / Workspace | bounded memory + shared cognitive bottleneck | C0 + optional C1 |
| `v0.9` | Executive / Planner | adaptive cognition + optional planning | C0 + optional C1/C2 |
| `v0.10` | Training & Revision Lifecycle | first safe learnable update pipeline | C1/C2, C0 toy path |
| `v0.11` | Research Harness | full Eval/Verification/Claims workflow | C0 smoke + C2 experiments |
| `v0.12` | Integration Hardening | release-candidate quality | C0 mandatory + optional C1/C2 |
| `v1.0` | Research Baseline | first stable MINDRA research release | portable; reference study may use C2 |

---

# 6. `v0.1 — Core Kernel`

## Цель

Создать минимальное software основание, на котором все последующие modules смогут появляться без изменения basic execution semantics.

## Scope

Главным образом:

```text
DU-01 System Context
DU-02 Dependency/Composition
DU-03 Logical Time
DU-04 CognitiveState
DU-05 Module Protocol/Scheduler
DU-06 Observability/Intervention foundation
DU-29 Engineering Verification foundation
```

## Обязательные capabilities

- package/application skeleton;
- explicit Composition Root;
- config/profile loading boundary;
- stable logical IDs/revisions/provenance primitives;
- semantic availability model;
- committed `CognitiveState`;
- staged owner-scoped updates;
- module descriptors/contracts;
- DAG/wave scheduler;
- module-private transactional state support;
- causal trace/evidence envelope;
- basic intervention test seam;
- initial `VerificationMatrix`;
- architecture dependency tests.

## Reference composition

Только synthetic deterministic modules.

Никаких LLM, Memory Store, RL или реального Environment.

## Gate

Должно быть машинно доказано минимум:

```text
same-wave modules read same base revision
partial writes invisible before commit
illegal write rejected
stale update rejected/recomputed by declared policy
module failure does not create partial commit
runtime Service Locator absent
trace reconstructs wave/commit lineage
```

CPU-only deterministic suite обязательна.

## Non-goals

- решение Environment task;
- Cortex;
- persistent Memory;
- learning;
- research claims.

---

# 7. `v0.2 — MicroWorld Interaction`

## Цель

Получить **первого реально исполняемого агента**, пусть ещё почти без когнитивных наворотов.

## First implemented boundaries

```text
DU-07 Environment
DU-08 Perception
DU-09 Goals
DU-23 Policy — простая reference implementation
DU-24 Action Boundary
DU-25 Experience Journal — минимальный source layer
```

## Reference loop

```text
MicroWorld
→ Observation
→ Canonical Percept
→ Goal state
→ deterministic/reference Policy
→ SelectedActionIntent
→ authorization
→ Action Commit
→ dispatch
→ Environment Transition
→ Outcome Commit
→ ExperienceEvent
```

## Обязательные capabilities

- deterministic MicroWorld profile;
- two-plane Environment boundary;
- Perception ingress/canonical representation;
- минимальный committed Goal Graph;
- heuristic/control Policy;
- Action Gate/Executor;
- termination/truncation;
- `execution_unknown` test path;
- append-only causal `Experience Journal`;
- episode/session identities;
- minimal task/behavior metrics.

## Gate

- одна или несколько deterministic tasks проходят end-to-end;
- same seed/profile повторяет заявленную deterministic trajectory;
- hidden world sentinel не попадает в Agent path;
- `SelectedActionIntent`, `Action Commit`, dispatch и transition различимы в evidence;
- definite dispatch failure и `execution_unknown` имеют разные outcomes;
- journal позволяет восстановить causal interaction history.

## Non-goals

- Cortex;
- Memory;
- World/Self Model;
- learned Policy;
- complex evaluation.

---

# 8. `v0.3 — Cortex Gateway`

## Цель

Подключить LLM как **сменную capability Agent**, не превращая MINDRA в wrapper одной модели.

## Scope

`DU-10 — Cortex Boundary` + необходимые integration points в существующем loop.

## Обязательные implementations

Минимум:

```text
NoCortex
Deterministic/Mock Cortex
one real Cortex adapter profile
```

Real adapter может быть local или remote; roadmap не фиксирует конкретную модель/provider.

## Capabilities

- capability negotiation;
- semantic request/response;
- context projection без ambient Agent access;
- structured-output validation;
- timeout/degradation/failure handling;
- model/backend revision provenance;
- optional feature/activation hooks только через declared capability;
- Cortex-free execution остаётся работоспособным.

## Gate

- backend заменяется через composition без переписывания consumers;
- `NoCortex` проходит core interaction suite;
- provider-specific objects не протекают в canonical state;
- malformed/timeout result fail/degrade according contract;
- Cortex не получает evaluator Ground Truth или весь Memory автоматически.

## Compute

Core tests — C0.

Real model inference — optional C1/C2.

---

# 9. `v0.4 — Memory & Restore`

## Цель

Сделать Agent **исторически продолжающимся объектом**, а не stateless episode runner.

## First implemented boundaries

```text
DU-11 Memory Core
DU-27 AgentSnapshot/Checkpoint — baseline scope
```

## Capabilities

- canonical `MemoryRecord` store;
- explicit write proposal/structural validation;
- retrieval request/result;
- rebuildable derived representation/index baseline;
- episode/session/persistent scopes;
- memory revision;
- source fidelity/provenance;
- Agent snapshot of all currently causally relevant state;
- persistent manifest-driven checkpoint;
- deterministic restore/fork profile;
- index rebuild without changing record identity.

## Gate

- Episode B может использовать memory evidence из Episode A;
- `Environment.reset()` не уничтожает persistent Memory;
- index loss/rebuild не уничтожает canonical records;
- checkpoint round-trip возвращает тот же semantic state в deterministic profile;
- fork branches имеют отдельный lineage;
- `CognitiveState ≠ Memory Store ≠ AgentSnapshot` соблюдается.

## Non-goals

- importance-based retention;
- consolidation;
- Training Replay.

---

# 10. `v0.5 — World & Self Models`

## Цель

Добавить explicit models внешней ситуации и собственных возможностей Agent.

## First implemented boundaries

```text
DU-12 World Model
DU-13 Self Model
```

## Capabilities

- current belief state;
- assimilation observed evidence;
- prediction отдельно от observation;
- small-horizon imagination/counterfactual representation;
- uncertainty where supported;
- capability/self facts;
- competence estimates;
- success/uncertainty predictions;
- calibration-ready outputs;
- versioned representation/provenance.

Reference implementations сначала могут быть rule-based/deterministic.

## Gate

- predicted/imaged state никогда не masquerade как observed fact;
- controlled world-model intervention меняет заявленный downstream path;
- Self Model prediction имеет measurable target;
- stale competence после revision change обнаруживается/маркируется;
- module-specific metrics существуют отдельно от final task score.

---

# 11. `v0.6 — Intrinsic / Drives / Appraisal`

## Цель

Ввести первые внутренние dynamics, отличающие **свойство опыта**, **регулируемое состояние** и **контекстное значение события**.

## First implemented boundaries

```text
DU-14 Intrinsic Signals
DU-15 Drives
DU-16 Appraisal
```

## Capabilities

- typed intrinsic providers;
- normalization/provenance/status;
- persistent typed Drive state;
- target/range/recovery/dynamics;
- event-centered multidimensional Appraisal;
- explicit dependence on Goal/World/Self/Drive context;
- interventions/control implementations.

## Gate

Должно быть различимо:

```text
novelty signal
≠ novelty-seeking Drive
≠ event Appraisal
```

Дополнительно:

- noisy/stochastic stimulus не обязан автоматически получать максимальную useful curiosity;
- Drive state имеет persistence/recovery;
- один и тот же event может иметь разный Appraisal при разном Goal/Drive context;
- никакой provider не пишет hidden reward/value scalar автоматически.

---

# 12. `v0.7 — Affect / Valuation / Salience`

## Цель

Замкнуть первый полный путь от истории событий к decision-relevant внутреннему состоянию и распределению обработки.

## First implemented boundaries

```text
DU-17 Affect
DU-18 Valuation
DU-19 Salience / Attention
```

## Capabilities

- history-dependent persistent Affect state;
- explicit decay/inertia/recovery;
- typed multi-objective `ValueProfile`;
- comparison/scalarization boundary only where needed;
- risk/constraint/incomparability support;
- `SalienceProfile` отдельно от `AttentionAllocation`;
- explicit attention budget;
- Policy может читать declared decision evidence без ownership transfer.

## Gate

- Affect intervention имеет history-dependent measurable downstream effect;
- matched recurrent-state control существует;
- Valuation не сворачивается неявно в один universal reward;
- conflicting/value-constraint scenarios диагностируемы;
- Random/Uniform/ValueOnly/NoveltyOnly salience controls доступны;
- final Policy attribution остаётся отдельно от Action Gate.

---

# 13. `v0.8 — Memory Regulation / Workspace`

## Цель

Добавить bounded information retention и bounded shared cognitive access.

## First implemented boundaries

```text
DU-20 Memory Regulation / Consolidation
DU-21 Workspace
```

## Capabilities

- `MemoryBudget`;
- policy admission/retention/forgetting/eviction;
- cognitive forgetting отдельно от physical deletion;
- Agent Memory replay/reactivation;
- source-preserving derived consolidation;
- representation maintenance;
- bounded Workspace;
- explicit candidate/admission/replacement;
- shared broadcast to declared consumers;
- temporary persistence;
- `NoWorkspace` и matched buffer controls.

## Gate

- Memory Core остаётся единственным owner canonical Store;
- replay frequency не становится natural experience count;
- consolidation не делает optimizer update;
- derived memory сохраняет source lineage;
- Workspace capacity реально ограничивает access;
- direct-reads/NoWorkspace/matched recurrent/shared buffer controls запускаются тем же harness;
- Workspace state входит в snapshot/restore.

---

# 14. `v0.9 — Executive / Planner`

## Цель

Добавить adaptive management самого cognitive process и optional long-horizon planning.

## First implemented boundaries

```text
DU-22 Executive Control
DU-23 Planner — полный optional provider path
```

Policy boundary из `v0.2` остаётся owner final `SelectedActionIntent`.

## Capabilities

- `CognitiveResourceEnvelope`;
- typed internal MetaAction proposals;
- adaptive decisions продолжить/остановить/распределить cognition;
- Scheduler исполняет только разрешённые meta-actions;
- Planner создаёт plans/action candidates, но не final action intent;
- search/rollout provenance;
- reactive/no-planner path остаётся first-class.

## Gate

- Executive не меняет dependency graph/write authority;
- Adaptive Executive сравнивается с Fixed Schedule при matched actual compute;
- Planner сравнивается с Reactive/Depth-1/Random-Shuffled/MatchedSearch controls;
- long-horizon MicroWorld suite показывает различимую planner responsibility;
- Policy остаётся единственным normal owner `SelectedActionIntent`.

---

# 15. `v0.10 — Training & Revision Lifecycle`

## Цель

Впервые безопасно изменить learned parameters MINDRA без скрытой мутации live Agent.

## Completed/expanded boundaries

```text
DU-25 Experience/Data/Replay — full dataset projections
DU-26 Training Lifecycle
DU-27 Training-resume checkpoint scope
```

## Capabilities

- versioned `DatasetManifest`;
- `TrainingSample` + transformation lineage;
- explicit `DataVisibilityPolicy`;
- Training Replay infrastructure;
- `TrainingPlan`;
- parameter/optimizer ownership;
- `GradientFlowPolicy`;
- pinned base revisions;
- candidate revision bundle;
- validation;
- atomic activation;
- rollback/history;
- behavior vs learner revision provenance;
- optimizer/scheduler/RNG resume state.

## First trainable target

Roadmap **не требует** сразу fine-tune всего Cortex.

Предпочтительно начать с одного небольшого trainable provider/adaptor, где можно получить дешёвый measurable target, например:

- small World/Self predictor;
- compact Policy/Valuation provider;
- small adapter поверх replaceable Cortex.

Exact target выбирается version design.

## Gate

- training не мутирует active Agent до activation;
- failed/OOM/invalid candidate оставляет live Agent unchanged;
- source experience не переписывается relabeling'ом;
- behavior revision известна для training sample;
- held-out metric для first trainable target улучшается по заранее заданному criterion;
- activation создаёт новую Agent revision;
- training resume из checkpoint воспроизводит заявленный lifecycle.

## Compute

Обязателен C0 tiny/toy training path для engineering tests.

Практический neural training ориентирован на C1/C2. Full fine-tuning large Cortex не является milestone requirement.

---

# 16. `v0.11 — Research Harness`

## Цель

Превратить интегрированную систему в **research instrument**, а не только runnable agent.

## Completed boundaries

```text
DU-27 full Experiment/Compute/Reproducibility manifests
DU-28 MINDRA-Eval
DU-29 Engineering Verification
DU-30 Research Claims / Limitations
```

## Capabilities

- reproducibility/compute manifests;
- evaluation conditions/suites/runs/units;
- replicate structure;
- statistical analysis plans;
- paired counterfactual experiments from verified checkpoints;
- matched controls/resource matching;
- module gates;
- calibration/robustness/compute metrics;
- full VerificationObligation/Matrix workflow;
- fault-injection profiles;
- Claim/Limitations/KnownUnknown registries;
- evidence → observation → interpretation → claim lineage.

## Reference study

Версия обязана провести хотя бы один complete study pipeline:

```text
StudyPlan
→ Conditions
→ Runs/Replicates
→ Evaluation Evidence
→ Engineering Validity
→ Observation
→ Interpretation
→ Scoped ResearchClaim / Negative/Inconclusive result
```

Study выбирается так, чтобы быть достаточно дешёвым; он не обязан доказывать пользу всей MINDRA.

## Gate

- Engineering Verification и MINDRA-Eval дают разные evidence artifacts;
- evaluator Ground Truth не попадает Agent;
- statistical unit/replicate structure explicit;
- actual compute входит в comparison;
- claim не сильнее supporting evidence/scope;
- negative/null/inconclusive/invalid различаются;
- paired counterfactual разрешён только при достаточном restore profile.

---

# 17. `v0.12 — Integration Hardening`

## Цель

Не добавлять новые cognitive mechanisms, а превратить весь accumulated stack в release candidate.

## Scope

Все boundaries F31, реализованные roadmap к этому моменту.

## Работы

- schema/revision migration;
- checkpoint compatibility/migration;
- backend/capability matrix;
- deterministic CPU reference profile;
- optional consumer-GPU profile;
- fault-injection/recovery hardening;
- corrupted artifact/checkpoint fail-closed paths;
- performance profiling;
- resource leaks/cleanup;
- install/package/entry-point polish;
- documentation consistency;
- experiment reproducibility from clean environment;
- no hidden TODO, который требует architecture decision.

## Gate

- нет unresolved blocking `VerificationObligation`;
- все F31 invariants, затронутые v1.0 reference composition, имеют evidence;
- checkpoint corruption/missing dependency не приводит к silent partial restore;
- external `execution_unknown` не допускает unsafe retry;
- reference profiles запускаются из clean checkout;
- optional backend absence не ломает CPU/core profile;
- migrations versioned/tested;
- known limitations документированы.

---

# 18. `v1.0 — MINDRA Research Baseline`

## Цель

Первый стабильный исследовательский release.

`v1.0` **не добавляет новый механизм**. Он является promotion `v0.12` после acceptance.

## Reference composition profiles

Минимально должны существовать несколько явных профилей.

### `minimal-deterministic`

- CPU-only;
- deterministic MicroWorld;
- NoCortex/control implementations;
- используется как engineering/reference oracle.

### `cortex-assisted`

- replaceable real Cortex;
- остальная архитектура та же;
- Cortex можно заменить без redesign.

### `full-cognitive`

- включает все F31 cognitive boundaries, которые reference release поддерживает как real/control implementations;
- conditional modules остаются явно отключаемыми.

### `trainable-research`

- включает хотя бы один safe Training Runtime path;
- candidate/validation/activation lifecycle;
- reproducible research pipeline.

## Release gate

`v1.0` допускается только если:

- `v0.12` engineering gates green;
- reference study reproducible в заявленном scope;
- exact version contracts/API задокументированы;
- all active F31 boundaries имеют explicit implementation/control status;
- no hidden privileged path;
- no untracked breaking semantic deviation from F31;
- known limitations/known unknowns опубликованы;
- release claim wording соответствует DU-30.

## Что `v1.0` НЕ означает

```text
AGI achieved
consciousness demonstrated
subjective emotions demonstrated
all modules empirically necessary
all modules end-to-end trained
large-scale distributed training solved
universal benchmark superiority
```

`v1.0` означает:

> существует стабильная модульная исследовательская платформа, на которой hypotheses MINDRA можно воспроизводимо проверять.

---

# 19. Dependency graph software milestones

```text
v0.1 Core Kernel
   ↓
v0.2 MicroWorld Interaction
   ↓
v0.3 Cortex Gateway
   ↓
v0.4 Memory & Restore
   ↓
v0.5 World & Self
   ↓
v0.6 Intrinsic / Drives / Appraisal
   ↓
v0.7 Affect / Valuation / Salience
   ↓
v0.8 Memory Regulation / Workspace
   ↓
v0.9 Executive / Planner
   ↓
v0.10 Training & Revision Lifecycle
   ↓
v0.11 Research Harness
   ↓
v0.12 Integration Hardening
   ↓
v1.0 Research Baseline
```

Параллельная implementation работа внутри одного milestone допустима только после принятия его version specification и если dependency boundaries позволяют независимые branches.

---

# 20. Mapping F31 boundary → first substantial software milestone

| Boundary | Первый substantial milestone |
|---|---|
| System/Dependency/Time/State/Scheduler/Observability | `v0.1` |
| Environment | `v0.2` |
| Perception | `v0.2` |
| Goals | `v0.2` |
| Policy baseline | `v0.2` |
| Action Boundary | `v0.2` |
| Experience Journal baseline | `v0.2` |
| Cortex | `v0.3` |
| Memory Core | `v0.4` |
| AgentSnapshot/Checkpoint baseline | `v0.4` |
| World Model | `v0.5` |
| Self Model | `v0.5` |
| Intrinsic Signals | `v0.6` |
| Drives | `v0.6` |
| Appraisal | `v0.6` |
| Affect | `v0.7` |
| Valuation | `v0.7` |
| Salience | `v0.7` |
| Memory Regulation | `v0.8` |
| Workspace | `v0.8` |
| Executive Control | `v0.9` |
| Planner | `v0.9` |
| Experience/Data projections full | `v0.10` |
| Training Lifecycle | `v0.10` |
| Training-resume Checkpoint | `v0.10` |
| MINDRA-Eval full harness | `v0.11` |
| Engineering Verification full workflow | `v0.11` |
| Research Claims / Limitations registry | `v0.11` |
| Integration/release hardening | `v0.12` |

Это mapping implementation introduction, а не изменение canonical owner.

---

# 21. Почему neural training отложен до v0.10

MINDRA исследует вклад architecture, поэтому преждевременный end-to-end learning создаёт максимальный confounding.

До первого серьёзного training milestone должны уже существовать:

- deterministic runtime semantics;
- explicit modules/contracts;
- Environment/MicroWorld;
- source-preserving Experience Journal;
- Memory/World/Self/internal dynamics;
- intervention/observability;
- snapshots/checkpoints;
- stable decision/action attribution.

Тогда можно спрашивать:

> что изменилось из-за обучения?

а не:

> какая из десятков одновременно меняющихся деталей случайно дала этот результат?

Parameter-efficient/adaptor training допускается как implementation candidate для ограниченного compute, но конкретный метод выбирается только `v0.10` version design.

---

# 22. Почему Cortex появляется рано, а его training поздно

Cortex нужен рано, чтобы:

- проверить replaceable LLM boundary;
- тестировать structured context/response;
- использовать языковую capability в дальнейших modules;
- не проектировать всё на Mock-only assumptions.

Но его parameters не обязаны меняться.

```text
v0.3:
Cortex inference capability

v0.10+:
optional adapter/fine-tuning experiment
```

Это сохраняет главный принцип:

```text
Cortex ≠ вся MINDRA
```

---

# 23. Version-specific design process после DU-32

Roadmap **не является прямым заданием Codex писать весь проект**.

Перед каждой версией выполняется отдельный design pass.

Для milestone `vX.Y` создаются минимум:

```text
docs/versions/vX.Y/README.md
docs/versions/vX.Y/implementation-sequence.md
```

Version README фиксирует:

- цели;
- exact scope;
- selected technologies/implementations;
- exact contract representations;
- config/defaults;
- compatibility assumptions;
- VerificationObligations;
- acceptance evidence;
- non-goals.

`implementation-sequence.md` переводит уже принятый version design в последовательные задания Codex.

Только после принятия обоих документов начинается implementation milestone.

---

# 24. Правило изменения roadmap

Roadmap может измениться без нового architecture ADR, если меняется только:

- grouping milestones;
- порядок implementation деталей;
- конкретный tool/backend;
- compute strategy;
- version numbering,

при сохранении F31 semantics.

Если обнаружен semantic blocker:

```text
implementation/research blocker
→ design review
→ новый ADR
→ новая freeze baseline revision
→ roadmap update
```

Нельзя исправлять architectural mismatch простым перемещением ответственности между версиями.

---

# 25. Gate DU-32

`DU-32` выполнен, если:

- каждый milestone dependency-complete;
- первая версия не требует GPU;
- первый runnable Agent появляется рано;
- Cortex заменяем и optional;
- stateful modules сразу учитывают snapshot/restore;
- Experience/Verification не добавляются задним числом;
- training появляется только после causal/data foundations;
- research harness существует до `v1.0` claims;
- `v1.0` не требует large-scale compute;
- ни одна версия не требует Codex менять F31 semantics;
- следующим шагом является **version design `v0.1`**, а не coding всей системы.

Gate выполнен.

---

# 26. Итог

Canonical sequence:

```text
F31 semantic architecture
        ↓
DU-32 Version Roadmap
        ↓
v0.1 version design
        ↓
v0.1 implementation sequence
        ↓
v0.1 implementation + verification
        ↓
v0.2 version design
        ↓
...
        ↓
v0.12 release candidate
        ↓
v1.0 MINDRA Research Baseline
```

После `DU-32` общий архитектурный Design Update cycle `DU-00 … DU-32` считается завершённым.

Следующая разрешённая работа:

```text
Version Design — v0.1 Core Kernel
```
