# Plan / Registro de ejecución — Capítulo 14: AdmissionController y la Admisión de una Activación Cruda

**Fecha:** 2026-09-14
**Estado:** ✅ Completado, sobre el estado dejado por `13da4a2` (CH-00..CH-13 como los catorce
únicos capítulos reales; BH-v0.1 completo — once componentes de Article III + dos capítulos de
integración).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-14-capitulo-11-agent-core.md` (origen de `AgentActivationRequest`/`AgentCore`, y del
  término de glosario "Ingress Activation" que este capítulo formaliza)
- `2026-09-14-capitulo-05-policy-engine.md` (precedente de `Default Deny` / outcome de varios
  valores nunca un Boolean, y de la frontera "Decision Ownership" entre dos componentes que
  producen un resultado con forma parecida)
- `2026-09-14-capitulo-13-integracion-caminos-de-gobierno.md` (capítulo más reciente antes de
  este, formato/estilo de referencia; método para cerrar deuda intencional sin reabrir código ya
  publicado)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Amendment v1.1 completo — `P-16`..`P-30`,
  `INV-E01`..`INV-E14`, "Canonical Enterprise Planes")

---

## 1. Objetivo

Escribir el decimoquinto capítulo real de contenido del libro ("¿Cómo construir un arnés?"),
CH-14, sobre `AdmissionController` — el primer componente del Amendment v1.1 ("Enterprise
Activation, Interoperability and Operations") que este libro materializa con código real, abriendo
una parte nueva del libro (el territorio Enterprise, más allá de los once componentes originales de
Article III). Verificar que el capítulo atraviesa todo el pipeline (validadores + BookIR + Web +
PDF + Mapa Mental) sin romper nada de lo que CH-00..CH-13 ya tenían construido.

## 2. Alcance decidido (Paso 2 del encargo, ya cerrado antes de escribir)

Exactamente 1 componente + 2 contratos:

1. **Componente `AdmissionController` (CMP-012)** — primer componente de este registry que NO
   corresponde a ninguno de los once nombres del árbol de Article III ("Agent Runtime"); pertenece
   al "Ingress & Activation Plane" de Amendment v1.1. `owns` (cita literal de `P-17`): "apply
   identity, authorization, tenant, capacity, rate, budget, deduplication and policy decisions
   before routing"; decidir con un outcome de dos valores (`ADMIT`/`REJECT`) si un
   `ActivationRequest` puede proceder; rechazar por defecto (fail-closed, `Default Reject`);
   correlacionar la decisión de vuelta con el `ActivationRequest` por `requestId`. `does_not_own`:
   normalizar el estímulo crudo (Ingress Adapter, `P-16`, infraestructura de borde), resolver o
   rutear hacia un `AgentId`/`AgentConfig` concreto (Routing, `P-17` "before routing", sin
   componente propio todavía), construir el `AgentState`/`AgentActivationRequest` real de un agente
   (`AgentCore`, CMP-011, CH-11), evaluar policy sobre una `ToolCall` ya en curso (`PolicyEngine`,
   CMP-005, CH-05). `consumes`: `C-022 ActivationRequest`; `produces`: `C-011 HarnessError`,
   `C-023 AdmissionDecision`.
2. **Contrato nuevo `ActivationRequest` (C-022)** — el estímulo externo ya normalizado por un
   ingress adapter: `id` (`ActivationRequestId`), `sourceRef` (`Text`, referencia opaca al
   canal/ingress mechanism), `externalIdentityRef` (`Text`, identidad/tenant externo todavía sin
   autorizar), `payload` (`Value`) y `receivedAt` (`Timestamp`). Deliberadamente sin `agentId`.
3. **Contrato nuevo `AdmissionDecision` (C-023)** — el resultado de evaluar un `ActivationRequest`:
   `requestId` (`ActivationRequestId`), `outcome` (`AdmissionOutcome`: `ADMIT`/`REJECT`, nunca un
   Boolean), `reason` (`Optional<HarnessError>`, poblado solo cuando `REJECT`, reutilizando
   `HarnessError` C-011) y `decidedAt` (`Timestamp`). Deliberadamente sin ningún `agentId` — "lo que
   permite continuar" cuando `ADMIT` es, únicamente, el `requestId`.
4. **Pseudocódigo del capítulo**: `evaluateAdmissionForActivationRequest(request: ActivationRequest)
   -> AdmissionDecision` — fail-closed (`Default Reject`) salvo que la primitiva asumida
   `admissionRulesGrantAccess(request)` conceda acceso. Sin `THROW`: el `REJECT` es un resultado
   válido, nunca una excepción (mismo patrón que `PolicyEngine`, CH-05).
5. No se tocó `book/chapters/00-*` a `12-*`; de CH-13 solo se tocó `next_chapter: null → CH-14` en
   el frontmatter.
6. `book/book.yaml` agrega CH-14 después de CH-13; CH-14 frontmatter → `previous_chapter: CH-13`,
   `next_chapter: null`. Prosa de apertura del capítulo marca explícitamente que empieza una parte
   nueva del libro (territorio Amendment v1.1 / Enterprise) — sin mecanismo nuevo en `book.yaml`.
7. `retrieval_set` de CH-14 incluye 2 `interleavedQuestions`: una conectando con CH-11
   (`AgentCore`/`AgentActivationRequest`, la frontera más importante de este capítulo) y otra con
   CH-05 (`PolicyEngine`, contrastando "admisión" vs. "autorización de una acción").
   `guidingQuestions` en lenguaje de problema, sin usar "AdmissionController"/"ActivationRequest"/
   "AdmissionDecision" literal (verificado con la prueba negativa de §8.4).

## 3. Decisiones de diseño centrales

### 3.1 Confirmación de los próximos ids libres (verificados, no asumidos)

Se leyó `registry/contracts.yaml` y `registry/components.yaml` completos antes de escribir. El
último contrato registrado era `C-021` (`AgentActivationRequest`, CH-11) — los próximos ids libres
son `C-022` y `C-023`, no `C-022` a secas ni ningún otro número asumido de antemano. El último
componente registrado era `CMP-011` (`AgentCore`, CH-11) — el próximo id libre es `CMP-012`.
Verificado también que ningún id de ese rango aparecía ya reservado en comentarios de capítulos
anteriores (a diferencia de `C-005..C-013`, que sí estaban reservados desde CH-01 §7).

### 3.2 El nombre del contrato: `ActivationRequest` (sin prefijo), a diferencia de CH-11

CH-11 acuñó deliberadamente `AgentActivationRequest` para NO colisionar con el término
`ActivationRequest` que Amendment v1.1 ya cita literalmente (`P-16`). Este capítulo es,
precisamente, el que formaliza ese término reservado — así que adopta el nombre corto y literal
que la Constitution ya usa, en vez de inventar un prefijo nuevo. Se verificó con grep que
`ActivationRequest` no colisiona con ningún nombre ya registrado en `registry/contracts.yaml`.

### 3.3 `AdmissionDecision` nunca resuelve un `AgentId` — la decisión de diseño con mayor efecto

Se evaluó explícitamente agregar un campo `admittedAgentId: Optional<AgentId>` a
`AdmissionDecision`, poblado cuando `outcome = ADMIT`, para que "lo que permite continuar" fuera
más concreto. Se descartó: `P-17` coloca la resolución hacia un agente concreto explícitamente
**después** de la admisión ("...decisions **before routing**") — resolver ese `AgentId` dentro de
`AdmissionController` habría absorbido silenciosamente una decisión de Routing (todavía sin dueño
en este registry) dentro de un componente cuya única pregunta es "¿puede esta activación
proceder?". `AdmissionDecision.requestId` es, en cambio, la única referencia que el contrato
necesita: suficiente para que una integración futura combine `(ActivationRequest, AdmissionDecision)`
con un mecanismo de Routing todavía por construir.

### 3.4 Por qué `AdmissionController` nunca construye un `AgentEvent` — hallazgo real, no una omisión

Se verificó, releyendo `STRUCT AgentEvent` (C-010, CH-00), que sus cuatro campos de correlación
(`runId`, `sessionId`, `agentId`, `traceId`) son todos obligatorios, nunca `Optional`. En el
instante en que se evalúa una admisión, ninguno de los cuatro existe todavía — ni siquiera
`agentId`, porque `AdmissionDecision` deliberadamente no lo resuelve (§3.3). Se descartó inventar
valores centinela para esos campos (mismo principio que motivó, en CH-13 §14, documentar
honestamente el reuso de `RUN_FAILED` en vez de forzar una solución artificial). Se decidió, en
cambio, documentar esto como el hallazgo real de este capítulo: `AdmissionController` es el primer
componente cuya función principal nunca emite ningún evento, por una razón distinta de `EventBus`
(CH-09, que tampoco emite, pero porque no decide nada) — y se conectó explícitamente con `P-25`
("Audit evidence is distinct from operational telemetry"): una auditoría real de decisiones de
admisión necesitaría un mecanismo distinto de `EventBus`/`AgentEvent`, que este capítulo no
construye (seccion 18 del capítulo).

### 3.5 Una nueva categoría de `ErrorCategory`: `ADMISSION`

Se evaluó reutilizar `POLICY` (ya que `P-17` menciona "policy decisions" como una de las ocho
dimensiones de admisión) o `VALIDATION`. Se descartó: `POLICY` pertenece, en exclusiva, a la
pregunta de `PolicyEngine` sobre una acción ya resuelta (CH-05) — reutilizarla aquí habría
conflacionado dos decisiones de Decision Ownership distintas, exactamente el error que Article IV
prohíbe. Se agregó `ADMISSION` como duodécimo valor de `ErrorCategory` — el tercer capítulo en
extender ese `ENUM` desde CH-00 (después de `HUMAN_INTERACTION`, CH-06) — con el mismo argumento
que CH-06 ya usó para su propia categoría nueva.

### 3.6 Una sola función, sin `THROW` — mismo patrón que `PolicyEngine` (CH-05), no que `AgentCore` (CH-11)

Se evaluó modelar `evaluateAdmissionForActivationRequest` con precondiciones que lanzaran
`HarnessError` (como `activateAgent`/`beginAgentInitialization`, CH-11). Se descartó: el rechazo de
una activación (`REJECT`) es, exactamente como `DENY` en `PolicyEngine` (CH-05), un resultado válido
del dominio — nunca una violación de precondición del llamador. Se siguió, en cambio, el patrón de
`evaluatePolicyForToolCall` (CH-05): una única función, sin `THROW`, con `Default Reject` como su
fail-closed.

### 3.7 `AdmissionController` sin ficha propia en Article III — grounding en Amendment v1.1, no en Article III

A diferencia de CMP-001..CMP-011 (cada uno con una sección propia en Article III, "Component
Sovereignty"), se verificó con grep completo sobre `constitution/ARCHITECTURE_CONSTITUTION.md` que
Article III no tiene ninguna sección para `AdmissionController` — Amendment v1.1 extiende la
Constitution sin reescribir Article III. Se decidió anclar el `owns`/ficha arquitectónica en la
cita literal de `P-17` en vez de en una sección de Article III que no existe, documentando esta
diferencia explícitamente en la seccion 3/8 del capítulo.

### 3.8 Tercera ausencia de fila en Article IV, por una tercera razón distinta

Se verificó (mismo grep que CH-09/CH-11 ya hicieron) que Article IV no tiene fila para
`AdmissionController` — ni podría, porque el archivo fuente de la Constitution no fue editado.
Se documentó explícitamente que esta es la tercera vez que un componente del libro carece de fila
propia, cada vez por una razón distinta: `EventBus` (CH-09) porque no decide nada; `AgentCore`
(CH-11) porque su decisión ocurre antes de que exista un `AgentRun`; `AdmissionController` (este
capítulo) porque su decisión ocurre un paso **antes todavía** — ni siquiera existe un `agentId`
resuelto sobre el cual la pregunta de `AgentCore` podría aplicarse.

## 4. Archivos creados

- `book/chapters/14-admission-controller/chapter.md` — capítulo completo (22 secciones: 0, 1-19,
  20, 21).
- `planes/2026-09-14-capitulo-14-admission-controller.md` — este registro.

## 5. Archivos modificados

- `registry/contracts.yaml` — agrega `C-022 ActivationRequest` y `C-023 AdmissionDecision`;
  actualiza `used_by` de `C-011` (agrega `CMP-012`); agrega comentario documentando la decisión de
  diseño (incluida la distinción explícita con `AgentActivationRequest`, CH-11).
- `registry/components.yaml` — agrega `CMP-012 AdmissionController`; actualiza el comentario de
  historial.
- `registry/glossary.yaml` — agrega `AdmissionController` (kind: component), `ActivationRequest`
  (kind: contract), `AdmissionDecision` (kind: contract), `Admission`, `Ingress Adapter`, `Routing
  (Amendment v1.1)` (kind: concept). No se editó la entrada previa "Ingress Activation" (CH-11):
  se preserva tal como CH-11 la escribió, como registro histórico de la deuda que este capítulo
  cierra.
- `book/book.yaml` — agrega la entrada `CH-14`.
- `book/chapters/13-integracion-caminos-de-gobierno/chapter.md` — únicamente
  `next_chapter: null` → `CH-14` en el frontmatter (sin tocar ninguna otra sección).

## 6. Resultado real del pipeline

Comando (desde la raíz del repo, `dist/` borrado antes para forzar un build limpio):

```text
$ rm -rf dist && ./scripts/build-all
...
▶ validate-chapter book/chapters/14-admission-controller/chapter.md
validate-chapter: OK — secciones: 22/19, bloques pseudocode: 6, contratos introducidos: 2,
  componentes introducidos: 1
