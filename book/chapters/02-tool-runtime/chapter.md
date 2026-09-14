---
id: CH-02
title: "ToolRuntime y la Ejecución Controlada de una Tool Call"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-002]
introduces_contracts: [C-008, C-009]
modifies_contracts: []
constitutional_articles: [P-03, P-04, P-05, P-12, P-13, INV-04, INV-05, INV-06, INV-07, INV-18, INV-19, INV-20]
previous_chapter: CH-01
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH02
    text: |
      Al terminar este capítulo podrás distinguir, dentro del camino completo que atraviesa una
      acción con efectos reales, qué tramo le pertenece en exclusiva al componente que ejecuta esa
      acción y qué tramos pertenecen a dominios distintos (autorización, aprobación humana,
      presupuesto operacional, resolución de qué implementación satisface la capacidad pedida) que
      todavía no tienen componente propio — y podrás diseñar, para cualquier resultado de esa
      ejecución, una representación normalizada que no dependa de que cada implementación invente
      su propia forma de decir "esto falló" o "esto funcionó".
  skeleton:
    id: SK-CH02
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
    components_to_be_introduced: [CMP-002]
    contracts_to_be_introduced: [C-008, C-009]
  guiding_questions:
    - id: GQ-CH02-01
      text: |
        Cuando el modelo propone usar una herramienta y la ejecución queda esperando esa
        resolución (ver capítulo anterior), ¿quién decide exactamente qué implementación concreta
        satisface esa intención, y qué debe verificarse antes de permitir que la acción externa
        ocurra?
      answered_by: RQ-CH02-01
    - id: GQ-CH02-02
      text: |
        Si la intención de usar una herramienta llega con datos de entrada que no corresponden a lo
        que esa herramienta espera recibir, ¿en qué punto exacto del camino debe detectarse ese
        problema, y qué impide que la ejecución siga adelante de todos modos?
      answered_by: RQ-CH02-02
    - id: GQ-CH02-03
      text: |
        Una vez que la acción externa termina, ¿de qué forma se le comunica al resto del sistema si
        tuvo éxito o si falló, sin que cada implementación distinta invente su propia manera de
        representarlo?
      answered_by: RQ-CH02-03
    - id: GQ-CH02-04
      text: |
        ¿Por qué el mismo componente que coordina la ejecución de una acción externa no debería,
        además, decidir si esa acción estaba autorizada, si alguien humano debía aprobarla primero,
        o si el presupuesto de ejecución todavía lo permite?
      answered_by: RQ-CH02-04
  systems_lens:
    iceberg_visible_fact: |
      Sin un dueño explícito para "¿cómo se ejecuta una acción ya aprobada?", cada implementación
      termina invocando la herramienta de una manera distinta: algunas confían en que el propio
      modelo arme correctamente los argumentos; otras ejecutan la función encontrada por nombre sin
      validar nada antes; otras mezclan, en el mismo lugar donde se ejecuta la acción, la pregunta
      de si esa acción estaba permitida (ver seccion 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que, sin un componente con fronteras explícitas, la decisión de
      "cómo ejecutar una acción aprobada" tiende a absorber silenciosamente decisiones vecinas
      (autorización, aprobación humana, presupuesto, incluso qué implementación concreta responde a
      una capacidad) solo porque están físicamente cerca del punto donde ocurre la ejecución —
      exactamente lo que Article IV prohíbe. Y sin un resultado normalizado, cada componente que
      consume el resultado de una acción externa termina interpretando "éxito" y "fallo" de forma
      distinta (ver seccion 3, Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala el segundo componente real del libro, `ToolRuntime` (CMP-002), con una
      ficha que declara tanto lo que posee (`owns`: resolver capabilities, validar llamadas,
      ejecutar hooks, coordinar ejecución, devolver resultados normalizados) como lo que
      explícitamente NO posee (`does_not_own`: autorización, aprobación humana, enforcement de
      presupuesto, resolución de qué implementación satisface una capacidad) — y formaliza
      `ToolCall` (C-008) y `ToolResult` (C-009) como los dos contratos que ya citaba
      `constitution/ARCHITECTURE_CONSTITUTION.md` por nombre (INV-04, INV-05, INV-07) sin que
      ninguno de los dos existiera todavía como contrato registrado (ver seccion 8, Component
      Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior sigue siendo el Ownership Rule de Article IV,
      ahora aplicado a un segundo componente: "ningún componente debe absorber silenciosamente
      decisiones que pertenecen a otro dominio". `ToolRuntime` existe precisamente para que "¿cómo
      se ejecuta una acción aprobada?" tenga un dueño — sin que ese dueño se convierta, además, en
      el dueño de "¿está permitida esta acción?" (ver seccion 4, Impacto Constitucional).
    reinforcing_loop: |
      Cada vez que un componente nuevo se introduce sin declarar explícitamente su `does_not_own`,
      aumenta la probabilidad de que absorba silenciosamente la próxima decisión vecina "porque ya
      estaba ahí" — el mismo bucle que CH-01 ya cortó para `AgentLoop`. Este capítulo repite el
      mismo corte para `ToolRuntime`, con cuatro decisiones vecinas explícitamente declaradas fuera
      de su alcance en vez de una.
    balancing_loop: |
      `executeToolCall` (seccion 11) es el mecanismo de equilibrio: antes de coordinar cualquier
      ejecución real, rechaza con un `ToolResult` fallido — nunca con una excepción sin tipar —
      tanto una capability sin resolver como un input que no cumple el schema declarado, en vez de
      dejar que una acción mal formada llegue a ejecutarse.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `ToolRuntime` (CMP-002) declare su
      `does_not_own` con cuatro exclusiones explícitas — no solo dos, como `AgentLoop` en CH-01 —
      en el mismo momento en que se introduce, antes de que exista código real que pueda absorber
      silenciosamente la autorización, la aprobación humana, el presupuesto o la resolución de
      capacidades. Si esta frontera no se fija aquí, cada uno de los cuatro componentes futuros que
      sí poseen esas decisiones (`PolicyEngine`, `HumanInteractionService`, `ExecutionController`,
      `CapabilityRegistry`) tendría que arrancarle esa responsabilidad a `ToolRuntime` en vez de
      simplemente ocuparla.
  recall_questions:
    - id: RQ-CH02-01
      text: |
        ¿Qué contrato representa la intención ya resuelta de invocar una capacidad con un input
        dado, y qué componente es responsable exclusivo de ejecutarla según INV-05?
    - id: RQ-CH02-02
      text: |
        ¿Qué invariante exige que todo `ToolCall` se valide antes de ejecutarse (INV-04), y qué dos
        señales booleanas de la firma de `executeToolCall` modelan esa verificación en este
        capítulo?
    - id: RQ-CH02-03
      text: |
        ¿Qué contrato normaliza el resultado de ejecutar una tool call, y qué contrato ya existente
        reutiliza — sin modificarlo — para representar un fallo?
    - id: RQ-CH02-04
      text: |
        Según Article IV, ¿qué decisión posee `ToolRuntime` y qué cuatro decisiones relacionadas NO
        posee — y a qué componentes, todavía sin introducir, pertenece cada una?
  explain_prompts:
    - id: EP-CH02-01
      text: |
        `ToolRuntime` posee coordinar la ejecución de una tool call ya aprobada. Explica, como si
        hablaras con alguien sin contexto técnico, por qué NO posee la decisión de si esa acción
        estaba permitida — ¿qué se rompería, en concreto, si `ToolRuntime` empezara a decidir
        autorización directamente "ya que de todos modos es quien ejecuta la acción"?
      target_entity: CMP-002
    - id: EP-CH02-02
      text: |
        `ToolResult` reutiliza `HarnessError` (C-011, ya existente desde CH-00) para representar un
        fallo, en vez de definir un tipo de error nuevo propio de las tool calls. Explica qué
        perderíamos, en términos de auditoría y consistencia, si cada componente del libro
        definiera su propia forma de representar un fallo en vez de compartir un único contrato de
        error clasificado.
      target_entity: C-009
  interleaved_questions:
    - id: IQ-CH02-01
      text: |
        Cuando `AgentLoop.runTurn` (CH-01) transiciona una ejecución a `WAITING_FOR_TOOL` porque el
        modelo propuso `modelProposesToolCall = TRUE`, ¿qué dos campos de la señal que el modelo
        propuso necesitaría poblar quien construya el `ToolCall` correspondiente, para que
        `ToolRuntime` pueda intentar resolver la capacidad solicitada?
      current_chapter_entities: [CMP-002, C-008]
      prior_chapter_entities: [CMP-001, C-013]
      prior_chapter: CH-01
  flashcards:
    - id: FC-CH02-01
      front: |
        ¿Qué posee `ToolRuntime` (Article III / Article IV), en una frase?
      back: |
        Resolver la capability solicitada, validar el input contra su schema declarado, ejecutar
        los hooks `beforeToolCall`/`afterToolCall`, coordinar la ejecución y devolver un
        `ToolResult` normalizado.
      source_entity: CMP-002
      chapter_introduced_in: CH-02
      review_stage: DAY_1
    - id: FC-CH02-02
      front: |
        ¿Qué NO posee `ToolRuntime`, y a qué componentes (todavía sin introducir) pertenecen esas
        cuatro decisiones?
      back: |
        Autorización (`PolicyEngine`), aprobación humana (`HumanInteractionService`), enforcement
        de `ExecutionBudget` (`ExecutionController`) y resolución de qué implementación satisface
        una capability (`CapabilityRegistry`) — ninguno de los cuatro existe todavía en
        `registry/components.yaml`.
      source_entity: CMP-002
      chapter_introduced_in: CH-02
      review_stage: DAY_1
    - id: FC-CH02-03
      front: |
        ¿Qué campos tiene `ToolCall` (C-008), y qué representan?
      back: |
        `id` (ToolCallId), `capability` (CapabilityId, la capacidad ya resuelta por nombre),
        `arguments` (Map<Text, Value>, el input) y `requestedAt` (Timestamp) — la intención de
        invocar una capacidad, ya resuelta, todavía sin ejecutar.
      source_entity: C-008
      chapter_introduced_in: CH-02
      review_stage: DAY_1
    - id: FC-CH02-04
      front: |
        ¿Qué campos tiene `ToolResult` (C-009), y qué contrato reutiliza para representar un fallo?
      back: |
        `callId` (ToolCallId, correlaciona con el `ToolCall` original), `succeeded` (Boolean),
        `output` (Optional<Value>), `error` (Optional<HarnessError> — reutiliza C-011 sin
        modificarlo) y `completedAt` (Timestamp).
      source_entity: C-009
      chapter_introduced_in: CH-02
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH02-01
      recall_question: RQ-CH02-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH02-02
      recall_question: RQ-CH02-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH02-03
      recall_question: RQ-CH02-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH02-04
      recall_question: RQ-CH02-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 2 — ToolRuntime y la Ejecución Controlada de una Tool Call

> **Regla constitucional (Article VI, Execution Rule 2):** las tools se ejecutan exclusivamente
> mediante `ToolRuntime`.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de
> saber cómo se llama el componente de este capítulo. El detalle estructurado de esta sección
> vive en `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, dentro del camino completo
que atraviesa una acción con efectos reales, qué tramo le pertenece en exclusiva al componente que
este capítulo introduce y qué tramos pertenecen a dominios distintos (autorización, aprobación
humana, presupuesto operacional, resolución de qué implementación satisface la capacidad pedida)
que todavía no tienen componente propio — y podrás diseñar, para cualquier resultado de esa
ejecución, una representación normalizada que no dependa de que cada implementación invente su
propia forma de decir "esto falló" o "esto funcionó".

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e
introduce dos contratos de datos (`ToolCall`, `ToolResult` — formalizando dos nombres que la
Constitution ya usaba en INV-04/INV-05/INV-07 sin que existieran como contratos registrados) y el
segundo componente de runtime del libro (`ToolRuntime`) — todavía sin explicarlos, solo como mapa.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar
atrás; están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este
capítulo va a definir):

1. Cuando el modelo propone usar una herramienta y la ejecución queda esperando esa resolución (ver
   capítulo anterior), ¿quién decide exactamente qué implementación concreta satisface esa
   intención, y qué debe verificarse antes de permitir que la acción externa ocurra?
2. Si la intención de usar una herramienta llega con datos de entrada que no corresponden a lo que
   esa herramienta espera recibir, ¿en qué punto exacto del camino debe detectarse ese problema, y
   qué impide que la ejecución siga adelante de todos modos?
3. Una vez que la acción externa termina, ¿de qué forma se le comunica al resto del sistema si tuvo
   éxito o si falló, sin que cada implementación distinta invente su propia manera de
   representarlo?
4. ¿Por qué el mismo componente que coordina la ejecución de una acción externa no debería, además,
   decidir si esa acción estaba autorizada, si alguien humano debía aprobarla primero, o si el
   presupuesto de ejecución todavía lo permite?

## 1. Arquitectura Actual (Current Architecture)

CH-00 dejó instalados siete contratos de datos y CH-01 agregó el octavo (`AgentRunStatus`, C-013)
junto con el primer componente de runtime, `AgentLoop` (CMP-001). `AgentLoop.runTurn` (CH-01 §11)
puede transicionar una ejecución a `WAITING_FOR_TOOL` cuando el modelo propone usar una herramienta
— y ahí se detiene, a propósito: ninguna tool se ejecuta todavía, porque Article VI, Execution Rule
1 prohíbe que `AgentLoop` ejecute directamente side effects, y Execution Rule 2 exige que las tools
se ejecuten exclusivamente mediante `ToolRuntime` — un componente que, hasta este capítulo, seguía
siendo solo un nombre en la tabla de preview de `constitution/ARCHITECTURE_CONSTITUTION.md` Article
III.

`constitution/ARCHITECTURE_CONSTITUTION.md` ya nombraba, desde su versión 1.0, tres invariantes que
dependen de contratos que todavía no existían como tales: INV-04 ("Todo `ToolCall` debe validarse
antes de ejecutarse"), INV-05 ("Todo `ToolCall` pasa por `ToolRuntime`") e INV-07 ("Todo
`ToolResult` vuelve al ciclo del agente como observación explícita cuando el lifecycle continúa").
Los tres invariantes citan `ToolCall` y `ToolResult` por nombre — pero `registry/contracts.yaml`
no tenía ninguna entrada para ninguno de los dos; sus ids, `C-008` y `C-009`, seguían reservados
desde CH-01 §7.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas, la decisión "¿cómo se ejecuta una acción ya aprobada?"
no tiene un lugar fijo donde vivir. Una implementación puede invocar la función encontrada por
nombre sin validar sus argumentos contra ningún schema; otra puede mezclar, en el mismo lugar donde
ocurre la ejecución, la pregunta de si esa acción estaba permitida (una decisión de un dominio
distinto, Article IV); una tercera puede devolver el resultado de la ejecución con una forma
distinta cada vez — a veces una excepción cruda del lenguaje de programación subyacente, a veces un
texto libre, a veces `null` — de modo que nada más adelante en el sistema puede depender de una
forma estable para decidir si la ejecución continúa o se detiene.

Necesitamos que "¿cómo se ejecuta una acción ya aprobada?" tenga un dueño único y nombrado — y que
ese dueño declare, con la misma fuerza con la que declara lo que posee, las decisiones vecinas
(autorización, aprobación humana, presupuesto, resolución de capacidades) que explícitamente no
posee.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los ocho contratos y el único componente que existen hasta este punto no bastan porque:

- `AgentLoop` (CH-01) declara explícitamente, en su propio `does_not_own`, que no ejecuta tool
  calls — pero ningún componente todavía posee esa ejecución; `WAITING_FOR_TOOL` es, literalmente,
  un handoff sin resolver (CH-01 §5, §18);
- `ToolCall` y `ToolResult` siguen siendo nombres citados por INV-04/INV-05/INV-07 sin contrato
  registrado — cualquier capítulo futuro que los use "por nombre" heredaría una versión ambigua, o
  peor, cada implementación futura los definiría de forma distinta;
- nada impide que la validación de schema de un input (INV-04), la ejecución misma, y la
  autorización de esa ejecución (Article IV: `PolicyEngine` → "¿está permitida esta acción?") se
  resuelvan en el mismo lugar del código, aunque Article IV las asigna a dueños distintos;
- no existe ningún resultado normalizado que distinga, de forma consistente, "la capacidad
  solicitada no existe", "el input no cumple el schema declarado" y "la acción se ejecutó pero
  falló" — tres fallos de naturaleza distinta que Article VII exige clasificar de forma diferente.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la
> secuencia `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una
> entidad que no haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT`
> registrado — **no magic entities**. Este capítulo aplica la misma disciplina de *ownership* que
> CH-01 ya estableció: ningún componente puede reclamar en prosa una responsabilidad que su propia
> ficha no declara en `owns`.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-03   Tools are explicit capabilities, not prompt tricks.
           ToolCall/ToolResult son la primera materialización concreta de este principio: toda
           acción sobre el mundo externo se representa mediante contratos explícitos, validables
           y observables — nunca como texto libre interpretado por convención.
    P-04   Every action produces observable events.
           executeToolCall (seccion 11) emite un AgentEvent en cada resolución (éxito o fallo).
    P-05   Side effects pass through policy.
           ToolRuntime declara explícitamente que NO posee policy evaluation (does_not_own) —
           Execution Rule 3 ("las policies se evalúan antes del side effect") sigue siendo una
           regla declarada, todavía sin componente que la haga cumplir.
    P-12   Events observe; hooks intervene.
           beforeToolCall/afterToolCall son los primeros puntos de extensión reales del libro,
           modelados como los puntos definidos que P-12 exige, sin introducir todavía un registro
           de hooks propio.
    P-13   Authorization is deterministic and external to the LLM.
           ToolRuntime tampoco decide autorización — la misma frontera que P-13 exige, ahora
           respetada por un segundo componente además de AgentLoop.

Invariants preserved
    INV-04   Todo ToolCall debe validarse antes de ejecutarse.
             executeToolCall rechaza con un ToolResult fallido tanto una capability sin resolver
             como un input que no cumple el schema declarado, antes de coordinar cualquier
             ejecución real (ver seccion 11).
    INV-05   Todo ToolCall pasa por ToolRuntime.
             Primera cita literal posible de este invariante: ya existe un ToolRuntime real que es
             el único camino declarado para ejecutar una tool call (Article VI, Execution Rule 2).
    INV-06   Todo side effect pasa por PolicyEngine.
             Preservado, no reimplementado: PolicyEngine sigue sin existir (preview, ver seccion 9
             y seccion 18) — ToolRuntime deliberadamente no absorbe esta decisión.
    INV-07   Todo ToolResult vuelve al ciclo del agente como observación explícita cuando el
             lifecycle continúa.
             Declarado, todavía no ejercido: este capítulo produce un ToolResult real, pero
             conectarlo de vuelta al runTurn de AgentLoop (CH-01) — resolviendo WAITING_FOR_TOOL —
             es explícitamente el trabajo de un capítulo posterior (ver seccion 18/19).
    INV-18   Toda acción significativa produce un evento observable.
             executeToolCall emite AgentEvent (TOOL_CALL_COMPLETED / TOOL_CALL_FAILED) en cada
             resolución.
    INV-19   Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy
             relevante.
             Cada AgentEvent que emite ToolRuntime lleva el traceId de su ExecutionContext.
    INV-20   Todo error operacional pertenece a una categoría conocida.
             ToolResult.error reutiliza HarnessError (C-011, sin modificarlo) — nunca una
             excepción cruda ni un texto libre.

Component ownership changes
    CMP-002 ToolRuntime se introduce — registry/components.yaml pasa de 1 a 2 componentes. owns/
    does_not_own citados literalmente contra Article III (sección "ToolRuntime") y Article IV.

Lifecycle changes
    Ninguno sobre AgentRunStatus (C-013): este capítulo no modifica su ENUM ni su tabla de
    transiciones (propiedad de AgentLoop, CH-01). La transición WAITING_FOR_TOOL → RUNNING sigue
    marcada como Preview en CH-01 §12 — ToolRuntime ahora existe, pero conectarlo de vuelta al
    runTurn de AgentLoop es trabajo de un capítulo posterior (ver seccion 12).

Security implications
    Ninguna nueva superficie de ataque: P-05/P-13 se preservan sin enforcement real todavía.
    ToolRuntime.does_not_own excluye explícitamente autorización, aprobación humana y enforcement
    de presupuesto — el pipeline completo de Article VI (Policy Evaluation → Authorization →
    Human Approval? → Execution Budget → Sandbox) sigue sin componente que lo ejecute.

Observability implications
    ToolRuntime es el segundo componente que emite AgentEvent en la práctica, extendiendo
    AgentEventType con dos valores nuevos (TOOL_CALL_COMPLETED, TOOL_CALL_FAILED) sin modificar
    el envelope AgentEvent (C-010) ni su STRUCT.

Deterministic vs agentic boundary
    Article XII se refina de nuevo a nivel de componente: el modelo ya no participa en absoluto en
    este tramo — ToolCall llega como intención ya resuelta (Article IV, "LLM → What should I try?"
    quedó resuelto por AgentLoop en CH-01); ToolRuntime — determinístico — decide si ejecuta, y
    cómo, sin volver a consultar al modelo.
```

## 5. Conceptos Nuevos (New Concepts)

- **Capability** *(preview conceptual — Article III, `CapabilityRegistry` no introducido en este
  capítulo)*: la abstracción que desacopla la intención de una acción (nombrada en un `ToolCall`)
  de la implementación concreta que la satisface. Este capítulo trata "qué implementación satisface
  una capability" como una pregunta ya resuelta externamente (una señal booleana en el pseudocódigo
  de la seccion 11), no como un mecanismo propio.
- **Tool Call**: la intención, ya resuelta, de invocar una capability con un input concreto —
  contrato canónico `ToolCall` (C-008), citado por nombre en INV-04/INV-05 desde la primera versión
  de la Constitution, formalizado recién en este capítulo.
- **Tool Result**: el resultado normalizado de ejecutar un `ToolCall` — éxito u error, nunca una
  excepción cruda — contrato canónico `ToolResult` (C-009), citado por nombre en INV-07.
- **Extension Point** *(beforeToolCall / afterToolCall)*: los puntos definidos del ciclo de
  ejecución donde un hook puede intervenir (P-12, Article VI: "Los hooks pueden intervenir en
  puntos definidos"). Este capítulo los modela como primitivas invocables — igual que `now()` o
  `newEventId()` desde CH-00 — no como un registro de hooks con contrato propio; formalizar ese
  registro es trabajo de un capítulo posterior.
- **Schema Validation Gate**: el punto explícito, exigido por INV-04, en el que `executeToolCall`
  verifica que el input de un `ToolCall` cumple el schema que su capability declara, antes de
  coordinar cualquier ejecución real. Qué es exactamente ese schema y cómo se declara pertenece a
  `CapabilityRegistry` (preview); este capítulo solo exige que la verificación ocurra.
- **Decision Ownership** *(Article IV, en uso desde CH-01, ahora aplicado a un segundo componente)*:
  `ToolRuntime` decide "¿cómo se ejecuta una acción ya aprobada?"; explícitamente NO decide "¿está
  permitida esta acción?" (`PolicyEngine`), "¿requiere aprobación humana?" (`HumanInteractionService`),
  "¿puede el run seguir gastando presupuesto?" (`ExecutionController`) ni "¿qué implementación
  satisface esta capability?" (`CapabilityRegistry`).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores heredados del metamodelo común

`ToolCallId` y `CapabilityId` ya forman parte del metamodelo canónico desde
`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §3.1 (identificadores fundamentales disponibles
para cualquier capítulo), pero ningún capítulo anterior los había usado todavía dentro de un
`STRUCT` real. Este es el primero.

### `AgentEventType` — extendido, sin redefinir `AgentEvent`

CH-00 definió `AgentEventType` con cuatro valores (`RUN_STARTED`, `TURN_CONTINUED`,
`RUN_COMPLETED`, `RUN_FAILED`), sin contrato `C-XXX` propio (vive embebido como el tipo del campo
`eventType` de `AgentEvent`, C-010). Este capítulo agrega dos valores — los primeros eventos que
observan la ejecución de una tool call, no la continuación de un turno:

```pseudocode
ENUM AgentEventType
    RUN_STARTED
    TURN_CONTINUED
    RUN_COMPLETED
    RUN_FAILED
    TOOL_CALL_COMPLETED
    TOOL_CALL_FAILED
END
```

`AgentEvent` (C-010) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 (`eventId`,
`eventType`, `timestamp`, `runId`, `sessionId`, `agentId`, `traceId`, `payload`) — solo el rango de
valores permitido para `eventType` crece, igual que `AgentRunStatus` creció en CH-01 sin que
`AgentState` (C-003) cambiara de forma.

### `ToolCall` — la intención ya resuelta

```pseudocode
STRUCT ToolCall
    id: ToolCallId
    capability: CapabilityId
    arguments: Map<Text, Value>
    requestedAt: Timestamp
END
```

`capability` identifica la capability ya resuelta por nombre (Article IV, "LLM → What should I
try?" ya fue resuelto por `AgentLoop`/el modelo en un capítulo anterior); `ToolRuntime` no decide
qué intentar, solo qué hacer con la intención que recibe.

### `ToolResult` — el resultado normalizado

```pseudocode
STRUCT ToolResult
    callId: ToolCallId
    succeeded: Boolean
    output: Optional<Value>
    error: Optional<HarnessError>
    completedAt: Timestamp
END
```

`error` reutiliza `HarnessError` (C-011, CH-00) sin modificarlo — ningún tipo de error nuevo se
introduce para las tool calls; `ErrorCategory.TOOL` (ya definido en CH-00) es la categoría que
clasifica un fallo de ejecución (ver seccion 13).

**Unchanged / Not yet introduced**: `ContextSnapshot`, `ModelRequest` y `ModelResponse` siguen
reservados como `C-005`/`C-006`/`C-007` (CH-01 §7) — llegan junto con `ModelGateway`/`ContextEngine`
en un capítulo posterior. Tampoco se introduce ningún `STRUCT Tool` (la declaración de una
capability y su schema) ni ningún contrato para `CapabilityRegistry` — este capítulo trata "qué es
un `Tool`" y "cómo se resuelve una capability" como preview, sin definirlos como contrato propio
todavía (ver seccion 9/18).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía (formalizar `ToolRuntime`
como interfaz con implementaciones concretas, al estilo `INTERFACE ModelGateway` de
`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §7, queda para cuando este libro necesite más de
una implementación). Introduce dos contratos de datos, registrados en `registry/contracts.yaml`:

```text
ID:                     C-008
Name:                   ToolCall
Version:                v1
Introduced In:          CH-02
Current Definition:     STRUCT ToolCall (ver §6)
Used By:                [CMP-002]
Modified By:            []
Constitutional Impact:  [P-03, INV-04, INV-05]
```

```text
ID:                     C-009
Name:                   ToolResult
Version:                v1
Introduced In:          CH-02
Current Definition:     STRUCT ToolResult (ver §6)
Used By:                [CMP-002]
Modified By:            []
Constitutional Impact:  [INV-07, INV-20, P-04]
```

Con `C-008` y `C-009` ya asignados, `C-005`..`C-007` quedan como los únicos ids todavía reservados
(`ContextSnapshot`/`ModelRequest`/`ModelResponse`, ver seccion 6) — la reserva completa de cinco ids
que CH-01 §7 documentó se resuelve en dos capítulos, no en uno solo.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el segundo componente de runtime del libro:

```pseudocode
COMPONENT ToolRuntime
    consumes: ExecutionContext, ToolCall
    produces: ToolResult, AgentEvent, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Article III (sección "ToolRuntime"):

```text
COMPONENT: ToolRuntime

Responsibility:
    Resolver la capability solicitada por un ToolCall, validar su input contra el schema
    declarado, ejecutar los hooks de extensión y coordinar la ejecución de la acción aprobada,
    devolviendo un ToolResult normalizado.

Consumes:
    C-004 ExecutionContext, C-008 ToolCall

Depends on:
    (ninguno todavía — PolicyEngine, HumanInteractionService, ExecutionController y
    CapabilityRegistry son Preview, no introducidos en este capítulo; ver seccion 9)

Produces:
    C-009 ToolResult, C-010 AgentEvent (TOOL_CALL_COMPLETED / TOOL_CALL_FAILED),
    C-011 HarnessError (embebido en un ToolResult fallido)

Owns (Article III, cita literal):
    - resolver tools/capabilities
    - validar llamadas
    - ejecutar hooks
    - coordinar ejecución
    - devolver resultados normalizados

Does NOT own (Article IV — declarado con el mismo peso que Owns):
    - policy evaluation y autorización de la acción (PolicyEngine, Article IV — no introducido
      en este capítulo)
    - aprobación humana (HumanInteractionService — no introducido en este capítulo)
    - enforcement de ExecutionBudget (ExecutionController — no introducido en este capítulo,
      mismo patrón ya establecido por AgentLoop en CH-01)
    - registro y resolución de qué implementación satisface una capability solicitada
      (CapabilityRegistry, Article III — no introducido en este capítulo, es un componente
      distinto)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — pero esta vez
con **cuatro** exclusiones explícitas, no dos: `ToolRuntime` está un paso más cerca del mundo
externo que `AgentLoop`, y por eso tiene más vecinos con quienes podría, silenciosamente, confundir
fronteras si no las declarara todas ahora.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
ToolRuntime
    consumes → ExecutionContext, ToolCall
    produces → ToolResult, AgentEvent, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`ToolRuntime` no depende hoy de ningún otro componente registrado — ni siquiera de `AgentLoop`
(CMP-001): la relación entre ambos es la inversa de una `dependency` en el sentido de
`registry/components.yaml` (`AgentLoop` invocaría a `ToolRuntime`, no al revés), y ese cableado
end-to-end pertenece a un capítulo posterior (ver seccion 12/18). En prosa (nunca dentro de un
bloque `pseudocode`, per `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las
dependencias futuras que capítulos posteriores agregarán son:

| Componente futuro (Preview — no introducido en este capítulo) | Qué le daría a `ToolRuntime` |
|---|---|
| `PolicyEngine` | la autorización que `ToolRuntime` explícitamente no posee |
| `HumanInteractionService` | la aprobación humana que `ToolRuntime` explícitamente no posee |
| `ExecutionController` | el enforcement de `ExecutionBudget` que `ToolRuntime` explícitamente no posee |
| `CapabilityRegistry` | la resolución real de qué implementación satisface una capability |

Toda dependencia futura deberá apuntar hacia el contrato/interfaz estable de esos componentes,
nunca hacia una implementación concreta (regla fijada en CH-00 §9, reafirmada en CH-01 §9).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[AgentLoop — WAITING_FOR_TOOL, CH-01] → ToolRuntime → [Capability real — CapabilityRegistry,
Preview, no introducido]
```

**Vista 2 — Sequence**

```text
ToolCall
   │ (intención ya resuelta, recibida por ToolRuntime)
   ▼
ToolRuntime
   │ executeToolCall(call, execution, agentId, capabilityResolved, inputValid,
   │                 executionSucceeded, executionOutput)
   │ resuelve capability / valida schema del input
   │ beforeToolCall(call)
   │ coordina la ejecución
   │ afterToolCall(result)
   │ emite: AgentEvent (TOOL_CALL_COMPLETED | TOOL_CALL_FAILED)
   ▼
ToolResult
   │
   ▼
[AgentLoop retoma el ciclo con este ToolResult como observación — Preview, capítulo posterior
que conecta ambos extremos, ver seccion 12/18]
```

**Vista 3 — Pseudocódigo**

Ver §11: `executeToolCall` es la primera formalización ejecutable de "`ToolRuntime` decide cómo se
ejecuta una acción ya aprobada".

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde CH-00/CH-01.

```pseudocode
FUNCTION executeToolCall(
    call: ToolCall,
    execution: ExecutionContext,
    agentId: AgentId,
    capabilityResolved: Boolean,
    inputValid: Boolean,
    executionSucceeded: Boolean,
    executionOutput: Value
) -> ToolResult

    failure: HarnessError = NULL

    IF NOT capabilityResolved
        failure = HarnessError(
            category = VALIDATION,
            code = "CAPABILITY_NOT_FOUND",
            message = "ToolRuntime no pudo resolver la capability solicitada por este ToolCall",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    ELSE IF NOT inputValid
        failure = HarnessError(
            category = VALIDATION,
            code = "TOOL_INPUT_SCHEMA_MISMATCH",
            message = "El input de este ToolCall no cumple el schema declarado por la capability",
            recoverable = TRUE,
            retryable = FALSE,
            metadata = {}
        )
    END

    IF failure != NULL
        rejected: ToolResult = ToolResult(
            callId = call.id,
            succeeded = FALSE,
            output = NULL,
            error = failure,
            completedAt = now()
        )

        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = TOOL_CALL_FAILED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = rejected
        )

        RETURN rejected
    END

    beforeToolCall(call)

    settled: ToolResult

    IF executionSucceeded
        settled = ToolResult(
            callId = call.id,
            succeeded = TRUE,
            output = executionOutput,
            error = NULL,
            completedAt = now()
        )
    ELSE
        settled = ToolResult(
            callId = call.id,
            succeeded = FALSE,
            output = NULL,
            error = HarnessError(
                category = TOOL,
                code = "TOOL_EXECUTION_FAILED",
                message = "La capability invocada terminó con un fallo durante su ejecución",
                recoverable = TRUE,
                retryable = TRUE,
                metadata = {}
            ),
            completedAt = now()
        )
    END

    afterToolCall(settled)

    resolvedEventType: AgentEventType = TOOL_CALL_COMPLETED
    IF NOT settled.succeeded
        resolvedEventType = TOOL_CALL_FAILED
    END

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = resolvedEventType,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = settled
    )

    RETURN settled
END
```

`newEventId()`, `now()`, `beforeToolCall(...)` y `afterToolCall(...)` son primitivas/puntos de
extensión (igual que en CH-00/CH-01) — no son entidades arquitectónicas ni componentes, no
requieren ficha ni registro; `beforeToolCall`/`afterToolCall` son, literalmente, los puntos donde
P-12 permite que un hook intervenga, modelados aquí solo como invocación, sin definir todavía un
registro de hooks propio.

`capabilityResolved`, `inputValid`, `executionSucceeded` y `executionOutput` son señales de entrada
— igual que `modelFinished`/`modelProposesToolCall` en CH-01 §11 — que un componente todavía sin
introducir (`CapabilityRegistry`, y la implementación concreta de la capability) produciría en la
realidad. `executeToolCall` no calcula ninguna de las cuatro: las recibe y decide, determinísticamente,
qué `ToolResult` construir a partir de ellas.

Nótese lo que `executeToolCall` **no** hace: no evalúa ninguna policy ni decide autorización
(Article VI, Execution Rule 3: "las policies se evalúan antes del side effect" — todavía sin
componente que lo haga cumplir), no espera ninguna aprobación humana, no verifica
`execution.budget` (esa es la operational continuation que Article IV asigna a
`ExecutionController`, preview — mismo patrón que CH-01 §11 ya estableció para `AgentLoop`), y no
decide qué implementación concreta satisface `call.capability` — solo recibe si esa resolución ya
ocurrió (`capabilityResolved`).

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013): esa máquina de estados sigue
siendo propiedad exclusiva de `AgentLoop` (CH-01 §12), y su tabla de transiciones no cambia aquí.

`executeToolCall` (§11) sí atraviesa un camino implícito con cuatro puntos de decisión — pero
deliberadamente **no** se formaliza como un nuevo contrato de lifecycle en este capítulo (eso
introduciría una tercera entidad nueva, fuera del alcance decidido para este capítulo):

```text
ToolCall recibido
   → capability sin resolver     → ToolResult (succeeded = FALSE, error = CAPABILITY_NOT_FOUND)
   → input inválido              → ToolResult (succeeded = FALSE, error = TOOL_INPUT_SCHEMA_MISMATCH)
   → beforeToolCall
   → ejecución falla              → ToolResult (succeeded = FALSE, error = TOOL_EXECUTION_FAILED)
   → ejecución tiene éxito         → ToolResult (succeeded = TRUE, output = executionOutput)
   → afterToolCall
```

**Lo que este capítulo explícitamente no cierra**: la tabla de transiciones de `AgentRunStatus`
(CH-01 §12) sigue anotando `WAITING_FOR_TOOL → RUNNING` como "Preview — ToolRuntime resuelve el
ToolResult; no introducido en este capítulo". Esa anotación seguía siendo literalmente cierta en el
capítulo anterior porque `ToolRuntime` no existía; ahora que existe, la pieza que falta no es
`ToolRuntime` en sí, sino el cableado que tomaría el `ToolResult` que este capítulo sí sabe producir
y lo usaría para decidir la siguiente transición de `AgentRunStatus` — ese cableado pertenece a un
capítulo posterior (ver seccion 18/19), y `book/chapters/01-agent-loop/chapter.md` no se modifica
para reflejarlo todavía (fuera de su campo `next_chapter`).

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6) clasifica también los fallos que introduce este capítulo,
fiel a los `Failure Examples` de `constitution/ARCHITECTURE_CONSTITUTION.md` Article VII:

```text
VALIDATION
    CAPABILITY_NOT_FOUND        — ToolRuntime no pudo resolver la capability solicitada
        → recoverable: FALSE, retryable: FALSE
    TOOL_INPUT_SCHEMA_MISMATCH  — el input no cumple el schema declarado ("Invalid tool
                                    arguments → validation/recoverable", Article VII)
        → recoverable: TRUE, retryable: FALSE

TOOL
    TOOL_EXECUTION_FAILED       — la capability se ejecutó pero falló ("Tool timeout → tool/
                                    potentially retryable", Article VII)
        → recoverable: TRUE, retryable: TRUE
```

`executeToolCall` nunca devuelve una excepción cruda ni un `ToolResult` sin `error` cuando
`succeeded = FALSE`: siempre construye un `HarnessError` con `category`, `recoverable` y
`retryable` explícitos — mismo patrón que `runTurn` (CH-01 §11) y `governTurnContinuation` (CH-00
§11).

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo de `category = POLICY`
(autorización denegada) o `category = BUDGET` (presupuesto agotado) sigue sin ser responsabilidad
de `ToolRuntime` — su propio `does_not_own` (seccion 8) excluye explícitamente ambas decisiones.
Este capítulo no reclasifica ni reimplementa esa semántica; solo se abstiene de absorberla.

## 14. Eventos Producidos (Events Produced)

Este capítulo agrega dos valores a `AgentEventType` (seccion 6) — los primeros que observan la
ejecución de una tool call, no la continuación de un turno:

```text
TOOL_CALL_COMPLETED   — ToolRuntime ejecutó la acción y tuvo éxito (executeToolCall, §11)
TOOL_CALL_FAILED      — ToolRuntime rechazó o no pudo completar la ejecución (executeToolCall, §11)
```

`RUN_STARTED`, `TURN_CONTINUED`, `RUN_COMPLETED` y `RUN_FAILED` (CH-00/CH-01) no se emiten desde
`executeToolCall`: pertenecen al ciclo cognitivo que posee `AgentLoop`, no a la ejecución de una
tool call. Un capítulo posterior que conecte ambos extremos (ver seccion 18/19) podrá correlacionar
un `TOOL_CALL_COMPLETED`/`TOOL_CALL_FAILED` con el siguiente `TURN_CONTINUED` sin redefinir el
envelope común `AgentEvent` (C-010).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

Este capítulo no implementa el pipeline completo de Article VI (`Tool Intent → Resolve Capability →
Validate Schema → beforeToolCall → Policy Evaluation → Authorization → Human Approval? →
Execution Budget → Sandbox → Execute → afterToolCall → ToolResult → Observation`). `executeToolCall`
(§11) solo modela el tramo que le pertenece a `ToolRuntime` por su propia ficha constitucional:
`Resolve Capability` (como señal ya resuelta, `capabilityResolved`), `Validate Schema`
(`inputValid`), `beforeToolCall`, coordinar `Execute` (`executionSucceeded`/`executionOutput`) y
`afterToolCall` — y devuelve el `ToolResult`.

Los tramos que este capítulo **no** implementa, y que `ToolRuntime.does_not_own` declara
explícitamente:

- **Policy Evaluation / Authorization** (P-05, P-13): no hay `PolicyEngine` todavía (seccion 9).
  Nada en `executeToolCall` evalúa si la acción está permitida — recibe `capabilityResolved` como
  dado, no decide si debería estarlo.
- **Human Approval?**: no hay `HumanInteractionService` todavía. `executeToolCall` nunca espera una
  resolución humana; si una capability la requiriera, esa decisión pertenece a un componente
  distinto, no a `ToolRuntime`.
- **Execution Budget**: no hay `ExecutionController` todavía. `executeToolCall` no verifica
  `execution.budget.maxToolCalls` ni `maxConcurrentTools` (C-012, CH-00) — mismo patrón que
  `AgentLoop.runTurn` ya estableció para `budget.maxTurns` en CH-01.
- **Sandbox**: no modelado en este capítulo — la coordinación de la ejecución real (`executionSucceeded`/
  `executionOutput`) es, deliberadamente, una señal de entrada, no un mecanismo de aislamiento.

`ToolResult` es, por diseño, la forma en que `ToolRuntime` comunica el resultado de ese tramo
parcial — nunca una afirmación de que el pipeline completo de Article VI se ejecutó.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST ExecuteToolCallNeverSkipsInputSchemaValidation
TEST ExecuteToolCallNeverInvokesPolicyEngineHumanInteractionServiceOrExecutionControllerDirectly
TEST ExecuteToolCallAlwaysReturnsAToolResultCorrelatedByCallId
TEST ExecuteToolCallAlwaysEmitsAnAgentEventOnCompletionOrFailure
TEST ToolResultErrorIsAlwaysAHarnessErrorWhenSucceededIsFalse
TEST ToolResultErrorIsAlwaysAbsentWhenSucceededIsTrue
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.1, después de CH-02)

