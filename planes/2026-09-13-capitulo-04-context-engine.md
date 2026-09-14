# Plan / Registro de ejecución — Capítulo 4: ContextEngine y Qué Ve Realmente el Modelo

**Fecha:** 2026-09-13 / 2026-09-14
**Estado:** ✅ Completado — ejecutado en dos sesiones (la primera se cortó por rate limit justo
después de escribir `book/chapters/04-context-engine/chapter.md`; esta continúa desde ahí sin
repetir el trabajo ya hecho), sobre el estado dejado por `2bca443` (CH-00, CH-01, CH-02, CH-03 como
los cuatro únicos capítulos reales; `ModelRequest`/`ModelGateway` ya existentes, `ContextSnapshot`
todavía como el único id reservado desde CH-01).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-13-capitulo-01-agent-loop.md`, `2026-09-13-capitulo-02-tool-runtime.md` y
  `2026-09-13-capitulo-03-model-gateway.md` (precedentes directos: mismo formato, misma disciplina
  de `owns`/`does_not_own`, misma reserva de ids)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Article III "ContextEngine", Article IV Decision
  Ownership, Article I P-01/P-14, Article VII Failure Constitution — `ErrorCategory.CONTEXT`)

---

## 1. Objetivo

Escribir el quinto capítulo real de contenido del libro ("¿Cómo construir un arnés?"), CH-04, sobre
`ContextEngine` — el componente que decide qué debería saber el modelo, cerrando la última pregunta
de Article IV que seguía sin componente real ("`ContextEngine` → What should the model know?") — y
verificar que atraviesa todo el pipeline (validadores + BookIR + Web + PDF + Mapa Mental) sin
romper nada de lo que CH-00/CH-01/CH-02/CH-03 ya tenían construido.

## 2. Alcance decidido (Paso 2 del encargo, ya cerrado antes de escribir)

Exactamente 1 componente + 1 contrato, con grounding real en la Constitution:

1. **Componente `ContextEngine` (CMP-004)** — cuarto componente de runtime del libro. `owns` cita
   literal Article III (sección "ContextEngine": selección, ranking, composición, compaction,
   context budgets, provenance); `does_not_own` excluye explícitamente cuatro decisiones vecinas:
   invocar al modelo (`ModelGateway`, ya existente), decidir continuación del turno (`AgentLoop`,
   ya existente), persistir/recuperar historial de sesión (`SessionManager`, preview) y
   policy/autorización sobre qué información puede verse (`PolicyEngine`, preview) — esta última
   distinta, deliberadamente, de "seleccionar por relevancia", que sí le pertenece.
2. **Contrato `ContextSnapshot` (C-005)** — el único id que seguía reservado desde CH-01 §7. Diseñado
   con `blocks: List<ContextBlock>` (cada `ContextBlock` con `provenance`/`content`/`compacted`,
   embebido sin `C-XXX` propio), `budget: ExecutionBudget` (C-012 reutilizado sin modificar) y
   `estimatedTokens: Integer` (campo simple embebido, mismo patrón que `RawToolCallProposal` en
   CH-03) + `producedAt: Timestamp`.
3. Frontera con `ModelRequest` (C-006, ya existente): NO se modifica (`modifies_contracts: []`) —
   el cableado `ContextSnapshot.blocks → ModelRequest.messages` queda documentado como deuda
   intencional hacia un capítulo futuro (§18/19 del capítulo).
4. No se tocó `book/chapters/00-*`, `01-*` ni `02-*`; de CH-03 solo se tocó
   `next_chapter: null → CH-04` en el frontmatter.
5. `book/book.yaml` agrega CH-04 después de CH-03; CH-04 frontmatter →
   `previous_chapter: CH-03`, `next_chapter: null`.
6. `retrieval_set` de CH-04 incluye 1 `interleavedQuestion` conectando con CH-03 (`ModelGateway`/
   `ModelRequest`) y `guidingQuestions` en lenguaje de problema, sin usar "ContextEngine"/
   "ContextSnapshot" literal.

## 3. Decisión de diseño central: los campos de `ContextSnapshot` (sin interfaz literal previa)

Como en CH-02/CH-03, no existía una interfaz previa que copiar — el diseño se ancló directamente en
Article III (owns: selección, ranking, composición, compaction, context budgets, provenance) y en
P-01/P-14.

**Problema de diseño:** `ContextSnapshot` debe representar, a la vez, (a) qué material sobrevivió
la selección, (b) de dónde vino cada fragmento (provenance), (c) si tuvo que resumirse
(compaction), y (d) contra qué presupuesto se validó — sin inventar un tipo de presupuesto nuevo
(`ExecutionBudget`, C-012, ya existe desde CH-00 con `maxInputTokens`) y sin fragmentar la
responsabilidad hacia componentes que esta Constitution no reconoce (`Compactor`/`Summarizer`, que
sí aparecen en el outline general pero no en `constitution/ARCHITECTURE_CONSTITUTION.md` Article
III de este proyecto).

**Solución adoptada:**

```pseudocode
STRUCT ContextBlock
    provenance: Text
    content: Value
    compacted: Boolean
