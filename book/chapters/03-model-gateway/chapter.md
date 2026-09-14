---
id: CH-03
title: "ModelGateway y la Invocación Real del Modelo"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-003]
introduces_contracts: [C-006, C-007]
modifies_contracts: []
constitutional_articles: [P-01, P-02, P-10, P-12, P-13, INV-01, INV-02, INV-03, INV-18, INV-19, INV-20]
previous_chapter: CH-02
next_chapter: CH-04
retrieval_set:
  expected_outcome:
    id: EO-CH03
    text: |
      Al terminar este capítulo podrás distinguir, dentro de la invocación real de un modelo de
      lenguaje, qué tramo le pertenece en exclusiva al componente que adapta mensajes e invoca al
      proveedor y qué tramos pertenecen a dominios distintos (continuación cognitiva, ejecución de
      una tool call, selección de contexto) que ya tienen o todavía no tienen componente propio —
      y podrás diseñar, para cualquier respuesta cruda de un proveedor, una representación
      normalizada que distinga texto final de una propuesta de acción sin resolver esa propuesta
      prematuramente.
  skeleton:
    id: SK-CH03
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
    components_to_be_introduced: [CMP-003]
    contracts_to_be_introduced: [C-006, C-007]
  guiding_questions:
    - id: GQ-CH03-01
      text: |
        Ya que AgentLoop decide si debe ocurrir otro turno pero nunca invoca directamente ningún
        modelo (ver capítulo anterior sobre AgentLoop), y que el modelo real puede pertenecer a
        proveedores completamente distintos entre sí, ¿quién adapta los mensajes de un turno hacia
        el formato que cada proveedor espera, y quién invoca realmente al modelo elegido?
      answered_by: RQ-CH03-01
    - id: GQ-CH03-02
      text: |
        Cuando la respuesta cruda de un proveedor de modelos llega con una forma distinta a la de
        cualquier otro proveedor, ¿cómo evitamos que el resto del ciclo cognitivo tenga que
        entender la forma particular de cada proveedor para saber si el modelo terminó de razonar o
        si propuso usar una herramienta?
      answered_by: RQ-CH03-02
    - id: GQ-CH03-03
      text: |
        Si el modelo propone usar una herramienta, ¿qué tan resuelta debe estar esa propuesta en el
        momento en que sale del componente que acaba de invocar al modelo, y quién es responsable
        de validar más adelante que esa propuesta realmente corresponde a una capacidad existente
        con argumentos válidos?
      answered_by: RQ-CH03-03
    - id: GQ-CH03-04
      text: |
        ¿Por qué el mismo componente que sabe cómo hablarle a un proveedor de modelos concreto no
        debería, además, decidir si el ciclo cognitivo completo debe continuar con otro turno?
      answered_by: RQ-CH03-04
  systems_lens:
    iceberg_visible_fact: |
      Sin un dueño explícito para "¿cómo se invoca realmente al modelo elegido?", cada
      implementación termina acoplando el ciclo cognitivo completo al SDK particular de un
      proveedor: el formato de mensajes de ese proveedor se filtra hacia arriba, su forma
      particular de anunciar "terminé" o "quiero usar una herramienta" se filtra hacia arriba, y
      cambiar de proveedor exige reescribir el ciclo cognitivo entero, no solo un adapter (ver
      seccion 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que, sin un componente con fronteras explícitas, la invocación del
      modelo tiende a absorber silenciosamente decisiones vecinas (¿debe ocurrir otro turno?, ¿está
      permitida la acción que el modelo propuso?) solo porque físicamente es el único lugar del
      código que "ya tiene la respuesta del modelo a la mano" — exactamente lo que Article IV
      prohíbe. Y sin una representación normalizada de esa respuesta, cada proveedor nuevo obliga a
      reinterpretar, en todo el sistema, qué significa "el modelo terminó" o "el modelo propuso una
      acción" (ver seccion 3, Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala el tercer componente real del libro, `ModelGateway` (CMP-003), con una
      ficha que declara tanto lo que posee (`owns`: selección de provider, adaptación de mensajes,
      invocación del modelo, streaming, normalización de respuestas) como lo que explícitamente NO
      posee (`does_not_own`: continuación cognitiva, ejecución de tool calls, selección de
      contexto, autorización) — y formaliza `ModelRequest` (C-006) y `ModelResponse` (C-007), los
      dos últimos ids que seguían reservados desde CH-00 (ver seccion 8, Component
      Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior sigue siendo el Ownership Rule de Article IV,
      ahora aplicado a un tercer componente, junto con P-02 ("The model is replaceable"): el
      runtime nunca debe depender estructuralmente de un proveedor específico. `ModelGateway` existe
      precisamente para que "¿cómo debe invocarse el modelo seleccionado?" tenga un dueño — sin que
      ese dueño se convierta, además, en el dueño de "¿debe ocurrir otro turno?" (`AgentLoop`, ya
      resuelto desde CH-01) (ver seccion 4, Impacto Constitucional).
    reinforcing_loop: |
      Cada vez que un componente nuevo se introduce sin declarar explícitamente su `does_not_own`,
      aumenta la probabilidad de que absorba silenciosamente la próxima decisión vecina "porque ya
      estaba ahí" — el mismo bucle que CH-01 y CH-02 ya cortaron para `AgentLoop` y `ToolRuntime`.
      Este capítulo repite el mismo corte para `ModelGateway`, con la particularidad de que ahora
      hay dos componentes reales ya existentes (no solo preview) cuyas fronteras `ModelGateway`
      podría invadir por accidente.
    balancing_loop: |
      `invoke` (seccion 11) es el mecanismo de equilibrio: normaliza la respuesta cruda del
      proveedor hacia un `ModelResponse` cuyo campo `proposedToolCall`, cuando existe, es
      deliberadamente una propuesta sin validar — nunca un `ToolCall` (C-008) real — en vez de
      dejar que `ModelGateway` decida por su cuenta que una capacidad existe o que sus argumentos
      son válidos.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `ModelResponse` (producido por
      `ModelGateway`, CMP-003) represente una propuesta de tool call cruda y sin validar
      (`proposedToolCall`), en vez de que `ModelGateway` resuelva esa propuesta hacia un `ToolCall`
      completo él mismo. Si `ModelGateway` cruzara esa línea, estaría invadiendo la responsabilidad
      de resolución/validación que Article III asigna a `ToolRuntime` (CH-02) y a
      `CapabilityRegistry` (preview) — el próximo capítulo que cablee los tres componentes de punta
      a punta heredaría una frontera ya confundida en vez de una frontera clara.
  recall_questions:
    - id: RQ-CH03-01
      text: |
        ¿Qué componente adapta los `AgentMessage` de un turno (más los límites de generación
        relevantes) hacia una forma que el modelo puede consumir, y qué contrato representa esa
        forma empaquetada?
    - id: RQ-CH03-02
      text: |
        ¿Qué contrato normaliza la respuesta cruda de un proveedor hacia algo que `AgentLoop` puede
        eventualmente consumir, y qué dos formas puede tomar esa normalización?
    - id: RQ-CH03-03
      text: |
        ¿Qué campo de `ModelResponse` representa que el modelo propuso usar una herramienta, qué
        dos subcampos sin validar transporta, y qué decidimos deliberadamente NO hacer con ese
        campo en este capítulo?
    - id: RQ-CH03-04
      text: |
        Según Article IV, ¿qué decisión posee `ModelGateway` y qué decisión relacionada, ya
        resuelta por `AgentLoop` desde CH-01, NO posee?
  explain_prompts:
    - id: EP-CH03-01
      text: |
        `ModelGateway` posee adaptar mensajes e invocar al modelo. Explica, como si hablaras con
        alguien sin contexto técnico, por qué NO posee decidir si debe ocurrir otro turno de
        razonamiento, aunque sea el único componente que realmente "habla" con el modelo — ¿qué se
        rompería, en concreto, si `ModelGateway` empezara a decidir eso directamente "ya que de
        todos modos es quien recibe la respuesta primero"?
      target_entity: CMP-003
    - id: EP-CH03-02
      text: |
        `ModelResponse.proposedToolCall` es una propuesta cruda, sin validar. Explica por qué
        `ModelGateway` no construye directamente un `ToolCall` (C-008, ya existente desde CH-02) a
        partir de esa propuesta — ¿qué principio de Article IV estaría violando si lo hiciera, y
        qué perderíamos si cada componente que "toca primero" un dato decidiera también resolverlo
        por su cuenta?
      target_entity: C-007
  interleaved_questions:
    - id: IQ-CH03-01
      text: |
        Cuando `ModelResponse.finished` es `TRUE` o `ModelResponse.proposedToolCall` no es nulo,
        ¿qué dos señales booleanas de `runTurn` (`AgentLoop`, CH-01) tendría que poblar quien
        conecte ambos capítulos, y qué dos campos de `proposedToolCall` necesitaría además quien
        construya el `ToolCall` (`ToolRuntime`, CH-02) correspondiente?
      current_chapter_entities: [CMP-003, C-007]
      prior_chapter_entities: [CMP-001, C-013, CMP-002, C-008]
      prior_chapter: CH-01
  flashcards:
    - id: FC-CH03-01
      front: |
        ¿Qué posee `ModelGateway` (Article III / Article IV), en una frase?
      back: |
        Selección de provider, adaptación de mensajes, invocación del modelo, streaming y
        normalización de respuestas — cita literal de Article III, sección "ModelGateway".
      source_entity: CMP-003
      chapter_introduced_in: CH-03
      review_stage: DAY_1
    - id: FC-CH03-02
      front: |
        ¿Qué NO posee `ModelGateway`, y a qué componentes pertenecen esas decisiones?
      back: |
        Decidir si otro turno debe ocurrir (`AgentLoop`, ya existente), ejecutar tool calls
        (`ToolRuntime`, ya existente), seleccionar/componer contexto (`ContextEngine`, preview) y
        policy/autorización (`PolicyEngine`, preview).
      source_entity: CMP-003
      chapter_introduced_in: CH-03
      review_stage: DAY_1
    - id: FC-CH03-03
      front: |
        ¿Qué campos tiene `ModelRequest` (C-006), y qué representan?
      back: |
        `messages` (List<AgentMessage>, los mensajes ya existentes del turno), `budget`
        (ExecutionBudget, los límites de generación relevantes) y `requestedAt` (Timestamp) — la
        forma empaquetada e independiente de proveedor que `ModelGateway` adapta hacia el provider.
      source_entity: C-006
      chapter_introduced_in: CH-03
      review_stage: DAY_1
    - id: FC-CH03-04
      front: |
        ¿Qué campos tiene `ModelResponse` (C-007), y por qué `proposedToolCall` es deliberadamente
        una propuesta cruda?
      back: |
        `finished` (Boolean), `content` (Optional<Value>), `proposedToolCall`
        (Optional<RawToolCallProposal>, solo `capabilityName` + `rawArguments`, sin validar) y
        `producedAt` (Timestamp). Es cruda porque resolverla hacia un `ToolCall` (C-008) real
        pertenece a `ToolRuntime`/`CapabilityRegistry`, no a `ModelGateway` — resolverla aquí
        invadiría esa frontera (Article IV).
      source_entity: C-007
      chapter_introduced_in: CH-03
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH03-01
      recall_question: RQ-CH03-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH03-02
      recall_question: RQ-CH03-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH03-03
      recall_question: RQ-CH03-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH03-04
      recall_question: RQ-CH03-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 3 — ModelGateway y la Invocación Real del Modelo

> **Regla constitucional (Article I, P-02):** el modelo es reemplazable — el runtime nunca debe
> depender estructuralmente de un proveedor específico.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de
> saber cómo se llama el componente de este capítulo. El detalle estructurado de esta sección
> vive en `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, dentro de la invocación real
de un modelo de lenguaje, qué tramo le pertenece en exclusiva al componente que este capítulo
introduce y qué tramos pertenecen a dominios distintos (continuación cognitiva, ejecución de una
tool call, selección de contexto) que ya tienen o todavía no tienen componente propio — y podrás
diseñar, para cualquier respuesta cruda de un proveedor, una representación normalizada que
distinga texto final de una propuesta de acción sin resolver esa propuesta prematuramente.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e
introduce dos contratos de datos (`ModelRequest`, `ModelResponse` — los dos últimos ids que seguían
reservados desde CH-00) y el tercer componente de runtime del libro (`ModelGateway`) — todavía sin
explicarlos, solo como mapa.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar
atrás; están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este
capítulo va a definir):

1. Ya que `AgentLoop` decide si debe ocurrir otro turno pero nunca invoca directamente ningún
   modelo (ver capítulo anterior), y que el modelo real puede pertenecer a proveedores completamente
   distintos entre sí, ¿quién adapta los mensajes de un turno hacia el formato que cada proveedor
   espera, y quién invoca realmente al modelo elegido?
2. Cuando la respuesta cruda de un proveedor de modelos llega con una forma distinta a la de
   cualquier otro proveedor, ¿cómo evitamos que el resto del ciclo cognitivo tenga que entender la
   forma particular de cada proveedor para saber si el modelo terminó de razonar o si propuso usar
   una herramienta?
3. Si el modelo propone usar una herramienta, ¿qué tan resuelta debe estar esa propuesta en el
   momento en que sale del componente que acaba de invocar al modelo, y quién es responsable de
   validar más adelante que esa propuesta realmente corresponde a una capacidad existente con
   argumentos válidos?
4. ¿Por qué el mismo componente que sabe cómo hablarle a un proveedor de modelos concreto no
   debería, además, decidir si el ciclo cognitivo completo debe continuar con otro turno?

## 1. Arquitectura Actual (Current Architecture)

CH-00 dejó instalados siete contratos de datos y dos componentes de runtime ya existen:
`AgentLoop` (CMP-001, CH-01) decide si otro turno de razonamiento debe ocurrir, y `ToolRuntime`
(CMP-002, CH-02) coordina la ejecución de una tool call ya resuelta. Ambos capítulos, sin embargo,
dejaron exactamente la misma deuda intencional documentada en sus respectivas secciones 18/19: las
señales que `AgentLoop.runTurn` consume (`modelFinished`, `modelProposesToolCall`, CH-01 §11) son
**señales de entrada asumidas** — nadie en el libro las produce todavía. `ModelGateway` seguía
siendo, hasta este capítulo, solo un nombre en la tabla de preview de
`constitution/ARCHITECTURE_CONSTITUTION.md` Article III, y ninguno de los tres invariantes que
Article II dedica explícitamente al modelo (INV-01, INV-02, INV-03) tenía todavía un componente
real que los hiciera cumplir en la práctica.

`registry/contracts.yaml` seguía reservando tres ids desde CH-01 §7 (`C-005`..`C-007`) para
`ContextSnapshot`/`ModelRequest`/`ModelResponse` — de los cuales `C-008`/`C-009` (`ToolCall`/
`ToolResult`) ya se asignaron en CH-02, dejando exactamente `C-005`..`C-007` como los tres únicos
ids todavía sin asignar.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas, la decisión "¿cómo se invoca realmente al modelo
seleccionado?" no tiene un lugar fijo donde vivir. Una implementación puede construir el payload
específico de un proveedor directamente dentro del ciclo cognitivo, acoplando `AgentLoop` al SDK de
ese proveedor (violando P-02, "the model is replaceable"); otra puede interpretar la respuesta
cruda del proveedor —con su forma particular de anunciar "terminé" o "quiero usar una
herramienta"— en el mismo lugar donde decide si continuar el turno, mezclando dos decisiones de
dominios distintos; una tercera puede, al encontrar que el modelo propuso usar una herramienta,
construir directamente el `ToolCall` completo y validado ella misma, sin que ningún componente
dedicado a resolver capacidades haya intervenido todavía.

Necesitamos que "¿cómo se invoca al modelo seleccionado?" tenga un dueño único y nombrado — y que
ese dueño devuelva una respuesta normalizada que el resto del sistema pueda consumir sin conocer el
proveedor real, y sin que esa normalización se adelante a resolver una propuesta de acción que
todavía no ha sido validada por nadie.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los ocho contratos y los dos componentes que existen hasta este punto no bastan porque:

- `AgentLoop.runTurn` (CH-01) consume `modelFinished`/`modelProposesToolCall` como señales de
  entrada asumidas — nadie las produce todavía en la práctica; sin `ModelGateway`, cerrar ese ciclo
  end-to-end es imposible;
- `ModelRequest` y `ModelResponse` siguen siendo dos de los tres nombres que CH-01 §7 dejó
  reservados sin contrato registrado — cualquier capítulo futuro que los use "por nombre" heredaría
  una versión ambigua, o peor, cada implementación futura los definiría de forma distinta;
- INV-01 ("`AgentCore` no depende directamente de APIs específicas de OpenAI, Anthropic, Google u
  otro proveedor") e INV-02 ("toda comunicación interna del runtime utiliza contratos propios,
  incluyendo `AgentMessage`") siguen siendo reglas declaradas desde CH-00, pero ningún componente
  real las ejercita todavía: `AgentMessage` (C-001) no tenía, hasta este capítulo, ningún
  componente registrado que lo consumiera (`used_by: []`);
- nada impide que, al recibir la respuesta del modelo, el mismo lugar del código que la interpreta
  decida también si el ciclo cognitivo debe continuar (`AgentLoop`, ya resuelto desde CH-01) o si
  una propuesta de tool call ya es una acción autorizada y ejecutable (`ToolRuntime`, ya resuelto
  desde CH-02) — aunque Article IV asigna cada una de esas decisiones a un dueño distinto.

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la
> secuencia `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una
> entidad que no haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT`
> registrado — **no magic entities**. Este capítulo aplica la misma disciplina de *ownership* que
> CH-01/CH-02 ya establecieron: ningún componente puede reclamar en prosa una responsabilidad que
> su propia ficha no declara en `owns` — y, por primera vez en el libro, con dos componentes reales
> ya existentes (`AgentLoop`, `ToolRuntime`) cuyas fronteras `ModelGateway` podría invadir por
> accidente si no se declaran explícitamente.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-01   Context is a first-class architectural component.
           ModelRequest transporta los AgentMessage ya seleccionados y el ExecutionBudget
           relevante — pero no decide qué mensajes incluir ni cómo priorizarlos; esa selección
           sigue siendo trabajo de ContextEngine (preview, no introducido en este capítulo).
    P-02   The model is replaceable.
           ModelGateway es la primera materialización concreta de este principio: ningún otro
           componente del libro depende estructuralmente de un proveedor específico — todos
           consumen ModelRequest/ModelResponse, nunca un payload propio de un SDK.
    P-10   The harness owns execution state—not the model.
           ModelGateway normaliza lo que el modelo propuso (ModelResponse), pero nunca asigna
           directamente ningún AgentRunStatus — esa transición sigue siendo exclusiva de
           AgentLoop (CH-01), que ModelGateway.does_not_own reafirma.
    P-12   Events observe; hooks intervene.
           invoke (seccion 11) emite un AgentEvent en cada resolución (éxito o fallo) — el
           tercer componente del libro que produce eventos en la práctica.
    P-13   Authorization is deterministic and external to the LLM.
           ModelResponse.proposedToolCall es una propuesta cruda, nunca una autorización — el
           modelo puede proponer una capacidad y argumentos, pero ModelGateway no los valida ni
           los ejecuta, y mucho menos los autoriza.

Invariants preserved
    INV-01   AgentCore no depende directamente de APIs específicas de OpenAI, Anthropic, Google
             u otro proveedor.
             Primera cita literal posible de este invariante: ya existe un ModelGateway real
             cuya ficha (owns: "selección de provider") es el único lugar del libro donde un
             adapter de proveedor concreto podría vivir — ningún otro componente lo necesita.
    INV-02   Toda comunicación interna del runtime utiliza contratos propios, incluyendo
             AgentMessage.
             Primera vez que AgentMessage (C-001, CH-00) es consumido realmente por un
             componente registrado: ModelRequest lo transporta sin modificarlo.
    INV-03   El modelo nunca constituye una fuente de autorización.
             ModelResponse.proposedToolCall (seccion 6) es, por diseño, una propuesta cruda sin
             validar — el modelo propone una capacidad por nombre y argumentos sin resolver;
             autorizarla o siquiera verificar que existe sigue sin ser decisión de ModelGateway.
    INV-18   Toda acción significativa produce un evento observable.
             invoke emite AgentEvent (MODEL_RESPONSE_RECEIVED / MODEL_INVOCATION_FAILED) en cada
             resolución.
    INV-19   Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy
             relevante.
             Cada AgentEvent que emite ModelGateway lleva el traceId de su ExecutionContext.
    INV-20   Todo error operacional pertenece a una categoría conocida.
             Cuando el proveedor no responde, invoke construye un HarnessError con
             category = MODEL (Article VII, "Model unavailable → model / potentially provider
             fallback") — nunca una excepción cruda del SDK subyacente.

Component ownership changes
    CMP-003 ModelGateway se introduce — registry/components.yaml pasa de 2 a 3 componentes.
    owns/does_not_own citados literalmente contra Article III (sección "ModelGateway") y
    Article IV.

Lifecycle changes
    Ninguno sobre AgentRunStatus (C-013): sigue siendo propiedad exclusiva de AgentLoop (CH-01),
    y su tabla de transiciones no cambia aquí. ModelResponse.finished/.proposedToolCall son,
    conceptualmente, la fuente real que un cableado futuro usaría para poblar
    modelFinished/modelProposesToolCall — pero ese cableado formal (modificar la firma de
    runTurn) sigue sin ocurrir en este capítulo (ver seccion 12/18).

Security implications
    Ninguna nueva superficie de ataque: P-05/P-13 se preservan. ModelGateway.does_not_own
    excluye explícitamente autorización — ProposedToolCall llega sin validar hasta el capítulo
    que finalmente la resuelva.

Observability implications
    ModelGateway es el tercer componente que emite AgentEvent en la práctica, extendiendo
    AgentEventType con dos valores nuevos (MODEL_RESPONSE_RECEIVED, MODEL_INVOCATION_FAILED)
    sin modificar el envelope AgentEvent (C-010) ni su STRUCT.

Deterministic vs agentic boundary
    Article XII se refina una tercera vez a nivel de componente: el modelo, dentro de este
    tramo, SÍ participa — es quien produce la propuesta semántica ("interpret intent",
    "propose a semantic next action", Article XII) — pero ModelGateway, determinístico, es
    quien decide cómo se invoca y cómo se normaliza esa propuesta hacia un ModelResponse, sin
    interpretarla ni autorizarla.
```

## 5. Conceptos Nuevos (New Concepts)

- **Model Invocation**: el tramo determinístico que adapta los mensajes de un turno hacia el
  formato de un proveedor concreto, invoca ese proveedor y normaliza su respuesta cruda —
  responsabilidad exclusiva de `ModelGateway` (Article III, Article IV: "`ModelGateway` → How
  should the selected model be invoked?").
- **Provider Adapter** *(preview conceptual — no se implementa ningún adapter concreto en este
  capítulo)*: la pieza que traduciría `ModelRequest` hacia el payload específico de un proveedor
  (OpenAI, Anthropic, Gemini, un modelo local) y su respuesta de vuelta hacia `ModelResponse`. Este
  capítulo trata "qué proveedor concreto responde" como una señal ya resuelta externamente (varias
  señales de entrada en el pseudocódigo de la seccion 11), no como un mecanismo propio — igual que
  CH-02 trató "qué implementación satisface una capability" como señal asumida.
- **Raw Proposal (propuesta cruda de tool call)**: la forma en la que `ModelResponse` representa
  que el modelo propuso usar una herramienta — nombre de capacidad y argumentos, sin resolver ni
  validar — para no invadir la responsabilidad de resolución/validación que Article III asigna a
  `ToolRuntime`/`CapabilityRegistry`. Modelada como `RawToolCallProposal` (seccion 6), un `STRUCT`
  embebido dentro de `ModelResponse` sin contrato `C-XXX` propio — igual que `AgentEventType` vive
  embebido dentro de `AgentEvent` sin contrato propio (CH-00/CH-02).
- **Streaming** *(citado literalmente en Article III, sección "ModelGateway" — no modelado en
  pseudocódigo en este capítulo)*: la entrega incremental de una respuesta del modelo. `invoke`
  (seccion 11) se muestra como una invocación síncrona de request/response completo; implementar el
  mecanismo de streaming (chunks incrementales, backpressure) queda fuera de alcance de este
  capítulo, aunque `owns` lo declare literalmente porque Article III se lo asigna a `ModelGateway`
  (ver seccion 18).
- **Decision Ownership** *(Article IV, en uso desde CH-01, ahora aplicado a un tercer componente)*:
  `ModelGateway` decide "¿cómo debe invocarse el modelo seleccionado?"; explícitamente NO decide
  "¿debe ocurrir otro turno?" (`AgentLoop`, ya resuelto), "¿cómo se ejecuta una acción aprobada?"
  (`ToolRuntime`, ya resuelto), "¿qué debería saber el modelo?" (`ContextEngine`, preview) ni "¿está
  permitida esta acción?" (`PolicyEngine`, preview).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados de CH-00/CH-01/CH-02

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `AgentId`, `RunId`, `SessionId`, `TraceId`,
`Timestamp`, `AgentMessage`, `AgentState`, `ExecutionContext`, `ExecutionBudget`, `AgentEvent`,
`HarnessError`.

### `AgentEventType` — extendido, sin redefinir `AgentEvent`

CH-02 extendió `AgentEventType` a seis valores (`RUN_STARTED`, `TURN_CONTINUED`, `RUN_COMPLETED`,
`RUN_FAILED`, `TOOL_CALL_COMPLETED`, `TOOL_CALL_FAILED`), sin contrato `C-XXX` propio. Este
capítulo agrega dos valores — los primeros eventos que observan la invocación de un modelo:

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
END
```

`AgentEvent` (C-010) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — solo el rango de
valores permitido para `eventType` crece, igual que en CH-01 y CH-02.

### `RawToolCallProposal` — la propuesta cruda embebida (sin `C-XXX` propio)

```pseudocode
STRUCT RawToolCallProposal
    capabilityName: Text
    rawArguments: Map<Text, Value>
END
```

Deliberadamente **no** es un `ToolCall` (C-008, CH-02): no tiene `id` (`ToolCallId`) ni
`requestedAt`, y `capabilityName` es texto libre todavía sin resolver contra ningún registro de
capacidades — resolverlo hacia un `CapabilityId` real y envolverlo en un `ToolCall` con identidad
propia es, explícitamente, trabajo de un capítulo posterior (ver seccion 18/19). Vive embebido
dentro de `ModelResponse`, sin contrato `C-XXX` propio — el mismo patrón que `AgentEventType` (CH-00)
o `ErrorCategory` (CH-00): un tipo real, con `STRUCT` propio, que ningún capítulo registra como
contrato independiente.

### `ModelRequest` — la forma empaquetada e independiente de proveedor

```pseudocode
STRUCT ModelRequest
    messages: List<AgentMessage>
    budget: ExecutionBudget
    requestedAt: Timestamp
END
```

`messages` transporta los `AgentMessage` (C-001, CH-00) que el turno ya construyó — `ModelRequest`
no decide qué mensajes incluir ni cómo priorizarlos (esa selección es de `ContextEngine`, preview,
Article III); solo empaqueta los que ya llegaron. `budget` reutiliza `ExecutionBudget` (C-012,
CH-00) para transportar los límites de generación relevantes (p. ej. `maxOutputTokens`), sin
redefinir ningún campo nuevo de presupuesto.

### `ModelResponse` — la respuesta normalizada, independiente de proveedor

```pseudocode
STRUCT ModelResponse
    finished: Boolean
    content: Optional<Value>
    proposedToolCall: Optional<RawToolCallProposal>
    producedAt: Timestamp
END
```

`finished` y `proposedToolCall` son la contraparte normalizada de las señales que `AgentLoop.runTurn`
(CH-01 §11) ya consume por nombre (`modelFinished`, `modelProposesToolCall`) — pero conectar
formalmente ambos capítulos (que `runTurn` reciba un `ModelResponse` en vez de dos booleanos sueltos)
sigue siendo trabajo de un capítulo posterior (ver seccion 12/18). `content` transporta la
respuesta textual final cuando `finished = TRUE`; `proposedToolCall`, cuando no es `NULL`, es
siempre una propuesta cruda (ver `RawToolCallProposal` arriba) — nunca un `ToolCall` (C-008) ya
resuelto.

**Unchanged / Not yet introduced**: `ContextSnapshot` sigue siendo el único id reservado desde
CH-00 (`C-005`) — llega junto con `ContextEngine` en un capítulo posterior. Tampoco se introduce
ningún `STRUCT Tool`, `INTERFACE ModelGateway` formal con múltiples `IMPLEMENTATION` (por
proveedor), ni `CapabilityRegistry` — este capítulo trata "qué proveedor concreto responde" y "qué
capacidad satisface `capabilityName`" como preview, sin definirlos como contrato propio todavía
(ver seccion 9/18).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía (formalizar `ModelGateway`
como interfaz con múltiples `IMPLEMENTATION` por proveedor, al estilo del ejemplo de
`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §7, queda para cuando este libro necesite modelar
más de un provider real). Introduce dos contratos de datos, registrados en
`registry/contracts.yaml`:

```text
ID:                     C-006
Name:                   ModelRequest
Version:                v1
Introduced In:          CH-03
Current Definition:     STRUCT ModelRequest (ver §6)
Used By:                [CMP-003]
Modified By:            []
Constitutional Impact:  [P-01, P-02, INV-02]
```

```text
ID:                     C-007
Name:                   ModelResponse
Version:                v1
Introduced In:          CH-03
Current Definition:     STRUCT ModelResponse (ver §6)
Used By:                [CMP-003]
Modified By:            []
Constitutional Impact:  [P-10, P-13, INV-03]
```

Con `C-006` y `C-007` ya asignados, `C-005` (`ContextSnapshot`) queda como el único id todavía
reservado — la reserva completa de tres ids que CH-01 §7 documentó (`C-005`..`C-007`) termina de
resolverse en este capítulo, dos capítulos después de que CH-02 resolviera `C-008`/`C-009`.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el tercer componente de runtime del libro:

```pseudocode
COMPONENT ModelGateway
    consumes: AgentMessage, ExecutionContext, ModelRequest
    produces: ModelResponse, AgentEvent, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Article III (sección "ModelGateway"):

```text
COMPONENT: ModelGateway

Responsibility:
    Seleccionar el provider de modelo correspondiente, adaptar los AgentMessage de un turno (más
    los límites de generación relevantes) hacia el ModelRequest que ese provider espera, invocar
    al modelo, soportar streaming y normalizar la respuesta cruda del provider hacia un
    ModelResponse — sin decidir si otro turno de razonamiento debe ocurrir, sin ejecutar ninguna
    tool call y sin resolver ninguna propuesta de acción hacia un ToolCall validado.

Consumes:
    C-001 AgentMessage, C-004 ExecutionContext, C-006 ModelRequest

Depends on:
    (ninguno todavía — ContextEngine y PolicyEngine son Preview, no introducidos en este
    capítulo; ver seccion 9)

Produces:
    C-007 ModelResponse, C-010 AgentEvent (MODEL_RESPONSE_RECEIVED / MODEL_INVOCATION_FAILED),
    C-011 HarnessError (embebido en un fallo de invocación)

Owns (Article III, cita literal):
    - selección de provider
    - adaptación de mensajes
    - invocación del modelo
    - streaming
    - normalización de respuestas

Does NOT own (Article IV — declarado con el mismo peso que Owns):
    - decidir si otro turno de razonamiento debe ocurrir (AgentLoop, CMP-001, ya introducido en
      CH-01 — Article IV: "AgentLoop → Should another reasoning turn occur?")
    - ejecutar tools/side effects (ToolRuntime, CMP-002, ya introducido en CH-02 — Article IV:
      "ToolRuntime → How should an approved action be executed?")
    - seleccionar/rankear/componer contexto (ContextEngine, Article III — no introducido en este
      capítulo, es un componente distinto)
    - policy/autorización de una acción (PolicyEngine, Article IV — no introducido en este
      capítulo)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con una
particularidad respecto a CH-01/CH-02: dos de las cuatro exclusiones ya no son "preview, todavía
sin componente", sino fronteras contra componentes reales que ya existen (`AgentLoop`,
`ToolRuntime`). `ModelGateway` es el primer componente del libro que debe declarar explícitamente
que no invade el territorio de otro componente ya construido, no solo de uno futuro.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
ModelGateway
    consumes → AgentMessage, ExecutionContext, ModelRequest
    produces → ModelResponse, AgentEvent, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`ModelGateway` no depende hoy de ningún otro componente registrado. En prosa (nunca dentro de un
bloque `pseudocode`, per `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las
dependencias futuras que capítulos posteriores agregarán son:

| Componente futuro (Preview — no introducido en este capítulo) | Qué le daría a `ModelGateway` |
|---|---|
| `ContextEngine` | la selección/ranking/composición real de los `AgentMessage` que hoy `ModelRequest` recibe ya resueltos |
| `PolicyEngine` | ninguna relación directa nueva — `ModelGateway` seguiría sin decidir autorización aunque `PolicyEngine` exista |

`AgentLoop` (CMP-001, ya existente) sería, en la práctica, quien invoque a `ModelGateway` para
obtener un `ModelResponse` — pero esa relación es la inversa de una `dependency` en el sentido de
`registry/components.yaml` (`AgentLoop` dependería de `ModelGateway`, no al revés), y ese cableado
formal (agregar `CMP-003` a `AgentLoop.dependencies`, extender la firma de `runTurn` para que
consuma un `ModelResponse` en vez de dos booleanos sueltos) es, explícitamente, trabajo de un
capítulo posterior — el mismo patrón que CH-02 §9 ya estableció para la relación inversa entre
`AgentLoop` y `ToolRuntime`. `book/chapters/01-agent-loop/chapter.md` no se modifica para
reflejarlo todavía (fuera de su campo `next_chapter`, ya actualizado por CH-02).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[AgentLoop — arma los mensajes del turno, CH-01] → ModelGateway → [Provider real — Preview, no
introducido] → ModelGateway → [AgentLoop retoma con un ModelResponse]
```

**Vista 2 — Sequence**

```text
AgentLoop
   │ arma pendingMessages: List<AgentMessage> para este turno
   ▼
ModelGateway
   │ invokeModelForTurn(state, execution, pendingMessages, ...)
   │ empaqueta pendingMessages + execution.budget → ModelRequest
   │ invoke(request, execution, ...)
   │ selecciona provider / adapta ModelRequest (Preview — provider real no modelado)
   │ invoca al modelo (Preview — provider real no modelado)
   │ normaliza la respuesta cruda → ModelResponse
   │ emite: AgentEvent (MODEL_RESPONSE_RECEIVED | MODEL_INVOCATION_FAILED)
   ▼
ModelResponse
   │
   ▼
[AgentLoop retoma el ciclo con este ModelResponse — Preview, el cableado formal hacia
modelFinished/modelProposesToolCall es trabajo de un capítulo posterior, ver seccion 12/18]
```

**Vista 3 — Pseudocódigo**

Ver §11: `invoke` es la primera formalización ejecutable de "`ModelGateway` decide cómo se invoca
el modelo seleccionado"; `invokeModelForTurn` es la primera vez que el libro puede mostrar, con
pseudocódigo real, el tramo completo `AgentLoop → ModelGateway → ModelResponse` usando tres
componentes que ya existen los tres.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde
CH-00/CH-01/CH-02.

```pseudocode
FUNCTION invoke(
    request: ModelRequest,
    execution: ExecutionContext,
    agentId: AgentId,
    providerRespondedSuccessfully: Boolean,
    providerFinished: Boolean,
    providerProposesToolCall: Boolean,
    providerCapabilityName: Text,
    providerRawArguments: Map<Text, Value>,
    providerContent: Value
) -> ModelResponse

    IF NOT providerRespondedSuccessfully
        failure: HarnessError = HarnessError(
            category = MODEL,
            code = "MODEL_UNAVAILABLE",
            message = "El provider seleccionado no respondió a esta invocación",
            recoverable = TRUE,
            retryable = TRUE,
            metadata = {}
        )

        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = MODEL_INVOCATION_FAILED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = failure
        )

        THROW failure
    END

    proposal: RawToolCallProposal = NULL

    IF providerProposesToolCall
        proposal = RawToolCallProposal(
            capabilityName = providerCapabilityName,
            rawArguments = providerRawArguments
        )
    END

    response: ModelResponse = ModelResponse(
        finished = providerFinished,
        content = providerContent,
        proposedToolCall = proposal,
        producedAt = now()
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = MODEL_RESPONSE_RECEIVED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = response
    )

    RETURN response
END
```

`newEventId()` y `now()` son las mismas primitivas de CH-00/CH-01/CH-02 (no son entidades
arquitectónicas ni componentes). `providerRespondedSuccessfully`, `providerFinished`,
`providerProposesToolCall`, `providerCapabilityName`, `providerRawArguments` y `providerContent` son
señales de entrada — igual que `modelFinished`/`modelProposesToolCall` en CH-01 §11 y
`capabilityResolved`/`inputValid` en CH-02 §11 — que un `Provider Adapter` todavía sin introducir
(seccion 5) produciría en la realidad. `invoke` no decide qué proveedor invocar ni cómo adaptar el
payload concreto: recibe el resultado ya asumido de esa invocación y decide, determinísticamente,
qué `ModelResponse` normalizado construir a partir de él.

Por primera vez en el libro, con los tres componentes de runtime ya existentes (`AgentLoop`,
`ToolRuntime`, y `ModelGateway` recién definido en este mismo capítulo), se puede mostrar el tramo
completo `AgentLoop → ModelGateway → ModelResponse` con pseudocódigo real:

```pseudocode
FUNCTION invokeModelForTurn(
    state: AgentState,
    execution: ExecutionContext,
    pendingMessages: List<AgentMessage>,
    providerRespondedSuccessfully: Boolean,
    providerFinished: Boolean,
    providerProposesToolCall: Boolean,
    providerCapabilityName: Text,
    providerRawArguments: Map<Text, Value>,
    providerContent: Value
) -> ModelResponse

    request: ModelRequest = ModelRequest(
        messages = pendingMessages,
        budget = execution.budget,
        requestedAt = now()
    )

    response: ModelResponse = invoke(
        request,
        execution,
        state.agentId,
        providerRespondedSuccessfully,
        providerFinished,
        providerProposesToolCall,
        providerCapabilityName,
        providerRawArguments,
        providerContent
    )

    RETURN response
END
```

`invokeModelForTurn` es una demostración de integración, no una tercera responsabilidad nueva: no
es un método registrado de ninguna ficha de componente (`ModelGateway.consumes`/`.produces` ya
quedaron declarados en la seccion 8 sin este nombre), y **no** modifica `CMP-001 AgentLoop` —
ni su ficha, ni sus `consumes`/`produces`/`dependencies` en `registry/components.yaml`, ni la firma
de `runTurn` (CH-01 §11), que sigue consumiendo exactamente los mismos dos booleanos que consumía
antes de este capítulo. Muestra únicamente que, con los tres componentes ya existentes, es posible
construir el `ModelRequest` a partir de mensajes que `AgentLoop` ya tendría armados y obtener un
`ModelResponse` real de vuelta — el cableado formal que haría que `runTurn` reciba ese
`ModelResponse` en lugar de dos booleanos sueltos sigue siendo, explícitamente, trabajo de un
capítulo posterior (ver seccion 12/18/19).

Nótese lo que ni `invoke` ni `invokeModelForTurn` hacen: no deciden ningún `AgentRunStatus` (Article
IV, "`AgentLoop` → Should another reasoning turn occur?" sigue sin respuesta aquí), no ejecutan
ningún `ToolRuntime.execute(...)` real ni construyen un `ToolCall` (C-008) a partir de
`proposedToolCall` (Article IV, "`ToolRuntime` → How should an approved action be executed?" y
"`CapabilityRegistry` → What implementation satisfies a requested capability?" siguen sin
respuesta), y no evalúan ninguna policy sobre la propuesta recibida (P-13).

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013): esa máquina de estados sigue
siendo propiedad exclusiva de `AgentLoop` (CH-01 §12), y su tabla de transiciones no cambia aquí.

`invoke` (§11) sí atraviesa un camino implícito con dos desenlaces — pero deliberadamente **no** se
formaliza como un nuevo contrato de lifecycle en este capítulo (eso introduciría una tercera
entidad nueva, fuera del alcance decidido para este capítulo):

```text
ModelRequest enviado
   → provider no responde        → HarnessError (category = MODEL, code = MODEL_UNAVAILABLE)
   → provider responde, terminó   → ModelResponse (finished = TRUE, content = ...)
   → provider responde, propone   → ModelResponse (finished = FALSE, proposedToolCall = ...)
     una tool call
```

**Lo que este capítulo explícitamente no cierra**: la tabla de transiciones de `AgentRunStatus`
(CH-01 §12) sigue anotando `WAITING_FOR_MODEL → COMPLETED (runTurn: modelFinished)` y
`WAITING_FOR_MODEL → WAITING_FOR_TOOL (runTurn: modelProposesToolCall)` exactamente como CH-01 las
dejó. Ese texto seguía siendo literalmente cierto en los dos capítulos anteriores porque
`ModelGateway` no existía; ahora que existe, la pieza que falta no es `ModelGateway` en sí, sino el
cableado que tomaría el `ModelResponse` que este capítulo sí sabe producir (`response.finished`,
`response.proposedToolCall`) y lo usaría para poblar `modelFinished`/`modelProposesToolCall` — ese
cableado pertenece a un capítulo posterior (ver seccion 18/19), y `book/chapters/01-agent-loop/chapter.md`
no se modifica para reflejarlo todavía (fuera de su campo `next_chapter`, ya actualizado por CH-02).

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6) clasifica también los fallos que introduce este capítulo,
fiel a los `Failure Examples` de `constitution/ARCHITECTURE_CONSTITUTION.md` Article VII:

