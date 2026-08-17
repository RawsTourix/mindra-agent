# Candidate contract Policy / Planner MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-23 — Policy / Planner`

Этот документ уточняет machine-facing semantic формы accepted design [`../modules/policy-planner.md`](../modules/policy-planner.md).

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC/dataclass/TensorDict/Pydantic;
- конкретную Policy neural architecture;
- конкретный Planner algorithm;
- MCTS/MPC/beam search/ToT;
- action-space encoding;
- exact value scalarization;
- exact stochastic distribution;
- training algorithm/loss;
- checkpoint encoding.

---

# 1. Каноническая форма

```text
BehavioralContext
        +
CandidateGenerationRequest
        ↓
ActionCandidate / PlanCandidate providers
        ↓
PolicyCandidateSet
        +
Valuation / Comparison evidence
        ↓
PolicySelectionRequest
        ↓
PolicySelectionResult
        ├── SelectedActionIntent
        └── DecisionDeferral
```

Planner path:

```text
PlanningRequest
        ↓
Planner
        ↓
PlanCandidate / PlannerActionCandidate
        ↓
PolicyCandidateSet
```

---

# 2. PolicySystemDescriptor

```text
PolicySystemDescriptor
├── system_id
├── system_revision
├── policy_revision
├── candidate-generation capabilities
├── selection capabilities
├── stochastic capability
├── recurrent/stateful capability
├── Planner-consumer capability
├── ValueProfile/Comparison consumer capability
├── snapshot capability
├── supported fallback modes
└── provenance
```

---

# 3. PlannerSystemDescriptor

```text
PlannerSystemDescriptor
├── planner_id
├── planner_revision
├── supported plan kinds
├── supported search/rollout capabilities
├── supported World Model query kinds
├── Cortex-assisted capability
├── contingent-plan capability
├── persistent-plan capability
├── subgoal-proposal capability
├── stochastic capability
├── snapshot capability
└── provenance
```

`PlannerSystemDescriptor` не содержит live provider objects.

---

# 4. BehavioralContext

```text
BehavioralContext
├── context_id
├── base state_revision
├── decision_id
├── agent_revision
├── committed Goal refs
├── GoalFocusDirective ref?
├── WorldBelief ref/summary
├── Self evidence refs?
├── Workspace ref/projection?
├── explicit RetrievalResult refs[]?
├── Drive/Affect/Appraisal refs?
├── Valuation context refs?
├── action capability descriptor ref
├── Executive disposition/budget refs?
├── degraded/unavailable capability states
└── provenance
```

Это declared read projection, не ambient dump `CognitiveState`.

---

# 5. ActionCapabilityDescriptor

До `DU-24` точный action schema не frozen, но Policy должна видеть только agent-visible допустимую semantic surface действий.

```text
ActionCapabilityDescriptor
├── descriptor_id
├── descriptor_revision
├── action families / semantic kinds
├── parameter-domain descriptors
├── capability availability
├── known agent-visible constraints
├── interface revision
└── provenance
```

Он не содержит hidden Environment Ground Truth или evaluator-only validation.

---

# 6. ActionCandidate

```text
ActionCandidate
├── candidate_id
├── candidate_revision
├── action semantic proposal/ref
├── source identity/revision
├── base state_revision
├── decision_id
├── agent_revision
├── Goal refs[]
├── assumptions/preconditions[]?
├── WorldPrediction / ImaginedTrajectory refs[]?
├── Plan ref?
├── Self feasibility refs?
├── ValueProfile refs[]?
├── Comparison refs[]?
├── Risk/Constraint refs[]?
├── confidence/support?
├── source mode
├── branch lineage
├── intervention/degradation provenance
└── provenance
```

Source mode conceptually может различать:

```text
reactive_policy
planner
cortex_assisted
scripted_control
hierarchical_subpolicy
research_intervention
```

---

# 7. PolicyCandidateSet

