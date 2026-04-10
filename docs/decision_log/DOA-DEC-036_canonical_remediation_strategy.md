## Metadata

- Project: DocOps Agent
- Doc type: decision_log
- ID: DOA-DEC-036
- Status: accepted
- Date: 2026-04-10
- Parent: DOA-OP-022

---

## Title

Canonical remediation strategy under create-only constraint

## Context

- canonical metadata является source of truth;
- текущие canonical blockers мешают автоматической трассировке;
- legacy документы не могут быть массово переписаны;
- требуется способ устранения нарушений без изменения исторических документов.

## Decision

### 1. No in-place edits

- запрещено изменять существующие документы;
- исторические ошибки не переписываются.

---

### 2. Remediation through overlay layer

Вводится отдельный слой данных поверх документов.

#### 2.1 Mapping registry

- отдельный документ (или набор документов), содержащий:
  - `legacy_id -> canonical_id`
  - `broken_parent -> resolved_parent`
  - `duplicate_id -> canonical_resolution`

#### 2.2 Alias mechanism

- допускается объявление alias для ID:
  - один canonical ID
  - несколько legacy ссылок

#### 2.3 Override entries

- точечные исправления:
  - Parent
  - Replaces
  - metadata inconsistencies

---

### 3. Validator integration

- validator должен учитывать overlay слой:
  - сначала читается overlay
  - затем документы
- findings могут иметь статус:
  - `resolved_via_overlay`
  - `unresolved`

---

### 4. Gate behavior

- ошибки, закрытые overlay:
  - не считаются `error`
  - могут быть downgraded до `info`

---

### 5. Transparency

- все overlay решения:
  - документируются
  - трассируются
  - не скрывают исходную проблему

---

### 6. Gradual canonicalization

- новые документы -> только canonical;
- legacy остается, но:
  - не расширяется
  - постепенно "поглощается" overlay

## Rationale

- create-only сохраняется;
- история не искажается;
- система остается детерминированной;
- устраняется необходимость ручных массовых правок.

## Consequences

Плюсы:

- можно устранить текущие blockers;
- система становится управляемой;
- уменьшается noise.

Минусы:

- появляется дополнительный слой (overlay);
- усложняется validator.

## Follow-ups

- создать `docs/rules/` или аналог для overlay registry;
- обновить validator для поддержки overlay;
- обновить gate для учета resolved findings.