```text
MODEL
    MODEL_UNAVAILABLE   — el provider seleccionado no respondió a esta invocación ("Model
                           unavailable → model / potentially provider fallback", Article VII)
        → recoverable: TRUE, retryable: TRUE
```

`invoke` nunca devuelve una excepción cruda del SDK subyacente ni un `ModelResponse` a medias
cuando el proveedor no responde: siempre construye un `HarnessError` con `category`, `recoverable`
y `retryable` explícitos — mismo patrón que `runTurn` (CH-01 §11) y `executeToolCall` (CH-02 §11).

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo de `category = POLICY`
(autorización denegada sobre una `proposedToolCall`) o `category = VALIDATION` (una
`proposedToolCall` cuyo `capabilityName` no existe) sigue sin ser responsabilidad de
`ModelGateway` — su propio `does_not_own` (seccion 8) excluye explícitamente esas decisiones; esa
clasificación pertenece al capítulo que finalmente resuelva `proposedToolCall` hacia un `ToolCall`
real.

## 14. Eventos Producidos (Events Produced)

Este capítulo agrega dos valores a `AgentEventType` (seccion 6) — los primeros que observan la
invocación de un modelo, no la continuación de un turno ni la ejecución de una tool call:

```text
MODEL_RESPONSE_RECEIVED   — ModelGateway invocó al modelo y normalizó su respuesta con éxito
                            (invoke, §11)
MODEL_INVOCATION_FAILED   — ModelGateway no pudo completar la invocación (invoke, §11)
```

