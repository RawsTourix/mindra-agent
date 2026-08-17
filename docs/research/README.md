# Исследовательский журнал MINDRA

## Назначение

Этот каталог хранит датированные literature/research pass, будущие hypotheses, experiments, results, verification evidence и claim-review evidence.

Каноническая архитектура живёт в `docs/design/`; research evidence само по себе design не меняет.

---

# Текущая структура

```text
research/
├── README.md
├── literature/
│   ├── DU-10-cortex-landscape-2026-08.md
│   ├── ...
│   ├── DU-28-mindra-eval-landscape-2026-08.md
│   ├── DU-29-engineering-testing-landscape-2026-08.md
│   └── DU-30-research-claims-limitations-landscape-2026-08.md
├── hypotheses.md          # появится позже
├── experiments/           # появится позже
├── results/               # появится позже
├── verification/          # появится позже
└── claims/                # physical layout определится позже
```

---

# Literature / tool research pass

Текущие pass `DU-10 … DU-30` находятся в [`literature/`](literature/).

Последние:

- [`literature/DU-28-mindra-eval-landscape-2026-08.md`](literature/DU-28-mindra-eval-landscape-2026-08.md) — reliable evaluation/statistics/calibration/matched-control evidence;
- [`literature/DU-29-engineering-testing-landscape-2026-08.md`](literature/DU-29-engineering-testing-landscape-2026-08.md) — property/state-machine testing, architecture dependency checks, flaky/determinism guidance и engineering-verification implications;
- [`literature/DU-30-research-claims-limitations-landscape-2026-08.md`](literature/DU-30-research-claims-limitations-landscape-2026-08.md) — research reporting, reproducibility/replication, uncertainty/null evidence, claim scope и consciousness-overclaim boundaries.

Эти документы **не выбирают** canonical implementation framework/algorithm/tool.

---

# Research discipline

Правильный путь изменения архитектуры:

```text
research evidence / experiment result
→ Observation / Interpretation / ResearchClaim review
→ design review
→ ADR при существенном выборе
→ canonical design update
→ implementation/version update
```

Для future confirmatory experiments действуют requirements `DU-28`.

Engineering evidence `DU-29` хранится отдельно от research evidence:

```text
contract/invariant test passed
≠
mechanism functionally useful
```

После `DU-30` future substantial research result должен также быть связан с canonical claim/limitation semantics:

```text
Evaluation/Verification evidence
→ ObservationRecord
→ InterpretationRecord
→ ResearchClaim + ClaimScope
→ Limitations / KnownUnknowns
→ ClaimReview / supersession
```

Publication/report prose не является source of truth claim.

---

# Результаты

Любой research result должен быть связан с конкретными commit/config/checkpoint/restore profile/agent revision/environment distribution/evaluation condition/raw artifacts/data/training refs/software/hardware/compute manifests/metric+analysis revisions/limitations.

Любой engineering verification result должен быть связан минимум с repository revision, test spec, relevant environment profile и obligation refs.

Отрицательные/null/inconclusive results сохраняются; invalid/not-measured не смешиваются с отрицательным evidence.

Failed module gate инициирует ClaimReview/design review; architecture меняется только через ADR.

---

# Claims / limitations discipline

До появления physical registry implementation действуют canonical contracts `DU-30`:

- claim имеет stable identity/revision;
- scope обязателен;
- supporting и challenging evidence сосуществуют;
- limitations и known unknowns first-class;
- claim можно weaken/narrow/supersede без history rewrite;
- causal/generalization/architecture claims не расширяются сильнее evidence;
- functional similarity не считается evidence phenomenological equivalence;
- `Self Model`, Affect, Workspace и Cortex self-report не доказывают consciousness/subjective experience автоматически.

---

# Текущий статус

Experiment/hypothesis/claim registry implementation ещё не создан. Сейчас журнал используется в основном для датированных research/tool pass и не должен смешиваться с canonical design.
