---
id: CH-12
title: "Integración: el Camino Feliz de un AgentRun Completo"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: []
introduces_contracts: []
modifies_contracts: []
constitutional_articles: [P-04, P-05, P-10, P-12, P-13, INV-06, INV-07, INV-08, INV-09, INV-18, INV-19, INV-20]
previous_chapter: CH-11
next_chapter: CH-13
retrieval_set:
  expected_outcome:
    id: EO-CH12
    text: |
      Al terminar este capítulo podrás verificar, para cualquier ejecución completa de un agente
      que nunca requiere ni denegación ni aprobación humana, exactamente qué componente real
      resuelve cada paso del camino — desde que se solicita activarlo hasta que produce una
      respuesta final — y podrás diagnosticar, para cualquier par de componentes de este libro,
      si la señal que uno consume del otro sigue siendo una suposición aislada o si ya proviene de
      una llamada real dentro de una misma ejecución.
  skeleton:
    id: SK-CH12
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
    - id: GQ-CH12-01
      text: |
        Once componentes distintos demostraron, cada uno por su cuenta, una función real que
        recibía como parámetro una señal que en la práctica todavía nadie produce — un booleano
        suelto, una propuesta cruda sin resolver, un uso de presupuesto ya calculado. ¿Qué hace
        falta para que una sola ejecución real encadene esas once demostraciones en el orden
        correcto, en vez de dejarlas para siempre como piezas aisladas que nunca se tocan entre sí?
      answered_by: RQ-CH12-01
    - id: GQ-CH12-02
      text: |
        Un componente ya transiciona una ejecución hacia un punto de espera exacto cuando el
        modelo propone usar una herramienta, y se detiene ahí a propósito — sin que ningún
        capítulo, hasta ahora, haya mostrado cómo esa espera realmente termina con el resultado de
        esa herramienta ya ejecutada. ¿Qué necesita ocurrir, y en qué orden, para que ese punto de
        espera deje de ser un final sin resolver?
      answered_by: RQ-CH12-02
    - id: GQ-CH12-03
      text: |
        Una construcción de la gramática de este libro, reservada desde el primer capítulo para
        anunciar "esto ya ocurrió", aparece decenas de veces a lo largo de los capítulos
        anteriores — y ninguna de esas apariciones tuvo jamás un destino real. ¿Qué tendría que
        pasar, dentro de una ejecución real y no en una demostración aislada, para que cada una de
        esas apariciones por fin llegara a alguien?
      answered_by: RQ-CH12-03
    - id: GQ-CH12-04
      text: |
        Dos componentes distintos, cada uno con su propia pregunta ("¿está permitida esta acción
        concreta?" y "¿puede esta ejecución seguir existiendo frente a sus límites?"), nunca fueron
        invocados realmente por el componente que coordina el ciclo cognitivo ni por el que
        coordina la ejecución de una acción. ¿En qué punto exacto del camino debería consultarse
        cada uno, para que una acción o un turno nuevo solo ocurran después de que ambas preguntas
        ya se respondieron que sí?
      answered_by: RQ-CH12-04
  systems_lens:
    iceberg_visible_fact: |
      Después de once capítulos reales y veintiún contratos registrados, ningún archivo de este
      libro había mostrado nunca, de principio a fin, una sola ejecución completa de un agente:
      cada componente demostraba su propia función aislada, con señales de entrada asumidas en vez
      de con la salida real de su vecino (ver seccion 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite, ahora aplicado a la integración misma, es que cada capítulo cerró su
      propia demostración con la misma disciplina — "esto no invade el territorio del vecino" — y
      dejó, con la misma disciplina, una nota explícita en su seccion 18/19 señalando exactamente
      qué llamada real faltaba. Once notas de deuda, cada una honesta y acotada, nunca se
      convierten solas en una ejecución real: alguien tiene que, por fin, escribir el código que
      las conecta (ver seccion 3, Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo no instala un componente nuevo — instala, por primera vez, una función de
      integración (`runAgentTurnEndToEnd`, seccion 11) que invoca, en el orden correcto y con datos
      reales fluyendo entre sí, las funciones que los once capítulos anteriores ya publicaron:
      `activateAgent`/`beginAgentInitialization` (CH-11), `evaluateExecutionContinuation` (CH-07),
      `assembleContextSnapshot` (CH-04), `invokeModelForTurn` (CH-03), `runTurn` (CH-01),
      `resolveModelProposedToolCall` (CH-08), `evaluatePolicyForToolCall` (CH-05),
      `executeToolCall` (CH-02), `distributeEvent` (CH-09) y
      `createOrUpdateSessionCheckpoint` (CH-10) — sin modificar el código publicado de ninguno de
      los once (ver seccion 8, Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es que el Ownership Rule de Article IV nunca
      exigió que los componentes se ignoraran entre sí para siempre — exigió que cada uno declarara
      su frontera antes de que existiera código real que pudiera cruzarla. Una vez que las once
      fronteras ya están declaradas, componerlas en el orden correcto dentro de una única ejecución
      no viola ninguna de ellas: cada componente sigue haciendo, exactamente, lo que su propia
      ficha ya decía que hacía (ver seccion 4, Impacto Constitucional).
    reinforcing_loop: |
      Cada vez que un capítulo nuevo se escribió sin cablear realmente al anterior, la lista de
      "deuda intencional hacia el próximo capítulo" creció en vez de resolverse — once capítulos
      seguidos señalando el mismo problema desde ángulos distintos, sin que ninguno lo cerrara,
      porque cerrarlo no era su propio alcance decidido. Este capítulo corta esa espiral
      exactamente donde CH-11 §19 lo dejó anotado: con los once componentes ya reales, el
      problema natural ya no es introducir un componente más, es conectar los que ya existen.
    balancing_loop: |
      `runAgentTurnEndToEnd` (seccion 11) es el mecanismo de equilibrio: en cada punto de decisión
      (¿puede la ejecución continuar operacionalmente?, ¿está permitida esta acción?) verifica el
      resultado real antes de avanzar, y se detiene explícitamente — sin inventar el resto del
      camino — en cuanto ese resultado no es el camino feliz, dejando ese resto, con toda
      honestidad, para el capítulo que todavía no existe (ver seccion 18/19).
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que la integración se escriba como una
      función nueva y propia (`runAgentTurnEndToEnd`) que orquesta llamadas reales a las once
      funciones ya publicadas, en vez de reabrir y modificar el pseudocódigo ya publicado de
      cualquiera de los once capítulos anteriores. Si este capítulo hubiera editado, por ejemplo,
      la firma de `AgentLoop.runTurn` para que aceptara un `ModelResponse` directamente, habría
      alterado un contrato de comportamiento que once capítulos de lectores ya aprendieron —
      exactamente el tipo de estabilidad que este libro protege capítulo a capítulo.
  recall_questions:
    - id: RQ-CH12-01
      text: |
        ¿Qué nombre recibe la función de integración de este capítulo, y qué diez funciones ya
        publicadas invoca, en el orden correcto, para completar un `AgentRun` real de principio a
        fin?
    - id: RQ-CH12-02
      text: |
        Después de que `AgentLoop.runTurn` transiciona una ejecución a `WAITING_FOR_TOOL`, ¿qué
        tres funciones ya publicadas se invocan, en qué orden, antes de que la ejecución se
        retome — y con qué `AgentRunStatus` se construye el `AgentState` que representa esa
        reanudación?
    - id: RQ-CH12-03
      text: |
        ¿Qué función nueva de este capítulo le da, por primera vez, un destino real a cada `EMIT`
        que un componente ya publicado produce, y qué dos parámetros necesita para construir el
        `AgentEvent` equivalente y entregárselo a `EventBus`?
    - id: RQ-CH12-04
      text: |
        ¿Antes de qué dos operaciones, respectivamente, invoca este capítulo a
        `evaluateExecutionContinuation` y a `evaluatePolicyForToolCall`, y qué valor de cada
        resultado tiene que darse para que el camino feliz continúe en vez de detenerse ahí?
  explain_prompts:
    - id: EP-CH12-01
      text: |
        Este capítulo nunca modifica el pseudocódigo ya publicado de `AgentLoop.runTurn`
        (CH-01), aunque `runTurn` sigue recibiendo dos booleanos sueltos en vez de un
        `ModelResponse` completo. Explica, como si hablaras con alguien sin contexto técnico, cómo
        es posible que ese booleano ya no sea una suposición aislada sino un valor real, sin haber
        cambiado ni una línea de la función que lo recibe — ¿dónde vive exactamente esa
        transformación?
      target_entity: CMP-001
    - id: EP-CH12-02
      text: |
        `ToolRuntime.executeToolCall` (CH-02) sigue recibiendo `capabilityResolved` e `inputValid`
        como dos booleanos de entrada, exactamente como los recibía en su propio capítulo. Explica
        por qué, dentro de la función de integración de este capítulo, es correcto pasarle `TRUE`
        a ambos en vez de calcularlos de nuevo — ¿qué tuvo que ocurrir, unas líneas antes, para que
        esos dos `TRUE` ya no sean una suposición sino un hecho verificado?
      target_entity: CMP-002
  interleaved_questions:
    - id: IQ-CH12-01
      text: |
        `AgentCore.activateAgent` (CH-11) instancia el primer `AgentState` de un run nuevo, con
        `runId` recién minado — y `ToolRuntime.executeToolCall` (CH-02), varios pasos después
        dentro de la misma ejecución, coordina una acción concreta sobre el mundo externo. ¿Qué
        campo de `ExecutionContext`, construido una sola vez cerca del principio de la ejecución,
        tiene que sobrevivir sin cambiar hasta esa tool call para que ambos extremos de la
        ejecución puedan correlacionarse en una auditoría posterior?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-011, CMP-002, C-004]
      prior_chapter: CH-11
    - id: IQ-CH12-02
      text: |
        `ContextEngine.assembleContextSnapshot` (CH-04) registra la procedencia de cada fragmento
        que decide incluir, y `CapabilityRegistry.resolveToolCall` (CH-08) valida que los
        argumentos de una propuesta cumplan un schema declarado antes de producir cualquier
        intención de acción. ¿Qué tienen en común estas dos verificaciones, ambas ubicadas antes de
        que el modelo o una acción lleguen más lejos, y por qué ninguna de las dos podría
        colapsarse en la otra sin violar Article IV?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-004, CMP-008]
      prior_chapter: CH-04
    - id: IQ-CH12-03
      text: |
        `AgentLoop` (CH-01) decide si otro turno de razonamiento debe ocurrir; `ExecutionController`
        (CH-07) decide si la ejecución puede seguir existiendo frente a sus límites operacionales.
        ¿Cuál de las dos preguntas se responde primero dentro de una ejecución real, y qué pasaría
        si se invirtiera ese orden — si `AgentLoop` decidiera continuar antes de que
        `ExecutionController` confirmara que el presupuesto todavía lo permite?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-001, CMP-007]
      prior_chapter: CH-01
    - id: IQ-CH12-04
      text: |
        `ModelGateway.invoke` (CH-03) normaliza la respuesta del modelo hacia un `ModelResponse`
        cuyo `proposedToolCall` es, deliberadamente, una propuesta cruda sin validar — y
        `ToolRuntime.executeToolCall` (CH-02) exige que esa propuesta ya llegue como un `ToolCall`
        resuelto y validado. ¿Cuántos componentes distintos, y en qué orden, tienen que intervenir
        entre esos dos extremos para que la propuesta cruda de uno se convierta en la intención ya
        resuelta que el otro exige recibir?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-003, CMP-002]
      prior_chapter: CH-03
    - id: IQ-CH12-05
      text: |
        `EventBus.distributeEvent` (CH-09) puede entregar cualquier `AgentEvent` ya producido a
        cualquier suscripción activa que haga match — incluido, en principio,
        `HUMAN_INTERACTION_REQUESTED` (CH-06), un valor que este capítulo nunca llega a emitir
        porque su camino feliz nunca produce una `PolicyDecision` con `outcome = REQUIRE_APPROVAL`.
        ¿Qué tendría que ocurrir, en un capítulo todavía no escrito, para que ese evento en
        particular sí llegara a `distributeEvent` — y por qué `EventBus` no necesita cambiar ni una
        línea de su propio código para que eso funcione el día que ocurra?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-009, CMP-006]
      prior_chapter: CH-09
  flashcards:
    - id: FC-CH12-01
      front: |
        ¿Qué función nueva orquesta, por primera vez, un `AgentRun` completo de principio a fin —
        y qué NO hace ella misma, según la disciplina de Article IV?
      back: |
        `runAgentTurnEndToEnd` (seccion 11): invoca, en el orden correcto, las funciones ya
        publicadas de los once componentes de Article III. No decide nada por su cuenta — cada
        decisión (¿debe continuar el turno?, ¿puede seguir la ejecución?, ¿está permitida la
        acción?) sigue perteneciendo, exactamente igual que antes, al componente que ya la poseía.
      source_entity: CMP-001
      chapter_introduced_in: CH-12
      review_stage: DAY_1
    - id: FC-CH12-02
      front: |
        Después de que `runTurn` transiciona a `WAITING_FOR_TOOL`, ¿qué tres funciones se invocan,
        en orden, antes de que la ejecución se retome con `status = RUNNING`?
      back: |
        `resolveModelProposedToolCall` (CH-08, resuelve la propuesta cruda hacia un `ToolCall`
        real), `evaluatePolicyForToolCall` (CH-05, decide si esa acción está permitida) y, solo si
        `outcome = ALLOW`, `executeToolCall` (CH-02, coordina la ejecución real y produce el
        `ToolResult` que se convierte en la observación del siguiente turno).
      source_entity: CMP-008
      chapter_introduced_in: CH-12
      review_stage: DAY_1
    - id: FC-CH12-03
      front: |
        ¿Qué función nueva de este capítulo le da un destino real a cada `EMIT`, y qué hace
        exactamente?
      back: |
        `emitAndDistribute(eventType, execution, agentId, payload, activeSubscriptions)`: construye
        el `AgentEvent` equivalente al que el componente ya publicado produjo, y lo entrega a
        `EventBus.distributeEvent` (CH-09) — la primera vez que un `EMIT` de este libro llega
        realmente a alguien, dentro de una ejecución real y no en una demostración aislada.
      source_entity: CMP-009
      chapter_introduced_in: CH-12
      review_stage: DAY_1
    - id: FC-CH12-04
      front: |
        ¿En qué orden invoca este capítulo a `ExecutionController` y a `PolicyEngine` respecto de
        `AgentLoop` y `ToolRuntime`, respectivamente, y por qué ese orden no podría invertirse?
      back: |
        `evaluateExecutionContinuation` se invoca ANTES de `runTurn` (la ejecución debe poder
        seguir operacionalmente antes de que el ciclo cognitivo decida otro turno) y
        `evaluatePolicyForToolCall` se invoca ANTES de `executeToolCall` (una acción nunca se
        ejecuta antes de que se determine que está permitida). Invertir cualquiera de los dos
        órdenes dejaría ocurrir un turno o una acción antes de que la pregunta correspondiente de
        Article IV se respondiera.
      source_entity: CMP-007
      chapter_introduced_in: CH-12
      review_stage: DAY_1
    - id: FC-CH12-05
      front: |
        ¿Qué NO resuelve este capítulo, aunque los once componentes de Article III ya son reales?
      back: |
        `PolicyDecision.outcome = DENY` o `REQUIRE_APPROVAL`, y `ExecutionDecision.outcome = STOP`
        o `CANCELLED` — los caminos que terminan en una denegación, una aprobación humana pendiente
        o una terminación operacional. Este capítulo modela, exclusivamente, el camino feliz
        (`ALLOW`/`CONTINUE`); el resto queda como el problema del próximo capítulo (seccion 18/19).
      source_entity: CMP-005
      chapter_introduced_in: CH-12
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH12-01
      recall_question: RQ-CH12-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH12-02
      recall_question: RQ-CH12-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH12-03
      recall_question: RQ-CH12-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH12-04
      recall_question: RQ-CH12-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 12 — Integración: el Camino Feliz de un AgentRun Completo

