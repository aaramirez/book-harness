---
id: CH-27
title: "Integración Enterprise: los Caminos de Control y Traspaso de un Turno Gobernado"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: []
introduces_contracts: []
modifies_contracts: []
constitutional_articles: [P-05, P-10, P-13, P-25, P-30, INV-06, INV-08, INV-09, INV-18, INV-19, INV-20, INV-E10, INV-E12, INV-E14]
previous_chapter: CH-26
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH27
    text: |
      Al terminar este capítulo podrás verificar, para cualquier turno gobernado de nivel
      enterprise que un `ControlDirective` interrumpe a la fuerza o que una denegación de política
      escala hacia control humano, exactamente qué componente real produce esa interrupción o esa
      escalación, y podrás diagnosticar por qué un traspaso estructurado (`HandoffPackage`) es la
      consecuencia natural de ambos caminos — sin que eso confunda nunca la decisión de
      interrumpir (`OperationalController`) con la decisión de empaquetar la transferencia
      (`HandoffCoordinator`).
  skeleton:
    id: SK-CH27
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
    - id: GQ-CH27-01
      text: |
        Un comando operacional ya sabe forzar la terminación de una ejecución sin esperar a que
        el ciclo cognitivo coopere, y ya sabe hacerlo sin invocar ni una sola función del
        componente que decide continuación operacional. Si esa terminación forzada deja un run a
        medio camino, ¿qué le falta todavía a la ejecución para que un humano pueda, de verdad,
        hacerse cargo de lo que quedó pendiente?
      answered_by: RQ-CH27-01
    - id: GQ-CH27-02
      text: |
        Una denegación de autorización ya tiene, desde hace varios capítulos, un camino real que
        le devuelve al modelo una observación para que intente algo distinto. ¿Qué tendría que ser
        distinto en esa denegación para que, en vez de dejar que el modelo lo intente de nuevo,
        alguien decida que un humano debería revisar la situación directamente?
      answered_by: RQ-CH27-02
    - id: GQ-CH27-03
      text: |
        Dos disparadores completamente distintos —un comando operacional forzado desde afuera, y
        una denegación de autorización evaluada desde dentro del propio turno— podrían, ambos,
        terminar produciendo la misma clase de paquete estructurado hacia un humano. ¿Qué tiene
        que seguir siendo cierto sobre quién decide cada uno de los dos disparadores, para que esa
        coincidencia en la forma del traspaso no signifique que un componente empezó a decidir lo
        que le pertenece a otro?
      answered_by: RQ-CH27-03
  systems_lens:
    iceberg_visible_fact: |
      CH-26 cableó, con código real, el camino feliz de un turno enterprise completo — pero
      únicamente el camino en el que nadie interrumpe el run desde afuera y ninguna denegación es
      lo bastante grave como para necesitar a un humano. `OperationalController` (CH-18) y
      `HandoffCoordinator` (CH-23), publicados ambos antes de CH-26, siguieron sin una sola
      ejecución real que los recorriera (ver sección 2, El Problema).
    iceberg_patterns: |
      El mismo patrón que CH-13 §2 ya describió respecto a CH-12 se repite aquí, un nivel más
      arriba: un capítulo de integración que solo demuestra el resultado más permisivo deja, otra
      vez, un componente real (`OperationalController`) y otro (`HandoffCoordinator`) existiendo
      únicamente en demostraciones aisladas — la misma espiral, aplicada ahora a Amendment v1.1
      (ver sección 3).
    iceberg_structures: |
      Este capítulo no instala ningún componente nuevo — instala dos funciones de integración
      nuevas y propias (`interruptGovernedEnterpriseRunWithKillSwitch` y
      `escalateGovernedEnterpriseRunAfterSevereDenial`, sección 11) que invocan las funciones que
      `OperationalController` (CH-18), `HandoffCoordinator` (CH-23) y `AuditLedger` (CH-19) ya
      publicaron — sin modificar el código publicado de ninguno de los tres, ni el de
      `runGovernedEnterpriseTurn` (CH-26).
    iceberg_mental_models: |
      El mismo modelo mental que CH-13 §4 ya estableció para los caminos de gobierno del runtime
      original: cerrar un cable no significa reescribir el componente que produce la señal —
      significa escribir, en un capítulo nuevo, el código que por fin consume esa señal hasta su
      destino real, honrando exactamente el resultado que el componente ya devolvía.
    reinforcing_loop: |
      Cada vez que un capítulo de integración demuestra solo el camino más permisivo, los caminos
      de control y de traspaso siguen existiendo únicamente en prosa — el mismo bucle que CH-18
      §18 y CH-23 §18 señalaron, cada uno por su cuenta, y que CH-26 heredó sin cerrarlo,
      documentándolo con la misma honestidad en su propia sección 18.
    balancing_loop: |
      Cada una de las dos funciones de este capítulo exige, con un `THROW` explícito o con una
      precondición real, que su propio disparador ya haya ocurrido de verdad
      (`applyControlDirective` con `type = KILL_SWITCH` ya aplicado; `PolicyDecision` con
      `outcome = DENY` real) — ninguna asume el resultado que le conviene.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que un `ControlDirective` de tipo
      `KILL_SWITCH` SIEMPRE termine en un `HandoffPackage`, nunca solo en un `AgentState`
      `CANCELLED` silencioso. `OperationalController.applyControlDirective` (CH-18) ya fuerza la
      transición sin cooperación del ciclo cognitivo — pero un run forzado a detenerse a mitad de
      camino deja, casi siempre, trabajo real a medio hacer; `HandoffCoordinator.createHandoffPackage`
      (CH-23) es lo que convierte esa terminación forzada en algo que un humano puede, de verdad,
      continuar.
  recall_questions:
    - id: RQ-CH27-01
      text: |
        ¿Qué función de este capítulo invoca, en qué orden, a `OperationalController.issueControlDirective`,
        `OperationalController.applyControlDirective` y `HandoffCoordinator.createHandoffPackage`, y
        por qué el `HandoffPackage` que produce siempre lleva `reason = KILL_SWITCH`?
      answered_by: RQ-CH27-01
    - id: RQ-CH27-02
      text: |
        ¿Qué precondición exige `escalateGovernedEnterpriseRunAfterSevereDenial` sobre la
        `PolicyDecision` que recibe, y qué construye en su lugar de la observación de denegación
        que `runAgentTurnWithPolicyDenial` (CH-13) ya sabía construir?
      answered_by: RQ-CH27-02
    - id: RQ-CH27-03
      text: |
        ¿Qué invoca este capítulo, además de `createHandoffPackage`, en cada uno de sus dos
        caminos, y por qué esa invocación adicional no depende de que `EventBus` haya distribuido
        nada?
      answered_by: RQ-CH27-03
  explain_prompts:
    - id: EP-CH27-01
      text: |
        `OperationalController.applyControlDirective` (CH-18) nunca cambia una sola línea en este
        capítulo, y sigue sin invocar `ExecutionController.evaluateExecutionContinuation` (CH-07)
        para decidir si el kill switch procede. Explica, como si hablaras con alguien sin contexto
        técnico, por qué eso es exactamente lo que INV-E14 exige — ¿qué se rompería si un kill
        switch tuviera que esperar a que el ciclo cognitivo decidiera revisarlo?
      target_entity: CMP-016
    - id: EP-CH27-02
      text: |
        `HandoffCoordinator.createHandoffPackage` (CH-23) nunca decide si un run debería
        transferirse a un humano — solo empaqueta la transferencia una vez que otro componente ya
        lo decidió. Explica por qué este capítulo puede invocarla desde dos disparadores
        completamente distintos (`OperationalController` y una `PolicyDecision` severa) sin que
        eso signifique que `HandoffCoordinator` empezó a decidir algo que no le pertenece.
      target_entity: CMP-021
  interleaved_questions:
    - id: IQ-CH27-01
      text: |
        `OperationalController.applyControlDirective` (CH-18) fuerza `AgentRunStatus.CANCELLED`
        directamente, sin invocar ningún turno de `AgentLoop.runTurn` (CH-01); CH-13 ya había
        construido `terminateAgentRunOperationally`, que SÍ transiciona hacia `CANCELLED`, pero
        únicamente cuando `ExecutionController.evaluateExecutionContinuation` (CH-07) decide
        `outcome = CANCELLED` desde dentro del propio ciclo. ¿Por qué este capítulo necesita una
        función nueva y distinta de `terminateAgentRunOperationally`, en vez de simplemente
        reutilizarla para el caso del kill switch?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-016, CMP-007, CMP-001, C-028]
      prior_chapter: CH-18
    - id: IQ-CH27-02
      text: |
        `PolicyEngine.evaluatePolicyForToolCall` (CH-05) produce `PolicyDecision.outcome = DENY`
        sin que ese contrato tenga jamás un campo de "severidad"; `HandoffCoordinator.HandoffReason`
        (CH-23) sí declara `EXPLICIT_ESCALATION` como uno de sus cuatro valores posibles. ¿Quién
        decide, en este capítulo, que una denegación concreta merece `EXPLICIT_ESCALATION` en vez
        del camino normal de `runAgentTurnWithPolicyDenial` (CH-13), y por qué esa decisión no
        podría pertenecer, sin violar Article IV, a `PolicyEngine` ni a `HandoffCoordinator` por sí
        solos?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-005, CMP-021, C-014, C-034]
      prior_chapter: CH-05
    - id: IQ-CH27-03
      text: |
        `AuditLedger.recordAuditEntry` (CH-19) ya se invocó en CH-26 sobre una admisión y sobre una
        ejecución real de una tool call. ¿Por qué este capítulo la invoca otra vez sobre un
        `ControlDirective` ya aplicado y sobre un `HandoffPackage` ya creado, y qué tienen en común
        los cuatro usos —admisión, ejecución, control, traspaso— que ninguno de ellos podría
        resolverse pasando, en cambio, por `EventBus.distributeEvent` (CH-09) solamente?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-017, CMP-009, C-029]
      prior_chapter: CH-19
  flashcards:
    - id: FC-CH27-01
      front: |
        ¿Qué tres funciones invoca `interruptGovernedEnterpriseRunWithKillSwitch`, en qué orden, y
        qué `HandoffReason` lleva siempre el `HandoffPackage` que produce?
      back: |
        `issueControlDirective(KILL_SWITCH, ...)` (CH-18), luego `applyControlDirective(...)`
        (CH-18) —que fuerza `AgentRunStatus.CANCELLED` sin invocar `AgentLoop` ni
        `ExecutionController`—, y finalmente `createHandoffPackage(...)` (CH-23) con
        `reason = KILL_SWITCH`: un run detenido a la fuerza siempre se transfiere a un humano, en
        vez de quedar `CANCELLED` sin que nadie continúe lo que quedó pendiente.
      source_entity: CMP-016
      chapter_introduced_in: CH-27
      review_stage: DAY_1
    - id: FC-CH27-02
      front: |
        ¿Qué precondición exige `escalateGovernedEnterpriseRunAfterSevereDenial` sobre la
        `PolicyDecision` que recibe, y qué construye en su lugar de la observación normal?
      back: |
        Exige `decision.outcome == DENY` (lanza `HarnessError` si no) — pero, a diferencia de
        `runAgentTurnWithPolicyDenial` (CH-13), nunca construye una observación de vuelta al
        modelo: construye, en su lugar, un `HandoffPackage` con `reason = EXPLICIT_ESCALATION`,
        transfiriendo la decisión a un humano en vez de dejar que el modelo lo intente de nuevo.
      source_entity: CMP-021
      chapter_introduced_in: CH-27
      review_stage: DAY_1
    - id: FC-CH27-03
      front: |
        ¿Por qué ambas funciones de este capítulo invocan `AuditLedger.recordAuditEntry` (CH-19)
        además de `emitAndDistribute` (CH-12)?
      back: |
        Porque un `ControlDirective` aplicado y un `HandoffPackage` creado son, ambos, decisiones
        críticas que Amendment v1.1 (P-25) exige preservar como evidencia inmutable —
        independientemente de si `EventBus` tenía o no una suscripción activa en ese instante
        (CH-19 §15: los dos mecanismos son ortogonales, nunca se conflacionan).
      source_entity: CMP-017
      chapter_introduced_in: CH-27
      review_stage: DAY_1
    - id: FC-CH27-04
      front: |
        ¿Qué NO resuelve este capítulo, aunque cierra los dos caminos de control/traspaso que
        CH-26 dejó pendientes?
      back: |
        No cablea estas dos funciones DENTRO de `runGovernedEnterpriseTurn` (CH-26) ni dentro de
        `runAgentTurnEndToEnd` (CH-12) — siguen siendo invocaciones alternativas, nunca ramas
        agregadas al pseudocódigo ya publicado de ninguno de los dos. Tampoco modela quién decide
        que una denegación es "severa" (una señal asumida, ver sección 11/18), ni las transiciones
        `PENDING → ACCEPTED → COMPLETED` de `HandoffStatus` (deuda ya heredada de CH-23 §18).
      source_entity: CMP-021
      chapter_introduced_in: CH-27
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH27-01
      recall_question: RQ-CH27-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH27-02
      recall_question: RQ-CH27-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH27-03
      recall_question: RQ-CH27-03
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 27 — Integración Enterprise: los Caminos de Control y Traspaso de un Turno Gobernado

