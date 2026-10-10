---
id: "C-061"
tipo: contrato
nombre: "SessionAudience"
version: "v1"
capitulo: "CH-46"
tags: [contrato, c-061]
used_by: ["CMP-018"]
modified_by: []
articulos_constitucionales: ["P-37", "INV-E23"]
---

# SessionAudience (C-061)

> Contrato v1 — introducido en [[ch-46-observabilidad-por-audiencia|CH-46]].

## Definición canónica

```text
STRUCT SessionAudience
    sessionId: SessionId
    kind: AudienceKind
    decidedBy: Text
    decidedAt: Timestamp
END
```

## Usado por

[[CMP-018-datagovernanceengine|CMP-018]]

## Modificado por

Ninguno

## Impacto constitucional

P-37, INV-E23

## Contexto del libro

- Introducido en: [[ch-46-observabilidad-por-audiencia|CH-46]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
