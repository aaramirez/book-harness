# Plan / Registro de ejecución — Capítulo 16: CredentialBroker y la Resolución Segura de una Credencial

**Fecha:** 2026-09-14
**Estado:** ✅ Completado, sobre el estado dejado por `61b6787` (CH-00..CH-15 como los dieciséis
únicos capítulos reales; Agent Interoperability Plane, segundo plano de Amendment v1.1 cubierto por
el libro, con `AgentCommunicationGateway`, CMP-013).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-14-capitulo-15-agent-communication-gateway.md` (precedente inmediato: segundo componente
  de Amendment v1.1, patrón de ficha sin sección propia de Article III, `THROW` sobre un artefacto
  ya emitido en vez de un tercer contrato `Decision`)
- `2026-09-14-capitulo-14-admission-controller.md` (precedente del primer componente de Amendment
  v1.1, mismo patrón de `does_not_own` citando componentes ya registrados)
- `2026-09-14-capitulo-08-capability-registry.md` (origen de `CapabilityDescriptor`, C-018,
  `implementationRef` opaco — la pieza que este capítulo consume ya resuelta)
- `2026-09-13-capitulo-02-tool-runtime.md` (origen del hueco genuino que este capítulo cierra:
  `executeToolCall` nunca modeló cómo se autentica una ejecución real)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Amendment v1.1 completo — `P-16`..`P-30`,
  `INV-E01`..`INV-E14`, "Canonical Enterprise Planes")
- `reference/md/REGLAS_LIBRO_AGENT_HARNESS(1).md` §26 (estructura obligatoria de capítulo) y §31
  ("Amendment v0.5 — Reglas para arquitectura empresarial y comunicación")

---

## 1. Objetivo

Escribir el decimoséptimo capítulo real de contenido del libro ("¿Cómo construir un arnés?"), CH-16,
sobre `CredentialBroker` — el componente del "Capability & Integration Plane" de Amendment v1.1, el
tercero de los nueve planos canónicos que este libro cubre (el primero fue Ingress & Activation,
CH-14; el segundo, Agent Interoperability, CH-15). Verificar que el capítulo atraviesa todo el
pipeline (validadores + BookIR + Web + PDF + Mapa Mental) sin romper nada de lo que CH-00..CH-15 ya
tenían construido.

## 2. Alcance decidido (Paso 2 del encargo, ya cerrado antes de escribir)

Exactamente 1 componente + 1 contrato:

1. **Componente `CredentialBroker` (CMP-014)** — tercer componente de este registry que NO
   corresponde a ninguno de los once nombres del árbol de Article III; pertenece al "Capability &
   Integration Plane" de Amendment v1.1. `owns` (cita literal de `INV-E08`/`INV-E07`, más lectura de
   `P-22`): resolver, para una implementación de capability ya resuelta (`CapabilityDescriptor`,
   C-018, CH-08), la credencial que necesita para autenticarse contra el sistema externo real que
   envuelve — produciendo exclusivamente una `CredentialReference` opaca, nunca el valor real del
   secreto (`INV-E08` literal: "Credentials are resolved by a `CredentialBroker` and SHOULD NOT
   enter model context"); aplicar sobre ese secreto el gobierno de datos que `P-22` exige
   (clasificación, rotación/expiración); aislar credenciales por tenant (`INV-E07` literal:
   "Tenant data, memory, credentials, artifacts and audit records are isolated"); rechazar por
   defecto cuando el secreto no corresponde, no existe o ya venció. `does_not_own`: decidir si un
   `ToolCall` está autorizado a ejecutarse (`PolicyEngine`, CH-05), resolver qué implementación
   satisface una capability (`CapabilityRegistry`, CH-08 — `CredentialBroker` entra DESPUÉS),
   ejecutar el side effect en sí (`ToolRuntime`, CH-02), el mecanismo real de almacenamiento/rotación
   del secreto (Secret Store, infraestructura de borde), decidir continuación de turno (`AgentLoop`,
   CH-01).
2. **Contrato nuevo `CredentialReference` (C-026)** — la referencia opaca que exige `INV-E08`: `id`,
   `capability` (`CapabilityId`, referencia opaca al `CapabilityDescriptor`, C-018, sin modificarlo),
   `credentialName` (`Text`, nombre/scope del secreto), `classification`
   (`CredentialClassification`, ENUM nuevo de dos valores — materialización literal de `P-22`),
   `resolvedAt` (`Timestamp`) y `expiresAt` (`Optional<Timestamp>`, rotación/expiración). Ningún
   campo transporta jamás el valor real del secreto — decisión de diseño explícita y deliberada,
   documentada en el capítulo (seccion 6), no una omisión.
3. **Frontera con `ToolRuntime`/`CapabilityRegistry`/`PolicyEngine`**: no se editó
   `registry/components.yaml` en las entradas de `CMP-002`/`CMP-005`/`CMP-008`. El pseudocódigo de
   este capítulo (`resolveCredentialReference`) resuelve una `CredentialReference` de forma
   autónoma a partir de un `CapabilityDescriptor` de ejemplo. La prosa (seccion 9/18) deja explícito
   que "`ToolRuntime.executeToolCall` obtiene la credencial resuelta antes de invocar la
   implementación" es trabajo de un capítulo de integración futuro.
4. No se tocó `book/chapters/00-*` a `14-*`; de CH-15 solo se tocó `next_chapter: null → CH-16` en
   el frontmatter.
5. `book/book.yaml` agrega CH-16 después de CH-15; CH-16 frontmatter → `previous_chapter: CH-15`,
   `next_chapter: null`.
6. `retrieval_set` de CH-16 incluye 2 `interleavedQuestions`: una conectando con CH-08
   (`CapabilityRegistry`/`CapabilityDescriptor`, distinguiendo "qué implementación satisface la
   capability" de "qué credencial necesita esa implementación ya resuelta") y otra con CH-05
   (`PolicyEngine`, distinguiendo autorización de la acción de resolución de credencial).
   `guidingQuestions` en lenguaje de problema, sin usar "CredentialBroker"/"CredentialReference"
   literal (verificado con la prueba negativa de §8.2).

## 3. Decisiones de diseño centrales

### 3.1 Confirmación de los próximos ids libres (verificados, no asumidos)

Se leyó `registry/contracts.yaml` y `registry/components.yaml` completos antes de escribir. El
último contrato registrado era `C-025` (`DelegationGrant`, CH-15) — el próximo id libre es `C-026`.
El último componente registrado era `CMP-013` (`AgentCommunicationGateway`, CH-15) — el próximo id
libre es `CMP-014`. Verificado con grep que ningún nombre candidato (`CredentialBroker`,
`CredentialReference`, `CredentialClassification`) colisionaba ya con algo registrado.

### 3.2 Por qué se avanza al Capability & Integration Plane (cuarto plano canónico) en vez de
retroceder al Execution Plane (segundo)

El encargo pidió explícitamente el "Capability & Integration Plane" como "tercer plano canónico
cubierto" por el libro (no el segundo del orden canónico de Amendment v1.1, que sigue siendo el
Execution Plane, todavía sin cubrir). Se documentó esta decisión de forma explícita en la apertura
del capítulo y en seccion 1/19 — el Execution Plane completo queda, deliberadamente, como candidato
igualmente válido para un incremento futuro (seccion 18/19), mismo patrón que CH-15 ya estableció
para su propio salto de plano.

### 3.3 `capability: CapabilityId`, nunca `CapabilityDescriptor` embebido

Se evaluó embeber el `CapabilityDescriptor` completo dentro de `CredentialReference`. Se descartó:
una referencia por id (el mismo `CapabilityId` que ya vive dentro de `CapabilityDescriptor.
capability`) evita que esta estructura cargue una copia que podría quedar desactualizada respecto al
registro real — el mismo argumento que ya usó `DelegationGrant.delegatingRunId` como
`Optional<RunId>` en vez de un `AgentRun` embebido (CH-15 §6).

### 3.4 Por qué `CredentialReference` nunca tiene un campo con el valor del secreto — el hallazgo
real de este capítulo

Se evaluó, y se descartó de inmediato, cualquier variante que incluyera el secreto real dentro de
este contrato — ni siquiera cifrado, ni siquiera como campo opcional "solo para auditoría". Razón
estructural, no estilística: un contrato de este registry viaja por componentes, se serializa, puede
terminar dentro de un `payload` de `AgentEvent` o de cualquier estructura que un capítulo futuro
construya para dar contexto al modelo. Si `CredentialReference` transportara el secreto en cualquier
forma, cada componente que la reciba se convertiría, por diseño, en una superficie de fuga potencial
— la violación exacta que `INV-E08` prohíbe. Documentado explícitamente en el capítulo (seccion 6,
15, 20) como decisión de diseño deliberada, no una omisión — exactamente lo que pedía el encargo.

### 3.5 `CredentialClassification` como `ENUM` de dos valores, nunca un `Boolean isSensitive`

Se evaluó explícitamente un campo `Boolean`. Se descartó por el mismo argumento que ya descartó
`allowAll: Boolean` para `DelegationGrant.delegatedScope` en CH-15 §6: no todos los secretos cargan
el mismo riesgo, y un `Boolean` de dos estados colapsaría esa diferencia real a un solo bit. Se
adoptó `CredentialClassification` (`CONFIDENTIAL`/`RESTRICTED`) como la materialización mínima —
deliberadamente mínima, no el esquema completo de `P-22` (residencia, lineage, legal-hold quedan
fuera de alcance, ver seccion 18).

### 3.6 `expiresAt: Optional<Timestamp>`, no obligatorio como `DelegationGrant.expiresAt` (CH-15)

Se evaluó exigir siempre una fecha de vencimiento, siguiendo el precedente de `DelegationGrant`
(donde `P-21` exige literalmente "time-bounded" sin excepción). Se descartó: `P-22` no impone la
misma exigencia universal sobre todo dato gobernado — no todo secreto tiene, necesariamente, una
política de rotación explícita todavía modelada. Exigir `expiresAt` siempre habría inventado una
política de rotación que `P-22` nunca dijo que existiera universalmente.

### 3.7 Orden de verificación en `resolveCredentialReference`: pertenencia antes que existencia

Se decidió verificar `credentialBelongsToCapability` como primer chequeo, antes que `secretExists`.
Verificar primero la pertenencia a la capability evita una fuga de información por canal lateral: si
el orden fuera inverso, un llamador podría inferir, a partir de cuál de los dos errores recibe, si un
`credentialName` existe en el Secret Store en términos absolutos, incluso para una capability a la
que nunca debería pertenecer. Documentado explícitamente en la seccion 11 del capítulo.

### 3.8 Por qué `CredentialBroker` SÍ produce `AgentEvent`, a diferencia de CH-14/CH-15

A diferencia de `AdmissionController` (CH-14, el run todavía no existe) y `AgentCommunicationGateway`
(CH-15, `AgentCommunicationMessage` no tiene `sessionId`), cuando `CredentialBroker` actúa, el
`AgentRun` que necesita la credencial ya existe con `ExecutionContext` completo
(`runId`/`sessionId`/`traceId`) — la misma situación que `CapabilityRegistry` (CH-08). Se decidió
que `resolveCredentialReference` emita `AgentEvent` (`CREDENTIAL_RESOLVED`/
`CREDENTIAL_RESOLUTION_FAILED`) en cada rama — documentado en el capítulo como un contraste
explícito con los dos componentes anteriores de Amendment v1.1, y como evidencia de que emitir esta
telemetría nunca compromete `INV-E08` (el `payload` es siempre la referencia opaca o el
`HarnessError`, nunca el secreto).

### 3.9 `CREDENTIAL` como nueva categoría de `ErrorCategory`, no `VALIDATION`

Se evaluó reutilizar `VALIDATION` (CH-02/CH-08) para `CREDENTIAL_CAPABILITY_MISMATCH`, dado el
parecido superficial con un fallo de forma/esquema. Se descartó: `VALIDATION` pertenece, en
exclusiva, a fallos sobre la forma de una intención de acción ya resuelta (`ToolCall`) — una
pregunta sobre argumentos y schemas, nunca sobre qué secreto autentica un sistema. Se agregó
`CREDENTIAL` como decimocuarto valor de `ErrorCategory` — el quinto capítulo en extender ese `ENUM`
desde CH-00 (después de `HUMAN_INTERACTION` CH-06, `ADMISSION` CH-14, `DELEGATION` CH-15).

## 4. Archivos creados

- `book/chapters/16-credential-broker/chapter.md` — capítulo completo (22 secciones: 0, 1-19, 20,
  21).
- `planes/2026-09-14-capitulo-16-credential-broker.md` — este registro.

## 5. Archivos modificados

- `registry/contracts.yaml` — agrega `C-026 CredentialReference`, con comentario documentando la
  decisión de diseño (ningún campo transporta el secreto real).
- `registry/components.yaml` — agrega `CMP-014 CredentialBroker`; actualiza el comentario de
  historial.
- `registry/glossary.yaml` — agrega `CredentialBroker` (component), `CredentialReference`
  (contract), `Secret`, `Credential Classification`, `Credential Rotation`, `Secret Store`, `Tenant
  Isolation of Credentials` (kind: concept).
- `book/book.yaml` — agrega la entrada `CH-16`.
- `book/chapters/15-agent-communication-gateway/chapter.md` — únicamente `next_chapter: null` →
  `CH-16` en el frontmatter (sin tocar ninguna otra sección).
- `scripts/lib/render-diagram.js` — **fix de infraestructura compartida, no de contenido** (ver
  seccion 6.1): normaliza con Ghostscript (`pdfwrite`, `CompatibilityLevel=1.4`) cada PDF que `dot
  -Tpdf` produce antes de que `build-pdf` lo incruste, porque el `xdvipdfmx` instalado en este
  entorno rompía con "Error 11 (driver return code)" al incrustar el diagrama de mapa mental de este
  capítulo (109 nodos/167 aristas, el primero en cruzar ese umbral) — sin afectar el formato SVG
  usado por `build-web`. Best-effort: si `gs` no está disponible, conserva el comportamiento previo
  en vez de romper el build.

## 6. Resultado real del pipeline

### 6.1 Hallazgo real durante la verificación: `xdvipdfmx` rompía al incrustar el mapa mental de CH-16

La primera corrida de `rm -rf dist && ./scripts/build-all` con CH-16 ya escrito y registrado falló
en la etapa `build-pdf`, con `pandoc: Error producing PDF` / `Error 11 (driver return code)
generating output`, **después** de tipografiar exitosamente las 405 páginas de contenido (sin ningún
error real de TeX — solo warnings preexistentes de "Missing character... U+2192", ya presentes en
builds anteriores que sí pasaban). Se diagnosticó de forma metódica, sin adivinar:

1. Se confirmó, revirtiendo temporalmente a `61b6787` (`git stash`) y reconstruyendo, que el build de
   16 capítulos (sin CH-16) seguía pasando limpio en este mismo entorno — descartando una
   degradación general del entorno.
2. Se aisló el problema a la incrustación de imágenes: un documento LaTeX mínimo que solo incrusta
   `dist/.build/mindmap/chapter-16.pdf` (el mapa mental de este capítulo, generado por `dot -Tpdf`,
   PDF 1.7) reproducía el mismo "Error 11" de forma aislada.
3. Se confirmó la causa raíz: reescribir ese mismo PDF con Ghostscript
   (`gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4`) antes de incrustarlo elimina el error —
   `xdvipdfmx` (TeX Live 2022) no puede incrustar, de forma confiable, el PDF que `dot -Tpdf` produce
   una vez el diagrama cruza cierto tamaño/complejidad (el mapa mental de CH-16, 109 nodos/167
   aristas, fue el primero en cruzar ese umbral — el de CH-15, 101/155, todavía no lo cruzaba).
4. Se aplicó el fix mínimo en `scripts/lib/render-diagram.js` (ver seccion 5): post-procesar con
   Ghostscript cada PDF que `renderDiagram` produce, exclusivamente en la rama `format === 'pdf'`
   (el formato SVG de `build-web` no se toca). Best-effort con fallback silencioso si `gs` no está
   disponible.
5. Se reconstruyó todo desde `dist/` limpio y el pipeline completo pasó, con conteos idénticos en
   reconstrucciones repetidas (ver §7).

Esto es infraestructura compartida (`scripts/lib/render-diagram.js`), no contenido de ningún
capítulo — corregido porque el encargo exige un pipeline verde real para los 17 capítulos, y este
umbral se habría vuelto a cruzar, de todos modos, en cualquier capítulo futuro cuyo mapa mental
acumulado siguiera creciendo.

### 6.2 Corrida limpia final

Comando (desde la raíz del repo, `dist/` borrado antes para forzar un build limpio):

```text
$ rm -rf dist && ./scripts/build-all
...
▶ validate-chapter book/chapters/16-credential-broker/chapter.md
validate-chapter: OK — secciones: 22/19, bloques pseudocode: 6, contratos introducidos: 1,
  componentes introducidos: 1
