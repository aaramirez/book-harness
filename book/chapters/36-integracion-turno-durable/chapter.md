---
id: CH-36
title: "Integración: el Turno Durable Gobernado"
starting_version: "0.1"
ending_version: "0.2"
introduces_components: []
introduces_contracts: []
modifies_contracts: []
constitutional_articles: [P-13, P-16, P-17, P-23, P-31, P-32, P-33, P-34, P-35, INV-05, INV-07, INV-13, INV-15, INV-E02, INV-E15, INV-E16, INV-E17, INV-E18, INV-E19, INV-E20]
previous_chapter: CH-35
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH36
    text: |
      Al terminar este capítulo podrás explicar un turno completo del agente desde que llega un mensaje
      por un canal hasta que termina, se estaciona esperando una aprobación o se recupera después de
      una caída, y señalar en cada punto qué componente decide y qué garantía de la versión 0.2 se
      cumple ahí.
  skeleton:
    id: SK-CH36
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
    contracts_to_be_introduced: []
  guiding_questions:
    - id: GQ-CH36-01
      text: |
        Cuando llega un mensaje por un canal, ¿qué tiene que pasar, y en qué orden, antes de que el
        modelo vea una sola palabra de él?
      answered_by: RQ-CH36-01
    - id: GQ-CH36-02
      text: |
        Si en medio de un turno el modelo propone una acción que necesita aprobación, ¿qué queda
        guardado, qué queda encendido y qué pasa cuando llega la aprobación dos días después?
      answered_by: RQ-CH36-02
    - id: GQ-CH36-03
      text: |
        Si el proceso se cae justo mientras una herramienta envía un correo, ¿qué hace el arnés al
        volver a arrancar, y quién decide si el correo se reenvía?
      answered_by: RQ-CH36-03
    - id: GQ-CH36-04
      text: |
        ¿Por qué no alcanza con llamar, en orden, a las funciones que los capítulos anteriores ya
        publicaron? ¿Qué pasa si una de ellas hace dos cosas en una sola llamada?
      answered_by: RQ-CH36-04
  systems_lens:
    iceberg_visible_fact: |
      CH-28..CH-35 introdujeron pasos durables, esperas estacionadas, direcciones de continuación,
      identidad en cada turno y un entorno sin secretos, pero cada capítulo dejó su cableado "para la
      integración": ninguna función los usa juntos (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que cada pieza funciona sola, pero algunas funciones publicadas antes
      — beginToolApprovalPause y resumeAfterHumanResolution de CH-13 — hacen dos cosas en una sola
      llamada y no exponen lo que el journal necesita registrar (ver sección 3).
    iceberg_structures: |
      Este capítulo no introduce componentes ni contratos: compone los de CH-03..CH-35 en cinco
      funciones de integración — enterDurableTurn, bindDurableCaller, runDurableGovernedStep,
      resumeDurableApproval y resolvePendingStepOnRecovery — con un tipo embebido,
      DurableStepOutcome (ver sección 11).
    iceberg_mental_models: |
      Los modelos mentales son P-23 (ejecución durable), P-32 (el paso es la unidad de
      recuperación), P-33 (esperar no consume cómputo) y P-35 (los secretos nunca entran al cómputo
      del modelo), cumplidos a la vez en el mismo turno (ver sección 4).
    reinforcing_loop: |
      Si cada garantía se cumple solo en su capítulo, cada integración nueva las reimplementa a su
      manera y deja huecos distintos; cuantas más integraciones, más huecos. Un turno durable de
      referencia corta la espiral: las integraciones futuras (CH-47) parten de él.
    balancing_loop: |
      El journal es el mecanismo de equilibrio del turno completo: por muchas caídas, esperas y
      reanudaciones que ocurran, cada paso se compromete una sola vez y nunca se repite (INV-E16).
    leverage_point: |
      La decisión con mayor efecto de este capítulo es componer las piezas de CH-13 en vez de
      invocarlas cuando una de ellas oculta lo que el journal necesita: así la tool call se registra
      siempre antes de ejecutarse, también después de una aprobación.
  recall_questions:
    - id: RQ-CH36-01
      text: |
        ¿Qué tres funciones de CH-31 y CH-34 llama enterDurableTurn, en qué orden, y qué devuelve si
        la admisión rechaza o si el llamante no puede continuar la sesión?
    - id: RQ-CH36-02
      text: |
        En runDurableGovernedStep, ¿qué hace el camino REQUIRE_APPROVAL, en qué estado queda el
        StepRecord, y qué registra resumeDurableApproval antes de ejecutar la tool?
    - id: RQ-CH36-03
      text: |
        ¿Qué hace resolvePendingStepOnRecovery con un paso RESOLVE_PENDING_TOOL, con qué valor de
        executionStillInFlight llama a decideUnknownOutcome, y qué pasa en cada caso de ReplayPolicy?
    - id: RQ-CH36-04
      text: |
        ¿Por qué el turno durable no invoca beginToolApprovalPause ni resumeAfterHumanResolution de
        CH-13, y qué piezas de CH-06, CH-10 y CH-13 compone en su lugar?
  explain_prompts:
    - id: EP-CH36-01
      text: |
        ExecutionJournal y ResumptionCoordinator actúan sobre el mismo turno cuando hace falta una
        aprobación. Explica, como si hablaras con alguien sin contexto técnico, qué guarda cada uno
        mientras el run espera, y por qué el paso sigue abierto pero nada se ejecutó.
      target_entity: CMP-023
    - id: EP-CH36-02
      text: |
        Explica por qué la persona que aprueba una acción no pasa a ser el llamante del turno, y qué
        se rompería si la acción se ejecutara con los permisos del aprobador.
      target_entity: CMP-024
  interleaved_questions:
    - id: IQ-CH36-01
      text: |
        CH-26 integró por primera vez los componentes enterprise en runGovernedEnterpriseTurn, pero
        todo el turno corría en un solo proceso de principio a fin. ¿Qué pasos de ese turno se
        vuelven durables en CH-36, y cuál sigue fuera del journal?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-012, CMP-015, CMP-014]
      prior_chapter: CH-26
  flashcards:
    - id: FC-CH36-01
      front: |
        ¿Cuáles son las cinco funciones de integración de CH-36 y qué hace cada una?
      back: |
        enterDurableTurn (admite y enruta), bindDurableCaller (liga el llamante), runDurableGovernedStep
        (un paso con journal: modelo, política, tool aislada o espera), resumeDurableApproval (reanuda
        una aprobación registrando antes de ejecutar) y resolvePendingStepOnRecovery (resuelve un
        efecto pendiente tras una caída).
      source_entity: CMP-023
      chapter_introduced_in: CH-36
      review_stage: DAY_1
    - id: FC-CH36-02
      front: |
        ¿En qué estado queda el StepRecord de un paso estacionado esperando una aprobación?
      back: |
        STARTED, con modelResponse y sin toolCall: nada se ejecutó. Al reanudar, la tool call se
        registra antes de ejecutarse; si se rechaza, el paso se compromete sin tool call.
      source_entity: C-042
      chapter_introduced_in: CH-36
      review_stage: DAY_1
    - id: FC-CH36-03
      front: |
        ¿Quién es el llamante después de que alguien aprueba una espera?
      back: |
        El mismo de antes (caller.current): la acción se ejecuta en nombre de quien la pidió. El
        aprobador queda registrado como resolvedBy de la resolución (CH-06).
      source_entity: C-044
      chapter_introduced_in: CH-36
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH36-01
      recall_question: RQ-CH36-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH36-02
      recall_question: RQ-CH36-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH36-03
      recall_question: RQ-CH36-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH36-04
      recall_question: RQ-CH36-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 36 — Integración: el Turno Durable Gobernado

