# DU-32 — Version Roadmap: compute/tooling landscape, 2026-08

## Статус

Датированный research/tool pass для `DU-32 — Version Roadmap`.

Этот документ **не является canonical architecture**. Он фиксирует внешние engineering facts/candidates, которые использовались для проверки реалистичности roadmap на ограниченном compute.

Canonical owner roadmap: `docs/design/version-roadmap.md`.

---

# 1. Главный вывод

Roadmap должен предполагать:

- CPU-only deterministic core;
- optional consumer GPU для небольшого inference/training;
- hosted notebook accelerator как burst compute, а не guaranteed hardware contract;
- parameter-efficient training как candidate поздних milestones;
- checkpoint/resume до тяжёлых training/evaluation runs;
- сменность concrete model/provider.

Ни один конкретный GPU, model family, PEFT implementation или notebook service не становится F31/roadmap architecture invariant.

---

# 2. Google Colab / hosted notebook compute

Источник:

- Google Colab FAQ — https://research.google.com/colaboratory/faq.html

Актуальные operational facts:

- Colab предоставляет hosted notebook environment с optional GPU/TPU;
- resources и usage limits не гарантированы и могут меняться;
- доступные GPU/TPU types меняются со временем;
- runtime lifetime/idle behavior зависит от tier, availability и usage;
- для гарантированного specific hardware Google предлагает отдельные dedicated/GCP варианты.

Engineering consequence для MINDRA:

```text
Colab GPU
≠
fixed deployment contract
```

Поэтому training/evaluation milestone должен:

- обнаруживать device/capabilities в runtime;
- не hardcode'ить конкретную GPU model;
- сохранять checkpoints;
- уметь resume после interruption;
- записывать actual hardware/compute provenance;
- иметь CPU/control smoke path независимо от hosted GPU.

---

# 3. Parameter-efficient fine-tuning

Источники:

- Hugging Face PEFT LoRA guide — https://huggingface.co/docs/peft/main/conceptual_guides/lora
- Hugging Face PEFT Memory Efficient Training — https://huggingface.co/docs/peft/main/developer_guides/memory_efficient_training
- Transformers PEFT integration — https://huggingface.co/docs/transformers/main/peft

Актуальные engineering observations:

- LoRA/adapter methods обучают небольшое количество дополнительных parameters при frozen base weights;
- это уменьшает gradient/optimizer-state memory относительно full fine-tuning;
- adapters удобно version/activate отдельно от base model;
- memory всё равно зависит от base weights, activations, batch/sequence length и dtype;
- меньшая base model/shorter sequence/smaller batch остаются базовыми способами уменьшить memory.

Это хорошо совместимо с F31 `CandidateRevisionBundle` и replaceable Cortex boundary.

Но roadmap не принимает:

```text
LoRA mandatory
QLoRA mandatory
Transformers mandatory
PEFT library mandatory
```

как architecture choice.

Они являются сильными candidates для `v0.10` version design на ограниченном GPU.

---

# 4. Почему first learned target не обязан быть Cortex

Даже при PEFT Cortex остаётся наиболее тяжёлым и confounded target.

Для первого Training Runtime experiment дешевле и диагностируемее может быть:

- небольшой World Model predictor;
- competence/Self Model predictor;
- compact Policy/Valuation model;
- небольшой adapter provider.

Это позволяет сначала доказать:

```text
Dataset lineage
→ TrainingPlan
→ candidate revision
→ validation
→ activation
```

без одновременной проверки всей LLM fine-tuning stack.

После lifecycle verification Cortex adapter training можно добавить как отдельный profile.

---

# 5. Approximate memory reasoning

PEFT documentation приводит полезный порядок величин: сами weights модели масштаба ~1B в fp16 занимают порядка нескольких GiB, а full training добавляет gradients, optimizer state и activation memory.

Следствие для consumer GPU class:

- raw parameter count сам по себе недостаточен для ответа «поместится ли training»;
- inference и full training имеют принципиально разные memory profiles;
- early roadmap не должен зависеть от full fine-tuning даже относительно небольшой LLM;
- exact batch/sequence/dtype/quantization/adaptor strategy выбираются только после измерений конкретной версии.

---

# 6. Candidate tooling classes для будущих version designs

Ниже не frozen choices, а области, которые можно исследовать отдельно при проектировании соответствующих milestones.

## Runtime/contracts

- стандартный Python object model;
- dataclass/Pydantic/TypedDict/Tensor-oriented containers;
- explicit dependency injection/composition factories.

## Environment

- custom deterministic MicroWorld;
- Gymnasium-compatible adapter как возможная interoperability layer.

## Neural/Cortex

- PyTorch ecosystem;
- Transformers-compatible local models;
- remote model adapters;
- quantized inference where supported.

## Training

- plain PyTorch training loop;
- PEFT/adapters;
- higher-level trainers только если они не скрывают F31 lifecycle.

## Storage/checkpoint

- content-addressed local artifacts;
- structured manifest + tensor/data files;
- concrete format выбирается после v0.4/v0.10 requirements.

## Testing

- example/unit/integration tests;
- property/state-machine testing;
- architecture/import rules;
- fault injection;
- exact tool selection — version-level.

---

# 7. Roadmap implications

External tooling landscape поддерживает следующие DU-32 choices:

1. `v0.1/v0.2` обязаны работать CPU-only.
2. Real Cortex можно подключить уже `v0.3`, но он optional.
3. Hosted notebook/Colab рассматривается как burst compute, не как fixed platform.
4. Checkpoint/restore появляется до тяжёлого training.
5. Full neural training отложен до `v0.10`.
6. Первый trainable target может быть существенно меньше Cortex.
7. PEFT является preferred research candidate, но не roadmap invariant.
8. `v1.0` engineering completeness не зависит от одного конкретного GPU/provider.

---

# 8. Что намеренно не исследовано/не frozen в DU-32

Roadmap не выбирает:

- конкретную Python minor version;
- package manager;
- PyTorch vs JAX;
- конкретную small LLM;
- quantization backend;
- exact PEFT method;
- concrete database/vector index;
- exact CI provider;
- exact experiment tracker;
- конкретные Colab subscription limits;
- универсальный VRAM threshold.

Эти choices быстро меняются и должны исследоваться датированно перед соответствующим version design.
