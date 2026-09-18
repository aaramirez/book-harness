---
id: CH-26
title: "Integración Enterprise: el Camino Feliz de una Activación Admitida y Gobernada"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: []
introduces_contracts: []
modifies_contracts: []
constitutional_articles: [P-04, P-05, P-10, P-12, P-13, P-16, P-17, P-22, P-24, P-25, INV-06, INV-07, INV-08, INV-09, INV-11, INV-18, INV-19, INV-20, INV-E01, INV-E02, INV-E07, INV-E08, INV-E09, INV-E10, INV-E11]
previous_chapter: CH-25
next_chapter: CH-27
retrieval_set:
  expected_outcome:
    id: EO-CH26
    text: |
      Al terminar este capítulo podrás verificar, para cualquier turno gobernado de nivel
      enterprise que arranca en una activación externa cruda y termina en una respuesta admitida,
      clasificada, resuelta con una credencial real y protegida contra doble ejecución, exactamente
      qué componente de Amendment v1.1 resuelve cada paso adicional sobre el camino feliz que
      CH-12 ya dejó cableado — y podrás diagnosticar, para `AdmissionController`,
      `DataGovernanceEngine`, `SkillLibrary`, `CredentialBroker`, `IdempotencyGuard` y
      `AuditLedger`, si la deuda de integración que cada uno documentó, por su cuenta, en su propia
      sección 18, ya se cerró con una llamada real dentro de una misma ejecución, o si sigue siendo
      una demostración aislada.
  skeleton:
    id: SK-CH26
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
    contracts_to_be_introduced: []
  guiding_questions:
    - id: GQ-CH26-01
      text: |
        Un componente ya decide, con código real, si una activación externa cruda debería
        siquiera convertirse en un intento de ejecución — pero su propia decisión nunca puede
        expresarse como el tipo de evento observable que el resto de este libro ya sabe
        distribuir, porque en el instante de esa decisión todavía no existe ninguna ejecución a la
        que ese evento pudiera pertenecer. ¿Qué mecanismo, distinto del que ya distribuye eventos,
        podría preservar esa decisión de todas formas?
      answered_by: RQ-CH26-01
    - id: GQ-CH26-02
      text: |
        Un componente ya sabe resolver "qué herramienta ejecutar" a partir de una propuesta cruda
        del modelo, y otro componente distinto ya sabe resolver "qué procedimiento aplica" a partir
        del nombre de una situación — sin que ninguno de los dos pueda producir el resultado del
        otro. ¿En qué momento de un mismo turno tendría sentido consultar a ambos, y por qué
        consultarlos en el orden equivocado no ayudaría a nada?
      answered_by: RQ-CH26-02
    - id: GQ-CH26-03
      text: |
        Antes de que una acción con efectos reales sobre el mundo externo se ejecute, dos
        preguntas distintas —"¿con qué secreto exactamente?" y "¿ya se ejecutó esto antes bajo
        esta misma clave?"— ya tienen, cada una, un componente real que sabe responderlas. ¿En qué
        orden deberían responderse esas dos preguntas respecto a la autorización que ya decidió
        que la acción está permitida, y respecto a la ejecución real de la acción misma?
      answered_by: RQ-CH26-03
    - id: GQ-CH26-04
      text: |
        Un fragmento de contexto ya fue seleccionado como relevante y ya fue autorizado a que el
        modelo lo vea, antes de que exista ningún componente que decida qué reglas de gobierno de
        datos le aplican. ¿En qué punto exacto de la construcción de lo que el modelo va a ver
        debería ocurrir esa clasificación, para que nunca dependa de que el modelo mismo decida
        cómo tratar ese fragmento?
      answered_by: RQ-CH26-04
  systems_lens:
    iceberg_visible_fact: |
      CH-14, CH-16, CH-17, CH-19, CH-20 y CH-24 —seis capítulos de Amendment v1.1— demostraron,
      cada uno por su cuenta, una función real que resolvía correctamente su propia pregunta con
      datos de ejemplo, aislada del resto del libro. Ninguno de los seis fue invocado jamás dentro
      de la traza real de un `AgentRun` completo que CH-12/CH-13 ya dejaron cableada — ver sección
      2, El Problema.
    iceberg_patterns: |
      El mismo patrón que CH-12 §2 ya describió para los once componentes de Article III se
      repitió, capítulo a capítulo, para los seis componentes de Amendment v1.1 que este capítulo
      cablea: cada uno cerró su propia demostración con la misma disciplina de *ownership*, y dejó,
      con la misma honestidad, una nota explícita en su propia sección 18 señalando exactamente qué
      llamada real faltaba (ver sección 3).
    iceberg_structures: |
      Este capítulo no instala ningún componente nuevo — instala una función de integración nueva
      y propia, `runGovernedEnterpriseTurn` (sección 11), que invoca, con datos reales fluyendo
      entre sí, las funciones que CH-14/CH-16/CH-17/CH-19/CH-20/CH-24 ya publicaron —
      `evaluateAdmissionForActivationRequest`, `classifyData`, `resolveSkillForSituation`,
      `resolveCredentialReference`, `checkIdempotency`, `recordIdempotentExecution` y
      `recordAuditEntry`— entrelazadas con las mismas funciones que CH-12 ya cableó
      (`activateAgent`, `assembleContextSnapshot`, `invokeModelForTurn`, `runTurn`,
      `resolveModelProposedToolCall`, `evaluatePolicyForToolCall`, `executeToolCall`,
      `emitAndDistribute`, `createOrUpdateSessionCheckpoint`) — sin modificar el código publicado
      de ninguno de los diecisiete (ver sección 8).
    iceberg_mental_models: |
      El modelo mental es, literalmente, el mismo que CH-12 §4 ya estableció para los once
      componentes de Article III, aplicado ahora a los seis primeros componentes reales de
      Amendment v1.1: el Ownership Rule nunca exigió que estos seis componentes se ignoraran entre
      sí ni con el runtime de Article III para siempre — exigió que cada uno declarara su frontera
      antes de que existiera código real que pudiera cruzarla. Con las seis fronteras ya
      declaradas, componerlas dentro de una única ejecución no viola ninguna.
    reinforcing_loop: |
      Cada capítulo de Amendment v1.1 que se escribió sin cablearse de verdad hacia el runtime de
      Article III hizo crecer, capítulo a capítulo, la misma lista de "deuda intencional hacia un
      capítulo de integración futuro" que CH-12 §2 ya describió para los once componentes
      originales — seis capítulos más señalando el mismo problema, sin que ninguno lo cerrara,
      porque cerrarlo no era su propio alcance decidido.
    balancing_loop: |
      `runGovernedEnterpriseTurn` (sección 11) es, otra vez, el mecanismo de equilibrio: en cada
      punto nuevo (¿la activación fue admitida?, ¿qué gobierno le aplica a este fragmento?, ¿esta
      ejecución ya ocurrió antes?) invoca la función real que ya sabe responder esa pregunta, y se
      detiene explícitamente cuando el resultado no es el más permisivo, dejando ese resto para el
      capítulo siguiente (sección 18/19).
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `AuditLedger.recordAuditEntry` (CH-19)
      se invoque con `execution = NULL` para la `AdmissionDecision` — antes de que exista cualquier
      `ExecutionContext` real. Esa única llamada resuelve, con código real, la tensión que CH-14
      §14 documentó honestamente ("este es el primer componente real del libro cuya función
      principal nunca construye un `AgentEvent`, porque `runId`/`sessionId`/`agentId`/`traceId` no
      son `Optional`"): `AuditLedger` es, precisamente, el mecanismo que Amendment v1.1 (P-25)
      exige para una decisión anterior a que cualquier `AgentRun` exista — algo que `EventBus`, por
      diseño, nunca podría prometer.
  recall_questions:
    - id: RQ-CH26-01
      text: |
        ¿Qué componente resuelve la pregunta de si una activación externa debería siquiera
        convertirse en un intento de ejecución, y qué mecanismo —distinto de `EventBus`— preserva
        esa decisión aunque todavía no exista ningún `ExecutionContext` real?
      answered_by: RQ-CH26-01
    - id: RQ-CH26-02
      text: |
        ¿En qué momento del turno se consulta `SkillLibrary.resolveSkillForSituation`, respecto a
        cuándo se consulta `CapabilityRegistry.resolveModelProposedToolCall`, y qué produce cada
        uno que el otro nunca podría producir?
      answered_by: RQ-CH26-02
    - id: RQ-CH26-03
      text: |
        Antes de `ToolRuntime.executeToolCall`, ¿en qué orden se invocan
        `CredentialBroker.resolveCredentialReference` e `IdempotencyGuard.checkIdempotency`, y qué
        decide si `executeToolCall` llega a invocarse siquiera?
      answered_by: RQ-CH26-03
    - id: RQ-CH26-04
      text: |
        ¿En qué punto exacto de `assembleContextSnapshot` (CH-04) hasta que el modelo ve un
        `ContextBlock`, este capítulo invoca `DataGovernanceEngine.classifyData`, y qué campo real
        de `ContextBlock` usa como procedencia?
      answered_by: RQ-CH26-04
  explain_prompts:
    - id: EP-CH26-01
      text: |
        `AdmissionController.evaluateAdmissionForActivationRequest` (CH-14) nunca cambia una sola
        línea en este capítulo, y sin embargo este capítulo demuestra, por primera vez, que su
        `AdmissionDecision` puede preservarse como evidencia real aunque `EventBus` no pueda
        transportarla. Explica, como si hablaras con alguien sin contexto técnico, por qué
        `AuditLedger` puede hacer esto cuando `EventBus` no podría — ¿qué campo, exactamente,
        distingue a los dos mecanismos?
      target_entity: CMP-012
    - id: EP-CH26-02
      text: |
        `IdempotencyGuard.checkIdempotency` (CH-17) sigue recibiendo `existingRecordForKey` como
        un valor ya dado, exactamente como lo recibía en su propio capítulo. Explica por qué es
        correcto, dentro de este capítulo, que ese valor pueda venir poblado (una ejecución
        anterior real) sin que eso signifique que `ToolRuntime.executeToolCall` cambió su propio
        comportamiento — ¿quién decide, en este capítulo, si `executeToolCall` se invoca o no?
      target_entity: CMP-015
  interleaved_questions:
    - id: IQ-CH26-01
      text: |
        `AdmissionController` (CH-14) decide si una activación cruda procede, sin resolver todavía
        ningún `AgentId` concreto; `AgentCore.activateAgent` (CH-11) mina el primer `runId` real de
        una ejecución. ¿Qué señal de entrada de este capítulo, ya asumida, representa exactamente
        el "routing" que CH-14 §18/§19 dejó como problema sin resolver entre esos dos componentes?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-012, CMP-011, C-022, C-021]
      prior_chapter: CH-14
    - id: IQ-CH26-02
      text: |
        `ContextEngine.assembleContextSnapshot` (CH-04) selecciona qué `ContextBlock` es relevante;
        `DataGovernanceEngine.classifyData` (CH-20) decide qué gobierno le aplica a ese mismo
        bloque. ¿Por qué la clasificación tiene que ocurrir DESPUÉS de la selección, y no antes —
        qué se rompería si `DataGovernanceEngine` decidiera relevancia en vez de `ContextEngine`?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-004, CMP-018, C-030]
      prior_chapter: CH-04
    - id: IQ-CH26-03
      text: |
        `CapabilityRegistry.resolveModelProposedToolCall` (CH-08) siempre produce un `ToolCall` que
        representa una acción pendiente; `SkillLibrary.resolveSkillForSituation` (CH-24) nunca
        produce nada que se parezca a una acción. ¿Qué le pasaría a `PolicyEngine.evaluate` (CH-05)
        si, por error, alguien le pasara un `SkillDescriptor` en vez de un `ToolCall`?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-008, CMP-022, C-035]
      prior_chapter: CH-08
    - id: IQ-CH26-04
      text: |
        `CredentialBroker.resolveCredentialReference` (CH-16) y `IdempotencyGuard.checkIdempotency`
        (CH-17) fueron publicados en capítulos separados, cada uno negándose explícitamente a
        invocar `ToolRuntime.executeToolCall` (CH-02) por su cuenta. ¿Por qué hacían falta ambos —
        y no solo uno de los dos— antes de que este capítulo pudiera invocar `executeToolCall` con
        una base real, en vez de con los dos booleanos que CH-02 siempre recibió como dados?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-014, CMP-015, CMP-002, C-026, C-027]
      prior_chapter: CH-16
    - id: IQ-CH26-05
      text: |
        `AuditLedger.recordAuditEntry` (CH-19) declaró, desde su propio capítulo, que nunca invoca
        `EventBus.distributeEvent` (CH-09) para propagar un `AuditRecord`. ¿Por qué este capítulo,
        en cambio, sí invoca `emitAndDistribute` (CH-12) después de cada `recordAuditEntry` real —
        qué evento distribuye, y por qué eso no contradice la propia distinción que CH-19 §15 ya
        trazó entre los dos mecanismos?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-017, CMP-009, C-029]
      prior_chapter: CH-19
  flashcards:
    - id: FC-CH26-01
      front: |
        ¿Qué hace `runGovernedEnterpriseTurn` con la `AdmissionDecision` que
        `evaluateAdmissionForActivationRequest` (CH-14) produce, antes de que exista cualquier
        `ExecutionContext`?
      back: |
        La entrega a `AuditLedger.recordAuditEntry` (CH-19) con `execution = NULL`/`agentId = NULL`
        — el primer uso real de `AuditLedger` sin que exista ningún `AgentRun` todavía, resolviendo
        con código real la ausencia de `AgentEvent` que CH-14 §14 documentó honestamente. Si
        `outcome != ADMIT`, la función retorna `NULL`: ningún `AgentActivationRequest` (CH-11) se
        construye jamás para una activación rechazada.
      source_entity: CMP-012
      chapter_introduced_in: CH-26
      review_stage: DAY_1
    - id: FC-CH26-02
      front: |
        ¿En qué punto exacto invoca este capítulo a `DataGovernanceEngine.classifyData` (CH-20), y
        qué le pasa como `provenance`?
      back: |
        Dentro del `FOR EACH block IN snapshot.blocks` — inmediatamente después de que
        `ContextEngine.assembleContextSnapshot` (CH-04) ya seleccionó y compactó ese `ContextBlock`,
        y antes de convertirlo en el `AgentMessage` que el modelo va a ver. `provenance` es,
        literalmente, `block.provenance` — el mismo campo real que CH-04 ya produce, nunca un valor
        inventado.
      source_entity: CMP-018
      chapter_introduced_in: CH-26
      review_stage: DAY_1
    - id: FC-CH26-03
      front: |
        ¿Qué produce `SkillLibrary.resolveSkillForSituation` (CH-24) que
        `CapabilityRegistry.resolveModelProposedToolCall` (CH-08) nunca podría producir, y en qué
        orden se consultan ambos dentro de este capítulo?
      back: |
        `resolveSkillForSituation` produce un `SkillDescriptor` — una referencia consultable a un
        procedimiento, sin `arguments`, nunca una acción pendiente. Este capítulo lo consulta
        ANTES de invocar al modelo (junto con el `ContextSnapshot` ya ensamblado); solo DESPUÉS de
        que el modelo propone una tool call se consulta `resolveModelProposedToolCall`, que sí
        produce una acción pendiente (`ToolCall`).
      source_entity: CMP-022
      chapter_introduced_in: CH-26
      review_stage: DAY_1
    - id: FC-CH26-04
      front: |
        Antes de `ToolRuntime.executeToolCall`, ¿qué dos funciones invoca este capítulo, y qué pasa
        si `IdempotencyGuard.checkIdempotency` (CH-17) encuentra un `IdempotencyRecord` ya
        `COMPLETED`?
      back: |
        `CredentialBroker.resolveCredentialReference` (CH-16) primero, luego
        `IdempotencyGuard.checkIdempotency`. Si el registro encontrado ya está `COMPLETED`,
        `executeToolCall` NUNCA se invoca — este capítulo reutiliza el `ToolResult` ya guardado en
        `existingRecord.result` en su lugar, exactamente el mecanismo que P-24/INV-11 exigen.
      source_entity: CMP-015
      chapter_introduced_in: CH-26
      review_stage: DAY_1
    - id: FC-CH26-05
      front: |
        ¿Qué NO resuelve este capítulo, aunque cablea seis componentes reales de Amendment v1.1?
      back: |
        No cablea `OperationalController` (CH-18) ni `HandoffCoordinator` (CH-23) — los caminos de
        control/traspaso quedan para CH-27, el mismo patrón de división que CH-12/CH-13 ya
        establecieron. Tampoco cablea `AgentCommunicationGateway` (CH-15, frontera entre agentes
        distintos), `EvaluationHarness` (CH-22, certificación pre-producción) ni
        `ExecutionFabricAdapter` (CH-21, topología de despliegue) — los tres operan en una escala
        distinta a la de un turno individual (ver sección 18).
      source_entity: CMP-017
      chapter_introduced_in: CH-26
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH26-01
      recall_question: RQ-CH26-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH26-02
      recall_question: RQ-CH26-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH26-03
      recall_question: RQ-CH26-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH26-04
      recall_question: RQ-CH26-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 26 — Integración Enterprise: el Camino Feliz de una Activación Admitida y Gobernada

