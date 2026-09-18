---
id: CH-16
title: "CredentialBroker y la Resolución Segura de una Credencial"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: [CMP-014]
introduces_contracts: [C-026]
modifies_contracts: []
constitutional_articles: [P-13, P-22, INV-E07, INV-E08, INV-18, INV-19, INV-20]
previous_chapter: CH-15
next_chapter: CH-17
retrieval_set:
  expected_outcome:
    id: EO-CH16
    text: |
      Al terminar este capítulo podrás distinguir, para cualquier implementación de capability ya
      resuelta que necesita autenticarse contra un sistema externo real para producir un side
      effect, qué tramo le pertenece en exclusiva al componente que resuelve esa credencial sin que
      su valor real entre jamás al contexto del modelo (Amendment v1.1, `INV-E08`) — sin decidir si
      esa acción ya resuelta está autorizada para ejecutarse, sin decidir qué implementación
      satisface la capability solicitada — y podrás diseñar, para cualquier secreto que un sistema
      necesite, una referencia opaca que nunca transporte el valor crudo, aplicando sobre ese
      secreto el gobierno de datos que exige `P-22` (clasificación, rotación, expiración).
  skeleton:
    id: SK-CH16
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
    components_to_be_introduced: [CMP-014]
    contracts_to_be_introduced: [C-026]
  guiding_questions:
    - id: GQ-CH16-01
      text: |
        Cuando una implementación de capability, ya resuelta y ya identificada de forma exacta,
        necesita autenticarse contra un sistema externo real para producir un side effect, ¿quién
        decide qué secreto usa, y qué necesitaría existir para garantizar que ese valor crudo nunca
        llegue a formar parte del contexto que el modelo puede leer?
      answered_by: RQ-CH16-01
    - id: GQ-CH16-02
      text: |
        La decisión de si una acción ya resuelta está autorizada para ejecutarse ya tiene, en este
        libro, un dueño propio. ¿Esa misma pregunta sirve también para decidir con qué secreto un
        sistema se autentica ante otro, o son, honestamente, dos preguntas distintas que necesitan
        dueños distintos?
      answered_by: RQ-CH16-02
    - id: GQ-CH16-03
      text: |
        Si un secreto usado para autenticarse tiene una fecha de vencimiento, o necesita rotarse
        periódicamente, ¿qué debería pasar cuando alguien intenta usar una referencia a ese secreto
        que ya venció?
      answered_by: RQ-CH16-03
    - id: GQ-CH16-04
      text: |
        Un secreto que permite autenticarse contra un sistema externo es, en sí mismo, una forma de
        dato empresarial con sensibilidad real. ¿Necesita el mismo tipo de gobierno explícito
        (clasificación, aislamiento) que cualquier otro dato gobernado de este libro, o puede
        tratarse como un detalle de implementación sin tratamiento especial?
      answered_by: RQ-CH16-04
  systems_lens:
    iceberg_visible_fact: |
      Dieciséis capítulos reales instalaron un runtime completo más dos componentes de Enterprise
      (`AdmissionController`, CH-14; `AgentCommunicationGateway`, CH-15) — pero ningún capítulo
      modeló jamás cómo una implementación de capability ya resuelta (`CapabilityDescriptor.
      implementationRef`, C-018, CH-08 — una referencia deliberadamente opaca) obtiene el secreto
      que necesita para autenticarse contra el sistema externo real que envuelve. `ToolRuntime.
      executeToolCall` (CH-02 §11) recibe `executionSucceeded`/`executionOutput` como señales
      externas asumidas, sin modelar jamás cómo esa ejecución se autenticó (ver seccion 2, El
      Problema).
    iceberg_patterns: |
      El mismo patrón que motivó CH-14 y CH-15 se repite un plano después: Amendment v1.1 nombra
      literalmente `CredentialBroker` desde que fue adoptada (`INV-E08`), y tanto CH-14 §18 como
      CH-15 §18 ya lo mencionaron por nombre, dos veces seguidas, entre los componentes
      explícitamente diferidos — una deuda nombrada dos veces, resuelta recién en este capítulo (ver
      seccion 3, Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Este capítulo instala el tercer componente de Amendment v1.1 — y, deliberadamente, el tercer
      plano que este libro cubre de los nueve que la enmienda enumera: no el "Execution Plane" (el
      segundo en el orden canónico, todavía sin cubrir), sino el "Capability & Integration Plane"
      (el cuarto) — con una ficha que declara tanto lo que posee (`owns`: resolver la credencial que
      una implementación ya resuelta necesita, sin que su valor real entre jamás al contexto del
      modelo, `INV-E08` cita literal; aplicar sobre ese secreto el gobierno de datos que `P-22`
      exige — clasificación, rotación, expiración) como lo que explícitamente NO posee (decidir si
      la acción ya resuelta está autorizada, decidir qué implementación satisface la capability,
      ejecutar el side effect en sí) (ver seccion 8, Component Responsibilities).
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es que "¿con qué se autentica un sistema?" es
      una pregunta completamente distinta de "¿está permitida esta acción?" (`P-13`, ya aplicada
      desde CH-05 a la autorización, aplicada aquí por segunda vez a la credencial misma) y de
      "¿qué implementación satisface esta capability?" (`CapabilityRegistry`, CH-08) — tres
      preguntas con dueños distintos que, sin este componente, corrían el riesgo de resolverse todas
      en el mismo lugar, con el mismo secreto crudo circulando sin control (ver seccion 4, Impacto
      Constitucional).
    reinforcing_loop: |
      Cada vez que un sistema deja sin modelar cómo una implementación obtiene sus credenciales,
      cualquier componente puede terminar incrustando el secreto directamente en el contexto del
      modelo (para que "arme" la petición) o hardcodeado sin ningún ciclo de vida — exactamente lo
      que `INV-E08` existe para prevenir, el mismo bucle de "la ausencia de un dueño se vuelve una
      dependencia implícita" que ya combatieron `P-02` (CH-03) y `P-19` (CH-15), ahora aplicado al
      secreto en vez de al modelo o al protocolo.
    balancing_loop: |
      `resolveCredentialReference` (seccion 11) es el mecanismo de equilibrio: nunca devuelve el
      secreto real — solo una `CredentialReference` opaca — y rechaza, con un `HarnessError`
      categorizado, tanto un secreto que no corresponde a la capability resuelta como uno ausente o
      ya vencido, antes de que cualquier implementación llegue a intentar autenticarse con él.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que `CredentialReference` (C-026) nunca
      tenga, en ningún campo, el valor real del secreto que representa — ni siquiera cifrado, ni
      siquiera parcialmente. Si `CredentialReference` transportara el secreto (aunque fuera
      "protegido"), cualquier componente río abajo que lo reciba —incluyendo, eventualmente, algo
      que termine construyendo contexto para el modelo— se convertiría en una superficie real de
      fuga, exactamente la violación que `INV-E08` prohíbe.
  recall_questions:
    - id: RQ-CH16-01
      text: |
        ¿Qué componente resuelve la credencial que una implementación de capability ya resuelta
        necesita, y qué invariante literal de Amendment v1.1 exige que su valor real nunca entre al
        contexto del modelo?
    - id: RQ-CH16-02
      text: |
        ¿Qué campos tiene `CredentialReference` (C-026), y por qué ninguno de ellos contiene jamás
        el valor real del secreto que representa?
    - id: RQ-CH16-03
      text: |
        ¿Qué dos capítulos anteriores ya nombraron literalmente, cada uno en su propia sección 18,
        el componente que este capítulo por fin instala con código real?
    - id: RQ-CH16-04
      text: |
        ¿Qué `ENUM` introduce este capítulo para materializar, por primera vez con código real, la
        exigencia de clasificación de `P-22` aplicada específicamente a un secreto, y por qué se
        descartó un campo `Boolean` en su lugar?
  explain_prompts:
    - id: EP-CH16-01
      text: |
        `CredentialBroker` posee resolver la credencial que una implementación de capability ya
        resuelta necesita para autenticarse. Explica, como si hablaras con alguien sin contexto
        técnico, por qué NO posee decidir si la acción que esa implementación va a ejecutar está
        autorizada — ¿qué se rompería si, ya que de todos modos maneja el secreto, también decidiera
        eso?
      target_entity: CMP-014
    - id: EP-CH16-02
      text: |
        `CredentialReference` es una referencia deliberadamente opaca: nunca transporta el valor
        real del secreto que representa. Explica qué perderíamos — y qué riesgo nuevo
        introduciríamos — si en vez de una referencia opaca, este contrato incluyera directamente el
        secreto (aunque fuera cifrado) para ahorrarle a otros componentes una segunda consulta.
      target_entity: C-026
  interleaved_questions:
    - id: IQ-CH16-01
      text: |
        `CapabilityRegistry` (CH-08) ya resuelve qué implementación concreta satisface una
        capability solicitada, produciendo un `CapabilityDescriptor` (C-018) con un
        `implementationRef` deliberadamente opaco. Cuando ese descriptor ya existe, ¿le corresponde
        a este capítulo volver a decidir qué implementación es la correcta, o asume esa resolución
        como un hecho ya cerrado y solo se ocupa de lo que todavía falta — el secreto que esa
        implementación, ya identificada, necesita para autenticarse?
      current_chapter_entities: [CMP-014, C-026]
      prior_chapter_entities: [CMP-008, C-018]
      prior_chapter: CH-08
    - id: IQ-CH16-02
      text: |
        `PolicyEngine` (CH-05) ya decide si un `ToolCall` está autorizado para ejecutarse. Si esa
        autorización ya fue concedida, ¿alcanza con que la implementación use cualquier secreto que
        tenga a mano, o la pregunta de qué credencial exacta usar — y si esa credencial en concreto
        sigue vigente — sigue siendo una pregunta distinta, con un dueño distinto, que
        `PolicyEngine` nunca respondió ni podría responder?
      current_chapter_entities: [CMP-014, C-026]
      prior_chapter_entities: [CMP-005]
      prior_chapter: CH-05
  flashcards:
    - id: FC-CH16-01
      front: |
        ¿Qué posee `CredentialBroker`?
      back: |
        Resolver la credencial (API key, token, secreto) que una implementación de capability ya
        resuelta necesita para producir un side effect real, garantizando que su valor crudo nunca
        entre al contexto del modelo (`INV-E08`, cita literal); aplicar sobre ese secreto el
        gobierno de datos que `P-22` exige — clasificación y rotación/expiración —; aislar
        credenciales por tenant (`INV-E07`, cita literal); y rechazar por defecto (fail-closed)
        cuando el secreto no corresponde a la capability, no existe o ya venció.
      source_entity: CMP-014
      chapter_introduced_in: CH-16
      review_stage: DAY_1
    - id: FC-CH16-02
      front: |
        ¿Qué NO posee `CredentialBroker`?
      back: |
        Decidir si una acción/`ToolCall` ya resuelta está autorizada para ejecutarse (`PolicyEngine`,
        CMP-005, CH-05 — pregunta distinta: "con qué se autentica" nunca es "si está permitido");
        resolver qué implementación satisface una capability solicitada (`CapabilityRegistry`,
        CMP-008, CH-08 — este componente actúa DESPUÉS, sobre un `CapabilityDescriptor` ya
        resuelto); ejecutar el side effect en sí (`ToolRuntime`, CMP-002, CH-02); ni el mecanismo
        real de almacenamiento/rotación del secreto (Secret Store — infraestructura de borde, no un
        componente de este registry).
      source_entity: CMP-014
      chapter_introduced_in: CH-16
      review_stage: DAY_1
    - id: FC-CH16-03
      front: |
        ¿Qué campos tiene `CredentialReference` (C-026), y por qué ninguno contiene el secreto real?
      back: |
        `id`, `capability` (`CapabilityId`, referencia opaca al `CapabilityDescriptor`, C-018, CH-08,
        al que pertenece este secreto), `credentialName` (`Text`, nombre/scope del secreto, p. ej.
        "github-api-token"), `classification` (`CredentialClassification`, P-22), `resolvedAt`
        (`Timestamp`) y `expiresAt` (`Optional<Timestamp>`, rotación/expiración, P-22). El valor
        real del secreto nunca aparece: si apareciera, cualquier componente que reciba esta
        referencia se volvería una superficie de fuga — la violación exacta que `INV-E08` prohíbe.
      source_entity: C-026
      chapter_introduced_in: CH-16
      review_stage: DAY_1
    - id: FC-CH16-04
      front: |
        ¿Por qué `CredentialReference.classification` es un `ENUM` (`CredentialClassification`) y no
        un `Boolean isSensitive`?
      back: |
        Porque no todos los secretos cargan el mismo riesgo — una API key de solo lectura y un
        token administrativo no deberían gobernarse igual — y un `Boolean` colapsaría esa diferencia
        real a un solo bit, exactamente el mismo argumento de diseño que ya descartó `allowAll:
        Boolean` para `DelegationGrant.delegatedScope` en CH-15: un valor de dos estados hace
        estructuralmente imposible representar una gradación que `P-22` exige poder distinguir.
      source_entity: C-026
      chapter_introduced_in: CH-16
      review_stage: DAY_1
    - id: FC-CH16-05
      front: |
        ¿Por qué `CredentialBroker` sí produce un `AgentEvent` real, a diferencia de los dos
        componentes de Amendment v1.1 que lo precedieron (`AdmissionController`, CH-14;
        `AgentCommunicationGateway`, CH-15)?
      back: |
        Porque, a diferencia de esos dos, cuando `CredentialBroker` actúa, el `AgentRun` que lo
        necesita ya existe con `runId`/`sessionId`/`agentId`/`traceId` completos — la misma
        situación de `CapabilityRegistry` (CH-08). El payload del evento es siempre la
        `CredentialReference` opaca o el `HarnessError`, nunca el secreto — la emisión de telemetría
        nunca compromete `INV-E08`.
      source_entity: CMP-014
      chapter_introduced_in: CH-16
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH16-01
      recall_question: RQ-CH16-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH16-02
      recall_question: RQ-CH16-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH16-03
      recall_question: RQ-CH16-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH16-04
      recall_question: RQ-CH16-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 16 — CredentialBroker y la Resolución Segura de una Credencial

> **Regla constitucional (Amendment v1.1, `INV-E08`):** "Credentials are resolved by a
> `CredentialBroker` and SHOULD NOT enter model context."

CH-14 y CH-15 abrieron el territorio de Amendment v1.1 con dos planos consecutivos — Ingress &
Activation (`AdmissionController`) y Agent Interoperability (`AgentCommunicationGateway`). Este
capítulo entra al **tercer plano que este libro cubre**, de nuevo deliberadamente NO en el orden
canónico que la enmienda enumera (Ingress & Activation → Execution → Agent Interoperability →
Capability & Integration → ...): en vez de retroceder al Execution Plane (el segundo de la lista,
todavía sin cubrir), este capítulo avanza hacia el cuarto — **Capability & Integration Plane** —
porque es el plano donde vive, desde que Amendment v1.1 fue adoptada, la única mención literal de
`CredentialBroker` en toda la Constitution (`INV-E08`), y porque tanto CH-14 §18 como CH-15 §18 ya
lo nombraron explícitamente, dos veces seguidas, entre los componentes diferidos. Los seis planos
restantes — incluyendo el Execution Plane completo — quedan, otra vez deliberadamente, para
incrementos futuros (ver seccion 19).

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de saber
> cómo se llama el componente de este capítulo. El detalle estructurado de esta sección vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida
> automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás distinguir, para cualquier implementación
de capability ya resuelta que necesita autenticarse contra un sistema externo real para producir un
side effect, qué tramo le pertenece en exclusiva al componente que resuelve esa credencial sin que
su valor real entre jamás al contexto del modelo (Amendment v1.1, `INV-E08`) — sin decidir si esa
acción ya resuelta está autorizada para ejecutarse, sin decidir qué implementación satisface la
capability solicitada — y podrás diseñar, para cualquier secreto que un sistema necesite, una
referencia opaca que nunca transporte el valor crudo, aplicando sobre ese secreto el gobierno de
datos que exige `P-22` (clasificación, rotación, expiración).

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment) e introduce
un contrato de datos nuevo y el tercer componente de este libro que pertenece a Amendment v1.1 en
vez de a los once nombres originales de Article III — todavía sin explicarlos, solo como mapa.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar atrás;
están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que este capítulo
va a definir):

