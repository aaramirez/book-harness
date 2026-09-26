---
id: CH-32
title: "Pasos Durables y la Recuperación a Mitad de Turno"
starting_version: "0.1"
ending_version: "0.2"
introduces_components: [CMP-023]
introduces_contracts: [C-042, C-043]
modifies_contracts: []
constitutional_articles: [P-23, P-24, P-32, INV-07, INV-11, INV-13, INV-E16, INV-E17]
previous_chapter: CH-31
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH32
    text: |
      Al terminar este capítulo podrás descomponer un turno en pasos durables, explicar por qué cada
      hecho de un paso se escribe antes del efecto siguiente, y decidir, para cualquier paso que
      encuentres en el registro después de una caída del proceso, qué hace la recuperación con él
      sin repetir nunca algo que ya quedó comprometido.
  skeleton:
    id: SK-CH32
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
    components_to_be_introduced: [CMP-023]
    contracts_to_be_introduced: [C-042, C-043]
  guiding_questions:
    - id: GQ-CH32-01
      text: |
        Si el proceso del agente se cae en medio de un turno largo, ¿qué debería quedar guardado para
        poder continuar sin empezar el turno desde cero?
      answered_by: RQ-CH32-01
    - id: GQ-CH32-02
      text: |
        ¿Por qué importa si el registro de "voy a ejecutar esta herramienta" se escribe antes o
        después de ejecutarla?
      answered_by: RQ-CH32-02
    - id: GQ-CH32-03
      text: |
        Si al recuperar encuentras una llamada al modelo que se cortó a la mitad, pero ya tenías
        parte de la respuesta guardada, ¿vale la pena volver a llamar al modelo?
      answered_by: RQ-CH32-03
    - id: GQ-CH32-04
      text: |
        Si una herramienta que envía un correo quedó a medias cuando el proceso se cayó, ¿quién
        debería decidir si se vuelve a enviar: el registro de pasos, la herramienta o alguien más?
      answered_by: RQ-CH32-04
  systems_lens:
    iceberg_visible_fact: |
      Cuando el proceso se cae a mitad de un turno, el arnés solo sabe cómo estaba la sesión en el
      último checkpoint: todo lo que pasó dentro del turno — la respuesta del modelo, la tool call
      que se estaba ejecutando — se pierde con la memoria del proceso (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que P-23 e INV-13 exigen reconstruir un run desde estado
      persistido, pero la única unidad persistida es el checkpoint por fase de SessionManager. La
      recuperación solo puede elegir entre repetir el turno entero (y duplicar efectos) o darlo por
      perdido (ver sección 3).
    iceberg_structures: |
      Este capítulo introduce ExecutionJournal (CMP-023), StepRecord (C-042) y RecoveryDecision
      (C-043): un registro por paso escrito antes de cada efecto (write-ahead) y una decisión de
      recuperación por paso que entrega los efectos pendientes a IdempotencyGuard (ver sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-32 (el paso es la unidad de durabilidad), INV-E16 (un paso
      comprometido nunca se re-ejecuta) e INV-E17 (un efecto desconocido se repite solo si su
      capability es SAFE) (ver sección 4).
    reinforcing_loop: |
      Sin registro por paso, cada caída obliga a repetir turnos completos; cada repetición gasta
      presupuesto y arriesga duplicar efectos, y los turnos largos — los que más se caen — son los
      que más se repiten. El journal corta la espiral: se repite a lo sumo un paso.
    balancing_loop: |
      INV-E16 es el mecanismo de equilibrio: por mucho que se recupere un run, lo comprometido se
      reproduce desde el registro y nunca vuelve a producir efectos.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es write-ahead: registrar la tool call en el
      StepRecord (C-042) antes de ejecutarla. Es lo que permite a decideStepRecovery distinguir
      "ningún efecto empezó" de "el efecto pudo haber empezado".
  recall_questions:
    - id: RQ-CH32-01
      text: |
        ¿Qué campos de un StepRecord se escriben durante un paso, en qué orden, y qué exige
        commitStep antes de marcarlo COMMITTED?
    - id: RQ-CH32-02
      text: |
        Si un StepRecord STARTED tiene modelResponse con una tool call propuesta pero toolCall =
        NULL, ¿qué acción decide decideStepRecovery, y cuál decide si toolCall existe pero
        toolResult = NULL?
    - id: RQ-CH32-03
      text: |
        ¿Cuándo decide decideStepRecovery CLOSE_WITH_PARTIAL y cuándo REEXECUTE_MODEL_CALL, y por
        qué repetir la llamada al modelo no viola P-24?
    - id: RQ-CH32-04
      text: |
        ¿Qué hace la integración con una RecoveryDecision RESOLVE_PENDING_TOOL, qué componente
        decide si el efecto se repite, y con qué valor de executionStillInFlight lo invoca?
  explain_prompts:
    - id: EP-CH32-01
      text: |
        ExecutionJournal y SessionManager guardan estado durable de un run. Explica, como si
        hablaras con alguien sin contexto técnico, por qué el checkpoint de sesión no sirve como
        unidad de recuperación dentro de un turno, y qué decide ExecutionJournal que SessionManager
        no decide.
      target_entity: CMP-023
    - id: EP-CH32-02
      text: |
        Explica por qué un StepRecord registra la tool call antes de ejecutarla, y qué error de
        recuperación aparecería si se registrara solo al terminar.
      target_entity: C-042
  interleaved_questions:
    - id: IQ-CH32-01
      text: |
        En CH-30, decideUnknownOutcome recibía executionStillInFlight como una señal asumida. Con
        ExecutionJournal, ¿de dónde sale esa señal durante una recuperación, y por qué
        ExecutionJournal no aplica él mismo la ReplayPolicy (C-039) de la capability?
      current_chapter_entities: [C-042, C-043, CMP-023]
      prior_chapter_entities: [C-039, CMP-015]
      prior_chapter: CH-30
  flashcards:
    - id: FC-CH32-01
      front: |
        ¿Qué es un StepRecord (C-042) y qué es un paso?
      back: |
        El registro durable de un paso: una llamada al modelo y la tool call que su respuesta
        propuso. Guarda status (STARTED / COMMITTED), salida parcial, respuesta, tool call (escrita
        antes de ejecutarse) y resultado.
      source_entity: C-042
      chapter_introduced_in: CH-32
      review_stage: DAY_1
    - id: FC-CH32-02
      front: |
        ¿Qué dice INV-E16 y qué acción de RecoveryDecision (C-043) lo materializa?
      back: |
        Un paso comprometido nunca se re-ejecuta durante la recuperación: todo paso COMMITTED recibe
        REPLAY_RECORDED y se reproduce desde el registro.
      source_entity: C-043
      chapter_introduced_in: CH-32
      review_stage: DAY_1
    - id: FC-CH32-03
      front: |
        ¿Qué posee ExecutionJournal (CMP-023) y qué no?
      back: |
        Posee registrar cada paso antes del efecto siguiente, comprometerlo solo con su resultado
        persistido y decidir la recuperación por paso. No posee decidir si un efecto desconocido se
        repite (IdempotencyGuard, INV-E17), la historia de sesión (SessionManager) ni ejecutar tools
        o llamar al modelo.
      source_entity: CMP-023
      chapter_introduced_in: CH-32
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH32-01
      recall_question: RQ-CH32-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH32-02
      recall_question: RQ-CH32-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH32-03
      recall_question: RQ-CH32-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH32-04
      recall_question: RQ-CH32-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 32 — Pasos Durables y la Recuperación a Mitad de Turno

> **Regla constitucional (P-32):** el paso es la unidad de durabilidad y de recuperación.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás descomponer un turno en pasos durables y
explicar por qué cada hecho de un paso se escribe antes del efecto siguiente. También podrás decidir,
para cualquier paso que encuentres en el registro después de una caída del proceso, qué hace la
recuperación con él, sin repetir nunca algo que ya quedó comprometido.

**Esqueleto.** Quinto capítulo del Tramo 4 y primer componente nuevo de la versión 0.2:
`ExecutionJournal`. Introduce dos contratos y no modifica ninguno.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si el proceso del agente se cae en medio de un turno largo, ¿qué debería quedar guardado para
   poder continuar sin empezar el turno desde cero?
2. ¿Por qué importa si el registro de "voy a ejecutar esta herramienta" se escribe antes o después
   de ejecutarla?
3. Si al recuperar encuentras una llamada al modelo que se cortó a la mitad, pero ya tenías parte de
   la respuesta guardada, ¿vale la pena volver a llamar al modelo?
4. Si una herramienta que envía un correo quedó a medias cuando el proceso se cayó, ¿quién debería
   decidir si se vuelve a enviar: el registro de pasos, la herramienta o alguien más?

## 1. Arquitectura Actual (Current Architecture)

- **`SessionManager` (CMP-010, CH-10)** guarda un `SessionCheckpoint` con el `AgentState` al final de
  cada fase, y CH-29 le agregó la navegación entre checkpoints. Es la **historia** de la sesión.
- **`IdempotencyGuard` (CMP-015, CH-17 y CH-30)** sabe si un efecto con una clave ya se ejecutó
  (`PENDING` / `COMPLETED`) y, desde CH-30, qué hacer si su resultado se desconoce, según la
  `ReplayPolicy` (C-039) de la capability. Pero `decideUnknownOutcome` recibe
  `executionStillInFlight` como una **señal asumida**: nadie la produce todavía.
- **`ModelResponse` (C-007, CH-03)** trae a lo sumo una `proposedToolCall`, que la integración
  (CH-12/CH-13) gobierna y ejecuta con `ToolRuntime` (CMP-002).
- Las funciones de integración de CH-12, CH-13, CH-26 y CH-27 corren el turno de principio a fin en
  un solo proceso.

## 2. El Problema (Problem)

Un turno real tiene varias llamadas al modelo y varias herramientas, y puede durar minutos. Si el
proceso se cae a la mitad:
- lo único guardado es el último checkpoint de sesión, del final de la fase anterior;
- la respuesta del modelo que ya había llegado se pierde, y hay que pagarla de nuevo;
- no se sabe si la herramienta que se estaba ejecutando (un pago, un correo) llegó a ejecutarse.

La recuperación solo tiene dos opciones, y las dos son malas:
- **repetir el turno entero**, que duplica efectos y gasta presupuesto;
- **darlo por perdido**, que viola P-23.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **El checkpoint es por fase, no por paso.** `SessionManager` guarda la historia de la sesión, no el
  progreso dentro de un turno. Usarlo como unidad de recuperación obliga a repetir todo lo posterior.
- **Nadie registra la tool call antes de ejecutarla.** Sin ese registro, después de una caída es
  imposible distinguir "la herramienta nunca empezó" de "empezó y no sabemos cómo terminó".
- **`IdempotencyGuard` decide sobre un efecto, no sobre un turno.** Sabe qué hacer con un
  `IdempotencyRecord` `PENDING` huérfano, pero no sabe **qué paso** quedó interrumpido ni si el resto
  del turno ya estaba comprometido.
- **Ningún componente posee la decisión** "¿este paso ya se comprometió y qué hago con él?". No es de
  `SessionManager` (historia), ni de `IdempotencyGuard` (efectos por clave), ni de
  `ExecutionController` (presupuesto). Por eso este capítulo introduce un componente (EVO-01).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-23   Durable execution is a core runtime property.
           El journal, no la memoria del proceso, es la fuente de verdad del progreso del turno.
    P-24   Side effects require idempotency semantics.
           Repetir una llamada al modelo no es un efecto visible fuera del arnés; los efectos
           de las capabilities siguen gobernados por IdempotencyGuard.

Principles introduced (Amendment v1.2, ya ratificado)
    P-32   A step is the unit of durability and recovery.
           ExecutionJournal materializa el paso: StepRecord, commitStep y decideStepRecovery.

Invariants preserved
    INV-07   Todo ToolResult vuelve al ciclo como observación explícita.
             Un resultado recuperado del journal vuelve igual que uno recién producido.
    INV-11   Side effects críticos soportan idempotencia.
             RESOLVE_PENDING_TOOL entrega el efecto pendiente a IdempotencyGuard.
    INV-13   Una ejecución durable debe poder reconstruirse desde estado persistido suficiente.
             "Suficiente", a nivel de paso: respuesta, tool call escrita antes y resultado.
    INV-E16  (Amendment v1.2) A committed step is never re-executed during recovery.
             Todo paso COMMITTED recibe REPLAY_RECORDED.
    INV-E17  (Amendment v1.2) Un efecto desconocido se repite solo si su capability es SAFE.
             No lo decide ExecutionJournal: lo sigue decidiendo IdempotencyGuard (CH-30).

Component ownership changes
    Nuevo: ExecutionJournal (CMP-023). Ningún componente existente pierde decisiones.

Contract changes
    Nuevos: C-042 StepRecord, C-043 RecoveryDecision. Ninguno modificado.

Security implications
    Nunca se repite un efecto que pudo haber empezado sin pasar por la ReplayPolicy de su
    capability (ver sección 15).

Observability implications
    Nuevos AgentEventType: STEP_COMMITTED y STEP_RECOVERY_DECIDED.

Deterministic vs agentic boundary
    Todo el journal es determinístico. El modelo no ve el journal ni decide la recuperación.
```

## 5. Conceptos Nuevos (New Concepts)

- **Paso** (*step*): una llamada al modelo y la tool call que su respuesta propuso. Un turno tiene
  varios pasos. En este libro un paso tiene **a lo sumo una** tool call, porque `ModelResponse`
  (C-007) propone una sola.
- **Escribir antes del efecto** (*write-ahead*): cada hecho del paso se guarda en el journal antes
  del efecto siguiente. La tool call se registra **antes** de que `ToolRuntime` la ejecute. Así el
  registro distingue dos situaciones que sin él son idénticas:
  - respuesta sin tool call registrada: **ningún efecto empezó**;
  - tool call sin resultado: **el efecto pudo haber empezado**.
- **Paso comprometido** (*committed*): un paso cuya respuesta y cuyo resultado ya están persistidos.
  Nunca se vuelve a ejecutar (INV-E16).
- **Salida parcial** (aporte de pi): lo que ya se recibió de una llamada al modelo que se cortó. Si
  está guardada, la recuperación cierra la llamada con esa salida en vez de volver a pagar al
  proveedor.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `ModelResponse` (C-007), `ToolCall` (C-008), `ToolResult` (C-009),
  `ExecutionContext` (C-004), `AgentEvent` (C-010), `HarnessError` (C-011);
- **primitivos:** `RunId`, `ToolCallId`, `AgentId`, `Timestamp`.

| Identificador | Rol en este capítulo |
|---|---|
| `StepId` | identificador nuevo de un paso, único dentro del journal |
| `AgentEventType` | se agregan `STEP_COMMITTED` y `STEP_RECOVERY_DECIDED` |
| `ErrorCategory` | reutiliza `PERSISTENCE`, sin valores nuevos |

### `StepStatus` — el estado de un paso (embebido)

```pseudocode
ENUM StepStatus
    STARTED
    COMMITTED
END
```

### `StepRecord` — el registro de un paso (C-042)

```pseudocode
STRUCT StepRecord
    stepId: StepId
    runId: RunId
    turn: Integer
    index: Integer
    status: StepStatus
    partialOutput: Optional<Value>
    modelResponse: Optional<ModelResponse>
    toolCall: Optional<ToolCall>
    toolResult: Optional<ToolResult>
    startedAt: Timestamp
    committedAt: Optional<Timestamp>
END
```

`turn` e `index` ubican el paso: el tercer paso del segundo turno tiene `turn = 2` e `index = 3`.

### `RecoveryAction` — qué hace la recuperación con un paso (embebido)

```pseudocode
ENUM RecoveryAction
    REPLAY_RECORDED
    COMMIT_RECORDED
    CLOSE_WITH_PARTIAL
    REEXECUTE_MODEL_CALL
    RESUME_FROM_RESPONSE
    RESOLVE_PENDING_TOOL
END
```

| Acción | Cuándo | Qué hace la integración |
|---|---|---|
| `REPLAY_RECORDED` | el paso está `COMMITTED` | reproduce respuesta y resultado desde el registro (INV-E16) |
| `COMMIT_RECORDED` | todo el resultado ya está en el registro, falta marcarlo | compromete el paso sin ejecutar nada |
| `CLOSE_WITH_PARTIAL` | la llamada al modelo se cortó y hay salida parcial | cierra la llamada con esa salida, sin volver al proveedor |
| `REEXECUTE_MODEL_CALL` | la llamada al modelo se cortó sin salida parcial | repite la llamada al modelo |
| `RESUME_FROM_RESPONSE` | hay respuesta con tool call propuesta, pero ninguna tool call registrada | vuelve a gobernar la propuesta (resolución, política, ejecución): ningún efecto empezó |
| `RESOLVE_PENDING_TOOL` | hay tool call registrada sin resultado | entrega la tool call a `IdempotencyGuard.decideUnknownOutcome` (CH-30) |

### `RecoveryDecision` — la decisión, trazable (C-043)

```pseudocode
STRUCT RecoveryDecision
    runId: RunId
    stepId: StepId
    action: RecoveryAction
    pendingToolCall: Optional<ToolCallId>
    decidedAt: Timestamp
END
```

`pendingToolCall` solo tiene valor con `RESOLVE_PENDING_TOOL`.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

```text
ID:                     C-042
Name:                   StepRecord
Version:                v1
Introduced In:          CH-32
Used By:                [CMP-023]
Constitutional Impact:  [P-23, P-32, INV-13, INV-E16]
```

```text
ID:                     C-043
Name:                   RecoveryDecision
Version:                v1
Introduced In:          CH-32
Used By:                [CMP-023]
Constitutional Impact:  [P-32, INV-13, INV-E16, INV-E17, INV-19]
```

`StepStatus` y `RecoveryAction` quedan embebidos. `StepId` es un identificador primitivo nuevo.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el primer componente de la versión 0.2:

```pseudocode
COMPONENT ExecutionJournal
    consumes: ExecutionContext, ModelResponse, ToolCall, ToolResult
    produces: StepRecord, RecoveryDecision, AgentEvent, HarnessError
END
```

```text
COMPONENT: ExecutionJournal (CMP-023)

Responsibility:
    Registrar, paso por paso, el progreso durable de un turno, escribiendo cada hecho antes del
    efecto siguiente; declarar un paso COMMITTED solo cuando todo su resultado está persistido; y
    decidir, al recuperar un run interrumpido, qué hacer con cada paso del journal.

Owns (Amendment v1.2 y Article II, citas literales):
    - "A turn MUST be decomposed into steps … recovery MUST reason per step, not per turn" (P-32)
    - "Process memory MUST NOT be the source of truth for durable runs" (P-23)
    - "Una ejecución durable debe poder reconstruirse desde estado persistido suficiente" (INV-13),
      decidiendo qué es "suficiente" a nivel de paso
    - declarar un paso COMMITTED solo con su respuesta y su resultado persistidos, y rechazar
      (fail-closed) cualquier escritura sobre un paso ya COMMITTED
    - "A committed step is never re-executed during recovery" (INV-E16), decidiendo por paso la
      RecoveryAction

Does NOT own:
    - decidir si un efecto cuyo resultado se desconoce se repite (IdempotencyGuard, CMP-015,
      CH-17/CH-30). Es la frontera más importante del capítulo: ExecutionJournal detecta QUÉ paso
      quedó con un efecto pendiente; IdempotencyGuard decide SI ese efecto se repite (INV-E17).
    - la historia y los checkpoints de la sesión (SessionManager, CMP-010, CH-10)
    - si el run puede seguir contra su presupuesto (ExecutionController, CMP-007, CH-07)
    - ejecutar la tool call (ToolRuntime, CMP-002) o invocar al modelo (ModelGateway, CMP-003)
    - el mecanismo físico de escritura durable y atómica (infraestructura de borde, Preview)
```

**Nota sobre el plan maestro.** La ficha original ponía `REEXECUTE / REPORT_OUTCOME_UNKNOWN` entre las
decisiones de `ExecutionJournal`. Desde CH-30 esa decisión ya es de `IdempotencyGuard`
(`decideUnknownOutcome`). Duplicarla violaría Article IV, así que `ExecutionJournal` la **delega**
con `RESOLVE_PENDING_TOOL`.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
ExecutionJournal
    consumes → ExecutionContext, ModelResponse, ToolCall, ToolResult
    produces → StepRecord, RecoveryDecision, AgentEvent, HarnessError
    depends on (componentes) → (ninguno)
```

`ExecutionJournal` no llama a ningún componente. La integración (CH-36, `runDurableGovernedTurn`) lo
envuelve alrededor del turno:

| Momento del turno | Llamada al journal |
|---|---|
| antes de invocar a `ModelGateway` | `beginStep` |
| mientras llega la respuesta | `recordPartialOutput` |
| al recibir la respuesta | `recordModelResponse` |
| después de gobernar la propuesta y **antes** de `ToolRuntime` | `recordToolCallBeforeExecution` |
| al recibir el `ToolResult` | `recordToolResult` |
| cuando la escritura durable confirma | `commitStep` |
| al arrancar un proceso con runs interrumpidos | `recoverRun` |

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
Integración → ExecutionJournal (write-ahead) → ModelGateway / ToolRuntime
Recuperación → ExecutionJournal.recoverRun → (RESOLVE_PENDING_TOOL) → IdempotencyGuard
```

**Vista 2 — Sequence: un paso normal**

```text
Integración
   │ beginStep(runId, turn, index, previous)             → StepRecord STARTED
   │ ModelGateway … recordPartialOutput(…)               → partialOutput
   │ recordModelResponse(record, response)               → modelResponse
   │ (resolución y política de la propuesta, CH-08/CH-05)
   │ recordToolCallBeforeExecution(record, toolCall)     → toolCall   ← antes del efecto
   │ ToolRuntime ejecuta
   │ recordToolResult(record, result)                    → toolResult
   │ commitStep(record, resultPersisted = TRUE, …)       → COMMITTED + STEP_COMMITTED
```

**Vista 2b — Sequence: recuperación tras una caída**

```text
Proceso nuevo
   │ recoverRun(journal, execution, agentId)
   │   paso 1 COMMITTED                       → REPLAY_RECORDED
   │   paso 2 COMMITTED                       → REPLAY_RECORDED
   │   paso 3 STARTED, toolCall sin resultado → RESOLVE_PENDING_TOOL
   ▼
IdempotencyGuard.decideUnknownOutcome(…, executionStillInFlight = FALSE, …)   (CH-30)
   │   SAFE  → REEXECUTE
   │   NEVER → REPORT_UNKNOWN (observación explícita, INV-07)
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

```pseudocode
FUNCTION beginStep(
    runId: RunId,
    turn: Integer,
    index: Integer,
    previous: Optional<StepRecord>
) -> StepRecord

    IF previous != NULL AND previous.status != COMMITTED
        THROW HarnessError(
            category = PERSISTENCE,
            code = "PREVIOUS_STEP_NOT_COMMITTED",
            message = "No se puede abrir un paso nuevo mientras el anterior no esté comprometido",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN StepRecord(
        stepId = newStepId(),
        runId = runId,
        turn = turn,
        index = index,
        status = STARTED,
        partialOutput = NULL,
        modelResponse = NULL,
        toolCall = NULL,
        toolResult = NULL,
        startedAt = now(),
        committedAt = NULL
    )
END
```

```pseudocode
FUNCTION requireOpenStep(
    record: StepRecord
) -> StepRecord

    IF record.status == COMMITTED
        THROW HarnessError(
            category = PERSISTENCE,
            code = "STEP_ALREADY_COMMITTED",
            message = "Un paso comprometido es de solo lectura: ninguna escritura puede modificarlo",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN record
END
```

```pseudocode
FUNCTION recordPartialOutput(
    record: StepRecord,
    output: Value
) -> StepRecord

    open: StepRecord = requireOpenStep(record)

    RETURN StepRecord(
        stepId = open.stepId,
        runId = open.runId,
        turn = open.turn,
        index = open.index,
        status = STARTED,
        partialOutput = output,
        modelResponse = open.modelResponse,
        toolCall = open.toolCall,
        toolResult = open.toolResult,
        startedAt = open.startedAt,
        committedAt = NULL
    )
END
```

```pseudocode
FUNCTION recordModelResponse(
    record: StepRecord,
    response: ModelResponse
) -> StepRecord

    open: StepRecord = requireOpenStep(record)

    RETURN StepRecord(
        stepId = open.stepId,
        runId = open.runId,
        turn = open.turn,
        index = open.index,
        status = STARTED,
        partialOutput = open.partialOutput,
        modelResponse = response,
        toolCall = NULL,
        toolResult = NULL,
        startedAt = open.startedAt,
        committedAt = NULL
    )
END
```

```pseudocode
FUNCTION recordToolCallBeforeExecution(
    record: StepRecord,
    toolCall: ToolCall
) -> StepRecord

    open: StepRecord = requireOpenStep(record)

    IF open.modelResponse == NULL OR open.modelResponse.proposedToolCall == NULL
        THROW HarnessError(
            category = PERSISTENCE,
            code = "TOOL_CALL_WITHOUT_PROPOSAL",
            message = "Solo se registra una tool call que la respuesta del modelo de este paso propuso",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN StepRecord(
        stepId = open.stepId,
        runId = open.runId,
        turn = open.turn,
        index = open.index,
        status = STARTED,
        partialOutput = open.partialOutput,
        modelResponse = open.modelResponse,
        toolCall = toolCall,
        toolResult = NULL,
        startedAt = open.startedAt,
        committedAt = NULL
    )
END
```

```pseudocode
FUNCTION recordToolResult(
    record: StepRecord,
    result: ToolResult
) -> StepRecord

    open: StepRecord = requireOpenStep(record)

    IF open.toolCall == NULL OR result.callId != open.toolCall.id
        THROW HarnessError(
            category = PERSISTENCE,
            code = "TOOL_RESULT_WITHOUT_RECORDED_CALL",
            message = "El resultado no corresponde a la tool call registrada antes de ejecutarse en este paso",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN StepRecord(
        stepId = open.stepId,
        runId = open.runId,
        turn = open.turn,
        index = open.index,
        status = STARTED,
        partialOutput = open.partialOutput,
        modelResponse = open.modelResponse,
        toolCall = open.toolCall,
        toolResult = result,
        startedAt = open.startedAt,
        committedAt = NULL
    )
END
```

```pseudocode
FUNCTION commitStep(
    record: StepRecord,
    resultPersisted: Boolean,
    execution: ExecutionContext,
    agentId: AgentId
) -> StepRecord

    open: StepRecord = requireOpenStep(record)

    IF open.modelResponse == NULL
        OR (open.toolCall != NULL AND open.toolResult == NULL)
        OR NOT resultPersisted

        THROW HarnessError(
            category = PERSISTENCE,
            code = "STEP_NOT_READY_TO_COMMIT",
            message = "Un paso se compromete solo con su respuesta, su resultado si hubo tool call, y la escritura durable confirmada",
            recoverable = TRUE,
            retryable = TRUE,
            metadata = {}
        )
    END

    committed: StepRecord = StepRecord(
        stepId = open.stepId,
        runId = open.runId,
        turn = open.turn,
        index = open.index,
        status = COMMITTED,
        partialOutput = open.partialOutput,
        modelResponse = open.modelResponse,
        toolCall = open.toolCall,
        toolResult = open.toolResult,
        startedAt = open.startedAt,
        committedAt = now()
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = STEP_COMMITTED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = committed
    )

    RETURN committed
END
```

```pseudocode
FUNCTION decideStepRecovery(
    record: StepRecord
) -> RecoveryDecision

    action: RecoveryAction = REPLAY_RECORDED
    pending: Optional<ToolCallId> = NULL

    IF record.status == STARTED
        IF record.modelResponse == NULL
            IF record.partialOutput != NULL
                action = CLOSE_WITH_PARTIAL
            ELSE
                action = REEXECUTE_MODEL_CALL
            END
        ELSE
            IF record.toolCall != NULL AND record.toolResult == NULL
                action = RESOLVE_PENDING_TOOL
                pending = record.toolCall.id
            ELSE
                IF record.toolCall == NULL AND record.modelResponse.proposedToolCall != NULL
                    action = RESUME_FROM_RESPONSE
                ELSE
                    action = COMMIT_RECORDED
                END
            END
        END
    END

    RETURN RecoveryDecision(
        runId = record.runId,
        stepId = record.stepId,
        action = action,
        pendingToolCall = pending,
        decidedAt = now()
    )
END
```

```pseudocode
FUNCTION recoverRun(
    journal: List<StepRecord>,
    execution: ExecutionContext,
    agentId: AgentId
) -> List<RecoveryDecision>

    decisions: List<RecoveryDecision> = []
    openStepSeen: Boolean = FALSE

    FOR EACH record IN journal
        IF record.runId != execution.runId OR openStepSeen
            THROW HarnessError(
                category = PERSISTENCE,
                code = "JOURNAL_INCONSISTENT",
                message = "El journal mezcla runs o tiene un paso después de uno sin comprometer",
                recoverable = FALSE,
                retryable = FALSE,
                metadata = {}
            )
        END

        IF record.status == STARTED
            openStepSeen = TRUE
        END

        decision: RecoveryDecision = decideStepRecovery(record)
        decisions = append(decisions, decision)

        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = STEP_RECOVERY_DECIDED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = decision
        )
    END

    RETURN decisions
END
```

`newStepId`, `newEventId`, `now` y `append` son utilidades primitivas. El journal llega ordenado por
`turn` e `index`.

Nótese lo que estas funciones **no** hacen:
- ninguna llama al modelo ni ejecuta una tool;
- ninguna decide si un efecto pendiente se repite: `RESOLVE_PENDING_TOOL` lo entrega a
  `IdempotencyGuard`, que lo decide con la `ReplayPolicy` de la capability y
  `executionStillInFlight = FALSE`, porque el proceso que lo ejecutaba ya no existe;
- ninguna persiste físicamente: `resultPersisted` es la confirmación del almacenamiento.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no cambia `AgentRunStatus`. El ciclo de vida de un `StepRecord`:

```text
beginStep                        → STARTED (vacío)
recordPartialOutput              → STARTED (+ partialOutput)
recordModelResponse              → STARTED (+ modelResponse)
recordToolCallBeforeExecution    → STARTED (+ toolCall)        ← antes del efecto
recordToolResult                 → STARTED (+ toolResult)
commitStep                       → COMMITTED                   ← solo lectura desde aquí
```

Y la tabla de recuperación de `decideStepRecovery`:

```text
COMMITTED                                         → REPLAY_RECORDED      (INV-E16)
STARTED, sin respuesta, con salida parcial        → CLOSE_WITH_PARTIAL
STARTED, sin respuesta, sin salida parcial        → REEXECUTE_MODEL_CALL
STARTED, respuesta con propuesta, sin toolCall    → RESUME_FROM_RESPONSE (ningún efecto empezó)
STARTED, toolCall sin toolResult                  → RESOLVE_PENDING_TOOL (INV-E17, vía CH-30)
STARTED, resultado completo sin comprometer       → COMMIT_RECORDED
```

## 13. Semántica de Fallos (Failure Semantics)

Cada fallo nuevo es un `HarnessError` de categoría `PERSISTENCE`:

```text
PERSISTENCE  PREVIOUS_STEP_NOT_COMMITTED        recoverable: FALSE, retryable: FALSE
PERSISTENCE  STEP_ALREADY_COMMITTED             recoverable: FALSE, retryable: FALSE
PERSISTENCE  TOOL_CALL_WITHOUT_PROPOSAL         recoverable: FALSE, retryable: FALSE
PERSISTENCE  TOOL_RESULT_WITHOUT_RECORDED_CALL  recoverable: FALSE, retryable: FALSE
PERSISTENCE  STEP_NOT_READY_TO_COMMIT           recoverable: TRUE,  retryable: TRUE
             (típicamente, la escritura durable todavía no confirmó)
PERSISTENCE  JOURNAL_INCONSISTENT               recoverable: FALSE, retryable: FALSE
```

`JOURNAL_INCONSISTENT` detiene la recuperación completa. Nunca se "adivina" el orden de un journal
dañado: es preferible un run detenido que un efecto duplicado.

## 14. Eventos Producidos (Events Produced)

```text
STEP_COMMITTED         — un paso quedó comprometido (payload: StepRecord)
STEP_RECOVERY_DECIDED  — la recuperación decidió qué hacer con un paso (payload: RecoveryDecision)
```

Los `record…` no emiten eventos: son escrituras intermedias de un paso abierto. El hecho observable
es el compromiso.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **Nunca se repite un efecto por accidente.** Un paso comprometido se reproduce (INV-E16), y un efecto
  que pudo haber empezado pasa por la `ReplayPolicy` de su capability (INV-E17). Un pago nunca se
  cobra dos veces por una recuperación.
- **`RESUME_FROM_RESPONSE` vuelve a gobernar.** Si el proceso se cayó antes de registrar la tool call,
  la propuesta pasa otra vez por resolución y política. Un permiso revocado durante la caída se
  respeta.
- **El journal contiene datos del turno** (respuestas del modelo, argumentos, resultados). Se protege
  con las mismas reglas que la sesión: gobierno del dato (CH-20) y aislamiento por tenant (INV-E07).
- **El modelo no ve ni escribe el journal.** La recuperación es enteramente determinística.

## 16. Tests (Tests)

```text
TEST BeginStepFailsWhilePreviousStepIsNotCommitted
TEST CommittedStepRejectsEveryWrite
TEST ToolCallIsRecordedBeforeToolRuntimeExecutes
TEST ToolCallWithoutProposalIsRejected
TEST ToolResultMustMatchTheRecordedCall
TEST CommitRequiresResponseResultAndPersistenceConfirmation
TEST CommittedStepIsReplayedNeverReexecuted
TEST InterruptedModelCallWithPartialOutputIsClosedWithoutCallingTheProvider
TEST InterruptedModelCallWithoutPartialOutputIsReexecuted
TEST ResponseWithoutRecordedToolCallResumesThroughGovernance
TEST PendingToolIsHandedToIdempotencyGuardWithExecutionNotInFlight
TEST NeverPolicyPendingToolIsReportedUnknownNotReexecuted
TEST JournalWithAStepAfterAnOpenStepIsInconsistent
TEST JournalMixingRunsIsInconsistent
TEST EveryRecoveryDecisionEmitsStepRecoveryDecided
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.2 en curso, después de CH-32)

Components — 23
 └── CMP-023 ExecutionJournal       (CH-32, nuevo — plano Reliability)

Contracts — 43
 ├── C-042 StepRecord               (CH-32, nuevo)
 └── C-043 RecoveryDecision         (CH-32, nuevo)

Relaciones nuevas (en la integración, CH-36)
 ExecutionJournal ──RESOLVE_PENDING_TOOL──→ IdempotencyGuard.decideUnknownOutcome (CH-30)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado en el turno completo.** Envolver `runGovernedTurn` con el journal es de la integración
  (CH-36, `runDurableGovernedTurn`).
- **Esperas largas.** Un paso que espera una aprobación humana no debería retener el proceso. Es de
  CH-33 (esperas durables, P-33).
- **Varias tool calls por respuesta.** `ModelResponse` v1 propone una. Si un capítulo futuro lo
  amplía, el paso tendrá una lista y la regla write-ahead aplicará a cada elemento.
- **Compactar o archivar el journal** de runs terminados. Es infraestructura de retención (CH-20).
- **El almacenamiento físico** (log, base de datos, cola) es infraestructura de borde.

## 19. Siguiente Incremento (Next Increment)

Ahora un run sobrevive a una caída sin repetir lo comprometido. Pero un run que **espera** (una
aprobación, una respuesta, una autorización OAuth) sigue ocupando un proceso, y
`resumeAfterHumanResolution` (CH-13) todavía no está cableada. `PAUSED` nunca se produce.

El siguiente capítulo introduce las **esperas durables** (P-33):
- una espera estacionada que no consume cómputo;
- la regla de que una entrega reanuda solo la espera a la que se dirige (INV-E18);
- el primer uso real de `PAUSED`.

Será CH-33 ("Esperas Durables y la Reanudación desde Cualquier Canal"), con el componente
`ResumptionCoordinator`. `next_chapter` queda en `null` porque CH-33 todavía no existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): una caída a mitad de turno pierde todo lo que pasó desde el último
   checkpoint, y no se sabe si la herramienta en curso se ejecutó.
2. **Patrones** (= §3): la única unidad persistida es el checkpoint por fase; la recuperación solo
   puede repetir el turno o perderlo.
3. **Estructuras** (= §8): `ExecutionJournal` (CMP-023), `StepRecord` (C-042) y `RecoveryDecision`
   (C-043), con write-ahead y delegación a `IdempotencyGuard`.
4. **Modelos mentales** (= §4): P-32, INV-E16 e INV-E17.

**Bucles de retroalimentación**

- **Refuerzo:** sin journal, cada caída repite turnos completos, y los turnos largos son los que más
  se caen. El journal limita la repetición a un paso.
- **Equilibrio:** INV-E16. Lo comprometido nunca vuelve a producir efectos.

**Punto de apalancamiento**

La decisión con mayor efecto es write-ahead: registrar la tool call en el `StepRecord` (C-042) antes
de ejecutarla, para que `decideStepRecovery` distinga "ningún efecto empezó" de "el efecto pudo haber
empezado".

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Qué campos de un `StepRecord` se escriben durante un paso, en qué orden, y qué exige
   `commitStep` antes de marcarlo `COMMITTED`? *(pregunta guía 1)*
2. Si un `StepRecord` `STARTED` tiene `modelResponse` con una tool call propuesta pero
   `toolCall = NULL`, ¿qué acción decide `decideStepRecovery`, y cuál decide si `toolCall` existe
   pero `toolResult = NULL`? *(pregunta guía 2)*
3. ¿Cuándo decide `decideStepRecovery` `CLOSE_WITH_PARTIAL` y cuándo `REEXECUTE_MODEL_CALL`, y por
   qué repetir la llamada al modelo no viola P-24? *(pregunta guía 3)*
4. ¿Qué hace la integración con una `RecoveryDecision` `RESOLVE_PENDING_TOOL`, qué componente decide
   si el efecto se repite, y con qué valor de `executionStillInFlight` lo invoca? *(pregunta guía 4)*

### Explicar

1. `ExecutionJournal` y `SessionManager` guardan estado durable de un run. Explica por qué el
   checkpoint de sesión no sirve como unidad de recuperación dentro de un turno, y qué decide
   `ExecutionJournal` que `SessionManager` no decide.
2. Explica por qué un `StepRecord` registra la tool call antes de ejecutarla, y qué error de
   recuperación aparecería si se registrara solo al terminar.

### Conectar

1. En CH-30, `decideUnknownOutcome` recibía `executionStillInFlight` como una señal asumida. Con
   `ExecutionJournal`, ¿de dónde sale esa señal durante una recuperación, y por qué
   `ExecutionJournal` no aplica él mismo la `ReplayPolicy` (C-039) de la capability?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
