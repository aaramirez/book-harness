---
id: "C-006"
tipo: contrato
nombre: "ModelRequest"
version: "v1"
capitulo: "CH-03"
tags: [contrato, c-006]
used_by: ["CMP-003"]
modified_by: []
articulos_constitucionales: ["P-01", "P-02", "INV-02"]
---

# ModelRequest (C-006)

> Contrato v1 — introducido en [[ch-03-model-gateway|CH-03]].

## Definición canónica

```text
STRUCT ModelRequest
    messages: List<AgentMessage>
    budget: ExecutionBudget
    requestedAt: Timestamp
END
```

## Usado por

[[CMP-003-modelgateway|CMP-003]]

## Modificado por

Ninguno

## Impacto constitucional

P-01, P-02, INV-02

## Contexto del libro

- Introducido en: [[ch-03-model-gateway|CH-03]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