> **Regla constitucional (Amendment v1.1, INV-E14 / INV-E12):** "Kill switches operate
> independently of AgentLoop." / "A human handoff transfers a structured HandoffPackage rather
> than only prose."

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1. El detalle
> estructurado de esta sección vive en `retrieval_set` (frontmatter) y es lo que
> `scripts/validate-retrieval-set` valida automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás verificar, para cualquier turno gobernado
de nivel enterprise que un `ControlDirective` interrumpe a la fuerza o que una denegación de
política escala hacia control humano, exactamente qué componente real produce esa interrupción o
esa escalación, y por qué un traspaso estructurado es la consecuencia natural de ambos caminos.

**Esqueleto.** Este capítulo recorre 19 secciones y, como CH-13 respecto a CH-12, **no introduce
ningún contrato ni ningún componente nuevo** — es el segundo y último capítulo de integración de
Amendment v1.1 planeado para este incremento: cierra los dos caminos que CH-26 dejó explícitamente
pendientes.

**Preguntas guía:**

1. Un comando operacional ya sabe forzar la terminación de una ejecución sin cooperación del
   ciclo cognitivo. Si esa terminación deja un run a medio camino, ¿qué le falta para que un
   humano pueda hacerse cargo?
2. Una denegación ya tiene un camino que le devuelve una observación al modelo. ¿Qué tendría que
   ser distinto para que, en vez de eso, un humano revise la situación?
