---
id: "CH-29"
tipo: capitulo
titulo: "Compactar sin Perder el Hilo: Resúmenes Estructurados y Sesiones en Árbol"
tags: [capitulo, ch29, tramo-4]
introduces_components: []
introduces_contracts: ["C-037", "C-038"]
modifies_contracts: ["C-020"]
articulos_constitucionales: ["P-01", "P-02", "P-08", "P-14", "INV-07", "INV-12", "INV-13", "INV-18", "INV-19"]
---

# CH-29 — Compactar sin Perder el Hilo: Resúmenes Estructurados y Sesiones en Árbol

## Navegación

⬅ [[ch-28-steering-follow-up|CH-28]] · **CH-29** · [[ch-30-politica-de-replay|CH-30]] ➡

## Resultado esperado

Al terminar este capítulo podrás:
- decidir cuándo un historial necesita compactarse;
- decidir dónde cortarlo sin separar nunca una tool call de su resultado;
- distinguir qué le toca al modelo (proponer el resumen) y qué al arnés (validar su forma y el corte);
- distinguir navegar hacia atrás dentro de una sesión (no borra nada) de ramificar en una sesión nueva.

## Qué introduce este capítulo

### Componentes

- Ninguno. Amplía [[CMP-004-contextengine|ContextEngine]] (compaction) y [[CMP-010-sessionmanager|SessionManager]] (branching) dentro de su `owns`.

### Contratos

- [[C-037-compactionsummary|C-037 CompactionSummary]]
- [[C-038-branchsummary|C-038 BranchSummary]]
- **Modifica** [[C-020-sessionstate|C-020 SessionState]] → v2 (ADR-003, parte v2): primera modificación real de un contrato en el libro.

## Artículos constitucionales relevantes

P-01, P-02, P-08, P-14, INV-07, INV-12, INV-13, INV-18, INV-19

## Localización en el repo

`book/chapters/29-compactacion-sesiones-arbol/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