▶ validate-retrieval-set book/chapters/16-credential-broker/chapter.md
validate-retrieval-set: OK — guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2,
  interleavedQuestions: 2, flashcards: 5, calibrationPairs: 4
...
▶ build-book-ir → OK → dist/book-ir.json (capítulos: 17 / contratos: 26 / componentes: 14 /
  glosario: 92 / flashcards: 80)
▶ build-mind-map
  chapter-15.diagram: 101 nodo(s), 155 arista(s)
  chapter-16.diagram: 109 nodo(s), 167 arista(s) (8 nuevo(s) en este capítulo)
  full-book.diagram: 109 nodo(s), 167 arista(s)
▶ build-web → OK → dist/web/ — index.html + 2 páginas de frontmatter + 17 capítulos + mapa.html
▶ build-pdf → OK → dist/book.pdf (2140040-2140041 bytes, tamaño estable entre corridas)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
```

Exit code: `0` (verificado explícitamente tras `rm -rf dist && ./scripts/build-all`, repetido tres
veces de forma consecutiva con `build-pdf` solo, y de nuevo tras revertir las dos pruebas negativas
de §8, con conteos idénticos: 109 nodos/167 aristas, 26 contratos, 14 componentes, 17 capítulos, 405
páginas de PDF).

## 7. Evidencia de verificación concreta

### 7.1 Mapa mental acumulativo (CH-16 > CH-15 > ... > CH-00)

`chapter-15.diagram`: 101 nodos / 155 aristas. `chapter-16.diagram`: **109 nodos / 167 aristas** (8
nuevos: el nodo `CHAPTER` de `CH-16`, `CMP-014`, `C-026`, y los cinco conceptos de glosario nuevos
con nodo propio). Cumple el criterio del encargo (más nodos/aristas que CH-15: 109 > 101, 167 > 155).
`full-book.diagram` coincide exactamente con el snapshot de CH-16 (el último), confirmando
acumulación real.

### 7.2 Web

- `dist/web/chapters/CH-16.html` existe, con SVG de mapa mental inline (`grep -c '<svg'` == 1).
- Anchors de entidad presentes: `id="CMP-014"` (1), `id="C-026"` (1).
- Navegación prev/next verificada en ambos sentidos: `CH-15.html` contiene `href="CH-16.html"`;
  `CH-16.html` contiene `href="CH-15.html"`; `CH-16.html` NO contiene `href="...CH-17.html"`
  (`next_chapter: null`, correcto).
- Anchors de capítulos previos verificados intactos (1 aparición cada uno): CH-00 (`C-001`), CH-01
  (`CMP-001`), CH-08 (`CMP-008`), CH-14 (`CMP-012`), CH-15 (`CMP-013`) — sin cambios.
- `<svg` aparece exactamente 1 vez en cada una de las 17 páginas de capítulo (CH-00..CH-16).
- `dist/web/index.html` lista los diecisiete capítulos.

### 7.3 PDF (`pypdf`)

- Build completo (CH-00..CH-16): **405 páginas** — más que las 379 páginas del build de 16
  capítulos citadas en el encargo.
- Texto extraído del PDF, verificado con `pypdf.PdfReader(...).extract_text()`:
  `"CredentialBroker"` → `True`, `"CredentialReference"` → `True`, `"CMP-014"` → `True`, `"C-026"` →
  `True`.

### 7.4 Pruebas negativas (inyectadas y revertidas, una a la vez)

1. **`produces` inválido en la ficha de componente**: se agregó `C-999` (inexistente) a
   `CMP-014.produces` en `registry/components.yaml` → `validate-components` falló limpio con
   `exit 1` y el mensaje exacto `Componente CMP-014: produces referencia contrato inexistente
   "C-999"`. Revertido (`diff` contra el backup en `/tmp/components.yaml.ch16.bak` confirmó archivo
   idéntico; `validate-components` volvió a `OK (14 componente(s))`, `exit 0`).
2. **Nombre canónico en una guiding question**: se reescribió `GQ-CH16-01` para que dijera
   literalmente "¿Decide CredentialBroker...?" → `validate-retrieval-set` falló limpio con `exit 1`
   y el mensaje exacto `retrievalSet.guidingQuestions[GQ-CH16-01] contiene el nombre canónico
   "CredentialBroker", que este mismo capítulo introduce — las preguntas guía deben usar lenguaje de
   problema`. Revertido (`diff` contra el backup en `/tmp/ch16.md.ch16.bak` confirmó archivo
   idéntico; `validate-retrieval-set` volvió a `OK`, `exit 0`).
3. Tras revertir ambas inyecciones (`diff` confirmó archivos idénticos byte a byte), `rm -rf dist &&
   ./scripts/build-all` volvió a pasar limpio con los mismos conteos de nodos/aristas (109/167), de
   contratos/componentes (26/14), de capítulos (17) y de páginas de PDF (405) que antes de las
   inyecciones (exit 0).

### 7.5 CH-00..CH-15 no se rompieron

- `validate-chapter`/`validate-retrieval-set` de los dieciséis siguen en verde (ver §6, corrida
  completa de `build-all`).
- Los anchors de CH-00..CH-15 no cambiaron de contenido (ver §7.2).
- Solo se editó `next_chapter` en el frontmatter de CH-15 — su cuerpo y su `retrieval_set` quedaron
  intactos.
- `mapa.html` sigue mostrando el grafo acumulado completo con los diecisiete capítulos.
- El fix de `scripts/lib/render-diagram.js` (§6.1) se verificó explícitamente que no cambia el
  formato SVG que `build-web` consume (solo post-procesa la rama `format === 'pdf'`) — las 17
  páginas web siguen mostrando su SVG inline sin cambios.

## 8. Definition of Done (restringido a este incremento)

- ✅ CH-16 completo: 22 secciones (0, 1-19, 20, 21), sin relleno — cada sección con contenido real.
- ✅ `registry/contracts.yaml` / `registry/components.yaml` / `registry/glossary.yaml` /
  `book/book.yaml` actualizados y validados (`validate-contracts`, `validate-components`).
- ✅ `RetrievalSet` completo con `interleavedQuestions = 2` conectando con CH-08 y CH-05.
- ✅ Pipeline completo (`build-all`) verde desde `dist/` limpio, para los 17 capítulos.
- ✅ Evidencia concreta: conteos de nodos/aristas del mapa mental (109/167 > 101/155), conteo de
  páginas de PDF (405 vs. 379 citadas en el encargo), texto extraído del PDF, anchors HTML, dos
  pruebas negativas con mensaje de error exacto y reversión confirmada con conteos idénticos.
- ✅ CH-00..CH-15 verificados intactos tras el cambio (salvo el campo de navegación autorizado en
  CH-15).
- ✅ Distinción explícita y documentada entre `CredentialBroker`/`CredentialReference` y
  `CapabilityRegistry`/`CapabilityDescriptor` (CH-08) y `PolicyEngine` (CH-05) — resolución de
  credencial vs. resolución de implementación vs. autorización de la acción.
- ✅ Primera cita literal con código real de `INV-E08`/`INV-E07`/`P-22` (Amendment v1.1) — `P-22`
  había sido citado solo en prosa por CH-10/CH-11, nunca materializado con código antes de este
  capítulo.
- ✅ Hallazgo real documentado (encontrado durante la verificación, no anticipado literalmente en el
  encargo): `xdvipdfmx` (TeX Live 2022 instalado en este entorno) no puede incrustar de forma
  confiable el PDF vectorial que `dot -Tpdf` produce una vez el mapa mental acumulado cruza cierto
  umbral de tamaño/complejidad — corregido con una normalización vía Ghostscript en
  `scripts/lib/render-diagram.js`, aplicable a cualquier capítulo futuro que siga haciendo crecer el
  mapa mental.
- ✅ Decisión de diseño explícita y documentada de que `CredentialReference` nunca transporte el
  valor real del secreto — la decisión de mayor efecto del capítulo, citada en la seccion 6/15/20.

## 9. Deuda intencional hacia el próximo capítulo (fuera de este alcance)

- **El cableado real `CapabilityRegistry → CredentialBroker → ToolRuntime → implementación`**:
  ningún componente invoca todavía `resolveCredentialReference` seguido de una entrega real de la
  `CredentialReference` a la implementación.
- **El Secret Store real** (vault, KMS, secret manager): infraestructura de borde, no modelada.
- **El mecanismo real de rotación automática** detrás de `CredentialReference.expiresAt`.
- **El aislamiento real por tenant** (`INV-E07`): citado literalmente, sin mecanismo de enforcement
  modelado.
- **Un esquema de clasificación más rico** que `CredentialClassification` de dos valores —
  residencia, retención con ventana explícita, lineage, encriptación, legal-hold — pertenece, con
  mayor propiedad, a un capítulo futuro del "Data & Context Plane" (quinto plano canónico).
- **La emisión real de un secreto hacia un Secret Store en primer lugar**: asumido, no modelado.
- **Ausencia de evidencia de auditoría real** (`P-25`) para una `CredentialReference` resuelta:
  señalado explícitamente, no silenciado.
- **El Execution Plane completo** (segundo plano canónico, todavía sin cubrir) y **los seis planos
  restantes** de Amendment v1.1: fuera de alcance.
- Reviewers plurales, evals y orquestación multi-agente propiamente dicha: explícitamente fuera de
  alcance de BH-v0.1.
- **El capítulo que profundice el Capability & Integration Plane** (Secret Store real, cableado
  real hacia `ToolRuntime`), o que cubra el Execution Plane, o que avance hacia cualquiera de los
  cinco planos restantes: candidato natural para el próximo incremento (CH-16 §19).