> **Regla constitucional (Article IV, Ownership Rule):** ningún componente debe absorber
> silenciosamente decisiones que pertenecen a otro dominio — ni siquiera el capítulo que, por
> primera vez, los conecta a todos.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1. El detalle
> estructurado de esta sección vive en `retrieval_set` (frontmatter) y es lo que
> `scripts/validate-retrieval-set` valida automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás verificar, para cualquier ejecución
completa de un agente que nunca requiere ni denegación ni aprobación humana, exactamente qué
componente real resuelve cada paso del camino — desde que se solicita activarlo hasta que produce
una respuesta final — y podrás diagnosticar, para cualquier par de componentes de este libro, si
la señal que uno consume del otro sigue siendo una suposición aislada o si ya proviene de una
llamada real dentro de una misma ejecución.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) y **no
introduce ningún contrato ni ningún componente nuevo** — es el primer capítulo de este libro que es
pura composición: invoca, con datos reales fluyendo entre sí, las funciones que los once
capítulos anteriores ya publicaron y ya registraron.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar
atrás; están formuladas en lenguaje de problema):

1. Once componentes distintos demostraron, cada uno por su cuenta, una función real que recibía
   como parámetro una señal que en la práctica todavía nadie produce. ¿Qué hace falta para que una
   sola ejecución real encadene esas once demostraciones en el orden correcto?
2. Un componente ya transiciona una ejecución hacia un punto de espera exacto cuando el modelo
   propone usar una herramienta, y se detiene ahí a propósito. ¿Qué necesita ocurrir, y en qué
   orden, para que ese punto de espera deje de ser un final sin resolver?
3. Una construcción de la gramática de este libro, reservada desde el primer capítulo para
   anunciar "esto ya ocurrió", aparece decenas de veces sin destino real. ¿Qué tendría que pasar
   para que cada una de esas apariciones por fin llegara a alguien?
4. Dos componentes distintos, cada uno con su propia pregunta, nunca fueron invocados realmente
   por quien coordina el ciclo cognitivo ni por quien coordina la ejecución de una acción. ¿En qué
   punto exacto del camino debería consultarse cada uno?

## 1. Arquitectura Actual (Current Architecture)

CH-00 dejó siete contratos fundacionales. CH-01..CH-11 instanciaron, uno por uno, los once
componentes que `constitution/ARCHITECTURE_CONSTITUTION.md` Article III enumera en su árbol de
"Agent Runtime" — `AgentLoop` (CH-01), `ToolRuntime` (CH-02), `ModelGateway` (CH-03),
`ContextEngine` (CH-04), `PolicyEngine` (CH-05), `HumanInteractionService` (CH-06),
`ExecutionController` (CH-07), `CapabilityRegistry` (CH-08), `EventBus` (CH-09), `SessionManager`
(CH-10) y `AgentCore` (CH-11) — y catorce contratos adicionales, para un total de veintiún
contratos registrados (`C-001`..`C-021`) y once componentes registrados (`CMP-001`..`CMP-011`).
Con CH-11, ninguno de los once nombres de Article III sigue siendo únicamente una palabra en una
tabla de preview.

Pero cada uno de esos once capítulos, con la misma disciplina, hizo dos cosas a la vez: demostró
su propia función con pseudocódigo real, y **aisló** esa demostración de sus vecinos mediante
señales de entrada asumidas — un booleano suelto (`modelFinished`, `capabilityResolved`,
`argumentsMatchSchema`), un resultado ya calculado (`ExecutionUsage`, `registeredCapabilities`), o
una construcción de la gramática (`EMIT`) sin ningún destino real. La sección 18/19 de cada uno de
esos once capítulos documentó, explícitamente, cuál era esa señal y qué componente, todavía sin
existir o ya existente pero no invocado, tendría que producirla de verdad. CH-11 §19 lo resumió
así, al cerrar el último componente de Article III: "el problema natural del próximo incremento ya
no es introducir un componente nuevo: es el capítulo de integración de punta a punta que CH-02..
CH-10 fueron posponiendo, capítulo a capítulo".

