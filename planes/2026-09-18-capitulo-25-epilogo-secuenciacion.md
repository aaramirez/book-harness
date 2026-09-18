# Plan / Registro de ejecución — Capítulo 25: Epílogo — El Orden que Nunca se Declaró en Prosa

**Fecha:** 2026-09-18
**Estado:** ✅ Completado, sobre el estado dejado por `95b879d` (CH-00..CH-24 como los veinticinco
únicos capítulos reales; sesenta y tres de sesenta y cuatro reglas constitucionales citadas con
código real — `P-09` señalada por el plan de CH-24 como la última pendiente, fuera de alcance de
ese capítulo por instrucción explícita).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-18-capitulo-23-handoff-coordinator.md` (identificó `P-07`/`P-09` como las dos últimas
  reglas sin citar)
- `2026-09-18-capitulo-24-skill-library.md` (cerró `P-07`; dejó `P-09` explícitamente pendiente y
  documentó la corrección metodológica de verificar cobertura por `frontmatter.
  constitutional_articles`, no por grep de texto libre — método heredado y reutilizado aquí)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Article I — `P-09`, línea 123; Article III —
  componentes de Article III, CH-00..CH-11; Amendment v1.1 — los nueve planos, CH-14..CH-24)

---

## 1. Objetivo

Escribir el vigesimosexto y ÚLTIMO capítulo planeado de este libro, CH-25 — un capítulo de
CIERRE/REFLEXIÓN, sin componente ni contrato nuevo (mismo patrón estructural que CH-12/CH-13), que
cierra la única regla de la Constitution sin ninguna cita real: `P-09` ("Single-agent reliability
precedes multi-agent complexity").

**Decisión de alcance (confirmada, no reabierta):** `P-09` no describe una responsabilidad que un
componente pueda `owns` — es una regla de secuenciación sobre CÓMO se construye el sistema
completo, no sobre QUÉ construye. Este capítulo NO inventa un componente para ella. En su lugar,
verifica con evidencia mecánica el hecho real y ya ocurrido de que este libro, en la práctica, ya
la cumplió: CH-00..CH-13 (los once componentes de Article III más los dos capítulos de integración,
catorce capítulos, cien por ciento single-agent) quedaron completos y validados ANTES de que CH-15
introdujera `AgentCommunicationGateway` (CMP-013) — la primera y única pieza multi-agente de todo
el libro.

## 2. Verificación de la premisa (antes de escribir), con el método correcto heredado de CH-24

Repetir el mismo grep de texto libre que CH-23/CH-24 ya identificaron como contaminado (P-09 aparece
como substring solo porque CH-23/CH-24 lo mencionan en prosa al documentar que quedaba pendiente).
Se usó, en su lugar, la señal estructurada — `frontmatter.constitutional_articles`, la misma fuente
que usa `scripts/validate-chapter` — sobre los veinticinco `chapter.md` anteriores a este capítulo:

```
$ node -e '
const fs = require("fs");
const path = require("path");
for (const d of fs.readdirSync("book/chapters")) {
  if (d === "00-arquitectura-constitucion") continue;
  const raw = fs.readFileSync(path.join("book/chapters", d, "chapter.md"), "utf8");
  const m = raw.match(/constitutional_articles:\s*\[([^\]]*)\]/);
  const ids = m ? m[1].split(",").map(s => s.trim()) : [];
  if (ids.includes("P-09")) console.log(d, ids);
}
'
(sin salida — CH-01..CH-24: ningún capítulo real declaró P-09 en su propio frontmatter)
```

Confirmado: `P-09` era, en efecto, la única de las sesenta y cuatro reglas sin ninguna cita real
antes de este capítulo.

## 3. Alcance de CH-25 (decisión ya tomada, ejecutada sin reabrirla)

- `introduces_components: []`, `introduces_contracts: []`, `modifies_contracts: []`.
- `constitutional_articles: [P-09, P-06, P-15]` — `P-09` como cita nueva y central; `P-06`
  ("Agents are configuration over a shared runtime") y `P-15` ("Automation and agents should share
  the same execution substrate") como refuerzo del mismo argumento aplicado también a los nueve
  planos de Amendment v1.1 (CH-14..CH-24, todos single-agent salvo CH-15).
- Contenido: reflexión de cierre sobre el ORDEN REAL de construcción del libro como evidencia de
  `P-09` (CH-00..CH-13 single-agent, completos y verificados antes de que CH-15 introdujera la
  primera pieza multi-agente) — verificado con scripts reales sobre `book/book.yaml` y
  `registry/components.yaml`, no afirmado en prosa. Amplía la reflexión hacia adelante: con los
  nueve planos de Amendment v1.1 ya completos (CH-14..CH-24), ¿qué le faltaría al libro para
  justificar agregar orquestación multi-agente real más allá de `AgentCommunicationGateway`? La
  seccion 18 del capítulo responde con la lista real y honesta de deuda de integración que
  CH-12..CH-24 ya dejaron documentada — mientras esa deuda esté abierta, `P-09` sugiere que el
  problema natural sigue siendo cerrarla, no agregar un componente de coordinación multi-agente.
- No se tocó ningún `book/chapters/00-*` a `23-*`. `book/chapters/24-skill-library/chapter.md`
  recibió únicamente el cambio de navegación permitido: `next_chapter: null → CH-25` (su cuerpo de
  prosa se dejó intacto, mismo tratamiento que CH-22 recibió de CH-23 y CH-23 de CH-24).
- `book/book.yaml`: CH-25 agregado después de CH-24, con `file: chapters/25-epilogo-secuenciacion/chapter.md`.
- `book/chapters/25-epilogo-secuenciacion/chapter.md`: `previous_chapter: CH-24`,
  `next_chapter: null` — el libro termina aquí, por decisión explícita del encargo.
- `registry/components.yaml` y `registry/contracts.yaml`: **sin cambios** — verificado
  (22 componentes, 35 contratos, idénticos antes y después de este capítulo).

## 4. Decisión de formato — adaptación de la estructura de 22 secciones a un capítulo reflexivo

Se siguió la misma estructura obligatoria de 19 secciones (`reference/md/
REGLAS_LIBRO_AGENT_HARNESS(1).md` §26) más las 3 secciones de cierre del método activo (§0 Preguntas
Guía, §20 Lente de Sistemas, §21 Practica lo que Aprendiste) — 22 secciones en total, exactamente
como CH-12/CH-13. La adaptación real, documentada explícitamente dentro del propio capítulo
(secciones 5-11):

- **Secciones 5, 6, 7 (New Concepts/Data Structures/Contracts)**: honestamente vacías de
  registro — introduce dos ideas narrativas sin ficha ("Secuencia verificable", "Regla sin ficha")
  que no se registran en `registry/glossary.yaml`, siguiendo el mismo patrón que CH-12 §5 ya
  estableció para sus propias ideas narrativas ("Camino Feliz", "Cierre de Cableado").
- **Sección 8 (Component Responsibilities)**: en vez de una ficha nueva, clasifica los veintidós
  componentes ya existentes contra `introduced_in` en "single-agent" (21) vs. "multi-agent" (1,
  `CMP-013`) — una lectura del registro ya existente, no una edición.
  Sección 9 (Dependency Relationships): confirma, sin editar ninguna ficha, que ningún componente
  anterior a CH-15 declara una dependencia hacia `CMP-013`.
- **Sección 10 (Sequence Diagram)**: en vez de una interacción en tiempo de ejecución entre
  componentes, muestra la secuencia de CAPÍTULOS del libro — con un script Node.js real (transcrito
  con su salida real, dentro de un bloque ` ```text` `, nunca ` ```pseudocode` `) que calcula el
  índice de `CH-15` dentro de `book/book.yaml` y lista los catorce capítulos estrictamente
  anteriores, verificando contra `introduced_in` que ninguno es `CMP-013`.
- **Sección 11 (Pseudocode)**: declarada explícitamente vacía de bloques ` ```pseudocode` ` — este
  capítulo no opera sobre entidades del dominio del arnés (no hay ningún `AgentState`/`ToolCall`
  que invocar), así que forzar un bloque de pseudocódigo habría sido, literalmente, una "magic
  entity" sin domicilio real. Se documenta por qué, en vez de rellenar la sección con algo
  artificial.
- **Sección 12 (State Transitions)**: no hay `AgentRunStatus` que transicionar; en su lugar,
  documenta el lifecycle real (no registrado como `ENUM`) de un capítulo de este libro
  (PLANEADO → ESCRITO → VALIDADO → CONSTRUIDO → PUBLICADO) y confirma que CH-00..CH-13 alcanzaron
  el último estado antes de que CH-15 alcanzara el primero.
- **Sección 13 (Failure Semantics)**: sin código de error nuevo; cumple el requisito de
  `scripts/validate-chapter` (mención literal de `ErrorCategory`/`HarnessError`) reflexionando sobre
  por qué introducir orquestación multi-agente antes de que `ErrorCategory` cubriera con
  confiabilidad los fallos de un solo agente multiplicaría el riesgo sin gobierno.
- **Sección 16 (Tests)**: los tres scripts reales ejecutados por este capítulo (cobertura
  estructurada, secuencia real, cobertura final de las 64 reglas) se documentan como los "tests
  arquitectónicos" de este capítulo — no hay ningún test funcional sobre el dominio del arnés
  porque este capítulo no describe ningún `AgentRun`.

Esta adaptación se decidió y documentó explícitamente, siguiendo la misma disciplina que CH-12/CH-13
ya aplicaron al desviarse del molde de "componente nuevo" — nunca forzando contenido artificial
para llenar una sección, y siempre declarando por qué una sección da un resultado vacío/distinto.

## 5. `retrieval_set` — decisión explícita

Sí se escribió un `retrieval_set` completo, adaptado: 4 `guiding_questions` de síntesis sobre TODO
el libro (no dependen de ninguna entidad nueva, porque este capítulo no introduce ninguna), 4
`recall_questions`, 2 `explain_prompts`, 3 `interleaved_questions` (contra CH-15/`CMP-013`,
CH-12/`CMP-001`, CH-24/`CMP-022` — las tres relaciones más relevantes para el argumento del
capítulo), 4 `flashcards` (con `source_entity` apuntando a componentes ya existentes, ya que este
capítulo no introduce ninguno propio — el chequeo [7] de `validate-retrieval-set` no exige nada aquí
porque `introduces_components`/`introduces_contracts` están vacíos), 4 `calibration_pairs`.

## 6. Verificación ejecutada (evidencia concreta)

```
./scripts/validate-chapter book/chapters/25-epilogo-secuenciacion       → OK a la primera
    (22/19 secciones, 0 bloques pseudocode, 0 contratos introducidos, 0 componentes introducidos)