Constitution
 ├── Article I    — Principles (P-01 .. P-15)
 ├── Article II   — Invariants (INV-01 .. INV-20)
 ├── Article III  — Component Sovereignty (AgentLoop, ToolRuntime: dos componentes instanciados)
 ├── Article IV   — Decision Ownership (en uso: AgentLoop y ToolRuntime declaran owns/does_not_own)
 └── Article VI   — Execution Constitution (tramo Resolve Capability .. afterToolCall modelado;
                     Policy Evaluation .. Sandbox sigue sin componente)

Contracts (registry/contracts.yaml)
 ├── C-001 AgentMessage        (CH-00)
 ├── C-002 AgentConfig         (CH-00)
 ├── C-003 AgentState          (CH-00)
 ├── C-004 ExecutionContext    (CH-00)
 ├── C-008 ToolCall            (CH-02, nuevo — formaliza lo que INV-04/INV-05 solo citaban por nombre)
 ├── C-009 ToolResult          (CH-02, nuevo — formaliza lo que INV-07 solo citaba por nombre)
 ├── C-010 AgentEvent          (CH-00)
 ├── C-011 HarnessError        (CH-00)
 ├── C-012 ExecutionBudget     (CH-00)
 └── C-013 AgentRunStatus      (CH-01)

Components (registry/components.yaml)
 ├── CMP-001 AgentLoop         (CH-01)
 └── CMP-002 ToolRuntime       (CH-02, nuevo — segundo componente del libro)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El pipeline completo de Article VI**: `Policy Evaluation`, `Authorization`, `Human Approval?`,
  `Execution Budget` y `Sandbox` siguen sin componente que los ejecute. `executeToolCall` (§11)
  modela únicamente el tramo que `ToolRuntime` posee por su propia ficha constitucional — el resto
  es deuda intencional hacia los capítulos que introduzcan `PolicyEngine`,
  `HumanInteractionService` y `ExecutionController`.
