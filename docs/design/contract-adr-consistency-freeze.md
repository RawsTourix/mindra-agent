# Contract + ADR Consistency Freeze MINDRA

## Статус документа

**Design Update:** `DU-31 — Contract + ADR Consistency Freeze`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ фиксирует общий consistency/freeze pass по архитектуре `DU-01 … DU-30` перед проектированием software version roadmap.

`DU-31` **не добавляет новый когнитивный модуль, data plane или training mechanism**. Его задача — определить единое нормативное чтение уже принятых ADR/design/contracts, устранить накопленные неоднозначности между ранними generic формулировками и поздними уточнениями и зафиксировать, какие semantic choices больше не могут быть оставлены Codex как implementation guess.

Главный результат:

> Архитектурная линия `DU-01 … DU-30` получает статус **ready for version planning**.

После `DU-31` разрешён `DU-32 — Version Roadmap`.

---

# 1. Semantic Freeze Baseline F31

MINDRA вводит логическую freeze baseline:

```text
Semantic Freeze Baseline: F31
scope: DU-01 … DU-30
ADR set: ADR-0001 … ADR-0030
contract set: DU-07 … DU-30 semantic contracts
status: ready_for_version_planning
```

`F31` не является software release/tag и не требует конкретного Git tag имени. Это semantic identity архитектурного baseline, который version roadmap обязан считать исходной системой ограничений.

---

# 2. Проверенный состав design line

## 2.1. Foundation / system owners

Уникальные canonical owners существуют для:

```text
DU-01 System Context
DU-02 Dependency & Composition Rules
DU-03 Runtime / Temporal Model
DU-04 CognitiveState Semantics
DU-05 Module Protocol & Scheduling
DU-06 Observability & Intervention
```

Для foundation не требуется искусственно создавать отдельные subsystem candidate contracts: их semantics задаются canonical system docs и ADR-0001 … ADR-0006.

## 2.2. Cognitive/runtime boundaries

Уникальные owners существуют для `DU-07 … DU-24`:

```text
Environment
Perception
Goals
Cortex
Memory Core
World Model
Self Model
Intrinsic Signals
Drives
Appraisal
Affect
Valuation
Salience
Memory Regulation
Workspace
Executive Control
Policy / Planner
Action Boundary
```

## 2.3. Внешние planes

Уникальные owners существуют для:

```text
DU-25 Experience / Data / Replay
DU-26 Training Lifecycle
DU-27 Checkpoint / Reproducibility / Compute
DU-28 MINDRA-Eval
DU-29 Engineering Testing
DU-30 Research Claims / Limitations
```

## 2.4. ADR completeness

Проверен непрерывный набор:

```text
ADR-0001 … ADR-0030
```

На момент freeze:

- все 30 ADR имеют статус `accepted`;
- `proposed` ADR отсутствуют;
- отдельные `rejected` ADR отсутствуют, rejected alternatives сохранены внутри решений;
- `superseded` ADR отсутствуют;
- скрытых параллельно действующих альтернативных ADR не обнаружено.

## 2.5. Contract completeness

Для всех semantic boundaries `DU-07 … DU-30` существует candidate machine-facing contract.

Итого semantic boundary contracts перед freeze: **24**.

После `DU-31` они остаются физически документами с пометкой candidate, но их **semantic meaning считается frozen baseline F31**. Exact Python/API/serialization shape остаётся deferred.

---

# 3. Правило нормативного чтения после freeze

До DU-31 ранние documents иногда содержали generic формулировку, которую позже намеренно уточнял специализированный DU.

После freeze нельзя использовать правило:

> «берём более удобную из двух формулировок».

Нормативный порядок:

```text
accepted ADR
+
canonical owner конкретной responsibility
+
DU-31 consistency resolution, если зафиксирована
        ↓
semantic baseline F31
        ↓
version specification
        ↓
implementation
```

`DU-31 consistency resolution` не создаёт новую semantics поверх позднего ADR; она только указывает, **какое уже принятое позднее решение уточняет generic раннюю формулировку**.

