# Candidate contract Action Boundary / Gate / Executor MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-24 — Action Boundary / Gate / Executor`

Этот документ уточняет machine-facing semantic формы accepted design [`../modules/action-boundary.md`](../modules/action-boundary.md).

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC/dataclass/TensorDict/Pydantic;
- concrete Environment action enum/schema;
- exact constraint language;
- конкретный safety shield/runtime assurance algorithm;
- ROS/gRPC/HTTP transport;
- retry framework;
- timeout values;
- exact cancellation state machine;
- checkpoint encoding.

---

# 1. Каноническая форма

```text
SelectedActionIntent
        ↓
ActionAuthorizationRequest
        ↓
Action Gate / Authorization Chain
        ↓
ActionAuthorizationResult
        ├── rejection
        └── AuthorizedAction
                ↓
          ActionCommitRecord
                ↓
            DispatchAttempt
                ↓
      EnvironmentActionReceipt?
                ↓
      execution / transition evidence
                ↓
            Outcome Commit
```

---

# 2. ActionBoundaryDescriptor

```text
ActionBoundaryDescriptor
├── boundary_id
├── boundary_revision
├── gate_revision
├── action interface revision
├── supported validation stages
├── normalization capability
├── override capability
├── constraint-source descriptors
├── dispatch capability descriptor ref
├── snapshot capability
├── intervention capability
└── provenance
```

---

# 3. ActionAuthorizationRequest

```text
ActionAuthorizationRequest
├── request_id
├── selected_intent_ref
├── base state_revision
├── current state_revision
├── decision_id
├── episode_id
├── agent_revision
├── policy_revision
├── action capability descriptor ref/revision
├── action interface revision
├── explicit precondition refs[]
├── explicit constraint-set refs[]
├── lifecycle status
└── provenance
```

Request не содержит hidden Environment Ground Truth normal runtime способом.

---

# 4. ActionConstraintSet

```text
ActionConstraintSet
├── constraint_set_id
├── constraint_set_revision
├── owner / trust boundary
├── agent-visible status
├── scope
├── rule/constraint descriptors[]
├── applicable action families
├── validity/freshness metadata
└── provenance
```

Constraint source conceptually может быть:

```text
action_interface
agent_visible_task
capability
runtime_assurance
research_intervention
```

Evaluator-only labels/test answers не являются normal constraint source.

---

# 5. AuthorizationStageRecord

```text
AuthorizationStageRecord
├── stage_record_id
├── stage_kind
├── stage_owner/revision
├── input action ref
├── base/current revision refs
├── status
├── reason code / structured evidence
├── normalization output ref?
├── override proposal ref?
└── provenance
```

Stage status semantic classes должны позволять различить минимум:

```text
accepted
rejected
stale
malformed
capability_unavailable
precondition_failed
precondition_unknown
constraint_violation
internal_failure
```

Exact enum не frozen.

---

# 6. ActionNormalizationRecord

```text
ActionNormalizationRecord
├── normalization_id
├── input action ref
├── output action ref
├── transformation kind/revision
├── semantics-preserving assertion/evidence
├── unit/encoding/interface metadata
└── provenance
```

Normalization не должна менять behavioral intent.

---

# 7. ActionOverrideRecord

```text
ActionOverrideRecord
├── override_id
├── original selected_intent_ref
├── original semantic action ref
├── replacement semantic action
├── override policy identity/revision
├── owner/trust boundary
├── triggering constraint/evidence refs[]
├── reason
├── agent-visible status
├── intervention/deployment provenance
└── provenance
```

Behavior-changing replacement без `ActionOverrideRecord` запрещён.

---

# 8. ActionAuthorizationResult

```text
ActionAuthorizationResult
├── authorization_result_id
├── request_ref
├── overall status
├── stage_records[]
├── rejection record?
├── normalized action ref?
├── override record?
├── authorized_action?
├── gate revision
├── constraint revisions
└── provenance
```

`overall status` conceptually различает:

```text
authorized
rejected
stale
blocked
failed
```

---

# 9. ActionRejection

```text
ActionRejection
├── rejection_id
├── selected_intent_ref
├── rejection_class
├── reason/evidence refs[]
├── recoverability hint?
├── requires_reselection?
├── current state/action-interface refs
└── provenance
```

Rejection не является Environment Outcome.

---

# 10. AuthorizedAction

```text
AuthorizedAction
├── authorized_action_id
├── selected_intent_ref
├── final semantic action
├── base/current state_revision refs
├── decision_id
├── episode_id
├── agent_revision
├── policy_revision
├── gate revision
├── action interface revision
├── normalization refs[]
├── override ref?
├── authorization stage refs[]
├── constraint revisions[]
├── availability/freshness
└── provenance
```

До `Action Commit` может стать invalid/stale и не должен отправляться.

---

# 11. ActionCommitRecord