1. Cuando una implementación de capability, ya resuelta y ya identificada de forma exacta, necesita
   autenticarse contra un sistema externo real para producir un side effect, ¿quién decide qué
   secreto usa, y qué necesitaría existir para garantizar que ese valor crudo nunca llegue a formar
   parte del contexto que el modelo puede leer?
2. La decisión de si una acción ya resuelta está autorizada para ejecutarse ya tiene, en este libro,
   un dueño propio. ¿Esa misma pregunta sirve también para decidir con qué secreto un sistema se
   autentica ante otro, o son, honestamente, dos preguntas distintas que necesitan dueños distintos?
3. Si un secreto usado para autenticarse tiene una fecha de vencimiento, o necesita rotarse
   periódicamente, ¿qué debería pasar cuando alguien intenta usar una referencia a ese secreto que
   ya venció?
4. Un secreto que permite autenticarse contra un sistema externo es, en sí mismo, una forma de dato
   empresarial con sensibilidad real. ¿Necesita el mismo tipo de gobierno explícito (clasificación,
   aislamiento) que cualquier otro dato gobernado de este libro, o puede tratarse como un detalle de
   implementación sin tratamiento especial?

## 1. Arquitectura Actual (Current Architecture)

CH-00..CH-15 dejaron instalados veinticinco contratos de datos y trece componentes: los once nombres
completos de Article III ("Agent Runtime"), dos capítulos de integración, `AdmissionController`
(CMP-012, CH-14, Ingress & Activation Plane) y `AgentCommunicationGateway` (CMP-013, CH-15, Agent
Interoperability Plane). Ninguno de los trece resolvió jamás, con código real, cómo una
implementación de capability se autentica contra el sistema externo que envuelve.

`CapabilityDescriptor.implementationRef` (C-018, CH-08 §6) es, por diseño explícito de ese capítulo,
una referencia opaca (`Text`) a la implementación concreta — "nunca el código de esa implementación
ni su detalle interno". Esa decisión fue correcta entonces y sigue siéndolo: pero significa que,
hasta este capítulo, ningún contrato de este libro modeló jamás qué necesita esa implementación,
ya identificada, para funcionar de verdad contra un sistema externo real — específicamente, con qué
credencial se autentica. `ToolRuntime.executeToolCall` (CH-02 §11) recibe `executionSucceeded` y
`executionOutput` como señales externas ya asumidas, exactamente en el punto donde una
autenticación real tendría que haber ocurrido — CH-02 nunca reclamó cerrar ese hueco, y ningún
capítulo posterior lo cerró tampoco.