```text
PolicyCandidateSet
├── candidate_set_id
├── candidate_set_revision
├── base state_revision
├── decision_id
├── candidates[]
├── source descriptors[]
├── dedup/equivalence metadata?
├── candidate-generation coverage state?
├── missing/unavailable sources
└── provenance
```

Candidate set после создания semantically immutable; изменение состава создаёт новую revision/set.

---

# 8. CandidateGenerationRequest

```text
CandidateGenerationRequest
├── request_id
├── context ref
├── requested source kinds
├── Goal refs
├── action capability ref
├── generation constraints?
├── desired candidate diversity/coverage?
├── resource/budget refs
├── lifecycle phase
└── provenance
```

Concrete candidate-generation algorithm не frozen.

---

# 9. PlanningRequest

```text
PlanningRequest
├── request_id
├── base state_revision
├── decision_id
├── Goal refs
├── WorldBelief ref
├── allowed context refs
├── action capability ref
├── planning purpose
├── requested horizon semantics?
├── requested branch/search budget?
├── constraints/risk context refs?
├── current PlanState ref?
├── ExecutiveDecision / MetaAction ref
├── branch mode
└── provenance
```

Planning request normal runtime способом должен быть разрешён соответствующей Executive/meta-action boundary, если planning является optional compute.

---

# 10. PlanNode / PlanStep

Conceptually:

```text
PlanNode
├── node_id
├── action candidate ref?
├── subgoal proposal ref?
├── observation/belief condition?
├── predicted outcome refs[]
├── child/contingency refs[]
├── Value/Comparison refs[]?
├── assumptions
├── terminal/continuation semantics
└── provenance
```

Plan node не является Environment transition.

---

# 11. PlanCandidate

```text
PlanCandidate
├── plan_id
├── plan_revision
├── planner_revision
├── root Goal refs
├── base state_revision
├── base belief_revision
├── nodes/steps refs
├── root action candidate refs[]
├── contingency structure
├── horizon semantics
├── assumptions[]
├── validity/invalidation rules
├── WorldPrediction/ImaginedTrajectory refs[]
├── Value/Comparison refs[]
├── Self feasibility refs[]?
├── Cortex evidence refs[]?
├── branch provenance
└── provenance
```

`PlanCandidate` не означает adoption Policy.

---

# 12. PlanState

Если Planner поддерживает persistent planning:

```text
PlanState
├── plan_state_id
├── plan_state_revision
├── active Plan ref?
├── validity state
├── base/current revision refs
├── completed/remaining node refs
├── pending contingencies
├── invalidation evidence
├── replan status
├── private search-state descriptor?
└── provenance
```

Validity states должны уметь выразить минимум semantically:

```text
valid
stale
partially_applicable
invalidated
unknown
unavailable
```

Точные enum names не frozen.

---

# 13. PlannerSearchEvidence

Для observability, если Planner использует search:

```text
PlannerSearchEvidence
├── search_id
├── planning request ref
├── planner revision
├── budget granted/consumed
├── expanded branch/node identities
├── World Model rollout refs[]
├── candidate/pruning evidence
├── Value/Comparison refs[]
├── stopping reason
└── provenance
```

Raw search tree может быть private artifact; contract требует causal summary/evidence, а не обязательный universal tree format.

---

# 14. PolicySelectionRequest

```text
PolicySelectionRequest
├── request_id
├── BehavioralContext ref
├── PolicyCandidateSet ref
├── ValueProfile refs[]
├── ComparisonResult refs[]
├── constraints/risk refs[]
├── current Plan ref?
├── selection policy revision
├── stochastic configuration ref?
├── fallback configuration ref
└── provenance
```

---

# 15. PolicySelectionResult

Union-like semantic result:

```text
PolicySelectionResult
├── result_id
├── base state_revision
├── decision_id
├── policy revision
├── status
├── SelectedActionIntent?
├── DecisionDeferral?
├── fallback/degradation metadata?
└── provenance
```

---

# 16. SelectedActionIntent

