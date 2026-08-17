# Memory Regulation / Consolidation MINDRA

## Статус документа

**Design Update:** `DU-20 — Memory Regulation / Consolidation`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ совместно с [`memory.md`](memory.md)

[`memory.md`](memory.md) остаётся каноническим владельцем нейтрального `Memory Core`: identity `MemoryRecord`, store, retrieval, representations/indexes и базовой write validation. Этот документ добавляет поверх него **agent-owned regulation responsibility**: управляемое admission, retention, aging/forgetting, eviction, internal replay и source-preserving consolidation.

`Memory Regulation` является отдельной архитектурной ответственностью, но **не вторым владельцем Memory Store**. Она формирует versioned решения/предложения; commit record/lifecycle state остаётся за `Memory Core`.

Документ определяет:

- границу `Memory Core ↔ Memory Regulation`;
- admission при ограниченной capacity;
- `MemoryRegulationProfile` и purpose-specific policy;
- explicit memory budgets;
- retention/aging/forgetting/eviction;
- различие cognitive forgetting и physical deletion;
- влияние Salience без `salience = retention` shortcut;
- recency/diversity/redundancy/source/provenance evidence;
- internal Memory replay/reactivation;
- различие Agent Memory replay и Training Runtime replay;
- Consolidation Event;
- episodic → derived/semantic `MemoryRecord`;
- source preservation и lineage;
- contradiction/supersession semantics;
- provenance/authority non-amplification;
- representation maintenance/re-encoding;
- границу с slow-weight learning;
- logical-time semantics;
- observability/intervention;
- snapshot/revision/failure/degradation;
- `NoRegulation`, episodic-only и matched controls.

Документ опирается на:

- [`memory.md`](memory.md) — canonical store/record/retrieval boundary;
- [`salience.md`](salience.md) — purpose-dependent allocation evidence;
- [`../execution-model.md`](../execution-model.md) — `Consolidation Event`, replay и logical time;
- [`../cognitive-state.md`](../cognitive-state.md) — committed revisions/ownership;
- [`../module-lifecycle.md`](../module-lifecycle.md) — staged effects/atomic commit;
- [`../observability-and-intervention.md`](../observability-and-intervention.md) — evidence/intervention;
- [`appraisal.md`](appraisal.md), [`affect.md`](affect.md), [`drives.md`](drives.md), [`valuation.md`](valuation.md) — возможные explicit evidence sources, но не владельцы memory lifecycle;
- [`perception.md`](perception.md) — representation/version semantics.

Документ намеренно **не** определяет:

- конкретный neural consolidation model;
- mandatory LLM summarization;
- конкретную forgetting curve;
- universal `memory_importance` scalar;
- fixed top-K/FIFO/LRU policy как canonical;
- Training Runtime replay/data schema — `DU-25/26`;
- optimizer/gradient/slow-weight update — `DU-26`;
- exact checkpoint encoding — `DU-27`;
- Workspace — `DU-21`;
- Executive scheduling consolidation on demand — `DU-22`;
- exact Python API.

---

# 1. Цель DU-20

`DU-11` намеренно сделал Memory Core почти нейтральным:

```text
valid MemoryWriteProposal
→ explicit baseline admission
→ MemoryRecord
```

Это было необходимо, чтобы не зашить «важность» до появления Goals/Drives/Appraisal/Affect/Valuation/Salience.

После `DU-19` система уже умеет представлять разнородную significance/priority evidence. Теперь Memory должна уметь отвечать на отдельные вопросы:

```text
что принять в память при ограниченном бюджете?
что продолжать удерживать?
что временно сделать менее доступным?
что логически забыть/evict?
что переактивировать при consolidation?
из каких episodes вывести более устойчивое знание?
```

Но эти вопросы **не являются одним и тем же ranking problem**.

---

# 2. Главное архитектурное решение

MINDRA принимает **source-preserving, budget-aware Memory Regulation layer с purpose-specific policies и gated consolidation**.

