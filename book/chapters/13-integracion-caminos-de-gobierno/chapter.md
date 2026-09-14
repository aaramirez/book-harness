---
id: CH-13
title: "Integración: los Caminos de Gobierno de un AgentRun Completo"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: []
introduces_contracts: []
modifies_contracts: []
constitutional_articles: [P-05, P-10, P-13, INV-06, INV-09, INV-10, INV-14, INV-15, INV-18, INV-19, INV-20]
previous_chapter: CH-12
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH13
    text: |
      Al terminar este capítulo podrás verificar, para cualquier ejecución de un agente que el
      sistema deniega, pausa para que un humano decida, o detiene por presupuesto o cancelación,
      exactamente qué componente real produce esa decisión de gobierno y hacia qué estado terminal
      o de espera transiciona el run — y podrás diagnosticar, para cualquier punto donde el camino
      feliz de este libro se detuvo con un `RETURN` temprano, qué función real de este capítulo
      resuelve ese punto en vez de dejarlo, otra vez, como una nota de deuda.
  skeleton:
    id: SK-CH13
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
    - id: GQ-CH13-01
      text: |
        Cuando la evaluación de autorización de una acción concreta resuelve que esa acción no
        está permitida, el componente que la ejecutaría nunca llega a invocarse. ¿Qué le devuelve
        entonces el ciclo cognitivo al modelo en el turno siguiente, si no es el resultado de una
        ejecución que nunca ocurrió?
      answered_by: RQ-CH13-01
    - id: GQ-CH13-02
      text: |
        Un estado de espera, declarado desde el primer capítulo de este libro, nunca había sido
        el destino real de ninguna transición. Cuando una acción concreta por fin necesita que un
        humano la apruebe, ¿en qué momento exacto entra la ejecución a ese estado, y por qué la
        función que la lleva ahí puede simplemente terminar, sin ningún proceso que se quede
        esperando?
      answered_by: RQ-CH13-02
    - id: GQ-CH13-03
      text: |
        Una vez que la aprobación humana pendiente por fin se resuelve, ¿qué distingue, en el
        camino que sigue la ejecución, una resolución que aprueba la acción de una que la
        rechaza — y por qué el segundo caso termina pareciéndose al camino de una denegación que
        nunca pasó por un humano?
      answered_by: RQ-CH13-03
    - id: GQ-CH13-04
      text: |
        Tres estados finales de una ejecución, declarados desde el capítulo que formalizó su
        lifecycle completo, nunca habían sido el resultado real de ningún pseudocódigo de este
        libro. ¿Qué componente ya sabe distinguir, entre esos tres desenlaces, cuál corresponde a
        un límite operacional agotado y cuál a una cancelación explícita — y qué le falta todavía
        para que esa distinción se convierta en el estado real de una ejecución?
      answered_by: RQ-CH13-04
  systems_lens:
    iceberg_visible_fact: |
      El capítulo anterior recorrió, con código real, un `AgentRun` completo — pero únicamente en
      el único mundo donde nada sale mal: cada policy permite, cada presupuesto alcanza, nadie
      cancela nada. El resto de este libro — tres resultados reales que `PolicyEngine` y
      `ExecutionController` ya sabían producir desde sus propios capítulos — seguía sin una sola
      ejecución que los recorriera (ver seccion 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite, ahora aplicado a la integración misma, es que el capítulo anterior
      cerró su propia demostración con la misma disciplina que los once componentes ya habían
      establecido — modelar solo el resultado más permisivo de cada decisión — y dejó, con la
      misma honestidad, tres notas explícitas señalando exactamente qué faltaba. Un capítulo de
      integración que solo demuestra el camino feliz dejaría, para siempre, sin ejercitar la mitad
      de lo que `PolicyEngine`, `HumanInteractionService` y `ExecutionController` ya saben hacer
      desde que se escribieron (ver seccion 3, Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo no instala ningún componente nuevo — instala cinco funciones de integración
      nuevas y propias (`resumeTurnWithObservation`, `runAgentTurnWithPolicyDenial`,
      `beginToolApprovalPause`, `resumeAfterHumanResolution` y
      `terminateAgentRunOperationally`, seccion 11) que invocan, en los tres puntos exactos donde
      `runAgentTurnEndToEnd` (CH-12 §11) se detuvo con un `RETURN` temprano, las funciones que
      `PolicyEngine`, `HumanInteractionService` y `ExecutionController` ya publicaron desde sus
      propios capítulos — sin modificar el código publicado de `runAgentTurnEndToEnd` ni de
      ninguno de los once componentes (ver seccion 8, Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es el mismo que CH-12 ya estableció, aplicado
      esta vez a los desenlaces que no son el más permisivo: cerrar un cable no significa
      reescribir el componente que produce la señal — significa escribir, en un capítulo nuevo, el
      código que por fin consume esa señal hasta su destino real, honrando exactamente el
      resultado que el componente ya devolvía (ver seccion 4, Impacto Constitucional).
    reinforcing_loop: |
      Cada vez que un capítulo de integración demuestra solo el resultado más permisivo de cada
      decisión, dos resultados reales (`DENY`/`REQUIRE_APPROVAL` de `PolicyEngine`,
      `STOP`/`CANCELLED` de `ExecutionController`) siguen existiendo únicamente en prosa — el
      mismo bucle que CH-05, CH-06 y CH-07 señalaron cada uno por su cuenta, y que CH-12 heredó sin
      cerrarlo, documentándolo con la misma honestidad en su propia seccion 18.
    balancing_loop: |
      Cada una de las cinco funciones de este capítulo (seccion 11) es el mecanismo de equilibrio:
      se detiene exactamente en el punto donde su propio resultado deja de ser el que le
      corresponde resolver (`runAgentTurnWithPolicyDenial` exige `outcome = DENY`,
      `beginToolApprovalPause` exige `outcome = REQUIRE_APPROVAL`,
      `terminateAgentRunOperationally` exige `outcome != CONTINUE`) — cada una construida contra
      una única precondición real, nunca contra una suposición.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que los tres caminos que CH-12 dejó
      pendientes se resuelvan como funciones nuevas y separadas, en vez de reabrir
      `runAgentTurnEndToEnd` (CMP-001, seccion 8) para agregarle ramas nuevas. Si este capítulo
      hubiera editado esa función para incluir `IF/ELSE` sobre cada desenlace posible, el
      resultado habría sido una sola función gigantesca que mezcla el camino feliz con los tres
      caminos de gobierno — exactamente la clase de acoplamiento que Article IV, aplicado ahora a
      la integración misma, existe para evitar.
  recall_questions:
    - id: RQ-CH13-01
      text: |
        Cuando `evaluatePolicyForToolCall` devuelve `outcome = DENY` dentro de una ejecución real,
        ¿qué función nunca se invoca, y qué construye `runAgentTurnWithPolicyDenial` en su lugar
        para que el modelo vea la denegación en el turno siguiente?
    - id: RQ-CH13-02
      text: |
        ¿Qué función de este capítulo transiciona un `AgentRun` real, por primera vez, hacia
        `WAITING_FOR_HUMAN`, y por qué esa función puede terminar (`RETURN`) sin que ningún proceso
        quede esperando la resolución humana?
    - id: RQ-CH13-03
      text: |
        ¿Qué dos funciones ya publicadas invoca `resumeAfterHumanResolution`, en qué orden, y qué
        decide cuál de las dos ramas (`executeToolCall` real o una observación de rechazo) sigue
        después?
    - id: RQ-CH13-04
      text: |
        Según el mapeo que `terminateAgentRunOperationally` ejecuta por primera vez con código
        real, ¿hacia qué tres valores distintos de `AgentRunStatus` puede transicionar un
        `ExecutionDecision` cuyo `outcome != CONTINUE`, y qué campo exacto de esa decisión separa
        los tres casos?
  explain_prompts:
    - id: EP-CH13-01
      text: |
        `ToolRuntime.executeToolCall` (CH-02) nunca cambia una sola línea en este capítulo, y sin
        embargo este capítulo demuestra, por primera vez con código real, que esa función puede
        simplemente no ser invocada dentro de un turno completo. Explica, como si hablaras con
        alguien sin contexto técnico, por qué eso es exactamente lo que Article VI, Execution Rule
        3 exige — ¿qué se rompería si `executeToolCall` se invocara "solo para completar el
        turno", incluso cuando `PolicyEngine` ya dijo que no?
      target_entity: CMP-002
    - id: EP-CH13-02
      text: |
        `HumanInteractionService.createHumanInteractionRequest` (CH-06) fue publicada hace siete
        capítulos, pero hasta este capítulo nunca había sido invocada con una `PolicyDecision`
        real ni había producido una transición real de `AgentRunStatus`. Explica por qué esa
        espera de siete capítulos no significa que `createHumanInteractionRequest` estuviera mal
        diseñada — ¿qué le permitió, sin cambiar una sola línea, quedar lista para este momento?
      target_entity: CMP-006
  interleaved_questions:
    - id: IQ-CH13-01
      text: |
        `AgentLoop` (CH-01) declaró `WAITING_FOR_HUMAN` como uno de los once estados de
        `AgentRunStatus` desde su primer capítulo, sin que ninguna transición real lo alcanzara —
        y `HumanInteractionService` (CH-06) formalizó, seis capítulos después, el par de contratos
        capaz de justificar esa espera. ¿Por qué hicieron falta ambos capítulos, y no solo uno de
        los dos, para que este capítulo pudiera por fin escribir el código que entra y sale de ese
        estado?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-001, C-013, CMP-006, C-015]
      prior_chapter: CH-01
    - id: IQ-CH13-02
      text: |
        `ExecutionController` (CH-07) documentó en prosa, en su propia sección 12, hacia qué
        `AgentRunStatus` terminal apuntaría cada `ExecutionDecision` — sin que ningún pseudocódigo,
        hasta este capítulo, ejecutara realmente esa tabla. ¿Qué tuvo que existir primero,
        `runAgentTurnEndToEnd` (CH-12) o `terminateAgentRunOperationally` (este capítulo), para que
        esa tabla dejara de ser solo prosa — y por qué el orden importa?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-007, C-017]
      prior_chapter: CH-07
    - id: IQ-CH13-03
      text: |
        `PolicyEngine` (CH-05) puede producir `outcome = DENY` sin que ningún humano intervenga
        jamás, y `HumanInteractionService` (CH-06) puede producir una resolución `REJECTED` que
        tampoco requiere que ningún humano se haya equivocado con la política. ¿Por qué este
        capítulo hace que ambos caminos terminen pareciéndose — la misma forma de observación de
        vuelta al modelo — sin que eso signifique que `PolicyEngine` y `HumanInteractionService`
        dejen de ser dos dueños distintos de dos preguntas distintas?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-005, CMP-006]
      prior_chapter: CH-05
    - id: IQ-CH13-04
      text: |
        `EventBus.distributeEvent` (CH-09) nunca necesitó cambiar una sola línea para distribuir
        `HUMAN_INTERACTION_REQUESTED` — CH-12 ya lo había anticipado como una pregunta abierta en
        su propia `interleavedQuestions`. ¿Qué tuvo que ocurrir en este capítulo, y qué no tuvo que
        ocurrir en `EventBus`, para que esa predicción se cumpliera exactamente como CH-12 la
        planteó?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-009, CMP-006]
      prior_chapter: CH-09
    - id: IQ-CH13-05
      text: |
        `ToolRuntime.executeToolCall` (CH-02) exige recibir `capabilityResolved = TRUE` e
        `inputValid = TRUE` como señales ya dadas. En el camino de aprobación humana de este
        capítulo, ¿en qué momento exacto se vuelven ciertas esas dos señales — y qué tiene que
        haber ocurrido antes, en `HumanInteractionService`, para que invocar `executeToolCall` ahí
        ya no sea una suposición sino un hecho verificado?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-002, CMP-006]
      prior_chapter: CH-02
    - id: IQ-CH13-06
      text: |
        `AgentLoop.runTurn` (CH-01) nunca construye directamente un `AgentRunStatus` terminal
        distinto de `COMPLETED` — ese poder, según Article IV, tampoco pertenece a
        `ExecutionController` (CH-07), que nunca decide continuación cognitiva. ¿Quién construye,
        entonces, el primer `AgentState` real de este libro con `status = FAILED`,
        `CANCELLED` o `EXPIRED`, y por qué eso no es lo mismo que invadir la propiedad de
        `AgentLoop` sobre `AgentRunStatus`?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-001, C-013]
      prior_chapter: CH-01
  flashcards:
    - id: FC-CH13-01
      front: |
        Cuando `evaluatePolicyForToolCall` devuelve `outcome = DENY`, ¿qué invoca
        `runAgentTurnWithPolicyDenial` y qué NUNCA invoca?
      back: |
        Construye una observación (`AgentMessage`, `role = TOOL`) a partir del `HarnessError` que
        `PolicyDecision.reason` ya trae, la agrega a `candidates`, y retoma el ciclo con
        `resumeTurnWithObservation` — pero nunca invoca `ToolRuntime.executeToolCall` (Article VI,
        Execution Rule 3: las policies se evalúan antes del side effect).
      source_entity: CMP-005
      chapter_introduced_in: CH-13
      review_stage: DAY_1
    - id: FC-CH13-02
      front: |
        ¿Qué función transiciona un `AgentRun` real hacia `WAITING_FOR_HUMAN` por primera vez, y
        por qué puede simplemente `RETURN` sin dejar ningún proceso esperando?
      back: |
        `beginToolApprovalPause`: invoca `createHumanInteractionRequest` (CH-06) sobre una
        `PolicyDecision` real con `outcome = REQUIRE_APPROVAL`, construye el `AgentState` en
        `WAITING_FOR_HUMAN` y termina — Article VIII: "una ejecución durable no debe mantener
        necesariamente un proceso abierto mientras espera intervención humana".
      source_entity: CMP-006
      chapter_introduced_in: CH-13
      review_stage: DAY_1
    - id: FC-CH13-03
      front: |
        ¿Qué hace `resumeAfterHumanResolution` según el `outcome` de la resolución humana?
      back: |
        Invoca `resolveHumanInteractionRequest` (CH-06); si `outcome = APPROVED`, invoca
        `executeToolCall` (CH-02) como si `PolicyEngine` hubiera dicho `ALLOW` desde el principio;
        si `outcome = REJECTED`, construye la misma forma de observación que el camino `DENY` —
        sin volver a evaluar policy.
      source_entity: CMP-006
      chapter_introduced_in: CH-13
      review_stage: DAY_1
    - id: FC-CH13-04
      front: |
        ¿Qué mapeo ejecuta `terminateAgentRunOperationally`, con código real, por primera vez en
        este libro?
      back: |
        `ExecutionDecision.outcome = CANCELLED` → `AgentRunStatus.CANCELLED`;
        `outcome = STOP` con `stopReason = MAX_RUNTIME_EXCEEDED` → `EXPIRED`; `outcome = STOP` con
        cualquier otro `stopReason` → `FAILED` — la tabla que CH-07 §12 documentó solo en prosa.
      source_entity: CMP-007
      chapter_introduced_in: CH-13
      review_stage: DAY_1
    - id: FC-CH13-05
      front: |
        ¿Qué NO resuelve este capítulo, aunque cierra los tres caminos que CH-12 dejó pendientes?
      back: |
        No fusiona estas cinco funciones dentro de `runAgentTurnEndToEnd` (siguen siendo
        invocaciones alternativas en los mismos puntos donde esa función ya se detenía); no agrega
        `RUN_CANCELLED`/`RUN_EXPIRED` a `AgentEventType` (reutiliza `RUN_FAILED`, ver seccion 14);
        y no modela expiración de una `HumanInteractionRequest` que nadie resuelve nunca.
      source_entity: CMP-007
      chapter_introduced_in: CH-13
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH13-01
      recall_question: RQ-CH13-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH13-02
      recall_question: RQ-CH13-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH13-03
      recall_question: RQ-CH13-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH13-04
      recall_question: RQ-CH13-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 13 — Integración: los Caminos de Gobierno de un AgentRun Completo

