# Plan / Registro de ejecución — Capítulo 3: ModelGateway y la Invocación Real del Modelo

**Fecha:** 2026-09-13
**Estado:** ✅ Completado — ejecutado y documentado en una sola pasada, sobre el estado dejado por
`a3dda24` (CH-00, CH-01, CH-02 como los tres únicos capítulos reales; `AgentLoop` y `ToolRuntime`
todavía sin un `ModelGateway` real que produjera las señales que ambos consumían como asumidas).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-13-capitulo-01-agent-loop.md` y `2026-09-13-capitulo-02-tool-runtime.md` (precedentes
  directos: mismo formato, misma disciplina de `owns`/`does_not_own`, misma reserva de ids)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Article III "ModelGateway", Article IV Decision
  Ownership, Article XII, Model Invariants INV-01/INV-02/INV-03, Article VII Failure Constitution)

---

## 1. Objetivo

Escribir el cuarto capítulo real de contenido del libro ("¿Cómo construir un arnés?"), CH-03, sobre
`ModelGateway` — el componente que finalmente conecta `AgentLoop` con el modelo real, cerrando (a
nivel de pseudocódigo demostrativo) el tramo `AgentLoop → ModelGateway → ModelResponse` que CH-01
dejó abierto — y verificar que atraviesa todo el pipeline (validadores + BookIR + Web + PDF + Mapa
Mental) sin romper nada de lo que CH-00/CH-01/CH-02 ya tenían construido.

## 2. Alcance decidido (Paso 2 del encargo, ya cerrado antes de escribir)

Exactamente 1 componente + 2 contratos, todos con grounding real en la Constitution:

1. **Componente `ModelGateway` (CMP-003)** — tercer componente de runtime del libro. `owns` cita
   literal Article III (sección "ModelGateway": selección de provider, adaptación de mensajes,
   invocación del modelo, streaming, normalización de respuestas); `does_not_own` excluye
   explícitamente cuatro decisiones vecinas: continuación cognitiva (`AgentLoop`, ya existente),
   ejecución de tool calls (`ToolRuntime`, ya existente), selección/composición de contexto
   (`ContextEngine`, preview) y policy/autorización (`PolicyEngine`, preview).
2. **Contrato `ModelRequest` (C-006)** y **contrato `ModelResponse` (C-007)** — los dos últimos ids
   que seguían reservados desde CH-01 §7 (junto con `C-005`, que sigue reservado para
   `ContextSnapshot`). `ModelRequest` transporta `List<AgentMessage>` (los mensajes ya existentes
   del turno) + `ExecutionBudget` (límites de generación relevantes) + `requestedAt`.
   `ModelResponse` normaliza la salida del proveedor hacia `finished: Boolean`,
   `content: Optional<Value>`, `proposedToolCall: Optional<RawToolCallProposal>` y `producedAt`.
3. `ModelGateway` modela únicamente el tramo que le pertenece por ficha constitucional (adaptar
   mensajes, invocar, normalizar) — la resolución de un proveedor real (`Provider Adapter`), el
   streaming real y la resolución de `proposedToolCall` hacia un `ToolCall` (C-008) real quedan
   documentados como deuda intencional en §18 del capítulo.
4. No se tocó `book/chapters/00-*`, `01-*` ni `02-*` salvo el único campo de navegación permitido:
   `book/chapters/02-tool-runtime/chapter.md` frontmatter → `next_chapter: null → CH-03`.
5. `book/book.yaml` agrega CH-03 después de CH-02; CH-03 frontmatter → `previous_chapter: CH-02`,
   `next_chapter: null`.
6. `retrieval_set` de CH-03 incluye 1 `interleavedQuestion` conectando con CH-01 (`AgentLoop`,
   `runTurn`) y CH-02 (`ToolRuntime`, `ToolCall`) a la vez, y `guidingQuestions` en lenguaje de
   problema, sin usar "ModelGateway"/"ModelRequest"/"ModelResponse" literal.

## 3. Decisión de diseño central: la frontera `ModelGateway` ↔ `ToolRuntime` (`proposedToolCall`)

Este es el punto de diseño más importante del capítulo, explícitamente señalado por el encargo.

**Problema:** `ModelResponse` debe poder representar "el modelo propuso una tool call" sin que
`ModelGateway` (a) dependa de `CMP-002 ToolRuntime`, ni (b) construya él mismo un `ToolCall` (C-008)
completo — eso invadiría la responsabilidad de *resolución/validación* que Article III asigna a
`ToolRuntime`/`CapabilityRegistry`, no a `ModelGateway` (cuyo `owns` es "normalización de
respuestas", no "resolución de capacidades").

**Solución adoptada:** un `STRUCT RawToolCallProposal` embebido dentro de `ModelResponse`
(`proposedToolCall: Optional<RawToolCallProposal>`), con exactamente dos campos:

```pseudocode
STRUCT RawToolCallProposal
    capabilityName: Text
    rawArguments: Map<Text, Value>
