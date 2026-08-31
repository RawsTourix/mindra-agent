# V0.1-IS-15 — CLI & deterministic end-to-end smoke exact shape

## Статус

**Статус:** `accepted exact clarification`  
**Область:** `V0.1-IS-15 — CLI & deterministic end-to-end smoke`  
**Baseline:** F31 + accepted v0.1 design + accepted IS-01 … IS-14

Этот документ фиксирует implementation-level choices финального feature step `v0.1`, которые нельзя оставлять Codex на самостоятельный выбор.

Он не меняет F31, Composition Root, scheduler, intervention или Evidence Plane semantics. CLI остаётся тонким user-facing adapter поверх уже принятых composition/runtime boundaries.

---

# 1. Scope

IS-15 должен доказать один runnable vertical foundation slice:

```text
CLI
 ↓
strict profile load
 ↓
build_reference_registry()
 ↓
CompositionRoot
 ↓
KernelRuntime
 ↓
one deterministic cognitive cycle
 ↓
reference final join = 10
```

Поддерживаются ровно две команды:

```text
mindra validate-profile --profile PATH
mindra kernel-smoke --profile PATH
```

и те же команды через:

```text
python -m mindra ...
```

CLI первой версии не является stable public SDK/output protocol `v1.0`.

---

# 2. Physical layout

Использовать:

```text
src/mindra/entrypoints/
├── __init__.py
└── cli.py

src/mindra/__main__.py
```

`mindra.entrypoints.__init__` re-export только public `main` из `cli.py`.

Existing `src/mindra/__main__.py` продолжает делегировать тому же `mindra.entrypoints.main` и не содержит отдельной CLI semantics.

Existing `pyproject.toml` console script:

```toml
[project.scripts]
mindra = "mindra.entrypoints:main"
```

уже является canonical console entrypoint. Не создавать второй script alias.

---

# 3. Dependency boundary

`mindra.entrypoints` может импортировать `mindra.composition`, `mindra.contracts` и необходимые public runtime identity factory forms.

CLI НЕ:

- собирает module instances вручную;
- создаёт `StateSchema`/Scheduler/CommitCoordinator напрямую;
- читает reference module internals;
- обходит `CompositionRoot`;
- получает private store/gateway/service locator;
- мутирует runtime state напрямую.

Canonical assembly для обеих команд:

```text
load_kernel_profile(path)
→ build_reference_registry()
→ CompositionRoot(...).build(profile)
```

---

# 4. Public main API

Exact user-entry API:

```text
main(argv: Sequence[str] | None = None) -> int
```

`argv=None` означает использовать обычный `sys.argv[1:]` через `argparse`.

Explicit `argv` существует только как обычная testable CLI adapter boundary и не является stable SDK promise.

`main()` не принимает streams/logger/runtime factory callbacks.

---

# 5. argparse surface

Использовать только stdlib `argparse`.

Top-level parser program name:

```text
mindra
```

Required subcommands:

```text
validate-profile
kernel-smoke
```

У обеих команд ровно один required option:

```text
--profile PATH
```

Не добавлять в v0.1:

- `--seed`;
- `--json`;
- `--verbose`/`--debug`;
- intervention flags;
- cycle-count option;
- plugin/config override flags.

Standard argparse `-h/--help` поддерживается автоматически.

Missing/unknown command/option и malformed CLI syntax используют standard argparse usage error semantics:

```text
exit code 2
usage/error text -> stderr
```

---

# 6. Deterministic CLI identity policy

CLI smoke/validation являются reproducible engineering boundary и используют `DeterministicIdFactory`, а не `Uuid7IdFactory`.

Canonical namespace:

```python
uuid.NAMESPACE_URL
```

Exact seeds:

```text
validate-profile: "mindra.v0_1.validate_profile"
kernel-smoke:     "mindra.v0_1.kernel_smoke"
```

Каждый invocation создаёт новый factory с counter `0`.

