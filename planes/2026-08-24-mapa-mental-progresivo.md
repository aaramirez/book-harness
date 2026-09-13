# Plan — Mapa mental progresivo del libro

**Fecha:** 2026-08-24 (aprobado 2026-09-13)
**Estado:** ✅ Completado — ver §9
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (método de aprendizaje — este documento se conecta directamente con "Esqueleto", "Conectar" y "Lente de Sistemas")

---

## 1. La idea

Que el libro no solo se lea de forma lineal, sino que el lector pueda ver, en cualquier punto, **un mapa mental de todo lo aprendido hasta ese capítulo** — y que ese mapa crezca capítulo a capítulo hasta convertirse, en el último capítulo, en el mapa completo del sistema/arnés enseñado por el libro.

No es un mapa mental genérico de "ideas sueltas": es un grafo de la arquitectura real que el libro construye — los mismos conceptos, componentes y contratos que ya existen como datos estructurados en el harness.

---

## 2. Por qué no es una función nueva, sino exponer algo que el plan base ya modela

En `BOOK_HARNESS_BUILD_INSTRUCTIONS(1).md`:

- §5 ya define `BookState.dependencies: ArchitectureDependencyGraph` — un grafo que crece con cada capítulo.
- §8 ya lista `build-dependency-graph` entre los scripts deterministas del harness.
- §11 (Web Renderer) ya exige que los nombres de componentes puedan **enlazar a su definición canónica** y que existan "architecture diagrams" navegables.
- `REGLAS_LIBRO_AGENT_HARNESS(1).md` §9 ya exige un "Architecture Dependency Map" con una versión temprana y una versión posterior — es decir, el libro **ya está obligado** a mostrar cómo crece el árbol de dependencias.

Lo que falta no es el dato — es tratarlo como **artefacto de lectura, no solo de validación interna**, y ampliarlo de "solo componentes" a "conceptos + componentes + contratos", que es lo que realmente forma un mapa mental completo del libro.

```text
Ya existe (uso interno)                Se agrega (uso lector)
────────────────────────               ──────────────────────
ArchitectureDependencyGraph      →     BookMindMap
build-dependency-graph script    →     snapshot visual por capítulo
Dependency Map (solo componentes) →    + conceptos + contratos + glosario
```

---

## 3. Modelo de datos

### 3.1 `BookMindMap` — extiende, no reemplaza, `ArchitectureDependencyGraph`

```text
STRUCT BookMindMap
    nodes: List<MindMapNode>
    edges: List<MindMapEdge>
    snapshotAsOfChapter: ChapterId     # hasta qué capítulo llega esta foto
END

STRUCT MindMapNode
    id: NodeId
    kind: NodeKind
    label: Text                       # nombre canónico (Component/Contract)
                                       # o término de Glossary (Concept)
    introducedInChapter: ChapterId
END

ENUM NodeKind
    CONCEPT           # entrada de Glossary
    COMPONENT         # entrada de Component Registry
    CONTRACT          # entrada de Contract Registry
END

STRUCT MindMapEdge
    from: NodeId
    to: NodeId
    kind: EdgeKind
END

ENUM EdgeKind
    DEPENDS_ON
    PRODUCES
    CONSUMES
    INTRODUCES         # capítulo → entidad
    MODIFIES           # capítulo → entidad ya existente
END
```

Cada capítulo produce **un snapshot** (`snapshotAsOfChapter = ese capítulo`), acumulativo: el snapshot del capítulo N contiene todos los nodos/aristas de los snapshots 0..N-1 más lo que introduce/modifica el capítulo N. El snapshot del último capítulo es el mapa mental completo del libro.

### 3.2 Origen determinista de cada snapshot (sin contenido nuevo que inventar)

```text
Glossary                     →  nodos CONCEPT
Component Registry           →  nodos COMPONENT
Contract Registry            →  nodos CONTRACT
"Depends on" de cada ficha   →  aristas DEPENDS_ON
"Produces" / "Consumes"      →  aristas PRODUCES / CONSUMES
"Introduces Components/      →  aristas INTRODUCES (capítulo → entidad)
 Contracts" del capítulo
"Modifies Contracts"         →  aristas MODIFIES
 del capítulo
```

Todo esto ya es obligatorio por `REGLAS_LIBRO_AGENT_HARNESS(1).md` §10-§12 (Contract Registry, Component Registry, declaración de cambios por capítulo). El mapa mental es una **proyección** de esos datos, no una fuente nueva de verdad — igual que el `RetrievalSet` del método de aprendizaje (mismo principio: derivar, no inventar).

