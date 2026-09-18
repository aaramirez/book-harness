---
id: CH-19
title: "AuditLedger y la Evidencia de Auditoría Estructuralmente Inmutable"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-017]
introduces_contracts: [C-029]
modifies_contracts: []
constitutional_articles: [P-13, P-25, INV-18, INV-19, INV-20, INV-E10]
previous_chapter: CH-18
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH19
    text: |
      Al terminar este capítulo podrás distinguir, para cualquier decisión crítica ya tomada por
      cualquier componente de este libro (una denegación de policy, un kill switch aplicado, una
      admisión rechazada...), qué tramo le pertenece al flujo general de telemetría operacional que
      un mecanismo de distribución desacoplado ya reparte hacia consumidores como logs o tracing, y
      qué tramo le pertenece, en cambio, a un registro de evidencia estructuralmente inmutable —
      nunca editado ni borrado una vez escrito — que además fija, para esa decisión concreta, el
      snapshot exacto de versiones de agente, skill, policy, configuración de modelo y contrato de
      capability vigentes en el instante en que ocurrió. Podrás diseñar, para ese registro, un
      contrato sin ningún campo de estado ni ninguna función de actualización o borrado, y
      argumentar por qué esa ausencia es, en sí misma, la garantía de inmutabilidad.
  skeleton:
    id: SK-CH19
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
    components_to_be_introduced: [CMP-017]
    contracts_to_be_introduced: [C-029]
  guiding_questions:
    - id: GQ-CH19-01
      text: |
        Un mecanismo ya existente en este libro distribuye, hacia quien se suscriba, cada hecho
        significativo que cualquier componente produce — incluido, nombrado explícitamente desde
        su propio capítulo, un consumidor dedicado a auditoría. Si ese mismo mecanismo ya puede
        filtrar exactamente los hechos que ese consumidor necesita, ¿basta esa distribución, por sí
        sola, para que exista evidencia de auditoría real — o falta algo que ningún filtro, por
        preciso que sea, puede proveer?
      answered_by: RQ-CH19-01
    - id: GQ-CH19-02
      text: |
        Cinco decisiones críticas de este libro (una denegación de autorización, una admisión
        rechazada, una credencial resuelta, una ejecución deduplicada, un kill switch aplicado) ya
        se documentan, cada una, como un hecho operacional distribuible. ¿Le pertenece a quien tomó
        cada una de esas decisiones registrar, además, evidencia de que ocurrió de forma que nunca
        pueda editarse ni borrarse después — o esa responsabilidad, honestamente, pertenece a otro
        dueño, distinto del que decide?
      answered_by: RQ-CH19-02
    - id: GQ-CH19-03
      text: |
        Si una decisión crítica se toma hoy contra una versión concreta del agente que la ejecuta,
        de la regla de policy que la evaluó, del modelo que razonó y del contrato de capability
        involucrado — y cualquiera de esas versiones cambia mañana — ¿qué necesitaría quedar
        fijado, en el instante exacto de la decisión, para que alguien pudiera reconstruir después,
        sin ambigüedad, contra qué versión exacta de cada una se decidió?
      answered_by: RQ-CH19-03
    - id: GQ-CH19-04
      text: |
        ¿Qué tendría que ser verdad sobre un registro para que, una vez escrito, nadie —ni siquiera
        el propio componente que lo escribió— pudiera después editarlo o borrarlo? ¿Basta con una
        convención documentada de "nunca lo hagas", o hace falta algo estructural en el propio
        contrato que lo haga, directamente, imposible de expresar?
      answered_by: RQ-CH19-04
  systems_lens:
    iceberg_visible_fact: |
      Diecinueve capítulos reales, y `P-25` ("Logs, traces, execution ledger and immutable audit
      evidence have different purposes and MUST NOT be conflated") fue citado, sin resolverse, seis
      veces seguidas: CH-09 lo reconoció como la razón de que "Audit" fuera uno de los nueve
      consumidores nombrados de `EventBus`, sin construir jamás su mecanismo; CH-14, CH-15, CH-16 y
      CH-17 lo citaron, cada uno, en la sección 14 de su propio capítulo, señalando la misma
      ausencia sobre su propio contrato (`AdmissionDecision`, `AgentCommunicationMessage`/
      `DelegationGrant`, `CredentialReference`, `IdempotencyRecord`); CH-18 lo citó por sexta vez
      sobre `ControlDirective` y nombró, en su propia sección 19, el "Observability & Governance
      Plane" como el candidato natural para, "por fin", resolver esa deuda (ver seccion 2, El
      Problema).
    iceberg_patterns: |
      El patrón que se repite, capítulo tras capítulo desde CH-09, es que un principio real y
      citado (`P-25`) puede sobrevivir seis capítulos completos —cada uno construyendo un contrato
      legítimo con su propia trazabilidad parcial (`requestId`, `traceId`,
      `delegatorRef`/`grantedAt`)— sin que ninguno construya jamás el mecanismo estructural que ese
      principio exige por nombre: evidencia distinta de la telemetría, y además inmutable (ver
      seccion 3, Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala `AuditLedger` (`CMP-017`), el sexto componente de este libro que no
      corresponde a ninguno de los once nombres de Article III — y el sexto plano de Amendment v1.1
      que este libro cubre (el octavo plano canónico, "Observability & Governance Plane") — con una
      ficha que declara tanto lo que posee (`owns`: producir y preservar evidencia estructuralmente
      inmutable, capturar el `VersionSnapshot` exacto que `INV-E10` exige) como lo que
      explícitamente NO posee (`does_not_own`: distribuir el flujo general de eventos operacionales
      — `EventBus`, CH-09, la frontera más importante de este capítulo) (ver seccion 8, Component
      Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es que "evidencia de auditoría" y "telemetría
      operacional" comparten, a veces, el mismo origen (una `PolicyDecision`, un `ControlDirective`)
      pero nunca la misma garantía: la telemetría puede filtrarse, reinterpretarse y distribuirse
      por volumen (`EventBus`); la evidencia debe preservarse exactamente como se escribió, para
      siempre — un contrato sin ningún campo de estado es, precisamente, la forma en la que este
      capítulo hace esa garantía imposible de violar por accidente (ver seccion 4, Impacto
      Constitucional).
    reinforcing_loop: |
      Cada vez que un principio constitucional real se cita seis veces sin resolverse, crece la
      tentación de tratarlo como "ya cubierto por `EventBus`" — hasta que alguna decisión crítica
      necesita, de verdad, sobrevivir a una disputa o a una investigación, y el único registro
      disponible resulta ser un evento entre miles, sin ninguna garantía de que no haya sido
      reinterpretado, perdido o nunca distribuido a nadie.
    balancing_loop: |
      `recordAuditEntry` (seccion 11) es el mecanismo de equilibrio: produce un `AuditRecord` sin
      ningún campo de estado y sin ninguna función de actualización o borrado — de modo que, una
      vez escrito, ningún camino del propio componente puede modificarlo, cerrando exactamente el
      bucle que CH-09..CH-18 dejaron abierto.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `AuditRecord` (`C-029`) no tenga ningún
      campo de estado ni ninguna función de actualización — a diferencia de `ControlDirective`
      (`ISSUED`/`APPLIED`) o `IdempotencyRecord` (`PENDING`/`COMPLETED`), ambos con un lifecycle
      real. Si `AuditRecord` hubiera heredado ese mismo patrón, habría abierto, por diseño, la
      posibilidad conceptual de una segunda escritura sobre el mismo registro — exactamente lo que
      `P-25` prohíbe. La ausencia total de un campo de estado es la forma en que `AuditLedger` hace
      la inmutabilidad estructural, no solo documentada.
  recall_questions:
    - id: RQ-CH19-01
      text: |
        ¿Qué componente produce evidencia de auditoría estructuralmente inmutable para una decisión
        crítica ya tomada, y en qué se diferencia, con precisión, del mecanismo que ya distribuye el
        flujo general de eventos operacionales del harness?
      # respuesta esperada: AuditLedger (CMP-017); frontera con EventBus (CMP-009, CH-09); P-25.
    - id: RQ-CH19-02
      text: |
        ¿Qué decide `AuditLedger`, y qué NO decide — en particular, respecto de la decisión crítica
        que audita?
    - id: RQ-CH19-03
      text: |
        ¿Qué campos tiene `AuditRecord` (`C-029`), y por qué no tiene ningún campo de
        estado/lifecycle, a diferencia de `ControlDirective` (CH-18) o `IdempotencyRecord` (CH-17)?
    - id: RQ-CH19-04
      text: |
        ¿Qué cinco versiones exige capturar `INV-E10` dentro de un `VersionSnapshot`, y por qué
        ninguna de ellas tenía, hasta este capítulo, un campo dedicado en ningún contrato anterior
        de este libro?
  explain_prompts:
    - id: EP-CH19-01
      text: |
        `AuditLedger` posee producir evidencia de auditoría para una `PolicyDecision` con
        `outcome = DENY` ya tomada por `PolicyEngine`. Explica, como si hablaras con alguien sin
        contexto técnico, por qué NO posee decidir si esa acción debía denegarse — ¿qué se
        confundiría, en la práctica, si la misma pieza de software decidiera Y auditara la misma
        decisión?
      target_entity: CMP-017
    - id: EP-CH19-02
      text: |
        `AuditRecord` nunca tiene un campo de estado, y `AuditLedger` nunca ofrece ninguna función
        para editarlo o borrarlo. Explica qué garantía real se perdería, y qué riesgo
        introduciríamos, si en cambio existiera una función que permitiera actualizar un
        `AuditRecord` ya escrito, aunque nadie, en la práctica, la usara todavía.
      target_entity: C-029
  interleaved_questions:
    - id: IQ-CH19-01
      text: |
        `EventBus` (CH-09) ya distribuye cada `AgentEvent` —incluido uno con
        `eventType = POLICY_EVALUATED` y `payload = PolicyDecision`— hacia cualquier
        `EventSubscription` que haga match, incluido un `subscriberRef` dedicado a auditoría
        (Article X, ya nombrado desde el propio capítulo de `EventBus`). Si ese consumidor de
        auditoría ya recibe, vía `EventBus`, exactamente la misma `PolicyDecision` que este
        capítulo audita, ¿qué le falta a esa distribución para servir, por sí sola, como la
        evidencia de auditoría que `P-25` exige — y qué construye este capítulo que `EventBus`,
        honestamente, nunca prometió dar?
      current_chapter_entities: [CMP-017, C-029]
      prior_chapter_entities: [CMP-009, C-019]
      prior_chapter: CH-09
    - id: IQ-CH19-02
      text: |
        `PolicyEngine.evaluatePolicyForToolCall` (CH-05) ya produce, con código real, una
        `PolicyDecision` con `outcome = DENY` cuando ninguna regla concede acceso — pero nunca
        decide, ni le corresponde decidir, si esa denegación necesita quedar preservada como
        evidencia inmutable más allá de la vida de ese `ToolCall`. Si este capítulo necesita
        auditar exactamente esa `PolicyDecision`, ¿le correspondería a
        `evaluatePolicyForToolCall` invocar, él mismo, el mecanismo de este capítulo — o existe,
        otra vez, una frontera de dueño distinto entre "decidir y devolver una `PolicyDecision`" y
        "preservar evidencia de que esa `PolicyDecision` ocurrió"?
      current_chapter_entities: [CMP-017, C-029]
      prior_chapter_entities: [CMP-005, C-014]
      prior_chapter: CH-05
  flashcards:
    - id: FC-CH19-01
      front: |
        ¿Qué posee `AuditLedger`?
      back: |
        Producir y preservar, de forma estructuralmente inmutable (append-only, nunca editada ni
        borrada una vez escrita), evidencia de auditoría (`AuditRecord`) para una decisión crítica
        ya tomada por otro componente — cita literal, `P-25`; capturar el `VersionSnapshot` exacto
        de agente/skill/policy/configuración de modelo/capability vigente en ese instante (cita
        literal, `INV-E10`); correlacionar cada `AuditRecord` con el actor y el contexto que
        `INV-19` exige; producir un `contentHash` verificable; y rechazar por defecto (fail-closed)
        un `AuditRecord` sin sujeto, sin actor, o con un `VersionSnapshot` incompleto.
      source_entity: CMP-017
      chapter_introduced_in: CH-19
      review_stage: DAY_1
    - id: FC-CH19-02
      front: |
        ¿Qué NO posee `AuditLedger`, y a qué componente pertenece la frontera más importante de
        este capítulo?
      back: |
        Distribuir el flujo general de eventos operacionales del harness hacia consumidores
        desacoplados (`EventBus`, `CMP-009`, CH-09 — frontera más importante: `EventBus` mueve un
        `AgentEvent` mutable, de alto volumen, para logs/tracing/debugging; `AuditLedger` produce
        un subconjunto específico, estructuralmente inmutable, de evidencia); tomar la decisión que
        audita (`PolicyEngine`/`OperationalController`/`AdmissionController`/etc., cada uno ya
        introducido — `AuditLedger` registra una decisión YA TOMADA, nunca la toma ni la modifica);
        autorizar el acceso de lectura al propio ledger (Preview); ni el mecanismo real de
        almacenamiento append-only/WORM (Preview, infraestructura de borde).
      source_entity: CMP-017
      chapter_introduced_in: CH-19
      review_stage: DAY_1
    - id: FC-CH19-03
      front: |
        ¿Qué campos tiene `AuditRecord` (`C-029`)?
      back: |
        `id` (`AuditRecordId`), `subjectRef` (`Text`, referencia opaca a la decisión original ya
        auditada — `PolicyDecision`/`ControlDirective`/`AdmissionDecision`/etc.), `versionSnapshot`
        (`VersionSnapshot`, embebido, el snapshot exacto que `INV-E10` exige), `actor` (`ActorId`,
        reusado de CH-06/CH-18, trazabilidad `INV-19`), `context` (`Optional<TraceId>`, cuando la
        decisión auditada tiene un `ExecutionContext` real), `recordedAt` (`Timestamp`) y
        `contentHash` (`Text`, garantía de integridad verificable).
      source_entity: C-029
      chapter_introduced_in: CH-19
      review_stage: DAY_1
    - id: FC-CH19-04
      front: |
        ¿Por qué `AuditRecord` es el primer contrato de este libro sin ningún campo de
        estado/lifecycle, y sin ninguna función de actualización o borrado?
      back: |
        Porque introducir un campo de estado (como `ControlDirectiveStatus` o
        `IdempotencyRecordStatus`) implicaría, por diseño, que un `AuditRecord` puede transicionar
        — abriendo la posibilidad conceptual de una segunda escritura sobre el mismo registro,
        exactamente lo que `P-25` ("audit evidence... MUST NOT be conflated" con telemetría
        mutable) prohíbe. La ausencia total de un campo de estado, y la ausencia total de cualquier
        función `updateAuditRecord`/`deleteAuditRecord`, es la forma en que este capítulo hace la
        inmutabilidad estructural — imposible de violar por accidente, no solo documentada como una
        convención.
      source_entity: C-029
      chapter_introduced_in: CH-19
      review_stage: DAY_1
    - id: FC-CH19-05
      front: |
        `VersionSnapshot` embebe cinco campos de versión. ¿Por qué ninguno de esos cinco tenía,
        hasta este capítulo, un campo dedicado en `AgentConfig`, `PolicyDecision` o `ModelRequest`?
      back: |
        Porque ningún capítulo anterior necesitó nunca fijar, de forma durable, la versión exacta
        de un agente, una policy o una configuración de modelo — `AgentConfig` (CH-00) nunca
        declaró un campo `version`, `PolicyDecision` (CH-05) correlaciona con `policyRuleId` pero
        no con una versión de esa regla, y `ModelRequest`/`ModelResponse` (CH-03) nunca declararon
        una versión de configuración. Solo `CapabilityDescriptor.version` (`C-018`, CH-08, `P-26`)
        ya existía. `VersionSnapshot` (embebido en `AuditRecord`, sin contrato `C-XXX` propio)
        captura las cinco como valores ya resueltos y provistos por quien invoca
        `recordAuditEntry` — sin retroceder a modificar ningún contrato de un capítulo anterior
        (fuera del alcance de este capítulo, ver seccion 18).
      source_entity: C-029
      chapter_introduced_in: CH-19
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH19-01
      recall_question: RQ-CH19-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH19-02
      recall_question: RQ-CH19-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH19-03
      recall_question: RQ-CH19-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH19-04
      recall_question: RQ-CH19-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 19 — AuditLedger y la Evidencia de Auditoría Estructuralmente Inmutable

> **Regla constitucional (Amendment v1.1, `P-25`):** "Logs, traces, execution ledger and immutable
> audit evidence have different purposes and MUST NOT be conflated."
>
> **Regla constitucional (Amendment v1.1, `INV-E10`):** "Every production run records exact
> versions of agent, skill, policy, model configuration and capability contracts."

CH-14, CH-15, CH-16, CH-17 y CH-18 abrieron cinco de los nueve planos canónicos de Amendment v1.1 —
Ingress & Activation (`AdmissionController`), Agent Interoperability (`AgentCommunicationGateway`),
Capability & Integration (`CredentialBroker`), Reliability (`IdempotencyGuard`) y Control
(`OperationalController`). Este capítulo entra al **sexto plano que este libro cubre** — el
**Observability & Governance Plane**, que en la enumeración de la enmienda ocupa la **octava**
posición (Ingress & Activation → Execution → Agent Interoperability → Capability & Integration →
Data & Context → Control → Reliability → **Observability & Governance** → Execution Fabric) — el
mismo patrón de salto que ya usaron `IdempotencyGuard` (CH-17, Reliability, séptimo canónico) y
`OperationalController` (CH-18, Control, sexto canónico): este libro no cubre los nueve planos en su
orden canónico, sino en el orden en que cada uno adquiere una razón de peso para escribirse.

La razón de peso, aquí, no es nueva — es la más repetida de todo Amendment v1.1. `P-25` ("Audit
evidence is distinct from operational telemetry") fue citado por primera vez en CH-09, el capítulo
que instaló `EventBus`, reconociendo desde entonces que "Audit" es uno de los nueve consumidores que
Article X nombra explícitamente — y, sin excepción, cada uno de los cinco capítulos de Amendment
v1.1 que le siguieron (CH-14, CH-15, CH-16, CH-17, CH-18) volvió a citar `P-25` en su propia sección
14, señalando, honestamente, que su propio contrato (`AdmissionDecision`, `AgentCommunicationMessage`/
`DelegationGrant`, `CredentialReference`, `IdempotencyRecord`, `ControlDirective`) todavía carecía de
un mecanismo de evidencia inmutable, distinto de `AgentEvent`/`EventBus` — y que ese mecanismo "no se
construye aquí". CH-18 §19 llegó a nombrar, explícitamente, el "Observability & Governance Plane"
como el candidato que "por fin resolvería la deuda de `P-25`". Este capítulo, el vigésimo capítulo
real de contenido de este libro, es el primero en resolverla con código real.

Ningún texto de la Constitution nombra literalmente un componente para esto — igual que
`IdempotencyGuard` (CH-17) y `OperationalController` (CH-18), el nombre que este capítulo adopta,
`AuditLedger`, es una **síntesis de este libro**, evaluada explícitamente contra alternativas
(`AuditTrail`, descartado porque "trail" sugiere un flujo apendible sin comprometerse con
inmutabilidad estructural — el mismo riesgo de ambigüedad que ya distingue a un `AgentEvent`
distribuido de la evidencia que este capítulo exige; `ComplianceRecorder`, descartado porque implica
juzgar cumplimiento normativo, una decisión que este componente nunca toma; `EvidenceStore`,
descartado porque subestima que este componente *produce* activamente cada registro —incluyendo su
`contentHash`— y no solo lo almacena pasivamente) y elegida porque "Ledger" transporta, con precisión
deliberada, la metáfora financiera de un libro de cuentas: secuencial, append-only, cada entrada
verificable y ninguna jamás corregida por sobrescritura — exactamente el modelo que `P-25` exige (ver
seccion 8).

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de saber
> cómo se llama el componente de este capítulo. El detalle estructurado de esta sección vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, para cualquier decisión
crítica ya tomada por cualquier componente de este libro, qué tramo le pertenece al flujo general de
telemetría operacional que un mecanismo de distribución desacoplado ya reparte hacia consumidores
como logs o tracing, y qué tramo le pertenece, en cambio, a un registro de evidencia estructuralmente
inmutable — nunca editado ni borrado una vez escrito — que además fija, para esa decisión concreta,
el snapshot exacto de versiones de agente, skill, policy, configuración de modelo y contrato de
capability vigentes en el instante en que ocurrió. Podrás diseñar, para ese registro, un contrato sin
ningún campo de estado ni ninguna función de actualización o borrado, y argumentar por qué esa
ausencia es, en sí misma, la garantía de inmutabilidad.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e introduce
un contrato de datos nuevo y el sexto componente de este libro que pertenece a Amendment v1.1 en vez
de a los once nombres originales de Article III.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar atrás;
están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este capítulo va
a definir):

1. Un mecanismo ya existente en este libro distribuye, hacia quien se suscriba, cada hecho
   significativo que cualquier componente produce — incluido un consumidor dedicado a auditoría. Si
   ese mismo mecanismo ya puede filtrar exactamente los hechos que ese consumidor necesita, ¿basta
   esa distribución, por sí sola, para que exista evidencia de auditoría real — o falta algo que
   ningún filtro, por preciso que sea, puede proveer?
2. Cinco decisiones críticas de este libro ya se documentan, cada una, como un hecho operacional
   distribuible. ¿Le pertenece a quien tomó cada una de esas decisiones registrar, además, evidencia
   de que ocurrió de forma que nunca pueda editarse ni borrarse después — o esa responsabilidad,
   honestamente, pertenece a otro dueño, distinto del que decide?
3. Si una decisión crítica se toma hoy contra una versión concreta del agente, de la regla de
   policy, del modelo y del contrato de capability involucrados — y cualquiera de esas versiones
   cambia mañana — ¿qué necesitaría quedar fijado, en el instante exacto de la decisión, para que
   alguien pudiera reconstruir después, sin ambigüedad, contra qué versión exacta de cada una se
   decidió?
4. ¿Qué tendría que ser verdad sobre un registro para que, una vez escrito, nadie —ni siquiera el
   propio componente que lo escribió— pudiera después editarlo o borrarlo? ¿Basta con una convención
   documentada de "nunca lo hagas", o hace falta algo estructural en el propio contrato que lo haga,
   directamente, imposible de expresar?

## 1. Arquitectura Actual (Current Architecture)

CH-00..CH-18 dejaron instalados veintiocho contratos de datos y dieciséis componentes: los once
nombres completos de Article III ("Agent Runtime"), dos capítulos de integración, y cinco componentes
de Amendment v1.1 (`AdmissionController`, CMP-012, CH-14; `AgentCommunicationGateway`, CMP-013,
CH-15; `CredentialBroker`, CMP-014, CH-16; `IdempotencyGuard`, CMP-015, CH-17;
`OperationalController`, CMP-016, CH-18).

`EventBus` (CMP-009, CH-09) es, de los dieciséis, el único cuya responsabilidad completa es hacer
llegar un `AgentEvent` (C-010) ya producido hacia quien lo necesite. `distributeEvent` (CH-09 §11)
entrega, sin modificarlo, cada `AgentEvent` hacia toda `EventSubscription` (C-019) activa cuyo
`EventFilter` haga match — y CH-09 §4 ya reconoció explícitamente, citando `P-25`, que "la distinción
entre lo que es evidencia de auditoría y lo que es telemetría operacional la conserva cada consumidor
mediante su propio filtro, nunca `EventBus` por decisión propia". Article X nombra, desde la primera
versión de la Constitution que este repositorio adoptó, nueve consumidores que "esta fuente de
eventos debe poder alimentar": `Logs`, `Tracing`, `Audit`, `Replay`, `Analytics`, `Evals`, `Cost
Analysis`, `Debugging`, `UI` — y "Audit" ha estado, desde CH-09, en esa lista.

Pero ningún capítulo, hasta este, construyó jamás lo que ese consumidor de auditoría necesitaría
recibir para ser, de verdad, evidencia de auditoría. Cinco capítulos de Amendment v1.1 lo señalaron,
cada uno sobre su propio contrato, sin resolverlo:

- CH-14 §14: "Una evidencia de auditoría real de cada `AdmissionDecision` (quién la evaluó, con qué
  reglas, en qué momento) necesitaría, per `P-25`, un mecanismo **distinto** de `EventBus` — uno que
  este capítulo no construye." Solo dejó disponible la correlación mínima de
  `AdmissionDecision.requestId`.
- CH-15 §14: la misma conclusión para `AgentCommunicationMessage`/`DelegationGrant`, dejando
  disponible solo `AgentCommunicationMessage.traceId` y `DelegationGrant.delegatorRef`/`grantedAt`.
- CH-16 §14: la misma conclusión para `CredentialReference`, dejando disponible solo la telemetría
  operacional que `CredentialBroker` sí produce.
- CH-17 §14: la misma conclusión para `IdempotencyRecord`.
- CH-18 §14: la misma conclusión para `ControlDirective` — y CH-18 §19 nombró, explícitamente, el
  "Observability & Governance Plane" como el plano que "por fin resolvería la deuda de `P-25`,
  señalada sin resolver desde CH-09 y repetida en cada capítulo de Amendment v1.1 desde entonces".

`CapabilityDescriptor.version` (C-018, CH-08, `P-26`) es, hasta este capítulo, el único campo de todo
este libro que fija una versión explícita de algo. Ningún contrato declara jamás una versión de
agente (`AgentConfig`, C-002, CH-00, no tiene campo `version`), de policy (`PolicyDecision.
policyRuleId`, C-014, CH-05, identifica qué regla decidió, no qué versión de esa regla) ni de
configuración de modelo (`ModelRequest`/`ModelResponse`, C-006/C-007, CH-03, no tienen campo de
versión). `INV-E10` ("Every production run records exact versions of agent, skill, policy, model
configuration and capability contracts") ya exige, desde Amendment v1.1, las cinco — pero ningún
capítulo, hasta este, había citado ese invariante en prosa ni resuelto con código real ninguna de las
cinco.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas para esto, "evidencia de auditoría" tiende a colapsarse,
silenciosamente, en "lo que `EventBus` ya distribuye hacia quien se suscriba con el filtro correcto".
Y esa suposición es, precisamente, la conflación que `P-25` prohíbe por nombre. Un `AgentEvent` que
`EventBus` distribuye hoy hacia un `subscriberRef` de auditoría es, en todo sentido estructural,
idéntico a cualquier otro `AgentEvent` que ese mismo `EventBus` distribuye hacia `Logs` o `Debugging`:
mismo `STRUCT` (C-010), mismas garantías (ninguna de preservación durable, ninguna de inmutabilidad,
ninguna de integridad verificable), mismo mecanismo de entrega (`deliver`, una primitiva asumida sin
garantías de orden ni de reintento). Nada distingue, estructuralmente, "esto es telemetría operacional
de alto volumen que puede perderse o reinterpretarse sin consecuencia" de "esto es evidencia que
necesita sobrevivir, exactamente como se escribió, a una disputa o una investigación futura" — la
distinción vive, hoy, únicamente en la cabeza de quien decide, informalmente, tratar un
`subscriberRef` como "el de auditoría".

Hay una segunda dimensión del problema. `INV-E10` exige que "todo run de producción registre las
versiones exactas de agente, skill, policy, configuración de modelo y contrato de capability" — pero
ningún contrato de este libro, hasta este capítulo, tiene dónde guardar esas cinco versiones juntas,
en el instante exacto de una decisión crítica. Si el agente que ejecutó una acción se actualiza mañana,
si la regla de policy que la autorizó cambia de versión, o si el modelo detrás de `ModelGateway`
(CH-03) se reemplaza — nada en este libro, hasta ahora, permite reconstruir, sin ambigüedad, contra
qué versión exacta de cada uno se tomó una decisión ya pasada.

Hay una tercera dimensión, la más delicada: incluso si alguien construyera, hoy, un contrato con los
campos correctos, nada le impediría —por conveniencia, por un parche apurado, por una migración de
esquema— agregarle después una función que lo actualice o lo borre. Un registro de auditoría que
*puede*, aunque sea en teoría, ser editado después de escrito no es evidencia de auditoría: es,
simplemente, otro dato mutable más, indistinguible en la práctica de la telemetría operacional que
`P-25` exige mantener separada.

Necesitamos que "preservar evidencia inmutable de una decisión crítica ya tomada" tenga, por fin, un
dueño único y nombrado — que capture una referencia opaca a esa decisión (sin importar de qué
contrato provenga), que fije el snapshot exacto de versiones que `INV-E10` exige, que correlacione
esa evidencia con el actor y el contexto que `INV-19` ya exige para toda decisión crítica, y que haga
la inmutabilidad una propiedad **estructural** del propio contrato — no una promesa documentada que
cualquier función futura podría romper.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los veintiocho contratos y los dieciséis componentes que existen hasta este punto no bastan porque:

- `P-25` fue citado seis veces (CH-09, CH-14, CH-15, CH-16, CH-17, CH-18) — verificado con grep
  directo contra los archivos de capítulo, sin asumir el conteo de memoria — y ninguna de las seis
  veces produjo jamás el mecanismo de evidencia inmutable que el propio texto exige; `EventBus`
  (CH-09) declaró explícitamente, en su propio `does_not_own`, que interpretar o distinguir "esto es
  auditoría" de "esto es telemetría" no le pertenece;
- ningún contrato de este libro modela, todavía, un registro cuya inmutabilidad sea estructural en
  vez de documental — `ControlDirective` (C-028, CH-18) e `IdempotencyRecord` (C-027, CH-17) son
  write-once por convención de sus propias funciones (`applyControlDirective`,
  `recordIdempotentExecution` rechazan reaplicar), pero ambos SÍ tienen un campo de estado y, con él,
  la posibilidad conceptual de que una versión futura de esas funciones lo reutilizara para una
  segunda escritura; ninguno de los dos fue diseñado para ser, además, la evidencia final de que algo
  ocurrió;
- `INV-E10` exige, en una sola frase, capturar cinco versiones exactas — y ningún contrato de este
  libro, verificado con grep sobre `registry/contracts.yaml`, declara un campo `version` salvo
  `CapabilityDescriptor` (C-018, CH-08, para la quinta de las cinco); `AgentConfig` (C-002),
  `PolicyDecision` (C-014) y `ModelRequest`/`ModelResponse` (C-006/C-007) no declaran ninguno para
  las otras cuatro;
- nada impide, hoy, que una decisión crítica (una `PolicyDecision` con `outcome = DENY`, un
  `ControlDirective` `APPLIED`) quede correlacionada únicamente por los campos de correlación
  mínimos que su propio capítulo ya provee (`callId`, `requestId`, `traceId`) — suficientes para
  reconstruir "qué decisión fue", nunca suficientes para un registro autónomo, íntegro y verificable
  de "esto ocurrió, y no ha sido alterado desde entonces";
- ningún componente de este libro declara, todavía, `owns` una responsabilidad que sea, literalmente,
  "preservar evidencia" en vez de "tomar una decisión", "ejecutar un side effect" o "distribuir un
  hecho ya ocurrido" — las tres categorías que Article III y CH-09 ya cubrieron, dejando a `P-25` sin
  un cuarto dueño hasta este capítulo.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la secuencia
> `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una entidad que no
> haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT` registrado — **no
> magic entities**. Este capítulo aplica la misma disciplina que CH-00..CH-18 ya establecieron, con
> una particularidad que ningún capítulo anterior enfrentó: es el primero cuyo contrato nuevo no
> declara ningún `ENUM` de estado propio — ni `ControlDirectiveStatus` (CH-18) ni
> `IdempotencyRecordStatus` (CH-17) tienen equivalente aquí. La ausencia es deliberada, no un olvido:
> introducir un `ENUM AuditRecordStatus` habría sugerido, por la sola existencia del campo, que un
> `AuditRecord` puede transicionar — precisamente lo que `P-25` prohíbe (ver seccion 12 para el
> desarrollo completo).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-13   Authorization is deterministic and external to the LLM.
           El mismo argumento que ya protegió la autorización desde CH-01/CH-05, la credencial
           desde CH-16, la deduplicación desde CH-17 y el control operacional desde CH-18, se
           extiende aquí a la evidencia de auditoría: el modelo nunca decide, nunca ve y nunca
           constituye una fuente de verdad sobre qué se audita ni sobre el contenido de un
           AuditRecord — recordAuditEntry (seccion 11) es completamente determinístico y externo
           al LLM.
    P-25   Audit evidence is distinct from operational telemetry.
           Primera materialización real, con código, de este principio en todo el libro —
           AuditRecord (seccion 6/7) y AuditLedger (seccion 8) formalizan, por fin, la distinción
           que EventBus (CH-09) ya reconoció en prosa pero nunca construyó: un registro
           estructuralmente inmutable, distinto del AgentEvent mutable que EventBus distribuye.

Invariants preserved
    INV-18    Toda acción significativa produce un evento observable.
              recordAuditEntry (seccion 11) emite un AgentEvent (AUDIT_RECORD_CREATED) cuando
              existe un ExecutionContext y un AgentId reales para la decisión auditada — pero, con
              la misma disciplina que CH-18 aplicó a DISABLE_CAPABILITY/ISOLATE_TENANT/ROLLBACK,
              nunca fabrica esos campos cuando no existen (ver seccion 14 para el desarrollo
              completo, incluyendo por qué ese evento NUNCA es, él mismo, la evidencia de
              auditoría).
    INV-19    Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy
              relevante.
              AuditRecord.actor (ActorId, reusado de CH-06/CH-18) y AuditRecord.context
              (Optional<TraceId>) son la materialización, con más fuerza que en cualquier capítulo
              anterior, de este invariante — porque, a diferencia de ControlDirective (CH-18), que
              nunca almacena contexto en su propio STRUCT, AuditRecord SÍ lo preserva como parte
              permanente de la evidencia.
    INV-20    Todo error operacional pertenece a una categoría conocida.
              Los tres fallos reales de este capítulo (seccion 13) introducen AUDIT, una categoría
              nueva de ErrorCategory — deliberadamente NO reutiliza CONTROL (CH-18) ni ninguna de
              las diecisiete categorías ya existentes, por la misma razón de fondo que motiva todo
              este capítulo: conflacionar el fallo de auditar con el fallo de cualquier otro
              dominio sería, en espíritu, la misma conflación que P-25 prohíbe a nivel de
              propósito, ahora aplicada a nivel de ErrorCategory.
    INV-E10   Every production run records exact versions of agent, skill, policy, model
              configuration and capability contracts.
              Cita literal y definitoria de este capítulo — la primera vez que este libro escribe
              un STRUCT (VersionSnapshot, seccion 6) que declara, juntas, las cinco versiones
              exactas que este invariante exige por nombre.

Component ownership changes
    CMP-017 AuditLedger se introduce — registry/components.yaml pasa de 16 a 17 componentes. Es el
    sexto componente de este registry que NO corresponde a ninguno de los once nombres del árbol
    de Article III ("Agent Runtime") — pertenece, en cambio, al "Observability & Governance Plane"
    de Amendment v1.1 (el octavo plano canónico, sexto que este libro cubre — ver apertura del
    capítulo). Es, además, el segundo componente de todo este libro sin fila propia en la tabla de
    Decision Ownership de Article IV — junto a EventBus (CMP-009, CH-09): registrar evidencia de
    una decisión ya tomada no es, en sí mismo, tomar una decisión nueva (ver seccion 8).
    registry/components.yaml de CMP-005 (PolicyEngine), CMP-009 (EventBus), CMP-012..CMP-016 NO se
    modifica: ninguno cablea todavía su relación real con AuditLedger (ver seccion 9/18).

Lifecycle changes
    Ninguna modificación al ENUM AgentRunStatus (C-013): sigue siendo, sin cambios desde CH-01, el
    mismo conjunto de once valores. AuditRecord (C-029) es el primer contrato nuevo de este libro
    que no introduce ningún ENUM de estado propio — ni ControlDirectiveStatus (CH-18) ni
    IdempotencyRecordStatus (CH-17) tienen equivalente aquí (ver seccion 3/12 para el porqué
    explícito).

Security implications
    AuditLedger es el primer componente de este libro cuya responsabilidad completa es preservar,
    nunca decidir ni distribuir. Ver seccion 15 para el análisis completo, incluyendo la frontera
    más importante de este capítulo, contra EventBus.

Observability implications
    A diferencia de IdempotencyGuard/CapabilityRegistry/CredentialBroker (que siempre emiten) y de
    AdmissionController/AgentCommunicationGateway (que nunca emiten), AuditLedger emite
    condicionalmente — igual que OperationalController (CH-18) — pero con una particularidad
    nueva: el AgentEvent que emite NUNCA es, él mismo, la evidencia de auditoría; es, apenas, una
    notificación —tan mutable y tan distribuible como cualquier otra— de que esa evidencia ya fue
    escrita (ver seccion 14).

Deterministic vs agentic boundary
    Article XII se refina una decimoséptima vez a nivel de componente: AuditLedger, igual que
    EventBus (CH-09) y OperationalController (CH-18), no recibe ninguna entrada que el modelo haya
    producido — ni siquiera de forma indirecta. Evalúa exclusivamente una referencia opaca a una
    decisión ya tomada, un VersionSnapshot ya resuelto y un actor ya identificado — todos ajenos a
    cualquier razonamiento del modelo.
```

## 5. Conceptos Nuevos (New Concepts)

- **Immutable Audit Evidence** *(cita literal, `P-25`, "audit evidence... MUST NOT be conflated"
  con telemetría operacional)*: un registro que, una vez escrito, nunca se edita ni se borra —
  distinto de un `AgentEvent` distribuido por `EventBus` (mutable en el sentido de que puede
  perderse, reinterpretarse o simplemente nunca haber sido distribuido a nadie interesado). Modelado
  como `AuditRecord` (C-029, seccion 6/7).
- **Version Pinning** *(lectura de `INV-E10`)*: fijar, en el instante exacto de una decisión crítica,
  las versiones exactas de agente, skill, policy, configuración de modelo y contrato de capability
  que esa decisión involucró — de modo que, si cualquiera de esas cinco versiones cambia después,
  alguien pueda reconstruir, sin ambigüedad, contra qué versión exacta se decidió. Modelado como
  `VersionSnapshot` (seccion 6), embebido dentro de `AuditRecord` sin contrato `C-XXX` propio.
- **Subject Reference (Opaque)**: la referencia opaca al contrato de decisión original que un
  `AuditRecord` audita — nunca un campo distinto por cada tipo posible de decisión
  (`PolicyDecision`/`ControlDirective`/`AdmissionDecision`/etc.), sino un único `Text` genérico, cuyo
  significado exacto depende de qué componente lo produjo — mismo tratamiento que
  `ControlDirective.targetRef` (CH-18) o `ActivationRequest.sourceRef` (CH-14).
- **Structural Immutability (por ausencia)**: la propiedad de que un contrato sea inmutable no porque
  una función lo declare así en prosa, sino porque su propio `STRUCT` no tiene ningún campo de estado
  y su componente no ofrece ninguna función de actualización o borrado — la inmutabilidad se
  garantiza por lo que el contrato y el componente **no pueden expresar**, no por una convención que
  una función futura podría romper.
- **Content Integrity (Hash)**: la garantía, embebida en cada `AuditRecord` (`contentHash: Text`), de
  que su contenido puede verificarse contra alteración posterior — este capítulo modela el campo y su
  cómputo determinístico, dejando el algoritmo criptográfico real y el mecanismo de verificación como
  Preview (ver seccion 18).
- **Decision Ownership por ausencia, por segunda vez** *(Article IV, aplicado por primera vez a
  `EventBus`, CH-09, aplicado aquí por segunda vez)*: `AuditLedger` es el segundo componente real de
  este libro que Article IV no enumera en su tabla — porque, igual que distribuir no es decidir,
  **registrar tampoco es decidir**. `AuditLedger` nunca responde una pregunta de la forma "¿qué
  debería ocurrir?"; solo preserva, sin interpretarla, una respuesta que otro componente ya dio.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `Text`, `Timestamp`, `Boolean`, `Optional`,
`ExecutionContext` (C-004, CH-00), `AgentEvent` (C-010, CH-00), `HarnessError` (C-011, CH-00),
`PolicyDecision` (C-014, CH-05).

Este capítulo también reusa, sin redefinirlo, un identificador opaco introducido por un capítulo
anterior — mismo patrón de reuso explícito que CH-13 §6 y CH-18 §6 ya aplicaron:

| Identificador (reusado, no nuevo) | Introducido en | Uso en este capítulo |
|---|---|---|
| `ActorId` | CH-06 §6 | tipo del campo `AuditRecord.actor` — el mismo identificador opaco que ya usan `HumanInteractionResolution.resolvedBy` (C-016, CH-06) y `ControlDirective.issuedBy` (C-028, CH-18) |

### Un identificador opaco nuevo

Siguiendo el mismo patrón que CH-00 §6 estableció para los identificadores fundamentales, y que
CH-14/CH-15/CH-16/CH-17/CH-18 repitieron para los suyos:

| Identificador (nuevo de este capítulo) | Identifica |
|---|---|
| `AuditRecordId` | un `AuditRecord` concreto — el registro de evidencia inmutable producido para una decisión crítica ya auditada |

### `ErrorCategory` — extendido, sin redefinir `HarnessError`

Este es el octavo capítulo que agrega un valor a `ErrorCategory` desde que CH-00 lo declaró (después
de `HUMAN_INTERACTION`, CH-06; `ADMISSION`, CH-14; `DELEGATION`, CH-15; `CREDENTIAL`, CH-16;
`IDEMPOTENCY`, CH-17; y `CONTROL`, CH-18): el valor `AUDIT`, necesario porque ninguna de las
dieciséis categorías ya existentes representa, sin conflación, un fallo específico de la integridad
o completitud de la evidencia de auditoría — reutilizar `CONTROL` (CH-18) o `VALIDATION` (CH-00)
habría sido, precisamente, el tipo de conflación que `P-25` prohíbe a nivel de propósito, ahora
aplicada a nivel de `ErrorCategory`:

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
END
```

`HarnessError` (C-011) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — mismo patrón
exacto que las extensiones de CH-06/CH-14/CH-15/CH-16/CH-17/CH-18, aplicado aquí por séptima vez a
`ErrorCategory`.

### `AgentEventType` — extendido, sin redefinir `AgentEvent`

CH-18 dejó `AgentEventType` en veintisiete valores. Este capítulo agrega un único valor nuevo — mismo
patrón que CH-05/CH-07/CH-18 (una sola operación real, no un par éxito/fallo — seccion 14 explica la
razón completa):

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
END
```

`AgentEvent` (C-010) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — solo el rango de
valores permitido para `eventType` crece, igual que en cada capítulo anterior salvo `EventBus`
(CH-09), `AdmissionController` (CH-14) y `AgentCommunicationGateway` (CH-15).

### `VersionSnapshot` — el snapshot exacto que `INV-E10` exige (sin `C-XXX` propio)

```pseudocode
STRUCT VersionSnapshot
    agentVersion: Text
    skillVersion: Optional<Text>
    policyVersion: Text
    modelConfigVersion: Text
    capabilityVersion: Optional<Text>
END
```

Cinco campos, uno por cada sustantivo que `INV-E10` enumera literalmente ("agent, skill, policy,
model configuration and capability contracts"). `agentVersion`, `policyVersion` y
`modelConfigVersion` son obligatorios: toda decisión crítica de este libro involucra, siempre, algún
agente ejecutándose, alguna policy evaluada (aunque sea la ausencia de una regla que aplique,
`PolicyEngine`, CH-05) y alguna configuración de modelo vigente. `skillVersion` y
`capabilityVersion` son `Optional<Text>`: este libro nunca modeló, hasta este capítulo, un concepto
de "skill" como entidad propia (ni siquiera `AgentConfig`, C-002, CH-00, lo declara), y no toda
decisión crítica involucra necesariamente una capability concreta (una `AdmissionDecision`, CH-14,
puede rechazar una activación antes de que exista ningún `ToolCall`). Los cinco campos son `Text`
opacos, no una referencia tipada a un contrato existente — evaluado explícitamente contra reusar
`CapabilityDescriptor.version` (C-018, CH-08) directamente para `capabilityVersion`: se descartó
porque `VersionSnapshot` necesita las cinco versiones con la misma forma, y forzar cuatro de los
cinco campos a inventar un tipo propio (`AgentVersion`, `PolicyVersion`, `ModelConfigVersion`) para
solo poder compartir la forma de uno habría introducido más tipos nuevos de los que este capítulo
necesita para demostrar el mecanismo.

**Por qué `VersionSnapshot` no tiene contrato `C-XXX` propio.** Mismo patrón que `ExecutionUsage`
(CH-07), `ContextBlock` (CH-04), `EventFilter` (CH-09) o `ControlDirectiveApplication` (CH-18): un
tipo real, con forma explícita, pero embebido dentro de `AuditRecord` (seccion siguiente) sin
necesitar un identificador de Contract Registry independiente porque nunca se referencia fuera de la
estructura que lo contiene.

### `AuditRecord` — el registro de evidencia estructuralmente inmutable

```pseudocode
STRUCT AuditRecord
    id: AuditRecordId
    subjectRef: Text
    versionSnapshot: VersionSnapshot
    actor: ActorId
    context: Optional<TraceId>
    recordedAt: Timestamp
    contentHash: Text
END
```

Siete campos, cada uno respondiendo a una parte exacta del alcance decidido para este capítulo: `id`
identifica este registro de forma estable; `subjectRef` es una referencia opaca (`Text`) a la
decisión original ya auditada — un `PolicyDecision.callId` cuando se audita una denegación de policy,
un `ControlDirective.id` cuando se audita un kill switch, un `AdmissionDecision.requestId` cuando se
audita un rechazo de admisión — **nunca embebiendo la decisión completa**, el mismo argumento que ya
usó `ControlDirective.targetRef` (CH-18) para no cargar una copia de un objeto ajeno; `versionSnapshot`
es el `VersionSnapshot` de la sección anterior; `actor` es `ActorId` (reusado de CH-06/CH-18) —
trazabilidad literal de `INV-19`; `context` es `Optional<TraceId>`, poblado únicamente cuando la
decisión auditada ocurrió dentro de un `ExecutionContext` real; `recordedAt` registra cuándo se
escribió este registro; `contentHash` es la garantía de integridad verificable (seccion 5).

**Por qué un único `subjectRef: Text` opaco, y no un campo por cada tipo de decisión posible.** Se
evaluó explícitamente modelar campos `Optional` separados
(`policyDecisionRef`/`controlDirectiveRef`/`admissionDecisionRef`/...), uno por cada contrato de
decisión ya existente en este libro. Se descartó por la misma razón, ya establecida, que motivó
`ControlDirective.targetRef` (CH-18) e `IdempotencyRecord.capability` (CH-17): un `AuditRecord`
dado tendría, siempre, todos esos campos `NULL` salvo uno — y, peor aún, cada nuevo tipo de decisión
que un capítulo futuro introdujera (y este libro ya tiene, hoy, al menos cinco tipos de decisión
crítica auditable) obligaría a reabrir el `STRUCT AuditRecord` para agregar un campo más. `subjectRef`
opaco, con su significado determinado por quién invoca `recordAuditEntry` (seccion 11), es genérico
por diseño — el propio punto de este capítulo es que `AuditLedger` nunca necesita saber, para hacer su
trabajo, de qué tipo de decisión se trata.

**Por qué `AuditRecord` no embebe una copia completa de la decisión auditada.** Se evaluó también
tipar `subjectRef` como `Value` (el mismo primitivo genérico que `AgentEvent.payload` ya usa) para
embeber la decisión completa, en vez de una referencia opaca. Se descartó: `AuditRecord` audita el
*hecho* de que una decisión ocurrió, con qué versiones y bajo qué actor — no reemplaza al contrato
original que la representa (`PolicyDecision`, `ControlDirective`, etc.), que sigue siendo, en cada
caso, la fuente de verdad completa de sus propios campos. Embeber una copia completa habría hecho de
`AuditRecord` una segunda representación mutable-por-desincronización de algo que ya tiene un dueño —
exactamente el tipo de duplicación que Article IV (Ownership Rule) desalienta.

**Por qué `AuditRecord` no tiene ningún campo de estado.** A diferencia de `ControlDirective`
(`status: ControlDirectiveStatus`, CH-18) o `IdempotencyRecord` (`status: IdempotencyRecordStatus`,
CH-17), `AuditRecord` no declara ningún `ENUM` de lifecycle. Se evaluó explícitamente introducir un
`ENUM AuditRecordStatus` (p. ej. `RECORDED`/`VERIFIED`) y se descartó: cualquier campo de estado, por
diseño, sugiere que un `AuditRecord` puede transicionar entre valores — abriendo la posibilidad
conceptual de una segunda escritura sobre el mismo registro. `P-25` exige, literalmente, que la
evidencia de auditoría nunca se conflacione con algo mutable; un contrato sin ningún campo que pueda
cambiar de valor después de creado es la forma más directa de cumplir esa exigencia con la propia
forma del `STRUCT`, no solo con la disciplina de las funciones que lo producen (ver seccion 12 para
el desarrollo completo).

**Unchanged / Not yet introduced**: `AgentEvent` (C-010) no cambia de forma. Ningún `STRUCT` para
representar un "actor de auditoría" distinto de `ActorId`, ningún mecanismo real de almacenamiento
append-only/WORM, y ningún algoritmo criptográfico concreto detrás de `contentHash` (ver seccion 18).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce un contrato de
datos, registrado en `registry/contracts.yaml`:

```text
ID:                     C-029
Name:                   AuditRecord
Version:                v1
Introduced In:          CH-19
Current Definition:     STRUCT AuditRecord (ver §6)
Used By:                [CMP-017]
Modified By:            []
Constitutional Impact:  [P-25, INV-19, INV-E10]
```

`C-029` es el decimosexto id que este libro asigna sin que estuviera reservado desde CH-01 §7 — el
correlativo simplemente continúa después de `C-028` (CH-18). No colisiona, por nombre, con ningún
contrato ya registrado — verificado con grep completo sobre `registry/contracts.yaml` antes de
escribir este capítulo.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el sexto componente del registry que no corresponde a ninguno de los once
nombres del árbol de Article III ("Agent Runtime") — pertenece, en cambio, al "Observability &
Governance Plane" de Amendment v1.1:

```pseudocode
COMPONENT AuditLedger
    consumes: ExecutionContext
    produces: AuditRecord, AgentEvent, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Amendment v1.1 (`P-25`/`INV-E10`) — Article III no tiene,
todavía, una sección propia para este componente, exactamente igual que `AdmissionController`
(CH-14), `AgentCommunicationGateway` (CH-15), `CredentialBroker` (CH-16), `IdempotencyGuard` (CH-17)
y `OperationalController` (CH-18):

```text
COMPONENT: AuditLedger

Responsibility:
    Producir y preservar, de forma estructuralmente inmutable (append-only, nunca editada ni
    borrada una vez escrita), evidencia de auditoría para una decisión crítica ya tomada por otro
    componente — capturando una referencia opaca a esa decisión, el snapshot exacto de versiones
    de agente/skill/policy/configuración de modelo/capability vigente en ese instante, y el
    actor/contexto que INV-19 exige — sin tomar ni modificar la decisión que audita, sin distribuir
    el flujo general de eventos operacionales del harness y sin autorizar el acceso de lectura al
    propio ledger.

Consumes:
    C-004 ExecutionContext (solo cuando la decisión auditada ocurrió dentro de uno real, ver
    seccion 11)

Depends on:
    (ninguno todavía — el cableado real hacia PolicyEngine/OperationalController/
    AdmissionController/CredentialBroker/IdempotencyGuard/AgentCommunicationGateway para que cada
    uno invoque de verdad recordAuditEntry sobre sus propias decisiones es Preview, no introducido
    en este capítulo; ver seccion 9)

Produces:
    C-029 AuditRecord (la evidencia inmutable en sí), C-010 AgentEvent (AUDIT_RECORD_CREATED, solo
    cuando existe un ExecutionContext y un AgentId reales para la decisión auditada — nunca la
    evidencia misma, ver seccion 14), C-011 HarnessError

Owns (Amendment v1.1 `P-25`/`INV-E10`, cita y lectura literal):
    - "Logs, traces, execution ledger and immutable audit evidence have different purposes and
      MUST NOT be conflated" (cita literal, P-25) — producir, en exclusiva, el subconjunto de
      evidencia estructuralmente inmutable que ese principio distingue de la telemetría
      operacional que EventBus (CH-09) ya distribuye
    - "Every production run records exact versions of agent, skill, policy, model configuration
      and capability contracts" (cita literal, INV-E10) — capturar el VersionSnapshot exacto
      vigente en el momento de la decisión auditada
    - correlacionar cada AuditRecord con el actor (ActorId) y, cuando existe, el contexto
      (traceId) de la decisión auditada (INV-19)
    - garantizar, por ausencia estructural de cualquier función de actualización o borrado, que un
      AuditRecord ya escrito nunca se edite ni se elimine (write-once por diseño, no por
      convención)
    - producir una garantía de integridad verificable (contentHash) sobre el contenido de cada
      AuditRecord
    - rechazar por defecto (fail-closed) un AuditRecord sin referencia de sujeto, sin actor, o con
      un VersionSnapshot incompleto

Does NOT own:
    - distribuir el flujo general de eventos operacionales del harness hacia consumidores
      desacoplados (EventBus, CMP-009, ya introducido en CH-09 — la frontera más importante de
      este capítulo: EventBus mueve un AgentEvent mutable, de alto volumen, para logs/tracing/
      debugging/replay/analytics/evals/cost analysis/UI; AuditLedger produce un subconjunto
      específico, estructuralmente inmutable, de evidencia — nunca el flujo general)
    - tomar la decisión que audita — evaluar policy (PolicyEngine, CMP-005, ya introducido en
      CH-05), aplicar control operacional (OperationalController, CMP-016, ya introducido en
      CH-18), decidir admisión (AdmissionController, CMP-012, ya introducido en CH-14), resolver
      una credencial (CredentialBroker, CMP-014, ya introducido en CH-16), o cualquier otra
      decisión crítica ya tomada por su dueño correspondiente (AuditLedger registra una decisión
      YA TOMADA, nunca la toma ni la modifica)
    - autorizar el acceso de lectura al propio ledger (Preview, fuera de alcance de este capítulo)
    - el mecanismo real y durable de almacenamiento append-only/WORM que preserva un AuditRecord
      más allá de la vida del proceso, y el algoritmo criptográfico real detrás de contentHash
      (Preview, infraestructura de borde, ver seccion 18)
    - generar por sí mismo el subjectRef o el VersionSnapshot — ambos llegan como señales de
      entrada ya resueltas (mismo patrón que targetRef en CH-18, o capabilityResolved en CH-02)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con la misma
particularidad que `AdmissionController`/`AgentCommunicationGateway`/`CredentialBroker`/
`IdempotencyGuard`/`OperationalController`: ninguna de las cinco exclusiones proviene de una ficha
propia de Article III (que no existe para este componente); provienen de fronteras ya establecidas
por componentes ya registrados. La primera exclusión de esta lista es, deliberadamente, la más
parecida en prosa informal a lo que este componente sí posee — el mismo cuidado editorial que CH-09
§8 ya aplicó frente a los nueve consumidores de Article X, y que CH-18 §8 ya aplicó frente a
`ExecutionController`.

**Nota sobre la ausencia en Article IV (segunda vez en el libro).** Igual que `EventBus` (CH-09),
Article IV no enumera ninguna fila para `AuditLedger`. Esta ausencia, otra vez, no es un descuido: es
la confirmación textual más fuerte posible de que `AuditLedger` no decide nada — preserva, sin
interpretarla, una decisión que otro componente ya tomó. `EventBus` y `AuditLedger` comparten esta
propiedad (ninguno decide), pero difieren en todo lo demás: `EventBus` mueve un flujo general y
mutable hacia N consumidores desacoplados sin preservar nada más allá del instante de la entrega;
`AuditLedger` preserva un subconjunto específico y estructuralmente inmutable, para siempre, sin
distribuirlo hacia nadie más que quien lo consulte directamente.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
AuditLedger
    consumes → ExecutionContext
    produces → AuditRecord, AgentEvent, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`AuditLedger` no depende hoy de ningún otro componente registrado — mismo patrón que CH-01..CH-18 ya
establecieron para sus propios componentes. En prosa (nunca dentro de un bloque `pseudocode`, per
`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las relaciones futuras que un capítulo
de integración agregaría son:

| Componente futuro (relación inversa — no cableada en este capítulo) | Qué relación tendría con `AuditLedger` |
|---|---|
| `PolicyEngine` (ya existente, CMP-005) | `evaluatePolicyForToolCall` (CH-05 §11) invocaría, tras producir una `PolicyDecision` con `outcome = DENY`, `recordAuditEntry` sobre esa misma decisión — el cableado exacto que este capítulo deja explícitamente para un capítulo de integración futuro, sin tocar una sola línea de CH-05 |
| `OperationalController` (ya existente, CMP-016) | `applyControlDirective` (CH-18 §11) invocaría `recordAuditEntry` tras completar un `ControlDirective`, especialmente un `KILL_SWITCH` exitoso |
| `AdmissionController` (ya existente, CMP-012) | `evaluateAdmissionForActivationRequest` (CH-14 §11) invocaría `recordAuditEntry` tras cada `AdmissionDecision`, sin importar `ADMIT`/`REJECT` |
| `CredentialBroker`, `IdempotencyGuard`, `AgentCommunicationGateway` (ya existentes, CMP-014/CMP-015/CMP-013) | cada uno invocaría `recordAuditEntry` sobre sus propias decisiones críticas ya producidas (`CredentialReference` resuelta, `IdempotencyRecord` completado, un mensaje `EXTERNAL` autorizado) |
| `EventBus` (ya existente, CMP-009) | podría distribuir, como un `AgentEvent` más, el `AUDIT_RECORD_CREATED` que `AuditLedger` emite condicionalmente (seccion 14) — exactamente igual que distribuye el de cualquier otro productor; `AuditLedger` nunca depende de `EventBus` para cumplir su propio trabajo, la evidencia ya quedó escrita antes de que ese evento exista |

`registry/components.yaml` de `CMP-005`, `CMP-009`, `CMP-012`..`CMP-016` **no se modifica** en este
capítulo: ninguno agrega `CMP-017` a sus `dependencies`, y ninguno cambia su pseudocódigo. El
pseudocódigo de la seccion 11 muestra a `AuditLedger` auditando, de forma completamente autónoma, una
`PolicyDecision` de ejemplo con la forma exacta que `PolicyEngine` (CH-05) ya produce — sin que ese
componente cambie una sola línea para que este capítulo sea correcto. Ese cableado real de punta a
punta es, explícitamente, trabajo de un capítulo de integración futuro (ver seccion 18/19).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[PolicyEngine — produce una PolicyDecision con outcome = DENY, CH-05, conceptual] → AuditLedger →
[AuditRecord — evidencia inmutable, preservada; nunca distribuida por este componente]
```

**Vista 2 — Sequence**

```text
PolicyDecision (outcome = DENY)
   │ (ya producida por PolicyEngine.evaluatePolicyForToolCall, CH-05 — conceptual, sin cambios)
   ▼
AuditLedger
   │ recordAuditEntry(subjectRef, versionSnapshot, actor, execution, agentId)
   │ ¿subjectRef vacío? sí → HarnessError (AUDIT_RECORD_MISSING_SUBJECT_REF)
   │ ¿actor vacío? sí → HarnessError (AUDIT_RECORD_MISSING_ACTOR)
   │ ¿versionSnapshot incompleto (agentVersion/policyVersion/modelConfigVersion vacíos)? sí →
   │     HarnessError (AUDIT_RECORD_INCOMPLETE_VERSION_SNAPSHOT)
   │ construye AuditRecord (id, subjectRef, versionSnapshot, actor, context, recordedAt,
   │   contentHash) — sin ningún campo de estado
   │ ¿execution y agentId ambos resueltos? sí → emite: AgentEvent (AUDIT_RECORD_CREATED) — una
   │     notificación, nunca la evidencia misma
   ▼
AuditRecord (evidencia estructuralmente inmutable — ninguna función de este componente puede
editarla ni borrarla después de este punto)
   │
   │ ... integración futura: EventBus (CH-09) podría distribuir el AUDIT_RECORD_CREATED emitido;
   │     PolicyEngine (CH-05), OperationalController (CH-18), AdmissionController (CH-14) y demás
   │     invocarían recordAuditEntry de verdad sobre sus propias decisiones ...
```

**Vista 3 — Pseudocódigo**

Ver §11: `recordAuditEntry` es la primera formalización ejecutable de "el harness preserva evidencia
inmutable de una decisión crítica ya tomada, distinta de su telemetría operacional" (`P-25`/
`INV-E10`) — construida exclusivamente a partir de material que ya existe (`ExecutionContext`/
`AgentEvent`/`HarnessError` desde CH-00, `ActorId` desde CH-06, `PolicyDecision` desde CH-05 para la
demostración) más el contrato y los `ENUM`/`STRUCT` nuevos de este capítulo.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde
CH-00/CH-05/CH-06.

```pseudocode
FUNCTION recordAuditEntry(
    subjectRef: Text,
    versionSnapshot: VersionSnapshot,
    actor: ActorId,
    execution: Optional<ExecutionContext>,
    agentId: Optional<AgentId>
) -> AuditRecord

    IF subjectRef == ""
        missingSubject: HarnessError = HarnessError(
            category = AUDIT,
            code = "AUDIT_RECORD_MISSING_SUBJECT_REF",
            message = "recordAuditEntry fue invocada sin una referencia a la decisión que se audita — un AuditRecord nunca puede escribirse sin saber qué decisión representa",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW missingSubject
    END

    IF actor == ""
        missingActor: HarnessError = HarnessError(
            category = AUDIT,
            code = "AUDIT_RECORD_MISSING_ACTOR",
            message = "recordAuditEntry fue invocada sin un actor — INV-19 exige que toda decisión crítica se trace hasta su actor, y un AuditRecord nunca lo omite",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW missingActor
    END

    IF versionSnapshot.agentVersion == ""
        OR versionSnapshot.policyVersion == ""
        OR versionSnapshot.modelConfigVersion == ""

        incompleteSnapshot: HarnessError = HarnessError(
            category = AUDIT,
            code = "AUDIT_RECORD_INCOMPLETE_VERSION_SNAPSHOT",
            message = "recordAuditEntry fue invocada con un VersionSnapshot incompleto — INV-E10 exige agentVersion, policyVersion y modelConfigVersion en todo AuditRecord",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW incompleteSnapshot
    END

    context: Optional<TraceId> = NULL
    IF execution != NULL
        context = execution.traceId
    END

    recordedAt: Timestamp = now()

    record: AuditRecord = AuditRecord(
        id = newAuditRecordId(),
        subjectRef = subjectRef,
        versionSnapshot = versionSnapshot,
        actor = actor,
        context = context,
        recordedAt = recordedAt,
        contentHash = hash(subjectRef, versionSnapshot, actor, context, recordedAt)
    )

    IF execution != NULL AND agentId != NULL
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = AUDIT_RECORD_CREATED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = record
        )
    END

    RETURN record
END
```

`now()`, `newEventId()` y `newAuditRecordId()` son las mismas primitivas de CH-00/CH-14/CH-15/CH-16/
CH-17/CH-18. `hash(...)` es una primitiva nueva, asumida legítima igual que `now()`: representa el
cómputo determinístico de una garantía de integridad verificable sobre el contenido ya construido del
registro — este capítulo modela el campo `contentHash` y el hecho de que se computa siempre, sobre
los mismos campos, de forma determinística; el algoritmo criptográfico real detrás de `hash` (SHA-256
u otro) y el mecanismo real de verificación posterior son Preview, infraestructura de borde (ver
seccion 18).

**Por qué `recordAuditEntry` recibe `execution`/`agentId` como `Optional`, y no como campos
obligatorios.** No toda decisión crítica de este libro ocurre dentro de un `AgentRun` ya arrancado —
una `AdmissionDecision` (CH-14) puede rechazar una activación antes de que exista ningún `AgentState`.
Exigir un `ExecutionContext`/`AgentId` obligatorios habría forzado a fabricar valores centinela para
ese caso, exactamente el tipo de dato inventado que este libro evita (mismo argumento que motivó
`OperationalController.applyControlDirective` a aceptar `execution: Optional<ExecutionContext>`,
CH-18 §11).

**Por qué `recordAuditEntry` verifica `subjectRef`/`actor`/`versionSnapshot` en ese orden.** El orden
refleja la severidad creciente de lo que faltaría en la evidencia si se omitiera cada verificación: sin
`subjectRef`, el registro no representa ninguna decisión identificable; sin `actor`, viola `INV-19`
directamente; con un `versionSnapshot` incompleto, el registro existe y es trazable, pero no cumple
`INV-E10` — la razón constitucional más específica, verificada al final. Mismo criterio editorial que
`applyControlDirective` (CH-18 §11) ya aplicó al comprobar `directive.status == APPLIED` antes que
cualquier verificación específica de `type`.

Ahora, con `PolicyEngine` (CMP-005, CH-05) ya existente, se puede mostrar el ejemplo que motiva este
capítulo: auditar una `PolicyDecision` real con `outcome = DENY`, exactamente como
`evaluatePolicyForToolCall` (CH-05 §11) ya la produce cuando ninguna regla concede acceso:

```pseudocode
FUNCTION demonstrateAuditingADeniedPolicyDecision(
    deniedPolicyDecision: PolicyDecision,
    subjectRef: Text,
    versionSnapshot: VersionSnapshot,
    actor: ActorId,
    execution: Optional<ExecutionContext>,
    agentId: Optional<AgentId>
) -> AuditRecord

    RETURN recordAuditEntry(subjectRef, versionSnapshot, actor, execution, agentId)
END
```

`demonstrateAuditingADeniedPolicyDecision` es una demostración de integración, no una tercera
responsabilidad nueva — mismo patrón que `demonstrateEventBusDistributingEventsFromTwoDifferentProducers`
(CH-09 §11): no modifica `CMP-005 PolicyEngine`, ni su ficha, ni la firma de
`evaluatePolicyForToolCall` (CH-05 §11), que sigue devolviendo exactamente lo mismo que devolvía antes
de este capítulo. Nótese, deliberadamente, que `recordAuditEntry` **nunca recibe**
`deniedPolicyDecision` como parámetro, y que la función de demostración nunca lee ni ramifica sobre
`deniedPolicyDecision.outcome` — el propio punto de este capítulo es que `AuditLedger` audita
genéricamente, a través de `subjectRef`, sin necesitar conocer de qué tipo de decisión se trata ni
cuál fue su resultado: un `AuditRecord` para una `PolicyDecision` con `outcome = DENY` se construye,
byte a byte, exactamente igual que uno para `outcome = ALLOW` — la asimetría de severidad entre
"denegado" y "permitido" pertenece, en exclusiva, a `PolicyEngine` (CH-05), nunca a `AuditLedger`.

`subjectRef`, en la práctica, sería la referencia opaca que correlaciona con `deniedPolicyDecision`
(p. ej. su `callId`, ya resuelto por quien invoca ambas funciones) — su resolución exacta, igual que
`targetRef` en `ControlDirective` (CH-18 §18) o `sourceRef` en `ActivationRequest` (CH-14 §18), es una
señal de entrada asumida, no construida por este capítulo.

Nótese también lo que `recordAuditEntry` **nunca hace**: no invoca
`PolicyEngine.evaluatePolicyForToolCall` (CH-05) para volver a evaluar nada — la decisión ya se tomó,
en otro lugar, antes de que este componente exista en la secuencia; no invoca
`EventBus.distributeEvent` (CH-09) para propagar el `AuditRecord` — el `AgentEvent` que emite es,
como mucho, una notificación de que el registro ya existe, nunca el vehículo de la evidencia misma; y
no ofrece, en ningún camino, ninguna función que reciba un `AuditRecord` ya construido para
modificarlo — la ausencia misma de esa función es, junto con la ausencia de un campo de estado
(seccion 6), la garantía estructural de inmutabilidad de este capítulo.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no modifica `AgentRunStatus` (C-013): sigue siendo, sin cambios, el mismo `ENUM` de
once estados que `AgentLoop` (CH-01) formalizó.

`AuditRecord` es, deliberadamente, el primer contrato nuevo de este libro **sin ningún lifecycle
propio** — a diferencia de `ControlDirective` (`ISSUED`/`APPLIED`, CH-18),
`IdempotencyRecord` (`PENDING`/`COMPLETED`, CH-17) o `EventSubscription` (`ACTIVE`/`CANCELLED`,
CH-09):

```text
(AuditRecord recién creado)
   → recordAuditEntry(...)
     RETURN AuditRecord — completo, terminal por construcción, sin ningún campo que pueda cambiar
     de valor después

(cualquier intento posterior de modificar un AuditRecord ya devuelto)
   → no existe ninguna función de este componente que lo reciba como entrada para producir una
     versión distinta — ni actualización, ni borrado; la única forma de "cambiar" un AuditRecord
     sería reemplazarlo por completo, y este capítulo no ofrece ningún mecanismo para eso
```

**Por qué la ausencia de un lifecycle es, en sí misma, la garantía — no una limitación.** `Control
Directive` e `IdempotencyRecord` necesitan un lifecycle real porque representan un proceso que ocurre
en dos momentos distintos (un comando que se emite y, después, se aplica; una ejecución que empieza y,
después, concluye). `AuditRecord` representa, en cambio, un hecho ya completamente ocurrido en el
instante en que se audita — no hay una "primera mitad" de auditar algo que deje una "segunda mitad"
pendiente. Introducir un campo de estado aquí no capturaría ningún proceso real: solo abriría, por la
sola forma del `STRUCT`, la posibilidad conceptual de que alguna función futura lo usara para
justificar una segunda escritura sobre el mismo registro — precisamente la conflación entre evidencia
y dato mutable que `P-25` prohíbe. La inmutabilidad de `AuditRecord` no depende de que
`recordAuditEntry` "se porte bien": depende de que ninguna función de este componente puede, siquiera
sintácticamente, expresar una actualización.

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6, extendido en la seccion 6 de este capítulo) clasifica también
los tres fallos reales que introduce este capítulo:

```text
AUDIT
    AUDIT_RECORD_MISSING_SUBJECT_REF          — recordAuditEntry fue invocada sin una referencia a
                                                 la decisión que se audita
        → recoverable: FALSE, retryable: FALSE
    AUDIT_RECORD_MISSING_ACTOR                — recordAuditEntry fue invocada sin un actor —
                                                 INV-19 exige trazar toda decisión crítica hasta el
                                                 suyo
        → recoverable: FALSE, retryable: FALSE
    AUDIT_RECORD_INCOMPLETE_VERSION_SNAPSHOT  — el VersionSnapshot provisto no incluye
                                                 agentVersion/policyVersion/modelConfigVersion —
                                                 INV-E10 exige las tres en todo AuditRecord
        → recoverable: FALSE, retryable: FALSE
```

Los tres fallos son `recoverable = FALSE` y `retryable = FALSE`: los tres representan un uso
incorrecto de la propia invocación a `recordAuditEntry` (una referencia de sujeto faltante, un actor
faltante, o un snapshot de versiones incompleto) — ninguno se corrige reintentando la misma operación
tal cual, sino corrigiendo lo que se le provee.

**La distinción más importante de esta sección**: ninguno de los tres fallos se clasifica como
`CONTROL` (CH-18) ni como `VALIDATION` (CH-00) — aunque, estructuralmente, los tres son "un campo
requerido llegó vacío", el mismo tipo de fallo que `EventBus` (CH-09) sí clasificó como `VALIDATION`.
La diferencia no es la forma del fallo, es su dominio: `EventBus` reutilizó `VALIDATION` porque
distribuir un evento no tiene un dominio constitucional propio más allá de "los datos de entrada
tienen la forma correcta" (CH-09 §13). Auditar sí lo tiene — `P-25` distingue explícitamente la
evidencia de auditoría de cualquier otro propósito, y reutilizar cualquier categoría ya existente
para un fallo de `AuditLedger` habría sido, en espíritu, la misma conflación que ese principio
prohíbe a nivel de propósito, ahora replicada a nivel de `ErrorCategory` — el mismo argumento que ya
usaron CH-15 §13 (contra `BUDGET`), CH-16 §13 (contra `VALIDATION`), CH-17 §13 (contra `VALIDATION`/
`BUDGET`) y CH-18 §13 (contra `CANCELLATION`).

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo de `category = INFRASTRUCTURE`
que pudiera ocurrir en el mecanismo real y durable que efectivamente preserva un `AuditRecord` más
allá de la vida del proceso, o en el algoritmo real detrás de `contentHash` — ese valor de
`ErrorCategory` sigue, después de este capítulo, sin que ningún componente real lo haya ejercitado
nunca (mismo límite que CH-11 §13/CH-14 §13/CH-15 §13/CH-16 §13/CH-17 §13/CH-18 §13 ya documentaron
para sus propias primitivas asumidas).

## 14. Eventos Producidos (Events Produced)

`AuditLedger` es el segundo componente de este libro que emite `AgentEvent` de forma **condicional**
—después de `OperationalController` (CH-18)— pero con una particularidad estructural nueva que
ningún capítulo anterior enfrentó: agrega `AUDIT_RECORD_CREATED` a `AgentEventType` (seccion 6), y lo
emite únicamente cuando `execution` y `agentId` llegan ambos resueltos a `recordAuditEntry` (seccion
11) — pero, incluso cuando lo emite, **ese evento nunca es, él mismo, la evidencia de auditoría**.

**Por qué la emisión es condicional.** Un `AgentEvent` (C-010) exige `runId`/`sessionId`/`agentId`/
`traceId` genuinos. No toda decisión crítica auditada ocurre dentro de un `AgentRun` con esos cuatro
campos ya resueltos — una `AdmissionDecision` (CH-14) puede rechazar una activación antes de que
exista ningún `AgentState`, exactamente la misma situación que ya llevó a `AdmissionController`
(CH-14) y `AgentCommunicationGateway` (CH-15) a no emitir nunca, y a `OperationalController` (CH-18) a
emitir solo para `KILL_SWITCH`.

**Por qué, incluso cuando emite, el `AgentEvent` nunca es la evidencia misma — la distinción más
importante de esta sección.** `payload = record` significa que el `AgentEvent` transporta una copia
del `AuditRecord` ya escrito — pero ese `AgentEvent`, una vez emitido, queda sujeto exactamente a las
mismas garantías (o ausencia de garantías) que cualquier otro: `EventBus` (CH-09) podría distribuirlo,
perderlo si ningún `EventSubscription` hace match, o —en teoría, si algún capítulo futuro lo
permitiera— reinterpretarlo. El `AuditRecord` real, la evidencia que `P-25` exige preservar, ya quedó
escrito y devuelto por `recordAuditEntry` **antes** de que este `AgentEvent` exista: emitirlo o no
emitirlo nunca afecta si la evidencia existe, solo si alguien más, además, se entera de que existe en
el momento en que se creó. Confundir "`AuditLedger` emitió un evento sobre haber auditado algo" con
"la auditoría ya existe" sería, precisamente, la conflación que este capítulo entero existe para
evitar.

**Por qué esto no es una limitación real hacia `INV-18`, a diferencia de la que `OperationalController`
(CH-18 §14) sí documentó para `DISABLE_CAPABILITY`/`ISOLATE_TENANT`/`ROLLBACK`.** `INV-18` exige que
"toda acción significativa produzca un evento observable" — pero la acción verdaderamente
significativa de este capítulo, preservar evidencia inmutable, ya se cumple con la sola existencia
del `AuditRecord` devuelto por `recordAuditEntry`, que no depende de `AgentEvent`/`EventBus` para
"ser" evidencia. El `AgentEvent` condicional es, aquí, una conveniencia de observabilidad adicional
—que alguien pueda enterarse, en el momento, de que una nueva auditoría se registró—, nunca el
mecanismo que hace la evidencia real.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

`AuditLedger` es el primer componente de este libro cuya responsabilidad completa es preservar, nunca
decidir ni distribuir.

**La distinción con `EventBus` (CH-09), explícita, completa y la más importante de este capítulo.**
`EventBus.distributeEvent` (CH-09) mueve, sin interpretar ni preservar, cada `AgentEvent` ya producido
hacia cualquier `EventSubscription` activa que haga match — un mecanismo de alto volumen, pensado para
`Logs`/`Tracing`/`Debugging`/`Replay`/`Analytics`/`Evals`/`Cost Analysis`/`UI` (Article X), donde
perder un evento porque nadie estaba suscrito en ese instante "no es un error" (CH-09 §12, literal).
`AuditLedger.recordAuditEntry` (este capítulo) produce, en cambio, un registro que existe por sí
mismo, sin depender de que nadie lo reciba ni de que ningún filtro haga match con nada — y que, una
vez escrito, nunca puede editarse ni borrarse. Las dos preguntas son, literalmente, ortogonales: un
`AgentEvent` puede distribuirse hacia cien suscriptores sin que ninguno preserve nada más allá del
instante de la entrega; y, a la inversa, un `AuditRecord` puede existir sin que jamás se haya
distribuido ningún evento sobre él. `P-25` exige, en una sola frase, que ambos mecanismos existan
**sin conflacionarse** — y este capítulo resuelve la mitad que `EventBus` (CH-09) reconoció, desde su
propio capítulo, que no le correspondía construir.

**El caso, superficialmente similar, que NO es el mismo problema.** Podría parecer que "Audit" —el
consumidor que Article X ya nombra desde CH-09— es, simplemente, un `subscriberRef` más de
`EventBus`, y que este capítulo era innecesario: bastaría con que alguien se suscribiera con el
`EventFilter` correcto. Este capítulo resuelve explícitamente por qué eso no basta: incluso el
`EventSubscription` más preciso solo controla **qué** `AgentEvent` llega a un consumidor, nunca **si**
ese `AgentEvent`, una vez recibido, se preserva de forma inmutable, verificable e independiente de si
`EventBus` estuvo disponible en ese instante. `AuditLedger` no reemplaza a `EventBus` como mecanismo
de distribución — construye la garantía estructural que ningún mecanismo de distribución, por
definición, puede prometer.

**La distinción con `PolicyEngine` (CH-05), `OperationalController` (CH-18) y `AdmissionController`
(CH-14), heredada de capítulos anteriores.** Cada uno de los tres decide algo real: si una acción está
autorizada, si un control operacional debe intervenir, si una activación puede proceder.
`AuditLedger` nunca toma ninguna de esas tres decisiones — solo preserva, después, evidencia de que
una de ellas ya ocurrió. Un `AuditRecord` para una `PolicyDecision` con `outcome = DENY` no vuelve a
evaluar si esa denegación fue correcta; simplemente fija, para siempre, que ocurrió, cuándo, bajo qué
actor y contra qué versiones exactas.

**Límite que este capítulo deja explícitamente abierto.** `recordAuditEntry` (seccion 11) no modela
ningún control de acceso sobre **quién** puede invocarlo, ni sobre **quién**, después, puede leer un
`AuditRecord` ya escrito — cualquier llamador puede, en este capítulo, producir un `AuditRecord` para
cualquier `subjectRef`. Autorizar la escritura y, sobre todo, autorizar la lectura del propio ledger
(una pregunta con implicaciones de seguridad reales: no todo actor debería poder leer toda la
evidencia de auditoría de todo tenant, `INV-E07`) queda, explícitamente, fuera de alcance de este
capítulo (ver seccion 18).

**`P-13`, aplicado con la misma disciplina que todo el libro.** `recordAuditEntry` no recibe ninguna
entrada que el modelo haya producido — ni siquiera de forma indirecta. El modelo no decide qué se
audita, no puede alterar un `VersionSnapshot` ya resuelto, y no puede, bajo ninguna circunstancia,
producir ni modificar un `AuditRecord` — la ausencia total del modelo en el pseudocódigo de este
capítulo es, otra vez, la materialización directa de `P-13`.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST RecordAuditEntryRejectsAnEmptySubjectRef
TEST RecordAuditEntryRejectsAnEmptyActor
TEST RecordAuditEntryRejectsAnIncompleteVersionSnapshot
TEST RecordAuditEntryProducesTheSameAuditRecordShapeRegardlessOfTheAuditedDecisionOutcome
TEST RecordAuditEntryNeverInspectsTheAuditedDecisionItself
TEST RecordAuditEntryEmitsAnAgentEventOnlyWhenExecutionAndAgentIdAreBothResolved
TEST TheEmittedAgentEventIsNeverTreatedAsTheAuditEvidenceItself
TEST AuditRecordHasNoStatusFieldAndNoUpdateOrDeleteFunctionExists
TEST AuditLedgerNeverEvaluatesPolicyOrAnyOtherDecisionOnTheSubjectItAudits
TEST AuditLedgerNeverDistributesAnAuditRecordToAnyDecoupledConsumer
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (después de CH-19 — sexto plano de Amendment v1.1 cubierto por este libro, y primer
capítulo que materializa P-25/INV-E10 con código real)

Constitution
 ├── Article IV     — Decision Ownership (tabla original sin cambios; AuditLedger, segundo
 │                     componente sin fila propia junto a EventBus, CH-09 — registrar no es
 │                     decidir)
 ├── Article X      — Observability Constitution ("Audit", uno de los nueve consumidores
 │                     nombrados desde CH-09, tiene ahora, por primera vez, un contrato de
 │                     evidencia estructuralmente inmutable que consultar — distinto del AgentEvent
 │                     que EventBus ya distribuye)
 └── Amendment v1.1 — Enterprise Activation, Interoperability and Operations
                       (P-25/INV-E10 citados por primera vez con código real; Ingress &
                       Activation Plane, CH-14, Agent Interoperability Plane, CH-15, Capability &
                       Integration Plane, CH-16, Reliability Plane, CH-17, Control Plane, CH-18, y
                       Observability & Governance Plane, este capítulo, seis de nueve planos
                       canónicos instalados)

Contracts (registry/contracts.yaml)
 ├── C-001..C-028  (sin cambios — CH-00..CH-18)
 └── C-029 AuditRecord  (CH-19, nuevo — el registro de evidencia de auditoría estructuralmente
                        inmutable, sin ningún campo de estado ni función de actualización o
                        borrado, P-25/INV-19/INV-E10)

Components (registry/components.yaml)
 ├── CMP-001..CMP-016  (sin cambios — CH-01..CH-18)
 └── CMP-017 AuditLedger  (CH-19, nuevo — sexto componente de este registry que no corresponde a
                          ninguno de los once nombres de Article III; pertenece al Observability &
                          Governance Plane de Amendment v1.1; segundo componente de todo el libro
                          sin fila propia en Article IV, junto a EventBus, CH-09)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado real de cada componente que decide hacia `recordAuditEntry`**: `PolicyEngine`
  (CH-05), `OperationalController` (CH-18), `AdmissionController` (CH-14), `CredentialBroker`
  (CH-16), `IdempotencyGuard` (CH-17) y `AgentCommunicationGateway` (CH-15) no fueron modificados
  para invocar de verdad `recordAuditEntry` sobre sus propias decisiones — la demostración de la
  seccion 11 prueba que el mecanismo funciona, no que ya esté conectado dentro de un flujo real.
- **El mecanismo real y durable de almacenamiento append-only/WORM**: este capítulo produce un
  `AuditRecord` estructuralmente inmutable en memoria, pero no modela dónde ni cómo se persiste ese
  registro más allá de la vida del proceso que lo creó — mismo límite que `registeredCapabilities`
  (CH-08) o `subscriptions` (CH-09) ya documentaron para sus propios registros asumidos.
- **El algoritmo criptográfico real detrás de `contentHash`, y su verificación posterior**: este
  capítulo modela el campo y su cómputo determinístico sobre el contenido del registro, pero no
  especifica el algoritmo (SHA-256 u otro) ni construye ninguna función `verifyAuditRecord` que
  recompute y compare ese hash contra el contenido almacenado.
- **La generación real de `subjectRef` y `VersionSnapshot`**: quién resuelve, en la práctica, la
  referencia opaca exacta a cada tipo de decisión y las cinco versiones exactas vigentes en ese
  instante — asumidas, no modeladas (mismo límite que CH-16 §18 documentó para la emisión de un
  secreto, y CH-18 §18 para la generación de un `targetRef`).
- **El concepto de "skill" como entidad propia**: `INV-E10` lo nombra literalmente, pero ningún
  contrato de este libro (`AgentConfig`, C-002, incluido) modela todavía un "skill" — `VersionSnapshot.
  skillVersion` es, deliberadamente, `Optional<Text>` opaco, sin ningún componente ni contrato
  `Skill` propio.
- **Autorización de lectura sobre el propio ledger**: quién puede consultar un `AuditRecord` ya
  escrito — señalado explícitamente en la seccion 15, no resuelto.
- **Los tres planos restantes de Amendment v1.1** (Execution Plane, Data & Context Plane, Execution
  Fabric) y **la profundización del Observability & Governance Plane más allá de este primer
  componente** (p. ej. un mecanismo real de replay o de reconstrucción de una sesión completa a
  partir de sus `AuditRecord`): explícitamente fuera de alcance.
- Reviewers plurales, evals y orquestación multi-agente propiamente dicha: explícitamente fuera de
  alcance de BH-v0.1.

## 19. Siguiente Incremento (Next Increment)

Con este capítulo, el "Observability & Governance Plane" de Amendment v1.1 tiene su primer componente
real — pero el plano completo (el cableado real hacia cada componente que decide, el mecanismo
durable de almacenamiento, la verificación de integridad, la autorización de lectura) sigue sin
construirse de punta a punta. El problema natural del próximo incremento es, o bien profundizar este
mismo plano (cableando por fin `AuditLedger` dentro de `PolicyEngine.evaluatePolicyForToolCall` y de
`OperationalController.applyControlDirective`, el mismo patrón de integración que CH-12/CH-13 ya
establecieron para el camino feliz y los caminos de gobierno de un `AgentRun`), o bien avanzar hacia
cualquiera de los tres planos restantes que Amendment v1.1 enumera junto a este — el Execution Plane
(segundo plano canónico, todavía sin cubrir por ningún capítulo de este libro), el Data & Context
Plane (quinto plano canónico, que resolvería `P-22`/`INV-E11`, señalados desde CH-16 sin un dueño
propio) o el Execution Fabric (noveno y último plano canónico) son, los tres, candidatos
particularmente naturales.

`next_chapter` queda en `null` en el frontmatter de este capítulo porque, en este momento del libro,
ese próximo capítulo todavía no existe como archivo — solo como el problema que motivaría su
escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg / Bucles
> de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows),
> secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): `P-25` fue citado, sin resolverse, seis veces seguidas
   (CH-09, CH-14, CH-15, CH-16, CH-17, CH-18) — cada capítulo reconociendo la misma ausencia sobre
   su propio contrato, sin construir jamás el mecanismo que el propio texto exige por nombre.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): un principio real y
   citado puede sobrevivir seis capítulos completos, cada uno con su propia trazabilidad parcial, sin
   que ninguno construya el mecanismo estructural que ese principio exige — evidencia distinta de la
   telemetría, y además inmutable.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `AuditLedger` con una ficha que declara tanto lo que posee (`owns`: evidencia estructuralmente
   inmutable, `VersionSnapshot` exacto) como lo que explícitamente NO posee (`does_not_own`:
   distribuir el flujo general de eventos — `EventBus`, CH-09).