> **Regla constitucional (Amendment v1.1, P-25):** "Logs, traces, execution ledger and immutable
> audit evidence have different purposes and MUST NOT be conflated."

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1. El detalle
> estructurado de esta sección vive en `retrieval_set` (frontmatter) y es lo que
> `scripts/validate-retrieval-set` valida automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás verificar, para cualquier turno gobernado
de nivel enterprise que arranca en una activación externa cruda y termina en una respuesta
admitida, clasificada, resuelta con una credencial real y protegida contra doble ejecución,
exactamente qué componente de Amendment v1.1 resuelve cada paso adicional sobre el camino feliz que
CH-12 ya dejó cableado.

**Esqueleto.** Este capítulo recorre 19 secciones y, como CH-12/CH-13, **no introduce ningún
contrato ni ningún componente nuevo** — es, otra vez, pura composición: invoca, con datos reales
fluyendo entre sí, las funciones que seis capítulos de Amendment v1.1 ya publicaron.

**Preguntas guía:**

1. Un componente ya decide si una activación cruda debería siquiera convertirse en un intento de
   ejecución, pero su decisión nunca puede expresarse como el tipo de evento que este libro ya
   distribuye. ¿Qué mecanismo distinto podría preservarla?
2. Un componente sabe resolver "qué herramienta ejecutar"; otro sabe resolver "qué procedimiento
   aplica". ¿En qué momento de un mismo turno tendría sentido consultar a ambos?
3. Dos preguntas — "¿con qué secreto?" y "¿esto ya se ejecutó antes?"— ya tienen dueño real. ¿En
   qué orden deberían responderse respecto a la ejecución de la acción misma?
4. Un fragmento de contexto ya fue seleccionado como relevante antes de que exista ningún
   componente que decida qué reglas de gobierno le aplican. ¿En qué punto debería ocurrir esa
   clasificación?

## 1. Arquitectura Actual (Current Architecture)

CH-12/CH-13 dejaron, con código real, un `AgentRun` completo de principio a fin — tanto su camino
feliz (`runAgentTurnEndToEnd`) como sus tres caminos de gobierno
(`runAgentTurnWithPolicyDenial`/`beginToolApprovalPause`/`resumeAfterHumanResolution`/
`terminateAgentRunOperationally`). CH-14, CH-16, CH-17, CH-18, CH-19, CH-20, CH-21, CH-22, CH-23 y
CH-24 instanciaron, después, diez componentes reales más — los nueve planos canónicos de Amendment
v1.1 — cada uno con su propia demostración aislada, exactamente con la misma disciplina que CH-01..
CH-11 ya establecieron para Article III.

Este capítulo cablea seis de esos diez componentes hacia la traza real de un turno individual —
`AdmissionController` (CH-14), `CredentialBroker` (CH-16), `IdempotencyGuard` (CH-17),
`AuditLedger` (CH-19), `DataGovernanceEngine` (CH-20) y `SkillLibrary` (CH-24) — heredando, cada
uno, una deuda puntual documentada por su propio capítulo:

1. **CH-14 → CH-11.** `evaluateAdmissionForActivationRequest` nunca es seguida de un routing real
   ni de `AgentCore.activateAgent` — "ese cableado... sigue siendo trabajo de un capítulo de
   integración futuro" (CH-14 §18).
2. **CH-14 → CH-19 (hallazgo real).** `AdmissionController` es "el primer componente real del
   libro cuya función principal nunca construye un `AgentEvent`" (CH-14 §14) — su decisión no
   tiene, todavía, ningún destino real de evidencia.
3. **CH-20 → CH-04.** `assembleContextSnapshot` (CH-04) no consulta todavía `classifyData` sobre
   cada `ContextBlock` que produce — "el cableado exacto que este capítulo deja explícitamente
   para un capítulo de integración futuro" (CH-20 §9).
4. **CH-24 → CH-01/CH-08.** Ningún componente invoca todavía `resolveSkillForSituation` dentro de
   un turno real — "el pseudocódigo... prueba que el mecanismo funciona, no que ya esté conectado
   dentro de un flujo real" (CH-24 §18).
5. **CH-16 → CH-02.** `ToolRuntime.executeToolCall` nunca obtiene, todavía, la credencial que
   `resolveCredentialReference` resolvería — "el cableado exacto que este capítulo deja
   explícitamente para un capítulo de integración futuro" (CH-16 §18).
6. **CH-17 → CH-02.** `ToolRuntime.executeToolCall` nunca consulta `checkIdempotency` antes de
   ejecutar, ni invoca `recordIdempotentExecution` después — mismo tratamiento explícito (CH-17
   §18).
7. **CH-19 → todos.** `PolicyEngine`, `AdmissionController`, `CredentialBroker`,
   `IdempotencyGuard` y el resto "no fueron modificados para invocar de verdad
   `recordAuditEntry` sobre sus propias decisiones" (CH-19 §18).

Explícitamente **fuera** de esta lista — y fuera del alcance de este capítulo (ver sección 3 y
sección 18) — quedan `OperationalController` (CH-18) y `HandoffCoordinator` (CH-23), que CH-27
cablea; y `AgentCommunicationGateway` (CH-15), `EvaluationHarness` (CH-22) y
`ExecutionFabricAdapter` (CH-21), que ningún capítulo de integración de un turno individual debería
cablear (ver sección 18 para la justificación completa de cada exclusión).

## 2. El Problema (Problem)

Con los diecisiete componentes reales de este libro (once de Article III, seis de Amendment v1.1
ya elegidos para este capítulo) cada uno con su propia función correcta, el problema deja de ser
"falta un componente" — es, otra vez, el mismo problema que CH-12 §2 ya nombró para el runtime
original, ahora un nivel más arriba: **nadie ha visto, todavía, un turno gobernado de nivel
enterprise correr de principio a fin**. `runAgentTurnEndToEnd` (CH-12) nunca ha recibido una
activación que primero tuviera que ser admitida. `assembleContextSnapshot` (CH-04) nunca ha
producido un `ContextBlock` que alguien clasificara. `executeToolCall` (CH-02) nunca ha sido
invocada después de que una credencial real se resolviera o de que se verificara que esa misma
acción no se hubiera ejecutado ya antes bajo la misma clave.

Necesitamos, por fin, la traza real de un turno enterprise: una función que tome una activación
cruda, la admita, la lleve hasta un `AgentRun`, clasifique lo que el modelo va a ver, consulte qué
procedimiento aplica además de qué herramienta ejecutar, resuelva una credencial real, verifique
idempotencia antes de cualquier efecto sobre el mundo, y deje evidencia de auditoría de cada
decisión crítica — sin inventar ningún componente nuevo, sin modificar el pseudocódigo ya
publicado de ninguno de los diecisiete existentes, y sin fingir que los caminos de control/
traspaso (CH-27) también quedan resueltos aquí.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los treinta y cinco contratos y los veintidós componentes que existen hasta este punto no bastan
porque, literalmente, cada uno de los seis que este capítulo cablea lo dice de sí mismo en su
propia sección 18 (ver sección 1). Ninguna de esas notas es un descuido: cada una es la misma
disciplina de *ownership* aplicada con honestidad — un componente que declara "esto no me
pertenece a mí" no puede, al mismo tiempo, escribir el código que lo conecta con el runtime que ya
existía, porque ese código pertenece a una decisión distinta: la de secuenciar, no la de decidir.
Exactamente el mismo argumento que CH-12 §3 ya usó para los once componentes originales.

Un hueco adicional, más allá de las seis deudas puntuales, confirma que la arquitectura actual no
basta: `AgentEvent` (C-010) exige `runId`/`sessionId`/`agentId`/`traceId` no `Optional` — y
`AdmissionController` decide antes de que ninguno de los cuatro exista (CH-14 §14). Ningún
capítulo, hasta este, había mostrado jamás qué mecanismo real —distinto de `EventBus`— podría
preservar esa decisión de todas formas. `AuditLedger.recordAuditEntry` (CH-19), con
`execution: Optional<ExecutionContext>`, es la respuesta — pero nadie, hasta este capítulo, la
había invocado con `execution = NULL` dentro de una traza real.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la
> secuencia `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una
> entidad que no haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT`
> registrado — **no magic entities**. Este capítulo aplica la misma disciplina que CH-12/CH-13 ya
> aplicaron en su forma más estricta: no define ni un solo `STRUCT`/`ENUM`/`COMPONENT` nuevo — cada
> entidad que su pseudocódigo utiliza ya estaba registrada, o se documenta aquí por referencia
> (sección 6), exactamente como CH-12/CH-13 ya hicieron con `ExecutionUsage`/`HumanInteractionOutcome`.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-04   Every action produces observable events.
           Extendido, no repetido: además de cada AgentEvent que CH-12 ya distribuía, este
           capítulo distribuye, por primera vez con ejecución real, CREDENTIAL_RESOLVED,
           IDEMPOTENT_EXECUTION_DETECTED/RECORDED, DATA_CLASSIFIED, SKILL_RESOLVED y
           AUDIT_RECORD_CREATED — seis tipos de evento que CH-16/CH-17/CH-19/CH-20/CH-24 ya
           habían declarado, pero que ningún EMIT interno de esos capítulos había alcanzado nunca
           a EventBus.distributeEvent (CH-09) hasta ahora (ver sección 14).
    P-05   Side effects pass through policy.
           Sin cambios de fondo respecto a CH-12: executeToolCall (CH-02) sigue sin invocarse
           antes de que evaluatePolicyForToolCall (CH-05) decida ALLOW. Lo nuevo es que, incluso
           con ALLOW, executeToolCall tampoco se invoca si IdempotencyGuard ya encontró un
           IdempotencyRecord COMPLETED para la misma clave (ver sección 11).
    P-10   The harness owns execution state—not the model.
           evaluateAdmissionForActivationRequest (CH-14) decide, antes de que exista cualquier
           AgentState, si una activación procede — una decisión tan poco delegada al modelo como
           cualquiera de las que CH-12/CH-13 ya protegían.
    P-12   Events observe; hooks intervene.
           Cada AgentEvent que este capítulo distribuye reconstruye, sin agregarle ni quitarle
           campos, exactamente el que la función productora ya construía internamente — el mismo
           principio que emitAndDistribute (CH-12) ya respetaba para los once componentes de
           Article III, aplicado ahora a seis componentes más.
    P-13   Authorization is deterministic and external to the LLM.
           credentialBelongsToCapability/secretExists (CredentialBroker) y
           existingRecordForKey (IdempotencyGuard) son señales deterministas, ya dadas — nunca
           una negociación con el modelo, exactamente como admissionRulesGrantAccess (CH-14) ya
           lo era.
    P-16   Activation is independent from execution.
           Primera cita literal con ejecución real: evaluateAdmissionForActivationRequest se
           invoca ANTES de que exista cualquier AgentActivationRequest (C-021) — la activación
           (una decisión sobre un ActivationRequest crudo) queda, verificablemente, separada de la
           ejecución (una decisión sobre un AgentRun ya existente).
    P-17   Admission precedes execution.
           Primera cita literal con ejecución real: IF admission.outcome != ADMIT RETURN NULL —
           ningún AgentActivationRequest se construye jamás para una activación no admitida.
    P-22   Enterprise data is governed throughout its lifecycle.
           Primera cita literal con ejecución real, en dos formas distintas dentro del mismo
           turno: classifyData (CH-20) sobre cada ContextBlock, y resolveCredentialReference
           (CH-16) sobre el secreto que respalda una tool call — dos aplicaciones reales del mismo
           principio, sobre dos tipos de dato distintos.
    P-24   Side effects require idempotency semantics.
           Primera cita literal con ejecución real de punta a punta: checkIdempotency se invoca
           antes de cualquier side effect potencial, y recordIdempotentExecution después de que
           uno nuevo concluye.
    P-25   Audit evidence is distinct from operational telemetry.
           Primera cita literal con ejecución real, y la más importante de este capítulo:
           recordAuditEntry (CH-19) se invoca, dos veces, sobre decisiones que EventBus también
           observa (vía emitAndDistribute) — demostrando con código que ambos mecanismos coexisten
           sin conflacionarse (CH-19 §15), y una tercera vez (la admisión) donde solo AuditLedger
           puede preservar la decisión.

