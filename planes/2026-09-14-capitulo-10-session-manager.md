# Plan / Registro de ejecución — Capítulo 10: SessionManager y la Persistencia Durable de una Sesión

**Fecha:** 2026-09-14
**Estado:** ✅ Completado — ejecutado en dos sesiones (la primera se cortó por rate limit justo
después de escribir `book/chapters/10-session-manager/chapter.md`; esta continuó desde ahí sin
repetir trabajo), sobre el estado dejado por `68f19df` (CH-00..CH-09 como los diez únicos capítulos
reales; `SessionManager` citado como deuda pendiente en el `does_not_own`/seccion 9/18 de CH-01,
CH-02, CH-04, CH-06 y CH-09 — el componente más citado como preview después de `CapabilityRegistry`,
ya resuelto en CH-08).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-13-capitulo-01-agent-loop.md` (origen de `AgentState`, C-003, y de la primera mención de
  `SessionManager` como deuda pendiente)
- `2026-09-14-capitulo-06-human-interaction-service.md` (precedente directo de la frontera de
  persistencia que este capítulo tiene que trazar con cuidado: `persistHumanInteractionRequest`/
  `persistHumanInteractionResolution` como primitivas asumidas, explícitamente marcadas como
  "la persistencia real de fondo pertenece a `SessionManager`, todavía sin construir")
- `2026-09-14-capitulo-09-event-bus.md` (capítulo más reciente antes de este, formato/estilo de
  referencia; también cita `SessionManager` como el consumidor futuro que podría reconstruir
  historial a partir de eventos ya distribuidos)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Article III "SessionManager", Article IV fila
  "SessionManager → What execution history and checkpoints persist?", Article I P-08/P-23, Article
  II INV-12/INV-13/INV-18/INV-19/INV-20)

---

## 1. Objetivo

Escribir el undécimo capítulo real de contenido del libro ("¿Cómo construir un arnés?"), CH-10,
sobre `SessionManager` — el componente más citado como deuda pendiente después de
`CapabilityRegistry` (~20 menciones en CH-01/CH-02/CH-04/CH-06/CH-09) — y el que, por fin, le da un
contrato formal a `SessionState`, un nombre que la Constitution (P-08, INV-12) ya usaba desde CH-00
sin que existiera como contrato registrado. Verificar que el capítulo atraviesa todo el pipeline
(validadores + BookIR + Web + PDF + Mapa Mental) sin romper nada de lo que CH-00..CH-09 ya tenían
construido.

## 2. Alcance decidido (Paso 2 del encargo, ya cerrado antes de escribir)

Exactamente 1 componente + 1 contrato:

1. **Componente `SessionManager` (CMP-010)** — décimo componente de runtime del libro. `owns`
   (cita literal de Article III): persistencia, recuperación, branching, checkpoints,
   reconstrucción — de la historia de una sesión, que puede abarcar múltiples `AgentRun` en el
   tiempo, a diferencia de `AgentState`, que es el estado operativo de UNA ejecución en curso.
   `does_not_own`: el estado operativo de un run activo (`AgentState`, C-003, ya existente —
   producido/consumido por `AgentLoop`, CMP-001, ya introducido en CH-01 — citando P-08/INV-12 con
   precisión), persistir sus propias solicitudes pendientes de interacción humana
   (`HumanInteractionService`, CMP-006, ya introducido en CH-06 — responsabilidad ya acotada, no
   duplicada ni absorbida), decidir continuación de turno (`AgentLoop`), distribuir eventos
   (`EventBus`, CMP-009, ya introducido en CH-09 — aunque `SessionManager` podría, en un capítulo
   futuro, CONSUMIR eventos de `EventBus` para reconstruir historial; documentado en prosa en la
   seccion 9, sin modelarlo como contrato nuevo). `consumes`: `C-003 AgentState`,
   `C-004 ExecutionContext`; `produces`: `C-020 SessionState`, `C-010 AgentEvent`, `C-011
   HarnessError`.
2. **Contrato nuevo `SessionState` (C-020)** — el artefacto persistido/recuperable de una sesión:
   `sessionId` (qué sesión es), `runIds: List<RunId>` (qué ejecuciones le pertenecen),
   `latestCheckpoint: SessionCheckpoint` (embebido, sin contrato `C-XXX` propio — mismo patrón que
   `ContextBlock`/`ExecutionUsage`/`EventFilter`; desde qué punto puede reconstruirse),
   `parentCheckpointId: Optional<SessionCheckpointId>` (linaje de branching, `NULL` salvo cuando
   hubo una ramificación real), `createdAt`/`updatedAt: Timestamp`.
3. **Pseudocódigo del capítulo**: `createOrUpdateSessionCheckpoint` (crea/actualiza un `SessionState`
   a partir de un `AgentState` ya existente, reutilizando `C-003`/`C-004` sin modificarlos),
   `reconstructSessionState` (reconstruye un `SessionState` completo desde un `SessionCheckpoint` ya
   persistido — INV-13, de forma autónoma, sin que `AgentLoop`/`HumanInteractionService` cambien su
   código ya publicado) y `branchSessionFromCheckpoint` (opera la responsabilidad literal de
   branching, poblando `parentCheckpointId`).
4. No se tocó `book/chapters/00-*` a `08-*`; de CH-09 solo se tocó `next_chapter: null → CH-10` en
   el frontmatter.
5. `book/book.yaml` agrega CH-10 después de CH-09; CH-10 frontmatter → `previous_chapter: CH-09`,
   `next_chapter: null`.
6. `retrieval_set` de CH-10 incluye 2 `interleavedQuestions`: una conectando con CH-01
   (`AgentLoop`/`AgentState`, la frontera P-08/INV-12) y otra con CH-06 (`HumanInteractionService`,
   la frontera de qué persiste cada uno). `guidingQuestions` en lenguaje de problema, sin usar
   "SessionManager"/"SessionState" literal (verificado con la prueba negativa de §8.4).

## 3. Decisiones de diseño centrales

### 3.1 El nombre del contrato: `SessionState`, literal, citando P-08/INV-12

Se evaluó explícitamente un nombre alternativo (`SessionRecord`, para distinguirlo con más fuerza de
`AgentState` en la prosa) y se descartó: `P-08` e `INV-12` ya usan el nombre `SessionState` desde la
primera versión de la Constitution adoptada por este repositorio — renombrar el contrato habría
dejado a ambos citando, por su cuenta, un nombre que ya no correspondería a ningún `STRUCT` real.
Mismo patrón que `AgentRunStatus` (C-013) resolvió en CH-01 para un `ENUM` en vez de un `STRUCT`:
un nombre que la Constitution ya cita, formalizado tal cual por el capítulo que finalmente lo
construye.

### 3.2 La frontera `AgentState` (C-003) vs. `SessionState` (C-020), per P-08/INV-12

Se leyó `AgentState` completo (`runId`, `sessionId`, `agentId`, `status`, `currentTurn`, CH-00 §6)
antes de diseñar `SessionCheckpoint`. Decisión: `SessionCheckpoint.agentState` embebe una **copia
inmutable** de un `AgentState` ya producido por `AgentLoop` — nunca una referencia mutable, nunca la
fuente de verdad de la ejecución activa. `SessionManager` nunca escribe de vuelta hacia `AgentLoop`,
nunca muta el `AgentState` que recibe, y su ficha (`does_not_own`) declara explícitamente que el
estado operativo de una ejecución en curso sigue siendo propiedad exclusiva de `AgentLoop`. Esta es
la frontera que el capítulo traza con más cuidado (seccion 8/15/20), documentando literalmente qué
se rompería si se confundiera (`EP-CH10-01`, `TEST
SessionManagerNeverTreatsAnEmbeddedAgentStateAsTheActiveRunsSourceOfTruth`).

### 3.3 La frontera con `HumanInteractionService` (CH-06) — no absorber su persistencia acotada

CH-06 §11/§18 marcó explícitamente `persistHumanInteractionRequest`/
`persistHumanInteractionResolution` como primitivas asumidas cuya "persistencia real de fondo
pertenece a `SessionManager`, todavía sin construir". Se evaluó, y se descartó deliberadamente, leer
esa nota como una instrucción para que CH-10 absorbiera esa persistencia. Se decidió, en cambio, que
`HumanInteractionRequest`/`HumanInteractionResolution` siguen siendo, después de este capítulo,
responsabilidad exclusiva y acotada de `HumanInteractionService` — la nota de CH-06 se reinterpreta
en la seccion 15 de CH-10 como referida, como mucho, a que ambas primitivas *podrían* compartir
infraestructura de bajo nivel, nunca a que `SessionManager` deba poseer o interpretar el contenido de
una interacción humana. `CMP-006` no se modifica en este capítulo.

### 3.4 `ErrorCategory.PERSISTENCE`: primer fallo real del libro bajo esta categoría

Se verificó, por grep sobre los nueve capítulos previos, que ningún componente había clasificado
jamás un fallo bajo `category = PERSISTENCE` (declarada desde CH-00 entre los diez valores
originales de `ErrorCategory`) — CH-06 y CH-09 solo la mencionaron en prosa como pendiente. Se
decidió modelar `persistSessionState(sessionState) -> Boolean` como una primitiva asumida que **sí
puede fallar** (a diferencia de toda primitiva de persistencia anterior en el libro, documentadas
explícitamente como "en este incremento, no fallan") — y que, cuando falla,
`createOrUpdateSessionCheckpoint`/`branchSessionFromCheckpoint` lanzan un `HarnessError` con
`category = PERSISTENCE`, `recoverable = TRUE`, `retryable = TRUE` (mismo argumento que "HTTP 503 →
transient/retryable", Article VII). Es, deliberadamente, la primera vez que este valor del enum se
ejercita con código real.

### 3.5 Tres funciones, no dos — para ejercitar `branching` con código real

El encargo pedía, como mínimo, dos operaciones (`crear/actualizar` y `reconstruir`). Se decidió
agregar una tercera, `branchSessionFromCheckpoint`, para que `SessionState.parentCheckpointId` —
literalmente el campo de linaje que el encargo pedía modelar — tuviera al menos una función real que
lo poblara, en vez de quedar como un campo nunca ejercitado por ningún pseudocódigo del capítulo.
Esto también permite mapear, con precisión, los cinco términos de `owns` (persistencia, recuperación,
branching, checkpoints, reconstrucción) contra tres operaciones concretas: `persistir/checkpoint` →
`createOrUpdateSessionCheckpoint`; `recuperación/reconstrucción` → `reconstructSessionState`;
`branching` → `branchSessionFromCheckpoint`.

### 3.6 Ningún `ENUM SessionStatus` — la progresión se modela como cadena de checkpoints

A diferencia de `HumanInteractionStatus` (CH-06) o `EventSubscriptionStatus` (CH-09), se decidió no
introducir un `ENUM` de dos o tres estados para `SessionState`. Argumento: una sesión no tiene, en
este incremento, un lifecycle de valores discretos — su progresión real es la cadena de checkpoints
enlazados por `parentCheckpointId`, ya suficiente para expresar continuación lineal vs. ramificación
sin necesitar una segunda entidad nueva. Documentado explícitamente como decisión de alcance en
seccion 6/12/18, no como omisión.

### 3.7 Cuatro valores nuevos de `AgentEventType`, con un evento de fallo real (a diferencia de CH-06)

`SESSION_CHECKPOINT_CREATED`, `SESSION_RECONSTRUCTED`, `SESSION_BRANCHED` (uno por operación real,
mismo argumento que `HumanInteractionService` en CH-06) más `SESSION_PERSISTENCE_FAILED`
(compartido entre las dos operaciones que escriben). A diferencia de los fallos de
`HumanInteractionService` (violaciones de precondición, que nunca emiten nada antes de su `THROW`),
el fallo de `persistSessionState` ocurre *después* de construir un `SessionState` completo y válido
— el mismo tipo de fallo de infraestructura que `CAPABILITY_RESOLUTION_FAILED` (CH-08) o
`CONTEXT_SNAPSHOT_FAILED` (CH-04) ya modelaron, y por eso sí se emite un evento.

## 4. Otras decisiones de diseño tomadas durante la ejecución

### 4.1 `SessionManager.dependencies: []`

Igual que CH-01..CH-09: no depende de ningún otro componente registrado. El cableado real de
`AgentLoop → SessionManager`, la migración real de las primitivas de `HumanInteractionService`, y la
suscripción real a `EventBus` quedan, explícitamente, como trabajo de un capítulo de integración
futuro (seccion 9/18).

### 4.2 Grounding constitucional de `constitutional_articles`

`P-04` (eventos observables — este capítulo emite cuatro valores nuevos), `P-08` (la cita literal
central del capítulo), `P-23` (Amendment v1.1, "Durable execution is a core runtime property" — el
primer capítulo que cita esta enmienda por nombre para justificar `SessionCheckpoint`), `INV-12`,
`INV-13` (la cita literal para `reconstructSessionState`), `INV-18`, `INV-19`, `INV-20`.

### 4.3 Los dos ejemplos de interleaving (CH-01/CH-06)

Se eligieron los dos capítulos que más directamente motivan este capítulo por nombre:
`AgentLoop`/`AgentState` (CH-01, para la frontera P-08/INV-12 — quién produce el material que este
capítulo persiste) y `HumanInteractionService` (CH-06, para la frontera de qué persiste cada uno —
la nota explícita que este capítulo cierra sin absorber).

## 5. Archivos creados

- `book/chapters/10-session-manager/chapter.md` — capítulo completo (22 secciones: 0, 1-19, 20, 21).
- `planes/2026-09-14-capitulo-10-session-manager.md` — este registro.

## 6. Archivos modificados

- `registry/contracts.yaml` — agrega `C-020 SessionState`; actualiza `used_by` de `C-003` y `C-004`
  (agrega `CMP-010`); agrega comentario documentando la decisión de diseño.
- `registry/components.yaml` — agrega `CMP-010 SessionManager`; actualiza el comentario de
  historial.
- `registry/glossary.yaml` — agrega `SessionManager` (kind: component), `SessionState` (kind:
  contract), `Session`, `Checkpoint`, `Branching`, `Session Reconstruction` (kind: concept).
- `book/book.yaml` — agrega la entrada `CH-10`.
- `book/chapters/09-event-bus/chapter.md` — únicamente `next_chapter: null` → `CH-10` en el
  frontmatter (sin tocar ninguna otra sección ni la ficha de `CMP-009`).

## 7. Resultado real del pipeline

Comando (desde la raíz del repo, `dist/` borrado antes para forzar un build limpio):

```text
$ rm -rf dist && ./scripts/build-all
...
▶ validate-chapter book/chapters/10-session-manager/chapter.md
validate-chapter: OK — secciones: 22/19, bloques pseudocode: 8, contratos introducidos: 1,
  componentes introducidos: 1
