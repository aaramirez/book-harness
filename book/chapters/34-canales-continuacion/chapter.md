---
id: CH-34
title: "Canales y Direcciones de Continuación: HTTP, WebSocket, Webhooks y Schedules"
starting_version: "0.1"
ending_version: "0.2"
introduces_components: [CMP-025]
introduces_contracts: [C-046]
modifies_contracts: [C-022]
constitutional_articles: [P-16, P-17, P-34, INV-E01, INV-E02, INV-E15, INV-E19]
previous_chapter: CH-33
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH34
    text: |
      Al terminar este capítulo podrás decidir, para cualquier mensaje que llegue al agente por un
      canal — una API, un chat, un WebSocket, un webhook o un schedule —, si continúa una
      conversación que ya existe o empieza una nueva, sin adivinarlo, y explicar por qué una
      conversación externa solo puede pertenecer a una sesión a la vez.
  skeleton:
    id: SK-CH34
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
    components_to_be_introduced: [CMP-025]
    contracts_to_be_introduced: [C-046]
  guiding_questions:
    - id: GQ-CH34-01
      text: |
        Si alguien escribe por segunda vez en el mismo hilo de chat donde ya habló con el agente,
        ¿debería el agente empezar una conversación nueva o continuar la anterior? ¿Cómo lo sabe?
      answered_by: RQ-CH34-01
    - id: GQ-CH34-02
      text: |
        ¿Qué problema aparecería si dos sesiones distintas del agente creyeran ser dueñas del mismo
        hilo de chat?
      answered_by: RQ-CH34-02
    - id: GQ-CH34-03
      text: |
        Un schedule que corre todos los lunes y un webhook que llega de otro sistema no son personas
        escribiendo. ¿Deberían entrar al agente por un camino distinto al de un mensaje de chat?
      answered_by: RQ-CH34-03
    - id: GQ-CH34-04
      text: |
        Que un mensaje continúe una sesión existente, ¿significa que quien lo envía puede operar esa
        sesión?
      answered_by: RQ-CH34-04
  systems_lens:
    iceberg_visible_fact: |
      Cada mensaje que llega por un canal se convierte en un ActivationRequest y activa un run
      nuevo; un segundo mensaje en el mismo hilo no continúa nada, y si se intentara continuar, el
      arnés tendría que adivinar qué sesión corresponde (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que P-16 normaliza el estímulo pero nadie guarda la relación entre
      una conversación externa y una sesión durable; cada canal la resolvería a su manera, con
      heurísticas ("la última sesión de este usuario") que fallan justo cuando hay varias (ver
      sección 3).
    iceberg_structures: |
      Este capítulo introduce ContinuationRegistry (CMP-025) y ContinuationAddress (C-046), y lleva
      ActivationRequest (C-022) a v2 con sourceKind y continuationAddress: una dirección explícita
      con una sola sesión dueña, y una decisión CONTINUE_SESSION / ACTIVATE_NEW /
      ACTIVATE_UNADDRESSED para cada estímulo admitido (ver sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-34 (las conversaciones externas se direccionan, no se infieren),
      INV-E19 (una dirección tiene a lo sumo una sesión dueña) y P-16 (todo canal es un mecanismo de
      ingreso que produce un ActivationRequest) (ver sección 4).
    reinforcing_loop: |
      Sin dirección explícita, cada canal inventa su heurística de continuación; cada heurística
      falla en casos distintos y se parcha con otra regla ad hoc, así que el comportamiento de
      continuación diverge entre canales. Una dirección con dueña única corta la espiral: una sola
      regla para todos.
    balancing_loop: |
      INV-E19 es el mecanismo de equilibrio: por muchos mensajes que lleguen a la vez por el mismo
      hilo, solo una sesión puede ser su dueña, y un segundo reclamo se rechaza.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que el Ingress Adapter declare la
      ContinuationAddress (C-046) en el ActivationRequest, para que routeAdmittedRequest nunca tenga
      que inferir a qué sesión va un estímulo.
  recall_questions:
    - id: RQ-CH34-01
      text: |
        ¿Qué decide routeAdmittedRequest para un ActivationRequest sin dirección, con dirección sin
        dueña y con dirección con dueña, y qué exige antes de decidir?
    - id: RQ-CH34-02
      text: |
        ¿Qué hace claimContinuationAddress si la dirección ya tiene como dueña a la misma sesión, y
        qué si tiene como dueña a otra?
    - id: RQ-CH34-03
      text: |
        ¿Cuáles son los seis valores de SourceKind, qué verifica un Ingress Adapter de webhook antes de
        producir el ActivationRequest, y cómo entra un schedule?
    - id: RQ-CH34-04
      text: |
        Cuando routeAdmittedRequest decide CONTINUE_SESSION, ¿qué función de CH-31 decide todavía si el
        llamante puede operar esa sesión, y a qué componente de CH-33 va la entrega si la sesión está
        estacionada?
  explain_prompts:
    - id: EP-CH34-01
      text: |
        AdmissionController y ContinuationRegistry actúan sobre el mismo ActivationRequest, uno
        después del otro. Explica, como si hablaras con alguien sin contexto técnico, qué pregunta
        responde cada uno, y por qué no pueden ser la misma decisión.
      target_entity: CMP-025
    - id: EP-CH34-02
      text: |
        Explica por qué una ContinuationAddress necesita channelRef y conversationRef, y qué se
        rompería si solo se guardara el identificador de la conversación.
      target_entity: C-046
  interleaved_questions:
    - id: IQ-CH34-01
      text: |
        En CH-14, AdmissionController rechazaba por defecto y no emitía eventos porque todavía no
        existía un run. ¿Por qué routeAdmittedRequest tampoco emite eventos, y por qué
        claimContinuationAddress sí puede hacerlo?
      current_chapter_entities: [C-046, CMP-025]
      prior_chapter_entities: [C-022, C-023, CMP-012]
      prior_chapter: CH-14
  flashcards:
    - id: FC-CH34-01
      front: |
        ¿Qué es una ContinuationAddress (C-046)?
      back: |
        La dirección explícita de una conversación externa: channelRef (qué canal) y conversationRef
        (qué hilo, issue, socket o schedule dentro de ese canal). Mapea a una sesión durable con dueña
        única (INV-E19).
      source_entity: C-046
      chapter_introduced_in: CH-34
      review_stage: DAY_1
    - id: FC-CH34-02
      front: |
        ¿Qué tres decisiones produce routeAdmittedRequest?
      back: |
        CONTINUE_SESSION (la dirección tiene sesión dueña), ACTIVATE_NEW (dirección sin dueña: se crea
        una sesión y se reclama) y ACTIVATE_UNADDRESSED (sin dirección: sesión nueva, sin reclamo).
        Solo sobre un request con ADMIT.
      source_entity: CMP-025
      chapter_introduced_in: CH-34
      review_stage: DAY_1
    - id: FC-CH34-03
      front: |
        ¿Qué posee ContinuationRegistry (CMP-025) y qué no?
      back: |
        Posee la propiedad exclusiva de cada dirección y la decisión continuar / activar. No posee
        admitir (AdmissionController), decidir si el llamante opera la sesión (CH-31), reanudar
        esperas (ResumptionCoordinator), elegir el agente (Routing) ni transportar el estímulo
        (Ingress Adapter).
      source_entity: CMP-025
      chapter_introduced_in: CH-34
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH34-01
      recall_question: RQ-CH34-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH34-02
      recall_question: RQ-CH34-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH34-03
      recall_question: RQ-CH34-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH34-04
      recall_question: RQ-CH34-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 34 — Canales y Direcciones de Continuación: HTTP, WebSocket, Webhooks y Schedules

> **Regla constitucional (P-34):** las conversaciones externas se direccionan, no se infieren.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir, para cualquier mensaje que llegue
al agente por un canal (una API, un chat, un WebSocket, un webhook o un schedule), si continúa una
conversación que ya existe o empieza una nueva, sin adivinarlo. También podrás explicar por qué una
conversación externa solo puede pertenecer a una sesión a la vez.

**Esqueleto.** Séptimo capítulo del Tramo 4. Introduce el componente `ContinuationRegistry` y un
contrato, lleva `ActivationRequest` a v2 y describe cada canal como un Ingress Adapter.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si alguien escribe por segunda vez en el mismo hilo de chat donde ya habló con el agente,
   ¿debería el agente empezar una conversación nueva o continuar la anterior? ¿Cómo lo sabe?
2. ¿Qué problema aparecería si dos sesiones distintas del agente creyeran ser dueñas del mismo hilo
   de chat?
3. Un schedule que corre todos los lunes y un webhook que llega de otro sistema no son personas
   escribiendo. ¿Deberían entrar al agente por un camino distinto al de un mensaje de chat?
4. Que un mensaje continúe una sesión existente, ¿significa que quien lo envía puede operar esa
   sesión?

## 1. Arquitectura Actual (Current Architecture)

- **P-16** exige normalizar todo estímulo externo en un `ActivationRequest` (C-022) antes de entrar
  al núcleo. El **Ingress Adapter** que lo hace es infraestructura de borde, fuera del registro, y
  nunca llama a `AgentLoop` directamente (INV-E01).
- **`AdmissionController` (CMP-012, CH-14 y CH-31)** decide si el request entra (`AdmissionDecision`,
  C-023), con un `Principal` verificado y arranque cerrado (INV-E15).
- **El Routing** ("before routing", P-17) está declarado como Preview: ningún componente elige hacia
  dónde va una activación admitida.
- **`SessionManager` (CMP-010)** crea y guarda sesiones; **`ResumptionCoordinator` (CMP-024, CH-33)**
  reanuda esperas; **`PendingInput` (C-036, CH-28)** recibe mensajes para un run en curso.

## 2. El Problema (Problem)

Una persona escribe al agente en un hilo de chat. El agente responde. Diez minutos después, la misma
persona escribe otra vez **en el mismo hilo**. Hoy:
- ese segundo mensaje es otro `ActivationRequest`, idéntico en forma al primero;
- nada dice que pertenece a la conversación anterior, así que el agente empieza de cero y pierde
  todo el contexto;
- si se quisiera continuar, habría que **adivinar** la sesión ("la última de este usuario"), y la
  heurística falla justo cuando la persona tiene dos conversaciones abiertas.

Y hay canales donde ni siquiera escribe una persona:
- un **webhook** de otro sistema (un issue nuevo, un pago recibido);
- un **schedule** que corre todos los lunes;
- una **conexión WebSocket** que se mantiene abierta y manda mensajes durante horas.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **`ActivationRequest` no dice a qué conversación pertenece.** `sourceRef` dice de dónde viene, no
  qué conversación continúa.
- **Nadie guarda la relación** "conversación externa → sesión". Sin ella, cada canal tendría que
  resolverla a su manera.
- **Nada impide que dos sesiones reclamen el mismo hilo.** Dos mensajes simultáneos podrían crear
  dos sesiones dueñas del mismo hilo, y el agente respondería dos veces con dos contextos distintos.
- **Ningún componente posee la decisión** "¿este estímulo continúa una sesión o activa una nueva?".
  No es de `AdmissionController` (si entra), ni de `SessionManager` (la historia), ni del Routing
  (qué agente). Por eso este capítulo introduce un componente (EVO-01).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-16   Activation is independent from execution.
           Cada canal sigue siendo un Ingress Adapter que produce un ActivationRequest.
    P-17   Admission precedes execution.
           routeAdmittedRequest solo actúa sobre un ADMIT del mismo request.

Principles introduced (Amendment v1.2, ya ratificado)
    P-34   External conversations are addressed, not inferred.
           ContinuationAddress + routeAdmittedRequest.

Invariants preserved
    INV-E01  No ingress adapter calls AgentLoop directly.
             Los canales de este capítulo solo producen ActivationRequest.
    INV-E02  Ninguna activación se ejecuta sin AdmissionDecision.
             REQUEST_NOT_ADMITTED si se intenta enrutar sin ADMIT.
    INV-E15  Un arnés sin configurar no admite nada.
             Por lo tanto, un canal sin regla de admisión no escucha.
    INV-E19  (Amendment v1.2) A continuation address has at most one owning session at a time.
             claimContinuationAddress rechaza un segundo dueño.

Component ownership changes
    Nuevo: ContinuationRegistry (CMP-025). Ningún componente existente pierde decisiones.

Contract changes
    Nuevo: C-046 ContinuationAddress.
    C-022 ActivationRequest v1 → v2 (+ sourceKind, + continuationAddress, ambos Optional).

Security implications
    Continuar una sesión no da permiso para operarla; un webhook sin firma válida nunca
    produce un ActivationRequest (ver sección 15).

Observability implications
    Nuevos AgentEventType: CONTINUATION_ADDRESS_CLAIMED, CONTINUATION_ADDRESS_RELEASED y
    CONTINUATION_CLAIM_REJECTED.

Deterministic vs agentic boundary
    Todo es determinístico. El modelo nunca decide a qué sesión va un mensaje.
```

## 5. Conceptos Nuevos (New Concepts)

- **Dirección de continuación** (*continuation address*): el par "canal + conversación" que
  identifica una conversación externa. Ejemplos:
  - canal `chat-equipo`, conversación "hilo 1718";
  - canal `issues`, conversación "issue 42";
  - canal `websocket`, conversación "sesión de cliente abc";
  - canal `schedule`, conversación "reporte-semanal".
- **Dueña única** (*exclusive ownership*): cada dirección tiene a lo sumo una sesión dueña a la vez.
  Otra sesión solo puede reclamarla después de que la dueña la libere.
- **Continuar o activar:** un estímulo admitido
  - **continúa** la sesión dueña de su dirección;
  - **activa** una sesión nueva si la dirección no tiene dueña (y la reclama);
  - **activa sin dirección** si el canal no declara ninguna (cada estímulo, una sesión).
- **Tipo de fuente** (*source kind*): de qué clase de canal vino el estímulo. No cambia la regla de
  continuación, pero sí la trazabilidad y lo que el Ingress Adapter debió verificar.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `ActivationRequest` (C-022, que pasa a v2), `AdmissionDecision` (C-023),
  `ExecutionContext` (C-004), `AgentEvent` (C-010), `HarnessError` (C-011);
- **primitivos:** `SessionId`, `AgentId`, `Timestamp`.

| Identificador | Rol en este capítulo |
|---|---|
| `ActivationRequestId` | identificador de un `ActivationRequest` (heredado de CH-14) |
| `AdmissionOutcome` | `ADMIT` / `REJECT` (heredado de CH-14) |
| `AgentEventType` | se agregan `CONTINUATION_ADDRESS_CLAIMED`, `CONTINUATION_ADDRESS_RELEASED` y `CONTINUATION_CLAIM_REJECTED` |
| `ErrorCategory` | reutiliza `ADMISSION`, sin valores nuevos |

### `SourceKind` — de qué clase de canal vino el estímulo (embebido)

```pseudocode
ENUM SourceKind
    API
    CHANNEL
    WEBSOCKET
    WEBHOOK
    SCHEDULE
    STREAM_EVENT
END
```

### `ContinuationAddress` — la dirección de una conversación externa (C-046)

```pseudocode
STRUCT ContinuationAddress
    channelRef: Text
    conversationRef: Text
END
```

`channelRef` hace falta porque el mismo `conversationRef` ("42") puede existir en dos canales
distintos (el issue 42 y el hilo 42) sin ser la misma conversación.

### `ActivationRequest` — versión 2 (C-022)

```pseudocode
STRUCT ActivationRequest
    id: ActivationRequestId
    sourceRef: Text
    sourceKind: Optional<SourceKind>
    externalIdentityRef: Text
    continuationAddress: Optional<ContinuationAddress>
    payload: Value
    receivedAt: Timestamp
END
```

**Compatibilidad hacia atrás:** con `continuationAddress = NULL`, un request activa una sesión nueva,
como todos los de CH-14..CH-33. `sourceKind = NULL` es un canal sin tipo declarado.

### `ClaimStatus` y `ContinuationClaim` — quién es dueña de una dirección (embebidos)

```pseudocode
ENUM ClaimStatus
    ACTIVE
    RELEASED
END
```

```pseudocode
STRUCT ContinuationClaim
    address: ContinuationAddress
    sessionId: SessionId
    status: ClaimStatus
    claimedAt: Timestamp
    releasedAt: Optional<Timestamp>
END
```

### `RouteAction` y `ContinuationRoute` — continuar o activar (embebidos)

```pseudocode
ENUM RouteAction
    CONTINUE_SESSION
    ACTIVATE_NEW
    ACTIVATE_UNADDRESSED
END
```

```pseudocode
STRUCT ContinuationRoute
    requestId: ActivationRequestId
    action: RouteAction
    sessionId: Optional<SessionId>
    decidedAt: Timestamp
END
```

`sessionId` solo tiene valor con `CONTINUE_SESSION`: en los otros dos casos la sesión todavía no
existe.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

```text
ID:                     C-046
Name:                   ContinuationAddress
Version:                v1
Introduced In:          CH-34
Used By:                [CMP-025]
Constitutional Impact:  [P-34, INV-E19]
```

```text
C-022 ActivationRequest  v1 → v2   Modified By: [CH-34]
                         + sourceKind: Optional<SourceKind>
                         + continuationAddress: Optional<ContinuationAddress>
Used By:                 [CMP-012, CMP-025]
```

`SourceKind`, `ClaimStatus`, `ContinuationClaim`, `RouteAction` y `ContinuationRoute` quedan
embebidos.

## 8. Responsabilidades de Componentes (Component Responsibilities)

```pseudocode
COMPONENT ContinuationRegistry
    consumes: ExecutionContext, ActivationRequest, AdmissionDecision
    produces: ContinuationAddress, AgentEvent, HarnessError
END
```

```text
COMPONENT: ContinuationRegistry (CMP-025)

Responsibility:
    Mantener qué sesión es dueña de cada dirección de continuación y decidir, para un
    ActivationRequest ya admitido, si continúa la sesión dueña de su dirección o activa una nueva,
    sin inferir nunca qué run continúa un estímulo.

Owns (Amendment v1.2, citas literales):
    - "Every external conversation … MUST map to a durable session through an explicit
      continuation address with exclusive ownership. The runtime MUST NOT guess which run a
      stimulus continues" (P-34)
    - "A continuation address has at most one owning session at a time" (INV-E19): reclamar,
      liberar y rechazar un segundo dueño
    - decidir CONTINUE_SESSION / ACTIVATE_NEW / ACTIVATE_UNADDRESSED

Does NOT own:
    - admitir o rechazar la activación (AdmissionController, CMP-012, CH-14). Es la frontera más
      importante del capítulo: AdmissionController decide SI un estímulo entra; ContinuationRegistry
      decide A QUÉ SESIÓN va un estímulo que ya entró.
    - decidir si el llamante puede continuar esa sesión (continuationAllowedForCaller, CH-31)
    - reanudar una espera estacionada (ResumptionCoordinator, CMP-024, CH-33)
    - elegir qué agente atiende una activación nueva (Routing, Preview)
    - crear la sesión ni guardar su historia (SessionManager, CMP-010)
    - normalizar el estímulo, verificar firmas, mantener sockets o disparar schedules
      (Ingress Adapter, INV-E01)
```

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
ContinuationRegistry
    consumes → ExecutionContext, ActivationRequest, AdmissionDecision
    produces → ContinuationAddress, AgentEvent, HarnessError
    depends on (componentes) → (ninguno)
```

La integración (CH-36) encadena, para cada estímulo:
1. el Ingress Adapter produce el `ActivationRequest` v2, con `sourceKind` y, si el canal la tiene,
   `continuationAddress`;
2. `admitWithVerifiedIdentity` (CH-31) → `ADMIT` con `principal`;
3. `routeAdmittedRequest` → `ContinuationRoute`;
4. según la acción:
   - `CONTINUE_SESSION`: `continuationAllowedForCaller` (CH-31) decide si el llamante puede operarla.
     Si la sesión tiene un run en curso, el mensaje entra como `PendingInput` (CH-28). Si está
     estacionada y el mensaje nombra una espera, va a `ResumptionCoordinator` (CH-33). Si no, abre un
     run nuevo en la sesión;
   - `ACTIVATE_NEW`: el Routing elige el agente, `SessionManager` crea la sesión y
     `claimContinuationAddress` la hace dueña de la dirección;
   - `ACTIVATE_UNADDRESSED`: igual, sin reclamo.

### Los canales, uno por uno (Ingress Adapters, fuera del registro)

Ninguno de estos canales es un componente. Todos terminan en lo mismo: un `ActivationRequest` v2.

| Canal | `sourceKind` | `continuationAddress` | Lo que el adaptador debe hacer antes |
|---|---|---|---|
| **API HTTP de sesiones** | `API` | la sesión que el cliente nombra, o ninguna para empezar | verificar el token del cliente (adaptador de identidad, CH-31) |
| **Chat** (un hilo de un canal de equipo) | `CHANNEL` | canal + hilo | verificar que el evento viene del proveedor del chat |
| **WebSocket de entrada** | `WEBSOCKET` | `websocket` + la clave de sesión del cliente | autenticar al abrir la conexión; **cada mensaje es un turno**, nunca una conexión es un run |
| **Webhook** | `WEBHOOK` | sistema + objeto (p.ej. `issues` + "42") | verificar la **firma** del cuerpo con comparación en **tiempo constante**, y rechazar entregas repetidas o fuera de ventana |
| **Schedule** (cron) | `SCHEDULE` | `schedule` + nombre, si debe continuar una sesión; ninguna si cada ejecución es nueva | disparar con la identidad `SERVICE` configurada para ese schedule |
| **Evento de stream** | `STREAM_EVENT` | la que declare la fuente (CH-40) | igual que un webhook: verificar el origen |

Tres reglas valen para todos los canales:
- **un canal sin regla de admisión no escucha.** No hace falta una función nueva: con INV-E15
  (CH-31) un arnés sin reglas rechaza todo, llegue por donde llegue;
- **la conexión no es el run.** Un WebSocket abierto durante horas no mantiene un run vivo: cada
  mensaje produce un `ActivationRequest` y, con la misma dirección, continúa la misma sesión;
- **la verificación del canal es previa.** Un webhook con firma inválida nunca llega a ser un
  `ActivationRequest`; eso no es una decisión de admisión, sino del adaptador.

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
Canal → [Ingress Adapter] → AdmissionController → ContinuationRegistry → sesión existente | sesión nueva
```

**Vista 2 — Sequence: primer mensaje de un hilo**

```text
Chat (hilo 1718)
   ▼ Ingress Adapter: ActivationRequest(sourceKind = CHANNEL, address = chat-equipo/1718)
AdmissionController: admitWithVerifiedIdentity → ADMIT
ContinuationRegistry: routeAdmittedRequest → ACTIVATE_NEW (la dirección no tiene dueña)
   │ (Routing elige el agente; SessionManager crea la sesión S1)
ContinuationRegistry: claimContinuationAddress(address, S1) → ACTIVE + CONTINUATION_ADDRESS_CLAIMED
```

**Vista 2b — Sequence: segundo mensaje del mismo hilo**

```text
Chat (hilo 1718) → ActivationRequest(address = chat-equipo/1718) → ADMIT
ContinuationRegistry: routeAdmittedRequest → CONTINUE_SESSION(S1)
   │ continuationAllowedForCaller (CH-31) → PendingInput (CH-28) | ResumptionCoordinator (CH-33) | run nuevo en S1
```

**Vista 2c — Sequence: dos sesiones reclaman el mismo hilo**

```text
S2: claimContinuationAddress(chat-equipo/1718, S2)
   → CONTINUATION_CLAIM_REJECTED + CONTINUATION_ADDRESS_ALREADY_OWNED (S1 sigue siendo la dueña)
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

```pseudocode
FUNCTION sameAddress(
    a: ContinuationAddress,
    b: ContinuationAddress
) -> Boolean

    RETURN a.channelRef == b.channelRef AND a.conversationRef == b.conversationRef
END
```

```pseudocode
FUNCTION findActiveClaim(
    claims: List<ContinuationClaim>,
    address: ContinuationAddress
) -> Optional<ContinuationClaim>

    FOR EACH claim IN claims
        IF claim.status == ACTIVE AND sameAddress(claim.address, address)
            RETURN claim
        END
    END

    RETURN NULL
END
```

```pseudocode
FUNCTION routeAdmittedRequest(
    request: ActivationRequest,
    decision: AdmissionDecision,
    claims: List<ContinuationClaim>
) -> ContinuationRoute

    IF decision.outcome != ADMIT OR decision.requestId != request.id
        THROW HarnessError(
            category = ADMISSION,
            code = "REQUEST_NOT_ADMITTED",
            message = "Solo se decide la continuación de un ActivationRequest con una AdmissionDecision ADMIT propia",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    IF request.continuationAddress == NULL
        RETURN ContinuationRoute(
            requestId = request.id,
            action = ACTIVATE_UNADDRESSED,
            sessionId = NULL,
            decidedAt = now()
        )
    END

    owner: Optional<ContinuationClaim> = findActiveClaim(claims, request.continuationAddress)

    IF owner == NULL
        RETURN ContinuationRoute(
            requestId = request.id,
            action = ACTIVATE_NEW,
            sessionId = NULL,
            decidedAt = now()
        )
    END

    RETURN ContinuationRoute(
        requestId = request.id,
        action = CONTINUE_SESSION,
        sessionId = owner.sessionId,
        decidedAt = now()
    )
END
```

```pseudocode
FUNCTION claimContinuationAddress(
    claims: List<ContinuationClaim>,
    address: ContinuationAddress,
    sessionId: SessionId,
    execution: ExecutionContext,
    agentId: AgentId
) -> ContinuationClaim

    owner: Optional<ContinuationClaim> = findActiveClaim(claims, address)

    IF owner != NULL AND owner.sessionId == sessionId
        RETURN owner
    END

    IF owner != NULL
        failure: HarnessError = HarnessError(
            category = ADMISSION,
            code = "CONTINUATION_ADDRESS_ALREADY_OWNED",
            message = "La dirección de continuación ya tiene otra sesión dueña; solo puede reclamarse cuando esa sesión la libere",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = CONTINUATION_CLAIM_REJECTED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = failure
        )
        THROW failure
    END

    claim: ContinuationClaim = ContinuationClaim(
        address = address,
        sessionId = sessionId,
        status = ACTIVE,
        claimedAt = now(),
        releasedAt = NULL
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = CONTINUATION_ADDRESS_CLAIMED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = claim
    )

    RETURN claim
END
```

```pseudocode
FUNCTION releaseContinuationAddress(
    claim: ContinuationClaim,
    sessionId: SessionId,
    execution: ExecutionContext,
    agentId: AgentId
) -> ContinuationClaim

    IF claim.status != ACTIVE OR claim.sessionId != sessionId
        THROW HarnessError(
            category = ADMISSION,
            code = "NOT_THE_ADDRESS_OWNER",
            message = "Solo la sesión dueña puede liberar una dirección de continuación activa",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    released: ContinuationClaim = ContinuationClaim(
        address = claim.address,
        sessionId = claim.sessionId,
        status = RELEASED,
        claimedAt = claim.claimedAt,
        releasedAt = now()
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = CONTINUATION_ADDRESS_RELEASED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = released
    )

    RETURN released
END
```

`newEventId` y `now` son utilidades primitivas. `claims` es la lista durable de reclamos; el
almacenamiento que garantiza que dos reclamos simultáneos no ganen ambos es infraestructura de borde,
igual que en `IdempotencyGuard` (CH-17).

Nótese lo que estas funciones **no** hacen:
- `routeAdmittedRequest` no emite eventos: todavía no hay run al cual atribuirlos (el mismo criterio
  de CH-14);
- ninguna decide si el llamante puede operar la sesión ni qué agente atiende una activación nueva;
- ninguna mira el `payload`: la continuación depende de la dirección declarada, nunca del texto.

## 12. Transiciones de Estado (State Transitions)

El ciclo de vida de un `ContinuationClaim`:

```text
claimContinuationAddress (dirección libre)     → ACTIVE    (CONTINUATION_ADDRESS_CLAIMED)
claimContinuationAddress (misma sesión dueña)  → ACTIVE    (sin cambios, idempotente)
claimContinuationAddress (otra sesión dueña)   → rechazo   (CONTINUATION_CLAIM_REJECTED)
releaseContinuationAddress (la dueña)          → RELEASED  (CONTINUATION_ADDRESS_RELEASED)
```

Y la tabla de `routeAdmittedRequest`:

```text
sin ADMIT propio                  → REQUEST_NOT_ADMITTED
sin continuationAddress           → ACTIVATE_UNADDRESSED
dirección sin reclamo ACTIVE      → ACTIVATE_NEW
dirección con reclamo ACTIVE      → CONTINUE_SESSION (sessionId de la dueña)
```

## 13. Semántica de Fallos (Failure Semantics)

Cada fallo nuevo es un `HarnessError` de categoría `ADMISSION`:

```text
ADMISSION  REQUEST_NOT_ADMITTED                recoverable: FALSE, retryable: FALSE
ADMISSION  CONTINUATION_ADDRESS_ALREADY_OWNED  recoverable: FALSE, retryable: FALSE
ADMISSION  NOT_THE_ADDRESS_OWNER               recoverable: FALSE, retryable: FALSE
```

Cuando dos mensajes del mismo hilo llegan a la vez y ambos deciden `ACTIVATE_NEW`, solo uno gana el
reclamo. El perdedor recibe `CONTINUATION_ADDRESS_ALREADY_OWNED` y la integración lo vuelve a
enrutar: ahora sale `CONTINUE_SESSION`. Nunca quedan dos sesiones dueñas.

## 14. Eventos Producidos (Events Produced)

```text
CONTINUATION_ADDRESS_CLAIMED   — una sesión pasó a ser dueña de una dirección (payload: ContinuationClaim)
CONTINUATION_ADDRESS_RELEASED  — la dueña liberó la dirección (payload: ContinuationClaim)
CONTINUATION_CLAIM_REJECTED    — otra sesión intentó reclamar una dirección con dueña (payload: HarnessError)
```

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **Conocer la dirección no da acceso.** Que alguien escriba en el hilo 1718 hace que el mensaje vaya
  a la sesión S1, pero `continuationAllowedForCaller` (CH-31) sigue decidiendo si esa persona puede
  operarla. Enrutar no es autorizar.
- **Un webhook sin firma válida no existe.** El adaptador compara la firma en tiempo constante (para
  no filtrar por tiempos cuánto de la firma coincidió) y descarta entregas repetidas antes de
  producir el `ActivationRequest`.
- **Un schedule no es anónimo.** Entra con una identidad `SERVICE` configurada, y pasa por la misma
  admisión que un usuario.
- **Un canal sin reglas no abre la puerta.** INV-E15 aplica a todos los canales por igual.
- **La continuación nunca se decide por el contenido.** Un mensaje que diga "continúa mi otra
  conversación" no cambia la dirección: el modelo no puede redirigir un estímulo.

## 16. Tests (Tests)

```text
TEST RouteRequiresTheRequestsOwnAdmit
TEST RequestWithoutAddressActivatesUnaddressed
TEST AddressWithoutOwnerActivatesNew
TEST AddressWithOwnerContinuesThatSession
TEST SameConversationRefInTwoChannelsAreDifferentAddresses
TEST ClaimIsIdempotentForTheOwningSession
TEST SecondSessionCannotClaimAnOwnedAddress
TEST ConcurrentClaimsLeaveExactlyOneOwner
TEST OnlyTheOwnerCanRelease
TEST ReleasedAddressCanBeClaimedAgain
TEST RoutingNeverReadsThePayload
TEST ContinuingASessionStillRequiresContinuationAllowedForCaller
TEST WebSocketMessageIsATurnNotARun
TEST WebhookWithInvalidSignatureNeverBecomesAnActivationRequest
TEST RequestWithoutSourceKindBehavesAsV1
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.2 en curso, después de CH-34)

Components — 25
 └── CMP-025 ContinuationRegistry    (CH-34, nuevo — plano Ingress & Activation)

Contracts — 46
 ├── C-022 ActivationRequest v2      (CH-14 → modificado en CH-34: sourceKind, continuationAddress)
 └── C-046 ContinuationAddress       (CH-34, nuevo)

Ingreso, en orden
 Ingress Adapter → AdmissionController → ContinuationRegistry → (Routing, Preview) → sesión
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **Cuándo se libera una dirección.** Al cerrar la sesión, al vencer, o durante un handoff a un
  humano (CH-23), donde eve deja un marcador. La integración (CH-36) fija la regla.
- **Responder por el canal.** La dirección dice a dónde volver a escribir, pero la salida hacia un
  canal es un adaptador de salida que se modela en la integración.
- **El Routing:** qué agente atiende una activación nueva sigue siendo Preview.
- **El vencimiento de esperas** (deuda de CH-33) puede dispararse con un schedule interno; se cablea
  en CH-36.
- **Eventos de stream como fuente de datos:** su lado de lectura es de CH-40.

## 19. Siguiente Incremento (Next Increment)

Ahora cada estímulo llega a la sesión correcta. Pero cuando el agente ejecuta código o comandos, lo
hace en el mismo lugar donde viven las credenciales: una tool de shell podría leerlas, y un modelo
manipulado podría pedirle que las imprima.

El siguiente capítulo introduce el **entorno aislado** (P-35):
- una sesión de sandbox con política de red explícita;
- credenciales que solo existen en el egress, nunca dentro del entorno (INV-E20).

Será CH-35 ("El Entorno Aislado y las Credenciales que Solo Existen en el Egress"), con el componente
`IsolatedExecutionEnvironment`. `next_chapter` queda en `null` porque CH-35 todavía no existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): cada mensaje de un canal activa un run nuevo; continuar exigiría
   adivinar la sesión.
2. **Patrones** (= §3): nadie guarda la relación conversación → sesión; cada canal inventaría su
   heurística.
3. **Estructuras** (= §8): `ContinuationRegistry` (CMP-025), `ContinuationAddress` (C-046) y
   `ActivationRequest` v2.
4. **Modelos mentales** (= §4): P-34, INV-E19 y P-16.

**Bucles de retroalimentación**

- **Refuerzo:** heurísticas por canal que se parchan con más heurísticas. Una dirección explícita
  corta la espiral.
- **Equilibrio:** INV-E19. Un segundo reclamo se rechaza.

**Punto de apalancamiento**

La decisión con mayor efecto es que el Ingress Adapter declare la `ContinuationAddress` (C-046) en el
`ActivationRequest`, para que `routeAdmittedRequest` nunca tenga que inferir.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Qué decide `routeAdmittedRequest` para un `ActivationRequest` sin dirección, con dirección sin
   dueña y con dirección con dueña, y qué exige antes de decidir? *(pregunta guía 1)*
2. ¿Qué hace `claimContinuationAddress` si la dirección ya tiene como dueña a la misma sesión, y qué
   si tiene como dueña a otra? *(pregunta guía 2)*
3. ¿Cuáles son los seis valores de `SourceKind`, qué verifica un Ingress Adapter de webhook antes de
   producir el `ActivationRequest`, y cómo entra un schedule? *(pregunta guía 3)*
4. Cuando `routeAdmittedRequest` decide `CONTINUE_SESSION`, ¿qué función de CH-31 decide todavía si
   el llamante puede operar esa sesión, y a qué componente de CH-33 va la entrega si la sesión está
   estacionada? *(pregunta guía 4)*

### Explicar

1. `AdmissionController` y `ContinuationRegistry` actúan sobre el mismo `ActivationRequest`, uno
   después del otro. Explica qué pregunta responde cada uno, y por qué no pueden ser la misma
   decisión.
2. Explica por qué una `ContinuationAddress` necesita `channelRef` y `conversationRef`, y qué se
   rompería si solo se guardara el identificador de la conversación.

### Conectar

1. En CH-14, `AdmissionController` rechazaba por defecto y no emitía eventos porque todavía no
   existía un run. ¿Por qué `routeAdmittedRequest` tampoco emite eventos, y por qué
   `claimContinuationAddress` sí puede hacerlo?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
