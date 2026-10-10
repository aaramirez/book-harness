---
id: CH-47
title: "Medir el Aporte de un Cambio: Evaluación con Lift"
starting_version: "0.2.1"
ending_version: "0.3"
introduces_components: []
introduces_contracts: [C-064]
modifies_contracts: [C-032]
constitutional_articles: [P-28, P-29, INV-19, INV-E07, INV-E13]
previous_chapter: CH-46
next_chapter: CH-48
retrieval_set:
  expected_outcome:
    id: EO-CH47
    text: |
      Al terminar este capítulo podrás decidir si un cambio mejora al agente frente a la versión
      anterior, con casos suficientes y corridas aisladas, y explicar cómo esa comparación se convierte
      en la evidencia de una certificación.
  skeleton:
    id: SK-CH47
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
    components_to_be_introduced: []
    contracts_to_be_introduced: [C-064]
  guiding_questions:
    - id: GQ-CH47-01
      text: |
        Si cambias el prompt de un agente y en tres pruebas le va mejor, ¿ya puedes decir que el cambio
        lo mejora? ¿Qué te falta saber?
      answered_by: RQ-CH47-01
    - id: GQ-CH47-02
      text: |
        Si la versión vieja y la nueva corren en el mismo entorno, una después de la otra, ¿qué podría
        salir mal en la comparación?
      answered_by: RQ-CH47-02
    - id: GQ-CH47-03
      text: |
        Si la diferencia entre las dos versiones es muy chica, ¿deberías decir que mejoró, que empeoró o
        ninguna de las dos?
      answered_by: RQ-CH47-03
    - id: GQ-CH47-04
      text: |
        ¿Cómo debería pesar una comparación así en la decisión de llevar el cambio a producción?
      answered_by: RQ-CH47-04
  systems_lens:
    iceberg_visible_fact: |
      EvaluationHarness certifica un candidato a partir de una señal que llega ya resuelta, y no hay
      forma gobernada de medir si un cambio mejora al agente frente a la versión anterior: se promueve
      lo que "parece andar mejor" en unas pocas pruebas (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que un puntaje aislado no dice nada sin una línea base, y una
      comparación sin aislamiento ni casos suficientes confunde el cambio con el ruido: las corridas se
      contaminan entre sí y una diferencia chica se lee como mejora (ver sección 3).
    iceberg_structures: |
      Este capítulo introduce LiftReport (C-064), lleva EvaluationReport (C-032) a v2 con evidence, y
      le da a EvaluationHarness el cálculo del lift con corridas aisladas y la traducción del lift en la
      señal de certificación de CH-22 (ver sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-28 (evaluar antes de promover), INV-E13 (certificar según la clase de
      riesgo), INV-E07 (aislamiento) e INV-19 (cada decisión crítica se traza hasta su evidencia) (ver
      sección 4).
    reinforcing_loop: |
      Si se promueve lo que parece andar mejor en pocas pruebas, algunos cambios que no mejoran nada
      llegan a producción; como "pasaron la evaluación", la confianza en la evaluación crece justo
      cuando menos lo merece, y se prueba cada vez menos.
    balancing_loop: |
      El umbral mínimo y el mínimo de casos son el equilibrio: una diferencia chica o con pocos casos
      queda INCONCLUSIVE, y un cambio solo se certifica cuando el lift supera el ruido.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que LiftReport (C-064) sea la evidencia de la
      certificación: una comparación pareada, con corridas aisladas, casos suficientes y tres veredictos,
      reemplaza la señal sin origen que recibía evaluateCandidateForPromotion.
  recall_questions:
    - id: RQ-CH47-01
      text: |
        ¿Cómo calcula computeLift el lift, y qué veredicto da si hay menos casos que el mínimo?
    - id: RQ-CH47-02
      text: |
        ¿Qué verifica requireIsolatedCase, qué verifica computeLift entre casos distintos, y qué error
        produce si se viola?
    - id: RQ-CH47-03
      text: |
        ¿Qué tres veredictos puede dar liftVerdict, y con qué comparaciones contra minimumLift?
    - id: RQ-CH47-04
      text: |
        ¿Qué señal de certificación devuelve certificationSignalFromLift para una regresión, para todos
        IMPROVED y para el resto, y qué EvaluationOutcome produce cada una?
  explain_prompts:
    - id: EP-CH47-01
      text: |
        EvaluationHarness ya decidía si un candidato se certifica. Explica, como si hablaras con alguien
        sin contexto técnico, por qué medir el lift también le pertenece, y por qué no hace falta un
        componente nuevo.
      target_entity: CMP-020
    - id: EP-CH47-02
      text: |
        Explica por qué un informe de lift necesita una línea base, los mismos casos, corridas aisladas y
        un umbral, y qué podría salir mal si faltara cualquiera de los cuatro.
      target_entity: C-064
  interleaved_questions:
    - id: IQ-CH47-01
      text: |
        En CH-22, evaluateCandidateForPromotion recibía certificationSatisfied ya resuelto y nunca
        fabricaba CERTIFIED sin base. ¿De dónde sale ahora esa señal, qué valor toma cuando la evidencia
        no alcanza, y qué resultado produce eso?
      current_chapter_entities: [C-064]
      prior_chapter_entities: [C-032, CMP-020]
      prior_chapter: CH-22
  flashcards:
    - id: FC-CH47-01
      front: |
        ¿Qué es LiftReport (C-064)?
      back: |
        El informe de una comparación pareada: línea base y tratamiento, métrica, puntajes por caso con
        sus entornos aislados, lift (diferencia de medias), umbral y veredicto (IMPROVED, INCONCLUSIVE,
        REGRESSED).
      source_entity: C-064
      chapter_introduced_in: CH-47
      review_stage: DAY_1
    - id: FC-CH47-02
      front: |
        ¿Qué agrega EvaluationReport v2 (C-032)?
      back: |
        evidence: los LiftReport en los que se apoya el resultado. Si falta, se lee como lista vacía,
        como en v1.
      source_entity: C-032
      chapter_introduced_in: CH-47
      review_stage: DAY_1
    - id: FC-CH47-03
      front: |
        ¿Por qué cada corrida de una evaluación va en su propio entorno aislado?
      back: |
        Porque dos corridas en el mismo entorno pueden contaminarse (archivos, caché, estado). computeLift
        rechaza un informe en el que dos corridas comparten SandboxId.
      source_entity: C-064
      chapter_introduced_in: CH-47
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH47-01
      recall_question: RQ-CH47-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH47-02
      recall_question: RQ-CH47-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH47-03
      recall_question: RQ-CH47-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH47-04
      recall_question: RQ-CH47-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 47 — Medir el Aporte de un Cambio: Evaluación con Lift

> **Regla constitucional (INV-E13):** la promoción a producción exige una política de certificación
> cuando la clase de riesgo lo requiere. Este capítulo le da evidencia.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir si un cambio mejora al agente frente a
la versión anterior, con casos suficientes y corridas aisladas. También podrás explicar cómo esa
comparación se convierte en la evidencia de una certificación.

**Esqueleto.** Noveno capítulo de la versión 0.3. No introduce componentes: agrega `LiftReport`, lleva
`EvaluationReport` a v2 y amplía `EvaluationHarness`.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si cambias el prompt de un agente y en tres pruebas le va mejor, ¿ya puedes decir que el cambio lo
   mejora? ¿Qué te falta saber?
2. Si la versión vieja y la nueva corren en el mismo entorno, una después de la otra, ¿qué podría salir
   mal en la comparación?
3. Si la diferencia entre las dos versiones es muy chica, ¿deberías decir que mejoró, que empeoró o
   ninguna de las dos?
4. ¿Cómo debería pesar una comparación así en la decisión de llevar el cambio a producción?

## 1. Arquitectura Actual (Current Architecture)

- **`EvaluationHarness` (CMP-020, CH-22)** evalúa un candidato antes de su promoción.
  `evaluateCandidateForPromotion` produce un `EvaluationReport` (C-032) con tres resultados posibles:
  `CERTIFIED`, `REJECTED` o `NEEDS_REVIEW`.
- **La señal `certificationSatisfied` llega ya resuelta:** CH-22 modeló la forma del resultado, no de
  dónde sale la señal.
- **`IsolatedExecutionEnvironment` (CMP-026, CH-35)** abre un `SandboxSession` (C-047) por sesión,
  aislado de los demás.
- **`RiskClass`** (LOW, MEDIUM, HIGH, CRITICAL) decide si hace falta certificación (INV-E13).

## 2. El Problema (Problem)

Un equipo cambia el prompt de su agente de facturación. Lo prueban con tres preguntas, le va mejor que
antes y lo promueven. Una semana después, la tasa de facturas mal clasificadas sube. Hoy:
- **no hay línea base:** "le va mejor" no dice frente a qué, ni en qué métrica;
- **tres casos son ruido:** cualquier diferencia en tres casos puede ser azar;
- **las dos versiones corrieron en el mismo entorno:** la segunda encontró archivos y caché que dejó la
  primera;
- **una diferencia chica se leyó como mejora:** no había umbral;
- **la certificación no tiene evidencia:** `certificationSatisfied = TRUE` no dice de dónde salió.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **Un puntaje aislado no dice nada:** hace falta compararlo con la versión anterior sobre los mismos
  casos.
- **Sin aislamiento, la comparación mide el entorno, no el cambio.**
- **Sin mínimo de casos ni umbral, el ruido se lee como mejora.**
- **Sin evidencia en el informe, la certificación no se puede trazar** (INV-19).
- **No hace falta un componente nuevo:** evaluar candidatos antes de producción ya es de
  `EvaluationHarness` (P-28, EVO-01).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-28   Production and evaluation are separate execution concerns.
           Las corridas de evaluación van en entornos propios, nunca en los de producción.
    P-29   Business outcomes are first-class observability.
           La métrica de un LiftReport puede ser un outcome de negocio (CH-22).

Invariants preserved
    INV-19   Toda decisión crítica se traza hasta su evidencia: EvaluationReport.evidence.
    INV-E07  Aislamiento: cada corrida en su propio entorno (requireIsolatedCase).
    INV-E13  Production promotion requires certification policy where risk class requires it.
             certificationSignalFromLift le da a la certificación una señal con origen.

Component ownership changes
    Ninguno nuevo. EvaluationHarness gana el cálculo del lift y su traducción en certificación.

Contract changes
    Nuevo: C-064 LiftReport.
    C-032 EvaluationReport v1 → v2 (+ evidence).

Observability implications
    Nuevo AgentEventType: LIFT_REPORT_PRODUCED.
```

## 5. Conceptos Nuevos (New Concepts)

- **Línea base y tratamiento:** la versión actual (baseline) y la versión con el cambio (treatment).
- **Comparación pareada:** las dos versiones corren sobre los mismos casos y se puntúan con la misma
  métrica, caso por caso.
- **Lift:** la media de los puntajes del tratamiento menos la media de los de la línea base. Positivo
  si mejora.
- **Umbral mínimo:** la diferencia por debajo de la cual el lift se considera ruido.
- **Mínimo de casos:** con menos casos, ningún lift alcanza para decidir.
- **Tres veredictos:** `IMPROVED` (el lift supera el umbral), `REGRESSED` (empeora más que el umbral) e
  `INCONCLUSIVE` (todo lo demás).
- **Corrida aislada:** cada corrida, de cada versión, en cada caso, en su propio entorno aislado.
- **Evidencia de la certificación:** los informes de lift en los que se apoya un `EvaluationReport`.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `EvaluationReport` (C-032, que pasa a v2), `ExecutionContext` (C-004),
  `AgentEvent` (C-010), `HarnessError` (C-011);
- **primitivos:** `LiftReportId`, `EvaluationReportId`, `SandboxId`, `AgentId`, `Timestamp`.

| Identificador | Rol en este capítulo |
|---|---|
| `LiftReportId` | id de un informe de lift; nuevo primitivo |
| `EvaluationReportId` | CH-22 §6: id de un `EvaluationReport` |
| `SandboxId` | CH-35 §6: id de un entorno aislado |
| `RiskClass` | CH-22 §6: LOW, MEDIUM, HIGH, CRITICAL |
| `EvaluationOutcome` | CH-22 §6: CERTIFIED, REJECTED, NEEDS_REVIEW |
| `AgentEventType` | se agrega `LIFT_REPORT_PRODUCED` |
| `ErrorCategory` | reutiliza `EVALUATION` (CH-22) |

### `LiftVerdict` (embebido)

```pseudocode
ENUM LiftVerdict
    IMPROVED
    INCONCLUSIVE
    REGRESSED
END
```

### `CaseScore` — un caso, dos corridas (embebido)

```pseudocode
STRUCT CaseScore
    caseId: Text
    baselineScore: Number
    treatmentScore: Number
    baselineSandboxId: SandboxId
    treatmentSandboxId: SandboxId
END
```

Cada puntaje lleva el entorno aislado en que se obtuvo: el aislamiento queda como dato, no como
promesa.

### `LiftReport` — la comparación (C-064)

```pseudocode
STRUCT LiftReport
    reportId: LiftReportId
    baselineRef: Text
    treatmentRef: Text
    metric: Text
    scores: List<CaseScore>
    lift: Number
    minimumLift: Number
    verdict: LiftVerdict
    isolationRef: Text
    producedAt: Timestamp
END
```

- `baselineRef` y `treatmentRef` usan la misma forma que `EvaluationReport.subjectRef` (CH-22).
- `isolationRef` es el entorno base con que se abrieron todas las corridas (`environmentRef`, CH-35).

### `EvaluationReport` — versión 2 (C-032)

```pseudocode
STRUCT EvaluationReport
    id: EvaluationReportId
    subjectRef: Text
    riskClass: RiskClass
    certificationRequired: Boolean
    outcome: EvaluationOutcome
    evaluatedAt: Timestamp
    evidence: List<LiftReportId>
END
```

**Compatibilidad hacia atrás:** un `EvaluationReport` sin `evidence` se lee con la lista vacía, como en
CH-22..CH-46.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

```text
ID:                     C-064
Name:                   LiftReport
Version:                v1
Introduced In:          CH-47
Used By:                [CMP-020]
Constitutional Impact:  [P-28, INV-19, INV-E07, INV-E13]
```

```text
C-032 EvaluationReport  v1 → v2   Modified By: [CH-47]
                        + evidence: List<LiftReportId>
```

`CaseScore` y `LiftVerdict` quedan embebidos.

## 8. Responsabilidades de Componentes (Component Responsibilities)

**Este capítulo no introduce componentes.** `EvaluationHarness` gana funciones dentro de su `owns`
literal:

```text
EvaluationHarness (CMP-020)
    owns: evaluar cualquier candidato antes de su promoción (P-28); aplicar la certificación según
          la clase de riesgo, con NEEDS_REVIEW cuando no puede resolverse (INV-E13)
    nuevas:
        requireIsolatedCase, computeLift, liftVerdict, certificationSignalFromLift,
        evaluateCandidateWithLift
    no posee:
        ejecutar el candidato ni puntuarlo (el ejecutor de evaluaciones, un adaptador)
        abrir los entornos aislados (IsolatedExecutionEnvironment, CH-35)
        promover a producción (el despliegue, CH-45, y los comandos operacionales, CH-18)
```

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
Por cada caso y cada versión:
    sesión de evaluación propia → openSandboxSession (CH-35) → SandboxSession propio
    el ejecutor corre la versión y puntúa con la métrica → puntaje + SandboxId
Con todos los casos:
    computeLift → requireIsolatedCase por caso, SandboxId sin repetir → liftVerdict → LiftReport
                → LIFT_REPORT_PRODUCED
Certificación:
    evaluateCandidateWithLift → certificationSignalFromLift → evaluateCandidateForPromotion (CH-22)
                              → EvaluationReport v2 (evidence)
```

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
ejecutor de evaluaciones → IsolatedExecutionEnvironment (un entorno por corrida) → puntajes
EvaluationHarness.computeLift → LiftReport → evaluateCandidateWithLift → EvaluationReport v2
```

**Vista 2 — Sequence: el nuevo prompt de facturación**

```text
baseline "prompt-v3", treatment "prompt-v4", métrica "factura bien clasificada", 200 casos
   │ 400 corridas, cada una en su SandboxSession (sb-1 … sb-400)
   │ computeLift: media baseline 0,81, media treatment 0,84 → lift 0,03
   │ minimumLift 0,02, mínimo de casos 100 → IMPROVED      → LIFT_REPORT_PRODUCED
   ▼ evaluateCandidateWithLift(prompt-v4, HIGH, certificación requerida, [lr-1])
   │ certificationSignalFromLift = TRUE → CERTIFIED, evidence [lr-1]
```

**Vista 2b — Sequence: tres casos**

```text
3 casos, lift 0,15 → menos casos que el mínimo → INCONCLUSIVE
   → certificationSignalFromLift = NULL → NEEDS_REVIEW (CH-22)
```

**Vista 2c — Sequence: un entorno compartido**

```text
caso c-7: baselineSandboxId = treatmentSandboxId = sb-9 → SHARED_EVALUATION_ENVIRONMENT
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

```pseudocode
FUNCTION requireIsolatedCase(
    score: CaseScore
) -> CaseScore

    IF score.baselineSandboxId == score.treatmentSandboxId
        THROW HarnessError(
            category = EVALUATION,
            code = "SHARED_EVALUATION_ENVIRONMENT",
            message = "La línea base y el tratamiento de un caso corrieron en el mismo entorno aislado",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN score
END
```

```pseudocode
FUNCTION liftVerdict(
    lift: Number,
    minimumLift: Number,
    caseCount: Integer,
    minimumCases: Integer
) -> LiftVerdict

    IF caseCount < minimumCases
        RETURN INCONCLUSIVE
    END

    IF lift >= minimumLift
        RETURN IMPROVED
    END

    IF lift <= 0 - minimumLift
        RETURN REGRESSED
    END

    RETURN INCONCLUSIVE
END
```

```pseudocode
FUNCTION computeLift(
    baselineRef: Text,
    treatmentRef: Text,
    metric: Text,
    scores: List<CaseScore>,
    minimumLift: Number,
    minimumCases: Integer,
    isolationRef: Text,
    execution: Optional<ExecutionContext>,
    agentId: Optional<AgentId>
) -> LiftReport

    IF baselineRef == treatmentRef
        THROW HarnessError(
            category = EVALUATION,
            code = "SAME_BASELINE_AND_TREATMENT",
            message = "Una comparación necesita dos versiones distintas",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    IF length(scores) == 0
        THROW HarnessError(
            category = EVALUATION,
            code = "EMPTY_EVALUATION",
            message = "Una comparación sin casos no tiene lift",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    seen: List<SandboxId> = []
    baselineValues: List<Number> = []
    treatmentValues: List<Number> = []

    FOR EACH score IN scores
        requireIsolatedCase(score)

        IF contains(seen, score.baselineSandboxId) OR contains(seen, score.treatmentSandboxId)
            THROW HarnessError(
                category = EVALUATION,
                code = "SHARED_EVALUATION_ENVIRONMENT",
                message = "Dos corridas de casos distintos comparten entorno aislado",
                recoverable = FALSE,
                retryable = FALSE,
                metadata = {}
            )
        END

        seen = append(append(seen, score.baselineSandboxId), score.treatmentSandboxId)
        baselineValues = append(baselineValues, score.baselineScore)
        treatmentValues = append(treatmentValues, score.treatmentScore)
    END

    lift: Number = mean(treatmentValues) - mean(baselineValues)

    report: LiftReport = LiftReport(
        reportId = newLiftReportId(),
        baselineRef = baselineRef,
        treatmentRef = treatmentRef,
        metric = metric,
        scores = scores,
        lift = lift,
        minimumLift = minimumLift,
        verdict = liftVerdict(lift, minimumLift, length(scores), minimumCases),
        isolationRef = isolationRef,
        producedAt = now()
    )

    IF execution != NULL AND agentId != NULL
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = LIFT_REPORT_PRODUCED,
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

```pseudocode
FUNCTION certificationSignalFromLift(
    reports: List<LiftReport>
) -> Optional<Boolean>

    IF length(reports) == 0
        RETURN NULL
    END

    allImproved: Boolean = TRUE

    FOR EACH report IN reports
        IF report.verdict == REGRESSED
            RETURN FALSE
        END
        IF report.verdict != IMPROVED
            allImproved = FALSE
        END
    END

    IF allImproved
        RETURN TRUE
    END

    RETURN NULL
END
```

```pseudocode
FUNCTION evaluateCandidateWithLift(
    subjectRef: Text,
    riskClass: RiskClass,
    certificationRequired: Boolean,
    reports: List<LiftReport>,
    execution: Optional<ExecutionContext>,
    agentId: Optional<AgentId>
) -> EvaluationReport

    evidence: List<LiftReportId> = []

    FOR EACH report IN reports
        IF report.treatmentRef != subjectRef
            THROW HarnessError(
                category = EVALUATION,
                code = "LIFT_REPORT_NOT_OF_SUBJECT",
                message = "Un informe de lift evalúa otro tratamiento, no este candidato",
                recoverable = FALSE,
                retryable = FALSE,
                metadata = {}
            )
        END
        evidence = append(evidence, report.reportId)
    END

    base: EvaluationReport = evaluateCandidateForPromotion(
        subjectRef, riskClass, certificationRequired, certificationSignalFromLift(reports), NULL, NULL
    )

    report: EvaluationReport = EvaluationReport(
        id = base.id,
        subjectRef = base.subjectRef,
        riskClass = base.riskClass,
        certificationRequired = base.certificationRequired,
        outcome = base.outcome,
        evaluatedAt = base.evaluatedAt,
        evidence = evidence
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

Utilidades primitivas: `length`, `contains`, `append`, `mean` (media aritmética), `newLiftReportId`,
`newEventId` y `now`.

`evaluateCandidateForPromotion` (CH-22) no cambia: se la llama sin contexto para que no emita su
evento, y `evaluateCandidateWithLift` emite el mismo `EVALUATION_REPORT_PRODUCED` con el informe v2.

**Por qué un solo informe `INCONCLUSIVE` deja todo en `NEEDS_REVIEW`:** la certificación se apoya en
toda la evidencia. Si una métrica mejora y otra no se puede decidir, una persona tiene que mirar
(CH-22). Solo una regresión decide sola: una regresión nunca se certifica.

Nótese lo que estas funciones **no** hacen:
- ninguna ejecuta el candidato ni lo puntúa: eso lo hace el ejecutor de evaluaciones;
- ninguna abre entornos: verifican que cada corrida tuvo el suyo;
- ninguna promueve a producción: producen evidencia para quien decide.

## 12. Transiciones de Estado (State Transitions)

`AgentRunStatus` no cambia. De los informes al resultado:

```text
sin informes                       → señal NULL  → NEEDS_REVIEW (si hace falta certificación)
algún REGRESSED                    → señal FALSE → REJECTED
todos IMPROVED                     → señal TRUE  → CERTIFIED
algún INCONCLUSIVE, ningún REGRESSED → señal NULL  → NEEDS_REVIEW
certificación no requerida (CH-22) → CERTIFIED, con la evidencia que haya
```

## 13. Semántica de Fallos (Failure Semantics)

Códigos nuevos de `HarnessError`, con una `ErrorCategory` ya existente (`EVALUATION`, CH-22):

```text
EVALUATION  SHARED_EVALUATION_ENVIRONMENT  recoverable: FALSE, retryable: FALSE
EVALUATION  SAME_BASELINE_AND_TREATMENT    recoverable: FALSE, retryable: FALSE
EVALUATION  EMPTY_EVALUATION               recoverable: FALSE, retryable: FALSE
EVALUATION  LIFT_REPORT_NOT_OF_SUBJECT     recoverable: FALSE, retryable: FALSE
```

- Un entorno compartido invalida el informe entero: no se descarta el caso en silencio, porque la
  contaminación pudo afectar a otros.
- Pocos casos o un lift chico no son errores: son `INCONCLUSIVE`.
- Una corrida que falla al ejecutarse es un puntaje de la métrica (por ejemplo, 0), que decide el
  ejecutor; no se omite.

## 14. Eventos Producidos (Events Produced)

```text
LIFT_REPORT_PRODUCED        — se produjo un informe de lift (payload: LiftReport)
EVALUATION_REPORT_PRODUCED  — (CH-22) ahora con payload EvaluationReport v2, con evidence
```

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **Ningún cambio se certifica por parecer mejor:** hace falta un lift sobre el umbral con casos
  suficientes.
- **Una regresión nunca se certifica,** aunque otras métricas mejoren.
- **La evaluación no contamina producción ni a sí misma:** cada corrida tiene su entorno aislado, sin
  credenciales (CH-35, INV-E20).
- **Cada certificación se puede trazar hasta sus informes** (INV-19): `evidence` los nombra.
- **Los casos de evaluación son datos:** su clasificación sigue las reglas de CH-20, y un informe con
  casos sensibles se gobierna como cualquier dato derivado (CH-42).

## 16. Tests (Tests)

```text
TEST LiftIsTheDifferenceOfMeans
TEST FewerCasesThanMinimumIsInconclusive
TEST LiftAboveThresholdIsImproved
TEST LiftBelowNegativeThresholdIsRegressed
TEST SmallLiftIsInconclusive
TEST SharedSandboxWithinACaseIsRejected
TEST SharedSandboxAcrossCasesIsRejected
TEST SameBaselineAndTreatmentIsRejected
TEST EmptyEvaluationIsRejected
TEST AnyRegressionRejects
TEST AllImprovedCertifies
TEST InconclusiveLeadsToNeedsReview
TEST ReportOfAnotherSubjectIsRejected
TEST EvaluationReportCarriesTheLiftReportIds
TEST ReportWithoutEvidenceBehavesAsV1
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (v0.3 en curso, después de CH-47) — 29 componentes, 64 contratos, 48 capítulos

Components — 29, sin cambios
 └── CMP-020 EvaluationHarness   (+ lift pareado con corridas aisladas, evidencia de certificación)

Contracts — 64
 ├── C-032 EvaluationReport v2   (CH-22 → modificado en CH-47: evidence)
 └── C-064 LiftReport            (CH-47)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **Pruebas estadísticas** (intervalos de confianza, significancia): el umbral y el mínimo de casos
  son la versión más simple de "no confundir ruido con mejora"; una prueba estadística es otra forma
  de calcular el veredicto, con la misma estructura. No es deuda.
- **Cómo se puntúa un caso** (un juez automático, una regla, una persona): es del ejecutor de
  evaluaciones. No es deuda.
- **Evaluar en producción con tráfico real** (canarios, A/B): es despliegue, no evaluación previa, y
  P-28 los separa. No es deuda.
- **Elegir y versionar el conjunto de casos:** es un dato del equipo; el informe lo referencia por sus
  `caseId`. No es deuda.

## 19. Siguiente Incremento (Next Increment)

Ahora un cambio puede medirse antes de llegar a producción. Pero un agente sigue siendo una
configuración repartida en código, registros y archivos sin una forma convencional: no hay un lugar
donde **leer** qué es un agente, ni un diagnóstico que impida activarlo si está mal escrito.

El siguiente capítulo introduce **el agente como directorio**:
- un `AgentManifest` que dice de qué archivos está hecho un agente y de dónde vino cada parte;
- un `AuthoringDiagnostic` con nivel, código y ruta;
- INV-E27: un diagnóstico de nivel ERROR impide activar ese agente.

Será CH-48 ("El Agente como Directorio"). `next_chapter` queda en `null` porque CH-48 todavía no
existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): se promueve lo que parece andar mejor en pocas pruebas, sin línea base ni
   aislamiento.
2. **Patrones** (= §3): un puntaje aislado no dice nada, y sin aislamiento ni umbral el ruido se lee
   como mejora.
3. **Estructuras** (= §8): `LiftReport` (C-064), `EvaluationReport` v2 y funciones nuevas en
   `EvaluationHarness`.
4. **Modelos mentales** (= §4): P-28, INV-E13, INV-E07 e INV-19.

**Bucles de retroalimentación**

- **Refuerzo:** promover sin evidencia hace crecer una confianza que no se merece.
- **Equilibrio:** el umbral y el mínimo de casos. Un cambio solo se certifica cuando el lift supera el
  ruido.

**Punto de apalancamiento**

La decisión con mayor efecto es que `LiftReport` (C-064) sea la evidencia de la certificación:
reemplaza la señal sin origen que recibía `evaluateCandidateForPromotion`.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Cómo calcula `computeLift` el lift, y qué veredicto da si hay menos casos que el mínimo?
   *(pregunta guía 1)*
2. ¿Qué verifica `requireIsolatedCase`, qué verifica `computeLift` entre casos distintos, y qué error
   produce si se viola? *(pregunta guía 2)*
3. ¿Qué tres veredictos puede dar `liftVerdict`, y con qué comparaciones contra `minimumLift`?
   *(pregunta guía 3)*
4. ¿Qué señal de certificación devuelve `certificationSignalFromLift` para una regresión, para todos
   IMPROVED y para el resto, y qué `EvaluationOutcome` produce cada una? *(pregunta guía 4)*

### Explicar

1. `EvaluationHarness` ya decidía si un candidato se certifica. Explica por qué medir el lift también
   le pertenece, y por qué no hace falta un componente nuevo.
2. Explica por qué un informe de lift necesita una línea base, los mismos casos, corridas aisladas y un
   umbral, y qué podría salir mal si faltara cualquiera de los cuatro.

### Conectar

1. En CH-22, `evaluateCandidateForPromotion` recibía `certificationSatisfied` ya resuelto y nunca
   fabricaba `CERTIFIED` sin base. ¿De dónde sale ahora esa señal, qué valor toma cuando la evidencia
   no alcanza, y qué resultado produce eso?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
