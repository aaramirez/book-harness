# Plan — Book Production Harness para "¿Cómo construir un arnés?"

**Fecha:** 2026-08-23 (aprobado 2026-09-13)
**Estado:** ✅ Completado — BH-v0.1 ejecutado de punta a punta (ver §11)

---

## 0. Fuentes usadas para este plan

Leídas directamente de `reference/md/`:

- `BOOK_HARNESS_BUILD_INSTRUCTIONS(1).md` — **documento rector**: especifica cómo construir el harness que escribe el libro (misión, outputs, agentes, skills, validadores, BookIR, milestone v0.1, Definition of Done).
- `REGLAS_LIBRO_AGENT_HARNESS(1).md` — reglas editoriales/arquitectónicas que el contenido del libro debe cumplir (estructura de capítulo obligatoria, "no magic entities", registries, tres vistas por interacción, etc.).
- `ARCHITECTURE_CONSTITUTION(1).md` — constitución arquitectónica de referencia (Principios P-01..P-15, Invariantes INV-01..INV-20, Component Sovereignty) que el propio harness debe respetar y que el libro debe enseñar a construir.

No se leyeron completos (se listan como posible contexto adicional, no bloquean este plan): `Estructura_Libro_*`, `Propuesta_Libro_*`, `Arquitectura_Agent_Harness_inspirado_en_Pi(1).md`, `APPLICATION_DEVELOPMENT_HARNESS(1).md`, `harness-empresarial-general(1).md`, `RH-0X_*` (catálogo de harnesses de referencia).

---

## 1. Supuesto clave (⚠️ confirmar)

El repo se llama `arnes-kb` y todo el material de referencia habla de construir un **"Agent Harness"** (arnés de agentes de software). Interpreto que el libro **"¿Cómo construir un arnés?"** es la versión en español de ese mismo libro (*Construyendo un Agent Harness*), no un libro sobre arneses físicos/de seguridad.

Si esto es incorrecto, avisa antes de que se ejecute el plan.

---

## 2. Misión (tomada del documento rector)

Construir un **Book Production Harness**: un sistema editorial gobernado — no un "escritor IA genérico" — que él mismo sea una implementación de referencia de las ideas arquitectónicas que el libro enseña.

> Probabilistic systems may propose decisions. Deterministic systems must govern consequences.

Debe producir, desde una única fuente canónica, dos salidas sincronizadas: libro Web y libro PDF.

---

## 3. Alcance de este plan

Ejecutar **BH-v0.1** (el "vertical slice" mínimo definido en la sección 20 del documento rector), aplicado al libro *¿Cómo construir un arnés?*, dentro de este repositorio. Explícitamente **no** se implementan en v0.1: reviewer agents plurales (técnico/pedagógico/consistencia), policies de aprobación humana, evals, orquestación multi-agente — quedan en el roadmap (sección 10 de este plan).

---

## 4. Estructura de repositorio a crear

Adaptada de la sección 18 del documento rector, con `arnes-kb` como raíz:

```text
arnes-kb/
├── constitution/
│   └── ARCHITECTURE_CONSTITUTION.md        # semilla: copiar/adaptar desde reference/md/ARCHITECTURE_CONSTITUTION(1).md
│
├── book/
│   ├── book.yaml                            # manifiesto canónico (id, versión, lista de capítulos)
│   ├── frontmatter/
│   │   ├── preface.md
│   │   └── introduction.md
│   ├── chapters/
│   │   └── 00-arquitectura-constitucion/
│   │       └── chapter.md                   # capítulo piloto de la Fase 5
│   ├── appendices/
│   │   └── glossary.md
│   └── assets/
│
├── registry/
│   ├── contracts.yaml
│   ├── components.yaml
│   └── glossary.yaml
│
├── agents/
│   ├── book-architect.md
│   └── chapter-author.md
│
├── skills/
│   ├── write-technical-chapter/SKILL.md
│   ├── define-contract/SKILL.md
│   ├── define-component/SKILL.md
│   ├── write-pseudocode/SKILL.md
│   └── analyze-constitutional-impact/SKILL.md
│
├── policies/
│   └── publishing.yaml                      # regla mínima v0.1: bloquear build si hay errores de validación
│
├── scripts/
│   ├── validate-chapter
│   ├── validate-contracts
│   ├── validate-components
│   ├── build-book-ir
│   ├── build-web
│   └── build-pdf
│
├── evals/                                    # vacío en v0.1, reservado
│
├── docs/
│   └── adr/
│
└── dist/
    ├── web/
    └── book.pdf
```

