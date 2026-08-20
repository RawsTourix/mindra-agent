# V0.1-IS-09 — Active composition boundary consistency correction

## Статус

**Статус:** `accepted correction clarification`  
**Область:** только correction `V0.1-IS-09 — Atomic CommitCoordinator`  
**Baseline:** accepted `is-09-commit-coordinator-shape.md` + `is-08-private-state-store-shape.md` + `F31`

Этот документ закрывает implementation-level defect, обнаруженный ChatGPT audit после commit `c11d79e78716d2273a602b94d1e78a4a3846c45b`.

## 1. Defect

`CommitCoordinator` принимает active `ModuleDescriptor` и уже построенный `PrivateStateStore`, но текущая реализация не доказывает, что store создан из той же active composition.

Из-за этого возможен несовместимый runtime boundary:

```text
CommitCoordinator descriptor ModuleId=A, implementation/private contract X
PrivateStateStore descriptor ModuleId=A, implementation/private contract Y
```

Тогда public proposal валидируется по X, а private proposal — по Y. Один successful commit может тем самым объединить public/private semantics разных composition definitions.

Это нарушает fail-closed active composition boundary.

## 2. Required correction

При construction `CommitCoordinator` обязан fail closed подтвердить совместимость `descriptors` и `PrivateStateStore` **до первого commit**.

Минимальные semantics:

- набор зарегистрированных `ModuleId` в coordinator и private store совпадает точно;
- для каждого `ModuleId` store относится к тому же active `ModuleDescriptor`;
- statefulness совпадает;
- implementation identity/revision совпадают;
- private-state descriptor/contract boundary соответствует active descriptor;
- extra/missing module в store запрещён.

Предпочтительно использовать internal runtime-only compatibility helper/private inspection в `mindra.runtime.private_state`; не добавлять module-facing/public cognitive API.

## 3. Important constraints

- не дублировать concrete private payload validation в `CommitCoordinator`;
- private proposal по-прежнему проходит `PrivateStateStore._prepare()`;
- не добавлять Service Locator/registry;
- не менять public `ModuleComputeRequest`;
- не менять commit pipeline, DAG, scheduler или Evidence semantics;
- не начинать `IS-10`.

## 4. Verification

Добавить regression tests минимум для:

1. coordinator + exactly matching store descriptors -> success;
2. same ModuleId, but different implementation identity/revision -> coordinator construction reject;
3. same ModuleId, but different statefulness/private descriptor/contract -> reject;
4. store missing active module -> reject;
5. store has extra module -> reject;
6. failed coordinator construction не мутирует private store и не расходует `CommitId`;
7. normal public/private commit semantics после correction не регрессируют.

После correction выполнить targeted verification и полный `FULL-C0`.