---

## 4. Script nuevo: `build-mind-map`

Se agrega a `scripts/` (Fase 4 del plan base, junto a `build-dependency-graph`):

```text
build-mind-map:
    INPUT:
        registry/components.yaml
        registry/contracts.yaml
        registry/glossary.yaml
        book/book.yaml (orden de capítulos)
        declaraciones "Introduces/Modifies" de cada capítulo ya
            validado por validate-chapter

    PROCESO:
        para cada capítulo, en orden:
            snapshot[N] = snapshot[N-1]
                          + nodos/aristas que este capítulo introduce
                          + aristas que este capítulo modifica

    OUTPUT:
        un BookMindMap por capítulo (snapshot acumulativo)
        + un BookMindMap final = snapshot del último capítulo

    Falla si un capítulo referencia un nodo que no existe todavía en
    el snapshot anterior — mismo principio "no magic entities",
    aplicado al grafo.
```

---

## 5. Renderizado

- **Web**: cada capítulo termina (o abre, ver §6) con una vista del mapa hasta ese punto. Los nodos son **clicables** y llevan a la definición canónica (ya exigido por §11 del plan base para componentes; se generaliza a conceptos y contratos). Los nodos nuevos de este capítulo se resaltan visualmente distinto de los ya conocidos. Existe además una vista global `/mapa` con el mapa completo acumulado hasta el capítulo actual del lector.
- **PDF**: un diagrama vectorial estático por capítulo (mismo principio de "Diagrams as Source" del plan base §13 — nunca raster) + un apéndice final con el mapa completo del libro.
- Igual que los demás diagramas del libro (sequence diagrams, dependency map), el mapa se guarda como **fuente de diagrama**, no como imagen generada a mano:

```text
diagrams/
└── mindmap/
    ├── chapter-00.diagram
    ├── chapter-01.diagram
    └── ...
    └── full-book.diagram
```

---

## 6. Cómo se conecta con el método de aprendizaje activo (documento previo)

- **Esqueleto (Reducir, Sección 0):** en vez de solo listar los títulos de sección, la Sección 0 puede mostrar el mapa **hasta el capítulo anterior**, con los nodos que este capítulo va a agregar marcados como "próximamente" — visualiza el 20% esencial antes del detalle.
- **Recordar / retrieval (Sección 21):** antes de revelar el snapshot actualizado, pedir al lector que **reconstruya de memoria** qué nodo(s) nuevo(s) se conectan y a qué nodo existente se enganchan — el mapeo conceptual es en sí mismo una técnica de recuerdo activo (Joseph Novak, *concept mapping*, Cornell — no confundir con el método del Video 2 del documento anterior, son técnicas distintas aunque de la misma época).
- **Conectar / interleaving:** el mapa es la herramienta visual literal para la regla "Error 2: estudiar temas aislados" — cualquier pregunta de interleaving puede señalarse directamente como dos nodos no adyacentes en el mapa que el capítulo actual termina conectando.
- **Lente de Sistemas (Sección 20):** la capa "estructuras/reglas/incentivos" del Iceberg y el "punto de apalancamiento" pueden señalarse directamente sobre el mapa (qué nodo tiene más aristas entrantes = candidato natural a punto de apalancamiento).

---

## 7. Alcance v0.1 vs. después

**Sí entra en v0.1:**
- `BookMindMap` como snapshot estático por capítulo (nodos + aristas), derivado de los registries ya obligatorios.
- Script `build-mind-map`.
- Render estático (Web: SVG no interactivo más allá de enlaces a definiciones; PDF: diagrama vectorial) al cierre de cada capítulo + mapa completo como apéndice.

**Fuera de v0.1 (roadmap):**
- Vista `/mapa` interactiva navegable/zoomable con historial ("cómo se veía el mapa en el capítulo 3").
- Animación de "qué se agregó este capítulo" en la Web.
- Reconstrucción de memoria del mapa como ejercicio evaluado (necesita el mismo `SessionManager`/persistencia que el resto de la capa de aprendizaje activo — BH-v0.5+).

---

## 8. Siguiente paso

Este documento queda en `/planes` junto a los otros dos. Si lo apruebas, se ejecuta junto con las Fases 4 y 6 del plan base (validadores y BookIR/renderers), incorporando `build-mind-map` y los snapshots de `BookMindMap` desde la primera pasada.

---

## 9. Registro de ejecución

