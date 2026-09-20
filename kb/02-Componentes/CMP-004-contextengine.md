---
id: "CMP-004"
tipo: componente
nombre: "ContextEngine"
capitulo: "CH-04"
tags: [componente, cmp-004]
consumes: ["C-001", "C-003", "C-004"]
produces: ["C-005", "C-010", "C-011"]
articulos_constitucionales: ["P-01", "P-04", "P-12", "P-14", "INV-02", "INV-09", "INV-18", "INV-19", "INV-20"]
---

# ContextEngine (CMP-004)

> Componente introducido en [[ch-04-context-engine|CH-04]] — parte del runtime del arnés.

## Responsabilidad

Seleccionar, rankear, componer y compactar el material candidato de un turno (AgentMessage, AgentState, ExecutionContext) dentro de un presupuesto de contexto explícito, devolviendo un ContextSnapshot que registra la procedencia (provenance) de cada bloque incluido — sin invocar al modelo, sin decidir si otro turno debe ocurrir, sin persistir historial de sesión y sin autorizar qué información puede verse.

## Decisiones que posee (owns)

- selección
- ranking
- composición
- compaction
- context budgets
- provenance

## Decisiones que NO posee (does_not_own)

- invocar al modelo seleccionado (ModelGateway, CMP-003, ya introducido en CH-03)
- decidir si otro turno de razonamiento debe ocurrir (AgentLoop, CMP-001, ya introducido en CH-01)
- persistir/recuperar historial de sesión y checkpoints (SessionManager, Article IV — no introducido en este capítulo, es un componente distinto)
- policy/autorización sobre qué información puede verse (PolicyEngine, Article IV — no introducido en este capítulo; distinto de seleccionar por relevancia, que sí le pertenece a ContextEngine)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-001-agentmessage|C-001]], [[C-003-agentstate|C-003]], [[C-004-executioncontext|C-004]] |
| 🡐 Produce | [[C-005-contextsnapshot|C-005]], [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]] |

## Artículos constitucionales

P-01, P-04, P-12, P-14, INV-02, INV-09, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-04-context-engine|CH-04]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
