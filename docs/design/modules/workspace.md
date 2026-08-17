# Workspace MINDRA

## Статус документа

**Design Update:** `DU-21 — Workspace`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет `Workspace` MINDRA — ограниченную временную shared-access surface, через которую причинно идентифицируемый subset уже доступной Agent информации может динамически стать доступным нескольким заранее допущенным cognitive consumers без прямой связи каждого producer с каждым consumer.

Workspace принимается **не как модель сознания**, не как обязательный путь всей cognition и не как второй `CognitiveState`. Это falsifiable engineering/research boundary с first-class `NoWorkspace` и matched controls.

Документ определяет:

- module gate Workspace;
- отличие Workspace от `CognitiveState`, Salience, Memory и Cortex context;
- candidate/proposal/admission boundary;
- bounded `WorkspaceBudget`;
- `WorkspaceItem` и source-preserving semantics;
- broadcast/read semantics;
- producer/consumer eligibility;
- persistence, replacement и expiration;
- multi-cycle continuity;
- связь с Salience;
- Memory retrieval → Workspace boundary;
- Cortex context packing boundary;
- branch/imagination semantics;
- scheduler/commit semantics;
- observability/intervention;
- snapshot/revision/failure/degradation;
- `NoWorkspace` и matched controls;
- отрицательный критерий, при котором отдельная Workspace boundary должна быть пересмотрена.

Документ опирается на:

- [`../cognitive-state.md`](../cognitive-state.md) — versioned shared-state surface;
- [`../dependency-rules.md`](../dependency-rules.md) — explicit dependencies и запрет runtime Service Locator;
- [`../execution-model.md`](../execution-model.md) — logical time/branch semantics;
- [`../module-lifecycle.md`](../module-lifecycle.md) — staged update/commit;
- [`../observability-and-intervention.md`](../observability-and-intervention.md) — Evidence Plane/Intervention Gateway;
- [`salience.md`](salience.md) — priority/allocation evidence;
- [`memory.md`](memory.md) и [`memory-regulation.md`](memory-regulation.md) — persistent Memory/retrieval/regulation;
- [`cortex.md`](cortex.md) — explicit semantic Cortex context;
- [`valuation.md`](valuation.md), [`appraisal.md`](appraisal.md), [`affect.md`](affect.md), [`goals.md`](goals.md) — возможные source contents/evidence без передачи ownership.

Документ намеренно **не** определяет:

- Metacognitive / Executive Control — `DU-22`;
- final Policy / Planner — `DU-23`;
- Action Gate — `DU-24`;
- training objectives — `DU-26`;
- exact checkpoint encoding — `DU-27`;
- конкретную Global Workspace Theory как теорию сознания;
- обязательный neural latent bottleneck;
- обязательный slot count/top-K;
- обязательный Transformer/cross-attention router;
- exact Python API.

---

# 1. Цель DU-21

После `DU-04` MINDRA уже имеет `CognitiveState`: общую versioned поверхность опубликованного состояния с declared read dependencies.

После `DU-19` MINDRA также умеет оценивать purpose-dependent priority ограниченного processing.

Поэтому Workspace нельзя обосновать фразой:

> «нужен общий буфер, чтобы модули могли обмениваться данными».

Эту функцию уже выполняет `CognitiveState`.

Workspace имеет право существовать только если добавляет отдельную измеримую функцию:

> **динамически отбирать ограниченный subset информации, поддерживать его кратковременную доступность и предоставлять один shared broadcast channel нескольким eligible consumers при реальном capacity/bandwidth bottleneck.**

---

# 2. Module gate

## 2.1. Альтернатива без Workspace

Полностью допустим Agent:

```text
Module A ─┐
Module B ─┼→ CognitiveState
Module C ─┘
            ↓
      declared consumers
```

Если этого достаточно, отдельный Workspace не нужен.

## 2.2. Что добавляет Workspace