> **Regla constitucional (Article VI, Execution Rule 3):** las policies se evalúan antes del side
> effect.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1. El detalle
> estructurado de esta sección vive en `retrieval_set` (frontmatter) y es lo que
> `scripts/validate-retrieval-set` valida automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás verificar, para cualquier ejecución de un
agente que el sistema deniega, pausa para que un humano decida, o detiene por presupuesto o
cancelación, exactamente qué componente real produce esa decisión de gobierno y hacia qué estado
terminal o de espera transiciona el run — y podrás diagnosticar, para cualquier punto donde el
camino feliz de este libro se detuvo con un `RETURN` temprano, qué función real de este capítulo
resuelve ese punto en vez de dejarlo, otra vez, como una nota de deuda.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) y, como
CH-12, **no introduce ningún contrato ni ningún componente nuevo** — es el segundo y último
capítulo de integración planeado para este libro: cierra, con código real, los tres caminos que
CH-12 dejó explícitamente pendientes.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar
atrás; están formuladas en lenguaje de problema):

1. Cuando la evaluación de autorización de una acción resuelve que esa acción no está permitida,
   el componente que la ejecutaría nunca llega a invocarse. ¿Qué le devuelve entonces el ciclo
   cognitivo al modelo en el turno siguiente?
2. Un estado de espera, declarado desde el primer capítulo de este libro, nunca había sido el
   destino real de ninguna transición. ¿En qué momento exacto entra la ejecución a ese estado, y
   por qué la función que la lleva ahí puede simplemente terminar?
3. Una vez que la aprobación humana pendiente se resuelve, ¿qué distingue una resolución que
   aprueba la acción de una que la rechaza?
4. Tres estados finales de una ejecución, declarados desde hace varios capítulos, nunca habían
   sido el resultado real de ningún pseudocódigo. ¿Qué falta todavía para que la distinción que un
   componente ya sabe hacer se convierta en el estado real de una ejecución?

## 1. Arquitectura Actual (Current Architecture)

CH-12 escribió, con código real, el primer `AgentRun` completo de este libro — pero únicamente su
**camino feliz**: cada `PolicyDecision.outcome` que produjo fue `ALLOW`, cada
`ExecutionDecision.outcome` que produjo fue `CONTINUE`. Lo hizo con honestidad explícita: su propia
seccion 15 documentó, uno por uno, los tres resultados reales que `PolicyEngine` (CH-05),
`HumanInteractionService` (CH-06) y `ExecutionController` (CH-07) ya sabían producir desde sus
propios capítulos, sin que ninguna ejecución real los hubiera recorrido todavía:

1. **`PolicyDecision.outcome = DENY`** (CH-05 §11) — `evaluatePolicyForToolCall` ya deniega, por
   defecto o porque una regla real lo deniega, desde que CH-05 se escribió. CH-12 §11 se detiene
   ahí con un `RETURN turnOneState` explícito, sin resolver qué le llega al modelo después.
