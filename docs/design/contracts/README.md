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
- Perception/Canonical Percept contract;
- checkpoint format;
- experiment record format;
- module state serialization;
- configuration schema.

Это предварительный список типов контрактов, а не утверждённый catalog.

---

# Текущие candidate contracts

- [`environment.md`](environment.md) — candidate semantic machine-facing contract после `DU-07`: agent-facing/research-facing Environment operations, snapshot/clone/fork/intervention и transition-evidence requirements;
- [`perception.md`](perception.md) — candidate semantic contract после `DU-08`: Perception input, `Canonical Percept`, Semantic Core, Feature Views, representation identity/versioning и research capabilities.

Оба документа **не** являются frozen Python API и могут уточняться последующими DU до общего contract freeze.

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

Perception contract не должен превращать конкретный encoder/Cortex hidden state в универсальный canonical representation.

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

После `DU-04` … `DU-08` уже приняты semantic requirements для:

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
- External Task Feedback vs Objective Task Metric vs Internal Utility distinction;
- `Raw Observation` vs `Canonical Percept` boundary;
- hybrid Semantic Core + optional Feature Views;
- Perception provenance/missingness/entity ordering semantics;
- learned representation identity/version/drift;
- no-Cortex-compatible Perception boundary.

Однако **общий exact Python contract set пока намеренно не зафиксирован**.

`environment.md` остаётся candidate, поскольку `DU-09`, `DU-24`, `DU-25`, `DU-27` и `DU-28` ещё могут уточнить exact task/action/data/snapshot forms.

`perception.md` остаётся candidate, поскольку `DU-09` … `DU-13`, `DU-25` … `DU-28` могут уточнить exact Goal/Cortex/Memory/World Model representation потребности, persistence и evaluation contracts.

Будущие module-specific Design Updates должны продолжать проверять semantic protocol реальными требованиями. В частности, только они покажут:

- какие exact public/private probes реально нужны;
- какие intervention targets являются осмысленными;
- какие Feature Views действительно нужны downstream modules;
- где необходимы compatibility adapters между representation revisions;
- какие данные слишком велики для общего trace contract;
- какие backend-specific research adapters потребуются.

До contract freeze запрещено считать обсуждавшиеся `Protocol`, ABC, TensorDict `in_keys/out_keys`, dataclass schemas, OpenTelemetry span model, PyTorch hooks, pyvene API, Gymnasium `Env`, конкретный Perception encoder или scheduler/intervention result type каноническими.

Exact contracts создаются тогда, когда соответствующая семантика достаточно устойчива и есть основания зафиксировать machine-facing форму.
