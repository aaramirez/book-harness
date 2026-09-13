# Plan — Método de Aprendizaje Activo para el lector del libro

**Fecha:** 2026-08-23 (revisado con transcripciones reales; aprobado 2026-09-13)
**Estado:** ✅ Completado — ver §8 (ejecutado 2026-09-13)
**Depende de:** `2026-08-23-book-harness-como-construir-un-arnes.md` (este documento lo complementa, no lo reemplaza)

---

## 0. Fuentes (revisadas con transcripción real)

Transcripciones provistas por el usuario en `reference/metodo_estudio_harvard.md` y `reference/domina_cualquier_tema_ia.md`. Esta revisión **corrige una atribución incorrecta** de la versión anterior de este documento (ver §0.3).

### 0.1 Video 1 — "El Método de las 5 Rs" (Harvard)

*Canal InvernovAH, basado en investigación de William Perry y Eric Mazur (Harvard).*

- **3 errores fatales al estudiar:**
  1. Estudiar sin preguntas y esperar demasiado para explicar — "lo explicas para darte cuenta de si realmente lo entiendes", no al revés.
  2. Estudiar temas aislados, sin contraste — impide saber *cuándo* aplica una idea y cuándo no.
  3. Creer que más horas es mejor — el foco se mide por intensidad, no por tiempo sentado.
- **Las 5 Rs:**
  1. **Reversibilidad** — antes de abrir el material, define qué te van a pedir hacer con él; estudia hacia atrás desde ese resultado.
  2. **Reducir** — obtén primero la estructura/esqueleto (títulos, secciones) e identifica el 20% esencial antes de los detalles.
  3. **Recordar activamente** (técnica Feynman, inspirada en el cuaderno de Feynman) — cierra el material e intenta explicarlo en voz alta con palabras simples; donde te atasques, ahí está tu punto débil.
  4. **Repasar espaciadamente** (curva del olvido de Ebbinghaus) — repasos con recuperación activa al día siguiente, a los 3 días, al día 7, al día 21.
  5. **Rendimiento profundo** — bloques de ~90 minutos sin distracciones, con un objetivo concreto (inspirado en los *Think Weeks* de Bill Gates).

### 0.2 Video 2 — "Dinámica de Sistemas con IA" (el método real de 1972)

*Canal Xavier Mitjana. El método de 1972 es **Dinámica de Sistemas**, de Jay Forrester (MIT), popularizado después por Donella Meadows — no tiene relación con repetición espaciada.* Idea central: un problema complejo no se entiende mirando sus piezas aisladas, sino cómo se conectan y retroalimentan. El video muestra cómo aplicarlo con IA (NotebookLM) mediante tres lentes:

1. **El Iceberg** — cuatro niveles de profundidad: (1) el hecho visible, (2) los patrones que se repiten en el tiempo, (3) las estructuras/reglas/incentivos que producen esos patrones, (4) los modelos mentales que lo sostienen todo.
2. **Bucles de retroalimentación** — de **refuerzo** (disparan espirales, ej. deuda que genera más deuda) y de **equilibrio** (estabilizan, ej. un fondo de emergencia que corrige desviaciones).
3. **Punto de apalancamiento** — de todas las palancas posibles, cuál cambio pequeño produce el mayor efecto (no la más obvia o repetida, sino la real).

### 0.3 Corrección respecto a la versión anterior de este documento

La versión previa afirmaba que el "método MIT de 1972" era el **sistema Leitner** (cajas de repetición espaciada) potenciado con IA. **Eso es incorrecto** — fue una inferencia hecha sin la transcripción real, basada solo en la coincidencia de la fecha "1972". El método real es Dinámica de Sistemas (Forrester/Meadows), un marco de pensamiento sistémico, no una técnica de memorización. Esta revisión:

- Elimina la atribución a Leitner/MIT del mecanismo de repaso espaciado — el repaso espaciado sigue siendo parte del método, pero correctamente atribuido a **Ebbinghaus vía el Video 1** (día 1 / 3 / 7 / 21, no las cajas Leitner que se habían inventado antes).
- Incorpora **Dinámica de Sistemas** (Iceberg / Bucles / Punto de apalancamiento) como un movimiento nuevo y genuino del método, que la versión anterior no tenía porque se basó en una atribución equivocada.
- Incorpora **Reversibilidad** y **Reducir** (las 5 Rs completas), que la versión anterior omitía por falta de la transcripción real.

---

## 1. Problema que resuelve

El harness definido en el plan base optimiza para que el **contenido sea correcto y arquitectónicamente coherente** (registries, validadores, "no magic entities"). Pero un libro puede ser arquitectónicamente perfecto y aun así **no producir aprendizaje real**: leer no es aprender. `REGLAS_LIBRO_AGENT_HARNESS(1).md` no define ningún mecanismo para forzar preguntas iniciales, recuerdo activo, espaciado, contraste entre capítulos o pensamiento sistémico por parte del lector.

Este documento define esa capa faltante, aplicada a cada capítulo, más los cambios de arquitectura del harness necesarios para producirla de forma sistemática (no como ocurrencia manual de un autor).

