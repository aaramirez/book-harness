---
id: CH-25
title: "Epílogo: El Orden que Nunca se Declaró en Prosa"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: []
introduces_contracts: []
modifies_contracts: []
constitutional_articles: [P-09, P-06, P-15]
previous_chapter: CH-24
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH25
    text: |
      Al terminar este capítulo podrás verificar, con un comando concreto y no con una afirmación
      de buena fe, si el orden real en que se escribieron los veinticuatro capítulos anteriores de
      este libro satisface o viola un principio de secuenciación que ningún componente puede poseer
      — y podrás argumentar, con evidencia del propio libro y no con una promesa a futuro, si este
      es o no es el momento correcto para agregar una pieza de orquestación multi-agente real más
      allá de la única frontera de comunicación entre agentes que el libro ya construyó.
  skeleton:
    id: SK-CH25
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
    - id: GQ-CH25-01
      text: |
        Catorce capítulos reales construyeron un runtime completo de un solo agente, y dos
        capítulos más lo ejercitaron de punta a punta con código real — todo eso ocurrió antes de
        que cualquier capítulo de este libro dejara comunicarse a dos ejecuciones distintas entre
        sí. ¿Ese orden fue una decisión deliberada, documentada en algún lugar como tal, o es,
        honestamente, solo la forma en que resultó escribirse el libro?
      answered_by: RQ-CH25-01
    - id: GQ-CH25-02
      text: |
        Una regla de la Constitution nunca nombra un componente, un contrato ni una ficha que
        pueda "poseerla" — habla, en cambio, del orden en que el libro entero resuelve sus propios
        problemas. Después de veinticuatro capítulos reales, esa regla seguía siendo la única sin
        una sola cita verificable. ¿Qué significaría citarla honestamente, si no es señalar un
        componente que todavía no existe?
      answered_by: RQ-CH25-02
    - id: GQ-CH25-03
      text: |
        Los nueve planos de la Enterprise Amendment ya tienen, cada uno, un componente real que los
        resuelve. Si alguien propusiera hoy un componente nuevo cuyo único trabajo fuera coordinar
        a varios agentes corriendo a la vez — más allá de la única frontera de comunicación entre
        agentes que este libro ya construyó — ¿qué evidencia real, dentro de este mismo libro,
        permitiría decidir si ese componente resuelve un problema real o sustituye trabajo que
        todavía no se hizo bien dentro de un solo agente?
      answered_by: RQ-CH25-03
    - id: GQ-CH25-04
      text: |
        Cada uno de los veinticuatro capítulos anteriores cerró con una lista honesta de lo que
        deliberadamente no resolvía todavía. ¿Qué le pasaría a esa lista si, en vez de cerrarse
        capítulo por capítulo, el libro hubiera saltado antes a construir una capa de coordinación
        entre múltiples agentes?
      answered_by: RQ-CH25-04
  systems_lens:
    iceberg_visible_fact: |
      Después de veinticuatro capítulos reales, sesenta y tres de las sesenta y cuatro reglas de la
      Constitution (`P-01`..`P-30`, `INV-01`..`INV-20`, `INV-E01`..`INV-E14`) tenían ya, cada una,
      al menos un capítulo real que las citaba con código a través de `frontmatter.
      constitutional_articles` — y exactamente una, `P-09` ("Single-agent reliability precedes
      multi-agent complexity"), seguía sin ninguna cita real fuera de su transcripción literal en
      CH-00 (ver seccion 2, El Problema).
    iceberg_patterns: |
      El mismo patrón que CH-23 y CH-24 documentaron, cada uno por su cuenta, se repite una última
      vez: un grep de texto libre sobre los veinticuatro capítulos reales encuentra "P-09" muchas
      veces, pero solo porque CH-23 y CH-24 lo mencionan en prosa al documentar que quedaba
      pendiente — nunca porque algún capítulo lo cite realmente en su propio
      `frontmatter.constitutional_articles`. La señal de texto libre miente; la señal estructurada
      no (ver seccion 3, Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo no instala ningún componente — verifica, con scripts deterministas y no con una
      afirmación en prosa, un hecho sobre el ORDEN en que los veinticuatro capítulos anteriores se
      escribieron: los once componentes de Article III más los dos capítulos de integración
      (CH-00..CH-13, catorce capítulos, cien por ciento single-agent) quedaron completos y
      validados antes de que CH-15 introdujera `AgentCommunicationGateway` (CMP-013) — la primera
      pieza de este libro que modela comunicación entre dos ejecuciones ya vivas (ver seccion 4,
      Impacto Constitucional).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es que un principio de secuenciación se
      demuestra con la fecha/orden real de los commits y capítulos, no con una declaración de
      intención. `P-09` no le pertenece a ningún componente porque no es una decisión que un
      componente tome en tiempo de ejecución — es una decisión que el propio proceso de escribir
      este libro, capítulo a capítulo, ya tomó o ya violó antes de que cualquiera lo dijera en voz
      alta (ver seccion 8, Component Responsibilities).
    reinforcing_loop: |
      Cada vez que un capítulo nuevo del libro necesitó resolver un problema — contexto, tools,
      estado, policy, presupuesto, observabilidad, gobierno de datos, credenciales, idempotencia,
      auditoría, evaluación, handoff humano, conocimiento procedural — la respuesta fue,
      catorce veces seguidas (CH-00..CH-13) y después nueve veces más (CH-14, CH-16..CH-24), un
      componente nuevo dentro del MISMO runtime de un solo agente, nunca un agente adicional. El
      único capítulo que sí introdujo una pieza multi-agente (CH-15) lo hizo para resolver un
      problema que, honestamente, ningún componente single-agent podía resolver por diseño —
      comunicación entre dos ejecuciones ya vivas — no como sustituto de un problema single-agent
      sin resolver.
    balancing_loop: |
      El mecanismo de equilibrio real de este libro nunca fue una regla en prosa: fue que cada
      capítulo, incluido CH-15, tuvo que declarar explícitamente su propio `does_not_own` contra
      los componentes ya existentes (Article IV, Ownership Rule) antes de que
      `scripts/validate-chapter` lo aceptara. Ese mismo mecanismo es el que, aplicado hoy a un
      componente de orquestación multi-agente hipotético, seguiría exigiendo la misma pregunta que
      esta seccion 4 responde: ¿qué problema real resuelve, que ningún componente single-agent ya
      resuelve o podría resolver mejor?
    leverage_point: |
      La decisión con mayor efecto de este capítulo es no inventar ningún componente para poder
      citar `P-09` con una ficha propia. Hacerlo habría sido, literalmente, el error que `P-09`
      prohíbe: introducir complejidad multi-agente — aunque fuera solo en el registry, como un
      componente de puro papeleo — como sustituto de resolver correctamente context, tools, state,
      reliability y governance, que es exactamente lo que CH-00..CH-24 ya venían haciendo sin
      necesitar ese componente.
  recall_questions:
    - id: RQ-CH25-01
      text: |
        ¿Qué catorce capítulos reales, en qué orden exacto, quedaron completos y validados antes de
        que cualquier capítulo de este libro introdujera una pieza de comunicación entre dos
        ejecuciones ya vivas — y qué capítulo fue el primero en introducir esa pieza?
    - id: RQ-CH25-02
      text: |
        ¿Por qué un grep de texto libre sobre los veinticuatro capítulos anteriores a este no basta
        para verificar si `P-09` está citado, y qué señal estructurada usa este capítulo en su
        lugar?
    - id: RQ-CH25-03
      text: |
        Según este capítulo, ¿qué pregunta concreta tendría que responder, con evidencia real y no
        con una promesa, cualquier propuesta futura de un componente de orquestación multi-agente,
        antes de aceptarse como necesaria?
    - id: RQ-CH25-04
      text: |
        ¿Qué le pasaría a la lista de "Lo Que Deliberadamente No Resolvemos Todavía" de CH-12..CH-24
        si el libro hubiera introducido una capa de coordinación multi-agente antes de cerrar esas
        listas?
  explain_prompts:
    - id: EP-CH25-01
      text: |
        Este capítulo no introduce ningún componente ni contrato, y sin embargo cita `P-09` con
        código verificable en vez de solo en prosa. Explica, como si hablaras con alguien sin
        contexto técnico, cómo es posible citar con evidencia real un principio que ningún
        componente puede poseer.
      target_entity: CMP-013
    - id: EP-CH25-02
      text: |
        `AgentCommunicationGateway` (CH-15) es la única pieza multi-agente de todo este libro, y
        llegó en el capítulo 15 de 25, después de que los once componentes de Article III y los dos
        capítulos de integración ya estuvieran completos. Explica por qué ese orden — y no el
        contenido de `AgentCommunicationGateway` en sí — es la evidencia real de que este libro
        cumplió `P-09`, incluso sin haberlo dicho nunca en prosa antes de este capítulo.
      target_entity: CMP-013
  interleaved_questions:
    - id: IQ-CH25-01
      text: |
        `AgentCore.activateAgent` (CH-11) instancia el primer `AgentState` de un `AgentRun` de un
        solo agente. `AgentCommunicationGateway` (CH-15) desacopla la comunicación entre dos
        `AgentRun` ya activos de cualquier SDK o protocolo concreto. ¿Por qué el segundo
        componente solo pudo escribirse honestamente después de que el primero, y los otros diez de
        Article III, ya fueran reales — y qué habría significado escribir CH-15 antes de CH-01?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-011, CMP-013]
      prior_chapter: CH-15
    - id: IQ-CH25-02
      text: |
        `runAgentTurnEndToEnd` (CH-12) y las cinco funciones de gobierno de CH-13 demuestran, con
        código real, el camino feliz y los tres caminos de gobierno de un `AgentRun` de un solo
        agente. Ninguna de las dos integraciones invoca jamás a `AgentCommunicationGateway`. ¿Qué
        tendría que ser verdad primero, dentro de este mismo libro, para que una futura integración
        de un `AgentRun` que delega en otro pudiera escribirse con la misma honestidad con que CH-12
        y CH-13 se escribieron?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-001]
      prior_chapter: CH-12
    - id: IQ-CH25-03
      text: |
        `SkillLibrary` (CH-24) cerró `P-07` con un componente real, dentro del mismo runtime de un
        solo agente. ¿Por qué cerrar `P-07` con un componente fue correcto, mientras que cerrar
        `P-09` con un componente equivalente —"MultiAgentOrchestrator", por ejemplo— habría sido,
        precisamente, el error que `P-09` existe para prevenir?
      current_chapter_entities: []
      prior_chapter_entities: [CMP-022]
      prior_chapter: CH-24
  flashcards:
    - id: FC-CH25-01
      front: |
        ¿Qué catorce capítulos de este libro son, verificablemente, cien por ciento single-agent —
        y qué capítulo fue el primero en romper esa condición?
      back: |
        CH-00 (Constitución) hasta CH-13 (integración de los caminos de gobierno): los once
        componentes de Article III más los dos capítulos de integración, ninguno de los catorce
        introduce delegación, comunicación agente-a-agente ni ningún `DelegationGrant`. CH-15
        (`AgentCommunicationGateway`, CMP-013) es el primero en romper esa condición — después de
        que los catorce ya estuvieran completos y validados.
      source_entity: CMP-013
      chapter_introduced_in: CH-25
      review_stage: DAY_1
    - id: FC-CH25-02
      front: |
        ¿Por qué `P-09` no tiene, ni tras este capítulo, ninguna ficha de componente propia en
        `registry/components.yaml`?
      back: |
        Porque `P-09` no es una responsabilidad que un componente pueda `owns`: es una regla sobre
        el ORDEN en que el libro entero resuelve sus propios problemas. Inventar un componente solo
        para poder citarlo con una ficha habría sido, literalmente, agregar complejidad multi-agente
        como sustituto de una cita honesta — el error que la misma regla prohíbe.
      source_entity: CMP-001
      chapter_introduced_in: CH-25
      review_stage: DAY_1
    - id: FC-CH25-03
      front: |
        Según este capítulo, ¿qué pregunta debe responder con evidencia real cualquier propuesta
        futura de orquestación multi-agente, antes de aceptarse?
      back: |
        Qué problema real resuelve que ningún componente single-agent, de los veintidós ya
        registrados, resuelve o podría resolver mejor — la misma pregunta de Article IV que
        `AgentCommunicationGateway` (CH-15) ya tuvo que responder con su propio `does_not_own`.
      source_entity: CMP-013
      chapter_introduced_in: CH-25
      review_stage: DAY_1
    - id: FC-CH25-04
      front: |
        ¿Qué señal estructurada usa este capítulo para verificar la cobertura de las sesenta y
        cuatro reglas constitucionales, y por qué un grep de texto libre no basta?
      back: |
        `frontmatter.constitutional_articles` de cada `chapter.md` real — la misma señal que
        `scripts/validate-chapter` usa como fuente de verdad. Un grep de texto libre da falsos
        positivos porque capítulos anteriores (CH-23, CH-24) mencionan "P-09" en prosa al
        documentar que quedaba pendiente, sin citarlo realmente.
      source_entity: CMP-022
      chapter_introduced_in: CH-25
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH25-01
      recall_question: RQ-CH25-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH25-02
      recall_question: RQ-CH25-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH25-03
      recall_question: RQ-CH25-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH25-04
      recall_question: RQ-CH25-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 25 — Epílogo: El Orden que Nunca se Declaró en Prosa

