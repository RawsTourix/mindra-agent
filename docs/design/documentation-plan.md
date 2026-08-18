# План проектирования документации MINDRA

## Статус документа

**Статус:** завершённый исторический design-plan.  
**Область:** `DU-00 … DU-32`.

Этот документ фиксирует порядок, в котором была спроектирована общая архитектурная документация MINDRA.

Он **не является текущим roadmap реализации** и не определяет следующий разрешённый software milestone. Актуальный статус всегда определяется [`current.md`](current.md), а software roadmap — [`version-roadmap.md`](version-roadmap.md).

Общий design-cycle завершён:

```text
DU-00 … DU-32 complete
Semantic Freeze Baseline F31 accepted
software roadmap accepted
```

Документ сохраняется как карта зависимостей и как объяснение того, почему архитектурные темы проектировались именно в таком порядке.

---

# 1. Что означал Design Update

Каждый идентификатор `DU-xx` обозначал самостоятельный **Design Update**: ограниченный documentation patch, закрывающий один связный набор архитектурных вопросов до перехода к следующему слою.

Базовый принцип цикла:

```text
не проектировать следующий слой через предположения
о ещё не определённом предыдущем слое
```

Каждый DU должен был:

1. иметь чёткую цель и prerequisites;
2. отделять собственный scope от downstream вопросов;
3. при нетривиальном выборе опираться на targeted research;
4. сравнивать реалистичные варианты и trade-offs;
5. определять canonical owner темы;
6. фиксировать значимые решения ADR;
7. обновлять связанные glossary/index/contracts/status documents;
8. иметь completion gate.

После завершения `DU-31` semantic meaning общей архитектуры был заморожен как baseline `F31`; `DU-32` затем разбил её на software milestones.

---

# 2. Фактическая завершённая цепочка

```text
DU-00 Documentation Foundation
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
DU-28 MINDRA-Eval
        ↓
DU-29 Engineering Testing
        ↓
DU-30 Research Claims / Limitations
        ↓
DU-31 Contract + ADR Consistency Freeze
        ↓
DU-32 Version Roadmap
```

Это был порядок **semantic design**, а не literal runtime DAG и не порядок реализации software.

---

# 3. Фактические canonical owners

## Foundation

| DU | Тема | Canonical owner |
|---|---|---|
| `DU-00` | Documentation Foundation | `project-concept.md`, `architecture-concept.md`, `research-methodology.md`, foundation-файлы `design/` |
| `DU-01` | System Context | [`system-context.md`](system-context.md) |
| `DU-02` | Dependency & Composition | [`dependency-rules.md`](dependency-rules.md) |
| `DU-03` | Runtime / Temporal Model | [`execution-model.md`](execution-model.md) |
| `DU-04` | CognitiveState | [`cognitive-state.md`](cognitive-state.md) |
| `DU-05` | Module Protocol / Scheduling | [`module-lifecycle.md`](module-lifecycle.md) |
| `DU-06` | Observability / Intervention | [`observability-and-intervention.md`](observability-and-intervention.md) |

## Cognitive/runtime boundaries

| DU | Тема | Canonical owner |
|---|---|---|
| `DU-07` | Environment | [`modules/environment.md`](modules/environment.md) |
| `DU-08` | Perception | [`modules/perception.md`](modules/perception.md) |
| `DU-09` | Goals | [`modules/goals.md`](modules/goals.md) |
| `DU-10` | Cortex | [`modules/cortex.md`](modules/cortex.md) |
| `DU-11` | Memory Core | [`modules/memory.md`](modules/memory.md) |
| `DU-12` | World Model | [`modules/world-model.md`](modules/world-model.md) |
| `DU-13` | Self Model | [`modules/self-model.md`](modules/self-model.md) |
| `DU-14` | Intrinsic Signals | [`modules/intrinsic-signals.md`](modules/intrinsic-signals.md) |
| `DU-15` | Drives | [`modules/drives.md`](modules/drives.md) |
| `DU-16` | Appraisal | [`modules/appraisal.md`](modules/appraisal.md) |
| `DU-17` | Affect | [`modules/affect.md`](modules/affect.md) |
| `DU-18` | Valuation | [`modules/valuation.md`](modules/valuation.md) |
| `DU-19` | Salience / Attention | [`modules/salience.md`](modules/salience.md) |
| `DU-20` | Memory Regulation | [`modules/memory-regulation.md`](modules/memory-regulation.md) |
| `DU-21` | Workspace | [`modules/workspace.md`](modules/workspace.md) |
| `DU-22` | Executive Control | [`modules/executive-control.md`](modules/executive-control.md) |
| `DU-23` | Policy / Planner | [`modules/policy-planner.md`](modules/policy-planner.md) |
| `DU-24` | Action Boundary | [`modules/action-boundary.md`](modules/action-boundary.md) |

## External planes и завершение архитектурного цикла

