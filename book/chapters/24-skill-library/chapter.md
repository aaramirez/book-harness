---
id: CH-24
title: "SkillLibrary y el Conocimiento Procedural que Nunca Fue una Capability"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-022]
introduces_contracts: [C-035]
modifies_contracts: []
constitutional_articles: [P-07, P-13, INV-18, INV-19, INV-20]
previous_chapter: CH-23
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH24
    text: |
      Al terminar este capítulo podrás distinguir, con precisión, dos preguntas que ambas
      resuelven un nombre de texto libre contra un registro propio pero pertenecen a dominios
      completamente distintos: cuál implementación concreta satisface una capacidad solicitada, y
      cuál procedimiento o guía reusable aplica a una situación dada. Podrás diseñar el registro de
      ese segundo tipo de conocimiento como una capa separada del core del agente, de sus
      tools/capabilities y de su identidad, y podrás explicar por qué resolver una guía reusable
      nunca produce, ni debería producir jamás, algo que un runtime ejecute como una acción.
  skeleton:
    id: SK-CH24
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
    components_to_be_introduced: [CMP-022]
    contracts_to_be_introduced: [C-035]
  guiding_questions:
    - id: GQ-CH24-01
      text: |
        Ya existe un componente que resuelve, de forma determinística, qué implementación
        concreta corresponde a un nombre de capacidad solicitado. Si en cambio lo que hace falta
        resolver no es QUÉ CÓDIGO ejecutar sino QUÉ PROCEDIMIENTO O GUÍA reusable aplica a una
        situación dada, ¿es esa la misma pregunta formulada sobre otro sustantivo, o una pregunta
        de un dominio de conocimiento completamente distinto?
      answered_by: RQ-CH24-01
    - id: GQ-CH24-02
      text: |
        Ya existe un componente que representa, de forma estable, la identidad y configuración de
        un agente, independiente de cualquier run. Si un procedimiento reusable necesita estar
        disponible para muchas situaciones sin duplicarse dentro de la identidad de cada agente
        que lo use, ¿dónde debería vivir ese conocimiento en su lugar, y qué se rompería si se
        guardara dentro de esa misma identidad?
      answered_by: RQ-CH24-02
    - id: GQ-CH24-03
      text: |
        Si resolver cuál procedimiento aplica a una situación produce, como resultado, una
        referencia a una guía — nunca una acción lista para ejecutarse —, ¿debería ese resultado
        pasar jamás por el mismo mecanismo que decide si una acción está permitida para
        ejecutarse, o esa pregunta simplemente no aplica a algo que nunca fue una acción?
      answered_by: RQ-CH24-03
    - id: GQ-CH24-04
      text: |
        Cuando el nombre de una situación no corresponde a ningún procedimiento reusable ya
        conocido, ¿debería el mecanismo que resuelve esa búsqueda inventar o adivinar una guía
        plausible, o fallar de forma explícita y clasificada, exactamente como ya ocurre cuando un
        nombre de capacidad no corresponde a ninguna implementación registrada?
      answered_by: RQ-CH24-04
  systems_lens:
    iceberg_visible_fact: |
      Veinticuatro capítulos reales, y `P-07` ("Skills encode reusable procedural knowledge")
      nunca fue citado con código real por ningún capítulo anterior — verificado, esta vez, no con
      un barrido de texto completo (contaminado por la propia mención en prosa de `P-07`/`P-09`
      que CH-23 §4/§17/§19 hace al documentar el hallazgo que dejó abierto), sino contra la señal
      estructurada que `scripts/validate-chapter` mismo usa como fuente de verdad: el campo
      `frontmatter.constitutional_articles` de cada uno de los veinticuatro `chapter.md`
      existentes. Solo CH-00 (que transcribe la Constitution completa) declara `P-07` en ese campo;
      ningún capítulo real (CH-01..CH-23) lo declaró nunca como una cita propia (ver seccion 2, El
      Problema).
    iceberg_patterns: |
      El patrón que ya se repitió entre `ToolRuntime`/`ModelGateway` y `CapabilityRegistry` (CH-08)
      reaparece aquí con una variante distinta: no son dos componentes vecinos señalando la misma
      responsabilidad desde direcciones opuestas, sino un componente ya existente,
      `CapabilityRegistry`, cuya resolución de "un nombre de texto libre contra un registro
      conocido" se parece, en la superficie, exactamente a lo que este capítulo necesita — al
      punto de que sería tentador extenderlo en vez de instalar un dueño nuevo. La tentación es la
      misma que ya motivó CH-22 y CH-23: una responsabilidad nueva puede parecer, en prosa
      informal, una variación de una ya resuelta, aunque Article IV la asigne a una fila distinta
      de su tabla (ver seccion 3, Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala `SkillLibrary` (`CMP-022`), el undécimo componente de este registry
      que no corresponde a ninguno de los once nombres de Article III, con una ficha que declara
      tanto lo que posee (`owns`: registrar el descriptor de una skill como conocimiento procedural
      reusable, separado del core/tools/identidad — cita literal de `P-07`) como lo que
      explícitamente NO posee (`does_not_own`: resolver qué implementación concreta satisface una
      capability solicitada, la frontera más importante de este capítulo, contra
      `CapabilityRegistry`) — y formaliza `SkillDescriptor` (`C-035`), deliberadamente con la
      misma forma de cinco campos que `CapabilityDescriptor` (`C-018`, CH-08) para que el contraste
      entre ambos sea legible sin sugerir jamás que son el mismo concepto (ver seccion 8, Component
      Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es la lectura literal de `P-07`: "reusable
      procedural knowledge" no es "otra forma de nombrar una capability" — es CÓMO hacer algo paso
      a paso, un dominio de conocimiento ortogonal a QUÉ CÓDIGO ejecuta una acción
      (`CapabilityRegistry`, CH-08), QUÉ ES un agente (`AgentCore`/`AgentConfig`, CH-11/CH-00) y
      CÓMO se ejecuta un side effect (`ToolRuntime`, CH-02). Confundir estos cuatro dominios —
      exactamente lo que `P-07` exige mantener separado — sería repetir, a una escala más amplia,
      el mismo riesgo que Article IV ya previene fila por fila (ver seccion 4, Impacto
      Constitucional).
    reinforcing_loop: |
      Cada vez que un componente nuevo resuelve "un nombre contra un registro conocido", crece la
      tentación de asumir que ya existe un componente que hace exactamente eso —
      `CapabilityRegistry` (CH-08) — y que basta con extenderlo, en vez de preguntar primero qué
      TIPO de resultado produce esa resolución: una implementación lista para ejecutarse, o una
      guía para consultar. Sin esa pregunta, dos dominios de conocimiento completamente distintos
      convergerían, con el tiempo, en un solo componente sobrecargado.
    balancing_loop: |
      `resolveSkillForSituation` (seccion 11) es el mecanismo de equilibrio: recorre el registro
      real de `SkillDescriptor` y rechaza, con un `HarnessError` categorizado — nunca con una
      ejecución silenciosa de una guía inventada — tanto un `situationName` ausente como uno que no
      corresponde a ningún descriptor registrado, sin jamás producir algo que se parezca a un
      `ToolCall` listo para ejecutarse.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `SkillDescriptor` (`C-035`) nunca se
      confunda, ni en su forma ni en su tratamiento, con `CapabilityDescriptor` (`C-018`) —
      `resolveSkillForSituation` produce una referencia consultable a un procedimiento, nunca una
      acción, y por eso nunca pasa por `PolicyEngine.evaluate` ni por `ToolRuntime.execute`. Si
      `SkillLibrary` hubiera heredado, aunque fuera parcialmente, el tratamiento de una capability
      resuelta, `P-07` habría quedado satisfecho en la forma pero no en el fondo: el conocimiento
      procedural habría dejado de estar realmente separado de las tools, exactamente el
      acoplamiento que Article IV existe para prevenir.
  recall_questions:
    - id: RQ-CH24-01
      text: |
        ¿Qué componente ya resuelve, de forma determinística, qué implementación concreta
        corresponde a un nombre de capacidad, y qué tiene que ser distinto —en tipo de resultado,
        no solo en nombre— de lo que resuelve qué procedimiento reusable aplica a una situación?
    - id: RQ-CH24-02
      text: |
        ¿Qué componente ya representa la identidad/configuración estable de un agente, y por qué
        un procedimiento reusable no debería, jamás, embeberse dentro de ese mismo contrato?
    - id: RQ-CH24-03
      text: |
        ¿Por qué el resultado de resolver qué skill aplica a una situación nunca pasa por
        `PolicyEngine.evaluate` ni por `ToolRuntime.execute`, a diferencia de un `ToolCall` ya
        resuelto?
    - id: RQ-CH24-04
      text: |
        ¿Qué código de `HarnessError` se produce cuando un `situationName` no corresponde a ningún
        `SkillDescriptor` registrado, y por qué esa categoría es la misma que ya usa
        `CapabilityRegistry` para su propio fallo análogo?
  explain_prompts:
    - id: EP-CH24-01
      text: |
        `SkillLibrary` posee registrar y resolver el conocimiento procedural reusable de una
        skill. Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee
        resolver qué implementación concreta satisface una capability solicitada, aunque ambas
        resoluciones "buscan un nombre en un registro" — ¿qué se rompería, en concreto, si
        `SkillLibrary` empezara a producir algo que `ToolRuntime` pudiera ejecutar directamente?
      target_entity: CMP-022
    - id: EP-CH24-02
      text: |
        `SkillDescriptor.procedureRef` es una referencia opaca al procedimiento real, no su
        contenido completo en prosa. Explica qué perderíamos si `SkillLibrary`, en vez de guardar
        una referencia opaca, modelara el texto completo de cada guía dentro de su propio registro.
      target_entity: C-035
  interleaved_questions:
    - id: IQ-CH24-01
      text: |
        `CapabilityRegistry` (CH-08) ya resuelve un `capabilityName` de texto libre contra un
        registro de `CapabilityDescriptor`, produciendo un `ToolCall` listo para pasar por policy
        y ejecución. Este capítulo resuelve un `situationName` contra un registro de
        `SkillDescriptor`. ¿Por qué el resultado de esta segunda resolución nunca podría, sin
        romper la frontera que CH-08 ya estableció, pasar por `ToolRuntime.execute` ni por
        `PolicyEngine.evaluate` como si fuera un `ToolCall`?
      current_chapter_entities: [CMP-022, C-035]
      prior_chapter_entities: [CMP-008, C-018]
      prior_chapter: CH-08
    - id: IQ-CH24-02
      text: |
        `AgentCore` (CH-11) ya representa la identidad de un agente — independiente de cualquier
        run— a través de `AgentConfig` (C-002, CH-00), y `P-07` exige que el conocimiento
        procedural reusable esté separado de esa identidad. ¿Qué se rompería si un
        `SkillDescriptor` resuelto se embebiera dentro de `AgentConfig`, y por qué `AgentCore` no
        necesita cambiar una sola línea de su propio capítulo para que esa separación sea real
        desde este capítulo?
      current_chapter_entities: [CMP-022, C-035]
      prior_chapter_entities: [CMP-011, C-002]
      prior_chapter: CH-11
  flashcards:
    - id: FC-CH24-01
      front: |
        ¿Qué posee `SkillLibrary` (Amendment original, `P-07`), en una frase?
      back: |
        Registrar, en exclusiva, el descriptor de una skill como conocimiento procedural
        reusable — separado de `AgentCore` (identidad), de `CapabilityRegistry`/`ToolRuntime`
        (tools/capabilities) y de `PolicyEngine` (autorización) — y resolver, contra ese registro,
        qué `SkillDescriptor` aplica a una situación nombrada. Cita literal de `P-07`: "El
        conocimiento procedural reusable debe estar separado del core, las tools y la identidad
        del agente".
      source_entity: CMP-022
      chapter_introduced_in: CH-24
      review_stage: DAY_1
    - id: FC-CH24-02
      front: |
        ¿Qué NO posee `SkillLibrary`, y a qué componentes pertenecen esas decisiones?
      back: |
        Resolver qué implementación concreta satisface una capability solicitada
        (`CapabilityRegistry`, CH-08 — la frontera más importante); representar la
        identidad/configuración de un agente (`AgentCore`, CH-11); ejecutar el side effect en sí de
        ninguna acción (`ToolRuntime`, CH-02); decidir autorización sobre ninguna acción
        (`PolicyEngine`, CH-05); certificar un candidato de skill antes de su promoción a
        producción (`EvaluationHarness`, CH-22).
      source_entity: CMP-022
      chapter_introduced_in: CH-24
      review_stage: DAY_1
    - id: FC-CH24-03
      front: |
        ¿Qué campos tiene `SkillDescriptor` (`C-035`)?
      back: |
        `skill` (`SkillId`, el identificador ya resuelto — mismo patrón que `capability:
        CapabilityId` en `CapabilityDescriptor`), `name` (`Text`, el nombre canónico contra el que
        se compara `situationName`), `version` (`Text`, explícita — mismo criterio de versionado
        que `CapabilityDescriptor`/`P-26`, sin que `P-26` en sí se extienda a skills),
        `procedureRef` (`Text`, referencia opaca al procedimiento/guía real) y `appliesTo`
        (`Optional<Text>`, referencia opaca y opcional a qué capabilities/situaciones aplica).
      source_entity: C-035
      chapter_introduced_in: CH-24
      review_stage: DAY_1
    - id: FC-CH24-04
      front: |
        ¿Por qué `SkillDescriptor` tiene deliberadamente la misma forma de cinco campos que
        `CapabilityDescriptor` (C-018, CH-08), y por qué eso NO significa que sean el mismo
        concepto?
      back: |
        La simetría hace legible el contraste que este capítulo necesita trazar: ambos registran
        un nombre canónico, una versión y una referencia opaca a "lo real" (`implementationRef`
        frente a `procedureRef`). Pero `CapabilityDescriptor.capability` resuelve QUÉ CÓDIGO/API
        ejecuta una acción; `SkillDescriptor.skill` resuelve QUÉ PROCEDIMIENTO aplica a una
        situación — el resultado de uno es una acción pendiente de policy y ejecución; el
        resultado del otro es, siempre, una guía para consultar, nunca algo que un runtime
        ejecute.
      source_entity: C-035
      chapter_introduced_in: CH-24
      review_stage: DAY_1
    - id: FC-CH24-05
      front: |
        ¿Qué produce `resolveSkillForSituation` cuando `situationName` no corresponde a ningún
        `SkillDescriptor` registrado, y por qué esa clasificación reutiliza `VALIDATION` en vez de
        una categoría nueva?
      back: |
        Un `HarnessError` con `code = "SKILL_NOT_FOUND"`, categoría `VALIDATION` — la misma
        categoría, y el mismo argumento, que `CapabilityRegistry.resolveToolCall` (CH-08) ya usó
        para `CAPABILITY_NOT_FOUND`: un nombre inexistente es un fallo de validación de la
        *entrada*, no un fallo de la resolución en sí ni de ninguna ejecución — introducir una
        categoría `SKILL` nueva solo para distinguir "quién" detectó el problema fragmentaría
        `ErrorCategory` sin ganancia semántica real.
      source_entity: CMP-022
      chapter_introduced_in: CH-24
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH24-01
      recall_question: RQ-CH24-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH24-02
      recall_question: RQ-CH24-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH24-03
      recall_question: RQ-CH24-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH24-04
      recall_question: RQ-CH24-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 24 — SkillLibrary y el Conocimiento Procedural que Nunca Fue una Capability

> **Regla constitucional (Article I, `P-07`):** "Skills encode reusable procedural knowledge" — "El
> conocimiento procedural reusable debe estar separado del core, las tools y la identidad del
> agente."

CH-23 cerró `INV-E12` — la regla que su propio encargo (heredado de CH-22) señalaba como la última
de la Constitution sin ninguna cita real — y documentó, con evidencia programática propia, un
hallazgo no anticipado: la premisa de exclusividad no era del todo exacta, porque `P-07` ("Skills
encode reusable procedural knowledge") y `P-09` ("Single-agent reliability precedes multi-agent
complexity") quedaban en la misma situación. CH-23 decidió, correctamente, no expandir su propio
alcance ya cerrado para resolverlos — pero dejó ambos documentados como el problema natural de un
incremento futuro.

Este capítulo, el vigesimoquinto capítulo real de contenido de este libro, toma uno de esos dos
caminos: cierra `P-07` con un componente y un contrato dedicados. Antes de escribir una sola línea
de contenido nuevo, este capítulo repitió la verificación de CH-23 — pero de forma más precisa. Un
barrido de texto completo sobre los veinticuatro `chapter.md` existentes (CH-00..CH-23) encuentra la
subcadena `"P-07"` también en CH-23 mismo — pero solo porque CH-23 §4/§17/§19 **menciona el nombre
de la regla en prosa** al documentar que quedaba sin resolver, nunca porque CH-23 la cite como una
responsabilidad real que algún `owns` satisface. La señal correcta —la misma que
`scripts/validate-chapter` usa como fuente de verdad— es el campo estructurado
`frontmatter.constitutional_articles` de cada capítulo, no un grep de texto libre contaminado por la
propia meta-discusión de un capítulo anterior:

```text
$ node -e '
const fs = require("fs");
const path = require("path");
for (const d of fs.readdirSync("book/chapters")) {
  if (d === "00-arquitectura-constitucion" || d.startsWith("24-")) continue;
  const raw = fs.readFileSync(path.join("book/chapters", d, "chapter.md"), "utf8");
  const m = raw.match(/constitutional_articles:\s*\[([^\]]*)\]/);
  const ids = m ? m[1].split(",").map(s => s.trim()) : [];
  if (ids.includes("P-07") || ids.includes("P-09")) console.log(d, ids);
}
'
(sin salida — ningún capítulo real, CH-01..CH-23, declaró jamás P-07 ni P-09 en su propio
frontmatter.constitutional_articles; solo CH-00, que transcribe la Constitution completa, lo hace)
```

`P-09` ("Single-agent reliability precedes multi-agent complexity") es, por diseño de este mismo
encargo, un principio de secuenciación arquitectónica de todo el libro — no una responsabilidad que
un componente pueda poseer — y queda, deliberadamente, sin cerrar por este capítulo: una decisión
editorial distinta, que otra sesión tomará después, decidirá cómo (o si) materializarlo. Este
capítulo cierra, exclusivamente, `P-07`.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de saber
> cómo se llama el componente de este capítulo. El detalle estructurado de esta sección vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, con precisión, dos preguntas
que ambas resuelven un nombre de texto libre contra un registro propio pero pertenecen a dominios
completamente distintos: cuál implementación concreta satisface una capacidad solicitada, y cuál
procedimiento o guía reusable aplica a una situación dada. Podrás diseñar el registro de ese segundo
tipo de conocimiento como una capa separada del core del agente, de sus tools/capabilities y de su
identidad, y podrás explicar por qué resolver una guía reusable nunca produce, ni debería producir
jamás, algo que un runtime ejecute como una acción.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e introduce
un contrato de datos nuevo y el undécimo componente de este libro que no corresponde a ninguno de
los once nombres originales de Article III.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar atrás;
están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este capítulo va
a definir):

1. Ya existe un componente que resuelve, de forma determinística, qué implementación concreta
   corresponde a un nombre de capacidad solicitado. Si en cambio lo que hace falta resolver no es
   QUÉ CÓDIGO ejecutar sino QUÉ PROCEDIMIENTO O GUÍA reusable aplica a una situación dada, ¿es esa
   la misma pregunta formulada sobre otro sustantivo, o una pregunta de un dominio de conocimiento
   completamente distinto?
2. Ya existe un componente que representa, de forma estable, la identidad y configuración de un
   agente, independiente de cualquier run. Si un procedimiento reusable necesita estar disponible
   para muchas situaciones sin duplicarse dentro de la identidad de cada agente que lo use, ¿dónde
   debería vivir ese conocimiento en su lugar?
3. Si resolver cuál procedimiento aplica a una situación produce, como resultado, una referencia a
   una guía —nunca una acción lista para ejecutarse—, ¿debería ese resultado pasar jamás por el
   mismo mecanismo que decide si una acción está permitida para ejecutarse?
4. Cuando el nombre de una situación no corresponde a ningún procedimiento reusable ya conocido,
   ¿debería el mecanismo que resuelve esa búsqueda inventar o adivinar una guía plausible, o fallar
   de forma explícita y clasificada?

## 1. Arquitectura Actual (Current Architecture)

CH-00..CH-23 dejaron instalados treinta y cuatro contratos de datos y veintiún componentes: los
once nombres completos de Article III ("Agent Runtime"), dos capítulos de integración, y diez
componentes de Amendment v1.1 (`AdmissionController`, CMP-012, CH-14; `AgentCommunicationGateway`,
CMP-013, CH-15; `CredentialBroker`, CMP-014, CH-16; `IdempotencyGuard`, CMP-015, CH-17;
`OperationalController`, CMP-016, CH-18; `AuditLedger`, CMP-017, CH-19; `DataGovernanceEngine`,
CMP-018, CH-20; `ExecutionFabricAdapter`, CMP-019, CH-21; `EvaluationHarness`, CMP-020, CH-22;
`HandoffCoordinator`, CMP-021, CH-23).

`CapabilityRegistry` (CMP-008, CH-08) es, de los veintiuno, el único que resuelve un nombre de texto
libre contra un registro real de descriptores conocidos. Su función, `resolveToolCall` (CH-08 §11),
compara `RawToolCallProposal.capabilityName` (C-007, CH-03) contra `CapabilityDescriptor.name`
(C-018, CH-08 §6) y produce, cuando encuentra una coincidencia, un `ToolCall` (C-008, CH-02) — una
intención de acción todavía sin autorizar, pero ya lista para atravesar `PolicyEngine.evaluate`
(CH-05) y, después, `ToolRuntime.execute` (CH-02). Cada uno de los cinco campos de
`CapabilityDescriptor` (`capability`, `name`, `version`, `inputSchema`, `implementationRef`)
responde, exactamente, a la pregunta de Article IV: "`CapabilityRegistry` → What implementation
satisfies a requested capability?" — una pregunta sobre QUÉ CÓDIGO ejecuta una acción.

`AgentCore` (CMP-011, CH-11) es, de los veintiuno, el único que representa la identidad y
configuración de un agente — independiente de cualquier run o sesión particular — a través de
`AgentConfig` (C-002, CH-00: `agentId`, `name`, `budget`). CH-11 §8 declaró, citando literalmente
Article III, que `AgentCore` posee "representar la identidad/definición del agente... el 'qué es
este agente', no 'qué está haciendo ahora mismo'" — pero ni `AgentConfig` ni `AgentState` (C-003,
CH-00) tienen jamás, en ningún campo, espacio para un procedimiento o una guía reusable que ese
agente pudiera seguir.

`P-07` ("Skills encode reusable procedural knowledge") fue transcrito, junto con el resto del
Article I original, en CH-00 §5 — pero ningún capítulo posterior lo citó nunca en su propia sección
de Impacto Constitucional con código real, ni en su propio `frontmatter.constitutional_articles`
(ver apertura de este capítulo para la verificación exacta). Ningún contrato de este libro, hasta
este capítulo, modela el conocimiento procedural reusable de una skill como una entidad propia,
separada de una capability.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas para esto, "resolver un nombre de texto libre contra un
registro conocido" tiende a colapsarse en una sola suposición incompleta: que si
`CapabilityRegistry` (CH-08) ya resuelve `capabilityName` contra `CapabilityDescriptor`, entonces
cualquier otra resolución que también compare un nombre contra un registro —incluida la de qué
procedimiento reusable aplica a una situación— debería, por comodidad, extenderse dentro de ese
mismo componente o reusar la misma forma de resultado. Pero `CapabilityRegistry.resolveToolCall`
produce, siempre, un `ToolCall` — una acción todavía sin ejecutar que sí necesita pasar, después, por
`PolicyEngine` y por `ToolRuntime`. Un procedimiento reusable —una guía de "cómo hacer X paso a
paso"— no es una acción: no tiene argumentos que ejecutar, no produce un side effect por sí mismo, y
consultarlo no debería requerir jamás la misma autorización que ejecutar una tool call requiere.

Hay una segunda dimensión del problema, la que da nombre literal a `P-07`: incluso si alguna
implementación decidiera, por su cuenta, guardar algo parecido a una skill, nada le impide guardarla
directamente dentro de `AgentConfig` (por ejemplo, un campo `proceduralNotes: Text` con instrucciones
embebidas) o dentro del propio `CapabilityDescriptor` (extendiendo `inputSchema` o
`implementationRef` para que "también" describan un procedimiento). Cualquiera de las dos rutas
"funcionaría", en un sentido superficial — pero violaría exactamente lo que `P-07` prohíbe
explícitamente: que el conocimiento procedural reusable deje de estar separado del core, las tools
y la identidad del agente. Un procedimiento embebido en `AgentConfig` duplicaría esa guía en cada
agente que la necesitara, en vez de compartirla; un procedimiento embebido en `CapabilityDescriptor`
confundiría "qué código ejecuta una acción" con "qué guía sigue un razonamiento" — la misma
conflación de dominios que Article IV existe para prevenir, a una escala más amplia.

Necesitamos que "¿qué procedimiento o guía reusable aplica a esta situación?" tenga, por fin, un
dueño único y nombrado — separado de `AgentCore` (identidad), de `CapabilityRegistry`/`ToolRuntime`
(tools/capabilities y su ejecución) y de `PolicyEngine` (autorización) — que registre explícitamente
cada skill disponible con su versión y una referencia opaca a su procedimiento real, que resuelva un
nombre de situación contra ese registro mediante un mecanismo real, y que produzca, siempre, una
referencia consultable a una guía — nunca algo que se parezca a una acción lista para ejecutarse.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los treinta y cuatro contratos y los veintiún componentes que existen hasta este punto no bastan
porque:

- `CapabilityDescriptor` (C-018, CH-08 §6) tiene, deliberadamente, cinco campos orientados a
  resolver una implementación ejecutable (`capability`, `inputSchema`, `implementationRef`) —
  ninguno de ellos representa "cómo razonar paso a paso sobre una situación"; forzar ese
  significado dentro de `implementationRef` rompería la premisa de CH-08 §6, que declara esa
  referencia como "opaca a la implementación concreta", nunca a un procedimiento de conocimiento;
- `AgentConfig` (C-002, CH-00 §6) tiene, deliberadamente, tres campos (`agentId`, `name`,
  `budget`) — ninguno representa conocimiento procedural, y CH-11 §8 ya citó literalmente que
  `AgentCore` posee "representar la identidad... independiente de cualquier run", nunca el
  conocimiento que un agente podría consultar durante uno;
- `CapabilityRegistry.resolveToolCall` (CH-08 §11) produce, siempre, un `ToolCall` — un contrato que
  `PolicyEngine` y `ToolRuntime` ya tratan, en toda la Constitution, como una acción pendiente de
  autorización y ejecución; no existe, en este libro, ningún contrato que represente el resultado de
  una resolución que **no** sea una acción;
- ningún componente de este libro declara, todavía, `owns` una responsabilidad que sea, literalmente,
  "conocimiento procedural reusable, separado del core, las tools y la identidad del agente" — la
  cita exacta de `P-07`, que hasta este capítulo permanece, en la práctica, sin ningún mecanismo real
  que la materialice;
- `EvaluationHarness` (CMP-020, CH-22 §8) ya declara evaluable, entre otros candidatos, "una skill"
  antes de su promoción a producción — pero evaluar un candidato ANTES de que exista, y registrar/
  resolver una skill YA registrada para consultarla, son dos preguntas distintas: ninguna de las dos
  sustituye a la otra, y CH-22 nunca instaló ningún registro real de skills, solo declaró que podrían
  ser candidatas de certificación.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la secuencia
> `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una entidad que no
> haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT` registrado — **no
> magic entities**. Este capítulo aplica la misma disciplina que CH-00..CH-23 ya establecieron.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-13   Authorization is deterministic and external to the LLM.
           El mismo argumento que ya protegió la autorización desde CH-01/CH-05, y el empaquetado
           de un handoff desde CH-23, se extiende aquí a la resolución de una skill: el modelo
           nunca decide, nunca ve y nunca constituye una fuente de verdad sobre qué procedimiento
           existe realmente en el registro — resolveSkillForSituation (seccion 11) es completamente
           determinística y externa al LLM; el situationName que recibe se trata como texto no
           confiable, exactamente como CapabilityRegistry trata capabilityName.

Invariants preserved
    INV-18    Toda acción significativa produce un evento observable.
              resolveSkillForSituation (seccion 11) emite un AgentEvent condicionalmente, cuando
              existe un ExecutionContext y un AgentId reales — mismo patrón exacto que
              CapabilityRegistry (CH-08) y cada componente de Amendment v1.1 ya aplicaron a sus
              propias funciones (ver seccion 14).
    INV-19    Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy relevante.
              Cada AgentEvent que emite SkillLibrary lleva el traceId de su ExecutionContext, y el
              SkillDescriptor resuelto correlaciona, por su campo skill, con el registro exacto que
              lo produjo — mismo patrón que CapabilityRegistry ya estableció para ToolCall.capability.
    INV-20    Todo error operacional pertenece a una categoría conocida.
              El único fallo real de este capítulo (seccion 13) reutiliza VALIDATION — la misma
              categoría, y el mismo argumento, que CapabilityRegistry (CH-08 §13) ya usó para
              CAPABILITY_NOT_FOUND: un nombre de situación inexistente es un fallo de validación de
              la entrada, no un fallo de ejecución; este capítulo NO agrega ninguna categoría nueva
              a ErrorCategory (a diferencia de la mayoría de los componentes de Amendment v1.1,
              CH-14..CH-23, que sí agregaron una — ver razonamiento completo en seccion 13).

Principles newly cited with real code (primera vez en este libro que un capítulo real, no solo
CH-00, lo declara en su propio frontmatter.constitutional_articles — la regla que motivó el encargo
de este capítulo)
    P-07   Skills encode reusable procedural knowledge. El conocimiento procedural reusable debe
           estar separado del core, las tools y la identidad del agente.
           Primera materialización real, con código, de este principio — verificado antes de
           escribir este capítulo contra frontmatter.constitutional_articles de los veinticuatro
           chapter.md existentes (ver apertura del capítulo), no contra un grep de texto completo
           contaminado por la propia mención en prosa que CH-23 §4/§17/§19 hace del hallazgo.
           SkillDescriptor (seccion 6/7) y SkillLibrary (seccion 8) producen, por fin, el registro
           separado que la regla exige — deliberadamente con la misma forma de campos que
           CapabilityDescriptor (C-018, CH-08) para que el contraste sea legible, pero resolviendo
           una pregunta de un dominio distinto: QUÉ PROCEDIMIENTO aplica, nunca QUÉ CÓDIGO ejecuta.

Component ownership changes
    CMP-022 SkillLibrary se introduce — registry/components.yaml pasa de 21 a 22 componentes. Es
    el undécimo componente de este registry que NO corresponde a ninguno de los once nombres del
    árbol de Article III ("Agent Runtime"). registry/components.yaml de CMP-008
    (CapabilityRegistry), CMP-011 (AgentCore), CMP-002 (ToolRuntime), CMP-005 (PolicyEngine) y
    CMP-020 (EvaluationHarness) NO se modifica: ninguno cablea todavía su relación real con
    SkillLibrary (ver seccion 9/18).

Lifecycle changes
    Ninguna modificación a AgentRunStatus (C-013), AgentConfig (C-002) ni CapabilityDescriptor
    (C-018): los tres siguen, sin cambios, exactamente como sus capítulos los dejaron.
    SkillDescriptor (C-035, este capítulo) no introduce ningún lifecycle de estados propio — a
    diferencia de HandoffPackage (CH-23) o EvaluationReport (CH-22), un descriptor de skill no
    transiciona: existe, en el registro, o no existe (ver seccion 12).

Security implications
    SkillLibrary es el primer componente de este libro cuya responsabilidad completa es el
    conocimiento procedural reusable de una skill, deliberadamente aislado de toda ejecución. Ver
    seccion 15 para el análisis completo, incluyendo la frontera más importante de este capítulo,
    contra CapabilityRegistry.

Observability implications
    SkillLibrary emite AgentEvent de forma condicional desde su única función real
    (SKILL_RESOLVED / SKILL_RESOLUTION_FAILED) — mismo patrón condicional que CapabilityRegistry
    (CH-08), OperationalController (CH-18), DataGovernanceEngine (CH-20), ExecutionFabricAdapter
    (CH-21), EvaluationHarness (CH-22) y HandoffCoordinator (CH-23).

Deterministic vs agentic boundary
    Article XII se refina una vigesimosegunda vez a nivel de componente: SkillLibrary, igual que
    CapabilityRegistry (CH-08), PolicyEngine y ExecutionController, no interpreta la intención del
    modelo — solo compara, determinísticamente, un situationName contra un registro que el harness
    controla por completo. El modelo puede proponer cualquier situationName; SkillLibrary nunca le
    otorga el beneficio de la duda, exactamente como CapabilityRegistry nunca se lo otorga a
    capabilityName.
```

## 5. Conceptos Nuevos (New Concepts)

- **Reusable Procedural Knowledge** *(cita literal, `P-07`, "Skills encode reusable procedural
  knowledge" / "El conocimiento procedural reusable debe estar separado del core, las tools y la
  identidad del agente")*: el CÓMO hacer algo paso a paso — una guía o procedimiento reusable — como
  un dominio de conocimiento separado de QUÉ CÓDIGO ejecuta una acción (`CapabilityRegistry`,
  CH-08), QUÉ ES un agente (`AgentCore`/`AgentConfig`, CH-11/CH-00) y CÓMO se ejecuta un side effect
  (`ToolRuntime`, CH-02).
- **Skill Resolution**: el tramo determinístico en el que se compara el nombre de una situación
  contra un registro real de skills conocidas (`SkillDescriptor`) y se produce una referencia
  consultable al procedimiento que aplica — nunca una acción ejecutable. Contraste deliberado con
  **Capability Resolution** (CH-08): la misma FORMA de búsqueda (un nombre de texto libre contra un
  registro), un TIPO de resultado completamente distinto.
- **Skill Descriptor**: el registro nombrado de una skill — su identificador, su nombre canónico, su
  versión explícita, y una referencia opaca al procedimiento/guía real. Modelado como el contrato
  `SkillDescriptor` (C-035, seccion 7) — deliberadamente una referencia, nunca el contenido en prosa
  completo del procedimiento (ver seccion 6, nota sobre `procedureRef`).
- **Opaque Procedure Reference**: la referencia al procedimiento/guía real que un `SkillDescriptor`
  transporta (`procedureRef: Text`), sin modelar su detalle — mismo patrón que
  `CapabilityDescriptor.implementationRef` (CH-08), aplicado aquí a un propósito distinto: apuntar,
  sin duplicar, a un procedimiento en vez de a una implementación.
- **Decision Ownership, aplicado por undécima vez** *(Article IV)*: `SkillLibrary` decide "¿qué
  procedimiento reusable aplica a esta situación?"; explícitamente NO decide "¿qué implementación
  concreta satisface una capability solicitada?" (`CapabilityRegistry`, ya resuelto, CH-08 — la
  frontera más importante de este capítulo), "¿qué es este agente?" (`AgentCore`, ya resuelto,
  CH-11), "¿cómo se ejecuta un side effect?" (`ToolRuntime`, ya resuelto, CH-02) ni "¿está permitida
  esta acción?" (`PolicyEngine`, ya resuelto, CH-05).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `Text`, `Timestamp`, `Optional`, `AgentId`,
`ExecutionContext` (C-004, CH-00), `AgentEvent` (C-010, CH-00), `HarnessError` (C-011, CH-00).

Este capítulo cita, además en prosa, dos contratos de capítulos anteriores sin usarlos dentro de su
propio pseudocódigo — mismo patrón de reuso explícito que CH-13, CH-19..CH-23 §6 ya aplicaron:

| Contrato/tipo (reusado, no nuevo) | Introducido en | Uso en este capítulo |
|---|---|---|
| `CapabilityDescriptor` | CH-08 §6 | citado en prosa (seccion 1/2/3/5/15) para trazar la frontera más importante de este capítulo — nunca usado dentro del pseudocódigo |
| `AgentConfig` | CH-00 §6 | citado en prosa (seccion 1/2/3/15) para trazar la separación que `P-07` exige respecto a la identidad del agente — nunca usado dentro del pseudocódigo |

### Un identificador opaco nuevo

Siguiendo el mismo patrón que CH-00 §6 estableció para los identificadores fundamentales, y que
CH-08..CH-23 repitieron para los suyos:

| Identificador (nuevo de este capítulo) | Identifica |
|---|---|
| `SkillId` | un `SkillDescriptor` concreto — el registro de conocimiento procedural reusable que `resolveSkillForSituation` produce cuando encuentra una coincidencia |

### `ErrorCategory` — sin cambios en este capítulo

A diferencia de la mayoría de los componentes de Amendment v1.1 (CH-14..CH-23), que agregaron cada
uno un valor nuevo a `ErrorCategory`, este capítulo evaluó explícitamente agregar un valor `SKILL` —
y lo descartó por el mismo argumento que `CapabilityRegistry` (CH-08 §13) ya usó para no agregar un
valor `CAPABILITY`: el único fallo real de este capítulo (`SKILL_NOT_FOUND`, seccion 13) es un fallo
de validación de la *entrada* (un `situationName` que no corresponde a nada registrado), no un fallo
de una *ejecución*. `ErrorCategory` (CH-00 §6) sigue teniendo, después de este capítulo, exactamente
los mismos veintiún valores que dejó CH-23 §6 — ver seccion 13 para el razonamiento completo.
`HarnessError` (C-011) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00.

### `AgentEventType` — extendida, sin redefinir `AgentEvent`

CH-23 dejó `AgentEventType` en treinta y cuatro valores. Este capítulo agrega dos valores — los
primeros que observan la resolución de una skill, no de una capability, ni de ninguna otra
resolución previa:

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
    SKILL_RESOLVED
    SKILL_RESOLUTION_FAILED
END
```

`AgentEvent` (C-010) no cambia: solo el rango de valores permitido para `eventType` crece, igual que
en cada capítulo anterior salvo `EventBus` (CH-09), `AdmissionController` (CH-14) y
`AgentCommunicationGateway` (CH-15).

### `SkillDescriptor` — el registro estructurado que `P-07` exige

```pseudocode
STRUCT SkillDescriptor
    skill: SkillId
    name: Text
    version: Text
    procedureRef: Text
    appliesTo: Optional<Text>
END
```

Cinco campos — deliberadamente la misma cantidad y, en gran parte, la misma forma que
`CapabilityDescriptor` (C-018, CH-08 §6: `capability`, `name`, `version`, `inputSchema`,
`implementationRef`) — cada uno respondiendo a una parte exacta del alcance decidido para este
capítulo: `skill` es el identificador ya resuelto que este descriptor produce — mismo patrón que
`capability: CapabilityId` en `CapabilityDescriptor`, nunca un `SkillDescriptorId` separado de fila;
`name` es el nombre canónico contra el que se compara `situationName` (texto libre, sin garantía de
formato); `version` es una versión explícita (`Text`, p. ej. `"1.0.0"`) — reusa el mismo criterio de
versionado que `CapabilityDescriptor.version` y `P-26` ya establecieron (ver nota más abajo);
`procedureRef` es, deliberadamente, una referencia opaca (`Text`) al procedimiento/guía real — nunca
su contenido completo en prosa, que queda fuera de alcance de este capítulo; `appliesTo` es
`Optional<Text>`, una referencia opaca y opcional a qué capabilities o situaciones más amplias aplica
esta skill.

**Por qué esta forma deliberadamente se parece a `CapabilityDescriptor`, y por qué eso NO las
convierte en el mismo concepto.** Se evaluó explícitamente dar a `SkillDescriptor` una forma
completamente distinta —para evitar cualquier apariencia de que es "una capability con otro
nombre"— y se descartó: la simetría de forma es precisamente lo que hace legible el contraste que
este capítulo necesita trazar (la misma disciplina editorial que `HandoffStatus` de tres estados,
CH-23, usó deliberadamente CONTRA la forma de dos estados de `HumanInteractionStatus`, para señalar
una diferencia real). Aquí la señal es la inversa: la forma es intencionalmente parecida porque el
riesgo real no es que se confundan visualmente, sino que se confunda su TRATAMIENTO — por eso la
distinción que de verdad importa no vive en la forma del `STRUCT`, sino en qué produce
`resolveSkillForSituation` (seccion 11) frente a qué produce `resolveToolCall` (CH-08 §11): uno
nunca es una acción; el otro siempre lo es.

**Por qué `version` reusa el criterio de `P-26`/`CapabilityDescriptor.version`, sin que `P-26` en sí
se extienda a este contrato.** `P-26` ("Capabilities have governed lifecycles") declara, literalmente,
"Tools/capabilities MUST support explicit versions..." — un texto que no menciona skills. Se evaluó
explícitamente citar `P-26` como parte del impacto constitucional de `SkillDescriptor` — y se
descartó: extender la cita literal de un principio a una entidad que ese principio no nombra sería
la misma clase de sobre-extensión que este libro ya evitó en otros capítulos (p. ej. CH-23 nunca citó
`INV-14` en su propio `frontmatter` aunque el mismo principio de fondo aplicaba). En su lugar, este
capítulo **reusa el mismo criterio de diseño** — una versión explícita como `Text`, sin implementar
todavía compatibility policy, rollout, deprecation ni retirement — por consistencia de ingeniería,
no por cita constitucional nueva (ver seccion 18).

**Por qué `procedureRef` es una referencia opaca `Text`, y no un campo que embeba el contenido
completo del procedimiento.** Se evaluó explícitamente modelar el procedimiento real como un `Text`
largo con el paso a paso completo, o como una `STRUCT` estructurada de pasos — y se descartó por dos
razones. Primera: el contenido real de un procedimiento reusable puede ser arbitrariamente extenso,
versionarse por su cuenta, o vivir en un sistema de autoría completamente distinto (el mismo
argumento que ya motivó `CapabilityDescriptor.implementationRef`, CH-08, a preferir una referencia
sobre el código real). Segunda: `SkillLibrary` no necesita conocer el contenido real de un
procedimiento para cumplir su propia responsabilidad —resolver cuál aplica—, preservando la misma
independencia de contratos que Article III ya exige en todo el libro. `procedureRef` es,
deliberadamente, el mismo patrón de referencia opaca que `implementationRef` (CH-08) y `contextRef`
(CH-23), aplicado aquí a un propósito distinto: apuntar, sin duplicar, al procedimiento real.

**Por qué `appliesTo` es `Optional<Text>` opaco, y no `List<CapabilityId>`.** Se evaluó
explícitamente modelar `appliesTo` como `List<CapabilityId>` — una lista real de las capabilities a
las que esta skill aplicaría, aprovechando que `CapabilityId` ya existe desde CH-02 — y se descartó:
eso obligaría a este capítulo a modelar, con código real, la relación estructurada entre una skill y
un conjunto de capabilities, una responsabilidad que su alcance decidido no incluye (y que
correspondería, si se necesitara, a un capítulo de integración futuro). `appliesTo` queda, en cambio,
como una referencia opaca y opcional — reconoce que la pregunta "¿a qué aplica esta skill?" existe,
sin resolver su mecanismo real, mismo tratamiento que `HandoffPackage.contextRef` (CH-23) dio a una
pregunta análoga.

**Unchanged / Not yet introduced**: `CapabilityDescriptor` (C-018, CH-08) y `AgentConfig` (C-002,
CH-00) no cambian de forma — ninguno de los dos gana un campo que referencie `SkillDescriptor`
(ver seccion 9/18).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce un contrato de
datos, registrado en `registry/contracts.yaml`:

```text
ID:                     C-035
Name:                   SkillDescriptor
Version:                v1
Introduced In:          CH-24
Current Definition:     STRUCT SkillDescriptor (ver §6)
Used By:                [CMP-022]
Modified By:            []
Constitutional Impact:  [P-07, INV-19]
```

`C-035` es el vigesimosegundo id que este libro asigna sin que estuviera reservado desde CH-01 §7 —
el correlativo simplemente continúa después de `C-034` (CH-23). No colisiona, por nombre, con ningún
contrato ya registrado — verificado con grep completo sobre `registry/contracts.yaml` antes de
escribir este capítulo. El nombre `SkillDescriptor`, y no `Skill` a secas, es deliberado —
`SkillDescriptor` es, específicamente, el registro de datos concreto que representa el conocimiento
procedural (Article I, `P-07`) dentro del runtime, la misma disciplina de nombres que ya distinguió
`CapabilityDescriptor` (el registro) de "Capability" (el concepto, CH-02).

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el undécimo componente del registry que no corresponde a ninguno de los
once nombres del árbol de Article III ("Agent Runtime") — pertenece, en cambio, a `P-07` de Article
I:

```pseudocode
COMPONENT SkillLibrary
    consumes: ExecutionContext
    produces: SkillDescriptor, AgentEvent, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Article I (`P-07`) — Article III no tiene, todavía, una
sección propia para este componente, exactamente igual que `AdmissionController` (CH-14),
`AgentCommunicationGateway` (CH-15), `CredentialBroker` (CH-16), `IdempotencyGuard` (CH-17),
`OperationalController` (CH-18), `AuditLedger` (CH-19), `DataGovernanceEngine` (CH-20),
`ExecutionFabricAdapter` (CH-21), `EvaluationHarness` (CH-22) y `HandoffCoordinator` (CH-23):

```text
COMPONENT: SkillLibrary

Responsibility:
    Registrar el descriptor de una skill — conocimiento procedural reusable, nombre canónico,
    versión y una referencia opaca al procedimiento/guía real — como una capa separada del core del
    agente, de las tools/capabilities y de la identidad del agente, y resolver qué SkillDescriptor
    aplica a una situación nombrada — sin resolver qué implementación concreta satisface una
    capability solicitada, sin representar la identidad/configuración de un agente, sin ejecutar
    ningún side effect y sin decidir autorización sobre ninguna acción.

Consumes:
    C-004 ExecutionContext (solo cuando la resolución ocurre dentro de uno real, ver seccion 11)

Depends on:
    (ninguno todavía — el cableado real hacia AgentCore, CapabilityRegistry, ModelGateway y
    EvaluationHarness es Preview, no introducido en este capítulo; ver seccion 9)

Produces:
    C-035 SkillDescriptor (el descriptor registrado que este componente posee), C-010 AgentEvent
    (SKILL_RESOLVED / SKILL_RESOLUTION_FAILED, condicional, ver seccion 14), C-011 HarnessError

Owns (Article I, cita literal, expandida contra el hallazgo de CH-23):
    - "Skills encode reusable procedural knowledge" (cita literal, título P-07) — "El conocimiento
      procedural reusable debe estar separado del core, las tools y la identidad del agente" (cita
      literal, texto P-07) — registrar, en exclusiva, el descriptor de una skill como conocimiento
      procedural reusable, como una capa separada de AgentCore (identidad), de
      CapabilityRegistry/ToolRuntime (tools/capabilities) y de PolicyEngine (autorización)
    - resolver, contra ese registro, qué SkillDescriptor aplica a una situación nombrada —
      produciendo una referencia consultable a un procedimiento reusable, nunca una acción
      ejecutable ni una implementación de capability
    - rechazar por defecto (fail-closed) una resolución de skill invocada sin un situationName
      real, o cuyo situationName no corresponde a ningún SkillDescriptor registrado

