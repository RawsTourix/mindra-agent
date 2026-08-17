# Action Boundary / Gate / Executor MINDRA

## Статус документа

**Design Update:** `DU-24 — Action Boundary / Gate / Executor`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет причинную границу между выбранным `Policy System` поведенческим намерением и внешним изменением `Environment`.

Ключевое решение `DU-24`:

- `SelectedActionIntent` ещё не является действием, которое разрешено или отправлено во внешний мир;
- перед внешним воздействием существует обязательная `Action Boundary` с явной authorization/validation semantics;
- канонический `Action Commit` происходит **после** финальной pre-dispatch authorization/staleness/precondition проверки и **до** dispatch;
- normal `Action Gate` не выполняет скрытую behavior-changing substitution;
- semantics-preserving normalization/encoding не считается новым выбором поведения;
- behavior-changing override допускается только через отдельную explicit `ActionOverridePolicy`/runtime-assurance stage с собственной provenance;
- после `Action Commit` история не переписывается даже при dispatch/execution failure;
- dispatch/execution обязаны иметь stable correlation identities и capability-declared retry/idempotency semantics;
- `Action Dispatcher` является execution infrastructure, а не cognitive decision maker;
- `Environment` остаётся владельцем фактического transition/outcome.

Документ опирается на:

- [`../system-context.md`](../system-context.md) — Agent/Execution Runtime/Environment logical boundaries;
- [`../execution-model.md`](../execution-model.md) — `Decision Window`, `Action Commit`, `Environment Transition`, `Outcome Commit`;
- [`../cognitive-state.md`](../cognitive-state.md) — committed state/revision/provenance;
- [`../module-lifecycle.md`](../module-lifecycle.md) — atomic commits и stale semantics;
- [`../observability-and-intervention.md`](../observability-and-intervention.md) — evidence/intervention;
- [`environment.md`](environment.md) — agent/research planes и Environment transition ownership;
- [`policy-planner.md`](policy-planner.md) — `SelectedActionIntent`, Policy ownership и `ActionCapabilityDescriptor`;
- [`self-model.md`](self-model.md) — agent-visible capability/limitation evidence;
- [`valuation.md`](valuation.md) — constraints/risk не являются Action Gate сами по себе;
- [`executive-control.md`](executive-control.md) — Executive не выбирает Environment action.

Документ намеренно **не** определяет:

- concrete MicroWorld action enum/schema;
- универсальную моральную/normative safety policy;
- конкретный formal-verification/shielding algorithm;
- обязательный learned Action Gate;
- ROS/gRPC/HTTP как transport;
- конкретный retry framework;
- exact Python API;
- Experience/Data/Replay schema — `DU-25`;
- training — `DU-26`;
- checkpoint encoding — `DU-27`.

---

# 1. Цель DU-24

После `DU-23` Agent уже способен сформировать:

```text
SelectedActionIntent
```

со смыслом:

> «Policy при текущем committed context выбрала это поведение».

Но из этого ещё не следует:

```text
action structurally valid
action всё ещё актуален
action capability доступна
action разрешён configured constraints
action committed
action dispatch состоялся
action был принят Environment
action физически/логически исполнился
world transition произошёл
outcome наблюдён
```

`DU-24` обязан сделать все эти границы причинно различимыми.

Каноническая цепочка:

```text
SelectedActionIntent
        ↓
Action Authorization / Gate
        ↓
AuthorizedAction
        ↓
Action Commit
        ↓
Dispatch
        ↓
Environment acceptance/execution
        ↓
Environment Transition
        ↓
Outcome Observation
        ↓
Outcome Commit
```

Но failure branches являются first-class и не должны скрываться в одном `step()`.

---

# 2. Module / responsibility gate

## 2.1. Action Boundary обязательна

Отдельная semantic boundary проходит gate **безусловно**.

Без неё невозможно отличить:

```text
что Policy выбрала
от
что фактически ушло во внешний мир
```

и невозможно корректно представить stale intent, runtime constraint, transport failure, override, duplicate dispatch или partial execution.