2. **`PolicyDecision.outcome = REQUIRE_APPROVAL`** (CH-05 §11) → el ciclo completo de
   `HumanInteractionService` (`createHumanInteractionRequest`/`resolveHumanInteractionRequest`,
   CH-06 §11), y la transición real hacia `AgentRunStatus.WAITING_FOR_HUMAN` (declarada desde
   CH-01 §6) — ninguna de las dos cosas ocurre en CH-12.
3. **`ExecutionDecision.outcome = STOP` o `CANCELLED`** (CH-07 §11) → hacia qué
   `AgentRunStatus` terminal exacto (`FAILED`/`CANCELLED`/`EXPIRED`, los tres declarados desde
   CH-01 §6) debería transicionar un run — CH-07 §12 lo documentó en prosa ("apuntaría a..."), sin
   que ningún pseudocódigo, hasta este capítulo, lo ejecutara.

`runAgentTurnEndToEnd` (CH-12 §11) contiene, literalmente, los tres puntos exactos donde estos
caminos empiezan y donde este capítulo los retoma:

```text
IF continuationOne.outcome != CONTINUE            → punto A (este capítulo, seccion 11)
    RETURN runningState

IF decisionOne.outcome != ALLOW                    → punto B (este capítulo, seccion 11)
    RETURN turnOneState

IF continuationTwo.outcome != CONTINUE             → punto A, segunda aparición
    RETURN resumedState
```

Ninguno de esos tres `RETURN` cambia en este capítulo — `book/chapters/12-integracion-camino-feliz/chapter.md`
no se modifica salvo su campo de navegación (seccion 17). Este capítulo escribe, en cambio, las
funciones que un capítulo posterior (o el mismo `runAgentTurnEndToEnd`, en una revisión futura
fuera de este alcance) invocaría **en vez de** ese `RETURN`, cuando el resultado real no es el más
permisivo.

## 2. El Problema (Problem)

Con el camino feliz ya recorrido de principio a fin, el problema deja de ser "falta conectar los
componentes" — CH-12 ya demostró que eso es posible sin modificar ninguno de los once. El problema
es más preciso: **este libro nunca ha mostrado qué pasa cuando el sistema dice que no, cuando
alguien tiene que decidir en su lugar, o cuando el tiempo o el presupuesto se agotan**. Un lector
que solo leyera hasta CH-12 aprendería a construir un agente que nunca falla, nunca espera a un
humano y nunca se queda sin presupuesto — exactamente el agente que no existe en producción.

`PolicyEngine.evaluatePolicyForToolCall` deniega por defecto (Default Deny, CH-05 §5) precisamente
para los casos en que algo debería detenerse — pero ese resultado nunca ha tenido, hasta ahora, un
destino real dentro de una ejecución completa. `AgentRunStatus.WAITING_FOR_HUMAN` (CH-01 §6) y el
lifecycle de dos estados de `HumanInteractionRequest` (CH-06 §12) existen, ambos, desde hace varios
capítulos, sin que ninguna transición real los conecte. Y `AgentRunStatus.FAILED`/`CANCELLED`/
`EXPIRED` (CH-01 §6) — tres de los once estados que Article V exige — nunca han sido, hasta este
capítulo, el resultado de ningún pseudocódigo real, a pesar de que `ExecutionController` sabe
exactamente cuándo cada uno correspondería (CH-07 §12).

Necesitamos, por fin, el resto de la traza real: qué recibe el modelo cuando su propuesta se
deniega; cómo entra y sale una ejecución de una espera humana real, sin que eso exija mantener un
proceso vivo mientras tanto (Article VIII); y hacia qué estado terminal exacto transiciona un run
cuando su presupuesto se agota o alguien lo cancela.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los veintiún contratos y los once componentes — más `runAgentTurnEndToEnd`/`emitAndDistribute`
(CH-12) — no bastan porque:

- `runAgentTurnEndToEnd` (CH-12 §11) se detiene, con un `RETURN` explícito, en cada uno de los tres
  puntos citados en la seccion 1 — documentado con total honestidad en su propia seccion 15/18,
  nunca oculto, pero tampoco resuelto;
- `HumanInteractionService.createHumanInteractionRequest`/`resolveHumanInteractionRequest`
  (CH-06 §11) llevan siete capítulos publicadas y nunca han sido invocadas con una
  `PolicyDecision`/`HumanInteractionRequest` real producida dentro de una ejecución — solo con
  datos de ejemplo dentro de su propio capítulo;
- `AgentRunStatus.WAITING_FOR_HUMAN`/`FAILED`/`CANCELLED`/`EXPIRED` (CH-01 §6) siguen siendo,
  después de doce capítulos reales, cuatro de los once valores del `ENUM` que ningún pseudocódigo
  de este libro ha usado jamás para construir un `AgentState` real;