Amendment v1.1 ya nombra, literalmente, el componente que resolvería esto — desde la primera versión
de esta enmienda adoptada por el repositorio, antes de que este capítulo existiera:

- `INV-E08`: "Credentials are resolved by a `CredentialBroker` and SHOULD NOT enter model context."
- `INV-E07`: "Tenant data, memory, credentials, artifacts and audit records are isolated." (cita
  "credentials" explícitamente, junto a otros cuatro tipos de dato gobernado).
- `P-22` ("Enterprise data is governed throughout its lifecycle"): "Classification, residency,
  retention, lineage, encryption, deletion and legal-hold requirements MUST be enforceable
  independently of model reasoning."

Y este componente ya fue nombrado, dos veces, por capítulos anteriores de este mismo libro sin que
ninguno lo resolviera: CH-14 §18 lo listó explícitamente entre "los ocho planes restantes de
Amendment v1.1... y sus componentes (`AgentCommunicationGateway`, `CredentialBroker`, y el resto)";
CH-15 §18 repitió, palabra por palabra, la misma mención — "los seis planos restantes... y sus
componentes (`CredentialBroker`, y el resto)". `P-22`, además, ya fue citado en prosa por CH-10 §15
y CH-11 §18 como un límite reconocido de gobierno de datos sobre lo persistido — pero ningún
capítulo, hasta este, lo materializó jamás con un campo real de un `STRUCT` registrado.

## 2. El Problema (Problem)

Sin un componente con fronteras explícitas para esto, "¿con qué credencial se autentica una
implementación ya resuelta?" tiende a resolverse de la forma más simple y más peligrosa: el secreto
crudo termina incrustado directamente donde sea más conveniente — a veces hardcodeado dentro de la
implementación misma, sin ningún ciclo de vida (sin rotación, sin expiración, sin clasificación); a
veces, peor todavía, expuesto dentro del propio contexto que el modelo puede leer, para que el
modelo "arme" correctamente la petición que necesita autenticación — exactamente lo que `INV-E08`
existe para prohibir. Ninguna de las dos rutas es hipotética: son, literalmente, el comportamiento
por defecto de cualquier sistema que no tenga un componente dedicado a esta pregunta.

Hay una segunda dimensión del problema, tan real como la primera. Aun si el secreto nunca llegara al
modelo, nada impide, todavía, que "¿qué credencial usar?" se confunda con "¿está permitida esta
acción?" — dos preguntas de dominios distintos que Article IV asignaría a dueños distintos si
existiera un componente que ocupara la primera. `PolicyEngine` (CH-05) ya decide si un `ToolCall`
está autorizado; eso no dice nada sobre si la credencial concreta que la implementación usaría para
ejecutarlo sigue vigente, no ha vencido, y en efecto corresponde a esa capability y no a otra.

Necesitamos que "¿qué credencial necesita esta implementación ya resuelta, y sigue siendo válida?"
tenga, por fin, un dueño único y nombrado — que reciba un `CapabilityDescriptor` ya resuelto (nunca
decida, de nuevo, qué implementación usar — eso ya lo resolvió `CapabilityRegistry`), que nunca
decida si la acción que esa implementación va a ejecutar está autorizada (eso sigue siendo de
`PolicyEngine`), que produzca exclusivamente una referencia opaca — nunca el secreto real — y que
aplique, sobre ese secreto específico, el gobierno de datos que `P-22` exige: clasificación y
rotación/expiración explícitas.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Los veinticinco contratos y los trece componentes que existen hasta este punto no bastan porque:

- `INV-E08` cita literalmente, desde que Amendment v1.1 fue adoptada, `CredentialBroker` — un
  nombre que ningún capítulo había materializado con código real; CH-14 §18 y CH-15 §18 ya lo
  mencionaron, ambos, entre los componentes explícitamente diferidos, sin resolverlo ninguno de los
  dos;
- `CapabilityDescriptor.implementationRef` (C-018, CH-08) es, por diseño, una referencia opaca —
  correctamente, para no modelar el detalle interno de una implementación — pero eso deja
  completamente sin resolver qué necesita esa implementación, ya identificada, para autenticarse
  contra el sistema externo real que envuelve;
- `ToolRuntime.executeToolCall` (CH-02 §11) trata `executionSucceeded`/`executionOutput` como
  señales externas asumidas, exactamente en el tramo donde una autenticación real ocurriría — nunca
  modeló, ni reclamó modelar, cómo se obtiene la credencial que esa ejecución necesitaría;
- ningún contrato de este libro representa, todavía, un secreto ni una referencia a él —
  `HarnessError` (C-011), `ExecutionBudget` (C-012) y el resto de los veinticinco contratos
  existentes no tienen ningún campo pensado para transportar, ni siquiera de forma opaca, la
  identidad de una credencial;
- `P-22` fue citado en prosa por CH-10 §15 y CH-11 §18 como un límite reconocido — pero ningún
  `STRUCT`/`ENUM` de este libro lo materializó jamás con un campo de clasificación o de vencimiento
  real; sigue siendo, hasta este capítulo, una cita sin código;
- `PolicyEngine` (CMP-005, CH-05) evalúa si un `ToolCall` está autorizado — pero nunca evaluó, ni
  podría evaluar sin invadir Decision Ownership, si la credencial concreta que autenticaría esa
  acción sigue siendo válida: son preguntas de dominios distintos, formuladas sobre material
  distinto (una intención de acción ya resuelta contra un secreto que esa acción necesitaría).

> **Regla editorial fundamental (recordatorio):** todo concepto debe atravesar siempre la secuencia
> `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una entidad que no
> haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT` registrado — **no
> magic entities**. Este capítulo aplica la misma disciplina que CH-00..CH-15 ya establecieron, con
> una particularidad: es el tercer componente de este registry cuyo `owns` se ancla en la cita
> literal de un invariante de Amendment v1.1 (`INV-E08`) que menciona el nombre del componente
> palabra por palabra, no solo su dominio de responsabilidad.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-13   Authorization is deterministic and external to the LLM.
           El mismo argumento que ya protegió la autorización desde CH-01/CH-05 se extiende aquí
           a la credencial misma: el modelo nunca elige, nunca ve y nunca constituye una fuente de
           verdad sobre qué secreto se usa para autenticarse — resolveCredentialReference (seccion
           11) es completamente determinístico y externo al LLM.
    P-22   Enterprise data is governed throughout its lifecycle.
           Primera materialización real, con código, de este principio en todo el libro —
           CredentialReference.classification/expiresAt (seccion 6/7), después de que CH-10 §15 y
           CH-11 §18 solo lo hubieran citado en prosa como un límite reconocido, nunca resuelto.

Invariants preserved
    INV-E07   Tenant data, memory, credentials, artifacts and audit records are isolated.
              Primera cita literal con código real de la palabra "credentials" de este invariante:
              CredentialReference (seccion 6/7) es el contrato que haría posible, en una
              integración futura, que un CredentialBroker real aplique aislamiento por tenant sobre
              credenciales — el mecanismo de aislamiento en sí sigue siendo Preview (ver seccion
              15/18).
    INV-E08   Credentials are resolved by a CredentialBroker and SHOULD NOT enter model context.
              Cita literal y definitoria de este capítulo completo: CredentialBroker (seccion 8) es
              la primera materialización real del nombre que este invariante ya usaba desde que
              Amendment v1.1 fue adoptada — CredentialReference (seccion 6/7) es, por diseño,
              incapaz de transportar el valor real del secreto (ver seccion 6, "por qué nunca un
              campo de valor").
    INV-18    Toda acción significativa produce un evento observable.
              resolveCredentialReference (seccion 11) emite un AgentEvent en cada resolución (éxito
              o fallo) — a diferencia de AdmissionController (CH-14) y AgentCommunicationGateway
              (CH-15), este componente SÍ produce eventos reales (ver seccion 14 para el porqué).
    INV-19    Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy relevante.
              Cada AgentEvent que emite CredentialBroker lleva el traceId de su ExecutionContext, y
              la CredentialReference producida correlaciona, por su campo capability, con el
              CapabilityDescriptor exacto que la originó.
    INV-20    Todo error operacional pertenece a una categoría conocida.
              El único fallo real de este capítulo (seccion 13) introduce CREDENTIAL, una categoría
              nueva de ErrorCategory — ninguna de las catorce ya existentes (incluida VALIDATION,
              que pertenece a fallos de forma/esquema, CH-02/CH-08) representa, sin conflación, el
              rechazo de una resolución de credencial por ausencia, vencimiento o mismatch de
              capability.

Component ownership changes
    CMP-014 CredentialBroker se introduce — registry/components.yaml pasa de 13 a 14 componentes.
    Es el tercer componente de este registry que NO corresponde a ninguno de los once nombres del
    árbol de Article III ("Agent Runtime") — pertenece, en cambio, al "Capability & Integration
    Plane" de Amendment v1.1 (el cuarto plano canónico, tercero que este libro cubre — ver apertura
    del capítulo). registry/components.yaml de CMP-002 (ToolRuntime), CMP-005 (PolicyEngine) y
    CMP-008 (CapabilityRegistry) NO se modifica: ninguno cablea todavía su relación real con
    CredentialBroker (ver seccion 9/18).

