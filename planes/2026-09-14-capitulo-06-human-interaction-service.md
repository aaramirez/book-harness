# Plan / Registro de ejecución — Capítulo 6: HumanInteractionService y la Reanudación de una Ejecución Pausada

**Fecha:** 2026-09-14
**Estado:** ✅ Completado — ejecutado en una sola sesión, sobre el estado dejado por `1a8e5c7` (CH-00,
CH-01, CH-02, CH-03, CH-04, CH-05 como los seis únicos capítulos reales; `HumanInteractionService`
todavía como nombre de preview citado por `PolicyEngine.does_not_own` (CH-05) y por
`ToolRuntime.does_not_own` (CH-02); `AgentRunStatus.WAITING_FOR_HUMAN` declarado desde CH-01 sin
ninguna transición real).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-13-capitulo-01-agent-loop.md` .. `2026-09-14-capitulo-05-policy-engine.md` (precedentes
  directos: mismo formato, misma disciplina de `owns`/`does_not_own`)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Article III "HumanInteractionService", Article IV
  Decision Ownership, Article VIII completo — Human Interaction Constitution —, Article II
  INV-14/INV-15/INV-18/INV-19/INV-20, Article I P-11, Article VII Failure Constitution —
  `ErrorCategory.HUMAN_INTERACTION`)

---

## 1. Objetivo

Escribir el séptimo capítulo real de contenido del libro ("¿Cómo construir un arnés?"), CH-06,
sobre `HumanInteractionService` — la pieza que por fin le da un significado real a
`AgentRunStatus.WAITING_FOR_HUMAN` (declarado desde CH-01, sin uso real hasta ahora) y a
`PolicyDecision.outcome = REQUIRE_APPROVAL` (CH-05) — y verificar que atraviesa todo el pipeline
(validadores + BookIR + Web + PDF + Mapa Mental) sin romper nada de lo que CH-00..CH-05 ya tenían
construido.

## 2. Alcance decidido (Paso 2 del encargo, ya cerrado antes de escribir)

Exactamente 1 componente + 2 contratos (mismo patrón request/resolution ya usado en CH-02
`ToolCall`/`ToolResult` y CH-03 `ModelRequest`/`ModelResponse`):

1. **Componente `HumanInteractionService` (CMP-006)** — sexto componente de runtime del libro.
   `owns` cita literal Article III (sección "HumanInteractionService": representar solicitudes
   humanas, persistir interacciones pendientes, recibir resoluciones, permitir reanudación);
   `does_not_own` excluye explícitamente cuatro decisiones vecinas: decidir SI se requiere
   aprobación (`PolicyEngine`, ya existente — la entrada real de este capítulo), transportar la
   interacción por un canal concreto (Channel Adapter — concepto de infraestructura de borde,
   mencionado en prosa, nunca introducido como componente propio del registry), ejecutar la acción
   ya resuelta (`ToolRuntime`, ya existente) y decidir continuación del turno (`AgentLoop`, ya
   existente). `consumes`: `C-004 ExecutionContext`, `C-014 PolicyDecision` (ya existente, de
   CH-05); `produces`: `C-015 HumanInteractionRequest`, `C-016 HumanInteractionResolution` (los dos
   contratos nuevos), `C-010 AgentEvent`, `C-011 HarnessError`.
2. **Contrato nuevo `HumanInteractionRequest` (C-015)** — la solicitud persistida: `id`
   (`HumanInteractionRequestId`, identificador opaco nuevo), `type` (`HumanInteractionType` — ENUM
   `APPROVAL`/`INPUT`/`REVIEW`/`DECISION`, cita literal de Article VIII "Tipos mínimos"), `callId`
   (`ToolCallId`, reutiliza la correlación que `PolicyDecision.callId` ya estableció en CH-05 en
   vez de inventar una relación nueva hacia `PolicyDecision`), `status`
   (`HumanInteractionStatus` — ENUM `PENDING`/`RESOLVED`) y `requestedAt` (`Timestamp`).
   Deliberadamente **sin ningún campo de canal**.
3. **Contrato nuevo `HumanInteractionResolution` (C-016)** — la resolución que un humano produjo:
   `requestId` (`HumanInteractionRequestId`, correlaciona con la solicitud resuelta), `outcome`
   (`HumanInteractionOutcome` — ENUM `APPROVED`/`REJECTED`/`PROVIDED`, tres valores, no un
   `Boolean`, mismo argumento que `PolicyOutcome` en CH-05), `value` (`Optional<Value>`, poblado
   únicamente cuando `outcome = PROVIDED` — misma asimetría de diseño que `PolicyDecision.reason`),
   `resolvedBy` (`ActorId`, identificador opaco nuevo, trazabilidad INV-19) y `resolvedAt`
   (`Timestamp`).
4. **Frontera con `PolicyEngine` (CMP-005) y `AgentLoop`/`AgentRunStatus` (CMP-001/CH-01)**: NO se
   editó `registry/components.yaml` en las entradas de `CMP-001`/`CMP-005` (no existe mecanismo
   `modifies_components`, mismo precedente ya establecido en CH-03/04/05). El pseudocódigo de este
   capítulo (`createHumanInteractionRequest`/`resolveHumanInteractionRequest`, §11) muestra a
   `HumanInteractionService` creando una `HumanInteractionRequest` a partir de una `PolicyDecision`
   y, más tarde, recibiendo una `HumanInteractionResolution`, de forma completamente autónoma, sin
   que `AgentLoop`/`PolicyEngine` cambien una sola línea. La integración real (`AgentLoop`
   transiciona a `WAITING_FOR_HUMAN` y espera la resolución antes de reanudar el turno;
   `ToolRuntime` espera la resolución antes de `Execute`) queda documentada en prosa (secciones
   9/15/18/19) como trabajo de un capítulo de integración futuro.
5. No se tocó `book/chapters/00-*` a `04-*`; de CH-05 solo se tocó `next_chapter: null → CH-06` en
   el frontmatter.
6. `book/book.yaml` agrega CH-06 después de CH-05; CH-06 frontmatter →
   `previous_chapter: CH-05`, `next_chapter: null`.
7. `retrieval_set` de CH-06 incluye 2 `interleavedQuestions`: una conectando con CH-05
   (`PolicyEngine`/`PolicyDecision`/`REQUIRE_APPROVAL` → `HumanInteractionRequest.callId`) y otra
   con CH-01 (`AgentRunStatus.WAITING_FOR_HUMAN`, todavía sin transición real). `guidingQuestions`
   en lenguaje de problema, sin usar "HumanInteractionService"/"HumanInteractionRequest"/
   "HumanInteractionResolution" literal (verificado con la prueba negativa de §8.4).

## 3. Decisión de diseño central: los campos de `HumanInteractionRequest`/`HumanInteractionResolution`

Como en CH-02..CH-05, no existía una interfaz previa que copiar — el diseño se ancló directamente
en Article III (owns literal), Article IV ("How is required human intervention represented and
resolved?"), Article VIII completo (tipos mínimos, flujo, canales, Human Interaction Rule) e
INV-14/INV-15/INV-19.

**Problema de diseño 1 — ¿un solo contrato o dos?** El encargo fijó explícitamente el patrón
request/resolution (como `ToolCall`/`ToolResult` en CH-02 o `ModelRequest`/`ModelResponse` en
CH-03) en vez de un único `STRUCT` mutable. Se adoptó: `HumanInteractionRequest` representa el
momento "esto está pendiente" (con su propio lifecycle de dos estados, `PENDING`/`RESOLVED`,
seccion 12 del capítulo) y `HumanInteractionResolution` representa el momento "esto es lo que un
humano decidió" — inmutable una vez creada, nunca se actualiza in-place.

**Problema de diseño 2 — la correlación hacia `PolicyDecision`.** Se evaluó agregar un campo
`policyDecisionId` a `HumanInteractionRequest`, pero `PolicyDecision` (C-014, CH-05) no tiene un
identificador propio — solo `callId: ToolCallId`. Inventar un id nuevo para `PolicyDecision`
habría exigido modificar retroactivamente C-014 (`modifies_contracts`), violando el precedente de
no tocar contratos de capítulos anteriores salvo que el propio encargo lo pida. Se adoptó reutilizar
`callId: ToolCallId` como la referencia que dispara la solicitud — la misma correlación que
`PolicyDecision.callId` ya usa hacia el `ToolCall` (C-008, CH-02); dado que un `ToolCall` produce,
como mucho, una `PolicyDecision` real por evaluación, `callId` identifica de forma suficiente cuál
fue la decisión que motivó la solicitud, sin inventar una relación nueva.

**Problema de diseño 3 — `HumanInteractionOutcome` de tres valores, no un `Boolean`.** El encargo
lo pedía explícitamente ("ajústalo al tipo de la request"). Se adoptó:

```pseudocode
ENUM HumanInteractionOutcome
    APPROVED
    REJECTED
    PROVIDED