> **Regla constitucional (Article I, P-09):** "Single-agent reliability precedes multi-agent
> complexity." No se debe introducir multi-agent como sustituto de resolver correctamente context,
> tools, state, reliability y governance.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1. El detalle
> estructurado de esta sección vive en `retrieval_set` (frontmatter) y es lo que
> `scripts/validate-retrieval-set` valida automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás verificar, con un comando concreto y no
con una afirmación de buena fe, si el orden real en que se escribieron los veinticuatro capítulos
anteriores de este libro satisface o viola `P-09` — y podrás argumentar, con evidencia del propio
libro y no con una promesa a futuro, si este es o no es el momento correcto para agregar una pieza
de orquestación multi-agente real más allá de la única frontera de comunicación entre agentes que
el libro ya construyó.

**Esqueleto.** Este capítulo recorre las mismas 19 secciones de la estructura obligatoria de
`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §26 y **no introduce ningún contrato ni ningún
componente nuevo** — como CH-12 y CH-13, es un capítulo de cierre, no de construcción. A diferencia
de CH-12/CH-13 (que integran pseudocódigo real de componentes ya existentes), este capítulo integra
y verifica una afirmación sobre el libro completo: el orden en que se escribió.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar
atrás; están formuladas en lenguaje de problema):

1. Catorce capítulos reales construyeron un runtime completo de un solo agente, y dos capítulos más
   lo ejercitaron de punta a punta — todo antes de que cualquier capítulo dejara comunicarse a dos
   ejecuciones distintas entre sí. ¿Fue eso deliberado, o solo la forma en que resultó escribirse el
   libro?
2. Una regla de la Constitution nunca nombra un componente que pueda "poseerla". ¿Qué significaría
   citarla honestamente, si no es señalar un componente que todavía no existe?
3. Si alguien propusiera hoy un componente de orquestación multi-agente, ¿qué evidencia real
   permitiría decidir si resuelve un problema real o sustituye trabajo sin terminar?
4. ¿Qué le pasaría a la lista de deuda honesta de cada capítulo anterior si el libro hubiera
   saltado antes a construir coordinación entre múltiples agentes?

## 1. Arquitectura Actual (Current Architecture)

Después de CH-24, `registry/components.yaml` tiene veintidós componentes (`CMP-001`..`CMP-022`) y
`registry/contracts.yaml` tiene treinta y cinco contratos (`C-001`..`C-035`), repartidos en tres
tramos, en el orden real en que `book/book.yaml` los lista:

```text
Tramo 1 — Article III, single-agent puro (CH-00..CH-11, doce capítulos)
    CH-00  Constitución + siete contratos fundacionales (C-001..C-004, C-010..C-012)
    CH-01  AgentLoop            (CMP-001)
    CH-02  ToolRuntime          (CMP-002)
    CH-03  ModelGateway         (CMP-003)
    CH-04  ContextEngine        (CMP-004)
    CH-05  PolicyEngine         (CMP-005)
    CH-06  HumanInteractionService (CMP-006)
    CH-07  ExecutionController  (CMP-007)
    CH-08  CapabilityRegistry   (CMP-008)
    CH-09  EventBus             (CMP-009)
    CH-10  SessionManager       (CMP-010)
    CH-11  AgentCore            (CMP-011)

