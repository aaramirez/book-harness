---
id: CH-15
title: "AgentCommunicationGateway y la Frontera Explícita entre Agentes"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-013]
introduces_contracts: [C-024, C-025]
modifies_contracts: []
constitutional_articles: [P-18, P-19, P-20, P-21, P-25, INV-E03, INV-E04, INV-E05, INV-E06, INV-18, INV-19, INV-20]
previous_chapter: CH-14
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH15
    text: |
      Al terminar este capítulo podrás distinguir, para cualquier mensaje que cruce la frontera
      entre dos agentes (dos runs ya en ejecución, o un run ya activo que delega parte de su
      trabajo hacia un sub-agente), qué validación le pertenece en exclusiva al componente que
      desacopla esa comunicación de cualquier SDK, protocolo o transporte concreto — sin decidir si
      el estímulo que inició cualquiera de los dos runs tenía derecho a arrancar, sin autorizar una
      acción ya resuelta, sin decidir continuación de turno — y podrás diagnosticar, para cualquier
      token de delegación emitido, si la autoridad que representa está de verdad acotada en scope,
      en tiempo y en presupuesto (Amendment v1.1, P-21), o si equivale, en la práctica, a heredar
      sin límite la autoridad de quien delega.
  skeleton:
    id: SK-CH15
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
    components_to_be_introduced: [CMP-013]
    contracts_to_be_introduced: [C-024, C-025]
  guiding_questions:
    - id: GQ-CH15-01
      text: |
        Cuando un agente que ya está corriendo necesita que otro agente — uno interno, gestionado
        por el mismo runtime, o uno externo, operado por un tercero completamente distinto — haga
        algo en su nombre, ¿qué necesitaría existir para que esa comunicación nunca dependa de que
        el runtime conozca, de antemano, el SDK o el protocolo de mensajería concreto que ese otro
        agente usa?
      answered_by: RQ-CH15-01
    - id: GQ-CH15-02
      text: |
        La decisión de si un estímulo externo crudo tiene siquiera derecho a arrancar un run ya
        tiene, en este libro, un dueño que actúa antes de que exista cualquier ejecución. ¿Esa
        misma pregunta sirve también para decidir si un run que YA está en marcha puede
        comunicarse con otro run ya en marcha, o es, honestamente, una pregunta distinta que
        necesita su propio dueño?
      answered_by: RQ-CH15-02
    - id: GQ-CH15-03
      text: |
        Cuando un run le pide a otro — o a un agente completamente externo, operado fuera de este
        sistema — que actúe en su nombre, ¿basta con que el que delega simplemente confíe en que
        el otro nunca hará más de lo que se le pidió, o necesita existir algo escrito, con
        vencimiento explícito, que declare exactamente cuánta autoridad se transfiere?
      answered_by: RQ-CH15-03
    - id: GQ-CH15-04
      text: |
        Un presupuesto operacional ya existe en este libro para acotar cuántos turnos, tool calls,
        tokens y costo puede consumir una única ejecución. Cuando esa ejecución delega parte de su
        trabajo hacia otra, ¿ese mismo presupuesto se hereda automáticamente y sin límites nuevos,
        o necesita una forma más acotada, propia de la relación de delegación, que nunca reemplace
        al presupuesto original?
      answered_by: RQ-CH15-04
  systems_lens:
    iceberg_visible_fact: |
      Catorce capítulos reales construyeron un runtime completo más su primer componente de
      Enterprise (`AdmissionController`, CH-14) — pero ninguno modeló, todavía, qué pasa cuando un
      agente que YA está en ejecución necesita comunicarse con otro agente: ni con un sub-agente
      interno al que delega parte de su trabajo, ni con un agente externo, operado por un tercero,
      con el que necesita federarse. La única forma de "otro agente" que este libro nombró hasta
      ahora es "other agents" dentro de la propia lista de `P-16` ("ingress mechanisms") — un
      estímulo de ENTRADA, nunca una comunicación entre dos ejecuciones ya vivas (ver seccion 2, El
      Problema).
    iceberg_patterns: |
      El mismo patrón que motivó CH-14 se repite aquí, un plano después: Amendment v1.1 nombra
      literalmente `AgentCommunicationGateway` desde que fue adoptada (`P-19`), y
      `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §31 ("Regla de comunicación entre agentes")
      ya exige, palabra por palabra, "Nunca acoplar un agente a la implementación de otro. Usar
      `AgentCommunicationGateway`. Diferenciar: internal delegation, external federation, protocol
      y transport" — una deuda nombrada, no resuelta todavía por ningún capítulo (ver seccion 3,
      Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala el segundo componente de Amendment v1.1 — y, deliberadamente, el
      segundo plano que este libro cubre de los nueve que la enmienda enumera: no el "Execution
      Plane" (el segundo en el orden canónico), sino el "Agent Interoperability Plane" (el
      tercero) — con una ficha que declara tanto lo que posee (`owns`: adaptar mensajes semánticos
      hacia/desde protocolos externos vía adapters, desacoplar el core de cualquier SDK/protocolo/
      transporte concreto, y verificar — nunca redefinir — el límite de `ExecutionBudget` ya
      existente sobre una comunicación delegada) como lo que explícitamente NO posee (decidir si un
      estímulo crudo puede arrancar un run, autorizar una acción ya resuelta, decidir continuación
      de turno, o el protocolo/transporte concreto en sí) (ver seccion 8, Component
      Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es que "comunicación entre agentes" no es una
      pregunta única: Amendment v1.1 la divide, con nombres propios, en delegación interna (un
      protocolo interno, hacia un sub-agente gestionado por el mismo runtime) y federación externa
      (un boundary basado en estándares, como A2A, hacia un agente operado independientemente) —
      dos preguntas con la misma forma superficial ("¿puedo comunicarme con ese otro agente?") pero
      con dueños, riesgos y mecanismos de confianza completamente distintos (`P-20`) (ver seccion 4,
      Impacto Constitucional).
    reinforcing_loop: |
      Cada vez que un sistema deja sin modelar la frontera de comunicación entre agentes, cualquier
      componente puede invocar directamente el SDK o el endpoint HTTP de otro agente "porque total,
      ya sabemos su dirección" — acoplando el core a un protocolo concreto exactamente como
      `AgentLoop` (CH-01, CH-03) ya se negó a acoplarse a un provider de modelo concreto; el mismo
      bucle de "la ausencia de un dueño se vuelve una dependencia implícita" que `P-02` (model
      replaceability) y `P-19` combaten, ahora aplicado a otro agente en vez de a un modelo.
    balancing_loop: |
      `authorizeAgentCommunicationMessage` (seccion 11) es el mecanismo de equilibrio: dejar pasar
      sin fricción cualquier mensaje que no declara ningún `DelegationGrant` (comunicación sin
      autoridad delegada de por medio), pero rechazar — nunca heredar en silencio — cualquier
      mensaje que sí lo declara en cuanto ese grant ya expiró o pide algo fuera de su
      `delegatedScope` explícito.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `DelegationGrant.delegatedScope` sea
      siempre una lista explícita y acotada (`List<Text>`), nunca un booleano de "toda la
      autoridad" — y que `AgentCommunicationMessage.delegationGrantId` sea `Optional`, nunca
      obligatorio. Si `DelegationGrant` representara "delega todo" en vez de un scope explícito, o
      si todo mensaje exigiera un grant (incluso la federación externa sin relación de delegación),
      `AgentCommunicationGateway` absorbería silenciosamente una autorización sin límites — la
      violación exacta que `P-21` ("delegated authority is explicit and least-privileged") prohíbe.
  recall_questions:
    - id: RQ-CH15-01
      text: |
        ¿Qué componente nuevo desacopla la comunicación semántica entre agentes de cualquier
        protocolo o transporte concreto (`P-18`/`P-19`), y qué dos conceptos, distinguidos
        literalmente por `P-20`, mantiene siempre separados?
    - id: RQ-CH15-02
      text: |
        ¿Qué campos tiene `AgentCommunicationMessage` (C-024), y por qué su campo
        `delegationGrantId` es `Optional` en vez de obligatorio?
    - id: RQ-CH15-03
      text: |
        ¿Qué campos tiene `DelegationGrant` (C-025), y qué tres propiedades exige `P-21` que esos
        campos, en conjunto, garanticen?
    - id: RQ-CH15-04
      text: |
        ¿Por qué `authorizeAgentCommunicationMessage` nunca revalida la coherencia interna del
        `ExecutionBudget` embebido en un `DelegationGrant`, y qué componente ya existente posee esa
        validación?
  explain_prompts:
    - id: EP-CH15-01
      text: |
        `AgentCommunicationGateway` posee desacoplar la comunicación entre agentes de cualquier
        SDK/protocolo/transporte concreto y verificar el límite de delegación que un
        `DelegationGrant` ya declara. Explica, como si hablaras con alguien sin contexto técnico,
        por qué NO posee decidir si el estímulo que inició cualquiera de los dos runs comunicándose
        tenía siquiera derecho a arrancar — ¿qué se rompería si, ya que de todos modos media la
        comunicación entre los dos, también decidiera eso?
      target_entity: CMP-013
    - id: EP-CH15-02
      text: |
        `AgentCommunicationMessage.delegationGrantId` es `Optional<DelegationGrantId>`, nunca un
        campo obligatorio. Explica por qué exigir siempre un `DelegationGrant` — incluso para un
        mensaje de federación externa que no delega ninguna autoridad, solo intercambia
        información entre dos agentes independientes — inventaría una relación de delegación que
        `P-20` nunca dijo que existiera.
      target_entity: C-024
  interleaved_questions:
    - id: IQ-CH15-01
      text: |
        `AdmissionController` (CH-14) decide si un estímulo externo crudo tiene siquiera derecho a
        arrancar un run, antes de que exista un `agentId` resuelto. `AgentCommunicationGateway`
        (este capítulo) media la comunicación entre dos runs que, en ambos casos, ya lograron
        arrancar. Si un `AgentCommunicationMessage` llegara con un `sourceAgentRef` que nunca pasó
        por ninguna `AdmissionDecision` con `outcome = ADMIT`, ¿es esa ausencia responsabilidad de
        `AgentCommunicationGateway` — o esa misma pregunta, otra vez, pertenece a una frontera
        distinta y anterior, que este capítulo asume ya resuelta sin volver a verificarla?
      current_chapter_entities: [CMP-013, C-024]
      prior_chapter_entities: [CMP-012, C-023]
      prior_chapter: CH-14
    - id: IQ-CH15-02
      text: |
        `ExecutionController` (CH-07) ya evalúa, con `ExecutionDecision`, si UN `AgentRun` puede
        continuar operacionalmente contra su propio `ExecutionBudget` — turnos, tool calls,
        tokens, costo, runtime, concurrencia. `DelegationGrant.budget` (este capítulo) reutiliza el
        mismo `STRUCT ExecutionBudget` (C-012) para acotar, por separado, lo que un run delegado
        puede consumir. ¿Alcanza con que `ExecutionController` seguido evalúe ese presupuesto
        heredado como si fuera el suyo propio, o `INV-E06` exige que el límite de la relación de
        delegación en sí — cuánto se delegó, y por cuánto tiempo — tenga un dueño distinto de
        `ExecutionController`, que nunca decide a quién se le permitió delegar qué?
      current_chapter_entities: [CMP-013, C-025]
      prior_chapter_entities: [CMP-007, C-012]
      prior_chapter: CH-07
  flashcards:
    - id: FC-CH15-01
      front: |
        ¿Qué posee `AgentCommunicationGateway`?
      back: |
        Adaptar mensajes semánticos hacia/desde protocolos de interoperabilidad externos (A2A u
        otros) exclusivamente a través de adapters (`P-19`); desacoplar el core de cualquier SDK,
        protocolo o transporte concreto (`P-18`, `INV-E04`); y verificar — nunca redefinir — que
        una comunicación respaldada por un `DelegationGrant` respete su scope, su vencimiento y el
        `ExecutionBudget` acotado que ese grant ya declara (`INV-E06`).
      source_entity: CMP-013
      chapter_introduced_in: CH-15
      review_stage: DAY_1
    - id: FC-CH15-02
      front: |
        ¿Qué NO posee `AgentCommunicationGateway`?
      back: |
        Decidir si un estímulo externo crudo tiene siquiera derecho a arrancar un run
        (`AdmissionController`, CMP-012, CH-14 — pregunta anterior, sobre runs que todavía no
        existen); autorizar una acción/tool call ya resuelta (`PolicyEngine`, CMP-005, CH-05);
        decidir continuación de turno (`AgentLoop`, CMP-001, CH-01); ni el protocolo de wire o
        transporte concreto en sí — HTTP, gRPC, WebSocket, un SDK de A2A — que sigue siendo
        infraestructura de borde, fuera de este registry (mismo tratamiento que `Channel Adapter`,
        CH-06, e `Ingress Adapter`, CH-14).
      source_entity: CMP-013
      chapter_introduced_in: CH-15
      review_stage: DAY_1
    - id: FC-CH15-03
      front: |
        ¿Qué campos tiene `AgentCommunicationMessage` (C-024), y qué distingue `boundary =
        INTERNAL` de `boundary = EXTERNAL`?
      back: |
        `id`, `boundary` (`AgentCommunicationBoundary`: `INTERNAL`/`EXTERNAL`, cita literal de
        `INV-E03`, "AgentCommunication boundary"), `sourceAgentRef`/`targetAgentRef` (`Text`,
        referencias opacas — nunca `AgentId` tipado, porque un agente externo puede no tener
        ninguno en este sistema), `content` (`Value`), `delegationGrantId`
        (`Optional<DelegationGrantId>` — `NULL` cuando el mensaje no representa ninguna autoridad
        delegada), `traceId` (`TraceId`, reutilizado) y `sentAt` (`Timestamp`). `INTERNAL` es
        delegación gestionada por el mismo runtime (puede usar un protocolo interno, `P-20`);
        `EXTERNAL` es federación con un agente operado independientemente (debería usar un boundary
        basado en estándares como A2A, `P-20`).
      source_entity: C-024
      chapter_introduced_in: CH-15
      review_stage: DAY_1
    - id: FC-CH15-04
      front: |
        ¿Qué campos tiene `DelegationGrant` (C-025), y cómo satisface, cada uno, una exigencia
        literal de `P-21`?
      back: |
        `id`, `delegatingRunId` (`Optional<RunId>`, el run que delega, si existe uno), `delegatorRef`
        (`Text`, quién delegó — auditable), `delegateRef` (`Text`, a quién se delega), `delegatedScope`
        (`List<Text>`, nunca un booleano de "todo permitido" — scoped), `budget` (`ExecutionBudget`,
        C-012 reutilizado sin modificar — el presupuesto acotado del run delegado, `INV-E06`),
        `expiresAt` (`Timestamp` — time-bounded) y `grantedAt` (`Timestamp` — auditable, cuándo).
        Juntos: scoped + time-bounded + auditable, las tres propiedades que `P-21` exige
        literalmente para toda autoridad delegada.
      source_entity: C-025
      chapter_introduced_in: CH-15
      review_stage: DAY_1
    - id: FC-CH15-05
      front: |
        ¿Por qué `AgentCommunicationGateway` es el tercer componente del libro cuya función
        principal nunca construye un `AgentEvent`, y en qué se diferencia de los dos anteriores?
      back: |
        `EventBus` (CH-09) no lo construye porque no decide nada. `AdmissionController` (CH-14) no
        lo construye porque su decisión ocurre antes de que exista cualquier `AgentRun` (sin
        `runId`/`sessionId`/`agentId`/`traceId` todavía). `AgentCommunicationGateway` es distinto:
        el run casi siempre YA existe — pero `AgentCommunicationMessage` deliberadamente no tiene
        ningún campo `sessionId`, porque un agente externo federado puede no compartir el concepto
        de `Session` de este sistema en absoluto; inventar un `sessionId` centinela para construir
        el `AgentEvent` fabricaría un dato que no existe, el mismo límite que CH-14 §14 ya
        documentó para sus propios cuatro campos faltantes.
      source_entity: CMP-013
      chapter_introduced_in: CH-15
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH15-01
      recall_question: RQ-CH15-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH15-02
      recall_question: RQ-CH15-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH15-03
      recall_question: RQ-CH15-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH15-04
      recall_question: RQ-CH15-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 15 — AgentCommunicationGateway y la Frontera Explícita entre Agentes

> **Regla constitucional (Amendment v1.1, `P-19`):** "A2A or future interoperability standards
> MUST be integrated through `AgentCommunicationGateway` adapters. The core MUST NOT depend
> directly on an A2A SDK or a particular wire protocol."

CH-14 abrió el territorio de Amendment v1.1 — Enterprise cubriendo, en exclusiva, el primero de los
nueve "Canonical Enterprise Planes": Ingress & Activation Plane. Este capítulo entra al **segundo
plano que este libro cubre**, deliberadamente NO en el orden canónico que la enmienda enumera
(Ingress & Activation → Execution → Agent Interoperability → ...): en vez de profundizar el
Execution Plane (el segundo de la lista), este capítulo salta directamente al tercero — **Agent
Interoperability Plane** — porque es el plano que `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§31 nombra con su propia regla dedicada ("Regla de comunicación entre agentes": "Nunca acoplar un
agente a la implementación de otro. Usar `AgentCommunicationGateway`") y el que Amendment v1.1
respalda con cuatro principios propios (`P-18`..`P-21`) más seis invariantes (`INV-E03`..`INV-E06`,
más `INV-E07`/`INV-E08` que quedan fuera de este capítulo). El Execution Plane completo — y los
seis planos restantes — quedan, otra vez deliberadamente, para incrementos futuros (ver seccion 19).

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de saber
> cómo se llama el componente de este capítulo. El detalle estructurado de esta sección vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, para cualquier mensaje que
cruce la frontera entre dos agentes (dos runs ya en ejecución, o un run ya activo que delega parte
de su trabajo hacia un sub-agente), qué validación le pertenece en exclusiva al componente que
desacopla esa comunicación de cualquier SDK, protocolo o transporte concreto — sin decidir si el
estímulo que inició cualquiera de los dos runs tenía derecho a arrancar, sin autorizar una acción ya
resuelta, sin decidir continuación de turno — y podrás diagnosticar, para cualquier token de
delegación emitido, si la autoridad que representa está de verdad acotada en scope, en tiempo y en
presupuesto (Amendment v1.1, `P-21`), o si equivale, en la práctica, a heredar sin límite la
autoridad de quien delega.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e introduce
dos contratos de datos nuevos y el segundo componente de este libro que pertenece a Amendment v1.1
en vez de a los once nombres originales de Article III — todavía sin explicarlos, solo como mapa.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar atrás;
están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este capítulo
va a definir):

