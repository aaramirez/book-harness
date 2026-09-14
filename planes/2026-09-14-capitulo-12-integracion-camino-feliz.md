# Plan / Registro de ejecución — Capítulo 12: Integración, el Camino Feliz de un AgentRun Completo

**Fecha:** 2026-09-14
**Estado:** ✅ Completado, sobre el estado dejado por `1bc4e7a` (CH-00..CH-11 como los doce únicos
capítulos reales; los once componentes de Article III ya instanciados desde CH-11, cada uno con su
propia demostración aislada y su propia deuda intencional hacia un capítulo de integración que
todavía no existía).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- Los once planes `2026-09-1{3,4}-capitulo-0{1..9}-*.md` / `capitulo-1{0,1}-*.md` (cada uno
  documenta, en su propia sección de deuda intencional, exactamente qué llamada real hacia otro
  capítulo dejó pendiente — la lista consolidada de nueve cables que este capítulo cierra, ver §2)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Article III — Component Sovereignty, Article IV —
  Decision Ownership, Article V — Lifecycle, Article VI — Execution Constitution)

---

## 1. Objetivo

Escribir el decimotercer capítulo real de contenido del libro ("¿Cómo construir un arnés?"), CH-12
— el primer capítulo de **integración**: el camino feliz (*allow path*) de un `AgentRun` completo,
de principio a fin. A diferencia de los doce capítulos anteriores, este no introduce ningún
componente ni ningún contrato nuevo — es pura composición: invoca, con datos reales fluyendo entre
sí, las funciones que los once capítulos anteriores ya publicaron y ya registraron, sin modificar
el pseudocódigo ya publicado de ninguno de ellos.

## 2. Los nueve cables cerrados (Paso 1 del encargo — lectura completa de los 12 capítulos + 11 planes)

Consolidados desde la sección 18/19 de CH-01, CH-02, CH-03, CH-04, CH-05, CH-07, CH-08, CH-09,
CH-10 (y confirmados en CH-11 §19, que los resume todos como el problema natural del próximo
incremento):

1. **CH-11 → CH-01.** `AgentCore.beginAgentInitialization` producía `AgentState(INITIALIZING)` sin
   que nadie lo llevara a `RUNNING` ni se lo entregara a `AgentLoop.runTurn`. **Cerrado**:
   `runAgentTurnEndToEnd` construye explícitamente el `AgentState(RUNNING)` y es la primera función
   del libro en invocar `runTurn` sobre un `AgentState` que `AgentCore` produjo.
2. **CH-01 → CH-03.** `runTurn` decidía la transición con dos booleanos sueltos
   (`modelFinished`/`modelProposesToolCall`), nunca con un `ModelResponse` real. **Cerrado**: este
   capítulo deriva ambos booleanos de `responseOne.finished`/`responseOne.proposedToolCall != NULL`
   — un `ModelResponse` real producido por `invokeModelForTurn` (CH-03) — sin modificar la firma de
   `runTurn`.
3. **CH-04 → CH-03.** `ContextSnapshot.blocks` nunca se conectaba con `ModelRequest.messages`.
   **Cerrado**: este capítulo construye, a partir de cada `ContextBlock.content` de un
   `ContextSnapshot` real, los `AgentMessage` que `invokeModelForTurn` recibe como
   `pendingMessages`.
4. **CH-03 → CH-08.** `RawToolCallProposal` se resolvía contra `CapabilityRegistry` solo de forma
   aislada (con datos de ejemplo, CH-08 §11), nunca dentro de un turno real. **Cerrado**:
   `resolveModelProposedToolCall` se invoca sobre el `ModelResponse` real que
   `invokeModelForTurn` acaba de producir dentro del mismo turno.