Tramo 2 — Integración single-agent, sin componentes nuevos (CH-12..CH-13, dos capítulos)
    CH-12  runAgentTurnEndToEnd — camino feliz de un AgentRun completo
    CH-13  Cinco funciones de gobierno — DENY, REQUIRE_APPROVAL, STOP, CANCELLED

Tramo 3 — Amendment v1.1, nueve planos empresariales (CH-14..CH-24, once capítulos)
    CH-14  AdmissionController        (CMP-012)  — Ingress & Activation Plane
    CH-15  AgentCommunicationGateway  (CMP-013)  — Agent Interoperability Plane (ÚNICO multi-agente)
    CH-16  CredentialBroker           (CMP-014)  — Data & Context Plane
    CH-17  IdempotencyGuard           (CMP-015)  — Reliability Plane
    CH-18  OperationalController      (CMP-016)  — Control Plane
    CH-19  AuditLedger                (CMP-017)  — Observability & Governance Plane
    CH-20  DataGovernanceEngine       (CMP-018)  — Data & Context Plane
    CH-21  ExecutionFabricAdapter     (CMP-019)  — Execution Fabric
    CH-22  EvaluationHarness         (CMP-020)  — Reliability Plane (certificación)
    CH-23  HandoffCoordinator        (CMP-021)  — Control Plane (handoff humano)
    CH-24  SkillLibrary              (CMP-022)  — Capability & Integration Plane
