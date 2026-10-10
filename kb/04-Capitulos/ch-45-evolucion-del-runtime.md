---
id: "CH-45"
tipo: capitulo
titulo: "Evolución del Runtime con Sesiones Abiertas"
tags: [capitulo, ch45, v0-3]
introduces_components: []
introduces_contracts: ["C-060"]
modifies_contracts: ["C-020"]
articulos_constitucionales: ["P-08", "P-23", "P-36", "INV-12", "INV-13", "INV-E10", "INV-E22"]
---

# CH-45 — Evolución del Runtime con Sesiones Abiertas

## Navegación

⬅ [[ch-44-invocacion-entre-agentes|CH-44]] · **CH-45**

## Resultado esperado

Al terminar este capítulo podrás decidir cuándo una sesión abierta puede pasar a una versión nueva del agente, la política, el modelo, las conexiones o el formato de sesión, y explicar qué trabajo vivo lo impide y qué se registra cuando cambia.

## Qué introduce este capítulo

### Componentes

- Ninguno nuevo. [[CMP-010-sessionmanager|SessionManager]] gana `liveWorkOf`, `sessionMayMigrate`, `migrateSessionRuntime`, `recordModelSwitch` y `reconstructWithRuntimeVersion`, entre otras; [[CMP-028-connectionmanager|ConnectionManager]] gana `connectionVersionFor` y `connectionVersionInUse`.

### Contratos

- [[C-060-runtimeversionsnapshot|C-060 RuntimeVersionSnapshot]]
- [[C-020-sessionstate|C-020 SessionState]] v2 → v3 (ADR-003 parte v3)

### Deuda

Resuelve D-017, D-022, D-046 y D-048.

## Artículos constitucionales relevantes

P-08, P-23, P-36, INV-12, INV-13, INV-E10, INV-E22

## Localización en el repo

`book/chapters/45-evolucion-del-runtime/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
