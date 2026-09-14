---
id: CH-11
title: "AgentCore y el Nacimiento de un AgentState"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-011]
introduces_contracts: [C-021]
modifies_contracts: []
constitutional_articles: [P-06, P-10, P-12, INV-01, INV-08, INV-09, INV-16, INV-18, INV-19, INV-20]
previous_chapter: CH-10
next_chapter: CH-12
retrieval_set:
  expected_outcome:
    id: EO-CH11
    text: |
      Al terminar este capítulo podrás distinguir, en el nacimiento de un AgentState nuevo, qué
      validación y qué transición le pertenecen en exclusiva al componente que representa la
      identidad de un agente — independiente de cualquier run o sesión particular — y qué le
      pertenece a un componente vecino ya existente (decidir continuación de turno, persistir la
      historia de una sesión, invocar al modelo seleccionado); y podrás diagnosticar, para
      cualquier AgentState recién producido, si su status refleja honestamente el punto exacto
      del lifecycle de Article V en el que una ejecución todavía no ha empezado a correr.
  skeleton:
    id: SK-CH11
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
    components_to_be_introduced: [CMP-011]
    contracts_to_be_introduced: [C-021]
  guiding_questions:
    - id: GQ-CH11-01
      text: |
        Un componente ya existente siempre recibe, como parámetro, un estado de ejecución que ya
        existe — nunca explica quién lo creó la primera vez, ni de dónde salió su identificador de
        run. ¿Quién instancia ese primer estado, antes de que exista ningún turno que decidir, y
        qué necesita validar antes de dejarlo existir?
      answered_by: RQ-CH11-01
    - id: GQ-CH11-02
      text: |
        Un componente ya existente distingue el estado operativo de una ejecución en curso de la
        historia persistida de una sesión completa — pero ninguno de los dos representa qué agente
        es, en sí mismo, independientemente de cualquier ejecución o sesión particular. ¿Qué
        representa esa tercera capa, y quién es responsable de validarla antes de que exista la
        primera ejecución?
      answered_by: RQ-CH11-02
    - id: GQ-CH11-03
      text: |
        Si un componente ya decide si otro turno de razonamiento debe ocurrir una vez que una
        ejecución está en curso, ¿por qué esa misma decisión no basta para decidir si esa ejecución
        debería, siquiera, llegar a existir — y qué se rompería si el componente que arranca una
        ejecución compitiera con el que ya gobierna su continuación?
      answered_by: RQ-CH11-03
    - id: GQ-CH11-04
      text: |
        El lifecycle formal de una ejecución define un primer estado en el que un run apenas
        existe, y un segundo en el que ya se está preparando para correr — pero, después de diez
        capítulos reales, ningún pseudocódigo del libro ha mostrado nunca esa primera transición
        ocurriendo de verdad. ¿Qué tiene que validarse antes de que esa transición ocurra, y qué
        produce exactamente del otro lado?
      answered_by: RQ-CH11-04
  systems_lens:
    iceberg_visible_fact: |
      Después de diez capítulos reales, `AgentLoop.runTurn` (CH-01 §11) siempre recibió un
      `AgentState` ya existente como parámetro — nunca explicó quién lo creó, de dónde salió su
      `runId`, ni por qué su `status` empezaba en el valor que fuera. `AgentConfig` (C-002, CH-00)
      tenía contrato desde la primera página del libro, pero ningún componente real lo validaba
      nunca antes de que una ejecución arrancara (ver seccion 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite, ahora aplicado al origen mismo de una ejecución, es que un nombre
      puede vivir en Article III desde la primera versión de la Constitution adoptada — igual que
      `SessionManager` en CH-10 — y seguir siendo, capítulo tras capítulo, solo la entrada de una
      tabla de preview mientras cada componente vecino resuelve su propio dominio (persistencia,
      invocación del modelo, autorización, ejecución de tools) dejando siempre el origen de la
      primera ejecución como un supuesto silencioso, nunca como código (ver seccion 3, Por Qué la
      Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala el undécimo y último componente de Article III, con una ficha que
      declara tanto lo que posee (`owns`: identidad del agente, validación de su configuración,
      instanciación del primer `AgentState`, la transición `CREATED → INITIALIZING`) como lo que
      explícitamente NO posee (`does_not_own`: las cuatro exclusiones literales de Article III más
      la frontera, ya resuelta, de no competir con `AgentLoop` una vez que el run está `RUNNING`) —
      y formaliza `AgentActivationRequest` (C-021), la solicitud que hace posible, por primera vez
      en el libro, mostrar con pseudocódigo real cómo nace un `AgentState` (ver seccion 8,
      Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es que Article IV formula todas sus preguntas
      ("¿debe ocurrir otro turno?", "¿puede el run continuar operacionalmente?", ...) sobre una
      ejecución que YA EXISTE — y que, antes de que exista, esas preguntas simplemente no aplican
      todavía. El componente que este capítulo introduce no le falta una fila en esa tabla porque
      no decida nada (como `EventBus`, CH-09): le falta porque su decisión ocurre en el instante
      anterior a que cualquier pregunta de Article IV tenga sentido (ver seccion 4, Impacto
      Constitucional).
    reinforcing_loop: |
      Cada vez que un componente nuevo se introduce sin declarar explícitamente su `does_not_own`,
      aumenta la probabilidad de que absorba silenciosamente la próxima decisión vecina "porque ya
      estaba ahí" — el mismo bucle que CH-01..CH-10 ya cortaron. Este capítulo enfrenta una
      variante nueva de esa tentación: al ser el componente que arranca literalmente toda
      ejecución, sería fácil que también empezara a decidir si esa ejecución debe continuar turno
      a turno "ya que de todos modos la creó".
    balancing_loop: |
      `beginAgentInitialization` (seccion 11) es el mecanismo de equilibrio: transiciona el
      `AgentState` exactamente una vez, de `CREATED` a `INITIALIZING`, y se detiene ahí — nunca
      invoca `runTurn` ni ninguna lógica de continuación de turno; el testigo pasa a `AgentLoop`
      (CH-01) sin que este capítulo le arranque una sola responsabilidad.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es dividir la activación en dos funciones
      distintas — `activateAgent` (produce `CREATED`, sin evento) y `beginAgentInitialization`
      (transiciona a `INITIALIZING`, con el primer `ExecutionContext` real del libro y el primer
      `RUN_STARTED` jamás emitido) — en vez de una sola función que hiciera las dos cosas a la vez.
      Si `AgentCore` (CMP-011) colapsara ambos pasos en uno, ningún componente futuro podría
      observar, ni auditar, el instante exacto en el que un run existe pero todavía no ha
      empezado a prepararse para correr.
  recall_questions:
    - id: RQ-CH11-01
      text: |
        ¿Qué componente instancia el primer `AgentState` de un nuevo run, y qué campos de
        `AgentConfig` (C-002) valida antes de dejarlo existir?
    - id: RQ-CH11-02
      text: |
        ¿Qué representa la identidad de un agente, independiente de cualquier run o sesión
        particular, y qué componente la valida antes de que exista la primera ejecución?
    - id: RQ-CH11-03
      text: |
        ¿Qué decide `AgentCore` que `AgentLoop` explícitamente no decide, y en qué punto exacto
        `AgentCore` deja de intervenir?
    - id: RQ-CH11-04
      text: |
        ¿Qué dos funciones de este capítulo ejercitan, por primera vez en el libro, la transición
        `CREATED → INITIALIZING` de Article V, y qué evento se emite en la segunda?
  explain_prompts:
    - id: EP-CH11-01
      text: |
        `AgentCore` posee representar la identidad de un agente y validar su `AgentConfig` antes
        de que arranque cualquier ejecución. Explica, como si hablaras con alguien sin contexto
        técnico, por qué NO posee decidir si otro turno de razonamiento debe ocurrir una vez que
        el run ya está corriendo — ¿qué se rompería si `AgentCore`, ya que de todos modos arranca
        la ejecución, empezara también a decidir su continuación turno a turno?
      target_entity: CMP-011
    - id: EP-CH11-02
      text: |
        `AgentActivationRequest.sessionId` es `Optional`. Explica por qué modelar la posibilidad
        de adjuntarse a una sesión ya existente como un campo opcional — en vez de, por ejemplo,
        exigir siempre un `sessionId` nuevo o siempre uno provisto por el llamador — es preferible,
        y qué perderíamos si este contrato no distinguiera nunca entre activar un run dentro de una
        sesión ya trackeada y empezar una sesión completamente nueva.
      target_entity: C-021
  interleaved_questions:
    - id: IQ-CH11-01
      text: |
        `AgentLoop.runTurn` (CH-01) recibe un `AgentState` ya existente y nunca pregunta quién lo
        produjo — su único guard rechaza los estados terminales (`COMPLETED`/`FAILED`/`CANCELLED`/
        `EXPIRED`). ¿Qué valor exacto de `AgentRunStatus` tiene el `AgentState` que este capítulo
        entrega a quien sea que invoque a `AgentLoop` por primera vez, y por qué ese guard, tal
        como CH-01 lo escribió, no lo rechazaría ni tampoco lo distinguiría de `RUNNING`?
      current_chapter_entities: [CMP-011, C-021]
      prior_chapter_entities: [CMP-001, C-003]
      prior_chapter: CH-01
    - id: IQ-CH11-02
      text: |
        `SessionManager` (CH-10) construye un `SessionCheckpoint` embebiendo una copia de
        cualquier `AgentState` que reciba, sin importar qué componente lo produjo. ¿Podría
        `SessionManager`, sin cambiar una sola línea de su propio código ya publicado, aceptar el
        primer `AgentState` que este capítulo produce (`status = CREATED`, antes incluso de
        `INITIALIZING`) para construir el primer checkpoint de una sesión, y qué campo de
        `SessionState` confirmaría, después del hecho, que esa sesión nació de una activación y no
        de un turno ya en curso?
      current_chapter_entities: [CMP-011, C-021]
      prior_chapter_entities: [CMP-010, C-020]
      prior_chapter: CH-10
  flashcards:
    - id: FC-CH11-01
      front: |
        ¿Qué posee `AgentCore` (Article III / Article IV), en una frase?
      back: |
        Representar la identidad de un agente independiente de cualquier run o sesión particular,
        validar su `AgentConfig` antes de que arranque cualquier ejecución, e instanciar el
        `AgentState` inicial de un nuevo run — asignando `runId`, decidiendo `sessionId` y
        transicionando `CREATED → INITIALIZING` (Article V) — sin competir nunca con `AgentLoop`
        una vez que el run ya está `RUNNING`.
      source_entity: CMP-011
      chapter_introduced_in: CH-11
      review_stage: DAY_1
    - id: FC-CH11-02
      front: |
        ¿Qué NO posee `AgentCore`, y a qué componentes pertenecen esas decisiones?
      back: |
        UI (`INV-16`, cita literal), persistencia específica de sesión (`SessionManager`,
        CMP-010, ya introducido en CH-10), proveedores de modelo (`ModelGateway`, CMP-003, ya
        introducido en CH-03 — `INV-01`, cita literal), business integrations (sin componente
        propio, fuera de alcance) y decidir continuación de turno una vez `RUNNING` (`AgentLoop`,
        CMP-001, ya introducido en CH-01) — `AgentCore` entrega el testigo a `AgentLoop` después
        de `INITIALIZING`, nunca compite con él.
      source_entity: CMP-011
      chapter_introduced_in: CH-11
      review_stage: DAY_1
    - id: FC-CH11-03
      front: |
        ¿Qué campos tiene `AgentActivationRequest` (C-021), y qué representan?
      back: |
        `agentId` (`AgentId`, qué agente configurado se activa), `sessionId`
        (`Optional<SessionId>`, `NULL` si es una sesión nueva, poblado si se adjunta a una ya
        trackeada por `SessionManager`), `input` (`Value`, el objetivo/input inicial que el agente
        debe procesar) y `requestedAt` (`Timestamp`, cuándo se solicitó la activación).
      source_entity: C-021
      chapter_introduced_in: CH-11
      review_stage: DAY_1
    - id: FC-CH11-04
      front: |
        ¿Por qué este capítulo es el primero en emitir `AgentEventType.RUN_STARTED`?
      back: |
        Porque `RUN_STARTED` fue declarado desde CH-00 y CH-01 §14 señaló explícitamente que
        pertenecía "al arranque de un `AgentRun`, todavía sin componente propio que lo orqueste" —
        `beginAgentInitialization` (seccion 11) es la primera función real del libro que produce
        ese arranque, diez capítulos después de que el valor quedara reservado sin dueño.
      source_entity: C-021
      chapter_introduced_in: CH-11
      review_stage: DAY_1
    - id: FC-CH11-05
      front: |
        ¿Por qué `AgentCore`, como `EventBus` (CH-09), tampoco tiene fila propia en la tabla de
        Decision Ownership de Article IV — y por qué es una razón distinta?
      back: |
        `EventBus` no tiene fila porque no decide nada, solo distribuye. `AgentCore` no tiene fila
        porque su "decisión" — validar y activar un agente — ocurre ANTES de que exista ningún
        `AgentRun` sobre el cual las preguntas de Article IV (todas formuladas sobre una ejecución
        ya en curso) puedan siquiera aplicarse.
      source_entity: CMP-011
      chapter_introduced_in: CH-11
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH11-01
      recall_question: RQ-CH11-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH11-02
      recall_question: RQ-CH11-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH11-03
      recall_question: RQ-CH11-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH11-04
      recall_question: RQ-CH11-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 11 — AgentCore y el Nacimiento de un AgentState

> **Regla constitucional (Article III, sección "AgentCore"):** responsable de representar y
> coordinar las primitives fundamentales del agente. No debe absorber responsabilidades de UI,
> persistencia específica, proveedores o business integrations.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de saber
> cómo se llama el componente de este capítulo. El detalle estructurado de esta sección vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, en el nacimiento de un
`AgentState` nuevo, qué validación y qué transición le pertenecen en exclusiva al componente que
representa la identidad de un agente — independiente de cualquier run o sesión particular — y qué
le pertenece a un componente vecino ya existente (decidir continuación de turno, persistir la
historia de una sesión, invocar al modelo seleccionado); y podrás diagnosticar, para cualquier
`AgentState` recién producido, si su `status` refleja honestamente el punto exacto del lifecycle de
Article V en el que una ejecución todavía no ha empezado a correr.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e
introduce un contrato de datos nuevo y el undécimo y último componente de runtime de Article III —
todavía sin explicarlos, solo como mapa.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar
atrás; están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este
capítulo va a definir):

1. Un componente ya existente siempre recibe, como parámetro, un estado de ejecución que ya existe
   — nunca explica quién lo creó la primera vez, ni de dónde salió su identificador de run. ¿Quién
   instancia ese primer estado, antes de que exista ningún turno que decidir, y qué necesita
   validar antes de dejarlo existir?
2. Un componente ya existente distingue el estado operativo de una ejecución en curso de la
   historia persistida de una sesión completa — pero ninguno de los dos representa qué agente es,
   en sí mismo, independientemente de cualquier ejecución o sesión particular. ¿Qué representa esa
   tercera capa, y quién es responsable de validarla antes de que exista la primera ejecución?
3. Si un componente ya decide si otro turno de razonamiento debe ocurrir una vez que una ejecución
   está en curso, ¿por qué esa misma decisión no basta para decidir si esa ejecución debería,
   siquiera, llegar a existir — y qué se rompería si el componente que arranca una ejecución
   compitiera con el que ya gobierna su continuación?
4. El lifecycle formal de una ejecución define un primer estado en el que un run apenas existe, y
   un segundo en el que ya se está preparando para correr — pero, después de diez capítulos reales,
   ningún pseudocódigo del libro ha mostrado nunca esa primera transición ocurriendo de verdad.
   ¿Qué tiene que validarse antes de que esa transición ocurra, y qué produce exactamente del otro
   lado?

## 1. Arquitectura Actual (Current Architecture)

CH-00..CH-10 dejaron instalados veinte contratos de datos y diez componentes de runtime. De los
once nombres que Article III enumera en su árbol de "Agent Runtime" (`AgentCore`, `AgentLoop`,
`ModelGateway`, `ContextEngine`, `ToolRuntime`, `PolicyEngine`, `SessionManager`,
`HumanInteractionService`, `EventBus`, `ExecutionController`, `CapabilityRegistry`), CH-10 dejó
exactamente uno todavía en preview: `AgentCore`.

Esa deuda no es reciente ni sutil. `AgentCore` aparece nombrado, literalmente, en tres invariantes
de Article II desde la primera versión de la Constitution adoptada por este repositorio —
`INV-01` ("`AgentCore` no depende directamente de APIs específicas de OpenAI, Anthropic, Google u
otro proveedor"), `INV-16` ("`AgentCore` puede ejecutarse sin UI") — y CH-03 (`ModelGateway`) ya
tuvo que interpretar `INV-01` de forma indirecta, porque en ese punto del libro `AgentCore` no
existía todavía como componente real: "Primera cita literal posible de este invariante: ya existe
un `ModelGateway` real cuya ficha (...) es el único lugar del libro donde un adapter de proveedor
concreto podría vivir" (CH-03 §4). Ese rodeo — citar el invariante sin que su sujeto gramatical
existiera — es, precisamente, la deuda que este capítulo cierra: por primera vez, `AgentCore` deja
de ser solo el nombre que dos invariantes mencionan, y pasa a ser el componente real que esos
invariantes describen.

Hay, además, una segunda deuda — más silenciosa, porque ningún capítulo la nombró nunca
explícitamente como pendiente. `AgentLoop.runTurn` (CH-01 §11) declara su primer parámetro así:

```pseudocode
FUNCTION runTurn(
    state: AgentState,
    execution: ExecutionContext,
    modelFinished: Boolean,
    modelProposesToolCall: Boolean
) -> AgentState
```

`state: AgentState` — un `AgentState` que **ya existe**. Diez capítulos completos (CH-01..CH-10)
construyeron un runtime entero — turnos, tools, invocación de modelo, contexto, policy, aprobación
humana, presupuesto, capabilities, eventos, sesiones — y ninguno de ellos mostró jamás cómo nace la
primera instancia de ese `AgentState`, quién le asigna su `runId`, ni por qué su `status` empieza
en el valor que sea. `AgentConfig` (C-002, CH-00) — `agentId`, `name`, `budget` — tiene contrato
desde la primera página del libro, con `used_by: [CMP-001]` (solo `AgentLoop` lo consume, y solo
para leer su `budget` de forma indirecta a través de `ExecutionContext`); pero ningún componente
real lo **valida**: nada en el libro, hasta este capítulo, comprueba que un `AgentConfig` referido
por su `agentId` exista de verdad, ni que su `ExecutionBudget` (C-012) sea coherente, antes de que
una ejecución arranque.

`AgentRunStatus` (C-013, CH-01) ya declara `CREATED` e `INITIALIZING` como sus dos primeros
valores, fieles al diagrama de Article V — pero CH-01 §12 documentó la transición
`CREATED → INITIALIZING` solo en prosa, sin ningún pseudocódigo que la ejercitara: "`INITIALIZING`
→ `RUNNING` / `FAILED`" aparece en esa tabla como una fila más, nunca como código real. Y
`AgentEventType.RUN_STARTED` (declarado desde CH-00 §6) sigue, después de diez capítulos, sin que
ningún componente lo haya emitido jamás — CH-01 §14 lo señaló explícitamente: "`RUN_STARTED`
pertenece al arranque de un `AgentRun` (todavía sin componente propio que lo orqueste)".

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas para esto, la pregunta "¿quién decide que este agente,
con esta configuración, puede empezar a existir como una ejecución concreta?" no tiene ningún
lugar fijo donde vivir. Una implementación puede saltarse la pregunta por completo y construir un
`AgentState` a mano, en cualquier punto del código que necesite uno, sin validar nunca que el
`AgentConfig` referenciado exista o que su presupuesto sea coherente; otra puede confundir esa
validación con la que `AgentLoop` ya hace turno a turno, dejando que el mismo componente que decide
"¿debe ocurrir otro turno?" decida también "¿debería esta ejecución, siquiera, haber llegado a
existir?" — dos preguntas de dominios distintos, resueltas por el mismo lugar solo porque ambas
tocan un `AgentState`.

Hay una segunda dimensión del mismo problema, más conceptual que operativa. `SessionManager`
(CH-10) ya distingue con precisión el estado operativo de una ejecución en curso (`AgentState`) de
la historia persistida de una sesión completa (`SessionState`) — pero ninguno de los dos
contratos representa qué **es** un agente, en sí mismo, independientemente de cualquier ejecución
o sesión particular. `AgentConfig` (C-002) se acerca — es la configuración declarativa de un
agente sobre el runtime compartido (`P-06`) — pero un `STRUCT` sin comportamiento no es, todavía,
una identidad que alguien valide, coordine o active: es un dato que cualquiera podría leer, y que
nadie, hasta este capítulo, tiene la responsabilidad exclusiva de custodiar antes de que una
ejecución empiece.

Necesitamos que "¿puede este agente, con esta configuración, activarse como un nuevo run — y qué
`AgentState` inicial resulta de esa activación?" tenga, por fin, un dueño único y nombrado — que
valide el `AgentConfig` referenciado, que asigne un `runId` nuevo, que decida si el run se adjunta
a una sesión ya trackeada o empieza una nueva, que produzca el primer `AgentState` con el status
correcto de Article V, y que se detenga ahí — sin decidir nada de lo que ya pertenece a
`AgentLoop`, `ModelGateway` o `SessionManager`.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los veinte contratos y los diez componentes que existen hasta este punto no bastan porque:

- Article III nombra `AgentCore` en su árbol de "Agent Runtime" desde la primera versión de la
  constitución adoptada, con una responsabilidad explícita ("representar y coordinar las
  primitives fundamentales del agente") que ningún capítulo había materializado con código real;
- `INV-01` e `INV-16` citan literalmente el nombre `AgentCore` desde CH-00, y CH-03 tuvo que
  interpretarlos de forma indirecta (a través de `ModelGateway`) precisamente porque su sujeto
  gramatical no existía todavía como componente — la misma clase de vacío que `AgentRunStatus`
  (CH-01) y `SessionState` (CH-10) ya cerraron, cada uno para un contrato de datos; este capítulo
  lo cierra, por primera vez, para el sujeto de un invariante;
- `AgentLoop.runTurn` (CH-01 §11) recibe `state: AgentState` como su primer parámetro sin que
  ningún componente del libro haya mostrado jamás cómo se produjo esa primera instancia — el
  runtime entero descrito en CH-01..CH-10 asume, silenciosamente, que un `AgentState` ya existe
  antes de que cualquiera de esos diez capítulos empiece a actuar sobre él;
- `AgentConfig` (C-002, CH-00) sigue sin que ningún componente lo valide: nada comprueba que el
  `agentId` referenciado corresponda a una configuración real, ni que su `ExecutionBudget` (C-012)
  sea coherente, antes de que una ejecución arranque;
- `AgentEventType.RUN_STARTED` (CH-00) sigue siendo un valor declarado sin que ningún componente
  real lo haya emitido jamás — CH-01 §14 documentó explícitamente que pertenecía "al arranque de
  un `AgentRun`, todavía sin componente propio que lo orqueste";
- la transición `CREATED → INITIALIZING` del diagrama de Article V (documentada en prosa desde
  CH-01 §12) sigue sin ningún pseudocódigo real que la ejercite — a diferencia de
  `WAITING_FOR_HUMAN → EXPIRED` (CH-01), `INITIALIZING → RUNNING` (documentada, nunca ejercitada
  con código) o cualquiera de las transiciones que `AgentLoop`/`ExecutionController` sí cubren con
  funciones reales.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la
> secuencia `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una
> entidad que no haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT`
> registrado — **no magic entities**. Este capítulo aplica la misma disciplina de *ownership* que
> CH-01..CH-10 ya establecieron, con una particularidad nueva: por primera vez, un componente nace
> siendo el **origen** de identificadores que los diez capítulos anteriores siempre recibieron ya
> dados (`RunId`, `TraceId`, y opcionalmente `SessionId`) — y debe demostrar, con código real, que
> minarlos no equivale a decidir nada de lo que sucede después de que existen.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-06   Agents are configuration over a shared runtime.
           activateAgent (seccion 11) es la primera vez que un componente real valida un
           AgentConfig antes de que una ejecución exista — la configuración declarativa deja de
           ser un STRUCT que cualquiera podría leer sin verificación y pasa a tener un guardián.
    P-10   The harness owns execution state—not the model.
           El primer AgentState y el primer ExecutionContext de todo el libro nacen de una
           validación puramente determinística (¿existe el AgentConfig? ¿es coherente su
           budget?) — el modelo no interviene en absoluto en esta decisión, ni siquiera de forma
           indirecta.
    P-12   Events observe; hooks intervene.
           beginAgentInitialization (seccion 11) emite RUN_STARTED — declarado desde CH-00,
           jamás emitido hasta este capítulo.

Invariants preserved
    INV-01   AgentCore no depende directamente de APIs específicas de OpenAI, Anthropic, Google
             u otro proveedor.
             Primera cita LITERAL de este invariante en sentido estricto: hasta este capítulo,
             solo pudo citarse de forma indirecta a través de ModelGateway (CH-03 §4, "primera
             cita literal posible"). Ahora AgentCore existe, y su ficha (does_not_own:
             "proveedores") confirma en código lo que el invariante exigía en prosa desde CH-00.
    INV-08   El harness es propietario del execution state.
             activateAgent / beginAgentInitialization (seccion 11) producen el AgentState y el
             ExecutionContext iniciales de un run completamente nuevos — ninguno de los dos existe
             antes de que este capítulo los construya.
    INV-09   Todo AgentRun tiene límites explícitos.
             activateAgent rechaza cualquier AgentConfig cuyo ExecutionBudget (C-012) no sea
             coherente, antes de que exista ningún AgentState — un run nunca llega a nacer con
             límites incoherentes, ni siquiera antes de que ExecutionController (CH-07) empiece a
             gobernarlo turno a turno.
    INV-16   AgentCore puede ejecutarse sin UI.
             Mismo caso que INV-01: primera cita literal en sentido estricto. Ni activateAgent ni
             beginAgentInitialization dependen de ningún adapter de presentación.
    INV-18   Toda acción significativa produce un evento observable.
             beginAgentInitialization emite AgentEvent (RUN_STARTED) en su único camino exitoso.
    INV-19   Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy
             relevante.
             beginAgentInitialization construye el primer TraceId real de la ejecución y lo
             incluye en el AgentEvent que emite — ningún capítulo anterior había construido un
             TraceId nuevo; todos lo recibían ya dado dentro de un ExecutionContext existente.
    INV-20   Todo error operacional pertenece a una categoría conocida.
             Los tres fallos de este capítulo (seccion 13) se clasifican bajo VALIDATION, con
             recoverable/retryable explícitos — nunca una excepción cruda.

Component ownership changes
    CMP-011 AgentCore se introduce — registry/components.yaml pasa de 10 a 11 componentes. De los
    once nombres de Article III, ninguno sigue en preview después de este capítulo. owns/
    does_not_own citados literalmente contra Article III (sección "AgentCore") y Article IV.
    registry/components.yaml de CMP-001 (AgentLoop), CMP-003 (ModelGateway) y CMP-010
    (SessionManager) NO se modifica: ninguno cablea todavía su relación real con AgentCore (ver
    seccion 9/18).

Lifecycle changes
    Ninguna modificación a AgentRunStatus (C-013): sigue siendo, sin cambios, el mismo ENUM de
    once estados que CH-01 formalizó. Este capítulo es, en cambio, el primero en EJERCITAR con
    pseudocódigo real la transición CREATED → INITIALIZING que ese mismo ENUM ya declaraba desde
    CH-01 solo en prosa (CH-01 §12).

Security implications
    AgentCore nunca decide autorización (P-13 sigue siendo exclusivo de PolicyEngine, CH-05) ni
    invoca al modelo (ModelGateway, CH-03) para decidir si un agente puede activarse. Ver seccion
    15 para el análisis completo, incluyendo la distinción explícita frente al ActivationRequest
    de Amendment v1.1 (P-16/P-17), deliberadamente fuera de alcance de BH-v0.1.

Observability implications
    AgentCore es el undécimo componente que emite AgentEvent en la práctica — pero, a diferencia
    de cada uno de los diez anteriores, no agrega ningún valor nuevo a AgentEventType: reutiliza
    RUN_STARTED, declarado desde CH-00 y nunca antes emitido por ningún componente real.

Deterministic vs agentic boundary
    Article XII se refina una undécima vez a nivel de componente: AgentCore, igual que EventBus
    (CH-09), no consume ninguna salida del modelo ni directa ni indirectamente — a diferencia de
    EventBus, cuya frontera determinística separa un evento ya producido de sus consumidores, la
    de AgentCore separa una solicitud de activación (con un agentId y un input, nunca una
    invocación al modelo) del primer estado operativo determinístico que resulta de validarla.
```

## 5. Conceptos Nuevos (New Concepts)

- **Agent Identity**: lo que un agente **es**, independientemente de cualquier run o sesión
  particular — la referencia estable (`AgentId`) y la configuración declarativa (`AgentConfig`,
  C-002, CH-00) que describen ese agente antes de que exista ninguna ejecución concreta sobre él.
  Distinta de `AgentState` (el presente operativo de UNA ejecución, CH-00/CH-01) y de
  `SessionState` (la historia persistida de UNA sesión a través del tiempo, CH-10) — una tercera
  capa, conceptualmente anterior a las otras dos, que ningún contrato había representado con un
  componente que la validara hasta este capítulo.
- **Agent Activation**: el acto de admitir que un agente configurado (`AgentConfig` ya existente y
  válido) empiece a existir como una ejecución concreta — produciendo el primer `AgentState` de un
  nuevo `runId`, con `status = CREATED`. Nunca decide si esa ejecución debe continuar después de
  arrancar; eso pertenece, desde CH-01, a `AgentLoop`.
- **Agent Initialization**: la transición formal `CREATED → INITIALIZING` del diagrama de Article
  V — el instante en el que un run, ya activado, empieza a prepararse para correr (construyendo su
  primer `ExecutionContext` real) sin que todavía se haya invocado ningún turno de razonamiento.
  Documentada en prosa desde CH-01 §12; ejercitada con pseudocódigo real por primera vez en este
  capítulo.
- **Decision Ownership** *(Article IV, en uso desde CH-01, ahora aplicado a un undécimo
  componente — el último de Article III)*: `AgentCore` decide "¿puede este agente activarse, y
  cuál es su primer `AgentState`?"; explícitamente NO decide "¿debe ocurrir otro turno de
  razonamiento?" (`AgentLoop`, ya resuelto), "¿qué historia de sesión persiste?" (`SessionManager`,
  ya resuelto) ni "¿cómo se invoca al modelo seleccionado?" (`ModelGateway`, ya resuelto).
- **Ingress Activation (Amendment v1.1, P-16/P-17 — concepto distinto, no introducido en este
  capítulo)**: la normalización de un estímulo **externo** (un prompt, un webhook, una cola, un
  evento de otro sistema) hacia un `ActivationRequest` de Enterprise, evaluado por un
  `AdmissionController` (identidad, autorización, tenant, capacidad, rate, presupuesto,
  deduplicación, policy) antes de que exista siquiera un `agentId` resuelto — Ingress & Activation
  Plane, fuera de alcance de BH-v0.1. Deliberadamente distinto de la Agent Activation de este
  capítulo, que parte de un `agentId` ya conocido y ya configurado (ver seccion 7 y seccion 15 para
  la distinción completa).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados de CH-00/CH-01

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `AgentId`, `SessionId`, `RunId`, `TraceId`,
`Timestamp`, `Value`, `AgentConfig`, `AgentState`, `ExecutionContext`, `ExecutionBudget`,
`AgentEvent`, `HarnessError`.

### `AgentActivationRequest` — la solicitud de activar un run

```pseudocode
STRUCT AgentActivationRequest
    agentId: AgentId
    sessionId: Optional<SessionId>
    input: Value
    requestedAt: Timestamp
END
```

Cuatro campos, cada uno respondiendo a una parte exacta del alcance decidido para este capítulo:
`agentId` referencia el `AgentConfig` (C-002) que describe el agente que se quiere activar;
`sessionId` es `Optional<SessionId>` — `NULL` cuando la activación debe empezar una sesión
completamente nueva, poblado con el id de una sesión ya trackeada por `SessionManager` (CH-10)
cuando el nuevo run debe adjuntarse a una historia existente; `input` es el objetivo o entrada
inicial que el agente debe procesar (tipado como `Value`, el mismo primitivo genérico que
`AgentMessage.content`, C-001, CH-00, ya usa — este capítulo no le exige una forma más estricta,
porque interpretar ese input es trabajo de `ContextEngine`/`ModelGateway`, ya resueltos, no de
`AgentCore`); `requestedAt` registra cuándo se solicitó la activación.

**Por qué el nombre es `AgentActivationRequest`, y no `ActivationRequest` a secas.** Se evaluó
explícitamente reutilizar el nombre `ActivationRequest` — el término que Amendment v1.1 ya usa
literalmente en `P-16` ("External stimuli MUST be normalized into an `ActivationRequest` before
entering the execution core") — y se descartó con cuidado. `ActivationRequest` (Amendment v1.1) es
la normalización de un estímulo **externo y crudo** (un prompt, un webhook, un evento) antes de que
exista siquiera un `agentId` resuelto, evaluada por un `AdmissionController` (identidad,
autorización, tenant, capacidad, rate, presupuesto, deduplicación, policy — Ingress & Activation
Plane, Enterprise, fuera de alcance de BH-v0.1). `AgentActivationRequest` (este capítulo) es algo
mucho más acotado: la solicitud de activar un run de un agente **que ya tiene un `agentId`
conocido y un `AgentConfig` ya registrado** — el tramo que ocurre, en el mejor de los casos,
**después** de que un `AdmissionController` (si existiera) ya admitió el estímulo, o, en el
alcance actual de BH-v0.1 (sin ese plano Enterprise todavía construido), directamente como la
única solicitud de activación que el libro modela. Reutilizar el nombre corto habría sugerido que
este capítulo implementa `P-16`/`P-17` — no es así, y decirlo con un nombre distinto evita que un
lector futuro confunda ambos conceptos (ver seccion 15 para la distinción completa).

**Unchanged / Not yet introduced**: `AgentConfig` (C-002) y `ExecutionBudget` (C-012) no cambian de
forma — este capítulo los consume, nunca los modifica. Ningún `ENUM AgentActivationStatus` propio:
a diferencia de `HumanInteractionRequest` (CH-06) o `EventSubscription` (CH-09), una solicitud de
activación no persiste como una entidad con lifecycle propio — se procesa una única vez, de forma
síncrona, y su resultado es directamente un `AgentState` (ver seccion 12).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce un contrato de
datos, registrado en `registry/contracts.yaml`:

```text
ID:                     C-021
Name:                   AgentActivationRequest
Version:                v1
Introduced In:          CH-11
Current Definition:     STRUCT AgentActivationRequest (ver §6)
Used By:                [CMP-011]
Modified By:            []
Constitutional Impact:  [P-06, P-10, INV-08, INV-09]
```

`C-021` es el octavo id verdaderamente nuevo del libro (el correlativo continúa después de `C-020`,
CH-10 — ningún id quedaba reservado desde CH-01 §7). A diferencia de `SessionState` (C-020,
CH-10) o `AgentRunStatus` (C-013, CH-01) — dos contratos cuyo nombre exacto la Constitution ya
citaba antes de que el capítulo que los formalizó los escribiera — `AgentActivationRequest` es un
nombre acuñado por este capítulo: la Constitution solo cita, literalmente, `ActivationRequest`
(Amendment v1.1, `P-16`) — un concepto deliberadamente distinto (ver seccion 6 y seccion 15).

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el undécimo y último componente de runtime de Article III:

```pseudocode
COMPONENT AgentCore
    consumes: AgentConfig, AgentActivationRequest, ExecutionBudget
    produces: AgentState, ExecutionContext, AgentEvent, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Article III (sección "AgentCore"):

```text
COMPONENT: AgentCore

Responsibility:
    Representar la identidad de un agente — independiente de cualquier run o sesión particular —,
    validar su AgentConfig antes de que arranque cualquier ejecución, e instanciar el AgentState
    inicial de un nuevo run: asignar su runId, decidir su sessionId y producir la primera
    transición formal de Article V (CREATED → INITIALIZING) — sin decidir nada de lo que ocurre
    una vez que ese run ya está RUNNING.

Consumes:
    C-002 AgentConfig, C-021 AgentActivationRequest, C-012 ExecutionBudget

Depends on:
    (ninguno todavía — el cableado real hacia AgentLoop, ModelGateway y SessionManager es Preview,
    no introducido en este capítulo; ver seccion 9)

Produces:
    C-003 AgentState (el primero de un nuevo run), C-004 ExecutionContext (el primero construido
    por código real en todo el libro), C-010 AgentEvent (RUN_STARTED), C-011 HarnessError

Owns (Article III, cita literal, mas la lectura concreta de este capítulo):
    - "representar y coordinar las primitives fundamentales del agente" (cita literal)
    - representar la identidad/definición del agente, independiente de cualquier run o sesión
      particular — el "qué es este agente", no "qué está haciendo ahora mismo"
    - validar un AgentConfig antes de que arranque cualquier ejecución
    - instanciar el AgentState inicial de un nuevo run: asignar runId, decidir sessionId
    - la transición CREATED → INITIALIZING (Article V) — la primera de todo el lifecycle

Does NOT own (Article III, cita literal, las cuatro exclusiones — mas las fronteras ya
establecidas por otros componentes):
    - "UI" (cita literal — ninguna función de este capítulo depende de ningún adapter de
      presentación; INV-16)
    - "persistencia específica" (cita literal — SessionManager, CMP-010, ya introducido en CH-10,
      posee la persistencia durable de la historia de una sesión; AgentCore nunca invoca
      createOrUpdateSessionCheckpoint ni ningún mecanismo de SessionManager)
    - "proveedores" (cita literal — ModelGateway, CMP-003, ya introducido en CH-03, posee la
      selección e invocación de provider; INV-01)
    - "business integrations" (cita literal — sin componente propio todavía en este registry;
      fuera de alcance genérico de BH-v0.1, igual que en la Constitution)
    - decidir si otro turno de razonamiento debe ocurrir una vez que el run ya está RUNNING
      (AgentLoop, CMP-001, ya introducido en CH-01 — AgentCore entrega el testigo a AgentLoop
      inmediatamente después de INITIALIZING; ninguna de las dos funciones de este capítulo
      invoca runTurn ni ninguna lógica de continuación de turno)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con una
particularidad respecto a CH-01..CH-10: por primera vez, las cuatro exclusiones literales de
Article III (UI, persistencia específica, proveedores, business integrations) coinciden,
palabra por palabra, con la ficha original de la Constitution — ningún otro componente del libro
tuvo, en su artículo fundacional, exactamente cuatro exclusiones ya nombradas de antemano.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
AgentCore
    consumes → AgentConfig, AgentActivationRequest, ExecutionBudget
    produces → AgentState, ExecutionContext, AgentEvent, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`AgentCore` no depende hoy de ningún otro componente registrado — mismo patrón que CH-01..CH-10 ya
establecieron para sus propios componentes. En prosa (nunca dentro de un bloque `pseudocode`, per
`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las relaciones futuras que un
capítulo de integración agregaría son:

| Componente futuro (relación inversa — no cableada en este capítulo) | Qué relación tendría con `AgentCore` |
|---|---|
| `AgentLoop` (ya existente, CMP-001) | tomaría el `AgentState` en `status = INITIALIZING` que `AgentCore` produjo, sería responsable (en un capítulo de integración futuro) de completar la transición `INITIALIZING → RUNNING`, y solo entonces invocaría `runTurn` por primera vez sobre ese run — `AgentLoop` no cambia una sola línea de su código ya publicado (CH-01) para que este capítulo sea correcto |
| `SessionManager` (ya existente, CMP-010) | podría, en un capítulo de integración futuro, invocar `createOrUpdateSessionCheckpoint` con el primer `AgentState` que `AgentCore` produce, exactamente igual que lo haría con cualquier `AgentState` producido después de un turno — `SessionManager` no necesita distinguir "quién" produjo el `AgentState` que recibe |
| `ModelGateway` (ya existente, CMP-003) | seguiría siendo el único componente que invoca al modelo — `AgentCore` nunca lo hace directamente, ni siquiera para decidir si un agente puede activarse |

`registry/components.yaml` de `CMP-001` (`AgentLoop`), `CMP-003` (`ModelGateway`) y `CMP-010`
(`SessionManager`) **no se modifica** en este capítulo: ninguno agrega `CMP-011` a sus
`dependencies`, y ninguno cambia su pseudocódigo. El pseudocódigo de la seccion 11 construye,
válida y transiciona un `AgentActivationRequest`/`AgentState`/`ExecutionContext` de forma
completamente autónoma — sin que ninguno de los tres componentes ya existentes cambie una sola
línea para que este capítulo sea correcto. Ese cableado real es, explícitamente, trabajo de un
capítulo de integración futuro (ver seccion 18/19).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[Llamador — todavía sin componente propio, Preview] → AgentCore →
[AgentLoop — Preview de esta interacción, retoma después de INITIALIZING]
```

**Vista 2 — Sequence**

```text
AgentActivationRequest
   │ (agentId, sessionId opcional, input, requestedAt)
   ▼
AgentCore
   │ activateAgent(request)
   │ ¿existe un AgentConfig para agentId? no → HarnessError (AGENT_CONFIG_NOT_FOUND, VALIDATION)
   │ ¿su ExecutionBudget es coherente? no → HarnessError (INCOHERENT_EXECUTION_BUDGET, VALIDATION)
   │ decide sessionId (el provisto, o uno nuevo) y genera un runId nuevo
   │ construye: AgentState (status = CREATED, currentTurn = 0)
   ▼
AgentState (CREATED) — un run existe; nada ha empezado a prepararse todavía
   │
   │ ... el mismo AgentCore, o un llamador con la misma referencia, decide iniciar ...
   ▼
AgentCore
   │ beginAgentInitialization(state, config)
   │ ¿state.status != CREATED? sí → HarnessError (INITIALIZATION_REQUIRES_CREATED_STATE, VALIDATION)
   │ construye el primer ExecutionContext real de este run (traceId nuevo)
   │ transiciona: CREATED → INITIALIZING
   │ emite: AgentEvent (RUN_STARTED) — primera vez que este libro lo emite
   ▼
AgentState (INITIALIZING) — el testigo pasa a AgentLoop (CH-01, Preview de esta interacción; su
    código no cambia)
```

**Vista 3 — Pseudocódigo**

Ver §11: `activateAgent` y `beginAgentInitialization` son la primera formalización ejecutable de
"`AgentCore` valida un agente y produce el primer `AgentState` de un nuevo run" — construidas
exclusivamente a partir de material que ya existe (`AgentConfig`, `ExecutionBudget` desde CH-00,
`AgentState`, `ExecutionContext` desde CH-00) más el contrato nuevo de este capítulo.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde CH-00/CH-01.

```pseudocode
FUNCTION activateAgent(request: AgentActivationRequest) -> AgentState

    config: Optional<AgentConfig> = findAgentConfig(request.agentId)

    IF config == NULL
        notFound: HarnessError = HarnessError(
            category = VALIDATION,
            code = "AGENT_CONFIG_NOT_FOUND",
            message = "activateAgent no encontró ningún AgentConfig registrado para el agentId recibido",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW notFound
    END

    IF NOT isExecutionBudgetCoherent(config.budget)
        incoherent: HarnessError = HarnessError(
            category = VALIDATION,
            code = "INCOHERENT_EXECUTION_BUDGET",
            message = "activateAgent recibió un AgentConfig cuyo ExecutionBudget declara al menos un límite no positivo",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW incoherent
    END

    resolvedSessionId: SessionId = request.sessionId

    IF resolvedSessionId == NULL
        resolvedSessionId = newSessionId()
    END

    initialState: AgentState = AgentState(
        runId = newRunId(),
        sessionId = resolvedSessionId,
        agentId = request.agentId,
        status = CREATED,
        currentTurn = 0
    )

    RETURN initialState
END
```

```pseudocode
FUNCTION beginAgentInitialization(
    state: AgentState,
    config: AgentConfig
) -> AgentState

    IF state.status != CREATED
        wrongStatus: HarnessError = HarnessError(
            category = VALIDATION,
            code = "INITIALIZATION_REQUIRES_CREATED_STATE",
            message = "beginAgentInitialization fue invocada sobre un AgentState cuyo status no es CREATED",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW wrongStatus
    END

    execution: ExecutionContext = ExecutionContext(
        runId = state.runId,
        sessionId = state.sessionId,
        traceId = newTraceId(),
        budget = config.budget
    )

    nextState: AgentState = AgentState(
        runId = state.runId,
        sessionId = state.sessionId,
        agentId = state.agentId,
        status = INITIALIZING,
        currentTurn = state.currentTurn
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = RUN_STARTED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = state.agentId,
        traceId = execution.traceId,
        payload = nextState
    )

    RETURN nextState
END
```

`newEventId()` y `now()` son las mismas primitivas de CH-00..CH-10. `findAgentConfig(agentId) ->
Optional<AgentConfig>` es una primitiva asumida — el mecanismo real de registro/almacenamiento de
`AgentConfig` que hay detrás no se modela en este capítulo, el mismo tipo de restricción de alcance
que ya aplicó `persistSessionState` (CH-10) para su propio almacén. `isExecutionBudgetCoherent(
budget: ExecutionBudget) -> Boolean` verifica que cada límite de `ExecutionBudget` (`maxTurns`,
`maxToolCalls`, `maxInputTokens`, `maxOutputTokens`, `maxCost`, `maxRuntimeMs`,
`maxConcurrentTools`) sea estrictamente mayor que cero — sin implementar ninguna política más
sofisticada de coherencia entre límites (ver seccion 18).

`newRunId()`, `newSessionId()` y `newTraceId()` son primitivas de generación de identificador, en
el mismo espíritu que `newEventId()` (CH-00) o `newSessionCheckpointId()` (CH-10) — pero con una
diferencia real: son la **primera vez en el libro** que `RunId`, `SessionId` y `TraceId` se minan
desde cero. Los diez capítulos anteriores siempre recibieron los tres ya dados, empaquetados dentro
de un `AgentState`/`ExecutionContext` que ya existía como parámetro de entrada — ninguno tuvo,
hasta ahora, la responsabilidad de originarlos.

Nótese lo que ninguna de las dos funciones hace: ninguna invoca `runTurn` (`AgentLoop`, CH-01) ni
ninguna otra lógica de continuación de turno; ninguna invoca al modelo (`ModelGateway`, CH-03);
ninguna persiste nada en `SessionManager` (CH-10); y `activateAgent` no emite ningún evento — el
único camino de este capítulo que emite algo es `beginAgentInitialization`, exactamente en el
instante en que la transición formal de Article V ocurre.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013): sigue siendo, sin cambios, el
mismo `ENUM` de once estados que `AgentLoop` (CH-01 §6/§12) formalizó. Lo que este capítulo agrega
es la primera formalización ejecutable de su primera transición:

```text
(activateAgent, AgentConfig válido, ExecutionBudget coherente)
   → AgentState con status = CREATED, currentTurn = 0
     (el run existe; nada ha empezado a prepararse todavía)

(beginAgentInitialization, state.status == CREATED)
   → AgentState con status = INITIALIZING
     (primer ExecutionContext real de este run; primer RUN_STARTED emitido)

INITIALIZING
   → RUNNING   (Preview — AgentLoop, CH-01 §12, ya documentado en prosa; no ejercitado con
                pseudocódigo real en ningún capítulo todavía, incluido este)
   → FAILED    (Preview — mismo caso)
```

**Lo que este capítulo ejercita, y lo que deliberadamente deja para después.** `CREATED →
INITIALIZING` (§11) es, por fin, la primera transición del diagrama de Article V que un
pseudocódigo real de este libro produce — CH-01 §12 solo la había documentado como una fila de una
tabla. `INITIALIZING → RUNNING` sigue, después de este capítulo, exactamente igual de documentada
en prosa y exactamente igual de sin ejercitar con código: `AgentLoop.runTurn` (CH-01 §11) nunca
comprueba que `state.status == RUNNING` antes de operar — su único guard rechaza los cuatro
estados terminales (`COMPLETED`/`FAILED`/`CANCELLED`/`EXPIRED`), y por lo tanto, tal como CH-01 lo
escribió, `runTurn` aceptaría sin protestar un `AgentState` en `status = INITIALIZING` exactamente
igual que uno en `RUNNING` — una asimetría real entre el diagrama de Article V (que sí distingue
ambos estados) y el código de `AgentLoop` (que no los distingue todavía). Este capítulo señala esa
asimetría explícitamente en vez de resolverla en silencio, y sin tocar el código de CH-01 para
"arreglarla" (ver seccion 18).

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6) clasifica también los fallos que introduce este capítulo:

```text
VALIDATION
    AGENT_CONFIG_NOT_FOUND                    — activateAgent invocada con un agentId para el
                                                  que no existe ningún AgentConfig registrado
        → recoverable: FALSE, retryable: FALSE
    INCOHERENT_EXECUTION_BUDGET                — activateAgent recibió un AgentConfig cuyo
                                                  ExecutionBudget declara al menos un límite no
                                                  positivo
        → recoverable: FALSE, retryable: FALSE
    INITIALIZATION_REQUIRES_CREATED_STATE      — beginAgentInitialization invocada sobre un
                                                  AgentState cuyo status no es CREATED
        → recoverable: FALSE, retryable: FALSE
```

Los tres fallos de este capítulo son violaciones de precondición del llamador — nunca de
infraestructura — y por eso ninguno emite ningún `AgentEvent` antes de su `THROW`: mismo patrón
que `TURN_ON_TERMINAL_STATE` (CH-01), `SESSION_ID_MISMATCH` (CH-10) o cualquiera de las
validaciones de precondición que este libro ya estableció. `recoverable = FALSE` y
`retryable = FALSE` en los tres casos: reintentar la misma llamada con los mismos argumentos nunca
resuelve un `agentId` inexistente, un `ExecutionBudget` incoherente, ni un `AgentState` que ya dejó
de estar en `CREATED`.

`activateAgent` y `beginAgentInitialization` nunca devuelven una excepción cruda ni un `AgentState`
a medias cuando algo falla: siempre construyen un `HarnessError` con `category`, `recoverable` y
`retryable` explícitos — mismo patrón que cada función anterior del libro.

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo de `category =
INFRASTRUCTURE` que pudiera ocurrir en una implementación real de `findAgentConfig` (por ejemplo,
un almacén de configuraciones completamente inalcanzable) — ese valor de `ErrorCategory` sigue,
después de este capítulo, sin que ningún componente real lo haya ejercitado nunca.

## 14. Eventos Producidos (Events Produced)

Este capítulo no agrega ningún valor nuevo a `AgentEventType` — y, a diferencia de cada uno de los
diez capítulos anteriores (salvo `EventBus`, CH-09, que tampoco agregó ninguno, por una razón
distinta: no decide qué información contiene ningún evento), este capítulo reutiliza un valor que
llevaba declarado, sin dueño, desde la primera página del libro:

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
valores permitido para `eventType` tampoco crece en este capítulo.

**Por qué este capítulo es el primero en emitir `RUN_STARTED`.** CH-00 §6 declaró `RUN_STARTED`
entre los cuatro valores originales de `AgentEventType`, documentado explícitamente como "aún no
implementado; declarado para uso futuro" (CH-00 §14). CH-01 §14 repitió la misma nota, ya con
lenguaje de propiedad: "`RUN_STARTED` pertenece al arranque de un `AgentRun` (todavía sin
componente propio que lo orqueste)". Diez capítulos completos —`ToolRuntime`, `ModelGateway`,
`ContextEngine`, `PolicyEngine`, `HumanInteractionService`, `ExecutionController`,
`CapabilityRegistry`, `EventBus`, `SessionManager`— pasaron sin que ninguno lo reclamara, porque
ninguno orquesta el arranque de un run: cada uno actúa sobre un run que ya está, de alguna forma,
en curso. `beginAgentInitialization` (seccion 11) es, por fin, la función que orquesta ese
arranque — y `RUN_STARTED` es exactamente el evento que le corresponde, once capítulos después de
que el valor quedara reservado.

`RUN_FAILED`, el otro valor que CH-01 §14 dejó explícitamente pendiente ("a un `HarnessError` no
recuperable a nivel de todo el run"), sigue sin emitirse en este capítulo: los tres fallos de la
seccion 13 son violaciones de precondición sobre la solicitud de activación, no el fallo de un run
que ya llegó a existir — la misma distinción que separa `TURN_ON_TERMINAL_STATE` (CH-01) de
`RUN_FAILED`.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

`AgentCore` nunca decide autorización (`P-13` sigue siendo exclusivo de `PolicyEngine`, CH-05):
`activateAgent` valida que un `AgentConfig` exista y que su `ExecutionBudget` sea coherente, nunca
si el agente o su llamador tienen permiso para activarse — esa es, precisamente, la clase de
decisión que Amendment v1.1 asigna a un `AdmissionController` (ver más abajo), no a `AgentCore`.

**La distinción con `ActivationRequest` (Amendment v1.1, `P-16`/`P-17`), explícita y completa.**
Este es el límite más delicado de este capítulo, y merece repetirse con precisión, igual que CH-10
repitió la frontera `SessionManager`/`HumanInteractionService`. `P-16` exige que todo estímulo
externo (prompts, APIs, webhooks, colas, horarios, eventos, archivos, bases de datos, sistemas u
otros agentes) se normalice hacia un `ActivationRequest` **antes de entrar al núcleo de
ejecución** — y `P-17` exige que ningún `ActivationRequest` tenga derecho inherente a ejecutarse:
un `AdmissionController` debe aplicar identidad, autorización, tenant, capacidad, rate, presupuesto,
deduplicación y policy antes de admitirlo (`INV-E01`/`INV-E02`). Ninguna de esas dos piezas —
`ActivationRequest` ni `AdmissionController` — se modela en este capítulo: pertenecen al "Ingress &
Activation Plane" de Amendment v1.1, explícitamente Enterprise, fuera de alcance de BH-v0.1 (mismo
tipo de exclusión que `P-22`, gobernanza de datos, CH-06/CH-10).

`AgentActivationRequest` (C-021, este capítulo) es, deliberadamente, un concepto más acotado y
posterior en la cadena: parte siempre de un `agentId` **ya resuelto** y un `AgentConfig` **ya
registrado** — nunca de un estímulo externo crudo. En la topología completa que Amendment v1.1
describe, `AgentCore.activateAgent` ocurriría, en el mejor de los casos, después de que un
`AdmissionController` ya admitió la solicitud; en el alcance actual de BH-v0.1, sin ese plano
Enterprise todavía construido, `AgentActivationRequest` es simplemente la única solicitud de
activación que el libro modela. Confundir ambos conceptos — tratar `activateAgent` como si ya
implementara `P-16`/`P-17` — sería exactamente el error que Article IV (Ownership Rule) prohíbe:
atribuirle a un componente una decisión (admisión, autorización de tenant, rate limiting) que su
propia ficha no declara en `owns`.

**La frontera con `AgentLoop` (Article IV), de nuevo.** `beginAgentInitialization` transiciona
`CREATED → INITIALIZING` y se detiene ahí — nunca invoca `runTurn`, nunca evalúa
`modelFinished`/`modelProposesToolCall`, nunca decide si un turno de razonamiento debe ocurrir. Si
`AgentCore` alguna vez avanzara el `AgentState` más allá de `INITIALIZING` por su cuenta —por
ejemplo, decidiendo también la primera transición hacia `RUNNING`— empezaría a competir con
`AgentLoop` por una decisión que Article IV ya le asignó a un dueño distinto desde CH-01.

**Lo que este capítulo NO implementa todavía.** Ningún control de autorización sobre quién puede
invocar `activateAgent` para un `agentId` ajeno — `findAgentConfig` acepta cualquier `agentId` que
reciba, sin verificar que quien invoca tenga permiso sobre ese agente. Esto es una limitación real,
documentada aquí y en la seccion 18, no un descuido silencioso — la misma clase de límite que CH-10
§15 documentó para `reconstructSessionState`/`branchSessionFromCheckpoint`.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST ActivateAgentRejectsAnUnknownAgentId
TEST ActivateAgentRejectsAnIncoherentExecutionBudget
TEST ActivateAgentNeverEmitsAnEventBeforeThrowing
TEST ActivateAgentAlwaysProducesStatusCreatedWithCurrentTurnZero
TEST BeginAgentInitializationRejectsAnyStatusOtherThanCreated
TEST BeginAgentInitializationIsTheFirstRealExerciseOfCreatedToInitializing
TEST BeginAgentInitializationAlwaysConstructsAFreshExecutionContext
TEST BeginAgentInitializationEmitsRunStartedForTheFirstTimeInTheBook
TEST AgentCoreNeverInvokesRunTurnOrAnyTurnContinuationLogic
TEST AgentCoreNeverConflatesItselfWithTheAmendmentActivationRequest
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.1, después de CH-11)

Constitution
 ├── Article III  — Component Sovereignty (AgentCore: undécimo y último componente instanciado;
 │                   de los once nombres de Article III, ninguno sigue en preview)
 ├── Article IV   — Decision Ownership (AgentCore, como EventBus, CH-09, sin fila propia — por
 │                   una razón distinta: su decisión ocurre antes de que exista ningún AgentRun)
 └── Article V    — Lifecycle (CREATED → INITIALIZING ejercitada con código real por primera vez)

Contracts (registry/contracts.yaml)
 ├── C-001 AgentMessage                (CH-00)
 ├── C-002 AgentConfig                 (CH-00 — validado ahora también por CMP-011)
 ├── C-003 AgentState                  (CH-00 — producido ahora también por CMP-011)
 ├── C-004 ExecutionContext            (CH-00 — producido ahora también por CMP-011)
 ├── C-005 ContextSnapshot             (CH-04)
 ├── C-006 ModelRequest                (CH-03)
 ├── C-007 ModelResponse               (CH-03)
 ├── C-008 ToolCall                    (CH-02)
 ├── C-009 ToolResult                  (CH-02)
 ├── C-010 AgentEvent                  (CH-00 — producido ahora también por CMP-011)
 ├── C-011 HarnessError                (CH-00 — producido ahora también por CMP-011)
 ├── C-012 ExecutionBudget             (CH-00 — consumido ahora también por CMP-011)
 ├── C-013 AgentRunStatus              (CH-01)
 ├── C-014 PolicyDecision              (CH-05)
 ├── C-015 HumanInteractionRequest     (CH-06)
 ├── C-016 HumanInteractionResolution  (CH-06)
 ├── C-017 ExecutionDecision           (CH-07)
 ├── C-018 CapabilityDescriptor        (CH-08)
 ├── C-019 EventSubscription           (CH-09)
 ├── C-020 SessionState                (CH-10)
 └── C-021 AgentActivationRequest      (CH-11, nuevo — la solicitud que hace nacer el primer
                                        AgentState de un nuevo run)

Components (registry/components.yaml)
 ├── CMP-001 AgentLoop                 (CH-01)
 ├── CMP-002 ToolRuntime                (CH-02)
 ├── CMP-003 ModelGateway               (CH-03)
 ├── CMP-004 ContextEngine              (CH-04)
 ├── CMP-005 PolicyEngine               (CH-05)
 ├── CMP-006 HumanInteractionService    (CH-06)
 ├── CMP-007 ExecutionController        (CH-07)
 ├── CMP-008 CapabilityRegistry         (CH-08)
 ├── CMP-009 EventBus                   (CH-09)
 ├── CMP-010 SessionManager             (CH-10)
 └── CMP-011 AgentCore                  (CH-11, nuevo — undécimo y último componente de Article
                                          III; ninguno de los once nombres sigue en preview)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado real `AgentCore → AgentLoop`**: ningún componente invoca todavía
  `activateAgent`/`beginAgentInitialization` seguido de `runTurn` como un único flujo — y, más
  puntualmente, `AgentLoop.runTurn` (CH-01) sigue sin distinguir `INITIALIZING` de `RUNNING` en su
  guard (ver seccion 12): la transición `INITIALIZING → RUNNING` sigue documentada solo en prosa.
- **El cableado real `AgentCore → SessionManager`**: `beginAgentInitialization` no invoca
  `createOrUpdateSessionCheckpoint` — el primer checkpoint de una sesión recién activada sigue
  siendo, después de este capítulo, un paso manual no modelado.
- **El mecanismo real detrás de `findAgentConfig`**: primitiva asumida, sin modelar qué registro o
  almacén concreto resuelve un `agentId` hacia su `AgentConfig`.
- **El "Ingress & Activation Plane" completo de Amendment v1.1** (`ActivationRequest`,
  `AdmissionController`, `P-16`/`P-17`, `INV-E01`/`INV-E02`): explícitamente distinto de
  `AgentActivationRequest` (ver seccion 6/15) y fuera de alcance de BH-v0.1.
  `AgentCommunicationGateway`, `CredentialBroker` y el resto de componentes de Amendment v1.1: igual
  de fuera de alcance.
- **Autorización sobre quién puede activar un agente ajeno**: señalado explícitamente en la
  seccion 15 como un límite de seguridad real, no silenciado.
- **Reactivación, desactivación o versión de un `AgentConfig` ya existente**: no modelado — este
  capítulo solo valida un `AgentConfig` que ya existe, nunca lo crea, actualiza ni retira.
- **Cancelación de una activación a medio camino** (entre `activateAgent` y
  `beginAgentInitialization`): no modelado — `ExecutionController` (CH-07) sigue gobernando
  cancelación solo para runs que ya están operacionalmente en curso.
- Reviewers plurales, evals y orquestación multi-agente: explícitamente fuera de alcance de BH-v0.1
  (igual que todos los capítulos anteriores).

## 19. Siguiente Incremento (Next Increment)

Con este capítulo, los once nombres que Article III enumera en su árbol de "Agent Runtime" tienen,
todos, un componente real en `registry/components.yaml` — ninguno sigue siendo únicamente una
palabra en una tabla de preview. El problema natural del próximo incremento ya no es introducir un
componente nuevo: es el capítulo de integración de punta a punta que CH-02..CH-10 fueron
posponiendo, capítulo a capítulo, en sus propias secciones 18/19, y que este capítulo hereda
también — cablear de verdad `AgentCore → AgentLoop → ContextEngine → ModelGateway →
CapabilityRegistry → PolicyEngine → ToolRuntime → HumanInteractionService → SessionManager →
EventBus` como un único flujo operante, resolviendo en el camino las asimetrías que este capítulo
señaló sin cerrar (`INITIALIZING → RUNNING` sin ejercitar, `AgentCore → SessionManager` sin
cablear).

`next_chapter` queda en `null` en el frontmatter de este capítulo porque, en este momento del
libro, ese próximo capítulo todavía no existe como archivo — solo como el problema que motivaría su
escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg /
> Bucles de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows),
> secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): después de diez capítulos reales, `AgentLoop.runTurn`
   siempre recibió un `AgentState` ya existente como parámetro — nunca explicó quién lo creó, ni de
   dónde salió su `runId`; `AgentConfig` tenía contrato desde la primera página del libro, pero
   ningún componente real lo validaba nunca antes de que una ejecución arrancara.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): un nombre puede
   vivir en Article III desde la primera versión de la Constitution adoptada, y ser citado
   literalmente por dos invariantes (`INV-01`, `INV-16`) desde CH-00, y seguir siendo, capítulo tras
   capítulo, solo una entrada de preview mientras cada componente vecino resuelve su propio
   dominio, dejando el origen mismo de la primera ejecución como un supuesto silencioso.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `AgentCore` (CMP-011) con una ficha que declara tanto lo que posee (`owns`: identidad del
   agente, validación de configuración, instanciación del primer `AgentState`, la transición
   `CREATED → INITIALIZING`) como lo que explícitamente NO posee (`does_not_own`: las cuatro
   exclusiones literales de Article III, más no competir con `AgentLoop`) y formaliza
   `AgentActivationRequest` (C-021), la solicitud que por fin hace posible mostrar, con código
   real, cómo nace un `AgentState`.
4. **Modelos mentales** (= §4, Constitutional Impact): Article IV formula todas sus preguntas sobre
   una ejecución que YA EXISTE — el componente que este capítulo introduce no le falta una fila en
   esa tabla porque no decida nada (como `EventBus`, CH-09): le falta porque su decisión ocurre en
   el instante anterior a que cualquier pregunta de Article IV tenga sentido.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un componente nuevo se introduce sin declarar
  explícitamente su `does_not_own`, aumenta la probabilidad de que absorba silenciosamente la
  próxima decisión vecina "porque ya estaba ahí" — el mismo bucle que CH-01..CH-10 ya cortaron.
  Este capítulo enfrenta una variante nueva: al ser el componente que arranca literalmente toda
  ejecución, sería fácil que también empezara a decidir su continuación turno a turno.
- **Bucle de equilibrio (estabiliza):** `beginAgentInitialization` (§11) transiciona el
  `AgentState` exactamente una vez, de `CREATED` a `INITIALIZING`, y se detiene ahí — nunca invoca
  `runTurn` ni ninguna lógica de continuación, dejando el testigo intacto para `AgentLoop`.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es dividir la activación en dos funciones distintas
— `activateAgent` (produce `CREATED`, sin evento) y `beginAgentInitialization` (transiciona a
`INITIALIZING`, con el primer `ExecutionContext` real del libro y el primer `RUN_STARTED` jamás
emitido) — en vez de una sola función que hiciera las dos cosas a la vez. Si `AgentCore` colapsara
ambos pasos en uno, ningún componente futuro podría observar, ni auditar, el instante exacto en el
que un run existe pero todavía no ha empezado a prepararse para correr.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo
> de esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set`
> (frontmatter) y es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa,
> para lectura directa del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Un componente ya existente siempre recibe, como parámetro, un estado de ejecución que ya existe
   — nunca explica quién lo creó la primera vez, ni de dónde salió su identificador de run. ¿Quién
   instancia ese primer estado, antes de que exista ningún turno que decidir, y qué necesita
   validar antes de dejarlo existir? *(cierra la pregunta guía 1)*
2. Un componente ya existente distingue el estado operativo de una ejecución en curso de la
   historia persistida de una sesión completa — pero ninguno de los dos representa qué agente es,
   en sí mismo, independientemente de cualquier ejecución o sesión particular. ¿Qué representa esa
   tercera capa, y quién es responsable de validarla antes de que exista la primera ejecución?
   *(cierra la pregunta guía 2)*
3. Si un componente ya decide si otro turno de razonamiento debe ocurrir una vez que una ejecución
   está en curso, ¿por qué esa misma decisión no basta para decidir si esa ejecución debería,
   siquiera, llegar a existir? *(cierra la pregunta guía 3)*
4. El lifecycle formal de una ejecución define un primer estado en el que un run apenas existe, y
   un segundo en el que ya se está preparando para correr. ¿Qué tiene que validarse antes de que
   esa transición ocurra, y qué produce exactamente del otro lado? *(cierra la pregunta guía 4)*

### Explicar

1. `AgentCore` posee representar la identidad de un agente y validar su `AgentConfig` antes de que
   arranque cualquier ejecución. Explica, como si hablaras con alguien sin contexto técnico, por
   qué NO posee decidir si otro turno de razonamiento debe ocurrir una vez que el run ya está
   corriendo.
2. `AgentActivationRequest.sessionId` es `Optional`. Explica por qué modelar la posibilidad de
   adjuntarse a una sesión ya existente como un campo opcional es preferible a exigir siempre un
   `sessionId` nuevo o siempre uno provisto por el llamador.

### Conectar

1. `AgentLoop.runTurn` (CH-01) recibe un `AgentState` ya existente y nunca pregunta quién lo
   produjo. ¿Qué valor exacto de `AgentRunStatus` tiene el `AgentState` que este capítulo entrega,
   y por qué el guard de `runTurn` no lo rechazaría ni lo distinguiría de `RUNNING`?
2. `SessionManager` (CH-10) construye un `SessionCheckpoint` embebiendo una copia de cualquier
   `AgentState` que reciba. ¿Podría aceptar el primer `AgentState` que este capítulo produce sin
   cambiar una sola línea de su propio código, y qué campo de `SessionState` confirmaría que esa
   sesión nació de una activación?

### Espaciar

Las cinco tarjetas de repaso de este capítulo (dos sobre `AgentCore` — su `owns` y su
`does_not_own` —, dos sobre `AgentActivationRequest` — sus campos y por qué este capítulo ejercita
por primera vez `RUN_STARTED` —, y una sobre la ausencia de fila en Article IV) entran hoy en
`reviewStage = DAY_1`. Repásalas de nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) — ver
el apéndice de tarjetas al final del libro (edición PDF) o `retrieval_set.flashcards` en
`dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te equivocaste,
ese es precisamente el punto ciego que este método existe para revelar.
