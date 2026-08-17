# Semantic Freeze Manifest F31

## Статус

**Связанный Design Update:** `DU-31 — Contract + ADR Consistency Freeze`  
**Статус:** semantic freeze manifest  
**Baseline:** `F31`

Этот документ является machine-facing картой того, **какой набор semantic contracts считается frozen для version planning после DU-31**.

Он не является Python API и не заменяет отдельные contracts.

---

# 1. Frozen contract set

В baseline `F31` входят semantic contracts:

```text
DU-07 environment.md
DU-08 perception.md
DU-09 goals.md
DU-10 cortex.md
DU-11 memory.md
DU-12 world-model.md
DU-13 self-model.md
DU-14 intrinsic-signals.md
DU-15 drives.md
DU-16 appraisal.md
DU-17 affect.md
DU-18 valuation.md
DU-19 salience.md
DU-20 memory-regulation.md
DU-21 workspace.md
DU-22 executive-control.md
DU-23 policy-planner.md
DU-24 action-boundary.md
DU-25 experience-data-replay.md
DU-26 training-lifecycle.md
DU-27 checkpoint-reproducibility-compute.md
DU-28 mindra-eval.md
DU-29 engineering-testing.md
DU-30 research-claims-limitations.md
```

Количество boundary contracts: **24**.

Foundation `DU-01 … DU-06` входит в F31 через canonical design + ADR и не требует отдельных duplicated contract files.

---

# 2. Freeze level

Для каждого перечисленного contract frozen:

- semantic responsibility;
- semantic owner/write authority;
- source-of-truth role;
- major lifecycle/commit boundaries;
- required distinction между source/derived entities;
- provenance/visibility expectations;
- revision/freshness/availability meaning;
- observability/intervention requirements;
- failure/degradation meaning на архитектурном уровне;
- snapshot/restore causally relevant state classes;
- No*/Dummy/control semantics, где они приняты;
- negative module gate, где он принят.

Не frozen:

- Python class/interface names;
- exact field names, если semantic identity однозначна;
- exact enum strings/codes;
- serialization format;
- tensor shape/dtype;
- backend/library/framework;
- algorithm/model;
- physical storage/deployment.

---

# 3. Cross-contract consistency resolutions

Версия F31 применяет:

```text
CR-01 Action lifecycle
CR-02 Memory admission ownership
CR-03 Replay taxonomy
CR-04 Consolidation vs Learning Update
CR-05 candidate/validated/activated Agent revision lifecycle
```

Полное описание: [`../contract-adr-consistency-freeze.md`](../contract-adr-consistency-freeze.md).

Version specification не может выбирать альтернативное чтение этих терминов.

---

# 4. Common semantic conventions

## Identity

Stable logical identity не равна:

- Python object identity;
- DB row position;
- vector-index slot;
- file path;
- device address.

## Revision

`revision` — versioned semantic identity/state, а не wall-clock timestamp.

## Causal base

Update/computation/result должен ссылаться на base/parent/source revision там, где stale mismatch causally material.

## Source lineage

Derived record/sample/profile/claim не теряет source lineage.

## Availability

Общий baseline:

```text
available
unknown
stale
unavailable
missing
```

Exact encoding version-specific.

## Historical immutability

Committed historical entity не переписывается молча; correction/update/review создаёт new revision/record/link.

---

# 5. Frozen distinction registry

Version design обязан сохранять минимум:

```text
CognitiveState ≠ Agent Snapshot ≠ Checkpoint
CognitiveState ≠ Workspace
MemoryRecord ≠ representation/index
Memory Core ≠ Memory Regulation
Retrieval ≠ Memory Replay ≠ Training Replay
Consolidation ≠ Learning Update
World Prediction ≠ observed fact
Intrinsic Signal ≠ Drive ≠ Value
Appraisal ≠ Affect ≠ Valuation
SalienceProfile ≠ AttentionAllocation
Scheduler ≠ Executive ≠ Policy
Planner ≠ Policy
ActionCandidate ≠ SelectedActionIntent
SelectedActionIntent ≠ AuthorizedAction ≠ Action Commit
Action Commit ≠ Dispatch ≠ Environment Transition
ExperienceEvent ≠ TrainingSample
Training Runtime ≠ cognition
CandidateRevisionBundle ≠ Active AgentRevision
ComputeManifest ≠ CognitiveResourceEnvelope
MINDRA-Eval ≠ Engineering Testing
Observation ≠ Interpretation ≠ ResearchClaim
functional similarity ≠ phenomenological equivalence
```

---

# 6. Status of conditional modules

Следующие boundaries semantic-frozen, но empirically conditional/falsifiable:

```text
Affect
Workspace
Adaptive Executive Control
Planner
```

Freeze не превращает их в доказанно необходимые modules.

`No*`/matched controls остаются обязательной частью evaluation design, где это предусмотрено canonical owner.

---

# 7. Version-spec responsibility

`DU-32` и конкретная version specification должны для каждого включённого contract определить:

- concrete implementation profile;
- exact Python/API representation;
- active optional capabilities;
- config/defaults/budgets;
- serialization where required;
- compatibility/migration needs;
- VerificationObligations;
- evaluation/control condition;
- explicit non-goals.

Если version не реализует boundary целиком, это оформляется как explicit version subset/control implementation, а не reinterpretation contract.

---

# 8. Breaking change marker

Любое изменение frozen semantic meaning требует нового ADR и новой freeze baseline revision.

Обычный implementation choice, не меняющий frozen meaning, не требует изменения F31.

---

# 9. Freeze result

```text
baseline_id: F31
semantic_contract_count: 24
foundation_scope: DU-01…DU-06
boundary_scope: DU-07…DU-30
status: ready_for_version_planning
next_design_update: DU-32
```
