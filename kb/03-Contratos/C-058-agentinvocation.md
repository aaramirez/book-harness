---
id: "C-058"
tipo: contrato
nombre: "AgentInvocation"
version: "v1"
capitulo: "CH-44"
tags: [contrato, c-058]
used_by: ["CMP-013"]
modified_by: []
articulos_constitucionales: ["P-20", "P-21", "INV-E03", "INV-E06", "INV-E21"]
---

# AgentInvocation (C-058)

> Contrato v1 — introducido en [[ch-44-invocacion-entre-agentes|CH-44]].

## Definición canónica

```text
STRUCT AgentInvocation
    invocationId: AgentInvocationId
    boundary: AgentCommunicationBoundary
    parentRunId: RunId
    targetAgentRef: Text
    skill: Text
    owner: Principal
    depth: Integer
    childRunId: Optional<RunId>
    remoteTaskRef: Optional<Text>
    status: AgentInvocationStatus
    budget: ExecutionBudget
    pendingWaitId: Optional<WaitId>
    result: Optional<Value>
    error: Optional<HarnessError>
    openedAt: Timestamp
    expiresAt: Optional<Timestamp>
END
```

## Usado por

[[CMP-013-agentcommunicationgateway|CMP-013]]

## Modificado por

Ninguno

## Impacto constitucional

P-20, P-21, INV-E03, INV-E06, INV-E21

## Contexto del libro

- Introducido en: [[ch-44-invocacion-entre-agentes|CH-44]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