Does NOT own (Article IV — declarado con el mismo peso que Owns):
    - resolver qué implementación concreta satisface una capability solicitada (CapabilityRegistry,
      CMP-008, ya introducido en CH-08 — la frontera más importante de este capítulo:
      CapabilityRegistry resuelve QUÉ CÓDIGO/API concreto ejecuta una acción; SkillLibrary resuelve
      QUÉ PROCEDIMIENTO/GUÍA reusable aplica a una situación — dos preguntas ortogonales, aun cuando
      ambas comparan un nombre de texto libre contra un registro propio)
    - representar la identidad/configuración de un agente (AgentCore, CMP-011, ya introducido en
      CH-11 — AgentConfig, C-002, CH-00, ya representa qué es un agente independiente de cualquier
      run; ningún SkillDescriptor resuelto se embebe jamás dentro de AgentConfig ni de AgentState)
    - ejecutar el side effect en sí de ninguna acción (ToolRuntime, CMP-002, ya introducido en CH-02)
    - decidir autorización sobre ninguna acción, incluida la lectura de una skill (PolicyEngine,
      CMP-005, ya introducido en CH-05)
    - certificar un candidato de skill antes de su promoción a producción (EvaluationHarness,
      CMP-020, ya introducido en CH-22 — EvaluationHarness ya declara evaluable, entre otros
      candidatos, a una skill antes de su promoción controlada; SkillLibrary registra y resuelve una
      skill YA registrada, nunca decide si debe promoverse)
    - generar por sí mismo el contenido procedural real detrás de procedureRef (Preview,
      infraestructura de borde — referencia opaca, mismo patrón que implementationRef en
      CapabilityDescriptor, CH-08)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con la misma