Workspace добавляет комбинацию четырёх свойств:

1. **bounded capacity** — далеко не всё published state допускается одновременно;
2. **dynamic admission** — содержимое зависит от текущей конкуренции/контекста;
3. **temporary persistence** — admitted content может переживать несколько Cognitive Cycles без превращения в долговременную Memory;
4. **shared availability** — один admitted item может стать доступен нескольким eligible consumers через одну стабильную boundary.

Conceptually:

```text
many explicit producers
        ↓
WorkspaceCandidateSet
        ↓
Salience hint + Workspace policy + budget
        ↓
limited WorkspaceSnapshot
        ↓
multiple declared consumers
```

## 2.3. Gate принят условно

Workspace **принимается как отдельная boundary**, но решение falsifiable.

Если будущая evaluation показывает, что:

- `NoWorkspace + declared direct reads` не хуже;
- random/fixed/matched shared buffer даёт тот же эффект;
- capacity/broadcast interventions не имеют специфического causal effect;
- Workspace не уменьшает coordination burden и не улучшает performance/generalization under bottleneck;

то `ADR-0021` должен быть пересмотрен, а Workspace может быть удалён/слит с `CognitiveState`.

---

# 3. Главное архитектурное решение

MINDRA использует **bounded source-preserving broadcast Workspace overlay**.

Conceptually:

```text
explicit WorkspaceCandidateSet
        +
optional SalienceProfile / AttentionAllocation
        +
WorkspaceBudget
        ↓
Workspace AdmissionPolicy
        ↓
staged admission / retention / replacement
        ↓
atomic Workspace commit
        ↓
WorkspaceSnapshot W_(t+1)
        ↓
declared eligible consumers
```

Ключевые invariants:

```text
Workspace ≠ CognitiveState
Workspace ≠ Memory
Workspace ≠ Salience
Workspace ≠ Cortex context
Workspace admission ≠ Salience allocation
Workspace availability ≠ automatic module execution
Workspace content ≠ new factual authority
Workspace ≠ proof of consciousness
```

Решение фиксируется в `ADR-0021`.

---

# 4. Workspace и CognitiveState

## 4.1. CognitiveState

`CognitiveState` — общая versioned shared-state поверхность всех contract-defined current values.

Она может содержать множество namespaces:

```text
perception
world
self
goals
drives
appraisal
affect
valuation
salience
workspace
...
```

## 4.2. Workspace

Workspace — **owner-controlled bounded namespace/capability внутри общей state architecture**, имеющая отдельные admission/capacity/persistence/broadcast semantics.

То есть физически future implementation может:

- хранить Workspace namespace прямо в `CognitiveState`;
- хранить payload отдельно, а в `CognitiveState` публиковать `WorkspaceSnapshot`/refs;
- использовать structural sharing.

Архитектурный invariant — не физический контейнер, а отдельная semantics.

## 4.3. Почему это не дублирование

Обычное поле `world.current_belief` существует потому, что его owner публикует его согласно contract.

Workspace item существует потому, что информация **выиграла/прошла ограниченную admission boundary** для shared temporary access.

```text
published somewhere in CognitiveState
≠
admitted to Workspace
```

---

# 5. Workspace не заменяет dependency discipline

Наличие Workspace не означает:

```text
любой модуль может читать всё, что попало в Workspace
```

Consumer обязан заранее иметь declared capability/dependency:

```text
reads_workspace = allowed
supported WorkspaceItem kinds = ...
```

Producer также не получает direct write authority.

Workspace therefore не является:

- runtime Service Locator;
- event bus;
- pub/sub callback system;
- ambient global dictionary.

`WorkspaceItem` — данные, а не сервис.

---

# 6. Workspace Candidate / Proposal

Любой разрешённый producer формирует proposal/candidate, но не пишет Workspace напрямую.

```text
producer
  ↓
WorkspaceProposal
  ↓
Workspace Candidate Set
  ↓
Workspace admission
```