После F31 принцип «просто более поздний документ всегда побеждает» не используется. Любое новое semantic изменение требует governance из раздела 22.

---

# 4. Consistency resolution CR-01 — Action lifecycle

Ранний `DU-03` ввёл generic `Action Commit` до появления Policy и Action Gate.

Поздние `DU-23/24` уточнили final lifecycle.

Каноническое чтение F31:

```text
ActionCandidate
      ↓
SelectedActionIntent      # owner: Policy
      ↓
Action authorization
      ↓
AuthorizedAction
      ↓
Action Commit             # после authorization, до dispatch
      ↓
Dispatch Attempt
      ↓
Environment acceptance/execution
      ↓
Environment Transition?   # может отсутствовать при definite dispatch failure
      ↓
Outcome Commit, если observation/outcome существует
```

Инварианты:

```text
SelectedActionIntent ≠ Action Commit
AuthorizedAction ≠ Action Commit
Action Commit ≠ Dispatch
Action Commit ≠ Environment Transition
post-commit failure ≠ rollback commit
execution_unknown ≠ not_executed
```

Happy-path схема `DU-03` читается как сокращение успешного случая, а не как утверждение, что каждый `Action Commit` обязательно создаёт `Environment Transition`.

Нормативный owner authorization/dispatch/retry semantics: `DU-24 + ADR-0024`.

---

# 5. Consistency resolution CR-02 — Memory admission ownership

`DU-11` проектировался до Memory Regulation и использовал слово `admission` одновременно для structural validity и baseline policy acceptance.

После `DU-20` это две разные responsibility.

Каноническое чтение F31:

```text
MemoryWriteProposal
       ↓
Memory Core
→ structural eligibility / schema / authority /
  provenance / visibility validation
       ↓
eligible proposal
       ↓
Memory Regulation
→ policy admission under MemoryBudget/context
       ↓
RegulationDecision
       ↓
Memory Core
→ canonical commit / Memory revision
```

Owner split:

```text
Memory Core
→ record identity, canonical payload/store,
  structural validation, retrieval, representations/indexes,
  lifecycle commit

Memory Regulation
→ admission/retention/forgetting/eviction policy,
  replay/consolidation selection and regulation state
```

Исторический `DU-11 baseline admission` после F31 трактуется только как control/no-regulation policy behavior, а не как второй policy owner внутри Memory Core.

---

# 6. Consistency resolution CR-03 — Replay taxonomy

Generic термин `Replay Step` в раннем temporal design не является одной storage/training responsibility.

После `DU-20/25/26` canonical distinction:

```text
Retrieval
≠
Agent Memory Replay / Reactivation
≠
Training Replay
```

### Retrieval

Query-driven normal cognition operation над Memory.

### Agent Memory Replay / Reactivation

Agent-owned повторная активация существующего `MemoryRecord` в memory/consolidation dynamics.

### Training Replay

Внешнее повторное использование derived/source-linked training data `Training Runtime`.

Общее правило:

```text
replay ≠ new natural Environment experience
```

Source causal identity сохраняется; replay frequency не увеличивает natural visitation/experience count.

---

# 7. Consistency resolution CR-04 — Consolidation и Learning Update

Ранний `DU-03` оставлял открытой возможность связать Consolidation Event с learned-state change.

`DU-20/26` эту границу уже определили.

После F31:

```text
Memory Consolidation
→ source-preserving derived MemoryRecord / memory maintenance

Representation Maintenance / re-encoding
→ derived representation/index maintenance

Learning Update
→ parameter/model-fitting change через Training Runtime
```

Канонически:

```text
Consolidation ≠ Learning Update
Consolidation ≠ optimizer.step()
Re-encoding ≠ semantic consolidation
Runtime State Update ≠ Learning Update
```

Если future algorithm использует replayed memory как **training input**, сам optimizer update всё равно является отдельным `Learning Update` `DU-26`, а не скрытым действием Consolidation Event.

---

# 8. Consistency resolution CR-05 — Learning revision activation