Invariants preserved
    INV-06   Todo side effect pasa por PolicyEngine.       (heredado sin cambios de CH-12/CH-13)
    INV-07   Todo ToolResult vuelve al ciclo como observación explícita. (heredado sin cambios)
    INV-08   El harness es propietario del execution state. (heredado, y extendido: ningún
             AgentActivationRequest se construye antes de una AdmissionDecision real)
    INV-09   Todo AgentRun tiene límites explícitos.        (heredado sin cambios de CH-12)
    INV-11   Side effects críticos soportan idempotencia, deduplicación o protección equivalente.
             Primera cita literal con ejecución real: checkIdempotency/recordIdempotentExecution
             se invocan alrededor de cada executeToolCall real de este capítulo.
    INV-18   Toda acción significativa produce un evento observable. (extendido — ver P-04)
    INV-19   Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy relevante.
             El mismo ExecutionContext (mismo runId/sessionId/traceId) que CH-12 ya construía
             sobrevive, sin cambiar, hasta CredentialBroker/IdempotencyGuard/DataGovernanceEngine —
             y AuditLedger.recordAuditEntry trae, además, actor (ActorId) y versionSnapshot reales.
    INV-20   Todo error operacional pertenece a una categoría conocida. (heredado, ver sección 13)
    INV-E01  No ingress adapter calls AgentLoop directly; it produces an ActivationRequest.
             Este capítulo nunca invoca AgentLoop.runTurn sobre una activación cruda — siempre
             pasa primero por evaluateAdmissionForActivationRequest y por la construcción real de
             un AgentActivationRequest (C-021).
    INV-E02  No ActivationRequest executes without an AdmissionDecision.
             Primera cita literal con ejecución real: ningún AgentActivationRequest se construye
             en este capítulo sin que exista ya, antes, un AdmissionDecision con outcome = ADMIT.
    INV-E07  Tenant data, memory, credentials, artifacts and audit records are isolated.
             No profundizado por este capítulo (ver sección 18) — se preserva sin regresión: la
             CredentialReference que este capítulo resuelve nunca porta el valor real del secreto.
    INV-E08  Credentials are resolved by a CredentialBroker and SHOULD NOT enter model context.
             Primera cita literal con ejecución real: la CredentialReference que
             resolveCredentialReference produce nunca se agrega a candidates/pendingMessages — el
             modelo nunca la ve.
    INV-E09  Every side-effecting capability declares idempotency and retry semantics.
             Primera cita literal con ejecución real, mitad "idempotency": ver INV-11 arriba.
    INV-E10  Every production run records exact versions of agent, skill, policy, model
             configuration and capability contracts.
             Primera cita literal con ejecución real: cada recordAuditEntry de este capítulo recibe
             un VersionSnapshot real, no NULL ni omitido.
    INV-E11  Data governance policy follows context and artifacts across component boundaries.
             Primera cita literal con ejecución real: classifyData produce un DataGovernanceLabel
             por cada ContextBlock ya seleccionado por ContextEngine (CH-04) — el gobierno sigue al
             dato a través de la frontera entre los dos componentes.

Component ownership changes
    Ninguno. introduces_components: [] — este capítulo no instala ningún componente nuevo, y no
    modifica ni un solo campo owns/does_not_own/consumes/produces/dependencies de ninguna de las
    veintidós fichas ya registradas en registry/components.yaml.

Lifecycle changes
    Ninguna modificación a AgentRunStatus (C-013) ni a AdmissionOutcome/IdempotencyRecordStatus/
    DataClassificationLevel (embebidos, CH-14/CH-17/CH-20). Este capítulo es, en cambio, el primero
    en ejercitar con código real la secuencia completa "activación cruda → AdmissionDecision(ADMIT)
    → AgentActivationRequest real" que CH-14/CH-11, juntos, dejaron documentada solo en prosa.

Security implications
    Este capítulo nunca ejecuta una acción sin que PolicyEngine ya la haya evaluado con
    outcome = ALLOW, y nunca la ejecuta de nuevo si IdempotencyGuard ya la reconoce como completada
    — ver sección 15 para el análisis completo.

Observability implications
    Primer capítulo que demuestra, con código real, que un mismo AgentEvent puede alcanzar
    EventBus.distributeEvent (CH-09, vía emitAndDistribute, CH-12) Y que la misma decisión, por
    separado, puede alcanzar AuditLedger.recordAuditEntry (CH-19) — dos mecanismos que P-25 exige
    sin conflacionar, y que este capítulo ejercita juntos por primera vez (ver sección 14).

Deterministic vs agentic boundary
    Sin cambios de fondo: los seis componentes que este capítulo cablea ya eran, cada uno desde su
    propio capítulo, deterministas y externos al modelo. Lo que este capítulo demuestra, por
    primera vez, es que esa frontera se preserva intacta cuando los seis se ejecutan junto al
    runtime de Article III, en el orden real.
```

## 5. Conceptos Nuevos (New Concepts)

Este capítulo no introduce ningún concepto que amerite una entrada propia en
`registry/glossary.yaml` (que, deliberadamente, no toca — mismo precedente que CH-12/CH-13 §5).
Introduce dos ideas puramente narrativas:

- **Turno enterprise gobernado (Governed Enterprise Turn)**: la traza de un `AgentRun` que, además
  de recorrer el camino feliz que CH-12 ya cableó, pasa por `AdmissionController`,
  `DataGovernanceEngine`, `SkillLibrary`, `CredentialBroker`, `IdempotencyGuard` y `AuditLedger` en
  los puntos exactos donde cada uno ya declaró, en su propio capítulo, que su cableado real
  quedaba pendiente. Es lo que `runGovernedEnterpriseTurn` (sección 11) demuestra con código real.
- **Evidencia anterior a la ejecución (Pre-Execution Evidence)**: el acto de invocar
  `AuditLedger.recordAuditEntry` con `execution = NULL`/`agentId = NULL` sobre una decisión que
  ocurre antes de que exista cualquier `AgentRun` — el mecanismo real, verificado en este capítulo,
  que resuelve la ausencia de `AgentEvent` que CH-14 §14 documentó honestamente para
  `AdmissionController`.

Ninguna de las dos ideas anteriores es una responsabilidad nueva que algún componente deba `owns`:
son, simplemente, la forma de describir en prosa lo que `runGovernedEnterpriseTurn` hace.

## 6. Nuevas Estructuras de Datos (New Data Structures)

**Este capítulo no introduce ningún `STRUCT` ni `ENUM` nuevo.** Reutiliza, sin modificar ni un solo
campo, los contratos ya registrados desde CH-00..CH-24: además de los veintiún contratos que CH-12
ya usaba (`C-001`..`C-021`), este capítulo usa `ActivationRequest` (C-022, CH-14),
`AdmissionDecision` (C-023, CH-14), `CredentialReference` (C-026, CH-16), `IdempotencyRecord`
(C-027, CH-17), `AuditRecord` (C-029, CH-19), `DataGovernanceLabel` (C-030, CH-20) y
`SkillDescriptor` (C-035, CH-24) — los siete contratos de Amendment v1.1 que corresponden,
exactamente, a los seis componentes de la sección 1.

Cuatro tipos embebidos, sin `C-XXX` propio, necesitan documentarse aquí por referencia — el mismo
mecanismo que CH-12 §6 ya usó para `ExecutionUsage` y CH-13 §6 para `HumanInteractionOutcome`/
`ActorId`:

| Identificador (heredado, sin `C-XXX` propio) | Introducido en | Rol en este capítulo |
|---|---|---|
| `ExecutionUsage` | CH-07 §6 | tipo del parámetro `usage` que este capítulo pasa, ya dado, a `evaluateExecutionContinuation` (CH-07) |
| `VersionSnapshot` | CH-19 §6 | tipo del parámetro `versionSnapshot` que este capítulo pasa, ya dado, a cada invocación de `recordAuditEntry` (CH-19) |
| `ActorId` | CH-06 §6 | tipo del parámetro `auditActor` que este capítulo pasa, ya dado, a `recordAuditEntry` (CH-19) |
| `CredentialClassification` | CH-16 §6 | tipo del parámetro `credentialClassification` que este capítulo pasa, ya dado, a `resolveCredentialReference` (CH-16) |

**Unchanged**: ningún otro tipo heredado cambia de forma. Este capítulo no introduce ningún
identificador de tipo `Xxx­Id` opaco nuevo — reutiliza `newMessageId()`/`newEventId()`/`now()`/
`newTraceId()` exactamente como CH-11/CH-12 ya los usaban.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

**Este capítulo no introduce ningún contrato nuevo.** `introduces_contracts: []` en el
frontmatter — `registry/contracts.yaml` permanece, después de este capítulo, exactamente en los
treinta y cinco contratos que CH-24 dejó registrados (`C-001`..`C-035`).

## 8. Responsabilidades de Componentes (Component Responsibilities)

**Este capítulo no introduce ningún componente nuevo.** `introduces_components: []` en el
frontmatter — `registry/components.yaml` permanece, después de este capítulo, exactamente en los
veintidós componentes que CH-24 dejó registrados (`CMP-001`..`CMP-022`), sin que ninguna de sus
fichas cambie un solo campo.

Lo que este capítulo sí hace es mostrar — con una función nueva y propia,
`runGovernedEnterpriseTurn` (sección 11) — el orden real en que los diecisiete componentes
relevantes se invocan entre sí dentro de una sola ejecución:

```text
Orden de invocación real dentro de runGovernedEnterpriseTurn (camino feliz enterprise)

 0.  AdmissionController.evaluateAdmissionForActivationRequest (CH-14) → AdmissionDecision
     AuditLedger.recordAuditEntry (CH-19, execution = NULL)            → AuditRecord
     [IF outcome != ADMIT → RETURN NULL]
 1.  AgentCore.activateAgent / beginAgentInitialization        (CH-11) → AgentState
 2.  ExecutionController.evaluateExecutionContinuation          (CH-07) → ExecutionDecision (CONTINUE)
 3.  ContextEngine.assembleContextSnapshot                      (CH-04) → ContextSnapshot
     DataGovernanceEngine.classifyData por cada ContextBlock    (CH-20) → DataGovernanceLabel
 4.  SkillLibrary.resolveSkillForSituation                      (CH-24) → SkillDescriptor
 5.  ModelGateway.invokeModelForTurn                            (CH-03) → ModelResponse
 6.  AgentLoop.runTurn                                           (CH-01) → AgentState (WAITING_FOR_TOOL)
 7.  SessionManager.createOrUpdateSessionCheckpoint              (CH-10) → SessionState
 8.  CapabilityRegistry.resolveModelProposedToolCall             (CH-08) → ToolCall
 9.  PolicyEngine.evaluatePolicyForToolCall                      (CH-05) → PolicyDecision (ALLOW)
10.  CredentialBroker.resolveCredentialReference                 (CH-16) → CredentialReference
11.  IdempotencyGuard.checkIdempotency                            (CH-17) → Optional<IdempotencyRecord>
12.  [SI COMPLETED: reusa ToolResult. SI NO:]
     ToolRuntime.executeToolCall                                 (CH-02) → ToolResult
     IdempotencyGuard.recordIdempotentExecution                  (CH-17) → IdempotencyRecord
     AuditLedger.recordAuditEntry (execution real)                (CH-19) → AuditRecord