> **Regla de integración:** ninguna garantía de la versión 0.2 vale si no se cumple en el mismo turno
> que las demás.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás explicar un turno completo del agente desde
que llega un mensaje por un canal hasta que termina, se estaciona esperando una aprobación o se
recupera después de una caída. También podrás señalar en cada punto qué componente decide y qué
garantía de la versión 0.2 se cumple ahí.

**Esqueleto.** Noveno y último capítulo del Tramo 4. No introduce componentes ni contratos: compone
los de CH-03..CH-35 en cinco funciones de integración.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Cuando llega un mensaje por un canal, ¿qué tiene que pasar, y en qué orden, antes de que el
   modelo vea una sola palabra de él?
2. Si en medio de un turno el modelo propone una acción que necesita aprobación, ¿qué queda
   guardado, qué queda encendido y qué pasa cuando llega la aprobación dos días después?
3. Si el proceso se cae justo mientras una herramienta envía un correo, ¿qué hace el arnés al volver
   a arrancar, y quién decide si el correo se reenvía?
4. ¿Por qué no alcanza con llamar, en orden, a las funciones que los capítulos anteriores ya
   publicaron? ¿Qué pasa si una de ellas hace dos cosas en una sola llamada?

## 1. Arquitectura Actual (Current Architecture)

La versión 0.2 agregó, capítulo por capítulo:

| Capítulo | Pieza | Garantía |
|---|---|---|
| CH-28 | `PendingInput` en `AgentLoop` | un mensaje que llega durante el turno no interrumpe una tool |
| CH-29 | compactación estructurada en `ContextEngine` | el historial se resume sin cortar una tool call de su resultado |
| CH-30 | `ReplayPolicy` en `IdempotencyGuard` | un efecto desconocido solo se repite si es `SAFE` (INV-E17) |
| CH-31 | `Principal` / `CallerSnapshot` en `AdmissionController` | la identidad viaja con cada turno; arranque cerrado (INV-E15) |
| CH-32 | `ExecutionJournal` | un paso comprometido nunca se repite (INV-E16) |
| CH-33 | `ResumptionCoordinator` | esperar no consume cómputo; la entrega nombra su espera (INV-E18) |
| CH-34 | `ContinuationRegistry` | una conversación externa tiene una sola sesión dueña (INV-E19) |
| CH-35 | `IsolatedExecutionEnvironment` | ninguna credencial dentro del entorno del código (INV-E20) |

La última integración del libro es `runGovernedEnterpriseTurn` (CH-26) y su variante de control
(CH-27): admisión, credenciales, idempotencia, auditoría y gobierno del dato, pero todo en **un
solo proceso**, de principio a fin.

## 2. El Problema (Problem)

Cada capítulo de CH-31 a CH-35 terminó con la misma frase en su sección 18: "se cablea en CH-36".
Hoy:
- ninguna función lleva el `Principal` de la admisión al `ExecutionContext` del turno;
- ningún turno registra sus pasos en el journal;
- ningún turno se estaciona con `parkRun`: los caminos de CH-13 siguen corriendo en un proceso;
- ningún turno ejecuta sus tools en el entorno aislado;
- ninguna recuperación resuelve un paso con un efecto pendiente.

