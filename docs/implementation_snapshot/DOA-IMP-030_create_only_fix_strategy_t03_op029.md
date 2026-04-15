## Metadata

- Project: DOA
- Doc type: implementation_snapshot
- ID: DOA-IMP-030
- Status: draft
- Date: 2026-04-15
- Parent: DOA-IMP-029

---

## Summary

Для шага **DOA-OP-029-T03** определена стратегия remediation under create-only на основе классификации из **DOA-IMP-029** и baseline-артефактов T01. На этом шаге remediation не выполнялась; зафиксирован только порядок и формат будущего исполнения для снятия blocker subset в рамках ограничений **DOA-DEC-048**.

## Source artifacts

- `docs/decision_log/DOA-DEC-048_no_go_until_integrity_baseline.md`
- `docs/operational_plan/DOA-OP-029_integrity_baseline_cleanup.md`
- `docs/implementation_snapshot/DOA-IMP-028_integrity_baseline_run_t01_op029.md`
- `docs/implementation_snapshot/DOA-IMP-029_integrity_baseline_classification_t02_op029.md`
- `reports/doa_link_id_validator_run_003_integrity_baseline_op029_t01.json`
- `reports/doa_document_gate_run_004_integrity_baseline_op029_t01.json`

## Remediation buckets

| Bucket ID | Bucket name | Finding categories | Covered files/cases (from T01/T02) | Remediation pattern (design only) | Create-only compatibility | Decision need | Micro-cycle need | Risk (traceability / parent graph / ID integrity) | Expected effect on blocker subset | T03 remediation type |
|-----------|-------------|--------------------|-------------------------------------|------------------------------------|---------------------------|---------------|------------------|---------------------------------------------------|----------------------------------|----------------------|
| BKT-A | Enum normalization | `status_not_in_enum` | `DOA-DEC-027`, `DOA-IMP-018..022`, `DOA-OP-021..025` | Выпуск create-only successor документов с canonical `Status` и traceable links на legacy-источник; без in-place правок | conditionally compatible | Новый `decision_log` желателен для policy границы между successor и legacy | Да, отдельный подцикл | Высокий риск ID/parent drift при массовом выпуске successor-файлов | Может снять до 11 blocking findings | B |
| BKT-B | Parent/reference consistency | `unresolved_parent`, `missing_parent_field` | `DOA-ARCH-003`, `DOA-DEC-027` | Нормализация Parent через новые канонические successor-артефакты или policy-backed mapping в рамках уже принятого контракта | conditionally compatible | Нужен `decision_log` для выбора единого механизма (successor-only vs policy mapping) | Да | Критичный риск parent graph integrity при неоднородном подходе | Может снять 2 blocking findings | B |
| BKT-C | Duplicate ID resolution | `duplicate_id_registry` (unresolved) | `DOA-OP-021` pair | Create-only разведение ID через новые документы с уникальным ID + явная декларация replacement lineage | conditionally compatible | Нужен `decision_log` (правила dedup без ретро-правок accepted) | Да | Критичный риск ID integrity и связности ссылок | Может снять 1 blocking finding | B |
| BKT-D | Metadata key normalization | `noncanonical_doc_type_key` | `DOA-DEC-027` | Новый canonical successor с правильным `Doc type` key и parent linkage | compatible | Новый `decision_log` не обязателен | Нет (можно в общем цикле blocker-fixes) | Средний риск, локальный и хорошо трассируемый | Может снять 1 blocking finding | A |
| BKT-E | Replaces format normalization | `invalid_replaces_format` | `DOA-OP-001` | Новый canonical successor с валидным `Replaces`/traceability полем по текущему контракту | compatible | Новый `decision_log` не обязателен | Нет (можно в общем цикле blocker-fixes) | Низкий-средний риск; точечная правка формата через новый документ | Может снять 1 blocking finding | A |
| BKT-F | Legacy-only continuity | `legacy_no_canonical_metadata`, `root_markdown_outside_docs_model` | 43 legacy docs + `README.md`/`WORKFLOW.md` | Вынести в отдельный поток вне blocker-remediation; не смешивать с baseline unblock | compatible | Новый `decision_log` не обязателен для T04+ unblock | Да (отдельный поток) | Риск размывания scope и задержки unblock, если смешать с blocker subset | Не влияет на текущий blocker subset | D |
| BKT-G | Overlay-resolved continuity | `resolved_via_overlay` subset | `DOA-IDEA-002` parent override, `DOA-IMP-014` duplicate mapping | Зафиксировать как stable non-blocking evidence; без изменений на T03/T04 | compatible | Новый `decision_log` не обязателен | Нет | Низкий риск; важно не регрессировать существующее overlay покрытие | Не уменьшает blocker напрямую | D |
| BKT-H | Cross-zone integrity watch | `cross_zone_violations` | T01: `0` | Сохранить как monitor-only checkpoint, без remediation действий | compatible | Не требуется | Нет | Низкий; контроль на случай регрессии в следующих прогонах | Нет прямого эффекта (сейчас 0) | D |