- **Resolución real de capabilities**: `CapabilityRegistry` sigue sin existir. `capabilityResolved`
  y `executionSucceeded`/`executionOutput` son señales de entrada asumidas, no producidas todavía
  por ningún componente. Tampoco existe un `STRUCT Tool` que declare nombre, schema y `execute` de
  una capability — ese contrato pertenece al mismo capítulo futuro.
- **El cableado de vuelta hacia `AgentLoop`**: `WAITING_FOR_TOOL → RUNNING` (C-013, CH-01 §12) sigue
  sin resolverse en la práctica. Este capítulo produce un `ToolResult` real, pero conectarlo con
  `runTurn` para que `AgentLoop` retome el ciclo (INV-07) es trabajo explícito de un capítulo
  posterior — probablemente el mismo que introduzca `ModelGateway` y complete el ciclo real
  extremo a extremo.
- **Paralelismo y secuencialidad (Execution Rules 5/6)**: este capítulo modela la ejecución de un
  único `ToolCall`. Coordinar múltiples tool calls independientes en paralelo, o forzar
  secuencialidad cuando comparten estado mutable, queda fuera de alcance — ninguna metadata de
  `execution: { mode, sideEffect }` (mencionada en
  `reference/md/Estructura_Libro_Construyendo_un_Agent_Harness_v0.2.md`, Capítulo 6 del outline
  original) se introduce todavía.