Cada garantía existe, pero solo dentro de su capítulo.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **Llamar a las piezas en orden no alcanza.** Dos funciones de CH-13 hacen dos cosas en una sola
  llamada y no exponen lo que el journal necesita:
  - `beginToolApprovalPause` crea la `HumanInteractionRequest` y pausa el run, pero **no devuelve la
    solicitud**. `parkRun` (CH-33) necesita su id;
  - `resumeAfterHumanResolution` resuelve la solicitud, **ejecuta la tool** y continúa el turno, sin
    exponer el `ToolResult`. El journal necesita registrar la tool call **antes** de ejecutarla y su
    resultado **después** (write-ahead, CH-32).
- **CH-33 cableó `resumeAfterHumanResolution`** con `resumeToolApprovalWait`, pero sin journal: si el
  proceso se cae durante esa ejecución, la recuperación no sabe que la tool empezó.
- **La recuperación de CH-32 se detiene en `RESOLVE_PENDING_TOOL`**, que entrega el efecto a
  `IdempotencyGuard`, pero nadie une las dos decisiones con la ejecución y el compromiso del paso.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved (todos, en el mismo turno)
    P-13  la autorización sigue siendo de PolicyEngine en cada paso
    P-16  el estímulo llega como ActivationRequest v2
    P-17  la admisión precede a todo lo demás (enterDurableTurn)
    P-23  el turno sobrevive a una caída (journal + resolvePendingStepOnRecovery)
    P-31  el Principal de la admisión viaja en el ExecutionContext (bindDurableCaller)
    P-32  cada llamada al modelo y su tool call son un paso registrado
    P-33  el camino REQUIRE_APPROVAL estaciona el run y termina
    P-34  la continuación sale de la dirección, nunca del texto
    P-35  la tool corre en el entorno aislado; el egress lleva la credencial desde el borde

Invariants preserved
    INV-05   toda tool call pasa por executeToolCallIsolated → executeToolCall (CH-02)
    INV-07   el resultado, recuperado o nuevo, vuelve como observación
    INV-13   el run se reconstruye desde el journal
    INV-15   la tool aprobada no se ejecuta antes de acceptDelivery
    INV-E02  sin ADMIT no hay ruta ni run
    INV-E15  un arnés sin reglas rechaza desde enterDurableTurn
    INV-E16  un paso COMMITTED se reproduce, nunca se re-ejecuta
    INV-E17  el efecto pendiente se repite solo si es SAFE (decideUnknownOutcome)
    INV-E18  solo la entrega dirigida y autorizada reanuda la espera
    INV-E19  la dirección tiene una sola sesión dueña
    INV-E20  ninguna credencial dentro del entorno

Component ownership changes
    Ninguno. Las cinco funciones son de integración: no deciden nada que no decida ya un
    componente registrado.

Contract changes
    Ninguno. Un tipo embebido, DurableStepOutcome, sin C-XXX.

Deterministic vs agentic boundary
    Sin cambios: el modelo propone una respuesta y una tool call por paso; todo lo demás es
    determinístico.
```

## 5. Conceptos Nuevos (New Concepts)

- **Turno durable gobernado** (*durable governed turn*): un turno que cumple a la vez todas las
  garantías de la versión 0.2. No es un componente: es la forma en que la integración compone los
  componentes.
- **Componer en vez de invocar:** cuando una función publicada hace dos cosas en una sola llamada y
  oculta un dato que otra garantía necesita, la integración usa sus mismas piezas por separado. La
  función original no se modifica y sigue siendo válida en su contexto (un proceso, sin journal).
- **Paso estacionado:** un paso cuya respuesta ya llegó y cuya tool call espera aprobación. Queda
  `STARTED`, con `modelResponse` y sin `toolCall`: nada se ejecutó, y no hay proceso esperando.

## 6. Nuevas Estructuras de Datos (New Data Structures)

**Este capítulo no introduce contratos.** Usa, sin modificarlos, los contratos registrados hasta
CH-35, y un único tipo embebido propio de la integración.

| Identificador (heredado, sin `C-XXX` propio) | Introducido en | Rol en este capítulo |
|---|---|---|
| `ExecutionUsage` | CH-07 §6 | uso del run, que `resumeTurnWithObservation` recibe |
| `ProcessMode` | CH-31 §6 | modo del proceso, que `admitWithVerifiedIdentity` recibe |
| `SessionOwnershipRule` | CH-31 §6 | regla de propiedad de la sesión que se continúa |
| `ContinuationClaim` | CH-34 §6 | reclamos durables de direcciones |
| `ContinuationRoute` | CH-34 §6 | la decisión continuar / activar |
| `ResponderRule` | CH-33 §6 | quién puede aprobar la espera |
| `WaitDelivery` | CH-33 §6 | la respuesta que llega por un canal |
| `UnknownOutcomeDecision` | CH-30 §6 | la decisión de `IdempotencyGuard` ante un efecto pendiente |
| `AgentEventType` | CH-00 | reutiliza `MODEL_RESPONSE_RECEIVED`, `POLICY_EVALUATED`, `TOOL_CALL_COMPLETED`, `TOOL_CALL_FAILED`, `HUMAN_INTERACTION_REQUESTED`, `HUMAN_INTERACTION_RESOLVED` y `SESSION_CHECKPOINT_CREATED` |

### `DurableStepOutcome` — lo que deja un paso durable (embebido)

```pseudocode
STRUCT DurableStepOutcome
    step: StepRecord
    state: AgentState
    wait: Optional<ParkedWait>
    request: Optional<HumanInteractionRequest>