Ранние generic формулировки `Learning Update → Agent revision changes` уточняются `DU-26`.

Canonical lifecycle:

```text
BaseRevisionBundle
      ↓
TrainingAttempt
      ↓
CandidateRevisionBundle
      ↓
Validation
      ↓
LearningUpdateRecord
      ↓
RevisionActivationRecord
      ↓
Active AgentRevision
```

Инварианты:

```text
candidate ≠ active
loss improvement ≠ activation
training success ≠ activation
rollback ≠ history rewrite
```

Live cognition не меняет behavior-relevant revisions посреди pinned causal segment/Decision Window без явной activation boundary.

---

# 9. CognitiveState, Workspace и полный Agent state

Проверено отсутствие owner conflict.

```text
CognitiveState
→ committed published shared-state surface

Workspace
→ bounded owner-controlled shared broadcast capability,
  которая может физически быть namespace/ref внутри общей state architecture

Agent Snapshot
→ всё causally relevant agent-owned state,
  включая private state/Memory/RNG/parameters/etc. согласно scope
```

Следовательно:

```text
CognitiveState ≠ Workspace
CognitiveState ≠ Agent Snapshot
WorkspaceItem admission ≠ ordinary state publication
```

Физическое хранение Workspace payload в `CognitiveState` не стирает semantic boundary.

---

# 10. Scheduler и Executive Control

Проверено отсутствие двойного owner.

```text
Cognitive Scheduler
→ invariant execution mechanics:
  DAG/waves/reads/writes/stale validation/commit

Executive Control
→ agent-owned выбор разрешённых internal meta-actions
  и allocation внутри provided resource envelope
```

Инварианты:

```text
Executive Control ≠ Scheduler
Executive decision ≠ direct service call
Executive ≠ Policy
```

Executive не меняет dependency graph, write authority или atomicity semantics.

---

# 11. Planner, Policy и Action Boundary

Owner chain frozen:

```text
Planner(optional)
→ Plan / ActionCandidate provider

Policy
→ owner final SelectedActionIntent

Action Boundary
→ authorization / normalization / explicit override /
  Action Commit / dispatch lifecycle
```

Инварианты:

```text
Planner ≠ Policy
Valuation ≠ Policy
Policy ≠ Action Gate
Action Gate override ≠ Policy choice
```

Policy может defer decision и запросить дополнительную cognition через committed Executive-control path; recursive hidden call-stack loop запрещён.

---

# 12. Signal / motivation / meaning / value freeze

Следующая semantic decomposition проверена и сохраняется:

```text
Intrinsic Signal
≠ Drive State
≠ Appraisal
≠ Affect State
≠ ValueProfile
≠ SalienceProfile
≠ Policy Decision
```

Ключевые meanings:

- Intrinsic Signal — typed измерение свойства опыта;
- Drive — persistent regulatory/motivational state;
- Appraisal — event/target-relative contextual meaning;
- Affect — persistent history-dependent modulation state;
- Valuation — structured decision-relevant value/comparison evidence;
- Salience — processing priority/allocation evidence;
- Policy — behavioral selection.

Никакой обязательный общий `reward`, `motivation`, `valence` или `importance` scalar не вводится F31.

---

# 13. Budget / resource taxonomy

Разные бюджеты не являются aliases:

```text
AttentionBudget
MemoryBudget
WorkspaceBudget
CognitiveResourceEnvelope
Training budget
ComputeManifest / ComputeUsageRecord
```

`Executive Control` распределяет agent-visible cognitive resources только внутри предоставленного envelope.

Infrastructure measured compute из `DU-27` не становится автоматически cognitive input.

---

# 14. Source / derived / authority semantics

Across Memory, Experience, Training, Evaluation и Claims действует один freeze-invariant:

```text
source entity
≠ derived representation
≠ derived interpretation
```

Примеры:

```text
MemoryRecord ≠ embedding/index
Source MemoryRecord ≠ consolidated derived MemoryRecord
ExperienceEvent ≠ TrainingSample
MetricRecord ≠ InterpretationRecord
ObservationRecord ≠ ResearchClaim
```

