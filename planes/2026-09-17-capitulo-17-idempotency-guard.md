# Plan / Registro de ejecución — Capítulo 17: IdempotencyGuard y la Deduplicación de un Side Effect Crítico

**Fecha:** 2026-09-17
**Estado:** ✅ Completado, sobre el estado dejado por `0755573` (CH-00..CH-16 como los diecisiete
únicos capítulos reales; Capability & Integration Plane, tercer plano de Amendment v1.1 cubierto por
el libro, con `CredentialBroker`, CMP-014).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-14-capitulo-16-credential-broker.md` (precedente inmediato: tercer componente de
  Amendment v1.1, formato de capítulo más actualizado, y el hallazgo real de `render-diagram.js`
  sobre `xdvipdfmx`/Ghostscript que este capítulo reutiliza sin modificar)
- `2026-09-14-capitulo-14-admission-controller.md` / `2026-09-14-capitulo-15-agent-communication-gateway.md`
  (precedentes de componentes de Amendment v1.1 sin nombre en Article III, patrón de `does_not_own`
  citando componentes ya registrados)
- `2026-09-13-capitulo-02-tool-runtime.md` (origen del hueco genuino que este capítulo protege:
  `ToolCall`/`ToolResult`/`executeToolCall` nunca modelaron deduplicación)
- `2026-09-14-capitulo-07-execution-controller.md` (el componente cuya frontera con este capítulo
  hay que distinguir con más cuidado: "reintentar por presupuesto" vs. "deduplicar una ejecución ya
  exitosa")
- `2026-09-13-capitulo-00-arquitectura-constitucion.md` (origen de `INV-11`, nunca antes citado en
  prosa por ningún capítulo)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Article II completo — `INV-11`; Amendment v1.1 —
  `P-24`/`INV-E09`, "Canonical Enterprise Planes")
- `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §26 (estructura obligatoria de capítulo)

---

## 1. Objetivo

Escribir el decimoctavo capítulo real de contenido del libro ("¿Cómo construir un arnés?"), CH-17,
sobre el cuarto plano de Amendment v1.1 que este libro cubre — el "Reliability Plane" — cerrando
`INV-11`, un invariante del Article II original de la Constitution declarado desde CH-00 y nunca
antes resuelto por ningún componente. Verificar que el capítulo atraviesa todo el pipeline
(validadores + BookIR + Web + PDF + Mapa Mental) sin romper nada de lo que CH-00..CH-16 ya tenían
construido.

## 2. Alcance decidido (Paso 2 del encargo, ya cerrado antes de escribir)

Exactamente 1 componente + 1 contrato:

1. **Componente `IdempotencyGuard` (CMP-015)** — cuarto componente de este registry que NO
   corresponde a ninguno de los once nombres del árbol de Article III; pertenece al "Reliability
   Plane" de Amendment v1.1 (el séptimo plano canónico de la lista, el cuarto que este libro
   cubre). `owns` (cita literal de `INV-11`/`P-24`/`INV-E09`): detectar cuándo un `ToolCall` con
   side effects (C-008, CH-02) ya se ejecutó antes bajo la misma clave de idempotencia; decidir si
   una ejecución repetida debe reusar el `ToolResult` (C-009, CH-02) ya conocido en vez de que el
   side effect real vuelva a ejecutarse; registrar, de forma terminal y write-once, el
   `IdempotencyRecord` que resulta de una ejecución nueva ya concluida; rechazar por defecto cuando
   la clave no corresponde a la capability solicitada o cuando se intenta re-registrar una
   ejecución ya `COMPLETED`. `does_not_own`: ejecutar el side effect en sí (`ToolRuntime`, CH-02),
   decidir autorización (`PolicyEngine`, CH-05), resolver qué implementación satisface la
   capability (`CapabilityRegistry`, CH-08), decidir si un run puede reintentar contra su
   presupuesto (`ExecutionController`, CH-07 — la distinción central de este capítulo), generar la
   clave de idempotencia misma, y el mecanismo real de persistencia atómica.