Conceptually:

```text
MemoryWriteProposal / existing MemoryRecord set
        +
explicit memory-specific evidence
        +
optional SalienceProfile / other declared evidence
        +
MemoryBudget
        ↓
Memory Regulation
        ↓
MemoryRegulationProfile
        ↓
purpose-specific RegulationPolicy
        ↓
RegulationDecision / Proposal
        ↓
Memory Core validation + atomic commit
        ↓
new memory_revision
```

Для consolidation:

```text
explicit Consolidation Event
        ↓
source MemoryRecord candidates
        ↓
Replay/Consolidation selection
        ↓
source-preserving derivation
        ↓
DerivedMemoryRecordProposal
        ↓
Memory Core validation
        ↓
new derived MemoryRecord
        ├── derived_from source IDs
        ├── support/contradiction refs
        └── derivation provenance
```

Ключевые invariants:

```text
MemoryRecord source evidence ≠ derived summary
forgetting ≠ physical deletion
retrieval frequency ≠ importance
SalienceProfile ≠ retention decision
internal Memory replay ≠ Training Runtime replay
consolidation ≠ optimizer update
consolidation ≠ in-place rewrite of past
```

Решение фиксируется в `ADR-0020`.

---

# 3. Module gate и ownership

## 3.1. Почему regulation — отдельная responsibility

Она имеет собственные:

- decision semantics при ограниченной capacity;
- policy revisions;
- budgets;
- aging/access-history state;
- replay/consolidation selection;
- causal interventions;
- evaluation/control strategy.

Эти функции не принадлежат retrieval, Appraisal, Salience или Valuation.

## 3.2. Почему это не второй Memory Store owner

`Memory Core` остаётся единственным владельцем:

- canonical record identity;
- canonical payload/provenance;
- record lifecycle commit;
- store revision.

`Memory Regulation` владеет **policy state и decisions**, но не делает direct mutation store.

```text
Regulation decides/proposes
Memory Core validates/commits
```

## 3.3. Не обязателен один monolithic trainable module

Future implementation может иметь:

- rule-based policies;
- отдельные admission/retention/consolidation providers;
- learned policy;
- hybrid configuration.

Канонична responsibility boundary, а не один класс/NN.

---

# 4. Два этапа admission

Memory write теперь должен различать:

## 4.1. Core eligibility/validation

`Memory Core` проверяет:

- schema;
- write authority;
- agent-visible information discipline;
- provenance;
- source validity;
- duplicate identity/error conditions.

Невалидный proposal нельзя «спасти» высоким Salience.

## 4.2. Regulation admission

Только после structural validity policy решает, стоит ли принять eligible proposal при текущем budget/context.

```text
invalid proposal
→ reject by Memory Core

valid proposal
→ RegulationProfile
→ admit / defer / reject / degrade
```

Точные result enum не frozen.

---

# 5. MemoryRegulationProfile

Не вводится один универсальный:

```text
memory_importance = 0.82
```

Вместо этого policy получает typed profile с evidence, релевантным конкретной операции.

Conceptually:

```text
MemoryRegulationProfile
├── target memory/proposal ID
├── purpose
├── source/provenance quality
├── age / recency evidence
├── access/retrieval-history evidence
├── redundancy / similarity evidence
├── diversity / coverage contribution
├── contradiction / unresolved-evidence role
├── scope / expiration constraints
├── storage/index cost
├── optional SalienceProfile
├── optional Value/Appraisal/Affect-derived declared evidence
├── representation compatibility state
├── uncertainty/support
└── revisions/provenance
```

Один profile не обязан содержать все поля.

---

# 6. Purpose-specific RegulationPolicy

Admission, eviction, replay и consolidation — разные decisions.

Поэтому policy всегда имеет purpose:

```text
admission
retention_review
eviction
reactivation/replay_selection
consolidation_candidate_selection
consolidation_acceptance
representation_maintenance
```

