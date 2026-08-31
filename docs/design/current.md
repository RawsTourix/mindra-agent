# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какая implementation-работа разрешена следующей.

Operational workflow не хранится в истории чата. Его canonical entry points:

- [`../process/README.md`](../process/README.md) — durable handoff, роли, modes и acceptance lifecycle;
- [`../process/independent-audit.md`](../process/independent-audit.md) — independent implementation/correction audit;
- [`../process/codex-instruction-authoring.md`](../process/codex-instruction-authoring.md) — opening next step и authoring copy-ready Codex instructions.

---

# 1. Общий статус

```text
Semantic Freeze Baseline F31: accepted
Version Roadmap DU-32: accepted
Current milestone: v0.1 Core Kernel
v0.1 exact design: accepted
v0.1 implementation-sequence: accepted
V0.1-IS-01 … V0.1-IS-12: accepted
V0.1-IS-13: CLOSED — exact design clarification required
V0.1-IS-14+: CLOSED
```

`V0.1-IS-12 — Reference synthetic modules` принят после independent audit implementation commit:

```text
39f48959e385d22a74c18dc4e793464e6fe4af2b
feat(reference): add synthetic reference modules
```

Final audit подтвердил:

- scope ровно `IS-12`: `mindra.reference.synthetic` + exports + focused tests;
- exact classes `SyntheticSourceModule`, `SyntheticDoubleModule`, `SyntheticTripleModule`, `SyntheticJoinModule`;
- exact ModuleId / ImplementationId / ImplementationRevision и four canonical int StateKeys;
- stateless deterministic `COGNITIVE_CYCLE` descriptors;
- `CURRENT_CYCLE`, required, `Available`-only dependency semantics;
- source constructor `value: int` с reject `bool`/non-int без artificial range limits;
- exact arithmetic `source`, `*2`, `*3`, `double + triple`;
- staged proposal/provenance identities зеркалят `ModuleComputeRequest.context` и own descriptor;
- `private_state_update=None` для всех reference modules;
- production `mindra.reference` не импортирует runtime/composition/entrypoints;
- existing Import Linter contracts остаются green;
- existing `ExecutionPlanCompiler` для всех 24 descriptor permutations строит exact waves `source -> {double,triple} -> join`;
- Composition Root/config/registry/schema builder/Scheduler/CommitCoordinator не изменялись.

Verification evidence:

```text
Targeted verification: PASS — 16 passed
FULL-C0 local: PASS — 297 passed
build: PASS
git diff --check: PASS
GitHub Actions run 33369411116
head 39f48959e385d22a74c18dc4e793464e6fe4af2b
Ubuntu Python 3.14: PASS
Windows Python 3.14: PASS
```

Final verdict:

```text
AUDIT-PASS
V0.1-IS-12: accepted
```

VerificationObligations на предусмотренном `IS-12` уровне:

- `V01-012` — closed at reference/runtime independence layer;
- `V01-013` — foundation.

`V01-013` полностью не закрывается до configured runnable reference profile/Composition Root из `IS-13`.

---

# 2. Канонические входные точки

Semantic baseline:

- [`contract-adr-consistency-freeze.md`](contract-adr-consistency-freeze.md);
- [`contracts/semantic-freeze-manifest.md`](contracts/semantic-freeze-manifest.md);
- [`ADR-0031`](decisions/ADR-0031-semantic-contract-consistency-freeze.md).

Operational workflow:

- [`../process/README.md`](../process/README.md);
- [`../process/independent-audit.md`](../process/independent-audit.md);
- [`../process/codex-instruction-authoring.md`](../process/codex-instruction-authoring.md).

Version-specific source of truth:

- [`../versions/v0.1/README.md`](../versions/v0.1/README.md) — accepted exact design;
- [`../versions/v0.1/implementation-sequence.md`](../versions/v0.1/implementation-sequence.md) — accepted dependency-ordered implementation plan;
- [`../versions/v0.1/is-06-contract-shape.md`](../versions/v0.1/is-06-contract-shape.md) — accepted clarification `IS-06`;
- [`../versions/v0.1/is-07-execution-plan-shape.md`](../versions/v0.1/is-07-execution-plan-shape.md) — accepted clarification `IS-07`;
- [`../versions/v0.1/is-07-controlled-construction-correction.md`](../versions/v0.1/is-07-controlled-construction-correction.md) — accepted correction `IS-07`;
- [`../versions/v0.1/is-08-private-state-store-shape.md`](../versions/v0.1/is-08-private-state-store-shape.md) — accepted clarification `IS-08`;
- [`../versions/v0.1/is-09-commit-coordinator-shape.md`](../versions/v0.1/is-09-commit-coordinator-shape.md) — accepted exact clarification `IS-09`;
- [`../versions/v0.1/is-09-active-boundary-consistency-correction.md`](../versions/v0.1/is-09-active-boundary-consistency-correction.md) — accepted correction clarification `IS-09`;
- [`../versions/v0.1/is-10-evidence-plane-shape.md`](../versions/v0.1/is-10-evidence-plane-shape.md) — accepted exact clarification `IS-10`;
- [`../versions/v0.1/is-11-wave-scheduler-shape.md`](../versions/v0.1/is-11-wave-scheduler-shape.md) — accepted exact clarification `IS-11`;
- [`../versions/v0.1/is-11-attempt-result-binding-correction.md`](../versions/v0.1/is-11-attempt-result-binding-correction.md) — accepted correction clarification `IS-11`;
- [`../versions/v0.1/is-12-reference-synthetic-shape.md`](../versions/v0.1/is-12-reference-synthetic-shape.md) — accepted exact clarification `IS-12`;
- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md) — canonical operational prompt template, revision `CSPT-02`.