2. **Contrato nuevo `IdempotencyRecord` (C-027)** — el registro persistido de una clave de
   idempotencia ya vista: `id`, `idempotencyKey` (`Text`, asumida como dada), `capability`
   (`CapabilityId`, referencia opaca), `originalToolCallId` (`ToolCallId`), `status`
   (`IdempotencyRecordStatus`: `PENDING`/`COMPLETED`, `ENUM` nuevo de dos valores — nunca un
   `Boolean`), `result` (`Optional<ToolResult>`), `createdAt` (`Timestamp`) y `completedAt`
   (`Optional<Timestamp>`).
3. **Pseudocódigo autónomo**: `checkIdempotency(toolCall, idempotencyKey, existingRecordForKey,
   execution, agentId) -> Optional<IdempotencyRecord>` y `recordIdempotentExecution(toolCall,
   toolResult, idempotencyKey, existingRecordForKey, execution, agentId) -> IdempotencyRecord`, sin
   modificar `ToolRuntime.executeToolCall` (CH-02). La prosa (seccion 9/18) deja explícito que
   "`ToolRuntime` consulta `IdempotencyGuard` antes de ejecutar y registra el resultado después" es
   trabajo de un capítulo de integración futuro — mismo patrón que domina el libro desde CH-03.
4. No se tocó `book/chapters/00-*` a `15-*`; de CH-16 solo se tocó `next_chapter: null → CH-17` en
   el frontmatter.
5. `book/book.yaml` agrega CH-17 después de CH-16; CH-17 frontmatter → `previous_chapter: CH-16`,
   `next_chapter: null`.
6. `retrieval_set` de CH-17 incluye 2 `interleavedQuestions`: una conectando con CH-02
   (`ToolRuntime`/`ToolCall`/`ToolResult`, la frontera más importante para la integración futura) y
   otra con CH-07 (`ExecutionController`, para contrastar "reintentar por fallo de presupuesto" vs.
   "deduplicar una ejecución ya exitosa"). `guidingQuestions` en lenguaje de problema, sin usar
   "IdempotencyGuard"/"IdempotencyRecord" literal (verificado con la prueba negativa de §8.2).
7. `scripts/lib/render-diagram.js` (fix de Ghostscript de CH-16): revisado, no modificado — sigue
   funcionando correctamente para el mapa mental de este capítulo (116 nodos/179 aristas, más
   grande que el de CH-16), sin ningún error nuevo de `xdvipdfmx` (ver seccion 6.1).

## 3. Decisiones de diseño centrales

### 3.1 Confirmación de los próximos ids libres (verificados, no asumidos)

Se leyó `registry/contracts.yaml` y `registry/components.yaml` completos antes de escribir. El
último contrato registrado era `C-026` (`CredentialReference`, CH-16) — el próximo id libre es
`C-027`. El último componente registrado era `CMP-014` (`CredentialBroker`, CH-16) — el próximo id
libre es `CMP-015`. Verificado con grep que ningún nombre candidato (`IdempotencyGuard`,
`IdempotencyRecord`, `IdempotencyRecordStatus`) colisionaba ya con algo registrado.

### 3.2 Por qué `INV-11` (Article II original) motiva este capítulo, no solo Amendment v1.1

