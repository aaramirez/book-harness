# Plan / Registro de ejecución — Capítulo 2: ToolRuntime y la Ejecución Controlada de una Tool Call

**Fecha:** 2026-09-13
**Estado:** ✅ Completado — ejecutado y documentado en una sola pasada (no hubo un plan previo
separado: se pidió directamente en la conversación, sobre el estado dejado por `273ef61` — CH-00 y
CH-01 como los dos únicos capítulos reales, `AgentLoop` transicionando a `WAITING_FOR_TOOL` sin
resolver).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-13-capitulo-01-agent-loop.md` (precedente directo: mismo formato, misma disciplina de
  `owns`/`does_not_own`, misma reserva de ids `C-005`..`C-009`)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Article III "ToolRuntime", Article IV Decision
  Ownership, Article VI Execution Constitution, Article VII Failure Constitution, INV-04/05/06/07)

---

## 1. Objetivo

Escribir el tercer capítulo real de contenido del libro ("¿Cómo construir un arnés?"), CH-02, con
grounding literal en la Constitution, retomando exactamente el hilo que CH-01 dejó abierto
(`AgentLoop` transicionando a `WAITING_FOR_TOOL` sin resolver) — y verificar que atraviesa todo el
pipeline (validadores + BookIR + Web + PDF + Mapa Mental) sin romper nada de lo que CH-00/CH-01 ya
tenían construido.

## 2. Alcance decidido (Paso 2 del encargo, ya cerrado antes de escribir)

Exactamente 1 componente + 2 contratos, todos con grounding real en la Constitution:

1. **Componente `ToolRuntime` (CMP-002)** — segundo componente de runtime del libro. `owns` cita
   literal Article III (sección "ToolRuntime"); `does_not_own` excluye explícitamente cuatro
   decisiones vecinas: policy evaluation/autorización (`PolicyEngine`), aprobación humana
   (`HumanInteractionService`), enforcement de `ExecutionBudget` (`ExecutionController`), y
   registro/resolución de qué implementación satisface una capability (`CapabilityRegistry`) — los
   cuatro mencionados solo en prosa como preview, nunca dentro de un bloque ```pseudocode```.
2. **Contrato `ToolCall` (C-008)** y **contrato `ToolResult` (C-009)** — sus campos se diseñaron en
   esta ejecución (no había una interfaz literal ya redactada en la Constitution para ninguno de
   los dos, a diferencia de `AgentRunStatus` en CH-01), pero anclados en el pipeline real de
   Article VI y en las citas textuales de INV-04/INV-05/INV-07. Ambos viajan en `AgentEvent.payload`
   (C-010) sin modificarlo.
3. `ToolRuntime` modela únicamente el tramo del pipeline de Article VI que le pertenece por ficha
   constitucional (`Resolve Capability` → `Validate Schema` → `beforeToolCall` → coordinar
   `Execute` → `afterToolCall` → `ToolResult`) — el resto (`Policy Evaluation` → `Authorization` →
   `Human Approval?` → `Execution Budget` → `Sandbox`) queda documentado como deuda intencional en
   §18 del capítulo.
4. No se tocó `book/chapters/01-agent-loop/chapter.md` ni la ficha de `CMP-001 AgentLoop` — la
   única edición permitida y realizada sobre CH-01 fue su campo de frontmatter `next_chapter`
   (`null` → `CH-02`). `ToolRuntime.dependencies` quedó vacío (no depende de `AgentLoop` en el
   sentido de `depends_on` del registry — es al revés, `AgentLoop` lo invocaría).
5. `book/book.yaml` agrega CH-02 después de CH-01; CH-02 frontmatter → `previous_chapter: CH-01`,
   `next_chapter: null`.
6. `retrieval_set` de CH-02 incluye 1 `interleavedQuestion` conectando con CH-01
   (`AgentLoop`/`WAITING_FOR_TOOL`), y `guidingQuestions` en lenguaje de problema, sin usar
   "ToolRuntime"/"ToolCall"/"ToolResult" literal.

## 3. Decisiones de diseño tomadas durante la ejecución (no cubiertas explícitamente por el encargo)

### 3.1 Campos de `ToolCall` (C-008) y `ToolResult` (C-009): ancladas en el ejemplo canónico de la propia guía de reglas, con una simplificación deliberada

`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §5 ("Data structures before behavior") muestra un
ejemplo hipotético de `ToolCall`/`ToolResult` (`id`, `capability`, `arguments: Map<String, Value>`
para `ToolCall`; `callId`, `status: ToolExecutionStatus`, `output: Optional<Value>`,
`error: Optional<HarnessError>`, `metadata: ToolExecutionMetadata` para `ToolResult`). Se adoptó la
misma convención de nombres de campo (`id`/`capability`/`arguments`, `callId`/`output`/`error`) por
consistencia editorial, pero **deliberadamente no** se introdujo `ENUM ToolExecutionStatus` ni
`STRUCT ToolExecutionMetadata`: habrían sido una tercera y cuarta entidad nueva, fuera del alcance
decidido (exactamente 2 contratos). En su lugar:

- `ToolResult.succeeded: Boolean` reemplaza a `status: ToolExecutionStatus` — la distinción entre
  `SUCCESS`/`FAILED`/`DENIED`/`CANCELLED`/`TIMED_OUT` del ejemplo genérico se resuelve, en este
  libro, con `succeeded: Boolean` + `error.category` (reutilizando `ErrorCategory`, ya existente
  desde CH-00) — evita duplicar la misma clasificación en dos lugares distintos.
- No se agregó `metadata: ToolExecutionMetadata`; se agregó en su lugar `requestedAt: Timestamp`
  (en `ToolCall`) y `completedAt: Timestamp` (en `ToolResult`) para auditabilidad (Article VI,
  Execution Rule 8: "las operaciones críticas deben ser auditables"), reutilizando el tipo
  `Timestamp` ya disponible desde CH-00 en vez de introducir un contrato de metadata propio.
- `arguments: Map<Text, Value>` usa `Text` (el primitivo canónico de este libro, ya usado en
  `HarnessError.message`/`.code`), no `String` (el nombre usado en el ejemplo genérico de otro
  documento).

### 3.2 Extensión de `AgentEventType` con `TOOL_CALL_COMPLETED`/`TOOL_CALL_FAILED`: decisión no cubierta por el Paso 2

