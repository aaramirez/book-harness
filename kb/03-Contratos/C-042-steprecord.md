---
id: "C-042"
tipo: contrato
nombre: "StepRecord"
version: "v1"
capitulo: "CH-32"
tags: [contrato, c-042]
used_by: ["CMP-023"]
modified_by: []
articulos_constitucionales: ["P-23", "P-32", "INV-13", "INV-E16"]
---

# StepRecord (C-042)

> Contrato v1 — introducido en [[ch-32-pasos-durables|CH-32]].

## Definición canónica

```text
STRUCT StepRecord
    stepId: StepId
    runId: RunId
    turn: Integer
    index: Integer
    status: StepStatus
    partialOutput: Optional<Value>
    modelResponse: Optional<ModelResponse>
    toolCall: Optional<ToolCall>
    toolResult: Optional<ToolResult>
    startedAt: Timestamp
    committedAt: Optional<Timestamp>
END
```

## Usado por

[[CMP-023-executionjournal|CMP-023]]

## Modificado por

Ninguno

## Impacto constitucional

P-23, P-32, INV-13, INV-E16

## Contexto del libro

- Introducido en: [[ch-32-pasos-durables|CH-32]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
