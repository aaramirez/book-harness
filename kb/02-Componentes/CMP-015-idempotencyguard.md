---
id: "CMP-015"
tipo: componente
nombre: "IdempotencyGuard"
capitulo: "CH-17"
tags: [componente, cmp-015]
consumes: ["C-004", "C-008", "C-009"]
produces: ["C-010", "C-011", "C-027"]
articulos_constitucionales: ["P-13", "P-24", "INV-11", "INV-E09", "INV-18", "INV-19", "INV-20"]
---

# IdempotencyGuard (CMP-015)

> Componente introducido en [[ch-17-idempotency-guard|CH-17]] — parte del runtime del arnés.

## Responsabilidad

Rastrear, para un ToolCall con side effects (C-008, CH-02) identificado por una clave de idempotencia ya asumida como dada, si esa ejecución ya ocurrió antes bajo esa misma clave — permitiendo, cuando corresponda, reusar el ToolResult (C-009, CH-02) ya producido en vez de duplicar el side effect real — y registrar, una vez que una ejecución nueva concluye, el IdempotencyRecord terminal correspondiente, sin sobrescribir jamás uno ya producido — sin ejecutar el side effect en sí, sin decidir autorización, sin resolver qué implementación satisface la capability y sin decidir si un run puede reintentar contra su presupuesto.

## Decisiones que posee (owns)

- Side effects críticos deben soportar idempotencia, deduplicación o una protección equivalente (cita literal, INV-11, Article II — Execution Invariants)
- Capabilities with externally visible side effects MUST declare idempotency, retry and duplicate-delivery behavior (cita literal, P-24)
- Every side-effecting capability declares idempotency and retry semantics (cita literal, INV-E09 — la mitad de "idempotency"; la mitad de "retry" pertenece a ExecutionController)
- detectar cuándo un ToolCall ya se ejecutó antes bajo la misma clave de idempotencia, produciendo el IdempotencyRecord ya asociado a esa clave (PENDING o COMPLETED), cuando existe
- decidir si una ejecución repetida debe reusar el ToolResult ya conocido, en vez de que el side effect real vuelva a ejecutarse
- registrar, de forma terminal y write-once, el IdempotencyRecord COMPLETED que resulta de una ejecución nueva ya concluida
- rechazar por defecto (fail-closed) cuando la clave de idempotencia encontrada corresponde a una capability distinta de la solicitada, o cuando se intenta re-registrar una ejecución ya COMPLETED

## Decisiones que NO posee (does_not_own)

- ejecutar el side effect en sí (ToolRuntime, CMP-002, ya introducido en CH-02 — IdempotencyGuard decide SI debe ejecutarse de nuevo, nunca CÓMO se ejecuta)
- decidir si la acción/ToolCall ya resuelta está autorizada (PolicyEngine, CMP-005, ya introducido en CH-05 — distinta pregunta, distinto momento: "¿ya se hizo esto?" nunca es "¿está permitido hacerlo?")
- resolver qué implementación satisface una capability solicitada (CapabilityRegistry, CMP-008, ya introducido en CH-08)
- decidir si un AgentRun puede seguir operacionalmente contra su ExecutionBudget, incluyendo si reintentar tras un fallo transitorio (ExecutionController, CMP-007, ya introducido en CH-07 — distinción central de este capítulo: "puedo seguir intentando" y "ya se hizo con éxito" son preguntas ortogonales sobre materiales distintos)
- generar la clave de idempotencia misma, ni decidir con qué algoritmo se deriva (asumida como una señal de entrada dada)
- el mecanismo real de persistencia atómica que evita una condición de carrera entre dos ejecuciones concurrentes que reclaman la misma clave al mismo tiempo (Preview, infraestructura de borde, no un componente propio de este registry)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]], [[C-008-toolcall|C-008]], [[C-009-toolresult|C-009]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-027-idempotencyrecord|C-027]] |

## Artículos constitucionales

P-13, P-24, INV-11, INV-E09, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-17-idempotency-guard|CH-17]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