Derived entity обязана сохранять lineage до source настолько, насколько требует соответствующий contract.

Derivation не повышает epistemic authority source автоматически.

---

# 15. Visibility / privileged data

Canonical trust boundary согласована:

```text
Environment hidden state / Research Ground Truth
      ↓
Research/Evaluation/Test Plane only
```

Normal Agent path получает только agent-visible data согласно Environment/Perception/Memory contracts.

Privileged data может входить в training только через explicit `DataVisibilityPolicy` / privileged-supervision condition.

Инварианты:

```text
Evaluator Ground Truth ≠ Agent input
Test Oracle ≠ Agent input
Trace/control metadata ≠ cognitive feature автоматически
```

---

# 16. Availability / unknown semantics

Общий semantic baseline из `DU-04` сохраняется:

```text
available
unknown
stale
unavailable
missing
```

Meaning:

- `available` — применимое актуальное значение существует;
- `unknown` — значение применимо, но неизвестно/не оценено;
- `stale` — существующее значение не покрывает текущий causal validity context;
- `unavailable` — capability/value намеренно недоступны или неприменимы в текущей composition/phase;
- `missing` — required structural contract element отсутствует; обычно ошибка.

Эти semantics не кодируются универсальными magic sentinels.

Другие status families не являются aliases этой taxonomy:

```text
execution_unknown
inconclusive
invalid evaluation
not_measured
not_run / skipped
```

Например `execution_unknown` относится к external action lifecycle, а не к epistemic availability field.

Exact enums/serialization остаются version-level choice.

---

# 17. Failure / history semantics

Across runtime/data/training/checkpoint действует правило:

> уже committed causal history не переписывается последующим failure/retry/rollback.

Примеры:

```text
module attempt failed
→ no partial commit

Action Commit succeeded, dispatch failed
→ commit remains

candidate training failed
→ active Agent unchanged

checkpoint materialization interrupted
→ no final CheckpointManifest commit

rollback
→ new causal activation, not deletion of previous active revision

claim superseded
→ old claim remains historical revision
```

`failure`, `no_effect`, `partial`, `unknown`, `invalid`, `censored`, `not measured` не сворачиваются в один boolean.

---

# 18. Snapshot / checkpoint consistency

Freeze confirms three different levels:

```text
CognitiveState snapshot
≠ Agent Snapshot
≠ persistent Checkpoint
```

Full causally relevant Agent snapshot/checkpoint scope учитывает, где применимо:

- committed `CognitiveState`;
- module-private state;
- Memory Store + Memory Regulation state;
- Workspace/Executive/Planner/Policy private state;
- Drive/Affect/provider state;
- trainable parameters + active revisions;
- RNG/stochastic state;
- candidate/training state для training-resume scope;
- pending external-effect state;
- Environment state для full-system exact counterfactual scope.

`DU-27` остаётся owner persistent capture/restore semantics.

---

# 19. Evaluation / Verification / Claims boundary

Эти три внешние responsibility frozen как разные planes:

```text
MINDRA-Eval
→ функциональный/research evidence

Engineering Testing
→ implementation contract/invariant evidence

Research Claims / Limitations
→ допустимая interpretation/scoped claim поверх evidence
```

Инварианты:

```text
engineering verified ≠ functionally useful
research result ≠ implementation correctness
metric ≠ claim
association ≠ causation
functional similarity ≠ phenomenological equivalence
```

Research evidence меняет accepted architecture только через design review + ADR.

---

# 20. No*/Dummy/control semantics

`No*`, Dummy, Constant, Random, Shuffled, matched-capacity/compute/recurrent controls являются **experimental implementations/conditions**, а не alternate hidden architectures.

Общие требования:

- capability absence/behavior явны;
- provenance сохранена;
- disabled component не оставляет скрытый live path;
- matched-control claim указывает реально matched factors;
- control не получает privileged data без explicit oracle condition;
- negative module gate может ослабить design claim, но не удаляет accepted boundary без ADR.

---

# 21. Что именно frozen после DU-31