`RUN_STARTED`, `TURN_CONTINUED`, `RUN_COMPLETED`, `RUN_FAILED` (CH-00/CH-01) y
`TOOL_CALL_COMPLETED`/`TOOL_CALL_FAILED` (CH-02) no se emiten desde `invoke`: pertenecen al ciclo
cognitivo que posee `AgentLoop` o a la ejecución que posee `ToolRuntime`, no a la invocación del
modelo. Un capítulo posterior que conecte los tres extremos (ver seccion 18/19) podrá correlacionar
un `MODEL_RESPONSE_RECEIVED` con el siguiente `TURN_CONTINUED` o `TOOL_CALL_COMPLETED` sin
redefinir el envelope común `AgentEvent` (C-010).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

Este capítulo no implementa autorización todavía (no existe `PolicyEngine` — ver seccion 9), y
`ModelGateway.does_not_own` lo declara explícitamente:

- **P-13 — Authorization is deterministic and external to the LLM**: se preserva sin cambios.
  `ModelResponse.proposedToolCall` es una propuesta cruda del modelo — `ModelGateway` no la
  convierte en un `ToolCall` ejecutable, no verifica que `capabilityName` exista, y no evalúa si
  esos argumentos serían autorizados. Esa cadena completa (Article VI: `Tool Intent → Resolve
  Capability → Validate Schema → ... → Authorization`) sigue empezando después de este capítulo,
  no dentro de él.