Lifecycle changes
    Ninguna modificación a AgentRunStatus (C-013): este capítulo no construye, ni transiciona,
    ningún AgentState. CredentialReference no tiene ningún ENUM de estado propio — su vigencia se
    deriva, en cada evaluación, de comparar now() contra expiresAt (mismo patrón que DelegationGrant,
    C-025, CH-15 §12).

Security implications
    CredentialBroker es el primer componente de este libro cuya responsabilidad completa es
    resolver, sin exponerlo jamás, un secreto real. Ver seccion 15 para el análisis completo,
    incluyendo por qué CredentialReference nunca puede degradar en la práctica hacia una fuga de
    INV-E08.

Observability implications
    A diferencia de AdmissionController (CH-14, el run todavía no existe) y AgentCommunicationGateway
    (CH-15, AgentCommunicationMessage no tiene sessionId), CredentialBroker SÍ produce AgentEvent en
    la práctica — el run que necesita una credencial ya existe con runId/sessionId/agentId/traceId
    completos, la misma situación que CapabilityRegistry (CH-08). Ver seccion 14.

Deterministic vs agentic boundary
    Article XII se refina una decimocuarta vez a nivel de componente: CredentialBroker, igual que
    CapabilityRegistry (CH-08), no interpreta ninguna salida del modelo — compara,
    determinísticamente, un CapabilityDescriptor y un conjunto de señales de gobierno contra un
    registro de secretos que el harness controla por completo. El modelo ni siquiera es consciente
    de que esta resolución ocurrió.
```

## 5. Conceptos Nuevos (New Concepts)

- **Credential / Secret**: el valor sensible real (una API key, un token, una contraseña) que
  autentica una implementación de capability contra el sistema externo que envuelve. Este libro
  **nunca** modela ese valor como un contrato — no existe, ni existirá, ningún `STRUCT` cuyo campo
  contenga un secreto crudo. Se representa, exclusivamente, mediante una referencia opaca (ver
  siguiente concepto).
- **Credential Reference** *(cita literal, `INV-E08`)*: la referencia opaca que viaja por el sistema
  en lugar del secreto real — modelada, por primera vez con código real, como el contrato
  `CredentialReference` (C-026, seccion 6/7).
- **Credential Resolution**: el acto determinístico de encontrar, validar (pertenencia a la
  capability correcta, existencia, vigencia) y referenciar — nunca exponer — la credencial que una
  implementación de capability ya resuelta necesita.
- **Credential Classification** *(materialización literal de `P-22`, "classification")*: la
  exigencia de que un secreto declare un nivel de sensibilidad explícito, en vez de tratarse como un
  detalle de implementación sin gobierno. Modelada como `CredentialReference.classification:
  CredentialClassification` (seccion 6).
- **Credential Rotation** / **Credential Expiration** *(lectura de `P-22`, "retention" aplicada
  específicamente a un secreto)*: el vencimiento explícito de una `CredentialReference`, más allá del
  cual `CredentialBroker` rechaza por defecto — modelado, de forma mínima, como
  `CredentialReference.expiresAt: Optional<Timestamp>`. Este capítulo no modela el mecanismo real que
  rota un secreto detrás de esa fecha (ver seccion 18).
- **Secret Store** *(concepto de infraestructura de borde, no un componente de este registry)*: la
  pieza real (vault, secret manager, KMS) que almacenaría el valor crudo de un secreto detrás de
  `CredentialBroker` — mismo tratamiento que `Protocol Adapter`/`Transport Adapter` (CH-15) o
  `Ingress Adapter` (CH-14): nombrado, nunca modelado en detalle.
- **Tenant Isolation of Credentials** *(lectura de `INV-E07`)*: la exigencia de que las credenciales
  de un tenant nunca sean visibles ni resolubles por otro — citada literalmente en este capítulo,
  sin que su mecanismo de enforcement se modele todavía (ver seccion 15/18).
- **Decision Ownership** *(Article IV, en uso desde CH-01, aplicado aquí por tercera vez a un
  componente de Amendment v1.1)*: `CredentialBroker` decide "¿qué credencial necesita esta
  implementación ya resuelta, y sigue siendo válida?"; explícitamente NO decide "¿está autorizada
  esta acción?" (`PolicyEngine`, CH-05), "¿qué implementación satisface esta capability?"
  (`CapabilityRegistry`, CH-08) ni "¿cómo se ejecuta el side effect en sí?" (`ToolRuntime`, CH-02).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen desde capítulos anteriores (no se redefinen aquí, solo se referencian por
nombre en el pseudocódigo de este capítulo): `AgentId`, `CapabilityId`, `Timestamp`, `Text`,
`Boolean`, `Optional`, `ExecutionContext` (C-004, CH-00), `AgentEvent` (C-010, CH-00), `HarnessError`
(C-011, CH-00), `CapabilityDescriptor` (C-018, CH-08).

### Un identificador opaco nuevo

Siguiendo el mismo patrón que CH-00 §6 estableció para los identificadores fundamentales, y que
CH-14/CH-15 repitieron para los suyos:

| Identificador (nuevo de este capítulo) | Identifica |
|---|---|
| `CredentialReferenceId` | una `CredentialReference` concreta — la referencia opaca al secreto que este capítulo resuelve |

### `ErrorCategory` — extendido, sin redefinir `HarnessError`

Este es el quinto capítulo que agrega un valor a `ErrorCategory` desde que CH-00 lo declaró (después
de `HUMAN_INTERACTION`, CH-06; `ADMISSION`, CH-14; y `DELEGATION`, CH-15): el valor `CREDENTIAL`,
necesario porque ninguna de las catorce categorías ya existentes representa, sin conflación, el
rechazo de una resolución de credencial por ausencia, vencimiento o mismatch de capability —
`VALIDATION` pertenece, en exclusiva, a fallos de forma/esquema de una intención de acción (CH-02/
CH-08), y reutilizarla aquí confundiría dos decisiones de dominios distintos:

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
END
```

`HarnessError` (C-011) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — mismo patrón
exacto que las extensiones de CH-06/CH-14/CH-15, aplicado aquí por cuarta vez a `ErrorCategory`.

### `AgentEventType` — extendido, sin redefinir `AgentEvent`

CH-10 dejó `AgentEventType` en veinte valores (CH-11 los reutilizó sin cambios; CH-14/CH-15 no lo
tocaron). Este capítulo agrega dos valores — los primeros eventos que observan la resolución de una
credencial, no la de una capability, un turno o una activación:

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
END
```

`AgentEvent` (C-010) no cambia: su `STRUCT` sigue siendo exactamente el de CH-00 — solo el rango de
valores permitido para `eventType` crece, igual que en cada capítulo anterior salvo `EventBus`
(CH-09), `AdmissionController` (CH-14) y `AgentCommunicationGateway` (CH-15).

### `CredentialClassification` — la materialización literal de `P-22`

```pseudocode
ENUM CredentialClassification
    CONFIDENTIAL
    RESTRICTED
END
```

**Por qué un `ENUM` de dos valores, y no un `Boolean isSensitive`.** Se evaluó explícitamente un
campo `Boolean` — más simple de construir. Se descartó por el mismo argumento que ya descartó
`allowAll: Boolean` para `DelegationGrant.delegatedScope` en CH-15 §6: no todos los secretos cargan
el mismo riesgo — una API key de solo lectura contra un servicio de bajo impacto no debería
gobernarse igual que un token administrativo con alcance destructivo — y un `Boolean` de dos estados
colapsaría esa diferencia real a un solo bit. `CredentialClassification` deja espacio, dentro del
alcance mínimo de este capítulo, para que un secreto declare cuál de los dos niveles le corresponde;
un esquema de clasificación más rico (con más niveles, o con residencia/lineage/legal-hold — el resto
de lo que `P-22` enumera) queda, deliberadamente, fuera de alcance de este capítulo (ver seccion 18).

### `CredentialReference` — la referencia opaca que exige `INV-E08`

```pseudocode
STRUCT CredentialReference
    id: CredentialReferenceId
    capability: CapabilityId
    credentialName: Text
    classification: CredentialClassification
    resolvedAt: Timestamp
    expiresAt: Optional<Timestamp>
