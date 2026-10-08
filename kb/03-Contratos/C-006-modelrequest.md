---
id: "C-006"
tipo: contrato
nombre: "ModelRequest"
version: "v2"
capitulo: "CH-03"
tags: [contrato, c-006]
used_by: ["CMP-003"]
modified_by: ["CH-39"]
articulos_constitucionales: ["P-01", "P-02", "INV-02"]
---

# ModelRequest (C-006)

> Contrato **v2** — introducido en [[ch-03-model-gateway|CH-03]], modificado en [[ch-39-modelo-como-dato|CH-39]].

## Definición canónica

```text
STRUCT ModelRequest
    messages: List<AgentMessage>
    budget: ExecutionBudget
    cacheRetention: Optional<CacheRetention>
    requestedAt: Timestamp
END
```

## Usado por

[[CMP-003-modelgateway|CMP-003]]

## Modificado por

[[ch-39-modelo-como-dato|CH-39]]: agrega `cacheRetention` (NONE / SHORT / LONG; NULL = sin cache, como en v1)

## Impacto constitucional

P-01, P-02, INV-02

## Contexto del libro

- Introducido en: [[ch-03-model-gateway|CH-03]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