## 21.1. Semantic-frozen

Для baseline F31 заморожены:

- logical boundaries и ownership;
- distinction cognitive/runtime/external planes;
- source-of-truth responsibilities;
- proposal/validation/commit ownership;
- causal ordering/commit boundaries;
- separation actual/predicted/imagined/replayed/intervened;
- provenance/visibility principles;
- availability meanings;
- source-vs-derived distinctions;
- action selection/authorization/dispatch distinctions;
- training candidate/validation/activation distinctions;
- snapshot/checkpoint/reproducibility distinctions;
- Evaluation/Verification/Claims separation;
- negative module gates и requirement first-class controls там, где они приняты;
- requirement explicit revisions/lineage/status/failure semantics;
- отсутствие mandatory universal scalarization там, где design её отверг;
- отсутствие runtime Service Locator/hidden ambient dependencies.

## 21.2. Semantic contract set frozen, API нет

Contracts `DU-07 … DU-30` считаются **semantic-frozen for roadmap**.

Это означает:

> software version может выбрать concrete representation, но не имеет права изменить смысл сущности/owner/lifecycle без нового ADR.

Например version design может выбрать:

```text
@dataclass
Pydantic
TypedDict
TensorDict
protobuf
```

если semantic contract сохраняется.

## 21.3. Не frozen

Остаются version/implementation choices:

- Python package/file layout;
- Protocol/ABC/dataclass/Pydantic/TensorDict choice;
- exact field names там, где semantic identity однозначна;
- exact enum values/status encoding;
- tensor shapes/dtypes;
- concrete neural architectures;
- Cortex model/backend;
- World/Self/Affect/etc. algorithms;
- optimizer/loss/RL algorithm;
- LoRA/PEFT choice;
- memory/index/database backend;
- checkpoint physical format/hash/storage;
- Environment/MicroWorld concrete tasks;
- exact budgets/horizons/thresholds;
- benchmark/task suite;
- seed count/statistical test/threshold;
- test/property/CI tooling;
- plotting/tracking/report tooling;
- hardware/provider/deployment topology.

Эти вопросы разрешено выбирать в `DU-32`/version specification без нового ADR, **если выбор не меняет semantic-frozen инвариант**.

---

# 22. Breaking semantic change после F31

После freeze semantic breaking change не может появиться только в code или version README.

Обязательный путь:

```text
new evidence / implementation blocker / design issue
        ↓
design review
        ↓
new ADR
        ↓
старый ADR status при необходимости:
superseded / superseded in part
        ↓
canonical owner update
        ↓
semantic contract update
        ↓
glossary / freeze baseline revision
        ↓
VerificationObligation update
        ↓
version plan / implementation
```

Breaking semantic change включает, например:

- смену owner canonical state;
- слияние ранее различённых responsibilities;
- изменение commit ordering;
- превращение optional/falsifiable module в mandatory без ADR;
- введение hidden direct dependency;
- изменение privileged visibility;
- изменение source-of-truth entity;
- изменение claim/evidence semantics.

Неблокирующая typo/clarification, которая не меняет meaning, отдельного ADR не требует.

---

# 23. Field / revision conventions для version design

До exact API frozen следующие conventions смысла:

- `*_id`/typed identity обозначает stable logical identity, а не memory address/array index;
- `revision` означает versioned semantic state/entity и не подменяется wall-clock timestamp;
- `base_*_revision`/parent ref связывает вычисление с causal source revision;
- immutable historical records меняются через new revision/new related record, а не silent rewrite;
- source references сохраняются для derived entity;
- missing optional value не кодируется magic numeric sentinel;
- provider/backend identity не является semantic owner;
- physical location/path/device не является identity canonical entity.

Exact identifier types и naming details определит first version specification.

---

# 24. Implementation leakage audit

В semantic contracts не обнаружено обязательного выбора:

```text
PyTorch / JAX / TensorFlow
TorchRL
LangChain / agent framework
Qwen / Gemma / Llama
FAISS / HNSW / SQLite
RLDS / Minari / Reverb
Safetensors / DCP
pytest / Hypothesis / Import Linter
GitHub Actions
конкретного statistical package
```

