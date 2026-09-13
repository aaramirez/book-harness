# Plan / Registro de ejecución — Capítulo 1: El Agent Loop y el Ciclo de Ejecución Cognitiva

**Fecha:** 2026-09-13
**Estado:** ✅ Completado — ejecutado y documentado en una sola pasada (no hubo un plan previo
separado: se pidió directamente en la conversación, sobre el estado dejado por
`1fb1c5a` — BH-v0.1 + Ciclo de Dominio Activo + Mapa Mental Progresivo, con CH-00 como único
capítulo real).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Article III "AgentLoop", Article IV Decision
  Ownership, Article V Lifecycle, Article VI Execution Constitution)

---

## 1. Objetivo

Escribir el segundo capítulo real de contenido del libro ("¿Cómo construir un arnés?"), CH-01, con
grounding literal en la Constitution, y verificar que atraviesa todo el pipeline (validadores +
BookIR + Web + PDF + Mapa Mental) sin romper nada de lo que CH-00 ya tenía construido.

## 2. Alcance decidido (Paso 2 del encargo, ya cerrado antes de escribir)

Exactamente 2 entidades nuevas, ambas citando literal la Constitution:

1. **Contrato `AgentRunStatus`** — formaliza lo que CH-00 ya usaba por nombre
   (`AgentState.status: AgentRunStatus`, C-003) sin haberlo registrado como contrato propio.
2. **Componente `AgentLoop` (CMP-001)** — primer componente de runtime del libro. `owns`/
   `does_not_own` citados literal de Article III (sección "AgentLoop"). `consumes`/`produces`
   solo contratos ya existentes (los 7 de CH-00 + `AgentRunStatus`); `dependencies: []` (ningún
   otro componente existe todavía). `ModelGateway`/`ToolRuntime`/`PolicyEngine`/
   `ExecutionController` se mencionan solo en prosa como "Preview — no introducido en este
   capítulo", nunca dentro de un bloque ```pseudocode```.

## 3. Decisiones de diseño tomadas durante la ejecución (no cubiertas explícitamente por el encargo)

### 3.1 Numeración del nuevo contrato: `C-013`, no `C-005`

`reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §10 muestra, como ejemplo de numeración de un
Contract Registry, `C-005 ContextSnapshot`, `C-006 ModelRequest`, `C-007 ModelResponse`,
`C-008 ToolCall`, `C-009 ToolResult` — exactamente los cinco contratos que CH-00 §6 ya anunciaba
como "Unchanged / Not yet introduced" junto a `ModelGateway`/`ContextEngine`/`ToolRuntime`. Aunque
`registry/contracts.yaml` de este repo no tiene placeholders reales para esos cinco ids (están
simplemente ausentes, no reservados por un validador), asignarle `C-005` a `AgentRunStatus` habría
colisionado con esa convención editorial en el momento en que un capítulo futuro (`CH-02`,
`ToolRuntime`) necesite `ContextSnapshot`. Se optó por `C-013` (el mismo id que ese documento de
reglas usa como ejemplo para un sexto contrato, `ToolDefinition`, en un contexto distinto — sin
relación semántica con nuestro `AgentRunStatus`, solo una coincidencia de numeración conveniente) y
se documentó la reserva de `C-005`..`C-009` explícitamente en `registry/contracts.yaml` y en
CH-01 §7, para que el próximo capítulo no tenga que redescubrir esta convención.

### 3.2 `governTurnContinuation` (CH-00) NO se reutiliza por nombre en el pseudocódigo de CH-01

Se evaluó llamar directamente a `governTurnContinuation` (la función de CH-00 que verifica
`budget.maxTurns`) desde el `runTurn` de `AgentLoop`, ya que `scripts/lib/chapter-parser.js` no
prohíbe referenciar funciones en `lowerCamelCase` de otro capítulo (el escáner "no magic entities"
de `validate-chapter` solo vigila identificadores que empiezan con mayúscula — `STRUCT`/`ENUM`/
`INTERFACE`/`COMPONENT`; una llamada a una función `lowerCamelCase` como `newEventId()`/`now()` ya
pasaba libre en CH-00). Se decidió **no** hacerlo: Article IV (Decision Ownership) separa
"¿debe ocurrir otro turno de razonamiento?" (`AgentLoop`) de "¿puede el run continuar
operacionalmente?" (`ExecutionController`, todavía sin introducir). Si `runTurn` invocara
`governTurnContinuation` (una verificación de presupuesto), `AgentLoop` estaría absorbiendo en la
práctica una decisión que su propia ficha declara en `does_not_own`. En su lugar, `runTurn` no
verifica presupuesto en absoluto — deja esa verificación fuera de su alcance, deliberadamente, y
lo documenta como deuda intencional (§18 del capítulo, y §7 de este registro).

### 3.3 Corrección de `AgentRunStatus`: se agrega `EXPIRED`, ausente en la versión de trabajo de CH-00

`constitution/ARCHITECTURE_CONSTITUTION.md` Article V define `AgentRunStatus` con 11 valores
(incluyendo `expired`). CH-00 §6 ya mostraba un `ENUM AgentRunStatus` de trabajo con solo 10
valores (sin `EXPIRED`), y su tabla de transiciones (§12) enrutaba `WAITING_FOR_HUMAN --expired-->`
hacia `FAILED` en consecuencia. Al formalizar `AgentRunStatus` como contrato completo (C-013, fiel
a la Constitution), CH-01 agrega `EXPIRED` y corrige explícitamente esa transición
(`expired → EXPIRED`, no `FAILED`) — documentado en CH-01 §12 como una corrección explícita, no
silenciosa, sobre la versión preliminar de CH-00. **No se editó el pseudocódigo de CH-00** (fuera
de alcance, "no reabrir" el Paso 2): CH-00 sigue mostrando su propia versión de trabajo de 10
estados como lo que siempre fue — una demostración conceptual anterior a que existiera ningún
componente, ahora explícitamente superada por CH-01.

### 3.4 `AgentEventType` / `ErrorCategory`: reutilizados por tipo, sin nuevo contrato ni valores nuevos

Ninguno de los dos tiene `C-XXX` propio (viven embebidos en `AgentEvent`/`HarnessError` desde
CH-00). Para poder anotar variables locales con esos tipos en el pseudocódigo de CH-01
(`resolvedEventType: AgentEventType = TURN_CONTINUED`) sin violar "no magic entities", se agregó
una tabla `| \`AgentEventType\` | ... |` / `| \`ErrorCategory\` | ... |` en CH-01 §6 (mismo
mecanismo que CH-00 ya usaba para sus identificadores fundamentales) — sin agregar ningún valor
nuevo a ninguno de los dos enums, solo referenciándolos por tipo.

### 3.5 `governTurnContinuation` sigue sin dueño — deuda intencional explícita, no un `ExecutionController` de utilería

Se consideró introducir un `ExecutionController` mínimo solo para poder asignarle la verificación
de presupuesto y "cerrar" la ficha de `AgentLoop` sin cabos sueltos. Se descartó: el encargo
(Paso 2) limita este capítulo a exactamente 2 entidades nuevas, y crear un componente placeholder
solo para tener a quién asignarle una responsabilidad sería precisamente el antipatrón que Article
IV prohíbe ("crear estructura para que el código compile", no para que la arquitectura sea
correcta). La verificación de presupuesto permanece código sin dueño formal, documentada como tal.

## 4. Archivos creados

- `book/chapters/01-agent-loop/chapter.md` — capítulo completo (22 secciones: 0, 1-19, 20, 21).
- `planes/2026-09-13-capitulo-01-agent-loop.md` — este registro.

## 5. Archivos modificados

- `registry/contracts.yaml` — agrega `C-013 AgentRunStatus`; actualiza `used_by` de
  `C-002/C-003/C-004/C-010/C-011` a `[CMP-001]` (bookkeeping descriptivo, no un cambio de
  definición — no requiere `modifies_contracts`).
- `registry/components.yaml` — agrega `CMP-001 AgentLoop` (primer componente del registry, que
  hasta este capítulo estaba vacío).
- `registry/glossary.yaml` — agrega `AgentRunStatus` (kind: contract), `AgentLoop` (kind:
  component), `Turn`, `Agent Run`, `Decision Ownership` (kind: concept).