4. **Modelos mentales** (= §4, Constitutional Impact): "evidencia de auditoría" y "telemetría
   operacional" comparten, a veces, el mismo origen pero nunca la misma garantía — la telemetría
   puede perderse por diseño; la evidencia, nunca.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un principio constitucional real se cita sin
  resolverse, crece la tentación de tratarlo como "ya cubierto" por el mecanismo de distribución más
  cercano — hasta que una decisión crítica necesita, de verdad, sobrevivir a una disputa, y el único
  registro disponible resulta ser un evento entre miles, sin ninguna garantía real.
- **Bucle de equilibrio (estabiliza):** `recordAuditEntry` (§11) produce un `AuditRecord` sin ningún
  campo de estado y sin ninguna función de actualización o borrado — cerrando, con una forma de
  contrato que hace la inmutabilidad imposible de violar por accidente, el bucle que CH-09..CH-18
  dejaron abierto.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `AuditRecord` (`C-029`) no tenga ningún campo de
estado ni ninguna función de actualización o borrado — a diferencia de `ControlDirective` o
`IdempotencyRecord`, ambos con un lifecycle real. Si `AuditRecord` hubiera heredado ese mismo patrón,
habría abierto, por diseño, la posibilidad conceptual de una segunda escritura sobre el mismo
registro — exactamente lo que `P-25` prohíbe. La ausencia total de un campo de estado es la forma en
que este capítulo hace la inmutabilidad estructural, no solo documentada.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo de
> esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set` (frontmatter) y
> es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa, para lectura directa
> del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Un mecanismo ya existente distribuye cada hecho significativo hacia quien se suscriba, incluido un
   consumidor dedicado a auditoría. ¿Basta esa distribución, por sí sola, para que exista evidencia
   de auditoría real? *(cierra la pregunta guía 1)*
2. ¿Le pertenece a quien tomó una decisión crítica registrar, además, evidencia inmutable de que
   ocurrió — o esa responsabilidad pertenece a otro dueño? *(cierra la pregunta guía 2)*
3. Si una decisión se toma hoy contra versiones concretas de agente, policy, modelo y capability, ¿qué
   necesitaría quedar fijado en el instante exacto de la decisión? *(cierra la pregunta guía 3)*
4. ¿Qué tendría que ser verdad, estructuralmente, para que un registro nunca pudiera editarse ni
   borrarse después de escrito? *(cierra la pregunta guía 4)*

### Explicar

1. `AuditLedger` posee producir evidencia de auditoría para una `PolicyDecision` con
   `outcome = DENY` ya tomada por `PolicyEngine`. Explica, como si hablaras con alguien sin contexto
   técnico, por qué NO posee decidir si esa acción debía denegarse.
2. `AuditRecord` nunca tiene un campo de estado, y `AuditLedger` nunca ofrece ninguna función para
   editarlo o borrarlo. Explica qué garantía real se perdería si existiera una función que permitiera
   actualizarlo, aunque nadie, en la práctica, la usara todavía.

### Conectar

1. `EventBus` (CH-09) ya distribuye cada `AgentEvent`, incluido uno con `payload = PolicyDecision`,
   hacia un consumidor de auditoría. ¿Qué le falta a esa distribución para servir, por sí sola, como
   evidencia de auditoría?
2. `PolicyEngine.evaluatePolicyForToolCall` (CH-05) ya produce una `PolicyDecision` con
   `outcome = DENY` con código real. ¿Le correspondería a esa misma función invocar el mecanismo de
   este capítulo, o pertenece a un dueño distinto?

### Espaciar

Las cinco tarjetas de repaso de este capítulo (dos sobre `AuditLedger` — su `owns` y su
`does_not_own` —, dos sobre `AuditRecord` — sus campos y por qué no tiene campo de estado —, y una
sobre `VersionSnapshot`) entran hoy en `reviewStage = DAY_1`. Repásalas de nuevo al día 3, al día 7 y
al día 21 (curva de Ebbinghaus) — ver el apéndice de tarjetas al final del libro (edición PDF) o
`retrieval_set.flashcards` en `dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te equivocaste,
ese es precisamente el punto ciego que este método existe para revelar.
