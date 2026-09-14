# Plan / Registro de ejecución — Capítulo 7: ExecutionController y los Límites Operacionales de una Ejecución

**Fecha:** 2026-09-14
**Estado:** ✅ Completado — ejecutado en una sola sesión, sobre el estado dejado por `fb9cabe` (CH-00,
CH-01, CH-02, CH-03, CH-04, CH-05, CH-06 como los siete únicos capítulos reales; `ExecutionController`
todavía como nombre de preview citado ~21 veces entre CH-00/CH-01/CH-02/CH-05 como "todavía no
introducido"; `ExecutionBudget` (C-012, CH-00) sin ningún enforcement real salvo la función huérfana
`governTurnContinuation` (CH-00 §11), que solo verifica `maxTurns` y no pertenece a ningún
componente registrado).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-13-capitulo-01-agent-loop.md` .. `2026-09-14-capitulo-06-human-interaction-service.md`
  (precedentes directos: mismo formato, misma disciplina de `owns`/`does_not_own`)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Article III "ExecutionController", Article IV
  Decision Ownership, Article IX completo — Resource and Budget Constitution —, Article II
  INV-08/INV-09/INV-10/INV-18/INV-19/INV-20, Article I P-10, Article VII Failure Constitution —
  `ErrorCategory.BUDGET`/`ErrorCategory.CANCELLATION`)

---

## 1. Objetivo

Escribir el octavo capítulo real de contenido del libro ("¿Cómo construir un arnés?"), CH-07, sobre
`ExecutionController` — el componente más referenciado como deuda pendiente hasta ahora (citado ~21
veces entre CH-00/CH-01/CH-02/CH-05 como "todavía no introducido") — y el que por fin le da dientes
reales a `ExecutionBudget` (C-012, introducido en CH-00, citado desde entonces sin que nadie lo
hiciera cumplir) — y verificar que atraviesa todo el pipeline (validadores + BookIR + Web + PDF +
Mapa Mental) sin romper nada de lo que CH-00..CH-06 ya tenían construido.

## 2. Alcance decidido (Paso 2 del encargo, ya cerrado antes de escribir)

Exactamente 1 componente + 1 contrato:

1. **Componente `ExecutionController` (CMP-007)** — séptimo componente de runtime del libro. `owns`
   cita literal Article III (sección "ExecutionController": budgets, cancellation, deadlines,
   runtime limits, operational continuation); `does_not_own` excluye explícitamente cuatro
   decisiones vecinas: decidir si otro turno de razonamiento *cognitivo* debe ocurrir (`AgentLoop`,
   ya existente — la distinción constitucional sutil entre "debe" y "puede", documentada con
   cuidado en §8 del capítulo), ejecutar tools/side effects (`ToolRuntime`, ya existente), evaluar
   policy/autorización (`PolicyEngine`, ya existente) e invocar al modelo (`ModelGateway`, ya
   existente). `consumes`: `C-003 AgentState`, `C-004 ExecutionContext`, `C-012 ExecutionBudget`
   (los tres ya existentes, ninguno modificado); `produces`: `C-010 AgentEvent`,
   `C-011 HarnessError`, `C-017 ExecutionDecision` (el contrato nuevo).
2. **Contrato nuevo `ExecutionDecision` (C-017)** — el resultado de una evaluación de
   `ExecutionController`: `runId` (RunId), `outcome` (`ExecutionOutcome` — ENUM
   `CONTINUE`/`STOP`/`CANCELLED`, tres valores, nunca un `Boolean`, mismo patrón que `PolicyOutcome`
   CH-05 y `HumanInteractionOutcome` CH-06), `stopReason` (`Optional<ExecutionStopReason>` — ENUM de
   siete valores, uno por cada campo de `ExecutionBudget`, poblado únicamente cuando
   `outcome = STOP`), `reason` (`Optional<HarnessError>`, categoría `BUDGET` o `CANCELLATION`,
   poblado cuando `outcome != CONTINUE` — primera vez que esas dos categorías, declaradas desde
   CH-00, se ejercitan en un componente real), `usage` (`ExecutionUsage`, el uso actual **embebido
   dentro de este mismo contrato nuevo** — seis campos, uno por cada dimensión de `ExecutionBudget`
   que `AgentState.currentTurn` no cubre) y `evaluatedAt` (Timestamp).
3. **Terminación del `AgentRun`**: seccion 12 documenta, en prosa (sin tocar `AgentRunStatus` ni la
   tabla de transiciones de CH-01), hacia qué estado terminal apuntaría cada `ExecutionDecision` una
   vez que un capítulo de integración futuro cablee la consulta real dentro de `AgentLoop`:
   `STOP` con `stopReason = MAX_RUNTIME_EXCEEDED` → `EXPIRED` (un deadline venció, misma familia
   semántica que la expiración de una aprobación humana ya usada en CH-01/CH-06); `STOP` con
   cualquier otro `stopReason` → `FAILED` (un límite discreto de recursos se agotó); `CANCELLED` →
   `CANCELLED`. Primera vez que este libro describe con precisión una ruta real hacia los tres
   valores de `AgentRunStatus` que Article V declaró desde CH-01 pero que ningún pseudocódigo había
   producido hasta ahora.
4. **Frontera con `AgentLoop` (CMP-001)**: NO se editó `registry/components.yaml` en la entrada de
   `CMP-001` (mismo precedente: no tocar retroactivamente componentes previos). El pseudocódigo de
   este capítulo (`evaluateExecutionContinuation`, §11) muestra a `ExecutionController` evaluando de
   forma autónoma un run contra su `ExecutionBudget` y produciendo su decisión, sin que `AgentLoop`
   cambie una sola línea. La integración real ("`AgentLoop` consulta a `ExecutionController` antes
   de decidir continuar cada turno") queda documentada en prosa (secciones 9/12/18/19) como trabajo
   de un capítulo de integración futuro.
5. No se tocó `book/chapters/00-*` a `05-*`; de CH-06 solo se tocó `next_chapter: null → CH-07` en
   el frontmatter.
6. `book/book.yaml` agrega CH-07 después de CH-06; CH-07 frontmatter → `previous_chapter: CH-06`,
   `next_chapter: null`.
7. `retrieval_set` de CH-07 incluye 2 `interleavedQuestions`: una conectando con CH-01
   (`AgentLoop`/`AgentState.currentTurn`, la conexión más natural — la operational continuation que
   `AgentLoop` excluyó desde su propio capítulo) y otra con CH-00 (`ExecutionBudget`/
   `governTurnContinuation`, la función huérfana que este capítulo por fin generaliza).
   `guidingQuestions` en lenguaje de problema, sin usar "ExecutionController"/"ExecutionDecision"
   literal (verificado con la prueba negativa de §8.4).

## 3. Decisión de diseño central: los campos de `ExecutionDecision` y el problema del "uso actual"

Como en CH-02..CH-06, no existía una interfaz previa que copiar — el diseño se ancló directamente en
Article III (owns literal), Article IV ("May the run continue operationally?"), Article IX completo
(el diagrama `AgentLoop → ExecutionController → {turns?/tool calls?/tokens?/cost?/runtime?/
concurrency?}` y la Budget Rule) e INV-08/INV-09/INV-10/INV-18/INV-19/INV-20.

**Problema de diseño 1 — el resultado no puede ser un `Boolean`.** El encargo lo pedía
explícitamente: un resultado de 3+ estados, nunca un booleano, mismo patrón que `PolicyDecision`/
`HumanInteractionResolution.outcome`. Se adoptó `ExecutionOutcome` con tres valores
(`CONTINUE`/`STOP`/`CANCELLED`) — no dos, porque un simple "puede seguir" / "no puede seguir" no
distinguiría **por qué** se detuvo (un presupuesto agotado, causado por el propio consumo del run,
frente a una cancelación explícita, una señal externa) — la misma distinción que `INV-09` e
`INV-10` exigen mantener separada.

**Problema de diseño 2 — el hueco real del "uso actual".** `C-003 AgentState` solo trackea
`currentTurn`; `C-012 ExecutionBudget` declara siete límites sin que ningún contrato registre cuánto
se ha consumido de seis de ellos (tool calls, tokens de entrada/salida, costo, runtime, concurrencia).
El encargo prohibía explícitamente resolver esto extendiendo retroactivamente `C-003`/`C-012` o
creando un contrato `C-XXX` adicional (el alcance es 1 componente + 1 contrato). Se adoptó
`ExecutionUsage`, un `STRUCT` embebido dentro del contrato nuevo (`ExecutionDecision`, C-017) — el
mismo patrón exacto que `RawToolCallProposal` embebido dentro de `ModelResponse` (CH-03): seis
campos (`toolCallsUsed`, `inputTokensUsed`, `outputTokensUsed`, `costUsed`, `runtimeMsElapsed`,
`concurrentToolsInFlight`), uno por cada dimensión de `ExecutionBudget` que `AgentState.currentTurn`
no cubre (la séptima, turnos, se sigue leyendo directamente de `AgentState.currentTurn`, sin
duplicarla). `ExecutionUsage` llega como parámetro ya resuelto a `evaluateExecutionContinuation` —
una primitiva asumida (mismo espíritu que `policyRuleFound(...)` en CH-05), documentada
explícitamente en §6/§9/§18 como una deuda real: ningún componente de este libro reporta todavía
tool calls, tokens, costo o runtime hacia esos seis contadores.

**Problema de diseño 3 — `stopReason` (siete valores) y `reason` (`HarnessError`), dos campos de
"razón" a la vez.** Se evaluó modelar solo un `ExecutionStopReason` estructurado, pero
`PolicyDecision` (CH-05) ya estableció el precedente de combinar un campo estructurado
(`policyRuleId`) con un `HarnessError` completo (`reason`) para el caso de fallo. Se adoptó el mismo
patrón: `stopReason: Optional<ExecutionStopReason>` (siete valores, uno por campo de
`ExecutionBudget`, para dispatch programático — por ejemplo, hacia qué `AgentRunStatus` apuntaría) y
`reason: Optional<HarnessError>` (para observabilidad/auditoría, INV-19/INV-20) — ambos poblados
únicamente cuando `outcome != CONTINUE`, y `stopReason` en particular nunca poblado cuando
`outcome = CANCELLED` (la cancelación no es una dimensión de presupuesto). Esto además permitió
ejercitar, por primera vez en un componente real, `ErrorCategory.BUDGET` y
`ErrorCategory.CANCELLATION` (ambos declarados desde CH-00, nunca usados por ningún componente
registrado hasta este capítulo).

**Problema de diseño 4 — la distinción constitucional sutil "debe" vs. "puede".** El encargo pedía
documentar con cuidado que `ExecutionController` decide si la ejecución PUEDE continuar
operacionalmente (límites), no si el modelo DEBERÍA seguir razonando (`AgentLoop`). Se adoptó:
`ExecutionDecision` no contiene ningún campo `AgentRunStatus`, y la primera entrada del
`does_not_own` de `CMP-007` está dedicada íntegramente a separar esta pregunta de la de `AgentLoop`,
con una nota explícita en la ficha de componente (§8) señalando que esta es la exclusión más sutil
del capítulo — no porque `ExecutionController` invada un componente vecino obviamente distinto, sino
porque las dos preguntas se sienten, en prosa informal, como la misma.

**Problema de diseño 5 — mapear `ExecutionDecision` hacia `AgentRunStatus` sin tocar `AgentLoop`.**
El encargo pedía que la terminación resultante pudiera alcanzar `FAILED`/`CANCELLED`/`EXPIRED` (los
tres valores declarados desde CH-01 pero nunca producidos). Se decidió NO agregar un campo
`AgentRunStatus` a `ExecutionDecision` (eso encroachearía sobre la propiedad exclusiva de `AgentLoop`
sobre esa máquina de estados, Article IV) — en su lugar, seccion 12 documenta en prosa una tabla de
mapeo (`STOP`+`MAX_RUNTIME_EXCEEDED` → `EXPIRED`, cualquier otro `STOP` → `FAILED`, `CANCELLED` →
`CANCELLED`), dejando explícito que ningún pseudocódigo de este capítulo produce esa transición —
mismo patrón que CH-05 usó para documentar, sin cablear, la relación entre `REQUIRE_APPROVAL` y
`WAITING_FOR_HUMAN`.

## 4. Otras decisiones de diseño tomadas durante la ejecución

### 4.1 Un solo valor nuevo de `AgentEventType` (`EXECUTION_EVALUATED`), no un par éxito/fallo

Mismo patrón que `PolicyEngine` (CH-05, `POLICY_EVALUATED`): evaluar continuación operacional nunca
"falla" en el sentido operacional — siempre produce un resultado válido (`CONTINUE`/`STOP`/
`CANCELLED`). El único caso que interrumpe la función (`EXECUTION_EVALUATION_ON_TERMINAL_STATE`) es
una violación de precondición de invocación, no un fallo de la evaluación en sí, y no emite ningún
evento (el `THROW` interrumpe antes del `EMIT`, mismo patrón que `TURN_ON_TERMINAL_STATE` en CH-01).

### 4.2 Orden fijo de comprobación: precondición → cancelación → las siete dimensiones en el orden de Article IX

`evaluateExecutionContinuation` (§11) revisa primero si `AgentRunStatus` ya es terminal (mismo
patrón que `runTurn`, CH-01), luego `cancellationRequested` (una señal externa se honra antes que
cualquier presupuesto), y luego cada dimensión de `ExecutionBudget` en el mismo orden que el
diagrama de Article IX dibuja (`turns? → tool calls? → tokens? → cost? → runtime? → concurrency?`),
desdoblando "tokens?" en `maxInputTokens`/`maxOutputTokens` para precisión — mismo nivel de detalle
que `ExecutionBudget` (C-012) ya declara. Este orden nunca se invierte, documentado explícitamente
en §11 con la misma disciplina que CH-05 aplicó al orden de sus propias comprobaciones.

### 4.3 `governTurnContinuation` (CH-00) no se retira ni se modifica

CH-00 no se edita: `governTurnContinuation` sigue existiendo tal cual, como código históricamente
sin dueño, verificando solo `maxTurns`. Este capítulo no lo reemplaza en el registry (no existe tal
mecanismo) — documenta en prosa (§1/§3/§19) que el problema que esa función motivó queda, por fin,
resuelto por un componente con `owns`/`does_not_own` propios, generalizado a las siete dimensiones.

### 4.4 `ExecutionController.dependencies: []`

Igual que CH-01..CH-06: no depende de ningún otro componente registrado. La relación real
(`AgentLoop` consultaría a `ExecutionController`; `ToolRuntime`/`ModelGateway` reportarían uso) es la
inversa de un `dependency` en el sentido del registry, y ese cableado pertenece a un capítulo futuro
— `registry/components.yaml` de `CMP-001`/`CMP-002`/`CMP-003`/`CMP-005` no se modifica en este
capítulo.

## 5. Archivos creados

- `book/chapters/07-execution-controller/chapter.md` — capítulo completo (22 secciones: 0, 1-19, 20,
  21).
- `planes/2026-09-14-capitulo-07-execution-controller.md` — este registro.

## 6. Archivos modificados

- `registry/contracts.yaml` — agrega `C-017 ExecutionDecision`; actualiza `used_by` de
  `C-003`/`C-004`/`C-010`/`C-011` (agrega `CMP-007`) y de `C-012` (de `[]` a `[CMP-007]` — primer
  consumidor real de `ExecutionBudget`); agrega comentario documentando la decisión de diseño.
- `registry/components.yaml` — agrega `CMP-007 ExecutionController`; actualiza el comentario de
  historial.
- `registry/glossary.yaml` — agrega `ExecutionController` (kind: component), `Execution Decision`
  (kind: contract), `Operational Continuation`, `Execution Usage`, `Default Stop (Fail-Safe de
  Ejecución)` (kind: concept).
- `book/book.yaml` — agrega la entrada `CH-07`.
- `book/chapters/06-human-interaction-service/chapter.md` — únicamente `next_chapter: null` →
  `CH-07` en el frontmatter (sin tocar ninguna otra sección ni la ficha de `CMP-006`).

## 7. Resultado real del pipeline

Comando (desde la raíz del repo, `dist/` borrado antes para forzar un build limpio):

```text
$ rm -rf dist && ./scripts/build-all
...
▶ validate-chapter CH-07      → OK — secciones: 22/19, bloques pseudocode: 7, contratos: 1,
  componentes: 1
