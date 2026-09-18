# Plan / Registro de ejecución — Capítulo 22: EvaluationHarness y la Certificación de un Candidato Antes de que Exista Ningún Run

**Fecha:** 2026-09-18
**Estado:** ✅ Completado, sobre el estado dejado por `94d8211` (CH-00..CH-21 como los veintidós únicos
capítulos reales; los once componentes de Article III + dos capítulos de integración + los nueve
componentes/planos de Amendment v1.1 ya cubiertos — `AdmissionController` CH-14,
`AgentCommunicationGateway` CH-15, `CredentialBroker` CH-16, `IdempotencyGuard` CH-17,
`OperationalController` CH-18, `AuditLedger` CH-19, `DataGovernanceEngine` CH-20,
`ExecutionFabricAdapter` CH-21).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-18-capitulo-21-execution-fabric-adapter.md` (precedente inmediato: mismo tratamiento
  editorial para un componente de Amendment v1.1 sin nombre literal previo — con la diferencia
  explícita de que este capítulo SÍ tiene, en `P-28`, una cita casi literal de su propio nombre)
- `2026-09-14-capitulo-05-policy-engine.md` (la frontera más importante a trazar: `PolicyEngine` ya
  evalúa ACCIONES dentro de un run que ya existe; este capítulo evalúa CANDIDATOS antes de que
  exista ningún run)
- `2026-09-14-capitulo-08-capability-registry.md` (`CapabilityDescriptor.version`, `P-26` — un
  candidato a certificar es, con frecuencia, una nueva versión de una capability ya registrada)
- `2026-09-18-capitulo-19-audit-ledger.md` (`AuditLedger` produce evidencia inmutable de una
  decisión YA TOMADA; `EvaluationHarness` es quien toma esa decisión, nunca la audita de forma
  inmutable)
- `2026-09-14-capitulo-06-human-interaction-service.md` (`HumanInteractionRequestId`, reusado
  opacamente por `BusinessOutcomeCorrelation.humanEscalationRef`, sin tocar `HumanInteractionRequest`)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Amendment v1.1 — `P-28`/`P-29`/`INV-E13`, líneas
  978-987)

---

## 1. Objetivo

Escribir el vigesimotercer capítulo real de contenido del libro, CH-22 — el noveno componente de
este registry que no corresponde a ninguno de los once nombres de Article III, y el que cierra las
últimas tres reglas de la Constitution (Article original + Amendment v1.1) que ningún capítulo
anterior había citado nunca, ni con código ni en prosa: `P-28` ("Production and evaluation are
separate execution concerns"), `P-29` ("Business outcomes are first-class observability") e
`INV-E13` ("Production promotion requires certification policy where risk class requires it").

**Verificación de la premisa central, ejecutada antes de escribir una sola línea del capítulo**: un
barrido programático (`grep`/Python, ver seccion 4) sobre el texto íntegro de los veintidós
`chapter.md` anteriores confirmó que `P-28`, `P-29` e `INV-E13` no aparecen ni una sola vez fuera de
la transcripción de Amendment v1.1 en CH-00 — y que, contrario a lo que la carga del encargo daba por
sentado implícitamente, existe una CUARTA regla en la misma situación: `INV-E12` ("A human handoff
transfers a structured HandoffPackage rather than only prose"). Esta cuarta regla se documenta
explícitamente en el capítulo (seccion 18/19) como lo único que queda pendiente tras CH-22, sin
expandir el alcance decidido de este capítulo para resolverla — honestidad de cobertura en vez de una
afirmación de "Constitution 100% cubierta" que habría sido falsa.

## 2. Alcance (decisión ya tomada antes de escribir, confirmada en el resultado)

Exactamente **1 componente + 2 contratos**:

1. **`EvaluationHarness`** (`CMP-020`) — a diferencia de los ocho componentes de Amendment v1.1
   anteriores (todos sintetizados por este libro, sin nombre literal en la Constitution), `P-28`
   nombra casi textualmente este componente ("evaluable in an **Evaluation Harness**") — la
   capitalización canónica es la única transformación editorial aplicada. `owns`: evaluar cualquier
   candidato (agente/prompt/skill/modelo/policy/capability) ANTES de su promoción controlada a
   producción (`P-28` literal); aplicar/verificar la policy de certificación que la `riskClass` de
   un candidato exige (`INV-E13` literal); correlacionar la ejecución de un run con un outcome de
   negocio medible, un SLA/SLO aplicable y una posible escalación humana (`P-29` literal).
   `does_not_own` (frontera trazada contra seis componentes ya existentes): evaluar/autorizar una
   ACCIÓN dentro de un run ya en curso (`PolicyEngine`, `CMP-005`, CH-05 — la frontera más importante:
   `PolicyEngine` decide si UNA ACCIÓN puede ocurrir DENTRO de un run que ya existe;
   `EvaluationHarness` decide si UN CANDIDATO debe promoverse a producción ANTES de que exista
   ningún run); producir evidencia de auditoría inmutable (`AuditLedger`, `CMP-017`, CH-19); registrar
   versiones de capability (`CapabilityRegistry`, `CMP-008`, CH-08); decidir continuación operacional
   de un run (`ExecutionController`, `CMP-007`, CH-07); representar/resolver la intervención humana
   que `NEEDS_REVIEW` exige (`HumanInteractionService`, `CMP-006`, CH-06); aplicar kill switches
   (`OperationalController`, `CMP-016`, CH-18).
2. **`EvaluationReport`** (`C-032`) — `id`, `subjectRef: Text` (opaco, mismo patrón que
   `AuditRecord`/`DataGovernanceLabel` — universo heterogéneo, nunca un identificador fuerte como
   `RunId`), `riskClass: RiskClass` (`ENUM` de cuatro valores `LOW`/`MEDIUM`/`HIGH`/`CRITICAL`,
   mismo tamaño de escala que `DataClassificationLevel`, CH-20), `certificationRequired: Boolean`
   (evaluado y documentado explícitamente por qué SÍ puede ser `Boolean` — propiedad binaria de la
   policy de certificación vigente, nunca el resultado de la decisión misma), `outcome:
   EvaluationOutcome` (`ENUM` de tres valores `CERTIFIED`/`REJECTED`/`NEEDS_REVIEW`, nunca reducido a
   dos), `evaluatedAt: Timestamp`.
3. **`BusinessOutcomeCorrelation`** (`C-033`) — `id`, `runId: RunId` (identificador YA EXISTENTE,
   mismo argumento que `ExecutionPlacement.runId`, CH-21 — universo homogéneo, siempre exactamente un
   run), `measuredOutcome: Text` (deliberadamente opaco, no `Number` ni una `STRUCT Metric`
   estructurada — fuera de alcance construir un sistema de métricas completo), `slaRef:
   Optional<Text>` (referencia opaca a un SLA/SLO aplicable), `humanEscalationRef:
   Optional<HumanInteractionRequestId>` (reutiliza el identificador fuerte que
   `HumanInteractionService`, CH-06, ya produce, en vez de un campo nuevo en
   `HumanInteractionRequest` — decisión evaluada explícitamente y documentada en el propio capítulo),
   `correlatedAt: Timestamp`.
4. **Pseudocódigo**: `evaluateCandidateForPromotion(subjectRef, riskClass, certificationRequired,
   certificationSatisfied, execution, agentId) -> EvaluationReport` (fail-closed hacia
   `EVALUATION_REPORT_MISSING_SUBJECT_REF`; `outcome` por defecto `NEEDS_REVIEW`, nunca `CERTIFIED`,
   mismo principio fail-closed que `evaluatePolicyForToolCall`, CH-05, y `classifyData`, CH-20) y
   `correlateRunWithBusinessOutcome(runId, measuredOutcome, slaRef, humanEscalationRef, execution,
   agentId) -> BusinessOutcomeCorrelation` (fail-closed hacia
   `BUSINESS_OUTCOME_CORRELATION_MISSING_RUN_ID`) — ambas completamente autónomas, sin invocar ni
   modificar `PolicyEngine`, `CapabilityRegistry`, `AuditLedger` ni `HumanInteractionService`. Se
   documenta en prosa (seccion 9/18) que ningún componente anterior invoca todavía ninguna de las dos
   funciones — deuda de integración explícita, patrón ya establecido por CH-09..CH-21.
5. `consumes: [C-004]`, `produces: [C-010, C-011, C-032, C-033]` — ningún componente previo editado
   (`CMP-001`..`CMP-019` intactos, incluidos `CMP-005 PolicyEngine`, `CMP-006
   HumanInteractionService`, `CMP-007 ExecutionController`, `CMP-008 CapabilityRegistry` y `CMP-017
   AuditLedger`); `registry/contracts.yaml` no modifica ningún `STRUCT`/`ENUM` existente (`C-014
   PolicyDecision`, `C-015 HumanInteractionRequest` y `C-018 CapabilityDescriptor` quedan intactos);
   `book/chapters/21-execution-fabric-adapter/chapter.md` solo recibió `next_chapter: CH-22`.
6. `EvaluationHarness` emite `AgentEvent` desde dos funciones distintas
   (`EVALUATION_REPORT_PRODUCED`, `BUSINESS_OUTCOME_CORRELATED`), condicionalmente: solo cuando
   `execution`/`agentId` llegan ambos resueltos — y se documenta explícitamente (seccion 14) que
   ninguno de los dos eventos es nunca evidencia de auditoría inmutable (frontera con `AuditLedger`,
   CH-19).

## 3. Corrección/precisión editorial explícita sobre CH-21

CH-21 declaró, con razón, los nueve "Canonical Enterprise Planes" de Amendment v1.1 completamente
cubiertos. Este capítulo precisa esa cuenta, sin contradecirla: un plano canónico y un principio
constitucional no son la misma unidad de cobertura. `P-28`, `P-29` e `INV-E13` no pertenecen a
ninguno de los nueve planos que CH-21 cerró — permanecieron, hasta este capítulo, completamente
huérfanos de cualquier cobertura, plano o no. La apertura del propio capítulo (§0/§1) construye este
argumento explícitamente para que no se lea como una inconsistencia con CH-21, sino como una precisión
necesaria sobre qué significa "cerrado".

## 4. Verificación ejecutada (evidencia concreta)

```
Verificación de la premisa (antes de escribir):
  grep -c "P-28\|P-29\|INV-E13" book/chapters/*/chapter.md sobre constitutional_articles → 0 en los
  22 capítulos anteriores, confirmado también con un barrido Python sobre el texto íntegro de cada
  chapter.md (no solo frontmatter) — resultado adicional: INV-E12 también queda sin citar (ver
  seccion 1/18 del capítulo).

./scripts/validate-contracts                                              → OK (33 contratos)
./scripts/validate-components                                             → OK (20 componentes)
./scripts/validate-chapter book/chapters/22-evaluation-harness            → OK a la primera
    (22/19 secciones, 9 bloques pseudocode, 2 contratos introducidos, 1 componente introducido)
./scripts/validate-retrieval-set book/chapters/22-evaluation-harness      → OK a la primera
    (guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2, interleavedQuestions: 3
    — CH-05/CH-08/CH-06 — flashcards: 5, calibrationPairs: 4)
./scripts/validate-chapter book/chapters/21-execution-fabric-adapter      → OK (revalidado tras
    el único cambio de navegación permitido, next_chapter: CH-22)
rm -rf dist && ./scripts/build-all                                        → exit 0
```

23 capítulos reales, todos pasando `validate-chapter`/`validate-retrieval-set`. `build-mind-map`:
`chapter-22.diagram` con 149 nodos/229 aristas — más que `chapter-21.diagram` (141 nodos/217 aristas),
como exige la verificación. Se leyó `scripts/lib/render-diagram.js` (fix de Ghostscript, CH-16) antes
de empezar y no se encontró ningún problema real que justificara modificarlo.

**Web**: `dist/web/chapters/CH-22.html` con SVG inline (`grep -c '<svg'` = 1 en las 23 páginas,
verificado una por una), anchors `id="CMP-020"`/`id="C-032"`/`id="C-033"` presentes, navegación
CH-21↔CH-22 verificada en ambos sentidos (`href="CH-22.html"` desde CH-21, `href="CH-21.html"` desde
CH-22). Anchors clave de capítulos anteriores (`CMP-001` en CH-01, `CMP-005` en CH-05, `CMP-008` en
CH-08, `CMP-011` en CH-11, `CMP-017` en CH-19, `CMP-018` en CH-20, `CMP-019` en CH-21) intactos.

**PDF**: con `pypdf`, 597 páginas — más que el build de referencia de 22 capítulos (561 páginas).
Texto extraído de las últimas 40 páginas contiene, verificado programáticamente,
"EvaluationHarness", "EvaluationReport" y "BusinessOutcomeCorrelation".

**Prueba negativa real**: se renombró el campo obligatorio `does_not_own` de `CMP-020` a
`does_not_own_BROKEN` en `registry/components.yaml` (edición dirigida solo a la ficha de `CMP-020`,
sin tocar los otros diecinueve componentes). `./scripts/validate-components` falló con `exit 1` y el
mensaje exacto `Componente CMP-020: falta el campo obligatorio "does_not_own"`; `rm -rf dist &&
./scripts/build-all` se detuvo en la etapa de validación con `exit 1` real (confirmado con
`${PIPESTATUS[0]}`, no inferido de un pipe) y `policies/publishing.yaml:
unresolved_validation_errors = deny → build detenido.`, sin construir `dist/`. Se restauró el campo
desde una copia de respaldo (`cp registry/components.yaml` previo), se confirmó
`validate-components: OK (20 componente(s))`, y se reconstruyó todo desde cero: mismos 23 capítulos,
33 contratos, 20 componentes, mismos nodos/aristas por capítulo (149/229 en CH-22), mismo número de
páginas de PDF (597) — conteos idénticos al build previo a la prueba negativa.

## 5. Decisiones de diseño no cubiertas en el encargo original

- **`certificationRequired: Boolean` justificado explícitamente frente a `RiskClass`/
  `EvaluationOutcome`, ambos `ENUM`**: el encargo pedía documentar por qué este campo sí puede ser
  `Boolean` — se desarrolló como el argumento central de la sección 6/§5 del capítulo: es una
  propiedad YA DETERMINADA de la policy vigente para una `riskClass` dada (binaria por definición de
  la propia policy, no una decisión que este componente tome), mientras `outcome` es el RESULTADO de
  una decisión que legítimamente puede no resolverse todavía.
- **`humanEscalationRef: Optional<HumanInteractionRequestId>`, tipado fuerte, en vez de una referencia
  opaca `Text`**: se evaluó explícitamente el patrón opaco (`subjectRef`-like) y se descartó porque
  `HumanInteractionRequestId` ya existe como identificador fuerte desde CH-06 — mismo argumento que ya
  justificó `ExecutionPlacement.runId` tipado (CH-21) frente a un `Text` opaco.
- **`measuredOutcome: Text`, no `Number` ni una `STRUCT Metric`**: documentado explícitamente por qué
  un sistema de métricas de negocio completo queda fuera de alcance — el mismo tratamiento que
  `computeResourceRef`/`residencyRequirement` (`Optional<Text>`) ya dieron a un detalle real en
  capítulos anteriores.
- **Hallazgo no anticipado por el encargo**: `INV-E12` también permanece sin citar tras este
  capítulo — verificado con un barrido Python independiente sobre las 64 reglas de la Constitution
  (Article original + Amendment v1.1) contra el texto íntegro de los 22 capítulos anteriores. Se
  documenta explícitamente en la seccion 18/19 del capítulo como lo único pendiente, sin expandir el
  alcance de CH-22 para resolverlo — decisión editorial de honestidad de cobertura, consistente con
  la instrucción de no reabrir el alcance ya decidido.
- **Frontera con `CapabilityRegistry` (CH-08) vía `subjectRef` opaco, sin dependencia declarada**: se
  evaluó explícitamente que `EvaluationHarness` consumiera `CapabilityDescriptor` como dependencia
  formal — se descartó porque el candidato llega siempre como una referencia opaca ya resuelta,
  preservando la independencia de contratos que el resto del libro ya exige.
- **`AgentEventType` con dos valores nuevos** (`EVALUATION_REPORT_PRODUCED`,
  `BUSINESS_OUTCOME_CORRELATED`), uno por función real — mismo patrón que `IdempotencyGuard` (CH-17)
  y `DataGovernanceEngine` (CH-20).

## 6. Deuda intencional hacia el próximo capítulo

- **El cableado real hacia `CapabilityRegistry`, `PolicyEngine`, `HumanInteractionService` y
  `AuditLedger`**: ningún componente anterior invoca todavía, de verdad, `evaluateCandidateForPromotion`
  ni `correlateRunWithBusinessOutcome`.
- **Cuál `EvaluationReport` es "el vigente"** para un `subjectRef` dado cuando existen varios: no
  modelado, Preview — mismo límite abierto que "cuál `ExecutionPlacement` es el vigente" (CH-21 §18).
- **Un registro agregado de todas las correlaciones de negocio de un `runId`**: no construido.
- **El motor real de evaluación y la política real de certificación por clase de riesgo**: asumidos
  como señales de entrada ya resueltas, no construidos — Preview, infraestructura de borde.
- **La medición real de un outcome de negocio**: asumida, no construida.
- **Autorización de lectura/escritura sobre `EvaluationReport`/`BusinessOutcomeCorrelation`**, e
  `INV-E07`: no resuelto — mismo límite abierto que `AuditLedger` (CH-19) y `DataGovernanceEngine`
  (CH-20) dejaron para sus propios registros.
- **Auditar una certificación o una correlación con `AuditLedger`**: ningún cableado real.
- **`INV-E12`** ("A human handoff transfers a structured HandoffPackage rather than only prose"): la
  única regla de la Constitution que sigue sin citarse con código real tras este capítulo — candidato
  natural para el próximo incremento, conectando con `HumanInteractionService` (CH-06).

## 7. Nota de cierre — sesenta y tres de sesenta y cuatro reglas constitucionales, citadas

Con CH-22, sesenta y tres de las sesenta y cuatro reglas de la Constitution (Article original +
Amendment v1.1) tienen, cada una, al menos un capítulo real de este libro que las cita con código
real. Solo `INV-E12` permanece, verificado programáticamente, sin ninguna cita — ni con código, ni en
prosa — en ningún capítulo de este libro.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