5. **CH-05 → CH-02.** `ToolRuntime.executeToolCall` nunca invocaba
   `PolicyEngine.evaluatePolicyForToolCall` antes de ejecutar. **Cerrado, para `outcome = ALLOW`**:
   este capítulo invoca `evaluatePolicyForToolCall` sobre el `ToolCall` real que
   `CapabilityRegistry` acaba de resolver, y solo invoca `executeToolCall` cuando
   `outcome == ALLOW` — deteniéndose explícitamente en caso contrario (DENY/REQUIRE_APPROVAL,
   CH-13).
6. **CH-07 → CH-01.** `runTurn` nunca invocaba
   `ExecutionController.evaluateExecutionContinuation` antes de decidir si continuar. **Cerrado,
   para `outcome = CONTINUE`**: este capítulo invoca `evaluateExecutionContinuation` antes de cada
   uno de los dos turnos, y solo continúa cuando `outcome == CONTINUE` — deteniéndose
   explícitamente en caso contrario (STOP/CANCELLED, CH-13).
7. **CH-02 → CH-01 (INV-07).** `runTurn` transicionaba a `WAITING_FOR_TOOL` y se detenía ahí, sin
   que nadie lo retomara con el `ToolResult` real como observación. **Cerrado**: este capítulo
   construye un `AgentMessage` (`role = TOOL`) a partir del `ToolResult` real que `executeToolCall`
   produce, lo agrega a `candidates`, y transiciona explícitamente el estado de vuelta a `RUNNING`
   antes del segundo turno — que sí ve esa observación en su `ContextSnapshot`.
8. **CH-09 → CH-00..CH-08/CH-10/CH-11.** Ningún `EMIT` de ningún capítulo anterior invocaba de
   verdad `EventBus.distributeEvent`. **Cerrado, para cada evento de la traza de este capítulo**:
   la función nueva `emitAndDistribute` (seccion 11) reconstruye el `AgentEvent` equivalente al que
   cada función ya publicada produce internamente, y lo entrega explícitamente a `distributeEvent`
   — quince apariciones en total, diez tipos de evento distintos (seccion 14).
9. **CH-10 → CH-01.** `runTurn` nunca invocaba `SessionManager.createOrUpdateSessionCheckpoint` al
   cierre de un turno. **Cerrado**: este capítulo invoca `createOrUpdateSessionCheckpoint`
   inmediatamente después de cada una de las dos invocaciones de `runTurn`.

**Explícitamente fuera de este capítulo (CH-13, no escrito)**: `PolicyDecision.outcome = DENY`;
`PolicyDecision.outcome = REQUIRE_APPROVAL` → `HumanInteractionService` → resolución →
reanudación; `ExecutionDecision.outcome = STOP`/`CANCELLED` → terminación
(`FAILED`/`CANCELLED`/`EXPIRED`). Mencionados en prosa (seccion 15/18/19), no implementados.

## 3. Decisiones de diseño centrales

### 3.1 Una función de integración nueva, nunca una modificación de las once ya publicadas

Se decidió, siguiendo literalmente el encargo, escribir `runAgentTurnEndToEnd` (más un helper,
`emitAndDistribute`) como funciones nuevas y propias de este capítulo — nunca reabrir ni modificar
el pseudocódigo ya publicado de `AgentLoop.runTurn`, `ToolRuntime.executeToolCall`, ni ninguna otra
de las once funciones invocadas. Esto significa, en particular, que `runTurn` sigue recibiendo dos
booleanos sueltos (nunca un `ModelResponse`) y que `executeToolCall` sigue recibiendo
`capabilityResolved`/`inputValid` como booleanos (nunca calculándolos de nuevo) — la integración
ocurre en cómo se calculan esos valores ANTES de la llamada, no en cambiar qué reciben las
funciones ya publicadas.

### 3.2 `emitAndDistribute`: cómo se le da un destino real a `EMIT` sin tocar ningún componente

