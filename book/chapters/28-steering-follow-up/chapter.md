---
id: CH-28
title: "Entradas que Llegan Durante el Turno: Steering y Follow-up"
starting_version: "0.1"
ending_version: "0.2"
introduces_components: []
introduces_contracts: [C-036]
modifies_contracts: []
constitutional_articles: [P-10, P-12, P-13, INV-07, INV-08, INV-10, INV-15, INV-18, INV-19]
previous_chapter: CH-27
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH28
    text: |
      Al terminar este capítulo podrás decidir, para cualquier mensaje que un usuario envía
      mientras el turno de un agente todavía corre, en qué frontera exacta del turno debe
      aplicarse (antes de la próxima llamada al modelo, o solo cuando el agente iba a terminar) —
      y podrás distinguir ese mensaje de una resolución humana, de una cancelación y de una
      autorización, que el arnés ya asigna a dueños distintos.
  skeleton:
    id: SK-CH28
    section_titles:
      - "1. Arquitectura Actual (Current Architecture)"
      - "2. El Problema (Problem)"
      - "3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)"
      - "4. Impacto Constitucional (Constitutional Impact)"
      - "5. Conceptos Nuevos (New Concepts)"
      - "6. Nuevas Estructuras de Datos (New Data Structures)"
      - "7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)"
      - "8. Responsabilidades de Componentes (Component Responsibilities)"
      - "9. Relaciones de Dependencia (Dependency Relationships)"
      - "10. Diagrama de Secuencia (Sequence Diagram)"
      - "11. Pseudocódigo (Pseudocode)"
      - "12. Transiciones de Estado (State Transitions)"
      - "13. Semántica de Fallos (Failure Semantics)"
      - "14. Eventos Producidos (Events Produced)"
      - "15. Implicaciones de Seguridad / Política (Security / Policy Implications)"
      - "16. Tests (Tests)"
      - "17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)"
      - "18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)"
      - "19. Siguiente Incremento (Next Increment)"
    components_to_be_introduced: []
    contracts_to_be_introduced: [C-036]
  guiding_questions:
    - id: GQ-CH28-01
      text: |
        Si el usuario escribe una corrección mientras el agente está esperando el resultado de
        una herramienta, ¿debería esa corrección detener la herramienta que ya está corriendo, o
        esperar a un punto posterior del turno — y cuál sería ese punto?
      answered_by: RQ-CH28-01
    - id: GQ-CH28-02
      text: |
        Si el modelo dice que ya terminó, pero el usuario dejó un mensaje pendiente "para cuando
        acabes", ¿quién decide que el turno en realidad no termina todavía: el modelo o el arnés?
      answered_by: RQ-CH28-02
    - id: GQ-CH28-03
      text: |
        Si llegan tres mensajes seguidos mientras el turno corre, ¿se entregan todos juntos o uno
        por vez — y quién decide eso: el mensaje, el usuario o una regla fija de la cola?
      answered_by: RQ-CH28-03
    - id: GQ-CH28-04
      text: |
        Si un mensaje que llega a mitad del turno dice "sí, aprobado", ¿alcanza para dar por
        resuelta una aprobación humana pendiente, o para cancelar la ejecución?
      answered_by: RQ-CH28-04
  systems_lens:
    iceberg_visible_fact: |
      Un usuario escribe mientras el agente todavía trabaja, y la implementación no sabe qué hacer
      con ese mensaje: o lo descarta, o corta la herramienta que estaba corriendo, o lo mete en el
      contexto en un punto arbitrario — tres comportamientos distintos para la misma situación,
      ninguno declarado (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que, sin fronteras declaradas dentro del turno, cualquier mensaje
      nuevo termina resuelto por el código que lo recibió en ese instante: la UI decide cortar, el
      canal decide encolar, el modelo decide si "ya terminó". La continuación del turno — que
      Article III asigna a AgentLoop — se fragmenta entre actores que no la poseen (ver sección 3).
    iceberg_structures: |
      Este capítulo introduce PendingInput (C-036) y dos fronteras explícitas del turno
      (BEFORE_MODEL_CALL para el steering, WOULD_COMPLETE para el follow-up), ambas dentro del
      owns ya existente de AgentLoop (turn lifecycle, continuation). Una entrada pendiente no es
      una resolución humana, ni una cancelación, ni una autorización (ver sección 8 y sección 15).
    iceberg_mental_models: |
      El modelo mental es P-10: el arnés — no el modelo — es dueño del estado de ejecución. El
      modelFinished del modelo es una propuesta; AgentLoop decide si el turno termina, y puede
      anular esa propuesta mientras quede una entrada pendiente (ver sección 4).
    reinforcing_loop: |
      Cada mensaje que una implementación descarta en silencio "porque el agente estaba ocupado"
      obliga al usuario a repetirlo, lo que produce más mensajes durante turnos en curso — y más
      descartes. Declarar la cola y sus fronteras corta esa espiral: ningún mensaje se pierde, solo
      espera su frontera.
    balancing_loop: |
      El modo de la cola (ONE_AT_A_TIME o ALL) es el mecanismo de equilibrio: impide que una ráfaga
      de mensajes se aplique entera de golpe cuando el diseño quiere una corrección por turno, y
      permite agruparlos cuando el diseño lo prefiere — una regla fija de la cola, nunca una
      decisión de cada mensaje.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que PendingInput (C-036) solo pueda
      aplicarse en dos fronteras declaradas del turno, y que en WOULD_COMPLETE la decisión final
      sea de AgentLoop y no del modelo. Si esa frontera no se fija aquí, cada canal futuro (CH-34)
      reinventaría cuándo "interrumpir" al agente.
  recall_questions:
    - id: RQ-CH28-01
      text: |
        ¿En qué frontera del turno se aplica una entrada PendingInput con kind = STEER, y por qué
        nunca interrumpe una tool que ToolRuntime ya está ejecutando (INV-07)?
    - id: RQ-CH28-02
      text: |
        ¿Qué hace resolveCompletionWithPendingInput cuando el modelo propone modelFinished = TRUE
        pero la cola todavía tiene un follow-up pendiente, y qué valor le llega entonces a runTurn?
    - id: RQ-CH28-03
      text: |
        ¿Dónde vive el modo de entrega (ONE_AT_A_TIME / ALL) — en cada PendingInput o en la cola
        — y qué devuelve takeByMode en cada caso?
    - id: RQ-CH28-04
      text: |
        ¿Por qué una PendingInput nunca puede resolver una HumanInteractionRequest pendiente ni
        cancelar un AgentRun, aunque su texto diga "aprobado" o "detente"?
  explain_prompts:
    - id: EP-CH28-01
      text: |
        La decisión "¿en qué frontera del turno se aplica un mensaje pendiente?" pertenece a
        AgentLoop porque es continuación del turno (Article III). Explica, como si hablaras con
        alguien sin contexto técnico, por qué AgentLoop NO posee la ejecución de la tool que ya
        está corriendo — ¿qué se rompería si un steering pudiera cortarla a la mitad?
      target_entity: CMP-001
    - id: EP-CH28-02
      text: |
        Usando P-10 y P-13, explica por qué el texto de una PendingInput — aunque diga "aprobado" —
        no es una autorización ni una resolución humana: ¿qué componente ya introducido posee esa
        decisión, y con qué contrato la representa?
      target_entity: C-036
  interleaved_questions:
    - id: IQ-CH28-01
      text: |
        Una PendingInput con kind = STEER y una HumanInteractionResolution (CH-06) pueden llegar
        por el mismo canal y a la misma sesión. ¿Qué campo del contrato de CH-06 vincula su
        resolución a una solicitud concreta, y por qué una PendingInput no tiene (ni necesita) ese
        vínculo?
      current_chapter_entities: [C-036]
      prior_chapter_entities: [C-016, CMP-006]
      prior_chapter: CH-06
  flashcards:
    - id: FC-CH28-01
      front: |
        ¿Qué es una PendingInput (C-036) y qué campos tiene?
      back: |
        Una entrada del usuario que llegó mientras el turno corre: id, runId, kind
        (PendingInputKind — STEER / FOLLOW_UP), message (AgentMessage, rol USER) y receivedAt. No
        es una resolución humana ni una cancelación ni una autorización.
      source_entity: C-036
      chapter_introduced_in: CH-28
      review_stage: DAY_1
    - id: FC-CH28-02
      front: |
        ¿En qué frontera se aplica un STEER y en cuál un FOLLOW_UP?
      back: |
        STEER: BEFORE_MODEL_CALL — después de que las tools del paso devolvieron su resultado y
        antes de la próxima llamada al modelo. FOLLOW_UP: WOULD_COMPLETE — solo cuando el turno iba
        a terminar; el arnés anula el modelFinished del modelo mientras quede uno pendiente.
      source_entity: C-036
      chapter_introduced_in: CH-28
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH28-01
      recall_question: RQ-CH28-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH28-02
      recall_question: RQ-CH28-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH28-03
      recall_question: RQ-CH28-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH28-04
      recall_question: RQ-CH28-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 28 — Entradas que Llegan Durante el Turno: Steering y Follow-up

> **Regla constitucional (P-10):** el arnés es dueño del estado de ejecución — no el modelo.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de
> saber cómo se llama el contrato de este capítulo. El detalle estructurado de esta sección vive
> en `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida.

**Resultado esperado.** Al terminar este capítulo podrás decidir, para cualquier mensaje que un
usuario envía mientras el turno de un agente todavía corre, en qué frontera exacta del turno debe
aplicarse (antes de la próxima llamada al modelo, o solo cuando el agente iba a terminar), y podrás
distinguir ese mensaje de una resolución humana, de una cancelación y de una autorización, que el
arnés ya asigna a dueños distintos.

**Esqueleto.** Este capítulo, el primero del Tramo 4 ("enriquecer el núcleo de agente único"),
recorre 19 secciones e introduce un único contrato de datos. No introduce componentes: amplía, sin
cambiar su ficha, lo que el componente del turno ya poseía.

**Preguntas guía** (respóndelas de memoria en la sección 21, sin volver a mirar atrás):

1. Si el usuario escribe una corrección mientras el agente está esperando el resultado de una
   herramienta, ¿debería esa corrección detener la herramienta que ya está corriendo, o esperar a
   un punto posterior del turno? ¿Cuál sería ese punto?
2. Si el modelo dice que ya terminó, pero el usuario dejó un mensaje pendiente "para cuando
   acabes", ¿quién decide que el turno en realidad no termina todavía: el modelo o el arnés?
3. Si llegan tres mensajes seguidos mientras el turno corre, ¿se entregan todos juntos o uno por
   vez? ¿Y quién decide eso: el mensaje, el usuario o una regla fija de la cola?
4. Si un mensaje que llega a mitad del turno dice "sí, aprobado", ¿alcanza para dar por resuelta
   una aprobación humana pendiente, o para cancelar la ejecución?

## 1. Arquitectura Actual (Current Architecture)

El libro llega a CH-28 con 22 componentes y 35 contratos, en dos tramos.

- **Tramo 1 (CH-01..CH-11):** el núcleo de agente único de Article III.
- **Tramo 3 (CH-14..CH-24):** los planos enterprise de Amendment v1.1.
- **Integraciones (CH-12/13 y CH-26/27):** las funciones que los cablean.

El turno ya tiene un dueño claro, `AgentLoop` (CMP-001, CH-01). Su función `runTurn` recibe dos señales que propone el modelo (`modelFinished`, `modelProposesToolCall`) y decide, de forma determinística, la transición de `AgentRunStatus` (C-013):
- a `COMPLETED`;
- a `WAITING_FOR_TOOL`;
- o a otro `WAITING_FOR_MODEL`.

Las funciones de integración de CH-12 (`runAgentTurnEndToEnd`) y CH-13 (`resumeTurnWithObservation`) encadenan el turno así:
1. continuación (`ExecutionController`);
2. contexto (`ContextEngine`);
3. modelo (`ModelGateway`);
4. `runTurn`;
5. checkpoint (`SessionManager`).

En todo ese recorrido, la única entrada del usuario que el arnés conoce es la que **inició** el turno. Tampoco existe todavía una **integración durable** que cablee de verdad los caminos alternativos de CH-13 (deuda que Amendment v1.2 y el Tramo 5 de este libro van a resolver).

## 2. El Problema (Problem)

Un usuario real no espera en silencio a que el agente termine. Escribe mientras el agente trabaja,
y lo hace por dos motivos distintos:

- **para corregir** ("no, el archivo es el de producción, no el de test");
- **para encargar algo después** ("cuando termines, resume lo que cambiaste").

Hoy el arnés no tiene dónde poner ese mensaje. Cada implementación lo resuelve a su manera: lo
descarta porque "el agente está ocupado", corta la herramienta que estaba corriendo para meter el
mensaje enseguida, o lo agrega al contexto en un punto cualquiera. Son tres comportamientos para la
misma situación, y ninguno está declarado.

Necesitamos que un mensaje que llega durante el turno tenga una **frontera declarada** donde se
aplica, y que la decisión de si el turno termina siga siendo del arnés, aunque el modelo diga "ya
terminé".

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Con lo que el libro tiene hasta CH-27:

- `runTurn` solo conoce las dos señales del modelo. Si el modelo propone `modelFinished = TRUE`, el
  turno termina **aunque** el usuario haya dejado un mensaje pendiente. De hecho, la decisión queda
  en manos de la señal del modelo, y eso contradice el espíritu de P-10.
- Ningún contrato representa "un mensaje que llegó durante el turno". `AgentMessage` (C-001) es un
  mensaje ya incorporado al historial, no uno que espera su frontera.
- Nada impide que una implementación **corte una tool en ejecución** para aplicar un mensaje nuevo.
  Eso viola INV-07: el `ToolResult` debe volver siempre al ciclo como observación explícita, y una
  tool cortada a la mitad no produce ninguna.
- La tentación de tratar un mensaje "sí, aprobado" como resolución de una aprobación pendiente, o
  "detente" como cancelación, no tiene nada que la contenga. Pero esas decisiones ya tienen dueño:
  `HumanInteractionService` (CH-06) para la resolución humana (INV-15), y `ExecutionController` /
  `OperationalController` para la cancelación (INV-10).

> **Regla editorial fundamental (recordatorio):** todo concepto atraviesa
> `Concept → Contract → Pseudocode → Interaction`, y ningún pseudocódigo usa una entidad no
> definida (**no magic entities**). Este capítulo aplica la misma disciplina al tiempo: ninguna
> entrada pendiente altera el turno fuera de una frontera declarada.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-10   The harness owns execution state—not the model.
           resolveCompletionWithPendingInput convierte el modelFinished del modelo en una
           propuesta: AgentLoop decide si el turno termina, y lo anula mientras quede una
           entrada pendiente.
    P-12   Events observe; hooks intervene.
           PENDING_INPUT_QUEUED y PENDING_INPUT_APPLIED observan; ninguna entrada pendiente
           interviene fuera de las dos fronteras declaradas.
    P-13   Authorization is deterministic and external to the LLM.
           Una PendingInput nunca es una autorización: su texto no cambia ninguna PolicyDecision.

Invariants preserved
    INV-07   El ToolResult vuelve al loop como observación explícita.
             El steering solo se aplica en BEFORE_MODEL_CALL, después de que las tools del paso
             ya devolvieron su resultado — nunca interrumpe una tool en ejecución.
    INV-08   El harness es propietario del execution state.
             La cola de entradas pendientes vive junto al AgentState del arnés, no en el modelo
             ni en la UI.
    INV-10   Todo AgentRun puede cancelarse.
             Preservado sin absorberlo: cancelar sigue siendo de ExecutionController /
             OperationalController; una PendingInput que diga "detente" no cancela nada.
    INV-15   Una acción que requiere aprobación no se ejecuta antes de una resolución válida.
             Una PendingInput no es una HumanInteractionResolution (CH-06).
    INV-18   Toda acción significativa produce un evento observable.
             Encolar y aplicar una entrada pendiente emiten AgentEvent.
    INV-19   Toda decisión crítica es trazable hasta su actor, contexto y policy.
             Cada evento lleva el traceId del ExecutionContext y el id de la entrada.

Component ownership changes
    Ninguno en registry/components.yaml. AgentLoop (CMP-001) ya posee literalmente "turn
    lifecycle" y "continuation" (Article III); decidir en qué frontera del turno se aplica una
    entrada pendiente es continuación del turno. runTurn (CH-01) no se modifica.

Lifecycle changes
    Ningún valor nuevo en AgentRunStatus (C-013). Un follow-up pendiente convierte un
    COMPLETED que runTurn habría producido en otro WAITING_FOR_MODEL — una transición que el
    lifecycle de CH-01 ya permitía.

Security implications
    Una entrada pendiente es un mensaje de rol USER, nunca una autorización, una resolución
    humana ni una cancelación (ver sección 15).

Observability implications
    Dos valores nuevos de AgentEventType: PENDING_INPUT_QUEUED y PENDING_INPUT_APPLIED.

Deterministic vs agentic boundary
    El modelo sigue proponiendo modelFinished; el arnés decide. La frontera de Article XII se
    refuerza: la decisión de terminar pasa a depender también de un estado que el modelo no
    controla (la cola).
```

## 5. Conceptos Nuevos (New Concepts)

- **Entrada pendiente**: un mensaje del usuario que llega **durante** un turno en curso y todavía no forma parte del contexto del modelo. Espera su frontera en una cola del arnés.
- **Steering**: una entrada pendiente de tipo corrección. Se aplica en la frontera **antes de la próxima llamada al modelo**, es decir, después de que las tools del paso ya devolvieron su resultado. Nunca interrumpe una tool en ejecución.
- **Follow-up**: una entrada pendiente de tipo "para después". Se aplica solo cuando el turno **iba a terminar**. Mientras quede un follow-up pendiente, el arnés no deja terminar el turno, aunque el modelo lo proponga.
- **Frontera del turno** (*turn boundary*): el punto exacto donde una entrada pendiente puede aplicarse. Hay solo dos: `BEFORE_MODEL_CALL` y `WOULD_COMPLETE`. Fuera de ellas, la cola no altera nada.
- **Modo de entrega**: la regla con que la cola entrega sus entradas en una frontera. Puede ser **una por vez** (`ONE_AT_A_TIME`) o **todas juntas** (`ALL`). Es una propiedad de la cola, no de cada mensaje, porque un mensaje no elige cómo se le entrega.
- **Prioridad del steering**: en la frontera `WOULD_COMPLETE`, una corrección pendiente se aplica antes que un follow-up. Una corrección que todavía no se aplicó cambia el trabajo; un encargo "para después" no.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato** (`registry/contracts.yaml`): `AgentMessage` (C-001), `AgentState` (C-003), `ExecutionContext` (C-004), `AgentEvent` (C-010), `HarnessError` (C-011);
- **identificadores primitivos:** `RunId`, `Timestamp`.

Cinco identificadores más se usan sin contrato `C-XXX` propio:

| Identificador | Rol en este capítulo |
|---|---|
| `PendingInputId` | identificador estable de una entrada pendiente (nuevo, mismo patrón que `EventId`) |
| `MessageId` | identificador de un `AgentMessage` (heredado de CH-00) |
| `MessageRole` | rol del mensaje; una entrada pendiente siempre es `USER` (heredado de CH-00) |
| `AgentEventType` | tipo de los eventos que emite este capítulo (se agregan `PENDING_INPUT_QUEUED` y `PENDING_INPUT_APPLIED`) |
| `ErrorCategory` | categoría de los errores de este capítulo (reutiliza `VALIDATION`, sin valores nuevos) |

### `PendingInputKind` — el tipo de entrada (embebido, sin contrato propio)

```pseudocode
ENUM PendingInputKind
    STEER
    FOLLOW_UP
END
```

### `PendingInputMode` — el modo de entrega de la cola (embebido)

```pseudocode
ENUM PendingInputMode
    ONE_AT_A_TIME
    ALL
END
```

### `PendingInput` — el contrato de este capítulo (C-036)

```pseudocode
STRUCT PendingInput
    id: PendingInputId
    runId: RunId
    kind: PendingInputKind
    message: AgentMessage
    receivedAt: Timestamp
END
```

`message` reutiliza `AgentMessage` (C-001) sin cambios: una entrada pendiente **es** un mensaje de
rol `USER` que todavía no entró al contexto. No se inventa un segundo formato de mensaje.

### `PendingInputQueue` — la cola del run (embebida)

```pseudocode
STRUCT PendingInputQueue
    runId: RunId
    steering: List<PendingInput>
    followUp: List<PendingInput>
    steeringMode: PendingInputMode
    followUpMode: PendingInputMode
END
```

Dos listas separadas en vez de una sola lista con un campo `kind`: así la prioridad del steering y
el modo de cada una se leen directamente de la estructura, sin filtrar.

### `TurnBoundary` — las dos fronteras del turno (embebido)

```pseudocode
ENUM TurnBoundary
    BEFORE_MODEL_CALL
    WOULD_COMPLETE
END
```

### `PendingInputSelection` — el resultado de aplicar la cola en una frontera (embebido)

```pseudocode
STRUCT PendingInputSelection
    boundary: TurnBoundary
    applied: List<PendingInput>
    messages: List<AgentMessage>
    remaining: PendingInputQueue
END
```

**Unchanged / Not yet introduced:**
- **Persistencia durable de la cola:** si el proceso muere, hoy la cola se pierde. Eso es de los pasos durables y las esperas durables (CH-32/CH-33).
- **Canales** que entregan estas entradas (CH-34).
- **Integración** que las aplica dentro de `resumeTurnWithObservation` (CH-36).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento. Introduce un contrato de datos,
registrado en `registry/contracts.yaml`:

```text
ID:                     C-036
Name:                   PendingInput
Version:                v1
Introduced In:          CH-28
Current Definition:     STRUCT PendingInput (ver seccion 6)
Used By:                [CMP-001]
Modified By:            []
Constitutional Impact:  [P-10, INV-08, INV-07]
```

`PendingInputKind`, `PendingInputMode`, `PendingInputQueue`, `TurnBoundary` y
`PendingInputSelection` quedan **embebidos**, sin contrato propio (mismo patrón que `ExecutionUsage`
en CH-07 o `ContextBlock` en CH-04): solo cruzan la frontera de `AgentLoop` como parte de sus
propias funciones.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo **no introduce componentes**. Amplía el comportamiento de `AgentLoop` (CMP-001) sin
cambiar su ficha, porque la decisión nueva ya cabe en su `owns` literal (Article III, sección
"AgentLoop"):

```text
COMPONENT: AgentLoop (CMP-001, CH-01 — ficha sin cambios)

Owns (Article III, cita literal) — lo que este capítulo usa:
    - turn lifecycle
    - continuation
    - completion

Decisión nueva, dentro de ese owns:
    "¿En qué frontera del turno se aplica una entrada pendiente, y cuáles se aplican en
     esa frontera según el modo de la cola?"

Does NOT own (se preserva, con énfasis en este capítulo):
    - la ejecución de una tool en curso (ToolRuntime, CH-02) — el steering nunca la corta
    - la resolución de una solicitud humana (HumanInteractionService, CH-06)
    - la cancelación de un run (ExecutionController, CH-07 / OperationalController, CH-18)
    - la autorización de una acción (PolicyEngine, CH-05)
```

Por qué no hace falta un componente nuevo (EVO-01, "keep the core small"): la cola no decide nada
que no sea continuación del turno. Un `PendingInputManager` separado tendría que preguntarle a
`AgentLoop` en cada frontera si el turno sigue, y duplicaría una decisión que ya tiene dueño.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
AgentLoop (ampliado en CH-28)
    consumes → AgentState, ExecutionContext, PendingInput (C-036), AgentMessage
    produces → PendingInputSelection (embebido), AgentEvent, HarnessError
    depends on (componentes) → ninguno nuevo
```

Como en el resto del libro, las llamadas entre componentes ocurren en funciones de integración, no
dentro de los componentes. Una integración futura (CH-36, Preview, no introducida en este capítulo) aplicará las entradas pendientes así:

| Punto de la integración | Qué función de este capítulo se invoca |
|---|---|
| después de `executeToolCall` (CH-02) y antes de `assembleContextSnapshot` (CH-04) | `selectPendingInputsAtBoundary(queue, BEFORE_MODEL_CALL)`: sus `messages` se agregan a los candidatos del contexto |
| justo antes de `runTurn` (CH-01) | `resolveCompletionWithPendingInput`: calcula el `modelFinished` efectivo |
| si el turno iba a terminar y hay follow-up | `selectPendingInputsAtBoundary(queue, WOULD_COMPLETE)` |

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
Usuario → [Canal — Preview, CH-34] → AgentLoop (cola) → ContextEngine / runTurn
```

**Vista 2 — Sequence**

```text
Usuario
   │ escribe durante el turno: "no, usa el archivo de producción"   (STEER)
   │ escribe durante el turno: "cuando termines, resume los cambios" (FOLLOW_UP)
   ▼
AgentLoop
   │ enqueuePendingInput(queue, state, input)   → PENDING_INPUT_QUEUED
   │
   │ [ToolRuntime termina la tool en curso — nunca se interrumpe (INV-07)]
   │
   │ frontera BEFORE_MODEL_CALL
   │ selectPendingInputsAtBoundary(queue, BEFORE_MODEL_CALL) → aplica el STEER
   │   → PENDING_INPUT_APPLIED; sus messages entran a los candidatos de ContextEngine
   ▼
ModelGateway (invocación del modelo con la corrección ya en contexto)
   │ el modelo propone modelFinished = TRUE
   ▼
AgentLoop
   │ resolveCompletionWithPendingInput(TRUE, queue) → FALSE (queda un FOLLOW_UP)
   │ runTurn(..., modelFinished = FALSE, ...) → WAITING_FOR_MODEL
   │ frontera WOULD_COMPLETE
   │ selectPendingInputsAtBoundary(queue, WOULD_COMPLETE) → aplica el FOLLOW_UP
   │   → PENDING_INPUT_APPLIED
   ▼
ModelGateway (otro turno: el modelo resume los cambios) → modelFinished = TRUE, cola vacía
   ▼
AgentLoop: resolveCompletionWithPendingInput(TRUE, cola vacía) → TRUE → runTurn → COMPLETED
```

**Vista 3 — Pseudocódigo**

Ver la sección 11: `enqueuePendingInput`, `takeByMode`, `selectPendingInputsAtBoundary` y
`resolveCompletionWithPendingInput`.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades definidas en la sección 6 o registradas desde capítulos anteriores.

```pseudocode
FUNCTION enqueuePendingInput(
    queue: PendingInputQueue,
    state: AgentState,
    execution: ExecutionContext,
    input: PendingInput
) -> PendingInputQueue

    IF state.status == COMPLETED
        OR state.status == FAILED
        OR state.status == CANCELLED
        OR state.status == EXPIRED

        THROW HarnessError(
            category = VALIDATION,
            code = "PENDING_INPUT_ON_TERMINAL_RUN",
            message = "Se intentó encolar una entrada pendiente sobre un run terminal",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    IF input.runId != queue.runId
        THROW HarnessError(
            category = VALIDATION,
            code = "PENDING_INPUT_RUN_MISMATCH",
            message = "La entrada pendiente pertenece a otro run que la cola",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    steering: List<PendingInput> = queue.steering
    followUp: List<PendingInput> = queue.followUp

    IF input.kind == STEER
        steering = append(steering, input)
    ELSE
        followUp = append(followUp, input)
    END

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = PENDING_INPUT_QUEUED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = state.agentId,
        traceId = execution.traceId,
        payload = input
    )

    RETURN PendingInputQueue(
        runId = queue.runId,
        steering = steering,
        followUp = followUp,
        steeringMode = queue.steeringMode,
        followUpMode = queue.followUpMode
    )
END
```

```pseudocode
FUNCTION takeByMode(
    inputs: List<PendingInput>,
    mode: PendingInputMode
) -> List<PendingInput>

    IF isEmpty(inputs)
        RETURN []
    END

    IF mode == ONE_AT_A_TIME
        RETURN [first(inputs)]
    END

    RETURN inputs
END
```

```pseudocode
FUNCTION selectPendingInputsAtBoundary(
    queue: PendingInputQueue,
    boundary: TurnBoundary,
    state: AgentState,
    execution: ExecutionContext
) -> PendingInputSelection

    applied: List<PendingInput> = []
    steering: List<PendingInput> = queue.steering
    followUp: List<PendingInput> = queue.followUp

    IF boundary == BEFORE_MODEL_CALL
        applied = takeByMode(steering, queue.steeringMode)
        steering = removeAll(steering, applied)
    ELSE IF NOT isEmpty(steering)
        applied = takeByMode(steering, queue.steeringMode)
        steering = removeAll(steering, applied)
    ELSE
        applied = takeByMode(followUp, queue.followUpMode)
        followUp = removeAll(followUp, applied)
    END

    messages: List<AgentMessage> = []
    FOR EACH pending IN applied
        messages = append(messages, pending.message)
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = PENDING_INPUT_APPLIED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = state.agentId,
            traceId = execution.traceId,
            payload = pending
        )
    END

    RETURN PendingInputSelection(
        boundary = boundary,
        applied = applied,
        messages = messages,
        remaining = PendingInputQueue(
            runId = queue.runId,
            steering = steering,
            followUp = followUp,
            steeringMode = queue.steeringMode,
            followUpMode = queue.followUpMode
        )
    )
END
```

```pseudocode
FUNCTION resolveCompletionWithPendingInput(
    modelFinished: Boolean,
    queue: PendingInputQueue
) -> Boolean

    IF NOT modelFinished
        RETURN FALSE
    END

    IF NOT isEmpty(queue.steering) OR NOT isEmpty(queue.followUp)
        RETURN FALSE
    END

    RETURN TRUE
END
```

`append`, `first`, `removeAll`, `isEmpty`, `newEventId` y `now` son utilidades primitivas sobre
listas y tiempo. No son entidades arquitectónicas y no requieren ficha ni registro.

Nótese lo que estas funciones **no** hacen:
- ninguna corta una tool en ejecución;
- ninguna modifica `runTurn`;
- ninguna resuelve una `HumanInteractionRequest`;
- ninguna cancela un run.

`resolveCompletionWithPendingInput` recibe la señal del modelo y devuelve la **decisión del arnés**, que es exactamente lo que P-10 exige.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no agrega valores a `AgentRunStatus` (C-013). Cambia **cuándo** se produce una transición que ya existía:

```text
WAITING_FOR_MODEL
   → COMPLETED          (runTurn: modelFinished efectivo = TRUE — cola vacía)
   → WAITING_FOR_MODEL  (runTurn: el modelo propuso terminar, pero quedaba una entrada
                         pendiente; resolveCompletionWithPendingInput devolvió FALSE)
   → WAITING_FOR_TOOL   (sin cambios respecto a CH-01)
```

La cola tiene su propia evolución, fuera de `AgentRunStatus`:

```text
entrada recibida → encolada (PENDING_INPUT_QUEUED)
encolada → aplicada en BEFORE_MODEL_CALL (STEER) o en WOULD_COMPLETE (FOLLOW_UP,
           o STEER si todavía quedaba) (PENDING_INPUT_APPLIED)
```

Una entrada solo se aplica **una vez**: `selectPendingInputsAtBoundary` la quita de la cola en el
mismo paso en que la entrega.

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` clasifica los dos fallos nuevos de este capítulo en un `HarnessError` explícito:

```text
VALIDATION
    enqueuePendingInput sobre un run terminal (COMPLETED/FAILED/CANCELLED/EXPIRED)
    → recoverable: FALSE, retryable: FALSE
    → código: PENDING_INPUT_ON_TERMINAL_RUN

VALIDATION
    enqueuePendingInput con una entrada de otro run (input.runId != queue.runId)
    → recoverable: FALSE, retryable: FALSE
    → código: PENDING_INPUT_RUN_MISMATCH
```

Lo que este capítulo **deliberadamente no clasifica**: una entrada que llega a un run terminal no se
"reabre". El canal que la recibió deberá activar un run nuevo (P-16, `ActivationRequest`). Eso lo resuelve CH-34, con las direcciones de continuación.

## 14. Eventos Producidos (Events Produced)

Dos valores nuevos de `AgentEventType`:

```text
PENDING_INPUT_QUEUED    — AgentLoop encoló una entrada que llegó durante el turno
                          (enqueuePendingInput, seccion 11)
PENDING_INPUT_APPLIED   — AgentLoop aplicó una entrada pendiente en una frontera del turno
                          (selectPendingInputsAtBoundary, seccion 11; uno por entrada aplicada)
```

Los dos usan el envelope común `AgentEvent` (C-010) sin modificarlo, y llevan la `PendingInput`
como `payload`. `TURN_CONTINUED` y `RUN_COMPLETED` siguen siendo emitidos por `runTurn` (CH-01), que no cambia.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **Una entrada pendiente no es autorización (P-13).** Su texto nunca cambia una `PolicyDecision`.
  Si el modelo, después de leer un steering, propone una tool call, esa tool call pasa por
  `CapabilityRegistry` y `PolicyEngine` como cualquier otra.
- **Una entrada pendiente no es una resolución humana (INV-15).** "Sí, aprobado" en un steering no
  resuelve una `HumanInteractionRequest`. La resolución sigue exigiendo
  `resolveHumanInteractionRequest` (CH-06), con su vínculo explícito a la solicitud que resuelve.
- **Una entrada pendiente no es una cancelación (INV-10).** "Detente" en un steering es un mensaje
  para el modelo, no un `ControlDirective`. Cancelar sigue siendo de `ExecutionController` (CH-07)
  y de `OperationalController` (CH-18), que no dependen de la cooperación del modelo (P-30).
- **Un mensaje no elige su modo de entrega.** El modo vive en la cola, fijado por el arnés. Así un
  mensaje no puede forzar que una ráfaga entera entre de golpe al contexto.
- **Quién puede encolar** en un run concreto (identidad del remitente) no se resuelve aquí. Lo cubren CH-31 (identidad del llamante) y CH-34 (canales y direcciones).

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo:

```text
TEST SteeringIsAppliedOnlyAtBeforeModelCallBoundary
TEST SteeringNeverInterruptsAToolAlreadyExecuting
TEST FollowUpPreventsCompletionWhileAnyPendingInputRemains
TEST ResolveCompletionReturnsTrueOnlyWhenModelFinishedAndQueueIsEmpty
TEST SteeringHasPriorityOverFollowUpAtWouldCompleteBoundary
TEST OneAtATimeModeAppliesExactlyOnePendingInputPerBoundary
TEST AllModeAppliesEveryPendingInputOfThatKindAtOnce
TEST AnAppliedPendingInputIsRemovedFromTheQueue
TEST EnqueueOnTerminalRunThrowsPendingInputOnTerminalRun
TEST EnqueueFromAnotherRunThrowsPendingInputRunMismatch
TEST PendingInputNeverResolvesAHumanInteractionRequest
TEST PendingInputNeverCancelsAnAgentRun
TEST RunTurnIsNotModifiedByThisChapter
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.2 en curso, después de CH-28)