3. Dos disparadores distintos podrían terminar produciendo la misma clase de paquete hacia un
   humano. ¿Qué tiene que seguir siendo cierto sobre quién decide cada disparador?

## 1. Arquitectura Actual (Current Architecture)

CH-26 escribió, con código real, el camino feliz de un turno gobernado de nivel enterprise —
`AdmissionController` admite, `DataGovernanceEngine` clasifica, `SkillLibrary` resuelve un
procedimiento, `CredentialBroker` resuelve una credencial, `IdempotencyGuard` protege contra doble
ejecución, `AuditLedger` preserva evidencia. Su propia sección 18 documentó, con la misma
honestidad que CH-12 §18 ya estableció para el runtime original, dos componentes reales que
seguían sin una sola ejecución que los recorriera:

1. **`OperationalController` (CH-18)** — `issueControlDirective`/`applyControlDirective` ya saben
   forzar `AgentRunStatus.CANCELLED` sobre un run, sin cooperación del ciclo cognitivo (INV-E14).
   Ningún capítulo, hasta este, invocó jamás esas funciones sobre el `AgentState` real que
   `runGovernedEnterpriseTurn` (CH-26) produce.
2. **`HandoffCoordinator` (CH-23)** — `createHandoffPackage` ya sabe empaquetar la transferencia
   completa de un run/sesión hacia un humano. Ningún capítulo, hasta este, la invocó jamás sobre
   una situación real — ni sobre un kill switch ya aplicado, ni sobre una denegación real de
   `PolicyEngine`.

`runGovernedEnterpriseTurn` (CH-26 §11) nunca invoca ninguna de las dos — y no lo hará en este
capítulo tampoco: exactamente como CH-13 §1 documentó respecto a `runAgentTurnEndToEnd` (CH-12),
"el encargo prohíbe reabrir su pseudocódigo ya publicado". Este capítulo escribe, en cambio, dos
funciones nuevas que representan los dos escenarios que interrumpirían ese camino feliz desde
afuera o que lo desviarían desde dentro.

## 2. El Problema (Problem)

Con el camino feliz enterprise ya recorrido de principio a fin (CH-26), el problema deja de ser
"falta conectar los componentes de Amendment v1.1" — es, otra vez, el mismo problema que CH-13 §2
ya nombró para el runtime original, un nivel más arriba: **este libro nunca ha mostrado qué pasa
cuando alguien, desde afuera, decide detener un run enterprise a la fuerza, o cuando una
denegación es lo bastante grave como para que ni siquiera valga la pena dejar que el modelo lo
intente de nuevo**. Un lector que solo leyera hasta CH-26 aprendería a construir un turno
enterprise que nunca necesita intervención de control ni escalación humana — exactamente el turno
que no existe en producción, la misma observación que CH-13 §2 ya hizo sobre el camino feliz
original.

`OperationalController.applyControlDirective` (CH-18) y `HandoffCoordinator.createHandoffPackage`
(CH-23) existen, ambos, desde hace varios capítulos, sin que ninguna ejecución real los conecte
entre sí ni con el resto del turno enterprise. Necesitamos, por fin, el resto de la traza real: qué
pasa con un run cuando un kill switch lo interrumpe, y qué pasa con una denegación cuando, en vez
de devolverle la observación al modelo, alguien decide que un humano debe intervenir directamente.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los treinta y cinco contratos y los veintidós componentes — más `runGovernedEnterpriseTurn`
(CH-26) — no bastan porque:

- `OperationalController.issueControlDirective`/`applyControlDirective` (CH-18 §11) llevan varios
  capítulos publicadas sin que ninguna ejecución real las invocara sobre el `AgentState` que un
  turno enterprise (CH-26) produce;
