# Plan / Registro de ejecución — Capítulo 9: EventBus y la Distribución Desacoplada de un Evento Ya Producido

**Fecha:** 2026-09-14
**Estado:** ✅ Completado — ejecutado en una sola sesión, sobre el estado dejado por `ade1787` (CH-00
..CH-08 como los nueve únicos capítulos reales; los ocho componentes CMP-001..CMP-008 emitiendo
`AgentEvent` de verdad —quince apariciones de `EMIT AgentEvent(...)` repartidas en los nueve archivos
de capítulo— sin que ningún capítulo hubiera dado nunca destino real a ese evento).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-14-capitulo-05-policy-engine.md` .. `2026-09-14-capitulo-08-capability-registry.md`
  (mismo formato, misma disciplina de `owns`/`does_not_own`; CH-05/CH-02 son, además, los dos
  capítulos cuyos `AgentEvent` (`POLICY_EVALUATED`/`TOOL_CALL_COMPLETED`) se usan como ejemplo de
  distribución en este capítulo)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Article III "EventBus", Article IV Decision
  Ownership — notablemente SIN fila para `EventBus`, Article X Observability Constitution completo,
  Article II INV-18/INV-19/INV-20, Article I P-04/P-11/P-12/P-25, Article XI EVO-01 "Event
  Consumer" citado en prosa)

---

## 1. Objetivo

Escribir el décimo capítulo real de contenido del libro ("¿Cómo construir un arnés?"), CH-09, sobre
`EventBus` — el componente que Article III nombra desde la primera versión de la constitución
adoptada, pero que ningún capítulo había instalado — y el primer capítulo que responde, con código
real, la pregunta que quince apariciones de `EMIT AgentEvent(...)` (repartidas en ocho componentes
productores distintos) dejaron sin resolver desde CH-00: ¿a dónde va un `AgentEvent` una vez
construido? Verificar que el capítulo atraviesa todo el pipeline (validadores + BookIR + Web + PDF +
Mapa Mental) sin romper nada de lo que CH-00..CH-08 ya tenían construido.

## 2. Alcance decidido (Paso 2 del encargo, ya cerrado antes de escribir)

Exactamente 1 componente + 1 contrato:

1. **Componente `EventBus` (CMP-009)** — noveno componente de runtime del libro, y el primero cuya
   ficha cita literalmente Article III ("distribuir eventos del runtime a consumidores
   desacoplados") sin que Article IV le asigne ninguna fila propia en su tabla de Decision
   Ownership — hecho verificado por lectura textual completa de Article IV (ver §3.1 de este plan).
   `owns`: registrar una suscripción de un consumidor desacoplado (`subscriberRef` opaco + filtro
   opcional), cancelarla, distribuir (fan-out) cada `AgentEvent` ya producido hacia las
   suscripciones activas que hagan match, y desacoplar al productor de sus consumidores.
   `does_not_own`: decidir qué información va dentro de un `AgentEvent` (cada componente productor
   ya lo decide, CMP-001..CMP-008), interpretar o actuar sobre un evento distribuido (los nueve
   consumidores de Article X, ninguno componente propio de este registry), persistir historial de
   sesión de forma durable (`SessionManager`, preview), y decidir continuación de turno u otra
   decisión arquitectónica (`AgentLoop`/`PolicyEngine`/`ExecutionController`, ya existentes).
   `consumes`: `C-010 AgentEvent` (lo que distribuye); `produces`: `C-011 HarnessError`,
   `C-019 EventSubscription` (el contrato nuevo) — deliberadamente **sin** `C-010` en `produces` (ver
   §3.2) y **sin** `C-004 ExecutionContext` en `consumes` (ver §3.3).
2. **Contrato nuevo `EventSubscription` (C-019)** — el registro de la relación entre un consumidor
   desacoplado (`subscriberRef: Text`, opaco por diseño) y los eventos que le interesan (`filter:
   Optional<EventFilter>`, embebido, sin contrato `C-XXX` propio — mismo patrón que
   `RawToolCallProposal`/`ContextBlock`/`ExecutionUsage`), junto con su estado
   (`EventSubscriptionStatus`: `ACTIVE`/`CANCELLED`) y `subscribedAt: Timestamp`.
3. **El momento central del capítulo — distribución real**: `distributeEvent` (§11) toma un
   `AgentEvent` ya producido por cualquier componente y una lista de `EventSubscription` ya
   registradas, filtra las activas que hagan match (`eventMatchesFilter`, la primera "puerta" del
   libro que es pseudocódigo real de principio a fin, no una señal asumida) y entrega
   (`deliver`, primitiva asumida) el evento a cada una — demostrado con dos ejemplos reales: un
   `AgentEvent` con la forma exacta de `POLICY_EVALUATED` (`PolicyDecision`, CH-05) y otro con la
   forma exacta de `TOOL_CALL_COMPLETED` (`ToolResult`, CH-02), sin que ninguno de los dos
   componentes productores cambie una sola línea.
4. **Frontera con los ocho componentes productores**: no se editó `registry/components.yaml` en las
   entradas de `CMP-001`..`CMP-008` (mismo precedente que CH-02..CH-08). El pseudocódigo de este
   capítulo es autónomo.
5. No se tocó `book/chapters/00-*` a `07-*`; de CH-08 solo se tocó `next_chapter: null → CH-09` en
   el frontmatter.
6. `book/book.yaml` agrega CH-09 después de CH-08; CH-09 frontmatter → `previous_chapter: CH-08`,
   `next_chapter: null`.
7. `retrieval_set` de CH-09 incluye 2 `interleavedQuestions`: una conectando con CH-02
   (`ToolRuntime`/`ToolResult`/`TOOL_CALL_COMPLETED`) y otra con CH-05 (`PolicyEngine`/
   `PolicyDecision`/`POLICY_EVALUATED`) — los mismos dos ejemplos que el pseudocódigo usa.
   `guidingQuestions` en lenguaje de problema, sin usar "EventBus"/"EventSubscription" literal
   (verificado con la prueba negativa de §8.4).

## 3. Decisiones de diseño centrales

### 3.1 La ausencia de `EventBus` en la tabla de Decision Ownership de Article IV

Antes de escribir la ficha del componente se leyó Article IV completo (línea por línea): enumera
`LLM`, `AgentLoop`, `ContextEngine`, `ModelGateway`, `ToolRuntime`, `PolicyEngine`,
`HumanInteractionService`, `SessionManager`, `ExecutionController`, `CapabilityRegistry`, `UI` — once
filas, y **ninguna** para `EventBus`, pese a que Article III sí lo nombra en su árbol de componentes.
Se decidió no "corregir" esa ausencia inventando una pregunta que Article IV no hace: en cambio, el
capítulo la usa como el argumento central de §4/§8/§20 — `EventBus` es el primer componente real del
libro que confirma, con código propio, que no le pertenece ninguna decisión, solo la distribución.
Esto se verificó de forma determinista buscando `EventBus` en todo `Article IV` del archivo
constitucional (cero coincidencias) antes de afirmarlo en prosa.

### 3.2 Por qué `EventBus` no produce `AgentEvent` ni agrega valores a `AgentEventType`

Problema de diseño evaluado explícitamente: ¿debería `EventBus` emitir su propio `AgentEvent` cuando
registra una suscripción o cuando distribuye un evento (siguiendo el patrón de los ocho capítulos
anteriores, que agregaron 1-2 valores nuevos cada uno)? Se descartó por dos razones, ambas
documentadas en §14 del capítulo:

1. Una `EventSubscription` no está necesariamente ligada a un único `AgentRun` (su `filter.runId`
   puede ser `NULL`), así que `EventBus` no siempre tiene un `ExecutionContext` real con el cual
   fabricar, de forma honesta, los campos obligatorios (`runId`/`sessionId`/`traceId`) de un
   `AgentEvent` propio.
2. Emitir un evento sobre "distribuí este evento" sería circular: ese nuevo evento también tendría
   que distribuirse, y `EventBus` tendría que decidir que su propia distribución es "significativa"
   (INV-18) — exactamente la interpretación de contenido que su `does_not_own` le prohíbe.

Consecuencia directa en el registry: `CMP-009.produces` **no** incluye `C-010` (a diferencia de
`CMP-001`..`CMP-008`, que sí lo incluyen todos) — la primera vez que un componente real del libro no
produce `AgentEvent`. `C-010.used_by` sí incluye `CMP-009` (lo consume para distribuirlo), tal como
pedía el encargo.

### 3.3 Por qué `EventBus` no consume `ExecutionContext`

Consecuencia del mismo argumento: los ocho componentes anteriores consumían `C-004 ExecutionContext`
porque cada uno necesitaba `runId`/`sessionId`/`traceId` para fabricar su propio `AgentEvent` nuevo.
`EventBus` nunca fabrica un `AgentEvent` nuevo — solo recibe uno ya completo — así que no tiene
ninguna necesidad real de un `ExecutionContext` propio. Se documentó explícitamente en §9 como la
primera vez que esto ocurre en el libro, en vez de agregarlo por inercia solo para "verse igual" que
los capítulos anteriores.

### 3.4 `eventMatchesFilter`: la primera "puerta" del libro sin señal asumida

CH-02 (`inputValid`) y CH-08 (`argumentsMatchSchema`) modelaron su gate de validación como una señal
booleana de entrada asumida, porque el schema contra el que comparaban (`Value` genérico) no tiene
lenguaje de validación definido en este libro. `EventFilter`, en cambio, tiene una forma
completamente conocida y simple (dos campos opcionales, comparación directa) — se decidió,
deliberadamente, escribir `eventMatchesFilter` como pseudocódigo real y completo, marcando en el
propio capítulo (§11) que esta es la primera vez que el libro resuelve una "puerta" así sin dejar
ningún tramo pendiente.

### 3.5 `EventFilter` con exactamente dos campos (`eventType`, `runId`), no un lenguaje de filtrado genérico

El encargo permitía "un filtro por eventType/runId/etc.". Se decidió modelar únicamente esos dos
campos, documentando explícitamente en §6/§18 que un filtro adicional (`sessionId`, `agentId`, rango
de `timestamp`) queda fuera de alcance — dos campos alcanzan para demostrar el mecanismo de match
completo sin necesitar un lenguaje de filtrado genérico, que hubiera sido una segunda entidad nueva
fuera del alcance de "1 componente + 1 contrato".

### 3.6 Reutilizar `VALIDATION`, no introducir una categoría `EVENT_BUS`/`SUBSCRIPTION` nueva

Mismo argumento que CH-08 §3 (Problema de diseño 3): `SUBSCRIBER_REF_REQUIRED`,
`SUBSCRIPTION_NOT_FOUND`, `SUBSCRIPTION_ALREADY_CANCELLED` y `DISTRIBUTION_REQUESTED_WITHOUT_EVENT`
son, todos, fallos de validación de entrada — no de la distribución en sí. Se evaluó y descartó una
categoría nueva por la misma razón de fragmentación sin ganancia semántica.

### 3.7 `cancelSubscription` es terminal — no se modela reactivación

Mismo patrón que `HumanInteractionStatus` (CH-06, dos estados, sin `EXPIRED`): `cancelSubscription`
sobre una suscripción ya `CANCELLED` es un `HarnessError` (`SUBSCRIPTION_ALREADY_CANCELLED`), no una
operación idempotente ni una reactivación — documentado como límite deliberado en §12/§18.

## 4. Otras decisiones de diseño tomadas durante la ejecución

### 4.1 Grounding constitucional de `constitutional_articles`

Se buscó, principio por principio (P-01..P-30), cuáles aplican de verdad a un "dumb pipe" de
distribución: `P-04` ("Every action produces observable events" — la mitad que `EventBus` completa),
`P-11` ("UI is an adapter" — UI recibe su evento igual que cualquier consumidor), `P-12` ("Events
observe; hooks intervene" — la cita que sostiene todo el `does_not_own`), `P-25` ("Audit evidence is
distinct from operational telemetry" — por qué `EventBus` no fusiona los nueve consumidores en un
canal indiferenciado). Se descartó `EVO-01` como entrada de `constitutional_articles` (aunque se
cita en prosa, §3): `scripts/lib/registries.js` (`loadConstitutionArticleIds`) solo reconoce
`P-\d{2}`/`INV-\d{2}`/`INV-E\d{2}`, nunca `EVO-\d{2}` — incluirlo en el frontmatter habría fallado
`validate-chapter` con "referencia artículo inexistente".

### 4.2 Los dos ejemplos de distribución (`POLICY_EVALUATED`/CH-05, `TOOL_CALL_COMPLETED`/CH-02)

Se eligieron, entre los dieciséis valores de `AgentEventType` disponibles, dos que ya tenían un
`payload` con contrato propio bien establecido (`PolicyDecision`, `ToolResult`) y que pertenecen a
capítulos suficientemente distantes entre sí (CH-02 y CH-05) para demostrar que la distribución es
uniforme sin importar el productor ni la antigüedad del contrato.

### 4.3 `EventBus.dependencies: []`

Igual que CH-01..CH-08: no depende de ningún otro componente registrado. El cableado real de cada
`EMIT` de los ocho productores hacia `distributeEvent` es, explícitamente, trabajo de un capítulo de
integración futuro.

## 5. Archivos creados

- `book/chapters/09-event-bus/chapter.md` — capítulo completo (22 secciones: 0, 1-19, 20, 21).
- `planes/2026-09-14-capitulo-09-event-bus.md` — este registro.

## 6. Archivos modificados

- `registry/contracts.yaml` — agrega `C-019 EventSubscription`; actualiza `used_by` de `C-010`
  (agrega `CMP-009`); agrega comentario documentando la decisión de diseño.
- `registry/components.yaml` — agrega `CMP-009 EventBus`; actualiza el comentario de historial.
- `registry/glossary.yaml` — agrega `EventBus` (kind: component), `Event Subscription` (kind:
  contract), `Fan-out`, `Subscriber / Decoupled Consumer`, `Event Filter` (kind: concept).
- `book/book.yaml` — agrega la entrada `CH-09`.
- `book/chapters/08-capability-registry/chapter.md` — únicamente `next_chapter: null` → `CH-09` en
  el frontmatter (sin tocar ninguna otra sección ni la ficha de `CMP-008`).

## 7. Resultado real del pipeline

Comando (desde la raíz del repo, `dist/` borrado antes para forzar un build limpio):

```text
$ rm -rf dist && ./scripts/build-all
...
▶ validate-chapter book/chapters/09-event-bus/chapter.md
validate-chapter: OK — secciones: 22/19, bloques pseudocode: 9, contratos introducidos: 1,
  componentes introducidos: 1
