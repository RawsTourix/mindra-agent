# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какой следующий Design Update допустим.

---

# 1. Общий статус

**`DU-01 … DU-29` завершены и приняты. Реализация ещё не начата.**

Приняты:

- foundation/system boundaries `DU-01 … DU-06`;
- cognitive/runtime boundaries `DU-07 … DU-24`;
- Experience / Data / Replay `DU-25`;
- Training Lifecycle `DU-26`;
- Checkpoint / Reproducibility / Compute `DU-27`;
- MINDRA-Eval `DU-28`;
- Engineering Testing `DU-29`;
- 29 accepted ADR;
- candidate semantic contracts для boundaries `DU-07 … DU-29`.

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
```

---

# 3. DU-29

Canonical design:

- [`engineering-testing.md`](engineering-testing.md)

Candidate contract:

- [`contracts/engineering-testing.md`](contracts/engineering-testing.md)

Accepted decision:

- [`ADR-0029`](decisions/ADR-0029-layered-invariant-driven-engineering-verification.md)

Research/tool pass:

- [`../research/literature/DU-29-engineering-testing-landscape-2026-08.md`](../research/literature/DU-29-engineering-testing-landscape-2026-08.md)

Главные результаты:

```text
Engineering Testing
≠
MINDRA-Eval

line coverage
≠
architectural invariant coverage

seed
≠
deterministic equality contract
```

- каждый accepted engineering invariant получает `VerificationObligation` либо explicit статус manual/non-machine-checkable/research-only;
- `VerificationMatrix` связывает ADR/design/contracts с test specs, CI tiers и evidence;
- static architecture, unit, contract/conformance, property, state-machine, integration, fault/recovery, persistence/migration/backend/system tests являются разными слоями;
- заменяемые implementations проходят shared conformance suites по заявленным capabilities;
- ownership/write authority, scheduler/waves/atomic commit/staleness проверяются явно;
- privileged Ground Truth/test oracle leakage должен обнаруживаться автоматически;
- `Action Commit → dispatch → execution_unknown → reconciliation` получает отдельную state-machine/fault suite;
- Training Runtime проверяется на candidate/activation/rollback и отсутствие hidden live mutation;
- checkpoint tests следуют заявленному scope/restore/reproducibility profile, а не universal bitwise oracle;
- golden tests ограничены stable deterministic contract surfaces;
- flaky rerun/quarantine не считается satisfied VerificationObligation;
- `No*`/Dummy/control implementations имеют declared conformance profiles;
- CI tiers различают static/CPU/stateful-fault/accelerator/remote-provider classes без выбора конкретного CI provider;
- skipped/not-run/quarantined не превращаются в pass;
- concrete pytest/Hypothesis/Import Linter/coverage/mutation/CI implementations не выбраны.

---

# 4. Следующий допустимый Design Update

```text
DU-30 — Research Claims / Limitations
```

Цель `DU-30` — определить **какие утверждения MINDRA вообще имеет право делать о своих результатах и архитектуре**, как strength of claim связывается с evidence `DU-28`, и как документируются отрицательные результаты, ограничения, неизвестность и антропоморфные пределы интерпретации.

Обязательные вопросы:

```text
observation vs interpretation vs claim
engineering evidence vs research evidence
claim strength / evidence ladder
causal claim requirements
generalization scope
reproducibility vs replicability
negative / null results
failed module gates
limitations registry
known unknowns
unsupported claims
anthropomorphic / consciousness claims
subjective experience claims
capability vs architecture attribution
Cortex/provider dependence
compute/data/tuning limitations
statistical uncertainty
post-hoc vs preregistered evidence
claim versioning / supersession
paper/report language discipline
```

Особенно нужно определить:

- наличие Drives/Appraisal/Affect/Self Model/Workspace не является evidence сознания или субъективных чувств;
- функциональное сходство с человеческим механизмом не доказывает феноменологическое равенство;
- strong causal wording требует соответствующего intervention/matched evidence;
- result scope не расширяется с одного checkpoint/task family на «AGI» автоматически;
- отрицательный module gate должен быть reportable и может инициировать ADR/design review;
- limitations должны быть versioned first-class artifacts, а не примечанием в конце статьи;
- конкретный paper/template/publication venue пока не выбирается.

После принятия `DU-30` допускается:

```text
DU-31 — Contract + ADR Consistency Freeze
```

---

# 5. Ещё не приняты

Пока отсутствуют accepted решения по:

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
