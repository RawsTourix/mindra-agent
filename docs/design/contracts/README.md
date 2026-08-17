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
- [`self-model.md`](self-model.md) — AgentCapabilityManifest, SelfEvidence, SelfBelief, competence profile, SelfPrediction/Resolution и calibration/staleness semantics после `DU-13`;
- [`intrinsic-signals.md`](intrinsic-signals.md) — typed Signal Providers, IntrinsicSignal/Bundle, novelty/rarity/information/competence/normalization semantics после `DU-14`;
- [`drives.md`](drives.md) — DriveSystem/DriveDescriptor/DriveStateSet, typed homeostatic/adaptive dynamics, coupling, Goal Proposal и snapshot semantics после `DU-15`;
- [`appraisal.md`](appraisal.md) — AppraisalTarget/Context/Profile/Record, multidimensional event assessment, reappraisal и intervention semantics после `DU-16`;
- [`affect.md`](affect.md) — typed persistent AffectStateSet, source-mode/temporal dynamics, branch-local imagined Affect и falsification/control semantics после `DU-17`.

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
- Self Model contract не превращает Cortex verbal confidence в canonical self-knowledge, не смешивает capability availability с competence и не даёт Self Model decision authority Executive Control/Policy;
- Intrinsic Signals contract не превращает typed measures в universal reward/value, не смешивает signal families и требует provider/source/reference/normalization provenance;
- Drive contract не превращает persistent state в global motivation/reward, не требует set-point для каждого drive и не даёт Drive direct Goal/Policy authority;
- Appraisal contract не превращает event assessment в emotion label/global utility, не смешивает controllability с coping potential и не хранит hidden persistent Affect;
- Affect contract не превращает history-dependent state в emotion label/global valence/reward, не дублирует Drive state и не обновляет real Affect из imagination по умолчанию.

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

После `DU-04` … `DU-17` приняты semantic requirements для state/scheduler/observability и subsystem boundaries Environment, Perception, Goals, Cortex, Memory, World Model, Self Model, Intrinsic Signals, Drives, Appraisal и Affect.

Для Affect теперь зафиксированы:

- единый `Affect System` ownership boundary;
- typed `AffectChannelDescriptor`/`AffectChannelState`/`AffectStateSet`;
- explicit `AffectUpdateContext`/`AffectUpdateProposal`;
- source modes actual/predicted/imagined/retrospective/intervened/replayed;
- temporal lineage и previous committed Affect feedback;
- branch-local `SimulatedAffectState` для imagination;
- optional versioned `AffectView`;
- explicit baseline/persistence/reset semantics;
- intervention/failure/degradation/snapshot requirements;
- `NoAffect`, ResetEveryEvent, shuffled-history и matched recurrent controls;
- отсутствие обязательного emotion label/valence-arousal/PAD/global utility output.

Однако **общий exact Python contract set пока намеренно не зафиксирован**.

`environment.md` остаётся candidate до Action/Data/Checkpoint/Evaluation DU.

`perception.md` остаётся candidate до Data/Training/Evaluation DU.

`goals.md` остаётся candidate до Valuation/Executive/Policy/Data/Evaluation integration freeze.

`cortex.md` остаётся candidate до Workspace/Executive/Policy/Training/Checkpoint/Evaluation DU.

`memory.md` остаётся candidate до Salience/Consolidation/Workspace/Data/Checkpoint/Evaluation DU.

`world-model.md` остаётся candidate до Valuation/Executive/Policy/Data/Training/Checkpoint/Evaluation DU.

`self-model.md` остаётся candidate до Valuation/Executive/Policy/Data/Training/Checkpoint/Evaluation DU.

`intrinsic-signals.md` остаётся candidate до Valuation/Salience/Policy/Data/Training/Checkpoint/Evaluation DU.

`drives.md` остаётся candidate до Valuation/Salience/Executive/Policy/Data/Training/Checkpoint/Evaluation integration freeze.

`appraisal.md` остаётся candidate до Valuation/Salience/Executive/Policy/Data/Training/Checkpoint/Evaluation integration freeze.

`affect.md` остаётся candidate, поскольку `DU-18…23`, `DU-25` … `DU-28` ещё уточнят Valuation/Salience/Memory Regulation/Workspace/Executive/Policy/data/training/checkpoint/evaluation integration.

До contract freeze запрещено считать конкретные `Protocol`, ABC, TensorDict, dataclass/Pydantic schemas, emotion taxonomy, mandatory valence/arousal/PAD geometry, decay equation, recurrent architecture или global affect scalar каноническими.
