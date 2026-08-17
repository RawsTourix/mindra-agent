# Candidate / exact internal contracts MINDRA

## Назначение

Этот каталог хранит machine-facing semantic contracts уже принятых subsystem/data/training/reproducibility/evaluation boundaries.

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
- [`experience-data-replay.md`](experience-data-replay.md) — ExperienceEvent/Journal, causal revisions, annotations, projections, DatasetManifest, TrainingSample и Training Replay provenance после `DU-25`;
- [`training-lifecycle.md`](training-lifecycle.md) — TrainingPlan/Attempt, GradientFlowPolicy, CandidateRevisionBundle, LearningUpdateRecord и RevisionActivation semantics после `DU-26`;
- [`checkpoint-reproducibility-compute.md`](checkpoint-reproducibility-compute.md) — checkpoint scope/capture/artifacts, restore profiles, reproducibility claims и software/hardware/compute manifests после `DU-27`;
- [`mindra-eval.md`](mindra-eval.md) — EvaluationStudy/Suite/Condition/Run/Unit, controls, metrics, paired interventions, statistical plan, module gates и report lineage после `DU-28`.

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
Memory Replay ≠ Training Replay
Consolidation ≠ in-place rewrite ≠ Learning Update
CognitiveState ≠ Workspace
Executive Control ≠ Cognitive Scheduler ≠ Policy
Policy ≠ Planner
Plan ≠ ImaginedTrajectory
SelectedActionIntent ≠ AuthorizedAction ≠ Action Commit
Action Commit ≠ Dispatch ≠ Environment Transition
TraceEvent ≠ ExperienceEvent
Experience Journal ≠ Agent runtime state
Source Experience ≠ TrainingSample
Training Runtime ≠ cognitive module
Runtime State Update ≠ Learning Update
Training Objective ≠ Agent Goal ≠ ValueProfile
runtime dependency graph ≠ gradient graph
CandidateRevisionBundle ≠ Active AgentRevision
AgentSnapshot ≠ persistent Checkpoint
Checkpoint ≠ TrainingResumeCheckpoint ≠ ExperimentManifest
same seed ≠ same RNG state ≠ guaranteed same execution
semantic restore ≠ bitwise reproducibility
artifact identity ≠ physical path
ComputeManifest ≠ CognitiveResourceEnvelope
Evaluation Runtime ≠ Agent cognition
Task score ≠ module/causal/calibration evidence
EvaluationCondition ≠ architecture name only
nested episode ≠ independent training replicate
Policy pre-Gate quality ≠ post-Gate system quality
```

Для MINDRA-Eval дополнительно:

- evaluator-only Ground Truth не пересекает Agent Interaction Plane normal runtime способом;
- confirmatory study pin'ит primary hypotheses/contrasts/metrics/statistical plan до outcome evidence;
- experimental/statistical unit и replicate nesting explicit;
- stochastic aggregate claim требует uncertainty/distribution evidence;
- ablation не masquerade как matched semantic control;
- matched-compute/capacity claim сохраняет actual matched/unmatched factors;
- paired causal intervention требует verified compatible base state;
- invalid/censored/`execution_unknown` не превращаются молча в task failure;
- Policy, Action Gate и post-Gate system metrics separate;
- aggregate score derived и сохраняет source metric lineage;
- privileged oracle conditions маркируются отдельно;
- module gate имеет explicit negative criterion;
- actual compute/data/context/tuning differences входят в attribution;
- report traceable до raw runs/metrics/evidence.

---

# Текущий статус

После `DU-04 … DU-28` semantic requirements приняты, но **общий exact Python contract set намеренно не frozen**.

`mindra-eval.md` остаётся candidate до Engineering Testing/Research Claims/contract freeze integration.

До contract freeze нельзя считать каноническими:

- `Protocol`/ABC/dataclass/TensorDict/Pydantic;
- exact event/status enums;
- benchmark/evaluation framework;
- concrete MicroWorld evaluation tasks;
- metrics/statistics library;
- t-test/bootstrap/permutation/Bayesian implementation;
- exact seed count/alpha;
- Brier/NLL/ECE mandatory set;
- rliable;
- experiment tracker/dashboard;
- report/plot format;
- universal composite score;
- CI provider;
- storage/backend implementation.

---

# Иерархия

```text
accepted ADR + canonical design
→ candidate/exact contract
→ version specification
→ implementation sequence
→ implementation
```
