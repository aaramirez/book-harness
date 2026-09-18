---
id: CH-18
title: "OperationalController y los Kill Switches Independientes de AgentLoop"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-016]
introduces_contracts: [C-028]
modifies_contracts: []
constitutional_articles: [P-13, P-30, INV-08, INV-18, INV-19, INV-20, INV-E14]
previous_chapter: CH-17
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH18
    text: |
      Al terminar este capítulo podrás distinguir, para cualquier decisión que detenga, deshabilite
      o aísle algo dentro del harness, qué tramo le pertenece en exclusiva al control operacional
      que actúa desde AFUERA de un `AgentRun` — capaz de deshabilitar una capability completa,
      aislar todos los runs de un tenant, revertir un rollout o forzar de inmediato la terminación
      de una ejecución, sin depender de que el modelo coopere ni de que ningún `AgentLoop` esté
      corriendo o respondiendo en ese instante — y qué tramo le pertenece a la evaluación de
      continuación operacional de UN run específico, hecha desde DENTRO de su propio ciclo. Podrás
      distinguir ambas preguntas con precisión, y diseñar, para un comando operacional emitido por
      un actor externo, un contrato con un tipo de al menos cuatro valores y un estado explícito de
      propagación — nunca un Boolean.
  skeleton:
    id: SK-CH18
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
    components_to_be_introduced: [CMP-016]
    contracts_to_be_introduced: [C-028]
  guiding_questions:
    - id: GQ-CH18-01
      text: |
        Si un operador humano —o un sistema de gobierno automatizado— necesita detener de
        inmediato una ejecución que se está comportando mal, sin depender de que esa ejecución
        coopere ni de que el ciclo que la gobierna llegue a revisarla en su próximo turno, ¿qué
        necesitaría existir para que esa detención ocurra de todos modos?
      answered_by: RQ-CH18-01
    - id: GQ-CH18-02
      text: |
        Ya existe, en este libro, un dueño para decidir si UN run puede seguir contra su propio
        presupuesto operacional, evaluado desde dentro del propio ciclo de esa ejecución. ¿Esa
        misma pregunta sirve también para deshabilitar una capability entera para todos los runs
        que la usen, o para aislar de golpe todos los runs de un tenant — o es, honestamente, una
        decisión de otra naturaleza, tomada desde otro lugar?
      answered_by: RQ-CH18-02
    - id: GQ-CH18-03
      text: |
        Si alguien revierte una versión de una capability ya desplegada, o aísla un tenant
        completo, ¿qué forma necesitaría tener el comando que representa esa acción — de modo que
        cualquiera, después, pueda saber quién lo emitió, a qué alcance aplicó, y si ya se propagó
        de verdad o todavía no?
      answered_by: RQ-CH18-03
    - id: GQ-CH18-04
      text: |
        Si dos mecanismos distintos —uno que vigila el presupuesto de una ejecución desde dentro
        de su propio ciclo, y otro que puede forzar su fin desde fuera, sin pedirle permiso—
        pudieran, en teoría, intentar terminar la misma ejecución casi al mismo tiempo, ¿qué
        debería pasar? ¿Alguno de los dos debería tener prioridad sobre el otro, o el simple orden
        en que cada uno llega a escribir el resultado ya decide todo?
      answered_by: RQ-CH18-04
  systems_lens:
    iceberg_visible_fact: |
      Dieciocho capítulos reales construyeron un runtime completo, más cuatro componentes de
      Enterprise (`AdmissionController`, CH-14; `AgentCommunicationGateway`, CH-15;
      `CredentialBroker`, CH-16; `IdempotencyGuard`, CH-17) — y ninguno de los dieciocho puede,
      hoy, detener una ejecución, deshabilitar una capability o aislar un tenant sin que algo
      dentro de esa misma ejecución tenga que cooperar primero. `ExecutionController`
      (`evaluateExecutionContinuation`, CH-07 §11) es lo más cerca que este libro ha llegado a
      "detener algo" — y, sin excepción, opera desde DENTRO del ciclo de evaluación de un único
      run, nunca desde afuera y nunca sobre más de un run a la vez (ver seccion 2, El Problema).
    iceberg_patterns: |
      `P-30` (Amendment v1.1, "Operational control can override autonomy") e `INV-E14` ("Kill
      switches operate independently of AgentLoop") fueron adoptados por este libro desde que
      Amendment v1.1 entró en vigor — pero, dieciocho capítulos después, ningún componente los
      había citado en prosa ni resuelto con código real: el "Control Plane" (sexto plano canónico
      de Amendment v1.1) seguía siendo, hasta este capítulo, el único de los cuatro planos que este
      libro ya había empezado a cubrir (Ingress & Activation, Agent Interoperability, Capability &
      Integration, Reliability) sin ningún componente propio (ver seccion 3, Por Qué la
      Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala el quinto componente de este libro que no corresponde a ninguno de los
      once nombres de Article III — y el quinto plano de Amendment v1.1 que este libro cubre
      (tras Ingress & Activation, CH-14; Agent Interoperability, CH-15; Capability & Integration,
      CH-16; y Reliability, CH-17), con una ficha que declara tanto lo que posee (`owns`: forzar la
      terminación inmediata de un `AgentRun` sin pasar por su ciclo cooperativo, deshabilitar una
      capability, aislar un tenant, revertir un rollout) como lo que explícitamente NO posee
      (cancelar UN run específico desde DENTRO de su propio ciclo por presupuesto —
      `ExecutionController`, CH-07 — la frontera más importante de este capítulo) (ver seccion 8,
      Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es que "¿puede este run seguir contra SU
      presupuesto, evaluado desde dentro de su propio ciclo?" (`ExecutionController`, CH-07) es una
      pregunta completamente distinta de "¿debe el control operacional forzar, desde afuera y sin
      pedir cooperación, la terminación de este run — o de algo más grande que un run?" (este
      capítulo) — dos preguntas que comparten un destino posible (`AgentRunStatus.CANCELLED`) pero
      nunca el mismo dueño, el mismo disparador ni el mismo momento (ver seccion 4, Impacto
      Constitucional).
    reinforcing_loop: |
      Cada vez que un sistema deja el control operacional dependiendo de la cooperación de lo que
      se quiere controlar, un incidente real (un agente atascado, un bucle costoso, una capability
      comprometida) se vuelve indetenible exactamente cuando más urge detenerlo — el mismo bucle de
      "la ausencia de un dueño se vuelve una dependencia implícita" que ya combatieron `P-02`
      (CH-03), `P-19` (CH-15), `INV-E08` (CH-16) e `INV-11` (CH-17), ahora aplicado al control
      mismo en vez de al modelo, al protocolo, al secreto o al side effect.
    balancing_loop: |
      `issueControlDirective`/`applyControlDirective` (seccion 11) son el mecanismo de equilibrio:
      antes de que un kill switch tenga efecto, `applyControlDirective` verifica que el
      `ControlDirective` no se haya aplicado ya (write-once) y que el `AgentRun` objetivo no haya
      alcanzado ya un `AgentRunStatus` terminal por otra vía — y, cuando ambas condiciones se
      cumplen, fuerza la transición sin invocar jamás `evaluateExecutionContinuation` (CH-07) ni
      esperar ningún turno de `AgentLoop` (CH-01).
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `applyControlDirective`, para el caso
      `KILL_SWITCH`, escriba directamente un `AgentState` nuevo con `status = CANCELLED` — la
      primera vez en todo el libro que un pseudocódigo real produce esa transición, y la primera
      vez que un componente distinto de `AgentLoop` transiciona `AgentRunStatus` (C-013). Si esta
      transición hubiera quedado, como en `ExecutionController` (CH-07), diferida a que un
      capítulo de integración futuro la cableara dentro de `AgentLoop.runTurn`, un kill switch
      dependería de la cooperación de ese mismo ciclo para tener efecto — exactamente lo que
      `INV-E14` prohíbe.
  recall_questions:
    - id: RQ-CH18-01
      text: |
        ¿Qué componente puede forzar la terminación de un `AgentRun`, deshabilitar una capability,
        aislar un tenant o revertir un rollout, sin depender de la cooperación del modelo ni de que
        `AgentLoop` lo procese en su próximo turno — y qué invariante de Amendment v1.1, citado
        literalmente, exige que el kill switch en particular funcione así?
      # respuesta esperada: OperationalController (CMP-016); INV-E14.
    - id: RQ-CH18-02
      text: |
        ¿En qué se diferencia "¿puede este run seguir contra su propio presupuesto?"
        (`ExecutionController`, CH-07, evaluado desde dentro del ciclo de ese run) de "¿debe el
        control operacional forzar, desde afuera, la terminación de este run — o deshabilitar,
        aislar o revertir algo a una escala mayor que un solo run?" (este capítulo)?
    - id: RQ-CH18-03
      text: |
        ¿Qué campos tiene `ControlDirective` (C-028), y por qué su campo `type` es un `ENUM` de al
        menos cuatro valores citados literalmente de `P-30`, mientras que su campo `status` nunca
        es un `Boolean`?
    - id: RQ-CH18-04
      text: |
        Si `OperationalController` emite un kill switch sobre un `AgentRun` que
        `ExecutionController` también podría haber detenido por presupuesto agotado, ¿quién gana,
        y qué regla explícita —no una ambigüedad tolerada— lo decide en este capítulo?
  explain_prompts:
    - id: EP-CH18-01
      text: |
        `OperationalController` posee forzar la terminación inmediata de un `AgentRun` mediante un
        kill switch. Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee
        decidir si ESE MISMO run puede seguir contra su presupuesto operacional — ¿qué se
        confundiría, en la práctica, si ambas preguntas se resolvieran en el mismo lugar?
      target_entity: CMP-016
    - id: EP-CH18-02
      text: |
        `ControlDirective.status` nunca es un `Boolean` "ya se aplicó / no se ha aplicado".
        Explica qué información real se perdería, y qué riesgo introduciríamos, si no
        distinguiéramos explícitamente un comando ya emitido de uno ya propagado con efecto real.
      target_entity: C-028
  interleaved_questions:
    - id: IQ-CH18-01
      text: |
        `ExecutionController.evaluateExecutionContinuation` (CH-07) produce una `ExecutionDecision`
        de tres estados evaluando exclusivamente `ExecutionBudget` y una señal de cancelación
        asumida como dada — pero nunca actúa si ningún turno de `AgentLoop` la invoca, y CH-07 §18
        dejó explícitamente pendiente que ningún pseudocódigo del libro escribiera todavía una
        transición real hacia `AgentRunStatus.CANCELLED`. Si este capítulo necesita forzar esa
        misma transición sin esperar a que exista ese cableado, ¿le correspondería reutilizar
        `evaluateExecutionContinuation` para lograrlo, o construir un camino completamente
        independiente hacia el mismo destino?
      current_chapter_entities: [CMP-016, C-028]
      prior_chapter_entities: [CMP-007, C-017]
      prior_chapter: CH-07
    - id: IQ-CH18-02
      text: |
        `CapabilityRegistry` (CH-08) registra cada `CapabilityDescriptor` con una versión explícita
        (`P-26`) y resuelve, contra ese registro, qué implementación satisface una capability
        solicitada — pero nunca modela si una capability ya registrada puede, además, estar
        deshabilitada por una decisión operacional externa. Si un `ControlDirective` de este
        capítulo declarara deshabilitada una capability completa, ¿le correspondería a
        `CapabilityRegistry.resolveToolCall` absorber esa verificación silenciosamente, o pertenece
        a un dueño distinto, aunque el mecanismo real de enforcement quede, honestamente, para un
        capítulo posterior?
      current_chapter_entities: [CMP-016, C-028]
      prior_chapter_entities: [CMP-008, C-018]
      prior_chapter: CH-08
    - id: IQ-CH18-03
      text: |
        `AgentLoop` (CH-01) es, desde su propio capítulo, el único productor real de transiciones
        de `AgentRunStatus` (C-013) — `runTurn` decide cada transición del ciclo cooperativo
        turno a turno. Si un `ControlDirective` de tipo `KILL_SWITCH` necesita forzar
        `AgentRunStatus.CANCELLED` sobre un run que en ese instante podría no estar cooperando en
        absoluto (un proceso atascado, un ciclo que no responde), ¿tendría sentido que ese kill
        switch tuviera que esperar a que `AgentLoop.runTurn` decidiera procesarlo, o la Constitution
        exige, por diseño, una vía que no dependa de esa cooperación?
      current_chapter_entities: [CMP-016, C-028]
      prior_chapter_entities: [CMP-001, C-013]
      prior_chapter: CH-01
  flashcards:
    - id: FC-CH18-01
      front: |
        ¿Qué posee `OperationalController`?
      back: |
        Forzar la terminación inmediata de un `AgentRun` mediante un kill switch, sin depender de
        la cooperación del modelo ni de `AgentLoop` (cita literal, `INV-E14`); deshabilitar una
        capability completa (a nivel de `CapabilityDescriptor`, C-018); aislar todos los runs de un
        tenant; revertir un rollout hacia una versión de capability ya desplegada (reusando el
        versionado de `P-26`/`C-018`) — las cuatro formas de que "operational control can override
        autonomy" (cita literal, `P-30`) — y rechazar por defecto (fail-closed) tanto un
        `ControlDirective` ya aplicado que se intenta reaplicar como un kill switch sobre un
        `AgentRun` que ya alcanzó un `AgentRunStatus` terminal.
      source_entity: CMP-016
      chapter_introduced_in: CH-18
      review_stage: DAY_1
    - id: FC-CH18-02
      front: |
        ¿Qué NO posee `OperationalController`, y a qué componente pertenece la distinción central
        de este capítulo?
      back: |
        Decidir si UN `AgentRun` específico puede seguir operacionalmente contra su
        `ExecutionBudget`, evaluado desde DENTRO del propio ciclo de esa ejecución
        (`ExecutionController`, CMP-007, CH-07 — distinción central: "¿puedo seguir intentando,
        evaluado desde dentro?" nunca es "¿debe el control externo forzar el fin, desde afuera,
        sin pedir cooperación?"); decidir si una acción/`ToolCall` ya resuelta está autorizada
        (`PolicyEngine`, CMP-005, CH-05); ejecutar el side effect en sí (`ToolRuntime`, CMP-002,
        CH-02); resolver qué implementación satisface una capability (`CapabilityRegistry`,
        CMP-008, CH-08); ni el mecanismo real y distribuido que efectivamente bloquea los runs de
        un tenant o impide invocar una capability ya deshabilitada (Preview, infraestructura de
        borde).
      source_entity: CMP-016
      chapter_introduced_in: CH-18
      review_stage: DAY_1
    - id: FC-CH18-03
      front: |
        ¿Qué campos tiene `ControlDirective` (C-028)?
      back: |
        `id` (`ControlDirectiveId`), `type` (`ControlDirectiveType`: `DISABLE_CAPABILITY` /
        `ISOLATE_TENANT` / `ROLLBACK` / `KILL_SWITCH` — cita literal de `P-30`), `targetRef`
        (`Text`, referencia opaca — `capabilityId`/`tenantId`/`rolloutId`/`runId` según el tipo),
        `issuedBy` (`ActorId`, reusado de CH-06 §6, trazabilidad `INV-19`), `status`
        (`ControlDirectiveStatus`: `ISSUED`/`APPLIED`, nunca un `Boolean`), `issuedAt` (`Timestamp`)
        y `appliedAt` (`Optional<Timestamp>`, poblado solo cuando `status = APPLIED`).
      source_entity: C-028
      chapter_introduced_in: CH-18
      review_stage: DAY_1
    - id: FC-CH18-04
      front: |
        ¿Por qué `ControlDirective.type` tiene cuatro valores en vez de uno solo dedicado a
        kill switches, y por qué `status` nunca es un `Boolean`?
      back: |
        `P-30` exige, en una sola frase, cuatro formas de control operacional independientes de la
        cooperación del modelo (deshabilitar capabilities, aislar tenants, revertir rollouts y kill
        switches) — colapsarlas en cuatro contratos separados habría duplicado `issuedBy`/`status`/
        `issuedAt`/`appliedAt` cuatro veces sin ninguna diferencia real de forma, solo de alcance
        (`targetRef`). `status` nunca es un `Boolean` porque "emitido" y "ya con efecto real"
        exigen respuestas distintas de un llamador: un `ControlDirective` `ISSUED` todavía no
        garantiza que el kill switch ya haya detenido nada; uno `APPLIED` sí — colapsar ambos en
        un único valor `TRUE` ocultaría, precisamente, la ventana en la que el comando existe pero
        todavía no tuvo efecto.
      source_entity: C-028
      chapter_introduced_in: CH-18
      review_stage: DAY_1
    - id: FC-CH18-05
      front: |
        Si un kill switch (`OperationalController`) y una evaluación de presupuesto
        (`ExecutionController`) pudieran, en teoría, terminar el mismo `AgentRun` casi al mismo
        tiempo, ¿quién gana?
      back: |
        `AgentRunStatus` es terminal-una-vez (Article V): quien escriba primero sobre un
        `AgentState` todavía no terminal gana, y `applyControlDirective` rechaza, fail-closed
        (`KILL_SWITCH_ON_TERMINAL_AGENT_STATE`), forzar un kill switch sobre un `AgentRun` que ya
        llegó a un estado terminal por otra vía. En la práctica, hasta este capítulo, el kill
        switch SIEMPRE gana: es la única de las dos vías que este libro ha cableado realmente hasta
        `AgentState.status` — `ExecutionController` (CH-07 §18) sigue dejando esa escritura como
        Preview, pendiente de un capítulo de integración futuro.
      source_entity: CMP-016
      chapter_introduced_in: CH-18
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH18-01
      recall_question: RQ-CH18-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH18-02
      recall_question: RQ-CH18-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH18-03
      recall_question: RQ-CH18-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH18-04
      recall_question: RQ-CH18-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 18 — OperationalController y los Kill Switches Independientes de AgentLoop

> **Regla constitucional (Amendment v1.1, `P-30`):** "The platform MUST support cancellation,
> capability disablement, tenant isolation, rollout rollback and kill switches without relying on
> model cooperation."
>
> **Regla constitucional (Amendment v1.1, `INV-E14`):** "Kill switches operate independently of
> AgentLoop."

CH-14, CH-15, CH-16 y CH-17 abrieron cuatro de los nueve planos canónicos de Amendment v1.1 —
Ingress & Activation (`AdmissionController`), Agent Interoperability (`AgentCommunicationGateway`),
Capability & Integration (`CredentialBroker`) y, saltando directamente a la séptima posición de la
enumeración canónica, Reliability (`IdempotencyGuard`). Este capítulo entra al **quinto plano que
este libro cubre** — el **Control Plane**, que en la enumeración de la enmienda ocupa la **sexta**
posición (Ingress & Activation → Execution → Agent Interoperability → Capability & Integration →
Data & Context → **Control** → Reliability → Observability & Governance → Execution Fabric), no la
quinta — verificado con grep directo contra `constitution/ARCHITECTURE_CONSTITUTION.md`, sin asumir
el orden de memoria. El mismo patrón de salto que ya usó `IdempotencyGuard` (CH-17) para el
Reliability Plane: este libro no cubre los nueve planos en su orden canónico, sino en el orden en
que cada uno adquiere una razón de peso para escribirse.

La razón de peso, aquí, es doble y explícita desde la propia Constitution: `P-30` ("Operational
control can override autonomy") exige, en una sola frase, cinco capacidades operacionales
—cancelación, deshabilitación de capabilities, aislamiento de tenant, rollback de rollout y kill
switches— que funcionen **sin depender de la cooperación del modelo**; e `INV-E14` exige,
adicionalmente y con más fuerza todavía, que los kill switches en particular **operen
independientemente de `AgentLoop`** — no solo del modelo, sino del propio ciclo que gobierna un
`AgentRun`. Ningún texto de la Constitution nombra literalmente un componente para esto — igual que
`IdempotencyGuard` (CH-17), el nombre que este capítulo adopta, `OperationalController`, es una
**síntesis de este libro**, evaluada explícitamente contra alternativas (`KillSwitchController`,
que habría descrito solo una de las cuatro capacidades que `P-30` exige; `ControlPlaneGateway`, que
habría sugerido —incorrectamente— que este componente es un adaptador de protocolo, como
`AgentCommunicationGateway`, CH-15) y elegida porque "Operational" describe con precisión el eje
que separa a este componente de todo lo construido hasta ahora: actúa sobre la operación del
harness **desde afuera**, nunca desde dentro del ciclo de una ejecución particular (ver seccion 8).

De las cinco capacidades que `P-30` exige, una ya tiene dueño parcial en este libro:
`ExecutionController` (CH-07) posee, literalmente, "cancellation" dentro de su `owns` (Article III:
"budgets; cancellation; deadlines; runtime limits; operational continuation"). Este capítulo no
puede, ni debe, duplicar esa responsabilidad — la distinción que traza con más cuidado que ninguna
otra es, precisamente, esa: `ExecutionController` cancela UN `AgentRun` específico **desde DENTRO**
del ciclo de ese mismo run (`evaluateExecutionContinuation` se invoca, en principio, dentro del
propio turno que evalúa); `OperationalController` actúa **desde AFUERA** — un operador humano, o un
sistema de gobierno automatizado, puede deshabilitar una capability completa, aislar un tenant o
revertir un rollout para TODOS los runs afectados, o forzar la terminación inmediata de un run
concreto mediante un kill switch, incluso sin que ese `AgentLoop` particular esté cooperando o
siquiera corriendo en ese instante (ver seccion 15 para el análisis completo, incluyendo el caso
límite en el que ambos mecanismos podrían, en teoría, competir por el mismo run).

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de saber
> cómo se llama el componente de este capítulo. El detalle estructurado de esta sección vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, para cualquier decisión que
detenga, deshabilite o aísle algo dentro del harness, qué tramo le pertenece en exclusiva al
control operacional que actúa desde AFUERA de un `AgentRun` — capaz de deshabilitar una capability
completa, aislar todos los runs de un tenant, revertir un rollout o forzar de inmediato la
terminación de una ejecución, sin depender de que el modelo coopere ni de que ningún `AgentLoop`
esté corriendo o respondiendo en ese instante — y qué tramo le pertenece a la evaluación de
continuación operacional de UN run específico, hecha desde DENTRO de su propio ciclo. Podrás
diseñar, para un comando operacional emitido por un actor externo, un contrato con un tipo de al
menos cuatro valores y un estado explícito de propagación, nunca un booleano.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e
introduce un contrato de datos nuevo y el quinto componente de este libro que pertenece a Amendment
v1.1 en vez de a los once nombres originales de Article III.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar atrás;
están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este capítulo
va a definir):

1. Si un operador humano —o un sistema de gobierno automatizado— necesita detener de inmediato una
   ejecución que se está comportando mal, sin depender de que esa ejecución coopere ni de que el
   ciclo que la gobierna llegue a revisarla en su próximo turno, ¿qué necesitaría existir para que
   esa detención ocurra de todos modos?
2. Ya existe, en este libro, un dueño para decidir si UN run puede seguir contra su propio
   presupuesto operacional, evaluado desde dentro del propio ciclo de esa ejecución. ¿Esa misma
   pregunta sirve también para deshabilitar una capability entera para todos los runs que la usen,
   o para aislar de golpe todos los runs de un tenant, o son, honestamente, dos preguntas distintas
   sobre materiales distintos?
3. Si alguien revierte una versión de una capability ya desplegada, o aísla un tenant completo,
   ¿qué forma necesitaría tener el comando que representa esa acción — de modo que cualquiera,
   después, pueda saber quién lo emitió, a qué alcance aplicó, y si ya se propagó de verdad o
   todavía no?
4. Si dos mecanismos distintos —uno que vigila el presupuesto de una ejecución desde dentro de su
   propio ciclo, y otro que puede forzar su fin desde fuera, sin pedirle permiso— pudieran, en
   teoría, intentar terminar la misma ejecución casi al mismo tiempo, ¿qué debería pasar? ¿Alguno
   de los dos debería tener prioridad, o el simple orden en que cada uno llega a escribir el
   resultado ya decide todo?

## 1. Arquitectura Actual (Current Architecture)

CH-00..CH-17 dejaron instalados veintisiete contratos de datos y quince componentes: los once
nombres completos de Article III ("Agent Runtime"), dos capítulos de integración, y cuatro
componentes de Amendment v1.1 (`AdmissionController`, CMP-012, CH-14; `AgentCommunicationGateway`,
CMP-013, CH-15; `CredentialBroker`, CMP-014, CH-16; `IdempotencyGuard`, CMP-015, CH-17). Ninguno de
los quince puede, hoy, detener una ejecución, deshabilitar una capability o aislar un tenant sin
que algo DENTRO de esa misma ejecución tenga que cooperar primero.

`ExecutionController` (CMP-007, CH-07) es, de los quince, el que más cerca ha llegado a "detener
algo": `evaluateExecutionContinuation` produce una `ExecutionDecision` de tres estados
(`CONTINUE`/`STOP`/`CANCELLED`) evaluando `ExecutionBudget` y una señal de cancelación
(`cancellationRequested`) ya asumida como dada. Pero, sin excepción, esa evaluación:

- se invoca sobre UN `AgentRun` específico, identificado por su propio `AgentState`/
  `ExecutionContext` — nunca sobre "todos los runs de un tenant" ni sobre "todos los runs que usan
  una capability";
- nunca escribe, ella misma, ninguna transición real de `AgentRunStatus` (C-013): CH-07 §12/§18
  documentó, en prosa, hacia qué estado terminal apuntaría cada `ExecutionDecision`, pero dejó
  explícitamente pendiente, para un capítulo de integración futuro, que algún pseudocódigo real
  produjera esa transición — ni `AgentLoop.runTurn` (CH-01) ni ningún otro componente construido
  hasta CH-17 la produce todavía;
- depende, para tener efecto, de que algo invoque `evaluateExecutionContinuation` en el momento
  correcto — típicamente, se asume, `AgentLoop.runTurn` en cada turno cooperativo (ese cableado
  sigue siendo Preview).

`CapabilityRegistry` (CMP-008, CH-08) registra cada `CapabilityDescriptor` (C-018) con un campo
`version: Text` explícito (`P-26`, "Capabilities have governed lifecycles") — pero
`resolveToolCall` nunca verifica si una capability ya registrada está, además, deshabilitada por
una decisión operacional externa; toda capability registrada se trata, implícitamente, como
disponible para siempre.

La Constitution ya exige esta capacidad, en una sola frase, desde Amendment v1.1:

- `P-30` ("Operational control can override autonomy"): "The platform MUST support cancellation,
  capability disablement, tenant isolation, rollout rollback and kill switches without relying on
  model cooperation."
- `INV-E14`: "Kill switches operate independently of AgentLoop."

Y esta misma exigencia ya fue nombrada, en prosa, sin resolverse: CH-07 §9 dejó constancia de que
`ExecutionController` "no depende hoy de ningún otro componente registrado" y que el cableado real
hacia `AgentLoop` "es, explícitamente, trabajo de un capítulo de integración futuro" — sin que
ningún capítulo posterior, hasta este, construyera la vía **no cooperativa** que `INV-E14` exige
por nombre.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas para esto, "el control operacional puede detener lo que
sea necesario" tiende a resolverse de la forma más frágil posible: asumiendo que la ejecución que
se quiere controlar seguirá cooperando el tiempo suficiente para notar la señal de detención. Un
agente atascado en un bucle costoso, un proceso que dejó de responder, una capability que empieza a
fallar de forma peligrosa para todos los tenants que la usan — ninguno de estos escenarios espera,
cortésmente, a que `AgentLoop.runTurn` decida revisar si debe seguir. Si la única vía hacia
"detener esto" pasa por el mismo ciclo que se quiere detener, esa vía puede, exactamente cuando más
se necesita, no llegar a ejecutarse nunca.

Hay una segunda dimensión del problema, tan real como la primera. `ExecutionController` (CH-07) ya
resuelve, con dueño propio, "¿puede ESTE run seguir contra SU presupuesto?" — una pregunta que se
responde comparando el estado interno de un run contra sus propios límites, y que existe,
literalmente, dentro del ciclo de vida de ese run. Pero "deshabilitar una capability para todos los
runs que la usen", "aislar todos los runs de un tenant" o "revertir la versión de una capability ya
desplegada" no son preguntas sobre un único run: son preguntas sobre un alcance más amplio —una
capability, un tenant, un rollout— que ningún run individual podría, por definición, responder por
sí mismo. Confundir ambas preguntas dejaría a `ExecutionController` absorbiendo silenciosamente una
responsabilidad que no le pertenece, o dejaría estas cuatro capacidades de `P-30` sin ningún dueño
en absoluto.

Hay una tercera dimensión, más sutil: incluso una vez que existe un comando operacional explícito
("deshabilita esta capability", "aísla este tenant", "aplica este kill switch"), sigue existiendo la
pregunta de si ese comando ya tuvo efecto real o si todavía es solo una intención registrada. Un
sistema que solo distinga "comando emitido" de "comando no emitido" con un simple booleano no puede
representar la ventana, real y potencialmente larga en un sistema distribuido, entre que un
operador emite un kill switch y que ese kill switch efectivamente detiene la ejecución objetivo.

Y hay una cuarta dimensión, la más delicada: si `OperationalController` puede, desde afuera, forzar
la terminación de un run que `ExecutionController` también podría haber detenido, desde dentro, por
presupuesto agotado — ¿qué pasa si ambos intentan actuar sobre el mismo run casi al mismo tiempo?
Dejar esta pregunta sin resolver de forma explícita sería, precisamente, el tipo de ambigüedad que
Article IV (Ownership Rule) prohíbe tolerar.

Necesitamos que "el control operacional puede detener, deshabilitar o aislar algo, sin depender de
que el modelo o `AgentLoop` cooperen" tenga, por fin, un dueño único y nombrado — que actúe desde
afuera del ciclo de cualquier run particular (nunca decida, de nuevo, si UN run puede seguir contra
su presupuesto — eso ya lo resolvió `ExecutionController`), que represente su alcance mediante una
referencia opaca en vez de intentar modelar tenants/rollouts/capabilities como entidades propias de
este registry, que distinga con un estado explícito un comando ya emitido de uno ya propagado, y
que resuelva, sin ambigüedad, qué pasa cuando compite por el mismo destino que `ExecutionController`
podría alcanzar por su propio camino.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los veintisiete contratos y los quince componentes que existen hasta este punto no bastan porque:

- `P-30` e `INV-E14` fueron adoptados desde que este libro incorporó Amendment v1.1 (CH-14) — pero,
  verificado con grep, ningún capítulo posterior los había citado en prosa, y ningún componente
  registrado había reclamado jamás, como propio, actuar "sin depender de la cooperación del
  modelo" a la escala que `P-30` exige (una capability, un tenant, un rollout — no solo un run);
- `ExecutionController.evaluateExecutionContinuation` (CH-07 §11) evalúa, en exclusiva, si UN
  `AgentRun` puede seguir contra SU `ExecutionBudget` — nunca si una capability entera debe
  deshabilitarse, si un tenant completo debe aislarse, o si un rollout debe revertirse; ampliar su
  alcance más allá de un único run invadiría, silenciosamente, un dominio que la propia
  Constitution asigna a un control operacional distinto (`P-30`, "override autonomy" — una frase
  que `ExecutionController`, por diseño, nunca cita);
- CH-07 §12/§18 documentó, honestamente, que ningún pseudocódigo de este libro escribe todavía una
  transición real hacia `AgentRunStatus.FAILED`/`CANCELLED`/`EXPIRED` — dejando, sin quererlo, a
  `INV-E14` sin ninguna vía real (cooperativa o no) hacia `CANCELLED` hasta este capítulo;
- `CapabilityDescriptor` (C-018, CH-08) declara una `version: Text` explícita desde CH-08 (`P-26`)
  — pero ningún componente verifica todavía si una capability registrada está, además,
  deshabilitada operacionalmente; el campo existe, la exigencia de `P-30` sobre él, no;
- ningún contrato de este libro representa, todavía, un comando operacional emitido por un actor
  externo con un alcance que pueda ser una capability, un tenant, un rollout o un run concreto —
  `AdmissionController` (CH-14) decide sobre una activación todavía sin agente resuelto,
  `AgentCommunicationGateway` (CH-15) sobre un mensaje entre agentes, `CredentialBroker` (CH-16)
  sobre una credencial, `IdempotencyGuard` (CH-17) sobre una ejecución con side effects — ninguno
  de los cuatro representa una orden operacional que se aplica DESDE AFUERA de cualquiera de esos
  procesos;
- nada impide que, sin un estado explícito de propagación, "el kill switch ya se emitió" se
  confunda con "el kill switch ya tuvo efecto" — perdiendo, exactamente, la ventana real que un
  sistema distribuido necesita representar entre ambos momentos.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la secuencia
> `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una entidad que no
> haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT` registrado — **no
> magic entities**. Este capítulo aplica la misma disciplina que CH-00..CH-17 ya establecieron, con
> una particularidad que ningún capítulo anterior enfrentó: es el primero cuyo pseudocódigo escribe,
> de verdad, una transición de `AgentRunStatus` (C-013) — y lo hace, deliberadamente, sin invocar a
> `AgentLoop` (CH-01) ni a `ExecutionController` (CH-07). CH-07 §12 había declarado que la máquina
> de estados de `AgentRunStatus` era, en ese momento del libro, "propiedad exclusiva de `AgentLoop`"
> — una afirmación correcta entonces, porque ningún otro componente podía, todavía, producir ninguna
> transición real. Este capítulo matiza esa afirmación sin contradecirla: el camino COOPERATIVO de
> esa máquina de estados sigue siendo, sin excepción, exclusivo de `AgentLoop`; pero `P-30`/`INV-E14`
> exigen, por diseño constitucional explícito, una segunda vía —no cooperativa, disparada por un
> `ControlDirective` de tipo `KILL_SWITCH`— hacia el mismo destino terminal. No es una violación de
> Article IV: es la propia Constitution definiendo, para una transición específica y un disparador
> específico, un segundo dueño (ver seccion 12/15 para el desarrollo completo).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-13   Authorization is deterministic and external to the LLM.
           El mismo argumento que ya protegió la autorización desde CH-01/CH-05, la credencial
           desde CH-16 y la deduplicación desde CH-17, se extiende aquí al control operacional: el
           modelo nunca decide, nunca ve y nunca constituye una fuente de verdad sobre si una
           capability está deshabilitada, un tenant está aislado o un run debe terminarse —
           issueControlDirective/applyControlDirective (seccion 11) son completamente
           determinísticos y externos al LLM.
    P-30   Operational control can override autonomy.
           Primera materialización real, con código, de este principio en todo el libro —
           ControlDirective (seccion 6/7) y OperationalController (seccion 8) formalizan, por
           primera vez, las cuatro capacidades que P-30 exige en una sola frase.

Invariants preserved
    INV-08    El harness es propietario del execution state.
              La transición forzada de AgentState.status = CANCELLED (seccion 11, caso
              KILL_SWITCH) es, igual que en AgentLoop (CH-01) y ExecutionController (CH-07), una
              decisión del harness — nunca del modelo, y nunca dependiente de que el modelo
              coopere para tener efecto.
    INV-18    Toda acción significativa produce un evento observable.
              applyControlDirective (seccion 11) emite un AgentEvent quando aplica un kill switch
              con éxito — pero, a diferencia de IdempotencyGuard (CH-17) o CapabilityRegistry
              (CH-08), no puede emitir un evento honesto para los otros tres tipos de
              ControlDirective, cuyo alcance no es un único run (ver seccion 14 para el porqué
              explícito y la limitación que esto deja abierta).
    INV-19    Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy
              relevante.
              ControlDirective.issuedBy (ActorId, reusado de CH-06 §6) correlaciona cada comando
              operacional con el actor —humano o sistema de gobierno— que lo emitió; el
              AgentEvent que applyControlDirective emite para KILL_SWITCH lleva el traceId del
              ExecutionContext del run afectado.
    INV-20    Todo error operacional pertenece a una categoría conocida.
              Los cuatro fallos reales de este capítulo (seccion 13) introducen CONTROL, una
              categoría nueva de ErrorCategory — ninguna de las quince ya existentes (incluida
              CANCELLATION, que pertenece a la cancelación de UN run evaluada dentro de su propio
              ciclo por ExecutionController) representa, sin conflación, un conflicto de un
              comando operacional emitido desde afuera.
    INV-E14   Kill switches operate independently of AgentLoop.
              Cita literal y definitoria de este capítulo — la primera vez que este libro escribe
              una transición real de AgentRunStatus sin invocar AgentLoop.runTurn ni
              ExecutionController.evaluateExecutionContinuation (seccion 11).

Component ownership changes
    CMP-016 OperationalController se introduce — registry/components.yaml pasa de 15 a 16
    componentes. Es el quinto componente de este registry que NO corresponde a ninguno de los
    once nombres del árbol de Article III ("Agent Runtime") — pertenece, en cambio, al "Control
    Plane" de Amendment v1.1 (el sexto plano canónico, quinto que este libro cubre — ver apertura
    del capítulo). registry/components.yaml de CMP-001 (AgentLoop) y CMP-007 (ExecutionController)
    NO se modifica: ninguno cablea todavía su relación real con OperationalController (ver
    seccion 9/18), y ninguno de los dos declaró jamás poseer, en su propio owns, la vía no
    cooperativa que INV-E14 exige.

Lifecycle changes
    Ninguna modificación al ENUM AgentRunStatus (C-013): sigue siendo, sin cambios desde CH-01, el
    mismo conjunto de once valores. Pero este capítulo SÍ es el primero en producir, con
    pseudocódigo real, una transición efectiva hacia CANCELLED — CH-07 §12 solo la había descrito
    en prosa, sin ningún código que la ejecutara. registry/contracts.yaml de C-003 (AgentState) y
    C-013 (AgentRunStatus) actualiza únicamente su lista used_by para incluir CMP-016 — ninguno de
    los dos STRUCT/ENUM cambia de forma.

Security implications
    OperationalController es el primer componente de este libro cuya responsabilidad completa es
    actuar DESDE AFUERA del ciclo de una ejecución, sin depender de su cooperación. Ver seccion 15
    para el análisis completo, incluyendo el caso límite del "empate" con ExecutionController.

Observability implications
    A diferencia de IdempotencyGuard/CapabilityRegistry/CredentialBroker (que siempre emiten
    porque el run ya existe) y de AdmissionController/AgentCommunicationGateway (que nunca emiten
    porque el run todavía no existe), OperationalController emite condicionalmente: solo cuando
    aplica un KILL_SWITCH sobre un run cuyo ExecutionContext ya se conoce (ver seccion 14).

Deterministic vs agentic boundary
    Article XII se refina una decimosexta vez a nivel de componente: OperationalController, igual
    que ExecutionController (CH-07), no recibe ninguna entrada que el modelo haya producido — ni
    siquiera de forma indirecta. Evalúa exclusivamente un ControlDirective ya construido y, cuando
    aplica, un AgentState ya resuelto — ambos completamente ajenos a cualquier razonamiento del
    modelo.
```

## 5. Conceptos Nuevos (New Concepts)

- **Operational Control** *(cita literal, `P-30`, "Operational control can override autonomy")*: la
  capacidad del harness de detener, deshabilitar o aislar algo — una capability, un tenant, un
  rollout, un run concreto — sin depender de que el modelo, o el ciclo que lo gobierna, cooperen.
  Distinta de la autonomía que el resto de este libro protege (Article I, "Model reasoning must
  remain probabilistic and replaceable"): `P-30` no discute la autonomía del modelo dentro de un
  turno normal, discute qué debe poder ocurrir CUANDO esa autonomía deja de ser deseable.
- **Kill Switch** *(cita literal, `P-30`/`INV-E14`)*: el mecanismo más inmediato de control
  operacional — forzar la terminación de un `AgentRun` específico, de inmediato, sin pasar por su
  ciclo cooperativo. `INV-E14` exige, con nombre propio, que esta vía sea independiente de
  `AgentLoop` — no una variante más rápida del mismo camino cooperativo, sino un camino
  completamente distinto hacia el mismo destino terminal.
- **Capability Disablement** *(lectura de `P-30`)*: deshabilitar una capability ya registrada
  (`CapabilityDescriptor`, C-018, CH-08) de modo que ningún `ToolCall` pueda resolverse contra ella
  mientras esté deshabilitada — sin resolver, este capítulo, el mecanismo real de enforcement (ver
  seccion 18).
- **Tenant Isolation** *(lectura de `P-30`, distinta de `INV-E07`, "Tenant data, memory,
  credentials, artifacts and audit records are isolated", ya citada por `CredentialBroker`, CH-16)*:
  detener o bloquear TODOS los runs de un tenant de una sola vez — no aislar sus datos entre
  tenants (eso ya lo exige `INV-E07`), sino aislar su capacidad de seguir ejecutando.
- **Rollout Rollback** *(lectura de `P-30`, reusa el versionado de `P-26`/`CapabilityDescriptor.
  version`, ya existente desde CH-08)*: revertir una capability desplegada hacia una versión
  anterior ya conocida — este capítulo no introduce un sistema de versiones nuevo, ni un contrato
  para representar un "rollout" como entidad propia; reusa `CapabilityDescriptor.version` (Text) ya
  existente como el identificador de la versión objetivo.
- **Control Directive**: el comando operacional explícito que representa cualquiera de las cuatro
  capacidades anteriores — quién lo emitió, a qué alcance opaco aplica, y si ya se propagó con
  efecto real o todavía no. Modelado como `ControlDirective` (C-028, seccion 6/7).
- **Operational Override**: la propiedad, exigida por `P-30`, de que un `ControlDirective` tenga
  efecto incluso cuando el proceso o ciclo objetivo no coopera — el eje que distingue a
  `OperationalController` de cualquier componente que, hasta CH-17, dependiera de que el propio run
  invocara su función en el momento correcto.
- **Decision Ownership** *(Article IV, en uso desde CH-01, aplicado aquí por quinta vez a un
  componente de Amendment v1.1)*: `OperationalController` decide "¿debe el control operacional
  forzar, desde afuera, la terminación de este run, o deshabilitar/aislar/revertir algo a una
  escala mayor que un run?"; explícitamente NO decide "¿puede este run específico seguir contra su
  propio presupuesto, evaluado desde dentro de su ciclo?" (`ExecutionController`, CH-07 — ver
  seccion 15 para el contraste completo, el más importante de este capítulo), "¿está autorizada
  esta acción?" (`PolicyEngine`, CH-05), "¿qué implementación satisface esta capability?"
  (`CapabilityRegistry`, CH-08) ni "¿cómo se ejecuta el side effect?" (`ToolRuntime`, CH-02).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `Text`, `Timestamp`, `Boolean`, `Optional`,
`AgentState` (C-003, CH-00), `ExecutionContext` (C-004, CH-00), `AgentEvent` (C-010, CH-00),
`HarnessError` (C-011, CH-00), `AgentRunStatus` (C-013, CH-01).

Este capítulo también reusa, sin redefinirlo, un identificador opaco introducido por un capítulo
anterior — mismo patrón de reuso explícito que CH-13 §6 ya aplicó al mismo tipo:

| Identificador (reusado, no nuevo) | Introducido en | Uso en este capítulo |
|---|---|---|
| `ActorId` | CH-06 §6 | tipo del campo `ControlDirective.issuedBy` — el mismo identificador opaco que ya usa `HumanInteractionResolution.resolvedBy` (C-016, CH-06) para trazar quién resuelve una interacción humana, aplicado aquí a quién emite un comando operacional |

### Un identificador opaco nuevo

Siguiendo el mismo patrón que CH-00 §6 estableció para los identificadores fundamentales, y que
CH-14/CH-15/CH-16/CH-17 repitieron para los suyos:

| Identificador (nuevo de este capítulo) | Identifica |
|---|---|
| `ControlDirectiveId` | un `ControlDirective` concreto — el comando operacional emitido para deshabilitar una capability, aislar un tenant, revertir un rollout o forzar un kill switch |

### `ErrorCategory` — extendido, sin redefinir `HarnessError`

Este es el séptimo capítulo que agrega un valor a `ErrorCategory` desde que CH-00 lo declaró
(después de `HUMAN_INTERACTION`, CH-06; `ADMISSION`, CH-14; `DELEGATION`, CH-15; `CREDENTIAL`,
CH-16; e `IDEMPOTENCY`, CH-17): el valor `CONTROL`, necesario porque ninguna de las quince
categorías ya existentes representa, sin conflación, un conflicto de un comando operacional emitido
desde afuera — `CANCELLATION` (CH-07) pertenece, en exclusiva, a la cancelación de UN run evaluada
desde DENTRO de su propio ciclo por `ExecutionController`; ninguna representa, sin conflación, "este
comando ya se aplicó y no se reaplica" o "este kill switch no tiene un run objetivo real sobre el
cual actuar":

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
END
```

`HarnessError` (C-011) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — mismo patrón
exacto que las extensiones de CH-06/CH-14/CH-15/CH-16/CH-17, aplicado aquí por sexta vez a
`ErrorCategory`.

### `AgentEventType` — extendido, sin redefinir `AgentEvent`

CH-17 dejó `AgentEventType` en veintiséis valores. Este capítulo agrega un único valor nuevo — mismo
patrón que CH-05/CH-07 (una sola operación real, no un par éxito/fallo — seccion 14 explica la razón
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
END
```

`AgentEvent` (C-010) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — solo el rango de
valores permitido para `eventType` crece, igual que en cada capítulo anterior salvo `EventBus`
(CH-09), `AdmissionController` (CH-14) y `AgentCommunicationGateway` (CH-15).

### `ControlDirectiveType` — cuatro valores, cita literal de `P-30`

```pseudocode
ENUM ControlDirectiveType
    DISABLE_CAPABILITY
    ISOLATE_TENANT
    ROLLBACK
    KILL_SWITCH
END
```

Cuatro valores, uno por cada sustantivo que `P-30` enumera explícitamente ("capability
disablement", "tenant isolation", "rollout rollback" y "kill switches") — deliberadamente sin un
quinto valor para "cancellation": esa quinta palabra de `P-30` ya tiene, desde CH-07, un dueño
propio (`ExecutionController.owns`, cita literal de Article III), y `KILL_SWITCH` es, precisamente,
la forma en la que `OperationalController` provee la mitad de "cancellation" que le corresponde a
él — la cancelación forzada **desde afuera**, sin depender de la cooperación del run objetivo —
mientras que la cancelación evaluada **desde dentro** del propio ciclo de un run, contra su
presupuesto, sigue siendo, sin excepción, de `ExecutionController` (ver seccion 15 para el
desarrollo completo de esta distinción).

### `ControlDirectiveStatus` — dos valores, nunca un `Boolean`

```pseudocode
ENUM ControlDirectiveStatus
    ISSUED
    APPLIED
END
```

**Por qué un `ENUM` de dos valores, y no un `Boolean` `applied`.** Se evaluó explícitamente un
campo `Boolean` — más simple de construir, y aparentemente suficiente: "¿ya se aplicó o no?". Se
descartó por la misma razón que ya motivó `IdempotencyRecordStatus` (CH-17): un `Boolean` de dos
estados solo distinguiría "aplicado" de "no aplicado" en el instante en que se consulta, pero no
le dice a un llamador si el comando siquiera EXISTE todavía como una intención registrada. `ISSUED`
representa la ventana, real en cualquier sistema distribuido, entre que un operador emite un
`ControlDirective` y que ese comando efectivamente se propaga y tiene efecto; `APPLIED` es terminal
y write-once — una vez alcanzado, `applyControlDirective` (seccion 11) rechaza reaplicarlo.

### `ControlDirective` — el comando operacional persistido

```pseudocode
STRUCT ControlDirective
    id: ControlDirectiveId
    type: ControlDirectiveType
    targetRef: Text
    issuedBy: ActorId
    status: ControlDirectiveStatus
    issuedAt: Timestamp
    appliedAt: Optional<Timestamp>
END
```

Siete campos, cada uno respondiendo a una parte exacta del alcance decidido para este capítulo:
`id` identifica este comando de forma estable; `type` es `ControlDirectiveType` (sección anterior);
`targetRef` es una referencia opaca (`Text`) — un `CapabilityId` cuando `type = DISABLE_CAPABILITY`,
un identificador de tenant cuando `type = ISOLATE_TENANT`, la versión objetivo de un rollout
(reusando `CapabilityDescriptor.version`, C-018) cuando `type = ROLLBACK`, o un `RunId` cuando
`type = KILL_SWITCH` — nunca embebiendo la entidad completa a la que se refiere, el mismo argumento
que ya usaron `CredentialReference.capability` (CH-16) e `IdempotencyRecord.capability` (CH-17)
para no cargar una copia de un objeto ajeno que podría desactualizarse; `issuedBy` es `ActorId`
(reusado de CH-06 §6) — trazabilidad literal de `INV-19`: quién, humano o sistema de gobierno,
emitió este comando; `status` es `ControlDirectiveStatus` (sección anterior); `issuedAt` registra
cuándo se emitió; `appliedAt` es `Optional<Timestamp>`, poblado únicamente cuando
`status = APPLIED`.

**Por qué un único `targetRef: Text` opaco, y no cuatro campos separados
(`capabilityId`/`tenantId`/`rolloutId`/`runId`)**. Se evaluó explícitamente modelar cuatro campos
`Optional`, uno por cada `ControlDirectiveType`, poblando solo el que correspondiera según `type`.
Se descartó: habría introducido tres campos que, en cualquier `ControlDirective` dado, están
garantizados `NULL` — el mismo tipo de ambigüedad estructural que `IdempotencyRecord.result`
(CH-17) evita al ser `Optional` una sola vez, no cuatro. `targetRef: Text`, con su significado
determinado por `type`, es el mismo patrón que ya usaron `ActivationRequest.sourceRef` (CH-14) y
`AgentCommunicationMessage.sourceAgentRef`/`targetAgentRef` (CH-15): una referencia opaca cuyo
significado exacto depende del contexto, documentado en prosa, no en cuatro campos del `STRUCT`.

### `ControlDirectiveApplication` — el resultado embebido de aplicar un directive (sin `C-XXX` propio)

```pseudocode
STRUCT ControlDirectiveApplication
    directive: ControlDirective
    updatedAgentState: Optional<AgentState>
END
```

Dos campos, embebidos dentro del resultado de `applyControlDirective` (seccion 11), sin contrato
`C-XXX` propio — el mismo patrón que `ExecutionUsage` (CH-07), `ContextBlock` (CH-04) o
`EventFilter` (CH-09): un tipo real, con campos propios, que ningún capítulo registra como
contrato independiente. `directive` es el `ControlDirective` ya completado (`status = APPLIED`);
`updatedAgentState` es `Optional<AgentState>` — poblado únicamente cuando `directive.type =
KILL_SWITCH` tuvo éxito (el `AgentState` del run objetivo, ya con `status = CANCELLED`), y `NULL`
para los otros tres tipos, cuyo alcance nunca es un único `AgentState`.

**Unchanged / Not yet introduced**: `AgentState` (C-003) y `AgentRunStatus` (C-013) no cambian de
forma — este capítulo los consume y, para el caso `KILL_SWITCH`, produce una nueva instancia de
`AgentState` con un valor ya existente de `AgentRunStatus` (`CANCELLED`), nunca un valor nuevo del
`ENUM`. Ningún `STRUCT` para representar un "tenant" o un "rollout" como entidades propias de este
registry: ambos permanecen, deliberadamente, como referencias opacas dentro de `targetRef` (ver
seccion 18).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce un contrato de
datos, registrado en `registry/contracts.yaml`:

```text
ID:                     C-028
Name:                   ControlDirective
Version:                v1
Introduced In:          CH-18
Current Definition:     STRUCT ControlDirective (ver §6)
Used By:                [CMP-016]
Modified By:            []
Constitutional Impact:  [P-30, INV-E14, INV-19]
```

`C-028` es el decimoquinto id que este libro asigna sin que estuviera reservado desde CH-01 §7 — el
correlativo simplemente continúa después de `C-027` (CH-17). No colisiona, por nombre, con ningún
contrato ya registrado — verificado con grep completo sobre `registry/contracts.yaml` antes de
escribir este capítulo.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el quinto componente del registry que no corresponde a ninguno de los once
nombres del árbol de Article III ("Agent Runtime") — pertenece, en cambio, al "Control Plane" de
Amendment v1.1:

```pseudocode
COMPONENT OperationalController
    consumes: ExecutionContext, AgentState
    produces: ControlDirective, AgentEvent, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Amendment v1.1 (`P-30`/`INV-E14`) — Article III no tiene,
todavía, una sección propia para este componente, exactamente igual que `AdmissionController`
(CH-14), `AgentCommunicationGateway` (CH-15), `CredentialBroker` (CH-16) e `IdempotencyGuard`
(CH-17):

```text
COMPONENT: OperationalController

Responsibility:
    Emitir y aplicar un comando operacional (ControlDirective) que deshabilita una capability,
    aísla los runs de un tenant, revierte un rollout o fuerza, mediante un kill switch, la
    terminación inmediata de un AgentRun — actuando siempre desde AFUERA del ciclo de cualquier
    run particular y sin depender de la cooperación del modelo ni de AgentLoop — sin decidir si
    UN run específico puede seguir contra su propio presupuesto operacional, sin autorizar
    ninguna acción ya resuelta, sin resolver qué implementación satisface una capability y sin
    ejecutar el side effect en sí.

Consumes:
    C-004 ExecutionContext, C-003 AgentState (solo para el caso KILL_SWITCH, ver seccion 11)

Depends on:
    (ninguno todavía — el cableado real hacia CapabilityRegistry para que una capability
    deshabilitada realmente deje de resolverse, hacia un mecanismo real de aislamiento
    distribuido de tenant, y hacia AgentLoop para que un kill switch aplicado se refleje en el
    resto del ciclo de vida del run, es Preview, no introducido en este capítulo; ver seccion 9)

Produces:
    C-028 ControlDirective (el comando, ISSUED o APPLIED, listo para que un capítulo de
    integración futuro lo consulte antes de resolver una capability, rutear una activación o
    continuar un run), C-010 AgentEvent (CONTROL_DIRECTIVE_APPLIED, solo para KILL_SWITCH
    aplicado con éxito), C-011 HarnessError

Owns (Amendment v1.1 `P-30`/`INV-E14`, cita y lectura literal):
    - "The platform MUST support cancellation, capability disablement, tenant isolation, rollout
      rollback and kill switches without relying on model cooperation" (cita literal, P-30 —
      "cancellation" se provee aquí exclusivamente como KILL_SWITCH, la mitad externa de esa
      palabra; la mitad interna, evaluada desde dentro del ciclo de un run, sigue siendo de
      ExecutionController, ver Does NOT own)
    - "Kill switches operate independently of AgentLoop" (cita literal, INV-E14)
    - emitir un ControlDirective (ISSUED) para cualquiera de los cuatro tipos, validando que su
      targetRef no esté vacío
    - forzar, para un ControlDirective de tipo KILL_SWITCH, la transición inmediata de un
      AgentState en un AgentRunStatus no terminal hacia CANCELLED — sin invocar
      evaluateExecutionContinuation (ExecutionController, CH-07) ni ningún turno de AgentLoop
      (CH-01)
    - registrar, de forma terminal y write-once, cuándo un ControlDirective ya se aplicó
      (APPLIED), rechazando reaplicar uno ya APPLIED
    - rechazar por defecto (fail-closed) un kill switch cuyo AgentRun objetivo ya alcanzó un
      AgentRunStatus terminal por cualquier otra vía — la regla explícita que resuelve el "empate"
      con ExecutionController (ver seccion 15)

Does NOT own:
    - decidir si UN AgentRun específico puede seguir operacionalmente contra su ExecutionBudget,
      evaluado desde DENTRO del propio ciclo de esa ejecución (ExecutionController, CMP-007, ya
      introducido en CH-07 — distinción central de este capítulo: "¿puedo seguir intentando,
      evaluado desde dentro de mi propio ciclo?" nunca es "¿debe el control externo forzar mi fin,
      desde afuera, sin pedir cooperación?"; la mitad de "cancellation" evaluada por presupuesto
      sigue siendo, sin excepción, de ExecutionController)
    - decidir si una acción/ToolCall ya resuelta está autorizada (PolicyEngine, CMP-005, ya
      introducido en CH-05 — distinta pregunta, distinto momento: "¿debe detenerse/deshabilitarse
      esto por control operacional?" nunca es "¿está permitido hacerlo?")
    - resolver qué implementación satisface una capability solicitada (CapabilityRegistry,
      CMP-008, ya introducido en CH-08 — este componente decide SI una capability está
      deshabilitada, nunca CUÁL implementación la satisface)
    - ejecutar el side effect en sí (ToolRuntime, CMP-002, ya introducido en CH-02)
    - generar el targetRef mismo, ni decidir a qué capability/tenant/rollout/run corresponde en el
      mundo real más allá de la referencia opaca ya provista (asumida como una señal de entrada
      dada, igual que otros capítulos asumen señales — ver seccion 6)
    - el mecanismo real y distribuido que efectivamente impide invocar una capability
      deshabilitada, bloquea físicamente los runs de un tenant aislado, o redespliega una versión
      anterior de un rollout (Preview, infraestructura de borde, ver seccion 18)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con la misma
particularidad que `AdmissionController`/`AgentCommunicationGateway`/`CredentialBroker`/
`IdempotencyGuard`: ninguna de las seis exclusiones proviene de una ficha propia de Article III
(que no existe para este componente); provienen de fronteras ya establecidas por componentes ya
registrados (`ExecutionController`, `PolicyEngine`, `CapabilityRegistry`, `ToolRuntime`). La primera
exclusión de esta lista es, deliberadamente, la más parecida en prosa informal a lo que este
componente sí posee — el mismo cuidado editorial que CH-07 §8 ya aplicó frente a `AgentLoop`.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
OperationalController
    consumes → ExecutionContext, AgentState
    produces → ControlDirective, AgentEvent, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`OperationalController` no depende hoy de ningún otro componente registrado — mismo patrón que
CH-01..CH-17 ya establecieron para sus propios componentes. En prosa (nunca dentro de un bloque
`pseudocode`, per `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las relaciones
futuras que un capítulo de integración agregaría son:

| Componente futuro (relación inversa — no cableada en este capítulo) | Qué relación tendría con `OperationalController` |
|---|---|
| `CapabilityRegistry` (ya existente, CMP-008) | `resolveToolCall` (CH-08 §11) consultaría, antes de resolver una capability, si existe un `ControlDirective` `APPLIED` de tipo `DISABLE_CAPABILITY` cuyo `targetRef` coincida con esa capability — el cableado exacto que este capítulo deja explícitamente para un capítulo de integración futuro, sin tocar una sola línea del `resolveToolCall` ya publicado en CH-08 |
| `AgentLoop` (ya existente, CMP-001) | reflejaría, en su propio ciclo, que un `AgentState` que le pertenece ya fue transicionado a `CANCELLED` por un `ControlDirective` de tipo `KILL_SWITCH` — sin que `AgentLoop.runTurn` tenga que invocar nada para que esa transición ya haya ocurrido (`INV-E14`) |
| `ExecutionController` (ya existente, CMP-007) | seguiría evaluando, sin cambios, si un `AgentRun` puede continuar contra su `ExecutionBudget` — una pregunta completamente anterior e independiente de si el control operacional decidió, desde afuera, forzar su fin (ver seccion 15) |
| `AdmissionController` (ya existente, CMP-012) | consultaría, antes de admitir una nueva `ActivationRequest`, si existe un `ControlDirective` `APPLIED` de tipo `ISOLATE_TENANT` cuyo `targetRef` coincida con el tenant de esa activación |
| Un mecanismo real de aislamiento distribuido de tenant, y un mecanismo real de redeploy de rollout (todavía sin componente propio en este registry) | garantizarían que un `ControlDirective` `APPLIED` de tipo `ISOLATE_TENANT`/`ROLLBACK` tenga efecto real sobre runs en curso y futuros — infraestructura de borde, fuera de este registry (ver seccion 18) |

`registry/components.yaml` de `CMP-001` (`AgentLoop`), `CMP-007` (`ExecutionController`) y `CMP-008`
(`CapabilityRegistry`) **no se modifica** en este capítulo: ninguno agrega `CMP-016` a sus
`dependencies`, y ninguno cambia su pseudocódigo. El pseudocódigo de la seccion 11 evalúa un
`ControlDirective`/`AgentState` de ejemplo de forma completamente autónoma — sin que ninguno de los
tres componentes ya existentes cambie una sola línea para que este capítulo sea correcto. Ese
cableado real es, explícitamente, trabajo de un capítulo de integración futuro (ver seccion 18/19).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[Operador humano / sistema de gobierno — externo, conceptual] → OperationalController →
[AgentState del AgentRun objetivo, forzado a CANCELLED — solo caso KILL_SWITCH; para los otros
 tres tipos, un alcance más amplio que un run — CapabilityRegistry/Tenant/Rollout, conceptual]
```

**Vista 2 — Sequence**

```text
Actor externo (humano u operador de gobierno) decide: deshabilitar una capability, aislar un
tenant, revertir un rollout, o aplicar un kill switch sobre un AgentRun
   │
   ▼
OperationalController
   │ issueControlDirective(type, targetRef, issuedBy)
   │ ¿targetRef vacío? sí → HarnessError (CONTROL_DIRECTIVE_MISSING_TARGET_REF)
   │ construye ControlDirective (status = ISSUED) — sin emitir ningún AgentEvent todavía (ningún
   │   ExecutionContext resuelto existe en este instante, ni siquiera para KILL_SWITCH)
   ▼
ControlDirective (ISSUED)
   │
   ▼
OperationalController
   │ applyControlDirective(directive, targetState, execution)
   │ ¿directive.status ya es APPLIED? sí → HarnessError (CONTROL_DIRECTIVE_ALREADY_APPLIED)
   │ ¿directive.type == KILL_SWITCH?
   │     sí → ¿targetState == NULL o execution == NULL? sí → HarnessError
   │             (KILL_SWITCH_MISSING_TARGET_CONTEXT)
   │          → ¿targetState.status ya es terminal? sí → HarnessError
   │             (KILL_SWITCH_ON_TERMINAL_AGENT_STATE) — el "empate" con ExecutionController se
   │             resuelve aquí: quien llega primero a un AgentRunStatus terminal, gana
   │          → construye un AgentState nuevo (status = CANCELLED) — SIN invocar
   │             evaluateExecutionContinuation (CH-07) ni ningún turno de AgentLoop (CH-01)
   │          → emite: AgentEvent (CONTROL_DIRECTIVE_APPLIED)
   │     no → (DISABLE_CAPABILITY / ISOLATE_TENANT / ROLLBACK: sin AgentState afectado, sin
   │          evento — el alcance no es un único run, ver seccion 14)
   │ marca ControlDirective como APPLIED (appliedAt = now())
   ▼
ControlDirectiveApplication (directive APPLIED, updatedAgentState solo si KILL_SWITCH)
   │
   │ ... integración futura: CapabilityRegistry.resolveToolCall (CH-08) consultaría un
   │     ControlDirective APPLIED de tipo DISABLE_CAPABILITY antes de resolver; AgentLoop (CH-01)
   │     reflejaría que su AgentState ya fue transicionado a CANCELLED por esta vía ...
```

**Vista 3 — Pseudocódigo**

Ver §11: `issueControlDirective`/`applyControlDirective` son la primera formalización ejecutable de
"el control operacional puede detener, deshabilitar o aislar algo sin depender de la cooperación del
modelo ni de `AgentLoop`" (`P-30`/`INV-E14`) — construidas exclusivamente a partir de material que ya
existe (`AgentState`/`ExecutionContext`/`AgentRunStatus` desde CH-00/CH-01, `ActorId` desde CH-06)
más el contrato y los `ENUM` nuevos de este capítulo.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde
CH-00/CH-01/CH-06.

```pseudocode
FUNCTION issueControlDirective(
    type: ControlDirectiveType,
    targetRef: Text,
    issuedBy: ActorId
) -> ControlDirective

    IF targetRef == ""
        error: HarnessError = HarnessError(
            category = CONTROL,
            code = "CONTROL_DIRECTIVE_MISSING_TARGET_REF",
            message = "issueControlDirective fue invocada sin una referencia de alcance (targetRef) — un ControlDirective nunca puede emitirse sin saber a qué capability/tenant/rollout/run aplica",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW error
    END

    directive: ControlDirective = ControlDirective(
        id = newControlDirectiveId(),
        type = type,
        targetRef = targetRef,
        issuedBy = issuedBy,
        status = ISSUED,
        issuedAt = now(),
        appliedAt = NULL
    )

    RETURN directive
END

FUNCTION applyControlDirective(
    directive: ControlDirective,
    targetState: Optional<AgentState>,
    execution: Optional<ExecutionContext>
) -> ControlDirectiveApplication

    IF directive.status == APPLIED
        conflict: HarnessError = HarnessError(
            category = CONTROL,
            code = "CONTROL_DIRECTIVE_ALREADY_APPLIED",
            message = "Este ControlDirective ya fue aplicado; applyControlDirective nunca reaplica un comando operacional ya terminal",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW conflict
    END

    updatedState: Optional<AgentState> = NULL

    IF directive.type == KILL_SWITCH
        IF targetState == NULL OR execution == NULL
            missing: HarnessError = HarnessError(
                category = CONTROL,
                code = "KILL_SWITCH_MISSING_TARGET_CONTEXT",
                message = "Un ControlDirective de tipo KILL_SWITCH requiere el AgentState y el ExecutionContext reales del AgentRun objetivo — ninguno de los dos se infiere",
                recoverable = FALSE,
                retryable = FALSE,
                metadata = {}
            )
            THROW missing
        END

        IF targetState.status == COMPLETED
            OR targetState.status == FAILED
            OR targetState.status == CANCELLED
            OR targetState.status == EXPIRED

            terminal: HarnessError = HarnessError(
                category = CONTROL,
                code = "KILL_SWITCH_ON_TERMINAL_AGENT_STATE",
                message = "El AgentRun objetivo ya alcanzó un AgentRunStatus terminal por otra vía; un kill switch nunca reescribe un estado terminal ya alcanzado",
                recoverable = FALSE,
                retryable = FALSE,
                metadata = {}
            )
            THROW terminal
        END

        updatedState = AgentState(
            runId = targetState.runId,
            sessionId = targetState.sessionId,
            agentId = targetState.agentId,
            status = CANCELLED,
            currentTurn = targetState.currentTurn
        )

        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = CONTROL_DIRECTIVE_APPLIED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = targetState.agentId,
            traceId = execution.traceId,
            payload = directive
        )
    END

    completedDirective: ControlDirective = ControlDirective(
        id = directive.id,
        type = directive.type,
        targetRef = directive.targetRef,
        issuedBy = directive.issuedBy,
        status = APPLIED,
        issuedAt = directive.issuedAt,
        appliedAt = now()
    )

    RETURN ControlDirectiveApplication(
        directive = completedDirective,
        updatedAgentState = updatedState
    )
END
```

`now()`, `newEventId()` y `newControlDirectiveId()` son las mismas primitivas de CH-00/CH-14/CH-15/
CH-16/CH-17. `targetState` y `execution` son señales de entrada — igual que `existingRecordForKey`
en CH-17 §11 o `capabilityResolved` en CH-02 §11 — que un mecanismo real de resolución (Preview,
fuera de este registry) produciría en la práctica: `applyControlDirective` no busca, por sí misma,
el `AgentState` del run objetivo — lo recibe ya resuelto, y decide, determinísticamente, qué
`ControlDirectiveApplication` o qué `HarnessError` construir a partir de él.

**Por qué `issueControlDirective` nunca emite ningún `AgentEvent`, ni siquiera para `KILL_SWITCH`.**
En el instante en que se emite un `ControlDirective`, `targetRef` es solo una referencia opaca —
incluso para `KILL_SWITCH`, todavía no existe ningún `ExecutionContext` resuelto del run objetivo
(ese contexto solo llega como parámetro de `applyControlDirective`). Emitir un `AgentEvent` sin un
`runId`/`sessionId`/`traceId` genuinos habría significado fabricar esos campos o dejarlos vacíos —
la misma decisión que ya tomaron `AdmissionController` (CH-14) y `AgentCommunicationGateway`
(CH-15) frente al mismo problema (ver seccion 14 para el desarrollo completo).

**Por qué `applyControlDirective` verifica `directive.status == APPLIED` ANTES de mirar el `type`.**
El write-once de un `ControlDirective` ya aplicado es una propiedad de CUALQUIER tipo de comando,
no solo de `KILL_SWITCH` — comprobarlo primero, en un único punto, evita que la lógica específica de
cada tipo tenga que repetir la misma verificación cuatro veces (el mismo orden que ya usó
`IdempotencyGuard.recordIdempotentExecution`, CH-17 §11, al comprobar `existingRecordForKey.status
== COMPLETED` antes de cualquier otra cosa).

**Por qué `applyControlDirective` rechaza un `KILL_SWITCH` sobre un `AgentState` ya terminal — la
regla explícita que resuelve el "empate" con `ExecutionController`.** `AgentRunStatus` es, desde
Article V, terminal-una-vez: ningún capítulo de este libro permite transicionar fuera de
`COMPLETED`/`FAILED`/`CANCELLED`/`EXPIRED` una vez alcanzados. Si `OperationalController` emite un
kill switch sobre un run que, por cualquier otra vía, ya llegó a un estado terminal —incluyendo, en
un futuro capítulo de integración, una vía cableada desde `ExecutionController` hacia `FAILED` o
`CANCELLED` por presupuesto agotado— `applyControlDirective` lo rechaza explícitamente
(`KILL_SWITCH_ON_TERMINAL_AGENT_STATE`) en vez de intentar sobrescribir silenciosamente un estado ya
fijado. La regla, sin ambigüedad, es: **quien escribe primero sobre un `AgentState` todavía no
terminal, gana** — y, hasta este capítulo, `OperationalController` es la ÚNICA de las dos vías que
este libro ha cableado realmente hasta `AgentState.status` (`ExecutionController`, CH-07 §18, sigue
dejando esa escritura como Preview) — de modo que, en la práctica, un kill switch siempre gana hoy,
no porque este capítulo le otorgue una prioridad abstracta sobre `ExecutionController`, sino porque
es, literalmente, el primero en llegar (ver seccion 15 para el desarrollo completo).

Nótese también lo que `applyControlDirective` **nunca hace**: no invoca
`ExecutionController.evaluateExecutionContinuation` (CH-07) para decidir si el kill switch procede
— la decisión de forzarlo ya se tomó, desde afuera, en el momento de emitir el `ControlDirective`;
no invoca ningún turno de `AgentLoop.runTurn` (CH-01) — la transición hacia `CANCELLED` ocurre
directamente, sin esperar ningún ciclo cooperativo; y no invoca `CapabilityRegistry.resolveToolCall`
(CH-08) ni `PolicyEngine.evaluatePolicyForToolCall` (CH-05) — ninguna de las dos preguntas que
ambos resuelven es relevante para decidir si un comando operacional ya emitido debe aplicarse.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no modifica `AgentRunStatus` (C-013): sigue siendo, sin cambios, el mismo `ENUM` de
once estados que `AgentLoop` (CH-01) formalizó. `ControlDirective`, igual que `IdempotencyRecord`
(CH-17 §12) y a diferencia de `CredentialReference` (CH-16 §12) o `DelegationGrant` (CH-15 §12),
introduce su propio `ENUM` de estado (`ControlDirectiveStatus`), porque "emitido pero todavía sin
efecto" no es una condición que se derive de comparar fechas — es una escritura explícita
(`applyControlDirective`) la que la resuelve.

```text
(ControlDirective recién emitido)
   → issueControlDirective(...)
     RETURN ControlDirective(status = ISSUED) — el comando existe, pero todavía no tiene efecto
     garantizado sobre nada

(applyControlDirective, con directive.status == ISSUED)
   → produce/completa un ControlDirective con status = APPLIED — transición terminal, el único
     destino real que este capítulo formaliza con pseudocódigo

(applyControlDirective, con directive.status ya APPLIED)
   → lanza HarnessError (CONTROL_DIRECTIVE_ALREADY_APPLIED) — write-once, nunca sobrescribe

(directive.type == KILL_SWITCH, targetState.status == RUNNING o cualquier valor no terminal)
   → applyControlDirective construye un AgentState nuevo con status = CANCELLED — la PRIMERA
     transición real y ejecutable de este libro hacia AgentRunStatus.CANCELLED (CH-07 §12 solo la
     había descrito en prosa); ocurre SIN invocar evaluateExecutionContinuation (CH-07) ni ningún
     turno de AgentLoop (CH-01) — exactamente la independencia que INV-E14 exige

(directive.type == KILL_SWITCH, targetState.status ya terminal — COMPLETED/FAILED/CANCELLED/
 EXPIRED)
   → applyControlDirective lanza HarnessError (KILL_SWITCH_ON_TERMINAL_AGENT_STATE) — fail-closed;
     la regla explícita del "empate" con ExecutionController: quien llega primero a un
     AgentRunStatus terminal, gana, y este capítulo nunca reescribe uno ya fijado

(directive.type != KILL_SWITCH — DISABLE_CAPABILITY / ISOLATE_TENANT / ROLLBACK)
   → applyControlDirective completa el ControlDirective (status = APPLIED) sin construir ningún
     AgentState nuevo — el alcance de estos tres tipos nunca es un único run (ver seccion 18 para
     el mecanismo real de enforcement, todavía Preview)
```

**Sobre la propiedad de `AgentRunStatus` (matiz explícito, no una contradicción).** CH-07 §12
declaró que la máquina de estados de `AgentRunStatus` "sigue siendo propiedad exclusiva de
`AgentLoop`" — una afirmación correcta en el momento en que se escribió: hasta CH-17, ningún otro
componente podía, ni pretendía, producir ninguna transición real. Este capítulo no contradice esa
afirmación para el camino COOPERATIVO del lifecycle (`CREATED` → `INITIALIZING` → `RUNNING` → ... →
`COMPLETED`), que sigue siendo, sin excepción, exclusivo de `AgentLoop`. Lo que este capítulo
formaliza, por primera vez con código real, es la única excepción que la propia Constitution exige
por nombre (`INV-E14`): una segunda vía, no cooperativa, hacia `CANCELLED`, disparada
exclusivamente por un `ControlDirective` de tipo `KILL_SWITCH` — nunca una reclamación general de
`OperationalController` sobre el resto del lifecycle.

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6, extendido en la seccion 6 de este capítulo) clasifica también
los cuatro fallos reales que introduce este capítulo:

```text
CONTROL
    CONTROL_DIRECTIVE_MISSING_TARGET_REF     — issueControlDirective fue invocada sin una
                                                referencia de alcance (targetRef)
        → recoverable: FALSE, retryable: FALSE
    CONTROL_DIRECTIVE_ALREADY_APPLIED        — applyControlDirective nunca reaplica un
                                                ControlDirective ya APPLIED
        → recoverable: FALSE, retryable: FALSE
    KILL_SWITCH_MISSING_TARGET_CONTEXT       — un ControlDirective de tipo KILL_SWITCH requiere
                                                el AgentState y el ExecutionContext reales del
                                                AgentRun objetivo
        → recoverable: FALSE, retryable: FALSE
    KILL_SWITCH_ON_TERMINAL_AGENT_STATE      — el AgentRun objetivo ya alcanzó un AgentRunStatus
                                                terminal por otra vía; el "empate" con
                                                ExecutionController se resuelve fail-closed aquí
        → recoverable: FALSE, retryable: FALSE
```

Los cuatro fallos son `recoverable = FALSE` y `retryable = FALSE`: los cuatro representan un uso
incorrecto del propio `ControlDirective` (una referencia de alcance faltante, un intento de
reaplicar un comando ya terminal, un kill switch sin contexto real, o un kill switch tardío contra
un run que ya terminó) — ninguno se corrige reintentando la misma operación tal cual.

**La distinción más importante de esta sección**: ninguno de los cuatro fallos se clasifica como
`category = CANCELLATION` — aunque `KILL_SWITCH_ON_TERMINAL_AGENT_STATE` podría, a primera vista,
parecer relacionado con la cancelación que `ExecutionController` (CH-07) ya clasifica bajo
`CANCELLATION`. `CANCELLATION` (CH-07) pertenece, en exclusiva, a la cancelación de UN run evaluada
desde DENTRO de su propio ciclo, contra una señal (`cancellationRequested`) que `AgentLoop`
recibiría antes de decidir si otro turno ocurre. `CONTROL` (este capítulo) pertenece, en exclusiva,
a un comando operacional emitido desde AFUERA de cualquier ciclo — reutilizar `CANCELLATION` aquí
habría conflacionado dos decisiones de dos componentes distintos, exactamente el error que Article
IV (Ownership Rule) prohíbe — el mismo argumento que ya usaron CH-15 §13 (para no reutilizar
`BUDGET`), CH-16 §13 (para no reutilizar `VALIDATION`) y CH-17 §13 (para no reutilizar `VALIDATION`
ni `BUDGET`).

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo de `category =
INFRASTRUCTURE` que pudiera ocurrir en el mecanismo real y distribuido que efectivamente aísla un
tenant o impide invocar una capability deshabilitada — ese valor de `ErrorCategory` sigue, después
de este capítulo, sin que ningún componente real lo haya ejercitado nunca (mismo límite que
CH-11 §13/CH-14 §13/CH-15 §13/CH-16 §13/CH-17 §13 ya documentaron para sus propias primitivas
asumidas).

## 14. Eventos Producidos (Events Produced)

`OperationalController` es el primer componente de este libro que emite `AgentEvent` de forma
**condicional al tipo de comando que procesa** — ni siempre (como `IdempotencyGuard`/
`CapabilityRegistry`/`CredentialBroker`), ni nunca (como `AdmissionController`/
`AgentCommunicationGateway`): agrega `CONTROL_DIRECTIVE_APPLIED` a `AgentEventType` (seccion 6), y
solo la rama `KILL_SWITCH` exitosa de `applyControlDirective` (seccion 11) lo emite.

**Por qué solo `KILL_SWITCH` emite, y `DISABLE_CAPABILITY`/`ISOLATE_TENANT`/`ROLLBACK` no.** Un
`AgentEvent` (C-010) exige `runId`/`sessionId`/`agentId`/`traceId` genuinos — campos que solo tienen
sentido cuando el alcance de la decisión es, precisamente, UN `AgentRun` concreto. Cuando
`OperationalController` aplica un `KILL_SWITCH`, el run objetivo ya existe con un `ExecutionContext`
completo — la misma situación que `CapabilityRegistry` (CH-08) y `CredentialBroker` (CH-16) ya
establecieron para sus propios capítulos. Cuando aplica `DISABLE_CAPABILITY`, `ISOLATE_TENANT` o
`ROLLBACK`, en cambio, el alcance es potencialmente TODOS los runs de una capability o de un tenant
— no existe ningún `runId`/`sessionId`/`traceId` único que represente honestamente ese alcance sin
fabricar valores o elegir arbitrariamente un run entre muchos. Ante esa disyuntiva,
`OperationalController` elige, para esos tres tipos, no emitir ningún evento — la misma decisión que
ya tomaron `AdmissionController` (CH-14) y `AgentCommunicationGateway` (CH-15) frente al mismo
problema estructural, aunque por una razón inversa (ellos, porque el run TODAVÍA no existe; este
componente, porque el alcance es MÁS GRANDE que un solo run).

**Por qué esto es una limitación real hacia `INV-18`, honestamente señalada y no resuelta.** `INV-18`
exige que "toda acción significativa produzca un evento observable" — deshabilitar una capability
completa o aislar un tenant son, sin duda, acciones significativas. Este capítulo no resuelve cómo
observar esas dos acciones con el mismo mecanismo (`AgentEvent`/`EventBus`, Article X) que el resto
del libro usa para runs individuales; documenta la limitación explícitamente en vez de forzar un
`AgentEvent` con campos fabricados (ver seccion 18).

**Lo que este capítulo no resuelve (relación con `P-25`).** Una auditoría completa de "quién emitió
cada `ControlDirective`, cuándo, y sobre qué alcance" necesitaría, per `P-25` ("Audit evidence is
distinct from operational telemetry"), algo más que `AgentEvent`/`EventBus` — un mecanismo de
evidencia inmutable, distinto de la telemetría operacional que este capítulo produce solo
parcialmente. Ese mecanismo no se construye aquí (mismo límite, honestamente señalado, que
CH-14 §14/CH-15 §14/CH-16 §14/CH-17 §14 ya documentaron cada uno para su propio contrato).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

`OperationalController` es el primer componente de este libro cuya responsabilidad completa es
actuar DESDE AFUERA del ciclo de una ejecución, sin depender de su cooperación.

**La distinción con `ExecutionController` (CH-07), explícita, completa y la más importante de este
capítulo.** `ExecutionController.evaluateExecutionContinuation` (CH-07) decide si UN `AgentRun`
puede seguir *operacionalmente* contra SU `ExecutionBudget` — una evaluación que ocurre, por
diseño, DENTRO del ciclo de vida de ese mismo run, y que depende de que algo (típicamente
`AgentLoop.runTurn`, aunque ese cableado sigue siendo Preview) la invoque en el momento correcto.
`OperationalController.applyControlDirective` (este capítulo) decide si el control operacional debe
forzar, DESDE AFUERA, la terminación de un run — o deshabilitar/aislar/revertir algo a una escala
mayor que un run — sin depender de que nada dentro de ese ciclo coopere, y sin invocar jamás
`evaluateExecutionContinuation`. Las dos preguntas son, literalmente, ortogonales: un run puede
tener presupuesto de sobra y, aun así, ser terminado por un kill switch (un incidente de seguridad,
una decisión humana, un comportamiento peligroso detectado por un sistema de gobierno externo); y,
a la inversa, un run puede agotar su presupuesto sin que ningún operador humano haya intervenido
nunca. `P-30` exige, en una sola frase, cinco capacidades — "cancellation, capability disablement,
tenant isolation, rollout rollback and kill switches" — y este capítulo resuelve las cuatro que
`ExecutionController` no podía resolver sin invadir un dominio ajeno, dejando la quinta
("cancellation" evaluada desde dentro del propio ciclo de un run) exactamente donde Article III ya
la había asignado desde CH-07.

**El caso límite del "empate": cuando ambos podrían terminar el mismo run.** Si
`OperationalController` emite un kill switch sobre un `AgentRun` que `ExecutionController` también
podría haber detenido, por su propio camino, por presupuesto agotado — ¿quién gana? Este capítulo
resuelve la pregunta con una regla explícita, no con una ambigüedad tolerada: **`AgentRunStatus` es
terminal-una-vez** (Article V — ningún capítulo de este libro permite transicionar fuera de un
estado terminal ya alcanzado), de modo que la regla real es **"quien escribe primero sobre un
`AgentState` todavía no terminal, gana"** — y `applyControlDirective` (seccion 11) hace cumplir esa
regla explícitamente: rechaza (`KILL_SWITCH_ON_TERMINAL_AGENT_STATE`) forzar un kill switch sobre un
run que ya alcanzó un estado terminal por cualquier otra vía, en vez de sobrescribirlo
silenciosamente. Hoy, en la práctica, a través de los dieciocho capítulos reales de este libro, el
kill switch SIEMPRE gana ese hipotético empate — no porque este capítulo le otorgue una prioridad
abstracta sobre `ExecutionController`, sino porque `OperationalController` es, literalmente, la
única de las dos vías que este libro ha cableado hasta escribir `AgentState.status` de verdad:
`ExecutionController` (CH-07 §18) sigue dejando esa escritura como Preview, pendiente de que un
capítulo de integración futuro la cablee dentro de `AgentLoop.runTurn`. El día en que ese cableado
exista, la misma regla ("terminal-una-vez", "primero en escribir, gana") seguirá resolviendo
cualquier competencia real entre ambos caminos sin necesitar ninguna prioridad especial adicional —
`P-30` ("operational control can override autonomy") se cumple no porque `OperationalController`
tenga, en abstracto, más autoridad que `ExecutionController`, sino porque nunca necesita esperar su
turno cooperativo para llegar primero.

**La distinción con `PolicyEngine` (CH-05) y `CapabilityRegistry` (CH-08), heredada de capítulos
anteriores.** `PolicyEngine.evaluatePolicyForToolCall` (CH-05) decide si una acción ya resuelta
puede ejecutarse — una pregunta que se responde sin necesitar saber jamás si el control operacional
decidió, desde afuera, deshabilitar toda una capability. `CapabilityRegistry.resolveToolCall`
(CH-08) decide qué implementación satisface una capability solicitada — tampoco necesita saber, hoy,
si esa capability está operacionalmente deshabilitada (ese cableado es, explícitamente, Preview, ver
seccion 9/18). `OperationalController` asume ambas resoluciones como fuera de su alcance: nunca
autoriza una acción, nunca resuelve una implementación — se ocupa exclusivamente de si el control
operacional debe intervenir desde afuera. La misma disciplina de límites que CH-14 §15/CH-15 §15/
CH-16 §15/CH-17 §15 ya aplicaron frente a sus propios vecinos.

**`P-13`, aplicado con la misma disciplina que todo el libro.** `issueControlDirective`/
`applyControlDirective` no reciben ninguna entrada que el modelo haya producido — ni siquiera de
forma indirecta. El modelo no puede emitir un `ControlDirective` (`issuedBy: ActorId` nunca
representa al modelo), no puede evitar que uno se aplique, y ni siquiera necesita ser consciente de
que uno existe: `P-30` exige, literalmente, que el control operacional funcione "without relying on
model cooperation" — la ausencia total del modelo en el pseudocódigo de este capítulo es la
materialización directa de esa frase.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST IssueControlDirectiveRejectsAnEmptyTargetRef
TEST IssueControlDirectiveNeverEmitsAnAgentEventRegardlessOfType
TEST ApplyControlDirectiveRejectsReapplyingAnAlreadyAppliedDirective
TEST ApplyControlDirectiveRejectsAKillSwitchMissingTargetStateOrExecutionContext
TEST ApplyControlDirectiveRejectsAKillSwitchOnAnAlreadyTerminalAgentState
TEST ApplyControlDirectiveForcesCancelledWithoutInvokingEvaluateExecutionContinuation
TEST ApplyControlDirectiveNeverInvokesAnyAgentLoopTurnForAKillSwitch
TEST ApplyControlDirectiveEmitsAnAgentEventOnlyForASuccessfulKillSwitch
TEST ApplyControlDirectiveNeverProducesAnUpdatedAgentStateForNonKillSwitchTypes
TEST OperationalControllerNeverEvaluatesExecutionBudgetOrToolCallAuthorization
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (después de CH-18 — quinto plano de Amendment v1.1 cubierto por este libro, y primer
componente distinto de AgentLoop que produce, con pseudocódigo real, una transición de
AgentRunStatus)

Constitution
 ├── Article IV     — Decision Ownership (tabla original sin cambios; OperationalController
 │                     documentado en prosa, igual que AdmissionController/
 │                     AgentCommunicationGateway/CredentialBroker/IdempotencyGuard)
 ├── Article V      — Lifecycle (AgentRunStatus sin cambios de forma; CANCELLED alcanzado, por
 │                     primera vez, con código real y por una vía no cooperativa)
 └── Amendment v1.1 — Enterprise Activation, Interoperability and Operations
                       (P-30/INV-E14 citados por primera vez con código real; Ingress &
                       Activation Plane, CH-14, Agent Interoperability Plane, CH-15, Capability &
                       Integration Plane, CH-16, Reliability Plane, CH-17, y Control Plane, este
                       capítulo, los cinco primeros de nueve planos canónicos instalados)

Contracts (registry/contracts.yaml)
 ├── C-001..C-027  (sin cambios — CH-00..CH-17)
 └── C-028 ControlDirective  (CH-18, nuevo — el comando operacional emitido para deshabilitar una
                              capability, aislar un tenant, revertir un rollout o forzar un kill
                              switch, P-30/INV-E14)

Components (registry/components.yaml)
 ├── CMP-001..CMP-015  (sin cambios — CH-01..CH-17)
 └── CMP-016 OperationalController  (CH-18, nuevo — quinto componente de este registry que no
                                     corresponde a ninguno de los once nombres de Article III;
                                     pertenece al Control Plane de Amendment v1.1, y es el primero
                                     cuyo pseudocódigo escribe, de verdad, una transición de
                                     AgentRunStatus sin invocar AgentLoop)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado real `CapabilityRegistry ↔ OperationalController`**: `resolveToolCall` (CH-08) no
  consulta todavía si una capability tiene un `ControlDirective` `APPLIED` de tipo
  `DISABLE_CAPABILITY` antes de resolverla — el propio encargo de este capítulo señala,
  explícitamente, que ese cableado es trabajo de un capítulo de integración futuro.
- **El mecanismo real y distribuido de aislamiento de tenant**: este capítulo produce un
  `ControlDirective` `APPLIED` de tipo `ISOLATE_TENANT`, pero ningún pseudocódigo de este libro
  bloquea, todavía, ninguna `ActivationRequest` ni ningún `AgentRun` en curso de ese tenant — la
  propagación real hacia `AdmissionController` (CH-14) es Preview.
- **El mecanismo real de rollback de un rollout**: este capítulo reusa `CapabilityDescriptor.
  version` (C-018) como el identificador de la versión objetivo, pero no modela cómo
  `CapabilityRegistry` pasaría a resolver, de hecho, la versión anterior en vez de la más reciente.
- **La generación real de un `targetRef`**: quién decide qué capability/tenant/rollout/run es el
  objetivo correcto de un `ControlDirective` — asumida, no modelada (mismo límite que CH-16 §18
  documentó para la emisión de un secreto, y CH-17 §18 para la generación de una idempotencyKey).
- **Quién está autorizado a emitir un `ControlDirective`**: `issueControlDirective` recibe
  `issuedBy: ActorId` ya resuelto, pero este capítulo no decide si ese actor tiene, de hecho,
  autoridad para deshabilitar una capability o aislar un tenant — esa pregunta ("¿está permitido
  que ESTE actor emita ESTE comando?") suena, deliberadamente, a `PolicyEngine` (CH-05), pero
  cablear esa verificación real queda, honestamente, fuera de alcance de este capítulo.
- **La observabilidad completa de `DISABLE_CAPABILITY`/`ISOLATE_TENANT`/`ROLLBACK`** (seccion 14):
  ningún `AgentEvent` real los representa todavía — una limitación señalada explícitamente, no
  silenciada.
- **Ausencia de evidencia de auditoría real** (`P-25`) para un `ControlDirective` producido:
  señalado explícitamente (seccion 14), no silenciado.
- **Los cuatro planos restantes de Amendment v1.1** (Execution Plane, Data & Context Plane,
  Observability & Governance Plane, Execution Fabric) y **la profundización del Control Plane más
  allá de este primer componente**: explícitamente fuera de alcance.
- Reviewers plurales, evals y orquestación multi-agente propiamente dicha: explícitamente fuera de
  alcance de BH-v0.1.

## 19. Siguiente Incremento (Next Increment)

Con este capítulo, el "Control Plane" de Amendment v1.1 tiene su primer componente real — pero el
plano completo (el cableado real hacia `CapabilityRegistry`, el mecanismo real de aislamiento
distribuido de tenant, el mecanismo real de rollback de un rollout, la autorización real de quién
puede emitir un `ControlDirective`) sigue sin construirse de punta a punta. El problema natural del
próximo incremento es, o bien profundizar este mismo plano (cableando por fin `OperationalController`
dentro de `CapabilityRegistry.resolveToolCall` y de `AdmissionController.evaluateAdmission`, el
mismo patrón de integración que CH-12/CH-13 ya establecieron para el camino feliz y los caminos de
gobierno de un `AgentRun`), o bien avanzar hacia cualquiera de los cuatro planos restantes que
Amendment v1.1 enumera junto a este — el Execution Plane (segundo plano canónico, todavía sin
cubrir por ningún capítulo de este libro) o el Observability & Governance Plane (que por fin
resolvería la deuda de `P-25`, señalada sin resolver desde CH-09 y repetida en cada capítulo de
Amendment v1.1 desde entonces) son, ambos, candidatos particularmente naturales.

`next_chapter` queda en `null` en el frontmatter de este capítulo porque, en este momento del libro,
ese próximo capítulo todavía no existe como archivo — solo como el problema que motivaría su
escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg / Bucles
> de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows),
> secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): dieciocho capítulos reales construyeron un runtime
   completo más cuatro componentes de Enterprise, pero ninguno de ellos puede, hoy, detener una
   ejecución, deshabilitar una capability o aislar un tenant sin que algo dentro de esa misma
   ejecución tenga que cooperar primero.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): `P-30`/`INV-E14`
   fueron adoptados desde CH-14, nunca citados en prosa ni resueltos hasta este capítulo; el
   "Control Plane" seguía siendo el único de los cuatro planos ya iniciados sin ningún componente
   propio.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `OperationalController` con una ficha que declara tanto lo que posee (`owns`: kill switch,
   deshabilitación de capability, aislamiento de tenant, rollback de rollout) como lo que
   explícitamente NO posee (cancelar UN run desde dentro de su propio ciclo por presupuesto,
   autorización, resolución de implementación, ejecución del side effect).
4. **Modelos mentales** (= §4, Constitutional Impact): "¿puede este run seguir contra SU
   presupuesto, evaluado desde dentro de su propio ciclo?" es una pregunta completamente distinta
   de "¿debe el control operacional forzar, desde afuera, la terminación de este run — o algo más
   grande que un run?" — dos preguntas que comparten, a veces, el mismo destino posible pero nunca
   el mismo dueño.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un sistema deja el control operacional dependiendo
  de la cooperación de lo que se quiere controlar, un incidente real se vuelve indetenible
  exactamente cuando más urge detenerlo — el mismo bucle de "la ausencia de un dueño se vuelve una
  dependencia implícita" ya combatido por `P-02`/`P-19`/`INV-E08`/`INV-11`, ahora aplicado al
  control mismo.
- **Bucle de equilibrio (estabiliza):** `issueControlDirective`/`recordIdempotentExecution`... —
  `issueControlDirective`/`applyControlDirective` (§11) rechazan, con un `HarnessError`
  categorizado, tanto reaplicar un comando ya terminal como forzar un kill switch sobre un run que
  ya llegó a un estado terminal por otra vía — el mismo mecanismo que garantiza que "quien escribe
  primero, gana" nunca se convierta en "quien escribe último, sobrescribe".

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `applyControlDirective`, para el caso
`KILL_SWITCH`, escriba directamente un `AgentState` nuevo con `status = CANCELLED` — sin esperar a
que un capítulo de integración futuro cablee esa transición dentro de `AgentLoop.runTurn`, como sí
quedó pendiente para `ExecutionController` (CH-07). Si esta transición hubiera quedado, también
aquí, diferida a un cableado cooperativo futuro, un kill switch dependería de la misma cooperación
que `INV-E14` exige, por nombre, que nunca necesite.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo de
> esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set` (frontmatter) y
> es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa, para lectura directa
> del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Si un operador humano —o un sistema de gobierno automatizado— necesita detener de inmediato una
   ejecución que se está comportando mal, sin depender de que esa ejecución coopere, ¿qué
   necesitaría existir para que esa detención ocurra de todos modos? *(cierra la pregunta guía 1)*
2. ¿Esa misma pregunta que ya resuelve si un run puede seguir contra su presupuesto sirve también
   para deshabilitar una capability entera o aislar un tenant completo? *(cierra la pregunta guía
   2)*
3. ¿Qué forma necesitaría tener el comando que representa una decisión operacional externa, de modo
   que se sepa quién lo emitió y si ya tuvo efecto? *(cierra la pregunta guía 3)*
4. Si dos mecanismos distintos pudieran, en teoría, terminar la misma ejecución casi al mismo
   tiempo, ¿qué debería pasar? *(cierra la pregunta guía 4)*

### Explicar

1. `OperationalController` posee forzar la terminación inmediata de un `AgentRun` mediante un kill
   switch. Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee decidir si
   ESE MISMO run puede seguir contra su presupuesto operacional.
2. El estado de un comando operacional nunca se modela con un `Boolean` "ya se aplicó / no se ha
   aplicado". Explica qué perderíamos, y qué riesgo introduciríamos, si colapsáramos ambos casos en
   un solo valor.

### Conectar

1. `ExecutionController` (CH-07) nunca escribió, con código real, una transición hacia
   `AgentRunStatus.CANCELLED`. Si este capítulo necesita forzar esa transición sin esperar a que
   exista ese cableado, ¿debería reutilizar `evaluateExecutionContinuation`, o construir un camino
   independiente?
2. `CapabilityRegistry` (CH-08) resuelve qué implementación satisface una capability, pero nunca
   verifica si esa capability está deshabilitada. ¿A quién le pertenece esa verificación, aunque su
   mecanismo real quede para un capítulo posterior?

### Espaciar

Las cinco tarjetas de repaso de este capítulo (dos sobre `OperationalController` — su `owns` y su
`does_not_own` —, dos sobre `ControlDirective` — sus campos y por qué ni `type` ni `status` se
colapsan a formas más simples —, y una sobre la regla del "empate" con `ExecutionController`) entran
hoy en `reviewStage = DAY_1`. Repásalas de nuevo al día 3, al día 7 y al día 21 (curva de
Ebbinghaus) — ver el apéndice de tarjetas al final del libro (edición PDF) o
`retrieval_set.flashcards` en `dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te equivocaste,
ese es precisamente el punto ciego que este método existe para revelar.