---

## 2. El método: Ciclo de Dominio Activo (CDA)

Ocho movimientos organizados en tres fases — **Antes**, **Durante** y **Después** de leer cada capítulo — más una recomendación a nivel de libro (no por capítulo). Cada movimiento cita su fuente real.

```text
ANTES DE LEER  (Sección 0 — abre el capítulo)
─────────────────────────────────────────────
RESULTADO ESPERADO   →  antes de leer, el lector fija qué va a poder
                         HACER con esta arquitectura al terminar
                         (decidir, construir, diagnosticar). Se estudia
                         hacia atrás desde ese resultado.
                         [Fuente: R1 Reversibilidad — Video 1]

ESQUELETO            →  vista previa de la estructura del capítulo
                         (secciones, componentes/contratos que se van
                         a introducir) ANTES de leer el detalle. El 20%
                         esencial primero, para no sobrecargar.
                         [Fuente: R2 Reducir — Video 1]

PREGUNTAR            →  preguntas guía en lenguaje de problema, que el
                         lector debe poder responder al terminar el
                         capítulo. Abren la lectura con intención.
                         [Fuente: Error Fatal 1 ("estudiar sin
                         preguntas") — Video 1]

   ... el lector lee el capítulo con esto en mente ...

DURANTE LA LECTURA  (Sección 20 — al cierre del cuerpo del capítulo)
─────────────────────────────────────────────
LENTE DE SISTEMAS    →  aplicar Iceberg / Bucles de retroalimentación /
                         Punto de apalancamiento a la arquitectura que
                         el capítulo acaba de enseñar (ver §2.2).
                         [Fuente: Dinámica de Sistemas — Video 2]

DESPUÉS DE LEER  (Sección 21 — cierra el capítulo)
─────────────────────────────────────────────
RECORDAR              →  el lector vuelve a las preguntas guía de la
                         Sección 0 y las responde de memoria, sin
                         mirar atrás.
                         [Fuente: Error Fatal 1 + retrieval practice —
                         Video 1]

EXPLICAR              →  explicar un concepto/componente nuevo en voz
                         alta y en lenguaje simple, como a alguien sin
                         contexto técnico — técnica Feynman.
                         [Fuente: R3 Recordar activamente — Video 1]

CONECTAR              →  preguntas que mezclan el capítulo actual con
                         1-2 capítulos previos no consecutivos.
                         [Fuente: Error Fatal 2 ("temas aislados") —
                         Video 1]

ESPACIAR              →  cada concepto nuevo entra a un calendario de
                         repaso con recuperación activa: día 1, día 3,
                         día 7, día 21.
                         [Fuente: R4 Repasar espaciadamente, curva de
                         Ebbinghaus — Video 1]
```

```text
NIVEL DE LIBRO  (no por capítulo — recomendación en el prefacio)
─────────────────────────────────────────────
RENDIMIENTO PROFUNDO  →  leer cada capítulo en un bloque de ~90 min sin
                          distracciones, con un objetivo concreto. El
                          foco importa más que las horas acumuladas.
                          [Fuente: R5 + Error Fatal 3 — Video 1]
```

> Regla rectora: **el libro no está terminado cuando el lector puede pasar la vista por el capítulo. Está terminado cuando puede recordarlo, explicarlo, conectarlo, ubicarlo dentro del sistema completo, y sigue recordándolo semanas después.**

*(Nota: "Calibrar" — predecir confianza antes de ver la respuesta — se mantiene como adición propia de la versión anterior, no proviene de ninguno de los dos videos. Se conserva en el modelo de datos §3 como práctica de metacognición complementaria, pero se marca como tal y no cuenta como parte de las 8 fuentes citadas arriba.)*

### 2.1 Por qué "Preguntar" va primero y por qué no puede usar la jerga del capítulo

Las preguntas guía se leen **antes** de que el capítulo defina sus conceptos nuevos. Si una pregunta usa un nombre canónico que el capítulo mismo va a introducir (p. ej. `ToolRuntime`), el lector no tiene con qué responderla y la pregunta no orienta nada — solo genera ruido.

Regla: las preguntas guía se formulan en el lenguaje del **problema**, no de la **solución**. Se derivan de las secciones "Problem" y "Why the Current Architecture Is Insufficient" (ya obligatorias, §26 de `REGLAS_LIBRO_AGENT_HARNESS`), no de "New Concepts".

```text
Mal  (usa jerga que el capítulo aún no ha definido):
    "¿Qué hace ToolRuntime.execute()?"

Bien (lenguaje de problema, respondible solo después de leer):
    "Si un agente puede ejecutar acciones reales, ¿quién decide si
     una acción es segura, y cómo se hace esa decisión verificable
     en vez de dejarla implícita en el juicio del modelo?"
```

Esto es automatizable: un validador puede rechazar cualquier pregunta guía que contenga un nombre canónico listado en el "Introduces Components/Contracts" de ese mismo capítulo (ver §3.3).

### 2.2 La Lente de Sistemas aplicada a *este* libro específicamente