END

STRUCT ContextSnapshot
    blocks: List<ContextBlock>
    budget: ExecutionBudget
    estimatedTokens: Integer
    producedAt: Timestamp
END
```

- **`ContextBlock` embebido, sin contrato `C-XXX` propio** — mismo patrón que `RawToolCallProposal`
  (embebido en `ModelResponse`, CH-03) o `AgentEventType` (embebido en `AgentEvent`, CH-00). Esto
  respeta la restricción "exactamente 1 contrato registrado" del encargo: `registry/contracts.yaml`
  gana únicamente `C-005`.
- **`blocks` es una `List` ordenada** — el orden ES el ranking ya resuelto (el primer bloque es el
  de mayor prioridad), en vez de necesitar un campo de prioridad numérico adicional.
- **`provenance: Text`** en cada `ContextBlock` — la cita literal de Article III ("provenance")
  materializada como campo real, no solo como concepto de prosa.
- **`compacted: Boolean`** en cada `ContextBlock` — materializa "compaction" (owns literal) sin
  introducir un componente `Compactor` separado: la transformación ocurre dentro de
  `ContextEngine` mismo, vía una primitiva (`compact(...)`, análoga a `beforeToolCall`/
  `afterToolCall` de CH-02), y el campo booleano deja explícito, por bloque, si ocurrió.
- **`budget: ExecutionBudget`** — se evaluó extender `ExecutionBudget` (C-012) con un campo nuevo de
  "presupuesto de contexto", pero sus campos ya existentes (`maxInputTokens`) alcanzan exactamente
  para expresar el límite relevante; reutilizarlo sin modificarlo evita un tipo de presupuesto
  duplicado y seis capítulos después sigue siendo el único `STRUCT` de presupuesto del libro.
- **`estimatedTokens: Integer`** — el campo simple, embebido y sin contrato propio que sí hacía
  falta: `ExecutionBudget` solo expresa límites máximos, ningún campo de "cuánto se usó". Se agregó
  directamente a `ContextSnapshot`, exactamente el patrón que el encargo autorizó explícitamente
  ("mismo patrón que `RawToolCallProposal` embebido en `ModelResponse` en CH-03").

**Alternativa descartada:** modificar `ExecutionBudget` (C-012) agregando `maxContextBlocks` o
similar. Se descartó porque (a) el encargo pedía evaluar `ExecutionBudget` primero y solo agregar un
campo embebido en `ContextSnapshot` si no alcanzaba, y `maxInputTokens` sí alcanza para expresar el
límite real que `assembleContextSnapshot` valida; (b) modificar `C-012` habría requerido declarar
`modifies_contracts: [C-012]` y actualizar `modified_by` en el registry, una superficie de cambio
mayor a la necesaria para un capítulo que ya introduce su propio contrato nuevo.

## 4. Otras decisiones de diseño tomadas durante la ejecución

### 4.1 El algoritmo de `assembleContextSnapshot` es real, no una señal externa asumida

A diferencia de `executeToolCall` (CH-02) o `invoke` (CH-03) — que reciben como "señal externa
asumida" el resultado de una decisión que un componente futuro tomaría (`capabilityResolved`,
`providerFinished`) — `ContextEngine` posee literalmente la selección/ranking/composición/
compaction (Article III, `owns`). Por eso `assembleContextSnapshot` no recibe un booleano
"yaSeleccionado": recorre `candidates: List<AgentMessage>` (material real, ya existente desde
CH-00, no una señal de un componente sin construir) y decide, greedy y determinísticamente, para
cada uno, si cabe completo, si debe compactarse, o si queda fuera. Es el primer `FUNCTION` del libro
que usa `FOR EACH` sobre una lista — CH-01/CH-02/CH-03 solo usaron `IF`/`ELSE` sobre una única
entidad de entrada.

### 4.2 Primer uso real de `ErrorCategory.CONTEXT`

`ErrorCategory` (C-011, CH-00) declara `CONTEXT` desde la primera versión de la Constitution, pero
ningún componente lo había ejercitado hasta este capítulo. `CONTEXT_BUDGET_EXHAUSTED`
(`recoverable: TRUE`, `retryable: FALSE`, mismo patrón que `TOOL_INPUT_SCHEMA_MISMATCH` de CH-02) es
el primer fallo real bajo esa categoría — se documenta explícitamente en §13 del capítulo como un
hito narrativo (el 3er de 8 valores de `ErrorCategory` ejercitados hasta ahora: `VALIDATION`,
`TOOL`, `MODEL`, y ahora `CONTEXT`).

### 4.3 La frontera `ContextEngine` ↔ `PolicyEngine` (seleccionar por relevancia vs. autorizar visibilidad)

El encargo pedía documentar esta distinción "con cuidado, es un límite constitucional real". Se
dedicó la sección 15 completa (Security/Policy Implications) a separar explícitamente "¿es esto
relevante?" (P-14, `ContextEngine`) de "¿puede verse esto en absoluto?" (Article IV, `PolicyEngine`
→ "May this action occur?"). `assembleContextSnapshot` recibe `candidates` bajo la precondición
documentada de que ya llegó autorizado — el mismo patrón de "señal externa asumida" que
`capabilityResolved` (CH-02), pero aplicado aquí a una precondición sobre el parámetro de entrada en
vez de a un booleano explícito, porque la autorización de visibilidad no es una decisión que
`ContextEngine` deba ni siquiera empaquetar como señal — directamente no le pertenece verificarla.

### 4.4 No se introduce ningún `Compactor`/`Summarizer`/`ContextProvider` como componente propio

El outline general (`reference/md/Estructura_Libro_Construyendo_un_Agent_Harness_v0.2.md`, Parte
IV, capítulos 7-9) fragmenta este territorio en `ContextBuilder`, `ContextProvider` (interfaz con
implementaciones como `GitContextProvider`), y `Summarizer`/`Compactor` para context budgets. Este
capítulo documenta explícitamente, en una nota editorial dentro de §3 y de nuevo en §18, que esta
Constitution (Article III de este proyecto) consolida todo ese territorio en `ContextEngine` — y
que ningún capítulo futuro de este libro debería introducir esos nombres como componentes nuevos.

### 4.5 `ContextEngine.dependencies: []`

Igual que CH-01/CH-02/CH-03: `ContextEngine` no depende de ningún otro componente registrado. La
relación real (`ModelGateway` consumiría `ContextSnapshot.blocks` para construir `ModelRequest.
messages`) es la inversa de un `dependency` en el sentido del registry, y ese cableado pertenece a
un capítulo futuro — `registry/contracts.yaml` no incluye `C-006` en `modifies_contracts` de este
capítulo.

## 5. Archivos creados

- `book/chapters/04-context-engine/chapter.md` — capítulo completo (22 secciones: 0, 1-19, 20, 21;
  1102 líneas).
- `planes/2026-09-13-capitulo-04-context-engine.md` — este registro.

## 6. Archivos modificados

- `registry/contracts.yaml` — agrega `C-005 ContextSnapshot`; actualiza `used_by` de `C-001`
  (`[CMP-003]` → `[CMP-003, CMP-004]`), `C-003` (`[CMP-001]` → `[CMP-001, CMP-004]`), `C-004`
  (agrega `CMP-004`), `C-010`/`C-011` (agrega `CMP-004`); actualiza los dos comentarios de reserva
  de ids para dejar explícito que ya no queda ningún id reservado del lote original
  `C-005`..`C-009` (CH-01 §7).
- `registry/components.yaml` — agrega `CMP-004 ContextEngine`; actualiza el comentario de
  historial.
- `registry/glossary.yaml` — agrega `ContextEngine` (kind: component), `Context Snapshot` (kind:
  contract), `Context Block`, `Provenance`, `Context Budget` (kind: concept).
- `book/book.yaml` — agrega la entrada `CH-04`.
- `book/chapters/03-model-gateway/chapter.md` — únicamente `next_chapter: null` → `CH-04` en el
  frontmatter (sin tocar ninguna otra sección ni la ficha de `CMP-003`).

## 7. Resultado real del pipeline

Comando (desde la raíz del repo, `dist/` borrado antes para forzar un build limpio):

```text
$ rm -rf dist && ./scripts/build-all