END
```

`wait` y `request` solo tienen valor cuando el paso se estacionó esperando una aprobación.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

**Este capítulo no introduce ni modifica contratos.** `registry/contracts.yaml` sigue en los 48
contratos que CH-35 dejó registrados.

## 8. Responsabilidades de Componentes (Component Responsibilities)

**Este capítulo no introduce componentes ni cambia ninguna ficha.** Cada decisión del turno la toma
el mismo componente que la tomaba en su capítulo:

| Decisión | Componente | Capítulo |
|---|---|---|
| ¿entra este estímulo? | AdmissionController | CH-14, CH-31 |
| ¿a qué sesión va? | ContinuationRegistry | CH-34 |
| ¿puede este llamante continuarla? | AdmissionController | CH-31 |
| ¿qué responde el modelo? | ModelGateway | CH-03 |
| ¿qué capability es? | CapabilityRegistry | CH-08 |
| ¿está permitida? | PolicyEngine | CH-05 |
| ¿cómo se pide la aprobación? | HumanInteractionService | CH-06 |
| ¿cómo espera el run y quién responde? | ResumptionCoordinator | CH-33 |
| ¿dónde corre el código y qué alcanza? | IsolatedExecutionEnvironment | CH-35 |
| ¿cómo se ejecuta la tool? | ToolRuntime | CH-02 |
| ¿qué paso quedó comprometido? | ExecutionJournal | CH-32 |
| ¿se repite un efecto desconocido? | IdempotencyGuard | CH-17, CH-30 |
| ¿cómo sigue el turno con la observación? | (integración de CH-13) | CH-13 |

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
enterDurableTurn          → admitWithVerifiedIdentity (CH-31) → routeAdmittedRequest (CH-34)
                            → continuationAllowedForCaller (CH-31)
bindDurableCaller         → buildCallerSnapshot → bindCallerToExecution (CH-31)
runDurableGovernedStep    → beginStep / recordModelResponse (CH-32) → invokeModelForTurn (CH-03)
                            → resolveModelProposedToolCall (CH-08) → evaluatePolicyForToolCall (CH-05)
                            → DENY: commitStep (CH-32)
                            → REQUIRE_APPROVAL: createHumanInteractionRequest (CH-06) → parkRun /
                              linkRequestToWait / parkedAgentState (CH-33)
                              → createOrUpdateSessionCheckpoint (CH-10)
                            → ALLOW: recordToolCallBeforeExecution → executeToolCallIsolated (CH-35)
                              → recordToolResult → commitStep (CH-32)
resumeDurableApproval     → acceptDelivery (CH-33) → resolveHumanInteractionRequest (CH-06)
                            → recordToolCallBeforeExecution → executeToolCallIsolated → recordToolResult
                              → commitStep → resumeTurnWithObservation (CH-13)
resolvePendingStepOnRecovery → decideUnknownOutcome (CH-30) → executeToolCallIsolated (CH-35) o
                               buildUnknownOutcomeResult (CH-30) → recordToolResult → commitStep (CH-32)
```

**Por qué no se invocan `beginToolApprovalPause` ni `resumeAfterHumanResolution` (CH-13).** Ambas
siguen siendo correctas para lo que CH-13 modela: un turno en un solo proceso. Pero la primera no
devuelve la solicitud que crea, y la segunda ejecuta la tool dentro de la misma llamada que continúa
el turno. El turno durable necesita el id de la solicitud (para estacionar) y un punto entre "voy a
ejecutar" y "ya ejecuté" (para el journal). Por eso compone sus mismas piezas: `createHumanInteractionRequest`
y `createOrUpdateSessionCheckpoint` para estacionar; `resolveHumanInteractionRequest`,
`executeToolCall` (vía `executeToolCallIsolated`) y `resumeTurnWithObservation` para reanudar.
Ninguna de ellas cambia. `resumeToolApprovalWait` (CH-33) queda como el camino no durable.

**La creación del run** (activar el agente, inicializarlo, construir el `ExecutionContext`) es la de
CH-26 y no se repite aquí. `bindDurableCaller` se aplica a ese `ExecutionContext` antes del primer
paso.

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
Canal → AdmissionController → ContinuationRegistry → [run de CH-26] → ExecutionJournal
      → ModelGateway → CapabilityRegistry → PolicyEngine
      → (ALLOW) IsolatedExecutionEnvironment + ToolRuntime | (REQUIRE_APPROVAL) ResumptionCoordinator
```

**Vista 2 — Sequence: un turno con aprobación y una caída**

```text
Canal: ActivationRequest(address = chat-equipo/1718)
   │ enterDurableTurn → ADMIT (principal) → CONTINUE_SESSION(S1) → continuationAllowedForCaller
   │ bindDurableCaller → ExecutionContext.caller
   │
   │ paso 1: runDurableGovernedStep → modelo → sin tool call → COMMITTED
   │ paso 2: runDurableGovernedStep → modelo propone "pagar" → REQUIRE_APPROVAL
   │         → request → parkRun (DESIGNATED_PRINCIPAL) → WAITING_FOR_HUMAN → checkpoint
   ▼ (el proceso termina; el paso 2 queda STARTED, sin toolCall)
