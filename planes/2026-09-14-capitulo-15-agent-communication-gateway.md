# Plan / Registro de ejecución — Capítulo 15: AgentCommunicationGateway y la Frontera Explícita entre Agentes

**Fecha:** 2026-09-14
**Estado:** ✅ Completado, sobre el estado dejado por `3fda3d5` (CH-00..CH-14 como los quince
únicos capítulos reales; Ingress & Activation Plane, primer plano de Amendment v1.1, con su primer
componente, `AdmissionController`, CMP-012).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-14-capitulo-14-admission-controller.md` (precedente inmediato: primer componente de
  Amendment v1.1, patrón de ficha sin sección propia de Article III, patrón de `THROW` vs.
  `Decision`-struct discutido explícitamente en su seccion 3.6)
- `2026-09-14-capitulo-11-agent-core.md` (precedente del patrón `THROW HarnessError` sobre
  precondiciones de un artefacto ya existente — `activateAgent`/`beginAgentInitialization`)
- `2026-09-14-capitulo-07-execution-controller.md` (origen del cumplimiento real de
  `ExecutionBudget`, C-012, reutilizado sin modificar por `DelegationGrant`)
- `2026-09-14-capitulo-05-policy-engine.md` (precedente de `Default Deny` / resultado de varios
  valores nunca un Boolean, contrastado explícitamente con la elección de este capítulo)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Amendment v1.1 completo — `P-16`..`P-30`,
  `INV-E01`..`INV-E14`, "Canonical Enterprise Planes")
- `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §31 ("Amendment v0.5 — Reglas para arquitectura
  empresarial y comunicación", en particular "Regla de comunicación entre agentes" y "Regla A2A")

---

## 1. Objetivo

Escribir el decimosexto capítulo real de contenido del libro ("¿Cómo construir un arnés?"), CH-15,
sobre `AgentCommunicationGateway` — el componente del "Agent Interoperability Plane" de Amendment
v1.1, el segundo de los nueve planos canónicos que este libro cubre (el primero fue Ingress &
Activation, CH-14; este capítulo salta deliberadamente el segundo plano canónico, Execution Plane,
para cubrir el tercero). Verificar que el capítulo atraviesa todo el pipeline (validadores + BookIR
+ Web + PDF + Mapa Mental) sin romper nada de lo que CH-00..CH-14 ya tenían construido.

## 2. Alcance decidido (Paso 2 del encargo, ya cerrado antes de escribir)

Exactamente 1 componente + 2 contratos:

1. **Componente `AgentCommunicationGateway` (CMP-013)** — segundo componente de este registry que
   NO corresponde a ninguno de los once nombres del árbol de Article III; pertenece al "Agent
   Interoperability Plane" de Amendment v1.1. `owns` (cita literal de `P-18`/`P-19`, más lectura de
   `P-20`/`INV-E06`): adaptar mensajes semánticos hacia/desde protocolos externos exclusivamente vía
   adapters; desacoplar el core de cualquier SDK/protocolo/transporte concreto; distinguir siempre
   delegación interna de federación externa; verificar — nunca redefinir — que un `DelegationGrant`
   que respalda un mensaje siga vigente, cubra el mensaje y respete su `ExecutionBudget` acotado;
   rechazar por defecto cuando el grant declarado no se encuentra, no corresponde, expiró o no
   cubre el mensaje. `does_not_own`: decidir si un estímulo externo crudo tiene derecho a arrancar
   un run (`AdmissionController`, CMP-012, CH-14), autorizar una acción/tool call ya resuelta
   (`PolicyEngine`, CMP-005, CH-05), decidir continuación de turno (`AgentLoop`, CMP-001, CH-01), el
   protocolo/transporte concreto en sí (Protocol Adapter/Transport Adapter, `INV-E04`, fuera de este
   registry), revalidar la coherencia interna de un `ExecutionBudget` ya construido (`AgentCore`,
   CMP-011, CH-11). `consumes`: `C-024 AgentCommunicationMessage`, `C-025 DelegationGrant`;
   `produces`: `C-011 HarnessError`, `C-024 AgentCommunicationMessage` (el mismo mensaje, ya
   autorizado).
