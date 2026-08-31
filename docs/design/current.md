# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какая implementation-работа разрешена следующей.

Operational workflow:

- [`../process/README.md`](../process/README.md);
- [`../process/independent-audit.md`](../process/independent-audit.md);
- [`../process/codex-instruction-authoring.md`](../process/codex-instruction-authoring.md).

---

# 1. Общий статус

```text
Semantic Freeze Baseline F31: accepted
Version Roadmap DU-32: accepted
Current milestone: v0.1 Core Kernel
v0.1 exact design: accepted
v0.1 implementation-sequence: accepted
V0.1-IS-01 … V0.1-IS-15: accepted
V0.1-IS-16: CLOSED — exact acceptance-hardening clarification required
```

Последний accepted implementation step:

```text
V0.1-IS-15 — CLI & deterministic end-to-end smoke
657b8140e82f73dae14878ada8d788f03069c5cc
feat(cli): add deterministic kernel smoke commands
```

Independent acceptance evidence:

```text
Targeted verification: PASS — 12 passed
FULL-C0 local: PASS — 362 passed
build: PASS
git diff --check: PASS
GitHub Actions run 33405884901
head 657b8140e82f73dae14878ada8d788f03069c5cc
Ubuntu Python 3.14: PASS — 362 passed
Windows Python 3.14: PASS
AUDIT-PASS
```

Final audit подтвердил:

- thin stdlib argparse entrypoint поверх public Composition Root/runtime API;
- exact commands `validate-profile --profile` и `kernel-smoke --profile`;
- identical console-script / `python -m mindra` behavior;
- fixed deterministic CLI identity seeds;
- full CompositionRoot validation без cognitive cycle для `validate-profile`;
- ровно один reference cognitive cycle для `kernel-smoke`;
- canonical output `waves=3 revision=3 join=10`;
- expected domain/usage/internal exit semantics без traceback;
- deterministic repeat по semantic plan, state payload/revisions и normalized O0 `(kind, logical_time, payload)` sequence;
- installed console script реально проверяется subprocess test внутри locked environment;
- entrypoints не собирают modules/runtime internals вручную и не создают Service Locator/global registry.

VerificationObligations после IS-15:

- `V01-009` — closed at deterministic v0.1 end-to-end O0 integration;
- `V01-013` — closed at deterministic runnable reference profile/CLI layer.

Final milestone acceptance и `V01-014` остаются за `IS-16` version acceptance hardening.

---

# 2. Canonical entry points

Semantic baseline:

- [`contract-adr-consistency-freeze.md`](contract-adr-consistency-freeze.md);
- [`contracts/semantic-freeze-manifest.md`](contracts/semantic-freeze-manifest.md);
- [`ADR-0031`](decisions/ADR-0031-semantic-contract-consistency-freeze.md).

Version-specific:

- [`../versions/v0.1/README.md`](../versions/v0.1/README.md);
- [`../versions/v0.1/implementation-sequence.md`](../versions/v0.1/implementation-sequence.md);
- [`../versions/v0.1/is-06-contract-shape.md`](../versions/v0.1/is-06-contract-shape.md);
- [`../versions/v0.1/is-07-execution-plan-shape.md`](../versions/v0.1/is-07-execution-plan-shape.md);
- [`../versions/v0.1/is-07-controlled-construction-correction.md`](../versions/v0.1/is-07-controlled-construction-correction.md);
- [`../versions/v0.1/is-08-private-state-store-shape.md`](../versions/v0.1/is-08-private-state-store-shape.md);
- [`../versions/v0.1/is-09-commit-coordinator-shape.md`](../versions/v0.1/is-09-commit-coordinator-shape.md);
- [`../versions/v0.1/is-09-active-boundary-consistency-correction.md`](../versions/v0.1/is-09-active-boundary-consistency-correction.md);
- [`../versions/v0.1/is-10-evidence-plane-shape.md`](../versions/v0.1/is-10-evidence-plane-shape.md);
- [`../versions/v0.1/is-11-wave-scheduler-shape.md`](../versions/v0.1/is-11-wave-scheduler-shape.md);
- [`../versions/v0.1/is-11-attempt-result-binding-correction.md`](../versions/v0.1/is-11-attempt-result-binding-correction.md);
- [`../versions/v0.1/is-12-reference-synthetic-shape.md`](../versions/v0.1/is-12-reference-synthetic-shape.md);
- [`../versions/v0.1/is-13-composition-root-shape.md`](../versions/v0.1/is-13-composition-root-shape.md);
- [`../versions/v0.1/is-14-intervention-gateway-shape.md`](../versions/v0.1/is-14-intervention-gateway-shape.md);
- [`../versions/v0.1/is-15-cli-smoke-shape.md`](../versions/v0.1/is-15-cli-smoke-shape.md);
- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md), revision `CSPT-02`.

