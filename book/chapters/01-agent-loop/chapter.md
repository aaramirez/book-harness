---
id: CH-01
title: "El Agent Loop y el Ciclo de Ejecución Cognitiva"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-001]
introduces_contracts: [C-013]
modifies_contracts: []
constitutional_articles: [P-10, P-12, P-13, INV-08, INV-09, INV-16, INV-17, INV-18, INV-19]
previous_chapter: CH-00
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH01
    text: |
      Al terminar este capítulo podrás distinguir, dentro de la decisión "¿debe ocurrir otro
      turno de razonamiento?", qué parte le pertenece en exclusiva a AgentLoop y qué parte
      pertenece a un dominio distinto (autorización, presupuesto operacional, ejecución de una
      tool call) que todavía no tiene componente propio — y podrás diagnosticar, para cualquier
      AgentRunStatus dado, si la transición que propones respeta el lifecycle formal de Article V
      o si en realidad está inventando un estado que el contrato no reconoce.
  skeleton:
    id: SK-CH01
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
    components_to_be_introduced: [CMP-001]
    contracts_to_be_introduced: [C-013]
  guiding_questions:
    - id: GQ-CH01-01
      text: |
        Si el modelo termina de razonar y propone que ya tiene la respuesta final, ¿quién decide
        que el ciclo cognitivo realmente debe detenerse, en vez de asumir que el propio modelo
        simplemente dejará de proponer turnos?
      answered_by: RQ-CH01-01
    - id: GQ-CH01-02
      text: |
        Cuando el modelo propone usar una herramienta con efectos reales, ¿en qué punto exacto
        del ciclo queda la ejecución mientras esa decisión de autorización todavía no se ha
        resuelto, y quién resuelve finalmente ese punto?
      answered_by: RQ-CH01-02
    - id: GQ-CH01-03
      text: |
        Dentro del mismo componente que decide si otro turno debe ocurrir, ¿por qué mezclar esa
        decisión con la de si el presupuesto de ejecución todavía lo permite violaría una regla
        arquitectónica ya establecida, aunque nadie más esté todavía disponible para tomar esa
        segunda decisión?
      answered_by: RQ-CH01-03
    - id: GQ-CH01-04
      text: |
        Si una ejecución se detiene a mitad de un turno sin haber terminado ni haber fallado por
        un error operacional, ¿qué punto intermedio formal representa exactamente esa espera, y
        por qué no basta con reutilizar el mismo estado que usamos para un error?
      answered_by: RQ-CH01-04
  systems_lens:
    iceberg_visible_fact: |
      Sin un dueño explícito para "¿debe ocurrir otro turno?", cada implementación termina
      decidiéndolo de una manera distinta: algunas confían en que el modelo diga "ya terminé";
      otras cuentan turnos a mano en el llamador; otras mezclan esa decisión con la de si el
      presupuesto todavía alcanza — tres decisiones distintas resueltas por tres criterios
      distintos, ninguno declarado (ver seccion 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que, sin un componente con fronteras explícitas, la decisión de
      continuación cognitiva tiende a absorber silenciosamente decisiones vecinas (presupuesto,
      autorización) solo porque están físicamente cerca en el código — exactamente lo que Article
      IV prohíbe. Y sin un `AgentRunStatus` completo y registrado, cada punto de espera a mitad de
      un turno (¿tool call pendiente? ¿aprobación humana pendiente? ¿aprobación humana que venció
      sin resolverse?) termina representado con el mismo campo de estado ambiguo, o con texto libre
      (ver seccion 3, Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala el primer componente real del libro, `AgentLoop` (CMP-001), con una
      ficha que declara tanto lo que posee (`owns`: turn lifecycle, continuation, completion) como
      lo que explícitamente NO posee (`does_not_own`: autorización, operational continuation,
      ejecución de una tool call) — y formaliza `AgentRunStatus` (C-013) como contrato completo de
      11 estados, corrigiendo la versión preliminar de CH-00 que no distinguía `EXPIRED` de
      `FAILED` (ver seccion 8, Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es el Ownership Rule de Article IV (Decision
      Ownership): "ningún componente debe absorber silenciosamente decisiones que pertenecen a
      otro dominio". `AgentLoop` existe precisamente para que "¿debe ocurrir otro turno?" tenga un
      dueño — y para que esa misma ficha declare, con la misma fuerza, qué decisiones vecinas
      todavía no tienen dueño en este punto del libro (ver seccion 4, Impacto Constitucional).
    reinforcing_loop: |
      Cada vez que un componente nuevo se introduce sin declarar explícitamente su `does_not_own`,
      aumenta la probabilidad de que absorba silenciosamente la próxima decisión vecina "porque ya
      estaba ahí" — y de que el siguiente capítulo herede esa ambigüedad en vez de heredar una
      frontera clara. Este capítulo corta esa espiral declarando el `does_not_own` de `AgentLoop`
      con el mismo peso que su `owns`.
    balancing_loop: |
      `runTurn` (seccion 11) es el mecanismo de equilibrio: antes de decidir cualquier transición,
      rechaza con un `HarnessError` toda invocación sobre un `AgentRunStatus` terminal
      (`COMPLETED`/`FAILED`/`CANCELLED`/`EXPIRED`), en vez de permitir que un turno fantasma
      continúe silenciosamente después de que la ejecución ya cerró.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `AgentLoop` (CMP-001) declare su
      `does_not_own` en el mismo momento en que se introduce — antes de que exista código que
      pueda absorber silenciosamente la operational continuation (presupuesto) o la autorización.
      Si esta frontera no se fija aquí, el próximo componente que sí las posea (`ExecutionController`,
      `PolicyEngine`) tendría que arrancarle esa responsabilidad a `AgentLoop` en vez de simplemente
      ocuparla.
  recall_questions:
    - id: RQ-CH01-01
      text: |
        ¿Qué decide `AgentLoop` cuando `runTurn` recibe `modelFinished = TRUE`, y a qué valor de
        `AgentRunStatus` transiciona la ejecución?
    - id: RQ-CH01-02
      text: |
        ¿A qué valor de `AgentRunStatus` transiciona `runTurn` cuando el modelo propone una tool
        call, y qué componente (todavía no introducido en este libro) es responsable de resolver
        ese estado?
    - id: RQ-CH01-03
      text: |
        Según Article IV (Decision Ownership), ¿qué decisión posee `AgentLoop` y qué decisión
        relacionada NO posee — y a qué componente, todavía sin introducir, pertenece esa segunda
        decisión?
    - id: RQ-CH01-04
      text: |
        ¿Qué valor agrega este capítulo al `ENUM AgentRunStatus` que la versión preliminar de
        CH-00 no tenía, y qué transición de la tabla de estados de CH-00 corrige exactamente?
  explain_prompts:
    - id: EP-CH01-01
      text: |
        `AgentLoop` posee la decisión de continuación cognitiva (turn lifecycle, continuation,
        completion). Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee
        la autorización de una tool call ni su ejecución concreta — ¿qué se rompería, en concreto,
        si `AgentLoop` empezara a ejecutar tools directamente "ya que de todos modos decide cuándo
        se piden"?
      target_entity: CMP-001
    - id: EP-CH01-02
      text: |
        Usando el Ownership Rule de Article IV, explica por qué la verificación de
        `budget.maxTurns` que CH-00 ya introdujo (`governTurnContinuation`) NO se convierte
        automáticamente en una responsabilidad de `AgentLoop` solo porque `AgentLoop` ya existe
        como componente real — ¿a qué componente, todavía sin introducir en este libro, pertenece
        esa decisión?
      target_entity: CMP-001
  interleaved_questions:
    - id: IQ-CH01-01
      text: |
        Cada vez que `AgentLoop` transiciona el `AgentRunStatus` de una ejecución y emite un
        `AgentEvent`, ¿qué tres campos de `ExecutionContext` (introducido en CH-00) necesita leer
        para poblar el `runId`, el `sessionId` y el `traceId` de ese evento?
      current_chapter_entities: [CMP-001, C-013]
      prior_chapter_entities: [C-004, C-010]
      prior_chapter: CH-00
  flashcards:
    - id: FC-CH01-01
      front: |
        ¿Qué estado agrega este capítulo al `ENUM AgentRunStatus` que CH-00 no tenía, y qué
        transición corrige?
      back: |
        `EXPIRED`: un estado terminal distinto de `FAILED`, para cuando una aprobación humana
        pendiente vence sin resolverse. CH-00 enrutaba esa transición hacia `FAILED` por no tener
        todavía este estado propio en su versión preliminar del enum.
      source_entity: C-013
      chapter_introduced_in: CH-01
      review_stage: DAY_1
    - id: FC-CH01-02
      front: |
        ¿Qué posee `AgentLoop` (Article III / Article IV), en una frase?
      back: |
        Turn lifecycle, el ciclo model → action → observation (la decisión de continuar, no su
        ejecución), continuation y completion — la pregunta "¿debe ocurrir otro turno de
        razonamiento?".
      source_entity: CMP-001
      chapter_introduced_in: CH-01
      review_stage: DAY_1
    - id: FC-CH01-03
      front: |
        ¿Qué NO posee `AgentLoop`, y a qué componentes (todavía sin introducir) pertenecen esas
        decisiones?
      back: |
        Autorización y ejecución de tool calls (`PolicyEngine`/`ToolRuntime`) y operational
        continuation por presupuesto/cancelación (`ExecutionController`) — ninguno de los tres
        existe todavía en `registry/components.yaml`; `AgentLoop` solo transiciona a
        `WAITING_FOR_TOOL` y deja ese punto deliberadamente sin resolver.
      source_entity: CMP-001
      chapter_introduced_in: CH-01
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH01-01
      recall_question: RQ-CH01-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH01-02
      recall_question: RQ-CH01-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH01-03
      recall_question: RQ-CH01-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH01-04
      recall_question: RQ-CH01-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 1 — El Agent Loop y el Ciclo de Ejecución Cognitiva

> **Regla constitucional (Article IV):** ningún componente debe absorber silenciosamente
> decisiones que pertenecen a otro dominio.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de
> saber cómo se llama el componente de este capítulo. El detalle estructurado de esta sección
> vive en `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, dentro de la decisión "¿debe
ocurrir otro turno de razonamiento?", qué parte le pertenece en exclusiva al componente que este
capítulo introduce y qué parte pertenece a un dominio distinto (autorización, presupuesto
operacional, ejecución de una tool call) que todavía no tiene componente propio — y podrás
diagnosticar, para cualquier estado de ejecución dado, si la transición que propones respeta el
lifecycle formal de la Constitution o si en realidad está inventando un estado que el contrato no
reconoce.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e
introduce un contrato de datos (`AgentRunStatus`, formalizando lo que CH-00 ya usaba por nombre) y
el primer componente de runtime del libro (`AgentLoop`) — todavía sin explicarlos, solo como mapa.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar
atrás; están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este
capítulo va a definir):

1. Si el modelo termina de razonar y propone que ya tiene la respuesta final, ¿quién decide que el
   ciclo cognitivo realmente debe detenerse, en vez de asumir que el propio modelo simplemente
   dejará de proponer turnos?
2. Cuando el modelo propone usar una herramienta con efectos reales, ¿en qué punto exacto del
   ciclo queda la ejecución mientras esa decisión de autorización todavía no se ha resuelto, y
   quién resuelve finalmente ese punto?
3. Dentro del mismo componente que decide si otro turno debe ocurrir, ¿por qué mezclar esa
   decisión con la de si el presupuesto de ejecución todavía lo permite violaría una regla
   arquitectónica ya establecida, aunque nadie más esté todavía disponible para tomar esa segunda
   decisión?
4. Si una ejecución se detiene a mitad de un turno sin haber terminado ni haber fallado por un
   error operacional, ¿qué punto intermedio formal representa exactamente esa espera, y por qué no
   basta con reutilizar el mismo estado que usamos para un error?

## 1. Arquitectura Actual (Current Architecture)

CH-00 dejó instalados siete contratos de datos fundamentales (`AgentMessage`, `AgentConfig`,
`AgentState`, `ExecutionContext`, `AgentEvent`, `HarnessError`, `ExecutionBudget`) y dos políticas
(P-05, P-13) — pero `registry/components.yaml` seguía vacío. La única función ejecutable que
existía, `governTurnContinuation` (CH-00 §11), no tenía dueño: era una demostración genérica de
"Harness Runtime governs", escrita antes de que existiera ningún componente al que asignársela.

`AgentState.status: AgentRunStatus` (C-003) ya referenciaba `AgentRunStatus` por nombre desde
CH-00, y CH-00 §6 incluso mostraba un `ENUM AgentRunStatus` de trabajo — pero ese enum nunca se
registró como contrato propio en `registry/contracts.yaml`, y su versión de trabajo tenía diez
estados, no los once que `constitution/ARCHITECTURE_CONSTITUTION.md` Article V realmente define.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas, la decisión "¿debe ocurrir otro turno de razonamiento?"
no tiene un lugar fijo donde vivir. Una implementación puede decidirlo preguntándole al modelo si
ya terminó (dejando la decisión en manos de la propia entidad probabilística que P-10 dice que no
debe controlarla); otra puede contar turnos manualmente en el código que invoca el ciclo; una
tercera puede mezclar esa decisión con la de si el presupuesto de ejecución todavía alcanza, porque
ambas viven físicamente cerca en el mismo bucle `while`.

Necesitamos que "¿debe ocurrir otro turno?" tenga un dueño único y nombrado — y que ese dueño
declare, con la misma fuerza con la que declara lo que posee, lo que explícitamente no posee.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los siete contratos de CH-00 describen datos, no comportamiento. Sin un componente:

- nada impide que la decisión de continuación cognitiva absorba silenciosamente la decisión de si
  el presupuesto operacional todavía lo permite — ambas terminan resueltas por la misma función,
  aunque Article IV las asigna a dueños distintos (`AgentLoop` vs. `ExecutionController`);
- `AgentRunStatus` sigue siendo un enum de trabajo sin registrar, con diez estados en vez de los
  once reales — cualquier capítulo futuro que lo use "por nombre" heredaría una versión incompleta;
- no existe ningún punto formal que represente "el modelo propuso una tool call y la ejecución
  está esperando que alguien más, todavía no introducido en este libro, resuelva esa autorización
  y esa ejecución";
- `governTurnContinuation` (CH-00) sigue sin dueño: es código que existe, pero no pertenece
  todavía a ningún componente con `owns`/`does_not_own` declarados.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la
> secuencia `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una
> entidad que no haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT`
> registrado — **no magic entities**. Este capítulo aplica la misma disciplina a nivel de
> *ownership*: ningún componente puede reclamar en prosa una responsabilidad que su propia ficha
> no declara en `owns`.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-10   The harness owns execution state—not the model.
           AgentLoop es la primera materialización concreta de este principio: decide la
           transición de AgentRunStatus, nunca el modelo.
    P-12   Events observe; hooks intervene.
           runTurn (seccion 11) emite un AgentEvent en cada transición — el primer componente
           del libro que produce eventos en la práctica, no solo en la definición del contrato.
    P-13   Authorization is deterministic and external to the LLM.
           AgentLoop declara explícitamente que NO posee autorización (does_not_own) — la
           frontera de P-13 ahora tiene un componente concreto que la respeta por diseño.

Invariants preserved
    INV-08   El harness es propietario del execution state.
             AgentLoop.owns declara turn lifecycle/continuation/completion; ningún otro
             actor (el modelo, la UI) los controla.
    INV-09   Todo AgentRun tiene límites explícitos.
             Preservado, no reimplementado: la verificación de ExecutionBudget sigue siendo
             de ExecutionController (preview, no introducido aquí) — AgentLoop deliberadamente
             no la absorbe (ver seccion 3 y seccion 18).
    INV-16   AgentCore puede ejecutarse sin UI.
             runTurn no depende de ningún adapter de presentación.
    INV-17   La UI observa y presenta el runtime mediante contratos; no contiene la lógica
             soberana del AgentLoop.
             Primera cita literal posible de este invariante: ya existe un AgentLoop real cuya
             lógica una UI NO puede absorber.
    INV-18   Toda acción significativa produce un evento observable.
             runTurn emite AgentEvent (TURN_CONTINUED / RUN_COMPLETED) en cada transición.
    INV-19   Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy
             relevante.
             Cada AgentEvent que emite AgentLoop lleva el traceId de su ExecutionContext.

Component ownership changes
    CMP-001 AgentLoop se introduce — registry/components.yaml deja de estar vacío. owns/
    does_not_own citados literalmente contra Article III (sección "AgentLoop") y Article IV.

Lifecycle changes
    AgentRunStatus se formaliza como C-013 (11 estados, fiel a Article V) — se agrega EXPIRED,
    ausente en la versión de trabajo de CH-00, y se corrige la transición
    WAITING_FOR_HUMAN --expired--> (antes FAILED, ahora EXPIRED).

Security implications
    Ninguna nueva. P-05/P-13 se preservan; AgentLoop.does_not_own excluye explícitamente
    autorización y ejecución de tool calls — ningún cambio de superficie de ataque.

Observability implications
    AgentLoop es el primer componente que emite AgentEvent en la práctica (INV-18/INV-19),
    reutilizando el envelope y los eventType ya definidos por CH-00 sin modificarlos.

Deterministic vs agentic boundary
    Article XII se refina a nivel de componente: el modelo aporta las señales de entrada
    (modelFinished, modelProposesToolCall); AgentLoop — determinístico — decide la transición
    de AgentRunStatus resultante. El modelo nunca asigna directamente un valor a status.
```

## 5. Conceptos Nuevos (New Concepts)

- **Turn**: una iteración completa del ciclo model → action → observation dentro de un `AgentRun`
  — el modelo propone, `AgentLoop` decide si esa propuesta implica otro turno, una tool call o el
  fin de la ejecución.
- **Agent Run**: una ejecución concreta de un agente (identificada por `RunId`), cuyo progreso
  representa `AgentState` y cuyo lifecycle completo describe `AgentRunStatus`.
- **Decision Ownership** *(Article IV, ya anunciado como marco en CH-00, ahora en uso)*: cada
  decisión arquitectónica tiene un dueño único y nombrado. `AgentLoop` decide "¿debe ocurrir otro
  turno?"; explícitamente NO decide "¿puede el run continuar operacionalmente?" (`ExecutionController`,
  preview) ni "¿está permitida esta acción?" (`PolicyEngine`, preview).
- **Turn Lifecycle**: el conjunto de transiciones que un `AgentRun` atraviesa dentro de un mismo
  turno — de `RUNNING`/`WAITING_FOR_MODEL` hacia `WAITING_FOR_MODEL`, `WAITING_FOR_TOOL` o
  `COMPLETED` — responsabilidad exclusiva de `AgentLoop`.
- **Handoff sin resolver** *(concepto de esta ejecución, no citado literalmente de la Constitution)*:
  el punto en el que `AgentLoop` transiciona a `WAITING_FOR_TOOL` y dejar de decidir — la
  autorización y ejecución de esa tool call pertenecen a componentes que este libro todavía no
  introduce (`PolicyEngine`, `ToolRuntime`).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados de CH-00

Estos tipos ya existen desde CH-00 (no se redefinen aquí, solo se referencian por nombre en el
pseudocódigo de este capítulo — disponibles vía `registry/contracts.yaml`, `introduced_in: CH-00`):
`AgentId`, `SessionId`, `RunId`, `TraceId`, `Timestamp`, `AgentMessage`, `AgentConfig`,
`AgentState`, `ExecutionContext`, `AgentEvent`, `HarnessError`, `ExecutionBudget`.

Dos tipos adicionales de CH-00 no tienen contrato propio con `C-XXX` (viven embebidos dentro de
`HarnessError`/`AgentEvent`), pero este capítulo los reutiliza por tipo, sin agregarles valores
nuevos:

| Identificador (heredado de CH-00, sin `C-XXX` propio) | Rol en este capítulo |
|---|---|
| `AgentEventType` | tipo de `eventType` en los `AgentEvent` que emite `AgentLoop` (reutiliza `TURN_CONTINUED`/`RUN_COMPLETED`, ya definidos en CH-00 §6; no se agregan valores) |
| `ErrorCategory` | tipo de `category` en los `HarnessError` que emite `AgentLoop` (reutiliza `VALIDATION`, ya definido en CH-00 §6) |

### `AgentRunStatus` — formalizado como contrato

CH-00 ya usaba `AgentRunStatus` por nombre (`AgentState.status: AgentRunStatus`, C-003) y mostraba
una versión de trabajo de diez estados, sin registrarla como contrato propio. Este capítulo la
formaliza fiel a `constitution/ARCHITECTURE_CONSTITUTION.md` Article V — que define once estados,
incluyendo `EXPIRED` (ausente en la versión de trabajo de CH-00):

```pseudocode
ENUM AgentRunStatus
    CREATED
    INITIALIZING
    RUNNING
    WAITING_FOR_MODEL
    WAITING_FOR_TOOL
    WAITING_FOR_HUMAN
    PAUSED
    COMPLETED
    FAILED
    CANCELLED
    EXPIRED
END
```

**Unchanged / Not yet introduced**: no hay todavía `ToolCall`, `ToolResult`, `ModelRequest`,
`ModelResponse` ni `ContextSnapshot` — siguen llegando junto con `ModelGateway`, `ContextEngine` y
`ToolRuntime` en capítulos posteriores (fuera del alcance de esta ejecución). Tampoco se agrega
ningún valor nuevo a `AgentEventType` ni a `ErrorCategory` — este capítulo los reutiliza tal cual
CH-00 los definió.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce un contrato de
datos, registrado en `registry/contracts.yaml`:

```text
ID:                     C-013
Name:                   AgentRunStatus
Version:                v1
Introduced In:          CH-01
Current Definition:     ENUM AgentRunStatus (ver §6)
Used By:                [CMP-001]
Modified By:            []
Constitutional Impact:  [P-10, INV-08, INV-09]
```

Nota de numeración: `C-005`..`C-009` quedan deliberadamente libres — reservados por convención
editorial para `ContextSnapshot`/`ModelRequest`/`ModelResponse`/`ToolCall`/`ToolResult`, los cinco
contratos que CH-00 §6 ya anunció como "Unchanged / Not yet introduced" y que llegarán junto con
`ModelGateway`/`ContextEngine`/`ToolRuntime` en un capítulo posterior. `AgentRunStatus` toma el
siguiente id realmente libre, `C-013`.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el primer componente de runtime del libro:

```pseudocode
COMPONENT AgentLoop
    consumes: AgentConfig, AgentState, ExecutionContext, AgentRunStatus
    produces: AgentState, AgentEvent, HarnessError, AgentRunStatus
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Article III (sección "AgentLoop"):

```text
COMPONENT: AgentLoop

Responsibility:
    Coordinar el turn lifecycle de una ejecución cognitiva (el ciclo model → action →
    observation), decidir si otro turno de razonamiento debe ocurrir y producir la transición
    de AgentRunStatus y el AgentEvent correspondientes.

Consumes:
    C-002 AgentConfig, C-003 AgentState, C-004 ExecutionContext, C-013 AgentRunStatus

Depends on:
    (ninguno todavía — ModelGateway, ToolRuntime, PolicyEngine y ExecutionController son
    Preview, no introducidos en este capítulo; ver seccion 9)

Produces:
    C-003 AgentState (actualizado), C-010 AgentEvent, C-011 HarnessError, C-013 AgentRunStatus
    (la transición resultante)

Owns (Article III, cita literal):
    - turn lifecycle
    - model → action → observation cycle
    - continuation
    - completion
    - coordinación de la ejecución cognitiva

Does NOT own (Article III, cita literal):
    - autorización
    - rendering
    - almacenamiento concreto
    - APIs específicas de proveedores
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule): dos
responsabilidades vecinas quedan explícitamente sin dueño en este punto del libro —
**operational continuation** (budgets/cancelación/deadlines, que Article IV asigna a
`ExecutionController`) y **ejecución de una tool call aprobada** (`ToolRuntime`) — ninguna de las
dos se le atribuye a `AgentLoop` solo porque hoy es el único componente que existe.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
AgentLoop
    consumes → AgentConfig, AgentState, ExecutionContext, AgentRunStatus
    produces → AgentState, AgentEvent, HarnessError, AgentRunStatus
    depends on (componentes) → (ninguno registrado todavía)
```

`AgentLoop` no depende hoy de ningún otro componente porque ningún otro componente existe todavía
en `registry/components.yaml`. En prosa (nunca dentro de un bloque `pseudocode`, per
`BOOK_HARNESS_BUILD_INSTRUCTIONS(1).md` §22 regla 8), las dependencias futuras que capítulos
posteriores agregarán son:

| Componente futuro (Preview — no introducido en este capítulo) | Qué le daría a `AgentLoop` |
|---|---|
| `ModelGateway` | la invocación real del modelo que produce `modelFinished`/`modelProposesToolCall` |
| `ToolRuntime` | la resolución real de `WAITING_FOR_TOOL` |
| `PolicyEngine` | la autorización que `AgentLoop` explícitamente no posee |
| `ExecutionController` | la operational continuation (budget/cancelación) que `AgentLoop` explícitamente no posee |

Toda dependencia futura deberá apuntar hacia el contrato/interfaz estable de esos componentes,
nunca hacia una implementación concreta (regla fijada en CH-00 §9).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (REGLAS_LIBRO_AGENT_HARNESS(1).md §14):

**Vista 1 — Componentes**

```text
Model → AgentLoop → [ToolRuntime — Preview, no introducido] / [fin del AgentRun]
```

**Vista 2 — Sequence**

```text
Model
   │ propone: modelFinished | modelProposesToolCall | continuar razonando
   ▼
AgentLoop
   │ runTurn(state, execution, modelFinished, modelProposesToolCall)
   │ decide: WAITING_FOR_MODEL | WAITING_FOR_TOOL | COMPLETED
   │ emite: AgentEvent (TURN_CONTINUED | RUN_COMPLETED)
   ▼
[WAITING_FOR_TOOL queda sin resolver — Preview, ToolRuntime/PolicyEngine] / [AgentRun cerrado]
```

**Vista 3 — Pseudocódigo**

Ver §11: `runTurn` es la primera formalización ejecutable de "`AgentLoop` decide si otro turno de
razonamiento debe ocurrir".

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde CH-00.

```pseudocode
FUNCTION runTurn(
    state: AgentState,
    execution: ExecutionContext,
    modelFinished: Boolean,
    modelProposesToolCall: Boolean
) -> AgentState

    IF state.status == COMPLETED
        OR state.status == FAILED
        OR state.status == CANCELLED
        OR state.status == EXPIRED

        error: HarnessError = HarnessError(
            category = VALIDATION,
            code = "TURN_ON_TERMINAL_STATE",
            message = "runTurn fue invocada sobre un AgentRunStatus terminal",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW error
    END

    nextStatus: AgentRunStatus = WAITING_FOR_MODEL

    IF modelFinished
        nextStatus = COMPLETED
    ELSE IF modelProposesToolCall
        nextStatus = WAITING_FOR_TOOL
    END

    nextState: AgentState = AgentState(
        runId = state.runId,
        sessionId = state.sessionId,
        agentId = state.agentId,
        status = nextStatus,
        currentTurn = state.currentTurn + 1
    )

    resolvedEventType: AgentEventType = TURN_CONTINUED

    IF nextStatus == COMPLETED
        resolvedEventType = RUN_COMPLETED
    END

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = resolvedEventType,
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

`newEventId()` y `now()` son las mismas utilidades primitivas de CH-00 (no son entidades
arquitectónicas ni componentes — no requieren ficha ni registro).

Nótese lo que `runTurn` **no** hace: no verifica `execution.budget` (esa es la operational
continuation que Article IV asigna a `ExecutionController`, preview — ver §8/§18), no invoca
ningún `ToolRuntime.execute(...)` real para resolver `WAITING_FOR_TOOL` (Article VI, Execution
Rule 1: "`AgentLoop` no ejecuta directamente side effects"; Execution Rule 2: "las tools se
ejecutan exclusivamente mediante `ToolRuntime`"), y no le pregunta al modelo qué `AgentRunStatus`
asignar — `modelFinished`/`modelProposesToolCall` son señales de entrada que el modelo propone,
pero `nextStatus` lo decide, determinísticamente, `runTurn`.

## 12. Transiciones de Estado (State Transitions)

`AgentRunStatus` (§6, ahora C-013) define el lifecycle completo (Article V):

```text
CREATED
   → INITIALIZING

INITIALIZING
   → RUNNING
   → FAILED

RUNNING
   → WAITING_FOR_MODEL
   → WAITING_FOR_TOOL
   → WAITING_FOR_HUMAN
   → COMPLETED
   → FAILED
   → CANCELLED

WAITING_FOR_MODEL
   → COMPLETED         (runTurn: modelFinished)
   → WAITING_FOR_TOOL  (runTurn: modelProposesToolCall)
   → WAITING_FOR_MODEL (runTurn: ninguna de las anteriores — otro turno de razonamiento)

WAITING_FOR_TOOL
   → RUNNING   (Preview — ToolRuntime resuelve el ToolResult; no introducido en este capítulo)
   → FAILED

WAITING_FOR_HUMAN
   → approved  → RUNNING
   → rejected  → RUNNING / FAILED
   → expired   → EXPIRED
   → cancelled → CANCELLED
```

**Corrección respecto a CH-00**: la versión preliminar de esta tabla (CH-00 §12) enrutaba la
transición `expired` hacia `FAILED`, porque su `ENUM AgentRunStatus` de trabajo todavía no tenía un
estado `EXPIRED` propio. Al formalizar `AgentRunStatus` como contrato completo (C-013, fiel a
Article V), esta tabla corrige esa transición: `expired` ahora aterriza en `EXPIRED`, un estado
terminal distinto de `FAILED` — una aprobación humana que vence sin resolverse no es lo mismo que
una ejecución que falló por un error operacional, y agruparlas bajo el mismo estado le habría
ocultado esa distinción a cualquier componente futuro que audite el historial de un `AgentRun`.

El LLM no controla directamente esta máquina de estados (P-10): `runTurn` (§11) es quien decide
la transición, a partir de señales que el modelo propone (`modelFinished`,
`modelProposesToolCall`), nunca a partir de un valor de `AgentRunStatus` que el modelo asigne
directamente.

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6) clasifica también los fallos que introduce este capítulo:

```text
VALIDATION
    runTurn invocada sobre un AgentRunStatus terminal (COMPLETED/FAILED/CANCELLED/EXPIRED)
    → recoverable: FALSE, retryable: FALSE
    → código: TURN_ON_TERMINAL_STATE (ver §11)
```

`runTurn` nunca lanza un error genérico: siempre construye un `HarnessError` con `category`,
`recoverable` y `retryable` explícitos — mismo patrón que `governTurnContinuation` (CH-00 §11).

Lo que `runTurn` **deliberadamente no clasifica**: cualquier fallo de `category = BUDGET`
(`MAX_TURNS_EXCEEDED` y similares, ya definidos en CH-00) sigue siendo responsabilidad de la
operational continuation — no de `AgentLoop` — porque `AgentLoop.does_not_own` excluye
explícitamente esa decisión (ver §8). Este capítulo no reclasifica ni reimplementa esa semántica;
solo se abstiene de absorberla.

## 14. Eventos Producidos (Events Produced)

Este capítulo no agrega valores nuevos a `AgentEventType` — reutiliza el vocabulario que CH-00 ya
definió:

```text
TURN_CONTINUED    — AgentLoop autorizó continuar con otro turno de razonamiento (runTurn, §11)
RUN_COMPLETED     — AgentLoop determinó que el AgentRun terminó exitosamente (runTurn, §11)
```

`RUN_STARTED` y `RUN_FAILED` (CH-00) no se emiten desde `runTurn` en este capítulo: `RUN_STARTED`
pertenece al arranque de un `AgentRun` (todavía sin componente propio que lo orqueste) y
`RUN_FAILED` a un `HarnessError` no recuperable a nivel de todo el run (ver §13 — el error de
`runTurn` es de `category = VALIDATION`, no un fallo del run completo). Capítulos posteriores
podrán conectar ambos sin redefinir el envelope común `AgentEvent` (C-010).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

Este capítulo no implementa autorización todavía (no existe `PolicyEngine` — ver §9), y
`AgentLoop.does_not_own` lo declara explícitamente:

- **P-05 — Side effects pass through policy**: se preserva sin cambios. `runTurn` nunca ejecuta
  una tool call; solo transiciona a `WAITING_FOR_TOOL` y se detiene ahí.
- **P-13 — Authorization is deterministic and external to the LLM**: se preserva sin cambios.
  `modelProposesToolCall` es una señal de entrada, no una autorización — `AgentLoop` no la
  convierte en permiso, solo en un cambio de `AgentRunStatus` que dice "esto está esperando a
  alguien más".

`WAITING_FOR_TOOL` es, por diseño, un **handoff sin resolver** (§5): el punto exacto donde termina
la responsabilidad de `AgentLoop` y donde, cuando exista, empezará la de `PolicyEngine` +
`ToolRuntime`.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (REGLAS_LIBRO_AGENT_HARNESS(1).md §28):

```text
TEST RunTurnNeverTransitionsFromATerminalAgentRunStatus
TEST RunTurnNeverInvokesToolRuntimeOrPolicyEngineDirectly
TEST RunTurnAlwaysReturnsAnAgentStateWithIncrementedCurrentTurn
TEST RunTurnAlwaysEmitsAnAgentEventOnEveryTransition
TEST WaitingForToolIsAHandoffNotAnExecution
TEST AgentRunStatusExpiredIsDistinctFromFailed
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.1, después de CH-01)

Constitution
 ├── Article I    — Principles (P-01 .. P-15)
 ├── Article II   — Invariants (INV-01 .. INV-20)
 ├── Article III  — Component Sovereignty (AgentLoop: primer componente instanciado)
 └── Article IV   — Decision Ownership (en uso: AgentLoop.owns/does_not_own)

Contracts (registry/contracts.yaml)
 ├── C-001 AgentMessage        (CH-00)
 ├── C-002 AgentConfig         (CH-00)
 ├── C-003 AgentState          (CH-00)
 ├── C-004 ExecutionContext    (CH-00)
 ├── C-010 AgentEvent          (CH-00)
 ├── C-011 HarnessError        (CH-00)
 ├── C-012 ExecutionBudget     (CH-00)
 └── C-013 AgentRunStatus      (CH-01, nuevo — formaliza lo que CH-00 solo usaba por nombre)

Components (registry/components.yaml)
 └── CMP-001 AgentLoop         (CH-01, nuevo — primer componente del libro)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **`WAITING_FOR_TOOL` sin resolver**: `runTurn` transiciona a este estado y se detiene ahí a
  propósito. Resolverlo requiere `ToolCall`/`ToolResult`/`ToolRuntime` — fuera de alcance de este
  capítulo (deuda intencional hacia `CH-02`, ver §19).
- **Operational continuation (budget/cancelación)**: sigue sin componente propio.
  `governTurnContinuation` (CH-00) sigue siendo código sin dueño formal — este capítulo
  deliberadamente NO se lo asigna a `AgentLoop` (violaría Article IV) ni inventa
  `ExecutionController` solo para tener a quién asignárselo. Queda como deuda intencional
  explícita, no como una responsabilidad absorbida en silencio.
- **Autorización real**: `PolicyEngine` sigue sin existir; P-05/P-13 siguen siendo reglas
  declaradas, no reglas exigidas por código.
- **Invocación real del modelo**: `ModelGateway` no existe; `modelFinished`/`modelProposesToolCall`
  son señales de entrada asumidas, no producidas por ningún componente todavía.
- **Persistencia real de `AgentState`/`SessionState`**: sin cambios respecto a CH-00 —
  `SessionManager` no existe.
- **Human-in-the-loop implementado**: sin cambios respecto a CH-00 — solo el estado
  `WAITING_FOR_HUMAN` (contrato) existe, sin `HumanInteractionService`.
- **Reviewers plurales, evals, orquestación multi-agente y aprobación humana persistente del
  propio Book Harness**: explícitamente fuera de alcance de BH-v0.1 (igual que CH-00).

## 19. Siguiente Incremento (Next Increment)

El problema natural del próximo capítulo: ahora que `AgentLoop` puede transicionar a
`WAITING_FOR_TOOL` y detenerse ahí (§11), ¿quién resuelve ese punto — quién valida, autoriza y
ejecuta una tool call real, y quién le devuelve un `ToolResult` observable al ciclo? Eso requiere
introducir `ToolCall`/`ToolResult`/`ToolRuntime` (y, para que `ToolRuntime` tenga a quién pedirle
autorización, probablemente `PolicyEngine`) — el segundo y tercer componente de Article III que
dejarían de ser preview.

Ese capítulo (`CH-02`, fuera del alcance de esta ejecución) heredaría directamente la deuda
intencional de §18: `WAITING_FOR_TOOL` sin resolver. `next_chapter` queda en `null` en el
frontmatter de este capítulo porque, en este momento del libro, `CH-02` todavía no existe como
archivo — solo como el problema que motivará su escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de
> la secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco
> Iceberg / Bucles de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas,
> Forrester/Meadows), secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): sin un dueño explícito para "¿debe ocurrir otro turno?",
   cada implementación termina decidiéndolo de una manera distinta — algunas confían en que el
   modelo diga "ya terminé", otras cuentan turnos a mano, otras mezclan esa decisión con la del
   presupuesto — tres decisiones distintas resueltas por tres criterios distintos, ninguno
   declarado.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): sin un componente
   con fronteras explícitas, la decisión de continuación cognitiva tiende a absorber
   silenciosamente decisiones vecinas (presupuesto, autorización) solo porque están físicamente
   cerca en el código — exactamente lo que Article IV prohíbe — y sin un `AgentRunStatus`
   completo y registrado, cada punto de espera a mitad de un turno termina representado de forma
   ambigua.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `AgentLoop` (CMP-001) con una ficha que declara tanto lo que posee (`owns`) como lo que
   explícitamente NO posee (`does_not_own`) y formaliza `AgentRunStatus` (C-013) como contrato
   completo de once estados, corrigiendo la versión preliminar de CH-00.
4. **Modelos mentales** (= §4, Constitutional Impact): el Ownership Rule de Article IV — "ningún
   componente debe absorber silenciosamente decisiones que pertenecen a otro dominio".

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un componente nuevo se introduce sin declarar
  explícitamente su `does_not_own`, aumenta la probabilidad de que absorba silenciosamente la
  próxima decisión vecina "porque ya estaba ahí". Este capítulo corta esa espiral declarando el
  `does_not_own` de `AgentLoop` con el mismo peso que su `owns`.
- **Bucle de equilibrio (estabiliza):** `runTurn` (§11) rechaza con un `HarnessError` toda
  invocación sobre un `AgentRunStatus` terminal, en vez de permitir que un turno fantasma continúe
  silenciosamente después de que la ejecución ya cerró.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `AgentLoop` (CMP-001) declare su
`does_not_own` en el mismo momento en que se introduce — antes de que exista código que pueda
absorber silenciosamente la operational continuation o la autorización. Si esta frontera no se fija
aquí, el próximo componente que sí las posea tendría que arrancarle esa responsabilidad a
`AgentLoop` en vez de simplemente ocuparla.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado
> completo de esta sección (con ids estables para cada pregunta/tarjeta) vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida. Aquí se
> presenta en prosa, para lectura directa del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. ¿Qué decide `AgentLoop` cuando `runTurn` recibe `modelFinished = TRUE`, y a qué valor de
   `AgentRunStatus` transiciona la ejecución? *(cierra la pregunta guía 1)*
2. ¿A qué valor de `AgentRunStatus` transiciona `runTurn` cuando el modelo propone una tool call,
   y qué componente (todavía no introducido en este libro) es responsable de resolver ese estado?
   *(cierra la pregunta guía 2)*
3. Según Article IV, ¿qué decisión posee `AgentLoop` y qué decisión relacionada NO posee — y a qué
   componente, todavía sin introducir, pertenece esa segunda decisión? *(cierra la pregunta guía 3)*
4. ¿Qué valor agrega este capítulo al `ENUM AgentRunStatus` que la versión preliminar de CH-00 no
   tenía, y qué transición de la tabla de estados de CH-00 corrige exactamente? *(cierra la
   pregunta guía 4)*

### Explicar

1. `AgentLoop` posee la decisión de continuación cognitiva. Explica, como si hablaras con alguien
   sin contexto técnico, por qué NO posee la autorización de una tool call ni su ejecución
   concreta — ¿qué se rompería, en concreto, si `AgentLoop` empezara a ejecutar tools
   directamente "ya que de todos modos decide cuándo se piden"?
2. Usando el Ownership Rule de Article IV, explica por qué la verificación de `budget.maxTurns`
   que CH-00 ya introdujo NO se convierte automáticamente en una responsabilidad de `AgentLoop`
   solo porque `AgentLoop` ya existe como componente real — ¿a qué componente, todavía sin
   introducir en este libro, pertenece esa decisión?

### Conectar

1. Cada vez que `AgentLoop` transiciona el `AgentRunStatus` de una ejecución y emite un
   `AgentEvent`, ¿qué tres campos de `ExecutionContext` (introducido en CH-00) necesita leer para
   poblar el `runId`, el `sessionId` y el `traceId` de ese evento?

### Espaciar

Las tres tarjetas de repaso de este capítulo (`AgentRunStatus`, y dos sobre `AgentLoop` — su
`owns` y su `does_not_own`) entran hoy en `reviewStage = DAY_1`. Repásalas de nuevo al día 3, al
día 7 y al día 21 (curva de Ebbinghaus) — ver el apéndice de tarjetas al final del libro (edición
PDF) o `retrieval_set.flashcards` en `dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te
equivocaste, ese es precisamente el punto ciego que este método existe para revelar.
