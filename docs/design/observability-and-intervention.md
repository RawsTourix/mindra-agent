# Наблюдаемость и controlled intervention MINDRA

## Статус документа

**Design Update:** `DU-06 — Observability & Intervention`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет исследовательскую наблюдаемость MINDRA, causal tracing, границы inspection private state и семантику controlled intervention поверх:

- [`system-context.md`](system-context.md) — логических границ Agent/Evaluation/Artifact infrastructure;
- [`dependency-rules.md`](dependency-rules.md) — направления зависимостей и запрет hidden coupling;
- [`execution-model.md`](execution-model.md) — logical causal time и commit boundaries;
- [`cognitive-state.md`](cognitive-state.md) — committed state revisions, provenance и forks;
- [`module-lifecycle.md`](module-lifecycle.md) — execution plan, waves, module attempts и atomic commit.

Документ намеренно **не** определяет:

- конкретный telemetry framework;
- OpenTelemetry как обязательную зависимость;
- конкретную базу логов/метрик;
- exact Python API probes/interventions;
- окончательный artifact schema;
- exact full `Agent Snapshot` format;
- Environment clone/restore API;
- конкретные Cortex backend hooks;
- конкретные statistical metrics causal effect;
- exact Evaluation Harness;
- конкретную политику хранения больших raw activations.

Эти решения относятся к последующим Design Updates и version planning.

---

# 1. Цель DU-06

MINDRA является исследовательским проектом. Возможность увидеть итоговый action или reward недостаточна, если нужно проверить функциональную роль отдельных механизмов.

`DU-06` отвечает на два разных вопроса:

1. **Что именно произошло внутри архитектуры и можно ли восстановить причинный ход исполнения?**
2. **Можно ли контролируемо изменить ограниченный фактор и измерить последствия, не превратив evaluator в скрытую часть cognition?**

После принятия `DU-06` должно быть однозначно понятно:

- какие execution events являются обязательным causal evidence;
- чем trace отличается от metric и debug dump;
- как tracing связывается с Run/Session/Episode/Decision/Cycle/Wave/Module Attempt;
- как наблюдать canonical state без изменения его semantics;
- как наблюдать causally relevant private state без прямого доступа к mutable implementation object;
- почему raw Cortex/backend activations требуют отдельного opt-in режима;
- где проходит граница между passive observability и active intervention;
- какие классы intervention допускаются;
- на каких causal boundaries intervention может применяться;
- как intervention влияет на lineage и provenance;
- как сохраняются natural value и treatment value;
- когда counterfactual fork считается корректным, а когда только приближённым replay;
- как учитывать intervention-induced out-of-distribution state;
- как observability failure влияет на валидность эксперимента;
- как не позволить tracing metadata стать cognitive input.

---

# 2. Главное архитектурное решение

MINDRA принимает **разделённую архитектуру passive Evidence Plane и explicit Intervention Gateway**.

Каноническая схема:

```text
                    MINDRA Agent
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
 canonical execution              declared research
 events / snapshots                  probes
          │                             │
          └──────────────┬──────────────┘
                         ▼
                 Evidence Plane
                         │
                         ▼
                 Artifact Collector
                         │
                         ▼
                  Artifact Storage

Evaluation Runtime
        │
        ▼
Intervention Gateway
        │ explicit treatment
        ▼
committed boundary / declared target
        │
        ▼
new experimental lineage / revision
```

Ключевые invariants:

```text
Observability
≠
Intervention
```

```text
trace metadata
≠
cognitive input
```

```text
natural execution
≠
intervened execution
```

```text
inspection capability
≠
write authority
```

Passive observer не получает права изменять Agent только потому, что имеет доступ к evidence.

Active intervention не маскируется под обычный module output или observation.

Это решение дополнительно зафиксировано в `ADR-0006`.

---

# 3. Evidence Plane

## 3.1. Назначение

`Evidence Plane` — логическая однонаправленная поверхность, через которую Agent/runtime публикуют исследовательски значимые копии событий, snapshot metadata и diagnostics во внешнюю artifact infrastructure.