2. **Contrato nuevo `AgentCommunicationMessage` (C-024)** — el contrato semántico explícito que
   exige `P-18`: `id`, `boundary` (`AgentCommunicationBoundary`: `INTERNAL`/`EXTERNAL`, cita literal
   de `INV-E03`), `sourceAgentRef`/`targetAgentRef` (`Text`, opacos — nunca `AgentId`),
   `content` (`Value`), `delegationGrantId` (`Optional<DelegationGrantId>`), `traceId` (`TraceId`,
   reutilizado) y `sentAt` (`Timestamp`). Deliberadamente sin ningún campo de protocolo/transporte
   (`INV-E04`) y sin `sessionId` (ver hallazgo real, §3.4 de este plan).
3. **Contrato nuevo `DelegationGrant` (C-025)** — el token de delegación explícito que exige `P-21`:
   `id`, `delegatingRunId` (`Optional<RunId>`), `delegatorRef`/`grantedAt` (auditable),
   `delegateRef` (a quién), `delegatedScope` (`List<Text>`, nunca un `Boolean` de "todo"),
   `budget` (`ExecutionBudget`, C-012 reutilizado sin modificar, `INV-E06`) y `expiresAt`
   (time-bounded).
4. **Pseudocódigo del capítulo**: `authorizeAgentCommunicationMessage(message:
   AgentCommunicationMessage, grant: Optional<DelegationGrant>) -> AgentCommunicationMessage` — deja
   pasar sin fricción cualquier mensaje sin `delegationGrantId`; `THROW HarnessError` (categoría
   `DELEGATION`, nueva) cuando el grant declarado no se encuentra, no corresponde, expiró o no cubre
   el mensaje (`delegationScopeCoversMessage`, primitiva asumida).
5. No se tocó `book/chapters/00-*` a `13-*`; de CH-14 solo se tocó `next_chapter: null → CH-15` en
   el frontmatter.
6. `book/book.yaml` agrega CH-15 después de CH-14; CH-15 frontmatter → `previous_chapter: CH-14`,
   `next_chapter: null`.
7. `retrieval_set` de CH-15 incluye 2 `interleavedQuestions`: una conectando con CH-14
   (`AdmissionController`/`AdmissionDecision`, distinguiendo admisión de un estímulo crudo frente a
   comunicación entre runs ya admitidos) y otra con CH-07 (`ExecutionController`/`ExecutionBudget`,
   distinguiendo el presupuesto operacional de UN run frente al límite de una relación de
   delegación entre dos runs, `INV-E06`). `guidingQuestions` en lenguaje de problema, sin usar
   "AgentCommunicationGateway"/"AgentCommunicationMessage"/"DelegationGrant" literal (verificado con
   la prueba negativa de §8.2).

## 3. Decisiones de diseño centrales

### 3.1 Confirmación de los próximos ids libres (verificados, no asumidos)

Se leyó `registry/contracts.yaml` y `registry/components.yaml` completos antes de escribir. El
último contrato registrado era `C-023` (`AdmissionDecision`, CH-14) — los próximos ids libres son
`C-024` y `C-025`. El último componente registrado era `CMP-012` (`AdmissionController`, CH-14) — el
próximo id libre es `CMP-013`. Verificado con grep que ningún nombre candidato
(`AgentCommunicationGateway`, `AgentCommunicationMessage`, `DelegationGrant`,
`AgentCommunicationBoundary`) colisionaba ya con algo registrado.

### 3.2 Por qué se salta el Execution Plane (segundo plano canónico) para cubrir Agent
Interoperability Plane (tercero)

El encargo pidió explícitamente el "Agent Interoperability Plane" como "segundo plano que se cubre
en el libro" (no el segundo del orden canónico de Amendment v1.1). Se documentó esta decisión de
forma explícita en la apertura del capítulo y en seccion 1/19 — el Execution Plane completo queda,
deliberadamente, como candidato igualmente válido para un incremento futuro (seccion 18).

### 3.3 `sourceAgentRef`/`targetAgentRef` como `Text`, nunca `AgentId`

Se evaluó tipar ambos campos como `AgentId` (C-002, CH-00), el identificador fuertemente tipado ya
existente. Se descartó: cuando `boundary = EXTERNAL`, el agente objetivo puede ser un agente operado
por un tercero completamente independiente, sin ningún `AgentId` registrado en este sistema — el
mismo argumento que motivó, en CH-14 §6, que `ActivationRequest.externalIdentityRef` fuera `Text` en
vez de `AgentId`. `Text` mantiene un único `STRUCT` válido para ambos lados de la frontera.

