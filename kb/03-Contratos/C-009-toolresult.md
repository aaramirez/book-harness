---
id: "C-009"
tipo: contrato
nombre: "ToolResult"
version: "v1"
capitulo: "CH-02"
tags: [contrato, c-009]
used_by: ["CMP-002"]
modified_by: []
articulos_constitucionales: ["INV-07", "INV-20", "P-04"]
---

# ToolResult (C-009)

> Contrato v1 — introducido en [[ch-02-tool-runtime|CH-02]].

## Definición canónica

```text
STRUCT ToolResult
    callId: ToolCallId
    succeeded: Boolean
    output: Optional<Value>
    error: Optional<HarnessError>
    completedAt: Timestamp
END
```

## Usado por

[[CMP-002-toolruntime|CMP-002]]

## Modificado por

Ninguno

## Impacto constitucional

INV-07, INV-20, P-04

## Contexto del libro

- Introducido en: [[ch-02-tool-runtime|CH-02]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