---

## 5. Fases de ejecución

### Fase 0 — Bootstrap
- Crear el árbol de directorios anterior.
- Copiar `ARCHITECTURE_CONSTITUTION(1).md` a `constitution/ARCHITECTURE_CONSTITUTION.md` como documento rector del propio harness (sin traducir aún; adaptar referencias de "Agent Harness" al marco de "arnés" si aplica).
- Elegir el runtime de los scripts deterministas (**decisión abierta**, ver §8) y dejarlo fijado en `scripts/README.md`.

### Fase 1 — Registries y modelo canónico
- Crear `registry/contracts.yaml`, `registry/components.yaml`, `registry/glossary.yaml`, inicialmente vacíos pero con el esquema de campos exigido por `REGLAS_LIBRO_AGENT_HARNESS`: para contratos (ID, Name, Version, Introduced In, Current Definition, Used By, Modified By, Constitutional Impact); para componentes (ID, Name, Responsibility, Owns, Does Not Own, Dependencies, Consumes, Produces, Introduced In, Constitutional Articles).
- Crear `book/book.yaml` con `book.id`, `book.version: 0.1` y la lista de capítulos (empezar solo con el capítulo piloto).

### Fase 2 — Agentes
Implementar como subagentes de Claude Code (`agents/*.md` con frontmatter de subagente):
- **Book Architect Agent**: propone estructura, valida dependencias de capítulos, progresión de conceptos, cumplimiento constitucional. No aprueba automáticamente cambios fundamentales.
- **Chapter Author Agent**: recibe un *Chapter Brief* controlado (brief + arquitectura previa + contratos/componentes disponibles + artículos constitucionales relevantes + reglas editoriales + skills relevantes) y escribe el capítulo. Nunca recibe el libro completo de una vez.

### Fase 3 — Skills
Crear las 5 skills del milestone v0.1 como `skills/<nombre>/SKILL.md`, codificando procedimiento (no solo prompts):
- `write-technical-chapter` — fuerza la secuencia de 19 secciones obligatorias de `REGLAS_LIBRO_AGENT_HARNESS` §26 (Current Architecture → … → Next Increment).
- `define-contract` — plantilla de contrato + reglas PC-01..PC-10.
- `define-component` — ficha arquitectónica obligatoria (Responsibility / Consumes / Depends on / Produces / Owns / Does NOT own).
- `write-pseudocode` — gramática canónica (`STRUCT`, `INTERFACE`, `IMPLEMENTATION`, etc.), regla "no magic entities".
- `analyze-constitutional-impact` — genera el bloque "Constitutional Impact" (principios afectados, invariantes introducidos/preservados) contra `constitution/ARCHITECTURE_CONSTITUTION.md`.

### Fase 4 — Validadores deterministas
Implementar como scripts ejecutables en `scripts/`:
- `validate-chapter`: checklist mínimo de la sección 8 del documento rector (metadata, contratos/componentes referenciados existen, ningún componente "futuro" citado antes de su introducción, secciones obligatorias presentes, Constitutional Impact presente).
- `validate-contracts` / `validate-components`: consistencia contra los registries.
- La pipeline de publicación debe fallar (`exit 1`) ante cualquier error de validación estructural.

### Fase 5 — Capítulo piloto (fuente canónica real)
- Elegir **un** capítulo real para probar el pipeline completo (propuesta: capítulo 0, "La Constitución Arquitectónica de un Arnés" — introduce el vocabulario y el marco P-xx/INV-xx que todo el libro reutilizará).
- Pasarlo por: Book Architect → Chapter Brief → Chapter Author → Draft → `validate-chapter`/`validate-contracts`/`validate-components` → si falla, revisar; si pasa, se convierte en fuente canónica.

