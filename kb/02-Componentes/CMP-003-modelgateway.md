---
id: "CMP-003"
tipo: componente
nombre: "ModelGateway"
capitulo: "CH-03"
tags: [componente, cmp-003]
consumes: ["C-001", "C-004", "C-006"]
produces: ["C-007", "C-010", "C-011"]
articulos_constitucionales: ["P-01", "P-02", "P-10", "P-12", "P-13", "INV-01", "INV-02", "INV-03", "INV-18", "INV-19", "INV-20"]
---

# ModelGateway (CMP-003)

> Componente introducido en [[ch-03-model-gateway|CH-03]] — parte del runtime del arnés.

## Responsabilidad

Seleccionar el provider de modelo correspondiente, adaptar los AgentMessage de un turno (más los límites de generación relevantes) hacia el ModelRequest que ese provider espera, invocar al modelo, soportar streaming y normalizar la respuesta cruda del provider hacia un ModelResponse — sin decidir si otro turno de razonamiento debe ocurrir, sin ejecutar ninguna tool call y sin resolver ninguna propuesta de acción hacia un ToolCall validado.

## Decisiones que posee (owns)

- selección de provider
- adaptación de mensajes
- invocación del modelo
- streaming
- normalización de respuestas

## Decisiones que NO posee (does_not_own)

- decidir si otro turno de razonamiento debe ocurrir (AgentLoop, CMP-001, ya introducido en CH-01)
- ejecutar tools/side effects (ToolRuntime, CMP-002, ya introducido en CH-02)
- seleccionar/rankear/componer contexto (ContextEngine, Article III — no introducido en este capítulo, es un componente distinto)
- policy/autorización de una acción (PolicyEngine, Article IV — no introducido en este capítulo)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-001-agentmessage|C-001]], [[C-004-executioncontext|C-004]], [[C-006-modelrequest|C-006]] |
| 🡐 Produce | [[C-007-modelresponse|C-007]], [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]] |

## Artículos constitucionales

P-01, P-02, P-10, P-12, P-13, INV-01, INV-02, INV-03, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-03-model-gateway|CH-03]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
