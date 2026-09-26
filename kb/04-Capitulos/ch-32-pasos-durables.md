---
id: "CH-32"
tipo: capitulo
titulo: "Pasos Durables y la Recuperación a Mitad de Turno"
tags: [capitulo, ch32, tramo-4]
introduces_components: ["CMP-023"]
introduces_contracts: ["C-042", "C-043"]
modifies_contracts: []
articulos_constitucionales: ["P-23", "P-24", "P-32", "INV-07", "INV-11", "INV-13", "INV-E16", "INV-E17"]
---

# CH-32 — Pasos Durables y la Recuperación a Mitad de Turno

## Navegación

⬅ [[ch-31-identidad-del-llamante|CH-31]] · **CH-32** · [[ch-33-esperas-durables|CH-33]] ➡

## Resultado esperado

Al terminar este capítulo podrás descomponer un turno en pasos durables y explicar por qué cada hecho de un paso se escribe antes del efecto siguiente. También podrás decidir, para cualquier paso que encuentres en el registro después de una caída del proceso, qué hace la recuperación con él, sin repetir nunca algo que ya quedó comprometido.

## Qué introduce este capítulo

### Componentes

- [[CMP-023-executionjournal|CMP-023 ExecutionJournal]]: primer componente de v0.2. Delega en [[CMP-015-idempotencyguard|IdempotencyGuard]] la decisión sobre un efecto pendiente (INV-E17).

### Contratos

- [[C-042-steprecord|C-042 StepRecord]]
- [[C-043-recoverydecision|C-043 RecoveryDecision]]

## Artículos constitucionales relevantes

P-23, P-24, P-32, INV-07, INV-11, INV-13, INV-E16, INV-E17

## Localización en el repo

`book/chapters/32-pasos-durables/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