- `HandoffCoordinator.createHandoffPackage` (CH-23 §11) sigue, hasta este capítulo, sin ninguna
  invocación real — solo con el ejemplo aislado que su propio capítulo construyó (CH-23 §11, "el
  ejemplo... prueba que el mecanismo funciona, no que ya esté conectado dentro de un flujo real");
- nada, hasta este capítulo, demuestra con código que un kill switch aplicado y una denegación
  severa pueden, ambos, converger en la misma forma de traspaso estructurado sin que eso confunda
  las dos decisiones de origen.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la
> secuencia `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una
> entidad que no haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT`
> registrado — **no magic entities**. Este capítulo hereda la misma disciplina que CH-12/CH-13/
> CH-26 ya aplicaron: no define ni un solo `STRUCT`/`ENUM`/`COMPONENT` nuevo.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-05   Side effects pass through policy.
           escalateGovernedEnterpriseRunAfterSevereDenial nunca invoca executeToolCall — la
           denegación ya decidió que la acción no procede; empaquetar un traspaso no es un side
           effect sobre el mundo externo que PolicyEngine deba evaluar de nuevo.
    P-10   The harness owns execution state—not the model.
           interruptGovernedEnterpriseRunWithKillSwitch construye, vía applyControlDirective
           (CH-18), el AgentState CANCELLED de un run enterprise real — el harness, nunca el
           modelo, decide ese desenlace, y lo decide sin que el modelo participe en absoluto.
    P-13   Authorization is deterministic and external to the LLM.
           La decisión de que una PolicyDecision es "severa" (parámetro assumed de este capítulo,
           ver sección 11) nunca consulta al modelo — es, exactamente igual que
           evaluatePolicyForToolCall (CH-05), una señal determinista externa a él.
    P-25   Audit evidence is distinct from operational telemetry.
           Ambas funciones de este capítulo invocan recordAuditEntry (CH-19) ADEMÁS de
           emitAndDistribute (CH-12) — un ControlDirective aplicado y un HandoffPackage creado son,
           los dos, decisiones críticas que merecen evidencia inmutable, no solo telemetría.
    P-30   Operational control can override autonomy.
           Primera cita literal con ejecución real de punta a punta sobre un turno enterprise
           completo: un ControlDirective de tipo KILL_SWITCH interrumpe runGovernedEnterpriseTurn
           (CH-26) sin que ninguna cooperación del ciclo cognitivo sea necesaria.

Invariants preserved
    INV-06   Todo side effect pasa por PolicyEngine.        (heredado, sin cambios de CH-26)
    INV-08   El harness es propietario del execution state. (heredado — ver P-10)
    INV-09   Todo AgentRun tiene límites explícitos.         (heredado, sin cambios de CH-26)
    INV-18   Toda acción significativa produce un evento observable. (ver sección 14)
    INV-19   Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy relevante.
             Cada AuditRecord de este capítulo trae un actor (ActorId) real — issuedBy en el
             camino del kill switch, auditActor en el camino de escalación.
    INV-20   Todo error operacional pertenece a una categoría conocida. (ver sección 13)
    INV-E10  Every production run records exact versions of agent, skill, policy, model
             configuration and capability contracts.
             Cada recordAuditEntry de este capítulo recibe un VersionSnapshot real — mismo patrón
             que CH-26 ya estableció.
    INV-E12  A human handoff transfers a structured HandoffPackage rather than only prose.
             Primera cita literal con ejecución real, dos veces: createHandoffPackage (CH-23) se
             invoca con datos reales producidos por este mismo capítulo (KILL_SWITCH,
             EXPLICIT_ESCALATION) — nunca con un resumen de texto libre.
    INV-E14  Kill switches operate independently of AgentLoop.
             Primera cita literal con ejecución real sobre un AgentState producido por
             runGovernedEnterpriseTurn (CH-26): applyControlDirective (CH-18) transiciona el run
             sin invocar AgentLoop.runTurn (CH-01) ni ExecutionController.evaluateExecutionContinuation
             (CH-07).

Component ownership changes
    Ninguno. introduces_components: [] — este capítulo no instala ningún componente nuevo, y no
    modifica ni un solo campo owns/does_not_own/consumes/produces/dependencies de ninguna de las
    veintidós fichas ya registradas.

Lifecycle changes
    Ninguna modificación a AgentRunStatus (C-013) ni a ControlDirectiveType/ControlDirectiveStatus/
    HandoffReason/HandoffStatus (embebidos, CH-18/CH-23). Este capítulo es, en cambio, el primero
    en ejercitar con código real que un AgentState producido por un turno enterprise (CH-26) puede
    alcanzar CANCELLED por la vía del kill switch, en vez de por la vía de
    ExecutionController.evaluateExecutionContinuation (CH-07/CH-13).

Security implications
    Este capítulo demuestra, con código real, que un run forzado a detenerse nunca queda
    simplemente CANCELLED sin que nadie continúe el trabajo pendiente — ver sección 15.

Observability implications
    Primera ejecución real, en este libro, de CONTROL_DIRECTIVE_APPLIED y HANDOFF_PACKAGE_CREATED
    (CH-18/CH-23) hacia EventBus.distributeEvent (CH-09), y de sus AuditRecord equivalentes hacia
    AuditLedger (CH-19) — ambos mecanismos, otra vez, sin conflacionarse (ver sección 14).

Deterministic vs agentic boundary
    Sin cambios de fondo: los dos caminos de este capítulo dependen de un ControlDirective ya
    aplicado y de una PolicyDecision ya evaluada, ambos deterministas desde sus propios capítulos
    — ninguna rama nueva de este capítulo consulta al modelo para decidir su propio desenlace.
```

## 5. Conceptos Nuevos (New Concepts)

Este capítulo no introduce ningún concepto que amerite una entrada propia en
`registry/glossary.yaml` (que, deliberadamente, no toca). Introduce una idea puramente narrativa:

- **Traspaso como consecuencia, no como decisión (Handoff as Consequence)**: la observación de que
  tanto una interrupción forzada (`OperationalController`) como una denegación severa
  (`PolicyEngine`) pueden, ambas, converger hacia la misma forma de traspaso estructurado
  (`HandoffCoordinator.createHandoffPackage`) sin que ninguno de los dos componentes de origen
  decida jamás CÓMO se empaqueta esa transferencia — esa decisión sigue perteneciendo,
  exclusivamente, a `HandoffCoordinator`.

## 6. Nuevas Estructuras de Datos (New Data Structures)

**Este capítulo no introduce ningún `STRUCT` ni `ENUM` nuevo.** Reutiliza, sin modificar ni un solo
campo, los contratos ya registrados desde CH-00..CH-26: `ControlDirective` (C-028, CH-18) y
`HandoffPackage` (C-034, CH-23), además de los ya usados por CH-26.

Dos tipos embebidos, sin `C-XXX` propio, necesitan documentarse aquí por referencia — el mismo
mecanismo que CH-12/CH-13/CH-26 §6 ya usaron:

| Identificador (heredado, sin `C-XXX` propio) | Introducido en | Rol en este capítulo |
|---|---|---|
| `ControlDirectiveApplication` | CH-18 §6 | tipo del resultado que `applyControlDirective` (CH-18) devuelve — este capítulo lee su campo `updatedAgentState` |
| `VersionSnapshot` | CH-19 §6 | tipo del parámetro `versionSnapshot` que este capítulo pasa, ya dado, a cada invocación de `recordAuditEntry` (CH-19) |

`ActorId` (CH-06 §6) ya quedó disponible para todo capítulo posterior desde que CH-13/CH-18/CH-19/
CH-23/CH-26 lo redeclararon cada uno en su propia sección 6 — este capítulo lo redeclara aquí una
vez más, por el mismo motivo (la disponibilidad de un identificador sin `C-XXX` propio no es
acumulativa entre capítulos, `scripts/lib/chapter-parser.js`):

| Identificador (heredado, sin `C-XXX` propio) | Introducido en | Rol en este capítulo |
|---|---|---|
| `ActorId` | CH-06 §6 | tipo de `issuedBy` (`issueControlDirective`, CH-18) y de `auditActor`/`transferTo` (este capítulo) |

**Unchanged**: ningún otro tipo heredado cambia de forma. Este capítulo no introduce ninguna
primitiva de generación de identificador nueva.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

**Este capítulo no introduce ningún contrato nuevo.** `introduces_contracts: []` en el
frontmatter — `registry/contracts.yaml` permanece, después de este capítulo, exactamente en
`C-001`..`C-035`.

## 8. Responsabilidades de Componentes (Component Responsibilities)

**Este capítulo no introduce ningún componente nuevo.** `introduces_components: []` en el
frontmatter — `registry/components.yaml` permanece, después de este capítulo, exactamente en
`CMP-001`..`CMP-022`, sin que ninguna de sus fichas cambie un solo campo.

Lo que este capítulo sí hace es escribir dos funciones nuevas y propias que representan los dos
escenarios que CH-26 dejó pendientes:

```text
Función nueva                                    Disparador                        Camino que cierra
------------------------------------------------ ---------------------------------- -----------------
interruptGovernedEnterpriseRunWithKillSwitch      ControlDirective (KILL_SWITCH)     interrupción forzada
escalateGovernedEnterpriseRunAfterSevereDenial     PolicyDecision (DENY, "severa")    escalación por denegación
```

Cada una de las veintidós fichas ya publicadas se respeta exactamente: `OperationalController`
sigue sin decidir si un run debe transferirse a un humano; `HandoffCoordinator` sigue sin decidir
si un kill switch debe aplicarse ni si una denegación es lo bastante severa;
`PolicyEngine`/`ExecutionController` siguen sin producir, jamás, un `HandoffPackage` por su
cuenta. Ninguna decisión cambió de dueño — este capítulo solo escribe el código que traduce dos
decisiones ya tomadas, por dos componentes distintos, hacia la misma forma de consecuencia.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
interruptGovernedEnterpriseRunWithKillSwitch (función de integración, no un componente registrado)
    invoca → issueControlDirective, applyControlDirective (CMP-016)
    invoca → createHandoffPackage (CMP-021)
    invoca → recordAuditEntry (CMP-017)
    invoca → emitAndDistribute → distributeEvent (CMP-009)

escalateGovernedEnterpriseRunAfterSevereDenial
    invoca → createHandoffPackage (CMP-021)
    invoca → recordAuditEntry (CMP-017)
    invoca → emitAndDistribute → distributeEvent (CMP-009)
```

**Límite real de este capítulo, documentado con la misma honestidad que CH-12/CH-13/CH-26 §9.**
`registry/components.yaml` **no se modifica** — ninguna de las veintidós fichas agrega, en su
propio campo `dependencies`, a ninguno de sus vecinos. `diagrams/mindmap/chapter-27.diagram` no
gana, por el mismo mecanismo ya documentado tres veces, ninguna arista `DEPENDS_ON`/`PRODUCES`/
`CONSUMES` nueva.

Un límite adicional, propio de este capítulo: ninguna de las dos funciones nuevas se invoca desde
dentro de `runGovernedEnterpriseTurn` (CH-26) ni de `runAgentTurnEndToEnd` (CH-12) — el encargo
prohíbe reabrir el pseudocódigo ya publicado de cualquiera de los dos. Cablear la sustitución real
de un punto de `runGovernedEnterpriseTurn` por una llamada a una de estas dos funciones sigue
siendo, honestamente, trabajo de una revisión futura (ver sección 18).

## 10. Diagrama de Secuencia (Sequence Diagram)

Dos vistas, una por camino (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §14):

**Vista 1 — Componentes**

```text
Camino kill switch:
    OperationalController → OperationalController → HandoffCoordinator → AuditLedger
    (EventBus recibe cada AgentEvent producido)

Camino escalación por denegación:
    PolicyEngine (ya evaluado) → [escalateGovernedEnterpriseRunAfterSevereDenial] →
    HandoffCoordinator → AuditLedger
```

**Vista 2 — Sequence**

```text
ControlDirective (type = KILL_SWITCH, emitido por issueControlDirective)
   ▼
interruptGovernedEnterpriseRunWithKillSwitch
   │ applyControlDirective(directive, targetState, execution)
   │   → ControlDirectiveApplication(updatedAgentState = AgentState(status = CANCELLED))
   │ EMIT CONTROL_DIRECTIVE_APPLIED → EventBus (vía emitAndDistribute)
   │ recordAuditEntry(targetRef, versionSnapshot, issuedBy, execution, agentId) → AuditRecord
   ▼
createHandoffPackage(runId, sessionId, reason = KILL_SWITCH, contextRef, transferTo, ...)
   │ → HandoffPackage(status = PENDING)
   │ EMIT HANDOFF_PACKAGE_CREATED → EventBus
   │ recordAuditEntry(contextRef, versionSnapshot, transferTo, execution, agentId) → AuditRecord
   ▼
HandoffPackage — un humano puede, ahora, hacerse cargo del run ya CANCELLED

---

PolicyDecision (outcome = DENY, ya evaluada por PolicyEngine — CH-05/CH-13)
   ▼
escalateGovernedEnterpriseRunAfterSevereDenial
   │ ¿decision.outcome == DENY? — NO → THROW HarnessError(NOT_A_SEVERE_DENIAL)
   ▼ SÍ
createHandoffPackage(runId, sessionId, reason = EXPLICIT_ESCALATION, contextRef, transferTo, ...)
   │ → HandoffPackage(status = PENDING)
   │ EMIT HANDOFF_PACKAGE_CREATED → EventBus (si execution/agentId reales)
   │ recordAuditEntry(contextRef, versionSnapshot, auditActor, execution, agentId) → AuditRecord
   ▼
HandoffPackage — un humano revisa la denegación directamente, sin que el modelo la vea primero
```

**Vista 3 — Pseudocódigo**

Ver §11: las dos funciones son la primera formalización ejecutable, en todo este libro, de "qué
pasa cuando un run enterprise se interrumpe a la fuerza, o cuando una denegación no debería
volver, siquiera, al modelo" — construidas exclusivamente a partir de funciones ya publicadas por
CH-00..CH-26, sin modificar ninguna.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya registradas desde CH-00..CH-26, más `ControlDirectiveApplication`,
`VersionSnapshot` y `ActorId` (sección 6, disponibles por referencia).

```pseudocode
FUNCTION interruptGovernedEnterpriseRunWithKillSwitch(
    targetState: AgentState,
    execution: ExecutionContext,
    targetRef: Text,
    issuedBy: ActorId,
    versionSnapshot: VersionSnapshot,
    transferTo: ActorId,
    contextRef: Text,
    activeSubscriptions: List<EventSubscription>
) -> HandoffPackage

    // el disparador (decidir que este run concreto debe interrumpirse) ya ocurrio afuera de
    // esta funcion — issueControlDirective solo construye el comando ya decidido (CH-18 sec11).
    directive: ControlDirective = issueControlDirective(KILL_SWITCH, targetRef, issuedBy)

    application: ControlDirectiveApplication = applyControlDirective(directive, targetState, execution)
    // applyControlDirective (CH-18) fuerza CANCELLED sin invocar AgentLoop.runTurn ni
    // ExecutionController.evaluateExecutionContinuation — INV-E14 con codigo real (ver sec4).

    IF application.updatedAgentState != NULL
        emitAndDistribute(
            CONTROL_DIRECTIVE_APPLIED, execution, targetState.agentId, application.directive, activeSubscriptions
        )
    END

    controlAudit: AuditRecord = recordAuditEntry(
        targetRef, versionSnapshot, issuedBy, execution, targetState.agentId
    )
    emitAndDistribute(AUDIT_RECORD_CREATED, execution, targetState.agentId, controlAudit, activeSubscriptions)

    // un run detenido a la fuerza casi siempre deja trabajo real a medio hacer — el kill switch
    // por si solo nunca es suficiente; el traspaso estructurado es la consecuencia natural.
    package: HandoffPackage = createHandoffPackage(
        execution.runId, execution.sessionId, KILL_SWITCH, contextRef, transferTo, NULL,
        execution, targetState.agentId
    )
    emitAndDistribute(HANDOFF_PACKAGE_CREATED, execution, targetState.agentId, package, activeSubscriptions)

    handoffAudit: AuditRecord = recordAuditEntry(
        contextRef, versionSnapshot, transferTo, execution, targetState.agentId
    )
    emitAndDistribute(AUDIT_RECORD_CREATED, execution, targetState.agentId, handoffAudit, activeSubscriptions)

    RETURN package
END
```

```pseudocode
FUNCTION escalateGovernedEnterpriseRunAfterSevereDenial(
    decision: PolicyDecision,
    runId: RunId,
    sessionId: SessionId,
    execution: Optional<ExecutionContext>,
    agentId: Optional<AgentId>,
    versionSnapshot: VersionSnapshot,
    auditActor: ActorId,
    transferTo: ActorId,
    contextRef: Text,
    activeSubscriptions: List<EventSubscription>
) -> HandoffPackage

    IF decision.outcome != DENY
        error: HarnessError = HarnessError(
            category = VALIDATION,
            code = "NOT_A_SEVERE_DENIAL",
            message = "escalateGovernedEnterpriseRunAfterSevereDenial fue invocada sobre una PolicyDecision cuyo outcome no es DENY",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW error
    END

    // que ESTA denegacion concreta merezca escalar (en vez de seguir el camino normal de
    // runAgentTurnWithPolicyDenial, CH-13) es una senal ya decidida afuera de esta funcion —
    // PolicyDecision (C-014) no declara ningun campo de severidad propio; quien invoca esta
    // funcion en vez de runAgentTurnWithPolicyDenial ya tomo esa decision (ver seccion 18).

    package: HandoffPackage = createHandoffPackage(
        runId, sessionId, EXPLICIT_ESCALATION, contextRef, transferTo, NULL, execution, agentId
    )

    IF execution != NULL AND agentId != NULL
        emitAndDistribute(HANDOFF_PACKAGE_CREATED, execution, agentId, package, activeSubscriptions)
    END

    escalationAudit: AuditRecord = recordAuditEntry(contextRef, versionSnapshot, auditActor, execution, agentId)

    IF execution != NULL AND agentId != NULL
        emitAndDistribute(AUDIT_RECORD_CREATED, execution, agentId, escalationAudit, activeSubscriptions)
    END

    RETURN package
END
```

Nótese lo que ninguna de las dos funciones hace: ninguna decide si un kill switch debe aplicarse
(`OperationalController` sigue siendo quien lo decide, afuera, antes de que
`interruptGovernedEnterpriseRunWithKillSwitch` se invoque); ninguna decide si una denegación es lo
bastante severa como para escalar en vez de devolver la observación normal (una señal ya decidida
afuera, exactamente igual que `resolvedAgentId` en CH-26 §11 representaba un routing ya resuelto);
y ninguna decide CÓMO se empaqueta el traspaso (`HandoffCoordinator.createHandoffPackage`, CH-23,
sigue siendo quien construye el `HandoffPackage` real). Cada una solo traduce, hacia la misma
consecuencia estructurada, una decisión que dos componentes distintos ya tomaron por caminos
distintos.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013) ni `HandoffStatus`/`HandoffReason`
(embebidos, CH-23). Es, en cambio, el primer capítulo en ejercitar con código real, sobre un
`AgentState` que un turno enterprise (CH-26) produjo, la transición forzada de kill switch:

```text
RUNNING | WAITING_FOR_TOOL | WAITING_FOR_HUMAN --[ControlDirective(KILL_SWITCH) APPLIED]--> CANCELLED
    (interruptGovernedEnterpriseRunWithKillSwitch — sin invocar AgentLoop.runTurn, INV-E14)
    → siempre acompañado de un HandoffPackage(status = PENDING) nuevo
```

**Por qué esto no invade la propiedad de `AgentLoop` sobre `AgentRunStatus` (Article IV).** La
transición hacia `CANCELLED` la construye, con código real, `OperationalController.applyControlDirective`
(CH-18) — este capítulo solo invoca esa función ya existente, exactamente igual que CH-13 §12 ya
argumentó para `terminateAgentRunOperationally`. `HandoffCoordinator.createHandoffPackage` (CH-23),
por su parte, nunca construye ni lee ningún `AgentRunStatus` — su propio `HandoffPackage` correlaciona
el traspaso con el run vía `runId`/`sessionId` (campos opacos), nunca reescribiendo su estado.

## 13. Semántica de Fallos (Failure Semantics)

Este capítulo no introduce ningún código nuevo de `HarnessError`, salvo uno propio de este
capítulo (no de ningún componente): `NOT_A_SEVERE_DENIAL` (categoría `VALIDATION`, `recoverable =
FALSE`, `retryable = FALSE`) — la misma disciplina de precondición explícita que
`runAgentTurnWithPolicyDenial`/`terminateAgentRunOperationally` (CH-13 §11) ya establecieron para
sus propias funciones de integración. Reutiliza, sin cambios, el resto de las categorías ya
declaradas por `OperationalController` (`CONTROL`: `CONTROL_DIRECTIVE_MISSING_TARGET_REF`,
`CONTROL_DIRECTIVE_ALREADY_APPLIED`, `KILL_SWITCH_MISSING_TARGET_CONTEXT`,
`KILL_SWITCH_ON_TERMINAL_AGENT_STATE`, CH-18 §13), `HandoffCoordinator` (`HANDOFF`:
`HANDOFF_PACKAGE_MISSING_RUN_ID`, CH-23 §13) y `AuditLedger` (`AUDIT`, CH-19 §13).