```text
ActionCommitRecord
├── action_commit_id
├── authorized_action_ref
├── selected_intent_ref
├── committed semantic action
├── decision_id
├── episode_id
├── state_revision_at_commit
├── agent_revision
├── policy_revision
├── gate/constraint revisions
├── action interface revision
├── normalization/override lineage
├── dispatch_id
├── logical commit identity/time
└── provenance
```

После создания `ActionCommitRecord` semantic action immutable для данного `Decision Window`.

---

# 12. DispatchCapabilityDescriptor

```text
DispatchCapabilityDescriptor
├── adapter_id
├── adapter_revision
├── environment interface revision
├── synchronous/asynchronous capability
├── acknowledgement capability
├── execution-status capability
├── cancellation capability
├── dedup/idempotency capability
├── retry capability
├── reconciliation capability
└── provenance
```

Dedup/idempotency semantics должны быть explicit, а не inferred из transport name.

---

# 13. DispatchAttempt

```text
DispatchAttempt
├── dispatch_attempt_id
├── dispatch_id
├── action_commit_ref
├── attempt_index
├── adapter/provider revision
├── payload/encoding revision
├── start evidence
├── transport result
├── acknowledgement ref?
├── definitely_sent / definitely_not_sent / unknown?
├── failure reason?
└── provenance
```

Повторный attempt того же logical dispatch использует тот же `dispatch_id`.

---

# 14. EnvironmentActionReceipt

```text
EnvironmentActionReceipt
├── receipt_id
├── action_commit_ref
├── dispatch_id
├── environment action/execution handle?
├── acceptance state
├── environment/interface revision
├── received evidence
└── provenance
```

`accepted` не означает `completed`/`succeeded`.

---

# 15. ActionExecutionRecord

```text
ActionExecutionRecord
├── execution_record_id
├── action_commit_ref
├── dispatch_id
├── environment execution handle?
├── execution status
├── effect/transition refs[]?
├── partial-effect evidence?
├── cancellation/preemption refs[]?
├── failure/unknown reason?
└── provenance
```

Semantic classes должны позволять различить как минимум:

```text
not_started
accepted
executing
completed
no_effect
partial
aborted
cancelled
rejected
unknown
```

Exact enum/environment mapping не frozen.

---

# 16. DispatchReconciliationRecord

```text
DispatchReconciliationRecord
├── reconciliation_id
├── action_commit_ref
├── dispatch_id
├── previous unknown state
├── evidence queried/received
├── resolved execution status?
├── retry safety result
├── recovery disposition
└── provenance
```

`execution_unknown` не разрешает silent automatic retry.

---

# 17. Cancellation / preemption record

Если environment поддерживает long-running action control:

```text
ActionExecutionControlRecord
├── control_id
├── target execution/action_commit ref
├── command kind
├── source/owner
├── authorization/provenance
├── acceptance/result
└── causal refs
```

Cancellation после Action Commit не удаляет исходный commit.

---

# 18. ActionBoundarySnapshot

```text
ActionBoundarySnapshot
├── boundary/gate revisions
├── pending authorization state?
├── committed-but-not-resolved actions[]
├── dispatch identities
├── dispatch attempts
├── acknowledgement/execution state
├── dedup/reconciliation state
├── constraint-set revisions
├── adapter/interface revisions
├── causally relevant RNG/private state?
└── intervention/degradation state
```

Snapshot Agent без согласованного Environment/external execution state не гарантирует exact rollback внешнего мира.

---

# 19. Observability invariants

Trace должен поддерживать join chain:

```text
candidate_id
→ selected_intent_id
→ authorization_result_id
→ authorized_action_id
→ action_commit_id
→ dispatch_id / dispatch_attempt_id
→ receipt/execution identity
→ environment_transition_id
→ outcome identity
```

Override chain:

```text
selected_intent A
→ override record
→ committed action B
```

обязательна.

---

# 20. Contract invariants

Будущий implementation должен автоматически проверять, где возможно:

1. rejected/stale/malformed intent не получает `ActionCommitRecord`;
2. один Decision Window имеет не более одного normal committed external action;
3. `ActionCommitRecord` ссылается на successfully authorized action;
4. post-commit semantic action не меняется;
5. behavior-changing substitution имеет explicit override provenance;
6. retry не создаёт новый Action Commit;
7. retry того же logical dispatch использует тот же `dispatch_id`;
8. non-idempotent/unknown execution не retry'ится молча;
9. receipt `accepted` не интерпретируется как success;
10. partial/no-effect/transport failure различаются;
11. terminal outcome сохраняется до reset;
12. hidden evaluator truth не является normal authorization input;
13. provider-specific payload не протекает обратно в Policy contract.

---

# 21. Что не frozen

До общего contract freeze не каноничны:

```text
ActionKind enum
status enums
constraint DSL
normalization implementation
shield/RTA implementation
idempotency token format
transport protocol
async runtime library
retry count/backoff
cancellation API
exact timeout values
Python types
```
