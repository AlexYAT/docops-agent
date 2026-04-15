## Metadata

- Project: DOA
- Doc type: decision_log
- ID: DOA-DEC-049
- Status: draft
- Date: 2026-04-15
- Parent: DOA-IMP-030

---

## Title

Create-only remediation model for integrity baseline

## Context

- По линии **DOA-OP-029** зафиксирован blocker subset для integrity baseline (16 unresolved canonical findings) в **DOA-IMP-029**.
- В **DOA-IMP-030** определено, что buckets **BKT-A/B/C** требуют governance-решение до старта remediation.
- Переход к следующему слою реализации запрещен до PASS baseline по **DOA-DEC-048**.
- Remediation должна выполняться без ретро-редактирования существующих документов в рамках create-only дисциплины.

## Problem

Отсутствует формально принятая модель:

- что считается «исправлением» finding в create-only режиме;
- как трактовать legacy broken документы без in-place правок;
- как validator/gate должны интерпретировать successor и overlay механизмы для снижения blocker subset без потери traceability.

## Options considered

### 1) Только successor модель

- Все remediation выполняются только через новые документы-наследники (successor lineage), без overlay-резолюций.
- Плюс: максимальная документальная трассируемость в markdown-артефактах.
- Минус: высокий операционный объем и задержка для точечных конфликтов (особенно duplicate/parent mapping).

### 2) Только overlay модель

- Все remediation трактуются через policy mapping в overlay без выпуска successor-документов.
- Плюс: быстрое операционное снятие части блокеров.
- Минус: риск превращения overlay в скрытый SoT и снижения прозрачности документной эволюции.

### 3) Гибрид: successor + overlay

- Семантические и структурные исправления идут через successor-документы.
- Overlay используется только как ограниченный механизм интерпретации и мост совместимости для явно разрешенных классов.

## Chosen solution

Принят **Option 3 (гибрид successor + overlay)** с приоритетом на successor-путь:

1. **Successor-first** для канонических structural fixes (status/metadata/parent/replaces/id lineage).
2. **Overlay-constrained** как вторичный механизм:
   - только для явно перечисленных policy-случаев;
   - только с явной ссылкой на source rule;
   - без замены документной трассируемости.
3. Любой новый тип overlay-резолюции, влияющий на blocker subset, требует отдельного decision_log.

## Rules

### 1. Status normalization

- Категория: `status_not_in_enum`.
- Допустимый remediation path: выпуск successor-документа с каноническим `Status` из утвержденного enum.
- Legacy-источник не переписывается.
- Overlay может понижать severity только если есть явное policy-rule соответствие в рамках уже принятой схемы; расширение этого набора — через новый decision_log.

### 2. Parent remediation

- Категории: `unresolved_parent`, `missing_parent_field`.
- Базовый path: successor-документ с валидным `Parent` и явной линией преемственности.
- Parent override через overlay допустим только как строго ограниченный bridge для подтвержденных кейсов и не должен подменять долгосрочную successor-модель.

### 3. Duplicate ID resolution

- Категория: `duplicate_id_registry`.
- Базовый path: create-only разведение конфликтов через новые документы с уникальными ID и прозрачной replacement-lineage.
- Overlay mapping допустим как временная совместимость, если уже формально принят и не создает неоднозначности ID graph.

### 4. Metadata normalization

- Категория: `noncanonical_doc_type_key` (и аналогичные key-level нарушения).
- Исправление выполняется через successor-документ с canonical metadata keys.
- In-place правка legacy/accepted артефакта не используется.

### 5. Replaces semantics

- Категория: `invalid_replaces_format`.
- Исправление выполняется successor-артефактом с валидным `Replaces` форматом по действующему контракту.
- `Replaces` не должен использоваться для сокрытия lineage; связь должна оставаться machine-traceable.

## Resolution semantics

Finding считается **resolved**, если выполнено одно из условий:

1. **Resolved via successor**
   - существует новый canonical документ в корректном `doc_type` каталоге;
   - в нем устранена причина исходного finding;
   - lineage к исходному документу machine-traceable (`Parent`/`Replaces`/ID references по контракту);
   - validator/gate на следующем run больше не выдает исходный blocker как unresolved.

2. **Resolved via overlay**
   - finding попадает в явно разрешенный overlay-rule;
   - отчёт содержит `resolution_status=resolved_via_overlay` и ссылку на `overlay_source`/rule type;
   - severity интерпретируется по policy как non-blocking для текущего цикла.

3. **Resolved via combination**
   - successor устраняет целевую структуру;
   - overlay используется только как переходный bridge до полной консистентности ссылочного графа;
   - финальная цель — свести зависимость от overlay для blocker-класса к нулю или к формально утвержденному минимальному набору.

## Validator/Gate interpretation rules

- По умолчанию unresolved canonical findings остаются **error** и удерживают `gate_status=REJECT`.
- Findings с `resolution_status=resolved_via_overlay` по утвержденной policy понижаются до **info** (или иного non-blocking уровня, если это явно зафиксировано policy).
- Legacy-only findings остаются non-blocking наблюдениями (`warn/info`) и не должны маскировать blocker subset.
- Cross-zone violations в controlled контуре остаются блокирующими без downgrade.
- Gate обязан сохранять раздельную видимость:
  - `gate_status` (общий),
  - `gate_status_controlled`,
  - dual-mode counts и resolution markers.

## Why

- Гибридная модель балансирует скорость и управляемость: successor сохраняет документную трассируемость, overlay дает контролируемый механизм переходной интерпретации.
- Модель совместима с create-only и не требует ретро-редактирования historical/accepted документов.
- Подход уменьшает риск policy drift между документацией и validator/gate поведением.

## Trade-offs

- Governance-слой становится сложнее: нужно строго контролировать границы overlay применения.
- Successor-first увеличивает количество новых документов и требует дисциплины по lineage.
- Быстрые «чисто overlay» решения ограничены, чтобы не размыть source-of-truth модель.

## Follow-ups

- Запуск **T04 micro-cycles** по порядку из **DOA-IMP-030**:
  1) BKT-D + BKT-E,
  2) BKT-B + BKT-C,
  3) BKT-A.
- Для каждого micro-cycle:
  - отдельный create-only change set,
  - отдельный implementation_snapshot,
  - последующий rerun validator/gate как evidence.
- Legacy-only поток (BKT-F/G/H) вести отдельно от blocker remediation.
