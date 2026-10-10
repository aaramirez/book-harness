---
id: "C-066"
tipo: contrato
nombre: "AuthoringDiagnostic"
version: "v1"
capitulo: "CH-48"
tags: [contrato, c-066]
used_by: ["CMP-011"]
modified_by: []
articulos_constitucionales: ["P-39", "INV-E27"]
---

# AuthoringDiagnostic (C-066)

> Contrato v1 — introducido en [[ch-48-agente-como-directorio|CH-48]].

## Definición canónica

```text
STRUCT AuthoringDiagnostic
    level: DiagnosticLevel
    code: Text
    path: Text
    message: Text
END
```

## Usado por

[[CMP-011-agentcore|CMP-011]]

## Modificado por

Ninguno

## Impacto constitucional

P-39, INV-E27

## Contexto del libro

- Introducido en: [[ch-48-agente-como-directorio|CH-48]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
