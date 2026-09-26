---
id: "C-046"
tipo: contrato
nombre: "ContinuationAddress"
version: "v1"
capitulo: "CH-34"
tags: [contrato, c-046]
used_by: ["CMP-025"]
modified_by: []
articulos_constitucionales: ["P-34", "INV-E19"]
---

# ContinuationAddress (C-046)

> Contrato v1 — introducido en [[ch-34-canales-continuacion|CH-34]].

## Definición canónica

```text
STRUCT ContinuationAddress
    channelRef: Text
    conversationRef: Text
END
```

## Usado por

[[CMP-025-continuationregistry|CMP-025]]

## Modificado por

Ninguno

## Impacto constitucional

P-34, INV-E19

## Contexto del libro

- Introducido en: [[ch-34-canales-continuacion|CH-34]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
