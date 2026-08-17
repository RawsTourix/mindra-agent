# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какой следующий Design Update допустим.

---

# 1. Общий статус

**`DU-01 … DU-28` завершены и приняты. Реализация ещё не начата.**

Приняты:

- foundation/system boundaries `DU-01 … DU-06`;
- cognitive/runtime boundaries `DU-07 … DU-24`;
- Experience / Data / Replay `DU-25`;
- Training Lifecycle `DU-26`;
- Checkpoint / Reproducibility / Compute `DU-27`;
- MINDRA-Eval `DU-28`;
- 28 accepted ADR;
- candidate semantic contracts для boundaries `DU-07 … DU-28`.

---

# 2. Завершённые Design Updates

```text
DU-00 — Documentation Foundation
DU-01 — System Context
DU-02 — Dependency & Composition Rules
DU-03 — Runtime / Temporal Model
DU-04 — CognitiveState Semantics
DU-05 — Module Protocol & Scheduling
DU-06 — Observability & Intervention
DU-07 — Environment / MicroWorld Contract
DU-08 — Perception / Canonical Representation
DU-09 — Goal System
DU-10 — Cortex Boundary
DU-11 — Memory Core
DU-12 — World Model
DU-13 — Self Model
DU-14 — Intrinsic Signals
DU-15 — Drives
DU-16 — Appraisal
DU-17 — Affect Dynamics
DU-18 — Valuation
DU-19 — Salience / Attention
DU-20 — Memory Regulation / Consolidation
DU-21 — Workspace
DU-22 — Metacognitive / Executive Control
DU-23 — Policy / Planner
DU-24 — Action Boundary / Gate / Executor
DU-25 — Experience / Data / Replay
DU-26 — Training Lifecycle
DU-27 — Checkpoint / Reproducibility / Compute
DU-28 — MINDRA-Eval
```

---

# 3. DU-28

Canonical design:

- [`mindra-eval.md`](mindra-eval.md)

Candidate contract:

- [`contracts/mindra-eval.md`](contracts/mindra-eval.md)

Accepted decision:

- [`ADR-0028`](decisions/ADR-0028-multi-layer-causal-evaluation-harness.md)

Research pass:

- [`../research/literature/DU-28-mindra-eval-landscape-2026-08.md`](../research/literature/DU-28-mindra-eval-landscape-2026-08.md)

Главные результаты:

```text
Task score
≠ module evidence
≠ causal evidence
≠ calibration evidence
≠ compute-efficiency evidence

Evaluation Runtime
≠ Agent cognition

Policy quality before Gate
≠ post-Gate system quality
```

- `EvaluationStudy → Suite → Condition → Run → Unit → Metric/Contrast → Report` является основной evaluation hierarchy;
- `EvaluationCondition` pin'ит Agent/checkpoint/world/Cortex/interventions/data/resources/software/hardware context;
- experimental/statistical unit и replicate axes объявляются явно;
- nested episodes одного checkpoint не считаются independent training replicates;
- stochastic aggregate claim требует distribution/interval uncertainty evidence;
- confirmatory study заранее фиксирует primary hypothesis/metric/contrast/statistical plan;
- `No*`/Dummy/random/shuffled и matched-capacity/compute controls first-class;
- paired counterfactual interventions используют только проверенный DU-27 causal base state;
- evaluator Ground Truth остаётся privileged и не попадает в Agent Interaction Plane;
- proper scoring/calibration diagnostics отделены от task accuracy;
- actual compute/data/context/tuning differences входят в attribution;
- Policy, Action Gate и post-Gate system outcome оцениваются отдельно;
- `Affect`, `Workspace`, `Planner`, `Executive Control` имеют explicit negative module gates;
- `execution_unknown`, censored и invalid conditions не превращаются молча в обычный failure;
- optional composite score не заменяет typed metric/causal evidence;
- strength of research claim bounded by evidence/design strength;
- concrete benchmark/statistics/plotting framework не выбран.

---

# 4. Следующий допустимый Design Update

```text
DU-29 — Engineering Testing
```

Цель `DU-29` — спроектировать **инженерную систему проверки реализации MINDRA**, отделённую от research evaluation.

Нужно определить, как автоматически проверять contracts/invariants/failure semantics на уровне modules, runtime, data, training, checkpoints и evaluation infrastructure.

Обязательные вопросы:

```text
unit tests vs contract tests vs research evaluation
architecture/dependency tests
schema/serialization tests
property/invariant tests
state ownership/read-write tests
scheduler/DAG/wave/atomic commit tests
logical-time and stale-state tests
snapshot/restore/checkpoint round-trip tests
RNG/determinism tests
Environment clone/restore/action idempotency tests
execution_unknown/reconciliation tests
failure injection / fault tolerance
Cortex backend contract tests
No*/Dummy/control conformance
representation revision compatibility
Memory provenance/index rebuild tests
training candidate/activation/rollback tests
data lineage / evaluator leakage tests
EvaluationCondition/metric/statistics manifest validation
migration/backward-compatibility tests
fuzz/property-based testing
resource/timeout/OOM behavior
CI test tiers
fast vs slow vs accelerator-required suites
golden tests and their update policy
flaky-test policy
coverage of architectural invariants
```

Особенно нужно определить:

- `Engineering Testing ≠ MINDRA-Eval`;
- research hypothesis не заменяет contract/invariant test;
- unit test не является evidence функциональной полезности модуля;
- каждый accepted invariant должен иметь, где возможно, machine-checkable enforcement/test;
- failure semantics должны тестироваться намеренно, а не только happy path;
- oracle leakage и illegal dependency должны обнаруживаться автоматически;
- checkpoints/data/manifests должны проверяться на corruption/staleness/incompatibility;
- конкретный testing framework/CI provider пока implementation choice.

После принятия `DU-29` допускается:

```text
DU-30 — Research Claims / Limitations
```

---

# 5. Ещё не приняты

Пока отсутствуют accepted решения по:

- Engineering Testing;
- Research Claims / Limitations;
- Contract + ADR Consistency Freeze;
- Version Roadmap;
- implementation sequences.

Также не выбраны concrete Python/framework/model/algorithm/storage/evaluation/testing implementations.

---

# 6. Implementation status

```text
Исследовательская/production реализация: не начата
Дорожная карта версий: не спроектирована
Software version: отсутствует
Implementation HEAD: отсутствует
```

Detailed design сам по себе не разрешает Codex начинать implementation до `DU-32` и соответствующего version/implementation sequence.