1. Cuando un agente que ya está corriendo necesita que otro agente — uno interno, gestionado por el
   mismo runtime, o uno externo, operado por un tercero completamente distinto — haga algo en su
   nombre, ¿qué necesitaría existir para que esa comunicación nunca dependa de que el runtime
   conozca, de antemano, el SDK o el protocolo de mensajería concreto que ese otro agente usa?
2. La decisión de si un estímulo externo crudo tiene siquiera derecho a arrancar un run ya tiene, en
   este libro, un dueño que actúa antes de que exista cualquier ejecución. ¿Esa misma pregunta sirve
   también para decidir si un run que YA está en marcha puede comunicarse con otro run ya en marcha,
   o es, honestamente, una pregunta distinta que necesita su propio dueño?
3. Cuando un run le pide a otro — o a un agente completamente externo, operado fuera de este
   sistema — que actúe en su nombre, ¿basta con que el que delega simplemente confíe en que el otro
   nunca hará más de lo que se le pidió, o necesita existir algo escrito, con vencimiento explícito,
   que declare exactamente cuánta autoridad se transfiere?
4. Un presupuesto operacional ya existe en este libro para acotar cuántos turnos, tool calls, tokens
   y costo puede consumir una única ejecución. Cuando esa ejecución delega parte de su trabajo hacia
   otra, ¿ese mismo presupuesto se hereda automáticamente y sin límites nuevos, o necesita una forma
   más acotada, propia de la relación de delegación, que nunca reemplace al presupuesto original?

## 1. Arquitectura Actual (Current Architecture)

CH-00..CH-14 dejaron instalados veintitrés contratos de datos y doce componentes: los once nombres
completos de Article III ("Agent Runtime"), dos capítulos de integración, y `AdmissionController`
(CMP-012, CH-14) — el primer componente de Amendment v1.1, que resolvió quién decide si un estímulo
externo crudo puede siquiera empezar a procesarse, antes de que exista un `agentId` resuelto. Ese
capítulo, sin embargo, dejó explícitamente fuera de su alcance "los ocho planes restantes de
Amendment v1.1... y sus componentes (`AgentCommunicationGateway`, `CredentialBroker`, y el resto)"
(CH-14 §18).