13.  ExecutionController.evaluateExecutionContinuation            (CH-07) → ExecutionDecision (CONTINUE)
14.  ContextEngine.assembleContextSnapshot (con la observación)   (CH-04) → ContextSnapshot
     DataGovernanceEngine.classifyData por cada ContextBlock      (CH-20) → DataGovernanceLabel
15.  ModelGateway.invokeModelForTurn                              (CH-03) → ModelResponse (finished = TRUE)
16.  AgentLoop.runTurn                                             (CH-01) → AgentState (COMPLETED)
17.  SessionManager.createOrUpdateSessionCheckpoint                (CH-10) → SessionState

En cada paso productor de un AgentEvent real, EventBus.distributeEvent (CH-09) lo entrega vía
emitAndDistribute (CH-12) — ver sección 14.
```

Cada una de las diecisiete fichas ya publicadas se respeta exactamente: `AdmissionController`
sigue sin resolver ningún `AgentId`; `DataGovernanceEngine` sigue sin decidir relevancia;
`SkillLibrary` sigue sin producir ninguna acción pendiente; `CredentialBroker` sigue sin ejecutar
ningún side effect; `IdempotencyGuard` sigue sin decidir autorización; `AuditLedger` sigue sin
depender de `EventBus`. Ninguna decisión cambió de dueño — solo se invocó, por primera vez, en el
orden real.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
runGovernedEnterpriseTurn (función de integración, no un componente registrado)
    invoca → evaluateAdmissionForActivationRequest (CMP-012)
    invoca → recordAuditEntry (CMP-017)
    invoca → activateAgent, beginAgentInitialization (CMP-011)
    invoca → evaluateExecutionContinuation (CMP-007)
    invoca → assembleContextSnapshot (CMP-004)
    invoca → classifyData (CMP-018)
    invoca → resolveSkillForSituation (CMP-022)
    invoca → invokeModelForTurn (CMP-003)
    invoca → runTurn (CMP-001)
    invoca → resolveModelProposedToolCall (CMP-008)
    invoca → evaluatePolicyForToolCall (CMP-005)
    invoca → resolveCredentialReference (CMP-014)
    invoca → checkIdempotency, recordIdempotentExecution (CMP-015)
    invoca → executeToolCall (CMP-002)
    invoca → createOrUpdateSessionCheckpoint (CMP-010)
    invoca → emitAndDistribute → distributeEvent (CMP-009)
```

**Límite real de este capítulo, documentado con la misma honestidad que CH-12/CH-13 §9.**
`registry/components.yaml` **no se modifica**: ninguna de las veintidós fichas agrega, en su
propio campo `dependencies`, a ninguno de sus vecinos. Como ya documentaron CH-12 §9 y CH-13 §9,
esto significa que `diagrams/mindmap/chapter-26.diagram` no gana ninguna arista
`DEPENDS_ON`/`PRODUCES`/`CONSUMES` nueva por este capítulo — el mecanismo actual del `BookMindMap`
sigue sin tener ningún camino para que un capítulo de integración agregue esas aristas sin editar
la ficha de un componente ya existente, y este capítulo, por instrucción explícita, no la edita.

En prosa, entonces, las relaciones que este capítulo sí ejercita por primera vez con código real
son exactamente las diecisiete invocaciones de la sección 8 — la integración vive en
`runGovernedEnterpriseTurn`, no en `registry/components.yaml`.

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
AdmissionController → AuditLedger → AgentCore → ExecutionController → ContextEngine →
DataGovernanceEngine → SkillLibrary → ModelGateway → AgentLoop → SessionManager →
CapabilityRegistry → PolicyEngine → CredentialBroker → IdempotencyGuard → ToolRuntime →
IdempotencyGuard → AuditLedger → ExecutionController → ContextEngine → DataGovernanceEngine →
ModelGateway → AgentLoop → SessionManager
(EventBus recibe, en cada paso productor de evento, el AgentEvent correspondiente)
```

**Vista 2 — Sequence**

```text
ActivationRequest
   │
   ▼
AdmissionController
   │ evaluateAdmissionForActivationRequest → AdmissionDecision
   ▼
AuditLedger
   │ recordAuditEntry(execution = NULL) → AuditRecord   (sin AgentEvent posible — CH-14 §14)
   │
   │ ¿outcome == ADMIT? — NO → RETURN NULL (fin de la traza, sin AgentRun)
   ▼ SÍ
AgentCore
   │ activateAgent / beginAgentInitialization → AgentState; EMIT RUN_STARTED → EventBus
   ▼
ExecutionController → ContextEngine
   │ assembleContextSnapshot → ContextSnapshot
   ▼
DataGovernanceEngine  (por cada ContextBlock)
   │ classifyData(block.provenance, block.provenance, legalHold, execution, agentId)
   │ → DataGovernanceLabel; EMIT DATA_CLASSIFIED → EventBus
   ▼
SkillLibrary
   │ resolveSkillForSituation(situationName, registeredSkills, execution, agentId)
   │ → SkillDescriptor; EMIT SKILL_RESOLVED → EventBus
   ▼
ModelGateway → AgentLoop → SessionManager
   │ (mismo patrón que CH-12 §11 — WAITING_FOR_TOOL)
   ▼
CapabilityRegistry → PolicyEngine
   │ resolveModelProposedToolCall → ToolCall; evaluatePolicyForToolCall → PolicyDecision(ALLOW)
   ▼
CredentialBroker
   │ resolveCredentialReference(descriptor, ...) → CredentialReference; EMIT CREDENTIAL_RESOLVED
   ▼
IdempotencyGuard
   │ checkIdempotency(callOne, idempotencyKey, existingRecord, ...) → Optional<IdempotencyRecord>
   │
   │ ¿ya existe un registro COMPLETED? — SÍ → reusa ToolResult, NO ejecuta de nuevo
   ▼ NO
ToolRuntime
   │ executeToolCall → ToolResult
   ▼
IdempotencyGuard
   │ recordIdempotentExecution → IdempotencyRecord(COMPLETED); EMIT IDEMPOTENT_EXECUTION_RECORDED
   ▼
AuditLedger
   │ recordAuditEntry(execution real) → AuditRecord; EMIT AUDIT_RECORD_CREATED → EventBus
   ▼
ExecutionController → ContextEngine → DataGovernanceEngine → ModelGateway → AgentLoop
   │ (segundo turno, mismo patrón; finished = TRUE)
   ▼
SessionManager
   ▼