Evidence Plane:

- не является cognitive module;
- не является Memory;
- не является state bus;
- не определяет action;
- не возвращает evaluator score в cognition;
- не создаёт hidden dependency Agent от logger/backend.

## 3.2. Логическая принадлежность

Producer-side instrumentation может физически находиться внутри Agent runtime core или module adapter, но получатель evidence логически относится к external Artifact/Evaluation infrastructure.

Канонический поток:

```text
Agent/runtime
    ↓ copies / events
Evidence Plane
    ↓
Artifact Collector
```

Normal execution не имеет обратного dataflow из Artifact Collector.

## 3.3. Наблюдение не даёт ownership

Если collector получил копию:

- `CognitiveState`;
- private-state projection;
- module output;
- raw activation;

это не меняет semantic owner исходных данных.

---

# 4. Три класса observability data

MINDRA различает как минимум три класса evidence.

## 4.1. Trace events

Структурированные causally ordered события конкретного исполнения.

Они отвечают на вопрос:

> что произошло, в каком causal context и с каким результатом?

## 4.2. Metrics

Производные числовые измерения/агрегации.

Примеры conceptually:

- latency;
- количество module attempts;
- prediction error;
- memory size;
- success rate.

Metric не заменяет raw causal trace.

## 4.3. Diagnostic artifacts

Более тяжёлые или специализированные данные:

- state snapshots;
- private-state exports;
- raw activations;
- gradients;
- search trees;
- profiler traces;
- debug dumps.

Они могут собираться выборочно и не обязаны присутствовать в каждом Run.

---

# 5. Canonical trace hierarchy

Trace model должен сохранять уже принятую temporal/scheduler иерархию.

Conceptually:

```text
Run
└── Agent Session
    └── Episode
        └── Decision Window
            └── Cognitive Cycle
                ├── Execution Plan / segment
                ├── Wave Attempt
                │   ├── Module Attempt A
                │   ├── Module Attempt B
                │   └── Module Attempt C
                └── Commit Attempt
```

Рядом существуют отдельные causal events:

```text
Action Commit
Environment Transition
Outcome Commit
Learning Update
Replay Step
Consolidation Event
Intervention Event
Fork Event
Restore Event
```

Trace nesting является способом навигации; причинность определяется identifiers/lineage/links, а не только красивым деревом.

---

# 6. Обязательные causal identities

Evidence должна позволять коррелировать событие минимум с применимыми identifiers из уже принятой temporal model.

Conceptually могут использоваться:

```text
run_id
agent_session_id
episode_id
decision_id
cognitive_cycle_id
execution_plan_id / revision
wave_id / wave_attempt_id
module_identity
module_attempt_id
state_revision
agent_revision
environment_transition_id
learning_update_id
replay_step_id
consolidation_id
intervention_id
branch_id / lineage_id
```

Exact names/type/schema определяются позже.

Не каждое событие обязано содержать все identifiers физически, если они однозначно наследуются через trace context.

---

# 7. Attempt и Commit — разные evidence events

Очень важно различать:

```text
модуль вычислялся
≠
его результат стал committed
```

Поэтому trace должен сохранять не только успешный commit, но и attempts, которые были:

- успешны и committed;
- успешны, но отброшены как stale;
- отклонены validation;
- завершились error;
- отменены вследствие failure другого required module wave;
- retried/recomputed.

Иначе post-hoc анализ увидит только «чистую историю победителей» и потеряет причины failure/degradation.

---

# 8. Wave tracing

Для каждой execution wave evidence должна позволять восстановить:

- base `state_revision`;
- закреплённую `agent_revision`;
- active execution plan;
- список scheduled modules;
- declared dependency context;
- module attempt outcomes;
- proposed writes metadata;
- validation/conflict result;
- commit success/failure;
- resulting `state_revision`, если commit состоялся;
- failure/degradation decision.

Physical completion timestamps допустимы как profiler metadata, но не определяют logical ordering.

---

# 9. State observability

## 9.1. Canonical state

