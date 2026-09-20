---
id: "C-024"
tipo: contrato
nombre: "AgentCommunicationMessage"
version: "v1"
capitulo: "CH-15"
tags: [contrato, c-024]
used_by: ["CMP-013"]
modified_by: []
articulos_constitucionales: ["P-18", "P-20", "INV-E03", "INV-E04"]
---

# AgentCommunicationMessage (C-024)

> Contrato v1 — introducido en [[ch-15-agent-communication-gateway|CH-15]].

## Definición canónica

```text
STRUCT AgentCommunicationMessage
    id: AgentCommunicationMessageId
    boundary: AgentCommunicationBoundary
    sourceAgentRef: Text
    targetAgentRef: Text
    content: Value
    delegationGrantId: Optional<DelegationGrantId>
    traceId: TraceId
    sentAt: Timestamp
END
```

## Usado por

[[CMP-013-agentcommunicationgateway|CMP-013]]

## Modificado por

Ninguno

## Impacto constitucional

P-18, P-20, INV-E03, INV-E04

## Contexto del libro

- Introducido en: [[ch-15-agent-communication-gateway|CH-15]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
