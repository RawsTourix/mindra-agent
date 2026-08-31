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
V0.1-IS-01 … V0.1-IS-14: accepted
V0.1-IS-15: CLOSED — exact design clarification required
V0.1-IS-16+: CLOSED
```

Последний accepted implementation step:

```text
V0.1-IS-14 — InterventionGateway
9b6ca91389dcd05653ef1d8e072fe75984090749
feat(runtime): add controlled state intervention gateway
```

Independent acceptance evidence:

```text
Targeted verification: PASS — 27 passed
FULL-C0 local: PASS — 350 passed
build: PASS
git diff --check: PASS
GitHub Actions run 33382166078
head 9b6ca91389dcd05653ef1d8e072fe75984090749
Ubuntu Python 3.14: PASS — 350 passed
Windows Python 3.14: PASS
AUDIT-PASS
```

Final audit подтвердил:

- immutable `StateInterventionWrite` / `StateInterventionSpec` / exact-path `InterventionPolicy`;
- default-disabled reference runtime и explicit allowlist для research/test composition;
- exact base binding по `StateRevision + LineageId + BranchId`;
- schema/policy/value validation до allocation intervention identities;
- exact allocation order `InterventionId -> LineageId -> BranchId`;
- one-shot multi-target public treatment публикуется одной новой `StateRevision` или не публикуется вовсе;
- natural base snapshot остаётся immutable;
- successful treatment получает новую treatment lineage/branch;
- semantic field owner не меняется;
- provenance использует `RuntimeBoundaryId("evaluation.intervention")` и explicit intervention/base refs;
- O0 evidence exact order `intervention_applied -> state_revision_committed`;
- evidence failure не заменяет `KernelRuntime.state`;
- `KernelRuntime.apply_intervention()` доступен только между cognitive cycles;
- `_cycle_active` reset сохраняется через `try/finally` при scheduler infrastructure failure;
- subsequent normal cycle продолжает treatment lineage/branch;
- cognitive modules не получили intervention capability;
- private/module-result/backend intervention и full fork manager не реализованы.

VerificationObligations после IS-14:

- `V01-011` — closed;
- `V01-009` — intervention lineage extension substantial/closed for v0.1 intervention producer.

Overall `V01-009` final closure остаётся за deterministic end-to-end integration (`IS-15`) и version hardening (`IS-16`).

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
| `IS-15` | CLOSED — clarification required | implementation not started |

---

# 4. Transition gate перед `V0.1-IS-15`

Следующий по accepted implementation sequence:

```text
V0.1-IS-15 — CLI & deterministic end-to-end smoke
```

Accepted version design уже фиксирует high-level semantics:

- console script `mindra` уже объявлен через `mindra.entrypoints:main`;
- `python -m mindra` делегирует тому же `main()`;
- CLI использует stdlib `argparse`;
- требуются `kernel-smoke --profile ...` и `validate-profile --profile ...`;
- CLI делегирует accepted composition/runtime API и не собирает modules вручную;
- reference smoke обязан пройти graph `source -> {double,triple} -> join` и получить final join `10`;
- deterministic repeat должен сравнивать semantic plan, waves, state payload/revisions и logical O0 causal sequence, исключая physical timestamps;
- `V01-009` и `V01-013` должны закрываться end-to-end evidence этого шага.

Перед coding требуется exact clarification минимум для:

- physical CLI/entrypoint file split;
- exact argparse command/option surface и help behavior;
- exact stdout/stderr contract для success/failure;
- exit-code mapping для valid run, invalid profile/configuration и unexpected internal failure;
- exact `validate-profile` behavior: parse-only либо parse + registry/factory/composition validation;
- exact `kernel-smoke` assembly path и число cognitive cycles;
- deterministic `IdFactory` seed/namespace policy для smoke/repeat tests;
- exact concise success summary fields/order;
- exact equality normalization для causal evidence sequence;
- console-script и `python -m mindra` behavioral equivalence;
- profile path/IO error reporting без traceback как normal configuration failure;
- subprocess/in-process test matrix и installed-package/build smoke boundary;
- запрет на stable SDK/output promises сверх v0.1 smoke contract.

Текущий mode:

```text
MODE-DESIGN — V0.1-IS-15 exact clarification
```

До принятия clarification:

```text
V0.1-IS-15: CLOSED
V0.1-IS-16+: CLOSED
```

---

# 5. Разрешённая текущая работа

Разрешена только documentation/design работа внутри accepted v0.1 semantics:

```text
V0.1-IS-15 exact clarification
```

Нельзя:

- начинать CLI/smoke implementation до accepted clarification;
- выполнять version acceptance hardening (`IS-16`) заранее;
- менять F31/ADR/version semantics;
- открывать `IS-16`.

---

# 6. Operational mode

Canonical template:

- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md), revision `CSPT-02`.

`CSPT-02` остаётся применимым, но `MODE-INSTRUCTION` для `IS-15` разрешён только после accepted exact clarification и явного открытия step в этом файле.