## 2.2. Action Gate не обязан быть cognitive module

Базовый `Action Gate` относится к `Agent runtime core` как invariant execution boundary, а не как модуль, определяющий цели/utility/policy.

Он может иметь versioned authorization policy, но не получает ambient decision authority.

## 2.3. Dispatcher / Executor не является cognition

`Action Dispatcher`/execution adapter логически относится к `Execution Runtime`/Environment integration boundary.

Он:

- сериализует/передаёт уже committed action;
- управляет transport identities/retries согласно capability;
- получает acknowledgement/result;
- не выбирает другой action;
- не вычисляет utility;
- не вызывает Policy fallback скрыто.

Фактические transition rules принадлежат `Environment`.

---

# 3. Канонические различия

```text
SelectedActionIntent
≠
NormalizedAction
≠
AuthorizedAction
≠
CommittedAction
≠
DispatchAttempt
≠
EnvironmentActionReceipt
≠
Executed/Applied Action status
≠
Environment Transition
≠
Outcome Commit
```

Также:

```text
malformed intent
≠
stale intent
≠
constraint rejection
≠
dispatch failure
≠
execution unknown
≠
Environment-level no-effect
≠
partial execution
```

И:

```text
Policy choice
≠
external runtime override
```

---

# 4. Ownership и логические роли

## 4.1. Policy System

Владеет:

- `SelectedActionIntent`;
- selection provenance.

Не владеет authorization/dispatch/execution.

## 4.2. Action Boundary / Gate

Владеет semantic responsibility:

- проверить intent относительно declared action contract;
- проверить freshness/base revisions;
- проверить agent-visible/current capability availability;
- применить explicit authorization constraints;
- сформировать `ActionAuthorizationResult`;
- сформировать `AuthorizedAction` при успехе;
- инициировать canonical `Action Commit` только после финальной authorization.

Gate не владеет Goals/Utility/Policy selection.

## 4.3. Execution Runtime / Action Dispatcher

Владеет:

- transport/provider integration;
- `DispatchAttempt`;
- retry/dedup/reconciliation mechanics;
- provider acknowledgements;
- mapping canonical committed action в provider/environment-native representation, если mapping semantics-preserving.

## 4.4. Environment

Владеет:

- фактическим принятием/применением action согласно environment contract;
- hidden transition rules;
- `Environment Transition`;
- agent-visible outcome/feedback;
- termination/truncation.

---

# 5. SelectedActionIntent и freshness

`SelectedActionIntent` обязан сохранять как минимум semantic references к:

```text
intent_id
base state_revision
decision_id
agent_revision
policy_revision
action capability/interface revision
selected candidate/action semantics
relevant assumptions/preconditions
selection/RNG provenance
```

Перед authorization Gate проверяет, что intent ещё относится к допустимому committed context.

## 5.1. Stale intent

Intent считается stale, если изменилось behavior-relevant состояние/contract, относительно которого выбор больше нельзя считать тем же решением.

Например:

```text
Policy выбрала use(key)
↓
до Action Commit action capability изменилась
↓
intent stale
```

Default:

```text
stale intent
→ reject / require reselection
```

Запрещено:

```text
stale intent
→ implicit rebase
```

Compatibility/revalidation может быть разрешена только explicit versioned policy.

---

# 6. Action authorization pipeline

Conceptually:

```text
SelectedActionIntent
        ↓
structural/schema validation
        ↓
freshness/revision validation
        ↓
capability/availability validation
        ↓
explicit precondition validation
        ↓
constraint / authorization stages
        ↓
normalization/compilation
        ↓
AuthorizedAction
```

Порядок конкретных stages может быть version-specific, но каждый stage должен иметь identity/revision/provenance.

## 6.1. Structural validation

Проверяет:

- action kind известен;
- required parameters присутствуют;
- parameter domain/schema корректен;
- action interface revision совместима.

Malformed intent не отправляется Environment.

## 6.2. Capability validation

Gate использует только declared action capability surface и разрешённый current state.

Если capability unavailable:

```text
SelectedActionIntent
→ capability_rejected
→ no Action Commit
```

