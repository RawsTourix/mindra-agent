# Exact internal contracts MINDRA

## Назначение

Этот каталог предназначен для точных machine-facing контрактов между подсистемами MINDRA.

Контракт создаётся **после** semantic design соответствующей области и не должен преждевременно определять архитектуру только потому, что конкретный Python API удобен для реализации.

---

# Что относится к exact internal contracts

В будущем здесь могут появиться спецификации уровня:

- `CognitiveState` schema;
- `ModuleProtocol`;
- `ModuleDescriptor`;
- observability event/trace schema;
- module research probe contract;
- intervention request/result contract;
- Cortex backend contract;
- Environment API;
- checkpoint format;
- experiment record format;
- module state serialization;
- configuration schema.

Это предварительный список типов контрактов, а не утверждённый catalog.

---

# Текущие candidate contracts

- [`environment.md`](environment.md) — candidate semantic machine-facing contract, появившийся после `DU-07`. Он фиксирует классы agent-facing/research-facing Environment operations, snapshot/clone/fork/intervention/transition-evidence requirements, но **не** является frozen Python API.

Candidate contract может уточняться последующими DU до общего contract freeze.

---

# Правила

Exact contract должен фиксировать, где применимо:

- поля и типы;
- required/optional semantics;
- shape/dtype/device semantics для tensor data;
- ownership;
- declared reads/writes;
- freshness/availability requirements;
- lifecycle;
- private-state/snapshot obligations;
- observability/probe capabilities;
- intervention target/phase/provenance semantics;
- error/degradation behavior;
- versioning;
- serialization;
- backward/forward compatibility expectations;
- invariants, которые можно проверить автоматическими tests.

Contract не должен протаскивать private implementation detail одного backend во всю систему без design justification.

Research observability contract не должен автоматически давать runtime consumers доступ к private state.

Intervention contract не должен быть скрытым extension обычного logging callback.

Environment research capability не должна автоматически становиться agent-facing capability.

---

# Иерархия

```text
canonical semantic design
→ accepted ADR
→ candidate/exact internal contract
→ implementation
```

Exact contract уточняет форму принятой семантики, но не может сам молча изменить её смысл.

---

# Текущий статус

После `DU-04` … `DU-07` уже приняты semantic requirements для:

- versioned committed `CognitiveState`;
- state ownership/provenance/scopes;
- module descriptors и declared dependencies;
- DAG/wave scheduling;
- staged public/private effects;
- lifecycle/failure semantics;
- causal execution tracing;
- passive Evidence Plane;
- declared private-state research probes;
- explicit Intervention Gateway;
- intervention lineage/provenance;
- exact-vs-approximate counterfactual distinction;
- agent-visible vs research-only Environment boundaries;
- Environment snapshot/clone/fork/intervention semantics;
- procedural world identity/version/RNG provenance;
- External Task Feedback vs Objective Task Metric vs Internal Utility distinction.

Однако **общий exact Python contract set пока намеренно не зафиксирован**.

`environment.md` уже существует как candidate contract, потому что `DU-07` дал достаточно устойчивую семантику для описания required capabilities. Он остаётся candidate, поскольку `DU-08`, `DU-09`, `DU-24`, `DU-25`, `DU-27` и `DU-28` ещё могут уточнить exact observation/action/data/snapshot forms.

Будущие module-specific Design Updates (`DU-08` … `DU-24`) должны продолжать проверять semantic protocol реальными требованиями Cortex, Memory, World Model, Policy и других подсистем. В частности, только они покажут:

- какие public/private probes реально нужны;
- какие intervention targets являются осмысленными;
- какие данные слишком велики для общего trace contract;
- какие backend-specific research adapters потребуются;
- какие Environment observation/action fields действительно нужны downstream modules.

До contract freeze запрещено считать обсуждавшиеся `Protocol`, ABC, TensorDict `in_keys/out_keys`, dataclass schemas, OpenTelemetry span model, PyTorch hooks, pyvene API, Gymnasium `Env` или конкретный scheduler/intervention result type каноническими.

Exact contracts создаются тогда, когда соответствующая семантика достаточно устойчива и есть основания зафиксировать machine-facing форму.
