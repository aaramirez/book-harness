---
id: CH-17
title: "IdempotencyGuard y la Deduplicación de un Side Effect Crítico"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-015]
introduces_contracts: [C-027]
modifies_contracts: []
constitutional_articles: [P-13, P-24, INV-11, INV-E09, INV-18, INV-19, INV-20]
previous_chapter: CH-16
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH17
    text: |
      Al terminar este capítulo podrás distinguir, para cualquier `ToolCall` con side effects que
      pueda entregarse más de una vez bajo la misma intención lógica (un reintento de red, una
      entrega duplicada de una cola, dos llamadas concurrentes), qué tramo le pertenece en
      exclusiva al componente que rastrea si esa ejecución ya ocurrió antes y decide si corresponde
      reusar el resultado ya producido — sin ejecutar el side effect en sí, sin decidir si la
      acción está autorizada, sin resolver qué implementación la satisface y sin decidir si un run
      puede seguir reintentando contra su presupuesto operacional — y podrás diseñar, para
      cualquier registro de una ejecución con side effects, un estado explícito de dos valores que
      distinga una ejecución todavía en curso de una ya terminada, en vez de colapsar ambas en un
      simple booleano "ya se hizo" / "no se ha hecho".
  skeleton:
    id: SK-CH17
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
    components_to_be_introduced: [CMP-015]
    contracts_to_be_introduced: [C-027]
  guiding_questions:
    - id: GQ-CH17-01
      text: |
        Cuando un `ToolCall` con side effects reales se entrega más de una vez bajo la misma
        intención lógica —por un reintento de red, una entrega duplicada de una cola, o dos
        llamadas concurrentes— ¿qué necesitaría existir para reconocer que ya se ejecutó antes, y
        decidir si el side effect real debe volver a ocurrir o si basta con reusar lo que ya se
        produjo?
      answered_by: RQ-CH17-01
    - id: GQ-CH17-02
      text: |
        La decisión de si un run puede seguir reintentando contra su presupuesto operacional ya
        tiene, en este libro, un dueño propio. ¿Esa misma pregunta sirve también para decidir si
        una ejecución concreta, ya exitosa, debe repetirse — o son, honestamente, dos preguntas
        distintas sobre materiales distintos?
      answered_by: RQ-CH17-02
    - id: GQ-CH17-03
      text: |
        Si dos peticiones que representan la misma intención lógica llegan casi al mismo tiempo,
        antes de que la primera haya terminado, ¿qué debería pasarle a la segunda — ejecutar el
        side effect de todos modos, fallar de inmediato, o esperar a que la primera termine?
      answered_by: RQ-CH17-03
    - id: GQ-CH17-04
      text: |
        Desde el primer capítulo de este libro, uno de los invariantes originales de la
        Constitution exige que los side effects críticos soporten alguna protección contra
        ejecutarse dos veces por accidente — sin que ningún componente, en dieciséis capítulos
        reales, haya reclamado jamás esa responsabilidad como propia. ¿Qué tendría que existir
        para que esa protección deje de ser solo una promesa declarada y se vuelva, por fin, código
        real?
      answered_by: RQ-CH17-04
  systems_lens:
    iceberg_visible_fact: |
      Diecisiete capítulos reales construyeron un runtime completo más tres componentes de
      Enterprise (`AdmissionController`, CH-14; `AgentCommunicationGateway`, CH-15;
      `CredentialBroker`, CH-16) — pero ningún componente rastreó jamás si un side effect con
      consecuencias reales ya se había ejecutado antes bajo la misma intención lógica.
      `ToolRuntime.executeToolCall` (CH-02 §11) sigue recibiendo `executionSucceeded`/
      `executionOutput` como señales externas asumidas, exactamente en el punto donde una
      repetición accidental del side effect ocurriría sin que nada lo impida (ver seccion 2, El
      Problema).
    iceberg_patterns: |
      `INV-11` (Article II, "Execution Invariants" — no Amendment v1.1) fue declarado desde CH-00,
      dentro de la tabla original de invariantes de la Constitution — pero nunca citado en prosa por
      ningún capítulo, y nunca resuelto por ningún componente en dieciséis capítulos reales; CH-08
      §18 llegó a nombrar explícitamente "idempotencia y semántica de reintentos de una capability
      (`P-24`, Amendment v1.1)" como "fuera de alcance, igual que en capítulos anteriores" — la
      misma deuda, señalada dos veces (Article II original y Amendment v1.1), resuelta recién en
      este capítulo (ver seccion 3, Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala el cuarto componente de este libro que no corresponde a ninguno de los
      once nombres de Article III — y, deliberadamente, el cuarto plano de Amendment v1.1 que este
      libro cubre (tras Ingress & Activation, CH-14; Agent Interoperability, CH-15; Capability &
      Integration, CH-16), aunque en la numeración canónica de la enmienda el "Reliability Plane"
      ocupa la séptima posición, no la cuarta — con una ficha que declara tanto lo que posee
      (`owns`: detectar si un `ToolCall` con side effects ya se ejecutó antes bajo la misma clave de
      idempotencia, decidir si corresponde reusar el `ToolResult` ya producido, registrar de forma
      terminal y write-once una ejecución nueva ya concluida) como lo que explícitamente NO posee
      (ejecutar el side effect, autorizar la acción, resolver la implementación, decidir si un run
      puede reintentar por presupuesto) (ver seccion 8, Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es que "¿ya se hizo esto antes?" es una
      pregunta completamente distinta de "¿puedo seguir intentando?" (`ExecutionController`, CH-07),
      de "¿está permitido hacerlo?" (`PolicyEngine`, CH-05), de "¿qué implementación lo hace?"
      (`CapabilityRegistry`, CH-08) y de "¿cómo se hace?" (`ToolRuntime`, CH-02) — cinco preguntas
      con dueños distintos que, sin este componente, corrían el riesgo de resolverse todas en el
      mismo lugar, con un side effect crítico ejecutándose dos veces cada vez que la respuesta a la
      primera pregunta se asumía en vez de verificarse (ver seccion 4, Impacto Constitucional).
    reinforcing_loop: |
      Cada vez que un sistema deja sin modelar esta protección, un reintento razonable —de red, de
      una cola de mensajes, de un usuario impaciente— se convierte en un side effect duplicado real:
      un cargo cobrado dos veces, un correo enviado dos veces, un recurso creado dos veces — el
      mismo bucle de "la ausencia de un dueño se vuelve una dependencia implícita" que ya combatieron
      `P-02` (CH-03), `P-19` (CH-15) e `INV-E08` (CH-16), ahora aplicado a la repetición de un side
      effect en vez de al modelo, al protocolo o al secreto.
    balancing_loop: |
      `checkIdempotency`/`recordIdempotentExecution` (seccion 11) son el mecanismo de equilibrio:
      antes de que un side effect se repita, `checkIdempotency` puede devolver un `IdempotencyRecord`
      ya conocido —para reusar en vez de repetir, o para esperar en vez de duplicar—, y
      `recordIdempotentExecution` nunca sobrescribe silenciosamente un registro terminal ya
      producido (`IDEMPOTENCY_RECORD_ALREADY_COMPLETED`).
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `IdempotencyRecordStatus` (parte de
      `IdempotencyRecord`, C-027) tenga exactamente dos valores explícitos — `PENDING`/`COMPLETED` —
      y que la ausencia misma de un registro (no un tercer valor de `ENUM`) sea lo que representa
      "nunca visto antes". Si `status` fuera un `Boolean`, no habría forma de distinguir una
      ejecución que ya terminó y puede reusarse de una que apenas empezó y todavía no debería
      duplicarse — exactamente la ambigüedad que `INV-11`/`P-24`/`INV-E09` exigen resolver.
  recall_questions:
    - id: RQ-CH17-01
      text: |
        ¿Qué componente rastrea si un `ToolCall` con side effects ya se ejecutó antes bajo la misma
        clave de idempotencia, y qué invariante original de la Constitution (declarado desde CH-00,
        nunca antes resuelto por ningún componente) cierra este capítulo?
      # respuesta esperada: IdempotencyGuard (CMP-015); INV-11.
    - id: RQ-CH17-02
      text: |
        ¿Qué campos tiene `IdempotencyRecord` (C-027), y por qué su campo `status` nunca es un
        `Boolean`?
    - id: RQ-CH17-03
      text: |
        ¿Qué debería pasar cuando dos ejecuciones concurrentes comparten la misma
        `idempotencyKey`, y qué valor de `IdempotencyRecordStatus` representa esa situación?
    - id: RQ-CH17-04
      text: |
        ¿Qué distingue "reintentar un run porque su presupuesto operacional todavía lo permite"
        (`ExecutionController`, CH-07) de "deduplicar una ejecución que ya ocurrió con éxito" (este
        capítulo)?
  explain_prompts:
    - id: EP-CH17-01
      text: |
        `IdempotencyGuard` posee detectar cuándo una ejecución con side effects ya ocurrió antes
        bajo la misma clave. Explica, como si hablaras con alguien sin contexto técnico, por qué NO
        posee ejecutar el side effect en sí — ¿qué se rompería si, dado que ya rastrea las
        ejecuciones, también las ejecutara directamente?
      target_entity: CMP-015
    - id: EP-CH17-02
      text: |
        `IdempotencyRecord` nunca modela con un solo campo `Boolean` si una ejecución "ya se hizo".
        Explica qué información real se perdería, y qué riesgo de duplicar un side effect
        introduciríamos, si `status` colapsara a dos valores booleanos simples en vez de distinguir
        explícitamente una ejecución todavía en curso de una ya terminada.
      target_entity: C-027
  interleaved_questions:
    - id: IQ-CH17-01
      text: |
        `ToolRuntime.executeToolCall` (CH-02) recibe `executionSucceeded`/`executionOutput` como
        señales externas asumidas, sin modelar nunca cómo se decide si ese side effect debe
        ejecutarse de nuevo o si ya se ejecutó antes bajo la misma intención lógica. Si este
        capítulo produjera, para un `ToolCall` (C-008) dado, un `IdempotencyRecord` ya `COMPLETED`
        con un `ToolResult` (C-009) reusable, ¿le correspondería a `executeToolCall` decidir
        ignorarlo y ejecutar de todos modos, o la pregunta de si ejecutar de nuevo pertenece, con
        dueño propio, a otro componente?
      current_chapter_entities: [CMP-015, C-027]
      prior_chapter_entities: [CMP-002, C-008, C-009]
      prior_chapter: CH-02
    - id: IQ-CH17-02
      text: |
        `ExecutionController` (CH-07) ya decide, con una `ExecutionDecision` de tres estados, si un
        `AgentRun` puede seguir operacionalmente contra su `ExecutionBudget` — incluyendo, en
        principio, si tendría sentido reintentar tras un fallo transitorio. Si esa misma ejecución
        representa un side effect que ya se completó con éxito la primera vez, ¿alcanza con que
        `ExecutionController` conceda continuar, o hace falta una pregunta completamente distinta —
        si ese side effect específico ya ocurrió, y si repetirlo sería seguro— con un dueño
        distinto?
      current_chapter_entities: [CMP-015, C-027]
      prior_chapter_entities: [CMP-007, C-017]
      prior_chapter: CH-07
  flashcards:
    - id: FC-CH17-01
      front: |
        ¿Qué posee `IdempotencyGuard`?
      back: |
        Detectar cuándo un `ToolCall` (C-008) con side effects ya se ejecutó antes bajo la misma
        clave de idempotencia (`INV-11`/`INV-E09`, citas literales); decidir si una ejecución
        repetida debe reusar el `ToolResult` (C-009) ya conocido en vez de que el side effect real
        vuelva a ejecutarse; registrar, de forma terminal y write-once, el `IdempotencyRecord`
        `COMPLETED` que resulta de una ejecución nueva ya concluida; y rechazar por defecto
        (fail-closed) cuando la clave encontrada corresponde a una capability distinta de la
        solicitada, o cuando se intenta re-registrar una ejecución ya `COMPLETED`.
      source_entity: CMP-015
      chapter_introduced_in: CH-17
      review_stage: DAY_1
    - id: FC-CH17-02
      front: |
        ¿Qué NO posee `IdempotencyGuard`?
      back: |
        Ejecutar el side effect en sí (`ToolRuntime`, CMP-002, CH-02 — decide SI debe ejecutarse de
        nuevo, nunca CÓMO); decidir si la acción está autorizada (`PolicyEngine`, CMP-005, CH-05);
        resolver qué implementación satisface la capability solicitada (`CapabilityRegistry`,
        CMP-008, CH-08); decidir si un `AgentRun` puede seguir operacionalmente contra su
        `ExecutionBudget`, incluyendo si reintentar tras un fallo (`ExecutionController`, CMP-007,
        CH-07 — pregunta ortogonal, ver seccion 15); ni generar la clave de idempotencia misma
        (asumida como señal de entrada dada).
      source_entity: CMP-015
      chapter_introduced_in: CH-17
      review_stage: DAY_1
    - id: FC-CH17-03
      front: |
        ¿Qué campos tiene `IdempotencyRecord` (C-027)?
      back: |
        `id` (`IdempotencyRecordId`), `idempotencyKey` (`Text`, asumida como dada), `capability`
        (`CapabilityId`, referencia opaca — nunca el `ToolCall` completo embebido), `originalToolCallId`
        (`ToolCallId`, referencia al `ToolCall` que primero reclamó esta clave), `status`
        (`IdempotencyRecordStatus`: `PENDING`/`COMPLETED`, nunca un `Boolean`), `result`
        (`Optional<ToolResult>`, poblado solo cuando `status = COMPLETED`), `createdAt` (`Timestamp`)
        y `completedAt` (`Optional<Timestamp>`, poblado solo cuando `status = COMPLETED`).
      source_entity: C-027
      chapter_introduced_in: CH-17
      review_stage: DAY_1
    - id: FC-CH17-04
      front: |
        ¿Por qué `IdempotencyRecord.status` es un `ENUM` de dos valores (`PENDING`/`COMPLETED`) y no
        un `Boolean alreadyExecuted`?
      back: |
        Porque un `Boolean` de dos estados solo distinguiría "visto antes" / "no visto antes", y eso
        no le dice a un llamador qué hacer: una ejecución `COMPLETED` significa que puede reusarse
        de inmediato el `ToolResult` ya producido; una ejecución `PENDING` significa que el side
        effect todavía está en curso y que repetirlo ahora lo duplicaría — la respuesta correcta es
        esperar, no reusar un resultado que todavía no existe. La ausencia total de un registro (no
        un tercer valor del `ENUM`) es lo que representa "nunca visto antes" — el mismo patrón que
        ya usó `CredentialReference.expiresAt: Optional<Timestamp>` (CH-16) para no inventar un
        estado que la ausencia de dato ya representa.
      source_entity: C-027
      chapter_introduced_in: CH-17
      review_stage: DAY_1
    - id: FC-CH17-05
      front: |
        ¿Qué invariante original de la Constitution, declarado desde CH-00 y nunca antes resuelto
        por ningún componente, cierra este capítulo?
      back: |
        `INV-11` (Article II, "Execution Invariants"): "Side effects críticos deben soportar
        idempotencia, deduplicación o una protección equivalente." Listado en `constitutional_articles`
        de CH-00 desde el primer capítulo del libro, pero nunca citado en prosa ni resuelto por
        ningún componente hasta `IdempotencyGuard` — la misma deuda que Amendment v1.1 retoma,
        dieciséis capítulos después, con `P-24`/`INV-E09` y el "Reliability Plane".
      source_entity: CMP-015
      chapter_introduced_in: CH-17
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH17-01
      recall_question: RQ-CH17-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH17-02
      recall_question: RQ-CH17-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH17-03
      recall_question: RQ-CH17-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH17-04
      recall_question: RQ-CH17-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 17 — IdempotencyGuard y la Deduplicación de un Side Effect Crítico

> **Regla constitucional (Article II, `INV-11`, declarada desde CH-00):** "Side effects críticos
> deben soportar idempotencia, deduplicación o una protección equivalente."
>
> **Regla constitucional (Amendment v1.1, `P-24`):** "Capabilities with externally visible side
> effects MUST declare idempotency, retry and duplicate-delivery behavior." (`INV-E09`: "Every
> side-effecting capability declares idempotency and retry semantics.")

CH-14, CH-15 y CH-16 abrieron el territorio de Amendment v1.1 con tres planos consecutivos —
Ingress & Activation (`AdmissionController`), Agent Interoperability (`AgentCommunicationGateway`)
y Capability & Integration (`CredentialBroker`). Este capítulo entra al **cuarto plano que este
libro cubre** — pero, a diferencia de los tres anteriores, no avanza ni retrocede dentro del orden
canónico que la enmienda enumera por proximidad: salta directamente al **Reliability Plane**, que
en esa lista ocupa la **séptima** posición (Ingress & Activation → Execution → Agent
Interoperability → Capability & Integration → Data & Context → Control → **Reliability** →
Observability & Governance → Execution Fabric), no la cuarta — verificado con grep directo contra
`constitution/ARCHITECTURE_CONSTITUTION.md`, sin asumir el orden de memoria.

La razón de este salto es distinta de la que motivó los tres capítulos anteriores. `CredentialBroker`
(CH-16), `AgentCommunicationGateway` (CH-15) y `AdmissionController` (CH-14) existen porque Amendment
v1.1 los **nombra literalmente** dentro de un invariante (`INV-E08`, `P-19`, `P-17`). Ningún texto de
la Constitution — ni Article II original ni Amendment v1.1 — nombra literalmente un componente para
resolver idempotencia: `P-24`/`INV-E09` describen la exigencia ("toda capability con side effects
visibles externamente DEBE declarar comportamiento de idempotencia, retry y entrega duplicada"), pero
ninguno de los dos acuña un nombre propio. El nombre `IdempotencyGuard` que este capítulo adopta es,
por lo tanto, una **síntesis de este libro** — no una cita literal de un nombre ya existente en la
Constitution — evaluada explícitamente contra alternativas (`DeduplicationBroker`,
`SideEffectLedger`) y elegida porque "Guard" describe con precisión lo que este componente hace:
interceptar, antes de que un side effect se repita, para decidir si debe dejarlo pasar, hacerlo
esperar, o entregarle un resultado ya conocido — nunca ejecutar nada él mismo (ver seccion 8).

Lo que sí motiva, con la misma fuerza que una cita literal, este capítulo y este momento del libro es
`INV-11` — un invariante del **Article II original** de la Constitution, no de Amendment v1.1,
declarado en la tabla de invariantes de CH-00 desde el primer capítulo real de este libro, y nunca
resuelto por ningún componente en los dieciséis capítulos que siguieron. CH-08 §18 llegó incluso a
nombrar explícitamente la mitad de Amendment v1.1 de este mismo problema ("Idempotencia y semántica
de reintentos de una capability, `P-24`") como "fuera de alcance, igual que en capítulos anteriores".
Este capítulo cierra esa deuda — la más antigua de las dos (`INV-11`, CH-00) y la más reciente
(`P-24`/`INV-E09`, Amendment v1.1) — con un componente real. Los cinco planos restantes de Amendment
v1.1 (Execution, Data & Context, Control, Observability & Governance, Execution Fabric) quedan, otra
vez deliberadamente, para incrementos futuros (ver seccion 19).

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de saber
> cómo se llama el componente de este capítulo. El detalle estructurado de esta sección vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, para cualquier `ToolCall` con
side effects que pueda entregarse más de una vez bajo la misma intención lógica (un reintento de
red, una entrega duplicada de una cola, dos llamadas concurrentes), qué tramo le pertenece en
exclusiva al componente que rastrea si esa ejecución ya ocurrió antes y decide si corresponde reusar
el resultado ya producido — sin ejecutar el side effect en sí, sin decidir si la acción está
autorizada, sin resolver qué implementación la satisface y sin decidir si un run puede seguir
reintentando contra su presupuesto operacional — y podrás diseñar, para cualquier registro de una
ejecución con side effects, un estado explícito de dos valores que distinga una ejecución todavía en
curso de una ya terminada, en vez de colapsar ambas en un simple booleano.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e introduce
un contrato de datos nuevo y el cuarto componente de este libro que pertenece a Amendment v1.1 en vez
de a los once nombres originales de Article III.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar atrás;
están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este capítulo va
a definir):

1. Cuando un `ToolCall` con side effects reales se entrega más de una vez bajo la misma intención
   lógica —por un reintento de red, una entrega duplicada de una cola, o dos llamadas concurrentes—
   ¿qué necesitaría existir para reconocer que ya se ejecutó antes, y decidir si el side effect real
   debe volver a ocurrir o si basta con reusar lo que ya se produjo?
2. La decisión de si un run puede seguir reintentando contra su presupuesto operacional ya tiene, en
   este libro, un dueño propio. ¿Esa misma pregunta sirve también para decidir si una ejecución
   concreta, ya exitosa, debe repetirse, o son, honestamente, dos preguntas distintas sobre
   materiales distintos?
3. Si dos peticiones que representan la misma intención lógica llegan casi al mismo tiempo, antes de
   que la primera haya terminado, ¿qué debería pasarle a la segunda — ejecutar el side effect de
   todos modos, fallar de inmediato, o esperar a que la primera termine?
4. Desde el primer capítulo de este libro, uno de los invariantes originales de la Constitution
   exige que los side effects críticos soporten alguna protección contra ejecutarse dos veces por
   accidente — sin que ningún componente, en dieciséis capítulos reales, haya reclamado jamás esa
   responsabilidad como propia. ¿Qué tendría que existir para que esa protección deje de ser solo
   una promesa declarada y se vuelva, por fin, código real?

## 1. Arquitectura Actual (Current Architecture)

CH-00..CH-16 dejaron instalados veintiséis contratos de datos y catorce componentes: los once
nombres completos de Article III ("Agent Runtime"), dos capítulos de integración, y tres componentes
de Amendment v1.1 (`AdmissionController`, CMP-012, CH-14; `AgentCommunicationGateway`, CMP-013,
CH-15; `CredentialBroker`, CMP-014, CH-16). Ninguno de los catorce resolvió jamás, con código real,
si un side effect ya se había ejecutado antes bajo la misma intención lógica.

`ToolCall` (C-008, CH-02 §6) y `ToolResult` (C-009, CH-02 §6) siguen siendo, exactamente, los mismos
seis y cinco campos definidos en CH-02: ningún campo de `ToolCall` correlaciona dos intentos de la
misma intención lógica entre sí, y ningún campo de `ToolResult` indica si ese resultado ya fue
producido antes y podría reusarse. `ToolRuntime.executeToolCall` (CH-02 §11) recibe
`executionSucceeded`/`executionOutput` como señales externas ya asumidas — exactamente en el punto
donde una ejecución repetida del side effect ocurriría, si es que ocurre, sin que nada en el
pseudocódigo de ese capítulo lo detecte ni lo impida. CH-02 nunca reclamó cerrar ese hueco, y ningún
capítulo posterior lo cerró tampoco.

`ExecutionController` (CMP-007, CH-07) sí produce, desde su propio capítulo, una `ExecutionDecision`
de tres estados (`CONTINUE`/`STOP`/`CANCELLED`) que evalúa si un `AgentRun` puede seguir
operacionalmente contra su `ExecutionBudget` — pero esa evaluación se hace exclusivamente contra
contadores de uso agregado (turnos, tool calls, tokens, costo, tiempo, concurrencia); en ningún
momento pregunta si una `ToolCall` específica, identificada por una intención lógica concreta, ya
produjo un side effect real la primera vez que se intentó. Un run puede tener presupuesto de sobra
(`ExecutionDecision.outcome = CONTINUE`) y, aun así, estar a punto de duplicar un cargo ya cobrado si
nada más lo detiene — el presupuesto y la deduplicación son, literalmente, dos preguntas ortogonales
(ver seccion 15).

La Constitution ya señala esta exigencia desde dos lugares distintos, uno original y uno de Amendment
v1.1:

- `INV-11` (Article II, "Execution Invariants"): "Side effects críticos deben soportar idempotencia,
  deduplicación o una protección equivalente." — listado en `constitutional_articles` de CH-00 desde
  el primer capítulo real de este libro (verificado con grep directo sobre
  `book/chapters/00-arquitectura-constitucion/chapter.md`: `INV-11` aparece únicamente en esa lista
  de frontmatter, nunca citado en prosa dentro del cuerpo de CH-00 ni de ningún capítulo posterior
  hasta este).
- `P-24` ("Side effects require idempotency semantics"): "Capabilities with externally visible side
  effects MUST declare idempotency, retry and duplicate-delivery behavior."; `INV-E09`: "Every
  side-effecting capability declares idempotency and retry semantics."

Y esta misma deuda ya fue nombrada, en prosa, por un capítulo anterior sin que se resolviera: CH-08
§18 escribió literalmente "Idempotencia y semántica de reintentos de una capability (`P-24`,
Amendment v1.1): fuera de alcance de BH-v0.1, igual que en capítulos anteriores" — la mitad de
Amendment v1.1 de este problema, señalada y diferida, dos capítulos antes de que `CredentialBroker`
(CH-16) o `AgentCommunicationGateway` (CH-15) existieran siquiera.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas para esto, "¿ya se ejecutó este side effect antes?" tiende
a resolverse de la forma más peligrosa posible: no resolverse en absoluto. Un reintento de red tras un
timeout, una entrega duplicada de una cola de mensajes, o dos llamadas concurrentes que representan
la misma intención del usuario, terminan ejecutando el mismo side effect real dos veces — un cargo
cobrado dos veces, un correo enviado dos veces, un recurso creado dos veces. Ninguna de estas rutas es
hipotética: son, literalmente, el comportamiento por defecto de cualquier sistema que trate cada
`ToolCall` como si fuera, por definición, la primera y única vez que esa intención se intenta.

Hay una segunda dimensión del problema, tan real como la primera. Aun si alguien intentara resolver
esto de forma improvisada, "¿ya se hizo esto?" se confunde con facilidad con preguntas que ya tienen
dueño en este libro: `ExecutionController` (CH-07) decide si un run puede seguir *operacionalmente*
contra su presupuesto — eso no dice nada sobre si un side effect *específico* ya produjo su resultado
la primera vez. `PolicyEngine` (CH-05) decide si una acción está *autorizada* — una `ToolCall` puede
estar perfectamente autorizada y, aun así, ser una repetición exacta de otra ya ejecutada con éxito.
`CapabilityRegistry` (CH-08) decide qué implementación satisface la capability — eso tampoco dice
nada sobre si esta invocación concreta de esa implementación ya ocurrió. Sin un dueño propio para
"¿ya se ejecutó esto?", cualquiera de esos tres componentes corre el riesgo de absorber la pregunta
silenciosamente, o —peor— de que nadie la responda nunca.

Hay una tercera dimensión, más sutil: la concurrencia. Si dos peticiones que representan la misma
intención lógica llegan casi al mismo tiempo, y la primera todavía no ha terminado de ejecutar su
side effect cuando llega la segunda, un sistema que solo distinga "ya se hizo" / "no se ha hecho" con
un simple booleano no tiene forma de representar el caso intermedio: la segunda no debería ejecutar
el side effect de nuevo (duplicaría), pero tampoco hay todavía ningún resultado que reusar (la primera
no ha terminado). La respuesta correcta —esperar— exige un tercer estado real, no dos.

Necesitamos que "¿ya se ejecutó este `ToolCall` bajo esta clave de idempotencia, y qué corresponde
hacer con una repetición?" tenga, por fin, un dueño único y nombrado — que reciba un `ToolCall` (C-008)
ya resuelto (nunca decida, de nuevo, si está autorizado o qué implementación lo satisface — eso ya lo
resolvieron `PolicyEngine` y `CapabilityRegistry`), que nunca ejecute el side effect en sí (eso sigue
siendo de `ToolRuntime`), que nunca decida si el run puede seguir contra su presupuesto (eso sigue
siendo de `ExecutionController`), y que distinga, con un estado explícito de más de dos valores
booleanos posibles, una ejecución todavía en curso de una ya terminada.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los veintiséis contratos y los catorce componentes que existen hasta este punto no bastan porque:

- `INV-11` (Article II) fue declarado desde CH-00, dentro de la tabla original de invariantes de la
  Constitution — pero, verificado con grep, nunca fue citado en prosa por ningún capítulo posterior,
  y ningún componente registrado lo reclamó jamás como propio;
- `P-24`/`INV-E09` (Amendment v1.1) retoman, dieciséis capítulos después, exactamente la misma
  exigencia — y CH-08 §18 ya la había nombrado explícitamente como "fuera de alcance", dos capítulos
  antes de que existiera ningún componente de Amendment v1.1 en este libro;
- `ToolCall` (C-008) y `ToolResult` (C-009), sin cambiar de forma desde CH-02, no tienen ningún campo
  que correlacione dos intentos de la misma intención lógica entre sí, ni ningún campo que indique si
  un resultado ya fue producido antes y podría reusarse;
- `ToolRuntime.executeToolCall` (CH-02 §11) trata `executionSucceeded`/`executionOutput` como señales
  externas asumidas, exactamente en el tramo donde una repetición accidental del side effect
  ocurriría — nunca modeló, ni reclamó modelar, si esa ejecución ya había sucedido antes;
- `ExecutionController.evaluateExecutionContinuation` (CH-07 §11) evalúa exclusivamente contadores de
  uso agregado contra `ExecutionBudget` — nunca evaluó, ni podría evaluar sin invadir Decision
  Ownership, si un side effect específico ya produjo su resultado; un run con presupuesto de sobra
  puede, sin este capítulo, duplicar un side effect que el presupuesto nunca tuvo forma de detectar
  (ver seccion 15 para el contraste completo);
- ningún `ENUM` de este libro representa, todavía, un estado de "ejecución en curso, no duplicar
  todavía, pero tampoco hay resultado que reusar" — `AgentRunStatus` (C-013) y `ExecutionOutcome`
  (CH-07) describen el estado de un *run* completo, nunca el de un side effect individual identificado
  por una clave.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la secuencia
> `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una entidad que no
> haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT` registrado — **no
> magic entities**. Este capítulo aplica la misma disciplina que CH-00..CH-16 ya establecieron, con
> una particularidad: es el primer componente de este registry cuyo `owns` se ancla, ante todo, en
> un invariante del **Article II original** de la Constitution (`INV-11`) — no solo en Amendment
> v1.1 — que ningún capítulo anterior había citado siquiera en prosa.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-13   Authorization is deterministic and external to the LLM.
           El mismo argumento que ya protegió la autorización desde CH-01/CH-05, y la credencial
           desde CH-16, se extiende aquí a la deduplicación: el modelo nunca decide, nunca ve y
           nunca constituye una fuente de verdad sobre si un side effect ya se ejecutó antes —
           checkIdempotency/recordIdempotentExecution (seccion 11) son completamente
           determinísticos y externos al LLM.
    P-24   Side effects require idempotency semantics.
           Primera materialización real, con código, de este principio en todo el libro —
           IdempotencyRecord (seccion 6/7), después de que CH-08 §18 solo lo hubiera citado en
           prosa como "fuera de alcance, igual que en capítulos anteriores".

Invariants preserved
    INV-11    Side effects críticos deben soportar idempotencia, deduplicación o una protección
              equivalente.
              Cita literal y definitoria de este capítulo completo — el invariante más antiguo de
              todo el libro en recibir, por fin, un componente propio: declarado en la tabla de
              CH-00 desde el primer capítulo real, nunca citado en prosa ni resuelto hasta
              IdempotencyGuard (seccion 8).
    INV-E09   Every side-effecting capability declares idempotency and retry semantics.
              Segunda cita literal del mismo problema, esta vez desde Amendment v1.1 —
              IdempotencyRecord (seccion 6/7) materializa la mitad de "idempotency" que este
              invariante exige; la mitad de "retry semantics" queda explícitamente fuera de alcance
              (ver seccion 15/18: reintentar es una decisión de ExecutionController, no de este
              componente).
    INV-18    Toda acción significativa produce un evento observable.
              checkIdempotency y recordIdempotentExecution (seccion 11) emiten un AgentEvent en
              cada rama relevante — a diferencia de AdmissionController (CH-14) y
              AgentCommunicationGateway (CH-15), este componente sí produce eventos reales (ver
              seccion 14 para el porqué), la misma situación de CapabilityRegistry (CH-08) y
              CredentialBroker (CH-16).
    INV-19    Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy relevante.
              Cada AgentEvent que emite IdempotencyGuard lleva el traceId de su ExecutionContext, y
              el IdempotencyRecord producido correlaciona, por su campo capability y por
              originalToolCallId, con el ToolCall exacto que primero reclamó esa clave.
    INV-20    Todo error operacional pertenece a una categoría conocida.
              Los dos fallos reales de este capítulo (seccion 13) introducen IDEMPOTENCY, una
              categoría nueva de ErrorCategory — ninguna de las quince ya existentes (incluida
              VALIDATION, que pertenece a fallos de forma/esquema, y BUDGET, que pertenece a límites
              operacionales agregados) representa, sin conflación, un conflicto de deduplicación.

Component ownership changes
    CMP-015 IdempotencyGuard se introduce — registry/components.yaml pasa de 14 a 15 componentes.
    Es el cuarto componente de este registry que NO corresponde a ninguno de los once nombres del
    árbol de Article III ("Agent Runtime") — pertenece, en cambio, al "Reliability Plane" de
    Amendment v1.1 (el séptimo plano canónico, cuarto que este libro cubre — ver apertura del
    capítulo). registry/components.yaml de CMP-002 (ToolRuntime) y CMP-007 (ExecutionController)
    NO se modifica: ninguno cablea todavía su relación real con IdempotencyGuard (ver seccion 9/18).

Lifecycle changes
    Ninguna modificación a AgentRunStatus (C-013): este capítulo no construye, ni transiciona,
    ningún AgentState. IdempotencyRecord introduce su propio ENUM de estado —
    IdempotencyRecordStatus (PENDING/COMPLETED, seccion 6) — a diferencia de CredentialReference
    (CH-16) o DelegationGrant (CH-15), cuya vigencia se derivaba de comparar fechas: aquí sí hace
    falta un ENUM propio porque la ausencia de vigencia no es lo mismo que "en curso" (ver seccion
    12 para el porqué explícito).

Security implications
    IdempotencyGuard es el primer componente de este libro cuya responsabilidad completa es
    prevenir que un side effect crítico ya ejecutado vuelva a ejecutarse. Ver seccion 15 para el
    análisis completo, incluyendo el contraste central con ExecutionController.

Observability implications
    A diferencia de AdmissionController (CH-14, el run todavía no existe) y AgentCommunicationGateway
    (CH-15, AgentCommunicationMessage no tiene sessionId), IdempotencyGuard SÍ produce AgentEvent en
    la práctica — el run cuyo ToolCall necesita deduplicación ya existe con
    runId/sessionId/agentId/traceId completos, la misma situación que CapabilityRegistry (CH-08) y
    CredentialBroker (CH-16). Ver seccion 14.

Deterministic vs agentic boundary
    Article XII se refina una decimoquinta vez a nivel de componente: IdempotencyGuard, igual que
    CredentialBroker (CH-16), no interpreta ninguna salida del modelo — compara,
    determinísticamente, un ToolCall ya resuelto y una clave de idempotencia ya asumida contra un
    registro de ejecuciones que el harness controla por completo. El modelo ni siquiera es
    consciente de que esta verificación ocurrió.
```

## 5. Conceptos Nuevos (New Concepts)

- **Idempotency / Idempotent Execution** *(cita literal, `INV-11`/`P-24`/`INV-E09`)*: la propiedad de
  que ejecutar un side effect crítico más de una vez, bajo la misma intención lógica, produzca el
  mismo efecto neto que ejecutarlo una sola vez — nunca un efecto duplicado. Este libro no modela
  cómo lograr que un side effect *individual* sea intrínsecamente idempotente (eso depende de la
  implementación concreta que envuelve, fuera de este registry); modela, en cambio, el mecanismo que
  **detecta** una repetición antes de que el side effect vuelva a dispararse (ver `IdempotencyGuard`,
  seccion 8).
- **Idempotency Key**: el identificador, provisto por quien origina la intención lógica, que
  correlaciona dos o más intentos del mismo `ToolCall` entre sí. Quién genera esta clave, y con qué
  algoritmo, queda **fuera de alcance de este capítulo** — se asume como dada, igual que otros
  capítulos de este libro asumen señales de entrada (`credentialBelongsToCapability` en CH-16,
  `argumentsMatchSchema` en CH-08). Modelada como `IdempotencyRecord.idempotencyKey: Text` (seccion
  6).
- **Deduplication** *(lectura de `INV-11`, "deduplicación")*: el acto de reconocer que un intento de
  ejecución corresponde a una intención lógica ya vista, y decidir reusar el resultado ya producido
  en vez de repetir el side effect real.
- **Duplicate Delivery** *(cita literal, `INV-E09`/`P-24`, "duplicate-delivery")*: el escenario que
  motiva todo este capítulo — la misma petición lógica entregada más de una vez por una causa externa
  al harness (un reintento de red, una cola de mensajes que garantiza entrega "at-least-once", un
  cliente que reenvía tras no recibir respuesta a tiempo). `IdempotencyGuard` no elimina la entrega
  duplicada en sí (eso depende del transporte, fuera de este registry) — hace que esa duplicidad deje
  de traducirse en un side effect duplicado.
- **Concurrent Execution Guard**: la exigencia, más sutil que la simple deduplicación de intentos ya
  terminados, de que una segunda ejecución concurrente bajo la misma `idempotencyKey` — mientras la
  primera todavía está en curso — espere en vez de duplicar el side effect. Modelada, de forma
  mínima, mediante `IdempotencyRecordStatus.PENDING` (seccion 6); el mecanismo real que hace esperar
  a esa segunda ejecución (colas, locks, polling) es Preview (ver seccion 18).
- **Decision Ownership** *(Article IV, en uso desde CH-01, aplicado aquí por cuarta vez a un
  componente de Amendment v1.1)*: `IdempotencyGuard` decide "¿ya se ejecutó este `ToolCall` bajo esta
  clave, y qué corresponde hacer con una repetición?"; explícitamente NO decide "¿cómo se ejecuta el
  side effect?" (`ToolRuntime`, CH-02), "¿está autorizada esta acción?" (`PolicyEngine`, CH-05), "¿qué
  implementación satisface esta capability?" (`CapabilityRegistry`, CH-08) ni "¿puede este run seguir
  contra su presupuesto, incluyendo si reintentar?" (`ExecutionController`, CH-07 — ver seccion 15
  para el contraste completo, el más importante de este capítulo).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `AgentId`, `CapabilityId`, `ToolCallId`, `Timestamp`,
`Text`, `Boolean`, `Optional`, `ExecutionContext` (C-004, CH-00), `AgentEvent` (C-010, CH-00),
`HarnessError` (C-011, CH-00), `ToolCall` (C-008, CH-02), `ToolResult` (C-009, CH-02).

### Un identificador opaco nuevo

Siguiendo el mismo patrón que CH-00 §6 estableció para los identificadores fundamentales, y que
CH-14/CH-15/CH-16 repitieron para los suyos:

| Identificador (nuevo de este capítulo) | Identifica |
|---|---|
| `IdempotencyRecordId` | un `IdempotencyRecord` concreto — el registro de que un `ToolCall` con side effects ya se vio antes bajo una `idempotencyKey` dada |

### `ErrorCategory` — extendido, sin redefinir `HarnessError`

Este es el sexto capítulo que agrega un valor a `ErrorCategory` desde que CH-00 lo declaró (después de
`HUMAN_INTERACTION`, CH-06; `ADMISSION`, CH-14; `DELEGATION`, CH-15; y `CREDENTIAL`, CH-16): el valor
`IDEMPOTENCY`, necesario porque ninguna de las quince categorías ya existentes representa, sin
conflación, un conflicto de deduplicación — `VALIDATION` pertenece, en exclusiva, a fallos de
forma/esquema de una intención de acción (CH-02/CH-08), y `BUDGET` pertenece, en exclusiva, a límites
operacionales agregados de un run completo (CH-07); ninguna de las dos representa, sin conflación,
"esta clave de idempotencia no corresponde a lo que se está pidiendo" o "esta ejecución ya se registró
como terminada":

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
    ADMISSION
    DELEGATION
    CREDENTIAL
    IDEMPOTENCY
END
```

`HarnessError` (C-011) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — mismo patrón
exacto que las extensiones de CH-06/CH-14/CH-15/CH-16, aplicado aquí por quinta vez a `ErrorCategory`.

### `AgentEventType` — extendido, sin redefinir `AgentEvent`

CH-16 dejó `AgentEventType` en veintidós valores. Este capítulo agrega cuatro valores — los primeros
eventos que observan la deduplicación de una ejecución, no su resolución ni su credencial:

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
    CREDENTIAL_RESOLVED
    CREDENTIAL_RESOLUTION_FAILED
    IDEMPOTENT_EXECUTION_DETECTED
    IDEMPOTENCY_CHECK_FAILED
    IDEMPOTENT_EXECUTION_RECORDED
    IDEMPOTENCY_RECORD_CONFLICT
END
```

`AgentEvent` (C-010) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — solo el rango de
valores permitido para `eventType` crece, igual que en cada capítulo anterior salvo `EventBus`
(CH-09), `AdmissionController` (CH-14) y `AgentCommunicationGateway` (CH-15).

### `IdempotencyRecordStatus` — dos valores, nunca un `Boolean`

```pseudocode
ENUM IdempotencyRecordStatus
    PENDING
    COMPLETED
END
```

**Por qué un `ENUM` de dos valores, y no un `Boolean alreadyExecuted`.** Se evaluó explícitamente un
campo `Boolean` — más simple de construir, y aparentemente suficiente: "¿ya se ejecutó esto o no?".
Se descartó porque un `Boolean` de dos estados solo puede distinguir "visto antes" de "no visto
antes" — y esa distinción no le dice a un llamador **qué hacer** con la repetición. Una ejecución
`COMPLETED` significa que el side effect ya terminó y que su `ToolResult` puede reusarse de inmediato,
sin volver a tocar el sistema externo. Una ejecución `PENDING` significa que el side effect todavía
está en curso — y ahí la respuesta correcta no es "reusar un resultado" (todavía no existe ninguno)
sino "esperar a que la primera ejecución termine, para no duplicar el side effect mientras sigue en
curso". Un `Boolean` colapsaría estas dos situaciones, con acciones correctas opuestas, en el mismo
valor `TRUE`.

**Por qué solo dos valores, y no un tercero para "nunca visto".** La ausencia total de un
`IdempotencyRecord` para una `idempotencyKey` dada —representada por `Optional<IdempotencyRecord> =
NULL` en `checkIdempotency` (seccion 11), nunca por un tercer valor de este `ENUM`— es lo que
significa "nunca visto antes". Agregar un valor `NOT_FOUND` habría duplicado, dentro del `ENUM`, una
distinción que la ausencia misma del contrato ya representa — el mismo argumento que ya evitó un
campo `expiresAt` obligatorio con un valor centinela en `CredentialReference` (CH-16 §6): la ausencia
de dato, cuando es información real, no necesita fabricarse un valor propio dentro de un `ENUM`.

### `IdempotencyRecord` — el registro persistido de una clave ya vista

```pseudocode
STRUCT IdempotencyRecord
    id: IdempotencyRecordId
    idempotencyKey: Text
    capability: CapabilityId
    originalToolCallId: ToolCallId
    status: IdempotencyRecordStatus
    result: Optional<ToolResult>
    createdAt: Timestamp
    completedAt: Optional<Timestamp>
END
```

Ocho campos, cada uno respondiendo a una parte exacta del alcance decidido para este capítulo: `id`
identifica este registro de forma estable; `idempotencyKey` es la clave misma que correlaciona todos
los intentos de esta intención lógica — asumida como dada (seccion 5), nunca generada por este
componente; `capability` es una referencia opaca — el mismo `CapabilityId` que ya vive dentro de
`ToolCall.capability` (C-008, CH-02) — a la capability que esta clave reclamó primero (nunca el
`ToolCall` completo embebido: una referencia por id evita que este registro cargue una copia que
podría quedar desactualizada, el mismo argumento que ya usó `CredentialReference.capability` en
CH-16 §6); `originalToolCallId` referencia el `ToolCallId` exacto del `ToolCall` que primero reclamó
esta clave — trazabilidad hacia atrás, sin duplicar sus `arguments`; `status` es
`IdempotencyRecordStatus` (sección anterior); `result` es `Optional<ToolResult>` — el `ToolResult`
(C-009) ya producido, poblado únicamente cuando `status = COMPLETED` (mientras `status = PENDING` no
existe todavía ningún resultado que ofrecer, y el campo permanece `NULL`); `createdAt` registra cuándo
se vio esta clave por primera vez; `completedAt` es `Optional<Timestamp>`, poblado únicamente cuando
`status = COMPLETED`.

**Por qué `capability`, y no embeber el `ToolCall` completo — el mismo argumento de CH-16, aplicado
aquí a un problema distinto.** Un `IdempotencyRecord` que embebiera el `ToolCall` completo tentaría a
compararlo campo por campo contra un intento nuevo para "confirmar" que es la misma intención — pero
eso es exactamente lo que la `idempotencyKey` ya existe para resolver sin ambigüedad. Guardar
`capability` (nunca el `ToolCall` entero) sirve, en cambio, para una verificación mucho más acotada y
mucho más barata: que la clave encontrada no se esté reutilizando, por error o por colisión, para una
capability completamente distinta de la que el intento actual solicita (`checkIdempotency`, seccion
11, rechaza ese caso explícitamente en vez de reusar un resultado ajeno).

**Por qué `result: Optional<ToolResult>`, y no un campo `output: Optional<Value>` propio.** Se evaluó
duplicar dentro de `IdempotencyRecord` los campos relevantes de un resultado (`output`/`error`). Se
descartó: `ToolResult` (C-009, CH-02) ya es, precisamente, el contrato que normaliza el resultado de
una `ToolCall` — reusarlo tal cual, sin reconstruirlo, es la misma decisión que ya tomó
`PolicyDecision.reason: Optional<HarnessError>` (CH-05) al reusar `HarnessError` en vez de inventar
una segunda representación de un fallo.

**Unchanged / Not yet introduced**: `ToolCall` (C-008) y `ToolResult` (C-009) no cambian de forma —
este capítulo los consume y los reusa, nunca los modifica. Ningún `STRUCT` para la `idempotencyKey`
misma más allá de `Text`, ni para el mecanismo real que genera esa clave: primitivas asumidas, fuera
de alcance (ver seccion 18).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce un contrato de
datos, registrado en `registry/contracts.yaml`:

```text
ID:                     C-027
Name:                   IdempotencyRecord
Version:                v1
Introduced In:          CH-17
Current Definition:     STRUCT IdempotencyRecord (ver §6)
Used By:                [CMP-015]
Modified By:            []
Constitutional Impact:  [INV-11, P-24, INV-E09]
```

`C-027` es el decimocuarto id que este libro asigna sin que estuviera reservado desde CH-01 §7 — el
correlativo simplemente continúa después de `C-026` (CH-16). No colisiona, por nombre, con ningún
contrato ya registrado — verificado con grep completo sobre `registry/contracts.yaml` antes de
escribir este capítulo.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el cuarto componente del registry que no corresponde a ninguno de los once
nombres del árbol de Article III ("Agent Runtime") — pertenece, en cambio, al "Reliability Plane" de
Amendment v1.1:

```pseudocode
COMPONENT IdempotencyGuard
    consumes: ExecutionContext, ToolCall, ToolResult
    produces: IdempotencyRecord, AgentEvent, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Article II (`INV-11`) y Amendment v1.1
(`P-24`/`INV-E09`) — Article III no tiene, todavía, una sección propia para este componente,
exactamente igual que `AdmissionController` (CH-14), `AgentCommunicationGateway` (CH-15) y
`CredentialBroker` (CH-16):

```text
COMPONENT: IdempotencyGuard

Responsibility:
    Rastrear, para un ToolCall con side effects (C-008, CH-02) identificado por una clave de
    idempotencia ya asumida como dada, si esa ejecución ya ocurrió antes bajo esa misma clave —
    permitiendo, cuando corresponda, reusar el ToolResult (C-009, CH-02) ya producido en vez de
    duplicar el side effect real — y registrar, una vez que una ejecución nueva concluye, el
    IdempotencyRecord terminal correspondiente, sin sobrescribir jamás uno ya producido.

Consumes:
    C-004 ExecutionContext, C-008 ToolCall, C-009 ToolResult

Depends on:
    (ninguno todavía — el cableado real hacia ToolRuntime, para que checkIdempotency se consulte
    antes de ejecutar y recordIdempotentExecution se invoque después, es Preview, no introducido
    en este capítulo; ver seccion 9)

Produces:
    C-027 IdempotencyRecord (el registro, PENDING o COMPLETED, listo para que un capítulo de
    integración futuro lo consulte antes de ejecutar y lo escriba después), C-010 AgentEvent
    (IDEMPOTENT_EXECUTION_DETECTED / IDEMPOTENCY_CHECK_FAILED / IDEMPOTENT_EXECUTION_RECORDED /
    IDEMPOTENCY_RECORD_CONFLICT), C-011 HarnessError

Owns (Article II `INV-11`, Amendment v1.1 `P-24`/`INV-E09`, cita y lectura literal):
    - "Side effects críticos deben soportar idempotencia, deduplicación o una protección
      equivalente" (cita literal, INV-11, Article II — Execution Invariants)
    - "Capabilities with externally visible side effects MUST declare idempotency, retry and
      duplicate-delivery behavior" (cita literal, P-24)
    - "Every side-effecting capability declares idempotency and retry semantics" (cita literal,
      INV-E09 — la mitad de "idempotency", ver Does NOT own para la mitad de "retry")
    - detectar cuándo un ToolCall (C-008) ya se ejecutó antes bajo la misma clave de idempotencia,
      produciendo el IdempotencyRecord ya asociado a esa clave (PENDING o COMPLETED), cuando existe
    - decidir si una ejecución repetida debe reusar el ToolResult (C-009) ya conocido, en vez de que
      el side effect real vuelva a ejecutarse
    - registrar, de forma terminal y write-once, el IdempotencyRecord COMPLETED que resulta de una
      ejecución nueva ya concluida
    - rechazar por defecto (fail-closed) cuando la clave de idempotencia encontrada corresponde a
      una capability distinta de la solicitada, o cuando se intenta re-registrar una ejecución ya
      COMPLETED

Does NOT own:
    - ejecutar el side effect en sí (ToolRuntime, CMP-002, ya introducido en CH-02 — IdempotencyGuard
      decide SI el side effect debe volver a ejecutarse, nunca CÓMO se ejecuta)
    - decidir si la acción/ToolCall ya resuelta está autorizada (PolicyEngine, CMP-005, ya
      introducido en CH-05 — distinta pregunta, distinto momento: "¿ya se hizo esto?" nunca es "¿está
      permitido hacerlo?")
    - resolver qué implementación satisface una capability solicitada (CapabilityRegistry, CMP-008,
      ya introducido en CH-08 — este componente no vuelve a decidir cuál es la implementación
      correcta, solo si la invocación ya identificada ya ocurrió)
    - decidir si un AgentRun puede seguir operacionalmente contra su ExecutionBudget, incluyendo si
      reintentar tras un fallo transitorio (ExecutionController, CMP-007, ya introducido en CH-07 —
      distinción central de este capítulo, ver seccion 15: "puedo seguir intentando" y "ya se hizo
      con éxito" son preguntas ortogonales sobre materiales distintos; la mitad de "retry semantics"
      de INV-E09 pertenece a ExecutionController, no a este componente)
    - generar la clave de idempotencia misma, ni decidir con qué algoritmo se deriva (asumida como
      una señal de entrada dada, igual que otros capítulos asumen señales — ver seccion 6)
    - el mecanismo real de persistencia atómica que evita una condición de carrera entre dos
      ejecuciones concurrentes que reclaman la misma clave al mismo tiempo (Preview, ver seccion 18)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con la misma
particularidad que `AdmissionController`/`AgentCommunicationGateway`/`CredentialBroker`: ninguna de
las seis exclusiones proviene de una ficha propia de Article III (que no existe para este
componente); provienen de fronteras ya establecidas por componentes ya registrados (`ToolRuntime`,
`PolicyEngine`, `CapabilityRegistry`, `ExecutionController`).

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
IdempotencyGuard
    consumes → ExecutionContext, ToolCall, ToolResult
    produces → IdempotencyRecord, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`IdempotencyGuard` no depende hoy de ningún otro componente registrado — mismo patrón que CH-01..
CH-16 ya establecieron para sus propios componentes. En prosa (nunca dentro de un bloque
`pseudocode`, per `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las relaciones
futuras que un capítulo de integración agregaría son:

| Componente futuro (relación inversa — no cableada en este capítulo) | Qué relación tendría con `IdempotencyGuard` |
|---|---|
| `ToolRuntime` (ya existente, CMP-002) | **`ToolRuntime.executeToolCall` consultaría `checkIdempotency` ANTES de ejecutar el side effect, y llamaría a `recordIdempotentExecution` DESPUÉS de que termine** — el cableado exacto que este capítulo deja explícitamente para un capítulo de integración futuro, sin tocar una sola línea del `executeToolCall` ya publicado en CH-02 |
| `ExecutionController` (ya existente, CMP-007) | seguiría decidiendo, sin cambios, si el `AgentRun` puede continuar operacionalmente contra su `ExecutionBudget` — una pregunta completamente anterior e independiente de si un side effect específico ya se ejecutó (ver seccion 15) |
| `PolicyEngine` (ya existente, CMP-005) | seguiría decidiendo, sin cambios, si el `ToolCall` que produciría el side effect está autorizado — una pregunta completamente anterior e independiente de la deduplicación |
| Un mecanismo real de persistencia atómica (todavía sin componente propio en este registry) | garantizaría que dos ejecuciones concurrentes que reclaman la misma `idempotencyKey` no puedan, ambas, crear un `IdempotencyRecord` `PENDING` al mismo tiempo — infraestructura de borde, fuera de este registry (ver seccion 18) |

`registry/components.yaml` de `CMP-002` (`ToolRuntime`) y `CMP-007` (`ExecutionController`) **no se
modifica** en este capítulo: ninguno agrega `CMP-015` a sus `dependencies`, y ninguno cambia su
pseudocódigo. El pseudocódigo de la seccion 11 evalúa un `ToolCall`/`ToolResult` de ejemplo de forma
completamente autónoma — sin que ninguno de los dos componentes ya existentes cambie una sola línea
para que este capítulo sea correcto. Ese cableado real es, explícitamente, trabajo de un capítulo de
integración futuro (ver seccion 18/19).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[ToolRuntime — consultaría antes de ejecutar el side effect, CH-02, conceptual] → IdempotencyGuard →
[ToolRuntime — reusaría el ToolResult ya conocido, o ejecutaría el side effect real y registraría el
 resultado después, CH-02, conceptual]
```

**Vista 2 — Sequence**

```text
ToolCall (con side effect, ya resuelto y ya autorizado)
   │
   ▼
IdempotencyGuard
   │ checkIdempotency(toolCall, idempotencyKey, existingRecordForKey, execution, agentId)
   │ ¿existingRecordForKey == NULL? sí → RETURN NULL (nada visto antes, puede proceder a ejecutar)
   │ ¿capability de existingRecordForKey != toolCall.capability? sí → HarnessError
   │   (IDEMPOTENCY_KEY_CAPABILITY_MISMATCH)
   │ si no → RETURN existingRecordForKey (PENDING: esperar, no ejecutar; COMPLETED: reusar
   │   existingRecordForKey.result en vez de ejecutar)
   │ emite: AgentEvent (IDEMPOTENT_EXECUTION_DETECTED | IDEMPOTENCY_CHECK_FAILED)
   ▼
[si NULL: ToolRuntime ejecuta el side effect real, CH-02, conceptual] → ToolResult
   │
   ▼
IdempotencyGuard
   │ recordIdempotentExecution(toolCall, toolResult, idempotencyKey, existingRecordForKey,
   │                            execution, agentId)
   │ ¿existingRecordForKey ya COMPLETED? sí → HarnessError (IDEMPOTENCY_RECORD_ALREADY_COMPLETED,
   │   nunca sobrescribe un registro terminal)
   │ construye/completa IdempotencyRecord (status = COMPLETED, result = toolResult)
   │ emite: AgentEvent (IDEMPOTENT_EXECUTION_RECORDED | IDEMPOTENCY_RECORD_CONFLICT)
   ▼
IdempotencyRecord (COMPLETED, listo para que la próxima entrega duplicada lo reuse)
   │
   │ ... integración futura: ToolRuntime.executeToolCall (CH-02) llamaría a checkIdempotency antes
   │     de ejecutar y a recordIdempotentExecution después — incluyendo la persistencia real de un
   │     registro PENDING en el instante en que la ejecución arranca, para que una segunda ejecución
   │     concurrente lo vea en vez de a NULL ...
```

**Vista 3 — Pseudocódigo**

Ver §11: `checkIdempotency`/`recordIdempotentExecution` son la primera formalización ejecutable de
"ningún side effect crítico se repite sin que el harness lo sepa" (`INV-11`/`P-24`/`INV-E09`) —
construidas exclusivamente a partir de material que ya existe (`ToolCall`/`ToolResult` desde CH-02,
`HarnessError`/`ExecutionContext`/`AgentEvent` desde CH-00) más el contrato y los `ENUM` nuevos de
este capítulo.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde CH-00/CH-02.

```pseudocode
FUNCTION checkIdempotency(
    toolCall: ToolCall,
    idempotencyKey: Text,
    existingRecordForKey: Optional<IdempotencyRecord>,
    execution: ExecutionContext,
    agentId: AgentId
) -> Optional<IdempotencyRecord>

    IF existingRecordForKey == NULL
        RETURN NULL
    END

    IF existingRecordForKey.capability != toolCall.capability
        mismatched: HarnessError = HarnessError(
            category = IDEMPOTENCY,
            code = "IDEMPOTENCY_KEY_CAPABILITY_MISMATCH",
            message = "La idempotencyKey ya tiene un IdempotencyRecord asociado a una capability distinta de la que este ToolCall solicita",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )

        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = IDEMPOTENCY_CHECK_FAILED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = mismatched
        )

        THROW mismatched
    END

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = IDEMPOTENT_EXECUTION_DETECTED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = existingRecordForKey
    )

    RETURN existingRecordForKey
