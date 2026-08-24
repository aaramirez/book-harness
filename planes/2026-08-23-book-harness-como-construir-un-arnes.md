# Plan — Book Production Harness para "¿Cómo construir un arnés?"

**Fecha:** 2026-08-23
**Estado:** 🟡 Borrador para revisión — no ejecutar todavía

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

## 8. Decisiones abiertas para revisión antes de ejecutar

1. **Runtime de los scripts deterministas**: Node.js sin dependencias (rápido de correr con Bash, cero setup) vs. un stack con dependencias (p. ej. TypeScript + un motor de render Markdown/PDF más robusto). Propuesta: Node.js plano para v0.1, revisar en BH-v0.2 si hace falta más.
2. **Motor de PDF**: `pandoc` si está disponible en el entorno, o un renderer propio minimalista en v0.1 (sin diseño editorial todavía). Confirmar si `pandoc`/`wkhtmltopdf`/similar ya está instalado o si hay que asumir su ausencia.
3. **Idioma del contenido**: dado que el libro se titula en español pero todo el material de referencia y vocabulario canónico (`AgentLoop`, `ToolRuntime`, etc.) está en inglés — ¿el capítulo piloto se escribe en español con términos técnicos en inglés (como hace este mismo plan), o completamente en inglés?
4. **Capítulo piloto**: confirmar que el capítulo 0 propuesto (Constitución Arquitectónica) es el punto de partida correcto, o si prefieres otro capítulo como prueba end-to-end.
5. **Ubicación**: confirmar que todo esto vive en la raíz de `arnes-kb` (mismo repo que `reference/`) y no en un repo/carpeta nuevo separado.

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