▶ validate-retrieval-set book/chapters/09-event-bus/chapter.md
validate-retrieval-set: OK — guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2,
  interleavedQuestions: 2, flashcards: 5, calibrationPairs: 4
...
▶ build-book-ir → OK → dist/book-ir.json (capítulos: 10 / contratos: 19 / componentes: 9 /
  glosario: 56 / flashcards: 45)
▶ build-mind-map
  chapter-08.diagram: 60 nodo(s), 99 arista(s)
  chapter-09.diagram: 66 nodo(s), 107 arista(s) (6 nuevo(s) en este capítulo)
  full-book.diagram: 66 nodo(s), 107 arista(s)
▶ build-web → OK → dist/web/ — index.html + 2 páginas de frontmatter + 10 capítulos + mapa.html
▶ build-pdf → OK → dist/book.pdf (1173286 bytes)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
```

Exit code: `0` (verificado explícitamente con `echo $?` tras `rm -rf dist && ./scripts/build-all`,
y de nuevo tras revertir las dos pruebas negativas de §8.4, con conteos idénticos).

## 8. Evidencia de verificación concreta

### 8.1 Mapa mental acumulativo (CH-09 > CH-08 > ... > CH-00)

`chapter-08.diagram`: 60 nodos / 99 aristas. `chapter-09.diagram`: **66 nodos / 107 aristas** (6
nodos nuevos: `CH-09`, `CMP-009`, `C-019`, y los conceptos de glosario nuevos que resuelven a nodos
propios). Cumple el criterio del encargo (más nodos/aristas que CH-08). `full-book.diagram` coincide
exactamente con el snapshot de CH-09 (el último), confirmando acumulación real.

Aristas confirmadas explícitamente (grafo acumulado, incluyendo una referencia hacia `C-010`, seis
capítulos antes):

```text
"CMP-009" -> "C-011" [label="PRODUCES", ...];
"CMP-009" -> "C-019" [label="PRODUCES", ...];
"C-010" -> "CMP-009" [label="CONSUMES", ...];   ← C-010 introducido en CH-00, nueve capítulos antes
```

### 8.2 Web

- `dist/web/chapters/CH-09.html` existe, con SVG de mapa mental inline (`grep -c '<svg'` == 1).
- Anchors de entidad presentes: `id="CMP-009"` (1), `id="C-019"` (1).
- Navegación prev/next verificada en ambos sentidos: `CH-08.html` contiene `href="CH-09.html"`;
  `CH-09.html` contiene `href="CH-08.html"`.
- Anchors de capítulos previos verificados intactos (1 aparición cada uno): CH-00 (`C-001`), CH-01
  (`CMP-001`/`C-013`), CH-02 (`CMP-002`/`C-008`), CH-03 (`CMP-003`/`C-006`), CH-04
  (`CMP-004`/`C-005`), CH-05 (`CMP-005`/`C-014`), CH-06 (`CMP-006`/`C-015`), CH-07
  (`CMP-007`/`C-017`), CH-08 (`CMP-008`/`C-018`) — sin cambios.
- `<svg` aparece exactamente 1 vez en cada una de las 10 páginas de capítulo (CH-00..CH-09).
- `dist/web/index.html` lista los diez capítulos (`CH-00`..`CH-09`).

### 8.3 PDF (`pypdf`)

- Build completo (CH-00..CH-09): **229 páginas** — el build de 9 capítulos (CH-00..CH-08) tenía 201
  páginas (ver `planes/2026-09-14-capitulo-08-capability-registry.md` §8.3); 229 > 201, confirmando
  el crecimiento esperado.
- Texto extraído del PDF completo, verificado con `pypdf.PdfReader(...).extract_text()`:
  `"EventBus"` → `True`, `"EventSubscription"` → `True`, `"CMP-009"` → `True`, `"C-019"` → `True`,
  `"Fan-out"` → `True`, `"subscriberRef"` → `True`.

### 8.4 Pruebas negativas (inyectadas y revertidas, una a la vez)

1. **`consumes` inválido en la ficha de componente**: se agregó `C-999` (inexistente) a
   `CMP-009.consumes` en `registry/components.yaml` → `validate-components` falló limpio con
   `exit 1` y el mensaje exacto `Componente CMP-009: consumes referencia contrato inexistente
   "C-999"`. Revertido (`diff` contra el backup en `/tmp/components.yaml.bak` confirmó archivo
   idéntico; `validate-components` volvió a `OK (9 componente(s))`, `exit 0`).
2. **Nombre canónico en una guiding question**: se reescribió `GQ-CH09-01` para que dijera
   literalmente "¿Decide EventBus quién más se entera de que un AgentEvent ya producido por otro
   componente ocurrió?" → `validate-retrieval-set` falló limpio con `exit 1` y el mensaje exacto
   `retrievalSet.guidingQuestions[GQ-CH09-01] contiene el nombre canónico "EventBus", que este mismo
   capítulo introduce — las preguntas guía deben usar lenguaje de problema`. Revertido (`diff`
   contra el backup en `/tmp/ch09.md.bak` confirmó archivo idéntico; `validate-retrieval-set` volvió
   a `OK`, `exit 0`).
3. Tras revertir ambas inyecciones (`diff` confirmó archivos idénticos byte a byte), `rm -rf dist &&
   ./scripts/build-all` volvió a pasar limpio con los mismos conteos de nodos/aristas (66/107), de
   contratos/componentes (19/9), de capítulos (10) y de páginas de PDF (229, verificado de nuevo con
   `pypdf`) que antes de las inyecciones (exit 0).

### 8.5 CH-00..CH-08 no se rompieron

- `validate-chapter`/`validate-retrieval-set` de los nueve siguen en verde (ver §7, corrida completa
  de `build-all`).
- Los anchors de CH-00..CH-08 no cambiaron de contenido (ver §8.2).
- Solo se editó `next_chapter` en el frontmatter de CH-08 — su cuerpo, su ficha de
  `CapabilityRegistry` y su `retrieval_set` quedaron intactos.
- `mapa.html` sigue mostrando el grafo acumulado completo con los diez capítulos.

## 9. Definition of Done (restringido a este incremento)

- ✅ CH-09 completo: 22 secciones (0, 1-19, 20, 21), sin relleno — cada sección con contenido real.
- ✅ `registry/contracts.yaml` / `registry/components.yaml` / `registry/glossary.yaml` /
  `book/book.yaml` actualizados y validados (`validate-contracts`, `validate-components`).
- ✅ `RetrievalSet` completo con `interleavedQuestions = 2` conectando con CH-02 y CH-05.
- ✅ Pipeline completo (`build-all`) verde desde `dist/` limpio, para los 10 capítulos.
- ✅ Evidencia concreta: conteos de nodos/aristas del mapa mental, conteo de páginas de PDF (229 vs.
  201 del build de 9 capítulos), texto extraído del PDF, anchors HTML, dos pruebas negativas con
  mensaje de error exacto y reversión confirmada con conteos idénticos.
- ✅ CH-00..CH-08 verificados intactos tras el cambio (salvo el campo de navegación autorizado en
  CH-08).
- ✅ Frontera `EventBus` ↔ CMP-001..CMP-008 documentada explícitamente en §8/§9/§15/§18 del
  capítulo, sin modificar ningún componente previo.
- ✅ `EventBus` es, por diseño explícito y documentado, el primer componente real sin fila en
  Article IV, el primero que no consume `ExecutionContext`, y el primero (junto con CH-01, por una
  razón distinta) que no agrega valores a `AgentEventType`.

## 10. Deuda intencional hacia el próximo capítulo (fuera de este alcance)

- **El cableado real de cada `EMIT` hacia `distributeEvent`**: ningún componente productor fue
  modificado para invocar de verdad la distribución.
- **El mecanismo real de alta/persistencia de una `EventSubscription`**: llega como parámetro ya
  poblado, mismo patrón que `registeredCapabilities` en CH-08.
- **Autorización sobre quién puede suscribirse a qué**: señalado explícitamente en §15/§18 como un
  límite de seguridad real, no silenciado.
- **Los nueve consumidores concretos de Article X**: siguen sin componente propio.
- **Garantías de entrega, reactivación de suscripciones, filtros adicionales**: fuera de alcance.
- **`SessionManager`, `AgentCore`, Provider Adapters reales, el pipeline de integración completo**:
  deuda heredada, sin cambios en este capítulo — de los once nombres de Article III, solo
  `AgentCore` y `SessionManager` siguen preview.
- Reviewers plurales, evals y orquestación multi-agente: explícitamente fuera de alcance de BH-v0.1.
