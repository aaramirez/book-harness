---
id: "C-039"
tipo: contrato
nombre: "ReplayPolicy"
version: "v1"
capitulo: "CH-30"
tags: [contrato, c-039]
used_by: ["CMP-008", "CMP-015"]
modified_by: []
articulos_constitucionales: ["P-24", "INV-E09", "INV-E17"]
---

# ReplayPolicy (C-039)

> Contrato v1 — introducido en [[ch-30-politica-de-replay|CH-30]].

## Definición canónica

```text
ENUM ReplayPolicy
    NEVER
    SAFE
END
```

## Usado por

[[CMP-008-capabilityregistry|CMP-008]] · [[CMP-015-idempotencyguard|CMP-015]]

## Modificado por

Ninguno

## Impacto constitucional

P-24, INV-E09, INV-E17

## Contexto del libro

- Introducido en: [[ch-30-politica-de-replay|CH-30]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