Esto no es un añadido genérico de "pensamiento sistémico" — encaja con precisión en lo que el harness ya modela, porque un capítulo de este libro **ya es**, estructuralmente, una descripción de sistema:

```text
Iceberg                              →  ya existe en el capítulo como
─────────────────────────────────────────────────────────────────────
1. Hecho visible                     →  "Problem" (la limitación
                                          concreta que dispara el
                                          capítulo)
2. Patrones que se repiten           →  "Why the Current Architecture
                                          Is Insufficient"
3. Estructuras/reglas/incentivos     →  Component Registry (Owns /
   que producen esos patrones           Does NOT own) + Policies
4. Modelos mentales que lo sostienen →  Constitutional Impact
   (Principles / Invariants afectados)

Bucles de retroalimentación          →  ya existe en el capítulo como
─────────────────────────────────────────────────────────────────────
Bucle de refuerzo (espiral)          →  ej. un tool call sin política
                                          de autorización → más
                                          bypasses → más superficie de
                                          fallo (Failure Semantics)
Bucle de equilibrio (estabiliza)     →  ej. un validador determinista
                                          que rechaza la publicación
                                          ante un error estructural
                                          (Quality Gates)

Punto de apalancamiento              →  ya existe en el capítulo como
─────────────────────────────────────────────────────────────────────
La decisión de este capítulo que,    →  normalmente es la frontera de
si cambiara, cambiaría todo lo          responsabilidad nueva que
demás                                   declara la ficha arquitectónica
                                         del componente nuevo (Owns /
                                         Does NOT own)
```

La skill no inventa contenido nuevo: **reetiqueta** secciones que el capítulo ya está obligado a tener, bajo el marco Iceberg/Bucles/Palanca, y le pide al lector que las relea con esa lente antes de pasar a memorizar.

### 2.3 Por qué encaja con la arquitectura del harness (no es un añadido cosmético)

El punto fuerte de este libro es que ya obliga a mantener **Contract Registry** y **Component Registry** con fichas estructuradas (ID, Responsibility, Owns, Depends on...). Eso es, sin quererlo, **material de tarjetas de recuerdo ya perfectamente estructurado**. El método no pide contenido nuevo desde cero: pide **derivar** el material de aprendizaje de lo que el harness ya está obligado a producir.

```text
Contract Registry / Component Registry
              │
              ▼
   Generador de tarjetas (determinista)
              │
              ▼
   RetrievalSet del capítulo (preguntas + tarjetas + calendario)
```

---

## 3. Qué se agrega al modelo del Book Harness

Extensiones puntuales sobre lo ya definido en el plan base (no lo contradicen, lo amplían):

### 3.1 Nueva estructura en `ChapterIR`

```text
STRUCT RetrievalSet
    expectedOutcome: ExpectedOutcome             # "Resultado Esperado"
    skeleton: ChapterSkeleton                    # "Esqueleto"
    guidingQuestions: List<GuidingQuestion>      # "Preguntar"
    systemsLens: SystemsLensBlock                # "Lente de Sistemas"
    recallQuestions: List<RecallQuestion>        # "Recordar"
    explainPrompts: List<ExplainPrompt>          # "Explicar"
    interleavedQuestions: List<InterleavedQuestion>  # "Conectar"
    flashcards: List<Flashcard>                  # "Espaciar"
    calibrationPairs: List<CalibrationPair>      # "Calibrar" (adición
                                                  # propia, no citada
                                                  # de los videos)
END

STRUCT ExpectedOutcome
    id: ExpectedOutcomeId
    text: Text                 # "al terminar este capítulo podrás..."
                                # decidir / construir / diagnosticar X
END

STRUCT ChapterSkeleton
    id: ChapterSkeletonId
    sectionTitles: List<Text>              # vista previa de secciones
    componentsToBeIntroduced: List<ComponentId>
    contractsToBeIntroduced: List<ContractId>
END

STRUCT GuidingQuestion
    id: GuidingQuestionId
    text: Text                          # lenguaje de problema, sin jerga
                                         # introducida por este capítulo
    answeredBy: QuestionId              # RecallQuestion que la cierra
END

STRUCT SystemsLensBlock
    icebergVisibleFact: Text            # = Problem
    icebergPatterns: Text                # = Why Current Architecture
                                          #   Is Insufficient
    icebergStructures: Text              # = Component Registry
                                          #   Owns/Does NOT own + Policies
    icebergMentalModels: Text            # = Constitutional Impact
    reinforcingLoop: Optional<Text>      # espiral si no se corrige
    balancingLoop: Optional<Text>        # mecanismo que estabiliza
    leveragePoint: Text                  # la decisión de este capítulo
                                          # con mayor efecto
END

STRUCT Flashcard
    id: FlashcardId
    front: Text
    back: Text
    sourceEntity: ContractId | ComponentId         # de dónde se derivó
    chapterIntroducedIn: ChapterId
    reviewStage: ReviewStage                       # estado inicial = DAY_1
END

ENUM ReviewStage
    DAY_1
    DAY_3
    DAY_7
    DAY_21
    MASTERED
END
```