Se verificó explícitamente con grep, ANTES de escribir, dónde CH-00 cita `INV-11`: únicamente en la
lista `constitutional_articles` del frontmatter de `book/chapters/00-arquitectura-constitucion/chapter.md`
— nunca en el cuerpo/prosa de ese capítulo ni de ningún capítulo posterior. Esto confirma la premisa
del encargo: `INV-11` fue "declarado" (listado) desde CH-00, pero nunca "resuelto" con un componente
propio ni siquiera citado en prosa, en diecisiete capítulos reales. Se verificó también que CH-08
§18 ya había señalado la mitad de Amendment v1.1 del mismo problema ("Idempotencia y semántica de
reintentos de una capability, `P-24`") como "fuera de alcance, igual que en capítulos anteriores" —
grep confirmó que esa es la única mención previa en prosa de `P-24` en todo el libro antes de este
capítulo.

### 3.3 Corrección explícita del número de plano canónico

El encargo describía el "Reliability Plane" como "cuarto plano canónico". Se verificó con grep
directo sobre la sección "Canonical Enterprise Planes" de `constitution/ARCHITECTURE_CONSTITUTION.md`
que el Reliability Plane ocupa, en realidad, la **séptima** posición de los nueve planos canónicos
(1. Ingress & Activation, 2. Execution, 3. Agent Interoperability, 4. Capability & Integration, 5.
Data & Context, 6. Control, 7. Reliability, 8. Observability & Governance, 9. Execution Fabric) — no
la cuarta. Lo que sí es exacto es que este es el **cuarto plano que el libro cubre** (después de
Ingress & Activation CH-14, Agent Interoperability CH-15, Capability & Integration CH-16). Se
documentó esta corrección explícitamente en la apertura del capítulo, con la misma disciplina de
"confirmar con grep, no asumir" que el encargo pedía, en vez de repetir silenciosamente la cifra
incorrecta del encargo.

### 3.4 Por qué `IdempotencyGuard`, y por qué es una síntesis de este libro, no una cita literal

A diferencia de `AdmissionController` (`INV-E01`/`INV-E02`, cita indirecta de "AdmissionController"),
`AgentCommunicationGateway` (`P-19`, cita literal del nombre) y `CredentialBroker` (`INV-E08`, cita
literal del nombre), se verificó con grep completo sobre `constitution/ARCHITECTURE_CONSTITUTION.md`
que ningún invariante o principio —ni `INV-11` (Article II) ni `P-24`/`INV-E09` (Amendment v1.1)—
nombra un componente específico para resolver idempotencia. Se evaluaron tres candidatos:
`IdempotencyGuard` (el sugerido por el encargo), `DeduplicationBroker` (descartado: "Broker" ya
describe, en este libro, un componente que resuelve una referencia externa opaca —`CredentialBroker`—,
un rol distinto de "detectar una repetición e impedir que se duplique") y `SideEffectLedger`
(descartado: "Ledger" sugiere un registro contable pasivo, y minimiza la función activa de bloqueo/
decisión que este componente cumple). Se adoptó `IdempotencyGuard` — "Guard" describe con precisión
la función de interceptar antes de que un side effect se repita — y se documentó explícitamente, en
la apertura del capítulo y en `registry/components.yaml`, que este nombre es una síntesis de este
libro, no una cita literal de un nombre ya existente en la Constitution.

### 3.5 `IdempotencyRecordStatus` como `ENUM` de dos valores, nunca un `Boolean`, y por qué no un
tercer valor para "nunca visto"

Se evaluó explícitamente un campo `Boolean alreadyExecuted`. Se descartó: un `Boolean` de dos
estados solo distingue "visto antes" / "no visto antes", y no le dice a un llamador si debe reusar
un resultado (`COMPLETED`) o esperar porque el side effect todavía está en curso (`PENDING`) — dos
acciones correctas opuestas que un solo bit colapsaría. Se evaluó también agregar un tercer valor
`NOT_FOUND` al `ENUM` para representar "nunca visto". Se descartó: la ausencia total de un
`IdempotencyRecord` (`Optional<IdempotencyRecord> = NULL` en `checkIdempotency`) ya representa esa
situación sin necesidad de un valor de `ENUM` adicional — el mismo argumento que ya evitó un campo
centinela en `CredentialReference.expiresAt` (CH-16 §6).

### 3.6 `capability: CapabilityId`, nunca el `ToolCall` completo embebido

Mismo argumento que ya usó `CredentialReference.capability` en CH-16 §6 y `DelegationGrant.
delegatingRunId` en CH-15 §6: una referencia por id evita que `IdempotencyRecord` cargue una copia
que podría quedar desactualizada respecto al `ToolCall` real, y sirve exclusivamente para una
verificación acotada (que la clave encontrada no se reutilice, por error, para una capability
distinta) — nunca para "confirmar" la identidad de la intención lógica, que es exactamente lo que la
`idempotencyKey` ya resuelve sin ambigüedad.

### 3.7 Por qué `recordIdempotentExecution` preserva `id`/`createdAt` de un registro `PENDING` previo

Se decidió que, cuando `existingRecordForKey` ya existe en estado `PENDING`, completar esa ejecución
debe producir el mismo `IdempotencyRecord` lógico (identidad preservada), nunca un segundo registro
independiente para la misma clave — evitando la ambigüedad de que dos registros coexistan para una
misma `idempotencyKey`.

### 3.8 Por qué `recordIdempotentExecution` rechaza sobrescribir un registro ya `COMPLETED`

Write-once explícito: si una llamada posterior pudiera sobrescribir un `IdempotencyRecord` terminal
ya `COMPLETED`, una entrega duplicada tardía podría reemplazar un resultado correcto con uno
potencialmente distinto — exactamente lo que `INV-11` exige impedir. Se agregó
`IDEMPOTENCY_RECORD_ALREADY_COMPLETED` como fallo explícito en vez de permitir la sobrescritura
silenciosa.

### 3.9 `IDEMPOTENCY` como nueva categoría de `ErrorCategory`, no `VALIDATION` ni `BUDGET`

Se evaluó reutilizar `VALIDATION` (parecido superficial: un mismatch de clave/capability) y `BUDGET`
(parecido superficial: ambos son límites operacionales). Se descartaron ambos: `VALIDATION`
pertenece, en exclusiva, a fallos de forma/esquema de una intención de acción; `BUDGET` pertenece,
en exclusiva, a límites operacionales agregados de un run completo. Se agregó `IDEMPOTENCY` como
decimoquinto valor de `ErrorCategory` — el sexto capítulo en extender ese `ENUM` desde CH-00
(después de `HUMAN_INTERACTION` CH-06, `ADMISSION` CH-14, `DELEGATION` CH-15, `CREDENTIAL` CH-16).

### 3.10 Distinción central del capítulo: `IdempotencyGuard` vs. `ExecutionController` (CH-07)

Documentada extensamente en la seccion 15 del capítulo (la más importante): "¿puedo seguir
intentando contra mi presupuesto?" (`ExecutionController`) y "¿ya se ejecutó este side effect con
éxito?" (`IdempotencyGuard`) son preguntas ortogonales sobre materiales distintos — un run puede
tener presupuesto de sobra y, aun así, estar a punto de duplicar un side effect ya ejecutado; y un
run puede haber agotado su presupuesto sin que eso tenga relación alguna con si algún `ToolCall`
particular ya se había ejecutado antes. Esta distinción es, explícitamente, la razón por la que el
encargo pidió conectar CH-17 con CH-07 en `interleaved_questions`.

## 4. Archivos creados

- `book/chapters/17-idempotency-guard/chapter.md` — capítulo completo (22 secciones: 0, 1-19, 20,
  21).
- `planes/2026-09-17-capitulo-17-idempotency-guard.md` — este registro.

## 5. Archivos modificados

- `registry/contracts.yaml` — agrega `C-027 IdempotencyRecord`, con comentario documentando por qué
  `status` es un `ENUM` de dos valores.
- `registry/components.yaml` — agrega `CMP-015 IdempotencyGuard`; actualiza el comentario de
  historial, documentando explícitamente que el nombre es una síntesis de este libro (ningún texto
  de la Constitution lo nombra literalmente).
- `registry/glossary.yaml` — agrega `IdempotencyGuard` (component), `IdempotencyRecord` (contract),
  `Idempotency Key`, `Deduplication`, `Duplicate Delivery`, `Concurrent Execution Guard` (kind:
  concept).
- `book/book.yaml` — agrega la entrada `CH-17`.
- `book/chapters/16-credential-broker/chapter.md` — únicamente `next_chapter: null` → `CH-17` en el
  frontmatter (sin tocar ninguna otra sección).
- `scripts/lib/render-diagram.js` — **no modificado**. Se revisó explícitamente (per el encargo) y
  se confirmó que sigue funcionando sin ningún error nuevo de `xdvipdfmx` para el mapa mental de
  este capítulo (116 nodos/179 aristas — más grande que el de CH-16, que fue el primero en cruzar
  el umbral que motivó el fix). No se encontró ningún problema real que documentar.

## 6. Resultado real del pipeline

### 6.1 `scripts/lib/render-diagram.js` — revisado, sin cambios

Se leyó el archivo completo antes de escribir este capítulo, y se verificó, en la corrida completa
de `build-all` (§6.2), que el mapa mental de CH-17 (116 nodos/179 aristas, mayor que el de CH-16)
se incrusta en el PDF sin ningún "Error 11 (driver return code)" ni ningún otro fallo de
`xdvipdfmx`. El fix de Ghostscript introducido en CH-16 sigue funcionando correctamente para un
diagrama todavía más grande — no se encontró ningún problema real que justificara modificarlo.

### 6.2 Corrida limpia final (repetida tres veces, incluyendo una ronda de pruebas negativas)

Comando (desde la raíz del repo, `dist/` borrado antes para forzar un build limpio):

```text
$ rm -rf dist && ./scripts/build-all
...
▶ validate-chapter book/chapters/17-idempotency-guard/chapter.md
validate-chapter: OK — secciones: 22/19, bloques pseudocode: 6, contratos introducidos: 1,
  componentes introducidos: 1
▶ validate-retrieval-set book/chapters/17-idempotency-guard/chapter.md
validate-retrieval-set: OK — guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2,
  interleavedQuestions: 2, flashcards: 5, calibrationPairs: 4
...
▶ build-book-ir → OK → dist/book-ir.json (capítulos: 18 / contratos: 27 / componentes: 15 /
  glosario: 98 / flashcards: 85)
▶ build-mind-map
  chapter-16.diagram: 109 nodo(s), 167 arista(s)
  chapter-17.diagram: 116 nodo(s), 179 arista(s) (7 nuevo(s) en este capítulo)
  full-book.diagram: 116 nodo(s), 179 arista(s)
▶ build-web → OK → dist/web/ — index.html + 2 páginas de frontmatter + 18 capítulos + mapa.html
▶ build-pdf → OK → dist/book.pdf (2299394-2299398 bytes, tamaño estable entre corridas)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
BookState persistido en dist/book-state.json
```

Exit code: `0` (verificado explícitamente tras `rm -rf dist && ./scripts/build-all`, repetido dos
veces de forma completa, y una vez más después de revertir las dos pruebas negativas de §8, con
conteos idénticos: 116 nodos/179 aristas, 27 contratos, 15 componentes, 18 capítulos, 433 páginas de
PDF).

**Nota operacional real durante la verificación**: la primera corrida de este capítulo coincidió,
en este entorno, con un proceso `build-all` residual de un intento anterior (`/tmp/ch17_build.log`)
que seguía en ejecución y que, al terminar, hizo `rm -rf dist` y regeneró `dist/` de nuevo por su
cuenta — produciendo una lectura transitoria inconsistente de `dist/book.pdf` (momentáneamente
ausente) mientras ambos procesos escribían al mismo directorio. Se esperó explícitamente a que ese
proceso terminara (confirmado con `ps aux`, sin procesos `xelatex`/`pandoc`/`build-all` activos) y se
re-verificó `dist/` en su estado final y estable antes de dar cualquier resultado por bueno — ningún
resultado de este capítulo se aceptó mientras un build seguía en curso.

## 7. Evidencia de verificación concreta

### 7.1 Mapa mental acumulativo (CH-17 > CH-16 > ... > CH-00)

`chapter-16.diagram`: 109 nodos / 167 aristas. `chapter-17.diagram`: **116 nodos / 179 aristas** (7
nuevos: el nodo `CHAPTER` de `CH-17`, `CMP-015`, `C-027`, y los cuatro conceptos de glosario nuevos
con nodo propio). Cumple el criterio del encargo (más nodos/aristas que CH-16: 116 > 109, 179 >
167). `full-book.diagram` coincide exactamente con el snapshot de CH-17 (el último), confirmando
acumulación real.

### 7.2 Web

- `dist/web/chapters/CH-17.html` existe, con SVG de mapa mental inline (`grep -c '<svg'` == 1).
- Anchors de entidad presentes: `id="CMP-015"` (1), `id="C-027"` (1).
- Navegación prev/next verificada en ambos sentidos: `CH-16.html` contiene `href="CH-17.html"`;
  `CH-17.html` contiene `href="CH-16.html"`; `CH-17.html` NO contiene ningún link hacia `CH-18.html`
  (`next_chapter: null`, correcto — verificado con `grep -c 'CH-18'` == 0).
- `<svg` aparece exactamente 1 vez en cada una de las 18 páginas de capítulo (CH-00..CH-17).
- Anchors de capítulos previos verificados intactos (1 aparición cada uno): CH-00 (`C-001`), CH-01
  (`CMP-001`), CH-08 (`CMP-008`), CH-14 (`CMP-012`), CH-15 (`CMP-013`), CH-16 (`CMP-014`) — sin
  cambios.
- `dist/web/index.html` lista los dieciocho capítulos.

### 7.3 PDF (`pypdf`)

- Build completo (CH-00..CH-17): **433 páginas** — más que las 405 páginas del build de 17
  capítulos citadas en el encargo.
- Texto extraído del PDF, verificado con `pypdf.PdfReader(...).extract_text()`:
  `"IdempotencyGuard"` → `True`, `"IdempotencyRecord"` → `True`, `"CMP-015"` → `True`, `"C-027"` →
  `True`, `"INV-11"` → `True`, `"IdempotencyRecordStatus"` → `True`.

### 7.4 Pruebas negativas (inyectadas y revertidas, una a la vez)

1. **`produces` inválido en la ficha de componente**: se agregó `C-999` (inexistente) a
   `CMP-015.produces` en `registry/components.yaml` → `validate-components` falló limpio con
   `exit 1` y el mensaje exacto `Componente CMP-015: produces referencia contrato inexistente
   "C-999"`. Revertido (`diff` contra el backup en `/tmp/components.yaml.ch17.bak` confirmó archivo
   idéntico; `validate-components` volvió a `OK (15 componente(s))`, `exit 0`).
2. **Nombre canónico en una guiding question**: se reescribió `GQ-CH17-01` para que dijera
   literalmente "¿Decide IdempotencyGuard...?" → `validate-retrieval-set` falló limpio con `exit 1`
   y el mensaje exacto `retrievalSet.guidingQuestions[GQ-CH17-01] contiene el nombre canónico
   "IdempotencyGuard", que este mismo capítulo introduce — las preguntas guía deben usar lenguaje de
   problema`. Revertido (`diff` contra el backup en `/tmp/ch17.md.ch17.bak` confirmó archivo
   idéntico; `validate-retrieval-set` volvió a `OK`, `exit 0`).
3. Tras revertir ambas inyecciones (`diff` confirmó archivos idénticos byte a byte), `rm -rf dist &&
   ./scripts/build-all` volvió a pasar limpio con los mismos conteos de nodos/aristas (116/179), de
   contratos/componentes (27/15), de capítulos (18) y de páginas de PDF (433) que antes de las
   inyecciones (exit 0).

### 7.5 CH-00..CH-16 no se rompieron

- `validate-chapter`/`validate-retrieval-set` de los diecisiete siguen en verde (ver §6, corrida
  completa de `build-all`).
- Los anchors de CH-00..CH-16 no cambiaron de contenido (ver §7.2).
- Solo se editó `next_chapter` en el frontmatter de CH-16 — su cuerpo y su `retrieval_set` quedaron
  intactos.
- `mapa.html` sigue mostrando el grafo acumulado completo con los dieciocho capítulos.
- `scripts/lib/render-diagram.js` no se modificó — el mapa mental acumulado, ahora más grande, sigue
  incrustándose en el PDF sin errores.

## 8. Definition of Done (restringido a este incremento)

- ✅ CH-17 completo: 22 secciones (0, 1-19, 20, 21), sin relleno — cada sección con contenido real.
- ✅ `registry/contracts.yaml` / `registry/components.yaml` / `registry/glossary.yaml` /
  `book/book.yaml` actualizados y validados (`validate-contracts` vía `validate-components`,
  `validate-components`).
- ✅ `RetrievalSet` completo con `interleavedQuestions = 2` conectando con CH-02 y CH-07.
- ✅ Pipeline completo (`build-all`) verde desde `dist/` limpio, para los 18 capítulos, verificado
  tres veces con conteos idénticos.
- ✅ Evidencia concreta: conteos de nodos/aristas del mapa mental (116/179 > 109/167), conteo de
  páginas de PDF (433 vs. 405 citadas en el encargo), texto extraído del PDF, anchors HTML, dos
  pruebas negativas con mensaje de error exacto y reversión confirmada con conteos idénticos.
- ✅ CH-00..CH-16 verificados intactos tras el cambio (salvo el campo de navegación autorizado en
  CH-16).
- ✅ Distinción explícita y documentada entre `IdempotencyGuard`/`IdempotencyRecord` y
  `ToolRuntime`/`PolicyEngine`/`CapabilityRegistry`/`ExecutionController` — deduplicación de una
  ejecución vs. ejecución del side effect vs. autorización vs. resolución de implementación vs.
  continuación operacional por presupuesto.
- ✅ Primera cita en prosa, en todo el libro, de `INV-11` (Article II original, declarado desde
  CH-00, nunca antes citado ni resuelto) — verificado con grep antes de escribir, no asumido.
- ✅ Corrección explícita del número de plano canónico del "Reliability Plane" (séptimo, no cuarto,
  en la lista de Amendment v1.1) — verificado con grep, documentado en la apertura del capítulo en
  vez de repetir silenciosamente la cifra del encargo.
- ✅ Nombre del componente (`IdempotencyGuard`) documentado explícitamente como síntesis de este
  libro — ningún texto de la Constitution lo nombra literalmente, a diferencia de
  `AdmissionController`/`AgentCommunicationGateway`/`CredentialBroker`.
- ✅ `scripts/lib/render-diagram.js` revisado (per instrucción del encargo) y confirmado funcional
  sin cambios para un mapa mental más grande que el que motivó el fix original de CH-16.
- ✅ Decisión de diseño explícita y documentada de por qué `IdempotencyRecordStatus` es un `ENUM` de
  dos valores y no un `Boolean`, y por qué no un tercer valor para "nunca visto" — la decisión de
  mayor efecto del capítulo, citada en la seccion 6/12/20.

## 9. Deuda intencional hacia el próximo capítulo (fuera de este alcance)

- **El cableado real `ToolRuntime ↔ IdempotencyGuard`**: ningún componente invoca todavía
  `checkIdempotency` antes de ejecutar un side effect, ni `recordIdempotentExecution` después.
- **La persistencia real de un `IdempotencyRecord` `PENDING` en el instante en que una ejecución
  arranca**: este capítulo solo demuestra la transición terminal (`COMPLETED`).
- **El mecanismo real que hace esperar a una ejecución concurrente bajo `PENDING`**: colas, locks,
  polling — ninguno modelado.
- **La generación real de una `idempotencyKey`**: asumida, no modelada.
- **La semántica real de "retry"** (la segunda mitad de `P-24`/`INV-E09`): pertenece a
  `ExecutionController` (CH-07), no se profundiza aquí.
- **Una política real de expiración/garbage collection** para `IdempotencyRecord` ya `COMPLETED`.
- **La ruta de "protección equivalente" que `INV-11` deja abierta como alternativa** (compensación
  después del hecho): este capítulo eligió, deliberadamente, solo la ruta de prevención.
- **Ausencia de evidencia de auditoría real** (`P-25`) para un `IdempotencyRecord` producido:
  señalado explícitamente, no silenciado.
- **Los cinco planos restantes de Amendment v1.1** (Execution Plane, Data & Context Plane, Control
  Plane, Observability & Governance Plane, Execution Fabric) y **la profundización del Reliability
  Plane más allá de este primer componente**: fuera de alcance.
- Reviewers plurales, evals y orquestación multi-agente propiamente dicha: explícitamente fuera de
  alcance de BH-v0.1.
- **El capítulo que profundice el Reliability Plane** (cableado real hacia `ToolRuntime`,
  persistencia atómica real), o que cubra el Execution Plane, o el Observability & Governance Plane
  (que resolvería, por fin, la deuda de `P-25`): candidato natural para el próximo incremento
  (CH-17 §19).
