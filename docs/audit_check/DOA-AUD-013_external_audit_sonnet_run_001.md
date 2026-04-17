# DOA-AUD-013 — External audit Sonnet run 001

## Metadata

- Project: docops-agent
- Doc type: audit_check
- ID: DOA-AUD-013
- Status: accepted
- Date: 2026-04-17
- Parent: DOA-DEC-055

---

## Scope and Inputs

Аудит выполнен независимо от DOA-AUD-012. Все артефакты прочитаны напрямую из репозитория без подгонки под вывод Codex.

Использованные артефакты:

- `docs/architecture_draft/DOA-ARCH-024_snapshot_artifact_spec.md` — Status: **draft**
- `docs/decision_log/DOA-DEC-053_snapshot_lifecycle.md`
- `docs/decision_log/DOA-DEC-054_snapshot_policy_severity.md`
- `docs/decision_log/DOA-DEC-055_external_multi_model_audit_strategy.md`
- `docs/operational_plan/DOA-OP-034_snapshot_creation_protocol.md` — Status: **draft**
- `docs/operational_plan/DOA-OP-035_snapshot_validator_gate_rules.md` — Status: **draft**
- `docs/operational_plan/DOA-OP-036_snapshot_readiness_checks.md` — Status: **draft**
- `docs/implementation_snapshot/DOA-IMP-035_snapshot_validator_gate_mvp.md`
- `docs/audit_check/DOA-AUD-011_snapshot_readiness_audit_run_001.md`
- `docs/audit_check/DOA-AUD-012_external_audit_codex_run_001.md` (для сравнения)
- `reports/doa_link_id_validator_run_007_snapshot_readiness_audit_001.json`
- `reports/doa_document_gate_run_008_snapshot_readiness_audit_001.json`
- `scripts/doa_link_id_validator.py`
- `scripts/doa_document_gate.py`

---

## Executive Assessment

### Q1. Корректна ли snapshot-driven архитектурная модель в целом?

**Да, концептуально корректна.** Epoch-boundary model — зрелый паттерн управления эволюцией систем. Реализация в DocOps соответствует принципу: фиксируй состояние, затем двигайся вперёд без оглядки на историю.

**Системное предупреждение:** ключевой архитектурный документ (`DOA-ARCH-024`) имеет `Status: draft`. Это означает, что вся snapshot subsystem формально стоит на незакреплённой архитектурной основе. Это не блокер на MVP, но структурный риск.

---

### Q2. Корректно ли проведено разделение legacy / controlled?

**Разделение работоспособно, но механизм хрупок.**

Зона определяется через `git log --diff-filter=A` для каждого файла, результат сравнивается с `BOUNDARY_COMMIT`. Это единственная точка правды о принадлежности файла к зоне.

Два конкретных риска в коде, которые Codex не указал:

1. `BOUNDARY_COMMIT = "d94a7d7b..."` — захардкожен в скрипте. При необходимости смены эпохи нужно менять код, а не документ.
2. `closure_semantics_enabled = False` в `doa_link_id_validator.py`, но `True` в `doa_document_gate.py` — эта асимметрия намеренна (только gate применяет T07 activation), но нигде не задокументирована как invariant. Это риск рассинхронизации при будущих правках.

---

### Q3. Достаточно ли консистентны validator и gate относительно policy?

**Частично.** Error-slice реализован. Но:

- `DOA-DEC-054` описывает три severity класса (error/warn/info), однако в `doa_link_id_validator.py` реализованы только 4 snapshot error checks без ни одного warning/info check.
- В gate добавлен `SNAPSHOT_CATEGORY_SEVERITY_OVERRIDES` с 4 ключами — ровно те же 4 categories что в validator. Это self-consistent, но неполно относительно policy-документа.

Конкретная несоответствие: `DOA-DEC-054` перечисляет в разделе Warning `неполный scope`, `недостаточно ясное описание epoch`, `неполный validator status` — ни одно из этих условий не имеет machine check.

---

### Q4. Не содержит ли readiness logic скрытого противоречия?

**Содержит слабость, которую я оцениваю жёстче, чем Codex.**

Readiness PASSED основан на `controlled_findings_count = 0`. В репозитории на момент audit run 33 controlled-документа. Это молодая зона, и `0 findings` скорее говорит о том, что controlled документы ещё не накопили нарушений, чем о том, что система действительно здорова.

Спорный момент: вывод `readiness PASSED` технически корректен по формальным критериям. Однако аргумент "отсутствие нарушений — доказательство качества" — логически слабый, особенно для зоны, созданной 1 день назад. Это не противоречие, но потенциально ложная уверенность.