Candidate должен быть причинно идентифицируемым и содержать conceptually:

```text
candidate_id
source subsystem
source_ref
source_revision
semantic content/projection
content kind
causal mode
freshness/availability
requested/allowed lifetime?
provenance
```

Exact fields не frozen.

Candidate не имеет права повышать собственный authority только из-за admission.

---

# 7. Source-preserving WorkspaceItem

После admission создаётся `WorkspaceItem`.

Conceptually:

```text
WorkspaceItem
├── workspace_item_id
├── source_ref
├── source_revision
├── source provenance/authority
├── semantic payload/projection
├── content schema/revision
├── admitted_at logical identity
├── workspace_revision
├── freshness/staleness
├── lifetime/expiration
├── admission provenance
└── intervention/degradation provenance?
```

## 7.1. Admission не создаёт новую истину

Если source был:

```text
World Prediction
```

Workspace item остаётся prediction.

Если source был:

```text
Cortex inference
```

Workspace не превращает его в observed fact.

Если source был:

```text
Memory retrieval
```

Workspace item остаётся retrieved memory content/projection.

## 7.2. Snapshot semantics

Admitted item представляет содержание **на определённой source revision**.

Если source позже изменился, Workspace item не должен молча переписаться.

Возможны explicit:

```text
refresh
replace
expire as stale
retain historical admitted snapshot
```

по versioned policy.

---

# 8. WorkspaceBudget

Workspace обязан иметь реальный capacity/bandwidth constraint, иначе отдельная boundary теряет основную функциональную гипотезу.

Conceptually budget может описывать:

```text
item/slot count
semantic payload units
bytes
token-like context estimate
feature capacity
per-cycle write bandwidth
```

Concrete units первой версии не frozen.

Ключевое:

```text
WorkspaceBudget
≠
AttentionBudget
≠
MemoryBudget
≠
Executive global compute budget
```

Salience может распределить `AttentionBudget` между workspace candidates, но actual Workspace capacity остаётся отдельным resource contract.

---

# 9. Admission boundary

Workspace admission должна быть отдельной от Salience.

Допустимый pattern:

```text
WorkspaceCandidateSet
        ↓
Salience request
purpose = workspace_admission_hint
        ↓
SalienceProfile / AttentionAllocation
        ↓
WorkspaceAdmissionProfile
        +
capacity / freshness / diversity / compatibility / lifetime
        ↓
Workspace AdmissionPolicy
        ↓
admit / defer / retain / replace / reject
```

Ключевой invariant:

```text
AttentionAllocation
≠
Workspace admission decision
```

Высокая Salience не может обойти structural validity/capacity/lifecycle constraints.

---

# 10. Competition

Workspace допускает competition между candidates при дефиците capacity.

Но канонически не требуется:

```text
winner_take_all
```

или один scalar score.

Допустимы future policies:

```text
fixed slots
ranked admission
quota/diversity admission
constraint-first
soft capacity allocation
learned routing
hybrid
```

Exact policy относится к version design.

---

# 11. Workspace lifecycle

Workspace предназначен для **краткоживущей active accessibility**, а не долговременного storage.

Допустимые semantic states conceptually:

```text
candidate
admitted/active
retained
stale
replaced
evicted
expired
invalid/unavailable
```

Exact enum не frozen.

---

# 12. Persistence

Workspace может переживать несколько Cognitive Cycles.

Это и создаёт working-context continuity.

Но persistence всегда bounded/explicit.

Typical scopes могут включать:

```text
one cycle
Decision Window
N logical cycles
until Action Commit
until Outcome Commit
explicit episode-local persistence
```

Workspace item не становится долговременным только потому, что долго удерживался.

Session/agent-long-lived information должна принадлежать Goals/Memory/другому owner, а не Workspace по умолчанию.

---

# 13. Replacement и expiration

При полном Workspace новое содержимое может потребовать replacement.

