# DU-24 — Action Boundary / Gate / Executor: research pass 2026-08

## Статус

**Дата:** 2026-08-17  
**Тип:** non-canonical research evidence  
**Связанный Design Update:** `DU-24 — Action Boundary / Gate / Executor`

Этот документ фиксирует исследовательские и инженерные ориентиры, использованные при проектировании `DU-24`.

Он **не выбирает** concrete safety shield, transport, ROS, retry library, constraint DSL или action schema.

---

# 1. Исследовательский вопрос

Нужно спроектировать границу:

```text
Policy selected intent
→ authorization
→ commit
→ dispatch
→ execution
→ outcome
```

так, чтобы:

- Policy attribution не терялась;
- stale/invalid action не уходил Environment;
- safety/runtime assurance не превращалась в hidden Policy;
- network/transport failure не создавал silent duplicate action;
- partial/unknown execution был first-class;
- hidden evaluator truth не протекал в normal cognition.

---

# 2. Safe RL via Shielding

## Alshiekh et al. — Safe Reinforcement Learning via Shielding

- arXiv: `1708.08611`
- https://arxiv.org/abs/1708.08611

Работа рассматривает safety shield, который может быть расположен:

1. **до** решения learner и предоставлять только допустимые actions;
2. **после** learner и корректировать выбранное действие при нарушении specification.

Для MINDRA это важный evidence, что существуют как минимум две реально используемые semantics:

```text
safe candidate restriction
```

и:

```text
post-policy override/correction
```

Но второй вариант создаёт attribution problem:

```text
Policy chose A
Shield executed B
```

Поэтому `DU-24` допускает behavior-changing override только через explicit `ActionOverrideRecord`, а не скрытую замену.

---

# 3. Probabilistic shielding и partial observability

## Jansen et al. — Safe Reinforcement Learning via Probabilistic Shields

- arXiv: `1807.06096`
- https://arxiv.org/abs/1807.06096

Probabilistic shielding использует probabilistic safety information для ограничения решений.

## Carr et al. — Safe Reinforcement Learning via Shielding under Partial Observability

- arXiv: `2204.00755`
- https://arxiv.org/abs/2204.00755

Работа отдельно рассматривает shielding при partial observability.

Для MINDRA важен общий вывод:

> safety/action filtering может использовать отдельную model/specification boundary, но доступность safety evidence должна быть явно определена.

Это **не** разрешает normal Action Gate читать `Environment Research Ground Truth` или evaluator answer без отдельного trust contract.

---

# 4. Runtime Assurance

## NASA — A Verification Framework for Runtime Assurance of Autonomous UAS

- NTRS: `20240007986`
- https://ntrs.nasa.gov/citations/20240007986

Runtime Assurance / Simplex architecture разделяет:

```text
advanced/untrusted controller
+
runtime monitor
+
trusted/reversionary controller
```

При нарушении property управление может передаваться backup controller.

Для MINDRA это поддерживает возможность **external deployment runtime-assurance layer**, отличного от Policy.

Но MINDRA не принимает Simplex/RTA как обязательную cognitive architecture.

Если RTA подменяет action, evidence обязано сохранять:

```text
original Policy intent
→ external override
→ committed external action
```

и evaluation не должна приписывать override behavior самой Policy.

---

# 5. Fresh 2026 RTA evidence

## Haroon et al. — Learning When to Act: Communication-Efficient Reinforcement Learning via Run-Time Assurance

- arXiv: `2605.12561`
- https://arxiv.org/abs/2605.12561

Работа 2026 года использует run-time assurance layer, который override'ит learned policy при нарушении Lyapunov-based safety condition.

Для `DU-24` это актуальное evidence, что архитектурное разделение:

```text
learned behavioral policy
≠
runtime safety enforcement
```

остаётся practically relevant.

MINDRA при этом не принимает их Lyapunov/LQR design или reward как canonical implementation.

---

# 6. ROS 2 Actions: selection/acceptance/execution/result различаются

## ROS 2 Documentation — Understanding actions

- https://docs.ros.org/en/ros2_documentation/kilted/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html

ROS 2 Actions предназначены для операций, которые могут быть длительными.

Практически присутствуют:

```text
send goal
→ goal accepted with unique ID
→ feedback
→ result
```

Unique goal ID связывает request, feedback и result.

## action_msgs / GoalStatus

- https://docs.ros.org/en/ros2_packages/kilted/api/action_msgs/msg/GoalStatus.html