END
```

Seis campos, cada uno respondiendo a una parte exacta del alcance decidido para este capítulo: `id`
identifica esta referencia de forma estable; `capability` es una referencia opaca — el mismo
`CapabilityId` que ya vive dentro de `CapabilityDescriptor.capability` (C-018, CH-08) — al
descriptor de capability al que pertenece este secreto (nunca el `CapabilityDescriptor` completo
embebido: una referencia por id evita que esta estructura cargue una copia que podría quedar
desactualizada respecto al registro real, el mismo argumento que ya usó `DelegationGrant.
delegatingRunId` como `Optional<RunId>` en vez de un `AgentRun` embebido, CH-15 §6);
`credentialName` es el nombre o scope del secreto (`Text`, p. ej. `"github-api-token"`) —
deliberadamente un nombre lógico, nunca el valor; `classification` es el nivel de gobierno que `P-22`
exige declarar explícitamente (sección anterior); `resolvedAt` registra cuándo `CredentialBroker`
resolvió esta referencia; `expiresAt` es `Optional<Timestamp>` — el vencimiento/rotación explícitos
que la lectura de `P-22` aplica a un secreto, cuando ese secreto los tiene.

**Por qué `CredentialReference` nunca tiene un campo con el valor del secreto — decisión de diseño
explícita y deliberada, no una omisión.** Se evaluó, y se descartó de inmediato, cualquier variante
que incluyera el secreto real dentro de este contrato — ni siquiera cifrado, ni siquiera como un
campo opcional "solo para casos de auditoría". La razón es estructural, no estilística: `INV-E08`
exige que un secreto "SHOULD NOT enter model context" — pero un contrato de este registry no vive
aislado, viaja por componentes, se serializa, puede terminar, eventualmente, dentro de un `payload`
de `AgentEvent` (seccion 14) o de cualquier estructura que un capítulo futuro construya para dar
contexto al modelo. Si `CredentialReference` transportara el secreto en cualquier forma, **cada**
componente que la reciba se convertiría, por diseño, en una superficie de fuga potencial — la
violación exacta que `INV-E08` prohíbe, multiplicada por cada lugar donde este contrato circule. Una
referencia estructuralmente incapaz de cargar el secreto es la única forma de que esa garantía se
sostenga sin depender de que cada componente futuro "recuerde" no filtrarlo.

**Por qué `expiresAt` es `Optional`, y no obligatorio como `DelegationGrant.expiresAt` (CH-15).** Se
evaluó exigir siempre una fecha de vencimiento, siguiendo el precedente de `DelegationGrant` — donde
`P-21` exige literalmente que toda autoridad delegada sea "time-bounded", sin excepción. `P-22` no
impone la misma exigencia universal sobre todo dato gobernado: clasificación, residencia, retención,
lineage, encriptación, borrado y legal-hold son, cada uno, aplicables según el tipo de dato y su
contexto regulatorio — no todo secreto tiene, necesariamente, una política de rotación explícita
todavía modelada por el sistema que lo emitió. Exigir `expiresAt` siempre habría inventado una
política de rotación que `P-22` nunca dijo que existiera universalmente; dejarlo `Optional` permite
que `resolveCredentialReference` (seccion 11) la aplique cuando existe, sin fabricar una cuando no.

**Unchanged / Not yet introduced**: `CapabilityDescriptor` (C-018) no cambia de forma — este capítulo
lo consume, nunca lo modifica. Ningún `STRUCT` para el secreto real, ni para el mecanismo de
alta/baja/rotación de un secreto en un Secret Store: primitivas asumidas, fuera de alcance (ver
seccion 18).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` de comportamiento todavía. Introduce un contrato de
datos, registrado en `registry/contracts.yaml`:

```text
ID:                     C-026
Name:                   CredentialReference
Version:                v1
Introduced In:          CH-16
Current Definition:     STRUCT CredentialReference (ver §6)
Used By:                [CMP-014]
Modified By:            []
Constitutional Impact:  [P-22, INV-E07, INV-E08]
```

`C-026` es el decimotercer id que este libro asigna sin que estuviera reservado desde CH-01 §7 — el
correlativo simplemente continúa después de `C-025` (CH-15). No colisiona, por nombre, con ningún
contrato ya registrado — verificado con grep completo sobre `registry/contracts.yaml` antes de
escribir este capítulo.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo introduce el tercer componente del registry que no corresponde a ninguno de los once
nombres del árbol de Article III ("Agent Runtime") — pertenece, en cambio, al "Capability &
Integration Plane" de Amendment v1.1:

```pseudocode
COMPONENT CredentialBroker
    consumes: CapabilityDescriptor, ExecutionContext
    produces: CredentialReference, AgentEvent, HarnessError
END
```

Ficha arquitectónica completa (`skills/define-component/SKILL.md`), citando literalmente
`constitution/ARCHITECTURE_CONSTITUTION.md` Amendment v1.1 (`INV-E08`/`INV-E07`/`P-22`) — Article
III no tiene, todavía, una sección propia para este componente, exactamente igual que
`AdmissionController` (CH-14) y `AgentCommunicationGateway` (CH-15):

```text
COMPONENT: CredentialBroker

Responsibility:
    Resolver, para una implementación de capability ya resuelta (CapabilityDescriptor, C-018,
    CH-08), la credencial que necesita para autenticarse contra el sistema externo real que
    envuelve — produciendo exclusivamente una CredentialReference opaca, nunca el valor real del
    secreto — y aplicar sobre ese secreto el gobierno de datos que P-22 exige (clasificación,
    rotación/expiración), sin decidir si la acción que esa implementación va a ejecutar está
    autorizada, sin decidir qué implementación satisface la capability solicitada y sin ejecutar el
    side effect en sí.

Consumes:
    C-018 CapabilityDescriptor, C-004 ExecutionContext

Depends on:
    (ninguno todavía — el cableado real hacia un Secret Store concreto, y hacia ToolRuntime para
    que la credencial resuelta llegue a la implementación antes de invocarla, es Preview, no
    introducido en este capítulo; ver seccion 9)

Produces:
    C-026 CredentialReference (la referencia opaca, lista para que un capítulo de integración
    futuro la entregue a la implementación real), C-010 AgentEvent (CREDENTIAL_RESOLVED /
    CREDENTIAL_RESOLUTION_FAILED), C-011 HarnessError

Owns (Amendment v1.1, `INV-E08`/`INV-E07`/`P-22`, cita y lectura literal):
    - "Credentials are resolved by a CredentialBroker and SHOULD NOT enter model context" (cita
      literal, INV-E08)
    - "Tenant data, memory, credentials, artifacts and audit records are isolated" (cita literal,
      INV-E07, aplicada específicamente a credenciales)
    - aplicar sobre un secreto el gobierno de datos que P-22 exige — clasificación explícita
      (CredentialReference.classification) y rotación/expiración explícitas
      (CredentialReference.expiresAt) — cuando ese secreto las declara
    - verificar que el secreto solicitado corresponda a la capability ya resuelta, exista y no haya
      vencido, antes de producir cualquier CredentialReference
    - rechazar por defecto (fail-closed) cuando el secreto no corresponde, no existe o ya venció —
      nunca dejar pasar una resolución ambigua
    - garantizar, por construcción del propio contrato (CredentialReference, seccion 6), que el
      valor real del secreto nunca aparezca en ningún dato que este componente produce

Does NOT own:
    - decidir si la acción/ToolCall ya resuelta que la implementación va a ejecutar está autorizada
      (PolicyEngine, CMP-005, ya introducido en CH-05 — distinta pregunta, distinto momento: "con
      qué se autentica" nunca es "si está permitido")
    - resolver qué implementación satisface una capability solicitada (CapabilityRegistry, CMP-008,
      ya introducido en CH-08 — este componente actúa DESPUÉS: recibe un CapabilityDescriptor ya
      resuelto, nunca vuelve a decidir cuál es la implementación correcta)
    - ejecutar el side effect en sí, incluyendo la autenticación real contra el sistema externo con
      la credencial ya resuelta (ToolRuntime, CMP-002, ya introducido en CH-02 — CredentialBroker
      produce la referencia; ToolRuntime.executeToolCall obteniendo esa referencia y pasándola a la
      implementación real antes de invocarla es trabajo de un capítulo de integración futuro, ver
      seccion 9/18)
    - el mecanismo real de almacenamiento, cifrado o rotación física del secreto (Secret Store —
      infraestructura de borde, no un componente propio de este registry, mismo tratamiento que
      Protocol Adapter/Transport Adapter, CH-15, o Ingress Adapter, CH-14)
    - decidir si otro turno de razonamiento debe ocurrir (AgentLoop, CMP-001, ya introducido en
      CH-01)
```

`does_not_own` se declara con el mismo peso que `owns` (Article IV, Ownership Rule) — con la misma
particularidad que `AdmissionController`/`AgentCommunicationGateway`: ninguna de las cinco
exclusiones proviene de una ficha propia de Article III (que no existe para este componente);
provienen de fronteras ya establecidas por Amendment v1.1 (`INV-E07`) o por componentes ya
registrados (`PolicyEngine`, `CapabilityRegistry`, `ToolRuntime`, `AgentLoop`).

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
CredentialBroker
    consumes → CapabilityDescriptor, ExecutionContext
    produces → CredentialReference, HarnessError
    depends on (componentes) → (ninguno registrado todavía)
```

`CredentialBroker` no depende hoy de ningún otro componente registrado — mismo patrón que CH-01..
CH-15 ya establecieron para sus propios componentes. En prosa (nunca dentro de un bloque
`pseudocode`, per `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §22 regla 8), las relaciones
futuras que un capítulo de integración agregaría son:

| Componente futuro (relación inversa — no cableada en este capítulo) | Qué relación tendría con `CredentialBroker` |
|---|---|
| `CapabilityRegistry` (ya existente, CMP-008) | produciría el `CapabilityDescriptor` que este componente consume — hoy `resolveCredentialReference` (seccion 11) recibe ese descriptor ya armado, como demostración autónoma |
| `ToolRuntime` (ya existente, CMP-002) | **`ToolRuntime.executeToolCall` obtendría la credencial resuelta antes de invocar la implementación** — el cableado exacto que este capítulo deja explícitamente para un capítulo de integración futuro, sin tocar una sola línea del `executeToolCall` ya publicado en CH-02 |
| `PolicyEngine` (ya existente, CMP-005) | seguiría decidiendo, sin cambios, si el `ToolCall` que la implementación ejecutaría está autorizado — una pregunta completamente anterior e independiente de con qué credencial se autentica |
| Un Secret Store concreto (todavía sin componente propio en este registry) | almacenaría, cifraría y rotaría el valor real del secreto detrás de `CredentialBroker` — infraestructura de borde, `INV-E08`, fuera de este registry |

