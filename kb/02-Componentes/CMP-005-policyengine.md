---
id: "CMP-005"
tipo: componente
nombre: "PolicyEngine"
capitulo: "CH-05"
tags: [componente, cmp-005]
consumes: ["C-004", "C-008"]
produces: ["C-010", "C-011", "C-014"]
articulos_constitucionales: ["P-05", "P-13", "INV-04", "INV-06", "INV-15", "INV-18", "INV-19", "INV-20"]
---

# PolicyEngine (CMP-005)

> Componente introducido en [[ch-05-policy-engine|CH-05]] — parte del runtime del arnés.

## Responsabilidad

Evaluar si una acción ya resuelta (ToolCall) puede ocurrir, produciendo una PolicyDecision determinística de tres resultados posibles (allow, deny, require_approval) — con la regla aplicable y el ToolCall evaluado siempre trazables — sin ejecutar la acción, sin invocar al modelo, sin seleccionar contexto, sin decidir continuación del turno y sin resolver ella misma la aprobación humana cuando la exige.

## Decisiones que posee (owns)

- allow
- deny
- constraints
- approval requirements
- policy evaluation

## Decisiones que NO posee (does_not_own)

- ejecutar la acción ya evaluada (ToolRuntime, CMP-002, ya introducido en CH-02 — Article IV: "ToolRuntime → How should an approved action be executed?")
- invocar al modelo seleccionado (ModelGateway, CMP-003, ya introducido en CH-03)
- seleccionar/rankear/componer contexto (ContextEngine, CMP-004, ya introducido en CH-04)
- decidir si otro turno de razonamiento debe ocurrir (AgentLoop, CMP-001, ya introducido en CH-01)
- representar, persistir y resolver la aprobación humana cuando outcome = REQUIRE_APPROVAL (HumanInteractionService, Article III — no introducido en este capítulo; INV-15 exige que la acción no se ejecute antes de una resolución válida, pero resolver esa aprobación no es trabajo de PolicyEngine)
- enforcement de ExecutionBudget (ExecutionController, Article III — no introducido en este capítulo)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]], [[C-008-toolcall|C-008]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-014-policydecision|C-014]] |

## Artículos constitucionales

P-05, P-13, INV-04, INV-06, INV-15, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-05-policy-engine|CH-05]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