- **Autorización real, aprobación humana real, budget enforcement real**: `PolicyEngine`,
  `HumanInteractionService` y `ExecutionController` siguen sin existir; P-05/P-13 y Execution Rule 3
  siguen siendo reglas declaradas, no reglas exigidas por código.
- **Persistencia real de `AgentState`/`SessionState`**: sin cambios respecto a CH-00/CH-01 —
  `SessionManager` no existe.
- **Reviewers plurales, evals, orquestación multi-agente y aprobación humana persistente del
  propio Book Harness**: explícitamente fuera de alcance de BH-v0.1 (igual que CH-00/CH-01).

## 19. Siguiente Incremento (Next Increment)

El problema natural del próximo capítulo: ahora que `ToolRuntime` puede producir un `ToolResult`
real (§11), ¿quién decide si la acción que ese `ToolResult` representa estaba permitida —
antes de que `executeToolCall` llegue siquiera a coordinar la ejecución — y quién conecta ese
resultado de vuelta con el `AgentRunStatus` de `AgentLoop` para que el ciclo cognitivo realmente
continúe? Eso apunta hacia `PolicyEngine` (Article IV: "¿está permitida esta acción?") como el
tercer componente candidato de Article III que dejaría de ser preview, y hacia el capítulo que
finalmente cablee `AgentLoop` + `ToolRuntime` de punta a punta (probablemente junto con
`ModelGateway`, para que `modelProposesToolCall` deje de ser una señal asumida).