- **INV-03 — El modelo nunca constituye una fuente de autorización**: `proposedToolCall` puede
  nombrar cualquier `capabilityName`, incluso uno inexistente o malicioso — `invoke` no lo filtra,
  porque filtrarlo sería resolver la propuesta, no solo normalizarla. Ese filtro pertenece a
  `ToolRuntime`/`CapabilityRegistry` en un capítulo posterior.
- **P-02 — The model is replaceable**: `ModelGateway` es el único punto del libro donde un adapter
  de proveedor concreto podría introducir código específico de un vendor — ningún otro componente
  (`AgentLoop`, `ToolRuntime`) necesita conocer qué proveedor respondió.

`ModelResponse` es, por diseño, la forma en que `ModelGateway` comunica lo que el modelo propuso —
nunca una afirmación de que esa propuesta ya es segura, válida o autorizada.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST InvokeNeverConstructsAToolCallDirectlyFromAProposedToolCall
TEST InvokeNeverDecidesAgentRunStatusTransition
TEST InvokeNeverInvokesToolRuntimeOrPolicyEngineDirectly
TEST InvokeAlwaysEmitsAnAgentEventOnSuccessOrFailure
TEST ModelResponseProposedToolCallIsAlwaysRawAndUnvalidated
TEST ModelUnavailableIsRecoverableAndRetryable
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.1, después de CH-03)