Ninguno de los quince nombres instalados hasta ahora — ni `AgentActivationRequest`/`AgentCore`
(C-021/CMP-011, CH-11), ni `ActivationRequest`/`AdmissionController` (C-022/C-023/CMP-012, CH-14) —
modela qué pasa cuando un agente que **ya está corriendo** necesita comunicarse con otro agente. La
palabra "agents" aparece, de hecho, ya desde `P-16` (CH-14 §1): "User prompts, APIs, webhooks,
queues, schedules, events, files, databases, systems **and other agents** are ingress mechanisms" —
pero ahí describe a otro agente como un mecanismo de **entrada** que podría disparar una nueva
activación, exactamente igual que un webhook o una cola. Ese no es el problema de este capítulo:
aquí ambos extremos de la comunicación ya son runs vivos (o, en el caso de una delegación, un run
vivo que está a punto de hacer nacer a otro).

Amendment v1.1 ya nombra, literalmente, el componente y los cuatro principios que resolverían esto —
desde la primera versión de esta enmienda adoptada por el repositorio, antes de que este capítulo
existiera:

- `P-18` ("Communication semantics are independent from protocol and transport"): "Agent
  communication MUST use explicit semantic contracts. Protocols define interoperability; transports
  define delivery. Neither belongs inside Agent Core."
- `P-19` ("External agent interoperability is adapter-based"): "A2A or future interoperability
  standards MUST be integrated through `AgentCommunicationGateway` adapters. The core MUST NOT
  depend directly on an A2A SDK or a particular wire protocol."
- `P-20` ("Internal delegation and external federation are different concerns"): "Managed
  sub-agent delegation MAY use an internal protocol. Communication with independently operated
  agents SHOULD use a standards-based federation boundary such as A2A where appropriate."
- `P-21` ("Delegated authority is explicit and least-privileged"): "A child or remote agent MUST
  NOT automatically inherit the caller's authority. Delegation MUST be scoped, time-bounded,
  auditable and represented by an explicit delegation contract/token."
- `INV-E03`: "Agent-to-agent messages cross an explicit `AgentCommunication` boundary."
- `INV-E04`: "Protocol adapters and transport adapters are replaceable independently."
- `INV-E05`: "A2A is an external interoperability option, not an Agent Core dependency."
- `INV-E06`: "Delegation depth, child runs and delegated cost are bounded by `ExecutionBudget`."

Y `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §31 ya trae, desde antes de que existiera este
capítulo, una regla editorial dedicada exclusivamente a este problema: "Regla de comunicación entre
agentes: Nunca acoplar un agente a la implementación de otro. Usar `AgentCommunicationGateway`.
Diferenciar: internal delegation, external federation, protocol y transport." Este capítulo es,
precisamente, el que paga esa deuda ya nombrada.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas para esto, "un agente necesita que otro agente haga algo
en su nombre" tiende a resolverse de la forma más simple y más peligrosa: el código de un agente
invoca directamente el SDK, el endpoint HTTP o la cola de mensajes del otro agente, porque "ya
conoce su dirección". Eso acopla al core a un protocolo y a un transporte concretos exactamente de
la misma manera que `ModelGateway` (CH-03) se negó a acoplar `AgentLoop` a un provider de modelo
específico (`P-02`) — solo que aquí el "provider" reemplazable es otro agente completo, y el costo
de acoplarse mal es mayor: cambiar de A2A a un protocolo futuro, o de HTTP a gRPC, obligaría a
reescribir la lógica del agente mismo, no solo un adapter.

Hay una segunda dimensión del problema, todavía más delicada. Cuando la comunicación entre agentes
implica que uno **delega** trabajo hacia otro — un sub-agente interno gestionado por el mismo
runtime, o incluso un agente externo actuando en su nombre — ¿qué autoridad exacta se transfiere?
`P-21` es explícito sobre el riesgo de no responder esto con cuidado: "A child or remote agent MUST
NOT automatically inherit the caller's authority." Sin un contrato que declare, por escrito, un
scope acotado, una expiración explícita y un presupuesto delegado, la alternativa por defecto es que
el sub-agente reciba, en silencio, toda la autoridad de quien delega — la superficie de riesgo se
duplica, se triplica, se multiplica con cada nivel de delegación, sin que ningún límite lo contenga.

Necesitamos que "¿puede este mensaje cruzar la frontera hacia otro agente, y con qué autoridad?"
tenga, por fin, un dueño único y nombrado — que reciba un mensaje semántico ya construido (nunca
acoplado a un protocolo o transporte concreto, `P-18`), que distinga sin ambigüedad entre delegación
interna y federación externa (`P-20`), que verifique — sin redefinirlo — el límite de
`ExecutionBudget` que un token de delegación ya declara (`INV-E06`), y que se detenga ahí, sin
decidir si el estímulo que originó cualquiera de los dos runs tenía derecho a arrancar, ni autorizar
ninguna acción ya resuelta dentro de esos runs.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los veintitrés contratos y los doce componentes que existen hasta este punto no bastan porque:

- `P-18`/`P-19`/`P-20`/`P-21`/`INV-E03`..`INV-E06` citan literalmente, desde que Amendment v1.1 fue
  adoptada, `AgentCommunicationGateway` — un nombre que ningún capítulo había materializado con
  código real; CH-14 ya lo mencionó por nombre entre los componentes explícitamente diferidos
  (CH-14 §18), sin resolverlo;
- ningún contrato de este libro representa, todavía, un mensaje semántico entre dos agentes — ni
  `AgentMessage` (C-001, CH-00, el mensaje DENTRO del ciclo cognitivo de UN agente, entre el modelo y
  el propio run) ni `ActivationRequest` (C-022, CH-14, un estímulo de ENTRADA que todavía no tiene
  agente resuelto) representan "un mensaje que ya sabe exactamente de qué agente viene y hacia qué
  agente va, cruzando una frontera explícita entre dos runs";
- ningún contrato de este libro representa, todavía, la autoridad delegada de un run hacia otro —
  `ExecutionBudget` (C-012, CH-00) acota una única ejecución contra sí misma; ninguna estructura
  existente declara scope, vencimiento y presupuesto de una relación de delegación entre DOS runs
  distintos;
- `AdmissionController` (CMP-012, CH-14) decide si un estímulo crudo puede empezar a procesarse —
  pero nunca evaluó, ni podría evaluar sin invadir Decision Ownership, si dos runs YA admitidos y YA
  en ejecución pueden comunicarse entre sí: son preguntas de dominios distintos, formuladas sobre
  material de entrada distinto (un `ActivationRequest` sin `agentId` resuelto contra un mensaje que
  ya conoce ambos extremos);
- `PolicyEngine` (CMP-005, CH-05) evalúa si una acción ya resuelta (`ToolCall`) puede ocurrir dentro
  de UN run — pero nunca evaluó si la autoridad de ESE run puede transferirse, acotada, hacia otro;
- `ExecutionController` (CMP-007, CH-07) evalúa si UN `AgentRun` puede continuar operacionalmente
  contra su propio `ExecutionBudget` — pero nunca evaluó si un `ExecutionBudget` heredado por un run
  delegado sigue siendo válido frente al token de delegación que lo acota.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la secuencia
> `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una entidad que no
> haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT` registrado — **no
> magic entities**. Este capítulo aplica la misma disciplina que CH-00..CH-14 ya establecieron, con
> una particularidad: es el segundo componente de este registry cuyo `owns` se ancla en la cita
> literal de varios principios de Amendment v1.1 (`P-18`/`P-19`/`P-21`) a la vez, no en una sola
> sección propia de Article III (que Amendment v1.1 no reescribe).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-18   Communication semantics are independent from protocol and transport.
           AgentCommunicationMessage (seccion 6/7) es el primer contrato real de este libro que
           representa comunicación entre dos agentes usando exclusivamente un contrato semántico —
           sin ningún campo de protocolo o transporte concreto (ese adapter permanece
           infraestructura de borde, fuera de este registry, mismo tratamiento que Channel
           Adapter/Ingress Adapter).
    P-19   External agent interoperability is adapter-based.
           AgentCommunicationGateway (seccion 8) es la primera materialización real del nombre que
           esta cita literal ya usaba desde que Amendment v1.1 fue adoptada — el único punto por el
           que un adapter de A2A (u otro estándar futuro) podría integrarse, nunca una dependencia
           directa del core hacia un SDK concreto.
    P-20   Internal delegation and external federation are different concerns.
           AgentCommunicationMessage.boundary (INTERNAL/EXTERNAL) formaliza, por primera vez con
           código real, la distinción que esta cita literal exige — delegación interna gestionada
           por el mismo runtime frente a federación con un agente operado independientemente.
    P-21   Delegated authority is explicit and least-privileged.
           DelegationGrant (seccion 6/7) es la primera formalización ejecutable de "a child or
           remote agent MUST NOT automatically inherit the caller's authority" — scope explícito
           (delegatedScope, nunca un booleano de "todo"), vencimiento explícito (expiresAt) y
           referencia auditable (delegatorRef/grantedAt).
    P-25   Audit evidence is distinct from operational telemetry.
           Igual que CH-14 §14, este capítulo documenta explícitamente (seccion 14/18) que
           AgentCommunicationMessage/DelegationGrant NO producen ningún AgentEvent — una auditoría
           real de cada comunicación entre agentes necesitaría, per P-25, un mecanismo distinto de
           EventBus/AgentEvent, que este capítulo tampoco construye.

Invariants preserved
    INV-E03   Agent-to-agent messages cross an explicit AgentCommunication boundary.
              Cita literal por primera vez con un contrato real: AgentCommunicationMessage.boundary
              adopta, palabra por palabra, el nombre "AgentCommunication boundary" de este
              invariante como su propio ENUM (AgentCommunicationBoundary).
    INV-E04   Protocol adapters and transport adapters are replaceable independently.
              AgentCommunicationMessage (C-024) no declara ningún campo de protocolo ni de
              transporte — ambos permanecen, deliberadamente, fuera de este registry (seccion 5),
              exactamente lo que hace posible que sean reemplazables sin tocar el contrato
              semántico.
    INV-E05   A2A is an external interoperability option, not an Agent Core dependency.
              Ningún STRUCT/ENUM/FUNCTION de este capítulo menciona A2A como un tipo o una
              dependencia real — A2A se cita únicamente en prosa (seccion 5/15), como el estándar
              que un adapter futuro (Preview, no introducido) podría implementar detrás de
              AgentCommunicationGateway.
    INV-E06   Delegation depth, child runs and delegated cost are bounded by ExecutionBudget.
              DelegationGrant.budget (STRUCT ExecutionBudget, C-012, reutilizado sin modificar) es
              la primera formalización real de este invariante; authorizeAgentCommunicationMessage
              (seccion 11) verifica — nunca redefine — que un DelegationGrant siga vigente antes de
              dejar pasar el mensaje que respalda.
    INV-18    Toda acción significativa produce un evento observable.
              Tensión real, documentada sin resolver (seccion 14, tercera instancia del mismo
              hallazgo que CH-09/CH-14 ya documentaron, por una tercera razón distinta):
              AgentCommunicationMessage no tiene ningún campo sessionId, y AgentEvent (C-010) lo
              exige como obligatorio.
    INV-19    Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy relevante.
              AgentCommunicationMessage.traceId (reutilizado de CH-00/CH-11) y
              DelegationGrant.delegatorRef/grantedAt son el ancla de trazabilidad de este capítulo.
    INV-20    Todo error operacional pertenece a una categoría conocida.
              El único fallo real de este capítulo (seccion 13) introduce DELEGATION, una categoría
              nueva de ErrorCategory — ninguna de las doce ya existentes (incluida BUDGET, que
              pertenece a ExecutionController evaluando SU PROPIO run, CH-07) representa, sin
              conflación, el rechazo de una comunicación por un token de delegación inválido.

Component ownership changes
    CMP-013 AgentCommunicationGateway se introduce — registry/components.yaml pasa de 12 a 13
    componentes. Es el segundo componente de este registry que NO corresponde a ninguno de los once
    nombres del árbol de Article III ("Agent Runtime") — pertenece, en cambio, al "Agent
    Interoperability Plane" de Amendment v1.1 (el tercer plano canónico, segundo que este libro
    cubre — ver apertura del capítulo). registry/components.yaml de CMP-005 (PolicyEngine), CMP-007
    (ExecutionController) y CMP-012 (AdmissionController) NO se modifica: ninguno cablea todavía su
    relación real con AgentCommunicationGateway (ver seccion 9/18).

Lifecycle changes
    Ninguna modificación a AgentRunStatus (C-013): este capítulo no construye, ni transiciona,
    ningún AgentState. Un DelegationGrant puede, en una integración futura, acompañar el nacimiento
    de un nuevo AgentState delegado (AgentCore, CH-11) — pero ese cableado no ocurre en este
    capítulo (ver seccion 9/18).

Security implications
    AgentCommunicationGateway es el primer componente de este libro cuya responsabilidad completa es
    de seguridad de frontera ENTRE agentes — nunca de admisión de un estímulo crudo
    (AdmissionController, CH-14) ni de autorización de una acción ya resuelta dentro de un mismo run
    (PolicyEngine, CH-05). Ver seccion 15 para el análisis completo.

Observability implications
    Tercer componente real del libro cuya función principal nunca produce un AgentEvent (C-010) —
    después de EventBus (CH-09, no decide nada) y AdmissionController (CH-14, el run todavía no
    existe) — esta vez por una tercera razón distinta: el run casi siempre YA existe, pero
    AgentCommunicationMessage deliberadamente no tiene sessionId. Ver seccion 14.

Deterministic vs agentic boundary
    Article XII se refina una decimotercera vez a nivel de componente: AgentCommunicationGateway,
    igual que AgentCore (CH-11), AdmissionController (CH-14) y EventBus (CH-09), no consume ninguna
    salida del modelo ni directa ni indirectamente. Su frontera determinística separa el contenido
    semántico de un mensaje (Value, que pudo haber sido producido, río arriba, por un modelo — pero
    este componente nunca lo interpreta) del gate determinístico — autorizado/rechazado — que decide
    si ese mensaje puede cruzar la frontera hacia otro agente.
```