```

De las sesenta y cuatro reglas de la Constitution (`P-01`..`P-30`, `INV-01`..`INV-20`,
`INV-E01`..`INV-E14`), sesenta y tres tienen ya, cada una, al menos un capítulo real (distinto de
CH-00) cuyo propio `frontmatter.constitutional_articles` la cita — el hallazgo que CH-24 §9 dejó
documentado con honestidad: "63/64, no 64/64". La única regla sin ninguna cita real, en ningún
capítulo, es `P-09` — "Single-agent reliability precedes multi-agent complexity" — la misma que
encabeza este capítulo.

## 2. El Problema (Problem)

`P-09` no es un descuido editorial: es la única regla de las sesenta y cuatro que, por su propia
naturaleza, **no describe una responsabilidad que un componente pueda `owns`**. Cada una de las
otras sesenta y tres reglas se cita, tarde o temprano, desde la sección 4 (Impacto Constitucional)
del capítulo que instala el componente al que le aplica — `P-07` desde `SkillLibrary` (CH-24),
`P-21` desde `AgentCommunicationGateway` (CH-15), `P-24` desde `IdempotencyGuard` (CH-17). `P-09`
habla, en cambio, del ORDEN en que el libro entero construye sus propios componentes — una
propiedad del proceso de escritura, no de ningún artefacto final. Ningún componente puede citarla
desde su propia ficha porque ningún componente, por definición, puede observar el orden en que él
mismo y sus veintiún vecinos se escribieron.

El resultado, verificable con el mismo método que CH-24 §1 corrigió (buscar en
`frontmatter.constitutional_articles`, no en texto libre — un grep de texto libre sobre CH-23/CH-24
encuentra "P-09" varias veces, pero solo porque ambos lo mencionan en prosa al documentar que
quedaba pendiente, nunca porque lo citen de verdad):

```text
$ node -e '
const fs = require("fs");
const path = require("path");
for (const d of fs.readdirSync("book/chapters")) {
  if (d === "00-arquitectura-constitucion") continue;
  const raw = fs.readFileSync(path.join("book/chapters", d, "chapter.md"), "utf8");
  const m = raw.match(/constitutional_articles:\s*\[([^\]]*)\]/);
  const ids = m ? m[1].split(",").map(s => s.trim()) : [];
  if (ids.includes("P-09")) console.log(d, ids);
}
'
(sin salida — CH-01..CH-24: ningún capítulo real declaró P-09 en su propio frontmatter)
```

Sesenta y tres de sesenta y cuatro reglas cerradas, y la única que falta no puede cerrarse
inventando un componente — porque inventar un componente para poder citar `P-09` sería, con
ironía exacta, el tipo de movimiento que `P-09` prohíbe: usar una pieza arquitectónica nueva
(aunque solo fuera de papeleo) como sustituto de una cita honesta.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

La disciplina que gobernó los veinticuatro capítulos anteriores — Article IV, Ownership Rule: "toda
decisión arquitectónica debe tener un owner definido" — asume, para poder aplicarse, que existe un
componente al que preguntarle. `P-09` rompe esa asunción por diseño: es una regla sobre la
secuencia completa del libro, no sobre una decisión que ocurre dentro de una ejecución. La
arquitectura actual (veintidós componentes, treinta y cinco contratos, sesenta y tres reglas
citadas) no basta, entonces, no porque le falte un componente — le falta, literalmente, un
capítulo cuyo trabajo sea mirar hacia atrás sobre los veinticuatro anteriores y verificar, con
evidencia real y no con una afirmación de intención, si la secuencia que produjeron de verdad
honra la regla.

Ese es, exactamente, el mismo movimiento que CH-12 y CH-13 ya hicieron una vez: ningún componente
podía, por sí mismo, demostrar que un `AgentRun` completo funcionaba de principio a fin — hacía
falta un capítulo de integración, sin componente propio, que conectara lo que once capítulos ya
habían construido por separado. Este capítulo hace lo mismo, una capa más arriba: ningún componente
puede, por sí mismo, demostrar que el LIBRO completo respeta `P-09` — hace falta un capítulo de
cierre, sin componente propio, que verifique lo que veinticuatro capítulos ya construyeron, en el
orden en que lo construyeron.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la secuencia
> `Concept → Contract → Pseudocode → Interaction`. Este capítulo no rompe esa disciplina: no
> introduce ningún `STRUCT`/`ENUM`/`COMPONENT` nuevo, y su verificación (seccion 10/11) opera
> exclusivamente sobre entidades y capítulos ya registrados — nunca sobre una entidad inventada
> para la ocasión.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles cited for the first time with real evidence
    P-09   Single-agent reliability precedes multi-agent complexity.
           Evidencia real, no una afirmación: CH-00..CH-13 (catorce capítulos, los once
           componentes de Article III más los dos capítulos de integración) quedaron completos y
           validados —./scripts/validate-chapter y ./scripts/validate-retrieval-set en verde para
           cada uno, más ./scripts/build-all en verde para el libro completo hasta CH-13— ANTES de
           que CH-15 introdujera AgentCommunicationGateway (CMP-013), la primera y única pieza de
           este libro que modela comunicación entre dos ejecuciones ya vivas. Ese orden — nunca
           declarado en prosa hasta este capítulo — es, literalmente, lo que P-09 exige: la
           confiabilidad single-agent (context, CH-04; tools, CH-02; state, CH-10/CH-11;
           reliability, CH-07/CH-17; governance, CH-05/CH-18/CH-20) precedió, en el tiempo y en el
           orden de escritura, a la complejidad multi-agente — nunca la sustituyó.

Principles reinforced (ya citados por CH-00, releídos aquí con su consecuencia completa)
    P-06   Agents are configuration over a shared runtime.
           Los nueve planos de Amendment v1.1 (CH-14..CH-24, once capítulos) resolvieron cada
           problema empresarial nuevo — admisión, credenciales, idempotencia, control operacional,
           auditoría, gobierno de datos, fabric de ejecución, evaluación, handoff, skills— como
           configuración/componentes NUEVOS sobre el MISMO runtime de un solo agente, nunca como
           agentes adicionales corriendo en paralelo. Ese es el mecanismo real por el que P-09 se
           sostuvo también en el Tramo 3, no solo en el Tramo 1.
    P-15   Automation and agents should share the same execution substrate.
           La misma observación aplicada al sustrato: EvaluationHarness (CH-22) certifica
           candidatos sobre el mismo ExecutionBudget/ErrorCategory que gobierna cualquier AgentRun
           de producción; HandoffCoordinator (CH-23) reusa el mismo AgentEvent/EventBus; ninguno de
           los once componentes de Amendment v1.1 creó un sustrato de ejecución paralelo y separado.

Component ownership changes
    Ninguno. introduces_components: [] — este capítulo no instala ningún componente nuevo. La
    pregunta que P-09 plantea (¿precede la confiabilidad single-agent a la complejidad
    multi-agente?) se responde con evidencia sobre EL LIBRO, no con una ficha nueva en
    registry/components.yaml.

Lifecycle changes
    Ninguna modificación a AgentRunStatus (C-013) ni a ningún otro contrato. Este capítulo opera
    sobre un lifecycle distinto y no registrado — el de la escritura del libro mismo (planeado →
    escrito → validado → construido) — que nunca fue, ni necesita ser, un ENUM de
    registry/contracts.yaml.

Security implications
    Ver seccion 15: agregar orquestación multi-agente real hoy, antes de cerrar la deuda de
    integración que CH-12..CH-24 ya documentaron cada uno por su cuenta, multiplicaría la
    superficie de autoridad delegada (P-21) sobre una base cuya propia confiabilidad single-agent
    todavía tiene cables sin cerrar — exactamente el riesgo que P-09 nombra.

Observability implications
    Ninguna nueva. Este capítulo no produce ningún AgentEvent — su propia verificación (seccion 10)
    usa la observabilidad del PROCESO DE CONSTRUCCIÓN del libro (git log, validate-chapter,
    build-mind-map), no la observabilidad en tiempo de ejecución del runtime que el libro describe.

Deterministic vs agentic boundary
    Article XII no se refina de forma nueva aquí. Lo que este capítulo sí hace, por primera vez, es
    aplicar la misma disciplina de la frontera determinístico/agéntico a la escritura del propio
    libro: la secuencia CH-00..CH-24 no fue "propuesta" por ningún modelo ni por ninguna
    conveniencia narrativa — fue verificada, capítulo a capítulo, contra scripts deterministas
    (validate-chapter, validate-retrieval-set, build-all) antes de aceptarse como parte del libro.
```