Constitution
 ├── Article I    — Principles (P-01 .. P-15)
 ├── Article II   — Invariants (INV-01 .. INV-20)
 ├── Article III  — Component Sovereignty (AgentLoop, ToolRuntime, ModelGateway: tres
 │                  componentes instanciados)
 ├── Article IV   — Decision Ownership (en uso: los tres componentes declaran owns/does_not_own)
 └── Article VI   — Execution Constitution (sin cambios respecto a CH-02)

Contracts (registry/contracts.yaml)
 ├── C-001 AgentMessage        (CH-00 — consumido por un componente real por primera vez: CMP-003)
 ├── C-002 AgentConfig         (CH-00)
 ├── C-003 AgentState          (CH-00)
 ├── C-004 ExecutionContext    (CH-00)
 ├── C-006 ModelRequest        (CH-03, nuevo — formaliza el id reservado desde CH-01)
 ├── C-007 ModelResponse       (CH-03, nuevo — formaliza el id reservado desde CH-01)
 ├── C-008 ToolCall            (CH-02)
 ├── C-009 ToolResult          (CH-02)
 ├── C-010 AgentEvent          (CH-00)
 ├── C-011 HarnessError        (CH-00)
 ├── C-012 ExecutionBudget     (CH-00)
 └── C-013 AgentRunStatus      (CH-01)