Отдельное наблюдение: в gate-отчёте зафиксировано `other_zone_findings_count: 2`. Это findings с неизвестной зоной (`source_zone` не legacy, не controlled, не boundary). Они не объяснены ни в одном readiness документе и не включены в readiness criteria.

---

### Q5. Самые сильные стороны системы на текущем этапе

1. **Docs-first governance до кода** — lifecycle, policy и readiness criteria зафиксированы в документах прежде, чем написан код. Это сильная сторона дисциплины.
2. **Реальная dual-mode operational verdicts** — `gate_status` и `gate_status_controlled` работают и дают разные сигналы. Система не блокируется legacy noise.
3. **Трассируемость через Parent/ID цепочку** — от концепции (`DOA-IDEA-004`) до audit run можно восстановить всю цепочку решений.
4. **Create-only дисциплина** — enforced не только в документах, но и в практике (нет ни одного edited existing accepted document в controlled zone).

---

### Q6. 3–5 наиболее серьёзных архитектурных рисков

1. **Hardcoded BOUNDARY_COMMIT** — при создании новой эпохи нужно менять код скрипта. Это нарушает принцип, при котором документ (новый FSN) должен быть единственным источником изменения эпохи. Документ меняется, а код — нет автоматически.

2. **Draft-статус ключевых архитектурных документов, используемых как operational foundation** — `DOA-ARCH-024`, `DOA-OP-034`, `DOA-OP-035`, `DOA-OP-036` имеют `Status: draft` и при этом уже являются операционной основой системы. Это создаёт несоответствие: система готова к следующему snapshot cycle, но строит его на незакреплённых документах.

3. **Closure semantics asymmetry не зафиксирована как invariant** — разное значение `closure_semantics_enabled` в validator и gate — намеренный дизайн, но нигде явно не задокументированный как правило. Это риск будущей рассинхронизации.

4. **other_zone_findings_count: 2 не в scope readiness** — эти findings не объяснены и не включены в readiness criteria. При росте системы аналогичные unexplained findings могут скрывать реальные проблемы.

5. **SNAPSHOT_ID_RE ограничивает DOA-FSN до 3 знаков** — регулярное выражение `^DOA-FSN-\d{3}$` допускает только номера 001–999. При серьёзном масштабировании это может стать ограничением (спорный момент: для большинства реалистичных сценариев это несущественно).

---

### Q7. Следующий наиболее разумный шаг

Не snapshot creation, а закрытие трёх технических долгов в правильном порядке:

1. Перевести ключевые документы из draft в accepted (`DOA-ARCH-024`, `DOA-OP-034..036`) — это обязательный шаг перед тем, как считать систему operationally sound.
2. Задокументировать `closure_semantics_enabled` asymmetry как explicit invariant.
3. Объяснить и закрыть `other_zone_findings_count: 2`.

После этого — snapshot creation по `DOA-OP-034`.

---

### Q8. Есть ли расхождение между документной моделью и фактической операционной моделью?

**Да, и это конкретно:**

| Аспект | Документная модель | Фактическая реализация |
|---|---|---|
| Severity для snapshot findings | Error + Warning + Info (DOA-DEC-054) | Только Error (4 checks) |
| Смена эпохи | Создать новый DOA-FSN документ | Также нужно менять `BOUNDARY_COMMIT` в коде |
| Closure semantics | Единый документ | Разные флаги в validator и gate |
| Draft-статус ключевых docs | Документы в draft | Используются как operational foundation |

---

### Q9. Сравнение с Codex (DOA-AUD-012)

**Подтверждаю выводы Codex:**

- Git-based zone attribution fragility — согласен, это ключевой риск.
- Неполное покрытие warning/info policy — согласен, это задокументированная несоответствие.
- Риск policy-code drift — согласен.
- Рекомендация по отдельному snapshot diagnostics block — согласен.

**Считаю спорными или неполными:**

- Codex не отметил, что `DOA-ARCH-024` и операционные планы имеют `Status: draft`. Это значимый governance gap, который Codex пропустил.
- Codex вывел readiness как "логически корректный" без оговорок. Я считаю, что `controlled_findings_count=0` в молодой зоне — слабый сигнал, и readiness PASSED должен сопровождаться явным предупреждением об этом.
- Codex не зафиксировал `other_zone_findings_count: 2` как неисследованный gap.
- Codex рекомендует "versioned readiness profile" — я считаю это преждевременным. Сначала нужно закрыть draft-статусы и coverage gap policy matrix.
- Codex не упомянул `closure_semantics_enabled` asymmetry.
- Codex не заметил ограничение `SNAPSHOT_ID_RE` до 3 знаков.

---

## Layered Analysis

### Docs Layer

**Strengths**
- Структурная целостность: документы связаны по Parent/ID, цепочка восстанавливается.
- Policy зафиксирована до кода.
- Lifecycle формализован.

