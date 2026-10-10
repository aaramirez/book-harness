---
id: "C-059"
tipo: contrato
nombre: "AgentCard"
version: "v1"
capitulo: "CH-44"
tags: [contrato, c-059]
used_by: ["CMP-013"]
modified_by: []
articulos_constitucionales: ["P-19", "P-20", "INV-E04", "INV-E05"]
---

# AgentCard (C-059)

> Contrato v1 — introducido en [[ch-44-invocacion-entre-agentes|CH-44]].

## Definición canónica

```text
STRUCT AgentCard
    agentRef: Text
    description: Text
    skills: List<Text>
    boundary: AgentCommunicationBoundary
    endpointRef: Optional<Text>
    authScheme: Optional<Text>
END
```

## Usado por

[[CMP-013-agentcommunicationgateway|CMP-013]]

## Modificado por

Ninguno

## Impacto constitucional

P-19, P-20, INV-E04, INV-E05

## Contexto del libro

- Introducido en: [[ch-44-invocacion-entre-agentes|CH-44]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
