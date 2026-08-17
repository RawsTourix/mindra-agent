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
- [`intrinsic-signals.md`](intrinsic-signals.md) — typed Signal Providers, IntrinsicSignal/Bundle, novelty/rarity/information/competence/normalization semantics после `DU-14`.

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
- Intrinsic Signals contract не превращает typed measures в universal reward/value, не смешивает signal families и требует provider/source/reference/normalization provenance.

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

После `DU-04` … `DU-14` приняты semantic requirements для state/scheduler/observability и subsystem boundaries Environment, Perception, Goals, Cortex, Memory, World Model, Self Model и Intrinsic Signals.

Для Intrinsic Signals теперь зафиксированы:

- multi-provider architecture;
- `IntrinsicSignalProviderDescriptor`;
- typed `IntrinsicSignal` и `IntrinsicSignalBundle`;
- prediction discrepancy отдельно от probabilistic surprisal;
- novelty отдельно от visitation rarity;
- information gain только при meaningful knowledge-update semantics;
- signed uncertainty/competence change;
- temporal/reference scope и baseline/history revisions;
- provider-specific normalization identity/revision;
- representation-drift compatibility metadata;
- actual/replayed/imagined/intervened provenance;
- stateful-provider snapshot obligations;
- `NoIntrinsicSignals`/Dummy/Constant/Random/Shuffled/Control distinctions.

Однако **общий exact Python contract set пока намеренно не зафиксирован**.

`environment.md` остаётся candidate до Action/Data/Checkpoint/Evaluation DU.

`perception.md` остаётся candidate до Data/Training/Evaluation DU.

`goals.md` остаётся candidate до Drives/Valuation/Executive/Policy/Data/Evaluation DU.

`cortex.md` остаётся candidate до Workspace/Executive/Policy/Training/Checkpoint/Evaluation DU.

`memory.md` остаётся candidate до Salience/Consolidation/Workspace/Data/Checkpoint/Evaluation DU.

`world-model.md` остаётся candidate до Intrinsic/Valuation/Executive/Policy/Data/Training/Checkpoint/Evaluation DU.

`self-model.md` остаётся candidate до Intrinsic/Valuation/Executive/Policy/Data/Training/Checkpoint/Evaluation DU.

`intrinsic-signals.md` остаётся candidate, поскольку `DU-15`, `DU-18/19`, `DU-22/23`, `DU-25` … `DU-28` ещё уточнят Drives/Valuation/Salience/regulation/policy/data/training/checkpoint/evaluation integration.

До contract freeze запрещено считать конкретные `Protocol`, ABC, TensorDict, dataclass/Pydantic schemas, RND/ICM/VIME/RIDE/NGU/Plan2Explore, count/density model, normalization formula, common scalarization или intrinsic-reward training adapter каноническими.