### 3.4 `AgentCommunicationMessage` sin `sessionId` — el hallazgo real de este capítulo

Se evaluó explícitamente agregar `sessionId: Optional<SessionId>` a `AgentCommunicationMessage`,
para poder construir un `AgentEvent` (C-010) real cuando el run de origen ya existe. Se descartó:
para `boundary = EXTERNAL`, el agente destino puede no compartir en absoluto el concepto de
`Session` (`SessionManager`, CH-10) de este runtime — poblar `sessionId` solo con el del run de
origen, o dejarlo `NULL`, habría fabricado o silenciado un dato de forma inconsistente entre los dos
casos de `boundary`. Se decidió, en cambio, que `AgentCommunicationMessage` no tenga `sessionId` en
absoluto, documentando esto como el hallazgo real de este capítulo: el tercer componente del libro
(después de `EventBus`, CH-09, y `AdmissionController`, CH-14) cuya función principal nunca
construye un `AgentEvent`, por una tercera razón distinta de las dos anteriores — el run casi
siempre YA existe aquí, a diferencia de `AdmissionController`, pero el contrato deliberadamente no
tiene el campo que `AgentEvent` exige como obligatorio.

### 3.5 `DELEGATION` como nueva categoría de `ErrorCategory`, no `BUDGET`

Se evaluó reutilizar `BUDGET` (CH-07) para `DELEGATION_SCOPE_EXCEEDED`, dado el parecido superficial
con "exceder un límite". Se descartó: `BUDGET` pertenece, en exclusiva, a la pregunta de
`ExecutionController` sobre si UN `AgentRun` puede continuar contra SU PROPIO `ExecutionBudget` — una
pregunta operacional turno a turno sobre una ejecución que ya existe, evaluada por un componente
distinto. `DELEGATION_SCOPE_EXCEEDED` es sobre si un token — no una ejecución — cubre lo que un
mensaje concreto pide. Se agregó `DELEGATION` como decimotercer valor de `ErrorCategory` — el cuarto
capítulo en extender ese `ENUM` desde CH-00 (después de `HUMAN_INTERACTION`, CH-06, y `ADMISSION`,
CH-14) — con el mismo argumento de Decision Ownership que motivó ambas extensiones anteriores.

### 3.6 `THROW HarnessError`, no un tercer contrato de `Decision` — la decisión de diseño con mayor
efecto sobre el alcance

Se evaluó explícitamente introducir un tercer contrato (`AgentCommunicationDecision`, con un
`outcome` de dos valores), siguiendo el molde de `PolicyDecision` (CH-05) o `AdmissionDecision`
(CH-14) — ambos ya usados en el libro para decisiones de outcome binario/ternario con más de un
componente vecino reaccionando de forma distinta a cada resultado. Se descartó, deliberadamente,
para mantener el alcance del capítulo en exactamente dos contratos (Paso 2 del encargo): a
diferencia de `PolicyEngine`/`AdmissionController` — que evalúan una acción o activación **todavía
sin resolver** contra un espacio de reglas de negocio con resultados igualmente válidos —, este
capítulo verifica la integridad de un `DelegationGrant` **ya emitido**, exactamente la misma
naturaleza de precondición que `AgentCore.activateAgent`/`beginAgentInitialization` (CH-11) ya
verifican con `THROW` sobre un `AgentConfig`/`AgentState` ya existentes. No existe, en este
capítulo, ningún componente vecino que reaccione de forma distinta a cada uno de los cuatro modos de
rechazo — todos significan, para `AgentCommunicationGateway`, exactamente lo mismo: el mensaje no
cruza la frontera. Esta distinción (y su contraste explícito con CH-05/CH-14) se documenta en la
seccion 11 del capítulo, no solo en este plan.

### 3.7 `delegatedScope: List<Text>`, nunca un `Boolean` de "todo permitido"

