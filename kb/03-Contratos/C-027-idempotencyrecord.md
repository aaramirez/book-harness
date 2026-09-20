---
id: "C-027"
tipo: contrato
nombre: "IdempotencyRecord"
version: "v1"
capitulo: "CH-17"
tags: [contrato, c-027]
used_by: ["CMP-015"]
modified_by: []
articulos_constitucionales: ["INV-11", "P-24", "INV-E09"]
---

# IdempotencyRecord (C-027)

> Contrato v1 — introducido en [[ch-17-idempotency-guard|CH-17]].

## Definición canónica

```text
STRUCT IdempotencyRecord
    id: IdempotencyRecordId
    idempotencyKey: Text
    capability: CapabilityId
    originalToolCallId: ToolCallId
    status: IdempotencyRecordStatus
    result: Optional<ToolResult>
    createdAt: Timestamp
    completedAt: Optional<Timestamp>
END
```

## Usado por

[[CMP-015-idempotencyguard|CMP-015]]

## Modificado por

Ninguno

## Impacto constitucional

INV-11, P-24, INV-E09

## Contexto del libro

- Introducido en: [[ch-17-idempotency-guard|CH-17]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