END
```

con `value: Optional<Value>` poblado únicamente cuando `outcome = PROVIDED` — el mismo patrón
exacto que `PolicyDecision.reason` (CH-05, poblado únicamente cuando `outcome = DENY`). Esto cierra
un eco pedagógico deliberado con CH-05: el mismo argumento que motivó que `PolicyOutcome` no fuera
un `Boolean` (no puede representar "todavía no, requiere aprobación") se repite aquí para que
`HumanInteractionOutcome` tampoco lo sea (no puede representar "el humano proveyó un valor" sin
perder ese valor).

**Problema de diseño 4 — ningún campo de canal, en ningún contrato.** El encargo lo pedía
explícitamente ("NO reinventes un tipo de 'canal' dentro del contrato más allá de una referencia
opaca si la necesitas"). Se decidió no incluir ninguna referencia al canal, ni siquiera opaca:
INV-14 ("Human Interaction nunca depende de una interfaz particular") y la Human Interaction Rule
("las interfaces transportan la interacción; el runtime define y persiste su significado") se
preservan así de forma estructural — el contrato mismo no le deja espacio a esa dependencia,
en vez de confiar en que cada implementación de un Channel Adapter respete la regla por disciplina.
Documentado extensamente en §5/§15/§20 del capítulo como la decisión de mayor efecto de seguridad
(`leverage_point` del `retrieval_set`).

**Problema de diseño 5 — `resolvedBy: ActorId`, un identificador opaco nuevo, no `AgentId`.** Se
evaluó reutilizar `AgentId` (ya existente desde CH-00) para identificar quién resolvió una
solicitud, pero se descartó: `AgentId` identifica, por definición del glosario, "un agente
configurado sobre el runtime" — no a un humano ni a un actor externo que resuelve una interacción.
Se introdujo `ActorId` como identificador opaco nuevo (mismo patrón que CH-00 usó para `MessageId`/
`EventId`: una tabla en la seccion 6, sin `STRUCT Actor`/`User` propio) — misma restricción de
alcance que CH-02 aplicó a `Capability`/`Tool`.

## 4. Otras decisiones de diseño tomadas durante la ejecución

### 4.1 Extender `ErrorCategory` con `HUMAN_INTERACTION` — primer uso real, y primera vez que se agrega un valor a este enum desde CH-00

Se encontró, al releer Article VII (Failure Constitution), que su lista canónica de
`Failure Examples` incluye literalmente `HumanInteractionError` — pero el `ENUM ErrorCategory` que
CH-00 formalizó (`VALIDATION`/`POLICY`/`TOOL`/`MODEL`/`CONTEXT`/`PERSISTENCE`/`INFRASTRUCTURE`/
`BUDGET`/`CANCELLATION`/`FATAL`) nunca llegó a incluir ese valor — a diferencia de `POLICY` o
`CONTEXT` (declarados pero no ejercitados hasta CH-05/CH-04 respectivamente), aquí el valor ni
siquiera existía. Se decidió agregarlo (`HUMAN_INTERACTION`), reproduciendo el `ENUM` completo y
extendiéndolo — exactamente el mismo patrón estructural que cada capítulo anterior ya aplicó a
`AgentEventType` — sin que esto cuente como `modifies_contracts` de `C-011` (`HarnessError`), ya
que su `STRUCT` no cambia, solo el rango de valores del enum embebido (mismo precedente que
`AgentEventType`/`AgentEvent`).

### 4.2 Dos valores nuevos de `AgentEventType`, no un par éxito/fallo de una sola operación

`HUMAN_INTERACTION_REQUESTED` y `HUMAN_INTERACTION_RESOLVED` — uno por cada una de las dos
operaciones reales que `HumanInteractionService` posee (crear la solicitud, recibir la
resolución), no un par éxito/fallo de una sola operación como CH-02/CH-03/CH-04, ni un solo valor
como CH-05. Justificación explícita en §14 del capítulo: cada una de las dos funciones, igual que
`evaluatePolicyForToolCall` (CH-05), siempre produce un resultado válido una vez que su
precondición se satisface; los casos que sí fallan son violaciones de precondición del llamador
(mismo patrón que `TURN_ON_TERMINAL_STATE` en `AgentLoop`, CH-01), no un fallo operacional de la
operación en sí, y por eso no requieren un evento de fallo paralelo.

### 4.3 `VALIDATION` vs. `HUMAN_INTERACTION` como categorías de fallo distintas

`POLICY_DECISION_NOT_REQUIRE_APPROVAL` y `REQUEST_ALREADY_RESOLVED` se clasificaron como
`VALIDATION` (violaciones de precondición de invocación, mismo tipo de error que
`TURN_ON_TERMINAL_STATE` en CH-01). `OUTCOME_TYPE_MISMATCH` (una resolución cuyo `outcome` no
corresponde al `type` de la solicitud — p. ej. `PROVIDED` sobre una solicitud `APPROVAL`) se
clasificó como `HUMAN_INTERACTION`: no es un error de invocar la operación en el momento
equivocado, sino un error de contenido específico del dominio de la interacción humana — la
primera vez que este valor de `ErrorCategory` se ejercita en la práctica.

### 4.4 `HumanInteractionStatus` con dos estados únicamente (`PENDING`/`RESOLVED`), sin `EXPIRED`

A diferencia de `AgentRunStatus` (que sí tiene `EXPIRED` desde CH-01), `HumanInteractionStatus` v1
no modela expiración — documentado explícitamente en §18 como debate reconocido pero fuera de
alcance de v1, para no inflar el contrato más allá de lo que este incremento necesita (misma
disciplina que CH-05 aplicó a `constraints`).

### 4.5 `HumanInteractionService.dependencies: []`

Igual que CH-01..CH-05: no depende de ningún otro componente registrado. La relación real
(`PolicyEngine` invocaría a `HumanInteractionService`; `AgentLoop` reaccionaría a sus contratos) es
la inversa de un `dependency` en el sentido del registry, y ese cableado pertenece a un capítulo
futuro — `registry/components.yaml` de `CMP-001`/`CMP-005` no se modifica en este capítulo.

## 5. Archivos creados

- `book/chapters/06-human-interaction-service/chapter.md` — capítulo completo (22 secciones: 0,
  1-19, 20, 21).
- `planes/2026-09-14-capitulo-06-human-interaction-service.md` — este registro.

## 6. Archivos modificados

- `registry/contracts.yaml` — agrega `C-015 HumanInteractionRequest` y
  `C-016 HumanInteractionResolution`; actualiza `used_by` de `C-004`/`C-010`/`C-011` (agrega
  `CMP-006`) y de `C-014` (agrega `CMP-006`); agrega comentario documentando la decisión de diseño.
- `registry/components.yaml` — agrega `CMP-006 HumanInteractionService`; actualiza el comentario de
  historial.
- `registry/glossary.yaml` — agrega `HumanInteractionService` (kind: component),
  `Human Interaction Request`, `Human Interaction Resolution` (kind: contract), `Channel Adapter`,
  `Human-in-the-loop` (kind: concept).
- `book/book.yaml` — agrega la entrada `CH-06`.
- `book/chapters/05-policy-engine/chapter.md` — únicamente `next_chapter: null` → `CH-06` en el
  frontmatter (sin tocar ninguna otra sección ni la ficha de `CMP-005`).

## 7. Resultado real del pipeline

Comando (desde la raíz del repo, `dist/` borrado antes para forzar un build limpio):

```text
$ rm -rf dist && ./scripts/build-all
...
▶ validate-chapter CH-06      → OK — secciones: 22/19, pseudocode: 10, contratos: 2, componentes: 1
▶ validate-retrieval-set CH-06 → OK — guidingQuestions: 4, interleavedQuestions: 2, flashcards: 5
...
▶ build-book-ir  → OK → dist/book-ir.json (capítulos: 7 / contratos: 16 / componentes: 6 /
  glosario: 42 / flashcards: 30)
