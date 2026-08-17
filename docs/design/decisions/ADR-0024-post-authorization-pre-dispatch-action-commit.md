# ADR-0024 — Action Commit после authorization и до dispatch

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-24 — Action Boundary / Gate / Executor`

---

# 1. Контекст

После `DU-23` Policy создаёт `SelectedActionIntent`, но MINDRA ещё не определяла точную границу:

```text
selected
→ authorized
→ committed
→ dispatched
→ executed
→ observed
```

Нужно решить:

- где находится canonical `Action Commit`;
- кто имеет право veto/transform intent;
- как отделить Policy choice от runtime override;
- как обрабатывать stale intent;
- что считать failure после commit;
- как делать retry без duplicate external effect;
- кто владеет dispatch/execution semantics.

---

# 2. Рассмотренные варианты

1. `SelectedActionIntent` сразу является `Action Commit`;
2. `Action Commit` происходит только после Environment acknowledgement/success;
3. Gate может молча заменить любое Policy action безопасным fallback;
4. authorization → **Action Commit → dispatch**, с explicit override provenance и transport/idempotency semantics.

---

# 3. Требования

Решение должно:

- сохранять Policy/action attribution;
- предотвращать dispatch stale/malformed/unauthorized action;
- не использовать hidden evaluator oracle normal runtime способом;
- сохранять irrevocable causal history после commit;
- различать dispatch failure и Environment no-effect;
- поддерживать sync и async/long-running environments;
- не обещать universal physical exactly-once;
- позволять explicit safety/runtime-assurance boundary;
- не превращать Action Gate в вторую Policy;
- поддерживать deterministic research tracing/interventions.

---

# 4. Вариант A — Intent сразу равен Action Commit

Conceptually:

```text
Policy
→ SelectedActionIntent = ActionCommit
→ Gate/Environment
```

## Плюсы

- минимальная цепочка;
- простая реализация.

## Минусы

- stale/capability/constraint rejection происходит уже после commit;
- трудно отличить Policy selection от фактически разрешённого action;
- behavior-changing shield correction ломает attribution;
- transport preparation и semantic authorization смешиваются.

**Решение:** отклонён.

---

# 5. Вариант B — Commit только после Environment success

Conceptually:

```text
intent
→ dispatch
→ Environment succeeded
→ Action Commit
```

## Плюсы

- committed actions всегда имеют outcome.

## Минусы

- причинно неверно: Agent уже принял необратимое решение до результата;
- dispatch/execution failures исчезают из behavioral history;
- online learning/revision attribution становится двусмысленной;
- нельзя корректно анализировать действия, которые были выбраны и отправлены, но провалились.

**Решение:** отклонён.

---

# 6. Вариант C — Gate свободно исправляет Policy action

Conceptually:

```text
Policy A
→ Gate
→ если A плохое, отправить B
```

## Плюсы

- может быть удобно для safety shielding;
- внешнее поведение остаётся допустимым.

## Минусы

- trajectory маскирует реальную ошибку Policy;
- Gate становится hidden Policy;
- невозможно честно оценить вклад shield/override;
- обучение на фактическом B может приписать Policy выбор, которого она не делала.

**Решение:** отклонён как normal implicit behavior.

Behavior-changing override допускается только как explicit `ActionOverridePolicy` с отдельным lineage `A → B`.

---

# 7. Вариант D — Authorization → Commit → Dispatch

Conceptually:

```text
SelectedActionIntent
        ↓
Action Gate
        ↓
AuthorizedAction
        ↓
ACTION COMMIT
        ↓
Dispatch
        ↓
Execution / Environment Transition
        ↓
Outcome Commit
```

Failure branches после commit сохраняются отдельно.

## Плюсы

- Policy choice и committed external action различимы;
- stale/malformed/rejected action не commit'ится;
- Action Commit остаётся необратимой границей `DU-03`;
- dispatch failure не стирает behavioral history;
- external override можно честно атрибутировать;
- retry/idempotency можно рассматривать отдельно от cognition;
- подходит как sync MicroWorld, так и async robotics/service environments.

## Минусы

- больше semantic identities/states;
- recovery после committed-but-not-executed action сложнее;
- нужен explicit `execution_unknown`/reconciliation path.

**Решение:** принято.

---

# 8. Принятое решение

MINDRA принимает:

1. `SelectedActionIntent` как Policy output, ещё не внешний action;
2. mandatory authorization boundary до commit;
3. default Gate semantics: validate/accept/reject + semantics-preserving normalization;
4. behavior-changing substitution только через explicit `ActionOverridePolicy`/RTA stage;
5. canonical `Action Commit` после финальной authorization и до dispatch;
6. `ActionCommitRecord` сохраняется независимо от последующего transport/execution result;
7. Dispatcher принадлежит execution infrastructure и не выбирает behavior;
8. Environment владеет actual transition/outcome;
9. stable `action_commit_id`/`dispatch_id` связывают retries и outcome;
10. universal exactly-once не обещается;
11. retry разрешён только при explicit idempotency/dedup semantics или достоверном definite-non-send;
12. неизвестное применение action оформляется как `execution_unknown`, а не silent resend;
13. terminal outcome фиксируется до reset.

---

# 9. Refinement DU-03

`DU-03` happy-path:

```text
Action Commit
→ Dispatch
→ Environment Transition
→ Outcome Commit
```

остаётся действительным.

`DU-24` добавляет допустимые failure branches:

```text
Action Commit
→ Dispatch definitely failed
→ execution fault / no Environment Transition
```

и:

```text
Action Commit
→ dispatch status unknown
→ reconciliation required
```

Это не меняет смысл самого `Action Commit`.

---

# 10. Ownership

```text
Policy
→ SelectedActionIntent

Agent runtime Action Boundary
→ authorization + Action Commit semantics

Execution Runtime / adapter
→ dispatch/retry/reconciliation mechanics

Environment
→ actual execution/transition/outcome
```

External runtime-assurance gate может находиться вне Agent cognition, но его veto/override должен быть explicit в provenance.

---

# 11. Последствия

## Положительные

- causal trace полностью восстанавливает intent → outcome;
- Policy и safety/override можно оценивать отдельно;
- transport failure не маскируется как cognitive failure;
- idempotency/retry можно тестировать независимо;
- partial observability не ломается hidden Gate oracle.

## Отрицательные

- больше типов evidence;
- нужен recovery design для unknown execution;
- exact distributed checkpoint/restore сложнее и остаётся `DU-27`.

---

# 12. Что не принято этим ADR

ADR не выбирает:

- конкретный action schema;
- конкретную safety specification;
- shielding/RTA algorithm;
- transport protocol;
- retry count/backoff;
- ROS/gRPC/HTTP;
- concrete action cancellation API;
- exact Python implementation.

---

# 13. Research controls

Для сложного Gate/override минимум сравнивать:

```text
PassThrough/SchemaOnly
vs Capability/Constraint Gate
vs explicit Shield/RTA
vs Random/Shuffled rejection control
```

Policy quality анализируется **до** Gate, а фактическое environment behavior — **после** Gate.

Для retry/idempotency обязательны injected transport failure, duplicate-attempt и unknown-execution scenarios.