./scripts/validate-retrieval-set book/chapters/25-epilogo-secuenciacion → OK
    (guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2, interleavedQuestions: 3,
    flashcards: 4, calibrationPairs: 4)
./scripts/validate-chapter book/chapters/24-skill-library               → OK (revalidado tras
    el único cambio de navegación permitido, next_chapter: CH-25)
./scripts/validate-retrieval-set book/chapters/24-skill-library         → OK (sin cambios en su
    propio retrieval_set — el cambio de navegación no lo afecta)
rm -rf dist && ./scripts/build-all                                       → exit 0
```

26 capítulos reales, todos pasando `validate-chapter`/`validate-retrieval-set` (revalidados los
26, uno por uno, tras el build). `build-mind-map`: `chapter-25.diagram` con 160 nodos/245 aristas
(1 nuevo nodo, 0 aristas nuevas respecto a `chapter-24.diagram`, 159 nodos/245 aristas) — consistente
con un capítulo que no introduce ningún componente ni contrato nuevo, pero sí agrega un nodo de
capítulo al mapa acumulativo.

**Web**: `dist/web/chapters/CH-25.html` existe. Navegación verificada en ambos sentidos:
`CH-24.html` contiene `href="CH-25.html"` (dos apariciones, header y footer); `CH-25.html` contiene
`href="CH-24.html"` (múltiples apariciones, incluidas anclas a `CMP-022`/`C-035`). `CH-25.html` no
tiene ningún link "Siguiente" hacia un capítulo posterior (no existe `CH-26.html`). `CH-00.html` y
el resto de capítulos previos permanecen intactos (verificado que `CH-00.html` sigue enlazando a
`CH-01`).

**PDF**: con `pypdf`, `dist/book.pdf` tiene **679 páginas** — más que el build de referencia de 25
capítulos (661 páginas) y más que el de 24 capítulos (631 páginas, CH-24). El texto extraído
contiene "P-09", "CH-15", "AgentCommunicationGateway", "Single-agent reliability" y "Epílogo" —
confirmando que el capítulo real (no solo su título) llegó al PDF construido.

**Verificación final de cobertura total (los 64 principios/invariantes)**, ejecutada contra la
misma señal estructurada que usa `scripts/validate-chapter` (`frontmatter.constitutional_articles`
de cada `chapter.md` real, vía `scripts/lib/registries.js#loadConstitutionArticleIds`, no un grep
de texto libre):

