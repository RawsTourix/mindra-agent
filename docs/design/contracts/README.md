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
- [`world-model.md`](world-model.md) — WorldBelief, assimilation, WorldPrediction, imagination, uncertainty, prediction error и snapshot semantics после `DU-12`.

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
- World Model contract не превращает prediction/imagination в observed fact, не делает backend latent universal state и не смешивает prediction error с reward/value.

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

После `DU-04` … `DU-12` приняты semantic requirements для state/scheduler/observability и subsystem boundaries Environment, Perception, Goals, Cortex, Memory и World Model.

Для World Model теперь зафиксированы:

- `World Belief` отдельно от текущего percept и hidden world state;
- assimilation actual evidence отдельно от action-conditioned prediction;
- one-step prediction и multi-step imagination;
- structured + optional feature/latent prediction surface;
- prediction/imagination provenance;
- cautious uncertainty semantics;
- prediction error отдельно от reward/intrinsic utility;
- Memory/Cortex integration только через explicit boundaries;
- model/belief revisioning;
- snapshot/restore/counterfactual obligations;
- `NoWorldModel`/Dummy/Control distinctions.

Однако **общий exact Python contract set пока намеренно не зафиксирован**.

`environment.md` остаётся candidate до Action/Data/Checkpoint/Evaluation DU.

`perception.md` остаётся candidate до Self/Data/Training/Evaluation DU.

`goals.md` остаётся candidate до Self/Drives/Valuation/Executive/Policy/Data/Evaluation DU.

`cortex.md` остаётся candidate до Workspace/Executive/Policy/Training/Checkpoint/Evaluation DU.

`memory.md` остаётся candidate до Salience/Consolidation/Workspace/Data/Checkpoint/Evaluation DU.

`world-model.md` остаётся candidate, поскольку `DU-13/14`, `DU-18`, `DU-22/23`, `DU-25` … `DU-28` ещё уточнят Self/Intrinsic/Valuation/Planning/Data/Training/Checkpoint/Evaluation integration.

До contract freeze запрещено считать конкретные `Protocol`, ABC, TensorDict, dataclass/Pydantic schemas, RSSM/Dreamer/Transformer/TD-MPC, TorchRL, uncertainty estimator или rollout framework каноническими.
