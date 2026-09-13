# Scripts — runtime

**Runtime elegido (Fase 0, decisión §8.1 del plan): Node.js plano.**

- Versión disponible en el entorno de desarrollo: `v22.11.0` (ejecutar `node --version` para confirmar
  la versión local; cualquier Node.js ≥ 18 LTS con soporte de módulos CommonJS y `fs`/`path` del
  core basta).
- **Sin dependencias de npm.** No hay `package.json`, no hay `node_modules`. Todo parseo (YAML,
  Markdown, frontmatter) está escrito a mano en `scripts/lib/` usando solo el standard library de
  Node (`fs`, `path`). Esto es deliberado: los validadores y builders deben poder ejecutarse en
  cualquier máquina con Node instalado, sin paso de instalación, sin lockfile, sin supply-chain de
  terceros.
- Cada script es un archivo ejecutable (`#!/usr/bin/env node`, `chmod +x`) invocable directamente:

  ```bash
  ./scripts/validate-chapter book/chapters/00-arquitectura-constitucion
  ./scripts/validate-contracts
  ./scripts/validate-components
  ./scripts/build-book-ir
  ./scripts/build-web
  ./scripts/build-pdf
  ./scripts/build-all        # pipeline end-to-end (Fase 7)
  ```

- Todos los scripts terminan con `process.exit(1)` ante cualquier error de validación estructural
  real (no simulado) y `process.exit(0)` si todo pasa, para que puedan encadenarse con `&&` en CI
  o en `build-all`.

## `scripts/lib/`

- `yaml-lite.js` — parser YAML de un subconjunto suficiente para los registries y el frontmatter
  de capítulos de este repo (mappings anidados por indentación, secuencias `- item`, listas en
  línea `[a, b, c]`, escalares con o sin comillas). No implementa YAML completo (no anchors, no
  multi-document, no tags) — es intencionalmente mínimo y auditable.
- `chapter-parser.js` — separa un `chapter.md` en frontmatter YAML + secciones Markdown (`##`) +
  bloques de pseudocódigo (` ```pseudocode `) para los validadores y para `build-book-ir`.
- `registries.js` — carga y valida el esquema mínimo de `registry/contracts.yaml`,
  `registry/components.yaml`, `registry/glossary.yaml` y `book/book.yaml`.

## Motor de PDF (decisión §8.2 del plan)

`build-pdf` invoca el binario `pandoc` ya instalado en el entorno (`pandoc 1.19.2.4`) con
`--latex-engine=xelatex` (sintaxis de pandoc < 2.0; nótese que NO es `--pdf-engine`, que solo
existe desde pandoc 2.x). `xelatex`/`pdflatex` están disponibles vía TeX Live
(`/Library/TeX/texbin/`). Sin diseño editorial todavía: portada mínima, TOC, capítulos, numeración
de página — suficiente para v0.1.