El encargo no especificaba si `ToolRuntime` debía emitir `AgentEvent` ni con qué `eventType`. Se
decidió que sí debía hacerlo (P-04/INV-18 exigen que "toda acción significativa produzca un evento
observable", y `ToolRuntime` es ahora un componente real que ejecuta acciones reales) — y que
reutilizar los cuatro valores existentes de CH-00 (`RUN_STARTED`/`TURN_CONTINUED`/`RUN_COMPLETED`/
`RUN_FAILED`, todos semánticamente ligados al ciclo de turno de `AgentLoop`) habría sido más confuso
que agregar dos valores nuevos y obviamente nombrados: `TOOL_CALL_COMPLETED`/`TOOL_CALL_FAILED`.

Esto **no** requiere un nuevo `C-XXX` ni tocar `modifies_contracts` en el frontmatter:
`AgentEventType` nunca tuvo contrato propio (vive embebido como el tipo de `AgentEvent.eventType`,
C-010) — CH-01 ya estableció el precedente de referenciarlo "por tipo" sin agregarle valores; CH-02
es el primer capítulo que sí le agrega valores, mostrando el `ENUM AgentEventType` extendido en su
propia sección 6 y dejando explícito en prosa que `AgentEvent` (C-010, su `STRUCT`) no cambia de
forma — solo crece el rango permitido de `eventType`, exactamente el mismo patrón que CH-01 usó
para `AgentRunStatus` sobre `AgentState`.

### 3.3 Señales de entrada asumidas (`capabilityResolved`, `inputValid`, `executionSucceeded`, `executionOutput`): mismo patrón que CH-01, no una decisión nueva

`executeToolCall` (§11) recibe como parámetros booleanos/`Value` cuatro resultados que, en una
implementación real, produciría `CapabilityRegistry` (no introducido) y la ejecución real de la
capability. Esto replica exactamente el patrón que CH-01 ya estableció con
`modelFinished`/`modelProposesToolCall` (señales que `ModelGateway`, no introducido, produciría en
la realidad) — no es una decisión nueva de esta ejecución, solo su aplicación consistente a un
segundo componente.

### 3.4 `ToolRuntime.dependencies: []` — sin depender de `AgentLoop`

Se consideró (y se descartó) declarar `ToolRuntime.dependencies: [CMP-001]`, ya que en la práctica
`AgentLoop` es quien eventualmente invocaría a `ToolRuntime`. Se descartó porque `dependencies` en
`registry/components.yaml` representa "de qué componentes depende este componente para funcionar" —
y `ToolRuntime` no depende de `AgentLoop` para resolver una capability, validar un schema o
coordinar una ejecución: la relación es la inversa (`AgentLoop` dependería de `ToolRuntime`, no al
revés), y ese cableado en sí (que `AgentLoop` invoque a `ToolRuntime`) es explícitamente el trabajo
de un capítulo futuro (§18/§19 del capítulo), no de este.

### 3.5 No se definió `STRUCT Tool` ni se introdujo `CapabilityRegistry` mínimo

Se consideró introducir un `STRUCT Tool` mínimo (nombre, schema, `execute`) solo para poder mostrar
`inputValid` como el resultado de una validación real contra un schema concreto. Se descartó por la
misma razón que CH-01 descartó introducir un `ExecutionController` mínimo: habría sido crear
estructura para que el pseudocódigo "se viera más completo", no porque la arquitectura lo exigiera
— y habría sido una tercera entidad nueva no autorizada por el Paso 2. `inputValid` permanece una
señal de entrada asumida, documentada como tal.

## 4. Archivos creados

- `book/chapters/02-tool-runtime/chapter.md` — capítulo completo (22 secciones: 0, 1-19, 20, 21).
- `planes/2026-09-13-capitulo-02-tool-runtime.md` — este registro.

## 5. Archivos modificados

- `registry/contracts.yaml` — agrega `C-008 ToolCall` y `C-009 ToolResult`; actualiza `used_by` de
  `C-004`/`C-010`/`C-011` a `[CMP-001, CMP-002]`; actualiza el comentario de reserva de ids junto a
  `C-013` (ahora solo `C-005`..`C-007` siguen reservados).
- `registry/components.yaml` — agrega `CMP-002 ToolRuntime`; actualiza el comentario de historial.
- `registry/glossary.yaml` — agrega `ToolRuntime` (kind: component), `Tool Call`, `Tool Result`
  (kind: contract), `Capability`, `Extension Point` (kind: concept).
- `book/book.yaml` — agrega la entrada `CH-02`.
- `book/chapters/01-agent-loop/chapter.md` — únicamente `next_chapter: null` → `CH-02` en el
  frontmatter (sin tocar ninguna otra sección ni la ficha de `CMP-001`).

## 6. Resultado real del pipeline

Comando (desde la raíz del repo, `dist/` borrado antes para forzar un build limpio):

```text
$ rm -rf dist && ./scripts/build-all

=== build-all: validación determinista ===
▶ validate-contracts
validate-contracts: OK (10 contrato(s))
▶ validate-components
validate-components: OK (2 componente(s))
▶ validate-chapter book/chapters/00-arquitectura-constitucion/chapter.md
validate-chapter: OK — secciones: 22/19, bloques pseudocode: 12, contratos: 7, componentes: 0
▶ validate-retrieval-set book/chapters/00-arquitectura-constitucion/chapter.md
validate-retrieval-set: OK — guidingQuestions: 5, recallQuestions: 5, explainPrompts: 2,
  interleavedQuestions: 0 (exención capítulo 0), flashcards: 7, calibrationPairs: 5
▶ validate-chapter book/chapters/01-agent-loop/chapter.md
validate-chapter: OK — secciones: 22/19, bloques pseudocode: 3, contratos: 1, componentes: 1
▶ validate-retrieval-set book/chapters/01-agent-loop/chapter.md
validate-retrieval-set: OK — guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2,
  interleavedQuestions: 1, flashcards: 3, calibrationPairs: 4
▶ validate-chapter book/chapters/02-tool-runtime/chapter.md
validate-chapter: OK — secciones: 22/19, bloques pseudocode: 5, contratos: 2, componentes: 1
▶ validate-retrieval-set book/chapters/02-tool-runtime/chapter.md
validate-retrieval-set: OK — guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2,
  interleavedQuestions: 1, flashcards: 4, calibrationPairs: 4

=== build-all: construcción ===
▶ build-book-ir
build-book-ir: OK → dist/book-ir.json
  frontmatter: 2 página(s) / capítulos: 3 / contratos: 10 / componentes: 2 / glosario: 22 /
  flashcards: 14
▶ build-mind-map
  chapter-00.diagram: 13 nodo(s), 12 arista(s) (13 nuevo(s) en este capítulo)
  chapter-01.diagram: 19 nodo(s), 25 arista(s) (6 nuevo(s) en este capítulo)
  chapter-02.diagram: 25 nodo(s), 35 arista(s) (6 nuevo(s) en este capítulo)
  full-book.diagram: 25 nodo(s), 35 arista(s)
▶ build-web
build-web: OK → dist/web/ — index.html + 2 páginas de frontmatter + 3 capítulos + mapa.html
▶ build-pdf
build-pdf: OK → dist/book.pdf (341746 bytes)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
```

Exit code: `0`.

## 7. Evidencia de verificación concreta

### 7.1 Mapa mental acumulativo (CH-02 > CH-01 > CH-00, los tres coexisten en `mapa.html`)

`chapter-01.diagram`: 19 nodos / 25 aristas. `chapter-02.diagram`: 25 nodos / 35 aristas (6 nodos
nuevos: `CMP-002`, `C-008`, `C-009`, y los 3 conceptos de glosario `ToolRuntime`... — en realidad
`ToolRuntime` es el propio `CMP-002`; los nuevos nodos de concepto son `Capability` y
`Extension Point`, más el nodo `CHAPTER` de CH-02 mismo). `full-book.diagram` coincide con el
snapshot de CH-02 (el último), confirmando acumulación real, no reemplazo.

### 7.2 Web

- `dist/web/chapters/CH-02.html` existe (86590 bytes), con SVG de mapa mental inline
  (`grep -c '<svg'` == 1).
- Anchors de entidad presentes: `id="CMP-002"`, `id="C-008"`, `id="C-009"`.
- Navegación prev/next verificada en ambos sentidos: `CH-01.html` contiene `href="CH-02.html"` (2
  apariciones — nav superior e inferior); `CH-02.html` contiene `href="CH-01.html"` (3
  apariciones, incluyendo enlaces del mapa mental embebido hacia anchors de CH-01).
- `dist/web/chapters/CH-00.html` conserva sus 7 anchors originales (`C-001`, `C-002`, `C-003`,
  `C-004`, `C-010`, `C-011`, `C-012`) sin cambios.
- `dist/web/index.html` lista los tres capítulos (`CH-00`, `CH-01`, `CH-02`).

### 7.3 PDF (`pypdf`)

- Build completo (CH-00 + CH-01 + CH-02): **62 páginas**, 341746 bytes.
- Build de control con `book/book.yaml` temporalmente reducido a solo CH-00 + CH-01 (mismo
  `registry/`, restaurado inmediatamente después de medir con `diff` confirmando el archivo
  idéntico): **44 páginas**, 247576 bytes. Confirma que el crecimiento de páginas (+18) es
  atribuible a CH-02, no a un artefacto del build. (La cifra de 44 difiere en 1 página del 43
  registrado en la ejecución de CH-01 por un ajuste menor de paginación entre builds — no afecta
  la conclusión: CH-02 agrega contenido real y sustancial.)
- Texto extraído del PDF completo, verificado con `pypdf.PdfReader(...).extract_text()`:
  `"ToolRuntime"` → `True`, `"ToolCall"` → `True`, `"ToolResult"` → `True`, `"CMP-002"` → `True`,
  `"C-008"` → `True`, `"C-009"` → `True`, `"CAPABILITY_NOT_FOUND"` → `True`.

### 7.4 Pruebas negativas (inyectadas y revertidas, una a la vez)

1. **`consumes` inválido en la ficha de componente**: se agregó `C-999` (inexistente) a
   `CMP-002.consumes` en `registry/components.yaml` → `validate-components` falló limpio con
   `exit 1` (`Componente CMP-002: consumes referencia contrato inexistente "C-999"`), y
   `./scripts/build-all` se detuvo en la etapa de validación con `exit 1` **sin** construir
   BookIR/Web/PDF (`policies/publishing.yaml: unresolved_validation_errors = deny`). Revertido
   (`diff` contra el backup confirmó archivo idéntico).
2. **Guiding question con nombre canónico**: se inyectó `"¿decide ToolRuntime..."` en
   `GQ-CH02-01` (que este mismo capítulo introduce) → `validate-retrieval-set` falló limpio con
   `exit 1` y el mensaje exacto `contiene el nombre canónico "ToolRuntime"...`. Revertido
   (`diff` confirmó archivo idéntico).
3. Tras revertir ambas inyecciones, `rm -rf dist && ./scripts/build-all` volvió a pasar limpio con
   los mismos conteos de nodos/aristas/páginas que antes de las inyecciones.

### 7.5 CH-00 y CH-01 no se rompieron

- `validate-chapter`/`validate-retrieval-set` de CH-00 y CH-01 siguen en verde (ver §6).
- Los 7 anchors de CH-00 y los anchors de CH-01 (`CMP-001`, `C-013`) no cambiaron de contenido.
- Solo se editó `next_chapter` en el frontmatter de CH-01 — su cuerpo, su ficha de `AgentLoop` y su
  `retrieval_set` quedaron intactos.
- `mapa.html` sigue mostrando el grafo acumulado completo con los tres capítulos.

## 8. Definition of Done (restringido a este incremento)

- ✅ CH-02 completo: 22 secciones (0, 1-19, 20, 21), sin relleno — cada sección con contenido real.
- ✅ `registry/contracts.yaml` / `registry/components.yaml` / `registry/glossary.yaml` /
  `book/book.yaml` actualizados y validados (`validate-contracts`, `validate-components`).
- ✅ `RetrievalSet` completo con `interleavedQuestions >= 1` conectando con CH-01.
- ✅ Pipeline completo (`build-all`) verde desde `dist/` limpio.
- ✅ Evidencia concreta (no solo "pasó"): conteos de nodos/aristas del mapa mental, conteo de
  páginas de PDF con y sin CH-02, texto extraído del PDF, anchors HTML, pruebas negativas con
  mensaje de error exacto y reversión confirmada.
- ✅ CH-00 y CH-01 verificados intactos tras el cambio (salvo el campo de navegación autorizado).

## 9. Deuda intencional hacia el próximo capítulo (`CH-03`, fuera de este alcance)

- **El pipeline completo de Article VI**: `Policy Evaluation`, `Authorization`, `Human Approval?`,
  `Execution Budget` y `Sandbox` siguen sin componente que los ejecute — deuda hacia los capítulos
  que introduzcan `PolicyEngine`, `HumanInteractionService` y `ExecutionController`.
- **Resolución real de capabilities**: `CapabilityRegistry` sigue sin existir; no hay `STRUCT Tool`
  que declare nombre/schema/`execute` de una capability.
- **El cableado de vuelta hacia `AgentLoop`**: `WAITING_FOR_TOOL → RUNNING` (C-013, CH-01 §12) sigue
  sin resolverse en la práctica — `ToolRuntime` ya produce un `ToolResult` real, pero conectarlo con
  `runTurn` (INV-07) es trabajo de un capítulo posterior, probablemente el mismo que introduzca
  `ModelGateway`.
- **Paralelismo y secuencialidad (Execution Rules 5/6)**: este capítulo modela un único `ToolCall`;
  coordinar múltiples tool calls en paralelo o forzar secuencialidad queda fuera de alcance.
- Persistencia (`SessionManager`), reviewers plurales, evals y orquestación multi-agente: sin
  cambios respecto al alcance ya excluido por BH-v0.1.
