---
id: "C-036"
tipo: contrato
nombre: "PendingInput"
version: "v1"
capitulo: "CH-28"
tags: [contrato, c-036]
used_by: ["CMP-001"]
modified_by: []
articulos_constitucionales: ["P-10", "INV-08", "INV-07"]
---

# PendingInput (C-036)

> Contrato v1 — introducido en [[ch-28-steering-follow-up|CH-28]].

## Definición canónica

```text
STRUCT PendingInput
    id: PendingInputId
    runId: RunId
    kind: PendingInputKind
    message: AgentMessage
    receivedAt: Timestamp
END
```

## Usado por

[[CMP-001-agentloop|CMP-001]]

## Modificado por

Ninguno

## Impacto constitucional

P-10, INV-08, INV-07

## Contexto del libro

- Introducido en: [[ch-28-steering-follow-up|CH-28]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
