---
id: CH-21
title: "ExecutionFabricAdapter y la Topología de Despliegue que el Comportamiento del Agente Nunca Debe Conocer"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-019]
introduces_contracts: [C-031]
modifies_contracts: []
constitutional_articles: [P-13, P-27, INV-18, INV-19, INV-20]
previous_chapter: CH-20
next_chapter: CH-22
retrieval_set:
  expected_outcome:
    id: EO-CH21
    text: |
      Al terminar este capítulo podrás distinguir, para un run que ya existe, tres preguntas que
      se confunden con facilidad porque las tres suenan a "recursos": cuánto puede consumir ese run
      antes de detenerse, sobre qué tipo de infraestructura de cómputo se materializa su ejecución,
      y quién lo creó en primer lugar. Podrás diseñar una descripción opaca y portátil de esa
      infraestructura — su topología de despliegue, una referencia al recurso de cómputo concreto,
      y una restricción de residencia geográfica si aplica — que viaje junto con el run sin que
      ningún componente del núcleo del harness necesite ramificar su lógica según dónde corre. Y
      podrás argumentar, con precisión, por qué esa misma independencia es la única forma de que un
      harness se despliegue hoy en un proceso único y mañana en un clúster distribuido sin reescribir
      una sola línea de su razonamiento.
  skeleton:
    id: SK-CH21
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
    components_to_be_introduced: [CMP-019]
    contracts_to_be_introduced: [C-031]
  guiding_questions:
    - id: GQ-CH21-01
      text: |
        Ya existe un componente que decide, dentro de un presupuesto explícito, cuánto tiempo,
        cuántas tool calls concurrentes y cuánto costo puede consumir un run ya en marcha. ¿Esa
        misma decisión determina también en qué tipo de infraestructura de cómputo corre ese run —
        dentro de un único proceso, en un worker, en un clúster, en una función serverless — o son
        preguntas de un dominio completamente distinto?
      answered_by: RQ-CH21-01
    - id: GQ-CH21-02
      text: |
        Ya existe un componente que adapta la comunicación de un agente hacia un proveedor de
        modelo concreto, y otro que la adapta hacia protocolos de interoperabilidad entre agentes
        externos. Si el comportamiento de un agente no debe depender de dónde corre físicamente su
        propio runtime, ¿qué necesitaría abstraerse — y hacia qué tipo de destino apuntaría esa
        adaptación, comparado con las dos anteriores?
      answered_by: RQ-CH21-02
    - id: GQ-CH21-03
      text: |
        Un run ya fue creado, con su identidad y su estado inicial ya instanciados. Describir sobre
        qué tipo de infraestructura corre ese run, ¿le pertenece a quien lo creó, o a un dueño
        completamente distinto que actúa después, sin haber participado en su creación?
      answered_by: RQ-CH21-03
    - id: GQ-CH21-04
      text: |
        Si un dato que un run procesa debe residir dentro de cierta jurisdicción, ¿esa misma
        restricción se aplica automáticamente al lugar físico donde se ejecuta el cómputo de ese
        run, o son dos preguntas relacionadas pero que conviene mantener separables?
      answered_by: RQ-CH21-04
  systems_lens:
    iceberg_visible_fact: |
      Veintiún capítulos reales, y `P-27` ("Deployment topology is independent from agent
      semantics") nunca fue citado con código real por ningún capítulo anterior — apareció
      exclusivamente como el nombre de un plano en la lista de "Canonical Enterprise Planes" de
      Amendment v1.1, sin una sola línea de pseudocódigo que lo materializara (ver seccion 2, El
      Problema).
    iceberg_patterns: |
      El patrón que se repite, ahora por octava vez desde `AdmissionController` (CH-14), es que un
      plano canónico completo de la enmienda puede quedar reducido, durante varios capítulos, a un
      nombre en una lista — hasta que alguien nota que ninguna otra frontera ya trazada (recursos,
      creación del run, comunicación externa) responde, ni siquiera parcialmente, la pregunta que
      ese plano protege (ver seccion 3, Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala `ExecutionFabricAdapter` (`CMP-019`), el octavo componente de este
      libro que no corresponde a ninguno de los once nombres de Article III — y el noveno y último
      plano canónico de Amendment v1.1 que este libro cubre — con una ficha que declara tanto lo
      que posee (`owns`: abstraer el substrato de cómputo concreto detrás de una interfaz uniforme)
      como lo que explícitamente NO posee (`does_not_own`: decidir cuánto puede consumir un run —
      `ExecutionController`, CH-07, la frontera más importante de este capítulo — ni instanciar el
      run que describe — `AgentCore`, CH-11) (ver seccion 8, Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es el mismo argumento que ya protegió la
      autorización desde `P-13`, ahora aplicado a la infraestructura de ejecución en vez de a las
      acciones o a los datos: que un run corra dentro de un proceso único o repartido en un
      clúster de mil nodos no debe cambiar, ni un bit, lo que ese run razona, decide o produce — la
      topología de despliegue es un hecho sobre DÓNDE se ejecuta el cómputo, nunca una entrada que
      el razonamiento del agente pueda observar o condicionar (ver seccion 4, Impacto
      Constitucional).
    reinforcing_loop: |
      Cada vez que un componente nuevo resuelve una pregunta que "suena" a infraestructura de
      ejecución — un presupuesto de recursos (CH-07), la creación de un run (CH-11) — crece la
      tentación de asumir que la topología de despliegue "ya quedó cubierta" por alguno de esos dos
      — hasta que un mismo harness necesita, de verdad, correr hoy en un proceso local y mañana en
      un clúster administrado, y ningún componente existente describe, siquiera, sobre qué corre.
    balancing_loop: |
      `resolveExecutionPlacement` (seccion 11) es el mecanismo de equilibrio: rechaza por defecto
      (fail-closed) un `ExecutionPlacement` sin referencia al run que describe — mismo principio
      fail-closed que `evaluatePolicyForToolCall` (CH-05) y `classifyData` (CH-20) ya aplicaron a
      sus propios dominios — en vez de permitir que una topología de despliegue quede, por
      omisión, sin ningún registro asociado a ningún run.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `resolveExecutionPlacement` produzca un
      `ExecutionPlacement` completamente autónomo de `AgentLoop.runTurn` (CH-01) — sin que esa
      función, ni `AgentState`, necesiten cambiar una sola línea para que la topología de
      despliegue exista como un hecho consultable. Si en cambio la topología se hubiera modelado
      como un campo embebido dentro de `AgentState` o `ExecutionContext`, cada capítulo futuro que
      tocara esos contratos habría tenido que cargar, para siempre, una responsabilidad ajena a la
      suya. Mantener `ExecutionPlacement` como un contrato independiente, referenciado por
      `runId`, es la forma en que este capítulo hace la independencia de `P-27` real por diseño de
      contratos, no solo por convención documentada.
  recall_questions:
    - id: RQ-CH21-01
      text: |
        ¿Qué componente describe la topología de despliegue sobre la que corre un run, y en qué se
        diferencia, con precisión, del componente que decide cuánto puede consumir ese mismo run
        contra su presupuesto?
      # respuesta esperada: ExecutionFabricAdapter (CMP-019); frontera con ExecutionController
      # (CMP-007, CH-07); P-27.
    - id: RQ-CH21-02
      text: |
        ¿Qué decide `ExecutionFabricAdapter`, y qué NO decide — en particular, respecto de la
        instanciación del `AgentState` inicial de un run?
    - id: RQ-CH21-03
      text: |
        ¿Qué campos tiene `ExecutionPlacement` (`C-031`), y por qué `runId` se modela como el
        identificador `RunId` ya existente, en vez de una referencia opaca `Text` como
        `subjectRef` en `AuditRecord` (CH-19) o `DataGovernanceLabel` (CH-20)?
    - id: RQ-CH21-04
      text: |
        ¿Por qué `ExecutionPlacement.residencyConstraint` es un concepto distinto de
        `DataGovernanceLabel.residencyRequirement` (CH-20), aunque ambos hablen de "dónde debe
        estar algo"?
  explain_prompts:
    - id: EP-CH21-01
      text: |
        `ExecutionFabricAdapter` posee describir sobre qué tipo de infraestructura corre un run ya
        existente — dentro de un proceso, en un worker, en un clúster, en una función serverless.
        Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee decidir cuánto
        tiempo o cuántos recursos puede consumir ese mismo run — ¿qué se confundiría, en la
        práctica, si la misma pieza de software decidiera dónde corre un run Y cuánto puede gastar?
      target_entity: CMP-019
    - id: EP-CH21-02
      text: |
        `ExecutionPlacement.residencyConstraint` describe dónde se ejecuta el CÓMPUTO de un run;
        `DataGovernanceLabel.residencyRequirement` (CH-20) describe dónde debe residir el DATO que
        ese run procesa. Explica qué problema real aparecería si un capítulo futuro colapsara
        ambos campos en uno solo, asumiendo que "el cómputo y el dato siempre tienen que estar en
        el mismo lugar".
      target_entity: C-031
  interleaved_questions:
    - id: IQ-CH21-01
      text: |
        `ExecutionController.evaluateExecutionContinuation` (CH-07) ya decide, con código real, si
        un run puede seguir contra su `ExecutionBudget` — comparando `usage.runtimeMsElapsed`
        contra `budget.maxRuntimeMs`, y `usage.concurrentToolsInFlight` contra
        `budget.maxConcurrentTools`, entre otros límites — sin que ninguno de esos campos indique,
        jamás, en qué tipo de infraestructura corre el run que los consume. Si ahora necesitamos
        saber, además, si ese run corre dentro de un proceso único o repartido en un clúster
        Kubernetes, ¿le correspondería a `evaluateExecutionContinuation` producir esa respuesta —
        ya que de todos modos está "mirando" el mismo run — o pertenece, otra vez, a un dueño
        distinto del que evalúa el presupuesto?
      current_chapter_entities: [CMP-019, C-031]
      prior_chapter_entities: [CMP-007, C-017]
      prior_chapter: CH-07
    - id: IQ-CH21-02
      text: |
        `AgentCore` (CH-11) ya instancia, con código real, el `AgentState` inicial de un nuevo run
        — asignando su `runId`, decidiendo su `sessionId`, y produciendo la primera transición
        formal de Article V (`CREATED → INITIALIZING`) — sin que ninguna de sus dos funciones
        decida, en ningún momento, sobre qué tipo de infraestructura de cómputo va a ejecutarse ese
        run una vez que `AgentLoop` tome el testigo. Si ahora ese run necesita, además, una
        descripción de su topología de despliegue, ¿le correspondería a `AgentCore` producirla en
        el mismo instante en que crea el `AgentState` — ya que de todos modos está "creando" ese
        run — o esa descripción pertenece, deliberadamente, a un componente que actúa después,
        sobre un run que ya existe?
      current_chapter_entities: [CMP-019, C-031]
      prior_chapter_entities: [CMP-011, C-003]
      prior_chapter: CH-11
    - id: IQ-CH21-03
      text: |
        `ModelGateway.invokeModel` (CH-03) ya selecciona, con código real, el provider de modelo
        correspondiente y adapta el turno hacia el `ModelRequest` que ese provider espera — una
        adaptación que apunta siempre HACIA AFUERA, hacia un proveedor de modelo externo. Si
        `ExecutionFabricAdapter` de este capítulo también "adapta" algo — el substrato de cómputo
        concreto detrás de una interfaz uniforme — ¿está resolviendo el mismo tipo de pregunta que
        `ModelGateway`, con un destino distinto, o son dos nociones de "adaptar" que apuntan en
        direcciones fundamentalmente distintas?
      current_chapter_entities: [CMP-019, C-031]
      prior_chapter_entities: [CMP-003, C-006]
      prior_chapter: CH-03
  flashcards:
    - id: FC-CH21-01
      front: |
        ¿Qué posee `ExecutionFabricAdapter`?
      back: |
        Abstraer el substrato de cómputo concreto sobre el que se materializa la ejecución de un
        run ya existente (in-process, worker, Kubernetes, serverless, cloud, edge, on-premise)
        detrás de una interfaz uniforme — cita literal, `P-27` ("Agent behavior MUST NOT depend on
        whether execution occurs in-process, on a worker, Kubernetes, serverless, cloud, edge or
        on-premise") — produciendo un `ExecutionPlacement` opaco y portátil que describe esa
        topología sin exponer el detalle real de cada substrato; registrar, cuando aplica, una
        restricción de residencia sobre DÓNDE se ejecuta ese cómputo; rechazar por defecto
        (fail-closed) un `ExecutionPlacement` sin referencia al run que describe.
      source_entity: CMP-019
      chapter_introduced_in: CH-21
      review_stage: DAY_1
    - id: FC-CH21-02
      front: |
        ¿Qué NO posee `ExecutionFabricAdapter`, y a qué componente pertenece la frontera más
        importante de este capítulo?
      back: |
        Decidir cuánto tiempo, cuántas tool calls concurrentes o cuánto presupuesto puede consumir
        un run (`ExecutionController`, `CMP-007`, CH-07 — frontera más importante: `ExecutionController`
        decide CUÁNTO puede consumir un run ya en marcha, en cualquier substrato;
        `ExecutionFabricAdapter` decide DÓNDE/EN QUÉ TIPO DE INFRAESTRUCTURA corre ese mismo run);
        invocar proveedores de modelo concretos (`ModelGateway`, `CMP-003`, CH-03 — adapta hacia
        afuera, hacia el proveedor; este componente adapta hacia abajo, hacia el substrato propio);
        adaptar protocolos de comunicación entre agentes externos (`AgentCommunicationGateway`,
        `CMP-013`, CH-15); instanciar el `AgentState` inicial de un run (`AgentCore`, `CMP-011`,
        CH-11 — describe sobre qué corre un run YA instanciado, nunca lo crea); clasificar
        requisitos de gobernanza de un dato (`DataGovernanceEngine`, `CMP-018`, CH-20); ejecutar el
        aprovisionamiento/scheduling real (Preview, infraestructura de borde).
      source_entity: CMP-019
      chapter_introduced_in: CH-21
      review_stage: DAY_1
    - id: FC-CH21-03
      front: |
        ¿Qué campos tiene `ExecutionPlacement` (`C-031`)?
      back: |
        `id` (`ExecutionPlacementId`), `runId` (`RunId`, el identificador ya existente desde CH-00
        — nunca una referencia opaca `Text`, porque el universo de lo que este contrato describe es
        siempre exactamente un run, nunca un tipo heterogéneo de dato), `topology`
        (`DeploymentTopology`, `ENUM` de siete valores citados literalmente de `P-27`:
        `IN_PROCESS`/`WORKER`/`KUBERNETES`/`SERVERLESS`/`CLOUD`/`EDGE`/`ON_PREMISE`),
        `computeResourceRef` (`Optional<Text>`, referencia opaca al recurso de cómputo concreto —
        nunca el detalle real de cada substrato), `residencyConstraint` (`Optional<Text>`,
        restricción de residencia geográfica SOBRE EL CÓMPUTO, distinta de
        `DataGovernanceLabel.residencyRequirement`) y `resolvedAt` (`Timestamp`).
      source_entity: C-031
      chapter_introduced_in: CH-21
      review_stage: DAY_1
    - id: FC-CH21-04
      front: |
        ¿Por qué `DeploymentTopology` tiene siete valores en vez de un `Boolean isDistributed` o
        un `ENUM` más corto?
      back: |
        Porque `P-27` enumera, literalmente, siete formas de despliegue ("in-process, on a worker,
        Kubernetes, serverless, cloud, edge or on-premise"), y cada una representa una realidad
        operacional distinta que un consumidor de `ExecutionPlacement` podría necesitar distinguir
        — un `Boolean` colapsaría las siete en dos categorías arbitrarias, y cualquier subconjunto
        menor a siete dejaría, sin representación posible, alguna topología que la propia
        Constitution ya nombra por su nombre. Mismo argumento, aplicado a topologías de despliegue,
        que ya motivó `DataClassificationLevel` (CH-20) y `RetentionEnforcementOutcome` (CH-20)
        frente a sus propios `Boolean` descartados.
      source_entity: C-031
      chapter_introduced_in: CH-21
      review_stage: DAY_1
    - id: FC-CH21-05
      front: |
        `ExecutionController.evaluateExecutionContinuation` (CH-07) ya evalúa `ExecutionBudget`
        contra el uso real de un run. ¿Por qué `ExecutionFabricAdapter` no extiende ese mismo
        mecanismo para incluir la topología de despliegue como un límite más?
      back: |
        Porque `ExecutionBudget` (`C-012`, CH-00) modela, deliberadamente, límites de CONSUMO —
        `maxTurns`/`maxToolCalls`/`maxInputTokens`/`maxOutputTokens`/`maxCost`/`maxRuntimeMs`/
        `maxConcurrentTools` — todos ellos preguntas de "cuánto", nunca de "dónde". Agregar un campo
        de topología a `ExecutionBudget` habría forzado a `ExecutionController` a ramificar su
        lógica según el substrato de cómputo concreto — exactamente lo que `P-27` prohíbe. La
        independencia que `P-27` exige solo es real si NINGÚN componente que decide "cuánto" necesita
        saber "dónde" — `ExecutionFabricAdapter` existe, en exclusiva, para que esa segunda pregunta
        tenga un dueño que nunca sea `ExecutionController`.
      source_entity: CMP-019
      chapter_introduced_in: CH-21
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH21-01
      recall_question: RQ-CH21-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH21-02
      recall_question: RQ-CH21-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH21-03
      recall_question: RQ-CH21-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH21-04
      recall_question: RQ-CH21-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 21 — ExecutionFabricAdapter y la Topología de Despliegue que el Comportamiento del Agente Nunca Debe Conocer

> **Regla constitucional (Amendment v1.1, `P-27`):** "Agent behavior MUST NOT depend on whether
> execution occurs in-process, on a worker, Kubernetes, serverless, cloud, edge or on-premise."

CH-14..CH-20 abrieron ocho de los nueve planos canónicos de Amendment v1.1 — Ingress & Activation
(`AdmissionController`), Agent Interoperability (`AgentCommunicationGateway`), Capability &
Integration (`CredentialBroker`), Reliability (`IdempotencyGuard`), Control
(`OperationalController`), Observability & Governance (`AuditLedger`) y Data & Context
(`DataGovernanceEngine`) — más el Execution Plane (segundo canónico), cubierto desde el propio
origen del libro por el núcleo de BH-v0.1: `AgentLoop` (CH-01, continuación de turno), `ToolRuntime`
(CH-02, ejecución de tool calls), `ModelGateway` (CH-03, invocación del modelo), `PolicyEngine`
(CH-05, autorización determinística) y `ExecutionController` (CH-07, presupuesto de ejecución) ya
materializan, con código real desde el primer tercio del libro, exactamente los mecanismos que ese
plano nombra. Esta es una corrección explícita sobre lo que CH-20 §0/§19 dejó dicho: aquel capítulo
contó el Execution Plane entre los planos "sin cubrir", conflacionándolo, sin proponérselo, con el
Execution Fabric — el noveno y último plano, y el único que, hasta este capítulo, seguía siendo
exclusivamente un nombre en una lista, sin una sola línea de pseudocódigo que lo materializara.

Este capítulo, el vigesimosegundo capítulo real de contenido de este libro, cierra esa última pieza.
`P-27` ("Deployment topology is independent from agent semantics") nunca había sido citado con código
real por ningún capítulo anterior — a diferencia de `P-22` (CH-16, luego CH-20) o `P-25` (CH-19), que
al menos habían sido citados en prosa antes de resolverse, `P-27` no aparece mencionado ni una sola
vez en los veintiún capítulos anteriores fuera de la propia transcripción de Amendment v1.1 en CH-00.
Con este capítulo, los nueve "Canonical Enterprise Planes" de Amendment v1.1 quedan, por primera vez,
completamente cubiertos por al menos un capítulo real de este libro.

Ningún texto de la Constitution nombra literalmente un componente para esto — igual que
`IdempotencyGuard` (CH-17), `OperationalController` (CH-18), `AuditLedger` (CH-19) y
`DataGovernanceEngine` (CH-20), el nombre que este capítulo adopta, `ExecutionFabricAdapter`, es una
**síntesis de este libro**, evaluada explícitamente contra alternativas (`DeploymentTopologyAdapter`,
descartado porque "Deployment" evoca, con demasiada fuerza, el proceso de release/CI-CD de una
versión de software — un dominio ya cercano al de `OperationalController` y su `ROLLOUT_ROLLBACK`,
CH-18 — cuando lo que este componente describe es, en cambio, dónde y sobre qué corre una ejecución
ya en marcha, no cómo se publica una versión nueva; `ExecutionSubstrate`, descartado porque nombra
correctamente el CONTRATO de datos que resulta —el sustrato de cómputo mismo—, pero no transmite que
existe un componente activo que produce esa descripción, verificándola y empaquetándola de forma
uniforme; un `STRUCT` puede llamarse `ExecutionSubstrate`, pero un `COMPONENT` necesita un nombre que
comunique una acción) y elegida porque conecta, sin ambigüedad, con el nombre que la propia enmienda
usa para el noveno plano canónico ("Execution Fabric") y con el patrón adapter-based que Amendment
v1.1 ya estableció para el único otro componente cuyo trabajo es, también, desacoplar el core de un
detalle externo variable (`AgentCommunicationGateway`, `P-19`, "integrated through
AgentCommunicationGateway adapters") — "Adapter" transporta, sin ambigüedad, que este componente
traduce una realidad de infraestructura variable hacia una interfaz uniforme, nunca que decide nada
sobre esa infraestructura (ver seccion 8).

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de saber
> cómo se llama el componente de este capítulo. El detalle estructurado de esta sección vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, para un run que ya existe, tres
preguntas que se confunden con facilidad porque las tres suenan a "recursos": cuánto puede consumir
ese run antes de detenerse, sobre qué tipo de infraestructura de cómputo se materializa su ejecución,
y quién lo creó en primer lugar. Podrás diseñar una descripción opaca y portátil de esa
infraestructura — su topología de despliegue, una referencia al recurso de cómputo concreto, y una
restricción de residencia geográfica si aplica — que viaje junto con el run sin que ningún componente
del núcleo del harness necesite ramificar su lógica según dónde corre.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e introduce
un contrato de datos nuevo y el octavo componente de este libro que pertenece a Amendment v1.1 en vez
de a los once nombres originales de Article III.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar atrás;
están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este capítulo va
a definir):

1. Ya existe un componente que decide, dentro de un presupuesto explícito, cuánto tiempo, cuántas
   tool calls concurrentes y cuánto costo puede consumir un run ya en marcha. ¿Esa misma decisión
   determina también en qué tipo de infraestructura de cómputo corre ese run — dentro de un único
   proceso, en un worker, en un clúster, en una función serverless — o son preguntas de un dominio
   completamente distinto?
2. Ya existe un componente que adapta la comunicación de un agente hacia un proveedor de modelo
   concreto, y otro que la adapta hacia protocolos de interoperabilidad entre agentes externos. Si el
   comportamiento de un agente no debe depender de dónde corre físicamente su propio runtime, ¿qué
   necesitaría abstraerse — y hacia qué tipo de destino apuntaría esa adaptación, comparado con las
   dos anteriores?
3. Un run ya fue creado, con su identidad y su estado inicial ya instanciados. Describir sobre qué
   tipo de infraestructura corre ese run, ¿le pertenece a quien lo creó, o a un dueño completamente
   distinto que actúa después, sin haber participado en su creación?
4. Si un dato que un run procesa debe residir dentro de cierta jurisdicción, ¿esa misma restricción se
   aplica automáticamente al lugar físico donde se ejecuta el cómputo de ese run, o son dos preguntas
   relacionadas pero que conviene mantener separables?

## 1. Arquitectura Actual (Current Architecture)

CH-00..CH-20 dejaron instalados treinta contratos de datos y dieciocho componentes: los once nombres
completos de Article III ("Agent Runtime"), dos capítulos de integración, y siete componentes de
Amendment v1.1 (`AdmissionController`, CMP-012, CH-14; `AgentCommunicationGateway`, CMP-013, CH-15;
`CredentialBroker`, CMP-014, CH-16; `IdempotencyGuard`, CMP-015, CH-17; `OperationalController`,
CMP-016, CH-18; `AuditLedger`, CMP-017, CH-19; `DataGovernanceEngine`, CMP-018, CH-20).

`ExecutionController` (CMP-007, CH-07) es, de los dieciocho, el único cuya responsabilidad completa
incluye decidir si un run puede seguir operacionalmente contra un límite explícito.
`evaluateExecutionContinuation` (CH-07 §11) compara `usage.runtimeMsElapsed` contra
`budget.maxRuntimeMs`, `usage.concurrentToolsInFlight` contra `budget.maxConcurrentTools`, y el resto
de los siete campos de `ExecutionBudget` (`maxTurns`, `maxToolCalls`, `maxInputTokens`,
`maxOutputTokens`, `maxCost`, `maxRuntimeMs`, `maxConcurrentTools`, C-012, CH-00) contra el uso real
ya acumulado de un run — produciendo un `ExecutionDecision` (`CONTINUE`/`STOP`/`CANCELLED`, C-017).
Cada uno de esos siete campos responde, sin excepción, a una pregunta de "cuánto": cuánto tiempo,
cuántas tool calls, cuántos tokens, cuánto dinero. Ninguno de los siete, ni `ExecutionBudget` como
conjunto, indica jamás sobre qué tipo de infraestructura de cómputo corre el run que los consume — un
mismo `ExecutionBudget` con `maxRuntimeMs = 60000` describe, con exactamente el mismo significado, un
run que corre dentro de un único proceso o uno repartido en mil nodos de un clúster.

`AgentCore` (CMP-011, CH-11) es, de los dieciocho, el único cuya responsabilidad completa incluye
instanciar el `AgentState` inicial de un run nuevo. `instantiateAgentState`/`validateAgentConfig`
(CH-11 §11) asignan `runId`, deciden `sessionId`, y producen la primera transición formal de Article V
(`CREATED → INITIALIZING`) — y CH-11 §8 ya excluyó explícitamente, en su propio `does_not_own`,
decidir nada de lo que ocurre una vez que ese run ya está `RUNNING`. Ninguna de las dos funciones de
`AgentCore` decide, en ningún momento, sobre qué tipo de infraestructura ese run recién creado va a
ejecutarse una vez que `AgentLoop` (CH-01) tome el testigo.

`ModelGateway` (CMP-003, CH-03) y `AgentCommunicationGateway` (CMP-013, CH-15) son, de los dieciocho,
los dos únicos componentes cuya responsabilidad completa consiste, en esencia, en adaptar: el primero
selecciona el provider de modelo correspondiente y traduce un turno hacia el `ModelRequest` que ese
provider espera (`P-02`, "Model access MUST be abstracted through a uniform provider interface");
el segundo adapta mensajes semánticos hacia protocolos de interoperabilidad externos entre agentes
(`P-19`, "integrated through AgentCommunicationGateway adapters"). Ambos apuntan, sin excepción, HACIA
AFUERA — hacia un proveedor de modelo concreto, o hacia un protocolo de comunicación entre agentes
externos. Ninguno de los dos, ni los dos juntos, resuelve una tercera dirección de adaptación que
ningún capítulo hasta este había separado explícitamente: no hacia afuera (un proveedor, un
protocolo), sino hacia ABAJO — hacia el propio substrato de cómputo sobre el que corre el harness que
ejecuta ambos adapters.

`P-27` ("Deployment topology is independent from agent semantics") fue transcrito, junto con el resto
de Amendment v1.1, en CH-00 §5 (la sección que introduce la enmienda completa como Preview) — pero
ningún capítulo posterior lo citó nunca en su propia sección de Impacto Constitucional, ni construyó
ningún mecanismo real que lo materializara. Ningún contrato de este libro, hasta este capítulo, modela
una descripción opaca de la topología de despliegue de un run.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas para esto, "dónde corre un run" tiende a colapsarse,
silenciosamente, en una de tres suposiciones igual de incompletas. La primera: que si
`ExecutionController` ya decide cuánto puede consumir un run, entonces ya sabe, de paso, dónde corre
— pero un `ExecutionBudget` de siete campos de "cuánto" nunca respondió, ni parcialmente, la pregunta
de "sobre qué tipo de infraestructura". La segunda: que si `AgentCore` ya crea el `AgentState` inicial
de un run, entonces también podría decidir, en ese mismo instante, sobre qué substrato va a correr —
pero CH-11 §8 ya trazó, con precisión, que `AgentCore` entrega el testigo a `AgentLoop` inmediatamente
después de `INITIALIZING`, sin decidir nada de lo que ocurre mientras el run está `RUNNING` — y dónde
corre ese run es, precisamente, una propiedad de su ejecución en curso, no de su creación. La tercera:
que, como `ModelGateway` y `AgentCommunicationGateway` ya "adaptan" hacia algo externo, cualquier
adaptación adicional podría absorberse dentro de uno de los dos — pero ninguno de los dos adapta hacia
el substrato de cómputo propio del harness; ambos adaptan hacia destinos externos al propio proceso
que los ejecuta.

Hay una segunda dimensión del problema, más delicada, y es la que da nombre a `P-27`: que el
comportamiento del agente NO DEBE depender de la topología de despliegue. Sin un componente dedicado,
la única forma en que un sistema real terminaría "respetando" esa independencia sería que cada
componente del núcleo —`AgentLoop`, `ModelGateway`, `ContextEngine`, `ToolRuntime`— incluyera, dentro
de su propia lógica, ramas condicionales según si corre en un proceso local, en un worker, o en un
clúster Kubernetes — exactamente la fragmentación que `P-27` prohíbe, y exactamente el mismo tipo de
acoplamiento que `P-19` ya previno para los protocolos de comunicación entre agentes ("Protocols
define interoperability; transports define delivery. Neither belongs inside Agent Core").

Hay una tercera dimensión, sutil: la residencia. `DataGovernanceEngine` (CH-20) ya resolvió, para
cualquier dato que fluye por el sistema, un requisito de residencia geográfica —
`DataGovernanceLabel.residencyRequirement`— que responde dónde debe residir o procesarse ESE DATO. Pero
un run entero, con su propio cómputo en ejecución, puede tener una restricción de residencia distinta
e independiente de la de cualquier dato particular que procese — por ejemplo, una jurisdicción que
exige que el cómputo mismo (no solo el dato) permanezca dentro de sus fronteras. Confundir ambos
conceptos —"dónde debe estar el dato" y "dónde debe ejecutarse el cómputo"— llevaría a que un capítulo
futuro reutilizara, sin pensarlo, el mismo campo para dos preguntas relacionadas pero no idénticas.

Necesitamos que "abstraer el substrato de cómputo concreto sobre el que corre un run" tenga, por fin,
un dueño único y nombrado — que produzca una descripción portátil y uniforme, capaz de acompañar a un
run ya existente sin que `AgentLoop.runTurn` (CH-01) necesite cambiar ni una línea, sin absorber la
decisión de presupuesto que ya pertenece a `ExecutionController`, y sin absorber la creación del run
que ya pertenece a `AgentCore`.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los treinta contratos y los dieciocho componentes que existen hasta este punto no bastan porque:

- `P-27` fue transcrito una sola vez, como parte de la transcripción completa de Amendment v1.1 en
  CH-00 §5, y nunca fue citado de nuevo, en Impacto Constitucional, por ningún capítulo posterior —
  a diferencia de `P-22` (citado en prosa por CH-10/CH-11 antes de resolverse en CH-16/CH-20), `P-27`
  llegó a este punto del libro sin ningún precedente parcial que resolver;
- `ExecutionBudget` (C-012, CH-00) declara siete campos, todos ellos límites de consumo — ninguno
  describe, ni de forma aproximada, sobre qué tipo de infraestructura corre el run que los consume;
  y `ExecutionController.does_not_own` (CH-07 §8) ya excluyó explícitamente cualquier decisión sobre
  continuación cognitiva o autorización, dejando un vacío real entre "cuánto puede consumir" y "dónde
  se ejecuta";
- `AgentState`/`ExecutionContext` (C-003/C-004, CH-00) no declaran ningún campo de topología de
  despliegue — y `AgentCore.does_not_own` (CH-11 §8) ya excluyó explícitamente decidir nada de lo que
  ocurre una vez que el run creado está `RUNNING`, dejando la pregunta de dónde corre sin ningún dueño
  entre la creación del run y su ejecución en curso;
- `ModelGateway` (CH-03) y `AgentCommunicationGateway` (CH-15) adaptan, los dos, hacia destinos
  externos al propio proceso que ejecuta el harness — ninguno de los dos modela una adaptación hacia
  el substrato de cómputo PROPIO sobre el que ese mismo proceso corre;
- `DataGovernanceLabel.residencyRequirement` (C-030, CH-20) modela, deliberadamente, dónde debe residir
  un DATO — extenderlo para describir, además, dónde debe ejecutarse el CÓMPUTO de un run habría
  reabierto un contrato ya registrado (`C-030`) para una responsabilidad que nunca le perteneció a
  `DataGovernanceEngine` en primer lugar: ese componente clasifica datos ya seleccionados o producidos,
  nunca el run completo que los produce;
- nada impide, hoy, que un capítulo de integración futuro conecte el núcleo del harness directamente
  contra un detalle real de infraestructura (un cliente de Kubernetes, un SDK de una plataforma
  serverless concreta) sin pasar antes por ninguna interfaz uniforme — exactamente el acoplamiento que
  `P-27` prohíbe;
- ningún componente de este libro declara, todavía, `owns` una responsabilidad que sea, literalmente,
  "describir el substrato de cómputo del run" en vez de "decidir cuánto puede consumir", "crear el run"
  o "adaptar hacia un destino externo" — las tres categorías más cercanas que CH-07/CH-11/CH-03/CH-15
  ya cubrieron, dejando a `P-27` sin un dueño propio hasta este capítulo.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la secuencia
> `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una entidad que no
> haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT` registrado — **no
> magic entities**. Este capítulo aplica la misma disciplina que CH-00..CH-20 ya establecieron.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-13   Authorization is deterministic and external to the LLM.
           El mismo argumento que ya protegió la autorización desde CH-01/CH-05, la credencial
           desde CH-16, la deduplicación desde CH-17, el control operacional desde CH-18, la
           evidencia de auditoría desde CH-19 y la gobernanza de datos desde CH-20, se extiende
           aquí a la infraestructura de ejecución: el modelo nunca decide, nunca ve y nunca
           constituye una fuente de verdad sobre la topología de despliegue de un run —
           resolveExecutionPlacement (seccion 11) es completamente determinística y externa al
           LLM, y no recibe ninguna entrada que el modelo haya producido.
    P-27   Deployment topology is independent from agent semantics.
           Primera materialización real, con código, de este principio — nunca antes citado con
           código real por ningún capítulo de este libro (solo transcrito como parte de Amendment
           v1.1 en CH-00 §5). ExecutionPlacement (seccion 6/7) y ExecutionFabricAdapter (seccion 8)
           producen, por fin, la descripción opaca y uniforme que permite que ningún componente del
           núcleo necesite ramificar su lógica según dónde corre.

Invariants preserved
    INV-18    Toda acción significativa produce un evento observable.
              resolveExecutionPlacement (seccion 11) emite un AgentEvent
              (EXECUTION_PLACEMENT_RESOLVED) cuando existe un ExecutionContext y un AgentId
              reales — pero, con la misma disciplina que CH-18/CH-19/CH-20 aplicaron a sus propias
              funciones, nunca fabrica esos campos cuando no existen (ver seccion 14).
    INV-19    Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy
              relevante.
              ExecutionPlacement no incluye un campo de actor propio (ver seccion 6 para el
              porqué explícito) — la trazabilidad de INV-19 se satisface aquí, igual que en
              DataGovernanceLabel (CH-20), a través del traceId que el AgentEvent condicional ya
              transporta.
    INV-20    Todo error operacional pertenece a una categoría conocida.
              El único fallo real de este capítulo (seccion 13) introduce EXECUTION_FABRIC, una
              categoría nueva de ErrorCategory — deliberadamente NO reutiliza BUDGET (CH-00,
              propio de límites de consumo) ni INFRASTRUCTURE (CH-00, propio de fallos de
              infraestructura de bajo nivel ya asumidos, nunca de la descripción misma de una
              topología), por la misma razón de fondo que motiva todo este capítulo: conflacionar
              un fallo de descripción de topología con el fallo de cualquier otro dominio sería,
              en espíritu, la misma conflación de responsabilidades que Article IV prohíbe a nivel
              de componente, ahora aplicada a nivel de ErrorCategory.

Component ownership changes
    CMP-019 ExecutionFabricAdapter se introduce — registry/components.yaml pasa de 18 a 19
    componentes. Es el octavo componente de este registry que NO corresponde a ninguno de los
    once nombres del árbol de Article III ("Agent Runtime") — pertenece, en cambio, al "Execution
    Fabric" de Amendment v1.1 (el noveno y último plano canónico, y el último que este libro
    cubre).
    registry/components.yaml de CMP-007 (ExecutionController), CMP-011 (AgentCore), CMP-003
    (ModelGateway), CMP-013 (AgentCommunicationGateway), CMP-018 (DataGovernanceEngine) NO se
    modifica: ninguno cablea todavía su relación real con ExecutionFabricAdapter (ver seccion
    9/18).

Lifecycle changes
    Ninguna modificación al ENUM AgentRunStatus (C-013): sigue siendo, sin cambios desde CH-01, el
    mismo conjunto de once valores. ExecutionPlacement (C-031), igual que DataGovernanceLabel
    (C-030, CH-20), no introduce ningún ENUM de lifecycle propio — el cambio se modela, otra vez,
    por reemplazo: una invocación nueva de resolveExecutionPlacement para el mismo runId produce
    un ExecutionPlacement nuevo (p. ej., tras un rebalanceo de infraestructura), nunca una edición
    del anterior (ver seccion 12).

Security implications
    ExecutionFabricAdapter es el primer componente de este libro cuya responsabilidad completa es
    describir la infraestructura de cómputo de un run, independientemente de cuánto puede consumir
    o de cómo fue creado. Ver seccion 15 para el análisis completo, incluyendo la frontera más
    importante de este capítulo, contra ExecutionController, y la frontera más precisa, contra
    AgentCore.

Observability implications
    Igual que DataGovernanceEngine (CH-20), OperationalController (CH-18) y AuditLedger (CH-19),
    ExecutionFabricAdapter emite AgentEvent de forma condicional — desde una única función
    (EXECUTION_PLACEMENT_RESOLVED), a diferencia de DataGovernanceEngine, que lo hace desde dos.

Deterministic vs agentic boundary
    Article XII se refina una decimonovena vez a nivel de componente: ExecutionFabricAdapter,
    igual que EventBus (CH-09), OperationalController (CH-18), AuditLedger (CH-19) y
    DataGovernanceEngine (CH-20), no recibe ninguna entrada que el modelo haya producido — ni
    siquiera de forma indirecta. Evalúa exclusivamente una referencia a un run ya existente, una
    topología ya decidida por un proceso de despliegue externo, y una referencia opaca al recurso
    de cómputo concreto — todos ajenos a cualquier razonamiento del modelo.
```

## 5. Conceptos Nuevos (New Concepts)

- **Deployment Topology** *(cita literal, `P-27`, "whether execution occurs in-process, on a worker,
  Kubernetes, serverless, cloud, edge or on-premise")*: el tipo de infraestructura de cómputo sobre la
  que se materializa la ejecución de un run concreto — modelado como `DeploymentTopology` (`ENUM` de
  siete valores, seccion 6), nunca un `Boolean` "es distribuido o no". Es la propiedad que `P-27`
  exige que el comportamiento del agente nunca observe ni condicione.
- **Compute Substrate (Opaque)**: el recurso de cómputo real y concreto sobre el que corre un run —
  un pod de Kubernetes, una invocación serverless, un proceso worker — modelado como
  `ExecutionPlacement.computeResourceRef` (`Optional<Text>`), una referencia opaca cuyo detalle real
  (qué proveedor, qué identificador exacto) es una señal de entrada asumida, nunca modelada por este
  capítulo — el mismo tratamiento que `residencyRequirement` (CH-20) o `lineageRef` (CH-20) ya dieron
  a un detalle real que queda, deliberadamente, fuera de alcance.
- **Execution Residency (distinta de Data Residency, CH-20)**: la restricción de que el CÓMPUTO de un
  run —no el dato que procesa— deba ejecutarse dentro de una región o jurisdicción concreta —
  modelada como `ExecutionPlacement.residencyConstraint` (`Optional<Text>`), un concepto relacionado
  pero deliberadamente distinto de `DataGovernanceLabel.residencyRequirement` (C-030, CH-20): un run
  puede tener una restricción de residencia sobre su cómputo sin que ningún dato particular que
  procese tenga, individualmente, la misma restricción, y viceversa (ver seccion 6).
- **Execution Fabric Adaptation** *(cita literal, `P-27`, "Agent behavior MUST NOT depend on...")*: la
  propiedad de que la topología de despliegue de un run se describa detrás de una interfaz uniforme,
  nunca embebida como una rama condicional dentro de la lógica del núcleo (`AgentLoop`, `ModelGateway`,
  `ContextEngine`, `ToolRuntime`) — el mismo argumento estructural que `P-19` ya aplicó a los
  protocolos de comunicación entre agentes, ahora aplicado al substrato de cómputo propio del harness.
- **Placement Portability**: la propiedad de que la descripción de la topología de un run no viva
  embebida dentro del propio `AgentState`/`ExecutionContext`, sino como un contrato independiente
  (`ExecutionPlacement`) referenciado por `runId` — de modo que ni `AgentState` ni `ExecutionContext`
  necesiten reabrirse cada vez que un capítulo futuro necesite describir, con más detalle, un
  substrato de cómputo nuevo.
- **Decision Ownership, aplicado por octava vez** *(Article IV)*: `ExecutionFabricAdapter` decide
  "¿sobre qué tipo de infraestructura corre este run?"; explícitamente NO decide "¿cuánto puede
  consumir este run contra su presupuesto?" (`ExecutionController`, ya resuelto, CH-07), "¿este run
  debe crearse, y con qué identidad inicial?" (`AgentCore`, ya resuelto, CH-11), "¿qué proveedor de
  modelo debe invocarse?" (`ModelGateway`, ya resuelto, CH-03) ni "¿qué protocolo de comunicación debe
  usarse hacia otro agente?" (`AgentCommunicationGateway`, ya resuelto, CH-15) — la primera de estas
  cuatro exclusiones es la frontera más importante de este capítulo (ver seccion 15).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `Text`, `Timestamp`, `Boolean`, `Optional`, `RunId`,
`AgentId`, `ExecutionContext` (C-004, CH-00), `AgentEvent` (C-010, CH-00), `HarnessError` (C-011,
CH-00).

Este capítulo cita, sin redefinirlo, un contrato ya registrado de un capítulo anterior — mismo patrón
de reuso explícito que CH-13 §6, CH-19 §6 y CH-20 §6 ya aplicaron:

| Contrato/tipo (reusado, no nuevo) | Introducido en | Uso en este capítulo |
|---|---|---|
| `ExecutionBudget` | CH-00 §6 | citado en prosa (seccion 1/3/5/8/15) como el precedente de "cuánto" que este capítulo distingue de "dónde" — nunca usado dentro del pseudocódigo de este capítulo |
| `DataGovernanceLabel` | CH-20 §6 | citado en prosa (seccion 2/5/8/15) para trazar la frontera entre residencia del cómputo y residencia del dato — nunca usado dentro del pseudocódigo de este capítulo |

### Un identificador opaco nuevo

Siguiendo el mismo patrón que CH-00 §6 estableció para los identificadores fundamentales, y que
CH-14..CH-20 repitieron para los suyos:

| Identificador (nuevo de este capítulo) | Identifica |
|---|---|
| `ExecutionPlacementId` | un `ExecutionPlacement` concreto — la topología de despliegue vigente asociada a un run dado |

**Por qué `ExecutionPlacement` referencia el run con `runId: RunId`, un identificador ya existente, y
no con una referencia opaca `Text` como `subjectRef` (`AuditRecord`, CH-19) o
`DataGovernanceLabel.subjectRef` (CH-20).** Se evaluó explícitamente seguir el mismo patrón de
`subjectRef: Text` opaco que ya usaron `AuditRecord` y `DataGovernanceLabel` — genérico por diseño,
porque el universo de lo que esos dos contratos referencian es heterogéneo (una `PolicyDecision`, un
`ControlDirective`, un `ContextBlock`, un `ToolResult`, entre otros tipos posibles). Se descartó para
este capítulo: lo que `ExecutionPlacement` describe es, siempre y sin excepción, la topología de
despliegue de UN RUN — nunca de un dato, nunca de una decisión, nunca de un evento. Ese universo no es
heterogéneo; es exactamente uno, y ese uno ya tiene un identificador fuerte y existente desde CH-00
(`RunId`). Usar `Text` opaco aquí habría renunciado, sin necesidad, a la verificación de tipos que
`RunId` ya provee de forma gratuita — la misma disciplina que ya evitó "reinventar" un identificador
donde uno real ya existía en cualquier otro capítulo de este libro.

### `ErrorCategory` — extendido, sin redefinir `HarnessError`

Este es el décimo capítulo que agrega un valor a `ErrorCategory` desde que CH-00 lo declaró (después
de `HUMAN_INTERACTION`, CH-06; `ADMISSION`, CH-14; `DELEGATION`, CH-15; `CREDENTIAL`, CH-16;
`IDEMPOTENCY`, CH-17; `CONTROL`, CH-18; `AUDIT`, CH-19; y `GOVERNANCE`, CH-20): el valor
`EXECUTION_FABRIC`, necesario porque ninguna de las dieciocho categorías ya existentes representa, sin
conflación, un fallo específico de describir la topología de despliegue de un run — reutilizar
`BUDGET` (CH-00, propio de límites de consumo) o `INFRASTRUCTURE` (CH-00, propio de fallos de bajo
nivel ya asumidos como externos) habría sido, precisamente, el tipo de conflación de dominios que
Article IV prohíbe a nivel de componente, ahora aplicada a nivel de `ErrorCategory`:

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
    CONTROL
    AUDIT
    GOVERNANCE
    EXECUTION_FABRIC
END
```

`HarnessError` (C-011) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — mismo patrón
exacto que las extensiones de CH-06/CH-14/CH-15/CH-16/CH-17/CH-18/CH-19/CH-20, aplicado aquí por
novena vez a `ErrorCategory`.

### `AgentEventType` — extendido, sin redefinir `AgentEvent`

CH-20 dejó `AgentEventType` en treinta valores. Este capítulo agrega un único valor nuevo — mismo
patrón que la mayoría de los capítulos del Amendment v1.1, salvo `IdempotencyGuard` (CH-17) y
`DataGovernanceEngine` (CH-20), que agregaron dos porque introdujeron dos funciones reales:

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
    CONTROL_DIRECTIVE_APPLIED
    AUDIT_RECORD_CREATED
    DATA_CLASSIFIED
    RETENTION_ENFORCEMENT_EVALUATED
    EXECUTION_PLACEMENT_RESOLVED
END
```

`AgentEvent` (C-010) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — solo el rango de
valores permitido para `eventType` crece, igual que en cada capítulo anterior salvo `EventBus`
(CH-09), `AdmissionController` (CH-14) y `AgentCommunicationGateway` (CH-15).

### `DeploymentTopology` — el tipo de infraestructura, citado literalmente de `P-27`

```pseudocode
ENUM DeploymentTopology
    IN_PROCESS
    WORKER
    KUBERNETES
    SERVERLESS
    CLOUD
    EDGE
    ON_PREMISE
END
```

**Por qué siete valores, citados literalmente de `P-27`, y no un `Boolean isDistributed` ni un
subconjunto más corto.** Se evaluó explícitamente un `Boolean` — más simple de construir — y se
descartó por el mismo argumento que ya descartó un `Boolean` en `DataClassificationLevel` (CH-20 §6):
un `Boolean` colapsaría siete realidades operacionales distintas (correr dentro del mismo proceso que
el resto del harness; correr en un worker separado pero en la misma máquina; correr orquestado por
Kubernetes; correr como una función serverless de vida efímera; correr en una nube pública genérica;
correr en un nodo edge cercano al usuario; correr on-premise dentro de la infraestructura propia de
una empresa) en dos categorías arbitrarias. Se evaluó también un subconjunto más corto —por ejemplo,
solo `IN_PROCESS`/`DISTRIBUTED`— y se descartó porque `P-27` nombra, literalmente, las siete
topologías por su nombre exacto: representar un subconjunto habría dejado, sin representación
posible, alguna topología que la propia Constitution ya distingue explícitamente. Siete valores,
citados palabra por palabra de `P-27`, son el mínimo necesario para no perder ninguna distinción que
la enmienda ya considera real.

### `ExecutionPlacement` — la descripción portátil de dónde corre un run

```pseudocode
STRUCT ExecutionPlacement
    id: ExecutionPlacementId
    runId: RunId
    topology: DeploymentTopology
    computeResourceRef: Optional<Text>
    residencyConstraint: Optional<Text>
    resolvedAt: Timestamp
END
```

Seis campos, cada uno respondiendo a una parte exacta del alcance decidido para este capítulo: `id`
identifica esta descripción de forma estable; `runId` referencia, con el identificador fuerte ya
existente desde CH-00, exactamente el run cuya ejecución se describe (ver el análisis explícito más
arriba, en esta misma sección, sobre por qué no es un `subjectRef: Text` opaco); `topology` es el
`DeploymentTopology` de la sección anterior; `computeResourceRef` es una referencia opaca
`Optional<Text>` al recurso de cómputo concreto — un identificador de pod, una invocación serverless,
un nombre de worker — cuyo formato exacto depende de la topología y queda, deliberadamente, sin
modelar (sección 5); `residencyConstraint` es, también, una referencia opaca `Optional<Text>` a una
restricción de residencia geográfica SOBRE EL CÓMPUTO, cuando aplica; `resolvedAt` registra cuándo se
produjo esta descripción.

**Por qué `computeResourceRef` y `residencyConstraint` son ambos `Optional`, y no campos
obligatorios.** No toda topología necesita, en la práctica, una referencia de recurso distinguible —
un run `IN_PROCESS` puede no tener ningún identificador de recurso más allá del propio proceso del
harness — y no todo run está sujeto a una restricción de residencia geográfica sobre su cómputo. Exigir
ambos campos como obligatorios habría forzado a fabricar valores centinela para los casos donde,
legítimamente, no aplican — exactamente el tipo de dato inventado que este libro evita (mismo
argumento que ya usó `retentionDeadline: Optional<Timestamp>` en `DataGovernanceLabel`, CH-20 §6).

**Por qué `ExecutionPlacement.residencyConstraint` es un concepto DISTINTO de
`DataGovernanceLabel.residencyRequirement` (C-030, CH-20), y no el mismo campo reusado.** Se evaluó
explícitamente reusar el tipo o incluso el propio campo de `DataGovernanceLabel` para representar
esta restricción — se descartó porque describen dos sujetos completamente distintos que, aunque
relacionados en la práctica, no son intercambiables por diseño: `DataGovernanceLabel.residencyRequirement`
restringe dónde debe residir o procesarse un DATO concreto — un `ContextBlock`, un `ToolResult` — y su
dueño es, sin excepción, `DataGovernanceEngine` (CH-20); `ExecutionPlacement.residencyConstraint`
restringe dónde debe ejecutarse el CÓMPUTO de un run completo, independientemente de los datos
particulares que ese run procese en cualquiera de sus turnos. Un run puede tener una restricción de
residencia sobre su propio cómputo sin que ningún dato específico que procese la tenga (por ejemplo,
una política operacional que exige que cierto tipo de carga de trabajo corra siempre dentro de una
región, sin importar qué datos toque); y, a la inversa, un dato con una restricción de residencia
estricta puede fluir a través de un run cuyo cómputo, en sí mismo, no está sujeto a ninguna
restricción geográfica propia (por ejemplo, un run `IN_PROCESS` que simplemente reenvía ese dato hacia
un side effect externo que sí respeta esa restricción, sin que el run mismo necesite estar anclado a
ninguna región). Colapsar ambos conceptos en un único campo asumiría, sin justificación, que el
cómputo y el dato siempre comparten exactamente la misma restricción — una suposición que, en la
práctica empresarial que `P-22`/`P-27` regulan por separado, no siempre se cumple. `ExecutionPlacement`
no consume `DataGovernanceLabel` como dependencia, ni lo referencia: `residencyConstraint` llega como
una señal de entrada ya resuelta, exactamente igual que `topology` o `computeResourceRef` (ver seccion
9).

**Por qué `ExecutionPlacement` no incluye un campo `actor: ActorId`, siguiendo el mismo argumento que
`DataGovernanceLabel` (CH-20 §6).** Se evaluó explícitamente agregarlo, siguiendo el precedente de
`INV-19`. Se descartó, con el mismo argumento exacto que ya usó `DataGovernanceLabel`:
`ExecutionPlacement` describe una propiedad de LA INFRAESTRUCTURA sobre la que corre un run —no una
decisión tomada por un actor humano o de sistema en un instante dado—, y la trazabilidad de `INV-19`
sigue siendo satisfecha a través del `traceId`/`agentId` que el `AgentEvent` condicional ya transporta
(seccion 14) cuando existen.

**Por qué `ExecutionPlacement` no tiene ningún campo de estado, y qué significa esa ausencia aquí.**
Igual que `DataGovernanceLabel` (CH-20 §12), la ausencia de un campo de estado no significa que un
`ExecutionPlacement` sea inmutable en el sentido de `AuditRecord` (CH-19): un run puede, en principio,
ser reprogramado hacia un substrato distinto durante su ciclo de vida (por ejemplo, un rebalanceo de
infraestructura administrado externamente) — ese cambio se modela por **reemplazo** (una invocación
nueva de `resolveExecutionPlacement` produce un `ExecutionPlacement` completamente nuevo, con un `id`
distinto), nunca por mutación de la instancia anterior (ver seccion 12).

**Unchanged / Not yet introduced**: `AgentState`/`ExecutionContext` (C-003/C-004, CH-00) no cambian de
forma — ninguno de los dos gana un campo `placement` en este capítulo (ver seccion 9/18).
`ExecutionBudget` (C-012, CH-00) tampoco cambia: sigue siendo, sin excepción, el contrato exclusivo de
límites de consumo. Ningún registro de "cuál es el `ExecutionPlacement` vigente actual para un
`runId` dado" cuando existen varios producidos en momentos distintos (ver seccion 18).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce un contrato de
datos, registrado en `registry/contracts.yaml`:

```text
ID:                     C-031
Name:                   ExecutionPlacement
Version:                v1
Introduced In:          CH-21
Current Definition:     STRUCT ExecutionPlacement (ver §6)
Used By:                [CMP-019]
Modified By:            []
Constitutional Impact:  [P-27, INV-19]
```

`C-031` es el decimoctavo id que este libro asigna sin que estuviera reservado desde CH-01 §7 — el
correlativo simplemente continúa después de `C-030` (CH-20). No colisiona, por nombre, con ningún
contrato ya registrado — verificado con grep completo sobre `registry/contracts.yaml` antes de
escribir este capítulo.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el octavo componente del registry que no corresponde a ninguno de los once
nombres del árbol de Article III ("Agent Runtime") — pertenece, en cambio, al "Execution Fabric" de
Amendment v1.1, el noveno y último plano canónico:

```pseudocode
COMPONENT ExecutionFabricAdapter
    consumes: ExecutionContext
    produces: ExecutionPlacement, AgentEvent, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Amendment v1.1 (`P-27`) — Article III no tiene, todavía,
una sección propia para este componente, exactamente igual que `AdmissionController` (CH-14),
`AgentCommunicationGateway` (CH-15), `CredentialBroker` (CH-16), `IdempotencyGuard` (CH-17),
`OperationalController` (CH-18), `AuditLedger` (CH-19) y `DataGovernanceEngine` (CH-20):

```text
COMPONENT: ExecutionFabricAdapter

Responsibility:
    Abstraer, detrás de una interfaz uniforme, el substrato de cómputo concreto sobre el que se
    materializa la ejecución de un run ya existente (in-process, worker, Kubernetes, serverless,
    cloud, edge, on-premise) — produciendo un ExecutionPlacement opaco y portátil que describe esa
    topología sin exponer el detalle real de cada substrato, y registrando, cuando aplica, una
    restricción de residencia sobre DÓNDE se ejecuta ese cómputo — sin decidir límites de recursos
    o presupuesto de un run, sin invocar proveedores de modelo, sin adaptar protocolos de
    comunicación entre agentes externos y sin instanciar el AgentState inicial de un run.

Consumes:
    C-004 ExecutionContext (solo cuando la resolución ocurre dentro de uno real, ver seccion 11)

Depends on:
    (ninguno todavía — el cableado real hacia AgentCore para runs recién creados, hacia
    ExecutionController para el ciclo de vida del run en curso, y hacia un Provisioning Adapter
    concreto de Kubernetes/serverless/edge, es Preview, no introducido en este capítulo; ver
    seccion 9)

Produces:
    C-031 ExecutionPlacement (la descripción de topología en sí), C-010 AgentEvent
    (EXECUTION_PLACEMENT_RESOLVED, solo cuando existe un ExecutionContext y un AgentId reales, ver
    seccion 14), C-011 HarnessError

Owns (Amendment v1.1 `P-27`, cita y lectura literal):
    - "Agent behavior MUST NOT depend on whether execution occurs in-process, on a worker,
      Kubernetes, serverless, cloud, edge or on-premise" (cita literal, P-27) — abstraer, en
      exclusiva, el substrato de cómputo concreto sobre el que corre la ejecución de un run detrás
      de una interfaz uniforme
    - producir, para un run ya existente (runId), una referencia opaca y uniforme al substrato de
      cómputo (topology + computeResourceRef) — nunca el detalle real de cada substrato concreto
    - registrar, cuando aplica, una restricción de residencia geográfica sobre DÓNDE se ejecuta el
      cómputo de un run — distinta de dónde debe residir el DATO que ese run procesa
    - rechazar por defecto (fail-closed) un ExecutionPlacement sin referencia al run que representa

Does NOT own:
    - decidir límites de recursos o presupuesto de un run — cuánto tiempo puede correr, cuántas
      tool calls concurrentes, cuánto cuesta (ExecutionController, CMP-007, ya introducido en
      CH-07 — la frontera más importante de este capítulo: ExecutionController decide CUÁNTO puede
      consumir un run ya en marcha, en cualquier substrato; ExecutionFabricAdapter decide DÓNDE/EN
      QUÉ TIPO DE INFRAESTRUCTURA corre ese mismo run — dos preguntas ortogonales sobre el mismo
      run)
    - invocar proveedores de modelo concretos (ModelGateway, CMP-003, ya introducido en CH-03 —
      ModelGateway adapta HACIA AFUERA, hacia qué proveedor de modelo; ExecutionFabricAdapter
      adapta HACIA ABAJO, hacia qué substrato de cómputo corre el propio harness)
    - adaptar protocolos de comunicación entre agentes externos (AgentCommunicationGateway,
      CMP-013, ya introducido en CH-15 — adapta hacia protocolos de interoperabilidad entre
      agentes, no hacia el substrato de cómputo del propio harness)
    - instanciar el AgentState inicial de un run (AgentCore, CMP-011, ya introducido en CH-11 —
      ExecutionFabricAdapter describe sobre qué substrato corre un run YA instanciado, nunca lo
      crea)
    - clasificar los requisitos de gobernanza de un dato, incluida su residencia
      (DataGovernanceEngine, CMP-018, ya introducido en CH-20 — residencyRequirement ahí describe
      dónde debe residir el DATO; residencyConstraint aquí describe dónde se ejecuta el CÓMPUTO
      del run — conceptos relacionados pero distintos, ver seccion 6)
    - ejecutar el aprovisionamiento real, el scheduling real, o el mecanismo real que efectivamente
      coloca un proceso dentro de un pod de Kubernetes, una función serverless o un nodo edge
      (Preview, infraestructura de borde — este componente decide QUÉ topología describir, nunca
      CÓMO se aprovisiona físicamente)
    - generar por sí mismo el runId, la topología o el computeResourceRef — todas llegan como
      señales de entrada ya resueltas (mismo patrón que subjectRef en CH-19/CH-20)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con la misma
particularidad que `AdmissionController`/`AgentCommunicationGateway`/`CredentialBroker`/
`IdempotencyGuard`/`OperationalController`/`AuditLedger`/`DataGovernanceEngine`: ninguna de las seis
exclusiones proviene de una ficha propia de Article III (que no existe para este componente); provienen
de fronteras ya establecidas por componentes ya registrados. La primera exclusión de esta lista es,
deliberadamente, la más parecida en prosa informal a lo que este componente sí posee — el mismo
cuidado editorial que CH-04 §8, CH-19 §8 y CH-20 §8 ya aplicaron frente a su propia frontera más
importante.

**Nota sobre Article IV.** A diferencia de `EventBus` (CH-09) y `AuditLedger` (CH-19), que no tienen
fila propia porque "distribuir" y "registrar" no son decidir, `ExecutionFabricAdapter` sí decide
algo real — qué descripción de topología corresponde a un run dado, y si esa descripción tiene una
restricción de residencia — igual que `DataGovernanceEngine` (¿qué requisitos de gobierno aplican?) o
`PolicyEngine` (¿está permitido?). Es, en ese sentido, más parecido a `DataGovernanceEngine` que a
`EventBus`: un componente que responde una pregunta real de dominio propio, no uno que solo preserva o
distribuye una respuesta ajena.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
ExecutionFabricAdapter
    consumes → ExecutionContext
    produces → ExecutionPlacement, AgentEvent, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`ExecutionFabricAdapter` no depende hoy de ningún otro componente registrado — mismo patrón que
CH-01..CH-20 ya establecieron para sus propios componentes. En prosa (nunca dentro de un bloque
`pseudocode`, per `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las relaciones
futuras que un capítulo de integración agregaría son:

| Componente futuro (relación inversa — no cableada en este capítulo) | Qué relación tendría con `ExecutionFabricAdapter` |
|---|---|
| `AgentCore` (ya existente, CMP-011) | `instantiateAgentState` (CH-11 §11) podría invocar, inmediatamente después de producir el primer `ExecutionContext` de un run nuevo, `resolveExecutionPlacement` sobre ese mismo `runId` — el cableado exacto que este capítulo deja explícitamente para un capítulo de integración futuro, sin tocar una sola línea de CH-11 |
| `ExecutionController` (ya existente, CMP-007) | `evaluateExecutionContinuation` (CH-07 §11) permanecería sin relación con `ExecutionFabricAdapter`: `ExecutionBudget` sigue siendo, sin excepción, el contrato exclusivo de límites de consumo — la frontera se mantiene, no se cablea |
| `OperationalController` (ya existente, CMP-016) | un `ControlDirective` de tipo `TENANT_ISOLATION` (CH-18 §6) podría, en principio, consultar el `ExecutionPlacement` de los runs de un tenant para decidir sobre qué substratos aplicar el aislamiento — sin que eso convierta a `ExecutionFabricAdapter` en un componente de control operacional |
| `AuditLedger` (ya existente, CMP-017) | podría auditar, con `recordAuditEntry` (CH-19 §11), el hecho de que una resolución de topología concreta ocurrió — usando el `id` de un `ExecutionPlacement` como `subjectRef` — sin que eso convierta a `ExecutionPlacement` mismo en evidencia inmutable (ver seccion 15) |
| `EventBus` (ya existente, CMP-009) | podría distribuir, como un `AgentEvent` más, `EXECUTION_PLACEMENT_RESOLVED` (seccion 14) — exactamente igual que distribuye el de cualquier otro productor |

`registry/components.yaml` de `CMP-003`, `CMP-007`, `CMP-011`, `CMP-013`, `CMP-016`, `CMP-017`,
`CMP-018` **no se modifica** en este capítulo: ninguno agrega `CMP-019` a sus `dependencies`, y
ninguno cambia su pseudocódigo. El pseudocódigo de la seccion 11 muestra a `ExecutionFabricAdapter`
resolviendo, de forma completamente autónoma, la topología de un `ExecutionContext` de ejemplo con la
forma exacta que `AgentCore` (CH-11) ya produce — sin que ese componente cambie una sola línea para
que este capítulo sea correcto. Ese cableado real de punta a punta es, explícitamente, trabajo de un
capítulo de integración futuro (ver seccion 18/19).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[AgentCore — instancia un AgentState/ExecutionContext ya existentes, CH-11, conceptual] →
ExecutionFabricAdapter → [ExecutionPlacement — la topología vigente, consultable por cualquier
componente futuro vía runId]
```

**Vista 2 — Sequence**

```text
ExecutionContext (runId ya asignado, ya producido por AgentCore.instantiateAgentState, CH-11 —
conceptual, sin cambios)
   │
   ▼
ExecutionFabricAdapter
   │ resolveExecutionPlacement(runId, topology, computeResourceRef, residencyConstraint,
   │   execution, agentId)
   │ ¿runId ausente? sí → HarnessError (EXECUTION_FABRIC_PLACEMENT_MISSING_RUN_ID)
   │ construye ExecutionPlacement (id, runId, topology, computeResourceRef,
   │   residencyConstraint, resolvedAt)
   │ ¿execution y agentId ambos resueltos? sí → emite: AgentEvent (EXECUTION_PLACEMENT_RESOLVED)
   ▼
ExecutionPlacement (la descripción de topología vigente para este runId)
   │
   │ ... integración futura: AgentCore (CH-11) invocaría resolveExecutionPlacement de verdad tras
   │     crear cada run nuevo; ExecutionController (CH-07) seguiría, sin cambios, evaluando
   │     únicamente ExecutionBudget/ExecutionUsage — nunca ExecutionPlacement; AuditLedger (CH-19)
   │     podría auditar el hecho de que una resolución de topología concreta ocurrió ...
```

**Vista 3 — Pseudocódigo**

Ver §11: `resolveExecutionPlacement` es la primera formalización ejecutable de "el comportamiento del
agente no depende de dónde corre su propio runtime" (`P-27`) — construida exclusivamente a partir de
material que ya existe (`ExecutionContext`/`AgentEvent`/`HarnessError`/`RunId` desde CH-00) más el
contrato y los `ENUM`/`STRUCT` nuevos de este capítulo.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde CH-00.

```pseudocode
FUNCTION resolveExecutionPlacement(
    runId: RunId,
    topology: DeploymentTopology,
    computeResourceRef: Optional<Text>,
    residencyConstraint: Optional<Text>,
    execution: Optional<ExecutionContext>,
    agentId: Optional<AgentId>
) -> ExecutionPlacement

    IF runId == NULL
        missingRunId: HarnessError = HarnessError(
            category = EXECUTION_FABRIC,
            code = "EXECUTION_FABRIC_PLACEMENT_MISSING_RUN_ID",
            message = "resolveExecutionPlacement fue invocada sin una referencia al run cuya ejecución se describe — un ExecutionPlacement nunca puede escribirse sin saber a qué run pertenece",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW missingRunId
    END

    placement: ExecutionPlacement = ExecutionPlacement(
        id = newExecutionPlacementId(),
        runId = runId,
        topology = topology,
        computeResourceRef = computeResourceRef,
        residencyConstraint = residencyConstraint,
        resolvedAt = now()
    )

    IF execution != NULL AND agentId != NULL
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = EXECUTION_PLACEMENT_RESOLVED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = placement
        )
    END

    RETURN placement
END
```

`now()`, `newEventId()` son las mismas primitivas de CH-00..CH-20. `newExecutionPlacementId()` sigue
el mismo patrón que `newDataGovernanceLabelId()` (CH-20) o `newAuditRecordId()` (CH-19). `topology`,
`computeResourceRef` y `residencyConstraint` llegan como parámetros ya resueltos por un proceso de
despliegue externo — este capítulo modela la forma de la descripción (opaca, uniforme, portátil), no
un motor real que decida a qué topología concreta debe asignarse un run nuevo, ni un catálogo real de
recursos de cómputo disponibles; esa decisión de asignación real es, deliberadamente, Preview,
infraestructura de borde, en el mismo espíritu que `dataGovernanceRuleFound`/`matchDataGovernanceRule`
(CH-20 §11) dejaron Preview el motor real de reglas de gobernanza.

**Por qué `resolveExecutionPlacement` no valida `topology`, a diferencia de `runId`.** `topology`
llega tipada como `DeploymentTopology`, un `ENUM` de siete valores cerrados — a diferencia de
`runId`, no existe ningún valor "vacío" o "ausente" que `topology` pueda tomar sin dejar de ser uno de
los siete valores válidos; la propia gramática del `ENUM` ya garantiza que, si `resolveExecutionPlacement`
recibe una `topology`, esa `topology` es una de las siete reconocidas por `P-27`. `computeResourceRef`
y `residencyConstraint`, por su parte, son `Optional` por diseño (seccion 6): su ausencia es un estado
válido, nunca un error. Por eso este capítulo introduce un único código de fallo real, a diferencia de
los dos de `classifyData` (CH-20 §11) — una diferencia legítima, no una inconsistencia: `classifyData`
recibía dos campos `Text` potencialmente vacíos (`subjectRef`, `provenance`); `resolveExecutionPlacement`
recibe solo un campo cuya ausencia constituye, de verdad, un uso incorrecto de la función (seccion 13).

Ahora, con `AgentCore` (CMP-011, CH-11) ya existente, se puede mostrar el ejemplo que motiva este
capítulo: asociar la topología de un run con el `ExecutionContext` real que `instantiateAgentState`
(CH-11 §11) ya produce, sin que `AgentLoop.runTurn` (CH-01 §11) necesite cambiar ni una línea:

```pseudocode
FUNCTION demonstrateAssociatingAnExecutionContextWithItsPlacement(
    execution: ExecutionContext,
    topology: DeploymentTopology,
    computeResourceRef: Optional<Text>,
    residencyConstraint: Optional<Text>,
    agentId: Optional<AgentId>
) -> ExecutionPlacement

    RETURN resolveExecutionPlacement(
        execution.runId,
        topology,
        computeResourceRef,
        residencyConstraint,
        execution,
        agentId
    )
END
```

`demonstrateAssociatingAnExecutionContextWithItsPlacement` es una demostración de integración, no una
segunda responsabilidad nueva — mismo patrón que `demonstrateClassifyingAContextBlock` (CH-20 §11) y
`demonstrateAuditingADeniedPolicyDecision` (CH-19 §11): no modifica `CMP-011 AgentCore`, ni su ficha,
ni la firma de `instantiateAgentState` (CH-11 §11), que sigue devolviendo exactamente lo mismo que
devolvía antes de este capítulo; tampoco modifica `AgentLoop.runTurn` (CH-01 §11), que sigue
recibiendo exactamente los mismos parámetros — `state`, `execution`, `modelFinished`,
`modelProposesToolCall` — sin ningún nuevo argumento de topología. `runTurn` puede ejecutarse, sin
ningún cambio, sin que exista jamás un `ExecutionPlacement` para el `runId` que procesa: la
independencia que `P-27` exige es, precisamente, que el comportamiento del agente nunca necesite que
esta función se haya invocado.

Nótese lo que `resolveExecutionPlacement` **nunca hace**: no invoca `ExecutionController.
evaluateExecutionContinuation` (CH-07) para decidir nada sobre presupuesto — ambas funciones son
completamente independientes, y pueden invocarse en cualquier orden, o ninguna, sin afectar a la otra;
no invoca `AgentCore.instantiateAgentState` (CH-11) para crear ningún run — recibe siempre un `runId`
ya existente; y no invoca `EventBus.distributeEvent` (CH-09) para propagar su resultado — el
`AgentEvent` que emite es, como mucho, una notificación, nunca el vehículo del resultado mismo.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no modifica `AgentRunStatus` (C-013): sigue siendo, sin cambios, el mismo `ENUM` de
once estados que `AgentLoop` (CH-01) formalizó.

`ExecutionPlacement`, igual que `DataGovernanceLabel` (C-030, CH-20), no declara ningún `ENUM` de
lifecycle propio:

```text
(ExecutionPlacement recién producido para un runId)
   → resolveExecutionPlacement(...)
     RETURN ExecutionPlacement — vigente para ese runId hasta que una invocación posterior de
     resolveExecutionPlacement produzca uno nuevo

(el mismo runId necesita una descripción de topología distinta más tarde — p. ej. un rebalanceo de
infraestructura administrado externamente movió el run hacia un substrato distinto)
   → resolveExecutionPlacement(...) se invoca de nuevo, con el mismo runId
     RETURN un ExecutionPlacement COMPLETAMENTE NUEVO (id distinto, resolvedAt posterior) — el
     anterior nunca se edita ni se reemplaza in place; simplemente deja de ser el más reciente
```

**Por qué la ausencia de un campo de estado aquí sigue el mismo argumento que `DataGovernanceLabel`
(CH-20 §12), no el de `AuditRecord` (CH-19 §12).** `AuditRecord` no tiene ningún campo de estado
porque introducir uno abriría, por la sola forma del `STRUCT`, la posibilidad conceptual de una
segunda escritura sobre el mismo registro — exactamente lo que `P-25` prohíbe. `ExecutionPlacement`,
en cambio, sí puede quedar obsoleto — una infraestructura administrada externamente puede reprogramar
un run hacia un substrato distinto — pero ese cambio nunca se modela como una transición interna del
mismo `STRUCT`: se modela por **reemplazo completo**, produciendo una nueva instancia con un nuevo
`id`, exactamente el mismo tratamiento que `DataGovernanceLabel` ya estableció para su propio
lifecycle.

**Lo que este capítulo explícitamente no cierra**: ningún mecanismo registra, todavía, cuál
`ExecutionPlacement` es "el vigente" para un `runId` dado cuando existen varios producidos en
momentos distintos — ver seccion 18.

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6, extendido en la seccion 6 de este capítulo) clasifica también
el único fallo real que introduce este capítulo:

```text
EXECUTION_FABRIC
    EXECUTION_FABRIC_PLACEMENT_MISSING_RUN_ID  — resolveExecutionPlacement fue invocada sin una
                                                   referencia al run cuya ejecución se describe
        → recoverable: FALSE, retryable: FALSE
```

El único fallo de este capítulo es `recoverable = FALSE` y `retryable = FALSE`: representa un uso
incorrecto de la propia invocación a `resolveExecutionPlacement` (una referencia de run faltante) —
no se corrige reintentando la misma operación tal cual, sino corrigiendo lo que se le provee.

**La distinción más importante de esta sección**: este fallo no se clasifica como `BUDGET` (CH-00,
propio de límites de consumo agotados) ni como `INFRASTRUCTURE` (CH-00, propio de fallos reales de
infraestructura de bajo nivel, no de la descripción misma de una topología) — aunque, estructuralmente,
"describir infraestructura" y "un fallo de infraestructura" suenan al mismo dominio, la diferencia no
es la forma del fallo, es su naturaleza: `EXECUTION_FABRIC_PLACEMENT_MISSING_RUN_ID` es un error de uso
de la propia función (un parámetro obligatorio ausente), nunca un fallo real del substrato de cómputo
subyacente (un pod que no arranca, una función serverless que se queda sin memoria) — ese segundo tipo
de fallo seguiría siendo, sin ambigüedad, `INFRASTRUCTURE`, exactamente como lo era antes de este
capítulo. El mismo argumento que ya usaron CH-16 §13 (contra `VALIDATION`), CH-18 §13 (contra
`CANCELLATION`), CH-19 §13 (contra `CONTROL`/`VALIDATION`) y CH-20 §13 (contra `CONTEXT`/`CREDENTIAL`).

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo real de `category =
INFRASTRUCTURE` que pudiera ocurrir en el mecanismo real de aprovisionamiento o scheduling que
efectivamente coloca un proceso dentro de un substrato concreto (un pod que falla al arrancar, una
invocación serverless que agota su timeout) — ese valor de `ErrorCategory` sigue, después de este
capítulo, sin que `ExecutionFabricAdapter` lo ejercite nunca (mismo límite que CH-14..CH-20 ya
documentaron para sus propias primitivas asumidas).

## 14. Eventos Producidos (Events Produced)

`ExecutionFabricAdapter` emite `AgentEvent` de forma condicional desde su única función real, agregando
`EXECUTION_PLACEMENT_RESOLVED` a `AgentEventType` (seccion 6), emitido únicamente cuando `execution` y
`agentId` llegan ambos resueltos (mismo patrón condicional que `AuditLedger`, CH-19,
`OperationalController`, CH-18, y `DataGovernanceEngine`, CH-20).

**Por qué la emisión es condicional.** Mismo argumento que `DataGovernanceEngine` (CH-20 §14): un
`AgentEvent` (C-010) exige `runId`/`sessionId`/`agentId`/`traceId` genuinos, y no toda resolución de
topología ocurre dentro de un `AgentRun` con esos cuatro campos ya resueltos — un proceso de
aprovisionamiento externo podría invocar `resolveExecutionPlacement` antes de que un run tenga,
siquiera, un `agentId` asignado.

**Por qué, incluso cuando emite, `EXECUTION_PLACEMENT_RESOLVED` no es evidencia de auditoría —
frontera explícita con `AuditLedger` (CH-19).** `payload = placement` transporta una copia del
resultado ya producido — pero, exactamente igual que `DATA_CLASSIFIED`/`RETENTION_ENFORCEMENT_EVALUATED`
(CH-20 §14), queda sujeto a las mismas garantías (o ausencia de garantías) que cualquier otro
`AgentEvent`: `EventBus` podría distribuirlo, perderlo si nadie está suscrito, o nunca llegar a existir
si `execution`/`agentId` no estaban resueltos. Si alguien necesitara, en cambio, evidencia
estructuralmente inmutable de que una resolución de topología concreta ocurrió, esa es, sin ambigüedad,
una responsabilidad de `AuditLedger` (CH-19) — nunca de este evento condicional (ver seccion 15).

**Por qué esto no es una limitación real hacia `INV-18`.** La acción verdaderamente significativa de
este capítulo — producir una descripción de topología vigente para un run — ya se cumple con el
`RETURN` directo de `resolveExecutionPlacement` a quien la invoca, sin depender de `AgentEvent`/
`EventBus` para "existir". El `AgentEvent` condicional es, aquí, una conveniencia de observabilidad
adicional, nunca el mecanismo que hace el resultado real.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

`ExecutionFabricAdapter` es el primer componente de este libro cuya responsabilidad completa es
describir la infraestructura de cómputo de un run, de forma independiente de cuánto puede consumir o
de cómo fue creado.

**La distinción con `ExecutionController` (CH-07), explícita, completa y la más importante de este
capítulo.** `ExecutionController.evaluateExecutionContinuation` (CH-07) decide, contra un
`ExecutionBudget` explícito, si un run ya en marcha puede seguir consumiendo turnos, tool calls,
tokens, costo y tiempo — una pregunta de "cuánto", completamente independiente de sobre qué
infraestructura corre ese consumo. `ExecutionFabricAdapter.resolveExecutionPlacement` (este capítulo)
decide, sobre ese mismo run, en qué tipo de infraestructura se materializa su ejecución — una pregunta
de `P-27`, completamente ortogonal al consumo. Las dos preguntas son, literalmente, independientes: un
run puede tener un `ExecutionBudget` generoso y correr, al mismo tiempo, `IN_PROCESS`; y, a la
inversa, un run con un `ExecutionBudget` muy ajustado puede correr distribuido en un clúster
`KUBERNETES` completo. Si `ExecutionController` fusionara ambas preguntas —ya que de todos modos está
"mirando" el mismo run para evaluar su continuación—, la independencia que `P-27` exige dejaría de ser
real: cada evaluación de presupuesto tendría que, de hecho, conocer la topología para decidir "cuánto",
exactamente el acoplamiento que `P-27` prohíbe, el mismo argumento que CH-20 §15 ya aplicó, con
matices distintos, a la frontera entre `DataGovernanceEngine` y `ContextEngine`.

**La distinción con `AgentCore` (CH-11), precisa y necesaria.** `AgentCore.instantiateAgentState`
(CH-11) ya asigna el `runId` de un run nuevo y produce su primer `ExecutionContext` — el momento
exacto en que ese run nace. `ExecutionFabricAdapter` no reclasifica jamás esa creación: actúa siempre
DESPUÉS, sobre un `runId` que ya existe, describiendo sobre qué substrato corre — nunca decidiendo si
ese run debe existir, ni con qué identidad inicial. Confundir esta frontera llevaría a que `AgentCore`
tuviera que conocer, en el instante de creación de un run, el catálogo completo de substratos de
cómputo disponibles — información que, por diseño, pertenece a un momento posterior y a un dominio
distinto, exactamente el tipo de "decisión absorbida por un componente vecino" que Article IV existe
para prevenir.

**La distinción con `ModelGateway` (CH-03) y `AgentCommunicationGateway` (CH-15), heredada y aplicada
aquí con una dirección nueva.** Los tres componentes "adaptan" algo, pero en direcciones distintas:
`ModelGateway.invokeModel` adapta HACIA AFUERA, hacia un proveedor de modelo concreto —
desacoplando el núcleo de un SDK de modelo particular (`P-02`). `AgentCommunicationGateway` adapta
también HACIA AFUERA, hacia un protocolo de interoperabilidad entre agentes externos — desacoplando el
núcleo de un SDK de A2A particular (`P-19`). `ExecutionFabricAdapter` adapta HACIA ABAJO — hacia el
substrato de cómputo sobre el que corre el propio proceso del harness, no hacia ningún destino externo
al que el harness se conecta. Confundir esta dirección llevaría a tratar la topología de despliegue
como si fuera un "proveedor" más, cuando en realidad describe algo estructuralmente distinto: no a
quién el harness le habla, sino sobre qué el harness mismo corre.

**`P-13`, extendido a la infraestructura de ejecución con la misma disciplina que todo el libro.**
`resolveExecutionPlacement` no recibe ninguna entrada que el modelo haya producido — ni siquiera de
forma indirecta. El modelo no decide la topología de despliegue de su propio run, no puede solicitar
un substrato distinto, y no puede, bajo ninguna circunstancia, observar o alterar un
`ExecutionPlacement` ya producido — la ausencia total del modelo en el pseudocódigo de este capítulo
es, otra vez, la materialización directa del mismo argumento que `P-13` ya estableció para la
autorización de acciones, ahora aplicado, por primera vez con código real, a la infraestructura de
ejecución.

**Límite que este capítulo deja explícitamente abierto.** `resolveExecutionPlacement` no modela ningún
control de acceso sobre **quién** puede invocarla, ni sobre **quién**, después, puede leer un
`ExecutionPlacement` ya producido — cualquier llamador puede, en este capítulo, producir una
descripción de topología para cualquier `runId`, o consultar la de cualquier otro. Autorizar la
escritura y la lectura de descripciones de topología (una pregunta con implicaciones reales: la
topología de despliegue de un run puede, en la práctica, revelar información operacional sensible
sobre la infraestructura de un tenant, `INV-E07`) queda, explícitamente, fuera de alcance de este
capítulo — el mismo límite que `AuditLedger` (CH-19 §15) y `DataGovernanceEngine` (CH-20 §15) ya
dejaron abierto para sus propios registros.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST ResolveExecutionPlacementRejectsAMissingRunId
TEST ResolveExecutionPlacementAcceptsEveryDeploymentTopologyValueFromP27
TEST ResolveExecutionPlacementNeverRequiresAComputeResourceRefOrAResidencyConstraint
TEST ResolveExecutionPlacementEmitsAnAgentEventOnlyWhenExecutionAndAgentIdAreBothResolved
TEST ExecutionFabricAdapterNeverDecidesExecutionBudgetContinuation
TEST ExecutionFabricAdapterNeverInstantiatesAnAgentState
TEST AgentLoopRunTurnSignatureIsUnchangedByExecutionPlacement
TEST ExecutionPlacementResidencyConstraintIsDistinctFromDataGovernanceLabelResidencyRequirement
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (después de CH-21 — noveno y último plano de Amendment v1.1 cubierto por este libro, y
primer capítulo que materializa P-27 con código real)

Constitution
 ├── Article IV     — Decision Ownership (tabla original sin cambios; ExecutionFabricAdapter, como
 │                     DataGovernanceEngine/PolicyEngine/ContextEngine, decide algo real — no
 │                     comparte la ausencia de fila de EventBus/AuditLedger)
 └── Amendment v1.1 — Enterprise Activation, Interoperability and Operations
                       (P-27 citado por primera vez con código real; Ingress & Activation Plane,
                       CH-14, Agent Interoperability Plane, CH-15, Capability & Integration Plane,
                       CH-16, Reliability Plane, CH-17, Control Plane, CH-18, Observability &
                       Governance Plane, CH-19, Data & Context Plane, CH-20, y Execution Fabric,
                       este capítulo — junto con el Execution Plane, cubierto desde el origen del
                       libro por el núcleo de BH-v0.1 — los nueve planos canónicos completos,
                       cubiertos por al menos un capítulo real de este libro)

Contracts (registry/contracts.yaml)
 ├── C-001..C-030  (sin cambios — CH-00..CH-20)
 └── C-031 ExecutionPlacement  (CH-21, nuevo — la descripción portátil de topología de despliegue
                        que viaja asociada a un run, P-27/INV-19)

Components (registry/components.yaml)
 ├── CMP-001..CMP-018  (sin cambios — CH-01..CH-20)
 └── CMP-019 ExecutionFabricAdapter  (CH-21, nuevo — octavo componente de este registry que no
                          corresponde a ninguno de los once nombres de Article III; pertenece al
                          Execution Fabric de Amendment v1.1)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado real de `AgentCore` hacia `resolveExecutionPlacement`**: `AgentCore.instantiateAgentState`
  (CH-11) no fue modificado para invocar de verdad `resolveExecutionPlacement` tras crear cada run
  nuevo — la demostración de la seccion 11 prueba que el mecanismo funciona, no que ya esté conectado
  dentro de un flujo real.
- **Cuál `ExecutionPlacement` es "el vigente"** para un `runId` dado cuando existen varios producidos
  en momentos distintos (p. ej. tras un rebalanceo de infraestructura): asumido, no construido (mismo
  límite que `registeredCapabilities`, CH-08, o el "vigente" de `DataGovernanceLabel`, CH-20 §18, ya
  documentaron para sus propios registros asumidos).
- **El motor real de asignación de topología**: quién decide, en la práctica, que un run nuevo deba
  correr `IN_PROCESS` frente a `KUBERNETES` — este capítulo modela la forma de la descripción (opaca,
  uniforme), no un scheduler real ni una política administrable de asignación.
- **El mecanismo real de aprovisionamiento y scheduling**: colocar efectivamente un proceso dentro de
  un pod de Kubernetes, invocar una función serverless, o desplegar hacia un nodo edge concreto queda,
  deliberadamente, sin modelar — Preview, infraestructura de borde.
- **Autorización de lectura/escritura sobre las propias descripciones de topología**: quién puede
  producir o consultar un `ExecutionPlacement` — señalado explícitamente en la seccion 15, no
  resuelto (mismo límite abierto que `AuditLedger`, CH-19 §15, y `DataGovernanceEngine`, CH-20 §15,
  dejaron para sus propios registros). `INV-E07` (aislamiento por tenant) tampoco se modela aquí.
- **Auditar una resolución de topología con `AuditLedger`**: ningún cableado real conecta todavía
  `ExecutionFabricAdapter` con `recordAuditEntry` (CH-19) para preservar evidencia inmutable de que
  una resolución concreta ocurrió — señalado en prosa (seccion 9/15), no construido.
- **La interacción real con `OperationalController` sobre aislamiento de tenant por substrato**: si
  un `ControlDirective` de tipo `TENANT_ISOLATION` (CH-18) debería, en la práctica, consultar
  `ExecutionPlacement` para decidir sobre qué substratos aplicar el aislamiento — señalado en prosa
  (seccion 9), no construido.
- **La profundización del Execution Fabric más allá de este primer componente** (p. ej. un catálogo
  real de substratos disponibles, o el cableado de punta a punta descrito arriba): explícitamente
  fuera de alcance.
- Reviewers plurales, evals y orquestación multi-agente propiamente dicha: explícitamente fuera de
  alcance de BH-v0.1.

## 19. Siguiente Incremento (Next Increment)

Con este capítulo, los nueve "Canonical Enterprise Planes" de Amendment v1.1 tienen, cada uno, al
menos un componente real que los materializa con código — pero ningún plano, incluido este, está
completamente construido de punta a punta: el cableado real entre `AgentCore` y
`ExecutionFabricAdapter`, el motor real de asignación de topología, el mecanismo real de
aprovisionamiento, y el registro de "cuál placement es el vigente" siguen sin construirse. El problema
natural del próximo incremento ya no es abrir un plano nuevo —los nueve están abiertos—, sino
profundizar cualquiera de ellos: cablear, por fin, alguno de los puntos de integración que CH-12/CH-13
ya establecieron como patrón para el camino feliz y los caminos de gobierno de un `AgentRun`, ahora
extendido a los siete componentes de Amendment v1.1 que, hasta este capítulo, permanecen sin invocarse
desde ningún flujo real del núcleo.

`next_chapter` queda en `null` en el frontmatter de este capítulo porque, en este momento del libro,
ese próximo capítulo todavía no existe como archivo — solo como el problema que motivaría su
escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg / Bucles
> de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows),
> secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): `P-27` nunca fue citado con código real por ningún capítulo
   anterior — apareció exclusivamente como el nombre de un plano en la lista de "Canonical Enterprise
   Planes", sin una sola línea de pseudocódigo que lo materializara.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): un plano canónico
   completo puede quedar reducido, durante varios capítulos, a un nombre en una lista — hasta que
   alguien nota que ninguna otra frontera ya trazada (recursos, creación del run, comunicación
   externa) responde, ni siquiera parcialmente, la pregunta que ese plano protege.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `ExecutionFabricAdapter` con una ficha que declara tanto lo que posee (`owns`: abstraer el
   substrato de cómputo detrás de una interfaz uniforme) como lo que explícitamente NO posee
   (`does_not_own`: decidir cuánto puede consumir un run — `ExecutionController`, CH-07 — ni
   instanciar el run que describe — `AgentCore`, CH-11).
4. **Modelos mentales** (= §4, Constitutional Impact): el mismo argumento que ya protegió la
   autorización de acciones (`P-13`) se extiende aquí a la infraestructura de ejecución (`P-27`) —
   que un run corra en un proceso único o en un clúster de mil nodos no debe cambiar, ni un bit, lo
   que ese run razona, decide o produce.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un componente nuevo resuelve una pregunta que "suena"
  a infraestructura de ejecución — un presupuesto de recursos (CH-07), la creación de un run (CH-11)
  — crece la tentación de asumir que la topología de despliegue "ya quedó cubierta" por alguno de
  esos dos, hasta que un mismo harness necesita correr, de verdad, sobre substratos distintos.
- **Bucle de equilibrio (estabiliza):** `resolveExecutionPlacement` (§11) rechaza por defecto un
  `ExecutionPlacement` sin referencia al run que describe — cerrando, con el mismo principio
  fail-closed que ya protegió la autorización desde CH-05 y la gobernanza de datos desde CH-20, el
  bucle que este capítulo abre.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `resolveExecutionPlacement` produzca un
`ExecutionPlacement` completamente autónomo de `AgentLoop.runTurn` (CH-01) — sin que esa función, ni
`AgentState`, necesiten cambiar una sola línea para que la topología de despliegue exista como un
hecho consultable. Mantener `ExecutionPlacement` como un contrato independiente, referenciado por
`runId`, es la forma en que este capítulo hace la independencia de `P-27` real por diseño de
contratos, no solo por convención documentada.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo de
> esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set` (frontmatter) y
> es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa, para lectura directa
> del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Ya existe un componente que decide cuánto tiempo, cuántas tool calls concurrentes y cuánto costo
   puede consumir un run ya en marcha. ¿Esa misma decisión determina también en qué tipo de
   infraestructura corre ese run, o son preguntas de dominios distintos? *(cierra la pregunta guía 1)*
2. Ya existe un componente que adapta hacia un proveedor de modelo, y otro que adapta hacia protocolos
   de interoperabilidad entre agentes. ¿Hacia qué destino apuntaría una tercera adaptación, si el
   comportamiento del agente no debe depender de dónde corre su propio runtime? *(cierra la pregunta
   guía 2)*
3. Un run ya fue creado. ¿Describir sobre qué infraestructura corre le pertenece a quien lo creó, o a
   un dueño distinto que actúa después? *(cierra la pregunta guía 3)*
4. Si un dato debe residir en cierta jurisdicción, ¿esa restricción aplica automáticamente al lugar
   donde se ejecuta el cómputo del run que lo procesa? *(cierra la pregunta guía 4)*

### Explicar

1. `ExecutionFabricAdapter` posee describir sobre qué tipo de infraestructura corre un run ya
   existente. Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee decidir
   cuánto tiempo o cuántos recursos puede consumir ese mismo run.
2. `ExecutionPlacement.residencyConstraint` describe dónde se ejecuta el cómputo de un run;
   `DataGovernanceLabel.residencyRequirement` (CH-20) describe dónde debe residir el dato. Explica qué
   problema aparecería si un capítulo futuro colapsara ambos campos en uno solo.

### Conectar

1. `ExecutionController.evaluateExecutionContinuation` (CH-07) ya evalúa un `ExecutionBudget` completo
   contra el uso real de un run. ¿Le correspondería a esa misma función producir, además, la
   descripción de topología de ese run, o pertenece a un dueño distinto?
2. `AgentCore` (CH-11) ya instancia el `AgentState` inicial de un run nuevo. ¿Le correspondería a
   `AgentCore` producir, en el mismo instante, la descripción de la topología sobre la que ese run va
   a ejecutarse?
3. `ModelGateway` (CH-03) ya adapta un turno hacia un proveedor de modelo concreto. ¿Es
   `ExecutionFabricAdapter` el mismo tipo de adaptación, con un destino distinto, o algo
   fundamentalmente diferente?

### Espaciar

Las cinco tarjetas de repaso de este capítulo (dos sobre `ExecutionFabricAdapter` — su `owns` y su
`does_not_own` —, dos sobre `ExecutionPlacement` — sus campos y por qué `DeploymentTopology` tiene
siete valores —, y una sobre la frontera con `ExecutionBudget`) entran hoy en `reviewStage = DAY_1`.
Repásalas de nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) — ver el apéndice de tarjetas
al final del libro (edición PDF) o `retrieval_set.flashcards` en `dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te equivocaste,
ese es precisamente el punto ciego que este método existe para revelar.