**Fecha de ejecución:** 2026-09-13.
**Resultado:** BookMindMap progresivo implementado y cableado al pipeline completo (Web + PDF),
verificado sobre el único capítulo real del libro (`CH-00`) y con una prueba negativa real de
"no magic entities" aplicada al grafo.

### 9.1 Qué se creó

```text
scripts/lib/mindmap.js        # NUEVO — lógica pura: snapshots acumulativos de BookMindMap
scripts/lib/dot-writer.js     # NUEVO — snapshot → texto Graphviz DOT
scripts/lib/render-diagram.js # NUEVO — helper compartido: dot -Tsvg / dot -Tpdf
scripts/build-mind-map        # NUEVO — CLI: escribe diagrams/mindmap/*.diagram

diagrams/mindmap/chapter-00.diagram   # NUEVO — fuente DOT, snapshot acumulado hasta CH-00
diagrams/mindmap/full-book.diagram    # NUEVO — fuente DOT, snapshot completo del libro

scripts/lib/book-ir.js   # MODIFICADO — ChapterIR gana `contractsModified` y
                          # `mindMapDiagramPath`; BookIR gana `mindMapFullBookDiagramPath`
scripts/build-all        # MODIFICADO — corre `build-mind-map` entre build-book-ir y build-web
scripts/build-web         # MODIFICADO — anchors de entidad por capítulo, bloque de mapa mental
                          # inline por capítulo, página nueva dist/web/mapa.html
scripts/build-pdf         # MODIFICADO — página de diagrama vectorial por capítulo + apéndice
                          # final "Mapa Mental Completo del Libro"
scripts/README.md         # MODIFICADO — documenta build-mind-map y la decisión de formato DOT
```

### 9.2 Decisiones de diseño no especificadas al 100% por el plan (o por el Paso 2 del encargo)

1. **Nodo `CHAPTER` — extensión del `NodeKind` del plan.** El plan (§3.1) solo enumera
   `CONCEPT | COMPONENT | CONTRACT` como `NodeKind`, pero define `EdgeKind.INTRODUCES` /
   `MODIFIES` como "capítulo → entidad" — lo cual exige que el capítulo exista como nodo real del
   grafo (Graphviz necesita un nodo origen). Se agregó `CHAPTER` como un cuarto `NodeKind`
   práctico (`id` = `ChapterId`, `shape=folder`), documentado en `scripts/lib/mindmap.js`. Sin
   este nodo, las aristas INTRODUCES/MODIFIES no tendrían origen representable.
2. **Glosario → nodos CONCEPT: solo entradas `kind: concept`.** `registry/glossary.yaml` tiene
   entradas con `kind: contract`/`kind: component` que ya duplican (vía `ref`) una entrada de
   `registry/contracts.yaml`/`components.yaml`. Generar un nodo CONCEPT aparte para esas entradas
   habría duplicado la misma entidad con dos ids distintos en el grafo. Se decidió: solo
   `kind: concept` produce un nodo CONCEPT propio (con id sintetizado, ver punto 3); las entradas
   `kind: contract`/`kind: component` del glosario se tratan como metadato del registry
   correspondiente, no como nodo aparte.
3. **Simplificación documentada de "enlace a la definición canónica" (Paso 2, punto 5 del
   encargo).** No existen páginas de definición dedicadas por entidad ni un glosario navegable en
   este alcance v0.1 (sería un plan mucho mayor). Se implementó: cada nodo del DOT lleva un
   atributo `URL` (Graphviz lo traduce a `<a xlink:href>` real en el SVG) apuntando a
   `chapters/<ChapterId>.html#<entity-id>` — un anchor nuevo (`<a id="..."></a>`) agregado por
   `build-web` al inicio del cuerpo de la página del capítulo que INTRODUCE esa entidad (no el que
   la modifica). Verificado con `xml.dom.minidom` sobre el SVG real: 13 elementos `<a>` con
   `xlink:href` apuntando a los 13 anchors esperados de `CH-00.html`.
4. **Dirección de las aristas PRODUCES / CONSUMES.** El plan no especifica la dirección exacta.
   Se decidió: `PRODUCES` va `component → contract` (el componente emite el contrato) y
   `CONSUMES` va `contract → component` (el contrato "fluye hacia" quien lo consume) — una
   convención de flujo de datos consistente, documentada en `scripts/lib/mindmap.js`. No hay datos
   reales todavía para ejercitar esto (`registry/components.yaml` sigue vacío tras CH-00), pero la
   prueba negativa (9.4) ejercita la validación "no magic entities" sobre `consumes`.