Replacement policy обязана быть explicit/versioned.

Нельзя скрыто использовать:

```text
oldest wins
latest wins
lowest salience wins
```

как universal law.

Replacement может учитывать:

- admission priority;
- current relevance;
- freshness;
- age;
- redundancy/diversity;
- source compatibility;
- persistence commitment;
- budget cost.

Но exact formula не frozen.

---

# 14. Broadcast semantics

В MINDRA `broadcast` означает:

> admitted Workspace content становится доступным **всем declared eligible consumers**, которым разрешён соответствующий content kind, при их обычном scheduled compute.

Broadcast **не означает**:

```text
push callback
interrupt consumer
сразу вызвать все modules
изменить scheduler graph
автоматически вызвать Cortex
```

Это pull/read availability через canonical state boundary.

Так сохраняются `DU-02/05` invariants.

---

# 15. Global availability не означает unrestricted access

Workspace может быть глобально доступен на уровне архитектурной capability, но access control остаётся declared.

Например:

```text
World Model: reads Workspace semantic facts/hypotheses
Policy: reads Workspace action-relevant items
Cortex context builder: reads explicit Workspace projection
Perception: may not read Workspace at all
```

Это определяется contract/version, а не runtime discovery.

---

# 16. Memory relation

```text
Memory
→ long-lived experience/knowledge

Workspace
→ bounded temporary shared accessibility
```

Retrieval не попадает в Workspace автоматически.

Правильно:

```text
RetrievalResult
        ↓
WorkspaceProposal
        ↓
admission
        ↓
WorkspaceItem
```

Таким образом можно наблюдать отдельно:

1. что было retrieved;
2. что было предложено в Workspace;
3. что было admitted;
4. что реально читали consumers.

Workspace eviction также **не удаляет MemoryRecord**.

---

# 17. Workspace и forgetting

Если MemoryRecord был retrieved и admitted в Workspace, а затем Memory Regulation делает исходный record недоступным, admitted Workspace item может оставаться доступным до собственной expiration boundary, если policy это разрешает.

Это моделирует различие:

```text
уже удерживаю информацию в active workspace
≠
могу заново retrieve её из long-term Memory
```

Но после expiry Workspace не имеет права самостоятельно «воскресить» forgotten memory.

---

# 18. Cortex context boundary

Workspace **не является Cortex prompt/context window**.

Правильная цепочка:

```text
WorkspaceSnapshot
        ↓
explicit cognitive/context consumer
        ↓
semantic CortexRequest fragments
        ↓
Cortex Gateway
        ↓
backend-specific prompt/tokenization
```

Нельзя:

```text
Workspace = concatenate all items into prompt
```

как canonical behavior.

Cortex context budget может отличаться от Workspace budget.

---

# 19. Goals / Appraisal / Affect / Valuation relation

Эти subsystems могут:

- создавать candidates;
- предоставлять evidence для Salience/admission;
- читать Workspace, если contract разрешает.

Но admission не меняет ownership:

```text
Goal admitted to Workspace
≠
Workspace owns Goal
```

И:

```text
high Value
≠
automatic Workspace admission
```

---

# 20. Workspace не выбирает действия

Даже если Workspace содержит:

```text
candidate action A
candidate action B
```

он не решает:

```text
Action Commit = A
```

Final planning/action selection остаётся `DU-23`, а execution — `DU-24`.

---

# 21. Workspace и Executive Control

`DU-21` не решает:

- сколько Cognitive Cycles провести;
- сколько Cortex calls разрешить;
- инициировать ли retrieval;
- инициировать ли consolidation;
- какой Goal держать в focus;
- когда менять WorkspaceBudget динамически.

Future `DU-22` сможет использовать Workspace state/pressure/contents как evidence и менять разрешённые budgets/purposes через explicit contract.

Но Workspace сам не является Executive Control.

---

# 22. Workspace и scheduler