Committed `CognitiveState` является естественной research observation boundary.

Evaluator/collector может получать:

- state envelope;
- selected cognitive payload fields;
- state diff между revisions;
- availability/freshness/provenance;
- schema/lineage metadata.

## 9.2. Full dump не обязателен

Каждый commit не обязан сохранять полную копию всех tensors.

Допустимы:

- structural diff;
- content-addressed references;
- selected projections;
- periodic full snapshots + deltas;
- sampling.

Но evidence policy конкретного эксперимента должна быть известна заранее настолько, насколько она влияет на возможность causal reconstruction.

## 9.3. Debug metadata отделена от payload

`trace_id`, `experiment_id`, profiler timestamp и другие observability fields не становятся частью cognitive payload только потому, что сопровождают state snapshot.

---

# 10. Private-state observability

`DU-04` разрешил causally relevant module-private state. `DU-06` запрещает исследователю обходить encapsulation через arbitrary object introspection как канонический механизм.

## 10.1. Declared probe/export capability

Модуль, private state которого важен для проверки гипотезы или воспроизводимости, должен позднее предоставлять declared research projection/probe.

Probe может возвращать:

- semantic private-state snapshot;
- summary/statistics;
- stable references;
- backend-specific research artifact,

в зависимости от module design.

## 10.2. Probe является read-only по semantics

Получение private-state evidence не предоставляет evaluator write authority.

Недопустимо:

```text
probe вернул mutable tensor reference
→ evaluator изменил его inplace
→ private state Agent незаметно изменился
```

## 10.3. Encapsulation сохраняется

Downstream cognitive modules не получают право читать private probe output другого модуля.

Research visibility и runtime dependency — разные вещи.

---

# 11. Уровни глубины observability

Для управления стоимостью и backend isolation вводятся conceptual уровни.

## O0 — structural

- module identity;
- attempt status;
- revisions;
- causal links;
- errors;
- commit result.

Минимальный слой для всех серьёзных runs.

## O1 — semantic public

- selected canonical state values;
- availability/freshness;
- proposed/committed semantic outputs;
- module-specific public metrics.

## O2 — semantic private

- declared private-state projections;
- module-internal summaries, имеющие стабильный research meaning.

## O3 — backend/raw

- hidden activations;
- gradients;
- token-level logits;
- KV/cache internals;
- implementation-specific tensors;
- profiler-level backend data.

O3 является opt-in research mode и не должен становиться обязательным capability любого backend.

Exact naming/configuration levels может измениться в implementation; канонически важна **многоуровневая глубина**, а не конкретные символы `O0...O3`.

---

# 12. Cortex/raw activation boundary

Raw activations требуют особой дисциплины.

Причины:

- огромный объём;
- model-specific shapes;
- возможная зависимость от provider/backend API;
- риск сделать конкретную модель обязательной для всей research infrastructure;
- возможное содержание исходных пользовательских/текстовых данных в производной форме.

Поэтому:

1. canonical MINDRA observability не требует raw Cortex activations;
2. raw access реализуется через backend-specific research adapter;
3. такой adapter не меняет общий Cortex semantic contract;
4. отсутствие raw activation access не делает Cortex backend автоматически несовместимым;
5. experiment, которому нужны raw activations, явно объявляет это capability requirement;
6. storage/sampling/retention policy должна быть указана в experiment configuration.

---

# 13. Passive observability invariant

Наблюдение должно быть **семантически пассивным**.

Это означает:

- collector не изменяет input/output module;
- logger не изменяет scheduling order;
- metric callback не вызывает Cortex/Memory/Policy;
- tracing metadata не используется в cognition;
- trace export failure не должен незаметно выбирать другой action;
- sampling decision не должен менять semantic state Agent.

## 13.1. Observer overhead

Instrumentation может физически увеличить latency/VRAM/RAM/disk usage.

Пока wall-clock не является частью Environment contract, такая задержка не меняет logical cognitive time.

Если будущая Environment делает real-time deadline частью задачи, observability overhead становится возможным experimental confounder и должен учитываться отдельно.

