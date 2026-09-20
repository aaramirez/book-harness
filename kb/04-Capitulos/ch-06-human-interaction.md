---
id: "CH-06"
tipo: capitulo
titulo: "HumanInteractionService y la Reanudación de una Ejecución Pausada"
tags: [capitulo, ch06]
introduces_components: ["CMP-006"]
introduces_contracts: ["C-015", "C-016"]
articulos_constitucionales: ["P-11", "INV-14", "INV-15", "INV-18", "INV-19", "INV-20"]
---

# CH-06 — HumanInteractionService y la Reanudación de una Ejecución Pausada

## Navegación

⬅ [[ch-05-policy-engine|CH-05]] · **CH-06** · [[ch-07-execution-controller|CH-07]] ➡

## Resultado esperado

Al terminar este capítulo podrás distinguir, dentro del tercer resultado posible de una evaluación de autorización ("todavía no, necesita aprobación humana"), qué tramo le pertenece en exclusiva al componente que representa y resuelve esa espera y qué tramos siguen perteneciendo a otros dominios (decidir si se requiere aprobación, transportar esa solicitud a través de un canal concreto, ejecutar la acción una vez resuelta, decidir si el turno continúa) — y podrás diseñar, para cualquier resolución humana, un resultado que no colapse en un simple aprobado/rechazado cuando en realidad se trata de un valor provisto, preservando siempre quién la resolvió para que sea auditable después.

## Qué introduce este capítulo

### Componentes

- [[CMP-006-humaninteractionservice|CMP-006]] — Representar una solicitud de intervención humana a partir de una PolicyDecision con outcome = REQUIRE_APPROVAL, persistirla mientras está pendiente, recibir su resolución y dejar disponible la información que permitiría reanudar la ejecución — sin decidir si esa aprobación se requiere, sin transportar la interacción por ningún canal concreto, sin ejecutar la acción una vez resuelta y sin decidir si el turno debe continuar.

### Contratos

- [[C-015-humaninteractionrequest|C-015]] — HumanInteractionRequest (impacto: INV-14, INV-15, INV-18, INV-19)
- [[C-016-humaninteractionresolution|C-016]] — HumanInteractionResolution (impacto: INV-14, INV-15, INV-18, INV-19)


## Artículos constitucionales relevantes

P-11, INV-14, INV-15, INV-18, INV-19, INV-20

## Localización en el repo

`book/chapters/06-human-interaction-service/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
