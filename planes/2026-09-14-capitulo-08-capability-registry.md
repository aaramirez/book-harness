# Plan / Registro de ejecución — Capítulo 8: CapabilityRegistry y la Resolución Real de una Tool Call

**Fecha:** 2026-09-14
**Estado:** ✅ Completado — ejecutado en una sola sesión, sobre el estado dejado por `2106937` (CH-00
..CH-07 como los ocho únicos capítulos reales; `CapabilityRegistry` todavía citado treinta veces a
lo largo de esos ocho capítulos —veintiuna de ellas concentradas entre CH-02, doce, y CH-03, nueve—
siempre como "todavía no introducido"; `ToolCall.capability` (C-008, CH-02) exigiendo un
`CapabilityId` ya resuelto sin que ningún componente real lo produjera; `ModelResponse.
proposedToolCall` (C-007, CH-03) transportando una `RawToolCallProposal` deliberadamente cruda).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-13-capitulo-02-tool-runtime.md` y `2026-09-13-capitulo-03-model-gateway.md` (los dos
  precedentes directos que dejaron la deuda que este capítulo resuelve)
- `2026-09-14-capitulo-05-policy-engine.md` .. `2026-09-14-capitulo-07-execution-controller.md`
  (mismo formato, misma disciplina de `owns`/`does_not_own`)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Article III "CapabilityRegistry", Article IV
  Decision Ownership — fila "What implementation satisfies a requested capability?", Article VI
  Execution Constitution — pipeline "Resolve Capability → Validate Schema", Article II
  INV-03/INV-04/INV-05/INV-18/INV-19/INV-20, Article I P-03/P-13, Amendment v1.1 P-26 "Capabilities
  have governed lifecycles")

---

## 1. Objetivo

Escribir el noveno capítulo real de contenido del libro ("¿Cómo construir un arnés?"), CH-08, sobre
`CapabilityRegistry` — el componente más citado como deuda pendiente en todo el libro hasta ahora
(treinta menciones en ocho capítulos, veintiuna de ellas repartidas entre CH-02 y CH-03) — y el
primer capítulo que, por fin, resuelve de verdad una propuesta cruda de tool call
(`RawToolCallProposal`, CH-03) hacia un contrato ya existente de otro capítulo (`ToolCall`, C-008,
CH-02) mediante una resolución real (una búsqueda contra un registro), no mediante una señal
booleana asumida — y verificar que atraviesa todo el pipeline (validadores + BookIR + Web + PDF +
Mapa Mental) sin romper nada de lo que CH-00..CH-07 ya tenían construido.

## 2. Alcance decidido (Paso 2 del encargo, ya cerrado antes de escribir)

Exactamente 1 componente + 1 contrato, con la particularidad de que este capítulo, por primera vez,
produce de verdad un contrato ya existente de otro capítulo:

1. **Componente `CapabilityRegistry` (CMP-008)** — octavo componente de runtime del libro. `owns`
   parte de la cita literal, deliberadamente terse, de Article III ("desacoplar la intención de una
   capacidad de su implementación concreta") y se expande con grounding textual en cómo CH-02
   («registro y resolución de qué implementación satisface una capability solicitada») y CH-03
   («resolver `proposedToolCall` hacia un `ToolCall` real... requiere `CapabilityRegistry`») ya la
   citaron: registrar el descriptor de una capability, resolver su nombre contra ese registro,
   validar sus argumentos crudos contra el schema declarado, y desacoplar intención de
   implementación. `does_not_own` excluye cuatro decisiones vecinas: ejecutar la capability ya
   resuelta (`ToolRuntime`, ya existente — frontera que CH-02 ya había marcado desde el lado
   opuesto), invocar al modelo o interpretar su propuesta cruda (`ModelGateway`, ya existente —
   frontera que CH-03 ya había marcado desde el lado opuesto), evaluar policy/autorización
   (`PolicyEngine`, ya existente — distinción cuidadosa entre "¿existe e implementa correctamente
   esta capability?" y "¿está permitido usarla ahora?"), y decidir continuación de turno
   (`AgentLoop`, ya existente). `consumes`: `C-004 ExecutionContext`, `C-007 ModelResponse` (de
   donde viene la propuesta cruda); `produces`: `C-008 ToolCall` (primera vez que este contrato se
   produce con una resolución real, no como parámetro ya armado), `C-010 AgentEvent`,
   `C-011 HarnessError`, `C-018 CapabilityDescriptor` (el contrato nuevo).
2. **Contrato nuevo `CapabilityDescriptor` (C-018)** — el descriptor registrado de una capability:
   `capability` (`CapabilityId`, el identificador ya resuelto), `name` (`Text`, el nombre canónico
   contra el que se compara `capabilityName`), `version` (`Text`, explícita — grounding en P-26
   "Capabilities have governed lifecycles", Amendment v1.1, no en Article XI como sugería el
   encargo original: Article XI/EVO-08 habla de ADRs para breaking changes de contratos, no de
   versionado explícito de capabilities; P-26 es la cita literal correcta), `inputSchema` (`Value`,
   contra el que se valida `rawArguments`, sin definir un lenguaje de schema propio) e
   `implementationRef` (`Text`, una referencia opaca a la implementación concreta, deliberadamente
   sin modelar su detalle — Article III distingue "intención" de "implementación concreta"; modelar
   el detalle cruzaría esa línea).
3. **El momento central del capítulo — resolución real**: `resolveToolCall` (§11) toma una
   `RawToolCallProposal` (`capabilityName`, `rawArguments`) y una lista de `CapabilityDescriptor` ya
   registrados, ejecuta una búsqueda real (`FOR EACH candidate IN registeredCapabilities ... IF
   candidate.name == proposal.capabilityName`) — no una señal booleana asumida como
   `capabilityResolved` en CH-02 — valida `rawArguments` contra el schema (mediante una señal
   asumida, `argumentsMatchSchema`, ver §3 de este plan) y produce un `ToolCall` (C-008) real,
   tomando `capability` directamente del descriptor resuelto. `resolveModelProposedToolCall` es la
   demostración de integración que toma un `ModelResponse` (CH-03) completo y delega hacia
   `resolveToolCall`. Un fallo (capability inexistente, argumentos inválidos) se categoriza con
   `HarnessError` (C-011) reutilizando exactamente los mismos códigos y categoría (`VALIDATION`,
   `CAPABILITY_NOT_FOUND`/`TOOL_INPUT_SCHEMA_MISMATCH`) que `ToolRuntime` (CH-02) ya había declarado
   para las mismas señales, entonces asumidas — se evaluó explícitamente introducir una categoría
   `CAPABILITY` nueva y se descartó (ver §3 de este plan).
4. **Frontera con `ToolRuntime`/`ModelGateway`**: no se editó `registry/components.yaml` en las
   entradas de `CMP-002`/`CMP-003` (mismo precedente que CH-02..CH-07: no tocar retroactivamente
   componentes previos). El pseudocódigo de este capítulo es autónomo: toma un `ModelResponse` de
   ejemplo y produce un `ToolCall` de ejemplo — no requiere que `ModelGateway`/`ToolRuntime` cambien
   su código ya publicado. La sección 18 documenta explícitamente que el pipeline completo
   `AgentLoop → ModelGateway → CapabilityRegistry → PolicyEngine → ToolRuntime` como un solo flujo
   sigue siendo trabajo de un capítulo de integración futuro.
5. No se tocó `book/chapters/00-*` a `06-*`; de CH-07 solo se tocó `next_chapter: null → CH-08` en
   el frontmatter.
6. `book/book.yaml` agrega CH-08 después de CH-07; CH-08 frontmatter → `previous_chapter: CH-07`,
   `next_chapter: null`.
7. `retrieval_set` de CH-08 incluye 2 `interleavedQuestions`: una conectando con CH-02
   (`ToolRuntime`/`ToolCall`, el `does_not_own` que CH-02 ya había declarado) y otra con CH-03
   (`ModelGateway`/`ModelResponse`, la propuesta cruda que este capítulo resuelve) — la conexión más
   rica del libro hasta ahora, dos capítulos distintos convergiendo en uno. `guidingQuestions` en
   lenguaje de problema, sin usar "CapabilityRegistry"/"CapabilityDescriptor" literal (verificado
   con la prueba negativa de §8.4).

## 3. Decisión de diseño central: cómo modelar la resolución `RawToolCallProposal → ToolCall`

Como en CH-02..CH-07, no existía código previo que copiar — el diseño se ancló directamente en
Article III (cita literal terse, expandida con grounding en CH-02/CH-03), Article IV (la fila
"What implementation satisfies a requested capability?"), Article VI (el pipeline `Tool Intent →
Resolve Capability → Validate Schema → ...`, cuyos dos primeros pasos después de `Tool Intent` son
exactamente el tramo que este capítulo materializa) e INV-03/INV-04/INV-05/INV-18/INV-19/INV-20.

**Problema de diseño 1 — la resolución debe ser código real, no una señal asumida.** El punto
diferenciador de todo el capítulo: CH-02 modeló `capabilityResolved: Boolean` como señal de entrada
asumida; CH-03 dejó `capabilityName: Text` como texto libre sin resolver. Este capítulo no podía
repetir el mismo patrón (una tercera señal asumida) sin fallar en su propósito central. Se adoptó
`registeredCapabilities: List<CapabilityDescriptor>` como la señal asumida **legítima** (el
mecanismo de alta/registro de capabilities queda fuera de alcance, igual que en cada capítulo
anterior), pero la **resolución en sí** —comparar `capabilityName` contra `candidate.name` mediante
un `FOR EACH` real— se escribió como pseudocódigo ejecutable de verdad, no como un booleano de
entrada. Esta es la línea exacta que separa "qué capabilities existen" (fuera de alcance, como en
todo capítulo anterior) de "cómo se resuelve un nombre contra las que existen" (el propósito de este
capítulo, resuelto con código real).

**Problema de diseño 2 — qué permanece como señal asumida.** Se evaluó también modelar el algoritmo
de validación de esquemas (comparar `rawArguments` campo por campo contra `inputSchema`) con código
real. Se descartó: eso exigiría definir un lenguaje de schema propio (un motor de validación
completo), muy por fuera del alcance de 1 componente + 1 contrato decidido para este capítulo. Se
adoptó `argumentsMatchSchema: Boolean` como señal asumida — mismo patrón exacto que `inputValid` en
CH-02 §11 — documentando explícitamente en §5/§11/§18 que la diferencia respecto a CH-02 es que
ahora existe un campo real (`CapabilityDescriptor.inputSchema`) contra el cual ese algoritmo, cuando
exista, compararía.

**Problema de diseño 3 — reutilizar los códigos de error de CH-02, no inventar una categoría
nueva.** El encargo pedía evaluar explícitamente si `ErrorCategory` (con sus diez valores desde
CH-00) alcanzaba, o si hacía falta una categoría `CAPABILITY` nueva. Se concluyó que `VALIDATION`
alcanza: un `capabilityName` inexistente o unos `rawArguments` mal formados son, ambos, fallos de
validación de la *entrada*, no fallos de la *ejecución* (que sería `TOOL`, ya reservado para cuando
una capability ya resuelta falla al ejecutarse, CH-02). Se reutilizaron, deliberadamente, los
mismos códigos exactos que CH-02 ya había declarado (`CAPABILITY_NOT_FOUND`,
`TOOL_INPUT_SCHEMA_MISMATCH`) — este capítulo es, literalmente, la primera vez que un componente
real produce esos dos códigos en vez de asumirlos como señal de entrada.

**Problema de diseño 4 — el campo `version` y su grounding constitucional correcto.** El encargo
sugería anclar el campo de versión en "Article XI de evolución". Al leer Article XI completo
(EVO-01..EVO-10), se determinó que esas reglas hablan de *breaking changes de contratos* (ADRs,
`modified_by`) — no de que una *capability* declare una versión explícita. El grounding correcto,
verificado por búsqueda textual en toda la Constitution, es **P-26** ("Capabilities have governed
lifecycles", Amendment v1.1: "Tools/capabilities MUST support explicit versions, compatibility
policy, rollout, deprecation and retirement"). Se adoptó `CapabilityDescriptor.version: Text` como
la materialización mínima de ese principio — documentando explícitamente, en §5/§6/§18, que el
resto de lo que P-26 exige (compatibility policy, rollout, deprecation, retirement) permanece fuera
de alcance de BH-v0.1.

**Problema de diseño 5 — `implementationRef` como referencia opaca, nunca la implementación
misma.** El encargo lo pedía explícitamente: "una referencia, no el código de la implementación
misma". Se adoptó `implementationRef: Text` — deliberadamente sin estructura, sin URL tipada, sin
ningún STRUCT que modele "qué es" esa implementación. Modelar ese detalle cruzaría exactamente la
línea que Article III traza entre "la intención de una capacidad" y "su implementación concreta".

**Problema de diseño 6 — el nombre del contrato: `CapabilityDescriptor`, no `Capability`.** Se
evaluó nombrar el contrato simplemente `Capability`, pero ese nombre ya es un término de glosario
desde CH-02 (la abstracción conceptual, Article III). `CapabilityDescriptor` distingue el concepto
(`Capability`, ya existente) del registro de datos concreto que lo representa — la misma disciplina
de nombres que ya distingue "Tool Call" (concepto) de `ToolCall` (contrato, C-008).

## 4. Otras decisiones de diseño tomadas durante la ejecución

### 4.1 Dos valores nuevos de `AgentEventType` (`CAPABILITY_RESOLVED`/`CAPABILITY_RESOLUTION_FAILED`), un par, no uno solo

A diferencia de `PolicyEngine`/`ExecutionController` (CH-05/CH-07, un solo valor porque su
evaluación "nunca falla" en el sentido operacional), la resolución de una capacidad sí puede fallar
de verdad (capability inexistente, argumentos inválidos) — mismo patrón que `ToolRuntime`/
`ModelGateway`/`ContextEngine` (CH-02/CH-03/CH-04, un par éxito/fallo). El único caso que interrumpe
la función sin emitir evento (`RESOLUTION_REQUESTED_WITHOUT_PROPOSAL`) es una violación de
precondición de invocación, no un resultado legítimo de la resolución — mismo patrón que
`TURN_ON_TERMINAL_STATE` (CH-01) y `EXECUTION_EVALUATION_ON_TERMINAL_STATE` (CH-07).

### 4.2 El campo `capability` de `ToolCall` se toma del descriptor resuelto, nunca del texto libre del modelo

`resolveToolCall` construye `ToolCall.capability = descriptor.capability` — nunca
`proposal.capabilityName` directamente. Esta es la materialización literal de INV-03: el
`capabilityName` que el modelo propuso es solo la clave de búsqueda; el valor que efectivamente
queda grabado en el `ToolCall` proviene enteramente del registro que el harness controla, no del
texto que el modelo produjo.

### 4.3 Uso legítimo del mecanismo de whitelisting de `validate-chapter` para `RawToolCallProposal`

`RawToolCallProposal` es un `STRUCT` embebido dentro de `ModelResponse` (C-007, CH-03), sin
contrato `C-XXX` propio — no está en `registry/contracts.yaml`, así que no está automáticamente
disponible para el pseudocódigo de un capítulo distinto al que lo introdujo. Se usó, de forma
legítima (no como un truco), el mecanismo que `scripts/validate-chapter` ya expone para esto: una
tabla markdown `| \`RawToolCallProposal\` | ... |` en la sección 6 ("Identificadores y tipos
heredados") — el mismo patrón que el propio comentario del validador anticipa ("p.ej. la tabla de
identificadores fundamentales de la sección 'New Data Structures'"). Esta es la primera vez que el
libro necesita este mecanismo, porque es el primer capítulo que consume, en su propio pseudocódigo,
un tipo embebido introducido por un capítulo distinto.

### 4.4 `CapabilityRegistry.dependencies: []`

Igual que CH-01..CH-07: no depende de ningún otro componente registrado. La relación real
(`ModelGateway` produciría el `ModelResponse` de entrada; `PolicyEngine`/`ToolRuntime` consumirían
el `ToolCall` de salida; `AgentLoop` invocaría la resolución dentro de un turno) es la inversa de un
`dependency` en el sentido del registry, y ese cableado pertenece a un capítulo de integración
futuro — `registry/components.yaml` de `CMP-001`/`CMP-002`/`CMP-003` no se modifica en este
capítulo.

## 5. Archivos creados

- `book/chapters/08-capability-registry/chapter.md` — capítulo completo (22 secciones: 0, 1-19, 20,
  21).
- `planes/2026-09-14-capitulo-08-capability-registry.md` — este registro.

## 6. Archivos modificados

- `registry/contracts.yaml` — agrega `C-018 CapabilityDescriptor`; actualiza `used_by` de
  `C-004`/`C-007`/`C-008`/`C-010`/`C-011` (agrega `CMP-008` a cada uno); agrega comentario
  documentando la decisión de diseño.
- `registry/components.yaml` — agrega `CMP-008 CapabilityRegistry`; actualiza el comentario de
  historial.
- `registry/glossary.yaml` — agrega `CapabilityRegistry` (kind: component), `Capability Descriptor`
  (kind: contract), `Capability Resolution`, `Capability Versioning` (kind: concept).
- `book/book.yaml` — agrega la entrada `CH-08`.
- `book/chapters/07-execution-controller/chapter.md` — únicamente `next_chapter: null` → `CH-08` en
  el frontmatter (sin tocar ninguna otra sección ni la ficha de `CMP-007`).

## 7. Resultado real del pipeline

Comando (desde la raíz del repo, `dist/` borrado antes para forzar un build limpio):

```text
$ rm -rf dist && ./scripts/build-all
...
▶ validate-chapter CH-08       → OK — secciones: 22/19, bloques pseudocode: 5, contratos: 1,
  componentes: 1
▶ validate-retrieval-set CH-08 → OK — guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2,
  interleavedQuestions: 2, flashcards: 5, calibrationPairs: 4
...
▶ build-book-ir  → OK → dist/book-ir.json (capítulos: 9 / contratos: 18 / componentes: 8 /
  glosario: 51 / flashcards: 40)
▶ build-mind-map
  chapter-07.diagram: 55 nodo(s), 89 arista(s)
  chapter-08.diagram: 60 nodo(s), 99 arista(s) (5 nuevo(s) en este capítulo)
  full-book.diagram: 60 nodo(s), 99 arista(s)
▶ build-web → OK → dist/web/ — index.html + 2 páginas de frontmatter + 9 capítulos + mapa.html
▶ build-pdf → OK → dist/book.pdf (1043266 bytes)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
```

Exit code: `0` (verificado explícitamente con `echo $?` tras `rm -rf dist && ./scripts/build-all`,
y de nuevo tras un segundo `rm -rf dist && ./scripts/build-all` posterior a revertir las dos
pruebas negativas de §8.4).

## 8. Evidencia de verificación concreta

### 8.1 Mapa mental acumulativo (CH-08 > CH-07 > ... > CH-00)

`chapter-07.diagram`: 55 nodos / 89 aristas. `chapter-08.diagram`: **60 nodos / 99 aristas** (5
nodos nuevos: `CH-08`, `CMP-008`, `C-018`, y los conceptos de glosario nuevos que resuelven a nodos
propios). Cumple el criterio del encargo (más nodos/aristas que CH-07). `full-book.diagram` coincide
exactamente con el snapshot de CH-08 (el último), confirmando acumulación real.

Se confirmó explícitamente la arista que el encargo pedía verificar — la primera vez que un
capítulo nuevo produce una arista `PRODUCES`/`CONSUMES` hacia una entidad de un capítulo NO
inmediatamente anterior:

```text
"CMP-008" -> "C-008" [label="PRODUCES", ...];   ← C-008 introducido en CH-02, seis capítulos antes
"CMP-008" -> "C-010" [label="PRODUCES", ...];
"CMP-008" -> "C-011" [label="PRODUCES", ...];
"CMP-008" -> "C-018" [label="PRODUCES", ...];
"C-004" -> "CMP-008" [label="CONSUMES", ...];
"C-007" -> "CMP-008" [label="CONSUMES", ...];   ← C-007 introducido en CH-03, cinco capítulos antes
```

`build-mind-map` no la rechazó (no debía: `C-008`/`C-007` ya existían en el snapshot acumulado
antes de procesar CH-08, por ser capítulos estrictamente anteriores).

### 8.2 Web

- `dist/web/chapters/CH-08.html` existe, con SVG de mapa mental inline (`grep -c '<svg'` == 1).
- Anchors de entidad presentes: `id="CMP-008"` (1), `id="C-018"` (1).
- Navegación prev/next verificada en ambos sentidos: `CH-07.html` contiene `href="CH-08.html"` (≥1
  aparición); `CH-08.html` contiene `href="CH-07.html"` (≥1 aparición).
- Anchors de capítulos previos verificados intactos (1 aparición cada uno): `CH-00.html`
  (`C-001`); `CH-01.html` (`CMP-001`/`C-013`); `CH-02.html` (`CMP-002`/`C-008`); `CH-03.html`
  (`CMP-003`/`C-006`); `CH-04.html` (`CMP-004`/`C-005`); `CH-05.html` (`CMP-005`/`C-014`);
  `CH-06.html` (`CMP-006`/`C-015`); `CH-07.html` (`CMP-007`/`C-017`) — sin cambios.
- `<svg` aparece exactamente 1 vez en cada una de las 9 páginas de capítulo (CH-00..CH-08).
- `dist/web/index.html` lista los nueve capítulos (`CH-00`..`CH-08`).

### 8.3 PDF (`pypdf`)

- Build completo (CH-00..CH-08): **201 páginas** — el build de 8 capítulos (CH-00..CH-07) tenía 177
  páginas (ver `planes/2026-09-14-capitulo-07-execution-controller.md` §8.3); 201 > 177,
  confirmando el crecimiento esperado.
- Texto extraído del PDF completo, verificado con `pypdf.PdfReader(...).extract_text()`:
  `"CapabilityRegistry"` → `True`, `"CapabilityDescriptor"` → `True`, `"CMP-008"` → `True`,
  `"C-018"` → `True`, `"RawToolCallProposal"` → `True`, `"inputSchema"` → `True`,
  `"implementationRef"` → `True`.

### 8.4 Pruebas negativas (inyectadas y revertidas, una a la vez)

1. **`consumes` inválido en la ficha de componente**: se agregó `C-999` (inexistente) a
   `CMP-008.consumes` en `registry/components.yaml` → `validate-components` falló limpio con
   `exit 1` y el mensaje exacto `Componente CMP-008: consumes referencia contrato inexistente
   "C-999"`. Revertido (`diff` contra el backup en `/tmp/components.yaml.bak` confirmó archivo
   idéntico; `validate-components` volvió a `OK (8 componente(s))`, `exit 0`).
2. **Nombre canónico en una guiding question**: se reescribió `GQ-CH08-01` para que dijera
   literalmente "¿Decide CapabilityRegistry qué implementación concreta corresponde a un nombre de
   capacidad propuesto por el modelo?" → `validate-retrieval-set` falló limpio con `exit 1` y el
   mensaje exacto `retrievalSet.guidingQuestions[GQ-CH08-01] contiene el nombre canónico
   "CapabilityRegistry", que este mismo capítulo introduce — las preguntas guía deben usar lenguaje
   de problema`. Revertido (`diff` contra el backup en `/tmp/ch08.md.bak` confirmó archivo idéntico;
   `validate-retrieval-set` volvió a `OK`, `exit 0`).
3. Tras revertir ambas inyecciones (`diff` confirmó archivos idénticos byte a byte), `rm -rf dist &&
   ./scripts/build-all` volvió a pasar limpio con los mismos conteos de nodos/aristas (60/99), de
   contratos/componentes (18/8), de capítulos (9) y de páginas de PDF (201, verificado de nuevo con
   `pypdf`) que antes de las inyecciones (exit 0).

### 8.5 CH-00..CH-07 no se rompieron

- `validate-chapter`/`validate-retrieval-set` de los ocho siguen en verde (ver §7, corrida completa
  de `build-all`).
- Los anchors de CH-00 (`C-001`), CH-01 (`CMP-001`/`C-013`), CH-02 (`CMP-002`/`C-008`), CH-03
  (`CMP-003`/`C-006`), CH-04 (`CMP-004`/`C-005`), CH-05 (`CMP-005`/`C-014`), CH-06
  (`CMP-006`/`C-015`) y CH-07 (`CMP-007`/`C-017`) no cambiaron de contenido.
- Solo se editó `next_chapter` en el frontmatter de CH-07 — su cuerpo, su ficha de
  `ExecutionController` y su `retrieval_set` quedaron intactos.
- `mapa.html` sigue mostrando el grafo acumulado completo con los nueve capítulos.

## 9. Definition of Done (restringido a este incremento)

- ✅ CH-08 completo: 22 secciones (0, 1-19, 20, 21), sin relleno — cada sección con contenido real.
- ✅ `registry/contracts.yaml` / `registry/components.yaml` / `registry/glossary.yaml` /
  `book/book.yaml` actualizados y validados (`validate-contracts`, `validate-components`).
- ✅ `RetrievalSet` completo con `interleavedQuestions = 2` conectando con CH-02 y CH-03 — la
  conexión más rica del libro hasta ahora.
- ✅ Pipeline completo (`build-all`) verde desde `dist/` limpio, para los 9 capítulos.
- ✅ Evidencia concreta (no solo "pasó"): conteos de nodos/aristas del mapa mental (incluyendo la
  arista `PRODUCES` `CMP-008 → C-008` hacia una entidad de un capítulo no inmediatamente anterior),
  conteo de páginas de PDF (201 vs. 177 del build de 8 capítulos), texto extraído del PDF, anchors
  HTML, dos pruebas negativas con mensaje de error exacto y reversión confirmada con conteos
  idénticos.
- ✅ CH-00..CH-07 verificados intactos tras el cambio (salvo el campo de navegación autorizado en
  CH-07).
- ✅ Frontera `CapabilityRegistry` ↔ `ToolRuntime`/`ModelGateway`/`PolicyEngine`/`AgentLoop`
  documentada explícitamente en §8/§9/§15/§18 del capítulo, sin modificar
  `CMP-001`/`CMP-002`/`CMP-003`/`CMP-005`.
- ✅ `ToolCall` (C-008, CH-02) tiene, por primera vez, un componente real que lo produce mediante
  una resolución real — sin que este capítulo sobreestime lo que resuelve: el cableado end-to-end
  real que lo conecta con `AgentLoop`/`ModelGateway`/`PolicyEngine`/`ToolRuntime` sigue siendo,
  explícitamente, trabajo futuro.
- ✅ `CapabilityDescriptor.version` (P-26) es la primera materialización, en este libro, de
  versionado explícito de capabilities — sin implementar todavía el resto del lifecycle que P-26
  exige.

## 10. Deuda intencional hacia el próximo capítulo (fuera de este alcance)

- **El pipeline de integración completo `AgentLoop → ModelGateway → CapabilityRegistry →
  PolicyEngine → ToolRuntime`**: el candidato más claro de todo el libro para un capítulo de
  integración futuro — este capítulo cierra la última resolución que faltaba (CH-02/CH-03), pero
  ningún `AgentRun` real atraviesa todavía los cinco componentes en una sola ejecución.
- **El mecanismo real de registro/alta de capabilities**: `registeredCapabilities` llega como
  parámetro ya poblado; ningún componente de este libro modela quién registra un
  `CapabilityDescriptor` nuevo ni dónde se persiste.
- **El algoritmo real de validación de esquemas**: `argumentsMatchSchema` sigue siendo una señal de
  entrada asumida — el schema vive en un campo real (`inputSchema`), pero el motor de comparación
  no está modelado.
- **Capability lifecycle completo (P-26)**: `version` es explícita; compatibility policy, rollout,
  deprecation y retirement quedan fuera de alcance.
- **`SessionManager`, Provider Adapters reales, streaming real, `Channel Adapter` real,
  persistencia real de `ExecutionUsage`**: deuda heredada de capítulos anteriores, sin cambios en
  este capítulo.
- Reviewers plurales, evals y orquestación multi-agente: explícitamente fuera de alcance de BH-v0.1
  (igual que todos los capítulos anteriores).