… dos días …
Canal: WaitDelivery(waitId, aprobador, APPROVED)
   │ resumeDurableApproval → acceptDelivery → resolveHumanInteractionRequest
   │   → recordToolCallBeforeExecution → executeToolCallIsolated …
   ▼ (caída del proceso durante la ejecución)
Proceso nuevo: recoverRun (CH-32)
   │ paso 1 → REPLAY_RECORDED ; paso 2 → RESOLVE_PENDING_TOOL
   │ resolvePendingStepOnRecovery → decideUnknownOutcome(…, executionStillInFlight = FALSE)
   │   "pagar" es NEVER → REPORT_UNKNOWN → buildUnknownOutcomeResult → COMMITTED
   │ el modelo recibe "resultado desconocido" como observación (INV-07)
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

```pseudocode
FUNCTION enterDurableTurn(
    request: ActivationRequest,
    verifiedPrincipal: Optional<Principal>,
    admissionConfigured: Boolean,
    processMode: ProcessMode,
    claims: List<ContinuationClaim>,
    ownerSnapshot: Optional<CallerSnapshot>,
    ownershipRule: SessionOwnershipRule
) -> Optional<ContinuationRoute>

    admission: AdmissionDecision = admitWithVerifiedIdentity(
        request, verifiedPrincipal, admissionConfigured, processMode
    )

    IF admission.outcome != ADMIT
        RETURN NULL
    END

    route: ContinuationRoute = routeAdmittedRequest(request, admission, claims)

    IF route.action == CONTINUE_SESSION
        AND (ownerSnapshot == NULL
            OR NOT continuationAllowedForCaller(ownerSnapshot, admission.principal, ownershipRule))

        THROW HarnessError(
            category = ADMISSION,
            code = "SESSION_CONTINUATION_NOT_ALLOWED",
            message = "El estímulo fue admitido y su dirección tiene sesión dueña, pero la regla de propiedad no permite que este llamante la continúe",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN route
END
```

```pseudocode
FUNCTION bindDurableCaller(
    execution: ExecutionContext,
    principal: Principal
) -> ExecutionContext

    snapshot: CallerSnapshot = buildCallerSnapshot(execution.caller, principal)

    RETURN bindCallerToExecution(execution, snapshot)
END
```

```pseudocode
FUNCTION runDurableGovernedStep(
    state: AgentState,
    execution: ExecutionContext,
    previousStep: Optional<StepRecord>,
    turn: Integer,
    index: Integer,
    pendingMessages: List<AgentMessage>,
    providerFinished: Boolean,
    providerProposesToolCall: Boolean,
    providerCapabilityName: Text,
    providerRawArguments: Map<Text, Value>,
    providerContent: Value,
    registeredCapabilities: List<CapabilityDescriptor>,
    argumentsMatchSchema: Boolean,
    approvalRule: ResponderRule,
    designatedApprover: Optional<Principal>,
    approvalExpiresAt: Optional<Timestamp>,
    sandbox: Optional<SandboxSession>,
    isolatedCapabilities: List<CapabilityId>,
    toolExecutionSucceeded: Boolean,
    toolExecutionOutput: Value,
    resultPersisted: Boolean,
    session: Optional<SessionState>,
    activeSubscriptions: List<EventSubscription>
) -> DurableStepOutcome

    IF execution.caller == NULL
        THROW HarnessError(
            category = ADMISSION,
            code = "DURABLE_TURN_WITHOUT_CALLER",
            message = "Un turno durable necesita el llamante verificado en su ExecutionContext (bindDurableCaller)",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    step: StepRecord = beginStep(execution.runId, turn, index, previousStep)

    response: ModelResponse = invokeModelForTurn(
        state, execution, pendingMessages, TRUE, providerFinished, providerProposesToolCall,
        providerCapabilityName, providerRawArguments, providerContent
    )
    emitAndDistribute(MODEL_RESPONSE_RECEIVED, execution, state.agentId, response, activeSubscriptions)

    step = recordModelResponse(step, response)

    IF response.proposedToolCall == NULL
        committed: StepRecord = commitStep(step, resultPersisted, execution, state.agentId)
        RETURN DurableStepOutcome(step = committed, state = state, wait = NULL, request = NULL)
    END

    call: ToolCall = resolveModelProposedToolCall(
        response, registeredCapabilities, execution, state.agentId, argumentsMatchSchema
    )
    decision: PolicyDecision = evaluatePolicyForToolCall(call, execution, state.agentId)
    emitAndDistribute(POLICY_EVALUATED, execution, state.agentId, decision, activeSubscriptions)

    IF decision.outcome == DENY
        denied: StepRecord = commitStep(step, resultPersisted, execution, state.agentId)
        RETURN DurableStepOutcome(step = denied, state = state, wait = NULL, request = NULL)
    END

    IF decision.outcome == REQUIRE_APPROVAL
        request: HumanInteractionRequest = createHumanInteractionRequest(
            decision, APPROVAL, execution, state.agentId
        )
        emitAndDistribute(HUMAN_INTERACTION_REQUESTED, execution, state.agentId, request, activeSubscriptions)

        wait: ParkedWait = parkRun(
            state, TOOL_APPROVAL, request.id, NULL, execution.caller.current,
            approvalRule, designatedApprover, approvalExpiresAt, execution
        )
        linked: HumanInteractionRequest = linkRequestToWait(request, wait)
        pausedState: AgentState = parkedAgentState(state, wait)

        checkpoint: SessionState = createOrUpdateSessionCheckpoint(
            session, pausedState, execution, state.agentId
        )
        emitAndDistribute(SESSION_CHECKPOINT_CREATED, execution, state.agentId, checkpoint, activeSubscriptions)

        RETURN DurableStepOutcome(step = step, state = pausedState, wait = wait, request = linked)
    END

    step = recordToolCallBeforeExecution(step, call)

    result: ToolResult = executeToolCallIsolated(
        call, sandbox, isolatedCapabilities, execution, state.agentId,
        TRUE, TRUE, toolExecutionSucceeded, toolExecutionOutput
    )

    IF result.succeeded
        emitAndDistribute(TOOL_CALL_COMPLETED, execution, state.agentId, result, activeSubscriptions)
    ELSE
        emitAndDistribute(TOOL_CALL_FAILED, execution, state.agentId, result, activeSubscriptions)
    END

    step = recordToolResult(step, result)
    done: StepRecord = commitStep(step, resultPersisted, execution, state.agentId)

    RETURN DurableStepOutcome(step = done, state = state, wait = NULL, request = NULL)
END
```

