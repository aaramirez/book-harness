# Plan / Registro de ejecución — Capítulo 24: SkillLibrary y el Conocimiento Procedural que Nunca Fue una Capability

**Fecha:** 2026-09-18
**Estado:** ✅ Completado, sobre el estado dejado por `466431b` (CH-00..CH-23 como los veinticuatro
únicos capítulos reales; sesenta y dos de sesenta y cuatro reglas constitucionales citadas con
código real — `P-07` y `P-09` señaladas por el plan de CH-23 como las dos últimas pendientes).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-18-capitulo-23-handoff-coordinator.md` (precedente inmediato: identificó `P-07`/`P-09`
  como las dos últimas reglas sin citar, sin resolverlas — encargo directo de este capítulo)
- `2026-09-13-capitulo-08-capability-registry.md` (`CapabilityDescriptor`/`CapabilityRegistry`, la
  frontera más importante a trazar contra el componente/contrato de este capítulo)
- `2026-09-14-capitulo-11-agent-core.md` (`AgentCore`/`AgentConfig`, la separación de identidad que
  `P-07` exige)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Article I — `P-07`, línea 115)

---

## 1. Objetivo

Escribir el vigesimoquinto capítulo real de contenido del libro, CH-24 — el undécimo componente de
este registry que no corresponde a ninguno de los once nombres de Article III, y el que cierra
`P-07` ("Skills encode reusable procedural knowledge"), una de las dos últimas reglas de la
Constitution que el plan de ejecución de CH-23 había señalado sin ninguna cita real. `P-09`
("Single-agent reliability precedes multi-agent complexity") — un principio de secuenciación
arquitectónica de todo el libro, no un componente — queda, deliberadamente, fuera del alcance de
este capítulo por instrucción explícita del encargo: una decisión editorial distinta, que otra
sesión tomará después.

**Verificación de la premisa, ejecutada antes de escribir una sola línea del capítulo, y corregida
respecto al método de CH-23**: el propio plan de CH-23 verificó la ausencia de cita de `P-07`/`P-09`
con un grep de texto completo sobre los veintitrés `chapter.md` anteriores a CH-23. Repetir
literalmente ese mismo método sobre los veinticuatro `chapter.md` anteriores a CH-24 (CH-00..CH-23)
da un resultado **vacío** — no porque `P-07`/`P-09` ya estuvieran citados con código real, sino
porque CH-23 mismo menciona ambos nombres en prosa (§4/§17/§19) al **documentar que quedaban sin
resolver** — una contaminación del propio método de verificación por la meta-discusión de un
capítulo anterior sobre el mismo hallazgo:

```text
$ python3 - <<'EOF'
import re, glob
expected = ['P-07','P-09']
full_text = ""
for c in sorted(glob.glob('book/chapters/*/chapter.md')):
    if '00-arquitectura-constitucion' in c:
        continue
    full_text += open(c, encoding='utf-8').read()
cited = set(re.findall(r'\b(?:P-\d{2}|INV-E\d{2}|INV-\d{2})\b', full_text))
print(sorted(set(expected) - cited))
EOF
[]   # <- vacío: P-07/P-09 SÍ aparecen como substring en el texto completo, pero solo porque CH-23
     #    los menciona en prosa al documentar que no estaban cerrados, no porque los cite con owns
```

Se corrigió el método: en vez de un grep de texto libre, se verificó contra el campo estructurado
`frontmatter.constitutional_articles` de cada capítulo — la misma señal que `scripts/validate-chapter`
usa como fuente de verdad para lo que un capítulo declara citar realmente — y, adicionalmente, contra
el contenido de la sección 4 (Impacto Constitucional) buscando un formato de cita real (encabezado de
bullet tipo `    P-13   Authorization is...`) en vez de una mención de nombre en prosa:

```text
$ node -e '
const fs = require("fs");
const path = require("path");
for (const d of fs.readdirSync("book/chapters")) {
  if (d === "00-arquitectura-constitucion") continue;
  const raw = fs.readFileSync(path.join("book/chapters", d, "chapter.md"), "utf8");
  const m = raw.match(/constitutional_articles:\s*\[([^\]]*)\]/);
  const ids = m ? m[1].split(",").map(s => s.trim()) : [];
  if (ids.includes("P-07") || ids.includes("P-09")) console.log(d, ids);
}
'
(sin salida — CH-01..CH-23: ningún capítulo real declaró P-07 ni P-09 en su propio frontmatter)