Упоминания конкретных технологий в research/design docs читаются как examples/candidates/evidence, если accepted ADR явно не утверждает обратное.

---

# 25. Deferred questions, которые НЕ блокируют DU-32

Следующие вопросы намеренно передаются version planning:

- какой минимальный vertical slice реализовать первым;
- какие optional modules включить в первую software version;
- какой Cortex использовать;
- какие modules rule-based, learned или Dummy на конкретной версии;
- joint vs separate training конкретных components;
- exact canonical state Python representation;
- storage/file formats;
- concrete MicroWorld/task suite;
- exact compute budgets;
- exact evaluation metrics/statistics для первого experiment;
- exact testing/CI stack;
- конкретные algorithm choices.

Они не требуют Codex самостоятельно определять **architecture semantics**, если version specification их явно выберет.

---

# 26. Open research questions, которые также НЕ блокируют roadmap

Research-falsifiable boundaries остаются условными:

- отдельный Affect;
- Workspace;
- adaptive Executive Control;
- optional Planner;
- concrete Intrinsic/Drive mappings;
- конкретная Valuation scalarization/comparison strategy;
- конкретные Memory consolidation algorithms.

Их uncertainty является свойством research program, а не дырой в architecture contract.

Version roadmap обязан предусматривать controls/No* и не трактовать conditional boundary как уже эмпирически доказанную.

---

# 27. Verification obligations перед implementation

`DU-29` уже определяет Verification Plane. После F31 first version specification обязана преобразовать frozen semantic invariants в implementation-facing `VerificationObligation`.

Особенно обязательны checks для:

```text
forbidden dependencies / Service Locator
single-writer ownership
stale/base revision validation
wave atomicity
Ground Truth leakage
Memory Core vs Regulation ownership
Workspace vs CognitiveState
Executive vs Scheduler
Policy vs Planner vs Action Gate
Action Commit/dispatch/retry lifecycle
Memory Replay vs Training Replay
Consolidation vs Learning Update
candidate vs active revision
checkpoint integrity/restore
Evaluation vs Agent isolation
Verification vs Evaluation distinction
claim/evidence wording lineage where implemented
```

DU-31 не выбирает testing framework; он фиксирует, что эти obligations нельзя потерять при декомпозиции roadmap.

---

# 28. Audit result

Consistency pass `DU-01 … DU-30` завершён.

Результат:

```text
ADR completeness: PASS
canonical owner uniqueness: PASS
semantic contract coverage DU-07…30: PASS
ownership consistency: PASS after CR-02 normalization
runtime/temporal consistency: PASS after CR-01/03/04/05 normalization
CognitiveState/Workspace separation: PASS
Policy/Planner/Action separation: PASS
source/provenance/visibility consistency: PASS
snapshot/checkpoint consistency: PASS
Evaluation/Verification/Claims separation: PASS
availability/unknown semantics: PASS
negative-gate/control discipline: PASS
implementation leakage: PASS
blocking architectural TODO: NONE FOUND
```

Найденные CR-01 … CR-05 являются фиксацией уже принятых поздних уточнений, а не новыми subsystem choices.

---

# 29. Gate DU-31

Gate выполнен, если Codex при проектировании первой software version **не должен самостоятельно решать**:

- кто владеет состоянием;
- где commit boundary;
- что является source of truth;
- какая responsibility относится к cognitive/runtime/training/evaluation/testing/claim plane;
- чем replay/consolidation/training различаются;
- где проходит privilege boundary;
- что означает unknown/stale/missing;
- как semantic breaking change должен оформляться.

По результату audit gate выполнен.

---

# 30. Итог

Архитектурная линия получает статус:

```text
MINDRA semantic design DU-01 … DU-30
= F31
= ready for version planning
```

Следующий допустимый Design Update:

```text
DU-32 — Version Roadmap
```

До принятия `DU-32` production/research implementation по-прежнему не начинается.