```pseudocode
FUNCTION resumeDurableApproval(
    wait: ParkedWait,
    delivery: WaitDelivery,
    request: HumanInteractionRequest,
    step: StepRecord,
    call: ToolCall,
    pausedState: AgentState,
    execution: ExecutionContext,
    sandbox: Optional<SandboxSession>,
    isolatedCapabilities: List<CapabilityId>,
    toolExecutionSucceeded: Boolean,
    toolExecutionOutput: Value,
    resultPersisted: Boolean,
    candidatesSoFar: List<AgentMessage>,
    session: Optional<SessionState>,
    activeSubscriptions: List<EventSubscription>,
    usage: ExecutionUsage,
    finalModelContent: Value
) -> AgentState

    accepted: ParkedWait = acceptDelivery(wait, delivery, execution, pausedState.agentId)

    resolution: HumanInteractionResolution = resolveHumanInteractionRequest(
        request, delivery.outcome, delivery.value, delivery.responder.principalId,
        execution, pausedState.agentId
    )
    emitAndDistribute(HUMAN_INTERACTION_RESOLVED, execution, pausedState.agentId, resolution, activeSubscriptions)

    resumedState: AgentState = AgentState(
        runId = pausedState.runId,
        sessionId = pausedState.sessionId,
        agentId = pausedState.agentId,
        status = RUNNING,
        currentTurn = pausedState.currentTurn
    )

    observation: AgentMessage = AgentMessage(
        id = newMessageId(),
        role = TOOL,
        content = HarnessError(
            category = POLICY,
            code = "HUMAN_APPROVAL_REJECTED",
            message = "La aprobación humana requerida para este ToolCall fue rechazada",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        ),
        timestamp = now()
    )

    IF resolution.outcome == APPROVED
        opened: StepRecord = recordToolCallBeforeExecution(step, call)

        result: ToolResult = executeToolCallIsolated(
            call, sandbox, isolatedCapabilities, execution, resumedState.agentId,
            TRUE, TRUE, toolExecutionSucceeded, toolExecutionOutput
        )

        IF result.succeeded
            emitAndDistribute(TOOL_CALL_COMPLETED, execution, resumedState.agentId, result, activeSubscriptions)
        ELSE
            emitAndDistribute(TOOL_CALL_FAILED, execution, resumedState.agentId, result, activeSubscriptions)
        END

        recorded: StepRecord = recordToolResult(opened, result)
        commitStep(recorded, resultPersisted, execution, resumedState.agentId)

        observation = AgentMessage(
            id = newMessageId(),
            role = TOOL,
            content = result,
            timestamp = now()
        )
    ELSE
        commitStep(step, resultPersisted, execution, resumedState.agentId)
    END

    candidates: List<AgentMessage> = append(candidatesSoFar, observation)

    RETURN resumeTurnWithObservation(
        resumedState, execution, candidates, session, activeSubscriptions, usage, finalModelContent
    )
END
```

```pseudocode
FUNCTION resolvePendingStepOnRecovery(
    step: StepRecord,
    decision: RecoveryDecision,
    descriptor: CapabilityDescriptor,
    pendingRecord: IdempotencyRecord,
    sandbox: Optional<SandboxSession>,
    isolatedCapabilities: List<CapabilityId>,
    execution: ExecutionContext,
    agentId: AgentId,
    toolExecutionSucceeded: Boolean,
    toolExecutionOutput: Value,
    resultPersisted: Boolean
) -> StepRecord

    IF decision.action != RESOLVE_PENDING_TOOL OR decision.stepId != step.stepId
        THROW HarnessError(
            category = PERSISTENCE,
            code = "NOT_A_PENDING_TOOL_STEP",
            message = "Solo se resuelve en recuperación un paso cuya decisión es RESOLVE_PENDING_TOOL",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    outcome: UnknownOutcomeDecision = decideUnknownOutcome(
        step.toolCall, descriptor, pendingRecord, FALSE, execution, agentId
    )

    result: ToolResult = NULL

    IF outcome.action == REEXECUTE
        result = executeToolCallIsolated(
            step.toolCall, sandbox, isolatedCapabilities, execution, agentId,
            TRUE, TRUE, toolExecutionSucceeded, toolExecutionOutput
        )
    ELSE
        result = buildUnknownOutcomeResult(step.toolCall, outcome)
    END

    recorded: StepRecord = recordToolResult(step, result)

    RETURN commitStep(recorded, resultPersisted, execution, agentId)
END
```

