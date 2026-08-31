# Software versions MINDRA

## Назначение

Этот каталог содержит version-specific design после завершения общего архитектурного цикла `DU-00 … DU-32`.

Canonical roadmap:

- [`../design/version-roadmap.md`](../design/version-roadmap.md)

Semantic baseline:

- [`../design/contract-adr-consistency-freeze.md`](../design/contract-adr-consistency-freeze.md)
- [`../design/contracts/semantic-freeze-manifest.md`](../design/contracts/semantic-freeze-manifest.md)

Operational workflow:

- [`../process/README.md`](../process/README.md);
- [`../process/independent-audit.md`](../process/independent-audit.md);
- [`../process/codex-instruction-authoring.md`](../process/codex-instruction-authoring.md).

Canonical operational prompt для Codex:

- [`codex-step-prompt-template.md`](codex-step-prompt-template.md), current accepted revision определяется самим template и при необходимости `docs/design/current.md`.

---

# Правило разработки

Roadmap не является прямым заданием на coding.

Для каждой версии сначала принимаются:

```text
docs/versions/vX.Y/README.md
docs/versions/vX.Y/implementation-sequence.md
```

Каждый coding task выполняет только один `IS` и проходит:

```text
accepted previous step
→ opening/clarification следующего step
→ copy-ready Codex instruction
→ implementation
→ targeted verification
→ полный local regression gate
→ CI evidence/status
→ отчёт Codex
→ operator commit/push
→ independent ChatGPT audit
→ correction ИЛИ acceptance
→ только затем next step
```

Подробный lifecycle находится в [`../process/README.md`](../process/README.md).

Новые обязательные требования к Codex prompt нельзя хранить только в истории чата: canonical source — [`codex-step-prompt-template.md`](codex-step-prompt-template.md).

Новые обязательные ChatGPT-side правила audit/transition/instruction delivery нельзя хранить только в чате: canonical source — [`../process/`](../process/README.md).

---

# Software milestones

| Версия | Статус | Название |
|---|---|---|
| `v0.1` | accepted | Core Kernel |
| `v0.2` | design + implementation sequence accepted | MicroWorld Interaction |
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

Accepted historical baseline:

- [`v0.1/README.md`](v0.1/README.md) — accepted exact design `Core Kernel`;
- [`v0.1/implementation-sequence.md`](v0.1/implementation-sequence.md) — historical accepted sequence `V0.1-IS-01 … V0.1-IS-16`;
- [`v0.1/verification-matrix.md`](v0.1/verification-matrix.md) — final verification evidence.

Accepted current version design:

- [`v0.2/README.md`](v0.2/README.md) — accepted exact design `MicroWorld Interaction`;
- [`v0.2/implementation-sequence.md`](v0.2/implementation-sequence.md) — accepted dependency-ordered implementation sequence.

Accepted step-specific clarification/correction docs и live version status перечисляются в [`../design/current.md`](../design/current.md), который является единственным live status.

Этот version index намеренно не дублирует номер текущего `IS`.

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

При принятии нового version design обязательно проверяется актуальность [`codex-step-prompt-template.md`](codex-step-prompt-template.md) и operational workflow в [`../process/`](../process/README.md).

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
- быть совместимым с canonical prompt template;
- поддерживать independent audit/correction lifecycle.

Перед открытием следующего `IS` после ChatGPT audit:

1. проверить prerequisites;
2. проверить необходимость step-specific clarification;
3. проверить актуальность prompt template;
4. только затем обновить `docs/design/current.md` и открыть следующий step;
5. выдать prompt по [`../process/codex-instruction-authoring.md`](../process/codex-instruction-authoring.md).

---

# Verification workflow

Каждая active version определяет свой полный local regression profile поверх обязательной engineering verification foundation.

Для исторической `v0.1` после `IS-01` использовался `FULL-C0`: targeted verification каждого step, полный local regression gate, CI status/evidence и independent audit после push.

Если изменения ещё не находятся на remote commit или среда Codex не имеет доступа к Actions, статус фиксируется как `PENDING`/`NOT AVAILABLE`, а не `PASS`.

Предложение названия коммита не разрешает Codex самостоятельно commit/push.

После push результат обязательно проходит [`../process/independent-audit.md`](../process/independent-audit.md).

---

# Current implementation status

Единственный source of truth:

- [`../design/current.md`](../design/current.md).

Именно он определяет:

- какие version designs/sequences приняты;
- какие steps accepted;
- какой step `OPEN`;
- какие последующие steps `CLOSED`;
- какие step-specific clarifications обязательны;
- какие implementation/correction commits считаются принятыми.

Нельзя копировать live step number в этот README или другие index docs: такая информация быстро становится stale.
