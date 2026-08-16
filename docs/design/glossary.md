# Глоссарий MINDRA

## Назначение

Этот документ фиксирует рабочие значения основных терминов проекта.

Термины могут уточняться вместе с canonical design, но одно слово не должно одновременно использоваться для нескольких существенно разных механизмов без явного пояснения.

---

# Agent

Логическая когнитивная система MINDRA, которая владеет внутренним состоянием, использует свои cognitive capabilities и выбирает действия при взаимодействии с Environment.

Agent не равен Cortex, не равен одной neural network и не равен process/VM/GPU, в котором исполняется.

Каноническая system boundary определена в `system-context.md`.

---

# Agent boundary

Логическая граница ответственности, отделяющая когнитивную систему MINDRA и agent-owned state от Environment, training/evaluation infrastructure, experiment control plane и compute/storage infrastructure.

Agent boundary не обязана совпадать с process/device/network boundary.

---

# Environment

Внешняя по отношению к Agent система динамики мира, которая принимает actions и возвращает contract-defined observations, внешние task signals и сведения о завершении/ограничении episode.

Hidden Environment state не является автоматически доступным Agent.

---

# Logical boundary

Граница, определяемая responsibility и state ownership, а не физическим размещением кода.

В MINDRA logical boundary имеет приоритет над deployment topology при описании canonical architecture.

---

# Deployment topology

Физическая схема размещения компонентов по process/thread/worker/device/machine/provider boundaries.

Deployment topology не определяет architecture semantics, если это отдельно не зафиксировано canonical design.

---

# Execution Runtime

Внешняя инфраструктурная роль, которая хостит исполнение Agent, соединяет его с Environment и обеспечивает run-level lifecycle, не являясь когнитивным модулем.

---

# Training Runtime

Внешняя по отношению к Agent инфраструктура обучения, которая работает с опытом, datasets, losses, optimizer state и обновляет agent-owned trainable state через явную update boundary.

Training Runtime не становится частью cognition только потому, что меняет параметры Agent.

---

# Evaluation Runtime

Внешняя исследовательская инфраструктура, которая запускает controlled evaluation, interventions и измерения поведения Agent.

Evaluation-derived information по умолчанию не является agent-visible input.

---

# Experiment Runner

Внешний control-plane компонент, задающий идентичность и конфигурацию исследовательского запуска, seed, режим выполнения и orchestration runtime components.

Experiment metadata не должна скрыто влиять на cognition Agent.

---

# Artifact Collector

Пассивная исследовательская инфраструктура, собирающая logs, trajectories, metrics, snapshots, checkpoints и другие evidence/artifacts.

Artifact Collector не должен быть источником normal decision signals Agent.

---

# Artifact Storage

Внешнее долговечное хранилище checkpoints, trajectories, logs, experiment manifests и других research/training artifacts.

Artifact Storage не является синонимом активной Memory Agent.

---

# Compute Substrate

Физические вычислительные ресурсы, на которых размещаются логические компоненты: CPU/GPU, process, VM, local machine, notebook runtime, remote host или future distributed infrastructure.

Compute Substrate не является когнитивной архитектурой.

---

# Research Control Plane

Внешняя область orchestration и experiment integrity, включающая researcher/operator, Experiment Runner, Evaluation Runtime и evidence pipeline.

Она управляет постановкой эксперимента, но не должна скрыто решать задачи за Agent.

---

# Agent-owned state

Состояние, которое семантически принадлежит Agent независимо от физического места хранения.

К нему могут относиться runtime internal state, активная Memory, trainable parameters и Cortex integration state после принятия соответствующих module contracts.

---

# Cortex

Заменяемая pretrained capability внутри логической границы Agent, предоставляющая богатые языковые, семантические и/или reasoning capabilities.

Cortex может быть LLM, но MINDRA не должна зависеть от конкретной модели.

Физический backend может исполняться вне основного process/machine boundary.

---

# Cortex backend

Конкретная реализация Cortex capability.

Примеры конкретных моделей пока не являются частью canonical design.

---

# Cortex Execution Provider

Внешний физический runtime/provider, который исполняет Cortex backend, когда вычисление вынесено за основной deployment boundary.

Provider не становится отдельным когнитивным модулем MINDRA только из-за физического размещения.

---

# CognitiveState

Рабочее concept-название канонического внутреннего состояния/границы обмена данными между когнитивными модулями.

Точная структура, tensor representation и framework пока не определены.

---

# Module

Компонент с явной responsibility, входами, выходами, state/lifecycle и диагностической границей.

Модуль не обязан быть нейросетью.

---

# World Model

Механизм, прогнозирующий динамику среды и/или последствия действий.

---

# Self Model

Механизм, прогнозирующий или представляющий релевантные свойства самого агента: способности, uncertainty, competence, ограничения, cost и другие self-related variables, если они будут приняты design.

Self Model не означает автоматически self-awareness.

---

# Drive

Внутренняя динамическая переменная или механизм, который способен менять относительную ценность состояний/действий для агента.

Drive не является синонимом reward.

---

# Appraisal

Функциональный механизм оценки значения события/состояния относительно текущего контекста агента: целей, drives, памяти, прогнозов и других relevant variables.

Appraisal не является доказательством эмоции как субъективного переживания.

---

# Affect

Рабочий зонтичный термин для внутреннего функционального состояния, возникающего из appraisal и влияющего на другие процессы системы, если такой механизм будет принят.

Не использовать `affect` как автоматический синоним человеческого чувства.

---

# Salience

Оценка относительной значимости информации для последующего внимания, memory, replay, workspace или learning.

Полезность Salience должна проверяться эмпирически.

---

# Memory