Concretamente, este capítulo hereda nueve deudas puntuales, cada una citada por nombre en el
capítulo que la dejó pendiente:

1. **CH-11 → CH-01.** `AgentCore.beginAgentInitialization` produce un `AgentState` con
   `status = INITIALIZING` y nunca lo entrega a `AgentLoop.runTurn` — nadie completa la transición
   `INITIALIZING → RUNNING` ni invoca `runTurn` por primera vez sobre ese run (CH-11 §18).
2. **CH-01 → CH-03.** `AgentLoop.runTurn` decide la transición del turno a partir de dos
   booleanos sueltos (`modelFinished`, `modelProposesToolCall`) — "señales de entrada asumidas...
   que un componente todavía sin construir (`ModelGateway`) produciría en la realidad" (CH-01
   §11/§18), nunca a partir de un `ModelResponse` real.
3. **CH-04 → CH-03.** `ContextEngine.assembleContextSnapshot` produce un `ContextSnapshot.blocks`
   ya seleccionado y compactado, pero "`ContextSnapshot.blocks` todavía no se cablea formalmente
   hacia `ModelRequest.messages`" (CH-04 §18) — nadie construye los `AgentMessage` reales que
   `ModelGateway` necesitaría a partir de ese resultado.
4. **CH-03 → CH-08.** `ModelResponse.proposedToolCall` es, por diseño, una `RawToolCallProposal`
   cruda — y `CapabilityRegistry.resolveModelProposedToolCall` (CH-08 §11) solo la resolvió, hasta
   ahora, "de forma completamente autónoma" con un `ModelResponse` de ejemplo, nunca dentro de un
   turno real producido por `ModelGateway`.
5. **CH-05 → CH-02.** `ToolRuntime.executeToolCall` recibe `capabilityResolved`/`inputValid` como
   señales ya dadas y "nunca evalúa si la acción que va a coordinar está autorizada — su propio
   `does_not_own` lo excluye explícitamente, pero sin un componente real que sí lo haga, INV-06...
   sigue siendo una regla declarada, no una regla exigida por código" (CH-05 §3).
6. **CH-07 → CH-01.** `ExecutionController.evaluateExecutionContinuation` nunca es invocada por
   `AgentLoop.runTurn` — "`runTurn` no verifica ningún presupuesto; ese cableado es,
   explícitamente, trabajo de un capítulo de integración futuro" (CH-07 §9).
7. **CH-02 → CH-01 (INV-07).** `AgentLoop.runTurn` transiciona a `WAITING_FOR_TOOL` y se detiene
   ahí — "un **handoff sin resolver**" (CH-01 §5) — y aunque `ToolRuntime.executeToolCall` ya
   produce un `ToolResult` real desde CH-02, "conectarlo con `runTurn` para que `AgentLoop` retome
   el ciclo (INV-07) es trabajo explícito de un capítulo posterior" (CH-02 §18).
8. **CH-09 → CH-00..CH-08.** Los quince `EMIT AgentEvent(...)` que CH-00..CH-08 ya producían
   correctamente "nunca tienen, hasta este capítulo, ningún destino real" (CH-09 §2) —
   `EventBus.distributeEvent` (CH-09 §11) solo se demostró con eventos de ejemplo.
9. **CH-10 → CH-01.** `SessionManager.createOrUpdateSessionCheckpoint` nunca es invocada al cierre
   de un turno — "que `AgentLoop` invoque de verdad `createOrUpdateSessionCheckpoint` después de
   cada turno es, explícitamente, trabajo de un capítulo de integración futuro" (CH-10 §9).

Explícitamente **fuera** de esta lista — y fuera del alcance de este capítulo (ver seccion 3 y
seccion 18) — quedan los caminos que CH-05/CH-06/CH-07 dejaron modelados pero deliberadamente sin
cablear: `PolicyDecision.outcome = DENY` o `REQUIRE_APPROVAL` (y, en ese segundo caso, todo el
ciclo de `HumanInteractionService`, CH-06), y `ExecutionDecision.outcome = STOP` o `CANCELLED`.

## 2. El Problema (Problem)

Con los once componentes ya reales, el problema deja de ser "falta un componente" — cada pregunta
de Article IV ya tiene, desde CH-11, un dueño real que la responde con pseudocódigo ejecutable. El
problema es distinto y más simple de enunciar, aunque no de resolver: **nadie ha visto, todavía,
una sola ejecución de un agente correr de principio a fin**. Cada capítulo demostró su propio
tramo con datos de ejemplo, aislado a propósito de sus vecinos — la disciplina correcta para
introducir un componente nuevo sin invadir el territorio de otro que todavía no existía. Pero esa
misma disciplina, aplicada once veces seguidas, deja como resultado once islas correctas que nunca
se tocan entre sí. `AgentLoop.runTurn` nunca ha recibido, ni una sola vez en este libro, un
`ModelResponse` real. `ToolRuntime.executeToolCall` nunca ha sido invocada después de que
`PolicyEngine` la autorizara de verdad. `EventBus.distributeEvent` nunca ha distribuido un evento
que otro componente, dentro de la misma ejecución, produjo de verdad.

Necesitamos, por fin, una traza real: una función que tome una solicitud de activación y la lleve,
componente por componente, hasta una respuesta final — sin inventar ningún componente nuevo, sin
modificar el pseudocódigo ya publicado de ninguno de los once existentes, y sin fingir que el
camino de denegación o de aprobación humana también quedan resueltos cuando, honestamente, no es
así todavía.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los veintiún contratos y los once componentes que existen hasta este punto no bastan porque,
literalmente, cada uno de ellos lo dice de sí mismo en su propia sección 18/19 (ver seccion 1, la
lista completa de nueve deudas puntuales). Ninguna de esas notas es un descuido: cada una es la
misma disciplina de *ownership* aplicada con honestidad — un componente que declara "esto no me
pertenece a mí" no puede, al mismo tiempo, escribir el código que lo conecta con quien sí lo
posee, porque ese código pertenece a una decisión distinta: **la de secuenciar**, no la de decidir.
Article IV nunca asignó esa decisión de secuenciar a ninguno de los once componentes — y por eso
seguía sin resolverse después de CH-11.

Tres huecos adicionales, más allá de las nueve deudas puntuales, confirman que la arquitectura
actual (once componentes correctos, pero nunca ejercitados juntos) no basta:

- `AgentRunStatus.WAITING_FOR_TOOL` (C-013, CH-01) es, después de once capítulos, un estado que
  ningún pseudocódigo de este libro ha visto resolverse hacia `RUNNING` con una observación real —
  solo documentado en prosa como "Preview" desde CH-01 §12, repetido sin cerrar en CH-02 §12, CH-03
  §12 y CH-08 §12.
- Ningún componente, hasta este capítulo, ha construido jamás un `AgentMessage` a partir de un
  `ContextBlock` ya ensamblado — `ModelRequest.messages` (CH-03) y `ContextSnapshot.blocks` (CH-04)
  siguen siendo dos resultados que ningún pseudocódigo real conecta.
- `EventSubscription` (C-019, CH-09) nunca recibió, hasta este capítulo, un `AgentEvent` que no
  fuera un dato de ejemplo construido dentro de la propia sección 11 de CH-09.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la
> secuencia `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una
> entidad que no haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT`
> registrado — **no magic entities**. Este capítulo aplica esa misma disciplina en su forma más
> estricta hasta ahora: no define ni un solo `STRUCT`/`ENUM`/`COMPONENT` nuevo (más allá de
> redeclarar, sin cambios, un `ENUM` ya existente — ver seccion 6) — cada entidad que su
> pseudocódigo utiliza ya estaba registrada antes de que este capítulo se escribiera.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-04   Every action produces observable events.
           Hasta este capítulo, se cumplía solo a medias (cada componente construía el evento,
           pero EventBus nunca lo distribuía dentro de una ejecución real). runAgentTurnEndToEnd
           (seccion 11) es la primera vez que un AgentEvent producido dentro de un turno real llega
           de verdad a distributeEvent (CH-09).
    P-05   Side effects pass through policy.
           Primera vez que este principio se cumple dentro de una ejecución real de principio a
           fin: executeToolCall (CH-02) nunca se invoca en este capítulo sin que
           evaluatePolicyForToolCall (CH-05) ya haya decidido outcome = ALLOW primero.
    P-10   The harness owns execution state—not the model.
           El AgentState atraviesa, dentro de una sola ejecución real, CREATED → INITIALIZING →
           RUNNING → WAITING_FOR_TOOL → RUNNING → COMPLETED — cada transición decidida por
           AgentCore o AgentLoop, nunca por el modelo, y nunca inventada por este capítulo.
    P-12   Events observe; hooks intervene.
           Cada AgentEvent que este capítulo distribuye sigue siendo, exactamente, el que su
           componente productor ya construía — este capítulo nunca le agrega ni le quita campos.
    P-13   Authorization is deterministic and external to the LLM.
           evaluatePolicyForToolCall (CH-05) se invoca sobre un ToolCall ya resuelto por
           CapabilityRegistry (CH-08), nunca sobre la RawToolCallProposal cruda que el modelo
           propuso — la autorización sigue sin depender de ninguna entrada del modelo.

