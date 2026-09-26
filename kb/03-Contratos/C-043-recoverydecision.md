---
id: "C-043"
tipo: contrato
nombre: "RecoveryDecision"
version: "v1"
capitulo: "CH-32"
tags: [contrato, c-043]
used_by: ["CMP-023"]
modified_by: []
articulos_constitucionales: ["P-32", "INV-13", "INV-E16", "INV-E17", "INV-19"]
---

# RecoveryDecision (C-043)

> Contrato v1 — introducido en [[ch-32-pasos-durables|CH-32]].

## Definición canónica

```text
STRUCT RecoveryDecision
    runId: RunId
    stepId: StepId
    action: RecoveryAction
    pendingToolCall: Optional<ToolCallId>
    decidedAt: Timestamp
END
```

## Usado por

[[CMP-023-executionjournal|CMP-023]]

## Modificado por

Ninguno

## Impacto constitucional

P-32, INV-13, INV-E16, INV-E17, INV-19

## Contexto del libro

- Introducido en: [[ch-32-pasos-durables|CH-32]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