`registry/components.yaml` de `CMP-002` (`ToolRuntime`), `CMP-005` (`PolicyEngine`) y `CMP-008`
(`CapabilityRegistry`) **no se modifica** en este capítulo: ninguno agrega `CMP-014` a sus
`dependencies`, y ninguno cambia su pseudocódigo. El pseudocódigo de la seccion 11 evalúa un
`CapabilityDescriptor` de ejemplo de forma completamente autónoma — sin que ninguno de los tres
componentes ya existentes cambie una sola línea para que este capítulo sea correcto. Ese cableado
real es, explícitamente, trabajo de un capítulo de integración futuro (ver seccion 18/19).

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§14):

**Vista 1 — Componentes**

```text
[CapabilityRegistry — produce CapabilityDescriptor, CH-08, conceptual] → CredentialBroker →
[Secret Store — infraestructura de borde, fuera de este registry] →
[ToolRuntime — obtendría la CredentialReference antes de invocar la implementación real, CH-02,
 conceptual]
```

**Vista 2 — Sequence**

```text
CapabilityDescriptor
   │ (ya resuelto por CapabilityRegistry, CH-08 — implementationRef opaco)
   ▼
CredentialBroker
   │ resolveCredentialReference(descriptor, credentialName, classification,
   │                            credentialBelongsToCapability, secretExists, expiresAt,
   │                            execution, agentId)
   │ ¿credentialBelongsToCapability? no → HarnessError (CREDENTIAL_CAPABILITY_MISMATCH)
   │ ¿secretExists? no → HarnessError (CREDENTIAL_NOT_FOUND)
   │ ¿expiresAt != NULL AND now() > expiresAt? sí → HarnessError (CREDENTIAL_EXPIRED)
   │ construye CredentialReference (nunca incluye el secreto real)
   │ emite: AgentEvent (CREDENTIAL_RESOLVED | CREDENTIAL_RESOLUTION_FAILED)
   ▼
CredentialReference (la referencia opaca, nunca el secreto)
   │
   │ ... integración futura: ToolRuntime.executeToolCall (CH-02) obtiene esta referencia y la
   │     entrega a la implementación real antes de invocarla — la implementación resolvería el
   │     valor real contra un Secret Store (Preview, fuera de este registro) usando esta referencia,
   │     nunca al revés ...
```

**Vista 3 — Pseudocódigo**

Ver §11: `resolveCredentialReference` es la primera formalización ejecutable de "ningún secreto
entra al contexto del modelo" (`INV-E08`) — construida exclusivamente a partir de material que ya
existe (`CapabilityDescriptor` desde CH-08, `HarnessError`/`ExecutionContext`/`AgentEvent` desde
CH-00) más el contrato y el `ENUM` nuevos de este capítulo.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6/§7 de este capítulo o registradas desde CH-00/CH-08.

```pseudocode
FUNCTION resolveCredentialReference(
    descriptor: CapabilityDescriptor,
    credentialName: Text,
    classification: CredentialClassification,
    credentialBelongsToCapability: Boolean,
    secretExists: Boolean,
    expiresAt: Optional<Timestamp>,
    execution: ExecutionContext,
    agentId: AgentId
) -> CredentialReference

    IF NOT credentialBelongsToCapability
        mismatched: HarnessError = HarnessError(
            category = CREDENTIAL,
            code = "CREDENTIAL_CAPABILITY_MISMATCH",
            message = "El credentialName solicitado no corresponde a la capability descrita por este CapabilityDescriptor",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )

        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = CREDENTIAL_RESOLUTION_FAILED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = mismatched
        )

        THROW mismatched
    END

    IF NOT secretExists
        notFound: HarnessError = HarnessError(
            category = CREDENTIAL,
            code = "CREDENTIAL_NOT_FOUND",
            message = "CredentialBroker no encontró ningún secreto registrado para este credentialName",
            recoverable = TRUE,
            retryable = FALSE,
            metadata = {}
        )

        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = CREDENTIAL_RESOLUTION_FAILED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = notFound
        )

        THROW notFound
    END

    IF expiresAt != NULL AND now() > expiresAt
        expired: HarnessError = HarnessError(
            category = CREDENTIAL,
            code = "CREDENTIAL_EXPIRED",
            message = "El secreto que respaldaría esta CredentialReference ya superó su expiresAt",
            recoverable = TRUE,
            retryable = FALSE,
            metadata = {}
        )

        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = CREDENTIAL_RESOLUTION_FAILED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = expired
        )

        THROW expired
    END

    reference: CredentialReference = CredentialReference(
        id = newCredentialReferenceId(),
        capability = descriptor.capability,
        credentialName = credentialName,
        classification = classification,
        resolvedAt = now(),
        expiresAt = expiresAt
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = CREDENTIAL_RESOLVED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = reference
    )

    RETURN reference
END
```

`now()`, `newEventId()` y `newCredentialReferenceId()` son las mismas primitivas de CH-00/CH-14/
CH-15. `credentialBelongsToCapability`, `secretExists` y `expiresAt` son señales de entrada — igual
que `capabilityResolved`/`inputValid` en CH-02 §11 o `argumentsMatchSchema` en CH-08 §11 — que un
Secret Store real (Preview, fuera de este registry) produciría en la práctica: `resolveCredentialReference`
no calcula ninguna de las tres, las recibe y decide, determinísticamente, qué `CredentialReference` o
qué `HarnessError` construir a partir de ellas.

**Por qué este capítulo verifica `credentialBelongsToCapability` como primer chequeo, antes que
`secretExists`.** Verificar primero la pertenencia a la capability, y solo después la existencia del
secreto, evita una fuga de información por canal lateral: si el orden fuera inverso, un llamador
podría inferir, a partir de cuál de los dos errores recibe, si un `credentialName` existe en el
Secret Store en términos absolutos — incluso para una capability a la que nunca debería pertenecer.
Verificar primero la pertenencia asegura que un secreto ajeno a esta capability se rechace siempre
con el mismo código (`CREDENTIAL_CAPABILITY_MISMATCH`), exista o no.

Nótese también lo que `resolveCredentialReference` **no** hace: no invoca `PolicyEngine.
evaluatePolicyForToolCall` (CH-05) ni `CapabilityRegistry.resolveToolCall` (CH-08); no invoca
`ToolRuntime.executeToolCall` (CH-02) ni ejecuta ningún side effect; y — a diferencia de
`authorizeAgentCommunicationMessage` (CH-15 §11) — sí emite un `AgentEvent` en cada rama, porque a
diferencia de ese capítulo, aquí `ExecutionContext` ya trae `runId`/`sessionId`/`traceId` completos
(ver seccion 14).

## 12. Transiciones de Estado (State Transitions)

Este capítulo no introduce ni modifica `AgentRunStatus` (C-013): sigue siendo, sin cambios, el mismo
`ENUM` de once estados que `AgentLoop` (CH-01) formalizó. `CredentialReference` no tiene,
deliberadamente, ningún `ENUM` de estados propio — mismo patrón que `DelegationGrant` (CH-15 §12) ya
estableció: se evalúa de forma síncrona, y su vigencia se deriva, en cada evaluación, exclusivamente
de comparar `now()` contra `expiresAt` — nunca de una transición persistida `ACTIVE → EXPIRED` con su
propio `STRUCT`.

```text
(resolveCredentialReference, CapabilityDescriptor recibido)
   → credentialBelongsToCapability == FALSE
     (el credentialName solicitado no pertenece a esta capability; nunca se llega a verificar
     existencia ni vigencia — HarnessError, categoría CREDENTIAL)

   → credentialBelongsToCapability == TRUE, secretExists == FALSE
     (el secreto no está registrado en el Secret Store asumido — HarnessError, categoría CREDENTIAL)

   → credentialBelongsToCapability == TRUE, secretExists == TRUE, expiresAt != NULL, now() >
     expiresAt
     (el secreto existía y pertenecía a esta capability, pero ya venció — HarnessError, categoría
     CREDENTIAL)

   → credentialBelongsToCapability == TRUE, secretExists == TRUE, expiresAt == NULL O now() <=
     expiresAt
     (CredentialReference producida — opaca, lista para que un capítulo de integración futuro la
     entregue a la implementación real, nunca al modelo)
```

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (heredado de CH-00 §6, extendido en la seccion 6 de este capítulo) clasifica también
los tres fallos reales que introduce este capítulo:

```text
CREDENTIAL
    CREDENTIAL_CAPABILITY_MISMATCH  — el credentialName solicitado no corresponde a la capability
                                      descrita por el CapabilityDescriptor recibido
        → recoverable: FALSE, retryable: FALSE
    CREDENTIAL_NOT_FOUND            — ningún secreto registrado corresponde a este credentialName
        → recoverable: TRUE, retryable: FALSE
    CREDENTIAL_EXPIRED              — el secreto que respaldaría esta CredentialReference ya superó
                                      su expiresAt
        → recoverable: TRUE, retryable: FALSE
```

`CREDENTIAL_CAPABILITY_MISMATCH` es `recoverable = FALSE` (un mismatch de nombre/capability es un
error de configuración o de código, no algo que se corrija reintentando ni rotando un secreto) y
`retryable = FALSE`. `CREDENTIAL_NOT_FOUND` y `CREDENTIAL_EXPIRED` son `recoverable = TRUE` (el
problema es corregible — provisionar o rotar el secreto correspondiente resolvería cualquiera de los
dos) pero `retryable = FALSE` (reintentar exactamente la misma resolución fallaría de forma idéntica)
— mismo razonamiento exacto que `DELEGATION_GRANT_EXPIRED` (CH-15) ya estableció para su propio
fail-closed.