AgentState (COMPLETED) — el turno enterprise terminó, de principio a fin, con código real
```

**Vista 3 — Pseudocódigo**

Ver §11: `runGovernedEnterpriseTurn` es la primera formalización ejecutable, en todo este libro, de
un turno gobernado de nivel enterprise — construida exclusivamente a partir de funciones ya
publicadas por CH-00..CH-24, sin modificar ninguna.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya registradas desde CH-00..CH-24, más `ExecutionUsage`,
`VersionSnapshot`, `ActorId` y `CredentialClassification` (sección 6, disponibles por referencia).

```pseudocode
FUNCTION runGovernedEnterpriseTurn(
    activationRequest: ActivationRequest,
    resolvedAgentId: AgentId,
    registeredCapabilities: List<CapabilityDescriptor>,
    registeredSkills: List<SkillDescriptor>,
    situationName: Text,
    activeSubscriptions: List<EventSubscription>,
    usage: ExecutionUsage,
    versionSnapshot: VersionSnapshot,
    auditActor: ActorId,
    admissionSubjectRef: Text,
    contextSubjectRef: Text,
    toolAuditSubjectRef: Text,
    proposedCapabilityName: Text,
    proposedRawArguments: Map<Text, Value>,
    argumentsMatchSchema: Boolean,
    credentialName: Text,
    credentialClassification: CredentialClassification,
    credentialBelongsToCapability: Boolean,
    secretExists: Boolean,
    credentialExpiresAt: Optional<Timestamp>,
    idempotencyKey: Text,
    existingIdempotencyRecord: Optional<IdempotencyRecord>,
    toolExecutionSucceeded: Boolean,
    toolExecutionOutput: Value,
    contextLegalHold: Boolean,
    finalModelContent: Value
) -> Optional<AgentState>

    // --- 0) AdmissionController decide si esta activación cruda procede siquiera -------------
    admission: AdmissionDecision = evaluateAdmissionForActivationRequest(activationRequest)

    // AuditLedger preserva esta decisión aunque todavia no exista ningun ExecutionContext real
    // (CH-14 §14: "el primer componente real del libro cuya funcion principal nunca construye
    // un AgentEvent" — AgentEvent exige runId/sessionId/agentId/traceId no Optional; AuditRecord
    // no los exige; esto es, precisamente, el mecanismo que P-25 exige para una decision
    // anterior a que exista cualquier ejecucion.)
    admissionAudit: AuditRecord = recordAuditEntry(
        admissionSubjectRef, versionSnapshot, auditActor, NULL, NULL
    )
    // admissionAudit nunca produce un AgentEvent (execution = NULL) — no hay, todavia, ningun
    // emitAndDistribute posible para este paso; ver seccion 14.

    IF admission.outcome != ADMIT
        // outcome = REJECT: ningun AgentActivationRequest se construye jamas para esta
        // activacion — INV-E02, con codigo real; la traza termina aqui, sin ninguna ejecucion.
        RETURN NULL
    END

    // --- 1) AgentCore: la activacion ya admitida se convierte en una ejecucion real ---------
    // resolvedAgentId es la senal de entrada asumida que representa el routing que CH-14
    // §18/19 dejo, explicitamente, sin construir: "quien resuelve que AgentId concreto le
    // corresponde a un externalIdentityRef ya admitido" (CH-14, IQ-CH14-01).
    createdState: AgentState = activateAgent(AgentActivationRequest(
        agentId = resolvedAgentId,
        sessionId = NULL,
        input = activationRequest.payload,
        requestedAt = activationRequest.receivedAt
    ))

    config: Optional<AgentConfig> = findAgentConfig(resolvedAgentId)
    initializingState: AgentState = beginAgentInitialization(createdState, config)

    execution: ExecutionContext = ExecutionContext(
        runId = initializingState.runId,
        sessionId = initializingState.sessionId,
        traceId = newTraceId(),
        budget = config.budget
    )

    emitAndDistribute(RUN_STARTED, execution, initializingState.agentId, initializingState, activeSubscriptions)

    runningState: AgentState = AgentState(
        runId = initializingState.runId,
        sessionId = initializingState.sessionId,
        agentId = initializingState.agentId,
        status = RUNNING,
        currentTurn = initializingState.currentTurn
    )

    session: Optional<SessionState> = NULL
    firstMessage: AgentMessage = AgentMessage(
        id = newMessageId(), role = USER, content = activationRequest.payload, timestamp = now()
    )
    candidates: List<AgentMessage> = []
    candidates.append(firstMessage)

    // --- 2) ExecutionController, exactamente como en CH-12 §11 ------------------------------
    continuationOne: ExecutionDecision = evaluateExecutionContinuation(
        runningState, execution, execution.budget, usage, FALSE
    )
    emitAndDistribute(EXECUTION_EVALUATED, execution, runningState.agentId, continuationOne, activeSubscriptions)

    IF continuationOne.outcome != CONTINUE
        RETURN runningState
    END

    // --- 3) ContextEngine ensambla el snapshot; DataGovernanceEngine clasifica cada bloque ---
    // ANTES de que exista cualquier AgentMessage a partir de el (cierra la deuda CH-20 -> CH-04)
    snapshotOne: ContextSnapshot = assembleContextSnapshot(candidates, execution, runningState.agentId)
    emitAndDistribute(CONTEXT_SNAPSHOT_ASSEMBLED, execution, runningState.agentId, snapshotOne, activeSubscriptions)

    pendingMessagesOne: List<AgentMessage> = []
    FOR EACH block IN snapshotOne.blocks
        labelOne: DataGovernanceLabel = classifyData(
            contextSubjectRef, block.provenance, contextLegalHold, execution, runningState.agentId
        )
        emitAndDistribute(DATA_CLASSIFIED, execution, runningState.agentId, labelOne, activeSubscriptions)

        pendingMessagesOne.append(AgentMessage(
            id = newMessageId(), role = USER, content = block.content, timestamp = now()
        ))
    END

    // --- 4) SkillLibrary: "que procedimiento aplica", una pregunta distinta de "que tool
    // ejecutar" (CapabilityRegistry, paso 8 mas abajo) — se consulta ANTES de invocar al modelo,
    // junto con el ContextSnapshot ya ensamblado (cierra la deuda CH-24 -> CH-01/CH-08).
    resolvedSkill: SkillDescriptor = resolveSkillForSituation(
        situationName, registeredSkills, execution, runningState.agentId
    )
    emitAndDistribute(SKILL_RESOLVED, execution, runningState.agentId, resolvedSkill, activeSubscriptions)

    pendingMessagesOne.append(AgentMessage(
        id = newMessageId(), role = USER, content = resolvedSkill.procedureRef, timestamp = now()
    ))

    // --- 5) ModelGateway / AgentLoop / SessionManager, exactamente como en CH-12 §11 --------
    responseOne: ModelResponse = invokeModelForTurn(
        runningState, execution, pendingMessagesOne,
        TRUE, FALSE, TRUE, proposedCapabilityName, proposedRawArguments, NULL
    )
    emitAndDistribute(MODEL_RESPONSE_RECEIVED, execution, runningState.agentId, responseOne, activeSubscriptions)

    modelFinishedOne: Boolean = responseOne.finished
    modelProposesToolCallOne: Boolean = responseOne.proposedToolCall != NULL

    turnOneState: AgentState = runTurn(runningState, execution, modelFinishedOne, modelProposesToolCallOne)
    emitAndDistribute(TURN_CONTINUED, execution, turnOneState.agentId, turnOneState, activeSubscriptions)

    sessionAfterTurnOne: SessionState = createOrUpdateSessionCheckpoint(
        session, turnOneState, execution, turnOneState.agentId
    )
    emitAndDistribute(SESSION_CHECKPOINT_CREATED, execution, turnOneState.agentId, sessionAfterTurnOne, activeSubscriptions)
    session = sessionAfterTurnOne

    resumedState: AgentState = turnOneState

    IF turnOneState.status == WAITING_FOR_TOOL
        // --- 6) CapabilityRegistry / PolicyEngine, exactamente como en CH-12 §11 -----------
        callOne: ToolCall = resolveModelProposedToolCall(
            responseOne, registeredCapabilities, execution, turnOneState.agentId, argumentsMatchSchema
        )
        emitAndDistribute(CAPABILITY_RESOLVED, execution, turnOneState.agentId, callOne, activeSubscriptions)

        decisionOne: PolicyDecision = evaluatePolicyForToolCall(callOne, execution, turnOneState.agentId)
        emitAndDistribute(POLICY_EVALUATED, execution, turnOneState.agentId, decisionOne, activeSubscriptions)

        IF decisionOne.outcome != ALLOW
            // DENY / REQUIRE_APPROVAL: caminos de CH-13/CH-27 — este capitulo cierra solo ALLOW.
            RETURN turnOneState
        END

        // --- 7) CredentialBroker resuelve la credencial ANTES del side effect (cierra CH-16) -
        // descriptor ya existe en registeredCapabilities: CapabilityRegistry (paso 6) acaba de
        // resolver callOne.capability contra esa misma lista — la busqueda es determinista.
        descriptor: CapabilityDescriptor = descriptorForCapability(callOne.capability, registeredCapabilities)

        credential: CredentialReference = resolveCredentialReference(
            descriptor, credentialName, credentialClassification, credentialBelongsToCapability,
            secretExists, credentialExpiresAt, execution, turnOneState.agentId
        )
        emitAndDistribute(CREDENTIAL_RESOLVED, execution, turnOneState.agentId, credential, activeSubscriptions)
        // credential nunca se agrega a candidates/pendingMessages — INV-E08: el modelo no la ve.

        // --- 8) IdempotencyGuard verifica ANTES del side effect (cierra la deuda CH-17) ------
        existingRecord: Optional<IdempotencyRecord> = checkIdempotency(
            callOne, idempotencyKey, existingIdempotencyRecord, execution, turnOneState.agentId
        )

        IF existingRecord != NULL
            emitAndDistribute(IDEMPOTENT_EXECUTION_DETECTED, execution, turnOneState.agentId, existingRecord, activeSubscriptions)
        END

        resultOne: ToolResult

        IF existingRecord != NULL AND existingRecord.status == COMPLETED
            // el side effect real NUNCA se reejecuta — P-24/INV-11 con codigo real.
            resultOne = existingRecord.result
        ELSE
            resultOne = executeToolCall(
                callOne, execution, turnOneState.agentId, TRUE, TRUE,
                toolExecutionSucceeded, toolExecutionOutput
            )

            IF resultOne.succeeded
                emitAndDistribute(TOOL_CALL_COMPLETED, execution, turnOneState.agentId, resultOne, activeSubscriptions)
            ELSE
                emitAndDistribute(TOOL_CALL_FAILED, execution, turnOneState.agentId, resultOne, activeSubscriptions)
            END

            completedRecord: IdempotencyRecord = recordIdempotentExecution(
                callOne, resultOne, idempotencyKey, existingIdempotencyRecord, execution, turnOneState.agentId
            )
            emitAndDistribute(IDEMPOTENT_EXECUTION_RECORDED, execution, turnOneState.agentId, completedRecord, activeSubscriptions)
        END

        // --- 9) AuditLedger preserva evidencia de esta accion ya ejecutada (cierra CH-19) ----
        executionAudit: AuditRecord = recordAuditEntry(
            toolAuditSubjectRef, versionSnapshot, auditActor, execution, turnOneState.agentId
        )
        emitAndDistribute(AUDIT_RECORD_CREATED, execution, turnOneState.agentId, executionAudit, activeSubscriptions)

        observation: AgentMessage = AgentMessage(id = newMessageId(), role = TOOL, content = resultOne, timestamp = now())
        candidates.append(observation)

        resumedState = AgentState(
            runId = turnOneState.runId, sessionId = turnOneState.sessionId, agentId = turnOneState.agentId,
            status = RUNNING, currentTurn = turnOneState.currentTurn
        )
    END

    // --- 10) segundo turno: mismo patron; DataGovernanceEngine clasifica otra vez ------------
    continuationTwo: ExecutionDecision = evaluateExecutionContinuation(
        resumedState, execution, execution.budget, usage, FALSE
    )
    emitAndDistribute(EXECUTION_EVALUATED, execution, resumedState.agentId, continuationTwo, activeSubscriptions)

    IF continuationTwo.outcome != CONTINUE
        RETURN resumedState
    END

    snapshotTwo: ContextSnapshot = assembleContextSnapshot(candidates, execution, resumedState.agentId)
    emitAndDistribute(CONTEXT_SNAPSHOT_ASSEMBLED, execution, resumedState.agentId, snapshotTwo, activeSubscriptions)

    pendingMessagesTwo: List<AgentMessage> = []
    FOR EACH block IN snapshotTwo.blocks
        labelTwo: DataGovernanceLabel = classifyData(
            contextSubjectRef, block.provenance, contextLegalHold, execution, resumedState.agentId
        )
        emitAndDistribute(DATA_CLASSIFIED, execution, resumedState.agentId, labelTwo, activeSubscriptions)

        pendingMessagesTwo.append(AgentMessage(
            id = newMessageId(), role = USER, content = block.content, timestamp = now()
        ))
    END

    responseTwo: ModelResponse = invokeModelForTurn(
        resumedState, execution, pendingMessagesTwo, TRUE, TRUE, FALSE, "", {}, finalModelContent
    )
    emitAndDistribute(MODEL_RESPONSE_RECEIVED, execution, resumedState.agentId, responseTwo, activeSubscriptions)

    modelFinishedTwo: Boolean = responseTwo.finished
    modelProposesToolCallTwo: Boolean = responseTwo.proposedToolCall != NULL

    finalState: AgentState = runTurn(resumedState, execution, modelFinishedTwo, modelProposesToolCallTwo)

    IF finalState.status == COMPLETED
        emitAndDistribute(RUN_COMPLETED, execution, finalState.agentId, finalState, activeSubscriptions)
    ELSE
        emitAndDistribute(TURN_CONTINUED, execution, finalState.agentId, finalState, activeSubscriptions)
    END

    finalSession: SessionState = createOrUpdateSessionCheckpoint(session, finalState, execution, finalState.agentId)
    emitAndDistribute(SESSION_CHECKPOINT_CREATED, execution, finalState.agentId, finalSession, activeSubscriptions)

    RETURN finalState
