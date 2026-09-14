---
id: CH-08
title: "CapabilityRegistry y la Resolución Real de una Tool Call"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-008]
introduces_contracts: [C-018]
modifies_contracts: []
constitutional_articles: [P-03, P-13, P-26, INV-03, INV-04, INV-05, INV-18, INV-19, INV-20]
previous_chapter: CH-07
next_chapter: CH-09
retrieval_set:
  expected_outcome:
    id: EO-CH08
    text: |
      Al terminar este capítulo podrás distinguir, dentro de la resolución de una propuesta cruda
      de tool call, qué tramo le pertenece en exclusiva al componente que decide qué implementación
      satisface una capacidad solicitada y qué tramos pertenecen a dominios distintos (interpretar
      la respuesta del modelo, ejecutar la acción ya resuelta, autorizarla) — y podrás diseñar,
      para cualquier nombre de capacidad y argumentos crudos, el mecanismo que los resuelve hacia
      una intención de acción ya validada y lista para ejecutarse, sin que esa resolución decida
      por sí sola si la acción está permitida.
  skeleton:
    id: SK-CH08
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
    components_to_be_introduced: [CMP-008]
    contracts_to_be_introduced: [C-018]
  guiding_questions:
    - id: GQ-CH08-01
      text: |
        Cuando el modelo propone usar una herramienta nombrándola solo por texto libre y con
        argumentos todavía sin resolver (ver capítulo sobre la invocación real del modelo), ¿quién
        decide qué implementación concreta corresponde a ese nombre, y qué necesita existir de
        antemano para que esa decisión sea posible?
      answered_by: RQ-CH08-01
    - id: GQ-CH08-02
      text: |
        Si esa propuesta llega con argumentos que no corresponden a lo que la implementación
        resuelta espera recibir, ¿en qué momento exacto del camino debe detectarse ese desajuste, y
        qué le impide a una intención de acción mal formada seguir avanzando hacia su ejecución?
      answered_by: RQ-CH08-02
    - id: GQ-CH08-03
      text: |
        Dos capítulos distintos ya dejaron marcada la misma frontera desde lados opuestos — uno
        diciendo "esto todavía no está resuelto, solo lo transporto" y otro diciendo "resolver esto
        no me corresponde a mí, solo ejecuto lo ya resuelto". ¿Qué necesita existir para que esa
        frontera compartida por fin tenga, en la práctica, quien la ocupe?
      answered_by: RQ-CH08-03
    - id: GQ-CH08-04
      text: |
        ¿Alcanza con verificar que exista una implementación para el nombre de capacidad solicitado,
        o hace falta además algo que describa qué versión de esa implementación es y qué forma de
        entrada espera recibir, antes de aceptar cualquier argumento que llegue junto al nombre?
      answered_by: RQ-CH08-04
  systems_lens:
    iceberg_visible_fact: |
      El componente que decide "qué implementación satisface una capacidad solicitada" lleva citado
      treinta veces a lo largo de los primeros ocho capítulos del libro — veintiuna de ellas
      concentradas, en partes casi iguales, entre el capítulo que ejecuta tool calls y el que invoca
      al modelo — siempre como una deuda pendiente, nunca como código real: el campo
      `ToolCall.capability` (C-008) exige un `CapabilityId` ya resuelto desde CH-02, y
      `ModelResponse.proposedToolCall` (C-007) transporta, desde CH-03, un nombre de capacidad como
      texto libre sin resolver — y entre ambos extremos, hasta este capítulo, no existía ningún
      mecanismo real que los conectara (ver seccion 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite, ahora aplicado a la resolución de capacidades, es que dos
      componentes ya construidos pueden declarar honestamente, cada uno desde su propio
      `does_not_own`, que una responsabilidad no les pertenece — y aun así esa responsabilidad
      quedar sin dueño real durante varios capítulos, porque declarar una exclusión no es lo mismo
      que instalar el componente que la ocupa. Sin ese componente, "el nombre de capacidad existe"
      y "el nombre de capacidad está autorizado para usarse ahora" corren el riesgo de tratarse como
      la misma pregunta, aunque Article IV las asigna a filas distintas de su tabla (ver seccion 3,
      Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala el octavo componente real del libro, `CapabilityRegistry` (CMP-008),
      con una ficha que declara tanto lo que posee (`owns`: registrar el descriptor de una
      capability, resolver su nombre contra ese registro, validar sus argumentos crudos contra el
      schema declarado, desacoplar la intención de su implementación concreta — cita literal de
      Article III) como lo que explícitamente NO posee (`does_not_own`: ejecutar la capability ya
      resuelta, invocar al modelo o interpretar su propuesta cruda, evaluar policy/autorización,
      decidir continuación de turno) — y formaliza `CapabilityDescriptor` (C-018), el primer
      contrato del libro que incluye un campo de versión explícito (ver seccion 8, Component
      Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior sigue siendo el Ownership Rule de Article IV,
      ahora aplicado a un octavo componente, junto con la cita literal de Article III
      ("`CapabilityRegistry` → Responsable de desacoplar la intención de una capacidad de su
      implementación concreta") y la fila correspondiente de Article IV ("`CapabilityRegistry` →
      What implementation satisfies a requested capability?") — la pregunta que este capítulo, por
      primera vez, responde con código real en vez de con una exclusión declarada (ver seccion 4,
      Impacto Constitucional).
    reinforcing_loop: |
      Cada vez que dos componentes vecinos declaran, cada uno por su cuenta, que una
      responsabilidad no les pertenece, aumenta el riesgo de que esa responsabilidad se quede sin
      dueño real más tiempo del necesario — porque cada declaración de exclusión se siente, por sí
      sola, como progreso, aunque ninguna instale el componente que falta. Este capítulo corta ese
      bucle instalando, por fin, el componente que dos capítulos distintos (CH-02 y CH-03) ya habían
      señalado desde direcciones opuestas.
    balancing_loop: |
      `resolveToolCall` (seccion 11) es el mecanismo de equilibrio: recorre el registro real de
      `CapabilityDescriptor`s y rechaza, con un `HarnessError` categorizado — nunca con una
      excepción sin tipar ni con una ejecución silenciosa de un nombre inexistente — tanto un
      `capabilityName` que no corresponde a ningún descriptor registrado como un `rawArguments` que
      no cumple el `inputSchema` declarado, antes de producir cualquier `ToolCall`.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `CapabilityRegistry` (CMP-008) resuelva
      el `capabilityName` de una `RawToolCallProposal` mediante una búsqueda real contra una lista
      de `CapabilityDescriptor` (C-018) — no mediante una señal booleana asumida, como
      `capabilityResolved` en CH-02 — y que el `ToolCall` (C-008) que produce tome su campo
      `capability` directamente del descriptor encontrado, nunca del texto libre que el modelo
      propuso. Si esta resolución siguiera siendo una señal asumida, el libro completo llegaría a
      un capítulo de integración final sin que ningún componente hubiera demostrado, con
      pseudocódigo real, cómo un nombre de texto libre se convierte en una acción ya resuelta y
      lista para pasar por policy y ejecución.
  recall_questions:
    - id: RQ-CH08-01
      text: |
        ¿Qué componente resuelve el `capabilityName` de una `RawToolCallProposal` (CH-03) contra un
        registro de capacidades, y qué contrato produce como resultado de esa resolución?
    - id: RQ-CH08-02
      text: |
        ¿Contra qué campo del descriptor registrado se valida `rawArguments`, y qué código de
        `HarnessError` se construye cuando esa validación falla?
    - id: RQ-CH08-03
      text: |
        ¿Qué dos capítulos anteriores señalaron, cada uno desde su propio `does_not_own`, la misma
        responsabilidad que este capítulo por fin ocupa con código real?
    - id: RQ-CH08-04
      text: |
        ¿Qué cinco campos tiene el descriptor registrado de una capability (C-018), y por qué
        incluye un campo de versión explícito en vez de dejarlo implícito?
  explain_prompts:
    - id: EP-CH08-01
      text: |
        `CapabilityRegistry` posee resolver qué implementación satisface una capacidad solicitada.
        Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee ejecutar esa
        capacidad una vez resuelta, aunque acaba de "encontrarla" — ¿qué se rompería, en concreto,
        si `CapabilityRegistry` empezara a ejecutar directamente la implementación que encontró, en
        vez de solo producir un `ToolCall` resuelto?
      target_entity: CMP-008
    - id: EP-CH08-02
      text: |
        `CapabilityDescriptor.implementationRef` es una referencia opaca a la implementación
        concreta, no el código de esa implementación. Explica qué perderíamos si
        `CapabilityRegistry`, en vez de guardar una referencia opaca, modelara el detalle interno de
        cada implementación dentro de su propio registro.
      target_entity: C-018
  interleaved_questions:
    - id: IQ-CH08-01
      text: |
        `ToolRuntime` (CH-02) declaró desde su propio capítulo que no le pertenece "el registro y la
        resolución de qué implementación satisface una capability solicitada", y `ToolCall` (C-008,
        CH-02) exige un campo `capability` ya resuelto antes de llegar a ejecutarse. ¿Qué construye
        este capítulo para que ese `ToolCall` deje de depender de una resolución externa asumida, y
        qué campo del descriptor registrado termina poblando exactamente el campo `capability` de
        ese `ToolCall`?
      current_chapter_entities: [CMP-008, C-018]
      prior_chapter_entities: [CMP-002, C-008]
      prior_chapter: CH-02
    - id: IQ-CH08-02
      text: |
        `ModelResponse` (C-007, CH-03) transporta `proposedToolCall` como una `RawToolCallProposal`
        deliberadamente cruda — solo `capabilityName` y `rawArguments`, sin resolver. ¿Qué hace este
        capítulo con esos dos campos exactos para producir, por primera vez, un `ToolCall` real, y
        por qué `ModelGateway` (CH-03) nunca podría haber hecho ese mismo trabajo él mismo?
      current_chapter_entities: [CMP-008, C-018]
      prior_chapter_entities: [CMP-003, C-007]
      prior_chapter: CH-03
  flashcards:
    - id: FC-CH08-01
      front: |
        ¿Qué posee `CapabilityRegistry` (Article III / Article IV), en una frase?
      back: |
        Registrar el descriptor de una capability (nombre, versión, schema de entrada,
        implementación), resolver el nombre de una propuesta cruda contra ese registro, validar sus
        argumentos contra el schema declarado y desacoplar la intención de una capacidad de su
        implementación concreta — cita literal de Article III.
      source_entity: CMP-008
      chapter_introduced_in: CH-08
      review_stage: DAY_1
    - id: FC-CH08-02
      front: |
        ¿Qué NO posee `CapabilityRegistry`, y a qué componentes pertenecen esas decisiones?
      back: |
        Ejecutar la capability ya resuelta (`ToolRuntime`, ya existente), invocar al modelo o
        interpretar su propuesta cruda (`ModelGateway`, ya existente), evaluar policy/autorización
        sobre si la acción ya resuelta debe ejecutarse (`PolicyEngine`, ya existente) y decidir
        continuación de turno (`AgentLoop`, ya existente).
      source_entity: CMP-008
      chapter_introduced_in: CH-08
      review_stage: DAY_1
    - id: FC-CH08-03
      front: |
        ¿Qué campos tiene `CapabilityDescriptor` (C-018), y qué representan?
      back: |
        `capability` (CapabilityId, el identificador ya resuelto), `name` (Text, el nombre canónico
        contra el que se compara `capabilityName`), `version` (Text, explícita — P-26), `inputSchema`
        (Value, contra el que se valida `rawArguments`) y `implementationRef` (Text, una referencia
        opaca a la implementación concreta, sin modelar su detalle).
      source_entity: C-018
      chapter_introduced_in: CH-08
      review_stage: DAY_1
    - id: FC-CH08-04
      front: |
        ¿Por qué `CapabilityDescriptor` incluye un campo `version` explícito?
      back: |
        Porque P-26 ("Capabilities have governed lifecycles") exige que tools/capabilities soporten
        versiones explícitas, compatibility policy, rollout, deprecation y retirement — este
        capítulo adopta el campo `version` como base mínima de ese principio, sin implementar
        todavía el resto del lifecycle (rollout/deprecation/retirement quedan fuera de alcance, ver
        seccion 18).
      source_entity: C-018
      chapter_introduced_in: CH-08
      review_stage: DAY_1
    - id: FC-CH08-05
      front: |
        ¿Qué produce este capítulo, por primera vez, que dos capítulos anteriores solo habían
        dejado declarado como pendiente?
      back: |
        Un `ToolCall` (C-008) real y válido, resuelto mediante una búsqueda real contra un registro
        de `CapabilityDescriptor` — no mediante una señal booleana asumida (`capabilityResolved` en
        CH-02) ni mediante una propuesta cruda sin resolver (`RawToolCallProposal` en CH-03).
      source_entity: CMP-008
      chapter_introduced_in: CH-08
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH08-01
      recall_question: RQ-CH08-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH08-02
      recall_question: RQ-CH08-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH08-03
      recall_question: RQ-CH08-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH08-04
      recall_question: RQ-CH08-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 8 — CapabilityRegistry y la Resolución Real de una Tool Call

> **Regla constitucional (Article III, sección "CapabilityRegistry"):** responsable de desacoplar
> la intención de una capacidad de su implementación concreta.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de saber
> cómo se llama el componente de este capítulo. El detalle estructurado de esta sección vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, dentro de la resolución de
una propuesta cruda de tool call, qué tramo le pertenece en exclusiva al componente que decide qué
implementación satisface una capacidad solicitada y qué tramos pertenecen a dominios distintos
(interpretar la respuesta del modelo, ejecutar la acción ya resuelta, autorizarla) — y podrás
diseñar, para cualquier nombre de capacidad y argumentos crudos, el mecanismo que los resuelve
hacia una intención de acción ya validada y lista para ejecutarse, sin que esa resolución decida
por sí sola si la acción está permitida.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e
introduce un contrato de datos nuevo (`CapabilityDescriptor`) y el octavo componente de runtime del
libro (`CapabilityRegistry`) — todavía sin explicarlos, solo como mapa. A diferencia de los siete
capítulos anteriores, este es el primero que **produce de verdad** un contrato que otro capítulo ya
había introducido (`ToolCall`, C-008, CH-02): no lo redefine, no le agrega campos — por fin lo
construye con una resolución real en vez de recibirlo ya armado desde una señal asumida.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar
atrás; están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este
capítulo va a definir):

1. Cuando el modelo propone usar una herramienta nombrándola solo por texto libre y con argumentos
   todavía sin resolver (ver capítulo sobre la invocación real del modelo), ¿quién decide qué
   implementación concreta corresponde a ese nombre, y qué necesita existir de antemano para que
   esa decisión sea posible?
2. Si esa propuesta llega con argumentos que no corresponden a lo que la implementación resuelta
   espera recibir, ¿en qué momento exacto del camino debe detectarse ese desajuste, y qué le
   impide a una intención de acción mal formada seguir avanzando hacia su ejecución?
3. Dos capítulos distintos ya dejaron marcada la misma frontera desde lados opuestos — uno diciendo
   "esto todavía no está resuelto, solo lo transporto" y otro diciendo "resolver esto no me
   corresponde a mí, solo ejecuto lo ya resuelto". ¿Qué necesita existir para que esa frontera
   compartida por fin tenga, en la práctica, quien la ocupe?
4. ¿Alcanza con verificar que exista una implementación para el nombre de capacidad solicitado, o
   hace falta además algo que describa qué versión de esa implementación es y qué forma de entrada
   espera recibir, antes de aceptar cualquier argumento que llegue junto al nombre?

## 1. Arquitectura Actual (Current Architecture)

CH-00..CH-07 dejaron instalados diecisiete contratos de datos y siete componentes de runtime.
Ningún componente de este libro, hasta este capítulo, ha resuelto jamás una capacidad por su
nombre: `ToolCall` (C-008, CH-02) declara `capability: CapabilityId` como un campo ya resuelto
desde su primera versión, pero `ToolRuntime.executeToolCall` (CH-02 §11) siempre recibió esa
resolución como una señal booleana externa (`capabilityResolved: Boolean`), nunca calculada de
verdad. `ModelResponse.proposedToolCall` (C-007, CH-03) transporta, desde su primera versión, una
`RawToolCallProposal` — `capabilityName: Text`, texto libre sin resolver — precisamente porque
`ModelGateway.invoke` (CH-03 §11) se negó, por diseño, a resolverla él mismo.

`CapabilityRegistry` es, con diferencia, el nombre más citado de todo el libro sin tener todavía
componente propio: aparece **treinta veces** a lo largo de CH-00..CH-07, veintiuna de ellas
concentradas casi por igual entre dos capítulos que lo señalan desde direcciones opuestas —
`ToolRuntime` (CH-02, doce menciones), cuyo propio `does_not_own` excluye explícitamente "registro
y resolución de qué implementación satisface una capability solicitada", y `ModelGateway` (CH-03,
nueve menciones), cuya sección 19 ("Siguiente Incremento") señaló textualmente que resolver
`proposedToolCall` hacia un `ToolCall` real "requiere `CapabilityRegistry`". `PolicyEngine` (CH-05)
y `ExecutionController` (CH-07) también lo citan como preview, en ambos casos para distinguir su
propia responsabilidad ("¿está permitido usarla?", "¿puede el run seguir?") de la que este capítulo
por fin ocupa ("¿qué implementación satisface el nombre solicitado?").

`constitution/ARCHITECTURE_CONSTITUTION.md` Article III describe `CapabilityRegistry`, desde su
primera versión, con una sola línea deliberadamente terser que la de cualquier otro componente:
"Responsable de desacoplar la intención de una capacidad de su implementación concreta." Article IV
le asigna, igual de terso, su fila de Decision Ownership: "`CapabilityRegistry` → What
implementation satisfies a requested capability?" Hasta este capítulo, ningún código de este libro
había respondido esa pregunta con algo más que una señal asumida.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas, la propuesta cruda de una tool call queda atrapada
entre dos capítulos que, cada uno por su cuenta, se negaron honestamente a resolverla:
`ModelGateway` porque resolverla invadiría la responsabilidad de validación que Article III asigna
a otro dominio (CH-03 §5/§15); `ToolRuntime` porque su propio `does_not_own` excluye explícitamente
esa resolución desde su primer capítulo (CH-02 §8). Ninguna de las dos exclusiones es un error —
ambas son exactamente la disciplina de *ownership* que este libro exige — pero, sin un tercer
componente que efectivamente ocupe esa responsabilidad, "¿este nombre de capacidad corresponde a
algo que existe?" y "¿con qué versión, y bajo qué forma de entrada?" no tienen ningún lugar real
donde resolverse.

Sin ese lugar, una implementación real tendría que inventar su propio mecanismo cada vez: alguna
confiaría ciegamente en el `capabilityName` que el modelo produjo, ejecutando cualquier texto como
si ya fuera una capacidad válida — exactamente lo que INV-03 y P-13 prohíben, porque convertiría al
modelo en una fuente de autorización de facto; otra validaría los argumentos de entrada con una
lógica distinta cada vez, sin ningún schema declarado contra el cual comparar; una tercera
mezclaría, en el mismo lugar donde se resuelve el nombre, la pregunta de si esa capacidad está
permitida para usarse ahora — confundiendo "¿existe e implementa correctamente esta capability?"
(este capítulo) con "¿está permitida su ejecución en este momento?" (`PolicyEngine`, ya resuelto
desde CH-05), aunque Article IV las asigna a filas distintas de su tabla.

Necesitamos que "¿qué implementación satisface el nombre de capacidad solicitado?" tenga, por fin,
un dueño único y nombrado — que registre explícitamente cada capacidad disponible con su versión y
su forma de entrada esperada, que resuelva un nombre de texto libre contra ese registro mediante un
mecanismo real (no una señal asumida), que valide los argumentos crudos contra la forma declarada
antes de producir cualquier intención de acción, y que produzca, por fin, un `ToolCall` (C-008)
real y válido a partir de una `RawToolCallProposal` (C-007) — sin decidir, en el mismo movimiento,
si esa acción ya resuelta está autorizada para ejecutarse.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los diecisiete contratos y los siete componentes que existen hasta este punto no bastan porque:

- `constitution/ARCHITECTURE_CONSTITUTION.md` Article VI dibuja el pipeline completo de ejecución
  como `Tool Intent → Resolve Capability → Validate Schema → beforeToolCall → Policy Evaluation →
  Authorization → Human Approval? → Execution Budget → Sandbox → Execute → afterToolCall →
  ToolResult → Observation` — los dos primeros pasos después de `Tool Intent`, literalmente
  llamados `Resolve Capability` y `Validate Schema`, son exactamente el tramo que
  `ToolRuntime.executeToolCall` (CH-02 §11) modeló con dos señales asumidas
  (`capabilityResolved`, `inputValid`) precisamente porque, cuando se escribió CH-02, ningún
  componente los producía todavía;
- `RawToolCallProposal.capabilityName` (CH-03) sigue siendo texto libre sin ninguna garantía de que
  corresponda a algo registrado — nada en el libro, hasta este capítulo, compara ese texto contra
  un conjunto real de capacidades conocidas;
- `ToolCall.capability` (C-008) exige un `CapabilityId` ya resuelto desde su primera versión (CH-02
  §6), pero ningún componente real de este libro ha construido jamás un `ToolCall` a partir de una
  propuesta cruda — todos los `ToolCall` que aparecieron en pseudocódigo hasta CH-07 llegaron ya
  armados, como parámetro de entrada asumido;
- no existe ningún contrato que registre, para una capacidad concreta, su versión explícita ni el
  schema de entrada contra el cual validar sus argumentos — `ToolRuntime` (CH-02 §5) ya nombró este
  hueco como "Schema Validation Gate", dejando deliberadamente sin resolver "qué es exactamente ese
  schema y cómo se declara";
- nada impide, todavía, que "el nombre de capacidad existe y su implementación es correcta" se
  confunda con "esa capacidad está permitida para usarse ahora" — dos preguntas que Article IV
  asigna, cada una, a un dueño distinto (`CapabilityRegistry` y `PolicyEngine`, respectivamente).

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la
> secuencia `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una
> entidad que no haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT`
> registrado — **no magic entities**. Este capítulo aplica la misma disciplina de *ownership* que
> CH-01..CH-07 ya establecieron, con una particularidad nueva: por primera vez, el pseudocódigo de
> este capítulo consume directamente un tipo embebido introducido por otro capítulo
> (`RawToolCallProposal`, embebido en `ModelResponse`, CH-03) — sin redefinirlo informalmente, solo
> referenciándolo por nombre, exactamente como esta misma sección exige para cualquier entidad ya
> definida.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-03   Tools are explicit capabilities, not prompt tricks.
           Primera vez que este principio se materializa por completo: la capacidad no solo se
           representa mediante un contrato explícito (ToolCall, CH-02) — ahora también se registra
           explícitamente, con nombre, versión y schema, en vez de depender de que el modelo
           "adivine" correctamente el nombre exacto de una función.
    P-13   Authorization is deterministic and external to the LLM.
           CapabilityRegistry no decide autorización: resuelve si el nombre de texto libre que el
           modelo propuso corresponde a algo registrado y si sus argumentos cumplen el schema
           declarado — ninguna de las dos verificaciones es una decisión de "¿está permitido?".
    P-26   Capabilities have governed lifecycles (Amendment v1.1).
           CapabilityDescriptor.version es la primera materialización, en este libro, de la
           exigencia de que las capabilities soporten versiones explícitas — sin implementar
           todavía compatibility policy, rollout, deprecation ni retirement (ver seccion 18).

Invariants preserved
    INV-03   El modelo nunca constituye una fuente de autorización.
             resolveToolCall (seccion 11) trata capabilityName como texto no confiable: lo compara
             contra un registro real en vez de asumir que corresponde a algo válido, y su
             resolución exitosa nunca equivale a una autorización (ver seccion 15).
    INV-04   Todo ToolCall debe validarse antes de ejecutarse.
             Primera materialización real de este invariante contra un schema real: resolveToolCall
             rechaza con un HarnessError cualquier rawArguments que no cumpla el inputSchema del
             CapabilityDescriptor resuelto, antes de construir el ToolCall.
    INV-05   Todo ToolCall pasa por ToolRuntime.
             Preservado, no reimplementado: este capítulo produce el ToolCall, nunca lo ejecuta —
             CapabilityRegistry.does_not_own excluye explícitamente la ejecución (ToolRuntime,
             CH-02, sigue siendo el único camino declarado para ejecutar una tool call).
    INV-18   Toda acción significativa produce un evento observable.
             resolveToolCall (seccion 11) emite un AgentEvent en cada resolución (éxito o fallo) —
             el octavo componente del libro que produce eventos en la práctica.
    INV-19   Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy relevante.
             Cada AgentEvent que emite CapabilityRegistry lleva el traceId de su ExecutionContext,
             y el ToolCall producido correlaciona, por su campo capability, con el
             CapabilityDescriptor exacto que lo resolvió.
    INV-20   Todo error operacional pertenece a una categoría conocida.
             CAPABILITY_NOT_FOUND y TOOL_INPUT_SCHEMA_MISMATCH reutilizan exactamente los mismos
             códigos y la misma categoría (VALIDATION) que ToolRuntime (CH-02) ya había declarado
             para las mismas señales, entonces asumidas — este capítulo es la primera vez que un
             componente real los produce de verdad.

Component ownership changes
    CMP-008 CapabilityRegistry se introduce — registry/components.yaml pasa de 7 a 8 componentes.
    owns/does_not_own citados literalmente contra Article III (sección "CapabilityRegistry") y
    Article IV. registry/components.yaml de CMP-001 AgentLoop, CMP-002 ToolRuntime, CMP-003
    ModelGateway y CMP-005 PolicyEngine NO se modifica: sus exclusiones ya quedaron declaradas
    desde sus propios capítulos; este capítulo solo instala, por fin, el componente al que
    apuntaban.

Lifecycle changes
    Ninguno sobre AgentRunStatus (C-013): sigue siendo propiedad exclusiva de AgentLoop (CH-01).
    ToolCall (C-008) y ToolResult (C-009) tampoco cambian de forma — su STRUCT sigue siendo
    exactamente el de CH-02; este capítulo cambia CÓMO se produce un ToolCall (con una resolución
    real en vez de una señal asumida), nunca su forma.

Security implications
    Este es el primer capítulo que materializa, con código real, los dos primeros pasos del
    pipeline de Article VI ("Resolve Capability" y "Validate Schema"). Ver seccion 15 para el
    análisis completo, incluyendo por qué una resolución exitosa nunca implica autorización.

Observability implications
    CapabilityRegistry es el octavo componente que emite AgentEvent en la práctica, extendiendo
    AgentEventType con dos valores nuevos (CAPABILITY_RESOLVED, CAPABILITY_RESOLUTION_FAILED) sin
    modificar el envelope AgentEvent (C-010) ni su STRUCT.

Deterministic vs agentic boundary
    Article XII se refina una octava vez a nivel de componente: CapabilityRegistry, igual que
    PolicyEngine y ExecutionController, no interpreta la intención del modelo — solo compara,
    determinísticamente, el texto que el modelo produjo contra un registro que el harness controla
    por completo. El modelo puede proponer cualquier capabilityName; CapabilityRegistry nunca le
    otorga el beneficio de la duda.
```

## 5. Conceptos Nuevos (New Concepts)

- **Capability Resolution**: el tramo determinístico, exigido por Article VI ("Resolve Capability"
  → "Validate Schema"), en el que se compara el `capabilityName` de una `RawToolCallProposal`
  contra un registro real de capacidades conocidas y se valida `rawArguments` contra la forma de
  entrada que esa capacidad declara — respondiendo, por primera vez con código real, la pregunta de
  Article IV: "`CapabilityRegistry` → What implementation satisfies a requested capability?".
- **Capability Descriptor**: el registro nombrado de una capability — su nombre canónico, su
  versión explícita, el schema de entrada contra el que se valida y una referencia opaca a su
  implementación concreta. Modelado como el contrato `CapabilityDescriptor` (C-018, seccion 7) —
  deliberadamente una referencia, nunca el detalle de la implementación misma (ver seccion 8, nota
  sobre `implementationRef`).
- **Capability Versioning** *(P-26, Amendment v1.1 — "Capabilities have governed lifecycles")*: la
  exigencia de que una capability declare una versión explícita, en vez de depender de que su
  nombre por sí solo identifique de forma estable qué implementación exacta responde. Este capítulo
  adopta el campo `version` como base mínima de ese principio — compatibility policy, rollout,
  deprecation y retirement quedan fuera de alcance (ver seccion 18).
- **Schema Validation Gate** *(nombrado por CH-02 §5 como preview, resuelto aquí)*: CH-02 dejó
  explícitamente sin resolver "qué es exactamente ese schema y cómo se declara". Este capítulo
  responde la primera mitad — el schema vive como `CapabilityDescriptor.inputSchema` — pero el
  mecanismo real de comparación entre ese schema y `rawArguments` (un algoritmo de validación de
  esquemas) sigue siendo, deliberadamente, una señal de entrada asumida (`argumentsMatchSchema`,
  seccion 11) — el mismo patrón que CH-02 ya usó para `inputValid`.
- **Decision Ownership** *(Article IV, en uso desde CH-01, ahora aplicado a un octavo componente)*:
  `CapabilityRegistry` decide "¿qué implementación satisface el nombre de capacidad solicitado?";
  explícitamente NO decide "¿cómo se ejecuta una acción ya resuelta?" (`ToolRuntime`, ya resuelto),
  "¿cómo se invoca al modelo o se interpreta su propuesta cruda?" (`ModelGateway`, ya resuelto),
  "¿está permitida esta acción ya resuelta?" (`PolicyEngine`, ya resuelto) ni "¿debe ocurrir otro
  turno?" (`AgentLoop`, ya resuelto).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados de CH-00/CH-02/CH-03

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `AgentId`, `CapabilityId`, `ToolCallId`, `Timestamp`,
`ExecutionContext`, `ToolCall`, `ModelResponse`, `AgentEvent`, `HarnessError`.

`RawToolCallProposal` merece una mención aparte: es un `STRUCT` embebido dentro de `ModelResponse`
(C-007, CH-03), sin contrato `C-XXX` propio — este capítulo es el primero del libro que lo
consume, por nombre, fuera del capítulo que lo introdujo, exactamente el tipo de referencia que
`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §2 permite ("no magic entities" exige que una
entidad esté *definida*, no que se redefina en cada capítulo que la usa):

| Identificador | Origen y forma |
|---|---|
| `RawToolCallProposal` | `STRUCT` embebido en `ModelResponse` (C-007, CH-03): `capabilityName: Text`, `rawArguments: Map<Text, Value>` — la propuesta cruda que este capítulo, por primera vez, resuelve. |

### `AgentEventType` — extendido, sin redefinir `AgentEvent`

CH-07 extendió `AgentEventType` a catorce valores. Este capítulo agrega dos valores — los primeros
eventos que observan la resolución de una capacidad, no su ejecución, su invocación al modelo, su
autorización ni la continuación operacional del run:

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
END
```

`AgentEvent` (C-010) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — solo el rango de
valores permitido para `eventType` crece, igual que en cada capítulo anterior.

### `CapabilityDescriptor` — el descriptor registrado de una capability

```pseudocode
STRUCT CapabilityDescriptor
    capability: CapabilityId
    name: Text
    version: Text
    inputSchema: Value
    implementationRef: Text
END
```

Cinco campos, cada uno respondiendo a una parte exacta del alcance decidido para este capítulo:
`capability` es el identificador ya resuelto que este descriptor produce — el mismo tipo que
`ToolCall.capability` (C-008, CH-02) ya exige desde su primera versión; `name` es el nombre
canónico contra el que se compara `RawToolCallProposal.capabilityName` (texto libre, sin garantía
de formato); `version` es una versión explícita (Text, p. ej. `"1.2.0"`) — la materialización
mínima de P-26 (Amendment v1.1, "Capabilities have governed lifecycles") que este capítulo adopta,
sin implementar compatibility policy, rollout, deprecation ni retirement (ver seccion 18);
`inputSchema` es la forma de entrada esperada, contra la cual se valida `rawArguments` — modelada
como `Value` porque este libro no define todavía un lenguaje de schema propio (el mecanismo real de
comparación sigue siendo una señal asumida, ver seccion 11); `implementationRef` es,
deliberadamente, una referencia opaca (Text) a la implementación concreta — nunca el código de esa
implementación ni su detalle interno, que queda fuera de alcance de este capítulo (Article III
distingue "la intención de una capacidad" de "su implementación concreta"; modelar esa
implementación en detalle sería cruzar exactamente esa línea).

**Unchanged / Not yet introduced**: `ToolCall` (C-008) y `ToolResult` (C-009) no cambian de forma —
siguen siendo exactamente los `STRUCT` de CH-02. Este capítulo tampoco introduce ningún `STRUCT`
para representar el mecanismo de *registro* de una capability (no hay
`CapabilityRegistrationRequest` ni equivalente): el conjunto de `CapabilityDescriptor` ya
registrados llega, a `resolveToolCall` (seccion 11), como parámetro ya poblado — una primitiva
asumida, en el mismo espíritu que `ExecutionUsage` (CH-07) o `policyRuleFound(...)` (CH-05) — el
mecanismo real de alta/baja de capabilities queda, deliberadamente, fuera de alcance (ver
seccion 18).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce un contrato de
datos, registrado en `registry/contracts.yaml`:

```text
ID:                     C-018
Name:                   CapabilityDescriptor
Version:                v1
Introduced In:          CH-08
Current Definition:     STRUCT CapabilityDescriptor (ver §6)
Used By:                [CMP-008]
Modified By:            []
Constitutional Impact:  [P-03, P-26, INV-04, INV-20]
```

`C-018` es el quinto id verdaderamente nuevo del libro (el correlativo continúa después de `C-017`,
CH-07 — ningún id quedaba reservado desde CH-01 §7, exactamente como ya ocurrió con `C-014`..`C-017`
en CH-05/CH-06/CH-07). El nombre `CapabilityDescriptor`, y no `Capability` a secas, es deliberado:
"Capability" (sin sufijo) ya es un término de glosario desde CH-02, referido a la abstracción
conceptual que desacopla intención de implementación (Article III) — `CapabilityDescriptor` es,
específicamente, el registro de datos concreto que representa esa abstracción dentro del runtime,
la misma disciplina de nombres que distingue "Tool Call" (el concepto, CH-02) de `ToolCall` (el
contrato, C-008).

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el octavo componente de runtime del libro:

```pseudocode
COMPONENT CapabilityRegistry
    consumes: ExecutionContext, ModelResponse
    produces: ToolCall, AgentEvent, HarnessError, CapabilityDescriptor
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Article III (sección "CapabilityRegistry") y Article
IV:

```text
COMPONENT: CapabilityRegistry

Responsibility:
    Registrar las capabilities disponibles junto con su descriptor (nombre canónico, versión,
    schema de entrada esperado y una referencia opaca a su implementación concreta), resolver el
    capabilityName de una RawToolCallProposal contra ese registro, validar sus rawArguments contra
    el schema declarado y producir un ToolCall resuelto — sin ejecutar la capability, sin invocar
    al modelo ni interpretar su propuesta cruda, sin evaluar policy/autorización y sin decidir
    continuación de turno.

Consumes:
    C-004 ExecutionContext, C-007 ModelResponse (para leer proposedToolCall)

Depends on:
    (ninguno todavía — el cableado real con AgentLoop, ModelGateway, PolicyEngine y ToolRuntime es
    Preview, no introducido en este capítulo; ver seccion 9)

Produces:
    C-008 ToolCall (primera vez que este contrato se produce con una resolución real, no como
    parámetro ya armado), C-010 AgentEvent (CAPABILITY_RESOLVED / CAPABILITY_RESOLUTION_FAILED),
    C-011 HarnessError (embebido en una resolución fallida), C-018 CapabilityDescriptor (el
    descriptor registrado que este componente posee)

Owns (Article III, cita literal, expandida contra cómo CH-02/CH-03 ya la citaron):
    - registrar el descriptor de una capability disponible (nombre, versión, schema de entrada,
      referencia de implementación)
    - resolver qué implementación satisface una capability solicitada (cita literal de CH-02
      does_not_own: "registro y resolución de qué implementación satisface una capability
      solicitada")
    - validar los argumentos crudos de una propuesta contra el schema declarado por la capability
      resuelta
    - desacoplar la intención de una capacidad de su implementación concreta (cita literal de
      Article III)

Does NOT own (Article IV — declarado con el mismo peso que Owns):
    - ejecutar la capability ya resuelta (ToolRuntime, CMP-002, ya introducido en CH-02 — Article
      IV: "ToolRuntime → How should an approved action be executed?"; CH-02 ya marcó esta frontera
      exacta desde su propio does_not_own)
    - invocar al modelo seleccionado o interpretar su propuesta cruda antes de que llegue como
      ModelResponse (ModelGateway, CMP-003, ya introducido en CH-03 — Article IV: "ModelGateway →
      How should the selected model be invoked?"; CH-03 §18/§19 ya dejó explícito que resolver
      proposedToolCall hacia un ToolCall real es trabajo de CapabilityRegistry, no de ModelGateway)
    - evaluar policy/autorización sobre si la acción ya resuelta debe ejecutarse (PolicyEngine,
      CMP-005, ya introducido en CH-05 — distinción cuidadosa: "¿existe e implementa correctamente
      esta capability?" es de CapabilityRegistry; "¿está permitido usarla ahora?" es de
      PolicyEngine; ninguna de las dos preguntas sustituye a la otra)
    - decidir si otro turno de razonamiento debe ocurrir (AgentLoop, CMP-001, ya introducido en
      CH-01)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con una
particularidad respecto a CH-01..CH-07: dos de las cuatro exclusiones de esta lista
(`ToolRuntime`, `ModelGateway`) no son fronteras nuevas que este capítulo inventa, sino la
confirmación textual, con código real, de fronteras que esos dos capítulos ya habían declarado
desde el lado opuesto — la primera vez que este libro cierra un círculo de `does_not_own` cruzados
entre dos componentes que ya existían antes de que el componente que ambos señalaban existiera.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
CapabilityRegistry
    consumes → ExecutionContext, ModelResponse
    produces → ToolCall, AgentEvent, HarnessError, CapabilityDescriptor
    depends on (componentes) → (ninguno registrado todavía)
```

`CapabilityRegistry` no depende hoy de ningún otro componente registrado — mismo patrón que
CH-01..CH-07 ya establecieron para sus propios componentes. En prosa (nunca dentro de un bloque
`pseudocode`, per `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las relaciones
futuras que un capítulo de integración agregaría son:

| Componente futuro (relación inversa — no cableada en este capítulo) | Qué relación tendría con `CapabilityRegistry` |
|---|---|
| `ModelGateway` (ya existente, CMP-003) | produciría el `ModelResponse` cuyo `proposedToolCall` este componente resuelve — hoy `resolveModelProposedToolCall` (seccion 11) recibe ese `ModelResponse` ya armado, como demostración autónoma |
| `PolicyEngine` (ya existente, CMP-005) | evaluaría el `ToolCall` que este componente produce, **antes** de que `ToolRuntime` lo ejecute — la resolución de este capítulo nunca implica autorización (ver seccion 15) |
| `ToolRuntime` (ya existente, CMP-002) | ejecutaría el `ToolCall` ya resuelto por este componente, una vez que `PolicyEngine` lo autorice |
| `AgentLoop` (ya existente, CMP-001) | invocaría, en algún punto del turno, la resolución de este componente antes de que `ToolRuntime` reciba el `ToolCall` resultante |

`registry/components.yaml` de `CMP-001` (`AgentLoop`), `CMP-002` (`ToolRuntime`) y `CMP-003`
(`ModelGateway`) **no se modifica** en este capítulo: ninguno de los tres agrega `CMP-008` a su
`dependencies`, y ninguno cambia su pseudocódigo. El pseudocódigo de la seccion 11 muestra a
`CapabilityRegistry` resolviendo, de forma completamente autónoma, un `ModelResponse` de ejemplo
contra un registro de `CapabilityDescriptor` de ejemplo — sin que `ModelGateway`, `PolicyEngine` ni
`ToolRuntime` cambien una sola línea para que este capítulo sea correcto. El cableado real de punta
a punta (`AgentLoop → ModelGateway → CapabilityRegistry → PolicyEngine → ToolRuntime` como un solo
flujo) es, explícitamente, trabajo de un capítulo de integración futuro (ver seccion 18/19) — el
mismo patrón que CH-02..CH-07 ya establecieron para sus propias relaciones inversas.

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[ModelGateway — produce ModelResponse, CH-03, conceptual] → CapabilityRegistry →
[PolicyEngine — evaluaría el ToolCall resuelto, CH-05, conceptual] → [ToolRuntime — ejecutaría el
ToolCall ya autorizado, CH-02, conceptual]
```

**Vista 2 — Sequence**

```text
ModelResponse
   │ (proposedToolCall: RawToolCallProposal, ya producido por ModelGateway — CH-03, conceptual)
   ▼
CapabilityRegistry
   │ resolveModelProposedToolCall(response, registeredCapabilities, execution, agentId,
   │                              argumentsMatchSchema)
   │ ¿response.proposedToolCall == NULL?
   │     sí → HarnessError (RESOLUTION_REQUESTED_WITHOUT_PROPOSAL, VALIDATION)
   │ busca, dentro de registeredCapabilities, un CapabilityDescriptor cuyo name coincida con
   │ proposedToolCall.capabilityName
   │     no encontrado → HarnessError (CAPABILITY_NOT_FOUND, VALIDATION)
   │     encontrado, argumentsMatchSchema = FALSE → HarnessError (TOOL_INPUT_SCHEMA_MISMATCH,
   │       VALIDATION)
   │     encontrado, argumentsMatchSchema = TRUE → construye ToolCall (capability tomado del
   │       descriptor resuelto)
   │ emite: AgentEvent (CAPABILITY_RESOLVED | CAPABILITY_RESOLUTION_FAILED)
   ▼
ToolCall
   │
   ▼
[PolicyEngine evaluaría este ToolCall antes de que ToolRuntime lo ejecute — Preview, cableado
formal de un capítulo de integración futuro, ver seccion 9/18]
```

**Vista 3 — Pseudocódigo**

Ver §11: `resolveToolCall` es la primera formalización ejecutable de "`CapabilityRegistry` decide
qué implementación satisface una capacidad solicitada"; `resolveModelProposedToolCall` es la
primera vez que el libro muestra, con pseudocódigo real, el tramo completo que toma un
`ModelResponse` (CH-03) y produce un `ToolCall` (CH-02) — dos contratos de dos capítulos distintos,
conectados por primera vez por un tercero.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde
CH-00/CH-02/CH-03.

```pseudocode
FUNCTION resolveToolCall(
    proposal: RawToolCallProposal,
    registeredCapabilities: List<CapabilityDescriptor>,
    execution: ExecutionContext,
    agentId: AgentId,
    argumentsMatchSchema: Boolean
) -> ToolCall

    descriptor: Optional<CapabilityDescriptor> = NULL

    FOR EACH candidate IN registeredCapabilities
        IF candidate.name == proposal.capabilityName
            descriptor = candidate
        END
    END

    IF descriptor == NULL
        failure: HarnessError = HarnessError(
            category = VALIDATION,
            code = "CAPABILITY_NOT_FOUND",
            message = "CapabilityRegistry no encontró ningún CapabilityDescriptor registrado para este capabilityName",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )

        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = CAPABILITY_RESOLUTION_FAILED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = failure
        )

        THROW failure
    END

    IF NOT argumentsMatchSchema
        failure: HarnessError = HarnessError(
            category = VALIDATION,
            code = "TOOL_INPUT_SCHEMA_MISMATCH",
            message = "rawArguments no cumple el inputSchema declarado por el CapabilityDescriptor resuelto",
            recoverable = TRUE,
            retryable = FALSE,
            metadata = {}
        )

        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = CAPABILITY_RESOLUTION_FAILED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = failure
        )

        THROW failure
    END

    call: ToolCall = ToolCall(
        id = newToolCallId(),
        capability = descriptor.capability,
        arguments = proposal.rawArguments,
        requestedAt = now()
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = CAPABILITY_RESOLVED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = call
    )

    RETURN call
END
```

`newEventId()` y `now()` son las mismas primitivas de CH-00..CH-07. `newToolCallId()` es una
primitiva nueva, en el mismo espíritu que `newHumanInteractionRequestId()` (CH-06): genera un
`ToolCallId` nuevo — no es una entidad arquitectónica ni un componente, no requiere ficha ni
registro. `registeredCapabilities` es una señal de entrada asumida — el conjunto de
`CapabilityDescriptor` ya registrados llega como parámetro ya poblado (seccion 6/18): este capítulo
modela la **resolución** contra ese registro (el `FOR EACH` que compara `candidate.name` con
`proposal.capabilityName`, real y ejecutable), no el **mecanismo de alta** que lo puebla.
`argumentsMatchSchema` es, igual que `inputValid` en CH-02 §11, una señal de entrada asumida: el
algoritmo real que compararía `proposal.rawArguments` contra `descriptor.inputSchema` (un motor de
validación de esquemas) queda fuera de alcance de este capítulo (ver seccion 18) — la diferencia
respecto a CH-02 es que ahora existe un campo real (`inputSchema`) contra el cual ese algoritmo,
cuando exista, compararía.

Por primera vez en el libro, con `ModelGateway` (CMP-003, CH-03) y `CapabilityRegistry` (CMP-008,
recién definido) ya existentes, se puede mostrar el tramo completo que toma un `ModelResponse` y
produce un `ToolCall` con pseudocódigo real:

```pseudocode
FUNCTION resolveModelProposedToolCall(
    response: ModelResponse,
    registeredCapabilities: List<CapabilityDescriptor>,
    execution: ExecutionContext,
    agentId: AgentId,
    argumentsMatchSchema: Boolean
) -> ToolCall

    IF response.proposedToolCall == NULL
        failure: HarnessError = HarnessError(
            category = VALIDATION,
            code = "RESOLUTION_REQUESTED_WITHOUT_PROPOSAL",
            message = "resolveModelProposedToolCall fue invocada sobre un ModelResponse sin proposedToolCall",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        THROW failure
    END

    call: ToolCall = resolveToolCall(
        response.proposedToolCall,
        registeredCapabilities,
        execution,
        agentId,
        argumentsMatchSchema
    )

    RETURN call
END
```

`resolveModelProposedToolCall` es una demostración de integración, no una tercera responsabilidad
nueva: no es un método registrado de ninguna ficha de componente adicional
(`CapabilityRegistry.consumes`/`.produces` ya quedaron declarados en la seccion 8 sin este nombre),
y **no** modifica `CMP-003 ModelGateway` — ni su ficha, ni sus `consumes`/`produces`/`dependencies`
en `registry/components.yaml`, ni la firma de `invoke` (CH-03 §11), que sigue devolviendo
exactamente el mismo `ModelResponse` que devolvía antes de este capítulo. Muestra únicamente que,
con `ModelGateway` y `CapabilityRegistry` ya existentes, es posible tomar un `ModelResponse` real
(con su `proposedToolCall` sin resolver) y obtener de vuelta un `ToolCall` real — el cableado formal
que haría que `AgentLoop` invoque esta resolución dentro del ciclo de un turno sigue siendo,
explícitamente, trabajo de un capítulo posterior (ver seccion 9/18/19).

Nótese lo que ni `resolveToolCall` ni `resolveModelProposedToolCall` hacen: no ejecutan ningún
`ToolRuntime.execute(...)` real (Article IV, "`ToolRuntime` → How should an approved action be
executed?" sigue sin respuesta aquí), no evalúan ninguna policy sobre el `ToolCall` que acaban de
producir (P-13, "`PolicyEngine` → May this action occur?" sigue sin respuesta aquí), y no deciden
ningún `AgentRunStatus` ni continuación de turno (Article IV, "`AgentLoop` → Should another
reasoning turn occur?" sigue sin respuesta aquí).

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013): esa máquina de estados sigue
siendo propiedad exclusiva de `AgentLoop` (CH-01 §12), y su tabla de transiciones no cambia aquí.
`ToolCall` (C-008) tampoco tiene, ni tuvo nunca, un campo de estado propio — sigue siendo, como en
CH-02, una intención ya resuelta y todavía sin ejecutar.

`resolveToolCall` (§11) sí atraviesa un camino implícito con tres desenlaces — pero deliberadamente
**no** se formaliza como un nuevo contrato de lifecycle en este capítulo (eso introduciría una
segunda entidad nueva, fuera del alcance decidido para este capítulo):

```text
RawToolCallProposal recibida
   → capabilityName sin descriptor registrado    → HarnessError (CAPABILITY_NOT_FOUND)
   → rawArguments no cumple el inputSchema        → HarnessError (TOOL_INPUT_SCHEMA_MISMATCH)
     del descriptor resuelto
   → descriptor encontrado, argumentos válidos    → ToolCall (capability = descriptor.capability)
```

**Lo que este capítulo explícitamente no cierra**: `ToolRuntime.executeToolCall` (CH-02 §11) sigue
recibiendo `capabilityResolved`/`inputValid` como señales de entrada asumidas — este capítulo
produce, por fin, la pieza real que llenaría esas dos señales, pero conectar formalmente ambos
capítulos (que `executeToolCall` reciba un `ToolCall` ya producido por `resolveToolCall`, en vez de
dos booleanos sueltos) sigue siendo, explícitamente, trabajo de un capítulo posterior (ver seccion
18/19); `book/chapters/02-tool-runtime/chapter.md` no se modifica para reflejarlo todavía.

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6) clasifica también los fallos que introduce este capítulo,
fiel a los `Failure Examples` de `constitution/ARCHITECTURE_CONSTITUTION.md` Article VII:

```text
VALIDATION
    RESOLUTION_REQUESTED_WITHOUT_PROPOSAL  — resolveModelProposedToolCall invocada sobre un
                                              ModelResponse sin proposedToolCall (precondición de
                                              invocación, no un fallo de resolución en sí)
        → recoverable: FALSE, retryable: FALSE
    CAPABILITY_NOT_FOUND                   — ningún CapabilityDescriptor registrado corresponde al
                                              capabilityName solicitado ("Invalid tool arguments →
                                              validation", familia de Article VII)
        → recoverable: FALSE, retryable: FALSE
    TOOL_INPUT_SCHEMA_MISMATCH             — rawArguments no cumple el inputSchema del descriptor
                                              resuelto
        → recoverable: TRUE, retryable: FALSE
```

`CAPABILITY_NOT_FOUND` y `TOOL_INPUT_SCHEMA_MISMATCH` reutilizan, deliberadamente, los mismos
códigos y la misma categoría (`VALIDATION`) que `ToolRuntime.executeToolCall` (CH-02 §13) ya había
declarado para las mismas señales, entonces asumidas (`capabilityResolved`, `inputValid`) — este
capítulo evaluó explícitamente si `VALIDATION` seguía siendo la categoría correcta para un fallo de
resolución de capacidades (frente a introducir una categoría `CAPABILITY` nueva) y concluyó que sí:
`ErrorCategory` (CH-00 §6) ya distingue `VALIDATION` (un dato de entrada no cumple una forma
esperada) de `TOOL` (una capability ya resuelta falla durante su ejecución, CH-02) — un
`capabilityName` inexistente o unos `rawArguments` mal formados son, ambos, fallos de validación de
la *entrada*, no fallos de la *ejecución*; introducir una categoría nueva solo para distinguir
"quién" detectó el problema (`CapabilityRegistry` en vez de `ToolRuntime`) fragmentaría
`ErrorCategory` sin ganancia semántica real, y rompería la continuidad exacta que este capítulo
busca con CH-02.

`resolveToolCall`/`resolveModelProposedToolCall` nunca devuelven una excepción cruda ni un
`ToolCall` a medias cuando la resolución falla: siempre construyen un `HarnessError` con
`category`, `recoverable` y `retryable` explícitos — mismo patrón que cada función de CH-00..CH-07.
A diferencia de la precondición de invocación (`RESOLUTION_REQUESTED_WITHOUT_PROPOSAL`, que
interrumpe la función con `THROW` sin `EMIT` — mismo patrón que
`EXECUTION_EVALUATION_ON_TERMINAL_STATE`, CH-07), los casos `CAPABILITY_NOT_FOUND`/
`TOOL_INPUT_SCHEMA_MISMATCH` sí emiten un `AgentEvent` antes de lanzar el error: son resultados de
una resolución que sí llegó a ejecutarse, no violaciones de una precondición de invocación.

## 14. Eventos Producidos (Events Produced)

Este capítulo agrega dos valores a `AgentEventType` (seccion 6) — los primeros que observan la
resolución de una capacidad, no su ejecución, su invocación al modelo, su autorización ni la
continuación operacional del run:

```text
CAPABILITY_RESOLVED             — CapabilityRegistry encontró un CapabilityDescriptor para el
                                   capabilityName solicitado y sus rawArguments cumplen el
                                   inputSchema declarado (resolveToolCall, §11)
CAPABILITY_RESOLUTION_FAILED    — CapabilityRegistry no pudo resolver la propuesta: el
                                   capabilityName no corresponde a ningún descriptor registrado, o
                                   sus argumentos no cumplen el schema (resolveToolCall, §11)
```

`RESOLUTION_REQUESTED_WITHOUT_PROPOSAL` no emite ningún `AgentEvent` — mismo patrón que
`TURN_ON_TERMINAL_STATE` (CH-01) y `EXECUTION_EVALUATION_ON_TERMINAL_STATE` (CH-07): el `THROW`
interrumpe la función antes de llegar al `EMIT`, porque es una violación de precondición de
invocación, no un resultado legítimo de la resolución en sí. `TOOL_CALL_COMPLETED`/
`TOOL_CALL_FAILED` (CH-02), `MODEL_RESPONSE_RECEIVED`/`MODEL_INVOCATION_FAILED` (CH-03),
`POLICY_EVALUATED` (CH-05) y `EXECUTION_EVALUATED` (CH-07) no se emiten desde `resolveToolCall`:
pertenecen a dominios distintos — ejecución, invocación del modelo, autorización y continuación
operacional, respectivamente — no a la resolución de una capacidad.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

Este capítulo materializa, por primera vez con código real, los dos primeros pasos del pipeline
completo de Article VI (`Tool Intent → Resolve Capability → Validate Schema → beforeToolCall →
Policy Evaluation → Authorization → Human Approval? → Execution Budget → Sandbox → Execute →
afterToolCall → ToolResult → Observation`):

- **`Resolve Capability`**: `resolveToolCall` (§11) compara `capabilityName` contra un registro
  real de `CapabilityDescriptor` — ya no una señal asumida (`capabilityResolved`, CH-02).
- **`Validate Schema`**: `resolveToolCall` rechaza cualquier `rawArguments` que no cumpla
  `descriptor.inputSchema` — ya no una señal asumida (`inputValid`, CH-02), aunque el algoritmo de
  comparación en sí sigue siendo una señal asumida (`argumentsMatchSchema`, ver seccion 11/18).

Los tramos que este capítulo **no** implementa, y que `CapabilityRegistry.does_not_own` declara
explícitamente:

- **`beforeToolCall` en adelante**: `ToolRuntime` (CH-02) sigue siendo el único componente que
  ejecuta hooks de extensión y coordina la ejecución real — este capítulo produce el `ToolCall` de
  entrada a ese tramo, nunca participa en él.
- **`Policy Evaluation` / `Authorization`** (P-05, P-13): una resolución exitosa
  (`CAPABILITY_RESOLVED`) significa, exclusivamente, "este nombre corresponde a una implementación
  registrada y estos argumentos cumplen su forma esperada" — **nunca** "esta acción está permitida
  para ejecutarse ahora". `PolicyEngine` (CH-05) sigue siendo el único componente que evalúa esa
  pregunta distinta, y sigue evaluándola **después** de que este capítulo resuelva el `ToolCall`,
  nunca antes ni en su lugar. Confundir ambas preguntas sería exactamente el error que Article IV
  prohíbe: "¿existe e implementa correctamente esta capability?" (`CapabilityRegistry`) y "¿está
  permitido usarla ahora?" (`PolicyEngine`) son dos filas distintas de la misma tabla.
- **`Human Approval?` / `Execution Budget` / `Sandbox`**: `HumanInteractionService` (CH-06) y
  `ExecutionController` (CH-07) siguen siendo, cada uno, el único componente responsable de su
  propio tramo — ninguno de los dos participa en la resolución de capacidades.
- **INV-03 (el modelo nunca constituye una fuente de autorización)**: `capabilityName` es texto que
  el modelo produjo — `resolveToolCall` nunca le otorga el beneficio de la duda: si no corresponde
  a ningún `CapabilityDescriptor` registrado, la resolución falla, sin importar cuán plausible
  parezca el nombre propuesto.

`ToolCall` es, por diseño, la forma en que `CapabilityRegistry` comunica que una propuesta cruda
corresponde a algo real y bien formado — nunca una afirmación de que esa acción ya puede
ejecutarse.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST ResolveToolCallNeverProducesAToolCallForAnUnregisteredCapabilityName
TEST ResolveToolCallNeverProducesAToolCallWhenArgumentsDoNotMatchSchema
TEST ResolveToolCallAlwaysTakesToolCallCapabilityFromTheResolvedDescriptorNeverFromRawInput
TEST ResolveToolCallNeverInvokesToolRuntimeModelGatewayOrPolicyEngineDirectly
TEST ResolveToolCallAlwaysEmitsAnAgentEventOnResolutionOrFailure
TEST CapabilityResolutionSuccessNeverImpliesAuthorization
TEST ResolveModelProposedToolCallNeverModifiesModelGatewayOrItsRegistryEntry
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.1, después de CH-08)

Constitution
 ├── Article III  — Component Sovereignty (CapabilityRegistry: octavo componente instanciado)
 ├── Article IV   — Decision Ownership (en uso: CapabilityRegistry.owns/does_not_own)
 └── Article VI   — Execution Constitution (Resolve Capability / Validate Schema materializados
                     por primera vez con código real; beforeToolCall en adelante sigue sin cambios)

Contracts (registry/contracts.yaml)
 ├── C-001 AgentMessage                (CH-00)
 ├── C-002 AgentConfig                 (CH-00)
 ├── C-003 AgentState                  (CH-00)
 ├── C-004 ExecutionContext            (CH-00)
 ├── C-005 ContextSnapshot             (CH-04)
 ├── C-006 ModelRequest                (CH-03)
 ├── C-007 ModelResponse               (CH-03)
 ├── C-008 ToolCall                    (CH-02 — producido con resolución real desde CH-08)
 ├── C-009 ToolResult                  (CH-02)
 ├── C-010 AgentEvent                  (CH-00)
 ├── C-011 HarnessError                (CH-00)
 ├── C-012 ExecutionBudget             (CH-00)
 ├── C-013 AgentRunStatus              (CH-01)
 ├── C-014 PolicyDecision              (CH-05)
 ├── C-015 HumanInteractionRequest     (CH-06)
 ├── C-016 HumanInteractionResolution  (CH-06)
 ├── C-017 ExecutionDecision           (CH-07)
 └── C-018 CapabilityDescriptor        (CH-08, nuevo)

Components (registry/components.yaml)
 ├── CMP-001 AgentLoop                 (CH-01)
 ├── CMP-002 ToolRuntime               (CH-02)
 ├── CMP-003 ModelGateway              (CH-03)
 ├── CMP-004 ContextEngine             (CH-04)
 ├── CMP-005 PolicyEngine              (CH-05)
 ├── CMP-006 HumanInteractionService   (CH-06)
 ├── CMP-007 ExecutionController       (CH-07)
 └── CMP-008 CapabilityRegistry        (CH-08, nuevo — octavo componente, primero en producir de
                                         verdad un contrato introducido por otro capítulo, C-008)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El pipeline de integración completo `AgentLoop → ModelGateway → CapabilityRegistry →
  PolicyEngine → ToolRuntime`**: `resolveModelProposedToolCall` (§11) es una demostración autónoma,
  no una modificación real de `AgentLoop.runTurn` (CH-01), `ModelGateway.invoke` (CH-03),
  `PolicyEngine.evaluate` (CH-05) ni `ToolRuntime.executeToolCall` (CH-02). Que un `AgentRun` real
  atraviese los cinco componentes en una sola ejecución, sin que ninguna señal siga siendo
  "asumida", es, explícitamente, trabajo de un capítulo de integración futuro — el candidato más
  claro de todo el libro hasta ahora, dado que este capítulo cierra la última resolución que
  faltaba.
- **El mecanismo real de registro/alta de capabilities**: `registeredCapabilities` llega como
  parámetro ya poblado (§6/§11) — este capítulo no modela quién registra un `CapabilityDescriptor`
  nuevo, ni dónde se persiste ese registro entre ejecuciones. No existe ningún
  `CapabilityRegistrationRequest`, ninguna API administrativa ni ningún mecanismo de descubrimiento
  automático de capabilities.
- **El algoritmo real de validación de esquemas**: `argumentsMatchSchema` sigue siendo una señal de
  entrada asumida (§11) — este capítulo define dónde vive el schema (`CapabilityDescriptor.
  inputSchema`), pero no el motor que compararía `rawArguments` contra ese schema campo por campo.
- **Capability lifecycle completo (P-26, Amendment v1.1)**: `CapabilityDescriptor.version` es
  explícita, pero compatibility policy, rollout, deprecation y retirement — el resto de lo que
  P-26 exige — quedan fuera de alcance; no existe ningún mecanismo que rechace una versión
  deprecada ni que gestione una migración entre versiones.
- **Idempotencia y semántica de reintentos de una capability (P-24, Amendment v1.1)**: fuera de
  alcance de BH-v0.1, igual que en capítulos anteriores.
- **El cableado formal de vuelta hacia `ToolRuntime`**: `ToolRuntime.executeToolCall` (CH-02) sigue
  recibiendo `capabilityResolved`/`inputValid` como señales de entrada asumidas — este capítulo
  produce la pieza real que las llenaría, pero no modifica la firma de `executeToolCall`.
- **`SessionManager`, Provider Adapters reales, streaming real, `Channel Adapter` real,
  persistencia real de `ExecutionUsage`**: deuda heredada de capítulos anteriores, sin cambios
  aquí.
- Reviewers plurales, evals y orquestación multi-agente: explícitamente fuera de alcance de BH-v0.1
  (igual que todos los capítulos anteriores).

## 19. Siguiente Incremento (Next Increment)

El problema natural del próximo capítulo: con los ocho componentes centrales del arnés ya
existentes (`AgentLoop`, `ToolRuntime`, `ModelGateway`, `ContextEngine`, `PolicyEngine`,
`HumanInteractionService`, `ExecutionController`, `CapabilityRegistry`), y con cada uno de ellos
demostrado de forma autónoma pero nunca los ocho juntos en una sola ejecución real, ¿quién cablea
formalmente el flujo completo de un turno — de modo que `AgentLoop.runTurn` invoque realmente a
`ModelGateway.invoke`, que su `ModelResponse` se resuelva realmente mediante
`CapabilityRegistry.resolveToolCall`, que el `ToolCall` resultante pase realmente por
`PolicyEngine.evaluate` antes de llegar a `ToolRuntime.executeToolCall`, y que
`ExecutionController.evaluateExecutionContinuation` se consulte en el punto correcto del ciclo? Ese
capítulo de integración heredaría, de una sola vez, la deuda intencional que CH-01..CH-08 fueron
posponiendo, capítulo a capítulo, en sus propias secciones 18.

`next_chapter` queda en `null` en el frontmatter de este capítulo porque, en este momento del
libro, ese capítulo de integración todavía no existe como archivo — solo como el problema que
motivaría su escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de
> la secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco
> Iceberg / Bucles de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas,
> Forrester/Meadows), secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): el componente que decide "qué implementación satisface
   una capacidad solicitada" lleva citado treinta veces a lo largo de los primeros ocho capítulos
   del libro — veintiuna de ellas concentradas entre `ToolRuntime` y `ModelGateway` — siempre como
   deuda pendiente, nunca como código real.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): dos componentes ya
   construidos pueden declarar honestamente, cada uno desde su propio `does_not_own`, que una
   responsabilidad no les pertenece — y aun así esa responsabilidad quedar sin dueño real, porque
   declarar una exclusión no es lo mismo que instalar el componente que la ocupa.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `CapabilityRegistry` (CMP-008) con una ficha que declara tanto lo que posee (`owns`) como lo que
   explícitamente NO posee (`does_not_own`) y formaliza `CapabilityDescriptor` (C-018) — el primer
   contrato del libro con un campo de versión explícito.
