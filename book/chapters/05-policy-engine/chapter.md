---
id: CH-05
title: "PolicyEngine y la Frontera de Autorización"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-005]
introduces_contracts: [C-014]
modifies_contracts: []
constitutional_articles: [P-05, P-13, INV-04, INV-06, INV-15, INV-18, INV-19, INV-20]
previous_chapter: CH-04
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH05
    text: |
      Al terminar este capítulo podrás distinguir, dentro de la pregunta "¿puede ocurrir esta
      acción?", qué tramo le pertenece en exclusiva al componente que evalúa autorización y qué
      tramos pertenecen a dominios distintos (ejecución de la acción ya aprobada, resolución de
      una aprobación humana pendiente, enforcement de presupuesto) que ya tienen o todavía no
      tienen componente propio — y podrás diseñar, para cualquier evaluación de autorización, un
      resultado de tres estados que nunca colapse en un simple sí/no y que deniegue por defecto
      cuando ningún criterio conocido aplica, en vez de permitir por accidente.
  skeleton:
    id: SK-CH05
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
    components_to_be_introduced: [CMP-005]
    contracts_to_be_introduced: [C-014]
  guiding_questions:
    - id: GQ-CH05-01
      text: |
        Cuando la ejecución controlada de una acción (ver dos capítulos atrás) recibe esa acción ya
        resuelta pero explícitamente no decide si está permitida, ¿quién evalúa esa autorización
        antes de que la ejecución ocurra, y qué debería pasar cuando ningún criterio conocido cubre
        el caso — permitirla por defecto o negarla por defecto?
      answered_by: RQ-CH05-01
    - id: GQ-CH05-02
      text: |
        Si una acción no es simplemente "permitida" o "denegada", sino que primero necesita que un
        humano la apruebe, ¿cómo se representa ese tercer resultado sin que quien lo produce
        necesite ya saber cómo se resuelve esa aprobación?
      answered_by: RQ-CH05-02
    - id: GQ-CH05-03
      text: |
        Para que una decisión de autorización se pueda auditar después de que ocurrió, ¿qué
        información mínima debería acompañar a ese resultado, más allá de un simple sí o no?
      answered_by: RQ-CH05-03
    - id: GQ-CH05-04
      text: |
        ¿Por qué el mismo componente que decide si una acción está permitida no debería, además,
        ejecutar esa acción, invocar al modelo, seleccionar qué información es relevante, o decidir
        si el turno debe continuar?
      answered_by: RQ-CH05-04
  systems_lens:
    iceberg_visible_fact: |
      Sin un dueño explícito para "¿puede ocurrir esta acción?", la autorización tiende a
      resolverse de dos formas igual de peligrosas: o se asume implícitamente que sí (nada la
      niega, así que ocurre), o se dispersa como verificaciones ad hoc en el mismo lugar donde la
      acción se ejecuta o donde el contexto se selecciona (ver seccion 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que, sin un componente con fronteras explícitas, la ausencia de
      una regla aplicable tiende a interpretarse como autorización implícita ("nadie dijo que no")
      en vez de como una señal para negar por defecto — y sin un resultado de tres estados, una
      acción que en realidad necesita aprobación humana termina forzada a la casilla más cercana
      (permitida o denegada), perdiendo la posibilidad real de pausar en vez de decidir (ver
      seccion 3, Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala el quinto componente real del libro, `PolicyEngine` (CMP-005), con una
      ficha que declara tanto lo que posee (`owns`: allow, deny, constraints, approval
      requirements, policy evaluation — cita literal de Article III) como lo que explícitamente NO
      posee (`does_not_own`: ejecutar la acción ya evaluada, invocar al modelo, seleccionar
      contexto, decidir continuación del turno, y resolver la aprobación humana que puede exigir)
      — y formaliza `PolicyDecision` (C-014), el primer contrato verdaderamente nuevo del libro,
      no reservado desde CH-01 (ver seccion 8, Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es P-13 ("Authorization is deterministic and
      external to the LLM") junto con INV-06 ("Todo side effect pasa por PolicyEngine"): la
      autorización nunca depende de que el modelo se comporte bien, y cuando el sistema no sabe
      qué decidir, la respuesta correcta es negar, nunca permitir (ver seccion 4, Impacto
      Constitucional).
    reinforcing_loop: |
      Cada vez que un componente nuevo se introduce sin declarar explícitamente su `does_not_own`,
      aumenta la probabilidad de que absorba silenciosamente la próxima decisión vecina "porque ya
      estaba ahí" — el mismo bucle que CH-01/CH-02/CH-03/CH-04 ya cortaron. Este capítulo lo repite
      para `PolicyEngine`, con una particularidad nueva: la tentación más fuerte no es que
      `PolicyEngine` invada a otro componente, sino que otro componente (`ToolRuntime`) absorba la
      autorización "ya que de todos modos va a ejecutar la acción" — la misma tentación que CH-02
      §8 ya anticipó y cerró desde el otro lado.
    balancing_loop: |
      `evaluatePolicyForToolCall` (seccion 11) es el mecanismo de equilibrio: cuando ninguna policy
      rule aplica, el resultado es `DENY` — nunca `ALLOW` por omisión, nunca una excepción sin
      clasificar — en vez de dejar que la ausencia de una regla se confunda con autorización.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `PolicyDecision.outcome` sea un `ENUM`
      de tres valores (`ALLOW`/`DENY`/`REQUIRE_APPROVAL`) en vez de un `Boolean`, combinado con que
      `evaluatePolicyForToolCall` deniegue por defecto cuando ninguna regla aplica. Si esta
      autorización colapsara a un booleano, o si la ausencia de regla se interpretara como
      permiso, cada capítulo futuro que dependa de `PolicyEngine` (la integración real con
      `ToolRuntime`, `HumanInteractionService`) heredaría un modelo de autorización incapaz de
      representar "todavía no" — solo "sí" o "no".
  recall_questions:
    - id: RQ-CH05-01
      text: |
        ¿Qué componente evalúa si un `ToolCall` ya resuelto puede ejecutarse, y qué contrato
        produce como resultado de esa evaluación?
    - id: RQ-CH05-02
      text: |
        ¿Cuáles son los tres valores posibles de `PolicyDecision.outcome`, y qué componente
        todavía sin introducir sería responsable de resolver el caso en el que ese valor es
        `REQUIRE_APPROVAL`?
    - id: RQ-CH05-03
      text: |
        ¿Qué campo de `PolicyDecision` registra la regla que motivó la decisión (INV-19), y qué
        ocurre con `outcome` cuando `evaluatePolicyForToolCall` no encuentra ninguna policy rule
        aplicable a un `ToolCall`?
    - id: RQ-CH05-04
      text: |
        Según Article IV, ¿qué decisión posee `PolicyEngine` y qué cuatro decisiones relacionadas
        NO posee — y a qué componentes, ya existentes o todavía sin introducir, pertenece cada
        una?
  explain_prompts:
    - id: EP-CH05-01
      text: |
        `PolicyEngine` posee decidir si una acción está permitida. Explica, como si hablaras con
        alguien sin contexto técnico, por qué NO posee ejecutar esa acción una vez que la permite
        — ¿qué se rompería, en concreto, si `PolicyEngine` empezara a ejecutar la acción
        directamente "ya que de todos modos acaba de decidir que está permitida"?
      target_entity: CMP-005
    - id: EP-CH05-02
      text: |
        `PolicyDecision.reason` reutiliza `HarnessError` (C-011) únicamente cuando
        `outcome = DENY`, nunca cuando `outcome = ALLOW` o `REQUIRE_APPROVAL`. Explica por qué una
        denegación se modela como un `HarnessError` (Article VII: "Policy denied → policy /
        non-retryable") pero un `REQUIRE_APPROVAL` no es, en sí mismo, un fallo — ¿qué perderíamos
        si tratáramos ambos casos de la misma forma?
      target_entity: C-014
  interleaved_questions:
    - id: IQ-CH05-01
      text: |
        `ToolRuntime` (CH-02) recibe un `ToolCall` ya resuelto pero, por su propio
        `does_not_own`, nunca evalúa si esa acción está autorizada. ¿Qué campo de `ToolCall`
        necesitaría leer quien evalúe la policy aplicable a esa acción para poblar
        `PolicyDecision.callId`, y qué correlación permite ese campo entre la `PolicyDecision`
        resultante y la tool call que la motivó?
      current_chapter_entities: [CMP-005, C-014]
      prior_chapter_entities: [CMP-002, C-008]
      prior_chapter: CH-02
    - id: IQ-CH05-02
      text: |
        `ContextEngine` (CH-04) asume que sus `candidates` ya llegaron autorizados para verse, sin
        verificarlo él mismo (su propio `does_not_own` lo declara explícitamente). ¿Qué `outcome`
        de la evaluación de este capítulo correspondería, conceptualmente, a negar la visibilidad
        de uno de esos candidatos, y por qué esa respuesta no obliga a `ContextEngine` a empezar a
        producir ese resultado él mismo?
      current_chapter_entities: [CMP-005, C-014]
      prior_chapter_entities: [CMP-004]
      prior_chapter: CH-04
  flashcards:
    - id: FC-CH05-01
      front: |
        ¿Qué posee `PolicyEngine` (Article III / Article IV), en una frase?
      back: |
        Allow, deny, constraints, approval requirements y policy evaluation — cita literal de
        Article III, sección "PolicyEngine": decidir si una acción ya resuelta puede ocurrir.
      source_entity: CMP-005
      chapter_introduced_in: CH-05
      review_stage: DAY_1
    - id: FC-CH05-02
      front: |
        ¿Qué NO posee `PolicyEngine`, y a qué componentes pertenecen esas decisiones?
      back: |
        Ejecutar la acción ya evaluada (`ToolRuntime`, ya existente), invocar al modelo
        (`ModelGateway`, ya existente), seleccionar contexto (`ContextEngine`, ya existente),
        decidir continuación del turno (`AgentLoop`, ya existente), resolver la aprobación humana
        (`HumanInteractionService`, preview) y enforcement de `ExecutionBudget`
        (`ExecutionController`, preview).
      source_entity: CMP-005
      chapter_introduced_in: CH-05
      review_stage: DAY_1
    - id: FC-CH05-03
      front: |
        ¿Qué campos tiene `PolicyDecision` (C-014), y qué representan?
      back: |
        `callId` (ToolCallId, qué `ToolCall` se evaluó), `outcome` (PolicyOutcome — ALLOW/DENY/
        REQUIRE_APPROVAL), `policyRuleId` (Text, qué regla motivó la decisión — INV-19),
        `reason` (Optional<HarnessError>, poblado solo cuando outcome = DENY) y `decidedAt`
        (Timestamp).
      source_entity: C-014
      chapter_introduced_in: CH-05
      review_stage: DAY_1
    - id: FC-CH05-04
      front: |
        ¿Por qué `PolicyDecision.outcome` es un `ENUM` de tres valores en vez de un `Boolean`, y
        qué ocurre cuando ninguna policy rule aplica a un `ToolCall`?
      back: |
        Un `Boolean` no puede representar "todavía no, necesita aprobación humana" — solo sí/no.
        Cuando ninguna regla aplica, `evaluatePolicyForToolCall` deniega por defecto
        (fail-closed, `outcome = DENY`) en vez de permitir por omisión o lanzar una excepción sin
        clasificar.
      source_entity: C-014
      chapter_introduced_in: CH-05
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH05-01
      recall_question: RQ-CH05-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH05-02
      recall_question: RQ-CH05-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH05-03
      recall_question: RQ-CH05-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH05-04
      recall_question: RQ-CH05-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 5 — PolicyEngine y la Frontera de Autorización

> **Regla constitucional (Article II, INV-06):** todo side effect pasa por `PolicyEngine`.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de
> saber cómo se llama el componente de este capítulo. El detalle estructurado de esta sección
> vive en `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, dentro de la pregunta "¿puede
ocurrir esta acción?", qué tramo le pertenece en exclusiva al componente que este capítulo
introduce y qué tramos pertenecen a dominios distintos (ejecución de la acción ya aprobada,
resolución de una aprobación humana pendiente, enforcement de presupuesto) que ya tienen o todavía
no tienen componente propio — y podrás diseñar, para cualquier evaluación de autorización, un
resultado de tres estados que nunca colapse en un simple sí/no y que deniegue por defecto cuando
ningún criterio conocido aplica, en vez de permitir por accidente.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e
introduce un contrato de datos (`PolicyDecision` — el primer id verdaderamente nuevo del libro, no
reservado desde CH-01) y el quinto componente de runtime del libro (`PolicyEngine`) — todavía sin
explicarlos, solo como mapa.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar
atrás; están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este
capítulo va a definir):

1. Cuando la ejecución controlada de una acción (ver dos capítulos atrás) recibe esa acción ya
   resuelta pero explícitamente no decide si está permitida, ¿quién evalúa esa autorización antes
   de que la ejecución ocurra, y qué debería pasar cuando ningún criterio conocido cubre el caso —
   permitirla por defecto o negarla por defecto?
2. Si una acción no es simplemente "permitida" o "denegada", sino que primero necesita que un
   humano la apruebe, ¿cómo se representa ese tercer resultado sin que quien lo produce necesite ya
   saber cómo se resuelve esa aprobación?
3. Para que una decisión de autorización se pueda auditar después de que ocurrió, ¿qué información
   mínima debería acompañar a ese resultado, más allá de un simple sí o no?
4. ¿Por qué el mismo componente que decide si una acción está permitida no debería, además,
   ejecutar esa acción, invocar al modelo, seleccionar qué información es relevante, o decidir si
   el turno debe continuar?

## 1. Arquitectura Actual (Current Architecture)

CH-00 dejó siete contratos de datos instalados y reservó cinco ids adicionales (`C-005`..`C-009`).
CH-01 agregó `AgentRunStatus` (C-013) y el primer componente de runtime, `AgentLoop` (CMP-001).
CH-02 resolvió `C-008`/`C-009` (`ToolCall`/`ToolResult`) junto con el segundo componente,
`ToolRuntime` (CMP-002). CH-03 resolvió `C-006`/`C-007` (`ModelRequest`/`ModelResponse`) junto con
el tercer componente, `ModelGateway` (CMP-003). CH-04 resolvió `C-005` (`ContextSnapshot`) junto con
el cuarto componente, `ContextEngine` (CMP-004) — y con eso, los cinco ids que CH-01 §7 dejó
reservados quedaron todos asignados.

Dos capítulos, de forma independiente, dejaron la misma pregunta abierta y apuntando al mismo
nombre. CH-02 §8 declaró, en el `does_not_own` de `ToolRuntime`, que "policy evaluation y
autorización de la acción" pertenecen a `PolicyEngine` — y su `executeToolCall` (CH-02 §11) recibe
`capabilityResolved`/`inputValid` como señales ya dadas, sin evaluar en ningún momento si la acción
está permitida. CH-04 §15 dedicó una sección completa a separar "¿es esto relevante?"
(`ContextEngine`, este componente) de "¿puede verse esto en absoluto?" (`PolicyEngine`, preview) —
y su `assembleContextSnapshot` asume, como precondición documentada, que `candidates` ya llegó
autorizado. Ambas deudas señalan al mismo componente todavía sin construir: Article IV lo nombra
como `PolicyEngine → May this action occur?`, y hasta este capítulo seguía siendo, literalmente,
solo esa línea en la tabla de Article III.

`ErrorCategory` (C-011, CH-00 §6) declara, desde la primera versión de la Constitution, un valor
`POLICY` — pero ningún componente del libro lo ha ejercitado todavía: de los diez valores de
`ErrorCategory`, hasta este capítulo se han ejercitado `VALIDATION`/`TOOL` (CH-02), `MODEL` (CH-03)
y `CONTEXT` (CH-04). `POLICY` sigue siendo un valor declarado sin ningún fallo real clasificado bajo
él. `AgentRunStatus` (C-013, CH-01) también declara, desde su primera versión, un estado
`WAITING_FOR_HUMAN` — y ese estado tampoco ha sido nunca el destino de una transición real: ningún
componente construido hasta ahora produce una señal que lo justifique.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas, "¿puede ocurrir esta acción?" tiende a resolverse de
dos formas, ambas peligrosas. La primera: la autorización se asume implícitamente — si nada la
niega explícitamente, la acción ocurre, exactamente lo que P-13 prohíbe ("el modelo nunca
constituye una fuente de verdad para autorización", pero tampoco lo hace la ausencia de una
verificación). La segunda: la autorización se dispersa como verificaciones ad hoc en el mismo lugar
donde una acción se ejecuta (dentro de `ToolRuntime`, violando su propio `does_not_own` de CH-02) o
donde el contexto se selecciona (dentro de `ContextEngine`, violando el suyo de CH-04) — cada
implementación decidiendo, con su propio criterio y en un lugar distinto, qué está permitido.

Un segundo problema, más sutil: incluso si alguna implementación evaluara autorización en un lugar
único, un resultado binario ("permitido" / "denegado") no puede representar un caso real y
frecuente — una acción que no está prohibida, pero que tampoco puede ejecutarse todavía porque
necesita que un humano la apruebe primero (Article II, INV-15). Forzar ese caso a la casilla más
cercana ("denegado, por ahora" o "permitido, y ya veremos") pierde información que el resto del
sistema necesita para actuar correctamente.

Necesitamos que "¿puede ocurrir esta acción?" tenga un dueño único y nombrado — que produzca un
resultado de tres estados, no dos; que registre qué regla motivó la decisión (para que sea
auditable después, INV-19); y que, cuando ningún criterio conocido cubra el caso, deniegue por
defecto en vez de permitir por omisión.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los trece contratos y los cuatro componentes que existen hasta este punto no bastan porque:

- `ToolRuntime` (CH-02) recibe `capabilityResolved`/`inputValid` como señales ya dadas y nunca
  evalúa si la acción que va a coordinar está autorizada — su propio `does_not_own` lo excluye
  explícitamente, pero sin un componente real que sí lo haga, INV-06 ("Todo side effect pasa por
  `PolicyEngine`") sigue siendo una regla declarada, no una regla exigida por código;
- `ContextEngine` (CH-04) asume que `candidates` ya llegó autorizado para verse, sin verificarlo —
  la misma deuda, aplicada a visibilidad de información en vez de a ejecución de acciones;
- `ErrorCategory.POLICY` (CH-00) sigue siendo un valor declarado sin ningún componente que
  clasifique un fallo real bajo esa categoría, y `AgentRunStatus.WAITING_FOR_HUMAN` (CH-01) sigue
  siendo un estado del lifecycle que ninguna transición real ha alcanzado todavía;
- nada impide que, sin un resultado de tres estados, una acción que en realidad necesita aprobación
  humana termine forzada a "permitida" (con el riesgo de que ocurra sin que nadie la revisó) o a
  "denegada" (perdiendo la posibilidad real de pausar y preguntar, en vez de simplemente rechazar) —
  Article II, INV-15 exige distinguir ambos casos, pero ningún contrato del libro puede
  representarlo todavía.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la
> secuencia `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una
> entidad que no haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT`
> registrado — **no magic entities**. Este capítulo aplica la misma disciplina de *ownership* que
> CH-01/CH-02/CH-03/CH-04 ya establecieron — con una particularidad: la tentación más fuerte que
> este capítulo debe cortar no es que `PolicyEngine` invada a otro componente, sino la inversa —
> que `ToolRuntime` (CH-02, ya construido) absorba la autorización "ya que de todos modos ejecuta
> la acción". Esa frontera ya quedó declarada desde el lado de `ToolRuntime` en CH-02 §8; este
> capítulo la cierra desde el lado de `PolicyEngine`, sin modificar `ToolRuntime` en absoluto.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-05   Side effects pass through policy.
           Primera vez que este principio tiene un componente real que lo ejecuta: hasta este
           capítulo, INV-06 estaba preservado solo porque ToolRuntime (CH-02) declaraba
           explícitamente que NO evaluaba policy — nadie la evaluaba en absoluto. Ahora existe
           PolicyEngine, aunque su integración real con ToolRuntime sigue siendo trabajo de un
           capítulo posterior (ver seccion 9/18).
    P-13   Authorization is deterministic and external to the LLM.
           evaluatePolicyForToolCall (seccion 11) es la primera formalización ejecutable de este
           principio: ninguna entrada del modelo participa en la evaluación, y el resultado es
           siempre determinístico dado el mismo ToolCall y ExecutionContext.

Invariants preserved
    INV-04   Todo ToolCall debe validarse antes de ejecutarse.
             Este capítulo añade una segunda forma de validación, distinta de la validación de
             schema que ToolRuntime ya posee (CH-02): la autorización. Ambas ocurren antes de
             Execute (Article VI), pero son decisiones de dominios distintos con dueños distintos.
    INV-06   Todo side effect pasa por PolicyEngine.
             Primera cita literal posible de este invariante: ya existe un PolicyEngine real que
             puede evaluar cualquier ToolCall antes de que ToolRuntime coordine su ejecución —
             aunque el cableado real entre ambos sigue siendo deuda intencional (ver seccion 18).
    INV-15   Una acción que requiere aprobación no puede ejecutarse antes de una resolución
             válida.
             PolicyDecision.outcome = REQUIRE_APPROVAL es la primera señal real del libro que
             podría justificar la transición AgentRunStatus.WAITING_FOR_HUMAN (declarada desde
             CH-01, nunca alcanzada) — este capítulo produce esa señal; resolverla sigue siendo
             trabajo de HumanInteractionService (preview, ver seccion 12/18).
    INV-18   Toda acción significativa produce un evento observable.
             evaluatePolicyForToolCall emite un AgentEvent (POLICY_EVALUATED) en cada evaluación —
             el quinto componente del libro que produce eventos en la práctica.
    INV-19   Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy
             relevante.
             PolicyDecision.policyRuleId es, literalmente, la "policy relevante" que este
             invariante exige poder trazar — la primera vez que el propio texto de INV-19 se
             materializa como un campo real de un contrato.
    INV-20   Todo error operacional pertenece a una categoría conocida.
             Cuando outcome = DENY, PolicyDecision.reason construye un HarnessError con
             category = POLICY — la primera vez que este valor de ErrorCategory (declarado desde
             CH-00) se ejercita en la práctica.

Component ownership changes
    CMP-005 PolicyEngine se introduce — registry/components.yaml pasa de 4 a 5 componentes.
    owns/does_not_own citados literalmente contra Article III (sección "PolicyEngine") y
    Article IV. registry/components.yaml de CMP-002 ToolRuntime NO se modifica: la frontera ya
    quedó declarada desde CH-02, este capítulo solo la ejercita desde el otro lado.

Lifecycle changes
    Ninguno sobre AgentRunStatus (C-013): esa máquina de estados sigue siendo propiedad exclusiva
    de AgentLoop (CH-01), y su tabla de transiciones no cambia aquí. PolicyDecision tampoco
    introduce ningún lifecycle propio (ver seccion 12) — pero por primera vez existe una señal
    real (outcome = REQUIRE_APPROVAL) que apunta hacia una transición del lifecycle que CH-01 ya
    había anticipado (WAITING_FOR_HUMAN) sin que ningún componente la produjera hasta ahora.

Security implications
    Este es, literalmente, el primer capítulo de seguridad ejecutable del libro: P-05/P-13 dejan
    de ser reglas declaradas sin enforcement y pasan a tener un componente real que las aplica.
    Ver seccion 15 para el análisis completo, incluyendo el diseño fail-closed (denegar por
    defecto cuando ninguna policy rule aplica).

Observability implications
    PolicyEngine es el quinto componente que emite AgentEvent en la práctica, extendiendo
    AgentEventType con UN solo valor nuevo (POLICY_EVALUATED) — a diferencia de CH-02/CH-03/CH-04,
    que agregaron dos valores cada uno (éxito/fallo). La razón se documenta en la seccion 14: a
    diferencia de ejecutar una tool call, invocar un modelo o ensamblar contexto, evaluar policy
    nunca "falla" en el sentido operacional — siempre produce un resultado válido (ALLOW, DENY o
    REQUIRE_APPROVAL), incluso cuando ninguna regla aplica (fail-closed, ver seccion 11).

Deterministic vs agentic boundary
    Article XII se refina una quinta vez a nivel de componente: PolicyEngine es, de los cinco
    componentes del libro, el que menos participación del modelo admite en absoluto — ni siquiera
    recibe contenido generado por el modelo como entrada (a diferencia de ToolRuntime, que sí
    recibe argumentos que el modelo ayudó a producir). Evalúa exclusivamente ToolCall y
    ExecutionContext, ambos ya resueltos determinísticamente por capítulos anteriores.
```

## 5. Conceptos Nuevos (New Concepts)

- **Policy Evaluation**: el tramo determinístico, exigido por INV-06 y P-05, en el que
  `PolicyEngine` decide si una acción ya resuelta (`ToolCall`) puede ocurrir — antes de que
  `ToolRuntime` (CH-02) llegue a coordinar su ejecución. Responsabilidad exclusiva de
  `PolicyEngine` (Article III, Article IV: "`PolicyEngine` → May this action occur?").
- **Approval Requirement**: el tercer resultado posible de una evaluación de policy, distinto de
  permitir y de denegar — la acción no está prohibida, pero tampoco puede ejecutarse todavía
  porque necesita que un humano la apruebe primero (INV-15). Este capítulo solo puede **expresar**
  este resultado (`PolicyOutcome.REQUIRE_APPROVAL`, seccion 6); resolverlo — representar la
  solicitud, persistirla, recibir la resolución humana y permitir que la ejecución se reanude —
  pertenece a `HumanInteractionService` (Article III, preview, no introducido en este capítulo).
- **Default Deny (Fail-Closed)**: la regla de diseño por la cual `evaluatePolicyForToolCall`
  (seccion 11) responde `DENY` cuando ninguna policy rule conocida aplica a un `ToolCall`, en vez
  de permitir la acción por defecto o lanzar una excepción sin clasificar. La ausencia de una
  regla aplicable nunca se interpreta como autorización implícita — el mismo principio que
  gobierna el diseño de cualquier sistema de autorización real (P-13).
- **Policy Rule** *(preview conceptual — no se introduce ningún `STRUCT Policy`/`Rule` en este
  capítulo)*: el criterio concreto contra el que se evalúa un `ToolCall`. Este capítulo trata "qué
  reglas existen y cómo se almacenan" como una pregunta ya resuelta externamente (primitivas
  asumidas en el pseudocódigo de la seccion 11, en el mismo espíritu que `compact(...)`/
  `estimateTokens(...)` en CH-04), no como un mecanismo propio con su propio contrato — el mismo
  tipo de restricción de alcance que CH-02 aplicó a `Capability`/`Tool` y CH-03 a la selección de
  provider.
- **Constraints** *(cita literal de Article III, no modelado como campo en v1)*: Article III
  incluye "constraints" entre lo que `PolicyEngine` posee — por ejemplo, permitir una acción solo
  bajo ciertas condiciones adicionales (un límite de monto, una redacción parcial del resultado).
  Este capítulo reconoce esa responsabilidad en prosa, pero `PolicyDecision` v1 no introduce un
  campo estructurado para expresarla — un resultado no modelado explícitamente en seccion 18, para
  no inflar el alcance decidido de este incremento (1 componente + 1 contrato).
- **Decision Ownership** *(Article IV, en uso desde CH-01, ahora aplicado a un quinto
  componente)*: `PolicyEngine` decide "¿puede ocurrir esta acción?"; explícitamente NO decide
  "¿cómo se ejecuta una acción ya aprobada?" (`ToolRuntime`, ya resuelto), "¿cómo se invoca el
  modelo?" (`ModelGateway`, ya resuelto), "¿qué debería saber el modelo?" (`ContextEngine`, ya
  resuelto), "¿debe ocurrir otro turno?" (`AgentLoop`, ya resuelto) ni "¿cómo se representa y
  resuelve una aprobación humana pendiente?" (`HumanInteractionService`, preview).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados de CH-00/CH-01/CH-02/CH-03/CH-04

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `AgentId`, `ToolCallId`, `Timestamp`, `ToolCall`,
`ExecutionContext`, `AgentEvent`, `HarnessError`.

### `AgentEventType` — extendido, sin redefinir `AgentEvent`

CH-04 extendió `AgentEventType` a diez valores (`RUN_STARTED`, `TURN_CONTINUED`, `RUN_COMPLETED`,
`RUN_FAILED`, `TOOL_CALL_COMPLETED`, `TOOL_CALL_FAILED`, `MODEL_RESPONSE_RECEIVED`,
`MODEL_INVOCATION_FAILED`, `CONTEXT_SNAPSHOT_ASSEMBLED`, `CONTEXT_SNAPSHOT_FAILED`), sin contrato
`C-XXX` propio. Este capítulo agrega un único valor nuevo — no dos, a diferencia de CH-02/CH-03/
CH-04 (ver seccion 14 para la razón):

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
END
```

`AgentEvent` (C-010) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — solo el rango de
valores permitido para `eventType` crece, igual que en CH-01, CH-02, CH-03 y CH-04.

### `PolicyOutcome` — el resultado de tres estados (sin `C-XXX` propio)

```pseudocode
ENUM PolicyOutcome
    ALLOW
    DENY
    REQUIRE_APPROVAL
END
```

Tres valores, deliberadamente, no dos: un `Boolean` solo puede representar "sí" o "no", y no puede
expresar "todavía no, requiere aprobación humana" (INV-15). `PolicyOutcome` vive embebido dentro de
`PolicyDecision`, sin contrato `C-XXX` propio — el mismo patrón que `ContextBlock` (CH-04) o
`RawToolCallProposal` (CH-03): un tipo real, con `ENUM` propio, que ningún capítulo registra como
contrato independiente.

### `PolicyDecision` — el resultado normalizado, trazable, de evaluar un `ToolCall`

```pseudocode
STRUCT PolicyDecision
    callId: ToolCallId
    outcome: PolicyOutcome
    policyRuleId: Text
    reason: Optional<HarnessError>
    decidedAt: Timestamp
END
```

`callId` correlaciona esta decisión con el `ToolCall` (C-008, CH-02) que la motivó — el mismo
patrón de correlación que `ToolResult.callId` ya estableció en CH-02. `policyRuleId` es la
materialización literal de INV-19 ("toda decisión crítica debe poder trazarse hasta su actor,
contexto y policy relevante"): siempre tiene un valor, incluso cuando ninguna regla real aplicó
(seccion 11 documenta el valor centinela que usa ese caso). `reason` reutiliza `HarnessError`
(C-011, CH-00) — pero, a diferencia de `ToolResult.error` (CH-02), que se puebla en **todo** fallo,
aquí se puebla únicamente cuando `outcome = DENY`: un `REQUIRE_APPROVAL` no es un fallo (seccion
13), así que no construye ningún `HarnessError`.

**Unchanged / Not yet introduced**: ningún `STRUCT Policy`/`Rule` que declare cómo se almacenan o
componen las policy rules reales, ningún campo que exprese `constraints` (seccion 5), y ningún
`INTERFACE PolicyEngine` con múltiples `IMPLEMENTATION` — este capítulo introduce exactamente el
contrato que el encargo de este incremento fija: `C-014`, el primer id verdaderamente nuevo del
libro (no reservado desde CH-01 §7, a diferencia de `C-005`..`C-013`).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía (formalizar
`PolicyEngine` como interfaz con múltiples `IMPLEMENTATION` — por ejemplo, distintos motores de
reglas — queda para cuando este libro necesite modelar más de un mecanismo real de policy). Introduce
un contrato de datos, registrado en `registry/contracts.yaml`:

```text
ID:                     C-014
Name:                   PolicyDecision
Version:                v1
Introduced In:          CH-05
Current Definition:     STRUCT PolicyDecision (ver §6)
Used By:                [CMP-005]
Modified By:            []
Constitutional Impact:  [P-05, P-13, INV-06, INV-15, INV-19]
```

`C-014` es el primer id de contrato que este libro asigna sin que estuviera reservado desde CH-01
§7 (`C-005`..`C-013` ya estaban todos asignados al cierre de CH-04) — el correlativo simplemente
continúa.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el quinto componente de runtime del libro:

```pseudocode
COMPONENT PolicyEngine
    consumes: ExecutionContext, ToolCall
    produces: PolicyDecision, AgentEvent, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Article III (sección "PolicyEngine"):

```text
COMPONENT: PolicyEngine

Responsibility:
    Evaluar si una acción ya resuelta (ToolCall) puede ocurrir, produciendo una PolicyDecision
    determinística de tres resultados posibles (allow, deny, require_approval) — con la regla
    aplicable y el ToolCall evaluado siempre trazables — sin ejecutar la acción, sin invocar al
    modelo, sin seleccionar contexto, sin decidir continuación del turno y sin resolver ella
    misma la aprobación humana cuando la exige.

Consumes:
    C-004 ExecutionContext, C-008 ToolCall

Depends on:
    (ninguno todavía — HumanInteractionService y ExecutionController son Preview, no introducidos
    en este capítulo; ver seccion 9)

Produces:
    C-014 PolicyDecision, C-010 AgentEvent (POLICY_EVALUATED),
    C-011 HarnessError (embebido en una PolicyDecision con outcome = DENY)

Owns (Article III, cita literal):
    - allow
    - deny
    - constraints
    - approval requirements
    - policy evaluation

Does NOT own (Article IV — declarado con el mismo peso que Owns):
    - ejecutar la acción ya evaluada (ToolRuntime, CMP-002, ya introducido en CH-02 — Article IV:
      "ToolRuntime → How should an approved action be executed?")
    - invocar al modelo seleccionado (ModelGateway, CMP-003, ya introducido en CH-03)
    - seleccionar/rankear/componer contexto (ContextEngine, CMP-004, ya introducido en CH-04)
    - decidir si otro turno de razonamiento debe ocurrir (AgentLoop, CMP-001, ya introducido en
      CH-01)
    - representar, persistir y resolver la aprobación humana cuando outcome = REQUIRE_APPROVAL
      (HumanInteractionService, Article III — no introducido en este capítulo; INV-15 exige que
      la acción no se ejecute antes de una resolución válida, pero resolver esa aprobación no es
      trabajo de PolicyEngine)
    - enforcement de ExecutionBudget (ExecutionController, Article III — no introducido en este
      capítulo)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con una
particularidad respecto a CH-01/CH-02/CH-03/CH-04: tres de las cinco exclusiones ya no son
"preview, todavía sin componente", sino fronteras contra componentes reales que ya existen
(`ToolRuntime`, `ModelGateway`, `ContextEngine`, `AgentLoop`). `PolicyEngine` es el componente del
libro con más vecinos ya construidos en el momento de su introducción.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
PolicyEngine
    consumes → ExecutionContext, ToolCall
    produces → PolicyDecision, AgentEvent, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`PolicyEngine` no depende hoy de ningún otro componente registrado. En prosa (nunca dentro de un
bloque `pseudocode`, per `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las
dependencias futuras que capítulos posteriores agregarán son:

| Componente futuro (Preview — no introducido en este capítulo) | Qué le daría a `PolicyEngine` |
|---|---|
| `HumanInteractionService` | la resolución real de una `PolicyDecision` con `outcome = REQUIRE_APPROVAL` |
| `ExecutionController` | el enforcement de `ExecutionBudget`, distinto de la evaluación de policy |
| `CapabilityRegistry` | metadata real de la capability solicitada (p. ej. su nivel de riesgo declarado), que hoy `matchPolicyRule` asume resuelta implícitamente |

`ToolRuntime` (CMP-002, ya existente) sería, en la práctica, quien invoque a `PolicyEngine` antes de
llegar a `Execute` (Article VI: `... beforeToolCall → Policy Evaluation → Authorization → Human
Approval? → Execution Budget → Sandbox → Execute ...`) — pero esa relación es la inversa de una
`dependency` en el sentido de `registry/components.yaml` (`ToolRuntime` dependería de
`PolicyEngine`, no al revés), y ese cableado formal (agregar `CMP-005` a
`ToolRuntime.dependencies`, y que `executeToolCall` invoque realmente a `evaluatePolicyForToolCall`
antes de coordinar la ejecución) es, explícitamente, trabajo de un capítulo posterior — el mismo
patrón que CH-02, CH-03 y CH-04 ya establecieron para sus propias relaciones inversas.
`book/chapters/02-tool-runtime/chapter.md` no se modifica para reflejarlo todavía (ni su cuerpo ni
su ficha de `CMP-002` en `registry/components.yaml`), y `registry/contracts.yaml` no incluye
`C-008` en ningún `modifies_contracts` de este capítulo: `ToolCall` no cambia aquí. El pseudocódigo
de la seccion 11 muestra a `PolicyEngine` evaluando un `ToolCall` de forma completamente autónoma —
sin necesitar que `ToolRuntime` cambie una sola línea para que este capítulo sea correcto.

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[ToolRuntime — CH-02, conceptual, todavía no cablea esta llamada] → PolicyEngine →
[HumanInteractionService — Preview, no introducido, solo si outcome = REQUIRE_APPROVAL]
```

**Vista 2 — Sequence**

```text
ToolCall
   │ (intención ya resuelta desde CH-02, evaluada por PolicyEngine antes de Execute)
   ▼
PolicyEngine
   │ evaluatePolicyForToolCall(call, execution, agentId)
   │ ¿existe una policy rule aplicable a este ToolCall?
   │     no  → outcome = DENY (fail-closed, HarnessError NO_APPLICABLE_POLICY_RULE)
   │     sí  → ¿la regla aplicable permite la acción?
   │             no  → outcome = DENY (HarnessError POLICY_DENIED)
   │             sí  → ¿la regla aplicable exige aprobación humana?
   │                     sí → outcome = REQUIRE_APPROVAL
   │                     no → outcome = ALLOW
   │ construye PolicyDecision (callId, outcome, policyRuleId, reason, decidedAt)
   │ emite: AgentEvent (POLICY_EVALUATED)
   ▼
PolicyDecision
   │
   ▼
[ToolRuntime retomaría la coordinación de Execute solo si outcome = ALLOW; si outcome =
REQUIRE_APPROVAL, HumanInteractionService resolvería primero — Preview, cableado formal de un
capítulo posterior, ver seccion 9/18]
```

**Vista 3 — Pseudocódigo**

Ver §11: `evaluatePolicyForToolCall` es la primera formalización ejecutable de "`PolicyEngine`
decide si una acción puede ocurrir", construida exclusivamente a partir de material que ya existe
(`ToolCall` desde CH-02, `ExecutionContext` desde CH-00) — sin necesitar que `ToolRuntime` cambie.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde
CH-00/CH-01/CH-02/CH-03/CH-04.

```pseudocode
FUNCTION evaluatePolicyForToolCall(
    call: ToolCall,
    execution: ExecutionContext,
    agentId: AgentId
) -> PolicyDecision

    ruleFound: Boolean = policyRuleFound(call, execution)
    matchedRuleId: Text = "DEFAULT_DENY_NO_MATCHING_RULE"
    outcome: PolicyOutcome = DENY
    reason: HarnessError = HarnessError(
        category = POLICY,
        code = "NO_APPLICABLE_POLICY_RULE",
        message = "Ninguna policy rule aplica a este ToolCall; PolicyEngine deniega por defecto (fail-closed)",
        recoverable = TRUE,
        retryable = FALSE,
        metadata = {}
    )

    IF ruleFound
        matchedRuleId = matchPolicyRule(call, execution)

        IF NOT policyRuleAllows(matchedRuleId, call, execution)
            outcome = DENY
            reason = HarnessError(
                category = POLICY,
                code = "POLICY_DENIED",
                message = "La policy rule aplicable denegó esta acción",
                recoverable = FALSE,
                retryable = FALSE,
                metadata = {}
            )
        ELSE IF policyRuleRequiresApproval(matchedRuleId, call, execution)
            outcome = REQUIRE_APPROVAL
            reason = NULL
        ELSE
            outcome = ALLOW
            reason = NULL
        END
    END

    decision: PolicyDecision = PolicyDecision(
        callId = call.id,
        outcome = outcome,
        policyRuleId = matchedRuleId,
        reason = reason,
        decidedAt = now()
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = POLICY_EVALUATED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = decision
    )

    RETURN decision
END
```

`newEventId()` y `now()` son las mismas primitivas de CH-00/CH-01/CH-02/CH-03/CH-04.
`policyRuleFound(...)`, `matchPolicyRule(...)`, `policyRuleAllows(...)` y
`policyRuleRequiresApproval(...)` son primitivas nuevas de este capítulo, en el mismo espíritu que
`compact(...)`/`estimateTokens(...)` de CH-04: funciones deterministas ya asumidas, no entidades
arquitectónicas, sin ficha ni registro propio — este capítulo no modela cómo se almacenan o
componen las policy rules reales (seccion 5, "Policy Rule"); son primitivas de infraestructura que
cualquier implementación real de `PolicyEngine` debe proveer.

`call` y `execution` son el único material de entrada, y son, deliberadamente, material que ya
existe desde CH-02/CH-00 (a diferencia de `capabilityResolved` en CH-02 o `providerFinished` en
CH-03, que eran señales asumidas de un componente todavía sin construir) — porque "policy
evaluation" es, literalmente, lo que `PolicyEngine` posee (Article III): no delega esa decisión a
ninguna señal externa, la ejecuta.

Nótese el orden de las comprobaciones: primero se decide `ruleFound` (fail-closed si es `FALSE`,
sin evaluar nada más); solo si una regla aplica se pregunta si permite la acción; solo si la
permite se pregunta si exige aprobación. Este orden nunca se invierte — permitir primero y negar
después dejaría una ventana, aunque fuera momentánea en el pseudocódigo, en la que una acción sin
regla aplicable pareciera autorizada.

Nótese también lo que `evaluatePolicyForToolCall` **no** hace: no ejecuta ninguna acción (Article
IV, "`ToolRuntime` → How should an approved action be executed?" sigue sin respuesta aquí), no
invoca ningún modelo, no selecciona contexto, no decide ningún `AgentRunStatus` (Article IV,
"`AgentLoop` → Should another reasoning turn occur?" tampoco), y — cuando `outcome =
REQUIRE_APPROVAL` — no representa, persiste ni resuelve esa aprobación de ninguna forma: se limita
a producir la señal (`HumanInteractionService`, preview, ver seccion 15).

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013): esa máquina de estados sigue
siendo propiedad exclusiva de `AgentLoop` (CH-01 §12), y su tabla de transiciones no cambia aquí.

`evaluatePolicyForToolCall` (§11) sí atraviesa un camino implícito con tres desenlaces — pero
deliberadamente **no** se formaliza como un nuevo contrato de lifecycle en este capítulo (eso
introduciría una segunda entidad nueva, fuera del alcance decidido para este capítulo):

```text
ToolCall recibido
   → ninguna policy rule aplica            → PolicyDecision (outcome = DENY,
                                               policyRuleId = "DEFAULT_DENY_NO_MATCHING_RULE")
   → regla aplica y deniega la acción      → PolicyDecision (outcome = DENY,
                                               reason.code = "POLICY_DENIED")
   → regla aplica, permite, exige aprobación → PolicyDecision (outcome = REQUIRE_APPROVAL)
   → regla aplica, permite sin exigir aprobación → PolicyDecision (outcome = ALLOW)
```

**Lo que este capítulo explícitamente no cierra**: `AgentRunStatus.WAITING_FOR_HUMAN` (C-013,
declarado desde CH-01 §6) sigue sin ser el destino de ninguna transición real. Este capítulo
produce, por primera vez, una señal (`PolicyDecision.outcome = REQUIRE_APPROVAL`) que justificaría
esa transición — pero decidir que `AgentLoop` debe transicionar a `WAITING_FOR_HUMAN` cuando recibe
esa señal, y que algo debe eventualmente sacar la ejecución de ese estado, sigue siendo trabajo de
un capítulo posterior que cablee `PolicyEngine` con `AgentLoop` y con `HumanInteractionService` (ver
seccion 18/19). `book/chapters/01-agent-loop/chapter.md` no se modifica para reflejarlo todavía.

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6) clasifica también los fallos que introduce este capítulo,
fiel a los `Failure Examples` de `constitution/ARCHITECTURE_CONSTITUTION.md` Article VII (que cita
literalmente: "Policy denied → policy / non-retryable"):

```text
POLICY
    NO_APPLICABLE_POLICY_RULE   — ninguna policy rule conocida aplica a este ToolCall; PolicyEngine
                                   deniega por defecto (fail-closed) en vez de permitir por omisión
        → recoverable: TRUE, retryable: FALSE
    POLICY_DENIED                — una policy rule aplicable denegó explícitamente la acción
        → recoverable: FALSE, retryable: FALSE
```

Este es el primer fallo real del libro clasificado bajo `category = POLICY` — un valor de
`ErrorCategory` declarado desde CH-00 §6 que ningún componente había ejercitado hasta este
capítulo. `NO_APPLICABLE_POLICY_RULE` es `recoverable = TRUE` (el problema es corregible —
agregar la policy rule que faltaba) pero `retryable = FALSE` (reintentar exactamente el mismo
`ToolCall` sin cambiar las reglas fallaría de forma idéntica). `POLICY_DENIED` es
`recoverable = FALSE, retryable = FALSE`: una denegación explícita no es un problema transitorio.

**La distinción más importante de esta sección**: `PolicyDecision.reason` (un `HarnessError`) solo
se construye cuando `outcome = DENY`. Un `outcome = REQUIRE_APPROVAL` **no es un fallo** — es una
evaluación de policy completamente exitosa que produjo un resultado distinto de permitir o denegar;
tratarlo como un `HarnessError` confundiría "la acción todavía no puede ejecutarse, pero podría"
con "la acción no puede ejecutarse, punto" (ver seccion 14 para la misma distinción aplicada a los
eventos que este capítulo produce).

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo de `category = BUDGET`
(presupuesto agotado) sigue sin ser responsabilidad de `PolicyEngine` — su propio `does_not_own`
(seccion 8) excluye explícitamente esa decisión (`ExecutionController`, preview).

## 14. Eventos Producidos (Events Produced)

Este capítulo agrega un único valor a `AgentEventType` (seccion 6) — no dos, a diferencia de
CH-02/CH-03/CH-04:

```text
POLICY_EVALUATED   — PolicyEngine completó la evaluación de un ToolCall y produjo una
                      PolicyDecision (ALLOW, DENY o REQUIRE_APPROVAL) — evaluatePolicyForToolCall,
                      §11
```

**Por qué solo un valor, y no un par éxito/fallo.** `ToolRuntime` (CH-02), `ModelGateway` (CH-03) y
`ContextEngine` (CH-04) pueden, cada uno, no completar su trabajo — una capability sin resolver, un
proveedor inalcanzable, ningún candidato que quepa en el presupuesto — y ese "no completar" es,
genuinamente, un fallo operacional distinto de su resultado exitoso. `evaluatePolicyForToolCall` no
tiene ese segundo camino: dado cualquier `ToolCall` y `ExecutionContext` válidos, **siempre**
produce una `PolicyDecision` — incluso cuando ninguna policy rule aplica, el resultado es
`DENY` (fail-closed, seccion 11), no una excepción sin resolver. Por eso `POLICY_EVALUATED` cubre
los tres resultados posibles: emitir un evento distinto para `DENY` confundiría "la evaluación
falló" con "la evaluación tuvo éxito y el resultado fue denegar" — exactamente la misma distinción
que la seccion 13 ya trazó para `HarnessError`.

`RUN_STARTED`, `TURN_CONTINUED`, `RUN_COMPLETED`, `RUN_FAILED` (CH-00/CH-01),
`TOOL_CALL_COMPLETED`/`TOOL_CALL_FAILED` (CH-02), `MODEL_RESPONSE_RECEIVED`/
`MODEL_INVOCATION_FAILED` (CH-03) y `CONTEXT_SNAPSHOT_ASSEMBLED`/`CONTEXT_SNAPSHOT_FAILED` (CH-04)
no se emiten desde `evaluatePolicyForToolCall`: pertenecen a dominios distintos. Un capítulo
posterior que conecte los cinco extremos (ver seccion 18/19) podrá correlacionar un
`POLICY_EVALUATED` con el siguiente `TOOL_CALL_COMPLETED`/`TOOL_CALL_FAILED` sin redefinir el
envelope común `AgentEvent` (C-010).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

Este es, de los cinco capítulos reales del libro, el que más directamente materializa Article I
(P-05, P-13) y Article II (INV-06) como código ejecutable en vez de como reglas declaradas sin
enforcement.

**Fail-closed, no fail-open.** La decisión de diseño central de `evaluatePolicyForToolCall` (§11)
es que la ausencia de una policy rule aplicable produzca `DENY`, nunca `ALLOW`. Esto es
deliberado y merece explicarse: un sistema de autorización que "permite por defecto cuando no sabe
qué hacer" degrada silenciosamente hacia "todo está permitido" a medida que aparecen casos nuevos
que ninguna regla existente cubre todavía — exactamente lo que P-13 prohíbe (la autorización nunca
puede depender de que alguien, humano o modelo, se acuerde de escribir la regla correcta a tiempo).
Negar por defecto convierte cada caso sin cubrir en un fallo visible y clasificado
(`NO_APPLICABLE_POLICY_RULE`, categoría `POLICY`) en vez de en una brecha silenciosa.

**Lo que este capítulo NO implementa todavía.** `evaluatePolicyForToolCall` modela únicamente el
tramo "Policy Evaluation → Authorization" del pipeline completo de Article VI (`Tool Intent →
Resolve Capability → Validate Schema → beforeToolCall → Policy Evaluation → Authorization → Human
Approval? → Execution Budget → Sandbox → Execute → afterToolCall → ToolResult → Observation`):

- **Resolve Capability / Validate Schema / beforeToolCall / afterToolCall**: siguen siendo,
  exactamente como en CH-02, responsabilidad exclusiva de `ToolRuntime` — este capítulo no las
  toca ni las duplica.
- **Human Approval?**: `PolicyDecision.outcome = REQUIRE_APPROVAL` es la señal, pero
  `PolicyEngine` no representa la solicitud humana, no la persiste, no espera una resolución y no
  reanuda nada — eso pertenece íntegramente a `HumanInteractionService` (Article III, preview).
- **Execution Budget**: no hay `ExecutionController` todavía. `evaluatePolicyForToolCall` no
  verifica ningún campo de `execution.budget` — mismo patrón que los cuatro capítulos anteriores
  ya establecieron para sus propias operational continuations.
- **Sandbox / Execute**: no modelado en este capítulo — coordinar la ejecución real de la acción
  ya autorizada sigue siendo, íntegramente, trabajo de `ToolRuntime` (CH-02), sin cambios.
- **El cableado real `ToolRuntime → PolicyEngine`**: `ToolRuntime.executeToolCall` (CH-02 §11)
  todavía no invoca `evaluatePolicyForToolCall` en ningún punto — este capítulo deja a
  `PolicyEngine` capaz de evaluar cualquier `ToolCall` de forma autónoma, pero la integración real
  (que `ToolRuntime` la invoque antes de `Execute`, y que un `outcome = DENY` o
  `REQUIRE_APPROVAL` efectivamente detenga la ejecución) es, explícitamente, trabajo de un
  capítulo posterior (ver seccion 9/18).

`PolicyDecision` es, por diseño, la forma en que `PolicyEngine` comunica el resultado de este
tramo parcial — nunca una afirmación de que el pipeline completo de Article VI ya está enforced de
punta a punta.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST EvaluatePolicyForToolCallDeniesByDefaultWhenNoRuleApplies
TEST EvaluatePolicyForToolCallNeverReturnsAllowWithoutAMatchingRuleThatPermits
TEST EvaluatePolicyForToolCallOutcomeIsNeverABooleanCollapse
TEST EvaluatePolicyForToolCallNeverInvokesToolRuntimeModelGatewayContextEngineOrAgentLoopDirectly
TEST EvaluatePolicyForToolCallAlwaysReturnsAPolicyDecisionCorrelatedByCallId
TEST EvaluatePolicyForToolCallAlwaysEmitsAnAgentEventRegardlessOfOutcome
TEST PolicyDecisionReasonIsPopulatedOnlyWhenOutcomeIsDeny
TEST PolicyDecisionPolicyRuleIdIsNeverEmptyEvenOnDefaultDeny
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.1, después de CH-05)

Constitution
 ├── Article I    — Principles (P-01 .. P-15)
 ├── Article II   — Invariants (INV-01 .. INV-20)
 ├── Article III  — Component Sovereignty (AgentLoop, ToolRuntime, ModelGateway, ContextEngine,
 │                  PolicyEngine: cinco componentes instanciados)
 ├── Article IV   — Decision Ownership (en uso: los cinco componentes declaran owns/does_not_own)
 ├── Article VI   — Execution Constitution (tramo Policy Evaluation → Authorization modelado;
 │                  Human Approval? .. Sandbox sigue sin componente)
 └── Article VII  — Failure Constitution (ErrorCategory.POLICY ejercitado por primera vez)

Contracts (registry/contracts.yaml)
 ├── C-001 AgentMessage        (CH-00)
 ├── C-002 AgentConfig         (CH-00)
 ├── C-003 AgentState          (CH-00)
 ├── C-004 ExecutionContext    (CH-00 — consumido ahora también por CMP-005)
 ├── C-005 ContextSnapshot     (CH-04)
 ├── C-006 ModelRequest        (CH-03)
 ├── C-007 ModelResponse       (CH-03)
 ├── C-008 ToolCall            (CH-02 — consumido ahora también por CMP-005)
 ├── C-009 ToolResult          (CH-02)
 ├── C-010 AgentEvent          (CH-00 — producido ahora también por CMP-005)
 ├── C-011 HarnessError        (CH-00 — producido ahora también por CMP-005)
 ├── C-012 ExecutionBudget     (CH-00)
 ├── C-013 AgentRunStatus      (CH-01)
 └── C-014 PolicyDecision      (CH-05, nuevo — primer id no reservado desde CH-01 §7)

Components (registry/components.yaml)
 ├── CMP-001 AgentLoop         (CH-01)
 ├── CMP-002 ToolRuntime       (CH-02)
 ├── CMP-003 ModelGateway      (CH-03)
 ├── CMP-004 ContextEngine     (CH-04)
 └── CMP-005 PolicyEngine      (CH-05, nuevo — quinto componente del libro)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado formal `ToolRuntime ↔ PolicyEngine`**: `ToolRuntime.executeToolCall` (CH-02 §11)
  no invoca `evaluatePolicyForToolCall` en ningún punto — `ToolRuntime.dependencies` no agrega
  `CMP-005`, y `registry/components.yaml` de `CMP-002` no se modifica en este capítulo. Ese
  cableado, y la decisión de qué hace exactamente `ToolRuntime` cuando recibe un
  `outcome = DENY` o `REQUIRE_APPROVAL`, es trabajo de un capítulo posterior — el mismo patrón de
  deuda intencional que `ContextSnapshot → ModelRequest` (CH-04) o `RawToolCallProposal →
  ToolCall` (CH-03).
- **`HumanInteractionService` y la resolución real de `REQUIRE_APPROVAL`**: este capítulo produce
  la señal; representar la solicitud humana, persistirla, transicionar `AgentRunStatus` a
  `WAITING_FOR_HUMAN` (declarado desde CH-01, nunca alcanzado), recibir la resolución y permitir
  que la ejecución se reanude sigue sin componente propio.
- **`ExecutionController` y el enforcement real de `ExecutionBudget`**: sin cambios respecto a
  CH-01/CH-02/CH-03/CH-04 — `evaluatePolicyForToolCall` no verifica ningún campo de
  `execution.budget`.
- **`constraints` como campo estructurado de `PolicyDecision`**: Article III incluye "constraints"
  entre lo que `PolicyEngine` posee (seccion 5), pero `PolicyDecision` v1 no modela cómo expresar
  una autorización condicional (permitida solo bajo ciertos límites adicionales) — una v2 futura
  de este contrato podría agregar ese campo, declarándolo explícitamente en `modifies_contracts`
  del capítulo que lo haga.
- **Almacenamiento y composición real de policy rules**: ningún `STRUCT Policy`/`Rule` se
  introduce; `matchPolicyRule`/`policyRuleAllows`/`policyRuleRequiresApproval` (§11) son
  primitivas asumidas, no un mecanismo modelado — el mismo tipo de restricción de alcance que
  CH-02 aplicó a `Capability`/`Tool`.
- **La visibilidad de `candidates` en `ContextEngine` (CH-04 §15)**: este capítulo deja a
  `PolicyEngine` capaz, en principio, de evaluar cualquier `ToolCall` — pero no introduce ningún
  mecanismo para que `ContextEngine` consulte a `PolicyEngine` antes de incluir un candidato en un
  `ContextSnapshot`. Esa integración, distinta de la de `ToolRuntime`, sigue siendo trabajo futuro.
- **`CapabilityRegistry`, Provider Adapters reales, streaming real**: deuda intencional heredada de
  CH-02/CH-03/CH-04, sin cambios en este capítulo.
- **Persistencia real de `AgentState`/`SessionState`, reviewers plurales, evals y orquestación
  multi-agente**: sin cambios respecto a CH-00/CH-01/CH-02/CH-03/CH-04 — explícitamente fuera de
  alcance de BH-v0.1.

## 19. Siguiente Incremento (Next Increment)

El problema natural del próximo capítulo: ahora que `PolicyEngine` puede producir una
`PolicyDecision` real (§11), incluyendo la señal `REQUIRE_APPROVAL` que `AgentRunStatus` anticipó
desde CH-01 sin que nada la produjera, ¿quién representa y resuelve esa aprobación pendiente para
que la ejecución realmente pueda reanudarse — y quién cablea, de una vez, `ToolRuntime` con
`PolicyEngine` para que `INV-06` deje de ser una regla preservada solo por abstención y pase a ser
una regla exigida por código en cada `ToolCall` real? Eso apunta hacia `HumanInteractionService`
(Article IV: "How is required human intervention represented and resolved?") como el sexto
componente candidato de Article III que dejaría de ser preview — probablemente en el mismo
capítulo que finalmente conecte `ToolRuntime.executeToolCall` con
`PolicyEngine.evaluatePolicyForToolCall`, cerrando la integración que este capítulo dejó
deliberadamente sin cablear.

Ese capítulo (`CH-06`, fuera del alcance de esta ejecución) heredaría directamente la deuda
intencional de §18. `next_chapter` queda en `null` en el frontmatter de este capítulo porque, en
este momento del libro, `CH-06` todavía no existe como archivo — solo como el problema que
motivará su escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de
> la secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco
> Iceberg / Bucles de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas,
> Forrester/Meadows), secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): sin un dueño explícito para "¿puede ocurrir esta
   acción?", la autorización tiende a asumirse implícitamente (si nada la niega, ocurre) o a
   dispersarse como verificaciones ad hoc en el lugar donde la acción se ejecuta o el contexto se
   selecciona.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): sin un componente
   con fronteras explícitas, la ausencia de una regla aplicable se interpreta como autorización
   implícita en vez de como señal para negar, y sin un resultado de tres estados, una acción que
   necesita aprobación humana termina forzada a permitir o a denegar.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `PolicyEngine` (CMP-005) con una ficha que declara tanto lo que posee (`owns`: allow, deny,
   constraints, approval requirements, policy evaluation) como lo que explícitamente NO posee
   (`does_not_own`, con cinco exclusiones, tres contra componentes ya construidos) y formaliza
   `PolicyDecision` (C-014), el primer contrato verdaderamente nuevo del libro.
4. **Modelos mentales** (= §4, Constitutional Impact): P-13 ("Authorization is deterministic and
   external to the LLM") junto con INV-06 ("Todo side effect pasa por PolicyEngine") — la
   autorización nunca depende de que el modelo se comporte bien, y ante la duda, el sistema
   deniega, nunca permite.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un componente nuevo se introduce sin declarar
  explícitamente su `does_not_own`, aumenta la probabilidad de que absorba silenciosamente la
  próxima decisión vecina "porque ya estaba ahí" — el mismo bucle que CH-01/CH-02/CH-03/CH-04 ya
  cortaron. Este capítulo lo repite para `PolicyEngine`, cerrando además, desde el otro lado, la
  tentación inversa que CH-02 ya había anticipado: que `ToolRuntime` absorbiera la autorización.
- **Bucle de equilibrio (estabiliza):** `evaluatePolicyForToolCall` (§11) nunca interpreta la
  ausencia de una policy rule como permiso — deniega por defecto (fail-closed), convirtiendo cada
  caso sin cubrir en un fallo visible y clasificado en vez de en una brecha silenciosa.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `PolicyDecision.outcome` sea un `ENUM` de tres
valores en vez de un `Boolean`, combinado con que `evaluatePolicyForToolCall` deniegue por defecto
cuando ninguna regla aplica. Si esta autorización colapsara a un booleano, o si la ausencia de
regla se interpretara como permiso, cada capítulo futuro que dependa de `PolicyEngine` heredaría un
modelo de autorización incapaz de representar "todavía no" — solo "sí" o "no".

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado
> completo de esta sección (con ids estables para cada pregunta/tarjeta) vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida. Aquí se
> presenta en prosa, para lectura directa del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Cuando la ejecución controlada de una acción recibe esa acción ya resuelta pero explícitamente
   no decide si está permitida, ¿quién evalúa esa autorización antes de que la ejecución ocurra, y
   qué debería pasar cuando ningún criterio conocido cubre el caso — permitirla por defecto o
   negarla por defecto? *(cierra la pregunta guía 1)*
2. Si una acción no es simplemente "permitida" o "denegada", sino que primero necesita que un
   humano la apruebe, ¿cómo se representa ese tercer resultado sin que quien lo produce necesite
   ya saber cómo se resuelve esa aprobación? *(cierra la pregunta guía 2)*
3. Para que una decisión de autorización se pueda auditar después de que ocurrió, ¿qué información
   mínima debería acompañar a ese resultado, más allá de un simple sí o no? *(cierra la pregunta
   guía 3)*
4. ¿Por qué el mismo componente que decide si una acción está permitida no debería, además,
   ejecutar esa acción, invocar al modelo, seleccionar qué información es relevante, o decidir si
   el turno debe continuar? *(cierra la pregunta guía 4)*

### Explicar

1. `PolicyEngine` posee decidir si una acción está permitida. Explica, como si hablaras con
   alguien sin contexto técnico, por qué NO posee ejecutar esa acción una vez que la permite —
   ¿qué se rompería, en concreto, si `PolicyEngine` empezara a ejecutar la acción directamente "ya
   que de todos modos acaba de decidir que está permitida"?
2. `PolicyDecision.reason` reutiliza `HarnessError` (C-011) únicamente cuando `outcome = DENY`,
   nunca cuando `outcome = ALLOW` o `REQUIRE_APPROVAL`. Explica por qué una denegación se modela
   como un `HarnessError` (Article VII: "Policy denied → policy / non-retryable") pero un
   `REQUIRE_APPROVAL` no es, en sí mismo, un fallo — ¿qué perderíamos si tratáramos ambos casos de
   la misma forma?

### Conectar

1. `ToolRuntime` (CH-02) recibe un `ToolCall` ya resuelto pero, por su propio `does_not_own`,
   nunca evalúa si esa acción está autorizada. ¿Qué campo de `ToolCall` necesitaría leer quien
   evalúe la policy aplicable a esa acción para poblar `PolicyDecision.callId`, y qué correlación
   permite ese campo entre la `PolicyDecision` resultante y la tool call que la motivó?
2. `ContextEngine` (CH-04) asume que sus `candidates` ya llegaron autorizados para verse, sin
   verificarlo él mismo. ¿Qué `outcome` de la evaluación de este capítulo correspondería,
   conceptualmente, a negar la visibilidad de uno de esos candidatos, y por qué esa respuesta no
   obliga a `ContextEngine` a empezar a producir ese resultado él mismo?

### Espaciar

Las cuatro tarjetas de repaso de este capítulo (dos sobre `PolicyEngine` — su `owns` y su
`does_not_own` — y dos sobre `PolicyDecision` — sus campos y por qué `outcome` no es un `Boolean`)
entran hoy en `reviewStage = DAY_1`. Repásalas de nuevo al día 3, al día 7 y al día 21 (curva de
Ebbinghaus) — ver el apéndice de tarjetas al final del libro (edición PDF) o
`retrieval_set.flashcards` en `dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te
equivocaste, ese es precisamente el punto ciego que este método existe para revelar.