Workspace участвует в обычной scheduler semantics.

Conceptually:

```text
Committed Workspace W_t
        ↓
producers compute WorkspaceProposals
        ↓
Salience/admission wave(s)
        ↓
staged Workspace update
        ↓
atomic commit W_(t+1)
        ↓
downstream eligible consumers read W_(t+1)
```

Никакого partial Workspace state не должно быть видно между candidates в одной atomic boundary.

Если admission зависит от Salience текущих candidates, scheduling dependency должна быть explicit.

---

# 23. Workspace revision

Workspace имеет собственную logical revision:

```text
workspace_revision W17
→ admission/replacement/expiry commit
→ W18
```

Она отличается от:

```text
state_revision
memory_revision
agent_revision
salience revision
```

`WorkspaceSnapshot` должен быть связан с base `state_revision`, logical time и `agent_revision`.

---

# 24. Actual / predicted / imagined provenance

Workspace item всегда сохраняет causal mode.

Допустимы:

```text
actual
retrieved
predicted
imagined
retrospective
intervened
```

Но они не смешиваются.

Особенно:

```text
imagined WorkspaceItem
≠
real committed WorkspaceItem
```

---

# 25. Branch / imagination Workspace

World Model/Planner branch может иметь собственный branch-local Workspace.

Правильно:

```text
real Workspace W10
        ↓ fork
branch A: W10a → simulated W11a
branch B: W10b → simulated W11b
```

Изменения simulated Workspace не применяются обратно к real Workspace автоматически.

Чтобы hypothetical result попал в real Workspace, реальный cognitive process должен после завершения simulation создать explicit proposal с provenance:

```text
source_mode = imagined-derived inference
```

---

# 26. Workspace и information compression

Workspace item может быть semantic projection source content, но compression/summarization не должна скрывать provenance или authority.

Если Cortex/learned encoder создаёт compressed projection:

- backend/revision фиксируется;
- source refs сохраняются;
- uncertainty/source authority не повышаются автоматически;
- incompatible representation revisions не смешиваются молча.

Workspace не является ещё одной semantic Memory consolidation boundary.

---

# 27. Observability

Минимальный evidence должен позволять восстановить:

```text
какие candidates были доступны
кто их предложил
какой WorkspaceBudget действовал
какие Salience/admission evidence использовались
какая AdmissionPolicy/revision действовала
что было admitted/rejected/replaced/expired
какой WorkspaceSnapshot видели consumers
какие consumers реально прочитали какие items
сколько logical cycles item прожил
какая source/provenance у каждого item
```

Один итоговый `workspace_state` без admission history недостаточен для causal analysis.

---

# 28. Intervention

Допустимы controlled interventions:

- изменить WorkspaceBudget;
- inject/remove candidate;
- force/forbid admission;
- изменить item lifetime;
- заменить admission policy;
- shuffle Salience evidence;
- clamp Workspace content;
- remove broadcast access у конкретного consumer;
- заменить WorkspaceSnapshot matched control buffer;
- изменить source projection при explicit provenance.

Intervention всегда идёт через `Intervention Gateway`.

---

# 29. Snapshot / restore

Exact Agent Snapshot должен включать causally relevant Workspace state:

```text
WorkspaceSnapshot/content
workspace_revision
budget/policy revision
item lifetimes
admission/replacement state
private recurrent/router state, если есть
RNG
source refs/revisions
branch lineage
intervention/degradation state
```

Иначе counterfactual clone может иметь другую active-access history.

---

# 30. Failure / degradation

Нужно различать минимум conceptually:

```text
candidate invalid
budget unavailable
capacity exhausted
policy failure
source unavailable/stale
projection failure
item schema incompatibility
consumer capability mismatch
workspace unavailable
```

Failure не заменяется молча пустым Workspace.

Fallback/degradation policy должна быть explicit и traced.

---

# 31. NoWorkspace / Dummy / Controls

