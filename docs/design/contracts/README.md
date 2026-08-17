# Candidate / exact internal contracts MINDRA

## Назначение

Этот каталог хранит machine-facing semantic contracts уже принятых subsystem/data/training/reproducibility/evaluation/testing boundaries.

До общего contract freeze документы здесь остаются **candidate contracts**: они уточняют форму принятого design, но не имеют права молча менять его смысл или превращать удобный Python choice в архитектурный invariant.

---

# Текущие candidate contracts

- [`environment.md`](environment.md) — `DU-07`;
- [`perception.md`](perception.md) — `DU-08`;
- [`goals.md`](goals.md) — `DU-09`;
- [`cortex.md`](cortex.md) — `DU-10`;
- [`memory.md`](memory.md) — `DU-11`;
- [`world-model.md`](world-model.md) — `DU-12`;
- [`self-model.md`](self-model.md) — `DU-13`;
- [`intrinsic-signals.md`](intrinsic-signals.md) — `DU-14`;
- [`drives.md`](drives.md) — `DU-15`;
- [`appraisal.md`](appraisal.md) — `DU-16`;
- [`affect.md`](affect.md) — `DU-17`;
- [`valuation.md`](valuation.md) — `DU-18`;
- [`salience.md`](salience.md) — `DU-19`;
- [`memory-regulation.md`](memory-regulation.md) — `DU-20`;
- [`workspace.md`](workspace.md) — `DU-21`;
- [`executive-control.md`](executive-control.md) — `DU-22`;
- [`policy-planner.md`](policy-planner.md) — `DU-23`;
- [`action-boundary.md`](action-boundary.md) — `DU-24`;
- [`experience-data-replay.md`](experience-data-replay.md) — `DU-25`;
- [`training-lifecycle.md`](training-lifecycle.md) — `DU-26`;
- [`checkpoint-reproducibility-compute.md`](checkpoint-reproducibility-compute.md) — `DU-27`;
- [`mindra-eval.md`](mindra-eval.md) — `DU-28`;
- [`engineering-testing.md`](engineering-testing.md) — `DU-29`: VerificationObligation/Matrix, test specs, conformance/fault/state-machine/persistence evidence и CI gates.

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
Memory Replay ≠ Training Replay
Consolidation ≠ Learning Update
CognitiveState ≠ Workspace
Executive Control ≠ Scheduler ≠ Policy
Policy ≠ Planner
SelectedActionIntent ≠ AuthorizedAction ≠ Action Commit
Action Commit ≠ Dispatch ≠ Environment Transition
Experience Journal ≠ Agent runtime state
Source Experience ≠ TrainingSample
Training Runtime ≠ cognitive module
runtime dependency graph ≠ gradient graph
CandidateRevisionBundle ≠ Active AgentRevision
AgentSnapshot ≠ persistent Checkpoint
same seed ≠ same RNG state ≠ guaranteed same execution
ComputeManifest ≠ CognitiveResourceEnvelope
Evaluation Runtime ≠ Agent cognition
Task score ≠ module/causal/calibration evidence
Engineering Testing ≠ MINDRA-Eval
line coverage ≠ architectural invariant coverage
skipped/quarantined ≠ verified pass
Test Oracle ≠ Agent-visible input
```

Для Engineering Testing дополнительно:

- accepted engineering invariant имеет `VerificationObligation` или explicit non-machine-checkable status;
- `VerificationMatrix` сохраняет coverage/evidence lineage;
- capability-aware conformance не требует отсутствующую capability у `NoX`;
- fault injection не создаёт hidden production path;
- stateful tests сохраняют commit/revision/action lifecycle invariants;
- privileged sentinel/oracle leakage проверяется across agent-visible boundaries;
- bitwise assertion используется только при соответствующей guarantee;
- golden update требует reviewable semantic justification;
- flaky quarantine не считается выполненной obligation;
- `not run`/`skipped` не становятся pass;
- CI gate должен видеть unresolved verification gaps.

---

# Текущий статус

После `DU-04 … DU-29` semantic requirements приняты, но **общий exact Python contract set намеренно не frozen**.

`engineering-testing.md` остаётся candidate до Research Claims/contract freeze integration.

До contract freeze нельзя считать каноническими:

- `Protocol`/ABC/dataclass/TensorDict/Pydantic;
- exact event/status enums;
- pytest/unittest;
- Hypothesis;
- Import Linter;
- coverage/mutation tools и thresholds;
- конкретный CI provider/YAML;
- exact test directory layout;
- exact test tier names/timings;
- accelerator/provider matrix;
- concrete test artifact storage.

---

# Иерархия

```text
accepted ADR + canonical design
→ candidate/exact contract
→ version specification
→ implementation sequence
→ implementation
```
