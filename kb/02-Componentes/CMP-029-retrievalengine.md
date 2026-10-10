---
id: "CMP-029"
tipo: componente
nombre: "RetrievalEngine"
capitulo: "CH-42"
tags: [componente, cmp-029]
consumes: ["C-004", "C-040", "C-054", "C-055"]
produces: ["C-010", "C-011", "C-056"]
articulos_constitucionales: ["P-14", "P-22", "INV-E07", "INV-E11", "INV-E26", "INV-18", "INV-19", "INV-20"]
---

# RetrievalEngine (CMP-029)

> Componente introducido en [[ch-42-fuentes-de-datos|CH-42]] — parte del runtime del arnés (Data & Context Plane).

## Responsabilidad

Recuperar, de las fuentes de datos declaradas, los candidatos que una consulta puede ver — aplicando la regla de alcance de cada fuente sobre el llamante verificado, la clasificación declarada (o RESTRICTED si falta) y la frescura —, entregándolos con su procedencia para que ContextEngine decida cuáles entran al contexto — sin seleccionar ni componer el contexto, sin clasificar el dato con reglas de gobierno, sin autorizar, sin resolver credenciales y sin escribir en ninguna fuente.

## Decisiones que posee (owns)

- Context should be selected, not dumped (cita literal, P-14) — recuperar solo lo que una consulta acotada devuelve de fuentes declaradas, nunca volcar una fuente entera
- Every data source declares a classification; an undeclared source is RESTRICTED (cita literal, INV-E26)
- Nuevas fuentes de contexto deben identificar origen, freshness y reglas de acceso cuando corresponda (cita literal, EVO-09) — cada candidato lleva su procedencia; un candidato más viejo que la frescura de su fuente se descarta
- aplicar la regla de alcance de la fuente (SHARED, PER_TENANT, PER_PRINCIPAL) sobre execution.caller.current, y rechazar (fail-closed) una fuente con alcance por llamante sin un llamante que la satisfaga
- rechazar (fail-closed) una fuente que no sea de solo lectura, o una de recursos de conexión sin una conexión declarada

## Decisiones que NO posee (does_not_own)

- seleccionar, rankear y componer qué candidatos entran al contexto bajo presupuesto (ContextEngine, CMP-004, ya introducido en CH-04 — la frontera más importante de este capítulo: RetrievalEngine decide QUÉ PUEDE recuperarse; ContextEngine decide QUÉ ENTRA al contexto)
- clasificar el dato con reglas de gobierno y producir su DataGovernanceLabel (DataGovernanceEngine, CMP-018, ya introducido en CH-20)
- autorizar si un dato puede verse en absoluto (PolicyEngine, CMP-005, ya introducido en CH-05)
- resolver la credencial de la fuente (CredentialBroker, CMP-014, ya introducido en CH-16)
- escribir en una fuente (una tool con sus efectos, CapabilityRegistry y ToolRuntime)
- hablar el protocolo de cada fuente — SQL, HTTP, stream, recursos MCP (adaptador)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]], [[C-040-principal|C-040]], [[C-054-connectiondescriptor|C-054]], [[C-055-datasourcedescriptor|C-055]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-056-retrievedcandidate|C-056]] |

## Artículos constitucionales

P-14, P-22, INV-E07, INV-E11, INV-E26, INV-18, INV-19, INV-20 (y EVO-09)

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-42-fuentes-de-datos|CH-42]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