particularidad que los diez componentes de Amendment v1.1 anteriores: ninguna de las cinco
exclusiones de esta lista proviene de una ficha propia de Article III (que no existe para este
componente); provienen de fronteras ya establecidas por componentes ya registrados. La primera
exclusión de esta lista es, deliberadamente, la más parecida en prosa informal a lo que este
componente sí posee — el mismo cuidado editorial que CH-04 §8, CH-19..CH-23 §8 ya aplicaron frente a
su propia frontera más importante.

**Nota sobre Article IV.** Igual que `CapabilityRegistry` (CH-08), `DataGovernanceEngine` (CH-20),
`ExecutionFabricAdapter` (CH-21), `EvaluationHarness` (CH-22) o `HandoffCoordinator` (CH-23),
`SkillLibrary` sí decide algo real —qué `SkillDescriptor` aplica a una situación nombrada— y no
comparte la ausencia de fila de `EventBus` (CH-09) o `AuditLedger` (CH-19), que solo preservan o
distribuyen decisiones ajenas.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
SkillLibrary
    consumes → ExecutionContext
    produces → SkillDescriptor, AgentEvent, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`SkillLibrary` no depende hoy de ningún otro componente registrado — mismo patrón que CH-01..CH-23
ya establecieron para sus propios componentes. En prosa (nunca dentro de un bloque `pseudocode`, per
`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las relaciones futuras que un capítulo
de integración agregaría son:

| Componente futuro (relación inversa — no cableada en este capítulo) | Qué relación tendría con `SkillLibrary` |
|---|---|
| `AgentLoop` (ya existente, CMP-001) | podría consultar, en algún punto de un turno, qué `SkillDescriptor` aplica a la situación actual antes de construir el contexto que ve el modelo — sin que esa consulta implique, jamás, una acción a autorizar |
| `ModelGateway` (ya existente, CMP-003) | podría incluir el `procedureRef` de una skill resuelta como parte del `ModelRequest` (CH-03) que arma para el modelo — una decisión de `ContextEngine` (CH-04), no de `SkillLibrary` |
| `CapabilityRegistry` (ya existente, CMP-008) | permanecería, en su mayor parte, sin relación directa: `resolveToolCall` sigue resolviendo exclusivamente acciones ejecutables — salvo que un capítulo futuro decida correlacionar, vía `appliesTo`, qué `CapabilityDescriptor` se beneficia de qué `SkillDescriptor` |
| `AgentCore` (ya existente, CMP-011) | seguiría, sin cambios, representando la identidad de un agente — ninguna versión futura de `AgentConfig` necesitaría referenciar un `SkillDescriptor` directamente, precisamente porque `P-07` exige la separación que este capítulo instala |
| `EvaluationHarness` (ya existente, CMP-020) | podría certificar un `SkillDescriptor` candidato, vía `subjectRef` (CH-22), antes de que `SkillLibrary` lo acepte como registrado — una secuencia, no una fusión de responsabilidades |
| `EventBus` (ya existente, CMP-009) | podría distribuir, como un `AgentEvent` más, `SKILL_RESOLVED`/`SKILL_RESOLUTION_FAILED` (seccion 14) — exactamente igual que distribuye el de cualquier otro productor |

`registry/components.yaml` de `CMP-001`, `CMP-003`, `CMP-008`, `CMP-011` y `CMP-020` **no se
modifica** en este capítulo: ninguno agrega `CMP-022` a sus `dependencies`, y ninguno cambia su
pseudocódigo. El pseudocódigo de la seccion 11 muestra a `SkillLibrary` resolviendo una skill de
forma completamente autónoma — sin que ningún componente anterior cambie una sola línea para que
este capítulo sea correcto. Ese cableado real de punta a punta es, explícitamente, trabajo de un
capítulo de integración futuro (ver seccion 18/19).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[AgentLoop — consultaría la situación actual de un turno, CH-01, conceptual, todavía no cablea esta
llamada] → SkillLibrary → [SkillDescriptor — el procedimiento resuelto, consultable por cualquier
componente futuro, nunca ejecutable] → [ContextEngine — podría incluirlo en lo que ve el modelo,
CH-04, conceptual]
```

**Vista 2 — Sequence**

```text
situationName: Text (producido, en un flujo real futuro, por AgentLoop o por el propio modelo —
este capítulo no cablea ese origen)
   │
   ▼
SkillLibrary
   │ resolveSkillForSituation(situationName, registeredSkills, execution, agentId)
   │ ¿situationName vacío o NULL? sí → HarnessError (SKILL_RESOLUTION_REQUESTED_WITHOUT_SITUATION)
   │ busca, dentro de registeredSkills, un SkillDescriptor cuyo name coincida con situationName
   │     no encontrado → HarnessError (SKILL_NOT_FOUND, VALIDATION)
   │     encontrado → RETURN ese SkillDescriptor, sin construir ninguna acción
   │ emite: AgentEvent (SKILL_RESOLVED | SKILL_RESOLUTION_FAILED)
   ▼
SkillDescriptor (consultable — nunca algo que ToolRuntime pueda ejecutar ni que PolicyEngine deba
autorizar como una acción)
```

**Vista 3 — Pseudocódigo**

Ver §11: `resolveSkillForSituation` es la primera formalización ejecutable de "`SkillLibrary` decide
qué procedimiento reusable aplica a una situación" — construida exclusivamente a partir de material
que ya existe (`ExecutionContext`/`AgentEvent`/`HarnessError`/`AgentId` desde CH-00) más el
`ENUM`/`STRUCT` nuevos de este capítulo, y contrastada explícitamente, en prosa, contra
`resolveToolCall` (CH-08 §11).

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde CH-00/CH-08.

```pseudocode
FUNCTION resolveSkillForSituation(
    situationName: Text,
    registeredSkills: List<SkillDescriptor>,
    execution: Optional<ExecutionContext>,
    agentId: Optional<AgentId>
) -> SkillDescriptor

    IF situationName == NULL
        missingSituation: HarnessError = HarnessError(
            category = VALIDATION,
            code = "SKILL_RESOLUTION_REQUESTED_WITHOUT_SITUATION",
            message = "resolveSkillForSituation fue invocada sin un situationName real — no existe ninguna situación contra la cual resolver una skill",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW missingSituation
    END

    descriptor: Optional<SkillDescriptor> = NULL

    FOR EACH candidate IN registeredSkills
        IF candidate.name == situationName
            descriptor = candidate
        END
    END

    IF descriptor == NULL
        notFound: HarnessError = HarnessError(
            category = VALIDATION,
            code = "SKILL_NOT_FOUND",
            message = "SkillLibrary no encontró ningún SkillDescriptor registrado para este situationName",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )

        IF execution != NULL AND agentId != NULL
            EMIT AgentEvent(
                eventId = newEventId(),
                eventType = SKILL_RESOLUTION_FAILED,
                timestamp = now(),
                runId = execution.runId,
                sessionId = execution.sessionId,
                agentId = agentId,
                traceId = execution.traceId,
                payload = notFound
            )
        END

        THROW notFound
    END

    IF execution != NULL AND agentId != NULL
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = SKILL_RESOLVED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = descriptor
        )
    END

    RETURN descriptor
END
```

`now()` y `newEventId()` son las mismas primitivas de CH-00..CH-23. `registeredSkills` es una señal
de entrada asumida — el conjunto de `SkillDescriptor` ya registrados llega como parámetro ya poblado
(seccion 6/18): este capítulo modela la **resolución** contra ese registro (el `FOR EACH` que compara
`candidate.name` con `situationName`, real y ejecutable), no el **mecanismo de alta** que lo puebla —
mismo tratamiento exacto que `registeredCapabilities` recibió en `resolveToolCall` (CH-08 §11).

**Contraste explícito con `resolveToolCall` (CH-08 §11) — lo que esta función nunca hace.**
`resolveToolCall(proposal, registeredCapabilities, execution, agentId, argumentsMatchSchema)`
produce un `ToolCall` — una intención de acción con `arguments` que todavía necesita atravesar
`PolicyEngine.evaluate` (CH-05) y, si se autoriza, `ToolRuntime.execute` (CH-02); no producirlo
detiene, en la práctica, cualquier efecto sobre el mundo. `resolveSkillForSituation` produce un
`SkillDescriptor` — una referencia consultable a un procedimiento, sin `arguments`, sin ningún campo
que represente una acción pendiente. Nótese lo que esta función **nunca hace**: no construye ningún
`ToolCall`, no invoca `PolicyEngine.evaluate` (CH-05) sobre el resultado —un `SkillDescriptor`
resuelto nunca necesita autorización para ser CONSULTADO, exactamente porque consultarlo no es una
acción—, y no invoca `ToolRuntime.execute` (CH-02) ni ningún otro mecanismo de side effect. Si un
capítulo futuro decidiera que un agente debe SEGUIR el procedimiento que `procedureRef` referencia
—por ejemplo, ejecutando una secuencia de tool calls que la guía describe—, esas tool calls
resultantes pasarían, cada una, por `CapabilityRegistry.resolveToolCall` y por `PolicyEngine.evaluate`
exactamente como cualquier otra — pero eso sería un capítulo de integración distinto, no una
responsabilidad de `resolveSkillForSituation` en sí.

**Ningún componente de este libro invoca todavía, de verdad, `resolveSkillForSituation`** (ver
seccion 9/18) — mismo tratamiento explícito que CH-08 §11 ya dio a `resolveModelProposedToolCall` y
CH-23 §11 dio a su propio ejemplo con `ControlDirective`: esta función es una demostración autónoma
de que el mecanismo funciona, no una integración cableada dentro de un flujo real.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no modifica `AgentRunStatus` (C-013), `AgentConfig` (C-002) ni `CapabilityDescriptor`
(C-018): los tres siguen siendo, sin cambios, exactamente lo que sus propios capítulos dejaron.

`SkillDescriptor` (C-035, seccion 6) **no introduce ningún lifecycle de estados propio** — a
diferencia de `HandoffPackage` (`HandoffStatus`, CH-23) o `EvaluationReport` (`EvaluationOutcome`,
CH-22), un `SkillDescriptor` no representa un proceso que avanza por estados: representa un registro
que, en un momento dado, existe dentro de `registeredSkills` o no existe. `resolveSkillForSituation`
(§11) atraviesa un camino implícito con dos desenlaces, sin que este capítulo lo formalice como una
máquina de estados nueva (eso introduciría una segunda entidad nueva, fuera del alcance decidido para
este capítulo):

```text
situationName recibido
   → situationName ausente                    → HarnessError (SKILL_RESOLUTION_REQUESTED_WITHOUT_SITUATION)
   → situationName sin descriptor registrado   → HarnessError (SKILL_NOT_FOUND)
   → descriptor encontrado                     → SkillDescriptor (retornado sin ninguna transición)
```

**Por qué este capítulo no declara un lifecycle de versiones para `SkillDescriptor`.** Se evaluó
explícitamente modelar `rollout`/`deprecated`/`retired` como estados de un `SkillDescriptor` — el
mismo lifecycle completo que `P-26` exige, en su literal, para capabilities — y se descartó
deliberadamente por la misma razón que la seccion 6 ya explicó: `P-26` no nombra a las skills, y
extender su lifecycle completo aquí sería resolver, sin necesidad, un problema que el alcance de
este capítulo no exige todavía (ver seccion 18).

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6, **sin ningún valor nuevo agregado por este capítulo** — ver
seccion 6) clasifica también los dos fallos que introduce este capítulo, fiel a los `Failure
Examples` de `constitution/ARCHITECTURE_CONSTITUTION.md` Article VII:

```text
VALIDATION
    SKILL_RESOLUTION_REQUESTED_WITHOUT_SITUATION  — resolveSkillForSituation invocada sin un
                                                      situationName real (precondición de
                                                      invocación, no un fallo de resolución en sí)
        → recoverable: FALSE, retryable: FALSE
    SKILL_NOT_FOUND                                — ningún SkillDescriptor registrado corresponde
                                                      al situationName solicitado
        → recoverable: FALSE, retryable: FALSE
```

**Por qué ambos fallos reutilizan `VALIDATION`, y por qué este capítulo no agrega una categoría
`SKILL` nueva.** Se evaluó explícitamente introducir `SKILL` como una categoría nueva de
`ErrorCategory` — el patrón que la mayoría de los componentes de Amendment v1.1 (CH-14..CH-23) sí
siguieron — y se descartó, siguiendo en cambio el precedente que `CapabilityRegistry` (CH-08 §13) ya
sentó para su propio `CAPABILITY_NOT_FOUND`: `ErrorCategory` (CH-00 §6) ya distingue `VALIDATION` (un
dato de entrada no cumple una forma esperada) de `TOOL` (una capability ya resuelta falla durante su
ejecución); un `situationName` inexistente o ausente es, en ambos casos, un fallo de validación de la
*entrada*, no un fallo de una *ejecución* que este capítulo ni siquiera modela. Introducir una
categoría nueva solo para distinguir "quién" detectó el problema (`SkillLibrary` en vez de
`CapabilityRegistry`) fragmentaría `ErrorCategory` sin ganancia semántica real — el mismo argumento,
palabra por palabra, que CH-08 §13 ya usó.