END
```

Deliberadamente **no** tiene `id` (`ToolCallId`) ni `requestedAt` — no es un `ToolCall` disfrazado.
`capabilityName` es texto libre sin resolver contra ningún registro de capacidades (a diferencia de
`ToolCall.capability: CapabilityId`, que ya asume una capacidad *resuelta*). Este diseño:

- **No introduce un tercer contrato registrado.** `RawToolCallProposal` vive embebido en `C-007`
  sin `C-XXX` propio — el mismo patrón que `AgentEventType` (embebido en `AgentEvent`, C-010, sin
  contrato propio desde CH-00) o `ErrorCategory` (embebido en `HarnessError`, C-011). Esto respeta
  la restricción "exactamente 2 contratos" del encargo: `registry/contracts.yaml` gana `C-006` y
  `C-007`, no un tercero.
- **No depende de `ToolRuntime`.** `ModelGateway.consumes`/`.produces` (registry/components.yaml)
  no incluyen `C-008 ToolCall` ni `C-009 ToolResult` — `ModelGateway` nunca importa ni construye
  ninguno de los dos.
- **Explícitamente documentado como deuda intencional** (seccion 18 del capítulo): resolver
  `proposedToolCall` hacia un `ToolCall` (C-008) real — validar que `capabilityName` corresponde a
  una capacidad existente, resolverla hacia un `CapabilityId`, y envolver `rawArguments` en un
  `ToolCall` con `id`/`requestedAt` propios — es trabajo de un capítulo futuro (probablemente el que
  cablee `AgentLoop` + `ModelGateway` + `ToolRuntime` de punta a punta, y que introduzca
  `CapabilityRegistry`).

Se descartó la alternativa de que `ModelGateway` construyera directamente un `ToolCall` (C-008) a
partir de la propuesta del modelo: eso habría significado que `ModelGateway` decide qué capacidad
"existe" (sin haberla resuelto contra ningún registro) y le asigna una identidad estable
(`ToolCallId`) sin que nadie haya validado el input contra un schema — exactamente las dos
responsabilidades (`resolver tools/capabilities`, `validar llamadas`) que Article III asigna
literalmente a `ToolRuntime`, no a `ModelGateway`. Section 15 (Security/Policy Implications) y la
flashcard `FC-CH03-04` documentan esta frontera explícitamente.

## 4. Otras decisiones de diseño tomadas durante la ejecución (no cubiertas explícitamente por el encargo)

### 4.1 `ModelGateway.consumes` incluye `C-004 ExecutionContext`, no solo `C-001`/`C-006`

El encargo (Paso 2, punto 1) menciona literalmente "consumes: `C-001 AgentMessage` ... + el
`ModelRequest` nuevo" sin mencionar `ExecutionContext`. Se decidió agregar `C-004` de todos modos
porque el pseudocódigo real de `invoke` (§11) recibe `execution: ExecutionContext` como parámetro
(para poblar `runId`/`sessionId`/`traceId` de los `AgentEvent` que emite) — el mismo patrón que
`CMP-001`/`CMP-002` ya establecieron (ambos incluyen `C-004` en `consumes`). Omitirlo habría dejado
el registry inconsistente con el pseudocódigo real del propio capítulo.

### 4.2 `ModelGateway` sí emite `AgentEvent` y puede fallar con `HarnessError`

El encargo no especificaba explícitamente si `ModelGateway` debía emitir eventos. Se decidió que sí
(P-04/INV-18 exigen que "toda acción significativa produzca un evento observable", y CH-01/CH-02 ya
establecieron el precedente de que todo componente real de este libro emite `AgentEvent`) —
agregando dos valores nuevos a `AgentEventType`: `MODEL_RESPONSE_RECEIVED` / `MODEL_INVOCATION_FAILED`
(mismo patrón que CH-02 agregó `TOOL_CALL_COMPLETED`/`TOOL_CALL_FAILED`). Esto no requiere un nuevo
`C-XXX` ni tocar `modifies_contracts`: `AgentEventType` nunca tuvo contrato propio.

Para el caso de fallo (`MODEL_UNAVAILABLE`, `category = MODEL`), se ancló literalmente en Article
VII: "Model unavailable → model / potentially provider fallback" (`recoverable: TRUE`,
`retryable: TRUE`). `ModelGateway.produces` incluye por tanto `C-007`, `C-010` y `C-011`.

### 4.3 El pseudocódigo de integración (`invokeModelForTurn`) es una demostración, no una modificación de `AgentLoop`

El encargo (Paso 2, punto 3) pide explícitamente mostrar, por primera vez en el libro, el tramo
`AgentLoop construye mensajes → ModelGateway.invoke(...) → ModelResponse`. Se implementó como una
segunda `FUNCTION` en la seccion 11 del capítulo (`invokeModelForTurn`), claramente separada de la
`FUNCTION invoke` que es la ficha canónica de `ModelGateway`. El texto del capítulo aclara
explícitamente que esta segunda función:

- no está declarada en `ModelGateway.consumes`/`.produces` como un método propio adicional;
- **no modifica** `CMP-001 AgentLoop` en `registry/components.yaml` (ni su `owns`/`does_not_own`,
  ni `consumes`/`produces`/`dependencies`);
- **no modifica** la firma de `runTurn` (CH-01 §11), que sigue consumiendo exactamente los mismos
  dos booleanos (`modelFinished`, `modelProposesToolCall`) que consumía antes de este capítulo.

El cableado formal (que `runTurn` reciba un `ModelResponse` real, y que `CMP-003` se agregue a
`AgentLoop.dependencies`) queda documentado como trabajo explícito de un capítulo posterior (§18/19)
— el mismo patrón que CH-02 ya usó para la relación inversa `AgentLoop`↔`ToolRuntime`.

### 4.4 `ModelGateway.dependencies: []`

Igual que CH-01/CH-02 con `AgentLoop`/`ToolRuntime`: `ModelGateway` no depende de ningún otro
componente registrado. La relación real (`AgentLoop` invocaría a `ModelGateway`) es la inversa de un
`dependency` en el sentido del registry, y ese cableado pertenece a un capítulo futuro.

### 4.5 No se introdujo `INTERFACE ModelGateway` con múltiples `IMPLEMENTATION` por proveedor

`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §7 muestra un ejemplo de
`INTERFACE ModelGateway`/`IMPLEMENTATION OpenAIModelGateway`/`IMPLEMENTATION AnthropicModelGateway`.
Se decidió no formalizarlo todavía (igual que CH-01/CH-02 no formalizaron `INTERFACE AgentLoop`/
`ToolRuntime`): este libro no modela ningún adapter de proveedor concreto en ningún capítulo hasta
ahora, y hacerlo aquí habría sido una cuarta/quinta entidad nueva fuera del alcance decidido
("exactamente 1 componente + 2 contratos"). `Provider Adapter` queda documentado como concepto
preview (seccion 5/18).