Invariants preserved
    INV-06   Todo side effect pasa por PolicyEngine.
             Primera cita literal con ejecución real de punta a punta: PolicyEngine se invoca
             antes de ToolRuntime en cada tool call de este capítulo, para el caso outcome = ALLOW.
    INV-07   Todo ToolResult vuelve al ciclo del agente como observación explícita cuando el
             lifecycle continúa.
             Primera cita literal con ejecución real: el ToolResult que executeToolCall produce se
             convierte en un AgentMessage real, incluido en el ContextSnapshot del turno siguiente.
    INV-08   El harness es propietario del execution state.
             Cada transición de AgentRunStatus de este capítulo la decide AgentCore o AgentLoop —
             nunca el modelo, ni siquiera indirectamente.
    INV-09   Todo AgentRun tiene límites explícitos.
             Primera cita literal con ejecución real: evaluateExecutionContinuation (CH-07) se
             invoca antes de cada turno, y el camino feliz de este capítulo modela exclusivamente
             outcome = CONTINUE.
    INV-18   Toda acción significativa produce un evento observable.
             Ya no solo "construido" (como hasta CH-11): distributeEvent (CH-09) entrega, dentro de
             este capítulo, cada AgentEvent real a las suscripciones activas que hagan match.
    INV-19   Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy relevante.
             El mismo ExecutionContext (mismo runId/sessionId/traceId) atraviesa, sin cambiar, cada
             una de las once invocaciones de este capítulo — la trazabilidad de punta a punta que
             once capítulos aislados nunca pudieron demostrar juntos.
    INV-20   Todo error operacional pertenece a una categoría conocida.
             Este capítulo no introduce ningún código de error nuevo — reutiliza, sin cambios, los
             ya declarados por CH-00..CH-11 (ver seccion 13).

Component ownership changes
    Ninguno. introduces_components: [] — este capítulo no instala ningún componente nuevo, y no
    modifica ni un solo campo owns/does_not_own/consumes/produces/dependencies de ninguna de las
    once fichas ya registradas en registry/components.yaml.

Lifecycle changes
    Ninguna modificación a AgentRunStatus (C-013). Este capítulo es, en cambio, el primero en
    ejercitar con pseudocódigo real la secuencia COMPLETA CREATED → INITIALIZING → RUNNING →
    WAITING_FOR_TOOL → RUNNING → COMPLETED dentro de una sola ejecución — cada tramo de esa
    secuencia ya estaba documentado por separado (CH-01/CH-11), nunca recorrido de punta a punta.

Security implications
    Este capítulo nunca ejecuta una acción sin que PolicyEngine ya la haya evaluado con
    outcome = ALLOW — pero modela exclusivamente ese resultado. Ver seccion 15 para el análisis
    completo de lo que deliberadamente queda fuera (DENY, REQUIRE_APPROVAL, STOP, CANCELLED).

Observability implications
    Primer capítulo que demuestra, con pseudocódigo real, que un AgentEvent producido por un
    componente puede recorrer un camino real hasta EventBus y desde ahí hasta una suscripción
    activa — cerrando, para el camino feliz, el hueco que CH-09 documentó como el problema central
    de su propio capítulo.

Deterministic vs agentic boundary
    Article XII no se refina de forma nueva aquí: este capítulo no introduce ningún componente que
    consuma una entrada del modelo por primera vez. Lo que sí demuestra, por primera vez, es que la
    frontera que cada uno de los once componentes ya trazaba por separado se preserva intacta
    cuando esos once componentes se ejecutan juntos, en el orden real — ninguna frontera se
    disuelve al componerlas.
```

## 5. Conceptos Nuevos (New Concepts)

Este capítulo no introduce ningún concepto que amerite una entrada propia en
`registry/glossary.yaml` (que este capítulo, deliberadamente, no toca — ver seccion 9). Introduce,
en cambio, dos ideas puramente narrativas, útiles para leer la seccion 11, que no se registran como
vocabulario canónico del libro:

- **Camino feliz (Allow Path)**: la traza de un `AgentRun` en la que cada punto de decisión
  binaria/ternaria del libro (`PolicyDecision.outcome`, `ExecutionDecision.outcome`) resuelve hacia
  su valor más permisivo (`ALLOW`, `CONTINUE`) — nunca hacia `DENY`, `REQUIRE_APPROVAL`, `STOP` ni
  `CANCELLED`. Es el único camino que este capítulo modela con pseudocódigo real (seccion 11); los
  demás quedan, honestamente, para el capítulo que todavía no existe (seccion 18/19).
- **Cierre de cableado (Wire Closure)**: el acto de que una función de integración invoque
  realmente, con datos reales, una llamada que un capítulo anterior dejó documentada como
  pendiente en su propia sección 18/19 — sin modificar el código ya publicado de ninguno de los dos
  extremos de esa llamada. Las nueve deudas puntuales de la seccion 1 son, cada una, un cierre de
  cableado distinto que este capítulo realiza.

Ninguna de las dos ideas anteriores es una responsabilidad nueva que algún componente deba `owns`:
son, simplemente, la forma de describir en prosa lo que `runAgentTurnEndToEnd` (seccion 11) hace.

## 6. Nuevas Estructuras de Datos (New Data Structures)

**Este capítulo no introduce ningún `STRUCT` ni `ENUM` nuevo.** Reutiliza, sin modificar ni un solo
campo, los contratos ya registrados desde CH-00..CH-11: `AgentActivationRequest` (C-021),
`AgentConfig` (C-002), `AgentState` (C-003), `ExecutionContext` (C-004), `ExecutionBudget` (C-012),
`ContextSnapshot` (C-005), `AgentMessage` (C-001), `ModelResponse` (C-007), `ToolCall` (C-008),
`PolicyDecision` (C-014), `ToolResult` (C-009), `ExecutionDecision` (C-017),
`CapabilityDescriptor` (C-018), `EventSubscription` (C-019), `SessionState` (C-020) y `AgentEvent`
(C-010).

### `ExecutionUsage` — disponible por referencia, no por redefinición

`ExecutionUsage` (CH-07 §6) es un `STRUCT` embebido dentro de `ExecutionDecision` (C-017), sin
contrato `C-XXX` propio — el mismo patrón que `RawToolCallProposal` (CH-03) o `ContextBlock`
(CH-04). El pseudocódigo de la seccion 11 lo necesita como tipo explícito de un parámetro (para
invocar `evaluateExecutionContinuation`, CH-07), así que este capítulo lo documenta aquí, por
referencia, siguiendo exactamente el mismo mecanismo que CH-08 §6 ya usó para `RawToolCallProposal`
— citarlo en una tabla, sin redefinir su `STRUCT`:

| Identificador (heredado de CH-07, sin `C-XXX` propio) | Rol en este capítulo |
|---|---|
| `ExecutionUsage` | tipo del parámetro `usage` que este capítulo pasa, ya dado, a `evaluateExecutionContinuation` (CH-07) — el mismo `STRUCT` de seis campos (`toolCallsUsed`, `inputTokensUsed`, `outputTokensUsed`, `costUsed`, `runtimeMsElapsed`, `concurrentToolsInFlight`) que CH-07 §6 ya definió, sin cambios |

### `AgentEventType` — redeclarado, sin agregar ningún valor

CH-11 dejó `AgentEventType` en veinte valores (el último capítulo en agregar alguno fue CH-10, con
los cuatro `SESSION_*`). Este capítulo necesita el nombre `AgentEventType` disponible como tipo
explícito dentro de `emitAndDistribute` (seccion 11, el parámetro `eventType`), así que lo
redeclara aquí — exactamente igual que CH-11 §14 ya redeclaró el mismo `ENUM` sin agregar ningún
valor nuevo:

```pseudocode
ENUM AgentEventType
    RUN_STARTED
    TURN_CONTINUED
    RUN_COMPLETED
    RUN_FAILED
    TOOL_CALL_COMPLETED
    TOOL_CALL_FAILED
    MODEL_RESPONSE_RECEIVED
    MODEL_INVOCATION_FAILED
    CONTEXT_SNAPSHOT_ASSEMBLED
    CONTEXT_SNAPSHOT_FAILED
    POLICY_EVALUATED
    HUMAN_INTERACTION_REQUESTED
    HUMAN_INTERACTION_RESOLVED
    EXECUTION_EVALUATED
    CAPABILITY_RESOLVED
    CAPABILITY_RESOLUTION_FAILED
    SESSION_CHECKPOINT_CREATED
    SESSION_RECONSTRUCTED
    SESSION_BRANCHED
    SESSION_PERSISTENCE_FAILED
END
```

`AgentEvent` (C-010) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — y el rango de
valores permitido para `eventType` tampoco crece en este capítulo. Ninguno de los veinte valores es
nuevo; este capítulo solo necesita poder escribir `eventType: AgentEventType` como tipo explícito
en una firma, y `scripts/validate-chapter` exige que todo tipo así usado esté definido en algún
bloque de este mismo capítulo o ya registrado — `AgentEventType` no tiene contrato `C-XXX` propio,
así que la única forma de dejarlo disponible es redeclararlo, sin cambios, tal como CH-09 y CH-11
ya hicieron cada uno por su cuenta.

**Unchanged**: ningún otro tipo heredado cambia de forma. Este capítulo no introduce ningún
identificador nuevo (a diferencia de CH-02, CH-06, CH-08, CH-09, CH-10 y CH-11, cada uno de los
cuales sí introdujo al menos un `Xxx­Id` opaco nuevo) — la única primitiva de generación de
identificador nueva de este capítulo es `newMessageId()` (seccion 11), en el mismo espíritu que
`newToolCallId()` (CH-08) o `newSessionCheckpointId()` (CH-10): no es una entidad arquitectónica,
no requiere ficha ni registro.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

**Este capítulo no introduce ningún contrato nuevo.** `introduces_contracts: []` en el
frontmatter — y, a diferencia de CH-00..CH-11, esta sección no tiene ninguna ficha de Contract
Registry que agregar. `registry/contracts.yaml` permanece, después de este capítulo, exactamente
en los veintiún contratos que CH-11 dejó registrados (`C-001`..`C-021`).

## 8. Responsabilidades de Componentes (Component Responsibilities)

**Este capítulo no introduce ningún componente nuevo.** `introduces_components: []` en el
frontmatter — `registry/components.yaml` permanece, después de este capítulo, exactamente en los
once componentes que CH-11 dejó registrados (`CMP-001`..`CMP-011`), sin que ninguna de sus once
fichas cambie un solo campo (`owns`, `does_not_own`, `consumes`, `produces`, `dependencies`).

Lo que este capítulo sí hace, en su lugar, es mostrar — con una función nueva y propia,
`runAgentTurnEndToEnd` (seccion 11), que **no** es un método de ningún componente registrado — el
orden real en que los once componentes se invocan entre sí dentro de una sola ejecución:

```text
Orden de invocación real dentro de runAgentTurnEndToEnd (camino feliz)

