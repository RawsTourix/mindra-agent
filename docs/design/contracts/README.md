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
- Cortex backend contract;
- Environment API;
- checkpoint format;
- experiment record format;
- module state serialization;
- configuration schema.

Это предварительный список типов контрактов, а не утверждённый catalog.

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
- error/degradation behavior;
- versioning;
- serialization;
- backward/forward compatibility expectations;
- invariants, которые можно проверить автоматическими tests.

Contract не должен протаскивать private implementation detail одного backend во всю систему без design justification.

---

# Иерархия

```text
canonical semantic design
→ accepted ADR
→ exact internal contract
→ implementation
```

Exact contract уточняет форму принятой семантики, но не может сам молча изменить её смысл.

---

# Текущий статус

После `DU-04` и `DU-05` уже приняты semantic requirements для:

- versioned committed `CognitiveState`;
- state ownership/provenance/scopes;
- module descriptors и declared dependencies;
- DAG/wave scheduling;
- staged public/private effects;
- lifecycle/failure semantics.

Однако **exact Python contracts пока намеренно не зафиксированы**.

Причина: будущие module-specific Design Updates (`DU-07` … `DU-24`) должны сначала проверить semantic protocol реальными требованиями Environment, Cortex, Memory, World Model, Policy и других подсистем. Это позволит не закрепить слишком ранний API, который придётся ломать после первого же содержательного модуля.

До contract freeze запрещено считать обсуждавшиеся `Protocol`, ABC, TensorDict `in_keys/out_keys`, dataclass schemas или конкретный scheduler result type каноническими.

Exact contracts создаются тогда, когда соответствующая семантика достаточно устойчива и есть основания зафиксировать machine-facing форму.