Ninguna de las dos funciones de este capítulo reclasifica esos fallos ni les agrega ninguna
categoría nueva más allá de la única mencionada arriba.

## 14. Eventos Producidos (Events Produced)

Este capítulo no agrega ningún valor nuevo a `AgentEventType` — reutiliza, sin cambios, los que
CH-18 (`CONTROL_DIRECTIVE_APPLIED`) y CH-23 (`HANDOFF_PACKAGE_CREATED`) ya declararon, y el que
CH-19 (`AUDIT_RECORD_CREATED`) ya declaró. Es, para cada uno de los tres, la primera vez que
alcanza `EventBus.distributeEvent` (CH-09) dentro de una ejecución real, vía `emitAndDistribute`
(CH-12) — exactamente el mismo "cierre de cableado" (CH-12 §5) que CH-26 §14 ya demostró para seis
tipos de evento distintos, aplicado ahora a estos dos componentes.

**Nota de consistencia con CH-19 §15.** Cada una de las dos funciones de este capítulo invoca
`recordAuditEntry` (produciendo un `AuditRecord`) Y `emitAndDistribute` (distribuyendo un
`AgentEvent`) para la MISMA decisión — la demostración concreta, con código real, de que los dos
mecanismos coexisten sin conflacionarse: uno preserva evidencia inmutable, el otro distribuye
telemetría operacional a quien esté suscrito en ese instante.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