Se evaluó explícitamente un campo `allowAll: Boolean` para simplificar `DelegationGrant`. Se
descartó de inmediato: `P-21` prohíbe, literalmente, que un agente hijo o remoto herede
automáticamente toda la autoridad de quien delega — un `Boolean` que pudiera valer `TRUE` haría
posible, por diseño del propio contrato, la violación exacta que ese principio prohíbe. `List<Text>`
hace estructuralmente imposible que un `DelegationGrant` represente "todo".

### 3.8 `DelegationGrant.budget` reutiliza `ExecutionBudget` (C-012) como valor, sin modificar el
contrato

Se evaluó introducir un `STRUCT` de presupuesto nuevo, específico de la relación de delegación. Se
descartó: `INV-E06` exige, literalmente, que la delegación esté acotada por `ExecutionBudget` — el
mismo `STRUCT` que ya tiene cumplimiento real desde CH-07. `DelegationGrant.budget` es una
**instancia** de `ExecutionBudget`, tan acotada como haga falta, nunca una modificación al contrato
mismo (`modifies_contracts: []` en el frontmatter, verificado).

### 3.9 `AgentCommunicationMessage.delegationGrantId` como `Optional`, no obligatorio

Se evaluó exigir siempre un `DelegationGrant`, dado que este capítulo introduce el concepto. Se
descartó: `P-20` distingue delegación interna de federación externa, pero ninguna de las dos implica,
por sí sola, que exista una transferencia de autoridad — dos agentes pueden federarse sin que
ninguno delegue nada. Exigir el campo siempre habría inventado una relación de delegación que
`P-20`/`P-21` nunca dijeron que existiera en todo mensaje.

## 4. Archivos creados

- `book/chapters/15-agent-communication-gateway/chapter.md` — capítulo completo (22 secciones: 0,
  1-19, 20, 21).
- `planes/2026-09-14-capitulo-15-agent-communication-gateway.md` — este registro.

## 5. Archivos modificados

- `registry/contracts.yaml` — agrega `C-024 AgentCommunicationMessage` y `C-025 DelegationGrant`,
  con comentario documentando la decisión de diseño.
- `registry/components.yaml` — agrega `CMP-013 AgentCommunicationGateway`; actualiza el comentario
  de historial.
- `registry/glossary.yaml` — agrega `AgentCommunicationGateway` (component), `AgentCommunicationMessage`
  (contract), `DelegationGrant` (contract), `AgentCommunication Boundary`, `Internal Delegation`,
  `External Federation`, `A2A (Agent-to-Agent)`, `Federation Boundary`, `Delegated Authority`,
  `Protocol Adapter`, `Transport Adapter` (kind: concept).
- `book/book.yaml` — agrega la entrada `CH-15`.
- `book/chapters/14-admission-controller/chapter.md` — únicamente `next_chapter: null` → `CH-15` en
  el frontmatter (sin tocar ninguna otra sección).

## 6. Resultado real del pipeline

Comando (desde la raíz del repo, `dist/` borrado antes para forzar un build limpio):

```text
$ rm -rf dist && ./scripts/build-all
...
▶ validate-chapter book/chapters/15-agent-communication-gateway/chapter.md
validate-chapter: OK — secciones: 22/19, bloques pseudocode: 6, contratos introducidos: 2,
  componentes introducidos: 1
▶ validate-retrieval-set book/chapters/15-agent-communication-gateway/chapter.md
validate-retrieval-set: OK — guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2,
  interleavedQuestions: 2, flashcards: 5, calibrationPairs: 4
...
▶ build-book-ir → OK → dist/book-ir.json (capítulos: 16 / contratos: 25 / componentes: 13 /
  glosario: 85 / flashcards: 75)
▶ build-mind-map
  chapter-14.diagram: 89 nodo(s), 140 arista(s)
  chapter-15.diagram: 101 nodo(s), 155 arista(s) (12 nuevo(s) en este capítulo)
  full-book.diagram: 101 nodo(s), 155 arista(s)
▶ build-web → OK → dist/web/ — index.html + 2 páginas de frontmatter + 16 capítulos + mapa.html
▶ build-pdf → OK → dist/book.pdf (1990704 bytes)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
```

Exit code: `0` (verificado explícitamente tras `rm -rf dist && ./scripts/build-all`, y de nuevo tras
revertir las dos pruebas negativas de §8, con conteos idénticos: 101 nodos/155 aristas, 25
contratos, 13 componentes, 16 capítulos, 379 páginas de PDF).

