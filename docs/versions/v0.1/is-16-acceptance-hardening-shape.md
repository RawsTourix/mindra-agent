# V0.1-IS-16 — Version acceptance hardening exact shape

## Статус

**Статус:** `accepted exact clarification`  
**Область:** `V0.1-IS-16 — Version acceptance hardening`  
**Baseline:** F31 + accepted v0.1 design + accepted IS-01 … IS-15

Этот документ фиксирует последний implementation-level gate `v0.1`.

IS-16 не добавляет feature semantics. Его задача — превратить уже реализованный Core Kernel в проверяемый version candidate с явной матрицей VerificationObligations, clean artifact/install evidence и cross-platform CI evidence.

Codex не принимает milestone самостоятельно. После operator commit/push обязателен отдельный independent ChatGPT final acceptance audit.

---

# 1. Scope

Разрешены только:

- verification/hardening tests;
- verification tooling вне production package;
- CI hardening;
- `docs/versions/v0.1/verification-matrix.md`;
- минимальные correction changes, если hardening воспроизводимо выявляет настоящий defect внутри уже accepted semantics.

Ожидаемый normal IS-16 diff не требует изменений production `src/mindra/**`.

Новые cognitive/runtime features, refactor «на будущее» и v0.2 work запрещены.

---

# 2. Required repository additions

Создать минимум:

```text
docs/versions/v0.1/verification-matrix.md
tests/architecture/test_v0_1_acceptance_scope.py
tools/verify_v0_1_artifact.py
```

Обновить:

```text
.github/workflows/ci.yml
```

Тест/tool names являются canonical для этого step.

`tools/verify_v0_1_artifact.py` — engineering verification utility, не runtime API и не часть `mindra` package.

---

# 3. Verification matrix schema

`docs/versions/v0.1/verification-matrix.md` должен иметь один row для каждого:

```text
V01-001 … V01-014
```

Exact columns:

| ID | Invariant | Canonical source | Enforcement | Evidence refs | Environment | Status |
|---|---|---|---|---|---|---|

## 3.1. Status vocabulary

Допустимы только:

```text
PASS
PENDING-CI
FAIL
BLOCKED
```

Semantics:

- `PASS` — candidate имеет достаточное local/mechanical evidence, и для obligation не осталось отдельного post-push CI requirement;
- `PENDING-CI` — local/mechanical evidence green, но exact post-push cross-OS evidence текущего hardening commit ещё невозможно подтвердить;
- `FAIL` — обязательный check воспроизводимо failed;
- `BLOCKED` — evidence невозможно получить без design/semantic decision.

`N/A`, `SKIP`, `XFAIL`, `QUARANTINED` для `V01-001 … V01-014` запрещены.

При Codex handoff после local verification ожидается:

- `V01-001 … V01-013 = PASS`;
- `V01-014 = PENDING-CI`.

После operator push independent ChatGPT audit проверяет exact CI run candidate commit и только тогда может обновить `V01-014 -> PASS` и принять milestone.

Если любой `V01-001 … V01-013` не PASS — Codex не объявляет hardening complete.

---

# 4. Canonical obligation mapping

Матрица обязана содержать минимум следующие evidence refs.

## V01-001 — Same-base wave

Invariant:

```text
все sibling attempts wave читают один pinned public base;
private snapshots pinned до sibling compute;
sibling proposal не виден sibling attempt.
```

Evidence минимум:

```text
tests/property/test_same_base_wave.py
tests/integration/test_scheduler_wave_semantics.py
```

## V01-002 — Atomic wave commit

Invariant:

```text
wave public/private effects публикуются all-or-nothing;
failed current wave не публикует partial subset;
earlier successful waves не rollback.
```

Evidence минимум:

```text
tests/property/test_atomic_commit.py
tests/integration/test_wave_failure_atomicity.py
tests/state_machine/test_commit_state_machine.py
```

## V01-003 — Single writer authority

Invariant:

```text
module не коммитит чужой StatePath;
producer/attempt authority fail closed.
```

Evidence минимум:

```text
tests/contract/test_commit_authority.py
tests/integration/test_wave_failure_atomicity.py
```

## V01-004 — Declared reads only

Evidence минимум:

```text
tests/contract/test_state_projection.py
tests/contract/test_module_protocol.py
```

## V01-005 — Missing != availability

Evidence минимум:

```text
tests/unit/test_availability.py
tests/unit/test_cognitive_state.py
tests/contract/test_state_projection.py
```

## V01-006 — Stale proposal rejected

Evidence минимум:

```text
tests/property/test_stale_proposals.py
tests/state_machine/test_commit_state_machine.py
```

## V01-007 — DAG validity

Evidence минимум:

```text
tests/contract/test_plan_validation.py
tests/property/test_dag_decomposition.py
tests/integration/test_reference_plan.py
```

## V01-008 — Private-state transactionality

Evidence минимум:

```text
tests/unit/test_private_state_store.py
tests/contract/test_private_state_isolation.py
tests/property/test_atomic_commit.py
tests/integration/test_wave_failure_atomicity.py
```

## V01-009 — Evidence reconstructability

Evidence минимум:

```text
tests/unit/test_evidence_records.py
tests/contract/test_evidence_isolation.py
tests/integration/test_scheduler_trace.py
tests/integration/test_intervention_lineage.py
tests/property/test_reference_determinism.py
```

## V01-010 — Observability isolation

Evidence минимум:

```text
tests/contract/test_evidence_isolation.py
tests/contract/test_state_projection.py
tests/architecture/test_composition_boundary.py
```

## V01-011 — Intervention provenance

Evidence минимум:

```text
tests/contract/test_intervention_gateway.py
tests/integration/test_intervention_lineage.py
tests/state_machine/test_intervention_commit_sequence.py
```

## V01-012 — Dependency architecture

Evidence минимум:

```text
tests/architecture/test_package_layers.py
tests/architecture/test_reference_independence.py
tests/architecture/test_composition_boundary.py
uv run --locked lint-imports
```

## V01-013 — Deterministic reference profile

Evidence минимум:

```text
tests/contract/test_reference_modules.py
tests/integration/test_reference_plan.py
tests/integration/test_composition_root.py
tests/integration/test_kernel_runtime_reference.py
tests/integration/test_reference_profile.py
tests/integration/test_cli.py
tests/property/test_reference_determinism.py
mindra validate-profile --profile configs/v0.1/reference.toml
mindra kernel-smoke --profile configs/v0.1/reference.toml
```

## V01-014 — Build/install reproducibility

Evidence минимум:

```text
uv sync --locked
uv build
tests/architecture/test_v0_1_acceptance_scope.py
tools/verify_v0_1_artifact.py
GitHub Actions FULL-C0 ubuntu-latest / Python 3.14
GitHub Actions FULL-C0 windows-latest / Python 3.14
```

До exact post-push CI текущего IS-16 candidate:

```text
Status = PENDING-CI
```

---

# 5. Matrix evidence format

`Canonical source` содержит design/ADR/version refs, а не commit SHA как semantic source.

`Evidence refs` содержит concrete repository paths/commands.

`Environment` использует concise vocabulary:

```text
local locked Python 3.14
clean wheel venv Python 3.14
GitHub Actions ubuntu-latest Python 3.14
GitHub Actions windows-latest Python 3.14
```

Не вставлять unstable timestamps, local absolute paths или machine-specific temp paths.

В отдельном section `Candidate execution evidence` записать:

```text
Base HEAD: <starting IS-16 HEAD>
Local FULL-C0: PASS/FAIL
Canonical CLI: PASS/FAIL
Clean wheel install: PASS/FAIL
Runtime dependency audit: PASS/FAIL
Language policy review: PASS/FAIL
Future-responsibility scope audit: PASS/FAIL
Post-push GitHub Actions: PENDING
```

Codex не invent'ит future run ID.

Independent final audit после push может заменить `Post-push GitHub Actions: PENDING` на exact run/head/jobs evidence и обновить V01-014.

---

# 6. Acceptance-scope architecture test

Создать:

```text
tests/architecture/test_v0_1_acceptance_scope.py
```

Он должен machine-check минимум:

## 6.1. Runtime dependencies source declaration

Через stdlib `tomllib` проверить:

```text
pyproject.toml [project].dependencies == []
```

Dependency groups/build-system requirements не являются runtime dependencies.

## 6.2. Production import dependency audit

AST-scan всех:

```text
src/mindra/**/*.py
```

Каждый external import root должен быть:

- `mindra`;
- stdlib module из `sys.stdlib_module_names`;
- `__future__`.

Любой third-party production import fail.

Не whitelist конкретный third-party package.

## 6.3. v0.1 production responsibility surface

Top-level production package surface внутри `src/mindra` должен оставаться только foundation layers:

```text
contracts
runtime
reference
composition
entrypoints
__init__.py
__main__.py
```

Не должны появиться production packages/modules будущих cognitive responsibilities, например:

```text
environment
perception
goals
cortex
memory
world_model
self_model
intrinsic
drives
appraisal
affect
valuation
salience
memory_regulation
workspace
executive
policy
action
experience
training
checkpoint
eval
```

Future-facing primitive identity/contracts уже accepted v0.1 и сами по себе не являются forbidden responsibility implementation.

## 6.4. CLI surface regression

Public CLI остаётся только accepted IS-15 commands.

Не добавлять hidden acceptance command в production CLI.

---

# 7. Clean artifact verifier

Создать cross-platform stdlib-first engineering tool:

```text
tools/verify_v0_1_artifact.py
```

Это не package API.

Exact responsibility:

1. найти built wheel exact version `mindra_agent-0.1.0-py3-none-any.whl` в `dist/`;
2. открыть wheel как ZIP;
3. найти единственный `*.dist-info/METADATA`;
4. проверить:
   - `Name: mindra-agent`;
   - `Version: 0.1.0`;
   - отсутствуют строки `Requires-Dist:`;
5. создать fresh `TemporaryDirectory`;
6. создать отдельный venv Python 3.14 через current `uv`;
7. установить только built wheel через `uv pip install --python <fresh-python> <wheel>`;
8. не install dev dependency group;
9. запустить из fresh venv:
   - `python -m mindra validate-profile --profile <absolute canonical profile>`;
   - `python -m mindra kernel-smoke --profile <absolute canonical profile>`;
   - installed console script `mindra validate-profile ...`;
   - installed console script `mindra kernel-smoke ...`;
10. exact exit/stdout/stderr должны совпасть accepted IS-15 outputs;
11. fresh environment после wheel install не должен требовать third-party runtime packages;
12. temp environment автоматически удалить.

Cross-platform paths:

- Windows venv Python/console location вычислять platform-aware;
- POSIX location вычислять platform-aware;
- не hardcode только `bin/` или только `Scripts/`.

Tool должен возвращать process exit `0` только при полном PASS.

Tool не должен:

- импортировать project source из checkout как substitute built wheel;
- добавлять checkout `src` в `PYTHONPATH`;
- устанавливать editable project;
- устанавливать dev dependencies в fresh artifact env;
- обращаться в сеть ради package dependencies.

`uv`/Python toolchain itself является engineering prerequisite, не runtime dependency package.

---

# 8. Clean build procedure

Перед final artifact build удалить stale `dist/` cross-platform через Python/stdlib, затем:

```text
uv build
```

Required artifacts:

```text
dist/mindra_agent-0.1.0.tar.gz
dist/mindra_agent-0.1.0-py3-none-any.whl
```

`uv build` должен успешно строить wheel из source distribution согласно existing backend semantics.

После build обязательно:

```text
uv run --locked python tools/verify_v0_1_artifact.py
```

Это является local clean artifact/install gate.

---

# 9. CI hardening

Обновить existing `.github/workflows/ci.yml` без создания второго workflow.

Оставить existing matrix:

```text
ubuntu-latest
windows-latest
Python 3.14
```

После full pytest добавить explicit canonical CLI smoke:

```text
uv run --locked mindra validate-profile --profile configs/v0.1/reference.toml
uv run --locked mindra kernel-smoke --profile configs/v0.1/reference.toml
```

Перед build удалить stale `dist/` portable stdlib command либо гарантировать clean checkout и explicit fresh artifact output. Предпочтительно portable cleanup.

После `uv build` добавить:

```text
uv run --locked python tools/verify_v0_1_artifact.py
```

Таким образом каждый declared OS job проверяет:

- FULL-C0;
- canonical installed-project CLI in locked checkout env;
- build sdist/wheel;
- wheel metadata runtime dependencies;
- clean fresh wheel installation;
- `python -m mindra` + installed console script из fresh wheel env.

Не добавлять release/upload/publish steps.

---

# 10. Runtime dependency acceptance

Required claim v0.1:

```text
third-party runtime dependencies = 0
```

Он считается mechanically supported только если одновременно:

1. `pyproject.toml [project].dependencies == []`;
2. production AST import audit не находит third-party imports;
3. built wheel METADATA не содержит `Requires-Dist`;
4. clean wheel smoke запускается в fresh env без installation dev group.

Dev/build dependencies не смешивать с runtime dependency claim.

---

# 11. Language policy audit

Canonical policy из `AGENTS.md`:

```text
документация и комментарии — на русском;
technical identifiers/API/package/class/function/type names — на английском.
```

Natural-language classification не является надёжным automatic static rule, поэтому enforcement class:

```text
manual review only
```

IS-16 manual scope:

- repository documentation changed in IS-16;
- comments/docstrings в `src/mindra/**/*.py`;
- comments/docstrings в new/modified IS-16 tests/tools.

English technical identifiers/terms внутри русской technical prose не являются violation.

Если найден очевидный existing policy defect, допустима только documentation/comment correction без semantic code change.

Не делать массовый stylistic rewrite документации.

---

# 12. Future responsibility audit

Проверить, что v0.1 не реализовала responsibilities roadmap `v0.2+`.

Machine-check foundation package surface через `test_v0_1_acceptance_scope.py`.

Manual review дополнительно подтверждает отсутствие production implementations:

- Environment transition/task loop;
- Perception/Goals/Cortex;
- Memory/World/Self;
- intrinsic/drives/appraisal/affect/valuation/salience;
- Workspace/Executive/Policy/Action;
- Experience/Data/Replay;
- Training lifecycle;
- Checkpoint/restore system;
- MINDRA-Eval.

Наличие design docs и future-facing typed primitives не считать implementation leakage.

---

# 13. Defect handling

Если hardening выявляет настоящий implementation defect:

1. воспроизвести targeted test/check;
2. определить accepted invariant;
3. если correction однозначно следует из accepted semantics — разрешён minimal fix + regression test;
4. повторить affected targeted checks;
5. затем повторить весь final gate.

Если fix требует:

- semantic/F31 change;
- new architecture decision;
- new feature/API;
- reinterpretation accepted ADR;

STOP и blocker report.

Не ослаблять checks/matrix ради PASS.

---

# 14. Final local gate

Exact order после всех changes:

```text
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked lint-imports
uv run --locked pytest
uv run --locked mindra validate-profile --profile configs/v0.1/reference.toml
uv run --locked mindra kernel-smoke --profile configs/v0.1/reference.toml
```

Затем удалить stale `dist/` portable Python stdlib способом и выполнить:

```text
uv build
uv run --locked python tools/verify_v0_1_artifact.py
git diff --check
```

Expected canonical CLI output:

```text
OK validate-profile profile=v0_1.reference modules=4 waves=3
OK kernel-smoke profile=v0_1.reference waves=3 revision=3 join=10
```

Все required tests must pass without skip/xfail/quarantine substitute.

---

# 15. Post-push CI gate

Codex не commit/push.

Поэтому его final report обязан честно указать:

```text
Post-push CI: PENDING
V01-014: PENDING-CI
v0.1 milestone acceptance: NOT YET
```

После operator push independent ChatGPT audit проверяет exact candidate SHA:

- one CI workflow run for exact SHA;
- Ubuntu job PASS;
- Windows job PASS;
- canonical CLI steps PASS;
- artifact verifier PASS;
- build PASS.

Только после этого `V01-014` может стать PASS.

---

# 16. Final milestone transition owner

Codex НЕ обновляет самостоятельно:

- `docs/design/current.md` на milestone accepted;
- version implementation/acceptance status;
- roadmap/opening v0.2;
- `verification-matrix.md` post-push CI refs, которых ещё не существует.

После independent final audit только ChatGPT может выполнить final documentation transition.

Final transition должен минимум:

1. обновить matrix exact post-push CI evidence;
2. перевести `V01-014 -> PASS`;
3. зафиксировать `V01-001 … V01-014 = PASS`;
4. отметить `V0.1-IS-16: accepted`;
5. отметить `v0.1 Core Kernel: implemented/accepted` согласно operational status language;
6. не начинать v0.2 implementation автоматически.

---

# 17. Forbidden scope

IS-16 запрещает:

- новые runtime/cognitive features;
- Environment/Cortex/Memory work;
- v0.2 design/implementation;
- stable SDK promises;
- plugin/release/publish infrastructure;
- package upload;
- telemetry/exporter;
- refactor «на будущее»;
- new runtime dependency;
- new semantic identities/contracts;
- changing F31/ADR/version semantics;
- automatic milestone acceptance by Codex.

---

# 18. Expected Codex handoff state

При чистом hardening без defects:

```text
production code changes: none
verification matrix: created
acceptance scope test: PASS
runtime dependency audit: PASS
FULL-C0: PASS
canonical CLI: PASS
clean wheel build/install: PASS
language policy review: PASS
future responsibility audit: PASS
V01-001 … V01-013: PASS
V01-014: PENDING-CI
Post-push CI: PENDING
```

Это означает:

```text
IS-16 locally complete; ready for operator push + independent final acceptance audit
```

но НЕ означает milestone acceptance.
