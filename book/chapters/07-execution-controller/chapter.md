---
id: CH-07
title: "ExecutionController y los Límites Operacionales de una Ejecución"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-007]
introduces_contracts: [C-017]
modifies_contracts: []
constitutional_articles: [P-10, INV-08, INV-09, INV-10, INV-18, INV-19, INV-20]
previous_chapter: CH-06
next_chapter: CH-08
retrieval_set:
  expected_outcome:
    id: EO-CH07
    text: |
      Al terminar este capítulo podrás distinguir, dentro de la pregunta "¿puede esta ejecución
      seguir?", qué tramo le pertenece en exclusiva al componente que aplica los límites
      operacionales de un `AgentRun` y qué tramo le pertenece a un dominio distinto (la
      continuación cognitiva de un ciclo de razonamiento, la ejecución de una tool call, la
      autorización de una acción, la invocación del modelo) — y podrás diseñar, para cualquier
      evaluación de continuación operacional, un resultado de tres estados que distinga detenerse
      por presupuesto agotado de detenerse por cancelación explícita, en vez de colapsar ambos
      casos en un simple booleano "sí, puede seguir" / "no, no puede seguir".
  skeleton:
    id: SK-CH07
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
    components_to_be_introduced: [CMP-007]
    contracts_to_be_introduced: [C-017]
  guiding_questions:
    - id: GQ-CH07-01
      text: |
        Cuando un ciclo de razonamiento decide que otro turno debe ocurrir, ¿qué necesita
        comprobarse todavía antes de que ese turno realmente arranque — y por qué esa comprobación
        no debería vivir en el mismo lugar que decide si el modelo debe seguir razonando?
      answered_by: RQ-CH07-01
    - id: GQ-CH07-02
      text: |
        Si un run ya consumió cierto número de tool calls, tokens y costo real, pero el único
        contador que el estado de la ejecución trackea es el turno actual, ¿de dónde debería salir
        el resto de esa información para poder compararla contra un límite operacional?
      answered_by: RQ-CH07-02
    - id: GQ-CH07-03
      text: |
        ¿Alcanza con un simple sí/no para representar "esta ejecución puede seguir"? ¿Qué se
        perdería si detenerse porque un presupuesto se agotó y detenerse porque alguien canceló la
        ejecución explícitamente se representaran exactamente de la misma forma?
      answered_by: RQ-CH07-03
    - id: GQ-CH07-04
      text: |
        De los estados finales que una ejecución puede alcanzar, hay al menos tres que la
        Constitution declaró desde el principio del libro pero que ningún capítulo, hasta ahora, ha
        producido realmente en código — ¿qué mecanismo, apenas nombrado en un artículo sobre
        presupuestos pero nunca construido, sería el primero en producirlos de verdad?
      answered_by: RQ-CH07-04
  systems_lens:
    iceberg_visible_fact: |
      `ExecutionBudget` (C-012) existe desde el capítulo piloto del libro — siete límites
      explícitos, citado por nombre en `AgentConfig` y en `ExecutionContext` desde CH-00 — y sin
      embargo, después de seis capítulos reales, ningún componente lo ha verificado jamás en
      código real, salvo una única función huérfana (`governTurnContinuation`, CH-00 §11) que
      revisa un solo campo (`maxTurns`) y que ningún componente ha reclamado como propio (ver
      seccion 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite, ahora aplicado a los límites operacionales, es que sin un
      componente con fronteras explícitas la pregunta "¿puede esta ejecución seguir?" tiende a
      confundirse con una pregunta vecina pero distinta — "¿debe ocurrir otro turno de
      razonamiento?" — porque ambas se sienten como la misma decisión de continuar, aunque Article
      IV las asigna a dueños distintos; y sin un resultado de tres estados, detenerse por
      presupuesto agotado y detenerse por cancelación explícita terminan representados con el
      mismo booleano, perdiendo la distinción que Article IX y `INV-10` exigen (ver seccion 3, Por
      Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala el séptimo componente real del libro, `ExecutionController`
      (CMP-007), con una ficha que declara tanto lo que posee (`owns`: budgets, cancellation,
      deadlines, runtime limits, operational continuation — cita literal de Article III) como lo
      que explícitamente NO posee (`does_not_own`: decidir si otro turno de razonamiento cognitivo
      debe ocurrir, ejecutar tools, evaluar policy, invocar al modelo) — y formaliza
      `ExecutionDecision` (C-017), un resultado de tres estados (`CONTINUE`/`STOP`/`CANCELLED`)
      que embebe, como `ExecutionUsage`, el uso actual contra las seis dimensiones de
      `ExecutionBudget` que `AgentState` nunca trackeó (ver seccion 8, Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es la Budget Rule de Article IX ("el modelo
      nunca es la única autoridad para determinar cuándo debe detenerse una ejecución") junto con
      la distinción constitucional entre "¿debe ocurrir otro turno?" (`AgentLoop`, Article IV) y
      "¿puede el run continuar operacionalmente?" (`ExecutionController`, Article IV) — dos
      preguntas que suenan casi idénticas en prosa informal pero que la Constitution separa en dos
      filas distintas de la misma tabla (ver seccion 4, Impacto Constitucional).
    reinforcing_loop: |
      Cada vez que un componente nuevo se introduce sin declarar explícitamente su `does_not_own`,
      aumenta la probabilidad de que absorba silenciosamente la próxima decisión vecina "porque ya
      estaba ahí" — el mismo bucle que CH-01..CH-06 ya cortaron. Este capítulo lo repite para
      `ExecutionController`, con una particularidad nueva: la tentación más fuerte no viene de un
      componente vecino, sino de la propia semejanza superficial entre "¿debe?" (`AgentLoop`) y
      "¿puede?" (`ExecutionController`) — dos preguntas que un lector apresurado podría fusionar en
      una sola, exactamente lo que Article IV prohíbe.
    balancing_loop: |
      `evaluateExecutionContinuation` (seccion 11) es el mecanismo de equilibrio: revisa la
      cancelación explícita y cada dimensión de `ExecutionBudget` en el orden fijo que Article IX
      declara, y en cuanto una sola de ellas se excede, detiene la evaluación con `outcome = STOP`
      o `CANCELLED` — nunca continúa "por si acaso" ni delega esa decisión a ninguna señal que el
      modelo produzca.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `ExecutionDecision.outcome`
      (`ExecutionOutcome`, C-017) sea un `ENUM` de tres valores (`CONTINUE`/`STOP`/`CANCELLED`) en
      vez de un `Boolean`, combinado con que `ExecutionController` (CMP-007) nunca decida por su
      cuenta si otro turno de razonamiento cognitivo debe ocurrir. Si esta autorización colapsara a
      un booleano, o si `ExecutionController` empezara a transicionar `AgentRunStatus`
      directamente, el próximo capítulo que cablee esta relación con `AgentLoop` heredaría un
      componente incapaz de distinguir "se acabó el presupuesto" de "alguien canceló", o que ya
      habría invadido una decisión que Article IV asigna a otro dueño.
  recall_questions:
    - id: RQ-CH07-01
      text: |
        ¿Qué componente evalúa si un `AgentRun` puede continuar operacionalmente, y en qué se
        diferencia esa pregunta de si `AgentLoop` debe iniciar otro turno de razonamiento?
    - id: RQ-CH07-02
      text: |
        ¿Qué `STRUCT` nuevo de este capítulo representa el uso actual de un run contra las
        dimensiones de `ExecutionBudget` que `AgentState` no trackea, y por qué ese uso no se
        agregó directamente como campos nuevos de `AgentState`?
    - id: RQ-CH07-03
      text: |
        ¿Cuáles son los tres valores posibles de `ExecutionOutcome`, y por qué `CANCELLED` es un
        valor distinto de `STOP` en vez de tratarse como una razón más dentro de
        `ExecutionStopReason`?
    - id: RQ-CH07-04
      text: |
        ¿Qué tres valores de `AgentRunStatus` — declarados desde CH-01/Article V pero nunca
        producidos por ningún pseudocódigo hasta ahora — se vuelven alcanzables, en prosa y sin que
        `AgentLoop` cambie una sola línea, gracias a la `ExecutionDecision` de este capítulo?
  explain_prompts:
    - id: EP-CH07-01
      text: |
        `ExecutionController` posee budgets, cancellation, deadlines, runtime limits y operational
        continuation. Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee
        decidir si otro turno de razonamiento cognitivo debe ocurrir, aunque las dos preguntas
        ("¿debe seguir?" y "¿puede seguir?") suenen casi idénticas — ¿qué se rompería, en concreto,
        si `ExecutionController` empezara a transicionar `AgentRunStatus` directamente en vez de
        solo informar que un límite se excedió?
      target_entity: CMP-007
    - id: EP-CH07-02
      text: |
        `ExecutionDecision.stopReason` y `ExecutionDecision.reason` solo se pueblan cuando
        `outcome != CONTINUE`, y `stopReason` en particular nunca se puebla cuando
        `outcome = CANCELLED`. Explica por qué un `CONTINUE` no necesita ninguna razón, y por qué
        una cancelación explícita no reutiliza ninguno de los valores de `ExecutionStopReason` —
        ¿qué perderíamos si forzáramos la cancelación a parecer una razón de presupuesto más?
      target_entity: C-017
  interleaved_questions:
    - id: IQ-CH07-01
      text: |
        `AgentLoop` (CH-01) declaró desde su primer capítulo, en su propio `does_not_own`, que la
        operational continuation (budget/cancelación) no le pertenece — y `runTurn` (CH-01 §11)
        nunca verifica `execution.budget` antes de decidir la transición de un turno. ¿Qué campo de
        `AgentState` necesitaría leer quien evalúe si un run puede continuar operacionalmente para
        saber cuántos turnos ya consumió, y por qué ese campo por sí solo no basta para evaluar las
        otras seis dimensiones de `ExecutionBudget`?
      current_chapter_entities: [CMP-007, C-017]
      prior_chapter_entities: [CMP-001, C-003]
      prior_chapter: CH-01
    - id: IQ-CH07-02
      text: |
        `ExecutionBudget` (C-012, CH-00) declaró siete límites explícitos desde el capítulo piloto
        del libro, y `governTurnContinuation` (CH-00 §11) llegó a verificar uno solo de ellos
        (`maxTurns`) sin pertenecer a ningún componente registrado. ¿Qué mecanismo de este capítulo
        generaliza, a las otras seis dimensiones de `ExecutionBudget`, la comprobación que esa
        función huérfana solo hacía para turnos?
      current_chapter_entities: [CMP-007, C-017]
      prior_chapter_entities: [C-012]
      prior_chapter: CH-00
  flashcards:
    - id: FC-CH07-01
      front: |
        ¿Qué posee `ExecutionController` (Article III / Article IV), en una frase?
      back: |
        Budgets, cancellation, deadlines, runtime limits y operational continuation — cita literal
        de Article III, sección "ExecutionController": decidir si un `AgentRun` PUEDE continuar
        operacionalmente, nunca si DEBE continuar cognitivamente.
      source_entity: CMP-007
      chapter_introduced_in: CH-07
      review_stage: DAY_1
    - id: FC-CH07-02
      front: |
        ¿Qué NO posee `ExecutionController`, y a qué componentes pertenecen esas decisiones?
      back: |
        Decidir si otro turno de razonamiento cognitivo debe ocurrir (`AgentLoop`, ya existente —
        distinción constitucional literal entre "debe" y "puede"), ejecutar tools/side effects
        (`ToolRuntime`, ya existente), evaluar policy/autorización (`PolicyEngine`, ya existente) e
        invocar al modelo (`ModelGateway`, ya existente).
      source_entity: CMP-007
      chapter_introduced_in: CH-07
      review_stage: DAY_1
    - id: FC-CH07-03
      front: |
        ¿Qué campos tiene `ExecutionDecision` (C-017), y qué representan?
      back: |
        `runId` (RunId, qué run se evaluó), `outcome` (ExecutionOutcome —
        CONTINUE/STOP/CANCELLED), `stopReason` (Optional<ExecutionStopReason>, poblado solo cuando
        outcome = STOP), `reason` (Optional<HarnessError>, categoría BUDGET o CANCELLATION, poblado
        cuando outcome != CONTINUE), `usage` (ExecutionUsage, el uso actual embebido) y
        `evaluatedAt` (Timestamp).
      source_entity: C-017
      chapter_introduced_in: CH-07
      review_stage: DAY_1
    - id: FC-CH07-04
      front: |
        ¿Por qué `ExecutionOutcome` tiene tres valores en vez de un `Boolean`?
      back: |
        Un `Boolean` solo puede representar "puede seguir" / "no puede seguir" — no puede
        distinguir por qué se detuvo. `STOP` (presupuesto agotado) y `CANCELLED` (cancelación
        explícita) son causas distintas que exigen manejo distinto después (por ejemplo, hacia qué
        `AgentRunStatus` terminal apuntarían) — el mismo argumento que ya motivó `PolicyOutcome`
        (CH-05) y `HumanInteractionOutcome` (CH-06).
      source_entity: C-017
      chapter_introduced_in: CH-07
      review_stage: DAY_1
    - id: FC-CH07-05
      front: |
        ¿Qué es `ExecutionUsage`, y por qué no se agregó como campos nuevos de `AgentState` (C-003)?
      back: |
        Un `STRUCT` embebido dentro de `ExecutionDecision` (sin contrato `C-XXX` propio, mismo
        patrón que `RawToolCallProposal` en CH-03) que representa cuánto ha consumido un run de las
        seis dimensiones de `ExecutionBudget` que `AgentState.currentTurn` no cubre (tool calls,
        tokens de entrada/salida, costo, runtime transcurrido, concurrencia). No se agregó a
        `AgentState` porque este capítulo no modifica contratos de capítulos anteriores — mismo
        precedente que CH-02..CH-06 ya establecieron.
      source_entity: C-017
      chapter_introduced_in: CH-07
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH07-01
      recall_question: RQ-CH07-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH07-02
      recall_question: RQ-CH07-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH07-03
      recall_question: RQ-CH07-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH07-04
      recall_question: RQ-CH07-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 7 — ExecutionController y los Límites Operacionales de una Ejecución

> **Regla constitucional (Article IX, Budget Rule):** el modelo nunca es la única autoridad para
> determinar cuándo debe detenerse una ejecución.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de saber
> cómo se llama el componente de este capítulo. El detalle estructurado de esta sección vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, dentro de la pregunta "¿puede
esta ejecución seguir?", qué tramo le pertenece en exclusiva al componente que este capítulo
introduce y qué tramo le pertenece a un dominio distinto (la continuación cognitiva de un ciclo de
razonamiento, la ejecución de una tool call, la autorización de una acción, la invocación del
modelo) — y podrás diseñar, para cualquier evaluación de continuación operacional, un resultado de
tres estados que distinga detenerse por presupuesto agotado de detenerse por cancelación explícita,
en vez de colapsar ambos casos en un simple booleano "sí, puede seguir" / "no, no puede seguir".

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e
introduce un contrato de datos (`ExecutionDecision`) y el séptimo componente de runtime del libro
(`ExecutionController`) — todavía sin explicarlos, solo como mapa.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar
atrás; están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este
capítulo va a definir):

1. Cuando un ciclo de razonamiento decide que otro turno debe ocurrir, ¿qué necesita comprobarse
   todavía antes de que ese turno realmente arranque — y por qué esa comprobación no debería vivir
   en el mismo lugar que decide si el modelo debe seguir razonando?
2. Si un run ya consumió cierto número de tool calls, tokens y costo real, pero el único contador
   que el estado de la ejecución trackea es el turno actual, ¿de dónde debería salir el resto de
   esa información para poder compararla contra un límite operacional?
3. ¿Alcanza con un simple sí/no para representar "esta ejecución puede seguir"? ¿Qué se perdería si
   detenerse porque un presupuesto se agotó y detenerse porque alguien canceló la ejecución
   explícitamente se representaran exactamente de la misma forma?
4. De los estados finales que una ejecución puede alcanzar, hay al menos tres que la Constitution
   declaró desde el principio del libro pero que ningún capítulo, hasta ahora, ha producido
   realmente en código — ¿qué mecanismo, apenas nombrado en un artículo sobre presupuestos pero
   nunca construido, sería el primero en producirlos de verdad?

## 1. Arquitectura Actual (Current Architecture)

CH-00 dejó instalado `ExecutionBudget` (C-012): siete límites explícitos (`maxTurns`,
`maxToolCalls`, `maxInputTokens`, `maxOutputTokens`, `maxCost`, `maxRuntimeMs`,
`maxConcurrentTools`), referenciado desde `AgentConfig` (C-002) y desde `ExecutionContext` (C-004)
desde la primera versión del libro. CH-00 también dejó una única función ejecutable,
`governTurnContinuation` (CH-00 §11), que compara `state.currentTurn` contra `budget.maxTurns` y
lanza un `HarnessError` de categoría `BUDGET` cuando se excede — pero esa función nunca perteneció a
ningún componente: CH-01 §3/§18 lo señaló explícitamente ("`governTurnContinuation` sigue siendo
código sin dueño") y decidió, con la misma disciplina, no asignársela a `AgentLoop` (CMP-001) por no
violar Article IV.

Desde entonces, cada componente nuevo repitió la misma exclusión en su propio `does_not_own`:
`AgentLoop` (CH-01) excluyó explícitamente "operational continuation (budgets/cancelación/
deadlines — Article IV asigna esta decisión a `ExecutionController`, preview)"; `ToolRuntime`
(CH-02) excluyó "enforcement de `ExecutionBudget`"; `PolicyEngine` (CH-05) excluyó "enforcement de
`ExecutionBudget`" en su propia ficha. Tres capítulos, de forma independiente, señalaron el mismo
nombre — `ExecutionController` — sin que ese componente existiera todavía en
`registry/components.yaml`. En total, `ExecutionController` aparece citado por nombre, como preview
o como exclusión explícita, **veintiuna veces** a lo largo de CH-00..CH-06.

`AgentState` (C-003, CH-00) declara un único contador operativo: `currentTurn: Integer`. Ningún
contrato del libro, hasta este capítulo, trackea cuántas tool calls, tokens, costo o milisegundos de
runtime ha consumido un run — los seis límites restantes de `ExecutionBudget` existen desde CH-00
sin que ningún dato del propio libro registre el uso actual contra ellos.

`AgentRunStatus` (C-013, CH-01) declara once estados, incluyendo tres terminales distintos de
`COMPLETED`: `FAILED`, `CANCELLED` y `EXPIRED`. Ninguno de los tres ha sido, hasta ahora, el destino
de una transición que algún pseudocódigo de este libro produzca realmente — `runTurn` (CH-01 §11)
solo transiciona hacia `WAITING_FOR_MODEL`, `WAITING_FOR_TOOL` y `COMPLETED`, y ningún otro
componente construido hasta CH-06 produce ninguno de esos tres valores.

`ErrorCategory` (C-011, CH-00) declara, desde su primera versión, los valores `BUDGET` y
`CANCELLATION` — pero ningún componente los ha ejercitado en la práctica todavía: `governTurnContinuation`
construye un `HarnessError` con `category = BUDGET`, pero, al no pertenecer a ningún componente
registrado, ese uso queda fuera del alcance de lo que este libro reconoce como "producido por un
componente real" (misma distinción que CH-05 aplicó a `POLICY` y CH-06 a `HUMAN_INTERACTION`).

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas, "¿puede esta ejecución seguir?" tiende a confundirse con
una pregunta vecina pero distinta: "¿debe ocurrir otro turno de razonamiento?" (`AgentLoop`, ya
resuelta desde CH-01). Ambas preguntas suenan, en prosa informal, casi idénticas — las dos hablan de
"continuar" — pero Article IV las asigna a dos filas distintas de la misma tabla: `AgentLoop`
decide si el ciclo cognitivo debe seguir razonando; `ExecutionController` decide si la ejecución
puede seguir existiendo frente a sus límites operacionales. Confundirlas dejaría a `AgentLoop`
absorbiendo silenciosamente budgets y cancelación — exactamente lo que su propio `does_not_own`
(CH-01) ya se negó a hacer — o dejaría a `ExecutionController`, cuando exista, decidiendo si el
modelo debería seguir razonando, invadiendo un dominio que no le pertenece.

Un segundo problema, más concreto: `ExecutionBudget` (CH-00) tiene siete dimensiones, pero
`AgentState` solo trackea una (`currentTurn`). Sin un lugar donde represente cuánto se ha consumido
de las otras seis (tool calls, tokens de entrada, tokens de salida, costo, runtime transcurrido,
concurrencia de tools en vuelo), ningún componente puede compararlas honestamente contra sus
límites — la comprobación se quedaría, para siempre, tan incompleta como
`governTurnContinuation` (CH-00), que solo llegó a verificar `maxTurns`.

Un tercer problema, ya familiar desde CH-05/CH-06: un resultado binario ("puede seguir" / "no puede
seguir") no puede representar dos causas de detención con consecuencias distintas — un presupuesto
agotado (una condición que el propio run generó, turno a turno) y una cancelación explícita (una
señal externa, ajena al consumo de presupuesto). Forzar ambas hacia la misma casilla perdería
exactamente la distinción que `INV-10` ("todo `AgentRun` debe poder cancelarse") exige mantener
separada de `INV-09` ("todo `AgentRun` tiene límites explícitos").

Necesitamos que "¿puede esta ejecución seguir operacionalmente?" tenga un dueño único y nombrado —
distinto del dueño de "¿debe ocurrir otro turno?" — que produzca un resultado de tres estados, no
dos; que registre el uso actual contra el que evaluó, ya que ningún contrato existente lo trackea; y
que, por fin, le dé cumplimiento real a los siete límites de `ExecutionBudget` que este libro
declaró desde su primer capítulo.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los dieciséis contratos y los seis componentes que existen hasta este punto no bastan porque:

- `governTurnContinuation` (CH-00) sigue siendo código sin dueño, y sigue verificando una sola
  dimensión (`maxTurns`) de las siete que `ExecutionBudget` declara — nunca se generalizó a
  `maxToolCalls`/`maxInputTokens`/`maxOutputTokens`/`maxCost`/`maxRuntimeMs`/`maxConcurrentTools`
  porque ningún componente reclamó esa responsabilidad;
- `AgentLoop` (CH-01), `ToolRuntime` (CH-02) y `PolicyEngine` (CH-05) declararon, cada uno por su
  cuenta y en momentos distintos, que "enforcement de `ExecutionBudget`" no les pertenece — tres
  exclusiones consistentes, pero sin que ningún componente real las recogiera todavía;
- `AgentState` (C-003) no trackea seis de las siete dimensiones de `ExecutionBudget` — sin ese
  dato, ninguna evaluación honesta de continuación operacional es posible, más allá de contar
  turnos;
- `AgentRunStatus.FAILED`/`CANCELLED`/`EXPIRED` (C-013, CH-01) siguen siendo estados declarados sin
  ninguna transición real que los alcance — la Constitution los anticipó desde Article V, pero
  ningún componente construido hasta ahora produce la señal que los justificaría;
- `ErrorCategory.BUDGET`/`CANCELLATION` (CH-00) siguen siendo valores declarados sin que ningún
  componente registrado los haya ejercitado en la práctica — la única vez que `BUDGET` se usó
  (`governTurnContinuation`) fue antes de que existiera ningún componente al que atribuírselo;
- nada impide que, sin un resultado de tres estados, "detenerse por presupuesto" y "detenerse por
  cancelación explícita" se traten como el mismo evento, perdiendo la distinción que `INV-09` e
  `INV-10` exigen mantener separada.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la
> secuencia `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una
> entidad que no haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT`
> registrado — **no magic entities**. Este capítulo aplica la misma disciplina de *ownership* que
> CH-01..CH-06 ya establecieron — con una particularidad nueva: la tentación más fuerte que este
> capítulo debe cortar no es que `ExecutionController` invada a un componente vecino ya construido,
> sino que se fusione, en la cabeza de quien lo diseñe, con `AgentLoop` — porque "¿debe continuar?"
> y "¿puede continuar?" se sienten como la misma pregunta hasta que se leen, literalmente, como dos
> filas distintas de la tabla de Article IV.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-10   The harness owns execution state—not the model.
           Primera vez que la mitad "límites operacionales" de este principio tiene un componente
           real que la ejecuta: hasta este capítulo, INV-09 estaba preservado solo porque
           ExecutionBudget existía como dato — nadie lo hacía cumplir en código real, salvo la
           función huérfana de CH-00 que verificaba una sola dimensión.

Invariants preserved
    INV-08   El harness es propietario del execution state.
             ExecutionController es, junto con AgentLoop, el segundo componente cuya única razón
             de existir es que el harness — nunca el modelo — decida cuándo una ejecución debe
             detenerse.
    INV-09   Todo AgentRun tiene límites explícitos.
             Primera cita literal posible de este invariante con enforcement real: las siete
             dimensiones de ExecutionBudget (CH-00) se comparan, por primera vez, contra un uso
             actual (ExecutionUsage, seccion 6) dentro de una función real.
    INV-10   Todo AgentRun debe poder cancelarse.
             Primera cita literal posible de este invariante: ExecutionDecision.outcome = CANCELLED
             es la primera señal real del libro que representa una cancelación explícita, distinta
             de agotar un presupuesto.
    INV-18   Toda acción significativa produce un evento observable.
             evaluateExecutionContinuation (seccion 11) emite un AgentEvent (EXECUTION_EVALUATED)
             en cada evaluación — el séptimo componente del libro que produce eventos en la
             práctica.
    INV-19   Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy
             relevante.
             ExecutionDecision.usage dentro de la propia decisión es, literalmente, la evidencia
             trazable de contra qué se evaluó la ejecución — sin ella, "se agotó el presupuesto"
             sería una afirmación no auditable.
    INV-20   Todo error operacional pertenece a una categoría conocida.
             Este capítulo es la primera vez que ErrorCategory.BUDGET y ErrorCategory.CANCELLATION
             (declarados desde CH-00, nunca ejercitados por ningún componente registrado) se
             materializan en la práctica dentro de ExecutionDecision.reason.

Component ownership changes
    CMP-007 ExecutionController se introduce — registry/components.yaml pasa de 6 a 7
    componentes. owns/does_not_own citados literalmente contra Article III (sección
    "ExecutionController") y Article IV. registry/components.yaml de CMP-001 AgentLoop, CMP-002
    ToolRuntime y CMP-005 PolicyEngine NO se modifica: las tres exclusiones ya quedaron
    declaradas desde sus propios capítulos; este capítulo solo introduce, por fin, el componente
    al que apuntaban.

Lifecycle changes
    Ninguno sobre AgentRunStatus (C-013): esa máquina de estados sigue siendo propiedad exclusiva
    de AgentLoop (CH-01), y su tabla de transiciones no cambia aquí — este capítulo no le agrega
    ninguna transición nueva al ENUM ni a la tabla de CH-01 §12. Sí documenta, en prosa (seccion
    12), hacia qué AgentRunStatus terminal apuntaría cada ExecutionDecision una vez que un
    capítulo de integración futuro cablee esa consulta dentro de AgentLoop.

Security implications
    Este es el primer capítulo que materializa Article IX completo como código ejecutable. Ver
    seccion 15 para el análisis completo, incluyendo por qué evaluateExecutionContinuation nunca
    depende de ninguna señal que el modelo produzca.

Observability implications
    ExecutionController es el séptimo componente que emite AgentEvent en la práctica, extendiendo
    AgentEventType con UN solo valor nuevo (EXECUTION_EVALUATED) — mismo patrón que PolicyEngine
    (CH-05): evaluar continuación operacional siempre produce un resultado válido (CONTINUE, STOP
    o CANCELLED), nunca una falla operacional de la evaluación en sí misma.

Deterministic vs agentic boundary
    Article XII se refina una séptima vez a nivel de componente: ExecutionController, igual que
    PolicyEngine, no recibe ninguna entrada que el modelo haya producido — ni siquiera de forma
    indirecta. Evalúa exclusivamente AgentState, ExecutionContext, ExecutionBudget y
    ExecutionUsage, los cuatro ya resueltos determinísticamente por capítulos anteriores o por
    este mismo capítulo.
```

## 5. Conceptos Nuevos (New Concepts)

- **Operational Continuation**: la pregunta "¿puede el run continuar operacionalmente?" (Article
  IV) — distinta de la continuación cognitiva que `AgentLoop` posee ("¿debe ocurrir otro turno de
  razonamiento?"). Mira los límites de `ExecutionBudget` y la cancelación explícita, nunca si el
  modelo terminó de razonar. Responsabilidad exclusiva de `ExecutionController` (Article III,
  Article IV: "`ExecutionController` → May the run continue operationally?").
- **Execution Usage**: el uso actual de un `AgentRun` contra las seis dimensiones de
  `ExecutionBudget` que `AgentState` no trackea (`currentTurn` es la única que sí). Modelado como
  `ExecutionUsage`, un `STRUCT` embebido dentro de `ExecutionDecision`, sin contrato `C-XXX`
  propio — el mismo patrón que `RawToolCallProposal` (CH-03) o `ContextBlock` (CH-04): un tipo
  real, con campos propios, que ningún capítulo registra como contrato independiente.
- **Default Stop (Fail-Safe de Ejecución)** *(extensión del principio Default Deny de CH-05,
  aplicado aquí a límites en vez de a autorización)*: la regla de diseño por la cual
  `evaluateExecutionContinuation` (seccion 11) detiene la ejecución (`outcome = STOP` o
  `CANCELLED`) en cuanto cualquier dimensión de `ExecutionBudget` se excede o se solicitó
  cancelación explícita — nunca permite continuar "por si acaso" ni delega esa decisión a ninguna
  señal que el modelo produzca (Article IX, Budget Rule).
- **Deadline** *(cita literal de Article III, sección "ExecutionController")*: el límite de tiempo
  transcurrido (`maxRuntimeMs`) contra el que se evalúa `usage.runtimeMsElapsed` — la única
  dimensión de `ExecutionBudget` cuya naturaleza es temporal en vez de un conteo discreto, y la que
  este capítulo trata, en prosa (seccion 12), como la más cercana en semántica a `EXPIRED` (un
  plazo que venció) en vez de a `FAILED` (un límite discreto que se agotó).
- **Decision Ownership** *(Article IV, en uso desde CH-01, ahora aplicado a un séptimo
  componente)*: `ExecutionController` decide "¿puede el run continuar operacionalmente?";
  explícitamente NO decide "¿debe ocurrir otro turno de razonamiento?" (`AgentLoop`, ya resuelto),
  "¿cómo se ejecuta una acción ya aprobada?" (`ToolRuntime`, ya resuelto), "¿puede ocurrir esta
  acción?" (`PolicyEngine`, ya resuelto) ni "¿cómo se invoca el modelo?" (`ModelGateway`, ya
  resuelto).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados de CH-00/CH-01

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `RunId`, `Timestamp`, `AgentState`, `ExecutionContext`,
`ExecutionBudget`, `AgentEvent`, `HarnessError`.

### `AgentEventType` — extendido, sin redefinir `AgentEvent`

CH-06 extendió `AgentEventType` a trece valores. Este capítulo agrega un único valor nuevo — mismo
patrón que CH-05 (una sola operación real, no un par éxito/fallo — seccion 14 explica la razón
completa):

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
END
```

`AgentEvent` (C-010) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — solo el rango de
valores permitido para `eventType` crece, igual que en cada capítulo anterior.

### `ExecutionOutcome` — el resultado de tres estados (sin `C-XXX` propio)

```pseudocode
ENUM ExecutionOutcome
    CONTINUE
    STOP
    CANCELLED
END
```

Tres valores, deliberadamente, no dos: un `Boolean` solo puede representar "puede seguir" / "no
puede seguir", y no puede distinguir **por qué** se detuvo. `STOP` (un límite de `ExecutionBudget`
se excedió) y `CANCELLED` (una cancelación explícita, ajena al consumo de presupuesto) son causas
distintas — el mismo argumento que ya motivó `PolicyOutcome` (CH-05) y `HumanInteractionOutcome`
(CH-06). `ExecutionOutcome` vive embebido dentro de `ExecutionDecision`, sin contrato `C-XXX` propio.

### `ExecutionStopReason` — la dimensión de `ExecutionBudget` que se excedió

```pseudocode
ENUM ExecutionStopReason
    MAX_TURNS_EXCEEDED
    MAX_TOOL_CALLS_EXCEEDED
    MAX_INPUT_TOKENS_EXCEEDED
    MAX_OUTPUT_TOKENS_EXCEEDED
    MAX_COST_EXCEEDED
    MAX_RUNTIME_EXCEEDED
    MAX_CONCURRENT_TOOLS_EXCEEDED
END
```

Siete valores, uno por cada campo de `ExecutionBudget` (C-012, CH-00) — ni más, ni menos. Vive
embebido dentro de `ExecutionDecision`, poblado únicamente cuando `outcome = STOP`: una cancelación
(`outcome = CANCELLED`) nunca reutiliza uno de estos siete valores, porque cancelar explícitamente
no es agotar ninguna dimensión de presupuesto (seccion 13 profundiza en esta asimetría).

### `ExecutionUsage` — el uso actual, embebido (el hueco que `AgentState` no cubre)

```pseudocode
STRUCT ExecutionUsage
    toolCallsUsed: Integer
    inputTokensUsed: Integer
    outputTokensUsed: Integer
    costUsed: Number
    runtimeMsElapsed: Integer
    concurrentToolsInFlight: Integer
END
```

Seis campos, uno por cada dimensión de `ExecutionBudget` que `AgentState.currentTurn` **no** cubre
— `currentTurn` sigue siendo la única fuente de verdad para turnos consumidos (CH-00/CH-01, sin
cambios). `ExecutionUsage` vive embebido dentro de `ExecutionDecision`, sin contrato `C-XXX`
propio — el mismo patrón que `RawToolCallProposal` (CH-03, embebido dentro de `ModelResponse`) o
`ContextBlock` (CH-04, embebido dentro de `ContextSnapshot`). Este capítulo no propone ningún
mecanismo real que mantenga estos seis contadores actualizados en vivo (tool calls contadas por
`ToolRuntime`, tokens y costo reportados por `ModelGateway`, runtime medido por un reloj) —
`usage: ExecutionUsage` llega como parámetro ya resuelto a `evaluateExecutionContinuation`
(seccion 11), en el mismo espíritu que `policyRuleFound(...)` (CH-05) o `compact(...)` (CH-04):
una primitiva asumida, no una entidad arquitectónica con ficha propia (seccion 18 documenta esta
deuda explícitamente).

### `ExecutionDecision` — el resultado normalizado de evaluar continuación operacional

```pseudocode
STRUCT ExecutionDecision
    runId: RunId
    outcome: ExecutionOutcome
    stopReason: Optional<ExecutionStopReason>
    reason: Optional<HarnessError>
    usage: ExecutionUsage
    evaluatedAt: Timestamp
END
```

`runId` correlaciona esta decisión con el `AgentRun` evaluado — el mismo campo que `ExecutionContext`
(C-004) ya expone. `stopReason` reutiliza `ExecutionStopReason` y se puebla únicamente cuando
`outcome = STOP` — nunca cuando `outcome = CANCELLED` (la cancelación no es una dimensión de
presupuesto, seccion 13). `reason` reutiliza `HarnessError` (C-011, CH-00) — igual que
`PolicyDecision.reason` (CH-05), se puebla únicamente cuando la ejecución se detiene
(`outcome != CONTINUE`): categoría `BUDGET` cuando `outcome = STOP`, categoría `CANCELLATION`
cuando `outcome = CANCELLED` — la primera vez que este libro ejercita esos dos valores de
`ErrorCategory` (declarados desde CH-00) dentro de un componente real. `usage` embebe el
`ExecutionUsage` completo contra el que se evaluó — la materialización literal de `INV-19`: sin
este campo, "se agotó el presupuesto" no sería una afirmación auditable.

**Unchanged / Not yet introduced**: ningún campo nuevo en `AgentState` (C-003) ni en
`ExecutionBudget` (C-012) — ninguno de los dos se modifica en este capítulo; ningún mecanismo real
que mantenga `ExecutionUsage` actualizado en vivo; y ningún `INTERFACE ExecutionController` con
múltiples `IMPLEMENTATION` (formalizarlo como interfaz queda para cuando este libro necesite
modelar más de un mecanismo real de enforcement de presupuesto).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce un contrato de
datos, registrado en `registry/contracts.yaml`:

```text
ID:                     C-017
Name:                   ExecutionDecision
Version:                v1
Introduced In:          CH-07
Current Definition:     STRUCT ExecutionDecision (ver §6)
Used By:                [CMP-007]
Modified By:            []
Constitutional Impact:  [P-10, INV-08, INV-09, INV-10, INV-18, INV-19, INV-20]
```

`C-017` es el cuarto id de contrato que este libro asigna sin que estuviera reservado desde CH-01
§7 (`C-014`, `C-015` y `C-016` ya rompieron esa reserva en CH-05/CH-06) — el correlativo
simplemente continúa después de `C-016` (CH-06).

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el séptimo componente de runtime del libro:

```pseudocode
COMPONENT ExecutionController
    consumes: AgentState, ExecutionContext, ExecutionBudget, ExecutionUsage
    produces: ExecutionDecision, AgentEvent, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Article III (sección "ExecutionController"):

```text
COMPONENT: ExecutionController

Responsibility:
    Evaluar si un AgentRun puede continuar operacionalmente contra su ExecutionBudget — turnos,
    tool calls, tokens, costo, runtime y concurrencia — o si fue cancelado explícitamente,
    produciendo una ExecutionDecision determinística de tres resultados posibles
    (continue/stop/cancelled) con el uso actual siempre trazable — sin decidir si otro turno de
    razonamiento cognitivo debe ocurrir, sin ejecutar tools/side effects, sin evaluar policy/
    autorización y sin invocar al modelo.

Consumes:
    C-003 AgentState, C-004 ExecutionContext, C-012 ExecutionBudget

Depends on:
    (ninguno todavía — el cableado real con AgentLoop, ToolRuntime, ModelGateway y
    CapabilityRegistry es Preview, no introducido en este capítulo; ver seccion 9)

Produces:
    C-017 ExecutionDecision, C-010 AgentEvent (EXECUTION_EVALUATED), C-011 HarnessError
    (embebido en una ExecutionDecision con outcome = STOP o CANCELLED)

Owns (Article III, cita literal):
    - budgets
    - cancellation
    - deadlines
    - runtime limits
    - operational continuation

Does NOT own (Article IV — declarado con el mismo peso que Owns):
    - decidir si otro turno de razonamiento cognitivo debe ocurrir (AgentLoop, CMP-001, ya
      introducido en CH-01 — Article IV: "AgentLoop → Should another reasoning turn occur?";
      distinción constitucional literal: ExecutionController decide si la ejecución PUEDE
      continuar operacionalmente frente a sus límites, AgentLoop decide si DEBE continuar
      cognitivamente — ninguna de las dos preguntas sustituye a la otra)
    - ejecutar tools/side effects (ToolRuntime, CMP-002, ya introducido en CH-02)
    - evaluar policy/autorización de una acción (PolicyEngine, CMP-005, ya introducido en CH-05)
    - invocar al modelo seleccionado (ModelGateway, CMP-003, ya introducido en CH-03)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con una
particularidad respecto a CH-01..CH-06: la primera exclusión de esta lista no separa
`ExecutionController` de un componente cuyo dominio sea obviamente distinto (ejecutar tools,
invocar el modelo), sino de `AgentLoop`, cuya pregunta ("¿debe ocurrir otro turno?") es la más
parecida, en prosa informal, a la que este componente sí posee ("¿puede continuar?"). Esa cercanía
superficial es exactamente la que Article IV exige separar por escrito, no la que más fácilmente se
habría dejado implícita.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
ExecutionController
    consumes → AgentState, ExecutionContext, ExecutionBudget, ExecutionUsage
    produces → ExecutionDecision, AgentEvent, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`ExecutionController` no depende hoy de ningún otro componente registrado — mismo patrón que
CH-01..CH-06 ya establecieron para sus propios componentes. En prosa (nunca dentro de un bloque
`pseudocode`, per `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las relaciones
futuras que capítulos posteriores agregarán son:

| Componente futuro (Preview — no cableado en este capítulo) | Qué relación tendría con `ExecutionController` |
|---|---|
| `AgentLoop` (ya existente, CMP-001) | consultaría a `ExecutionController` **antes** de decidir si continúa cada turno (`runTurn`, CH-01 §11) — hoy `runTurn` no verifica ningún presupuesto; ese cableado es, explícitamente, trabajo de un capítulo de integración futuro |
| `ToolRuntime` (ya existente, CMP-002) | reportaría cada tool call completada hacia el mecanismo que mantiene `ExecutionUsage.toolCallsUsed`/`concurrentToolsInFlight` actualizado |
| `ModelGateway` (ya existente, CMP-003) | reportaría tokens de entrada/salida y costo hacia `ExecutionUsage.inputTokensUsed`/`outputTokensUsed`/`costUsed` |
| `SessionManager` (Article III, preview) | la persistencia real y durable de `ExecutionUsage` entre pausas y reanudaciones de un run |
| `CapabilityRegistry` (Article III, preview) | metadata real de concurrencia declarada por una capability, que hoy `ExecutionUsage.concurrentToolsInFlight` asume ya resuelta |

`registry/components.yaml` de `CMP-001` (`AgentLoop`), `CMP-002` (`ToolRuntime`) y `CMP-005`
(`PolicyEngine`) **no se modifica** en este capítulo: ninguno de los tres agrega `CMP-007` a su
`dependencies`, y ninguno cambia su pseudocódigo. El pseudocódigo de la seccion 11 muestra a
`ExecutionController` evaluando un `AgentRun` de forma completamente autónoma contra su
`ExecutionBudget` — sin que `AgentLoop` cambie una sola línea para que este capítulo sea correcto.
Ese cableado real (que `AgentLoop.runTurn` invoque realmente a `evaluateExecutionContinuation` antes
de decidir la transición de cada turno) es, explícitamente, trabajo de un capítulo de integración
futuro — el mismo patrón que CH-02, CH-03, CH-04, CH-05 y CH-06 ya establecieron para sus propias
relaciones inversas.

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[AgentLoop — CH-01, conceptual, todavía no cablea esta llamada] → ExecutionController →
[AgentLoop reanudaría o detendría el run — Preview, cableado formal de un capítulo posterior]
```

**Vista 2 — Sequence**

```text
AgentRun en curso
   │ (turno en progreso, evaluado de forma autónoma por ExecutionController — este capítulo no
   │  cablea la invocación real desde AgentLoop.runTurn)
   ▼
ExecutionController
   │ evaluateExecutionContinuation(state, execution, budget, usage, cancellationRequested)
   │ ¿state.status ya es terminal?
   │     sí → HarnessError (EXECUTION_EVALUATION_ON_TERMINAL_STATE, VALIDATION)
   │ ¿cancellationRequested?
   │     sí → outcome = CANCELLED (reason: HarnessError categoría CANCELLATION)
   │     no → ¿alguna dimensión de ExecutionBudget excedida (en el orden de Article IX)?
   │             sí → outcome = STOP (stopReason correspondiente, reason: HarnessError
   │                   categoría BUDGET)
   │             no → outcome = CONTINUE
   │ construye ExecutionDecision (runId, outcome, stopReason, reason, usage, evaluatedAt)
   │ emite: AgentEvent (EXECUTION_EVALUATED)
   ▼
ExecutionDecision
   │
   ▼
[AgentLoop consultaría esta ExecutionDecision antes de decidir la transición del siguiente turno —
Preview, cableado formal de un capítulo posterior, ver seccion 9/18]
```

**Vista 3 — Pseudocódigo**

Ver §11: `evaluateExecutionContinuation` es la primera formalización ejecutable de
"`ExecutionController` decide si un `AgentRun` puede continuar operacionalmente", construida
exclusivamente a partir de material que ya existe (`AgentState`/`ExecutionContext`/
`ExecutionBudget` desde CH-00/CH-01) más los tipos nuevos de este capítulo — sin necesitar que
`AgentLoop` cambie.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde
CH-00/CH-01.

```pseudocode
FUNCTION evaluateExecutionContinuation(
    state: AgentState,
    execution: ExecutionContext,
    budget: ExecutionBudget,
    usage: ExecutionUsage,
    cancellationRequested: Boolean
) -> ExecutionDecision

    IF state.status == COMPLETED
        OR state.status == FAILED
        OR state.status == CANCELLED
        OR state.status == EXPIRED

        error: HarnessError = HarnessError(
            category = VALIDATION,
            code = "EXECUTION_EVALUATION_ON_TERMINAL_STATE",
            message = "evaluateExecutionContinuation fue invocada sobre un AgentRunStatus terminal",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW error
    END

    outcome: ExecutionOutcome = CONTINUE
    stopReason: Optional<ExecutionStopReason> = NULL
    reason: Optional<HarnessError> = NULL

    IF cancellationRequested
        outcome = CANCELLED
        reason = HarnessError(
            category = CANCELLATION,
            code = "EXECUTION_CANCELLED",
            message = "La ejecución fue cancelada explícitamente",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    ELSE IF state.currentTurn >= budget.maxTurns
        outcome = STOP
        stopReason = MAX_TURNS_EXCEEDED
        reason = HarnessError(
            category = BUDGET,
            code = "MAX_TURNS_EXCEEDED",
            message = "Execution budget exhausted: maxTurns reached",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    ELSE IF usage.toolCallsUsed >= budget.maxToolCalls
        outcome = STOP
        stopReason = MAX_TOOL_CALLS_EXCEEDED
        reason = HarnessError(
            category = BUDGET,
            code = "MAX_TOOL_CALLS_EXCEEDED",
            message = "Execution budget exhausted: maxToolCalls reached",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    ELSE IF usage.inputTokensUsed >= budget.maxInputTokens
        outcome = STOP
        stopReason = MAX_INPUT_TOKENS_EXCEEDED
        reason = HarnessError(
            category = BUDGET,
            code = "MAX_INPUT_TOKENS_EXCEEDED",
            message = "Execution budget exhausted: maxInputTokens reached",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    ELSE IF usage.outputTokensUsed >= budget.maxOutputTokens
        outcome = STOP
        stopReason = MAX_OUTPUT_TOKENS_EXCEEDED
        reason = HarnessError(
            category = BUDGET,
            code = "MAX_OUTPUT_TOKENS_EXCEEDED",
            message = "Execution budget exhausted: maxOutputTokens reached",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    ELSE IF usage.costUsed >= budget.maxCost
        outcome = STOP
        stopReason = MAX_COST_EXCEEDED
        reason = HarnessError(
            category = BUDGET,
            code = "MAX_COST_EXCEEDED",
            message = "Execution budget exhausted: maxCost reached",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    ELSE IF usage.runtimeMsElapsed >= budget.maxRuntimeMs
        outcome = STOP
        stopReason = MAX_RUNTIME_EXCEEDED
        reason = HarnessError(
            category = BUDGET,
            code = "MAX_RUNTIME_EXCEEDED",
            message = "Execution budget exhausted: maxRuntimeMs reached",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    ELSE IF usage.concurrentToolsInFlight >= budget.maxConcurrentTools
        outcome = STOP
        stopReason = MAX_CONCURRENT_TOOLS_EXCEEDED
        reason = HarnessError(
            category = BUDGET,
            code = "MAX_CONCURRENT_TOOLS_EXCEEDED",
            message = "Execution budget exhausted: maxConcurrentTools reached",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    decision: ExecutionDecision = ExecutionDecision(
        runId = execution.runId,
        outcome = outcome,
        stopReason = stopReason,
        reason = reason,
        usage = usage,
        evaluatedAt = now()
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = EXECUTION_EVALUATED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = state.agentId,
        traceId = execution.traceId,
        payload = decision
    )

    RETURN decision
END
```

`newEventId()` y `now()` son las mismas primitivas de CH-00..CH-06. `cancellationRequested` es una
señal de entrada asumida (primitiva, en el mismo espíritu que `modelFinished`/
`modelProposesToolCall` en CH-01): este capítulo no modela de dónde viene una solicitud de
cancelación real (un usuario, un kill switch, un timeout externo) — solo que, cuando llega, se
verifica **antes** que cualquier dimensión de presupuesto.

Nótese el orden de las comprobaciones, que nunca se invierte: primero la precondición de invocación
(¿el `AgentRunStatus` ya es terminal?); luego la cancelación explícita; luego cada dimensión de
`ExecutionBudget`, en el mismo orden en que Article IX las dibuja en su diagrama (`turns? → tool
calls? → tokens? → cost? → runtime? → concurrency?`, con `tokens?` desdoblado aquí en
`maxInputTokens`/`maxOutputTokens` para precisión, mismo nivel de detalle que `ExecutionBudget`
(C-012) ya declara). Revisar la cancelación antes que el presupuesto es deliberado: una cancelación
explícita es una señal externa que debe honrarse de inmediato, sin importar cuánto presupuesto
quede todavía disponible.

Nótese también lo que `evaluateExecutionContinuation` **no** hace: no decide ningún
`AgentRunStatus` (Article IV, "`AgentLoop` → Should another reasoning turn occur?" sigue sin
respuesta aquí, y `ExecutionDecision` tampoco contiene ningún campo `AgentRunStatus` — seccion 12
documenta en prosa, no en el contrato, hacia qué estado terminal apuntaría cada resultado), no
ejecuta ninguna tool call, no invoca ningún modelo y no evalúa policy — se limita a comparar
`state`/`usage` contra `budget` y a producir la señal.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013): esa máquina de estados sigue
siendo propiedad exclusiva de `AgentLoop` (CH-01 §12), y su tabla de transiciones no cambia aquí —
`ExecutionDecision` no contiene ningún campo `AgentRunStatus`, precisamente porque decidir esa
transición no pertenece a `ExecutionController` (Article IV).

Lo que este capítulo sí documenta, en prosa — **la primera vez que este libro describe una ruta real
hacia `FAILED`, `CANCELLED` y `EXPIRED`** — es hacia qué estado terminal apuntaría cada
`ExecutionDecision`, una vez que un capítulo de integración futuro cablee la consulta real dentro de
`AgentLoop.runTurn`:

```text
ExecutionDecision.outcome = CONTINUE
   → ninguna transición terminal; el run sigue su curso normal (AgentLoop decide el resto)

ExecutionDecision.outcome = STOP, stopReason = MAX_RUNTIME_EXCEEDED
   → apuntaría a AgentRunStatus.EXPIRED
     (un plazo de tiempo venció — misma familia semántica que WAITING_FOR_HUMAN --expired-->
     EXPIRED, CH-01/CH-06: no un límite discreto que se agotó, sino un deadline que venció)

ExecutionDecision.outcome = STOP, stopReason = cualquier otro valor
   (MAX_TURNS_EXCEEDED / MAX_TOOL_CALLS_EXCEEDED / MAX_INPUT_TOKENS_EXCEEDED /
   MAX_OUTPUT_TOKENS_EXCEEDED / MAX_COST_EXCEEDED / MAX_CONCURRENT_TOOLS_EXCEEDED)
   → apuntaría a AgentRunStatus.FAILED
     (un límite discreto de recursos se agotó — una falla operacional, no un plazo que venció)

ExecutionDecision.outcome = CANCELLED
   → apuntaría a AgentRunStatus.CANCELLED
     (una señal externa explícita, ajena por completo al consumo de presupuesto)
```

Esta tabla es, deliberadamente, prosa descriptiva y no una transición que ningún pseudocódigo de
este capítulo ejecute — `AgentLoop.runTurn` (CH-01) no cambia una sola línea aquí. Es, sin embargo,
la primera vez que este libro puede describir con precisión, para `FAILED`/`CANCELLED`/`EXPIRED`,
qué produciría realmente cada uno de los tres: hasta este capítulo, los tres eran valores del
`ENUM AgentRunStatus` (C-013) declarados desde CH-01 sin que ninguna función real de este libro
apuntara hacia ellos.

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00, extendido en CH-06 con `HUMAN_INTERACTION`) clasifica también
los fallos que introduce este capítulo:

```text
VALIDATION
    evaluateExecutionContinuation invocada sobre un AgentRunStatus terminal
    → recoverable: FALSE, retryable: FALSE
    → código: EXECUTION_EVALUATION_ON_TERMINAL_STATE (ver §11)

BUDGET
    ExecutionDecision.outcome = STOP — una dimensión de ExecutionBudget se excedió
    → recoverable: FALSE, retryable: FALSE
    → código: uno de MAX_TURNS_EXCEEDED / MAX_TOOL_CALLS_EXCEEDED / MAX_INPUT_TOKENS_EXCEEDED /
      MAX_OUTPUT_TOKENS_EXCEEDED / MAX_COST_EXCEEDED / MAX_RUNTIME_EXCEEDED /
      MAX_CONCURRENT_TOOLS_EXCEEDED (ver §11) — primera vez que ErrorCategory.BUDGET (declarado
      desde CH-00) se ejercita dentro de un componente real registrado

CANCELLATION
    ExecutionDecision.outcome = CANCELLED — cancelación explícita
    → recoverable: FALSE, retryable: FALSE
    → código: EXECUTION_CANCELLED (ver §11) — primera vez que ErrorCategory.CANCELLATION
      (declarado desde CH-00) se ejercita dentro de un componente real registrado
```

`evaluateExecutionContinuation` nunca lanza un error genérico: siempre construye un `HarnessError`
con `category`, `recoverable` y `retryable` explícitos — mismo patrón que cada función de
CH-00..CH-06. A diferencia de la precondición de invocación (`VALIDATION`, que sí interrumpe la
función con `THROW`), los casos `BUDGET`/`CANCELLATION` **nunca se lanzan**: se devuelven, embebidos
en `ExecutionDecision.reason`, como parte de un resultado válido — el mismo diseño que
`PolicyDecision.reason` (CH-05) ya estableció para `outcome = DENY`. Detener una ejecución por
presupuesto o por cancelación no es, en sí mismo, una falla de invocar la función: es uno de sus
tres resultados legítimos.

## 14. Eventos Producidos (Events Produced)

Este capítulo agrega un único valor nuevo a `AgentEventType` — mismo patrón que CH-05
(`POLICY_EVALUATED`), no un par éxito/fallo como CH-02/CH-03/CH-04, ni dos valores como CH-06:

```text
EXECUTION_EVALUATED   — ExecutionController evaluó si el AgentRun puede continuar operacionalmente
                         (evaluateExecutionContinuation, §11), sin importar si el resultado fue
                         CONTINUE, STOP o CANCELLED
```

La razón es la misma que CH-05 documentó para `POLICY_EVALUATED`: a diferencia de ejecutar una tool
call, invocar un modelo o ensamblar contexto, evaluar continuación operacional nunca "falla" en el
sentido operacional — siempre produce un resultado válido de `ExecutionDecision`, incluso cuando ese
resultado es `STOP` o `CANCELLED`. El único caso que sí interrumpe la función
(`EXECUTION_EVALUATION_ON_TERMINAL_STATE`) es una violación de precondición de invocación, no un
fallo de la evaluación en sí — y, siguiendo el mismo patrón que `TURN_ON_TERMINAL_STATE` (CH-01) y
`REQUEST_ALREADY_RESOLVED` (CH-06), no emite ningún `AgentEvent` (el `THROW` interrumpe antes de
llegar al `EMIT`).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

Este capítulo materializa Article IX (Resource and Budget Constitution) completo por primera vez
como código ejecutable:

- **Budget Rule — "el modelo nunca es la única autoridad para determinar cuándo debe detenerse una
  ejecución"**: `evaluateExecutionContinuation` (§11) no recibe absolutamente ninguna entrada que el
  modelo haya producido — ni `modelFinished` ni `modelProposesToolCall` (las señales que sí lee
  `AgentLoop.runTurn`, CH-01) participan aquí. Solo compara `state`/`usage`, ya resueltos
  determinísticamente, contra `budget`.
- **`INV-09` — Todo `AgentRun` tiene límites explícitos**: las siete dimensiones de
  `ExecutionBudget` (C-012, CH-00) se comparan, por primera vez, contra un uso actual real
  (`ExecutionUsage`) dentro de una función que pertenece a un componente registrado — no solo
  declaradas como dato, sino exigidas como comportamiento.
- **`INV-10` — Todo `AgentRun` debe poder cancelarse**: `cancellationRequested` se verifica
  **antes** que cualquier dimensión de presupuesto — una cancelación explícita nunca espera a que el
  presupuesto se agote para ser honrada.
- **P-13 (por contraste, ya preservado desde CH-05)**: `ExecutionController`, igual que
  `PolicyEngine`, no depende de que el modelo se comporte bien — a diferencia de `PolicyEngine`, ni
  siquiera evalúa una entidad (`ToolCall`) cuyo contenido el modelo haya ayudado a producir.

`ExecutionController` es, de los siete componentes del libro, el segundo (junto con `PolicyEngine`)
cuya evaluación nunca "falla" en el sentido operacional — siempre produce un resultado legítimo,
incluso cuando ese resultado detiene la ejecución.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST EvaluateExecutionContinuationNeverInvokedOnATerminalAgentRunStatus
TEST EvaluateExecutionContinuationChecksCancellationBeforeAnyBudgetDimension
TEST EvaluateExecutionContinuationChecksAllSevenBudgetDimensionsInArticleIXOrder
TEST ExecutionDecisionOutcomeIsNeverABoolean
TEST StopReasonPopulatedOnlyWhenOutcomeIsStopNeverWhenCancelled
TEST ExecutionControllerNeverDecidesCognitiveTurnContinuation
TEST ExecutionControllerNeverInvokesToolRuntimeModelGatewayOrPolicyEngineDirectly
TEST ExecutionDecisionNeverContainsAnAgentRunStatusField
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.1, después de CH-07)

Constitution
 ├── Article III  — Component Sovereignty (ExecutionController: séptimo componente instanciado)
 ├── Article IV   — Decision Ownership (en uso: ExecutionController.owns/does_not_own)
 └── Article IX   — Resource and Budget Constitution (primera materialización ejecutable completa)

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
 ├── C-010 AgentEvent                  (CH-00)
 ├── C-011 HarnessError                (CH-00)
 ├── C-012 ExecutionBudget             (CH-00 — con enforcement real desde CH-07)
 ├── C-013 AgentRunStatus              (CH-01)
 ├── C-014 PolicyDecision              (CH-05)
 ├── C-015 HumanInteractionRequest     (CH-06)
 ├── C-016 HumanInteractionResolution  (CH-06)
 └── C-017 ExecutionDecision           (CH-07, nuevo)

Components (registry/components.yaml)
 ├── CMP-001 AgentLoop                 (CH-01)
 ├── CMP-002 ToolRuntime               (CH-02)
 ├── CMP-003 ModelGateway              (CH-03)
 ├── CMP-004 ContextEngine             (CH-04)
 ├── CMP-005 PolicyEngine              (CH-05)
 ├── CMP-006 HumanInteractionService   (CH-06)
 └── CMP-007 ExecutionController       (CH-07, nuevo — primer enforcement real de ExecutionBudget)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado formal `AgentLoop ↔ ExecutionController`**: `AgentLoop.runTurn` (CH-01) no invoca
  `evaluateExecutionContinuation` todavía — sigue decidiendo la transición de cada turno sin
  consultar ningún presupuesto, exactamente como CH-01 lo dejó. Ese cableado (y la decisión de qué
  hace `AgentLoop` con una `ExecutionDecision` cuyo `outcome` no sea `CONTINUE`) es, explícitamente,
  trabajo de un capítulo de integración futuro.
- **Quién mantiene `ExecutionUsage` actualizado en vivo**: ningún componente de este libro reporta
  todavía tool calls completadas, tokens consumidos, costo acumulado o milisegundos transcurridos
  hacia `ExecutionUsage` — llega como parámetro ya resuelto, una primitiva asumida (seccion 6).
- **El cableado formal `ToolRuntime → ExecutionController`**: `ToolRuntime.executeToolCall` (CH-02)
  no reporta ninguna tool call completada hacia el mecanismo que mantendría
  `usage.toolCallsUsed`/`concurrentToolsInFlight`.
- **El cableado formal `ModelGateway → ExecutionController`**: `ModelGateway` (CH-03) no reporta
  tokens ni costo hacia `usage.inputTokensUsed`/`outputTokensUsed`/`costUsed`.
- **La transición real de `AgentRunStatus` hacia `FAILED`/`CANCELLED`/`EXPIRED`**: seccion 12
  documenta, en prosa, hacia qué estado apuntaría cada `ExecutionDecision` — pero ningún
  pseudocódigo de este libro produce todavía esa transición; `AgentLoop.runTurn` no cambia.
- **`SessionManager` y la persistencia real de `ExecutionUsage` entre pausas y reanudaciones**:
  sigue siendo, como toda persistencia durable, deuda heredada sin cambios en este capítulo.
- **`CapabilityRegistry`, Provider Adapters reales, streaming real, `Channel Adapter` real,
  expiración de una `HumanInteractionRequest`**: deuda heredada de capítulos anteriores, sin
  cambios aquí.
- Reviewers plurales, evals y orquestación multi-agente: explícitamente fuera de alcance de
  BH-v0.1 (igual que todos los capítulos anteriores).

## 19. Siguiente Incremento (Next Increment)

El problema natural del próximo capítulo: con `ExecutionController` (CMP-007) evaluando de forma
autónoma si un `AgentRun` puede continuar, y con `AgentLoop` (CMP-001) todavía decidiendo cada turno
sin consultarlo, ¿quién cablea realmente la consulta — de modo que `runTurn` (CH-01) pregunte a
`ExecutionController` antes de transicionar, y que una `ExecutionDecision` con `outcome != CONTINUE`
efectivamente detenga el run en `FAILED`, `CANCELLED` o `EXPIRED` según corresponda? Ese mismo
capítulo de integración también tendría que resolver, de forma simétrica, el cableado ya pendiente
desde CH-05 (`PolicyEngine → HumanInteractionService`) y desde CH-06
(`HumanInteractionService ↔ AgentLoop`/`ToolRuntime`) — los tres cableados formales que este libro
ha ido posponiendo, capítulo a capítulo, en su propia sección 18.

`next_chapter` queda en `null` en el frontmatter de este capítulo porque, en este momento del libro,
ese capítulo de integración todavía no existe como archivo — solo como el problema que motivaría su
escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de
> la secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco
> Iceberg / Bucles de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas,
> Forrester/Meadows), secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): `ExecutionBudget` existe desde el capítulo piloto del
   libro — siete límites explícitos — y, después de seis capítulos reales, ningún componente lo ha
   verificado jamás en código real, salvo una única función huérfana que revisa un solo campo.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): sin un componente
   con fronteras explícitas, "¿puede esta ejecución seguir?" tiende a confundirse con "¿debe ocurrir
   otro turno?" — dos preguntas que Article IV asigna a dueños distintos — y sin un resultado de
   tres estados, detenerse por presupuesto agotado y detenerse por cancelación explícita terminan
   representados de la misma forma.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `ExecutionController` (CMP-007) con una ficha que declara tanto lo que posee (`owns`) como lo que
   explícitamente NO posee (`does_not_own`) y formaliza `ExecutionDecision` (C-017) — un resultado
   de tres estados que embebe, como `ExecutionUsage`, el uso actual contra las seis dimensiones de
   `ExecutionBudget` que `AgentState` nunca trackeó.