**La distinción más importante de esta sección**: ninguno de los tres fallos se clasifica como
`category = VALIDATION` — aunque `CREDENTIAL_CAPABILITY_MISMATCH` podría, a primera vista, parecer
un problema de forma/esquema. `VALIDATION` (CH-02/CH-08) pertenece, en exclusiva, a fallos sobre la
forma de una intención de acción ya resuelta (`ToolCall`) — una pregunta sobre argumentos y schemas,
nunca sobre qué secreto autentica un sistema. Reutilizar `VALIDATION` aquí habría conflacionado dos
decisiones de dos componentes distintos, exactamente el error que Article IV (Ownership Rule)
prohíbe — el mismo argumento que ya usaron CH-14 §6 (para no reutilizar `POLICY`) y CH-15 §13 (para
no reutilizar `BUDGET`).

Lo que este capítulo **deliberadamente no clasifica**: cualquier fallo de `category = INFRASTRUCTURE`
que pudiera ocurrir en un Secret Store real (por ejemplo, un vault completamente inalcanzable) — ese
valor de `ErrorCategory` sigue, después de este capítulo, sin que ningún componente real lo haya
ejercitado nunca (mismo límite que CH-11 §13/CH-14 §13/CH-15 §13 ya documentaron para sus propias
primitivas asumidas).

## 14. Eventos Producidos (Events Produced)

**A diferencia de los dos componentes de Amendment v1.1 que lo precedieron** (`AdmissionController`,
CH-14; `AgentCommunicationGateway`, CH-15 — ambos, por razones distintas, nunca construyen un
`AgentEvent` real), `CredentialBroker` **sí** produce eventos reales: agrega `CREDENTIAL_RESOLVED` y
`CREDENTIAL_RESOLUTION_FAILED` a `AgentEventType` (seccion 6), y `resolveCredentialReference`
(seccion 11) los emite en cada rama de resolución.

**Por qué este componente sí puede emitir, cuando los dos anteriores no podían.** `AdmissionController`
(CH-14) no podía: ninguno de los cuatro campos obligatorios de `AgentEvent` (`runId`, `sessionId`,
`agentId`, `traceId`) existía todavía en el momento de su decisión. `AgentCommunicationGateway`
(CH-15) tampoco podía: `AgentCommunicationMessage` deliberadamente no tiene ningún campo `sessionId`.
`CredentialBroker` está en una situación distinta, la misma que `CapabilityRegistry` (CH-08): cuando
una implementación de capability ya resuelta necesita una credencial, el `AgentRun` que la necesita
ya existe, con `ExecutionContext` completo (`runId`/`sessionId`/`traceId`) — no hay ningún campo
faltante que fabricar ni que silenciar.

**Por qué emitir este evento nunca compromete `INV-E08`.** El `payload` de `CREDENTIAL_RESOLVED` es
siempre la `CredentialReference` misma — opaca por construcción, sin ningún campo capaz de
transportar el secreto real (seccion 6) — y el de `CREDENTIAL_RESOLUTION_FAILED` es el `HarnessError`
correspondiente, que tampoco lo transporta. Emitir telemetría operacional sobre **que** una
resolución ocurrió, y sobre **qué** referencia opaca produjo, no es lo mismo que exponer **el valor**
que esa referencia representa — la misma distinción, aplicada aquí a eventos en vez de a contexto de
modelo, que sostiene todo el diseño de `CredentialReference`.

**Lo que este capítulo no resuelve (relación con `P-25`).** Una auditoría completa de "quién accedió
a qué credencial, cuándo y desde qué run" necesitaría, per `P-25` ("Audit evidence is distinct from
operational telemetry"), algo más que `AgentEvent`/`EventBus` (Article X) — un mecanismo de evidencia
inmutable, distinto de la telemetría operacional que este capítulo sí produce. Ese mecanismo no se
construye aquí (mismo límite, honestamente señalado, que CH-14 §14 y CH-15 §14 ya documentaron cada
uno para su propio contrato).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

`CredentialBroker` es el primer componente de este libro cuya responsabilidad completa es resolver
—sin exponerlo jamás— un secreto real que autentica un sistema contra otro.

**La distinción con `PolicyEngine` (CH-05), explícita y completa.** `PolicyEngine.
evaluatePolicyForToolCall` (CH-05) decide si una acción ya resuelta puede ejecutarse — una pregunta
que se responde por completo sin necesitar saber jamás con qué credencial concreta se autenticaría
esa acción. `CredentialBroker.resolveCredentialReference` (este capítulo) decide qué credencial usar,
asumiendo que la autorización ya fue concedida (o está a punto de evaluarse por otro camino) — nunca
vuelve a evaluar si la acción está permitida. Un `ToolCall` puede estar perfectamente autorizado y,
aun así, no tener ninguna credencial válida disponible (`CREDENTIAL_NOT_FOUND`/`CREDENTIAL_EXPIRED`)
— y, a la inversa, una credencial puede resolverse sin problema para una acción que `PolicyEngine`
terminaría rechazando. Son, literalmente, preguntas independientes, con dueños independientes — la
misma lógica constitucional que `P-13` ya aplicó, desde CH-05, a la autorización, aplicada aquí por
segunda vez a la credencial misma: el modelo nunca decide autorización, y el modelo tampoco decide,
ni ve, con qué secreto se autentica un sistema.

**La distinción con `CapabilityRegistry` (CH-08), explícita y completa.** `CapabilityRegistry.
resolveToolCall` (CH-08) decide qué implementación satisface una capability solicitada, produciendo
un `CapabilityDescriptor` con un `implementationRef` opaco. `CredentialBroker` actúa **después**:
recibe ese descriptor como un hecho ya resuelto y nunca vuelve a preguntarse cuál es la
implementación correcta — solo qué necesita esa implementación, ya identificada, para autenticarse.
Si un `CapabilityDescriptor` llegara sin haber pasado nunca por una resolución real de
`CapabilityRegistry`, ese sería un hueco de una frontera **anterior y distinta** (ver `IQ-CH16-01`,
frontmatter), nunca una responsabilidad de `CredentialBroker` — exactamente el mismo cuidado de
límites que CH-14 §15/CH-15 §15 ya aplicaron frente a sus propios vecinos.

**`INV-E08`, aplicado con cuidado.** Ningún `STRUCT`/`ENUM`/`FUNCTION` de este capítulo modela el
valor real de un secreto como dato manipulable — `CredentialReference` es, por construcción,
incapaz de transportarlo (seccion 6). Esto es, literalmente, lo que hace posible que `INV-E08` se
cumpla por diseño del propio contrato, no solo por disciplina operacional: si `CredentialReference`
tuviera un campo `value` o `secretValue`, cualquier componente futuro que la reciba —incluyendo,
eventualmente, algo que ensamble contexto para el modelo— se convertiría en una vía real de fuga.

**`INV-E07`, citado y no todavía implementado.** Este capítulo cita literalmente "tenant data,
memory, credentials, artifacts and audit records are isolated" como parte del `owns` de
`CredentialBroker` — pero el mecanismo real de aislamiento por tenant (qué campo declara el tenant de
una `CredentialReference`, cómo se enforcea que un tenant nunca resuelva la credencial de otro) no se
modela en este capítulo. Señalado explícitamente como límite real, no silenciado (ver seccion 18).

**Lo que este capítulo NO implementa todavía.** Ningún Secret Store real (vault, KMS, secret
manager); ningún mecanismo real de rotación automática detrás de `expiresAt`; ningún cableado real
entre `CredentialBroker` y `ToolRuntime.executeToolCall` para que la implementación real reciba la
`CredentialReference` antes de ejecutarse; ningún esquema de clasificación más rico que
`CredentialClassification` de dos valores (residencia, lineage, legal-hold — el resto de lo que
`P-22` enumera).

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md`
§28):

```text
TEST CredentialBrokerRejectsACredentialThatDoesNotBelongToTheResolvedCapability
TEST CredentialBrokerRejectsAMissingCredential
TEST CredentialBrokerRejectsAnExpiredCredential
TEST CredentialBrokerResolvesAValidCredentialIntoAnOpaqueReference
TEST CredentialReferenceNeverContainsTheRawSecretValue
TEST CredentialBrokerNeverEvaluatesToolCallAuthorization
TEST CredentialBrokerNeverResolvesWhichImplementationSatisfiesACapability
TEST CredentialBrokerEmitsAnAgentEventOnEveryResolutionWithoutLeakingTheSecret
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (después de CH-16 — tercer plano de Amendment v1.1 cubierto por este libro)

Constitution
 ├── Article III  — Component Sovereignty (once componentes de "Agent Runtime", sin cambios desde
 │                   CH-11)
 ├── Article IV   — Decision Ownership (tabla original sin cambios; CredentialBroker documentado en
 │                   prosa, igual que AdmissionController/AgentCommunicationGateway)
 └── Amendment v1.1 — Enterprise Activation, Interoperability and Operations
                       (P-22/INV-E07/INV-E08 citados por primera vez con código real; Ingress &
                       Activation Plane, CH-14, Agent Interoperability Plane, CH-15, y Capability &
                       Integration Plane, este capítulo, los tres primeros de nueve planos
                       canónicos instalados)

Contracts (registry/contracts.yaml)
 ├── C-001..C-025  (sin cambios — CH-00..CH-15)
 └── C-026 CredentialReference  (CH-16, nuevo — la referencia opaca al secreto que una
                                 implementación ya resuelta necesita, P-22/INV-E07/INV-E08)

