# Plan — Arranque de "IA en la Empresa" (nuevo proyecto, `iaenlaempresa/`)

**Fecha:** 2026-09-08 (aprobado y ejecutado 2026-09-09)
**Estado:** ✅ Ejecutado — ver `iaenlaempresa/plans/0001-mvp-pipeline.md` para el registro completo
de qué se hizo realmente (incluida la paleta real extraída del logo/banner del canal, provista por
el usuario durante la ejecución — no la propuesta placeholder de la sección 2 de este documento).

---

## 0. Qué se revisó para este plan

- `book-harness/planes/2026-08-23-book-harness-como-construir-un-arnes.md` +
  `2026-08-24-mapa-mental-progresivo.md` + `2026-08-23-metodo-aprendizaje-activo-lector.md`:
  son el plan de **otro libro** ("Construyendo un Agent Harness" / repo `arnes-kb`), mucho más
  ambicioso (harness editorial gobernado, agentes/skills/validadores, salida Web+PDF sincronizada).
  Confirmado con el usuario: **no es esto** — queda intacto, sin tocar.
- `book-harness/reference/conversacion/*.md` (28 archivos, ~12k líneas): transcripción de una
  conversación sobre arquitectura de un "agent harness" tipo Pi (`pi-ai`/`pi-agent-core`/
  `pi-coding-agent`) — es la fuente de ESE otro libro, no de este.
- `book-harness/reference/metodo_estudio_harvard.md` + `domina_cualquier_tema_ia.md`: transcripciones
  de video sobre técnicas de estudio (método de las 5 Rs de Harvard, Dinámica de Sistemas del MIT
  aplicada con IA) — genéricas, no atadas a ningún libro puntual. Quedan como posible inspiración
  pedagógica a futuro (ver "Fuera de alcance"), no se adoptan automáticamente acá.
- `~/Downloads/iaenlaempresa-content/` — **la fuente real de este libro**:
  - 3 whitepapers de OpenAI (inglés, sin TOC embebido pero con página de contenidos como texto):
    - `ai-in-the-enterprise.pdf` (25p) — "AI in the Enterprise: Lessons from seven frontier
      companies". Estructura: intro + 7 lecciones (Start with evals / Embed AI into your products /
      Start now and invest early / Customize and fine-tune your models / Get AI in the hands of
      experts / Unblock your developers / Set bold automation goals) + conclusión + recursos.
    - `a-practical-guide-to-building-agents.pdf` (34p) — qué es un agente, cuándo construir uno,
      fundamentos de diseño, guardrails, conclusión.
    - `identifying-and-scaling-ai-use-cases.pdf` (34p) — cómo identificar y priorizar casos de uso
      de IA por departamento; "seis primitivos de casos de uso"; mapeo de flujos de trabajo.
  - `images and videos/` — 59 imágenes fijas usables en un PDF impreso (23 jpeg + 36 png, arte
    generado por IA: agentes, oficinas, ciudades, contexto/prompting, automatización...) + 77 mp4
    (video — **no sirven en un libro impreso**, ver "Fuera de alcance").
  - `audios/` — 15 `.wav` (tampoco sirven en un PDF).
  - Título de trabajo: **"IA en la Empresa"** (nombre de carpeta) — subtítulo propuesto abajo, a
    confirmar con el usuario.

## 1. Decisión de arquitectura (confirmada con el usuario)

- **Proyecto nuevo e independiente**: `iaenlaempresa/`, repo git propio (como
  `libro-de-panaderia/`, que ya convive como directorio hermano dentro de `book-harness/` sin ser
  parte del repo raíz de `book-harness`). NO es un libro dentro del sistema multi-libro de
  `libro-de-panaderia` (no vive en `libro-de-panaderia/books/`).
- **Mismo stack, confirmado por el usuario**: Markdown (front-matter YAML) + Jinja2 + WeasyPrint →
  PDF, mismo target físico KDP 8.5x11in. Se **copia y adapta** el pipeline ya probado de
  `libro-de-panaderia` (`scripts/lib/*.py` es 100% agnóstico de contenido — KDP specs, ensamblado,
  numeración, QC — no necesita reescribirse, solo copiarse) — no se comparte código en vivo entre
  los dos repos (son independientes), se parte de una copia.
- **Arquitectura de componentes desde el día uno** (no evolucionar hacia ella como en
  `libro-de-panaderia`, ya aprendimos que vale la pena): `layouts/components/` +
  `styles/components/` + un libro/catálogo de componentes desde el arranque, no al final.

## 2. Identidad visual — propuesta a confirmar

Contenido de negocio/adopción de IA para gerencia y equipos técnicos, NO un recetario — la paleta
cálida de panadería y el slab display juguetón de `libro-de-panaderia` no encajan. Propuesta:

- **Paleta**: tema "tech/corporativo" — tinta casi negra azulada (`ink: #14161c`), papel frío casi
  blanco (`paper: #f6f7fa`, nunca blanco puro), acento **índigo/violeta** (`#4f46e5`-ish) como
  color de marca de IA (evita el azul genérico "corporate" y el verde genérico "tech-startup"),
  con un segundo acento (ámbar/naranja) para callouts de estadística — el mismo patrón de
  acento-primario + acento-secundario-utilitario que ya usa `libro-de-panaderia`
  (`--accent`/`--color-herb`), no un sistema nuevo.
- **Tipografía**: display sans geométrico (candidato: Montserrat, ya está en
  `libro-de-panaderia/assets/fonts/` — se copiaría el archivo) para títulos grandes, + una segunda
  familia para cuerpo/labels (candidato: Poppins, también ya disponible) — **a confirmar**: ¿copiar
  fuentes ya presentes en `libro-de-panaderia/assets/fonts/` (Poppins/Montserrat/Lora/Alfa Slab
  One) o conseguir tipografía nueva? Copiar es más rápido y ya sabemos que renderizan bien en
  WeasyPrint; conseguir nueva da identidad más distintiva pero agrega trabajo de curaduría de
  licencias/archivos.
- **Título/subtítulo de trabajo**: "IA en la Empresa" / "Cómo adoptar Inteligencia Artificial sin
  perderte en el hype" (subtítulo placeholder, a confirmar o reemplazar).

## 3. Familias de layout y componentes propuestos (adaptados del inventario de recetas)

Reutilizando el patrón ya probado (una plantilla Jinja2 por familia + variantes CSS, componentes
en `layouts/components/`), adaptado al contenido:

**Familias de página** (equivalentes a `frontmatter/`, `chapter/`, `recipe/`, `gallery/`,
`backmatter/` de libro-de-panaderia):
- `frontmatter/*` — título, copyright, dedicatoria, TOC: **se reutilizan casi sin cambios**
  (genéricos, no específicos de recetas).
- `chapter/opener` — divisor de capítulo a sangre completa: **se reutiliza el mecanismo**, solo
  cambian las fotos (usar las imágenes generadas de `images and videos/` en vez de fotos de pan).
- `insight/*` (reemplaza `recipe/*`) — la página de contenido principal: una "lección" (de las 7 de
  AI-in-the-Enterprise), un "caso de uso" (de los 6 primitivos), o un patrón de diseño de agente
  (de la guía de agentes). Variantes análogas a photo-right/photo-top/no-photo.
- `gallery/mosaic` — **se reutiliza tal cual** (2 a 7 fotos a sangre completa, ya soporta
  cualquier conteo) — encaja perfecto con las 59 imágenes generadas disponibles.
- `backmatter/simple` — se reutiliza sin cambios (glosario de términos de IA, recursos, etc.).

**Componentes nuevos** (en `layouts/components/`, análogos a los de plan 0011 pero para este
contenido):
- `big_stat` — callout numérico grande (ej. "39%", "1.5x", "1%" de `identifying-and-scaling-ai-
  use-cases.pdf` p.2) + caption corta. No existe en `libro-de-panaderia` (los `stat_chip` son
  chips chicos tipo ficha técnica) — este es un elemento tipográfico grande, protagonista de
  página, más parecido a una portada de dato que a un chip.
- `lesson_card` (análogo a `step_card`, pero para una lección/primitivo de caso de uso en vez de un
  paso de receta): número + título + descripción, sin foto obligatoria.
- `customer_quote` (variante de `pull_quote`): cita + empresa/rol atribuido, para las historias de
  clientes que traen los 3 whitepapers.
- `checklist` (variante de `tip_box`): lista con marca de check en vez de bullet simple, para los
  "practical checklists" que menciona `identifying-and-scaling-ai-use-cases.pdf`.
- `stat_chip_row`/`meta_list`/`formula_table`/`toc_entries`/`kicker`: se reutilizan tal cual desde
  `libro-de-panaderia` (son genéricos) — `formula_table` probablemente no aplica a este contenido
  (no hay "fórmulas"), se deja disponible pero no se usa.

## 4. Contenido: curaduría manual desde los 3 whitepapers, NO ingesta automática

A diferencia del repo Jekyll de `libro-de-panaderia` (Markdown ya limpio, extracción confiable),
estos son PDFs de diseño (columnas, callouts, iconos) — extraer texto con PyMuPDF da texto plano
sin estructura fiable. Se propone: **curaduría manual** — leer cada whitepaper, traducir/adaptar al
español, y escribir el Markdown + front-matter directamente contra el schema de `insight/*`, igual
que ya se cura cada receta real de `libro-de-panaderia` a mano. Un script de ingesta automática NO
se justifica para 3 documentos de este tamaño (93 páginas totales, una sola vez).

## 5. Pasos