## Compatibility with create-only

- Полностью совместимые без нового решения: **BKT-D**, **BKT-E**.
- Условно совместимые (требуют предварительного governance-решения): **BKT-A**, **BKT-B**, **BKT-C**.
- Вне текущего unblock-потока (non-blocking/monitor): **BKT-F**, **BKT-G**, **BKT-H**.
- Bucket типа `not yet justified` в текущем T03 не выявлен: все blocker-категории либо операционно достижимы, либо достижимы после дополнительного `decision_log`.

## Decision requirements before remediation

Без нового решения можно обрабатывать:

- **BKT-D** (`noncanonical_doc_type_key`)
- **BKT-E** (`invalid_replaces_format`)

Требуют новый `decision_log` перед remediation:

- **BKT-A** (`status_not_in_enum`) — нужен единый policy-контур массовой нормализации через create-only successors.
- **BKT-B** (`unresolved_parent`, `missing_parent_field`) — нужен единый механизм восстановления parent-graph.
- **BKT-C** (`duplicate_id_registry`) — нужны однозначные dedup-правила без ретро-редактирования accepted-документов.

Create-only ambiguity point:

- Для **BKT-A/B/C** ambiguity в том, как считать «исправленным» legacy blocker без in-place правок legacy/accepted артефактов. Это требует отдельного governance решения до старта T04 remediation.

## Recommended remediation order

1. **BKT-D (metadata key normalization)** — быстрый и низкорисковый unblock.
2. **BKT-E (replaces format normalization)** — точечный и безопасный unblock.
3. **Decision gate for BKT-A/B/C** — принять единый `decision_log` на remediation-модель.
4. **BKT-B (parent/reference consistency)** — сначала стабилизация parent graph.
5. **BKT-C (duplicate ID resolution)** — затем устранение ID конфликтов на согласованной модели.
6. **BKT-A (enum normalization batch)** — в конце как самый объемный поток с наибольшим риском шумовых регрессий.
7. **BKT-F/G/H** — отдельный non-blocking stream, не блокирующий T04/T05 по baseline unblock.

## Proposed execution format

Рекомендуется **серия малых operational micro-cycles по bucket-ам**, а не один общий большой remediation cycle.

Почему это лучше для DocOps дисциплины:

- обеспечивает атомарные коммиты с прозрачным causal link «bucket -> change set -> rerun evidence»;
- снижает риск смешивания blocker и non-blocking потоков;
- упрощает traceability Parent/Replaces/ID при create-only выпуске successor-артефактов;
- позволяет остановиться после каждого micro-cycle и проверять регрессию до следующего шага.

Практический формат для T04+:

- micro-cycle M1: BKT-D + BKT-E (без нового decision_log),
- micro-cycle M2: после нового decision_log — BKT-B + BKT-C,
- micro-cycle M3: после того же/доп. decision_log — BKT-A batch,
- отдельный backlog stream: BKT-F/G/H.

## Conclusion

- Стратегия T03 зафиксирована без выполнения remediation, без rerun validator/gate и без изменений overlay/code/docs вне нового snapshot.
- Для быстрого и безопасного старта T04 доступны **BKT-D** и **BKT-E**.
- Для снятия оставшегося blocker subset требуется как минимум один дополнительный `decision_log` по create-only remediation governance для **BKT-A/B/C**.
- После принятия этого решения можно переходить к T04 в формате micro-cycles с повторными прогонами после каждого завершенного bucket-потока.

## Related tasks

- **DOA-OP-029-T03** — fix strategy under create-only.

## Related commits

- N/A (этот snapshot фиксирует design-only strategy шага T03).

## Known issues

- Baseline остается blocked до исполнения T04+ и подтвержденных rerun-артефактов.
- Для крупных blocker buckets пока отсутствует формально принятая governance-модель create-only remediation.

## Next step

- Подготовить отдельный `decision_log` для governance рамки remediation по **BKT-A/B/C**, затем запускать T04 как серию micro-cycles.
