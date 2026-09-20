---
id: "CH-18"
tipo: capitulo
titulo: "\"OperationalController y los Kill Switches Independientes de AgentLoop\""
tags: [capitulo, ch18]
introduces_components: ["CMP-016"]
introduces_contracts: ["C-028"]
articulos_constitucionales: ["P-13", "P-30", "INV-08", "INV-18", "INV-19", "INV-20", "INV-E14"]
---

# CH-18 — "OperationalController y los Kill Switches Independientes de AgentLoop"

## Navegación

⬅ [[ch-17-idempotency-guard|CH-17]] · **CH-18** · [[ch-19-audit-ledger|CH-19]] ➡

## Resultado esperado

—

## Qué introduce este capítulo

### Componentes

- [[CMP-016-operationalcontroller|CMP-016]] — Emitir y aplicar un comando operacional (ControlDirective) que deshabilita una capability, aísla los runs de un tenant, revierte un rollout o fuerza, mediante un kill switch, la terminación inmediata de un AgentRun — actuando siempre desde AFUERA del ciclo de cualquier run particular y sin depender de la cooperación del modelo ni de AgentLoop — sin decidir si UN run específico puede seguir contra su propio presupuesto operacional, sin autorizar ninguna acción ya resuelta, sin resolver qué implementación satisface una capability y sin ejecutar el side effect en sí.

### Contratos

- [[C-028-controldirective|C-028]] — ControlDirective (impacto: P-30, INV-E14, INV-19)


## Artículos constitucionales relevantes

P-13, P-30, INV-08, INV-18, INV-19, INV-20, INV-E14

## Localización en el repo

`book/chapters/18-operational-controller/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