5. **Un solo `.diagram`, dos convenciones de URL — resuelto con un rewrite documentado en
   `build-web`.** El mismo SVG (por capítulo) se incrusta en dos contextos con distinta base de
   ruta: `dist/web/chapters/CH-XX.html` (un nivel bajo `chapters/`) y, para el snapshot completo,
   `dist/web/mapa.html` (en la raíz). Se generó una única URL en el `.diagram` fuente, relativa a
   la raíz de `dist/web/` (`chapters/CH-XX.html#id`, igual que la usa `mapa.html`), y
   `build-web.rewriteSvgHrefsForChapterDir()` reescribe ese prefijo únicamente al incrustar el SVG
   dentro de la página del propio capítulo. Es la única excepción al criterio "un `.diagram`, una
   URL", documentada aquí y en el propio código.
6. **Ruta absoluta para las imágenes PDF en `build-pdf` (bug real encontrado y corregido durante
   esta ejecución).** El primer intento usó una ruta relativa a `dist/.build/` para las imágenes
   `![...](mindmap/chapter-00.pdf)`; pandoc 1.19.2.4 resuelve las rutas de imagen relativas al cwd
   del PROCESO pandoc (la raíz del repo, donde `build-all` invoca a `build-pdf`), no al directorio
   del propio `.md` — el primer build completo terminó con
   `[pandoc warning] Could not find image` y las páginas de diagrama simplemente no aparecían (el
   build no fallaba, pero el contenido faltaba silenciosamente). Corregido usando la ruta
   ABSOLUTA del `.pdf` renderizado en el markdown intermedio. Confirmado por conteo real de
   páginas del PDF antes/después del fix (ver 9.3).
7. **Orden del apéndice final: mapa mental DESPUÉS del apéndice de flashcards.** El encargo dejaba
   la decisión abierta. Se decidió que las flashcards (repaso espaciado, la pieza más
   "accionable") cierran el cuerpo práctico del libro, y el mapa mental completo es la última
   página del libro entero — el panorama de conjunto solo tiene sentido después de haber visto el
   detalle capítulo a capítulo y las tarjetas.