## 5. Archivos creados

- `book/chapters/03-model-gateway/chapter.md` — capítulo completo (22 secciones: 0, 1-19, 20, 21).
- `planes/2026-09-13-capitulo-03-model-gateway.md` — este registro.

## 6. Archivos modificados

- `registry/contracts.yaml` — agrega `C-006 ModelRequest` y `C-007 ModelResponse`; actualiza
  `used_by` de `C-001` (`[]` → `[CMP-003]`, primera vez que `AgentMessage` es consumido por un
  componente real), `C-004`/`C-010`/`C-011` (agrega `CMP-003`); actualiza los dos comentarios de
  reserva de ids para dejar claro que solo `C-005` (`ContextSnapshot`) sigue reservado.
- `registry/components.yaml` — agrega `CMP-003 ModelGateway`; actualiza el comentario de historial.
- `registry/glossary.yaml` — agrega `ModelGateway` (kind: component), `Model Request`,
  `Model Response` (kind: contract), `Raw Tool Call Proposal`, `Provider Adapter` (kind: concept).
- `book/book.yaml` — agrega la entrada `CH-03`.
- `book/chapters/02-tool-runtime/chapter.md` — únicamente `next_chapter: null` → `CH-03` en el
  frontmatter (sin tocar ninguna otra sección ni la ficha de `CMP-002`).

## 7. Resultado real del pipeline

Comando (desde la raíz del repo, `dist/` borrado antes para forzar un build limpio):

