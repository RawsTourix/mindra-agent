# Verification matrix v0.1

## Назначение

Матрица связывает обязательства `V01-001 … V01-014` с canonical source и
воспроизводимым engineering evidence для candidate `V0.1-IS-16`.

Допустимые статусы: `PASS`, `PENDING-CI`, `FAIL`, `BLOCKED`. Локальный `PASS` не
заменяет post-push evidence там, где обязательна проверка exact candidate на обеих
declared CI OS.

| ID | Invariant | Canonical source | Enforcement | Evidence refs | Environment | Status |
| -- | --------- | ---------------- | ----------- | ------------- | ----------- | ------ |
| `V01-001` | Все sibling attempts wave читают один pinned public base; private snapshots pinned до compute; sibling proposals не видны друг другу. | `docs/versions/v0.1/README.md`, §45; `docs/versions/v0.1/is-16-acceptance-hardening-shape.md`, §4 | property + integration | `tests/property/test_same_base_wave.py`<br>`tests/integration/test_scheduler_wave_semantics.py` | local locked Python 3.14 | `PASS` |
| `V01-002` | Public/private effects wave публикуются all-or-nothing; failed wave не публикует partial subset и не откатывает earlier successful waves. | `docs/versions/v0.1/README.md`, §45; `docs/versions/v0.1/is-16-acceptance-hardening-shape.md`, §4 | property + integration + state machine | `tests/property/test_atomic_commit.py`<br>`tests/integration/test_wave_failure_atomicity.py`<br>`tests/state_machine/test_commit_state_machine.py` | local locked Python 3.14 | `PASS` |
| `V01-003` | Module не коммитит чужой `StatePath`; producer/attempt authority fail closed. | `docs/versions/v0.1/README.md`, §45; `docs/versions/v0.1/is-16-acceptance-hardening-shape.md`, §4 | contract + integration | `tests/contract/test_commit_authority.py`<br>`tests/integration/test_wave_failure_atomicity.py` | local locked Python 3.14 | `PASS` |
| `V01-004` | `StateProjection` разрешает только declared reads. | `docs/versions/v0.1/README.md`, §45; `docs/versions/v0.1/is-16-acceptance-hardening-shape.md`, §4 | contract | `tests/contract/test_state_projection.py`<br>`tests/contract/test_module_protocol.py` | local locked Python 3.14 | `PASS` |
| `V01-005` | Structural `missing` не смешивается с `Unknown`, `Stale` или `Unavailable` existing field. | `docs/versions/v0.1/README.md`, §§12, 45; `docs/versions/v0.1/is-16-acceptance-hardening-shape.md`, §4 | unit + contract | `tests/unit/test_availability.py`<br>`tests/unit/test_cognitive_state.py`<br>`tests/contract/test_state_projection.py` | local locked Python 3.14 | `PASS` |
| `V01-006` | Proposal с недопустимой base revision отклоняется без silent rebase. | `docs/versions/v0.1/README.md`, §45; `docs/versions/v0.1/is-16-acceptance-hardening-shape.md`, §4 | property + state machine | `tests/property/test_stale_proposals.py`<br>`tests/state_machine/test_commit_state_machine.py` | local locked Python 3.14 | `PASS` |
| `V01-007` | Cycle, ambiguous writer и missing required current producer fail до normal execution; valid DAG имеет deterministic waves. | `docs/versions/v0.1/README.md`, §§24, 45; `docs/versions/v0.1/is-16-acceptance-hardening-shape.md`, §4 | contract + property + integration | `tests/contract/test_plan_validation.py`<br>`tests/property/test_dag_decomposition.py`<br>`tests/integration/test_reference_plan.py` | local locked Python 3.14 | `PASS` |
| `V01-008` | Own private state обновляется только successful atomic commit и изолирован от peer modules. | `docs/versions/v0.1/README.md`, §45; `docs/versions/v0.1/is-16-acceptance-hardening-shape.md`, §4 | unit + contract + property + integration | `tests/unit/test_private_state_store.py`<br>`tests/contract/test_private_state_isolation.py`<br>`tests/property/test_atomic_commit.py`<br>`tests/integration/test_wave_failure_atomicity.py` | local locked Python 3.14 | `PASS` |
| `V01-009` | O0 trace восстанавливает plan/wave/attempt/commit lineage, включая failures и interventions. | `docs/versions/v0.1/README.md`, §45; `docs/versions/v0.1/is-16-acceptance-hardening-shape.md`, §4 | unit + contract + integration + property | `tests/unit/test_evidence_records.py`<br>`tests/contract/test_evidence_isolation.py`<br>`tests/integration/test_scheduler_trace.py`<br>`tests/integration/test_intervention_lineage.py`<br>`tests/property/test_reference_determinism.py` | local locked Python 3.14 | `PASS` |
| `V01-010` | Trace/profiler/config metadata не попадает в module projection без explicit state contract. | `docs/versions/v0.1/README.md`, §45; `docs/versions/v0.1/is-16-acceptance-hardening-shape.md`, §4 | contract + architecture | `tests/contract/test_evidence_isolation.py`<br>`tests/contract/test_state_projection.py`<br>`tests/architecture/test_composition_boundary.py` | local locked Python 3.14 | `PASS` |
| `V01-011` | Controlled override создаёт explicit intervention provenance и отдельную revision, не маскируясь под natural output. | `docs/versions/v0.1/README.md`, §45; `docs/versions/v0.1/is-16-acceptance-hardening-shape.md`, §4 | contract + integration + state machine | `tests/contract/test_intervention_gateway.py`<br>`tests/integration/test_intervention_lineage.py`<br>`tests/state_machine/test_intervention_commit_sequence.py` | local locked Python 3.14 | `PASS` |
| `V01-012` | Import graph соблюдает accepted layers/independence; Service Locator и future responsibility packages отсутствуют. | `docs/design/dependency-rules.md`; `docs/versions/v0.1/README.md`, §45; `docs/versions/v0.1/is-16-acceptance-hardening-shape.md`, §§4, 6 | architecture + Import Linter | `tests/architecture/test_package_layers.py`<br>`tests/architecture/test_reference_independence.py`<br>`tests/architecture/test_composition_boundary.py`<br>`tests/architecture/test_v0_1_acceptance_scope.py`<br>`uv run --locked lint-imports` | local locked Python 3.14 | `PASS` |
| `V01-013` | Reference profile повторяет semantic final state, plan/waves и normalized logical trace; public CLI остаётся exact и deterministic. | `docs/versions/v0.1/README.md`, §45; `docs/versions/v0.1/is-15-cli-smoke-shape.md`; `docs/versions/v0.1/is-16-acceptance-hardening-shape.md`, §4 | contract + integration + property + CLI | `tests/contract/test_reference_modules.py`<br>`tests/integration/test_reference_plan.py`<br>`tests/integration/test_composition_root.py`<br>`tests/integration/test_kernel_runtime_reference.py`<br>`tests/integration/test_reference_profile.py`<br>`tests/integration/test_cli.py`<br>`tests/property/test_reference_determinism.py`<br>`uv run --locked mindra validate-profile --profile configs/v0.1/reference.toml`<br>`uv run --locked mindra kernel-smoke --profile configs/v0.1/reference.toml` | local locked Python 3.14 | `PASS` |
| `V01-014` | Clean locked sync/build/install воспроизводимы на declared Windows/Linux C0; wheel не имеет third-party runtime requirements. | `docs/versions/v0.1/README.md`, §§45–47; `docs/versions/v0.1/is-16-acceptance-hardening-shape.md`, §§4, 7–10, 15 | architecture + build + clean wheel smoke + cross-OS CI | `uv sync --locked`<br>`uv build`<br>`tests/architecture/test_v0_1_acceptance_scope.py`<br>`tools/verify_v0_1_artifact.py`<br>GitHub Actions `ubuntu-latest` / Python 3.14<br>GitHub Actions `windows-latest` / Python 3.14 | clean wheel venv Python 3.14<br>GitHub Actions ubuntu-latest Python 3.14<br>GitHub Actions windows-latest Python 3.14 | `PENDING-CI` |

## Candidate execution evidence

```text
Base HEAD: 2f81d1af9443c8e8a1d2d666a84565d18ba912f4
Local FULL-C0: PASS
Canonical CLI: PASS
Clean wheel install: PASS
Runtime dependency audit: PASS
Language policy review: PASS
Future-responsibility scope audit: PASS
Post-push GitHub Actions: PENDING
```

Runtime dependency claim `third-party runtime dependencies = 0` поддержан одновременно
пустым `[project].dependencies`, production AST import audit, отсутствием `Requires-Dist`
в wheel `METADATA` и запуском обеих форм canonical CLI из fresh wheel environment без
установки dev group.

Локальный handoff не принимает milestone: `V01-014` остаётся `PENDING-CI`, пока
independent final audit не проверит exact post-push candidate на Ubuntu и Windows.