```
$ node -e '
const reg = require("./scripts/lib/registries.js");
const fs = require("fs");
const path = require("path");
const ids = reg.loadConstitutionArticleIds();
const cited = new Set();
const perChapter = {};
for (const d of fs.readdirSync("book/chapters").sort()) {
  const cf = path.join("book/chapters", d, "chapter.md");
  if (!fs.existsSync(cf)) continue;
  const raw = fs.readFileSync(cf, "utf8");
  const idm = raw.match(/^id:\s*(CH-\d+)/m);
  const cam = raw.match(/constitutional_articles:\s*\[([^\]]*)\]/);
  const cids = cam ? cam[1].split(",").map(s => s.trim()).filter(Boolean) : [];
  perChapter[idm ? idm[1] : d] = cids;
  for (const id of cids) cited.add(id);
}
const missing = [...ids].filter(r => !cited.has(r)).sort();
console.log("Reglas totales en la Constitution:", ids.size);
console.log("Reglas citadas por >=1 capitulo real:", cited.size);
console.log("Faltantes:", missing.length ? missing.join(", ") : "NINGUNA -- 64/64 cubiertas");
console.log("P-09 citado por capitulos reales (excluyendo CH-00, transcripcion):",
  Object.entries(perChapter).filter(([ch, cids]) => ch !== "CH-00" && cids.includes("P-09")).map(([ch]) => ch));
'
Reglas totales en la Constitution: 64
Reglas citadas por >=1 capitulo real: 64
Faltantes: NINGUNA -- 64/64 cubiertas
P-09 citado por capitulos reales (excluyendo CH-00, transcripcion): [ 'CH-25' ]
```