---

# 14. Evidence-critical и best-effort telemetry

Не все данные одинаково критичны.

## 14.1. Evidence-critical

Если отсутствие события делает невозможным проверку primary hypothesis или causal reconstruction, run должен быть:

- остановлен;
- либо явно помечен invalid/incomplete для соответствующего claim.

Нельзя молча продолжить и затем анализировать run как полный.

## 14.2. Best-effort

Profiler/debug artifacts могут теряться без изменения поведения, если experiment не требует их как evidence.

Потеря должна быть видима в diagnostics.

## 14.3. Backpressure

Telemetry backpressure не имеет права менять logical ordering cognition.

Concrete runtime позже должен выбирать между buffering, bounded loss, blocking или fail-fast с учётом evidence class.

---

# 15. Metrics являются производными данными

Metric может вычисляться:

- online;
- после Run;
- Evaluation Runtime;
- отдельным analysis pipeline.

Но metric не должна считаться canonical causal fact, если её можно восстановить из raw evidence и определение может меняться.

Особенно:

```text
Evaluator score
≠
Agent internal value
```

и

```text
metric label
≠
cognitive feature
```

---

# 16. Intervention Gateway

`Intervention Gateway` — единственная каноническая research boundary для активного изменения исследуемой системы извне.

Он логически принадлежит **Evaluation Runtime / Research Control Plane**, а не Agent cognition.

Gateway обязан:

- валидировать target;
- проверять base causal revision;
- проверять допустимую intervention phase;
- проверять type/shape/availability semantics;
- присваивать `intervention_id`;
- фиксировать treatment payload/provenance;
- создавать/обозначать экспериментальную lineage;
- применять intervention через разрешённую boundary;
- публиковать evidence о natural/treatment context;
- не менять semantic owner целевого поля.

---

# 17. Intervention не меняет semantic ownership

Если evaluator устанавливает `drive.x = value`, владельцем `drive.x` не становится evaluator.

Правильная семантика:

```text
semantic owner: Drive module
origin/provenance текущего значения: controlled intervention
```

Это позволяет отличить:

```text
Drive сам вычислил 0.8
```

от:

```text
Evaluator принудительно установил 0.8
```

Downstream consumer может читать значение по своему обычному contract, если experiment design разрешает treatment.

---

# 18. Классы intervention targets

MINDRA допускает несколько уровней вмешательства, но каждый требует отдельной capability.

## 18.1. Canonical state intervention

Target — конкретный canonical path/namespace `CognitiveState`.

Применяется через state/intervention commit boundary, а не mutable reference.

## 18.2. Module public-result intervention

Evaluator заменяет/маскирует proposed public result конкретного module attempt до commit.

Это должно быть явно записано как treatment, а natural proposed result желательно сохранить отдельно, если experiment design позволяет.

## 18.3. Module-private semantic intervention

Изменение declared causally relevant private state через специальную module intervention capability.

Запрещён arbitrary object mutation.

## 18.4. Backend/raw representation intervention

Например, activation patching или steering внутри Cortex/neural module.

Такое вмешательство:

- backend-specific;
- opt-in;
- не является обязательным общим `ModuleProtocol`;
- должно иметь explicit target specification и provenance;
- требует особого контроля validity/OOD.

## 18.5. Composition intervention

Ablation/substitution модуля выполняется прежде всего через Composition Root/active plan, как принято `DU-02`/`DU-05`, а не путём runtime удаления объекта evaluator-ом.

---

# 19. Intervention points

Вмешательство должно происходить на **явной причинной границе**.

Минимально допустимые conceptual points:

- после committed state revision и до начала зависимого compute;
- над staged module result до его commit;
- при fork/restore до продолжения branch;
- через backend-specific declared hook внутри одного module compute, если experiment специально исследует internal representation.

По умолчанию запрещено вмешательство:

- в произвольный момент между tensor operations;
- через data race;
- через mutable alias;
- после того как downstream compute уже частично использовал старое значение, если это не отдельный explicit experimental protocol.