```text
STRUCT ChapterIR
    ...                          # campos ya definidos en el plan base
    retrievalSet: RetrievalSet   # NUEVO
END
```

> Cambio respecto a la versión anterior: `LeitnerBox` (5 cajas, calendario 1/3/7/16/35 inventado sin fuente real) se reemplaza por `ReviewStage` (4 pasos, calendario 1/3/7/21, citado directamente del Video 1 — curva de Ebbinghaus).

### 3.2 Nueva skill: `design-retrieval-practice`

`skills/design-retrieval-practice/SKILL.md` — procedimiento determinista de generación, no "prompt libre":

```text
INPUT:
    chapter draft (ya validado por validate-chapter)
    secciones "Problem" y "Why the Current Architecture Is
        Insufficient" del capítulo
    Component Registry / Contract Registry (para Owns / Does NOT own)
    Constitutional Impact declarado en el capítulo
    contracts introducidos/modificados en este capítulo
    components introducidos/modificados en este capítulo
    conceptos de los 2 capítulos anteriores (para interleaving)

REGLAS:
    0. expectedOutcome se redacta como una capacidad ("al terminar
       podrás decidir/construir/diagnosticar..."), nunca como un
       resumen de contenido.
    1. skeleton lista los títulos de sección y los componentes/
       contratos que el capítulo va a introducir, SIN explicarlos
       todavía — es un mapa, no un resumen.
    2. guidingQuestions se generan a partir de "Problem" / "Why the
       Current Architecture Is Insufficient", NUNCA de "New Concepts".
       Deben ser respondibles en lenguaje de problema y NO pueden
       contener ningún nombre canónico que este capítulo liste en
       "Introduces Components" o "Introduces Contracts".
       Cada guidingQuestion.answeredBy DEBE apuntar a una
       recallQuestion real de este mismo RetrievalSet.
    3. systemsLens.icebergVisibleFact / icebergPatterns /
       icebergStructures / icebergMentalModels se derivan
       respectivamente de "Problem" / "Why the Current Architecture
       Is Insufficient" / Component Registry (Owns, Does NOT own) +
       Policies / Constitutional Impact — NO se inventa contenido
       nuevo, se reetiqueta contenido ya obligatorio del capítulo.
       leveragePoint DEBE señalar una única decisión arquitectónica
       de este capítulo (normalmente el "Owns" del componente nuevo).
    4. Toda entidad marcada "Introduces Components/Contracts" en el
       capítulo DEBE producir al menos 1 flashcard.  (mismo principio
       "no magic entities", aplicado a la pedagogía)
    5. recallQuestions solo pueden referenciar entidades ya
       introducidas en este capítulo o anteriores — igual que el
       pseudocódigo. Nunca una entidad "futura".
    6. interleavedQuestions DEBEN mezclar al menos una entidad del
       capítulo actual con una de un capítulo anterior distinto.
    7. explainPrompts se generan para todo componente cuya ficha
       incluya "Owns" — pedir explicar por qué posee esa
       responsabilidad y por qué NO posee lo declarado en
       "Does NOT own".
    8. calibrationPairs empareja cada recallQuestion con un campo de
       autoevaluación de confianza (Alta/Media/Baja) ANTES de revelar
       la respuesta.
    9. Toda flashcard nueva entra en reviewStage = DAY_1.

OUTPUT:
    RetrievalSet completo para el capítulo.
```

### 3.3 Nuevo validador determinista: `validate-retrieval-set`

Agregado a `scripts/` (Fase 4 del plan base):

```text
validate-retrieval-set:
    [ ] expectedOutcome existe y está redactado como capacidad, no
        como resumen (heurística: contiene un verbo de acción).
    [ ] skeleton.componentsToBeIntroduced / contractsToBeIntroduced
        coinciden exactamente con "Introduces Components/Contracts"
        declarados en el capítulo.
    [ ] Existen entre 3 y 5 guidingQuestions (si el capítulo no es
        el capítulo 0).
    [ ] Ninguna guidingQuestion contiene un nombre canónico listado
        en "Introduces Components" / "Introduces Contracts" de ESTE
        capítulo (chequeo de regex contra los registries).
    [ ] Todo guidingQuestion.answeredBy apunta a una recallQuestion
        que existe en el mismo RetrievalSet.
    [ ] systemsLens.leveragePoint no está vacío y referencia un
        componente o contrato introducido en este capítulo.
    [ ] Cada Contract/Component "Introduces" en el capítulo tiene
        >= 1 flashcard asociada.
    [ ] Ninguna recallQuestion / explainPrompt referencia una entidad
        no introducida hasta este capítulo.
    [ ] Existe >= 1 interleavedQuestion si el capítulo no es el
        capítulo 0.
    [ ] Toda flashcard nueva tiene reviewStage = DAY_1 al crearse.

La pipeline de publicación falla si este validador falla — misma
regla que validate-chapter (sección 8 del plan base).
```

### 3.4 Renderizado