1.  AgentCore.activateAgent                    (CH-11) → AgentState (CREATED)
2.  AgentCore.beginAgentInitialization         (CH-11) → AgentState (INITIALIZING)
    [este capítulo construye el ExecutionContext y transiciona a RUNNING — ver seccion 11]
3.  ExecutionController.evaluateExecutionContinuation (CH-07) → ExecutionDecision (CONTINUE)
4.  ContextEngine.assembleContextSnapshot       (CH-04) → ContextSnapshot
5.  ModelGateway.invokeModelForTurn             (CH-03) → ModelResponse
6.  AgentLoop.runTurn                            (CH-01) → AgentState (WAITING_FOR_TOOL)
7.  SessionManager.createOrUpdateSessionCheckpoint (CH-10) → SessionState
8.  CapabilityRegistry.resolveModelProposedToolCall (CH-08) → ToolCall
9.  PolicyEngine.evaluatePolicyForToolCall       (CH-05) → PolicyDecision (ALLOW)
10. ToolRuntime.executeToolCall                  (CH-02) → ToolResult
    [este capítulo construye la observación y transiciona de vuelta a RUNNING — ver seccion 11]
11. ExecutionController.evaluateExecutionContinuation (CH-07) → ExecutionDecision (CONTINUE)
12. ContextEngine.assembleContextSnapshot       (CH-04) → ContextSnapshot (con la observación)
13. ModelGateway.invokeModelForTurn             (CH-03) → ModelResponse (finished = TRUE)
14. AgentLoop.runTurn                            (CH-01) → AgentState (COMPLETED)
15. SessionManager.createOrUpdateSessionCheckpoint (CH-10) → SessionState

En cada uno de los quince pasos anteriores, EventBus.distributeEvent (CH-09) entrega el
AgentEvent correspondiente a las suscripciones activas que hagan match — ver seccion 11/14.
```

Cada una de las once fichas ya publicadas se respeta exactamente: `AgentLoop` sigue sin decidir
autorización ni ejecutar tools; `ToolRuntime` sigue sin evaluar policy ni presupuesto;
`PolicyEngine` sigue sin ejecutar la acción que autoriza; `ExecutionController` sigue sin decidir
continuación cognitiva; `EventBus` sigue sin decidir qué contiene un evento. Ninguna decisión
cambió de dueño — solo se invocó, por primera vez, en el orden real.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
runAgentTurnEndToEnd (función de integración, no un componente registrado)
    invoca → activateAgent, beginAgentInitialization (CMP-011)
    invoca → evaluateExecutionContinuation (CMP-007)
    invoca → assembleContextSnapshot (CMP-004)
    invoca → invokeModelForTurn (CMP-003)
    invoca → runTurn (CMP-001)
    invoca → resolveModelProposedToolCall (CMP-008)
    invoca → evaluatePolicyForToolCall (CMP-005)
    invoca → executeToolCall (CMP-002)
    invoca → createOrUpdateSessionCheckpoint (CMP-010)
    invoca → distributeEvent (CMP-009)
```

**Límite real de este capítulo, documentado con honestidad.** `registry/components.yaml` **no se
modifica**: ninguna de las once fichas agrega, en su propio campo `dependencies`, a ninguno de sus
vecinos — el encargo de este capítulo prohíbe explícitamente editar la ficha de una entidad ya
existente, y este capítulo lo respeta. Esto tiene una consecuencia real y verificable en
`diagrams/mindmap/chapter-12.diagram` (ver seccion 17): el `BookMindMap` deriva sus aristas
`DEPENDS_ON`/`PRODUCES`/`CONSUMES` **exclusivamente** de los campos `dependencies`/`produces`/
`consumes` que cada componente ya declaraba en el capítulo en que se introdujo
(`scripts/lib/mindmap.js`, ver comentario de cabecera del archivo) — nunca de la prosa ni del
pseudocódigo de un capítulo posterior que simplemente invoca esas funciones. El grafo mecánico del
libro, tal como está construido hoy, no tiene ningún mecanismo para que un capítulo de integración
como este agregue aristas `DEPENDS_ON`/`PRODUCES`/`CONSUMES` nuevas sin editar la ficha de un
componente ya existente — y este capítulo, por instrucción explícita, no la edita. La seccion 17 y
el plan de ejecución de este capítulo documentan la cifra real verificada, no una cifra deseada.

En prosa, entonces (nunca como una arista nueva del grafo mecánico), las relaciones que este
capítulo sí ejercita por primera vez con código real son exactamente las quince invocaciones de la
seccion 8 — la integración vive en `runAgentTurnEndToEnd`, no en `registry/components.yaml`.

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
AgentCore → ExecutionController → ContextEngine → ModelGateway → AgentLoop → SessionManager
    → CapabilityRegistry → PolicyEngine → ToolRuntime
    → ExecutionController → ContextEngine → ModelGateway → AgentLoop → SessionManager
(EventBus recibe, en cada paso anterior, el AgentEvent correspondiente — fan-out hacia
Logs/Tracing/Audit/... conceptuales, Article X, sin componente propio todavía)
```

**Vista 2 — Sequence**

```text
AgentActivationRequest
   │
   ▼
AgentCore
   │ activateAgent → AgentState(CREATED)
   │ beginAgentInitialization → AgentState(INITIALIZING); EMIT RUN_STARTED → EventBus
   │ [este capítulo transiciona a RUNNING]
   ▼
ExecutionController
   │ evaluateExecutionContinuation → ExecutionDecision(CONTINUE); EMIT EXECUTION_EVALUATED → EventBus
   ▼
ContextEngine
   │ assembleContextSnapshot → ContextSnapshot; EMIT CONTEXT_SNAPSHOT_ASSEMBLED → EventBus
   │ [este capítulo construye AgentMessage a partir de cada ContextBlock]
   ▼
ModelGateway
   │ invokeModelForTurn → ModelResponse(finished=FALSE, proposedToolCall≠NULL)
   │ EMIT MODEL_RESPONSE_RECEIVED → EventBus
   ▼
AgentLoop
   │ runTurn(modelFinished=FALSE, modelProposesToolCall=TRUE) → AgentState(WAITING_FOR_TOOL)
   │ EMIT TURN_CONTINUED → EventBus
   ▼
SessionManager
   │ createOrUpdateSessionCheckpoint → SessionState; EMIT SESSION_CHECKPOINT_CREATED → EventBus
   ▼
CapabilityRegistry
   │ resolveModelProposedToolCall → ToolCall; EMIT CAPABILITY_RESOLVED → EventBus
   ▼
PolicyEngine
   │ evaluatePolicyForToolCall → PolicyDecision(ALLOW); EMIT POLICY_EVALUATED → EventBus
   ▼
ToolRuntime
   │ executeToolCall → ToolResult; EMIT TOOL_CALL_COMPLETED → EventBus
   │ [este capítulo construye la observación y transiciona de vuelta a RUNNING]
   ▼
ExecutionController → ContextEngine → ModelGateway → AgentLoop
   │ (mismo patrón; esta vez ModelResponse(finished=TRUE) → AgentState(COMPLETED))
   │ EMIT RUN_COMPLETED → EventBus
   ▼
SessionManager
   │ createOrUpdateSessionCheckpoint → SessionState final; EMIT SESSION_CHECKPOINT_CREATED → EventBus
   ▼
AgentState (COMPLETED) — el AgentRun terminó, de principio a fin, con código real en cada paso
```

**Vista 3 — Pseudocódigo**

Ver §11: `runAgentTurnEndToEnd` es la primera formalización ejecutable, en todo este libro, de un
`AgentRun` completo — construida exclusivamente a partir de funciones ya publicadas por
CH-01..CH-11, sin modificar ninguna.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya registradas desde CH-00..CH-11, más `ExecutionUsage` y
`AgentEventType` (ver seccion 6, disponibles por referencia/redeclaración, no por introducción).

```pseudocode
FUNCTION emitAndDistribute(
    eventType: AgentEventType,
    execution: ExecutionContext,
    agentId: AgentId,
    payload: Value,
    activeSubscriptions: List<EventSubscription>
) -> List<EventSubscription>

    event: AgentEvent = AgentEvent(
        eventId = newEventId(),
        eventType = eventType,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = payload
    )

    RETURN distributeEvent(event, activeSubscriptions)