---

# 20. Intervention transaction

Conceptual lifecycle:

```text
1. выбрать identifiable committed base
2. проверить target/capability
3. зафиксировать natural/base context
4. создать intervention record
5. fork или открыть explicit treatment transition
6. применить treatment
7. commit intervention-derived state/private state
8. продолжить cognition
9. сохранить resulting trajectory/effect evidence
```

Если intervention не может быть применён атомарно к causally relevant target state, experiment нельзя трактовать как чистое изменение одного фактора.

---

# 21. Default fork semantics

Для confirmatory causal experiments предпочтительный default:

```text
Base Snapshot / Revision
        ├── Control branch
        └── Treatment branch + Intervention
```

Intervention **не переписывает исходную natural lineage**.

Это позволяет сравнить branches и сохранить исходный экспериментальный факт.

## 21.1. In-place experimental treatment

Иногда intervention может применяться в продолжающейся evaluation trajectory без параллельной control branch.

Это допустимо только если:

- treatment момент явно записан;
- lineage после treatment помечена intervened;
- natural post-treatment continuation не выдаётся за наблюдённую;
- experiment design не требует paired counterfactual.

---

# 22. Natural value и treatment value

Где технически и научно осмысленно, evidence должна сохранять:

```text
natural candidate/value
intervention operation
treatment value
resulting committed value
```

Особенно это важно для module-output intervention.

Если natural value невозможно получить без изменения процесса эксперимента, это ограничение должно быть зафиксировано, а не скрыто.

---

# 23. Duration и scope intervention

Каждая intervention должна явно определять duration semantics.

Минимально различимы conceptually:

- one-shot — действует только на один target/commit;
- scope-bound — действует до конца Cycle/Decision/Episode или другого declared scope;
- persistent treatment — сохраняется до explicit release/restore.

Нельзя оставлять treatment «включённым пока кто-нибудь не перезапишет поле случайно».

Termination/release treatment также является evidence event.

---

# 24. Counterfactual fork correctness

Настоящий counterfactual fork требует восстановления **всего causally relevant state**, а не только `CognitiveState`.

Это может включать:

- committed `CognitiveState`;
- module-private state;
- active Memory;
- Cortex/backend causally relevant state;
- Agent revision/parameters;
- RNG state;
- Environment state;
- relevant scheduler/execution-plan identity.

Exact `Agent Snapshot` и checkpoint schema определяются в `DU-27`, Environment clone/restore — в `DU-07`.

## 24.1. Пока полного snapshot нет

Если experiment восстановил только часть причинного состояния, результат должен называться, например:

- partial replay;
- approximate counterfactual;
- controlled re-execution,

но не exact counterfactual clone.

---

# 25. RNG и stochastic branches

Для stochastic Agent/Environment одинаковый snapshot не гарантирует одинаковую дальнейшую trajectory без контроля stochastic state.

Experiment protocol должен явно определить:

- shared RNG continuation;
- независимые branch RNG;
- повторные Monte Carlo continuations;
- другую контролируемую policy.

Выбор зависит от causal question и фиксируется в experiment design.

Сам `DU-06` не устанавливает одну универсальную RNG policy.

---

# 26. Intervention validity и out-of-distribution risk

Сильное изменение internal representation может создать состояние, которое Agent естественно никогда не посещает.

Поэтому causal effect intervention не следует автоматически интерпретировать как естественную функцию переменной.

Для intervention, особенно raw/latent, experiment должен по возможности оценивать:

- magnitude treatment;
- близость к natural distribution/manifold;
- downstream off-target effects;
- intervention specificity;
- stability результата при близких treatments.

Если treatment явно создаёт divergent/OOD state, это часть limitations evidence.

---

# 27. Intervention contamination

Intervened trajectory является отдельным классом данных.

Она не должна молча попадать в:

- natural-behavior statistics;
- replay/training dataset как обычный observed experience;
- calibration dataset;
- baseline metrics,

если experiment/training design явно не разрешает использование treatment data.