La gramática canónica (`EMIT`, `skills/write-pseudocode/SKILL.md`) nunca definió un canal de
retorno — cada componente productor construye su propio `AgentEvent` y lo declara con `EMIT`
dentro de su propia función, sin devolverlo a quien invocó esa función. Este capítulo no puede
capturar el evento interno que, por ejemplo, `runTurn` ya emite. Se decidió, en su lugar, que
`runAgentTurnEndToEnd` reconstruya el `AgentEvent` equivalente (mismo `eventType`, el mismo
`execution`/`agentId` que ya comparte con la llamada que acaba de hacer, y el mismo `payload` que
esa llamada le devolvió) y lo entregue explícitamente a `distributeEvent` (CH-09) a través de un
helper, `emitAndDistribute`. Se documenta esta decisión con total honestidad en la seccion 11 del
capítulo: es una reconstrucción, no una captura literal del evento interno.

### 3.3 Dos turnos, no uno — para poder demostrar `WAITING_FOR_TOOL → RUNNING` con una observación real

Se decidió modelar exactamente dos turnos dentro de `runAgentTurnEndToEnd`: el primero, donde el
modelo propone una tool call (`WAITING_FOR_TOOL`), y el segundo, donde el modelo ya ve la
observación real de esa tool call y termina de razonar (`COMPLETED`). Se evaluó modelar un solo
turno (sin tool call) y se descartó: no habría demostrado el cierre del cable #7
(`WAITING_FOR_TOOL` resuelto con una observación real), que es, junto con el cierre del cable #8
(`EventBus`), el corazón de este capítulo.

### 3.4 Disponibilidad de tipos no registrados (`ExecutionUsage`, `AgentEventType`) sin introducir nada

Al escribir el pseudocódigo se encontró (verificado con `./scripts/validate-chapter`, primera
corrida) que referenciar `ExecutionUsage` (embebido en `ExecutionDecision`, CH-07, sin `C-XXX`
propio) y `AgentEventType` (embebido en `AgentEvent`, sin `C-XXX` propio) como tipos explícitos en
las firmas de este capítulo requiere que ambos estén "disponibles" según el mecanismo de
`scripts/lib/chapter-parser.js`/`validate-chapter` — que reconstruye la disponibilidad de
entidades **por capítulo**, no de forma acumulativa entre capítulos, para cualquier tipo sin
`C-XXX` propio. Se resolvió exactamente con los dos mecanismos que CH-08/CH-09/CH-11 ya
establecieron: una fila de tabla markdown para `ExecutionUsage` (mismo patrón que CH-08 usó para
`RawToolCallProposal`) y una redeclaración completa, sin agregar ningún valor, del `ENUM
AgentEventType` (mismo patrón que CH-11 §14 ya hizo). Ninguno de los dos mecanismos agrega nada a
`registry/contracts.yaml` ni cambia `modifies_contracts` (que permanece `[]`).

### 3.5 Hallazgo real: `AgentCore.beginAgentInitialization` no devuelve su `ExecutionContext`

Al escribir la integración se descubrió (no anticipado en el encargo original) que
`beginAgentInitialization` (CH-11 §11) construye su propio `ExecutionContext` únicamente para
poblar el `AgentEvent` que emite internamente, pero **nunca lo devuelve** — su firma retorna solo
`AgentState`. Como el encargo prohíbe modificar el código ya publicado de CH-11, este capítulo
construye un segundo `ExecutionContext` equivalente (mismo `runId`/`sessionId`/`budget`, un
`traceId` propio vía `newTraceId()`, la misma primitiva de CH-11) para el resto de la traza. Se
documenta este seam explícitamente en la seccion 11/18 del capítulo — es una inconsistencia real
del libro, no oculta, que una revisión futura de CH-11 (fuera de este alcance) podría resolver
haciendo que `beginAgentInitialization` también devuelva su `ExecutionContext`.

### 3.6 `registry/*.yaml` sin tocar: consecuencia real y verificada en el `BookMindMap`

