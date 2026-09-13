---
name: write-technical-chapter
description: >-
  Fuerza la estructura obligatoria de 19 secciones para un capítulo del libro "¿Cómo construir
  un arnés?" (REGLAS_LIBRO_AGENT_HARNESS(1).md §26-27). Usar siempre que se escriba o revise un
  chapter.md completo, antes de rellenar cualquier sección individual.
---

# Skill: write-technical-chapter

## Cuándo usar esta skill

Al empezar a escribir un `chapter.md` nuevo, o al auditar uno existente antes de correr
`scripts/validate-chapter`. Esta skill no escribe el contenido técnico por ti (eso lo dictan las
otras 4 skills y el Chapter Brief) — impone el **orden y la presencia** de cada sección.

## Procedimiento

### Paso 1 — Frontmatter

Todo `chapter.md` empieza con un bloque YAML delimitado por `---`:

```yaml
---
id: CH-XX
title: "Título en español"
starting_version: "0.X"
ending_version: "0.X"
introduces_components: [CMP-XXX, ...]   # [] si no introduce ninguno
introduces_contracts: [C-XXX, ...]      # [] si no introduce ninguno
modifies_contracts: [C-XXX, ...]        # [] si no modifica ninguno
constitutional_articles: [P-XX, INV-XX, ...]
previous_chapter: CH-XX | null
next_chapter: CH-XX | null
---
```

### Paso 2 — Las 19 secciones, EN ESTE ORDEN Y SIN SALTARSE NINGUNA

Cada una es un encabezado `## N. <Nombre en español (Nombre en inglés)>` seguido de contenido
real (no un placeholder). El nombre en inglés entre paréntesis existe para que
`scripts/validate-chapter` pueda ubicar la sección de forma determinística aunque el título en
español varíe ligeramente.

```text
1.  Current Architecture                          → "Arquitectura Actual"
2.  Problem                                        → "El Problema"
3.  Why the Current Architecture Is Insufficient   → "Por Qué la Arquitectura Actual No Basta"
4.  Constitutional Impact                          → "Impacto Constitucional"
5.  New Concepts                                    → "Conceptos Nuevos"
6.  New Data Structures                             → "Nuevas Estructuras de Datos"
7.  New Contracts / Interfaces                      → "Nuevos Contratos / Interfaces"
8.  Component Responsibilities                      → "Responsabilidades de Componentes"
9.  Dependency Relationships                        → "Relaciones de Dependencia"
10. Sequence Diagram                                → "Diagrama de Secuencia"
11. Pseudocode                                       → "Pseudocódigo"
12. State Transitions                                → "Transiciones de Estado"
13. Failure Semantics                                → "Semántica de Fallos"
14. Events Produced                                  → "Eventos Producidos"
15. Security / Policy Implications                   → "Implicaciones de Seguridad / Política"
16. Tests                                            → "Tests"
17. Architecture After This Chapter                  → "Arquitectura Después de Este Capítulo"
18. What We Deliberately Do Not Solve Yet             → "Lo Que Deliberadamente No Resolvemos Todavía"
19. Next Increment                                    → "Siguiente Incremento"
```

No invertir el orden salvo razón pedagógica explícita y documentada (REGLAS_LIBRO §27).

### Paso 3 — Reglas de contenido por sección

- **§1 Current Architecture**: si es el primer capítulo del libro, decir explícitamente "No existe
  arquitectura previa" — no omitir la sección.
- **§4 Constitutional Impact**: usar exactamente los campos de
  `skills/analyze-constitutional-impact/SKILL.md`.
- **§5 New Concepts**: solo prosa conceptual, sin pseudocódigo todavía.
- **§6 New Data Structures**: bloques ` ```pseudocode ` con `STRUCT`/`ENUM` — ver
  `skills/write-pseudocode/SKILL.md`.
- **§7 New Contracts / Interfaces**: una ficha de Contract Registry por contrato nuevo — ver
  `skills/define-contract/SKILL.md`.
- **§8 Component Responsibilities**: una ficha arquitectónica por componente nuevo — ver
  `skills/define-component/SKILL.md`. Si el capítulo no introduce componentes, decirlo
  explícitamente y, si se mencionan componentes futuros, marcarlos como
  "Preview — no introducido en este capítulo" (nunca en un bloque ` ```pseudocode `).
- **§10 Sequence Diagram**: las tres vistas obligatorias (Componentes / Sequence / Pseudocódigo)
  de REGLAS_LIBRO §14, coherentes entre sí.
- **§11 Pseudocode**: solo entidades ya definidas en §6/§7 de este capítulo o ya registradas en
  `registry/`. Ver regla "no magic entities".
- **§13 Failure Semantics**: clasificar cada fallo nuevo contra `ENUM ErrorCategory` (Article VII
  de la Constitution).
- **§16 Tests**: al menos un test arquitectónico (`TEST NombreDescriptivo`) por invariante nueva o
  preservada relevante (REGLAS_LIBRO §28).
- **§17 Architecture After This Chapter**: debe reflejar exactamente lo declarado en
  `introduces_components` / `introduces_contracts` del frontmatter — ni más, ni menos.
- **§19 Next Increment**: debe conectar con el `next_chapter` del frontmatter (o decir
  explícitamente que aún no hay capítulo siguiente planificado).

### Paso 4 — Checklist final (REGLAS_LIBRO §31) antes de entregar el borrador

```text
[ ] Every pseudocode entity is defined.
[ ] Every component has a responsibility boundary.
[ ] Every dependency points to a known contract.
[ ] Every new contract exists in the Contract Registry.
[ ] Every new component exists in the Component Registry.
[ ] Sequence diagrams match pseudocode.
[ ] State transitions are explicit.
[ ] Errors are classified.
[ ] Events are defined.
[ ] Constitutional impact is documented.
[ ] Current and resulting architecture are shown.
[ ] Remaining limitations are explicit.
[ ] The next chapter follows naturally.
```

### Paso 5 — Validar

```bash
./scripts/validate-chapter book/chapters/<carpeta-del-capitulo>
./scripts/validate-contracts
./scripts/validate-components
```

No considerar el capítulo terminado hasta que los tres comandos terminen con código de salida 0.