### Fase 6 — BookIR y renderers mínimos
- Definir `BookIR` (metadata, chapters, glossary, contracts, components) y `ChapterIR` (sections, diagrams, codeBlocks, references, contractsIntroduced, componentsIntroduced) tal como en la sección 10 del documento rector.
- `build-book-ir`: parsea `book/` + `registry/` → `BookIR`.
- `build-web`: BookIR → HTML mínimo con navegación anterior/siguiente (sin necesidad de búsqueda/expandable contracts en v0.1).
- `build-pdf`: BookIR → `dist/book.pdf` (portada, TOC, capítulos, page numbers como mínimo).

### Fase 7 — Pipeline end-to-end
- Un único comando que corra: validar → construir BookIR → construir Web → construir PDF, y falle limpio si algo no pasa.
- Verificar que Web y PDF muestran el mismo contenido del capítulo piloto, derivado del mismo `BookIR`.

### Fase 8 — Verificación contra Definition of Done (v0.1)
Chequear explícitamente contra la lista de la sección 23 del documento rector, restringida a lo que aplica en v0.1 (fuente canónica, BookState explícito, registries poblados, dependencias de capítulo validadas, contexto controlado por agente, skills como procedimiento, quality gates deterministas, BookIR independiente de renderer, Web/PDF desde el mismo BookIR, un solo comando de build). Lo que quede pendiente (aprobación humana de arquitectura, ADRs, evals, observabilidad de runs) se documenta como deuda intencional hacia BH-v0.2+.

---

## 6. Entregables concretos de esta ejecución

- Árbol de directorios de §4 creado y poblado.
- 2 agentes, 5 skills, 3 registries con esquema, 1 policy mínima, ~6 scripts.
- 1 capítulo piloto que pasa validación.
- `dist/web/` y `dist/book.pdf` generados desde el mismo `BookIR` para ese capítulo.
- Este documento actualizado con checkboxes marcados a medida que se ejecuta.

---

## 7. Explícitamente fuera de alcance en v0.1

- Technical / Pedagogical / Consistency Reviewer agents (BH-v0.2 / v0.3).
- Dependency graph automático y policies de aprobación arquitectónica con HITL persistente (BH-v0.3 / v0.4 / v0.5).
- Evals y scorecards de calidad (BH-v0.6).
- Extensiones, automatización programada, orquestación multi-agente (BH-v0.7..v0.9).
- Migración a los primitivos del harness genérico (`AgentLoop`, `ContextEngine`, `ModelGateway`, etc.) — el libro *enseña* esos primitivos, pero el propio Book Harness aún no corre sobre ellos (BH-v1.0, principio de self-hosting, sección 19 y 25 del documento rector).

---

## 8. Decisiones (resueltas al aprobar, 2026-09-13)

1. **Runtime de los scripts deterministas**: Node.js plano (v22.11.0 disponible en el entorno) — sin dependencias, sin setup.
2. **Motor de PDF**: `pandoc` (v1.19.2.4, disponible en el entorno) — se usa para v0.1, sin diseño editorial todavía.
3. **Idioma del contenido**: español, con vocabulario técnico canónico en inglés (`AgentLoop`, `ToolRuntime`, etc.) — mismo criterio que este plan.
4. **Capítulo piloto**: capítulo 0, "La Constitución Arquitectónica de un Arnés" — confirmado.
5. **Ubicación**: raíz de **este mismo repo** (`book-harness`) — no un repo/carpeta `arnes-kb` separado. Tras la limpieza del 2026-09-13, este repo quedó dedicado en exclusiva al libro del arnés, así que el árbol de §4 se crea directamente acá (sin el prefijo `arnes-kb/`).

---

## 9. Roadmap posterior (referencia, no parte de esta ejecución)