END
```

`descriptorForCapability(capability: CapabilityId, registeredCapabilities: List<CapabilityDescriptor>)
-> CapabilityDescriptor` es una primitiva asumida — una búsqueda determinista dentro de la misma
lista que `CapabilityRegistry.resolveModelProposedToolCall` ya usó momentos antes, exactamente en
el mismo espíritu que `admissionRulesGrantAccess` (CH-14) o `findAgentConfig` (CH-11): no es una
entidad arquitectónica, no requiere ficha ni registro.

`resolvedAgentId`, `registeredCapabilities`, `registeredSkills`, `situationName`,
`activeSubscriptions`, `usage`, `versionSnapshot`, `auditActor`, `admissionSubjectRef`,
`contextSubjectRef`, `toolAuditSubjectRef`, `proposedCapabilityName`, `proposedRawArguments`,
`argumentsMatchSchema`, `credentialName`, `credentialClassification`,
`credentialBelongsToCapability`, `secretExists`, `credentialExpiresAt`, `idempotencyKey`,
`existingIdempotencyRecord`, `toolExecutionSucceeded`, `toolExecutionOutput`, `contextLegalHold` y
`finalModelContent` son señales de entrada — igual que en CH-12 §11 — que un Ingress Adapter real,
un Secret Store real, un almacén real de registros de idempotencia, o un catálogo administrable de
skills producirían en la práctica; este capítulo no los calcula, los recibe ya dados.
`activationRequest`, en cambio, no es una señal asumida de un componente futuro: es la activación
cruda real con la que arranca la traza completa.

Nótese lo que `runGovernedEnterpriseTurn` **nunca** hace: no decide si la activación debe admitirse
(eso sigue siendo, exactamente igual que en CH-14, de `AdmissionController`); no decide qué gobierno
le aplica a un dato (`DataGovernanceEngine`); no decide qué procedimiento aplica (`SkillLibrary`);
no resuelve el valor real de ningún secreto (`CredentialBroker` produce solo una referencia); no
decide si una ejecución ya ocurrió antes (`IdempotencyGuard`); y no decide qué preservar como
evidencia inmutable más allá de invocar `recordAuditEntry` con los datos ya reales que cada paso
produjo (`AuditLedger`). Cada decisión sigue perteneciendo, exactamente igual que antes, al
componente que ya la posee.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013) ni `AdmissionOutcome`/
`IdempotencyRecordStatus`/`DataClassificationLevel` (embebidos). Es, en cambio, el primer capítulo
en ejercitar con código real la secuencia que empieza ANTES de que exista cualquier `AgentState`:

```text
(evaluateAdmissionForActivationRequest) → AdmissionDecision(REJECT) → [sin AgentRun; RETURN NULL]
(evaluateAdmissionForActivationRequest) → AdmissionDecision(ADMIT)  → [continúa]
(activateAgent)                          → CREATED         (AgentCore, CH-11)
(beginAgentInitialization)               → INITIALIZING    (AgentCore, CH-11)
[este capítulo]                          → RUNNING          (transición de datos, igual que CH-12 §12)
(runTurn: modelProposesToolCall = TRUE)  → WAITING_FOR_TOOL (AgentLoop, CH-01)
[este capítulo, tras credencial+idempotencia+ejecución] → RUNNING
(runTurn: modelFinished = TRUE)          → COMPLETED        (AgentLoop, CH-01)
```

**Por qué la transición `AdmissionDecision(REJECT) → RETURN NULL` no invade la propiedad de
`AgentLoop` sobre `AgentRunStatus` (Article IV).** No hay invasión posible porque, literalmente, no
existe todavía ningún `AgentState` al que invadir — `AdmissionController` decide ANTES del primer
estado de la máquina que `AgentLoop`/`AgentCore` gobiernan, exactamente la separación que Amendment
v1.1 (P-16, "Activation is independent from execution") exige.

## 13. Semántica de Fallos (Failure Semantics)

Este capítulo no introduce ningún código nuevo de `HarnessError` ni ningún valor nuevo de
`ErrorCategory`: reutiliza, sin cambios, los que cada una de las diecisiete funciones invocadas ya
declara — `NO_ADMISSION_RULE_GRANTS_ACCESS` (CH-14, categoría `ADMISSION`),
`CREDENTIAL_CAPABILITY_MISMATCH`/`CREDENTIAL_NOT_FOUND`/`CREDENTIAL_EXPIRED` (CH-16, `CREDENTIAL`),
`IDEMPOTENCY_KEY_CAPABILITY_MISMATCH`/`IDEMPOTENCY_RECORD_ALREADY_COMPLETED` (CH-17,
`IDEMPOTENCY`), `AUDIT_RECORD_MISSING_SUBJECT_REF`/`AUDIT_RECORD_MISSING_ACTOR`/
`AUDIT_RECORD_INCOMPLETE_VERSION_SNAPSHOT` (CH-19, `AUDIT`),
`DATA_GOVERNANCE_LABEL_MISSING_SUBJECT_REF`/`DATA_GOVERNANCE_LABEL_MISSING_PROVENANCE` (CH-20,
`GOVERNANCE`) y `SKILL_RESOLUTION_REQUESTED_WITHOUT_SITUATION`/`SKILL_NOT_FOUND` (CH-24,
`VALIDATION`) — más todos los ya heredados de CH-00..CH-13.

`runGovernedEnterpriseTurn` (sección 11) nunca construye un `HarnessError` por su cuenta —
exactamente la misma disciplina que `runAgentTurnEndToEnd` (CH-12 §13) ya estableció. Cuando
`admission.outcome != ADMIT` o `decisionOne.outcome != ALLOW`, se detiene con un `RETURN` explícito,
dejando que la función correspondiente ya haya construido, dentro de su propio resultado, el
`HarnessError` real que explica por qué.

## 14. Eventos Producidos (Events Produced)

Este capítulo no agrega ningún valor nuevo a `AgentEventType` — reutiliza, sin cambios, los valores
que CH-16 (`CREDENTIAL_RESOLVED`/`CREDENTIAL_RESOLUTION_FAILED`), CH-17
(`IDEMPOTENT_EXECUTION_DETECTED`/`IDEMPOTENCY_CHECK_FAILED`/`IDEMPOTENT_EXECUTION_RECORDED`/
`IDEMPOTENCY_RECORD_CONFLICT`), CH-19 (`AUDIT_RECORD_CREATED`), CH-20
(`DATA_CLASSIFIED`/`RETENTION_ENFORCEMENT_EVALUATED`) y CH-24 (`SKILL_RESOLVED`/
`SKILL_RESOLUTION_FAILED`) ya declararon dentro de sus propios capítulos, sin que ninguna ejecución
real los hubiera producido hasta ahora. Este capítulo es, para cada uno de los seis que sí ejercita
(`CREDENTIAL_RESOLVED`, `IDEMPOTENT_EXECUTION_DETECTED`, `IDEMPOTENT_EXECUTION_RECORDED`,
`AUDIT_RECORD_CREATED`, `DATA_CLASSIFIED`, `SKILL_RESOLVED`), la primera vez que alcanza
`EventBus.distributeEvent` (CH-09) dentro de una ejecución real, vía `emitAndDistribute` (CH-12).

**Hallazgo real, documentado con honestidad.** `AdmissionDecision` sigue sin ningún
`AgentEventType` propio (CH-14 §14, sin cambios) — este capítulo no fabrica uno, ni reutiliza
ninguno existente para ese paso: en su lugar, usa el mecanismo distinto que sí puede preservar esa
decisión sin necesitar un `AgentEvent` (`AuditLedger.recordAuditEntry`, ver sección 2/4). Es la
misma disciplina que CH-13 §14 ya aplicó al no inventar `RUN_CANCELLED`/`RUN_EXPIRED`.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

Este capítulo cierra, con código real, cinco implicaciones de seguridad que Amendment v1.1 exige
y que CH-14/CH-16/CH-17/CH-19/CH-20/CH-24 dejaron, cada uno, modeladas pero sin cablear:

- **Admission antes que ejecución (P-16/P-17, INV-E01/INV-E02)**: ningún `AgentActivationRequest`
  se construye jamás sin una `AdmissionDecision(ADMIT)` real que lo preceda.
- **Credenciales fuera del contexto del modelo (INV-E08)**: `CredentialReference` se resuelve, pero
  nunca se agrega a `candidates`/`pendingMessages` — el modelo nunca ve ni la referencia ni,
  mucho menos, el secreto real.
- **Idempotencia antes del side effect (P-24/INV-11)**: `executeToolCall` nunca se invoca una
  segunda vez para la misma clave de idempotencia si ya existe un `IdempotencyRecord` `COMPLETED`.
- **Gobierno de datos independiente del modelo (P-22/INV-E11)**: cada `ContextBlock` que el modelo
  va a ver ya fue clasificado por `DataGovernanceEngine` — sin que esa clasificación dependa, en
  ningún momento, de que el propio modelo la solicite o la respete.
- **Evidencia distinta de telemetría (P-25)**: la decisión de admisión, la ejecución con
  credencial real, y cada evento que `EventBus` también observa, dejan, además, un `AuditRecord`
  inmutable — sin que los dos mecanismos se conflacionen (CH-19 §15).

Ningún componente cambió su frontera para que esto fuera posible — la seguridad de este capítulo
consiste, otra vez, en traducir con honestidad decisiones ya tomadas, nunca en inventar una nueva.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST RunGovernedEnterpriseTurnReturnsNullWithoutAnyAgentStateWhenAdmissionOutcomeIsReject
TEST RunGovernedEnterpriseTurnRecordsAnAuditEntryForAdmissionWithNullExecutionContext
TEST RunGovernedEnterpriseTurnClassifiesEveryContextBlockBeforeBuildingItsAgentMessage
TEST RunGovernedEnterpriseTurnResolvesASkillForSituationBeforeInvokingTheModel
TEST RunGovernedEnterpriseTurnNeverInvokesExecuteToolCallWhenAnIdempotencyRecordIsAlreadyCompleted
TEST RunGovernedEnterpriseTurnNeverAddsACredentialReferenceToAnyPendingMessage
TEST RunGovernedEnterpriseTurnRecordsAnAuditEntryForEveryRealToolExecution
TEST RunGovernedEnterpriseTurnNeverModifiesAnyAlreadyPublishedComponentFunction
```

