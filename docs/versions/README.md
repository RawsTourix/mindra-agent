# Software versions MINDRA

## Назначение

Этот каталог содержит version-specific design после завершения общего архитектурного цикла `DU-00 … DU-32`.

Canonical roadmap:

- [`../design/version-roadmap.md`](../design/version-roadmap.md)

Semantic baseline:

- [`../design/contract-adr-consistency-freeze.md`](../design/contract-adr-consistency-freeze.md)
- [`../design/contracts/semantic-freeze-manifest.md`](../design/contracts/semantic-freeze-manifest.md)

Canonical operational prompt для Codex:

- [`codex-step-prompt-template.md`](codex-step-prompt-template.md)

---

# Правило

Roadmap не является прямым заданием на coding.

Для каждой версии сначала создаются и принимаются:

```text
docs/versions/vX.Y/README.md
docs/versions/vX.Y/implementation-sequence.md
```

Только после этого Codex может реализовывать version scope.

`README.md` версии определяет exact selected choices и acceptance criteria.

`implementation-sequence.md` разбивает уже принятый version design на небольшие dependency-ordered implementation steps.

Каждый coding task выполняет только один `IS` и перед переходом дальше проходит:

```text
implementation
→ targeted verification
→ полный уже существующий local regression gate
→ CI evidence/status, если применимо
→ отчёт Codex
→ ChatGPT audit
```

Для задания Codex используется [`codex-step-prompt-template.md`](codex-step-prompt-template.md). Обязательные новые требования к prompt нельзя хранить только в истории чата.

---

# Планируемые milestones

| Версия | Статус | Название |
|---|---|---|
| `v0.1` | implementation in progress — `IS-01` verification pending | Core Kernel |
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
- `V0.1-IS-01` реализован, но остаётся закрыть final verification evidence;
- `V0.1-IS-02` пока не открыт.

Статус конкретной работы всегда определяется [`../design/current.md`](../design/current.md).

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

Для `v0.1` такой pass создан:

- [`../research/literature/v0.1-core-kernel-tooling-landscape-2026-08.md`](../research/literature/v0.1-core-kernel-tooling-landscape-2026-08.md).

При принятии нового version design обязательно проверяется актуальность [`codex-step-prompt-template.md`](codex-step-prompt-template.md). Если версия вводит новые verification profiles, CI semantics, обязательные source-of-truth paths или reporting evidence, шаблон обновляется тем же документационным патчем.

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
- быть совместимым с canonical [`codex-step-prompt-template.md`](codex-step-prompt-template.md).

При каждом изменении implementation sequence и перед открытием следующего `IS` после ChatGPT audit проверяется актуальность prompt template. Если фактические verification/CI/reporting требования изменились, шаблон актуализируется до выдачи следующего coding task.

---

# Verification workflow

Targeted verification конкретного step не заменяет regression verification уже построенной части версии.

Для `v0.1` после `IS-01` каждый последующий Codex task перед отчётом обязан выполнить:

1. targeted verification своего step;
2. полный `FULL-C0` regression gate;
3. CI status/evidence для remote commit, если доступно.

Если изменения ещё не находятся на remote commit или среда Codex не имеет доступа к Actions, статус фиксируется как `PENDING`/`NOT AVAILABLE`, а не `PASS`.

---

# Текущий следующий шаг

До закрытия `IS-01` разрешена только его verification-follow-up работа.

```text
V0.1-IS-01 — final verification evidence
```

После подтверждения local/CI evidence выполняется ChatGPT acceptance audit. Только после него может быть открыт:

```text
V0.1-IS-02 — Identity / revision / logical time
```

Нельзя перескакивать к последующим implementation steps или начинать `v0.2` до полного acceptance gate `v0.1`.