```text
BH-v0.1  Autoría básica + validación + doble renderizado        ← este plan
BH-v0.2  Reviewers técnico y pedagógico
BH-v0.3  Reviewer de consistencia + dependency graph
BH-v0.4  Policies + workflow de aprobación arquitectónica
BH-v0.5  HITL durable + runs editoriales persistidos
BH-v0.6  Evals + scorecards de calidad
BH-v0.7  Modelo de extensión + renderizado enriquecido
BH-v0.8  Automatización de builds/reviews programados
BH-v0.9  Orquestación multi-agente selectiva
BH-v1.0  Book Harness corriendo sobre el Generic Agent Harness
```

---

## 10. Siguiente paso

Este plan queda en `/planes` para tu revisión. No se ha creado ningún archivo fuera de `planes/` todavía. Cuando lo apruebes (con o sin cambios a las decisiones abiertas de §8), ejecuto las Fases 0–8 en orden.

---

## 11. Registro de ejecución

**Fecha de ejecución:** 2026-09-13.
**Resultado:** BH-v0.1 completo — el capítulo piloto pasa validación y produce Web + PDF desde el mismo `BookIR`.

### 11.1 Qué se creó

Árbol completo en la raíz de `book-harness` (sin prefijo `arnes-kb/`, según §8.5):

```text
constitution/ARCHITECTURE_CONSTITUTION.md
book/book.yaml
book/frontmatter/{preface,introduction}.md
book/chapters/00-arquitectura-constitucion/chapter.md
book/appendices/glossary.md
book/assets/.gitkeep
registry/{contracts,components,glossary}.yaml
agents/{book-architect,chapter-author}.md
skills/{write-technical-chapter,define-contract,define-component,write-pseudocode,analyze-constitutional-impact}/SKILL.md
policies/publishing.yaml
scripts/README.md
scripts/{validate-chapter,validate-contracts,validate-components,build-book-ir,build-web,build-pdf,build-all}
scripts/lib/{yaml-lite,chapter-parser,registries,book-ir,book-state}.js
evals/.gitkeep
docs/adr/.gitkeep
dist/{book-ir.json,book-state.json,book.pdf,web/}   (generado por build-all; ver .gitignore)
```

### 11.2 Decisiones de diseño no 100% especificadas en el plan, tomadas durante la implementación

1. **Formato de los registries y del frontmatter de capítulo**: el plan pide YAML pero no dicta un
   parser. Runtime = Node.js plano sin dependencias npm (decisión §8.1), así que se escribió un
   parser YAML de subconjunto propio (`scripts/lib/yaml-lite.js`): mappings/secuencias por
   indentación, listas en línea `[a,b,c]`, escalares con/sin comillas y **block scalars** `|`
   (literal) / `>` (folded) — necesarios para que `current_definition` en `contracts.yaml` guarde
   un `STRUCT`/`ENUM` legible en varias líneas. No soporta anchors, tags ni flow maps: es
   deliberadamente mínimo y auditable, no un YAML completo.
2. **Qué entidades introduce el capítulo piloto**: el plan solo decía "capítulo 0, Constitución
   Arquitectónica". Se decidió que CH-00 introduce **7 contratos de datos fundamentales**
   (`C-001 AgentMessage`, `C-002 AgentConfig`, `C-003 AgentState`, `C-004 ExecutionContext`,
   `C-010 AgentEvent`, `C-011 HarnessError`, `C-012 ExecutionBudget` — IDs tomados de la tabla
   canónica de `REGLAS_LIBRO_AGENT_HARNESS(1).md` §10) pero **cero componentes de runtime**:
   `AgentLoop`, `ModelGateway`, `ToolRuntime`, etc. se mencionan solo como tabla de "Preview — no
   introducido en este capítulo" (permitido explícitamente por
   `BOOK_HARNESS_BUILD_INSTRUCTIONS(1).md` §22 regla 8), nunca dentro de un bloque de
   pseudocódigo. `registry/components.yaml` queda vacío tras esta ejecución; el primer componente
   real llegará en un capítulo futuro fuera de este alcance.
