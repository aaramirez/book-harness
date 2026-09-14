---
id: CH-09
title: "EventBus y la Distribución Desacoplada de un Evento Ya Producido"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-009]
introduces_contracts: [C-019]
modifies_contracts: []
constitutional_articles: [P-04, P-11, P-12, P-25, INV-18, INV-19, INV-20]
previous_chapter: CH-08
next_chapter: CH-10
retrieval_set:
  expected_outcome:
    id: EO-CH09
    text: |
      Al terminar este capítulo podrás distinguir, dentro del recorrido completo de un `AgentEvent`
      ya construido correctamente por cualquier componente del runtime, qué tramo le pertenece en
      exclusiva al mecanismo que lo hace llegar a quien lo necesita y qué tramos pertenecen a
      dominios distintos (decidir qué información contiene ese evento, interpretarlo, actuar sobre
      él, persistirlo de forma durable) — y podrás diseñar, para cualquier consumidor desacoplado
      que declare qué eventos le interesan, el mecanismo que registra esa relación y entrega cada
      evento nuevo hacia las relaciones activas que apliquen, sin que el componente que produjo el
      evento tenga que saber nada sobre quién lo recibe.
  skeleton:
    id: SK-CH09
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
    components_to_be_introduced: [CMP-009]
    contracts_to_be_introduced: [C-019]
  guiding_questions:
    - id: GQ-CH09-01
      text: |
        Cuando un componente ya construye correctamente el hecho de que algo significativo ocurrió
        (una decisión de autorización, una tool call completada, una capacidad resuelta) y lo
        declara mediante una construcción de la gramática de este libro reservada para "esto ya
        pasó", ¿quién decide, en la práctica, quién más se entera de que pasó — y qué tendría que
        existir para que esa pregunta tuviera una respuesta real en vez de asumida?
      answered_by: RQ-CH09-01
    - id: GQ-CH09-02
      text: |
        Si nueve tipos de consumidor completamente distintos (uno que solo guarda un registro
        plano, otro que reconstruye una traza completa, otro que audita, otro que reproduce una
        ejecución pasada...) necesitan enterarse del mismo hecho ocurrido dentro de una ejecución,
        ¿debería cada componente que produce ese hecho conocer, por nombre, a cada uno de esos
        nueve consumidores? ¿Qué se rompe si la respuesta es "sí"?
      answered_by: RQ-CH09-02
    - id: GQ-CH09-03
      text: |
        Si a un consumidor concreto solo le interesa un tipo de hecho entre dieciséis posibles —o
        solo los hechos de una ejecución concreta entre miles—, ¿en qué momento y con qué mecanismo
        se decide que ese consumidor no necesita enterarse de los otros quince tipos, sin que el
        componente que produjo el hecho tenga que saber nada sobre ese filtro?
      answered_by: RQ-CH09-03
    - id: GQ-CH09-04
      text: |
        Un consumidor que hoy quiere enterarse de algo puede, mañana, dejar de querer enterarse —
        sin que eso signifique que nunca debió haberse enterado en el pasado. ¿Qué necesita existir
        para que esa decisión de "ya no más" quede registrada de forma explícita, en vez de
        simplemente dejar de invocar en silencio un mecanismo que nunca se declaró formalmente?
      answered_by: RQ-CH09-04
  systems_lens:
    iceberg_visible_fact: |
      La construcción `EMIT AgentEvent(...)` aparece quince veces a lo largo de los nueve archivos
      de capítulo reales del libro (CH-00..CH-08), producida por ocho componentes distintos — y
      ninguna de esas quince apariciones nunca tuvo, hasta este capítulo, ningún mecanismo real que
      recibiera lo que emitía (ver seccion 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite, ahora aplicado a la distribución de eventos, es que un verbo de la
      gramática canónica del libro (`EMIT`, reservado desde `write-pseudocode/SKILL.md`) puede
      usarse correctamente, capítulo tras capítulo, sin que nadie repare en que ese verbo nunca tuvo
      un destino real — porque cada componente productor solo necesitaba demostrar que construía
      bien su propio `AgentEvent`, nunca a quién se lo entregaba (ver seccion 3, Por Qué la
      Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala el noveno componente real del libro, `EventBus` (CMP-009), con una
      ficha que declara tanto lo que posee (`owns`: registrar una suscripción, cancelarla,
      distribuir cada `AgentEvent` ya producido hacia las suscripciones activas que hagan match —
      cita literal de Article III) como lo que explícitamente NO posee (`does_not_own`: decidir qué
      información contiene un evento, interpretar o actuar sobre él, persistir historial de forma
      durable, decidir continuación de turno) — y formaliza `EventSubscription` (C-019), el sexto
      contrato verdaderamente nuevo del libro (ver seccion 8, Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior sigue siendo el Ownership Rule de Article IV
      — pero aplicado, por primera vez, a un componente que Article IV ni siquiera enumera en su
      tabla de Decision Ownership: `EventBus` es el primer componente real del libro sin una fila
      propia en esa tabla, porque distribuir no es decidir — la ausencia misma es la confirmación
      textual más fuerte de su frontera (ver seccion 4, Impacto Constitucional).
    reinforcing_loop: |
      Cuantos más de los nueve consumidores que Article X nombra (Logs, Tracing, Audit, Replay,
      Analytics, Evals, Cost Analysis, Debugging, UI) existan sin un mecanismo real de
      distribución, más tentador resulta que cada uno, al construirse, invente su propio
      acoplamiento directo contra cada uno de los ocho componentes productores — multiplicando
      nueve consumidores por ocho productores en vez de sumarlos.
    balancing_loop: |
      `distributeEvent` (seccion 11) es el mecanismo de equilibrio: colapsa esa multiplicación en
      una sola relación por consumidor (`EventSubscription`) y una sola llamada por productor
      (`EMIT`, sin cambios), sin que ningún productor necesite conocer, por nombre, a ningún
      consumidor.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `EventBus` (CMP-009) nunca decida qué
      información contiene un `AgentEvent`, nunca lo interprete, y nunca emita su propio evento
      sobre el hecho de haberlo distribuido — preservando exactamente la frontera que Article III
      traza entre "producir" (los ocho componentes ya existentes) y "distribuir" (este capítulo).
      Si `EventBus` cruzara esa frontera —agregando un campo al payload, o emitiendo un evento
      sobre su propia distribución—, dejaría de ser el "dumb pipe" desacoplado que Article III
      describe y empezaría a absorber silenciosamente decisiones que pertenecen a otros dominios.
  recall_questions:
    - id: RQ-CH09-01
      text: |
        ¿Qué componente resuelve, con un mecanismo real, quién más se entera de que un `AgentEvent`
        ya producido por otro componente ocurrió, y qué contrato registra esa relación?
    - id: RQ-CH09-02
      text: |
        ¿Por qué `EventBus` no necesita —ni le pertenece— conocer por nombre a cada consumidor
        (Logs, Tracing, Audit, ...) que Article X exige poder alimentar?
    - id: RQ-CH09-03
      text: |
        ¿Contra qué campos de `EventFilter` se compara un `AgentEvent` para decidir si hace match
        con una `EventSubscription`, y qué significa que ese filtro sea `NULL`?
    - id: RQ-CH09-04
      text: |
        ¿Qué dos estados tiene `EventSubscriptionStatus`, y qué le impide a `cancelSubscription`
        "reactivar" una suscripción ya cancelada?
  explain_prompts:
    - id: EP-CH09-01
      text: |
        `EventBus` posee distribuir un `AgentEvent` ya producido hacia las suscripciones activas
        que hagan match. Explica, como si hablaras con alguien sin contexto técnico, por qué NO
        posee decidir qué información va dentro de ese `AgentEvent`, aunque es literalmente quien
        lo entrega — ¿qué se rompería si `EventBus` empezara a agregar o quitar campos del payload
        antes de entregarlo?
      target_entity: CMP-009
    - id: EP-CH09-02
      text: |
        `EventSubscription.subscriberRef` es una referencia opaca a un consumidor desacoplado,
        nunca un `STRUCT` propio para Logs/Tracing/Audit/Replay/Analytics/Evals/Cost Analysis/
        Debugging/UI. Explica qué perderíamos si `EventBus`, en vez de una referencia opaca,
        modelara en detalle cada tipo concreto de consumidor dentro de su propio registro.
      target_entity: C-019
  interleaved_questions:
    - id: IQ-CH09-01
      text: |
        `ToolRuntime` (CH-02) emite `TOOL_CALL_COMPLETED`/`TOOL_CALL_FAILED` con un `ToolResult`
        (C-009) como `payload` desde su propio `executeToolCall` (CH-02 §11), sin que ese capítulo
        modele nunca a dónde va ese evento después de `EMIT`. ¿Qué construye este capítulo para que
        ese mismo `AgentEvent`, ya producido exactamente igual que en CH-02, pueda llegar a un
        consumidor real — y qué tuvo que cambiar en `ToolRuntime.executeToolCall` para que eso
        funcione?
      current_chapter_entities: [CMP-009, C-019]
      prior_chapter_entities: [CMP-002, C-009]
      prior_chapter: CH-02
    - id: IQ-CH09-02
      text: |
        `PolicyEngine` (CH-05) emite `POLICY_EVALUATED` con una `PolicyDecision` (C-014) como
        `payload` desde su propio `evaluatePolicy` (CH-05 §11). Un consumidor de auditoría (Article
        X, Article II P-25) necesita enterarse exactamente de ese hecho, y solo de ese hecho, entre
        los dieciséis tipos de `AgentEventType` que existen. ¿Qué mecanismo de este capítulo hace
        posible esa selectividad sin que `PolicyEngine` tenga que saber que la auditoría existe?
      current_chapter_entities: [CMP-009, C-019]
      prior_chapter_entities: [CMP-005, C-014]
      prior_chapter: CH-05
  flashcards:
    - id: FC-CH09-01
      front: |
        ¿Qué posee `EventBus` (Article III / Article IV), en una frase?
      back: |
        Registrar la suscripción de un consumidor desacoplado (una referencia opaca más un filtro
        opcional), cancelar una suscripción ya registrada, y distribuir (fan-out) cada `AgentEvent`
        ya producido por cualquier componente hacia las suscripciones activas que hagan match por
        filtro — cita literal de Article III: "distribuir eventos del runtime a consumidores
        desacoplados".
      source_entity: CMP-009
      chapter_introduced_in: CH-09
      review_stage: DAY_1
    - id: FC-CH09-02
      front: |
        ¿Qué NO posee `EventBus`, y a qué componentes/conceptos pertenecen esas decisiones?
      back: |
        Decidir qué información va dentro de un `AgentEvent` (cada componente productor ya
        existente, CMP-001..CMP-008), interpretar o actuar sobre un evento distribuido (Logs/
        Tracing/Audit/Replay/Analytics/Evals/Cost Analysis/Debugging/UI, Article X — ninguno
        componente propio de este registry todavía), persistir historial de sesión de forma
        durable (`SessionManager`, Article III, preview) y decidir continuación de turno u otra
        decisión arquitectónica (`AgentLoop`/`PolicyEngine`/`ExecutionController`, ya existentes).
      source_entity: CMP-009
      chapter_introduced_in: CH-09
      review_stage: DAY_1
    - id: FC-CH09-03
      front: |
        ¿Por qué `EventBus` es el primer componente real del libro sin fila propia en la tabla de
        Decision Ownership de Article IV?
      back: |
        Porque Article IV solo asigna una fila a un componente que decide algo ("¿debería ocurrir
        otro turno?", "¿puede ocurrir esta acción?", ...), y `EventBus` no decide nada: solo mueve,
        sin interpretar, algo que otro componente ya decidió. Su ausencia de esa tabla no es un
        descuido — es la confirmación textual más fuerte posible de que su única función es
        mecánica.
      source_entity: CMP-009
      chapter_introduced_in: CH-09
      review_stage: DAY_1
    - id: FC-CH09-04
      front: |
        ¿Qué campos tiene `EventSubscription` (C-019), y qué representan?
      back: |
        `id` (`EventSubscriptionId`, el identificador de esta suscripción), `subscriberRef` (`Text`,
        una referencia opaca al consumidor desacoplado), `filter` (`Optional<EventFilter>`, `NULL`
        significa "todo tipo de evento"; si no es `NULL`, restringe por `eventType` y/o `runId`),
        `status` (`EventSubscriptionStatus`: `ACTIVE`/`CANCELLED`) y `subscribedAt` (`Timestamp`).
      source_entity: C-019
      chapter_introduced_in: CH-09
      review_stage: DAY_1
    - id: FC-CH09-05
      front: |
        ¿Por qué `EventBus`, a diferencia de siete de los ocho componentes anteriores, no agrega
        ningún valor nuevo a `AgentEventType` ni emite jamás su propio `AgentEvent`?
      back: |
        Porque una suscripción no está necesariamente ligada a un único `AgentRun` (su `filter`
        puede dejar `runId` sin restringir), así que `EventBus` no siempre tiene un
        `ExecutionContext` real con el cual fabricar un `AgentEvent` propio y válido; y porque
        emitir un evento sobre "distribuí este evento" sería circular — obligaría a `EventBus` a
        interpretar como significativo un hecho (su propia distribución) que Article III le prohíbe
        interpretar.
      source_entity: CMP-009
      chapter_introduced_in: CH-09
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH09-01
      recall_question: RQ-CH09-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH09-02
      recall_question: RQ-CH09-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH09-03
      recall_question: RQ-CH09-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH09-04
      recall_question: RQ-CH09-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 9 — EventBus y la Distribución Desacoplada de un Evento Ya Producido

> **Regla constitucional (Article III, sección "EventBus"):** responsable de distribuir eventos
> del runtime a consumidores desacoplados.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de saber
> cómo se llama el componente de este capítulo. El detalle estructurado de esta sección vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, dentro del recorrido completo
de un `AgentEvent` ya construido correctamente por cualquier componente del runtime, qué tramo le
pertenece en exclusiva al mecanismo que lo hace llegar a quien lo necesita y qué tramos pertenecen a
dominios distintos (decidir qué información contiene ese evento, interpretarlo, actuar sobre él,
persistirlo de forma durable) — y podrás diseñar, para cualquier consumidor desacoplado que declare
qué eventos le interesan, el mecanismo que registra esa relación y entrega cada evento nuevo hacia
las relaciones activas que apliquen, sin que el componente que produjo el evento tenga que saber
nada sobre quién lo recibe.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e introduce
un contrato de datos nuevo (`EventSubscription`) y el noveno componente de runtime del libro
(`EventBus`) — todavía sin explicarlos, solo como mapa. A diferencia de los ocho capítulos
anteriores, este es el primero cuyo componente nuevo no aparece en la tabla de Decision Ownership de
Article IV: no porque el libro lo haya olvidado, sino porque —como este capítulo demuestra— no le
pertenece ninguna decisión.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar atrás;
están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este capítulo
va a definir):

1. Cuando un componente ya construye correctamente el hecho de que algo significativo ocurrió y lo
   declara mediante una construcción de la gramática de este libro reservada para "esto ya pasó",
   ¿quién decide, en la práctica, quién más se entera de que pasó — y qué tendría que existir para
   que esa pregunta tuviera una respuesta real en vez de asumida?
2. Si nueve tipos de consumidor completamente distintos necesitan enterarse del mismo hecho
   ocurrido dentro de una ejecución, ¿debería cada componente que produce ese hecho conocer, por
   nombre, a cada uno de esos nueve consumidores? ¿Qué se rompe si la respuesta es "sí"?
3. Si a un consumidor concreto solo le interesa un tipo de hecho entre dieciséis posibles —o solo
   los hechos de una ejecución concreta entre miles—, ¿en qué momento y con qué mecanismo se decide
   que ese consumidor no necesita enterarse de los otros quince tipos?
4. Un consumidor que hoy quiere enterarse de algo puede, mañana, dejar de querer enterarse. ¿Qué
   necesita existir para que esa decisión de "ya no más" quede registrada de forma explícita?

## 1. Arquitectura Actual (Current Architecture)

CH-00..CH-08 dejaron instalados dieciocho contratos de datos y ocho componentes de runtime.
Los ocho componentes emiten `AgentEvent` (C-010) de verdad: `AgentLoop` (CH-01), `ToolRuntime`
(CH-02), `ModelGateway` (CH-03), `ContextEngine` (CH-04), `PolicyEngine` (CH-05),
`HumanInteractionService` (CH-06), `ExecutionController` (CH-07) y `CapabilityRegistry` (CH-08) —
cada uno construyendo, correctamente, un `AgentEvent` con su `eventId`/`timestamp`/`runId`/
`sessionId`/`agentId`/`traceId`/`payload` completos, y declarándolo mediante la palabra reservada de
la gramática canónica del libro (`write-pseudocode/SKILL.md`) para "esto ya ocurrió": `EMIT`.

La construcción `EMIT AgentEvent(...)` aparece **quince veces** a lo largo de los nueve archivos de
capítulo reales (CH-00: 1, CH-01: 1, CH-02: 2, CH-03: 2, CH-04: 2, CH-05: 1, CH-06: 2, CH-07: 1,
CH-08: 3). `AgentEventType` (embebido en `AgentEvent`, C-010, CH-00) acumula, después de CH-08,
**dieciséis valores**: `RUN_STARTED`, `TURN_CONTINUED`, `RUN_COMPLETED`, `RUN_FAILED`,
`TOOL_CALL_COMPLETED`, `TOOL_CALL_FAILED`, `MODEL_RESPONSE_RECEIVED`, `MODEL_INVOCATION_FAILED`,
`CONTEXT_SNAPSHOT_ASSEMBLED`, `CONTEXT_SNAPSHOT_FAILED`, `POLICY_EVALUATED`,
`HUMAN_INTERACTION_REQUESTED`, `HUMAN_INTERACTION_RESOLVED`, `EXECUTION_EVALUATED`,
`CAPABILITY_RESOLVED`, `CAPABILITY_RESOLUTION_FAILED`.

Ninguna de esas quince apariciones de `EMIT` tiene, hasta este capítulo, ningún destino real. Ningún
capítulo definió jamás qué hace `EMIT` como operación — ni qué recibe lo emitido, ni si algo lo
recibe. `constitution/ARCHITECTURE_CONSTITUTION.md` Article III ya nombra `EventBus` desde la
primera versión de la constitución adoptada por este repositorio (la misma que introduce
`SessionManager`, ambos todavía preview hasta este capítulo), con una sola línea: "Responsable de
distribuir eventos del runtime a consumidores desacoplados." Article X (Observability Constitution)
exige, además, que "esta fuente de eventos debe poder alimentar": `Logs`, `Tracing`, `Audit`,
`Replay`, `Analytics`, `Evals`, `Cost Analysis`, `Debugging`, `UI` — nueve consumidores nombrados
explícitamente, ninguno de los cuales ha recibido jamás, en este libro, un solo `AgentEvent` real.

## 2. El Problema (Problem)

Cada uno de los ocho componentes existentes hace exactamente lo que le corresponde: construye un
`AgentEvent` con la forma correcta y lo declara con `EMIT`. Pero `EMIT`, tal como la gramática
canónica lo reserva, nunca fue una operación con destino — es, hasta este capítulo, un verbo sin
mecanismo. INV-18 exige que "toda acción significativa produce un evento observable"; los ocho
componentes cumplen la primera mitad de esa frase (producen el evento) pero ninguno, ni ningún otro
componente del libro, cumple la segunda (que ese evento sea, de verdad, observable por alguien fuera
del componente que lo produjo). Un evento que nadie puede recibir no es observable en ningún sentido
práctico — es, como mucho, construido.

Sin un componente con fronteras explícitas para esto, cada uno de los nueve consumidores que Article
X nombra (`Logs`, `Tracing`, `Audit`, `Replay`, `Analytics`, `Evals`, `Cost Analysis`, `Debugging`,
`UI`) tendría que inventar, el día que se construya, su propio acoplamiento directo contra cada uno
de los ocho componentes productores — exactamente lo que la Observability Rule de Article X
prohíbe: "la observabilidad debe surgir de primitives del runtime, no de instrumentación ad hoc
dispersa por las aplicaciones." Sin un dueño único para "quién recibe este `AgentEvent`", la pregunta
se resolvería, tarde o temprano, de nueve maneras distintas — una por consumidor, cada una
reintroduciendo el acoplamiento directo productor-consumidor que el resto de este libro evitó con
tanto cuidado (Article III, Component Sovereignty).

Necesitamos que "¿quién más se entera de que este `AgentEvent` ocurrió?" tenga, por fin, un dueño
único y nombrado — que registre, para cada consumidor desacoplado, qué eventos le interesan (todos,
o un subconjunto filtrado), que entregue cada `AgentEvent` nuevo hacia las relaciones activas que
apliquen, y que dependa exclusivamente de eventos ya producidos por cualquier componente anterior —
sin que ese mecanismo decida, en el mismo movimiento, qué información debería llevar ese evento, ni
qué debería hacer el consumidor con él una vez recibido.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los dieciocho contratos y los ocho componentes que existen hasta este punto no bastan porque:

- Article III nombra `EventBus` en su árbol de "Agent Runtime" desde la primera versión de la
  constitución adoptada, con una responsabilidad explícita ("distribuir eventos del runtime a
  consumidores desacoplados") que ningún capítulo había materializado con código real;
- Article IV (Decision Ownership) enumera una fila por cada componente que decide algo — `LLM`,
  `AgentLoop`, `ContextEngine`, `ModelGateway`, `ToolRuntime`, `PolicyEngine`,
  `HumanInteractionService`, `SessionManager`, `ExecutionController`, `CapabilityRegistry`, `UI` —
  pero **no** incluye ninguna fila para `EventBus`: distribuir un hecho ya decidido no es, en sí
  mismo, una decisión arquitectónica nueva, y esa ausencia textual es, precisamente, lo que este
  capítulo debe confirmar con código real, no contradecir;
- `AgentEvent` (C-010) se ha producido quince veces por ocho componentes distintos, siempre
  mediante `EMIT`, y cero veces ha existido un registro real de quién quiere recibir cada tipo de
  evento — no hay, hasta este capítulo, ningún contrato que represente esa relación;
- Article X nombra nueve consumidores explícitos que "esta fuente de eventos debe poder
  alimentar", y ninguno de los nueve tiene, hasta este capítulo, ningún camino real hacia ningún
  `AgentEvent` producido por este libro;
- Article XI (`EVO-01`, "Keep the core small") ya nombra `Event Consumer` como un punto de
  extensión legítimo, junto a `Extension`/`Hook`/`ContextProvider`/`Tool`/`Policy`/`Adapter` — pero
  sin un mecanismo real de suscripción, no existe ningún lugar donde un `Event Consumer` pudiera
  registrarse.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la secuencia
> `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una entidad que no
> haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT` registrado — **no
> magic entities**. Este capítulo aplica la misma disciplina que CH-01..CH-08 ya establecieron, con
> una particularidad: por primera vez, el pseudocódigo de este capítulo consume un contrato (
> `AgentEvent`, C-010) sin necesitar, para ninguna de sus operaciones, un `ExecutionContext` propio
> — ver seccion 8/9 para la razón completa.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-04   Every action produces observable events.
           Hasta este capítulo, P-04 se cumplía solo a medias: cada componente productor generaba
           el evento, pero ningún mecanismo lo hacía llegar a "UI, logging, tracing, persistence,
           analytics y audit" — exactamente los consumidores que P-04 nombra por su propio texto.
           EventBus es la primera vez que la segunda mitad de ese principio se materializa con
           código real.
    P-11   UI is an adapter, not part of the core.
           UI (Article IV, Article X) recibe su AgentEvent exactamente igual que Logs/Tracing/
           Audit: mediante una EventSubscription tan opaca como la de cualquier otro consumidor —
           EventBus no le concede ningún privilegio ni acoplamiento especial.
    P-12   Events observe; hooks intervene.
           EventBus solo mueve algo que observa (un AgentEvent) — nunca decide ni interviene en el
           lifecycle de una ejecución; esa frontera es, literalmente, su does_not_own (seccion 8).
    P-25   Audit evidence is distinct from operational telemetry.
           distributeEvent (seccion 11) entrega el mismo AgentEvent, sin fusionarlo ni
           reinterpretarlo, a cada EventSubscription que haga match — la distinción entre lo que es
           evidencia de auditoría y lo que es telemetría operacional la conserva cada consumidor
           mediante su propio filtro, nunca EventBus por decisión propia.

Invariants preserved
    INV-18   Toda acción significativa produce un evento observable.
             Primera vez que "observable" deja de significar solo "construido correctamente" para
             significar "puede llegar de verdad a un consumidor" — aunque qué cuenta como
             significativo lo sigue decidiendo, en exclusiva, el componente productor (EventBus
             nunca decide eso).
    INV-19   Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy relevante.
             distributeEvent (seccion 11) nunca modifica ningún campo del AgentEvent que recibe —
             ni siquiera su traceId — así que la trazabilidad que el componente productor ya
             construyó llega intacta hasta el consumidor, precisamente porque EventBus no
             interpreta el payload.
    INV-20   Todo error operacional pertenece a una categoría conocida.
             SUBSCRIBER_REF_REQUIRED, SUBSCRIPTION_NOT_FOUND, SUBSCRIPTION_ALREADY_CANCELLED y
             DISTRIBUTION_REQUESTED_WITHOUT_EVENT reutilizan VALIDATION, la misma categoría que
             CH-02/CH-08 ya usaron para fallos estructuralmente equivalentes de entrada.

Component ownership changes
    CMP-009 EventBus se introduce — registry/components.yaml pasa de 8 a 9 componentes. Es el
    primer componente real del libro sin fila propia en la tabla de Decision Ownership de Article
    IV — no por omisión editorial, sino porque distribuir no es decidir (seccion 8 lo confirma con
    código real). owns/does_not_own citados literalmente contra Article III (sección "EventBus").
    registry/components.yaml de CMP-001..CMP-008 NO se modifica.

Lifecycle changes
    Ninguno sobre AgentRunStatus (C-013): sigue siendo propiedad exclusiva de AgentLoop (CH-01).
    AgentEvent (C-010) no cambia de forma. A diferencia de siete de los ocho capítulos anteriores,
    este capítulo NO agrega ningún valor a AgentEventType (seccion 5/14 explican por qué) — la
    segunda vez que esto ocurre en el libro, después de CH-01, pero por una razón estructuralmente
    distinta (ver seccion 14).

Security implications
    EventBus nunca decide autorización ni interpreta el contenido de un AgentEvent (P-13 sigue
    siendo exclusivo de PolicyEngine, CH-05); su única superficie de fallo es administrativa —
    quién puede registrar o cancelar una suscripción, nunca qué contiene lo que se distribuye. Ver
    seccion 15 para el análisis completo, incluyendo un límite que este capítulo deja
    explícitamente abierto.

Observability implications
    Primer componente del libro que no extiende AgentEventType y que no emite ningún AgentEvent
    propio en ninguna de sus funciones — ni en el camino exitoso ni en el de fallo. Ver seccion 14
    para la justificación completa (evitar el problema de "un evento sobre distribuir un evento").

Deterministic vs agentic boundary
    Article XII no se refina de forma nueva aquí: de los nueve componentes reales del libro,
    EventBus es el primero cuya frontera determinística no tiene nada que ver con una propuesta
    del modelo — no consume ninguna salida del modelo, ni directa ni indirectamente. Su frontera es
    exclusivamente entre productores y consumidores ya determinísticos.
```

## 5. Conceptos Nuevos (New Concepts)

- **Event Distribution / Fan-out**: el mecanismo, exigido por Article III, que toma un `AgentEvent`
  ya producido por cualquier componente y lo entrega a cada consumidor desacoplado cuya suscripción
  haga match — respondiendo, por primera vez con código real, la pregunta que quince apariciones de
  `EMIT` dejaron sin resolver desde CH-00.
- **Event Subscription**: el registro nombrado de la relación entre un consumidor desacoplado y los
  eventos que le interesan — modelado como el contrato `EventSubscription` (C-019, seccion 7).
- **Decoupled Consumer / Subscriber**: quien se suscribe a la distribución de eventos, representado
  únicamente por una referencia opaca (`subscriberRef`) — nunca modelado en detalle: `Logs`,
  `Tracing`, `Audit`, `Replay`, `Analytics`, `Evals`, `Cost Analysis`, `Debugging` y `UI` (Article X)
  son consumidores conceptuales, no componentes propios de este registry todavía.
- **Event Filter**: el criterio opcional, embebido dentro de una `EventSubscription`, que decide si
  un `AgentEvent` concreto hace match con esa suscripción — por `eventType` y/o `runId`. Su ausencia
  (`filter = NULL`) significa "todo tipo de evento, de cualquier ejecución".
- **Decision Ownership por ausencia** *(Article IV, en uso desde CH-01, aplicado aquí por primera
  vez a la inversa)*: `EventBus` es el primer componente real del libro que Article IV no enumera
  en su tabla — porque no le pertenece decidir nada, solo distribuir lo que otros ya decidieron.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados de CH-00/CH-01/CH-02/CH-03/CH-04/CH-05/CH-06/CH-07/CH-08

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `RunId`, `Timestamp`, `AgentEvent`, `HarnessError`,
`ToolResult`, `PolicyDecision`.

Dos tipos adicionales, ya existentes desde CH-00, no tienen contrato propio con `C-XXX` (viven
embebidos dentro de `AgentEvent`/`HarnessError`), y este capítulo los reutiliza por tipo, sin
agregarles ningún valor nuevo — mismo patrón que CH-01 §6 ya estableció para el mismo caso:

| Identificador (heredado, sin `C-XXX` propio) | Rol en este capítulo |
|---|---|
| `AgentEventType` | tipo del campo opcional `EventFilter.eventType`; reutiliza los dieciséis valores ya definidos hasta CH-08 (`POLICY_EVALUATED`, `TOOL_CALL_COMPLETED`, ...) — no se agrega ningún valor nuevo (ver seccion 14) |
| `ErrorCategory` | tipo de `category` en los `HarnessError` que produce `EventBus`; reutiliza `VALIDATION`, ya definido en CH-00 |

### Un identificador opaco nuevo

Siguiendo el mismo patrón que CH-00 §6 estableció para los identificadores fundamentales y que
CH-02/CH-06/CH-08 ya repitieron cada uno para el suyo:

| Identificador (nuevo de este capítulo) | Identifica |
|---|---|
| `EventSubscriptionId` | una suscripción de un consumidor desacoplado, activa o ya cancelada |

### `EventSubscriptionStatus` — el lifecycle de dos estados de una suscripción

```pseudocode
ENUM EventSubscriptionStatus
    ACTIVE
    CANCELLED
END
```

Deliberadamente dos estados, no más — mismo argumento que `HumanInteractionStatus` (CH-06): este
capítulo no modela expiración automática ni reactivación como un tercer valor (seccion 12/18).

### `EventFilter` — el criterio opcional de una suscripción

```pseudocode
STRUCT EventFilter
    eventType: Optional<AgentEventType>
    runId: Optional<RunId>
END
```

`EventFilter` vive embebido dentro de `EventSubscription`, sin contrato `C-XXX` propio — el mismo
patrón que `RawToolCallProposal` (CH-03), `ContextBlock` (CH-04), `ExecutionUsage` (CH-07) o
`PolicyOutcome`/`HumanInteractionOutcome` (CH-05/CH-06): un tipo real, con forma explícita, pero sin
necesitar un identificador de Contract Registry independiente porque nunca se referencia fuera de la
estructura que lo contiene. Deliberadamente dos campos, ambos opcionales: `eventType` restringe por
el tipo de hecho ocurrido; `runId` restringe por la ejecución concreta. Un filtro adicional por
`sessionId`/`agentId`/rango de `timestamp` (el "etc." que un consumidor real podría necesitar) queda
fuera de alcance de este capítulo (ver seccion 18) — dos campos alcanzan para demostrar el mecanismo
de match completo (seccion 11) sin necesitar un lenguaje de filtrado genérico.

### `EventSubscription` — la suscripción registrada

```pseudocode
STRUCT EventSubscription
    id: EventSubscriptionId
    subscriberRef: Text
    filter: Optional<EventFilter>
    status: EventSubscriptionStatus
    subscribedAt: Timestamp
END
```

Cinco campos, cada uno respondiendo a una parte exacta del alcance decidido para este capítulo:
`id` identifica esta suscripción de forma estable; `subscriberRef` es, deliberadamente, una
referencia opaca (`Text`) al consumidor desacoplado — nunca un `STRUCT` que modele "qué es" `Logs`
o `Audit` en detalle (Article III llama a estos consumidores, literalmente, "desacoplados"; modelar
su detalle cruzaría exactamente esa línea); `filter` es `Optional<EventFilter>` — `NULL` significa
"todo tipo de evento, de cualquier ejecución"; `status` es el lifecycle de dos estados de la sección
anterior; `subscribedAt` registra cuándo se registró. **Ningún campo de canal, transporte ni
protocolo de entrega**: igual que `HumanInteractionRequest` (CH-06) no modela un canal concreto,
`EventSubscription` no modela cómo `deliver` (seccion 11) alcanza en la práctica a `subscriberRef` —
esa es, precisamente, la responsabilidad que Article III reserva a cada consumidor desacoplado, no a
`EventBus`.

**Unchanged / Not yet introduced**: `AgentEvent` (C-010) no cambia de forma — sigue siendo
exactamente el `STRUCT` de CH-00. Este capítulo tampoco introduce ningún `STRUCT` para representar
el mecanismo de *persistencia* de una `EventSubscription` entre reinicios (no hay
`SubscriptionRegistrationRequest` ni equivalente): el conjunto de `EventSubscription` ya registradas
llega, a `distributeEvent` (seccion 11), como parámetro ya poblado — la misma primitiva asumida
legítima que `registeredCapabilities` en CH-08.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce un contrato de
datos, registrado en `registry/contracts.yaml`:

```text
ID:                     C-019
Name:                   EventSubscription
Version:                v1
Introduced In:          CH-09
Current Definition:     STRUCT EventSubscription (ver §6)
Used By:                [CMP-009]
Modified By:            []
Constitutional Impact:  [P-04, P-12, INV-18, INV-19]
```

`C-019` es el sexto id verdaderamente nuevo del libro (el correlativo continúa después de `C-018`,
CH-08 — ningún id quedaba reservado desde CH-01 §7, exactamente como ya ocurrió con `C-014`..`C-018`
en CH-05/CH-06/CH-07/CH-08). El nombre `EventSubscription`, y no `Subscription` a secas ni
`Consumer`, es deliberado: el contrato no representa al consumidor (eso es `subscriberRef`, opaco
por diseño) ni a un evento (eso ya es `AgentEvent`, C-010) — representa, específicamente, la
*relación registrada* entre ambos, la misma disciplina de nombres que ya distingue
`CapabilityDescriptor` (el registro de una capability, CH-08) de `Capability` (el concepto, CH-02).

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el noveno componente de runtime del libro:

```pseudocode
COMPONENT EventBus
    consumes: AgentEvent
    produces: EventSubscription, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Article III (sección "EventBus"):

```text
COMPONENT: EventBus

Responsibility:
    Registrar la suscripción de un consumidor desacoplado (una referencia opaca más un filtro
    opcional por eventType/runId), permitir su cancelación y distribuir (fan-out) cada AgentEvent
    ya producido por cualquier otro componente del runtime hacia las suscripciones activas que
    hagan match — sin decidir qué información contiene ese evento, sin interpretar ni actuar sobre
    él, sin persistir historial de sesión de forma durable y sin decidir continuación de turno ni
    ninguna otra decisión arquitectónica.

Consumes:
    C-010 AgentEvent (lo que distribuye; ya producido por CMP-001..CMP-008)

Depends on:
    (ninguno todavía — el cableado real con cada componente productor y con los consumidores de
    Article X es Preview, no introducido en este capítulo; ver seccion 9)

Produces:
    C-011 HarnessError (fallos administrativos de suscripción), C-019 EventSubscription (el
    registro que este componente posee)

Owns (Article III, cita literal, expandida):
    - registrar una suscripción de un consumidor desacoplado (subscriberRef opaco más un filtro
      opcional)
    - cancelar una suscripción ya registrada
    - distribuir (fan-out) cada AgentEvent ya producido por cualquier componente hacia las
      suscripciones activas que hagan match por filtro
    - desacoplar al productor de un AgentEvent de sus consumidores (cita literal de Article III:
      "distribuir eventos del runtime a consumidores desacoplados")

Does NOT own (Article IV — declarado con el mismo peso que Owns, aunque Article IV no le asigna
fila propia a este componente, ver nota debajo):
    - decidir qué información va dentro de un AgentEvent (cada componente productor ya lo decide al
      construir su propio AgentEvent — CMP-001..CMP-008, ya introducidos; EventBus recibe ese
      AgentEvent ya completo y nunca le agrega ni le quita campos)
    - interpretar o actuar sobre un AgentEvent distribuido (Logs/Tracing/Audit/Replay/Analytics/
      Evals/Cost Analysis/Debugging/UI, Article X — ninguno es un componente propio de este
      registry todavía; actuar sobre un evento es, literalmente, trabajo del consumidor, no de
      quien lo transporta)
    - persistir historial de sesión de forma durable para reconstrucción posterior (SessionManager,
      Article III — no introducido, preview; distinción cuidadosa: EventBus distribuye en el
      momento, SessionManager podría usar esos mismos eventos para reconstruir estado más tarde —
      son responsabilidades distintas, nunca la misma)
    - decidir continuación de turno o cualquier otra decisión arquitectónica (AgentLoop, CMP-001;
      PolicyEngine, CMP-005; ExecutionController, CMP-007 — todos ya introducidos)
```

**Nota sobre la ausencia en Article IV**: a diferencia de los ocho componentes anteriores, cuya
ficha citaba una fila explícita de la tabla de Decision Ownership ("`AgentLoop` → Should another
reasoning turn occur?", "`CapabilityRegistry` → What implementation satisfies a requested
capability?", ...), Article IV **no** enumera ninguna fila para `EventBus`. Esta ausencia no es un
descuido de la constitución ni de este capítulo: es la confirmación textual más fuerte posible de
que `EventBus` no decide nada. Cada componente que Article IV sí enumera responde una pregunta de la
forma "¿qué debería ocurrir?"; `EventBus` nunca responde ninguna pregunta de esa forma — solo mueve,
sin decidir, algo que otro componente ya decidió.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
EventBus
    consumes → AgentEvent
    produces → EventSubscription, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`EventBus` no depende hoy de ningún otro componente registrado — mismo patrón que CH-01..CH-08 ya
establecieron para sus propios componentes. Una diferencia real respecto a los ocho anteriores: por
primera vez, un componente del libro **no consume `ExecutionContext` (C-004)**. Los ocho
componentes anteriores lo consumían porque cada uno necesitaba `runId`/`sessionId`/`traceId` para
fabricar su propio `AgentEvent` nuevo. `EventBus` nunca fabrica un `AgentEvent` nuevo (seccion 14) —
solo recibe uno ya completo, con esos mismos campos ya poblados por su productor — así que no
necesita un `ExecutionContext` propio para ninguna de sus operaciones.

En prosa (nunca dentro de un bloque `pseudocode`, per `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§22 regla 8), las relaciones futuras que un capítulo de integración agregaría son:

| Componente/concepto futuro (relación inversa — no cableada en este capítulo) | Qué relación tendría con `EventBus` |
|---|---|
| `AgentLoop`, `ToolRuntime`, `ModelGateway`, `ContextEngine`, `PolicyEngine`, `HumanInteractionService`, `ExecutionController`, `CapabilityRegistry` (todos ya existentes) | cada uno seguiría emitiendo su propio `AgentEvent` exactamente igual que hoy (`EMIT`, sin cambios) — un capítulo de integración futuro conectaría ese `EMIT` con `distributeEvent` (seccion 11) |
| `Logs` / `Tracing` / `Audit` / `Replay` / `Analytics` / `Evals` / `Cost Analysis` / `Debugging` (Article X, conceptos) | cada uno se registraría como una `EventSubscription` con `subscriberRef` propio — ninguno es un componente de este registry todavía |
| `UI` (Article IV, Article X) | recibiría su `AgentEvent` mediante una `EventSubscription` igual de opaca que cualquier otro consumidor — sin ningún acoplamiento especial (P-11) |
| `SessionManager` (Article III, preview) | podría suscribirse como un consumidor más para reconstruir historial de forma durable — distinto de la distribución en el momento que `EventBus` ya realiza |

`registry/components.yaml` de `CMP-001`..`CMP-008` **no se modifica** en este capítulo: ninguno
agrega `CMP-009` a su `dependencies`, y ninguno cambia su pseudocódigo. El pseudocódigo de la
seccion 11 muestra a `EventBus` distribuyendo, de forma completamente autónoma, dos `AgentEvent` de
ejemplo —uno con la forma exacta que `PolicyEngine` (CH-05) ya produce, otro con la forma exacta que
`ToolRuntime` (CH-02) ya produce— sin que ninguno de los dos componentes cambie una sola línea para
que este capítulo sea correcto. El cableado real de punta a punta (que el `EMIT` de cada componente
productor invoque de verdad `distributeEvent`) es, explícitamente, trabajo de un capítulo de
integración futuro (ver seccion 18/19).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[PolicyEngine — produce AgentEvent (POLICY_EVALUATED), CH-05, conceptual] → EventBus →
[Audit / Logs / Tracing / ... — consumidores desacoplados, Article X, conceptual]
```

**Vista 2 — Sequence**

```text
AgentEvent
   │ (ya producido por cualquier componente anterior — ej. PolicyEngine, CH-05, conceptual)
   ▼
EventBus
   │ distributeEvent(event, activeSubscriptions)
   │ ¿event == NULL?
   │     sí → HarnessError (DISTRIBUTION_REQUESTED_WITHOUT_EVENT, VALIDATION)
   │ recorre activeSubscriptions
   │     subscription.status == ACTIVE Y eventMatchesFilter(event, subscription.filter)
   │         sí → deliver(subscription.subscriberRef, event); agrega subscription a matched
   │         no → ignora esta subscription (no es un fallo)
   │ RETURN matched (puede ser una lista vacía — cero consumidores interesados no es un error)
   ▼
matched: List<EventSubscription>
   │
   ▼
[Logs / Tracing / Audit / Replay / Analytics / Evals / Cost Analysis / Debugging / UI —
consumidores desacoplados, Article X, conceptual — reciben event sin que EventBus interprete su
contenido]
```

**Vista 3 — Pseudocódigo**

Ver §11: `distributeEvent` es la primera formalización ejecutable de "`EventBus` decide quién más
se entera de que un `AgentEvent` ya ocurrió"; `eventMatchesFilter` es, además, la primera "puerta"
de todo el libro que es pseudocódigo real de principio a fin (no una señal asumida como
`argumentsMatchSchema`, CH-08, o `inputValid`, CH-02) — porque la forma de un `EventFilter` es lo
bastante simple (dos campos opcionales, comparación directa) para no necesitar un motor de
validación externo.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde
CH-00/CH-02/CH-05.

```pseudocode
FUNCTION registerSubscription(
    subscriberRef: Text,
    filter: Optional<EventFilter>
) -> EventSubscription

    IF subscriberRef == ""
        failure: HarnessError = HarnessError(
            category = VALIDATION,
            code = "SUBSCRIBER_REF_REQUIRED",
            message = "EventBus no puede registrar una suscripción sin un subscriberRef",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW failure
    END

    subscription: EventSubscription = EventSubscription(
        id = newEventSubscriptionId(),
        subscriberRef = subscriberRef,
        filter = filter,
        status = ACTIVE,
        subscribedAt = now()
    )

    RETURN subscription
END
```

```pseudocode
FUNCTION cancelSubscription(
    subscriptionId: EventSubscriptionId,
    subscriptions: List<EventSubscription>
) -> EventSubscription

    target: Optional<EventSubscription> = NULL

    FOR EACH candidate IN subscriptions
        IF candidate.id == subscriptionId
            target = candidate
        END
    END

    IF target == NULL
        failure: HarnessError = HarnessError(
            category = VALIDATION,
            code = "SUBSCRIPTION_NOT_FOUND",
            message = "EventBus no encontró ninguna EventSubscription registrada con este id",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW failure
    END

    IF target.status == CANCELLED
        failure: HarnessError = HarnessError(
            category = VALIDATION,
            code = "SUBSCRIPTION_ALREADY_CANCELLED",
            message = "cancelSubscription fue invocada sobre una EventSubscription ya cancelada",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW failure
    END

    cancelled: EventSubscription = EventSubscription(
        id = target.id,
        subscriberRef = target.subscriberRef,
        filter = target.filter,
        status = CANCELLED,
        subscribedAt = target.subscribedAt
    )

    RETURN cancelled
END
```

```pseudocode
FUNCTION eventMatchesFilter(
    event: AgentEvent,
    filter: Optional<EventFilter>
) -> Boolean

    IF filter == NULL
        RETURN TRUE
    END

    IF filter.eventType != NULL AND event.eventType != filter.eventType
        RETURN FALSE
    END

    IF filter.runId != NULL AND event.runId != filter.runId
        RETURN FALSE
    END

    RETURN TRUE
END
```

```pseudocode
FUNCTION distributeEvent(
    event: AgentEvent,
    subscriptions: List<EventSubscription>
) -> List<EventSubscription>

    IF event == NULL
        failure: HarnessError = HarnessError(
            category = VALIDATION,
            code = "DISTRIBUTION_REQUESTED_WITHOUT_EVENT",
            message = "distributeEvent fue invocada sin un AgentEvent para distribuir",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW failure
    END

    matched: List<EventSubscription> = []

    FOR EACH subscription IN subscriptions
        IF subscription.status == ACTIVE AND eventMatchesFilter(event, subscription.filter)
            deliver(subscription.subscriberRef, event)
            matched.append(subscription)
        END
    END

    RETURN matched
END
```

`newEventSubscriptionId()` y `now()` son las mismas primitivas de CH-00..CH-08 (esta última ya
usada, esta primera nueva, en el mismo espíritu que `newToolCallId()`/
`newHumanInteractionRequestId()`). `deliver(subscriberRef: Text, event: AgentEvent) -> Void` es una
primitiva asumida: representa la entrega real hacia el consumidor desacoplado que `subscriberRef`
referencia de forma opaca — igual que `now()`/`newEventId()` son primitivas de este libro, `deliver`
no es un componente ni requiere ficha propia; modelar su detalle (cómo exactamente `Logs`/`Tracing`/
`Audit`/`Replay`/`Analytics`/`Evals`/`Cost Analysis`/`Debugging`/`UI` reciben el evento en la
práctica — HTTP, cola de mensajes, stream, archivo) queda fuera de alcance de este capítulo (ver
seccion 18); Article III mismo llama a estos consumidores "desacoplados", precisamente lo que
`subscriberRef` preserva al mantenerlo opaco.

`eventMatchesFilter`, a diferencia de `argumentsMatchSchema` (CH-08 §11) o `inputValid` (CH-02 §11),
**no** es una señal de entrada asumida: es pseudocódigo real, completo y determinístico, porque la
forma de un `EventFilter` (dos campos opcionales, comparación directa) no requiere ningún lenguaje
de validación externo para expresarse. Esta es la primera "puerta" del libro que un capítulo
resuelve por completo, sin dejar ningún tramo pendiente.

Por primera vez en el libro, con `PolicyEngine` (CMP-005, CH-05), `ToolRuntime` (CMP-002, CH-02) y
`EventBus` (CMP-009, recién definido) ya existentes, se puede mostrar que la misma distribución
funciona de forma idéntica sin importar quién produjo el evento:

```pseudocode
FUNCTION demonstrateEventBusDistributingEventsFromTwoDifferentProducers(
    subscriptions: List<EventSubscription>,
    somePolicyDecision: PolicyDecision,
    someToolResult: ToolResult,
    runId: RunId,
    sessionId: SessionId,
    agentId: AgentId,
    traceId: TraceId
) -> List<EventSubscription>

    policyEvaluatedExample: AgentEvent = AgentEvent(
        eventId = newEventId(),
        eventType = POLICY_EVALUATED,
        timestamp = now(),
        runId = runId,
        sessionId = sessionId,
        agentId = agentId,
        traceId = traceId,
        payload = somePolicyDecision
    )

    toolCallCompletedExample: AgentEvent = AgentEvent(
        eventId = newEventId(),
        eventType = TOOL_CALL_COMPLETED,
        timestamp = now(),
        runId = runId,
        sessionId = sessionId,
        agentId = agentId,
        traceId = traceId,
        payload = someToolResult
    )

    deliveredForPolicy: List<EventSubscription> = distributeEvent(policyEvaluatedExample, subscriptions)
    deliveredForTool: List<EventSubscription> = distributeEvent(toolCallCompletedExample, subscriptions)

    RETURN deliveredForPolicy
END
```

`demonstrateEventBusDistributingEventsFromTwoDifferentProducers` es una demostración de integración,
no una tercera responsabilidad nueva: no es un método registrado de ninguna ficha de componente
adicional, y **no** modifica `CMP-005 PolicyEngine` ni `CMP-002 ToolRuntime` — ni sus fichas, ni sus
`consumes`/`produces`/`dependencies` en `registry/components.yaml`, ni la firma de
`evaluatePolicy`/`executeToolCall` (CH-05 §11 / CH-02 §11), que siguen devolviendo exactamente lo
mismo que devolvían antes de este capítulo. Muestra únicamente que, con `EventBus` ya existente, el
mismo `distributeEvent` trata un `AgentEvent` con `eventType = POLICY_EVALUATED` (payload:
`PolicyDecision`, CH-05) exactamente igual que uno con `eventType = TOOL_CALL_COMPLETED` (payload:
`ToolResult`, CH-02) — sin necesitar saber, en ningún punto de su lógica, cuál de los ocho
componentes productores lo generó.

Nótese lo que ninguna de estas funciones hace: no deciden qué información lleva el `payload` del
`AgentEvent` (eso ya lo decidió el componente productor), no interpretan ese `payload` de ninguna
forma, no evalúan ninguna policy sobre el evento que distribuyen, y no emiten, en ningún camino, un
`AgentEvent` propio sobre el hecho de haber distribuido algo (ver seccion 14).

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013): esa máquina de estados sigue siendo
propiedad exclusiva de `AgentLoop` (CH-01 §12), y su tabla de transiciones no cambia aquí.

`EventSubscriptionStatus` (§6) sí tiene un lifecycle propio, deliberadamente de dos estados y una
sola dirección:

```text
(registerSubscription) → ACTIVE
ACTIVE      --cancelSubscription-->  CANCELLED
CANCELLED   --cancelSubscription-->  HarnessError (SUBSCRIPTION_ALREADY_CANCELLED) — nunca reactiva
```

`distributeEvent` (§11) atraviesa un camino implícito con tres desenlaces posibles — deliberadamente
**no** formalizado como un contrato de lifecycle adicional (eso introduciría una segunda entidad
nueva, fuera del alcance decidido para este capítulo):

```text
AgentEvent recibido
   → event == NULL                                    → HarnessError (DISTRIBUTION_REQUESTED_WITHOUT_EVENT)
   → event válido, ninguna EventSubscription hace match → matched = [] (no es un error)
   → event válido, N EventSubscription hacen match      → matched tiene N elementos, cada uno entregado vía deliver
```

Una diferencia deliberada respecto a `resolveToolCall` (CH-08 §12): allí, "ningún `CapabilityDescriptor`
corresponde al nombre solicitado" **es** un fallo (`CAPABILITY_NOT_FOUND`) porque una tool call sin
capability resuelta no puede continuar. Aquí, "ninguna `EventSubscription` activa hace match" **no**
es un fallo: un evento sin consumidores interesados en este momento es una situación completamente
normal — nada obliga a que exista, en todo momento, al menos un suscriptor para cada tipo de evento.

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6) clasifica también los fallos que introduce este capítulo,
fiel a los `Failure Examples` de `constitution/ARCHITECTURE_CONSTITUTION.md` Article VII:

```text
VALIDATION
    SUBSCRIBER_REF_REQUIRED             — registerSubscription invocada con un subscriberRef vacío
        → recoverable: FALSE, retryable: FALSE
    SUBSCRIPTION_NOT_FOUND              — cancelSubscription invocada sobre un id que no
                                           corresponde a ninguna EventSubscription registrada
        → recoverable: FALSE, retryable: FALSE
    SUBSCRIPTION_ALREADY_CANCELLED      — cancelSubscription invocada sobre una EventSubscription
                                           cuyo status ya es CANCELLED (precondición de invocación,
                                           no un fallo de distribución en sí)
        → recoverable: FALSE, retryable: FALSE
    DISTRIBUTION_REQUESTED_WITHOUT_EVENT — distributeEvent invocada sin un AgentEvent para
                                            distribuir (precondición de invocación)
        → recoverable: FALSE, retryable: FALSE
```

Los cuatro fallos reutilizan, deliberadamente, `VALIDATION` — la misma categoría que CH-02/CH-08 ya
usaron para fallos estructuralmente equivalentes (un dato de entrada que no cumple una forma
esperada, nunca un fallo de la ejecución de una acción ya resuelta, que sería `TOOL`). Se evaluó
explícitamente introducir una categoría `SUBSCRIPTION` o `EVENT_BUS` nueva y se descartó por la
misma razón que CH-08 ya documentó para `CapabilityRegistry`: fragmentaría `ErrorCategory` sin
ganancia semántica real — "quién" detectó el problema no cambia "qué tipo" de problema es.

A diferencia de cada uno de los ocho capítulos anteriores, **ninguna** de las funciones de este
capítulo emite un `AgentEvent` antes de lanzar su `HarnessError` — ni siquiera en el camino exitoso.
Esta uniformidad (nunca `EMIT`, nunca) es, en sí misma, la característica distintiva de la Semántica
de Fallos de este capítulo: los ocho anteriores distinguían entre fallos que interrumpen una
precondición de invocación (sin `EMIT`, p. ej. `TURN_ON_TERMINAL_STATE`, CH-01) y fallos que sí son
un resultado legítimo de una operación que llegó a ejecutarse (con `EMIT`, p. ej.
`CAPABILITY_NOT_FOUND`, CH-08); `EventBus` no necesita esa distinción porque ninguno de sus caminos,
exitoso o fallido, emite jamás un evento propio (ver seccion 14 para la justificación completa).

## 14. Eventos Producidos (Events Produced)

Este capítulo, a diferencia de siete de los ocho anteriores, **no agrega ningún valor** a
`AgentEventType`, y ninguna de sus funciones emite jamás un `AgentEvent` propio.

La única excepción previa fue CH-01, que tampoco agregó valores — pero por una razón distinta y más
simple: sus propias acciones ya estaban cubiertas por vocabulario que CH-00 había definido
(`TURN_CONTINUED`, `RUN_COMPLETED`). La razón de este capítulo es estructuralmente más profunda, y
tiene dos partes:

1. **Una `EventSubscription` no está necesariamente ligada a un único `AgentRun`.** Su `filter`
   puede dejar `runId` sin restringir (`NULL`) — una suscripción es, por diseño, infraestructura que
   puede abarcar cero, uno o muchos runs. `AgentEvent` (C-010) exige `runId`/`sessionId`/`traceId`
   como campos obligatorios, no opcionales: `EventBus` no siempre tiene un `ExecutionContext` real y
   propio con el cual fabricar, de forma honesta, un `AgentEvent` sobre "se registró esta
   suscripción" — inventar uno sería fabricar trazabilidad que no existe (violaría, en espíritu,
   INV-19, no lo cumpliría).
2. **Emitir un evento sobre "distribuí este evento" sería circular.** Si `distributeEvent` emitiera
   su propio `AgentEvent` cada vez que entrega uno, ese nuevo evento también tendría que
   distribuirse — y `EventBus` tendría que decidir que el hecho de su propia distribución es, en sí
   mismo, significativo (INV-18), exactamente la interpretación de contenido que su
   `does_not_own` le prohíbe (seccion 8). La Observability Rule de Article X ("la observabilidad
   debe surgir de primitives del runtime, no de instrumentación ad hoc") se cumple mejor dejando que
   la significancia de un hecho la decida, una sola vez, quien lo produjo — no agregando una capa de
   eventos sobre eventos.

`TOOL_CALL_COMPLETED`/`TOOL_CALL_FAILED` (CH-02), `MODEL_RESPONSE_RECEIVED`/`MODEL_INVOCATION_FAILED`
(CH-03), `CONTEXT_SNAPSHOT_ASSEMBLED`/`CONTEXT_SNAPSHOT_FAILED` (CH-04), `POLICY_EVALUATED` (CH-05),
`HUMAN_INTERACTION_REQUESTED`/`HUMAN_INTERACTION_RESOLVED` (CH-06), `EXECUTION_EVALUATED` (CH-07) y
`CAPABILITY_RESOLVED`/`CAPABILITY_RESOLUTION_FAILED` (CH-08) siguen siendo, exactamente, los dieciséis
valores de `AgentEventType` que existen — `EventBus` los distribuye tal cual, sin agregar un
decimoséptimo.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

`EventBus` nunca decide autorización (P-13 sigue siendo exclusivo de `PolicyEngine`, CH-05) y nunca
interpreta el `payload` de un `AgentEvent` — un evento que documenta un `PolicyDecision.outcome =
DENY` se distribuye exactamente igual que uno que documenta `outcome = ALLOW`: `EventBus` no
discrimina según contenido, reforzando que su función es mecánica, no interpretativa (P-12: "events
observe; hooks intervene" — `EventBus` mueve lo que observa, nunca interviene sobre ello).

- **P-25 (Audit evidence is distinct from operational telemetry)**: `distributeEvent` entrega el
  mismo `AgentEvent`, sin fusión ni reinterpretación, a cada `EventSubscription` que haga match —
  la distinción entre lo que un consumidor trata como evidencia de auditoría y lo que otro trata
  como telemetría operacional la conserva cada consumidor mediante su propio `filter`, nunca
  `EventBus` por decisión propia. Si `EventBus` intentara clasificar internamente "esto es
  auditoría, esto es telemetría", estaría absorbiendo silenciosamente una decisión que P-25 exige
  mantener separada aguas abajo, en manos de quien de verdad la necesita.
- **Frontera con `SessionManager` (preview)**: `EventBus` distribuye en el momento — no persiste
  ningún historial que sobreviva a un reinicio. Un consumidor que necesite reconstruir estado
  después de un reinicio necesitaría un componente distinto (`SessionManager`, Article III, todavía
  no introducido) que se suscribiera igual que cualquier otro consumidor y persistiera lo que
  recibe — `EventBus` no lo hace por sí mismo.
- **Límite que este capítulo deja explícitamente abierto**: `registerSubscription` (seccion 11) no
  modela ningún control de acceso sobre **quién** puede registrar una suscripción, ni sobre **qué**
  `eventType`/`runId` puede filtrar — cualquier `subscriberRef` puede, en este capítulo, suscribirse
  a cualquier tipo de evento de cualquier ejecución. Esto es una limitación real, no un descuido
  silencioso (ver seccion 18): la autorización de suscripciones (p. ej. "¿puede este consumidor ver
  eventos de este `runId`?") queda fuera de alcance de BH-v0.1, y no debe asumirse resuelta.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST DistributeEventNeverModifiesTheAgentEventItReceives
TEST DistributeEventNeverThrowsWhenNoActiveSubscriptionMatches
TEST DistributeEventNeverDeliversToACancelledSubscription
TEST RegisterSubscriptionAlwaysRequiresANonEmptySubscriberRef
TEST CancelSubscriptionNeverSucceedsOnAnAlreadyCancelledSubscription
TEST EventBusNeverEmitsAnAgentEventOfItsOwn
TEST EventBusNeverInterpretsOrActsOnAnAgentEventPayload
TEST EventMatchesFilterReturnsTrueForANullFilterRegardlessOfEventContent
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.1, después de CH-09)

Constitution
 ├── Article III  — Component Sovereignty (EventBus: noveno componente instanciado; de los once
 │                   nombres que Article III enumera, solo AgentCore y SessionManager siguen preview)
 ├── Article IV   — Decision Ownership (EventBus, primer componente real sin fila propia — no
 │                   decide nada, solo distribuye)
 └── Article X    — Observability Constitution (los nueve consumidores nombrados tienen, por
                     primera vez, un mecanismo real de distribución hacia ellos)

Contracts (registry/contracts.yaml)
 ├── C-001 AgentMessage                (CH-00)
 ├── C-002 AgentConfig                 (CH-00)
 ├── C-003 AgentState                  (CH-00)
 ├── C-004 ExecutionContext            (CH-00)
 ├── C-005 ContextSnapshot             (CH-04)
 ├── C-006 ModelRequest                (CH-03)
 ├── C-007 ModelResponse               (CH-03)
 ├── C-008 ToolCall                    (CH-02)
 ├── C-009 ToolResult                  (CH-02)
 ├── C-010 AgentEvent                  (CH-00 — distribuido, por primera vez, desde CH-09)
 ├── C-011 HarnessError                (CH-00)
 ├── C-012 ExecutionBudget             (CH-00)
 ├── C-013 AgentRunStatus              (CH-01)
 ├── C-014 PolicyDecision              (CH-05)
 ├── C-015 HumanInteractionRequest     (CH-06)
 ├── C-016 HumanInteractionResolution  (CH-06)
 ├── C-017 ExecutionDecision           (CH-07)
 ├── C-018 CapabilityDescriptor        (CH-08)
 └── C-019 EventSubscription           (CH-09, nuevo)

Components (registry/components.yaml)
 ├── CMP-001 AgentLoop                 (CH-01)
 ├── CMP-002 ToolRuntime                (CH-02)
 ├── CMP-003 ModelGateway               (CH-03)
 ├── CMP-004 ContextEngine              (CH-04)
 ├── CMP-005 PolicyEngine               (CH-05)
 ├── CMP-006 HumanInteractionService    (CH-06)
 ├── CMP-007 ExecutionController        (CH-07)
 ├── CMP-008 CapabilityRegistry         (CH-08)
 └── CMP-009 EventBus                   (CH-09, nuevo — noveno componente, primero sin fila propia
                                          en Article IV, primero que no consume ExecutionContext)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado real de cada `EMIT` hacia `distributeEvent`**: ningún componente productor
  (`AgentLoop`..`CapabilityRegistry`) fue modificado para invocar de verdad `distributeEvent` cuando
  emite su `AgentEvent` — esta demostración autónoma prueba que el mecanismo funciona, no que ya
  esté conectado dentro de un `AgentRun` real.
- **El mecanismo real de alta/persistencia de una `EventSubscription`**: `subscriptions` llega, a
  `distributeEvent`, como parámetro ya poblado — este capítulo no modela dónde vive ese registro
  entre reinicios ni quién lo administra en producción, mismo patrón que `registeredCapabilities`
  en CH-08.
- **Autorización sobre quién puede suscribirse a qué**: seccion 15 ya lo señala explícitamente —
  ningún control de acceso sobre `subscriberRef` o sobre el `filter` que puede declarar.
- **Los nueve consumidores concretos de Article X**: `Logs`, `Tracing`, `Audit`, `Replay`,
  `Analytics`, `Evals`, `Cost Analysis`, `Debugging` y `UI` siguen sin componente propio en este
  registry — son consumidores conceptuales, cada uno representado, como mucho, por un
  `subscriberRef` opaco.
- **Garantías de entrega**: orden de entrega entre suscripciones, semántica ante un consumidor que
  falla al recibir (reintentos, backpressure, at-least-once vs. exactly-once) — `deliver` sigue
  siendo una primitiva asumida sin ninguna de estas garantías modeladas.
- **Reactivación de una `EventSubscription` cancelada**: no modelada — `cancelSubscription` es,
  deliberadamente, terminal.
- **Filtros adicionales de `EventFilter`** (`sessionId`, `agentId`, rango de `timestamp`): fuera de
  alcance, mismo argumento que seccion 6.
- **`SessionManager`, Provider Adapters reales, streaming real, `Channel Adapter` real, el pipeline
  de integración completo `AgentLoop → ModelGateway → CapabilityRegistry → PolicyEngine →
  ToolRuntime`**: deuda heredada de capítulos anteriores, sin cambios aquí.
- Reviewers plurales, evals y orquestación multi-agente: explícitamente fuera de alcance de BH-v0.1
  (igual que todos los capítulos anteriores).

## 19. Siguiente Incremento (Next Increment)

El problema natural del próximo capítulo: con nueve componentes reales ya existentes y un mecanismo
real de distribución de eventos instalado, de los once nombres que Article III enumera en su árbol
de "Agent Runtime" solo quedan dos sin componente propio: `AgentCore` (las primitives fundamentales
que coordinan todo lo demás) y `SessionManager` (persistencia durable de historial y checkpoints,
Article IV: "What execution history and checkpoints persist?" — una pregunta que, a diferencia de
`EventBus`, sí tiene fila propia en Article IV y sigue sin responderse con código real). Cualquiera
de los dos —o el capítulo de integración de punta a punta que CH-02..CH-08 fueron posponiendo,
capítulo a capítulo, en sus propias secciones 18— es un candidato real para el próximo incremento.

`next_chapter` queda en `null` en el frontmatter de este capítulo porque, en este momento del libro,
ese próximo capítulo todavía no existe como archivo — solo como el problema que motivaría su
escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg / Bucles
> de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows), secciones
> que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): la construcción `EMIT AgentEvent(...)` aparece quince
   veces en nueve archivos de capítulo, producida por ocho componentes distintos — y ninguna de esas
   quince apariciones tuvo jamás, hasta este capítulo, un destino real.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): un verbo de la
   gramática canónica del libro (`EMIT`) puede usarse correctamente, capítulo tras capítulo, sin que
   nadie repare en que nunca tuvo un mecanismo real detrás — porque cada componente productor solo
   necesitaba demostrar que construía bien su propio evento, nunca a quién se lo entregaba.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `EventBus` (CMP-009) con una ficha que declara tanto lo que posee (`owns`) como lo que
   explícitamente NO posee (`does_not_own`), y formaliza `EventSubscription` (C-019) — el sexto
   contrato del libro con un campo de filtro opcional embebido.
4. **Modelos mentales** (= §4, Constitutional Impact): el Ownership Rule de Article IV, aplicado
   aquí de forma inversa — la ausencia de `EventBus` en la tabla de Decision Ownership, no su
   presencia, es el modelo mental que este capítulo confirma con código real.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cuantos más de los nueve consumidores que Article X nombra
  existan sin un mecanismo real de distribución, más tentador resulta que cada uno, al construirse,
  invente su propio acoplamiento directo contra cada uno de los ocho componentes productores —
  multiplicando nueve consumidores por ocho productores en vez de sumarlos.
- **Bucle de equilibrio (estabiliza):** `distributeEvent` (§11) colapsa esa multiplicación en una
  sola relación por consumidor (`EventSubscription`) y ninguna llamada adicional por productor
  (`EMIT` sigue exactamente igual) — la razón clásica para introducir un bus de eventos.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `EventBus` (CMP-009) nunca decida qué
información contiene un `AgentEvent`, nunca lo interprete, y nunca emita su propio evento sobre el
hecho de haberlo distribuido — preservando exactamente la frontera que Article III traza entre
"producir" (los ocho componentes ya existentes) y "distribuir" (este capítulo). Si `EventBus`
cruzara esa frontera, dejaría de ser el "dumb pipe" desacoplado que Article III describe y empezaría
a absorber silenciosamente decisiones que pertenecen a otros dominios — exactamente el error que el
Ownership Rule de Article IV prohíbe.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo de
> esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set` (frontmatter) y
> es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa, para lectura directa
> del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Cuando un componente ya construye correctamente el hecho de que algo significativo ocurrió y lo
   declara mediante `EMIT`, ¿quién decide quién más se entera de que pasó, y qué tendría que existir
   para que esa pregunta tuviera una respuesta real? *(cierra la pregunta guía 1)*
2. ¿Debería cada componente que produce un hecho conocer, por nombre, a cada uno de los nueve
   consumidores de Article X? ¿Qué se rompe si la respuesta es "sí"? *(cierra la pregunta guía 2)*
3. Si a un consumidor solo le interesa un tipo de hecho entre dieciséis posibles, ¿en qué momento y
   con qué mecanismo se decide que no necesita enterarse de los otros quince? *(cierra la pregunta
   guía 3)*
4. ¿Qué necesita existir para que la decisión de un consumidor de "ya no más" quede registrada de
   forma explícita? *(cierra la pregunta guía 4)*

### Explicar

1. `EventBus` posee distribuir un `AgentEvent` ya producido hacia las suscripciones activas que
   hagan match. Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee decidir
   qué información va dentro de ese `AgentEvent`, aunque es literalmente quien lo entrega.
2. `EventSubscription.subscriberRef` es una referencia opaca, nunca un `STRUCT` propio para cada
   consumidor de Article X. Explica qué perderíamos si `EventBus` modelara en detalle cada tipo
   concreto de consumidor dentro de su propio registro.

### Conectar

1. `ToolRuntime` (CH-02) emite `TOOL_CALL_COMPLETED`/`TOOL_CALL_FAILED` sin modelar nunca a dónde va
   ese evento. ¿Qué construye este capítulo para que ese mismo `AgentEvent` pueda llegar a un
   consumidor real?
2. `PolicyEngine` (CH-05) emite `POLICY_EVALUATED` con una `PolicyDecision` como `payload`. ¿Qué
   mecanismo de este capítulo hace posible que un consumidor de auditoría se entere exactamente de
   ese hecho, y solo de ese hecho, sin que `PolicyEngine` sepa que la auditoría existe?

### Espaciar

Las cinco tarjetas de repaso de este capítulo (dos sobre `EventBus` — su `owns` y su `does_not_own`
—, una sobre su ausencia en Article IV, y dos sobre `EventSubscription` — sus campos, y por qué este
capítulo no agrega ningún valor a `AgentEventType`) entran hoy en `reviewStage = DAY_1`. Repásalas de
nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) — ver el apéndice de tarjetas al final del
libro (edición PDF) o `retrieval_set.flashcards` en `dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te equivocaste,
ese es precisamente el punto ciego que este método existe para revelar.