Одинаковая запись может иметь:

```text
high replay priority
low eviction priority
medium consolidation priority
```

Нет требования общей шкалы между purposes.

---

# 7. MemoryBudget

Regulation работает не с неявной «ограниченной памятью», а с explicit budget.

Budget может быть многомерным:

```text
record count
canonical payload bytes
active retrieval tier budget
representation/index cost
retrieval-context cost estimate
consolidation compute allowance
```

Конкретные units первой версии не frozen.

Важно:

```text
MemoryBudget
≠
Executive global compute budget
```

Memory subsystem получает разрешённый budget/context; она не увеличивает сама число Cognitive Cycles/Cortex calls.

---

# 8. Retention

Retention — policy решения о сохранении доступности/долговечности record во времени.

Potential evidence:

- Goal-related usefulness;
- future retrieval utility estimate;
- Salience;
- novelty/information;
- source uniqueness;
- contradiction coverage;
- representational diversity;
- recency;
- usage history;
- storage cost;
- scope/lifecycle.

Но ни один source не является автоматическим правилом.

Например:

```text
high salience
≠
retain forever
```

и:

```text
frequently retrieved
≠
objectively important
```

---

# 9. Retrieval history и self-reinforcing loops

Если запись чаще retrieval'ится, она может чаще влиять на future decisions и снова чаще retrieval'иться.

Поэтому запрещено скрытое:

```text
retrieval_count ↑
→ retention_strength ↑
→ retrieval probability ↑
→ ...
```

Usage history может быть explicit evidence, но policy должна иметь identity/revision и исследоваться на feedback/confirmation bias.

Нужны controls, где access history shuffled/disabled.

---

# 10. Aging и logical time

Memory aging использует принятую temporal model.

По умолчанию:

```text
logical experience / session / episode age
≠
wall-clock age
```

GPU latency, Colab pause или медленный network не должны автоматически «старить» memory.

Если wall-clock действительно становится значимым agent-visible временем в конкретной Environment/task, оно должно войти через explicit contract.

Не принимается одна Ebbinghaus-like forgetting curve как universal architecture.

---

# 11. Forgetting ≠ deletion

`Forgetting` в MINDRA означает **изменение agent-accessibility/retention state**, а не обязательное уничтожение байтов.

Нужно различать минимум semantics:

```text
active/normal accessibility
reduced/deprioritized accessibility
logically unavailable/forgotten to Agent
expired by scope
physically removed payload
```

Exact lifecycle names не frozen.

## 11.1. Cognitive forgetting

Может выражаться:

- исключением из normal retrieval eligibility;
- понижением retrieval tier;
- removal из active memory capacity;
- explicit lifecycle status.

## 11.2. Physical deletion

Это storage operation.

Physical deletion может быть нужна из-за hard capacity/privacy/cleanup policy, но не должна маскироваться как обычная cognitive forgetting semantics.

Если payload уничтожен, experiment/checkpoint evidence должен позволять отличить это от reversible logical forgetting настолько, насколько разрешает retention policy.

---

# 12. Eviction

Eviction — explicit capacity-management decision.

Она не обязана означать physical erasure.

Policy families могут учитывать:

```text
recency
random
cost
redundancy
diversity
Salience
Goal/value relevance
contradiction preservation
usage history
```

Но canonical default не выбран.

Особое правило:

> Eviction не должна молча удалять единственное evidence, на котором основан derived consolidated record, без обновления lineage/support status.

---

# 13. Diversity и confirmation bias

Memory regulation должна позволять policies, сохраняющие не только наиболее часто подтверждаемую информацию.

Причины:

- редкое evidence может опровергать популярную гипотезу;
- repeated retrieval создаёт popularity bias;
- aggressive consolidation может стирать minority/contradictory traces;
- salience/value могут быть ошибочны.

Поэтому policy contract должен уметь учитывать:

```text
coverage
diversity
contradiction role
source independence
uncertainty
```

Но exact diversity metric не frozen.

