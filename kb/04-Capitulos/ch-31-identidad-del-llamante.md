---
id: "CH-31"
tipo: capitulo
titulo: "La Identidad del Llamante y el Arranque que No Admite Nada"
tags: [capitulo, ch31, tramo-4]
introduces_components: []
introduces_contracts: ["C-040", "C-041"]
modifies_contracts: ["C-004", "C-023"]
articulos_constitucionales: ["P-13", "P-17", "P-31", "INV-19", "INV-E02", "INV-E07", "INV-E15"]
---

# CH-31 — La Identidad del Llamante y el Arranque que No Admite Nada

## Navegación

⬅ [[ch-30-politica-de-replay|CH-30]] · **CH-31**

## Resultado esperado

Al terminar este capítulo podrás decidir de dónde sale la identidad de quien llama al agente y cómo viaja con cada turno, y distinguir a quien inició una sesión de quien envía la entrega actual. También podrás justificar por qué un arnés recién instalado no debe admitir a nadie hasta que alguien configure quién puede entrar.

## Qué introduce este capítulo

### Componentes

- Ninguno. Amplía [[CMP-012-admissioncontroller|AdmissionController]] dentro de su `owns` ("apply identity, authorization, tenant…", P-17).

### Contratos

- [[C-040-principal|C-040 Principal]]
- [[C-041-callersnapshot|C-041 CallerSnapshot]]
- **Modifica** [[C-004-executioncontext|C-004 ExecutionContext]] → v2 y [[C-023-admissiondecision|C-023 AdmissionDecision]] → v2 (ADR-001).

## Artículos constitucionales relevantes

P-13, P-17, P-31, INV-19, INV-E02, INV-E07, INV-E15

## Localización en el repo

`book/chapters/31-identidad-del-llamante/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
