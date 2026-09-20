---
id: "C-033"
tipo: contrato
nombre: "BusinessOutcomeCorrelation"
version: "v1"
capitulo: "CH-22"
tags: [contrato, c-033]
used_by: ["CMP-020"]
modified_by: []
articulos_constitucionales: ["P-29", "INV-19"]
---

# BusinessOutcomeCorrelation (C-033)

> Contrato v1 — introducido en [[ch-22-evaluation-harness|CH-22]].

## Definición canónica

```text
STRUCT BusinessOutcomeCorrelation
    id: BusinessOutcomeCorrelationId
    runId: RunId
    measuredOutcome: Text
    slaRef: Optional<Text>
    humanEscalationRef: Optional<HumanInteractionRequestId>
    correlatedAt: Timestamp
END
```

## Usado por

[[CMP-020-evaluationharness|CMP-020]]

## Modificado por

Ninguno

## Impacto constitucional

P-29, INV-19

## Contexto del libro

- Introducido en: [[ch-22-evaluation-harness|CH-22]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