Ese capítulo (`CH-03`, fuera del alcance de esta ejecución) heredaría directamente la deuda
intencional de §18. `next_chapter` queda en `null` en el frontmatter de este capítulo porque, en
este momento del libro, `CH-03` todavía no existe como archivo — solo como el problema que
motivará su escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de
> la secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco
> Iceberg / Bucles de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas,
> Forrester/Meadows), secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): sin un dueño explícito para "¿cómo se ejecuta una acción
   ya aprobada?", cada implementación termina invocando la herramienta de una manera distinta —
   algunas sin validar argumentos, otras mezclando ejecución con autorización, otras devolviendo el
   resultado con una forma distinta cada vez.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): sin un componente
   con fronteras explícitas, la decisión de ejecución tiende a absorber silenciosamente decisiones
   vecinas (autorización, aprobación humana, presupuesto, resolución de capacidades) solo porque
   están físicamente cerca del punto donde ocurre la ejecución — exactamente lo que Article IV
   prohíbe.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `ToolRuntime` (CMP-002) con una ficha que declara tanto lo que posee (`owns`) como lo que
   explícitamente NO posee (`does_not_own`, con cuatro exclusiones) y formaliza `ToolCall` (C-008)
   y `ToolResult` (C-009) — los dos contratos que la Constitution ya citaba por nombre desde su
   primera versión (INV-04/INV-05/INV-07) sin que existieran todavía como tales.
