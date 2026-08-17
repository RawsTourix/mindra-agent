# Candidate / exact internal contracts MINDRA

## Назначение

Этот каталог хранит machine-facing semantic contracts уже принятых subsystem/data boundaries.

До общего contract freeze документы здесь остаются **candidate contracts**: они уточняют форму принятого design, но не имеют права молча менять его смысл или превращать удобный Python choice в архитектурный invariant.

---

# Текущие candidate contracts

- [`environment.md`](environment.md) — Environment interaction/research boundary после `DU-07`;
- [`perception.md`](perception.md) — Canonical Percept/Semantic Core/Feature Views после `DU-08`;
- [`goals.md`](goals.md) — Goal Proposal/Committed Goal/Goal Graph после `DU-09`;
- [`cortex.md`](cortex.md) — Cortex Gateway/capabilities/request/result после `DU-10`;
- [`memory.md`](memory.md) — Memory records/representations/retrieval после `DU-11`;
- [`world-model.md`](world-model.md) — World Belief/assimilation/prediction/imagination после `DU-12`;
- [`self-model.md`](self-model.md) — capability/competence/Self Prediction после `DU-13`;
- [`intrinsic-signals.md`](intrinsic-signals.md) — typed Intrinsic Signals после `DU-14`;
- [`drives.md`](drives.md) — typed persistent Drives после `DU-15`;
- [`appraisal.md`](appraisal.md) — multidimensional Appraisal после `DU-16`;
- [`affect.md`](affect.md) — persistent Affect dynamics после `DU-17`;
- [`valuation.md`](valuation.md) — ValueProfile/ComparisonPolicy/Risk/Constraint semantics после `DU-18`;
- [`salience.md`](salience.md) — SalienceTarget/Profile, AttentionBudget и AttentionAllocation после `DU-19`;
- [`memory-regulation.md`](memory-regulation.md) — MemoryBudget, lifecycle/replay/consolidation после `DU-20`;
- [`workspace.md`](workspace.md) — Workspace proposal/admission/items/budget/broadcast/read/snapshot semantics после `DU-21`;
- [`executive-control.md`](executive-control.md) — MetaActionProposal/InternalOperationCatalog, CognitiveResourceEnvelope, ExecutiveDecision, stop/continue и budget ledger semantics после `DU-22`;
- [`policy-planner.md`](policy-planner.md) — BehavioralContext, ActionCandidate, PlanCandidate, PolicyCandidateSet, DecisionDeferral и SelectedActionIntent после `DU-23`;
- [`action-boundary.md`](action-boundary.md) — authorization stages, AuthorizedAction, ActionCommitRecord, dispatch/receipt/execution/reconciliation semantics после `DU-24`;
- [`experience-data-replay.md`](experience-data-replay.md) — ExperienceEvent/Journal, causal revisions, annotations, projections, DatasetManifest, TrainingSample и Training Replay provenance после `DU-25`.

---

# Общие требования

Contract должен фиксировать, где применимо:

- required/optional semantic fields;
- ownership/read/write boundaries;
- revision/freshness/availability;
- causal provenance;
- lifecycle;
- public/private/visibility state;
- snapshot/restore references;
- observability/intervention;
- failure/degradation;
- compatibility/serialization;
- автоматически проверяемые invariants.

Exact implementation detail одного backend не должен протекать в canonical contract без design justification.

---

# Действующие safeguards

```text
Environment Ground Truth ≠ Agent input
Canonical Percept ≠ concrete encoder latent
Goal Proposal ≠ direct Goal mutation
Cortex ≠ ambient Agent-state owner
MemoryRecord ≠ embedding/index
World Prediction ≠ observed fact
Self Prediction ≠ Policy decision
Intrinsic Signal ≠ reward/value
Drive State ≠ global motivation/value
Appraisal ≠ emotion/value/Affect
Affect ≠ emotion label/Drive/value
ValueProfile ≠ mandatory scalar/reward/Policy decision
SalienceProfile ≠ AttentionAllocation
Memory Core validation ≠ Regulation admission
Forgetting ≠ physical deletion
Memory Replay ≠ Training Replay
Consolidation ≠ in-place rewrite ≠ Learning Update
CognitiveState ≠ Workspace
Workspace ≠ Memory ≠ Cortex context
Executive Control ≠ Cognitive Scheduler ≠ Policy
Policy ≠ Planner
Plan ≠ ImaginedTrajectory
ActionCandidate ≠ SelectedActionIntent
SelectedActionIntent ≠ AuthorizedAction ≠ Action Commit
Action Commit ≠ Dispatch ≠ Environment Transition
TraceEvent ≠ ExperienceEvent
Experience Journal ≠ Agent runtime state
Experience Journal ≠ Replay Buffer ≠ Agent Memory
Source Experience ≠ TrainingSample
ResearchAnnotation ≠ agent-visible payload
```

Для Experience / Data / Replay дополнительно:

- source Experience Events immutable по смыслу;
- hindsight/relabel/re-encode не переписывают source events;
- physical append/ingest order не заменяет causal parent/logical order;
- privileged/evaluator-only data входит через separate annotation + explicit visibility policy;
- `ActionCommitRecord` без Environment transition остаётся валидным data case;
- `execution_unknown` не получает fake next state;
- mixed `agent_revision` и component revisions сохраняются;
- derived projection/sample имеет source refs + transform lineage;
- terminated/truncated различаются до explicit training transform;
- replay buffer/table не является archival source;
- replay sampling metadata не становится cognitive importance;
- Agent Memory Replay и Training Replay имеют разные owners/event kinds;
- heavy artifacts могут отсутствовать отдельно от core causal completeness;
- lossy data transformation маркируется как lossy;
- dataset split/source manifest фиксируются для reproducibility.

---

# Текущий статус

После `DU-04 … DU-25` semantic requirements приняты, но **общий exact Python contract set намеренно не frozen**.

`experience-data-replay.md` остаётся candidate до Training/Checkpoint/Evaluation integration.

До contract freeze нельзя считать каноническими:

- `Protocol`/ABC/dataclass/TensorDict/Pydantic;
- exact event enum;
- nullable/union encoding;
- JSONL/Arrow/Parquet/HDF5/TFRecord/RLDS/Minari;
- database/storage engine;
- replay backend/table technology;
- reward/target mapping;
- replay priority algorithm;
- sequence/window length;
- training batch/tensor layout;
- checkpoint payload format;
- public export format.

---

# Иерархия

```text
accepted ADR + canonical design
→ candidate/exact contract
→ version specification
→ implementation sequence
→ implementation
```