END

FUNCTION recordIdempotentExecution(
    toolCall: ToolCall,
    toolResult: ToolResult,
    idempotencyKey: Text,
    existingRecordForKey: Optional<IdempotencyRecord>,
    execution: ExecutionContext,
    agentId: AgentId
) -> IdempotencyRecord

    IF existingRecordForKey != NULL AND existingRecordForKey.status == COMPLETED
        conflict: HarnessError = HarnessError(
            category = IDEMPOTENCY,
            code = "IDEMPOTENCY_RECORD_ALREADY_COMPLETED",
            message = "Ya existe un IdempotencyRecord COMPLETED para esta idempotencyKey; recordIdempotentExecution nunca sobrescribe un registro terminal ya producido",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )

        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = IDEMPOTENCY_RECORD_CONFLICT,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = conflict
        )

        THROW conflict
    END

    recordId: IdempotencyRecordId = newIdempotencyRecordId()
    createdAt: Timestamp = now()

    IF existingRecordForKey != NULL
        recordId = existingRecordForKey.id
        createdAt = existingRecordForKey.createdAt
    END

    record: IdempotencyRecord = IdempotencyRecord(
        id = recordId,
        idempotencyKey = idempotencyKey,
        capability = toolCall.capability,
        originalToolCallId = toolCall.id,
        status = COMPLETED,
        result = toolResult,
        createdAt = createdAt,
        completedAt = now()
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = IDEMPOTENT_EXECUTION_RECORDED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = record
    )

    RETURN record
