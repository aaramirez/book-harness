---
id: "C-054"
tipo: contrato
nombre: "ConnectionDescriptor"
version: "v1"
capitulo: "CH-41"
tags: [contrato, c-054]
used_by: ["CMP-028"]
modified_by: []
articulos_constitucionales: ["P-38", "INV-E08", "INV-E25"]
---

# ConnectionDescriptor (C-054)

> Contrato v1 — introducido en [[ch-41-conexiones|CH-41]].

## Definición canónica

```text
STRUCT ConnectionDescriptor
    connectionId: ConnectionId
    kind: ConnectionKind
    transport: ConnectionTransport
    endpointRef: Text
    toolFilter: ToolFilter
    providedArguments: Map<Text, Value>
    credentialName: Optional<Text>
    credentialScope: CredentialScope
    requiresApprovalByDefault: Boolean
END
```

## Usado por

[[CMP-028-connectionmanager|CMP-028]]

## Modificado por

Ninguno

## Impacto constitucional

P-38, INV-E08, INV-E25

## Contexto del libro

- Introducido en: [[ch-41-conexiones|CH-41]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