Constitution
 ├── Article I..XII, Amendment v1.1 (P-16..P-30), Amendment v1.2 (P-31..P-39)
 └── sin cambios en este capítulo

Contracts (registry/contracts.yaml) — 36
 ├── C-001 .. C-035   (CH-00 .. CH-24, sin cambios)
 └── C-036 PendingInput   (CH-28, nuevo)

Components (registry/components.yaml) — 22, sin cambios
 └── CMP-001 AgentLoop    (CH-01 — decisión nueva dentro de su owns: fronteras de entrada pendiente)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **Durabilidad de la cola.** Si el proceso muere, las entradas pendientes se pierden. Hacerlas durables pertenece a los pasos durables (CH-32) y a las esperas durables (CH-33).
- **Cablearlo en la integración.** Ninguna función de integración existente (CH-12, CH-13, CH-26, CH-27) llama todavía a estas funciones. El primer cableado real será `runDurableGovernedTurn` (CH-36).
- **Interrumpir la generación del modelo** antes de que emita su respuesta, como hacen algunos arneses de producción. Este capítulo solo aplica el steering en fronteras entre pasos. Abortar una llamada al modelo en curso exige que la llamada sea recuperable, y eso es de CH-32.
- **Canales** que entregan estas entradas (HTTP, WebSocket, chat) y la identidad de quien las envía: CH-34 y CH-31.
- **Límite de tamaño de la cola.** Si muchas entradas pendientes empujan el contexto más allá del presupuesto, sigue siendo tarea de `ContextEngine` (CH-04) y de la compactación de CH-29.

