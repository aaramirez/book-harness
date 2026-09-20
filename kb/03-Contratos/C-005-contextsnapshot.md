---
id: "C-005"
tipo: contrato
nombre: "ContextSnapshot"
version: "v1"
capitulo: "CH-04"
tags: [contrato, c-005]
used_by: ["CMP-004"]
modified_by: []
articulos_constitucionales: ["P-01", "P-14", "INV-09"]
---

# ContextSnapshot (C-005)

> Contrato v1 — introducido en [[ch-04-context-engine|CH-04]].

## Definición canónica

```text
STRUCT ContextSnapshot
    blocks: List<ContextBlock>
    budget: ExecutionBudget
    estimatedTokens: Integer
    producedAt: Timestamp
END
```

## Usado por

[[CMP-004-contextengine|CMP-004]]

## Modificado por

Ninguno

## Impacto constitucional

P-01, P-14, INV-09

## Contexto del libro

- Introducido en: [[ch-04-context-engine|CH-04]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
