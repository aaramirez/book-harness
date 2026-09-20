---
id: "C-032"
tipo: contrato
nombre: "EvaluationReport"
version: "v1"
capitulo: "CH-22"
tags: [contrato, c-032]
used_by: ["CMP-020"]
modified_by: []
articulos_constitucionales: ["P-28", "INV-E13", "INV-19"]
---

# EvaluationReport (C-032)

> Contrato v1 — introducido en [[ch-22-evaluation-harness|CH-22]].

## Definición canónica

```text
STRUCT EvaluationReport
    id: EvaluationReportId
    subjectRef: Text
    riskClass: RiskClass
    certificationRequired: Boolean
    outcome: EvaluationOutcome
    evaluatedAt: Timestamp
END
```

## Usado por

[[CMP-020-evaluationharness|CMP-020]]

## Modificado por

Ninguno

## Impacto constitucional

P-28, INV-E13, INV-19

## Contexto del libro

- Introducido en: [[ch-22-evaluation-harness|CH-22]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
