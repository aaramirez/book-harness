---
id: "CH-47"
tipo: capitulo
titulo: "Medir el Aporte de un Cambio: Evaluación con Lift"
tags: [capitulo, ch47, v0-3]
introduces_components: []
introduces_contracts: ["C-064"]
modifies_contracts: ["C-032"]
articulos_constitucionales: ["P-28", "P-29", "INV-19", "INV-E07", "INV-E13"]
---

# CH-47 — Medir el Aporte de un Cambio: Evaluación con Lift

## Navegación

⬅ [[ch-46-observabilidad-por-audiencia|CH-46]] · **CH-47**

## Resultado esperado

Al terminar este capítulo podrás decidir si un cambio mejora al agente frente a la versión anterior, con casos suficientes y corridas aisladas, y explicar cómo esa comparación se convierte en la evidencia de una certificación.

## Qué introduce este capítulo

### Componentes

- Ninguno nuevo. [[CMP-020-evaluationharness|EvaluationHarness]] gana `requireIsolatedCase`, `computeLift`, `liftVerdict`, `certificationSignalFromLift` y `evaluateCandidateWithLift`.

### Contratos

- [[C-064-liftreport|C-064 LiftReport]]
- [[C-032-evaluationreport|C-032 EvaluationReport]] v1 → v2

### Deuda

Sin deudas con destino CH-47.

## Artículos constitucionales relevantes

P-28, P-29, INV-19, INV-E07, INV-E13

## Localización en el repo

`book/chapters/47-evaluacion-con-lift/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