- nada, hasta este capítulo, demuestra con código que `ToolRuntime.executeToolCall` (CH-02)
  realmente **no** se invoca cuando la policy deniega — Article VI, Execution Rule 3 ("las
  policies se evalúan antes del side effect") sigue siendo una regla que ningún turno completo, de
  principio a fin, ha ejercitado en su forma negativa.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la
> secuencia `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una
> entidad que no haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT`
> registrado — **no magic entities**. Este capítulo hereda exactamente la misma disciplina que
> CH-12 ya aplicó en su forma más estricta: no define ni un solo `STRUCT`/`ENUM`/`COMPONENT`
> nuevo — cada entidad que su pseudocódigo utiliza ya estaba registrada, o se documenta aquí por
> referencia (seccion 6), exactamente como CH-12 ya hizo con `ExecutionUsage`.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-05   Side effects pass through policy.
           Primera vez que este principio se cumple también en su forma negativa dentro de una
           ejecución real: runAgentTurnWithPolicyDenial (seccion 11) nunca invoca executeToolCall
           cuando evaluatePolicyForToolCall ya devolvió DENY.
    P-10   The harness owns execution state—not the model.
           terminateAgentRunOperationally (seccion 11) construye, por primera vez con código real,
           un AgentState con status = FAILED/CANCELLED/EXPIRED — el harness, nunca el modelo,
           decide ese desenlace.
    P-13   Authorization is deterministic and external to the LLM.
           El camino DENY de este capítulo nunca consulta al modelo para decidir si la denegación
           es correcta — la observación que el modelo recibe es una consecuencia de la decisión ya
           tomada, no una negociación con él.

Invariants preserved
    INV-06   Todo side effect pasa por PolicyEngine.
             Primera cita literal de este invariante en su forma negativa con ejecución real:
             ningún side effect ocurre cuando PolicyEngine deniega, ni siquiera dentro del camino
             de aprobación humana rechazada (resumeAfterHumanResolution, rama REJECTED).
    INV-09   Todo AgentRun tiene límites explícitos.
             Primera vez que un ExecutionDecision con outcome = STOP produce, con código real, el
             AgentRunStatus terminal correspondiente (terminateAgentRunOperationally).
    INV-10   Todo AgentRun debe poder cancelarse.
             Primera vez que ExecutionDecision.outcome = CANCELLED produce, con código real, un
             AgentState con status = CANCELLED.
    INV-14   Human Interaction nunca depende de una interfaz particular.
             beginToolApprovalPause/resumeAfterHumanResolution invocan createHumanInteractionRequest/
             resolveHumanInteractionRequest sin que este capítulo introduzca ningún campo ni
             concepto de canal — la primera invocación real de ambas funciones respeta la misma
             frontera que CH-06 ya había declarado.
    INV-15   Una acción que requiere aprobación no puede ejecutarse antes de una resolución
             válida.
             Primera cita literal de este invariante con ejecución real de punta a punta:
             resumeAfterHumanResolution nunca invoca executeToolCall antes de que
             resolveHumanInteractionRequest haya producido una HumanInteractionResolution real con
             outcome = APPROVED.
    INV-18   Toda acción significativa produce un evento observable.
             Los tres caminos de este capítulo distribuyen, cada uno, su propio AgentEvent real vía
             emitAndDistribute (CH-12) — incluida, por primera vez, HUMAN_INTERACTION_REQUESTED/
             HUMAN_INTERACTION_RESOLVED dentro de una ejecución real (ver seccion 14).
    INV-19   Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy
             relevante.
             El mismo ExecutionContext que runAgentTurnEndToEnd (CH-12) ya construyó sobrevive,
             sin cambiar, a través de cada una de las cinco funciones de este capítulo — el mismo
             traceId correlaciona una denegación, una espera humana o una terminación con el resto
             del run.
    INV-20   Todo error operacional pertenece a una categoría conocida.
             Este capítulo no introduce ninguna categoría nueva de ErrorCategory — reutiliza POLICY
             (denegación y rechazo humano), BUDGET/CANCELLATION (terminación) y VALIDATION
             (precondiciones de las cinco funciones nuevas), ver seccion 13.

Component ownership changes
    Ninguno. introduces_components: [] — igual que CH-12, este capítulo no instala ningún
    componente nuevo, y no modifica ni un solo campo owns/does_not_own/consumes/produces/
    dependencies de ninguna de las once fichas ya registradas.

Lifecycle changes
    Ninguna modificación a AgentRunStatus (C-013): sigue siendo, sin cambios, el mismo ENUM de
    once estados. Este capítulo es, en cambio, el primero en construir con código real un
    AgentState en WAITING_FOR_HUMAN, FAILED, CANCELLED y EXPIRED — los cuatro valores del ENUM
    que CH-01..CH-12, entre todos, nunca habían alcanzado.

Security implications
    Este capítulo cierra, con código real, la mitad de Article VI/VIII/IX que CH-12 dejó sin
    ejercitar: qué pasa cuando la respuesta es no. Ver seccion 15 para el análisis completo.

Observability implications
    Primera ejecución real, en este libro, de HUMAN_INTERACTION_REQUESTED y
    HUMAN_INTERACTION_RESOLVED (CH-06 §14) hacia EventBus.distributeEvent (CH-09) — exactamente lo
    que la interleavedQuestion IQ-CH12-05 de CH-12 dejó como pregunta abierta.

Deterministic vs agentic boundary
    Sin cambios de fondo: los tres caminos de este capítulo dependen de PolicyDecision/
    ExecutionDecision/HumanInteractionResolution, los tres ya determinísticos desde sus propios
    capítulos — ninguna rama nueva de este capítulo consulta al modelo para decidir su propio
    desenlace.
```

## 5. Conceptos Nuevos (New Concepts)

Este capítulo no introduce ningún concepto que amerite una entrada propia en
`registry/glossary.yaml` (que, deliberadamente, no toca — mismo precedente que CH-12 §5). Introduce
dos ideas puramente narrativas:

- **Camino de gobierno (Governance Path)**: cualquiera de los tres desenlaces reales que CH-12
  dejó pendientes — denegación, aprobación humana pendiente, o terminación operacional — en
  oposición al "camino feliz" que CH-12 ya tituló. Es lo que este capítulo, en su totalidad,
  demuestra con código real (seccion 11).
- **Punto de bifurcación heredado (Inherited Fork Point)**: cada uno de los tres `RETURN`
  explícitos de `runAgentTurnEndToEnd` (CH-12 §11, citados en la seccion 1) que este capítulo
  interpreta como el lugar exacto donde una función nueva reemplazaría esa terminación temprana —
  sin que ese reemplazo exista todavía como una llamada real dentro del cuerpo de CH-12 (ver
  seccion 9/18: cablear esa sustitución dentro de `runAgentTurnEndToEnd` mismo sigue, deliberadamente,
  fuera de este capítulo, porque el encargo prohíbe modificar el pseudocódigo ya publicado de CH-12).

## 6. Nuevas Estructuras de Datos (New Data Structures)

**Este capítulo no introduce ningún `STRUCT` ni `ENUM` nuevo.** Reutiliza, sin modificar ni un solo
campo, los veintiún contratos ya registrados (`C-001`..`C-021`) — todos disponibles automáticamente
porque `CH-00`..`CH-12` son, todos, estrictamente anteriores a este capítulo en `book/book.yaml`.

Tres tipos embebidos, sin `C-XXX` propio, necesitan documentarse aquí por referencia — exactamente
el mismo mecanismo que CH-12 §6 ya usó para `ExecutionUsage` (la disponibilidad de un capítulo no
es acumulativa para tipos sin contrato propio, `scripts/lib/chapter-parser.js`, verificado con
`./scripts/validate-chapter`, primera corrida):

| Identificador (heredado, sin `C-XXX` propio) | Introducido en | Rol en este capítulo |
|---|---|---|
| `ExecutionUsage` | CH-07 §6 | tipo del parámetro `usage` que `resumeTurnWithObservation` y `terminateAgentRunOperationally` pasan a `evaluateExecutionContinuation` (CH-07) |
| `HumanInteractionOutcome` | CH-06 §6 | tipo del parámetro `outcome` de `resumeAfterHumanResolution`, que ese mismo parámetro reenvía a `resolveHumanInteractionRequest` (CH-06) |
| `ActorId` | CH-06 §6 | tipo del parámetro `resolvedBy` de `resumeAfterHumanResolution`, reenviado sin cambios a `resolveHumanInteractionRequest` (CH-06) |

No fue necesario redeclarar `AgentEventType`: a diferencia de CH-12, ninguna función de este
capítulo necesita declarar una variable local de ese tipo — cada llamada a `emitAndDistribute`
recibe su `eventType` como un valor literal del `ENUM` (`POLICY_EVALUATED`,
`HUMAN_INTERACTION_REQUESTED`, `HUMAN_INTERACTION_RESOLVED`, `EXECUTION_EVALUATED`,
`TOOL_CALL_COMPLETED`/`TOOL_CALL_FAILED`, `RUN_COMPLETED`/`TURN_CONTINUED`,
`SESSION_CHECKPOINT_CREATED`, `RUN_FAILED`), nunca a través de una variable tipada. Tampoco fue
necesario introducir ninguna primitiva de generación de identificador nueva: `newMessageId()`
(CH-12), `newEventId()`/`now()` (CH-00) cubren todo lo que este capítulo necesita.

**Unchanged**: ningún otro tipo heredado cambia de forma, y `registry/contracts.yaml` permanece,
después de este capítulo, exactamente en los veintiún contratos que CH-05/CH-06 dejaron
registrados.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

**Este capítulo no introduce ningún contrato nuevo.** `introduces_contracts: []` en el
frontmatter — `registry/contracts.yaml` permanece, después de este capítulo, exactamente en
`C-001`..`C-021`.

## 8. Responsabilidades de Componentes (Component Responsibilities)

**Este capítulo no introduce ningún componente nuevo.** `introduces_components: []` en el
frontmatter — `registry/components.yaml` permanece, después de este capítulo, exactamente en
`CMP-001`..`CMP-011`, sin que ninguna de sus once fichas cambie un solo campo.

Lo que este capítulo sí hace es escribir cinco funciones nuevas y propias — ninguna es un método de
ningún componente registrado — que se conectan, cada una, a un punto exacto de `runAgentTurnEndToEnd`
(CH-12 §11):

```text
Función nueva                      Punto de bifurcación heredado (CH-12 §11)     Camino que cierra
--------------------------------   --------------------------------------------  -----------------
resumeTurnWithObservation          (helper compartido, no bifurca por sí misma)   —
runAgentTurnWithPolicyDenial        IF decisionOne.outcome != ALLOW → DENY        DENY
beginToolApprovalPause              IF decisionOne.outcome != ALLOW → REQUIRE_APPROVAL  REQUIRE_APPROVAL (pausa)
resumeAfterHumanResolution          (invocada después de beginToolApprovalPause,
                                     nunca dentro del mismo turno síncrono)        REQUIRE_APPROVAL (reanudación)
terminateAgentRunOperationally      IF continuationOne/Two.outcome != CONTINUE     STOP / CANCELLED
                                     → STOP / CANCELLED
```

Cada una de las once fichas ya publicadas se respeta exactamente igual que en CH-12:
`PolicyEngine.evaluatePolicyForToolCall` sigue sin decidir qué observación construir cuando
deniega; `HumanInteractionService` sigue sin decidir si una acción requiere aprobación ni si el
turno debe continuar; `ExecutionController.evaluateExecutionContinuation` sigue sin decidir ningún
`AgentRunStatus` — `ExecutionDecision` (C-017) no tiene, ni tuvo nunca, un campo que lo exprese
(CH-07 §11). Ninguna decisión cambió de dueño — este capítulo solo escribe, por fin, el código que
traduce cada decisión ya tomada hacia su consecuencia real en el `AgentState`.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
resumeTurnWithObservation (función de integración, no un componente registrado)
    invoca → evaluateExecutionContinuation (CMP-007)
    invoca → assembleContextSnapshot (CMP-004)
    invoca → invokeModelForTurn (CMP-003)
    invoca → runTurn (CMP-001)
    invoca → createOrUpdateSessionCheckpoint (CMP-010)

runAgentTurnWithPolicyDenial
    invoca → evaluatePolicyForToolCall (CMP-005)
    invoca → resumeTurnWithObservation (este capítulo)

beginToolApprovalPause
    invoca → evaluatePolicyForToolCall (CMP-005)
    invoca → createHumanInteractionRequest (CMP-006)
    invoca → createOrUpdateSessionCheckpoint (CMP-010)

resumeAfterHumanResolution
    invoca → resolveHumanInteractionRequest (CMP-006)
    invoca → executeToolCall (CMP-002)               [solo si outcome = APPROVED]
    invoca → resumeTurnWithObservation (este capítulo)

terminateAgentRunOperationally
    invoca → evaluateExecutionContinuation (CMP-007)
    invoca → createOrUpdateSessionCheckpoint (CMP-010)

(las cinco funciones invocan → distributeEvent (CMP-009), vía emitAndDistribute, CH-12)
```

**Límite real de este capítulo, documentado con la misma honestidad que CH-12 §9.**
`registry/components.yaml` **no se modifica**: ninguna de las once fichas agrega, en su propio
campo `dependencies`, a ninguno de sus vecinos. Esto tiene, otra vez, la misma consecuencia
mecánica que CH-12 ya encontró y verificó (ver seccion 17): `scripts/lib/mindmap.js` deriva las
aristas `DEPENDS_ON`/`PRODUCES`/`CONSUMES` exclusivamente de los campos que cada componente ya
declaraba en su propio capítulo de introducción — nunca de la prosa ni del pseudocódigo de un
capítulo posterior que simplemente invoca esas funciones. `diagrams/mindmap/chapter-13.diagram` no
gana ninguna arista nueva por ese mecanismo, exactamente como no las ganó `chapter-12.diagram` — la
seccion 17 documenta la cifra real verificada.

Un límite adicional, propio de este capítulo: ninguna de las cinco funciones nuevas se invoca desde
dentro de `runAgentTurnEndToEnd` (CH-12) — el encargo prohíbe reabrir su pseudocódigo ya publicado.
Cablear la sustitución real de los tres `RETURN` (seccion 1/5) por una llamada real a una de estas
cinco funciones sigue siendo, honestamente, trabajo de una revisión futura de CH-12 (ver seccion 18).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14), una por cada camino de gobierno:

**Vista 1 — Componentes**

```text
Camino DENY:
    CapabilityRegistry → PolicyEngine → [runAgentTurnWithPolicyDenial] → ContextEngine →
    ModelGateway → AgentLoop → SessionManager (EventBus recibe cada AgentEvent)

Camino REQUIRE_APPROVAL:
    CapabilityRegistry → PolicyEngine → HumanInteractionService → [pausa: fin de la función] ...
    ... [tiempo indefinido, sin proceso abierto] ... → HumanInteractionService →
    ToolRuntime (si APPROVED) → ContextEngine → ModelGateway → AgentLoop → SessionManager

Camino STOP / CANCELLED:
    ExecutionController → [terminateAgentRunOperationally] → SessionManager
```

**Vista 2 — Sequence**

```text
PolicyDecision (outcome = DENY)
   │ (producida por evaluatePolicyForToolCall dentro de runAgentTurnWithPolicyDenial)
   ▼
runAgentTurnWithPolicyDenial
   │ executeToolCall NUNCA se invoca (Article VI, Execution Rule 3)
   │ construye AgentMessage(role = TOOL, content = decision.reason) como observación
   │ resumedState = AgentState(status = RUNNING, ...)
   ▼
resumeTurnWithObservation
   │ (mismo patrón que la segunda mitad de runAgentTurnEndToEnd, CH-12 §11)
   ▼
AgentState (COMPLETED o el estado que el segundo turno produzca)

---

PolicyDecision (outcome = REQUIRE_APPROVAL)
   ▼
beginToolApprovalPause
   │ createHumanInteractionRequest(decision, APPROVAL, execution, agentId) → HumanInteractionRequest(PENDING)
   │ pausedState = AgentState(status = WAITING_FOR_HUMAN, ...)
   │ RETURN pausedState — la función termina aquí (Article VIII)
   ▼
[ningún proceso espera — tiempo indefinido]
   ▼
resumeAfterHumanResolution(pausedState, request, outcome, resolvedBy, ...)
   │ resolveHumanInteractionRequest(request, outcome, NULL, resolvedBy, ...) → HumanInteractionResolution
   │ resumedState = AgentState(status = RUNNING, ...)
   │ ¿resolution.outcome == APPROVED?
   │     sí → executeToolCall(call, ..., TRUE, TRUE, ...) → ToolResult → observación real
   │     no → observación de rechazo (misma forma que el camino DENY)
   ▼
resumeTurnWithObservation
   ▼
AgentState (COMPLETED o el estado que el segundo turno produzca)

---

ExecutionDecision (outcome = STOP, stopReason = MAX_RUNTIME_EXCEEDED | ... | outcome = CANCELLED)
   ▼
terminateAgentRunOperationally
   │ ¿outcome == CANCELLED?           → terminalStatus = CANCELLED
   │ ¿stopReason == MAX_RUNTIME_EXCEEDED? → terminalStatus = EXPIRED
   │ (cualquier otro stopReason)      → terminalStatus = FAILED
   │ terminalState = AgentState(status = terminalStatus, ...)
   ▼
AgentState (FAILED | CANCELLED | EXPIRED) — desenlace terminal real
```

**Vista 3 — Pseudocódigo**

Ver §11: las cinco funciones son la primera formalización ejecutable, en todo este libro, de "qué
pasa cuando el sistema dice que no, cuando alguien tiene que decidir en su lugar, o cuando el
tiempo o el presupuesto se agotan" — construidas exclusivamente a partir de funciones ya publicadas
por CH-01..CH-12, sin modificar ninguna.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya registradas desde CH-00..CH-12, más `ExecutionUsage`,
`HumanInteractionOutcome` y `ActorId` (seccion 6, disponibles por referencia, no por
introducción).

```pseudocode
FUNCTION resumeTurnWithObservation(
    resumedState: AgentState,
    execution: ExecutionContext,
    candidates: List<AgentMessage>,
    session: Optional<SessionState>,
    activeSubscriptions: List<EventSubscription>,
    usage: ExecutionUsage,
    finalModelContent: Value
) -> AgentState

    continuation: ExecutionDecision = evaluateExecutionContinuation(
        resumedState, execution, execution.budget, usage, FALSE
    )
    emitAndDistribute(
        EXECUTION_EVALUATED, execution, resumedState.agentId, continuation, activeSubscriptions
    )

    IF continuation.outcome != CONTINUE
        // terminateAgentRunOperationally (mas abajo en esta misma seccion) es quien resolveria
        // este desenlace hacia un AgentRunStatus terminal real — esta funcion se detiene aqui,
        // exactamente como resumeTurnWithObservation ya lo hacia en runAgentTurnEndToEnd (CH-12).
        RETURN resumedState
    END

    snapshot: ContextSnapshot = assembleContextSnapshot(candidates, execution, resumedState.agentId)
    emitAndDistribute(
        CONTEXT_SNAPSHOT_ASSEMBLED, execution, resumedState.agentId, snapshot, activeSubscriptions
    )

    pendingMessages: List<AgentMessage> = []
    FOR EACH block IN snapshot.blocks
        pendingMessages.append(AgentMessage(
            id = newMessageId(),
            role = USER,
            content = block.content,
            timestamp = now()
        ))
    END

    response: ModelResponse = invokeModelForTurn(
        resumedState, execution, pendingMessages, TRUE, TRUE, FALSE, "", {}, finalModelContent
    )
    emitAndDistribute(
        MODEL_RESPONSE_RECEIVED, execution, resumedState.agentId, response, activeSubscriptions
    )

    modelFinished: Boolean = response.finished
    modelProposesToolCall: Boolean = response.proposedToolCall != NULL

    finalState: AgentState = runTurn(resumedState, execution, modelFinished, modelProposesToolCall)

    IF finalState.status == COMPLETED
        emitAndDistribute(RUN_COMPLETED, execution, finalState.agentId, finalState, activeSubscriptions)
    ELSE
        emitAndDistribute(TURN_CONTINUED, execution, finalState.agentId, finalState, activeSubscriptions)
    END

    finalSession: SessionState = createOrUpdateSessionCheckpoint(
        session, finalState, execution, finalState.agentId
    )
    emitAndDistribute(
        SESSION_CHECKPOINT_CREATED, execution, finalState.agentId, finalSession, activeSubscriptions
    )

    RETURN finalState
END
```

`resumeTurnWithObservation` es una función nueva y propia de este capítulo — no modifica
`runAgentTurnEndToEnd` (CH-12), aunque repite el mismo patrón que su segunda mitad ya estableció:
evaluar continuación operacional, ensamblar contexto, invocar al modelo y correr un turno más,
antes de cerrar el checkpoint. Las tres funciones siguientes la comparten como cola común.

```pseudocode
FUNCTION runAgentTurnWithPolicyDenial(
    turnState: AgentState,
    execution: ExecutionContext,
    call: ToolCall,
    candidatesSoFar: List<AgentMessage>,
    session: Optional<SessionState>,
    activeSubscriptions: List<EventSubscription>,
    usage: ExecutionUsage,
    finalModelContent: Value
) -> AgentState

    decision: PolicyDecision = evaluatePolicyForToolCall(call, execution, turnState.agentId)
    emitAndDistribute(POLICY_EVALUATED, execution, turnState.agentId, decision, activeSubscriptions)

    IF decision.outcome != DENY
        error: HarnessError = HarnessError(
            category = VALIDATION,
            code = "NOT_A_POLICY_DENIAL",
            message = "runAgentTurnWithPolicyDenial fue invocada sobre una PolicyDecision cuyo outcome no es DENY",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW error
    END

    // executeToolCall (ToolRuntime, CH-02) nunca se invoca en esta rama: la policy ya dijo que
    // no, y las policies se evaluan antes de cualquier side effect (ver seccion 3).

    denialMessage: AgentMessage = AgentMessage(
        id = newMessageId(),
        role = TOOL,
        content = decision.reason,
        timestamp = now()
    )
    candidates: List<AgentMessage> = candidatesSoFar
    candidates.append(denialMessage)

    resumedState: AgentState = AgentState(
        runId = turnState.runId,
        sessionId = turnState.sessionId,
        agentId = turnState.agentId,
        status = RUNNING,
        currentTurn = turnState.currentTurn
    )

    RETURN resumeTurnWithObservation(
        resumedState, execution, candidates, session, activeSubscriptions, usage, finalModelContent
    )
END
```

`call` llega ya resuelto — la misma precondición que `evaluatePolicyForToolCall` (CH-05) y
`runAgentTurnEndToEnd` (CH-12 §11, paso 7) ya asumían: `CapabilityRegistry.resolveModelProposedToolCall`
(CH-08) ya corrió antes, en el mismo punto donde CH-12 §11 ya lo demuestra. Este capítulo no repite
ese paso porque no varía entre el camino feliz y el camino `DENY` — lo único que varía es el
resultado de `evaluatePolicyForToolCall` en adelante.

