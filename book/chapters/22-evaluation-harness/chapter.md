---
id: CH-22
title: "EvaluationHarness y la Certificación de un Candidato Antes de que Exista Ningún Run"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-020]
introduces_contracts: [C-032, C-033]
modifies_contracts: []
constitutional_articles: [P-13, P-28, P-29, INV-E13, INV-18, INV-19, INV-20]
previous_chapter: CH-21
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH22
    text: |
      Al terminar este capítulo podrás distinguir, con precisión, dos preguntas que ambas se llaman
      "evaluación" pero pertenecen a dominios completamente distintos: si una acción concreta puede
      ejecutarse DENTRO de un run que ya existe, y si un candidato completo — un agente, un prompt,
      una skill, un modelo, una policy o una capability — debería promoverse a producción ANTES de
      que exista un solo run que lo use. Podrás diseñar un resultado de certificación de tres
      estados que nunca se reduce a un simple aprobado/rechazado, distinguir por qué una propiedad
      binaria de una policy de certificación puede modelarse como Boolean mientras el resultado de
      la propia decisión nunca puede, y argumentar por qué el éxito técnico de un run —cada tool
      call exitosa, cada turno dentro de presupuesto— nunca implica, por sí solo, que ese run haya
      producido algún valor de negocio medible.
  skeleton:
    id: SK-CH22
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
    components_to_be_introduced: [CMP-020]
    contracts_to_be_introduced: [C-032, C-033]
  guiding_questions:
    - id: GQ-CH22-01
      text: |
        Ya existe un componente que evalúa, en tiempo real, si una acción concreta dentro de un run
        que ya existe puede ejecutarse — con un resultado determinístico y trazable. Si ahora
        necesitamos decidir si un agente, un prompt, una skill, un modelo o una policy completos
        deberían siquiera promoverse a producción, antes de que exista un solo run que los use, ¿es
        esa la misma pregunta de evaluación formulada sobre un objeto distinto, o dos preguntas de
        dominios completamente distintos que conviene no confundir aunque ambas se llamen "evaluar"?
      answered_by: RQ-CH22-01
    - id: GQ-CH22-02
      text: |
        Ya existe un contrato que registra, para cada capability disponible en el sistema, una
        versión explícita. Si una nueva versión de una capability ya registrada es, con frecuencia,
        exactamente el tipo de candidato que una organización necesitaría evaluar antes de
        promoverlo a producción, ¿le corresponde a quien registra esa versión decidir también si
        debe certificarse, o son responsabilidades que pertenecen a dueños completamente distintos?
      answered_by: RQ-CH22-02
    - id: GQ-CH22-03
      text: |
        Si la clase de riesgo de un candidato determina si necesita, o no, una política de
        certificación antes de producción, ¿el resultado de esa certificación debería reducirse
        siempre a dos estados posibles — aprobado o rechazado — o existe un tercer estado legítimo
        en el que la decisión, deliberadamente, no puede tomarse todavía sin que intervenga un
        humano?
      answered_by: RQ-CH22-03
    - id: GQ-CH22-04
      text: |
        Un run puede terminar sin ningún error técnico — cada tool call exitosa, cada turno completado
        dentro de su presupuesto, ninguna policy denegada. ¿Ese éxito técnico garantiza, por sí solo,
        que ese run produjo algún valor de negocio medible, o son dos juicios completamente distintos
        que conviene poder correlacionar sin confundir jamás uno con el otro?
      answered_by: RQ-CH22-04
  systems_lens:
    iceberg_visible_fact: |
      Veintidós capítulos reales, y tres reglas completas de la Constitution — `P-28`, `P-29` e
      `INV-E13` — nunca fueron citadas con código real por ningún capítulo anterior, ni siquiera en
      prosa: a diferencia de `P-27` (CH-21), que al menos aparecía nombrado como uno de los nueve
      "Canonical Enterprise Planes", estas tres reglas no pertenecen a ninguno de los nueve planos
      que CH-21 declaró completamente cubiertos — quedaron, literalmente, fuera de esa taxonomía
      (ver seccion 2, El Problema).
    iceberg_patterns: |
      El patrón que ya se repitió ocho veces desde `AdmissionController` (CH-14) —una regla
      constitucional completa reducida, durante varios capítulos, a texto transcrito sin código—
      aquí aparece con una variante más sutil: CH-21 cerró, con razón, los nueve planos canónicos de
      Amendment v1.1, y ese cierre pudo leerse, por error, como "la Constitution ya está cubierta".
      Pero un plano y un principio no son la misma unidad de cobertura — completar los nueve planos
      no completó las treinta reglas de la enmienda (ver seccion 3, Por Qué la Arquitectura Actual No
      Basta).
    iceberg_structures: |
      Este capítulo instala `EvaluationHarness` (`CMP-020`), el noveno componente de este libro que
      no corresponde a ninguno de los once nombres de Article III — con una ficha que declara tanto
      lo que posee (`owns`: evaluar un candidato completo antes de su promoción a producción,
      aplicar la certificación que su clase de riesgo exige, correlacionar un run con un outcome de
      negocio medible) como lo que explícitamente NO posee (`does_not_own`: evaluar una acción
      DENTRO de un run ya en marcha — `PolicyEngine`, CH-05, la frontera más importante de este
      capítulo) (ver seccion 8, Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es que "evaluar" no es una sola pregunta: es,
      como mínimo, dos preguntas con objetos, momentos y dueños distintos — si ESTA ACCIÓN puede
      ocurrir AHORA, dentro de un run que ya existe (`PolicyEngine`), y si ESTE CANDIDATO debería
      promoverse a producción, ANTES de que exista un solo run que lo use (`EvaluationHarness`). Y
      una tercera idea, ortogonal a la anterior: que el éxito técnico de un run —ninguna policy
      denegada, ningún presupuesto agotado— nunca implica, por sí solo, éxito de negocio (ver
      seccion 4, Impacto Constitucional).
    reinforcing_loop: |
      Cada vez que un componente nuevo resuelve una pregunta que "suena" a evaluación —autorizar una
      acción (CH-05), clasificar un dato (CH-20)— crece la tentación de asumir que "evaluar un
      candidato antes de producción" ya quedó cubierto por alguno de esos dos, hasta que una
      organización necesita, de verdad, decidir si una versión nueva de una capability, un prompt o
      un modelo debería certificarse — y ningún componente existente responde, siquiera
      parcialmente, esa pregunta sobre un objeto que todavía no tiene ningún run.
    balancing_loop: |
      `evaluateCandidateForPromotion` (seccion 11) es el mecanismo de equilibrio: nunca colapsa su
      resultado a dos estados cuando la certificación exigida no puede resolverse todavía —
      produce, en cambio, `NEEDS_REVIEW`, el mismo principio de "no fabricar una respuesta binaria
      donde la Constitution exige un tercer estado" que `HumanInteractionService` (CH-06) ya aplicó
      a `REQUIRE_APPROVAL`, en vez de permitir que una certificación incierta se apruebe o se
      rechace por omisión.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `EvaluationReport` (`C-032`) y
      `BusinessOutcomeCorrelation` (`C-033`) sean contratos completamente autónomos de
      `AgentLoop.runTurn` (CH-01) y de `PolicyEngine.evaluatePolicyForToolCall` (CH-05) — ningún run
      necesita que exista un `EvaluationReport` para su agente, su prompt o su modelo antes de
      ejecutarse, y ningún run necesita que exista un `BusinessOutcomeCorrelation` para completarse.
      Si en cambio la certificación de un candidato se hubiera modelado como una precondición dentro
      de `AgentLoop.runTurn`, cada capítulo futuro que tocara esa función habría cargado, para
      siempre, una responsabilidad ajena a la suya. Mantener ambos contratos independientes,
      referenciados por `subjectRef`/`runId`, es la forma en que este capítulo hace real la
      separación de `P-28` ("Production and evaluation are separate execution concerns") por diseño
      de contratos, no solo por convención documentada.
  recall_questions:
    - id: RQ-CH22-01
      text: |
        ¿Qué componente evalúa si un candidato completo debería promoverse a producción, y en qué se
        diferencia, con precisión, del componente que evalúa si una acción concreta puede ejecutarse
        dentro de un run ya en marcha?
      # respuesta esperada: EvaluationHarness (CMP-020); frontera con PolicyEngine (CMP-005, CH-05);
      # P-28.
    - id: RQ-CH22-02
      text: |
        ¿Qué relación tiene `EvaluationHarness` con `CapabilityDescriptor.version` (CH-08), y por qué
        `EvaluationHarness` no registra por sí mismo ninguna versión de capability?
    - id: RQ-CH22-03
      text: |
        ¿Qué campos tiene `EvaluationReport` (`C-032`), y por qué `certificationRequired` es un
        `Boolean` mientras `outcome` es un `ENUM` de tres valores, nunca reducido a dos?
    - id: RQ-CH22-04
      text: |
        ¿Qué campos tiene `BusinessOutcomeCorrelation` (`C-033`), y por qué `humanEscalationRef` se
        modela como `Optional<HumanInteractionRequestId>` en vez de un campo nuevo dentro de
        `HumanInteractionRequest` (CH-06)?
  explain_prompts:
    - id: EP-CH22-01
      text: |
        `EvaluationHarness` posee decidir si un candidato completo —un agente, un prompt, una skill,
        un modelo, una policy o una capability— debería promoverse a producción. Explica, como si
        hablaras con alguien sin contexto técnico, por qué NO posee decidir si una acción concreta
        puede ejecutarse dentro de un run que ya está corriendo — ¿qué se confundiría, en la
        práctica, si la misma pieza de software certificara candidatos para producción Y autorizara
        cada tool call de cada run en curso?
      target_entity: CMP-020
    - id: EP-CH22-02
      text: |
        `EvaluationReport.outcome` puede valer `CERTIFIED`, `REJECTED` o `NEEDS_REVIEW` —nunca solo
        las dos primeras. Explica qué problema real aparecería si un capítulo futuro eliminara
        `NEEDS_REVIEW`, obligando a que toda certificación de un candidato se resuelva, siempre, en
        el mismo instante en que se solicita.
      target_entity: C-032
  interleaved_questions:
    - id: IQ-CH22-01
      text: |
        `PolicyEngine.evaluatePolicyForToolCall` (CH-05) ya evalúa, con código real, un `ToolCall`
        concreto contra reglas de policy, produciendo `ALLOW`/`DENY`/`REQUIRE_APPROVAL` — una
        decisión que existe siempre DENTRO de un `ExecutionContext` de un run que ya está en marcha,
        con un `agentId` y un `runId` ya asignados. Si ahora necesitamos decidir si el propio AGENTE
        —o el prompt, la skill, el modelo o la policy que ese agente usa— debería, siquiera,
        permitírsele correr en producción, ¿le correspondería a `evaluatePolicyForToolCall`
        producir esa respuesta, ya que de todos modos evalúa "si algo está permitido" — o pertenece,
        otra vez, a un dueño distinto que actúa ANTES de que exista cualquier `ToolCall` que evaluar?
      current_chapter_entities: [CMP-020, C-032]
      prior_chapter_entities: [CMP-005, C-014]
      prior_chapter: CH-05
    - id: IQ-CH22-02
      text: |
        `CapabilityRegistry` (CH-08) ya declara, con código real, un campo `version: Text` explícito
        dentro de `CapabilityDescriptor` — la primera materialización de `P-26` ("Capabilities have
        governed lifecycles") en este libro. Si una organización necesita decidir si esa nueva
        versión de una capability ya registrada puede promoverse a producción, ¿le correspondería a
        `CapabilityRegistry` producir esa decisión de certificación — ya que de todos modos conoce
        la versión exacta del candidato — o esa decisión pertenece, deliberadamente, a un componente
        distinto que actúa sobre una referencia opaca a esa versión, sin necesitar conocer el
        registro completo de capabilities?
      current_chapter_entities: [CMP-020, C-032]
      prior_chapter_entities: [CMP-008, C-018]
      prior_chapter: CH-08
    - id: IQ-CH22-03
      text: |
        `HumanInteractionService.createHumanInteractionRequest` (CH-06) ya representa, persiste y
        resuelve, con código real, una intervención humana concreta —identificada por
        `HumanInteractionRequestId`— disparada por una `PolicyDecision` con `outcome =
        REQUIRE_APPROVAL`. Si ahora necesitamos registrar, además, que un run concreto involucró una
        escalación humana al correlacionarlo con un outcome de negocio, ¿le correspondería a este
        capítulo modelar una segunda forma de representar esa escalación — o basta con referenciar,
        de forma opaca, una `HumanInteractionRequestId` que `HumanInteractionService` ya produjo,
        sin que ese componente cambie una sola línea?
      current_chapter_entities: [CMP-020, C-033]
      prior_chapter_entities: [CMP-006, C-015]
      prior_chapter: CH-06
  flashcards:
    - id: FC-CH22-01
      front: |
        ¿Qué posee `EvaluationHarness`?
      back: |
        Evaluar cualquier candidato (agente, prompt, skill, modelo, policy o capability) ANTES de
        su promoción controlada a producción — cita literal, `P-28` ("Candidate agents, prompts,
        skills, models, policies and capabilities MUST be evaluable in an Evaluation Harness before
        controlled promotion to production"); aplicar o verificar una policy de certificación cuando
        la clase de riesgo del candidato lo exige — cita literal, `INV-E13` ("Production promotion
        requires certification policy where risk class requires it"); correlacionar la ejecución de
        un run con un outcome de negocio medible, un SLA/SLO aplicable y una posible escalación
        humana — cita literal, `P-29` ("Technical success does not imply business success. Enterprise
        runs SHOULD correlate execution with measurable outcomes, value, SLA/SLO and human
        escalation"); rechazar por defecto (fail-closed) un `EvaluationReport` sin referencia al
        candidato o un `BusinessOutcomeCorrelation` sin referencia al run.
      source_entity: CMP-020
      chapter_introduced_in: CH-22
      review_stage: DAY_1
    - id: FC-CH22-02
      front: |
        ¿Qué NO posee `EvaluationHarness`, y a qué componente pertenece la frontera más importante
        de este capítulo?
      back: |
        Evaluar o autorizar una ACCIÓN dentro de un run ya en curso (`PolicyEngine`, `CMP-005`,
        CH-05 — frontera más importante: `PolicyEngine` decide si UNA ACCIÓN puede ocurrir DENTRO de
        un run que ya existe; `EvaluationHarness` decide si UN CANDIDATO debe promoverse a
        producción ANTES de que exista ningún run); producir evidencia de auditoría
        estructuralmente inmutable sobre la decisión de certificación (`AuditLedger`, `CMP-017`,
        CH-19 — `EvaluationHarness` produce el resultado; auditarlo de forma inmutable es
        responsabilidad de otro componente); registrar versiones de capability o gestionar su
        lifecycle (`CapabilityRegistry`, `CMP-008`, CH-08); decidir si un run puede continuar
        operacionalmente contra su presupuesto (`ExecutionController`, `CMP-007`, CH-07); representar
        o resolver la intervención humana que `NEEDS_REVIEW` exige (`HumanInteractionService`,
        `CMP-006`, CH-06); ejecutar el mecanismo real de evaluación —correr el candidato contra un
        dataset de test real, calcular métricas reales— (Preview, infraestructura de borde).
      source_entity: CMP-020
      chapter_introduced_in: CH-22
      review_stage: DAY_1
    - id: FC-CH22-03
      front: |
        ¿Qué campos tiene `EvaluationReport` (`C-032`), y por qué `certificationRequired` SÍ puede
        ser un `Boolean` mientras `outcome` nunca lo es?
      back: |
        `id` (`EvaluationReportId`), `subjectRef` (`Text`, referencia opaca al candidato — mismo
        patrón que `subjectRef` en `AuditRecord`/`DataGovernanceLabel`, porque el universo de lo que
        este contrato describe es heterogéneo: un agente, un prompt, una skill, un modelo, una
        policy, una capability), `riskClass` (`RiskClass`, `ENUM` de cuatro valores
        `LOW`/`MEDIUM`/`HIGH`/`CRITICAL`), `certificationRequired` (`Boolean`) y `outcome`
        (`EvaluationOutcome`, `ENUM` de tres valores `CERTIFIED`/`REJECTED`/`NEEDS_REVIEW`) y
        `evaluatedAt` (`Timestamp`). `certificationRequired` es una propiedad BINARIA de la POLICY
        de certificación vigente para esa `riskClass` — o la clase de riesgo exige certificación, o
        no la exige; no hay un tercer estado posible para esa pregunta. `outcome`, en cambio, es el
        RESULTADO de una DECISIÓN, y esa decisión tiene, legítimamente, un tercer estado
        (`NEEDS_REVIEW`) en el que ni `CERTIFIED` ni `REJECTED` serían honestos todavía — colapsarlo
        a `Boolean` obligaría a fabricar una de las dos respuestas cuando la decisión real es "todavía
        no lo sabemos".
      source_entity: C-032
      chapter_introduced_in: CH-22
      review_stage: DAY_1
    - id: FC-CH22-04
      front: |
        ¿Qué campos tiene `BusinessOutcomeCorrelation` (`C-033`), y por qué `humanEscalationRef` es
        `Optional<HumanInteractionRequestId>` en vez de un campo nuevo en `HumanInteractionRequest`?
      back: |
        `id` (`BusinessOutcomeCorrelationId`), `runId` (`RunId`, el identificador ya existente desde
        CH-00 — el universo que este contrato describe es siempre exactamente un run, mismo
        argumento que ya usó `ExecutionPlacement.runId`, CH-21), `measuredOutcome` (`Text`, el
        outcome/valor de negocio medido — deliberadamente `Text` opaco y no un sistema de métricas
        estructurado, fuera de alcance de este capítulo), `slaRef` (`Optional<Text>`, referencia
        opaca a un SLA/SLO aplicable, cuando existe uno), `humanEscalationRef`
        (`Optional<HumanInteractionRequestId>`) y `correlatedAt` (`Timestamp`).
        `humanEscalationRef` reutiliza el identificador fuerte que `HumanInteractionService` (CH-06)
        ya produce — `NULL` significa "sin escalación", un valor real significa "hubo escalación, y
        esta es la solicitud exacta que la representó" — en vez de agregar un campo booleano nuevo a
        `HumanInteractionRequest`, que ya tiene su propio dueño exclusivo y no necesita saber que
        `EvaluationHarness` existe.
      source_entity: C-033
      chapter_introduced_in: CH-22
      review_stage: DAY_1
    - id: FC-CH22-05
      front: |
        `PolicyEngine.evaluatePolicyForToolCall` (CH-05) ya evalúa acciones con código real. ¿Por
        qué `EvaluationHarness` no extiende ese mismo mecanismo para certificar candidatos, ya que
        ambos "evalúan" y ambos producen un resultado de tres o más estados?
      back: |
        Porque el OBJETO y el MOMENTO de cada evaluación son categóricamente distintos.
        `PolicyEngine` evalúa un `ToolCall` — una acción concreta, propuesta por un modelo, DENTRO de
        un `ExecutionContext` de un run que ya existe, con un `agentId` y un `runId` ya asignados.
        `EvaluationHarness` evalúa un candidato completo — un agente, un prompt, una skill, un
        modelo, una policy o una capability — ANTES de que exista un solo run, sin ningún
        `ExecutionContext` todavía. Fusionar ambos mecanismos —ya que de todos modos ambos
        "evalúan"— obligaría a `PolicyEngine` a razonar sobre candidatos que todavía no tienen
        ningún run, exactamente el tipo de conflación de dominios que Article IV prohíbe: dos
        preguntas distintas ("¿puede ejecutarse esto ahora?" vs. "¿debería siquiera existir esto en
        producción?") nunca deben compartir un mismo dueño solo porque ambas usan la palabra
        "evaluar".
      source_entity: CMP-020
      chapter_introduced_in: CH-22
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH22-01
      recall_question: RQ-CH22-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH22-02
      recall_question: RQ-CH22-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH22-03
      recall_question: RQ-CH22-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH22-04
      recall_question: RQ-CH22-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 22 — EvaluationHarness y la Certificación de un Candidato Antes de que Exista Ningún Run

> **Reglas constitucionales (Amendment v1.1, `P-28`/`P-29`/`INV-E13`):**
> `P-28` — "Candidate agents, prompts, skills, models, policies and capabilities MUST be evaluable
> in an Evaluation Harness before controlled promotion to production."
> `P-29` — "Technical success does not imply business success. Enterprise runs SHOULD correlate
> execution with measurable outcomes, value, SLA/SLO and human escalation."
> `INV-E13` — "Production promotion requires certification policy where risk class requires it."

CH-21 cerró, con razón, los nueve "Canonical Enterprise Planes" de Amendment v1.1 — Ingress &
Activation, Execution, Agent Interoperability, Capability & Integration, Data & Context, Control,
Reliability, Observability & Governance y Execution Fabric — con al menos un capítulo real de este
libro materializando cada uno. Esa cuenta es correcta, y sigue siéndolo. Pero un plano canónico y un
principio constitucional no son la misma unidad de cobertura: Amendment v1.1 declara treinta reglas
(`P-16`..`P-30`, más las catorce `INV-Exx`), y los nueve planos que CH-21 completó no garantizan, por
sí solos, que las treinta reglas ya hayan sido citadas con código real. Verificado con un barrido
completo sobre los veintiún capítulos anteriores — no solo sobre sus secciones de Impacto
Constitucional, sino sobre el texto íntegro de cada `chapter.md` — exactamente tres reglas de la
Constitution nunca aparecieron citadas, ni una sola vez, en ningún capítulo anterior de este libro:
`P-28` ("Production and evaluation are separate execution concerns"), `P-29` ("Business outcomes are
first-class observability") e `INV-E13` ("Production promotion requires certification policy where
risk class requires it"). Ninguna de las tres pertenece, además, a ninguno de los nueve planos que
CH-21 declaró cubiertos — quedaron, literalmente, fuera de esa taxonomía, sin que ningún capítulo
anterior las hubiera mencionado siquiera en prosa.

Este capítulo, el vigesimotercer capítulo real de contenido de este libro, cierra esa última pieza.
A diferencia de `IdempotencyGuard` (CH-17), `OperationalController` (CH-18), `AuditLedger` (CH-19),
`DataGovernanceEngine` (CH-20) y `ExecutionFabricAdapter` (CH-21) — los cinco componentes anteriores
que este libro tuvo que sintetizar porque ningún texto constitucional los nombraba literalmente —
`P-28` nombra, casi textualmente, el componente que este capítulo instala: "evaluable in an
**Evaluation Harness**". `EvaluationHarness` no es, esta vez, una síntesis editorial evaluada contra
alternativas descartadas; es, con una capitalización canónica aplicada al nombre común que la propia
enmienda ya usa, la lectura más directa posible de la propia regla que este capítulo materializa.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de saber
> cómo se llama el componente de este capítulo. El detalle estructurado de esta sección vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, con precisión, dos preguntas
que ambas se llaman "evaluación" pero pertenecen a dominios completamente distintos: si una acción
concreta puede ejecutarse DENTRO de un run que ya existe, y si un candidato completo —un agente, un
prompt, una skill, un modelo, una policy o una capability— debería promoverse a producción ANTES de
que exista un solo run que lo use. Podrás diseñar un resultado de certificación de tres estados que
nunca se reduce a un simple aprobado/rechazado, y argumentar por qué el éxito técnico de un run nunca
implica, por sí solo, éxito de negocio.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e introduce
dos contratos de datos nuevos y el noveno componente de este libro que pertenece a Amendment v1.1 en
vez de a los once nombres originales de Article III.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar atrás;
están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este capítulo va
a definir):

1. Ya existe un componente que evalúa, en tiempo real, si una acción concreta dentro de un run que ya
   existe puede ejecutarse. Si ahora necesitamos decidir si un agente, un prompt, una skill, un
   modelo o una policy completos deberían siquiera promoverse a producción, antes de que exista un
   solo run que los use, ¿es esa la misma pregunta de evaluación, formulada sobre un objeto distinto,
   o dos preguntas de dominios completamente distintos?
2. Ya existe un contrato que registra, para cada capability disponible, una versión explícita. Si una
   nueva versión de una capability ya registrada es, con frecuencia, exactamente el tipo de candidato
   que habría que evaluar antes de promoverlo, ¿le corresponde a quien registra esa versión decidir
   también si debe certificarse?
3. Si la clase de riesgo de un candidato determina si necesita una política de certificación, ¿ese
   resultado debería reducirse siempre a dos estados —aprobado o rechazado— o existe un tercer estado
   legítimo en el que la decisión no puede tomarse todavía sin un humano?
4. Un run puede terminar sin ningún error técnico. ¿Ese éxito técnico garantiza, por sí solo, que
   produjo algún valor de negocio medible, o son dos juicios distintos que conviene poder
   correlacionar sin confundir?

## 1. Arquitectura Actual (Current Architecture)

CH-00..CH-21 dejaron instalados treinta y un contratos de datos y diecinueve componentes: los once
nombres completos de Article III ("Agent Runtime"), dos capítulos de integración, y ocho componentes
de Amendment v1.1 (`AdmissionController`, CMP-012, CH-14; `AgentCommunicationGateway`, CMP-013,
CH-15; `CredentialBroker`, CMP-014, CH-16; `IdempotencyGuard`, CMP-015, CH-17;
`OperationalController`, CMP-016, CH-18; `AuditLedger`, CMP-017, CH-19; `DataGovernanceEngine`,
CMP-018, CH-20; `ExecutionFabricAdapter`, CMP-019, CH-21).

`PolicyEngine` (CMP-005, CH-05) es, de los diecinueve, el único cuya responsabilidad completa incluye
evaluar si una acción ya resuelta puede ocurrir. `evaluatePolicyForToolCall` (CH-05 §11) recibe
siempre un `ToolCall` (C-008, CH-02) y un `ExecutionContext` (C-004, CH-00) — es decir, opera siempre
DENTRO de un run que ya existe, con un `runId`, un `sessionId` y un `agentId` ya asignados por
`AgentCore` (CH-11). Produce una `PolicyDecision` de tres resultados (`ALLOW`/`DENY`/
`REQUIRE_APPROVAL`, C-014), determinística y fail-closed. Nada en `evaluatePolicyForToolCall`, ni en
`PolicyDecision` como contrato, evalúa jamás si el AGENTE mismo, o el modelo, el prompt, la skill o la
policy que ese agente usa, deberían siquiera tener permitido correr en producción — esa pregunta
nunca aparece en CH-05, porque para que exista un `ToolCall` que evaluar, el candidato completo ya
tuvo que promoverse, ejecutarse, y llegar al punto de proponer una acción.

`CapabilityRegistry` (CMP-008, CH-08) es, de los diecinueve, el único cuyo contrato registrado
(`CapabilityDescriptor`, C-018) declara un campo `version: Text` explícito — la primera
materialización de `P-26` ("Capabilities have governed lifecycles") en este libro (CH-08 §5/§18).
`resolveCapability` (CH-08 §11) busca, dentro de una lista de `CapabilityDescriptor` ya poblada, uno
cuyo `name` coincida con el `capabilityName` propuesto por el modelo — y nada en esa función decide
si una versión concreta de esa capability debería, siquiera, estar disponible para producción; recibe
el registro completo ya resuelto como una señal de entrada asumida (CH-08 §11/§18).

`AuditLedger` (CMP-017, CH-19) es, de los diecinueve, el único cuya responsabilidad completa consiste
en preservar evidencia estructuralmente inmutable de una decisión ya tomada por otro componente
(`P-25`). `recordAuditEntry` (CH-19 §11) recibe siempre una decisión ya tomada — nunca la toma, nunca
la evalúa, nunca decide si esa decisión fue correcta.

`HumanInteractionService` (CMP-006, CH-06) es, de los diecinueve, el único que representa, persiste y
resuelve una intervención humana concreta, identificada por `HumanInteractionRequestId` (CH-06 §6),
disparada siempre por una `PolicyDecision` con `outcome = REQUIRE_APPROVAL`.

`P-28` ("Production and evaluation are separate execution concerns"), `P-29` ("Business outcomes are
first-class observability") e `INV-E13` ("Production promotion requires certification policy where
risk class requires it") fueron transcritas, junto con el resto de Amendment v1.1, en CH-00 §5 — pero
ningún capítulo posterior las citó nunca en su propia sección de Impacto Constitucional, ni en prosa,
ni construyó ningún mecanismo real que las materializara. Ningún contrato de este libro, hasta este
capítulo, modela el resultado de evaluar un candidato antes de su promoción a producción, ni la
correlación entre la ejecución de un run y un resultado de negocio medible.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas para esto, "evaluar" tiende a colapsarse, silenciosamente,
en una de tres suposiciones igual de incompletas. La primera: que si `PolicyEngine` ya evalúa si algo
está permitido, entonces ya evalúa, de paso, si un candidato completo puede promoverse a producción —
pero `evaluatePolicyForToolCall` recibe siempre un `ToolCall` dentro de un run que ya existe; nunca
recibe, ni podría recibir con su firma actual, un agente, un prompt o un modelo completos que todavía
no tienen ningún run. La segunda: que si `CapabilityRegistry` ya conoce la versión exacta de cada
capability, entonces también podría decidir si esa versión debe certificarse — pero CH-08 §8 ya trazó,
con precisión, que `CapabilityRegistry` resuelve intención declarada hacia una implementación
concreta, sin decidir nada sobre el lifecycle de gobierno de esa capability más allá de exponer su
`version` como un campo consultable. La tercera: que, como `AuditLedger` ya preserva evidencia de
decisiones, cualquier resultado de certificación podría modelarse directamente como un `AuditRecord`
— pero un `AuditRecord` preserva evidencia de una decisión YA TOMADA por su dueño correspondiente;
`AuditLedger` no tiene, ni debería tener, ningún mecanismo para PRODUCIR esa decisión en primer lugar.

Hay una segunda dimensión del problema, la que da nombre a `INV-E13`: que un candidato de riesgo alto
o crítico —un agente con permisos amplios, una policy que gobierna decisiones financieras, un modelo
nuevo cuyo comportamiento todavía no se conoce bien en producción— pueda promoverse sin que exista
ningún mecanismo que verifique, siquiera, si una política de certificación aplica. Sin un componente
dedicado, la única forma en que un sistema real "respetaría" esa exigencia sería que cada equipo, por
su cuenta, decidiera informalmente si su propio candidato necesita revisión — exactamente la ausencia
de gobierno determinístico que Article IV, aplicado aquí a nivel de todo un candidato en vez de una
sola acción, existe para prevenir.

Hay una tercera dimensión, distinta de las dos anteriores, y es la que da nombre a `P-29`: que un run
pueda completarse sin ningún fallo técnico —cada `ToolCall` autorizada, cada turno dentro de
`ExecutionBudget`, ninguna policy denegada— y que, sin embargo, nada en este libro, hasta este
capítulo, correlacione ese éxito técnico con un resultado de negocio real. `ExecutionController`
(CH-07) certifica que un run respetó su presupuesto; `PolicyEngine` certifica que cada acción fue
autorizada; ninguno de los dos, ni los dos juntos, certifica que ese run produjo valor, cumplió un
SLA/SLO, o evitó una escalación humana que debería haberse registrado como una señal de negocio, no
solo como una intervención operacional puntual.

Necesitamos que "evaluar un candidato antes de su promoción a producción, con la certificación que su
riesgo exige" y "correlacionar la ejecución de un run con un resultado de negocio medible" tengan, por
fin, un dueño único y nombrado — que produzca, para lo primero, un resultado que nunca se reduzca a
dos estados cuando la decisión real exige un tercero, y que, para lo segundo, registre esa correlación
sin absorber ni la evaluación de acciones que ya pertenece a `PolicyEngine`, ni la auditoría inmutable
que ya pertenece a `AuditLedger`, ni el registro de versiones que ya pertenece a `CapabilityRegistry`.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los treinta y un contratos y los diecinueve componentes que existen hasta este punto no bastan
porque:

- `P-28`, `P-29` e `INV-E13` fueron transcritas una sola vez, como parte de la transcripción completa
  de Amendment v1.1 en CH-00 §5, y nunca fueron citadas de nuevo, en Impacto Constitucional ni en
  prosa, por ningún capítulo posterior — a diferencia de `P-27` (CH-21), que al menos era nombrado
  como uno de los nueve "Canonical Enterprise Planes", estas tres reglas no pertenecen a ninguno de
  esos nueve planos y llegaron a este punto del libro sin ningún precedente parcial que resolver;
- `PolicyDecision` (C-014, CH-05) y `evaluatePolicyForToolCall` (CH-05 §11) modelan, deliberadamente,
  la autorización de UNA ACCIÓN dentro de un run que ya existe — ninguno de los dos declara, ni podría
  declarar sin romper su propia frontera, un resultado sobre un candidato que todavía no tiene ningún
  `ExecutionContext`;
- `CapabilityDescriptor.version` (C-018, CH-08) expone una versión consultable, pero `CapabilityRegistry.
  does_not_own` (CH-08 §8) nunca declaró la responsabilidad de decidir si esa versión debe certificarse
  para producción — esa pregunta, hasta este capítulo, no tenía dueño;
- `AuditRecord` (C-029, CH-19) preserva evidencia de una decisión ya tomada — extenderlo para que,
  además, PRODUJERA el resultado de una certificación habría reabierto un contrato ya registrado para
  una responsabilidad que `AuditLedger` nunca tuvo: `AuditLedger` no decide, solo preserva lo que otro
  componente ya decidió;
- ningún contrato de este libro modela, todavía, la correlación entre un `RunId` ya existente y un
  resultado de negocio medible — ni `ExecutionBudget` (CH-00, límites de consumo), ni
  `AgentRunStatus` (CH-01, estado de ciclo de vida), ni `PolicyDecision` (CH-05, autorización) dicen
  jamás si un run, además de terminar sin errores técnicos, produjo algún valor real;
- nada impide, hoy, que un capítulo de integración futuro conecte la promoción de un candidato
  directamente al despliegue, sin pasar antes por ninguna evaluación explícita — exactamente lo que
  `P-28` prohíbe;
- ningún componente de este libro declara, todavía, `owns` una responsabilidad que sea, literalmente,
  "evaluar un candidato antes de producción" o "correlacionar un run con un outcome de negocio" en vez
  de "evaluar una acción", "registrar una versión" o "auditar una decisión" — las tres categorías más
  cercanas que CH-05/CH-08/CH-19 ya cubrieron, dejando a `P-28`/`P-29`/`INV-E13` sin un dueño propio
  hasta este capítulo.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la secuencia
> `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una entidad que no
> haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT` registrado — **no
> magic entities**. Este capítulo aplica la misma disciplina que CH-00..CH-21 ya establecieron.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-13   Authorization is deterministic and external to the LLM.
           El mismo argumento que ya protegió la autorización desde CH-01/CH-05, la infraestructura
           de ejecución desde CH-21, se extiende aquí a la certificación de candidatos: el modelo
           nunca decide, nunca ve y nunca constituye una fuente de verdad sobre si él mismo, su
           propio prompt o su propia policy deberían certificarse para producción —
           evaluateCandidateForPromotion (seccion 11) es completamente determinística y externa al
           LLM, y no recibe ninguna entrada que el modelo haya producido.

Principles newly cited with real code (first time in this book)
    P-28   Production and evaluation are separate execution concerns.
           Primera materialización real, con código, de este principio — nunca antes citado con
           código real ni en prosa por ningún capítulo de este libro (solo transcrito como parte de
           Amendment v1.1 en CH-00 §5). EvaluationReport (seccion 6/7) y EvaluationHarness (seccion
           8) producen, por fin, el resultado de evaluar un candidato completo antes de que exista
           un solo run que lo use — completamente separado de PolicyEngine (CH-05), que evalúa
           acciones dentro de runs que ya existen.
    P-29   Business outcomes are first-class observability.
           Primera materialización real, con código, de este principio. BusinessOutcomeCorrelation
           (seccion 6/7) correlaciona, por fin, un run ya existente con un outcome de negocio
           medible, una referencia a SLA/SLO y una posible escalación humana — sin que
           ExecutionController (CH-07) o PolicyEngine (CH-05) necesiten cambiar una sola línea para
           que esa correlación exista como un hecho consultable.

Invariants preserved
    INV-18    Toda acción significativa produce un evento observable.
              evaluateCandidateForPromotion y correlateRunWithBusinessOutcome (seccion 11) emiten
              un AgentEvent cada una, condicionalmente, cuando existe un ExecutionContext y un
              AgentId reales — pero, con la misma disciplina que CH-18..CH-21 aplicaron a sus propias
              funciones, nunca fabrican esos campos cuando no existen (ver seccion 14).
    INV-19    Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy relevante.
              Ni EvaluationReport ni BusinessOutcomeCorrelation incluyen un campo de actor propio
              (ver seccion 6 para el porqué explícito, mismo argumento que ExecutionPlacement,
              CH-21) — la trazabilidad de INV-19 se satisface aquí, igual que en capítulos
              anteriores, a través del traceId que el AgentEvent condicional ya transporta.
    INV-20    Todo error operacional pertenece a una categoría conocida.
              Los dos únicos fallos reales de este capítulo (seccion 13) introducen EVALUATION, una
              categoría nueva de ErrorCategory — deliberadamente NO reutiliza POLICY (CH-05, propio
              de autorización de acciones) ni AUDIT (CH-19, propio de evidencia inmutable), por la
              misma razón de fondo que motiva todo este capítulo: conflacionar un fallo de
              evaluación de candidatos con el fallo de cualquier otro dominio sería la misma
              conflación de responsabilidades que Article IV prohíbe a nivel de componente, ahora
              aplicada a nivel de ErrorCategory.

Invariants newly cited with real code (first time in this book)
    INV-E13   Production promotion requires certification policy where risk class requires it.
              Primera materialización real, con código, de este invariante. EvaluationReport.
              riskClass/certificationRequired (seccion 6) y evaluateCandidateForPromotion (seccion
              11) verifican, por fin, si la clase de riesgo de un candidato exige una política de
              certificación — produciendo NEEDS_REVIEW, nunca una aprobación fabricada, cuando esa
              certificación no puede resolverse todavía.

Component ownership changes
    CMP-020 EvaluationHarness se introduce — registry/components.yaml pasa de 19 a 20 componentes.
    Es el noveno componente de este registry que NO corresponde a ninguno de los once nombres del
    árbol de Article III ("Agent Runtime") — a diferencia de los ocho anteriores (CMP-012..CMP-019),
    no pertenece a ninguno de los nueve "Canonical Enterprise Planes" de Amendment v1.1: P-28, P-29
    e INV-E13 quedan, deliberadamente, fuera de esa taxonomía de planos.
    registry/components.yaml de CMP-005 (PolicyEngine), CMP-006 (HumanInteractionService), CMP-007
    (ExecutionController), CMP-008 (CapabilityRegistry) y CMP-017 (AuditLedger) NO se modifica:
    ninguno cablea todavía su relación real con EvaluationHarness (ver seccion 9/18).

Lifecycle changes
    Ninguna modificación al ENUM AgentRunStatus (C-013): sigue siendo, sin cambios desde CH-01, el
    mismo conjunto de once valores. Ni EvaluationReport (C-032) ni BusinessOutcomeCorrelation
    (C-033) introducen ningún ENUM de lifecycle propio — el cambio se modela, otra vez, por
    reemplazo: una invocación nueva de evaluateCandidateForPromotion sobre el mismo subjectRef
    produce un EvaluationReport nuevo, nunca una edición del anterior (ver seccion 12).

Security implications
    EvaluationHarness es el primer componente de este libro cuya responsabilidad completa es
    evaluar un candidato ANTES de que exista cualquier run, y correlacionar un run ya existente con
    un resultado de negocio — dos preguntas nunca resueltas por ningún componente anterior. Ver
    seccion 15 para el análisis completo, incluyendo la frontera más importante de este capítulo,
    contra PolicyEngine.

Observability implications
    Igual que DataGovernanceEngine (CH-20) e IdempotencyGuard (CH-17), EvaluationHarness emite
    AgentEvent de forma condicional desde dos funciones distintas (EVALUATION_REPORT_PRODUCED,
    BUSINESS_OUTCOME_CORRELATED) — una por cada responsabilidad real de este capítulo.

Deterministic vs agentic boundary
    Article XII se refina una vigésima vez a nivel de componente: EvaluationHarness, igual que
    EventBus (CH-09), OperationalController (CH-18), AuditLedger (CH-19), DataGovernanceEngine
    (CH-20) y ExecutionFabricAdapter (CH-21), no recibe ninguna entrada que el modelo haya producido
    — ni siquiera de forma indirecta. Evalúa exclusivamente una referencia opaca a un candidato, una
    clase de riesgo ya clasificada, una señal de certificación ya resuelta, y una referencia a un run
    ya existente — todas ajenas a cualquier razonamiento del propio modelo que ese candidato pudiera
    producir.
```

## 5. Conceptos Nuevos (New Concepts)

- **Pre-Production Candidate Evaluation** *(cita literal, `P-28`, "Candidate agents, prompts, skills,
  models, policies and capabilities MUST be evaluable in an Evaluation Harness before controlled
  promotion to production")*: la evaluación de un candidato completo —nunca de una acción concreta—
  ANTES de que exista un solo run que lo use, con el fin de decidir su promoción controlada a
  producción. Es la pregunta que `PolicyEngine` (CH-05) nunca responde, porque su firma exige siempre
  un `ToolCall` dentro de un run ya existente.
- **Risk Class**: la clasificación del nivel de riesgo de un candidato —modelada como `RiskClass`
  (`ENUM` de cuatro valores, seccion 6)— que determina si una política de certificación aplica o no.
  Sin ella, `INV-E13` no tendría ninguna señal de entrada sobre la que decidir.
- **Certification Policy** *(cita literal, `INV-E13`, "Production promotion requires certification
  policy where risk class requires it")*: la exigencia, condicionada por la `RiskClass` de un
  candidato, de que una política de certificación se aplique antes de su promoción. Modelada como
  `EvaluationReport.certificationRequired` (`Boolean`, seccion 6) — una propiedad binaria de la
  policy vigente para esa clase de riesgo, nunca el resultado de la evaluación misma.
- **Three-State Certification Outcome**: el resultado de evaluar un candidato nunca se reduce a
  aprobado/rechazado — modelado como `EvaluationOutcome` (`ENUM` de tres valores
  `CERTIFIED`/`REJECTED`/`NEEDS_REVIEW`, seccion 6), donde `NEEDS_REVIEW` es el estado que exige
  intervención humana antes de decidir, mismo principio que ya protegió `REQUIRE_APPROVAL`
  (`PolicyOutcome`, CH-05).
- **Business Outcome Correlation** *(cita literal, `P-29`, "Enterprise runs SHOULD correlate
  execution with measurable outcomes, value, SLA/SLO and human escalation")*: la asociación entre un
  run ya existente y un resultado de negocio medible, una referencia a un SLA/SLO aplicable, y una
  posible escalación humana — modelada como `BusinessOutcomeCorrelation` (seccion 6/7). Es la
  materialización directa de que el éxito técnico de un run (ningún error, presupuesto respetado) no
  implica, por sí solo, éxito de negocio.
- **Decision Ownership, aplicado por novena vez** *(Article IV)*: `EvaluationHarness` decide "¿debe
  este candidato promoverse a producción, y con qué nivel de certificación?" y "¿qué resultado de
  negocio correlaciona con este run?"; explícitamente NO decide "¿puede ejecutarse esta acción ahora
  mismo?" (`PolicyEngine`, ya resuelto, CH-05 — la frontera más importante de este capítulo), "¿debe
  registrarse esta versión de capability?" (`CapabilityRegistry`, ya resuelto, CH-08), "¿debe
  preservarse esta decisión como evidencia inmutable?" (`AuditLedger`, ya resuelto, CH-19) ni "¿puede
  este run seguir consumiendo su presupuesto?" (`ExecutionController`, ya resuelto, CH-07).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `Text`, `Timestamp`, `Boolean`, `Optional`, `RunId`,
`AgentId`, `ExecutionContext` (C-004, CH-00), `AgentEvent` (C-010, CH-00), `HarnessError` (C-011,
CH-00).

Este capítulo reutiliza, además, un identificador ya existente que no es un contrato completo
(`STRUCT`) sino un identificador opaco definido dentro del `STRUCT` de otro capítulo — se declara aquí
explícitamente, siguiendo la misma convención que `HumanInteractionRequest` (CH-06 §6) ya estableció
para sus propios identificadores:

| Identificador (reusado, no nuevo de este capítulo) | Identifica | Introducido en |
|---|---|---|
| `HumanInteractionRequestId` | la solicitud de interacción humana concreta que `BusinessOutcomeCorrelation.humanEscalationRef` referencia opacamente, cuando una escalación existió | CH-06 |

**Por qué `BusinessOutcomeCorrelation.humanEscalationRef` reutiliza `HumanInteractionRequestId` en vez
de agregar un campo booleano nuevo dentro de `HumanInteractionRequest` (CH-06).** Se evaluó
explícitamente extender `HumanInteractionRequest` con un campo que indicara si esa solicitud, además,
alimenta una correlación de negocio — se descartó porque `HumanInteractionRequest` ya tiene su dueño
exclusivo (`HumanInteractionService`, CH-06), y ese componente no necesita saber que
`EvaluationHarness` existe, ni que un run del que participó será, más adelante, correlacionado con un
outcome de negocio. Reutilizar el identificador fuerte ya existente, dentro de un campo `Optional` de
este capítulo, logra la misma trazabilidad —`NULL` significa "sin escalación", un valor real significa
"hubo una, y esta es la solicitud exacta"— sin reabrir un contrato de CH-06 para una responsabilidad
que nunca le perteneció.

Este capítulo cita, además en prosa, un contrato de un capítulo anterior sin usarlo dentro de su
propio pseudocódigo — mismo patrón de reuso explícito que CH-13 §6, CH-19 §6, CH-20 §6 y CH-21 §6 ya
aplicaron:

| Contrato/tipo (reusado, no nuevo) | Introducido en | Uso en este capítulo |
|---|---|---|
| `CapabilityDescriptor` | CH-08 §6 | citado en prosa (seccion 1/2/3/5/9) como el precedente de "un candidato típico a evaluar" — una nueva versión de una capability ya registrada — nunca usado dentro del pseudocódigo de este capítulo |
| `PolicyDecision` | CH-05 §6 | citado en prosa (seccion 1/2/8/15) para trazar la frontera entre evaluar una acción y evaluar un candidato — nunca usado dentro del pseudocódigo de este capítulo |

### Un identificador opaco nuevo, por cada contrato de este capítulo

Siguiendo el mismo patrón que CH-00 §6 estableció para los identificadores fundamentales, y que
CH-14..CH-21 repitieron para los suyos:

| Identificador (nuevo de este capítulo) | Identifica |
|---|---|
| `EvaluationReportId` | un `EvaluationReport` concreto — el resultado de evaluar un candidato antes de su promoción a producción |
| `BusinessOutcomeCorrelationId` | un `BusinessOutcomeCorrelation` concreto — la correlación vigente entre un run y un outcome de negocio |

### `ErrorCategory` — extendida, sin redefinir `HarnessError`

Este es el undécimo capítulo que agrega un valor a `ErrorCategory` desde que CH-00 lo declaró
(después de `HUMAN_INTERACTION`, CH-06; `ADMISSION`, CH-14; `DELEGATION`, CH-15; `CREDENTIAL`, CH-16;
`IDEMPOTENCY`, CH-17; `CONTROL`, CH-18; `AUDIT`, CH-19; `GOVERNANCE`, CH-20; y `EXECUTION_FABRIC`,
CH-21): el valor `EVALUATION`, necesario porque ninguna de las diecinueve categorías ya existentes
representa, sin conflación, un fallo específico de evaluar un candidato o de correlacionar un run con
un outcome de negocio — reutilizar `POLICY` (CH-05, propio de autorización de acciones dentro de un
run) o `AUDIT` (CH-19, propio de evidencia inmutable) habría sido, precisamente, el tipo de conflación
de dominios que Article IV prohíbe a nivel de componente, ahora aplicada a nivel de `ErrorCategory`:

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
    EVALUATION
END
```

`HarnessError` (C-011) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — mismo patrón
exacto que las extensiones de CH-06/CH-14..CH-21, aplicado aquí por décima vez a `ErrorCategory`.

### `AgentEventType` — extendida, sin redefinir `AgentEvent`

CH-21 dejó `AgentEventType` en treinta y un valores. Este capítulo agrega dos valores nuevos — mismo
patrón que `IdempotencyGuard` (CH-17) y `DataGovernanceEngine` (CH-20), que también agregaron dos
porque introdujeron dos funciones reales:

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
    EVALUATION_REPORT_PRODUCED
    BUSINESS_OUTCOME_CORRELATED
END
```

`AgentEvent` (C-010) no cambia: solo el rango de valores permitido para `eventType` crece, igual que en
cada capítulo anterior salvo `EventBus` (CH-09), `AdmissionController` (CH-14) y
`AgentCommunicationGateway` (CH-15).

### `RiskClass` — la clasificación de riesgo de un candidato

```pseudocode
ENUM RiskClass
    LOW
    MEDIUM
    HIGH
    CRITICAL
END
```

**Por qué cuatro valores, y no un `Boolean isHighRisk`.** `INV-E13` condiciona la exigencia de una
policy de certificación a "risk class" — en singular con un sustantivo de clasificación, no a un par
binario "alto riesgo / bajo riesgo". Se evaluó explícitamente un `Boolean` — más simple de construir —
y se descartó por el mismo argumento que ya descartó un `Boolean` en `DataClassificationLevel`
(CH-20 §6) y en `DeploymentTopology` (CH-21 §6): un `Boolean` colapsaría cuatro realidades operacionales
distintas —un candidato de riesgo trivial que no necesita ninguna revisión especial; uno de riesgo
moderado que podría necesitar revisión ligera; uno de riesgo alto, con impacto significativo si falla;
uno de riesgo crítico, con impacto potencialmente catastrófico o irreversible— en dos categorías
arbitrarias, perdiendo exactamente la gradación que una política de certificación real necesitaría
para decidir cuánta evidencia exigir. Cuatro valores es, además, el mismo tamaño de escala que ya usó
`DataClassificationLevel` (`PUBLIC`/`INTERNAL`/`CONFIDENTIAL`/`RESTRICTED`, CH-20) para un problema de
forma análoga —una escala ordinal de sensibilidad/riesgo, no una enumeración cerrada de casos
discretos como `DeploymentTopology`— reforzando que cuatro niveles es la granularidad mínima que este
libro ya considera suficiente para una escala de esta naturaleza.

### `EvaluationOutcome` — el resultado de una certificación, nunca reducido a dos estados

```pseudocode
ENUM EvaluationOutcome
    CERTIFIED
    REJECTED
    NEEDS_REVIEW
END
```

**Por qué tres valores, y no `Boolean approved`.** Se evaluó explícitamente un `Boolean` —
`CERTIFIED`/`REJECTED` únicamente— y se descartó por el mismo argumento que ya protegió
`PolicyOutcome.REQUIRE_APPROVAL` (CH-05) y `EvaluationOutcome` de CH-20's `RetentionEnforcementOutcome`:
existe una decisión que, honestamente, no puede tomarse todavía en el instante en que se evalúa un
candidato —cuando `certificationRequired = TRUE` pero la señal de si la certificación ya se satisfizo
todavía no ha llegado, o exige juicio humano explícito antes de decidir—. Un `Boolean` habría forzado
a `evaluateCandidateForPromotion` (seccion 11) a fabricar `CERTIFIED` o `REJECTED` en ese instante,
sin ninguna base real para ninguna de las dos respuestas — exactamente el tipo de dato inventado que
este libro evita.

### `EvaluationReport` — el resultado de evaluar un candidato antes de producción

```pseudocode
STRUCT EvaluationReport
    id: EvaluationReportId
    subjectRef: Text
    riskClass: RiskClass
    certificationRequired: Boolean
    outcome: EvaluationOutcome
    evaluatedAt: Timestamp
END
```

Seis campos, cada uno respondiendo a una parte exacta del alcance decidido para este capítulo: `id`
identifica este resultado de forma estable; `subjectRef` es una referencia opaca `Text` al candidato
evaluado — un agente, un prompt, una skill, un modelo, una policy o una capability — mismo patrón que
`subjectRef` en `AuditRecord` (CH-19) y `DataGovernanceLabel` (CH-20), porque el universo de lo que
este contrato describe es, deliberadamente, heterogéneo; `riskClass` es el `RiskClass` de la sección
anterior; `certificationRequired` es un `Boolean` — una propiedad de la POLICY de certificación vigente
para esa `riskClass`, nunca el resultado de la propia decisión (ver el análisis explícito más abajo);
`outcome` es el `EvaluationOutcome` de tres estados de la sección anterior; `evaluatedAt` registra
cuándo se produjo este resultado.

**Por qué `subjectRef` es una referencia opaca `Text`, y no un identificador fuerte como `runId:
RunId` en `ExecutionPlacement` (C-031, CH-21).** Se evaluó explícitamente seguir el patrón de
`ExecutionPlacement.runId` —un identificador fuerte, porque el universo referenciado era homogéneo:
siempre exactamente un run— y se descartó para este contrato: lo que `EvaluationReport` describe es,
por diseño de `P-28`, un candidato de seis tipos posibles y potencialmente más en el futuro (agente,
prompt, skill, modelo, policy, capability) — exactamente el mismo universo heterogéneo que ya motivó
`subjectRef: Text` en `AuditRecord` (CH-19) y `DataGovernanceLabel` (CH-20), nunca el universo
homogéneo que motivó `RunId` tipado en `ExecutionPlacement` (CH-21).

**Por qué `certificationRequired` SÍ puede modelarse como `Boolean`, cuando este libro ya descartó un
`Boolean` para `RiskClass` y para `EvaluationOutcome` en las dos secciones anteriores.** La diferencia
no es arbitraria: `certificationRequired` no es el resultado de una decisión que este componente toma
—es una PROPIEDAD YA DETERMINADA de la política de certificación vigente para una `riskClass` dada,
resuelta por completo antes de que `evaluateCandidateForPromotion` (seccion 11) se ejecute—. Para una
`riskClass` concreta, o la política exige certificación, o no la exige; no existe, para esta pregunta
específica, ningún tercer estado legítimo de incertidumbre, porque la propia clase de riesgo ya
determina la respuesta de forma binaria por definición de la política. `RiskClass` y `EvaluationOutcome`,
en cambio, sí necesitan más de dos valores porque cada uno representa una gradación real (cuatro
niveles de riesgo) o una decisión que puede, legítimamente, no resolverse todavía (tres estados de
certificación) — la lección de este contrato es que un campo `Boolean` sigue siendo correcto cuando la
pregunta que responde es, por naturaleza, binaria; el error sería aplicar esa misma simplicidad a una
pregunta que no lo es.

**Por qué `EvaluationReport` no incluye un campo `actor: ActorId`.** Mismo argumento exacto que
`DataGovernanceLabel` (CH-20 §6) y `ExecutionPlacement` (CH-21 §6): `EvaluationReport` describe una
propiedad del CANDIDATO evaluado —no una decisión tomada por un actor humano en un instante dado—, y
la trazabilidad de `INV-19` sigue siendo satisfecha a través del `traceId`/`agentId` que el `AgentEvent`
condicional ya transporta cuando existen (seccion 14).

**Por qué `EvaluationReport` no tiene ningún campo de estado propio.** Igual que `DataGovernanceLabel`
(CH-20 §12) y `ExecutionPlacement` (CH-21 §12), la ausencia de un campo de estado no significa que un
`EvaluationReport` sea inmutable en el sentido de `AuditRecord` (CH-19): un candidato puede
reevaluarse más tarde —una nueva versión, una nueva evidencia de certificación— y ese cambio se modela
por **reemplazo** (una invocación nueva de `evaluateCandidateForPromotion` produce un
`EvaluationReport` completamente nuevo), nunca por mutación de la instancia anterior (ver seccion 12).

### `BusinessOutcomeCorrelation` — la correlación entre un run y un resultado de negocio

```pseudocode
STRUCT BusinessOutcomeCorrelation
    id: BusinessOutcomeCorrelationId
    runId: RunId
    measuredOutcome: Text
    slaRef: Optional<Text>
    humanEscalationRef: Optional<HumanInteractionRequestId>
    correlatedAt: Timestamp
END
```

Seis campos: `id` identifica esta correlación de forma estable; `runId` referencia, con el
identificador fuerte ya existente desde CH-00 — mismo argumento exacto que ya justificó
`ExecutionPlacement.runId` (CH-21 §6): el universo de lo que este contrato describe es siempre
exactamente un run, nunca un tipo heterogéneo de dato — el run cuya ejecución se correlaciona;
`measuredOutcome` es el outcome/valor de negocio medido, deliberadamente `Text` opaco (ver el análisis
explícito más abajo); `slaRef` es una referencia opaca `Optional<Text>` a un SLA/SLO aplicable, cuando
existe uno; `humanEscalationRef` es `Optional<HumanInteractionRequestId>`, la referencia opaca a que
existió una escalación humana durante ese run (ver seccion 6, tabla de identificadores reusados, para
el análisis completo); `correlatedAt` registra cuándo se produjo esta correlación.

**Por qué `measuredOutcome` es `Text`, y no `Number` ni una `STRUCT Metric` estructurada.** Se evaluó
explícitamente un `Number` —más preciso para comparar outcomes entre runs— y se descartó porque el
universo de lo que `P-29` exige correlacionar es heterogéneo por naturaleza: un ingreso monetario, una
tasa de resolución de un ticket, una puntuación de satisfacción, o incluso un resultado categórico
("escalado a revisión manual", "conversión completada") que nunca fue, ni debería fingir ser, un
número. Se evaluó también una `STRUCT Metric` con campos tipados por tipo de outcome — y se descartó
explícitamente por estar fuera de alcance de este capítulo: construir un sistema de métricas de
negocio completo (unidades, agregaciones, series de tiempo) es, deliberadamente, un problema mucho más
grande que "correlacionar un run con un outcome medible" — el mismo tratamiento que
`computeResourceRef: Optional<Text>` (`ExecutionPlacement`, CH-21) o `residencyRequirement:
Optional<Text>` (`DataGovernanceLabel`, CH-20) ya dieron a un detalle real que un capítulo posterior,
si lo necesita, puede estructurar sin reabrir este contrato.

**Por qué `slaRef` y `humanEscalationRef` son `Optional`, y no obligatorios.** No todo run tiene un
SLA/SLO aplicable, y no toda ejecución involucra una escalación humana — exigir ambos campos como
obligatorios habría forzado a fabricar valores centinela para los casos donde, legítimamente, no
aplican, exactamente el mismo argumento que ya usó `ExecutionPlacement.residencyConstraint` (CH-21
§6).

**Por qué `BusinessOutcomeCorrelation` no tiene ningún campo de estado ni de actor.** Mismo argumento
que `EvaluationReport`, arriba: describe una propiedad medida de un run —no una decisión tomada por un
actor en un instante—, y un mismo `runId` puede acumular, con el tiempo, varias correlaciones distintas
(medidas en momentos diferentes tras la finalización del run) sin que ninguna reemplace ni invalide a
la anterior — a diferencia de `ExecutionPlacement` (CH-21), donde una nueva resolución sí vuelve
obsoleta a la anterior, aquí varias correlaciones coexistentes son, en sí mismas, información legítima
(ver seccion 12).

**Unchanged / Not yet introduced**: `AgentState`/`ExecutionContext` (C-003/C-004, CH-00) no cambian de
forma — ninguno de los dos gana un campo `evaluationReport` ni `businessOutcomeCorrelation` en este
capítulo (ver seccion 9/18). `PolicyDecision` (C-014, CH-05) tampoco cambia: sigue siendo, sin
excepción, el contrato exclusivo de autorización de acciones dentro de un run.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce dos contratos de
datos, registrados en `registry/contracts.yaml`:

```text
ID:                     C-032
Name:                   EvaluationReport
Version:                v1
Introduced In:          CH-22
Current Definition:     STRUCT EvaluationReport (ver §6)
Used By:                [CMP-020]
Modified By:            []
Constitutional Impact:  [P-28, INV-E13, INV-19]
```

```text
ID:                     C-033
Name:                   BusinessOutcomeCorrelation
Version:                v1
Introduced In:          CH-22
Current Definition:     STRUCT BusinessOutcomeCorrelation (ver §6)
Used By:                [CMP-020]
Modified By:            []
Constitutional Impact:  [P-29, INV-19]
```

`C-032` y `C-033` son el decimonoveno y vigésimo id que este libro asigna sin que estuvieran
reservados desde CH-01 §7 — el correlativo simplemente continúa después de `C-031` (CH-21). Ninguno
colisiona, por nombre, con ningún contrato ya registrado — verificado con grep completo sobre
`registry/contracts.yaml` antes de escribir este capítulo.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el noveno componente del registry que no corresponde a ninguno de los once
nombres del árbol de Article III ("Agent Runtime") — y, a diferencia de los ocho anteriores, no
pertenece a ninguno de los nueve "Canonical Enterprise Planes" de Amendment v1.1:

```pseudocode
COMPONENT EvaluationHarness
    consumes: ExecutionContext
    produces: EvaluationReport, BusinessOutcomeCorrelation, AgentEvent, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Amendment v1.1 (`P-28`/`P-29`/`INV-E13`) — Article III no
tiene, todavía, una sección propia para este componente, exactamente igual que `AdmissionController`
(CH-14), `AgentCommunicationGateway` (CH-15), `CredentialBroker` (CH-16), `IdempotencyGuard` (CH-17),
`OperationalController` (CH-18), `AuditLedger` (CH-19), `DataGovernanceEngine` (CH-20) y
`ExecutionFabricAdapter` (CH-21):

```text
COMPONENT: EvaluationHarness

Responsibility:
    Evaluar cualquier candidato (un agente, un prompt, una skill, un modelo, una policy o una
    capability) ANTES de su promoción controlada a producción, aplicando o verificando la policy de
    certificación que su clase de riesgo exige y produciendo un resultado de tres estados que nunca
    se reduce a aprobado/rechazado cuando la decisión no puede tomarse todavía — y correlacionar la
    ejecución de un run ya existente con un outcome de negocio medible, un SLA/SLO aplicable y una
    posible escalación humana — sin evaluar ni autorizar ninguna acción dentro de un run en curso,
    sin producir evidencia de auditoría inmutable, sin registrar versiones de capability y sin
    decidir si un run puede continuar operacionalmente.

Consumes:
    C-004 ExecutionContext (solo cuando la evaluación o la correlación ocurren dentro de uno real,
    ver seccion 11)

Depends on:
    (ninguno todavía — el cableado real hacia PolicyEngine/CapabilityRegistry/HumanInteractionService/
    AuditLedger/ExecutionController es Preview, no introducido en este capítulo; ver seccion 9)

Produces:
    C-032 EvaluationReport (el resultado de evaluar un candidato), C-033 BusinessOutcomeCorrelation
    (la correlación de negocio), C-010 AgentEvent (EVALUATION_REPORT_PRODUCED/
    BUSINESS_OUTCOME_CORRELATED, condicionales, ver seccion 14), C-011 HarnessError

Owns (Amendment v1.1 `P-28`/`P-29`/`INV-E13`, cita y lectura literal):
    - "Candidate agents, prompts, skills, models, policies and capabilities MUST be evaluable in an
      Evaluation Harness before controlled promotion to production" (cita literal, P-28) — evaluar,
      en exclusiva, cualquier candidato completo antes de su promoción controlada a producción,
      completamente separado de evaluar una acción dentro de un run ya existente
    - "Production promotion requires certification policy where risk class requires it" (cita
      literal, INV-E13) — aplicar o verificar, según la RiskClass de un candidato, si una policy de
      certificación aplica, produciendo NEEDS_REVIEW en vez de fabricar CERTIFIED/REJECTED cuando esa
      certificación no puede resolverse todavía
    - "Technical success does not imply business success. Enterprise runs SHOULD correlate
      execution with measurable outcomes, value, SLA/SLO and human escalation" (cita literal, P-29)
      — correlacionar, en exclusiva, la ejecución de un run ya existente con un outcome de negocio
      medible, una referencia opaca a un SLA/SLO aplicable, y una posible escalación humana
    - rechazar por defecto (fail-closed) un EvaluationReport sin referencia al candidato que evalúa,
      o un BusinessOutcomeCorrelation sin referencia al run que correlaciona

Does NOT own:
    - evaluar o autorizar una acción concreta dentro de un run ya en curso (PolicyEngine, CMP-005,
      ya introducido en CH-05 — la frontera más importante de este capítulo: PolicyEngine decide si
      UNA ACCIÓN puede ocurrir DENTRO de un run que ya existe; EvaluationHarness decide si UN
      CANDIDATO debe promoverse a producción ANTES de que exista ningún run que lo use — dos
      preguntas de "evaluación" que nunca comparten dueño, aunque ambas usen esa misma palabra)
    - producir evidencia de auditoría estructuralmente inmutable sobre la decisión de certificación
      (AuditLedger, CMP-017, ya introducido en CH-19 — EvaluationHarness produce el resultado de
      evaluación; auditarlo de forma inmutable, si alguien lo necesita, es responsabilidad de
      AuditLedger, nunca de este componente)
    - registrar versiones de capability o gestionar su lifecycle de rollout/deprecation/retirement
      (CapabilityRegistry, CMP-008, ya introducido en CH-08 — CapabilityRegistry declara qué
      CapabilityDescriptor existen y cuál es su version; EvaluationHarness evalúa, mediante
      subjectRef, si una versión concreta YA REGISTRADA debe certificarse para producción — nunca
      crea, versiona ni retira una capability)
    - decidir si un run puede continuar operacionalmente contra su ExecutionBudget
      (ExecutionController, CMP-007, ya introducido en CH-07 — presupuesto de consumo dentro de un
      run en marcha, pregunta ortogonal a certificar un candidato antes de que exista cualquier run)
    - representar, persistir o resolver la intervención humana que NEEDS_REVIEW exige
      (HumanInteractionService, CMP-006, ya introducido en CH-06 — EvaluationHarness produce el
      estado que exige esa intervención; HumanInteractionService es quien la representa, persiste y
      resuelve, exactamente como ya lo hace para REQUIRE_APPROVAL de PolicyEngine)
    - aplicar kill switches, aislamiento de tenant, o cualquier otro control operacional
      (OperationalController, CMP-016, ya introducido en CH-18)
    - ejecutar el mecanismo real de evaluación — correr el candidato contra un dataset de test real,
      calcular métricas reales de calidad o seguridad, o medir en la práctica un outcome de negocio
      (Preview, infraestructura de borde — este componente decide la FORMA del resultado, nunca
      construye el motor real que lo calcula)
    - generar por sí mismo el subjectRef, la riskClass, la señal de si la certificación ya se
      satisfizo, el runId o el measuredOutcome — todas llegan como señales de entrada ya resueltas
      (mismo patrón que subjectRef en CH-19/CH-20, o runId/topology en CH-21)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con la misma
particularidad que los ocho componentes de Amendment v1.1 anteriores: ninguna de las siete exclusiones
proviene de una ficha propia de Article III (que no existe para este componente); provienen de
fronteras ya establecidas por componentes ya registrados. La primera exclusión de esta lista es,
deliberadamente, la más parecida en prosa informal a lo que este componente sí posee — el mismo
cuidado editorial que CH-04 §8, CH-19 §8, CH-20 §8 y CH-21 §8 ya aplicaron frente a su propia frontera
más importante.

**Nota sobre Article IV.** Igual que `DataGovernanceEngine` (CH-20) o `ExecutionFabricAdapter`
(CH-21), `EvaluationHarness` sí decide algo real —si un candidato debe certificarse, y qué outcome de
negocio correlaciona con un run— y no comparte la ausencia de fila de `EventBus` (CH-09) o
`AuditLedger` (CH-19), que solo preservan o distribuyen decisiones ajenas.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
EvaluationHarness
    consumes → ExecutionContext
    produces → EvaluationReport, BusinessOutcomeCorrelation, AgentEvent, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`EvaluationHarness` no depende hoy de ningún otro componente registrado — mismo patrón que
CH-01..CH-21 ya establecieron para sus propios componentes. En prosa (nunca dentro de un bloque
`pseudocode`, per `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las relaciones futuras
que un capítulo de integración agregaría son:

| Componente futuro (relación inversa — no cableada en este capítulo) | Qué relación tendría con `EvaluationHarness` |
|---|---|
| `CapabilityRegistry` (ya existente, CMP-008) | una nueva entrada en `registeredCapabilities` (CH-08 §11), con un `CapabilityDescriptor.version` nuevo, podría disparar una invocación de `evaluateCandidateForPromotion` usando ese `version` como parte de `subjectRef` — sin que `resolveCapability` cambie una sola línea |
| `PolicyEngine` (ya existente, CMP-005) | permanecería sin relación con `EvaluationHarness`: `evaluatePolicyForToolCall` sigue evaluando exclusivamente acciones dentro de runs que ya existen — la frontera se mantiene, no se cablea |
| `HumanInteractionService` (ya existente, CMP-006) | un `EvaluationReport` con `outcome = NEEDS_REVIEW` podría, en principio, disparar un `HumanInteractionRequest` nuevo — de forma análoga a como `PolicyDecision.REQUIRE_APPROVAL` ya lo hace (CH-06 §9) — sin que `createHumanInteractionRequest` cambie su firma |
| `AuditLedger` (ya existente, CMP-017) | podría auditar, con `recordAuditEntry` (CH-19 §11), el hecho de que una certificación concreta ocurrió — usando el `id` de un `EvaluationReport` como `subjectRef` — sin que eso convierta a `EvaluationReport` mismo en evidencia inmutable (ver seccion 15) |
| `ExecutionController` (ya existente, CMP-007) | `evaluateExecutionContinuation` (CH-07 §11) permanecería sin relación con `EvaluationHarness`: `ExecutionBudget` sigue siendo, sin excepción, el contrato exclusivo de límites de consumo dentro de un run — pregunta ortogonal a certificar un candidato antes de que exista cualquier run |
| `EventBus` (ya existente, CMP-009) | podría distribuir, como un `AgentEvent` más, `EVALUATION_REPORT_PRODUCED`/`BUSINESS_OUTCOME_CORRELATED` (seccion 14) — exactamente igual que distribuye el de cualquier otro productor |

`registry/components.yaml` de `CMP-005`, `CMP-006`, `CMP-007`, `CMP-008` y `CMP-017` **no se modifica**
en este capítulo: ninguno agrega `CMP-020` a sus `dependencies`, y ninguno cambia su pseudocódigo. El
pseudocódigo de la seccion 11 muestra a `EvaluationHarness` evaluando un candidato y correlacionando un
run de forma completamente autónoma — sin que ningún componente anterior cambie una sola línea para
que este capítulo sea correcto. Ese cableado real de punta a punta es, explícitamente, trabajo de un
capítulo de integración futuro (ver seccion 18/19).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[Candidato — un agente, un prompt, una skill, un modelo, una policy o una capability, referenciado
opacamente, conceptual, nunca un run] → EvaluationHarness → [EvaluationReport — el resultado de
certificación, consultable por cualquier componente futuro vía subjectRef]

[AgentRun — ya completado o en curso, con su runId ya asignado, CH-00/CH-11, conceptual] →
EvaluationHarness → [BusinessOutcomeCorrelation — el outcome de negocio, consultable vía runId]
```

**Vista 2 — Sequence**

```text
Candidato (subjectRef, riskClass, certificationRequired ya resueltos — conceptual, sin
ExecutionContext propio necesariamente)
   │
   ▼
EvaluationHarness
   │ evaluateCandidateForPromotion(subjectRef, riskClass, certificationRequired,
   │   certificationSatisfied, execution, agentId)
   │ ¿subjectRef ausente? sí → HarnessError (EVALUATION_REPORT_MISSING_SUBJECT_REF)
   │ ¿certificationRequired? no → outcome = CERTIFIED
   │ ¿certificationRequired? sí, ¿certificationSatisfied ausente? sí → outcome = NEEDS_REVIEW
   │ ¿certificationRequired? sí, ¿certificationSatisfied = TRUE? sí → outcome = CERTIFIED
   │ ¿certificationRequired? sí, ¿certificationSatisfied = FALSE? sí → outcome = REJECTED
   │ construye EvaluationReport (id, subjectRef, riskClass, certificationRequired, outcome,
   │   evaluatedAt)
   │ ¿execution y agentId ambos resueltos? sí → emite: AgentEvent (EVALUATION_REPORT_PRODUCED)
   ▼
EvaluationReport (el resultado de certificación vigente para este subjectRef)

RunId (ya existente, run completado o en curso — conceptual)
   │
   ▼
EvaluationHarness
   │ correlateRunWithBusinessOutcome(runId, measuredOutcome, slaRef, humanEscalationRef,
   │   execution, agentId)
   │ ¿runId ausente? sí → HarnessError (BUSINESS_OUTCOME_CORRELATION_MISSING_RUN_ID)
   │ construye BusinessOutcomeCorrelation (id, runId, measuredOutcome, slaRef,
   │   humanEscalationRef, correlatedAt)
   │ ¿execution y agentId ambos resueltos? sí → emite: AgentEvent (BUSINESS_OUTCOME_CORRELATED)
   ▼
BusinessOutcomeCorrelation (la correlación de negocio vigente para este runId)
   │
   │ ... integración futura: CapabilityRegistry (CH-08) podría invocar
   │     evaluateCandidateForPromotion tras registrar una nueva versión; HumanInteractionService
   │     (CH-06) podría reaccionar a un outcome NEEDS_REVIEW; AuditLedger (CH-19) podría auditar el
   │     hecho de que una certificación concreta ocurrió; PolicyEngine (CH-05) seguiría, sin
   │     cambios, evaluando exclusivamente ToolCall dentro de runs ya existentes ...
```

**Vista 3 — Pseudocódigo**

Ver §11: `evaluateCandidateForPromotion` y `correlateRunWithBusinessOutcome` son la primera
formalización ejecutable de "production and evaluation are separate execution concerns" (`P-28`) y
"technical success does not imply business success" (`P-29`) — construidas exclusivamente a partir de
material que ya existe (`ExecutionContext`/`AgentEvent`/`HarnessError`/`RunId`/
`HumanInteractionRequestId` desde CH-00/CH-06) más los `ENUM`/`STRUCT` nuevos de este capítulo.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde CH-00/CH-06.

```pseudocode
FUNCTION evaluateCandidateForPromotion(
    subjectRef: Text,
    riskClass: RiskClass,
    certificationRequired: Boolean,
    certificationSatisfied: Optional<Boolean>,
    execution: Optional<ExecutionContext>,
    agentId: Optional<AgentId>
) -> EvaluationReport

    IF subjectRef == NULL OR subjectRef == ""
        missingSubjectRef: HarnessError = HarnessError(
            category = EVALUATION,
            code = "EVALUATION_REPORT_MISSING_SUBJECT_REF",
            message = "evaluateCandidateForPromotion fue invocada sin una referencia al candidato que se evalúa — un EvaluationReport nunca puede escribirse sin saber qué candidato certifica",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW missingSubjectRef
    END

    outcome: EvaluationOutcome = NEEDS_REVIEW

    IF certificationRequired == FALSE
        outcome = CERTIFIED
    ELSE
        IF certificationSatisfied == NULL
            outcome = NEEDS_REVIEW
        ELSE
            IF certificationSatisfied == TRUE
                outcome = CERTIFIED
            ELSE
                outcome = REJECTED
            END
        END
    END

    report: EvaluationReport = EvaluationReport(
        id = newEvaluationReportId(),
        subjectRef = subjectRef,
        riskClass = riskClass,
        certificationRequired = certificationRequired,
        outcome = outcome,
        evaluatedAt = now()
    )

    IF execution != NULL AND agentId != NULL
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = EVALUATION_REPORT_PRODUCED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = report
        )
    END

    RETURN report
END
```

`now()`, `newEventId()` son las mismas primitivas de CH-00..CH-21. `newEvaluationReportId()` sigue el
mismo patrón que `newExecutionPlacementId()` (CH-21) o `newDataGovernanceLabelId()` (CH-20).
`riskClass`, `certificationRequired` y `certificationSatisfied` llegan como parámetros ya resueltos
por una política de certificación externa — este capítulo modela la FORMA del resultado (nunca
`CERTIFIED`/`REJECTED` fabricados sin base), no un motor real que ejecute el candidato contra un
dataset de evaluación ni que calcule si su certificación ya se satisfizo; esa decisión real es,
deliberadamente, Preview, infraestructura de borde, en el mismo espíritu que
`dataGovernanceRuleFound`/`matchDataGovernanceRule` (CH-20 §11) o la asignación real de topología
(CH-21 §11) dejaron Preview sus propios motores reales.

**Por qué el valor por defecto de `outcome` es `NEEDS_REVIEW`, nunca `CERTIFIED`.** Mismo principio
fail-closed que `evaluatePolicyForToolCall` (CH-05, `DENY` por defecto) y `classifyData` (CH-20,
`RESTRICTED` por defecto) ya aplicaron a sus propios dominios: un candidato nunca se certifica por
omisión. La única forma de llegar a `CERTIFIED` es que la certificación no sea requerida, o que sí lo
sea y una señal real y explícita confirme que ya se satisfizo — nunca por ausencia de información.

```pseudocode
FUNCTION correlateRunWithBusinessOutcome(
    runId: RunId,
    measuredOutcome: Text,
    slaRef: Optional<Text>,
    humanEscalationRef: Optional<HumanInteractionRequestId>,
    execution: Optional<ExecutionContext>,
    agentId: Optional<AgentId>
) -> BusinessOutcomeCorrelation

    IF runId == NULL
        missingRunId: HarnessError = HarnessError(
            category = EVALUATION,
            code = "BUSINESS_OUTCOME_CORRELATION_MISSING_RUN_ID",
            message = "correlateRunWithBusinessOutcome fue invocada sin una referencia al run cuya ejecución se correlaciona — un BusinessOutcomeCorrelation nunca puede escribirse sin saber a qué run pertenece",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW missingRunId
    END

    correlation: BusinessOutcomeCorrelation = BusinessOutcomeCorrelation(
        id = newBusinessOutcomeCorrelationId(),
        runId = runId,
        measuredOutcome = measuredOutcome,
        slaRef = slaRef,
        humanEscalationRef = humanEscalationRef,
        correlatedAt = now()
    )

    IF execution != NULL AND agentId != NULL
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = BUSINESS_OUTCOME_CORRELATED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = correlation
        )
    END

    RETURN correlation
END
```

`newBusinessOutcomeCorrelationId()` sigue el mismo patrón que las primitivas anteriores.
`measuredOutcome`, `slaRef` y `humanEscalationRef` llegan como señales de entrada ya resueltas — este
capítulo no mide, por sí mismo, ningún outcome de negocio real, ni resuelve si un SLA/SLO concreto
aplica, ni decide si una escalación humana concreta pertenece a este run: eso es, deliberadamente,
Preview.

Nótese lo que ninguna de las dos funciones **nunca hace**: no invoca
`PolicyEngine.evaluatePolicyForToolCall` (CH-05) para autorizar ninguna acción — ninguna de las dos
recibe siquiera un `ToolCall`; no invoca `CapabilityRegistry.resolveCapability` (CH-08) para resolver
ninguna capability — `subjectRef` llega ya resuelto, opaco; no invoca `AuditLedger.recordAuditEntry`
(CH-19) para preservar evidencia inmutable — el `AgentEvent` que cada función emite es, como mucho,
una notificación, nunca el vehículo del resultado ni evidencia estructuralmente inmutable; y no invoca
`HumanInteractionService.createHumanInteractionRequest` (CH-06) cuando `outcome = NEEDS_REVIEW` — esa
reacción es, explícitamente, trabajo de un capítulo de integración futuro (seccion 9/18).

## 12. Transiciones de Estado (State Transitions)

Este capítulo no modifica `AgentRunStatus` (C-013): sigue siendo, sin cambios, el mismo `ENUM` de once
estados que `AgentLoop` (CH-01) formalizó.

Ni `EvaluationReport` ni `BusinessOutcomeCorrelation` declaran ningún `ENUM` de lifecycle propio, pero
cada uno se comporta de forma distinta ante una invocación repetida:

```text
(EvaluationReport recién producido para un subjectRef)
   → evaluateCandidateForPromotion(...)
     RETURN EvaluationReport — vigente para ese subjectRef hasta que una invocación posterior de
     evaluateCandidateForPromotion produzca uno nuevo

(el mismo subjectRef necesita reevaluarse más tarde — p. ej. nueva evidencia de certificación, o una
nueva versión del mismo candidato)
   → evaluateCandidateForPromotion(...) se invoca de nuevo, con el mismo subjectRef
     RETURN un EvaluationReport COMPLETAMENTE NUEVO (id distinto, evaluatedAt posterior) — el
     anterior nunca se edita ni se reemplaza in place; simplemente deja de ser el más reciente

(BusinessOutcomeCorrelation recién producido para un runId)
   → correlateRunWithBusinessOutcome(...)
     RETURN BusinessOutcomeCorrelation — una medición de negocio en un instante dado

(el mismo runId acumula una segunda medición más tarde — p. ej. valor de negocio medido en un
momento distinto tras la finalización del run)
   → correlateRunWithBusinessOutcome(...) se invoca de nuevo, con el mismo runId
     RETURN un segundo BusinessOutcomeCorrelation, con su propio id — AMBOS coexisten como
     mediciones legítimas del mismo run; a diferencia de EvaluationReport, ninguno vuelve
     obsoleto al otro
```

**Por qué `EvaluationReport` sigue el mismo argumento de reemplazo que `ExecutionPlacement` (CH-21
§12) y `DataGovernanceLabel` (CH-20 §12), mientras `BusinessOutcomeCorrelation` no.** Un
`EvaluationReport` describe LA certificación vigente para un candidato — solo una tiene sentido como
"la actual" en cualquier instante, así que una reevaluación reemplaza, en espíritu, a la anterior (sin
mutarla, produciendo una nueva instancia). Un `BusinessOutcomeCorrelation`, en cambio, describe UNA
medición de negocio en un instante — un mismo run puede, legítimamente, tener valor medido en
distintos momentos de su ciclo de vida de negocio (al completarse técnicamente, una semana después,
al cierre de un ciclo de facturación), y ninguna medición posterior invalida a la anterior: ambas son
hechos históricos igualmente válidos sobre el mismo run.

**Lo que este capítulo explícitamente no cierra**: ningún mecanismo registra, todavía, cuál
`EvaluationReport` es "el vigente" para un `subjectRef` dado cuando existen varios producidos en
momentos distintos, ni existe ningún registro agregado de "todas las correlaciones de negocio de un
runId" — ver seccion 18.

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6, extendido en la seccion 6 de este capítulo) clasifica también
los dos únicos fallos reales que introduce este capítulo:

```text
EVALUATION
    EVALUATION_REPORT_MISSING_SUBJECT_REF              — evaluateCandidateForPromotion fue invocada
                                                           sin una referencia al candidato evaluado
        → recoverable: FALSE, retryable: FALSE
    BUSINESS_OUTCOME_CORRELATION_MISSING_RUN_ID         — correlateRunWithBusinessOutcome fue
                                                           invocada sin una referencia al run
                                                           correlacionado
        → recoverable: FALSE, retryable: FALSE
```

Los dos fallos de este capítulo son `recoverable = FALSE` y `retryable = FALSE`: representan un uso
incorrecto de la propia invocación (una referencia obligatoria faltante) — no se corrigen reintentando
la misma operación tal cual, sino corrigiendo lo que se le provee. Dos códigos, uno por función, mismo
patrón que `IdempotencyGuard` (CH-17) y `DataGovernanceEngine` (CH-20) ya aplicaron cuando un capítulo
introduce dos funciones reales, cada una con exactamente una referencia obligatoria propia.

**La distinción más importante de esta sección**: ninguno de los dos fallos se clasifica como `POLICY`
(CH-05, propio de autorización de acciones dentro de un run) ni como `AUDIT` (CH-19, propio de
evidencia inmutable ya preservada) — aunque, en prosa informal, "certificar un candidato" y "autorizar
una acción" ambos suenen a "decidir si algo está permitido", la diferencia no es la forma del fallo, es
su naturaleza: `EVALUATION_REPORT_MISSING_SUBJECT_REF` y `BUSINESS_OUTCOME_CORRELATION_MISSING_RUN_ID`
son errores de uso de las propias funciones de este capítulo, nunca una `PolicyDecision` denegada ni un
`AuditRecord` corrupto — ese segundo y tercer tipo de fallo siguen siendo, sin ambigüedad, `POLICY` y
`AUDIT` respectivamente, exactamente como lo eran antes de este capítulo. El mismo argumento que ya
usaron CH-19 §13 (contra `CONTROL`/`VALIDATION`), CH-20 §13 (contra `CONTEXT`/`CREDENTIAL`) y CH-21 §13
(contra `BUDGET`/`INFRASTRUCTURE`).

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo real del motor de evaluación
—un candidato que no puede evaluarse porque el dataset de test no está disponible, una policy de
certificación que falla al ejecutarse— sigue, después de este capítulo, sin que `EvaluationHarness` lo
ejercite nunca (mismo límite que CH-14..CH-21 ya documentaron para sus propias primitivas asumidas).

## 14. Eventos Producidos (Events Produced)

`EvaluationHarness` emite `AgentEvent` de forma condicional desde sus dos funciones reales, agregando
`EVALUATION_REPORT_PRODUCED` y `BUSINESS_OUTCOME_CORRELATED` a `AgentEventType` (seccion 6), cada uno
emitido únicamente cuando `execution` y `agentId` llegan ambos resueltos (mismo patrón condicional que
`AuditLedger`, CH-19, `OperationalController`, CH-18, `DataGovernanceEngine`, CH-20, y
`ExecutionFabricAdapter`, CH-21).

**Por qué la emisión es condicional.** Mismo argumento que `ExecutionFabricAdapter` (CH-21 §14): un
`AgentEvent` (C-010) exige `runId`/`sessionId`/`agentId`/`traceId` genuinos, y no toda evaluación de un
candidato ocurre dentro de un `AgentRun` con esos cuatro campos ya resueltos — evaluar un agente antes
de su primer despliegue, por ejemplo, podría ocurrir sin que exista todavía ningún run cuyo
`ExecutionContext` referenciar.

**Por qué, incluso cuando emite, ninguno de los dos eventos es evidencia de auditoría — frontera
explícita con `AuditLedger` (CH-19).** `payload = report`/`payload = correlation` transporta una copia
del resultado ya producido — pero, exactamente igual que `EXECUTION_PLACEMENT_RESOLVED` (CH-21 §14),
queda sujeto a las mismas garantías (o ausencia de garantías) que cualquier otro `AgentEvent`:
`EventBus` podría distribuirlo, perderlo si nadie está suscrito, o nunca llegar a existir si
`execution`/`agentId` no estaban resueltos. Si alguien necesitara, en cambio, evidencia
estructuralmente inmutable de que una certificación o una correlación concretas ocurrieron, esa es,
sin ambigüedad, una responsabilidad de `AuditLedger` (CH-19) — nunca de estos eventos condicionales
(ver seccion 15).

**Por qué esto no es una limitación real hacia `INV-18`.** Las acciones verdaderamente significativas
de este capítulo —producir un `EvaluationReport` vigente para un candidato, producir un
`BusinessOutcomeCorrelation` para un run— ya se cumplen con el `RETURN` directo de cada función a
quien la invoca, sin depender de `AgentEvent`/`EventBus` para "existir". El `AgentEvent` condicional
es, aquí, una conveniencia de observabilidad adicional, nunca el mecanismo que hace el resultado real.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

`EvaluationHarness` es el primer componente de este libro cuya responsabilidad completa es evaluar un
candidato completo antes de que exista cualquier run, y correlacionar un run ya existente con un
resultado de negocio.

**La distinción con `PolicyEngine` (CH-05), explícita, completa y la más importante de este
capítulo.** `PolicyEngine.evaluatePolicyForToolCall` (CH-05) decide, contra reglas de policy
explícitas, si una acción concreta —un `ToolCall` ya propuesto— puede ejecutarse DENTRO de un run que
ya existe, con un `agentId` y un `runId` ya asignados. `EvaluationHarness.evaluateCandidateForPromotion`
(este capítulo) decide, sobre un candidato completo que todavía no tiene ningún run, si debería
promoverse a producción — una pregunta de `P-28`, completamente anterior en el tiempo y distinta en
objeto de la que resuelve `PolicyEngine`. Las dos preguntas son, literalmente, independientes: un
candidato puede estar `CERTIFIED` para producción y, sin embargo, cada acción concreta que su agente
proponga en cada run seguir evaluándose, una por una, por `PolicyEngine`; y, a la inversa, un candidato
`NEEDS_REVIEW` —todavía sin certificar— nunca debería llegar a producir ningún `ToolCall` real, porque
nunca debió promoverse en primer lugar. Si `PolicyEngine` absorbiera la certificación de candidatos —ya
que de todos modos está "evaluando" algo—, la separación que `P-28` exige ("Production and evaluation
are separate execution concerns") dejaría de ser real: cada evaluación de una acción tendría que, de
hecho, conocer el historial completo de certificación del candidato completo, exactamente el
acoplamiento que este principio prohíbe, el mismo argumento que CH-21 §15 ya aplicó, con matices
distintos, a la frontera entre `ExecutionController` y `ExecutionFabricAdapter`.

**La distinción con `CapabilityRegistry` (CH-08), precisa y necesaria.** `CapabilityRegistry.
resolveCapability` (CH-08) ya conoce, de primera mano, el `version` exacto de cada `CapabilityDescriptor`
registrado — pero CH-08 §8 nunca declaró la responsabilidad de decidir si esa versión debe certificarse
para producción; esa pregunta, hasta este capítulo, no tenía dueño. `EvaluationHarness` no reclasifica
jamás el registro de capabilities: recibe, en `subjectRef`, una referencia opaca que PUEDE apuntar a
una versión concreta ya registrada por `CapabilityRegistry`, sin necesitar conocer el catálogo completo
ni el mecanismo de resolución de esa versión. Confundir esta frontera llevaría a que
`CapabilityRegistry` tuviera que conocer, en el instante de registrar una nueva versión, el estado
completo de certificación de esa versión — información que, por diseño, pertenece a un momento y a un
dominio distintos.

**La distinción con `AuditLedger` (CH-19), heredada y aplicada aquí con un objeto nuevo.** Ambos
componentes producen algo sobre una decisión relacionada con gobierno — pero `AuditLedger` preserva,
de forma estructuralmente inmutable, evidencia de una decisión YA TOMADA por otro componente;
`EvaluationHarness` es quien TOMA la decisión de certificación en primer lugar. Confundir esta frontera
llevaría a que `EvaluationReport` tuviera que garantizar, por sí mismo, las mismas propiedades de
write-once que `AuditRecord` ya garantiza — una responsabilidad que, deliberadamente, este capítulo no
asume (ver seccion 12, donde un `EvaluationReport` se reemplaza, nunca se preserva para siempre).

**`P-13`, extendido a la certificación de candidatos con la misma disciplina que todo el libro.**
Ninguna de las dos funciones de este capítulo recibe ninguna entrada que el modelo haya producido — ni
siquiera de forma indirecta. El modelo no decide si él mismo, su propio prompt, o la policy que lo
gobierna deberían certificarse para producción, no puede solicitar su propia promoción, y no puede,
bajo ninguna circunstancia, observar o alterar un `EvaluationReport` o un `BusinessOutcomeCorrelation`
ya producidos — la ausencia total del modelo en el pseudocódigo de este capítulo es, otra vez, la
materialización directa del mismo argumento que `P-13` ya estableció para la autorización de acciones,
ahora aplicado, por primera vez con código real, a la certificación de candidatos completos y a la
correlación de negocio.

**Límite que este capítulo deja explícitamente abierto.** Ninguna de las dos funciones modela ningún
control de acceso sobre **quién** puede invocarlas, ni sobre **quién**, después, puede leer un
`EvaluationReport` o un `BusinessOutcomeCorrelation` ya producidos — cualquier llamador puede, en este
capítulo, producir una certificación para cualquier candidato, o correlacionar cualquier run con
cualquier outcome de negocio. Autorizar la escritura y la lectura de estos dos contratos (una pregunta
con implicaciones reales: un `EvaluationReport` de un candidato de riesgo crítico, o un
`BusinessOutcomeCorrelation` con datos de ingresos reales, pueden revelar información sensible sobre
un tenant, `INV-E07`) queda, explícitamente, fuera de alcance de este capítulo — el mismo límite que
`AuditLedger` (CH-19 §15), `DataGovernanceEngine` (CH-20 §15) y `ExecutionFabricAdapter` (CH-21 §15) ya
dejaron abierto para sus propios registros.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST EvaluateCandidateForPromotionRejectsAMissingSubjectRef
TEST EvaluateCandidateForPromotionReturnsCertifiedWhenCertificationIsNotRequired
TEST EvaluateCandidateForPromotionReturnsNeedsReviewWhenCertificationRequiredAndUnresolved
TEST EvaluateCandidateForPromotionReturnsRejectedWhenCertificationRequiredAndNotSatisfied
TEST EvaluateCandidateForPromotionReturnsCertifiedWhenCertificationRequiredAndSatisfied
TEST EvaluateCandidateForPromotionNeverDefaultsToCertifiedOnMissingInformation
TEST CorrelateRunWithBusinessOutcomeRejectsAMissingRunId
TEST CorrelateRunWithBusinessOutcomeNeverRequiresASlaRefOrHumanEscalationRef
TEST EvaluationHarnessNeverEvaluatesAToolCallWithinAnExistingRun
TEST EvaluationHarnessNeverProducesStructurallyImmutableAuditEvidence
TEST EvaluationReportOutcomeIsNeverReducedToTwoStates
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (después de CH-22 — los últimos tres principios de Amendment v1.1 nunca citados con
código real, P-28/P-29/INV-E13, materializados por primera vez)

Constitution
 ├── Article IV     — Decision Ownership (tabla original sin cambios; EvaluationHarness, como
 │                     DataGovernanceEngine/PolicyEngine/ExecutionFabricAdapter, decide algo real —
 │                     no comparte la ausencia de fila de EventBus/AuditLedger)
 └── Amendment v1.1 — Enterprise Activation, Interoperability and Operations
                       (P-28, P-29 e INV-E13 citados por primera vez con código real — las tres
                       únicas reglas de la enmienda que ningún capítulo anterior había citado, ni
                       siquiera en prosa; a diferencia de los nueve "Canonical Enterprise Planes",
                       ya completos desde CH-21, estas tres reglas no pertenecían a ninguno de esos
                       nueve planos)

Contracts (registry/contracts.yaml)
 ├── C-001..C-031  (sin cambios — CH-00..CH-21)
 ├── C-032 EvaluationReport              (CH-22, nuevo — el resultado de evaluar un candidato antes
 │                        de su promoción a producción, P-28/INV-E13/INV-19)
 └── C-033 BusinessOutcomeCorrelation    (CH-22, nuevo — la correlación entre un run y un outcome de
                          negocio medible, P-29/INV-19)

Components (registry/components.yaml)
 ├── CMP-001..CMP-019  (sin cambios — CH-01..CH-21)
 └── CMP-020 EvaluationHarness  (CH-22, nuevo — noveno componente de este registry que no
                          corresponde a ninguno de los once nombres de Article III; a diferencia de
                          los ocho anteriores, no pertenece a ninguno de los nueve planos canónicos
                          de Amendment v1.1)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado real hacia `CapabilityRegistry`, `PolicyEngine`, `HumanInteractionService` y
  `AuditLedger`**: ningún componente anterior invoca todavía, de verdad,
  `evaluateCandidateForPromotion` ni `correlateRunWithBusinessOutcome` — la demostración de la
  seccion 11 prueba que el mecanismo funciona, no que ya esté conectado dentro de un flujo real.
- **Cuál `EvaluationReport` es "el vigente"** para un `subjectRef` dado cuando existen varios
  producidos en momentos distintos: asumido, no construido (mismo límite que `registeredCapabilities`,
  CH-08, o el "vigente" de `ExecutionPlacement`, CH-21 §18, ya documentaron para sus propios registros
  asumidos).
- **Un registro agregado de todas las correlaciones de negocio de un `runId`**: este capítulo modela
  cómo producir UNA correlación, no un catálogo consultable de todas las que existan para un run dado.
- **El motor real de evaluación**: correr un candidato contra un dataset de test real, calcular
  métricas reales de calidad, seguridad o comportamiento — este capítulo modela la forma del
  resultado (`EvaluationReport`), no un motor real de evaluación — Preview, infraestructura de borde.
- **La política real de certificación por clase de riesgo**: quién decide, en la práctica, qué
  evidencia exige la certificación de un candidato `HIGH` frente a uno `CRITICAL` — asumido como una
  señal de entrada ya resuelta (`certificationSatisfied`), no como un motor de reglas real.
- **La medición real de un outcome de negocio**: cómo se calcula, en la práctica, el valor, el
  cumplimiento de un SLA/SLO, o si una escalación humana concreta debería asociarse a un run —
  asumido, no construido.
- **Autorización de lectura/escritura sobre los propios `EvaluationReport`/`BusinessOutcomeCorrelation`**:
  quién puede producir o consultar cualquiera de los dos — señalado explícitamente en la seccion 15, no
  resuelto (mismo límite abierto que `AuditLedger`, CH-19 §15, `DataGovernanceEngine`, CH-20 §15, y
  `ExecutionFabricAdapter`, CH-21 §15, dejaron para sus propios registros). `INV-E07` (aislamiento por
  tenant) tampoco se modela aquí.
- **Auditar una certificación o una correlación con `AuditLedger`**: ningún cableado real conecta
  todavía `EvaluationHarness` con `recordAuditEntry` (CH-19).
- **`INV-E12`, la única regla de la Constitution que sigue sin citarse con código real después de
  este capítulo**: verificado con el mismo barrido completo descrito en la apertura de este capítulo,
  `INV-E12` ("A human handoff transfers a structured HandoffPackage rather than only prose") es, tras
  CH-22, la única de las sesenta y cuatro reglas de la Constitution (Article original + Amendment
  v1.1) que ningún capítulo de este libro ha citado nunca, ni con código ni en prosa. Resolverla está,
  deliberadamente, fuera del alcance decidido para este capítulo — se señala aquí, explícitamente,
  como lo que de verdad queda pendiente, en vez de reclamar una cobertura constitucional completa que
  todavía no existe.
- Reviewers plurales, evals reales y orquestación multi-agente propiamente dicha: explícitamente fuera
  de alcance de BH-v0.1.

## 19. Siguiente Incremento (Next Increment)

Con este capítulo, sesenta y tres de las sesenta y cuatro reglas de la Constitution (Article original
más Amendment v1.1) tienen, cada una, al menos un capítulo real de este libro que las cita con código
—`P-28`, `P-29` e `INV-E13` fueron las últimas tres en cerrarse—. El problema natural del próximo
incremento tiene dos caminos igualmente legítimos: cablear, por fin, alguno de los puntos de
integración que este capítulo y los ocho anteriores de Amendment v1.1 dejaron explícitamente como
deuda (seccion 18); o resolver `INV-E12` ("A human handoff transfers a structured HandoffPackage
rather than only prose") — la única regla que queda, conectando naturalmente con
`HumanInteractionService` (CH-06), el componente que ya representa y resuelve una intervención humana,
pero cuyo contrato de resolución (`HumanInteractionResolution`, C-016) nunca fue diseñado, todavía,
para transportar un paquete estructurado de traspaso en vez de solo prosa.

`next_chapter` queda en `null` en el frontmatter de este capítulo porque, en este momento del libro,
ese próximo capítulo todavía no existe como archivo — solo como el problema que motivaría su
escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg / Bucles
> de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows),
> secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): `P-28`, `P-29` e `INV-E13` nunca fueron citadas con código
   real, ni siquiera en prosa, por ningún capítulo anterior — y ninguna de las tres pertenece a
   ninguno de los nueve "Canonical Enterprise Planes" que CH-21 ya había declarado completos.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): completar una
   taxonomía de planos (CH-21) puede leerse, por error, como completar la cobertura de principios —
   un plano y un principio no son la misma unidad de cobertura, y una regla constitucional completa
   puede seguir sin ningún dueño incluso después de que su propio plano parezca "cerrado".
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `EvaluationHarness` con una ficha que declara tanto lo que posee (`owns`: evaluar un candidato
   completo antes de producción, aplicar la certificación de riesgo, correlacionar negocio) como lo
   que explícitamente NO posee (`does_not_own`: evaluar una acción dentro de un run — `PolicyEngine`,
   CH-05).
4. **Modelos mentales** (= §4, Constitutional Impact): "evaluar" no es una sola pregunta — es, como
   mínimo, dos preguntas con objeto, momento y dueño distintos, y el éxito técnico de un run nunca
   implica, por sí solo, su éxito de negocio.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un componente nuevo resuelve una pregunta que "suena"
  a evaluación —autorizar una acción (CH-05), clasificar un dato (CH-20)— crece la tentación de asumir
  que "evaluar un candidato antes de producción" ya quedó cubierto por alguno de esos dos, hasta que
  una organización necesita, de verdad, certificar una versión nueva de un agente o de una capability.
- **Bucle de equilibrio (estabiliza):** `evaluateCandidateForPromotion` (§11) nunca colapsa su
  resultado a dos estados cuando la certificación exigida no puede resolverse todavía — produce
  `NEEDS_REVIEW` por defecto, cerrando, con el mismo principio fail-closed que ya protegió la
  autorización desde CH-05 y la infraestructura de ejecución desde CH-21, el bucle que este capítulo
  abre.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `EvaluationReport` y `BusinessOutcomeCorrelation`
sean contratos completamente autónomos de `AgentLoop.runTurn` (CH-01) y de
`PolicyEngine.evaluatePolicyForToolCall` (CH-05) — ningún run necesita que exista una certificación
previa para ejecutarse, y ninguna acción necesita conocer el historial de certificación de su propio
agente para autorizarse. Mantener ambos contratos independientes, referenciados por
`subjectRef`/`runId`, es la forma en que este capítulo hace real la separación de `P-28` por diseño de
contratos, no solo por convención documentada.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo de
> esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set` (frontmatter) y
> es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa, para lectura directa
> del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Ya existe un componente que evalúa si una acción concreta dentro de un run que ya existe puede
   ejecutarse. ¿Es la misma pregunta que decidir si un candidato completo debería promoverse a
   producción, o son preguntas de dominios distintos? *(cierra la pregunta guía 1)*
2. Ya existe un contrato que registra la versión de cada capability. ¿Le corresponde a ese mismo
   registro decidir si una versión debe certificarse para producción? *(cierra la pregunta guía 2)*
3. Si la clase de riesgo de un candidato determina si necesita certificación, ¿ese resultado debería
   reducirse siempre a dos estados, o existe un tercero legítimo? *(cierra la pregunta guía 3)*
4. Un run puede terminar sin ningún error técnico. ¿Eso garantiza, por sí solo, que produjo valor de
   negocio? *(cierra la pregunta guía 4)*

### Explicar

1. `EvaluationHarness` posee decidir si un candidato completo debería promoverse a producción.
   Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee decidir si una acción
   concreta puede ejecutarse dentro de un run ya en marcha.
2. `EvaluationReport.outcome` puede valer `CERTIFIED`, `REJECTED` o `NEEDS_REVIEW`. Explica qué
   problema aparecería si un capítulo futuro eliminara `NEEDS_REVIEW`.

### Conectar

1. `PolicyEngine.evaluatePolicyForToolCall` (CH-05) ya evalúa acciones con código real. ¿Le
   correspondería a esa misma función certificar, además, si el propio agente puede correr en
   producción?
2. `CapabilityRegistry` (CH-08) ya declara una versión explícita para cada capability. ¿Le
   correspondería a ese registro decidir, también, si esa versión debe certificarse?
3. `HumanInteractionService` (CH-06) ya representa y resuelve una intervención humana. Si una
   correlación de negocio necesita registrar que hubo una escalación, ¿basta con referenciar la
   solicitud que ese componente ya produjo, o hace falta un mecanismo nuevo?

### Espaciar

Las cinco tarjetas de repaso de este capítulo (dos sobre `EvaluationHarness` — su `owns` y su
`does_not_own` —, una sobre `EvaluationReport` — sus campos y por qué `certificationRequired` sí puede
ser `Boolean` mientras `outcome` no —, una sobre `BusinessOutcomeCorrelation` — sus campos y la
reutilización de `HumanInteractionRequestId` —, y una sobre la frontera con `PolicyEngine`) entran hoy
en `reviewStage = DAY_1`. Repásalas de nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) — ver
el apéndice de tarjetas al final del libro (edición PDF) o `retrieval_set.flashcards` en
`dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te equivocaste,
ese es precisamente el punto ciego que este método existe para revelar.