▶ validate-retrieval-set book/chapters/14-admission-controller/chapter.md
validate-retrieval-set: OK — guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2,
  interleavedQuestions: 2, flashcards: 5, calibrationPairs: 4
...
▶ build-book-ir → OK → dist/book-ir.json (capítulos: 15 / contratos: 23 / componentes: 12 /
  glosario: 74 / flashcards: 70)
▶ build-mind-map
  chapter-13.diagram: 82 nodo(s), 131 arista(s)
  chapter-14.diagram: 89 nodo(s), 140 arista(s) (7 nuevo(s) en este capítulo)
  full-book.diagram: 89 nodo(s), 140 arista(s)
▶ build-web → OK → dist/web/ — index.html + 2 páginas de frontmatter + 15 capítulos + mapa.html
▶ build-pdf → OK → dist/book.pdf (1832376 bytes)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
```

Exit code: `0` (verificado explícitamente tras `rm -rf dist && ./scripts/build-all`, y de nuevo
tras revertir las dos pruebas negativas de §8, con conteos idénticos: 89 nodos/140 aristas, 23
contratos, 12 componentes, 15 capítulos, 351 páginas de PDF, 1832376 bytes de PDF byte a byte).

## 7. Evidencia de verificación concreta

### 7.1 Mapa mental acumulativo (CH-14 > CH-13 > ... > CH-00)

`chapter-13.diagram`: 82 nodos / 131 aristas. `chapter-14.diagram`: **89 nodos / 140 aristas** (7
nuevos: el nodo `CHAPTER` de `CH-14`, `CMP-012`, `C-022`, `C-023`, y los tres conceptos de glosario
nuevos con nodo propio — `Admission`, `Ingress Adapter`, `Routing (Amendment v1.1)`). Cumple el
criterio del encargo (más nodos/aristas que CH-13: 89 > 82, 140 > 131 — a diferencia de CH-12/CH-13,
que no introdujeron entidades nuevas al registry). `full-book.diagram` coincide exactamente con el
snapshot de CH-14 (el último), confirmando acumulación real.

### 7.2 Web

- `dist/web/chapters/CH-14.html` existe, con SVG de mapa mental inline (`grep -c '<svg'` == 1).
- Anchors de entidad presentes: `id="CMP-012"` (1), `id="C-022"` (1), `id="C-023"` (1).
- Navegación prev/next verificada en ambos sentidos: `CH-13.html` contiene `href="CH-14.html"`;
  `CH-14.html` contiene `href="CH-13.html"`.
- Anchors de capítulos previos verificados intactos (1 aparición cada uno): CH-00 (`C-001`), CH-01
  (`CMP-001`, `C-013`), CH-11 (`CMP-011`, `C-021`) — sin cambios.
- `<svg` aparece exactamente 1 vez en cada una de las 15 páginas de capítulo (CH-00..CH-14).
- `dist/web/index.html` lista los quince capítulos (`CH-00`..`CH-14`).

### 7.3 PDF (`pypdf`)

- Build completo (CH-00..CH-14): **351 páginas** — más que las 329 páginas del build de 14
  capítulos citadas en el encargo.
- Texto extraído del PDF, verificado con `pypdf.PdfReader(...).extract_text()`:
  `"AdmissionController"` → `True`, `"ActivationRequest"` → `True`, `"AdmissionDecision"` → `True`,
  `"CMP-012"` → `True`, `"C-022"` → `True`, `"C-023"` → `True`.

### 7.4 Pruebas negativas (inyectadas y revertidas, una a la vez)

1. **`produces` inválido en la ficha de componente**: se agregó `C-999` (inexistente) a
   `CMP-012.produces` en `registry/components.yaml` → `validate-components` falló limpio con
   `exit 1` y el mensaje exacto `Componente CMP-012: produces referencia contrato inexistente
   "C-999"`. Revertido (`diff` contra el backup en `/tmp/components.yaml.bak` confirmó archivo
   idéntico; `validate-components` volvió a `OK (12 componente(s))`, `exit 0`).
2. **Nombre canónico en una guiding question**: se reescribió `GQ-CH14-01` para que dijera
   literalmente "¿Decide AdmissionController...?" → `validate-retrieval-set` falló limpio con
   `exit 1` y el mensaje exacto `retrievalSet.guidingQuestions[GQ-CH14-01] contiene el nombre
   canónico "AdmissionController", que este mismo capítulo introduce — las preguntas guía deben
   usar lenguaje de problema`. Revertido (`diff` contra el backup en `/tmp/ch14.md.bak` confirmó
   archivo idéntico; `validate-retrieval-set` volvió a `OK`, `exit 0`).
3. Tras revertir ambas inyecciones (`diff` confirmó archivos idénticos byte a byte), `rm -rf dist &&
   ./scripts/build-all` volvió a pasar limpio con los mismos conteos de nodos/aristas (89/140), de
   contratos/componentes (23/12), de capítulos (15) y de páginas/bytes de PDF (351 páginas,
   1832376 bytes, verificado de nuevo con `pypdf`) que antes de las inyecciones (exit 0).

### 7.5 CH-00..CH-13 no se rompieron

- `validate-chapter`/`validate-retrieval-set` de los catorce siguen en verde (ver §6, corrida
  completa de `build-all`).
- Los anchors de CH-00..CH-13 no cambiaron de contenido (ver §7.2).
- Solo se editó `next_chapter` en el frontmatter de CH-13 — su cuerpo y su `retrieval_set`
  quedaron intactos.
- `mapa.html` sigue mostrando el grafo acumulado completo con los quince capítulos.

### 7.6 Confirmación textual: `AdmissionController` sin ficha en Article III ni fila en Article IV

Verificado con `grep` de texto completo sobre `constitution/ARCHITECTURE_CONSTITUTION.md`: Article
III (líneas 233-354) no tiene ninguna sección `## AdmissionController`; Article IV (líneas 356-393)
no tiene ninguna fila para `AdmissionController`. Confirmado: es el tercer componente real del
libro sin fila en esa tabla (después de `EventBus`, CH-09, y `AgentCore`, CH-11), por una tercera
razón distinta, documentada en seccion 4/5/20 del capítulo (ver §3.8 de este plan).