▶ validate-retrieval-set CH-07 → OK — guidingQuestions: 4, interleavedQuestions: 2, flashcards: 5
...
▶ build-book-ir  → OK → dist/book-ir.json (capítulos: 8 / contratos: 17 / componentes: 7 /
  glosario: 47 / flashcards: 35)
▶ build-mind-map
  chapter-06.diagram: 49 nodo(s), 78 arista(s)
  chapter-07.diagram: 55 nodo(s), 89 arista(s) (6 nuevo(s) en este capítulo)
  full-book.diagram: 55 nodo(s), 89 arista(s)
▶ build-web → OK → dist/web/ — index.html + 2 páginas de frontmatter + 8 capítulos + mapa.html
▶ build-pdf → OK → dist/book.pdf (919829 bytes)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
```

Exit code: `0` (verificado explícitamente con `echo $?` tras `rm -rf dist && ./scripts/build-all`).

## 8. Evidencia de verificación concreta

### 8.1 Mapa mental acumulativo (CH-07 > CH-06 > CH-05 > CH-04 > CH-03 > CH-02 > CH-01 > CH-00)

`chapter-06.diagram`: 49 nodos / 78 aristas. `chapter-07.diagram`: **55 nodos / 89 aristas** (6
nodos nuevos: `CH-07`, `CMP-007`, `C-017`, y los conceptos de glosario nuevos que resuelven a nodos
propios). Cumple el criterio del encargo (más nodos/aristas que CH-06). `full-book.diagram` coincide
exactamente con el snapshot de CH-07 (el último), confirmando acumulación real.

### 8.2 Web

- `dist/web/chapters/CH-07.html` existe, con SVG de mapa mental inline (`grep -c '<svg'` == 1).
- Anchors de entidad presentes: `id="CMP-007"` (1), `id="C-017"` (1).
- Navegación prev/next verificada en ambos sentidos: `CH-06.html` contiene `href="CH-07.html"` (2
  apariciones); `CH-07.html` contiene `href="CH-06.html"` (3 apariciones).
- Anchors de capítulos previos verificados intactos (1 aparición cada uno): `CH-00.html`
  (`C-001`, `C-004`); `CH-01.html` (`CMP-001`/`C-013`); `CH-02.html` (`CMP-002`/`C-008`);
  `CH-03.html` (`CMP-003`/`C-006`); `CH-04.html` (`CMP-004`/`C-005`); `CH-05.html`
  (`CMP-005`/`C-014`); `CH-06.html` (`CMP-006`/`C-015`) — sin cambios.
- `<svg` aparece exactamente 1 vez en cada una de las 8 páginas de capítulo (CH-00..CH-07).
- `dist/web/index.html` lista los ocho capítulos (`CH-00`..`CH-07`).

### 8.3 PDF (`pypdf`)

- Build completo (CH-00..CH-07): **177 páginas** — el build de 7 capítulos (CH-00..CH-06) tenía 153
  páginas; 177 > 153, confirmando el crecimiento esperado.
- Texto extraído del PDF completo, verificado con `pypdf.PdfReader(...).extract_text()`:
  `"ExecutionController"` → `True`, `"ExecutionDecision"` → `True`, `"CMP-007"` → `True`,
  `"C-017"` → `True`, `"EXPIRED"` → `True`, `"CANCELLED"` → `True`, `"ExecutionUsage"` → `True`,
  `"ExecutionStopReason"` → `True`, `"ExecutionOutcome"` → `True`.

### 8.4 Pruebas negativas (inyectadas y revertidas, una a la vez)

1. **`consumes` inválido en la ficha de componente**: se agregó `C-999` (inexistente) a
   `CMP-007.consumes` en `registry/components.yaml` → `validate-components` falló limpio con
   `exit 1` y el mensaje exacto `Componente CMP-007: consumes referencia contrato inexistente
   "C-999"`. Revertido (`diff` contra el backup confirmó archivo idéntico; `validate-components`
   volvió a `OK (7 componente(s))`).
2. **Nombre canónico en una guiding question**: se reescribió `GQ-CH07-01` para que dijera
   literalmente "¿decide ExecutionController si esa ejecución puede continuar...?" →
   `validate-retrieval-set` falló limpio con `exit 1` y el mensaje exacto
   `retrievalSet.guidingQuestions[GQ-CH07-01] contiene el nombre canónico "ExecutionController",
   que este mismo capítulo introduce — las preguntas guía deben usar lenguaje de problema`. Se
   confirmó además que `./scripts/build-all` completo se detiene en la misma etapa de validación
   (tras haber pasado `validate-contracts`/`validate-components`/CH-00..CH-06 y `validate-chapter`
   de CH-07, fallando exactamente en `validate-retrieval-set` de CH-07), reportando
   `build-all: FALLÓ en la etapa de validación` (`policies/publishing.yaml:
   unresolved_validation_errors = deny`) sin llegar a BookIR/Web/PDF.
3. Tras revertir ambas inyecciones (`diff` confirmó archivos idénticos byte a byte), `rm -rf dist &&
   ./scripts/build-all` volvió a pasar limpio con los mismos conteos de nodos/aristas (55/89), de
   contratos/componentes (17/7), de capítulos (8) y de páginas de PDF (177, verificado de nuevo con
   `pypdf`) que antes de las inyecciones (exit 0).

### 8.5 CH-00..CH-06 no se rompieron

- `validate-chapter`/`validate-retrieval-set` de los siete siguen en verde (ver §7).
- Los anchors de CH-00 (`C-001`, `C-004`), CH-01 (`CMP-001`/`C-013`), CH-02 (`CMP-002`/`C-008`),
  CH-03 (`CMP-003`/`C-006`), CH-04 (`CMP-004`/`C-005`), CH-05 (`CMP-005`/`C-014`) y CH-06
  (`CMP-006`/`C-015`) no cambiaron de contenido.
- Solo se editó `next_chapter` en el frontmatter de CH-06 — su cuerpo, su ficha de
  `HumanInteractionService` y su `retrieval_set` quedaron intactos.
- `mapa.html` sigue mostrando el grafo acumulado completo con los ocho capítulos.

## 9. Definition of Done (restringido a este incremento)

- ✅ CH-07 completo: 22 secciones (0, 1-19, 20, 21), sin relleno — cada sección con contenido real.
- ✅ `registry/contracts.yaml` / `registry/components.yaml` / `registry/glossary.yaml` /
  `book/book.yaml` actualizados y validados (`validate-contracts`, `validate-components`).
- ✅ `RetrievalSet` completo con `interleavedQuestions = 2` conectando con CH-01 y CH-00.
- ✅ Pipeline completo (`build-all`) verde desde `dist/` limpio, para los 8 capítulos.
- ✅ Evidencia concreta (no solo "pasó"): conteos de nodos/aristas del mapa mental, conteo de
  páginas de PDF (177 vs. 153 del build de 7 capítulos), texto extraído del PDF, anchors HTML, dos
  pruebas negativas con mensaje de error exacto y reversión confirmada con conteos idénticos.
- ✅ CH-00..CH-06 verificados intactos tras el cambio (salvo el campo de navegación autorizado en
  CH-06).
- ✅ Frontera `ExecutionController` ↔ `AgentLoop` (puede vs. debe continuar) y
  `ExecutionController` ↔ `ToolRuntime`/`PolicyEngine`/`ModelGateway` (límites vs. ejecución/
  autorización/invocación) documentada explícitamente en §8/§9/§15/§18 del capítulo, sin modificar
  `CMP-001`/`CMP-002`/`CMP-003`/`CMP-005`.
- ✅ `ExecutionBudget` (C-012, CH-00) tiene, por primera vez, un componente real que lo hace cumplir
  — sin que este capítulo sobreestime lo que resuelve: el cableado real que lo conecta con
  `AgentLoop` sigue siendo, explícitamente, trabajo futuro.
- ✅ `AgentRunStatus.FAILED`/`CANCELLED`/`EXPIRED` (CH-01) tienen, por primera vez, una ruta
  documentada en prosa que los alcanzaría — sin que `AgentLoop` cambie una sola línea todavía.

## 10. Deuda intencional hacia el próximo capítulo (fuera de este alcance)

- **El cableado formal `AgentLoop → ExecutionController`**: `AgentLoop.runTurn` (CH-01) no invoca
  `evaluateExecutionContinuation` todavía.
- **El cableado formal `ToolRuntime → ExecutionController`** y **`ModelGateway → ExecutionController`**:
  ningún componente reporta tool calls, tokens o costo hacia `ExecutionUsage` en tiempo real.
- **La transición real de `AgentRunStatus` hacia `FAILED`/`CANCELLED`/`EXPIRED`**: documentada solo
  en prosa (seccion 12); ningún pseudocódigo la produce todavía.
- **El cableado formal `PolicyEngine → HumanInteractionService`** y
  **`HumanInteractionService ↔ AgentLoop`/`ToolRuntime`**: deuda heredada de CH-05/CH-06, sin
  cambios en este capítulo.
- **`SessionManager` y la persistencia real de `ExecutionUsage`**: sigue siendo, como toda
  persistencia durable, deuda heredada sin cambios en este capítulo.
- **`CapabilityRegistry`, Provider Adapters reales, streaming real, `Channel Adapter` real,
  expiración de una `HumanInteractionRequest`**: deuda heredada, sin cambios en este capítulo.
- Reviewers plurales, evals y orquestación multi-agente: explícitamente fuera de alcance de BH-v0.1
  (igual que todos los capítulos anteriores).