```pseudocode
FUNCTION beginToolApprovalPause(
    turnState: AgentState,
    execution: ExecutionContext,
    call: ToolCall,
    session: Optional<SessionState>,
    activeSubscriptions: List<EventSubscription>
) -> AgentState

    decision: PolicyDecision = evaluatePolicyForToolCall(call, execution, turnState.agentId)
    emitAndDistribute(POLICY_EVALUATED, execution, turnState.agentId, decision, activeSubscriptions)

    IF decision.outcome != REQUIRE_APPROVAL
        error: HarnessError = HarnessError(
            category = VALIDATION,
            code = "NOT_A_REQUIRE_APPROVAL_DECISION",
            message = "beginToolApprovalPause fue invocada sobre una PolicyDecision cuyo outcome no es REQUIRE_APPROVAL",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW error
    END

    request: HumanInteractionRequest = createHumanInteractionRequest(
        decision, APPROVAL, execution, turnState.agentId
    )
    emitAndDistribute(
        HUMAN_INTERACTION_REQUESTED, execution, turnState.agentId, request, activeSubscriptions
    )

    pausedState: AgentState = AgentState(
        runId = turnState.runId,
        sessionId = turnState.sessionId,
        agentId = turnState.agentId,
        status = WAITING_FOR_HUMAN,
        currentTurn = turnState.currentTurn
    )

    finalSession: SessionState = createOrUpdateSessionCheckpoint(
        session, pausedState, execution, pausedState.agentId
    )
    emitAndDistribute(
        SESSION_CHECKPOINT_CREATED, execution, pausedState.agentId, finalSession, activeSubscriptions
    )

    // la funcion termina aqui: ningun proceso queda esperando la resolucion humana; la reanudacion
    // real ocurre, mas tarde y por separado, en resumeAfterHumanResolution.

    RETURN pausedState
END
```

```pseudocode
FUNCTION resumeAfterHumanResolution(
    pausedState: AgentState,
    execution: ExecutionContext,
    request: HumanInteractionRequest,
    outcome: HumanInteractionOutcome,
    resolvedBy: ActorId,
    call: ToolCall,
    candidatesSoFar: List<AgentMessage>,
    session: Optional<SessionState>,
    activeSubscriptions: List<EventSubscription>,
    usage: ExecutionUsage,
    toolExecutionSucceeded: Boolean,
    toolExecutionOutput: Value,
    finalModelContent: Value
) -> AgentState

    resolution: HumanInteractionResolution = resolveHumanInteractionRequest(
        request, outcome, NULL, resolvedBy, execution, pausedState.agentId
    )
    emitAndDistribute(
        HUMAN_INTERACTION_RESOLVED, execution, pausedState.agentId, resolution, activeSubscriptions
    )

    resumedState: AgentState = AgentState(
        runId = pausedState.runId,
        sessionId = pausedState.sessionId,
        agentId = pausedState.agentId,
        status = RUNNING,
        currentTurn = pausedState.currentTurn
    )

    candidates: List<AgentMessage> = candidatesSoFar

    IF resolution.outcome == APPROVED
        result: ToolResult = executeToolCall(
            call, execution, resumedState.agentId, TRUE, TRUE,
            toolExecutionSucceeded, toolExecutionOutput
        )

        IF result.succeeded
            emitAndDistribute(TOOL_CALL_COMPLETED, execution, resumedState.agentId, result, activeSubscriptions)
        ELSE
            emitAndDistribute(TOOL_CALL_FAILED, execution, resumedState.agentId, result, activeSubscriptions)
        END

        observation: AgentMessage = AgentMessage(
            id = newMessageId(),
            role = TOOL,
            content = result,
            timestamp = now()
        )
        candidates.append(observation)
    ELSE
        // resolution.outcome == REJECTED: la accion no se ejecuta, exactamente como en el camino
        // DENY — pero aqui la rechazo un humano, no una policy rule. HumanInteractionResolution
        // no trae un HarnessError propio (rechazar es un desenlace valido, no un fallo de
        // HumanInteractionService), asi que esta funcion construye la observacion equivalente.
        rejection: HarnessError = HarnessError(
            category = POLICY,
            code = "HUMAN_APPROVAL_REJECTED",
            message = "La aprobacion humana requerida para este ToolCall fue rechazada",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        denialMessage: AgentMessage = AgentMessage(
            id = newMessageId(),
            role = TOOL,
            content = rejection,
            timestamp = now()
        )
        candidates.append(denialMessage)
    END

    RETURN resumeTurnWithObservation(
        resumedState, execution, candidates, session, activeSubscriptions, usage, finalModelContent
    )
END
```

`resumeAfterHumanResolution` asume que `outcome` corresponde al `type = APPROVAL` de `request` —
`resolveHumanInteractionRequest` (CH-06 §11) ya verifica esa correspondencia con
`outcomeMatchesRequestType` y lanza `OUTCOME_TYPE_MISMATCH` si no se cumple, así que esta función
nunca necesita repetir esa verificación. Nótese que `executeToolCall` recibe `TRUE`/`TRUE` para
`capabilityResolved`/`inputValid` — exactamente el mismo hecho ya verificado que CH-12 §11
justificaba (la propuesta ya fue resuelta por `CapabilityRegistry` antes de que `PolicyEngine`
evaluara), más un tercer hecho verificado que solo este capítulo puede aportar: la aprobación
humana requerida ya se resolvió con `outcome = APPROVED`.

```pseudocode
FUNCTION terminateAgentRunOperationally(
    state: AgentState,
    execution: ExecutionContext,
    budget: ExecutionBudget,
    usage: ExecutionUsage,
    cancellationRequested: Boolean,
    session: Optional<SessionState>,
    activeSubscriptions: List<EventSubscription>
) -> AgentState

    continuation: ExecutionDecision = evaluateExecutionContinuation(
        state, execution, budget, usage, cancellationRequested
    )
    emitAndDistribute(
        EXECUTION_EVALUATED, execution, state.agentId, continuation, activeSubscriptions
    )

    IF continuation.outcome == CONTINUE
        error: HarnessError = HarnessError(
            category = VALIDATION,
            code = "NOT_AN_OPERATIONAL_STOP",
            message = "terminateAgentRunOperationally fue invocada sobre una ExecutionDecision cuyo outcome es CONTINUE",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW error
    END

    terminalStatus: AgentRunStatus = FAILED

    IF continuation.outcome == CANCELLED
        terminalStatus = CANCELLED
    ELSE IF continuation.stopReason == MAX_RUNTIME_EXCEEDED
        terminalStatus = EXPIRED
    END

    // mapeo real (CH-07 seccion 12, documentado antes solo en prosa): CANCELLED -> CANCELLED;
    // STOP + MAX_RUNTIME_EXCEEDED -> EXPIRED; STOP + cualquier otro stopReason -> FAILED.

    terminalState: AgentState = AgentState(
        runId = state.runId,
        sessionId = state.sessionId,
        agentId = state.agentId,
        status = terminalStatus,
        currentTurn = state.currentTurn
    )

    // este capitulo reutiliza RUN_FAILED para los tres desenlaces terminales que no son
    // COMPLETED (ver seccion 14 para el hallazgo real sobre este reuso).
    emitAndDistribute(RUN_FAILED, execution, terminalState.agentId, terminalState, activeSubscriptions)

    finalSession: SessionState = createOrUpdateSessionCheckpoint(
        session, terminalState, execution, terminalState.agentId
    )
    emitAndDistribute(
        SESSION_CHECKPOINT_CREATED, execution, terminalState.agentId, finalSession, activeSubscriptions
    )

    RETURN terminalState
END
```

Nótese lo que ninguna de las cinco funciones hace: ninguna decide por su cuenta si una acción está
permitida (`evaluatePolicyForToolCall` sigue siendo quien decide `DENY`/`REQUIRE_APPROVAL`),
ninguna decide si una aprobación humana se requiere o cómo se resuelve
(`HumanInteractionService` sigue siendo quien lo posee), y ninguna decide si el run puede continuar
operacionalmente (`ExecutionController` sigue siendo quien lo posee) — cada una solo traduce una
decisión ya tomada hacia su consecuencia real en `AgentState`/`AgentMessage`, exactamente la misma
disciplina que `runAgentTurnEndToEnd` (CH-12 §11) ya estableció para el camino feliz.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013): sigue siendo, sin cambios, el
mismo `ENUM` de once estados. Es, en cambio, el primer capítulo en ejercitar con pseudocódigo real
cada una de las siguientes cuatro transiciones — las cuatro que CH-01..CH-12, entre todos, nunca
habían alcanzado:

```text
WAITING_FOR_TOOL --[PolicyDecision.outcome = DENY]--> RUNNING
    (runAgentTurnWithPolicyDenial: la observación de la denegación ya está en candidates)

WAITING_FOR_TOOL --[PolicyDecision.outcome = REQUIRE_APPROVAL]--> WAITING_FOR_HUMAN
    (beginToolApprovalPause: primera vez que este libro alcanza este estado)

WAITING_FOR_HUMAN --[HumanInteractionResolution.outcome = APPROVED | REJECTED]--> RUNNING
    (resumeAfterHumanResolution: primera vez que este libro sale de este estado)

RUNNING --[ExecutionDecision.outcome = CANCELLED]--> CANCELLED
RUNNING --[ExecutionDecision.outcome = STOP, stopReason = MAX_RUNTIME_EXCEEDED]--> EXPIRED
RUNNING --[ExecutionDecision.outcome = STOP, cualquier otro stopReason]--> FAILED
    (terminateAgentRunOperationally: primera vez que este libro alcanza cualquiera de los tres)
```

**Por qué esto no invade la propiedad de `AgentLoop` sobre `AgentRunStatus` (Article IV).** Ninguna
de las cinco funciones decide, por su cuenta, si el ciclo cognitivo debe continuar — cada
transición que construyen refleja una decisión que un componente distinto ya tomó
(`PolicyEngine`, `HumanInteractionService` o `ExecutionController`), exactamente el mismo
razonamiento que CH-12 §12 ya usó para justificar que él mismo construyera la transición
`INITIALIZING → RUNNING` sin invadir a `AgentCore`/`AgentLoop`: `runTurn` (CH-01) sigue siendo la
única función que decide una transición a partir de que **el modelo** terminó de razonar
(`modelFinished`/`modelProposesToolCall`) — estas cinco funciones nunca calculan esos dos
booleanos ni invocan `runTurn` con datos distintos de los que `resumeTurnWithObservation` ya deriva
de un `ModelResponse` real.