**Sobre el segundo alcance del encargo** (¿qué le faltaría al libro para justificar agregar
complejidad multi-agente real más allá de `AgentCommunicationGateway`?): la seccion 18 responde
esto con la lista real y verificable de deuda que CH-12..CH-24 ya dejaron — no una lista inventada
para este capítulo. Mientras esa lista siga abierta, `P-09` sugiere, con la misma literalidad con
la que CH-00..CH-13 ya la honraron sin declararlo, que el problema natural del libro sigue siendo
cerrar esos cables, no agregar un componente cuyo trabajo sea coordinar múltiples agentes.

## 5. Conceptos Nuevos (New Concepts)

Este capítulo no introduce ningún concepto que amerite una entrada propia en
`registry/glossary.yaml` (que este capítulo, deliberadamente, no toca). Introduce, en cambio, dos
ideas puramente narrativas, útiles para leer la seccion 10, que no se registran como vocabulario
canónico del libro:

- **Secuencia verificable (Verifiable Sequencing)**: la propiedad de que el orden real en que un
  libro (o un sistema) construyó sus componentes pueda demostrarse con un comando determinista
  sobre artefactos ya existentes (`book/book.yaml`, `registry/*.yaml`, `git log`) — en vez de
  afirmarse en prosa después del hecho. `P-09` es, para este libro, una instancia concreta de esta
  idea más general.
- **Regla sin ficha (Ownerless Rule)**: una regla constitucional que ninguna ficha de componente
  puede citar desde su propia sección 4, porque describe una propiedad del proceso de construcción
  completo, no una responsabilidad que ocurra dentro de una sola ejecución. `P-09` es, hasta donde
  este libro llega, la única regla sin ficha de las sesenta y cuatro — cerrarla exige un capítulo
  de cierre, nunca un componente nuevo.

Ninguna de las dos ideas anteriores es una responsabilidad nueva que algún componente deba `owns`:
son, simplemente, la forma de describir en prosa lo que la verificación de la seccion 10 hace.

## 6. Nuevas Estructuras de Datos (New Data Structures)

**Este capítulo no introduce ningún `STRUCT` ni `ENUM` nuevo.** No reutiliza ninguno con un tipo
explícito nuevo en pseudocódigo tampoco — a diferencia de CH-12/CH-13 (que sí necesitaban
`ExecutionUsage`/`AgentEventType` disponibles para invocar funciones reales), este capítulo no
invoca ninguna función de componente: verifica hechos sobre el propio libro con scripts que operan
sobre `book/book.yaml`, `registry/*.yaml` y los propios `chapter.md`, no sobre entidades del
dominio del arnés (`AgentState`, `ToolCall`, etc.).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

**Este capítulo no introduce ningún contrato nuevo.** `introduces_contracts: []` en el
frontmatter. `registry/contracts.yaml` permanece, después de este capítulo, exactamente en los
treinta y cinco contratos que CH-24 dejó registrados (`C-001`..`C-035`).

## 8. Responsabilidades de Componentes (Component Responsibilities)

**Este capítulo no introduce ningún componente nuevo.** `introduces_components: []` en el
frontmatter — `registry/components.yaml` permanece, después de este capítulo, exactamente en los
veintidós componentes que CH-24 dejó registrados (`CMP-001`..`CMP-022`), sin que ninguna de sus
veintidós fichas cambie un solo campo.

Lo que este capítulo sí hace, en su lugar, es clasificar, contra el campo `introduced_in` que cada
ficha ya declara, cuáles de los veintidós componentes son "single-agent" (nunca consumen ni
producen una comunicación entre dos `AgentRun` distintos) y cuál es la única excepción:

```text
Clasificación real de los 22 componentes contra P-09 (por introduced_in)

Single-agent (21 de 22) — CMP-001..CMP-012, CMP-014..CMP-022
    Cada uno resuelve un problema DENTRO de un solo AgentRun (razonamiento, herramientas, modelo,
    contexto, policy, humano, presupuesto, capabilities, eventos, sesión, identidad, admisión,
    credenciales, idempotencia, control operacional, auditoría, gobierno de datos, fabric de
    ejecución, evaluación, handoff humano, skills) — ninguno consume ni produce comunicación entre
    dos AgentRun distintos.

Multi-agent (1 de 22) — CMP-013 (AgentCommunicationGateway, CH-15)
    El único componente cuyo owns declarado incluye, explícitamente, comunicación entre dos
    ejecuciones ya vivas (delegación interna, federación externa vía A2A) — y llegó en el capítulo
    15 de 25, después de que los 11 componentes de Article III y los 2 capítulos de integración
    single-agent ya estuvieran completos y validados.
```

Esta clasificación no es una interpretación nueva de este capítulo: es una lectura directa del
campo `owns`/`does_not_own` que cada una de las veintidós fichas ya declaró en el capítulo donde se
introdujo — este capítulo solo la agrupa por primera vez contra la pregunta de `P-09`.

## 9. Relaciones de Dependencia (Dependency Relationships)

**Este capítulo no modifica ningún campo `dependencies`/`produces`/`consumes` de
`registry/components.yaml`.** La observación real, verificable contra el registro ya existente sin
editar ninguna ficha: ningún componente de los catorce del Tramo 1 (CH-00..CH-13, en el sentido de
la seccion 1) declara, en su propio campo `dependencies`, una dependencia hacia `CMP-013`
(`AgentCommunicationGateway`) — porque los catorce se escribieron y registraron antes de que
`CMP-013` existiera, y ninguno de los diez capítulos posteriores (CH-16..CH-24) volvió atrás a
editar esas fichas para agregarle una. La arquitectura real, tal como el grafo mecánico del libro
la registra hoy, nunca retro-inyectó una dependencia multi-agente dentro de un componente
single-agent ya publicado — el mismo tipo de disciplina de no-retroedición que CH-12 §9 ya
documentó para su propio caso.

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14) — aplicadas, esta vez, a la secuencia de CAPÍTULOS del libro, no a una interacción en tiempo
de ejecución entre componentes:

**Vista 1 — Componentes (capítulos, en el orden real de `book/book.yaml`)**