- `book/book.yaml` — agrega la entrada `CH-01`.
- `book/chapters/00-arquitectura-constitucion/chapter.md` — `next_chapter: null` → `CH-01`;
  actualiza la prosa de §19 (Next Increment), que decía explícitamente "CH-01 todavía no existe
  como archivo", para reflejar que ahora sí existe (sin tocar ninguna otra sección de CH-00).

## 6. Resultado real del pipeline

Comando (desde la raíz del repo, `dist/` borrado antes para forzar un build limpio):

```text
$ rm -rf dist && ./scripts/build-all

=== build-all: validación determinista ===
▶ validate-contracts
validate-contracts: OK (8 contrato(s))
▶ validate-components
validate-components: OK (1 componente(s))
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

=== build-all: construcción ===
▶ build-book-ir
build-book-ir: OK → dist/book-ir.json
  frontmatter: 2 página(s) / capítulos: 2 / contratos: 8 / componentes: 1 / glosario: 17 /
  flashcards: 10
▶ build-mind-map
  chapter-00.diagram: 13 nodo(s), 12 arista(s) (13 nuevo(s) en este capítulo)
  chapter-01.diagram: 19 nodo(s), 25 arista(s) (6 nuevo(s) en este capítulo)
  full-book.diagram: 19 nodo(s), 25 arista(s)
▶ build-web
build-web: OK → dist/web/ — index.html + 2 páginas de frontmatter + 2 capítulos + mapa.html
▶ build-pdf
build-pdf: OK → dist/book.pdf (245892 bytes)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
```

Exit code: `0`.

## 7. Evidencia de verificación concreta

### 7.1 Mapa mental acumulativo (CH-01 > CH-00, y ambos coexisten en `mapa.html`)

`chapter-00.diagram`: 13 nodos / 12 aristas. `chapter-01.diagram`: 19 nodos / 25 aristas (6 nodos
nuevos: `CMP-001`, `C-013`, y los 3 conceptos de glosario `Turn`/`Agent Run`/`Decision Ownership`
introducidos en CH-01, más el nodo `CHAPTER` de CH-01 mismo). `full-book.diagram` coincide con el
snapshot de CH-01 (el último), confirmando acumulación real, no reemplazo.

`dist/web/mapa.html` contiene 19 nodos SVG (`grep -c 'class="node"'`) y enlaces tanto a
`CH-00.html#...` como a `CH-01.html#...` — el grafo acumulado completo, no solo el último capítulo.

### 7.2 Web

- `dist/web/chapters/CH-01.html` existe, con SVG de mapa mental inline (`grep -c '<svg' == 1`).
- Anchors de entidad presentes: `id="C-013"`, `id="CMP-001"` (y `id="CONCEPT-turn"`,
  `id="CONCEPT-agent-run"`, `id="CONCEPT-decision-ownership"`).
- Navegación prev/next verificada en ambos sentidos: `CH-00.html` contiene `href="CH-01.html"`
  (dos apariciones, nav superior e inferior); `CH-01.html` contiene `href="CH-00.html"` (incluidos
  los links del mapa mental incrustado hacia anchors de CH-00: `CH-00.html#C-001` .. `#C-012` y
  sus conceptos).
- `dist/web/chapters/CH-00.html` conserva sus 7 anchors originales (`C-001`..`C-012`) sin cambios.
- `dist/web/index.html` lista ambos capítulos.

### 7.3 PDF (`pypdf`)

- Build completo (CH-00 + CH-01): **43 páginas**, 245892 bytes.
- Build de control con `book/book.yaml` temporalmente reducido a solo CH-00 (mismo `registry/`,
  restaurado inmediatamente después de medir): **28 páginas**, 158081 bytes. Confirma que el
  crecimiento de páginas es atribuible a CH-01, no a un artefacto del build.
- Texto extraído del PDF completo contiene, verificado con `pypdf.PdfReader(...).extract_text()`:
  `"AgentLoop"` → `True`, `"AgentRunStatus"` → `True`, `"EXPIRED"` → `True`, `"CMP-001"` → `True`.

### 7.4 Pruebas negativas (inyectadas y revertidas, una a la vez)