4. **Modelos mentales** (= §4, Constitutional Impact): la Budget Rule de Article IX — "el modelo
   nunca es la única autoridad para determinar cuándo debe detenerse una ejecución" — junto con la
   distinción constitucional entre "¿debe ocurrir otro turno?" y "¿puede el run continuar
   operacionalmente?".

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un componente nuevo se introduce sin declarar
  explícitamente su `does_not_own`, aumenta la probabilidad de que absorba silenciosamente la
  próxima decisión vecina "porque ya estaba ahí" — aquí, la tentación no viene de un componente
  vecino ya construido, sino de la propia semejanza superficial entre "¿debe?" y "¿puede?". Este
  capítulo corta esa espiral separando ambas preguntas por escrito, con la misma disciplina que
  CH-01..CH-06 ya aplicaron a sus propias fronteras.
- **Bucle de equilibrio (estabiliza):** `evaluateExecutionContinuation` (§11) revisa la cancelación
  y cada dimensión de `ExecutionBudget` en un orden fijo, y en cuanto una se excede, detiene la
  evaluación — nunca continúa "por si acaso" ni delega esa decisión a ninguna señal del modelo.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `ExecutionDecision.outcome`
(`ExecutionOutcome`, C-017) sea un `ENUM` de tres valores (`CONTINUE`/`STOP`/`CANCELLED`) en vez de
un `Boolean`, combinado con que `ExecutionController` (CMP-007) nunca decida por su cuenta si otro
turno de razonamiento cognitivo debe ocurrir. Si esta autorización colapsara a un booleano, o si
`ExecutionController` empezara a transicionar `AgentRunStatus` directamente, el próximo capítulo que
cablee esta relación con `AgentLoop` heredaría un componente incapaz de distinguir "se acabó el
presupuesto" de "alguien canceló", o que ya habría invadido una decisión que Article IV asigna a
otro dueño.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado
> completo de esta sección (con ids estables para cada pregunta/tarjeta) vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida. Aquí se
> presenta en prosa, para lectura directa del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Cuando un ciclo de razonamiento decide que otro turno debe ocurrir, ¿qué necesita comprobarse
   todavía antes de que ese turno realmente arranque — y por qué esa comprobación no debería vivir
   en el mismo lugar que decide si el modelo debe seguir razonando? *(cierra la pregunta guía 1)*