```text
$ rm -rf dist && ./scripts/build-all

=== build-all: validación determinista ===
▶ validate-contracts
validate-contracts: OK (12 contrato(s))
▶ validate-components
validate-components: OK (3 componente(s))
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
▶ validate-chapter book/chapters/03-model-gateway/chapter.md
validate-chapter: OK — secciones: 22/19, bloques pseudocode: 7, contratos: 2, componentes: 1
▶ validate-retrieval-set book/chapters/03-model-gateway/chapter.md
validate-retrieval-set: OK — guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2,
  interleavedQuestions: 1, flashcards: 4, calibrationPairs: 4

=== build-all: construcción ===
▶ build-book-ir
build-book-ir: OK → dist/book-ir.json
  frontmatter: 2 página(s) / capítulos: 4 / contratos: 12 / componentes: 3 / glosario: 27 /
  flashcards: 18
▶ build-mind-map
  chapter-00.diagram: 13 nodo(s), 12 arista(s)
  chapter-01.diagram: 19 nodo(s), 25 arista(s)
  chapter-02.diagram: 25 nodo(s), 35 arista(s)
  chapter-03.diagram: 31 nodo(s), 46 arista(s) (6 nuevo(s) en este capítulo)
  full-book.diagram: 31 nodo(s), 46 arista(s)
▶ build-web
build-web: OK → dist/web/ — index.html + 2 páginas de frontmatter + 4 capítulos + mapa.html
▶ build-pdf
build-pdf: OK → dist/book.pdf (446197 bytes)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
```

Exit code: `0`.

## 8. Evidencia de verificación concreta

### 8.1 Mapa mental acumulativo (CH-03 > CH-02 > CH-01 > CH-00, los cuatro coexisten en `mapa.html`)

`chapter-02.diagram`: 25 nodos / 35 aristas. `chapter-03.diagram`: **31 nodos / 46 aristas** (6
nodos nuevos: `CMP-003`, `C-006`, `C-007`, y los conceptos de glosario `Raw Tool Call Proposal` /
`Provider Adapter`, más el nodo `CHAPTER` de CH-03 mismo). Cumple el criterio del encargo (más
nodos/aristas que CH-02). `full-book.diagram` coincide exactamente con el snapshot de CH-03 (el
último), confirmando acumulación real, no reemplazo.

### 8.2 Web

- `dist/web/chapters/CH-03.html` existe (99791 bytes), con SVG de mapa mental inline
  (`grep -c '<svg'` == 1).
- Anchors de entidad presentes: `id="CMP-003"`, `id="C-006"`, `id="C-007"`.
- Navegación prev/next verificada en ambos sentidos: `CH-02.html` contiene `href="CH-03.html"` (2
  apariciones); `CH-03.html` contiene `href="CH-02.html"` (3 apariciones, incluyendo enlaces del
  mapa mental embebido hacia anchors de CH-02).
- `dist/web/chapters/CH-00.html` conserva sus 7 anchors originales (`C-001`..`C-004`, `C-010`,
  `C-011`, `C-012`); `CH-01.html` conserva `CMP-001`/`C-013`; `CH-02.html` conserva `CMP-002`/
  `C-008`/`C-009` — sin cambios.
- `dist/web/index.html` lista los cuatro capítulos (`CH-00`..`CH-03`).

### 8.3 PDF (`pypdf`)

- Build completo (CH-00 + CH-01 + CH-02 + CH-03): **86 páginas**, 446197 bytes.
- Build de control con `book/book.yaml` temporalmente reducido a CH-00..CH-02 (mismo `registry/`,
  restaurado inmediatamente después con `diff` confirmando el archivo idéntico): **62 páginas** —
  coincide exactamente con la cifra registrada al cerrar CH-02. Confirma que el crecimiento de
  páginas (+24) es atribuible por completo a CH-03, no a un artefacto del build.
- Texto extraído del PDF completo, verificado con `pypdf.PdfReader(...).extract_text()`:
  `"ModelGateway"` → `True`, `"ModelRequest"` → `True`, `"ModelResponse"` → `True`, `"CMP-003"` →
  `True`, `"C-006"` → `True`, `"C-007"` → `True`, `"RawToolCallProposal"` → `True`,
  `"MODEL_UNAVAILABLE"` → `True`.

### 8.4 Pruebas negativas (inyectadas y revertidas, una a la vez)

1. **`consumes` inválido en la ficha de componente**: se agregó `C-999` (inexistente) a
   `CMP-003.consumes` en `registry/components.yaml` → `validate-components` falló limpio con
   `exit 1` (`Componente CMP-003: consumes referencia contrato inexistente "C-999"`), y
   `./scripts/build-all` se detuvo en la etapa de validación con `exit 1` **sin** construir
   BookIR/Web/PDF (`policies/publishing.yaml: unresolved_validation_errors = deny`). Revertido
   (`diff` contra el backup confirmó archivo idéntico; `validate-components` volvió a OK).