## 5. Conceptos Nuevos (New Concepts)

- **AgentCommunication Boundary** *(cita literal, `INV-E03`)*: la frontera explícita que todo mensaje
  agente-a-agente debe cruzar — nunca una invocación directa de un agente hacia la implementación de
  otro. Modelada, por primera vez con código real, como `AgentCommunicationMessage.boundary`.
- **Internal Delegation**: comunicación hacia un sub-agente gestionado por el mismo runtime — `P-20`
  permite (no exige) que use un protocolo interno, y es la única forma de comunicación que este
  capítulo asocia con un `DelegationGrant` real (aunque un mensaje `INTERNAL` también puede no
  llevar ninguno, si no representa ninguna transferencia de autoridad).
- **External Federation**: comunicación con un agente operado independientemente, fuera de este
  sistema — `P-20` recomienda un boundary basado en estándares (A2A u otros) para este caso. Un
  mensaje `EXTERNAL` puede o no llevar un `DelegationGrant`, según si el agente externo actúa, o no,
  con autoridad delegada por este sistema.
- **A2A (Agent-to-Agent)**: el estándar de interoperabilidad que `P-19`/`INV-E05` citan por nombre
  como una opción externa — nunca una dependencia del core. Se enseña, en este libro, exclusivamente
  como el protocolo que un adapter futuro (Preview, no introducido) implementaría detrás de
  `AgentCommunicationGateway` — ningún `STRUCT`/`ENUM`/`FUNCTION` de este capítulo lo modela como
  tipo o dependencia real.
- **Protocol Adapter** *(concepto de infraestructura de borde, no un componente de este registry)*:
  la pieza (no modelada en detalle) que traduciría un `AgentCommunicationMessage` semántico hacia el
  formato concreto de un estándar de interoperabilidad (A2A u otro) y de vuelta — mismo tratamiento
  que `Provider Adapter` (CH-03) recibió para el lado del modelo.
- **Transport Adapter** *(concepto de infraestructura de borde, distinto de Protocol Adapter, no un
  componente de este registry)*: la pieza que entregaría físicamente un mensaje ya adaptado a un
  protocolo — HTTP, gRPC, WebSocket, SSE, una cola, un Service Bus — per
  `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §31 ("Regla de transporte": "No deben definir la
  semántica del agente"). `INV-E04` exige que ambos adapters — protocolo y transporte — sean
  reemplazables de forma independiente entre sí.
- **Federation Boundary**: el límite de confianza que separa a este sistema de un agente operado por
  un tercero independiente — la razón por la cual `External Federation` (a diferencia de
  `Internal Delegation`) debería apoyarse en un estándar público como A2A en vez de un protocolo
  interno propietario (`P-20`).
- **Delegated Authority**: la autoridad, siempre acotada, que un `DelegationGrant` transfiere de un
  run hacia un agente hijo o remoto — nunca la autoridad completa de quien delega (`P-21`, "MUST NOT
  automatically inherit the caller's authority").
- **Delegation Scope**: el conjunto explícito y finito de lo que un `DelegationGrant` autoriza —
  modelado como `delegatedScope: List<Text>`, nunca un `Boolean` de "todo permitido" (mismo espíritu
  de diseño que `PolicyDecision`/`AdmissionDecision` evitando un resultado de un solo valor
  implícito).
- **Delegation Window**: el período de validez explícito de un `DelegationGrant`, entre `grantedAt`
  y `expiresAt` — fuera de esa ventana, `authorizeAgentCommunicationMessage` (seccion 11) rechaza
  por defecto (mismo espíritu que `Default Deny`/`Default Reject`, CH-05/CH-14).
- **Decision Ownership** *(Article IV, en uso desde CH-01, aplicado aquí por segunda vez a un
  componente de Amendment v1.1)*: `AgentCommunicationGateway` decide "¿puede este mensaje cruzar la
  frontera hacia otro agente, con la autoridad que declara?"; explícitamente NO decide "¿tenía este
  estímulo derecho a arrancar un run?" (`AdmissionController`, CH-14), "¿puede esta acción ya
  resuelta ejecutarse?" (`PolicyEngine`, CH-05) ni "¿debe otro turno de razonamiento ocurrir?"
  (`AgentLoop`, CH-01).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `RunId`, `TraceId`, `Timestamp`, `Value`, `Text`,
`List`, `Optional`, `HarnessError`, `ExecutionBudget` (C-012, CH-00).

### Dos identificadores opacos nuevos

Siguiendo el mismo patrón que CH-00 §6 estableció para los identificadores fundamentales, y que
CH-14 §6 repitió para `ActivationRequestId`:

| Identificador (nuevo de este capítulo) | Identifica |
|---|---|
| `AgentCommunicationMessageId` | un `AgentCommunicationMessage` concreto — el mensaje semántico que cruza una frontera de comunicación entre agentes |
| `DelegationGrantId` | un `DelegationGrant` concreto — el token de autoridad delegada que este capítulo evalúa |

### `ErrorCategory` — extendido, sin redefinir `HarnessError`

Este es el cuarto capítulo que agrega un valor a `ErrorCategory` desde que CH-00 lo declaró (después
de `HUMAN_INTERACTION`, CH-06, y `ADMISSION`, CH-14): el valor `DELEGATION`, necesario porque
ninguna de las doce categorías ya existentes representa, sin conflación, el rechazo de una
comunicación por un `DelegationGrant` inválido — `BUDGET` pertenece, en exclusiva, a la pregunta de
`ExecutionController` sobre si UN run puede continuar contra SU PROPIO `ExecutionBudget` (CH-07), y
reutilizarla aquí confundiría dos decisiones de dominios distintos, con dueños distintos, sobre
presupuestos distintos:

```pseudocode
ENUM ErrorCategory
    VALIDATION
    POLICY
    TOOL
    MODEL
    CONTEXT
    PERSISTENCE
    INFRASTRUCTURE
    BUDGET
    CANCELLATION
    FATAL
    HUMAN_INTERACTION
    ADMISSION
    DELEGATION
END
```

`HarnessError` (C-011) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — mismo patrón
exacto que las extensiones de CH-06 y CH-14, aplicado aquí por tercera vez a `ErrorCategory`.

### `AgentCommunicationBoundary` — la distinción literal de `INV-E03`/`P-20`

```pseudocode
ENUM AgentCommunicationBoundary
    INTERNAL
    EXTERNAL
END
```

`INTERNAL` es delegación hacia un sub-agente gestionado por el mismo runtime (`P-20`: "Managed
sub-agent delegation MAY use an internal protocol"). `EXTERNAL` es federación con un agente operado
independientemente (`P-20`: "Communication with independently operated agents SHOULD use a
standards-based federation boundary such as A2A"). Ningún tercer valor: un mensaje siempre sabe, sin
ambigüedad, de qué lado de esa frontera nació.

### `AgentCommunicationMessage` — el contrato semántico explícito que exige `P-18`

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
END
```

Ocho campos, cada uno respondiendo a una parte exacta del alcance decidido para este capítulo: `id`
identifica este mensaje de forma estable; `boundary` es la distinción de la sección anterior;
`sourceAgentRef`/`targetAgentRef` son referencias opacas (`Text`) al agente que envía y al agente
que recibe; `content` es el contenido semántico del mensaje (tipado como `Value`, el mismo primitivo
genérico que `AgentMessage.content`, C-001, CH-00, ya usa — este capítulo no le exige una forma más
estricta, porque interpretar ese contenido es trabajo del agente receptor, nunca de
`AgentCommunicationGateway`); `delegationGrantId` correlaciona este mensaje con el `DelegationGrant`
que autoriza la autoridad que transporta, cuando la transporta; `traceId` reutiliza el `TraceId` ya
existente (CH-00/CH-11) para que este mensaje pueda ubicarse dentro de la traza de la ejecución que
lo originó; `sentAt` registra cuándo se envió.