4. **Modelos mentales** (= §4, Constitutional Impact): el Ownership Rule de Article IV — "ningún
   componente debe absorber silenciosamente decisiones que pertenecen a otro dominio" — aplicado
   ahora a un segundo componente, con más vecinos que declarar que los que tuvo `AgentLoop`.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un componente nuevo se introduce sin declarar
  explícitamente su `does_not_own`, aumenta la probabilidad de que absorba silenciosamente la
  próxima decisión vecina "porque ya estaba ahí" — el mismo bucle que CH-01 cortó para `AgentLoop`.
  Este capítulo repite el corte para `ToolRuntime`, con cuatro exclusiones explícitas en vez de dos.
- **Bucle de equilibrio (estabiliza):** `executeToolCall` (§11) rechaza con un `ToolResult` fallido
  — nunca con una excepción sin tipar — tanto una capability sin resolver como un input inválido,
  antes de coordinar cualquier ejecución real.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `ToolRuntime` (CMP-002) declare sus cuatro
`does_not_own` en el mismo momento en que se introduce — antes de que exista código real que pueda
absorber silenciosamente la autorización, la aprobación humana, el presupuesto o la resolución de
capacidades. Si esta frontera no se fija aquí, cada uno de los cuatro componentes futuros que sí
poseen esas decisiones tendría que arrancarle esa responsabilidad a `ToolRuntime` en vez de
simplemente ocuparla.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado
> completo de esta sección (con ids estables para cada pregunta/tarjeta) vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida. Aquí se
> presenta en prosa, para lectura directa del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Cuando el modelo propone usar una herramienta y la ejecución queda esperando esa resolución
   (ver capítulo anterior), ¿quién decide exactamente qué implementación concreta satisface esa
   intención, y qué debe verificarse antes de permitir que la acción externa ocurra? *(cierra la
   pregunta guía 1)*
