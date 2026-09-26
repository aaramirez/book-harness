---
id: "CH-33"
tipo: capitulo
titulo: "Esperas Durables y la Reanudación desde Cualquier Canal"
tags: [capitulo, ch33, tramo-4]
introduces_components: ["CMP-024"]
introduces_contracts: ["C-044", "C-045"]
modifies_contracts: ["C-015"]
articulos_constitucionales: ["P-11", "P-23", "P-31", "P-33", "INV-14", "INV-15", "INV-E08", "INV-E18"]
---

# CH-33 — Esperas Durables y la Reanudación desde Cualquier Canal

## Navegación

⬅ [[ch-32-pasos-durables|CH-32]] · **CH-33** · [[ch-34-canales-continuacion|CH-34]] ➡

## Resultado esperado

Al terminar este capítulo podrás estacionar un run que espera (una aprobación, una respuesta, una autorización o una decisión sobre su presupuesto) sin que ningún proceso quede ocupado. También podrás decidir, cuando llega una respuesta por cualquier canal, si reanuda esa espera y si quien responde tiene derecho a hacerlo.

## Qué introduce este capítulo

### Componentes

- [[CMP-024-resumptioncoordinator|CMP-024 ResumptionCoordinator]]. [[CMP-006-humaninteractionservice|HumanInteractionService]] gana `linkRequestToWait` dentro de su `owns`.

### Contratos

- [[C-044-parkedwait|C-044 ParkedWait]]
- [[C-045-authorizationchallenge|C-045 AuthorizationChallenge]]
- **Modifica** [[C-015-humaninteractionrequest|C-015 HumanInteractionRequest]] → v2 (`waitId`).
- Primer uso real de `PAUSED` ([[C-013-agentrunstatus|C-013]]) y de `resumeAfterHumanResolution` (CH-13).

## Artículos constitucionales relevantes

P-11, P-23, P-31, P-33, INV-14, INV-15, INV-E08, INV-E18

## Localización en el repo

`book/chapters/33-esperas-durables/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