- **Web**: al INICIO de cada capítulo (Sección 0, antes de "1. Current Architecture"), una caja destacada no colapsable con `expectedOutcome`, `skeleton` y las `guidingQuestions` (sin respuestas). Al cierre del cuerpo (Sección 20), un bloque "Lente de Sistemas" con las cuatro capas del iceberg, los bucles y el punto de apalancamiento — presentado como relectura, no como contenido nuevo. Al FINAL (Sección 21), bloque plegable "Practica lo que aprendiste" con Recordar / Explicar / Conectar / Espaciar / Calibrar. Las flashcards alimentan una vista global `/repaso` con el calendario de `ReviewStage` — **esto puede quedar fuera de v0.1** y entrar en v0.2 (ver §5), pero el `RetrievalSet` ya se genera desde v0.1 para no reescribir el modelo de datos después.
- **PDF**: la misma caja de apertura impresa en la página inicial del capítulo. Antes del cierre, una página "Lente de Sistemas". Al final, una página de "Repaso" con las preguntas de recuerdo (sin respuesta) y un apéndice final del libro con todas las flashcards agrupadas.
- **Prefacio del libro** (`book/frontmatter/preface.md` o `introduction.md`, no por capítulo): una nota "Cómo leer este libro" que recomienda **Rendimiento Profundo** — leer cada capítulo en un bloque de ~90 minutos sin distracciones. No es contenido de `ChapterIR`; es texto fijo del frontmatter.

---

## 4. Cómo se integra en la estructura de capítulo ya obligatoria

`REGLAS_LIBRO_AGENT_HARNESS(1).md` §26 define 19 secciones obligatorias por capítulo, empezando en "1. Current Architecture" y terminando en "19. Next Increment". Se agregan tres puntos — **no se reemplaza ni renumera ninguna sección existente**:

```text
0. Preguntas Guía                ← NUEVA (abre el capítulo: Resultado
                                    Esperado + Esqueleto + Preguntas
                                    Guía, antes de la sección 1)
1. Current Architecture          (ya existente)
...
19. Next Increment               (ya existente)
20. Lente de Sistemas            ← NUEVA (Iceberg / Bucles / Punto de
                                    apalancamiento, releyendo el propio
                                    capítulo)
21. Practica lo que aprendiste   ← NUEVA (Recordar / Explicar /
                                    Conectar / Espaciar / Calibrar)
```

Las secciones 0, 20 y 21 se numeran como umbral y cierre, no como pasos más de la secuencia arquitectónica "Problem → ... → New Architecture" que ya rige el cuerpo del capítulo (1-19). Esto mantiene intacta toda la doctrina editorial ya definida.

---

## 5. Alcance para v0.1 vs. después

**Sí entra en v0.1** (extiende el milestone del plan base sin agrandarlo mucho):
- `RetrievalSet` completo en `ChapterIR` (incluyendo `expectedOutcome`, `skeleton`, `guidingQuestions`, `systemsLens`).
- Skill `design-retrieval-practice` con las 10 reglas de §3.2.
- Validador `validate-retrieval-set` con los 9 chequeos de §3.3.
- Secciones 0, 20 y 21 renderizadas en Web y PDF como bloques estáticos, **sin** lógica de calendario interactivo todavía.
- Nota "Cómo leer este libro" en el frontmatter.

**Explícitamente fuera de v0.1** (roadmap):
- Vista `/repaso` interactiva con estado persistido de `ReviewStage` por lector (necesita `SessionManager`/persistencia — no existe hasta que el harness migre a los primitivos genéricos, sección 19 del plan base). → **BH-v0.5 o posterior**.
- Auditoría de la Lente de Sistemas y del `RetrievalSet` por un reviewer dedicado (`Pedagogical Reviewer Agent`, ya reservado para BH-v0.2). → **BH-v0.2**.
- Exportar las flashcards a una app externa de repetición espaciada (Anki, etc.) — queda como nota, no como entregable.

---

## 6. Criterio de éxito del método (qué significa que "funcionó")

No basta con que el `RetrievalSet` exista y pase el validador. Se considera que el capítulo cumple el CDA cuando:

```text
[ ] El lector puede decir, antes de leer, qué va a poder HACER al
    terminar el capítulo (expectedOutcome), no solo qué va a leer.
[ ] Las preguntas guía son respondibles solo en lenguaje de problema
    — un lector que solo vio el esqueleto NO puede responderlas
    todavía, pero SÍ puede entenderlas.
[ ] Cada pregunta guía tiene su contraparte de recuerdo al final,
    con la misma pregunta de fondo, ahora respondible con precisión.
[ ] El lector puede ubicar el capítulo en las cuatro capas del
    iceberg y nombrar al menos un bucle de refuerzo o de equilibrio
    presente en la arquitectura enseñada.
[ ] Cada componente/contrato introducido tiene una flashcard.
[ ] Existe al menos una pregunta que fuerza a explicar un límite
    ("Does NOT own"), no solo una definición.
[ ] Existe al menos una pregunta de interleaving con un capítulo
    anterior no consecutivo.
[ ] El lector nunca puede responder una pregunta copiando texto
    literal de la página anterior — debe reformular.
```