END
```

`now()`, `newEventId()` y `newIdempotencyRecordId()` son las mismas primitivas de CH-00/CH-14/CH-15/
CH-16. `idempotencyKey` y `existingRecordForKey` son señales de entrada — igual que
`capabilityResolved`/`inputValid` en CH-02 §11 o `credentialBelongsToCapability`/`secretExists` en
CH-16 §11 — que un mecanismo real de persistencia (Preview, fuera de este registry) produciría en la
práctica: ninguna de las dos funciones de este capítulo calcula la clave ni realiza la búsqueda, las
reciben y deciden, determinísticamente, qué `IdempotencyRecord` o qué `HarnessError` construir a
partir de ellas.

**Por qué `recordIdempotentExecution` preserva `id`/`createdAt` de un `existingRecordForKey` previo,
en vez de generar siempre un registro nuevo.** Si `existingRecordForKey` ya existía en estado
`PENDING` (una ejecución que había arrancado, todavía sin terminar), completar esa misma ejecución
debe producir el mismo `IdempotencyRecord` lógico —con su identidad preservada—, nunca un segundo
registro independiente para la misma clave. Generar siempre un `id` nuevo habría hecho posible que
dos registros coexistieran para la misma `idempotencyKey`, exactamente la ambigüedad que este
capítulo existe para prevenir.

**Por qué `recordIdempotentExecution` rechaza sobrescribir un registro ya `COMPLETED`.** Un
`IdempotencyRecord` en estado `COMPLETED` es, por diseño, terminal y write-once: una vez que un side
effect terminó y su `ToolResult` quedó registrado, ninguna llamada posterior a
`recordIdempotentExecution` para la misma clave debería reemplazarlo — si eso ocurriera sin control,
un segundo intento tardío (por ejemplo, una entrega duplicada que llega después de que la primera ya
completó) podría sobrescribir un resultado correcto con uno potencialmente distinto, exactamente lo
que `INV-11` exige impedir. `IDEMPOTENCY_RECORD_ALREADY_COMPLETED` fuerza a que un llamador que
encuentra un registro ya `COMPLETED` use `checkIdempotency` para reusarlo, nunca
`recordIdempotentExecution` para reemplazarlo.

Nótese también lo que ninguna de las dos funciones **hace**: no invocan `ToolRuntime.executeToolCall`
(CH-02) ni ejecutan ningún side effect; no invocan `PolicyEngine.evaluatePolicyForToolCall` (CH-05) ni
`CapabilityRegistry.resolveToolCall` (CH-08); y no invocan `ExecutionController.
evaluateExecutionContinuation` (CH-07) — decidir si el run puede seguir contra su presupuesto sigue
siendo, sin excepción, una pregunta completamente distinta (ver seccion 15).

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013): sigue siendo, sin cambios, el mismo
`ENUM` de once estados que `AgentLoop` (CH-01) formalizó. `IdempotencyRecord`, a diferencia de
`CredentialReference` (CH-16 §12) o `DelegationGrant` (CH-15 §12) —cuya vigencia se deriva, en cada
evaluación, de comparar `now()` contra una fecha—, sí introduce un `ENUM` de estado propio
(`IdempotencyRecordStatus`), porque "en curso" no es una fecha que pueda vencer: es una condición
binaria real que solo una escritura explícita (`recordIdempotentExecution`) puede resolver.

```text
(ninguna idempotencyKey vista todavía)
   → checkIdempotency(existingRecordForKey = NULL)
     RETURN NULL — el llamador puede proceder a ejecutar el side effect real

