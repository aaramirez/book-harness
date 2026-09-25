---
id: "CH-28"
tipo: capitulo
titulo: "Entradas que Llegan Durante el Turno: Steering y Follow-up"
tags: [capitulo, ch28, tramo-4]
introduces_components: []
introduces_contracts: ["C-036"]
articulos_constitucionales: ["P-10", "P-12", "P-13", "INV-07", "INV-08", "INV-10", "INV-15", "INV-18", "INV-19"]
---

# CH-28 — Entradas que Llegan Durante el Turno: Steering y Follow-up

## Navegación

⬅ [[ch-27-enterprise-control|CH-27]] · **CH-28** · [[ch-29-compactacion-sesiones-arbol|CH-29]] ➡

## Resultado esperado

Al terminar este capítulo podrás decidir, para cualquier mensaje que un usuario envía mientras el turno de un agente todavía corre, en qué frontera exacta del turno debe aplicarse:
- antes de la próxima llamada al modelo;
- o solo cuando el agente iba a terminar.

También podrás distinguir ese mensaje de una resolución humana, de una cancelación y de una autorización.

## Qué introduce este capítulo

### Componentes

- Ninguno. Amplía [[CMP-001-agentloop|AgentLoop]] dentro de su `owns` ya existente (continuación del turno).

### Contratos

- [[C-036-pendinginput|C-036 PendingInput]]

## Artículos constitucionales relevantes

P-10, P-12, P-13, INV-07, INV-08, INV-10, INV-15, INV-18, INV-19

## Localización en el repo

`book/chapters/28-steering-follow-up/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