Este capítulo cierra, con código real, dos implicaciones de seguridad que Amendment v1.1 exige y
que CH-18/CH-23 dejaron modeladas pero sin cablear:

- **Un kill switch nunca termina en un silencio operacional (P-30/INV-E14)**:
  `interruptGovernedEnterpriseRunWithKillSwitch` demuestra que forzar `CANCELLED` sin cooperación
  del ciclo cognitivo SIEMPRE se acompaña de un `HandoffPackage` — el trabajo que el run dejó a
  medio hacer nunca queda sin que un humano, al menos, tenga cómo hacerse cargo de él.
- **Una escalación explícita nunca deja que el modelo decida por sí mismo qué hacer con su propia
  denegación (INV-E12)**: `escalateGovernedEnterpriseRunAfterSevereDenial` nunca construye la
  observación normal que `runAgentTurnWithPolicyDenial` (CH-13) construiría — el `HandoffPackage`
  que produce transfiere la decisión completa a un humano, en vez de dejar que el modelo la vea y
  proponga otra cosa.

Ningún componente cambió su frontera para que esto fuera posible — la seguridad de este capítulo
consiste, otra vez, en traducir con honestidad dos decisiones ya tomadas hacia la misma
consecuencia estructurada, nunca en inventar una nueva.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST InterruptGovernedEnterpriseRunWithKillSwitchNeverInvokesAgentLoopOrExecutionController
TEST InterruptGovernedEnterpriseRunWithKillSwitchAlwaysProducesAHandoffPackageWithReasonKillSwitch
TEST EscalateGovernedEnterpriseRunAfterSevereDenialThrowsWhenPolicyDecisionOutcomeIsNotDeny
TEST EscalateGovernedEnterpriseRunAfterSevereDenialNeverBuildsTheNormalPolicyDenialObservation
TEST BothFunctionsInvokeRecordAuditEntryInAdditionToEmitAndDistributeForTheSameDecision
TEST NeitherFunctionModifiesAnyAlreadyPublishedComponentFunction
```

Ejemplo concreto para el camino del kill switch (sección 11): un `targetState` con
`status = WAITING_FOR_TOOL` y un `ControlDirective(type = KILL_SWITCH)` recién emitido producen,
vía `applyControlDirective` (CH-18 §11), un `updatedAgentState` con `status = CANCELLED` — y, a
continuación, un `HandoffPackage(reason = KILL_SWITCH, status = PENDING)` real, verificado contra
`createHandoffPackage` (CH-23 §11) sin modificar ninguna de las dos funciones.

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.1 + Amendment v1.1, después de CH-27)

Contracts (registry/contracts.yaml)
 └── C-001..C-035  (sin cambios — 35 contratos, idéntico a después de CH-26)

Components (registry/components.yaml)
 └── CMP-001..CMP-022  (sin cambios — 22 componentes, idéntico a después de CH-26)
```

**Hallazgo real, verificado y documentado sin ocultarlo.** Como `registry/components.yaml` no
cambia, `diagrams/mindmap/chapter-27.diagram` es, verificado con `./scripts/build-mind-map`,
idéntico en aristas a `diagrams/mindmap/chapter-26.diagram` — el mismo hallazgo, por cuarta vez,
que CH-12/CH-13/CH-26 ya documentaron cada uno por su cuenta.

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado real de estas dos funciones DENTRO de `runGovernedEnterpriseTurn` (CH-26) o de
  `runAgentTurnEndToEnd` (CH-12)**: ambas siguen siendo invocaciones alternativas e independientes
  — el encargo prohíbe reabrir el pseudocódigo ya publicado de cualquiera de los dos.
