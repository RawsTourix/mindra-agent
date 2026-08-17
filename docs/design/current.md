# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какой следующий Design Update допустим.

---

# 1. Общий статус

**`DU-01 … DU-31` завершены и приняты. Реализация ещё не начата.**

Приняты:

- foundation/system boundaries `DU-01 … DU-06`;
- cognitive/runtime boundaries `DU-07 … DU-24`;
- Experience / Data / Replay `DU-25`;
- Training Lifecycle `DU-26`;
- Checkpoint / Reproducibility / Compute `DU-27`;
- MINDRA-Eval `DU-28`;
- Engineering Testing `DU-29`;
- Research Claims / Limitations `DU-30`;
- Contract + ADR Consistency Freeze `DU-31`;
- 31 accepted ADR;
- semantic contracts `DU-07 … DU-30` frozen по смыслу как baseline `F31`;
- exact Python/API representation contracts ещё не frozen.

Архитектурная линия имеет статус:

```text
ready for version planning
```

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
DU-29 — Engineering Testing
DU-30 — Research Claims / Limitations
DU-31 — Contract + ADR Consistency Freeze
```

---

# 3. DU-31

Canonical freeze design:

- [`contract-adr-consistency-freeze.md`](contract-adr-consistency-freeze.md)

Accepted decision:

- [`ADR-0031`](decisions/ADR-0031-semantic-contract-consistency-freeze.md)

Machine-facing freeze manifest:

- [`contracts/semantic-freeze-manifest.md`](contracts/semantic-freeze-manifest.md)

Freeze identity:

```text
Semantic Freeze Baseline F31
scope: DU-01 … DU-30
semantic boundary contracts: 24
status: ready_for_version_planning
```

Главные результаты audit:

```text
ADR completeness: PASS
canonical owner uniqueness: PASS
semantic contract coverage DU-07…30: PASS
ownership consistency: PASS
runtime/temporal consistency: PASS
source/provenance/visibility consistency: PASS
snapshot/checkpoint consistency: PASS
Evaluation/Verification/Claims separation: PASS
blocking architectural TODO: NONE FOUND
```

Explicit consistency resolutions:

```text
CR-01 Action lifecycle
CR-02 Memory admission ownership
CR-03 Replay taxonomy
CR-04 Consolidation vs Learning Update
CR-05 candidate/validated/activated Agent revision lifecycle
```

Они закрепляют уже принятые поздние ADR и не создают новый subsystem design.

---

# 4. Что semantic-frozen

Для roadmap заморожены:

- logical boundaries/ownership;
- source-of-truth responsibilities;
- proposal/validation/commit semantics;
- causal ordering;
- source/derived/provenance/visibility distinctions;
- availability meanings;
- Memory Core vs Regulation;
- Replay/Consolidation/Training distinctions;
- Scheduler/Executive/Policy distinctions;
- Planner/Policy/Action Boundary distinctions;
- candidate/validation/activation training lifecycle;
- snapshot/checkpoint/reproducibility distinctions;
- Evaluation/Verification/Claims separation;
- negative module gates и control requirements;
- breaking-change governance.

Version design не может менять эти semantics без нового ADR.

---

# 5. Что остаётся version/implementation choice

До `DU-32` и concrete version specification не выбраны:

- software version decomposition;
- Python package/file layout;
- exact Protocol/ABC/dataclass/Pydantic/TensorDict forms;
- exact field/status enum encoding;
- Cortex/model/backend;
- neural/RL/learning algorithms;
- concrete Memory/index/storage backend;
- checkpoint file/storage format;
- exact MicroWorld/task suite;
- budgets/horizons/defaults;
- benchmark/statistical/test/CI tooling;
- hardware/deployment topology.

Эти choices не требуют нового ADR, пока сохраняют baseline `F31`.

---

# 6. Следующий допустимый Design Update

```text
DU-32 — Version Roadmap
```

Цель `DU-32` — разбить semantic-frozen architecture `F31` на реалистичные dependency-complete software milestones.

Roadmap должен определить:

- последовательность concrete software versions;
- vertical acceptance slice каждой версии;
- какие frozen boundaries включаются/остаются `No*`/Dummy/control;
- concrete compute constraints первой домашней/Colab реализации;
- dependencies между versions;
- non-goals;
- evaluation/verification gates;
- для каждой версии будущий `versions/vX.Y/README.md` и `implementation-sequence.md`.

`DU-32` **не имеет права заново выбирать semantic ownership/causal boundaries** — только конкретизировать реализацию baseline F31.

После принятия `DU-32` можно начинать отдельное подробное проектирование первой software version и её implementation sequence перед заданиями Codex.

---

# 7. Ещё не приняты

Пока отсутствуют accepted решения по:

- Version Roadmap;
- concrete software version specifications;
- implementation sequences конкретных software versions.

---

# 8. Implementation status

```text
Исследовательская/production реализация: не начата
Semantic design freeze: F31 accepted
Дорожная карта версий: не спроектирована
Software version: отсутствует
Implementation HEAD: отсутствует
```

До `DU-32` и конкретного version/implementation sequence Codex не начинает production/research implementation.