END
```

`emitAndDistribute` es la respuesta de este capítulo a la deuda #8 de la seccion 1: la gramática
canónica (`EMIT`, `skills/write-pseudocode/SKILL.md`) nunca definió un canal de retorno para lo que
emite — cada componente productor (CH-01..CH-08, CH-10, CH-11) construye su propio `AgentEvent` y
lo declara con `EMIT` dentro de su propia función, sin que esa función devuelva el evento a quien
la invocó. Este capítulo no puede — ni necesita — capturar el `AgentEvent` interno que, por
ejemplo, `runTurn` ya emite: en su lugar, reconstruye el evento equivalente (mismo `eventType`, el
mismo `execution`/`agentId` que ya comparte con la llamada que acaba de hacer, y el mismo `payload`
que esa llamada le devolvió) y lo entrega, explícitamente, a `distributeEvent` (CH-09). Es la
primera vez que este libro muestra, con código real, que un `EMIT` puede tener un destino.

```pseudocode
FUNCTION runAgentTurnEndToEnd(
    request: AgentActivationRequest,
    registeredCapabilities: List<CapabilityDescriptor>,
    activeSubscriptions: List<EventSubscription>,
    usage: ExecutionUsage,
    proposedCapabilityName: Text,
    proposedRawArguments: Map<Text, Value>,
    argumentsMatchSchema: Boolean,
    toolExecutionSucceeded: Boolean,
    toolExecutionOutput: Value,
    finalModelContent: Value
) -> AgentState

    // --- 1) AgentCore: nace el run y se prepara para correr (cierra deuda #1) -----------------
    createdState: AgentState = activateAgent(request)

    config: Optional<AgentConfig> = findAgentConfig(request.agentId)

    initializingState: AgentState = beginAgentInitialization(createdState, config)

    // beginAgentInitialization (CH-11) construye su propio ExecutionContext solo para poblar el
    // AgentEvent que emite internamente — no lo devuelve; este capítulo construye el
    // ExecutionContext real que el resto del turno comparte: mismo runId/sessionId/budget, con un
    // traceId propio (newTraceId(), la misma primitiva que CH-11 ya introdujo) — hallazgo real de
    // este capítulo, documentado en seccion 18: CH-11 no expone el ExecutionContext que construye.
    execution: ExecutionContext = ExecutionContext(
        runId = initializingState.runId,
        sessionId = initializingState.sessionId,
        traceId = newTraceId(),
        budget = config.budget
    )

    emitAndDistribute(
        RUN_STARTED, execution, initializingState.agentId, initializingState, activeSubscriptions
    )

    runningState: AgentState = AgentState(
        runId = initializingState.runId,
        sessionId = initializingState.sessionId,
        agentId = initializingState.agentId,
        status = RUNNING,
        currentTurn = initializingState.currentTurn
    )

    session: Optional<SessionState> = NULL

    firstMessage: AgentMessage = AgentMessage(
        id = newMessageId(),
        role = USER,
        content = request.input,
        timestamp = now()
    )
    candidates: List<AgentMessage> = []
    candidates.append(firstMessage)

    // --- 2) ExecutionController ANTES de que AgentLoop decida el turno (cierra deuda #6) -------
    continuationOne: ExecutionDecision = evaluateExecutionContinuation(
        runningState, execution, execution.budget, usage, FALSE
    )
    emitAndDistribute(
        EXECUTION_EVALUATED, execution, runningState.agentId, continuationOne, activeSubscriptions
    )

    IF continuationOne.outcome != CONTINUE
        // outcome = STOP / CANCELLED: terminación operacional real — deliberadamente CH-13.
        RETURN runningState
    END

    // --- 3) ContextEngine selecciona lo que el modelo va a ver (cierra deuda #3) ---------------
    snapshotOne: ContextSnapshot = assembleContextSnapshot(candidates, execution, runningState.agentId)
    emitAndDistribute(
        CONTEXT_SNAPSHOT_ASSEMBLED, execution, runningState.agentId, snapshotOne, activeSubscriptions
    )

    pendingMessagesOne: List<AgentMessage> = []
    FOR EACH block IN snapshotOne.blocks
        pendingMessagesOne.append(AgentMessage(
            id = newMessageId(),
            role = USER,
            content = block.content,
            timestamp = now()
        ))
    END

    // --- 4) ModelGateway invoca al modelo con el ContextSnapshot ya ensamblado -----------------
    responseOne: ModelResponse = invokeModelForTurn(
        runningState, execution, pendingMessagesOne,
        TRUE, FALSE, TRUE, proposedCapabilityName, proposedRawArguments, NULL
    )
    emitAndDistribute(
        MODEL_RESPONSE_RECEIVED, execution, runningState.agentId, responseOne, activeSubscriptions
    )

    // --- 5) AgentLoop recibe señales derivadas de un ModelResponse real (cierra deuda #2) ------
    modelFinishedOne: Boolean = responseOne.finished
    modelProposesToolCallOne: Boolean = responseOne.proposedToolCall != NULL

    turnOneState: AgentState = runTurn(runningState, execution, modelFinishedOne, modelProposesToolCallOne)
    emitAndDistribute(TURN_CONTINUED, execution, turnOneState.agentId, turnOneState, activeSubscriptions)

    // --- 6) SessionManager hace checkpoint al cierre del turno (cierra deuda #9) ---------------
    sessionAfterTurnOne: SessionState = createOrUpdateSessionCheckpoint(
        session, turnOneState, execution, turnOneState.agentId
    )
    emitAndDistribute(
        SESSION_CHECKPOINT_CREATED, execution, turnOneState.agentId, sessionAfterTurnOne,
        activeSubscriptions
    )
    session = sessionAfterTurnOne

    resumedState: AgentState = turnOneState

    IF turnOneState.status == WAITING_FOR_TOOL
        // --- 7) CapabilityRegistry resuelve la propuesta DENTRO del turno real (cierra deuda #4) -
        callOne: ToolCall = resolveModelProposedToolCall(
            responseOne, registeredCapabilities, execution, turnOneState.agentId, argumentsMatchSchema
        )
        emitAndDistribute(CAPABILITY_RESOLVED, execution, turnOneState.agentId, callOne, activeSubscriptions)

        // --- 8) PolicyEngine evalúa ANTES de que ToolRuntime ejecute (cierra deuda #5) ---------
        decisionOne: PolicyDecision = evaluatePolicyForToolCall(callOne, execution, turnOneState.agentId)
        emitAndDistribute(POLICY_EVALUATED, execution, turnOneState.agentId, decisionOne, activeSubscriptions)

        IF decisionOne.outcome != ALLOW
            // outcome = DENY / REQUIRE_APPROVAL: caminos de CH-13 — este capítulo cierra solo ALLOW.
            RETURN turnOneState
        END

        resultOne: ToolResult = executeToolCall(
            callOne, execution, turnOneState.agentId, TRUE, TRUE,
            toolExecutionSucceeded, toolExecutionOutput
        )

        toolEventType: AgentEventType = TOOL_CALL_COMPLETED
        IF NOT resultOne.succeeded
            toolEventType = TOOL_CALL_FAILED
        END
        emitAndDistribute(toolEventType, execution, turnOneState.agentId, resultOne, activeSubscriptions)

        // --- 9) la observación real, no una señal asumida (cierra deuda #7, INV-07) ------------
        observation: AgentMessage = AgentMessage(
            id = newMessageId(),
            role = TOOL,
            content = resultOne,
            timestamp = now()
        )
        candidates.append(observation)

        resumedState = AgentState(
            runId = turnOneState.runId,
            sessionId = turnOneState.sessionId,
            agentId = turnOneState.agentId,
            status = RUNNING,
            currentTurn = turnOneState.currentTurn
        )
    END

    // --- 10) segundo turno: mismo patrón; esta vez el modelo termina de razonar ---------------
    continuationTwo: ExecutionDecision = evaluateExecutionContinuation(
        resumedState, execution, execution.budget, usage, FALSE
    )
    emitAndDistribute(
        EXECUTION_EVALUATED, execution, resumedState.agentId, continuationTwo, activeSubscriptions
    )

    IF continuationTwo.outcome != CONTINUE
        RETURN resumedState
    END

    snapshotTwo: ContextSnapshot = assembleContextSnapshot(candidates, execution, resumedState.agentId)
    emitAndDistribute(
        CONTEXT_SNAPSHOT_ASSEMBLED, execution, resumedState.agentId, snapshotTwo, activeSubscriptions
    )

    pendingMessagesTwo: List<AgentMessage> = []
    FOR EACH block IN snapshotTwo.blocks
        pendingMessagesTwo.append(AgentMessage(
            id = newMessageId(),
            role = USER,
            content = block.content,
            timestamp = now()
        ))
    END

    responseTwo: ModelResponse = invokeModelForTurn(
        resumedState, execution, pendingMessagesTwo,
        TRUE, TRUE, FALSE, "", {}, finalModelContent
    )
    emitAndDistribute(
        MODEL_RESPONSE_RECEIVED, execution, resumedState.agentId, responseTwo, activeSubscriptions
    )

    modelFinishedTwo: Boolean = responseTwo.finished
    modelProposesToolCallTwo: Boolean = responseTwo.proposedToolCall != NULL

    finalState: AgentState = runTurn(resumedState, execution, modelFinishedTwo, modelProposesToolCallTwo)

    finalEventType: AgentEventType = TURN_CONTINUED
    IF finalState.status == COMPLETED
        finalEventType = RUN_COMPLETED
    END
    emitAndDistribute(finalEventType, execution, finalState.agentId, finalState, activeSubscriptions)

    finalSession: SessionState = createOrUpdateSessionCheckpoint(
        session, finalState, execution, finalState.agentId
    )
    emitAndDistribute(
        SESSION_CHECKPOINT_CREATED, execution, finalState.agentId, finalSession, activeSubscriptions
    )

    RETURN finalState