**Por qué `sourceAgentRef`/`targetAgentRef` son `Text`, no `AgentId`.** Se evaluó explícitamente
tipar ambos campos como `AgentId` (C-002, CH-00), el identificador ya existente y fuertemente tipado
de un agente registrado en este sistema. Se descartó: cuando `boundary = EXTERNAL`, el agente
objetivo puede ser un agente operado por un tercero completamente independiente, que este sistema
nunca registró y que no tiene, ni tendrá nunca, un `AgentId` propio — exigir `AgentId` aquí habría
hecho imposible representar, con el mismo `STRUCT`, la mitad de los casos que `boundary` existe
precisamente para distinguir. `Text` — una referencia opaca, igual que `ActivationRequest.
externalIdentityRef` (C-022, CH-14) — mantiene un único contrato válido para ambos lados de la
frontera, sin condicionar su forma al valor de `boundary`.

**Por qué `delegationGrantId` es `Optional`, no obligatorio.** `P-20` distingue delegación interna
de federación externa, pero ninguna de las dos implica, por sí sola, que exista una transferencia de
autoridad: dos agentes pueden federarse (`boundary = EXTERNAL`) simplemente para intercambiar
información, sin que ninguno delegue nada hacia el otro — y, más sutilmente, ni siquiera toda
delegación interna necesita, en principio, un token explícito si un capítulo futuro decidiera
modelar un caso distinto. Exigir `delegationGrantId` siempre habría inventado una relación de
delegación en mensajes que, honestamente, nunca la tuvieron — el mismo argumento que motivó, en
CH-14 §6, que `ActivationRequest` no exigiera un `agentId` que todavía no existía.

### `DelegationGrant` — el contrato/token de delegación explícito que exige `P-21`

```pseudocode
STRUCT DelegationGrant
    id: DelegationGrantId
    delegatingRunId: Optional<RunId>
    delegatorRef: Text
    delegateRef: Text
    delegatedScope: List<Text>
    budget: ExecutionBudget
    expiresAt: Timestamp
    grantedAt: Timestamp
END
```

Ocho campos, cada uno satisfaciendo, de forma literal, una de las tres propiedades que `P-21` exige
("scoped, time-bounded, auditable"): `id` identifica este grant de forma estable, para que un
`AgentCommunicationMessage` pueda correlacionarse con él; `delegatingRunId` es `Optional<RunId>` —
el `AgentRun` (C-003, CH-00) ya existente que originó la delegación, cuando existe uno (`NULL` si el
grant se emitió fuera de cualquier run modelado por este libro, por ejemplo por un proceso
operativo); `delegatorRef`/`grantedAt` son la referencia auditable que `P-21` exige — quién delegó y
cuándo; `delegateRef` es una referencia opaca al agente hijo o remoto que recibe la autoridad
(`Text`, mismo argumento que `sourceAgentRef`/`targetAgentRef` en `AgentCommunicationMessage`: el
delegado puede no tener ningún `AgentId` local); `delegatedScope` es el scope explícito y acotado —
**nunca** "toda la autoridad" (satisface "scoped"); `budget` reutiliza `ExecutionBudget` (C-012, sin
modificarlo) como el presupuesto acotado del run delegado (`INV-E06`); `expiresAt` es el vencimiento
explícito que satisface "time-bounded".

**Por qué `delegatedScope` es `List<Text>`, nunca un `Boolean`.** Se evaluó explícitamente un campo
`allowAll: Boolean` — más simple de construir. Se descartó de inmediato: `P-21` prohíbe, literalmente,
que un agente hijo o remoto herede automáticamente toda la autoridad de quien delega
("MUST NOT automatically inherit the caller's authority"); un `Boolean` que pudiera valer `TRUE`
haría posible, por diseño del propio contrato, exactamente la violación que ese principio prohíbe.
`List<Text>` — un conjunto explícito, finito, de lo que se delega — hace estructuralmente imposible
que un `DelegationGrant` represente "todo", sin necesidad de ninguna validación adicional en tiempo
de ejecución.

**Por qué `budget` reutiliza `ExecutionBudget` (C-012) en vez de un tipo nuevo.** `INV-E06` exige,
literalmente, que "delegation depth, child runs and delegated cost are bounded by `ExecutionBudget`"
— el mismo `STRUCT` que ya acota una única ejecución (CH-00, con cumplimiento real desde CH-07).
Introducir un tipo de presupuesto distinto para la relación de delegación habría fragmentado, sin
necesidad, el único mecanismo de límites operacionales que este libro ya tiene — y habría exigido
que `ExecutionController` (CH-07) aprendiera a evaluar dos formas distintas de presupuesto.
`DelegationGrant.budget` es, en cambio, un **valor** — una instancia de `ExecutionBudget` tan acotada
como haga falta, nunca el mismo `STRUCT` "más flexible" — que un capítulo de integración futuro
podría pasarle a `AgentCore` (CH-11) al activar el `AgentState` del run delegado.

**Unchanged / Not yet introduced**: `ExecutionBudget` (C-012) y `RunId`/`TraceId`/`Timestamp` no
cambian de forma — este capítulo los consume, nunca los modifica. Ningún `ENUM` de estado propio
para `DelegationGrant`: a diferencia de `HumanInteractionRequest` (CH-06) o `EventSubscription`
(CH-09), un grant no transiciona entre estados con código propio — su vigencia se deriva, en cada
evaluación, exclusivamente de comparar `now()` contra `expiresAt` (ver seccion 12).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce dos contratos de
datos, registrados en `registry/contracts.yaml`:

```text
ID:                     C-024
Name:                   AgentCommunicationMessage
Version:                v1
Introduced In:          CH-15
Current Definition:     STRUCT AgentCommunicationMessage (ver §6)
Used By:                [CMP-013]
Modified By:            []
Constitutional Impact:  [P-18, P-20, INV-E03, INV-E04]
```

```text
ID:                     C-025
Name:                   DelegationGrant
Version:                v1
Introduced In:          CH-15
Current Definition:     STRUCT DelegationGrant (ver §6)
Used By:                [CMP-013]
Modified By:            []
Constitutional Impact:  [P-21, INV-E06, INV-19]
```

`C-024` y `C-025` son el undécimo y el duodécimo id que este libro asigna sin que estuvieran
reservados desde CH-01 §7 — el correlativo simplemente continúa después de `C-023` (CH-14). Ninguno
colisiona, por nombre, con ningún contrato ya registrado — verificado con grep completo sobre
`registry/contracts.yaml` antes de escribir este capítulo.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el segundo componente del registry que no corresponde a ninguno de los once
nombres del árbol de Article III ("Agent Runtime") — pertenece, en cambio, al "Agent
Interoperability Plane" de Amendment v1.1:

```pseudocode
COMPONENT AgentCommunicationGateway
    consumes: AgentCommunicationMessage, DelegationGrant
    produces: AgentCommunicationMessage, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Amendment v1.1 (`P-18`/`P-19`/`P-21`) — Article III no
tiene, todavía, una sección propia para este componente, exactamente igual que `AdmissionController`
(CH-14):

```text
COMPONENT: AgentCommunicationGateway

Responsibility:
    Adaptar mensajes semánticos hacia/desde protocolos de interoperabilidad externos (A2A u otros)
    exclusivamente a través de adapters, desacoplando el core de cualquier SDK, protocolo o
    transporte concreto — y verificar, sin redefinirlo, que una comunicación respaldada por un
    DelegationGrant respete el scope, el vencimiento y el ExecutionBudget acotado que ese grant ya
    declara — sin decidir si el estímulo que originó cualquiera de los dos runs comunicándose tenía
    derecho a arrancar, sin autorizar ninguna acción ya resuelta y sin decidir continuación de
    turno.

Consumes:
    C-024 AgentCommunicationMessage, C-025 DelegationGrant

Depends on:
    (ninguno todavía — el cableado real hacia un Protocol Adapter/Transport Adapter concreto, hacia
    AgentCore para runs delegados nuevos, y hacia ExecutionController para el run delegado ya en
    marcha, es Preview, no introducido en este capítulo; ver seccion 9)

Produces:
    C-024 AgentCommunicationMessage (el mismo mensaje, ya autorizado, listo para que un Protocol
    Adapter fuera de este registry lo entregue), C-011 HarnessError

Owns (Amendment v1.1, `P-18`/`P-19`/`P-21`/`INV-E06`, cita y lectura literal):
    - "Agent communication MUST use explicit semantic contracts. Protocols define interoperability;
      transports define delivery. Neither belongs inside Agent Core" (cita literal, P-18)
    - "A2A or future interoperability standards MUST be integrated through AgentCommunicationGateway
      adapters. The core MUST NOT depend directly on an A2A SDK or a particular wire protocol"
      (cita literal, P-19)
    - distinguir siempre delegación interna de federación externa (boundary, P-20)
    - verificar — nunca redefinir — que un DelegationGrant que respalda un mensaje siga vigente
      (no expirado), cubra lo que el mensaje pide (scope) y respete el ExecutionBudget acotado que
      declara (INV-E06)
    - rechazar por defecto (fail-closed) cuando un DelegationGrant declarado no se encuentra, no
      corresponde, expiró o no cubre el mensaje