1. `iaenlaempresa/` — copiar de `libro-de-panaderia`: `scripts/lib/*.py` (sin
   cambios, es agnóstico de contenido), `scripts/build.py` (sin cambios), `Makefile`,
   `pyproject.toml`, `layouts/base.html` + `layouts/partials/page-rules.html` (sin cambios),
   `styles/tokens.css` + `styles/page-setup.css` + `styles/full-bleed.css` (estructurales, sin
   cambios), `config/kdp_specs.yaml` (sin cambios, son reglas de KDP no del libro). `git init`
   propio.
2. `config/book.yaml` (o `books/iaenlaempresa/config/book.yaml` si de entrada se decide dejarlo
   multi-libro-ready — a definir) con el `theme:` de la sección 2, título/subtítulo confirmados.
3. Copiar fuentes elegidas (sección 2) a `assets/fonts/`.
4. `layouts/frontmatter/*`, `layouts/chapter/opener.html`, `layouts/gallery/mosaic.html`,
   `layouts/backmatter/simple.html` — copiar tal cual desde `libro-de-panaderia` (genéricos).
5. `layouts/components/{titles,cards,lists,tables,icons}.html` + `styles/components/*.css` —
   copiar los genéricos (`kicker`, `meta_list`, `toc_entries`, `pull_quote`→base de
   `customer_quote`, `tip_box`→base de `checklist`) y crear los nuevos (`big_stat`, `lesson_card`,
   `customer_quote`, `checklist`).
6. `layouts/insight/*.html` + `styles/layouts/insight.css` — nueva familia, adaptando el patrón de
   `recipe/recipe.html` (stats/meta arriba, cuerpo, cards, quote, checklist).
7. `gallery/*.md` — fixture de layouts completos (como en `libro-de-panaderia`), con datos de
   muestra en español, usando 3-4 imágenes reales de `images and videos/` ya copiadas a
   `assets/images/`.
8. `books-catalogo` — libro/fixture de catálogo de componentes desde el arranque (no al final como
   en plan 0011), con tema neutro propio, mostrando `big_stat`/`lesson_card`/`customer_quote`/
   `checklist` además de los reutilizados.
9. Curar a mano 2-3 páginas de contenido REAL (ej. "Empieza con evaluaciones" de las 7 lecciones,
   un caso de uso de los 6 primitivos) como piloto — validar que el schema de `insight/*` alcanza
   antes de curar el resto de las 93 páginas de fuente.
10. `tests/` — copiar los tests agnósticos de contenido (`test_pagecount_thresholds.py`,
    `test_spine_formula.py`, `test_numbering.py`, `test_structural_gap.py`, `test_theme.py`,
    `test_components.py`) tal cual; ajustar solo lo que referencie "pan-venezolano"/rutas.
11. `README.md` + `.claude/skills/` propios (adaptar `panaderia-book-layout` a un
    `iaenlaempresa-book-layout` con la paleta/tipografía/componentes reales de este libro).

## 6. Verificación

- `make install` + `make test` en verde con el pipeline copiado, sin contenido real todavía.
- `scripts.build gallery` produce un PDF con los layouts de muestra, tema nuevo aplicado.
- El libro/catálogo de componentes construye limpio, QC en verde.
- Las 2-3 páginas piloto de contenido real (paso 9) construyen y se ven bien — validación de que
  el schema de `insight/*` alcanza antes de invertir en curar el resto.

## 7. Fuera de alcance (de este plan)

- **Video/audio de `Downloads/iaenlaempresa-content/`**: no entran en un PDF impreso. Si en algún
  momento se quiere un producto complementario (curso web, video) es un proyecto aparte, no este.
- **Curar las 93 páginas completas** de los 3 whitepapers a contenido `status: ready` — este plan
  solo llega a un piloto (paso 9); el resto es trabajo de curaduría posterior, receta por receta
  (o "lección por lección"), igual que en `libro-de-panaderia`.
- **Técnicas pedagógicas de `reference/metodo_estudio_harvard.md`/`domina_cualquier_tema_ia.md`**
  (método de las 5 Rs, dinámica de sistemas) como componentes/estructura del libro — quedan como
  inspiración a evaluar en un plan aparte si el usuario quiere que el libro enseñe usando esas
  técnicas explícitamente (ej. un componente "pregúntate esto antes de leer", checkpoints estilo
  Feynman) — no se asume que aplican solo porque están en `book-harness/reference/`.
- **Publicar a KDP de verdad**: portada final, ISBN, etc. — ni siquiera aplica todavía sin
  contenido real curado.

## 8. Decisiones que el usuario debe confirmar antes de ejecutar

1. ¿Subtítulo real del libro (o se define después de curar más contenido)?
2. ¿Paleta/tipografía propuestas en la sección 2, o prefieres otra dirección?
3. ¿Copiar fuentes ya existentes en `libro-de-panaderia/assets/fonts/` o conseguir tipografía
   nueva para este libro?
4. ¿El repo va en español (como `libro-de-panaderia`) — títulos de componentes, comentarios, todo
   en español — asumo que sí por continuidad, confirmar?