Components (registry/components.yaml)
 ├── CMP-001 AgentLoop         (CH-01)
 ├── CMP-002 ToolRuntime       (CH-02)
 └── CMP-003 ModelGateway      (CH-03, nuevo — tercer componente del libro)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado formal `AgentLoop ↔ ModelGateway`**: `invokeModelForTurn` (§11) es una demostración
  de integración, no una modificación real de `runTurn` (CH-01 §11). Que `AgentLoop.runTurn`
  consuma un `ModelResponse` real en vez de dos booleanos sueltos (`modelFinished`,
  `modelProposesToolCall`) — y que `CMP-003` se agregue a `AgentLoop.dependencies` en
  `registry/components.yaml` — sigue siendo trabajo de un capítulo posterior.
- **La resolución de `proposedToolCall` hacia un `ToolCall` real**: `RawToolCallProposal` no se
  valida, no se resuelve contra ningún registro de capacidades, y no se envuelve en un `ToolCall`
  (C-008) en este capítulo. Ese trabajo requiere `CapabilityRegistry` (para resolver
  `capabilityName` hacia un `CapabilityId` real) y, probablemente, el mismo capítulo que cablee
  `ModelGateway` con `ToolRuntime` de punta a punta.
- **Provider Adapters reales**: no existe ningún `IMPLEMENTATION OpenAIModelGateway`,
  `AnthropicModelGateway` ni equivalente. `providerRespondedSuccessfully`,
  `providerFinished`/`providerProposesToolCall`/`providerCapabilityName`/`providerRawArguments`/
  `providerContent` son señales de entrada asumidas — ningún componente de este libro las produce
  todavía en la práctica.