3. **Alcance de la validación "no magic entities"**: los validadores solo inspeccionan entidades
   dentro de bloques ` ```pseudocode ` (no menciones en prosa), y lo hacen **en orden dentro del
   capítulo** (un `STRUCT` solo está disponible para los bloques que le siguen), combinado con un
   set de "siempre disponibles" (primitivos de la gramática + identificadores fundamentales de
   `REGLAS_LIBRO` §3.1) y con lo ya registrado por capítulos **estrictamente anteriores** en
   `book/book.yaml`. Esto es una interpretación operacional razonable de una regla que el
   documento rector deja en prosa ("no magic entities", "no dump the whole book") — se documenta
   aquí por si un futuro capítulo la encuentra demasiado (o poco) estricta.
4. **`BookState` explícito como artefacto separado de `BookIR`**: el documento rector define
   ambos (§5 y §10) pero el plan no distinguía si había que materializar los dos. Se implementó
   `scripts/lib/book-state.js` + `dist/book-state.json` (con `dependencies: null` y `adrs: []`
   marcados explícitamente como pendientes, no omitidos) además de `dist/book-ir.json`, para que
   "BookState is explicit" (Definition of Done) no dependa de inferir el estado a partir del IR
   de renderizado.
5. **`dist/` no se versiona**: se agregó `dist/` a `.gitignore` (mismo criterio que
   `libro-de-panaderia/.gitignore` con su `build/`) — son artefactos regenerables con
   `./scripts/build-all`, no fuente canónica.
6. **Motor de PDF, sintaxis real**: `pandoc` instalado es 1.19.2.4 (pre-2.0): usa
   `--latex-engine=xelatex`, no `--pdf-engine` (que no existe en esa versión). Se confirmó
   `xelatex`/`pdflatex` disponibles vía TeX Live del sistema.

### 11.3 Resultado de correr el pipeline end-to-end (Fase 7)

Comando: `./scripts/build-all` (desde la raíz de `book-harness`, con `dist/` borrado antes para
probar un build limpio):

```text
=== build-all: validación determinista ===
▶ validate-contracts
validate-contracts: OK (7 contrato(s))
▶ validate-components
validate-components: OK (0 componente(s))
▶ validate-chapter book/chapters/00-arquitectura-constitucion/chapter.md
validate-chapter: OK (.../chapter.md)
  secciones: 19/19
  bloques pseudocode: 12
  contratos introducidos: 7
  componentes introducidos: 0

=== build-all: construcción ===
▶ build-book-ir
build-book-ir: OK → dist/book-ir.json
  capítulos: 1 / contratos: 7 / componentes: 0 / términos de glosario: 12
▶ build-web
build-web: OK → dist/web/ (index.html + 1 capítulo)
▶ build-pdf
build-pdf: OK → dist/book.pdf (77630 bytes, PDF 1.5 válido)