## 7. Evidencia de verificación concreta

### 7.1 Mapa mental acumulativo (CH-15 > CH-14 > ... > CH-00)

`chapter-14.diagram`: 89 nodos / 140 aristas. `chapter-15.diagram`: **101 nodos / 155 aristas** (12
nuevos: el nodo `CHAPTER` de `CH-15`, `CMP-013`, `C-024`, `C-025`, y los ocho conceptos de glosario
nuevos con nodo propio). Cumple el criterio del encargo (más nodos/aristas que CH-14: 101 > 89,
155 > 140). `full-book.diagram` coincide exactamente con el snapshot de CH-15 (el último),
confirmando acumulación real.

### 7.2 Web

- `dist/web/chapters/CH-15.html` existe, con SVG de mapa mental inline (`grep -c '<svg'` == 1).
- Anchors de entidad presentes: `id="CMP-013"` (1), `id="C-024"` (1), `id="C-025"` (1).
- Navegación prev/next verificada en ambos sentidos: `CH-14.html` contiene `href="CH-15.html"`;
  `CH-15.html` contiene `href="CH-14.html"`.
- Anchors de capítulos previos verificados intactos (1 aparición cada uno): CH-00 (`C-001`), CH-01
  (`CMP-001`, `C-013`), CH-11 (`CMP-011`, `C-021`), CH-14 (`CMP-012`) — sin cambios.
- `<svg` aparece exactamente 1 vez en cada una de las 16 páginas de capítulo (CH-00..CH-15).
- `dist/web/index.html` lista los dieciséis capítulos.

### 7.3 PDF (`pypdf`)

- Build completo (CH-00..CH-15): **379 páginas** — más que las 351 páginas del build de 15
  capítulos citadas en el encargo.
- Texto extraído del PDF, verificado con `pypdf.PdfReader(...).extract_text()`:
  `"AgentCommunicationGateway"` → `True`, `"AgentCommunicationMessage"` → `True`,
  `"DelegationGrant"` → `True`, `"CMP-013"` → `True`, `"C-024"` → `True`, `"C-025"` → `True`.

### 7.4 Pruebas negativas (inyectadas y revertidas, una a la vez)

1. **`produces` inválido en la ficha de componente**: se agregó `C-999` (inexistente) a
   `CMP-013.produces` en `registry/components.yaml` → `validate-components` falló limpio con
   `exit 1` y el mensaje exacto `Componente CMP-013: produces referencia contrato inexistente
   "C-999"`. Revertido (`diff` contra el backup en `/tmp/components.yaml.ch15.bak` confirmó archivo
   idéntico; `validate-components` volvió a `OK (13 componente(s))`, `exit 0`).
2. **Nombre canónico en una guiding question**: se reescribió `GQ-CH15-01` para que dijera
   literalmente "¿Decide AgentCommunicationGateway...?" → `validate-retrieval-set` falló limpio con
   `exit 1` y el mensaje exacto `retrievalSet.guidingQuestions[GQ-CH15-01] contiene el nombre
   canónico "AgentCommunicationGateway", que este mismo capítulo introduce — las preguntas guía
   deben usar lenguaje de problema`. Revertido (`diff` contra el backup en `/tmp/ch15.md.ch15.bak`
   confirmó archivo idéntico; `validate-retrieval-set` volvió a `OK`, `exit 0`).
3. Tras revertir ambas inyecciones (`diff` confirmó archivos idénticos byte a byte), `rm -rf dist &&
   ./scripts/build-all` volvió a pasar limpio con los mismos conteos de nodos/aristas (101/155), de
   contratos/componentes (25/13), de capítulos (16) y de páginas de PDF (379) que antes de las
   inyecciones (exit 0).

### 7.5 CH-00..CH-14 no se rompieron

- `validate-chapter`/`validate-retrieval-set` de los quince siguen en verde (ver §6, corrida
  completa de `build-all`).
- Los anchors de CH-00..CH-14 no cambiaron de contenido (ver §7.2).
- Solo se editó `next_chapter` en el frontmatter de CH-14 — su cuerpo y su `retrieval_set` quedaron
  intactos.
