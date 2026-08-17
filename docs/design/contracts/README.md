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
- [`memory.md`](memory.md) — MemoryWriteProposal, MemoryRecord, MemoryRepresentation, RetrievalIndex/Request/Result после `DU-11`;
- [`world-model.md`](world-model.md) — WorldBelief, assimilation, prediction/imagination/uncertainty после `DU-12`;
- [`self-model.md`](self-model.md) — capabilities, competence, SelfPrediction/calibration после `DU-13`;
- [`intrinsic-signals.md`](intrinsic-signals.md) — typed Signal Providers/Bundle после `DU-14`;
- [`drives.md`](drives.md) — typed Drive System/dynamics после `DU-15`;
- [`appraisal.md`](appraisal.md) — multidimensional Appraisal после `DU-16`;
- [`affect.md`](affect.md) — persistent typed Affect dynamics после `DU-17`;
- [`valuation.md`](valuation.md) — ValuationTarget, ValueProfile, Risk/Constraint/Feasibility profiles, ComparisonPolicy/Result и optional scalarization после `DU-18`.

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

---

# Действующие subsystem safeguards

- Environment Research Plane не становится agent-facing;
- Perception не превращает concrete encoder/Cortex hidden state в universal representation;
- Goal proposal sources не получают direct mutation authority Goal Graph;
- Cortex не получает ambient Agent-state access;
- MemoryRecord не равен embedding/index и Memory не смешивается с training replay;
- World Model prediction/imagination не становится observed fact;
- Self Model не равен Cortex self-report и не получает decision authority;
- Intrinsic Signals не являются universal reward/value;
- Drive State не является global motivation/Utility;
- Appraisal не является emotion label/global utility/persistent Affect;
- Affect не является emotion label/global valence/reward/Drive state;
- Valuation не превращает `ValueProfile` в mandatory scalar/reward/Policy decision, не смешивает uncertainty с risk и не использует evaluator-only preference/metric natural способом.

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

После `DU-04` … `DU-18` приняты semantic requirements для state/scheduler/observability и subsystem boundaries Environment, Perception, Goals, Cortex, Memory, World Model, Self Model, Intrinsic Signals, Drives, Appraisal, Affect и Valuation.

Для Valuation зафиксированы:

- `ValuationTarget` для state/outcome/action/trajectory/counterfactual families;
- typed `ValueComponent`/`ValueProfile`;
- отдельные `FeasibilityProfile`, `ConstraintProfile`, `RiskProfile`;
- explicit `ComparisonPolicyDescriptor`/`ComparisonRequest`/`ComparisonResult`;
- optional `ScalarizedValue` только как derived result;
- immediate/prospective/trajectory semantics;
- actual/predicted/imagined/counterfactual provenance;
- intervention/control/snapshot/failure/versioning requirements;
- `NoValuation`, weighted scalar, random/shuffled/matched, lexicographic и oracle controls.

Однако **общий exact Python contract set пока намеренно не зафиксирован**.

`valuation.md` остаётся candidate, поскольку `DU-19`, `DU-22/23`, `DU-25` … `DU-28` ещё уточнят Salience/Executive/Policy/data/training/checkpoint/evaluation integration.

До contract freeze запрещено считать конкретные `Protocol`, ABC, TensorDict, dataclass/Pydantic schemas, weighted sum, Pareto/Tchebycheff/lexicographic ordering, CVaR, discount factor, critic architecture или RL reward mapping каноническими.