8. **`contractsModified` agregado a `ChapterIR`.** El plan base ya definía `contractsIntroduced` /
   `componentsIntroduced` pero no `contractsModified`; se agregó (fuente:
   `frontmatter.modifies_contracts`) para poder generar también los anchors de entidades
   MODIFICADAS por un capítulo (Paso 2, punto 5 del encargo pide anchors para "introduce o
   modifica"), no solo las introducidas. En `CH-00`, `modifies_contracts` está vacío, así que este
   campo no tiene efecto observable todavía — queda listo para el primer capítulo que sí modifique
   un contrato existente.
9. **`size="6.5,9"; ratio=compress;` en el DOT.** No estaba en el plan; se agregó como atributo
   global del grafo para que `dot -Tpdf` produzca una página de tamaño razonable dentro del PDF
   (sin esto, un grafo ancho podría desbordar el margen de la página al incrustarse con
   `\includegraphics` sin escalado explícito). Afecta por igual al SVG (donde no es un problema:
   el CSS `.mindmap-svg svg { max-width:100% }` ya lo escala).

### 9.3 Resultado real del pipeline

Comando (desde limpio, `rm -rf dist` antes):

```text
$ rm -rf dist && ./scripts/build-all
=== build-all: validación determinista ===
▶ validate-contracts
validate-contracts: OK (7 contrato(s))
▶ validate-components
validate-components: OK (0 componente(s))
▶ validate-chapter book/chapters/00-arquitectura-constitucion/chapter.md
validate-chapter: OK (.../chapter.md)
  secciones: 22/19
  bloques pseudocode: 12
  contratos introducidos: 7
  componentes introducidos: 0
▶ validate-retrieval-set book/chapters/00-arquitectura-constitucion/chapter.md
validate-retrieval-set: OK (.../chapter.md)
  guidingQuestions: 5 / recallQuestions: 5 / explainPrompts: 2 / interleavedQuestions: 0 (exención CH-00)
  flashcards: 7 / calibrationPairs: 5

=== build-all: construcción ===
▶ build-book-ir
build-book-ir: OK → dist/book-ir.json (1 capítulo, 7 contratos, 0 componentes, 12 términos)
▶ build-mind-map
build-mind-map: escribiendo diagrams/mindmap/*.diagram (Graphviz DOT)
  chapter-00.diagram: 13 nodo(s), 12 arista(s) (13 nuevo(s) en este capítulo)
  full-book.diagram: 13 nodo(s), 12 arista(s)
build-mind-map: OK
▶ build-web
build-web: OK → dist/web/ (index.html + 2 frontmatter + 1 capítulo + mapa.html)
▶ build-pdf
build-pdf: OK → dist/book.pdf (157888 bytes)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
BookState persistido en dist/book-state.json
```

Exit code: `0`.

**Evidencia concreta de verificación (por contenido real, no por tamaño de archivo):**

- SVG inline: `grep -c '<svg' dist/web/chapters/CH-00.html` → `1`; `grep -c '<svg'
  dist/web/mapa.html` → `1`.
- Anchors de entidad: `grep -o 'id="C-001"' dist/web/chapters/CH-00.html` → coincide;
  `id="CONCEPT-harness"` también presente.
- Links reescritos correctamente por contexto: dentro de `dist/web/chapters/CH-00.html` los
  `href` son `CH-00.html#C-001` (sin prefijo); dentro de `dist/web/mapa.html` son
  `chapters/CH-00.html#C-001` (con prefijo) — confirmado con `grep` sobre ambos archivos.
- `dist/web/index.html` enlaza `mapa.html`.
- SVG real inspeccionado con `xml.dom.minidom`: 13 elementos `<a>` con `xlink:href`, uno por nodo,
  apuntando a los anchors esperados.
- PDF: `pypdf` — **24 páginas sin el mapa mental (baseline, generado revirtiendo temporalmente los
  cambios con `git stash`) → 28 páginas con el mapa mental** (+1 página de diagrama por capítulo
  +1 apéndice final, más el ajuste de TOC). Texto extraído contiene literalmente "Mapa Mental
  hasta este Capítulo" y "Apéndice: Mapa Mental Completo del Libro".
- Prueba negativa: se agregó a `registry/components.yaml` un componente inventado
  `CMP-999`/`FakeComponent` con `consumes: [C-999]` (contrato inexistente). Resultado:
  `validate-components` falla (`exit 1`, "consumes referencia contrato inexistente"), y de forma
  independiente `node scripts/build-mind-map` TAMBIÉN falla por su cuenta (`exit 1`,
  "declara consumes -> C-999... no magic entities") — confirmando que la validación "no magic
  entities" del grafo no depende solo de `validate-components`. `./scripts/build-all` se detiene
  limpio en la etapa de validación (`policies/publishing.yaml: unresolved_validation_errors =
  deny`). Se restauró `registry/components.yaml` a su contenido original (diff vacío) y se
  reconfirmó el build limpio (`exit 0`, mismos conteos que arriba).

### 9.4 Qué queda como deuda intencional hacia después (según §7 de este mismo plan)

Explícitamente fuera de v0.1, sin implementar en esta ejecución:

- Vista `/mapa` interactiva navegable/zoomable con historial ("cómo se veía el mapa en el
  capítulo 3") — hoy `mapa.html` es siempre el snapshot completo actual, sin navegación temporal.
- Animación de "qué se agregó este capítulo" en la Web — hoy la novedad se señala solo con
  borde/color más intenso en el SVG estático, no con una transición animada.
- Reconstrucción de memoria del mapa como ejercicio evaluado (plan §6, "Recordar / retrieval") —
  necesita el mismo `SessionManager`/persistencia que el resto del Ciclo de Dominio Activo
  (BH-v0.5+, ya declarado como deuda en el plan del método de aprendizaje activo).

Adicionalmente, identificado durante ESTA ejecución (no estaba en el §7 original, pero es una
consecuencia directa del alcance real del libro hoy):

- Con un solo capítulo real (`CH-00`) y `registry/components.yaml` vacío, las aristas
  `DEPENDS_ON`/`PRODUCES`/`CONSUMES` nunca se ejercitan con datos reales en este repo todavía —
  solo con la prueba negativa sintética de 9.3. Se ejercitarán de verdad en cuanto exista un
  capítulo que introduzca el primer componente real (fuera de alcance de esta ejecución).
- El link "canónico" de cada entidad apunta siempre al capítulo que la INTRODUJO, nunca a una
  página de definición dedicada (ver 9.2 punto 3) — si el libro crece lo suficiente, una vista de
  glosario navegable independiente del capítulo sigue siendo trabajo futuro real, no cosmético.
