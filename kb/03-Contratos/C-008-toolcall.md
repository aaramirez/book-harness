---
id: "C-008"
tipo: contrato
nombre: "ToolCall"
version: "v1"
capitulo: "CH-02"
tags: [contrato, c-008]
used_by: ["CMP-002", "CMP-005", "CMP-008"]
modified_by: []
articulos_constitucionales: ["P-03", "INV-04", "INV-05"]
---

# ToolCall (C-008)

> Contrato v1 — introducido en [[ch-02-tool-runtime|CH-02]].

## Definición canónica

```text
STRUCT ToolCall
    id: ToolCallId
    capability: CapabilityId
    arguments: Map<Text, Value>
    requestedAt: Timestamp
END
```

## Usado por

[[CMP-002-toolruntime|CMP-002]], [[CMP-005-policyengine|CMP-005]], [[CMP-008-capabilityregistry|CMP-008]]

## Modificado por

Ninguno

## Impacto constitucional

P-03, INV-04, INV-05

## Contexto del libro

- Introducido en: [[ch-02-tool-runtime|CH-02]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
