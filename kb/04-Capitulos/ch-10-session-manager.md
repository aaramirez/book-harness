---
id: "CH-10"
tipo: capitulo
titulo: "\"SessionManager y la Persistencia Durable de una Sesión\""
tags: [capitulo, ch10]
introduces_components: ["CMP-010"]
introduces_contracts: ["C-020"]
articulos_constitucionales: ["P-04", "P-08", "P-23", "INV-12", "INV-13", "INV-18", "INV-19", "INV-20"]
---

# CH-10 — "SessionManager y la Persistencia Durable de una Sesión"

## Navegación

⬅ [[ch-09-event-bus|CH-09]] · **CH-10** · [[ch-11-agent-core|CH-11]] ➡

## Resultado esperado

—

## Qué introduce este capítulo

### Componentes

- [[CMP-010-sessionmanager|CMP-010]] — Persistir y actualizar la historia de una sesión mediante checkpoints construidos a partir de un AgentState ya producido por una ejecución existente, reconstruir un SessionState completo desde un checkpoint ya persistido, y crear una rama nueva de sesión a partir de un checkpoint existente — sin poseer el estado operativo de la ejecución en curso, sin persistir las solicitudes de interacción humana que HumanInteractionService ya persiste por su cuenta, sin decidir continuación de turno y sin distribuir eventos.

### Contratos

- [[C-020-sessionstate|C-020]] — SessionState (impacto: P-08, P-23, INV-12, INV-13)


## Artículos constitucionales relevantes

P-04, P-08, P-23, INV-12, INV-13, INV-18, INV-19, INV-20

## Localización en el repo

`book/chapters/10-session-manager/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
