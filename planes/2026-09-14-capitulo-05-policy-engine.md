# Plan / Registro de ejecución — Capítulo 5: PolicyEngine y la Frontera de Autorización

**Fecha:** 2026-09-14
**Estado:** ✅ Completado — ejecutado en una sola sesión, sobre el estado dejado por `5afdf74` (CH-00,
CH-01, CH-02, CH-03, CH-04 como los cinco únicos capítulos reales; `PolicyEngine` todavía como
nombre de preview citado por `ToolRuntime.does_not_own` (CH-02) y `ContextEngine.does_not_own`
(CH-04)).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-13-capitulo-01-agent-loop.md`, `2026-09-13-capitulo-02-tool-runtime.md`,
  `2026-09-13-capitulo-03-model-gateway.md` y `2026-09-13-capitulo-04-context-engine.md`
  (precedentes directos: mismo formato, misma disciplina de `owns`/`does_not_own`)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Article III "PolicyEngine", Article IV Decision
  Ownership, Article I P-05/P-13, Article II INV-04/INV-06/INV-15/INV-19, Article VI pipeline de
  ejecución, Article VII Failure Constitution — `ErrorCategory.POLICY`)

---

## 1. Objetivo

Escribir el sexto capítulo real de contenido del libro ("¿Cómo construir un arnés?"), CH-05, sobre
`PolicyEngine` — el hueco de autorización que CH-02 (`ToolRuntime.does_not_own`) y CH-04
(`ContextEngine.does_not_own`, sección 15 completa) dejaron explícitamente abierto — y verificar
que atraviesa todo el pipeline (validadores + BookIR + Web + PDF + Mapa Mental) sin romper nada de
lo que CH-00..CH-04 ya tenían construido.

## 2. Alcance decidido (Paso 2 del encargo, ya cerrado antes de escribir)

Exactamente 1 componente + 1 contrato, con grounding real en la Constitution:

1. **Componente `PolicyEngine` (CMP-005)** — quinto componente de runtime del libro. `owns` cita
   literal Article III (sección "PolicyEngine": allow, deny, constraints, approval requirements,
   policy evaluation); `does_not_own` excluye explícitamente cinco decisiones vecinas: ejecutar la
   acción ya evaluada (`ToolRuntime`, ya existente — la contraparte exacta que motiva este
   capítulo), invocar al modelo (`ModelGateway`, ya existente), seleccionar contexto
   (`ContextEngine`, ya existente), decidir continuación de turno (`AgentLoop`, ya existente) y
   representar/resolver la aprobación humana (`HumanInteractionService`, preview — citando INV-15
   explícitamente) y enforcement de `ExecutionBudget` (`ExecutionController`, preview). `consumes`:
   `C-004 ExecutionContext`, `C-008 ToolCall` (ya existente, de CH-02 — evalúa la intención ya
   resuelta ANTES de que se ejecute); `produces`: `C-014 PolicyDecision` (el contrato nuevo),
   `C-010 AgentEvent`, `C-011 HarnessError`.
2. **Contrato nuevo `PolicyDecision` (C-014)** — el primer id verdaderamente nuevo del libro (no
   reservado desde CH-01 §7, a diferencia de `C-005`..`C-013`, que ya estaban todos asignados al
   cierre de CH-04). Diseñado con `callId: ToolCallId` (correlaciona con el `ToolCall` evaluado),
   `outcome: PolicyOutcome` (`ENUM` embebido de tres valores — `ALLOW`/`DENY`/`REQUIRE_APPROVAL`,
   nunca un `Boolean`), `policyRuleId: Text` (la regla que motivó la decisión — materialización
   literal de INV-19), `reason: Optional<HarnessError>` (reutiliza C-011 sin modificarlo, poblado
   únicamente cuando `outcome = DENY`) y `decidedAt: Timestamp`.
3. **Frontera con `ToolRuntime` (CMP-002, ya existente)**: NO se editó `registry/components.yaml`
   en la entrada de `CMP-002` (no existe mecanismo `modifies_components`, y el precedente ya
   establecido en CH-03/CH-04 es no tocar retroactivamente componentes previos). La integración
   real "`ToolRuntime` llama a `PolicyEngine` antes de `Execute`" queda documentada en prosa
   (secciones 9/15/18/19) como trabajo de un capítulo de integración futuro — mismo patrón de deuda
   intencional que `ContextSnapshot → ModelRequest` (CH-04) o `RawToolCallProposal → ToolCall`
   (CH-03). El pseudocódigo de este capítulo (`evaluatePolicyForToolCall`, §11) muestra a
   `PolicyEngine` evaluando un `ToolCall` de forma completamente autónoma, sin necesitar que
   `ToolRuntime` cambie una sola línea.
4. **Aprobación humana**: `PolicyOutcome.REQUIRE_APPROVAL` solo EXPRESA ese resultado — no se
   inventó ningún mecanismo de resolución; `PolicyEngine.does_not_own` excluye explícitamente
   "representar, persistir y resolver la aprobación humana", atribuido a `HumanInteractionService`
   (preview).
5. No se tocó `book/chapters/00-*`, `01-*`, `02-*` ni `03-*`; de CH-04 solo se tocó
   `next_chapter: null → CH-05` en el frontmatter.
6. `book/book.yaml` agrega CH-05 después de CH-04; CH-05 frontmatter →
   `previous_chapter: CH-04`, `next_chapter: null`.
7. `retrieval_set` de CH-05 incluye 2 `interleavedQuestions`: una conectando con CH-02
   (`ToolRuntime`/`ToolCall` — la conexión más natural y fuerte) y otra con CH-04 (`ContextEngine`,
   cerrando el hilo narrativo que CH-04 §15/§19 dejó explícitamente abierto). `guidingQuestions` en
   lenguaje de problema, sin usar "PolicyEngine"/"PolicyDecision" literal.

## 3. Decisión de diseño central: los campos de `PolicyDecision` (sin interfaz literal previa)

Como en CH-02/CH-03/CH-04, no existía una interfaz previa que copiar — el diseño se ancló
directamente en Article III (owns: allow, deny, constraints, approval requirements, policy
evaluation), Article IV ("May this action occur?") e INV-15/INV-19.

**Problema de diseño 1 — el nombre del contrato.** El encargo sugería `PolicyDecision` como nombre
posible. Se evaluó la alternativa `AuthorizationDecision` (más cercana al texto de Article IV, "May
this action occur?") pero se descartó: Article III nombra literalmente al componente
`PolicyEngine` y a su responsabilidad como "policy evaluation" — `PolicyDecision` preserva esa raíz
léxica exacta y evita introducir un segundo término ("Authorization") para el mismo concepto que
el glosario tendría que reconciliar. Se adoptó `PolicyDecision`.

**Problema de diseño 2 — `outcome` de tres estados, no un `Boolean`.** El encargo lo exigía
explícitamente (INV-15/"approval requirements" de Article III). Se definió:

```pseudocode
ENUM PolicyOutcome
    ALLOW
    DENY
    REQUIRE_APPROVAL