2. **Nombre canónico en una guiding question**: se reescribió `GQ-CH03-01` (que este mismo
   capítulo introduce `ModelGateway`) para que dijera literalmente "¿Decide ModelGateway si debe
   ocurrir otro turno...?" → `validate-retrieval-set` falló limpio con `exit 1` y el mensaje exacto
   `retrievalSet.guidingQuestions[GQ-CH03-01] contiene el nombre canónico "ModelGateway", que este
   mismo capítulo introduce — las preguntas guía deben usar lenguaje de problema`. Se confirmó
   además que `./scripts/build-all` completo se detiene en la misma etapa de validación con
   `exit 1` (tras haber pasado `validate-contracts`/`validate-components`/CH-00/CH-01/CH-02, y
   fallar exactamente en `validate-retrieval-set` de CH-03), sin llegar a BookIR/Web/PDF. Revertido
   (`diff` confirmó archivo idéntico; `validate-retrieval-set` volvió a OK).
3. Tras revertir ambas inyecciones, `rm -rf dist && ./scripts/build-all` volvió a pasar limpio con
   los mismos conteos de nodos/aristas/páginas que antes de las inyecciones (exit 0).

### 8.5 CH-00, CH-01 y CH-02 no se rompieron

- `validate-chapter`/`validate-retrieval-set` de los tres siguen en verde (ver §7).
- Los anchors de CH-00 (`C-001`..`C-004`, `C-010`..`C-012`), CH-01 (`CMP-001`, `C-013`) y CH-02
  (`CMP-002`, `C-008`, `C-009`) no cambiaron de contenido.
- Solo se editó `next_chapter` en el frontmatter de CH-02 — su cuerpo, su ficha de `ToolRuntime` y
  su `retrieval_set` quedaron intactos.
- `mapa.html` sigue mostrando el grafo acumulado completo con los cuatro capítulos.

## 9. Definition of Done (restringido a este incremento)

- ✅ CH-03 completo: 22 secciones (0, 1-19, 20, 21), sin relleno — cada sección con contenido real.
- ✅ `registry/contracts.yaml` / `registry/components.yaml` / `registry/glossary.yaml` /
  `book/book.yaml` actualizados y validados (`validate-contracts`, `validate-components`).
- ✅ `RetrievalSet` completo con `interleavedQuestions >= 1` conectando con CH-01 y CH-02 a la vez.
- ✅ Pipeline completo (`build-all`) verde desde `dist/` limpio.
- ✅ Evidencia concreta (no solo "pasó"): conteos de nodos/aristas del mapa mental, conteo de
  páginas de PDF con y sin CH-03, texto extraído del PDF, anchors HTML, dos pruebas negativas con
  mensaje de error exacto y reversión confirmada.
- ✅ CH-00, CH-01 y CH-02 verificados intactos tras el cambio (salvo el campo de navegación
  autorizado en CH-02).
- ✅ Frontera `ModelGateway` ↔ `ToolRuntime` resuelta con `RawToolCallProposal` embebido (sin tercer
  contrato registrado), documentada explícitamente como deuda intencional hacia un capítulo futuro.

## 10. Deuda intencional hacia el próximo capítulo (`CH-04`, fuera de este alcance)

- **El cableado formal `AgentLoop ↔ ModelGateway`**: `runTurn` (CH-01) sigue consumiendo dos
  booleanos sueltos, no un `ModelResponse` real; `invokeModelForTurn` (CH-03 §11) es solo una
  demostración de integración.
- **La resolución de `proposedToolCall` hacia un `ToolCall` real**: requiere `CapabilityRegistry`
  (para resolver `capabilityName` hacia un `CapabilityId`) y, probablemente, el mismo capítulo que
  cablee `ModelGateway` con `ToolRuntime` de punta a punta.
- **Provider Adapters reales, streaming real**: ningún adapter de proveedor concreto ni mecanismo
  de entrega incremental se implementa en este capítulo.
- **`ContextEngine`**: `ModelRequest.messages` recibe los `AgentMessage` ya seleccionados como
  dados — la selección/composición real de contexto sigue sin componente propio (`C-005`
  `ContextSnapshot` sigue reservado).
- **`PolicyEngine`**: sigue sin existir; evaluar una `proposedToolCall` antes de resolverla sigue
  siendo una regla declarada, no exigida por código.
- Persistencia (`SessionManager`), reviewers plurales, evals y orquestación multi-agente: sin
  cambios respecto al alcance ya excluido por BH-v0.1.