`resolveSkillForSituation` nunca devuelve una excepción cruda ni un `SkillDescriptor` a medias cuando
la resolución falla: siempre construye un `HarnessError` con `category`, `recoverable` y `retryable`
explícitos — mismo patrón que cada función de CH-00..CH-23. A diferencia de la precondición de
invocación (`SKILL_RESOLUTION_REQUESTED_WITHOUT_SITUATION`, que interrumpe la función con `THROW` sin
`EMIT` — mismo patrón que `RESOLUTION_REQUESTED_WITHOUT_PROPOSAL`, CH-08), el caso `SKILL_NOT_FOUND`
sí emite un `AgentEvent` antes de lanzar el error (cuando `execution`/`agentId` están resueltos): es
el resultado de una resolución que sí llegó a ejecutarse, no la violación de una precondición de
invocación.

**La distinción más importante de esta sección**: este fallo no se clasifica como `TOOL` (CH-02,
propio de una capability ya resuelta que falla al ejecutarse) — aunque, en prosa informal, "no
encontrar algo en un registro" pueda sonar parecido en ambos casos, la diferencia no es la forma del
fallo, es su naturaleza: `SKILL_NOT_FOUND` es un error de resolución de una guía consultable, nunca el
fallo de una ejecución real — esa clase de fallo sigue siendo, sin ambigüedad, `TOOL`, exactamente
como lo era antes de este capítulo.

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo real del contenido detrás de
`procedureRef` —un procedimiento que ya no existe en el sistema de autoría real, una guía
corrupta o inconsistente— sigue, después de este capítulo, sin que `SkillLibrary` lo ejercite nunca
(mismo límite que CH-08..CH-23 ya documentaron para sus propias primitivas asumidas).