`newMessageId`, `now` y `append` son utilidades primitivas. En `resolvePendingStepOnRecovery`, el
`ELSE` es `REPORT_UNKNOWN`: con `executionStillInFlight = FALSE`, `decideUnknownOutcome` nunca
devuelve `WAIT` (CH-30), así que las dos únicas salidas son `REEXECUTE` o `REPORT_UNKNOWN`.

Nótese lo que estas funciones **no** hacen:
- ninguna decide algo que no decida ya un componente (§8);
- ninguna modifica una función publicada: `beginToolApprovalPause` y `resumeAfterHumanResolution`
  siguen intactas;
- ninguna ejecuta una tool sin haberla registrado antes en el journal.

## 12. Transiciones de Estado (State Transitions)

```text
ActivationRequest   → REJECT                          → sin run (enterDurableTurn = NULL)
                    → ADMIT → ruta                    → run de CH-26 → bindDurableCaller
paso sin tool call  → STARTED → COMMITTED
paso DENY           → STARTED → COMMITTED (sin toolCall)
paso ALLOW          → STARTED → +toolCall → +toolResult → COMMITTED
paso REQUIRE_APPROVAL → STARTED (sin toolCall) · run WAITING_FOR_HUMAN · ParkedWait PARKED
   entrega APPROVED → +toolCall → +toolResult → COMMITTED · RUNNING · RESUMED
   entrega REJECTED → COMMITTED (sin toolCall) · RUNNING · RESUMED
caída con toolCall sin resultado → RESOLVE_PENDING_TOOL → SAFE: re-ejecuta | NEVER: UNKNOWN → COMMITTED
```

## 13. Semántica de Fallos (Failure Semantics)

Dos códigos nuevos de `HarnessError`, con `ErrorCategory` ya existentes, más todos los de
CH-30..CH-35:

```text
ADMISSION    DURABLE_TURN_WITHOUT_CALLER       recoverable: FALSE, retryable: FALSE
PERSISTENCE  NOT_A_PENDING_TOOL_STEP           recoverable: FALSE, retryable: FALSE
```

`enterDurableTurn` reutiliza `SESSION_CONTINUATION_NOT_ALLOWED` (CH-31), aquí **sin** evento: el run
de la sesión dueña todavía no está cargado, el mismo criterio de CH-14 para la admisión.

Un fallo de cualquier función compuesta se propaga tal cual: la integración no lo traduce ni lo
oculta.

## 14. Eventos Producidos (Events Produced)

Ningún `AgentEventType` nuevo. El turno durable produce los eventos de CH-03..CH-35 en su orden
natural, por ejemplo, en el camino con aprobación:

```text
MODEL_RESPONSE_RECEIVED → POLICY_EVALUATED → HUMAN_INTERACTION_REQUESTED → RUN_PARKED
→ SESSION_CHECKPOINT_CREATED        … (espera) …
RUN_RESUMED → HUMAN_INTERACTION_RESOLVED → TOOL_CALL_COMPLETED → STEP_COMMITTED
```

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **El aprobador no pasa a ser el llamante.** La acción se ejecuta en nombre de `caller.current`, que
  la pidió; el aprobador queda como `resolvedBy`. Si se ejecutara con los permisos del aprobador,
  cualquier aprobación sería una escalada de privilegios.
- **La política se evalúa una vez por paso, y otra vez al recuperar si hace falta.** Un paso
  estacionado no se "recupera": espera. Un paso interrumpido sin tool call registrada vuelve a pasar
  por `PolicyEngine` (`RESUME_FROM_RESPONSE`, CH-32).
- **Nunca se ejecuta sin registro.** La tool call se registra antes de ejecutarse en los tres
  caminos que ejecutan (ALLOW, aprobación, recuperación con `SAFE`).
- **Un efecto que pudo haber ocurrido nunca se repite a ciegas.** Tras una caída, `NEVER` produce
  "resultado desconocido", nunca un segundo pago.
- **Todo el código del modelo corre sin secretos**, también después de una aprobación o de una
  recuperación.

## 16. Tests (Tests)

