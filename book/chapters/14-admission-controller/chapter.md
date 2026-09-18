---
id: CH-14
title: "AdmissionController y la Admisión de una Activación Cruda"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-012]
introduces_contracts: [C-022, C-023]
modifies_contracts: []
constitutional_articles: [P-16, P-17, P-25, INV-E01, INV-E02, INV-18, INV-19, INV-20]
previous_chapter: CH-13
next_chapter: CH-15
retrieval_set:
  expected_outcome:
    id: EO-CH14
    text: |
      Al terminar este capítulo podrás distinguir, para cualquier estímulo externo que intente
      activar un agente, qué validación le pertenece en exclusiva al componente que decide si esa
      activación cruda puede siquiera empezar a procesarse — antes de que exista un agentId
      resuelto, un AgentRun o una traza — y qué le pertenece a un componente vecino ya existente
      (validar un AgentConfig y nacer un AgentState, evaluar policy sobre una acción ya resuelta);
      y podrás diagnosticar, para cualquier AdmissionDecision producida, si su outcome refleja
      honestamente que ninguna activación tiene derecho inherente a ejecutar (Amendment v1.1,
      P-17) hasta que una regla de admisión real se lo conceda.
  skeleton:
    id: SK-CH14
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
    components_to_be_introduced: [CMP-012]
    contracts_to_be_introduced: [C-022, C-023]
  guiding_questions:
    - id: GQ-CH14-01
      text: |
        Todo estímulo externo (un prompt, un webhook, una cola, un evento de otro sistema) que
        podría disparar la activación de un agente llega, hasta ahora, sin que ningún componente
        de este libro decida primero si ese estímulo, en sí mismo, tiene siquiera derecho a
        intentar activar algo. ¿Qué necesitaría existir para que esa pregunta — antes de que se
        sepa qué agente concreto se está pidiendo — tenga, por fin, un dueño único?
      answered_by: RQ-CH14-01
    - id: GQ-CH14-02
      text: |
        El contrato que hace nacer un run ya conocido siempre parte de un identificador de agente
        ya resuelto y ya registrado. ¿Qué forma tendría un contrato que representa la misma
        intención de activarse pero ANTES de que exista ese identificador — y qué no podría exigir
        todavía, precisamente porque ese identificador no existe?
      answered_by: RQ-CH14-02
    - id: GQ-CH14-03
      text: |
        Un resultado de dos valores — nunca un booleano — ya se usó en este libro para decidir si
        una acción ya resuelta puede ocurrir. ¿Por qué esa misma forma de resultado, aplicada ahora
        a la pregunta de si una activación cruda puede siquiera empezar a procesarse, necesita un
        dueño distinto del que ya decide sobre acciones ya resueltas?
      answered_by: RQ-CH14-03
    - id: GQ-CH14-04
      text: |
        Cada evento observable que este libro produjo hasta ahora necesita, como mínimo, un run,
        una sesión y una traza a las que pertenecer. ¿Qué pasa cuando la decisión que se necesita
        observar ocurre antes de que cualquiera de esas tres cosas exista, y qué queda pendiente si
        esa decisión, honestamente, no puede producir ese mismo tipo de evento?
      answered_by: RQ-CH14-04
  systems_lens:
    iceberg_visible_fact: |
      Trece capítulos reales (CH-00..CH-13) construyeron un runtime completo — turnos, tools,
      modelo, contexto, policy, aprobación humana, presupuesto, capabilities, eventos, sesiones,
      identidad de agente — pero ninguno de ellos preguntó jamás si el estímulo que dispara todo
      eso, en sí mismo, tenía derecho a intentarlo. `AgentActivationRequest` (C-021, CH-11) ya
      asume un `agentId` conocido y registrado; `AgentCore.activateAgent` (CH-11 §15) documentó,
      sin resolverlo, que "ningún control de autorización sobre quién puede invocar activateAgent
      para un agentId ajeno" existía todavía (ver seccion 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite, ahora aplicado a la frontera misma de entrada del sistema, es que
      Amendment v1.1 nombra literalmente `ActivationRequest` y `AdmissionController` (P-16/P-17,
      `INV-E01`/`INV-E02`) desde que esa enmienda fue adoptada — y que CH-11 ya encontró ese nombre,
      lo distinguió con cuidado de su propio `AgentActivationRequest`, y lo dejó explícitamente
      diferido bajo el término de glosario "Ingress Activation". Este capítulo es el pago de esa
      deuda señalada, no una reapertura (ver seccion 3, Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala el duodécimo componente del registry — el primero que pertenece a
      Amendment v1.1 en vez de a los once nombres originales de Article III — con una ficha que
      declara tanto lo que posee (`owns`: cita literal de P-17) como lo que explícitamente NO posee
      (`does_not_own`: normalizar el estímulo crudo, rutear hacia un agente concreto, construir el
      AgentState real, evaluar policy sobre una acción ya en curso) y formaliza el primer par
      solicitud/decisión que opera enteramente ANTES de que exista un agentId resuelto (ver
      seccion 8, Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es que Article IV y `AgentActivationRequest`
      (CH-11) ya asumen, como mínimo, que alguien decidió que esta activación puede proceder con un
      `agentId` conocido — este capítulo muestra que hay una pregunta todavía más temprana: "¿puede
      esta activación, sin que se sepa aún ni siquiera a qué agente se refiere, empezar a
      procesarse?" (ver seccion 4, Impacto Constitucional).
    reinforcing_loop: |
      Cada vez que un sistema deja sin modelar la frontera de ingreso, cualquier estímulo externo
      puede alcanzar directamente `AgentCore.activateAgent` asumiendo, en silencio, que quien lo
      invoca ya está autorizado — exactamente el mismo bucle de "la ausencia de un dueño se vuelve
      una autorización implícita" que CH-05 (Default Deny) y CH-11 (validación de AgentConfig) ya
      combatieron puertas adentro del runtime, ahora en su borde exterior.
    balancing_loop: |
      `evaluateAdmissionForActivationRequest` (seccion 11) es el mecanismo de equilibrio: rechaza
      por defecto (`Default Reject`, fail-closed) en cuanto ninguna regla de admisión concede
      acceso, y nunca resuelve por su cuenta a qué agente concreto correspondería una activación
      admitida — se detiene exactamente en el límite de su propia pregunta.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `AdmissionDecision` (C-023) se
      correlacione de vuelta con `ActivationRequest` (C-022) únicamente por `requestId` — nunca
      resolviendo, inventando o adivinando un `AgentId` concreto. Si `AdmissionController`
      construyera ese `AgentId` por su cuenta "ya que de todos modos decide si la activación puede
      proceder", absorbería silenciosamente el ruteo (`P-17`: "before routing") y la activación real
      (`AgentCore`, CH-11) — dos decisiones que Article IV exige mantener separadas.
  recall_questions:
    - id: RQ-CH14-01
      text: |
        ¿Qué componente nuevo evalúa, antes de que exista ningún `AgentActivationRequest`, si un
        estímulo externo ya normalizado puede siquiera proceder — y qué ocho dimensiones
        (Amendment v1.1, `P-17`) agrupa esa evaluación bajo un único resultado?
    - id: RQ-CH14-02
      text: |
        ¿Qué campos tiene `ActivationRequest` (C-022), y por qué NO tiene un campo `agentId` — a
        diferencia de `AgentActivationRequest` (C-021, CH-11)?
    - id: RQ-CH14-03
      text: |
        ¿Qué outcome de `AdmissionDecision` (C-023) corresponde al default fail-closed de este
        capítulo, y qué campo la correlaciona de vuelta con el `ActivationRequest` que evaluó, sin
        resolver nunca un `AgentId` concreto?
    - id: RQ-CH14-04
      text: |
        ¿Por qué `AdmissionController` nunca construye un `AgentEvent` (C-010), y qué cuatro campos
        obligatorios de ese `STRUCT` son, literalmente, imposibles de poblar en el instante en que
        se evalúa una admisión?
  explain_prompts:
    - id: EP-CH14-01
      text: |
        `AdmissionController` posee aplicar identity, authorization, tenant, capacity, rate,
        budget, deduplication y policy decisions antes de rutear una activación (`P-17`, cita
        literal). Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee
        resolver a qué `AgentId` concreto corresponde esa activación una vez admitida — ¿qué se
        rompería si, ya que de todos modos decide si la activación puede proceder, también decidiera
        hacia dónde debe ir?
      target_entity: CMP-012
    - id: EP-CH14-02
      text: |
        `ActivationRequest` (C-022) no tiene ningún campo `agentId`, a diferencia de
        `AgentActivationRequest` (C-021, CH-11), que lo exige siempre. Explica por qué esa ausencia
        es, precisamente, la que hace posible que `AdmissionController` exista como un componente
        distinto de `AgentCore`, y qué se perdería si `ActivationRequest` exigiera un `agentId` ya
        resuelto.
      target_entity: C-022
  interleaved_questions:
    - id: IQ-CH14-01
      text: |
        `AgentCore.activateAgent` (CH-11) ya valida que un `AgentConfig` exista y que su
        `ExecutionBudget` sea coherente antes de producir el primer `AgentState` — pero su propia
        seccion 15 documentó, sin resolverlo, que "ningún control de autorización sobre quién puede
        invocar activateAgent para un agentId ajeno" existía todavía. Si una `AdmissionDecision` con
        `outcome = ADMIT` llegara, en una integración futura, justo antes de `activateAgent`,
        ¿cerraría eso el hueco que CH-11 dejó abierto, o simplemente lo movería a una pregunta
        distinta y todavía sin dueño — la de quién resuelve qué `AgentId` concreto le corresponde a
        un `externalIdentityRef` ya admitido?
      current_chapter_entities: [CMP-012, C-022, C-023]
      prior_chapter_entities: [CMP-011, C-021]
      prior_chapter: CH-11
    - id: IQ-CH14-02
      text: |
        `PolicyEngine.evaluatePolicyForToolCall` (CH-05) ya produce un outcome de tres valores
        (nunca un Boolean) evaluando si una acción ya resuelta puede ocurrir, con `Default Deny`
        como su fail-closed. `AdmissionController` produce un outcome de dos valores evaluando si
        una activación cruda puede siquiera empezar a procesarse, con el mismo espíritu fail-closed.
        ¿Por qué no basta con que `PolicyEngine` evalúe también las `ActivationRequest`, y qué se
        perdería de Decision Ownership (Article IV) si una sola función decidiera tanto "puede esta
        activación empezar" como "puede esta acción ya resuelta ejecutarse"?
      current_chapter_entities: [CMP-012, C-023]
      prior_chapter_entities: [CMP-005, C-014]
      prior_chapter: CH-05
  flashcards:
    - id: FC-CH14-01
      front: |
        ¿Qué posee `AdmissionController`, citando `P-17` literalmente?
      back: |
        Aplicar identity, authorization, tenant, capacity, rate, budget, deduplication y policy
        decisions sobre un `ActivationRequest` ya normalizado, antes de rutear la activación hacia
        cualquier destino — decidiendo únicamente un outcome `ADMIT`/`REJECT`, nunca a qué `AgentId`
        concreto corresponde ni cómo nace el `AgentState` resultante.
      source_entity: CMP-012
      chapter_introduced_in: CH-14
      review_stage: DAY_1
    - id: FC-CH14-02
      front: |
        ¿Qué NO posee `AdmissionController`?
      back: |
        Normalizar el estímulo externo crudo en un `ActivationRequest` (Ingress Adapter,
        infraestructura de borde, `P-16`); resolver o rutear hacia un `AgentId`/`AgentConfig`
        concreto (routing, todavía sin componente propio); construir el `AgentState`/
        `AgentActivationRequest` real de un agente (`AgentCore`, CMP-011, CH-11); evaluar policy
        sobre una `ToolCall` ya en curso (`PolicyEngine`, CMP-005, CH-05) — cuatro fronteras
        distintas, cada una con su propio dueño.
      source_entity: CMP-012
      chapter_introduced_in: CH-14
      review_stage: DAY_1
    - id: FC-CH14-03
      front: |
        ¿Qué campos tiene `ActivationRequest` (C-022), y por qué no tiene `agentId`?
      back: |
        `id` (`ActivationRequestId`), `sourceRef` (`Text`, referencia opaca al ingress adapter/canal
        — nunca modela cada canal individualmente), `externalIdentityRef` (`Text`, una identidad o
        tenant externo todavía sin autorizar), `payload` (`Value`) y `receivedAt` (`Timestamp`). No
        tiene `agentId` porque ese identificador solo existe después de que algo — todavía sin
        componente en este libro — resuelva a qué agente concreto corresponde esta activación;
        exigirlo aquí asumiría una resolución que `P-17` coloca explícitamente después de la
        admisión ("before routing").
      source_entity: C-022
      chapter_introduced_in: CH-14
      review_stage: DAY_1
    - id: FC-CH14-04
      front: |
        ¿Qué campos tiene `AdmissionDecision` (C-023), y qué dos valores puede tomar su outcome?
      back: |
        `requestId` (`ActivationRequestId`, correlaciona de vuelta con el `ActivationRequest`
        evaluado), `outcome` (`AdmissionOutcome`: `ADMIT` o `REJECT`, nunca un Boolean), `reason`
        (`Optional<HarnessError>`, poblado solo cuando `REJECT`) y `decidedAt` (`Timestamp`). Nunca
        incluye un `AgentId`: "lo que permite continuar" cuando `ADMIT` es, únicamente, el
        `requestId` — resolver hacia qué agente concreto queda para una integración futura.
      source_entity: C-023
      chapter_introduced_in: CH-14
      review_stage: DAY_1
    - id: FC-CH14-05
      front: |
        ¿Por qué `AdmissionController` es el primer componente del libro cuya función principal
        nunca construye un `AgentEvent`?
      back: |
        `AgentEvent` (C-010) exige `runId`, `sessionId`, `agentId` y `traceId` como campos
        obligatorios — los cuatro describen un `AgentRun` que, en el instante de una admisión,
        todavía no existe (ni siquiera hay un `agentId` resuelto). `EventBus` (CH-09) tampoco
        producía `AgentEvent`, pero porque no decide nada; `AdmissionController` sí decide algo,
        un paso antes de que existan los datos mínimos que ese `STRUCT` exige para describir a qué
        pertenece la decisión.
      source_entity: CMP-012
      chapter_introduced_in: CH-14
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH14-01
      recall_question: RQ-CH14-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH14-02
      recall_question: RQ-CH14-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH14-03
      recall_question: RQ-CH14-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH14-04
      recall_question: RQ-CH14-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 14 — AdmissionController y la Admisión de una Activación Cruda

> **Regla constitucional (Amendment v1.1, `P-17`):** "No activation has an inherent right to
> execute. `AdmissionController` MUST apply identity, authorization, tenant, capacity, rate,
> budget, deduplication and policy decisions before routing."

Con este capítulo se abre una parte nueva del libro. CH-00..CH-13 construyeron, completos, los
once componentes de runtime de Article III y demostraron, con dos capítulos de integración, tanto
su camino feliz como sus tres caminos de gobierno — BH-v0.1 quedó cerrado como incremento. Este
capítulo entra, por primera vez, al territorio de **Amendment v1.1 — Enterprise Activation,
Interoperability and Operations** (`P-16`..`P-30`, `INV-E01`..`INV-E14`, "Canonical Enterprise
Planes"): un cuerpo normativo que **extiende**, sin invalidar, los Article I-XII originales
(Amendment v1.1, línea de apertura: "This amendment is normative and extends the original
Constitution without invalidating P-01 through P-15"). De los nueve "Canonical Enterprise Planes"
que Amendment v1.1 enumera, este capítulo cubre exclusivamente el primero — **Ingress & Activation
Plane** — y, dentro de él, exclusivamente su primer componente: `AdmissionController`. Los ocho
planes restantes (Execution, Agent Interoperability, Capability & Integration, Data & Context,
Control, Reliability, Observability & Governance, Execution Fabric) quedan, deliberadamente, para
capítulos futuros.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de saber
> cómo se llama el componente de este capítulo. El detalle estructurado de esta sección vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, para cualquier estímulo
externo que intente activar un agente, qué validación le pertenece en exclusiva al componente que
decide si esa activación cruda puede siquiera empezar a procesarse — antes de que exista un
`agentId` resuelto, un `AgentRun` o una traza — y qué le pertenece a un componente vecino ya
existente (validar un `AgentConfig` y hacer nacer un `AgentState`, evaluar policy sobre una acción
ya resuelta); y podrás diagnosticar, para cualquier `AdmissionDecision` producida, si su `outcome`
refleja honestamente que ninguna activación tiene derecho inherente a ejecutar (Amendment v1.1,
`P-17`) hasta que una regla de admisión real se lo conceda.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e
introduce dos contratos de datos nuevos y el primer componente de este libro que pertenece a
Amendment v1.1 en vez de a los once nombres originales de Article III — todavía sin explicarlos,
solo como mapa.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar
atrás; están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este
capítulo va a definir):

1. Todo estímulo externo (un prompt, un webhook, una cola, un evento de otro sistema) que podría
   disparar la activación de un agente llega, hasta ahora, sin que ningún componente de este libro
   decida primero si ese estímulo, en sí mismo, tiene siquiera derecho a intentar activar algo.
   ¿Qué necesitaría existir para que esa pregunta — antes de que se sepa qué agente concreto se
   está pidiendo — tenga, por fin, un dueño único?
2. El contrato que hace nacer un run ya conocido siempre parte de un identificador de agente ya
   resuelto y ya registrado. ¿Qué forma tendría un contrato que representa la misma intención de
   activarse pero ANTES de que exista ese identificador — y qué no podría exigir todavía,
   precisamente porque ese identificador no existe?
3. Un resultado de dos valores — nunca un booleano — ya se usó en este libro para decidir si una
   acción ya resuelta puede ocurrir. ¿Por qué esa misma forma de resultado, aplicada ahora a la
   pregunta de si una activación cruda puede siquiera empezar a procesarse, necesita un dueño
   distinto del que ya decide sobre acciones ya resueltas?
4. Cada evento observable que este libro produjo hasta ahora necesita, como mínimo, un run, una
   sesión y una traza a las que pertenecer. ¿Qué pasa cuando la decisión que se necesita observar
   ocurre antes de que cualquiera de esas tres cosas exista, y qué queda pendiente si esa decisión,
   honestamente, no puede producir ese mismo tipo de evento?

## 1. Arquitectura Actual (Current Architecture)

CH-00..CH-13 dejaron instalados veintiún contratos de datos y once componentes de runtime — los
once nombres completos de Article III ("Agent Runtime"), cada uno con ficha real, más dos
capítulos de integración que recorrieron un `AgentRun` completo tanto en su camino feliz (CH-12)
como en sus tres caminos de gobierno (CH-13). Todo ese runtime, sin embargo, comparte una premisa
que ningún capítulo cuestionó nunca: que alguien, en algún punto anterior a `AgentCore.
activateAgent` (CH-11), ya decidió que esta activación concreta puede proceder.

`AgentActivationRequest` (C-021, CH-11) — el contrato que hace posible, por primera vez en el
libro, mostrar cómo nace un `AgentState` — declara `agentId: AgentId` como su primer campo, sin
`Optional`: un identificador **ya resuelto**, referenciando un `AgentConfig` **ya registrado**.
CH-11 §6 fue explícito sobre esto: `AgentActivationRequest` "parte SIEMPRE de un `agentId` ya
conocido y un `AgentConfig` ya registrado — el tramo que ocurre, en el mejor de los casos,
**después** de que un `AdmissionController` (si existiera) ya admitió el estímulo". Y CH-11 §15
fue igual de explícito sobre lo que faltaba: "Ningún control de autorización sobre quién puede
invocar `activateAgent` para un `agentId` ajeno — `findAgentConfig` acepta cualquier `agentId` que
reciba, sin verificar que quien invoca tenga permiso sobre ese agente."

Amendment v1.1 ya nombra, literalmente, las dos piezas que cerrarían ese hueco — desde la primera
versión de esta enmienda adoptada por el repositorio, antes de que este capítulo existiera:

- `P-16` ("Activation is independent from execution"): "External stimuli MUST be normalized into
  an `ActivationRequest` before entering the execution core. User prompts, APIs, webhooks, queues,
  schedules, events, files, databases, systems and other agents are ingress mechanisms — not
  `AgentLoop` concerns."
- `P-17` ("Admission precedes execution"): "No activation has an inherent right to execute.
  `AdmissionController` MUST apply identity, authorization, tenant, capacity, rate, budget,
  deduplication and policy decisions before routing."
- `INV-E01`: "No ingress adapter calls `AgentLoop` directly; it produces an `ActivationRequest`."
- `INV-E02`: "No `ActivationRequest` executes without an `AdmissionDecision`."

CH-11 encontró estos cuatro artículos durante su propia lectura completa de la Constitution,
documentó la distinción con cuidado (glosario: "Ingress Activation"), y los dejó, deliberadamente,
fuera de su propio alcance — "el 'Ingress & Activation Plane' completo de Amendment v1.1... fuera
de alcance de BH-v0.1" (CH-11 §18). Este capítulo es, precisamente, el que cierra esa deuda ya
señalada — no la reabre, la resuelve.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas para esto, la pregunta "¿puede este estímulo externo,
que todavía no sabe a qué agente se refiere en los términos que el runtime entiende, siquiera
empezar a procesarse?" no tiene ningún lugar fijo donde vivir. Una implementación puede saltarse
la pregunta por completo y dejar que cualquier prompt, webhook, evento de cola o llamada de API
alcance directamente `AgentCore.activateAgent` (CH-11), asumiendo en silencio que quien lo invocó
ya estaba autorizado — exactamente el vacío que CH-11 §15 documentó sin resolver.

Hay una segunda dimensión del mismo problema, más conceptual que operativa. `AgentActivationRequest`
(C-021, CH-11) modela, con precisión, la intención de activar un run de un agente **ya conocido** —
pero ningún contrato de este libro representa, todavía, el estímulo externo **antes** de que se
sepa a qué agente se refiere: quién lo envió (en los términos crudos con los que llegó, no en los
términos que el runtime ya entiende), qué está pidiendo, y cuándo llegó. `P-17` es explícito sobre
por qué esa representación no puede saltarse directamente a una decisión de ejecución: "no
activation has an inherent right to execute" — ni siquiera una que ya trae un `agentId` reconocible
a simple vista.

Necesitamos que "¿puede esta activación cruda proceder, antes de que exista siquiera un `agentId`
resuelto?" tenga, por fin, un dueño único y nombrado — que reciba el estímulo ya normalizado (nunca
el estímulo crudo en sí: eso pertenece, per `P-16`, a un ingress adapter que no es responsabilidad
de este runtime), que aplique identidad, autorización, tenant, capacidad, rate, presupuesto,
deduplicación y policy (`P-17`), que produzca un resultado de dos valores — nunca un Boolean —, y
que se detenga ahí, sin resolver a qué agente concreto correspondería una activación admitida ni
construir el `AgentState`/`AgentActivationRequest` real de ese agente.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los veintiún contratos y los once componentes que existen hasta este punto no bastan porque:

- `P-16`/`P-17`/`INV-E01`/`INV-E02` citan literalmente, desde que Amendment v1.1 fue adoptada,
  `ActivationRequest` y `AdmissionController` — dos nombres que ningún capítulo había materializado
  con código real; CH-11 ya los encontró y los distinguió con cuidado de `AgentActivationRequest`
  (C-021), pero explícitamente los dejó fuera de su propio alcance;
- `AgentActivationRequest` (C-021, CH-11) exige `agentId: AgentId` sin `Optional` — ningún
  contrato de este libro representa, todavía, un estímulo de activación **antes** de que ese
  identificador exista;
- `AgentCore.activateAgent` (CH-11 §11) valida que un `AgentConfig` exista y que su
  `ExecutionBudget` sea coherente — pero nunca valida identidad, autorización, tenant, capacidad,
  rate, presupuesto de ingreso o deduplicación sobre quién está solicitando esa activación; CH-11
  §15 documentó esa ausencia explícitamente, sin resolverla;
- `PolicyEngine.evaluatePolicyForToolCall` (CH-05) ya decide, con un outcome de tres valores, si
  una acción **ya resuelta** puede ocurrir — pero nunca evaluó, ni podría evaluar sin invadir
  Decision Ownership, si una activación **todavía sin agente resuelto** puede siquiera empezar a
  procesarse: son preguntas de dominios distintos, formuladas sobre material de entrada distinto
  (un `ToolCall` ya resuelto contra un `ActivationRequest` crudo);
- ningún componente de este libro, hasta ahora, produce un resultado analogable a `PolicyDecision`
  o `ExecutionDecision` — un `outcome` de al menos dos valores, nunca un Boolean, con una razón
  trazable — para la pregunta específica de admisión de una activación.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la
> secuencia `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una
> entidad que no haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT`
> registrado — **no magic entities**. Este capítulo aplica la misma disciplina que CH-00..CH-13 ya
> establecieron, con una particularidad nueva: por primera vez, el componente que se introduce no
> corresponde a ninguno de los once nombres del árbol de Article III ("Agent Runtime") — su
> `owns` se ancla, en cambio, en la cita literal de un principio de Amendment v1.1 (`P-17`), no en
> una sección propia de Article III (que Amendment v1.1 no reescribe).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-16   Activation is independent from execution.
           ActivationRequest (seccion 6/7) es, por primera vez, un contrato real que representa el
           estímulo externo YA normalizado — sin que ningún ingress adapter concreto (webhook,
           cola, cron, API) se modele dentro de este registry (permanece infraestructura de borde,
           citado literalmente: "ingress mechanisms — not AgentLoop concerns").
    P-17   Admission precedes execution.
           evaluateAdmissionForActivationRequest (seccion 11) es la primera formalización
           ejecutable de "ninguna activación tiene derecho inherente a ejecutar" — un ActivationRequest
           nunca alcanza AgentCore.activateAgent (CH-11) sin que este capítulo produzca primero un
           AdmissionDecision con outcome = ADMIT.
    P-25   Audit evidence is distinct from operational telemetry.
           Este capítulo documenta explícitamente (seccion 14/18) que AdmissionDecision NO produce
           ningún AgentEvent — la evidencia de una decisión de admisión, si llegara a auditarse,
           necesitaría un mecanismo distinto de EventBus/AgentEvent (Article X), que este capítulo
           no construye.

Invariants preserved
    INV-E01   No ingress adapter calls AgentLoop directly; it produces an ActivationRequest.
              Cita literal por primera vez con un contrato real: ActivationRequest (C-022) es,
              precisamente, lo que un ingress adapter produciría — este capítulo no modela ningún
              ingress adapter concreto, solo lo que recibiría de él.
    INV-E02   No ActivationRequest executes without an AdmissionDecision.
              evaluateAdmissionForActivationRequest (seccion 11) es la única función de este
              capítulo, y produce siempre un AdmissionDecision — nunca deja pasar un
              ActivationRequest sin evaluarlo.
    INV-18    Toda acción significativa produce un evento observable.
              Tensión real, documentada sin resolver (seccion 14): AdmissionController es el primer
              componente del libro cuya función principal nunca construye un AgentEvent — los
              cuatro campos obligatorios de ese STRUCT (runId, sessionId, agentId, traceId)
              describen un AgentRun que, en el instante de una admisión, todavía no existe.
    INV-19    Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy
              relevante.
              AdmissionDecision.requestId correlaciona la decisión de vuelta con el
              ActivationRequest que la motivó — el ancla de trazabilidad disponible antes de que
              exista ningún TraceId real (que AgentCore, CH-11, solo mina después de la admisión).
    INV-20    Todo error operacional pertenece a una categoría conocida.
              El único fallo real de este capítulo (seccion 13) introduce ADMISSION, una categoría
              nueva de ErrorCategory — ninguna de las once ya existentes representa, sin
              conflación, el rechazo de una activación cruda.

Component ownership changes
    CMP-012 AdmissionController se introduce — registry/components.yaml pasa de 11 a 12
    componentes. Es el primer componente de este registry que NO corresponde a ninguno de los once
    nombres del árbol de Article III ("Agent Runtime") — su owns se ancla en la cita literal de
    P-17 (Amendment v1.1), no en una sección propia de Article III, que esta enmienda no reescribe.
    registry/components.yaml de CMP-011 (AgentCore) y CMP-005 (PolicyEngine) NO se modifica: ninguno
    cablea todavía su relación real con AdmissionController (ver seccion 9/18).

Lifecycle changes
    Ninguna modificación a AgentRunStatus (C-013): este capítulo no construye, ni transiciona,
    ningún AgentState. Su decisión ocurre un paso ANTES de la primera transición de Article V
    (CREATED, CH-11) — ni siquiera existe todavía un agentId resuelto sobre el cual esa primera
    transición pudiera aplicarse.

Security implications
    AdmissionController es el primer componente de este libro cuya responsabilidad completa es de
    seguridad perimetral (identity/authorization/tenant/capacity/rate/budget/deduplication/policy,
    P-17) — nunca autorización de una acción ya resuelta (P-13 sigue siendo exclusivo de
    PolicyEngine, CH-05) ni ruteo hacia un agente concreto. Ver seccion 15 para el análisis
    completo, incluyendo la distinción explícita frente a PolicyEngine y AgentCore.

Observability implications
    Primer componente real del libro cuya función principal nunca produce un AgentEvent (C-010) —
    ni EventBus (CH-09, que tampoco lo produce, pero porque no decide nada). Ver seccion 14 para el
    hallazgo real y su relación con P-25.

Deterministic vs agentic boundary
    Article XII se refina una duodécima vez a nivel de componente: AdmissionController, igual que
    AgentCore (CH-11) y EventBus (CH-09), no consume ninguna salida del modelo ni directa ni
    indirectamente. Su frontera determinística separa un estímulo ya normalizado (ActivationRequest,
    con una identidad externa todavía sin autorizar) del primer resultado determinístico —
    ADMIT/REJECT — que decide si ese estímulo puede siquiera aspirar a convertirse, algún día, en
    una ejecución.
```

## 5. Conceptos Nuevos (New Concepts)

- **Ingress Adapter**: la pieza de infraestructura de borde (un webhook handler, un consumidor de
  cola, un disparador de cron, un endpoint de API) que normaliza un estímulo externo crudo hacia un
  `ActivationRequest`, per `P-16` ("User prompts, APIs, webhooks, queues, schedules, events, files,
  databases, systems and other agents are ingress mechanisms"). Nunca un componente propio de este
  registry — mismo tratamiento que `Channel Adapter` (CH-06): infraestructura de borde, citada por
  nombre, nunca modelada en detalle dentro del runtime.
- **Admission**: la decisión de si un `ActivationRequest` ya normalizado puede proceder — evaluando
  identidad, autorización, tenant, capacidad, rate, presupuesto, deduplicación y policy (`P-17`) —
  antes de que exista cualquier ruteo hacia un agente concreto o cualquier intento de activación
  real. Responsabilidad exclusiva de `AdmissionController`.
- **Default Reject (Admission Fail-Closed)**: la regla de diseño, análoga a `Default Deny`
  (`PolicyEngine`, CH-05) pero aplicada un paso antes en la cadena, por la cual
  `evaluateAdmissionForActivationRequest` responde con `outcome = REJECT` en cuanto ninguna regla
  de admisión conocida concede acceso — la ausencia de una regla que admita nunca se interpreta
  como admisión implícita.
- **Routing (Amendment v1.1, concepto vecino, no introducido en este capítulo)**: la decisión,
  todavía sin componente propio en este registry, de a qué `AgentId`/`AgentConfig` concreto
  corresponde un `ActivationRequest` ya admitido. `P-17` la coloca explícitamente **después** de la
  admisión ("...decisions **before routing**"): `AdmissionController` nunca la resuelve — decide
  únicamente si la activación puede proceder, nunca hacia dónde.
- **Decision Ownership** *(Article IV, en uso desde CH-01, ahora aplicado por primera vez a un
  componente de Amendment v1.1)*: `AdmissionController` decide "¿puede esta activación cruda
  proceder?"; explícitamente NO decide "¿a qué agente concreto corresponde?" (Routing, sin dueño
  todavía), "¿cómo nace el `AgentState` de ese agente?" (`AgentCore`, ya resuelto en CH-11) ni
  "¿puede esta acción ya resuelta ejecutarse?" (`PolicyEngine`, ya resuelto en CH-05). Si Article IV
  extendiera su tabla para Amendment v1.1 (la Constitution, tal como este libro la recibe, no lo
  hace todavía), la fila de `AdmissionController` leería: "May this activation be admitted before
  routing?" — documentado aquí en prosa, nunca como una edición al archivo fuente de la
  Constitution.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados de CH-00/CH-11

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `AgentId`, `Timestamp`, `Value`, `HarnessError`.

### Un identificador opaco nuevo

Siguiendo el mismo patrón que CH-00 §6 estableció para los identificadores fundamentales
(`AgentId`, `MessageId`, ...): un tipo opaco, sin campos propios, usado como tipo de campo en los
`STRUCT` de esta sección.

| Identificador (nuevo de este capítulo) | Identifica |
|---|---|
| `ActivationRequestId` | un `ActivationRequest` concreto — el estímulo externo ya normalizado que este capítulo evalúa |

### `ErrorCategory` — extendido, sin redefinir `HarnessError`

Este es el tercer capítulo que agrega un valor a `ErrorCategory` desde que CH-00 lo declaró (CH-06
agregó `HUMAN_INTERACTION`): el valor `ADMISSION`, necesario porque ninguna de las once categorías
ya existentes representa, sin conflación, el rechazo de una activación cruda — `POLICY` pertenece,
en exclusiva, a la pregunta de `PolicyEngine` sobre una acción **ya resuelta** (CH-05), y
reutilizarla aquí confundiría dos decisiones de dominios distintos:

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
END
```

`HarnessError` (C-011) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — mismo patrón
exacto que la extensión de CH-06, aplicado aquí por segunda vez a `ErrorCategory`.

### `AdmissionOutcome` — el resultado de dos estados de una admisión

```pseudocode
ENUM AdmissionOutcome
    ADMIT
    REJECT
END
```

Dos valores, deliberadamente, nunca un `Boolean` — el mismo argumento que motivó `PolicyOutcome`
(CH-05, tres valores) y `ExecutionOutcome` (CH-07, tres valores): un resultado con nombre propio
deja espacio para que una versión futura de este contrato agregue un tercer valor (por ejemplo, una
admisión condicional o diferida) sin romper la forma del contrato — algo que un `Boolean` no
podría absorber nunca. `AdmissionOutcome` vive embebido dentro de `AdmissionDecision`, sin contrato
`C-XXX` propio — el mismo patrón que `PolicyOutcome` (CH-05) o `ExecutionOutcome` (CH-07).

### `ActivationRequest` — el estímulo externo ya normalizado

```pseudocode
STRUCT ActivationRequest
    id: ActivationRequestId
    sourceRef: Text
    externalIdentityRef: Text
    payload: Value
    receivedAt: Timestamp
END
```

Cinco campos, cada uno respondiendo a una parte exacta del alcance decidido para este capítulo:
`id` identifica esta solicitud de forma estable, para que una `AdmissionDecision` pueda
correlacionarse de vuelta con ella; `sourceRef` es una referencia opaca al ingress adapter/canal
que produjo esta activación (un webhook, una cola, un cron, una API) — **nunca modela cada canal
individualmente**, mismo tratamiento que `Channel Adapter` (CH-06) recibió para el lado de la
resolución humana; `externalIdentityRef` es una referencia opaca a la identidad o tenant externo
que reclama esta activación — **todavía sin autorizar**: es, literalmente, el material crudo sobre
el que `P-17` exige aplicar identity/authorization/tenant antes de que nada más ocurra;
`payload` es el estímulo/objetivo crudo que se está pidiendo (tipado como `Value`, el mismo
primitivo genérico que `AgentActivationRequest.input`, C-021, CH-11, ya usa); `receivedAt` registra
cuándo el ingress adapter recibió el estímulo.

**Por qué no tiene ningún campo `agentId`.** `AgentActivationRequest` (C-021, CH-11) exige
`agentId: AgentId` como su primer campo, sin `Optional` — porque parte, siempre, de un agente ya
conocido y ya registrado. `ActivationRequest` (este capítulo) representa el tramo **anterior**: un
estímulo que todavía no sabe, en los términos que el runtime entiende, a qué agente se refiere.
Agregarle un `agentId` aquí adelantaría, dentro del propio contrato, una resolución (routing) que
`P-17` coloca explícitamente **después** de la admisión ("...decisions **before routing**") — y que
este libro, deliberadamente, no modela todavía (seccion 5, "Routing"; seccion 18).

**Por qué el nombre es `ActivationRequest`, y no otro.** A diferencia de `AgentActivationRequest`
(C-021, CH-11) — un nombre acuñado por ese capítulo precisamente para NO colisionar con el término
que Amendment v1.1 ya usaba —, este contrato sí adopta el nombre corto y literal que `P-16` cita:
"External stimuli MUST be normalized into an `ActivationRequest`". CH-11 ya reservó, en prosa, este
significado exacto para el término (glosario: "Ingress Activation"); este capítulo es el primero en
darle, por fin, forma de `STRUCT` real.

### `AdmissionDecision` — el resultado de evaluar una admisión

```pseudocode
STRUCT AdmissionDecision
    requestId: ActivationRequestId
    outcome: AdmissionOutcome
    reason: Optional<HarnessError>
    decidedAt: Timestamp
END
```

`requestId` correlaciona esta decisión con el `ActivationRequest` que la motivó — mismo patrón de
correlación que `PolicyDecision.callId` (CH-05) o `HumanInteractionResolution.requestId` (CH-06).
`outcome` es el resultado de dos valores de la seccion anterior. `reason` es
`Optional<HarnessError>`, poblado **únicamente** cuando `outcome = REJECT` — la misma asimetría de
diseño que `PolicyDecision.reason` (CH-05). `decidedAt` registra cuándo se evaluó.

**Lo que este contrato deliberadamente NO tiene, y por qué.** Ningún campo `agentId` ni ninguna
referencia a un `AgentConfig`/`AgentActivationRequest` concreto: cuando `outcome = ADMIT`, "lo que
permite continuar" es, únicamente, el propio `requestId` — la referencia hacia el
`ActivationRequest` ya admitido, que una integración futura combinaría con un mecanismo de routing
(todavía sin componente propio) para recién entonces construir un `AgentActivationRequest` (C-021,
CH-11) real. Que `AdmissionDecision` no resuelva ese `agentId` por su cuenta es, precisamente, lo
que mantiene la admisión y el ruteo/la activación como tres decisiones separadas y con dueños
distintos (seccion 8/15).

**Unchanged / Not yet introduced**: `HarnessError` (C-011) no cambia de forma — este capítulo lo
consume, nunca lo modifica. Ningún `ENUM AdmissionStatus` propio: a diferencia de
`HumanInteractionRequest` (CH-06), una `ActivationRequest` no persiste como una entidad con
lifecycle propio — se evalúa una única vez, de forma síncrona, y su resultado es directamente un
`AdmissionDecision` (mismo patrón que `AgentActivationRequest`, CH-11, seccion 6).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce dos contratos
de datos, registrados en `registry/contracts.yaml`:

```text
ID:                     C-022
Name:                   ActivationRequest
Version:                v1
Introduced In:          CH-14
Current Definition:     STRUCT ActivationRequest (ver §6)
Used By:                [CMP-012]
Modified By:            []
Constitutional Impact:  [P-16, INV-E01]
```

```text
ID:                     C-023
Name:                   AdmissionDecision
Version:                v1
Introduced In:          CH-14
Current Definition:     STRUCT AdmissionDecision (ver §6)
Used By:                [CMP-012]
Modified By:            []
Constitutional Impact:  [P-17, INV-E02, INV-19, INV-20]
```

`C-022` y `C-023` son el noveno y el décimo id que este libro asigna sin que estuvieran reservados
desde CH-01 §7 — el correlativo simplemente continúa después de `C-021` (CH-11). A diferencia de
`AgentActivationRequest` (C-021), que CH-11 acuñó deliberadamente para no colisionar con el término
de Amendment v1.1, `ActivationRequest` (C-022) sí adopta, por fin, el nombre corto que `P-16` cita
literalmente desde que esa enmienda fue adoptada.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el primer componente del registry que no corresponde a ninguno de los once
nombres del árbol de Article III ("Agent Runtime") — pertenece, en cambio, al "Ingress & Activation
Plane" de Amendment v1.1:

```pseudocode
COMPONENT AdmissionController
    consumes: ActivationRequest
    produces: AdmissionDecision, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Amendment v1.1 (`P-17`) — Article III no tiene, todavía,
una sección propia para este componente, porque Amendment v1.1 extiende la Constitution sin
reescribir Article III:

```text
COMPONENT: AdmissionController

Responsibility:
    Aplicar identity, authorization, tenant, capacity, rate, budget, deduplication y policy
    decisions sobre un ActivationRequest ya normalizado, antes de que cualquier ruteo hacia un
    agente concreto sea siquiera posible — produciendo un AdmissionDecision determinístico de dos
    resultados posibles (ADMIT/REJECT, nunca un Boolean) — sin decidir a qué agente concreto
    corresponde la activación, sin construir ningún AgentState y sin evaluar policy sobre ninguna
    acción ya resuelta.

Consumes:
    C-022 ActivationRequest

Depends on:
    (ninguno todavía — el cableado real hacia un mecanismo de routing y hacia AgentCore es
    Preview, no introducido en este capítulo; ver seccion 9)

Produces:
    C-023 AdmissionDecision, C-011 HarnessError

Owns (Amendment v1.1, P-17, cita literal):
    - "apply identity, authorization, tenant, capacity, rate, budget, deduplication and policy
      decisions before routing" (cita literal)
    - decidir, con un outcome de dos valores (ADMIT/REJECT), si un ActivationRequest ya normalizado
      puede proceder
    - rechazar por defecto (fail-closed) cuando ninguna regla de admisión concede acceso
      (Default Reject)
    - correlacionar cada AdmissionDecision de vuelta con el ActivationRequest que la motivó
      (requestId)

Does NOT own:
    - normalizar el estímulo externo crudo en un ActivationRequest (Ingress Adapter —
      infraestructura de borde, P-16, "ingress mechanisms — not AgentLoop concerns"; tampoco un
      concern de AdmissionController, que recibe el estímulo YA normalizado)
    - resolver o rutear una activación admitida hacia un AgentId/AgentConfig concreto (Routing,
      Amendment v1.1 — P-17 la coloca explícitamente "before routing"; sin componente propio
      todavía en este registry)
    - construir el AgentState/AgentActivationRequest real de un agente concreto (AgentCore,
      CMP-011, ya introducido en CH-11 — AdmissionController decide SI se puede proceder, AgentCore
      decide CÓMO nace el run)
    - evaluar policy sobre una ToolCall ya en curso (PolicyEngine, CMP-005, ya introducido en
      CH-05 — distinto momento, distinta pregunta: "¿puede esta activación empezar?" vs. "¿puede
      esta acción ejecutarse?")
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con una
particularidad respecto a CH-01..CH-11: por primera vez, ninguna de las cuatro exclusiones proviene
de una ficha propia de Article III (que no existe para este componente); las cuatro provienen, en
cambio, de fronteras ya establecidas por Amendment v1.1 (`P-16`, "before routing" de `P-17`) o por
componentes ya registrados (`AgentCore`, `PolicyEngine`).

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
AdmissionController
    consumes → ActivationRequest
    produces → AdmissionDecision, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`AdmissionController` no depende hoy de ningún otro componente registrado — mismo patrón que
CH-01..CH-11 ya establecieron para sus propios componentes. En prosa (nunca dentro de un bloque
`pseudocode`, per `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las relaciones
futuras que un capítulo de integración agregaría son:

| Componente futuro (relación inversa — no cableada en este capítulo) | Qué relación tendría con `AdmissionController` |
|---|---|
| Un mecanismo de Routing (todavía sin componente propio en este registry) | tomaría un `AdmissionDecision` con `outcome = ADMIT`, junto con el `ActivationRequest` original, y resolvería a qué `AgentId`/`AgentConfig` concreto corresponde — una decisión que `P-17` coloca explícitamente después de la admisión, y que `AdmissionController` nunca resuelve por su cuenta |
| `AgentCore` (ya existente, CMP-011) | recibiría, de ese mecanismo de routing futuro, un `agentId` ya resuelto con el cual construir un `AgentActivationRequest` (C-021) real — `AgentCore.activateAgent` (CH-11) no cambia una sola línea de su código ya publicado para que este capítulo sea correcto |
| `PolicyEngine` (ya existente, CMP-005) | sigue evaluando, sin cambios, si una `ToolCall` ya resuelta dentro de un run ya admitido y ya activado puede ejecutarse — una pregunta completamente distinta, en un momento completamente distinto del pipeline, de la que `AdmissionController` responde |

`registry/components.yaml` de `CMP-005` (`PolicyEngine`) y `CMP-011` (`AgentCore`) **no se
modifica** en este capítulo: ninguno agrega `CMP-012` a sus `dependencies`, y ninguno cambia su
pseudocódigo. El pseudocódigo de la seccion 11 construye y evalúa un `ActivationRequest`/
`AdmissionDecision` de forma completamente autónoma — sin que ninguno de los dos componentes ya
existentes cambie una sola línea para que este capítulo sea correcto. Ese cableado real es,
explícitamente, trabajo de un capítulo de integración futuro (ver seccion 18/19).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14), siguiendo la forma canónica que `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §31 ("Regla
de activación") exige para toda arquitectura empresarial: "`Trigger -> Adapter -> ActivationRequest
-> Admission -> Route -> ExecutionTarget`" — nunca `Webhook -> AgentLoop` directamente.

**Vista 1 — Componentes**

```text
[Trigger — estímulo externo crudo, infraestructura, fuera de este registry] →
[Ingress Adapter — infraestructura de borde, fuera de este registry, produce ActivationRequest] →
AdmissionController →
[Routing — Preview de esta interacción, todavía sin componente propio] →
[AgentCore — CMP-011, ya existente, Preview de esta interacción: activateAgent solo se invoca
 después de un routing real que este capítulo no construye]
```

**Vista 2 — Sequence**

```text
ActivationRequest
   │ (id, sourceRef, externalIdentityRef, payload, receivedAt)
   ▼
AdmissionController
   │ evaluateAdmissionForActivationRequest(request)
   │ ¿admissionRulesGrantAccess(request)? — identity/authorization/tenant/capacity/rate/budget/
   │                                        deduplication/policy (P-17), evaluadas en conjunto
   │   no  → outcome = REJECT (fail-closed, HarnessError categoría ADMISSION)
   │   sí  → outcome = ADMIT (reason = NULL)
   ▼
AdmissionDecision (requestId, outcome, reason, decidedAt)
   │
   │ ... REJECT: el llamador original recibe la HarnessError embebida en reason; ningún AgentRun
   │             llega a existir; el ActivationRequest nunca alcanza AgentCore ...
   │
   │ ... ADMIT: un mecanismo de Routing (Preview, sin componente propio todavía) resolvería a qué
   │            AgentId corresponde externalIdentityRef, y solo entonces AgentCore.activateAgent
   │            (CH-11, Preview de esta interacción; su código no cambia) construiría un
   │            AgentActivationRequest (C-021) real — integración de un capítulo futuro ...
```

**Vista 3 — Pseudocódigo**

Ver §11: `evaluateAdmissionForActivationRequest` es la primera formalización ejecutable de "ninguna
activación tiene derecho inherente a ejecutar" (`P-17`) — construida exclusivamente a partir de
material que ya existe (`HarnessError` desde CH-00) más los dos contratos nuevos de este capítulo.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde CH-00.

```pseudocode
FUNCTION evaluateAdmissionForActivationRequest(request: ActivationRequest) -> AdmissionDecision

    outcome: AdmissionOutcome = REJECT
    reason: Optional<HarnessError> = HarnessError(
        category = ADMISSION,
        code = "NO_ADMISSION_RULE_GRANTS_ACCESS",
        message = "Ninguna regla de admisión (identity, authorization, tenant, capacity, rate, budget, deduplication o policy) concedió acceso a esta activación; AdmissionController rechaza por defecto (fail-closed)",
        recoverable = TRUE,
        retryable = FALSE,
        metadata = {}
    )

    IF admissionRulesGrantAccess(request)
        outcome = ADMIT
        reason = NULL
    END

    decision: AdmissionDecision = AdmissionDecision(
        requestId = request.id,
        outcome = outcome,
        reason = reason,
        decidedAt = now()
    )

    RETURN decision
END
```

`now()` es la misma primitiva de CH-00. `admissionRulesGrantAccess(request: ActivationRequest) ->
Boolean` es una primitiva nueva de este capítulo, en el mismo espíritu que `policyRuleFound(...)`/
`policyRuleAllows(...)` (CH-05) o `findAgentConfig(...)` (CH-11): una función determinista ya
asumida, sin ficha ni registro propio — este capítulo no modela cómo se almacenan o evalúan,
individualmente, las ocho dimensiones que `P-17` enumera (identity, authorization, tenant,
capacity, rate, budget, deduplication, policy); las agrupa bajo un único resultado booleano interno
a la primitiva, exactamente como `ExecutionController` (CH-07) agrupó seis dimensiones distintas de
`ExecutionBudget` bajo un único `ExecutionUsage` sin modelar cada una como su propio `STRUCT` (ver
seccion 18 para el porqué de este límite de alcance).

Nótese el orden: primero se asume `REJECT` — con su `HarnessError` ya construida —, y solo si
`admissionRulesGrantAccess` concede acceso se sobrescribe hacia `ADMIT`. Este orden nunca se
invierte, por la misma razón que `PolicyEngine` (CH-05) nunca invierte el suyo: asumir acceso
primero y negarlo después dejaría una ventana, aunque fuera momentánea en el pseudocódigo, en la
que una activación sin regla aplicable pareciera admitida.

Nótese también lo que `evaluateAdmissionForActivationRequest` **no** hace: no invoca
`AgentCore.activateAgent` (CH-11) ni construye ningún `AgentState`; no invoca
`PolicyEngine.evaluatePolicyForToolCall` (CH-05) ni ningún otro componente ya existente; no resuelve
ni construye ningún `AgentId` a partir de `request.externalIdentityRef`; y — a diferencia de cada
uno de los once componentes anteriores — no emite ningún `AgentEvent` (ver seccion 14 para el
hallazgo real y su porqué).

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013): sigue siendo, sin cambios, el
mismo `ENUM` de once estados que `AgentLoop` (CH-01) formalizó. A diferencia de CH-11 — que ya
ejercitó, por primera vez, la transición `CREATED → INITIALIZING` de Article V —, este capítulo no
ejercita ninguna transición de ese diagrama en absoluto: su decisión ocurre un paso **antes** de
que exista siquiera el primer `AgentState` (`CREATED`, CH-11), porque en el instante de una
admisión todavía no existe ni un `agentId` resuelto sobre el cual la primera transición de Article
V pudiera aplicarse.

```text
(evaluateAdmissionForActivationRequest, ActivationRequest recibido)
   → AdmissionDecision con outcome = REJECT
     (ninguna regla de admisión concedió acceso; el ActivationRequest nunca avanza más allá de
     este punto — ningún AgentRun llega a existir)

   → AdmissionDecision con outcome = ADMIT
     (la activación puede proceder; falta todavía resolver a qué AgentId corresponde — Routing,
     Preview — antes de que AgentCore.activateAgent, CH-11, pueda siquiera invocarse)
```

`ActivationRequest`/`AdmissionDecision` no tienen, deliberadamente, ningún `ENUM` de estados propio
— se evalúan una única vez, de forma síncrona, exactamente el mismo patrón que
`AgentActivationRequest` (CH-11 §6) ya estableció para su propio contrato de activación.

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6, extendido en la seccion 6 de este capítulo) clasifica
también el único fallo real que introduce este capítulo:

```text
ADMISSION
    NO_ADMISSION_RULE_GRANTS_ACCESS   — ninguna regla de admisión conocida (identity, authorization,
                                        tenant, capacity, rate, budget, deduplication, policy)
                                        concedió acceso a este ActivationRequest; AdmissionController
                                        rechaza por defecto (fail-closed)
        → recoverable: TRUE, retryable: FALSE
```

Este es el primer fallo real del libro clasificado bajo `category = ADMISSION` — un valor que este
mismo capítulo agrega a `ErrorCategory` (seccion 6), porque ninguna de las once categorías ya
existentes representa, sin conflación, el rechazo de una activación cruda. `recoverable = TRUE`
(el problema es corregible — por ejemplo, otorgar la autorización de tenant que faltaba) pero
`retryable = FALSE` (reintentar exactamente el mismo `ActivationRequest`, sin cambiar el contexto de
autorización, fallaría de forma idéntica) — mismo razonamiento exacto que `NO_APPLICABLE_POLICY_RULE`
(CH-05) ya estableció para su propio fail-closed.

**La distinción más importante de esta sección**: `AdmissionDecision.reason` (un `HarnessError`)
solo se construye cuando `outcome = REJECT`. Un `outcome = ADMIT` **no es, en sí mismo, un
resultado exitoso que necesite documentarse aquí** — es, simplemente, la ausencia de rechazo; la
misma distinción que CH-05 §13 ya trazó entre `DENY` (con `HarnessError`) y `ALLOW`/
`REQUIRE_APPROVAL` (sin él).

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo de `category =
INFRASTRUCTURE` que pudiera ocurrir en una implementación real de las ocho verificaciones que
`admissionRulesGrantAccess` agrupa (por ejemplo, un servicio de identidad completamente
inalcanzable) — ese valor de `ErrorCategory` sigue, después de este capítulo, sin que ningún
componente real lo haya ejercitado nunca (mismo límite que CH-11 §13 ya documentó para
`findAgentConfig`).

## 14. Eventos Producidos (Events Produced)

**Este es el primer componente real del libro cuya función principal nunca construye un
`AgentEvent`.** Este capítulo no agrega ningún valor nuevo a `AgentEventType` — y, a diferencia de
cada uno de los once componentes anteriores (incluido `EventBus`, CH-09, que tampoco produce
`AgentEvent`, pero por una razón distinta: no decide nada), `AdmissionController` sí decide algo
(`ADMIT`/`REJECT`) sin que ese "algo" pueda expresarse, hoy, como un `AgentEvent` válido.

**El hallazgo real, verificado y documentado sin ocultarlo.** `AgentEvent` (C-010, CH-00) declara
cuatro campos obligatorios — `runId: RunId`, `sessionId: SessionId`, `agentId: AgentId`,
`traceId: TraceId` — ninguno `Optional`. Los cuatro describen, literalmente, un `AgentRun` que
existe. En el instante en que `evaluateAdmissionForActivationRequest` produce un
`AdmissionDecision`:

- no existe ningún `runId` (`AgentCore.activateAgent`, CH-11, es quien lo mina, y solo después de
  la admisión y del routing);
- no existe ningún `sessionId` real (mismo caso);
- no existe ningún `agentId` **resuelto** — ni siquiera cuando `outcome = ADMIT`: `AdmissionDecision`
  (seccion 6) deliberadamente no lo resuelve, esa es la responsabilidad de un routing todavía sin
  construir;
- no existe ningún `traceId` (`AgentCore.beginAgentInitialization`, CH-11, es quien mina el primer
  `TraceId` real del libro, y solo después de que el run ya fue `CREATED`).

Construir un `AgentEvent` de todas formas exigiría inventar valores centinela para los cuatro
campos — exactamente el tipo de solución artificial que este libro evita (mismo principio que
motivó, en CH-13 §14, documentar honestamente el reuso de `RUN_FAILED` en vez de inventar una
extensión no planeada de `AgentEventType`). Este capítulo, en cambio, documenta la ausencia como lo
que es: un hallazgo real, no un descuido.

**La relación con `P-25` (Amendment v1.1: "Audit evidence is distinct from operational
telemetry").** Esta ausencia no es, en sí misma, un vacío de seguridad silencioso: es, precisamente,
la distinción que `P-25` exige explícitamente. `AgentEvent`/`EventBus` (Article X) modelan
telemetría operacional de un `AgentRun` ya en curso — nunca fueron diseñados para representar
decisiones anteriores a que un run exista. Una evidencia de auditoría real de cada
`AdmissionDecision` (quién la evaluó, con qué reglas, en qué momento) necesitaría, per `P-25`, un
mecanismo **distinto** de `EventBus` — uno que este capítulo no construye (seccion 18). Lo único que
este capítulo deja disponible para esa auditoría futura es la correlación mínima que
`AdmissionDecision.requestId` ya provee: suficiente para reconstruir, más tarde, qué
`ActivationRequest` produjo qué decisión — no suficiente, todavía, para un registro de auditoría
inmutable propiamente dicho.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

`AdmissionController` es el primer componente de este libro cuya responsabilidad completa es de
seguridad perimetral — no de autorización de una acción ya resuelta (eso sigue siendo, en
exclusiva, de `PolicyEngine`, CH-05, `P-13`), ni de ruteo hacia un agente concreto (sin dueño
todavía).

**La distinción con `PolicyEngine` (CH-05), explícita y completa.** Ambos componentes producen un
resultado determinístico de al menos dos valores con una razón trazable — y, precisamente por esa
semejanza superficial, la frontera merece repetirse con el mismo cuidado que CH-10/CH-11 ya
aplicaron a sus propias fronteras delicadas. `PolicyEngine.evaluatePolicyForToolCall` (CH-05)
recibe un `ToolCall` **ya resuelto** (`CapabilityRegistry`, CH-08, ya lo validó) dentro de un
`AgentRun` **ya en curso**, y decide si esa acción concreta puede ejecutarse. `AdmissionController.
evaluateAdmissionForActivationRequest` (este capítulo) recibe un `ActivationRequest` que ni siquiera
tiene un `agentId` resuelto, y decide si esa activación puede, en principio, empezar a procesarse —
mucho antes de que exista cualquier `ToolCall`, `AgentRun` o `ExecutionContext` sobre el cual
`PolicyEngine` pudiera operar. Reutilizar `PolicyEngine` para evaluar `ActivationRequest` — o
reutilizar la categoría `POLICY` para el `HarnessError` de este capítulo — confundiría dos
decisiones de dos dominios distintos, exactamente el error que Article IV (Ownership Rule) prohíbe.

**La distinción con `AgentCore` (CH-11), explícita y completa.** `AgentCore.activateAgent` (CH-11)
valida que un `AgentConfig` **ya conocido** exista y que su `ExecutionBudget` sea coherente —
preguntas que solo tienen sentido una vez que se sabe a qué agente se refiere la activación.
`AdmissionController` opera un paso antes: cuando `outcome = ADMIT`, todavía falta resolver (routing,
sin componente propio) a qué `AgentId` corresponde `request.externalIdentityRef` antes de que
`AgentCore.activateAgent` pueda siquiera invocarse con un `AgentActivationRequest` (C-021) real.
Que `AdmissionController` nunca resuelva ese `AgentId` por su cuenta es, precisamente, lo que impide
que absorba silenciosamente la responsabilidad de `AgentCore` (Article IV, Ownership Rule).

**Lo que este capítulo NO implementa todavía.** `admissionRulesGrantAccess` (seccion 11) es una
primitiva asumida: ningún mecanismo real de identidad, autorización de tenant, límites de
capacidad, rate limiting, presupuesto de ingreso, deduplicación o policy de admisión se modela en
detalle — la misma clase de límite que CH-05 §18 documentó para el almacenamiento real de policy
rules, o que CH-11 §15 documentó para `findAgentConfig`. Tampoco se modela ningún mecanismo real de
Routing (seccion 5/9), ni el `Ingress Adapter` concreto que produciría un `ActivationRequest` a
partir de un webhook, una cola o un cron real.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST AdmissionControllerRejectsByDefaultWhenNoAdmissionRuleGrantsAccess
TEST AdmissionControllerAdmitsOnlyWhenAdmissionRulesGrantAccess
TEST AdmissionControllerNeverConstructsAnAgentStateOrAgentActivationRequest
TEST AdmissionControllerNeverInvokesAgentCoreOrPolicyEngine
TEST AdmissionControllerNeverEmitsAnAgentEvent
TEST ActivationRequestNeverCarriesAResolvedAgentId
TEST AdmissionDecisionCorrelatesBackToActivationRequestByRequestIdOnly
TEST AdmissionDecisionReasonIsPopulatedOnlyWhenOutcomeIsReject
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (después de CH-14 — primer capítulo de Amendment v1.1, Enterprise)

Constitution
 ├── Article III  — Component Sovereignty (once componentes de "Agent Runtime", sin cambios desde
 │                   CH-11)
 ├── Article IV   — Decision Ownership (tabla original sin cambios; AdmissionController documentado
 │                   en prosa como la fila que Amendment v1.1 todavía no agrega al archivo fuente)
 └── Amendment v1.1 — Enterprise Activation, Interoperability and Operations (P-16/P-17/INV-E01/
                       INV-E02 citados por primera vez con código real; Ingress & Activation Plane,
                       primer componente instalado de nueve planes canónicos)

Contracts (registry/contracts.yaml)
 ├── C-001..C-021  (sin cambios — CH-00..CH-11)
 ├── C-022 ActivationRequest      (CH-14, nuevo — el estímulo externo ya normalizado, sin agentId
 │                                 resuelto)
 └── C-023 AdmissionDecision      (CH-14, nuevo — ADMIT/REJECT sobre un ActivationRequest, nunca
                                   un Boolean)

Components (registry/components.yaml)
 ├── CMP-001..CMP-011  (sin cambios — CH-01..CH-11)
 └── CMP-012 AdmissionController  (CH-14, nuevo — primer componente de este registry que no
                                   corresponde a ninguno de los once nombres de Article III;
                                   pertenece al Ingress & Activation Plane de Amendment v1.1)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado real `AdmissionController → Routing → AgentCore`**: ningún componente invoca
  todavía `evaluateAdmissionForActivationRequest` seguido de una resolución real de `AgentId` y de
  `AgentCore.activateAgent` (CH-11) como un único flujo — ese cableado, incluyendo qué componente
  resolvería el routing, sigue siendo trabajo de un capítulo de integración futuro (mismo patrón de
  deuda intencional que CH-12/CH-13 ya mostraron cómo cerrar cuando llegue el momento).
- **El "Ingress Adapter" real detrás de `ActivationRequest`**: primitiva/infraestructura asumida,
  sin modelar ningún webhook, cola, cron o API concretos que produzcan un `ActivationRequest` real.
- **El mecanismo real detrás de `admissionRulesGrantAccess`**: primitiva asumida, sin modelar
  identidad, autorización de tenant, límites de capacidad, rate limiting, presupuesto de ingreso,
  deduplicación ni policy de admisión en detalle — cada una de las ocho dimensiones de `P-17`
  queda, honestamente, sin implementación real.
- **Ausencia de `AgentEvent`/evidencia de auditoría real para una `AdmissionDecision`** (`P-25`):
  documentado con cuidado en la seccion 14 — este capítulo no construye el mecanismo de auditoría
  distinto de `EventBus` que `P-25` exigiría para un registro inmutable de cada admisión.
- **Los ocho planes restantes de Amendment v1.1** (Execution, Agent Interoperability, Capability &
  Integration, Data & Context, Control, Reliability, Observability & Governance, Execution Fabric)
  y sus componentes (`AgentCommunicationGateway`, `CredentialBroker`, y el resto): explícitamente
  fuera de alcance de este capítulo.
- **Deduplicación real de `ActivationRequest` repetidas**: `P-17` la menciona como una de las ocho
  dimensiones, pero este capítulo no modela ningún almacén de solicitudes ya vistas.
- **Admisión condicional o diferida** (un tercer valor de `AdmissionOutcome` distinto de
  `ADMIT`/`REJECT`): no modelado — ver seccion 6.
- Reviewers plurales, evals y orquestación multi-agente: explícitamente fuera de alcance de
  BH-v0.1 (igual que todos los capítulos anteriores).

## 19. Siguiente Incremento (Next Increment)

Con este capítulo, el "Ingress & Activation Plane" de Amendment v1.1 tiene su primer componente
real — pero el plano completo (Ingress Adapter concreto, Routing, el cableado real hacia
`AgentCore`) sigue sin construirse de punta a punta. El problema natural del próximo incremento es,
o bien profundizar este mismo plano (Routing como componente propio, un `Ingress Adapter` concreto),
o bien avanzar hacia el segundo de los nueve planes canónicos — Execution Plane — que Amendment
v1.1 enumera junto a este.

`next_chapter` queda en `null` en el frontmatter de este capítulo porque, en este momento del libro,
ese próximo capítulo todavía no existe como archivo — solo como el problema que motivaría su
escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg /
> Bucles de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows),
> secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): trece capítulos reales construyeron un runtime completo,
   pero ninguno preguntó si el estímulo que dispara todo eso, en sí mismo, tenía derecho a
   intentarlo — `AgentActivationRequest` (CH-11) ya asume un `agentId` conocido, y CH-11 §15
   documentó, sin resolverlo, que ningún control de autorización existía sobre quién puede activar
   un agente ajeno.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): Amendment v1.1
   nombra literalmente `ActivationRequest`/`AdmissionController` desde que fue adoptada; CH-11 ya
   encontró esos nombres, los distinguió con cuidado y los dejó explícitamente diferidos bajo el
   término "Ingress Activation" — este capítulo paga esa deuda, no la reabre.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `AdmissionController` con una ficha que declara tanto lo que posee (`owns`: cita literal de
   `P-17`) como lo que explícitamente NO posee (`does_not_own`: normalizar el estímulo, rutear,
   activar, evaluar policy sobre una acción ya en curso) y formaliza el primer par
   solicitud/decisión que opera enteramente antes de que exista un `agentId` resuelto.
4. **Modelos mentales** (= §4, Constitutional Impact): Article IV y `AgentActivationRequest` (CH-11)
   ya asumen que alguien decidió que esta activación puede proceder con un `agentId` conocido — este
   capítulo muestra que hay una pregunta todavía más temprana.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un sistema deja sin modelar la frontera de ingreso,
  cualquier estímulo externo puede alcanzar `AgentCore.activateAgent` asumiendo, en silencio, que
  quien lo invoca ya está autorizado — el mismo bucle que `Default Deny` (CH-05) ya combatió puertas
  adentro del runtime, ahora en su borde exterior.
- **Bucle de equilibrio (estabiliza):** `evaluateAdmissionForActivationRequest` (§11) rechaza por
  defecto (`Default Reject`) en cuanto ninguna regla de admisión concede acceso, y nunca resuelve
  por su cuenta a qué agente concreto correspondería una activación admitida.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `AdmissionDecision` se correlacione de vuelta
con `ActivationRequest` únicamente por `requestId` — nunca resolviendo, inventando o adivinando un
`AgentId` concreto. Si `AdmissionController` construyera ese `AgentId` por su cuenta "ya que de
todos modos decide si la activación puede proceder", absorbería silenciosamente el ruteo y la
activación real — dos decisiones que Article IV exige mantener con dueños separados.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo
> de esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set`
> (frontmatter) y es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa,
> para lectura directa del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Todo estímulo externo que podría disparar la activación de un agente llega, hasta ahora, sin que
   ningún componente decida primero si ese estímulo, en sí mismo, tiene siquiera derecho a intentar
   activar algo. ¿Qué necesitaría existir para que esa pregunta tenga, por fin, un dueño único?
   *(cierra la pregunta guía 1)*
2. El contrato que hace nacer un run ya conocido siempre parte de un identificador de agente ya
   resuelto. ¿Qué forma tendría un contrato que representa la misma intención de activarse pero
   ANTES de que exista ese identificador? *(cierra la pregunta guía 2)*
3. Un resultado de dos valores ya se usó en este libro para decidir si una acción ya resuelta puede
   ocurrir. ¿Por qué esa misma forma de resultado, aplicada a si una activación cruda puede
   siquiera empezar, necesita un dueño distinto? *(cierra la pregunta guía 3)*
4. Cada evento observable que este libro produjo necesita un run, una sesión y una traza a las que
   pertenecer. ¿Qué pasa cuando la decisión que se necesita observar ocurre antes de que
   cualquiera de esas tres cosas exista? *(cierra la pregunta guía 4)*

### Explicar

1. `AdmissionController` posee aplicar identity, authorization, tenant, capacity, rate, budget,
   deduplication y policy decisions antes de rutear una activación. Explica, como si hablaras con
   alguien sin contexto técnico, por qué NO posee resolver a qué `AgentId` concreto corresponde esa
   activación una vez admitida.
2. `ActivationRequest` no tiene ningún campo `agentId`, a diferencia de `AgentActivationRequest`
   (CH-11), que lo exige siempre. Explica por qué esa ausencia es, precisamente, la que hace
   posible que `AdmissionController` exista como un componente distinto de `AgentCore`.

### Conectar

1. `AgentCore.activateAgent` (CH-11) documentó, sin resolverlo, que ningún control de autorización
   existía sobre quién puede activar un agente ajeno. ¿Cerraría eso una `AdmissionDecision` con
   `outcome = ADMIT` justo antes de `activateAgent`, o simplemente movería el hueco a una pregunta
   distinta y todavía sin dueño?
2. `PolicyEngine` (CH-05) ya produce un outcome de tres valores evaluando si una acción ya resuelta
   puede ocurrir. ¿Por qué no basta con que `PolicyEngine` evalúe también las `ActivationRequest`?

### Espaciar

Las cinco tarjetas de repaso de este capítulo (dos sobre `AdmissionController` — su `owns` y su
`does_not_own` —, una sobre `ActivationRequest`, una sobre `AdmissionDecision`, y una sobre la
ausencia de `AgentEvent`) entran hoy en `reviewStage = DAY_1`. Repásalas de nuevo al día 3, al día 7
y al día 21 (curva de Ebbinghaus) — ver el apéndice de tarjetas al final del libro (edición PDF) o
`retrieval_set.flashcards` en `dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te equivocaste,
ese es precisamente el punto ciego que este método existe para revelar.