## 13. Semántica de Fallos (Failure Semantics)

Este capítulo no agrega ningún valor nuevo a `ErrorCategory` (CH-00, extendido por última vez en
CH-06 con `HUMAN_INTERACTION`) — reutiliza, sin cambios, las categorías ya declaradas:

```text
VALIDATION
    runAgentTurnWithPolicyDenial invocada sobre una PolicyDecision cuyo outcome no es DENY
        → código: NOT_A_POLICY_DENIAL (ver §11)
    beginToolApprovalPause invocada sobre una PolicyDecision cuyo outcome no es REQUIRE_APPROVAL
        → código: NOT_A_REQUIRE_APPROVAL_DECISION (ver §11)
    terminateAgentRunOperationally invocada sobre una ExecutionDecision cuyo outcome es CONTINUE
        → código: NOT_AN_OPERATIONAL_STOP (ver §11)

POLICY
    PolicyDecision.outcome = DENY — reason ya construido por evaluatePolicyForToolCall (CH-05),
    reutilizado sin cambios como el content de la observación (runAgentTurnWithPolicyDenial)
    HumanInteractionResolution.outcome = REJECTED — HUMAN_APPROVAL_REJECTED, construido por
    resumeAfterHumanResolution (este capítulo), no por HumanInteractionService: rechazar es un
    desenlace válido de esa resolución, no un fallo de CMP-006 (ver §11)

BUDGET / CANCELLATION
    ExecutionDecision.outcome = STOP / CANCELLED — reason ya construido por
    evaluateExecutionContinuation (CH-07), reutilizado sin cambios dentro de la
    ExecutionDecision que terminateAgentRunOperationally recibe
```

**La única construcción de `HarnessError` que este capítulo hace por su cuenta**
(`HUMAN_APPROVAL_REJECTED`, categoría `POLICY`) merece una nota honesta: `runAgentTurnEndToEnd`
(CH-12 §13) declaró explícitamente que "nunca construye un `HarnessError` por su cuenta" — pero esa
regla aplicaba al camino feliz, donde cada fallo ya tenía un componente dueño que lo clasificaba.
Aquí no existe ese dueño: `HumanInteractionResolution` (C-016, CH-06) no tiene ningún campo de
error — `REJECTED` es, para `HumanInteractionService`, un resultado tan válido como `APPROVED`. Que
el modelo necesite ver esa negativa con la misma forma que una denegación de policy es, en cambio,
una decisión de **este** capítulo de integración — documentada aquí explícitamente, no oculta.

## 14. Eventos Producidos (Events Produced)

Este capítulo no agrega ningún valor nuevo a `AgentEventType` (CH-11, veinte valores). Produce, por
primera vez en este libro, que los siguientes valores lleguen a `EventBus.distributeEvent` dentro
de una ejecución real que SÍ recorre un camino de gobierno:

```text
POLICY_EVALUATED             (runAgentTurnWithPolicyDenial / beginToolApprovalPause, outcome ≠ ALLOW)
HUMAN_INTERACTION_REQUESTED   (beginToolApprovalPause — primera vez con ejecución real)
HUMAN_INTERACTION_RESOLVED    (resumeAfterHumanResolution — primera vez con ejecución real)
EXECUTION_EVALUATED           (resumeTurnWithObservation / terminateAgentRunOperationally, outcome ≠ CONTINUE)
TOOL_CALL_COMPLETED/FAILED    (resumeAfterHumanResolution, rama APPROVED)
RUN_FAILED                    (terminateAgentRunOperationally — para FAILED, CANCELLED y EXPIRED)
```

`HUMAN_INTERACTION_REQUESTED`/`HUMAN_INTERACTION_RESOLVED` (CH-06) llevaban siete capítulos
declarados sin que ninguna ejecución real los hubiera producido — exactamente lo que
`IQ-CH12-05` (CH-12, frontmatter) dejó como pregunta abierta: "¿qué tendría que ocurrir para que
`HUMAN_INTERACTION_REQUESTED` llegara a `distributeEvent`, y por qué `EventBus` no necesitaría
cambiar?". La respuesta es, literalmente, `beginToolApprovalPause` (seccion 11) — y `EventBus`, en
efecto, no cambió ni una línea.

**Hallazgo real, documentado con honestidad (no anticipado por el encargo original).**
`AgentEventType` (CH-11, veinte valores) declara `RUN_COMPLETED` y `RUN_FAILED`, pero **no** declara
ningún valor distinto para un run que termina en `CANCELLED` o en `EXPIRED` — solo esos dos casos
carecen de un valor propio entre los once estados terminales/de espera de `AgentRunStatus`.
`terminateAgentRunOperationally` (seccion 11) reutiliza `RUN_FAILED` para los tres desenlaces
(`FAILED`, `CANCELLED`, `EXPIRED`), confiando en que el `payload` (el `AgentState` completo, con su
`status` real) lleve la distinción real — el `eventType` por sí solo no la lleva. Esto es una
consecuencia real y verificada de que `AgentEventType` no fue extendido en este capítulo (seccion 6:
este capítulo no agrega valores nuevos, a diferencia de CH-02..CH-06). Agregar `RUN_CANCELLED` y
`RUN_EXPIRED` sería una extensión real de `AgentEventType`, fuera del alcance decidido para este
capítulo — se documenta aquí, y en la seccion 18, como deuda intencional hacia una revisión futura.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

Este capítulo cierra, con código real, las tres implicaciones de seguridad que CH-12 §15 dejó
explícitamente abiertas:

- **`PolicyDecision.outcome = DENY`**: `runAgentTurnWithPolicyDenial` demuestra, por primera vez
  con código real en este libro, que `ToolRuntime.executeToolCall` **no** se invoca cuando la
  policy deniega — Article VI, Execution Rule 3 ("las policies se evalúan antes del side effect")
  deja de ser una regla verificable solo en su forma positiva (CH-12) para verificarse también en
  su forma negativa.
- **`PolicyDecision.outcome = REQUIRE_APPROVAL`**: `beginToolApprovalPause`/
  `resumeAfterHumanResolution` cierran, juntas, INV-15 con ejecución real de punta a punta: ninguna
  acción que requirió aprobación se ejecuta antes de que `resolveHumanInteractionRequest` (CH-06)
  produzca una resolución real con `outcome = APPROVED` — y, mientras esa resolución no existe, el
  `AgentRun` permanece en `WAITING_FOR_HUMAN` sin que ningún proceso siga corriendo (Article VIII).
- **`ExecutionDecision.outcome = STOP`/`CANCELLED`**: `terminateAgentRunOperationally` cierra INV-09
  e INV-10 con ejecución real: un run puede, verificablemente, dejar de existir tanto porque su
  presupuesto se agotó como porque alguien lo canceló explícitamente — y ambos casos producen un
  `AgentRunStatus` terminal distinguible (`FAILED`/`EXPIRED` vs. `CANCELLED`).

Ningún componente cambió su frontera para que esto fuera posible — la seguridad de este capítulo
consiste, otra vez, en traducir con honestidad una decisión ya tomada, nunca en inventar una nueva.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST RunAgentTurnWithPolicyDenialNeverInvokesExecuteToolCall
TEST RunAgentTurnWithPolicyDenialThrowsWhenPolicyDecisionOutcomeIsNotDeny
TEST BeginToolApprovalPauseTransitionsToWaitingForHumanOnlyWhenOutcomeIsRequireApproval
TEST BeginToolApprovalPauseReturnsWithoutAnyOpenProcessWaiting
TEST ResumeAfterHumanResolutionNeverInvokesExecuteToolCallBeforeResolutionOutcomeIsApproved
TEST ResumeAfterHumanResolutionProducesTheSamePolicyObservationShapeWhenRejected
TEST TerminateAgentRunOperationallyMapsCancelledStopReasonAndMaxRuntimeExceededToTheCorrectAgentRunStatus
TEST TerminateAgentRunOperationallyThrowsWhenExecutionDecisionOutcomeIsContinue
TEST NoneOfTheFiveNewFunctionsModifiesAnyAlreadyPublishedComponentFunction
```

Ejemplo concreto para el último camino (seccion 11, `terminateAgentRunOperationally`): un
`ExecutionUsage` con `runtimeMsElapsed >= budget.maxRuntimeMs` produce
`ExecutionDecision(outcome = STOP, stopReason = MAX_RUNTIME_EXCEEDED)` → `AgentRunStatus.EXPIRED`;
un `ExecutionUsage` con `toolCallsUsed >= budget.maxToolCalls` produce
`ExecutionDecision(outcome = STOP, stopReason = MAX_TOOL_CALLS_EXCEEDED)` → `AgentRunStatus.FAILED`;
`cancellationRequested = TRUE` produce `ExecutionDecision(outcome = CANCELLED)` →
`AgentRunStatus.CANCELLED` — los tres, verificados contra `evaluateExecutionContinuation` (CH-07
§11) sin modificar esa función.

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.1, después de CH-13)

Constitution
 ├── Article III  — Component Sovereignty (once componentes, sin cambios desde CH-11)
 ├── Article IV   — Decision Ownership (cada fila de la tabla, respetada también en sus
 │                   desenlaces menos permisivos)
 ├── Article V    — Lifecycle (los once estados de AgentRunStatus, todos alcanzados alguna vez
 │                   por un pseudocódigo real de este libro: CH-12 cerró siete, este capítulo
 │                   cierra los cuatro restantes — WAITING_FOR_HUMAN, FAILED, CANCELLED, EXPIRED)
 ├── Article VI   — Execution (Execution Rule 3 verificada también en su forma negativa)
 ├── Article VIII — Human Interaction (ciclo completo ejercitado con ejecución real de punta a
 │                   punta, incluida la pausa sin proceso abierto, Article VIII)
 └── Article IX   — Resources and Budgets (Budget Rule ejercitada hasta su desenlace terminal
                     real, no solo hasta la decisión de detenerse)

Contracts (registry/contracts.yaml)
 └── C-001..C-021  (sin cambios — 21 contratos, idéntico a después de CH-12)

Components (registry/components.yaml)
 └── CMP-001..CMP-011  (sin cambios — 11 componentes, idéntico a después de CH-12)
```

