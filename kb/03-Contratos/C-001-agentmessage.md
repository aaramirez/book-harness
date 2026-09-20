---
id: "C-001"
tipo: contrato
nombre: "AgentMessage"
version: "v1"
capitulo: "CH-00"
tags: [contrato, c-001]
used_by: ["CMP-003", "CMP-004"]
modified_by: []
articulos_constitucionales: ["P-02", "INV-02"]
---

# AgentMessage (C-001)

> Contrato v1 — introducido en [[ch-00-constitucion|CH-00]].

## Definición canónica

```text
STRUCT AgentMessage
    id: MessageId
    role: MessageRole
    content: Value
    timestamp: Timestamp
END
```

## Usado por

[[CMP-003-modelgateway|CMP-003]], [[CMP-004-contextengine|CMP-004]]

## Modificado por

Ninguno

## Impacto constitucional

P-02, INV-02

## Contexto del libro

- Introducido en: [[ch-00-constitucion|CH-00]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