▶ build-mind-map
  chapter-05.diagram: 43 nodo(s), 67 arista(s)
  chapter-06.diagram: 49 nodo(s), 78 arista(s) (6 nuevo(s) en este capítulo)
  full-book.diagram: 49 nodo(s), 78 arista(s)
▶ build-web → OK → dist/web/ — index.html + 2 páginas de frontmatter + 7 capítulos + mapa.html
▶ build-pdf → OK → dist/book.pdf (795898 bytes)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
```

Exit code: `0` (verificado explícitamente con `echo $?` tras `rm -rf dist && ./scripts/build-all`).

## 8. Evidencia de verificación concreta

### 8.1 Mapa mental acumulativo (CH-06 > CH-05 > CH-04 > CH-03 > CH-02 > CH-01 > CH-00)

`chapter-05.diagram`: 43 nodos / 67 aristas. `chapter-06.diagram`: **49 nodos / 78 aristas** (6
nodos nuevos: `CH-06`, `CMP-006`, `C-015`, `C-016`, y los conceptos de glosario nuevos que resuelven
a nodos propios). Cumple el criterio del encargo (más nodos/aristas que CH-05). `full-book.diagram`
coincide exactamente con el snapshot de CH-06 (el último), confirmando acumulación real.

### 8.2 Web

- `dist/web/chapters/CH-06.html` existe (145790 bytes), con SVG de mapa mental inline
  (`grep -c '<svg'` == 1).
- Anchors de entidad presentes: `id="CMP-006"` (1), `id="C-015"` (1), `id="C-016"` (1).
- Navegación prev/next verificada en ambos sentidos: `CH-05.html` contiene `href="CH-06.html"` (2
  apariciones); `CH-06.html` contiene `href="CH-05.html"` (3 apariciones).
- Anchors de capítulos previos verificados intactos (1 aparición cada uno): `CH-00.html`
  (`C-001`, `C-004`); `CH-01.html` (`CMP-001`/`C-013`); `CH-02.html` (`CMP-002`/`C-008`);
  `CH-03.html` (`CMP-003`/`C-006`); `CH-04.html` (`CMP-004`/`C-005`); `CH-05.html`
  (`CMP-005`/`C-014`) — sin cambios.
- `dist/web/index.html` lista los siete capítulos (`CH-00`..`CH-06`).

### 8.3 PDF (`pypdf`)

- Build completo (CH-00..CH-06): **153 páginas** — el build de 6 capítulos (CH-00..CH-05) tenía 123
  páginas; 153 > 123, confirmando el crecimiento esperado.
- Texto extraído del PDF completo, verificado con `pypdf.PdfReader(...).extract_text()`:
  `"HumanInteractionService"` → `True`, `"HumanInteractionRequest"` → `True`,
  `"HumanInteractionResolution"` → `True`, `"CMP-006"` → `True`, `"C-015"` → `True`,
  `"C-016"` → `True`, `"HumanInteractionOutcome"` → `True`, `"PROVIDED"` → `True`.

### 8.4 Pruebas negativas (inyectadas y revertidas, una a la vez)

1. **`consumes` inválido en la ficha de componente**: se agregó `C-999` (inexistente) a
   `CMP-006.consumes` en `registry/components.yaml` → `validate-components` falló limpio con
   `exit 1` y el mensaje exacto `Componente CMP-006: consumes referencia contrato inexistente
   "C-999"`. Revertido (`diff` contra el backup confirmó archivo idéntico salvo la línea
   inyectada; `validate-components` volvió a `OK (6 componente(s))`).
2. **Nombre canónico en una guiding question**: se reescribió `GQ-CH06-01` para que dijera
   literalmente "¿decide HumanInteractionService esa solicitud pendiente...?" →
   `validate-retrieval-set` falló limpio con `exit 1` y el mensaje exacto
   `retrievalSet.guidingQuestions[GQ-CH06-01] contiene el nombre canónico "HumanInteractionService",
   que este mismo capítulo introduce — las preguntas guía deben usar lenguaje de problema`. Se
   confirmó además que `./scripts/build-all` completo se detiene en la misma etapa de validación
   (tras haber pasado `validate-contracts`/`validate-components`/CH-00..CH-05 y `validate-chapter`
   de CH-06, fallando exactamente en `validate-retrieval-set` de CH-06), reportando
   `build-all: FALLÓ en la etapa de validación` (`policies/publishing.yaml:
   unresolved_validation_errors = deny`) sin llegar a BookIR/Web/PDF. Revertido (`diff` confirmó
   archivo idéntico; `validate-retrieval-set` volvió a `OK`).
3. Tras revertir ambas inyecciones, `rm -rf dist && ./scripts/build-all` volvió a pasar limpio con
   los mismos conteos de nodos/aristas (49/78), de contratos/componentes (16/6) y de capítulos (7)
   que antes de las inyecciones (exit 0), y el mismo total de páginas de PDF (153, verificado de
   nuevo con `pypdf`).

### 8.5 CH-00..CH-05 no se rompieron

- `validate-chapter`/`validate-retrieval-set` de los seis siguen en verde (ver §7).
- Los anchors de CH-00 (`C-001`, `C-004`), CH-01 (`CMP-001`/`C-013`), CH-02 (`CMP-002`/`C-008`),
  CH-03 (`CMP-003`/`C-006`), CH-04 (`CMP-004`/`C-005`) y CH-05 (`CMP-005`/`C-014`) no cambiaron de
  contenido.
- Solo se editó `next_chapter` en el frontmatter de CH-05 — su cuerpo, su ficha de `PolicyEngine`
  y su `retrieval_set` quedaron intactos.
- `mapa.html` sigue mostrando el grafo acumulado completo con los siete capítulos.

## 9. Definition of Done (restringido a este incremento)

- ✅ CH-06 completo: 22 secciones (0, 1-19, 20, 21), sin relleno — cada sección con contenido real.
- ✅ `registry/contracts.yaml` / `registry/components.yaml` / `registry/glossary.yaml` /
  `book/book.yaml` actualizados y validados (`validate-contracts`, `validate-components`).
- ✅ `RetrievalSet` completo con `interleavedQuestions = 2` conectando con CH-05 y CH-01.
- ✅ Pipeline completo (`build-all`) verde desde `dist/` limpio, para los 7 capítulos.
- ✅ Evidencia concreta (no solo "pasó"): conteos de nodos/aristas del mapa mental, conteo de
  páginas de PDF (153 vs. 123 del build de 6 capítulos), texto extraído del PDF, anchors HTML, dos
  pruebas negativas con mensaje de error exacto y reversión confirmada con conteos idénticos.
- ✅ CH-00..CH-05 verificados intactos tras el cambio (salvo el campo de navegación autorizado en
  CH-05).
- ✅ Frontera `HumanInteractionService` ↔ `PolicyEngine` (recibir la señal vs. decidirla) y
  `HumanInteractionService` ↔ `AgentLoop`/`ToolRuntime` (representar/resolver vs. reanudar/
  ejecutar) documentada explícitamente en §8/§9/§15/§18 del capítulo, sin modificar `CMP-001` ni
  `CMP-005`.
- ✅ `AgentRunStatus.WAITING_FOR_HUMAN` (CH-01) y `PolicyDecision.outcome = REQUIRE_APPROVAL`
  (CH-05) tienen, por primera vez, un mecanismo real que podría satisfacerlos — sin que este
  capítulo sobreestime lo que resuelve: el cableado real que los conecta (`AgentLoop`/`ToolRuntime`)
  sigue siendo, explícitamente, trabajo futuro.

## 10. Deuda intencional hacia el próximo capítulo (`CH-07`, fuera de este alcance)

- **El cableado formal `PolicyEngine → HumanInteractionService`**: `evaluatePolicyForToolCall`
  (CH-05) no invoca `createHumanInteractionRequest` todavía.
- **El cableado formal `HumanInteractionService ↔ AgentLoop`**: ninguna transición real hacia o
  desde `AgentRunStatus.WAITING_FOR_HUMAN`.
- **El cableado formal `HumanInteractionService ↔ ToolRuntime`**: `ToolRuntime.executeToolCall`
  (CH-02) no espera ninguna `HumanInteractionResolution` antes de `Execute`.
- **Channel Adapter real**: ningún `TUI`/`Web`/`Slack`/`Teams`/`Mobile`/`Email`/`API` implementado.
- **Expiración de una `HumanInteractionRequest`**: sin tercer estado `EXPIRED` en v1.
- **`SessionManager` y la persistencia real**: `persistHumanInteractionRequest`/
  `persistHumanInteractionResolution` siguen siendo primitivas asumidas.
- **`ActorId` sin `STRUCT Actor`/`User` propio; `ExecutionController`, `CapabilityRegistry`,
  Provider Adapters reales, streaming real**: deuda heredada, sin cambios en este capítulo.
- Persistencia real de `AgentState`/`SessionState`, reviewers plurales, evals y orquestación
  multi-agente: sin cambios respecto al alcance ya excluido por BH-v0.1.
