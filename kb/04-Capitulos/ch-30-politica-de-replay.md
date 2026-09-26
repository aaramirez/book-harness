---
id: "CH-30"
tipo: capitulo
titulo: "Cuando No se Sabe si Ocurrió: Política de Replay"
tags: [capitulo, ch30, tramo-4]
introduces_components: []
introduces_contracts: ["C-039"]
modifies_contracts: ["C-018", "C-009"]
articulos_constitucionales: ["P-24", "INV-07", "INV-11", "INV-20", "INV-E09", "INV-E17"]
---

# CH-30 — Cuando No se Sabe si Ocurrió: Política de Replay

## Navegación

⬅ [[ch-29-compactacion-sesiones-arbol|CH-29]] · **CH-30** · [[ch-31-identidad-del-llamante|CH-31]] ➡

## Resultado esperado

Al terminar este capítulo podrás decidir, para cualquier efecto externo que empezó pero cuyo resultado nunca se registró, si el arnés debe esperar, volver a ejecutarlo o reportar al modelo que el resultado es desconocido. También podrás justificar por qué esa decisión la declara cada capability y no la toma el modelo.

## Qué introduce este capítulo

### Componentes

- Ninguno. Amplía [[CMP-015-idempotencyguard|IdempotencyGuard]] dentro de su `owns`; [[CMP-008-capabilityregistry|CapabilityRegistry]] registra la política.

### Contratos

- [[C-039-replaypolicy|C-039 ReplayPolicy]]
- **Modifica** [[C-018-capabilitydescriptor|C-018 CapabilityDescriptor]] → v2 y [[C-009-toolresult|C-009 ToolResult]] → v2 (ADR-002).

## Artículos constitucionales relevantes

P-24, INV-07, INV-11, INV-20, INV-E09, INV-E17

## Localización en el repo

`book/chapters/30-politica-de-replay/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
