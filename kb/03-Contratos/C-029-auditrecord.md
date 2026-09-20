---
id: "C-029"
tipo: contrato
nombre: "AuditRecord"
version: "v1"
capitulo: "CH-19"
tags: [contrato, c-029]
used_by: ["CMP-017"]
modified_by: []
articulos_constitucionales: ["P-25", "INV-19", "INV-E10"]
---

# AuditRecord (C-029)

> Contrato v1 — introducido en [[ch-19-audit-ledger|CH-19]].

## Definición canónica

```text
STRUCT AuditRecord
    id: AuditRecordId
    subjectRef: Text
    versionSnapshot: VersionSnapshot
    actor: ActorId
    context: Optional<TraceId>
    recordedAt: Timestamp
    contentHash: Text
END
```

## Usado por

[[CMP-017-auditledger|CMP-017]]

## Modificado por

Ninguno

## Impacto constitucional

P-25, INV-19, INV-E10

## Contexto del libro

- Introducido en: [[ch-19-audit-ledger|CH-19]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