$ grep -n "^    P-07\|^    P-09" book/chapters/*/chapter.md | grep -v "00-arquitectura"
(sin salida — ningún capítulo tiene un bullet de cita real tipo "Principles preserved" para P-07/P-09)
```

Ambos comandos confirman, con la señal correcta, la premisa heredada de CH-23: `P-07` y `P-09` eran,
en efecto, las únicas dos reglas de la Constitution sin ninguna cita real fuera de la transcripción
de CH-00. Este hallazgo metodológico (que un grep de texto completo puede contaminarse por la propia
meta-discusión de un capítulo anterior sobre un hallazgo de cobertura) se documenta explícitamente en
la apertura del propio capítulo y en su sección 17/19, con el mismo rigor que CH-22/CH-23 ya
aplicaron a sus propios hallazgos de cobertura.

## 2. Alcance (decisión ya tomada antes de escribir, confirmada en el resultado)

Exactamente **1 componente + 1 contrato**, tal como especificó el encargo:

1. **`SkillLibrary`** (`CMP-022`) — evaluado contra dos alternativas de nombre:
   - `SkillRegistry`: descartado porque el nombre "Registry", ya usado literalmente por
     `CapabilityRegistry` (CMP-008, CH-08), invitaría a leer ambos componentes como la misma clase de
     mecanismo con distinto sustantivo — exactamente el riesgo de conflación que este capítulo existe
     para prevenir (P-07 exige una SEPARACIÓN, no un paralelismo de nombres que sugiera
     intercambiabilidad).
   - `ProceduralKnowledgeBase`: descartado por ser una traducción demasiado literal del texto de
     `P-07` que no sigue la convención de nombres de una palabra/sustantivo compuesto corto ya
     establecida por el resto del libro (`Coordinator`, `Gateway`, `Engine`, `Broker`, `Guard`,
     `Controller`, `Adapter`, `Harness`) — un nombre correcto pero pedagógicamente más pesado que sus
     pares.
   - **Elegido: `SkillLibrary`** — evoca literalmente "una biblioteca de conocimiento procedural
     reusable" (cita de P-07: "reusable procedural knowledge"), es gramaticalmente distinto de
     "Registry" (evita la lectura de intercambiabilidad con `CapabilityRegistry`) y sigue la
     convención de nombres cortos de un sustantivo del resto del libro.
   `owns`: registrar el descriptor de una skill (conocimiento procedural reusable) como una capa
   separada del core (`AgentCore`, CH-11), de las tools/capabilities (`CapabilityRegistry`/
   `ToolRuntime`, CH-08/CH-02) y de la identidad del agente (`AgentConfig`, CH-00) — cita literal de
   `P-07`; resolver, contra ese registro, qué `SkillDescriptor` aplica a una situación nombrada;
   fail-closed sobre una resolución sin `situationName` real o sin coincidencia registrada.
   `does_not_own` (frontera trazada contra cinco componentes ya existentes): resolver qué
   implementación concreta satisface una capability solicitada (`CapabilityRegistry`, CMP-008, CH-08
   — LA FRONTERA MÁS IMPORTANTE); representar la identidad/configuración de un agente (`AgentCore`,
   CMP-011, CH-11); ejecutar el side effect en sí de ninguna acción (`ToolRuntime`, CMP-002, CH-02);
   decidir autorización sobre ninguna acción (`PolicyEngine`, CMP-005, CH-05); certificar un
   candidato de skill antes de su promoción a producción (`EvaluationHarness`, CMP-020, CH-22 — que
   ya declara evaluable, entre otros candidatos, a una skill antes de su promoción).
2. **`SkillDescriptor`** (`C-035`) — `skill` (`SkillId`, identificador ya resuelto, mismo patrón que
   `capability: CapabilityId` en `CapabilityDescriptor`), `name` (`Text`, nombre canónico), `version`
   (`Text`, reusa el mismo criterio de versionado que `CapabilityDescriptor`/`P-26`, sin que `P-26`
   en sí — literalmente sobre "Tools/capabilities" — se extienda a skills), `procedureRef` (`Text`,
   referencia opaca al procedimiento/guía real, mismo patrón que `implementationRef`), `appliesTo`
   (`Optional<Text>`, referencia opaca y opcional a qué capabilities/situaciones aplica — se evaluó
   explícitamente `List<CapabilityId>` y se descartó por modelar una relación estructurada fuera de
   alcance). Deliberadamente con la misma forma de cinco campos que `CapabilityDescriptor` (C-018,
   CH-08) — para hacer el contraste legible, nunca para sugerir que son el mismo concepto.
3. **Pseudocódigo**: `resolveSkillForSituation(...)` — autónomo, fail-closed hacia
   `SKILL_RESOLUTION_REQUESTED_WITHOUT_SITUATION` y `SKILL_NOT_FOUND`, contrastado explícitamente en
   prosa contra `resolveToolCall` (CH-08 §11): una skill resuelta es siempre una referencia
   consultable, nunca una acción — nunca pasa por `PolicyEngine.evaluate` ni por
   `ToolRuntime.execute`. Documentado en prosa que ningún componente anterior invoca todavía esta
   función.
4. No se tocó ningún `book/chapters/00-*` a `22-*`. `book/chapters/23-handoff-coordinator/chapter.md`
   recibió únicamente el cambio de navegación permitido: `next_chapter: null → CH-24` (su cuerpo de
   prosa, incluida la frase "`next_chapter` queda en `null`...", se dejó intacta — mismo tratamiento
   exacto que CH-22 recibió de CH-23, verificado contra el propio archivo de CH-22 antes de aplicar
   el mismo patrón aquí).
5. `book/book.yaml`: CH-24 agregado después de CH-23. `previous_chapter: CH-23`, `next_chapter: null`
   en el frontmatter de CH-24 (no existe todavía ningún CH-25).
6. `retrieval_set` de CH-24: 4 `guidingQuestions`/`recallQuestions`, 2 `explainPrompts`, 2
   `interleavedQuestions` (CH-08 sobre la frontera con `CapabilityRegistry`/`CapabilityDescriptor` —
   la más importante; CH-11 sobre la separación de identidad con `AgentCore`/`AgentConfig`), 5
   `flashcards`, 4 `calibrationPairs`.

## 3. Decisión deliberada: ErrorCategory NO se extiende en este capítulo

A diferencia de la mayoría de los componentes de Amendment v1.1 (CH-14..CH-23), que agregaron cada
uno un valor nuevo a `ErrorCategory`, este capítulo evaluó explícitamente agregar un valor `SKILL` —
y lo descartó, siguiendo en cambio el precedente que `CapabilityRegistry` (CH-08 §13) ya sentó para
su propio `CAPABILITY_NOT_FOUND`: un `situationName` ausente o sin coincidencia es un fallo de
validación de la *entrada*, no de una *ejecución*; introducir una categoría nueva solo para
distinguir "quién" detectó el problema fragmentaría `ErrorCategory` sin ganancia semántica real.
`ErrorCategory` sigue teniendo, después de CH-24, exactamente los mismos veintiún valores que dejó
CH-23. Verificado explícitamente que esta decisión no rompe INV-20 (todo error operacional pertenece
a una categoría CONOCIDA — VALIDATION ya existe desde CH-00, no se necesita una nueva).

## 4. Gotcha de `scripts/lib/yaml-lite.js` — verificado, sin repetirlo esta vez

Antes de escribir cualquier entrada nueva en `registry/components.yaml`/`registry/contracts.yaml`,
se releyó `scripts/lib/yaml-lite.js` completo y el hallazgo documentado en
`planes/2026-09-18-capitulo-23-handoff-coordinator.md` §3: cada item de una secuencia (`owns:`/
`does_not_own:`) debe ser una única línea física completa, sin importar su longitud — una
continuación indentada en la línea siguiente rompe `parseSequence`/`parseMapping` de forma
silenciosa y engañosa. Todas las entradas de `owns`/`does_not_own` de `CMP-022` (siete items en
total) se escribieron, desde el primer intento, como una sola línea física cada una. Confirmado con
`./scripts/validate-components` → `OK (22 componente(s))` a la primera, sin ningún error de campos
faltantes.

## 5. Gotcha revisado y NO modificado: `scripts/lib/render-diagram.js`

Se releyó el archivo completo (fix de Ghostscript documentado en su propio encabezado, línea ~38-61)
antes de empezar. No se encontró ningún problema real que justificara modificarlo — el build de PDF
de este capítulo (seccion 6) no reveló ninguna regresión relacionada.

## 6. Verificación ejecutada (evidencia concreta)

```
./scripts/validate-contracts                                             → OK (35 contratos)
./scripts/validate-components                                            → OK (22 componentes)
./scripts/validate-chapter book/chapters/24-skill-library                → OK a la primera
    (22/19 secciones, 4 bloques pseudocode, 1 contrato introducido, 1 componente introducido)
./scripts/validate-retrieval-set book/chapters/24-skill-library           → OK
    (guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2, interleavedQuestions: 2,
    flashcards: 5, calibrationPairs: 4)
./scripts/validate-chapter book/chapters/23-handoff-coordinator          → OK (revalidado tras
    el único cambio de navegación permitido, next_chapter: CH-24)
./scripts/validate-retrieval-set book/chapters/23-handoff-coordinator    → OK (sin cambios en su
    propio retrieval_set — el cambio de navegación no lo afecta)
rm -rf dist && ./scripts/build-all                                        → exit 0
```

25 capítulos reales, todos pasando `validate-chapter`/`validate-retrieval-set`. `build-mind-map`:
`chapter-24.diagram` con 159 nodos/245 aristas — más que `chapter-23.diagram` (154 nodos/237
aristas), como exige la verificación.

**Web**: `dist/web/chapters/CH-24.html` con SVG inline, anchors `id="CMP-022"`/`id="C-035"`
presentes, navegación CH-23↔CH-24 verificada en ambos sentidos. CH-00..CH-23 no se rompieron (mismos
anchors clave verificados en las 25 páginas).

**PDF**: con `pypdf`, más páginas que el build de referencia de 24 capítulos (631 páginas). Texto
extraído contiene "SkillLibrary" y "SkillDescriptor".

**Prueba negativa real**: se rompió deliberadamente un campo obligatorio de `CMP-022` en
`registry/components.yaml`, se confirmó `exit 1` real (verificado con `$?` inmediatamente después,
no inferido de un pipe) y el mensaje de error exacto señalando el campo faltante; se restauró el
campo y se reconstruyó todo desde cero, confirmando conteos idénticos al build previo a la prueba.

## 7. Decisiones de diseño no cubiertas en el encargo original

- **Nombre del componente y del contrato** (ver seccion 2, punto 1) — `SkillLibrary` sobre
  `SkillRegistry`/`ProceduralKnowledgeBase`; `SkillDescriptor` (no `Skill` a secas, ni `SkillRecord`)
  para seguir la misma disciplina de nombres que ya distinguió `CapabilityDescriptor` de
  "Capability" (CH-02/CH-08).
- **`ErrorCategory` sin extender** (ver seccion 3): decisión explícita de reusar `VALIDATION` en vez
  de agregar `SKILL`, rompiendo el patrón (no la regla) que la mayoría de Amendment v1.1 siguió.
- **`SkillDescriptor.appliesTo` como `Optional<Text>` opaco, no `List<CapabilityId>`**: evaluado y
  descartado explícitamente por modelar una relación estructurada fuera del alcance decidido.
- **`version` reusa el criterio de `P-26` sin citar `P-26` como impacto constitucional propio**:
  `P-26` es, literalmente, sobre "Tools/capabilities" — extender su cita a `SkillDescriptor` habría
  sido una sobre-extensión no autorizada por el texto constitucional; se documentó como reuso de
  criterio de ingeniería, no como cita nueva.
- **Corrección metodológica sobre el barrido de cobertura de CH-23** (ver seccion 1): un grep de
  texto completo sobre capítulos reales puede contaminarse por la propia meta-discusión de un
  capítulo anterior sobre un hallazgo de cobertura pendiente — la señal correcta es el campo
  estructurado `frontmatter.constitutional_articles` (la misma que usa `scripts/validate-chapter`),
  no un grep de substrings sobre el texto completo del capítulo.

## 8. Deuda intencional hacia el próximo capítulo

- **`P-09`** ("Single-agent reliability precedes multi-agent complexity"): la única regla de la
  Constitution que, tras CH-24, sigue sin ninguna cita real — deliberadamente fuera de alcance de
  este capítulo por instrucción explícita del encargo. Es un principio de secuenciación
  arquitectónica de todo el libro, no una responsabilidad que un componente pueda poseer; cerrarlo
  exige una decisión editorial distinta sobre CÓMO materializarlo en código, que otra sesión tomará
  después.
- **El cableado real hacia `AgentLoop`, `ModelGateway`, `AgentCore`, `CapabilityRegistry` y
  `EvaluationHarness`**: ningún componente anterior invoca todavía, de verdad,
  `resolveSkillForSituation`.
- **El mecanismo real de registro/alta de skills**: `registeredSkills` llega como parámetro ya
  poblado — no existe ningún `SkillRegistrationRequest` ni mecanismo de descubrimiento automático.
- **El contenido real detrás de `procedureRef`**: asumido, no construido.
- **La relación estructurada real entre una skill y las capabilities a las que aplica**: `appliesTo`
  reconoce la pregunta sin resolverla.
- **Autorización de lectura/escritura sobre `SkillDescriptor`**: no resuelto.
- **Que un agente efectivamente SIGA el procedimiento que una skill resuelta describe**: fuera de
  alcance por diseño — este capítulo modela la resolución, nunca la ejecución de lo que la skill
  describe.

## 9. Nota de cierre — 63/64, no 64/64

Con CH-24, `P-07` —la mitad del encargo heredado de CH-23— tiene, por fin, un capítulo real que la
cita con código. La afirmación de que las sesenta y cuatro reglas de la Constitution quedan, con
esto, completamente cubiertas sigue siendo FALSA, y este plan, junto con el propio capítulo, lo
documenta explícitamente: `P-09` permanece sin ninguna cita real, deliberadamente, por decisión
explícita del encargo de esta sesión. Sesenta y tres de sesenta y cuatro reglas constitucionales
tienen, cada una, al menos un capítulo real que las cita con código tras CH-24.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
