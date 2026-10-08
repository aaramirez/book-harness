---
id: "C-050"
tipo: contrato
nombre: "UsageRecord"
version: "v1"
capitulo: "CH-39"
tags: [contrato, c-050]
used_by: ["CMP-003", "CMP-020"]
modified_by: []
articulos_constitucionales: ["P-29", "INV-09", "INV-E10"]
---

# UsageRecord (C-050)

> Contrato v1 — introducido en [[ch-39-modelo-como-dato|CH-39]].

## Definición canónica

```text
STRUCT UsageRecord
    modelId: Text
    descriptorVersion: Text
    inputTokens: Integer
    outputTokens: Integer
    cacheReadTokens: Integer
    cacheWriteTokens: Integer
    cost: Number
    currency: Text
    recordedAt: Timestamp
END
```

## Usado por

[[CMP-003-modelgateway|CMP-003]], [[CMP-020-evaluationharness|CMP-020]]

## Modificado por

Ninguno

## Impacto constitucional

P-29, INV-09, INV-E10

## Contexto del libro

- Introducido en: [[ch-39-modelo-como-dato|CH-39]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