- **Quién decide que una `PolicyDecision` concreta es "severa"**: `escalateGovernedEnterpriseRunAfterSevereDenial`
  recibe esa decisión ya tomada, sin modelar el mecanismo real que la produciría — `PolicyDecision`
  (C-014) no declara ningún campo de severidad propio, y este capítulo no le agrega uno (eso sería
  modificar un contrato ya publicado, fuera del alcance de este encargo). Queda, honestamente,
  como una señal asumida — mismo tratamiento que CH-23 §9 ya dio a la misma pregunta en prosa
  ("salvo que una policy explícita decida que una `REQUIRE_APPROVAL` reiterada... constituye, en
  la práctica, un `EXPLICIT_ESCALATION`").
- **Las transiciones `PENDING → ACCEPTED → COMPLETED` de `HandoffStatus`**: deuda ya heredada de
  CH-23 §18, sin cambios — ningún `HandoffPackage` que este capítulo produce transiciona jamás más
  allá de `PENDING`.
- **Múltiples `ControlDirective` concurrentes sobre el mismo run, o una `PolicyDecision` severa
  que llega después de que el run ya fue interrumpido por un kill switch**: fuera de alcance,
  mismo límite que CH-18 §18 ya documentó para el "empate" con `ExecutionController`.
- **`AgentCommunicationGateway` (CH-15), `EvaluationHarness` (CH-22) y `ExecutionFabricAdapter`
  (CH-21)**: las mismas tres exclusiones que CH-26 §18 ya justificó, sin cambios — ninguno opera
  en la escala de un turno individual ni en la de su interrupción/traspaso.
- Reviewers plurales, evals reales, y orquestación multi-agente propiamente dicha: explícitamente
  fuera de alcance de BH-v0.1, igual que en todos los capítulos anteriores.

## 19. Siguiente Incremento (Next Increment)

Con este capítulo, ocho de los nueve componentes de Amendment v1.1 tienen, entre CH-26 y CH-27,
al menos una integración real dentro de la traza de un turno individual — `AdmissionController`,
`CredentialBroker`, `IdempotencyGuard`, `OperationalController`, `AuditLedger`,
`DataGovernanceEngine`, `HandoffCoordinator` y `SkillLibrary`. El noveno,
`AgentCommunicationGateway` (CH-15), permanece deliberadamente sin cablear en esta escala, por la
razón documentada en CH-26 §18: su propia frontera opera entre dos agentes/runs, no dentro de uno.
`EvaluationHarness` (CH-22) y `ExecutionFabricAdapter` (CH-21) permanecen, igualmente, fuera de
esta escala por diseño — pre-producción y topología de despliegue, respectivamente.

No hay, en este momento del libro, un tercer capítulo de integración de Amendment v1.1 planeado
para esta escala. `next_chapter` queda en `null` en el frontmatter de este capítulo. Los problemas
reales que sí quedan, para quien continúe este libro más allá de este incremento, son exactamente
los que la sección 18 acaba de nombrar — ninguno exige un componente nuevo: todos son
refinamientos sobre los veintidós componentes ya existentes, sobre las funciones de integración
que CH-12/CH-13/CH-26 y este capítulo ya escribieron, o sobre la pregunta, todavía abierta desde
CH-15 §19, de si el próximo incremento debería, en cambio, profundizar el Agent Interoperability
Plane, el Execution Plane, o cablear por fin `AgentCommunicationGateway` entre dos runs reales.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg /
> Bucles de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows),
> secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2): CH-26 recorrió el camino feliz de un turno enterprise, pero solo en
   el mundo donde nadie interrumpe el run y ninguna denegación necesita a un humano.
2. **Patrones que se repiten** (= §3): un capítulo de integración que solo demuestra el camino más
   permisivo deja, otra vez, componentes reales existiendo únicamente en demostraciones aisladas.
3. **Estructuras / reglas / incentivos** (= §8): dos funciones nuevas, cada una atada a un
   disparador real y distinto, sin modificar el pseudocódigo ya publicado de ningún componente ni
   de ninguna función de integración anterior.
4. **Modelos mentales** (= §4/§5): cerrar un cable no significa reescribir el componente que
   produce la señal — significa escribir el código que por fin la consume hasta su destino real.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada capítulo que demuestra solo el camino más permisivo deja
  los caminos de control/traspaso como deuda que se repite, capítulo tras capítulo, exactamente
  igual que CH-05/CH-06/CH-07 lo hicieron para CH-12, y CH-18/CH-23 lo hicieron para CH-26.
- **Bucle de equilibrio (estabiliza):** cada una de las dos funciones de este capítulo exige, con
  un `THROW` explícito o una precondición real, que su propio disparador ya haya ocurrido de
  verdad — ninguna asume el resultado que le conviene.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que un `ControlDirective` de tipo `KILL_SWITCH`
SIEMPRE produzca un `HandoffPackage`, nunca solo un `AgentState` `CANCELLED` silencioso — la
diferencia entre un run que simplemente se detuvo y un run cuyo trabajo pendiente alguien, de
verdad, puede continuar.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo
> de esta sección vive en `retrieval_set` (frontmatter) y es lo que
> `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Si una terminación forzada deja un run a medio camino, ¿qué le falta para que un humano pueda
   hacerse cargo? *(cierra la pregunta guía 1)*
2. ¿Qué tendría que ser distinto en una denegación para que, en vez de dejar que el modelo lo
   intente de nuevo, un humano revise la situación? *(cierra la pregunta guía 2)*
3. ¿Qué tiene que seguir siendo cierto sobre quién decide cada disparador, para que converger en
   la misma forma de traspaso no confunda las dos decisiones de origen? *(cierra la pregunta guía 3)*

### Explicar

1. `OperationalController.applyControlDirective` nunca invoca `ExecutionController` para decidir
   si el kill switch procede. Explica por qué eso es exactamente lo que INV-E14 exige.
2. `HandoffCoordinator.createHandoffPackage` nunca decide si un run debería transferirse. Explica
   por qué este capítulo puede invocarla desde dos disparadores distintos sin invadir su frontera.

### Conectar

1. ¿Por qué este capítulo necesita una función nueva, distinta de `terminateAgentRunOperationally`
   (CH-13), para el caso del kill switch?
2. ¿Quién decide, en este capítulo, que una denegación merece escalación en vez del camino normal
   de `runAgentTurnWithPolicyDenial` (CH-13)?
3. ¿Qué tienen en común los cuatro usos de `AuditLedger` a través de CH-26 y este capítulo
   (admisión, ejecución, control, traspaso)?

### Espaciar

Las cuatro tarjetas de repaso de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas de
nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) — ver `retrieval_set.flashcards` en
`dist/book-ir.json`.

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo.