(una ejecución arranca bajo una idempotencyKey — creación de un registro PENDING)
   → Preview, no modelado por el pseudocódigo de este capítulo (seccion 18): la persistencia real
     de un IdempotencyRecord en estado PENDING, en el instante exacto en que una ejecución arranca
     y ANTES de que el side effect real se dispare, es exactamente el mecanismo de control de
     concurrencia que un capítulo de integración futuro tendría que cablear de forma atómica

(existingRecordForKey.status == PENDING — otra ejecución ya está en curso bajo esta clave)
   → checkIdempotency lo devuelve tal cual (nunca lo completa, nunca lo descarta)
     el llamador debería esperar, no ejecutar de nuevo — el mecanismo real de espera es Preview

(existingRecordForKey.status == COMPLETED, capability coincide)
   → checkIdempotency lo devuelve tal cual — el llamador reusa existingRecordForKey.result
     (un ToolResult ya producido) en vez de ejecutar el side effect de nuevo

(existingRecordForKey.status == COMPLETED, capability NO coincide)
   → checkIdempotency lanza HarnessError (IDEMPOTENCY_KEY_CAPABILITY_MISMATCH) — fail-closed,
     nunca reusa un resultado que pertenece a una capability distinta

(recordIdempotentExecution, con existingRecordForKey == NULL o PENDING)
   → produce/completa un IdempotencyRecord con status = COMPLETED — transición terminal, el único
     destino real que este capítulo formaliza con pseudocódigo