## 8. Definition of Done (restringido a este incremento)

- ✅ CH-14 completo: 22 secciones (0, 1-19, 20, 21), sin relleno — cada sección con contenido real.
- ✅ `registry/contracts.yaml` / `registry/components.yaml` / `registry/glossary.yaml` /
  `book/book.yaml` actualizados y validados (`validate-contracts`, `validate-components`).
- ✅ `RetrievalSet` completo con `interleavedQuestions = 2` conectando con CH-11 y CH-05.
- ✅ Pipeline completo (`build-all`) verde desde `dist/` limpio, para los 15 capítulos.
- ✅ Evidencia concreta: conteos de nodos/aristas del mapa mental (89/140 > 82/131), conteo de
  páginas de PDF (351 vs. 329 citadas en el encargo), texto extraído del PDF, anchors HTML, dos
  pruebas negativas con mensaje de error exacto y reversión confirmada con conteos idénticos.
- ✅ CH-00..CH-13 verificados intactos tras el cambio (salvo el campo de navegación autorizado en
  CH-13).
- ✅ Confirmado con grep: `AdmissionController` no tiene ficha en Article III ni fila en Article IV
  — documentado como el tercer componente del libro sin fila (después de `EventBus` y `AgentCore`),
  por una tercera razón distinta.
