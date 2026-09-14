---
id: CH-10
title: "SessionManager y la Persistencia Durable de una Sesión"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-010]
introduces_contracts: [C-020]
modifies_contracts: []
constitutional_articles: [P-04, P-08, P-23, INV-12, INV-13, INV-18, INV-19, INV-20]
previous_chapter: CH-09
next_chapter: CH-11
retrieval_set:
  expected_outcome:
    id: EO-CH10
    text: |
      Al terminar este capítulo podrás distinguir, dentro de la historia completa de una sesión que
      puede abarcar múltiples ejecuciones a lo largo del tiempo, qué tramo le pertenece en exclusiva
      al componente que persiste, recupera, hace checkpoint y reconstruye esa historia, y qué tramos
      pertenecen a dominios distintos (el estado operativo de una única ejecución en curso, la
      persistencia acotada de una interacción humana pendiente, decidir continuación de turno,
      distribuir eventos ya producidos) — y podrás diseñar, para cualquier historia de sesión
      persistida, una representación que registre qué ejecuciones le pertenecen, desde qué punto
      puede reconstruirse, y si ese punto proviene de una rama distinta de su propio linaje, sin
      confundir nunca esa copia persistida con la fuente de verdad de una ejecución activa.
  skeleton:
    id: SK-CH10
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
    components_to_be_introduced: [CMP-010]
    contracts_to_be_introduced: [C-020]
  guiding_questions:
    - id: GQ-CH10-01
      text: |
        AgentState (CH-00) representa el estado operativo de una única ejecución en curso, y varias
        ejecuciones pueden ocurrir, una tras otra, dentro de la misma sesión a lo largo del tiempo.
        ¿Quién persiste, recupera y reconstruye la historia que abarca esas múltiples ejecuciones —
        distinta del estado operativo de cualquiera de ellas en curso — y qué le permitiría, después
        de un reinicio, reconstruirse desde lo que ya persistió?
      answered_by: RQ-CH10-01
    - id: GQ-CH10-02
      text: |
        Desde la primera versión de la Constitution adoptada por este libro, un invariante declara
        que el estado operativo de una ejecución y la historia persistente de una sesión son
        conceptualmente independientes — pero, después de nueve capítulos reales, solo uno de los
        dos conceptos tiene un contrato registrado. ¿Qué forma debería tener el otro, y qué
        necesitaría contener para que una ejecución durable pudiera reconstruirse desde estado ya
        persistido?
      answered_by: RQ-CH10-02
    - id: GQ-CH10-03
      text: |
        Si una sesión durable pudiera, en algún momento, retomar su historia desde más de un punto
        anterior — abriendo una rama alterna en vez de continuar linealmente desde su último punto —
        ¿qué información tendría que persistir para que ese linaje quedara explícito, en vez de
        sobrescribir en silencio el registro anterior?
      answered_by: RQ-CH10-03
    - id: GQ-CH10-04
      text: |
        HumanInteractionService (CH-06) ya persiste sus propias solicitudes de interacción humana
        pendientes como una responsabilidad propia y acotada, señalando explícitamente que la
        persistencia real de fondo pertenecía a un componente todavía sin construir. Ahora que ese
        componente existe, ¿debería absorber esa responsabilidad ya acotada, o hay una razón real
        para mantenerla separada?
      answered_by: RQ-CH10-04
  systems_lens:
    iceberg_visible_fact: |
      Después de nueve capítulos reales, `AgentState` (C-003, CH-00) tiene contrato registrado desde
      la primera página del libro, pero la historia persistente de una sesión — que la misma
      Constitution nombra por su propio nombre, `SessionState`, desde P-08/INV-12 — nunca llegó a
      tener uno: `persistHumanInteractionRequest`/`persistHumanInteractionResolution` (CH-06) siguen
      siendo primitivas asumidas, y `EventBus` (CH-09) documentó explícitamente que distribuye en el
      momento, sin persistir nada que sobreviva a un reinicio (ver seccion 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite, ahora aplicado a la persistencia durable, es que un componente puede
      nombrarse en la Constitution desde su primera versión adoptada — igual que `EventBus` en CH-09
      — y seguir siendo, capítulo tras capítulo, solo una palabra en Article III mientras cada
      componente vecino resuelve su propia persistencia acotada (`HumanInteractionService`, CH-06)
      dejando siempre la persistencia general de la sesión como la misma nota al pie: "eso es trabajo
      de `SessionManager`" (ver seccion 3, Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala el décimo componente real del libro, `SessionManager` (CMP-010), con una
      ficha que declara tanto lo que posee (`owns`: persistencia, recuperación, branching,
      checkpoints, reconstrucción — cita literal de Article III) como lo que explícitamente NO posee
      (`does_not_own`: el estado operativo de una ejecución en curso, la persistencia acotada de
      `HumanInteractionService`, decidir continuación de turno, distribuir eventos) — y formaliza
      `SessionState` (C-020), el contrato que cierra, por fin, el nombre que INV-12 ya usaba sin
      definición desde CH-00 (ver seccion 8, Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es P-08 ("Agent state and session state are
      different concerns") junto con INV-12 ("`AgentState` y `SessionState` permanecen
      conceptualmente independientes") e INV-13 ("una ejecución durable debe poder reconstruirse
      desde estado persistido suficiente"): `SessionState` nunca sustituye a `AgentState` como fuente
      de verdad de una ejecución activa — solo conserva una copia inmutable de él, tantas veces como
      haga falta, para que la historia completa de la sesión sobreviva más allá de cualquier ejecución
      individual (ver seccion 4, Impacto Constitucional).
    reinforcing_loop: |
      Cada vez que un componente nuevo se introduce sin declarar explícitamente su `does_not_own`,
      aumenta la probabilidad de que absorba silenciosamente la próxima decisión vecina "porque ya
      estaba ahí" — el mismo bucle que CH-01..CH-09 ya cortaron. Este capítulo lo repite para
      `SessionManager`, con una variante nueva: la tentación no viene de una decisión vecina, sino de
      que `SessionManager` tiene, literalmente, una copia completa de un `AgentState` real dentro de
      cada checkpoint que persiste — sería fácil, con esa copia en la mano, empezar a tratarla como si
      fuera la ejecución activa en vez de un registro histórico de ella.
    balancing_loop: |
      `createOrUpdateSessionCheckpoint` (seccion 11) es el mecanismo de equilibrio: nunca muta el
      `AgentState` que recibe ni lo trata como la fuente de verdad de la ejecución en curso — solo lo
      embebe, sin tocarlo, dentro de un `SessionCheckpoint` nuevo, mientras `AgentLoop` (CH-01) sigue
      siendo, sin ningún cambio, el único dueño del estado operativo real de esa ejecución.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `SessionState` (C-020) registre
      `parentCheckpointId` como un campo `Optional` — casi siempre `NULL` — en vez de que cada
      ramificación de una sesión sobrescribiera en silencio el registro anterior. Si esa referencia de
      linaje se omitiera, ninguna implementación futura podría distinguir, después del hecho, si una
      sesión continuó linealmente su propia historia o si, en algún punto, se bifurcó desde el
      checkpoint de otra.
  recall_questions:
    - id: RQ-CH10-01
      text: |
        ¿Qué componente persiste, recupera, hace checkpoint y reconstruye la historia de una sesión
        — distinta del estado operativo de una ejecución en curso — y qué contrato representa esa
        historia ya persistida?
    - id: RQ-CH10-02
      text: |
        ¿Qué campos tiene `SessionState` (C-020), y cuál de ellos embebe, sin modificarlo, un
        contrato que ya existía desde CH-00?
    - id: RQ-CH10-03
      text: |
        ¿Qué campo de `SessionState` permite expresar que una sesión se ramificó desde un checkpoint
        anterior, y qué valor tiene ese campo cuando no hubo ninguna ramificación?
    - id: RQ-CH10-04
      text: |
        ¿Qué persiste `HumanInteractionService` por su cuenta (CH-06), y por qué `SessionManager` no
        absorbe esa responsabilidad aunque ambos, en algún sentido, "persisten" algo?
  explain_prompts:
    - id: EP-CH10-01
      text: |
        `SessionManager` posee persistir, recuperar, hacer checkpoint y reconstruir la historia de
        una sesión. Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee el
        estado operativo de una ejecución en curso (`AgentState`) — ¿qué se rompería, en concreto, si
        `SessionManager` empezara a tratar la copia de un `AgentState` que guarda dentro de un
        checkpoint como si fuera la ejecución activa, en vez de un registro histórico de ella?
      target_entity: CMP-010
    - id: EP-CH10-02
      text: |
        `SessionState.parentCheckpointId` es `Optional` y, en la inmensa mayoría de los casos, `NULL`.
        Explica por qué modelar el linaje de una ramificación como un campo opcional de referencia —
        en vez de, por ejemplo, un campo obligatorio o una lista completa de sesiones derivadas — es
        preferible, y qué perderíamos si `SessionState` no distinguiera nunca entre continuar
        linealmente y abrir una rama.
      target_entity: C-020
  interleaved_questions:
    - id: IQ-CH10-01
      text: |
        `AgentLoop` (CH-01) produce un `AgentState` (C-003) nuevo después de cada turno, una
        estructura que solo describe el estado operativo de una única ejecución en curso. ¿Qué campo
        de ese `AgentState` ya producido lee `SessionManager` para poblar `SessionCheckpoint.runId`,
        y por qué embeber una copia completa de ese `AgentState` dentro de un checkpoint no viola
        INV-12, aunque `SessionState` termine "conteniendo", en cierto sentido, un `AgentState`
        completo?
      current_chapter_entities: [CMP-010, C-020]
      prior_chapter_entities: [CMP-001, C-003]
      prior_chapter: CH-01
    - id: IQ-CH10-02
      text: |
        `HumanInteractionService` (CH-06) ya persiste, por su cuenta, `HumanInteractionRequest` y
        `HumanInteractionResolution` mediante primitivas que su propio capítulo marcó explícitamente
        como "la persistencia real de fondo pertenece a `SessionManager`, todavía sin construir".
        Ahora que `SessionManager` existe con código real, ¿qué campo de su propia ficha
        (`does_not_own`) confirma que esa persistencia acotada sigue siendo de `HumanInteractionService`,
        y qué se perdería si `SessionManager` la absorbiera en vez de mantenerla separada?
      current_chapter_entities: [CMP-010, C-020]
      prior_chapter_entities: [CMP-006, C-015]
      prior_chapter: CH-06
  flashcards:
    - id: FC-CH10-01
      front: |
        ¿Qué posee `SessionManager` (Article III / Article IV), en una frase?
      back: |
        Persistencia, recuperación, branching, checkpoints y reconstrucción de la historia de una
        sesión — cita literal de Article III, sección "SessionManager"; responde, por primera vez con
        código real, "What execution history and checkpoints persist?" (Article IV).
      source_entity: CMP-010
      chapter_introduced_in: CH-10
      review_stage: DAY_1
    - id: FC-CH10-02
      front: |
        ¿Qué NO posee `SessionManager`, y a qué componentes pertenecen esas decisiones?
      back: |
        El estado operativo de una ejecución en curso (`AgentState`, propiedad de `AgentLoop`, ya
        introducido en CH-01 — P-08/INV-12), la persistencia acotada de sus propias solicitudes de
        interacción humana (`HumanInteractionService`, ya introducido en CH-06), decidir continuación
        de turno (`AgentLoop`) y distribuir eventos ya producidos (`EventBus`, ya introducido en
        CH-09) — aunque podría suscribirse a `EventBus` como un consumidor más para reconstruir
        historial.
      source_entity: CMP-010
      chapter_introduced_in: CH-10
      review_stage: DAY_1
    - id: FC-CH10-03
      front: |
        ¿Qué campos tiene `SessionState` (C-020), y qué representan?
      back: |
        `sessionId` (`SessionId`), `runIds` (`List<RunId>`, qué ejecuciones pertenecen a esta sesión),
        `latestCheckpoint` (`SessionCheckpoint`, embebido — desde qué punto puede reconstruirse),
        `parentCheckpointId` (`Optional<SessionCheckpointId>`, linaje de ramificación, `NULL` si no
        hubo ninguna), `createdAt` y `updatedAt` (`Timestamp`).
      source_entity: C-020
      chapter_introduced_in: CH-10
      review_stage: DAY_1
    - id: FC-CH10-04
      front: |
        ¿Por qué este capítulo es el primero en clasificar un fallo real bajo `ErrorCategory.PERSISTENCE`?
      back: |
        Porque `PERSISTENCE` fue declarada desde CH-00 entre los diez valores originales de
        `ErrorCategory`, pero ningún componente de CH-00..CH-09 la necesitó de verdad — CH-06 y CH-09
        documentaron explícitamente que la persistencia real de fondo era trabajo de `SessionManager`,
        todavía sin construir. `createOrUpdateSessionCheckpoint`/`branchSessionFromCheckpoint` la
        ejercitan por primera vez cuando `persistSessionState` falla.
      source_entity: C-020
      chapter_introduced_in: CH-10
      review_stage: DAY_1
    - id: FC-CH10-05
      front: |
        ¿Por qué `SessionState.parentCheckpointId` es `Optional`, en vez de obligatorio?
      back: |
        Porque la inmensa mayoría de las actualizaciones de una sesión son continuaciones lineales de
        su propia historia, sin ninguna ramificación — obligar a este campo forzaría a inventar un
        valor sin significado real en el caso común. `Optional` con `NULL` por defecto deja que solo
        `branchSessionFromCheckpoint` (seccion 11) lo pueble, cuando de verdad ocurre una rama.
      source_entity: C-020
      chapter_introduced_in: CH-10
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH10-01
      recall_question: RQ-CH10-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH10-02
      recall_question: RQ-CH10-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH10-03
      recall_question: RQ-CH10-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH10-04
      recall_question: RQ-CH10-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 10 — SessionManager y la Persistencia Durable de una Sesión

> **Regla constitucional (Article III, sección "SessionManager"):** responsable de persistencia,
> recuperación, branching, checkpoints y reconstrucción.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de saber
> cómo se llama el componente de este capítulo. El detalle estructurado de esta sección vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, dentro de la historia completa
de una sesión que puede abarcar múltiples ejecuciones a lo largo del tiempo, qué tramo le pertenece
en exclusiva al componente que este capítulo introduce y qué tramos pertenecen a dominios distintos
(el estado operativo de una única ejecución en curso, la persistencia acotada de una interacción
humana pendiente, decidir continuación de turno, distribuir eventos ya producidos) — y podrás
diseñar, para cualquier historia de sesión persistida, una representación que registre qué
ejecuciones le pertenecen, desde qué punto puede reconstruirse, y si ese punto proviene de una rama
distinta de su propio linaje, sin confundir nunca esa copia persistida con la fuente de verdad de una
ejecución activa.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e introduce
un contrato de datos nuevo y el décimo componente de runtime del libro — todavía sin explicarlos,
solo como mapa.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar atrás;
están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este capítulo va
a definir):

1. `AgentState` (CH-00) representa el estado operativo de una única ejecución en curso, y varias
   ejecuciones pueden ocurrir, una tras otra, dentro de la misma sesión a lo largo del tiempo. ¿Quién
   persiste, recupera y reconstruye la historia que abarca esas múltiples ejecuciones — distinta del
   estado operativo de cualquiera de ellas en curso — y qué le permitiría, después de un reinicio,
   reconstruirse desde lo que ya persistió?
2. Desde la primera versión de la Constitution adoptada por este libro, un invariante declara que el
   estado operativo de una ejecución y la historia persistente de una sesión son conceptualmente
   independientes — pero, después de nueve capítulos reales, solo uno de los dos conceptos tiene un
   contrato registrado. ¿Qué forma debería tener el otro, y qué necesitaría contener para que una
   ejecución durable pudiera reconstruirse desde estado ya persistido?
3. Si una sesión durable pudiera, en algún momento, retomar su historia desde más de un punto
   anterior — abriendo una rama alterna en vez de continuar linealmente desde su último punto — ¿qué
   información tendría que persistir para que ese linaje quedara explícito, en vez de sobrescribir en
   silencio el registro anterior?
4. `HumanInteractionService` (CH-06) ya persiste sus propias solicitudes de interacción humana
   pendientes como una responsabilidad propia y acotada, señalando explícitamente que la persistencia
   real de fondo pertenecía a un componente todavía sin construir. Ahora que ese componente existe,
   ¿debería absorber esa responsabilidad ya acotada, o hay una razón real para mantenerla separada?

## 1. Arquitectura Actual (Current Architecture)

CH-00..CH-09 dejaron instalados diecinueve contratos de datos y nueve componentes de runtime. De los
once nombres que Article III enumera en su árbol de "Agent Runtime" (`AgentCore`, `AgentLoop`,
`ModelGateway`, `ContextEngine`, `ToolRuntime`, `PolicyEngine`, `SessionManager`,
`HumanInteractionService`, `EventBus`, `ExecutionController`, `CapabilityRegistry`), CH-09 dejó
exactamente dos todavía en preview: `AgentCore` y `SessionManager`.

`SessionManager` no es una omisión reciente — es la deuda intencional más citada del libro. Aparece
por nombre, marcado explícitamente como "preview" o "todavía no introducido", en el `does_not_own` o
la sección 9/18 de `AgentLoop` (CH-01, sobre quién persiste `AgentState` entre ejecuciones),
`ToolRuntime` (CH-02), `ContextEngine` (CH-04, sobre quién provee el historial real que hoy
`candidates` recibe ya dado), `HumanInteractionService` (CH-06, sobre quién persiste de verdad
`HumanInteractionRequest`/`HumanInteractionResolution`, más allá de las primitivas asumidas
`persistHumanInteractionRequest`/`persistHumanInteractionResolution`) y `EventBus` (CH-09, sobre quién
podría suscribirse para reconstruir historial a partir de eventos ya distribuidos). En total, el
nombre `SessionManager` aparece citado, entre los nueve archivos de capítulo reales, cerca de veinte
veces — más que cualquier otro componente todavía sin construir salvo `CapabilityRegistry`, que ya se
resolvió en CH-08.

Hay, además, una deuda constitucional más profunda que ningún capítulo anterior había cerrado:
`constitution/ARCHITECTURE_CONSTITUTION.md` Article II declara, desde la primera versión adoptada por
este repositorio, `INV-12` ("`AgentState` y `SessionState` permanecen conceptualmente
independientes") y Article I declara `P-08` ("Agent state and session state are different
concerns"). Ambos ya usan el nombre `SessionState` — pero, después de nueve capítulos reales y veinte
contratos registrados, ese nombre nunca llegó a tener una entrada en `registry/contracts.yaml`. Es el
mismo patrón que `AgentRunStatus` (C-013) resolvió en CH-01: un nombre que la Constitution ya
menciona por su cuenta, sin que ningún capítulo hubiera todavía formalizado el contrato detrás de él.

`AgentState` (C-003, CH-00) sí tiene contrato desde el primer capítulo:

```pseudocode
STRUCT AgentState
    runId: RunId
    sessionId: SessionId
    agentId: AgentId
    status: AgentRunStatus
    currentTurn: Integer
END
```

Nótese que `AgentState` ya incluye `sessionId` — la referencia hacia la sesión a la que pertenece esa
ejecución concreta — pero `AgentState` describe, exclusivamente, el estado operativo de **una única
ejecución en curso** (`runId`, `status`, `currentTurn`); no dice nada sobre qué otras ejecuciones
pertenecen a la misma sesión, ni desde qué punto podría reconstruirse esa sesión si el proceso que la
sostiene deja de existir.

`ErrorCategory` (C-011, CH-00) declara diez valores desde su primera versión — pero, después de nueve
capítulos reales, uno de ellos sigue sin que ningún componente lo haya ejercitado nunca:
`PERSISTENCE`. CH-06 §13 lo señaló explícitamente ("cualquier fallo de `category = PERSISTENCE` ...
esa semántica real pertenece a `SessionManager`, preview") y CH-09 §18 repitió la misma nota.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas para esto, la historia de una sesión que abarca múltiples
ejecuciones a lo largo del tiempo no tiene ningún lugar real donde persistir. `AgentState` describe
el presente operativo de una ejecución mientras esa ejecución está en curso — pero en cuanto termina
(o el proceso que la sostenía se reinicia), nada en el libro conserva un registro de que existió, de
qué otras ejecuciones comparten su misma sesión, ni de un punto desde el cual una implementación
futura podría reconstruir esa historia. `INV-13` exige que "una ejecución durable debe poder
reconstruirse desde estado persistido suficiente" — pero, hasta este capítulo, ningún componente
produce ese "estado persistido suficiente" de forma real.

Un segundo problema, más sutil: sin un dueño único para "¿qué persiste sobre la sesión, más allá de
lo que cada componente ya persiste por su cuenta?", es tentador que ese componente termine
absorbiendo, "ya que de todos modos persiste cosas", responsabilidades que otros componentes ya
resolvieron de forma acotada — en particular, la persistencia propia que `HumanInteractionService`
(CH-06) ya construyó para sus propias `HumanInteractionRequest`/`HumanInteractionResolution`. Que
ambos "persistan algo" no significa que deban fusionarse: son dos superficies de persistencia
distintas, con dueños distintos, y confundirlas sería repetir exactamente el error que Article IV
(Ownership Rule) prohíbe — un componente absorbiendo silenciosamente una decisión que ya pertenece a
otro dominio.

Necesitamos que "¿qué persiste sobre la historia de una sesión, y desde dónde puede reconstruirse?"
tenga, por fin, un dueño único y nombrado — que construya, a partir de un `AgentState` ya producido
por una ejecución existente, un registro persistido de la sesión a la que pertenece; que permita
reconstruir ese registro desde un punto ya persistido; que permita, cuando haga falta, abrir una rama
alterna de esa historia sin perder el rastro de dónde se originó; y que nunca trate su propia copia
persistida de un `AgentState` como si fuera la fuente de verdad de una ejecución activa.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los diecinueve contratos y los nueve componentes que existen hasta este punto no bastan porque:

- Article III nombra `SessionManager` en su árbol de "Agent Runtime" desde la primera versión de la
  constitución adoptada, con una responsabilidad explícita ("persistencia; recuperación; branching;
  checkpoints; reconstrucción") que ningún capítulo había materializado con código real;
- Article IV enumera una fila propia para `SessionManager` ("What execution history and checkpoints
  persist?") — a diferencia de `EventBus` (CH-09), que confirmó no tener ninguna, este componente sí
  tiene una pregunta real sin responder desde la primera versión de la tabla de Decision Ownership;
- `P-08`/`INV-12` ya usan el nombre `SessionState` desde la primera versión de la Constitution
  adoptada, sin que ningún capítulo hubiera formalizado jamás el contrato detrás de ese nombre —
  exactamente el mismo vacío que CH-01 cerró para `AgentRunStatus`;
- `INV-13` exige que una ejecución durable pueda reconstruirse desde estado persistido suficiente,
  pero ningún componente del libro produce, hasta este capítulo, ningún estado real que sobreviva a
  un reinicio: `persistHumanInteractionRequest`/`persistHumanInteractionResolution` (CH-06) siguen
  siendo primitivas asumidas que "en este incremento, no fallan", y `EventBus` (CH-09) distribuye en
  el momento, sin persistir nada;
- `ErrorCategory.PERSISTENCE` (CH-00) sigue siendo un valor declarado sin que ningún componente real
  haya clasificado jamás un fallo bajo esa categoría — la misma situación que `CONTEXT` (CH-04),
  `POLICY` (CH-05) y `HUMAN_INTERACTION` (CH-06) resolvieron cada uno para su propio dominio.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la secuencia
> `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una entidad que no
> haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT` registrado — **no
> magic entities**. Este capítulo aplica la misma disciplina de *ownership* que CH-01..CH-09 ya
> establecieron, con una particularidad nueva: por primera vez, un componente recibe, como parte de
> su propio material de entrada, una copia completa de un contrato que otro componente ya posee en
> exclusiva (`AgentState`, propiedad de `AgentLoop`) — y debe demostrar, con código real, que
> conservarla no equivale a poseerla.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-04   Every action produces observable events.
           createOrUpdateSessionCheckpoint / reconstructSessionState / branchSessionFromCheckpoint
           (seccion 11) emiten, cada una, un AgentEvent — el décimo componente del libro que
           produce eventos en la práctica.
    P-08   Agent state and session state are different concerns.
           Primera vez que este principio tiene, por fin, un componente real y un contrato real
           (SessionState, C-020) a cada lado de la frontera que declara: AgentState sigue siendo
           propiedad exclusiva de AgentLoop (CH-01); SessionState es lo que SessionManager persiste
           sobre la historia de la sesión — nunca el mismo dato, nunca la misma fuente de verdad.
    P-23   Durable execution is a core runtime property (Amendment v1.1).
           SessionCheckpoint (embebido en SessionState) es la primera materialización real de
           "persistence, checkpoint, pause, crash recovery and resume" que P-23 exige — sin que la
           memoria de un proceso en ejecución sea, nunca, la única fuente de verdad de una sesión
           durable.

Invariants preserved
    INV-12   AgentState y SessionState permanecen conceptualmente independientes.
             SessionState (C-020) nunca sustituye a AgentState (C-003) como fuente de verdad de una
             ejecución activa: SessionCheckpoint embebe una COPIA inmutable de un AgentState ya
             producido, nunca una referencia mutable ni el AgentState "real" que AgentLoop sigue
             poseyendo.
    INV-13   Una ejecución durable debe poder reconstruirse desde estado persistido suficiente.
             reconstructSessionState (seccion 11) es la primera formalización ejecutable de este
             invariante: reconstruye un SessionState completo a partir, exclusivamente, de un
             SessionCheckpoint ya persistido — sin necesitar ningún proceso en memoria que hubiera
             sobrevivido desde que ese checkpoint se creó.
    INV-18   Toda acción significativa produce un evento observable.
             Las tres operaciones reales de este capítulo (crear/actualizar un checkpoint,
             reconstruir, ramificar) emiten, cada una, su propio AgentEvent en el camino exitoso.
    INV-19   Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy relevante.
             Cada AgentEvent que emite SessionManager lleva el traceId de su ExecutionContext, y
             SessionState.parentCheckpointId deja trazable, cuando aplica, desde qué checkpoint
             concreto se originó una rama.
    INV-20   Todo error operacional pertenece a una categoría conocida.
             Este capítulo ejercita, por primera vez en el libro, ErrorCategory.PERSISTENCE — un
             valor declarado desde CH-00 sin que ningún componente lo hubiera necesitado hasta ahora.

Component ownership changes
    CMP-010 SessionManager se introduce — registry/components.yaml pasa de 9 a 10 componentes. De
    los once nombres de Article III, solo AgentCore sigue preview. owns/does_not_own citados
    literalmente contra Article III (sección "SessionManager") y Article IV. registry/
    components.yaml de CMP-001 (AgentLoop), CMP-006 (HumanInteractionService) y CMP-009 (EventBus)
    NO se modifica: ninguno cablea todavía su relación real con SessionManager (ver seccion 9/18).

Lifecycle changes
    Ninguno sobre AgentRunStatus (C-013): sigue siendo propiedad exclusiva de AgentLoop (CH-01), sin
    cambios. Este capítulo no introduce un ENUM de estados propio para SessionState (a diferencia de
    HumanInteractionStatus en CH-06 o EventSubscriptionStatus en CH-09) — su progresión se modela,
    en cambio, como una cadena de checkpoints enlazados por parentCheckpointId (ver seccion 12).

Security implications
    SessionManager nunca decide autorización (P-13 sigue siendo exclusivo de PolicyEngine, CH-05) ni
    absorbe la persistencia acotada que HumanInteractionService ya posee (CH-06). Ver seccion 15 para
    el análisis completo, incluyendo la frontera con la gobernanza de datos (P-22, Amendment v1.1),
    deliberadamente fuera de alcance.

Observability implications
    SessionManager es el décimo componente que emite AgentEvent en la práctica, extendiendo
    AgentEventType con cuatro valores nuevos (SESSION_CHECKPOINT_CREATED, SESSION_RECONSTRUCTED,
    SESSION_BRANCHED, SESSION_PERSISTENCE_FAILED) — el primer componente del libro cuyo evento de
    fallo (SESSION_PERSISTENCE_FAILED) corresponde a un fallo de infraestructura real, no a una
    violación de precondición del llamador.

Deterministic vs agentic boundary
    Article XII se refina una décima vez a nivel de componente: SessionManager, igual que EventBus
    (CH-09), no consume ninguna salida del modelo ni directa ni indirectamente — su frontera
    determinística es, exclusivamente, entre el estado operativo ya producido por una ejecución
    (AgentState, determinístico) y el registro persistido de la historia de la sesión.
```

## 5. Conceptos Nuevos (New Concepts)

- **Session**: la historia continua de un agente que puede abarcar múltiples `AgentRun` a lo largo
  del tiempo — ya nombrada desde CH-00 (`SessionId`, embebido en `AgentState`/`ExecutionContext`),
  pero sin que ningún contrato representara, hasta este capítulo, su historia persistida como un todo
  distinto de cualquier ejecución individual.
- **Checkpoint**: el punto persistido desde el cual una sesión puede reconstruirse — modelado como
  `SessionCheckpoint` (seccion 6), un `STRUCT` embebido dentro de `SessionState` sin contrato `C-XXX`
  propio, el mismo patrón que `ContextBlock` (CH-04) o `ExecutionUsage` (CH-07). Cada checkpoint
  embebe una copia inmutable de un `AgentState` ya producido — nunca una referencia mutable a la
  ejecución activa.
- **Branching**: la capacidad de que una sesión retome su historia desde un checkpoint que no es,
  necesariamente, el último de su propia línea — abriendo una nueva rama en vez de continuar
  linealmente. Modelada mediante `SessionState.parentCheckpointId` (`Optional`, seccion 6): `NULL`
  cuando no hubo ninguna ramificación, poblado con el id del checkpoint de origen cuando sí la hubo.
- **Session Reconstruction**: el tramo determinístico, exigido literalmente por `INV-13`, en el que
  se reconstruye un `SessionState` completo a partir, exclusivamente, de un `SessionCheckpoint` ya
  persistido — sin necesitar ningún proceso en memoria que hubiera sobrevivido desde que ese
  checkpoint se creó.
- **Decision Ownership** *(Article IV, en uso desde CH-01, ahora aplicado a un décimo componente)*:
  `SessionManager` decide "¿qué historia de ejecución y qué checkpoints persisten?"; explícitamente
  NO decide "¿cuál es el estado operativo de la ejecución en curso?" (`AgentLoop`, ya resuelto), "¿qué
  interacciones humanas pendientes persisten?" (`HumanInteractionService`, ya resuelto), "¿debe
  ocurrir otro turno?" (`AgentLoop`) ni "¿quién más se entera de un evento ya producido?"
  (`EventBus`, ya resuelto).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados de CH-00/CH-01/CH-06

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `SessionId`, `RunId`, `Timestamp`, `AgentState`,
`ExecutionContext`, `AgentEvent`, `HarnessError`.

### Un identificador opaco nuevo

Siguiendo el mismo patrón que CH-00 §6 estableció para los identificadores fundamentales y que
CH-02/CH-06/CH-08/CH-09 ya repitieron cada uno para el suyo:

| Identificador (nuevo de este capítulo) | Identifica |
|---|---|
| `SessionCheckpointId` | un checkpoint concreto de una sesión, ya persistido |

### `SessionCheckpoint` — el checkpoint embebido

```pseudocode
STRUCT SessionCheckpoint
    id: SessionCheckpointId
    runId: RunId
    agentState: AgentState
    createdAt: Timestamp
END
```

`agentState` embebe una **copia inmutable** de un `AgentState` (C-003, CH-00) ya producido por una
ejecución existente — nunca una referencia mutable hacia la ejecución activa que `AgentLoop` sigue
poseyendo en exclusiva (P-08/INV-12). `runId` correlaciona este checkpoint con la ejecución concreta
que lo originó — el mismo campo que `agentState.runId` ya contiene, elevado a la superficie del
checkpoint para no obligar a nadie a mirar dentro del `AgentState` embebido solo para saber de qué
ejecución proviene. Vive embebido dentro de `SessionState`, sin contrato `C-XXX` propio — el mismo
patrón que `ContextBlock` (CH-04), `ExecutionUsage` (CH-07) o `EventFilter` (CH-09): un tipo real, con
`STRUCT` propio, que ningún capítulo registra como contrato independiente porque nunca se referencia
fuera de la estructura que lo contiene.

### `SessionState` — la historia persistida de una sesión

```pseudocode
STRUCT SessionState
    sessionId: SessionId
    runIds: List<RunId>
    latestCheckpoint: SessionCheckpoint
    parentCheckpointId: Optional<SessionCheckpointId>
    createdAt: Timestamp
    updatedAt: Timestamp
END
```

Seis campos, cada uno respondiendo a una parte exacta del alcance decidido para este capítulo:
`sessionId` identifica la sesión a la que pertenece este registro; `runIds` es la lista, en orden de
aparición, de cada `RunId` que ha contribuido a esta sesión — la respuesta literal a "¿qué
ejecuciones pertenecen a esta sesión?"; `latestCheckpoint` es el `SessionCheckpoint` más reciente —
el punto desde el cual `reconstructSessionState` (seccion 11) puede reconstruir esta sesión completa;
`parentCheckpointId` es `Optional<SessionCheckpointId>` — `NULL` en la inmensa mayoría de los casos
(continuación lineal de la propia historia), poblado únicamente cuando este `SessionState` se creó
ramificando desde el checkpoint de otra línea (seccion 11, `branchSessionFromCheckpoint`);
`createdAt`/`updatedAt` registran cuándo se creó esta sesión y cuándo se actualizó por última vez.

**Por qué el nombre es, deliberadamente, `SessionState` y no otro.** `P-08` e `INV-12` ya usan este
nombre exacto desde la primera versión de la Constitution adoptada por este libro — el mismo patrón
que `AgentRunStatus` (C-013, CH-01): un nombre que la Constitution ya cita, sin contrato registrado
todavía. Se evaluó explícitamente un nombre alternativo (`SessionRecord`, para distinguirlo con más
fuerza de `AgentState` en la prosa) y se descartó: renombrar el contrato habría dejado a `P-08`/
`INV-12` citando, por su cuenta, un nombre que ya no correspondería a ningún `STRUCT` real — exactamente
la ambigüedad que este capítulo existe para cerrar. Mantener el nombre literal es lo que permite decir,
por fin, con precisión: `AgentState` (C-003) y `SessionState` (C-020) son dos `STRUCT` distintos,
producidos y poseídos por componentes distintos (`AgentLoop` / `SessionManager`), exactamente como
`INV-12` exige.

**Unchanged / Not yet introduced**: `AgentState` (C-003) no cambia de forma — sigue siendo
exactamente el `STRUCT` de CH-00; este capítulo lo consume, nunca lo modifica. Ningún `ENUM
SessionStatus` (a diferencia de `HumanInteractionStatus`, CH-06, o `EventSubscriptionStatus`, CH-09):
la progresión de una sesión se modela mediante la cadena de checkpoints, no mediante un estado
propio (ver seccion 12). Ningún mecanismo de fusión de ramas (`merge`) — `branchSessionFromCheckpoint`
(seccion 11) solo crea una rama nueva, nunca combina dos historias existentes en una sola (ver
seccion 18).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce un contrato de
datos, registrado en `registry/contracts.yaml`:

```text
ID:                     C-020
Name:                   SessionState
Version:                v1
Introduced In:          CH-10
Current Definition:     STRUCT SessionState (ver §6)
Used By:                [CMP-010]
Modified By:            []
Constitutional Impact:  [P-08, P-23, INV-12, INV-13]
```

`C-020` es el séptimo id verdaderamente nuevo del libro (el correlativo continúa después de `C-019`,
CH-09 — ningún id quedaba reservado desde CH-01 §7, exactamente como ya ocurrió con `C-014`..`C-019`
en CH-05..CH-09). A diferencia de esos seis, sin embargo, `SessionState` no es un nombre inventado
para este capítulo: es el primer contrato del libro cuyo nombre exacto ya existía, citado por la
Constitution, antes de que este capítulo lo formalizara — el mismo caso que `AgentRunStatus` (C-013)
resolvió en CH-01 para un `ENUM` en vez de un `STRUCT`.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el décimo componente de runtime del libro:

```pseudocode
COMPONENT SessionManager
    consumes: AgentState, ExecutionContext
    produces: SessionState, AgentEvent, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Article III (sección "SessionManager"):

```text
COMPONENT: SessionManager

Responsibility:
    Persistir y actualizar la historia de una sesión mediante checkpoints construidos a partir de
    un AgentState ya producido por una ejecución existente, reconstruir un SessionState completo
    desde un checkpoint ya persistido, y crear una rama nueva de sesión a partir de un checkpoint
    existente — sin poseer el estado operativo de la ejecución en curso, sin persistir las
    solicitudes de interacción humana que HumanInteractionService ya persiste por su cuenta, sin
    decidir continuación de turno y sin distribuir eventos.

Consumes:
    C-003 AgentState, C-004 ExecutionContext

Depends on:
    (ninguno todavía — el cableado real con AgentLoop, HumanInteractionService y EventBus es
    Preview, no introducido en este capítulo; ver seccion 9)

Produces:
    C-020 SessionState, C-010 AgentEvent (SESSION_CHECKPOINT_CREATED / SESSION_RECONSTRUCTED /
    SESSION_BRANCHED / SESSION_PERSISTENCE_FAILED), C-011 HarnessError

Owns (Article III, cita literal):
    - persistencia
    - recuperación
    - branching
    - checkpoints
    - reconstrucción

Does NOT own (Article IV — declarado con el mismo peso que Owns):
    - el estado operativo de una ejecución en curso (AgentState, C-003, ya existente — producido y
      poseído en exclusiva por AgentLoop, CMP-001, ya introducido en CH-01; P-08/INV-12 exigen que
      ambos permanezcan conceptualmente independientes: SessionManager solo persiste una COPIA
      inmutable de un AgentState ya producido, nunca lo posee ni lo trata como fuente de verdad de
      la ejecución activa)
    - persistir sus propias solicitudes de interacción humana pendientes (HumanInteractionService,
      CMP-006, ya introducido en CH-06 — ya tiene esa responsabilidad acotada y propia: representar,
      persistir y resolver HumanInteractionRequest/HumanInteractionResolution; SessionManager no la
      absorbe ni la duplica)
    - decidir si otro turno de razonamiento debe ocurrir (AgentLoop, CMP-001, ya introducido en
      CH-01)
    - distribuir eventos del runtime a consumidores desacoplados (EventBus, CMP-009, ya introducido
      en CH-09 — aunque SessionManager podría, en un capítulo futuro, suscribirse como un consumidor
      más de EventBus para reconstruir historial a partir de eventos ya distribuidos; ver seccion 9)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con una
particularidad respecto a CH-01..CH-09: por primera vez, una de las exclusiones no es "esto pertenece
a otro dominio de decisión", sino "esto pertenece a otro dueño de persistencia" — la distinción entre
la persistencia general de la sesión (este capítulo) y la persistencia acotada que
`HumanInteractionService` ya construyó para su propio dominio (CH-06) es la más sutil que este libro
ha tenido que trazar sobre el verbo "persistir" hasta ahora.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
SessionManager
    consumes → AgentState, ExecutionContext
    produces → SessionState, AgentEvent, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`SessionManager` no depende hoy de ningún otro componente registrado — mismo patrón que CH-01..CH-09
ya establecieron para sus propios componentes. En prosa (nunca dentro de un bloque `pseudocode`, per
`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las relaciones futuras que un capítulo
de integración agregaría son:

| Componente futuro (relación inversa — no cableada en este capítulo) | Qué relación tendría con `SessionManager` |
|---|---|
| `AgentLoop` (ya existente, CMP-001) | invocaría `createOrUpdateSessionCheckpoint` después de cada turno, pasándole el `AgentState` que ya produce hoy (CH-01 §11) — sin que `AgentLoop` necesite cambiar qué produce, solo agregar esta llamada |
| `HumanInteractionService` (ya existente, CMP-006) | seguiría persistiendo `HumanInteractionRequest`/`HumanInteractionResolution` por su cuenta — deliberadamente **sin** delegar esa persistencia a `SessionManager` (ver seccion 8/15); la relación futura, si existe, sería que ambos historiales se correlacionen por `sessionId`, nunca que uno absorba al otro |
| `EventBus` (ya existente, CMP-009) | `SessionManager` podría registrarse como un consumidor más (`EventSubscription`, C-019) para reconstruir historial a partir de `AgentEvent` ya distribuidos, en vez de (o adicionalmente a) recibir llamadas directas como `createOrUpdateSessionCheckpoint` — una relación de consumo, nunca de dependencia formal en el sentido de `registry/components.yaml` |

`registry/components.yaml` de `CMP-001` (`AgentLoop`), `CMP-006` (`HumanInteractionService`) y
`CMP-009` (`EventBus`) **no se modifica** en este capítulo: ninguno agrega `CMP-010` a su
`dependencies`, y ninguno cambia su pseudocódigo. El pseudocódigo de la seccion 11 muestra a
`SessionManager` construyendo, actualizando, reconstruyendo y ramificando un `SessionState` a partir
de un `AgentState` de ejemplo con la forma exacta que `AgentLoop` (CH-01) ya produce — de forma
completamente autónoma, sin que `AgentLoop` cambie una sola línea para que este capítulo sea
correcto. Ese cableado real (que `AgentLoop` invoque de verdad `createOrUpdateSessionCheckpoint`
después de cada turno) es, explícitamente, trabajo de un capítulo de integración futuro (ver seccion
18/19).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[AgentLoop — produce AgentState, CH-01, conceptual] → SessionManager →
[una implementación futura que reconstruye o ramifica una sesión ya persistida]
```

**Vista 2 — Sequence**

```text
AgentState
   │ (ya producido por AgentLoop tras un turno — CH-01, conceptual, este capítulo no cablea esa
   │  llamada)
   ▼
SessionManager
   │ createOrUpdateSessionCheckpoint(existingSession, agentState, execution, agentId)
   │ ¿agentState.sessionId != execution.sessionId?
   │     sí → HarnessError (SESSION_ID_MISMATCH, VALIDATION)
   │ construye un SessionCheckpoint nuevo embebiendo agentState sin modificarlo
   │ actualiza runIds (agrega agentState.runId si todavía no estaba)
   │ persistSessionState(...) — primitiva asumida, puede fallar
   │     falla → HarnessError (SESSION_PERSISTENCE_FAILED, PERSISTENCE) + AgentEvent
   │     éxito → AgentEvent (SESSION_CHECKPOINT_CREATED)
   ▼
SessionState (persistido)
   │
   │ ... tiempo después, o tras un reinicio ...
   ▼
SessionManager
   │ reconstructSessionState(checkpoint, runIds, execution, agentId)
   │ ¿checkpoint == NULL? → HarnessError (CHECKPOINT_REQUIRED_FOR_RECONSTRUCTION, VALIDATION)
   │ reconstruye un SessionState completo, exclusivamente desde el checkpoint ya persistido
   │ emite: AgentEvent (SESSION_RECONSTRUCTED)
   ▼
SessionState (reconstruido — INV-13)
```

**Vista 3 — Pseudocódigo**

Ver §11: `createOrUpdateSessionCheckpoint`, `reconstructSessionState` y
`branchSessionFromCheckpoint` son la primera formalización ejecutable de "`SessionManager` persiste,
recupera, hace checkpoint, reconstruye y ramifica la historia de una sesión" — construidas
exclusivamente a partir de material que ya existe (`AgentState` desde CH-00, `ExecutionContext` desde
CH-00) más los tipos nuevos de este capítulo.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde
CH-00/CH-01.

```pseudocode
FUNCTION createOrUpdateSessionCheckpoint(
    existingSession: Optional<SessionState>,
    agentState: AgentState,
    execution: ExecutionContext,
    agentId: AgentId
) -> SessionState

    IF agentState.sessionId != execution.sessionId
        mismatch: HarnessError = HarnessError(
            category = VALIDATION,
            code = "SESSION_ID_MISMATCH",
            message = "createOrUpdateSessionCheckpoint recibió un AgentState cuyo sessionId no coincide con el de la ExecutionContext recibida",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW mismatch
    END

    newCheckpoint: SessionCheckpoint = SessionCheckpoint(
        id = newSessionCheckpointId(),
        runId = agentState.runId,
        agentState = agentState,
        createdAt = now()
    )

    updatedRunIds: List<RunId> = []
    sessionCreatedAt: Timestamp = now()

    IF existingSession == NULL
        updatedRunIds.append(agentState.runId)
    ELSE
        alreadyIncluded: Boolean = FALSE
        FOR EACH existingRunId IN existingSession.runIds
            updatedRunIds.append(existingRunId)
            IF existingRunId == agentState.runId
                alreadyIncluded = TRUE
            END
        END
        IF NOT alreadyIncluded
            updatedRunIds.append(agentState.runId)
        END
        sessionCreatedAt = existingSession.createdAt
    END

    sessionState: SessionState = SessionState(
        sessionId = execution.sessionId,
        runIds = updatedRunIds,
        latestCheckpoint = newCheckpoint,
        parentCheckpointId = NULL,
        createdAt = sessionCreatedAt,
        updatedAt = now()
    )

    persisted: Boolean = persistSessionState(sessionState)

    IF NOT persisted
        failure: HarnessError = HarnessError(
            category = PERSISTENCE,
            code = "SESSION_PERSISTENCE_FAILED",
            message = "SessionManager no pudo persistir el SessionState con su nuevo checkpoint",
            recoverable = TRUE,
            retryable = TRUE,
            metadata = {}
        )

        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = SESSION_PERSISTENCE_FAILED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = failure
        )

        THROW failure
    END

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = SESSION_CHECKPOINT_CREATED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = sessionState
    )

    RETURN sessionState
END
```

```pseudocode
FUNCTION reconstructSessionState(
    checkpoint: SessionCheckpoint,
    runIds: List<RunId>,
    execution: ExecutionContext,
    agentId: AgentId
) -> SessionState

    IF checkpoint == NULL
        failure: HarnessError = HarnessError(
            category = VALIDATION,
            code = "CHECKPOINT_REQUIRED_FOR_RECONSTRUCTION",
            message = "reconstructSessionState fue invocada sin un SessionCheckpoint desde el cual reconstruir",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW failure
    END

    reconstructed: SessionState = SessionState(
        sessionId = checkpoint.agentState.sessionId,
        runIds = runIds,
        latestCheckpoint = checkpoint,
        parentCheckpointId = NULL,
        createdAt = checkpoint.createdAt,
        updatedAt = now()
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = SESSION_RECONSTRUCTED,
        timestamp = now(),
        runId = checkpoint.runId,
        sessionId = reconstructed.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = reconstructed
    )

    RETURN reconstructed
END
```

```pseudocode
FUNCTION branchSessionFromCheckpoint(
    sourceCheckpoint: SessionCheckpoint,
    newSessionId: SessionId,
    execution: ExecutionContext,
    agentId: AgentId
) -> SessionState

    IF sourceCheckpoint == NULL
        failure: HarnessError = HarnessError(
            category = VALIDATION,
            code = "CHECKPOINT_REQUIRED_FOR_BRANCHING",
            message = "branchSessionFromCheckpoint fue invocada sin un SessionCheckpoint desde el cual ramificar",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW failure
    END

    branchedRunIds: List<RunId> = []
    branchedRunIds.append(sourceCheckpoint.runId)

    branched: SessionState = SessionState(
        sessionId = newSessionId,
        runIds = branchedRunIds,
        latestCheckpoint = sourceCheckpoint,
        parentCheckpointId = sourceCheckpoint.id,
        createdAt = now(),
        updatedAt = now()
    )

    persisted: Boolean = persistSessionState(branched)

    IF NOT persisted
        failure: HarnessError = HarnessError(
            category = PERSISTENCE,
            code = "SESSION_PERSISTENCE_FAILED",
            message = "SessionManager no pudo persistir el SessionState ramificado a partir del checkpoint recibido",
            recoverable = TRUE,
            retryable = TRUE,
            metadata = {}
        )

        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = SESSION_PERSISTENCE_FAILED,
            timestamp = now(),
            runId = sourceCheckpoint.runId,
            sessionId = newSessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = failure
        )

        THROW failure
    END

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = SESSION_BRANCHED,
        timestamp = now(),
        runId = sourceCheckpoint.runId,
        sessionId = newSessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = branched
    )

    RETURN branched
END
```

`newEventId()` y `now()` son las mismas primitivas de CH-00..CH-09. `newSessionCheckpointId()` es
nueva, en el mismo espíritu que `newHumanInteractionRequestId()` (CH-06) o
`newEventSubscriptionId()` (CH-09). `persistSessionState(sessionState: SessionState) -> Boolean` es
la primitiva asumida más importante de este capítulo: a diferencia de
`persistHumanInteractionRequest`/`persistHumanInteractionResolution` (CH-06) o de cualquier primitiva
de persistencia anterior en el libro — todas documentadas explícitamente como "en este incremento, no
fallan" — `persistSessionState` **sí puede fallar**, y su fallo es, precisamente, lo que este capítulo
usa para ejercitar por primera vez `ErrorCategory.PERSISTENCE` (seccion 13). Modelar su detalle real
(qué motor de almacenamiento, qué garantías de durabilidad) queda, deliberadamente, fuera de alcance
(ver seccion 18) — la misma restricción que ya aplicó `deliver(...)` en CH-09 para el transporte real
hacia un consumidor desacoplado.

Nótese lo que ninguna de las tres funciones hace: ninguna muta el `AgentState` o el
`SessionCheckpoint` que recibe — `createOrUpdateSessionCheckpoint` construye siempre un
`SessionCheckpoint` y un `SessionState` nuevos, nunca modifica `existingSession` in-place, el mismo
patrón que `AgentLoop.runTurn` (CH-01) o `resolveHumanInteractionRequest` (CH-06) ya establecieron
para construir su siguiente estado; ninguna decide si otro turno debe ocurrir (`AgentLoop`, ya
resuelto); ninguna persiste ni interpreta una `HumanInteractionRequest`/`HumanInteractionResolution`
(`HumanInteractionService`, ya resuelto, CH-06); y ninguna distribuye el `AgentEvent` que emite hacia
ningún consumidor concreto (`EventBus`, ya resuelto, CH-09) — cada una se limita, estrictamente, a lo
que su propio `owns` declara.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013): esa máquina de estados sigue siendo
propiedad exclusiva de `AgentLoop` (CH-01 §12), y su tabla de transiciones no cambia aquí.

A diferencia de `HumanInteractionStatus` (CH-06) o `EventSubscriptionStatus` (CH-09), este capítulo
**no** introduce un `ENUM` de estados propio para `SessionState` — una sesión no tiene, en este
incremento, un lifecycle de valores discretos (`PENDING`/`RESOLVED`, `ACTIVE`/`CANCELLED`). En su
lugar, la progresión de una sesión se modela como una cadena de checkpoints enlazados:

```text
(createOrUpdateSessionCheckpoint, existingSession = NULL)
   → SessionState con latestCheckpoint = checkpoint₁, parentCheckpointId = NULL

(createOrUpdateSessionCheckpoint, existingSession = SessionState anterior)
   → SessionState con latestCheckpoint = checkpoint₂, parentCheckpointId = NULL
     (continuación lineal — runIds acumula, createdAt se conserva del original)

(reconstructSessionState, checkpoint = checkpointₙ ya persistido)
   → SessionState reconstruido con latestCheckpoint = checkpointₙ
     (rehidratación — INV-13, no escribe nada nuevo)

(branchSessionFromCheckpoint, sourceCheckpoint = checkpointₖ, cualquier k)
   → SessionState nuevo con sessionId distinto, latestCheckpoint = checkpointₖ,
     parentCheckpointId = checkpointₖ.id
     (ramificación — un nuevo linaje que desciende explícitamente de checkpointₖ)
```

**Lo que este capítulo explícitamente no cierra**: ninguna operación de fusión (`merge`) que combine
dos ramas en una sola línea de nuevo — `branchSessionFromCheckpoint` es, deliberadamente, de una sola
dirección (crea, nunca combina). Tampoco existe ningún mecanismo de expiración o archivado de una
sesión antigua (que hubiera requerido, precisamente, el `ENUM SessionStatus` que este capítulo decide
no introducir).

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6) clasifica también los fallos que introduce este capítulo,
fiel a los `Failure Examples` de `constitution/ARCHITECTURE_CONSTITUTION.md` Article VII:

```text
VALIDATION
    SESSION_ID_MISMATCH                     — createOrUpdateSessionCheckpoint invocada con un
                                                AgentState cuyo sessionId no coincide con el de la
                                                ExecutionContext recibida
        → recoverable: FALSE, retryable: FALSE
    CHECKPOINT_REQUIRED_FOR_RECONSTRUCTION   — reconstructSessionState invocada con checkpoint == NULL
        → recoverable: FALSE, retryable: FALSE
    CHECKPOINT_REQUIRED_FOR_BRANCHING        — branchSessionFromCheckpoint invocada con
                                                sourceCheckpoint == NULL
        → recoverable: FALSE, retryable: FALSE

PERSISTENCE
    SESSION_PERSISTENCE_FAILED               — persistSessionState devolvió FALSE al intentar
                                                persistir un SessionState nuevo o actualizado
                                                (createOrUpdateSessionCheckpoint o
                                                branchSessionFromCheckpoint)
        → recoverable: TRUE, retryable: TRUE
```

Este es el primer fallo real del libro clasificado bajo `category = PERSISTENCE` — un valor declarado
desde `ErrorCategory` (CH-00 §6) que ningún componente había ejercitado hasta este capítulo: CH-06 y
CH-09 documentaron, cada uno por su cuenta, que esa semántica real pertenecía a `SessionManager`,
todavía sin construir. `recoverable = TRUE` y `retryable = TRUE` porque un fallo al persistir es, por
naturaleza, del mismo tipo que "HTTP 503 → transient/retryable" (Article VII, Failure Examples): la
misma operación, reintentada contra el mismo almacén, puede tener éxito la siguiente vez — a
diferencia de los tres fallos de `VALIDATION`, que son violaciones de precondición del llamador y
nunca se resuelven reintentando la misma llamada con los mismos argumentos.

`createOrUpdateSessionCheckpoint`/`reconstructSessionState`/`branchSessionFromCheckpoint` nunca
devuelven una excepción cruda ni un `SessionState` a medias cuando algo falla: siempre construyen un
`HarnessError` con `category`, `recoverable` y `retryable` explícitos — mismo patrón que cada función
anterior del libro.

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo de `category = INFRASTRUCTURE`
o `FATAL` que pudiera ocurrir en una implementación real de `persistSessionState` (por ejemplo, un
almacén completamente inalcanzable, no solo temporalmente indisponible) — ambos valores de
`ErrorCategory` siguen, después de este capítulo, sin que ningún componente real los haya ejercitado
nunca.

## 14. Eventos Producidos (Events Produced)

Este capítulo agrega cuatro valores a `AgentEventType` — los primeros que observan la persistencia,
reconstrucción y ramificación de una sesión, no la ejecución de un turno, una tool call, una
invocación de modelo, una decisión de policy o una interacción humana:

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

`AgentEvent` (C-010) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — solo el rango de
valores permitido para `eventType` crece, igual que en cada capítulo anterior salvo `EventBus`
(CH-09, que no agregó ninguno).

**Por qué cuatro valores, y por qué uno de ellos es un evento de fallo real (a diferencia de
`HumanInteractionService`, CH-06, cuyos tres fallos nunca emitían nada).** Este capítulo tiene tres
operaciones reales (`createOrUpdateSessionCheckpoint`, `reconstructSessionState`,
`branchSessionFromCheckpoint`), cada una con su propio evento de éxito — mismo argumento que
`HumanInteractionService` ya estableció en CH-06 para sus dos operaciones reales. Pero, a diferencia
de los fallos de `HumanInteractionService` (violaciones de precondición del llamador, que nunca
llegaron a ejecutar nada digno de observarse), el fallo de `persistSessionState` ocurre **después**
de que `createOrUpdateSessionCheckpoint`/`branchSessionFromCheckpoint` ya construyeron un
`SessionState` completo y válido — el mismo tipo de fallo "de infraestructura, no de precondición"
que `CAPABILITY_RESOLUTION_FAILED` (CH-08) o `CONTEXT_SNAPSHOT_FAILED` (CH-04) ya modelaron. Por
eso, y solo para ese caso, este capítulo sí emite un evento de fallo (`SESSION_PERSISTENCE_FAILED`,
compartido entre las dos operaciones que pueden sufrirlo) — mientras que
`SESSION_ID_MISMATCH`/`CHECKPOINT_REQUIRED_FOR_RECONSTRUCTION`/`CHECKPOINT_REQUIRED_FOR_BRANCHING`,
violaciones de precondición, nunca emiten nada antes de su `THROW` (mismo patrón que
`TURN_ON_TERMINAL_STATE` en CH-01).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

`SessionManager` nunca decide autorización (`P-13` sigue siendo exclusivo de `PolicyEngine`, CH-05):
`createOrUpdateSessionCheckpoint` persiste cualquier `AgentState` que reciba, sin evaluar si esa
ejecución estaba autorizada a existir — esa decisión ya se tomó, aguas arriba, en los componentes que
la produjeron.

**La frontera con `HumanInteractionService` (CH-06), de nuevo.** Este es el límite más delicado de
este capítulo, y merece repetirse con precisión: `HumanInteractionService` ya persiste, por su
cuenta, `HumanInteractionRequest`/`HumanInteractionResolution` mediante primitivas
(`persistHumanInteractionRequest`/`persistHumanInteractionResolution`) que su propio capítulo marcó
explícitamente como "la persistencia real de fondo, todavía sin construir, pertenece a
`SessionManager`". Con `SessionManager` ya construido, es tentador leer esa nota como una instrucción
para que este capítulo absorba, ahora sí, esa persistencia. **Este capítulo no lo hace, deliberadamente**:
`HumanInteractionRequest`/`HumanInteractionResolution` siguen siendo, después de este capítulo,
responsabilidad exclusiva y acotada de `HumanInteractionService` (su propio `owns`, CH-06 §8, no
cambia). Lo que la nota de CH-06 en realidad señalaba es más modesto: que el **mecanismo real** detrás
de esas dos primitivas asumidas (qué almacén, qué garantías de durabilidad) podría, algún día,
compartir la misma infraestructura de bajo nivel que usa `persistSessionState` — nunca que
`SessionManager` deba poseer, leer o interpretar el contenido de una `HumanInteractionRequest`. Fundir
ambas responsabilidades en un único componente sería exactamente el error que Article IV (Ownership
Rule) prohíbe: dos dominios de persistencia con dueños, formas y reglas de acceso distintas,
colapsados "porque los dos, técnicamente, escriben algo a un almacén".

**La frontera con `AgentState`/`AgentLoop` (P-08/INV-12), de nuevo.** `SessionCheckpoint.agentState`
es una copia — no una referencia compartida ni un puntero al mismo objeto que `AgentLoop` sigue
mutando turno a turno. Ninguna función de este capítulo escribe de vuelta hacia `AgentLoop`, y ninguna
trata el `AgentState` embebido en un checkpoint como si describiera el presente operativo de una
ejecución: describe, únicamente, cómo se veía esa ejecución en el momento exacto en que el checkpoint
se creó. Si `SessionManager` alguna vez tratara esa copia como la fuente de verdad de la ejecución
activa — por ejemplo, dejando que un componente futuro leyera `SessionCheckpoint.agentState.status`
en vez de consultar a `AgentLoop` para saber si un run sigue corriendo — `INV-12` dejaría de
preservarse en la práctica, aunque el `STRUCT` siguiera siendo, formalmente, el mismo.

**Lo que este capítulo NO implementa todavía.** La gobernanza de datos sobre lo que persiste
(clasificación, residencia, retención, *legal hold* — `P-22`, Amendment v1.1, "Enterprise data is
governed throughout its lifecycle") no se modela en este capítulo: `persistSessionState` es una
primitiva asumida sin ninguna de esas garantías. Tampoco se modela ningún control de acceso sobre
quién puede reconstruir o ramificar la sesión de otro agente — `reconstructSessionState`/
`branchSessionFromCheckpoint` aceptan cualquier `SessionCheckpoint` que reciban, sin verificar que
quien invoca tenga autorización sobre esa sesión. Esto es una limitación real, documentada aquí y en
la seccion 18, no un descuido silencioso.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST CreateOrUpdateSessionCheckpointNeverMutatesTheAgentStateItReceives
TEST CreateOrUpdateSessionCheckpointRejectsAnAgentStateFromADifferentSession
TEST CreateOrUpdateSessionCheckpointAppendsANewRunIdWithoutDuplicating
TEST ReconstructSessionStateNeverRequiresALiveProcessBeyondThePersistedCheckpoint
TEST ReconstructSessionStateRejectsANullCheckpoint
TEST BranchSessionFromCheckpointAlwaysRecordsAParentCheckpointId
TEST BranchSessionFromCheckpointNeverMutatesTheSourceCheckpoint
TEST SessionPersistenceFailureIsRecoverableAndRetryable
TEST SessionManagerNeverTreatsAnEmbeddedAgentStateAsTheActiveRunsSourceOfTruth
TEST SessionManagerNeverPersistsAHumanInteractionRequestOrResolution
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.1, después de CH-10)

Constitution
 ├── Article III  — Component Sovereignty (SessionManager: décimo componente instanciado; de los
 │                   once nombres que Article III enumera, solo AgentCore sigue preview)
 ├── Article IV   — Decision Ownership (SessionManager responde, por primera vez con código real,
 │                   "What execution history and checkpoints persist?")
 └── Article VII  — Failure Constitution (ErrorCategory.PERSISTENCE ejercitado por primera vez)

Contracts (registry/contracts.yaml)
 ├── C-001 AgentMessage                (CH-00)
 ├── C-002 AgentConfig                 (CH-00)
 ├── C-003 AgentState                  (CH-00 — consumido ahora también por CMP-010)
 ├── C-004 ExecutionContext            (CH-00 — consumido ahora también por CMP-010)
 ├── C-005 ContextSnapshot             (CH-04)
 ├── C-006 ModelRequest                (CH-03)
 ├── C-007 ModelResponse               (CH-03)
 ├── C-008 ToolCall                    (CH-02)
 ├── C-009 ToolResult                  (CH-02)
 ├── C-010 AgentEvent                  (CH-00 — producido ahora también por CMP-010)
 ├── C-011 HarnessError                (CH-00 — producido ahora también por CMP-010)
 ├── C-012 ExecutionBudget             (CH-00)
 ├── C-013 AgentRunStatus              (CH-01)
 ├── C-014 PolicyDecision              (CH-05)
 ├── C-015 HumanInteractionRequest     (CH-06)
 ├── C-016 HumanInteractionResolution  (CH-06)
 ├── C-017 ExecutionDecision           (CH-07)
 ├── C-018 CapabilityDescriptor        (CH-08)
 ├── C-019 EventSubscription           (CH-09)
 └── C-020 SessionState                (CH-10, nuevo — cierra el nombre que P-08/INV-12 ya usaban)

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
 └── CMP-010 SessionManager             (CH-10, nuevo — décimo componente, solo AgentCore sigue
                                          preview de los once nombres de Article III)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado real `AgentLoop → SessionManager`**: `AgentLoop.runTurn` (CH-01 §11) no invoca
  `createOrUpdateSessionCheckpoint` en ningún punto — `AgentLoop.dependencies` no agrega `CMP-010`, y
  `registry/components.yaml` de `CMP-001` no se modifica en este capítulo.
- **La migración real de `HumanInteractionService`**: `persistHumanInteractionRequest`/
  `persistHumanInteractionResolution` (CH-06 §11) siguen siendo primitivas asumidas — no se
  reescribieron para invocar ningún mecanismo de `SessionManager`, precisamente porque su
  persistencia sigue siendo un dominio separado (ver seccion 15).
- **La suscripción real a `EventBus`**: `SessionManager` no se registra, en este capítulo, como una
  `EventSubscription` real — la relación de la seccion 9 es, deliberadamente, solo prosa.
- **Mecanismo real de fusión de ramas (`merge`)**: `branchSessionFromCheckpoint` solo crea, nunca
  combina dos historias existentes en una — ver seccion 12.
- **`ENUM SessionStatus`, expiración o archivado de una sesión**: no modelado (ver seccion 6/12) —
  una v2 futura de este contrato podría agregarlo, declarándolo explícitamente en
  `modifies_contracts` del capítulo que lo haga.
- **Autorización sobre quién puede reconstruir o ramificar la sesión de otro agente**: señalado
  explícitamente en la seccion 15 como un límite de seguridad real, no silenciado.
- **Gobernanza de datos sobre lo persistido** (`P-22`: clasificación, residencia, retención, *legal
  hold*): fuera de alcance de BH-v0.1.
- **Mecanismo real de almacenamiento detrás de `persistSessionState`**: primitiva asumida, sin
  modelar qué motor concreto la implementa ni sus garantías de durabilidad.
- **`AgentCore`**: de los once nombres de Article III, es, después de este capítulo, el único que
  sigue siendo únicamente una palabra en la tabla de preview.
- Reviewers plurales, evals y orquestación multi-agente: explícitamente fuera de alcance de BH-v0.1
  (igual que todos los capítulos anteriores).

## 19. Siguiente Incremento (Next Increment)

El problema natural del próximo capítulo: con diez componentes reales ya existentes y, por fin, un
mecanismo real de persistencia, reconstrucción y branching de sesión, de los once nombres que Article
III enumera en su árbol de "Agent Runtime" solo queda uno sin componente propio: `AgentCore` — "las
primitives fundamentales que coordinan todo lo demás", que Article III describe explícitamente como
lo que "no debe absorber responsabilidades de UI, persistencia específica, proveedores o business
integrations". Alternativamente, con los diez componentes de dominio ya resueltos cada uno por
separado, el capítulo de integración de punta a punta que CH-02..CH-09 fueron posponiendo, capítulo a
capítulo, en sus propias secciones 18 — cablear de verdad `AgentLoop → ContextEngine → ModelGateway →
CapabilityRegistry → PolicyEngine → ToolRuntime → HumanInteractionService → SessionManager →
EventBus` como un único flujo operante — es, también, un candidato real para el próximo incremento.

`next_chapter` queda en `null` en el frontmatter de este capítulo porque, en este momento del libro,
ese próximo capítulo todavía no existe como archivo — solo como el problema que motivaría su
escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg / Bucles
> de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows), secciones
> que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): después de nueve capítulos reales, `AgentState` tiene
   contrato desde la primera página del libro, pero la historia persistente de una sesión — que la
   misma Constitution nombra por su propio nombre, `SessionState`, desde `P-08`/`INV-12` — nunca
   llegó a tener uno.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): un componente puede
   nombrarse en la Constitution desde su primera versión adoptada y seguir siendo, capítulo tras
   capítulo, solo una nota al pie en el `does_not_own`/seccion 9/18 de cada componente vecino, cada
   uno resolviendo su propia persistencia acotada mientras la persistencia general de la sesión sigue
   sin dueño.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `SessionManager` (CMP-010) con una ficha que declara tanto lo que posee (`owns`: persistencia,
   recuperación, branching, checkpoints, reconstrucción) como lo que explícitamente NO posee
   (`does_not_own`, con la frontera con `HumanInteractionService` como la más sutil) y formaliza
   `SessionState` (C-020), el nombre que `P-08`/`INV-12` ya usaban sin contrato desde CH-00.
4. **Modelos mentales** (= §4, Constitutional Impact): `P-08` ("Agent state and session state are
   different concerns") junto con `INV-12`/`INV-13` — el estado operativo de una ejecución y la
   historia persistente de una sesión son responsabilidades distintas, y una ejecución durable debe
   poder reconstruirse desde estado ya persistido, no desde la memoria de un proceso que sobrevivió
   por casualidad.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un componente nuevo se introduce sin declarar
  explícitamente su `does_not_own`, aumenta la probabilidad de que absorba silenciosamente la próxima
  decisión vecina "porque ya estaba ahí" — el mismo bucle que CH-01..CH-09 ya cortaron. Este capítulo
  lo repite para `SessionManager`, con una variante: la tentación no viene de una decisión vecina, sino
  de que este componente literalmente sostiene una copia completa de un `AgentState` real dentro de
  cada checkpoint que persiste.
- **Bucle de equilibrio (estabiliza):** `createOrUpdateSessionCheckpoint` (§11) nunca muta el
  `AgentState` que recibe ni lo trata como la fuente de verdad de la ejecución en curso — solo lo
  embebe, sin tocarlo, dentro de un `SessionCheckpoint` nuevo, mientras `AgentLoop` sigue siendo, sin
  ningún cambio, el único dueño real del estado operativo de esa ejecución.

**Punto de apalancamiendo**

La decisión con mayor efecto de este capítulo es que `SessionState` (C-020) registre
`parentCheckpointId` como un campo `Optional` — casi siempre `NULL` — en vez de que cada ramificación
de una sesión sobrescribiera en silencio el registro anterior. Si esa referencia de linaje se
omitiera, ninguna implementación futura podría distinguir, después del hecho, si una sesión continuó
linealmente su propia historia o si, en algún punto, se bifurcó desde el checkpoint de otra.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo de
> esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set` (frontmatter) y
> es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa, para lectura directa
> del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. `AgentState` (CH-00) representa el estado operativo de una única ejecución en curso, y varias
   ejecuciones pueden ocurrir, una tras otra, dentro de la misma sesión a lo largo del tiempo. ¿Quién
   persiste, recupera y reconstruye la historia que abarca esas múltiples ejecuciones, y qué le
   permitiría, después de un reinicio, reconstruirse desde lo que ya persistió? *(cierra la pregunta
   guía 1)*
2. Un invariante declara, desde la primera versión de la Constitution, que el estado operativo de una
   ejecución y la historia persistente de una sesión son conceptualmente independientes. ¿Qué forma
   debería tener el contrato que representa esa historia, y qué necesitaría contener para permitir
   una reconstrucción real? *(cierra la pregunta guía 2)*
3. Si una sesión durable pudiera retomar su historia desde más de un punto anterior, ¿qué información
   tendría que persistir para que ese linaje quedara explícito? *(cierra la pregunta guía 3)*
4. Un componente ya persiste sus propias solicitudes de interacción humana como una responsabilidad
   acotada, señalando que la persistencia real de fondo pertenecía a otro componente todavía sin
   construir. ¿Ese otro componente debería absorber esa responsabilidad ya acotada, o mantenerla
   separada? *(cierra la pregunta guía 4)*

### Explicar

1. `SessionManager` posee persistir, recuperar, hacer checkpoint y reconstruir la historia de una
   sesión. Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee el estado
   operativo de una ejecución en curso — ¿qué se rompería si tratara la copia de un `AgentState` que
   guarda dentro de un checkpoint como si fuera la ejecución activa?
2. `SessionState.parentCheckpointId` es `Optional` y casi siempre `NULL`. Explica por qué modelar la
   ramificación como un campo opcional de referencia es preferible a un campo obligatorio o a una
   lista completa de sesiones derivadas.

### Conectar

1. `AgentLoop` (CH-01) produce un `AgentState` nuevo después de cada turno. ¿Qué campo de ese
   `AgentState` lee `SessionManager` para poblar `SessionCheckpoint.runId`, y por qué embeber una
   copia completa de ese `AgentState` no viola `INV-12`?
2. `HumanInteractionService` (CH-06) ya persiste, por su cuenta, sus propias solicitudes y
   resoluciones. ¿Qué campo de la ficha de `SessionManager` confirma que esa persistencia sigue
   siendo de `HumanInteractionService`, y qué se perdería si `SessionManager` la absorbiera?

### Espaciar

Las cinco tarjetas de repaso de este capítulo (dos sobre `SessionManager` — su `owns` y su
`does_not_own` —, y tres sobre `SessionState` — sus campos, por qué este capítulo ejercita por
primera vez `ErrorCategory.PERSISTENCE`, y por qué `parentCheckpointId` es opcional) entran hoy en
`reviewStage = DAY_1`. Repásalas de nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) — ver
el apéndice de tarjetas al final del libro (edición PDF) o `retrieval_set.flashcards` en
`dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te equivocaste,
ese es precisamente el punto ciego que este método existe para revelar.
