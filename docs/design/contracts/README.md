# Exact internal contracts MINDRA

## Назначение

Этот каталог предназначен для точных machine-facing контрактов между подсистемами MINDRA.

Контракт создаётся **после** semantic design соответствующей области и не должен преждевременно определять архитектуру только потому, что конкретный Python API удобен для реализации.

---

# Текущие candidate contracts

- [`environment.md`](environment.md) — Environment interaction/research boundary после `DU-07`;
- [`perception.md`](perception.md) — `Canonical Percept`, Semantic Core и Feature Views после `DU-08`;
- [`goals.md`](goals.md) — Goal Proposal/Committed Goal/Goal Graph после `DU-09`;
- [`cortex.md`](cortex.md) — Cortex Gateway/capabilities/request/result после `DU-10`;
- [`memory.md`](memory.md) — MemoryWriteProposal, MemoryRecord, MemoryRepresentation, RetrievalIndex/Request/Result и snapshot semantics после `DU-11`;
- [`world-model.md`](world-model.md) — WorldBelief, assimilation, WorldPrediction, imagination, uncertainty, prediction error и snapshot semantics после `DU-12`;
- [`self-model.md`](self-model.md) — AgentCapabilityManifest, SelfEvidence, SelfBelief, competence profile, SelfPrediction/Resolution и calibration/staleness semantics после `DU-13`.

Эти документы **не являются frozen Python API** и могут уточняться последующими DU до общего contract freeze.

---

# Общие правила

Exact contract должен фиксировать, где применимо:

- поля и типы;
- required/optional semantics;
- shape/dtype/device semantics;
- ownership;
- declared reads/writes;
- freshness/availability;
- lifecycle;
- private-state/snapshot obligations;
- observability/intervention;
- error/degradation behavior;
- versioning;
- serialization;
- compatibility expectations;
- автоматически проверяемые invariants.

Contract не должен протаскивать private implementation detail одного backend во всю систему без design justification.

Дополнительные действующие ограничения:

- research observability не даёт runtime consumers private-state access;
- Environment Research Plane не становится agent-facing;
- Perception не превращает конкретный encoder/Cortex hidden state в universal representation;
- Goal contract не даёт proposal sources direct mutation authority Goal Graph;
- Cortex contract не фиксирует model/provider и не даёт Gateway ambient Agent-state access;
- Memory contract не превращает vector index/embedding в canonical memory identity, не даёт Cortex ambient retrieval и не смешивает Memory с training replay;
- World Model contract не превращает prediction/imagination в observed fact, не делает backend latent universal state и не смешивает prediction error с reward/value;
- Self Model contract не превращает Cortex verbal confidence в canonical self-knowledge, не смешивает capability availability с competence и не даёт Self Model decision authority Executive Control/Policy.

---

# Иерархия

```text
canonical semantic design
→ accepted ADR
→ candidate/exact internal contract
→ implementation
```

Exact contract уточняет форму принятой семантики, но не может молча изменить её смысл.

---

# Текущий статус

После `DU-04` … `DU-13` приняты semantic requirements для state/scheduler/observability и subsystem boundaries Environment, Perception, Goals, Cortex, Memory, World Model и Self Model.

Для Self Model теперь зафиксированы:

- versioned `Agent Capability Manifest`;
- capability facts отдельно от learned competence;
- causal `Self Evidence`;
- committed context-conditioned `Self Belief`;
- explicit `SelfPredictionRequest → SelfPrediction` boundary;
- probability target/horizon/context semantics;
- probability of success отдельно от estimate uncertainty/support;
- Prediction Resolution для calibration evidence;
- staleness/recalibration после behavior-relevant Agent revision;
- Cortex self-report только как optional derived evidence;
- Self Model отдельно от World Model/Valuation/Executive Control;
- snapshot/restore obligations;
- `NoSelfModel`/Dummy/Control distinctions.

Однако **общий exact Python contract set пока намеренно не зафиксирован**.

`environment.md` остаётся candidate до Action/Data/Checkpoint/Evaluation DU.

`perception.md` остаётся candidate до Data/Training/Evaluation DU.

`goals.md` остаётся candidate до Drives/Valuation/Executive/Policy/Data/Evaluation DU.

`cortex.md` остаётся candidate до Workspace/Executive/Policy/Training/Checkpoint/Evaluation DU.

`memory.md` остаётся candidate до Salience/Consolidation/Workspace/Data/Checkpoint/Evaluation DU.

`world-model.md` остаётся candidate до Intrinsic/Valuation/Executive/Policy/Data/Training/Checkpoint/Evaluation DU.

`self-model.md` остаётся candidate, поскольку `DU-14`, `DU-18`, `DU-22/23`, `DU-25` … `DU-28` ещё уточнят competence-progress, value/regulation, policy use, data/training/checkpoint/evaluation integration.

До contract freeze запрещено считать конкретные `Protocol`, ABC, TensorDict, dataclass/Pydantic schemas, concrete calibration/competence estimator, task taxonomy, Brier/NLL/ECE policy или Self Model training algorithm каноническими.