2. Si la intención de usar una herramienta llega con datos de entrada que no corresponden a lo que
   esa herramienta espera recibir, ¿en qué punto exacto del camino debe detectarse ese problema, y
   qué impide que la ejecución siga adelante de todos modos? *(cierra la pregunta guía 2)*
3. Una vez que la acción externa termina, ¿de qué forma se le comunica al resto del sistema si tuvo
   éxito o si falló, sin que cada implementación distinta invente su propia manera de
   representarlo? *(cierra la pregunta guía 3)*
4. ¿Por qué el mismo componente que coordina la ejecución de una acción externa no debería, además,
   decidir si esa acción estaba autorizada, si alguien humano debía aprobarla primero, o si el
   presupuesto de ejecución todavía lo permite? *(cierra la pregunta guía 4)*

### Explicar

1. `ToolRuntime` posee coordinar la ejecución de una tool call ya aprobada. Explica, como si
   hablaras con alguien sin contexto técnico, por qué NO posee la decisión de si esa acción estaba
   permitida — ¿qué se rompería, en concreto, si `ToolRuntime` empezara a decidir autorización
   directamente "ya que de todos modos es quien ejecuta la acción"?
2. `ToolResult` reutiliza `HarnessError` (C-011, ya existente desde CH-00) para representar un
   fallo, en vez de definir un tipo de error nuevo propio de las tool calls. Explica qué
   perderíamos, en términos de auditoría y consistencia, si cada componente del libro definiera su
   propia forma de representar un fallo en vez de compartir un único contrato de error clasificado.

### Conectar

1. Cuando `AgentLoop.runTurn` (CH-01) transiciona una ejecución a `WAITING_FOR_TOOL` porque el
   modelo propuso `modelProposesToolCall = TRUE`, ¿qué dos campos de la señal que el modelo propuso
   necesitaría poblar quien construya el `ToolCall` correspondiente, para que `ToolRuntime` pueda
   intentar resolver la capacidad solicitada?

### Espaciar

Las cuatro tarjetas de repaso de este capítulo (dos sobre `ToolRuntime` — su `owns` y su
`does_not_own` — y una por cada contrato, `ToolCall`/`ToolResult`) entran hoy en
`reviewStage = DAY_1`. Repásalas de nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) —
ver el apéndice de tarjetas al final del libro (edición PDF) o `retrieval_set.flashcards` en
`dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te
equivocaste, ese es precisamente el punto ciego que este método existe para revelar.
