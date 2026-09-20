---
id: "C-022"
tipo: contrato
nombre: "ActivationRequest"
version: "v1"
capitulo: "CH-14"
tags: [contrato, c-022]
used_by: ["CMP-012"]
modified_by: []
articulos_constitucionales: ["P-16", "INV-E01"]
---

# ActivationRequest (C-022)

> Contrato v1 — introducido en [[ch-14-admission-controller|CH-14]].

## Definición canónica

```text
STRUCT ActivationRequest
    id: ActivationRequestId
    sourceRef: Text
    externalIdentityRef: Text
    payload: Value
    receivedAt: Timestamp
END
```

## Usado por

[[CMP-012-admissioncontroller|CMP-012]]

## Modificado por

Ninguno

## Impacto constitucional

P-16, INV-E01

## Contexto del libro

- Introducido en: [[ch-14-admission-controller|CH-14]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