4. **Modelos mentales** (= §4, Constitutional Impact): el Ownership Rule de Article IV, junto con
   la cita literal de Article III ("responsable de desacoplar la intención de una capacidad de su
   implementación concreta") — la pregunta que este capítulo, por primera vez, responde con código
   real en vez de con una exclusión declarada.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que dos componentes vecinos declaran, cada uno por su
  cuenta, que una responsabilidad no les pertenece, aumenta el riesgo de que esa responsabilidad se
  quede sin dueño real más tiempo del necesario — porque cada declaración de exclusión se siente,
  por sí sola, como progreso, aunque ninguna instale el componente que falta.
- **Bucle de equilibrio (estabiliza):** `resolveToolCall` (§11) recorre el registro real de
  `CapabilityDescriptor`s y rechaza, con un `HarnessError` categorizado, tanto un `capabilityName`
  sin descriptor registrado como un `rawArguments` que no cumple el schema declarado — antes de
  producir cualquier `ToolCall`.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `CapabilityRegistry` (CMP-008) resuelva el
`capabilityName` de una `RawToolCallProposal` mediante una búsqueda real contra una lista de
`CapabilityDescriptor` (C-018) — no mediante una señal booleana asumida — y que el `ToolCall`
(C-008) que produce tome su campo `capability` directamente del descriptor encontrado, nunca del
texto libre que el modelo propuso. Si esta resolución siguiera siendo una señal asumida, el libro
completo llegaría a un capítulo de integración final sin que ningún componente hubiera demostrado,
con pseudocódigo real, cómo un nombre de texto libre se convierte en una acción ya resuelta y lista
para pasar por policy y ejecución.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado
> completo de esta sección (con ids estables para cada pregunta/tarjeta) vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida. Aquí se
> presenta en prosa, para lectura directa del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Cuando el modelo propone usar una herramienta nombrándola solo por texto libre y con argumentos
   todavía sin resolver, ¿quién decide qué implementación concreta corresponde a ese nombre, y qué
   necesita existir de antemano para que esa decisión sea posible? *(cierra la pregunta guía 1)*
2. Si esa propuesta llega con argumentos que no corresponden a lo que la implementación resuelta
   espera recibir, ¿en qué momento exacto del camino debe detectarse ese desajuste, y qué le impide
   a una intención de acción mal formada seguir avanzando hacia su ejecución? *(cierra la pregunta
   guía 2)*
3. Dos capítulos distintos ya dejaron marcada la misma frontera desde lados opuestos. ¿Qué necesita
   existir para que esa frontera compartida por fin tenga, en la práctica, quien la ocupe? *(cierra
   la pregunta guía 3)*
4. ¿Alcanza con verificar que exista una implementación para el nombre de capacidad solicitado, o
   hace falta además algo que describa qué versión de esa implementación es y qué forma de entrada
   espera recibir? *(cierra la pregunta guía 4)*

### Explicar

1. `CapabilityRegistry` posee resolver qué implementación satisface una capacidad solicitada.
   Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee ejecutar esa
   capacidad una vez resuelta, aunque acaba de "encontrarla" — ¿qué se rompería, en concreto, si
   `CapabilityRegistry` empezara a ejecutar directamente la implementación que encontró?
2. `CapabilityDescriptor.implementationRef` es una referencia opaca a la implementación concreta,
   no el código de esa implementación. Explica qué perderíamos si `CapabilityRegistry`, en vez de
   guardar una referencia opaca, modelara el detalle interno de cada implementación dentro de su
   propio registro.

### Conectar

1. `ToolRuntime` (CH-02) declaró que no le pertenece "el registro y la resolución de qué
   implementación satisface una capability solicitada", y `ToolCall` (C-008) exige un campo
   `capability` ya resuelto. ¿Qué construye este capítulo para que ese `ToolCall` deje de depender
   de una resolución externa asumida?
2. `ModelResponse` (C-007, CH-03) transporta `proposedToolCall` como una `RawToolCallProposal`
   deliberadamente cruda. ¿Qué hace este capítulo con `capabilityName` y `rawArguments` para
   producir, por primera vez, un `ToolCall` real?

### Espaciar

Las cinco tarjetas de repaso de este capítulo (dos sobre `CapabilityRegistry` — su `owns` y su
`does_not_own` —, y tres sobre `CapabilityDescriptor` — sus campos, por qué incluye una versión
explícita, y qué produce este capítulo por primera vez) entran hoy en `reviewStage = DAY_1`.
Repásalas de nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) — ver el apéndice de
tarjetas al final del libro (edición PDF) o `retrieval_set.flashcards` en `dist/book-ir.json`
(edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te
equivocaste, ese es precisamente el punto ciego que este método existe para revelar.
