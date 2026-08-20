# Software versions MINDRA

## Назначение

Этот каталог содержит version-specific design после завершения общего архитектурного цикла `DU-00 … DU-32`.

Canonical roadmap:

- [`../design/version-roadmap.md`](../design/version-roadmap.md)

Semantic baseline:

- [`../design/contract-adr-consistency-freeze.md`](../design/contract-adr-consistency-freeze.md)
- [`../design/contracts/semantic-freeze-manifest.md`](../design/contracts/semantic-freeze-manifest.md)

Canonical operational prompt для Codex:

- [`codex-step-prompt-template.md`](codex-step-prompt-template.md), revision `CSPT-02`.

---

# Правило разработки

Roadmap не является прямым заданием на coding.

Для каждой версии сначала принимаются:

```text
docs/versions/vX.Y/README.md
docs/versions/vX.Y/implementation-sequence.md
```

Каждый coding task выполняет только один `IS` и перед переходом дальше проходит:

```text
implementation
→ targeted verification
→ полный local regression gate
→ CI evidence/status, если применимо
→ отчёт Codex
→ ChatGPT audit
```

Новые обязательные требования к Codex prompt нельзя хранить только в истории чата: canonical source — [`codex-step-prompt-template.md`](codex-step-prompt-template.md).

---

# Планируемые milestones

| Версия | Статус | Название |
|---|---|---|
| `v0.1` | implementation in progress — `IS-01…IS-07` accepted, `IS-08` open | Core Kernel |
| `v0.2` | planned | MicroWorld Interaction |
| `v0.3` | planned | Cortex Gateway |
| `v0.4` | planned | Memory & Restore |
| `v0.5` | planned | World & Self |
| `v0.6` | planned | Intrinsic / Drives / Appraisal |
| `v0.7` | planned | Affect / Valuation / Salience |
| `v0.8` | planned | Memory Regulation / Workspace |
| `v0.9` | planned | Executive / Planner |
| `v0.10` | planned | Training & Revision Lifecycle |
| `v0.11` | planned | Research Harness |
| `v0.12` | planned | Integration Hardening |
| `v1.0` | planned | MINDRA Research Baseline |

Текущая версия:

- [`v0.1/README.md`](v0.1/README.md) — accepted exact design `Core Kernel`;
- [`v0.1/implementation-sequence.md`](v0.1/implementation-sequence.md) — accepted sequence `V0.1-IS-01 … V0.1-IS-16`;
- [`v0.1/is-06-contract-shape.md`](v0.1/is-06-contract-shape.md) — accepted clarification `IS-06`;
- [`v0.1/is-07-execution-plan-shape.md`](v0.1/is-07-execution-plan-shape.md) — accepted clarification `IS-07`;
- [`v0.1/is-07-controlled-construction-correction.md`](v0.1/is-07-controlled-construction-correction.md) — accepted correction clarification `IS-07`;
- [`v0.1/is-08-private-state-store-shape.md`](v0.1/is-08-private-state-store-shape.md) — accepted exact clarification текущего `IS-08`;
- `V0.1-IS-01 … V0.1-IS-07` — accepted;
- `V0.1-IS-08` — единственный открытый implementation step.

Фактический current step всегда определяется [`../design/current.md`](../design/current.md).

---

# Version design checklist

Каждый version README должен определить минимум:

- цель версии;
- входной baseline/предыдущую версию;
- exact scope F31 boundaries;
- selected Python/runtime/tooling choices;
- exact representation relevant contracts;
- concrete implementations/control profiles;
- configuration/defaults;
- state/checkpoint/migration impact;
- data/evidence impact;
- VerificationObligations;
- evaluation/acceptance metrics;
- compute profile;
- non-goals;
- known risks/deferred work.

Если для выбора требуется актуальный внешний landscape, перед принятием version design выполняется новый датированный research/tool pass.

При принятии нового version design обязательно проверяется актуальность [`codex-step-prompt-template.md`](codex-step-prompt-template.md).

---

# Implementation sequence checklist

Каждый implementation sequence должен:

- быть dependency-complete;
- разбивать работу на небольшие reviewable changes;
- указывать affected contracts/invariants;
- перечислять tests/verification каждого шага;
- не просить Codex самому выбрать архитектуру;
- не объединять refactor, new feature и experiment в один непрозрачный change;
- завершаться version acceptance audit;
- быть совместимым с canonical prompt template.

Перед открытием следующего `IS` после ChatGPT audit проверяется актуальность prompt template. Если verification/CI/reporting requirements изменились, шаблон актуализируется до выдачи coding task.

---

# Verification workflow

Для `v0.1` после `IS-01` каждый Codex task перед отчётом обязан выполнить:

1. targeted verification своего step;
2. полный `FULL-C0` regression gate;
3. CI status/evidence для remote commit, если доступно;
4. предложить краткое название коммита в стиле Conventional Commits.

Если изменения ещё не находятся на remote commit или среда Codex не имеет доступа к Actions, статус фиксируется как `PENDING`/`NOT AVAILABLE`, а не `PASS`.

Предложение названия коммита не разрешает Codex самостоятельно commit/push.

---

# Принятые implementation checkpoints

| Step | Основной результат |
|---|---|
| `IS-01` | bootstrap/tooling + Windows UTF-8 correction |
| `IS-02` | identity/revisions/logical time |
| `IS-03` | availability/provenance/errors |
| `IS-04` | schema primitives + Enum snapshot-safety correction |
| `IS-05` | CognitiveState/StateProjection |
| `IS-06` | module contracts/staged proposals |
| `IS-07` | deterministic ExecutionPlanCompiler + controlled-construction correction |

`IS-07` commits:

```text
c88529300ab926b052e0b40089539735d64ac2e7
feat(runtime): add deterministic execution plan compiler

5b60d001f2d730c3fdc921244bc68b122f784a16
fix(runtime): restrict execution plan construction
```

`V01-007 — DAG validity`: closed.

---

# Текущий следующий шаг

```text
V0.1-IS-08 — PrivateStateStore
```

Перед открытием `IS-08` принят exact clarification [`v0.1/is-08-private-state-store-shape.md`](v0.1/is-08-private-state-store-shape.md).

Он фиксирует initialization/private ownership и transactional preparation semantics без изменения F31:

- stateful active module получает explicit initial private value и revision `0`;
- stateless module не имеет slot и получает `Unavailable`;
- private proposal validation/freezing отделены от mutation;
- internal prepared update имеет expected/next private revision;
- internal batch apply предварительно валидирует весь batch и не допускает partial private mutation;
- public+private atomic commit остаётся `IS-09`.

`V01-008` на `IS-08` достигает уровня `substantial/partial`.

Применимость `CSPT-02` проверена: новых CI jobs, verification profiles, mandatory commands или reporting semantics нет, revision шаблона не меняется.

`V0.1-IS-09` и последующие шаги остаются закрыты до implementation + verification + ChatGPT audit `IS-08`.

Нельзя начинать `v0.2` до полного acceptance gate `v0.1`.
