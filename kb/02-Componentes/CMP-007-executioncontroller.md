---
id: "CMP-007"
tipo: componente
nombre: "ExecutionController"
capitulo: "CH-07"
tags: [componente, cmp-007]
consumes: ["C-003", "C-004", "C-012"]
produces: ["C-010", "C-011", "C-017"]
articulos_constitucionales: ["P-10", "INV-08", "INV-09", "INV-10", "INV-18", "INV-19", "INV-20"]
---

# ExecutionController (CMP-007)

> Componente introducido en [[ch-07-execution-controller|CH-07]] — parte del runtime del arnés.

## Responsabilidad

Evaluar si un AgentRun puede continuar operacionalmente contra su ExecutionBudget — turnos, tool calls, tokens, costo, runtime y concurrencia — o si fue cancelado explícitamente, produciendo una ExecutionDecision determinística de tres resultados posibles (continue/stop/cancelled) con el uso actual siempre trazable — sin decidir si otro turno de razonamiento cognitivo debe ocurrir, sin ejecutar tools/side effects, sin evaluar policy/autorización y sin invocar al modelo.

## Decisiones que posee (owns)

- budgets
- cancellation
- deadlines
- runtime limits
- operational continuation

## Decisiones que NO posee (does_not_own)

- decidir si otro turno de razonamiento cognitivo debe ocurrir (AgentLoop, CMP-001, ya introducido en CH-01 — Article IV: "AgentLoop → Should another reasoning turn occur?"; distinción constitucional literal: ExecutionController decide si la ejecución PUEDE continuar operacionalmente frente a sus límites, AgentLoop decide si DEBE continuar cognitivamente — ninguna de las dos preguntas sustituye a la otra)
- ejecutar tools/side effects (ToolRuntime, CMP-002, ya introducido en CH-02)
- evaluar policy/autorización de una acción (PolicyEngine, CMP-005, ya introducido en CH-05)
- invocar al modelo seleccionado (ModelGateway, CMP-003, ya introducido en CH-03)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-003-agentstate|C-003]], [[C-004-executioncontext|C-004]], [[C-012-executionbudget|C-012]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-017-executiondecision|C-017]] |

## Artículos constitucionales

P-10, INV-08, INV-09, INV-10, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-07-execution-controller|CH-07]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