```text
SelectedActionIntent
├── intent_id
├── intent_revision
├── decision_id
├── base state_revision
├── agent_revision
├── selected candidate ref
├── action semantic proposal/ref
├── PolicyCandidateSet ref
├── policy revision
├── supporting Plan ref?
├── Goal refs[]
├── Value/Comparison refs[]?
├── Risk/Constraint refs[]?
├── stochastic selection evidence?
├── RNG ref/state identity?
├── intervention/degradation provenance
└── status
```

`SelectedActionIntent` не является `Action Commit` и не сообщает, что действие прошло `DU-24` gate.

---

# 17. DecisionDeferral

```text
DecisionDeferral
├── deferral_id
├── decision_id
├── base state_revision
├── reason
├── unresolved candidate refs[]?
├── unresolved Comparison refs[]?
├── required evidence kinds[]?
├── MetaActionProposal refs[]?
├── budget/resource state ref
├── fallback if no more cognition?
└── provenance
```

Reason semantics должны позволять различать минимум:

```text
insufficient_decision_evidence
incomparable_candidates
constraint_conflict
candidate_generation_incomplete
planner_required
valuation_required
capability_unavailable
resource_exhausted
policy_failure
```

Точные identifiers не frozen.

---

# 18. StochasticSelectionEvidence

Если Policy stochastic:

```text
StochasticSelectionEvidence
├── policy distribution/logit/ranking ref?
├── candidate support set
├── temperature/exploration config revision?
├── RNG identity/state ref
├── sampled candidate ref
└── provenance
```

Не требуется раскрывать backend-specific logits, если implementation их не предоставляет; но stochasticity должна быть причинно идентифицируема.

---

# 19. SubgoalProposalLink

Planner-generated subgoal остаётся обычным Goal Proposal.

Contract может хранить link:

```text
PlannerSubgoalLink
├── plan ref
├── GoalProposal ref
├── Goal System resolution ref?
├── dependency node refs
└── provenance
```

Planner не мутирует committed Goal Graph.

---

# 20. PolicyPlannerSnapshot

Conceptually:

```text
PolicyPlannerSnapshot
├── policy descriptor/revision
├── policy private causally relevant state
├── policy RNG state
├── planner descriptor/revision
├── active PlanState
├── planner private/search state
├── planner RNG state
├── pending candidate/deferral state
├── compatibility manifests
├── intervention/degradation state
└── provenance
```

Если concrete implementation stateless, соответствующие поля отсутствуют по contract, а не заполняются dummy values.

---

# 21. Failure semantics

Contract должен различать:

- unavailable Planner;
- exhausted planning budget;
- stale plan;
- invalid candidate set;
- no candidates;
- all candidates constraint-rejected;
- incomparability;
- missing Value/Comparison evidence;
- stale World/Self evidence;
- Policy backend failure;
- stochastic-selection failure;
- incompatible action capability revision;
- Cortex/World Model degradation используемого candidate source.

Failure не маскируется implicit random action.

---

# 22. Invariants для будущих tests

Автоматически/полуавтоматически проверять, где применимо:

```text
Planner cannot create SelectedActionIntent directly
Policy cannot execute Environment action
WorldPrediction cannot be aliased to Plan
Plan cannot reference hidden Environment state normal runtime способом
Planner subgoal cannot mutate Goal Graph
DecisionDeferral cannot recursively invoke Executive directly
SelectedActionIntent must reference committed base revision
stale candidate set cannot be silently rebased
stochastic selection must preserve RNG/provenance semantics
imagined candidate/plan provenance cannot become observed
```

---

# 23. Не frozen до Contract Freeze

Пока не каноничны:

- exact class names;
- exact action encoding;
- number of candidates;
- plan graph/tree/list representation;
- search algorithm;
- Planner neural architecture;
- Policy neural architecture;
- MCTS/MPC/ToT/beam search;
- explicit scalar score;
- exact stochastic distribution;
- tie-breaking algorithm;
- replanning frequency;
- plan horizon;
- concrete Cortex prompt;
- training objectives.