END
```

embebido dentro de `PolicyDecision`, sin contrato `C-XXX` propio — mismo patrón que `ContextBlock`
(CH-04) o `RawToolCallProposal` (CH-03).

**Problema de diseño 3 — trazabilidad (INV-19) sin inventar un contrato `Policy`/`Rule`.** Se
evaluó introducir un segundo contrato (`STRUCT PolicyRule`) para modelar la regla evaluada, pero se
descartó: el encargo fija el alcance en "exactamente 1 componente + 1 contrato", y modelar cómo se
almacenan/componen las policy rules reales es, honestamente, un mecanismo completo que ningún
capítulo anterior tuvo que resolver de golpe (CH-02 no modeló `Tool`/schema; CH-03 no modeló la
selección real de provider; CH-04 no modeló ranking semántico). Se adoptó en cambio
`policyRuleId: Text` como campo simple, siempre poblado (incluso con un valor centinela cuando
ninguna regla aplica — `"DEFAULT_DENY_NO_MATCHING_RULE"`), satisfaciendo INV-19 sin necesitar un
segundo contrato.

**Problema de diseño 4 — ¿reutilizar `HarnessError` (C-011) o inventar un tipo de razón nuevo?** El
encargo pedía evaluar esto explícitamente. Se decidió reutilizar `HarnessError` **únicamente**
cuando `outcome = DENY` — nunca cuando `outcome = ALLOW` o `REQUIRE_APPROVAL` — por dos razones:
(a) Article VII (`constitution/ARCHITECTURE_CONSTITUTION.md`) lista literalmente "Policy denied →
policy / non-retryable" como un `Failure Example` clasificado bajo `HarnessError`, así que
reutilizarlo para `DENY` es la lectura más fiel posible de la Constitution; (b) un
`REQUIRE_APPROVAL` no es, en ningún sentido razonable, un fallo — es una evaluación de policy
completamente exitosa que produjo un resultado distinto de permitir/denegar, y clasificarlo como
`HarnessError` habría confundido "todavía no, podría" con "no, definitivamente" (documentado en
detalle en §13 y en `EP-CH05-02` del `retrieval_set`). `reason: Optional<HarnessError>` refleja
esa asimetría directamente en el tipo (`Optional`, poblado solo en un caso de los tres).

**Alternativa descartada:** modelar `constraints` (el cuarto item literal de `owns` en Article III)
como un campo estructurado de `PolicyDecision` v1 (p. ej. `constraints: List<Text>`). Se descartó
por la misma razón que #3: habría exigido diseñar, en este mismo incremento, cómo se representa una
autorización condicional real (¿un límite de monto? ¿una redacción parcial?) sin ningún caso de uso
concreto que lo exija todavía. Se documentó explícitamente en §5 y §18 del capítulo como debate
reconocido pero fuera de alcance de v1 — la misma disciplina de "no inflar el contrato más allá de
lo que el incremento actual necesita" que CH-04 aplicó a `ContextSnapshot.estimatedTokens` (agregado
solo porque `ExecutionBudget` no alcanzaba) en vez de a un campo especulativo.

## 4. Otras decisiones de diseño tomadas durante la ejecución

### 4.1 Fail-closed (default deny) en vez de fail-open o excepción sin clasificar

Cuando `evaluatePolicyForToolCall` no encuentra ninguna policy rule aplicable a un `ToolCall`, el
resultado es `outcome = DENY` (con `HarnessError.code = "NO_APPLICABLE_POLICY_RULE"`) — nunca
`ALLOW` por omisión, nunca una excepción sin resolver (a diferencia de `CONTEXT_BUDGET_EXHAUSTED`
en CH-04, que sí usa `THROW`). Se documentó extensamente en §11 y §15 como la decisión de mayor
efecto de seguridad de este capítulo (`leverage_point` del `retrieval_set`): un sistema de
autorización que permite por defecto cuando no sabe qué hacer degrada silenciosamente hacia "todo
permitido" a medida que aparecen casos sin cubrir — exactamente lo que P-13 prohíbe.

### 4.2 Un solo valor nuevo de `AgentEventType` (`POLICY_EVALUATED`), no dos

A diferencia de CH-02/CH-03/CH-04 (que agregaron un par éxito/fallo cada uno), este capítulo agrega
solo `POLICY_EVALUATED`. Justificación explícita en §14: a diferencia de ejecutar una tool call,
invocar un modelo o ensamblar contexto — que sí pueden "no completarse" como fallo operacional
genuino — `evaluatePolicyForToolCall` **siempre** produce una `PolicyDecision` válida, incluso
cuando ninguna regla aplica (fail-closed, §4.1). No existe, en este incremento, un camino de fallo
operacional propio de la evaluación misma (distinto de un `DENY`), así que no se inventó un segundo
valor de evento solo por paralelismo con los capítulos anteriores — se documentó la asimetría en
vez de forzar el patrón.

### 4.3 Primer uso real de `ErrorCategory.POLICY`

Igual que CH-04 fue el primer uso real de `ErrorCategory.CONTEXT`, este capítulo es el primero en
ejercitar `ErrorCategory.POLICY` (declarado desde CH-00, nunca usado) — con dos códigos:
`NO_APPLICABLE_POLICY_RULE` (recoverable, no retryable) y `POLICY_DENIED` (ni recoverable ni
retryable, alineado literalmente con el `Failure Example` de Article VII).

### 4.4 `AgentRunStatus.WAITING_FOR_HUMAN` (C-013, CH-01) — primera señal real que lo justificaría

`AgentRunStatus` declara `WAITING_FOR_HUMAN` desde su primera versión (CH-01 §6), pero ningún
componente construido hasta CH-04 producía nunca una señal que justificara esa transición. Este
capítulo, con `PolicyDecision.outcome = REQUIRE_APPROVAL`, produce la primera señal real — sin
cablear la transición en sí (`AgentLoop` no se modifica; eso es deuda intencional hacia el capítulo
de `HumanInteractionService`). Se documentó explícitamente en §4/§12/§19 como un hallazgo narrativo
de esta ejecución: la Constitution había anticipado este estado desde CH-01 sin que ningún
capítulo, hasta ahora, tuviera un motivo real para producirlo.

### 4.5 `PolicyEngine.dependencies: []`

Igual que CH-01/CH-02/CH-03/CH-04: `PolicyEngine` no depende de ningún otro componente registrado.
La relación real (`ToolRuntime` invocaría a `PolicyEngine` antes de `Execute`) es la inversa de un
`dependency` en el sentido del registry, y ese cableado pertenece a un capítulo futuro —
`registry/components.yaml` de `CMP-002` no se modifica en este capítulo.

## 5. Archivos creados

- `book/chapters/05-policy-engine/chapter.md` — capítulo completo (22 secciones: 0, 1-19, 20, 21).
- `planes/2026-09-14-capitulo-05-policy-engine.md` — este registro.

## 6. Archivos modificados

- `registry/contracts.yaml` — agrega `C-014 PolicyDecision`; actualiza `used_by` de `C-004`
  (agrega `CMP-005`), `C-008` (`[CMP-002]` → `[CMP-002, CMP-005]`), `C-010`/`C-011` (agrega
  `CMP-005`); agrega comentario documentando que `C-014` es el primer id no reservado desde CH-01.
- `registry/components.yaml` — agrega `CMP-005 PolicyEngine`; actualiza el comentario de
  historial.
- `registry/glossary.yaml` — agrega `PolicyEngine` (kind: component), `Policy Decision` (kind:
  contract), `Policy Evaluation`, `Approval Requirement`, `Default Deny` (kind: concept).
- `book/book.yaml` — agrega la entrada `CH-05`.
- `book/chapters/04-context-engine/chapter.md` — únicamente `next_chapter: null` → `CH-05` en el
  frontmatter (sin tocar ninguna otra sección ni la ficha de `CMP-004`).

## 7. Resultado real del pipeline

Comando (desde la raíz del repo, `dist/` borrado antes para forzar un build limpio):

```text
$ rm -rf dist && ./scripts/build-all