Seed не configurable через CLI.

Это не меняет normal library/runtime contract: callers CompositionRoot вне CLI по-прежнему inject любой accepted `IdFactory`.

---

# 7. `validate-profile`

`validate-profile` означает НЕ parse-only, а full static composition validation без cognitive execution.

Exact pipeline:

1. `load_kernel_profile(path)`;
2. `build_reference_registry()`;
3. create deterministic validation `IdFactory`;
4. `CompositionRoot(registry=..., id_factory=...).build(profile)` с default-disabled interventions;
5. если build successful — command success;
6. `runtime.run_cycle()` НЕ вызывать.

Следовательно команда проверяет минимум:

- TOML/schema/semantic IDs;
- registry resolution;
- implementation-specific settings;
- StateSchema assembly;
- composition fingerprint construction;
- plan compilation/DAG validity;
- complete Composition Root compatibility.

Созданный ephemeral runtime после validation не сохраняется.

---

# 8. `validate-profile` success output

Success stdout — ровно одна строка:

```text
OK validate-profile profile=<profile_id> modules=<module_count> waves=<wave_count>
```

Для canonical reference profile:

```text
OK validate-profile profile=v0_1.reference modules=4 waves=3
```

После строки обычный newline.

Success stderr пуст.

Exit code:

```text
0
```

Не печатать:

- UUIDs;
- fingerprint;
- full plan;
- trace;
- timestamps;
- Python repr runtime objects.

---

# 9. `kernel-smoke`

`kernel-smoke` выполняет ровно один cognitive cycle.

Exact pipeline:

1. `load_kernel_profile(path)`;
2. `build_reference_registry()`;
3. create deterministic smoke `IdFactory`;
4. `CompositionRoot(... default interventions disabled).build(profile)`;
5. pin compiled plan semantics;
6. `runtime.run_cycle()` ровно один раз;
7. require `CycleExecutionOutcome.SUCCEEDED`;
8. require exact reference join path `synthetic.join.value` существует в schema/state;
9. require final join availability `Available[int]`;
10. emit concise summary.

CLI не пересчитывает synthetic arithmetic самостоятельно. It reads the committed result через public `KernelRuntime.state`/accepted state contracts.

Для canonical `configs/v0.1/reference.toml` source=2 должен получиться:

```text
waves = 3
final StateRevision = 3
synthetic.join.value = Available(10)
```

Smoke не выполняет intervention.

---

# 10. `kernel-smoke` success output

Success stdout — ровно одна строка:

```text
OK kernel-smoke profile=<profile_id> waves=<wave_count> revision=<state_revision> join=<join_value>
```

Для canonical reference profile:

```text
OK kernel-smoke profile=v0_1.reference waves=3 revision=3 join=10
```

После строки newline.

Success stderr пуст.

Exit code:

```text
0
```

Не печатать IDs/full trace/timestamps.

---

# 11. Domain/configuration failure mapping

Expected user/domain failures включают `KernelError` и filesystem/profile problems, уже нормализованные `load_kernel_profile()` в typed configuration errors.

CLI ловит `KernelError` для обеих команд и пишет в stderr ровно одну строку:

```text
error: <message>
```

Без traceback.

Exit code:

```text
2
```

stdout пуст.

Это включает invalid profile/configuration/composition/schema/plan failures, возникшие из пользовательского profile.

Не переклассифицировать typed kernel errors по строковым pattern matching.

---

# 12. Smoke execution failure mapping

Если `runtime.run_cycle()` возвращает нормальный typed failed `CycleExecutionResult`, а не raises infrastructure exception:

- stdout пуст;
- stderr:

```text
error: kernel smoke cycle failed: <TraceFailure.error_type>: <TraceFailure.message>
```

- exit code `1`.

Если failed result нарушает own invariant и не имеет failure diagnostic — это internal invariant error, не user config success.

---

# 13. Unexpected internal failure mapping

