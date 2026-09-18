---
id: CH-20
title: "DataGovernanceEngine y la Etiqueta de Gobernanza que Viaja con el Dato"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-018]
introduces_contracts: [C-030]
modifies_contracts: []
constitutional_articles: [P-13, P-22, INV-18, INV-19, INV-20, INV-E11]
previous_chapter: CH-19
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH20
    text: |
      Al terminar este capítulo podrás distinguir, para cualquier dato que ya fluyó por el sistema
      (un fragmento de contexto ya seleccionado, el resultado de un side effect ya ejecutado), qué
      tramo le pertenece a la decisión de que ese dato sea relevante para razonar sobre un turno, y
      qué tramo le pertenece, en cambio, a clasificar ese mismo dato — su nivel de sensibilidad,
      dónde debe residir, hasta cuándo puede conservarse y si algo impide borrarlo aunque su plazo ya
      se haya cumplido — de forma completamente independiente de si el modelo entiende o acepta esos
      requisitos. Podrás diseñar, para esa clasificación, una etiqueta portátil que viaja junto con
      el dato a través de fronteras de componentes, y argumentar con precisión por qué una bandera de
      preservación legal debe suspender un borrado programado sin borrar, junto con él, el registro
      de cuándo ese borrado debía haber ocurrido.
  skeleton:
    id: SK-CH20
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
    components_to_be_introduced: [CMP-018]
    contracts_to_be_introduced: [C-030]
  guiding_questions:
    - id: GQ-CH20-01
      text: |
        Ya existe un componente que decide, dentro de un presupuesto explícito, qué fragmento de
        información es relevante para que el modelo razone sobre el turno actual. ¿Esa misma
        decisión de relevancia responde también cuánto tiempo puede conservarse ese fragmento, en
        qué jurisdicción debe residir, o si algo impide borrarlo aunque su plazo ya se haya
        cumplido — o son preguntas de un dominio completamente distinto?
      answered_by: RQ-CH20-01
    - id: GQ-CH20-02
      text: |
        Si un dato ya fluyó hacia el material que el modelo puede ver, o volvió como el resultado
        de un side effect real ya ejecutado, ¿qué necesitaría quedar fijado sobre ESE dato — no
        sobre la decisión que lo produjo, ni sobre si es relevante — para que alguien, después,
        supiera cuán sensible es, dónde debe residir y hasta cuándo puede conservarse?
      answered_by: RQ-CH20-02
    - id: GQ-CH20-03
      text: |
        Si una orden legal exige preservar cierta información más allá de su fecha de borrado ya
        programada, ¿qué debería pasar: la orden legal cancela ese plazo, lo reemplaza por uno
        nuevo, o existe una relación más cuidadosa entre "cuándo debía borrarse" y "por qué no
        puede borrarse todavía"?
      answered_by: RQ-CH20-03
    - id: GQ-CH20-04
      text: |
        Ya existe un mecanismo que ya sabe aplicar, sobre un tipo específico de dato altamente
        sensible, un nivel de gobierno con solo dos gradaciones. Si ahora necesitamos aplicar ese
        mismo tipo de exigencia a cualquier otro dato que fluya por el sistema — no solo a ese tipo
        específico — ¿basta con reusar exactamente ese mismo esquema de dos gradaciones, o el resto
        del sistema necesita algo distinto?
      answered_by: RQ-CH20-04
  systems_lens:
    iceberg_visible_fact: |
      Veinte capítulos reales, y `P-22` ("Enterprise data is governed throughout its lifecycle") fue
      citado en prosa, sin un dueño general, desde CH-10 §15 y CH-11 §18 — y materializado con código
      real solo una vez, en CH-16, pero exclusivamente para un secreto (`CredentialReference`), nunca
      para cualquier otro dato del sistema (ver seccion 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que un principio real y citado (`P-22`) puede resolverse de forma
      parcial y correcta —`CredentialClassification` en CH-16 es un mecanismo legítimo— sin que
      nadie generalice jamás esa misma exigencia constitucional al resto del universo de datos que
      el sistema mueve: un `ContextBlock` ya seleccionado por `ContextEngine` (CH-04), un `ToolResult`
      ya producido por `ToolRuntime` (CH-02) (ver seccion 3, Por Qué la Arquitectura Actual No
      Basta).
    iceberg_structures: |
      Este capítulo instala `DataGovernanceEngine` (`CMP-018`), el séptimo componente de este libro
      que no corresponde a ninguno de los once nombres de Article III — y el quinto plano canónico de
      Amendment v1.1 que este libro cubre (el séptimo que este libro cubre en su propio orden
      editorial) — con una ficha que declara tanto lo que posee (`owns`: clasificar cualquier dato
      que fluya por el sistema, exigir residencia/retención/legal-hold de forma independiente del
      razonamiento del modelo, producir una etiqueta portátil) como lo que explícitamente NO posee
      (`does_not_own`: seleccionar qué contexto es relevante — `ContextEngine`, CH-04, la frontera
      más importante de este capítulo — y reclasificar un secreto que `CredentialBroker` ya clasificó
      — CH-16) (ver seccion 8, Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es el mismo argumento que ya protegió la
      autorización desde `P-13` ("Authorization is deterministic and external to the LLM"), ahora
      aplicado a los datos en vez de a las acciones: que un dato sea sensible, deba residir en cierta
      jurisdicción, o esté bajo preservación legal no depende de que el modelo lo entienda, lo acepte
      o siquiera lo sepa — es una propiedad exigible del dato mismo, resuelta por completo fuera del
      razonamiento probabilístico (ver seccion 4, Impacto Constitucional).
    reinforcing_loop: |
      Cada vez que un principio constitucional real se resuelve solo para un tipo estrecho de dato
      (un secreto, CH-16), crece la tentación de tratarlo como "ya cubierto" para el resto del
      sistema — hasta que un `ContextBlock` con información de un cliente, o el `output` de un
      `ToolResult` con datos personales, necesita, de verdad, una clasificación y un plazo de
      retención, y no existe ningún mecanismo general que se los aplique.
    balancing_loop: |
      `classifyData` (seccion 11) es el mecanismo de equilibrio: deniega por defecto hacia el nivel
      de clasificación más conservador (`RESTRICTED`) cuando ninguna regla de gobernanza aplica —
      mismo principio fail-closed que `evaluatePolicyForToolCall` (CH-05) ya aplicó a la
      autorización — en vez de que un dato sin regla conocida quede, por default, sin ninguna
      protección.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `enforceRetention` (seccion 11) evalúe
      `DataGovernanceLabel.legalHold` ANTES de comparar `retentionDeadline` contra la fecha actual —
      y que, al hacerlo, nunca borre ni reemplace `retentionDeadline`. Si `legalHold` sobrescribiera
      el plazo original, se perdería la única forma de saber, una vez liberada la preservación legal,
      si el borrado ya debía haber ocurrido. Esa precedencia, y esa preservación del dato original, es
      la forma en que este capítulo hace la interacción legal-hold/retención segura por diseño, no
      solo por convención documentada.
  recall_questions:
    - id: RQ-CH20-01
      text: |
        ¿Qué componente clasifica cualquier dato que fluye por el sistema con requisitos de
        residencia/retención/legal-hold, y en qué se diferencia, con precisión, del componente que
        decide qué contexto es relevante para que el modelo razone?
      # respuesta esperada: DataGovernanceEngine (CMP-018); frontera con ContextEngine (CMP-004,
      # CH-04); P-22.
    - id: RQ-CH20-02
      text: |
        ¿Qué decide `DataGovernanceEngine`, y qué NO decide — en particular, respecto de la
        clasificación que `CredentialBroker` ya aplica sobre un secreto?
    - id: RQ-CH20-03
      text: |
        ¿Qué campos tiene `DataGovernanceLabel` (`C-030`), y por qué `classification` es un `ENUM`
        de cuatro valores en vez de un `Boolean isSensitive`?
    - id: RQ-CH20-04
      text: |
        Cuando `legalHold = TRUE` sobre un `DataGovernanceLabel` cuyo `retentionDeadline` ya pasó,
        ¿qué determina `enforceRetention`, y por qué esa función nunca borra ni reemplaza
        `retentionDeadline` para representarlo?
  explain_prompts:
    - id: EP-CH20-01
      text: |
        `DataGovernanceEngine` posee clasificar un `ContextBlock` ya seleccionado por
        `ContextEngine` con un nivel de sensibilidad, un requisito de residencia y una fecha de
        retención. Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee
        decidir si ese mismo `ContextBlock` es relevante para el turno actual — ¿qué se
        confundiría, en la práctica, si la misma pieza de software decidiera relevancia Y
        gobernanza sobre el mismo fragmento de información?
      target_entity: CMP-018
    - id: EP-CH20-02
      text: |
        `DataGovernanceLabel.legalHold`, cuando está activo, suspende cualquier borrado programado
        — pero `retentionDeadline` nunca se borra ni se reemplaza mientras esa bandera esté activa.
        Explica qué se perdería, en la práctica, si en cambio `enforceRetention` simplemente
        borrara `retentionDeadline` al activarse `legalHold`, en vez de preservarlo y solo
        suspender su efecto.
      target_entity: C-030
  interleaved_questions:
    - id: IQ-CH20-01
      text: |
        `ContextEngine.assembleContextSnapshot` (CH-04) ya produce, con código real, un
        `ContextBlock` embebido dentro de un `ContextSnapshot`, decidiendo únicamente si ese
        fragmento es relevante y cabe dentro de `execution.budget.maxInputTokens` — nunca si ese
        mismo fragmento tiene, además, un requisito de residencia, una fecha límite de retención o
        una restricción de legal-hold. Si ese `ContextBlock` ya seleccionado necesita, ahora, una
        clasificación de gobernanza, ¿le correspondería a `assembleContextSnapshot` producirla él
        mismo -ya que de todos modos está "mirando" el mismo `content`- o pertenece, otra vez, a un
        dueño distinto del que selecciona por relevancia?
      current_chapter_entities: [CMP-018, C-030]
      prior_chapter_entities: [CMP-004, C-005]
      prior_chapter: CH-04
    - id: IQ-CH20-02
      text: |
        `CredentialBroker.resolveCredentialReference` (CH-16) ya aplica, con código real, un
        `CredentialClassification` de dos valores (`CONFIDENTIAL`/`RESTRICTED`) exclusivamente sobre
        un secreto ya resuelto — y CH-16 §18 dejó documentado, explícitamente, que "un esquema de
        clasificación más rico... para CUALQUIER dato empresarial gobernado, no solo credenciales"
        pertenecía a un capítulo futuro del Data & Context Plane. Si este capítulo ahora clasifica
        un `ToolResult` cualquiera con un `DataGovernanceLabel` de cuatro niveles, ¿le correspondería
        a `DataGovernanceEngine` reclasificar, además, un `CredentialReference` ya clasificado por
        `CredentialBroker` — o esa credencial específica sigue teniendo, sin excepción, un dueño
        distinto?
      current_chapter_entities: [CMP-018, C-030]
      prior_chapter_entities: [CMP-014, C-026]
      prior_chapter: CH-16
    - id: IQ-CH20-03
      text: |
        `AuditLedger.recordAuditEntry` (CH-19) ya produce, para una decisión crítica ya tomada, un
        `AuditRecord` estructuralmente inmutable que nunca se edita ni se borra una vez escrito. Un
        `DataGovernanceLabel` de este capítulo, en cambio, puede quedar obsoleto en cuanto una
        reclasificación posterior produzca uno nuevo para el mismo `subjectRef` — nunca se edita in
        place, pero tampoco pretende ser, él mismo, evidencia permanente de que una clasificación
        concreta ocurrió en un instante dado. ¿Le bastaría a `AuditLedger` auditar un
        `DataGovernanceLabel` exactamente igual que auditó una `PolicyDecision` con
        `outcome = DENY` en CH-19, o existe una diferencia real entre "la clasificación vigente hoy
        para este dato" y "evidencia inmutable de que una clasificación concreta ocurrió"?
      current_chapter_entities: [CMP-018, C-030]
      prior_chapter_entities: [CMP-017, C-029]
      prior_chapter: CH-19
  flashcards:
    - id: FC-CH20-01
      front: |
        ¿Qué posee `DataGovernanceEngine`?
      back: |
        Clasificar cualquier dato que fluye por el sistema (un `ContextBlock` de CH-04, un
        `ToolResult` de CH-02) con un nivel de clasificación, un requisito de residencia, una fecha
        límite de retención/borrado, una bandera de legal-hold y una referencia de lineage — cita
        literal, `P-22` ("Classification, residency, retention, lineage... and legal-hold
        requirements MUST be enforceable independently of model reasoning"); producir una etiqueta
        de gobernanza (`DataGovernanceLabel`) que viaja junto con el dato a través de fronteras de
        componentes (cita literal, `INV-E11`); denegar por defecto (fail-closed) hacia el nivel de
        clasificación más conservador cuando ninguna regla de gobernanza aplica.
      source_entity: CMP-018
      chapter_introduced_in: CH-20
      review_stage: DAY_1
    - id: FC-CH20-02
      front: |
        ¿Qué NO posee `DataGovernanceEngine`, y a qué componente pertenece la frontera más
        importante de este capítulo?
      back: |
        Seleccionar, rankear o componer qué contexto es relevante para que el modelo razone sobre un
        turno (`ContextEngine`, `CMP-004`, CH-04 — frontera más importante: `ContextEngine` decide
        QUÉ entra dentro de un presupuesto; `DataGovernanceEngine` decide QUÉ REQUISITOS aplican a lo
        que ya se decidió incluir); reclasificar un secreto que `CredentialBroker` ya clasificó con
        `CredentialClassification` (`CMP-014`/`C-026`, CH-16 — esquema narrow de dos valores,
        exclusivo de credenciales, sin tocar en este capítulo); producir evidencia de auditoría
        inmutable (`AuditLedger`, `CMP-017`, CH-19); aislar operacionalmente los runs de un tenant
        (`OperationalController`, `CMP-016`, CH-18); ejecutar el borrado/cifrado/residencia física
        reales (Preview, infraestructura de borde).
      source_entity: CMP-018
      chapter_introduced_in: CH-20
      review_stage: DAY_1
    - id: FC-CH20-03
      front: |
        ¿Qué campos tiene `DataGovernanceLabel` (`C-030`)?
      back: |
        `id` (`DataGovernanceLabelId`), `subjectRef` (`Text`, referencia opaca al dato gobernado —
        un `ContextBlock`/`ToolResult`/etc., nunca el dato completo embebido), `classification`
        (`DataClassificationLevel`, `ENUM` de cuatro valores: `PUBLIC`/`INTERNAL`/`CONFIDENTIAL`/
        `RESTRICTED` — nunca un `Boolean`), `residencyRequirement` (`Optional<Text>`, referencia
        opaca a una región/jurisdicción), `retentionDeadline` (`Optional<Timestamp>`), `legalHold`
        (`Boolean`), `lineageRef` (`Optional<Text>`, referencia opaca — el grafo completo de lineage
        queda fuera de alcance) y `classifiedAt` (`Timestamp`).
      source_entity: C-030
      chapter_introduced_in: CH-20
      review_stage: DAY_1
    - id: FC-CH20-04
      front: |
        ¿Por qué `DataGovernanceLabel.legalHold` SUSPENDE un borrado programado en vez de
        reemplazar o borrar `retentionDeadline`?
      back: |
        Porque `enforceRetention` (seccion 11) evalúa `legalHold` ANTES de comparar
        `retentionDeadline` contra la fecha actual — si `legalHold` está activo, la función
        devuelve `SUSPENDED_BY_LEGAL_HOLD` sin siquiera mirar el plazo, pero el plazo original
        permanece intacto dentro del `DataGovernanceLabel`. Si `legalHold` borrara o reemplazara
        `retentionDeadline`, se perdería, para siempre, la única forma de saber — una vez liberada
        la preservación legal — si el borrado ya debía haber ocurrido antes de que la preservación
        empezara.
      source_entity: C-030
      chapter_introduced_in: CH-20
      review_stage: DAY_1
    - id: FC-CH20-05
      front: |
        `CredentialClassification` (CH-16) ya aplica un `ENUM` de dos valores exclusivamente a un
        secreto. ¿Por qué `DataGovernanceEngine` no reutiliza ni extiende ese mismo `ENUM` para
        clasificar cualquier otro dato del sistema?
      back: |
        Porque `CredentialClassification` (`CONFIDENTIAL`/`RESTRICTED`) modela, deliberadamente, el
        piso mínimo de un secreto — ningún secreto es jamás `PUBLIC` ni meramente `INTERNAL` — y
        extenderlo habría requerido reabrir `CredentialReference` (`C-026`, CH-16), un contrato ya
        registrado que este capítulo no modifica (`modifies_contracts: []`). `DataClassificationLevel`
        (cuatro valores, este capítulo) cubre, en cambio, el universo completo de datos que el
        sistema mueve — incluyendo datos que sí pueden ser `PUBLIC` o `INTERNAL`, algo que un
        secreto nunca es. CH-16 §18 ya señaló explícitamente esta generalización como trabajo de un
        capítulo futuro del Data & Context Plane — este capítulo resuelve esa deuda sin tocar el
        contrato de CH-16.
      source_entity: C-030
      chapter_introduced_in: CH-20
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH20-01
      recall_question: RQ-CH20-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH20-02
      recall_question: RQ-CH20-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH20-03
      recall_question: RQ-CH20-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH20-04
      recall_question: RQ-CH20-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 20 — DataGovernanceEngine y la Etiqueta de Gobernanza que Viaja con el Dato

> **Regla constitucional (Amendment v1.1, `P-22`):** "Classification, residency, retention, lineage,
> encryption, deletion and legal-hold requirements MUST be enforceable independently of model
> reasoning."
>
> **Regla constitucional (Amendment v1.1, `INV-E11`):** "Data governance policy follows context and
> artifacts across component boundaries."

CH-14, CH-15, CH-16, CH-17, CH-18 y CH-19 abrieron seis de los nueve planos canónicos de Amendment
v1.1 — Ingress & Activation (`AdmissionController`), Agent Interoperability
(`AgentCommunicationGateway`), Capability & Integration (`CredentialBroker`), Reliability
(`IdempotencyGuard`), Control (`OperationalController`) y Observability & Governance
(`AuditLedger`). Este capítulo entra al **séptimo plano que este libro cubre** — el **Data & Context
Plane**, que en la enumeración de la enmienda ocupa la **quinta** posición (Ingress & Activation →
Execution → Agent Interoperability → Capability & Integration → **Data & Context** → Control →
Reliability → Observability & Governance → Execution Fabric) — el mismo patrón de salto que ya usaron
`IdempotencyGuard` (CH-17, Reliability, séptimo canónico), `OperationalController` (CH-18, Control,
sexto canónico) y `AuditLedger` (CH-19, Observability & Governance, octavo canónico): este libro no
cubre los nueve planos en su orden canónico, sino en el orden en que cada uno adquiere una razón de
peso para escribirse. Con este capítulo, solo dos planos canónicos quedan sin cubrir por este libro:
Execution Plane (segundo canónico) y Execution Fabric (noveno canónico).

La razón de peso, aquí, tampoco es nueva. `P-22` ("Enterprise data is governed throughout its
lifecycle") fue citado en prosa por primera vez en CH-10 §15 y repetido en CH-11 §18, como un límite
reconocido pero no resuelto — y CH-16 fue el primer capítulo en materializarlo con código real, pero
únicamente para un tipo de dato: un secreto (`CredentialReference`). CH-16 §18 dejó, explícitamente,
la generalización pendiente: "un esquema de clasificación más rico... residencia, retención con
ventana explícita, lineage, encriptación y legal-hold — el resto de lo que `P-22` enumera para
*cualquier* dato empresarial gobernado, no solo credenciales — queda fuera de alcance; ese trabajo
pertenece, con mayor propiedad, a un capítulo futuro del 'Data & Context Plane'." CH-19 §19 confirmó
la misma deuda desde el lado opuesto: "Data & Context Plane (quinto plano canónico, que resolvería
`P-22`/`INV-E11`, señalados desde CH-16 sin un dueño propio)". Este capítulo, el vigesimoprimer
capítulo real de contenido de este libro, es el primero en generalizar `P-22` más allá de las
credenciales, con código real.

Ningún texto de la Constitution nombra literalmente un componente para esto — igual que
`IdempotencyGuard` (CH-17), `OperationalController` (CH-18) y `AuditLedger` (CH-19), el nombre que
este capítulo adopta, `DataGovernanceEngine`, es una **síntesis de este libro**, evaluada
explícitamente contra alternativas (`DataClassifier`, descartado porque "Classifier" sugiere que la
única responsabilidad es asignar un nivel de sensibilidad, sin transmitir que este componente también
exige residencia, retención, legal-hold y lineage — la mitad restante de `P-22`; `ComplianceEngine`,
descartado porque "Compliance" implica juzgar activamente si el sistema cumple una regulación
concreta, una decisión de alcance mucho mayor y de un dominio distinto a simplemente clasificar un
dato y exigir sus requisitos mecánicos — además, "Engine" junto a "Compliance" invita a confundirlo
con `PolicyEngine`, CH-05, que autoriza acciones, no datos) y elegida porque `P-22` se titula,
literalmente, "Enterprise data is governed throughout its lifecycle": "Governance" transporta, sin
ambigüedad, la amplitud completa del principio (clasificación + residencia + retención + lineage +
legal-hold) sin implicar un juicio regulatorio que este componente nunca hace (ver seccion 8).

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de saber
> cómo se llama el componente de este capítulo. El detalle estructurado de esta sección vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, para cualquier dato que ya
fluyó por el sistema (un fragmento de contexto ya seleccionado, el resultado de un side effect ya
ejecutado), qué tramo le pertenece a la decisión de que ese dato sea relevante para razonar sobre un
turno, y qué tramo le pertenece, en cambio, a clasificar ese mismo dato — su nivel de sensibilidad,
dónde debe residir, hasta cuándo puede conservarse y si algo impide borrarlo aunque su plazo ya se
haya cumplido — de forma completamente independiente de si el modelo entiende o acepta esos
requisitos. Podrás diseñar, para esa clasificación, una etiqueta portátil que viaja junto con el dato
a través de fronteras de componentes, y argumentar con precisión por qué una bandera de preservación
legal debe suspender un borrado programado sin borrar, junto con él, el registro de cuándo ese
borrado debía haber ocurrido.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e introduce
un contrato de datos nuevo y el séptimo componente de este libro que pertenece a Amendment v1.1 en
vez de a los once nombres originales de Article III.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar atrás;
están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este capítulo va
a definir):

1. Ya existe un componente que decide, dentro de un presupuesto explícito, qué fragmento de
   información es relevante para que el modelo razone sobre el turno actual. ¿Esa misma decisión de
   relevancia responde también cuánto tiempo puede conservarse ese fragmento, en qué jurisdicción
   debe residir, o si algo impide borrarlo aunque su plazo ya se haya cumplido — o son preguntas de
   un dominio completamente distinto?
2. Si un dato ya fluyó hacia el material que el modelo puede ver, o volvió como el resultado de un
   side effect real ya ejecutado, ¿qué necesitaría quedar fijado sobre ESE dato — no sobre la
   decisión que lo produjo, ni sobre si es relevante — para que alguien, después, supiera cuán
   sensible es, dónde debe residir y hasta cuándo puede conservarse?
3. Si una orden legal exige preservar cierta información más allá de su fecha de borrado ya
   programada, ¿qué debería pasar: la orden legal cancela ese plazo, lo reemplaza por uno nuevo, o
   existe una relación más cuidadosa entre "cuándo debía borrarse" y "por qué no puede borrarse
   todavía"?
4. Ya existe un mecanismo que ya sabe aplicar, sobre un tipo específico de dato altamente sensible,
   un nivel de gobierno con solo dos gradaciones. Si ahora necesitamos aplicar ese mismo tipo de
   exigencia a cualquier otro dato que fluya por el sistema — no solo a ese tipo específico —
   ¿basta con reusar exactamente ese mismo esquema de dos gradaciones, o el resto del sistema
   necesita algo distinto?

## 1. Arquitectura Actual (Current Architecture)

CH-00..CH-19 dejaron instalados veintinueve contratos de datos y diecisiete componentes: los once
nombres completos de Article III ("Agent Runtime"), dos capítulos de integración, y seis componentes
de Amendment v1.1 (`AdmissionController`, CMP-012, CH-14; `AgentCommunicationGateway`, CMP-013,
CH-15; `CredentialBroker`, CMP-014, CH-16; `IdempotencyGuard`, CMP-015, CH-17;
`OperationalController`, CMP-016, CH-18; `AuditLedger`, CMP-017, CH-19).

`ContextEngine` (CMP-004, CH-04) es, de los diecisiete, el único cuya responsabilidad completa incluye
decidir qué material candidato termina formando parte de lo que el modelo ve. `assembleContextSnapshot`
(CH-04 §11) selecciona, rankea, compone y compacta cada `AgentMessage` candidato dentro de
`execution.budget.maxInputTokens`, produciendo un `ContextBlock` por cada fragmento incluido —con
`provenance`/`content`/`compacted`— embebido dentro de `ContextSnapshot` (C-005). CH-04 §15 ya
reconoció explícitamente, como la frontera más sutil que el libro había trazado hasta ese momento, que
"seleccionar por relevancia" (P-14, propio de `ContextEngine`) y "autorizar qué puede verse en
absoluto" (Article IV, `PolicyEngine`) son dos preguntas de dominios distintos — pero ninguna de las
dos, ni siquiera juntas, responde una tercera pregunta que ningún capítulo hasta este había separado
explícitamente: dado un `ContextBlock` ya relevante Y ya autorizado, ¿qué tan sensible es, dónde debe
residir, y hasta cuándo puede conservarse?

`ToolRuntime` (CMP-002, CH-02) produce, del mismo modo, un `ToolResult` (C-009) por cada `ToolCall`
ejecutado — el dato real que vuelve de un side effect. `ToolResult.output` puede contener, en la
práctica, cualquier cosa que la implementación real de una capability devuelva: datos de un cliente,
contenido de un documento, resultados de una consulta — sin que ningún componente del libro, hasta
este capítulo, clasifique jamás ese contenido.

`P-22` ("Enterprise data is governed throughout its lifecycle") fue citado en prosa, sin resolverse
con código, por CH-10 §15 (`SessionManager`, al persistir `AgentState`/checkpoints) y CH-11 §18
(`AgentCore`, al integrar el camino feliz completo) — ambos reconociendo la misma ausencia: nada en el
libro clasifica, hasta ese punto, ningún dato real. CH-16 fue el primer capítulo en materializar `P-22`
con código real, pero exclusivamente sobre un tipo estrecho de dato: `CredentialReference` (C-026),
con un `classification: CredentialClassification` (`ENUM` de dos valores, `CONFIDENTIAL`/
`RESTRICTED`) y un `expiresAt: Optional<Timestamp>` — la mitad de "retention" aplicada, sin ningún
campo para residencia, lineage o legal-hold, y sin ningún mecanismo que aplique lo mismo a cualquier
dato que no sea un secreto. CH-16 §18 documentó, en su propia lista de límites, exactamente esta
generalización pendiente, atribuyéndola "con mayor propiedad" a un capítulo futuro del Data & Context
Plane.

`INV-E11` ("Data governance policy follows context and artifacts across component boundaries") no
había sido citado por ningún capítulo hasta este — ningún contrato del libro, hasta ahora, modela una
etiqueta de gobernanza diseñada explícitamente para viajar, adosada a un dato, a través de las
fronteras de más de un componente.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas para esto, "gobernar un dato" tiende a colapsarse,
silenciosamente, en una de dos suposiciones igual de incompletas. La primera: que si `ContextEngine`
ya decide qué es relevante, y `PolicyEngine` (preview desde CH-04, real desde CH-05) ya decide qué
puede verse, entonces no queda ninguna pregunta más por responder sobre ese mismo dato — pero
relevancia y autorización de visibilidad, como CH-04 §15 ya distinguió, nunca respondieron "¿cuán
sensible es este dato, en qué jurisdicción debe residir, y hasta cuándo puede conservarse?". La
segunda: que, como `CredentialBroker` (CH-16) ya resuelve `P-22` para un secreto, el principio ya
está "cubierto" — pero un `ContextBlock` con información de un cliente, o el `output` de un
`ToolResult` con datos personales, nunca pasan por `CredentialBroker`, y por lo tanto nunca reciben
ninguna clasificación, ningún requisito de residencia, ninguna fecha de retención.

Hay una segunda dimensión del problema, más delicada. `P-22` exige, literalmente, que estos requisitos
sean "enforceable independently of model reasoning" — el mismo argumento de fondo que `P-13` ya aplicó
a la autorización de acciones ("Authorization is deterministic and external to the LLM"), ahora
aplicado a los datos: que un dato sea `RESTRICTED`, deba residir en cierta región, o esté bajo
preservación legal no puede depender de que el modelo lo entienda, lo acepte, o siquiera lo perciba.
Sin un componente dedicado, la única forma en que un sistema real terminaría "respetando" esos
requisitos sería que el propio modelo, dentro de su razonamiento, decidiera tratarlos con cuidado —
exactamente la dependencia de cooperación del modelo que `P-13`/`P-22` prohíben.

Hay una tercera dimensión: legal-hold. Si una orden legal exige preservar un dato más allá de su fecha
de borrado ya programada, y el mecanismo que aplica esa preservación simplemente sobrescribe o borra
la fecha original, se pierde la única forma de saber, una vez que la preservación legal se libere, si
el borrado ya debía haber ocurrido. Necesitamos que esa interacción quede modelada con cuidado, no
resuelta con un campo `Boolean` que, al activarse, destruye información que después hará falta.

Necesitamos que "clasificar un dato con requisitos exigibles de forma independiente del razonamiento
del modelo" tenga, por fin, un dueño único y nombrado — que produzca una etiqueta portátil, capaz de
viajar junto con el dato a través de las fronteras de cualquier componente (`INV-E11`), sin necesitar
reabrir el contrato de `CredentialReference` que CH-16 ya registró, y sin absorber, en el proceso, la
decisión de relevancia que ya pertenece a `ContextEngine`.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los veintinueve contratos y los diecisiete componentes que existen hasta este punto no bastan porque:

- `P-22` fue citado en prosa dos veces (CH-10, CH-11) y materializado con código real solo una vez
  (CH-16) — y esa única materialización real declara, explícitamente en su propia sección 18, que su
  alcance se limita a un secreto, dejando "cualquier dato empresarial gobernado, no solo
  credenciales" sin ningún mecanismo;
- `ContextBlock` (embebido en `ContextSnapshot`, C-005, CH-04) registra `provenance` y `compacted`,
  pero ningún campo de clasificación, residencia, retención o legal-hold — y `ContextEngine.
  does_not_own` (CH-04 §8) ya excluyó explícitamente cualquier decisión de autorización sobre ese
  mismo `content`, dejando un vacío real entre "es relevante y está autorizado" y "tiene requisitos
  de gobierno";
- `ToolResult` (C-009, CH-02) no declara ningún campo de clasificación sobre su `output` — el
  contenido real que vuelve de cualquier side effect ejecutado queda, hasta este capítulo, sin
  ninguna forma normalizada de saber cuán sensible es;
- `CredentialClassification` (CH-16) es, deliberadamente, un `ENUM` de dos valores diseñado para el
  piso mínimo de un secreto (nunca `PUBLIC`, nunca meramente `INTERNAL`) — extenderlo para cubrir el
  universo completo de datos habría exigido reabrir `CredentialReference` (C-026), un contrato ya
  registrado, para una responsabilidad que nunca le perteneció a `CredentialBroker` en primer lugar;
- ningún contrato de este libro modela, todavía, una etiqueta diseñada para viajar junto con un dato
  a través de fronteras de componentes — `INV-E11` ("Data governance policy follows context and
  artifacts across component boundaries") no había sido citado con código real por ningún capítulo
  hasta este;
- nada impide, hoy, que una bandera de preservación legal, si se modelara sin cuidado, borre o
  reemplace la fecha de retención original — perdiendo, para siempre, la evidencia de cuándo el
  borrado debía haber ocurrido antes de que la preservación empezara;
- ningún componente de este libro declara, todavía, `owns` una responsabilidad que sea, literalmente,
  "clasificar el dato mismo" en vez de "seleccionar qué dato es relevante", "autorizar una acción" o
  "resolver un secreto" — las tres categorías más cercanas que Article III/CH-04/CH-05/CH-16 ya
  cubrieron, dejando a `P-22` general sin un cuarto dueño hasta este capítulo.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la secuencia
> `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una entidad que no
> haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT` registrado — **no
> magic entities**. Este capítulo aplica la misma disciplina que CH-00..CH-19 ya establecieron, con
> una particularidad que merece cuidado: a diferencia de `AuditRecord` (CH-19), que deliberadamente
> no tiene ningún lifecycle porque audita un hecho ya completamente ocurrido,
> `DataGovernanceLabel` describe un requisito que puede cambiar en el tiempo (una preservación legal
> que se activa o se libera, una reclasificación posterior) — sin que eso signifique que el propio
> `STRUCT` necesite un campo de estado mutable (ver seccion 12 para el desarrollo completo).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-13   Authorization is deterministic and external to the LLM.
           El mismo argumento que ya protegió la autorización desde CH-01/CH-05, la credencial
           desde CH-16, la deduplicación desde CH-17, el control operacional desde CH-18 y la
           evidencia de auditoría desde CH-19, se extiende aquí a la gobernanza de datos: el
           modelo nunca decide, nunca ve y nunca constituye una fuente de verdad sobre la
           clasificación, residencia, retención o legal-hold de un dato — classifyData y
           enforceRetention (seccion 11) son completamente determinísticas y externas al LLM.
    P-22   Enterprise data is governed throughout its lifecycle.
           Primera materialización real, con código, de este principio aplicada a CUALQUIER dato
           del sistema — no solo a un secreto (CredentialReference, CH-16). DataGovernanceLabel
           (seccion 6/7) y DataGovernanceEngine (seccion 8) generalizan, por fin, la exigencia que
           CH-16 §18 dejó explícitamente pendiente.

Invariants preserved
    INV-18    Toda acción significativa produce un evento observable.
              classifyData y enforceRetention (seccion 11) emiten un AgentEvent (DATA_CLASSIFIED /
              RETENTION_ENFORCEMENT_EVALUATED) cuando existe un ExecutionContext y un AgentId
              reales — pero, con la misma disciplina que CH-18/CH-19 aplicaron a sus propias
              funciones, nunca fabrican esos campos cuando no existen (ver seccion 14).
    INV-19    Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy
              relevante.
              A diferencia de AuditRecord (CH-19), que almacena actor/context como campos
              permanentes del propio contrato, DataGovernanceLabel no lo hace (ver seccion 6 para
              el porqué explícito) — la trazabilidad de INV-19 se satisface aquí a través del
              traceId que cada AgentEvent emitido ya transporta, el mismo tratamiento que
              ContextEngine (CH-04) ya aplicó a CONTEXT_SNAPSHOT_ASSEMBLED.
    INV-20    Todo error operacional pertenece a una categoría conocida.
              Los dos fallos reales de este capítulo (seccion 13) introducen GOVERNANCE, una
              categoría nueva de ErrorCategory — deliberadamente NO reutiliza CONTEXT (CH-04),
              CREDENTIAL (CH-16) ni AUDIT (CH-19), por la misma razón de fondo que motiva todo este
              capítulo: conflacionar un fallo de gobernanza de datos con el fallo de cualquier otro
              dominio sería, en espíritu, la misma conflación de responsabilidades que Article IV
              prohíbe a nivel de componente, ahora aplicada a nivel de ErrorCategory.
    INV-E11   Data governance policy follows context and artifacts across component boundaries.
              Cita literal y definitoria de este capítulo — DataGovernanceLabel (C-030) es, por
              diseño, un contrato de datos independiente y portátil (nunca un campo embebido
              dentro de ContextBlock o ToolResult) precisamente para que pueda viajar, referenciado
              por subjectRef, a través de cualquier componente que necesite consultarlo — sin que
              ContextBlock/ToolResult necesiten reabrirse para cargarlo.

Component ownership changes
    CMP-018 DataGovernanceEngine se introduce — registry/components.yaml pasa de 17 a 18
    componentes. Es el séptimo componente de este registry que NO corresponde a ninguno de los
    once nombres del árbol de Article III ("Agent Runtime") — pertenece, en cambio, al "Data &
    Context Plane" de Amendment v1.1 (el quinto plano canónico, séptimo que este libro cubre — ver
    apertura del capítulo).
    registry/components.yaml de CMP-004 (ContextEngine), CMP-002 (ToolRuntime), CMP-014
    (CredentialBroker), CMP-017 (AuditLedger) NO se modifica: ninguno cablea todavía su relación
    real con DataGovernanceEngine (ver seccion 9/18).

Lifecycle changes
    Ninguna modificación al ENUM AgentRunStatus (C-013): sigue siendo, sin cambios desde CH-01, el
    mismo conjunto de once valores. DataGovernanceLabel (C-030), igual que AuditRecord (C-029,
    CH-19), no introduce ningún ENUM de lifecycle propio — pero por una razón distinta a la de
    AuditRecord (ver seccion 12 para el desarrollo completo de esta distinción).

Security implications
    DataGovernanceEngine es el primer componente de este libro cuya responsabilidad completa es
    clasificar el dato mismo, independientemente de si es relevante o si está autorizado para
    verse. Ver seccion 15 para el análisis completo, incluyendo la frontera más importante de este
    capítulo, contra ContextEngine, y la frontera más precisa, contra CredentialBroker.

Observability implications
    Igual que ContextEngine (CH-04), AuditLedger (CH-19) y OperationalController (CH-18),
    DataGovernanceEngine emite AgentEvent de forma condicional — pero es el primer componente que
    lo hace desde DOS funciones distintas con DOS eventos distintos (DATA_CLASSIFIED,
    RETENTION_ENFORCEMENT_EVALUATED), ninguno de los cuales es, él mismo, evidencia de auditoría
    inmutable (frontera con AuditLedger, ver seccion 15).

Deterministic vs agentic boundary
    Article XII se refina una decimoctava vez a nivel de componente: DataGovernanceEngine, igual
    que EventBus (CH-09), OperationalController (CH-18) y AuditLedger (CH-19), no recibe ninguna
    entrada que el modelo haya producido — ni siquiera de forma indirecta. Evalúa exclusivamente
    una referencia opaca a un dato ya existente, una procedencia ya conocida y una bandera de
    legal-hold ya decidida por un proceso externo — todos ajenos a cualquier razonamiento del
    modelo.
```

## 5. Conceptos Nuevos (New Concepts)

- **Data Classification** *(cita literal, `P-22`, "Classification... MUST be enforceable
  independently of model reasoning")*: el nivel de sensibilidad que se asigna a un dato concreto —
  modelado como `DataClassificationLevel` (`ENUM` de cuatro valores, seccion 6), nunca un `Boolean`
  "es sensible o no". Distinto de `CredentialClassification` (CH-16), un esquema más estrecho de dos
  valores exclusivo de secretos (ver seccion 3).
- **Data Residency** *(lectura de `P-22`, "residency")*: el requisito de que un dato deba procesarse
  o almacenarse dentro de una región o jurisdicción concreta — modelado como
  `DataGovernanceLabel.residencyRequirement` (`Optional<Text>`), una referencia opaca cuyo
  significado exacto (qué región, bajo qué régimen regulatorio) es una señal de entrada asumida, no
  modelada por este capítulo.
- **Legal Hold** *(cita literal, `P-22`, "legal-hold requirements MUST be enforceable independently
  of model reasoning")*: la bandera que, cuando está activa, suspende cualquier borrado programado
  sobre un dato — independientemente de si su `retentionDeadline` ya se cumplió. Modelada como
  `DataGovernanceLabel.legalHold` (`Boolean`) más la precedencia explícita que `enforceRetention`
  (seccion 11) le da sobre cualquier evaluación de plazo.
- **Data Lineage (Opaque)**: de dónde vino un dato, en el sentido de qué transformación o fuente lo
  produjo — modelada como `DataGovernanceLabel.lineageRef` (`Optional<Text>`), una referencia opaca;
  el grafo completo de lineage (qué transformó a qué, en qué orden) queda, deliberadamente, fuera de
  alcance de este capítulo (ver seccion 18).
- **Governance Label Portability** *(cita literal, `INV-E11`, "Data governance policy follows
  context and artifacts across component boundaries")*: la propiedad de que la clasificación de un
  dato no viva embebida dentro del propio dato (`ContextBlock`, `ToolResult`), sino como un contrato
  independiente (`DataGovernanceLabel`) referenciado por `subjectRef` — de modo que pueda consultarse
  desde cualquier componente que necesite conocer los requisitos de gobierno de ese dato, sin que el
  contrato original tenga que reabrirse para cargarlo.
- **Retention Enforcement**: la evaluación, en un instante dado, de si el borrado programado de un
  dato ya es exigible, sigue sin ser exigible todavía, o está suspendido por una preservación legal —
  modelada como `enforceRetention` (seccion 11) y su resultado, `RetentionEnforcementOutcome`
  (`ENUM` de tres valores, seccion 6).
- **Decision Ownership, aplicado por séptima vez** *(Article IV)*: `DataGovernanceEngine` decide
  "¿qué requisitos de gobierno aplican a este dato?"; explícitamente NO decide "¿es este dato
  relevante para el turno actual?" (`ContextEngine`, ya resuelto, CH-04), "¿puede verse este dato en
  absoluto?" (`PolicyEngine`, ya resuelto, CH-05), "¿cuál es la clasificación de este secreto
  específico?" (`CredentialBroker`, ya resuelto, CH-16) ni "¿esta decisión ya ocurrida necesita
  evidencia inmutable?" (`AuditLedger`, ya resuelto, CH-19) — la primera de estas cuatro exclusiones
  es la frontera más importante de este capítulo (ver seccion 15).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `Text`, `Timestamp`, `Boolean`, `Optional`, `AgentId`,
`ExecutionContext` (C-004, CH-00), `AgentEvent` (C-010, CH-00), `HarnessError` (C-011, CH-00),
`ContextBlock` (embebido en C-005, CH-04).

Este capítulo cita, sin redefinirlo, un contrato ya registrado de un capítulo anterior — mismo patrón
de reuso explícito que CH-13 §6, CH-18 §6 y CH-19 §6 ya aplicaron:

| Contrato/tipo (reusado, no nuevo) | Introducido en | Uso en este capítulo |
|---|---|---|
| `CredentialClassification` | CH-16 §6 | citado en prosa (seccion 3/5/8) como el precedente narrow de dos valores exclusivo de secretos — nunca usado dentro del pseudocódigo de este capítulo |
| `ContextBlock` | CH-04 §6 | tipo del parámetro `block` de `demonstrateClassifyingAContextBlock` (seccion 11) — el `STRUCT` embebido dentro de `ContextSnapshot` (C-005) que `ContextEngine.assembleContextSnapshot` ya produce, reusado sin modificarlo |

### Un identificador opaco nuevo

Siguiendo el mismo patrón que CH-00 §6 estableció para los identificadores fundamentales, y que
CH-14..CH-19 repitieron para los suyos:

| Identificador (nuevo de este capítulo) | Identifica |
|---|---|
| `DataGovernanceLabelId` | un `DataGovernanceLabel` concreto — la etiqueta de gobernanza vigente producida para un dato dado en el instante de su clasificación |

### `ErrorCategory` — extendido, sin redefinir `HarnessError`

Este es el noveno capítulo que agrega un valor a `ErrorCategory` desde que CH-00 lo declaró (después
de `HUMAN_INTERACTION`, CH-06; `ADMISSION`, CH-14; `DELEGATION`, CH-15; `CREDENTIAL`, CH-16;
`IDEMPOTENCY`, CH-17; `CONTROL`, CH-18; y `AUDIT`, CH-19): el valor `GOVERNANCE`, necesario porque
ninguna de las diecisiete categorías ya existentes representa, sin conflación, un fallo específico de
clasificación o gobernanza de datos — reutilizar `CONTEXT` (CH-04, propio de la selección de
material) o `CREDENTIAL` (CH-16, propio de un secreto específico) habría sido, precisamente, el tipo
de conflación de dominios que Article IV prohíbe a nivel de componente, ahora aplicada a nivel de
`ErrorCategory`:

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
END
```

`HarnessError` (C-011) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — mismo patrón
exacto que las extensiones de CH-06/CH-14/CH-15/CH-16/CH-17/CH-18/CH-19, aplicado aquí por octava vez
a `ErrorCategory`.

### `AgentEventType` — extendido, sin redefinir `AgentEvent`

CH-19 dejó `AgentEventType` en veintiocho valores. Este capítulo agrega dos valores nuevos — el
primer capítulo desde `IdempotencyGuard` (CH-17) en agregar más de uno, porque introduce dos funciones
reales (`classifyData`, `enforceRetention`) en vez de una sola:

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
END
```

`AgentEvent` (C-010) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — solo el rango de
valores permitido para `eventType` crece, igual que en cada capítulo anterior salvo `EventBus`
(CH-09), `AdmissionController` (CH-14) y `AgentCommunicationGateway` (CH-15).

### `DataClassificationLevel` — el nivel de sensibilidad, nunca un `Boolean`

```pseudocode
ENUM DataClassificationLevel
    PUBLIC
    INTERNAL
    CONFIDENTIAL
    RESTRICTED
END
```

**Por qué un `ENUM` de cuatro valores, y no un `Boolean isSensitive`, ni tampoco los dos valores de
`CredentialClassification` (CH-16).** Se evaluó explícitamente un `Boolean` — más simple de construir
— y se descartó por el mismo argumento que ya descartó `allowAll: Boolean` en `DelegationGrant`
(CH-15 §6) y que motivó, precisamente, el `ENUM` de dos valores de `CredentialClassification`: no
todo dato carga el mismo riesgo, y un `Boolean` de dos estados colapsaría esa diferencia real a un
solo bit. Se evaluó también, explícitamente, reutilizar `CredentialClassification` directamente para
este capítulo — se descartó porque ese `ENUM` modela, deliberadamente, el piso mínimo de un secreto
(ningún secreto es jamás `PUBLIC` ni meramente `INTERNAL`, CH-16 §6); el universo de datos que
`DataGovernanceEngine` clasifica es más amplio — incluye datos que sí pueden ser completamente
públicos o de uso interno sin ningún riesgo comparable al de un secreto — y forzar ese universo
completo dentro de un `ENUM` de dos valores habría subestimado la mitad menos sensible del espectro.
Cuatro valores, ordenados de menor a mayor sensibilidad, son el mínimo necesario para representar esa
gradación sin inventar más niveles de los que este capítulo necesita demostrar.

### `RetentionEnforcementOutcome` — el resultado de evaluar retención, nunca un `Boolean`

```pseudocode
ENUM RetentionEnforcementOutcome
    NOT_YET_DUE
    DELETION_DUE
    SUSPENDED_BY_LEGAL_HOLD
END
```

**Por qué tres valores, y no un `Boolean deletionRequired`.** Se evaluó explícitamente un `Boolean` —
y se descartó porque colapsaría dos situaciones completamente distintas dentro del mismo valor
`FALSE`: "el plazo de retención todavía no se cumple" (nada fuera de lo común) y "el plazo ya se
cumplió, pero una preservación legal lo suspende" (una situación que alguien con autoridad sobre esa
preservación necesita poder distinguir explícitamente, no inferir). Un `Boolean` habría hecho
estructuralmente imposible representar esa diferencia — el mismo argumento, aplicado aquí a un
resultado en vez de a una clasificación, que ya motivó `DataClassificationLevel` en esta misma
sección y `ControlDirectiveStatus` en CH-18 §6.

### `DataGovernanceLabel` — la etiqueta de gobernanza que viaja con el dato

```pseudocode
STRUCT DataGovernanceLabel
    id: DataGovernanceLabelId
    subjectRef: Text
    classification: DataClassificationLevel
    residencyRequirement: Optional<Text>
    retentionDeadline: Optional<Timestamp>
    legalHold: Boolean
    lineageRef: Optional<Text>
    classifiedAt: Timestamp
END
```

Ocho campos, cada uno respondiendo a una parte exacta del alcance decidido para este capítulo: `id`
identifica esta etiqueta de forma estable; `subjectRef` es una referencia opaca (`Text`) al dato
gobernado — el `provenance` de un `ContextBlock` (CH-04), el `callId` de un `ToolResult` (CH-02), o
cualquier otro dato que este libro produzca — **nunca embebiendo el dato completo**, el mismo
argumento que ya usó `AuditRecord.subjectRef` (CH-19) y `ControlDirective.targetRef` (CH-18) para no
cargar una copia de un objeto ajeno; `classification` es el `DataClassificationLevel` de la sección
anterior; `residencyRequirement` y `lineageRef` son referencias opacas `Optional<Text>` (sección 5);
`retentionDeadline` es `Optional<Timestamp>` — no todo dato tiene, necesariamente, una política de
retención explícita todavía modelada; `legalHold` es el `Boolean` que, junto con `enforceRetention`
(seccion 11), suspende cualquier borrado programado; `classifiedAt` registra cuándo se produjo esta
etiqueta.

**Por qué un único `subjectRef: Text` opaco, y no un campo por cada tipo de dato posible.** Mismo
argumento, ya establecido, que motivó `AuditRecord.subjectRef` (CH-19) y `ControlDirective.targetRef`
(CH-18): un `DataGovernanceLabel` dado tendría, siempre, todos esos campos `NULL` salvo uno, y cada
nuevo tipo de dato que un capítulo futuro produjera obligaría a reabrir el `STRUCT`. `subjectRef`
opaco, con su significado determinado por quién invoca `classifyData` (seccion 11), es genérico por
diseño — el propio punto de este capítulo es que `DataGovernanceEngine` nunca necesita saber, para
clasificar, de qué tipo exacto de dato se trata.

**Por qué `DataGovernanceLabel` no incluye un campo `actor: ActorId`, a diferencia de `AuditRecord`
(CH-19) o `ControlDirective` (CH-18).** Se evaluó explícitamente agregarlo, siguiendo el precedente de
`INV-19`. Se descartó: `AuditRecord` existe, específicamente, para probar QUIÉN decidió QUÉ en un
instante dado — el actor es parte permanente de esa evidencia. `DataGovernanceLabel`, en cambio,
describe una propiedad del DATO mismo (cuán sensible es, dónde debe residir), independientemente de
quién ejecutó la clasificación — la misma distinción, aplicada a datos en vez de a decisiones, que
`P-22` traza frente a `P-13`. Quién invocó `classifyData`, cuándo existe un `ExecutionContext` real,
sigue siendo trazable a través del `traceId`/`agentId` que el `AgentEvent` condicional ya transporta
(seccion 14) — sin que el propio `DataGovernanceLabel` necesite cargar esa información de forma
permanente.

**Por qué `DataGovernanceLabel` no tiene ningún campo de estado — y por qué esa ausencia significa
algo distinto que en `AuditRecord` (CH-19).** Ver seccion 12 para el desarrollo completo: la ausencia
de un campo de estado en `AuditRecord` existe para hacer *imposible* una segunda escritura sobre el
mismo registro (`P-25`). La ausencia de un campo de estado aquí existe por una razón distinta:
`DataGovernanceLabel` representa la clasificación *vigente* para un `subjectRef`, válida hasta que una
invocación posterior de `classifyData` produzca una etiqueta nueva — el cambio se modela por
**reemplazo** (una nueva instancia, un nuevo `id`), nunca por mutación de la instancia anterior.

**Unchanged / Not yet introduced**: `ContextBlock` (embebido en C-005, CH-04) y `ToolResult` (C-009,
CH-02) no cambian de forma — ninguno de los dos gana un campo `governanceLabel` en este capítulo (ver
seccion 9/18). `CredentialReference` (C-026, CH-16) tampoco cambia: `CredentialClassification` sigue
siendo, sin excepción, el esquema de gobierno exclusivo de un secreto ya resuelto. Ningún `STRUCT`
para representar el grafo completo de lineage, ni ningún registro de "cuál es la etiqueta vigente
actual para este `subjectRef`" (ver seccion 18).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce un contrato de
datos, registrado en `registry/contracts.yaml`:

```text
ID:                     C-030
Name:                   DataGovernanceLabel
Version:                v1
Introduced In:          CH-20
Current Definition:     STRUCT DataGovernanceLabel (ver §6)
Used By:                [CMP-018]
Modified By:            []
Constitutional Impact:  [P-22, INV-E11, INV-19]
```

`C-030` es el decimoséptimo id que este libro asigna sin que estuviera reservado desde CH-01 §7 — el
correlativo simplemente continúa después de `C-029` (CH-19). No colisiona, por nombre, con ningún
contrato ya registrado — verificado con grep completo sobre `registry/contracts.yaml` antes de
escribir este capítulo.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el séptimo componente del registry que no corresponde a ninguno de los once
nombres del árbol de Article III ("Agent Runtime") — pertenece, en cambio, al "Data & Context Plane"
de Amendment v1.1:

```pseudocode
COMPONENT DataGovernanceEngine
    consumes: ExecutionContext
    produces: DataGovernanceLabel, AgentEvent, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Amendment v1.1 (`P-22`/`INV-E11`) — Article III no tiene,
todavía, una sección propia para este componente, exactamente igual que `AdmissionController`
(CH-14), `AgentCommunicationGateway` (CH-15), `CredentialBroker` (CH-16), `IdempotencyGuard` (CH-17),
`OperationalController` (CH-18) y `AuditLedger` (CH-19):

```text
COMPONENT: DataGovernanceEngine

Responsibility:
    Clasificar cualquier dato que fluye por el sistema (un ContextBlock ya seleccionado, un
    ToolResult ya producido, o cualquier otro dato futuro) con un nivel de sensibilidad, un
    requisito de residencia, una fecha límite de retención, una bandera de legal-hold y una
    referencia de lineage — produciendo una etiqueta de gobernanza portátil que viaja junto con el
    dato a través de fronteras de componentes, de forma completamente independiente de si el
    modelo entiende o acepta esos requisitos — sin decidir si ese dato es relevante para el turno
    actual, sin decidir si puede verse en absoluto, sin reclasificar un secreto ya clasificado por
    CredentialBroker y sin producir evidencia de auditoría inmutable.

Consumes:
    C-004 ExecutionContext (solo cuando la clasificación ocurre dentro de uno real, ver seccion
    11)

Depends on:
    (ninguno todavía — el cableado real hacia ContextEngine/ToolRuntime para que cada uno invoque
    de verdad classifyData sobre su propio material producido es Preview, no introducido en este
    capítulo; ver seccion 9)

Produces:
    C-030 DataGovernanceLabel (la etiqueta de gobernanza en sí), C-010 AgentEvent (DATA_CLASSIFIED
    / RETENTION_ENFORCEMENT_EVALUATED, solo cuando existe un ExecutionContext y un AgentId reales,
    ver seccion 14), C-011 HarnessError

Owns (Amendment v1.1 `P-22`/`INV-E11`, cita y lectura literal):
    - "Classification, residency, retention, lineage, encryption, deletion and legal-hold
      requirements MUST be enforceable independently of model reasoning" (cita literal, P-22) —
      clasificar, en exclusiva, cualquier dato que fluya por el sistema con esos requisitos,
      resuelta por completo fuera del razonamiento del modelo
    - "Data governance policy follows context and artifacts across component boundaries" (cita
      literal, INV-E11) — producir una etiqueta portátil (DataGovernanceLabel), referenciada por
      subjectRef, consultable desde cualquier componente sin reabrir el dato original
    - decidir, para un plazo de retención dado, si el borrado ya es exigible, sigue sin serlo, o
      está suspendido por una preservación legal — sin borrar ni reemplazar nunca la fecha de
      retención original al aplicar esa suspensión
    - rechazar por defecto (fail-closed), hacia el nivel de clasificación más conservador
      (RESTRICTED), cualquier dato sin regla de gobernanza conocida
    - rechazar por defecto un DataGovernanceLabel sin referencia de sujeto o sin procedencia

Does NOT own:
    - seleccionar, rankear o componer qué contexto es relevante para que el modelo razone sobre un
      turno (ContextEngine, CMP-004, ya introducido en CH-04 — la frontera más importante de este
      capítulo: ContextEngine decide QUÉ material entra dentro de un presupuesto; DataGovernanceEngine
      decide QUÉ REQUISITOS de gobierno aplican a lo que ya se decidió incluir)
    - autorizar si un dato puede verse en absoluto (PolicyEngine, CMP-005, ya introducido en CH-05
      — distinta pregunta, distinto dominio: "¿cuán sensible es esto?" nunca es "¿puede verse esto
      en absoluto?")
    - reclasificar un secreto que CredentialBroker ya clasificó con CredentialClassification
      (CredentialBroker, CMP-014, ya introducido en CH-16 — esquema narrow de dos valores, exclusivo
      de credenciales; DataGovernanceEngine generaliza P-22 a cualquier OTRO dato, sin tocar el
      contrato de CH-16)
    - producir evidencia de auditoría estructuralmente inmutable sobre una clasificación ya
      producida (AuditLedger, CMP-017, ya introducido en CH-19 — un DataGovernanceLabel describe la
      clasificación vigente hoy, no evidencia permanente de que ocurrió; ver seccion 15)
    - aislar operacionalmente los runs de un tenant (OperationalController, CMP-016, ya introducido
      en CH-18 — aislamiento operacional es una decisión distinta de clasificar un dato, aunque
      ambas toquen, en espíritu, "quién puede ver qué")
    - ejecutar el borrado real, el cifrado real, o el mecanismo real que mueve o almacena un dato
      físicamente dentro de una región concreta (Preview, infraestructura de borde — este
      componente decide QUÉ requisitos aplican y SI un borrado ya es exigible, nunca CÓMO se
      ejecuta físicamente)
    - generar por sí mismo el subjectRef, la procedencia o la bandera de legal-hold — todas llegan
      como señales de entrada ya resueltas (mismo patrón que targetRef en CH-18 o subjectRef en
      CH-19)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con la misma
particularidad que `AdmissionController`/`AgentCommunicationGateway`/`CredentialBroker`/
`IdempotencyGuard`/`OperationalController`/`AuditLedger`: ninguna de las seis exclusiones proviene de
una ficha propia de Article III (que no existe para este componente); provienen de fronteras ya
establecidas por componentes ya registrados. La primera exclusión de esta lista es, deliberadamente,
la más parecida en prosa informal a lo que este componente sí posee — el mismo cuidado editorial que
CH-04 §8 ya aplicó frente a `PolicyEngine`, y que CH-19 §8 ya aplicó frente a `EventBus`.

**Nota sobre Article IV.** A diferencia de `EventBus` (CH-09) y `AuditLedger` (CH-19), que no tienen
fila propia porque "distribuir" y "registrar" no son decidir, `DataGovernanceEngine` sí decide algo
real — qué requisitos de gobierno aplican a un dato, y si un borrado ya es exigible — igual que
`ContextEngine` (¿qué es relevante?) o `PolicyEngine` (¿está permitido?). Es, en ese sentido, más
parecido a `PolicyEngine` que a `EventBus`: un componente que responde una pregunta real de dominio
propio, no uno que solo preserva o distribuye una respuesta ajena.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
DataGovernanceEngine
    consumes → ExecutionContext
    produces → DataGovernanceLabel, AgentEvent, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`DataGovernanceEngine` no depende hoy de ningún otro componente registrado — mismo patrón que
CH-01..CH-19 ya establecieron para sus propios componentes. En prosa (nunca dentro de un bloque
`pseudocode`, per `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las relaciones
futuras que un capítulo de integración agregaría son:

| Componente futuro (relación inversa — no cableada en este capítulo) | Qué relación tendría con `DataGovernanceEngine` |
|---|---|
| `ContextEngine` (ya existente, CMP-004) | `assembleContextSnapshot` (CH-04 §11) invocaría, tras construir cada `ContextBlock`, `classifyData` sobre su `provenance` — el cableado exacto que este capítulo deja explícitamente para un capítulo de integración futuro, sin tocar una sola línea de CH-04 |
| `ToolRuntime` (ya existente, CMP-002) | `executeToolCall` (CH-02 §11) invocaría `classifyData` sobre el `output` de cada `ToolResult` producido |
| `CredentialBroker` (ya existente, CMP-014) | permanecería sin relación con `DataGovernanceEngine`: `CredentialClassification` sigue siendo, sin excepción, el esquema de gobierno propio de un secreto — la frontera se mantiene, no se cablea |
| `AuditLedger` (ya existente, CMP-017) | podría auditar, con `recordAuditEntry` (CH-19 §11), el hecho de que una clasificación concreta ocurrió — usando el `id` de un `DataGovernanceLabel` como `subjectRef` — sin que eso convierta a `DataGovernanceLabel` mismo en evidencia inmutable (ver seccion 15) |
| `EventBus` (ya existente, CMP-009) | podría distribuir, como un `AgentEvent` más, `DATA_CLASSIFIED`/`RETENTION_ENFORCEMENT_EVALUATED` (seccion 14) — exactamente igual que distribuye el de cualquier otro productor |

`registry/components.yaml` de `CMP-002`, `CMP-004`, `CMP-009`, `CMP-014`, `CMP-017` **no se modifica**
en este capítulo: ninguno agrega `CMP-018` a sus `dependencies`, y ninguno cambia su pseudocódigo. El
pseudocódigo de la seccion 11 muestra a `DataGovernanceEngine` clasificando, de forma completamente
autónoma, un `ContextBlock` de ejemplo con la forma exacta que `ContextEngine` (CH-04) ya produce —
sin que ese componente cambie una sola línea para que este capítulo sea correcto. Ese cableado real de
punta a punta es, explícitamente, trabajo de un capítulo de integración futuro (ver seccion 18/19).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[ContextEngine — produce un ContextBlock ya seleccionado, CH-04, conceptual] → DataGovernanceEngine
→ [DataGovernanceLabel — la etiqueta vigente, consultable por cualquier componente futuro vía
subjectRef]
```

**Vista 2 — Sequence**

```text
ContextBlock (provenance = "conversation_history", ya seleccionado y ya autorizado)
   │ (ya producido por ContextEngine.assembleContextSnapshot, CH-04 — conceptual, sin cambios)
   ▼
DataGovernanceEngine
   │ classifyData(subjectRef, provenance, legalHold, execution, agentId)
   │ ¿subjectRef vacío? sí → HarnessError (DATA_GOVERNANCE_LABEL_MISSING_SUBJECT_REF)
   │ ¿provenance vacío? sí → HarnessError (DATA_GOVERNANCE_LABEL_MISSING_PROVENANCE)
   │ ¿existe una regla de gobernanza para esta procedencia? no → classification = RESTRICTED
   │     (fail-closed) sí → aplica classification/residencyRequirement/retentionDeadline/
   │     lineageRef de la regla encontrada
   │ construye DataGovernanceLabel (id, subjectRef, classification, residencyRequirement,
   │   retentionDeadline, legalHold, lineageRef, classifiedAt)
   │ ¿execution y agentId ambos resueltos? sí → emite: AgentEvent (DATA_CLASSIFIED)
   ▼
DataGovernanceLabel (la etiqueta vigente para este subjectRef)
   │
   │ ... más tarde, en cualquier instante ...
   ▼
DataGovernanceEngine
   │ enforceRetention(label, evaluatedAt, execution, agentId)
   │ ¿label.legalHold? sí → outcome = SUSPENDED_BY_LEGAL_HOLD (retentionDeadline permanece intacto)
   │ ¿retentionDeadline == NULL? sí → outcome = NOT_YET_DUE
   │ ¿evaluatedAt >= retentionDeadline? sí → outcome = DELETION_DUE   no → outcome = NOT_YET_DUE
   │ ¿execution y agentId ambos resueltos? sí → emite: AgentEvent (RETENTION_ENFORCEMENT_EVALUATED)
   ▼
RetentionEnforcementResult (outcome ya decidido — el borrado real, si DELETION_DUE, es Preview)
   │
   │ ... integración futura: ContextEngine (CH-04) y ToolRuntime (CH-02) invocarían classifyData
   │     de verdad sobre su propio material producido; AuditLedger (CH-19) podría auditar el hecho
   │     de que una clasificación concreta ocurrió ...
```

**Vista 3 — Pseudocódigo**

Ver §11: `classifyData`/`enforceRetention` son la primera formalización ejecutable de "el harness
gobierna cualquier dato con requisitos exigibles de forma independiente del razonamiento del modelo"
(`P-22`/`INV-E11`) — construidas exclusivamente a partir de material que ya existe
(`ExecutionContext`/`AgentEvent`/`HarnessError` desde CH-00, `ContextBlock` desde CH-04) más el
contrato y los `ENUM`/`STRUCT` nuevos de este capítulo.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde
CH-00/CH-04.

```pseudocode
FUNCTION classifyData(
    subjectRef: Text,
    provenance: Text,
    legalHold: Boolean,
    execution: Optional<ExecutionContext>,
    agentId: Optional<AgentId>
) -> DataGovernanceLabel

    IF subjectRef == ""
        missingSubject: HarnessError = HarnessError(
            category = GOVERNANCE,
            code = "DATA_GOVERNANCE_LABEL_MISSING_SUBJECT_REF",
            message = "classifyData fue invocada sin una referencia al dato que se clasifica — un DataGovernanceLabel nunca puede escribirse sin saber qué dato representa",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW missingSubject
    END

    IF provenance == ""
        missingProvenance: HarnessError = HarnessError(
            category = GOVERNANCE,
            code = "DATA_GOVERNANCE_LABEL_MISSING_PROVENANCE",
            message = "classifyData fue invocada sin procedencia — sin saber de dónde vino el dato, ninguna regla de gobernanza puede aplicarse de forma determinística",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW missingProvenance
    END

    classification: DataClassificationLevel = RESTRICTED
    residencyRequirement: Optional<Text> = NULL
    retentionDeadline: Optional<Timestamp> = NULL
    lineageRef: Optional<Text> = NULL

    ruleFound: Boolean = dataGovernanceRuleFound(provenance)

    IF ruleFound
        matchedRuleId: Text = matchDataGovernanceRule(provenance)
        classification = dataGovernanceRuleClassification(matchedRuleId)
        residencyRequirement = dataGovernanceRuleResidency(matchedRuleId)
        retentionDeadline = dataGovernanceRuleRetentionDeadline(matchedRuleId)
        lineageRef = dataGovernanceRuleLineage(matchedRuleId, subjectRef)
    END
    // ningún ruleFound == FALSE deja classification en su valor por defecto, RESTRICTED —
    // fail-closed: un dato sin regla de gobernanza conocida se gobierna como el más sensible
    // posible, nunca como el menos sensible.

    label: DataGovernanceLabel = DataGovernanceLabel(
        id = newDataGovernanceLabelId(),
        subjectRef = subjectRef,
        classification = classification,
        residencyRequirement = residencyRequirement,
        retentionDeadline = retentionDeadline,
        legalHold = legalHold,
        lineageRef = lineageRef,
        classifiedAt = now()
    )

    IF execution != NULL AND agentId != NULL
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = DATA_CLASSIFIED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = label
        )
    END

    RETURN label
END
```

`now()`, `newEventId()` son las mismas primitivas de CH-00..CH-19. `newDataGovernanceLabelId()` sigue
el mismo patrón que `newAuditRecordId()` (CH-19) o `newControlDirectiveId()` (CH-18).
`dataGovernanceRuleFound(...)`, `matchDataGovernanceRule(...)`, `dataGovernanceRuleClassification(...)`,
`dataGovernanceRuleResidency(...)`, `dataGovernanceRuleRetentionDeadline(...)` y
`dataGovernanceRuleLineage(...)` son primitivas nuevas de este capítulo, en el mismo espíritu que
`policyRuleFound`/`matchPolicyRule`/`policyRuleAllows`/`policyRuleRequiresApproval` (CH-05 §11): un
motor de reglas de gobernanza ya asumido y determinístico, cuya implementación real (un catálogo de
reglas por procedencia, un motor de políticas de datos empresarial) es Preview, infraestructura de
borde — este capítulo modela la forma de la decisión (fail-closed cuando no hay regla), no el
lenguaje de reglas en sí.

**Por qué `classifyData` deniega hacia `RESTRICTED` cuando ninguna regla aplica, en vez de hacia
`PUBLIC`.** Mismo argumento fail-closed que `evaluatePolicyForToolCall` (CH-05 §11) ya aplicó al
denegar por defecto cuando ninguna policy rule aplica: un dato sin regla de gobernanza conocida
podría, en la práctica, ser cualquier cosa — incluyendo el dato más sensible que el sistema mueve.
Clasificarlo por defecto hacia el nivel menos conservador (`PUBLIC`) trataría la ausencia de
información como evidencia de seguridad, exactamente lo opuesto de lo que `P-22` exige. `RESTRICTED`
por defecto es la única elección consistente con "gobernar de forma independiente del razonamiento" —
nadie, ni el modelo ni una regla ausente, puede degradar accidentalmente la protección de un dato no
reconocido.

Ahora, con `ContextEngine` (CMP-004, CH-04) ya existente, se puede mostrar el ejemplo que motiva este
capítulo: clasificar un `ContextBlock` real, exactamente como `assembleContextSnapshot` (CH-04 §11)
ya lo construye dentro de un `ContextSnapshot`:

```pseudocode
FUNCTION demonstrateClassifyingAContextBlock(
    block: ContextBlock,
    subjectRef: Text,
    legalHold: Boolean,
    execution: Optional<ExecutionContext>,
    agentId: Optional<AgentId>
) -> DataGovernanceLabel

    RETURN classifyData(subjectRef, block.provenance, legalHold, execution, agentId)
END
```

`demonstrateClassifyingAContextBlock` es una demostración de integración, no una tercera
responsabilidad nueva — mismo patrón que `demonstrateAuditingADeniedPolicyDecision` (CH-19 §11): no
modifica `CMP-004 ContextEngine`, ni su ficha, ni la firma de `assembleContextSnapshot` (CH-04 §11),
que sigue devolviendo exactamente lo mismo que devolvía antes de este capítulo. Nótese,
deliberadamente, que `classifyData` recibe `block.provenance` — un campo real que ya existe desde
CH-04 — pero **nunca recibe `block.content`**: la clasificación de este capítulo depende de dónde
vino el fragmento, nunca de inspeccionar su contenido real, el mismo cuidado que separa "clasificar
por procedencia" de "leer el dato para decidir cuán sensible es" — esta última, una capacidad que
`DataGovernanceEngine` deliberadamente no ejerce (ver seccion 18).

`subjectRef`, en la práctica, sería la referencia opaca que correlaciona con este `ContextBlock`
específico dentro de su `ContextSnapshot` (p. ej. su posición más un identificador de sesión, ya
resuelto por quien invoca ambas funciones) — su resolución exacta, igual que `targetRef` en
`ControlDirective` (CH-18 §18) o `subjectRef` en `AuditRecord` (CH-19 §18), es una señal de entrada
asumida, no construida por este capítulo.

Con la etiqueta ya producida, este capítulo formaliza la segunda mitad de `P-22`: decidir si un
borrado programado ya es exigible.

```pseudocode
STRUCT RetentionEnforcementResult
    label: DataGovernanceLabel
    outcome: RetentionEnforcementOutcome
    evaluatedAt: Timestamp
END

FUNCTION enforceRetention(
    label: DataGovernanceLabel,
    evaluatedAt: Timestamp,
    execution: Optional<ExecutionContext>,
    agentId: Optional<AgentId>
) -> RetentionEnforcementResult

    outcome: RetentionEnforcementOutcome = NOT_YET_DUE

    IF label.legalHold
        outcome = SUSPENDED_BY_LEGAL_HOLD
    ELSE IF label.retentionDeadline != NULL AND evaluatedAt >= label.retentionDeadline
        outcome = DELETION_DUE
    END
    // legalHold se evalúa PRIMERO, antes de siquiera mirar retentionDeadline — y en ningún camino
    // de esta función se borra, reemplaza o recalcula label.retentionDeadline: la preservación
    // legal suspende el EFECTO del plazo, nunca el plazo mismo.

    result: RetentionEnforcementResult = RetentionEnforcementResult(
        label = label,
        outcome = outcome,
        evaluatedAt = evaluatedAt
    )

    IF execution != NULL AND agentId != NULL
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = RETENTION_ENFORCEMENT_EVALUATED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = result
        )
    END

    RETURN result
END
```

**Por qué `legalHold` se evalúa antes que `retentionDeadline`, y no al revés.** Si el orden se
invirtiera — comprobar primero si el plazo ya se cumplió, y solo entonces mirar `legalHold` — el
resultado final sería el mismo (`SUSPENDED_BY_LEGAL_HOLD` cuando ambas condiciones se cumplen), pero
la intención del código sería ambigua: parecería que la preservación legal es una excepción que se
consulta *después* de determinar que el borrado ya era exigible, en vez de una precedencia real que
gobierna la decisión completa desde el principio. Evaluar `legalHold` primero dice, con la propia
estructura del código, lo que `P-22` exige en espíritu: ninguna fecha de retención, por vencida que
esté, tiene autoridad sobre una preservación legal activa.

**Por qué `enforceRetention` nunca borra ni reemplaza `label.retentionDeadline`.** Se evaluó
explícitamente una variante donde, al activarse `legalHold`, `retentionDeadline` se pusiera en `NULL`
— más simple de razonar en el momento. Se descartó: si la preservación legal se libera después, la
única forma de saber si el borrado ya debía haber ocurrido *antes* de que la preservación empezara es
que `retentionDeadline` siga siendo el valor original, intacto. Borrarlo destruiría, precisamente, la
información que hace falta consultar una vez que `legalHold` vuelva a `FALSE` — el mismo tipo de
pérdida irreversible que `P-25` (CH-19) existe para prevenir en otro contrato, ahora evitada aquí por
la forma en que se ordena la lógica, no por un mecanismo de inmutabilidad estructural.

**Por qué `classifyData`/`enforceRetention` reciben `execution`/`agentId` como `Optional`.** Mismo
argumento que `recordAuditEntry` (CH-19 §11) y `applyControlDirective` (CH-18 §11): no toda
clasificación ni toda evaluación de retención ocurre dentro de un `AgentRun` ya arrancado — un
proceso periódico que evalúa retención sobre etiquetas ya producidas, por ejemplo, podría ejecutarse
fuera de cualquier turno concreto. Exigir un `ExecutionContext`/`AgentId` obligatorios habría forzado
a fabricar valores centinela para ese caso, exactamente el tipo de dato inventado que este libro
evita.

Nótese lo que ninguna de las dos funciones **nunca hace**: `classifyData` no invoca
`ContextEngine.assembleContextSnapshot` (CH-04) para decidir relevancia — la selección ya ocurrió,
en otro lugar, antes de que este componente exista en la secuencia; ninguna de las dos invoca
`EventBus.distributeEvent` (CH-09) para propagar su resultado — el `AgentEvent` que cada una emite
es, como mucho, una notificación, nunca el vehículo del resultado mismo; y `enforceRetention` nunca
ejecuta ningún borrado real — solo decide si sería exigible, dejando la ejecución física del borrado,
deliberadamente, fuera de este capítulo (seccion 18).

## 12. Transiciones de Estado (State Transitions)

Este capítulo no modifica `AgentRunStatus` (C-013): sigue siendo, sin cambios, el mismo `ENUM` de
once estados que `AgentLoop` (CH-01) formalizó.

`DataGovernanceLabel`, igual que `AuditRecord` (C-029, CH-19), no declara ningún `ENUM` de lifecycle
propio — pero, a diferencia de `AuditRecord`, por una razón distinta:

```text
(DataGovernanceLabel recién producido para un subjectRef)
   → classifyData(...)
     RETURN DataGovernanceLabel — vigente para ese subjectRef hasta que una invocación posterior
     de classifyData produzca uno nuevo

(el mismo subjectRef necesita una clasificación distinta más tarde — p. ej. una regla de
gobernanza cambió, o se detectó información adicional sobre el dato)
   → classifyData(...) se invoca de nuevo, con el mismo subjectRef
     RETURN un DataGovernanceLabel COMPLETAMENTE NUEVO (id distinto, classifiedAt posterior) — el
     anterior nunca se edita ni se reemplaza in place; simplemente deja de ser el más reciente

(evaluar si un borrado ya es exigible sobre una etiqueta ya producida)
   → enforceRetention(label, ...)
     RETURN RetentionEnforcementResult — nunca modifica label; label.retentionDeadline permanece
     exactamente igual antes y después de esta llamada, sin importar el outcome
```

**Por qué la ausencia de un campo de estado aquí significa algo distinto que en `AuditRecord`
(CH-19) — la distinción más importante de esta sección.** `AuditRecord` (CH-19 §12) no tiene ningún
campo de estado porque introducir uno abriría, por la sola forma del `STRUCT`, la posibilidad
conceptual de una segunda escritura sobre el mismo registro — exactamente lo que `P-25` prohíbe:
`AuditRecord` representa un hecho ya completamente ocurrido, sin ninguna "primera mitad" pendiente.
`DataGovernanceLabel`, en cambio, sí puede quedar obsoleto — una preservación legal puede activarse o
liberarse, una regla de gobernanza puede cambiar — pero ese cambio nunca se modela como una
transición interna del mismo `STRUCT` (que exigiría un campo de estado como `ACTIVE`/`SUPERSEDED`):
se modela por **reemplazo completo**, produciendo una nueva instancia con un nuevo `id`. La ausencia
de un campo de estado, en ambos contratos, es deliberada — pero en `AuditRecord` existe para hacer
imposible una segunda escritura, y aquí existe porque el mecanismo de cambio ya es, por diseño,
"produce uno nuevo", nunca "edita el existente".

**Lo que este capítulo explícitamente no cierra**: ningún mecanismo registra, todavía, cuál
`DataGovernanceLabel` es "el vigente" para un `subjectRef` dado cuando existen varios producidos en
momentos distintos — ver seccion 18.

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6, extendido en la seccion 6 de este capítulo) clasifica también
los dos fallos reales que introduce este capítulo:

```text
GOVERNANCE
    DATA_GOVERNANCE_LABEL_MISSING_SUBJECT_REF  — classifyData fue invocada sin una referencia al
                                                   dato que se clasifica
        → recoverable: FALSE, retryable: FALSE
    DATA_GOVERNANCE_LABEL_MISSING_PROVENANCE   — classifyData fue invocada sin procedencia — sin
                                                   ella, ninguna regla de gobernanza puede aplicarse
                                                   de forma determinística
        → recoverable: FALSE, retryable: FALSE
```

Los dos fallos son `recoverable = FALSE` y `retryable = FALSE`: ambos representan un uso incorrecto
de la propia invocación a `classifyData` (una referencia de sujeto faltante, o una procedencia
faltante) — ninguno se corrige reintentando la misma operación tal cual, sino corrigiendo lo que se
le provee.

**La distinción más importante de esta sección**: ninguno de los dos fallos se clasifica como
`CONTEXT` (CH-04) ni como `CREDENTIAL` (CH-16) — aunque, estructuralmente, ambos son "un campo
requerido llegó vacío", el mismo tipo de fallo que otros capítulos ya clasificaron bajo su propia
categoría. La diferencia no es la forma del fallo, es su dominio: gobernar un dato tiene un propósito
constitucional propio (`P-22`) distinto de seleccionar contexto relevante (`P-14`, CH-04) o resolver
un secreto específico (`INV-E08`, CH-16) — reutilizar cualquier categoría ya existente habría sido,
en espíritu, la misma conflación de dominios que motiva todo este capítulo, ahora replicada a nivel
de `ErrorCategory` — el mismo argumento que ya usaron CH-16 §13 (contra `VALIDATION`), CH-17 §13
(contra `VALIDATION`/`BUDGET`), CH-18 §13 (contra `CANCELLATION`) y CH-19 §13 (contra `CONTROL`/
`VALIDATION`).

**`enforceRetention` deliberadamente nunca falla.** A diferencia de `classifyData`, `enforceRetention`
es una función total sobre cualquier `DataGovernanceLabel` ya válido: no existe ninguna combinación
de `legalHold`/`retentionDeadline` que la haga lanzar un `HarnessError` — siempre produce uno de los
tres valores de `RetentionEnforcementOutcome`. Esto es deliberado: evaluar si un borrado es exigible
es, por naturaleza, una pregunta que siempre tiene una respuesta válida, incluso cuando la respuesta
es "todavía no" o "suspendido".

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo de `category = INFRASTRUCTURE`
que pudiera ocurrir en el motor real de reglas de gobernanza asumido por `dataGovernanceRuleFound`/
`matchDataGovernanceRule`, o en el mecanismo real que ejecuta físicamente un borrado, un cifrado o un
movimiento de datos entre regiones — ese valor de `ErrorCategory` sigue, después de este capítulo,
sin que ningún componente real lo haya ejercitado nunca (mismo límite que CH-14..CH-19 ya
documentaron para sus propias primitivas asumidas).

## 14. Eventos Producidos (Events Produced)

`DataGovernanceEngine` es el primer componente de este libro que emite `AgentEvent` de forma
condicional desde **dos funciones distintas**, cada una con su propio tipo de evento — agrega
`DATA_CLASSIFIED` y `RETENTION_ENFORCEMENT_EVALUATED` a `AgentEventType` (seccion 6), emitidos
únicamente cuando `execution` y `agentId` llegan ambos resueltos (mismo patrón condicional que
`AuditLedger`, CH-19, y `OperationalController`, CH-18).

**Por qué son dos eventos, y no uno solo compartido.** `classifyData` y `enforceRetention` responden
preguntas distintas sobre datos distintos (una etiqueta recién producida; el resultado de evaluar una
etiqueta ya existente) — colapsarlas en un único tipo de evento habría obligado a un consumidor de
`EventBus` a inspeccionar el `payload` para saber cuál de las dos operaciones ocurrió, en vez de
poder filtrar por `eventType` directamente. Mismo criterio que ya separó `TOOL_CALL_COMPLETED` de
`TOOL_CALL_FAILED` (CH-02) en vez de un único `TOOL_CALL_FINISHED` con un campo de éxito.

**Por qué la emisión es condicional, en ambos casos.** Mismo argumento que `AuditLedger` (CH-19 §14)
y `OperationalController` (CH-18 §14): un `AgentEvent` (C-010) exige `runId`/`sessionId`/`agentId`/
`traceId` genuinos, y no toda clasificación ni toda evaluación de retención ocurre dentro de un
`AgentRun` con esos cuatro campos ya resueltos.

**Por qué, incluso cuando emiten, ninguno de los dos `AgentEvent` es evidencia de auditoría —
frontera explícita con `AuditLedger` (CH-19).** `payload = label` (en `DATA_CLASSIFIED`) o
`payload = result` (en `RETENTION_ENFORCEMENT_EVALUATED`) transportan una copia del resultado ya
producido — pero, exactamente igual que el `AUDIT_RECORD_CREATED` de `AuditLedger` (CH-19 §14),
quedan sujetos a las mismas garantías (o ausencia de garantías) que cualquier otro `AgentEvent`:
`EventBus` podría distribuirlos, perderlos si nadie está suscrito, o nunca llegar a existir si
`execution`/`agentId` no estaban resueltos. Si alguien necesitara, en cambio, evidencia
estructuralmente inmutable de que una clasificación concreta ocurrió, esa es, sin ambigüedad, una
responsabilidad de `AuditLedger` (CH-19) — nunca de estos dos eventos condicionales (ver seccion 15).

**Por qué esto no es una limitación real hacia `INV-18`.** La acción verdaderamente significativa de
este capítulo — producir una etiqueta de gobernanza vigente, o decidir si un borrado ya es exigible —
ya se cumple con el `RETURN` directo de `classifyData`/`enforceRetention` a quien las invoca, sin
depender de `AgentEvent`/`EventBus` para "existir". El `AgentEvent` condicional es, aquí, una
conveniencia de observabilidad adicional, nunca el mecanismo que hace el resultado real.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

`DataGovernanceEngine` es el primer componente de este libro cuya responsabilidad completa es
clasificar el dato mismo, de forma independiente de si es relevante o si está autorizado para verse.

**La distinción con `ContextEngine` (CH-04), explícita, completa y la más importante de este
capítulo.** `ContextEngine.assembleContextSnapshot` (CH-04) decide, dentro de un presupuesto
explícito, qué material candidato es relevante para razonar sobre el turno actual — una pregunta de
P-14 ("Context should be selected, not dumped"). `DataGovernanceEngine.classifyData` (este capítulo)
decide, sobre material que YA fue seleccionado como relevante (y ya autorizado a verse, per
`PolicyEngine`), qué requisitos de gobierno le aplican — una pregunta de `P-22`, completamente
ortogonal a la relevancia. Las dos preguntas son, literalmente, independientes: un `ContextBlock`
puede ser perfectamente relevante y, al mismo tiempo, `RESTRICTED` con una fecha de retención
estricta; y, a la inversa, un dato `PUBLIC` sin ningún requisito especial puede resultar completamente
irrelevante para el turno actual. Si `ContextEngine` fusionara ambas preguntas —ya que de todos modos
está "mirando" el mismo `content` para decidir relevancia—, la gobernanza de datos dejaría de ser una
capa determinística explícita y pasaría a depender de que la lógica de selección "también" clasifique
correctamente — exactamente el patrón que Article IV existe para prevenir, el mismo argumento que
CH-04 §15 ya aplicó, con matices distintos, a la frontera contra `PolicyEngine`.

**La distinción con `CredentialBroker` (CH-16), precisa y necesaria.** `CredentialBroker.
resolveCredentialReference` (CH-16) ya aplica un `CredentialClassification` de dos valores
exclusivamente sobre un secreto ya resuelto — y ese esquema, deliberadamente estrecho, sigue siendo,
sin excepción, el dueño de la gobernanza de un secreto específico. `DataGovernanceEngine` no
reclasifica jamás una `CredentialReference` ya clasificada: generaliza la misma exigencia
constitucional (`P-22`) al resto del universo de datos que un secreto nunca cubrió — un
`ContextBlock`, un `ToolResult`. Confundir esta frontera llevaría a que dos componentes distintos
pudieran producir, sobre el mismo secreto, dos clasificaciones potencialmente contradictorias — el
mismo riesgo de "decisión absorbida por un dominio vecino" que Article IV existe para prevenir.

**La distinción con `AuditLedger` (CH-19), heredada y aplicada aquí con una particularidad nueva.**
`AuditLedger.recordAuditEntry` (CH-19) produce evidencia estructuralmente inmutable de que una
decisión crítica YA OCURRIÓ — nunca editable ni reemplazable después de escrita. `DataGovernanceLabel`
(este capítulo) describe, en cambio, la clasificación VIGENTE HOY para un dato — que puede quedar
obsoleta en cuanto una invocación posterior de `classifyData` produzca una etiqueta nueva para el
mismo `subjectRef`. Si alguien necesitara, además, preservar evidencia inmutable de que una
clasificación concreta ocurrió en un instante dado (para sobrevivir una disputa o auditoría), esa
seguiría siendo, sin ambigüedad, responsabilidad de `AuditLedger` — auditando el `id` de un
`DataGovernanceLabel` como `subjectRef`, exactamente como auditaría cualquier otra decisión — nunca
una responsabilidad que `DataGovernanceLabel` asuma por sí mismo.

**`P-13`, extendido a los datos con la misma disciplina que todo el libro.** `classifyData` y
`enforceRetention` no reciben ninguna entrada que el modelo haya producido — ni siquiera de forma
indirecta. El modelo no decide la clasificación de un dato, no puede activar ni liberar una
preservación legal, y no puede, bajo ninguna circunstancia, alterar un `DataGovernanceLabel` ya
producido — la ausencia total del modelo en el pseudocódigo de este capítulo es, otra vez, la
materialización directa del mismo argumento que `P-13` ya estableció para la autorización de
acciones, ahora aplicado, por primera vez con código real, a los datos.

**Límite que este capítulo deja explícitamente abierto.** Ni `classifyData` ni `enforceRetention`
modelan ningún control de acceso sobre **quién** puede invocarlas, ni sobre **quién**, después, puede
leer un `DataGovernanceLabel` ya producido — cualquier llamador puede, en este capítulo, producir una
etiqueta para cualquier `subjectRef`, o consultar la etiqueta de cualquier otro. Autorizar la
escritura y la lectura de etiquetas de gobernanza (una pregunta con implicaciones reales: no todo
actor debería poder ver la clasificación completa de todo dato de todo tenant, `INV-E07`) queda,
explícitamente, fuera de alcance de este capítulo — el mismo límite que `AuditLedger` (CH-19 §15) ya
dejó abierto para la lectura de su propio ledger.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST ClassifyDataRejectsAnEmptySubjectRef
TEST ClassifyDataRejectsAnEmptyProvenance
TEST ClassifyDataDefaultsToRestrictedWhenNoGovernanceRuleMatches
TEST ClassifyDataNeverInspectsTheContentOfTheDataItClassifies
TEST ClassifyDataEmitsAnAgentEventOnlyWhenExecutionAndAgentIdAreBothResolved
TEST EnforceRetentionChecksLegalHoldBeforeComparingTheRetentionDeadline
TEST EnforceRetentionNeverMutatesOrClearsTheRetentionDeadlineOnALabel
TEST EnforceRetentionIsATotalFunctionThatNeverThrows
TEST DataGovernanceEngineNeverDecidesWhetherAContextBlockIsRelevant
TEST DataGovernanceEngineNeverReclassifiesACredentialReference
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (después de CH-20 — séptimo plano de Amendment v1.1 cubierto por este libro, y primer
capítulo que materializa P-22/INV-E11 con código real más allá de un secreto)

Constitution
 ├── Article IV     — Decision Ownership (tabla original sin cambios; DataGovernanceEngine, como
 │                     PolicyEngine/ContextEngine, decide algo real — no comparte la ausencia de
 │                     fila de EventBus/AuditLedger)
 └── Amendment v1.1 — Enterprise Activation, Interoperability and Operations
                       (P-22/INV-E11 citados por primera vez con código real más allá de
                       CredentialClassification; Ingress & Activation Plane, CH-14, Agent
                       Interoperability Plane, CH-15, Capability & Integration Plane, CH-16,
                       Reliability Plane, CH-17, Control Plane, CH-18, Observability & Governance
                       Plane, CH-19, y Data & Context Plane, este capítulo, siete de nueve planos
                       canónicos instalados — solo Execution Plane y Execution Fabric quedan sin
                       cubrir)

Contracts (registry/contracts.yaml)
 ├── C-001..C-029  (sin cambios — CH-00..CH-19)
 └── C-030 DataGovernanceLabel  (CH-20, nuevo — la etiqueta de gobernanza portátil que viaja con
                        un dato, P-22/INV-E11/INV-19)

Components (registry/components.yaml)
 ├── CMP-001..CMP-017  (sin cambios — CH-01..CH-19)
 └── CMP-018 DataGovernanceEngine  (CH-20, nuevo — séptimo componente de este registry que no
                          corresponde a ninguno de los once nombres de Article III; pertenece al
                          Data & Context Plane de Amendment v1.1)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado real de cada componente que produce un dato hacia `classifyData`**: `ContextEngine`
  (CH-04) y `ToolRuntime` (CH-02) no fueron modificados para invocar de verdad `classifyData` sobre
  su propio `ContextBlock`/`ToolResult` — la demostración de la seccion 11 prueba que el mecanismo
  funciona, no que ya esté conectado dentro de un flujo real.
- **Cuál `DataGovernanceLabel` es "el vigente" para un `subjectRef` dado**: este capítulo modela
  `classifyData` como productor de una etiqueta nueva en cada invocación, pero no modela ningún
  registro ni índice que responda "¿cuál es la última etiqueta producida para este dato?" — asumido,
  no construido (mismo límite que `registeredCapabilities`, CH-08, o `subscriptions`, CH-09,
  documentaron para sus propios registros asumidos).
- **El motor real de reglas de gobernanza** detrás de `dataGovernanceRuleFound`/
  `matchDataGovernanceRule`/`dataGovernanceRuleClassification`/`dataGovernanceRuleResidency`/
  `dataGovernanceRuleRetentionDeadline`/`dataGovernanceRuleLineage`: este capítulo modela la forma de
  la decisión (fail-closed hacia `RESTRICTED`), no un lenguaje de reglas real ni un catálogo
  administrable de reglas por procedencia.
- **El mecanismo real que ejecuta un borrado, un cifrado, o el movimiento físico de un dato entre
  regiones**: `enforceRetention` decide SI un borrado es exigible; ejecutarlo, cifrar un dato, o
  moverlo físicamente a la región que `residencyRequirement` exige, queda, deliberadamente, sin
  modelar — Preview, infraestructura de borde.
- **El grafo completo de lineage**: `lineageRef` es una referencia opaca; de dónde vino exactamente
  un dato, a través de qué transformaciones, en qué orden, no se modela como un grafo navegable en
  este capítulo.
- **Autorización de lectura/escritura sobre las propias etiquetas de gobernanza**: quién puede
  producir o consultar un `DataGovernanceLabel` — señalado explícitamente en la seccion 15, no
  resuelto (mismo límite abierto que `AuditLedger`, CH-19 §15, dejó para su propio ledger).
  `INV-E07` (aislamiento por tenant) tampoco se modela aquí, por la misma razón que CH-16 §18 ya
  documentó para `CredentialBroker`.
- **Auditar una clasificación con `AuditLedger`**: ningún cableado real conecta todavía
  `DataGovernanceEngine` con `recordAuditEntry` (CH-19) para preservar evidencia inmutable de que una
  clasificación concreta ocurrió — señalado en prosa (seccion 9/15), no construido.
- **Los dos planos restantes** del Amendment v1.1 (Execution Plane, Execution Fabric) y **la
  profundización del Data & Context Plane más allá de este primer componente** (p. ej. un esquema de
  reglas de gobernanza real, administrable, o el cableado de punta a punta descrito arriba):
  explícitamente fuera de alcance.
- Reviewers plurales, evals y orquestación multi-agente propiamente dicha: explícitamente fuera de
  alcance de BH-v0.1.

## 19. Siguiente Incremento (Next Increment)

Con este capítulo, el "Data & Context Plane" de Amendment v1.1 tiene su primer componente real que
generaliza `P-22` más allá de un secreto — pero el plano completo (el cableado real hacia
`ContextEngine`/`ToolRuntime`, el motor real de reglas de gobernanza, el mecanismo real de borrado/
cifrado/residencia física, el registro de "cuál etiqueta es la vigente") sigue sin construirse de
punta a punta. El problema natural del próximo incremento es, o bien profundizar este mismo plano
(cableando por fin `DataGovernanceEngine` dentro de `ContextEngine.assembleContextSnapshot` y de
`ToolRuntime.executeToolCall`, el mismo patrón de integración que CH-12/CH-13 ya establecieron para
el camino feliz y los caminos de gobierno de un `AgentRun`), o bien avanzar hacia cualquiera de los
dos planos restantes que Amendment v1.1 enumera — el Execution Plane (segundo plano canónico,
todavía sin cubrir por ningún capítulo de este libro) o el Execution Fabric (noveno y último plano
canónico) — son, los dos, candidatos particularmente naturales para cerrar la cobertura completa de
los nueve planos de la enmienda.

`next_chapter` queda en `null` en el frontmatter de este capítulo porque, en este momento del libro,
ese próximo capítulo todavía no existe como archivo — solo como el problema que motivaría su
escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg / Bucles
> de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows),
> secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): `P-22` fue citado en prosa dos veces (CH-10, CH-11) y
   materializado con código real solo una vez (CH-16) — exclusivamente para un secreto, dejando el
   resto del universo de datos del sistema sin ningún mecanismo de gobernanza.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): un principio real
   puede resolverse de forma parcial y correcta para un tipo estrecho de dato, sin que nadie
   generalice jamás esa misma exigencia constitucional al resto del universo que el sistema mueve.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `DataGovernanceEngine` con una ficha que declara tanto lo que posee (`owns`: clasificar cualquier
   dato, exigir residencia/retención/legal-hold de forma independiente del modelo) como lo que
   explícitamente NO posee (`does_not_own`: seleccionar por relevancia — `ContextEngine`, CH-04 — ni
   reclasificar un secreto ya clasificado — `CredentialBroker`, CH-16).
4. **Modelos mentales** (= §4, Constitutional Impact): el mismo argumento que ya protegió la
   autorización de acciones (`P-13`) se extiende aquí a los datos (`P-22`) — que un dato sea
   sensible no depende de que el modelo lo entienda o lo acepte.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un principio constitucional real se resuelve solo
  para un tipo estrecho de dato, crece la tentación de tratarlo como "ya cubierto" para el resto del
  sistema — hasta que un dato de un tipo distinto necesita, de verdad, una clasificación real, y no
  existe ningún mecanismo general que se la aplique.
- **Bucle de equilibrio (estabiliza):** `classifyData` (§11) deniega por defecto hacia el nivel de
  clasificación más conservador cuando ninguna regla aplica — cerrando, con el mismo principio
  fail-closed que ya protegió la autorización desde CH-05, el bucle que CH-10..CH-19 dejaron abierto.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `enforceRetention` (§11) evalúe `legalHold`
ANTES de comparar `retentionDeadline`, y que en ningún camino borre o reemplace ese plazo original. Si
la preservación legal sobrescribiera el plazo, se perdería, para siempre, la única forma de saber, una
vez liberada, si el borrado ya debía haber ocurrido — esa precedencia, y esa preservación del dato
original, es la forma en que este capítulo hace la interacción legal-hold/retención segura por
diseño.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo de
> esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set` (frontmatter) y
> es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa, para lectura directa
> del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Ya existe un componente que decide qué fragmento de información es relevante para que el modelo
   razone sobre el turno actual. ¿Esa misma decisión responde también cuánto tiempo puede
   conservarse ese fragmento, o son preguntas de dominios distintos? *(cierra la pregunta guía 1)*
2. Si un dato ya fluyó hacia el material que el modelo puede ver, ¿qué necesitaría quedar fijado
   sobre ESE dato para que alguien, después, supiera cuán sensible es, dónde debe residir y hasta
   cuándo puede conservarse? *(cierra la pregunta guía 2)*
3. Si una orden legal exige preservar un dato más allá de su fecha de borrado ya programada, ¿qué
   debería pasar con ese plazo original? *(cierra la pregunta guía 3)*
4. Un mecanismo ya sabe aplicar, sobre un tipo específico de dato, un nivel de gobierno con solo dos
   gradaciones. ¿Basta con reusar ese mismo esquema para cualquier otro dato del sistema, o hace
   falta algo distinto? *(cierra la pregunta guía 4)*

### Explicar

1. `DataGovernanceEngine` posee clasificar un `ContextBlock` ya seleccionado por `ContextEngine`
   con un nivel de sensibilidad y requisitos de residencia/retención. Explica, como si hablaras con
   alguien sin contexto técnico, por qué NO posee decidir si ese mismo `ContextBlock` es relevante
   para el turno actual.
2. `DataGovernanceLabel.legalHold`, cuando está activo, suspende cualquier borrado programado — pero
   `retentionDeadline` nunca se borra ni se reemplaza. Explica qué se perdería si, en cambio,
   `enforceRetention` simplemente borrara `retentionDeadline` al activarse `legalHold`.

### Conectar

1. `ContextEngine.assembleContextSnapshot` (CH-04) ya produce un `ContextBlock` con `provenance`.
   ¿Le correspondería a esa misma función producir, además, la clasificación de gobernanza de ese
   fragmento, o pertenece a un dueño distinto?
2. `CredentialBroker.resolveCredentialReference` (CH-16) ya aplica `CredentialClassification` sobre
   un secreto. ¿Le correspondería a `DataGovernanceEngine` reclasificar, además, ese mismo secreto?
3. `AuditLedger.recordAuditEntry` (CH-19) ya produce evidencia inmutable de una decisión ya tomada.
   ¿Le bastaría auditar un `DataGovernanceLabel` exactamente igual que auditó una `PolicyDecision`,
   o existe una diferencia real entre ambos casos?

### Espaciar

Las cinco tarjetas de repaso de este capítulo (dos sobre `DataGovernanceEngine` — su `owns` y su
`does_not_own` —, dos sobre `DataGovernanceLabel` — sus campos y la interacción legal-hold/retención
—, y una sobre la frontera con `CredentialClassification`) entran hoy en `reviewStage = DAY_1`.
Repásalas de nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) — ver el apéndice de tarjetas
al final del libro (edición PDF) o `retrieval_set.flashcards` en `dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te equivocaste,
ese es precisamente el punto ciego que este método existe para revelar.