State machine различает как минимум:

```text
ACCEPTED
EXECUTING
CANCELING
SUCCEEDED
CANCELED
ABORTED
```

Для MINDRA важна не ROS-specific state machine, а engineering precedent:

```text
command accepted
≠
command executing
≠
command succeeded
```

и stable action identity полезна для correlation.

`DU-24` поэтому не сворачивает всё в `env.step(action) -> done` как универсальную causal semantics.

---

# 7. Idempotency и retry после communication failure

## RFC 9110 — HTTP Semantics, Idempotent Methods

- RFC 9110 §9.2.2
- https://www.rfc-editor.org/rfc/rfc9110.html

RFC определяет идемпотентную request semantics как такую, при которой повтор одинакового запроса имеет тот же intended server effect, что и один запрос.

Особенно важно правило retry:

- автоматический repeat оправдан для idempotent semantics;
- non-idempotent request нельзя автоматически retry'ить, если клиент не знает, что операция не была применена, либо не имеет другой гарантии idempotency.

Это напрямую мотивирует `DU-24` distinction:

```text
definitely_not_sent
vs
execution_unknown
```

Если MINDRA отправила non-idempotent action и потеряла acknowledgement, опасно делать:

```text
retry blindly
```

Нужны explicit dedup/idempotency capability или reconciliation.

MINDRA не использует HTTP как обязательный transport; RFC используется как общий инженерный precedent retry semantics.

---

# 8. Action masking

## Gymnasium — Action Masking in Taxi

- https://gymnasium.farama.org/tutorials/training_agents/action_masking_taxi/

Gymnasium tutorial показывает распространённый pattern, при котором environment предоставляет mask допустимых действий и Policy рассматривает только valid actions.

Для MINDRA это useful baseline для **agent-visible capability constraints**.

Но canonical architecture не принимает правило:

```text
Environment hidden state
→ full valid-action mask
→ Policy
```

для всех сред.

Если action mask раскрывает information, которой Agent не должен знать, это изменяет observation/task contract.

Поэтому `ActionCapabilityDescriptor`/constraint source должны иметь explicit agent-visible semantics.

---

# 9. Почему normal Gate не должен быть hidden Policy

Safety literature допускает correction/backup action, но для исследовательской архитектуры MINDRA важно различать:

```text
Policy quality
```

и:

```text
external safety system quality
```

Если Gate молча исправляет Policy:

- нельзя понять, что Policy выбрала;
- downstream training data может неправильно атрибутировать replacement;
- ablation shield становится нечистой;
- causal intervention на Policy теряет смысл.

Поэтому default semantics:

```text
accept
reject/reselect
semantics-preserving normalize
```

а behavior-changing replacement только explicit override.

---

# 10. Action Commit placement

Рассмотренные conceptual placements:

```text
A. commit at Policy selection
B. commit after Environment success
C. commit after authorization, before dispatch
```

`C` лучше сохраняет:

- Policy attribution;
- pre-dispatch validation;
- causal irreversibility;
- failure evidence;
- online-learning revision history.

После commit может не произойти Environment Transition из-за transport failure. Это не повод удалять commit из history.

---

# 11. Exactly-once

Для arbitrary remote/physical environment универсальное physical exactly-once обещание слишком сильное.

Research/engineering target MINDRA:

```text
one logical Action Commit
stable dispatch identity
explicit retry capability
no silent duplicate effect
explicit unknown state
```

MicroWorld может предоставить более сильную deterministic deduplication по `action_commit_id`, но это property конкретного adapter/environment contract.

---

# 12. Evaluation implications

Будущая evaluation должна отдельно измерять:

```text
Policy intent accuracy/quality
Gate rejection/override behavior
runtime safety effect
dispatch reliability
duplicate suppression
unknown execution frequency
actual Environment effects
```

Нельзя давать полный system success score только Policy, если значительную часть unsafe решений исправил external shield.

---

# 13. Вывод для DU-24

Исследование поддерживает следующие architectural conclusions:

1. action authorization и Policy selection стоит разделять;
2. pre-selection filtering и post-policy override — разные semantics;
3. override должен иметь separate provenance;
4. acceptance/execution/result являются различимыми lifecycle states;
5. stable action identity полезна для correlation;
6. retry должен зависеть от idempotency/dedup semantics;
7. unknown execution нельзя скрывать;
8. transport/infrastructure не должен становиться cognitive Policy;
9. concrete shield/transport framework не следует фиксировать на canonical design level.