- ✅ Distinción explícita y documentada entre `ActivationRequest` (este capítulo) y
  `AgentActivationRequest` (C-021, CH-11) — resolviendo, con código real, la deuda que CH-11 ya
  había señalado y diferido explícitamente bajo el término de glosario "Ingress Activation".
- ✅ Primera cita literal con código real de `P-16`/`P-17`/`INV-E01`/`INV-E02` (Amendment v1.1).
- ✅ Hallazgo real documentado (no anticipado en el encargo original, encontrado durante el diseño):
  `AdmissionController` es el primer componente del libro cuya función principal nunca construye un
  `AgentEvent` — los cuatro campos obligatorios de ese `STRUCT` (`runId`/`sessionId`/`agentId`/
  `traceId`) describen un `AgentRun` que, en el instante de una admisión, todavía no existe —
  conectado explícitamente con `P-25` (audit evidence distinct from operational telemetry).
- ✅ `AdmissionDecision` nunca resuelve ni construye un `AgentId` — la frontera de Routing (`P-17`,
  "before routing") se mantiene explícitamente sin dueño, documentada como trabajo futuro.

## 9. Deuda intencional hacia el próximo capítulo (fuera de este alcance)

- **El cableado real `AdmissionController → Routing → AgentCore`**: nadie invoca
  `evaluateAdmissionForActivationRequest` seguido de una resolución real de `AgentId` y de
  `AgentCore.activateAgent` (CH-11) como un único flujo.
