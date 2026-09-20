---
id: "CMP-006"
tipo: componente
nombre: "HumanInteractionService"
capitulo: "CH-06"
tags: [componente, cmp-006]
consumes: ["C-004", "C-014"]
produces: ["C-010", "C-011", "C-015", "C-016"]
articulos_constitucionales: ["P-11", "INV-14", "INV-15", "INV-18", "INV-19", "INV-20"]
---

# HumanInteractionService (CMP-006)

> Componente introducido en [[ch-06-human-interaction|CH-06]] — parte del runtime del arnés.

## Responsabilidad

Representar una solicitud de intervención humana a partir de una PolicyDecision con outcome = REQUIRE_APPROVAL, persistirla mientras está pendiente, recibir su resolución y dejar disponible la información que permitiría reanudar la ejecución — sin decidir si esa aprobación se requiere, sin transportar la interacción por ningún canal concreto, sin ejecutar la acción una vez resuelta y sin decidir si el turno debe continuar.

## Decisiones que posee (owns)

- representar solicitudes humanas
- persistir interacciones pendientes
- recibir resoluciones
- permitir reanudación

## Decisiones que NO posee (does_not_own)

- decidir SI una acción requiere aprobación humana (PolicyEngine, CMP-005, ya introducido en CH-05 — esa decisión ya se tomó cuando PolicyDecision.outcome = REQUIRE_APPROVAL; este componente solo recibe esa señal)
- transportar la interacción a través de un canal concreto — TUI/Web/Slack/Teams/Mobile/Email/API (Channel Adapter, Article VIII/P-11 — concepto de infraestructura de borde, no un componente propio de Article III / del registry)
- ejecutar la acción una vez resuelta (ToolRuntime, CMP-002, ya introducido en CH-02 — Article IV: "ToolRuntime → How should an approved action be executed?")
- decidir si otro turno de razonamiento debe ocurrir o si la ejecución debe reanudarse operacionalmente (AgentLoop, CMP-001, ya introducido en CH-01)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]], [[C-014-policydecision|C-014]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-015-humaninteractionrequest|C-015]], [[C-016-humaninteractionresolution|C-016]] |

## Artículos constitucionales

P-11, INV-14, INV-15, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-06-human-interaction|CH-06]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
