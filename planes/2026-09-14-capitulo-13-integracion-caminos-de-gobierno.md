# Plan / Registro de ejecución — Capítulo 13: Integración, los Caminos de Gobierno de un AgentRun

**Fecha:** 2026-09-14
**Estado:** ✅ Completado, sobre el estado dejado por `13bd479` (CH-00..CH-12 como los trece únicos
capítulos reales; CH-12 ya cerró nueve cables de integración para el camino feliz de un `AgentRun`
completo, dejando explícitamente pendientes los tres caminos que este capítulo cierra).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-14-capitulo-12-integracion-camino-feliz.md` (contrato de continuidad: nombres exactos de
  `runAgentTurnEndToEnd`/`emitAndDistribute`, los nueve cables ya cerrados, y los tres explícitamente
  dejados pendientes — ver §2)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Article II — Invariants, Article VI — Execution,
  Article VIII — Human Interaction, Article IX — Resources and Budgets)

---

## 1. Objetivo

Escribir el decimocuarto capítulo real de contenido del libro ("¿Cómo construir un arnés?"), CH-13
— el segundo y último capítulo de integración planeado: los caminos que CH-12 dejó explícitamente
pendientes al modelar solo el camino feliz (`ALLOW`/`CONTINUE`) de un `AgentRun` completo. Igual que
CH-12, este capítulo no introduce ningún componente ni ningún contrato nuevo — es pura composición:
escribe cinco funciones nuevas y propias que invocan, con nombres exactos, las funciones que
CH-01..CH-12 ya publicaron, sin modificar el pseudocódigo ya publicado de ninguna de ellas
(incluyendo `runAgentTurnEndToEnd`/`emitAndDistribute`, CH-12).

## 2. Los tres caminos cerrados (heredados de CH-12 §2/§18, ver también constitution Article VI/VIII/IX)

1. **`PolicyDecision.outcome = DENY`.** `evaluatePolicyForToolCall` (CH-05) ya sabía producir este
   resultado; `runAgentTurnEndToEnd` (CH-12 §11) se detenía ahí con un `RETURN turnOneState`
   explícito. **Cerrado**: `runAgentTurnWithPolicyDenial` (seccion 11 de este capítulo) invoca
   `evaluatePolicyForToolCall`, nunca invoca `executeToolCall` (Article VI, Execution Rule 3),
   construye una observación (`AgentMessage`, `role = TOOL`) a partir del `HarnessError` que
   `PolicyDecision.reason` ya trae, y retoma el ciclo con `resumeTurnWithObservation` (helper nuevo
   de este capítulo, que replica la segunda mitad de `runAgentTurnEndToEnd` sin modificarla).
2. **`PolicyDecision.outcome = REQUIRE_APPROVAL` → `HumanInteractionService` → resolución →
   reanudación.** **Cerrado, en dos funciones separadas** (Article VIII: "una ejecución durable no
   debe mantener necesariamente un proceso abierto mientras espera intervención humana"):
   - `beginToolApprovalPause` invoca `createHumanInteractionRequest` (CH-06) sobre la
     `PolicyDecision` real, transiciona el `AgentState` a `WAITING_FOR_HUMAN` (primer uso real de
     ese estado, declarado desde CH-01, nunca ejercitado hasta este capítulo) y **termina** —
     ningún proceso queda esperando.
   - `resumeAfterHumanResolution`, invocada más tarde y por separado, invoca
     `resolveHumanInteractionRequest` (CH-06) sobre una resolución real; si
     `outcome = APPROVED`, invoca `executeToolCall` (CH-02) como si `PolicyEngine` hubiera dicho
     `ALLOW` desde el principio; si `REJECTED`, construye la misma forma de observación que el
     camino `DENY` (documentado con honestidad como una construcción de `HarnessError` que esta
     función sí hace por su cuenta — ver §3.3).
3. **`ExecutionDecision.outcome = STOP`/`CANCELLED` → terminación real.** **Cerrado**:
   `terminateAgentRunOperationally` invoca `evaluateExecutionContinuation` (CH-07) y ejecuta, por
   primera vez con código real, el mapeo que CH-07 §12 documentó solo en prosa: `CANCELLED` →
   `AgentRunStatus.CANCELLED`; `STOP` + `stopReason = MAX_RUNTIME_EXCEEDED` → `EXPIRED`; `STOP` +
   cualquier otro `stopReason` → `FAILED`. Emite el evento hacia `EventBus.distributeEvent` vía
   `emitAndDistribute` (CH-12), reutilizado sin cambios.

## 3. Decisiones de diseño centrales

### 3.1 Cinco funciones nuevas, atadas a los tres `RETURN` exactos de `runAgentTurnEndToEnd` (CH-12)

`runAgentTurnEndToEnd` (CH-12 §11) contiene, literalmente, tres puntos `IF ... RETURN` donde el
camino feliz se detenía. Este capítulo no reabre esa función (el encargo lo prohíbe explícitamente):
en cambio, escribe cinco funciones nuevas (`resumeTurnWithObservation`,
`runAgentTurnWithPolicyDenial`, `beginToolApprovalPause`, `resumeAfterHumanResolution`,
`terminateAgentRunOperationally`) que un capítulo futuro (o una revisión futura de CH-12, fuera de
este alcance) invocaría en lugar de cada uno de esos tres `RETURN`. Esto significa que
`runAgentTurnEndToEnd` sigue, hoy, deteniéndose exactamente donde CH-12 lo dejó — la sustitución
real de esos tres `RETURN` por una llamada a las funciones de este capítulo queda como deuda
intencional explícita hacia una revisión futura (seccion 9/18 del capítulo).

### 3.2 `resumeTurnWithObservation`: un helper compartido, no una reescritura de CH-12

Tres de las cinco funciones (`runAgentTurnWithPolicyDenial`, `resumeAfterHumanResolution`, y de
forma indirecta el propio flujo feliz) necesitan la misma "cola": evaluar continuación operacional,
ensamblar contexto, invocar al modelo, correr un turno más y cerrar el checkpoint — exactamente el
mismo patrón que la segunda mitad de `runAgentTurnEndToEnd` (CH-12 §11) ya estableció. Se decidió
factorizar ese patrón en una función nueva y propia de este capítulo,
`resumeTurnWithObservation`, en vez de duplicar ese bloque de pseudocódigo tres veces o de
modificar CH-12 para exponerlo. Es una función nueva (no modifica ninguna publicada), y es
deliberadamente redundante con la segunda mitad de `runAgentTurnEndToEnd` — se documenta esa
redundancia con honestidad en la seccion 11 del capítulo, en vez de ocultarla.

### 3.3 `HUMAN_APPROVAL_REJECTED`: la única vez que este capítulo construye un `HarnessError` por su cuenta

CH-12 §13 estableció que `runAgentTurnEndToEnd` "nunca construye un `HarnessError` por su cuenta" —
siempre deja que el componente dueño de la decisión construya su propio error. Ese principio no
puede aplicarse literalmente al camino `REJECTED`: `HumanInteractionResolution` (C-016, CH-06) no
tiene ningún campo de error, porque para `HumanInteractionService` un rechazo es un resultado tan
válido como una aprobación — no un fallo del componente. Como el modelo, en el turno siguiente,
necesita ver esa negativa con la misma forma que una denegación de policy (para poder razonar sobre
ambas de manera uniforme), se decidió que `resumeAfterHumanResolution` sea la única función de este
capítulo que construye un `HarnessError` por su cuenta (`category = POLICY`,
`code = "HUMAN_APPROVAL_REJECTED"`). Se documenta esta excepción explícitamente en la seccion 13 del
capítulo, señalando que es una decisión de integración, no una que le pertenezca a
`HumanInteractionService`.

### 3.4 `AgentEventType` no se redeclara en este capítulo (a diferencia de CH-12)

CH-12 §6 tuvo que redeclarar `AgentEventType` completo porque necesitaba declarar variables locales
de ese tipo (`toolEventType: AgentEventType = ...`). Este capítulo evita esa necesidad: cada llamada
a `emitAndDistribute` recibe su `eventType` como un literal `ENUM` directamente en la posición del
argumento, nunca a través de una variable tipada — así que `AgentEventType` nunca aparece como una
anotación de tipo explícita en el pseudocódigo de este capítulo, y no hizo falta redeclararlo. Sí
fue necesario, en cambio, documentar por referencia (mismo mecanismo que CH-12 §3.4 ya estableció
para `ExecutionUsage`) tres tipos embebidos sin `C-XXX` propio que sí aparecen como anotaciones de
tipo explícitas en las firmas de las funciones nuevas: `ExecutionUsage` (CH-07), `HumanInteractionOutcome`
(CH-06) y `ActorId` (CH-06) — ver seccion 6 del capítulo.

### 3.5 Hallazgo real: `AgentEventType` no tiene valores propios para `CANCELLED`/`EXPIRED`

Al escribir `terminateAgentRunOperationally` se encontró que `AgentEventType` (veinte valores,
estable desde CH-11) declara `RUN_COMPLETED` y `RUN_FAILED`, pero ningún valor distinto para un run
que termina en `CANCELLED` o `EXPIRED`. Como este capítulo decidió (§3.4) no extender
`AgentEventType`, se resolvió reutilizar `RUN_FAILED` para los tres desenlaces terminales que no son
`COMPLETED`, confiando en que el `payload` (el `AgentState.status` real) lleve la distinción que el
`eventType` por sí solo no lleva. Se documenta esto con honestidad en la seccion 14/18 del capítulo,
como una limitación real y no anticipada por el encargo original — agregar `RUN_CANCELLED`/
`RUN_EXPIRED` sería una extensión real de `AgentEventType`, fuera de este alcance.

### 3.6 `registry/*.yaml` sin tocar: la misma consecuencia mecánica que CH-12 ya encontró, verificada por segunda vez

Siguiendo el encargo con la misma literalidad que CH-12, este capítulo no modifica ninguna ficha de
`registry/components.yaml`/`registry/contracts.yaml`/`registry/glossary.yaml`. Se verificó con
`./scripts/build-mind-map` (§7) que `diagrams/mindmap/chapter-13.diagram` tiene **exactamente las
mismas 131 aristas** que `chapter-12.diagram` — un solo nodo nuevo (el nodo `CHAPTER` de `CH-13`).
Es el mismo hallazgo que CH-12 §3.6 ya documentó, confirmado por segunda vez con un capítulo de
integración distinto: el mecanismo actual de `scripts/lib/mindmap.js` no tiene ningún camino para
que un capítulo que no toca el registry agregue aristas `DEPENDS_ON`/`PRODUCES`/`CONSUMES` nuevas,
sin importar cuántas funciones reales de integración escriba. Se documenta en la seccion 9/17 del
capítulo y aquí, exactamente como información real, sin ocultarla ni forzarla.

## 4. Otras decisiones de diseño tomadas durante la ejecución

### 4.1 `call: ToolCall` llega ya resuelto — no se repite `resolveModelProposedToolCall`

`runAgentTurnWithPolicyDenial` y `beginToolApprovalPause` reciben `call: ToolCall` como parámetro,
en vez de invocar `CapabilityRegistry.resolveModelProposedToolCall` (CH-08) de nuevo. Se decidió así
porque esa resolución no varía entre el camino feliz (CH-12 §11, paso 7) y los caminos de gobierno
de este capítulo — lo único que varía es el resultado de `evaluatePolicyForToolCall` en adelante.
Repetir la resolución habría sido ruido, no una demostración nueva.

### 4.2 `constitutional_articles` del frontmatter

`P-05`/`P-10`/`P-13` (principios que ahora se cumplen también en su forma negativa/terminal, no
solo en el camino más permisivo) e `INV-06`/`INV-09`/`INV-10`/`INV-14`/`INV-15`/`INV-18`/`INV-19`/
`INV-20` (invariantes preservados, varios citados con ejecución real de punta a punta por primera
vez — en particular INV-10 e INV-15, que CH-12 había citado solo como pendientes).

### 4.3 Las seis `interleavedQuestions`, cruzando capítulos distantes

Se eligieron seis pares deliberadamente distantes: CH-01↔CH-06 (por qué hicieron falta ambos
capítulos para que `WAITING_FOR_HUMAN` tuviera una transición real), CH-07↔CH-12 (qué tuvo que
existir primero para que la tabla de CH-07 §12 dejara de ser solo prosa), CH-05↔CH-06 (por qué
`DENY` y `REJECTED` terminan pareciéndose sin que eso invada ninguna de las dos fronteras),
CH-09↔CH-06 (cerrando la pregunta que CH-12 IQ-05 dejó abierta sobre `HUMAN_INTERACTION_REQUESTED`),
CH-02↔CH-06 (cuándo se vuelven ciertas las señales que `executeToolCall` exige, en el camino de
aprobación humana) y CH-01↔CH-07 (quién construye el primer `AgentState` con un `AgentRunStatus`
terminal distinto de `COMPLETED`, y por qué eso no invade Article IV).

## 5. Archivos creados

- `book/chapters/13-integracion-caminos-de-gobierno/chapter.md` — capítulo completo (22 secciones:
  0, 1-19, 20, 21). Slug elegido: `13-integracion-caminos-de-gobierno`.
- `planes/2026-09-14-capitulo-13-integracion-caminos-de-gobierno.md` — este registro.

## 6. Archivos modificados

- `book/book.yaml` — agrega la entrada `CH-13` después de `CH-12`.
- `book/chapters/12-integracion-camino-feliz/chapter.md` — únicamente `next_chapter: null` →
  `CH-13` en el frontmatter (sin tocar ninguna otra sección ni su pseudocódigo publicado).
- `planes/2026-08-23-book-harness-como-construir-un-arnes.md` — agrega §11.7 (nota de cierre de la
  cadena de escritura, 1 capítulo piloto → 14 capítulos reales, con enlace a los planes
  individuales); no se reescribe el resto del documento.
- **Ningún archivo de `registry/`** (`components.yaml`/`contracts.yaml`/`glossary.yaml`) se
  modificó — verificado con `git status`/`git diff` antes de comitear (ver §9).

## 7. Resultado real del pipeline

Comando (desde la raíz del repo, `dist/` borrado antes para forzar un build limpio):

```text
$ rm -rf dist && ./scripts/build-all
...
▶ validate-chapter book/chapters/13-integracion-caminos-de-gobierno/chapter.md
validate-chapter: OK — secciones: 22/19, bloques pseudocode: 5, contratos introducidos: 0,
  componentes introducidos: 0
▶ validate-retrieval-set book/chapters/13-integracion-caminos-de-gobierno/chapter.md
validate-retrieval-set: OK — guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2,
  interleavedQuestions: 6, flashcards: 5, calibrationPairs: 4
...
▶ build-book-ir → OK → dist/book-ir.json (capítulos: 14 / contratos: 21 / componentes: 11 /
  glosario: 68 / flashcards (retrievalSet): 65)
▶ build-mind-map
  chapter-12.diagram: 81 nodo(s), 131 arista(s) (1 nuevo(s) en este capítulo)
  chapter-13.diagram: 82 nodo(s), 131 arista(s) (1 nuevo(s) en este capítulo)
  full-book.diagram: 82 nodo(s), 131 arista(s)
▶ build-web → OK → dist/web/ — index.html + 2 páginas de frontmatter + 14 capítulos + mapa.html
▶ build-pdf → OK → dist/book.pdf (1698085 bytes)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
```

Exit code: `0` — verificado explícitamente tras `rm -rf dist && ./scripts/build-all`, tres veces
(antes de la prueba negativa de §8, después de revertirla, y una corrida final de cierre), con
conteos idénticos las tres veces.

## 8. Evidencia de verificación concreta

### 8.1 Mapa mental acumulativo (CH-13 vs. CH-12)

`chapter-12.diagram`: 81 nodos / 131 aristas. `chapter-13.diagram`: **82 nodos / 131 aristas** — un
solo nodo nuevo (`CH-13`), **cero aristas nuevas**. `full-book.diagram` coincide exactamente con el
snapshot de `CH-13`. Mismo hallazgo que CH-12 (§3.6/§8.1 de su propio plan), confirmado por segunda
vez: el mecanismo actual del `BookMindMap` no tiene ningún camino para que un capítulo de
integración que no toca el registry agregue aristas nuevas de esos tres tipos.

### 8.2 Web

- `dist/web/chapters/CH-13.html` existe, con SVG de mapa mental inline (`grep -c '<svg'` == 1).
- Navegación prev/next verificada en ambos sentidos: `CH-12.html` contiene `href="CH-13.html"`;
  `CH-13.html` contiene `href="CH-12.html"`.
- `<svg` aparece exactamente 1 vez en cada una de las 14 páginas de capítulo (CH-00..CH-13).
- `dist/web/index.html` lista los catorce capítulos (`CH-00`..`CH-13`).
- Anchors de capítulos previos verificados intactos (1 aparición cada uno): CH-00 (`id="C-001"`),
  CH-01 (`id="CMP-001"`), CH-10 (`id="CMP-010"`), CH-11 (`id="CMP-011"`) — sin cambios.
- `CH-13.html` no tiene ningún `id="CMP-*"`/`id="C-0*"` propio (no introduce ninguno) — verificado,
  coincide con `introduces_components: []`/`introduces_contracts: []`.

### 8.3 PDF (`pypdf`)

- Build completo (CH-00..CH-13): **329 páginas** — más que el build de 13 capítulos (305 páginas,
  ver `planes/2026-09-14-capitulo-12-integracion-camino-feliz.md` §8.3); 329 > 305, confirmando el
  crecimiento esperado.
- Texto extraído del PDF completo, verificado con `pypdf.PdfReader(...).extract_text()`:
  `DENY`/`REQUIRE_APPROVAL`/`WAITING_FOR_HUMAN`/`CANCELLED`/`EXPIRED` → `True` cada uno;
  `runAgentTurnWithPolicyDenial`/`beginToolApprovalPause`/`resumeAfterHumanResolution`/
  `terminateAgentRunOperationally`/`resumeTurnWithObservation` → `True` cada uno;
  `HUMAN_APPROVAL_REJECTED`/`NOT_A_POLICY_DENIAL`/`NOT_AN_OPERATIONAL_STOP` → `True` cada uno.

### 8.4 Prueba negativa (inyectada y revertida)

Se inyectó una entidad inexistente (`bogus: NonExistentEntity = NULL`) dentro del bloque
`pseudocode` de `terminateAgentRunOperationally` → `validate-chapter` falló limpio con `exit 1` y el
mensaje exacto `Entidad no definida ("no magic entities") en bloque de pseudocódigo:
"NonExistentEntity"`. Revertido (`diff` contra el backup en `/tmp/ch13.md.bak` confirmó archivo
idéntico byte a byte; `validate-chapter`/`validate-retrieval-set` volvieron a `OK`, `exit 0`;
`rm -rf dist && ./scripts/build-all` volvió a pasar limpio con los mismos conteos: 82 nodos/131
aristas, 21 contratos, 11 componentes, 14 capítulos, 329 páginas de PDF).

Segunda nota real, encontrada durante la escritura (no una prueba negativa deliberada sino un error
real cometido y corregido): el regex de `validate-chapter` que implementa "no magic entities"
escanea **todo** el texto de un bloque ` ```pseudocode ` — incluidos los comentarios `//` — y no
solo las declaraciones de tipo. Dos comentarios del primer borrador de este capítulo (que
mencionaban, en prosa dentro del bloque, "Execution Rule 3" y una oración que empezaba con "La
reanudación...") dispararon el error real `Entidad no definida: "Execution"` / `"Rule"` / `"La"` —
palabras capitalizadas sueltas, no entidades, pero indistinguibles para el regex de un tipo
`PascalCase` real. Se corrigieron ambos comentarios (reescritos en minúsculas / sin esas palabras
sueltas) antes de la primera corrida en verde. Se documenta aquí porque es el mismo mecanismo, ya
usado deliberadamente por CH-12 (que escribe "seccion" sin tilde y en minúsculas dentro de sus
propios bloques de pseudocódigo, en vez de "Sección"), y que este capítulo no había anticipado en
su primer borrador.

### 8.5 CH-00..CH-12 no se rompieron

- `validate-chapter`/`validate-retrieval-set` de los trece siguen en verde (ver §7, corrida
  completa de `build-all`).
- Los anchors de CH-00..CH-12 no cambiaron de contenido (ver §8.2).
- Solo se editó `next_chapter` en el frontmatter de CH-12 — su cuerpo, su pseudocódigo publicado y
  su `retrieval_set` quedaron intactos.
- `registry/components.yaml`, `registry/contracts.yaml` y `registry/glossary.yaml` — sin cambios,
  verificado con `git diff` antes de comitear.

## 9. Definition of Done (restringido a este incremento)

- ✅ CH-13 completo: 22 secciones (0, 1-19, 20, 21), sin relleno — cada sección con contenido real.
- ✅ `introduces_components: []` / `introduces_contracts: []` / `modifies_contracts: []` —
  confirmado válido contra `validate-chapter` (sin error alguno) y `build-mind-map` (procesa el
  capítulo sin excepción).
- ✅ `book/book.yaml` actualizado (agrega `CH-13`); `book/chapters/12-integracion-camino-feliz/chapter.md`
  con únicamente `next_chapter: CH-13`; `registry/*.yaml` sin ninguna modificación.
- ✅ `RetrievalSet` completo con `interleavedQuestions = 6`, cruzando capítulos deliberadamente
  distantes (CH-01↔CH-06, CH-07↔CH-12, CH-05↔CH-06, CH-09↔CH-06, CH-02↔CH-06, CH-01↔CH-07).
- ✅ Pipeline completo (`build-all`) verde desde `dist/` limpio, para los 14 capítulos.
- ✅ Evidencia concreta: conteo de páginas de PDF (329 vs. 305 del build de 13 capítulos), texto
  extraído del PDF (las cinco funciones nuevas + los cuatro valores de gobierno, todos mencionados
  por nombre), anchors HTML, una prueba negativa con mensaje de error exacto y reversión confirmada
  con conteos idénticos.
- ✅ CH-00..CH-12 verificados intactos tras el cambio (salvo el campo de navegación autorizado en
  CH-12).
- ✅ Los tres caminos de la lista consolidada (§2), cerrados uno por uno, cada uno citando el
  capítulo/sección exacta de la deuda que cierra.
- ✅ Hallazgo real, no anticipado en el encargo, documentado con honestidad: `AgentEventType` no
  tiene valores propios para `CANCELLED`/`EXPIRED` (§3.5).
- ✅ Hallazgo real, confirmado por segunda vez: el mecanismo actual de `scripts/lib/mindmap.js` no
  produce aristas nuevas para un capítulo de integración que no modifica `registry/components.yaml`
  (§3.6/§8.1).
- ✅ `planes/2026-08-23-book-harness-como-construir-un-arnes.md` §11 actualizado con la nota de
  cierre de la cadena (14 capítulos, 11 componentes + 2 de integración).

## 10. Deuda intencional hacia un incremento futuro (no planeado — no hay "CH-14")

- **`runAgentTurnEndToEnd` (CH-12) sigue sin invocar, dentro de su propio cuerpo, ninguna de las
  cinco funciones de este capítulo** — los tres `RETURN` tempranos siguen ahí. Sustituirlos por una
  llamada real es, honestamente, trabajo de una revisión futura de CH-12, fuera de este alcance.
- **`AgentEventType` sin `RUN_CANCELLED`/`RUN_EXPIRED` propios** (§3.5): este capítulo reutiliza
  `RUN_FAILED` para los tres desenlaces terminales que no son `COMPLETED`.
- **Expiración de una `HumanInteractionRequest` que nadie resuelve nunca**: `HumanInteractionStatus`
  sigue teniendo solo dos estados (`PENDING`/`RESOLVED`).
- **Reintento tras `DENY`** y **múltiples aprobaciones pendientes concurrentes**: mencionados en
  prosa, no modelados con un escenario de ejemplo explícito.
- Paralelismo de tool calls, ranking semántico real de contexto, Provider Adapters reales,
  algoritmos reales de validación de schema, mecanismo real de alta de `CapabilityDescriptor`,
  autorización sobre quién puede activar un agente ajeno: deuda intencional heredada de
  CH-02..CH-12, sin cambios en este capítulo.
- Reviewers plurales, evals y orquestación multi-agente: explícitamente fuera de alcance de
  BH-v0.1 (igual que todos los capítulos anteriores).
- No hay, en este momento del libro, un tercer capítulo de integración planeado — `next_chapter`
  queda en `null` en el frontmatter de CH-13. Este es el último capítulo de la cadena encargada.