Components (registry/components.yaml)
 ├── CMP-001..CMP-013  (sin cambios — CH-01..CH-15)
 └── CMP-014 CredentialBroker  (CH-16, nuevo — tercer componente de este registry que no
                                corresponde a ninguno de los once nombres de Article III;
                                pertenece al Capability & Integration Plane de Amendment v1.1)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El cableado real `CapabilityRegistry → CredentialBroker → ToolRuntime → implementación`**:
  ningún componente invoca todavía `resolveCredentialReference` seguido de una entrega real de la
  `CredentialReference` a la implementación — el propio encargo de este capítulo señala,
  explícitamente, que "`ToolRuntime.executeToolCall` obtiene la credencial resuelta antes de invocar
  la implementación" es trabajo de un capítulo de integración futuro; ese cableado sigue sin
  construirse.
- **El Secret Store real** (vault, KMS, secret manager): infraestructura de borde, no modelada —
  mismo tratamiento que `Protocol Adapter`/`Transport Adapter` (CH-15) o `Ingress Adapter` (CH-14).
- **El mecanismo real de rotación automática** detrás de `CredentialReference.expiresAt`: este
  capítulo verifica que una fecha de vencimiento no haya pasado, pero no modela ningún proceso que
  rote un secreto antes de que eso ocurra.
- **El aislamiento real por tenant** (`INV-E07`, "credentials... are isolated"): citado
  explícitamente en el `owns` de `CredentialBroker` (seccion 8), sin que este capítulo modele qué
  campo declara el tenant de una `CredentialReference` ni cómo se enforcea, en la práctica, que un
  tenant nunca resuelva la credencial de otro.
- **Un esquema de clasificación más rico** que `CredentialClassification` de dos valores: residencia,
  retención con ventana explícita, lineage, encriptación y legal-hold — el resto de lo que `P-22`
  enumera para *cualquier* dato empresarial gobernado, no solo credenciales — queda fuera de alcance;
  ese trabajo pertenece, con mayor propiedad, a un capítulo futuro del "Data & Context Plane"
  (Amendment v1.1, quinto plano canónico).
- **La emisión real de un secreto hacia un Secret Store en primer lugar**: quién provisiona
  `secretExists = TRUE` para un `credentialName` dado, y con qué autoridad — asumido, no modelado
  (mismo límite que CH-08 §18 documentó para el alta/baja de un `CapabilityDescriptor`).
- **Ausencia de evidencia de auditoría real** (`P-25`) para una `CredentialReference` resuelta:
  señalado explícitamente (seccion 14), no silenciado.
- **El Execution Plane completo** (segundo plano canónico, todavía sin cubrir) y **los seis planos
  restantes** de Amendment v1.1 (Data & Context, Control, Reliability, Observability & Governance,
  Execution Fabric, y la profundización del Capability & Integration Plane más allá de este primer
  componente): explícitamente fuera de alcance.
- Reviewers plurales, evals y orquestación multi-agente propiamente dicha: explícitamente fuera de
  alcance de BH-v0.1.

## 19. Siguiente Incremento (Next Increment)

Con este capítulo, el "Capability & Integration Plane" de Amendment v1.1 tiene su primer componente
real — pero el plano completo (el Secret Store real, el cableado real hacia `ToolRuntime`, el
aislamiento por tenant que `INV-E07` exige) sigue sin construirse de punta a punta. El problema
natural del próximo incremento es, o bien profundizar este mismo plano (cableando por fin
`CredentialBroker` dentro de `ToolRuntime.executeToolCall`), o bien retroceder a cubrir el Execution
Plane (el segundo plano canónico, todavía sin cubrir), o bien avanzar hacia cualquiera de los cinco
planos restantes que Amendment v1.1 enumera junto a estos — Data & Context Plane, con su propio
`P-22` completo (residencia, lineage, legal-hold) más allá de lo que este capítulo ya materializó
para credenciales, es un candidato particularmente natural.

`next_chapter` queda en `null` en el frontmatter de este capítulo porque, en este momento del libro,
ese próximo capítulo todavía no existe como archivo — solo como el problema que motivaría su
escritura.

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de la
> secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco Iceberg / Bucles
> de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas, Forrester/Meadows),
> secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): dieciséis capítulos reales construyeron un runtime
   completo más dos componentes de Enterprise, pero ninguno modeló jamás cómo una implementación de
   capability ya resuelta obtiene el secreto que necesita para autenticarse contra un sistema
   externo real.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): Amendment v1.1 nombra
   literalmente `CredentialBroker` desde que fue adoptada; CH-14 y CH-15 ya lo mencionaron, dos veces
   seguidas, entre los componentes explícitamente diferidos, y `P-22` ya fue citado en prosa dos
   veces sin materializarse jamás con código real.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities): este capítulo instala
   `CredentialBroker` con una ficha que declara tanto lo que posee (`owns`: resolver la credencial
   que una implementación ya resuelta necesita, sin exponerla jamás; aplicar clasificación y
   rotación/expiración) como lo que explícitamente NO posee (autorización de la acción, resolución
   de qué implementación satisface una capability, ejecución del side effect en sí).
4. **Modelos mentales** (= §4, Constitutional Impact): "¿con qué se autentica un sistema?" es una
   pregunta completamente distinta de "¿está permitida esta acción?" y de "¿qué implementación la
   satisface?" — tres preguntas con dueños distintos que, sin este componente, corrían el riesgo de
   resolverse todas en el mismo lugar.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que un sistema deja sin modelar cómo una implementación
  obtiene sus credenciales, el secreto crudo termina incrustado donde sea más conveniente —
  hardcodeado, o expuesto al propio contexto del modelo — el mismo bucle que `P-02`/`P-19` ya
  combatieron para el modelo y para el protocolo, ahora aplicado al secreto.
- **Bucle de equilibrio (estabiliza):** `resolveCredentialReference` (§11) nunca devuelve el secreto
  real — solo una referencia opaca — y rechaza, con un `HarnessError` categorizado, cualquier
  solicitud sobre un secreto ausente, ajeno a la capability o ya vencido.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `CredentialReference` (C-026) sea
estructuralmente incapaz de transportar el valor real del secreto que representa — ni un solo campo
del contrato lo permite. Si `CredentialReference` transportara el secreto en cualquier forma, cada
componente que la reciba se convertiría, por diseño, en una superficie de fuga — la violación exacta
que `INV-E08` prohíbe.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado completo de
> esta sección (con ids estables para cada pregunta/tarjeta) vive en `retrieval_set` (frontmatter) y
> es lo que `scripts/validate-retrieval-set` valida. Aquí se presenta en prosa, para lectura directa
> del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. Cuando una implementación de capability ya resuelta necesita autenticarse contra un sistema
   externo real, ¿quién decide qué secreto usa, y cómo se garantiza que ese valor nunca llegue al
   contexto del modelo? *(cierra la pregunta guía 1)*
2. La decisión de si una acción ya resuelta está autorizada ya tiene un dueño. ¿Esa misma pregunta
   sirve para decidir con qué secreto se autentica un sistema? *(cierra la pregunta guía 2)*
3. Si un secreto tiene fecha de vencimiento o necesita rotarse, ¿qué debería pasar al intentar usar
   una referencia ya vencida? *(cierra la pregunta guía 3)*
4. Un secreto es, en sí mismo, un dato empresarial con sensibilidad real. ¿Necesita el mismo tipo de
   gobierno explícito que cualquier otro dato gobernado? *(cierra la pregunta guía 4)*

### Explicar

1. `CredentialBroker` posee resolver la credencial que una implementación ya resuelta necesita.
   Explica, como si hablaras con alguien sin contexto técnico, por qué NO posee decidir si la acción
   que esa implementación va a ejecutar está autorizada.
2. `CredentialReference` nunca transporta el valor real del secreto. Explica qué perderíamos, y qué
   riesgo nuevo introduciríamos, si en vez de una referencia opaca este contrato incluyera
   directamente el secreto.

### Conectar

1. `CapabilityRegistry` (CH-08) ya resuelve qué implementación satisface una capability, produciendo
   un `CapabilityDescriptor` con un `implementationRef` opaco. ¿Le corresponde a este capítulo volver
   a decidir cuál es la implementación correcta, o asume esa resolución como ya cerrada?
2. `PolicyEngine` (CH-05) ya decide si un `ToolCall` está autorizado. ¿Alcanza con que la
   implementación use cualquier secreto que tenga a mano una vez autorizada la acción, o la pregunta
   de qué credencial exacta usar sigue teniendo un dueño distinto?

### Espaciar

Las cinco tarjetas de repaso de este capítulo (dos sobre `CredentialBroker` — su `owns` y su
`does_not_own` —, dos sobre `CredentialReference` — sus campos y su clasificación —, y una sobre por
qué este componente sí produce eventos reales) entran hoy en `reviewStage = DAY_1`. Repásalas de
nuevo al día 3, al día 7 y al día 21 (curva de Ebbinghaus) — ver el apéndice de tarjetas al final del
libro (edición PDF) o `retrieval_set.flashcards` en `dist/book-ir.json` (edición Web).

### Calibrar

Antes de revisar tus respuestas de "Recordar", califica tu confianza en cada una — Alta / Media /
Baja — y solo entonces compárala con el texto del capítulo. Si calificaste "Alta" y te equivocaste,
ese es precisamente el punto ciego que este método existe para revelar.
