---
id: "C-007"
tipo: contrato
nombre: "ModelResponse"
version: "v2"
capitulo: "CH-03"
tags: [contrato, c-007]
used_by: ["CMP-003", "CMP-008"]
modified_by: ["CH-39"]
articulos_constitucionales: ["P-10", "P-13", "INV-03"]
---

# ModelResponse (C-007)

> Contrato **v2** — introducido en [[ch-03-model-gateway|CH-03]], modificado en [[ch-39-modelo-como-dato|CH-39]].

## Definición canónica

```text
STRUCT ModelResponse
    finished: Boolean
    content: Optional<Value>
    proposedToolCall: Optional<RawToolCallProposal>
    proposedToolCalls: List<RawToolCallProposal>
    usage: Optional<UsageRecord>
    producedAt: Timestamp
END
```

## Usado por

[[CMP-003-modelgateway|CMP-003]], [[CMP-008-capabilityregistry|CMP-008]]

## Modificado por

[[ch-39-modelo-como-dato|CH-39]]: agrega `proposedToolCalls` (todas las propuestas; `proposedToolCall` es la primera) y `usage` (UsageRecord)

## Impacto constitucional

P-10, P-13, INV-03

## Contexto del libro

- Introducido en: [[ch-03-model-gateway|CH-03]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
