---
id: "CMP-026"
tipo: componente
nombre: "IsolatedExecutionEnvironment"
capitulo: "CH-35"
tags: [componente, cmp-026]
consumes: ["C-004", "C-008"]
produces: ["C-010", "C-011", "C-047", "C-048"]
articulos_constitucionales: ["P-27", "P-35", "INV-05", "INV-E08", "INV-E20", "INV-18", "INV-19", "INV-20"]
---

# IsolatedExecutionEnvironment (CMP-026)

> Componente introducido en [[ch-35-entorno-aislado|CH-35]] — parte del runtime del arnés (plano Execution Fabric).

## Responsabilidad

Abrir, reusar y cerrar, por sesión, el entorno aislado donde corre el código que el modelo pide — con un ciclo de vida separado del runtime que guarda los secretos —, garantizar que ninguna credencial se materialice dentro de él y decidir, para cada salida de red del entorno, si la NetworkPolicy la permite, la deniega o la deja salir con una credencial que el borde inyecta — sin decidir dónde corre físicamente el cómputo, sin resolver la credencial, sin autorizar la tool y sin ejecutar el side effect en sí.

## Decisiones que posee (owns)

- sandboxing (cita literal, Article XII — Deterministic Decisions) — abrir, reusar y cerrar el entorno aislado de una sesión
- Credentials MUST remain outside both model context and the isolated environment where model-requested code executes (cita literal, P-35) — rechazar (fail-closed) cualquier configuración del entorno que nombre una credencial
- Credentials are never materialized inside the isolated execution environment (cita literal, INV-E20)
- aplicar la NetworkPolicy a cada salida de red del entorno: DENY, ALLOW o ALLOW_WITH_CREDENTIAL — denegar por defecto lo que una ALLOW_LIST no nombra
- decidir si una capability debe ejecutarse dentro del entorno aislado, según la lista de capabilities aisladas configurada

## Decisiones que NO posee (does_not_own)

- decidir sobre qué substrato físico corre el cómputo ([[CMP-019-executionfabricadapter|ExecutionFabricAdapter]], CH-21 — la frontera más importante: ExecutionFabricAdapter decide DÓNDE corre un run; IsolatedExecutionEnvironment decide QUÉ PUEDE HACER y QUÉ PUEDE ALCANZAR el código que el modelo pide)
- resolver la credencial que el borde inyecta ([[CMP-014-credentialbroker|CredentialBroker]], CH-16)
- autorizar la tool call ([[CMP-005-policyengine|PolicyEngine]], CH-05)
- ejecutar la tool call ([[CMP-002-toolruntime|ToolRuntime]], CH-02 — INV-05)
- decidir límites de recursos o presupuesto ([[CMP-007-executioncontroller|ExecutionController]], CH-07)
- el mecanismo real de aislamiento ni el proxy de red que inyecta encabezados (infraestructura de borde)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]], [[C-008-toolcall|C-008]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-047-sandboxsession|C-047]], [[C-048-networkpolicy|C-048]] |

## Artículos constitucionales

P-27, P-35, INV-05, INV-E08, INV-E20, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-35-entorno-aislado|CH-35]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