**Hallazgo real, verificado y documentado sin ocultarlo (ver seccion 9).** Igual que CH-12,
`registry/components.yaml` no cambia, así que `diagrams/mindmap/chapter-13.diagram` es, verificado
con `./scripts/build-mind-map`, **idéntico en aristas** a `diagrams/mindmap/chapter-12.diagram` —
un solo nodo nuevo (el nodo `CHAPTER` de `CH-13`), cero aristas `DEPENDS_ON`/`PRODUCES`/`CONSUMES`
nuevas. Es exactamente el mismo hallazgo que CH-12 §3.6/§17 ya documentó, ahora confirmado por
segunda vez con un capítulo de integración distinto: el mecanismo actual del `BookMindMap` no tiene
ningún camino para que un capítulo que no toca el registry agregue esas aristas — sin importar
cuántas funciones reales de integración escriba.

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **`runAgentTurnEndToEnd` (CH-12) sigue sin invocar, dentro de su propio cuerpo, ninguna de las
  cinco funciones de este capítulo**: los tres `RETURN` tempranos que la seccion 1 citó siguen
  ahí, sin cambios — el encargo prohíbe reabrir el pseudocódigo ya publicado de CH-12. Sustituir
  esos tres `RETURN` por una llamada real a `runAgentTurnWithPolicyDenial`/
  `beginToolApprovalPause`/`terminateAgentRunOperationally` sigue siendo, honestamente, trabajo de
  una revisión futura de CH-12.
- **`AgentEventType` sin `RUN_CANCELLED`/`RUN_EXPIRED` propios** (seccion 14): este capítulo
  reutiliza `RUN_FAILED` para los tres desenlaces terminales que no son `COMPLETED`, confiando en
  que el `payload` (el `AgentState.status` real) lleve la distinción — una extensión real de
  `AgentEventType` con dos valores nuevos queda fuera de este alcance.
- **Expiración de una `HumanInteractionRequest` que nadie resuelve nunca**: `HumanInteractionStatus`
  (CH-06 §6) sigue teniendo solo dos estados (`PENDING`/`RESOLVED`) — este capítulo no modela qué
  pasa si una aprobación pendiente nunca se resuelve; `AgentRunStatus.WAITING_FOR_HUMAN` no tiene,
  todavía, ninguna transición de salida por expiración, distinta de una resolución real.
- **Reintento tras `DENY`**: el modelo que ve la observación de una denegación puede, en principio,
  proponer una tool call distinta en el turno siguiente — `resumeTurnWithObservation` ya lo
  permite (el segundo turno vuelve a invocar `invokeModelForTurn` sobre el `ContextSnapshot`
  actualizado), pero este capítulo no construye un escenario de ejemplo que lo demuestre
  explícitamente.
- **Múltiples aprobaciones pendientes concurrentes, o un `ToolCall` que dispara más de una
  `HumanInteractionRequest`**: fuera de alcance, igual que en CH-06.
- Paralelismo de tool calls, ranking semántico real de contexto, Provider Adapters reales,
  algoritmos reales de validación de schema, mecanismo real de alta de `CapabilityDescriptor`,
  autorización sobre quién puede activar un agente ajeno: deuda intencional heredada de
  CH-02..CH-12, sin cambios en este capítulo.
- Reviewers plurales, evals y orquestación multi-agente: explícitamente fuera de alcance de
  BH-v0.1 (igual que todos los capítulos anteriores).

## 19. Siguiente Incremento (Next Increment)

Este capítulo cierra el segundo y último capítulo de integración planeado para BH-v0.1: los once
componentes de Article III (CH-01..CH-11) ya tienen, entre CH-12 y CH-13, una demostración real de
punta a punta tanto de su camino más permisivo como de sus tres caminos de gobierno. No hay, en
este momento del libro, un tercer capítulo de integración planeado — `next_chapter` queda en `null`
en el frontmatter de este capítulo, y `book/chapters/12-integracion-camino-feliz/chapter.md` solo
se modifica en su campo `next_chapter` (`null → CH-13`).

Los problemas reales que sí quedan, para quien continúe este libro más allá de BH-v0.1, son
exactamente los que la seccion 18 acaba de nombrar — ninguno exige un componente nuevo de Article
III: todos son refinamientos sobre los once ya existentes, o sobre las funciones de integración que
CH-12 y este capítulo ya escribieron.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg /
> Bucles de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows),
> secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): CH-12 recorrió un `AgentRun` completo, pero solo en el
   único mundo donde nada sale mal — tres resultados reales que `PolicyEngine` y
   `ExecutionController` ya sabían producir seguían sin una sola ejecución que los recorriera.
2. **Patrones que se repiten** (= §3): un capítulo de integración que solo demuestra el resultado
   más permisivo de cada decisión deja, otra vez, dos resultados reales existiendo únicamente en
   prosa — el mismo bucle que CH-05/CH-06/CH-07 señalaron y que CH-12 heredó sin cerrarlo.
3. **Estructuras / reglas / incentivos** (= §8): cinco funciones nuevas, cada una atada a un punto
   de bifurcación exacto de `runAgentTurnEndToEnd` (CH-12), sin modificar su pseudocódigo ya
   publicado ni el de ningún componente.
4. **Modelos mentales** (= §4): cerrar un cable no significa reescribir el componente que produce
   la señal — significa escribir el código que por fin la consume hasta su destino real.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada capítulo de integración que solo demuestra el camino más
  permisivo deja los desenlaces menos permisivos como deuda que se repite capítulo tras capítulo.
- **Bucle de equilibrio (estabiliza):** cada una de las cinco funciones de este capítulo exige,
  con un `THROW` explícito, que su propia precondición se cumpla — ninguna asume el resultado que
  le conviene, cada una verifica el que realmente recibió.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es resolver los tres caminos de gobierno como
funciones nuevas y separadas, atadas a los puntos exactos donde `runAgentTurnEndToEnd` (CH-12) ya
se detenía, en vez de reabrir esa función para agregarle ramas. Si este capítulo hubiera editado
`runAgentTurnEndToEnd`, el resultado habría sido una sola función que mezcla el camino feliz con
los tres caminos de gobierno — el acoplamiento que Article IV, aplicado a la integración misma,
existe para evitar.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo
> de esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set`
> (frontmatter) y es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Cuando la autorización deniega una acción, ¿qué recibe el modelo en el turno siguiente en vez
   del resultado de una ejecución que nunca ocurrió? *(cierra la pregunta guía 1)*
2. ¿En qué momento exacto entra la ejecución a `WAITING_FOR_HUMAN`, y por qué la función que la
   lleva ahí puede simplemente terminar? *(cierra la pregunta guía 2)*
3. ¿Qué distingue, en el camino que sigue la ejecución, una resolución que aprueba la acción de una
   que la rechaza? *(cierra la pregunta guía 3)*
4. ¿Qué le faltaba a este libro para que la distinción que `ExecutionController` ya sabía hacer se
   convirtiera en el estado real de una ejecución? *(cierra la pregunta guía 4)*

### Explicar

1. `ToolRuntime.executeToolCall` nunca cambia en este capítulo, y sin embargo este capítulo
   demuestra, por primera vez, que puede simplemente no ser invocada. Explica por qué eso es
   exactamente lo que Article VI exige.
2. `HumanInteractionService.createHumanInteractionRequest` llevaba siete capítulos publicada sin
   ejecución real. Explica qué le permitió, sin cambiar una línea, quedar lista para este momento.

### Conectar

1. ¿Por qué hicieron falta tanto CH-01 como CH-06 para que este capítulo pudiera escribir el código
   que entra y sale de `WAITING_FOR_HUMAN`?
2. ¿Qué tuvo que existir primero, `runAgentTurnEndToEnd` o `terminateAgentRunOperationally`, para
   que la tabla de CH-07 §12 dejara de ser solo prosa?
3. ¿Por qué el camino `DENY` y el camino `REJECTED` terminan pareciéndose, sin que eso signifique
   que `PolicyEngine` y `HumanInteractionService` dejen de ser dos dueños distintos?
4. ¿Qué tuvo que ocurrir en este capítulo, y qué no tuvo que ocurrir en `EventBus`, para que
   `HUMAN_INTERACTION_REQUESTED` por fin llegara a `distributeEvent`?
5. ¿Quién construye el primer `AgentState` real con `status = FAILED`/`CANCELLED`/`EXPIRED`, y por
   qué eso no invade la propiedad de `AgentLoop` sobre `AgentRunStatus`?

### Espaciar

Las cinco tarjetas de repaso de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas de
nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) — ver `retrieval_set.flashcards` en
`dist/book-ir.json`.

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo.
