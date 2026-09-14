---
id: CH-04
title: "ContextEngine y Qué Ve Realmente el Modelo"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-004]
introduces_contracts: [C-005]
modifies_contracts: []
constitutional_articles: [P-01, P-04, P-12, P-14, INV-02, INV-09, INV-18, INV-19, INV-20]
previous_chapter: CH-03
next_chapter: CH-05
retrieval_set:
  expected_outcome:
    id: EO-CH04
    text: |
      Al terminar este capítulo podrás distinguir, dentro de la construcción del material que un
      turno le presenta al modelo, qué tramo le pertenece en exclusiva al componente que selecciona,
      rankea, compone y compacta ese material dentro de un presupuesto explícito, y qué tramo
      pertenece a dominios distintos (invocación real del modelo, continuación del turno,
      persistencia de historial, autorización sobre qué puede verse) que ya tienen o todavía no
      tienen componente propio — y podrás diseñar, para cualquier conjunto de candidatos de
      contexto, una representación normalizada que registre de dónde vino cada fragmento incluido y
      contra qué presupuesto se validó, sin necesitar resolver todavía cómo ese resultado llega al
      modelo.
  skeleton:
    id: SK-CH04
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
    components_to_be_introduced: [CMP-004]
    contracts_to_be_introduced: [C-005]
  guiding_questions:
    - id: GQ-CH04-01
      text: |
        Ya que el contrato que empaqueta los mensajes de un turno hacia el modelo (ver capítulo
        anterior) explícitamente no decide cuáles incluir ni cómo priorizarlos, ¿quién selecciona,
        dentro de un turno, qué información realmente ve el modelo, y contra qué límite explícito
        valida esa selección?
      answered_by: RQ-CH04-01
    - id: GQ-CH04-02
      text: |
        Si el material candidato para un turno excede el presupuesto disponible, ¿qué debería pasar
        con la información que no cabe completa: descartarse en silencio, resumirse para que quepa,
        o quedar fuera con un registro explícito de que quedó fuera?
      answered_by: RQ-CH04-02
    - id: GQ-CH04-03
      text: |
        Para cada fragmento de información que termina formando parte de lo que el modelo ve,
        ¿por qué necesitamos poder responder de dónde vino, y qué se pierde en auditoría si esa
        procedencia nunca se registra?
      answered_by: RQ-CH04-03
    - id: GQ-CH04-04
      text: |
        ¿Por qué el mismo componente que decide qué información es relevante para el modelo no
        debería decidir, además, si el agente está siquiera autorizado a ver esa información en
        primer lugar?
      answered_by: RQ-CH04-04
  systems_lens:
    iceberg_visible_fact: |
      Sin un dueño explícito para "¿qué debería saber el modelo?", el material que llega a un turno
      crece sin límite real: cada mensaje que alguna vez existió termina, tarde o temprano,
      empaquetado hacia el modelo, porque ningún componente decide activamente qué queda fuera (ver
      seccion 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que, sin un componente con fronteras explícitas, la selección de
      contexto tiende a resolverse por default hacia "incluir todo lo que haya" — no porque alguien
      lo decida, sino porque nadie decide lo contrario — y sin un resultado normalizado, nada en el
      sistema puede auditar después de dónde vino cada fragmento que el modelo efectivamente vio
      (ver seccion 3, Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala el cuarto componente real del libro, `ContextEngine` (CMP-004), con una
      ficha que declara tanto lo que posee (`owns`: selección, ranking, composición, compaction,
      context budgets, provenance — cita literal de Article III) como lo que explícitamente NO posee
      (`does_not_own`: invocar al modelo, decidir continuación del turno, persistir historial de
      sesión, y — la exclusión más sutil de este capítulo — autorizar qué información puede verse) —
      y formaliza `ContextSnapshot` (C-005), el único id que seguía reservado desde CH-01 (ver
      seccion 8, Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es P-01 ("Context is a first-class
      architectural component") junto con P-14 ("Context should be selected, not dumped"): más
      contexto no implica mejor razonamiento, y el harness — no la casualidad de qué mensajes
      seguían en memoria — debe decidir qué entra dentro de un presupuesto explícito (ver seccion 4,
      Impacto Constitucional).
    reinforcing_loop: |
      Cada vez que un componente nuevo se introduce sin declarar explícitamente su `does_not_own`,
      aumenta la probabilidad de que absorba silenciosamente la próxima decisión vecina "porque ya
      estaba ahí" — el mismo bucle que CH-01/CH-02/CH-03 ya cortaron. Este capítulo lo repite para
      `ContextEngine`, con una particularidad: la exclusión de autorización aquí es más fácil de
      confundir que en capítulos anteriores, porque "seleccionar por relevancia" y "autorizar qué
      puede verse" pueden parecer la misma decisión si no se separan explícitamente.
    balancing_loop: |
      `assembleContextSnapshot` (seccion 11) es el mecanismo de equilibrio: nunca copia el material
      candidato completo hacia el resultado — para cada candidato decide si cabe completo, si debe
      compactarse para caber, o si queda explícitamente fuera cuando ni compactado cabe dentro del
      presupuesto — en vez de dejar que el contexto crezca sin límite real.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `ContextSnapshot` registre, por cada
      bloque incluido, tanto su `provenance` como si tuvo que `compacted`-se — en vez de que
      `ContextEngine` devolviera simplemente una lista de contenido ya lista para el modelo sin
      rastro de cómo se construyó. Si esa procedencia se pierde aquí, ningún capítulo futuro (ni
      siquiera uno que introduzca observability más rica) podría reconstruirla después.
  recall_questions:
    - id: RQ-CH04-01
      text: |
        ¿Qué componente selecciona, rankea, compone y compacta el material que un turno le presenta
        al modelo, y qué contrato produce como resultado ya seleccionado?
    - id: RQ-CH04-02
      text: |
        ¿Qué campo de `ContextBlock` (embebido en `ContextSnapshot`) indica que el contenido
        original tuvo que resumirse para caber en el presupuesto, y qué ocurre con un candidato que
        ni siquiera compactado cabe?
    - id: RQ-CH04-03
      text: |
        ¿Qué campo de `ContextBlock` registra la procedencia de cada fragmento incluido, y por qué
        esa procedencia es una responsabilidad literal de Article III para este componente?
    - id: RQ-CH04-04
      text: |
        Según Article IV, ¿qué decisión posee `ContextEngine` y qué decisión relacionada — sobre si
        cierta información puede verse en absoluto — pertenece a un componente distinto, todavía no
        introducido?
  explain_prompts:
    - id: EP-CH04-01
      text: |
        `ContextEngine` posee decidir qué información es relevante para el modelo dentro de un
        presupuesto explícito. Explica, como si hablaras con alguien sin contexto técnico, por qué
        NO posee decidir si el agente está autorizado a ver esa información en primer lugar — ¿qué
        se rompería, en concreto, si `ContextEngine` empezara a decidir también autorización "ya
        que de todos modos es quien procesa la información primero"?
      target_entity: CMP-004
    - id: EP-CH04-02
      text: |
        `ContextSnapshot.blocks` conserva el orden de los candidatos como su ranking, y cada
        `ContextBlock` incluido registra su `provenance` y si tuvo que compactarse. Explica por qué
        esta forma normalizada es preferible a que un componente futuro reciba directamente una
        lista cruda de `AgentMessage` sin ese registro — ¿qué perderíamos, en términos de auditoría,
        si un `ContextSnapshot` no dijera de dónde vino cada fragmento ni si fue resumido?
      target_entity: C-005
  interleaved_questions:
    - id: IQ-CH04-01
      text: |
        Cuando `ContextEngine` produce un `ContextSnapshot` con sus `blocks` ya seleccionados,
        priorizados y compactados, ¿qué campo de `ModelRequest` (`ModelGateway`, CH-03) tendría que
        poblar quien conecte ambos capítulos con el contenido de esos bloques, y qué campo de
        `ExecutionBudget` seguiría reutilizándose sin cambios en ese cableado futuro?
      current_chapter_entities: [CMP-004, C-005]
      prior_chapter_entities: [CMP-003, C-006]
      prior_chapter: CH-03
  flashcards:
    - id: FC-CH04-01
      front: |
        ¿Qué posee `ContextEngine` (Article III / Article IV), en una frase?
      back: |
        Selección, ranking, composición, compaction, context budgets y provenance del material que
        el modelo va a ver — cita literal de Article III, sección "ContextEngine".
      source_entity: CMP-004
      chapter_introduced_in: CH-04
      review_stage: DAY_1
    - id: FC-CH04-02
      front: |
        ¿Qué NO posee `ContextEngine`, y a qué componentes pertenecen esas decisiones?
      back: |
        Invocar al modelo (`ModelGateway`, ya existente), decidir si otro turno debe ocurrir
        (`AgentLoop`, ya existente), persistir/recuperar historial de sesión (`SessionManager`,
        preview) y policy/autorización sobre qué información puede verse (`PolicyEngine`, preview —
        distinto de seleccionar por relevancia, que sí le pertenece a `ContextEngine`).
      source_entity: CMP-004
      chapter_introduced_in: CH-04
      review_stage: DAY_1
    - id: FC-CH04-03
      front: |
        ¿Qué campos tiene `ContextSnapshot` (C-005), y qué representan?
      back: |
        `blocks` (List<ContextBlock>, cada uno con `provenance`/`content`/`compacted` — la
        selección, ranking y compaction ya resueltos), `budget` (ExecutionBudget reutilizado sin
        modificarlo), `estimatedTokens` (Integer, cuánto de ese presupuesto consumió) y
        `producedAt` (Timestamp).
      source_entity: C-005
      chapter_introduced_in: CH-04
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH04-01
      recall_question: RQ-CH04-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH04-02
      recall_question: RQ-CH04-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH04-03
      recall_question: RQ-CH04-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH04-04
      recall_question: RQ-CH04-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 4 — ContextEngine y Qué Ve Realmente el Modelo

> **Regla constitucional (Article I, P-14):** el contexto debe seleccionarse, no volcarse — más
> contexto no implica mejor razonamiento.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de
> saber cómo se llama el componente de este capítulo. El detalle estructurado de esta sección
> vive en `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, dentro de la construcción del
material que un turno le presenta al modelo, qué tramo le pertenece en exclusiva al componente que
este capítulo introduce y qué tramo pertenece a dominios distintos (invocación real del modelo,
continuación del turno, persistencia de historial, autorización sobre qué puede verse) que ya
tienen o todavía no tienen componente propio — y podrás diseñar, para cualquier conjunto de
candidatos de contexto, una representación normalizada que registre de dónde vino cada fragmento
incluido y contra qué presupuesto se validó, sin necesitar resolver todavía cómo ese resultado
llega al modelo.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e
introduce un contrato de datos (`ContextSnapshot` — el único id que seguía reservado desde CH-01) y
el cuarto componente de runtime del libro (`ContextEngine`) — todavía sin explicarlos, solo como
mapa.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar
atrás; están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este
capítulo va a definir):

1. Ya que el contrato que empaqueta los mensajes de un turno hacia el modelo (ver capítulo
   anterior) explícitamente no decide cuáles incluir ni cómo priorizarlos, ¿quién selecciona,
   dentro de un turno, qué información realmente ve el modelo, y contra qué límite explícito valida
   esa selección?
2. Si el material candidato para un turno excede el presupuesto disponible, ¿qué debería pasar con
   la información que no cabe completa: descartarse en silencio, resumirse para que quepa, o quedar
   fuera con un registro explícito de que quedó fuera?
3. Para cada fragmento de información que termina formando parte de lo que el modelo ve, ¿por qué
   necesitamos poder responder de dónde vino, y qué se pierde en auditoría si esa procedencia nunca
   se registra?
4. ¿Por qué el mismo componente que decide qué información es relevante para el modelo no debería
   decidir, además, si el agente está siquiera autorizado a ver esa información en primer lugar?

## 1. Arquitectura Actual (Current Architecture)

CH-00 dejó siete contratos de datos instalados y reservó cinco ids adicionales (`C-005`..`C-009`).
CH-01 agregó `AgentRunStatus` (C-013) y el primer componente de runtime, `AgentLoop` (CMP-001).
CH-02 resolvió `C-008`/`C-009` (`ToolCall`/`ToolResult`) junto con el segundo componente,
`ToolRuntime` (CMP-002). CH-03 resolvió `C-006`/`C-007` (`ModelRequest`/`ModelResponse`) junto con
el tercer componente, `ModelGateway` (CMP-003) — y dejó, explícitamente, un solo id todavía
reservado: `C-005` (`ContextSnapshot`), y un solo componente de Article III que seguía siendo
únicamente un nombre en la tabla de preview: `ContextEngine`.

`ModelRequest` (C-006, CH-03 §6) es explícito sobre el límite de lo que resuelve: "`messages`
transporta los `AgentMessage` (C-001, CH-00) que el turno ya construyó — `ModelRequest` no decide
qué mensajes incluir ni cómo priorizarlos (esa selección es de `ContextEngine`, preview, Article
III); solo empaqueta los que ya llegaron." En la práctica, hasta este capítulo, nada en el libro
decide activamente qué `AgentMessage` deberían llegar a ese empaquetado ni en qué orden — la
pregunta "¿qué debería saber el modelo?" (Article IV: `ContextEngine` → "What should the model
know?") sigue sin respuesta.

`ErrorCategory` (C-011, CH-00 §6) declara, desde la primera versión de la Constitution, un valor
`CONTEXT` — pero ningún componente del libro lo ha usado todavía: los seis valores de
`ErrorCategory` que sí se han ejercitado hasta ahora son `VALIDATION`, `TOOL` (CH-02) y `MODEL`
(CH-03); `CONTEXT`, `POLICY`, `PERSISTENCE`, `INFRASTRUCTURE`, `BUDGET`, `CANCELLATION` y `FATAL`
siguen siendo valores declarados sin ningún fallo real clasificado bajo ellos.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas, "¿qué debería saber el modelo en este turno?" no tiene
un lugar fijo donde vivir — y por default tiende a resolverse hacia "todo lo que exista hasta
ahora". Una implementación puede ir acumulando cada `AgentMessage` que alguna vez se generó dentro
de una sesión y empaquetarlo entero hacia `ModelRequest.messages`, sin ningún límite real más allá
de lo que el proveedor rechace; otra puede recortar mensajes de forma ad hoc en el mismo lugar
donde arma el turno (dentro de `AgentLoop`, violando su propio `does_not_own` de CH-01, o dentro de
`ModelGateway`, violando el suyo de CH-03); una tercera puede resumir contenido que no cabe sin
dejar ningún rastro de qué se resumió ni de dónde venía originalmente cada fragmento que el modelo
sí llegó a ver.

Necesitamos que "¿qué debería saber el modelo?" tenga un dueño único y nombrado — que seleccione
información relevante dentro de un presupuesto explícito (P-14), que registre de dónde vino cada
fragmento que decide incluir (provenance), y que dependa exclusivamente de material que otros
componentes ya producen (`AgentMessage`, `AgentState`, `ExecutionContext`) sin necesitar invocar al
modelo ni decidir la continuación del turno.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los doce contratos y los tres componentes que existen hasta este punto no bastan porque:

- `ModelRequest.messages` (C-006, CH-03) recibe los `AgentMessage` de un turno ya dados — CH-03
  documentó explícitamente que esa selección "es de `ContextEngine`, preview" — pero sin
  `ContextEngine` real, nada en el libro decide activamente qué mensajes llegan hasta ahí ni en qué
  orden; en la práctica, la única política posible hoy es "todo lo que haya", exactamente lo que
  P-14 prohíbe;
- `ContextSnapshot` sigue siendo el único id reservado desde CH-01 §7 sin contrato registrado —
  cualquier capítulo futuro que lo use "por nombre" heredaría una versión ambigua, o peor, cada
  implementación futura lo definiría de forma distinta;
- `ErrorCategory.CONTEXT` (CH-00) sigue siendo un valor declarado sin ningún componente que
  clasifique un fallo real bajo esa categoría — un presupuesto de contexto agotado no tiene, hasta
  este capítulo, ninguna forma normalizada de reportarse;
- nada impide que la selección de información relevante (P-14, un problema de razonamiento) se
  confunda, en el mismo lugar del código, con la pregunta de si esa información puede verse en
  absoluto por razones de autorización (Article IV: `PolicyEngine` → "May this action occur?") —
  dos decisiones de dominios completamente distintos que, sin un componente que las separe, tienden
  a resolverse juntas "porque total, ya estamos mirando el mismo contenido".

> **Nota editorial sobre el outline original.** El outline general de este libro
> (`reference/md/Estructura_Libro_Construyendo_un_Agent_Harness_v0.2.md`, Parte IV, capítulos 7-9)
> fragmenta este territorio en varias piezas — un `ContextBuilder`, una interfaz `ContextProvider`
> con múltiples implementaciones (`GitContextProvider`, `FileContextProvider`, ...), y componentes
> separados `Summarizer`/`Compactor` para el capítulo de context budgets. **Este libro no replica
> esa fragmentación.** La Constitution de este proyecto (`constitution/ARCHITECTURE_CONSTITUTION.md`
> Article III, sección "ContextEngine") asigna selección, ranking, composición, compaction, context
> budgets y provenance a un único componente — sin `Compactor` ni `Summarizer` como componentes
> propios, y sin una interfaz `ContextProvider` formalizada en este capítulo. Este capítulo sigue la
> Constitution de este proyecto, no el outline genérico: `ContextEngine` (CMP-004) es, desde su
> introducción, el dueño exclusivo de todo ese territorio.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la
> secuencia `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una
> entidad que no haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT`
> registrado — **no magic entities**. Este capítulo aplica la misma disciplina de *ownership* que
> CH-01/CH-02/CH-03 ya establecieron: ningún componente puede reclamar en prosa una responsabilidad
> que su propia ficha no declara en `owns` — y, por primera vez en el libro, con tres componentes
> reales ya existentes (`AgentLoop`, `ToolRuntime`, `ModelGateway`) cuyas fronteras `ContextEngine`
> podría invadir por accidente si no se declaran explícitamente.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-01   Context is a first-class architectural component.
           Primera materialización concreta de este principio: existe un ContextEngine real cuya
           ficha (owns: selección, ranking, composición, compaction, context budgets, provenance)
           es, textualmente, la definición operativa de "construido, seleccionado, priorizado,
           resumido, limitado y controlado por el harness" que P-01 exige.
    P-04   Every action produces observable events.
           assembleContextSnapshot (seccion 11) emite un AgentEvent en cada resolución (éxito o
           fallo) — el cuarto componente del libro que produce eventos en la práctica.
    P-12   Events observe; hooks intervene.
           ContextEngine no introduce ningún hook nuevo en este capítulo (a diferencia de
           beforeToolCall/afterToolCall en CH-02) — se preserva sin cambios ni extensión.
    P-14   Context should be selected, not dumped.
           assembleContextSnapshot nunca copia los candidatos completos hacia
           ContextSnapshot.blocks: selecciona dentro de execution.budget.maxInputTokens (C-012,
           reutilizado sin modificarlo), compactando o excluyendo explícitamente lo que no cabe —
           la primera vez que "más contexto no implica mejor razonamiento" tiene un mecanismo real
           en vez de solo una regla declarada.

Invariants preserved
    INV-02   Toda comunicación interna del runtime utiliza contratos propios, incluyendo
             AgentMessage.
             ContextEngine consume AgentMessage (C-001) sin modificarlo y produce ContextSnapshot
             (C-005) — nunca un Value/Map suelto sin contrato.
    INV-09   Todo AgentRun tiene límites explícitos.
             ContextSnapshot.estimatedTokens nunca excede execution.budget.maxInputTokens (C-012)
             — el primer componente del libro que valida en la práctica ese campo específico del
             ExecutionBudget compartido.
    INV-18   Toda acción significativa produce un evento observable.
             assembleContextSnapshot emite AgentEvent (CONTEXT_SNAPSHOT_ASSEMBLED /
             CONTEXT_SNAPSHOT_FAILED) en cada resolución.
    INV-19   Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy
             relevante.
             Cada AgentEvent que emite ContextEngine lleva el traceId de su ExecutionContext.
    INV-20   Todo error operacional pertenece a una categoría conocida.
             Cuando ningún candidato cabe, assembleContextSnapshot construye un HarnessError con
             category = CONTEXT — la primera vez que este valor de ErrorCategory (declarado desde
             CH-00) se ejercita en la práctica.

Component ownership changes
    CMP-004 ContextEngine se introduce — registry/components.yaml pasa de 3 a 4 componentes.
    owns/does_not_own citados literalmente contra Article III (sección "ContextEngine") y
    Article IV.

Lifecycle changes
    Ninguno sobre AgentRunStatus (C-013): sigue siendo propiedad exclusiva de AgentLoop (CH-01), y
    su tabla de transiciones no cambia aquí. ContextSnapshot tampoco introduce ningún lifecycle
    propio (ver seccion 12).

Security implications
    ContextEngine.does_not_own excluye explícitamente policy/autorización sobre qué información
    puede verse — una superficie de decisión distinta de "qué información es relevante" (P-14),
    que sí le pertenece a este componente. Ver seccion 15 para el análisis completo de este límite,
    el más sutil de los cuatro que este capítulo declara.

Observability implications
    ContextEngine es el cuarto componente que emite AgentEvent en la práctica, extendiendo
    AgentEventType con dos valores nuevos (CONTEXT_SNAPSHOT_ASSEMBLED,
    CONTEXT_SNAPSHOT_FAILED) sin modificar el envelope AgentEvent (C-010) ni su STRUCT.

Deterministic vs agentic boundary
    Article XII se refina una cuarta vez a nivel de componente: en este tramo el modelo no
    participa en absoluto — ContextEngine, determinístico, decide qué material del turno
    sobrevive dentro del presupuesto disponible antes de que el modelo llegue a ver nada.
```

## 5. Conceptos Nuevos (New Concepts)

- **Context Assembly**: el tramo determinístico que selecciona, rankea, compone y compacta el
  material candidato de un turno (`AgentMessage`, `AgentState`, `ExecutionContext`) hacia un
  resultado ya listo para volverse parte de un `ModelRequest` — responsabilidad exclusiva de
  `ContextEngine` (Article III, Article IV: "`ContextEngine` → What should the model know?").
- **Context Block**: el fragmento individual de contexto que `ContextEngine` decide incluir —
  modelado como `ContextBlock` (seccion 6), un `STRUCT` embebido dentro de `ContextSnapshot` sin
  contrato `C-XXX` propio — el mismo patrón que `RawToolCallProposal` (embebido en `ModelResponse`,
  CH-03) o `AgentEventType` (embebido en `AgentEvent`, CH-00).
- **Provenance**: de dónde vino un `ContextBlock` — Article III lo asigna literalmente a
  `ContextEngine` (`owns`: "provenance"). Sin este registro, nada en el sistema puede responder,
  después de que el modelo ya respondió, "¿por qué el modelo sabía esto?".
- **Context Budget**: el límite explícito contra el cual `ContextEngine` valida su selección — este
  capítulo reutiliza `ExecutionBudget.maxInputTokens` (C-012, CH-00) en vez de introducir un tipo de
  presupuesto nuevo; `ContextSnapshot.estimatedTokens` (seccion 6) es el campo simple, embebido, que
  registra cuánto de ese presupuesto consumió una selección concreta.
- **Compaction**: la transformación que reduce el tamaño de un candidato que no cabe completo, para
  que quepa dentro del presupuesto disponible — modelada en este capítulo mediante una primitiva
  (`compact(...)`, seccion 11), no mediante un componente `Compactor`/`Summarizer` propio (ver la
  nota editorial de la seccion 3): en esta Constitution, `ContextEngine` posee compaction él mismo.
- **Decision Ownership** *(Article IV, en uso desde CH-01, ahora aplicado a un cuarto componente)*:
  `ContextEngine` decide "¿qué debería saber el modelo?"; explícitamente NO decide "¿cómo se invoca
  el modelo seleccionado?" (`ModelGateway`, ya resuelto), "¿debe ocurrir otro turno?" (`AgentLoop`,
  ya resuelto), "¿qué historial de ejecución persiste?" (`SessionManager`, preview) ni "¿puede
  verse esta información en absoluto?" (`PolicyEngine`, preview) — esta última distinción, entre
  *seleccionar por relevancia* y *autorizar visibilidad*, es la más delicada que este libro ha
  tenido que trazar hasta ahora (ver seccion 15).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados de CH-00/CH-01/CH-02/CH-03

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `AgentId`, `RunId`, `SessionId`, `TraceId`,
`Timestamp`, `AgentMessage`, `AgentState`, `ExecutionContext`, `ExecutionBudget`, `AgentEvent`,
`HarnessError`.

### `AgentEventType` — extendido, sin redefinir `AgentEvent`

CH-03 extendió `AgentEventType` a ocho valores (`RUN_STARTED`, `TURN_CONTINUED`, `RUN_COMPLETED`,
`RUN_FAILED`, `TOOL_CALL_COMPLETED`, `TOOL_CALL_FAILED`, `MODEL_RESPONSE_RECEIVED`,
`MODEL_INVOCATION_FAILED`), sin contrato `C-XXX` propio. Este capítulo agrega dos valores — los
primeros eventos que observan el ensamblado de contexto, no la invocación de un modelo ni la
ejecución de una tool call:

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
END
```

`AgentEvent` (C-010) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — solo el rango de
valores permitido para `eventType` crece, igual que en CH-01, CH-02 y CH-03.

### `ContextBlock` — el fragmento embebido (sin `C-XXX` propio)

```pseudocode
STRUCT ContextBlock
    provenance: Text
    content: Value
    compacted: Boolean
END
```

`provenance` registra de dónde vino este fragmento (p. ej. `"conversation_history"`) — la cita
literal de Article III que motiva su existencia. `compacted` distingue un bloque cuyo `content` es
el original sin tocar (`FALSE`) de uno cuyo `content` ya es una versión resumida para caber dentro
del presupuesto (`TRUE`). Vive embebido dentro de `ContextSnapshot`, sin contrato `C-XXX` propio —
el mismo patrón que `RawToolCallProposal` (CH-03) o `AgentEventType` (CH-00): un tipo real, con
`STRUCT` propio, que ningún capítulo registra como contrato independiente.

### `ContextSnapshot` — el resultado ya seleccionado, priorizado y compactado

```pseudocode
STRUCT ContextSnapshot
    blocks: List<ContextBlock>
    budget: ExecutionBudget
    estimatedTokens: Integer
    producedAt: Timestamp
END
```

`blocks` es una lista **ordenada** — ese orden es, literalmente, el ranking que `ContextEngine` ya
resolvió: el primer bloque es el de mayor prioridad, no un orden arbitrario. `budget` reutiliza
`ExecutionBudget` (C-012, CH-00) sin modificarlo, para dejar explícito contra qué límite se validó
esta selección — no se introduce ningún tipo de presupuesto nuevo, siguiendo el mismo patrón que
`ModelRequest.budget` ya estableció en CH-03. `estimatedTokens` es el campo simple y embebido (sin
contrato `C-XXX` propio) que registra cuánto de `budget.maxInputTokens` consumió efectivamente esta
selección — `ExecutionBudget` no tiene ningún campo que exprese "cuánto se usó", solo límites
máximos, así que este capítulo no lo modifica: agrega el campo que le falta directamente a
`ContextSnapshot`, el mismo patrón que `RawToolCallProposal` embebido en `ModelResponse` (CH-03).

**Unchanged / Not yet introduced**: con `C-005` ya asignado en este capítulo, no queda ningún id
reservado del lote original que CH-01 §7 documentó (`C-005`..`C-009`) — los cinco ya están
asignados (`C-005` aquí, `C-006`/`C-007` en CH-03, `C-008`/`C-009` en CH-02). Tampoco se introduce
ningún `STRUCT ContextProvider`, `INTERFACE ContextEngine` formal con múltiples `IMPLEMENTATION`
(por fuente de contexto), ni ningún componente `Compactor`/`Summarizer` — ver la nota editorial de
la seccion 3: este libro no fragmenta esa responsabilidad. `ModelRequest` (C-006, CH-03) tampoco se
modifica: `ContextSnapshot.blocks` todavía no se cablea formalmente hacia `ModelRequest.messages`
(ver seccion 9/18).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía (formalizar
`ContextEngine` como interfaz con múltiples `IMPLEMENTATION` — por ejemplo, una por fuente de
contexto — queda para cuando este libro necesite modelar más de una fuente real de material, al
estilo del `ContextProvider` del outline general que este capítulo deliberadamente no adopta, ver
seccion 3). Introduce un contrato de datos, registrado en `registry/contracts.yaml`:

```text
ID:                     C-005
Name:                   ContextSnapshot
Version:                v1
Introduced In:          CH-04
Current Definition:     STRUCT ContextSnapshot (ver §6)
Used By:                [CMP-004]
Modified By:            []
Constitutional Impact:  [P-01, P-14, INV-09]
```

Con `C-005` ya asignado, no queda ningún id todavía reservado del lote original que CH-01 §7
documentó (`C-005`..`C-009`) — los cinco están asignados: `C-008`/`C-009` desde CH-02,
`C-006`/`C-007` desde CH-03, y `C-005` desde este mismo capítulo.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el cuarto componente de runtime del libro:

```pseudocode
COMPONENT ContextEngine
    consumes: AgentMessage, AgentState, ExecutionContext
    produces: ContextSnapshot, AgentEvent, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Article III (sección "ContextEngine"):

```text
COMPONENT: ContextEngine

Responsibility:
    Seleccionar, rankear, componer y compactar el material candidato de un turno (AgentMessage,
    AgentState, ExecutionContext) dentro de un presupuesto de contexto explícito, devolviendo un
    ContextSnapshot que registra la procedencia (provenance) de cada bloque incluido — sin invocar
    al modelo, sin decidir si otro turno debe ocurrir, sin persistir historial de sesión y sin
    autorizar qué información puede verse.

Consumes:
    C-001 AgentMessage, C-003 AgentState, C-004 ExecutionContext

Depends on:
    (ninguno todavía — SessionManager y PolicyEngine son Preview, no introducidos en este
    capítulo; ver seccion 9)

Produces:
    C-005 ContextSnapshot, C-010 AgentEvent (CONTEXT_SNAPSHOT_ASSEMBLED /
    CONTEXT_SNAPSHOT_FAILED), C-011 HarnessError (embebido en un fallo de ensamblado)

Owns (Article III, cita literal):
    - selección
    - ranking
    - composición
    - compaction
    - context budgets
    - provenance

Does NOT own (Article IV — declarado con el mismo peso que Owns):
    - invocar al modelo seleccionado (ModelGateway, CMP-003, ya introducido en CH-03 — Article IV:
      "ModelGateway → How should the selected model be invoked?")
    - decidir si otro turno de razonamiento debe ocurrir (AgentLoop, CMP-001, ya introducido en
      CH-01 — Article IV: "AgentLoop → Should another reasoning turn occur?")
    - persistir/recuperar historial de sesión y checkpoints (SessionManager, Article IV — no
      introducido en este capítulo, es un componente distinto: "SessionManager → What execution
      history and checkpoints persist?")
    - policy/autorización sobre qué información puede verse (PolicyEngine, Article IV — no
      introducido en este capítulo: "PolicyEngine → May this action occur?" — distinto de
      seleccionar por relevancia, que sí pertenece a ContextEngine; ver seccion 15)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con una
particularidad respecto a CH-01/CH-02/CH-03: dos de las cuatro exclusiones ya no son "preview,
todavía sin componente", sino fronteras contra componentes reales que ya existen (`AgentLoop`,
`ModelGateway`). `ContextEngine` es el segundo componente del libro, después de `ModelGateway`, que
debe declarar explícitamente que no invade el territorio de más de un componente ya construido.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
ContextEngine
    consumes → AgentMessage, AgentState, ExecutionContext
    produces → ContextSnapshot, AgentEvent, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`ContextEngine` no depende hoy de ningún otro componente registrado. En prosa (nunca dentro de un
bloque `pseudocode`, per `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las
dependencias futuras que capítulos posteriores agregarán son:

| Componente futuro (Preview — no introducido en este capítulo) | Qué le daría a `ContextEngine` |
|---|---|
| `SessionManager` | el historial de sesión real (persistido) del que hoy `candidates` recibe una lista ya dada, sin fuente propia |
| `PolicyEngine` | la autorización real sobre qué información puede verse — hoy asumida como ya resuelta antes de que `candidates` llegue a `ContextEngine` (ver seccion 15) |

`ModelGateway` (CMP-003, ya existente) sería, en la práctica, quien consuma el `ContextSnapshot` que
este capítulo sí sabe producir, para poblar `ModelRequest.messages` (C-006, CH-03) — pero esa
relación es la inversa de una `dependency` en el sentido de `registry/components.yaml`
(`ModelGateway` dependería de `ContextEngine`, no al revés), y ese cableado formal (agregar
`CMP-004` a `ModelGateway.dependencies`, extender `ModelRequest`/su construcción para que consuma
`ContextSnapshot.blocks` en vez de recibir `List<AgentMessage>` ya dado) es, explícitamente, trabajo
de un capítulo posterior — el mismo patrón que CH-02 y CH-03 ya establecieron para las relaciones
inversas anteriores. `book/chapters/03-model-gateway/chapter.md` no se modifica para reflejarlo
todavía (fuera de su campo `next_chapter`, ya actualizado por este capítulo), y `registry/
contracts.yaml` no incluye `C-006` en `modifies_contracts` de este capítulo: `ModelRequest` no
cambia aquí.

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[AgentLoop — turno en curso, conceptual, sin cablear formalmente en este capítulo] → ContextEngine
→ [AgentLoop retoma con un ContextSnapshot ya seleccionado]
```

**Vista 2 — Sequence**

```text
AgentLoop (conceptual)
   │ recopila candidates: List<AgentMessage> ya existentes para este turno (AgentState, historial)
   ▼
ContextEngine
   │ assembleContextSnapshot(candidates, execution, agentId)
   │ recorre candidates en su orden ya dado (ese orden ES el ranking)
   │ por cada candidato:
   │     ¿cabe completo dentro de budget.maxInputTokens?  → inclúyelo tal cual (compacted = FALSE)
   │     ¿no cabe completo? → compáctalo → ¿cabe compactado? → inclúyelo (compacted = TRUE)
   │     ¿ni compactado cabe? → queda fuera — selección explícita, no descarte silencioso
   │ si ningún candidato cupo, ni siquiera compactado, y sí había candidatos → HarnessError
   │ construye ContextSnapshot (blocks, budget, estimatedTokens, producedAt)
   │ emite: AgentEvent (CONTEXT_SNAPSHOT_ASSEMBLED | CONTEXT_SNAPSHOT_FAILED)
   ▼
ContextSnapshot
   │
   ▼
[AgentLoop retoma el ciclo con este ContextSnapshot — Preview, el cableado formal hacia
ModelRequest.messages (ModelGateway, CH-03) es trabajo de un capítulo posterior, ver seccion 18/19]
```

**Vista 3 — Pseudocódigo**

Ver §11: `assembleContextSnapshot` es la primera formalización ejecutable de "`ContextEngine`
decide qué debería saber el modelo", construida exclusivamente a partir de material que ya existe
(`AgentMessage` desde CH-00, `AgentState` desde CH-00, `ExecutionContext` desde CH-00) — sin
necesitar que `ModelGateway` ni `ModelRequest` cambien.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde
CH-00/CH-01/CH-02/CH-03.

```pseudocode
FUNCTION assembleContextSnapshot(
    candidates: List<AgentMessage>,
    execution: ExecutionContext,
    agentId: AgentId
) -> ContextSnapshot

    blocks: List<ContextBlock> = []
    usedTokens: Integer = 0

    FOR EACH candidate IN candidates
        fullTokens: Integer = estimateTokens(candidate.content)

        IF usedTokens + fullTokens <= execution.budget.maxInputTokens
            blocks.append(ContextBlock(
                provenance = "conversation_history",
                content = candidate.content,
                compacted = FALSE
            ))
            usedTokens = usedTokens + fullTokens
        ELSE
            compactedContent: Value = compact(candidate.content)
            compactedTokens: Integer = estimateTokens(compactedContent)

            IF usedTokens + compactedTokens <= execution.budget.maxInputTokens
                blocks.append(ContextBlock(
                    provenance = "conversation_history",
                    content = compactedContent,
                    compacted = TRUE
                ))
                usedTokens = usedTokens + compactedTokens
            END
            // si ni siquiera la versión compactada cabe, el candidato queda fuera de este
            // ContextSnapshot: selección explícita bajo presupuesto, nunca un descarte silencioso.
        END
    END

    IF candidates.length > 0 AND blocks.length == 0
        failure: HarnessError = HarnessError(
            category = CONTEXT,
            code = "CONTEXT_BUDGET_EXHAUSTED",
            message = "Ningún candidato, ni siquiera compactado, cupo dentro del presupuesto de contexto disponible",
            recoverable = TRUE,
            retryable = FALSE,
            metadata = {}
        )

        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = CONTEXT_SNAPSHOT_FAILED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = failure
        )

        THROW failure
    END

    snapshot: ContextSnapshot = ContextSnapshot(
        blocks = blocks,
        budget = execution.budget,
        estimatedTokens = usedTokens,
        producedAt = now()
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = CONTEXT_SNAPSHOT_ASSEMBLED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = snapshot
    )

    RETURN snapshot
END
```

`newEventId()` y `now()` son las mismas primitivas de CH-00/CH-01/CH-02/CH-03 (no son entidades
arquitectónicas ni componentes). `estimateTokens(...)` y `compact(...)` son primitivas nuevas de
este capítulo, en el mismo espíritu: funciones deterministas ya asumidas, como `beforeToolCall`/
`afterToolCall` desde CH-02 — no son entidades arquitectónicas, no requieren ficha ni registro, y
este capítulo no modela su implementación interna (cómo se cuenta un token concreto, o cómo se
resume un contenido concreto); son primitivas de infraestructura que cualquier implementación real
de `ContextEngine` debe proveer.

`candidates` es el único material de entrada, y es, deliberadamente, material que ya existe desde
CH-00 (`AgentMessage`) — a diferencia de `capabilityResolved` en CH-02 o `providerFinished` en
CH-03, que eran señales asumidas de componentes todavía sin construir, `candidates` no es una señal
asumida de un componente futuro: es historia real de la sesión, ya disponible. Lo que
`assembleContextSnapshot` sí posee, y ejecuta en la práctica, es la selección/ranking/composición/
compaction misma — a diferencia de `ModelGateway.invoke` (CH-03), que recibía la respuesta del
proveedor ya resuelta como dada, este componente no delega su responsabilidad central a ninguna
señal externa.

Nótese lo que `assembleContextSnapshot` **no** hace: no invoca ningún `ModelGateway.invoke(...)`
real (Article IV, "`ModelGateway` → How should the selected model be invoked?" sigue sin respuesta
aquí), no decide ningún `AgentRunStatus` (Article IV, "`AgentLoop` → Should another reasoning turn
occur?" tampoco), no persiste ni recupera ningún historial de sesión (`SessionManager`, preview —
`candidates` llega ya dado, no se busca ni se guarda aquí), y no filtra ningún candidato por razones
de autorización o visibilidad (`PolicyEngine`, preview — ver seccion 15): asume que todo lo que
llega en `candidates` ya es visible para este agente, y decide únicamente cuál de ese material ya
autorizado es relevante y cabe dentro del presupuesto.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013): esa máquina de estados sigue
siendo propiedad exclusiva de `AgentLoop` (CH-01 §12), y su tabla de transiciones no cambia aquí.

`assembleContextSnapshot` (§11) sí atraviesa un camino implícito con dos desenlaces — pero
deliberadamente **no** se formaliza como un nuevo contrato de lifecycle en este capítulo (eso
introduciría una segunda entidad nueva, fuera del alcance decidido para este capítulo):

```text
candidates recibidos
   → ningún bloque cupo, ni siquiera compactado   → HarnessError (category = CONTEXT,
                                                      code = CONTEXT_BUDGET_EXHAUSTED)
   → al menos un bloque cupo (completo o compactado) → ContextSnapshot (blocks = [...],
                                                          estimatedTokens = usedTokens)
```

**Lo que este capítulo explícitamente no cierra**: la tabla de transiciones de `AgentRunStatus`
(CH-01 §12) no anota ninguna transición nueva relacionada con el ensamblado de contexto — a
diferencia de `WAITING_FOR_MODEL`/`WAITING_FOR_TOOL` (que sí corresponden a handoffs explícitos
hacia `ModelGateway`/`ToolRuntime`), ensamblar un `ContextSnapshot` ocurre, conceptualmente, *antes*
de que `AgentLoop` decida invocar al modelo — no es, en sí mismo, un estado nuevo del lifecycle.
Conectar formalmente ambos capítulos (que `AgentLoop` invoque `assembleContextSnapshot` antes de
`invokeModelForTurn`, CH-03 §11) sigue siendo trabajo de un capítulo posterior (ver seccion 18/19).

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6) clasifica también los fallos que introduce este capítulo,
fiel a los `Failure Examples` de `constitution/ARCHITECTURE_CONSTITUTION.md` Article VII:

```text
CONTEXT
    CONTEXT_BUDGET_EXHAUSTED   — ningún candidato, ni siquiera compactado, cupo dentro del
                                  presupuesto de contexto disponible
        → recoverable: TRUE, retryable: FALSE
```

Este es el primer fallo real del libro clasificado bajo `category = CONTEXT` — un valor de
`ErrorCategory` declarado desde CH-00 §6 que ningún componente había ejercitado hasta este
capítulo. `recoverable = TRUE` porque el problema es corregible (ampliar el presupuesto, reducir o
resumir mejor los candidatos aguas arriba) — pero `retryable = FALSE`: reintentar exactamente la
misma llamada con los mismos `candidates` y el mismo `budget` fallaría de forma idéntica, el mismo
principio que ya aplicó `TOOL_INPUT_SCHEMA_MISMATCH` en CH-02.

`assembleContextSnapshot` nunca devuelve una excepción cruda ni un `ContextSnapshot` a medias
cuando ningún candidato cupo: siempre construye un `HarnessError` con `category`, `recoverable` y
`retryable` explícitos — mismo patrón que `runTurn` (CH-01 §11), `executeToolCall` (CH-02 §11) e
`invoke` (CH-03 §11).

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo de `category = POLICY`
(el agente no está autorizado a ver cierto candidato) sigue sin ser responsabilidad de
`ContextEngine` — su propio `does_not_own` (seccion 8) excluye explícitamente esa decisión; este
capítulo asume que `candidates` ya llegó filtrado por visibilidad antes de alcanzar
`assembleContextSnapshot` (ver seccion 15).

## 14. Eventos Producidos (Events Produced)

Este capítulo agrega dos valores a `AgentEventType` (seccion 6) — los primeros que observan el
ensamblado de contexto, no la invocación de un modelo ni la ejecución de una tool call:

```text
CONTEXT_SNAPSHOT_ASSEMBLED   — ContextEngine seleccionó, rankeó, compuso y compactó el material
                                candidato con éxito (assembleContextSnapshot, §11)
CONTEXT_SNAPSHOT_FAILED      — ContextEngine no pudo ensamblar ningún ContextSnapshot con el
                                material y presupuesto recibidos (assembleContextSnapshot, §11)
```

`RUN_STARTED`, `TURN_CONTINUED`, `RUN_COMPLETED`, `RUN_FAILED` (CH-00/CH-01),
`TOOL_CALL_COMPLETED`/`TOOL_CALL_FAILED` (CH-02) y `MODEL_RESPONSE_RECEIVED`/
`MODEL_INVOCATION_FAILED` (CH-03) no se emiten desde `assembleContextSnapshot`: pertenecen al ciclo
cognitivo, a la ejecución de una tool call o a la invocación del modelo — no al ensamblado de
contexto. Un capítulo posterior que conecte los cuatro extremos (ver seccion 18/19) podrá
correlacionar un `CONTEXT_SNAPSHOT_ASSEMBLED` con el siguiente `MODEL_RESPONSE_RECEIVED` sin
redefinir el envelope común `AgentEvent` (C-010).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

Esta es la frontera más sutil que este libro ha tenido que trazar hasta ahora, y merece un análisis
propio.

**El riesgo de confusión.** `ContextEngine` decide qué información es *relevante* para el modelo
(P-14: "el harness debe seleccionar información relevante dentro de presupuestos explícitos"). Es
tentador pensar que, como de todos modos `ContextEngine` ya está "mirando" cada candidato para
decidir si es relevante, también podría decidir si ese candidato *puede verse en absoluto* — por
ejemplo, si contiene datos de otro usuario, un secreto, o información que la política de la
organización restringe para este agente en particular. **Estas son dos preguntas distintas**, con
dueños distintos según Article IV:

- "¿Es esto relevante para razonar sobre el turno actual?" → `ContextEngine` (P-14, este capítulo).
- "¿Puede este agente ver esto en absoluto, independientemente de si es relevante?" → `PolicyEngine`
  (Article IV: "May this action occur?" — preview, no introducido en este capítulo).

Un candidato puede ser perfectamente relevante y, al mismo tiempo, estar prohibido: el mensaje más
relevante para responder una pregunta podría ser, precisamente, el que el agente no está autorizado
a citar. Si `ContextEngine` fusionara ambas preguntas, la autorización dejaría de ser una capa
determinística explícita (P-05, "side effects pass through policy" — aplicado aquí, por extensión,
a la visibilidad de información antes de que produzca ningún side effect) y pasaría a depender de
que la lógica de relevancia "también" filtre correctamente lo prohibido — exactamente el patrón que
Article IV existe para prevenir: una decisión absorbida silenciosamente por un dominio vecino
porque "ya estaba mirando el mismo dato".

**La solución de este capítulo.** `assembleContextSnapshot` (§11) recibe `candidates` como una
`List<AgentMessage>` que **asume ya autorizada** — el mismo patrón de "señal externa asumida" que
`capabilityResolved` en CH-02 o `providerFinished` en CH-03, salvo que aquí la señal no es un
booleano explícito, sino una precondición documentada sobre el parámetro de entrada: filtrar
`candidates` por autorización, antes de que lleguen a `ContextEngine`, es trabajo de un componente
que este libro todavía no introduce (`PolicyEngine`). `ContextEngine.does_not_own` (seccion 8) lo
declara explícitamente. Esto es deuda intencional, no una brecha de seguridad silenciada: se
documenta aquí, se repite en la seccion 18, y ningún test de la seccion 16 afirma que
`assembleContextSnapshot` filtra por visibilidad — todo lo contrario, uno de ellos afirma que nunca
lo intenta.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST AssembleContextSnapshotNeverExceedsExecutionBudgetMaxInputTokens
TEST AssembleContextSnapshotAlwaysRecordsProvenanceOnEveryContextBlock
TEST AssembleContextSnapshotPreservesCandidateOrderAsRankingOrder
TEST AssembleContextSnapshotNeverInvokesModelGatewayOrAgentLoopDirectly
TEST AssembleContextSnapshotNeverFiltersCandidatesByAuthorizationItself
TEST AssembleContextSnapshotAlwaysEmitsAnAgentEventOnSuccessOrFailure
TEST ContextBudgetExhaustedIsRecoverableButNotRetryable
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.1, después de CH-04)

Constitution
 ├── Article I    — Principles (P-01 .. P-15)
 ├── Article II   — Invariants (INV-01 .. INV-20)
 ├── Article III  — Component Sovereignty (AgentLoop, ToolRuntime, ModelGateway, ContextEngine:
 │                  cuatro componentes instanciados)
 ├── Article IV   — Decision Ownership (en uso: los cuatro componentes declaran owns/does_not_own)
 └── Article VII  — Failure Constitution (ErrorCategory.CONTEXT ejercitado por primera vez)

Contracts (registry/contracts.yaml)
 ├── C-001 AgentMessage        (CH-00 — consumido ahora también por CMP-004)
 ├── C-002 AgentConfig         (CH-00)
 ├── C-003 AgentState          (CH-00 — consumido por un segundo componente, CMP-004)
 ├── C-004 ExecutionContext    (CH-00)
 ├── C-005 ContextSnapshot     (CH-04, nuevo — formaliza el último id reservado desde CH-01)
 ├── C-006 ModelRequest        (CH-03)
 ├── C-007 ModelResponse       (CH-03)
 ├── C-008 ToolCall            (CH-02)
 ├── C-009 ToolResult          (CH-02)
 ├── C-010 AgentEvent          (CH-00)
 ├── C-011 HarnessError        (CH-00)
 ├── C-012 ExecutionBudget     (CH-00)
 └── C-013 AgentRunStatus      (CH-01)

Components (registry/components.yaml)
 ├── CMP-001 AgentLoop         (CH-01)
 ├── CMP-002 ToolRuntime       (CH-02)
 ├── CMP-003 ModelGateway      (CH-03)
 └── CMP-004 ContextEngine     (CH-04, nuevo — cuarto componente del libro)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado formal `ContextEngine ↔ ModelGateway`**: `ContextSnapshot.blocks` no se conecta
  todavía con `ModelRequest.messages` (C-006, CH-03) — `ModelRequest` no se modifica en este
  capítulo (`modifies_contracts: []`), y `ModelGateway.dependencies` no agrega `CMP-004`. Ese
  cableado, y la decisión de cómo un `ContextBlock.content` (potencialmente compactado) se
  convierte de vuelta en un `AgentMessage` real, es trabajo de un capítulo posterior.
- **Ranking real más allá de recencia + ajuste greedy al presupuesto**: `assembleContextSnapshot`
  preserva el orden de `candidates` como ranking y decide inclusión/compaction en ese orden — no
  modela ningún mecanismo de relevancia semántica, retrieval, memoria de trabajo, ni las fuentes
  adicionales que el outline general menciona (proyecto, skills, documentación). Esto sigue siendo,
  literalmente, trabajo de `ContextEngine` — no de un componente nuevo (ver la nota editorial de la
  seccion 3) — pero un algoritmo de ranking más rico que la recencia queda fuera de este capítulo.
- **`SessionManager`**: `candidates` llega ya dado a `assembleContextSnapshot` — de dónde viene
  realmente ese historial (persistencia, reconstrucción de una sesión durable) sigue sin componente
  propio.
- **`PolicyEngine` y la autorización de visibilidad**: como se documentó en la seccion 15,
  `ContextEngine` asume que `candidates` ya está autorizado; nada en este capítulo lo verifica.
- **Provider Adapters reales, streaming real, resolución de `proposedToolCall`,
  `CapabilityRegistry`**: deuda intencional heredada de CH-02/CH-03, sin cambios en este capítulo.
- **Ningún `Compactor`/`Summarizer`/`ContextProvider` como componente propio**: reafirmación
  explícita, no una omisión — esta Constitution asigna ese territorio íntegro a `ContextEngine`
  (Article III), y ningún capítulo futuro de este libro debería introducir esos nombres como
  componentes nuevos.
- **Persistencia real de `AgentState`/`SessionState`, human-in-the-loop implementado, reviewers
  plurales, evals y orquestación multi-agente**: sin cambios respecto a CH-00/CH-01/CH-02/CH-03 —
  explícitamente fuera de alcance de BH-v0.1.

## 19. Siguiente Incremento (Next Increment)

El problema natural del próximo capítulo: ahora que `ContextEngine` puede producir un
`ContextSnapshot` real (§11), pero asumiendo que todo lo que recibe ya está autorizado para verse
(§15), ¿quién decide realmente si un candidato de contexto — o una `proposedToolCall` cruda desde
CH-03 — está permitido, antes de que cualquiera de los dos llegue a su destino? Eso apunta hacia
`PolicyEngine` (Article IV: "May this action occur?") como el quinto componente candidato de
Article III que dejaría de ser preview: el mismo componente resolvería, de una sola vez, dos deudas
intencionales que ya lleva el libro — la autorización de `proposedToolCall` (CH-03 §18) y la
autorización de visibilidad sobre `candidates` (este capítulo, §15) — y probablemente sería también
el momento de cablear `ContextSnapshot.blocks` hacia `ModelRequest.messages`, cerrando el ciclo
completo `ContextEngine → ModelGateway → AgentLoop → ToolRuntime` de punta a punta.

Ese capítulo (`CH-05`, fuera del alcance de esta ejecución) heredaría directamente la deuda
intencional de §18. `next_chapter` queda en `null` en el frontmatter de este capítulo porque, en
este momento del libro, `CH-05` todavía no existe como archivo — solo como el problema que
motivará su escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de
> la secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco
> Iceberg / Bucles de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas,
> Forrester/Meadows), secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): sin un dueño explícito para "¿qué debería saber el
   modelo?", el material candidato de un turno tiende a resolverse por default hacia "incluir todo
   lo que haya" — no porque alguien lo decida, sino porque nadie decide activamente lo contrario.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): sin un componente
   con fronteras explícitas, la selección de contexto se confunde fácilmente con la autorización
   sobre qué puede verse — dos decisiones de dominios distintos que, sin separarse, tienden a
   resolverse juntas "porque total, ya estamos mirando el mismo dato".
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `ContextEngine` (CMP-004) con una ficha que declara tanto lo que posee (`owns`: selección,
   ranking, composición, compaction, context budgets, provenance) como lo que explícitamente NO
   posee (`does_not_own`, con la exclusión de autorización de visibilidad como la más sutil de
   todas) y formaliza `ContextSnapshot` (C-005), el último id que seguía reservado desde CH-01.
4. **Modelos mentales** (= §4, Constitutional Impact): P-01 ("Context is a first-class
   architectural component") junto con P-14 ("Context should be selected, not dumped") — más
   contexto no implica mejor razonamiento; el harness, no la casualidad, decide qué entra.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un componente nuevo se introduce sin declarar
  explícitamente su `does_not_own`, aumenta la probabilidad de que absorba silenciosamente la
  próxima decisión vecina "porque ya estaba ahí" — el mismo bucle que CH-01/CH-02/CH-03 ya
  cortaron. Este capítulo lo repite para `ContextEngine`, con la exclusión de autorización de
  visibilidad como el caso más fácil de confundir hasta ahora.
- **Bucle de equilibrio (estabiliza):** `assembleContextSnapshot` (§11) nunca copia el material
  candidato completo hacia el resultado — decide, para cada candidato, si cabe completo, si debe
  compactarse, o si queda explícitamente fuera, en vez de dejar que el contexto crezca sin límite.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `ContextSnapshot` registre, por cada bloque
incluido, tanto su `provenance` como si tuvo que `compacted`-se — en vez de que `ContextEngine`
devolviera simplemente contenido ya listo para el modelo sin ningún rastro de cómo se construyó. Si
esa procedencia se pierde aquí, en el único lugar del sistema donde se decide qué entra, ningún
capítulo futuro podría reconstruirla después.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado
> completo de esta sección (con ids estables para cada pregunta/tarjeta) vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida. Aquí se
> presenta en prosa, para lectura directa del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Ya que el contrato que empaqueta los mensajes de un turno hacia el modelo explícitamente no
   decide cuáles incluir ni cómo priorizarlos, ¿quién selecciona, dentro de un turno, qué
   información realmente ve el modelo, y contra qué límite explícito valida esa selección?
   *(cierra la pregunta guía 1)*
2. Si el material candidato para un turno excede el presupuesto disponible, ¿qué debería pasar con
   la información que no cabe completa: descartarse en silencio, resumirse para que quepa, o
   quedar fuera con un registro explícito de que quedó fuera? *(cierra la pregunta guía 2)*
3. Para cada fragmento de información que termina formando parte de lo que el modelo ve, ¿por qué
   necesitamos poder responder de dónde vino, y qué se pierde en auditoría si esa procedencia nunca
   se registra? *(cierra la pregunta guía 3)*
4. ¿Por qué el mismo componente que decide qué información es relevante para el modelo no debería
   decidir, además, si el agente está siquiera autorizado a ver esa información en primer lugar?
   *(cierra la pregunta guía 4)*

### Explicar

1. `ContextEngine` posee decidir qué información es relevante para el modelo dentro de un
   presupuesto explícito. Explica, como si hablaras con alguien sin contexto técnico, por qué NO
   posee decidir si el agente está autorizado a ver esa información en primer lugar — ¿qué se
   rompería, en concreto, si `ContextEngine` empezara a decidir también autorización "ya que de
   todos modos es quien procesa la información primero"?
2. `ContextSnapshot.blocks` conserva el orden de los candidatos como su ranking, y cada
   `ContextBlock` incluido registra su `provenance` y si tuvo que compactarse. Explica por qué esta
   forma normalizada es preferible a que un componente futuro reciba directamente una lista cruda
   de `AgentMessage` sin ese registro — ¿qué perderíamos, en términos de auditoría, si un
   `ContextSnapshot` no dijera de dónde vino cada fragmento ni si fue resumido?

### Conectar

1. Cuando `ContextEngine` produce un `ContextSnapshot` con sus `blocks` ya seleccionados,
   priorizados y compactados, ¿qué campo de `ModelRequest` (`ModelGateway`, CH-03) tendría que
   poblar quien conecte ambos capítulos con el contenido de esos bloques, y qué campo de
   `ExecutionBudget` seguiría reutilizándose sin cambios en ese cableado futuro?

### Espaciar

Las tres tarjetas de repaso de este capítulo (dos sobre `ContextEngine` — su `owns` y su
`does_not_own` — y una sobre `ContextSnapshot`) entran hoy en `reviewStage = DAY_1`. Repásalas de
nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) — ver el apéndice de tarjetas al final
del libro (edición PDF) o `retrieval_set.flashcards` en `dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te equivocaste,
ese es precisamente el punto ciego que este método existe para revelar.
