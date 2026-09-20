---
id: "C-010"
tipo: contrato
nombre: "AgentEvent"
version: "v1"
capitulo: "CH-00"
tags: [contrato, c-010]
used_by: ["CMP-001", "CMP-002", "CMP-003", "CMP-004", "CMP-005", "CMP-006", "CMP-007", "CMP-008", "CMP-009"]
modified_by: []
articulos_constitucionales: ["P-04", "INV-18", "INV-19"]
---

# AgentEvent (C-010)

> Contrato v1 — introducido en [[ch-00-constitucion|CH-00]].

## Definición canónica

```text
STRUCT AgentEvent
    eventId: EventId
    eventType: AgentEventType
    timestamp: Timestamp
    runId: RunId
    sessionId: SessionId
    agentId: AgentId
    traceId: TraceId
    payload: Value
END
```

## Usado por

[[CMP-001-agentloop|CMP-001]], [[CMP-002-toolruntime|CMP-002]], [[CMP-003-modelgateway|CMP-003]], [[CMP-004-contextengine|CMP-004]], [[CMP-005-policyengine|CMP-005]], [[CMP-006-humaninteractionservice|CMP-006]], [[CMP-007-executioncontroller|CMP-007]], [[CMP-008-capabilityregistry|CMP-008]], [[CMP-009-eventbus|CMP-009]]

## Modificado por

Ninguno

## Impacto constitucional

P-04, INV-18, INV-19

## Contexto del libro

- Introducido en: [[ch-00-constitucion|CH-00]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