Ejemplo concreto para el camino de idempotencia (sección 11): un `existingIdempotencyRecord` con
`status = COMPLETED` y `capability` igual a `callOne.capability` produce que `resultOne` provenga
de `existingRecord.result`, y que `ToolRuntime.executeToolCall` (CH-02) nunca se invoque — verificado
contra `checkIdempotency` (CH-17 §11) sin modificar esa función.

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.1 + Amendment v1.1, después de CH-26)

Contracts (registry/contracts.yaml)
 └── C-001..C-035  (sin cambios — 35 contratos, idéntico a después de CH-24)

Components (registry/components.yaml)
 └── CMP-001..CMP-022  (sin cambios — 22 componentes, idéntico a después de CH-24)
```

**Hallazgo real, verificado y documentado sin ocultarlo.** Como `registry/components.yaml` no
cambia, `diagrams/mindmap/chapter-26.diagram` es, verificado con `./scripts/build-mind-map`,
idéntico en aristas a `diagrams/mindmap/chapter-25.diagram` — mismo hallazgo, por tercera vez, que
CH-12 §17/CH-13 §17 ya documentaron: el `BookMindMap` mecánico no tiene ningún camino para que un
capítulo de integración agregue aristas nuevas sin editar la ficha de un componente ya existente.

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **`OperationalController` (CH-18) y `HandoffCoordinator` (CH-23)**: los caminos de control y de
  traspaso de un turno enterprise —un `ControlDirective` de tipo `KILL_SWITCH` interrumpiendo el
  run en cualquier punto, o un `PolicyDecision(DENY)` severo escalando hacia un humano— quedan,
  deliberadamente, para CH-27, el mismo patrón de división en dos capítulos que CH-12/CH-13 ya
  establecieron para el runtime original.
- **`AgentCommunicationGateway` (CH-15)**: deliberadamente fuera de alcance de CH-26 y de CH-27.
  Su propia frontera (CH-15 §1/§2) es la comunicación ENTRE dos agentes/runs distintos — dos runs
  ya en ejecución, o un run activo delegando hacia un sub-agente — nunca la traza interna de un
  turno individual. Cablearlo exigiría, como mínimo, un segundo `AgentRun` ya activo y un
  `DelegationGrant` ya emitido — dos precondiciones que ningún turno individual, por definición,
  puede producir por sí mismo. Es, para la escala de este capítulo, tan ortogonal como
  `EvaluationHarness`/`ExecutionFabricAdapter` (ver el punto siguiente), aunque por una razón
  distinta: no porque opere en una capa distinta (antes/después de un run), sino porque opera en
  un EJE distinto (entre runs, no dentro de uno).
- **`EvaluationHarness` (CH-22) y `ExecutionFabricAdapter` (CH-21)**: excluidos por instrucción
  explícita de este mismo encargo, y confirmados, al leerlos, con la misma honestidad. Ninguno
  opera en la escala de un turno individual: `EvaluationHarness` certifica un candidato completo
  (agente/skill/policy/modelo/capability) ANTES de su promoción controlada a producción — una
  decisión sobre un candidato, nunca sobre un `AgentRun` ya en curso (CH-22 §1, "completamente
  separado de evaluar una acción dentro de un run ya existente"); `ExecutionFabricAdapter`
  abstrae la topología de despliegue (in-process, worker, Kubernetes, serverless) sobre la que
  corre CUALQUIER run — una decisión de infraestructura que un turno individual ni necesita ni
  podría influir. Cablear cualquiera de los dos dentro de la traza de un turno confundiría una
  decisión de certificación pre-producción o de topología de despliegue con una decisión que
  pertenece, exclusivamente, al ciclo de un run ya activo — exactamente el tipo de conflación que
  Article IV, aplicado a la integración misma, existe para evitar.
- **El cableado real de `runGovernedEnterpriseTurn` DENTRO de `runAgentTurnEndToEnd` (CH-12)**:
  este capítulo escribe una función nueva y paralela, en vez de reabrir `runAgentTurnEndToEnd` para
  agregarle los seis pasos nuevos — el mismo argumento que CH-13 §9 ya usó para no reabrir CH-12.
- **La segunda mitad de `resolveSkillForSituation`** (CH-24 §19: "que `ContextEngine` decida si y
  cómo incluir un `procedureRef` resuelto dentro de lo que ve el modelo"): este capítulo sí decide
  esto (agrega el `procedureRef` como un `AgentMessage` más), pero como una decisión de ESTE
  capítulo de integración, no como un cambio a `ContextEngine.assembleContextSnapshot` (CH-04), que
  sigue sin saber nada de skills.
- **`enforceRetention` (CH-20)**: este capítulo invoca `classifyData`, pero no `enforceRetention` —
  la pregunta de si un dato ya clasificado debería borrarse queda, honestamente, sin ejercitar
  dentro de un turno.
- **Auditoría exhaustiva de cada paso**: este capítulo invoca `recordAuditEntry` en dos puntos
  (la admisión, y la ejecución real de la tool call) — una decisión de alcance deliberada, no un
  intento de auditar cada una de las diecisiete invocaciones de la sección 8.
- Reviewers plurales, evals reales, y orquestación multi-agente propiamente dicha: explícitamente
  fuera de alcance de BH-v0.1, igual que en todos los capítulos anteriores.

## 19. Siguiente Incremento (Next Increment)

El problema natural del próximo capítulo: ¿qué ocurre cuando el camino feliz enterprise que este
capítulo acaba de cablear no es el que corre — cuando un `ControlDirective` de `OperationalController`
(CH-18) interrumpe el run en cualquier punto, o cuando una denegación de `PolicyEngine` es lo
bastante severa como para que, en vez de devolverle la observación al modelo (CH-13), alguien
decida empaquetar el traspaso completo con `HandoffCoordinator` (CH-23)? Ese es, precisamente, el
alcance que este capítulo deja fuera a propósito (ver sección 18) — el "camino de control" que
complementa al camino feliz enterprise de este capítulo, y que CH-27 recorre a continuación.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg /
> Bucles de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows),
> secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): seis capítulos de Amendment v1.1 demostraron, cada uno
   por su cuenta, una función real correcta — sin que ninguno fuera invocado jamás dentro de la
   traza real de un `AgentRun` completo.
2. **Patrones que se repiten** (= §3): el mismo patrón que CH-12 §3 ya describió para los once
   componentes originales — cada capítulo cerró su demostración con disciplina de *ownership*, y
   dejó una nota explícita señalando qué llamada real faltaba.
3. **Estructuras / reglas / incentivos** (= §8): una función de integración nueva,
   `runGovernedEnterpriseTurn`, que invoca las funciones ya publicadas de seis componentes de
   Amendment v1.1 entrelazadas con las de los once de Article III, sin modificar ninguna.
4. **Modelos mentales** (= §4): el Ownership Rule de Article IV nunca exigió que estos seis
   componentes se ignoraran para siempre — exigió que cada uno declarara su frontera antes de que
   existiera código real que pudiera cruzarla.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada capítulo de Amendment v1.1 que se escribió sin cablearse
  hacia el runtime existente hizo crecer la misma lista de deuda intencional que CH-01..CH-11 ya
  generaron para Article III.
- **Bucle de equilibrio (estabiliza):** `runGovernedEnterpriseTurn` verifica el resultado real en
  cada punto de decisión nuevo, y se detiene explícitamente —sin inventar el resto del camino— en
  cuanto ese resultado no es el más permisivo (`admission != ADMIT`, `decisionOne != ALLOW`).

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es invocar `AuditLedger.recordAuditEntry` con
`execution = NULL` sobre la `AdmissionDecision` — antes de que exista cualquier `AgentRun`. Esa
única llamada resuelve, con código real, la tensión que CH-14 §14 documentó honestamente: la
decisión de admisión no puede expresarse jamás como un `AgentEvent` válido, pero sí puede
preservarse como evidencia de auditoría inmutable — exactamente la distinción que P-25 exige entre
telemetría operacional y evidencia de auditoría.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo
> de esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set`
> (frontmatter) y es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. ¿Qué mecanismo, distinto de `EventBus`, preserva la decisión de `AdmissionController` aunque
   todavía no exista ningún `ExecutionContext`? *(cierra la pregunta guía 1)*
2. ¿En qué momento del turno se consulta `SkillLibrary`, respecto a `CapabilityRegistry`? *(cierra
   la pregunta guía 2)*
3. Antes de `executeToolCall`, ¿en qué orden se invocan `CredentialBroker` e `IdempotencyGuard`?
   *(cierra la pregunta guía 3)*
4. ¿En qué punto exacto de la construcción del contexto ocurre la clasificación de
   `DataGovernanceEngine`? *(cierra la pregunta guía 4)*

### Explicar

1. `AdmissionController.evaluateAdmissionForActivationRequest` nunca cambia en este capítulo.
   Explica por qué `AuditLedger` puede preservar su decisión cuando `EventBus` no podría.
2. `IdempotencyGuard.checkIdempotency` sigue recibiendo `existingRecordForKey` como un valor ya
   dado. Explica quién decide, en este capítulo, si `executeToolCall` se invoca o no.

### Conectar

1. ¿Qué señal de entrada de este capítulo representa el "routing" que CH-14 dejó sin resolver?
2. ¿Por qué la clasificación de `DataGovernanceEngine` tiene que ocurrir después de la selección
   de `ContextEngine`, y no antes?
3. ¿Qué le pasaría a `PolicyEngine.evaluate` si alguien le pasara un `SkillDescriptor` en vez de
   un `ToolCall`?
4. ¿Por qué hacían falta tanto `CredentialBroker` como `IdempotencyGuard` antes de que
   `executeToolCall` se invocara con una base real?
5. ¿Por qué este capítulo sí invoca `emitAndDistribute` después de cada `recordAuditEntry`, si
   `AuditLedger` declaró que nunca depende de `EventBus`?

### Espaciar

Las cinco tarjetas de repaso de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas de
nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) — ver `retrieval_set.flashcards` en
`dist/book-ir.json`.

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo.