(recordIdempotentExecution, con existingRecordForKey ya COMPLETED)
   → lanza HarnessError (IDEMPOTENCY_RECORD_ALREADY_COMPLETED) — write-once, nunca sobrescribe
```

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6, extendido en la seccion 6 de este capítulo) clasifica también
los dos fallos reales que introduce este capítulo:

```text
IDEMPOTENCY
    IDEMPOTENCY_KEY_CAPABILITY_MISMATCH   — la idempotencyKey ya tiene un IdempotencyRecord
                                            asociado a una capability distinta de la que este
                                            ToolCall solicita
        → recoverable: FALSE, retryable: FALSE
    IDEMPOTENCY_RECORD_ALREADY_COMPLETED  — ya existe un IdempotencyRecord COMPLETED para esta
                                            idempotencyKey; recordIdempotentExecution nunca
                                            sobrescribe un registro terminal ya producido
        → recoverable: FALSE, retryable: FALSE
```

Ambos fallos son `recoverable = FALSE` y `retryable = FALSE`: los dos representan un uso incorrecto
de la `idempotencyKey` por parte del llamador (una colisión de clave entre dos capabilities distintas,
o un intento de re-registrar una ejecución que ya se registró como terminada) — ninguno de los dos se
corrige reintentando la misma operación, y ninguno es, en sí mismo, el tipo de fallo transitorio que
`P-24`/`INV-E09` piden declarar bajo "retry semantics" (esa mitad del problema —cuándo tiene sentido
reintentar un `ToolCall` que falló— sigue siendo, sin excepción, responsabilidad de
`ExecutionController`, CH-07, no de este componente).

**La distinción más importante de esta sección**: ninguno de los dos fallos se clasifica como
`category = VALIDATION` ni como `category = BUDGET` — aunque `IDEMPOTENCY_KEY_CAPABILITY_MISMATCH`
podría, a primera vista, parecer un problema de forma/esquema, y ambos podrían confundirse con un
límite operacional agotado. `VALIDATION` (CH-02/CH-08) pertenece, en exclusiva, a fallos sobre la
forma de una intención de acción ya resuelta — nunca sobre si esa acción ya se ejecutó antes.
`BUDGET` (CH-07) pertenece, en exclusiva, a límites operacionales agregados de un run completo —
nunca sobre la deduplicación de un side effect individual. Reutilizar cualquiera de las dos aquí
habría conflacionado dos decisiones de dos componentes distintos, exactamente el error que Article IV
(Ownership Rule) prohíbe — el mismo argumento que ya usaron CH-15 §13 (para no reutilizar `BUDGET`) y
CH-16 §13 (para no reutilizar `VALIDATION`).

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo de `category = INFRASTRUCTURE`
que pudiera ocurrir en el mecanismo real de persistencia detrás de `existingRecordForKey` (por
ejemplo, un almacén de registros completamente inalcanzable, o una condición de carrera real entre dos
escrituras concurrentes) — ese valor de `ErrorCategory` sigue, después de este capítulo, sin que
ningún componente real lo haya ejercitado nunca (mismo límite que CH-11 §13/CH-14 §13/CH-15 §13/
CH-16 §13 ya documentaron para sus propias primitivas asumidas).

## 14. Eventos Producidos (Events Produced)

**A diferencia de los dos componentes de Amendment v1.1 que nunca emiten eventos reales**
(`AdmissionController`, CH-14; `AgentCommunicationGateway`, CH-15), `IdempotencyGuard` **sí** produce
eventos reales, la misma situación que `CapabilityRegistry` (CH-08) y `CredentialBroker` (CH-16):
agrega `IDEMPOTENT_EXECUTION_DETECTED`, `IDEMPOTENCY_CHECK_FAILED`, `IDEMPOTENT_EXECUTION_RECORDED` y
`IDEMPOTENCY_RECORD_CONFLICT` a `AgentEventType` (seccion 6), y ambas funciones de la seccion 11 los
emiten en cada rama relevante.

**Por qué este componente sí puede emitir, cuando `AdmissionController`/`AgentCommunicationGateway`
no podían.** Cuando un `ToolCall` con side effects necesita verificarse contra `IdempotencyGuard`, el
`AgentRun` que lo origina ya existe, con `ExecutionContext` completo (`runId`/`sessionId`/`traceId`)
— no hay ningún campo faltante que fabricar ni que silenciar, la misma situación exacta que
`CapabilityRegistry` (CH-08) y `CredentialBroker` (CH-16) ya establecieron para sus propios
capítulos.

**Por qué no se emite ningún evento cuando `checkIdempotency` devuelve `NULL`.** El caso "nunca visto
antes" es, deliberadamente, el camino silencioso — es el comportamiento por defecto y esperado de la
inmensa mayoría de las `ToolCall` de este libro (una intención nueva, sin ningún intento previo bajo
la misma clave). Emitir un evento en ese camino habría producido ruido operacional sin ninguna señal
nueva que comunicar; el mismo criterio editorial que ya aplicó `ToolRuntime.executeToolCall` (CH-02)
al no emitir nada antes de que el side effect ocurra.

**Lo que este capítulo no resuelve (relación con `P-25`).** Una auditoría completa de "cuántas veces
se intentó ejecutar este side effect, y cuándo" necesitaría, per `P-25` ("Audit evidence is distinct
from operational telemetry"), algo más que `AgentEvent`/`EventBus` (Article X) — un mecanismo de
evidencia inmutable, distinto de la telemetría operacional que este capítulo sí produce. Ese
mecanismo no se construye aquí (mismo límite, honestamente señalado, que CH-14 §14/CH-15 §14/CH-16
§14 ya documentaron cada uno para su propio contrato).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

`IdempotencyGuard` es el primer componente de este libro cuya responsabilidad completa es prevenir
que un side effect crítico, ya ejecutado con éxito, vuelva a ejecutarse por accidente.

**La distinción con `ExecutionController` (CH-07), explícita, completa y la más importante de este
capítulo.** `ExecutionController.evaluateExecutionContinuation` (CH-07) decide si un `AgentRun` puede
seguir *operacionalmente* contra su `ExecutionBudget` — turnos, tool calls, tokens, costo, tiempo,
concurrencia — produciendo `CONTINUE`, `STOP` o `CANCELLED`. Esa pregunta se responde por completo sin
necesitar saber jamás si un side effect *específico*, identificado por una clave de idempotencia, ya
produjo su resultado. `IdempotencyGuard.checkIdempotency`/`recordIdempotentExecution` (este capítulo)
deciden si esa ejecución específica ya ocurrió, asumiendo que la pregunta de continuación operacional
ya se resolvió (o está a punto de resolverse) por otro camino — nunca vuelven a evaluar presupuesto.
Las dos preguntas son, literalmente, ortogonales: un run puede tener presupuesto de sobra
(`ExecutionDecision.outcome = CONTINUE`) y, aun así, estar a punto de duplicar un side effect ya
ejecutado si `IdempotencyGuard` no interviene; y, a la inversa, un run puede haber agotado su
presupuesto (`outcome = STOP`) sin que eso tenga ninguna relación con si algún `ToolCall` particular
ya se había ejecutado antes. `P-24`/`INV-E09` piden declarar tanto "idempotency" como "retry
semantics": este capítulo resuelve la primera mitad; la segunda —cuándo, y cuántas veces, tiene
sentido reintentar un `ToolCall` que falló de forma transitoria— sigue perteneciendo, sin excepción, a
`ExecutionController` (Preview, ver seccion 18).

**La distinción con `PolicyEngine` (CH-05) y `CapabilityRegistry` (CH-08), heredada de capítulos
anteriores.** `PolicyEngine.evaluatePolicyForToolCall` (CH-05) decide si una acción ya resuelta puede
ejecutarse — una pregunta que se responde por completo sin necesitar saber jamás si esa acción ya se
ejecutó antes. `CapabilityRegistry.resolveToolCall` (CH-08) decide qué implementación satisface una
capability solicitada — tampoco necesita saber si esta invocación concreta de esa implementación ya
ocurrió. `IdempotencyGuard` asume ambas resoluciones como hechos ya cerrados (recibe un `ToolCall` ya
resuelto y, se asume, ya autorizado) y se ocupa exclusivamente de lo que todavía falta: si esa
ejecución específica ya sucedió. La misma disciplina de límites que CH-14 §15/CH-15 §15/CH-16 §15 ya
aplicaron frente a sus propios vecinos.

**`INV-11`/`INV-E09`, aplicados con cuidado.** Este capítulo modela la detección de una repetición y
el registro write-once de una ejecución terminada — pero no modela, todavía, la "protección
equivalente" completa que `INV-11` deja abierta como alternativa a la idempotencia estricta (por
ejemplo, un mecanismo de compensación que revierta un side effect duplicado después del hecho, en vez
de prevenirlo antes). Este capítulo eligió deliberadamente la ruta de prevención (detectar antes de
ejecutar), no la de compensación (revertir después de ejecutar dos veces) — señalado explícitamente
como una decisión de alcance, no como una omisión silenciosa (ver seccion 18).

**Lo que este capítulo NO implementa todavía.** Ningún mecanismo real de persistencia atómica que
evite que dos ejecuciones concurrentes creen, ambas, un `IdempotencyRecord` `PENDING` para la misma
clave al mismo tiempo (la condición de carrera clásica "check-then-act"); ningún mecanismo real que
haga esperar a una segunda ejecución mientras la primera sigue `PENDING` (colas, locks, polling);
ningún cableado real entre `IdempotencyGuard` y `ToolRuntime.executeToolCall`; ninguna política real
de expiración/garbage collection para `IdempotencyRecord` antiguos (¿cuánto tiempo debe reusarse un
resultado ya `COMPLETED` antes de que la clave pueda reutilizarse?); ninguna semántica real de
"retry" (la segunda mitad de `INV-E09`, propiedad de `ExecutionController`, no de este componente).

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST IdempotencyGuardReturnsNullWhenNoRecordExistsForAKey
TEST IdempotencyGuardRejectsARecordThatBelongsToADifferentCapability
TEST IdempotencyGuardReturnsAPendingRecordWithoutCompletingOrDiscardingIt
TEST IdempotencyGuardReturnsACompletedRecordSoTheCallerCanReuseItsResult
TEST IdempotencyGuardNeverOverwritesAnAlreadyCompletedRecord
TEST IdempotencyGuardPreservesRecordIdentityWhenCompletingAPendingRecord
TEST IdempotencyGuardNeverExecutesTheSideEffectItself
TEST IdempotencyGuardNeverEvaluatesExecutionBudgetOrToolCallAuthorization
TEST IdempotencyGuardEmitsAnAgentEventOnEveryRelevantBranch
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (después de CH-17 — cuarto plano de Amendment v1.1 cubierto por este libro, y primer
componente que cierra un invariante del Article II original)

Constitution
 ├── Article II    — Invariants (INV-11, "Execution Invariants", declarado desde CH-00, cerrado por
 │                    primera vez con un componente real en este capítulo)
 ├── Article III   — Component Sovereignty (once componentes de "Agent Runtime", sin cambios desde
 │                    CH-11)
 ├── Article IV    — Decision Ownership (tabla original sin cambios; IdempotencyGuard documentado en
 │                    prosa, igual que AdmissionController/AgentCommunicationGateway/CredentialBroker)
 └── Amendment v1.1 — Enterprise Activation, Interoperability and Operations
                       (P-24/INV-E09 citados por primera vez con código real; Ingress & Activation
                       Plane, CH-14, Agent Interoperability Plane, CH-15, Capability & Integration
                       Plane, CH-16, y Reliability Plane, este capítulo, los cuatro primeros de nueve
                       planos canónicos instalados)

Contracts (registry/contracts.yaml)
 ├── C-001..C-026  (sin cambios — CH-00..CH-16)
 └── C-027 IdempotencyRecord  (CH-17, nuevo — el registro de que un ToolCall con side effects ya se
                               vio antes bajo una idempotencyKey dada, INV-11/P-24/INV-E09)

Components (registry/components.yaml)
 ├── CMP-001..CMP-014  (sin cambios — CH-01..CH-16)
 └── CMP-015 IdempotencyGuard  (CH-17, nuevo — cuarto componente de este registry que no
                                 corresponde a ninguno de los once nombres de Article III; pertenece
                                 al Reliability Plane de Amendment v1.1, y es el primero cuyo owns se
                                 ancla, ante todo, en un invariante del Article II original)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado real `ToolRuntime ↔ IdempotencyGuard`**: ningún componente invoca todavía
  `checkIdempotency` antes de ejecutar un side effect, ni `recordIdempotentExecution` después — el
  propio encargo de este capítulo señala, explícitamente, que ese cableado es trabajo de un capítulo
  de integración futuro; sigue sin construirse.
- **La persistencia real de un `IdempotencyRecord` `PENDING` en el instante exacto en que una
  ejecución arranca**: este capítulo demuestra la transición terminal (`recordIdempotentExecution`
  produciendo `COMPLETED`), pero nunca la creación del estado intermedio real — sin esa escritura
  atómica y anterior a la ejecución, una segunda ejecución concurrente seguiría viendo `NULL` en vez
  de `PENDING`, y el problema de la seccion 2 (tercera dimensión) seguiría sin resolverse en la
  práctica.
- **El mecanismo real que hace esperar a una ejecución concurrente bajo `PENDING`**: colas, locks
  distribuidos, polling con backoff — ninguno modelado; este capítulo solo formaliza que `PENDING`
  significa "espera", no cómo se implementa esa espera.
- **La generación real de una `idempotencyKey`**: quién la deriva, con qué algoritmo (un hash de los
  argumentos, un id provisto por el llamador externo, algo más) — asumida, no modelada (mismo límite
  que CH-16 §18 documentó para la emisión de un secreto hacia un Secret Store).
- **La semántica real de "retry"** (la segunda mitad de `P-24`/`INV-E09`): cuándo, y cuántas veces,
  tiene sentido reintentar un `ToolCall` que falló de forma transitoria — pertenece a
  `ExecutionController` (CH-07), no se profundiza aquí.
- **Una política real de expiración/garbage collection** para `IdempotencyRecord` ya `COMPLETED`:
  este capítulo no modela cuánto tiempo debe conservarse un registro antes de que su clave pueda
  reutilizarse con seguridad para una intención lógica distinta.
- **La ruta de "protección equivalente" que `INV-11` deja abierta como alternativa** (compensación
  después del hecho, en vez de prevención antes): este capítulo eligió, deliberadamente, solo la
  ruta de prevención (ver seccion 15).
- **Ausencia de evidencia de auditoría real** (`P-25`) para un `IdempotencyRecord` producido:
  señalado explícitamente (seccion 14), no silenciado.
- **Los cinco planos restantes de Amendment v1.1** (Execution Plane, Data & Context Plane, Control
  Plane, Observability & Governance Plane, Execution Fabric) y **la profundización del Reliability
  Plane más allá de este primer componente**: explícitamente fuera de alcance.
- Reviewers plurales, evals y orquestación multi-agente propiamente dicha: explícitamente fuera de
  alcance de BH-v0.1.

## 19. Siguiente Incremento (Next Increment)

Con este capítulo, el "Reliability Plane" de Amendment v1.1 tiene su primer componente real — pero el
plano completo (la persistencia atómica real, el mecanismo real de espera concurrente, el cableado
real hacia `ToolRuntime`, la semántica de "retry" que sigue perteneciendo a `ExecutionController`)
sigue sin construirse de punta a punta. El problema natural del próximo incremento es, o bien
profundizar este mismo plano (cableando por fin `IdempotencyGuard` dentro de
`ToolRuntime.executeToolCall`, el mismo patrón de integración que CH-12/CH-13 ya establecieron para
el camino feliz y los caminos de gobierno de un `AgentRun`), o bien avanzar hacia cualquiera de los
cinco planos restantes que Amendment v1.1 enumera junto a este — el Execution Plane (segundo plano
canónico, todavía sin cubrir por ningún capítulo de este libro) o el Observability & Governance Plane
(que por fin resolvería la deuda de `P-25`, señalada sin resolver desde CH-09 y repetida en cada
capítulo de Amendment v1.1 desde entonces) son, ambos, candidatos particularmente naturales.

`next_chapter` queda en `null` en el frontmatter de este capítulo porque, en este momento del libro,
ese próximo capítulo todavía no existe como archivo — solo como el problema que motivaría su
escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg / Bucles
> de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows),
> secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): diecisiete capítulos reales construyeron un runtime
   completo más tres componentes de Enterprise, pero ningún componente rastreó jamás si un side
   effect con consecuencias reales ya se había ejecutado antes bajo la misma intención lógica.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): `INV-11` fue
   declarado desde CH-00 dentro de la tabla original de invariantes, nunca citado en prosa ni
   resuelto; `P-24`/`INV-E09` retoman la misma exigencia dieciséis capítulos después, y CH-08 §18 ya
   la había señalado explícitamente como "fuera de alcance" antes de que existiera ningún componente
   de Amendment v1.1 en este libro.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `IdempotencyGuard` con una ficha que declara tanto lo que posee (`owns`: detectar una repetición,
   decidir si reusar un resultado, registrar de forma terminal y write-once) como lo que
   explícitamente NO posee (ejecución del side effect, autorización, resolución de implementación,
   continuación operacional por presupuesto).
4. **Modelos mentales** (= §4, Constitutional Impact): "¿ya se hizo esto antes?" es una pregunta
   completamente distinta de "¿puedo seguir intentando?", de "¿está permitido hacerlo?", de "¿qué
   implementación lo hace?" y de "¿cómo se hace?" — cinco preguntas con dueños distintos que, sin
   este componente, corrían el riesgo de resolverse todas en el mismo lugar.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un sistema deja sin modelar esta protección, un
  reintento razonable se convierte en un side effect duplicado real — el mismo bucle de "ausencia de
  dueño se vuelve dependencia implícita" ya combatido por `P-02`/`P-19`/`INV-E08`, ahora aplicado a la
  repetición de un side effect.
- **Bucle de equilibrio (estabiliza):** `checkIdempotency`/`recordIdempotentExecution` (§11) permiten
  reusar un resultado ya conocido en vez de repetir un side effect, y rechazan, con un `HarnessError`
  categorizado, tanto una clave que no corresponde a la capability solicitada como un intento de
  sobrescribir un registro ya terminado.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `IdempotencyRecordStatus` tenga exactamente dos
valores explícitos (`PENDING`/`COMPLETED`) — nunca un `Boolean`, y nunca un tercer valor para "nunca
visto" (esa ausencia la representa la ausencia misma del contrato). Si `status` fuera un `Boolean`, no
habría forma de decirle a un llamador si debe reusar un resultado ya producido o esperar a que uno
exista — exactamente la ambigüedad que `INV-11`/`P-24`/`INV-E09` exigen resolver.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo de
> esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set` (frontmatter) y
> es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa, para lectura directa
> del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Cuando un `ToolCall` con side effects reales se entrega más de una vez bajo la misma intención
   lógica, ¿qué necesitaría existir para reconocer que ya se ejecutó antes, y decidir si el side
   effect debe volver a ocurrir? *(cierra la pregunta guía 1)*