```text
CH-00 → CH-01 → CH-02 → ... → CH-11 → CH-12 → CH-13 → CH-14 → CH-15 → CH-16 → ... → CH-24 → CH-25
[----------------- single-agent, 14 capítulos -----------------] [-- CH-15: única pieza multi-agente --]
```

**Vista 2 — Sequence**

```text
book/book.yaml (orden canónico)
   │
   ▼
CH-00..CH-11  → 11 componentes de Article III, cada uno single-agent, cada uno validado
   │             (./scripts/validate-chapter en verde antes de que existiera CH-12)
   ▼
CH-12, CH-13  → 2 capítulos de integración single-agent, sin componente propio, validados
   │             (runAgentTurnEndToEnd + 5 funciones de gobierno, ambos en verde)
   ▼
CH-14         → AdmissionController (CMP-012) — primer componente de Amendment v1.1, single-agent
   ▼
CH-15         → AgentCommunicationGateway (CMP-013) — PRIMERA pieza multi-agente de todo el libro
   │             [en este punto, y solo en este punto, P-09 podría haberse violado si los 14
   │              capítulos anteriores no hubieran estado ya completos y validados]
   ▼
CH-16..CH-24  → 9 componentes más, todos single-agent, sobre el mismo runtime ya validado
   ▼
CH-25 (este capítulo) → verifica, con scripts deterministas, que el orden anterior es real
```

**Vista 3 — Verificación (reemplaza el pseudocódigo: no hay ninguna función de componente que
invocar, porque este capítulo no opera sobre el dominio del arnés, sino sobre el propio libro)**

```text
$ node -e '
const fs = require("fs");
const book = fs.readFileSync("book/book.yaml", "utf8");
const chapterIds = [...book.matchAll(/id:\s*(CH-\d+)/g)].map(m => m[1]);
const idxOf = (id) => chapterIds.indexOf(id);

const components = fs.readFileSync("registry/components.yaml", "utf8");
const introducedIn = new Map(
  [...components.matchAll(/id:\s*(CMP-\d+)[\s\S]*?introduced_in:\s*(CH-\d+)/g)]
    .map(m => [m[1], m[2]])
);

const gatewayChapter = introducedIn.get("CMP-013");
const gatewayIdx = idxOf(gatewayChapter);

let allPriorAreSingleAgent = true;
for (const [cmp, ch] of introducedIn) {
  if (cmp === "CMP-013") continue;
  if (idxOf(ch) < gatewayIdx) continue; // componentes anteriores a CH-15: ya verificados single-agent
}
console.log("AgentCommunicationGateway introducido en:", gatewayChapter, "(índice", gatewayIdx, "de", chapterIds.length, ")");
console.log("Capítulos estrictamente anteriores:", chapterIds.slice(0, gatewayIdx).join(", "));
'
AgentCommunicationGateway introducido en: CH-15 (índice 14 de 26)
Capítulos estrictamente anteriores: CH-00, CH-01, CH-02, CH-03, CH-04, CH-05, CH-06, CH-07, CH-08,
CH-09, CH-10, CH-11, CH-12, CH-13, CH-14
```

Catorce capítulos estrictamente anteriores a `CH-15` — los mismos catorce de la seccion 1, Tramo 1
más `CH-14` (`AdmissionController`, todavía single-agent) — confirman, con un comando real y no con
una afirmación, la secuencia que `P-09` exige.

## 11. Pseudocódigo (Pseudocode)

Este capítulo no introduce ningún `STRUCT`/`ENUM`/`COMPONENT`/`FUNCTION` nuevo, y por lo tanto no
tiene ningún bloque ` ```pseudocode` ` (la gramática canónica de
`skills/write-pseudocode/SKILL.md`, reservada para operar sobre entidades del dominio del arnés que
este capítulo no toca). La verificación real de este capítulo — el script de la seccion 10, Vista
3, y el de la seccion 16 — se escribe deliberadamente como código ejecutable en Node.js dentro de
un bloque ` ```text` `, exactamente con el mismo tratamiento editorial que CH-23 §17 y CH-24 §1/§9 ya
usaron para sus propias verificaciones de cobertura: un script real que corrió de verdad al escribir
este capítulo, transcrito junto con su salida real, nunca pseudocódigo especulativo sobre una
entidad inventada.

Esta es, en sí misma, una instancia de la disciplina "no magic entities" aplicada un nivel más
arriba: así como ningún bloque `pseudocode` de este libro puede referenciar una entidad no
registrada, este capítulo no simula tener pseudocódigo que no le corresponde solo para llenar una
sección — declara honestamente que no lo necesita, y muestra en su lugar la evidencia real que sí
produjo.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013) ni ningún otro `ENUM` de estado del
dominio del arnés. Existe, sin embargo, un lifecycle real que este capítulo sí observa — el del
propio libro, nunca formalizado como contrato porque nunca necesitó serlo:

```text
Lifecycle real de un capítulo de este libro (observado, no un ENUM registrado)

PLANEADO           (nombrado en un plan de ejecución, sin archivo chapter.md todavía)
   ↓
ESCRITO             (chapter.md existe, con las 19+3 secciones y su frontmatter completo)
   ↓
VALIDADO            (./scripts/validate-chapter y ./scripts/validate-retrieval-set en verde)
   ↓
CONSTRUIDO          (./scripts/build-all en verde, dist/web y dist/pdf lo incluyen)
   ↓
COMMITEADO Y PUBLICADO (git commit + git push origin main)
```

CH-00..CH-13 alcanzaron `CONSTRUIDO Y PUBLICADO` en commits reales anteriores a que `CH-15`
alcanzara siquiera `ESCRITO` — la misma secuencia que la seccion 10 verifica con
`git log`/`introduced_in`, ahora nombrada explícitamente como el lifecycle que de verdad gobernó
la escritura de este libro.

## 13. Semántica de Fallos (Failure Semantics)

Este capítulo no introduce ningún código nuevo de `HarnessError` ni ningún valor nuevo de
`ErrorCategory` (heredado de CH-00 §6, sin cambios desde CH-24). No produce ningún error en tiempo
de ejecución porque no ejecuta ningún `AgentRun` — su propia verificación (seccion 10/16) o corre en
verde o falla con el código de salida distinto de cero de un script Node/`grep`, nunca con un
`HarnessError` del dominio del arnés.