2. Si un run ya consumió cierto número de tool calls, tokens y costo real, pero el único contador
   que el estado de la ejecución trackea es el turno actual, ¿de dónde debería salir el resto de
   esa información para poder compararla contra un límite operacional? *(cierra la pregunta guía 2)*
3. ¿Alcanza con un simple sí/no para representar "esta ejecución puede seguir"? ¿Qué se perdería si
   detenerse porque un presupuesto se agotó y detenerse porque alguien canceló la ejecución
   explícitamente se representaran exactamente de la misma forma? *(cierra la pregunta guía 3)*
4. De los estados finales que una ejecución puede alcanzar, hay al menos tres que la Constitution
   declaró desde el principio del libro pero que ningún capítulo ha producido realmente en código —
   ¿qué mecanismo sería el primero en producirlos de verdad? *(cierra la pregunta guía 4)*

### Explicar

1. `ExecutionController` posee budgets, cancellation, deadlines, runtime limits y operational
   continuation. Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee
   decidir si otro turno de razonamiento cognitivo debe ocurrir, aunque las dos preguntas suenen
   casi idénticas — ¿qué se rompería, en concreto, si `ExecutionController` empezara a transicionar
   `AgentRunStatus` directamente?
2. `ExecutionDecision.stopReason` y `ExecutionDecision.reason` solo se pueblan cuando
   `outcome != CONTINUE`, y `stopReason` nunca se puebla cuando `outcome = CANCELLED`. Explica por
   qué una cancelación explícita no reutiliza ninguno de los valores de `ExecutionStopReason`.

