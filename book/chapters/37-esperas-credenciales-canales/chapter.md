---
id: CH-37
title: "Esperas, Credenciales y Canales Completos"
starting_version: "0.2"
ending_version: "0.2.1"
introduces_components: []
introduces_contracts: []
modifies_contracts: []
constitutional_articles: [P-11, P-16, P-31, P-33, P-34, INV-14, INV-15, INV-E08, INV-E18, INV-E19]
previous_chapter: CH-36
next_chapter: CH-38
retrieval_set:
  expected_outcome:
    id: EO-CH37
    text: |
      Al terminar este capítulo podrás decidir qué pasa con cada tipo de espera cuando llega su
      respuesta y cuando no llega nunca, explicar cómo un usuario autoriza el acceso a un servicio sin
      que su credencial pase por el run, y decidir cuándo una conversación externa deja de pertenecer
      a una sesión y por dónde el arnés le contesta.
  skeleton:
    id: SK-CH37
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
    - id: GQ-CH37-01
      text: |
        Si nadie responde nunca a una aprobación que el agente pidió, ¿el run debería quedarse
        esperando para siempre? ¿Quién se da cuenta de que ya pasó el plazo?
      answered_by: RQ-CH37-01
    - id: GQ-CH37-02
      text: |
        Cuando un usuario autoriza al agente a usar su calendario, el servicio externo devuelve un
        token. ¿Ese token debería pasar por el run que estaba esperando?
      answered_by: RQ-CH37-02
    - id: GQ-CH37-03
      text: |
        Si un run se detuvo porque se quedó sin presupuesto y un operador aprueba seguir, ¿quién decide
        cuánto presupuesto más tiene: el operador o el arnés?
      answered_by: RQ-CH37-03
    - id: GQ-CH37-04
      text: |
        Cuando una sesión termina, ¿qué pasa con el hilo de chat que le pertenecía? ¿Y a dónde debería
        el agente enviar su respuesta o el aviso de que está esperando algo?
      answered_by: RQ-CH37-04
  systems_lens:
    iceberg_visible_fact: |
      Una espera sin respuesta nunca vence, las preguntas, autorizaciones y límites de presupuesto no
      tienen reanudación durable, nadie abre una autorización cuando falta la credencial del usuario,
      las direcciones de continuación nunca se liberan y el arnés no tiene cómo contestar por el canal
      (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que CH-33 y CH-34 modelaron la mitad de entrada de cada mecanismo —
      estacionar, entregar, reclamar — y dejaron la mitad de salida — vencer, reanudar cada tipo,
      liberar, responder — "para la integración", que CH-36 no escribió (ver sección 3).
    iceberg_structures: |
      Este capítulo amplía ResumptionCoordinator (vencimiento), CredentialBroker (credencial faltante
      y callback) y ContinuationRegistry (liberar y responder), dentro de sus owns, y agrega cuatro
      funciones de integración con los tipos embebidos OutboundMessage y AuthorizationParking (ver
      sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-33 (esperar es durable, también cuando vence), INV-E08 (el token lo
      resuelve y guarda CredentialBroker, nunca la espera) y P-34 (se responde a la dirección que la
      sesión posee, nunca a una inferida) (ver sección 4).
    reinforcing_loop: |
      Si las esperas no vencen, cada aprobación olvidada deja un run estacionado para siempre y una
      dirección reclamada que nadie libera; cuantas más esperas olvidadas, más direcciones bloqueadas
      y más mensajes que no llegan a ninguna sesión útil. El vencimiento activo corta la espiral.
    balancing_loop: |
      expiresAt es el mecanismo de equilibrio: toda espera tiene un plazo, y al cumplirse el run sale
      de la espera por el mismo camino que un rechazo.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que acceptAuthorizationCallback produzca una
      WaitDelivery sin credenciales — solo "autorizado o no" — mientras el token va directo a
      CredentialBroker, para que la autorización interactiva cumpla INV-E08 de punta a punta.
  recall_questions:
    - id: RQ-CH37-01
      text: |
        ¿Qué selecciona dueParkedWaits, qué exige expireParkedWait antes de marcar una espera EXPIRED,
        y por qué camino entra el schedule que las vence?
    - id: RQ-CH37-02
      text: |
        ¿Qué verifica acceptAuthorizationCallback, qué produce, y dónde queda el token de la
        autorización?
    - id: RQ-CH37-03
      text: |
        En resumeDurableBudgetLimit, ¿qué función decide si el run continúa con el presupuesto
        extendido, y qué pasa si el operador rechaza o si esa función no devuelve CONTINUE?
    - id: RQ-CH37-04
      text: |
        ¿Qué hace releaseAddressesForSession con cada SessionEndReason, y qué exige buildOutboundMessage
        para enviar una respuesta o un aviso de espera?
  explain_prompts:
    - id: EP-CH37-01
      text: |
        ResumptionCoordinator ya decidía qué espera reanuda una entrega. Explica, como si hablaras con
        alguien sin contexto técnico, por qué decidir que una espera venció también le pertenece, y
        qué parte del vencimiento le toca a la integración.
      target_entity: CMP-024
    - id: EP-CH37-02
      text: |
        Explica por qué detectar que falta la credencial del usuario y recibir el token del callback
        le pertenecen a CredentialBroker, y qué se rompería si el token llegara al run dentro de la
        respuesta que reanuda la espera.
      target_entity: CMP-014
  interleaved_questions:
    - id: IQ-CH37-01
      text: |
        En CH-33, parkRun exigía SAME_PRINCIPAL para una espera AUTHORIZATION y createAuthorizationChallenge
        generaba un callbackRef opaco. ¿Qué dos verificaciones de acceptAuthorizationCallback dependen
        de esas decisiones de CH-33, y qué ataque evita cada una?
      current_chapter_entities: [CMP-014]
      prior_chapter_entities: [C-044, C-045, CMP-024]
      prior_chapter: CH-33
  flashcards:
    - id: FC-CH37-01
      front: |
        ¿Cómo vence una espera estacionada?
      back: |
        Un schedule interno (sourceKind = SCHEDULE, admitido con un Principal RUNTIME) llama a
        dueParkedWaits y expireParkedWait: la espera pasa a EXPIRED (WAIT_EXPIRED) y el run continúa
        como con un rechazo; un BUDGET_LIMIT vencido termina el run.
      source_entity: CMP-024
      chapter_introduced_in: CH-37
      review_stage: DAY_1
    - id: FC-CH37-02
      front: |
        ¿Qué recibe y qué produce acceptAuthorizationCallback (CredentialBroker)?
      back: |
        Recibe el callbackRef, el Principal que autorizó y la señal tokenStored del Secret Store; nunca
        el token. Verifica desafío, principal y vencimiento, y produce una WaitDelivery APPROVED o
        REJECTED para ResumptionCoordinator.
      source_entity: CMP-014
      chapter_introduced_in: CH-37
      review_stage: DAY_1
    - id: FC-CH37-03
      front: |
        ¿Cuándo libera ContinuationRegistry la dirección de una sesión, y a dónde responde el arnés?
      back: |
        La libera cuando la sesión se cierra (CLOSED) o vence (EXPIRED); la conserva durante un handoff
        (HANDED_OFF). Responde solo a la dirección ACTIVE que la sesión posee; un aviso de espera lleva
        su waitId.
      source_entity: CMP-025
      chapter_introduced_in: CH-37
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH37-01
      recall_question: RQ-CH37-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH37-02
      recall_question: RQ-CH37-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH37-03
      recall_question: RQ-CH37-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH37-04
      recall_question: RQ-CH37-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 37 — Esperas, Credenciales y Canales Completos

> **Regla de v0.2.1:** una garantía que solo funciona a la entrada no es una garantía; también tiene
> que funcionar cuando la respuesta no llega, cuando llega con un secreto y cuando el arnés tiene que
> contestar.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir qué pasa con cada tipo de espera
cuando llega su respuesta y cuando no llega nunca. También podrás explicar cómo un usuario autoriza el
acceso a un servicio sin que su credencial pase por el run, y decidir cuándo una conversación externa
deja de pertenecer a una sesión y por dónde el arnés le contesta.

**Esqueleto.** Primer capítulo de la versión 0.2.1, que cierra la deuda de la versión 0.2
(`registry/debt.yaml`: D-009..D-013). No introduce componentes ni contratos: amplía tres componentes
dentro de lo que ya poseen y agrega cuatro funciones de integración.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si nadie responde nunca a una aprobación que el agente pidió, ¿el run debería quedarse esperando
   para siempre? ¿Quién se da cuenta de que ya pasó el plazo?
2. Cuando un usuario autoriza al agente a usar su calendario, el servicio externo devuelve un token.
   ¿Ese token debería pasar por el run que estaba esperando?
3. Si un run se detuvo porque se quedó sin presupuesto y un operador aprueba seguir, ¿quién decide
   cuánto presupuesto más tiene: el operador o el arnés?
4. Cuando una sesión termina, ¿qué pasa con el hilo de chat que le pertenecía? ¿Y a dónde debería el
   agente enviar su respuesta o el aviso de que está esperando algo?

## 1. Arquitectura Actual (Current Architecture)

- **`ResumptionCoordinator` (CMP-024, CH-33)** estaciona un run en una `ParkedWait` (C-044) de cuatro
  tipos (`TOOL_APPROVAL`, `QUESTION`, `AUTHORIZATION`, `BUDGET_LIMIT`) con un `expiresAt` opcional, y
  valida la entrega dirigida (`acceptDelivery`, INV-E18). `WaitStatus` ya tiene `EXPIRED`, pero nada lo
  produce.
- **`CredentialBroker` (CMP-014, CH-16 y CH-35)** resuelve una `CredentialReference` opaca y, desde
  CH-35, la credencial del egress. Si el secreto no existe, falla con `CREDENTIAL_NOT_FOUND`.
- **`AuthorizationChallenge` (C-045, CH-33)** representa una autorización interactiva, sin token.
- **`ContinuationRegistry` (CMP-025, CH-34)** reclama y libera direcciones
  (`releaseContinuationAddress`), pero nadie decide **cuándo** liberar.
- **La integración durable (CH-36)** reanuda de forma durable solo la aprobación
  (`resumeDurableApproval`), con las funciones que expuso la revisión v0.2.1 de CH-13.

## 2. El Problema (Problem)

CH-33 y CH-34 construyeron la **entrada** de cada mecanismo. Faltó la **salida**:
- **una aprobación que nadie contesta** deja el run estacionado para siempre, y la dirección de su
  sesión reclamada para siempre;
- **una pregunta, una autorización o un límite de presupuesto** se pueden estacionar, pero no hay
  forma durable de reanudarlos;
- **nadie abre la autorización.** Cuando a una herramienta le falta la credencial del usuario,
  `CredentialBroker` falla, en vez de pedirle al usuario que autorice;
- **nadie recibe el token.** Cuando el usuario autoriza, el servicio externo devuelve un token, y no
  hay un lugar definido para él;
- **nada libera las direcciones** cuando la sesión termina;
- **el arnés no contesta.** No hay forma de enviar la respuesta, ni el aviso de "estoy esperando tu
  aprobación", por el canal de la conversación.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **`EXPIRED` existe, pero no hay reloj.** `expiresAt` se guarda y se compara al recibir una entrega
  tardía (CH-33), pero si la entrega no llega nunca, nadie lo mira.
- **`resumeDurableApproval` sirve solo para aprobaciones.** Una pregunta no ejecuta ninguna tool; una
  autorización no tiene `HumanInteractionRequest`; un límite de presupuesto necesita una decisión de
  `ExecutionController`, no una resolución humana.
- **`CREDENTIAL_NOT_FOUND` mezcla dos casos:** "este secreto no existe" y "este usuario todavía no
  conectó su cuenta". Solo el segundo se resuelve con una autorización interactiva.
- **`releaseContinuationAddress` sabe liberar, pero no sabe cuándo.** Sin regla, cada integración
  decidiría a su manera, y un handoff podría liberar una dirección que todavía se usa.
- **CH-36 dejó todo esto en su §18.** Es la deuda D-009..D-013 de `registry/debt.yaml`.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-11   UI is an adapter, not part of the core.
           El envío por el canal es un adaptador; el arnés solo decide a qué dirección.
    P-16   Activation is independent from execution.
           El vencimiento entra como un ActivationRequest de tipo SCHEDULE.
    P-31   Identity travels with every turn.
           La credencial faltante es la de caller.current; el callback lo firma el mismo Principal.
    P-33   Waiting is durable and consumes no compute.
           Ahora también al vencer, y para los cuatro tipos de espera.
    P-34   External conversations are addressed, not inferred.
           Se responde solo a la dirección que la sesión posee.

Invariants preserved
    INV-14   Human Interaction nunca depende de una interfaz particular.
             El aviso de espera sale por la dirección, sea cual sea el canal.
    INV-15   Una acción que requiere aprobación no se ejecuta antes de una resolución válida.
             Vencer es no aprobar.
    INV-E08  Credentials are resolved by a CredentialBroker and SHOULD NOT enter model context.
             El token del callback llega a CredentialBroker, nunca a la espera ni al run.
    INV-E18  A delivery resumes only the wait it addresses.
             El aviso de espera lleva su waitId; el callback se vuelve una WaitDelivery dirigida.
    INV-E19  A continuation address has at most one owning session at a time.
             Liberar al cerrar o vencer la sesión permite que otra la reclame después.

Component ownership changes
    Ninguno nuevo. ResumptionCoordinator, CredentialBroker y ContinuationRegistry ganan funciones
    dentro de sus owns (ver sección 8).

Contract changes
    Ninguno. Tipos embebidos: SessionEndReason, OutboundKind, OutboundMessage, AuthorizationParking.

Security implications
    El token nunca pasa por el run; el callback solo lo responde el mismo usuario; el arnés nunca
    responde a una dirección que no posee (ver sección 15).

Observability implications
    Nuevos AgentEventType: WAIT_EXPIRED y CALLER_AUTHORIZATION_RECEIVED.

Deterministic vs agentic boundary
    Sin cambios: el modelo nunca decide que una espera venció, ni a dónde se responde.
```

## 5. Conceptos Nuevos (New Concepts)

- **Vencimiento activo** (*active wait expiry*): un schedule interno busca las esperas cuyo plazo ya
  pasó y las marca `EXPIRED`. Vencer es otra forma de no recibir un "sí":
  - una aprobación o una autorización vencidas continúan el turno con la observación `WAIT_EXPIRED`,
    igual que un rechazo;
  - una pregunta vencida continúa con esa misma observación, y el modelo decide qué hacer;
  - un límite de presupuesto vencido termina el run.
- **Credencial faltante del llamante:** a diferencia de un secreto que no existe, es una cuenta que
  el usuario todavía no conectó. Se resuelve pidiéndole que autorice; el resultado queda guardado a
  su nombre.
- **Callback sin token:** cuando el usuario autoriza, el servicio externo devuelve un token al
  adaptador de callback. El adaptador lo entrega al Secret Store, y a `CredentialBroker` solo le
  avisa "quedó guardado". La espera recibe "autorizado" o "no autorizado", nada más.
- **Fin de sesión:** una sesión termina porque se cierra, porque vence o porque pasa a un humano
  (handoff). Las dos primeras liberan sus direcciones; la tercera no, porque la conversación sigue.
- **Respuesta por el canal** (*outbound reply*): el arnés envía un mensaje a la dirección que la
  sesión posee. Hay dos tipos: una respuesta, o un aviso de espera que lleva el `waitId` para que la
  contestación sea una entrega dirigida.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `ParkedWait` (C-044), `AuthorizationChallenge` (C-045), `ContinuationAddress`
  (C-046), `StepRecord` (C-042), `Principal` (C-040), `SandboxSession` (C-047),
  `CapabilityDescriptor` (C-018), `ToolCall` (C-008), `ToolResult` (C-009), `AgentState` (C-003),
  `ExecutionContext` (C-004), `ExecutionBudget` (C-012), `ExecutionDecision` (C-017),
  `HumanInteractionRequest` (C-015), `HumanInteractionResolution` (C-016), `AgentMessage` (C-001),
  `SessionState` (C-020), `EventSubscription` (C-019), `AgentEvent` (C-010), `HarnessError` (C-011);
- **primitivos:** `SessionId`, `AgentId`, `CapabilityId`, `Timestamp`.

| Identificador (heredado, sin `C-XXX` propio) | Introducido en | Rol en este capítulo |
|---|---|---|
| `WaitId` | CH-33 §6 | identificador de una espera |
| `WaitDelivery` | CH-33 §6 | la respuesta que llega por un canal, o la que produce el callback |
| `HumanInteractionOutcome` | CH-06 §6 | `APPROVED` / `REJECTED` / `PROVIDED` de una entrega |
| `ContinuationClaim` | CH-34 §6 | reclamos durables de direcciones |
| `ExecutionUsage` | CH-07 §6 | uso del run, para decidir si el presupuesto extendido alcanza |
| `AgentEventType` | CH-00 | se agregan `WAIT_EXPIRED` y `CALLER_AUTHORIZATION_RECEIVED` |
| `ErrorCategory` | CH-00 | reutiliza `HUMAN_INTERACTION`, `CREDENTIAL` y `ADMISSION` |

### `SessionEndReason` — por qué termina una sesión (embebido)

```pseudocode
ENUM SessionEndReason
    CLOSED
    EXPIRED
    HANDED_OFF
END
```

### `OutboundKind` y `OutboundMessage` — lo que el arnés envía por el canal (embebidos)

```pseudocode
ENUM OutboundKind
    REPLY
    WAIT_NOTICE
END
```

```pseudocode
STRUCT OutboundMessage
    address: ContinuationAddress
    sessionId: SessionId
    kind: OutboundKind
    content: Value
    waitId: Optional<WaitId>
    preparedAt: Timestamp
END
```

`waitId` solo tiene valor en un `WAIT_NOTICE`. El adaptador de salida del canal (infraestructura)
es quien lo envía.

### `AuthorizationParking` — el run estacionado por una credencial faltante (embebido)

```pseudocode
STRUCT AuthorizationParking
    challenge: AuthorizationChallenge
    wait: ParkedWait
    notice: OutboundMessage
END
```

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

**Este capítulo no introduce ni modifica contratos**, por la restricción de la versión 0.2.1: los ids
de la versión 0.3 (C-049..C-066) no se corren. `registry/contracts.yaml` sigue en 48 contratos.

## 8. Responsabilidades de Componentes (Component Responsibilities)

**Este capítulo no introduce componentes.** Tres componentes ganan funciones dentro de su `owns`
literal:

```text
ResumptionCoordinator (CMP-024)
    owns: "Approvals, questions, interactive authorizations and budget limits MUST park the run
           durably …" (P-33) y "rechazar por defecto una entrega a una espera ya reanudada,
           vencida o no dirigida"
    nuevas: dueParkedWaits, expireParkedWait, expiryObservation
    no posee: disparar el schedule (Ingress Adapter SCHEDULE, CH-34), ni decidir qué hace el
              turno después (la integración)

CredentialBroker (CMP-014)
    owns: "verificar que el secreto solicitado … exista y no haya vencido, antes de producir
           cualquier CredentialReference" y "garantizar … que el valor real del secreto nunca
           aparezca en ningún dato que este componente produce" (INV-E08)
    nuevas: detectMissingCallerCredential, acceptAuthorizationCallback
    no posee: el protocolo OAuth ni guardar el token (adaptador de callback y Secret Store,
              infraestructura), ni reanudar la espera (ResumptionCoordinator)

ContinuationRegistry (CMP-025)
    owns: "A continuation address has at most one owning session at a time" (INV-E19) —
          reclamar, liberar y rechazar un segundo dueño
    nuevas: releaseAddressesForSession, outboundAddressFor, buildOutboundMessage
    no posee: enviar el mensaje por el canal (adaptador de salida, P-11), ni decidir que la
              sesión terminó (SessionManager / HandoffCoordinator)
```

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
Vencimiento (D-009)
    Ingress Adapter SCHEDULE → ActivationRequest(sourceKind = SCHEDULE) → admitWithVerifiedIdentity
    (Principal RUNTIME) → dueParkedWaits → expireParkedWait → expiryObservation
    → resumeTurnWithObservation (CH-13) | terminateAgentRunOperationally (CH-13, BUDGET_LIMIT)

Autorización (D-011 + D-010)
    runDurableGovernedStep (CH-36, ALLOW) → detectMissingCallerCredential → parkForMissingCredential
    [createAuthorizationChallenge + parkRun (CH-33) + buildOutboundMessage] → el proceso termina
    … adaptador de callback → Secret Store (token) → acceptAuthorizationCallback → WaitDelivery
    → resumeDurableAuthorization → acceptDelivery (CH-33) → journal + executeToolCallIsolated (CH-35)

Pregunta y presupuesto (D-010)
    resumeDurableQuestion  → acceptDelivery → resolveHumanInteractionRequest (CH-06) → resumeTurnWithObservation
    resumeDurableBudgetLimit → acceptDelivery → evaluateExecutionContinuation (CH-07)
                               → continúa | terminateAgentRunOperationally (CH-13)

Direcciones (D-012 + D-013)
    fin de sesión → releaseAddressesForSession → releaseContinuationAddress (CH-34)
    respuesta o aviso → outboundAddressFor → buildOutboundMessage → adaptador de salida del canal
```

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
Schedule → ResumptionCoordinator (vencer)
Tool sin credencial → CredentialBroker (detectar) → ResumptionCoordinator (estacionar) → ContinuationRegistry (avisar)
Callback → CredentialBroker (sin token) → ResumptionCoordinator (reanudar)
Fin de sesión → ContinuationRegistry (liberar)
```

**Vista 2 — Sequence: una autorización interactiva de punta a punta**

```text
runDurableGovernedStep: PolicyEngine ALLOW sobre "leer calendario"
   │ detectMissingCallerCredential(descriptor, "calendario", execution, FALSE) → TRUE
   │ parkForMissingCredential → AuthorizationChallenge + ParkedWait(AUTHORIZATION, SAME_PRINCIPAL)
   │                          → OutboundMessage(WAIT_NOTICE, waitId) por el hilo de la sesión
   ▼ (el proceso termina; el paso queda STARTED, sin toolCall)
Usuario autoriza en el servicio externo → adaptador de callback → Secret Store guarda el token
   │ acceptAuthorizationCallback(challenge, wait, callbackRef, usuario, tokenStored = TRUE)
   │   → CALLER_AUTHORIZATION_RECEIVED + WaitDelivery(APPROVED)   (sin token)
   │ resumeDurableAuthorization → acceptDelivery → recordToolCallBeforeExecution
   │   → executeToolCallIsolated (el egress lleva la credencial desde el borde, CH-35) → COMMITTED
```

**Vista 2b — Sequence: una aprobación que vence**

```text
Schedule "expirar-esperas" → ActivationRequest(SCHEDULE) → ADMIT (Principal RUNTIME)
   │ dueParkedWaits(waits, now) → [espera de aprobación con expiresAt vencido]
   │ expireParkedWait → EXPIRED + WAIT_EXPIRED
   │ expiryObservation → observación WAIT_EXPIRED → resumeTurnWithObservation
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

### ResumptionCoordinator: vencer esperas (D-009)

```pseudocode
FUNCTION dueParkedWaits(
    waits: List<ParkedWait>,
    now: Timestamp
) -> List<ParkedWait>

    due: List<ParkedWait> = []

    FOR EACH wait IN waits
        IF wait.status == PARKED AND wait.expiresAt != NULL AND wait.expiresAt <= now
            due = append(due, wait)
        END
    END

    RETURN due
END
```

```pseudocode
FUNCTION expireParkedWait(
    wait: ParkedWait,
    firedAt: Timestamp,
    execution: ExecutionContext,
    agentId: AgentId
) -> ParkedWait

    IF wait.status == EXPIRED
        RETURN wait
    END

    IF wait.status != PARKED OR wait.expiresAt == NULL OR firedAt < wait.expiresAt
        THROW HarnessError(
            category = HUMAN_INTERACTION,
            code = "WAIT_NOT_DUE",
            message = "Solo vence una espera estacionada cuyo plazo ya pasó",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    expired: ParkedWait = ParkedWait(
        waitId = wait.waitId,
        runId = wait.runId,
        sessionId = wait.sessionId,
        kind = wait.kind,
        requestId = wait.requestId,
        challengeId = wait.challengeId,
        requestedBy = wait.requestedBy,
        responderRule = wait.responderRule,
        designatedResponder = wait.designatedResponder,
        status = EXPIRED,
        parkedAt = wait.parkedAt,
        expiresAt = wait.expiresAt,
        resumedAt = NULL
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = WAIT_EXPIRED,
        timestamp = now(),
        runId = wait.runId,
        sessionId = wait.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = expired
    )

    RETURN expired
END
```

```pseudocode
FUNCTION expiryObservation(
    wait: ParkedWait
) -> AgentMessage

    IF wait.status != EXPIRED
        THROW HarnessError(
            category = HUMAN_INTERACTION,
            code = "WAIT_NOT_EXPIRED",
            message = "Solo una espera EXPIRED produce la observación de vencimiento",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN AgentMessage(
        id = newMessageId(),
        role = TOOL,
        content = HarnessError(
            category = HUMAN_INTERACTION,
            code = "WAIT_EXPIRED",
            message = "La espera venció sin respuesta; la acción que dependía de ella no se ejecutó",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        ),
        timestamp = now()
    )
END
```

### CredentialBroker: credencial faltante y callback (D-011)

```pseudocode
FUNCTION detectMissingCallerCredential(
    descriptor: CapabilityDescriptor,
    credentialName: Text,
    execution: ExecutionContext,
    secretExistsForCaller: Boolean
) -> Boolean

    IF secretExistsForCaller
        RETURN FALSE
    END

    RETURN execution.caller != NULL AND execution.caller.current.principalType == USER
END
```

```pseudocode
FUNCTION acceptAuthorizationCallback(
    challenge: AuthorizationChallenge,
    wait: ParkedWait,
    callbackRef: Text,
    responder: Principal,
    tokenStored: Boolean,
    receivedAt: Timestamp,
    execution: ExecutionContext,
    agentId: AgentId
) -> WaitDelivery

    IF callbackRef != challenge.callbackRef
        OR wait.challengeId != challenge.challengeId
        OR NOT samePrincipal(challenge.principal, responder)
        OR receivedAt > challenge.expiresAt

        THROW HarnessError(
            category = CREDENTIAL,
            code = "AUTHORIZATION_CALLBACK_REJECTED",
            message = "El callback no corresponde a este desafío, lo firma otro principal o llegó vencido",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    outcome: HumanInteractionOutcome = REJECTED

    IF tokenStored
        outcome = APPROVED
    END

    delivery: WaitDelivery = WaitDelivery(
        waitId = wait.waitId,
        responder = responder,
        channelRef = "authorization-callback",
        outcome = outcome,
        value = NULL,
        receivedAt = receivedAt
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = CALLER_AUTHORIZATION_RECEIVED,
        timestamp = now(),
        runId = wait.runId,
        sessionId = wait.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = delivery
    )

    RETURN delivery
END
```

`samePrincipal` es la función de CH-33. `tokenStored` es la señal del Secret Store (infraestructura):
el valor del token nunca llega a esta función.

### ContinuationRegistry: liberar y responder (D-012, D-013)

```pseudocode
FUNCTION releaseAddressesForSession(
    claims: List<ContinuationClaim>,
    sessionId: SessionId,
    reason: SessionEndReason,
    execution: ExecutionContext,
    agentId: AgentId
) -> List<ContinuationClaim>

    IF reason == HANDED_OFF
        RETURN claims
    END

    updated: List<ContinuationClaim> = []

    FOR EACH claim IN claims
        IF claim.status == ACTIVE AND claim.sessionId == sessionId
            updated = append(updated, releaseContinuationAddress(claim, sessionId, execution, agentId))
        ELSE
            updated = append(updated, claim)
        END
    END

    RETURN updated
END
```

```pseudocode
FUNCTION outboundAddressFor(
    claims: List<ContinuationClaim>,
    sessionId: SessionId
) -> Optional<ContinuationAddress>

    FOR EACH claim IN claims
        IF claim.status == ACTIVE AND claim.sessionId == sessionId
            RETURN claim.address
        END
    END

    RETURN NULL
END
```

```pseudocode
FUNCTION buildOutboundMessage(
    claims: List<ContinuationClaim>,
    sessionId: SessionId,
    kind: OutboundKind,
    content: Value,
    waitId: Optional<WaitId>
) -> OutboundMessage

    address: Optional<ContinuationAddress> = outboundAddressFor(claims, sessionId)

    IF address == NULL OR (kind == WAIT_NOTICE AND waitId == NULL)
        THROW HarnessError(
            category = ADMISSION,
            code = "NO_OUTBOUND_ADDRESS",
            message = "La sesión no posee ninguna dirección activa, o un aviso de espera no nombra su waitId; el arnés nunca responde a una dirección inferida",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN OutboundMessage(
        address = address,
        sessionId = sessionId,
        kind = kind,
        content = content,
        waitId = waitId,
        preparedAt = now()
    )
END
```

### Integración: estacionar por credencial y reanudar cada tipo de espera (D-010)

```pseudocode
FUNCTION parkForMissingCredential(
    state: AgentState,
    execution: ExecutionContext,
    connectionRef: Text,
    challengeExpiresAt: Timestamp,
    claims: List<ContinuationClaim>
) -> AuthorizationParking

    challenge: AuthorizationChallenge = createAuthorizationChallenge(
        execution.caller.current, connectionRef, challengeExpiresAt
    )

    wait: ParkedWait = parkRun(
        state, AUTHORIZATION, NULL, challenge.challengeId, execution.caller.current,
        SAME_PRINCIPAL, NULL, challengeExpiresAt, execution
    )

    notice: OutboundMessage = buildOutboundMessage(
        claims, state.sessionId, WAIT_NOTICE, challenge.callbackRef, wait.waitId
    )

    RETURN AuthorizationParking(challenge = challenge, wait = wait, notice = notice)
END
```

```pseudocode
FUNCTION resumeDurableQuestion(
    wait: ParkedWait,
    delivery: WaitDelivery,
    request: HumanInteractionRequest,
    pausedState: AgentState,
    execution: ExecutionContext,
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

    answer: AgentMessage = AgentMessage(
        id = newMessageId(),
        role = USER,
        content = delivery.value,
        timestamp = now()
    )

    RETURN resumeTurnWithObservation(
        resumedState, execution, append(candidatesSoFar, answer), session, activeSubscriptions,
        usage, finalModelContent
    )
END
```

```pseudocode
FUNCTION resumeDurableAuthorization(
    wait: ParkedWait,
    delivery: WaitDelivery,
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
            category = CREDENTIAL,
            code = "AUTHORIZATION_NOT_GRANTED",
            message = "El usuario no autorizó el acceso; la tool que lo necesitaba no se ejecutó",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        ),
        timestamp = now()
    )

    IF delivery.outcome == APPROVED
        opened: StepRecord = recordToolCallBeforeExecution(step, call)

        result: ToolResult = executeToolCallIsolated(
            call, sandbox, isolatedCapabilities, execution, resumedState.agentId,
            TRUE, TRUE, toolExecutionSucceeded, toolExecutionOutput
        )

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

    RETURN resumeTurnWithObservation(
        resumedState, execution, append(candidatesSoFar, observation), session, activeSubscriptions,
        usage, finalModelContent
    )
END
```

```pseudocode
FUNCTION resumeDurableBudgetLimit(
    wait: ParkedWait,
    delivery: WaitDelivery,
    pausedState: AgentState,
    execution: ExecutionContext,
    extendedBudget: ExecutionBudget,
    usage: ExecutionUsage,
    session: Optional<SessionState>,
    activeSubscriptions: List<EventSubscription>
) -> AgentState

    accepted: ParkedWait = acceptDelivery(wait, delivery, execution, pausedState.agentId)

    resumedState: AgentState = AgentState(
        runId = pausedState.runId,
        sessionId = pausedState.sessionId,
        agentId = pausedState.agentId,
        status = RUNNING,
        currentTurn = pausedState.currentTurn
    )

    IF delivery.outcome == APPROVED
        extended: ExecutionContext = ExecutionContext(
            runId = execution.runId,
            sessionId = execution.sessionId,
            traceId = execution.traceId,
            budget = extendedBudget,
            caller = execution.caller
        )

        decision: ExecutionDecision = evaluateExecutionContinuation(
            resumedState, extended, extendedBudget, usage, FALSE
        )

        IF decision.outcome == CONTINUE
            RETURN resumedState
        END
    END

    RETURN terminateAgentRunOperationally(
        resumedState, execution, execution.budget, usage, FALSE, session, activeSubscriptions
    )
END
```

`newEventId`, `newMessageId`, `now` y `append` son utilidades primitivas. En
`resumeDurableBudgetLimit`, si la decisión es `CONTINUE`, el turno durable sigue con el
`ExecutionContext` cuyo `budget` es `extendedBudget`. Si el operador rechaza, `execution.budget`
sigue agotado y `terminateAgentRunOperationally` (CH-13) produce el `STOP`.

**Vencer usa estos mismos caminos.** Para una espera `EXPIRED`, la integración usa
`expiryObservation` en lugar de la observación de la entrega:
- aprobación, autorización y pregunta continúan con `resumeTurnWithObservation`, y el paso abierto
  se compromete sin tool call;
- un límite de presupuesto vencido va directo a `terminateAgentRunOperationally`.

Nótese lo que estas funciones **no** hacen:
- ninguna recibe, guarda ni devuelve un token;
- ninguna envía nada por un canal: `buildOutboundMessage` prepara el mensaje y el adaptador de
  salida lo envía;
- ninguna decide cuánto presupuesto se agrega: el operador lo propone y `ExecutionController`
  decide si alcanza.

## 12. Transiciones de Estado (State Transitions)

```text
ParkedWait
    PARKED → (entrega válida) RESUMED                      (CH-33)
    PARKED → (schedule, expiresAt vencido) EXPIRED          (CH-37, WAIT_EXPIRED)
    EXPIRED → EXPIRED                                       (idempotente)

Autorización
    tool ALLOW sin credencial del usuario → AuthorizationChallenge + ParkedWait(AUTHORIZATION)
    callback válido → WaitDelivery(APPROVED | REJECTED) → RESUMED
    paso: STARTED → +toolCall → +toolResult → COMMITTED   (APPROVED)
          STARTED → COMMITTED sin toolCall                (REJECTED o EXPIRED)

Límite de presupuesto
    APPROVED + CONTINUE → RUNNING
    APPROVED + STOP | REJECTED | EXPIRED → terminateAgentRunOperationally (FAILED o EXPIRED)

ContinuationClaim al terminar la sesión
    CLOSED | EXPIRED → RELEASED ; HANDED_OFF → sigue ACTIVE
```

## 13. Semántica de Fallos (Failure Semantics)

Códigos nuevos de `HarnessError`, con `ErrorCategory` ya existentes:

```text
HUMAN_INTERACTION  WAIT_NOT_DUE                       recoverable: FALSE, retryable: FALSE
HUMAN_INTERACTION  WAIT_NOT_EXPIRED                   recoverable: FALSE, retryable: FALSE
HUMAN_INTERACTION  WAIT_EXPIRED                       (observación, no fallo del run)
CREDENTIAL         AUTHORIZATION_CALLBACK_REJECTED    recoverable: FALSE, retryable: FALSE
CREDENTIAL         AUTHORIZATION_NOT_GRANTED          (observación, no fallo del run)
ADMISSION          NO_OUTBOUND_ADDRESS                recoverable: FALSE, retryable: FALSE
```

Un callback rechazado **no** cambia la espera: sigue `PARKED`, y el usuario correcto todavía puede
autorizar antes de que venza.

## 14. Eventos Producidos (Events Produced)

```text
WAIT_EXPIRED                   — una espera venció sin respuesta (payload: ParkedWait)
CALLER_AUTHORIZATION_RECEIVED  — un callback de autorización válido llegó (payload: WaitDelivery, sin token)
```

Se reutilizan `CONTINUATION_ADDRESS_RELEASED` (CH-34), `RUN_PARKED` / `RUN_RESUMED` (CH-33) y
`HUMAN_INTERACTION_RESOLVED` (CH-06).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **El token nunca pasa por el run.** El adaptador de callback lo entrega al Secret Store;
  `acceptAuthorizationCallback` solo recibe `tokenStored`, y la `WaitDelivery` que produce no tiene
  dónde llevarlo (INV-E08).
- **Solo el usuario autoriza su propia cuenta.** El callback debe venir firmado por el mismo
  `Principal` del desafío, y con el `callbackRef` que generó el arnés. Un callback reenviado, o
  firmado por otra persona de la misma empresa, se rechaza.
- **Vencer es no aprobar.** Una aprobación vencida nunca ejecuta la acción (INV-15).
- **El operador no fija el presupuesto:** propone un presupuesto extendido, y `ExecutionController`
  decide si el run puede seguir con él.
- **Nunca se responde a una dirección inferida.** Si la sesión no posee una dirección activa, no hay
  respuesta por el canal. Un mensaje que diga "contéstame por correo" no cambia la dirección.
- **Handoff no libera:** la dirección sigue siendo de la sesión mientras un humano la atiende, para
  que otra sesión no pueda reclamarla a mitad del traspaso.

## 16. Tests (Tests)

```text
TEST DueParkedWaitsSelectsOnlyParkedWaitsPastTheirDeadline
TEST ExpireParkedWaitIsIdempotent
TEST ExpireParkedWaitRejectsAWaitThatIsNotDue
TEST ExpiredApprovalNeverExecutesTheTool
TEST ExpiredBudgetLimitTerminatesTheRun
TEST ExpirySchedulerEntersAsAScheduleActivationRequest
TEST MissingCredentialIsDetectedOnlyForUserCallers
TEST AuthorizationCallbackFromAnotherPrincipalIsRejected
TEST AuthorizationCallbackWithWrongCallbackRefIsRejected
TEST AuthorizationCallbackNeverCarriesTheToken
TEST ApprovedAuthorizationRecordsTheToolCallBeforeExecuting
TEST RejectedAuthorizationCommitsTheStepWithoutExecuting
TEST AnsweredQuestionEntersAsAUserMessage
TEST ApprovedBudgetLimitContinuesOnlyIfExecutionControllerSaysContinue
TEST RejectedBudgetLimitTerminatesTheRun
TEST ClosingOrExpiringASessionReleasesItsAddresses
TEST HandoffKeepsTheAddressOwned
TEST OutboundMessageGoesOnlyToTheOwnedAddress
TEST WaitNoticeWithoutWaitIdIsRejected
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (v0.2.1 en curso, después de CH-37) — 26 componentes, 48 contratos, 38 capítulos

ResumptionCoordinator (CMP-024)  + dueParkedWaits, expireParkedWait, expiryObservation
CredentialBroker (CMP-014)       + detectMissingCallerCredential, acceptAuthorizationCallback
ContinuationRegistry (CMP-025)   + releaseAddressesForSession, outboundAddressFor, buildOutboundMessage
Integración                      + parkForMissingCredential, resumeDurableQuestion,
                                   resumeDurableAuthorization, resumeDurableBudgetLimit

Deuda: D-009..D-013 resueltas (registry/debt.yaml). Quedan 8 con destino CH-38.
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El protocolo OAuth** y el adaptador de callback: infraestructura de borde. El libro modela qué
  hace el arnés con su resultado.
- **Cuánto presupuesto propone el operador:** es un dato de la entrega; el presupuesto jerárquico
  llega en CH-43.
- **Avisar por un canal distinto del de la sesión** (por ejemplo, un correo a un aprobador que no
  está en el hilo): requiere una dirección propia del aprobador, y queda fuera de v0.2.1.
- **Las deudas de identidad, auditoría y retención** (D-001..D-008): son de CH-38.

## 19. Siguiente Incremento (Next Increment)

Ahora cada espera tiene salida, las autorizaciones empiezan y terminan sin tocar un token, y el arnés
sabe a dónde contestar. Lo que todavía no está cableado en el turno durable es la otra mitad de la
deuda:
- `PendingInput` y compactación durables;
- reglas de admisión y de política con el `Principal`;
- auditoría de capabilities `SAFE` y de continuaciones;
- retención del journal.

Será CH-38 ("Identidad, Auditoría y Retención en Todo el Turno"), el último capítulo de la versión
0.2.1. `next_chapter` queda en `null` porque CH-38 todavía no existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): las esperas no vencen, tres tipos no se reanudan, nadie abre ni cierra
   una autorización, las direcciones no se liberan y el arnés no contesta.
2. **Patrones** (= §3): CH-33 y CH-34 modelaron la entrada de cada mecanismo y dejaron la salida para
   una integración que no la escribió.
3. **Estructuras** (= §8): funciones nuevas en `ResumptionCoordinator`, `CredentialBroker` y
   `ContinuationRegistry`, y cuatro funciones de integración.
4. **Modelos mentales** (= §4): P-33, INV-E08 y P-34.

**Bucles de retroalimentación**

- **Refuerzo:** las esperas olvidadas bloquean runs y direcciones. El vencimiento activo corta la
  espiral.
- **Equilibrio:** `expiresAt`. Toda espera tiene un plazo.

**Punto de apalancamiento**

La decisión con mayor efecto es que `acceptAuthorizationCallback` produzca una `WaitDelivery` sin
credenciales mientras el token va directo a `CredentialBroker`, para que la autorización interactiva
cumpla INV-E08 de punta a punta.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Qué selecciona `dueParkedWaits`, qué exige `expireParkedWait` antes de marcar una espera
   `EXPIRED`, y por qué camino entra el schedule que las vence? *(pregunta guía 1)*
2. ¿Qué verifica `acceptAuthorizationCallback`, qué produce, y dónde queda el token de la
   autorización? *(pregunta guía 2)*
3. En `resumeDurableBudgetLimit`, ¿qué función decide si el run continúa con el presupuesto
   extendido, y qué pasa si el operador rechaza o si esa función no devuelve `CONTINUE`?
   *(pregunta guía 3)*
4. ¿Qué hace `releaseAddressesForSession` con cada `SessionEndReason`, y qué exige
   `buildOutboundMessage` para enviar una respuesta o un aviso de espera? *(pregunta guía 4)*

### Explicar

1. `ResumptionCoordinator` ya decidía qué espera reanuda una entrega. Explica por qué decidir que una
   espera venció también le pertenece, y qué parte del vencimiento le toca a la integración.
2. Explica por qué detectar que falta la credencial del usuario y recibir el token del callback le
   pertenecen a `CredentialBroker`, y qué se rompería si el token llegara al run dentro de la
   respuesta que reanuda la espera.

### Conectar

1. En CH-33, `parkRun` exigía `SAME_PRINCIPAL` para una espera `AUTHORIZATION` y
   `createAuthorizationChallenge` generaba un `callbackRef` opaco. ¿Qué dos verificaciones de
   `acceptAuthorizationCallback` dependen de esas decisiones de CH-33, y qué ataque evita cada una?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
