---
id: CH-33
title: "Esperas Durables y la Reanudación desde Cualquier Canal"
starting_version: "0.1"
ending_version: "0.2"
introduces_components: [CMP-024]
introduces_contracts: [C-044, C-045]
modifies_contracts: [C-015]
constitutional_articles: [P-11, P-23, P-31, P-33, INV-14, INV-15, INV-E08, INV-E18]
previous_chapter: CH-32
next_chapter: CH-34
retrieval_set:
  expected_outcome:
    id: EO-CH33
    text: |
      Al terminar este capítulo podrás estacionar un run que espera — una aprobación, una respuesta,
      una autorización o una decisión sobre su presupuesto — sin que ningún proceso quede ocupado, y
      decidir, cuando llega una respuesta por cualquier canal, si reanuda esa espera y si quien
      responde tiene derecho a hacerlo.
  skeleton:
    id: SK-CH33
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
    components_to_be_introduced: [CMP-024]
    contracts_to_be_introduced: [C-044, C-045]
  guiding_questions:
    - id: GQ-CH33-01
      text: |
        Si un agente necesita que alguien apruebe un pago y esa persona tarda dos días en responder,
        ¿debería quedar un proceso encendido esperando todo ese tiempo?
      answered_by: RQ-CH33-01
    - id: GQ-CH33-02
      text: |
        Si una sesión tiene dos preguntas pendientes y llega una respuesta por chat, ¿cómo sabe el
        arnés a cuál de las dos responde? ¿Debería adivinarlo?
      answered_by: RQ-CH33-02
    - id: GQ-CH33-03
      text: |
        Si el agente pide a un usuario que autorice el acceso a su calendario, ¿podría otra persona
        de la misma empresa completar esa autorización en su lugar?
      answered_by: RQ-CH33-03
    - id: GQ-CH33-04
      text: |
        ¿Qué tienen en común una aprobación humana, una pregunta, una autorización de acceso y un
        límite de presupuesto alcanzado, desde el punto de vista del run que se detiene?
      answered_by: RQ-CH33-04
  systems_lens:
    iceberg_visible_fact: |
      Un run que espera una aprobación queda estacionado por beginToolApprovalPause (CH-13), pero
      nadie decide qué respuesta lo reanuda ni quién puede darla; resumeAfterHumanResolution existe
      y nadie la invoca, y PAUSED nunca se produce (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que cada tipo de espera — aprobación, pregunta, autorización,
      presupuesto — se imagina con su propio mecanismo, o no se imagina, y ninguno valida que la
      respuesta vaya a la espera correcta ni que venga de alguien autorizado (ver sección 3).
    iceberg_structures: |
      Este capítulo introduce ResumptionCoordinator (CMP-024), ParkedWait (C-044) y
      AuthorizationChallenge (C-045), y lleva HumanInteractionRequest (C-015) a v2 con waitId: una
      sola espera durable para los cuatro tipos, reanudada solo por una entrega dirigida y
      autorizada (ver sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-33 (esperar es durable y no consume cómputo), INV-E18 (una entrega
      reanuda solo la espera a la que se dirige y solo si quien responde está autorizado) y P-31
      (la identidad de quien responde es un Principal verificado) (ver sección 4).
    reinforcing_loop: |
      Si esperar ocupa un proceso, cada espera larga reduce la capacidad del sistema; con menos
      capacidad los runs esperan más en cola, y hay más esperas simultáneas. Estacionar sin cómputo
      corta la espiral: una espera cuesta un registro, no un proceso.
    balancing_loop: |
      INV-E18 es el mecanismo de equilibrio: por muchas respuestas que lleguen, y por muchos canales,
      solo reanuda una espera la entrega que la nombra y cuyo Principal cumple su regla.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que la entrega nombre su espera (waitId) y
      traiga un Principal verificado: findAddressedWait nunca infiere y responderMayResolve decide
      con la regla de la ParkedWait (C-044), no con el canal.
  recall_questions:
    - id: RQ-CH33-01
      text: |
        ¿Qué hace parkRun, qué AgentRunStatus decide runStatusForWait para cada WaitKind, y por qué
        después de estacionar no queda ningún proceso esperando?
    - id: RQ-CH33-02
      text: |
        ¿Cómo encuentra findAddressedWait la espera de una WaitDelivery, y qué error lanza cuando la
        entrega no nombra ninguna espera estacionada?
    - id: RQ-CH33-03
      text: |
        ¿Qué ResponderRule exige parkRun para una espera AUTHORIZATION, qué contiene y qué no
        contiene un AuthorizationChallenge, y a dónde va el token?
    - id: RQ-CH33-04
      text: |
        ¿Cuáles son los cuatro WaitKind, qué ParkedWait tienen en común, y qué función de CH-13
        invoca resumeToolApprovalWait después de acceptDelivery?
  explain_prompts:
    - id: EP-CH33-01
      text: |
        HumanInteractionService y ResumptionCoordinator participan en toda aprobación humana.
        Explica, como si hablaras con alguien sin contexto técnico, qué decide cada uno, y por qué la
        solicitud y la espera son dos cosas distintas.
      target_entity: CMP-024
    - id: EP-CH33-02
      text: |
        Explica por qué ParkedWait guarda requestedBy y una regla de quién puede responder, y qué
        ataque sería posible si cualquier respuesta con el waitId correcto reanudara la espera.
      target_entity: C-044
  interleaved_questions:
    - id: IQ-CH33-01
      text: |
        En CH-31, continuationAllowedForCaller decidía si un Principal podía continuar una sesión con
        SAME_PRINCIPAL o SAME_TENANT. ¿En qué se parece y en qué se diferencia responderMayResolve,
        y por qué una espera necesita además DESIGNATED_PRINCIPAL?
      current_chapter_entities: [C-044, CMP-024]
      prior_chapter_entities: [C-040, C-041, CMP-012]
      prior_chapter: CH-31
  flashcards:
    - id: FC-CH33-01
      front: |
        ¿Qué es una ParkedWait (C-044)?
      back: |
        Un run estacionado durablemente, sin cómputo, esperando una aprobación, una pregunta, una
        autorización o una decisión de presupuesto. Guarda quién la pidió (requestedBy), quién puede
        responder (responderRule, designatedResponder) y su estado (PARKED / RESUMED / EXPIRED).
      source_entity: C-044
      chapter_introduced_in: CH-33
      review_stage: DAY_1
    - id: FC-CH33-02
      front: |
        ¿Qué dice INV-E18 y qué dos funciones lo materializan?
      back: |
        Una entrega reanuda solo la espera a la que se dirige, y solo si quien responde está
        autorizado. findAddressedWait busca por waitId explícito; responderMayResolve valida al
        Principal contra la regla de la espera.
      source_entity: CMP-024
      chapter_introduced_in: CH-33
      review_stage: DAY_1
    - id: FC-CH33-03
      front: |
        ¿Qué es un AuthorizationChallenge (C-045) y qué nunca contiene?
      back: |
        La solicitud de una autorización interactiva por usuario hacia un servicio externo (p.ej.
        OAuth): principal, connectionRef, callbackRef y vencimiento. Nunca contiene un token: el
        callback lo entrega directo a CredentialBroker (INV-E08).
      source_entity: C-045
      chapter_introduced_in: CH-33
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH33-01
      recall_question: RQ-CH33-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH33-02
      recall_question: RQ-CH33-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH33-03
      recall_question: RQ-CH33-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH33-04
      recall_question: RQ-CH33-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 33 — Esperas Durables y la Reanudación desde Cualquier Canal

> **Regla constitucional (P-33):** esperar es durable y no consume cómputo.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás estacionar un run que espera (una
aprobación, una respuesta, una autorización o una decisión sobre su presupuesto) sin que ningún
proceso quede ocupado. También podrás decidir, cuando llega una respuesta por cualquier canal, si
reanuda esa espera y si quien responde tiene derecho a hacerlo.

**Esqueleto.** Sexto capítulo del Tramo 4. Introduce el componente `ResumptionCoordinator` y dos
contratos, lleva `HumanInteractionRequest` a v2 y da el primer uso real a `PAUSED`.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si un agente necesita que alguien apruebe un pago y esa persona tarda dos días en responder,
   ¿debería quedar un proceso encendido esperando todo ese tiempo?
2. Si una sesión tiene dos preguntas pendientes y llega una respuesta por chat, ¿cómo sabe el arnés a
   cuál de las dos responde? ¿Debería adivinarlo?
3. Si el agente pide a un usuario que autorice el acceso a su calendario, ¿podría otra persona de la
   misma empresa completar esa autorización en su lugar?
4. ¿Qué tienen en común una aprobación humana, una pregunta, una autorización de acceso y un límite
   de presupuesto alcanzado, desde el punto de vista del run que se detiene?

## 1. Arquitectura Actual (Current Architecture)

- **`HumanInteractionService` (CMP-006, CH-06)** representa una `HumanInteractionRequest` (C-015),
  la persiste mientras está pendiente y recibe su `HumanInteractionResolution` (C-016). No
  transporta nada por ningún canal (P-11).
- **`beginToolApprovalPause` (CH-13)** crea la solicitud, deja el run en `WAITING_FOR_HUMAN`, guarda
  un checkpoint y **retorna**. Ningún proceso queda esperando. Es la mitad correcta.
- **`resumeAfterHumanResolution` (CH-13)** resuelve la solicitud y continúa el turno, pero **nadie
  la invoca**: CH-13 lo declara como límite.
- **`AgentRunStatus` (C-013)** tiene un valor `PAUSED` que ningún capítulo produce.
- **`Principal` (C-040, CH-31)** ya identifica a quien llama; `caller.current` viaja en cada turno.

## 2. El Problema (Problem)

Un run se detiene por cuatro razones muy distintas en apariencia:
- una acción necesita **aprobación** humana;
- el agente necesita una **respuesta** a una pregunta;
- una herramienta necesita que el usuario **autorice** el acceso a un servicio externo (OAuth);
- el run alcanzó un **límite de presupuesto** y alguien debe decidir si sigue.

Hoy no hay respuesta para las preguntas básicas de ninguna de ellas:
- **¿qué respuesta reanuda qué espera?** Si una sesión tiene dos esperas, una respuesta por chat
  podría reanudar la equivocada;
- **¿quién puede responder?** Nada impide que cualquiera con el identificador apruebe un pago;
- **¿dónde queda el token** de una autorización? Si pasa por el run, puede terminar en el contexto
  del modelo;
- las autorizaciones y los límites de presupuesto ni siquiera tienen mecanismo.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **La solicitud no es la espera.** `HumanInteractionService` sabe qué se preguntó y qué se
  respondió, pero no sabe qué run está estacionado ni qué entrega lo reanuda. Por eso
  `resumeAfterHumanResolution` no tiene quién la llame.
- **Nadie valida al que responde.** `resolveHumanInteractionRequest` recibe un `ActorId`, pero ningún
  componente decide si ese actor puede resolver **esa** espera.
- **Solo hay un tipo de espera.** Una autorización OAuth o un límite de presupuesto no son una
  `HumanInteractionRequest` (no hay tool call que aprobar), así que no tienen dónde vivir.
- **Ningún componente posee la decisión** "¿esta entrega reanuda esta espera?". No es de
  `HumanInteractionService` (la solicitud), ni de `AgentLoop` (el turno), ni de `PolicyEngine` (si
  hace falta aprobar). Por eso este capítulo introduce un componente (EVO-01).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-11   UI is an adapter, not part of the core.
           La entrega llega por cualquier canal; el canal nunca decide si es válida.
    P-23   Durable execution is a core runtime property.
           Una espera es un registro durable, no un proceso bloqueado.
    P-31   Identity travels with every turn.
           requestedBy es caller.current; quien responde es un Principal verificado.

Principles introduced (Amendment v1.2, ya ratificado)
    P-33   Waiting is durable and consumes no compute.
           parkRun estaciona y retorna; acceptDelivery reanuda.

Invariants preserved
    INV-14   Human Interaction nunca depende de una interfaz particular.
             WaitDelivery trae channelRef solo para trazabilidad.
    INV-15   Una acción que requiere aprobación no se ejecuta antes de una resolución válida.
             resumeToolApprovalWait solo ejecuta tras acceptDelivery.
    INV-E08  Credentials are resolved by a CredentialBroker and SHOULD NOT enter model context.
             AuthorizationChallenge nunca contiene un token.
    INV-E18  (Amendment v1.2) A delivery resumes only the wait it addresses, and only if its
             responder is authorized for it.
             findAddressedWait + responderMayResolve.

Component ownership changes
    Nuevo: ResumptionCoordinator (CMP-024).
    HumanInteractionService (CMP-006) gana linkRequestToWait, dentro de "persistir
    interacciones pendientes".

Contract changes
    Nuevos: C-044 ParkedWait, C-045 AuthorizationChallenge.
    C-015 HumanInteractionRequest v1 → v2 (+ waitId, Optional).
    C-013 AgentRunStatus: sin cambios; PAUSED se produce por primera vez.

Security implications
    Una espera solo la reanuda quien su regla permite; una autorización, solo su propio
    usuario (ver sección 15).

Observability implications
    Nuevos AgentEventType: RUN_PARKED, RUN_RESUMED y WAIT_DELIVERY_REJECTED.

Deterministic vs agentic boundary
    El modelo puede proponer una acción que requiera aprobación, pero nunca ve ni resuelve
    una espera.
```

## 5. Conceptos Nuevos (New Concepts)

- **Espera estacionada** (*parked wait*): un run detenido durablemente. El proceso que lo corría
  termina; la espera es un registro que sobrevive reinicios. Esperar dos días cuesta lo mismo que
  esperar dos segundos: un registro.
- **Cuatro tipos, una abstracción** (lección de eve): aprobación de una tool, pregunta, autorización
  interactiva y límite de presupuesto son la misma cosa desde el punto de vista del run: "me detengo
  hasta que alguien autorizado responda". Cambia qué se responde, no cómo se espera.
- **Entrega dirigida** (*addressed delivery*): la respuesta nombra explícitamente la espera que
  reanuda (`waitId`) y trae la identidad verificada de quien responde. Nunca se infiere.
- **Regla de quien responde:**
  - `SAME_PRINCIPAL`: solo la misma persona o servicio que pidió la espera;
  - `SAME_TENANT`: cualquier usuario verificado de la misma empresa;
  - `DESIGNATED_PRINCIPAL`: un principal concreto, por ejemplo el aprobador de pagos.
- **Estado del run mientras espera:** `WAITING_FOR_HUMAN` si espera a una persona que decide
  (aprobación, pregunta); `PAUSED` si espera algo que no es una decisión sobre el trabajo del agente
  (una autorización de acceso, un límite de presupuesto).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `AgentState` (C-003), `ExecutionContext` (C-004), `AgentRunStatus` (C-013),
  `HumanInteractionRequest` (C-015, que pasa a v2), `Principal` (C-040), `ToolCall` (C-008),
  `AgentMessage` (C-001), `SessionState` (C-020), `EventSubscription` (C-019), `AgentEvent` (C-010),
  `HarnessError` (C-011);
- **primitivos:** `RunId`, `SessionId`, `AgentId`, `ToolCallId`, `Timestamp`.

| Identificador | Rol en este capítulo |
|---|---|
| `WaitId` | identificador nuevo de una espera estacionada |
| `AuthorizationChallengeId` | identificador nuevo de un desafío de autorización |
| `HumanInteractionRequestId` | identificador de una solicitud humana (heredado de CH-06) |
| `HumanInteractionType` | `APPROVAL` / `INPUT` / `REVIEW` / `DECISION` (heredado de CH-06) |
| `HumanInteractionStatus` | `PENDING` / `RESOLVED` (heredado de CH-06) |
| `HumanInteractionOutcome` | `APPROVED` / `REJECTED` / `PROVIDED` (heredado de CH-06) |
| `ExecutionUsage` | uso del run (embebido en CH-07), que `resumeAfterHumanResolution` recibe |
| `AgentEventType` | se agregan `RUN_PARKED`, `RUN_RESUMED` y `WAIT_DELIVERY_REJECTED` |
| `ErrorCategory` | reutiliza `HUMAN_INTERACTION`, sin valores nuevos |

### `WaitKind` — los cuatro tipos de espera (embebido)

```pseudocode
ENUM WaitKind
    TOOL_APPROVAL
    QUESTION
    AUTHORIZATION
    BUDGET_LIMIT
END
```

### `WaitStatus` — el estado de una espera (embebido)

```pseudocode
ENUM WaitStatus
    PARKED
    RESUMED
    EXPIRED
END
```

### `ResponderRule` — quién puede responder (embebido)

```pseudocode
ENUM ResponderRule
    SAME_PRINCIPAL
    SAME_TENANT
    DESIGNATED_PRINCIPAL
END
```

### `ParkedWait` — la espera estacionada (C-044)

```pseudocode
STRUCT ParkedWait
    waitId: WaitId
    runId: RunId
    sessionId: SessionId
    kind: WaitKind
    requestId: Optional<HumanInteractionRequestId>
    challengeId: Optional<AuthorizationChallengeId>
    requestedBy: Principal
    responderRule: ResponderRule
    designatedResponder: Optional<Principal>
    status: WaitStatus
    parkedAt: Timestamp
    expiresAt: Optional<Timestamp>
    resumedAt: Optional<Timestamp>
END
```

`requestId` apunta a la solicitud humana (aprobación, pregunta); `challengeId`, al desafío de
autorización. Un límite de presupuesto no tiene ninguno de los dos.

### `AuthorizationChallenge` — la autorización interactiva (C-045)

```pseudocode
STRUCT AuthorizationChallenge
    challengeId: AuthorizationChallengeId
    principal: Principal
    connectionRef: Text
    callbackRef: Text
    createdAt: Timestamp
    expiresAt: Timestamp
END
```

`callbackRef` es una referencia opaca que genera el arnés. El adaptador de callback la usa para
saber a qué desafío corresponde la autorización que vuelve. No hay campo para un token: no existe.

### `WaitDelivery` — una respuesta que llega por algún canal (embebido)

```pseudocode
STRUCT WaitDelivery
    waitId: WaitId
    responder: Principal
    channelRef: Text
    outcome: HumanInteractionOutcome
    value: Optional<Value>
    receivedAt: Timestamp
END
```

`responder` ya viene verificado por el adaptador de identidad (CH-31). `channelRef` dice por dónde
llegó; ninguna decisión lo usa.

### `HumanInteractionRequest` — versión 2 (C-015)

```pseudocode
STRUCT HumanInteractionRequest
    id: HumanInteractionRequestId
    type: HumanInteractionType
    callId: ToolCallId
    status: HumanInteractionStatus
    waitId: Optional<WaitId>
    requestedAt: Timestamp
END
```

**Compatibilidad hacia atrás:** `waitId = NULL` es una solicitud como las de CH-06..CH-32. Ningún
pseudocódigo anterior cambia de significado.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

```text
ID:                     C-044
Name:                   ParkedWait
Version:                v1
Introduced In:          CH-33
Used By:                [CMP-024]
Constitutional Impact:  [P-23, P-33, INV-E18, INV-19]
```

```text
ID:                     C-045
Name:                   AuthorizationChallenge
Version:                v1
Introduced In:          CH-33
Used By:                [CMP-024]
Constitutional Impact:  [P-31, P-33, INV-E08, INV-E18]
```

```text
C-015 HumanInteractionRequest  v1 → v2   Modified By: [CH-33]   + waitId: Optional<WaitId>
Used By:                       [CMP-006, CMP-024]
```

`WaitKind`, `WaitStatus`, `ResponderRule` y `WaitDelivery` quedan embebidos. `C-013 AgentRunStatus`
no cambia.

## 8. Responsabilidades de Componentes (Component Responsibilities)

```pseudocode
COMPONENT ResumptionCoordinator
    consumes: AgentState, ExecutionContext, HumanInteractionRequest, Principal
    produces: ParkedWait, AuthorizationChallenge, AgentEvent, HarnessError
END
```

```text
COMPONENT: ResumptionCoordinator (CMP-024)

Responsibility:
    Estacionar durablemente un run que espera, sin retener cómputo, y decidir, cuando llega una
    entrega por cualquier canal, qué espera reanuda y si quien responde está autorizado para ella.

Owns (Amendment v1.2, citas literales):
    - "Approvals, questions, interactive authorizations and budget limits MUST park the run
      durably. A parked run MUST NOT hold compute, and MUST be resumable by a delivery arriving
      through any authorized channel" (P-33)
    - "A delivery resumes only the wait it addresses, and only if its responder is authorized for
      it" (INV-E18): encontrar la espera por waitId explícito y validar al que responde
    - decidir el AgentRunStatus de un run estacionado (WAITING_FOR_HUMAN o PAUSED)
    - representar la espera de una autorización interactiva sin contener credenciales
    - rechazar (fail-closed) entregas a esperas reanudadas, vencidas o no dirigidas

Does NOT own:
    - representar la solicitud humana, persistirla y recibir su resolución (HumanInteractionService,
      CMP-006, CH-06). Es la frontera más importante del capítulo: HumanInteractionService es dueño
      de la SOLICITUD y su RESOLUCIÓN; ResumptionCoordinator es dueño de la ESPERA.
    - decidir SI una acción requiere aprobación (PolicyEngine, CMP-005)
    - ejecutar la acción aprobada (ToolRuntime, CMP-002) ni decidir si el turno sigue (AgentLoop)
    - detectar que falta una credencial ni guardar el token (CredentialBroker, CMP-014, INV-E08)
    - decidir o ampliar el presupuesto (ExecutionController, CMP-007)
    - transportar la entrega por un canal concreto (Channel Adapter, P-11)
```

**HumanInteractionService (CMP-006)** gana una función, `linkRequestToWait`, dentro de su `owns`
literal "persistir interacciones pendientes": anotar en la solicitud la espera que abrió.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
ResumptionCoordinator
    consumes → AgentState, ExecutionContext, HumanInteractionRequest, Principal
    produces → ParkedWait, AuthorizationChallenge, AgentEvent, HarnessError
    depends on (componentes) → (ninguno)
```

La integración (CH-36) encadena, para una aprobación:
1. `beginToolApprovalPause` (CH-13) crea la solicitud y retorna el estado pausado;
2. `parkRun(…, TOOL_APPROVAL, request.id, …)` → `ParkedWait`;
3. `linkRequestToWait(request, wait)` → `HumanInteractionRequest` v2;
4. el proceso **termina**;
5. días después, un adaptador de canal entrega una `WaitDelivery`;
6. `findAddressedWait` → `resumeToolApprovalWait` → `acceptDelivery` → `resumeAfterHumanResolution` (CH-13).

Para una autorización, `CredentialBroker` detecta que no hay credencial del `caller.current` y la
integración invoca `createAuthorizationChallenge` + `parkRun(…, AUTHORIZATION, …)`. El adaptador de
callback entrega el token a `CredentialBroker` y una `WaitDelivery` (`APPROVED` o `REJECTED`) al
coordinador.

**Anexo — protocolo de UI remota (aporte de pi).** Una UI que corre en otro proceso (una extensión de
editor, una app móvil) necesita dos mensajes: "muéstrale al usuario este diálogo" (la solicitud, con
su `waitId`) y "el usuario respondió esto" (una `WaitDelivery`). Es un **adaptador de canal** de
`HumanInteractionService` (P-11, INV-14), no un componente: el núcleo no sabe si el diálogo se
mostró en una terminal, un navegador o un teléfono.

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
Integración → HumanInteractionService (solicitud) → ResumptionCoordinator (espera) → fin del proceso
Canal (cualquiera) → ResumptionCoordinator (entrega dirigida) → resumeAfterHumanResolution (CH-13)
```

**Vista 2 — Sequence: estacionar y reanudar una aprobación**

```text
Integración
   │ beginToolApprovalPause(…)                     → request (CH-13), WAITING_FOR_HUMAN
   │ parkRun(state, TOOL_APPROVAL, request.id, …, DESIGNATED_PRINCIPAL, aprobador)
   │                                               → ParkedWait PARKED + RUN_PARKED
   │ linkRequestToWait(request, wait)              → request.waitId
   ▼ (el proceso termina: nada queda esperando)
…
Canal (chat, correo, UI) → WaitDelivery(waitId, responder, APPROVED)
   │ findAddressedWait(waits, delivery)            → la espera nombrada
   │ resumeToolApprovalWait(…)
   │   acceptDelivery                              → RESUMED + RUN_RESUMED
   │   resumeAfterHumanResolution (CH-13)          → ejecuta la tool, sigue el turno
```

**Vista 2b — Sequence: una entrega no autorizada**

```text
Otra persona → WaitDelivery(waitId, otroPrincipal, APPROVED)
   │ acceptDelivery → responderMayResolve = FALSE
   │   → WAIT_DELIVERY_REJECTED + RESPONDER_NOT_AUTHORIZED; la espera sigue PARKED
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

```pseudocode
FUNCTION runStatusForWait(
    kind: WaitKind
) -> AgentRunStatus

    IF kind == TOOL_APPROVAL OR kind == QUESTION
        RETURN WAITING_FOR_HUMAN
    END

    RETURN PAUSED
END
```

```pseudocode
FUNCTION samePrincipal(
    a: Principal,
    b: Principal
) -> Boolean

    RETURN a.issuer == b.issuer AND a.principalId == b.principalId
END
```

```pseudocode
FUNCTION parkRun(
    state: AgentState,
    kind: WaitKind,
    requestId: Optional<HumanInteractionRequestId>,
    challengeId: Optional<AuthorizationChallengeId>,
    requestedBy: Principal,
    rule: ResponderRule,
    designated: Optional<Principal>,
    expiresAt: Optional<Timestamp>,
    execution: ExecutionContext
) -> ParkedWait

    IF ((kind == TOOL_APPROVAL OR kind == QUESTION) AND requestId == NULL)
        OR (kind == AUTHORIZATION AND challengeId == NULL)
        OR (rule == DESIGNATED_PRINCIPAL AND designated == NULL)
        OR (kind == AUTHORIZATION AND rule != SAME_PRINCIPAL)

        THROW HarnessError(
            category = HUMAN_INTERACTION,
            code = "INVALID_PARKED_WAIT",
            message = "La espera no referencia lo que espera, o su regla de quien responde es inválida (una autorización solo la responde su propio principal)",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    wait: ParkedWait = ParkedWait(
        waitId = newWaitId(),
        runId = state.runId,
        sessionId = state.sessionId,
        kind = kind,
        requestId = requestId,
        challengeId = challengeId,
        requestedBy = requestedBy,
        responderRule = rule,
        designatedResponder = designated,
        status = PARKED,
        parkedAt = now(),
        expiresAt = expiresAt,
        resumedAt = NULL
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = RUN_PARKED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = state.agentId,
        traceId = execution.traceId,
        payload = wait
    )

    RETURN wait
END
```

```pseudocode
FUNCTION parkedAgentState(
    state: AgentState,
    wait: ParkedWait
) -> AgentState

    RETURN AgentState(
        runId = state.runId,
        sessionId = state.sessionId,
        agentId = state.agentId,
        status = runStatusForWait(wait.kind),
        currentTurn = state.currentTurn
    )
END
```

```pseudocode
FUNCTION createAuthorizationChallenge(
    principal: Principal,
    connectionRef: Text,
    expiresAt: Timestamp
) -> AuthorizationChallenge

    RETURN AuthorizationChallenge(
        challengeId = newAuthorizationChallengeId(),
        principal = principal,
        connectionRef = connectionRef,
        callbackRef = newCallbackRef(),
        createdAt = now(),
        expiresAt = expiresAt
    )
END
```

```pseudocode
FUNCTION linkRequestToWait(
    request: HumanInteractionRequest,
    wait: ParkedWait
) -> HumanInteractionRequest

    IF wait.requestId != request.id
        THROW HarnessError(
            category = HUMAN_INTERACTION,
            code = "WAIT_DOES_NOT_REFERENCE_REQUEST",
            message = "La espera no fue abierta por esta solicitud humana",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN HumanInteractionRequest(
        id = request.id,
        type = request.type,
        callId = request.callId,
        status = request.status,
        waitId = wait.waitId,
        requestedAt = request.requestedAt
    )
END
```

```pseudocode
FUNCTION findAddressedWait(
    waits: List<ParkedWait>,
    delivery: WaitDelivery
) -> ParkedWait

    FOR EACH wait IN waits
        IF wait.waitId == delivery.waitId
            RETURN wait
        END
    END

    THROW HarnessError(
        category = HUMAN_INTERACTION,
        code = "WAIT_NOT_ADDRESSED",
        message = "La entrega no nombra ninguna espera estacionada; el arnés nunca infiere a qué espera va dirigida",
        recoverable = FALSE,
        retryable = FALSE,
        metadata = {}
    )
END
```

```pseudocode
FUNCTION responderMayResolve(
    wait: ParkedWait,
    responder: Principal
) -> Boolean

    IF wait.responderRule == SAME_PRINCIPAL
        RETURN samePrincipal(wait.requestedBy, responder)
    END

    IF wait.responderRule == DESIGNATED_PRINCIPAL
        RETURN samePrincipal(wait.designatedResponder, responder)
    END

    RETURN responder.principalType == USER
        AND responder.tenantId != NULL
        AND responder.tenantId == wait.requestedBy.tenantId
END
```

```pseudocode
FUNCTION rejectDelivery(
    code: Text,
    message: Text,
    wait: ParkedWait,
    execution: ExecutionContext,
    agentId: AgentId
) -> HarnessError

    failure: HarnessError = HarnessError(
        category = HUMAN_INTERACTION,
        code = code,
        message = message,
        recoverable = FALSE,
        retryable = FALSE,
        metadata = {}
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = WAIT_DELIVERY_REJECTED,
        timestamp = now(),
        runId = wait.runId,
        sessionId = wait.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = failure
    )

    THROW failure
END
```

```pseudocode
FUNCTION acceptDelivery(
    wait: ParkedWait,
    delivery: WaitDelivery,
    execution: ExecutionContext,
    agentId: AgentId
) -> ParkedWait

    IF delivery.waitId != wait.waitId
        rejectDelivery("WAIT_NOT_ADDRESSED", "La entrega nombra otra espera", wait, execution, agentId)
    END

    IF wait.status != PARKED
        rejectDelivery("WAIT_ALREADY_RESUMED", "La espera ya fue reanudada o venció", wait, execution, agentId)
    END

    IF wait.expiresAt != NULL AND delivery.receivedAt > wait.expiresAt
        rejectDelivery("WAIT_EXPIRED", "La entrega llegó después del vencimiento de la espera", wait, execution, agentId)
    END

    IF NOT responderMayResolve(wait, delivery.responder)
        rejectDelivery("RESPONDER_NOT_AUTHORIZED", "Quien responde no cumple la regla de esta espera", wait, execution, agentId)
    END

    resumed: ParkedWait = ParkedWait(
        waitId = wait.waitId,
        runId = wait.runId,
        sessionId = wait.sessionId,
        kind = wait.kind,
        requestId = wait.requestId,
        challengeId = wait.challengeId,
        requestedBy = wait.requestedBy,
        responderRule = wait.responderRule,
        designatedResponder = wait.designatedResponder,
        status = RESUMED,
        parkedAt = wait.parkedAt,
        expiresAt = wait.expiresAt,
        resumedAt = now()
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = RUN_RESUMED,
        timestamp = now(),
        runId = wait.runId,
        sessionId = wait.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = resumed
    )

    RETURN resumed
END
```

La función de integración que cablea por fin `resumeAfterHumanResolution` (CH-13):

```pseudocode
FUNCTION resumeToolApprovalWait(
    wait: ParkedWait,
    delivery: WaitDelivery,
    pausedState: AgentState,
    execution: ExecutionContext,
    request: HumanInteractionRequest,
    call: ToolCall,
    candidatesSoFar: List<AgentMessage>,
    session: Optional<SessionState>,
    activeSubscriptions: List<EventSubscription>,
    usage: ExecutionUsage,
    toolExecutionSucceeded: Boolean,
    toolExecutionOutput: Value,
    finalModelContent: Value
) -> AgentState

    IF wait.kind != TOOL_APPROVAL OR wait.requestId != request.id
        THROW HarnessError(
            category = HUMAN_INTERACTION,
            code = "NOT_A_TOOL_APPROVAL_WAIT",
            message = "Esta espera no corresponde a la aprobación de esta solicitud",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    accepted: ParkedWait = acceptDelivery(wait, delivery, execution, pausedState.agentId)

    RETURN resumeAfterHumanResolution(
        pausedState, execution, request, delivery.outcome, delivery.responder.principalId,
        call, candidatesSoFar, session, activeSubscriptions, usage,
        toolExecutionSucceeded, toolExecutionOutput, finalModelContent
    )
END
```

`newWaitId`, `newAuthorizationChallengeId`, `newCallbackRef`, `newEventId` y `now` son utilidades
primitivas. `delivery.responder.principalId` se usa como el `ActorId` que `resolveHumanInteractionRequest`
(CH-06) registra: ahora ese actor es un principal verificado, no un texto libre. En
`responderMayResolve`, la rama `DESIGNATED_PRINCIPAL` nunca recibe `NULL`: `parkRun` ya lo rechazó.

Nótese lo que estas funciones **no** hacen:
- ninguna espera activamente: `parkRun` retorna y el proceso puede terminar;
- ninguna decide si una acción requiere aprobación ni la ejecuta;
- ninguna toca un token: `AuthorizationChallenge` no tiene dónde guardarlo;
- ninguna usa `channelRef` para decidir.

## 12. Transiciones de Estado (State Transitions)

El ciclo de vida de una `ParkedWait`:

```text
parkRun                          → PARKED    (RUN_PARKED)
acceptDelivery válida            → RESUMED   (RUN_RESUMED)
entrega no dirigida / no autorizada / tardía → sigue PARKED (WAIT_DELIVERY_REJECTED)
vencimiento (Preview)            → EXPIRED
```

Y el estado del run mientras espera (`runStatusForWait`, primer uso real de `PAUSED`):

```text
TOOL_APPROVAL, QUESTION      → WAITING_FOR_HUMAN
AUTHORIZATION, BUDGET_LIMIT  → PAUSED
reanudación                  → RUNNING (resumeAfterHumanResolution, CH-13)
```

## 13. Semántica de Fallos (Failure Semantics)

Cada fallo nuevo es un `HarnessError` de categoría `HUMAN_INTERACTION`:

```text
HUMAN_INTERACTION  INVALID_PARKED_WAIT               recoverable: FALSE, retryable: FALSE
HUMAN_INTERACTION  WAIT_DOES_NOT_REFERENCE_REQUEST   recoverable: FALSE, retryable: FALSE
HUMAN_INTERACTION  WAIT_NOT_ADDRESSED                recoverable: FALSE, retryable: FALSE
HUMAN_INTERACTION  WAIT_ALREADY_RESUMED              recoverable: FALSE, retryable: FALSE
HUMAN_INTERACTION  WAIT_EXPIRED                      recoverable: FALSE, retryable: FALSE
HUMAN_INTERACTION  RESPONDER_NOT_AUTHORIZED          recoverable: FALSE, retryable: FALSE
HUMAN_INTERACTION  NOT_A_TOOL_APPROVAL_WAIT          recoverable: FALSE, retryable: FALSE
```

Una entrega rechazada **no** cambia la espera: sigue `PARKED` y la persona correcta todavía puede
responder. Rechazar una entrega no es un fallo del run.

## 14. Eventos Producidos (Events Produced)

```text
RUN_PARKED              — un run quedó estacionado (payload: ParkedWait)
RUN_RESUMED             — una entrega válida reanudó la espera (payload: ParkedWait)
WAIT_DELIVERY_REJECTED  — una entrega no dirigida, tardía o no autorizada (payload: HarnessError)
```

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **Conocer el `waitId` no basta.** Un enlace de aprobación reenviado a otra persona no le da derecho
  a aprobar: `responderMayResolve` exige que su `Principal` cumpla la regla de la espera (INV-E18).
- **Una autorización solo la da su dueño.** `parkRun` rechaza una espera `AUTHORIZATION` que no sea
  `SAME_PRINCIPAL`. Nadie de la misma empresa puede conectar su propia cuenta en nombre de otro.
- **El token nunca pasa por el run.** El callback lo entrega a `CredentialBroker`; el run solo sabe
  "autorizado o no". Así nunca puede llegar al contexto del modelo (INV-E08).
- **El canal no da autoridad.** Una respuesta por un canal "interno" no vale más que una por correo:
  lo que vale es el `Principal` verificado.
- **Nunca se adivina.** Si una sesión tiene varias esperas, una respuesta que no nombra una se
  rechaza en vez de aplicarse a "la más probable".

## 16. Tests (Tests)

```text
TEST ParkRunReturnsWithoutHoldingAProcess
TEST ApprovalAndQuestionWaitsSetWaitingForHuman
TEST AuthorizationAndBudgetWaitsSetPaused
TEST AuthorizationWaitMustBeAnsweredByItsOwnPrincipal
TEST DesignatedWaitWithoutDesignatedResponderIsInvalid
TEST DeliveryWithoutMatchingWaitIdIsNeverInferred
TEST DeliveryToAResumedWaitIsRejected
TEST LateDeliveryIsRejectedAsExpired
TEST ResponderOutsideTheRuleIsRejectedAndWaitStaysParked
TEST SameTenantRuleRejectsServicePrincipals
TEST ChannelNeverChangesTheDecision
TEST AuthorizationChallengeNeverContainsAToken
TEST ResumeToolApprovalWaitInvokesResumeAfterHumanResolution
TEST ToolIsNeverExecutedBeforeAnAcceptedDelivery
TEST RequestWithoutWaitIdBehavesAsV1
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.2 en curso, después de CH-33)

Components — 24
 ├── CMP-006 HumanInteractionService  (+ linkRequestToWait)
 └── CMP-024 ResumptionCoordinator    (CH-33, nuevo — plano Execution)

Contracts — 45
 ├── C-015 HumanInteractionRequest v2 (CH-06 → modificado en CH-33: waitId)
 ├── C-044 ParkedWait                 (CH-33, nuevo)
 └── C-045 AuthorizationChallenge     (CH-33, nuevo)

Primer uso real de PAUSED (C-013) y de resumeAfterHumanResolution (CH-13).
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El vencimiento activo.** Qué pasa cuando `expiresAt` llega sin respuesta (pasar a `EXPIRED`,
  avisar, cancelar el run) necesita un disparador de tiempo: es de los schedules (CH-34).
- **Reanudar preguntas, autorizaciones y límites de presupuesto.** Este capítulo cablea la
  aprobación (`resumeToolApprovalWait`). Las otras tres siguen el mismo patrón con
  `resolveHumanInteractionRequest` (CH-06), `CredentialBroker` (CH-16) y `ExecutionController`
  (CH-07); se integran en CH-36.
- **A qué canal avisar** que hay una espera. Es la dirección de continuación (CH-34).
- **Esperas de un run hijo** reenviadas al padre: invocación entre agentes (CH-42).
- **El protocolo OAuth** en sí: es un adaptador de callback, fuera del núcleo.

## 19. Siguiente Incremento (Next Increment)

Ahora un run puede esperar días sin ocupar un proceso, y reanudarse por cualquier canal. Pero el
arnés todavía no sabe **a dónde** contestar: una conversación que empezó en un canal de chat, o por
un webhook, no tiene una dirección a la que el agente pueda volver a escribir, y los schedules no
existen.

El siguiente capítulo introduce las **direcciones de continuación** (P-34):
- canales, WebSocket, webhooks y schedules como fuentes de activación;
- una dirección de continuación con a lo sumo una sesión dueña (INV-E19).

Será CH-34 ("Canales y Direcciones de Continuación"), con el componente `ContinuationRegistry`.
`next_chapter` queda en `null` porque CH-34 todavía no existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): un run que espera queda estacionado, pero nadie decide qué respuesta lo
   reanuda ni quién puede darla; `PAUSED` nunca se produce.
2. **Patrones** (= §3): cada tipo de espera se imagina con su propio mecanismo, o no se imagina, y
   ninguno valida destino ni autoridad de la respuesta.
3. **Estructuras** (= §8): `ResumptionCoordinator` (CMP-024), `ParkedWait` (C-044),
   `AuthorizationChallenge` (C-045) y `HumanInteractionRequest` v2.
4. **Modelos mentales** (= §4): P-33, INV-E18 y P-31.

**Bucles de retroalimentación**

- **Refuerzo:** si esperar ocupa un proceso, las esperas largas reducen la capacidad y generan más
  esperas. Estacionar sin cómputo corta la espiral.
- **Equilibrio:** INV-E18. Solo la entrega dirigida y autorizada reanuda una espera.

**Punto de apalancamiento**

La decisión con mayor efecto es que la entrega nombre su espera y traiga un `Principal` verificado:
`findAddressedWait` nunca infiere y `responderMayResolve` decide con la regla de la `ParkedWait`
(C-044), no con el canal.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Qué hace `parkRun`, qué `AgentRunStatus` decide `runStatusForWait` para cada `WaitKind`, y por
   qué después de estacionar no queda ningún proceso esperando? *(pregunta guía 1)*
2. ¿Cómo encuentra `findAddressedWait` la espera de una `WaitDelivery`, y qué error lanza cuando la
   entrega no nombra ninguna espera estacionada? *(pregunta guía 2)*
3. ¿Qué `ResponderRule` exige `parkRun` para una espera `AUTHORIZATION`, qué contiene y qué no
   contiene un `AuthorizationChallenge`, y a dónde va el token? *(pregunta guía 3)*
4. ¿Cuáles son los cuatro `WaitKind`, qué tienen en común como `ParkedWait`, y qué función de CH-13
   invoca `resumeToolApprovalWait` después de `acceptDelivery`? *(pregunta guía 4)*

### Explicar

1. `HumanInteractionService` y `ResumptionCoordinator` participan en toda aprobación humana. Explica
   qué decide cada uno, y por qué la solicitud y la espera son dos cosas distintas.
2. Explica por qué `ParkedWait` guarda `requestedBy` y una regla de quién puede responder, y qué
   ataque sería posible si cualquier respuesta con el `waitId` correcto reanudara la espera.

### Conectar

1. En CH-31, `continuationAllowedForCaller` decidía si un `Principal` podía continuar una sesión con
   `SAME_PRINCIPAL` o `SAME_TENANT`. ¿En qué se parece y en qué se diferencia `responderMayResolve`,
   y por qué una espera necesita además `DESIGNATED_PRINCIPAL`?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