## 6.3. Preconditions

Policy/Planner candidate может содержать assumptions/preconditions.

Gate проверяет только те preconditions, которые разрешено знать на текущей boundary.

Он **не получает права** спрашивать hidden Environment Ground Truth:

```text
«на самом деле за дверью ловушка?»
```

если Agent этого не наблюдает и отдельная deployment safety boundary не имеет такого разрешённого trust contract.

Следовательно, action может пройти Gate и всё равно оказаться ineffective/invalid по скрытой причине Environment. Это нормальная partial-observability semantics.

---

# 7. Constraints и safety boundary

`DU-24` не вводит универсальную моральную или safety value system.

Он вводит возможность explicit `ActionConstraintSet`/authorization stages из различимых источников:

```text
action interface constraints
agent-visible task/runtime constraints
capability constraints
explicit deployment/runtime-assurance constraints
research intervention constraints
```

Каждый constraint source обязан иметь:

```text
source identity
owner/trust boundary
revision
agent-visible status
scope
provenance
```

Evaluator-only correctness labels или hidden test answer не могут использоваться normal Gate как safety oracle.

## 7.1. External runtime assurance

Допускается внешний deployment guard, который находится вне cognitive Agent boundary.

Если такой guard veto/override'ит Policy behavior:

- это не считается решением Policy;
- override/rejection сохраняет external provenance;
- evaluation должна отдельно различать Agent performance и runtime-assurance intervention.

---

# 8. Accept, reject, normalize, override

## 8.1. Accept

Intent семантически разрешён без изменения behavior.

## 8.2. Reject / require reselection

Нормальный способ Gate не допустить action:

```text
SelectedActionIntent
→ ActionRejection
→ no Action Commit
→ новый committed control/decision boundary
→ Policy/Executive recovery согласно lifecycle
```

Gate не выбирает замену самостоятельно.

## 8.3. Semantics-preserving normalization

Допустимы representation-level преобразования:

```text
angle 450° → normalized 90°
canonical enum → Environment-native code
parameter unit conversion
field ordering/serialization
```

если transformation доказуемо сохраняет action semantics текущего contract.

Создаётся отдельный normalization provenance.

## 8.4. Behavior-changing substitution

Default normal Gate **не выполняет**:

```text
Policy выбрала A
Gate молча отправил B
```

Если deployment/research требует override:

```text
SelectedActionIntent A
        ↓
ActionOverridePolicy
        ↓
OverrideRecord(A → B)
        ↓
AuthorizedAction B
```

При этом:

```text
Policy choice = A
Committed external action = B
```

обе сущности сохраняются отдельно.

`ActionOverridePolicy` имеет отдельную identity/revision/trust provenance и может быть полностью отключена.

---

# 9. AuthorizedAction

`AuthorizedAction` — immutable по смыслу результат успешной pre-dispatch authorization.

Conceptually:

```text
AuthorizedAction
├── authorized_action_id
├── selected_intent_id
├── final semantic action
├── normalization refs[]
├── override ref?
├── authorization stage records[]
├── constraint-set revisions
├── base state_revision
├── action interface revision
├── agent_revision
└── provenance
```

Сам `AuthorizedAction` ещё можно отменить до `Action Commit` при обнаружении нового pre-commit invalidating event.

После commit нельзя.

---

# 10. Канонический Action Commit

`Action Commit` происходит в точке:

```text
final authorization complete
        ↓
AuthorizedAction valid/current
        ↓
ACTION COMMIT
        ↓
external dispatch allowed
```

Это означает:

> для данного Decision Window зафиксировано ровно одно действие, которое система намерена отправить во внешний action boundary.

## 10.1. ActionCommitRecord

Conceptually:

```text
ActionCommitRecord
├── action_commit_id
├── authorized_action_id
├── selected_intent_id
├── decision_id
├── episode_id
├── state_revision_at_commit
├── agent_revision
├── policy_revision
├── gate/constraint revisions
├── action interface revision
├── committed semantic action
├── override/normalization lineage
├── dispatch identity seed/key
└── provenance
```