Обязательные конфигурации:

## `NoWorkspace`

Workspace capability отсутствует. Consumers используют только обычные declared inputs.

## `DummyWorkspace`

Детерминированный engineering stub.

## Controls

Минимум:

```text
DirectReadsControl
FixedLatestK
RandomAdmission
ShuffledAdmission
Uniform/Salience-free admission
UnboundedWorkspace
WorkspaceWithoutBroadcast
MatchedSharedBufferControl
MatchedRecurrentBufferControl
```

Exact набор первой версии уточняется позже.

---

# 32. Ключевой matched control

Самый важный контроль — система с **такой же state capacity/compute**, но без целевой workspace semantics.

Например:

```text
Full Workspace
vs
Matched Recurrent Buffer
```

Одинаково:

- число параметров;
- объём state;
- update frequency;
- compute budget.

Различается:

- explicit candidate competition;
- source-preserving admission;
- bounded shared broadcast semantics.

Если matched buffer работает так же, отдельная Workspace boundary получает слабое функциональное обоснование.

---

# 33. Capacity experiment

Нужно исследовать не только:

```text
Workspace ON vs OFF
```

но и:

```text
capacity = 0
capacity = very small
capacity = medium
capacity = large
unbounded
```

Сильная workspace hypothesis предсказывает осмысленный trade-off:

- слишком маленькая capacity теряет нужную информацию;
- слишком большая может уничтожать competition/bottleneck benefit;
- полезный диапазон должен зависеть от task complexity.

Но такой результат является empirical claim, а не частью design.

---

# 34. Broadcast causal test

Нужно отдельно проверить именно shared availability.

Например:

```text
source module creates item X
X admitted
        ↓
consumer B uses X
consumer C uses X
```

Control:

```text
тот же item/state capacity
но broadcast access consumer C removed
```

Если consumer C никак не зависит от наличия broadcast при задачах, где такое shared integration требовалось hypothesis, роль Workspace сомнительна.

---

# 35. Отрицательный критерий

Workspace должен быть отклонён/пересмотрен как отдельная subsystem boundary, если на специально созданных coordination/bottleneck tasks выполняется совокупность:

```text
Full Workspace ≈ NoWorkspace/DirectReads
Full Workspace ≈ MatchedSharedBuffer
Workspace capacity intervention не даёт ожидаемого pattern
broadcast lesion не нарушает cross-module integration
item admission semantics не даёт специфического эффекта
```

В таком случае разумнее использовать `CognitiveState + Salience + declared reads` без отдельного Workspace.

---

# 36. Что research не доказывает

Даже если Workspace окажется функционально полезным, это доказывает только:

- пользу bounded shared communication;
- пользу dynamic admission;
- пользу temporary global availability;
- причинную роль конкретной workspace implementation.

Это **не доказывает**:

- субъективный опыт;
- сознание;
- qualia;
- эквивалентность человеческому Global Neuronal Workspace.

---

# 37. Что остаётся выбрать позднее

Не frozen:

- физическая форма Workspace;
- slot/token/byte capacity;
- admission algorithm;
- neural/non-neural router;
- cross-attention;
- learned compression;
- exact item schema;
- exact scopes;
- exact broadcast consumer set;
- update cadence;
- persistence dynamics;
- training losses;
- Cortex context packing policy.

---

# 38. Итоговые invariants

```text
CognitiveState ≠ Workspace
published state ≠ Workspace admission
SalienceProfile ≠ Workspace admission
WorkspaceBudget ≠ AttentionBudget ≠ Executive budget
WorkspaceItem ≠ source truth
Workspace ≠ Memory
Workspace eviction ≠ Memory forgetting
Memory retrieval ≠ Workspace admission
Workspace ≠ Cortex context
broadcast ≠ callback/execution
Workspace ≠ Policy
imagined Workspace ≠ real Workspace
Workspace ≠ proof of consciousness
```
