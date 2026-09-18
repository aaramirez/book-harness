---
id: CH-23
title: "HandoffCoordinator y el Paquete Estructurado que Nunca Es Solo Prosa"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-021]
introduces_contracts: [C-034]
modifies_contracts: []
constitutional_articles: [P-13, INV-E12, INV-18, INV-19, INV-20]
previous_chapter: CH-22
next_chapter: CH-24
retrieval_set:
  expected_outcome:
    id: EO-CH23
    text: |
      Al terminar este capítulo podrás distinguir, con precisión, dos preguntas que ambas
      involucran a un humano dentro de la ejecución de un agente pero pertenecen a dominios
      completamente distintos: si un humano debe resolver UNA decisión puntual dentro de un turno
      que sigue en marcha, y si el CONTROL COMPLETO de un run o de una sesión debe transferirse
      por entero a un humano. Podrás diseñar, para esa segunda pregunta, un paquete de traspaso
      cuya razón nunca se resuelve como un párrafo de prosa libre sino como un valor estructurado
      de un conjunto cerrado, y podrás explicar por qué el componente que construye ese paquete no
      debería, jamás, decidir por sí mismo cuándo debe ocurrir la transferencia que empaqueta.
  skeleton:
    id: SK-CH23
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
    components_to_be_introduced: [CMP-021]
    contracts_to_be_introduced: [C-034]
  guiding_questions:
    - id: GQ-CH23-01
      text: |
        Ya existe un componente que representa y resuelve una decisión puntual —aprobar, rechazar,
        proveer un valor— que un humano debe tomar dentro de un turno que sigue en marcha. Si en
        cambio un run completo necesita transferirse por entero a un humano porque el modelo se
        atascó, un control operacional externo lo exige, o el presupuesto se agotó, ¿es esa la
        misma pregunta formulada sobre un objeto más grande, o una pregunta de un dominio distinto
        que conviene no confundir aunque ambas involucren a un humano?
      answered_by: RQ-CH23-01
    - id: GQ-CH23-02
      text: |
        Si la razón por la que un run se transfiere por completo a un humano importa para decidir
        qué hacer después —el modelo se atascó, un control externo lo forzó, el presupuesto se
        agotó, alguien escaló explícitamente— ¿debería esa razón resumirse siempre en un párrafo de
        texto libre, o existe una forma estructurada, de un conjunto cerrado de valores, que un
        sistema futuro podría procesar sin tener que leer e interpretar prosa?
      answered_by: RQ-CH23-02
    - id: GQ-CH23-03
      text: |
        Ya existe un componente que puede forzar, desde fuera de un run y sin depender de que el
        modelo coopere, la terminación inmediata de ese run. Si esa misma señal, en vez de
        terminar el run, debiera transferir su control a un humano, ¿quién construye la
        representación de esa transferencia, y en qué momento respecto a la decisión de que la
        transferencia debía ocurrir?
      answered_by: RQ-CH23-03
    - id: GQ-CH23-04
      text: |
        Si transferir el control completo de un run a un humano es una operación distinta de
        pedirle que resuelva una sola decisión pendiente, ¿debería el componente que construye ese
        paquete de transferencia decidir, además, CUÁNDO debe ocurrir — o esa sigue siendo, igual
        que antes, una responsabilidad que pertenece a quien ya la decide hoy en otro dominio?
      answered_by: RQ-CH23-04
  systems_lens:
    iceberg_visible_fact: |
      Veintitrés capítulos reales, y `INV-E12` nunca fue citada con código real por ningún capítulo
      anterior, ni siquiera en prosa: verificado programáticamente sobre el texto íntegro de los
      veintitrés `chapter.md` anteriores, era, según el plan de ejecución de CH-22, la última regla
      de la Constitution que llegaba a este punto del libro sin ningún dueño (ver seccion 2, El
      Problema) — una premisa que la seccion 17/19 de este mismo capítulo verifica de forma
      independiente y corrige con evidencia adicional.
    iceberg_patterns: |
      El patrón que ya se repitió con `HumanInteractionService` (CH-06) reaparece aquí con una
      variante peligrosa: un componente que ya "toca" la intervención humana puede leerse, por
      comodidad, como si ya cubriera cualquier pregunta que involucre a un humano — pero
      "resolver una decisión puntual dentro de un turno en marcha" y "transferir el control
      completo de un run" son, en tamaño y en objeto, preguntas distintas, exactamente como
      `PolicyEngine` (evaluar una acción) y `EvaluationHarness` (evaluar un candidato completo,
      CH-22) ya lo fueron para la palabra "evaluar" (ver seccion 3, Por Qué la Arquitectura Actual
      No Basta).
    iceberg_structures: |
      Este capítulo instala `HandoffCoordinator` (`CMP-021`), el décimo componente de este libro
      que no corresponde a ninguno de los once nombres de Article III, con una ficha que declara
      tanto lo que posee (`owns`: construir el `HandoffPackage` estructurado que representa la
      transferencia completa de control) como lo que explícitamente NO posee (`does_not_own`:
      decidir CUÁNDO debe ocurrir esa transferencia, pedir o persistir una decisión puntual dentro
      de un turno) — y formaliza un contrato nuevo, `HandoffPackage` (`C-034`), cuyo campo `reason`
      es, deliberadamente, un `ENUM` cerrado en vez de un `Text` de prosa libre (ver seccion 8,
      Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es la lectura literal de `INV-E12`: "rather
      than only prose" no es una preferencia de estilo, es una exigencia estructural — un
      `HandoffPackage` que se redujera a un campo `summary: Text` podría, técnicamente, "cumplir"
      la letra del invariante mientras viola su espíritu por completo, exactamente el mismo riesgo
      que ya motivó `EvaluationOutcome`/`HumanInteractionOutcome` como `ENUM` de varios valores en
      vez de un campo libre (ver seccion 4, Impacto Constitucional).
    reinforcing_loop: |
      Cada vez que un componente nuevo toca, aunque sea tangencialmente, la intervención humana,
      crece la tentación de asumir que `HumanInteractionService` (CH-06) ya cubre cualquier
      pregunta futura sobre "un humano interviene aquí" — hasta que un sistema real necesita, de
      verdad, transferir el control completo de un run atascado, y descubre que
      `HumanInteractionType` no tiene ningún valor que signifique "hazte cargo de esto tú", solo
      valores que significan "resuelve esto y la ejecución continúa donde estaba".
    balancing_loop: |
      El mecanismo de equilibrio de este capítulo es estructural: `createHandoffPackage` (seccion
      11) nunca acepta invocarse sin una referencia al run/sesión que transfiere — fail-closed
      hacia `HANDOFF_PACKAGE_MISSING_RUN_ID` — y `HandoffPackage.reason` simplemente no tiene
      espacio para un párrafo libre, cerrando, con el mismo principio fail-closed que ya protegió
      la autorización desde CH-05, la evaluación de candidatos desde CH-22 y ahora también el
      traspaso a un humano.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `HandoffPackage` (`C-034`) referencie
      el estado/contexto relevante de forma completamente opaca (`contextRef: Text`) en vez de
      embeber una copia de `AgentState` o `ContextSnapshot` — y que `HandoffCoordinator` (`CMP-021`)
      no dependa de ningún componente que decida CUÁNDO ocurre un handoff. Si `HandoffCoordinator`
      hubiera absorbido esa decisión —ya que de todos modos construye el paquete—, `INV-E12` habría
      quedado satisfecho en la forma pero no en el fondo: cada control operacional futuro
      (`OperationalController`, CH-18; `ExecutionController`, CH-07; `PolicyEngine`, CH-05) habría
      tenido que conocer, de primera mano, cómo se construye un `HandoffPackage`, exactamente el
      acoplamiento que Article IV existe para prevenir.
  recall_questions:
    - id: RQ-CH23-01
      text: |
        ¿Qué componente representa y resuelve una decisión puntual dentro de un turno que sigue en
        marcha, y qué tiene que ser distinto —en tamaño y en objeto— de lo que transfiere el
        control completo de un run a un humano?
    - id: RQ-CH23-02
      text: |
        ¿Cuáles son los cuatro valores posibles de la razón estructurada de un handoff, y qué
        problema evita que ese campo sea un `Text` de prosa libre?
    - id: RQ-CH23-03
      text: |
        ¿Qué componente, ya introducido en un capítulo anterior, puede forzar la terminación de un
        run sin depender del modelo — y qué tipo de esa misma señal se usa en este capítulo como el
        ejemplo canónico de qué dispara un handoff?
    - id: RQ-CH23-04
      text: |
        ¿Qué tres decisiones —ya asignadas a componentes existentes— el componente de este
        capítulo explícita y deliberadamente no toma cuando construye un paquete de traspaso?
  explain_prompts:
    - id: EP-CH23-01
      text: |
        `HandoffCoordinator` posee construir el paquete estructurado que representa una
        transferencia de control completo. Explica, como si hablaras con alguien sin contexto
        técnico, por qué NO posee decidir CUÁNDO esa transferencia debe ocurrir — ¿qué se rompería,
        en concreto, si `HandoffCoordinator` empezara a decidir por su cuenta que un run debe
        transferirse a un humano, en vez de limitarse a empaquetar una decisión que otro componente
        ya tomó?
      target_entity: CMP-021
    - id: EP-CH23-02
      text: |
        `HandoffPackage.reason` es un `ENUM` de cuatro valores, nunca un `Text` libre. Explica qué
        información perdería un sistema futuro que necesitara decidir automáticamente, según la
        razón de un handoff, a qué equipo humano enrutarlo, si esa razón se hubiera modelado como
        una oración de prosa en vez de como un valor de un conjunto cerrado.
      target_entity: C-034
  interleaved_questions:
    - id: IQ-CH23-01
      text: |
        `HumanInteractionService` (CH-06) ya representa y resuelve una intervención humana
        identificada por `HumanInteractionRequestId`, pero esa intervención siempre ocurre DENTRO
        de un turno que sigue en marcha. `HandoffPackage.humanInteractionRef` (este capítulo)
        reutiliza ese mismo identificador de forma opcional. ¿Por qué esa reutilización es una
        correlación opcional en vez de una dependencia obligatoria, y qué seguiría siendo cierto de
        un `HandoffPackage` que nunca tuvo ninguna `HumanInteractionRequest` asociada?
      current_chapter_entities: [CMP-021, C-034]
      prior_chapter_entities: [CMP-006, C-015]
      prior_chapter: CH-06
    - id: IQ-CH23-02
      text: |
        `OperationalController` (CH-18) ya puede emitir un `ControlDirective` de tipo `KILL_SWITCH`
        que fuerza, sin depender del modelo, la terminación de un run. Este capítulo muestra ese
        mismo `ControlDirective` como la señal que dispara un `HandoffPackage`. ¿Qué campo exacto de
        `ControlDirective` se traduce en `HandoffPackage.reason = KILL_SWITCH`, y por qué construir
        el paquete a partir de esa señal no obliga a `OperationalController` a cambiar una sola
        línea de `applyControlDirective`?
      current_chapter_entities: [CMP-021, C-034]
      prior_chapter_entities: [CMP-016, C-028]
      prior_chapter: CH-18
  flashcards:
    - id: FC-CH23-01
      front: |
        ¿Qué posee `HandoffCoordinator` (Amendment v1.1, `INV-E12`), en una frase?
      back: |
        Construir, en exclusiva, el `HandoffPackage` estructurado que representa la transferencia
        COMPLETA de control de un run/sesión a un humano — cita literal de `INV-E12`: "a human
        handoff transfers a structured HandoffPackage rather than only prose".
      source_entity: CMP-021
      chapter_introduced_in: CH-23
      review_stage: DAY_1
    - id: FC-CH23-02
      front: |
        ¿Qué NO posee `HandoffCoordinator`, y a qué componentes pertenecen esas decisiones?
      back: |
        Pedir o persistir una decisión puntual dentro de un turno en marcha
        (`HumanInteractionService`, CH-06 — la frontera más importante); decidir CUÁNDO debe
        ocurrir un handoff (`OperationalController` vía kill switch, CH-18; `ExecutionController`
        vía terminación, CH-07; o `PolicyEngine`, CH-05); ejecutar cualquier acción una vez que el
        humano toma control (Preview, fuera de alcance).
      source_entity: CMP-021
      chapter_introduced_in: CH-23
      review_stage: DAY_1
    - id: FC-CH23-03
      front: |
        ¿Qué campos tiene `HandoffPackage` (`C-034`)?
      back: |
        `id` (`HandoffPackageId`), `runId`/`sessionId` (identificadores ya existentes, CH-00),
        `reason` (`HandoffReason` — `ENUM` de cuatro valores:
        `MODEL_STUCK`/`KILL_SWITCH`/`BUDGET_EXHAUSTED`/`EXPLICIT_ESCALATION`), `contextRef`
        (`Text` opaco al `AgentState`/`ContextSnapshot` relevante, sin duplicar su contenido),
        `transferTo` (`ActorId`, reusado de CH-06), `humanInteractionRef`
        (`Optional<HumanInteractionRequestId>`, correlación opcional reusada de CH-06), `status`
        (`HandoffStatus` — `ENUM` de tres valores: `PENDING`/`ACCEPTED`/`COMPLETED`, nunca un
        `Boolean`) y `createdAt` (`Timestamp`).
      source_entity: C-034
      chapter_introduced_in: CH-23
      review_stage: DAY_1
    - id: FC-CH23-04
      front: |
        ¿Por qué `HandoffPackage.reason` es un `ENUM` de cuatro valores en vez de un `Text` libre, y
        por qué `status` nunca es un `Boolean`?
      back: |
        `INV-E12` exige literalmente "rather than only prose" — un `Text` libre habría "cumplido"
        la letra sin cumplir el espíritu del invariante. Un `Boolean` en `status` solo podría
        representar "pendiente/no pendiente", perdiendo el estado intermedio `ACCEPTED` (un humano
        ya tomó el control, pero todavía no terminó de actuar) — el mismo argumento que ya protegió
        `EvaluationOutcome` (CH-22) y `HumanInteractionOutcome` (CH-06).
      source_entity: C-034
      chapter_introduced_in: CH-23
      review_stage: DAY_1
    - id: FC-CH23-05
      front: |
        ¿Qué `ControlDirective` (`C-028`, CH-18) se usa en este capítulo como el ejemplo canónico de
        qué dispara un handoff, y qué relación real existe entre ambos componentes tras este
        capítulo?
      back: |
        `ControlDirective` con `type = KILL_SWITCH` — la señal que, en el ejemplo de la seccion 11,
        se traduce en `HandoffPackage.reason = KILL_SWITCH`. Ninguna relación real: `createHandoffPackage`
        recibe `reason` ya resuelto como parámetro; `OperationalController.applyControlDirective`
        (CH-18) no invoca `createHandoffPackage`, ni cambia una sola línea para que este capítulo
        sea correcto — el cableado real es, deliberadamente, deuda de un capítulo de integración
        futuro (seccion 9/18).
      source_entity: CMP-021
      chapter_introduced_in: CH-23
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH23-01
      recall_question: RQ-CH23-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH23-02
      recall_question: RQ-CH23-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH23-03
      recall_question: RQ-CH23-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH23-04
      recall_question: RQ-CH23-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 23 — HandoffCoordinator y el Paquete Estructurado que Nunca Es Solo Prosa

> **Regla constitucional (Amendment v1.1, `INV-E12`):** "A human handoff transfers a structured
> `HandoffPackage` rather than only prose."

CH-22 cerró `P-28`, `P-29` e `INV-E13` — las últimas tres reglas de Amendment v1.1 que ningún
capítulo anterior había citado con código real — y documentó, explícitamente en su propia sección 18
y en su plan de ejecución, un hallazgo no anticipado por su propio encargo: `INV-E12` ("A human
handoff transfers a structured HandoffPackage rather than only prose") queda, tras CH-22, como la
regla que su plan de ejecución identificó como la única de la Constitution que ningún capítulo de
este libro había citado nunca, ni con código ni en prosa. Un barrido programático propio, ejecutado
antes de escribir una sola línea de este capítulo (`grep` sobre `constitutional_articles` de los
veintitrés `chapter.md` anteriores, más un barrido de texto completo para descartar una cita
únicamente en prosa), confirma que `INV-E12` en particular sigue sin ninguna cita fuera de la
transcripción íntegra de Amendment v1.1 en CH-00 §5 — pero, como se documenta con evidencia completa
en la seccion 17/19 de este mismo capítulo, un barrido más amplio sobre las sesenta y cuatro reglas
completas revela que la premisa de EXCLUSIVIDAD heredada de CH-22 ("`INV-E12` es la única") no era
del todo exacta: dos principios más quedan en la misma situación, sin que este capítulo expanda su
alcance ya decidido para resolverlos.

Este capítulo, el vigesimocuarto capítulo real de contenido de este libro, cierra la pieza que
motivó su encargo — `INV-E12` — y documenta, con la misma honestidad de cobertura que ya aplicó
CH-22, lo que ese cierre no alcanza a completar.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de saber
> cómo se llama el componente de este capítulo. El detalle estructurado de esta sección vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, con precisión, dos preguntas
que ambas involucran a un humano dentro de la ejecución de un agente pero pertenecen a dominios
completamente distintos: si un humano debe resolver UNA decisión puntual dentro de un turno que
sigue en marcha, y si el CONTROL COMPLETO de un run o de una sesión debe transferirse por entero a
un humano. Podrás diseñar, para esa segunda pregunta, un paquete de traspaso cuya razón nunca se
resuelve como un párrafo de prosa libre sino como un valor estructurado de un conjunto cerrado, y
podrás explicar por qué el componente que construye ese paquete no debería, jamás, decidir por sí
mismo cuándo debe ocurrir la transferencia que empaqueta.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e introduce
un contrato de datos nuevo y el décimo componente de este libro que no corresponde a ninguno de los
once nombres originales de Article III.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar atrás;
están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este capítulo va
a definir):

1. Ya existe un componente que representa y resuelve una decisión puntual —aprobar, rechazar,
   proveer un valor— que un humano debe tomar dentro de un turno que sigue en marcha. Si en cambio
   un run completo necesita transferirse por entero a un humano porque el modelo se atascó, un
   control operacional externo lo exige, o el presupuesto se agotó, ¿es esa la misma pregunta
   formulada sobre un objeto más grande, o una pregunta de un dominio distinto?
2. Si la razón por la que un run se transfiere por completo a un humano importa para decidir qué
   hacer después, ¿debería esa razón resumirse siempre en un párrafo de texto libre, o existe una
   forma estructurada que un sistema futuro podría procesar sin tener que interpretar prosa?
3. Ya existe un componente que puede forzar, desde fuera de un run, la terminación inmediata de ese
   run sin depender de que el modelo coopere. Si esa misma señal, en vez de terminar el run,
   debiera transferir su control a un humano, ¿quién construye la representación de esa
   transferencia, y en qué momento respecto a la decisión de que debía ocurrir?
4. Si transferir el control completo de un run es una operación distinta de pedirle a un humano que
   resuelva una sola decisión pendiente, ¿debería el componente que construye ese paquete decidir,
   además, CUÁNDO debe ocurrir la transferencia?

## 1. Arquitectura Actual (Current Architecture)

CH-00..CH-22 dejaron instalados treinta y tres contratos de datos y veinte componentes: los once
nombres completos de Article III ("Agent Runtime"), dos capítulos de integración, y nueve
componentes de Amendment v1.1 (`AdmissionController`, CMP-012, CH-14; `AgentCommunicationGateway`,
CMP-013, CH-15; `CredentialBroker`, CMP-014, CH-16; `IdempotencyGuard`, CMP-015, CH-17;
`OperationalController`, CMP-016, CH-18; `AuditLedger`, CMP-017, CH-19; `DataGovernanceEngine`,
CMP-018, CH-20; `ExecutionFabricAdapter`, CMP-019, CH-21; `EvaluationHarness`, CMP-020, CH-22).

`HumanInteractionService` (CMP-006, CH-06) es, de los veinte, el único que representa, persiste y
resuelve una intervención humana concreta. Su contrato de solicitud, `HumanInteractionRequest`
(C-015, CH-06 §6), modela exactamente cuatro tipos posibles —`HumanInteractionType`:
`Approval`/`Input`/`Review`/`Decision`, cita literal de Article VIII— y su contrato de resolución,
`HumanInteractionResolution` (C-016, CH-06 §6), modela un resultado de tres estados
(`Approved`/`Rejected`/`Provided`). Los cuatro tipos comparten una premisa que CH-06 nunca tuvo
motivo para cuestionar: cada uno resuelve UNA pregunta puntual —¿se aprueba esto? ¿cuál es este
valor? ¿se revisó esto? ¿cuál de estas opciones?— formulada siempre DENTRO de un turno que, salvo
la propia espera, sigue existiendo y sigue siendo capaz de reanudarse exactamente donde se detuvo
(CH-06 §9, tabla de relaciones futuras con `AgentLoop`). Ninguno de los cuatro tipos, ni la
resolución que los cierra, representa jamás "deja de intentar que este run continúe donde estaba;
transfiérele el control completo a un humano".

`OperationalController` (CMP-016, CH-18) es, de los veinte, el único que puede forzar, desde AFUERA
de un `AgentRun` y sin depender de que el modelo coopere, la terminación inmediata de ese run. Su
contrato, `ControlDirective` (C-028, CH-18 §6), modela cuatro tipos —`ControlDirectiveType`:
`DISABLE_CAPABILITY`/`ISOLATE_TENANT`/`ROLLBACK`/`KILL_SWITCH`, cita literal de `P-30`— y, cuando
`type = KILL_SWITCH`, `applyControlDirective` (CH-18 §11) escribe directamente un `AgentState` (C-003)
nuevo con `status = CANCELLED` — la primera y única vez, hasta este capítulo, en que un componente
distinto de `AgentLoop` transiciona `AgentRunStatus`. Un kill switch, tal como CH-18 lo construyó,
siempre TERMINA un run; nunca lo TRANSFIERE. Un run cancelado no tiene, en ningún contrato de este
libro hasta ahora, ninguna representación de "y ahora un humano debe hacerse cargo de lo que quedó
pendiente" — simplemente deja de existir como ejecución activa.

`INV-E12` ("A human handoff transfers a structured HandoffPackage rather than only prose") fue
transcrita, junto con el resto de Amendment v1.1, en CH-00 §5 — pero ningún capítulo posterior la
citó nunca en su propia sección de Impacto Constitucional, ni en prosa, ni construyó ningún mecanismo
real que la materializara. Ningún contrato de este libro, hasta este capítulo, modela la
transferencia del control completo de un run o de una sesión hacia un humano.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas para esto, "un humano interviene aquí" tiende a
colapsarse, silenciosamente, en dos suposiciones igual de incompletas. La primera: que si
`HumanInteractionService` (CH-06) ya representa y resuelve una intervención humana, entonces ya
cubre, de paso, cualquier pregunta futura que involucre a un humano — pero sus cuatro tipos
(`Approval`/`Input`/`Review`/`Decision`) resuelven, todos, una pregunta puntual dentro de un turno
que sigue vivo; ninguno de los cuatro fue diseñado, ni podría reinterpretarse sin romper CH-06 §8,
para significar "el run deja de intentar continuar; un humano toma el control completo desde aquí".
La segunda: que si `OperationalController` (CH-18) ya puede forzar, con un `ControlDirective` de
tipo `KILL_SWITCH`, la terminación de un run atascado, entonces ese mismo mecanismo ya resuelve el
problema del handoff — pero un `KILL_SWITCH` aplicado, tal como CH-18 §11 lo construyó, transiciona
`AgentRunStatus` a `CANCELLED` y ahí termina: ningún humano recibe, después de esa cancelación,
ninguna representación estructurada de por qué se canceló, qué estado quedó pendiente, o a quién le
corresponde hacerse cargo.

Hay una segunda dimensión del problema, la que da nombre literal a `INV-E12`: incluso si alguna
implementación decidiera, por su cuenta, construir ALGO para representar un traspaso, nada le
impide reducir ese algo a un campo de texto libre — un `summary: Text` con un párrafo describiendo
la situación. Eso "cumpliría", en un sentido superficial, con la idea de "avisarle a un humano" —
pero violaría exactamente lo que `INV-E12` prohíbe explícitamente: "rather than only prose". Un
párrafo de prosa no puede enrutarse automáticamente según su causa, no puede correlacionarse de
forma consultable con el run que describe, y obliga a cada humano que lo recibe a leerlo
completo, cada vez, para entender qué pasó — exactamente el mismo riesgo que ya evitaron
`EvaluationOutcome` (CH-22) y `HumanInteractionOutcome` (CH-06) al modelarse como `ENUM` en vez de
como texto descriptivo.

Necesitamos que "empaquetar, de forma estructurada, la transferencia del control completo de un
run/sesión a un humano" tenga, por fin, un dueño único y nombrado — que ese dueño nunca decida por
sí mismo si un handoff debe ocurrir (esa señal ya la produce, en distintos momentos, `PolicyEngine`,
`ExecutionController` u `OperationalController`), que nunca absorba la representación de una
decisión puntual dentro de un turno que sigue vivo (`HumanInteractionService`, CH-06), y que
construya un paquete cuya razón sea siempre un valor de un conjunto cerrado, nunca un resumen de
texto libre.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los treinta y tres contratos y los veinte componentes que existen hasta este punto no bastan
porque:

- `HumanInteractionType` (C-015, CH-06 §6) tiene, deliberadamente, cuatro valores —
  `Approval`/`Input`/`Review`/`Decision`— y ninguno de los cuatro representa "asumir el control
  completo de la ejecución"; agregar un quinto valor con ese significado rompería la premisa de
  CH-06 §9, que asume siempre que, tras resolverse una `HumanInteractionRequest`, el mismo turno
  puede reanudarse exactamente donde se detuvo — una transferencia de control completo no reanuda
  nada, transfiere el destino de la ejecución;
- `ControlDirective` (C-028, CH-18 §6) con `type = KILL_SWITCH` transiciona `AgentRunStatus` hacia
  `CANCELLED` (CH-18 §11/§12) — un estado terminal del que, por diseño de CH-01 §12, ningún run
  vuelve a salir; ese mecanismo termina la ejecución, pero no representa, en ningún campo de
  `ControlDirective`, ni a quién se transfiere el control, ni qué contexto necesitaría ver ese
  humano, ni en qué estado quedó el traspaso mismo;
- ningún contrato de este libro modela, todavía, una razón de traspaso como un valor estructurado
  de un conjunto cerrado — ni `HarnessError.category` (CH-00, categorías de fallo, no de traspaso)
  ni `PolicyDecision.reason` (CH-05, `Optional<Text>`, deliberadamente libre para una denegación
  puntual) sirven para ese propósito sin conflacionar dominios distintos;
- ningún contrato de este libro referencia, de forma opaca y sin duplicar su contenido, el
  `AgentState`/`ContextSnapshot` relevante que un humano necesitaría ver al tomar el control de un
  run — el patrón de referencia opaca (`subjectRef`, CH-19/CH-20/CH-22) existe, pero nunca se aplicó
  a este propósito específico;
- ningún componente de este libro declara, todavía, `owns` una responsabilidad que sea,
  literalmente, "empaquetar de forma estructurada la transferencia de control completo a un humano"
  en vez de "representar y resolver una decisión puntual" (`HumanInteractionService`, CH-06) o
  "forzar la terminación de un run" (`OperationalController`, CH-18) — las dos categorías más
  cercanas que este libro ya cubrió, dejando a `INV-E12` sin dueño propio hasta este capítulo.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la secuencia
> `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una entidad que no
> haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT` registrado — **no
> magic entities**. Este capítulo aplica la misma disciplina que CH-00..CH-22 ya establecieron.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-13   Authorization is deterministic and external to the LLM.
           El mismo argumento que ya protegió la autorización desde CH-01/CH-05, la certificación
           de candidatos desde CH-22, se extiende aquí al empaquetado de un handoff: el modelo
           nunca decide, nunca ve y nunca constituye una fuente de verdad sobre si él mismo debe
           transferirse a control humano — createHandoffPackage (seccion 11) es completamente
           determinística y externa al LLM.

Invariants preserved
    INV-18    Toda acción significativa produce un evento observable.
              createHandoffPackage (seccion 11) emite un AgentEvent condicionalmente, cuando existe
              un ExecutionContext y un AgentId reales — mismo patrón exacto que CH-18..CH-22 ya
              aplicaron a sus propias funciones (ver seccion 14).
    INV-19    Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy relevante.
              HandoffPackage.transferTo (ActorId, reusado de CH-06 §6) identifica a quién se
              transfiere el control — la trazabilidad de INV-19 se satisface, además, a través del
              traceId que el AgentEvent condicional ya transporta cuando existe.
    INV-20    Todo error operacional pertenece a una categoría conocida.
              El único fallo real de este capítulo (seccion 13) introduce HANDOFF, una categoría
              nueva de ErrorCategory — deliberadamente NO reutiliza HUMAN_INTERACTION (CH-06, propio
              de una decisión puntual dentro de un turno) ni CONTROL (CH-18, propio de comandos
              operacionales), por la misma razón de fondo que motiva todo este capítulo: conflacionar
              un fallo de traspaso de control con el fallo de cualquier otro dominio sería la misma
              conflación de responsabilidades que Article IV prohíbe a nivel de componente, ahora
              aplicada a nivel de ErrorCategory.

Invariants newly cited with real code (first time in this book — la regla que motivó el encargo de
este capítulo)
    INV-E12   A human handoff transfers a structured HandoffPackage rather than only prose.
              Primera materialización real, con código, de este invariante — la regla que el plan de
              ejecución de CH-22 había señalado como la última de la Constitution (Article original
              más Amendment v1.1) que llegaba a este capítulo sin ninguna cita real, ni con código ni
              en prosa (una premisa que la seccion 17/19 de este capítulo corrige: P-07 y P-09 quedan
              en la misma situación, sin que esa corrección expanda el alcance decidido para este
              capítulo). HandoffPackage (seccion 6/7) y HandoffCoordinator (seccion 8) producen, por
              fin, el paquete estructurado que la regla exige — con reason: HandoffReason (ENUM
              cerrado de cuatro valores) en vez de cualquier campo de texto libre, cerrando por
              diseño de contrato, no por convención, la posibilidad de que un capítulo futuro reduzca
              un handoff a un resumen de prosa.

Component ownership changes
    CMP-021 HandoffCoordinator se introduce — registry/components.yaml pasa de 20 a 21 componentes.
    Es el décimo componente de este registry que NO corresponde a ninguno de los once nombres del
    árbol de Article III ("Agent Runtime"). registry/components.yaml de CMP-006
    (HumanInteractionService), CMP-005 (PolicyEngine), CMP-007 (ExecutionController) y CMP-016
    (OperationalController) NO se modifica: ninguno cablea todavía su relación real con
    HandoffCoordinator (ver seccion 9/18).

Lifecycle changes
    Ninguna modificación a AgentRunStatus (C-013) ni a HumanInteractionStatus (CH-06): ambos
    siguen, sin cambios, exactamente como sus capítulos los dejaron. Este capítulo sí introduce el
    lifecycle propio de HandoffPackage (PENDING → ACCEPTED → COMPLETED, seccion 12) — de tres
    estados, más largo que el de dos estados de HumanInteractionRequest (CH-06), porque un traspaso
    de control tiene un estado intermedio real ("un humano ya tomó el control, pero todavía no
    terminó de actuar") que una simple aprobación/rechazo no necesita.

Security implications
    HandoffCoordinator es el primer componente de este libro cuya responsabilidad completa es
    empaquetar, de forma estructurada, la transferencia del control COMPLETO de un run/sesión a un
    humano — distinta, en tamaño y en objeto, de representar una decisión puntual dentro de un
    turno que sigue vivo. Ver seccion 15 para el análisis completo, incluyendo la frontera más
    importante de este capítulo, contra HumanInteractionService.

Observability implications
    HandoffCoordinator emite AgentEvent de forma condicional desde su única función real
    (HANDOFF_PACKAGE_CREATED) — mismo patrón condicional que OperationalController (CH-18),
    DataGovernanceEngine (CH-20), ExecutionFabricAdapter (CH-21) y EvaluationHarness (CH-22).

Deterministic vs agentic boundary
    Article XII se refina una vigesimoprimera vez a nivel de componente: HandoffCoordinator, igual
    que EventBus (CH-09), OperationalController (CH-18), AuditLedger (CH-19), DataGovernanceEngine
    (CH-20), ExecutionFabricAdapter (CH-21) y EvaluationHarness (CH-22), no recibe ninguna entrada
    que el modelo haya producido — ni siquiera de forma indirecta. Empaqueta exclusivamente una
    razón ya clasificada, una referencia opaca a contexto ya resuelto, y un actor de destino ya
    determinado — todas ajenas a cualquier razonamiento del propio modelo que ese run pudiera haber
    producido antes de atascarse.
```

## 5. Conceptos Nuevos (New Concepts)

- **Human Handoff** *(cita literal, `INV-E12`, "A human handoff transfers a structured
  HandoffPackage rather than only prose")*: la transferencia del control COMPLETO de un run o de
  una sesión a un humano — nunca una decisión puntual dentro de un turno que sigue vivo. Es la
  pregunta que `HumanInteractionService` (CH-06) nunca responde, porque sus cuatro tipos asumen
  siempre que el turno se reanuda donde se detuvo.
- **Structured Handoff Reason**: la razón de un handoff, modelada como `HandoffReason` (`ENUM` de
  cuatro valores, seccion 6) — nunca un párrafo de texto libre. Es la materialización literal del
  "rather than only prose" de `INV-E12`.
- **Opaque Context Reference, aplicado a un handoff**: la referencia al `AgentState`/
  `ContextSnapshot` relevante que un humano necesitaría ver al tomar el control — modelada como
  `HandoffPackage.contextRef` (`Text` opaco, seccion 6), sin duplicar el contenido real de ninguno
  de los dos contratos.
- **Three-State Handoff Lifecycle**: el estado de un traspaso nunca se reduce a
  pendiente/resuelto — modelado como `HandoffStatus` (`ENUM` de tres valores
  `PENDING`/`ACCEPTED`/`COMPLETED`, seccion 6), donde `ACCEPTED` representa el estado intermedio en
  el que un humano ya tomó el control pero todavía no terminó de actuar.
- **Decision Ownership, aplicado por décima vez** *(Article IV)*: `HandoffCoordinator` decide
  "¿cómo se representa, de forma estructurada, la transferencia de control completo de este
  run/sesión a este humano?"; explícitamente NO decide "¿debe ocurrir esta transferencia?"
  (`OperationalController`/`ExecutionController`/`PolicyEngine`, ya resuelto, según el caso),
  "¿cómo se representa y resuelve una decisión puntual dentro de un turno que sigue vivo?"
  (`HumanInteractionService`, ya resuelto, CH-06 — la frontera más importante de este capítulo) ni
  "¿qué acción ejecuta el humano una vez que toma el control?" (Preview, fuera de alcance).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `Text`, `Timestamp`, `Optional`, `RunId`, `SessionId`,
`AgentId`, `ExecutionContext` (C-004, CH-00), `AgentEvent` (C-010, CH-00), `HarnessError` (C-011,
CH-00).

Este capítulo reutiliza, además, dos identificadores ya existentes que no son contratos completos
(`STRUCT`) sino identificadores opacos definidos dentro del `STRUCT` de otro capítulo — se declaran
aquí explícitamente, siguiendo la misma convención que CH-22 §6 ya estableció para su propia tabla:

| Identificador (reusado, no nuevo de este capítulo) | Identifica | Introducido en |
|---|---|---|
| `ActorId` | quien resuelve una intervención humana o, en este capítulo, a quién se transfiere un run/sesión (`HandoffPackage.transferTo`) | CH-06 |
| `HumanInteractionRequestId` | la solicitud de interacción humana concreta que `HandoffPackage.humanInteractionRef` referencia opacamente, cuando un handoff se correlaciona con una | CH-06 |

**Por qué `HandoffPackage.humanInteractionRef` reutiliza `HumanInteractionRequestId` en vez de
construir un mecanismo de correlación nuevo.** Se evaluó explícitamente si `HandoffCoordinator`
debería, en cambio, invocar a `HumanInteractionService` para crear una `HumanInteractionRequest` de
algún tipo nuevo que representara el handoff — y se descartó por la misma razón que motiva la
frontera completa de este capítulo (seccion 15): los cuatro tipos de `HumanInteractionType`
representan decisiones puntuales dentro de un turno que se reanuda; forzar un quinto significado
("hazte cargo de todo") dentro de ese mismo `ENUM` habría roto la premisa de CH-06 §9 de que toda
`HumanInteractionResolution` permite reanudar exactamente donde se detuvo. En su lugar,
`humanInteractionRef` es un campo `Optional` — poblado únicamente cuando, además del handoff, existe
una decisión puntual correlacionada (por ejemplo, la aprobación específica que un humano dio para
aceptar hacerse cargo) — reutilizando el identificador fuerte que `HumanInteractionService` ya
produce, en vez de agregar un campo nuevo a `HumanInteractionRequest` (CH-06) para una
responsabilidad que nunca le perteneció. Mismo patrón exacto que `BusinessOutcomeCorrelation.
humanEscalationRef` (C-033, CH-22 §6) ya estableció para un problema de forma análoga.

Este capítulo cita, además en prosa, dos contratos de capítulos anteriores sin usarlos dentro de su
propio pseudocódigo — mismo patrón de reuso explícito que CH-13 §6, CH-19..CH-22 §6 ya aplicaron:

| Contrato/tipo (reusado, no nuevo) | Introducido en | Uso en este capítulo |
|---|---|---|
| `ControlDirective` | CH-18 §6 | citado en el ejemplo de la seccion 11 como la señal canónica —`type = KILL_SWITCH`— que se traduce en `HandoffPackage.reason = KILL_SWITCH`; nunca usado dentro de la firma de `createHandoffPackage` |
| `HumanInteractionRequest` / `HumanInteractionType` | CH-06 §6 | citado en prosa (seccion 1/2/3/5/15) para trazar la frontera más importante de este capítulo — nunca usado dentro del pseudocódigo |

### Un identificador opaco nuevo

Siguiendo el mismo patrón que CH-00 §6 estableció para los identificadores fundamentales, y que
CH-14..CH-22 repitieron para los suyos:

| Identificador (nuevo de este capítulo) | Identifica |
|---|---|
| `HandoffPackageId` | un `HandoffPackage` concreto — el paquete de traspaso vigente para un run/sesión que se transfiere a control humano |

### `ErrorCategory` — extendida, sin redefinir `HarnessError`

Este es el duodécimo capítulo que agrega un valor a `ErrorCategory` desde que CH-00 lo declaró
(después de `HUMAN_INTERACTION`, CH-06; `ADMISSION`, CH-14; `DELEGATION`, CH-15; `CREDENTIAL`, CH-16;
`IDEMPOTENCY`, CH-17; `CONTROL`, CH-18; `AUDIT`, CH-19; `GOVERNANCE`, CH-20; `EXECUTION_FABRIC`,
CH-21; y `EVALUATION`, CH-22): el valor `HANDOFF`, necesario porque ninguna de las veinte categorías
ya existentes representa, sin conflación, un fallo específico de empaquetar un traspaso de control:

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
    HANDOFF
END
```

`HarnessError` (C-011) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — mismo patrón
exacto que las once extensiones anteriores, aplicado aquí por duodécima vez a `ErrorCategory`.

### `AgentEventType` — extendida, sin redefinir `AgentEvent`

CH-22 dejó `AgentEventType` en treinta y tres valores. Este capítulo agrega un valor nuevo — una
sola función real, un solo valor, mismo patrón que `ExecutionFabricAdapter` (CH-21):

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
    HANDOFF_PACKAGE_CREATED
END
```

`AgentEvent` (C-010) no cambia: solo el rango de valores permitido para `eventType` crece, igual que
en cada capítulo anterior salvo `EventBus` (CH-09), `AdmissionController` (CH-14) y
`AgentCommunicationGateway` (CH-15).

### `HandoffReason` — la razón estructurada de un handoff, nunca un párrafo de prosa

```pseudocode
ENUM HandoffReason
    MODEL_STUCK
    KILL_SWITCH
    BUDGET_EXHAUSTED
    EXPLICIT_ESCALATION
END
```

**Por qué cuatro valores cerrados, y no un `Text` libre.** Este es, literalmente, el campo que
materializa "rather than only prose" de `INV-E12`. Se evaluó explícitamente un `Text` — más flexible
para describir cualquier situación real, sin necesidad de anticipar cada causa posible— y se
descartó porque un `Text` libre satisfaría la letra de "empaquetar una razón" mientras viola el
espíritu completo del invariante: un sistema futuro que necesitara enrutar automáticamente un
handoff (por ejemplo, un `KILL_SWITCH` a un equipo de operaciones, un `BUDGET_EXHAUSTED` a un equipo
de finanzas) tendría que analizar prosa para decidir el enrutamiento, exactamente el problema que
`INV-E12` existe para prevenir. Cuatro valores, cada uno correspondiente a un disparador real que
este libro ya conoce: `MODEL_STUCK` (el modelo deja de progresar dentro de su propio turno —
disparador conceptual, sin un contrato dedicado todavía en este libro), `KILL_SWITCH`
(`ControlDirective.type = KILL_SWITCH`, `OperationalController`, CH-18 — el ejemplo canónico de la
seccion 11), `BUDGET_EXHAUSTED` (`ExecutionBudget` agotado, `ExecutionController`, CH-07) y
`EXPLICIT_ESCALATION` (un actor, humano o de gobierno, solicita el traspaso sin que medie ninguno de
los tres disparadores anteriores).

### `HandoffStatus` — el lifecycle de tres estados de un traspaso

```pseudocode
ENUM HandoffStatus
    PENDING
    ACCEPTED
    COMPLETED
END
```

**Por qué tres valores, y no dos como `HumanInteractionStatus` (`PENDING`/`RESOLVED`, CH-06).** Se
evaluó explícitamente el lifecycle de dos estados que CH-06 ya estableció para una decisión puntual
— y se descartó porque un handoff tiene un estado intermedio real que una aprobación/rechazo no
necesita: entre "el paquete existe pero nadie lo tomó" (`PENDING`) y "el humano ya terminó de
hacerse cargo" (`COMPLETED`) hay un momento legítimo, `ACCEPTED`, en el que un humano ya asumió el
control pero todavía no completó lo que sea que decida hacer con él — un run transferido puede
permanecer `ACCEPTED` durante un tiempo indeterminado antes de resolverse.

### `HandoffPackage` — el paquete estructurado que `INV-E12` exige

```pseudocode
STRUCT HandoffPackage
    id: HandoffPackageId
    runId: RunId
    sessionId: SessionId
    reason: HandoffReason
    contextRef: Text
    transferTo: ActorId
    humanInteractionRef: Optional<HumanInteractionRequestId>
    status: HandoffStatus
    createdAt: Timestamp
END
```

Nueve campos, cada uno respondiendo a una parte exacta del alcance decidido para este capítulo: `id`
identifica este paquete de forma estable; `runId`/`sessionId` son los identificadores fuertes ya
existentes desde CH-00 —mismo argumento que ya justificó `ExecutionPlacement.runId` (CH-21 §6) y
`BusinessOutcomeCorrelation.runId` (CH-22 §6): el universo de lo que este contrato describe es
siempre exactamente un run y su sesión, nunca un tipo heterogéneo de dato como `subjectRef`—; `reason`
es el `HandoffReason` de la sección anterior; `contextRef` es una referencia opaca `Text` (ver el
análisis explícito más abajo); `transferTo` es el `ActorId` (reusado de CH-06 §6) a quien se
transfiere el control; `humanInteractionRef` es `Optional<HumanInteractionRequestId>` (ver la tabla
de identificadores reusados, arriba); `status` es el `HandoffStatus` de tres estados de la sección
anterior; `createdAt` registra cuándo se produjo este paquete.

**Por qué `contextRef` es una referencia opaca `Text`, y no un campo tipado que embeba
`AgentState`/`ContextSnapshot` directamente.** Se evaluó explícitamente embeber una copia de
`AgentState` (C-003) o de `ContextSnapshot` (C-005) dentro de `HandoffPackage`, para que el humano
que recibe el paquete tuviera todo el contexto en un solo lugar sin ninguna resolución adicional — y
se descartó por dos razones. Primera: `AgentState`/`ContextSnapshot` pueden mutar o crecer
independientemente de este paquete; embeber una copia la desactualizaría en el instante en que el
run subyacente cambiara, exactamente el mismo argumento que ya motivó `EvaluationReport.subjectRef`
(CH-22) y `AuditRecord.subjectRef` (CH-19) a preferir una referencia sobre una copia. Segunda:
`HandoffCoordinator` no necesita conocer la forma interna de `AgentState` ni de `ContextSnapshot`
para cumplir su propia responsabilidad —construir el paquete—, preservando la misma independencia de
contratos que el resto de Amendment v1.1 ya exige. `contextRef` es, deliberadamente, el mismo patrón
de referencia opaca que `subjectRef` (CH-19/CH-20/CH-22), aplicado aquí a un propósito distinto:
apuntar, sin duplicar, al contexto real que un humano necesitaría consultar.

**Por qué `HandoffPackage` no tiene ningún campo de canal** (mismo argumento que `HumanInteractionRequest`,
CH-06 §6). `INV-14` ("Human Interaction nunca depende de una interfaz particular") no cita a este
capítulo directamente en `frontmatter.constitutional_articles` —`HandoffPackage` no es, en sí mismo,
una `HumanInteractionRequest`— pero el mismo principio de fondo aplica por diseño: ningún campo de
este `STRUCT` identifica si el traspaso se notificará por una TUI, un panel web, o un sistema de
alertas — esa decisión sigue perteneciendo, exactamente igual que en CH-06, a un Channel Adapter de
infraestructura de borde que este libro nunca modela como componente propio.

**Por qué `HandoffPackage` no incluye un campo `issuedBy: ActorId`** (a diferencia de
`ControlDirective.issuedBy`, CH-18 §6). El paquete no representa un comando que un actor emitió — es
la CONSECUENCIA empaquetada de una decisión que otro componente (`OperationalController`,
`ExecutionController` o `PolicyEngine`) ya tomó por su propia cuenta y con su propia trazabilidad
(`ControlDirective.issuedBy`, `PolicyDecision.callId`); duplicar ese actor dentro de `HandoffPackage`
habría reabierto, sin necesidad, la misma información que el disparador original ya preserva.

**Unchanged / Not yet introduced**: `AgentState`/`ContextSnapshot`/`ExecutionContext` (C-003/C-005/
C-004, CH-00/CH-04) no cambian de forma — ninguno gana un campo `handoffPackage` en este capítulo
(ver seccion 9/18). `HumanInteractionRequest`/`HumanInteractionResolution` (C-015/C-016, CH-06)
tampoco cambian: siguen siendo, sin excepción, el contrato exclusivo de una decisión puntual dentro
de un turno vivo. `ControlDirective` (C-028, CH-18) tampoco cambia: sigue siendo, sin excepción, el
contrato exclusivo de un comando operacional emitido desde afuera de un run.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce un contrato de
datos, registrado en `registry/contracts.yaml`:

```text
ID:                     C-034
Name:                   HandoffPackage
Version:                v1
Introduced In:          CH-23
Current Definition:     STRUCT HandoffPackage (ver §6)
Used By:                [CMP-021]
Modified By:            []
Constitutional Impact:  [INV-E12, INV-19]
```

`C-034` es el vigesimoprimer id que este libro asigna sin que estuviera reservado desde CH-01 §7 —
el correlativo simplemente continúa después de `C-033` (CH-22). No colisiona, por nombre, con
ningún contrato ya registrado — verificado con grep completo sobre `registry/contracts.yaml` antes
de escribir este capítulo.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el décimo componente del registry que no corresponde a ninguno de los once
nombres del árbol de Article III ("Agent Runtime") — pertenece, en cambio, a `INV-E12` de Amendment
v1.1:

```pseudocode
COMPONENT HandoffCoordinator
    consumes: ExecutionContext
    produces: HandoffPackage, AgentEvent, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Amendment v1.1 (`INV-E12`) — Article III no tiene,
todavía, una sección propia para este componente, exactamente igual que `AdmissionController`
(CH-14), `AgentCommunicationGateway` (CH-15), `CredentialBroker` (CH-16), `IdempotencyGuard` (CH-17),
`OperationalController` (CH-18), `AuditLedger` (CH-19), `DataGovernanceEngine` (CH-20),
`ExecutionFabricAdapter` (CH-21) y `EvaluationHarness` (CH-22):

```text
COMPONENT: HandoffCoordinator

Responsibility:
    Empaquetar un HandoffPackage estructurado cuando la decisión de transferir el control COMPLETO
    de un run/sesión a un humano ya se tomó — con campos estructurados que nunca colapsan a un
    resumen de prosa libre — sin decidir CUÁNDO debe ocurrir ese handoff, sin pedir o persistir una
    decisión puntual dentro de un turno en curso, y sin ejecutar ninguna acción una vez que el
    humano toma control.

Consumes:
    C-004 ExecutionContext (solo cuando el handoff ocurre dentro de uno real, ver seccion 11)

Depends on:
    (ninguno todavía — el cableado real hacia OperationalController/ExecutionController/PolicyEngine/
    HumanInteractionService es Preview, no introducido en este capítulo; ver seccion 9)

Produces:
    C-034 HandoffPackage (el paquete estructurado de traspaso), C-010 AgentEvent
    (HANDOFF_PACKAGE_CREATED, condicional, ver seccion 14), C-011 HarnessError

Owns (Amendment v1.1 `INV-E12`, cita y lectura literal):
    - "A human handoff transfers a structured HandoffPackage rather than only prose" (cita literal,
      INV-E12) — construir, en exclusiva, el paquete estructurado que representa la transferencia
      COMPLETA de control de un run/sesión a un humano, nunca solo un bloque de texto libre
      resumiendo la situación
    - correlacionar, opcionalmente, un HandoffPackage con una HumanInteractionRequest ya existente
      (CMP-006, CH-06) vía una referencia reusada, sin modificar ese contrato
    - rechazar por defecto (fail-closed) un HandoffPackage sin referencia al run/sesión que se
      transfiere

Does NOT own:
    - pedir o persistir una decisión puntual dentro de un turno en curso (HumanInteractionService,
      CMP-006, ya introducido en CH-06 — la frontera más importante de este capítulo:
      HumanInteractionService representa y resuelve UNA decisión puntual dentro de un turno que
      sigue en marcha; HandoffCoordinator empaqueta la transferencia del CONTROL COMPLETO de un
      run/sesión, nunca una decisión aislada dentro de él — dos preguntas que ambas involucran a un
      humano, pero nunca comparten dueño)
    - decidir CUÁNDO debe ocurrir un handoff (OperationalController, CMP-016, ya introducido en
      CH-18, vía un kill switch; ExecutionController, CMP-007, ya introducido en CH-07, vía
      terminación por presupuesto; o PolicyEngine, CMP-005, ya introducido en CH-05 —
      HandoffCoordinator construye el paquete UNA VEZ que esa decisión ya se tomó, asumida como una
      señal de entrada, nunca antes)
    - ejecutar cualquier acción una vez que el humano toma control del run/sesión transferido
      (Preview, infraestructura de borde — este componente decide la FORMA del paquete, nunca lo
      que ocurre después de que un humano lo acepta)
    - transportar el HandoffPackage a través de ningún canal concreto (Channel Adapter, concepto de
      infraestructura de borde ya declarado por HumanInteractionService, CH-06 — no un componente
      propio de Article III / del registry)
    - generar por sí mismo el runId, el sessionId, la reason, el contextRef o el transferTo — todas
      llegan como señales de entrada ya resueltas (mismo patrón que subjectRef en CH-19/CH-20/CH-22,
      o runId/topology en CH-21)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con la misma
particularidad que los nueve componentes de Amendment v1.1 anteriores: ninguna de las cinco
exclusiones proviene de una ficha propia de Article III (que no existe para este componente);
provienen de fronteras ya establecidas por componentes ya registrados. La primera exclusión de esta
lista es, deliberadamente, la más parecida en prosa informal a lo que este componente sí posee — el
mismo cuidado editorial que CH-04 §8, CH-19..CH-22 §8 ya aplicaron frente a su propia frontera más
importante.

**Nota sobre Article IV.** Igual que `DataGovernanceEngine` (CH-20), `ExecutionFabricAdapter`
(CH-21) o `EvaluationHarness` (CH-22), `HandoffCoordinator` sí decide algo real —la forma estructurada
del paquete, y si correlacionarlo opcionalmente con una `HumanInteractionRequest` existente— y no
comparte la ausencia de fila de `EventBus` (CH-09) o `AuditLedger` (CH-19), que solo preservan o
distribuyen decisiones ajenas.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
HandoffCoordinator
    consumes → ExecutionContext
    produces → HandoffPackage, AgentEvent, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`HandoffCoordinator` no depende hoy de ningún otro componente registrado — mismo patrón que
CH-01..CH-22 ya establecieron para sus propios componentes. En prosa (nunca dentro de un bloque
`pseudocode`, per `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las relaciones
futuras que un capítulo de integración agregaría son:

| Componente futuro (relación inversa — no cableada en este capítulo) | Qué relación tendría con `HandoffCoordinator` |
|---|---|
| `OperationalController` (ya existente, CMP-016) | `applyControlDirective` (CH-18 §11), al aplicar un `ControlDirective` con `type = KILL_SWITCH`, podría invocar `createHandoffPackage` con `reason = KILL_SWITCH` en vez de (o además de) transicionar el run a `CANCELLED` — sin que `ControlDirective` como contrato cambie una sola línea |
| `ExecutionController` (ya existente, CMP-007) | `evaluateExecutionContinuation` (CH-07 §11), al detectar que `ExecutionBudget` se agotó, podría invocar `createHandoffPackage` con `reason = BUDGET_EXHAUSTED` en vez de simplemente detener el run |
| `PolicyEngine` (ya existente, CMP-005) | permanecería, en su mayor parte, sin relación directa: `evaluatePolicyForToolCall` sigue evaluando exclusivamente acciones dentro de runs que ya existen — salvo que una policy explícita decida que una `REQUIRE_APPROVAL` reiterada sin resolución constituye, en la práctica, un `EXPLICIT_ESCALATION` |
| `HumanInteractionService` (ya existente, CMP-006) | una `HumanInteractionRequest` de tipo `Approval` que un humano resuelve como "acepto hacerme cargo de este run" podría poblar `HandoffPackage.humanInteractionRef`, correlacionando ambos contratos sin que ninguno de los dos cambie su forma |
| `AgentLoop` / `SessionManager` (ya existentes, CMP-001/CMP-010) | resolverían, en la práctica, el `contextRef` opaco que este capítulo asume ya resuelto — sin que `createHandoffPackage` necesite conocer cómo se construye esa referencia |
| `EventBus` (ya existente, CMP-009) | podría distribuir, como un `AgentEvent` más, `HANDOFF_PACKAGE_CREATED` (seccion 14) — exactamente igual que distribuye el de cualquier otro productor |

`registry/components.yaml` de `CMP-005`, `CMP-006`, `CMP-007` y `CMP-016` **no se modifica** en este
capítulo: ninguno agrega `CMP-021` a sus `dependencies`, y ninguno cambia su pseudocódigo. El
pseudocódigo de la seccion 11 muestra a `HandoffCoordinator` empaquetando un traspaso de forma
completamente autónoma — sin que ningún componente anterior cambie una sola línea para que este
capítulo sea correcto. Ese cableado real de punta a punta es, explícitamente, trabajo de un capítulo
de integración futuro (ver seccion 18/19).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[OperationalController — CH-18, conceptual, todavía no cablea esta llamada] → HandoffCoordinator →
[HandoffPackage — el paquete estructurado, consultable por cualquier componente futuro vía runId] →
[Channel Adapter — concepto, no componente] → Human
```

**Vista 2 — Sequence**

```text
ControlDirective (type = KILL_SWITCH, status = APPLIED — producido de forma autónoma por
OperationalController, CH-18 — este capítulo no cablea esa llamada)
   │
   ▼
HandoffCoordinator
   │ createHandoffPackage(runId, sessionId, reason = KILL_SWITCH, contextRef, transferTo,
   │   humanInteractionRef, execution, agentId)
   │ ¿runId ausente? sí → HarnessError (HANDOFF_PACKAGE_MISSING_RUN_ID)
   │ construye HandoffPackage (id, runId, sessionId, reason, contextRef, transferTo,
   │   humanInteractionRef, status = PENDING, createdAt)
   │ ¿execution y agentId ambos resueltos? sí → emite: AgentEvent (HANDOFF_PACKAGE_CREATED)
   ▼
HandoffPackage (PENDING — el paquete de traspaso vigente para este runId)
   │
   ▼
[Channel Adapter — concepto, no componente — transportaría el paquete hacia un humano, mismo
concepto de infraestructura de borde que HumanInteractionService (CH-06) ya declaró fuera del árbol
de componentes]
   │
   ▼
Human
   │ ... acepta el control (HandoffPackage.status → ACCEPTED) y, más tarde, termina de actuar
   │     (HandoffPackage.status → COMPLETED) — ninguna de las dos transiciones se cablea en este
   │     capítulo (Preview, ver seccion 12/18) ...
```

**Vista 3 — Pseudocódigo**

Ver §11: `createHandoffPackage` es la primera formalización ejecutable de "a human handoff transfers
a structured HandoffPackage rather than only prose" (`INV-E12`) — construida exclusivamente a partir
de material que ya existe (`ExecutionContext`/`AgentEvent`/`HarnessError`/`RunId`/`SessionId`/
`ActorId`/`HumanInteractionRequestId` desde CH-00/CH-06) más los `ENUM`/`STRUCT` nuevos de este
capítulo.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde
CH-00/CH-06/CH-18.

```pseudocode
FUNCTION createHandoffPackage(
    runId: RunId,
    sessionId: SessionId,
    reason: HandoffReason,
    contextRef: Text,
    transferTo: ActorId,
    humanInteractionRef: Optional<HumanInteractionRequestId>,
    execution: Optional<ExecutionContext>,
    agentId: Optional<AgentId>
) -> HandoffPackage

    IF runId == NULL
        missingRunId: HarnessError = HarnessError(
            category = HANDOFF,
            code = "HANDOFF_PACKAGE_MISSING_RUN_ID",
            message = "createHandoffPackage fue invocada sin una referencia al run/sesión que se transfiere — un HandoffPackage nunca puede escribirse sin saber qué se transfiere",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW missingRunId
    END

    package: HandoffPackage = HandoffPackage(
        id = newHandoffPackageId(),
        runId = runId,
        sessionId = sessionId,
        reason = reason,
        contextRef = contextRef,
        transferTo = transferTo,
        humanInteractionRef = humanInteractionRef,
        status = PENDING,
        createdAt = now()
    )

    IF execution != NULL AND agentId != NULL
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = HANDOFF_PACKAGE_CREATED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = package
        )
    END

    RETURN package
END
```

`now()`, `newEventId()` son las mismas primitivas de CH-00..CH-22. `newHandoffPackageId()` sigue el
mismo patrón que `newEvaluationReportId()` (CH-22) o `newExecutionPlacementId()` (CH-21). `reason`,
`contextRef` y `transferTo` llegan como parámetros ya resueltos por quien invoca esta función — este
capítulo modela la FORMA del paquete, no el mecanismo real que decide que un handoff debe ocurrir ni
el que resuelve, en la práctica, la referencia de contexto.

**Por qué `status` siempre nace en `PENDING`, nunca en otro valor.** `createHandoffPackage` nunca
acepta un `status` como parámetro — el paquete siempre nace pendiente de que un humano lo acepte;
las transiciones hacia `ACCEPTED`/`COMPLETED` son, deliberadamente, Preview (seccion 12/18), igual
que `HumanInteractionRequest.status` (CH-06) siempre nace en `PENDING`.

**Ejemplo — construyendo los argumentos a partir de un `ControlDirective` de tipo `KILL_SWITCH`
(CH-18).** No es una función nueva: muestra cómo un llamador futuro (`OperationalController`,
todavía sin cablear esta llamada, ver seccion 9) traduciría un `ControlDirective` ya aplicado hacia
los argumentos de `createHandoffPackage`:

```pseudocode
// directive: ControlDirective ya aplicado por OperationalController (CH-18 §11)
//   directive.type       = KILL_SWITCH
//   directive.targetRef  = "run-4471"   (un RunId, opaco dentro de ControlDirective — CH-18 §6)
//   directive.issuedBy   = actorGovernanceBot
//   directive.status     = APPLIED

handoffPackage: HandoffPackage = createHandoffPackage(
    runId = resolveRunId(directive.targetRef),
    sessionId = resolveSessionIdForRun(resolveRunId(directive.targetRef)),
    reason = KILL_SWITCH,
    contextRef = "agentstate-ref://run-4471",
    transferTo = onCallOperator,
    humanInteractionRef = NULL,
    execution = NULL,
    agentId = NULL
)
```

`resolveRunId`/`resolveSessionIdForRun` son primitivas asumidas, no funciones de este capítulo — el
mismo tratamiento que CH-18 §11 ya dio a las primitivas de aplicación real de un `ControlDirective`.
Lo que este ejemplo demuestra es, exclusivamente, la traducción de `directive.type = KILL_SWITCH`
hacia `reason = KILL_SWITCH` — ninguna línea de `applyControlDirective` (CH-18 §11) cambia para que
este ejemplo sea correcto; **ningún componente de este libro invoca todavía, de verdad,
`createHandoffPackage`** (ver seccion 9/18).

Nótese lo que esta función **nunca hace**: no invoca `OperationalController.applyControlDirective`
(CH-18) ni `ExecutionController.evaluateExecutionContinuation` (CH-07) para decidir si el handoff
debe ocurrir — ambos parámetros (`runId`, `reason`) llegan ya resueltos; no invoca
`HumanInteractionService.createHumanInteractionRequest` (CH-06) para representar ninguna decisión
puntual — `humanInteractionRef` es, como mucho, una correlación opcional hacia una que ya existe; y
no ejecuta ninguna acción sobre el run transferido — construir y devolver el `HandoffPackage` es la
totalidad de lo que esta función hace.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no modifica `AgentRunStatus` (C-013) ni `HumanInteractionStatus` (CH-06): ambos siguen
siendo, sin cambios, exactamente lo que sus propios capítulos dejaron.

`HandoffPackage.status` (`HandoffStatus`, seccion 6) sí introduce un lifecycle propio de tres
estados:

```text
(HandoffPackage recién producido para un runId)
   → createHandoffPackage(...)
     RETURN HandoffPackage con status = PENDING — el único valor que esta función puede producir

(un humano acepta hacerse cargo del run/sesión transferido)
   → PENDING → ACCEPTED
     (transición no cableada por ninguna función de este capítulo — Preview, ver seccion 18)

(el humano termina de actuar sobre el run/sesión que aceptó)
   → ACCEPTED → COMPLETED
     (transición no cableada por ninguna función de este capítulo — Preview, ver seccion 18)
```

**Por qué este capítulo declara el `ENUM` completo de tres estados pero solo produce, en la
práctica, el primero.** Mismo tratamiento editorial que `HumanInteractionStatus` (CH-06 §12) dio a
`PENDING`/`RESOLVED` cuando `resolveHumanInteractionRequest` (CH-06 §11) sí cableaba ambos: aquí la
diferencia es deliberada — declarar los tres valores desde ahora evita que un capítulo de
integración futuro tenga que romper este contrato (`C-034`) para agregar `ACCEPTED`/`COMPLETED` más
tarde; construir las funciones reales que efectivamente transicionan un `HandoffPackage` existente
—`acceptHandoff`, `completeHandoff`, o como se llamen— es, explícitamente, trabajo de ese capítulo
futuro, exactamente el mismo tipo de deuda intencional que `ExecutionPlacement` (CH-21 §12) y
`EvaluationReport` (CH-22 §12) ya dejaron para sus propios registros.

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6, extendido en la seccion 6 de este capítulo) clasifica también
el único fallo real que introduce este capítulo:

```text
HANDOFF
    HANDOFF_PACKAGE_MISSING_RUN_ID          — createHandoffPackage fue invocada sin una referencia
                                                al run/sesión que se transfiere
        → recoverable: FALSE, retryable: FALSE
```

El único fallo de este capítulo es `recoverable = FALSE` y `retryable = FALSE`: representa un uso
incorrecto de la propia invocación (una referencia obligatoria faltante) — no se corrige
reintentando la misma operación tal cual, sino corrigiendo lo que se le provee. Un solo código, una
sola función real — mismo patrón que `ExecutionFabricAdapter` (CH-21 §13) ya aplicó cuando un
capítulo introduce exactamente una función real con exactamente una referencia obligatoria propia.

**La distinción más importante de esta sección**: este fallo no se clasifica como
`HUMAN_INTERACTION` (CH-06, propio de una decisión puntual dentro de un turno) ni como `CONTROL`
(CH-18, propio de un comando operacional ya emitido) — aunque, en prosa informal, "empaquetar un
traspaso a un humano" pueda sonar a cualquiera de los dos dominios, la diferencia no es la forma del
fallo, es su naturaleza: `HANDOFF_PACKAGE_MISSING_RUN_ID` es un error de uso de la propia función de
este capítulo, nunca una `HumanInteractionResolution` inválida ni un `ControlDirective` mal formado
— ese segundo y tercer tipo de fallo siguen siendo, sin ambigüedad, `HUMAN_INTERACTION` y `CONTROL`
respectivamente, exactamente como lo eran antes de este capítulo. El mismo argumento que ya usaron
CH-19 §13, CH-20 §13, CH-21 §13 y CH-22 §13 contra sus propios pares de categorías vecinas.

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo real de la resolución de
`contextRef` —un `AgentState`/`ContextSnapshot` que ya no existe, una referencia que apunta a un run
que nunca se transfirió— sigue, después de este capítulo, sin que `HandoffCoordinator` lo ejercite
nunca (mismo límite que CH-14..CH-22 ya documentaron para sus propias primitivas asumidas). Tampoco
clasifica ningún fallo de las transiciones `ACCEPTED`/`COMPLETED` que la seccion 12 deja como Preview.

## 14. Eventos Producidos (Events Produced)

`HandoffCoordinator` emite `AgentEvent` de forma condicional desde su única función real, agregando
`HANDOFF_PACKAGE_CREATED` a `AgentEventType` (seccion 6), emitido únicamente cuando `execution` y
`agentId` llegan ambos resueltos (mismo patrón condicional que `OperationalController`, CH-18,
`DataGovernanceEngine`, CH-20, `ExecutionFabricAdapter`, CH-21, y `EvaluationHarness`, CH-22).

**Por qué la emisión es condicional.** Mismo argumento que `EvaluationHarness` (CH-22 §14): un
`AgentEvent` (C-010) exige `runId`/`sessionId`/`agentId`/`traceId` genuinos, y no todo handoff ocurre
necesariamente dentro de un `ExecutionContext` con esos cuatro campos ya resueltos en el instante
exacto en que se construye el paquete.

**Por qué, incluso cuando emite, este evento no es evidencia de auditoría — frontera explícita con
`AuditLedger` (CH-19).** `payload = package` transporta una copia del paquete ya producido — pero,
exactamente igual que `EVALUATION_REPORT_PRODUCED` (CH-22 §14), queda sujeto a las mismas garantías
(o ausencia de garantías) que cualquier otro `AgentEvent`: `EventBus` podría distribuirlo, perderlo
si nadie está suscrito, o nunca llegar a existir si `execution`/`agentId` no estaban resueltos. Si
alguien necesitara, en cambio, evidencia estructuralmente inmutable de que un handoff concreto
ocurrió, esa es, sin ambigüedad, una responsabilidad de `AuditLedger` (CH-19) — nunca de este evento
condicional (ver seccion 15).

**Por qué esto no es una limitación real hacia `INV-18`.** La acción verdaderamente significativa de
este capítulo —producir un `HandoffPackage` vigente para un run/sesión— ya se cumple con el `RETURN`
directo de `createHandoffPackage` a quien la invoca, sin depender de `AgentEvent`/`EventBus` para
"existir". El `AgentEvent` condicional es, aquí, una conveniencia de observabilidad adicional, nunca
el mecanismo que hace el resultado real.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

`HandoffCoordinator` es el primer componente de este libro cuya responsabilidad completa es
empaquetar, de forma estructurada, la transferencia del control COMPLETO de un run/sesión a un
humano.

**La distinción con `HumanInteractionService` (CH-06), explícita, completa y la más importante de
este capítulo.** `HumanInteractionService.createHumanInteractionRequest`/
`resolveHumanInteractionRequest` (CH-06) representan y resuelven UNA decisión puntual —aprobar,
rechazar, proveer un valor, revisar algo— dentro de un turno que, salvo la propia espera, sigue vivo
y se reanuda exactamente donde se detuvo. `HandoffCoordinator.createHandoffPackage` (este capítulo)
empaqueta la transferencia del CONTROL COMPLETO de un run o de una sesión — una operación que no
reanuda nada donde estaba: el destino de la ejecución cambia por completo, hacia un humano que ahora
decide qué hacer con lo que recibió. Las dos preguntas son, literalmente, independientes: un run
puede, en teoría, pasar por múltiples `HumanInteractionRequest` resueltas —cada una aprobando una
acción puntual— sin que ninguna de ellas constituya jamás un handoff; y, a la inversa, un
`HandoffPackage` puede construirse sin que exista ninguna `HumanInteractionRequest` previa —un
`KILL_SWITCH` puede dispararse sobre un run que nunca pidió ninguna aprobación—. Si
`HumanInteractionService` absorbiera el handoff —ya que de todos modos "involucra a un humano"—, la
premisa completa de CH-06 §9 (que toda resolución permite reanudar el mismo turno) dejaría de ser
universalmente cierta, exactamente el mismo tipo de conflación que CH-22 §15 ya trazó, con matices
distintos, entre `PolicyEngine` y `EvaluationHarness` para la palabra "evaluar".

**La distinción con `OperationalController` (CH-18), precisa y necesaria.** `OperationalController.
applyControlDirective` (CH-18) ya decide, y ya aplica, que un run debe terminarse mediante un
`ControlDirective` de tipo `KILL_SWITCH` — pero CH-18 §8 nunca declaró la responsabilidad de
representar, de forma estructurada, qué le queda pendiente a un humano después de esa terminación;
esa pregunta, hasta este capítulo, no tenía dueño. `HandoffCoordinator` no decide jamás si un kill
switch debe aplicarse, ni cuándo: recibe, en `reason`, un valor ya determinado por el disparador real
(`KILL_SWITCH`, entre otros), sin necesitar conocer la lógica interna de `OperationalController` ni
autorizar por su cuenta ningún comando operacional.

**La distinción con `ExecutionController` (CH-07), heredada y aplicada aquí con un disparador
nuevo.** `evaluateExecutionContinuation` (CH-07) ya decide si un run puede seguir consumiendo su
`ExecutionBudget` — pero nunca decidió, ni podría decidir sin romper su propia frontera, qué le pasa
a un humano cuando ese presupuesto se agota; `BUDGET_EXHAUSTED` (`HandoffReason`, seccion 6) es, en
este capítulo, la traducción estructurada de esa misma señal hacia un traspaso, sin que
`ExecutionController` cambie una sola línea.

**`P-13`, extendido al empaquetado de un handoff con la misma disciplina que todo el libro.**
`createHandoffPackage` no recibe ninguna entrada que el modelo haya producido — ni siquiera de forma
indirecta. El modelo no decide si su propio run debe transferirse a un humano, no puede solicitar su
propio handoff, y no puede, bajo ninguna circunstancia, observar o alterar un `HandoffPackage` ya
producido — la ausencia total del modelo en el pseudocódigo de este capítulo es, otra vez, la
materialización directa del mismo argumento que `P-13` ya estableció para la autorización de
acciones, ahora aplicado, por primera vez con código real, al traspaso de control a un humano.

**Límite que este capítulo deja explícitamente abierto.** `createHandoffPackage` no modela ningún
control de acceso sobre **quién** puede invocarla, ni sobre **quién**, después, puede leer un
`HandoffPackage` ya producido — cualquier llamador puede, en este capítulo, transferir cualquier
run/sesión a cualquier `ActorId`. Autorizar la escritura y la lectura de este contrato (una pregunta
con implicaciones reales: un `HandoffPackage` referencia, vía `contextRef`, el estado interno de un
run que puede contener datos sensibles de un tenant, `INV-E07`) queda, explícitamente, fuera de
alcance de este capítulo — el mismo límite que `AuditLedger` (CH-19 §15), `DataGovernanceEngine`
(CH-20 §15), `ExecutionFabricAdapter` (CH-21 §15) y `EvaluationHarness` (CH-22 §15) ya dejaron
abierto para sus propios registros.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST CreateHandoffPackageRejectsAMissingRunId
TEST CreateHandoffPackageAlwaysStartsInPendingStatus
TEST CreateHandoffPackageNeverAcceptsAStatusParameter
TEST CreateHandoffPackageEmitsAnEventOnlyWhenExecutionAndAgentIdAreResolved
TEST HandoffReasonIsNeverAFreeTextField
TEST HandoffCoordinatorNeverRepresentsAPointInTurnHumanDecision
TEST HandoffCoordinatorNeverDecidesWhenAHandoffShouldOccur
TEST KillSwitchControlDirectiveTranslatesToHandoffReasonKillSwitch
TEST HandoffPackageStatusIsNeverReducedToABoolean
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (después de CH-23 — la última regla de la Constitution que ningún capítulo anterior
había citado con código real, INV-E12, materializada por primera vez)

Constitution
 ├── Article IV     — Decision Ownership (tabla original sin cambios; HandoffCoordinator, como
 │                     DataGovernanceEngine/ExecutionFabricAdapter/EvaluationHarness, decide algo
 │                     real — no comparte la ausencia de fila de EventBus/AuditLedger)
 └── Amendment v1.1 — Enterprise Activation, Interoperability and Operations
                       (INV-E12 citado por primera vez con código real — la última de las sesenta y
                       cuatro reglas del Article original más Amendment v1.1 que llegaba a este
                       capítulo sin ninguna cita real)

Contracts (registry/contracts.yaml)
 ├── C-001..C-033  (sin cambios — CH-00..CH-22)
 └── C-034 HandoffPackage   (CH-23, nuevo — el paquete estructurado que transfiere el control
                    completo de un run/sesión a un humano, INV-E12/INV-19)

Components (registry/components.yaml)
 ├── CMP-001..CMP-020  (sin cambios — CH-01..CH-22)
 └── CMP-021 HandoffCoordinator  (CH-23, nuevo — décimo componente de este registry que no
                    corresponde a ninguno de los once nombres de Article III)
```

**Verificación de cobertura constitucional — resultado real, no asumido.** El encargo de este
capítulo partía de la premisa (heredada de CH-22 §18/§19) de que `INV-E12` era la ÚNICA regla de la
Constitution que ningún capítulo anterior había citado nunca. Antes de escribir la sección 19, se
ejecutó un barrido programático propio sobre los veinticuatro `chapter.md` reales (CH-00..CH-23) para
verificar esa premisa de forma independiente, en vez de darla por buena — y el resultado, honesto,
es que la premisa NO era del todo correcta: además de `INV-E12` (ya cerrado por este capítulo), dos
reglas más —`P-07` ("Skills encode reusable procedural knowledge") y `P-09` ("Single-agent
reliability precedes multi-agent complexity")— aparecen, verificado con grep de texto completo,
ÚNICAMENTE dentro de la transcripción literal de `constitutional_articles` en el frontmatter de CH-00
§0 — nunca en la sección 4 (Impacto Constitucional) de CH-00 ni de ningún capítulo posterior, ni en
prosa, ni con ningún mecanismo real que las materialice. Ver seccion 19 para el comando exacto
ejecutado y su salida completa, y `planes/2026-09-18-capitulo-23-handoff-coordinator.md` para la
misma evidencia documentada fuera del capítulo. Este hallazgo queda, deliberadamente, sin resolver
por este capítulo —el alcance de CH-23 se decidió y se cerró exclusivamente alrededor de `INV-E12`,
y reabrirlo para cubrir `P-07`/`P-09` habría sido, precisamente, el tipo de expansión de alcance no
autorizada que este libro evita— pero se documenta aquí con el mismo rigor y la misma honestidad de
cobertura que CH-22 §18 ya aplicó al descubrir `INV-E12` sin haberlo buscado.

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado real hacia `OperationalController`, `ExecutionController`, `PolicyEngine` y
  `HumanInteractionService`**: ningún componente anterior invoca todavía, de verdad,
  `createHandoffPackage` — el ejemplo de la seccion 11 prueba que el mecanismo funciona y que la
  traducción `ControlDirective.type = KILL_SWITCH → HandoffPackage.reason = KILL_SWITCH` es
  consistente, no que ya esté conectado dentro de un flujo real.
- **Las transiciones `PENDING → ACCEPTED` y `ACCEPTED → COMPLETED`**: declaradas en el `ENUM`
  (seccion 6/12), pero ninguna función de este capítulo las cablea — asumido, no construido (mismo
  tratamiento que `ExecutionPlacement` (CH-21 §18) y `EvaluationReport` (CH-22 §18) ya dieron a sus
  propios límites de reemplazo/vigencia).
- **La resolución real de `contextRef`**: cómo, en la práctica, se construye una referencia opaca
  válida hacia el `AgentState`/`ContextSnapshot` de un run — asumida como una señal de entrada ya
  resuelta, no construida (Preview, infraestructura de borde).
- **El motor real que decide `MODEL_STUCK`**: a diferencia de `KILL_SWITCH` (`OperationalController`,
  CH-18) y `BUDGET_EXHAUSTED` (`ExecutionController`, CH-07), ningún componente de este libro decide
  hoy, con código real, cuándo un modelo "se atascó" dentro de su propio turno — ese disparador queda,
  deliberadamente, conceptual.
- **Autorización de lectura/escritura sobre el propio `HandoffPackage`**: quién puede construir uno o
  consultar uno ya producido — señalado explícitamente en la seccion 15, no resuelto (mismo límite
  abierto que `AuditLedger`, CH-19 §15, `DataGovernanceEngine`, CH-20 §15, `ExecutionFabricAdapter`,
  CH-21 §15, y `EvaluationHarness`, CH-22 §15, dejaron para sus propios registros). `INV-E07`
  (aislamiento por tenant) tampoco se modela aquí.
- **Auditar un handoff con `AuditLedger`**: ningún cableado real conecta todavía `HandoffCoordinator`
  con `recordAuditEntry` (CH-19).
- **Qué hace, en la práctica, un humano una vez que acepta el control de un run transferido**: fuera
  de alcance por diseño (seccion 8, `does_not_own`) — este capítulo modela la FORMA del traspaso,
  nunca lo que ocurre después de que un humano lo acepta.
- Reviewers plurales, evals reales, y orquestación multi-agente propiamente dicha: explícitamente
  fuera de alcance de BH-v0.1, igual que en todos los capítulos anteriores.

## 19. Siguiente Incremento (Next Increment)

Con este capítulo, `INV-E12` —la regla que motivó por completo su encargo— tiene, por fin, al menos
un capítulo real que la cita con código: la última de las reglas que el plan de CH-22 había señalado
explícitamente como pendiente. Pero la pregunta más amplia que el encargo de este capítulo también
pedía verificar —si, después de CH-23, TODAS las reglas de la Constitution (`P-01`..`P-30`,
`INV-01`..`INV-20`, `INV-E01`..`INV-E14`) tienen ya, cada una, al menos un capítulo real que las
cite— exige una respuesta basada en evidencia real, no en la premisa heredada. El comando ejecutado
y su salida completa:

```text
$ python3 - <<'EOF'
import re, glob
const = open('constitution/ARCHITECTURE_CONSTITUTION.md', encoding='utf-8').read()
expected = set(f'P-{i:02d}' for i in range(1,31)) | \
           set(f'INV-{i:02d}' for i in range(1,21)) | \
           set(f'INV-E{i:02d}' for i in range(1,15))
full_text = ""
for c in sorted(glob.glob('book/chapters/*/chapter.md')):
    if '00-arquitectura-constitucion' in c:
        continue
    full_text += open(c, encoding='utf-8').read()
cited = set(re.findall(r'\b(?:P-\d{2}|INV-E\d{2}|INV-\d{2})\b', full_text))
print(sorted(expected - cited))
EOF
['P-07', 'P-09']
```

El resultado, honesto: DOS reglas —`P-07` ("Skills encode reusable procedural knowledge") y `P-09`
("Single-agent reliability precedes multi-agent complexity")— siguen, después de CH-23, citadas
ÚNICAMENTE dentro de la transcripción literal de Amendment/Article original en el frontmatter de
CH-00 §0, sin que ningún capítulo —ni siquiera CH-00 en su propia sección 4— las haya citado nunca
con código real ni en prosa de Impacto Constitucional. La premisa heredada de CH-22 ("`INV-E12` es la
ÚNICA regla sin citar") era, por lo tanto, incompleta — cierta para `INV-E12` específicamente, pero
no para el conjunto completo de sesenta y cuatro reglas. Este capítulo no expande su alcance ya
decidido (seccion "Paso 2" del encargo) para resolver `P-07`/`P-09`: los deja documentados,
explícitamente, como el hallazgo no anticipado de este capítulo — el mismo tratamiento editorial que
CH-22 §18 ya dio al descubrir `INV-E12` sin haberlo buscado.

El problema natural del próximo incremento tiene, por lo tanto, tres caminos igualmente legítimos:
resolver `P-07` (un componente o una extensión de contrato para el conocimiento procedural reusable
de una skill, separado del core/tools/identidad del agente — candidato natural: extender
`CapabilityRegistry`, CH-08, o instalar un componente dedicado a `Skill` como entidad propia);
resolver `P-09` (una materialización explícita de que la confiabilidad single-agent — context,
tools, state, reliability, governance — precede a cualquier complejidad multi-agente real, más allá
de lo que `AgentCommunicationGateway`, CH-15, ya cubre para interoperabilidad); o cablear, por fin,
alguno de los muchos puntos de integración que este capítulo y los nueve anteriores de Amendment
v1.1 dejaron explícitamente como deuda (seccion 18) — que `OperationalController` invoque de verdad
`createHandoffPackage` al aplicar un `KILL_SWITCH`, que `ExecutionController` lo invoque al agotarse
un `ExecutionBudget`, o que las transiciones `ACCEPTED`/`COMPLETED` de `HandoffStatus` se cableen con
una función real.

`next_chapter` queda en `null` en el frontmatter de este capítulo porque, en este momento del libro,
ese próximo capítulo todavía no existe como archivo — solo como el conjunto de problemas de
integración que motivarían su escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg / Bucles
> de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows),
> secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): `INV-E12` nunca fue citada con código real, ni siquiera en
   prosa, por ningún capítulo anterior — la regla que el plan de CH-22 había señalado como la última
   de la Constitution sin ningún dueño (una premisa que la seccion 17/19 de este capítulo verifica de
   forma independiente y corrige: `P-07`/`P-09` quedan en la misma situación).
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): un componente que ya
   "toca" la intervención humana (`HumanInteractionService`, CH-06) puede leerse, por error, como si
   ya cubriera cualquier pregunta futura sobre un humano — hasta que aparece una pregunta de tamaño y
   objeto distintos (transferir el control completo, no resolver una decisión puntual).
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `HandoffCoordinator` con una ficha que declara tanto lo que posee (`owns`: construir el
   `HandoffPackage` estructurado) como lo que explícitamente NO posee (`does_not_own`: decidir CUÁNDO
   ocurre el handoff — `OperationalController`/`ExecutionController`/`PolicyEngine`, ya resueltos).
4. **Modelos mentales** (= §4, Constitutional Impact): "un humano interviene aquí" no es una sola
   pregunta — es, como mínimo, dos preguntas con objeto, tamaño y dueño distintos, y "estructurado"
   no es una preferencia de estilo sino una exigencia que un contrato debe cerrar por diseño, no por
   convención.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un componente nuevo toca, aunque sea
  tangencialmente, la intervención humana, crece la tentación de asumir que
  `HumanInteractionService` (CH-06) ya cubre cualquier pregunta futura sobre "un humano interviene
  aquí", hasta que un sistema real necesita, de verdad, transferir el control completo de un run
  atascado y descubre que ningún tipo existente de `HumanInteractionType` significa eso.
- **Bucle de equilibrio (estabiliza):** `createHandoffPackage` (§11) nunca acepta invocarse sin una
  referencia al run/sesión que transfiere, y `HandoffPackage.reason` nunca tiene espacio para un
  párrafo de prosa libre — cerrando, con el mismo principio fail-closed y el mismo principio
  estructural que ya protegieron la autorización desde CH-05 y la certificación de candidatos desde
  CH-22, el bucle que este capítulo abre.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `HandoffPackage` (`C-034`) referencie el
estado/contexto relevante de forma completamente opaca (`contextRef: Text`) y que `HandoffCoordinator`
(`CMP-021`) no dependa de ningún componente que decida CUÁNDO ocurre un handoff. Mantener ambas
independencias es la forma en que este capítulo hace real la separación que `INV-E12` exige por
diseño de contratos, no solo por convención documentada — exactamente como CH-22 lo hizo para `P-28`,
y CH-06 lo hizo para `INV-14`.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo de
> esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set` (frontmatter) y
> es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa, para lectura directa
> del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Ya existe un componente que representa y resuelve una decisión puntual dentro de un turno que
   sigue en marcha. ¿Es la misma pregunta que transferir el control completo de un run, o son
   preguntas de dominios distintos? *(cierra la pregunta guía 1)*
2. Si la razón de un handoff importa para decidir qué hacer después, ¿debería reducirse a un
   párrafo de texto libre? *(cierra la pregunta guía 2)*
3. Ya existe un componente que puede forzar la terminación de un run sin depender del modelo. ¿Quién
   construiría la representación de una transferencia a partir de esa misma señal, y cuándo? *(cierra
   la pregunta guía 3)*
4. ¿Debería el componente que construye un paquete de traspaso decidir, además, cuándo debe ocurrir
   la transferencia? *(cierra la pregunta guía 4)*

### Explicar

1. `HandoffCoordinator` posee construir el paquete estructurado de un traspaso. Explica, como si
   hablaras con alguien sin contexto técnico, por qué NO posee decidir CUÁNDO ese traspaso debe
   ocurrir.
2. `HandoffPackage.reason` es un `ENUM` de cuatro valores, nunca un `Text` libre. Explica qué
   información perdería un sistema futuro que necesitara enrutar automáticamente un handoff según su
   causa.

### Conectar

1. `HumanInteractionService` (CH-06) ya representa y resuelve una intervención humana. ¿Le
   correspondería a ese mismo componente, además, representar la transferencia de control completo
   de un run?
2. `OperationalController` (CH-18) ya puede forzar la terminación de un run con un `ControlDirective`
   de tipo `KILL_SWITCH`. ¿Qué campo exacto de ese contrato se traduce en la razón estructurada de un
   handoff en este capítulo?
3. `ExecutionController` (CH-07) ya decide si un run puede seguir consumiendo su presupuesto. Si ese
   presupuesto se agota, ¿quién debería construir la representación de que un humano ahora debe
   hacerse cargo?

### Espaciar

Las cinco tarjetas de repaso de este capítulo (dos sobre `HandoffCoordinator` — su `owns` y su
`does_not_own` —, dos sobre `HandoffPackage` — sus campos y por qué `reason`/`status` son `ENUM`
cerrados en vez de `Text`/`Boolean` —, y una sobre el ejemplo con `ControlDirective`/`KILL_SWITCH`)
entran hoy en `reviewStage = DAY_1`. Repásalas de nuevo al día 3, al día 7 y al día 21 (curva de
Ebbinghaus) — ver el apéndice de tarjetas al final del libro (edición PDF) o
`retrieval_set.flashcards` en `dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te equivocaste,
ese es precisamente el punto ciego que este método existe para revelar.
