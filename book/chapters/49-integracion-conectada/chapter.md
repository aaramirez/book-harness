---
id: CH-49
title: "Integración: el Arnés Conectado"
starting_version: "0.2.1"
ending_version: "0.3"
introduces_components: []
introduces_contracts: []
modifies_contracts: []
constitutional_articles: [P-13, P-14, P-21, P-31, P-33, P-35, P-37, P-38, P-39, INV-E06, INV-E16, INV-E21, INV-E23, INV-E24, INV-E25, INV-E26, INV-E27]
previous_chapter: CH-48
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH49
    text: |
      Al terminar este capítulo podrás decidir en qué orden se aplican los controles de la versión 0.3
      en un turno conectado, y explicar cómo un paso retoma una respuesta con varias herramientas sin
      volver a llamar al modelo, cómo se avisa a un aprobador ausente y dónde corre una extensión de
      proyecto.
  skeleton:
    id: SK-CH49
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
    - id: GQ-CH49-01
      text: |
        Si el modelo pidió tres herramientas en una sola respuesta y el servidor se reinicia después de
        la primera, ¿debería volver a preguntarle al modelo qué hacer?
      answered_by: RQ-CH49-01
    - id: GQ-CH49-02
      text: |
        Si una acción necesita la aprobación de una supervisora que no está en la conversación, ¿cómo
        debería enterarse, y por dónde debería volver su respuesta?
      answered_by: RQ-CH49-02
    - id: GQ-CH49-03
      text: |
        Si una extensión que trajo un proyecto empieza a bloquear herramientas por error, ¿dónde debería
        haber corrido su código, y cómo se la apaga?
      answered_by: RQ-CH49-03
    - id: GQ-CH49-04
      text: |
        En un turno que usa datos, herramientas externas y otros agentes, ¿en qué orden deberían
        aplicarse la admisión, el contexto, la política, los hooks y el aislamiento?
      answered_by: RQ-CH49-04
  systems_lens:
    iceberg_visible_fact: |
      Cada capítulo de la versión 0.3 agregó una pieza con sus funciones, pero la entrada y el paso
      durables de CH-36 siguen siendo los de la versión 0.2: no usan la admisión por principal, la
      política por llamante ni las entradas pendientes, y cuatro deudas quedaron con destino a este
      capítulo (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que cada pieza se probó sola: un capítulo garantiza su invariante, pero
      nadie mostró que sigan valiendo cuando se componen en un mismo turno, en un orden que no deje
      huecos entre un control y el siguiente (ver sección 3).
    iceberg_structures: |
      Este capítulo no agrega componentes ni contratos: compone los de CH-28..CH-48 en
      enterConnectedTurn, openConnectedGovernedTurn y runConnectedGovernedStep, con ExecutionJournal
      (CMP-023) como fuente del próximo paso y ExtensionHost (CMP-027) con extensiones aisladas (ver
      sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-39 e INV-E27 (solo corre un agente sin errores de autoría), INV-E25
      (ninguna tool externa llega sin descriptor resuelto y política evaluada), INV-E16 (un paso
      confirmado no se repite), INV-E23 (las trazas se recortan por audiencia) e INV-E24 (un hook nunca
      autoriza) (ver sección 4).
    reinforcing_loop: |
      Si cada pieza se integra a su manera, cada integración nueva abre un hueco entre controles; los
      huecos se tapan con excepciones, y cada excepción hace más difícil la integración siguiente.
    balancing_loop: |
      Un orden único del turno es el equilibrio: cada control nuevo entra en un lugar fijo, y los
      invariantes de los capítulos anteriores siguen valiendo porque nada se salta su turno.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que el journal de ExecutionJournal (CMP-023)
      decida el próximo paso antes que el modelo: con eso un reinicio retoma la respuesta registrada sin
      volver a llamar al modelo, y cada propuesta pasa por los mismos controles en el mismo orden.
  recall_questions:
    - id: RQ-CH49-01
      text: |
        ¿Qué cuenta nextProposalFromJournal para decidir la próxima propuesta, qué devuelve cuando ya no
        quedan, y por qué runConnectedGovernedStep no toma entradas pendientes en ese caso?
    - id: RQ-CH49-02
      text: |
        ¿Qué exige approverNoticeFor de la espera, a qué dirección va el aviso, y por qué la respuesta no
        necesita volver por el mismo canal?
    - id: RQ-CH49-03
      text: |
        ¿Qué exige requireExtensionPlacement para una extensión PROJECT, qué hace disableExtension con una
        directiva operacional, y por qué beforeToolHooksForStep nunca selecciona una extensión DISABLED?
    - id: RQ-CH49-04
      text: |
        ¿En qué orden recorren enterConnectedTurn, openConnectedGovernedTurn y runConnectedGovernedStep
        los controles de la versión 0.3, desde el manifiesto hasta las trazas?
  explain_prompts:
    - id: EP-CH49-01
      text: |
        ExecutionJournal ya registraba cada paso. Explica, como si hablaras con alguien sin contexto
        técnico, por qué el journal debe decidir el próximo paso antes que el modelo, y qué pasaría si se
        le volviera a preguntar al modelo después de un reinicio.
      target_entity: CMP-023
    - id: EP-CH49-02
      text: |
        ExtensionHost ya decidía qué extensiones se registran. Explica por qué una extensión de proyecto
        debe correr en el entorno aislado y por qué apagarla es un comando operacional y no una decisión
        del modelo.
      target_entity: CMP-027
  interleaved_questions:
    - id: IQ-CH49-01
      text: |
        En CH-36, runDurableGovernedStep llamaba al modelo en cada paso y evaluaba la política con
        evaluatePolicyForToolCall. ¿Qué cambia en runConnectedGovernedStep en esos dos puntos, y qué
        deuda cierra cada cambio?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-023, C-042]
      prior_chapter: CH-36
  flashcards:
    - id: FC-CH49-01
      front: |
        ¿Cómo retoma un paso una respuesta con varias tool calls sin volver a llamar al modelo (D-044)?
      back: |
        nextProposalFromJournal busca el paso del turno con modelResponse, cuenta los pasos confirmados
        con toolCall y devuelve la siguiente propuesta de effectiveToolCallProposals; si no quedan, NULL
        y el paso llama al modelo.
      source_entity: C-042
      chapter_introduced_in: CH-49
      review_stage: DAY_1
    - id: FC-CH49-02
      front: |
        ¿Cómo se avisa a un aprobador que no está en la sesión (D-042)?
      back: |
        approverNoticeFor: con un aprobador designado, prepara un WAIT_NOTICE a su dirección con el waitId.
        La respuesta vuelve a la espera por su waitId, con la regla de quien responde de siempre.
      source_entity: C-044
      chapter_introduced_in: CH-49
      review_stage: DAY_1
    - id: FC-CH49-03
      front: |
        ¿Dónde corre una extensión PROJECT y cómo se la apaga (D-045)?
      back: |
        En el entorno aislado abierto de la sesión, o no corre. Se apaga con una directiva DISABLE_CAPABILITY
        cuyo targetRef es la extensión (CH-18); DISABLED ya no se selecciona.
      source_entity: C-051
      chapter_introduced_in: CH-49
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH49-01
      recall_question: RQ-CH49-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH49-02
      recall_question: RQ-CH49-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH49-03
      recall_question: RQ-CH49-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH49-04
      recall_question: RQ-CH49-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 49 — Integración: el Arnés Conectado

> **Regla de integración:** ningún control de la versión 0.3 se salta su turno. El turno conectado
> los recorre siempre en el mismo orden.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir en qué orden se aplican los controles
de la versión 0.3 en un turno conectado. También podrás explicar cómo un paso retoma una respuesta con
varias herramientas sin volver a llamar al modelo, cómo se avisa a un aprobador ausente y dónde corre
una extensión de proyecto.

**Esqueleto.** Último capítulo de la versión 0.3. No introduce componentes ni contratos: compone los de
CH-28..CH-48 y cierra las cuatro deudas que quedaban abiertas (D-041, D-042, D-044, D-045).

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si el modelo pidió tres herramientas en una sola respuesta y el servidor se reinicia después de la
   primera, ¿debería volver a preguntarle al modelo qué hacer?
2. Si una acción necesita la aprobación de una supervisora que no está en la conversación, ¿cómo
   debería enterarse, y por dónde debería volver su respuesta?
3. Si una extensión que trajo un proyecto empieza a bloquear herramientas por error, ¿dónde debería
   haber corrido su código, y cómo se la apaga?
4. En un turno que usa datos, herramientas externas y otros agentes, ¿en qué orden deberían aplicarse
   la admisión, el contexto, la política, los hooks y el aislamiento?

## 1. Arquitectura Actual (Current Architecture)

- **CH-36** integró el turno durable de la versión 0.2: `enterDurableTurn` y `runDurableGovernedStep`.
- **CH-37 y CH-38** agregaron credenciales del llamante, avisos por el canal, admisión por principal,
  política por llamante y entradas pendientes en los bordes de paso. No se cablearon en CH-36 (D-041).
- **CH-39** permitió varias propuestas de tool call por respuesta (`effectiveToolCallProposals`), pero el
  paso durable registra una (D-044).
- **CH-40** introdujo extensiones con hooks que solo restringen, y dejó el aislamiento de las
  extensiones de proyecto y su apagado para después (D-045).
- **CH-41..CH-48:** conexiones, fuentes de datos, presupuesto heredado, invocación entre agentes,
  versión del runtime, audiencia, lift y el agente como directorio.
- **CH-37** dejó el aviso a un aprobador por otro canal para este capítulo (D-042).

## 2. El Problema (Problem)

Un agente de compras, escrito como directorio, atiende en el chat de la empresa. Un usuario le pide
renovar un contrato con un proveedor. El agente necesita leer el historial del proveedor (una fuente
de datos), consultar el sistema de contratos (una conexión), pedirle una cotización a un agente de
proveedores (una invocación) y emitir la orden, que requiere la aprobación de la jefa de compras. Hoy:
- **la entrada del turno no conoce el manifiesto ni las reglas por principal** (D-041);
- **el modelo pidió tres herramientas en una respuesta;** después de la primera, el servidor se
  reinicia, y el paso siguiente vuelve a llamar al modelo (D-044);
- **la jefa de compras no está en el chat:** el aviso de la aprobación sale por el canal de la sesión,
  donde ella no lo ve (D-042);
- **una extensión del proyecto revisa cada orden,** y su código corre en el proceso del arnés (D-045).

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **Cada pieza se probó sola.** Cada capítulo garantiza su invariante, pero nadie mostró que siga
  valiendo cuando se compone con las demás.
- **El paso de CH-36 llama al modelo siempre:** no sabe leer del journal lo que todavía no se ejecutó.
- **El aviso de una espera va a la dirección de la sesión:** no hay forma de dirigirlo a quien tiene
  que responder.
- **Una extensión de proyecto es código de terceros:** correrlo en el proceso del arnés contradice el
  aislamiento de CH-35.
- **No hace falta nada nuevo:** todo lo necesario ya existe; falta componerlo en un orden fijo.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-13  La aprobación humana sigue siendo explícita: el aviso cambia de canal, no de regla.
    P-14  El contexto se selecciona, no se vuelca: governedContextBlocks.
    P-21  La autoridad delegada es explícita: la invocación entre agentes es la de CH-44.
    P-31  La identidad viaja con cada turno: enterConnectedTurn y bindDurableCaller.
    P-33  Esperar es durable: la aprobación estaciona el run.
    P-35  Los secretos no entran en cómputo controlado por el modelo: credencial del llamante vía broker.
    P-37  La captura de observabilidad está acotada por la audiencia: traceConnectedStep.
    P-38  Las capabilities externas entran por conexiones declaradas.
    P-39  El agente se escribe como archivos inspeccionables: el turno empieza por su manifiesto.

Invariants preserved
    INV-E06, INV-E21  El presupuesto de una invocación sale del saldo del padre (CH-43, CH-44).
    INV-E16  Un paso confirmado no se repite: el journal decide el próximo paso.
    INV-E23  Ninguna traza supera el techo de la audiencia.
    INV-E24  Un hook nunca autoriza: corre después de un ALLOW.
    INV-E25  Ninguna tool externa llega sin descriptor resuelto y política evaluada.
    INV-E26  Una fuente sin clasificación es RESTRICTED.
    INV-E27  Un manifiesto con ERROR no se activa.

Component ownership changes
    Ninguno. Funciones de integración, como en CH-26 y CH-36.

Contract changes
    Ninguno.

Observability implications
    Ningún AgentEventType nuevo.
```

## 5. Conceptos Nuevos (New Concepts)

- **Turno conectado:** el turno que recorre todo lo de la versión 0.3 en un orden fijo:
  1. manifiesto sin errores (CH-48);
  2. admisión por principal y propiedad de la sesión (CH-31, CH-38);
  3. llamante en el contexto de ejecución (CH-31);
  4. contexto recuperado con el techo de la audiencia (CH-42, CH-46);
  5. propuesta del journal o, si no hay, del modelo con las entradas pendientes (CH-38, CH-39);
  6. política por llamante (CH-38);
  7. aprobación, con aviso al aprobador si no está en la sesión (CH-33, CH-37);
  8. hooks que solo restringen, con extensiones de proyecto aisladas (CH-40);
  9. credencial del llamante o espera de autorización (CH-37, CH-38);
  10. ejecución aislada, por conexión o como invocación de agente (CH-35, CH-41, CH-44);
  11. commit del paso y confirmación de las entradas pendientes (CH-32, CH-38);
  12. trazas recortadas por audiencia (CH-46).
- **El journal antes que el modelo:** si la respuesta registrada del turno tiene propuestas sin
  ejecutar, el paso toma la siguiente sin llamar al modelo.
- **Aviso dirigido:** el aviso de una espera puede ir a la dirección del aprobador designado, distinta
  de la de la sesión.
- **Extensión de proyecto aislada:** su código corre en el entorno aislado de la sesión, o no corre.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Este capítulo solo compone tipos que ya existen:
- **por contrato:** `AgentManifest` (C-065), `ActivationRequest` (C-022), `AdmissionDecision`
  (C-023), `Principal` (C-040), `CallerSnapshot` (C-041), `ExecutionContext` (C-004), `AgentState`
  (C-003), `StepRecord` (C-042), `ModelResponse` (C-007), `ToolCall` (C-008), `ToolResult` (C-009),
  `PolicyDecision` (C-014), `HumanInteractionRequest` (C-015), `ParkedWait` (C-044),
  `ContinuationAddress` (C-046), `SandboxSession` (C-047), `CapabilityDescriptor` (C-018),
  `CredentialReference` (C-026), `ControlDirective`, `ExtensionRegistration` (C-051),
  `RetrievedCandidate` (C-056), `SessionAudience` (C-061), `TraceCapturePolicy` (C-062),
  `TelemetrySpan` (C-063), `SessionState` (C-020), `EventSubscription` (C-019), `HarnessError` (C-011);
- **primitivos:** `AgentId`, `CapabilityId`, `Timestamp`.

| Identificador | Rol en este capítulo |
|---|---|
| `ProcessMode` | CH-31 §6 |
| `SessionOwnershipRule` | CH-31 §6 |
| `ContinuationClaim` | CH-34 §6 |
| `ContinuationRoute` | CH-34 §6: se usa `CONTINUE_SESSION` |
| `PrincipalAdmissionRule` | CH-38 §6 |
| `CallerPolicyRule` | CH-38 §6 |
| `PendingInputQueue` | CH-28 §6 |
| `PendingInputSelection` | CH-28 §6 |
| `RawToolCallProposal` | CH-03 §6 |
| `ResponderRule` | CH-33 §6: se exige `DESIGNATED_PRINCIPAL` para el aviso dirigido |
| `ApprovalPause` | CH-13 §6 (revisión de v0.2.1) |
| `OutboundMessage` | CH-37 §6: se usa `WAIT_NOTICE` |
| `AuthorizationParking` | CH-37 §6 |
| `CredentialClassification` | CH-16 §6 |
| `HookOutcome` | CH-40 §6 |
| `ExtensionSource` | CH-40 §6: se usa `PROJECT` |
| `ExtensionStatus` | CH-40 §6: se usa `DISABLED` |
| `ControlDirectiveType` | CH-18 §6: se usa `DISABLE_CAPABILITY` |
| `ContextBlock` | CH-04 §6 |
| `DataClassificationLevel` | CH-20 §6 |
| `TraceDestination` | CH-46 §6 |
| `SpanDelivery` | CH-46 §6 |
| `ErrorCategory` | reutiliza `ADMISSION`, `POLICY`, `CONTROL` y `HUMAN_INTERACTION` |

### Resultados de integración (embebidos)

```pseudocode
STRUCT ConnectedStepOutcome
    step: StepRecord
    state: AgentState
    wait: Optional<ParkedWait>
    request: Optional<HumanInteractionRequest>
    notice: Optional<OutboundMessage>
    queue: PendingInputQueue
END
```

```pseudocode
STRUCT ConnectedCredential
    reference: Optional<CredentialReference>
    parking: Optional<AuthorizationParking>
END
```

```pseudocode
STRUCT ConnectedTurnStart
    route: ContinuationRoute
    execution: ExecutionContext
    contextBlocks: List<ContextBlock>
END
```

`ConnectedStepOutcome` es el `DurableStepOutcome` de CH-36 con dos campos más: el aviso dirigido y la
cola de entradas pendientes después del paso.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ni modifica contratos. `ConnectedStepOutcome`, `ConnectedCredential` y
`ConnectedTurnStart` quedan embebidos.

## 8. Responsabilidades de Componentes (Component Responsibilities)

**Este capítulo no introduce componentes ni cambia el `owns` de ninguno.** Las funciones son de
integración, como `runGovernedEnterpriseTurn` (CH-26) o `runDurableGovernedStep` (CH-36):

```text
Integración del turno conectado
    enterConnectedTurn          AgentCore (manifiesto) + AdmissionController + ContinuationRegistry
    openConnectedGovernedTurn   + caller + RetrievalEngine / DataGovernanceEngine / ContextEngine
    runConnectedGovernedStep    ExecutionJournal + ModelGateway + CapabilityRegistry + PolicyEngine
                                + HumanInteractionService / ResumptionCoordinator + ExtensionHost
                                + IsolatedExecutionEnvironment
    credentialForConnectedCall  CredentialBroker + ResumptionCoordinator (espera de autorización)
    traceConnectedStep          DataGovernanceEngine + EventBus

Auxiliares de integración
    nextProposalFromJournal            lee el journal (ExecutionJournal, CMP-023)
    requireExtensionPlacement,
    beforeToolHooksForStep,
    disableExtension                   sobre registros de ExtensionHost (CMP-027) y directivas de CH-18
    approverNoticeFor                  sobre una ParkedWait (CH-33) y una dirección (CH-34)
    governedContextBlocks              CH-42 + CH-46
```

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
enterConnectedTurn
    requireActivatableManifest (CH-48) → admitWithPrincipalRules (CH-38)
    → routeAdmittedRequest (CH-34) → continuationAllowedForCaller (CH-31)
openConnectedGovernedTurn
    → bindDurableCaller (CH-36) → governedContextBlocks
        → governRetrievedCandidate (CH-42) → contextCeilingForAudience (CH-46)
        → selectRetrievedCandidates (CH-42)
runConnectedGovernedStep (por paso; el bucle es de AgentLoop, CH-01)
    beginStep (CH-32) → nextProposalFromJournal
        hay propuesta → resolveToolCall (CH-08)
        no hay        → takePendingInputsForStep (CH-38) → invokeModelForTurn (CH-03)
                        → recordModelResponse → effectiveToolCallProposals (CH-39)
    → evaluatePolicyForCaller (CH-38)
        DENY             → tool call registrada como fallida (POLICY_DENIED) → commit
        REQUIRE_APPROVAL → beginToolApprovalPauseForDecision (CH-13) → parkRun (CH-33)
                           → approverNoticeFor (si hay dirección del aprobador)
        ALLOW            → beforeToolHooksForStep → runBeforeToolHooks (CH-40)
                           → recordToolCallBeforeExecution → executeToolCallIsolated (CH-35)
                           → recordToolResult → commitStep (CH-32)
    → confirmPendingInputsAfterCommit (CH-38) si se tomaron entradas
Herramienta de conexión: credentialForConnectedCall antes de ejecutar; prepareConnectionCall (CH-41)
Herramienta de agente:   invokeAgentDurably (CH-44) en lugar de executeToolCallIsolated
Después de cada paso:    traceConnectedStep → captureCeilingFor → fanOutSpan (CH-46)
Operación:               disableExtension ← ControlDirective DISABLE_CAPABILITY (CH-18)
```

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
manifiesto → admisión → llamante → contexto (techo de audiencia)
→ journal o modelo → política por llamante → aprobación | hooks aislados → ejecución aislada
→ commit → trazas recortadas
```

**Vista 2 — Sequence: la renovación del contrato**

```text
enterConnectedTurn: manifiesto sin ERROR, principal admitido, sesión del chat (PUBLIC)
openConnectedGovernedTurn: historial del proveedor (CONFIDENTIAL) → techo de contexto INTERNAL
   → entra solo el resumen INTERNAL
paso 1: modelo → 3 propuestas (contratos.buscar, cotizar-proveedor, emitir-orden)
   │ contratos.buscar: política ALLOW, hook del proyecto en el entorno aislado, credencial del llamante
   │ commit
   ▼ el servidor se reinicia
paso 2: nextProposalFromJournal → cotizar-proveedor (sin llamar al modelo)
   │ invokeAgentDurably (CH-44), presupuesto desde el saldo; commit
paso 3: nextProposalFromJournal → emitir-orden → REQUIRE_APPROVAL
   │ parkRun (aprobadora designada) → approverNoticeFor → WAIT_NOTICE a la dirección de la jefa
   ▼ la jefa responde por su canal → la espera se resuelve por waitId (CH-33)
cada paso → traceConnectedStep → trazas sin el contenido CONFIDENTIAL
```

**Vista 2b — Sequence: apagar una extensión**

```text
la extensión del proyecto bloquea órdenes por error
operador → issueControlDirective(DISABLE_CAPABILITY, "revisor-ordenes") → applyControlDirective (CH-18)
disableExtension → status DISABLED → beforeToolHooksForStep ya no la selecciona
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

### Entrada y apertura del turno (D-041)

```pseudocode
FUNCTION enterConnectedTurn(
    manifest: AgentManifest,
    request: ActivationRequest,
    verifiedPrincipal: Optional<Principal>,
    admissionConfigured: Boolean,
    processMode: ProcessMode,
    principalRules: List<PrincipalAdmissionRule>,
    claims: List<ContinuationClaim>,
    ownerSnapshot: Optional<CallerSnapshot>,
    ownershipRule: SessionOwnershipRule,
    execution: ExecutionContext,
    agentId: AgentId
) -> Optional<ContinuationRoute>

    requireActivatableManifest(manifest, execution, agentId)

    admission: AdmissionDecision = admitWithPrincipalRules(
        request, verifiedPrincipal, admissionConfigured, processMode, principalRules
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
            message = "El estímulo fue admitido, pero la regla de propiedad no permite que este llamante continúe la sesión",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN route
END
```

```pseudocode
FUNCTION governedContextBlocks(
    candidates: List<RetrievedCandidate>,
    audience: SessionAudience,
    policyCeiling: DataClassificationLevel,
    publicCeiling: DataClassificationLevel,
    tokenBudget: Integer,
    legalHold: Boolean,
    execution: ExecutionContext,
    agentId: AgentId
) -> List<ContextBlock>

    governed: List<RetrievedCandidate> = []

    FOR EACH candidate IN candidates
        governed = append(governed, governRetrievedCandidate(candidate, legalHold, execution, agentId))
    END

    ceiling: DataClassificationLevel = contextCeilingForAudience(audience, policyCeiling, publicCeiling)

    RETURN selectRetrievedCandidates(governed, ceiling, tokenBudget)
END
```

```pseudocode
FUNCTION openConnectedGovernedTurn(
    route: ContinuationRoute,
    execution: ExecutionContext,
    principal: Principal,
    candidates: List<RetrievedCandidate>,
    audience: SessionAudience,
    policyCeiling: DataClassificationLevel,
    publicCeiling: DataClassificationLevel,
    tokenBudget: Integer,
    legalHold: Boolean,
    agentId: AgentId
) -> ConnectedTurnStart

    bound: ExecutionContext = bindDurableCaller(execution, principal)

    RETURN ConnectedTurnStart(
        route = route,
        execution = bound,
        contextBlocks = governedContextBlocks(
            candidates, audience, policyCeiling, publicCeiling, tokenBudget, legalHold, bound, agentId
        )
    )
END
```

### El journal antes que el modelo (D-044)

```pseudocode
FUNCTION nextProposalFromJournal(
    steps: List<StepRecord>,
    turn: Integer
) -> Optional<RawToolCallProposal>

    response: Optional<ModelResponse> = NULL
    executed: Integer = 0

    FOR EACH step IN steps
        IF step.turn == turn AND step.status == COMMITTED
            IF step.modelResponse != NULL
                response = step.modelResponse
            END
            IF step.toolCall != NULL
                executed = executed + 1
            END
        END
    END

    IF response == NULL
        RETURN NULL
    END

    proposals: List<RawToolCallProposal> = effectiveToolCallProposals(response)

    IF executed >= length(proposals)
        RETURN NULL
    END

    RETURN elementAt(proposals, executed)
END
```

### Extensiones de proyecto aisladas y apagables (D-045)

```pseudocode
FUNCTION requireExtensionPlacement(
    registration: ExtensionRegistration,
    sandbox: Optional<SandboxSession>
) -> ExtensionRegistration

    IF registration.source == PROJECT AND (sandbox == NULL OR sandbox.status != OPEN)
        THROW HarnessError(
            category = POLICY,
            code = "PROJECT_EXTENSION_REQUIRES_SANDBOX",
            message = "El código de una extensión de proyecto corre en el entorno aislado de la sesión, o no corre",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN registration
END
```

```pseudocode
FUNCTION beforeToolHooksForStep(
    registrations: List<ExtensionRegistration>,
    sandbox: Optional<SandboxSession>
) -> List<ExtensionRegistration>

    selected: List<ExtensionRegistration> = hooksFor(registrations, BEFORE_TOOL)

    FOR EACH registration IN selected
        requireExtensionPlacement(registration, sandbox)
    END

    RETURN selected
END
```

```pseudocode
FUNCTION disableExtension(
    registration: ExtensionRegistration,
    directive: ControlDirective
) -> ExtensionRegistration

    IF directive.type != DISABLE_CAPABILITY OR directive.targetRef != registration.extensionId
        THROW HarnessError(
            category = CONTROL,
            code = "DIRECTIVE_NOT_FOR_EXTENSION",
            message = "Solo una directiva DISABLE_CAPABILITY dirigida a esta extensión la apaga",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN ExtensionRegistration(
        extensionId = registration.extensionId,
        version = registration.version,
        source = registration.source,
        sourceRef = registration.sourceRef,
        contentHash = registration.contentHash,
        hookPoints = registration.hookPoints,
        capabilities = registration.capabilities,
        trustDecisionId = registration.trustDecisionId,
        status = DISABLED,
        registeredAt = registration.registeredAt
    )
END
```

### Aviso al aprobador por su canal (D-042)

```pseudocode
FUNCTION approverNoticeFor(
    wait: ParkedWait,
    request: HumanInteractionRequest,
    approverAddress: ContinuationAddress
) -> OutboundMessage

    IF wait.responderRule != DESIGNATED_PRINCIPAL OR wait.designatedResponder == NULL
        THROW HarnessError(
            category = HUMAN_INTERACTION,
            code = "APPROVER_NOT_DESIGNATED",
            message = "Un aviso dirigido exige una espera con aprobador designado",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN OutboundMessage(
        address = approverAddress,
        sessionId = wait.sessionId,
        kind = WAIT_NOTICE,
        content = request,
        waitId = wait.waitId,
        preparedAt = now()
    )
END
```

### Credencial del llamante para una herramienta de conexión (CH-37 + CH-38)

```pseudocode
FUNCTION credentialForConnectedCall(
    descriptor: CapabilityDescriptor,
    credentialName: Text,
    classification: CredentialClassification,
    credentialBelongsToCapability: Boolean,
    secretExistsForCaller: Boolean,
    expiresAt: Optional<Timestamp>,
    state: AgentState,
    connectionRef: Text,
    challengeExpiresAt: Timestamp,
    claims: List<ContinuationClaim>,
    execution: ExecutionContext,
    agentId: AgentId
) -> ConnectedCredential

    IF detectMissingCallerCredential(descriptor, credentialName, execution, secretExistsForCaller)
        RETURN ConnectedCredential(
            reference = NULL,
            parking = parkForMissingCredential(state, execution, connectionRef, challengeExpiresAt, claims)
        )
    END

    RETURN ConnectedCredential(
        reference = resolveCallerCredentialReference(
            descriptor, credentialName, classification, credentialBelongsToCapability,
            secretExistsForCaller, expiresAt, execution, agentId
        ),
        parking = NULL
    )
END
```

### El paso conectado (D-041)

```pseudocode
FUNCTION runConnectedGovernedStep(
    state: AgentState,
    execution: ExecutionContext,
    steps: List<StepRecord>,
    previousStep: Optional<StepRecord>,
    turn: Integer,
    index: Integer,
    queue: PendingInputQueue,
    providerFinished: Boolean,
    providerProposesToolCall: Boolean,
    providerCapabilityName: Text,
    providerRawArguments: Map<Text, Value>,
    providerContent: Value,
    registeredCapabilities: List<CapabilityDescriptor>,
    argumentsMatchSchema: Boolean,
    callerRules: List<CallerPolicyRule>,
    approvalRule: ResponderRule,
    designatedApprover: Optional<Principal>,
    approvalExpiresAt: Optional<Timestamp>,
    approverAddress: Optional<ContinuationAddress>,
    extensions: List<ExtensionRegistration>,
    hookOutcomes: List<HookOutcome>,
    sandbox: Optional<SandboxSession>,
    isolatedCapabilities: List<CapabilityId>,
    toolExecutionSucceeded: Boolean,
    toolExecutionOutput: Value,
    resultPersisted: Boolean,
    session: Optional<SessionState>,
    activeSubscriptions: List<EventSubscription>
) -> ConnectedStepOutcome

    IF execution.caller == NULL
        THROW HarnessError(
            category = ADMISSION,
            code = "DURABLE_TURN_WITHOUT_CALLER",
            message = "Un turno conectado necesita el llamante verificado en su ExecutionContext",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    step: StepRecord = beginStep(execution.runId, turn, index, previousStep)
    proposal: Optional<RawToolCallProposal> = nextProposalFromJournal(steps, turn)
    selection: Optional<PendingInputSelection> = NULL

    IF proposal == NULL
        selection = takePendingInputsForStep(queue, state, execution)

        response: ModelResponse = invokeModelForTurn(
            state, execution, selection.messages, TRUE, providerFinished, providerProposesToolCall,
            providerCapabilityName, providerRawArguments, providerContent
        )
        emitAndDistribute(MODEL_RESPONSE_RECEIVED, execution, state.agentId, response, activeSubscriptions)
        step = recordModelResponse(step, response)

        proposals: List<RawToolCallProposal> = effectiveToolCallProposals(response)

        IF length(proposals) == 0
            finished: StepRecord = commitStep(step, resultPersisted, execution, state.agentId)
            RETURN ConnectedStepOutcome(
                step = finished, state = state, wait = NULL, request = NULL, notice = NULL,
                queue = confirmPendingInputsAfterCommit(queue, selection, finished)
            )
        END

        proposal = elementAt(proposals, 0)
    END

    call: ToolCall = resolveToolCall(proposal, registeredCapabilities, execution, state.agentId, argumentsMatchSchema)
    decision: PolicyDecision = evaluatePolicyForCaller(call, execution, state.agentId, callerRules)
    emitAndDistribute(POLICY_EVALUATED, execution, state.agentId, decision, activeSubscriptions)

    IF decision.outcome == REQUIRE_APPROVAL
        pause: ApprovalPause = beginToolApprovalPauseForDecision(
            state, execution, decision, session, activeSubscriptions
        )
        wait: ParkedWait = parkRun(
            pause.pausedState, TOOL_APPROVAL, pause.request.id, NULL, execution.caller.current,
            approvalRule, designatedApprover, approvalExpiresAt, execution
        )
        linked: HumanInteractionRequest = linkRequestToWait(pause.request, wait)

        notice: Optional<OutboundMessage> = NULL
        IF approverAddress != NULL
            notice = approverNoticeFor(wait, linked, approverAddress)
        END

        RETURN ConnectedStepOutcome(
            step = step, state = pause.pausedState, wait = wait, request = linked, notice = notice,
            queue = queue
        )
    END

    blocked: Optional<HarnessError> = HarnessError(
        category = POLICY,
        code = "POLICY_DENIED",
        message = "PolicyEngine denegó esta tool call",
        recoverable = TRUE,
        retryable = FALSE,
        metadata = {}
    )

    IF decision.outcome == ALLOW
        blocked = runBeforeToolHooks(
            call, decision, beforeToolHooksForStep(extensions, sandbox), hookOutcomes, execution, state.agentId
        )
    END

    step = recordToolCallBeforeExecution(step, call)

    result: ToolResult = ToolResult(
        callId = call.id, succeeded = FALSE, outcome = NULL, output = NULL,
        error = blocked, completedAt = now()
    )

    IF blocked == NULL
        result = executeToolCallIsolated(
            call, sandbox, isolatedCapabilities, execution, state.agentId,
            TRUE, TRUE, toolExecutionSucceeded, toolExecutionOutput
        )
    END

    step = recordToolResult(step, result)
    done: StepRecord = commitStep(step, resultPersisted, execution, state.agentId)

    IF selection == NULL
        RETURN ConnectedStepOutcome(
            step = done, state = state, wait = NULL, request = NULL, notice = NULL, queue = queue
        )
    END

    RETURN ConnectedStepOutcome(
        step = done, state = state, wait = NULL, request = NULL, notice = NULL,
        queue = confirmPendingInputsAfterCommit(queue, selection, done)
    )
END
```

### Trazas del paso

```pseudocode
FUNCTION traceConnectedStep(
    span: TelemetrySpan,
    audience: SessionAudience,
    policies: List<TraceCapturePolicy>,
    destinations: List<TraceDestination>
) -> List<SpanDelivery>

    RETURN fanOutSpan(span, captureCeilingFor(audience, policies), destinations)
END
```

Utilidades primitivas: `append`, `length`, `elementAt` (el elemento en una posición de una lista,
empezando en 0) y `now`. `emitAndDistribute` es la de CH-26.

Funciones de capítulos anteriores que se usan sin cambios: `requireActivatableManifest` (CH-48),
`admitWithPrincipalRules` y `evaluatePolicyForCaller` (CH-38), `routeAdmittedRequest` (CH-34),
`continuationAllowedForCaller` (CH-31), `bindDurableCaller` (CH-36), `governRetrievedCandidate` y
`selectRetrievedCandidates` (CH-42), `contextCeilingForAudience`, `captureCeilingFor` y `fanOutSpan`
(CH-46), `effectiveToolCallProposals` (CH-39), `resolveToolCall` (CH-08), `invokeModelForTurn` (CH-03),
`beginStep`, `recordModelResponse`, `recordToolCallBeforeExecution`, `recordToolResult` y `commitStep`
(CH-32), `takePendingInputsForStep` y `confirmPendingInputsAfterCommit` (CH-38),
`beginToolApprovalPauseForDecision` (CH-13), `parkRun` y `linkRequestToWait` (CH-33), `hooksFor` y
`runBeforeToolHooks` (CH-40), `executeToolCallIsolated` (CH-35), `detectMissingCallerCredential` y
`parkForMissingCredential` (CH-37), `resolveCallerCredentialReference` (CH-38).

**Por qué una tool call denegada o bloqueada también se registra:** el journal dice que la tool call
se decidió y que no se ejecutó, con el error de la política o del hook, y el modelo lo recibe como
observación (INV-07). Si no se registrara, `nextProposalFromJournal` no la contaría y la volvería a
ofrecer en cada paso; registrada, el paso confirmado cuenta como resuelto (INV-E16).

**Por qué la rama de conexión y la de agente no están dentro del paso:** son las de CH-41 y CH-44 sin
cambios. Para una herramienta de conexión, `credentialForConnectedCall` y `prepareConnectionCall`
van antes de ejecutar; si hace falta autorización, el paso termina con la espera de autorización de
CH-37. Para una herramienta de agente, `invokeAgentDurably` reemplaza a `executeToolCallIsolated`. El
orden de los controles es el mismo.

Nótese lo que este capítulo **no** hace:
- no agrega componentes, contratos ni eventos;
- no cambia ninguna función de un capítulo anterior: las nuevas las componen;
- no decide cuándo termina el turno: eso sigue siendo de `AgentLoop` (CH-01).

## 12. Transiciones de Estado (State Transitions)

`AgentRunStatus` no cambia. Un paso conectado:

```text
inicio de paso
    hay propuesta pendiente en el journal → resolverla (sin modelo, sin entradas pendientes)
    no hay → entradas pendientes → modelo
        sin propuestas → commit (fin del turno para AgentLoop)
política
    DENY             → tool call registrada como fallida (POLICY_DENIED) → commit
    REQUIRE_APPROVAL → run estacionado (WAITING_FOR_HUMAN), aviso dirigido si hay dirección
    ALLOW            → hooks → bloqueado: tool call fallida | permitido: ejecución aislada → commit

Extensión
    ACTIVE → DISABLED (directiva DISABLE_CAPABILITY dirigida a ella)
```

## 13. Semántica de Fallos (Failure Semantics)

Códigos nuevos de `HarnessError`, con `ErrorCategory` ya existentes:

```text
POLICY             PROJECT_EXTENSION_REQUIRES_SANDBOX  recoverable: FALSE, retryable: FALSE
CONTROL            DIRECTIVE_NOT_FOR_EXTENSION         recoverable: FALSE, retryable: FALSE
HUMAN_INTERACTION  APPROVER_NOT_DESIGNATED             recoverable: FALSE, retryable: FALSE
```

Se reutilizan `SESSION_CONTINUATION_NOT_ALLOWED` y `DURABLE_TURN_WITHOUT_CALLER` (CH-36),
`AGENT_MANIFEST_HAS_ERRORS` (CH-48), `EXTENSION_BLOCKED_TOOL` (CH-40) y `POLICY_DENIED` (CH-05).

- **Una extensión de proyecto sin entorno aislado** detiene el paso antes de ejecutar nada: la sesión
  abre su entorno (CH-35) o la extensión se apaga.
- **Un fallo a mitad de una respuesta con varias propuestas** se recupera con las reglas de CH-32 y
  CH-36 para el paso abierto. Después, `nextProposalFromJournal` sigue con la propuesta siguiente.

## 14. Eventos Producidos (Events Produced)

Este capítulo no agrega `AgentEventType`. Los eventos del turno son los de los capítulos que compone,
entre ellos `MODEL_RESPONSE_RECEIVED`, `POLICY_EVALUATED`, `RUN_PARKED`, `TOOL_CALL_COMPLETED`,
`TOOL_CALL_FAILED`, `AGENT_INVOCATION_OPENED` y `AGENT_MANIFEST_REJECTED`.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **Ningún control se salta su turno:** el orden es fijo, y cada función nueva compone las de los
  capítulos anteriores sin cambiarlas.
- **Un reinicio no le da al modelo otra oportunidad de proponer:** las propuestas registradas se
  ejecutan en orden, cada una con su política.
- **Un aviso dirigido no le da a nadie más derecho a responder:** la regla de la espera es la misma.
- **El código de terceros corre aislado:** una extensión de proyecto sin entorno aislado no corre.
- **Apagar una extensión no depende del modelo ni de la extensión:** es un comando operacional.
- **Lo confidencial no sale por un canal público ni por las trazas:** techos de contexto y de captura
  por audiencia.

## 16. Tests (Tests)

```text
TEST ManifestWithErrorsStopsTheTurnBeforeAdmission
TEST AdmissionUsesPrincipalRules
TEST ContextCeilingFollowsTheAudience
TEST JournalProposalSkipsTheModelCall
TEST JournalReturnsNullWhenAllProposalsRan
TEST PendingInputsAreTakenOnlyBeforeAModelCall
TEST CallerPolicyRulesApply
TEST ApprovalNoticeGoesToTheDesignatedApproversAddress
TEST NoticeWithoutDesignatedApproverIsRejected
TEST ProjectExtensionWithoutSandboxIsRejected
TEST DisabledExtensionIsNotSelected
TEST DirectiveForAnotherExtensionIsRejected
TEST HookBlockedToolCallIsJournaledAsFailed
TEST MissingCallerCredentialParksForAuthorization
TEST SpansAreCappedByAudience
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness v0.3 (después de CH-49) — 29 componentes, 66 contratos, 50 capítulos

Components — 29 (22 hasta CH-27; CMP-023..026 en v0.2; CMP-027..029 en v0.3)
Contracts — 66 (35 hasta CH-27; C-036..C-048 en v0.2; C-049..C-066 en v0.3)

Deuda: D-041, D-042, D-044 y D-045 resueltas. registry/debt.yaml queda sin deudas abiertas.
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El bucle de pasos del turno:** sigue siendo de `AgentLoop` (CH-01); este capítulo compone un paso.
  No es deuda.
- **Ejecutar varias propuestas de una respuesta en paralelo:** el journal las ejecuta en orden, una por
  paso; ejecutarlas en paralelo exigiría un paso con varias tool calls, que es otro contrato. No es
  deuda.
- **El directorio de direcciones de los aprobadores:** quién es la aprobadora y dónde se la encuentra
  es configuración del despliegue; este capítulo recibe la dirección. No es deuda.
- **Lo que viene después de la versión 0.3:** se planea en un plan maestro nuevo. No es deuda.

## 19. Siguiente Incremento (Next Increment)

Con este capítulo, la versión 0.3 queda completa: el arnés conoce sus modelos como datos, se extiende
sin perder el control, se conecta a herramientas y datos externos, reparte presupuesto, invoca otros
agentes, evoluciona con sesiones abiertas, observa sin exponer, mide sus cambios y se escribe como un
directorio. Y no queda ninguna deuda abierta.

El siguiente paso no es un capítulo: es el **cierre de la versión 0.3**, con su revisión, su
aprobación y su etiqueta. Lo que venga después se planeará en un plan maestro nuevo.

`next_chapter` queda en `null` porque no hay un capítulo siguiente planeado.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): la entrada y el paso durables siguen siendo los de la versión 0.2, y
   cuatro deudas esperan este capítulo.
2. **Patrones** (= §3): cada pieza se probó sola; falta mostrar que los invariantes valen juntos.
3. **Estructuras** (= §8): funciones de integración que componen lo existente, con el journal como
   fuente del próximo paso.
4. **Modelos mentales** (= §4): P-39, INV-E27, INV-E25, INV-E16, INV-E23 e INV-E24.

**Bucles de retroalimentación**

- **Refuerzo:** cada integración a su manera abre huecos que se tapan con excepciones.
- **Equilibrio:** un orden único del turno. Cada control entra en un lugar fijo.

**Punto de apalancamiento**

La decisión con mayor efecto es que el journal de `ExecutionJournal` (CMP-023) decida el próximo paso
antes que el modelo: un reinicio retoma la respuesta registrada y cada propuesta pasa por los mismos
controles.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Qué cuenta `nextProposalFromJournal` para decidir la próxima propuesta, qué devuelve cuando ya no
   quedan, y por qué `runConnectedGovernedStep` no toma entradas pendientes en ese caso?
   *(pregunta guía 1)*
2. ¿Qué exige `approverNoticeFor` de la espera, a qué dirección va el aviso, y por qué la respuesta no
   necesita volver por el mismo canal? *(pregunta guía 2)*
3. ¿Qué exige `requireExtensionPlacement` para una extensión PROJECT, qué hace `disableExtension` con
   una directiva operacional, y por qué `beforeToolHooksForStep` nunca selecciona una extensión
   DISABLED? *(pregunta guía 3)*
4. ¿En qué orden recorren `enterConnectedTurn`, `openConnectedGovernedTurn` y
   `runConnectedGovernedStep` los controles de la versión 0.3, desde el manifiesto hasta las trazas?
   *(pregunta guía 4)*

### Explicar

1. `ExecutionJournal` ya registraba cada paso. Explica por qué el journal debe decidir el próximo paso
   antes que el modelo, y qué pasaría si se le volviera a preguntar al modelo después de un reinicio.
2. `ExtensionHost` ya decidía qué extensiones se registran. Explica por qué una extensión de proyecto
   debe correr en el entorno aislado y por qué apagarla es un comando operacional y no una decisión del
   modelo.

### Conectar

1. En CH-36, `runDurableGovernedStep` llamaba al modelo en cada paso y evaluaba la política con
   `evaluatePolicyForToolCall`. ¿Qué cambia en `runConnectedGovernedStep` en esos dos puntos, y qué
   deuda cierra cada cambio?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
