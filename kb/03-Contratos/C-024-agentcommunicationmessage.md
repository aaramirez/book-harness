---
id: "C-024"
tipo: contrato
nombre: "AgentCommunicationMessage"
version: "v2"
capitulo: "CH-15"
tags: [contrato, c-024]
used_by: ["CMP-013"]
modified_by: ["CH-44"]
articulos_constitucionales: ["P-18", "P-20", "INV-E03", "INV-E04"]
---

# AgentCommunicationMessage (C-024)

> Contrato **v2** — introducido en [[ch-15-agent-communication-gateway|CH-15]], modificado en [[ch-44-invocacion-entre-agentes|CH-44]].

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
    invocationId: Optional<AgentInvocationId>
END
```

## Usado por

[[CMP-013-agentcommunicationgateway|CMP-013]]

## Modificado por

[[ch-44-invocacion-entre-agentes|CH-44]]: agrega `invocationId` (opcional; NULL = mensaje suelto, como en v1), para que un mensaje pertenezca a una [[C-058-agentinvocation|invocación durable]].

## Impacto constitucional

P-18, P-20, INV-E03, INV-E04

## Contexto del libro

- Introducido en: [[ch-15-agent-communication-gateway|CH-15]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