**Risks**
- `DOA-ARCH-024` в статусе draft — архитектурный базис не закреплён.
- `DOA-OP-034`, `035`, `036` в статусе draft — операционные процедуры не закреплены.

**Inconsistencies**
- **Реальная несоответствие (не спорная):** система объявлена готовой к следующему snapshot cycle (`readiness PASSED`), но фундаментальные операционные документы для этого процесса (`DOA-OP-034`, `036`) имеют статус draft, что формально означает незавершённость.

**Recommendations**
- Перевести ключевые operational и architecture документы в `Status: accepted` перед snapshot creation run.

---

### Validator/Gate Layer

**Strengths**
- `fixed_snapshot` корректно изолирован как отдельный artifact class.
- Базовые error checks реализованы и связаны с gate policy.
- Dual-verdict работает и выдаёт правильные значения на текущем корпусе.

**Risks**
- `BOUNDARY_COMMIT` hardcoded — смена эпохи требует изменения кода.
- Warning/info checks отсутствуют.
- `other_zone_findings_count: 2` не покрыт readiness criteria.

**Inconsistencies**
- `closure_semantics_enabled` имеет разные значения в двух скриптах без документированного invariant.
- Gate принимает `engine_severity` от validator через поле и применяет `SNAPSHOT_CATEGORY_SEVERITY_OVERRIDES` поверх. Это double-classification: validator уже проставляет `"severity": "error"`, gate снова override-ит ту же категорию тем же значением. Это не ошибка, но избыточная логика с риском drift.

**Recommendations**
- Зафиксировать `closure_semantics_enabled` asymmetry как explicit architectural invariant в `DOA-ARCH` документе.
- Добавить warning-level snapshot checks по `DOA-DEC-054`.
- Вынести `BOUNDARY_COMMIT` в конфигурационный файл или читать из FSN-документа напрямую.

---

### Operational Semantics

**Strengths**
- Чёткое разделение historical REJECT и operational ACCEPT.
- Readiness criteria формализованы, документированы и проверены run-артефактами.

**Risks**
- `readiness PASSED` при `controlled_findings_count=0` — слабый сигнал в молодой зоне.
- `other_zone_findings_count: 2` не объяснён ни в одном документе.

**Inconsistencies**
- Readiness criteria в `DOA-OP-036` сформулированы как tasks (Done when), но сам документ имеет `Status: draft`. Это создаёт формальный gap: readiness запущен по незакреплённому checklist.

**Recommendations**
- Добавить в readiness criteria явный check: "ключевые operational документы имеют Status: accepted".
- Объяснить `other_zone_findings_count` в gate-отчёте как часть readiness evidence.

---

## Summary: Strengths

1. Docs-first governance с трассируемой цепочкой от идеи до audit.
2. Create-only дисциплина выдержана в controlled zone.
3. Dual-verdict рабочий и логически последовательный.
4. Snapshot как boundary artifact — архитектурно здравый выбор.

---

## Summary: Risks

1. Hardcoded BOUNDARY_COMMIT — смена эпохи требует изменения кода.
2. Ключевые docs в draft-статусе при operational use.
3. closure_semantics asymmetry без документированного invariant.
4. other_zone_findings_count: 2 не исследован и не включён в readiness.
5. Неполная severity matrix (только error-slice) vs. accepted policy (error/warn/info).

---

## Summary: Inconsistencies

1. **Реальная:** `DOA-ARCH-024`, `DOA-OP-034/035/036` = draft, используются как operational foundation.
2. **Реальная:** severity policy (`DOA-DEC-054`) шире фактических checks на 2 severity класса.
3. **Реальная:** double-classification severity в validator + gate для snapshot categories.
4. **Спорная:** `readiness PASSED` при `controlled_findings_count=0` в 33-документной зоне — технически корректно, практически слабый сигнал.

---

## Summary: Recommendations

1. Перевести `DOA-ARCH-024`, `DOA-OP-034`, `DOA-OP-035`, `DOA-OP-036` в `Status: accepted` перед snapshot creation.
2. Вынести `BOUNDARY_COMMIT` из кода в конфигурацию или считывать из FSN-документа.
3. Задокументировать `closure_semantics_enabled` asymmetry как invariant.
4. Объяснить и закрыть `other_zone_findings_count: 2`.
5. Реализовать warning-level snapshot quality checks согласно `DOA-DEC-054`.

---

## Final Verdict

Система технически работоспособна и концептуально здравая. Однако заявленная готовность к следующему snapshot cycle не вполне подтверждается формальным состоянием governance: ключевые операционные документы остаются в draft, severity policy реализована частично, а readiness signal основан на тонком слое из 33 новых документов без нарушений. Это не блокер, но требует явного признания текущих ограничений перед следующим cycle.