## 19. Siguiente Incremento (Next Increment)

Con steering y follow-up, una conversación puede crecer mucho dentro de un mismo run, porque cada
corrección y cada encargo agregan mensajes. El problema natural del siguiente capítulo es **cómo
compactar ese historial sin perder el hilo**:
- resúmenes estructurados en lugar de truncar;
- un punto de corte que nunca separe una tool call de su resultado (INV-07);
- sesiones que se ramifican cuando el usuario quiere explorar una alternativa sin perder la original.

Ese capítulo será CH-29 ("Compactar sin Perder el Hilo: Resúmenes Estructurados y Sesiones en Árbol"). `next_chapter` queda en `null` en el frontmatter porque CH-29 todavía no existe como archivo.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo). No introduce
> contenido nuevo: reetiqueta secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2): un usuario escribe mientras el agente trabaja, y la implementación no
   sabe qué hacer con el mensaje. Lo descarta, corta la herramienta en curso o lo mete en un punto
   arbitrario del contexto.
2. **Patrones que se repiten** (= §3): sin fronteras declaradas dentro del turno, cada mensaje nuevo
   lo resuelve el código que lo recibió. La continuación del turno se fragmenta entre actores que no
   la poseen.
3. **Estructuras / reglas / incentivos** (= §8, §15): `PendingInput` (C-036) y dos fronteras
   explícitas, `BEFORE_MODEL_CALL` y `WOULD_COMPLETE`, dentro del `owns` ya existente de
   `AgentLoop`. Una entrada pendiente no es resolución humana, ni cancelación, ni autorización.
