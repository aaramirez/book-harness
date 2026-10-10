---
id: "C-018"
tipo: contrato
nombre: "CapabilityDescriptor"
version: "v3"
capitulo: "CH-08"
tags: [contrato, c-018]
used_by: ["CMP-008", "CMP-015", "CMP-026", "CMP-028"]
modified_by: ["CH-30", "CH-41"]
articulos_constitucionales: ["P-03", "P-26", "INV-04", "INV-20"]
---

# CapabilityDescriptor (C-018)

> Contrato **v3** — introducido en [[ch-08-capability-registry|CH-08]], modificado en [[ch-30-politica-de-replay|CH-30]] (ADR-002) y en [[ch-41-conexiones|CH-41]] (ADR-005).

## Definición canónica

```text
STRUCT CapabilityDescriptor
    capability: CapabilityId
    name: Text
    version: Text
    inputSchema: Value
    implementationRef: Text
    replayPolicy: Optional<ReplayPolicy>
    sourceConnectionId: Optional<ConnectionId>
    executionKind: Optional<ExecutionKind>
END
```

## Usado por

[[CMP-008-capabilityregistry|CMP-008]], [[CMP-015-idempotencyguard|CMP-015]], [[CMP-026-isolatedexecutionenvironment|CMP-026]], [[CMP-028-connectionmanager|CMP-028]]

## Modificado por

[[ch-30-politica-de-replay|CH-30]]: agrega `replayPolicy` (ver [[C-039-replaypolicy|ReplayPolicy]]; NULL = NEVER)

[[ch-41-conexiones|CH-41]]: agrega `sourceConnectionId` (de qué conexión viene; NULL = local) y `executionKind` (LOCAL / ISOLATED / CONNECTION; NULL se deriva)

## Impacto constitucional

P-03, P-26, INV-04, INV-20

## Contexto del libro

- Introducido en: [[ch-08-capability-registry|CH-08]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