- **Streaming real**: mencionado en `owns` (Article III lo exige literalmente), pero no modelado en
  pseudocódigo — `invoke` es una invocación síncrona de request/response completo.
- **`ContextEngine`**: `ModelRequest.messages` recibe los `AgentMessage` ya seleccionados como
  dados — qué mensajes incluir, cómo priorizarlos o resumirlos (P-01, P-14) sigue sin componente
  propio.
- **`PolicyEngine`**: sigue sin existir; P-05/P-13 y la evaluación de una `proposedToolCall` siguen
  siendo reglas declaradas, no reglas exigidas por código.
- **Persistencia real de `AgentState`/`SessionState`, human-in-the-loop implementado, reviewers
  plurales, evals y orquestación multi-agente**: sin cambios respecto a CH-00/CH-01/CH-02 —
  explícitamente fuera de alcance de BH-v0.1.

## 19. Siguiente Incremento (Next Increment)

El problema natural del próximo capítulo: ahora que los tres componentes centrales del ciclo
cognitivo existen (`AgentLoop`, `ToolRuntime`, `ModelGateway`), ¿quién resuelve una
`proposedToolCall` cruda hacia un `ToolCall` real y validado — y quién cablea formalmente los tres
componentes de punta a punta, para que un `AgentRun` real pueda completar un turno completo sin que
ninguna señal siga siendo "asumida"? Eso apunta hacia `CapabilityRegistry` (Article IV: "What
implementation satisfies a requested capability?") como el cuarto componente candidato de Article
III que dejaría de ser preview, y hacia el capítulo que finalmente conecte `AgentLoop.runTurn`,
`ModelGateway.invoke` y `ToolRuntime.executeToolCall` en una sola ejecución real — probablemente
también el momento en que `PolicyEngine` deje de ser preview, para que una `proposedToolCall` recién
resuelta pueda además autorizarse antes de ejecutarse.

Ese capítulo (`CH-04`, fuera del alcance de esta ejecución) heredaría directamente la deuda
intencional de §18. `next_chapter` queda en `null` en el frontmatter de este capítulo porque, en
este momento del libro, `CH-04` todavía no existe como archivo — solo como el problema que
motivará su escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de
> la secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco
> Iceberg / Bucles de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas,
> Forrester/Meadows), secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): sin un dueño explícito para "¿cómo se invoca realmente al
   modelo elegido?", cada implementación termina acoplando el ciclo cognitivo completo al SDK
   particular de un proveedor — su formato de mensajes y su forma de anunciar "terminé" o "quiero
   usar una herramienta" se filtran hacia arriba, y cambiar de proveedor exige reescribir el ciclo
   entero.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): sin un componente
   con fronteras explícitas, la invocación del modelo tiende a absorber silenciosamente decisiones
   vecinas (continuación cognitiva, autorización de una acción propuesta) solo porque físicamente
   es el único lugar del código que "ya tiene la respuesta a la mano" — exactamente lo que Article
   IV prohíbe.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `ModelGateway` (CMP-003) con una ficha que declara tanto lo que posee (`owns`) como lo que
   explícitamente NO posee (`does_not_own`) y formaliza `ModelRequest` (C-006) y `ModelResponse`
   (C-007), los dos últimos ids que seguían reservados desde CH-00.