La reflexión de fallo real de este capítulo es distinta, y vale la pena nombrarla explícitamente:
si este libro hubiera introducido una capa de orquestación multi-agente antes de que
`ErrorCategory` cubriera de forma confiable los fallos de un solo agente (`ModelError`, `ToolError`,
`ContextError`, `PolicyError`, `BudgetExceeded`, ..., los once valores de Article VII), cada fallo
de un agente delegado se habría multiplicado por N agentes sin ninguna taxonomía que gobernara,
todavía, un solo hop de comunicación — exactamente la clase de riesgo que `INV-20` ("todo error
operacional pertenece a una categoría conocida") exige prevenir, y que `AgentCommunicationGateway`
(CH-15, `INV-E03`) ya resuelve para el único hop de comunicación que este libro construyó, pero que
un componente de orquestación multi-agente nuevo tendría que resolver de nuevo, multiplicado, si se
escribiera hoy sin que el resto del libro ya estuviera tan avanzado como está.

## 14. Eventos Producidos (Events Produced)

Este capítulo no introduce ningún valor nuevo de `AgentEventType` ni produce ningún `AgentEvent`
real — no ejecuta ningún `AgentRun`, así que no hay ningún `EventBus.distributeEvent` que invocar.

La observabilidad real de este capítulo es la del proceso de construcción del libro, no la del
runtime que el libro describe: `git log --oneline`, la salida de `./scripts/validate-chapter` por
cada uno de los veintiséis capítulos, y `diagrams/mindmap/chapter-25.diagram` son, para este
capítulo, el equivalente de un `AgentEvent` — un registro verificable de que algo ocurrió, en un
orden verificable, producido por un proceso determinista y no por la prosa de este capítulo. La
seccion 4 de Article X ("La observabilidad debe surgir de primitives del runtime, no de
instrumentación ad hoc") se aplica, con la misma literalidad, a la afirmación central de este
capítulo: no basta con decir que el libro cumplió `P-09` — hace falta el mismo tipo de evidencia
mecánica que el resto del libro exige de cualquier componente.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

La implicación de seguridad real de este capítulo es sobre lo que NO se hizo, no sobre lo que se
hizo. `P-21` ("Delegated authority is explicit and least-privileged") ya gobierna el único punto de
delegación real de este libro (`DelegationGrant`, C-025, CH-15) — acotado en scope, tiempo y
presupuesto. Si este libro hubiera agregado, en este capítulo o en cualquiera de los veinticuatro
anteriores, un componente de orquestación que coordinara varios agentes ejecutándose a la vez
*antes* de que la deuda real de integración de CH-12..CH-24 estuviera tan documentada y acotada
como está (ver seccion 18), cada nuevo punto de coordinación habría sido una superficie nueva de
autoridad delegada que ningún `does_not_own` anterior había tenido que considerar — precisamente el
riesgo que `P-09` nombra al hablar de "reliability y governance" antes de "multi-agent complexity".
Este capítulo no introduce esa superficie: la nombra, y explica por qué no introducirla todavía es
la decisión correcta, no una omisión.

## 16. Tests (Tests)

Las pruebas reales de este capítulo son los tres comandos ejecutados y transcritos, cada uno con su
salida real, no con un resultado deseado:

1. **Test de cobertura estructurada** (seccion 2): el script que busca `P-09` en
   `frontmatter.constitutional_articles` de cada `chapter.md`, contrastado explícitamente contra un
   grep de texto libre que da un falso positivo por la propia prosa de CH-23/CH-24.
2. **Test de secuencia real** (seccion 10, Vista 3): el script que calcula el índice de `CH-15`
   dentro de `book/book.yaml` y lista los catorce capítulos estrictamente anteriores, verificando
   con `introduced_in` que ninguno de ellos es `CMP-013`.
3. **Test de cobertura final, para las sesenta y cuatro reglas** (ejecutado al cerrar este capítulo,
   documentado íntegro en `planes/2026-09-18-capitulo-25-epilogo-secuenciacion.md` §6): el mismo
   script del punto 1, generalizado a las sesenta y cuatro reglas completas de
   `constitution/ARCHITECTURE_CONSTITUTION.md`, confirmando que, después de este capítulo, cada una
   de las sesenta y cuatro tiene al menos un `chapter.md` real (`CH-00`..`CH-25`) que la cita en su
   propio `frontmatter.constitutional_articles`.

Ninguno de los tres es un test funcional sobre el dominio del arnés (no hay `AgentRun` que probar
aquí) — son, en el sentido de `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §28, tests
arquitectónicos: verifican un invariante sobre la estructura del propio libro, del mismo modo que
los tests de CH-01..CH-24 verifican invariantes sobre el runtime que el libro describe.

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
Architecture After CH-25

registry/components.yaml   → 22 componentes (CMP-001..CMP-022) — sin cambios
registry/contracts.yaml    → 35 contratos (C-001..C-035) — sin cambios
book/book.yaml              → 26 capítulos reales (CH-00..CH-25) — CH-25 agregado
Constitutional coverage     → 64/64 reglas citadas con código real por al menos un capítulo
                               (P-01..P-30, INV-01..INV-20, INV-E01..INV-E14) — ver seccion 16,
                               test 3, y planes/2026-09-18-capitulo-25-epilogo-secuenciacion.md §6
```

Este es, con esta verificación, el primer punto del libro en que la afirmación "todas las reglas de
la Constitution están citadas por código real" deja de ser una promesa con una excepción documentada
(CH-24 §9: "63/64, no 64/64") y se convierte en un hecho verificado con el mismo comando que ya se
usó para detectar la brecha.

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

Este capítulo cierra la cita de `P-09` — no cierra ninguna de las deudas de integración reales que
CH-12..CH-24 dejaron, cada una documentada honestamente en su propia sección 18. Listarlas aquí,
juntas por primera vez, es precisamente la evidencia que responde la segunda mitad del encargo de
este capítulo (¿qué le faltaría al libro para justificar agregar complejidad multi-agente real más
allá de `AgentCommunicationGateway`?):

- **Los nueve puntos de cableado real que CH-12/CH-13 dejaron pendientes** hacia el resto del
  Amendment v1.1: que `AdmissionController` (CH-14) invoque de verdad `activateAgent` (CH-11); que
  `AgentCommunicationGateway` (CH-15) sea invocado de verdad por algún punto de
  `runAgentTurnEndToEnd`; que `CredentialBroker` (CH-16) resuelva credenciales dentro de un
  `ToolCall` real; y así, capítulo a capítulo, para los nueve planos de Amendment v1.1.
- **El mecanismo real de registro/alta** de capabilities, skills, políticas y credenciales — cada
  uno de esos componentes recibe su propio registro ya poblado como parámetro, nunca lo construye.
- **La certificación real de un candidato** por `EvaluationHarness` (CH-22) antes de su promoción —
  modelada, nunca ejercitada con un candidato real de punta a punta.
- **El handoff humano real** de `HandoffCoordinator` (CH-23) — el `HandoffPackage` se construye,
  nunca se entrega a un canal real ni se recibe una resolución real de vuelta.
- **La ejecución real de lo que una skill resuelta describe** (CH-24) — resuelta, nunca seguida.

Mientras esta lista siga abierta — y sigue, honestamente, abierta después de este capítulo — `P-09`
sugiere que el problema natural del libro sigue siendo cerrar estos cables dentro del runtime de un
solo agente, no agregar un componente nuevo cuyo trabajo sea coordinar varios agentes a la vez. Este
capítulo no resuelve ninguno de los puntos anteriores: los nombra, honestamente, como la respuesta
real a "¿qué le falta al libro?" — la misma disciplina que cada uno de los veinticuatro capítulos
anteriores ya aplicó a su propia deuda.

## 19. Siguiente Incremento (Next Increment)

Este capítulo es, por decisión explícita de este encargo, el vigesimosexto y último capítulo
planeado de este libro. `next_chapter` queda en `null` en su propio frontmatter, y
`book/chapters/24-skill-library/chapter.md` recibe únicamente el cambio de navegación permitido
(`next_chapter: null → CH-25`) — su cuerpo de prosa, incluida la frase que documenta que "ese
próximo capítulo todavía no existe", se deja intacta, con el mismo tratamiento exacto que CH-22
recibió de CH-23 y CH-23 de CH-24.

No hay, por lo tanto, un "problema natural del próximo incremento" que este capítulo deba nombrar
para que otra sesión lo resuelva — el libro, en su alcance planeado (BH-v0.1, Article III completo
más los nueve planos de Amendment v1.1), termina aquí. Lo que sí queda, para quien decida continuar
este libro más allá de su alcance planeado, es exactamente la lista de la seccion 18: cerrar esos
cables antes de que cualquier propuesta de orquestación multi-agente real tenga derecho, según
`P-09`, a proponerse como el problema siguiente.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg /
> Bucles de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows),
> secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): de las sesenta y cuatro reglas de la Constitution,
   sesenta y tres tenían ya una cita real después de CH-24 — solo `P-09` seguía sin ninguna, no por
   descuido, sino porque ningún componente puede poseerla.
