## Metadata

- Project: DOA
- Doc type: audit_check
- ID: DOA-AUD-001
- Status: draft
- Date: 2026-04-08
- Parent: DOA-IMP-009

---

## Summary

Аудит согласованности **DocOps Agent MVP bootstrap** после добавления примеров документов (T03): naming, metadata, цепочка Parent.

## Scope of audit

- Новые примеры: `DOA-IDEA-001`, `DOA-ARCH-011`, `DOA-DEC-025`, `DOA-LT-001`, `DOA-MT-001`, `DOA-OP-002`, `DOA-IMP-009`, `DOA-AUD-001`
- Выборочно: соответствие исторических документов ожидаемым **папкам** (без изменения файлов)

## Checked documents

- `docs/idea_to_mvp/DOA-IDEA-001.md`
- `docs/architecture_draft/DOA-ARCH-011.md`
- `docs/decision_log/DOA-DEC-025.md`
- `docs/longterm_plan/DOA-LT-001.md`
- `docs/midterm_plan/DOA-MT-001.md`
- `docs/operational_plan/DOA-OP-002.md`
- `docs/implementation_snapshot/DOA-IMP-009.md`
- `docs/implementation_snapshot/DOA-OP-017.md` _(legacy placement)_

## Findings

- Цепочка Parent по T03 соблюдена: `IDEA → ARCH → DEC`; `IDEA → LT → MT → OP → IMP → AUD`
- Metadata: Project **DOA**, Date **2026-04-08**, Status **draft**, Doc type совпадает с каталогом для новых примеров
- Исторический файл **`docs/implementation_snapshot/DOA-OP-017.md`** имеет тип **OP**, но расположен в каталоге **implementation_snapshot**

## Violations

- **Placement / organization (legacy) operational_plan-файла внутри `implementation_snapshot/`** — не соответствует желаемой карте каталогов для doc_type `operational_plan` (нарушение структуры **без** переписывания содержимого)

## Recommendations

- **Не исправлять ретроспективно** в рамках T03 (create-only и сохранение истории)
- Учитывать **`DOA-OP-017.md`** как **legacy artifact** при навигации и будущих аудитах
- Новые `DOA-OP-*` создавать только под `docs/operational_plan/`

## Decision needed

Не требуется: политика **fix forward** через новые артефакты согласована с `DOA-DEC-025` и операционными заметками `DOA-OP-002`.

## Result

**pass with noted legacy issue** — примеры T03 согласованы; зафиксировано одно структурное legacy-наблюдение без немедленного исправления.