---

# 14. Salience integration

`DU-19` предоставляет purpose-dependent `SalienceProfile`/`AttentionAllocation`.

Для Memory Regulation допустим pattern:

```text
Memory candidates
      ↓
Salience request
purpose = memory_regulation_hint
      ↓
SalienceProfile / allocation evidence
      ↓
MemoryRegulationProfile
      ↓
Memory RegulationPolicy
```

Ключевой invariant:

```text
SalienceProfile
≠
Memory retention decision
```

Memory Regulation добавляет memory-specific evidence: redundancy, capacity cost, age, contradiction coverage, source integrity и т.д.

---

# 15. Appraisal / Affect / Drives / Valuation relation

MINDRA допускает исследовательские hypotheses, где internal state влияет на memory regulation.

Например:

```text
Appraisal/Affect/Drive context
        ↓
Salience for memory purpose
        ↓
Memory Regulation
```

или explicit declared policy input, если это обосновано design/version.

Но запрещены universal shortcuts:

```text
negative affect → remember more
high drive pressure → retain forever
high value → never forget
```

Любой mapping versioned, observable и intervenable.

---

# 16. Internal Memory Replay / Reactivation

`Memory Regulation` вводит agent-owned **reactivation/replay selection**, но не hidden background cognition.

Conceptually:

```text
explicit Consolidation Event
        ↓
ReplayCandidateSet
        ↓
RegulationPolicy
        ↓
MemoryReplaySelection
        ↓
explicit reactivation operations
```

`MemoryReplaySelection` содержит source `memory_id`, base `memory_revision`, selection policy/revision и provenance.

## 16.1. Retrieval ≠ replay

```text
Retrieval
→ query-driven access для текущего cognitive consumer

Memory replay/reactivation
→ explicit re-presentation существующего memory content в consolidation/maintenance context
```

## 16.2. Replay не является новым опытом

Replay:

- не увеличивает Environment Transition counter;
- не становится новым natural visitation;
- не меняет original event provenance;
- не создаёт новый MemoryRecord автоматически.

---

# 17. Agent Memory Replay ≠ Training Replay

Канонически:

```text
Agent Memory Replay
≠
Training Runtime Experience Replay
```

### Agent Memory Replay

- часть agent-owned memory dynamics;
- reactivates existing `MemoryRecord`;
- может служить consolidation/maintenance;
- не обязан менять trainable weights.

### Training Replay

- внешний Training Runtime;
- использует experience/data для Learning Update;
- относится к `DU-25/26`;
- может использовать совершенно другой sampling/buffer semantics.

Prioritized Experience Replay в RL является полезным evidence, что sampling history способен влиять на learning efficiency, но не определяет Agent Memory Replay MINDRA.

---

# 18. Consolidation Event

`DU-03` уже выделил `Consolidation Event` отдельно от Cognitive Cycle/Environment Transition/Learning Update.

`DU-20` уточняет его semantics:

```text
Consolidation Event
├── event_id
├── base memory_revision
├── logical time identity
├── candidate-selection policy
├── allowed compute/capabilities
├── source lineage
└── output proposals / evidence
```

Consolidation Event не запускается скрытым background thread.

На текущем design этапе его initiation может быть fixed runtime/lifecycle policy. Future `DU-22` сможет решить, когда стоит инициировать дополнительную consolidation работу.

---

# 19. Consolidation как derivation, а не rewrite

Канонический pattern:

```text
M1 episodic
M2 episodic
M3 episodic
      ↓
Consolidation
      ↓
M20 derived/semantic
  derived_from = [M1,M2,M3]
```

Неправильно:

```text
M1.content = "обобщённая новая истина"
```

Original records остаются историческими evidence objects, пока отдельная retention policy не меняет их accessibility/lifecycle.

---

# 20. Derived / semantic MemoryRecord

Derived record является **новым canonical MemoryRecord**, а не особым privileged truth object.