Обычный unexpected `Exception`, который не является `KernelError`, считается internal CLI/runtime failure:

```text
error: internal failure: <ExceptionType>: <message>
```

stderr only, no traceback, exit code:

```text
1
```

`KeyboardInterrupt`, `SystemExit` и другие `BaseException` не маскировать этим catch.

Argparse `SystemExit(2)` остаётся standard usage semantics.

---

# 14. Output discipline

CLI stdout/stderr является только concise v0.1 smoke contract.

Запрещено:

- Rich/third-party formatting;
- colors/progress bars;
- log timestamps;
- nondeterministic UUID output;
- Python object repr;
- full evidence dump;
- extra success chatter.

Все success outputs deterministic для одинакового semantic profile.

---

# 15. Deterministic repeat semantics

Required deterministic repeat выполняется library-level integration/property test с двумя независимыми fresh runtime instances.

Оба build/run используют:

```text
DeterministicIdFactory(NAMESPACE_URL, "mindra.v0_1.kernel_smoke", counter=0)
```

и один и тот же immutable parsed profile semantics.

Сравниваются следующие normalized surfaces.

## 15.1. Semantic plan

Сравнить exact:

- phase;
- plan revision;
- schema revision;
- composition revision;
- plan fingerprint;
- dependencies;
- waves/module ordering.

`ExecutionPlanId` не нужен как semantic plan equality oracle, хотя при same deterministic seed он также должен reproducibly совпасть.

## 15.2. Final state semantic result

Сравнить exact:

- schema revision;
- final StateRevision;
- composition revision;
- `StatePath -> Availability` payload mapping.

Не использовать LineageId/BranchId/AgentRevisionId как единственный oracle semantic state result.

## 15.3. Logical O0 causal sequence

Из `runtime.evidence_snapshot()` для каждого event построить normalization:

```text
(event.kind, event.logical_time, event.payload)
```

`physical_timestamp_ns` намеренно исключить.

Normalized event tuple двух runs должен быть exactly equal.

Поскольку factory deterministic и producer ordering canonical, это доказывает воспроизводимую causal structural trace последовательность reference smoke.

Не сравнивать wall-clock duration/physical completion timing.

---

# 16. Expected canonical reference trace shape

Для одного successful reference cycle evidence начинается root events:

```text
composition_resolved
plan_compiled
```

затем scheduler cycle trace accepted IS-11 semantics.

Required deterministic test не должен hardcode каждый UUID string, но должен подтвердить:

- first two kinds root composition/plan;
- exactly one `cycle_started` и `cycle_finished`;
- three `wave_started`;
- successful commit sequence каждой wave;
- no `commit_failed`/`cycle_failed`/`intervention_applied`;
- logical normalized sequence repeats exactly.

---

# 17. Console/module equivalence

Behavioral equivalence обязательна для:

```text
mindra ...
python -m mindra ...
```

Для одного и того же valid canonical invocation сравнить:

- exit code;
- stdout exact;
- stderr exact.

Также минимум одна invalid-profile invocation должна иметь одинаковый domain-error class behavior (exit 2, stderr-only, no traceback) через обе entry forms.

`__main__.py` не реализует отдельный parser.

---

# 18. Test matrix

Создать минимум:

```text
tests/integration/test_reference_profile.py
tests/integration/test_cli.py
tests/property/test_reference_determinism.py
```

## 18.1. `test_reference_profile.py`

Проверить full in-process vertical slice:

- canonical profile loads;
- CompositionRoot builds;
- exact waves source / {double,triple} / join;
- one cycle succeeds;
- final revision 3;
- source/double/triple/join = 2/4/6/10;
- root + scheduler O0 evidence structurally valid;
- intervention absent/default-disabled.

## 18.2. `test_cli.py`

Проверить in-process `main(argv)`:

- validate success exact output/exit;
- smoke success exact output/exit;
- invalid/missing profile -> exit 2, stderr only, no traceback;
- unexpected ordinary Exception -> exit 1 deterministic internal line;
- argparse malformed invocation -> standard exit 2;
- no additional stdout chatter.

Subprocess:

- `python -m mindra validate-profile ...`;
- `python -m mindra kernel-smoke ...`;
- installed console script `mindra validate-profile ...`;
- installed console script `mindra kernel-smoke ...`;
- exact behavior equivalence.

Tests run inside locked environment after `uv sync`; console script existence is required there.

Cross-platform invocation must not hardcode Unix-only executable suffix/path.

## 18.3. `test_reference_determinism.py`

Два fresh deterministic full runs:

- same semantic plan;
- same waves;
- same state payload/revisions;
- same normalized O0 causal sequence excluding physical timestamp;
- expected join 10.

---

# 19. Build/install smoke boundary

IS-15 не создаёт nested second packaging system или custom installer.

Required evidence:

```text
uv sync --locked
```

создаёт current locked environment и устанавливает project/console script.

Subprocess test затем реально запускает installed `mindra` script и `python -m mindra`.

`uv build` отдельно подтверждает sdist/wheel buildability.

Чистая installation из wheel в ещё одно isolated environment не требуется на IS-15 и может быть проверена final hardening IS-16, если matrix потребует.

---

# 20. Architecture boundary

Entry points являются единственным новым production layer.

Architecture tests должны подтвердить минимум:

- `entrypoints` не создаёт module classes напрямую;
- no imports from `mindra.reference.synthetic`;
- no imports from runtime scheduler/commit/private implementation modules;
- no Service Locator/global registry;
- `runtime/reference/contracts` не импортируют entrypoints;
- existing Import Linter contracts remain green.

Entry points могут использовать public:

```text
mindra.composition
mindra.contracts
mindra.runtime.DeterministicIdFactory
```

только для user-facing orchestration, не для duplicate assembly.

---

# 21. VerificationObligations

После implementation ожидается:

```text
V01-009 — closed at deterministic v0.1 end-to-end O0 integration
V01-013 — closed at deterministic runnable reference profile/CLI layer
```

Final milestone acceptance этих obligations всё равно подтверждается IS-16 verification matrix/hardening.

---

# 22. Forbidden scope

IS-15 НЕ реализует:

- IS-16 verification matrix/hardening;
- Environment/Policy/Action/Experience Journal;
- evaluator/runtime;
- intervention CLI controls;
- multiple cycles CLI;
- arbitrary implementation/plugin loading;
- dynamic registry discovery;
- JSON/stable machine output API;
- logging framework;
- network telemetry;
- stable SDK promise;
- packaging/release publication;
- new runtime dependencies;
- new semantic identities/contracts;
- changes to scheduler/commit/intervention semantics.

---

# 23. Verification

Targeted:

```text
FAST + ARCH
pytest tests/integration/test_reference_profile.py \
       tests/integration/test_cli.py \
       tests/property/test_reference_determinism.py
```

После targeted green — `FULL-C0`.

Дополнительно вручную/automated subprocess evidence:

```text
uv run --locked mindra validate-profile --profile configs/v0.1/reference.toml
uv run --locked mindra kernel-smoke --profile configs/v0.1/reference.toml
uv run --locked python -m mindra validate-profile --profile configs/v0.1/reference.toml
uv run --locked python -m mindra kernel-smoke --profile configs/v0.1/reference.toml
```

Все четыре canonical invocations обязаны exit `0` и дать exact success lines этого clarification.

---

# 24. Relation to IS-16

После accepted IS-15 feature implementation завершена.

`IS-16` не добавляет новые feature semantics. Он выполняет version acceptance hardening:

- verification matrix `V01-001 … V01-014`;
- fresh clone/locked install/build checks;
- final regression/failure audits;
- status reconciliation;
- release-readiness evidence.

До independent acceptance IS-15 `IS-16` остаётся CLOSED.