---

# 3. Implementation checkpoints

| Step | Status | Implementation/correction |
|---|---|---|
| `IS-01` | accepted | bootstrap + correction `584db766...` |
| `IS-02` | accepted | `e457ada1...` |
| `IS-03` | accepted | `a5c9f314...` |
| `IS-04` | accepted | `86d38ff6...` + `afc1937b...` |
| `IS-05` | accepted | `df602abb...` |
| `IS-06` | accepted | `633babaf...` |
| `IS-07` | accepted | `c8852930...` + correction `5b60d001...` |
| `IS-08` | accepted | `92a2dd75...` |
| `IS-09` | accepted | `c11d79e7...` + correction `978897ad...` |
| `IS-10` | accepted | `510aad6f...` |
| `IS-11` | accepted | `e8aa2fa...` + correction `a0cc9dea...` |
| `IS-12` | accepted | `39f48959...` |
| `IS-13` | accepted | `b2be887c...` |
| `IS-14` | accepted | `9b6ca913...` |
| `IS-15` | accepted | `657b8140...` |
| `IS-16` | CLOSED — clarification required | acceptance hardening not started |

---

# 4. Transition gate перед `V0.1-IS-16`

Следующий и последний step accepted implementation sequence:

```text
V0.1-IS-16 — Version acceptance hardening
```

Это не feature step. Sequence уже требует:

- исправлять только реальные defects внутри accepted semantics;
- создать `docs/versions/v0.1/verification-matrix.md`;
- дать explicit evidence для `V01-001 … V01-014`;
- проверить Linux/Windows CI gates;
- проверить clean locked build/install reproducibility;
- подтвердить runtime dependencies = 0 third-party;
- проверить documentation/comment language policy;
- проверить отсутствие future cognitive responsibilities;
- выполнить final FULL-C0 + canonical CLI smoke;
- не переводить milestone в accepted самостоятельно.

Перед Codex task требуется exact acceptance-hardening clarification минимум для:

- exact schema/columns/status vocabulary `verification-matrix.md`;
- canonical mapping каждого `V01-001 … V01-014` к tests/specs/commands;
- format evidence refs для local verification и GitHub Actions;
- exact clean-build/install procedure и что считать `V01-014 PASS`;
- package/runtime dependency audit procedure;
- source documentation/comment language-policy audit scope;
- forbidden-future-responsibility audit scope;
- handling обнаруженного defect: correction vs documentation-only evidence;
- required final CLI/build commands и evidence capture;
- final Codex report shape перед independent ChatGPT milestone acceptance audit.

До принятия clarification:

```text
V0.1-IS-16: CLOSED
v0.1 milestone acceptance: NOT YET
```

---

# 5. Разрешённая текущая работа

Разрешена только documentation/design работа:

```text
V0.1-IS-16 exact acceptance-hardening clarification
```

Нельзя:

- добавлять новые features;
- делать refactor «на будущее»;
- начинать v0.2;
- менять F31/ADR/version semantics;
- объявлять v0.1 accepted до final independent audit.

---

# 6. Operational mode

```text
CSPT-02: applicable
MODE-DESIGN — V0.1-IS-16 exact acceptance-hardening clarification
```

После accepted clarification и явного открытия IS-16 будет разрешён только hardening/verification task.