**64/64 reglas de la Constitution (`P-01`..`P-30`, `INV-01`..`INV-20`, `INV-E01`..`INV-E14`) tienen,
después de este capítulo, al menos un capítulo real (`CH-00`..`CH-25`) que las cita con código en su
propio `frontmatter.constitutional_articles`.** `P-09` deja de ser la excepción documentada desde
CH-23/CH-24 y queda cerrada, honestamente, por este capítulo — no inventando un componente, sino
verificando con evidencia mecánica el hecho real del orden en que el libro se escribió.

`registry/components.yaml`/`registry/contracts.yaml` permanecen, después de este capítulo,
exactamente en 22 componentes / 35 contratos — sin ningún cambio, confirmado con `git status`.

## 7. Decisiones de diseño no cubiertas en el encargo original

- **Título**: "Epílogo: El Orden que Nunca se Declaró en Prosa" — combina ambas sugerencias del
  encargo. Preferido sobre "Lo Que Este Libro Ya Demostró Sin Decirlo" por ser más específico sobre
  QUÉ se demostró (un orden, no una capacidad genérica) y por evitar la ambigüedad de "ya
  demostró" (¿demostró qué, exactamente?).
- **Slug**: `25-epilogo-secuenciacion` — corto, sigue la convención `NN-slug-descriptivo` del resto
  del libro, y nombra el eje real del capítulo (secuenciación) sin repetir el título completo.
- **`constitutional_articles: [P-09, P-06, P-15]`** en vez de solo `[P-09]`: se decidió reforzar la
  cita central con dos principios ya citados por CH-00 (`P-06`, `P-15`) que explican POR QUÉ los
  nueve planos de Amendment v1.1 (CH-14..CH-24) también sostuvieron `P-09` — no solo el Tramo 1
  (CH-00..CH-13). Se evaluó y descartó agregar `INV-E03`..`INV-E06` (invariantes de comunicación
  entre agentes, ya citados por CH-15): habría diluido el foco del capítulo, que es sobre el ORDEN,
  no sobre el contenido de `AgentCommunicationGateway` en sí.
- **Sin pseudocódigo registrado**: decisión explícita, documentada dentro del propio capítulo
  (seccion 11), de no forzar un bloque ` ```pseudocode` ` — la disciplina "no magic entities"
  aplicada a la propia decisión editorial de este capítulo.
- **`introduces_components`/`introduces_contracts` vacíos, confirmados sin ambigüedad**: a
  diferencia de CH-24 (que evaluó y descartó extender `ErrorCategory`), este capítulo ni siquiera
  evalúa extender ningún registro — la naturaleza de `P-09` (regla de secuenciación, no de
  responsabilidad) hace que esa pregunta ni se plantee con seriedad.

## 8. Deuda intencional heredada, no resuelta por este capítulo (y por qué no)

Este capítulo es deliberadamente el último planeado — no deja, por diseño, un "problema natural del
siguiente incremento" (seccion 19 del propio capítulo lo documenta explícitamente). La deuda real
que sí queda, para quien continúe este libro más allá de su alcance planeado, es exactamente la
misma que CH-12..CH-24 ya documentaron cada uno en su propia sección 18 — listada, junta por
primera vez, en la sección 18 de este capítulo: los puntos de cableado real entre los nueve
componentes de Amendment v1.1, el mecanismo real de registro/alta de capabilities/skills/políticas,
la certificación real de un candidato por `EvaluationHarness`, el handoff humano real de
`HandoffCoordinator`, y la ejecución real de lo que una skill resuelta describe. Este capítulo no
resuelve ninguno de esos puntos — los usa, honestamente, como la respuesta real a "¿qué le falta al
libro para justificar más complejidad multi-agente?": cerrarlos primero, según `P-09`.

## 9. Nota de cierre — 64/64

Con CH-25, las sesenta y cuatro reglas de la Constitution (`P-01`..`P-30`, `INV-01`..`INV-20`,
`INV-E01`..`INV-E14`) quedan, cada una, citadas con código real por al menos un capítulo de este
libro — verificado en la seccion 6 con la misma señal estructurada que usa
`scripts/validate-chapter`, no con una afirmación de prosa. Este es el vigesimosexto y último
capítulo planeado de BH-v0.1.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
