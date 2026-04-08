# audit_check — DOA-AUD-002

## Metadata

- Project: DOA
- Doc type: audit_check
- ID: DOA-AUD-002
- Status: draft
- Date: 2026-04-08
- Parent: DOA-IMP-009

---

## Summary

Формальный аудит **DocOps Agent MVP bootstrap** после T01–T04: структура `docs/` и `templates/`, шаблоны, sample-документы T03, `WORKFLOW.md`, известный legacy `DOA-OP-017.md`. Итог: **pass with noted legacy issue**; ретро-исправлений не выполнялось.

---

## Scope of audit

- repository structure (`docs/*`, `templates/*`)
- templates (8 `*.template.md`, metadata и скелет разделов)
- sample documents (DOA-IDEA-001 … DOA-AUD-001)
- `WORKFLOW.md` (соответствие doc_types и planning layer)
- legacy artifacts (`DOA-OP-017.md`)

---

## Checked documents

**Каталоги** (наличие):

- `docs/architecture_draft/`
- `docs/audit_check/`
- `docs/decision_log/`
- `docs/idea_to_mvp/`
- `docs/implementation_snapshot/`
- `docs/longterm_plan/`
- `docs/midterm_plan/`
- `docs/operational_plan/`

**Шаблоны:**

- `templates/idea_to_mvp/idea_to_mvp.template.md`
- `templates/architecture_draft/architecture_draft.template.md`
- `templates/decision_log/decision_log.template.md`
- `templates/implementation_snapshot/implementation_snapshot.template.md`
- `templates/operational_plan/operational_plan.template.md`
- `templates/midterm_plan/midterm_plan.template.md`
- `templates/longterm_plan/longterm_plan.template.md`
- `templates/audit_check/audit_check.template.md`

**Sample docs (T03):**

- `docs/idea_to_mvp/DOA-IDEA-001.md`
- `docs/architecture_draft/DOA-ARCH-011.md`
- `docs/decision_log/DOA-DEC-025.md`
- `docs/longterm_plan/DOA-LT-001.md`
- `docs/midterm_plan/DOA-MT-001.md`
- `docs/operational_plan/DOA-OP-002.md`
- `docs/implementation_snapshot/DOA-IMP-009.md`
- `docs/audit_check/DOA-AUD-001.md`

**Прочее:**

- `WORKFLOW.md` (корень репозитория)
- `docs/implementation_snapshot/DOA-OP-017.md` (legacy placement)

---

## Findings

- Все перечисленные **doc_type** каталоги под `docs/` присутствуют.
- В `templates/` для каждого из **8** doc_types есть ровно один `*.template.md`; во всех проверенных шаблонах есть блок **`## Metadata`** с полем **`Doc type`**, далее идёт структура разделов по назначению типа.
- Sample-документы T03 существуют, используют единый стиль **`## Metadata`** с полями Project / Doc type / ID / Status / Date / Parent; naming `DOA-<TYPE>-<NNN>` для перечисленных ID соблюдён.
- Цепочка Parent для sample line согласована: `IDEA-001 (null)` → `ARCH-011` → `DEC-025`; `IDEA-001` → `LT-001` → `MT-001` → `OP-002` → `IMP-009` → `AUD-001`.
- `WORKFLOW.md` описывает те же **doc_types**, поток с **longterm_plan (optional)** → **midterm_plan** → **operational_plan**, отдельно **decision_log** на любых этапах, **planning layer** и **create-only**; противоречий с содержанием sample-документов (T03) не выявлено.
- В `docs/architecture_draft/` дополнительно присутствуют импортированные из TZ canonical **DOA-ARCH-001 … 010** (T03 импорт) — параллельно с sample **DOA-ARCH-011**; это **наблюдение** о двух линиях архитектурных артефактов, а не сбой методологии.

---

## Violations

### Critical

- **none**

### Non-critical

- В ряде каталогов `docs/<doc_type>/` сохранён пустой **`/.gitkeep`** рядом с уже добавленными документами (например `docs/idea_to_mvp/`) — визуальный шум; устранение не входит в данный audit (create-only / отдельная задача при желании).
- Часть **исторических** файлов в `docs/decision_log/` (например **DOA-DEC-004**) использует **иную** структуру заголовков (без единого блока `## Metadata` в стиле T03) — ожидаемо для наследия; унификация только через новые документы при необходимости.

### Legacy

- **`docs/implementation_snapshot/DOA-OP-017.md`** — документ типа **operational_plan** размещён в каталоге **implementation_snapshot** (несоответствие папки и doc_type). Уже зафиксировано в **DOA-AUD-001**; на этом шаге **не исправлялось** (политика create-only / DEC-027 для импорта TZ).

---

## Recommendations

- Продолжать выполнение **DOA-OP-001** по утверждённым планам.
- Legacy **DOA-OP-017.md** учитывать при навигации; **не** править ретроспективно без отдельного решения.
- Принять расширенную структуру **`docs/`** + **`WORKFLOW.md`** как **source of truth** для bootstrap; новые документы создавать по шаблонам из `templates/`.

---

## Decision needed

**no new decision required**

Новых **значимых** противоречий методологии (помимо известного legacy OP-017 и ожидаемого формата старых DEC) не выявлено; отдельный **decision_log** для этого аудита не создаётся.

---

## Result

**pass with noted legacy issue**

- Критических нарушений нет.
- Legacy: misplaced **DOA-OP-017.md** остаётся зафиксированным несоответствием без автоматического исправления.
