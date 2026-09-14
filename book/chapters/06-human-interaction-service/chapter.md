---
id: CH-06
title: "HumanInteractionService y la Reanudación de una Ejecución Pausada"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-006]
introduces_contracts: [C-015, C-016]
modifies_contracts: []
constitutional_articles: [P-11, INV-14, INV-15, INV-18, INV-19, INV-20]
previous_chapter: CH-05
next_chapter: CH-07
retrieval_set:
  expected_outcome:
    id: EO-CH06
    text: |
      Al terminar este capítulo podrás distinguir, dentro del tercer resultado posible de una
      evaluación de autorización ("todavía no, necesita aprobación humana"), qué tramo le
      pertenece en exclusiva al componente que representa y resuelve esa espera y qué tramos
      siguen perteneciendo a otros dominios (decidir si se requiere aprobación, transportar esa
      solicitud a través de un canal concreto, ejecutar la acción una vez resuelta, decidir si el
      turno continúa) — y podrás diseñar, para cualquier resolución humana, un resultado que no
      colapse en un simple aprobado/rechazado cuando en realidad se trata de un valor provisto,
      preservando siempre quién la resolvió para que sea auditable después.
  skeleton:
    id: SK-CH06
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
    components_to_be_introduced: [CMP-006]
    contracts_to_be_introduced: [C-015, C-016]
  guiding_questions:
    - id: GQ-CH06-01
      text: |
        Cuando la evaluación de autorización del capítulo anterior produce un tercer resultado —
        ni permitido ni denegado, sino "todavía no, necesita que un humano lo apruebe" — ¿quién
        representa esa solicitud pendiente, la persiste, y qué le permite a la ejecución,
        eventualmente, reanudarse?
      answered_by: RQ-CH06-01
    - id: GQ-CH06-02
      text: |
        Si la interfaz por la que un humano llega a ver y resolver esa solicitud pendiente pudiera
        ser una terminal, una página web, un mensaje de chat o un correo, ¿debería esa interfaz
        decidir qué significa "aprobado" o qué datos persisten de la solicitud, o ese significado
        vive en otro lugar, indiferente al canal que se use?
      answered_by: RQ-CH06-02
    - id: GQ-CH06-03
      text: |
        Una vez que alguien resuelve una solicitud pendiente, ¿qué debería evitar que esa misma
        solicitud se resuelva una segunda vez, y qué información mínima debería acompañar a esa
        resolución para que, después, se pueda auditar quién la tomó?
      answered_by: RQ-CH06-03
    - id: GQ-CH06-04
      text: |
        Si el resultado de resolver una solicitud pendiente no es siempre un simple sí/no — a
        veces es un valor que el humano proporcionó como respuesta — ¿ese resultado debería
        forzarse a un booleano, y por qué el componente que representa y resuelve esa espera no
        debería, además, decidir si el turno continúa o ejecutar la acción una vez aprobada?
      answered_by: RQ-CH06-04
  systems_lens:
    iceberg_visible_fact: |
      Sin un dueño explícito para "¿quién representa y resuelve una aprobación humana pendiente?",
      `AgentRunStatus.WAITING_FOR_HUMAN` (declarado desde CH-01) y `PolicyDecision.outcome =
      REQUIRE_APPROVAL` (producido desde CH-05) siguen siendo, literalmente, una señal sin
      receptor — el equivalente arquitectónico de un teléfono que suena en una habitación vacía
      (ver seccion 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite, ahora aplicado a la interacción humana, es que sin un componente con
      fronteras explícitas la tentación más fuerte no es que este componente invada a otro, sino
      que la interfaz concreta que un humano usa para responder (una TUI, una página web, un canal
      de chat) termine decidiendo, cada una a su manera, qué significa "aprobado" y cómo se
      persiste esa decisión — exactamente lo que Article VIII y P-11 prohíben (ver seccion 3, Por
      Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala el sexto componente real del libro, `HumanInteractionService`
      (CMP-006), con una ficha que declara tanto lo que posee (`owns`: representar solicitudes
      humanas, persistir interacciones pendientes, recibir resoluciones, permitir reanudación —
      cita literal de Article III) como lo que explícitamente NO posee (`does_not_own`: decidir SI
      se requiere aprobación, transportar la interacción a través de un canal concreto, ejecutar la
      acción ya resuelta, decidir continuación del turno) — y formaliza dos contratos nuevos,
      `HumanInteractionRequest` (C-015) y `HumanInteractionResolution` (C-016), el primer par
      solicitud/resolución del libro modelado explícitamente como dos momentos distintos de una
      misma espera (ver seccion 8, Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es la Human Interaction Rule de Article VIII
      ("las interfaces transportan la interacción; el runtime define y persiste su significado")
      junto con INV-14 ("Human Interaction nunca depende de una interfaz particular"): ningún
      campo de `HumanInteractionRequest` ni de `HumanInteractionResolution` registra por qué canal
      llegó o se resolvió la solicitud — esa omisión es deliberada, no un descuido (ver seccion 4,
      Impacto Constitucional).
    reinforcing_loop: |
      Cada vez que un componente nuevo se introduce sin declarar explícitamente su `does_not_own`,
      aumenta la probabilidad de que absorba silenciosamente la próxima decisión vecina "porque ya
      estaba ahí" — el mismo bucle que CH-01..CH-05 ya cortaron. Este capítulo lo repite para
      `HumanInteractionService`, con la misma particularidad que CH-05 ya había anticipado: la
      tentación más fuerte no viene de un componente vecino ya construido, sino de la superficie
      todavía sin componente propio (el canal concreto) reclamando, por comodidad de
      implementación, una responsabilidad que Article VIII asigna íntegramente al runtime.
    balancing_loop: |
      El mecanismo de equilibrio de este capítulo es estructural, no solo procedimental:
      `HumanInteractionRequest` y `HumanInteractionResolution` (seccion 6) simplemente no tienen
      ningún campo que represente un canal o transporte — INV-14 no se preserva por convención de
      quien implemente el canal, sino porque el contrato mismo no le deja espacio para expresarse.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que ni `HumanInteractionRequest` (C-015) ni
      `HumanInteractionResolution` (C-016) modelen un campo de canal — combinado con que
      `HumanInteractionOutcome` sea un `ENUM` de tres valores (`APPROVED`/`REJECTED`/`PROVIDED`) en
      vez de un `Boolean`, para no forzar "proveyó un valor" a la casilla más cercana. Si un canal
      se filtrara como campo del contrato, cada implementación futura de un Channel Adapter
      heredaría la posibilidad de que ese canal cambiara el significado de una resolución — lo que
      la Human Interaction Rule prohíbe explícitamente.
  recall_questions:
    - id: RQ-CH06-01
      text: |
        ¿Qué componente crea, persiste y eventualmente marca como resuelta una solicitud de
        interacción humana, y a partir de qué contrato de qué componente ya existente recibe la
        señal que la dispara?
    - id: RQ-CH06-02
      text: |
        ¿Qué invariante y qué regla constitucional explican por qué `HumanInteractionRequest` y
        `HumanInteractionResolution` no incluyen ningún campo que identifique el canal (TUI, Web,
        Slack, ...) por el que se transportó la interacción?
    - id: RQ-CH06-03
      text: |
        ¿Qué campo de `HumanInteractionRequest` impide que `resolveHumanInteractionRequest` la
        resuelva dos veces, y qué campo de `HumanInteractionResolution` registra quién la resolvió,
        para efectos de INV-19?
    - id: RQ-CH06-04
      text: |
        ¿Cuáles son los tres valores posibles de `HumanInteractionOutcome`, y qué dos decisiones
        relacionadas — ya asignadas a componentes existentes — `HumanInteractionService` explícita
        y deliberadamente no toma cuando produce esa resolución?
  explain_prompts:
    - id: EP-CH06-01
      text: |
        `HumanInteractionService` posee representar, persistir y resolver una solicitud de
        aprobación humana. Explica, como si hablaras con alguien sin contexto técnico, por qué NO
        posee decidir SI esa aprobación se requiere en primer lugar — ¿qué se rompería, en
        concreto, si `HumanInteractionService` empezara a decidir por su cuenta cuándo una acción
        necesita aprobación, en vez de limitarse a recibir esa señal ya decidida?
      target_entity: CMP-006
    - id: EP-CH06-02
      text: |
        `HumanInteractionResolution.outcome` es un `ENUM` de tres valores
        (`APPROVED`/`REJECTED`/`PROVIDED`), no un `Boolean`, y `value` solo se puebla cuando
        `outcome = PROVIDED`. Explica por qué forzar una resolución de tipo `Input` (alguien
        respondiendo con un dato, no con un sí/no) hacia `APPROVED`/`REJECTED` perdería
        información que un capítulo futuro necesitaría para reanudar la ejecución correctamente.
      target_entity: C-016
  interleaved_questions:
    - id: IQ-CH06-01
      text: |
        `PolicyEngine` (CH-05) produce `PolicyDecision.outcome = REQUIRE_APPROVAL` pero,
        explícitamente, no representa ni resuelve esa aprobación — ver su propio `does_not_own`.
        ¿Qué campo de `PolicyDecision` necesita leer quien construya una `HumanInteractionRequest`
        para poblar `HumanInteractionRequest.callId`, y por qué ese campo es una correlación
        reutilizada en vez de una relación nueva hacia `PolicyDecision`?
      current_chapter_entities: [CMP-006, C-015]
      prior_chapter_entities: [CMP-005, C-014]
      prior_chapter: CH-05
    - id: IQ-CH06-02
      text: |
        `AgentRunStatus.WAITING_FOR_HUMAN` (CH-01) sigue sin ser el destino de ninguna transición
        real: `AgentLoop` nunca transiciona hacia allí ni sale de allí en este libro. ¿Qué produce
        este capítulo que, por primera vez, haría posible esa transición completa (entrada y
        salida), y por qué construir ese contrato no obliga a `AgentLoop` a cambiar una sola línea
        todavía?
      current_chapter_entities: [CMP-006, C-016]
      prior_chapter_entities: [CMP-001, C-013]
      prior_chapter: CH-01
  flashcards:
    - id: FC-CH06-01
      front: |
        ¿Qué posee `HumanInteractionService` (Article III / Article IV), en una frase?
      back: |
        Representar solicitudes humanas, persistir interacciones pendientes, recibir resoluciones
        y permitir reanudación — cita literal de Article III, sección "HumanInteractionService":
        representar y resolver la espera, nunca decidir si se requiere.
      source_entity: CMP-006
      chapter_introduced_in: CH-06
      review_stage: DAY_1
    - id: FC-CH06-02
      front: |
        ¿Qué NO posee `HumanInteractionService`, y a qué componentes o conceptos pertenecen esas
        decisiones?
      back: |
        Decidir SI se requiere aprobación (`PolicyEngine`, ya introducido en CH-05), transportar la
        interacción por un canal concreto (Channel Adapter, concepto de infraestructura de borde,
        no un componente de Article III), ejecutar la acción ya resuelta (`ToolRuntime`, ya
        introducido en CH-02) y decidir continuación del turno (`AgentLoop`, ya introducido en
        CH-01).
      source_entity: CMP-006
      chapter_introduced_in: CH-06
      review_stage: DAY_1
    - id: FC-CH06-03
      front: |
        ¿Qué campos tiene `HumanInteractionRequest` (C-015), y por qué ninguno identifica un canal?
      back: |
        `id` (HumanInteractionRequestId), `type` (HumanInteractionType — Approval/Input/Review/
        Decision), `callId` (ToolCallId, correlación reutilizada de `PolicyDecision.callId`),
        `status` (HumanInteractionStatus — Pending/Resolved) y `requestedAt` (Timestamp). Ningún
        campo de canal: INV-14 exige que Human Interaction nunca dependa de una interfaz
        particular.
      source_entity: C-015
      chapter_introduced_in: CH-06
      review_stage: DAY_1
    - id: FC-CH06-04
      front: |
        ¿Qué campos tiene `HumanInteractionResolution` (C-016), y qué representa cada uno?
      back: |
        `requestId` (HumanInteractionRequestId, qué solicitud se resolvió), `outcome`
        (HumanInteractionOutcome — Approved/Rejected/Provided), `value` (Optional<Value>, poblado
        solo cuando outcome = Provided), `resolvedBy` (ActorId, trazabilidad INV-19) y
        `resolvedAt` (Timestamp).
      source_entity: C-016
      chapter_introduced_in: CH-06
      review_stage: DAY_1
    - id: FC-CH06-05
      front: |
        ¿Por qué `HumanInteractionOutcome` tiene tres valores en vez de un `Boolean`?
      back: |
        Porque una resolución de tipo `Input` no es un sí/no — es un valor que el humano proveyó.
        Un `Boolean` solo puede expresar aprobado/rechazado; `PROVIDED` (con `value` poblado) es el
        tercer caso que un booleano no puede representar sin perder información, el mismo problema
        que motivó que `PolicyOutcome` (CH-05) tuviera tres valores en vez de dos.
      source_entity: C-016
      chapter_introduced_in: CH-06
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH06-01
      recall_question: RQ-CH06-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH06-02
      recall_question: RQ-CH06-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH06-03
      recall_question: RQ-CH06-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH06-04
      recall_question: RQ-CH06-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 6 — HumanInteractionService y la Reanudación de una Ejecución Pausada

> **Regla constitucional (Article VIII, Human Interaction Rule):** las interfaces transportan la
> interacción; el runtime define y persiste su significado.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de saber
> cómo se llama el componente de este capítulo. El detalle estructurado de esta sección vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, dentro del tercer resultado
posible de una evaluación de autorización ("todavía no, necesita aprobación humana"), qué tramo le
pertenece en exclusiva al componente que este capítulo introduce y qué tramos siguen perteneciendo
a otros dominios (decidir si se requiere aprobación, transportar esa solicitud a través de un canal
concreto, ejecutar la acción una vez resuelta, decidir si el turno continúa) — y podrás diseñar,
para cualquier resolución humana, un resultado que no colapse en un simple aprobado/rechazado
cuando en realidad se trata de un valor provisto, preservando siempre quién la resolvió para que
sea auditable después.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e
introduce dos contratos de datos (`HumanInteractionRequest` y `HumanInteractionResolution`) y el
sexto componente de runtime del libro (`HumanInteractionService`) — todavía sin explicarlos, solo
como mapa.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar
atrás; están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este
capítulo va a definir):

1. Cuando la evaluación de autorización del capítulo anterior produce un tercer resultado — ni
   permitido ni denegado, sino "todavía no, necesita que un humano lo apruebe" — ¿quién representa
   esa solicitud pendiente, la persiste, y qué le permite a la ejecución, eventualmente,
   reanudarse?
2. Si la interfaz por la que un humano llega a ver y resolver esa solicitud pendiente pudiera ser
   una terminal, una página web, un mensaje de chat o un correo, ¿debería esa interfaz decidir qué
   significa "aprobado" o qué datos persisten de la solicitud, o ese significado vive en otro
   lugar, indiferente al canal que se use?
3. Una vez que alguien resuelve una solicitud pendiente, ¿qué debería evitar que esa misma
   solicitud se resuelva una segunda vez, y qué información mínima debería acompañar a esa
   resolución para que, después, se pueda auditar quién la tomó?
4. Si el resultado de resolver una solicitud pendiente no es siempre un simple sí/no — a veces es
   un valor que el humano proporcionó como respuesta — ¿ese resultado debería forzarse a un
   booleano, y por qué el componente que representa y resuelve esa espera no debería, además,
   decidir si el turno continúa o ejecutar la acción una vez aprobada?

## 1. Arquitectura Actual (Current Architecture)

CH-00 dejó instalados siete contratos de datos y dos políticas. CH-01 agregó `AgentRunStatus`
(C-013) y el primer componente de runtime, `AgentLoop` (CMP-001) — con un estado,
`WAITING_FOR_HUMAN`, declarado desde su primera versión pero sin ningún componente que lo
justificara. CH-02 resolvió `ToolCall`/`ToolResult` (C-008/C-009) junto con `ToolRuntime`
(CMP-002). CH-03 resolvió `ModelRequest`/`ModelResponse` (C-006/C-007) junto con `ModelGateway`
(CMP-003). CH-04 resolvió `ContextSnapshot` (C-005) junto con `ContextEngine` (CMP-004). CH-05
resolvió, con `PolicyDecision` (C-014) y `PolicyEngine` (CMP-005), la pregunta "¿puede ocurrir esta
acción?" — produciendo, por primera vez, una señal real (`PolicyDecision.outcome =
REQUIRE_APPROVAL`) capaz de justificar `WAITING_FOR_HUMAN`. Con eso, `registry/contracts.yaml`
suma catorce contratos y `registry/components.yaml` cinco componentes.

Pero CH-05 fue explícito, en su propio `does_not_own` (CH-05 §8) y en su sección de seguridad
(CH-05 §15), sobre lo que **no** resolvió: `PolicyEngine` "no representa la solicitud humana, no la
persiste, no espera una resolución y no reanuda nada". `AgentRunStatus.WAITING_FOR_HUMAN` (C-013,
declarado desde CH-01 §6) sigue siendo, después de cinco capítulos reales, un estado del lifecycle
que ninguna transición real ha alcanzado — ahora con una señal que lo justificaría
(`REQUIRE_APPROVAL`), pero sin nadie que la reciba.

Hay además una segunda deuda, más silenciosa, heredada directamente de CH-00: `ErrorCategory`
(embebido en `HarnessError`, C-011) declara diez valores (`VALIDATION`, `POLICY`, `TOOL`, `MODEL`,
`CONTEXT`, `PERSISTENCE`, `INFRASTRUCTURE`, `BUDGET`, `CANCELLATION`, `FATAL`) — pero
`constitution/ARCHITECTURE_CONSTITUTION.md` Article VII (Failure Constitution) enumera, en su lista
canónica de `Failure Examples`, un tipo de fallo que ese enum nunca llegó a incorporar:
`HumanInteractionError`. A diferencia de `ErrorCategory.POLICY` (que CH-05 encontró declarado pero
nunca ejercitado) o `ErrorCategory.CONTEXT` (que CH-04 encontró en la misma situación), aquí el
valor ni siquiera existe todavía en el `ENUM` — es una categoría de fallo que la Constitution
anticipó por nombre desde Article VII, sin que ningún capítulo, hasta ahora, hubiera tenido un
motivo real para agregarla.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas, "¿quién representa y resuelve una aprobación humana
pendiente?" tiende a resolverse de una forma peligrosa y predecible: la interfaz concreta que un
humano usa para responder — una TUI, una página web, un bot de Slack — termina decidiendo, cada
implementación a su manera, qué significa "aprobado", cómo se persiste la solicitud mientras
espera, y qué pasa si el proceso que la generó ya no existe cuando la respuesta llega. Eso es
exactamente lo que Article VIII prohíbe: "Human-in-the-loop es una capacidad del runtime, no de la
TUI" — y lo que P-11 generaliza para toda interfaz: "UI is an adapter, not part of the core".

Un segundo problema, más sutil: incluso si alguna implementación centralizara esa lógica en un
único lugar, nada le impide, con el mismo criterio con el que `PolicyEngine` (CH-05) evitó colapsar
su resultado a un booleano, cometer el error inverso aquí — forzar la resolución de una solicitud
que en realidad esperaba un **valor** (piénsese en "necesito que me confirmes este dato antes de
continuar") hacia la casilla más cercana, "aprobado" o "rechazado", perdiendo la información real
que la ejecución necesita para reanudarse correctamente.

Necesitamos que "representar, persistir, recibir y permitir la reanudación de una interacción
humana pendiente" tenga un dueño único y nombrado — que ese dueño construya la solicitud a partir
de la señal que `PolicyEngine` ya produce (sin decidir él mismo si se requiere aprobación), que
nunca dependa de saber por qué canal llegó una respuesta (INV-14), y que registre siempre quién
resolvió la solicitud, para que sea auditable después (INV-19).

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los catorce contratos y los cinco componentes que existen hasta este punto no bastan porque:

- `PolicyEngine` (CH-05) produce `PolicyDecision.outcome = REQUIRE_APPROVAL` como una señal
  completamente válida — pero su propio `does_not_own` excluye representarla, persistirla,
  resolverla o reanudar nada a partir de ella; sin un componente real que sí lo haga, esa señal no
  tiene ningún destino;
- `AgentRunStatus.WAITING_FOR_HUMAN` (CH-01) sigue siendo un estado del lifecycle sin ninguna
  transición real que lo alcance ni que salga de él — la Constitution lo anticipó desde Article V,
  pero nada en el libro, hasta ahora, lo ha necesitado de verdad;
- `ErrorCategory.HumanInteractionError` (Article VII) sigue sin existir como valor del `ENUM`
  `ErrorCategory` (CH-00) — un fallo genuino de este dominio (por ejemplo, que una resolución no
  corresponda al tipo de solicitud que dice resolver) no tendría, hoy, ninguna categoría real bajo
  la cual clasificarse;
- nada impide que, sin un contrato explícito para la solicitud y otro para su resolución, ambos
  momentos se confundan en una sola estructura mutable — perdiendo la distinción entre "esto está
  pendiente" y "esto ya se resolvió", exactamente el mismo tipo de distinción que CH-02 ya modeló
  entre `ToolCall` y `ToolResult`, y CH-03 entre `ModelRequest` y `ModelResponse`.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la
> secuencia `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una
> entidad que no haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT`
> registrado — **no magic entities**. Este capítulo aplica la misma disciplina de *ownership* que
> CH-01..CH-05 ya establecieron — con una particularidad nueva: la tentación más fuerte que este
> capítulo debe cortar no viene de un componente vecino ya construido, sino de la superficie
> todavía sin componente propio (el canal concreto por el que un humano responde) reclamando, por
> comodidad de implementación, una responsabilidad que Article VIII asigna íntegramente al
> runtime.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-11   UI is an adapter, not part of the core.
           Primera vez que este principio tiene un componente real que lo protege en el dominio
           de la interacción humana: HumanInteractionRequest/HumanInteractionResolution no
           incluyen ningún campo de canal — cualquier UI (TUI, Web, Slack, Teams, Mobile, Email,
           API) puede transportar la interacción sin poder cambiar su significado.

Invariants preserved
    INV-14   Human Interaction nunca depende de una interfaz particular.
             Primera cita literal posible de este invariante: ya existe un HumanInteractionService
             real, y ninguno de sus dos contratos (C-015/C-016) modela un canal — INV-14 se
             preserva estructuralmente, no por convención de quien implemente el Channel Adapter
             (fuera de alcance, ver seccion 9/18).
    INV-15   Una acción que requiere aprobación no puede ejecutarse antes de una resolución
             válida.
             CH-05 produjo la señal (PolicyDecision.outcome = REQUIRE_APPROVAL); este capítulo
             produce, por primera vez, un mecanismo real para representar esa espera
             (HumanInteractionRequest) y para producir la resolución que la cierra
             (HumanInteractionResolution) — sin que todavía exista el cableado que obligue a
             ToolRuntime a esperar esa resolución antes de Execute (deuda intencional, ver
             seccion 18).
    INV-18   Toda acción significativa produce un evento observable.
             createHumanInteractionRequest y resolveHumanInteractionRequest (seccion 11) emiten,
             cada una, un AgentEvent — el sexto componente del libro que produce eventos en la
             práctica.
    INV-19   Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy
             relevante.
             HumanInteractionResolution.resolvedBy es, literalmente, el "actor" que INV-19 exige
             poder trazar — la primera vez que este libro modela explícitamente quién, no solo
             qué, tomó una decisión crítica.
    INV-20   Todo error operacional pertenece a una categoría conocida.
             Este capítulo agrega HUMAN_INTERACTION a ErrorCategory (CH-00) — la primera vez que
             este valor, anticipado por nombre en Article VII ("HumanInteractionError") desde la
             primera versión de la Constitution, se materializa como un valor real del enum.

Component ownership changes
    CMP-006 HumanInteractionService se introduce — registry/components.yaml pasa de 5 a 6
    componentes. owns/does_not_own citados literalmente contra Article III (sección
    "HumanInteractionService") y Article IV. registry/components.yaml de CMP-001 AgentLoop y
    CMP-005 PolicyEngine NO se modifica: ninguno de los dos cablea todavía su relación real con
    HumanInteractionService (ver seccion 9/18).

Lifecycle changes
    Ninguno sobre AgentRunStatus (C-013): esa máquina de estados sigue siendo propiedad exclusiva
    de AgentLoop (CH-01), y su tabla de transiciones no cambia aquí. Este capítulo sí introduce el
    lifecycle propio de HumanInteractionRequest (PENDING → RESOLVED, seccion 12) — el primer
    lifecycle de dos estados del libro, distinto y más simple que AgentRunStatus.

Security implications
    Este es el primer capítulo que materializa Article VIII completo como código ejecutable. Ver
    seccion 15 para el análisis completo, incluyendo por qué ningún campo de canal existe en
    ninguno de los dos contratos nuevos.

Observability implications
    HumanInteractionService es el sexto componente que emite AgentEvent en la práctica,
    extendiendo AgentEventType con DOS valores nuevos (HUMAN_INTERACTION_REQUESTED,
    HUMAN_INTERACTION_RESOLVED) — uno por cada una de las dos operaciones reales que este
    componente posee, no un par éxito/fallo de una sola operación (ver seccion 14 para la razón
    completa).

Deterministic vs agentic boundary
    Article XII se refina una sexta vez a nivel de componente: HumanInteractionService no recibe
    absolutamente ninguna entrada que el modelo haya producido — ni siquiera de forma indirecta
    (a diferencia de PolicyEngine, que evalúa un ToolCall cuyos argumentos el modelo ayudó a
    proponer). Consume exclusivamente una PolicyDecision ya determinística (CH-05) y una
    resolución que, por definición, un humano produjo.
```

## 5. Conceptos Nuevos (New Concepts)

- **Human Interaction Request**: la representación persistida de una aprobación humana pendiente,
  construida a partir de una `PolicyDecision` con `outcome = REQUIRE_APPROVAL` (CH-05) —
  responsabilidad exclusiva de `HumanInteractionService` (Article III, Article IV:
  "`HumanInteractionService` → How is required human intervention represented and resolved?").
- **Human Interaction Resolution**: el resultado que un humano produjo al resolver una solicitud
  pendiente — aprobó, rechazó o proveyó un valor — junto con quién lo resolvió y cuándo. Es lo que,
  conceptualmente, permite el paso `Resolution → Resume` del flujo de Article VIII.
- **Channel Adapter** *(concepto de infraestructura de borde, no un componente de Article III / del
  registry)*: la pieza que transportaría una `HumanInteractionRequest` hacia un canal concreto
  (`TUI`/`Web`/`Slack`/`Teams`/`Mobile`/`Email`/`API`, Article VIII) y traería de vuelta la
  respuesta cruda del humano — este capítulo la menciona en prosa, exactamente como P-11 exige
  ("UI is an adapter, not part of the core"), sin introducirla como `COMPONENT` propio ni como
  dependencia registrada.
- **Human-in-the-loop**: la capacidad general del runtime de pausar una ejecución para que un
  humano intervenga antes de continuar — Article VIII la declara explícitamente como "una
  capacidad del runtime, no de la TUI"; este capítulo es la primera materialización real de esa
  capacidad.
- **Default Deny, aplicado a la resolución** *(extensión del principio de CH-05, no una regla
  nueva)*: `resolveHumanInteractionRequest` (seccion 11) nunca asume que una resolución es válida
  solo porque llegó — verifica que la solicitud siga `PENDING` y que el `outcome` recibido
  corresponda al `type` de la solicitud, antes de aceptarla (seccion 13).
- **Decision Ownership** *(Article IV, en uso desde CH-01, ahora aplicado a un sexto componente)*:
  `HumanInteractionService` decide "¿cómo se representa y resuelve una intervención humana
  requerida?"; explícitamente NO decide "¿se requiere aprobación?" (`PolicyEngine`, ya resuelto),
  "¿por qué canal se transporta?" (Channel Adapter, concepto sin componente propio), "¿cómo se
  ejecuta la acción ya aprobada?" (`ToolRuntime`, ya resuelto) ni "¿debe ocurrir otro turno o debe
  reanudarse la ejecución?" (`AgentLoop`, ya resuelto).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados de CH-00/CH-01/CH-02/CH-03/CH-04/CH-05

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `AgentId`, `ToolCallId`, `Timestamp`, `ExecutionContext`,
`AgentEvent`, `HarnessError`, `PolicyDecision`.

### Dos identificadores opacos nuevos

Siguiendo el mismo patrón que CH-00 §6 estableció para los identificadores fundamentales
(`AgentId`, `MessageId`, ...): tipos opacos, sin campos propios, usados como tipo de campo en los
`STRUCT` de esta sección.

| Identificador (nuevo de este capítulo) | Identifica |
|---|---|
| `HumanInteractionRequestId` | una solicitud de interacción humana pendiente o ya resuelta |
| `ActorId` | quien resolvió una solicitud de interacción humana — un identificador opaco; este capítulo no introduce ningún `STRUCT Actor`/`User` propio (misma restricción de alcance que `Capability`/`Tool` en CH-02) |

### `AgentEventType` — extendido, sin redefinir `AgentEvent`

CH-05 extendió `AgentEventType` a once valores. Este capítulo agrega dos valores nuevos — uno por
cada una de las dos operaciones reales que `HumanInteractionService` posee, no un par éxito/fallo
de una sola operación (seccion 14 explica la razón completa):

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
END
```

`AgentEvent` (C-010) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — solo el rango de
valores permitido para `eventType` crece, igual que en cada capítulo anterior.

### `ErrorCategory` — extendido, sin redefinir `HarnessError`

Este es el primer capítulo que agrega un valor a `ErrorCategory` desde que CH-00 lo declaró: el
valor `HUMAN_INTERACTION`, que Article VII anticipó por nombre (`HumanInteractionError`) sin que
ningún capítulo anterior lo necesitara de verdad:

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
END
```

`HarnessError` (C-011) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — mismo patrón
exacto que la extensión de `AgentEventType` de cada capítulo anterior, aplicado aquí por primera
vez a `ErrorCategory` en vez de a `AgentEventType`.

### `HumanInteractionType` — los cuatro tipos mínimos de Article VIII

```pseudocode
ENUM HumanInteractionType
    APPROVAL
    INPUT
    REVIEW
    DECISION
END
```

Cita literal de Article VIII ("Tipos mínimos: `Approval` / `Input` / `Review` / `Decision`") — este
capítulo no agrega ni reinterpreta ningún tipo adicional.

### `HumanInteractionStatus` — el lifecycle de dos estados de una solicitud

```pseudocode
ENUM HumanInteractionStatus
    PENDING
    RESOLVED
END
```

Deliberadamente dos estados, no más: este capítulo no modela expiración (`EXPIRED`) como un tercer
valor de `HumanInteractionStatus` — esa sería una extensión real, no un ajuste de v1 (seccion 18).

### `HumanInteractionOutcome` — el resultado de tres estados de una resolución

```pseudocode
ENUM HumanInteractionOutcome
    APPROVED
    REJECTED
    PROVIDED
END
```

Tres valores, deliberadamente, no dos: el mismo argumento que motivó `PolicyOutcome` (CH-05) — un
`Boolean` puede representar "aprobado" o "rechazado", pero no puede representar "el humano proveyó
un valor como respuesta" (tipo `Input` de `HumanInteractionType`) sin perder esa respuesta.
`HumanInteractionOutcome` vive embebido dentro de `HumanInteractionResolution`, sin contrato
`C-XXX` propio — el mismo patrón que `PolicyOutcome` (CH-05) o `ContextBlock` (CH-04).

### `HumanInteractionRequest` — la solicitud persistida

```pseudocode
STRUCT HumanInteractionRequest
    id: HumanInteractionRequestId
    type: HumanInteractionType
    callId: ToolCallId
    status: HumanInteractionStatus
    requestedAt: Timestamp
END
```

`callId` correlaciona esta solicitud con el `ToolCall` (C-008, CH-02) que originalmente la motivó —
el mismo campo que `PolicyDecision.callId` (C-014, CH-05) ya usa para correlacionarse con ese mismo
`ToolCall`. Este capítulo reutiliza esa correlación en vez de inventar una relación nueva hacia
`PolicyDecision`: dado que un `ToolCall` produce, como mucho, una `PolicyDecision` real por
evaluación, `callId` identifica de forma suficiente cuál fue la decisión que disparó esta solicitud
(seccion 9 profundiza en esta frontera). **Ningún campo de canal** (seccion 5, Channel Adapter):
INV-14 exige que Human Interaction nunca dependa de una interfaz particular, y este `STRUCT` no le
deja espacio a esa dependencia para expresarse siquiera.

### `HumanInteractionResolution` — la resolución que un humano produjo

```pseudocode
STRUCT HumanInteractionResolution
    requestId: HumanInteractionRequestId
    outcome: HumanInteractionOutcome
    value: Optional<Value>
    resolvedBy: ActorId
    resolvedAt: Timestamp
END
```

`requestId` correlaciona esta resolución con la `HumanInteractionRequest` que resuelve — mismo
patrón de correlación que `ToolResult.callId` (CH-02) o `PolicyDecision.callId` (CH-05). `value`
reutiliza `Value` (CH-00, el mismo tipo genérico que ya usa `AgentEvent.payload`), poblado
**únicamente** cuando `outcome = PROVIDED` — la misma asimetría de diseño que
`PolicyDecision.reason` (CH-05), aplicada aquí a un campo de éxito en vez de a uno de fallo.
`resolvedBy` es, literalmente, el "actor" que INV-19 exige poder trazar: la primera vez que este
libro modela explícitamente quién — no solo qué regla o qué contexto — tomó una decisión crítica.

**Unchanged / Not yet introduced**: ningún campo de canal en ninguno de los dos contratos; ningún
`STRUCT Actor`/`User` que modele quién puede resolver qué tipo de solicitud; ningún tercer estado
`EXPIRED` en `HumanInteractionStatus`; y ningún `INTERFACE HumanInteractionService` con múltiples
`IMPLEMENTATION` (formalizarlo como interfaz — por ejemplo, distintos backends de persistencia —
queda para cuando este libro necesite modelar más de un mecanismo real de persistencia).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce dos contratos de
datos, registrados en `registry/contracts.yaml`:

```text
ID:                     C-015
Name:                   HumanInteractionRequest
Version:                v1
Introduced In:          CH-06
Current Definition:     STRUCT HumanInteractionRequest (ver §6)
Used By:                [CMP-006]
Modified By:            []
Constitutional Impact:  [INV-14, INV-15, INV-18, INV-19]
```

```text
ID:                     C-016
Name:                   HumanInteractionResolution
Version:                v1
Introduced In:          CH-06
Current Definition:     STRUCT HumanInteractionResolution (ver §6)
Used By:                [CMP-006]
Modified By:            []
Constitutional Impact:  [INV-14, INV-15, INV-18, INV-19]
```

`C-015` y `C-016` son el segundo y tercer id de contrato que este libro asigna sin que estuvieran
reservados desde CH-01 §7 — el correlativo simplemente continúa después de `C-014` (CH-05).

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el sexto componente de runtime del libro:

```pseudocode
COMPONENT HumanInteractionService
    consumes: ExecutionContext, PolicyDecision
    produces: HumanInteractionRequest, HumanInteractionResolution, AgentEvent, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Article III (sección "HumanInteractionService"):

```text
COMPONENT: HumanInteractionService

Responsibility:
    Representar una solicitud de intervención humana a partir de una PolicyDecision con
    outcome = REQUIRE_APPROVAL, persistirla mientras está pendiente, recibir su resolución y
    dejar disponible la información que permitiría reanudar la ejecución — sin decidir si esa
    aprobación se requiere, sin transportar la interacción por ningún canal concreto, sin
    ejecutar la acción una vez resuelta y sin decidir si el turno debe continuar.

Consumes:
    C-004 ExecutionContext, C-014 PolicyDecision

Depends on:
    (ninguno todavía — el cableado real con AgentLoop, ToolRuntime y PolicyEngine, y la
    persistencia real de SessionManager, son Preview, no introducidos en este capítulo; ver
    seccion 9)

Produces:
    C-015 HumanInteractionRequest, C-016 HumanInteractionResolution, C-010 AgentEvent
    (HUMAN_INTERACTION_REQUESTED / HUMAN_INTERACTION_RESOLVED), C-011 HarnessError

Owns (Article III, cita literal):
    - representar solicitudes humanas
    - persistir interacciones pendientes
    - recibir resoluciones
    - permitir reanudación

Does NOT own (Article IV — declarado con el mismo peso que Owns):
    - decidir SI una acción requiere aprobación humana (PolicyEngine, CMP-005, ya introducido en
      CH-05 — esa decisión ya se tomó cuando PolicyDecision.outcome = REQUIRE_APPROVAL; este
      componente solo recibe esa señal)
    - transportar la interacción a través de un canal concreto — TUI/Web/Slack/Teams/Mobile/
      Email/API (Channel Adapter, Article VIII/P-11 — concepto de infraestructura de borde, no un
      componente propio de Article III / del registry)
    - ejecutar la acción una vez resuelta (ToolRuntime, CMP-002, ya introducido en CH-02 —
      Article IV: "ToolRuntime → How should an approved action be executed?")
    - decidir si otro turno de razonamiento debe ocurrir o si la ejecución debe reanudarse
      operacionalmente (AgentLoop, CMP-001, ya introducido en CH-01)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con una
particularidad respecto a CH-01..CH-05: por primera vez, una de las exclusiones no apunta a un
componente (existente o preview) sino a un **concepto de infraestructura de borde** (Channel
Adapter) que este libro nunca modelará como `COMPONENT` propio — Article VIII asigna el
significado de la interacción al runtime, y el canal queda, por diseño, fuera del árbol de
componentes de Article III.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
HumanInteractionService
    consumes → ExecutionContext, PolicyDecision
    produces → HumanInteractionRequest, HumanInteractionResolution, AgentEvent, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`HumanInteractionService` no depende hoy de ningún otro componente registrado — mismo patrón que
CH-01..CH-05 ya establecieron para sus propios componentes. En prosa (nunca dentro de un bloque
`pseudocode`, per `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las relaciones
futuras que capítulos posteriores agregarán son:

| Componente / concepto futuro (Preview — no cableado en este capítulo) | Qué relación tendría con `HumanInteractionService` |
|---|---|
| `AgentLoop` (ya existente, CMP-001) | transicionaría `AgentRunStatus` a `WAITING_FOR_HUMAN` al recibir la señal de una `HumanInteractionRequest` recién creada, y reanudaría la ejecución al recibir una `HumanInteractionResolution` |
| `ToolRuntime` (ya existente, CMP-002) | esperaría una `HumanInteractionResolution` con `outcome = APPROVED` antes de llegar a `Execute`, cuando `PolicyEngine` devolvió `REQUIRE_APPROVAL` para el `ToolCall` en curso |
| `PolicyEngine` (ya existente, CMP-005) | seguiría siendo, exclusivamente, la fuente de la señal `REQUIRE_APPROVAL` que dispara `createHumanInteractionRequest` — la relación es unidireccional: `HumanInteractionService` lee `PolicyDecision`, nunca al revés |
| `SessionManager` (Article III, preview) | la persistencia real y durable de `HumanInteractionRequest`/`HumanInteractionResolution`, distinta de las primitivas asumidas de este capítulo (`persistHumanInteractionRequest`/`persistHumanInteractionResolution`, seccion 11) |
| Channel Adapter (concepto, no un `ComponentId` del registry) | transportaría la `HumanInteractionRequest` hacia `TUI`/`Web`/`Slack`/`Teams`/`Mobile`/`Email`/`API` (Article VIII) y traería de vuelta la respuesta cruda que este capítulo normaliza hacia una `HumanInteractionResolution` |

`registry/components.yaml` de `CMP-001` (`AgentLoop`) y `CMP-005` (`PolicyEngine`) **no se
modifica** en este capítulo: ninguno de los dos agrega `CMP-006` a su `dependencies`, y ninguno
cambia su pseudocódigo. El pseudocódigo de la seccion 11 muestra a `HumanInteractionService`
creando una `HumanInteractionRequest` a partir de una `PolicyDecision` y, más tarde, recibiendo una
`HumanInteractionResolution` — de forma completamente autónoma, sin que `AgentLoop` o
`PolicyEngine` cambien una sola línea para que este capítulo sea correcto. Ese cableado real
(que `PolicyEngine` invoque a `HumanInteractionService`, y que `AgentLoop` transicione en función de
su resultado) es, explícitamente, trabajo de un capítulo de integración futuro (ver seccion 18/19).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14), siguiendo el mismo esqueleto de "Human-in-the-loop" que
`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §15 ya anticipaba:

**Vista 1 — Componentes**

```text
[PolicyEngine — CH-05, conceptual, todavía no cablea esta llamada] → HumanInteractionService →
[Channel Adapter — concepto, no componente] → Human → HumanInteractionService →
[AgentLoop / ToolRuntime — Preview, cableado real de un capítulo posterior]
```

**Vista 2 — Sequence**

```text
PolicyDecision (outcome = REQUIRE_APPROVAL)
   │ (producida de forma autónoma por PolicyEngine, CH-05 — este capítulo no cablea esa llamada)
   ▼
HumanInteractionService
   │ createHumanInteractionRequest(decision, interactionType, execution, agentId)
   │ ¿decision.outcome == REQUIRE_APPROVAL?
   │     no  → HarnessError (POLICY_DECISION_NOT_REQUIRE_APPROVAL, VALIDATION)
   │     sí  → construye HumanInteractionRequest (status = PENDING)
   │           persiste la solicitud (persistHumanInteractionRequest, primitiva asumida)
   │           emite: AgentEvent (HUMAN_INTERACTION_REQUESTED)
   ▼
HumanInteractionRequest (PENDING)
   │
   ▼
[Channel Adapter — concepto, no componente — transportaría la solicitud hacia TUI/Web/Slack/
Teams/Mobile/Email/API (Article VIII) y traería de vuelta la respuesta cruda del humano]
   │
   ▼
Human
   │ aprueba | rechaza | provee un valor
   ▼
HumanInteractionService
   │ resolveHumanInteractionRequest(request, outcome, value, resolvedBy, execution, agentId)
   │ ¿request.status == RESOLVED?
   │     sí → HarnessError (REQUEST_ALREADY_RESOLVED, VALIDATION)
   │ ¿outcome corresponde al type de la solicitud?
   │     no → HarnessError (OUTCOME_TYPE_MISMATCH, HUMAN_INTERACTION)
   │     sí → construye HumanInteractionResolution
   │          persiste la resolución y la solicitud actualizada (status = RESOLVED)
   │          emite: AgentEvent (HUMAN_INTERACTION_RESOLVED)
   ▼
HumanInteractionResolution
   │
   ▼
[AgentLoop reanudaría la ejecución (RUNNING) / ToolRuntime retomaría Execute — Preview, cableado
formal de un capítulo posterior, ver seccion 9/18]
```

**Vista 3 — Pseudocódigo**

Ver §11: `createHumanInteractionRequest` y `resolveHumanInteractionRequest` son la primera
formalización ejecutable de "`HumanInteractionService` representa y resuelve una intervención
humana requerida" — construidas exclusivamente a partir de material que ya existe
(`PolicyDecision` desde CH-05, `ExecutionContext` desde CH-00) más los tipos nuevos de este
capítulo.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde
CH-00/CH-01/CH-02/CH-03/CH-04/CH-05.

```pseudocode
FUNCTION createHumanInteractionRequest(
    decision: PolicyDecision,
    interactionType: HumanInteractionType,
    execution: ExecutionContext,
    agentId: AgentId
) -> HumanInteractionRequest

    IF decision.outcome != REQUIRE_APPROVAL
        error: HarnessError = HarnessError(
            category = VALIDATION,
            code = "POLICY_DECISION_NOT_REQUIRE_APPROVAL",
            message = "createHumanInteractionRequest fue invocada con una PolicyDecision cuyo outcome no es REQUIRE_APPROVAL",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW error
    END

    request: HumanInteractionRequest = HumanInteractionRequest(
        id = newHumanInteractionRequestId(),
        type = interactionType,
        callId = decision.callId,
        status = PENDING,
        requestedAt = now()
    )

    persistHumanInteractionRequest(request)

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = HUMAN_INTERACTION_REQUESTED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = request
    )

    RETURN request
END
```

```pseudocode
FUNCTION resolveHumanInteractionRequest(
    request: HumanInteractionRequest,
    outcome: HumanInteractionOutcome,
    value: Optional<Value>,
    resolvedBy: ActorId,
    execution: ExecutionContext,
    agentId: AgentId
) -> HumanInteractionResolution

    IF request.status == RESOLVED
        error: HarnessError = HarnessError(
            category = VALIDATION,
            code = "REQUEST_ALREADY_RESOLVED",
            message = "resolveHumanInteractionRequest fue invocada sobre una HumanInteractionRequest que ya estaba RESOLVED",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW error
    END

    IF NOT outcomeMatchesRequestType(request.type, outcome)
        error: HarnessError = HarnessError(
            category = HUMAN_INTERACTION,
            code = "OUTCOME_TYPE_MISMATCH",
            message = "El outcome de la resolución no corresponde al type de la HumanInteractionRequest",
            recoverable = TRUE,
            retryable = FALSE,
            metadata = {}
        )
        THROW error
    END

    resolution: HumanInteractionResolution = HumanInteractionResolution(
        requestId = request.id,
        outcome = outcome,
        value = value,
        resolvedBy = resolvedBy,
        resolvedAt = now()
    )

    resolvedRequest: HumanInteractionRequest = HumanInteractionRequest(
        id = request.id,
        type = request.type,
        callId = request.callId,
        status = RESOLVED,
        requestedAt = request.requestedAt
    )

    persistHumanInteractionResolution(resolution)
    persistHumanInteractionRequest(resolvedRequest)

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = HUMAN_INTERACTION_RESOLVED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = resolution
    )

    RETURN resolution
END
```

`newEventId()` y `now()` son las mismas primitivas de CH-00..CH-05. `newHumanInteractionRequestId()`,
`persistHumanInteractionRequest(...)`, `persistHumanInteractionResolution(...)` y
`outcomeMatchesRequestType(...)` son primitivas nuevas de este capítulo, en el mismo espíritu que
`compact(...)`/`estimateTokens(...)` (CH-04) o `matchPolicyRule(...)` (CH-05): funciones
deterministas ya asumidas, no entidades arquitectónicas, sin ficha ni registro propio.
`persistHumanInteractionRequest(...)`/`persistHumanInteractionResolution(...)` operacionalizan
"persistir interacciones pendientes" (Article III, owns) sin modelar ningún mecanismo real de
almacenamiento — esa es, íntegramente, la responsabilidad futura de `SessionManager` (seccion 9).

Nótese que `resolvedRequest` se construye como una copia nueva, inmutable, de `request` con
`status = RESOLVED` — el mismo patrón que `AgentLoop.runTurn` (CH-01) usó para construir
`nextState` a partir de `state`, en vez de mutar la solicitud original in-place.

Nótese también lo que ninguna de las dos funciones hace: ninguna decide si una acción requiere
aprobación (`decision.outcome` ya llega decidido por `PolicyEngine`, CH-05), ninguna transporta la
solicitud o la respuesta por ningún canal concreto (Channel Adapter, fuera de alcance), ninguna
ejecuta la acción que la `PolicyDecision` original evaluaba (Article IV, "`ToolRuntime` → How
should an approved action be executed?" sigue sin respuesta aquí), y ninguna decide ningún
`AgentRunStatus` ni si otro turno debe ocurrir (Article IV, "`AgentLoop` → Should another reasoning
turn occur?" tampoco).

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013): esa máquina de estados sigue
siendo propiedad exclusiva de `AgentLoop` (CH-01 §12), y su tabla de transiciones no cambia aquí.

Sí introduce, por primera vez en el libro, el lifecycle propio y completo de un contrato distinto
de `AgentRunStatus` — el de `HumanInteractionStatus` (§6), con solo dos estados:

```text
HumanInteractionRequest creada (createHumanInteractionRequest)
   → status = PENDING

PENDING
   → resolveHumanInteractionRequest (outcome válido para el type de la solicitud) → RESOLVED
   → resolveHumanInteractionRequest (status ya RESOLVED)     → HarnessError (REQUEST_ALREADY_RESOLVED)
   → resolveHumanInteractionRequest (outcome no corresponde al type) → HarnessError (OUTCOME_TYPE_MISMATCH)

RESOLVED
   → (terminal para HumanInteractionStatus — no hay transición de vuelta a PENDING)
```

**Lo que este capítulo explícitamente no cierra**: `AgentRunStatus.WAITING_FOR_HUMAN` (C-013,
declarado desde CH-01 §6) sigue sin ser el destino de ninguna transición real de `AgentRunStatus`.
Este capítulo produce, por primera vez, un mecanismo completo (`HumanInteractionRequest` +
`HumanInteractionResolution`) capaz de justificar tanto la entrada a `WAITING_FOR_HUMAN` (cuando se
crea la solicitud) como la salida de ese estado (cuando se recibe la resolución) — pero decidir que
`AgentLoop` debe transicionar en función de estas señales sigue siendo trabajo de un capítulo
posterior que cablee `HumanInteractionService` con `AgentLoop` (ver seccion 18/19).
`book/chapters/01-agent-loop/chapter.md` no se modifica para reflejarlo todavía.

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6, extendido en la seccion 6 de este capítulo) clasifica
también los fallos que introduce este capítulo:

```text
VALIDATION
    createHumanInteractionRequest invocada con una PolicyDecision cuyo outcome no es
    REQUIRE_APPROVAL
        → recoverable: FALSE, retryable: FALSE
        → código: POLICY_DECISION_NOT_REQUIRE_APPROVAL (ver §11)
    resolveHumanInteractionRequest invocada sobre una HumanInteractionRequest ya RESOLVED
        → recoverable: FALSE, retryable: FALSE
        → código: REQUEST_ALREADY_RESOLVED (ver §11)

HUMAN_INTERACTION
    resolveHumanInteractionRequest invocada con un outcome que no corresponde al type de la
    solicitud (por ejemplo, PROVIDED sobre una solicitud de type = APPROVAL)
        → recoverable: TRUE, retryable: FALSE
        → código: OUTCOME_TYPE_MISMATCH (ver §11)
```

Este es el primer fallo real del libro clasificado bajo `category = HUMAN_INTERACTION` — un valor
que este mismo capítulo agrega a `ErrorCategory` (seccion 6), anticipado por nombre en Article VII
(`HumanInteractionError`) desde la primera versión de la Constitution, sin que ningún capítulo
anterior lo hubiera necesitado.

**La distinción que motiva separar `VALIDATION` de `HUMAN_INTERACTION` aquí**: los dos primeros
códigos (`POLICY_DECISION_NOT_REQUIRE_APPROVAL`, `REQUEST_ALREADY_RESOLVED`) son violaciones de
precondición del **llamador** — invocar una función sobre un objeto en el estado equivocado, el
mismo tipo de error que `AgentLoop.runTurn` (CH-01) clasifica como `TURN_ON_TERMINAL_STATE` bajo
`VALIDATION`. `OUTCOME_TYPE_MISMATCH` es distinto: no es que la operación se invocara en el momento
equivocado, sino que el **contenido** de la resolución no encaja con el dominio de la interacción
humana que dice resolver — un error específico de este dominio, no un genérico error de estado,
que por eso merece su propia categoría (`HUMAN_INTERACTION`) en vez de sumarse a `VALIDATION`.

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo de `category = PERSISTENCE`
que pudiera ocurrir al persistir realmente una `HumanInteractionRequest`/`HumanInteractionResolution`
— `persistHumanInteractionRequest`/`persistHumanInteractionResolution` (seccion 11) son primitivas
asumidas que, en este incremento, no fallan; esa semántica real pertenece a `SessionManager`
(preview, seccion 9/18).

## 14. Eventos Producidos (Events Produced)

Este capítulo agrega dos valores a `AgentEventType` (seccion 6):

```text
HUMAN_INTERACTION_REQUESTED   — HumanInteractionService creó y persistió una HumanInteractionRequest
                                 a partir de una PolicyDecision con outcome = REQUIRE_APPROVAL
                                 (createHumanInteractionRequest, §11)
HUMAN_INTERACTION_RESOLVED    — HumanInteractionService recibió y persistió una
                                 HumanInteractionResolution válida para una solicitud pendiente
                                 (resolveHumanInteractionRequest, §11)
```

**Por qué dos valores, y no un par éxito/fallo de una sola operación.** A diferencia de
`ToolRuntime`/`ModelGateway`/`ContextEngine` (que agregaron un par éxito/fallo cada uno) y a
diferencia de `PolicyEngine` (CH-05, que agregó un único valor porque su evaluación siempre produce
un resultado válido), este capítulo agrega dos valores porque `HumanInteractionService` posee **dos
operaciones reales**, no una: crear la solicitud y recibir su resolución. Cada una de las dos,
igual que `evaluatePolicyForToolCall` en CH-05, siempre produce un resultado válido una vez que su
precondición se satisface — los casos que sí pueden fallar
(`POLICY_DECISION_NOT_REQUIRE_APPROVAL`, `REQUEST_ALREADY_RESOLVED`, `OUTCOME_TYPE_MISMATCH`) son
violaciones de precondición del llamador, no un fallo operacional distinto de la operación misma —
mismo patrón que `TURN_ON_TERMINAL_STATE` en `AgentLoop` (CH-01), que tampoco emite un
`AgentEvent` paralelo cuando `runTurn` lanza su `HarnessError`.

`RUN_STARTED`, `TURN_CONTINUED`, `RUN_COMPLETED`, `RUN_FAILED` (CH-00/CH-01),
`TOOL_CALL_COMPLETED`/`TOOL_CALL_FAILED` (CH-02), `MODEL_RESPONSE_RECEIVED`/
`MODEL_INVOCATION_FAILED` (CH-03), `CONTEXT_SNAPSHOT_ASSEMBLED`/`CONTEXT_SNAPSHOT_FAILED` (CH-04) y
`POLICY_EVALUATED` (CH-05) no se emiten desde ninguna de las dos funciones de este capítulo:
pertenecen a dominios distintos. Un capítulo posterior que conecte `HumanInteractionService` con
`AgentLoop` podrá correlacionar un `HUMAN_INTERACTION_RESOLVED` con la siguiente transición de
`AgentRunStatus` sin redefinir el envelope común `AgentEvent` (C-010).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

Este es, de los seis capítulos reales del libro, el que más directamente materializa Article VIII
(Human Interaction Constitution) como código ejecutable en vez de como reglas declaradas sin
enforcement.

**Ningún campo de canal, en ningún contrato — por diseño.** La decisión central de este capítulo es
que ni `HumanInteractionRequest` ni `HumanInteractionResolution` (seccion 6) modelen de qué canal
llegó la solicitud o la respuesta. Esto es deliberado y merece explicarse: si cualquiera de los dos
contratos incluyera, por ejemplo, `channel: Text`, cada implementación futura de un Channel Adapter
podría verse tentada a hacer que el significado de "aprobado" dependiera de por dónde llegó la
respuesta (¿un `POST` HTTP sin autenticar cuenta igual que un mensaje de Slack verificado?) —
exactamente lo que INV-14 y la Human Interaction Rule prohíben ("las interfaces transportan la
interacción; el runtime define y persiste su significado"). Al no dejarle espacio a ese campo en el
contrato, INV-14 se preserva estructuralmente, no por disciplina de quien implemente el canal.

**Lo que este capítulo NO implementa todavía.** `createHumanInteractionRequest` y
`resolveHumanInteractionRequest` modelan únicamente el tramo "`HumanInteractionRequest` → Persist →
... → Resolution`" del flujo completo de Article VIII (`HumanInteractionRequest → Persist →
WAITING_FOR_HUMAN → Channel Adapter → Human → Resolution → Resume`):

- **`WAITING_FOR_HUMAN`**: este capítulo no transiciona ningún `AgentRunStatus` — sigue siendo,
  íntegramente, propiedad de `AgentLoop` (CH-01), sin cambios.
- **`Channel Adapter`**: no modelado como componente ni como mecanismo — Article VIII lista
  `TUI`/`Web`/`Slack`/`Teams`/`Mobile`/`Email`/`API` como canales posibles, pero este capítulo no
  implementa ninguno; `resolveHumanInteractionRequest` recibe `outcome`/`value`/`resolvedBy` ya
  resueltos, como señales de entrada asumidas (mismo patrón que `modelFinished` en CH-01 o
  `capabilityResolved` en CH-02).
- **`Resume`**: `HumanInteractionResolution` es el resultado que, en principio, permitiría
  reanudar la ejecución — pero ni `ToolRuntime` ni `AgentLoop` consultan todavía este contrato en
  ningún punto real de su pseudocódigo.
- **El cableado real `PolicyEngine → HumanInteractionService`**: `evaluatePolicyForToolCall`
  (CH-05 §11) todavía no invoca `createHumanInteractionRequest` en ningún punto — este capítulo
  deja a `HumanInteractionService` capaz de crear una solicitud a partir de cualquier
  `PolicyDecision` con `outcome = REQUIRE_APPROVAL`, pero la integración real es, explícitamente,
  trabajo de un capítulo posterior (ver seccion 9/18).

`HumanInteractionRequest`/`HumanInteractionResolution` son, por diseño, la forma en que este tramo
parcial se comunica — nunca una afirmación de que el flujo completo de Article VIII ya está
enforced de punta a punta.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST CreateHumanInteractionRequestRejectsAPolicyDecisionWhoseOutcomeIsNotRequireApproval
TEST CreateHumanInteractionRequestAlwaysStartsInPendingStatus
TEST CreateHumanInteractionRequestAlwaysEmitsAnAgentEvent
TEST ResolveHumanInteractionRequestRejectsAnAlreadyResolvedRequest
TEST ResolveHumanInteractionRequestRejectsAnOutcomeThatDoesNotMatchTheRequestType
TEST ResolveHumanInteractionRequestAlwaysEmitsAnAgentEvent
TEST HumanInteractionRequestAndResolutionNeverStoreAChannelOrTransportDetail
TEST HumanInteractionServiceNeverInvokesToolRuntimeOrAgentLoopDirectly
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.1, después de CH-06)

Constitution
 ├── Article I    — Principles (P-01 .. P-15)
 ├── Article II   — Invariants (INV-01 .. INV-20)
 ├── Article III  — Component Sovereignty (AgentLoop, ToolRuntime, ModelGateway, ContextEngine,
 │                  PolicyEngine, HumanInteractionService: seis componentes instanciados)
 ├── Article IV   — Decision Ownership (en uso: los seis componentes declaran owns/does_not_own)
 ├── Article VI   — Execution Constitution (tramo Policy Evaluation → Authorization → Human
 │                  Approval? parcialmente modelado; Execution Budget .. Sandbox sigue sin
 │                  componente)
 ├── Article VII  — Failure Constitution (ErrorCategory.HUMAN_INTERACTION ejercitado por primera
 │                  vez)
 └── Article VIII — Human Interaction Constitution (tramo HumanInteractionRequest → Persist → ...
                    → Resolution modelado; WAITING_FOR_HUMAN, Channel Adapter y Resume siguen sin
                    cablear)

Contracts (registry/contracts.yaml)
 ├── C-001 AgentMessage               (CH-00)
 ├── C-002 AgentConfig                (CH-00)
 ├── C-003 AgentState                 (CH-00)
 ├── C-004 ExecutionContext           (CH-00 — consumido ahora también por CMP-006)
 ├── C-005 ContextSnapshot            (CH-04)
 ├── C-006 ModelRequest               (CH-03)
 ├── C-007 ModelResponse              (CH-03)
 ├── C-008 ToolCall                   (CH-02)
 ├── C-009 ToolResult                 (CH-02)
 ├── C-010 AgentEvent                 (CH-00 — producido ahora también por CMP-006)
 ├── C-011 HarnessError               (CH-00 — producido ahora también por CMP-006)
 ├── C-012 ExecutionBudget            (CH-00)
 ├── C-013 AgentRunStatus             (CH-01)
 ├── C-014 PolicyDecision             (CH-05 — consumido ahora también por CMP-006)
 ├── C-015 HumanInteractionRequest    (CH-06, nuevo)
 └── C-016 HumanInteractionResolution (CH-06, nuevo)

Components (registry/components.yaml)
 ├── CMP-001 AgentLoop                (CH-01)
 ├── CMP-002 ToolRuntime              (CH-02)
 ├── CMP-003 ModelGateway             (CH-03)
 ├── CMP-004 ContextEngine            (CH-04)
 ├── CMP-005 PolicyEngine             (CH-05)
 └── CMP-006 HumanInteractionService  (CH-06, nuevo — sexto componente del libro)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado formal `PolicyEngine → HumanInteractionService`**: `evaluatePolicyForToolCall`
  (CH-05 §11) no invoca `createHumanInteractionRequest` en ningún punto — `PolicyEngine.dependencies`
  no agrega `CMP-006`, y `registry/components.yaml` de `CMP-005` no se modifica en este capítulo.
- **El cableado formal `HumanInteractionService ↔ AgentLoop`**: ninguna transición real hacia o
  desde `AgentRunStatus.WAITING_FOR_HUMAN` (declarado desde CH-01, nunca alcanzado) — decidir que
  `AgentLoop` debe transicionar al recibir una `HumanInteractionRequest`, y reanudar al recibir una
  `HumanInteractionResolution`, sigue siendo trabajo de un capítulo posterior.
- **El cableado formal `HumanInteractionService ↔ ToolRuntime`**: `ToolRuntime.executeToolCall`
  (CH-02 §11) no espera ninguna `HumanInteractionResolution` antes de `Execute` — INV-15 tiene, por
  primera vez, un mecanismo real que podría satisfacerla, pero todavía no un enforcement real que
  la haga cumplir en cada `ToolCall`.
- **Channel Adapter real**: ningún `TUI`/`Web`/`Slack`/`Teams`/`Mobile`/`Email`/`API` implementado
  — `outcome`/`value`/`resolvedBy` siguen siendo señales de entrada asumidas en
  `resolveHumanInteractionRequest`.
- **Expiración de una `HumanInteractionRequest`**: `HumanInteractionStatus` v1 solo tiene
  `PENDING`/`RESOLVED` — ningún tercer estado `EXPIRED` (a diferencia de `AgentRunStatus`, que sí lo
  tiene desde CH-01). Una v2 futura de este contrato podría agregarlo, declarándolo explícitamente
  en `modifies_contracts` del capítulo que lo haga.
- **Persistencia real de `HumanInteractionRequest`/`HumanInteractionResolution`**:
  `persistHumanInteractionRequest`/`persistHumanInteractionResolution` (seccion 11) son primitivas
  asumidas — `SessionManager` (Article III, preview) sigue sin existir como componente.
- **`ActorId` como identificador opaco, sin un `STRUCT Actor`/`User` propio**: quién puede resolver
  qué tipo de solicitud (autorización sobre la propia resolución humana) no se modela en este
  capítulo.
- **`ExecutionController` y el enforcement real de `ExecutionBudget`, `CapabilityRegistry`,
  Provider Adapters reales, streaming real**: deuda intencional heredada de CH-01..CH-05, sin
  cambios en este capítulo.
- **Persistencia real de `AgentState`/`SessionState`, reviewers plurales, evals y orquestación
  multi-agente**: sin cambios respecto a CH-00..CH-05 — explícitamente fuera de alcance de BH-v0.1.

## 19. Siguiente Incremento (Next Increment)

El problema natural del próximo capítulo: ahora que `HumanInteractionService` puede crear y resolver
una interacción humana de forma completamente autónoma (§11), ¿quién cablea, de una vez, los tres
extremos que este libro dejó deliberadamente sueltos — que `PolicyEngine` invoque a
`HumanInteractionService` cuando produce `REQUIRE_APPROVAL`, que `AgentLoop` transicione
`AgentRunStatus` hacia y desde `WAITING_FOR_HUMAN` en función de esa interacción, y que
`ToolRuntime` efectivamente espere una `HumanInteractionResolution` antes de `Execute`? Eso
apuntaría hacia un capítulo de integración que no introduce ningún componente nuevo, sino que cierra
el pipeline completo de Article VI (`Tool Intent → ... → Policy Evaluation → Authorization → Human
Approval? → Execution Budget → Sandbox → Execute → ...`) — y, en paralelo, hacia `SessionManager`
(Article IV: "What execution history and checkpoints persist?") como el séptimo componente
candidato de Article III que dejaría de ser preview, dándole a `persistHumanInteractionRequest`/
`persistHumanInteractionResolution` un mecanismo real en vez de una primitiva asumida.

Ese capítulo (`CH-07`, fuera del alcance de esta ejecución) heredaría directamente la deuda
intencional de §18. `next_chapter` queda en `null` en el frontmatter de este capítulo porque, en
este momento del libro, `CH-07` todavía no existe como archivo — solo como el problema que
motivará su escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg /
> Bucles de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows),
> secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): sin un dueño explícito para "¿quién representa y
   resuelve una aprobación humana pendiente?", la interfaz concreta por la que un humano responde
   tiende a decidir, cada una a su manera, qué significa "aprobado" — exactamente lo que Article
   VIII y P-11 prohíben.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): sin un componente
   con fronteras explícitas, `PolicyDecision.outcome = REQUIRE_APPROVAL` (CH-05) y
   `AgentRunStatus.WAITING_FOR_HUMAN` (CH-01) siguen siendo señales sin receptor, y una resolución
   de tipo "valor provisto" corre el riesgo de forzarse a un simple aprobado/rechazado.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `HumanInteractionService` (CMP-006) con una ficha que declara tanto lo que posee (`owns`:
   representar, persistir, recibir resoluciones, permitir reanudación) como lo que explícitamente
   NO posee (`does_not_own`, con una exclusión nueva: un concepto de infraestructura de borde, no
   un componente) y formaliza `HumanInteractionRequest` (C-015) y `HumanInteractionResolution`
   (C-016), el primer par solicitud/resolución modelado como dos contratos distintos desde CH-02.
4. **Modelos mentales** (= §4, Constitutional Impact): la Human Interaction Rule de Article VIII
   ("las interfaces transportan la interacción; el runtime define y persiste su significado") junto
   con INV-14 — Human Interaction nunca depende de una interfaz particular, preservado
   estructuralmente porque ningún contrato de este capítulo modela un campo de canal.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un componente nuevo se introduce sin declarar
  explícitamente su `does_not_own`, aumenta la probabilidad de que absorba silenciosamente la
  próxima decisión vecina "porque ya estaba ahí" — el mismo bucle que CH-01..CH-05 ya cortaron.
  Este capítulo lo repite para `HumanInteractionService`, con una variante: la tentación no viene
  de un componente vecino ya construido, sino de la superficie sin componente propio (el canal).
- **Bucle de equilibrio (estabiliza):** ni `HumanInteractionRequest` ni `HumanInteractionResolution`
  (§6) modelan ningún campo de canal — INV-14 se preserva porque el contrato mismo no le deja
  espacio a esa dependencia, no porque cada implementación lo respete por disciplina.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que ninguno de los dos contratos nuevos modele un
campo de canal, combinado con que `HumanInteractionOutcome` sea un `ENUM` de tres valores
(`APPROVED`/`REJECTED`/`PROVIDED`) en vez de un `Boolean`. Si un canal se filtrara como campo del
contrato, cada Channel Adapter futuro heredaría la posibilidad de cambiar el significado de una
resolución según por dónde llegó — lo que la Human Interaction Rule prohíbe explícitamente; y si
`HumanInteractionOutcome` colapsara a un booleano, una resolución de tipo `Input` perdería el valor
real que un capítulo de integración futuro necesitaría para reanudar la ejecución correctamente.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo
> de esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set`
> (frontmatter) y es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa,
> para lectura directa del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Cuando la evaluación de autorización del capítulo anterior produce un tercer resultado — ni
   permitido ni denegado, sino "todavía no, necesita que un humano lo apruebe" — ¿quién representa
   esa solicitud pendiente, la persiste, y qué le permite a la ejecución, eventualmente,
   reanudarse? *(cierra la pregunta guía 1)*
2. Si la interfaz por la que un humano llega a ver y resolver esa solicitud pendiente pudiera ser
   una terminal, una página web, un mensaje de chat o un correo, ¿debería esa interfaz decidir qué
   significa "aprobado" o qué datos persisten de la solicitud, o ese significado vive en otro
   lugar, indiferente al canal que se use? *(cierra la pregunta guía 2)*
3. Una vez que alguien resuelve una solicitud pendiente, ¿qué debería evitar que esa misma
   solicitud se resuelva una segunda vez, y qué información mínima debería acompañar a esa
   resolución para que, después, se pueda auditar quién la tomó? *(cierra la pregunta guía 3)*
4. Si el resultado de resolver una solicitud pendiente no es siempre un simple sí/no — a veces es
   un valor que el humano proporcionó como respuesta — ¿ese resultado debería forzarse a un
   booleano, y por qué el componente que representa y resuelve esa espera no debería, además,
   decidir si el turno continúa o ejecutar la acción una vez aprobada? *(cierra la pregunta guía 4)*

### Explicar

1. `HumanInteractionService` posee representar, persistir y resolver una solicitud de aprobación
   humana. Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee decidir SI
   esa aprobación se requiere en primer lugar — ¿qué se rompería, en concreto, si
   `HumanInteractionService` empezara a decidir por su cuenta cuándo una acción necesita
   aprobación, en vez de limitarse a recibir esa señal ya decidida?
2. `HumanInteractionResolution.outcome` es un `ENUM` de tres valores
   (`APPROVED`/`REJECTED`/`PROVIDED`), no un `Boolean`, y `value` solo se puebla cuando
   `outcome = PROVIDED`. Explica por qué forzar una resolución de tipo `Input` hacia
   `APPROVED`/`REJECTED` perdería información que un capítulo futuro necesitaría para reanudar la
   ejecución correctamente.

### Conectar

1. `PolicyEngine` (CH-05) produce `PolicyDecision.outcome = REQUIRE_APPROVAL` pero, explícitamente,
   no representa ni resuelve esa aprobación. ¿Qué campo de `PolicyDecision` necesita leer quien
   construya una `HumanInteractionRequest` para poblar `HumanInteractionRequest.callId`, y por qué
   ese campo es una correlación reutilizada en vez de una relación nueva hacia `PolicyDecision`?
2. `AgentRunStatus.WAITING_FOR_HUMAN` (CH-01) sigue sin ser el destino de ninguna transición real.
   ¿Qué produce este capítulo que, por primera vez, haría posible esa transición completa (entrada
   y salida), y por qué construir ese contrato no obliga a `AgentLoop` a cambiar una sola línea
   todavía?

### Espaciar

Las cinco tarjetas de repaso de este capítulo (dos sobre `HumanInteractionService` — su `owns` y su
`does_not_own` —, dos sobre `HumanInteractionRequest`/`HumanInteractionResolution` y sus campos, y
una sobre por qué `HumanInteractionOutcome` no es un `Boolean`) entran hoy en
`reviewStage = DAY_1`. Repásalas de nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) — ver
el apéndice de tarjetas al final del libro (edición PDF) o `retrieval_set.flashcards` en
`dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te
equivocaste, ese es precisamente el punto ciego que este método existe para revelar.