- `mapa.html` sigue mostrando el grafo acumulado completo con los dieciséis capítulos.

## 8. Definition of Done (restringido a este incremento)

- ✅ CH-15 completo: 22 secciones (0, 1-19, 20, 21), sin relleno — cada sección con contenido real.
- ✅ `registry/contracts.yaml` / `registry/components.yaml` / `registry/glossary.yaml` /
  `book/book.yaml` actualizados y validados (`validate-contracts`, `validate-components`).
- ✅ `RetrievalSet` completo con `interleavedQuestions = 2` conectando con CH-14 y CH-07.
- ✅ Pipeline completo (`build-all`) verde desde `dist/` limpio, para los 16 capítulos.
- ✅ Evidencia concreta: conteos de nodos/aristas del mapa mental (101/155 > 89/140), conteo de
  páginas de PDF (379 vs. 351 citadas en el encargo), texto extraído del PDF, anchors HTML, dos
  pruebas negativas con mensaje de error exacto y reversión confirmada con conteos idénticos.
- ✅ CH-00..CH-14 verificados intactos tras el cambio (salvo el campo de navegación autorizado en
  CH-14).
- ✅ Distinción explícita y documentada entre `AgentCommunicationGateway`/`AgentCommunicationMessage`
  y `AdmissionController`/`ActivationRequest` (CH-14) — admisión de un estímulo crudo frente a
  comunicación entre runs ya admitidos.
- ✅ Primera cita literal con código real de `P-18`/`P-19`/`P-20`/`P-21`/`INV-E03`..`INV-E06`
  (Amendment v1.1).
- ✅ Hallazgo real documentado (encontrado durante el diseño, no anticipado literalmente en el
  encargo): `AgentCommunicationGateway` es el tercer componente del libro cuya función principal
  nunca construye un `AgentEvent`, por una tercera razón distinta de `EventBus` (CH-09) y
  `AdmissionController` (CH-14) — el run casi siempre ya existe, pero `AgentCommunicationMessage`
  deliberadamente no tiene `sessionId`.
- ✅ Decisión de diseño explícita y documentada de usar `THROW HarnessError` (precedente CH-11) en
  vez de un tercer contrato de `Decision` (precedente CH-05/CH-14), manteniendo el alcance en
  exactamente 2 contratos.
- ✅ `DelegationGrant` nunca representa autoridad sin acotar: `delegatedScope: List<Text>`, nunca un
  `Boolean` de "todo permitido" — documentado como la decisión de mayor efecto del capítulo.

## 9. Deuda intencional hacia el próximo capítulo (fuera de este alcance)

- **El cableado real `AgentCommunicationGateway → Protocol Adapter → Transport Adapter → destino`**:
  ningún componente invoca todavía `authorizeAgentCommunicationMessage` seguido de una entrega real.
- **El Protocol Adapter/Transport Adapter real** (A2A concreto, HTTP/gRPC): infraestructura de
  borde, no modelada.
- **El mecanismo real detrás de `delegationScopeCoversMessage`**: primitiva asumida.
- **Profundidad de delegación encadenada** (`INV-E06`, "delegation depth") y **consumo acumulado de
  `DelegationGrant.budget`** a través de múltiples mensajes: no modelado.
- **La emisión real de un `DelegationGrant`**: quién lo construye y con qué autoridad para delegar
  en primer lugar — asumido, no modelado.
- **Ausencia de evidencia de auditoría real** (`P-25`) para un `AgentCommunicationMessage`/
  `DelegationGrant`: señalado explícitamente, no silenciado.
- **El Execution Plane completo** (segundo plano canónico, deliberadamente saltado) y **los seis
  planos restantes** de Amendment v1.1 (Capability & Integration, Data & Context, Control,
  Reliability, Observability & Governance, Execution Fabric) y sus componentes
  (`CredentialBroker`, y el resto): fuera de alcance.
- Reviewers plurales, evals y orquestación multi-agente propiamente dicha: explícitamente fuera de
  alcance de BH-v0.1.
- **El capítulo que profundice el Agent Interoperability Plane** (Protocol Adapter/Transport Adapter
  concretos), o que cubra el Execution Plane, o que avance hacia cualquiera de los seis planos
  restantes: candidato natural para el próximo incremento (CH-15 §19).