## 10.2. Необратимость истории

После `Action Commit` нельзя:

- заменить committed action новым Policy result;
- применить Learning Update и назвать старое действие продуктом новой revision;
- удалить commit из trajectory из-за dispatch failure;
- «вернуть Decision Window назад» без explicit recovery semantics.

---

# 11. Action Commit и dispatch failure

`Action Commit` не гарантирует, что транспорт/Environment успешно применят action.

Поэтому accepted causal graph имеет failure branch:

```text
Action Commit
    ↓
Dispatch Attempt
    ├── definitely not sent
    │       ↓
    │   Dispatch Failure
    │   no Environment Transition
    │
    ├── sent / acknowledged
    │       ↓
    │   Environment processing
    │
    └── execution status unknown
            ↓
       Reconciliation required
```

Это уточняет базовый happy-path `DU-03`, не меняя смысла `Action Commit`.

## 11.1. Definitely-not-sent

Если runtime достоверно знает, что action не пересёк execution boundary:

- commit остаётся фактом;
- Environment Transition отсутствует;
- создаётся explicit execution/dispatch fault;
- дальнейшая recovery/reselection не маскирует исходный commit.

## 11.2. Unknown whether applied

Самый опасный случай:

```text
request sent
connection lost
неизвестно, успел ли Environment применить action
```

Запрещено автоматически считать:

```text
not executed
```

или автоматически повторно отправлять non-idempotent action.

Состояние:

```text
execution_unknown
```

становится first-class и требует reconciliation/reset/contract-specific recovery.

---

# 12. Dispatch identity и idempotency

Каждый committed external action получает stable identities:

```text
action_commit_id
dispatch_id
```

Retry того же **логического dispatch** обязан использовать ту же idempotency/dedup identity, а не создавать новый action commit.

## 12.1. Capability declaration

Environment/adapter обязан явно описывать transport semantics, например:

```text
idempotent_by_action_semantics
deduplicated_by_dispatch_id
at_most_once_transport
retry_safe_after_definite_non_send
non_idempotent / unknown
```

Exact enum не frozen.

## 12.2. Universal exactly-once не обещается

MINDRA не заявляет универсальное physical exactly-once execution.

Архитектурная цель:

```text
один logical Action Commit
+
однозначная dispatch/execution provenance
+
no silent duplicate effect
```

Concrete adapter обязан либо:

- поддержать deduplication/idempotency;
- доказать definite-not-sent перед retry;
- либо перейти в `execution_unknown` вместо опасного automatic resend.

## 12.3. MicroWorld baseline

Для локальной step-locked reference среды рекомендуется поддерживать:

```text
apply(action_commit_id, action)
```

так, чтобы повтор того же `action_commit_id` не создавал второй Environment Transition.

Это implementation target, а не универсальное требование внешних физических сред.

---

# 13. DispatchAttempt

Conceptually:

```text
DispatchAttempt
├── dispatch_attempt_id
├── dispatch_id
├── action_commit_id
├── attempt_index
├── adapter/provider revision
├── payload representation revision
├── started logical/runtime evidence
├── transport result
├── acknowledgement ref?
├── failure/unknown reason?
└── provenance
```

Новый retry attempt не создаёт новый `ActionCommitRecord`.

---

# 14. Environment acknowledgement / receipt

Для некоторых environments между dispatch и конечным outcome существует отдельное принятие команды.

Conceptually:

```text
EnvironmentActionReceipt
├── receipt_id
├── action_commit_id / dispatch_id
├── accepted / rejected / unknown
├── environment/action interface revision
├── execution handle/id?
└── provenance
```

Receipt:

```text
accepted
≠
succeeded
```

Для simple synchronous MicroWorld receipt может быть collapsed implementation detail, если causal evidence остаётся однозначной.

Для asynchronous/long-running environment receipt должен быть различим.

---

# 15. Execution status и фактический effect

Для general Environment action может иметь жизненный цикл:

```text
accepted
→ executing
→ completed / aborted / cancelled / partial / unknown
```

