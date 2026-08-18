# Исследовательский журнал MINDRA

## Назначение

Этот каталог хранит датированные literature/research/tool pass, будущие hypotheses, experiments, results, verification evidence и claim-review evidence.

Каноническая архитектура живёт в `docs/design/`; research evidence само по себе design не меняет.

---

# Текущая структура

```text
research/
├── README.md
├── literature/
│   ├── DU-10-cortex-landscape-2026-08.md
│   ├── ...
│   ├── DU-30-research-claims-limitations-landscape-2026-08.md
│   └── DU-32-version-roadmap-landscape-2026-08.md
├── hypotheses.md          # появится позже
├── experiments/           # появится позже
├── results/               # появится позже
├── verification/          # появится позже
└── claims/                # physical layout определится version design
```

---

# Literature / tool research pass

Датированные pass находятся в [`literature/`](literature/).

Последние существенные:

- `DU-28` — reliable evaluation/statistics/calibration/matched controls;
- `DU-29` — property/state-machine testing, architecture checks, flaky/determinism guidance;
- `DU-30` — research reporting, null/negative evidence, claim scope и consciousness-overclaim boundaries;
- [`literature/DU-32-version-roadmap-landscape-2026-08.md`](literature/DU-32-version-roadmap-landscape-2026-08.md) — hosted notebook/Colab compute variability, limited-memory training и PEFT candidates для roadmap.

Эти документы **не выбирают** canonical implementation framework/algorithm/tool.

---

# Research discipline

```text
research evidence / experiment result
→ Observation / Interpretation / ResearchClaim review
→ design review
→ ADR при semantic change
→ canonical design/freeze update
→ roadmap/version update
→ implementation
```

Engineering evidence хранится отдельно от research evidence:

```text
contract/invariant test passed
≠
mechanism functionally useful
```

Research reporting chain:

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

Любой substantial research result связывается с конкретными commit/config/checkpoint/restore profile/Agent revision/Environment distribution/evaluation condition/raw artifacts/data/training refs/software/hardware/compute manifests/metric+analysis revisions/limitations.

Engineering verification result связывается минимум с repository revision, test spec, environment profile и VerificationObligation refs.

Отрицательные/null/inconclusive results сохраняются; invalid/not-measured не смешиваются с negative evidence.

Failed module gate инициирует ClaimReview/design review; architecture меняется только через ADR.

---

# Roadmap research discipline

После `DU-32` внешний tooling landscape перепроверяется **перед той software version, где choice реально становится implementation dependency**.

Например:

- перед `v0.1` — Python/runtime/testing/packaging stack;
- перед `v0.2` — Environment/MicroWorld tooling;
- перед `v0.3` — актуальные small/open Cortex models и inference backends;
- перед `v0.10` — training/PEFT/quantization/accelerator stack;
- перед `v0.11` — актуальный evaluation/statistics/tracking tooling.

Roadmap специально не фиксирует быстро меняющиеся concrete tools заранее.

---

# Текущий статус

Общий architecture/roadmap design `DU-00 … DU-32` завершён.

Следующий этап — `Version Design v0.1 Core Kernel`.

Experiment/hypothesis/claim registry implementation ещё не создан; журнал пока используется в основном для датированных research/tool pass и не смешивается с canonical design.