Siguiendo el encargo con literalidad, este capítulo **no modifica ninguna ficha** de
`registry/components.yaml`/`registry/contracts.yaml`/`registry/glossary.yaml` — ni siquiera para
agregar, al campo `dependencies` de un componente existente, la relación real que este capítulo
demuestra en pseudocódigo. Se verificó con `./scripts/build-mind-map` (§7) que esto tiene una
consecuencia mecánica real: `scripts/lib/mindmap.js` deriva las aristas
`DEPENDS_ON`/`PRODUCES`/`CONSUMES` **exclusivamente** de los campos que cada componente ya
declaraba en su propio capítulo de introducción (ver el comentario de cabecera del archivo, y la
función `buildMindMapSnapshots`, que solo itera `componentsByChapter.get(chapterId)` — vacío para
`CH-12`, que no introduce ningún componente). El resultado real, verificado, es que
`diagrams/mindmap/chapter-12.diagram` tiene **exactamente las mismas 131 aristas** que
`chapter-11.diagram` — un solo nodo nuevo (el nodo `CHAPTER` de `CH-12` mismo, que
`buildMindMapSnapshots` agrega incondicionalmente para todo capítulo, sin importar qué introduce).
Esto **contradice la expectativa del encargo** ("`chapter-12.diagram` debería tener MUCHAS más
aristas que `chapter-11.diagram`... esta vez las aristas nuevas son de tipo
`DEPENDS_ON`/`CONSUMES`/`PRODUCES`") — se documenta aquí, en la seccion 9/17/18 del capítulo, y en
el reporte final de esta ejecución, exactamente como información real, sin ocultarla ni forzarla:
el mecanismo actual del `BookMindMap` no tiene ningún camino para que un capítulo de integración
que no toca el registry agregue aristas de esos tres tipos — solo un capítulo que declare
`introduces_components`/`dependencies` nuevos puede hacerlo, y este capítulo, por instrucción
explícita del encargo, no lo hace.

## 4. Otras decisiones de diseño tomadas durante la ejecución

### 4.1 Sin adiciones a `registry/glossary.yaml`

Se evaluó agregar 2-3 términos de glosario nuevos (`kind: concept`) — "Camino Feliz (Allow Path)",
"Cierre de Cableado (Wire Closure)" — que habrían agregado un puñado de nodos/aristas `INTRODUCES`
reales al `BookMindMap` sin tocar ningún componente/contrato existente. Se descartó: el encargo es
explícito ("NO toques `registry/*.yaml` salvo que necesites revisar — no editar"), y
`registry/glossary.yaml` está bajo ese mismo prefijo. Ambas ideas se documentan en la seccion 5 del
capítulo como conceptos puramente narrativos, sin entrada de glosario.

### 4.2 `constitutional_articles` del frontmatter

`P-04`/`P-05`/`P-10`/`P-12`/`P-13` (principios que, por primera vez, se cumplen con una ejecución
real de punta a punta en vez de solo declarados o demostrados de forma aislada) e
`INV-06`/`INV-07`/`INV-08`/`INV-09`/`INV-18`/`INV-19`/`INV-20` (invariantes preservados, varios
citados con ejecución real por primera vez). No se incluyeron `INV-10`/`INV-15` (cancelación /
aprobación humana): se citan solo en prosa (seccion 15/18) como los caminos que este capítulo
deliberadamente no cierra.

### 4.3 Las cinco `interleavedQuestions`, cruzando capítulos distantes

Se eligieron cinco pares deliberadamente distantes entre sí (no capítulos consecutivos): CH-11↔
CH-02 (identidad del run hasta la tool call), CH-04↔CH-08 (dos "puertas" de verificación antes de
avanzar), CH-01↔CH-07 (orden real entre continuación cognitiva y operacional), CH-03↔CH-02
(cuántos componentes median entre la propuesta cruda y la ejecución real), y CH-09↔CH-06
(`EventBus` distribuiría `HUMAN_INTERACTION_REQUESTED` sin cambiar una línea, el día que CH-13
exista). Cada una evita usar jerga que dé la respuesta, en lenguaje de problema.

## 5. Archivos creados

- `book/chapters/12-integracion-camino-feliz/chapter.md` — capítulo completo (22 secciones: 0,
  1-19, 20, 21). Slug elegido: `12-integracion-camino-feliz`.
- `planes/2026-09-14-capitulo-12-integracion-camino-feliz.md` — este registro.

## 6. Archivos modificados

- `book/book.yaml` — agrega la entrada `CH-12` después de `CH-11`.
- `book/chapters/11-agent-core/chapter.md` — únicamente `next_chapter: null` → `CH-12` en el
  frontmatter (sin tocar ninguna otra sección ni la ficha de `CMP-011`).
- **Ningún archivo de `registry/`** (`components.yaml`/`contracts.yaml`/`glossary.yaml`) se
  modificó — verificado con `git status`/`git diff` antes de comitear (ver §7).

## 7. Resultado real del pipeline

Comando (desde la raíz del repo, `dist/` borrado antes para forzar un build limpio):

```text
$ rm -rf dist && ./scripts/build-all
...
▶ validate-chapter book/chapters/12-integracion-camino-feliz/chapter.md
validate-chapter: OK — secciones: 22/19, bloques pseudocode: 3, contratos introducidos: 0,
  componentes introducidos: 0
▶ validate-retrieval-set book/chapters/12-integracion-camino-feliz/chapter.md
validate-retrieval-set: OK — guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2,
  interleavedQuestions: 5, flashcards: 5, calibrationPairs: 4
...
▶ build-book-ir → OK → dist/book-ir.json (capítulos: 13 / contratos: 21 / componentes: 11 /
  glosario: 68 / flashcards (retrievalSet): 60)
▶ build-mind-map
  chapter-11.diagram: 80 nodo(s), 131 arista(s) (7 nuevo(s) en este capítulo)
  chapter-12.diagram: 81 nodo(s), 131 arista(s) (1 nuevo(s) en este capítulo)
  full-book.diagram: 81 nodo(s), 131 arista(s)
▶ build-web → OK → dist/web/ — index.html + 2 páginas de frontmatter + 13 capítulos + mapa.html
▶ build-pdf → OK → dist/book.pdf (1570501 bytes)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
```

Exit code: `0` — verificado explícitamente tras `rm -rf dist && ./scripts/build-all`, dos veces
(una antes de la prueba negativa de §8, otra después de revertirla), con conteos idénticos.

**Nota real sobre `validate-chapter`/`build-mind-map` con `introduces_contracts: []`/
`introduces_components: []`**: ambos aceptan el capítulo sin ningún error ni advertencia especial
— no existe ninguna regla, en ninguno de los dos scripts, que exija que un capítulo introduzca al
menos un contrato o un componente. `validate-chapter` reporta, sin fallar, `contratos
introducidos: 0` / `componentes introducidos: 0`. `build-mind-map` procesa `CH-12` con
`componentsByChapter.get('CH-12') == undefined`, sin lanzar ninguna excepción — simplemente no
agrega ninguna arista `DEPENDS_ON`/`PRODUCES`/`CONSUMES` nueva (ver §3.6, hallazgo real).

## 8. Evidencia de verificación concreta

### 8.1 Mapa mental acumulativo (CH-12 vs. CH-11)

`chapter-11.diagram`: 80 nodos / 131 aristas. `chapter-12.diagram`: **81 nodos / 131 aristas** — un
solo nodo nuevo (`CH-12`, el nodo `CHAPTER` que `buildMindMapSnapshots` agrega
incondicionalmente), **cero aristas nuevas**. `full-book.diagram` coincide exactamente con el
snapshot de `CH-12` (el último). Este resultado **no coincide** con la expectativa original del
encargo ("muchas más aristas... de tipo DEPENDS_ON/CONSUMES/PRODUCES") — ver §3.6 para el análisis
completo de por qué el mecanismo actual del `BookMindMap` no puede producir ese resultado sin
editar `registry/components.yaml`, que el encargo prohíbe editar.

### 8.2 Web

- `dist/web/chapters/CH-12.html` existe, con SVG de mapa mental inline (`grep -c '<svg'` == 1).
- Navegación prev/next verificada en ambos sentidos: `CH-11.html` contiene `href="CH-12.html"`;
  `CH-12.html` contiene `href="CH-11.html"`.
- `<svg` aparece exactamente 1 vez en cada una de las 13 páginas de capítulo (CH-00..CH-12).
- Anchors de capítulos previos verificados intactos (1 aparición cada uno): CH-00 (`id="C-001"`),
  CH-01 (`id="CMP-001"`, `id="C-013"`), CH-10 (`id="CMP-010"`, `id="C-020"`) — sin cambios.
- `dist/web/index.html` lista los trece capítulos (`CH-00`..`CH-12`).
- `CH-12.html` no tiene ningún `id="CMP-*"`/`id="C-0*"` propio (no introduce ninguno) —
  verificado, coincide con `introduces_components: []`/`introduces_contracts: []`.

### 8.3 PDF (`pypdf`)

- Build completo (CH-00..CH-12): **305 páginas** — más que el build de 12 capítulos (277 páginas,
  ver `planes/2026-09-14-capitulo-11-agent-core.md` §8.3); 305 > 277, confirmando el crecimiento
  esperado.
- Texto extraído del PDF completo, verificado con `pypdf.PdfReader(...).extract_text()`: los once
  nombres de componente (`AgentCore`, `AgentLoop`, `ToolRuntime`, `ModelGateway`, `ContextEngine`,
  `PolicyEngine`, `HumanInteractionService`, `ExecutionController`, `CapabilityRegistry`,
  `EventBus`, `SessionManager`) → `True` cada uno; `runAgentTurnEndToEnd` → `True`;
  `emitAndDistribute` → `True`; `"Camino Feliz"` → `True`; `WAITING_FOR_TOOL` → `True`.

### 8.4 Prueba negativa (inyectada y revertida)

Se inyectó una entidad inexistente (`bogus: NonExistentEntity = NULL`) dentro del bloque
`pseudocode` de `runAgentTurnEndToEnd` → `validate-chapter` falló limpio con `exit 1` y el mensaje
exacto `Entidad no definida ("no magic entities") en bloque de pseudocódigo: "NonExistentEntity"`.
Revertido (`diff` contra el backup en `/tmp/ch12.md.bak` confirmó archivo idéntico byte a byte;
`validate-chapter`/`validate-retrieval-set` volvieron a `OK`, `exit 0`; `rm -rf dist &&
./scripts/build-all` volvió a pasar limpio con los mismos conteos: 81 nodos/131 aristas, 21
contratos, 11 componentes, 13 capítulos, 305 páginas de PDF).

No se encontró, más allá de esta, una segunda prueba negativa "natural" específica de este
capítulo contra la regla "no magic entities" ligada a `introduces_contracts`/`introduces_components`
(por ejemplo, "declarar un contrato en `introduces_contracts` que el pseudocódigo no define" — CH-11
§8.4 ya cubrió esa clase de prueba en un capítulo que sí introduce entidades). Se documenta como
válido que este capítulo no tenga una segunda prueba negativa de ese tipo, dado que
`introduces_contracts: []`/`introduces_components: []` no dejan ningún nombre "introducido por este
capítulo" contra el cual esa clase específica de regla pudiera fallar.

### 8.5 CH-00..CH-11 no se rompieron

- `validate-chapter`/`validate-retrieval-set` de los doce siguen en verde (ver §7, corrida completa
  de `build-all`).
- Los anchors de CH-00..CH-11 no cambiaron de contenido (ver §8.2).
- Solo se editó `next_chapter` en el frontmatter de CH-11 — su cuerpo, su ficha de `AgentCore` y su
  `retrieval_set` quedaron intactos.
- `registry/components.yaml`, `registry/contracts.yaml` y `registry/glossary.yaml` — sin cambios,
  verificado con `git diff` antes de comitear (ver §9).

## 9. Definition of Done (restringido a este incremento)

- ✅ CH-12 completo: 22 secciones (0, 1-19, 20, 21), sin relleno — cada sección con contenido real.
- ✅ `introduces_components: []` / `introduces_contracts: []` / `modifies_contracts: []` —
  confirmado válido contra `validate-chapter` (sin error alguno) y `build-mind-map` (procesa el
  capítulo sin excepción).
- ✅ `book/book.yaml` actualizado (agrega `CH-12`); `book/chapters/11-agent-core/chapter.md` con
  únicamente `next_chapter: CH-12`; `registry/*.yaml` sin ninguna modificación.
- ✅ `RetrievalSet` completo con `interleavedQuestions = 5`, cruzando capítulos deliberadamente
  distantes (CH-11↔CH-02, CH-04↔CH-08, CH-01↔CH-07, CH-03↔CH-02, CH-09↔CH-06).
- ✅ Pipeline completo (`build-all`) verde desde `dist/` limpio, para los 13 capítulos.
- ✅ Evidencia concreta: conteo de páginas de PDF (305 vs. 277 del build de 12 capítulos), texto
  extraído del PDF (los once componentes + las dos funciones de integración, todos mencionados por
  nombre), anchors HTML, una prueba negativa con mensaje de error exacto y reversión confirmada con
  conteos idénticos.
- ✅ CH-00..CH-11 verificados intactos tras el cambio (salvo el campo de navegación autorizado en
  CH-11).
- ✅ Los nueve cables de la lista consolidada (§2), cerrados uno por uno, cada uno citando el
  capítulo/sección exacta de la deuda que cierra.
- ✅ Hallazgo real, no anticipado en el encargo, documentado con honestidad: `AgentCore.
  beginAgentInitialization` (CH-11) no devuelve el `ExecutionContext` que construye internamente
  (§3.5).
- ✅ Hallazgo real, no anticipado en el encargo, documentado con honestidad: el mecanismo actual de
  `scripts/lib/mindmap.js` no puede producir aristas `DEPENDS_ON`/`PRODUCES`/`CONSUMES` nuevas para
  un capítulo de integración que no modifica `registry/components.yaml` — `chapter-12.diagram`
  tiene las mismas 131 aristas que `chapter-11.diagram`, no "muchas más" como anticipaba el encargo
  (§3.6/§8.1).

## 10. Deuda intencional hacia el próximo capítulo (fuera de este alcance — "CH-13")

- **El camino `DENY`**: qué debería pasar cuando `PolicyEngine` deniega una acción dentro de una
  ejecución real — ¿el turno termina en `FAILED`? ¿se le devuelve la denegación al modelo como
  observación?
- **El camino `REQUIRE_APPROVAL`**: cablear `HumanInteractionService.createHumanInteractionRequest`
  dentro de esta misma traza, transicionar realmente hacia `WAITING_FOR_HUMAN`, y reanudar con una
  `HumanInteractionResolution` real — el ciclo completo de Article VIII, todavía sin una sola
  ejecución real de punta a punta.
- **Los caminos `STOP`/`CANCELLED`**: hacia qué `AgentRunStatus` terminal exacto
  (`FAILED`/`CANCELLED`/`EXPIRED`) debería transicionar un run cuando `ExecutionController` decide
  que no puede continuar.
- **El seam real en `AgentCore.beginAgentInitialization`** (§3.5): no devuelve su
  `ExecutionContext` — una revisión futura de CH-11 podría resolverlo.
- **`registry/components.yaml` sin aristas de dependencia real** (§3.6): el `BookMindMap` mecánico
  no refleja, todavía, el cableado real que este capítulo demuestra en pseudocódigo.
- Paralelismo de tool calls, ranking semántico real de contexto, Provider Adapters reales,
  algoritmos reales de validación de schema, mecanismo real de alta de `CapabilityDescriptor`,
  autorización sobre quién puede activar un agente ajeno: deuda intencional heredada de
  CH-02..CH-11, sin cambios en este capítulo.
- Reviewers plurales, evals y orquestación multi-agente: explícitamente fuera de alcance de
  BH-v0.1 (igual que todos los capítulos anteriores).
