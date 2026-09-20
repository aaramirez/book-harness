---
id: "C-003"
tipo: contrato
nombre: "AgentState"
version: "v1"
capitulo: "CH-00"
tags: [contrato, c-003]
used_by: ["CMP-001", "CMP-004", "CMP-007", "CMP-010", "CMP-011", "CMP-016"]
modified_by: []
articulos_constitucionales: ["P-08", "P-10", "INV-12"]
---

# AgentState (C-003)

> Contrato v1 — introducido en [[ch-00-constitucion|CH-00]].

## Definición canónica

```text
STRUCT AgentState
    runId: RunId
    sessionId: SessionId
    agentId: AgentId
    status: AgentRunStatus
    currentTurn: Integer
END
```

## Usado por

[[CMP-001-agentloop|CMP-001]], [[CMP-004-contextengine|CMP-004]], [[CMP-007-executioncontroller|CMP-007]], [[CMP-010-sessionmanager|CMP-010]], [[CMP-011-agentcore|CMP-011]], [[CMP-016-operationalcontroller|CMP-016]]

## Modificado por

Ninguno

## Impacto constitucional

P-08, P-10, INV-12

## Contexto del libro

- Introducido en: [[ch-00-constitucion|CH-00]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