## 14. Eventos Producidos (Events Produced)

`SkillLibrary` emite `AgentEvent` de forma condicional desde su única función real, agregando
`SKILL_RESOLVED`/`SKILL_RESOLUTION_FAILED` a `AgentEventType` (seccion 6), emitidos únicamente cuando
`execution` y `agentId` llegan ambos resueltos (mismo patrón condicional que `CapabilityRegistry`,
CH-08, `OperationalController`, CH-18, `DataGovernanceEngine`, CH-20, `ExecutionFabricAdapter`,
CH-21, `EvaluationHarness`, CH-22, y `HandoffCoordinator`, CH-23).

**Por qué la emisión es condicional.** Mismo argumento que `CapabilityRegistry` (CH-08 §14): un
`AgentEvent` (C-010) exige `runId`/`sessionId`/`agentId`/`traceId` genuinos, y no toda resolución de
skill ocurre necesariamente dentro de un `ExecutionContext` con esos cuatro campos ya resueltos en el
instante exacto en que se invoca `resolveSkillForSituation`.

**Por qué, incluso cuando emite, este evento no es evidencia de auditoría — frontera explícita con
`AuditLedger` (CH-19).** `payload = descriptor` (o `payload = notFound`) transporta una copia del
resultado ya producido — pero, exactamente igual que `CAPABILITY_RESOLVED`/`CAPABILITY_RESOLUTION_FAILED`
(CH-08 §14), queda sujeto a las mismas garantías (o ausencia de garantías) que cualquier otro
`AgentEvent`: `EventBus` podría distribuirlo, perderlo si nadie está suscrito, o nunca llegar a
existir si `execution`/`agentId` no estaban resueltos. Si alguien necesitara, en cambio, evidencia
estructuralmente inmutable de que una skill concreta se resolvió, esa es, sin ambigüedad, una
responsabilidad de `AuditLedger` (CH-19) — nunca de este evento condicional.