4. **Modelos mentales** (= §4): P-10. El `modelFinished` del modelo es una propuesta, y el arnés
   decide.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada mensaje descartado "porque el agente estaba ocupado" obliga
  al usuario a repetirlo, y eso produce más mensajes durante turnos en curso. Declarar la cola corta
  la espiral: ningún mensaje se pierde, solo espera su frontera.
- **Bucle de equilibrio (estabiliza):** el modo de la cola (`ONE_AT_A_TIME` / `ALL`) impide que una
  ráfaga entre entera de golpe cuando el diseño quiere una corrección por turno.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `PendingInput` (C-036) solo pueda aplicarse en
dos fronteras declaradas del turno, y que en `WOULD_COMPLETE` la decisión final sea de `AgentLoop` y
no del modelo. Si esa frontera no se fija aquí, cada canal futuro (CH-34) reinventaría cuándo
"interrumpir" al agente.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado vive en
> `retrieval_set` (frontmatter). Aquí se presenta en prosa.

### Recordar

Vuelve a la sección 0 y responde de memoria:

1. ¿En qué frontera del turno se aplica una `PendingInput` con `kind = STEER`, y por qué nunca
   interrumpe una tool que `ToolRuntime` ya está ejecutando (INV-07)? *(cierra la pregunta guía 1)*
