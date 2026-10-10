---
id: "C-064"
tipo: contrato
nombre: "LiftReport"
version: "v1"
capitulo: "CH-47"
tags: [contrato, c-064]
used_by: ["CMP-020"]
modified_by: []
articulos_constitucionales: ["P-28", "INV-19", "INV-E07", "INV-E13"]
---

# LiftReport (C-064)

> Contrato v1 — introducido en [[ch-47-evaluacion-con-lift|CH-47]].

## Definición canónica

```text
STRUCT LiftReport
    reportId: LiftReportId
    baselineRef: Text
    treatmentRef: Text
    metric: Text
    scores: List<CaseScore>
    lift: Number
    minimumLift: Number
    verdict: LiftVerdict
    isolationRef: Text
    producedAt: Timestamp
END
```

## Usado por

[[CMP-020-evaluationharness|CMP-020]]

## Modificado por

Ninguno

## Impacto constitucional

P-28, INV-19, INV-E07, INV-E13

## Contexto del libro

- Introducido en: [[ch-47-evaluacion-con-lift|CH-47]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
