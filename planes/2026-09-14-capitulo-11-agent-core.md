# Plan / Registro de ejecución — Capítulo 11: AgentCore y el Nacimiento de un AgentState

**Fecha:** 2026-09-14
**Estado:** ✅ Completado, sobre el estado dejado por `d693592` (CH-00..CH-10 como los once únicos
capítulos reales; de los once nombres de Article III, solo `AgentCore` seguía en preview,
mencionado literalmente por `INV-01`/`INV-16` desde CH-00 sin que ningún componente real lo
materializara).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-13-capitulo-01-agent-loop.md` (origen de `AgentState`/`AgentConfig`, y del guard de
  `runTurn` que este capítulo reexamina con cuidado)
- `2026-09-14-capitulo-10-session-manager.md` (capítulo más reciente antes de este,
  formato/estilo de referencia; deja documentado que `AgentCore` es el único nombre de Article III
  todavía en preview)
- `2026-09-14-capitulo-03-model-gateway.md` (precedente de cómo citar un invariante que nombra
  literalmente a `AgentCore` — `INV-01` — antes de que el componente existiera)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Article III "AgentCore", Article IV — tabla sin
  fila para `AgentCore`, Article V — Lifecycle, `INV-01`/`INV-16`, Amendment v1.1 `P-16`/`P-17`
  "Enterprise Activation")

---

## 1. Objetivo

Escribir el duodécimo capítulo real de contenido del libro ("¿Cómo construir un arnés?"), CH-11,
sobre `AgentCore` — el último de los once componentes de Article III que faltaba, y el que cierra
un hueco estructural real: ningún capítulo anterior había mostrado nunca cómo nace un `AgentState`
(`AgentLoop.runTurn`, CH-01, siempre lo recibe ya existente como parámetro). Verificar que el
capítulo atraviesa todo el pipeline (validadores + BookIR + Web + PDF + Mapa Mental) sin romper
nada de lo que CH-00..CH-10 ya tenían construido.

## 2. Alcance decidido (Paso 2 del encargo, ya cerrado antes de escribir)

Exactamente 1 componente + 1 contrato:

1. **Componente `AgentCore` (CMP-011)** — undécimo y último componente de runtime de Article III.
   `owns` (cita literal de Article III, más la lectura concreta de este capítulo): representar y
   coordinar las primitives fundamentales del agente; representar la identidad/definición del
   agente, independiente de cualquier run o sesión particular; validar un `AgentConfig` antes de
   que arranque cualquier ejecución; instanciar el `AgentState` inicial de un nuevo run (asignar
   `runId`, decidir `sessionId`); la transición `CREATED → INITIALIZING` (Article V). `does_not_own`
   (las cuatro exclusiones literales de Article III + las fronteras ya establecidas por otros
   componentes): UI (`INV-16`), persistencia específica (`SessionManager`, CMP-010, CH-10),
   proveedores (`ModelGateway`, CMP-003, CH-03 — `INV-01`), business integrations (sin componente
   propio, fuera de alcance genérico), decidir continuación de turno una vez `RUNNING`
   (`AgentLoop`, CMP-001, CH-01 — `AgentCore` entrega el testigo, no compite). `consumes`: `C-002
   AgentConfig`, `C-012 ExecutionBudget`, `C-021 AgentActivationRequest`; `produces`: `C-003
   AgentState`, `C-004 ExecutionContext`, `C-010 AgentEvent`, `C-011 HarnessError`.
2. **Contrato nuevo `AgentActivationRequest` (C-021)** — la solicitud de activar/crear un nuevo run
   de un agente ya configurado: `agentId` (`AgentId`), `sessionId` (`Optional<SessionId>` — `NULL`
   si es una sesión nueva, poblado si se adjunta a una ya trackeada por `SessionManager`), `input`
   (`Value`, el objetivo/input inicial) y `requestedAt` (`Timestamp`).
3. **Pseudocódigo del capítulo**: `activateAgent(request: AgentActivationRequest) -> AgentState`
   (valida que el `AgentConfig` referenciado exista y que su `ExecutionBudget` sea coherente,
   genera un `runId` nuevo, decide `sessionId`, produce el `AgentState` inicial con `status =
   CREATED`) y `beginAgentInitialization(state, config) -> AgentState` (transiciona `CREATED →
   INITIALIZING` — el primer ejercicio real de esa transición de Article V — construyendo el
   primer `ExecutionContext` real del libro y emitiendo `RUN_STARTED` por primera vez). Termina
   explícitamente donde `AgentLoop.runTurn` (CH-01) retoma, sin tocar su código.
4. No se tocó `book/chapters/00-*` a `09-*`; de CH-10 solo se tocó `next_chapter: null → CH-11` en
   el frontmatter.
5. `book/book.yaml` agrega CH-11 después de CH-10; CH-11 frontmatter → `previous_chapter: CH-10`,
   `next_chapter: null`.
6. `retrieval_set` de CH-11 incluye 2 `interleavedQuestions`: una conectando con CH-01 (`AgentLoop`/
   `AgentState`, el guard de `runTurn` frente al `AgentState` que este capítulo entrega) y otra con
   CH-10 (`SessionManager`, si podría aceptar el primer `AgentState` sin cambiar su código).
   `guidingQuestions` en lenguaje de problema, sin usar "AgentCore"/"AgentActivationRequest"
   literal (verificado con la prueba negativa de §8.4).

## 3. Decisiones de diseño centrales

### 3.1 El nombre del contrato: `AgentActivationRequest`, y NO `ActivationRequest`

Durante la lectura de la Constitution completa (Paso 1 del encargo) se encontró que Amendment v1.1
ya define, literalmente, un contrato llamado `ActivationRequest` (`P-16`: "External stimuli MUST be
normalized into an `ActivationRequest` before entering the execution core") evaluado por un
`AdmissionController` (`P-17`, `INV-E01`/`INV-E02`) — el "Ingress & Activation Plane" de Enterprise,
explícitamente fuera de alcance de BH-v0.1. Se evaluó explícitamente reutilizar el nombre corto
`ActivationRequest` para el contrato de este capítulo y se descartó: son conceptos distintos.
`ActivationRequest` (Amendment v1.1) normaliza un estímulo **externo y crudo** (un prompt, un
webhook, una cola) *antes* de que exista siquiera un `agentId` resuelto. `AgentActivationRequest`
(este capítulo) parte siempre de un `agentId` ya conocido y un `AgentConfig` ya registrado — el
tramo posterior, mucho más acotado. Reutilizar el nombre corto habría sugerido, incorrectamente,
que este capítulo implementa `P-16`/`P-17`. Se documentó la distinción completa en la seccion 6 y
la seccion 15 del capítulo, con el mismo cuidado que CH-10 aplicó a la frontera
`SessionManager`/`HumanInteractionService`, y se agregó un término de glosario propio ("Ingress
Activation") para que quede trazable como concepto vecino, no absorbido.

### 3.2 `INV-01`/`INV-16`: la primera cita LITERAL en sentido estricto de un invariante que nombra a `AgentCore`

Se verificó con grep que `INV-01` ("`AgentCore` no depende directamente de APIs específicas de...")
e `INV-16` ("`AgentCore` puede ejecutarse sin UI") ya citan el nombre `AgentCore` desde la primera
versión de la Constitution adoptada por este repositorio (CH-00), y que CH-03 (`ModelGateway`) ya
tuvo que interpretarlos de forma indirecta ("Primera cita literal posible de este invariante: ya
existe un `ModelGateway` real...", CH-03 §4) porque `AgentCore` no existía todavía como componente.
Este capítulo documenta explícitamente, en la seccion 1 y la seccion 4, que ahora sí existe el
sujeto gramatical real de ambos invariantes — la primera vez que pueden citarse en sentido
estricto, no por aproximación a través de un componente vecino.

### 3.3 Dos funciones, no una — para poder observar el instante `CREATED` sin evento

Se decidió dividir la activación en `activateAgent` (produce `AgentState` con `status = CREATED`,
sin emitir ningún evento) y `beginAgentInitialization` (transiciona a `INITIALIZING`, construye el
primer `ExecutionContext` real del libro, y emite `RUN_STARTED`). Se evaluó una única función que
hiciera ambas cosas de una vez y se descartó: colapsarlas impediría que cualquier componente futuro
observara el instante exacto en que un run existe (`CREATED`) pero todavía no se ha preparado para
correr (`INITIALIZING`) — y perdería la oportunidad de mostrar, con código real, la transición
formal de Article V que ningún capítulo anterior había ejercitado.

### 3.4 Primera construcción real de `ExecutionContext`, y primeras primitivas `newRunId`/`newSessionId`/`newTraceId`

Se verificó con grep (`ExecutionContext(` como constructor, dentro de un bloque `pseudocode`) que
ningún capítulo anterior (CH-00..CH-10) construye jamás un `ExecutionContext` — siempre lo reciben
como parámetro ya existente. Se decidió que `beginAgentInitialization` sea la primera función del
libro en construirlo, con un `TraceId` recién minado (`newTraceId()`, primitiva nueva). De la misma
forma, `RunId` y `SessionId` siempre habían llegado ya dados en los diez capítulos anteriores; este
capítulo introduce `newRunId()`/`newSessionId()` como las primeras primitivas que los originan.

### 3.5 Por qué este capítulo es el primero en emitir `RUN_STARTED`

Se verificó con grep (`eventType = RUN_STARTED` dentro de cualquier bloque `pseudocode`) que ningún
capítulo anterior emitió jamás este valor, declarado desde CH-00 §6 y señalado explícitamente por
CH-01 §14 como perteneciente "al arranque de un `AgentRun`, todavía sin componente propio que lo
orqueste". `beginAgentInitialization` es esa función, once capítulos después. Por esta razón, y a
diferencia de cada uno de los diez capítulos anteriores salvo `EventBus` (CH-09), este capítulo no
agrega ningún valor nuevo a `AgentEventType` — reutiliza uno que llevaba reservado desde el
principio.

### 3.6 `AgentCore` sin fila en Article IV — la misma ausencia que `EventBus`, por una razón distinta

Se verificó con grep completo sobre `constitution/ARCHITECTURE_CONSTITUTION.md` que la tabla de
Article IV (Decision Ownership) no incluye ninguna fila para `AgentCore` (confirmado: las filas son
`AgentLoop`, `ContextEngine`, `ModelGateway`, `ToolRuntime`, `PolicyEngine`,
`HumanInteractionService`, `SessionManager`, `ExecutionController`, `CapabilityRegistry`, `UI`,
además de `LLM`). Es el segundo componente real del libro sin fila propia, después de `EventBus`
(CH-09) — pero por una razón distinta, documentada con cuidado en la seccion 4/5/20: `EventBus` no
decide nada, solo distribuye; `AgentCore` sí decide algo (validar y activar un agente), pero esa
decisión ocurre **antes** de que exista ningún `AgentRun` sobre el cual las preguntas de Article IV
(todas formuladas sobre una ejecución ya en curso) puedan siquiera aplicarse.

### 3.7 La asimetría real en `AgentLoop.runTurn` (CH-01): `INITIALIZING` no se distingue de `RUNNING`

Al releer `runTurn` (CH-01 §11) con cuidado (paso explícitamente pedido por el encargo), se
verificó que su único guard rechaza los cuatro estados terminales
(`COMPLETED`/`FAILED`/`CANCELLED`/`EXPIRED`) — nunca comprueba que `state.status == RUNNING`. Esto
significa que, tal como CH-01 lo escribió, `runTurn` aceptaría sin protestar un `AgentState` en
`INITIALIZING` exactamente igual que uno en `RUNNING`. Se decidió documentar esta asimetría
explícitamente (seccion 12/18, más la pregunta de interleaving IQ-CH11-01) en vez de "arreglarla"
tocando el código de CH-01 — está fuera del alcance decidido (Paso 2 del encargo prohíbe modificar
`runTurn`), y es exactamente el tipo de deuda intencional que el libro deja explícita.

## 4. Otras decisiones de diseño tomadas durante la ejecución

### 4.1 `AgentCore.dependencies: []`

Igual que CH-01..CH-10: no depende de ningún otro componente registrado. El cableado real
`AgentCore → AgentLoop` (completar `INITIALIZING → RUNNING` e invocar `runTurn` por primera vez) y
`AgentCore → SessionManager` (el primer checkpoint de una sesión recién activada) quedan,
explícitamente, como trabajo de un capítulo de integración futuro (seccion 9/18/19).

### 4.2 Grounding constitucional de `constitutional_articles`

`P-06` (Agents are configuration over a shared runtime — `activateAgent` es la primera validación
real de un `AgentConfig`), `P-10` (harness owns execution state — el primer `AgentState`/
`ExecutionContext` nacen de una validación puramente determinística), `P-12` (events observe —
`RUN_STARTED`), `INV-01`/`INV-16` (cita literal, ver §3.2), `INV-08`/`INV-09` (primer execution
state; budget coherente exigido antes de que el run exista), `INV-18`/`INV-19` (evento observable
con `traceId` trazable), `INV-20` (errores clasificados). No se incluyó `P-16`/`P-17`/`INV-E01`/
`INV-E02` en el frontmatter: se citan solo en prosa (seccion 5/15/18) para trazar la distinción con
`AgentActivationRequest`, sin declarar que este capítulo los implementa.

### 4.3 Los dos ejemplos de interleaving (CH-01/CH-10)

Se eligieron los dos capítulos que más directamente motivan este capítulo: `AgentLoop`/`AgentState`
(CH-01, para la asimetría real del guard de `runTurn` frente al `AgentState` que este capítulo
entrega) y `SessionManager` (CH-10, para verificar si el primer `AgentState` producido —
`status = CREATED`, antes incluso de `INITIALIZING`— podría aceptarse sin cambios en
`createOrUpdateSessionCheckpoint`).

## 5. Archivos creados

- `book/chapters/11-agent-core/chapter.md` — capítulo completo (22 secciones: 0, 1-19, 20, 21).
- `planes/2026-09-14-capitulo-11-agent-core.md` — este registro.

## 6. Archivos modificados

- `registry/contracts.yaml` — agrega `C-021 AgentActivationRequest`; actualiza `used_by` de
  `C-002`, `C-003`, `C-004` y `C-012` (agrega `CMP-011`); agrega comentario documentando la
  decisión de diseño (incluida la distinción explícita con `ActivationRequest`, Amendment v1.1).
- `registry/components.yaml` — agrega `CMP-011 AgentCore`; actualiza el comentario de historial.
- `registry/glossary.yaml` — agrega `AgentCore` (kind: component), `AgentActivationRequest` (kind:
  contract), `Agent Identity`, `Agent Activation`, `Agent Initialization`, `Ingress Activation`
  (kind: concept).
- `book/book.yaml` — agrega la entrada `CH-11`.
- `book/chapters/10-session-manager/chapter.md` — únicamente `next_chapter: null` → `CH-11` en el
  frontmatter (sin tocar ninguna otra sección ni la ficha de `CMP-010`).

## 7. Resultado real del pipeline

Comando (desde la raíz del repo, `dist/` borrado antes para forzar un build limpio):

```text
$ rm -rf dist && ./scripts/build-all
...
▶ validate-chapter book/chapters/11-agent-core/chapter.md
validate-chapter: OK — secciones: 22/19, bloques pseudocode: 6, contratos introducidos: 1,
  componentes introducidos: 1
▶ validate-retrieval-set book/chapters/11-agent-core/chapter.md
validate-retrieval-set: OK — guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2,
  interleavedQuestions: 2, flashcards: 5, calibrationPairs: 4
...
▶ build-book-ir → OK → dist/book-ir.json (capítulos: 12 / contratos: 21 / componentes: 11 /
  glosario: 68 / flashcards: 55)
▶ build-mind-map
  chapter-10.diagram: 73 nodo(s), 118 arista(s)
  chapter-11.diagram: 80 nodo(s), 131 arista(s) (7 nuevo(s) en este capítulo)
  full-book.diagram: 80 nodo(s), 131 arista(s)
▶ build-web → OK → dist/web/ — index.html + 2 páginas de frontmatter + 12 capítulos + mapa.html
▶ build-pdf → OK → dist/book.pdf (1435439 bytes)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
```

Exit code: `0` (verificado explícitamente tras `rm -rf dist && ./scripts/build-all`, y de nuevo
tras revertir las dos pruebas negativas de §8.4, con conteos idénticos: 80 nodos/131 aristas, 21
contratos, 11 componentes, 12 capítulos, 277 páginas de PDF).

## 8. Evidencia de verificación concreta

### 8.1 Mapa mental acumulativo (CH-11 > CH-10 > ... > CH-00)

`chapter-10.diagram`: 73 nodos / 118 aristas. `chapter-11.diagram`: **80 nodos / 131 aristas** (7
nodos nuevos: `CH-11`, `CMP-011`, `C-021`, y los cuatro conceptos de glosario nuevos con nodo
propio — `Agent Identity`, `Agent Activation`, `Agent Initialization`, `Ingress Activation`;
`AgentCore`/`AgentActivationRequest`, `kind: component`/`kind: contract` en el glosario, no generan
nodo propio, ya representados por `CMP-011`/`C-021`). Cumple el criterio del encargo (más
nodos/aristas que CH-10: 80 > 73, 131 > 118). `full-book.diagram` coincide exactamente con el
snapshot de CH-11 (el último), confirmando acumulación real.

### 8.2 Web

- `dist/web/chapters/CH-11.html` existe, con SVG de mapa mental inline (`grep -c '<svg'` == 1).
- Anchors de entidad presentes: `id="CMP-011"` (1), `id="C-021"` (1).
- Navegación prev/next verificada en ambos sentidos: `CH-10.html` contiene `href="CH-11.html"`;
  `CH-11.html` contiene `href="CH-10.html"`.
- Anchors de capítulos previos verificados intactos (1 aparición cada uno): CH-00 (`C-001`), CH-01
  (`CMP-001`, `C-013`), CH-10 (`CMP-010`, `C-020`) — sin cambios.
- `<svg` aparece exactamente 1 vez en cada una de las 12 páginas de capítulo (CH-00..CH-11).
- `dist/web/index.html` lista los doce capítulos (`CH-00`..`CH-11`).

### 8.3 PDF (`pypdf`)

- Build completo (CH-00..CH-11): **277 páginas** — el build de 11 capítulos (CH-00..CH-10) tenía
  255 páginas (ver `planes/2026-09-14-capitulo-10-session-manager.md` §8.3); 277 > 255,
  confirmando el crecimiento esperado.
- Texto extraído del PDF completo, verificado con `pypdf.PdfReader(...).extract_text()`:
  `"AgentCore"` → `True`, `"AgentActivationRequest"` → `True`, `"CMP-011"` → `True`, `"C-021"` →
  `True`, `"Agent Identity"` → `True`, `"Ingress Activation"` → `True`, `"RUN_STARTED"` → `True`.

### 8.4 Pruebas negativas (inyectadas y revertidas, una a la vez)

1. **`produces` inválido en la ficha de componente**: se agregó `C-999` (inexistente) a
   `CMP-011.produces` en `registry/components.yaml` → `validate-components` falló limpio con
   `exit 1` y el mensaje exacto `Componente CMP-011: produces referencia contrato inexistente
   "C-999"`. Revertido (`diff` contra el backup en `/tmp/components.yaml.bak` confirmó archivo
   idéntico; `validate-components` volvió a `OK (11 componente(s))`, `exit 0`).
2. **Nombre canónico en una guiding question**: se reescribió `GQ-CH11-01` para que dijera
   literalmente "¿Decide AgentCore quién instancia ese primer estado...?" → `validate-retrieval-set`
   falló limpio con `exit 1` y el mensaje exacto `retrievalSet.guidingQuestions[GQ-CH11-01]
   contiene el nombre canónico "AgentCore", que este mismo capítulo introduce — las preguntas guía
   deben usar lenguaje de problema`. Revertido (`diff` contra el backup en `/tmp/ch11.md.bak`
   confirmó archivo idéntico; `validate-retrieval-set` volvió a `OK`, `exit 0`).
3. Tras revertir ambas inyecciones (`diff` confirmó archivos idénticos byte a byte), `rm -rf dist &&
   ./scripts/build-all` volvió a pasar limpio con los mismos conteos de nodos/aristas (80/131), de
   contratos/componentes (21/11), de capítulos (12) y de páginas de PDF (277, verificado de nuevo
   con `pypdf`) que antes de las inyecciones (exit 0).

### 8.5 CH-00..CH-10 no se rompieron

- `validate-chapter`/`validate-retrieval-set` de los once siguen en verde (ver §7, corrida completa
  de `build-all`).
- Los anchors de CH-00..CH-10 no cambiaron de contenido (ver §8.2).
- Solo se editó `next_chapter` en el frontmatter de CH-10 — su cuerpo, su ficha de
  `SessionManager` y su `retrieval_set` quedaron intactos.
- `mapa.html` sigue mostrando el grafo acumulado completo con los doce capítulos.

### 8.6 Confirmación textual: `AgentCore` sin fila en Article IV

Verificado con `grep` de texto completo sobre `constitution/ARCHITECTURE_CONSTITUTION.md`: la
tabla de Article IV (líneas 360-393) enumera únicamente `LLM`, `AgentLoop`, `ContextEngine`,
`ModelGateway`, `ToolRuntime`, `PolicyEngine`, `HumanInteractionService`, `SessionManager`,
`ExecutionController`, `CapabilityRegistry` y `UI` — ninguna fila para `AgentCore`. Confirmado: es
el segundo componente real del libro sin fila propia (después de `EventBus`, CH-09), documentado
con la razón distinta en seccion 4/5/20 del capítulo (ver §3.6 de este plan).

## 9. Definition of Done (restringido a este incremento)

- ✅ CH-11 completo: 22 secciones (0, 1-19, 20, 21), sin relleno — cada sección con contenido real.
- ✅ `registry/contracts.yaml` / `registry/components.yaml` / `registry/glossary.yaml` /
  `book/book.yaml` actualizados y validados (`validate-contracts`, `validate-components`).
- ✅ `RetrievalSet` completo con `interleavedQuestions = 2` conectando con CH-01 y CH-10.
- ✅ Pipeline completo (`build-all`) verde desde `dist/` limpio, para los 12 capítulos.
- ✅ Evidencia concreta: conteos de nodos/aristas del mapa mental (80/131 > 73/118), conteo de
  páginas de PDF (277 vs. 255 del build de 11 capítulos), texto extraído del PDF, anchors HTML, dos
  pruebas negativas con mensaje de error exacto y reversión confirmada con conteos idénticos.
- ✅ CH-00..CH-10 verificados intactos tras el cambio (salvo el campo de navegación autorizado en
  CH-10).
- ✅ Confirmado con grep: `AgentCore` no tiene fila en la tabla de Decision Ownership de Article IV
  — documentado como el segundo componente del libro sin fila (después de `EventBus`), por una
  razón distinta (su decisión ocurre antes de que exista un `AgentRun`, no porque no decida nada).
- ✅ Distinción explícita y documentada entre `AgentActivationRequest` (este capítulo) y
  `ActivationRequest` (Amendment v1.1, `P-16`/`P-17`, Ingress & Activation Plane, Enterprise, fuera
  de alcance de BH-v0.1) — hallazgo real encontrado durante la lectura completa de la Constitution,
  no anticipado en el encargo original.
- ✅ Primera construcción real de `ExecutionContext` y primera emisión real de `RUN_STARTED`,
  ambos declarados desde CH-00 sin que ningún componente los hubiera ejercitado hasta este capítulo.
- ✅ Asimetría real documentada (no corregida): `AgentLoop.runTurn` (CH-01) no distingue
  `INITIALIZING` de `RUNNING` en su guard — señalada explícitamente en seccion 12/18 y en
  `IQ-CH11-01`, sin modificar el código de CH-01.

## 10. Deuda intencional hacia el próximo capítulo (fuera de este alcance)

- **El cableado real `AgentCore → AgentLoop`**: nadie invoca `runTurn` después de
  `beginAgentInitialization`; la transición `INITIALIZING → RUNNING` sigue sin ejercitarse con
  código, y el guard de `runTurn` sigue sin distinguir ambos estados.
- **El cableado real `AgentCore → SessionManager`**: `beginAgentInitialization` no invoca
  `createOrUpdateSessionCheckpoint`.
- **El mecanismo real detrás de `findAgentConfig`**: primitiva asumida, sin modelar el registro o
  almacén concreto de `AgentConfig`.
- **El "Ingress & Activation Plane" completo de Amendment v1.1** (`ActivationRequest`,
  `AdmissionController`, `P-16`/`P-17`, `INV-E01`/`INV-E02`) y el resto de componentes de esa
  enmienda (`AgentCommunicationGateway`, `CredentialBroker`, ...): fuera de alcance de BH-v0.1.
- **Autorización sobre quién puede activar un agente ajeno**: señalado explícitamente como límite
  de seguridad real, no silenciado.
- **Reactivación, desactivación o versión de un `AgentConfig` ya existente, cancelación de una
  activación a medio camino**: no modelado.
- Reviewers plurales, evals y orquestación multi-agente: explícitamente fuera de alcance de BH-v0.1.
- **El capítulo de integración de punta a punta** (`AgentCore → AgentLoop → ContextEngine →
  ModelGateway → CapabilityRegistry → PolicyEngine → ToolRuntime → HumanInteractionService →
  SessionManager → EventBus`): con los once nombres de Article III ya reales, este es ahora el
  candidato natural y único para el próximo incremento (CH-11 §19).