=== build-all: OK — validado, BookIR, Web y PDF generados desde la misma fuente canónica ===
BookState persistido en dist/book-state.json
```

Exit code: `0`.

**Pruebas negativas** (para confirmar que los validadores no son un "pase simulado"):
- Se inyectó una entidad inexistente (`NotARealType()`) en una copia del capítulo →
  `validate-chapter` la detectó y salió con `exit 1`.
- Se borró el campo `version` de un contrato en `registry/contracts.yaml` → `validate-contracts`
  y, en cadena, `./scripts/build-all` fallaron limpiamente con `exit 1` **sin** llegar a construir
  `BookIR`/Web/PDF (`policies/publishing.yaml: unresolved_validation_errors = deny`), y
  `dist/book-state.json` quedó con `buildStatus: "failed_validation"`. Al restaurar el archivo,
  `build-all` volvió a pasar limpio.

**Web y PDF desde el mismo BookIR**: ambos `build-web` y `build-pdf` leen exclusivamente
`dist/book-ir.json` (nunca vuelven a parsear `book/chapters/*.md`), confirmado por inspección de
código y por el contenido de `dist/web/chapters/CH-00.html` (pseudocódigo, secciones y acentos en
español se renderizan correctamente) y de `dist/book.pdf` (PDF 1.5 válido, 77 KB, generado sin
errores por `pandoc`/`xelatex`).

### 11.4 Definition of Done (BOOK_HARNESS_BUILD_INSTRUCTIONS(1).md §23) — restringido a BH-v0.1

- ✅ Canonical source exists. — `book/book.yaml` + `book/chapters/00-arquitectura-constitucion/chapter.md`.
- ✅ Book structure is machine-readable. — `book/book.yaml` parseado por `scripts/lib/registries.js`.
- ✅ BookState is explicit. — `scripts/lib/book-state.js` → `dist/book-state.json`.
- ✅ Contracts and components are registered. — `registry/contracts.yaml` (7), `registry/components.yaml` (0, correctamente vacío: CH-00 no introduce componentes).
- ✅ Chapter dependencies are validated. — `validate-chapter` rechaza referencias a entidades de capítulos futuros y a entidades no definidas aún dentro del propio capítulo (probado con inyección de entidad inexistente). El grafo de dependencias *automático* (`ArchitectureDependencyGraph` completo) es BH-v0.3 — ver ⬜ más abajo.
- ✅ Agents use controlled context. — `agents/book-architect.md` / `agents/chapter-author.md` definen explícitamente el Chapter Brief y prohíben pasar el libro completo.
- ✅ Skills encode reusable procedures. — 5 skills en `skills/`, cada una con pasos/checklist/plantilla concretos (no solo un prompt).
- ✅ Deterministic quality gates exist. — `validate-chapter` / `validate-contracts` / `validate-components`, con `exit 1` real verificado en pruebas negativas.
- ⬜ Architectural changes can require human approval. — Fuera de alcance de BH-v0.1 (plan §7: "policies de aprobación humana" quedan para BH-v0.4/v0.5). `agents/book-architect.md` documenta narrativamente la regla ("no aprueba automáticamente cambios fundamentales") pero no hay `policies/architecture.yaml` ni workflow `WAITING_FOR_HUMAN` persistido.
- ✅ BookIR is renderer-independent. — `scripts/lib/book-ir.js` + `dist/book-ir.json`; ni `build-web` ni `build-pdf` vuelven a tocar `book/chapters/*.md`.
- ✅ Web and PDF derive from the same BookIR. — Verificado por código e inspección de artefactos (§11.3).
- ✅ Cross-chapter terminology is consistent. — Consistencia verificada dentro del alcance de 1 capítulo (PC-05 aplicado vía nombres de registry); la prueba real de consistencia *entre* capítulos solo será observable cuando exista un CH-01 (fuera de este alcance).
- ✅ Pseudocode references only defined entities. — Escaneo "no magic entities" en `validate-chapter`, probado en positivo y negativo.
- ⬜ Architecture evolution is traceable through ADRs. — `docs/adr/` vacío; deuda intencional (BH-v0.2+).
- ⬜ Editorial runs are observable. — `dist/book-state.json` registra `buildStatus` y estado por capítulo, pero no hay historial persistido de runs, costos ni iteraciones de agentes; deuda intencional (alineado con el roadmap BH-v0.5 / enterprise amendment §25 del documento rector).
- ⬜ Evals can measure chapter quality. — `evals/` vacío; explícitamente fuera de alcance (BH-v0.6, plan §7).
- ✅ One command/pipeline can build the complete book. — `./scripts/build-all`, probado en limpio y en fallo.

### 11.5 Deuda intencional hacia BH-v0.2+

Coincide con lo ya declarado como fuera de alcance en §7 de este plan: reviewers técnico/
pedagógico/consistencia, `ArchitectureDependencyGraph` automático + policies de aprobación
arquitectónica con HITL persistente, evals/scorecards, extensiones/automatización/orquestación
multi-agente, y migración del propio Book Harness a los primitivos del harness genérico
(`AgentLoop`, `ContextEngine`, etc. — principio de self-hosting, BH-v1.0). A esto se suma,
identificado durante esta ejecución: ADRs persistidos (`docs/adr/` vacío) y observabilidad de
runs editoriales (qué agente propuso qué, cuántas iteraciones, costo) — ninguno de los dos estaba
en el alcance explícito de BH-v0.1 pero quedan como huecos concretos para BH-v0.2+.
