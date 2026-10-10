---
id: CH-44
title: "Invocación Durable entre Agentes y A2A"
starting_version: "0.2.1"
ending_version: "0.3"
introduces_components: []
introduces_contracts: [C-058, C-059]
modifies_contracts: [C-024]
constitutional_articles: [P-18, P-19, P-20, P-21, INV-E03, INV-E04, INV-E05, INV-E06, INV-E21]
previous_chapter: CH-43
next_chapter: CH-45
retrieval_set:
  expected_outcome:
    id: EO-CH44
    text: |
      Al terminar este capítulo podrás decidir cómo un agente invoca a otro, dentro del arnés o afuera,
      sin repetir la invocación después de un reinicio, y explicar qué identidad, qué presupuesto y qué
      esperas cruzan la frontera entre los dos.
  skeleton:
    id: SK-CH44
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
    contracts_to_be_introduced: [C-058, C-059]
  guiding_questions:
    - id: GQ-CH44-01
      text: |
        Si el servidor se reinicia mientras un agente espera la respuesta de otro al que le delegó una
        tarea, ¿qué debería pasar al volver: pedírsela de nuevo, o retomar la que ya estaba en curso?
      answered_by: RQ-CH44-01
    - id: GQ-CH44-02
      text: |
        Si el agente en el que se delegó necesita preguntarle algo al usuario, ¿por dónde debería
        llegarle la pregunta al usuario, que solo habla con el primer agente?
      answered_by: RQ-CH44-02
    - id: GQ-CH44-03
      text: |
        ¿Debería un agente de otra organización saber quién es el usuario que originó la tarea? ¿Y uno
        del mismo arnés?
      answered_by: RQ-CH44-03
    - id: GQ-CH44-04
      text: |
        ¿Qué impide que un agente delegue en otro, que delega en otro, que delega en otro, sin fin?
      answered_by: RQ-CH44-04
  systems_lens:
    iceberg_visible_fact: |
      Un agente puede enviarle un AgentCommunicationMessage a otro, pero ese mensaje no tiene dueño ni
      estado: si el servidor se reinicia, nadie sabe si el otro agente ya estaba trabajando, sus
      preguntas al usuario no tienen por dónde salir y no hay regla sobre qué identidad cruza (ver
      sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que CH-15 resolvió si un mensaje puede cruzar la frontera, pero no qué
      pasa con el trabajo que ese mensaje inicia: sin un registro durable, cada integración inventa su
      propio seguimiento, y la recuperación de un paso (CH-32) vuelve a invocar al otro agente (ver
      sección 3).
    iceberg_structures: |
      Este capítulo introduce AgentInvocation (C-058) y AgentCard (C-059), lleva
      AgentCommunicationMessage (C-024) a v2 con invocationId, y le da a AgentCommunicationGateway la
      apertura, la actualización y la exposición de esperas de una invocación (ver sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-20 (delegar adentro no es federar afuera), P-21 (la autoridad delegada
      es explícita y mínima), INV-E05 (A2A es una opción externa, no una dependencia del núcleo) e
      INV-E06 con INV-E21 (la delegación queda acotada por el presupuesto del padre) (ver sección 4).
    reinforcing_loop: |
      Si recuperar un paso vuelve a invocar al otro agente, cada reinicio lanza un hijo más; cada hijo
      gasta y puede a su vez delegar, así que los reinicios multiplican el trabajo y el gasto. Derivar el
      id de la invocación del paso corta esa espiral.
    balancing_loop: |
      La profundidad y el saldo son el equilibrio: cada nivel de delegación suma uno a depth y recibe
      solo una parte del saldo del padre, así que la cadena se detiene por maxDepth o por falta de saldo.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que AgentInvocation (C-058) sea un registro con id
      derivado del paso que la abrió: con eso la invocación sobrevive a un reinicio sin repetirse, tiene
      dueño y presupuesto, y puede exponer las esperas del hijo en el canal del padre.
  recall_questions:
    - id: RQ-CH44-01
      text: |
        ¿De qué se deriva el id de una AgentInvocation, y qué hace invokeAgentDurably cuando recibe una
        invocación existente con ese mismo id?
    - id: RQ-CH44-02
      text: |
        ¿Qué hace surfaceChildWait con la espera de un hijo interno, a qué estado pasa la invocación según
        el tipo de espera, y adónde va la respuesta del usuario?
    - id: RQ-CH44-03
      text: |
        ¿Qué devuelve forwardedCallerFor para un agente interno y para uno externo, y con qué se
        autentica el arnés ante un agente externo?
    - id: RQ-CH44-04
      text: |
        ¿Qué dos límites acotan una cadena de delegaciones, y qué funciones los hacen cumplir?
  explain_prompts:
    - id: EP-CH44-01
      text: |
        AgentCommunicationGateway ya decidía si un mensaje puede cruzar hacia otro agente. Explica, como
        si hablaras con alguien sin contexto técnico, por qué también le pertenece seguir el trabajo que
        ese mensaje inicia, y por qué A2A queda como un adaptador suyo.
      target_entity: CMP-013
    - id: EP-CH44-02
      text: |
        Explica por qué una invocación entre agentes necesita ser un registro con dueño, estado y
        presupuesto, y no basta con un mensaje de ida y otro de vuelta.
      target_entity: C-058
  interleaved_questions:
    - id: IQ-CH44-01
      text: |
        En CH-15, authorizeAgentCommunicationMessage verificaba que un DelegationGrant siguiera vigente y
        cubriera el mensaje. ¿Qué agrega invokeAgentDurably antes y después de esa verificación, y de qué
        campo del DelegationGrant sale el presupuesto de la invocación?
      current_chapter_entities: [C-058]
      prior_chapter_entities: [C-024, C-025, CMP-013]
      prior_chapter: CH-15
  flashcards:
    - id: FC-CH44-01
      front: |
        ¿Qué es AgentInvocation (C-058)?
      back: |
        El registro durable de una invocación entre agentes: dueño, agente y skill, profundidad,
        presupuesto, estado (WORKING, INPUT_REQUIRED, AUTHORIZATION_REQUIRED, COMPLETED, FAILED,
        CANCELLED) y espera pendiente. Su id se deriva del paso que la abrió.
      source_entity: C-058
      chapter_introduced_in: CH-44
      review_stage: DAY_1
    - id: FC-CH44-02
      front: |
        ¿Qué es AgentCard (C-059) y qué exige para un agente externo?
      back: |
        Lo que un agente anuncia que sabe hacer (skills) y cómo se lo invoca. Uno externo debe declarar
        endpointRef y authScheme; uno interno no tiene endpoint.
      source_entity: C-059
      chapter_introduced_in: CH-44
      review_stage: DAY_1
    - id: FC-CH44-03
      front: |
        ¿Qué agrega AgentCommunicationMessage v2 (C-024)?
      back: |
        invocationId, opcional: el mensaje pertenece a una invocación durable. NULL es un mensaje suelto,
        como en v1.
      source_entity: C-024
      chapter_introduced_in: CH-44
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH44-01
      recall_question: RQ-CH44-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH44-02
      recall_question: RQ-CH44-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH44-03
      recall_question: RQ-CH44-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH44-04
      recall_question: RQ-CH44-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 44 — Invocación Durable entre Agentes y A2A

> **Regla constitucional (P-20):** delegar dentro del arnés y federar con un agente externo son
> asuntos distintos, aunque compartan el mismo registro de invocación.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir cómo un agente invoca a otro, dentro
del arnés o afuera, sin repetir la invocación después de un reinicio. También podrás explicar qué
identidad, qué presupuesto y qué esperas cruzan la frontera entre los dos.

**Esqueleto.** Sexto capítulo de la versión 0.3 y el único multi-agente. No introduce componentes:
agrega `AgentInvocation` y `AgentCard`, lleva `AgentCommunicationMessage` a v2 y amplía
`AgentCommunicationGateway`.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si el servidor se reinicia mientras un agente espera la respuesta de otro al que le delegó una
   tarea, ¿qué debería pasar al volver: pedírsela de nuevo, o retomar la que ya estaba en curso?
2. Si el agente en el que se delegó necesita preguntarle algo al usuario, ¿por dónde debería llegarle
   la pregunta al usuario, que solo habla con el primer agente?
3. ¿Debería un agente de otra organización saber quién es el usuario que originó la tarea? ¿Y uno del
   mismo arnés?
4. ¿Qué impide que un agente delegue en otro, que delega en otro, que delega en otro, sin fin?

## 1. Arquitectura Actual (Current Architecture)

- **`AgentCommunicationGateway` (CMP-013, CH-15)** es la frontera entre agentes.
  `authorizeAgentCommunicationMessage` verifica que el `DelegationGrant` (C-025) que respalda un
  `AgentCommunicationMessage` (C-024) siga vigente, corresponda y cubra el mensaje.
- **El mensaje es suelto:** no pertenece a ningún trabajo con estado.
- **`ExecutionController` (CH-43)** ya reparte el saldo del padre (`allocateChildBudget`), verifica
  que un hijo no lo exceda (`requireChildWithinParent`) y suma su gasto al padre (`rollUpChildUsage`).
- **Pasos durables (CH-32):** un paso que quedó abierto se recupera después de un reinicio.
- **Esperas durables (CH-33):** un run se estaciona en una `ParkedWait` (C-044) y la respuesta llega
  por el canal de su sesión (CH-34, CH-37).
- **Identidad (CH-31):** cada run lleva un `CallerSnapshot` (C-041) con quien lo inició y quien lo
  continúa. Reenviarlo a otro agente quedó como deuda (D-020).

## 2. El Problema (Problem)

Un agente de compras recibe la pregunta de un usuario y delega dos tareas: una cotización en un agente
de proveedores del mismo arnés y una verificación de crédito en un agente de un banco, que habla A2A.
Hoy:
- **si el servidor se reinicia,** el paso que delegó se recupera y vuelve a delegar: el agente de
  proveedores recibe la tarea dos veces;
- **nadie sabe en qué estado está cada tarea:** el mensaje se envió, y nada más;
- **si el agente de proveedores necesita preguntarle algo al usuario,** su pregunta no tiene por dónde
  salir: el usuario habla con el agente de compras (D-023);
- **no hay regla sobre la identidad:** ¿recibe el banco el identificador del usuario? ¿Y el agente de
  proveedores? (D-020);
- **una cadena de delegaciones no tiene fondo explícito,** más allá de lo que alcance el saldo.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **CH-15 resolvió si un mensaje puede cruzar, no qué pasa con el trabajo que inicia.** Sin un
  registro con dueño y estado, cada integración inventa su propio seguimiento.
- **La recuperación de un paso no tiene cómo reconocer una invocación ya hecha.** Necesita un id
  estable que se pueda volver a calcular.
- **Una espera del hijo vive en la sesión del hijo,** y el canal es de la sesión del padre.
- **El protocolo externo no puede ser el modelo:** si los estados del arnés fueran los de A2A, el
  núcleo dependería de A2A, y INV-E05 lo prohíbe.
- **No hace falta un componente nuevo:** la frontera entre agentes ya es de
  `AgentCommunicationGateway` (P-18..P-21, EVO-01).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-18   Communication semantics are independent from protocol and transport.
           AgentInvocation es del arnés; A2A se traduce en el adaptador.
    P-19   External agent interoperability is adapter-based.
           Un AgentCard externo declara endpoint y esquema; el adaptador los usa.
    P-20   Internal delegation and external federation are different concerns.
           boundary decide qué identidad cruza y si hay run hijo.
    P-21   Delegated authority is explicit and least-privileged.
           El presupuesto y el alcance salen del DelegationGrant, nunca de más.

Invariants preserved
    INV-E03  Los mensajes entre agentes cruzan una frontera explícita.
    INV-E04  Los adaptadores de protocolo y de transporte se reemplazan por separado.
    INV-E05  A2A es una opción externa, no una dependencia de Agent Core.
    INV-E06  La profundidad, los hijos y el costo delegado quedan acotados (depth, maxDepth, saldo).
    INV-E21  El presupuesto de la invocación no excede el saldo del padre (requireChildWithinParent).

Component ownership changes
    Ninguno nuevo. AgentCommunicationGateway gana funciones dentro de su owns (P-18, P-20, INV-E06).

Contract changes
    Nuevos: C-058 AgentInvocation, C-059 AgentCard.
    C-024 AgentCommunicationMessage v1 → v2 (+ invocationId).

Observability implications
    Nuevos AgentEventType: AGENT_INVOCATION_OPENED, AGENT_INVOCATION_UPDATED.
```

## 5. Conceptos Nuevos (New Concepts)

- **Invocación durable:** invocar a otro agente como un registro con dueño, estado, profundidad y
  presupuesto. Sobrevive a un reinicio sin repetirse.
- **Id derivado del paso:** el id de la invocación se calcula a partir del paso y de la tool call que
  la abrieron. Recuperar el paso vuelve a calcular el mismo id y encuentra la invocación.
- **Tarjeta de agente:** lo que un agente anuncia que sabe hacer (skills) y cómo se lo invoca.
- **Invocar es una tool call larga:** para el padre, la invocación es una tool call. El run queda en
  `WAITING_FOR_TOOL` y el resultado vuelve como `ToolResult`.
- **Esperas expuestas:** cuando el hijo se estaciona para preguntarle algo a alguien, la invocación
  pasa a `INPUT_REQUIRED` o `AUTHORIZATION_REQUIRED` con el id de esa espera. El padre publica la
  pregunta en su canal y la respuesta va a la espera del hijo.
- **La identidad cruza hacia adentro:**
  - un agente interno recibe el mismo `CallerSnapshot`, con la autoridad acotada por el
    `DelegationGrant`;
  - un agente externo no recibe el `Principal`: autentica al arnés, no al usuario.
- **Profundidad:** cuántas invocaciones hay entre el run raíz y este. Un run raíz tiene profundidad 0.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `AgentCommunicationMessage` (C-024, que pasa a v2), `DelegationGrant` (C-025),
  `Principal` (C-040), `CallerSnapshot` (C-041), `StepRecord` (C-042), `ParkedWait` (C-044),
  `ExecutionBudget` (C-012), `ExecutionUsage` (C-057), `ToolCall` (C-008), `ToolResult` (C-009),
  `ControlDirective`, `ExecutionContext` (C-004), `AgentEvent` (C-010), `HarnessError` (C-011);
- **primitivos:** `AgentInvocationId`, `RunId`, `StepId`, `WaitId`, `ToolCallId`, `AgentId`,
  `ActorId`, `Timestamp`.

| Identificador | Rol en este capítulo |
|---|---|
| `AgentInvocationId` | id de una invocación; nuevo, derivado del paso (§11) |
| `AgentCommunicationMessageId` | CH-15 §6: id de un mensaje |
| `DelegationGrantId` | CH-15 §6: id de un `DelegationGrant` |
| `StepId` | CH-32 §6: id de un paso durable |
| `WaitId` | CH-33 §6: id de una `ParkedWait` |
| `ActorId` | CH-06 §6: quien emite una directiva operacional |
| `AgentCommunicationBoundary` | CH-15 §6: `INTERNAL` o `EXTERNAL` |
| `WaitKind` | CH-33 §6: qué espera el hijo |
| `ControlDirectiveType` | CH-18 §6: se usa `KILL_SWITCH` para cancelar un hijo interno |
| `AgentEventType` | se agregan `AGENT_INVOCATION_OPENED` y `AGENT_INVOCATION_UPDATED` |
| `ErrorCategory` | reutiliza `DELEGATION`, `VALIDATION` y `CANCELLATION` |

### `AgentInvocationStatus` (embebido)

```pseudocode
ENUM AgentInvocationStatus
    WORKING
    INPUT_REQUIRED
    AUTHORIZATION_REQUIRED
    COMPLETED
    FAILED
    CANCELLED
END
```

Tiene la forma de los estados de una tarea A2A, pero es del arnés: el adaptador A2A traduce en las dos
direcciones (INV-E04).

### `AgentInvocation` — la invocación durable (C-058)

```pseudocode
STRUCT AgentInvocation
    invocationId: AgentInvocationId
    boundary: AgentCommunicationBoundary
    parentRunId: RunId
    targetAgentRef: Text
    skill: Text
    owner: Principal
    depth: Integer
    childRunId: Optional<RunId>
    remoteTaskRef: Optional<Text>
    status: AgentInvocationStatus
    budget: ExecutionBudget
    pendingWaitId: Optional<WaitId>
    result: Optional<Value>
    error: Optional<HarnessError>
    openedAt: Timestamp
    expiresAt: Optional<Timestamp>
END
```

- `childRunId` se llena cuando el hijo interno arranca; `remoteTaskRef`, cuando el agente externo
  acepta la tarea.
- `owner` es quien llamaba al padre (`execution.caller.current`).
- `pendingWaitId` es la espera del hijo que la invocación está exponiendo, si hay una.

### `AgentCard` — lo que un agente anuncia (C-059)

```pseudocode
STRUCT AgentCard
    agentRef: Text
    description: Text
    skills: List<Text>
    boundary: AgentCommunicationBoundary
    endpointRef: Optional<Text>
    authScheme: Optional<Text>
END
```

`endpointRef` y `authScheme` son referencias: el adaptador los resuelve. La credencial del esquema la
entrega el broker (CH-16), nunca la tarjeta.

### `InvocationUpdate` — un cambio de estado observado (embebido)

```pseudocode
STRUCT InvocationUpdate
    invocationId: AgentInvocationId
    status: AgentInvocationStatus
    childRunId: Optional<RunId>
    remoteTaskRef: Optional<Text>
    pendingWaitId: Optional<WaitId>
    result: Optional<Value>
    error: Optional<HarnessError>
    observedAt: Timestamp
END
```

Lo produce la integración, a partir del estado del run hijo, o el adaptador A2A, a partir del estado
de la tarea remota.

### `AgentCommunicationMessage` — versión 2 (C-024)

```pseudocode
STRUCT AgentCommunicationMessage
    id: AgentCommunicationMessageId
    boundary: AgentCommunicationBoundary
    sourceAgentRef: Text
    targetAgentRef: Text
    content: Value
    delegationGrantId: Optional<DelegationGrantId>
    traceId: TraceId
    sentAt: Timestamp
    invocationId: Optional<AgentInvocationId>
END
```

**Compatibilidad hacia atrás:** con `invocationId` en `NULL`, el mensaje es suelto, como en
CH-15..CH-43.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

```text
ID:                     C-058
Name:                   AgentInvocation
Version:                v1
Introduced In:          CH-44
Used By:                [CMP-013]
Constitutional Impact:  [P-20, P-21, INV-E03, INV-E06, INV-E21]
```

```text
ID:                     C-059
Name:                   AgentCard
Version:                v1
Introduced In:          CH-44
Used By:                [CMP-013]
Constitutional Impact:  [P-19, P-20, INV-E04, INV-E05]
```

```text
C-024 AgentCommunicationMessage  v1 → v2   Modified By: [CH-44]
                                 + invocationId: Optional<AgentInvocationId>
```

`AgentInvocationStatus` e `InvocationUpdate` quedan embebidos.

## 8. Responsabilidades de Componentes (Component Responsibilities)

**Este capítulo no introduce componentes.** `AgentCommunicationGateway` gana funciones dentro de su
`owns` literal:

```text
AgentCommunicationGateway (CMP-013)
    owns (CH-15): contratos semánticos explícitos (P-18), adaptadores de protocolo (P-19),
                  delegación interna ≠ federación externa (P-20), verificar el DelegationGrant (INV-E06)
    nuevas:
        invocationIdForStep, requireAdvertisedSkill, forwardedCallerFor,
        openAgentInvocation, applyInvocationUpdate, invocationStatusForWait, surfaceChildWait
    no posee:
        repartir ni verificar el presupuesto (ExecutionController, CH-43)
        arrancar o detener el run hijo (la integración y OperationalController, CH-18)
        estacionar ni resolver esperas (CH-33)
        resolver la credencial del esquema externo (CredentialBroker, CH-16)
        hablar A2A en el cable (el adaptador de protocolo, INV-E04)
```

Las funciones de integración (`invokeAgentDurably`, `completeAgentInvocation`,
`parentUsageAfterInvocation`, `cancelChildInvocation`) componen el Gateway con `ExecutionController`
y `OperationalController`, como las integraciones de CH-36.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
Abrir:      invokeAgentDurably
               → invocationIdForStep (¿ya existe?)
               → requireAdvertisedSkill
               → authorizeAgentCommunicationMessage (CH-15)
               → requireChildWithinParent (CH-43)
               → openAgentInvocation
            el hijo interno arranca con forwardedCallerFor y el presupuesto de la invocación
Seguir:     estado del hijo / tarea A2A → InvocationUpdate → applyInvocationUpdate
Esperas:    ParkedWait del hijo (CH-33) → surfaceChildWait → canal del padre (CH-37)
            respuesta → acceptDelivery sobre la espera del hijo (CH-33)
Terminar:   completeAgentInvocation → ToolResult del padre
            parentUsageAfterInvocation → rollUpChildUsage (CH-43)
Cancelar:   cancelChildInvocation → issueControlDirective(KILL_SWITCH) (CH-18) o cancelación A2A
```

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
Padre → invokeAgentDurably → AgentCommunicationGateway (AgentInvocation WORKING)
      → hijo interno (run con el mismo CallerSnapshot)  |  adaptador A2A → agente externo
estado del hijo / de la tarea → applyInvocationUpdate → completeAgentInvocation → ToolResult del padre
```

**Vista 2 — Sequence: delegar en un agente interno que pregunta algo**

```text
Padre (agente de compras), paso s-7, tool call c-2
   │ invokeAgentDurably → invocationIdForStep(s-7, c-2) = inv-1, no existe
   │   → skill anunciada, DelegationGrant vigente, presupuesto dentro del saldo
   │   → AgentInvocation inv-1 WORKING, depth 1        → AGENT_INVOCATION_OPENED
   ▼ hijo (agente de proveedores) arranca con el mismo CallerSnapshot
   │ hijo se estaciona: ParkedWait w-9 (QUESTION)
   │ surfaceChildWait → inv-1 INPUT_REQUIRED, pendingWaitId w-9   → AGENT_INVOCATION_UPDATED
   │ el padre publica la pregunta en su canal; el usuario responde a w-9
   │ hijo sigue → inv-1 WORKING → termina → inv-1 COMPLETED
   ▼ completeAgentInvocation → ToolResult del padre; rollUpChildUsage
```

**Vista 2b — Sequence: el servidor se reinicia a mitad**

```text
recuperación del paso s-7 → invokeAgentDurably → invocationIdForStep(s-7, c-2) = inv-1
   → inv-1 ya existe → se devuelve tal cual: no se lanza un segundo hijo
```

**Vista 2c — Sequence: agente externo por A2A**

```text
invokeAgentDurably con un AgentCard EXTERNAL (endpointRef, authScheme)
   → forwardedCallerFor = NULL: el banco no recibe el Principal del usuario
   → el adaptador A2A envía la tarea; su estado vuelve como InvocationUpdate (remoteTaskRef)
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

```pseudocode
FUNCTION invocationIdForStep(
    stepId: StepId,
    callId: ToolCallId
) -> AgentInvocationId

    RETURN deriveId("agent-invocation", stepId, callId)
END
```

```pseudocode
FUNCTION requireAdvertisedSkill(
    card: AgentCard,
    skill: Text
) -> AgentCard

    IF NOT contains(card.skills, skill)
        THROW HarnessError(
            category = DELEGATION,
            code = "AGENT_SKILL_NOT_ADVERTISED",
            message = "El agente no anuncia esa skill en su AgentCard",
            recoverable = TRUE,
            retryable = FALSE,
            metadata = {}
        )
    END

    IF (card.boundary == EXTERNAL AND (card.endpointRef == NULL OR card.authScheme == NULL))
        OR (card.boundary == INTERNAL AND card.endpointRef != NULL)

        THROW HarnessError(
            category = DELEGATION,
            code = "INVALID_AGENT_CARD",
            message = "Un agente externo declara endpoint y esquema de autenticación; uno interno no tiene endpoint",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN card
END
```

```pseudocode
FUNCTION forwardedCallerFor(
    caller: Optional<CallerSnapshot>,
    boundary: AgentCommunicationBoundary
) -> Optional<CallerSnapshot>

    IF boundary == EXTERNAL
        RETURN NULL
    END

    RETURN caller
END
```

```pseudocode
FUNCTION openAgentInvocation(
    invocationId: AgentInvocationId,
    card: AgentCard,
    skill: Text,
    grant: DelegationGrant,
    parentDepth: Integer,
    maxDepth: Integer,
    expiresAt: Optional<Timestamp>,
    execution: ExecutionContext,
    agentId: AgentId
) -> AgentInvocation

    IF execution.caller == NULL
        THROW HarnessError(
            category = DELEGATION,
            code = "INVOCATION_OWNER_REQUIRED",
            message = "Una invocación entre agentes tiene dueño: el run padre necesita un llamante verificado",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    IF parentDepth + 1 > maxDepth
        THROW HarnessError(
            category = DELEGATION,
            code = "DELEGATION_DEPTH_EXCEEDED",
            message = "La cadena de delegaciones superaría la profundidad máxima del despliegue",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    IF grant.delegateRef != card.agentRef
        THROW HarnessError(
            category = DELEGATION,
            code = "DELEGATION_GRANT_TARGET_MISMATCH",
            message = "El DelegationGrant delega en otro agente, no en el de esta AgentCard",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    invocation: AgentInvocation = AgentInvocation(
        invocationId = invocationId,
        boundary = card.boundary,
        parentRunId = execution.runId,
        targetAgentRef = card.agentRef,
        skill = skill,
        owner = execution.caller.current,
        depth = parentDepth + 1,
        childRunId = NULL,
        remoteTaskRef = NULL,
        status = WORKING,
        budget = grant.budget,
        pendingWaitId = NULL,
        result = NULL,
        error = NULL,
        openedAt = now(),
        expiresAt = expiresAt
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = AGENT_INVOCATION_OPENED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = invocation
    )

    RETURN invocation
END
```

```pseudocode
FUNCTION isTerminalInvocationStatus(
    status: AgentInvocationStatus
) -> Boolean

    RETURN status == COMPLETED OR status == FAILED OR status == CANCELLED
END
```

```pseudocode
FUNCTION applyInvocationUpdate(
    invocation: AgentInvocation,
    update: InvocationUpdate,
    execution: ExecutionContext,
    agentId: AgentId
) -> AgentInvocation

    IF update.invocationId != invocation.invocationId
        THROW HarnessError(
            category = VALIDATION,
            code = "INVOCATION_UPDATE_MISMATCH",
            message = "La actualización es de otra invocación",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    IF isTerminalInvocationStatus(invocation.status)
        THROW HarnessError(
            category = DELEGATION,
            code = "INVOCATION_ALREADY_TERMINAL",
            message = "Una invocación terminada no cambia de estado",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    waiting: Boolean = update.status == INPUT_REQUIRED OR update.status == AUTHORIZATION_REQUIRED

    IF (waiting AND invocation.boundary == INTERNAL AND update.pendingWaitId == NULL)
        OR (update.status == COMPLETED AND update.result == NULL)
        OR ((update.status == FAILED OR update.status == CANCELLED) AND update.error == NULL)

        THROW HarnessError(
            category = VALIDATION,
            code = "INVALID_INVOCATION_UPDATE",
            message = "Una espera interna nombra su waitId, un COMPLETED trae resultado y un FAILED o CANCELLED trae error",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    updated: AgentInvocation = AgentInvocation(
        invocationId = invocation.invocationId,
        boundary = invocation.boundary,
        parentRunId = invocation.parentRunId,
        targetAgentRef = invocation.targetAgentRef,
        skill = invocation.skill,
        owner = invocation.owner,
        depth = invocation.depth,
        childRunId = firstPresent(update.childRunId, invocation.childRunId),
        remoteTaskRef = firstPresent(update.remoteTaskRef, invocation.remoteTaskRef),
        status = update.status,
        budget = invocation.budget,
        pendingWaitId = update.pendingWaitId,
        result = update.result,
        error = update.error,
        openedAt = invocation.openedAt,
        expiresAt = invocation.expiresAt
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = AGENT_INVOCATION_UPDATED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = updated
    )

    RETURN updated
END
```

```pseudocode
FUNCTION invocationStatusForWait(
    kind: WaitKind
) -> AgentInvocationStatus

    IF kind == AUTHORIZATION
        RETURN AUTHORIZATION_REQUIRED
    END

    RETURN INPUT_REQUIRED
END
```

```pseudocode
FUNCTION surfaceChildWait(
    invocation: AgentInvocation,
    childWait: ParkedWait,
    execution: ExecutionContext,
    agentId: AgentId
) -> AgentInvocation

    IF invocation.boundary != INTERNAL
        OR invocation.childRunId == NULL
        OR childWait.runId != invocation.childRunId

        THROW HarnessError(
            category = DELEGATION,
            code = "CHILD_WAIT_NOT_OF_INVOCATION",
            message = "La espera no es del run hijo de esta invocación",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN applyInvocationUpdate(
        invocation,
        InvocationUpdate(
            invocationId = invocation.invocationId,
            status = invocationStatusForWait(childWait.kind),
            childRunId = NULL,
            remoteTaskRef = NULL,
            pendingWaitId = childWait.waitId,
            result = NULL,
            error = NULL,
            observedAt = now()
        ),
        execution,
        agentId
    )
END
```

**Integración.** Componen el Gateway con `ExecutionController` (CH-43) y `OperationalController`
(CH-18):

```pseudocode
FUNCTION invokeAgentDurably(
    step: StepRecord,
    call: ToolCall,
    existing: Optional<AgentInvocation>,
    card: AgentCard,
    skill: Text,
    message: AgentCommunicationMessage,
    grant: DelegationGrant,
    parentBudget: ExecutionBudget,
    parentUsage: ExecutionUsage,
    parentDepth: Integer,
    maxDepth: Integer,
    expiresAt: Optional<Timestamp>,
    execution: ExecutionContext,
    agentId: AgentId
) -> AgentInvocation

    invocationId: AgentInvocationId = invocationIdForStep(step.stepId, call.id)

    IF existing != NULL AND existing.invocationId == invocationId
        RETURN existing
    END

    IF message.invocationId != invocationId
        THROW HarnessError(
            category = VALIDATION,
            code = "MESSAGE_NOT_OF_INVOCATION",
            message = "El mensaje que abre la invocación lleva su invocationId",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    requireAdvertisedSkill(card, skill)
    authorizeAgentCommunicationMessage(message, grant)
    requireChildWithinParent(grant.budget, parentBudget, parentUsage)

    RETURN openAgentInvocation(
        invocationId, card, skill, grant, parentDepth, maxDepth, expiresAt, execution, agentId
    )
END
```

```pseudocode
FUNCTION completeAgentInvocation(
    invocation: AgentInvocation,
    update: InvocationUpdate,
    call: ToolCall,
    execution: ExecutionContext,
    agentId: AgentId
) -> ToolResult

    IF NOT isTerminalInvocationStatus(update.status)
        THROW HarnessError(
            category = VALIDATION,
            code = "INVOCATION_NOT_FINISHED",
            message = "Solo una invocación terminada produce el resultado de la tool call del padre",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    finished: AgentInvocation = applyInvocationUpdate(invocation, update, execution, agentId)

    RETURN ToolResult(
        callId = call.id,
        succeeded = finished.status == COMPLETED,
        outcome = NULL,
        output = finished.result,
        error = finished.error,
        completedAt = now()
    )
END
```

```pseudocode
FUNCTION parentUsageAfterInvocation(
    parentUsage: ExecutionUsage,
    childUsage: Optional<ExecutionUsage>
) -> ExecutionUsage

    IF childUsage == NULL
        RETURN parentUsage
    END

    RETURN rollUpChildUsage(parentUsage, childUsage)
END
```

```pseudocode
FUNCTION cancelChildInvocation(
    invocation: AgentInvocation,
    issuedBy: ActorId,
    execution: ExecutionContext,
    agentId: AgentId
) -> AgentInvocation

    IF isTerminalInvocationStatus(invocation.status)
        RETURN invocation
    END

    IF invocation.boundary == INTERNAL AND invocation.childRunId != NULL
        directive: ControlDirective = issueControlDirective(KILL_SWITCH, toText(invocation.childRunId), issuedBy)
    END

    RETURN applyInvocationUpdate(
        invocation,
        InvocationUpdate(
            invocationId = invocation.invocationId,
            status = CANCELLED,
            childRunId = NULL,
            remoteTaskRef = NULL,
            pendingWaitId = NULL,
            result = NULL,
            error = HarnessError(
                category = CANCELLATION,
                code = "PARENT_CANCELLED",
                message = "El run padre se canceló, y su invocación con él",
                recoverable = FALSE,
                retryable = FALSE,
                metadata = {}
            ),
            observedAt = now()
        ),
        execution,
        agentId
    )
END
```

Utilidades primitivas:
- `deriveId` calcula un id determinista a partir de sus argumentos;
- `contains` dice si una lista tiene un elemento;
- `firstPresent` devuelve el primer argumento que no sea `NULL`;
- `toText` convierte un id en texto;
- `newEventId` y `now` son las de siempre.

`authorizeAgentCommunicationMessage` (CH-15), `requireChildWithinParent` y `rollUpChildUsage` (CH-43)
e `issueControlDirective` (CH-18) no cambian. La directiva de `cancelChildInvocation` la aplica
`OperationalController` (`applyControlDirective`, CH-18). Para un agente externo, el adaptador envía la
cancelación del protocolo.

**Por qué `parentUsageAfterInvocation` acepta un uso ausente:** de un hijo interno el arnés conoce el
`ExecutionUsage`; de un agente externo, no. El costo de un agente externo es una tool más: lo cuenta
su capability (CH-39), no `rollUpChildUsage`.

Nótese lo que estas funciones **no** hacen:
- ninguna habla A2A: el adaptador traduce `AgentInvocation` e `InvocationUpdate` a su protocolo;
- ninguna resuelve una espera: la respuesta va a la espera del hijo por `acceptDelivery` (CH-33);
- ninguna decide en qué agente delegar: lo decide el modelo dentro de lo que el `DelegationGrant`
  permite.

## 12. Transiciones de Estado (State Transitions)

`AgentRunStatus` no cambia: el padre espera en `WAITING_FOR_TOOL`. La invocación:

```text
(open) → WORKING
WORKING → INPUT_REQUIRED | AUTHORIZATION_REQUIRED   (el hijo se estacionó: pendingWaitId)
INPUT_REQUIRED | AUTHORIZATION_REQUIRED → WORKING   (la espera del hijo se resolvió)
WORKING → COMPLETED (result) | FAILED (error)
cualquiera no terminal → CANCELLED (cancelChildInvocation)
COMPLETED, FAILED, CANCELLED: terminales; ninguna actualización los cambia

Reinicio del servidor
    el paso abierto se recupera → mismo invocationId → la invocación existente se devuelve
```

## 13. Semántica de Fallos (Failure Semantics)

Códigos nuevos de `HarnessError`, con `ErrorCategory` ya existentes:

```text
DELEGATION    AGENT_SKILL_NOT_ADVERTISED        recoverable: TRUE,  retryable: FALSE
DELEGATION    INVALID_AGENT_CARD                recoverable: FALSE, retryable: FALSE
DELEGATION    INVOCATION_OWNER_REQUIRED         recoverable: FALSE, retryable: FALSE
DELEGATION    DELEGATION_DEPTH_EXCEEDED         recoverable: FALSE, retryable: FALSE
DELEGATION    DELEGATION_GRANT_TARGET_MISMATCH  recoverable: FALSE, retryable: FALSE
DELEGATION    INVOCATION_ALREADY_TERMINAL       recoverable: FALSE, retryable: FALSE
DELEGATION    CHILD_WAIT_NOT_OF_INVOCATION      recoverable: FALSE, retryable: FALSE
VALIDATION    INVOCATION_UPDATE_MISMATCH        recoverable: FALSE, retryable: FALSE
VALIDATION    INVALID_INVOCATION_UPDATE         recoverable: FALSE, retryable: FALSE
VALIDATION    MESSAGE_NOT_OF_INVOCATION         recoverable: FALSE, retryable: FALSE
VALIDATION    INVOCATION_NOT_FINISHED           recoverable: FALSE, retryable: FALSE
CANCELLATION  PARENT_CANCELLED                  recoverable: FALSE, retryable: FALSE
```

- Los errores al abrir vuelven al modelo del padre como `ToolResult` fallido (INV-07).
  `AGENT_SKILL_NOT_ADVERTISED` es recuperable: el modelo puede elegir otra skill u otro agente.
- Un hijo que falla deja la invocación en `FAILED` con su error, y el padre lo recibe como observación.
- Los errores de CH-15 (`DELEGATION_GRANT_EXPIRED`, `DELEGATION_SCOPE_EXCEEDED`…) y de CH-43
  (`CHILD_BUDGET_EXCEEDS_PARENT`) se propagan sin cambios.
- Si la invocación vence (`expiresAt`), la integración la cancela con `cancelChildInvocation`, igual
  que una espera vencida en CH-37.

## 14. Eventos Producidos (Events Produced)

```text
AGENT_INVOCATION_OPENED   — se abrió una invocación (payload: AgentInvocation)
AGENT_INVOCATION_UPDATED  — la invocación cambió de estado (payload: AgentInvocation)
```

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **La identidad del usuario no sale del arnés.** Un agente externo recibe una tarea autenticada con
  la credencial del arnés (`authScheme`, resuelta por el broker), nunca el `Principal` del usuario.
- **Un hijo interno actúa para el mismo usuario, con menos autoridad:** el `CallerSnapshot` es el
  mismo, pero el alcance y el presupuesto salen del `DelegationGrant` (P-21).
- **Delegar no multiplica el gasto:** el presupuesto de la invocación se verifica contra el saldo del
  padre (INV-E21), y la profundidad tiene techo (INV-E06).
- **Un reinicio no duplica trabajo:** el id derivado del paso impide lanzar un segundo hijo.
- **Responder a la espera del hijo exige lo de siempre:** la regla de quien responde de la
  `ParkedWait` del hijo (CH-33). Exponerla en el canal del padre no le da a nadie más derecho a
  contestarla.
- **El núcleo no conoce A2A** (INV-E05): cambiar de protocolo es cambiar de adaptador.

## 16. Tests (Tests)

```text
TEST InvocationIdIsDerivedFromStepAndCall
TEST RecoveredStepReturnsTheExistingInvocation
TEST SkillNotAdvertisedIsRejected
TEST ExternalCardWithoutEndpointOrAuthSchemeIsRejected
TEST ExternalInvocationDoesNotForwardThePrincipal
TEST InternalInvocationForwardsTheSameCallerSnapshot
TEST InvocationWithoutCallerIsRejected
TEST DelegationDepthAboveMaxIsRejected
TEST GrantForAnotherAgentIsRejected
TEST InvocationBudgetAboveParentRemainingIsRejected
TEST ChildQuestionPutsInvocationInInputRequired
TEST ChildAuthorizationPutsInvocationInAuthorizationRequired
TEST WaitOfAnotherRunIsNotSurfaced
TEST TerminalInvocationDoesNotChange
TEST CompletedInvocationBecomesSuccessfulToolResult
TEST ChildUsageRollsUpIntoTheParent
TEST CancellingTheParentIssuesKillSwitchForTheChild
TEST LooseMessageWithoutInvocationIdBehavesAsV1
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (v0.3 en curso, después de CH-44) — 29 componentes, 59 contratos, 45 capítulos

Components — 29, sin cambios
 └── CMP-013 AgentCommunicationGateway   (+ invocaciones durables, esperas expuestas, identidad que cruza)

Contracts — 59
 ├── C-024 AgentCommunicationMessage v2  (CH-15 → modificado en CH-44: invocationId)
 ├── C-058 AgentInvocation               (CH-44)
 └── C-059 AgentCard                     (CH-44)

Deuda: D-020 y D-023 resueltas.
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **Descubrir agentes** (un catálogo o directorio de `AgentCard`): las tarjetas se declaran en la
  configuración del despliegue, como las conexiones de CH-41. No es deuda.
- **Recibir invocaciones de agentes externos:** un agente externo que invoca al nuestro es un
  estímulo de entrada más; entra por el Ingress Adapter y la admisión de CH-14/CH-31 con un principal
  `SERVICE`. No es deuda.
- **Resultados parciales en streaming** de un agente externo: el adaptador puede acumularlos; la
  invocación solo guarda el resultado final. No es deuda.
- **Que la invocación sobreviva a una versión nueva del runtime:** un hijo activo es trabajo vivo, y
  qué pasa con él al cambiar de versión es de la evolución del runtime (CH-45, INV-E22), ya planeada.
  No es deuda.

## 19. Siguiente Incremento (Next Increment)

Ahora el arnés tiene trabajo vivo que dura: esperas estacionadas, pasos sin confirmar e invocaciones
con hijos activos. Pero nada dice qué pasa con ese trabajo cuando **se despliega una versión nueva**
del agente, de la política, del modelo o del formato de sesión.

El siguiente capítulo introduce la **evolución del runtime**:
- un `RuntimeVersionSnapshot` que fija con qué versiones corre cada sesión;
- `sessionMayMigrate`, que decide si una sesión puede pasar a la versión nueva;
- INV-E22: el trabajo vivo nunca migra entre versiones.

Será CH-45 ("Evolución del Runtime"). `next_chapter` queda en `null` porque CH-45 todavía no existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): un mensaje entre agentes no tiene dueño ni estado; un reinicio repite la
   delegación y las preguntas del hijo no tienen por dónde salir.
2. **Patrones** (= §3): CH-15 resolvió si un mensaje cruza, no qué pasa con el trabajo que inicia.
3. **Estructuras** (= §8): `AgentInvocation` (C-058), `AgentCard` (C-059),
   `AgentCommunicationMessage` v2 y funciones nuevas en `AgentCommunicationGateway`.
4. **Modelos mentales** (= §4): P-20, P-21, INV-E05, INV-E06 e INV-E21.

**Bucles de retroalimentación**

- **Refuerzo:** cada reinicio lanza un hijo más, y cada hijo puede delegar. El id derivado del paso
  corta la espiral.
- **Equilibrio:** la profundidad y el saldo. Cada nivel suma uno a `depth` y recibe solo una parte del
  saldo.

**Punto de apalancamiento**

La decisión con mayor efecto es que `AgentInvocation` (C-058) sea un registro con id derivado del paso
que la abrió: sobrevive a un reinicio sin repetirse, tiene dueño y presupuesto, y expone las esperas del
hijo en el canal del padre.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿De qué se deriva el id de una `AgentInvocation`, y qué hace `invokeAgentDurably` cuando recibe una
   invocación existente con ese mismo id? *(pregunta guía 1)*
2. ¿Qué hace `surfaceChildWait` con la espera de un hijo interno, a qué estado pasa la invocación
   según el tipo de espera, y adónde va la respuesta del usuario? *(pregunta guía 2)*
3. ¿Qué devuelve `forwardedCallerFor` para un agente interno y para uno externo, y con qué se
   autentica el arnés ante un agente externo? *(pregunta guía 3)*
4. ¿Qué dos límites acotan una cadena de delegaciones, y qué funciones los hacen cumplir?
   *(pregunta guía 4)*

### Explicar

1. `AgentCommunicationGateway` ya decidía si un mensaje puede cruzar hacia otro agente. Explica por qué
   también le pertenece seguir el trabajo que ese mensaje inicia, y por qué A2A queda como un adaptador
   suyo.
2. Explica por qué una invocación entre agentes necesita ser un registro con dueño, estado y
   presupuesto, y no basta con un mensaje de ida y otro de vuelta.

### Conectar

1. En CH-15, `authorizeAgentCommunicationMessage` verificaba que un `DelegationGrant` siguiera vigente
   y cubriera el mensaje. ¿Qué agrega `invokeAgentDurably` antes y después de esa verificación, y de
   qué campo del `DelegationGrant` sale el presupuesto de la invocación?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
