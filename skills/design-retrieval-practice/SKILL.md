---
name: design-retrieval-practice
description: >-
  Procedimiento determinista para derivar el RetrievalSet (Ciclo de Dominio Activo — CDA) de un
  capítulo ya escrito y validado por validate-chapter. Usar después de que un chapter.md pase
  `write-technical-chapter` + `validate-chapter`, y antes de correr `scripts/validate-retrieval-set`.
  No es un "prompt libre": produce datos estructurados que se agregan al bloque `retrieval_set:`
  del frontmatter del capítulo, siguiendo las 10 reglas de
  `planes/2026-08-23-metodo-aprendizaje-activo-lector.md` §3.2.
---

# Skill: design-retrieval-practice

## Cuándo usar esta skill

Cuando un `chapter.md` ya tiene sus 19 secciones obligatorias completas y pasa
`scripts/validate-chapter`, pero todavía no tiene su `retrieval_set` en el frontmatter (o hay que
actualizarlo porque el capítulo cambió). Esta skill no inventa contenido pedagógico nuevo: **deriva**
el `RetrievalSet` de lo que el capítulo ya está obligado a tener — la misma disciplina de "no magic
entities" aplicada a la pedagogía (ver `planes/2026-08-23-metodo-aprendizaje-activo-lector.md` §2.3).

```text
Contract Registry / Component Registry / secciones del capítulo
              │
              ▼
   Generador de tarjetas y preguntas (determinista, esta skill)
              │
              ▼
   RetrievalSet del capítulo (frontmatter retrieval_set:)
```

## Insumos requeridos antes de empezar

1. El `chapter.md` completo, ya validado (`./scripts/validate-chapter <ruta>` sale con `exit 0`).
2. Las secciones 2 (Problem) y 3 (Why the Current Architecture Is Insufficient) del capítulo.
3. `registry/components.yaml` / `registry/contracts.yaml` — específicamente las fichas `owns` /
   `does_not_own` de los componentes que este capítulo introduce (o registra vacío si no
   introduce ninguno).
4. La sección 4 (Constitutional Impact) del capítulo.
5. `frontmatter.introduces_contracts` / `frontmatter.introduces_components` de este capítulo.
6. `book/book.yaml` — para saber cuáles son los 1-2 capítulos **anteriores** (por orden, no por
   número) disponibles para interleaving. Si no hay ninguno (capítulo 0 / primer capítulo del
   libro), ver Paso 6 (excepción documentada).

## Procedimiento — 10 reglas, en orden

### Regla 0 — `expectedOutcome` como capacidad, no como resumen

Redacta `expected_outcome.text` empezando conceptualmente en "Al terminar este capítulo
podrás <verbo de acción: decidir / construir / diagnosticar / distinguir / explicar / evaluar
/ clasificar>...". Nunca "aprenderás sobre..." ni "conocerás...": eso es contenido, no
capacidad. Heurística de `validate-retrieval-set`: el texto debe contener uno de esos verbos de
acción.

### Regla 1 — `skeleton` es un mapa, no un resumen

`skeleton.section_titles` lista los títulos de las 19 secciones del capítulo (o las que existan)
tal cual aparecen como encabezados `## N. ...`, sin explicar su contenido.
`skeleton.contracts_to_be_introduced` / `skeleton.components_to_be_introduced` deben ser
**exactamente** `frontmatter.introduces_contracts` / `frontmatter.introduces_components` de este
mismo capítulo — ni un id de más, ni uno de menos. `validate-retrieval-set` lo verifica por
igualdad de conjuntos.

### Regla 2 — `guidingQuestions` desde Problem/Why-Insufficient, nunca desde New Concepts

Deriva cada `guiding_questions[].text` parafraseando una idea real de la sección 2 o 3 del
capítulo, en lenguaje de problema. Prohibido:

- usar el nombre canónico (PascalCase) de cualquier contrato/componente que este capítulo liste
  en `introduces_contracts` / `introduces_components` (el lector aún no los conoce);
- copiar una oración literal de esas secciones (debe ser una reformulación, no una cita).

Cada `guiding_questions[].answered_by` DEBE apuntar al `id` de una `recall_questions[]` real del
mismo `retrieval_set` (definida en la Regla 5). Construye ambas a la vez si es más simple:
primero decide la pregunta guía, luego escribe su contraparte de recuerdo.

Cantidad objetivo: 3 a 5 (`validate-retrieval-set` no exige el rango si el capítulo es el
capítulo 0 del libro, pero seguir apuntando a 3-5 igual es buena práctica editorial).

### Regla 3 — `systemsLens` reetiqueta, no inventa

Completa cada campo copiando/parafraseando la sección correspondiente — no redactes contenido
nuevo que el capítulo no respalde:

| Campo de `systems_lens` | Se deriva de |
|---|---|
| `iceberg_visible_fact` | §2 Problem |
| `iceberg_patterns` | §3 Why the Current Architecture Is Insufficient |
| `iceberg_structures` | §8 Component Responsibilities (`owns`/`does_not_own`) + políticas de seguridad relevantes (§15) |
| `iceberg_mental_models` | §4 Constitutional Impact |
| `reinforcing_loop` (opcional) | una espiral real si el capítulo la describe (p. ej. en Failure Semantics o Why-Insufficient) |
| `balancing_loop` (opcional) | un mecanismo estabilizador real (p. ej. un validador, un budget, una política) |
| `leverage_point` | la decisión arquitectónica de mayor efecto de este capítulo — normalmente el `owns` del componente/contrato nuevo más importante |