▶ validate-retrieval-set book/chapters/10-session-manager/chapter.md
validate-retrieval-set: OK — guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2,
  interleavedQuestions: 2, flashcards: 5, calibrationPairs: 4
...
▶ build-book-ir → OK → dist/book-ir.json (capítulos: 11 / contratos: 20 / componentes: 10 /
  glosario: 62 / flashcards: 50)
▶ build-mind-map
  chapter-09.diagram: 66 nodo(s), 107 arista(s)
  chapter-10.diagram: 73 nodo(s), 118 arista(s) (7 nuevo(s) en este capítulo)
  full-book.diagram: 73 nodo(s), 118 arista(s)
▶ build-web → OK → dist/web/ — index.html + 2 páginas de frontmatter + 11 capítulos + mapa.html
▶ build-pdf → OK → dist/book.pdf (1303310 bytes)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
```

Exit code: `0` (verificado explícitamente tras `rm -rf dist && ./scripts/build-all`, y de nuevo tras
revertir las dos pruebas negativas de §8.4, con conteos idénticos: 73 nodos/118 aristas, 20
contratos, 10 componentes, 11 capítulos, 255 páginas de PDF).

## 8. Evidencia de verificación concreta

### 8.1 Mapa mental acumulativo (CH-10 > CH-09 > ... > CH-00)

`chapter-09.diagram`: 66 nodos / 107 aristas. `chapter-10.diagram`: **73 nodos / 118 aristas** (7
nodos nuevos: `CH-10`, `CMP-010`, `C-020`, y los cuatro conceptos de glosario nuevos con nodo propio
— `Session`, `Checkpoint`, `Branching`, `Session Reconstruction`; `SessionManager`/`SessionState`,
`kind: component`/`kind: contract` en el glosario, no generan nodo propio, ya representados por
`CMP-010`/`C-020`). Cumple el criterio del encargo (más nodos/aristas que CH-09). `full-book.diagram`
coincide exactamente con el snapshot de CH-10 (el último), confirmando acumulación real.

Aristas confirmadas explícitamente (grafo acumulado):

```text
"CMP-010" -> "C-010" [label="PRODUCES", ...];
"CMP-010" -> "C-011" [label="PRODUCES", ...];
"CMP-010" -> "C-020" [label="PRODUCES", ...];
"C-003" -> "CMP-010" [label="CONSUMES", ...];   ← C-003 introducido en CH-00, diez capítulos antes
"C-004" -> "CMP-010" [label="CONSUMES", ...];   ← C-004 introducido en CH-00, diez capítulos antes
```

### 8.2 Web

- `dist/web/chapters/CH-10.html` existe, con SVG de mapa mental inline (`grep -c '<svg'` == 1).
- Anchors de entidad presentes: `id="CMP-010"` (1), `id="C-020"` (1).
- Navegación prev/next verificada en ambos sentidos: `CH-09.html` contiene `href="CH-10.html"`;
  `CH-10.html` contiene `href="CH-09.html"`.
- Anchors de capítulos previos verificados intactos (1 aparición cada uno): CH-00 (`C-001`), CH-01
  (`CMP-001`/`C-013`), CH-02 (`CMP-002`/`C-008`), CH-03 (`CMP-003`/`C-006`), CH-04
  (`CMP-004`/`C-005`), CH-05 (`CMP-005`/`C-014`), CH-06 (`CMP-006`/`C-015`), CH-07
  (`CMP-007`/`C-017`), CH-08 (`CMP-008`/`C-018`), CH-09 (`CMP-009`/`C-019`) — sin cambios.
- `<svg` aparece exactamente 1 vez en cada una de las 11 páginas de capítulo (CH-00..CH-10).
- `dist/web/index.html` lista los once capítulos (`CH-00`..`CH-10`).

### 8.3 PDF (`pypdf`)

- Build completo (CH-00..CH-10): **255 páginas** — el build de 10 capítulos (CH-00..CH-09) tenía 229
  páginas (ver `planes/2026-09-14-capitulo-09-event-bus.md` §8.3); 255 > 229, confirmando el
  crecimiento esperado.
- Texto extraído del PDF completo, verificado con `pypdf.PdfReader(...).extract_text()`:
  `"SessionManager"` → `True`, `"SessionState"` → `True`, `"CMP-010"` → `True`, `"C-020"` → `True`,
  `"SessionCheckpoint"` → `True`, `"parentCheckpointId"` → `True`, `"PERSISTENCE"` → `True`.

### 8.4 Pruebas negativas (inyectadas y revertidas, una a la vez)

1. **`produces` inválido en la ficha de componente**: se agregó `C-999` (inexistente) a
   `CMP-010.produces` en `registry/components.yaml` → `validate-components` falló limpio con
   `exit 1` y el mensaje exacto `Componente CMP-010: produces referencia contrato inexistente
   "C-999"`. Revertido (`diff` contra el backup en `/tmp/components.yaml.bak` confirmó archivo
   idéntico; `validate-components` volvió a `OK (10 componente(s))`, `exit 0`).
2. **Nombre canónico en una guiding question**: se reescribió `GQ-CH10-01` para que dijera
   literalmente "¿Decide SessionManager quién persiste, recupera y reconstruye la historia que
   abarca esas múltiples ejecuciones...?" → `validate-retrieval-set` falló limpio con `exit 1` y el
   mensaje exacto `retrievalSet.guidingQuestions[GQ-CH10-01] contiene el nombre canónico
   "SessionManager", que este mismo capítulo introduce — las preguntas guía deben usar lenguaje de
   problema`. Revertido (`diff` contra el backup en `/tmp/ch10.md.bak` confirmó archivo idéntico;
   `validate-retrieval-set` volvió a `OK`, `exit 0`).
3. Tras revertir ambas inyecciones (`diff` confirmó archivos idénticos byte a byte), `rm -rf dist &&
   ./scripts/build-all` volvió a pasar limpio con los mismos conteos de nodos/aristas (73/118), de
   contratos/componentes (20/10), de capítulos (11) y de páginas de PDF (255, verificado de nuevo
   con `pypdf`) que antes de las inyecciones (exit 0).

### 8.5 CH-00..CH-09 no se rompieron

- `validate-chapter`/`validate-retrieval-set` de los diez siguen en verde (ver §7, corrida completa
  de `build-all`).
- Los anchors de CH-00..CH-09 no cambiaron de contenido (ver §8.2).
- Solo se editó `next_chapter` en el frontmatter de CH-09 — su cuerpo, su ficha de `EventBus` y su
  `retrieval_set` quedaron intactos.
- `mapa.html` sigue mostrando el grafo acumulado completo con los once capítulos.

## 9. Definition of Done (restringido a este incremento)

- ✅ CH-10 completo: 22 secciones (0, 1-19, 20, 21), sin relleno — cada sección con contenido real.
- ✅ `registry/contracts.yaml` / `registry/components.yaml` / `registry/glossary.yaml` /
  `book/book.yaml` actualizados y validados (`validate-contracts`, `validate-components`).
- ✅ `RetrievalSet` completo con `interleavedQuestions = 2` conectando con CH-01 y CH-06.
- ✅ Pipeline completo (`build-all`) verde desde `dist/` limpio, para los 11 capítulos.
- ✅ Evidencia concreta: conteos de nodos/aristas del mapa mental, conteo de páginas de PDF (255 vs.
  229 del build de 10 capítulos), texto extraído del PDF, anchors HTML, dos pruebas negativas con
  mensaje de error exacto y reversión confirmada con conteos idénticos.
- ✅ CH-00..CH-09 verificados intactos tras el cambio (salvo el campo de navegación autorizado en
  CH-09).
- ✅ Frontera `SessionManager` ↔ `AgentState`/`AgentLoop` (P-08/INV-12) y `SessionManager` ↔
  `HumanInteractionService` (persistencia acotada de CH-06) documentada explícitamente en
  §8/§9/§15/§20 del capítulo, sin modificar ningún componente previo.
- ✅ `SessionManager` cierra, con código real, la última fila de la tabla de Decision Ownership de
  Article IV que seguía sin componente propio (`AgentCore` sigue siendo el único nombre de Article
  III todavía en preview).
- ✅ Primer fallo real del libro clasificado bajo `ErrorCategory.PERSISTENCE`, declarada desde CH-00
  sin que ningún componente la hubiera ejercitado hasta este capítulo.

## 10. Deuda intencional hacia el próximo capítulo (fuera de este alcance)

- **El cableado real `AgentLoop → SessionManager`**: `AgentLoop.runTurn` no invoca
  `createOrUpdateSessionCheckpoint` en ningún punto.
- **La migración real de `HumanInteractionService`**: sus primitivas de persistencia siguen sin
  invocar ningún mecanismo real de `SessionManager` — deliberado, ver §3.3.
- **La suscripción real a `EventBus`**: no modelada como código, solo como relación en prosa.
- **Mecanismo real de fusión de ramas (`merge`)**: `branchSessionFromCheckpoint` solo crea, nunca
  combina.
- **`ENUM SessionStatus`, expiración o archivado de una sesión**: no modelado.
- **Autorización sobre quién puede reconstruir o ramificar la sesión de otro agente**: señalado
  explícitamente como límite de seguridad real, no silenciado.
- **Gobernanza de datos (P-22)**, **mecanismo real de almacenamiento detrás de
  `persistSessionState`**: fuera de alcance de BH-v0.1.
- **`AgentCore`**: de los once nombres de Article III, el único que sigue siendo únicamente una
  palabra en la tabla de preview.
- Reviewers plurales, evals y orquestación multi-agente: explícitamente fuera de alcance de BH-v0.1.
