---
id: "C-052"
tipo: contrato
nombre: "HookPoint"
version: "v1"
capitulo: "CH-40"
tags: [contrato, c-052]
used_by: ["CMP-027"]
modified_by: []
articulos_constitucionales: ["P-12", "INV-E24"]
---

# HookPoint (C-052)

> Contrato v1 — introducido en [[ch-40-extension-host|CH-40]].

## Definición canónica

```text
ENUM HookPoint
    BEFORE_RUN
    TRANSFORM_CONTEXT
    BEFORE_REQUEST
    AFTER_RESPONSE
    BEFORE_TOOL
    AFTER_TOOL
    BEFORE_COMPACTION
    BEFORE_NAVIGATION
END
```

## Usado por

[[CMP-027-extensionhost|CMP-027]]

## Modificado por

Ninguno

## Impacto constitucional

P-12, INV-E24

## Contexto del libro

- Introducido en: [[ch-40-extension-host|CH-40]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
