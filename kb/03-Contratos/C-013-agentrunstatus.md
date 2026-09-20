---
id: "C-013"
tipo: contrato
nombre: "AgentRunStatus"
version: "v1"
capitulo: "CH-01"
tags: [contrato, c-013]
used_by: ["CMP-001", "CMP-016"]
modified_by: []
articulos_constitucionales: ["P-10", "INV-08", "INV-09"]
---

# AgentRunStatus (C-013)

> Contrato v1 — introducido en [[ch-01-agent-loop|CH-01]].

## Definición canónica

```text
ENUM AgentRunStatus
    CREATED
    INITIALIZING
    RUNNING
    WAITING_FOR_MODEL
    WAITING_FOR_TOOL
    WAITING_FOR_HUMAN
    PAUSED
    COMPLETED
    FAILED
    CANCELLED
    EXPIRED
END
```

## Usado por

[[CMP-001-agentloop|CMP-001]], [[CMP-016-operationalcontroller|CMP-016]]

## Modificado por

Ninguno

## Impacto constitucional

P-10, INV-08, INV-09

## Contexto del libro

- Introducido en: [[ch-01-agent-loop|CH-01]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
