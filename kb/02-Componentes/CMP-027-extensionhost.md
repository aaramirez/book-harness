---
id: "CMP-027"
tipo: componente
nombre: "ExtensionHost"
capitulo: "CH-40"
tags: [componente, cmp-027]
consumes: ["C-004", "C-040"]
produces: ["C-010", "C-011", "C-051", "C-052", "C-053"]
articulos_constitucionales: ["P-12", "P-13", "INV-05", "INV-06", "INV-E24", "INV-18", "INV-19", "INV-20"]
---

# ExtensionHost (CMP-027)

> Componente introducido en [[ch-40-extension-host|CH-40]] — parte del runtime del arnés (Capability & Integration Plane).

## Responsabilidad

Registrar las extensiones del arnés — con su origen, su hash y la decisión de confianza que las cubre —, mantener el catálogo cerrado de puntos de hook con los resultados que cada punto admite, y validar el resultado de cada hook antes de que el componente dueño de ese punto lo aplique — sin ejecutar los hooks en cada punto, sin autorizar ninguna acción, sin registrar ni resolver capabilities, sin ejecutar tools y sin descargar ni instalar código.

## Decisiones que posee (owns)

- Una extensión no puede saltarse ToolRuntime, PolicyEngine, lifecycle o controles de ejecución para realizar acciones que el core prohibiría (cita literal, EVO-10) — hacerlo verificable: registrar cada extensión y validar cada resultado de hook
- No hook point may return an authorization outcome (cita literal, INV-E24) — el catálogo de resultados de un hook (CONTINUE, BLOCK, TRANSFORM) no contiene ninguna autorización
- Los hooks permiten intervenir en puntos controlados del lifecycle (cita literal, P-12) — el catálogo cerrado de HookPoints y qué resultados admite cada uno
- rechazar por defecto (fail-closed) una extensión de proyecto u organización sin una ResourceTrustDecision TRUSTED que cubra su sourceRef y su contentHash actuales

## Decisiones que NO posee (does_not_own)

- ejecutar los hooks en cada punto del ciclo (el componente dueño del punto: ToolRuntime, CMP-002, ya introducido en CH-02, que posee "ejecutar hooks" para BEFORE_TOOL / AFTER_TOOL; ModelGateway, ContextEngine, AgentLoop y SessionManager para los suyos — la frontera más importante de este capítulo: ExtensionHost decide QUÉ hooks pueden correr y QUÉ pueden devolver; el dueño del punto los invoca y aplica el resultado ya validado)
- autorizar una acción (PolicyEngine, CMP-005, ya introducido en CH-05 — P-13, INV-06)
- registrar o resolver las capabilities que una extensión aporta (CapabilityRegistry, CMP-008, ya introducido en CH-08 — una capability de extensión entra por el mismo registro y la misma política que cualquier otra)
- ejecutar tools (ToolRuntime, CMP-002 — INV-05)
- observar y distribuir eventos (EventBus, CMP-009, ya introducido en CH-09 — P-12: los observers observan, los hooks intervienen)
- descargar, instalar o aislar el código de una extensión (infraestructura de borde y entorno aislado, CH-35)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]], [[C-040-principal|C-040]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-051-extensionregistration|C-051]], [[C-052-hookpoint|C-052]], [[C-053-resourcetrustdecision|C-053]] |

## Artículos constitucionales

P-12, P-13, INV-05, INV-06, INV-E24, INV-18, INV-19, INV-20 (y EVO-10)

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-40-extension-host|CH-40]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