=== build-all: validación determinista ===
▶ validate-contracts        → OK (14 contrato(s))
▶ validate-components        → OK (5 componente(s))
▶ validate-chapter CH-00      → OK — secciones: 22/19, pseudocode: 12, contratos: 7, componentes: 0
▶ validate-retrieval-set CH-00 → OK — guidingQuestions: 5, recallQuestions: 5, flashcards: 7
▶ validate-chapter CH-01      → OK — secciones: 22/19, pseudocode: 3, contratos: 1, componentes: 1
▶ validate-retrieval-set CH-01 → OK — guidingQuestions: 4, interleavedQuestions: 1, flashcards: 3
▶ validate-chapter CH-02      → OK — secciones: 22/19, pseudocode: 5, contratos: 2, componentes: 1
▶ validate-retrieval-set CH-02 → OK — guidingQuestions: 4, interleavedQuestions: 1, flashcards: 4
▶ validate-chapter CH-03      → OK — secciones: 22/19, pseudocode: 7, contratos: 2, componentes: 1
▶ validate-retrieval-set CH-03 → OK — guidingQuestions: 4, interleavedQuestions: 1, flashcards: 4
▶ validate-chapter CH-04      → OK — secciones: 22/19, pseudocode: 5, contratos: 1, componentes: 1
▶ validate-retrieval-set CH-04 → OK — guidingQuestions: 4, interleavedQuestions: 1, flashcards: 3
▶ validate-chapter CH-05      → OK — secciones: 22/19, pseudocode: 5, contratos: 1, componentes: 1
▶ validate-retrieval-set CH-05 → OK — guidingQuestions: 4, interleavedQuestions: 2, flashcards: 4