| DU | Тема | Canonical owner |
|---|---|---|
| `DU-25` | Experience / Data / Replay | [`experience-data-replay.md`](experience-data-replay.md) |
| `DU-26` | Training Lifecycle | [`training-lifecycle.md`](training-lifecycle.md) |
| `DU-27` | Checkpoint / Reproducibility / Compute | [`checkpoint-reproducibility-compute.md`](checkpoint-reproducibility-compute.md) |
| `DU-28` | MINDRA-Eval | [`mindra-eval.md`](mindra-eval.md) |
| `DU-29` | Engineering Testing | [`engineering-testing.md`](engineering-testing.md) |
| `DU-30` | Research Claims / Limitations | [`research-claims-limitations.md`](research-claims-limitations.md) |
| `DU-31` | Semantic consistency freeze | [`contract-adr-consistency-freeze.md`](contract-adr-consistency-freeze.md) |
| `DU-32` | Version Roadmap | [`version-roadmap.md`](version-roadmap.md) |

Machine-facing semantic contracts находятся в [`contracts/`](contracts/), а accepted decisions — в [`decisions/`](decisions/).

---

# 4. Почему порядок отличался от software roadmap

Порядок DU отвечал на вопрос:

> в какой последовательности нужно определить semantics и ownership, чтобы downstream design не строился на догадках?

Software roadmap отвечает на другой вопрос:

> в какой последовательности реализовать runnable vertical slices, чтобы каждая версия была проверяемой и не требовала semantic rewrite?

Поэтому после `DU-32` принята отдельная capability ladder:

```text
v0.1 Core Kernel
→ v0.2 MicroWorld Interaction
→ v0.3 Cortex Gateway
→ v0.4 Memory & Restore
→ v0.5 World & Self
→ v0.6 Intrinsic / Drives / Appraisal
→ v0.7 Affect / Valuation / Salience
→ v0.8 Memory Regulation / Workspace
→ v0.9 Executive / Planner
→ v0.10 Training & Revision Lifecycle
→ v0.11 Research Harness
→ v0.12 Integration Hardening
→ v1.0 MINDRA Research Baseline
```

Canonical owner: [`version-roadmap.md`](version-roadmap.md).

---

# 5. Ключевые разделения, полученные в ходе DU-cycle

Ниже перечислены distinction, которые особенно важны для дальнейшей реализации:

```text
CognitiveState ≠ Agent Snapshot ≠ Checkpoint
CognitiveState ≠ Workspace
MemoryRecord ≠ representation/index
Memory Core ≠ Memory Regulation
Retrieval ≠ Agent Memory Replay ≠ Training Replay
Consolidation ≠ Learning Update
World Prediction ≠ observed fact
Intrinsic Signal ≠ Drive ≠ Value
Appraisal ≠ Affect ≠ Valuation
SalienceProfile ≠ AttentionAllocation
Scheduler ≠ Executive Control ≠ Policy
Planner ≠ Policy
SelectedActionIntent ≠ AuthorizedAction ≠ Action Commit
Action Commit ≠ Dispatch ≠ Environment Transition
ExperienceEvent ≠ TrainingSample
Training Runtime ≠ cognition
CandidateRevisionBundle ≠ Active AgentRevision
MINDRA-Eval ≠ Engineering Testing
Observation ≠ Interpretation ≠ ResearchClaim
functional similarity ≠ phenomenological equivalence
```

Полное нормативное чтение задаёт baseline `F31`, а не этот исторический план.

---

# 6. Consistency freeze

`DU-31` закрыл накопившиеся междокументные неоднозначности перед roadmap.

Canonical resolutions:

```text
CR-01 Action lifecycle
CR-02 Memory admission ownership
CR-03 Replay taxonomy
CR-04 Consolidation vs Learning Update
CR-05 candidate/validated/activated revision lifecycle
```

Их нормативный owner:

- [`contract-adr-consistency-freeze.md`](contract-adr-consistency-freeze.md);
- [`contracts/semantic-freeze-manifest.md`](contracts/semantic-freeze-manifest.md);
- специализированные поздние canonical owners соответствующих responsibilities.

Version-specific design не должен возвращаться к более ранней generic формулировке, если она была уточнена F31.

---

# 7. Правило для будущих изменений

Завершение DU-cycle не означает, что архитектура объявлена неизменной навсегда.

Если implementation или research evidence обнаруживает semantic blocker:

```text
blocker / evidence
→ design review
→ новый ADR при semantic change
→ canonical owner / contract update
→ новая freeze baseline revision
→ roadmap/version update
→ implementation
```

Нельзя исправлять semantic mismatch только локальным кодом или version README.

Если меняется лишь concrete implementation choice при сохранении F31 meaning, новый global DU не требуется.

---

# 8. Текущий следующий шаг

Этот документ больше **не определяет текущий следующий шаг**.

Фактический статус находится только в [`current.md`](current.md).

На момент завершения `DU-32` следующий этап установлен как:

```text
Version Design — v0.1 Core Kernel
```

Перед coding должны быть приняты:

```text
docs/versions/v0.1/README.md
docs/versions/v0.1/implementation-sequence.md
```

После начала реализации дальнейшее движение определяется version-specific design, acceptance gates и `current.md`, а не историческим порядком `DU-00 … DU-32`.
