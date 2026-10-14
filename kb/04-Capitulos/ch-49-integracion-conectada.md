---
id: "CH-49"
tipo: capitulo
titulo: "Integración: el Arnés Conectado"
tags: [capitulo, ch49, v0-3]
introduces_components: []
introduces_contracts: []
modifies_contracts: []
articulos_constitucionales: ["P-13", "P-14", "P-21", "P-31", "P-33", "P-35", "P-37", "P-38", "P-39", "INV-E06", "INV-E16", "INV-E21", "INV-E23", "INV-E24", "INV-E25", "INV-E26", "INV-E27"]
---

# CH-49 — Integración: el Arnés Conectado

## Navegación

⬅ [[ch-48-agente-como-directorio|CH-48]] · **CH-49**

## Resultado esperado

Al terminar este capítulo podrás decidir en qué orden se aplican los controles de la versión 0.3 en un turno conectado, y explicar cómo un paso retoma una respuesta con varias herramientas sin volver a llamar al modelo, cómo se avisa a un aprobador ausente y dónde corre una extensión de proyecto.

## Qué introduce este capítulo

### Componentes

- Ninguno. Funciones de integración: `enterConnectedTurn`, `openConnectedGovernedTurn`, `runConnectedGovernedStep`, `nextProposalFromJournal`, `approverNoticeFor`, `requireExtensionPlacement`, `disableExtension`, `credentialForConnectedCall`, `traceConnectedStep`.

### Contratos

- Ninguno.

### Deuda

Resuelve D-041, D-042, D-044 y D-045. `registry/debt.yaml` queda sin deudas abiertas.

## Artículos constitucionales relevantes

P-13, P-14, P-21, P-31, P-33, P-35, P-37, P-38, P-39, INV-E06, INV-E16, INV-E21, INV-E23, INV-E24, INV-E25, INV-E26, INV-E27

## Revisión (2026-10-12)

`connectedModelMessages` lleva los bloques gobernados (`ConnectedTurnStart.contextBlocks`) a la llamada al modelo, antes de las entradas pendientes. Ver `planes/2026-10-12-revision-ch37-ch49-huecos.md`.

## Localización en el repo

`book/chapters/49-integracion-conectada/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