2. La decisión de si un run puede seguir reintentando contra su presupuesto ya tiene un dueño. ¿Esa
   misma pregunta sirve para decidir si una ejecución concreta, ya exitosa, debe repetirse?
   *(cierra la pregunta guía 2)*
3. Si dos peticiones concurrentes representan la misma intención lógica, ¿qué debería pasarle a la
   segunda mientras la primera todavía no termina? *(cierra la pregunta guía 3)*
4. ¿Qué invariante original de la Constitution, declarado desde CH-00 y nunca antes resuelto, cierra
   por fin este capítulo? *(cierra la pregunta guía 4)*

### Explicar

1. `IdempotencyGuard` posee detectar cuándo una ejecución con side effects ya ocurrió antes. Explica,
   como si hablaras con alguien sin contexto técnico, por qué NO posee ejecutar el side effect en sí.
2. `IdempotencyRecord` nunca modela con un `Boolean` si una ejecución "ya se hizo". Explica qué
   perderíamos, y qué riesgo de duplicar un side effect introduciríamos, si `status` colapsara a dos
   valores booleanos simples.

### Conectar

1. `ToolRuntime.executeToolCall` (CH-02) nunca modeló si un side effect ya se ejecutó antes. Si este
   capítulo produjera un `IdempotencyRecord` ya `COMPLETED` con un `ToolResult` reusable, ¿le
   correspondería a `executeToolCall` ejecutar de todos modos, o la pregunta pertenece a otro dueño?
2. `ExecutionController` (CH-07) ya decide si un run puede seguir contra su presupuesto. ¿Alcanza con
   que conceda continuar, o hace falta una pregunta distinta sobre si un side effect específico ya
   ocurrió?

### Espaciar

Las cinco tarjetas de repaso de este capítulo (dos sobre `IdempotencyGuard` — su `owns` y su
`does_not_own` —, dos sobre `IdempotencyRecord` — sus campos y por qué `status` nunca es un
`Boolean` —, y una sobre el invariante original que este capítulo cierra) entran hoy en
`reviewStage = DAY_1`. Repásalas de nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) — ver
el apéndice de tarjetas al final del libro (edición PDF) o `retrieval_set.flashcards` en
`dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te equivocaste,
ese es precisamente el punto ciego que este método existe para revelar.
