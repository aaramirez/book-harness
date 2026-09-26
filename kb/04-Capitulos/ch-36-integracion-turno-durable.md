---
id: "CH-36"
tipo: capitulo
titulo: "Integración: el Turno Durable Gobernado"
tags: [capitulo, ch36, tramo-4, integracion]
introduces_components: []
introduces_contracts: []
modifies_contracts: []
articulos_constitucionales: ["P-13", "P-16", "P-17", "P-23", "P-31", "P-32", "P-33", "P-34", "P-35", "INV-05", "INV-07", "INV-13", "INV-15", "INV-E02", "INV-E15", "INV-E16", "INV-E17", "INV-E18", "INV-E19", "INV-E20"]
---

# CH-36 — Integración: el Turno Durable Gobernado

## Navegación

⬅ [[ch-35-entorno-aislado|CH-35]] · **CH-36**

## Resultado esperado

Al terminar este capítulo podrás explicar un turno completo del agente desde que llega un mensaje por un canal hasta que termina, se estaciona esperando una aprobación o se recupera después de una caída. También podrás señalar en cada punto qué componente decide y qué garantía de la versión 0.2 se cumple ahí.

## Qué introduce este capítulo

Ningún componente ni contrato. Cinco funciones de integración que componen CH-03..CH-35:

- `enterDurableTurn` — [[CMP-012-admissioncontroller|AdmissionController]] + [[CMP-025-continuationregistry|ContinuationRegistry]]
- `bindDurableCaller` — `CallerSnapshot` en el `ExecutionContext` (CH-31)
- `runDurableGovernedStep` — [[CMP-023-executionjournal|ExecutionJournal]], ModelGateway, CapabilityRegistry, PolicyEngine, [[CMP-024-resumptioncoordinator|ResumptionCoordinator]], [[CMP-026-isolatedexecutionenvironment|IsolatedExecutionEnvironment]]
- `resumeDurableApproval` — reanuda una aprobación registrando la tool call antes de ejecutarla
- `resolvePendingStepOnRecovery` — [[CMP-015-idempotencyguard|IdempotencyGuard]] (`decideUnknownOutcome`, CH-30)

**Hallazgo:** `beginToolApprovalPause` y `resumeAfterHumanResolution` (CH-13) no se pueden envolver con el journal (no exponen la solicitud ni el `ToolResult`); el turno durable compone sus mismas piezas sin modificarlas.

## Artículos constitucionales relevantes

P-13, P-16, P-17, P-23, P-31, P-32, P-33, P-34, P-35, INV-05, INV-07, INV-13, INV-15, INV-E02, INV-E15, INV-E16, INV-E17, INV-E18, INV-E19, INV-E20

## Localización en el repo

`book/chapters/36-integracion-turno-durable/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
