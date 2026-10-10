---
id: "CH-43"
tipo: capitulo
titulo: "Presupuestos que se Heredan"
tags: [capitulo, ch43, v0-3]
introduces_components: []
introduces_contracts: ["C-057"]
modifies_contracts: ["C-012"]
articulos_constitucionales: ["P-09", "P-35", "INV-09", "INV-E06", "INV-E21"]
---

# CH-43 — Presupuestos que se Heredan

## Navegación

⬅ [[ch-42-fuentes-de-datos|CH-42]] · **CH-43**

## Resultado esperado

Al terminar este capítulo podrás decidir cuánto presupuesto recibe cada run hijo a partir de lo que le queda a su padre, explicar por qué un hijo nunca puede recibir más, y calcular cuánto le queda al padre después de que sus hijos terminan.

## Qué introduce este capítulo

### Componentes

- Ninguno nuevo. [[CMP-007-executioncontroller|ExecutionController]] gana `allocateChildBudget`, `childBudgetWithinParent`, `requireChildWithinParent`, `rollUpChildUsage` y `sandboxLimitsExceeded`.

### Contratos

- [[C-057-executionusage|C-057 ExecutionUsage]] (promovido desde la estructura embebida de CH-07)
- [[C-012-executionbudget|C-012 ExecutionBudget]] v1 → v2 (ADR-004)

### Deuda

Resuelve D-026.

## Artículos constitucionales relevantes

P-09, P-35, INV-09, INV-E06, INV-E21

## Localización en el repo

`book/chapters/43-presupuestos-heredados/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
