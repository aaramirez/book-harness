---
id: "C-063"
tipo: contrato
nombre: "TelemetrySpan"
version: "v1"
capitulo: "CH-46"
tags: [contrato, c-063]
used_by: ["CMP-009", "CMP-018"]
modified_by: []
articulos_constitucionales: ["P-04", "P-25", "INV-E23"]
---

# TelemetrySpan (C-063)

> Contrato v1 — introducido en [[ch-46-observabilidad-por-audiencia|CH-46]].

## Definición canónica

```text
STRUCT TelemetrySpan
    spanId: SpanId
    traceId: TraceId
    parentSpanId: Optional<SpanId>
    sessionId: SessionId
    name: Text
    startedAt: Timestamp
    endedAt: Optional<Timestamp>
    attributes: Map<Text, Value>
    body: Optional<Value>
    classification: DataClassificationLevel
    redacted: Boolean
END
```

## Usado por

[[CMP-009-eventbus|CMP-009]], [[CMP-018-datagovernanceengine|CMP-018]]

## Modificado por

Ninguno

## Impacto constitucional

P-04, P-25, INV-E23

## Contexto del libro

- Introducido en: [[ch-46-observabilidad-por-audiencia|CH-46]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