El último punto no es automatizable por completo en v0.1; se deja como criterio de revisión editorial humana hasta que exista un reviewer dedicado.

---

## 7. Siguiente paso

Este documento queda en `/planes` junto al plan base, ya corregido con las transcripciones reales. Si lo apruebas, la Fase 3/4/6 del plan base (`2026-08-23-book-harness-como-construir-un-arnes.md`) se ejecutan incorporando ya las extensiones de este documento (§3), en vez de hacerlo en una segunda pasada.

---

## 8. Registro de ejecución

**Fecha de ejecución:** 2026-09-13 (segunda pasada, retrofit sobre BH-v0.1 ya commiteado en
`3e2575b`).
**Resultado:** el Ciclo de Dominio Activo (CDA) queda incorporado al modelo del harness y al
capítulo piloto (`CH-00`). `./scripts/build-all` corre en verde con el validador nuevo integrado.

### 8.1 Qué se creó

```text
skills/design-retrieval-practice/SKILL.md
scripts/validate-retrieval-set
```

### 8.2 Qué se modificó

```text
scripts/lib/book-ir.js                                    (STRUCT RetrievalSet + normalizeRetrievalSet + ChapterIR.retrievalSet)
scripts/build-all                                          (validate-retrieval-set por capítulo, antes de construir)
scripts/build-book-ir                                      (log de conteo de flashcards)
scripts/build-web                                          (caja de apertura / Lente de Sistemas / Practica lo que aprendiste)
scripts/build-pdf                                          (idem para PDF + apéndice final de flashcards + -f markdown+raw_tex)
book/chapters/00-arquitectura-constitucion/chapter.md       (retrieval_set: en frontmatter + secciones 0/20/21)
book/frontmatter/preface.md                                (nota "Cómo leer este libro")
planes/2026-08-23-metodo-aprendizaje-activo-lector.md       (este registro)
```

### 8.3 Decisiones de diseño no 100% especificadas en el plan, tomadas durante la implementación

1. **Dónde vive el `RetrievalSet` fuente**: el plan (§3.1) define el STRUCT pero no dice dónde se
   autoriza. Se decidió seguir el mismo principio ya usado para contratos/componentes:
   frontmatter/registry = fuente estructurada, prosa del capítulo = presentación legible de esos
   mismos datos. Se agregó un bloque `retrieval_set:` al frontmatter YAML de `chapter.md`
   (parseado por el mismo `yaml-lite.js` que ya procesa el resto del frontmatter — sin tocar su
   código, solo usando mappings/secuencias/block scalars que ya soporta). Las secciones 0, 20 y
   21 del cuerpo del capítulo son prosa escrita a mano para coincidir con esos datos, no
   generadas automáticamente a partir de ellos — igual que la sección 7 ("New Contracts") ya
   repetía en prosa lo que también vive en `registry/contracts.yaml`.
2. **Structs no completamente especificados en el plan**: §3.1 define en detalle
   `ExpectedOutcome`, `ChapterSkeleton`, `GuidingQuestion`, `SystemsLensBlock`, `Flashcard` y
   `ReviewStage`, pero solo menciona `RecallQuestion`, `ExplainPrompt`, `InterleavedQuestion` y
   `CalibrationPair` como `List<...>` sin especificar sus campos. Se diseñaron como:
   `RecallQuestion{id,text}`, `ExplainPrompt{id,text,targetEntity}`,
   `InterleavedQuestion{id,text,currentChapterEntities,priorChapterEntities,priorChapter}`,
   `CalibrationPair{id,recallQuestion,confidenceLevels}` — documentado en el comentario de
   cabecera de `scripts/lib/book-ir.js`.
3. **Campo `interleavingException` (extensión no pedida por el STRUCT del plan)**: se agregó a
   `RetrievalSet` un campo de texto opcional para documentar, cuando un capítulo no tiene
   capítulo anterior (como `CH-00`), por qué `interleavedQuestions` queda vacío — en vez de
   inventar un capítulo previo falso (instrucción explícita del encargo de esta ejecución).
   `validate-retrieval-set` exige que este campo exista cuando el capítulo es el capítulo 0 y
   `interleavedQuestions` está vacío — no permite el vacío silencioso.
4. **Regla 7 (`explainPrompts` sobre "Owns"/"Does NOT own") adaptada para `CH-00`**: el capítulo
   piloto no introduce ningún componente (`registry/components.yaml` sigue vacío), así que no
   existe una ficha con `owns`/`does_not_own` real de la cual derivar el prompt. Se aplicó la
   misma lógica al límite constitucional más cercano disponible: el límite
   Probabilístico/Determinístico (Article XII, "qué decide el modelo y qué nunca decide") y al
   límite de responsabilidad de `HarnessError` (clasifica el fallo, pero no decide el reintento).
   `targetEntity` acepta texto libre para este caso (no solo `ContractId`/`ComponentId`),
   documentado en la skill y en `scripts/lib/book-ir.js`.