---

# 3. Implementation checkpoints

| Step | Статус | Implementation/correction |
|---|---|---|
| `IS-01` | accepted | bootstrap + correction `584db766...` |
| `IS-02` | accepted | `e457ada1...` |
| `IS-03` | accepted | `a5c9f314...` |
| `IS-04` | accepted | `86d38ff6...` + `afc1937b...` |
| `IS-05` | accepted | `df602abb...` |
| `IS-06` | accepted | `633babaf...` |
| `IS-07` | accepted | `c8852930...` + `5b60d001...` |
| `IS-08` | accepted | `92a2dd75...` |
| `IS-09` | accepted | `c11d79e7...` + clarification/correction `a4e99807...` / `978897ad...` |
| `IS-10` | accepted | `510aad6f...` |
| `IS-11` | accepted | `e8aa2fa...` + correction `a0cc9dea...` |
| `IS-12` | accepted | `39f48959...` |
| `IS-13` | CLOSED — clarification required | implementation not started |

---

# 4. Transition gate перед `V0.1-IS-13`

Следующий по accepted implementation sequence:

```text
V0.1-IS-13 — Configuration & Composition Root
```

Accepted v0.1 design уже фиксирует крупные semantics:

- profile schema `mindra.kernel-profile/v1` и stdlib TOML;
- immutable explicit `ImplementationRegistry` без import-time registration;
- `CompositionRoot` как единственную production assembly boundary;
- construction modules/schema/initial state/private store/plan/evidence/scheduler/runtime facade;
- deterministic composition fingerprint;
- schema-complete initial state с explicit availability и `StateRevision = 0`;
- `KernelRuntime.run_cycle()` facade;
- reference profile/config и `composition_resolved` / `plan_compiled` evidence.

Но implementation sequence/version design ещё оставляют choices, которые нельзя отдавать Codex на самостоятельный архитектурный выбор. Перед coding требуется exact clarification минимум для:

- physical package/file split `mindra.composition` и runtime facade ownership;
- exact `KernelProfile` / module profile value-object shapes и parser API;
- exact allowed/required TOML keys и strict unknown-key behavior на каждом уровне;
- exact `ImplementationRegistry` / factory descriptor API, duplicate handling и immutable settings boundary;
- exact reference factory settings validation (`SyntheticSourceModule.value` и no-settings modules);
- schema construction source-of-truth из active descriptors/reference keys;
- initial `CognitiveState` entries/availability/provenance/logical-time identities;
- initial private-state construction for stateless/current supported modules;
- exact composition revision / AgentRevisionId / lineage / branch / run-session identity ownership;
- canonical normalized composition fingerprint representation;
- exact `KernelRuntime` constructor/public surface and `run_cycle()` lifecycle/ID ownership;
- exact `composition_resolved` / `plan_compiled` event timing and payload construction;
- exact `configs/v0.1/reference.toml` contents;
- failure/cleanup ordering so partial composition objects are not externally published.

Текущий mode:

```text
MODE-DESIGN — V0.1-IS-13 exact clarification
```

До принятия clarification:

```text
V0.1-IS-13: CLOSED
V0.1-IS-14+: CLOSED
```

---

# 5. Разрешённая текущая работа

Разрешена только documentation/design работа внутри accepted v0.1 semantics:

```text
V0.1-IS-13 exact clarification
```

Нельзя:

- начинать production Configuration/Composition Root implementation до accepted clarification;
- реализовывать Intervention (`IS-14`);
- менять F31/ADR/version semantics;
- открывать `IS-14`.

---

# 6. Operational mode

Canonical template:

- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md), revision `CSPT-02`.

`CSPT-02` остаётся применимым, но `MODE-INSTRUCTION` для `IS-13` разрешён только после accepted exact clarification и явного открытия step в этом файле.