Он должен сохранять минимум conceptual provenance:

```text
derived memory_id
source memory IDs
supporting sources
contradicting sources?
derivation method/revision
Cortex/backend provenance?, если использован
confidence/support semantics?
creation Consolidation Event
source memory_revision(s)
agent_revision
```

Derived record может быть:

- summary;
- abstraction;
- generalized fact/hypothesis;
- cluster prototype/structured relation;
- compressed episode bundle.

Concrete taxonomy не frozen.

---

# 21. Source preservation и provenance non-amplification

Consolidation не имеет права стирать origin semantics.

Например:

```text
source:
Cortex inference / uncertain observation
```

не превращается после summarization в:

```text
observed fact
```

только потому, что текст стал короче/увереннее.

Derived record обязан сохранять source-authority/provenance ограничения или более консервативную uncertainty semantics.

Если разные sources конфликтуют, consolidation должна либо:

- сохранить conflict explicitly;
- сформировать hypothesis с support/conflict metadata;
- отказаться от derivation.

Нельзя скрыто majority-vote'ить противоречие в «истину» без versioned policy.

---

# 22. Consolidation не обязана происходить всегда

Допустимые decisions:

```text
retain raw only
consolidate and retain raw
consolidate + later regulate raw independently
defer consolidation
reject unsafe/unsupported derivation
```

Поэтому `NoConsolidation`/episodic-only является first-class control.

Consolidation trigger может учитывать:

- recurrence;
- redundancy;
- budget pressure;
- evidence density;
- cross-episode regularity;
- query/use patterns;
- unresolved contradiction;
- explicit experiment schedule.

Но один trigger не принят universal default.

---

# 23. Consolidation correctness и later correction

Derived record может оказаться ошибочным.

Поэтому historical derived payload не переписывается молча.

При новом evidence предпочтительны:

```text
new derived record
supersedes / contradicts / refines old derived record
```

или explicit lifecycle invalidation.

Если исходные source records сохранены, consolidation можно пересчитать другим algorithm/revision и сравнить outputs.

---

# 24. Representation maintenance ≠ semantic consolidation

Re-encoding старых MemoryRecords под новый retrieval encoder:

```text
MemoryRecord M5
feature space F2 → F3
```

не создаёт автоматически новое semantic memory.

Это `representation maintenance`:

- новый `MemoryRepresentation`;
- index rebuild/update;
- compatibility manifest.

Канонический payload M5 остаётся тем же.

Semantic consolidation создаёт новый derived record с новой identity.

---

# 25. Slow weights / learned parameters boundary

`DU-20` **не выполняет optimizer update trainable weights**.

Если consolidation/replay должен позднее обучать:

- World Model;
- Cortex adapter;
- Policy;
- learned semantic memory network;

`DU-20` может сформировать explicit evidence/candidate set для будущего Training Runtime, но actual Learning Update относится к `DU-26`.

То есть:

```text
Consolidation Event
≠
Learning Update
```

Это сохраняет temporal semantics `DU-03`.

---

# 26. Catastrophic forgetting boundary

В `DU-20` термин `catastrophic forgetting` нельзя использовать просто для eviction records.

Catastrophic forgetting trainable model weights — проблема будущего continual learning/Training Lifecycle.

Memory Regulation может помогать будущему training через:

- coverage-preserving replay candidates;
- diversity;
- old/new interleaving evidence;
- source-preserving episodes.

Но сам gradient-based mitigation относится к `DU-26`.

---

# 27. Cortex relation

Cortex может быть optional derivation capability:

```text
selected source records
→ explicit CortexRequest
→ derived candidate
→ ConsolidationProposal
→ Memory Core validation
```

Но Cortex:

- не сканирует Memory ambient способом;
- не получает direct write authority;
- не уничтожает source provenance;
- не делает свою summary automatically true;
- не скрыто выбирает retention policy.

`NoCortex` consolidation должен оставаться возможным для rule-based/structured implementations, если concrete version его поддерживает.