=== build-all: validación determinista ===
▶ validate-contracts
validate-contracts: OK (13 contrato(s))
▶ validate-components
validate-components: OK (4 componente(s))
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
▶ validate-chapter book/chapters/04-context-engine/chapter.md
validate-chapter: OK — secciones: 22/19, bloques pseudocode: 5, contratos: 1, componentes: 1
▶ validate-retrieval-set book/chapters/04-context-engine/chapter.md
validate-retrieval-set: OK — guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2,
  interleavedQuestions: 1, flashcards: 3, calibrationPairs: 4

=== build-all: construcción ===
▶ build-book-ir
build-book-ir: OK → dist/book-ir.json
  frontmatter: 2 página(s) / capítulos: 5 / contratos: 13 / componentes: 4 / glosario: 32 /
  flashcards: 21
▶ build-mind-map
  chapter-00.diagram: 13 nodo(s), 12 arista(s)
  chapter-01.diagram: 19 nodo(s), 25 arista(s)
  chapter-02.diagram: 25 nodo(s), 35 arista(s)
  chapter-03.diagram: 31 nodo(s), 46 arista(s)
  chapter-04.diagram: 37 nodo(s), 57 arista(s) (6 nuevo(s) en este capítulo)
  full-book.diagram: 37 nodo(s), 57 arista(s)
