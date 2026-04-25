# DOA-IDEA-008 --- Enforcement Scope Definition

## Metadata

Project: docops-agent  
Doc type: idea_to_mvp  
ID: DOA-IDEA-008  
Status: draft  
Date: 2026-04-25  
Parent: DOA-IMP-038  

---

## Summary

Определить scope применения enforcement layer для устранения шума и повышения доверия к validator.

---

## Problem

Текущий enforcement генерирует шум:

- legacy документы создают violations
- validator не различает зоны
- отсутствует понимание, где enforcement обязателен

Это приводит к:

- снижению доверия к validator
- невозможности использовать enforcement как контрольный механизм

---

## Root Cause

Отсутствует явное определение scope enforcement:

- нет разделения controlled / legacy
- нет boundary-aware логики
- нет правил применимости

---

## Goal

Определить минимальный enforcement scope:

- где enforcement применяется
- где игнорируется
- как учитывается boundary
- как определяется severity

---

## Scope

### Include

- определение зон (controlled / legacy)
- определение boundary
- правила применимости enforcement
- правила обработки severity в зависимости от зоны

### Exclude

- изменения validator
- autofix
- CI/CD интеграция
- изменение существующих документов

---

## Constraints

- MVP simplicity
- create-only
- отсутствие breaking changes
- отсутствие ретроспективных исправлений

---

## Expected Outcome

- снижение noise
- повышение доверия к validator
- возможность дальнейшего развития enforcement
- подготовка к policy layer

---

## Notes

- связано с концепцией snapshot boundary
- требует последующего DEC уровня

---

## Next Step

→ ARCH: определить модель зон и boundary