=== build-all: construcción ===
▶ build-book-ir  → OK → dist/book-ir.json (capítulos: 6 / contratos: 14 / componentes: 5 /
  glosario: 37 / flashcards: 25)
▶ build-mind-map
  chapter-00.diagram: 13 nodo(s), 12 arista(s)
  chapter-01.diagram: 19 nodo(s), 25 arista(s)
  chapter-02.diagram: 25 nodo(s), 35 arista(s)
  chapter-03.diagram: 31 nodo(s), 46 arista(s)
  chapter-04.diagram: 37 nodo(s), 57 arista(s)
  chapter-05.diagram: 43 nodo(s), 67 arista(s) (6 nuevo(s) en este capítulo)
  full-book.diagram: 43 nodo(s), 67 arista(s)
▶ build-web → OK → dist/web/ — index.html + 2 páginas de frontmatter + 6 capítulos + mapa.html
▶ build-pdf → OK → dist/book.pdf (668582 bytes)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
```

Exit code: `0`.

## 8. Evidencia de verificación concreta

### 8.1 Mapa mental acumulativo (CH-05 > CH-04 > CH-03 > CH-02 > CH-01 > CH-00)

`chapter-04.diagram`: 37 nodos / 57 aristas. `chapter-05.diagram`: **43 nodos / 67 aristas** (6
nodos nuevos: `CH-05`, `CMP-005`, `C-014`, y los conceptos de glosario `Policy Evaluation`/
`Approval Requirement`/`Default Deny` — los términos `PolicyEngine`/`Policy Decision` del glosario
resuelven al mismo nodo que `CMP-005`/`C-014`). Cumple el criterio del encargo (más nodos/aristas
que CH-04, que tenía 37/57). `full-book.diagram` coincide exactamente con el snapshot de CH-05 (el
último), confirmando acumulación real, no reemplazo.

### 8.2 Web

- `dist/web/chapters/CH-05.html` existe (127548 bytes), con SVG de mapa mental inline
  (`grep -c '<svg'` == 1).
- Anchors de entidad presentes: `id="CMP-005"` (1), `id="C-014"` (1).
- Navegación prev/next verificada en ambos sentidos: `CH-04.html` contiene `href="CH-05.html"` (2
  apariciones); `CH-05.html` contiene `href="CH-04.html"` (3 apariciones, incluyendo enlaces del
  mapa mental embebido hacia anchors de CH-04).
- Anchors de capítulos previos verificados intactos (1 aparición cada uno): `CH-00.html`
  (`C-001`..`C-004`, `C-010`..`C-012`); `CH-01.html` (`CMP-001`/`C-013`); `CH-02.html`
  (`CMP-002`/`C-008`/`C-009`); `CH-03.html` (`CMP-003`/`C-006`/`C-007`); `CH-04.html`
  (`CMP-004`/`C-005`) — sin cambios.
- `dist/web/index.html` lista los seis capítulos (`CH-00`..`CH-05`).

### 8.3 PDF (`pypdf`)

- Build completo (CH-00..CH-05): **123 páginas** — CH-04 documentó 103 páginas para CH-00..CH-04;
  123 > 103, confirmando el crecimiento esperado.
- Texto extraído del PDF completo, verificado con `pypdf.PdfReader(...).extract_text()`:
  `"PolicyEngine"` → `True`, `"PolicyDecision"` → `True`, `"CMP-005"` → `True`, `"C-014"` → `True`,
  `"PolicyOutcome"` → `True`, `"REQUIRE_APPROVAL"` → `True`, `"NO_APPLICABLE_POLICY_RULE"` →
  `True`, `"Default Deny"` → `True`.

### 8.4 Pruebas negativas (inyectadas y revertidas, una a la vez)

1. **`consumes` inválido en la ficha de componente**: se agregó `C-999` (inexistente) a
   `CMP-005.consumes` en `registry/components.yaml` → `validate-components` falló limpio con
   `exit 1` y el mensaje exacto `Componente CMP-005: consumes referencia contrato inexistente
   "C-999"`. Revertido (`diff` contra el backup confirmó archivo idéntico; `validate-components`
   volvió a OK).
2. **Nombre canónico en una guiding question**: se reescribió `GQ-CH05-01` para que dijera
   literalmente "¿decide PolicyEngine esa autorización...?" → `validate-retrieval-set` falló limpio
   con `exit 1` y el mensaje exacto `retrievalSet.guidingQuestions[GQ-CH05-01] contiene el nombre
   canónico "PolicyEngine", que este mismo capítulo introduce — las preguntas guía deben usar
   lenguaje de problema`. Se confirmó además que `./scripts/build-all` completo se detiene en la
   misma etapa de validación (tras haber pasado `validate-contracts`/`validate-components`/CH-00..
   CH-04 y `validate-chapter` de CH-05, fallando exactamente en `validate-retrieval-set` de CH-05),
   reportando `build-all: FALLÓ en la etapa de validación` (`policies/publishing.yaml:
   unresolved_validation_errors = deny`) sin llegar a BookIR/Web/PDF. Revertido (`diff` confirmó
   archivo idéntico; `validate-retrieval-set` volvió a OK).
3. Tras revertir ambas inyecciones, `rm -rf dist && ./scripts/build-all` volvió a pasar limpio con
   los mismos conteos de nodos/aristas (43/67) y de contratos/componentes (14/5) que antes de las
   inyecciones (exit 0), y el mismo total de páginas de PDF (123).

### 8.5 CH-00, CH-01, CH-02, CH-03 y CH-04 no se rompieron

- `validate-chapter`/`validate-retrieval-set` de los cinco siguen en verde (ver §7).
- Los anchors de CH-00 (`C-001`..`C-004`, `C-010`..`C-012`), CH-01 (`CMP-001`, `C-013`), CH-02
  (`CMP-002`, `C-008`, `C-009`), CH-03 (`CMP-003`, `C-006`, `C-007`) y CH-04 (`CMP-004`, `C-005`)
  no cambiaron de contenido.
- Solo se editó `next_chapter` en el frontmatter de CH-04 — su cuerpo, su ficha de `ContextEngine`
  y su `retrieval_set` quedaron intactos.
- `mapa.html` sigue mostrando el grafo acumulado completo con los seis capítulos.

## 9. Definition of Done (restringido a este incremento)

- ✅ CH-05 completo: 22 secciones (0, 1-19, 20, 21), sin relleno — cada sección con contenido real.
- ✅ `registry/contracts.yaml` / `registry/components.yaml` / `registry/glossary.yaml` /
  `book/book.yaml` actualizados y validados (`validate-contracts`, `validate-components`).
- ✅ `RetrievalSet` completo con `interleavedQuestions = 2` conectando con CH-02 y CH-04.
- ✅ Pipeline completo (`build-all`) verde desde `dist/` limpio, para los 6 capítulos.
- ✅ Evidencia concreta (no solo "pasó"): conteos de nodos/aristas del mapa mental, conteo de
  páginas de PDF (123 vs. 103 del build de 5 capítulos), texto extraído del PDF, anchors HTML, dos
  pruebas negativas con mensaje de error exacto y reversión confirmada con conteos idénticos.
- ✅ CH-00, CH-01, CH-02, CH-03 y CH-04 verificados intactos tras el cambio (salvo el campo de
  navegación autorizado en CH-04).
- ✅ Frontera `PolicyEngine` ↔ `ToolRuntime` (autonomía de evaluación vs. ejecución) documentada
  explícitamente en §9/§15 del capítulo, sin modificar `CMP-002`.
- ✅ Frontera `PolicyEngine` ↔ `HumanInteractionService` (expresar `REQUIRE_APPROVAL` vs.
  resolverlo) documentada explícitamente, citando INV-15, sin inventar mecanismo de resolución.

## 10. Deuda intencional hacia el próximo capítulo (`CH-06`, fuera de este alcance)

- **El cableado formal `ToolRuntime ↔ PolicyEngine`**: `ToolRuntime.executeToolCall` (CH-02) no
  invoca `evaluatePolicyForToolCall` todavía.
- **`HumanInteractionService` y la resolución real de `REQUIRE_APPROVAL`**: incluyendo, por fin,
  una transición real hacia `AgentRunStatus.WAITING_FOR_HUMAN` (declarado desde CH-01, nunca
  alcanzado).
- **`ExecutionController` y enforcement real de `ExecutionBudget`**: sin cambios.
- **`constraints` como campo estructurado de `PolicyDecision`**: reconocido en owns, no modelado en
  v1.
- **Almacenamiento/composición real de policy rules, `CapabilityRegistry`, Provider Adapters
  reales, streaming real**: deuda heredada, sin cambios en este capítulo.
- **La visibilidad de `candidates` en `ContextEngine` (CH-04 §15)**: `PolicyEngine` queda capaz de
  evaluar cualquier `ToolCall`, pero no se cablea ningún mecanismo para que `ContextEngine` lo
  consulte antes de incluir un candidato.
- Persistencia real de `AgentState`/`SessionState`, reviewers plurales, evals y orquestación
  multi-agente: sin cambios respecto al alcance ya excluido por BH-v0.1.