---

# 28. Observability

Минимальный evidence должен позволять восстановить:

```text
какие candidates рассматривались
какой MemoryBudget действовал
какие profile components были доступны
какая RegulationPolicy/revision использована
что было admitted/rejected/deferred/evicted
какие records replay'ились
какие sources вошли в consolidation
какой derived record создан
какие contradictions/support сохранились
какой Cortex/backend использован
какая memory_revision получилась
```

Policy decision без причинной provenance недостаточна для research claims.

---

# 29. Interventions

Допустимы controlled interventions:

- изменить admission policy;
- изменить MemoryBudget;
- clamp/remove Salience evidence;
- shuffle recency/access evidence;
- изменить retention status target;
- force/forbid eviction;
- изменить replay candidate order;
- force/defer Consolidation Event;
- заменить source set consolidation;
- inject contradictory memory through Intervention Gateway;
- заменить consolidation algorithm/revision.

Intervention не переписывает natural lineage молча.

---

# 30. Snapshot / reproducibility

Exact Agent Snapshot должен включать causally relevant Memory Regulation state:

```text
Memory Core snapshot
Regulation system/policy revisions
MemoryBudget state
record lifecycle/accessibility state
aging/logical-time markers
usage/access history, если policy её использует
replay/reactivation history
consolidation lineage/derived relations
pending consolidation state
representation-maintenance manifests
policy RNG
intervention/degradation state
```

Одинаковый Memory Store без одинакового regulation state не обязательно даёт одинаковое future memory behavior.

---

# 31. Failure / degradation

Нужно различать:

```text
capacity exhausted
regulation policy unavailable
required evidence unavailable
representation incompatible
consolidation failed
consolidation unsupported
Cortex unavailable
derived proposal validation failed
source record unavailable
snapshot/restore mismatch
```

Failure не должен скрыто приводить к другой policy.

Fallback допустим только explicit/degradation-provenance способом.

---

# 32. Controls / baselines

Обязательные классы control:

```text
NoRegulation / accept-all-until-budget
NoConsolidation / episodic-only
FIFO / oldest-first
recency-only
random retention/eviction
uniform replay
random replay
shuffled evidence
Salience-only
value-only
matched learned policy without target semantics
fixed periodic consolidation
random grouping consolidation
retain-raw-only
oracle research control
```

Exact set конкретного experiment определяется `MINDRA-Eval`, но architecture должна позволять такие подмены.

---

# 33. Functional gate

Memory Regulation считается функционально обоснованной, если при matched resource budgets она демонстрирует causal benefit сверх простых controls.

Нужно проверять отдельно:

```text
retention efficiency
retrieval utility
behavioral performance
source/provenance fidelity
contradiction preservation
false/incorrect consolidated memory rate
budget efficiency
generalization
robustness under distribution shift
```

Простого «память стала меньше» недостаточно.

Для consolidation особенно важны:

```text
Full consolidation
vs episodic-only
vs random consolidation
vs matched compression
```

Если consolidated memory ухудшает correctness или стирает provenance, отрицательный результат должен сохраняться как research evidence.

---

# 34. Что сознательно отложено

До будущих DU не фиксируются:

- exact memory budgets первой версии;
- конкретная forgetting curve;
- конкретная replay priority formula;
- exact semantic consolidation model;
- LLM prompt для summarization;
- cluster algorithm;
- learned retention network;
- generative replay model;
- gradient updates;
- exact data schema;
- exact checkpoint serialization.

---

# 35. Следующий шаг

После принятия `DU-20` разрешён:

```text
DU-21 — Workspace
```

К этому моменту Memory уже умеет:

```text
store/retrieve
+
regulate retention/accessibility
+
select explicit reactivation
+
create source-preserving derived knowledge
```

а `DU-21` сможет отдельно проверить, нужен ли MINDRA ограниченный temporary shared Workspace поверх обычного `CognitiveState` и Salience allocation.
