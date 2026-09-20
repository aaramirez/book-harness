---
id: "C-025"
tipo: contrato
nombre: "DelegationGrant"
version: "v1"
capitulo: "CH-15"
tags: [contrato, c-025]
used_by: ["CMP-013"]
modified_by: []
articulos_constitucionales: ["P-21", "INV-E06", "INV-19"]
---

# DelegationGrant (C-025)

> Contrato v1 — introducido en [[ch-15-agent-communication-gateway|CH-15]].

## Definición canónica

```text
STRUCT DelegationGrant
    id: DelegationGrantId
    delegatingRunId: Optional<RunId>
    delegatorRef: Text
    delegateRef: Text
    delegatedScope: List<Text>
    budget: ExecutionBudget
    expiresAt: Timestamp
    grantedAt: Timestamp
END
```

## Usado por

[[CMP-013-agentcommunicationgateway|CMP-013]]

## Modificado por

Ninguno

## Impacto constitucional

P-21, INV-E06, INV-19

## Contexto del libro

- Introducido en: [[ch-15-agent-communication-gateway|CH-15]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