**Por qué esto no es una limitación real hacia `INV-18`.** La acción verdaderamente significativa de
este capítulo —producir un `SkillDescriptor` consultable para un `situationName`— ya se cumple con el
`RETURN` directo de `resolveSkillForSituation` a quien la invoca, sin depender de
`AgentEvent`/`EventBus` para "existir". El `AgentEvent` condicional es, aquí, una conveniencia de
observabilidad adicional, nunca el mecanismo que hace el resultado real.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

`SkillLibrary` es el primer componente de este libro cuya responsabilidad completa es el
conocimiento procedural reusable de una skill, deliberadamente separado de toda ejecución.

**La distinción con `CapabilityRegistry` (CH-08), explícita, completa y la más importante de este
capítulo.** `CapabilityRegistry.resolveToolCall` (CH-08) resuelve un nombre de texto libre contra un
registro de implementaciones ejecutables, produciendo un `ToolCall` que existe, precisamente, para
pasar por `PolicyEngine.evaluate` y por `ToolRuntime.execute` — un resultado que, por diseño,
SIEMPRE es una acción pendiente. `SkillLibrary.resolveSkillForSituation` (este capítulo) resuelve un
nombre de texto libre contra un registro de guías reusables, produciendo un `SkillDescriptor` que
NUNCA es una acción — es, en todo momento, una referencia para consultar, no para ejecutar. Las dos
preguntas son, literalmente, independientes: una situación puede resolver una skill sin que eso
implique ninguna capability involucrada (una guía puramente de razonamiento, sin ningún side effect
sobre el mundo), y una capability puede resolverse y ejecutarse sin que exista ninguna skill asociada
(una acción simple, sin ningún procedimiento reusable de por medio). Si `CapabilityRegistry`
absorbiera la resolución de skills —ya que de todos modos "resuelve un nombre contra un registro"—,
la premisa completa de CH-08 §15 (que una resolución exitosa nunca implica autorización, PERO sí
implica una acción candidata a autorizarse) dejaría de ser universalmente cierta para todo lo que
`CapabilityRegistry` produce, exactamente el mismo tipo de conflación que CH-22 §15 y CH-23 §15 ya
trazaron, con matices distintos, para "evaluar" y para "un humano interviene aquí".

**La distinción con `AgentCore` (CH-11), precisa y necesaria.** `AgentCore` ya representa, a través
de `AgentConfig` (C-002, CH-00), la identidad estable de un agente — pero CH-11 §8 nunca declaró la
responsabilidad de representar ningún conocimiento procedural que ese agente pudiera consultar;
`P-07` exige, literalmente, que esa separación se mantenga. `SkillLibrary` no decide jamás qué agente
existe, ni modifica `AgentConfig` ni `AgentState`; recibe, en `situationName`, un nombre ya producido
por quien invoca la resolución, sin necesitar conocer la identidad del agente que la solicita más
allá del `agentId` opcional que usa exclusivamente para observabilidad condicional (seccion 14).

**La distinción con `EvaluationHarness` (CH-22), heredada y aplicada aquí con precisión.**
`EvaluationHarness` (CMP-020, CH-22 §8) ya declara evaluable, entre otros candidatos, "una skill"
antes de su promoción controlada a producción — pero esa certificación ocurre ANTES de que exista
ningún registro real que la resuelva; este capítulo instala, por fin, ESE registro. `SkillLibrary` no
certifica nada, no aplica ninguna `RiskClass`, y no produce ningún `EvaluationReport` — simplemente
registra y resuelve lo que, en algún momento anterior, pudo o no haber pasado por esa certificación
(una secuencia posible, nunca cableada por este capítulo, ver seccion 9/18).

**`P-13`, extendido a la resolución de una skill con la misma disciplina que todo el libro.**
`resolveSkillForSituation` no recibe ninguna entrada que el modelo haya producido con autoridad
propia — el `situationName` que recibe se trata como texto no confiable, exactamente como
`capabilityName` en CH-08: si no corresponde a ningún `SkillDescriptor` registrado, la resolución
falla, sin importar cuán plausible parezca el nombre propuesto. El modelo no decide qué skills
existen, no puede registrar una nueva por su cuenta, y no puede, bajo ninguna circunstancia, alterar
un `SkillDescriptor` ya registrado.

**Límite que este capítulo deja explícitamente abierto.** `resolveSkillForSituation` no modela ningún
control de acceso sobre **quién** puede invocarla, ni sobre **quién**, después, puede leer un
`SkillDescriptor` ya resuelto — cualquier llamador puede, en este capítulo, resolver cualquier
`situationName` contra el registro completo. Autorizar la lectura y la escritura (el alta) de este
contrato queda, explícitamente, fuera de alcance de este capítulo — el mismo límite que
`CapabilityRegistry` (CH-08 §15), `AuditLedger` (CH-19 §15), `DataGovernanceEngine` (CH-20 §15),
`ExecutionFabricAdapter` (CH-21 §15), `EvaluationHarness` (CH-22 §15) y `HandoffCoordinator` (CH-23
§15) ya dejaron abierto para sus propios registros.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST ResolveSkillForSituationRejectsAMissingSituationName
TEST ResolveSkillForSituationNeverProducesADescriptorForAnUnregisteredSituationName
TEST ResolveSkillForSituationNeverProducesAToolCallOrAnythingResemblingOne
TEST ResolveSkillForSituationNeverInvokesPolicyEngineOrToolRuntime
TEST ResolveSkillForSituationAlwaysEmitsAnAgentEventOnResolutionOrFailureWhenContextIsResolved
TEST SkillNotFoundReusesValidationRatherThanANewErrorCategory
TEST SkillLibraryNeverModifiesAgentConfigOrCapabilityDescriptor
TEST SkillDescriptorProcedureRefIsAlwaysAnOpaqueReferenceNeverFullProseContent
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (después de CH-24 — P-07 materializado por primera vez con código real; P-09 queda,
deliberadamente, sin cerrar — decisión editorial distinta, para otra sesión)

Constitution
 ├── Article I      — Foundational Principles (P-07 citado por primera vez con código real fuera de
 │                     la transcripción de CH-00 — verificado programáticamente antes de escribir
 │                     este capítulo, ver apertura y seccion 19)
 └── Article IV     — Decision Ownership (tabla original sin cambios; SkillLibrary, como
                       CapabilityRegistry/DataGovernanceEngine/ExecutionFabricAdapter/
                       EvaluationHarness/HandoffCoordinator, decide algo real — no comparte la
                       ausencia de fila de EventBus/AuditLedger)

Contracts (registry/contracts.yaml)
 ├── C-001..C-034  (sin cambios — CH-00..CH-23)
 └── C-035 SkillDescriptor   (CH-24, nuevo — el registro estructurado de conocimiento procedural
                    reusable, P-07/INV-19)

Components (registry/components.yaml)
 ├── CMP-001..CMP-021  (sin cambios — CH-01..CH-23)
 └── CMP-022 SkillLibrary  (CH-24, nuevo — undécimo componente de este registry que no corresponde
                    a ninguno de los once nombres de Article III)
