# Semantic internal contracts MINDRA

## Назначение

Этот каталог хранит machine-facing semantic contracts принятых subsystem/data/training/reproducibility/evaluation/testing/research-claim boundaries.

После `DU-31 — Contract + ADR Consistency Freeze` contracts `DU-07 … DU-30` считаются **semantic-frozen for roadmap baseline F31**.

Это означает:

- responsibility/ownership/lifecycle/source/provenance meaning frozen;
- exact Python/API/serialization representation **не frozen**;
- version specification может конкретизировать representation без нового ADR, если semantic meaning сохраняется.

Freeze manifest:

- [`semantic-freeze-manifest.md`](semantic-freeze-manifest.md).

Canonical consistency owner:

- [`../contract-adr-consistency-freeze.md`](../contract-adr-consistency-freeze.md).

---

# Semantic-frozen contract set F31

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
- [`engineering-testing.md`](engineering-testing.md) — `DU-29`;
- [`research-claims-limitations.md`](research-claims-limitations.md) — `DU-30`.

Количество: **24 semantic boundary contracts**.

Foundation `DU-01 … DU-06` входит в F31 через canonical design/ADR и не дублируется отдельными contract files.

---

# Общие frozen requirements

Contract должен сохранять, где применимо:

- semantic owner/read/write boundary;
- source-of-truth entity;
- required/optional semantic information;
- revision/freshness/availability;
- causal provenance/lineage;
- lifecycle/commit boundary;
- public/private/visibility/trust semantics;
- snapshot/restore causally relevant state;
- observability/intervention;
- failure/degradation;
- compatibility/migration meaning;
- control/No*/Dummy semantics;
- machine-checkable invariants, где practically возможно.

Exact implementation detail одного backend не должен протекать в contract meaning без нового design justification/ADR.

---

# Freeze consistency resolutions

Baseline F31 применяет:

```text
CR-01 Action lifecycle
CR-02 Memory admission ownership
CR-03 Replay taxonomy
CR-04 Consolidation vs Learning Update
CR-05 candidate/validated/activated revision lifecycle
```

Полное описание — [`../contract-adr-consistency-freeze.md`](../contract-adr-consistency-freeze.md).

---

# Действующие safeguards

```text
Environment Ground Truth ≠ Agent input
Canonical Percept ≠ concrete encoder latent
Goal Proposal ≠ direct Goal mutation
Cortex ≠ ambient Agent-state owner
MemoryRecord ≠ embedding/index
Memory Core ≠ Memory Regulation
World Prediction ≠ observed fact
Self Prediction ≠ Policy decision
Intrinsic Signal ≠ reward/value
Drive State ≠ global motivation/value
Appraisal ≠ emotion/value/Affect
Affect ≠ emotion label/Drive/value
ValueProfile ≠ mandatory scalar/reward/Policy decision
SalienceProfile ≠ AttentionAllocation
Retrieval ≠ Memory Replay ≠ Training Replay
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
Observation ≠ Interpretation ≠ ResearchClaim
ClaimScope ≠ universal scope
association ≠ causation
engineering verified ≠ functionally useful
functional similarity ≠ phenomenological equivalence
```

---

# Что всё ещё НЕ frozen

До concrete version specification не считать canonical implementation choice:

- `Protocol`/ABC/dataclass/TypedDict/Pydantic/TensorDict;
- exact field names/enum strings/status codes;
- exact tensor dimensions/dtypes;
- package/file layout;
- concrete model/backend/algorithm;
- storage/index/checkpoint format;
- optimizer/training library;
- pytest/Hypothesis/Import Linter/CI tooling;
- benchmark/statistical package/threshold;
- report/preregistration/tracker framework;
- deployment/provider/hardware topology.

---

# Breaking semantic change

После F31 изменение semantic owner/lifecycle/source/visibility/causal ordering требует:

```text
design review
→ new ADR
→ canonical owner update
→ contract update
→ freeze baseline revision
→ VerificationObligation update
→ version plan/code
```

Version specification не может молча переопределить F31.

---

# Иерархия после DU-31

```text
accepted ADR + canonical design
→ Semantic Freeze Baseline F31
→ semantic-frozen contracts
→ version specification / exact contracts
→ implementation sequence
→ implementation
→ engineering/research evidence
```