Does NOT own:
    - decidir si el estímulo externo crudo que originó cualquiera de los dos runs comunicándose
      tenía siquiera derecho a arrancar (AdmissionController, CMP-012, ya introducido en CH-14 —
      pregunta anterior, sobre un ActivationRequest todavía sin agentId resuelto; este componente
      asume que ambos extremos de la comunicación ya superaron esa admisión)
    - autorizar una acción/tool call ya resuelta dentro de un run (PolicyEngine, CMP-005, ya
      introducido en CH-05 — distinto momento, distinta pregunta: "¿puede este mensaje cruzar hacia
      otro agente?" vs. "¿puede esta acción ejecutarse dentro de este run?")
    - decidir si otro turno de razonamiento debe ocurrir (AgentLoop, CMP-001, ya introducido en
      CH-01)
    - el protocolo de wire o el transporte concreto en sí — HTTP, gRPC, WebSocket, un SDK de A2A
      (Protocol Adapter / Transport Adapter — infraestructura de borde, INV-E04, no un componente
      propio de este registry, mismo tratamiento que Channel Adapter, CH-06, e Ingress Adapter,
      CH-14)
    - revalidar la coherencia interna del ExecutionBudget embebido en un DelegationGrant (AgentCore,
      CMP-011, ya introducido en CH-11 — isExecutionBudgetCoherent ya existe ahí; este componente
      asume que un DelegationGrant ya construido trae un budget coherente, y solo verifica que siga
      vigente y cubierto para ESTE mensaje)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con la misma
particularidad que `AdmissionController` (CH-14): ninguna de las cuatro exclusiones proviene de una
ficha propia de Article III (que no existe para este componente); provienen de fronteras ya
establecidas por Amendment v1.1 (`INV-E04`) o por componentes ya registrados (`AdmissionController`,
`PolicyEngine`, `AgentLoop`, `AgentCore`).

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
AgentCommunicationGateway
    consumes → AgentCommunicationMessage, DelegationGrant
    produces → AgentCommunicationMessage, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`AgentCommunicationGateway` no depende hoy de ningún otro componente registrado — mismo patrón que
CH-01..CH-14 ya establecieron para sus propios componentes. En prosa (nunca dentro de un bloque
`pseudocode`, per `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las relaciones
futuras que un capítulo de integración agregaría son:

| Componente futuro (relación inversa — no cableada en este capítulo) | Qué relación tendría con `AgentCommunicationGateway` |
|---|---|
| Un Protocol Adapter/Transport Adapter concreto (todavía sin componente propio en este registry) | tomaría un `AgentCommunicationMessage` ya autorizado por este capítulo y lo traduciría/entregaría hacia el estándar y el transporte concretos (A2A sobre HTTP, por ejemplo) — una decisión que `INV-E04` coloca explícitamente fuera de este componente |
| `AgentCore` (ya existente, CMP-011) | recibiría, en una delegación interna admitida, el `budget` acotado de un `DelegationGrant` para activar el `AgentState` del run delegado — `AgentCore.activateAgent` (CH-11) no cambia una sola línea de su código ya publicado para que este capítulo sea correcto |
| `ExecutionController` (ya existente, CMP-007) | seguiría evaluando, sin cambios, si el run delegado ya activado puede continuar operacionalmente contra el `ExecutionBudget` que heredó — una pregunta distinta de "¿el `DelegationGrant` que autorizó esa delegación sigue vigente?", que sigue siendo de `AgentCommunicationGateway` |
| `AdmissionController` (ya existente, CMP-012) | seguiría decidiendo, sin cambios, si un estímulo externo crudo puede empezar a procesarse — incluyendo, en una integración futura, un estímulo que representa una solicitud de federación entrante desde un agente externo, antes de que ese agente externo tenga ningún `AgentCommunicationMessage` real que enviar |

`registry/components.yaml` de `CMP-005` (`PolicyEngine`), `CMP-007` (`ExecutionController`), `CMP-011`
(`AgentCore`) y `CMP-012` (`AdmissionController`) **no se modifica** en este capítulo: ninguno agrega
`CMP-013` a sus `dependencies`, y ninguno cambia su pseudocódigo. El pseudocódigo de la seccion 11
evalúa un `AgentCommunicationMessage`/`DelegationGrant` de forma completamente autónoma — sin que
ninguno de los cuatro componentes ya existentes cambie una sola línea para que este capítulo sea
correcto. Ese cableado real es, explícitamente, trabajo de un capítulo de integración futuro (ver
seccion 18/19).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14), siguiendo la forma que `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §31 ("Regla de
comunicación entre agentes") exige: nunca acoplar un agente a la implementación de otro, y
diferenciar siempre internal delegation, external federation, protocol y transport.

**Vista 1 — Componentes**

```text
[AgentRun de origen — ya RUNNING, CMP-001 AgentLoop, Preview] →
[DelegationGrant — Preview de emisión, asumido ya construido] →
AgentCommunicationGateway →
[Protocol Adapter / Transport Adapter — infraestructura de borde, fuera de este registry] →
[AgentRun destino — un sub-agente interno (CMP-011 AgentCore, Preview) o un agente externo,
 operado independientemente, fuera de este sistema]
```

**Vista 2 — Sequence**

```text
AgentCommunicationMessage
   │ (id, boundary, sourceAgentRef, targetAgentRef, content, delegationGrantId opcional, traceId,
   │  sentAt)
   ▼
AgentCommunicationGateway
   │ authorizeAgentCommunicationMessage(message, grant)
   │ ¿message.delegationGrantId == NULL? sí → no representa autoridad delegada, deja pasar el
   │                                          mensaje sin evaluar ningún DelegationGrant
   │ ¿message.delegationGrantId != NULL?
   │   ¿existe un DelegationGrant correspondiente? no → HarnessError (DELEGATION_GRANT_NOT_FOUND)
   │   ¿grant.id coincide con delegationGrantId? no → HarnessError (DELEGATION_GRANT_MISMATCH)
   │   ¿ya expiró (now() > grant.expiresAt)? sí → HarnessError (DELEGATION_GRANT_EXPIRED)
   │   ¿delegatedScope cubre lo que el mensaje pide? no → HarnessError (DELEGATION_SCOPE_EXCEEDED)
   ▼
AgentCommunicationMessage (el mismo mensaje, ya autorizado a cruzar la frontera)
   │
   │ ... integración futura: un Protocol Adapter (Preview, fuera de este registry) lo traduce hacia
   │     A2A u otro estándar, y un Transport Adapter (Preview) lo entrega por HTTP/gRPC/una cola —
   │     ninguno de los dos es responsabilidad de AgentCommunicationGateway ...
```

**Vista 3 — Pseudocódigo**

Ver §11: `authorizeAgentCommunicationMessage` es la primera formalización ejecutable de "ningún
agente hijo o remoto hereda automáticamente la autoridad de quien delega" (`P-21`) — construida
exclusivamente a partir de material que ya existe (`HarnessError`, `ExecutionBudget` desde CH-00)
más los dos contratos nuevos de este capítulo.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde CH-00/CH-11.

```pseudocode
FUNCTION authorizeAgentCommunicationMessage(
    message: AgentCommunicationMessage,
    grant: Optional<DelegationGrant>
) -> AgentCommunicationMessage

    IF message.delegationGrantId == NULL
        RETURN message
    END

    IF grant == NULL
        notFound: HarnessError = HarnessError(
            category = DELEGATION,
            code = "DELEGATION_GRANT_NOT_FOUND",
            message = "authorizeAgentCommunicationMessage recibió un AgentCommunicationMessage con delegationGrantId poblado, pero ningún DelegationGrant correspondiente",
            recoverable = TRUE,
            retryable = FALSE,
            metadata = {}
        )
        THROW notFound
    END

    IF grant.id != message.delegationGrantId
        mismatched: HarnessError = HarnessError(
            category = DELEGATION,
            code = "DELEGATION_GRANT_MISMATCH",
            message = "el DelegationGrant recibido no corresponde al delegationGrantId declarado por el AgentCommunicationMessage",
            recoverable = TRUE,
            retryable = FALSE,
            metadata = {}
        )
        THROW mismatched
    END

    IF now() > grant.expiresAt
        expired: HarnessError = HarnessError(
            category = DELEGATION,
            code = "DELEGATION_GRANT_EXPIRED",
            message = "el DelegationGrant que autorizaría este AgentCommunicationMessage ya expiró (expiresAt quedó en el pasado)",
            recoverable = TRUE,
            retryable = FALSE,
            metadata = {}
        )
        THROW expired
    END

    IF NOT delegationScopeCoversMessage(grant, message)
        outOfScope: HarnessError = HarnessError(
            category = DELEGATION,
            code = "DELEGATION_SCOPE_EXCEEDED",
            message = "el AgentCommunicationMessage pide algo fuera del delegatedScope explícito de su DelegationGrant",
            recoverable = TRUE,
            retryable = FALSE,
            metadata = {}
        )
        THROW outOfScope
    END

    RETURN message
END
```

`now()` es la misma primitiva de CH-00/CH-14. `delegationScopeCoversMessage(grant: DelegationGrant,
message: AgentCommunicationMessage) -> Boolean` es una primitiva nueva de este capítulo, en el mismo
espíritu que `admissionRulesGrantAccess(...)` (CH-14) o `policyRuleAllows(...)` (CH-05): una función
determinista ya asumida, sin ficha ni registro propio — este capítulo no modela cómo se compara,
concretamente, `grant.delegatedScope` contra el `content` de un mensaje, ni cómo se trackea el
consumo acumulado de `grant.budget` a través de múltiples mensajes (ver seccion 18 para el porqué de
este límite de alcance).

**Por qué este capítulo usa `THROW`, y no un `STRUCT` de decisión como `PolicyDecision`/
`AdmissionDecision`.** Se evaluó explícitamente introducir un tercer contrato — algo como
`AgentCommunicationDecision`, con un `outcome` de dos valores, siguiendo el mismo molde que
`PolicyDecision` (CH-05) o `AdmissionDecision` (CH-14). Se descartó, deliberadamente, para mantener
el alcance de este capítulo en exactamente dos contratos: a diferencia de `PolicyEngine`/
`AdmissionController` — que evalúan una acción o una activación **todavía sin resolver**, contra un
espacio de reglas de negocio con más de un resultado igualmente válido (allow/deny/require_approval;
admit/reject, cada uno con un componente vecino distinto que reacciona de forma distinta) —, este
capítulo verifica la integridad de un `DelegationGrant` **ya emitido**: un token que, en el momento
de evaluarse, o sigue siendo válido, o no. No existe ningún componente vecino que reaccione de forma
distinta a "expiró" frente a "no cubre el scope" — ambos casos significan, para
`AgentCommunicationGateway`, exactamente lo mismo: el mensaje no cruza la frontera. Esa es la misma
naturaleza de precondición que `AgentCore.activateAgent`/`beginAgentInitialization` (CH-11) ya
verifican sobre un `AgentConfig`/`AgentState` ya existentes — no una decisión de negocio con ramas
igualmente válidas, sino la integridad de un artefacto ya emitido, verificada antes de dejarlo
actuar. `HarnessError` (ya producido por este componente, ver ficha §8) sigue siendo la forma en la
que el llamador se entera de **por qué** se rechazó — sin necesitar un tercer contrato solo para
envolver un resultado binario.

Nótese también lo que `authorizeAgentCommunicationMessage` **no** hace: no invoca `AgentCore`
(CH-11) ni construye ningún `AgentState`; no invoca `PolicyEngine.evaluatePolicyForToolCall` (CH-05)
ni `AdmissionController.evaluateAdmissionForActivationRequest` (CH-14); no interpreta ni transforma
`message.content`; no revalida la coherencia interna de `grant.budget` (`isExecutionBudgetCoherent`,
CH-11, ya lo hizo cuando el grant se construyó); y — como `AdmissionController` (CH-14) — no emite
ningún `AgentEvent` (ver seccion 14 para el hallazgo real y su porqué, distinto del de CH-14).

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013): sigue siendo, sin cambios, el mismo
`ENUM` de once estados que `AgentLoop` (CH-01) formalizó. `AgentCommunicationMessage` y
`DelegationGrant` no tienen, deliberadamente, ningún `ENUM` de estados propio — mismo patrón que
`ActivationRequest`/`AdmissionDecision` (CH-14 §12) ya establecieron: se evalúan de forma síncrona,
y la vigencia de un `DelegationGrant` se deriva, en cada evaluación, exclusivamente de comparar
`now()` contra `expiresAt` — nunca de una transición persistida `ACTIVE → EXPIRED` con su propio
`STRUCT`.

```text
(authorizeAgentCommunicationMessage, AgentCommunicationMessage recibido)
   → message.delegationGrantId == NULL
     (el mensaje no representa ninguna autoridad delegada; cruza la frontera sin evaluar ningún
     DelegationGrant — la única rama de este capítulo que nunca puede fallar)

   → message.delegationGrantId != NULL, DelegationGrant válido y vigente
     (el mensaje cruza la frontera con la autoridad que el grant declara; falta todavía que un
     Protocol Adapter/Transport Adapter, Preview, lo entregue hacia su destino real)

   → message.delegationGrantId != NULL, DelegationGrant ausente / no coincide / expirado / fuera de
     scope
     (HarnessError, categoría DELEGATION; el mensaje nunca cruza la frontera — ningún AgentRun
     delegado llega a activarse a partir de este mensaje)
```

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6, extendido en la seccion 6 de este capítulo) clasifica también
los cuatro fallos reales que introduce este capítulo:

```text
DELEGATION
    DELEGATION_GRANT_NOT_FOUND     — message.delegationGrantId está poblado, pero ningún
                                      DelegationGrant correspondiente fue provisto a la evaluación
        → recoverable: TRUE, retryable: FALSE
    DELEGATION_GRANT_MISMATCH      — el DelegationGrant provisto no corresponde al
                                      delegationGrantId que el mensaje declara
        → recoverable: TRUE, retryable: FALSE
    DELEGATION_GRANT_EXPIRED       — el DelegationGrant que respaldaría este mensaje ya superó su
                                      expiresAt
        → recoverable: TRUE, retryable: FALSE
    DELEGATION_SCOPE_EXCEEDED      — el mensaje pide algo fuera del delegatedScope explícito del
                                      DelegationGrant
        → recoverable: TRUE, retryable: FALSE
```

Los cuatro fallos son `recoverable = TRUE` (el problema es corregible — emitir un nuevo
`DelegationGrant` con el scope o la vigencia correctos resolvería cualquiera de los cuatro) pero
`retryable = FALSE` (reintentar exactamente el mismo mensaje contra exactamente el mismo grant
fallaría de forma idéntica) — mismo razonamiento exacto que `NO_ADMISSION_RULE_GRANTS_ACCESS`
(CH-14) ya estableció para su propio fail-closed.

**La distinción más importante de esta sección**: ninguno de los cuatro fallos se clasifica como
`category = BUDGET` — aunque `DELEGATION_SCOPE_EXCEEDED` podría, a primera vista, parecer una
cuestión de presupuesto. `BUDGET` (CH-07) pertenece, en exclusiva, a la pregunta de
`ExecutionController` sobre si UN `AgentRun` ya en marcha puede continuar contra SU PROPIO
`ExecutionBudget` — una pregunta operacional, evaluada turno a turno, sobre una ejecución que ya
existe. `DELEGATION_SCOPE_EXCEEDED` es, en cambio, sobre si un `DelegationGrant` — un token, no una
ejecución — cubre lo que un mensaje concreto pide, antes de que ese mensaje cruce siquiera la
frontera. Reutilizar `BUDGET` aquí habría conflacionado dos decisiones de dos componentes distintos,
exactamente el error que Article IV (Ownership Rule) prohíbe — el mismo argumento que CH-14 §6 ya
usó para no reutilizar `POLICY`.

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo de `category = INFRASTRUCTURE`
que pudiera ocurrir en un Protocol Adapter o Transport Adapter real (por ejemplo, un endpoint de A2A
completamente inalcanzable) — ese valor de `ErrorCategory` sigue, después de este capítulo, sin que
ningún componente real lo haya ejercitado nunca (mismo límite que CH-11 §13/CH-14 §13 ya
documentaron para sus propias primitivas asumidas).

## 14. Eventos Producidos (Events Produced)

**Este es el tercer componente real del libro cuya función principal nunca construye un
`AgentEvent`** — después de `EventBus` (CH-09, no decide nada) y `AdmissionController` (CH-14, el
run todavía no existe) —, por una **tercera razón distinta**. Este capítulo no agrega ningún valor
nuevo a `AgentEventType`.

**El hallazgo real, verificado y documentado sin ocultarlo.** A diferencia de `AdmissionController`
(CH-14), donde ninguno de los cuatro campos obligatorios de `AgentEvent` (`runId`, `sessionId`,
`agentId`, `traceId`) existía todavía, aquí la situación es más sutil: en la mayoría de los casos, un
`AgentCommunicationMessage` ocurre cuando el run de origen (y, si es delegación interna, también el
run destino) **ya existen** — `traceId` incluso está disponible directamente en el propio
`AgentCommunicationMessage` (seccion 6). El problema real es distinto: `AgentEvent` (C-010, CH-00)
exige `sessionId: SessionId` como campo obligatorio, nunca `Optional` — y
`AgentCommunicationMessage` **deliberadamente no tiene ningún campo `sessionId`** (seccion 6). Esa
ausencia no es un descuido: cuando `boundary = EXTERNAL`, el agente objetivo puede ser un sistema
completamente independiente que no comparte, en absoluto, el concepto de `Session`
(`SessionManager`, CH-10) de este runtime — inventar un `sessionId` centinela, o reutilizar el del
run de origen para representar también al destino externo, fabricaría un dato que no existe,
exactamente el tipo de solución artificial que este libro evita (mismo principio que CH-13 §14 y
CH-14 §14 ya establecieron, cada uno para su propio campo faltante).

**La relación con `P-25` (Amendment v1.1: "Audit evidence is distinct from operational
telemetry").** Igual que CH-14 §14 concluyó para `AdmissionDecision`, esta ausencia es, precisamente,
la distinción que `P-25` exige explícitamente: `AgentEvent`/`EventBus` (Article X) modelan telemetría
operacional de UN `AgentRun`, con su propia `Session` — nunca fueron diseñados para representar una
comunicación que puede cruzar hacia un sistema que no comparte esa noción. Una evidencia de auditoría
real de cada `AgentCommunicationMessage`/`DelegationGrant` (quién delegó, a quién, con qué scope,
cuándo) necesitaría, per `P-25`, un mecanismo **distinto** de `EventBus` — uno que este capítulo no
construye. Lo único que este capítulo deja disponible para esa auditoría futura es la correlación
mínima que `AgentCommunicationMessage.traceId` y `DelegationGrant.delegatorRef`/`grantedAt` ya
proveen.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

`AgentCommunicationGateway` es el primer componente de este libro cuya responsabilidad completa es
de seguridad de **frontera entre agentes** — no de admisión de un estímulo crudo (eso sigue siendo,
en exclusiva, de `AdmissionController`, CH-14, `P-17`), ni de autorización de una acción ya resuelta
dentro de un mismo run (eso sigue siendo, en exclusiva, de `PolicyEngine`, CH-05, `P-13`).

**La distinción con `AdmissionController` (CH-14), explícita y completa.** `AdmissionController.
evaluateAdmissionForActivationRequest` (CH-14) recibe un `ActivationRequest` que todavía **no tiene**
ningún `agentId` resuelto, y decide si ese estímulo crudo puede siquiera empezar a procesarse.
`AgentCommunicationGateway.authorizeAgentCommunicationMessage` (este capítulo) recibe un
`AgentCommunicationMessage` que **ya sabe**, en `sourceAgentRef`/`targetAgentRef`, exactamente entre
qué dos agentes ocurre la comunicación — ambos, se asume, ya superaron cualquier admisión que les
correspondiera. Este capítulo nunca vuelve a verificar esa admisión: si un `sourceAgentRef` llegara
sin haber pasado nunca por una `AdmissionDecision` con `outcome = ADMIT`, ese sería un hueco de una
frontera **anterior y distinta** (ver `IQ-CH15-01`, frontmatter), nunca una responsabilidad de
`AgentCommunicationGateway` — exactamente el mismo cuidado de límites que CH-14 §15 ya aplicó frente
a `PolicyEngine`/`AgentCore`.

**La distinción con `PolicyEngine` (CH-05), explícita y completa.** `PolicyEngine.
evaluatePolicyForToolCall` (CH-05) decide si una acción **ya resuelta**, dentro de UN run, puede
ejecutarse. `AgentCommunicationGateway` decide si un mensaje puede **cruzar hacia otro run** — nunca
qué puede hacer ese run, una vez que el mensaje ya llegó, con la información o la autoridad que
recibió; esa siguiente pregunta le pertenece, de nuevo, a `PolicyEngine`, evaluado dentro del run
destino, no a este componente.

**`P-19`/`INV-E05`, aplicados con cuidado.** Ningún `STRUCT`/`ENUM`/`FUNCTION` de este capítulo
depende de A2A como tipo o como dependencia real — A2A se menciona únicamente como el estándar que
un Protocol Adapter futuro (Preview, fuera de este registry) podría implementar detrás de
`AgentCommunicationGateway`. Esto es, literalmente, lo que hace posible que `INV-E05` ("A2A is an
external interoperability option, not an Agent Core dependency") se cumpla por construcción: si
`AgentCommunicationMessage` tuviera un campo `a2aEnvelope` o si `authorizeAgentCommunicationMessage`
invocara un SDK de A2A directamente, el core dependería de un protocolo concreto — exactamente lo
que `P-19` prohíbe.

**Lo que este capítulo NO implementa todavía.** `delegationScopeCoversMessage` (seccion 11) es una
primitiva asumida: ningún mecanismo real de comparación entre `delegatedScope` y el contenido de un
mensaje, ni ningún trackeo de consumo acumulado de `grant.budget` a través de múltiples mensajes
(profundidad de delegación encadenada, `INV-E06` "delegation depth"), se modela en detalle — la
misma clase de límite que CH-05 §18 documentó para el almacenamiento real de policy rules. Tampoco
se modela ningún Protocol Adapter/Transport Adapter concreto, ni el mecanismo real por el cual un
`DelegationGrant` se emite en primer lugar (seccion 9/18).

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST AgentCommunicationGatewayPassesThroughMessagesWithoutADelegationGrant
TEST AgentCommunicationGatewayRejectsAMissingDelegationGrant
TEST AgentCommunicationGatewayRejectsAMismatchedDelegationGrant
TEST AgentCommunicationGatewayRejectsAnExpiredDelegationGrant
TEST AgentCommunicationGatewayRejectsAMessageOutsideDelegatedScope
TEST AgentCommunicationGatewayNeverInvokesAConcreteA2ASdkOrWireProtocol
TEST AgentCommunicationGatewayNeverDecidesActivationAdmission
TEST DelegationGrantNeverRepresentsUnboundedAuthority
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (después de CH-15 — segundo plano de Amendment v1.1 cubierto por este libro)

Constitution
 ├── Article III  — Component Sovereignty (once componentes de "Agent Runtime", sin cambios desde
 │                   CH-11)
 ├── Article IV   — Decision Ownership (tabla original sin cambios; AgentCommunicationGateway
 │                   documentado en prosa, igual que AdmissionController, CH-14)
 └── Amendment v1.1 — Enterprise Activation, Interoperability and Operations
                       (P-16..P-21/INV-E01..INV-E06 citados por primera vez con código real;
                       Ingress & Activation Plane, CH-14, y Agent Interoperability Plane, este
                       capítulo, los dos primeros de nueve planos canónicos instalados)

Contracts (registry/contracts.yaml)
 ├── C-001..C-023  (sin cambios — CH-00..CH-14)
 ├── C-024 AgentCommunicationMessage  (CH-15, nuevo — el contrato semántico explícito que cruza una
 │                                     frontera entre dos agentes, P-18/INV-E03)
 └── C-025 DelegationGrant            (CH-15, nuevo — el token de autoridad delegada, scoped/
                                       time-bounded/auditable, P-21/INV-E06)

Components (registry/components.yaml)
 ├── CMP-001..CMP-012  (sin cambios — CH-01..CH-14)
 └── CMP-013 AgentCommunicationGateway  (CH-15, nuevo — segundo componente de este registry que no
                                         corresponde a ninguno de los once nombres de Article III;
                                         pertenece al Agent Interoperability Plane de Amendment v1.1)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado real `AgentCommunicationGateway → Protocol Adapter → Transport Adapter → destino`**:
  ningún componente invoca todavía `authorizeAgentCommunicationMessage` seguido de una entrega real
  hacia A2A u otro estándar — ese cableado, incluyendo qué componente adaptaría el protocolo y cuál
  el transporte, sigue siendo trabajo de un capítulo de integración futuro.
- **El mecanismo real detrás de `delegationScopeCoversMessage`**: primitiva asumida, sin modelar
  cómo se compara, concretamente, un `delegatedScope: List<Text>` contra el `content: Value` de un
  mensaje real.
- **Profundidad de delegación encadenada** (`INV-E06`, "delegation depth"): este capítulo verifica UN
  `DelegationGrant` contra UN mensaje; no modela qué pasa cuando un run delegado, a su vez, delega
  hacia un tercer run — ni cómo se acotaría esa cadena para que no crezca sin límite.
- **El consumo acumulado de `DelegationGrant.budget` a través de múltiples mensajes**: este capítulo
  verifica que el grant no haya expirado y que cubra el mensaje evaluado, pero no trackea cuánto de
  `budget` ya se consumió en mensajes anteriores bajo el mismo grant — ese trackeo, y su relación con
  `ExecutionController` (CH-07) evaluando el run delegado ya activado, queda para un capítulo futuro.
- **La emisión real de un `DelegationGrant`**: quién lo construye, con qué autoridad para delegar en
  primer lugar, y contra qué política se decide cuánto delegar — asumido, no modelado (mismo límite
  que CH-11 §15 documentó para `findAgentConfig`, o CH-14 §18 para `admissionRulesGrantAccess`).
- **Ausencia de evidencia de auditoría real** (`P-25`) para un `AgentCommunicationMessage`/
  `DelegationGrant`: señalado explícitamente como límite real, no silenciado (seccion 14).
- **El Execution Plane completo** (el segundo plano canónico, deliberadamente saltado por este
  capítulo) y **los seis planos restantes** de Amendment v1.1 (Capability & Integration, Data &
  Context, Control, Reliability, Observability & Governance, Execution Fabric) y sus componentes
  (`CredentialBroker`, y el resto): explícitamente fuera de alcance.
- **Ningún Protocol Adapter/Transport Adapter concreto** (A2A sobre HTTP, gRPC, un SDK real):
  infraestructura de borde, no modelada — mismo tratamiento que `Ingress Adapter` (CH-14).
- Reviewers plurales, evals y orquestación multi-agente propiamente dicha (más de dos agentes
  coordinándose): explícitamente fuera de alcance de BH-v0.1.

## 19. Siguiente Incremento (Next Increment)

Con este capítulo, el "Agent Interoperability Plane" de Amendment v1.1 tiene su primer componente
real — pero el plano completo (Protocol Adapter/Transport Adapter concretos, el cableado real hacia
`AgentCore`/`ExecutionController`, la profundidad de delegación encadenada) sigue sin construirse de
punta a punta. El problema natural del próximo incremento es, o bien profundizar este mismo plano, o
bien retroceder a cubrir el Execution Plane (el segundo plano canónico, deliberadamente saltado por
este capítulo), o bien avanzar hacia cualquiera de los seis planos restantes que Amendment v1.1
enumera junto a estos.

`next_chapter` queda en `null` en el frontmatter de este capítulo porque, en este momento del libro,
ese próximo capítulo todavía no existe como archivo — solo como el problema que motivaría su
escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg / Bucles
> de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows),
> secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): catorce capítulos reales construyeron un runtime completo
   más el primer componente de Enterprise, pero ninguno modeló qué pasa cuando un agente que ya está
   corriendo necesita comunicarse con otro — ni con un sub-agente interno, ni con un agente externo
   operado por un tercero.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): Amendment v1.1 nombra
   literalmente `AgentCommunicationGateway` desde que fue adoptada; CH-14 ya lo mencionó entre los
   componentes explícitamente diferidos, y `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §31 trae
   una regla editorial dedicada que este capítulo, por fin, satisface.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `AgentCommunicationGateway` con una ficha que declara tanto lo que posee (`owns`: adaptar
   mensajes semánticos vía adapters, desacoplar el core de cualquier protocolo/transporte, verificar
   el límite de delegación ya existente) como lo que explícitamente NO posee (admisión de un
   estímulo crudo, autorización de una acción ya resuelta, continuación de turno, el protocolo/
   transporte concreto en sí).
4. **Modelos mentales** (= §4, Constitutional Impact): "comunicación entre agentes" no es una sola
   pregunta — Amendment v1.1 la divide, con nombres propios, en delegación interna y federación
   externa, dos preguntas con la misma forma superficial pero dueños y riesgos distintos.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un sistema deja sin modelar la frontera de
  comunicación entre agentes, cualquier componente puede invocar directamente el SDK o el endpoint
  de otro agente, acoplando el core a un protocolo concreto — el mismo bucle que `P-02` (model
  replaceability) ya combatió para el modelo, ahora aplicado a otro agente.
- **Bucle de equilibrio (estabiliza):** `authorizeAgentCommunicationMessage` (§11) deja pasar sin
  fricción cualquier mensaje sin autoridad delegada de por medio, pero rechaza — nunca hereda en
  silencio — cualquier mensaje respaldado por un `DelegationGrant` ya expirado o fuera de scope.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `DelegationGrant.delegatedScope` sea siempre
una lista explícita y acotada, nunca un booleano de "toda la autoridad" — y que
`AgentCommunicationMessage.delegationGrantId` sea `Optional`, nunca obligatorio. Si
`DelegationGrant` representara "delega todo" en vez de un scope explícito, `AgentCommunicationGateway`
absorbería silenciosamente una autorización sin límites — la violación exacta que `P-21` prohíbe.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo de
> esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set` (frontmatter) y
> es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa, para lectura directa
> del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Cuando un agente que ya está corriendo necesita que otro agente haga algo en su nombre, ¿qué
   necesitaría existir para que esa comunicación nunca dependa de un SDK o protocolo concreto?
   *(cierra la pregunta guía 1)*