5. **Render Web/PDF: secciones 0/20/21 no se duplican**. En vez de renderizar la prosa genérica
   de las secciones 0/20/21 Y además una caja estructurada con los mismos datos, `build-web` y
   `build-pdf` excluyen explícitamente esos tres números de sección del recorrido genérico de
   secciones y los reemplazan por bloques construidos desde `chapter.retrievalSet` — evita mostrar
   el mismo contenido dos veces con dos formatos distintos.
6. **PDF: extensión de lector `raw_tex` y bug de entorno con `---`**. El pandoc 1.19.2.4 instalado
   no pasa `\newpage` a LaTeX salvo que el reader tenga la extensión `raw_tex` habilitada
   (`-f markdown+raw_tex`, agregado a `scripts/build-pdf`). Durante la prueba se encontró además
   un bug preexistente del entorno pandoc/xelatex: un separador markdown `---` (thematic break)
   falla al compilar (`! Missing number, treated as zero` / `\linethickness` indefinido),
   reproducido de forma aislada con un `.md` mínimo sin ningún contenido de este plan — no es un
   bug introducido por esta ejecución. Se evitó generando el apéndice de flashcards sin
   separadores `---` (usando solo espaciado en blanco entre tarjetas).
7. **Frontmatter elegido para "Cómo leer este libro"**: `book/frontmatter/preface.md` (no
   `introduction.md`) — el prefacio ya habla del libro y de su propia forma de producción;
   `introduction.md` está dedicado al mapa de contenido técnico ("Qué vas a construir"). Se
   documenta además, por inspección de código, que `book/frontmatter/{preface,introduction}.md`
   **no están conectados a `BookIR`/Web/PDF en absoluto** en BH-v0.1 (ni `book-ir.js` ni
   `build-web`/`build-pdf` los leen) — brecha preexistente del harness base, no introducida ni
   corregida por esta ejecución (fuera del alcance pedido: solo se pidió agregar la nota al
   archivo correcto, no conectar el frontmatter al pipeline).
8. **`validate-retrieval-set` no depende de construir el `BookIR` completo del libro**: para no
   acoplar la validación de un capítulo a que todos los demás capítulos del libro estén bien
   formados, se exportó `normalizeRetrievalSet` desde `scripts/lib/book-ir.js` y el validador la
   usa directamente sobre el frontmatter ya parseado de un solo capítulo, en vez de invocar
   `buildBookIR()` (que itera `book/book.yaml` completo).
9. **Conteo de chequeos**: el encargo de esta ejecución habla de "9 chequeos" para
   `validate-retrieval-set`, pero la lista real de §3.3 enumera 10 viñetas distintas. Se
   implementaron las 10, sin omitir ninguna.

### 8.4 Resultado real del pipeline (build limpio)

Comando: `rm -rf dist && ./scripts/build-all` (raíz del repo):

```text
=== build-all: validación determinista ===
▶ validate-contracts
validate-contracts: OK (7 contrato(s))
▶ validate-components
validate-components: OK (0 componente(s))
▶ validate-chapter book/chapters/00-arquitectura-constitucion/chapter.md
validate-chapter: OK (.../chapter.md)
  secciones: 22/19
  bloques pseudocode: 12
  contratos introducidos: 7
  componentes introducidos: 0
▶ validate-retrieval-set book/chapters/00-arquitectura-constitucion/chapter.md
validate-retrieval-set: OK (.../chapter.md)
  guidingQuestions: 5
  recallQuestions: 5
  explainPrompts: 2
  interleavedQuestions: 0 (exención capítulo 0, documentada)
  flashcards: 7
  calibrationPairs: 5

=== build-all: construcción ===
▶ build-book-ir
build-book-ir: OK → dist/book-ir.json
  capítulos: 1 / contratos: 7 / componentes: 0 / términos de glosario: 12
  flashcards (retrievalSet): 7
▶ build-web
build-web: OK → dist/web/ (index.html + 1 capítulo)
▶ build-pdf
build-pdf: OK → dist/book.pdf (94644 bytes)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
BookState persistido en dist/book-state.json
```

Exit code: `0`.

**Pruebas negativas** (en copias/temporales, restauradas después):

- Se insertó el nombre canónico `AgentMessage` (introducido por `CH-00`) dentro de una
  `guidingQuestion` real del frontmatter → `validate-retrieval-set` falló señalando exactamente
  esa pregunta, y `./scripts/build-all` se detuvo en la etapa de validación con
  `exit 1` **sin** llegar a `build-book-ir`/`build-web`/`build-pdf` (confirmado: tras el fallo,
  `dist/` solo contenía `book-state.json` con `buildStatus` de fallo — ningún `book-ir.json`,
  `web/` ni `book.pdf`). Al restaurar el archivo original, `build-all` volvió a pasar limpio con
  `exit 0`.
- Se eliminó la única flashcard con `source_entity: C-012` (`ExecutionBudget`, contrato
  introducido por este capítulo) de una copia del capítulo → `validate-retrieval-set` falló con
  `El contrato "C-012" está en introduces_contracts pero no tiene ninguna flashcard con
  sourceEntity = "C-012"` y `exit 1`.

