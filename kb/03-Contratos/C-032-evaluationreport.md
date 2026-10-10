---
id: "C-032"
tipo: contrato
nombre: "EvaluationReport"
version: "v2"
capitulo: "CH-22"
tags: [contrato, c-032]
used_by: ["CMP-020"]
modified_by: ["CH-47"]
articulos_constitucionales: ["P-28", "INV-E13", "INV-19"]
---

# EvaluationReport (C-032)

> Contrato **v2** — introducido en [[ch-22-evaluation-harness|CH-22]], modificado en [[ch-47-evaluacion-con-lift|CH-47]].

## Definición canónica

```text
STRUCT EvaluationReport
    id: EvaluationReportId
    subjectRef: Text
    riskClass: RiskClass
    certificationRequired: Boolean
    outcome: EvaluationOutcome
    evaluatedAt: Timestamp
    evidence: List<LiftReportId>
END
```

## Usado por

[[CMP-020-evaluationharness|CMP-020]]

## Modificado por

[[ch-47-evaluacion-con-lift|CH-47]]: agrega `evidence` (los [[C-064-liftreport|LiftReport]] en que se apoya el resultado; vacía si falta, como en v1).

## Impacto constitucional

P-28, INV-E13, INV-19

## Contexto del libro

- Introducido en: [[ch-22-evaluation-harness|CH-22]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