- **El "Ingress Adapter" real** (webhook/cola/cron/API concretos): infraestructura de borde, no
  modelada.
- **El mecanismo real detrás de `admissionRulesGrantAccess`**: primitiva asumida; ninguna de las
  ocho dimensiones de `P-17` (identity/authorization/tenant/capacity/rate/budget/deduplication/
  policy) se modela en detalle.
- **Ausencia de evidencia de auditoría real** (`P-25`) para una `AdmissionDecision`: señalado
  explícitamente como límite real, no silenciado.
- **Los ocho planes restantes de Amendment v1.1** (Execution, Agent Interoperability, Capability &
  Integration, Data & Context, Control, Reliability, Observability & Governance, Execution Fabric)
  y sus componentes (`AgentCommunicationGateway`, `CredentialBroker`, ...): fuera de alcance.
- **Deduplicación real de `ActivationRequest`**, **admisión condicional o diferida** (tercer valor
  de `AdmissionOutcome`): no modelado.
- Reviewers plurales, evals y orquestación multi-agente: explícitamente fuera de alcance de
  BH-v0.1.
- **El capítulo que profundice el "Ingress & Activation Plane"** (Routing como componente propio,
  un Ingress Adapter concreto) o que avance hacia el segundo de los nueve planes canónicos
  (Execution Plane): candidato natural para el próximo incremento (CH-14 §19).