END
```

`newEventId()`, `now()`, `findAgentConfig(...)` y `newTraceId()` son las mismas primitivas de
CH-00/CH-11 (no son entidades arquitectónicas ni componentes). `newMessageId()` es la única
primitiva nueva de este capítulo, en el mismo espíritu — no requiere ficha ni registro.

`registeredCapabilities`, `activeSubscriptions`, `usage`, `proposedCapabilityName`,
`proposedRawArguments`, `argumentsMatchSchema`, `toolExecutionSucceeded`, `toolExecutionOutput` y
`finalModelContent` son señales de entrada — igual que en cada capítulo anterior — que un
`Provider Adapter` real, un algoritmo real de validación de esquemas, o una implementación real de
una capability producirían en la práctica; este capítulo no los calcula, los recibe ya dados,
exactamente con el mismo alcance que CH-02/CH-03/CH-08 ya declararon para señales equivalentes.
`request`, en cambio — igual que `candidates` en CH-04 — no es una señal asumida de un componente
futuro: es la solicitud real con la que arranca la traza completa.

Nótese lo que `runAgentTurnEndToEnd` **nunca** hace: no decide directamente ningún
`AgentRunStatus` fuera de los que `runTurn`/`beginAgentInitialization` ya deciden (las dos
construcciones literales de `AgentState` con `status = RUNNING` — la transición
`INITIALIZING → RUNNING` y la reanudación `WAITING_FOR_TOOL → RUNNING` — son transiciones de datos
puros, no una decisión de continuación cognitiva ni operacional: esas siguen perteneciendo,
exactamente igual que antes, a `AgentLoop`/`ExecutionController`); no evalúa policy ni presupuesto
por su cuenta (invoca a quien sí lo posee, y respeta su resultado); y no resuelve nunca
`decisionOne.outcome = DENY`/`REQUIRE_APPROVAL` ni `continuationOne/Two.outcome = STOP`/
`CANCELLED` — cada uno de esos cuatro casos termina la función con un `RETURN` explícito hacia el
estado tal como estaba, dejando la resolución real de esos caminos para el capítulo que todavía no
existe (ver seccion 18/19).

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013): sigue siendo, sin cambios, el
mismo `ENUM` de once estados que `AgentLoop` (CH-01) formalizó. Es, en cambio, el primer capítulo
en ejercitar con pseudocódigo real la secuencia completa que atraviesa un `AgentRun` que nunca
requiere denegación ni aprobación humana:

```text
(activateAgent)                          → CREATED         (AgentCore, CH-11)
(beginAgentInitialization)               → INITIALIZING    (AgentCore, CH-11)
[este capítulo]                          → RUNNING          (transición de datos, ver seccion 11)
(runTurn: modelProposesToolCall = TRUE)  → WAITING_FOR_TOOL (AgentLoop, CH-01)
[este capítulo, tras resolver/autorizar/ejecutar la tool call] → RUNNING
(runTurn: modelFinished = TRUE)          → COMPLETED        (AgentLoop, CH-01)
```

**Lo que este capítulo cierra, y lo que deliberadamente no corrige.** La asimetría real que CH-11
§12 documentó explícitamente — `AgentLoop.runTurn` nunca distingue `INITIALIZING` de `RUNNING` en
su guard, que solo rechaza los cuatro estados terminales — sigue sin corregirse en el código de
CH-01, exactamente como CH-11 la dejó: este capítulo no modifica `runTurn`. Lo que sí hace es
dejar de depender de esa asimetría por accidente: construye explícitamente un `AgentState` con
`status = RUNNING` antes de invocar `runTurn` por primera vez, precisamente para que la transición
`INITIALIZING → RUNNING` (Article V, documentada en prosa desde CH-01 §12, nunca ejercitada con
código hasta este capítulo) ocurra de verdad, en vez de dejar que `runTurn` reciba, sin distinguir,
un `AgentState` que todavía dice `INITIALIZING`.

## 13. Semántica de Fallos (Failure Semantics)

Este capítulo no introduce ningún código nuevo de `HarnessError` ni ningún valor nuevo de
`ErrorCategory` (heredado de CH-00 §6): reutiliza, sin cambios, los que cada una de las once
funciones invocadas ya declara — `TURN_ON_TERMINAL_STATE` (CH-01), `CAPABILITY_NOT_FOUND`/
`TOOL_INPUT_SCHEMA_MISMATCH`/`TOOL_EXECUTION_FAILED` (CH-02), `MODEL_UNAVAILABLE` (CH-03),
`CONTEXT_BUDGET_EXHAUSTED` (CH-04), `NO_APPLICABLE_POLICY_RULE`/`POLICY_DENIED` (CH-05),
`MAX_TURNS_EXCEEDED` y las demás seis variantes de `EXCEEDED`/`EXECUTION_CANCELLED` (CH-07),
`RESOLUTION_REQUESTED_WITHOUT_PROPOSAL` (CH-08), `SESSION_ID_MISMATCH`/`SESSION_PERSISTENCE_FAILED`
(CH-10) y `AGENT_CONFIG_NOT_FOUND`/`INCOHERENT_EXECUTION_BUDGET`/
`INITIALIZATION_REQUIRES_CREATED_STATE` (CH-11).

`runAgentTurnEndToEnd` (seccion 11) nunca construye un `HarnessError` por su cuenta: cuando
`continuationOne`/`continuationTwo.outcome != CONTINUE` o `decisionOne.outcome != ALLOW`, se
detiene con un `RETURN` explícito del estado tal como estaba — dejando que sea la función
correspondiente (`evaluateExecutionContinuation`/`evaluatePolicyForToolCall`, ya publicadas) la que
haya construido, dentro de su propio `ExecutionDecision`/`PolicyDecision`, el `HarnessError` real
que explica por qué (categoría `BUDGET`/`CANCELLATION` o el reutilizado `POLICY`). Este capítulo no
reclasifica esos fallos ni les agrega ninguna categoría nueva.

Lo que este capítulo **deliberadamente no clasifica todavía**: qué `HarnessError` correspondería a
que una `HumanInteractionRequest` (CH-06) quede pendiente sin resolverse dentro de una ejecución
real — esa clasificación pertenece al capítulo que cablee el camino `REQUIRE_APPROVAL` (ver
seccion 18/19).

## 14. Eventos Producidos (Events Produced)

Este capítulo no agrega ningún valor nuevo a `AgentEventType` (seccion 6). Lo que sí produce, por
primera vez en este libro, es que cada uno de los siguientes valores — todos ya declarados desde
CH-00..CH-10 — llegue de verdad a `EventBus.distributeEvent` dentro de una sola ejecución real, en
el orden en que `runAgentTurnEndToEnd` (seccion 11) los distribuye:

```text
RUN_STARTED                  (AgentCore, §11 paso 1)
EXECUTION_EVALUATED          (ExecutionController, §11 pasos 2 y 11 — dos veces)
CONTEXT_SNAPSHOT_ASSEMBLED   (ContextEngine, §11 pasos 3 y 12 — dos veces)
MODEL_RESPONSE_RECEIVED      (ModelGateway, §11 pasos 4 y 13 — dos veces)
TURN_CONTINUED               (AgentLoop, §11 paso 5 — el primer turno, WAITING_FOR_TOOL)
SESSION_CHECKPOINT_CREATED   (SessionManager, §11 pasos 6 y 15 — dos veces)
CAPABILITY_RESOLVED          (CapabilityRegistry, §11 paso 7)
POLICY_EVALUATED             (PolicyEngine, §11 paso 8)
TOOL_CALL_COMPLETED          (ToolRuntime, §11 paso 9 — camino feliz, resultOne.succeeded = TRUE)
RUN_COMPLETED                (AgentLoop, §11 paso 14 — el segundo turno, COMPLETED)
```

Diez tipos de evento distintos, quince apariciones en total — cada una entregada, por primera vez,
a través de `emitAndDistribute`/`distributeEvent` (CH-09) en vez de quedarse como una construcción
sin destino. `HUMAN_INTERACTION_REQUESTED`/`HUMAN_INTERACTION_RESOLVED` (CH-06),
`RUN_FAILED`/`TOOL_CALL_FAILED`/`MODEL_INVOCATION_FAILED`/`CONTEXT_SNAPSHOT_FAILED`/
`CAPABILITY_RESOLUTION_FAILED`/`SESSION_RECONSTRUCTED`/`SESSION_BRANCHED`/`SESSION_PERSISTENCE_FAILED`
no se emiten en el camino feliz de este capítulo — pertenecen a caminos que este capítulo no
recorre (ver seccion 15/18).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

Este capítulo nunca ejecuta una acción sin que `PolicyEngine` ya la haya evaluado — la primera vez
que INV-06 se cumple con una ejecución real de punta a punta — pero modela **exclusivamente** el
resultado `outcome = ALLOW`. Esto es una limitación real y deliberada, no una brecha silenciada:

- **`PolicyDecision.outcome = DENY`**: `evaluatePolicyForToolCall` (CH-05) ya sabe producir este
  resultado — este capítulo simplemente nunca construye el escenario de entrada que lo provocaría,
  y su `IF decisionOne.outcome != ALLOW` (seccion 11) se detiene ahí sin resolver nada más.
- **`PolicyDecision.outcome = REQUIRE_APPROVAL`**: requeriría invocar, por primera vez de forma
  real, `HumanInteractionService.createHumanInteractionRequest` (CH-06) — y esperar, de alguna
  forma, una `HumanInteractionResolution` antes de que `ToolRuntime` pudiera continuar. Ninguna de
  las dos cosas ocurre en este capítulo.
- **`ExecutionDecision.outcome = STOP` o `CANCELLED`**: `evaluateExecutionContinuation` (CH-07) ya
  sabe producir ambos resultados — este capítulo los deja explícitamente sin resolver con un
  `RETURN` temprano, sin decidir hacia qué `AgentRunStatus` terminal (`FAILED`/`CANCELLED`/
  `EXPIRED`) debería transicionar el run.

Ningún componente cambió su frontera para que esto fuera posible: `PolicyEngine` sigue sin
ejecutar la acción que evalúa, `ExecutionController` sigue sin decidir continuación cognitiva, y
`ToolRuntime` sigue exigiendo que la autorización ya haya ocurrido antes de recibir
`capabilityResolved = TRUE`/`inputValid = TRUE`. La seguridad de este capítulo consiste,
precisamente, en detenerse con honestidad en el primer punto en el que el camino feliz termina, en
vez de inventar un comportamiento para los casos que no modela.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST RunAgentTurnEndToEndNeverInvokesExecuteToolCallBeforePolicyEngineReturnsAllow
TEST RunAgentTurnEndToEndNeverInvokesRunTurnBeforeExecutionControllerReturnsContinue
TEST RunAgentTurnEndToEndDerivesModelFinishedAndModelProposesToolCallFromARealModelResponse
TEST RunAgentTurnEndToEndResumesWaitingForToolWithTheRealToolResultAsObservation
TEST RunAgentTurnEndToEndInvokesCreateOrUpdateSessionCheckpointAfterEveryRunTurnCall
TEST EmitAndDistributeAlwaysDeliversTheSameExecutionContextTraceIdAcrossEveryEvent
TEST RunAgentTurnEndToEndNeverModifiesAnyAlreadyPublishedComponentFunction
TEST RunAgentTurnEndToEndStopsExplicitlyOnAnyNonAllowOrNonContinueOutcome
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.1, después de CH-12)

Constitution
 ├── Article III  — Component Sovereignty (once componentes, sin cambios — CH-11 fue el último)
 ├── Article IV   — Decision Ownership (cada fila de la tabla, respetada sin excepción)
 └── Article V    — Lifecycle (primera secuencia CREATED → ... → COMPLETED ejercitada de punta a
                     punta con código real)

Contracts (registry/contracts.yaml)
 └── C-001..C-021  (sin cambios — 21 contratos, idéntico a después de CH-11)

Components (registry/components.yaml)
 └── CMP-001..CMP-011  (sin cambios — 11 componentes, idéntico a después de CH-11)
```