Provenance должна позволять фильтровать intervention-derived data.

---

# 28. Module observability contract requirements

Каждый будущий module design должен определить:

1. какие public outputs достаточно видеть на O1;
2. существует ли causally relevant private state;
3. какая его часть доступна через O2 semantic probe;
4. нужен ли O3 backend/raw access;
5. какие module-specific metrics являются диагностическими;
6. какие intervention targets поддерживаются;
7. какие targets намеренно не поддерживаются;
8. какие snapshots нужны для causal fork;
9. какие observability artifacts могут быть слишком велики/дороги;
10. влияет ли instrumentation на numerical/runtime behavior.

Если исследовательская гипотеза требует вмешательства в механизм, а модуль не предоставляет безопасной target boundary, такой модуль не считается research-ready для этой гипотезы.

---

# 29. Observability и module encapsulation

Research access не должен разрушать обычную архитектурную модульность.

Запрещён pattern:

```text
Evaluator
  ↓ imports concrete module class
  ↓ reaches module._hidden_state.foo.bar
  ↓ mutates tensor
```

Допустимый pattern conceptually:

```text
Evaluation Runtime
        ↓
Research capability / probe / intervention adapter
        ↓
semantic target
```

Concrete implementation может использовать hooks/reflection внутри adapter, но это не становится dependency других modules.

---

# 30. Observability и errors

Ошибки instrumentation различаются от ошибок cognition.

Например:

```text
Module succeeded
Artifact exporter failed
```

не равно:

```text
Module failed
```

Но если exporter failure уничтожил evidence-critical данные, run может быть исследовательски invalid.

Следовательно, evidence pipeline должен отдельно отражать:

- Agent/runtime status;
- telemetry status;
- experiment validity status.

---

# 31. Sampling и capture policy

Полный O3 trace каждого шага может быть непрактичен.

Поэтому future experiment configuration должна позволять capture policy, например conceptually:

- always;
- periodic;
- selected modules;
- selected episodes;
- trigger-on-error;
- intervention-only;
- sampled.

Но causal-critical structural metadata O0 не должна исчезать случайно из confirmatory runs, если без неё нельзя реконструировать эксперимент.

Sampling policy является частью experiment provenance.

---

# 32. Security/privacy/size boundary

MINDRA пока не проектирует полную security model, но research artifacts могут содержать:

- исходные observations/text;
- retrieved memory content;
- generated text;
- hidden activations;
- gradients;
- identifiers и experiment metadata.

Поэтому future artifact contract должен позволять классифицировать тяжёлые/чувствительные artifacts и задавать retention/export policy.

Raw Cortex dumps не должны включаться «по умолчанию на всякий случай».

---

# 33. Existing tooling как evidence реализуемости

`DU-06` не выбирает concrete observability/intervention stack.

Однако существующие инструменты подтверждают практичность нескольких требований:

- OpenTelemetry использует traces/spans/attributes/events и correlation context для наблюдения сложных распределённых систем;
- PyTorch предоставляет per-module forward/backward hooks, но некоторые hooks способны модифицировать вход/выход, а global hooks добавляют global state и предназначены главным образом для debugging/profiling;
- pyvene демонстрирует, что интервенции во внутренние состояния PyTorch models можно оформить как отдельный конфигурируемый слой поверх модели.

Эти инструменты рассматриваются как evidence/кандидаты, а не как canonical dependencies.

---

# 34. Принятые invariants DU-06

## OI-01

Observability и Intervention являются разными логическими каналами.

## OI-02

Passive Evidence Plane не является источником normal cognitive input.

## OI-03

Trace должен сохранять causal identities и различать attempt от commit.

## OI-04

Physical timestamps/latency не определяют logical causal order.

## OI-05

Research visibility private state не даёт evaluator write authority и не создаёт runtime dependency других modules.

## OI-06

Private-state inspection выполняется через declared probe/export boundary, а не arbitrary mutable object access как canonical mechanism.

## OI-07

Raw/backend observability является opt-in capability и не протекает в общий semantic contract.