▶ build-web
build-web: OK → dist/web/ — index.html + 2 páginas de frontmatter + 5 capítulos + mapa.html
▶ build-pdf
build-pdf: OK → dist/book.pdf (551206-551209 bytes según pasada, variación de metadata/timestamp)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
```

Exit code: `0`.

## 8. Evidencia de verificación concreta

### 8.1 Mapa mental acumulativo (CH-04 > CH-03 > CH-02 > CH-01 > CH-00, los cinco coexisten en `mapa.html`)

`chapter-03.diagram`: 31 nodos / 46 aristas. `chapter-04.diagram`: **37 nodos / 57 aristas** (6
nodos nuevos: `CMP-004`, `C-005`, y los conceptos de glosario `ContextEngine`/`ContextBlock`/
`Provenance`/`Context Budget` — nota: el término `ContextEngine` de glosario resuelve al mismo nodo
que `CMP-004` en el grafo, y el `CHAPTER` de CH-04 mismo). Cumple el criterio del encargo (más
nodos/aristas que CH-03). `full-book.diagram` coincide exactamente con el snapshot de CH-04 (el
último), confirmando acumulación real, no reemplazo.

### 8.2 Web

- `dist/web/chapters/CH-04.html` existe, con SVG de mapa mental inline (`grep -c '<svg'` == 1).
- Anchors de entidad presentes: `id="CMP-004"` (1), `id="C-005"` (1).
- Navegación prev/next verificada en ambos sentidos: `CH-03.html` contiene `href="CH-04.html"` (2
  apariciones); `CH-04.html` contiene `href="CH-03.html"` (3 apariciones, incluyendo enlaces del
  mapa mental embebido hacia anchors de CH-03).
- Anchors de capítulos previos verificados intactos: `CH-00.html` conserva `C-001`..`C-004`,
  `C-010`..`C-012` (1 aparición cada uno); `CH-01.html` conserva `CMP-001`/`C-013`; `CH-02.html`
  conserva `CMP-002`/`C-008`/`C-009`; `CH-03.html` conserva `CMP-003`/`C-006`/`C-007` — sin cambios.
- `dist/web/index.html` lista los cinco capítulos (`CH-00`..`CH-04`).

### 8.3 PDF (`pypdf`)

- Build completo (CH-00..CH-04): **103 páginas**.
- Comparación contra el build de 4 capítulos: el registro de CH-03 documentó 86 páginas para
  CH-00..CH-03 — 103 > 86, confirmando el crecimiento esperado. (No se repitió un build de control
  completo con CH-04 removido de `book/book.yaml` en esta sesión porque los registries ya
  referencian `CH-04` desde `introduced_in`/`modified_by`; remover solo la entrada de `book.yaml`
  sin revertir también los registries produce un `validate-contracts: FALLÓ` esperado
  — `Contrato C-005: introduced_in "CH-04" no existe en book/book.yaml` — confirmando la
  consistencia cruzada del pipeline, aunque no aísla un conteo de páginas de control en esta
  pasada.)
- Texto extraído del PDF completo, verificado con `pypdf.PdfReader(...).extract_text()`:
  `"ContextEngine"` → `True`, `"ContextSnapshot"` → `True`, `"CMP-004"` → `True`, `"C-005"` →
  `True`, `"ContextBlock"` → `True`, `"CONTEXT_BUDGET_EXHAUSTED"` → `True`.

### 8.4 Pruebas negativas (inyectadas y revertidas, una a la vez)

1. **`consumes` inválido en la ficha de componente**: se agregó `C-999` (inexistente) a
   `CMP-004.consumes` en `registry/components.yaml` → `validate-components` falló limpio con
   `exit 1` y el mensaje exacto `Componente CMP-004: consumes referencia contrato inexistente
   "C-999"`; `./scripts/build-all` se detuvo en la etapa de validación con `exit 0` de shell pero
   reportando `build-all: FALLÓ en la etapa de validación` internamente (`policies/publishing.yaml:
   unresolved_validation_errors = deny`), **sin** construir BookIR/Web/PDF. Revertido (`diff`
   contra el backup confirmó archivo idéntico; `validate-components` volvió a OK).
2. **Nombre canónico en una guiding question**: se reescribió `GQ-CH04-01` para que dijera
   literalmente "¿Decide ContextEngine qué información realmente ve el modelo...?" →
   `validate-retrieval-set` falló limpio con `exit 1` y el mensaje exacto
   `retrievalSet.guidingQuestions[GQ-CH04-01] contiene el nombre canónico "ContextEngine", que este
   mismo capítulo introduce — las preguntas guía deben usar lenguaje de problema`. Se confirmó
   además que `./scripts/build-all` completo se detiene en la misma etapa de validación (tras haber
   pasado `validate-contracts`/`validate-components`/CH-00/CH-01/CH-02/CH-03 y `validate-chapter`
   de CH-04, fallando exactamente en `validate-retrieval-set` de CH-04), sin llegar a
   BookIR/Web/PDF. Revertido (`diff` confirmó archivo idéntico; `validate-retrieval-set` volvió a
   OK).
3. Tras revertir ambas inyecciones, `rm -rf dist && ./scripts/build-all` volvió a pasar limpio con
   los mismos conteos de nodos/aristas (37/57) y de contratos/componentes (13/4) que antes de las
   inyecciones (exit 0).

### 8.5 CH-00, CH-01, CH-02 y CH-03 no se rompieron

- `validate-chapter`/`validate-retrieval-set` de los cuatro siguen en verde (ver §7).
- Los anchors de CH-00 (`C-001`..`C-004`, `C-010`..`C-012`), CH-01 (`CMP-001`, `C-013`), CH-02
  (`CMP-002`, `C-008`, `C-009`) y CH-03 (`CMP-003`, `C-006`, `C-007`) no cambiaron de contenido.
- Solo se editó `next_chapter` en el frontmatter de CH-03 — su cuerpo, su ficha de `ModelGateway`
  y su `retrieval_set` quedaron intactos.
- `mapa.html` sigue mostrando el grafo acumulado completo con los cinco capítulos.

## 9. Definition of Done (restringido a este incremento)

- ✅ CH-04 completo: 22 secciones (0, 1-19, 20, 21), sin relleno — cada sección con contenido real.
- ✅ `registry/contracts.yaml` / `registry/components.yaml` / `registry/glossary.yaml` /
  `book/book.yaml` actualizados y validados (`validate-contracts`, `validate-components`).
- ✅ `RetrievalSet` completo con `interleavedQuestions >= 1` conectando con CH-03.
- ✅ Pipeline completo (`build-all`) verde desde `dist/` limpio.
- ✅ Evidencia concreta (no solo "pasó"): conteos de nodos/aristas del mapa mental, conteo de
  páginas de PDF (103 vs. 86 del build de 4 capítulos), texto extraído del PDF, anchors HTML, dos
  pruebas negativas con mensaje de error exacto y reversión confirmada.
- ✅ CH-00, CH-01, CH-02 y CH-03 verificados intactos tras el cambio (salvo el campo de navegación
  autorizado en CH-03).
- ✅ Frontera `ContextEngine` ↔ `PolicyEngine` (relevancia vs. autorización de visibilidad)
  documentada explícitamente en §15 del capítulo.
- ✅ Frontera `ContextEngine` ↔ `ModelGateway` (`ContextSnapshot` sin cablear hacia
  `ModelRequest.messages`) documentada explícitamente como deuda intencional hacia un capítulo
  futuro, sin modificar `C-006`.

## 10. Deuda intencional hacia el próximo capítulo (`CH-05`, fuera de este alcance)

- **El cableado formal `ContextEngine ↔ ModelGateway`**: `ContextSnapshot.blocks` no se conecta
  todavía con `ModelRequest.messages` (C-006, CH-03).
- **Autorización real de `proposedToolCall` (CH-03) y de visibilidad de `candidates` (este
  capítulo)**: ambas deudas apuntan hacia `PolicyEngine`, todavía sin introducir.
- **Ranking más rico que recencia + ajuste greedy al presupuesto**: relevancia semántica,
  retrieval, memoria de trabajo — sigue siendo trabajo de `ContextEngine`, no de un componente
  nuevo, pero no se modela en este capítulo.
- **`SessionManager`**: `candidates` llega ya dado; de dónde viene realmente ese historial
  (persistencia real) sigue sin componente propio.
- **Provider Adapters reales, streaming real, `CapabilityRegistry`**: deuda heredada de CH-02/CH-03,
  sin cambios en este capítulo.
- Persistencia real de `AgentState`/`SessionState`, human-in-the-loop implementado, reviewers
  plurales, evals y orquestación multi-agente: sin cambios respecto al alcance ya excluido por
  BH-v0.1.
