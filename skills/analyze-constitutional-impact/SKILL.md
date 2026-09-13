---
name: analyze-constitutional-impact
description: >-
  Genera el bloque "Constitutional Impact" de un capítulo (principios afectados, invariantes
  introducidos/preservados, ownership, lifecycle, seguridad, observabilidad, frontera
  determinístico/agéntico) contra constitution/ARCHITECTURE_CONSTITUTION.md. Usar al escribir la
  sección 4 de todo capítulo, y de nuevo al escribir la sección 17 ("Architecture After This
  Chapter") para confirmar que lo declarado sigue siendo cierto.
---

# Skill: analyze-constitutional-impact

## Cuándo usar esta skill

Siempre, para la sección obligatoria "4. Constitutional Impact" de cualquier capítulo
(REGLAS_LIBRO_AGENT_HARNESS(1).md §22, y la lista de 19 secciones §26). También cada vez que se
proponga un componente, contrato, evento o cambio de estado nuevo — antes de aceptarlo, para
decidir si requiere aprobación humana (BOOK_HARNESS_BUILD_INSTRUCTIONS(1).md §15).

## Procedimiento

### Paso 1 — Responder las 10 preguntas de "Constitutional Compliance"

Tomadas literalmente de `constitution/ARCHITECTURE_CONSTITUTION.md` ("Constitutional
Compliance"):

```text
1. Which principles does this affect?
2. Which invariants must remain true?
3. Which component owns the decision?
4. Which contracts change?
5. How does the lifecycle change?
6. What are the failure semantics?
7. What are the security implications?
8. What events are produced?
9. What budgets apply?
10. Does this change the deterministic/agentic boundary?
```

### Paso 2 — Producir el bloque en el formato exigido (REGLAS_LIBRO §22)

```text
Constitutional Impact

Principles affected
    P-xx, P-xx

Invariants introduced
    INV-xx

Invariants preserved
    INV-xx

Component ownership changes
    <texto o "None">

Lifecycle changes
    <texto o "None">

Security implications
    <texto o "None">

Observability implications
    <texto o "None">

Deterministic vs agentic boundary
    <texto — qué queda del lado del modelo (Article XII "Agentic Decisions") y qué queda del
    lado del runtime (Article XII "Deterministic Decisions")>
```

Los 8 campos son obligatorios; usar `"None"` explícito en vez de omitir el campo cuando no
aplique.

### Paso 3 — Caso especial: el capítulo que introduce la propia Constitution

Si el capítulo ES la introducción de la Constitution (como el capítulo piloto CH-00), los campos
"Principles affected" / "Invariants preserved" no aplican todavía (no hay una constitución previa
que preservar) — usar en su lugar:

```text
Principles introduced
    P-01 .. P-15   (Article I completo)

Invariants introduced
    INV-01 .. INV-20   (Article II completo)
```

y documentarlo así explícitamente en el capítulo (no forzar el formato estándar cuando no
corresponde semánticamente).

### Paso 4 — Verificar consistencia con invariantes existentes

Para cada `INV-xx` marcado como "preserved", confirmar leyendo
`constitution/ARCHITECTURE_CONSTITUTION.md` Article II que el pseudocódigo del capítulo (sección
11) no lo contradice. Ejemplos de violaciones comunes a buscar:

- un componente ejecuta un side effect sin pasar por `PolicyEngine` → viola INV-06;
- el modelo decide directamente una transición de estado operacional → viola P-10/INV-08;
- un `ToolCall` se ejecuta sin validación previa → viola INV-04.

Si se detecta una violación, el capítulo no puede pasar `validate-chapter` — debe corregirse el
pseudocódigo o, si es un cambio constitucional deliberado, escalarse como modificación de la
Constitution (requiere aprobación humana, fuera de alcance de automatización en BH-v0.1).

### Paso 5 — Validar

```bash
./scripts/validate-chapter <ruta-del-capitulo>
```

`validate-chapter` verifica que la sección "Constitutional Impact" existe y contiene al menos un
`P-xx` o `INV-xx` real (no un placeholder vacío) referenciando artículos que existen en
`constitution/ARCHITECTURE_CONSTITUTION.md`.
