---
id: "C-021"
tipo: contrato
nombre: "AgentActivationRequest"
version: "v1"
capitulo: "CH-11"
tags: [contrato, c-021]
used_by: ["CMP-011"]
modified_by: []
articulos_constitucionales: ["P-06", "P-10", "INV-08", "INV-09"]
---

# AgentActivationRequest (C-021)

> Contrato v1 — introducido en [[ch-11-agent-core|CH-11]].

## Definición canónica

```text
STRUCT AgentActivationRequest
    agentId: AgentId
    sessionId: Optional<SessionId>
    input: Value
    requestedAt: Timestamp
END
```

## Usado por

[[CMP-011-agentcore|CMP-011]]

## Modificado por

Ninguno

## Impacto constitucional

P-06, P-10, INV-08, INV-09

## Contexto del libro

- Introducido en: [[ch-11-agent-core|CH-11]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