2. ¿Qué hace `resolveCompletionWithPendingInput` cuando el modelo propone `modelFinished = TRUE`
   pero la cola todavía tiene un follow-up pendiente, y qué valor le llega entonces a `runTurn`?
   *(cierra la pregunta guía 2)*
3. ¿Dónde vive el modo de entrega (`ONE_AT_A_TIME` / `ALL`), en cada `PendingInput` o en la cola, y
   qué devuelve `takeByMode` en cada caso? *(cierra la pregunta guía 3)*
4. ¿Por qué una `PendingInput` nunca puede resolver una `HumanInteractionRequest` pendiente ni
   cancelar un `AgentRun`, aunque su texto diga "aprobado" o "detente"? *(cierra la pregunta guía 4)*

### Explicar

1. La decisión "¿en qué frontera del turno se aplica un mensaje pendiente?" pertenece a `AgentLoop`
   porque es continuación del turno. Explica, como si hablaras con alguien sin contexto técnico, por
   qué `AgentLoop` NO posee la ejecución de la tool que ya está corriendo. ¿Qué se rompería si un
   steering pudiera cortarla a la mitad?
2. Usando P-10 y P-13, explica por qué el texto de una `PendingInput`, aunque diga "aprobado", no es
   una autorización ni una resolución humana. ¿Qué componente ya introducido posee esa decisión, y
   con qué contrato la representa?

### Conectar

1. Una `PendingInput` con `kind = STEER` y una `HumanInteractionResolution` (CH-06) pueden llegar por
   el mismo canal y a la misma sesión. ¿Qué campo del contrato de CH-06 vincula su resolución a una
   solicitud concreta, y por qué una `PendingInput` no tiene (ni necesita) ese vínculo?

### Espaciar

Las dos tarjetas de repaso de este capítulo (sobre `PendingInput` y sobre sus dos fronteras) entran
hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7 y al día 21. Ver el apéndice de tarjetas al final del libro.

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una (Alta / Media /
Baja). Si calificaste "Alta" y te equivocaste, ese es el punto ciego que este método existe para
revelar.