Подсистема сохранения и восстановления информации из предыдущего опыта.

Если Memory является активной частью cognition, её содержимое относится к agent-owned state независимо от физического storage backend.

Конкретные типы памяти будут определены design.

---

# Working memory / working state

Краткоживущее состояние, доступное в текущем цикле обработки.

Не фиксируется как отдельный модуль до соответствующего design.

---

# Episodic memory

Память о конкретных эпизодах/переходах/событиях опыта с достаточным контекстом для последующего retrieval или replay.

---

# Consolidation

Процесс, при котором накопленный опыт используется для более долгосрочного изменения representations/weights/knowledge системы.

На уровне `DU-01` consolidation отделяется от live Environment interaction как потенциальная maintenance/training phase, но точная реализация и ownership пока не определены.

---

# Replay

Повторное использование ранее сохранённого опыта для обучения, оценки или consolidation.

---

# Workspace

Рабочее concept-название ограниченного интеграционного механизма, через который selected information может становиться доступной нескольким подсистемам.

Использование термина вдохновлено cognitive architectures, но не означает утверждение о сознании.

---

# Policy

Механизм выбора action из доступного состояния и контекста.

Policy может включать learned и algorithmic части в зависимости от будущего design.

---

# Planner

Механизм явного сравнения/построения последовательностей возможных действий, если он будет выделен отдельно от Policy/Cortex.

---

# Reward

Внешний или внутренний scalar/vector training signal, используемый конкретным learning algorithm.

Не использовать `reward` как универсальное название любого внутреннего значения.

---

# Extrinsic signal

Сигнал ценности/успеха, задаваемый внешней средой, задачей или evaluator.

Если сигнал существует только как evaluation metric и не входит в Environment/task contract, он не является автоматически agent-visible feedback.

---

# Intrinsic signal

Сигнал, вычисляемый из внутренней динамики агента или его взаимодействия со средой, например из novelty/prediction error, если соответствующий механизм принят.

Intrinsic signal не обязательно является scalar reward.

---

# Utility

Общее рабочее понятие для функциональной ценности состояния/действия относительно текущей системы целей и внутренних факторов.

Точная математическая форма пока не зафиксирована.

---

# Goal

Представление желаемого будущего состояния, результата или ограничения поведения, которое влияет на выбор действий.

Точный lifecycle целей пока не определён.

---

# Novelty

Степень новизны состояния/наблюдения относительно опыта или learned representation агента.

Способ вычисления определяется конкретным design.

---

# Surprise / prediction error

Расхождение между предсказанием модели и фактическим наблюдением/исходом.

Не считать surprise и novelty автоматически одним и тем же.

---

# Uncertainty

Оценка недостатка уверенности/информации в prediction, state estimate или decision.

Нужно отличать uncertainty от raw model entropy, если design вводит более точную семантику.

---

# Competence

Оценка способности агента успешно решать класс задач или выполнять действие.

Если используется, должна иметь измеримую связь с фактическими outcome.

---

# Functional subjectivity

Рабочий термин MINDRA для свойства, при котором внутренняя оценка и поведение зависят не только от внешней ситуации, но и от собственного состояния/истории конкретного агента.

Не означает phenomenal consciousness.

---

# Consciousness

Широкий научно-философский термин, который не используется в MINDRA как автоматически достигнутое свойство архитектуры.

Любое более конкретное использование должно указывать, о каком аспекте сознания идёт речь.

---

# Phenomenal consciousness

Наличие субъективного опыта — условного «как это ощущается изнутри».

MINDRA не предполагает, что функциональные механизмы сами по себе доказывают phenomenal consciousness.

---

# Self-reference

Способность системы ссылаться на себя в representation или языке.

Не равна Self Model и не равна self-awareness.

---

# Self-awareness / самосознание

Термин не должен использоваться как техническая характеристика MINDRA без отдельного операционального определения и evidence.

---

# Ablation

Эксперимент, в котором компонент удаляется, отключается или заменяется control-реализацией для оценки его вклада.

---

# Intervention

Контролируемое изменение internal variable/representation с последующим измерением причинного эффекта при максимально фиксированных остальных условиях.

Evaluator intervention является специальной experimental operation и не должно смешиваться с normal Agent input.

---

# Counterfactual experiment

Эксперимент со сравнимыми ветвями, полученными из одного сохранённого состояния, где меняется ограниченный набор факторов.

---

# Baseline

Сравнительная система/конфигурация, относительно которой оценивается новый механизм.

---

# Control

Конфигурация, предназначенная для исключения альтернативного объяснения эффекта: например, random/no-op/parameter-matched implementation.

---

# Architecture gain

Рабочее понятие для улучшения измеряемой способности при добавлении MINDRA architecture относительно выбранного baseline.

Точная метрика будет определена позже.

---

# Provenance

Информация о происхождении данных, state update, artifact, checkpoint, intervention или experiment result, достаточная для последующего понимания того, откуда он появился и при каких условиях.

Точная schema определяется будущими Design Updates.

---

# Research evidence

Фактические результаты воспроизводимого эксперимента вместе с его условиями и ограничениями.

Research evidence не равно interpretation и не меняет design автоматически.

---

# Canonical design

Актуальная принятая архитектурная семантика, которая является source of truth для реализации.

---

# ADR

Architecture Decision Record — документ, фиксирующий существенный выбор между несколькими реалистичными вариантами, его причины и trade-offs.

---

# Exact internal contract

Точная machine-facing спецификация взаимодействия внутри MINDRA после того, как semantic design уже принят.

---

# Open question

Существенный вопрос, решение по которому ещё не принято.

Open question не должен превращаться в implicit implementation choice без design review.