### Conectar

1. `AgentLoop` (CH-01) declaró desde su primer capítulo que la operational continuation no le
   pertenece, y `runTurn` nunca verifica `execution.budget`. ¿Qué campo de `AgentState`
   necesitaría leer quien evalúe si un run puede continuar operacionalmente para saber cuántos
   turnos ya consumió, y por qué ese campo por sí solo no basta para evaluar las otras seis
   dimensiones de `ExecutionBudget`?
2. `ExecutionBudget` (C-012, CH-00) declaró siete límites desde el capítulo piloto, y
   `governTurnContinuation` (CH-00 §11) llegó a verificar uno solo de ellos. ¿Qué mecanismo de este
   capítulo generaliza esa comprobación a las otras seis dimensiones?

### Espaciar

Las cinco tarjetas de repaso de este capítulo (`ExecutionController` — su `owns` y su
`does_not_own` —, y `ExecutionDecision` — sus campos, por qué su `outcome` no es un `Boolean`, y
qué es `ExecutionUsage`) entran hoy en `reviewStage = DAY_1`. Repásalas de nuevo al día 3, al día 7
y al día 21 (curva de Ebbinghaus) — ver el apéndice de tarjetas al final del libro (edición PDF) o
`retrieval_set.flashcards` en `dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te equivocaste,
ese es precisamente el punto ciego que este método existe para revelar.