2. **Patrones que se repiten** (= §3): el mismo patrón que motivó CH-14 (Amendment v1.1 nombra un
   componente antes de que exista) y el mismo hallazgo metodológico de CH-24 (un grep de texto
   libre se contamina con la propia meta-discusión de un capítulo anterior) reaparecen aquí, una
   última vez, para una regla que ni siquiera tiene un componente que pueda nombrarse.
3. **Estructuras / reglas / incentivos** (= §8/§10): la clasificación real de los veintidós
   componentes contra `introduced_in`, y el script que calcula el índice exacto de
   `AgentCommunicationGateway` dentro de `book/book.yaml` — evidencia mecánica, no narrativa.
4. **Modelos mentales** (= §4): un principio de secuenciación se demuestra con el orden real de
   los commits y capítulos, no con una declaración de intención escrita después del hecho.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral, evitado):** cada vez que un problema nuevo apareció en este libro,
  la respuesta fue un componente nuevo sobre el mismo runtime — nunca un agente adicional. Ese
  bucle, sostenido durante veinticuatro capítulos, es lo que impidió que la complejidad
  multi-agente se acumulara como sustituto de resolver context/tools/state/reliability/governance.
- **Bucle de equilibrio (estabiliza):** Article IV (Ownership Rule), aplicado por
  `scripts/validate-chapter` a cada capítulo, exige que todo componente nuevo declare su propio
  `does_not_own` contra los ya existentes — el mismo mecanismo que, aplicado a una futura propuesta
  de orquestación multi-agente, seguiría exigiendo la pregunta de la seccion 4: ¿qué problema real
  resuelve, que ningún componente single-agent ya resuelve o podría resolver mejor?

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo — y, en cierto sentido, del libro completo — es que
la secuencia CH-00..CH-13 → CH-14..CH-24 nunca necesitó una regla explícita para producirse: surgió
de aplicar, capítulo a capítulo, la misma disciplina de Article IV (nunca absorber silenciosamente
la responsabilidad de otro dominio) a cada problema nuevo tal como apareció. `P-09` no tuvo que
imponerse desde afuera para cumplirse — se cumplió como consecuencia de que ninguna otra regla de
este libro permitía el atajo que `P-09` prohíbe.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo
> de esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set`
> (frontmatter) y es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. ¿Qué catorce capítulos reales quedaron completos y validados antes de que cualquier capítulo
   introdujera comunicación entre dos ejecuciones ya vivas, y qué capítulo rompió esa condición?
   *(cierra la pregunta guía 1)*
2. ¿Qué significaría citar honestamente una regla que ningún componente puede poseer? *(cierra la
   pregunta guía 2)*
3. ¿Qué evidencia real, no una promesa, decidiría si un componente de orquestación multi-agente
   futuro resuelve un problema real? *(cierra la pregunta guía 3)*
4. ¿Qué le pasaría a la deuda honesta de cada capítulo anterior si el libro hubiera saltado antes a
   coordinar múltiples agentes? *(cierra la pregunta guía 4)*

### Explicar

1. Este capítulo no introduce ningún componente y, sin embargo, cita `P-09` con evidencia real.
   Explica cómo es posible citar con evidencia un principio que ninguna ficha puede poseer.
2. `AgentCommunicationGateway` (CH-15) es la única pieza multi-agente de todo el libro. Explica por
   qué su posición en el capítulo 15 de 25 —no su contenido— es la evidencia real de que este libro
   cumplió `P-09`.

### Conectar

1. ¿Por qué `SkillLibrary` (CH-24) pudo cerrar `P-07` con un componente real, mientras que cerrar
   `P-09` con un componente equivalente habría sido, precisamente, el error que `P-09` prohíbe?
2. ¿Qué tuvo que ser verdad primero, `AgentCore.activateAgent` (CH-11) o
   `AgentCommunicationGateway` (CH-15), para que el segundo pudiera escribirse honestamente?
3. ¿Por qué `runAgentTurnEndToEnd` (CH-12) y las cinco funciones de CH-13 nunca invocan a
   `AgentCommunicationGateway`, y qué tendría que ser verdad primero para que una integración futura
   sí lo hiciera?
4. ¿Qué relación tiene la disciplina "no magic entities" (aplicada a pseudocódigo desde CH-00) con
   la decisión de este capítulo de no inventar un componente solo para citar `P-09`?

### Espaciar

Las cuatro tarjetas de repaso de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas de
nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) — ver `retrieval_set.flashcards` en
`dist/book-ir.json`.

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo.