4. **Modelos mentales** (= §4, Constitutional Impact): el Ownership Rule de Article IV, junto con
   P-02 ("The model is replaceable") — el runtime nunca debe depender estructuralmente de un
   proveedor específico.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un componente nuevo se introduce sin declarar
  explícitamente su `does_not_own`, aumenta la probabilidad de que absorba silenciosamente la
  próxima decisión vecina "porque ya estaba ahí" — el mismo bucle que CH-01 y CH-02 ya cortaron.
  Este capítulo repite el corte para `ModelGateway`, ahora contra dos componentes reales ya
  existentes, no solo contra dos previews.
- **Bucle de equilibrio (estabiliza):** `invoke` (§11) normaliza la respuesta cruda del proveedor
  hacia un `ModelResponse` cuyo `proposedToolCall`, cuando existe, es deliberadamente una propuesta
  sin validar — nunca un `ToolCall` real — en vez de dejar que `ModelGateway` decida por su cuenta
  que una capacidad existe o que sus argumentos son válidos.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `ModelResponse` represente una propuesta de
tool call cruda y sin validar (`proposedToolCall: Optional<RawToolCallProposal>`), en vez de que
`ModelGateway` resuelva esa propuesta hacia un `ToolCall` completo él mismo. Si `ModelGateway`
cruzara esa línea, estaría invadiendo la responsabilidad de resolución/validación que Article III
asigna a `ToolRuntime` y a `CapabilityRegistry` — el próximo capítulo que cablee los tres
componentes de punta a punta heredaría una frontera ya confundida en vez de una frontera clara.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado
> completo de esta sección (con ids estables para cada pregunta/tarjeta) vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida. Aquí se
> presenta en prosa, para lectura directa del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Ya que `AgentLoop` decide si debe ocurrir otro turno pero nunca invoca directamente ningún
   modelo, y que el modelo real puede pertenecer a proveedores completamente distintos entre sí,
   ¿quién adapta los mensajes de un turno hacia el formato que cada proveedor espera, y quién
   invoca realmente al modelo elegido? *(cierra la pregunta guía 1)*
2. Cuando la respuesta cruda de un proveedor de modelos llega con una forma distinta a la de
   cualquier otro proveedor, ¿cómo evitamos que el resto del ciclo cognitivo tenga que entender la
   forma particular de cada proveedor para saber si el modelo terminó de razonar o si propuso usar
   una herramienta? *(cierra la pregunta guía 2)*
3. Si el modelo propone usar una herramienta, ¿qué tan resuelta debe estar esa propuesta en el
   momento en que sale del componente que acaba de invocar al modelo, y quién es responsable de
   validar más adelante que esa propuesta realmente corresponde a una capacidad existente con
   argumentos válidos? *(cierra la pregunta guía 3)*
4. ¿Por qué el mismo componente que sabe cómo hablarle a un proveedor de modelos concreto no
   debería, además, decidir si el ciclo cognitivo completo debe continuar con otro turno? *(cierra
   la pregunta guía 4)*

### Explicar

1. `ModelGateway` posee adaptar mensajes e invocar al modelo. Explica, como si hablaras con alguien
   sin contexto técnico, por qué NO posee decidir si debe ocurrir otro turno de razonamiento,
   aunque sea el único componente que realmente "habla" con el modelo — ¿qué se rompería, en
   concreto, si `ModelGateway` empezara a decidir eso directamente "ya que de todos modos es quien
   recibe la respuesta primero"?
2. `ModelResponse.proposedToolCall` es una propuesta cruda, sin validar. Explica por qué
   `ModelGateway` no construye directamente un `ToolCall` (C-008, ya existente desde CH-02) a
   partir de esa propuesta — ¿qué principio de Article IV estaría violando si lo hiciera, y qué
   perderíamos si cada componente que "toca primero" un dato decidiera también resolverlo por su
   cuenta?

### Conectar

1. Cuando `ModelResponse.finished` es `TRUE` o `ModelResponse.proposedToolCall` no es nulo, ¿qué
   dos señales booleanas de `runTurn` (`AgentLoop`, CH-01) tendría que poblar quien conecte ambos
   capítulos, y qué dos campos de `proposedToolCall` necesitaría además quien construya el
   `ToolCall` (`ToolRuntime`, CH-02) correspondiente?

### Espaciar

Las cuatro tarjetas de repaso de este capítulo (dos sobre `ModelGateway` — su `owns` y su
`does_not_own` — y una por cada contrato, `ModelRequest`/`ModelResponse`) entran hoy en
`reviewStage = DAY_1`. Repásalas de nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) —
ver el apéndice de tarjetas al final del libro (edición PDF) o `retrieval_set.flashcards` en
`dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te
equivocaste, ese es precisamente el punto ciego que este método existe para revelar.
