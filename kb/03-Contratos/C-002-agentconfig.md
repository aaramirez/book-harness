---
id: "C-002"
tipo: contrato
nombre: "AgentConfig"
version: "v1"
capitulo: "CH-00"
tags: [contrato, c-002]
used_by: ["CMP-001", "CMP-011"]
modified_by: []
articulos_constitucionales: ["P-06"]
---

# AgentConfig (C-002)

> Contrato v1 — introducido en [[ch-00-constitucion|CH-00]].

## Definición canónica

```text
STRUCT AgentConfig
    agentId: AgentId
    name: Text
    budget: ExecutionBudget
END
```

## Usado por

[[CMP-001-agentloop|CMP-001]], [[CMP-011-agentcore|CMP-011]]

## Modificado por

Ninguno

## Impacto constitucional

P-06

## Contexto del libro

- Introducido en: [[ch-00-constitucion|CH-00]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