`leverage_point` NUNCA puede quedar vacío y DEBE mencionar, por nombre o por id, un componente o
contrato de `introduces_components` / `introduces_contracts` de este capítulo.

### Regla 4 — Cobertura total: 1 flashcard por entidad introducida ("no magic entities" pedagógico)

Por cada id en `frontmatter.introduces_contracts` y en `frontmatter.introduces_components`, crea
al menos una entrada en `flashcards` con `source_entity` igual a ese id exacto. Sin excepciones —
si un contrato se introduce, existe su tarjeta, aunque el capítulo tenga 20 contratos.

### Regla 5 — `recallQuestions` solo referencian el pasado o el presente

Cada `recall_questions[].text` puede nombrar libremente entidades introducidas en este capítulo o
en capítulos **estrictamente anteriores** según `book/book.yaml`. Nunca una entidad de un
capítulo posterior (regla idéntica a "no magic entities" del pseudocódigo, aplicada aquí a
prosa). `validate-retrieval-set` lo verifica escaneando nombres PascalCase conocidos del
registry contra el índice de capítulos.

### Regla 6 — `interleavedQuestions` mezclan dos capítulos de verdad

Cada `interleaved_questions[].text` DEBE combinar al menos una entidad de `current_chapter_entities`
(de este capítulo) con al menos una de `prior_chapter_entities` (de un capítulo anterior real,
declarado en `prior_chapter`). Mínimo 1 por capítulo, **salvo** que el capítulo no tenga ningún
capítulo anterior en `book/book.yaml` (p. ej. el primer capítulo del libro) — en ese caso, se deja
`interleaved_questions: []` y se documenta la razón explícitamente en
`retrieval_set.interleaving_exception` (campo de texto libre, no inventar un capítulo anterior
falso). `validate-retrieval-set` exime esta regla únicamente cuando `frontmatter.previous_chapter`
es `null`.

### Regla 7 — `explainPrompts` apuntan a un "Owns" y piden explicar el "Does NOT own"

Para cada componente que este capítulo introduzca y cuya ficha en `registry/components.yaml`
tenga `owns` no vacío, crea un `explain_prompts[]` que pida explicar por qué ese componente
posee esa responsabilidad **y** por qué NO posee algo de su `does_not_own`. Si el capítulo no
introduce ningún componente (como el capítulo 0, que solo introduce contratos), aplica la misma
lógica al límite constitucional más cercano disponible — normalmente el límite
Probabilístico/Determinístico (Article XII) o una responsabilidad exclusiva ya declarada en
prosa (p. ej. "el modelo nunca decide X") — y usa `target_entity` como texto libre describiendo
ese límite en vez de un id de registry. Documenta esta sustitución en el registro de ejecución
del capítulo si se usa.

### Regla 8 — `calibrationPairs` van antes de la respuesta, no después

Por cada `recall_questions[]`, agrega un `calibration_pairs[]` con `recall_question` apuntando a
su id y `confidence_levels: [Alta, Media, Baja]`. El lector se autoevalúa ANTES de ver la
respuesta real (instrucción editorial en la sección 21 del capítulo, no un campo adicional del
dato).

### Regla 9 — Toda flashcard nueva nace en `DAY_1`

`review_stage` de toda flashcard recién creada es siempre `DAY_1`. Nunca se crea una tarjeta ya
en `DAY_3`/`DAY_7`/etc. — esos estados solo existen tras un repaso real del lector (fuera de
alcance en v0.1; ver plan §5).

## Dónde escribir el resultado

Todo el `RetrievalSet` se escribe como bloque `retrieval_set:` en el frontmatter YAML del
`chapter.md` (mismo parser `yaml-lite.js` que el resto del frontmatter — soporta mappings
anidados, secuencias y block scalars `|`, ver `scripts/lib/yaml-lite.js`). Las secciones 0
("Preguntas Guía"), 20 ("Lente de Sistemas") y 21 ("Practica lo que Aprendiste") del cuerpo del
capítulo presentan ese mismo contenido en prosa legible para quien lee el Markdown crudo —
deben coincidir con los datos de `retrieval_set`, no divergir de ellos.

## Checklist final antes de entregar

```text
[ ] expectedOutcome usa un verbo de acción (Regla 0).
[ ] skeleton.contractsToBeIntroduced/componentsToBeIntroduced == frontmatter (Regla 1).
[ ] Ninguna guidingQuestion usa un nombre canónico de este capítulo (Regla 2).
[ ] Todo guidingQuestion.answeredBy apunta a un recallQuestion real (Regla 2).
[ ] systemsLens completo y leveragePoint no vacío, referenciando una entidad de este capítulo (Regla 3).
[ ] 1 flashcard por cada contrato/componente introducido, sin excepción (Regla 4).
[ ] Ninguna recallQuestion/explainPrompt referencia una entidad futura (Regla 5).
[ ] >=1 interleavedQuestion, o interleaving_exception documentada si no hay capítulo anterior (Regla 6).
[ ] >=1 explainPrompt sobre un "Does NOT own" (o su equivalente constitucional) (Regla 7).
[ ] calibrationPairs cubre cada recallQuestion (Regla 8).
[ ] Toda flashcard nueva tiene reviewStage = DAY_1 (Regla 9).
```

## Validar

```bash
./scripts/validate-retrieval-set book/chapters/<carpeta-del-capitulo>
```

No considerar el `RetrievalSet` terminado hasta que el comando anterior termine con código de
salida 0.