**Hallazgo real, verificado y documentado sin ocultarlo (ver seccion 9).** Como
`registry/components.yaml` no cambia, y `scripts/lib/mindmap.js` deriva las aristas
`DEPENDS_ON`/`PRODUCES`/`CONSUMES` exclusivamente de los campos que cada componente ya declaraba en
su propio capítulo de introducción, `diagrams/mindmap/chapter-12.diagram` es, verificado con
`./scripts/build-mind-map`, **idéntico** a `diagrams/mindmap/chapter-11.diagram` — mismos nodos,
mismas aristas (ver `planes/2026-09-14-capitulo-12-integracion-camino-feliz.md` para las cifras
exactas verificadas). Esto es consistente con `introduces_components: []`/`introduces_contracts:
[]`: un capítulo de integración que no toca el registry no le agrega, mecánicamente, ninguna
arista nueva al `BookMindMap` — el cableado real que este capítulo construye vive en
`runAgentTurnEndToEnd` (seccion 11), no en `registry/components.yaml`.

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El camino `DENY`**: `evaluatePolicyForToolCall` produciendo `outcome = DENY` dentro de una
  ejecución real, y qué debería pasar después (¿el turno termina en `FAILED`? ¿se le devuelve la
  denegación al modelo como observación para que proponga otra cosa?) — sin resolver.
- **El camino `REQUIRE_APPROVAL`**: cablear `HumanInteractionService.createHumanInteractionRequest`
  dentro de esta misma traza, transicionar realmente hacia `WAITING_FOR_HUMAN`, y reanudar con una
  `HumanInteractionResolution` real — el ciclo completo de Article VIII, todavía sin ejecución real
  de punta a punta.
- **Los caminos `STOP`/`CANCELLED`**: hacia qué `AgentRunStatus` terminal exacto
  (`FAILED`/`CANCELLED`/`EXPIRED`) debería transicionar un run cuando `ExecutionController` decide
  que no puede continuar — este capítulo se detiene con un `RETURN` temprano, sin decidirlo.
- **El seam real en `AgentCore.beginAgentInitialization` (CH-11), documentado con honestidad**:
  esa función construye su propio `ExecutionContext` internamente solo para poblar el evento que
  emite, pero no lo devuelve — este capítulo tuvo que construir un segundo `ExecutionContext`
  equivalente (mismo `runId`/`sessionId`/`budget`, `traceId` propio) para el resto de la traza. Una
  revisión futura de CH-11 (fuera del alcance de este capítulo, que no modifica capítulos
  anteriores) podría resolver este seam haciendo que `beginAgentInitialization` devuelva también su
  `ExecutionContext`.
- **`registry/components.yaml` sin aristas nuevas de dependencia real**: como se documenta en la
  seccion 9/17, este capítulo invoca realmente a los once componentes entre sí, pero ninguno de
  ellos declara esa relación en su propio campo `dependencies` — el `BookMindMap` mecánico no
  refleja, todavía, el cableado real que este capítulo demuestra en pseudocódigo.
- **Paralelismo de tool calls, ranking semántico real de contexto, Provider Adapters reales,
  algoritmos reales de validación de schema, mecanismo real de alta de `CapabilityDescriptor`,
  autorización sobre quién puede activar un agente ajeno**: deuda intencional heredada de
  CH-02..CH-11, sin cambios en este capítulo.
- Reviewers plurales, evals y orquestación multi-agente: explícitamente fuera de alcance de
  BH-v0.1 (igual que todos los capítulos anteriores).

## 19. Siguiente Incremento (Next Increment)

El problema natural del próximo capítulo: ahora que el camino feliz de un `AgentRun` completo tiene
código real de principio a fin, ¿qué ocurre en cada uno de los puntos donde este capítulo se
detuvo con honestidad en vez de continuar — `PolicyDecision.outcome = DENY` o
`REQUIRE_APPROVAL` (y, en ese segundo caso, el ciclo completo de `HumanInteractionService`, CH-06,
todavía sin una sola ejecución real), y `ExecutionDecision.outcome = STOP` o `CANCELLED` (y hacia
qué `AgentRunStatus` terminal exacto deberían transicionar)? Ese es, precisamente, el alcance que
esta misma ejecución dejó fuera a propósito (ver seccion 15/18) — el "camino infeliz" que
complementa al camino feliz de este capítulo.

`next_chapter` queda en `null` en el frontmatter de este capítulo porque, en este momento del
libro, ese próximo capítulo todavía no existe como archivo — solo como el problema que motivaría su
escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg /
> Bucles de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows),
> secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): después de once capítulos reales, ningún archivo de este
   libro había mostrado nunca una sola ejecución completa de un agente — cada componente
   demostraba su propia función aislada, con señales de entrada asumidas en vez de con la salida
   real de su vecino.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): cada capítulo
   cerró su propia demostración con la misma disciplina de *ownership*, y dejó, con la misma
   disciplina, una nota explícita señalando qué llamada real faltaba — nueve notas de deuda que
   nunca se resuelven solas.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   una función de integración, `runAgentTurnEndToEnd`, que invoca las once funciones ya publicadas
   en el orden correcto, sin modificar ni una línea de ninguna de las once fichas ya registradas.
4. **Modelos mentales** (= §4, Constitutional Impact): el Ownership Rule de Article IV nunca
   exigió que los componentes se ignoraran entre sí para siempre — exigió que cada uno declarara
   su frontera antes de que existiera código real que pudiera cruzarla.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada capítulo que se escribió sin cablear realmente al
  anterior hizo crecer la lista de deuda intencional en vez de resolverla — once capítulos
  seguidos señalando el mismo problema desde ángulos distintos.
- **Bucle de equilibrio (estabiliza):** `runAgentTurnEndToEnd` (§11) verifica el resultado real en
  cada punto de decisión y se detiene explícitamente, sin inventar el resto del camino, en cuanto
  ese resultado no es el camino feliz.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que la integración se escriba como una función
nueva (`runAgentTurnEndToEnd`) que orquesta llamadas reales, en vez de reabrir y modificar el
pseudocódigo ya publicado de cualquiera de los once capítulos anteriores. Si este capítulo hubiera
editado la firma de `AgentLoop.runTurn`, habría alterado un contrato de comportamiento que once
capítulos de lectores ya aprendieron — exactamente la estabilidad que este libro protege capítulo
a capítulo.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo
> de esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set`
> (frontmatter) y es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Once componentes distintos demostraron, cada uno por su cuenta, una función real con señales
   asumidas. ¿Qué hace falta para encadenarlas en una sola ejecución real? *(cierra la pregunta
   guía 1)*
2. ¿Qué necesita ocurrir, y en qué orden, para que `WAITING_FOR_TOOL` deje de ser un final sin
   resolver? *(cierra la pregunta guía 2)*
3. ¿Qué tendría que pasar para que cada `EMIT` de este libro por fin llegara a alguien? *(cierra
   la pregunta guía 3)*
4. ¿En qué punto exacto del camino deberían consultarse la autorización y el presupuesto
   operacional? *(cierra la pregunta guía 4)*

### Explicar

1. Este capítulo nunca modifica `AgentLoop.runTurn`, aunque sigue recibiendo dos booleanos
   sueltos. Explica dónde vive la transformación que hace que esos booleanos ya no sean una
   suposición aislada.
2. `ToolRuntime.executeToolCall` sigue recibiendo `capabilityResolved`/`inputValid` como
   booleanos. Explica qué tuvo que ocurrir, unas líneas antes, para que pasarle `TRUE` a ambos ya
   no sea una suposición.

### Conectar

1. ¿Qué campo de `ExecutionContext`, construido una sola vez cerca del principio de la ejecución,
   sobrevive sin cambiar hasta la tool call de `ToolRuntime`?
2. ¿Qué tienen en común la verificación de procedencia de `ContextEngine` y la validación de
   schema de `CapabilityRegistry`?
3. ¿Cuál de las dos preguntas — "¿debe continuar el turno?" o "¿puede seguir la ejecución?" — se
   responde primero, y qué pasaría si se invirtiera ese orden?
4. ¿Cuántos componentes distintos intervienen entre la propuesta cruda de `ModelGateway` y la
   ejecución real de `ToolRuntime`?
5. ¿Qué tendría que ocurrir para que `HUMAN_INTERACTION_REQUESTED` también llegara a
   `distributeEvent`, y por qué `EventBus` no necesitaría cambiar para que eso funcione?

### Espaciar

Las cinco tarjetas de repaso de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas de
nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) — ver `retrieval_set.flashcards` en
`dist/book-ir.json`.

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo.
