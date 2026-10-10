---
id: "CMP-028"
tipo: componente
nombre: "ConnectionManager"
capitulo: "CH-41"
tags: [componente, cmp-028]
consumes: ["C-004", "C-008", "C-018"]
produces: ["C-010", "C-011", "C-018", "C-054"]
articulos_constitucionales: ["P-03", "P-38", "INV-04", "INV-05", "INV-E25", "INV-18", "INV-19", "INV-20"]
---

# ConnectionManager (CMP-028)

> Componente introducido en [[ch-41-conexiones|CH-41]] — parte del runtime del arnés (Capability & Integration Plane).

## Responsabilidad

Gestionar las conexiones declaradas a proveedores externos de capabilities — servidores MCP por stdio o HTTP, y especificaciones OpenAPI — y traducir sus tools u operaciones en CapabilityDescriptor con espacio de nombres propio, filtro de tools y argumentos provistos que el modelo nunca ve, preparando cada invocación hacia el adaptador del protocolo — sin resolver tokens, sin autorizar, sin ejecutar la tool, sin resolver capabilities y sin depender del SDK de ningún protocolo.

## Decisiones que posee (owns)

- Capabilities provided by external systems (for example MCP servers or OpenAPI services) MUST enter through declared connections and be resolved as capability descriptors (cita literal, P-38) — traducir cada tool permitida de una conexión declarada en un CapabilityDescriptor <conexión>__<tool>
- aplicar el filtro de tools de la conexión (lista permitida o bloqueada) y rechazar (fail-closed) una tool fuera del filtro o un nombre que colisiona con una capability local
- ocultar al modelo los argumentos provistos de la conexión: quitarlos del schema que ve el modelo, agregarlos al preparar la invocación, y rechazar una tool call en la que el modelo intenta fijarlos

## Decisiones que NO posee (does_not_own)

- resolver qué implementación satisface una capability ni validar sus argumentos (CapabilityRegistry, CMP-008, ya introducido en CH-08 — la frontera más importante de este capítulo: ConnectionManager produce descriptores; CapabilityRegistry los resuelve como a cualquier otro, INV-E25)
- autorizar la tool call (PolicyEngine, CMP-005, ya introducido en CH-05)
- ejecutar la tool call (ToolRuntime, CMP-002, ya introducido en CH-02 — INV-05)
- resolver la credencial de la conexión (CredentialBroker, CMP-014, ya introducido en CH-16 — INV-E08)
- hablar el protocolo MCP u OpenAPI (adaptador de protocolo, P-38 — el núcleo no depende de un SDK)
- exponer el propio arnés como servidor MCP (Ingress Adapter de canal, CH-34 — un canal, no una conexión)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]], [[C-008-toolcall|C-008]], [[C-018-capabilitydescriptor|C-018]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-018-capabilitydescriptor|C-018]], [[C-054-connectiondescriptor|C-054]] |

## Artículos constitucionales

P-03, P-38, INV-04, INV-05, INV-E25, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-41-conexiones|CH-41]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