1. **Guiding question con nombre canónico**: se inyectó `"¿decide AgentLoop que el ciclo..."` en
   `GQ-CH01-01` (que este mismo capítulo introduce) → `validate-retrieval-set` falló limpio con
   `exit 1` y el mensaje exacto `contiene el nombre canónico "AgentLoop"...`. Revertido; se
   confirmó `validate-retrieval-set` OK de nuevo.
2. **`consumes` inválido en la ficha de componente**: se agregó `C-999` (inexistente) a
   `components.consumes` de `CMP-001` en `registry/components.yaml` → `validate-components` falló
   limpio con `exit 1` (`consumes referencia contrato inexistente "C-999"`), y
   `rm -rf dist && ./scripts/build-all` se detuvo en la etapa de validación con `exit 1`
   **sin** construir BookIR/Web/PDF (`policies/publishing.yaml: unresolved_validation_errors =
   deny`), dejando `dist/book-state.json` con `"buildStatus": "failed_validation"`. Revertido
   (`diff` contra el backup confirmó archivo idéntico); `build-all` volvió a pasar limpio con los
   mismos conteos de nodos/aristas/páginas que antes de la inyección.

### 7.5 CH-00 no se rompió

- `validate-chapter`/`validate-retrieval-set` de CH-00 siguen en verde (ver §6).
- Sus 7 anchors de entidad y su contenido no cambiaron (solo se editó `next_chapter` en el
  frontmatter y la prosa de §19 — ver §5).
- `mapa.html` sigue mostrando el grafo acumulado completo con ambos capítulos (§7.1).

## 8. Definition of Done (restringido a este incremento)

- ✅ CH-01 completo: 22 secciones (0, 1-19, 20, 21), sin relleno — cada sección con contenido real.
- ✅ `registry/contracts.yaml` / `registry/components.yaml` / `registry/glossary.yaml` /
  `book/book.yaml` actualizados y validados (`validate-contracts`, `validate-components`).
- ✅ `RetrievalSet` completo con `interleavedQuestions >= 1` (primer capítulo del libro donde esta
  regla aplica de verdad, ya que CH-00 estaba exento).
- ✅ Pipeline completo (`build-all`) verde desde `dist/` limpio.
- ✅ Evidencia concreta (no solo "pasó"): conteos de nodos/aristas del mapa mental, conteo de
  páginas de PDF con y sin CH-01, texto extraído del PDF, anchors HTML, pruebas negativas con
  mensaje de error exacto y reversión confirmada.
- ✅ CH-00 verificado intacto tras el cambio.

## 9. Deuda intencional hacia el próximo capítulo (`CH-02`, fuera de este alcance)

- **`WAITING_FOR_TOOL` sin resolver**: `AgentLoop.runTurn` transiciona a este estado y se detiene
  ahí a propósito (Article VI, Execution Rules 1-2: `AgentLoop` no ejecuta side effects; las tools
  se ejecutan exclusivamente mediante `ToolRuntime`). Resolverlo requiere `ToolCall`/`ToolResult`/
  `ToolRuntime` — y, para que `ToolRuntime` tenga a quién pedirle autorización, probablemente
  `PolicyEngine` — ninguno de los dos introducido todavía.
  `ContextSnapshot`/`ModelRequest`/`ModelResponse` quedan reservados como `C-005`..`C-009` para
  cuando ese capítulo (o el que introduzca `ModelGateway`/`ContextEngine`) los necesite.
- **Operational continuation (budget/cancelación) sigue sin componente propio**:
  `governTurnContinuation` (CH-00) sigue siendo código sin dueño formal. `AgentLoop` no la absorbió
  a propósito (§3.2/§3.5 de este registro) — la decisión de a qué componente asignarla
  (`ExecutionController`, Article III) queda explícitamente para cuando ese componente se
  introduzca.
- **Autorización real / invocación real del modelo**: `PolicyEngine`/`ModelGateway` siguen sin
  existir; `modelFinished`/`modelProposesToolCall` son señales de entrada asumidas en el
  pseudocódigo de CH-01, no producidas todavía por ningún componente.
- Persistencia (`SessionManager`), Human-in-the-loop implementado, reviewers plurales, evals y
  orquestación multi-agente: sin cambios respecto al alcance ya excluido por BH-v0.1 (ver
  `planes/2026-08-23-book-harness-como-construir-un-arnes.md` §7).