## OI-08

Trace/debug/experiment metadata не становится cognitive payload без явного design.

## OI-09

Evidence-critical telemetry loss делает соответствующий research claim invalid/incomplete, если evidence нельзя восстановить.

## OI-10

Intervention применяется только через explicit Intervention Gateway с `intervention_id`, target и provenance.

## OI-11

Intervention не меняет semantic owner целевого canonical field/module state.

## OI-12

Intervention должен происходить на declared causal boundary; arbitrary race/mutable alias mutation запрещены.

## OI-13

Confirmatory causal intervention по умолчанию предпочитает fork от identifiable committed base вместо переписывания natural lineage.

## OI-14

Intervened trajectory явно маркируется и не смешивается с natural experience без отдельного training/analysis decision.

## OI-15

Exact counterfactual claim требует полного causally relevant Agent + Environment state; partial restore должен называться приближённым.

## OI-16

Stochastic branch policy/RNG semantics являются частью experiment protocol.

## OI-17

Сильные latent/raw interventions требуют оценки validity/OOD и off-target effects.

## OI-18

Instrumentation overhead не меняет logical cognitive time; real-time tasks позже должны учитывать observer overhead как confounder.

## OI-19

Observability backend failure и Agent/module failure являются разными состояниями.

## OI-20

Capture/sampling policy является частью experiment provenance.

---

# 35. Что DU-06 намеренно не решает

Открытыми остаются:

- exact telemetry/event classes;
- exact trace/span implementation;
- OpenTelemetry dependency decision;
- exact artifact storage format;
- exact module probe Python interface;
- exact intervention request/result Python interface;
- concrete state diff representation;
- concrete raw activation capture implementation;
- exact snapshot/checkpoint format;
- Environment clone/restore implementation;
- concrete causal effect estimators;
- exact evaluation metrics;
- statistical test/threshold;
- retention/compression backend;
- UI/visualization stack;
- default production/research capture budgets.

Эти вопросы не должны решаться implementation раньше соответствующих Design Updates/version planning.

---

# 36. Последствия для следующих Design Updates

## DU-07 — Environment / MicroWorld

Должен определить:

- Environment state observability boundary;
- hidden state vs agent-visible observation;
- clone/restore/fork capability;
- Environment intervention semantics;
- deterministic/procedural seeds;
- evidence для Environment transitions.

## DU-08 — Perception

Должен определить semantic representations, которые доступны O1/O2 и могут быть intervention targets без backend leakage.

## DU-10 — Cortex

Должен определить:

- semantic Cortex observability;
- optional raw activation capability;
- backend-specific intervention adapter;
- provider limitations;
- huge artifact policy implications.

## Все module DU

Каждый module обязан определить собственные probes/intervention targets и research-readiness boundary.

## DU-25 — Experience/Data/Replay

Должен формализовать natural/intervened/replayed/imagined provenance в dataset/trajectory schema.

## DU-27 — Checkpoint/Reproducibility

Должен определить полный `Agent Snapshot`, необходимый exact fork/restore.

## DU-28 — Evaluation Harness

Должен построить experiment execution и causal metrics поверх принятого Intervention Gateway/Evidence Plane.

---

# 37. Completion gate DU-06

`DU-06` считается завершённым, если для любого future module/experiment можно ответить:

1. **Что именно наблюдается: trace, metric или diagnostic artifact?**
2. **Как событие связывается с causal identities/revisions?**
3. **Является ли наблюдаемое состояние public canonical или private probe?**
4. **Может ли observer изменить Agent?** — по умолчанию нет.
5. **Как intervention target валидируется и где находится causal boundary?**
6. **Как сохраняется natural/treatment provenance?**
7. **Создаётся ли отдельная branch/lineage?**
8. **Достаточен ли snapshot для exact counterfactual claim?**
9. **Есть ли OOD/off-target риск intervention?**
10. **Что происходит, если evidence потеряно?**

После принятия этого документа следующий допустимый Design Update:

```text
DU-07 — Environment / MicroWorld Contract
```
