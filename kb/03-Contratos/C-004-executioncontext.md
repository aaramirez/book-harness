---
id: "C-004"
tipo: contrato
nombre: "ExecutionContext"
version: "v1"
capitulo: "CH-00"
tags: [contrato, c-004]
used_by: ["CMP-001", "CMP-002", "CMP-003", "CMP-004", "CMP-005", "CMP-006", "CMP-007", "CMP-008", "CMP-010", "CMP-011", "CMP-016"]
modified_by: []
articulos_constitucionales: ["P-01", "P-14"]
---

# ExecutionContext (C-004)

> Contrato v1 — introducido en [[ch-00-constitucion|CH-00]].

## Definición canónica

```text
STRUCT ExecutionContext
    runId: RunId
    sessionId: SessionId
    traceId: TraceId
    budget: ExecutionBudget
END
```

## Usado por

[[CMP-001-agentloop|CMP-001]], [[CMP-002-toolruntime|CMP-002]], [[CMP-003-modelgateway|CMP-003]], [[CMP-004-contextengine|CMP-004]], [[CMP-005-policyengine|CMP-005]], [[CMP-006-humaninteractionservice|CMP-006]], [[CMP-007-executioncontroller|CMP-007]], [[CMP-008-capabilityregistry|CMP-008]], [[CMP-010-sessionmanager|CMP-010]], [[CMP-011-agentcore|CMP-011]], [[CMP-016-operationalcontroller|CMP-016]]

## Modificado por

Ninguno

## Impacto constitucional

P-01, P-14

## Contexto del libro

- Introducido en: [[ch-00-constitucion|CH-00]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