Exact states зависят от environment capability.

Важно различать:

## 15.1. Successful processing with no world effect

Например valid action `open(door)`, но дверь уже открыта.

Это может быть нормальный:

```text
Environment Transition
state change = none
```

а не transport failure.

## 15.2. Environment-level semantic failure

Например action корректен по agent-visible contract, но hidden precondition не выполнен.

Environment может вернуть agent-visible failure/no-effect согласно task contract.

Это не означает, что Gate был некорректен: partial observability сохранена.

## 15.3. Partial execution

Если action успел частично изменить мир:

- transition/effect не отменяется задним числом;
- original action нельзя безопасно retry автоматически как будто ничего не произошло;
- outcome обязан фиксировать partial status/evidence.

---

# 16. Cancellation и preemption

Для long-running actions cancellation/preemption может существовать как отдельная environment/action capability.

После `Action Commit` cancellation **не делает commit неслучившимся**.

Она создаёт отдельное causal control событие/command с собственным identity/provenance.

Конкретная cancellation Policy не определяется `DU-24`.

---

# 17. Termination / truncation

## 17.1. Episode уже закрыт до commit

Если Episode стал terminal/truncated до финального Action Commit:

```text
SelectedActionIntent
→ stale/closed-episode rejection
→ no Action Commit
```

## 17.2. Terminal outcome после action

```text
Action Commit
→ Environment Transition
→ terminal Outcome
→ Outcome Commit
→ Episode close
→ только затем reset
```

Terminal outcome нельзя потерять из-за autoreset.

## 17.3. Truncation между commit и dispatch/execution

Если внешний runtime прекращает episode/run после Action Commit:

- commit сохраняется;
- dispatch/execution state фиксируется как реально произошедший;
- нельзя притвориться, что intent просто не существовал;
- recovery semantics зависит от конкретного environment/runner contract.

---

# 18. Recovery после Gate rejection

Gate rejection **не является Environment Outcome**.

Conceptually:

```text
SelectedActionIntent
→ ActionRejection
→ committed internal rejection evidence
→ new Executive/Policy control boundary
→ re-evaluation/reselection
```

Чтобы избежать бесконечного цикла:

- rejection имеет reason/provenance;
- repeated equivalent rejection должна быть observable;
- Decision Window имеет finite budget/termination semantics;
- fallback не скрывается.

---

# 19. NoOp / abort

## 19.1. NoOp

`NoOp` считается обычным Environment action **только если** текущий Environment action contract явно определяет его семантику.

Нельзя универсально подменять любое rejection на `NoOp`.

## 19.2. Abort / no action dispatch

Если normal action невозможно сформировать/разрешить, runtime может завершить Decision Window/episode согласно explicit failure semantics.

Это не должно выглядеть как будто Environment получила `NoOp`.

---

# 20. Observability

Evidence Plane должен позволять восстановить цепочку:

```text
PolicyCandidate
→ SelectedActionIntent
→ Gate stage results
→ AuthorizedAction
→ ActionCommitRecord
→ DispatchAttempt(s)
→ EnvironmentActionReceipt
→ execution status
→ EnvironmentTransition
→ OutcomeCommit
```

Минимально полезны identities:

```text
selected_intent_id
authorized_action_id
action_commit_id
dispatch_id
dispatch_attempt_id
receipt/execution identity
environment_transition_id
outcome identity
```

Для override дополнительно обязательно:

```text
original Policy intent
→ override record
→ committed external action
```

---

# 21. Intervention

Допустимы отдельные controlled interventions:

```text
SelectedActionIntent intervention
Gate/constraint intervention
force rejection
force authorization
ActionOverridePolicy intervention
dispatch suppression
execution-failure injection
acknowledgement loss
duplicate-dispatch attempt
```

Каждый intervention должен сохранять `intervention_id` и provenance.

Evaluator не может молча заменить action и затем считать trajectory natural.

---

# 22. Snapshot / restore

До `Action Commit` snapshot должен сохранять pending action-boundary state, если он causally relevant.

После commit snapshot/recovery обязан учитывать как минимум:

```text
ActionCommitRecord
pending dispatch identity
completed dispatch attempts
known acknowledgement/execution status
dedup/reconciliation state
adapter/environment revision
Gate/constraint revisions
```

Нельзя restore'ить состояние после неизвестного внешнего execution так, будто внешний мир гарантированно откатился.

Exact Agent+Environment distributed recovery определяется `DU-27`, но ambiguity уже является canonical state, а не скрытой ошибкой.

---

# 23. Failure taxonomy

Минимально различимы:

```text
intent_malformed
intent_stale
capability_unavailable
precondition_unknown_or_failed
constraint_rejected
authorization_failure
override_applied
dispatch_definitely_failed
dispatch_timeout_execution_unknown
environment_rejected
environment_no_effect
execution_partial
execution_aborted
outcome_missing
```

Exact enum не frozen.

Важно, что failure classes принадлежат разным causal layers и не должны сворачиваться в один `action_failed=true`.

---

# 24. Controls / baselines

Минимально предусмотреть:

```text
PassThroughGate
SchemaOnlyGate
CapabilityOnlyGate
FixedConstraintGate
RandomRejectGate
ShuffledConstraintControl
OverrideDisabled
ExplicitShield/RuntimeAssurance control
```

Oracle Gate допускается только как privileged research control и никогда не считается normal Agent capability.

Для dispatch/retry:

```text
NoRetry
SafeIdempotentRetry
InjectedTransportFailure
DuplicateAttemptControl
```

---

# 25. Evaluation requirements

Нужно отдельно измерять:

## 25.1. Policy quality

Что Policy выбрала до Gate.

## 25.2. Gate effect

```text
accept/reject rate
rejection reasons
stale-intent rate
override rate
false/over-conservative rejection
constraint violation prevention
```

## 25.3. Dispatch reliability

```text
commits
dispatch attempts
retries
duplicate suppression
unknown execution states
transport failures
```

## 25.4. Environment execution

```text
accepted/executed/no-effect/partial/aborted
outcome correlation completeness
```

## 25.5. Attribution

Нельзя приписывать Policy успех override action без отдельного анализа.

Нельзя приписывать Gate ошибку, если hidden Environment precondition не могла быть известна Gate по contract.

---

# 26. Negative / falsification criteria

Action Boundary как semantic boundary обязательна, но отдельная сложная learned/constraint Gate не считается автоматически полезной.

Если:

```text
PassThrough/SchemaOnly
≈
сложный Gate
```

при тех же contract constraints и сложный Gate не предотвращает специфические invalid/unsafe actions, его дополнительная сложность не обоснована.

Behavior-changing override system также требует отдельного causal justification относительно reject/reselect или simpler shield.

---

# 27. Что намеренно не frozen

`DU-24` не фиксирует:

- Python classes/protocols;
- concrete action enum;
- exact Gate stages;
- exact constraint language;
- formal verification framework;
- learned vs rule-based Gate;
- retry library;
- transport protocol;
- ROS actions;
- gRPC/HTTP;
- exact idempotency token format;
- cancellation state machine;
- timeout values;
- concrete recovery algorithm.

---

# 28. Критерий принятия DU-24

`DU-24` считается закрытым, когда из документации однозначно следует:

1. `SelectedActionIntent` не равен внешнему действию;
2. Gate является обязательной authorization boundary, но не скрытой Policy;
3. stale/malformed/constraint-rejected intents не commit'ятся;
4. semantics-preserving normalization отделена от behavior-changing override;
5. override сохраняет отдельную provenance и не приписывается Policy;
6. `Action Commit` находится после authorization и до dispatch;
7. commit сохраняется даже при dispatch failure;
8. dispatch/retry имеют stable identities и explicit idempotency capability;
9. unknown execution является first-class состоянием;
10. Environment no-effect/partial execution не смешиваются с transport failure;
11. terminal outcome фиксируется до reset;
12. causal trace связывает intent → authorization → commit → dispatch → execution → outcome;
13. concrete transport/safety algorithms не заморожены.
