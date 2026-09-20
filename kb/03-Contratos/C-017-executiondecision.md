---
id: "C-017"
tipo: contrato
nombre: "ExecutionDecision"
version: "v1"
capitulo: "CH-07"
tags: [contrato, c-017]
used_by: ["CMP-007"]
modified_by: []
articulos_constitucionales: ["P-10", "INV-08", "INV-09", "INV-10", "INV-18", "INV-19", "INV-20"]
---

# ExecutionDecision (C-017)

> Contrato v1 — introducido en [[ch-07-execution-controller|CH-07]].

## Definición canónica

```text
STRUCT ExecutionDecision
    runId: RunId
    outcome: ExecutionOutcome
    stopReason: Optional<ExecutionStopReason>
    reason: Optional<HarnessError>
    usage: ExecutionUsage
    evaluatedAt: Timestamp
END
```

## Usado por

[[CMP-007-executioncontroller|CMP-007]]

## Modificado por

Ninguno

## Impacto constitucional

P-10, INV-08, INV-09, INV-10, INV-18, INV-19, INV-20

## Contexto del libro

- Introducido en: [[ch-07-execution-controller|CH-07]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