```

**Verificación de cobertura constitucional — resultado real, no asumido.** El encargo de este
capítulo partía de la premisa (heredada de CH-23 §17/§19) de que `P-07` y `P-09` eran las dos únicas
reglas de la Constitution que ningún capítulo anterior había citado nunca con código real, y que
cerrar `P-07` en este capítulo dejaría exclusivamente `P-09` pendiente — una decisión editorial
distinta, deliberadamente fuera de alcance de este mismo capítulo (ver apertura). Antes de escribir
la seccion 19, se ejecutó un barrido programático propio, contra el campo estructurado
`frontmatter.constitutional_articles` de los veinticuatro `chapter.md` anteriores (CH-00..CH-23) —no
un grep de texto completo, que la apertura de este capítulo ya mostró contaminado por la propia
mención en prosa de `P-07`/`P-09` que CH-23 hace al documentar el hallazgo que dejó abierto—, y el
resultado confirma la premisa exactamente: `P-07` y `P-09` eran, en efecto, las únicas dos reglas sin
ninguna cita real fuera de la transcripción de CH-00. Ver seccion 19 para el comando exacto y su
salida completa.

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **`P-09`** ("Single-agent reliability precedes multi-agent complexity"): la última regla de la
  Constitution que, tras este capítulo, sigue sin ninguna cita real — un principio de secuenciación
  arquitectónica de todo el libro, no una responsabilidad que un componente pueda poseer, y
  explícitamente fuera de alcance de este capítulo por decisión del propio encargo (ver apertura).
  Cerrarlo, si se decide hacerlo, es trabajo de una decisión editorial distinta.
- **El cableado real hacia `AgentLoop`, `ModelGateway`, `AgentCore`, `CapabilityRegistry` y
  `EvaluationHarness`**: ningún componente anterior invoca todavía, de verdad,
  `resolveSkillForSituation` — el pseudocódigo de la seccion 11 prueba que el mecanismo funciona y
  que su resultado nunca se confunde con el de `resolveToolCall` (CH-08), no que ya esté conectado
  dentro de un flujo real.
- **El mecanismo real de registro/alta de skills**: `registeredSkills` llega como parámetro ya
  poblado (§6/§11) — este capítulo no modela quién registra un `SkillDescriptor` nuevo, ni dónde se
  persiste ese registro entre ejecuciones. No existe ningún `SkillRegistrationRequest`, ninguna API
  administrativa ni ningún mecanismo de descubrimiento automático de skills.
- **El contenido real detrás de `procedureRef`**: cómo, en la práctica, se autoría, se almacena o se
  versiona el procedimiento real que esta referencia opaca apunta — asumido como una señal de
  entrada ya resuelta, no construido (Preview, infraestructura de borde). Este mismo repositorio
  contiene, como inspiración conceptual sin modelarse literalmente en el libro,
  `skills/*/SKILL.md` — conocimiento procedural real, distinto de cualquier capability/tool.
- **La relación estructurada real entre una skill y las capabilities/situaciones a las que aplica**:
  `appliesTo: Optional<Text>` reconoce la pregunta sin resolverla — no existe todavía ningún
  mecanismo que, a partir de una skill resuelta, produzca una lista real de `CapabilityDescriptor`
  relacionados.
- **Capability/Skill lifecycle completo (`P-26`, más allá del criterio de versionado reusado)**:
  compatibility policy, rollout, deprecation y retirement de una skill quedan fuera de alcance; no
  existe ningún mecanismo que rechace una versión deprecada de una skill ni que gestione una
  migración entre versiones.
- **Autorización de lectura/escritura sobre el propio `SkillDescriptor`**: quién puede registrar uno
  o consultar uno ya resuelto — señalado explícitamente en la seccion 15, no resuelto (mismo límite
  abierto que `CapabilityRegistry`, CH-08 §15, y cada componente de Amendment v1.1 dejaron para sus
  propios registros).
- **Que un agente efectivamente SIGA el procedimiento que una skill resuelta describe**: fuera de
  alcance por diseño (seccion 8, `does_not_own`; seccion 11, contraste con `resolveToolCall`) — este
  capítulo modela la RESOLUCIÓN de qué skill aplica, nunca la ejecución de lo que esa skill describe.
- Reviewers plurales, evals reales, y orquestación multi-agente propiamente dicha: explícitamente
  fuera de alcance de BH-v0.1, igual que en todos los capítulos anteriores.

## 19. Siguiente Incremento (Next Increment)

Con este capítulo, `P-07` —la mitad del encargo heredado de CH-23— tiene, por fin, al menos un
capítulo real que la cita con código: verificado, antes de escribir esta sección, contra el mismo
comando estructurado que la apertura de este capítulo ya mostró:

```text
$ node -e '
const fs = require("fs");
const path = require("path");
for (const d of fs.readdirSync("book/chapters")) {
  if (d === "00-arquitectura-constitucion") continue;
  const raw = fs.readFileSync(path.join("book/chapters", d, "chapter.md"), "utf8");
  const m = raw.match(/constitutional_articles:\s*\[([^\]]*)\]/);
  const ids = m ? m[1].split(",").map(s => s.trim()) : [];
  if (ids.includes("P-07")) console.log("P-07 en", d, ids);
  if (ids.includes("P-09")) console.log("P-09 en", d, ids);
}
'
P-07 en 24-skill-library ['P-07', 'P-13', 'INV-18', 'INV-19', 'INV-20']
(sin más salida — P-09 sigue sin aparecer en el frontmatter.constitutional_articles de ningún
capítulo real, CH-01..CH-24)
```

El resultado, honesto: `P-07` queda, por fin, citado con código real por un capítulo que no es CH-00.
`P-09` ("Single-agent reliability precedes multi-agent complexity") permanece, deliberadamente, sin
cerrar — no porque este capítulo lo haya olvidado, sino porque el encargo que lo motivó fue explícito:
`P-09` es un principio de secuenciación arquitectónica de todo el libro, no un componente, y cerrarlo
exige una decisión editorial distinta sobre CÓMO materializar en código un principio que habla sobre
el ORDEN en que este libro resuelve sus propios problemas — una decisión que otra sesión tomará
después.

El problema natural del próximo incremento tiene, por lo tanto, varios caminos igualmente legítimos:
decidir cómo (o si) materializar `P-09` con código real, más allá de lo que
`AgentCommunicationGateway` (CH-15) ya cubre para interoperabilidad entre agentes; cablear, por fin,
alguno de los muchos puntos de integración que este capítulo y los diez anteriores de Amendment v1.1
dejaron explícitamente como deuda (seccion 18) — que `AgentLoop` invoque de verdad
`resolveSkillForSituation` en algún punto de un turno, que `ContextEngine` decida si y cómo incluir
un `procedureRef` resuelto dentro de lo que ve el modelo, o que `EvaluationHarness` certifique de
verdad un `SkillDescriptor` candidato antes de que `SkillLibrary` lo acepte como registrado.

`next_chapter` queda en `null` en el frontmatter de este capítulo porque, en este momento del libro,
ese próximo capítulo todavía no existe como archivo — solo como el conjunto de problemas,
constitucionales y de integración, que motivarían su escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg / Bucles
> de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows), secciones
> que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): `P-07` nunca fue citado con código real, ni siquiera en el
   propio `frontmatter.constitutional_articles` de ningún capítulo real, por ningún capítulo anterior
   a este — verificado contra la señal estructurada correcta, no contra un grep de texto libre
   contaminado por la propia meta-discusión de CH-23 sobre el mismo hallazgo.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): un componente que ya
   resuelve "un nombre de texto libre contra un registro conocido" (`CapabilityRegistry`, CH-08)
   puede leerse, por comodidad, como si ya cubriera cualquier resolución futura de esa misma forma —
   hasta que aparece una resolución cuyo RESULTADO es de un tipo completamente distinto (una guía
   para consultar, no una acción para ejecutar).
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `SkillLibrary` con una ficha que declara tanto lo que posee (`owns`: registrar y resolver
   conocimiento procedural reusable) como lo que explícitamente NO posee (`does_not_own`: resolver
   qué implementación satisface una capability — `CapabilityRegistry`, ya resuelto).
4. **Modelos mentales** (= §4, Constitutional Impact): "resolver un nombre contra un registro" no es
   una sola pregunta — es, como mínimo, dos preguntas con TIPO DE RESULTADO distinto, y la forma
   parecida de dos contratos (`SkillDescriptor`/`CapabilityDescriptor`) puede, deliberadamente, hacer
   más legible un contraste sin volverlos el mismo concepto.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que una resolución nueva compara "un nombre contra un
  registro conocido", crece la tentación de asumir que `CapabilityRegistry` (CH-08) ya cubre
  cualquier resolución futura de esa misma forma, hasta que un sistema real necesita, de verdad,
  resolver conocimiento procedural reusable y descubre que el resultado de `CapabilityRegistry` es,
  por diseño, siempre una acción — nunca una guía.
- **Bucle de equilibrio (estabiliza):** `resolveSkillForSituation` (§11) nunca acepta invocarse sin
  un `situationName` real, y nunca produce algo parecido a un `ToolCall` — cerrando, con el mismo
  principio fail-closed y la misma disciplina de tipos de resultado, el bucle que este capítulo abre.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `SkillDescriptor` (`C-035`) nunca se confunda,
ni en su forma ni en su tratamiento, con `CapabilityDescriptor` (`C-018`) — `resolveSkillForSituation`
produce una referencia consultable, nunca una acción, y por eso nunca pasa por `PolicyEngine.evaluate`
ni por `ToolRuntime.execute`. Mantener esta independencia es la forma en que este capítulo hace real
la separación que `P-07` exige por diseño de contratos, no solo por convención documentada —
exactamente como CH-08 lo hizo para `P-03`/`P-13`, y CH-23 lo hizo para `INV-E12`.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo de
> esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set` (frontmatter) y
> es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa, para lectura directa
> del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Ya existe un componente que resuelve, de forma determinística, qué implementación concreta
   corresponde a un nombre de capacidad solicitado. ¿Es la misma pregunta, formulada sobre otro
   sustantivo, resolver qué procedimiento reusable aplica a una situación? *(cierra la pregunta guía
   1)*
2. Ya existe un componente que representa la identidad/configuración estable de un agente. ¿Dónde
   debería vivir un procedimiento reusable que muchas situaciones necesitan consultar, sin
   duplicarse dentro de esa identidad? *(cierra la pregunta guía 2)*
3. Si resolver cuál procedimiento aplica a una situación produce una referencia a una guía, nunca una
   acción, ¿debería ese resultado pasar por el mismo mecanismo que decide si una acción está
   permitida? *(cierra la pregunta guía 3)*
4. Cuando el nombre de una situación no corresponde a ningún procedimiento ya conocido, ¿debería el
   mecanismo de resolución inventar una guía plausible? *(cierra la pregunta guía 4)*

### Explicar

1. `SkillLibrary` posee registrar y resolver el conocimiento procedural reusable de una skill.
   Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee resolver qué
   implementación concreta satisface una capability solicitada, aunque ambas resoluciones "buscan un
   nombre en un registro".
2. `SkillDescriptor.procedureRef` es una referencia opaca al procedimiento real, no su contenido
   completo en prosa. Explica qué perderíamos si `SkillLibrary`, en vez de guardar una referencia
   opaca, modelara el texto completo de cada guía dentro de su propio registro.

### Conectar

1. `CapabilityRegistry` (CH-08) ya resuelve un nombre de texto libre contra un registro de
   implementaciones ejecutables, produciendo un `ToolCall`. ¿Por qué el resultado de este capítulo
   nunca podría pasar por `ToolRuntime.execute` ni por `PolicyEngine.evaluate` como si fuera un
   `ToolCall`?
2. `AgentCore` (CH-11) ya representa la identidad de un agente a través de `AgentConfig`. ¿Qué se
   rompería si un `SkillDescriptor` resuelto se embebiera dentro de ese mismo contrato?
3. `EvaluationHarness` (CH-22) ya declara evaluable, entre otros candidatos, a una skill antes de su
   promoción a producción. ¿Esa certificación sustituye, o precede, al registro real que este
   capítulo instala?

### Espaciar

Las cinco tarjetas de repaso de este capítulo (dos sobre `SkillLibrary` — su `owns` y su
`does_not_own` —, dos sobre `SkillDescriptor` — sus campos y por qué su forma se parece
deliberadamente a `CapabilityDescriptor` sin ser el mismo concepto —, y una sobre por qué su único
fallo reutiliza `VALIDATION` en vez de una categoría nueva) entran hoy en `reviewStage = DAY_1`.
Repásalas de nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) — ver el apéndice de tarjetas
al final del libro (edición PDF) o `retrieval_set.flashcards` en `dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te equivocaste,
ese es precisamente el punto ciego que este método existe para revelar.
