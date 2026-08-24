# Plan — Mapa mental progresivo del libro

**Fecha:** 2026-08-24
**Estado:** 🟡 Borrador para revisión — no ejecutar todavía
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