```text
TEST RejectedActivationNeverCreatesARoute
TEST ContinuationWithoutOwnershipRuleIsRejectedWithoutEvent
TEST DurableStepRequiresABoundCaller
TEST StepWithoutToolCallCommitsAfterTheModelResponse
TEST DeniedToolCallCommitsTheStepWithoutToolCall
TEST ApprovalParksTheRunAndLeavesTheStepStartedWithoutToolCall
TEST ApprovalRequestIsLinkedToItsWait
TEST ApprovedDeliveryRecordsTheToolCallBeforeExecuting
TEST RejectedDeliveryCommitsTheStepWithoutExecuting
TEST ApproverNeverBecomesTheCaller
TEST AllowedToolRunsInTheIsolatedEnvironment
TEST CrashDuringApprovedExecutionIsResolvedOnRecovery
TEST NeverPolicyPendingStepIsReportedUnknownAndCommitted
TEST SafePolicyPendingStepIsReexecutedAndCommitted
TEST CommittedStepsAreReplayedDuringRecovery
TEST PublishedFunctionsOfChapter13RemainUnchanged
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness v0.2 (después de CH-36) — 26 componentes, 48 contratos, 37 capítulos

Turno durable gobernado
 Canal → Ingress Adapter → AdmissionController (Principal, INV-E15)
       → ContinuationRegistry (INV-E19) → run (CH-26) → bindDurableCaller (P-31)
       → por cada paso: ExecutionJournal (P-32)
            → ModelGateway → CapabilityRegistry → PolicyEngine
            → ALLOW: IsolatedExecutionEnvironment + ToolRuntime (P-35)
            → REQUIRE_APPROVAL: HumanInteractionService + ResumptionCoordinator (P-33)
       → recuperación: ExecutionJournal → IdempotencyGuard (INV-E16, INV-E17)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **Steering y compactación (CH-28, CH-29)** actúan dentro de `AgentLoop` y `ContextEngine` entre
  pasos; el turno durable los atraviesa sin cambiarlos. Hacer durable un `PendingInput` que llegó
  entre dos pasos queda como deuda.
- **Preguntas, autorizaciones y límites de presupuesto** se estacionan igual que una aprobación; su
  reanudación durable sigue el patrón de `resumeDurableApproval` y no se escribe cuatro veces.
- **Liberar la dirección de continuación** al cerrar la sesión, y **responder por el canal**: siguen
  pendientes (CH-34).
- **Vencimiento activo de esperas** con un schedule interno (CH-33/CH-34).
- **La detección de la credencial faltante** que abriría un `AuthorizationChallenge` (CH-33).
- **Revisar CH-13** para que `beginToolApprovalPause` devuelva su solicitud y
  `resumeAfterHumanResolution` exponga el `ToolResult`: permitiría invocarlas en vez de componerlas.
  No se hace aquí para no reabrir pseudocódigo publicado.
- **El Routing** (qué agente atiende una activación nueva) sigue en Preview.

## 19. Siguiente Incremento (Next Increment)

La versión 0.2 está completa: el arnés sobrevive a caídas, espera sin cómputo, sabe a qué sesión va
cada mensaje, sabe quién llama y ejecuta el código del modelo sin secretos. Lo que todavía no sabe es
**con qué modelo** trabaja más allá de un nombre, **cuánto cuesta** cada llamada, ni cómo conectarse
con el mundo: herramientas externas, fuentes de datos y otros agentes.

Antes del siguiente capítulo se cierra la versión 0.2 (epílogo, diagramas generales, conteos y
tag). Luego empieza la versión 0.3 con el **modelo como dato** (catálogo, costo y cache).

Será CH-37 ("El Modelo como Dato: Catálogo, Costo y Cache"). `next_chapter` queda en `null` porque
CH-37 todavía no existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): cada garantía de la versión 0.2 existe, pero solo dentro de su capítulo.
2. **Patrones** (= §3): dos funciones de CH-13 hacen dos cosas en una llamada y ocultan lo que el
   journal necesita.
3. **Estructuras** (= §11): cinco funciones de integración y `DurableStepOutcome`, sin componentes
   ni contratos nuevos.
4. **Modelos mentales** (= §4): P-23, P-32, P-33 y P-35 en el mismo turno.

**Bucles de retroalimentación**

- **Refuerzo:** cada integración que reimplementa las garantías deja huecos distintos. Un turno
  durable de referencia corta la espiral.
- **Equilibrio:** el journal. Cada paso se compromete una sola vez.

**Punto de apalancamiento**

La decisión con mayor efecto es componer las piezas de CH-13 en vez de invocarlas cuando ocultan lo
que el journal necesita: así la tool call se registra antes de ejecutarse, también después de una
aprobación.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Qué tres funciones de CH-31 y CH-34 llama `enterDurableTurn`, en qué orden, y qué devuelve si la
   admisión rechaza o si el llamante no puede continuar la sesión? *(pregunta guía 1)*
2. En `runDurableGovernedStep`, ¿qué hace el camino `REQUIRE_APPROVAL`, en qué estado queda el
   `StepRecord`, y qué registra `resumeDurableApproval` antes de ejecutar la tool? *(pregunta guía 2)*
3. ¿Qué hace `resolvePendingStepOnRecovery` con un paso `RESOLVE_PENDING_TOOL`, con qué valor de
   `executionStillInFlight` llama a `decideUnknownOutcome`, y qué pasa en cada caso de
   `ReplayPolicy`? *(pregunta guía 3)*
4. ¿Por qué el turno durable no invoca `beginToolApprovalPause` ni `resumeAfterHumanResolution` de
   CH-13, y qué piezas de CH-06, CH-10 y CH-13 compone en su lugar? *(pregunta guía 4)*

### Explicar

1. `ExecutionJournal` y `ResumptionCoordinator` actúan sobre el mismo turno cuando hace falta una
   aprobación. Explica qué guarda cada uno mientras el run espera, y por qué el paso sigue abierto
   pero nada se ejecutó.
2. Explica por qué la persona que aprueba una acción no pasa a ser el llamante del turno, y qué se
   rompería si la acción se ejecutara con los permisos del aprobador.

### Conectar

1. CH-26 integró por primera vez los componentes enterprise en `runGovernedEnterpriseTurn`, pero todo
   el turno corría en un solo proceso de principio a fin. ¿Qué pasos de ese turno se vuelven durables
   en CH-36, y cuál sigue fuera del journal?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
