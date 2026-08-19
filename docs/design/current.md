# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какая работа разрешена следующей.

---

# 1. Общий статус

Общий архитектурный цикл `DU-00 … DU-32` завершён и принят.

```text
Semantic Freeze Baseline F31: accepted
Version Roadmap DU-32: accepted
Current milestone: v0.1 Core Kernel
v0.1 exact design: accepted
v0.1 implementation-sequence: accepted
V0.1-IS-01: accepted
V0.1-IS-02: accepted
V0.1-IS-03: accepted
V0.1-IS-04: accepted
V0.1-IS-05: accepted
current implementation step: V0.1-IS-06 — OPEN
V0.1-IS-07+: CLOSED
```

Приняты 32 ADR и semantic contracts `DU-07 … DU-30`, frozen по смыслу как baseline `F31`.

---

# 2. Канонические входные точки

Semantic baseline:

- [`contract-adr-consistency-freeze.md`](contract-adr-consistency-freeze.md)
- [`contracts/semantic-freeze-manifest.md`](contracts/semantic-freeze-manifest.md)
- [`ADR-0031`](decisions/ADR-0031-semantic-contract-consistency-freeze.md)

Roadmap:

- [`version-roadmap.md`](version-roadmap.md)
- [`ADR-0032`](decisions/ADR-0032-vertical-capability-version-roadmap.md)
- [`../versions/README.md`](../versions/README.md)

Version-specific source of truth:

- [`../versions/v0.1/README.md`](../versions/v0.1/README.md) — accepted exact design;
- [`../versions/v0.1/implementation-sequence.md`](../versions/v0.1/implementation-sequence.md) — accepted dependency-ordered implementation plan;
- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md) — canonical operational prompt template, revision `CSPT-02`.

Текущий разрешённый implementation step всегда определяется только этим файлом.

---

# 3. Принятые implementation checkpoints

## `V0.1-IS-01 — Project bootstrap & verification shell`

Принят после implementation/correction audit, local `FULL-C0` и Ubuntu/Windows GitHub Actions.

Correction commit:

```text
584db766e190739e22c7616f1ea1e68428ecf86e
fix(ci): enable UTF-8 for Import Linter on Windows
```

`V01-012` и `V01-014` остаются закрытыми только на предусмотренном для `IS-01` уровне `foundation/partial`; окончательное закрытие `V01-014` выполняется в `IS-16`.

## `V0.1-IS-02 — Identity / revision / logical time`

```text
e457ada1aa8ded3ff70cd47b5328e2bbcc96f724
feat(core): add identity revision and logical time primitives
```

ChatGPT code/design audit, targeted verification и local `FULL-C0`: `PASS`. Post-push Ubuntu/Windows GitHub Actions подтверждены оператором проекта как успешные.

## `V0.1-IS-03 — Availability / provenance / error foundation`

```text
a5c9f314bb0e9960da0434c6fcfd3556e8e9b5f2
feat(contracts): add availability provenance and kernel errors
```

ChatGPT code/design audit, targeted verification и local `FULL-C0`: `PASS`. Post-push Ubuntu/Windows GitHub Actions подтверждены оператором проекта как успешные.

VerificationObligations:

- `V01-005` — `foundation/partial`;
- `V01-010` — `foundation/partial`.

## `V0.1-IS-04 — State schema primitives`

Implementation commit:

```text
86d38ff6232239df190d69db8b75352927ac8b1f
feat(contracts): add state schema primitives
```

Correction commit:

```text
afc1937b82f09a9b7a082c3f5cf8d38fa264a5ef
fix(contracts): validate enum payload snapshot safety
```

ChatGPT audit подтвердил schema semantics, structural missing, snapshot safety, `StateEntry`/`StateEnvelope` и `ReadSpec` foundation. Targeted verification и local `FULL-C0`: `PASS`; post-push Ubuntu/Windows CI подтверждён оператором проекта.

`V01-005` достиг предусмотренного для `IS-04` уровня `substantial`.

## `V0.1-IS-05 — CognitiveState & StateProjection`

Implementation commit:

```text
df602abbf57d898952590d7a2eb145fff52b5f00
feat(state): add cognitive state and declared-read projections
```

ChatGPT audit подтвердил:

```text
scope IS-05                               PASS
forbidden scope IS-06+                   PASS
CognitiveState immutability              PASS
ValueContract integration                PASS
copy-on-commit isolation                 PASS
declared-read enforcement                PASS
availability semantics                   PASS
CURRENT_CYCLE semantics                  PASS
ANY_COMMITTED semantics                  PASS
```

По отчёту Codex targeted verification и local `FULL-C0`: `PASS`, полный suite — `130 passed`, build wheel/sdist — `PASS`. Post-push Ubuntu/Windows GitHub Actions подтверждены оператором проекта как успешные.

VerificationObligations:

- `V01-004` — closed at projection layer;
- `V01-005` — closed;
- `V01-010` — partial.

`V0.1-IS-05` принят.

---

# 4. Разрешённая implementation работа

Единственный разрешённый следующий coding step:

```text
V0.1-IS-06 — Module contracts & proposals
```

Scope определяется accepted `implementation-sequence.md`.

Ключевой результат:

```text
CognitiveModule Protocol
ModuleDescriptor
ModuleExecutionContext
ModuleComputeRequest / ModuleComputeResult
StateWrite / StateUpdateProposal
PrivateStateContract / PrivateStateSnapshot / PrivateStateProposal
private-state descriptor
execution traits
COGNITIVE_CYCLE phase marker
```

`ModuleComputeRequest` должен содержать только `StateProjection`, собственный private snapshot/unavailable и `ModuleExecutionContext`. Выполнение modules, DAG compilation и commit proposals на этом шаге запрещены.

`V0.1-IS-07` и последующие шаги закрыты до implementation + verification + отдельного ChatGPT audit `IS-06`.

---

# 5. Operational prompt

Canonical template:

- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md), revision `CSPT-02`.

Перед открытием `IS-06` применимость `CSPT-02` проверена. Новых verification profiles, CI jobs, mandatory commands или reporting semantics не появилось, поэтому revision шаблона не изменяется.

`CSPT-02` требует targeted verification, полный local `FULL-C0`, truthful GitHub Actions status/evidence и предложение Conventional Commit message в конце отчёта.

---

# 6. Ограничения

- не переходить к `V0.1-IS-07` до final acceptance `IS-06`;
- не начинать `v0.2` до полного acceptance gate `v0.1`;
- implementation-level correction допустима только внутри accepted `v0.1` semantics;
- semantic blocker требует design review и нового ADR/freeze update;
- Codex не меняет самостоятельно accepted version design/F31 и не открывает следующий implementation step.