**Inspección de artefactos generados** (no solo del Markdown fuente):

- `dist/web/chapters/CH-00.html`: contiene la caja `<div class="cda-box opening">` con
  Resultado esperado / Esqueleto / Preguntas guía antes de la sección 1, el bloque
  `<div class="cda-box systems-lens">` después de la sección 19, y el `<details>` plegable
  "Practica lo que aprendiste" con Recordar/Explicar/Conectar/Espaciar/Calibrar al final —
  confirmado por grep sobre el HTML generado, no sobre `chapter.md`.
- `dist/book.pdf`: 20 páginas (antes: 1 sin CDA sería menos); se confirmó por extracción de
  texto del PDF (no del Markdown intermedio) la presencia de "Resultado esperado", "Preguntas
  guía", "Lente de Sistemas", "Repaso" y "Apéndice" — es decir, las secciones CDA llegan
  realmente renderizadas al PDF final, con salto de página real (`\newpage` vía
  `-f markdown+raw_tex`) antes de "Lente de Sistemas", antes de "Repaso" y antes del apéndice.

### 8.5 Contraste contra el criterio de éxito real (§6 del plan)

```text
[✅] El lector puede decir, antes de leer, qué va a poder HACER al terminar el capítulo
     (expectedOutcome) — Sección 0 del capítulo + caja de apertura en Web/PDF.
[✅] Las preguntas guía son respondibles solo en lenguaje de problema — verificado
     automáticamente (validate-retrieval-set chequeo 4: ninguna guidingQuestion contiene un
     nombre canónico introducido por este capítulo) y por revisión editorial del contenido real.
[✅] Cada pregunta guía tiene su contraparte de recuerdo al final, con la misma pregunta de
     fondo — guidingQuestion.answeredBy → recallQuestion, 5/5, verificado por el chequeo 5.
[✅] El lector puede ubicar el capítulo en las cuatro capas del iceberg y nombrar al menos un
     bucle — systemsLens completo con icebergVisibleFact/Patterns/Structures/MentalModels +
     reinforcingLoop + balancingLoop, ambos presentes (no solo uno).
[✅] Cada componente/contrato introducido tiene una flashcard — 7/7 contratos cubiertos
     (0 componentes en este capítulo), verificado por el chequeo 7 y probado en negativo.
[✅] Existe al menos una pregunta que fuerza a explicar un límite ("Does NOT own") — 2
     explainPrompts, adaptados (ver §8.3.4) porque CH-00 no introduce componentes con ficha
     Owns/Does NOT own todavía.
[⚠️] Existe al menos una pregunta de interleaving con un capítulo anterior no consecutivo — NO
     se cumple para CH-00 específicamente, y no puede cumplirse honestamente: es el primer
     capítulo del libro, no existe un capítulo anterior real. Documentado explícitamente como
     excepción (retrievalSet.interleavingException) en vez de inventar un capítulo falso, tal
     como pedía el encargo de esta ejecución. validate-retrieval-set exime esta regla solo para
     el capítulo 0; se cumplirá de forma real a partir de CH-01.
[⬜] El lector nunca puede responder copiando texto literal de la página anterior — el propio
     plan (§6, último punto) declara esto explícitamente NO automatizable en v0.1; queda como
     criterio de revisión editorial humana hasta que exista un reviewer dedicado (BH-v0.2+).
```

6 de 8 cumplidos en automático + revisión editorial, 1 exención documentada (estructural, no
evitable en el primer capítulo del libro) y 1 explícitamente fuera de alcance de v0.1 según el
propio plan.

### 8.6 Deuda intencional hacia v0.2+ (según §5 del propio plan)

Sin cambios respecto a lo ya declarado en el plan — se re-confirma que ninguno de estos tres
puntos se implementó, tal como estaba decidido:

- Vista `/repaso` interactiva con `ReviewStage` persistido por lector — necesita
  `SessionManager`/persistencia, que no existe hasta que el harness migre a primitivos genéricos.
- Auditoría del `RetrievalSet`/Lente de Sistemas por un `Pedagogical Reviewer Agent` dedicado.
- Exportación de flashcards a una app externa de repetición espaciada (Anki u otra).

A esto se suma, identificado durante esta ejecución:

- `book/frontmatter/{preface,introduction}.md` siguen sin conectarse a `BookIR`/Web/PDF (§8.3.7)
  — no es parte del alcance de este plan, pero es una brecha real del harness base que un futuro
  incremento debería cerrar si se espera que el prefacio (con su nueva nota "Cómo leer este
  libro") llegue a los lectores de la edición Web/PDF, no solo a quien lee el repositorio.
- La vista `/repaso` (fuera de v0.1) también implica, cuando se construya, decidir cómo el
  lector marca una flashcard como repasada y cómo eso mueve su `reviewStage` — el modelo de
  datos ya lo soporta (`ReviewStage` enum completo), pero no hay ningún mecanismo de escritura
  todavía, ni siquiera manual.