2. La decisión de si un estímulo externo crudo tiene derecho a arrancar un run ya tiene un dueño.
   ¿Esa misma pregunta sirve para decidir si dos runs ya en marcha pueden comunicarse? *(cierra la
   pregunta guía 2)*
3. Cuando un run le pide a otro que actúe en su nombre, ¿basta con confiar, o necesita existir algo
   escrito, con vencimiento explícito, que declare cuánta autoridad se transfiere? *(cierra la
   pregunta guía 3)*
4. Un presupuesto operacional acota una única ejecución. Cuando esa ejecución delega parte de su
   trabajo, ¿ese presupuesto se hereda sin límites nuevos, o necesita una forma más acotada? *(cierra
   la pregunta guía 4)*

### Explicar

1. `AgentCommunicationGateway` posee desacoplar la comunicación entre agentes de cualquier SDK/
   protocolo/transporte concreto. Explica, como si hablaras con alguien sin contexto técnico, por
   qué NO posee decidir si el estímulo que inició cualquiera de los dos runs tenía derecho a
   arrancar.
2. `AgentCommunicationMessage.delegationGrantId` es `Optional`, nunca obligatorio. Explica por qué
   exigir siempre un `DelegationGrant` inventaría una relación de delegación que no siempre existe.

### Conectar

1. `AdmissionController` (CH-14) decide si un estímulo crudo puede arrancar un run. Si un mensaje
   llegara desde un agente que nunca pasó por esa admisión, ¿es responsabilidad de
   `AgentCommunicationGateway`, o de una frontera anterior y distinta?
2. `ExecutionController` (CH-07) ya evalúa un `ExecutionBudget` contra UN run. ¿Alcanza con que
   evalúe también el presupuesto heredado por un run delegado, o el límite de la relación de
   delegación en sí necesita un dueño distinto?

### Espaciar

Las cinco tarjetas de repaso de este capítulo (dos sobre `AgentCommunicationGateway` — su `owns` y
su `does_not_own` —, una sobre `AgentCommunicationMessage`, una sobre `DelegationGrant`, y una sobre
la ausencia de `AgentEvent`) entran hoy en `reviewStage = DAY_1`. Repásalas de nuevo al día 3, al día
7 y al día 21 (curva de Ebbinghaus) — ver el apéndice de tarjetas al final del libro (edición PDF) o
`retrieval_set.flashcards` en `dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te equivocaste,
ese es precisamente el punto ciego que este método existe para revelar.
