# Plan / Registro de ejecución — Capítulo 23: HandoffCoordinator y el Paquete Estructurado que Nunca Es Solo Prosa

**Fecha:** 2026-09-18
**Estado:** ✅ Completado, sobre el estado dejado por `0119841` (CH-00..CH-22 como los veintitrés
únicos capítulos reales; sesenta y tres de sesenta y cuatro reglas constitucionales citadas —
`INV-E12` señalada por el plan de CH-22 como la única pendiente).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-18-capitulo-22-evaluation-harness.md` (precedente inmediato: identificó `INV-E12` como el
  último invariante/principio sin citar, sin resolverlo — encargo directo de este capítulo)
- `2026-09-14-capitulo-06-human-interaction-service.md` (la frontera más importante a trazar:
  `HumanInteractionService` ya representa y resuelve una decisión puntual dentro de un turno vivo;
  este capítulo transfiere el control COMPLETO de un run/sesión, una operación distinta)
- `2026-09-18-capitulo-18-operational-controller.md` (`ControlDirective`/`KILL_SWITCH`, el disparador
  canónico usado en el pseudocódigo de este capítulo)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Amendment v1.1 — `INV-E12`, línea 986)

---

## 1. Objetivo

Escribir el vigesimocuarto capítulo real de contenido del libro, CH-23 — el décimo componente de
este registry que no corresponde a ninguno de los once nombres de Article III, y el que cierra
`INV-E12` ("A human handoff transfers a structured HandoffPackage rather than only prose"), la
regla que el plan de ejecución de CH-22 había señalado como la última de la Constitution sin
ninguna cita real.

**Verificación de la premisa central, ejecutada antes de escribir una sola línea del capítulo**: un
barrido programático (`grep`/Python) sobre `constitutional_articles` y sobre el texto íntegro de los
veintitrés `chapter.md` anteriores confirmó que `INV-E12` en particular sigue sin ninguna cita fuera
de la transcripción de Amendment v1.1 en CH-00 §5 — esa parte de la premisa es exacta. Pero, tal como
el encargo de este capítulo pedía explícitamente verificar ("si encontraras que ya no es así, dilo
explícitamente"), un segundo barrido — ejecutado esta vez sobre las SESENTA Y CUATRO reglas
completas de la Constitution, no solo sobre `INV-E12` — reveló que la premisa de EXCLUSIVIDAD
heredada de CH-22 ("`INV-E12` es la ÚNICA regla sin citar") no era del todo correcta:

```text
$ python3 - <<'EOF'
import re, glob
const = open('constitution/ARCHITECTURE_CONSTITUTION.md', encoding='utf-8').read()
expected = set(f'P-{i:02d}' for i in range(1,31)) | \
           set(f'INV-{i:02d}' for i in range(1,21)) | \
           set(f'INV-E{i:02d}' for i in range(1,15))
full_text = ""
for c in sorted(glob.glob('book/chapters/*/chapter.md')):
    if '00-arquitectura-constitucion' in c:
        continue  # CH-00 solo transcribe Amendment v1.1 en su frontmatter; no cuenta como "cita real"
    full_text += open(c, encoding='utf-8').read()
cited = set(re.findall(r'\b(?:P-\d{2}|INV-E\d{2}|INV-\d{2})\b', full_text))
print(sorted(expected - cited))
EOF
['P-07', 'P-09']
```

**Antes de CH-23** (sobre CH-00..CH-22): `INV-E12`, `P-07` y `P-09` — tres reglas, no una — llegaban
al capítulo sin ninguna cita real, ni con código ni en prosa, fuera de la transcripción literal del
frontmatter de CH-00 §0. `P-07` ("Skills encode reusable procedural knowledge") y `P-09`
("Single-agent reliability precedes multi-agent complexity") nunca aparecen, ni una sola vez, en la
sección 4 (Impacto Constitucional) de ningún capítulo, ni en prosa — verificado también buscando sus
frases clave ("procedural knowledge", "single-agent reliability", "multi-agent complexity") sin
ningún resultado fuera de la propia Constitution.

**Decisión editorial**: honrar el alcance ya decidido para este capítulo (Paso 2 del encargo,
"decisión ya tomada, no la reabras") y NO expandirlo para resolver `P-07`/`P-09` — pero documentar el
hallazgo con el mismo rigor y la misma honestidad de cobertura que CH-22 ya aplicó al descubrir
`INV-E12` sin haberlo buscado. El capítulo (secciones 17 y 19, más el párrafo de apertura y la
sección "Lente de Sistemas") fue corregido explícitamente para NO afirmar una cobertura constitucional
del 100% que sería falsa, y para documentar en su lugar el resultado real de la verificación.

## 2. Alcance (decisión ya tomada antes de escribir, confirmada en el resultado)

Exactamente **1 componente + 1 contrato**, tal como especificó el encargo:

1. **`HandoffCoordinator`** (`CMP-021`) — `owns`: construir, en exclusiva, el `HandoffPackage`
   estructurado que representa la transferencia COMPLETA de control de un run/sesión a un humano
   (`INV-E12` literal); correlacionar opcionalmente ese paquete con una `HumanInteractionRequest` ya
   existente (CH-06), sin modificarla; fail-closed sobre un paquete sin referencia al run/sesión.
   `does_not_own` (frontera trazada contra cuatro componentes ya existentes): pedir o persistir una
   decisión puntual dentro de un turno en curso (`HumanInteractionService`, CMP-006, CH-06 — LA
   FRONTERA MÁS IMPORTANTE, desarrollada con cuidado en seccion 2/3/8/15 del capítulo: los cuatro
   tipos de `HumanInteractionType` — `Approval`/`Input`/`Review`/`Decision` — resuelven siempre una
   pregunta puntual dentro de un turno que se reanuda donde se detuvo; un handoff no reanuda nada,
   transfiere el destino completo de la ejecución); decidir CUÁNDO debe ocurrir un handoff
   (`OperationalController` vía kill switch, CH-18; `ExecutionController` vía terminación por
   presupuesto, CH-07; o `PolicyEngine`, CH-05 — `HandoffCoordinator` construye el paquete UNA VEZ
   que esa decisión ya se tomó, asumida como señal de entrada); ejecutar cualquier acción una vez que
   el humano toma control (fuera de alcance, Preview); transportar el paquete por un canal concreto
   (Channel Adapter, mismo concepto de infraestructura de borde que CH-06 ya declaró fuera del árbol
   de componentes).
2. **`HandoffPackage`** (`C-034`) — `id`, `runId`/`sessionId` (identificadores fuertes ya existentes,
   CH-00 — universo homogéneo, siempre exactamente un run/sesión, mismo argumento que
   `ExecutionPlacement.runId`, CH-21, y `BusinessOutcomeCorrelation.runId`, CH-22), `reason`
   (`HandoffReason`, `ENUM` de cuatro valores `MODEL_STUCK`/`KILL_SWITCH`/`BUDGET_EXHAUSTED`/
   `EXPLICIT_ESCALATION` — la materialización literal de "rather than only prose"), `contextRef`
   (`Text` opaco al `AgentState`/`ContextSnapshot` relevante, sin duplicar su contenido — mismo patrón
   que `subjectRef` en CH-19/CH-20/CH-22), `transferTo` (`ActorId`, reusado de CH-06),
   `humanInteractionRef` (`Optional<HumanInteractionRequestId>`, correlación opcional reusada de
   CH-06, evaluada explícitamente contra la alternativa de extender `HumanInteractionType` y
   descartada — ver seccion 6 del capítulo), `status` (`HandoffStatus`, `ENUM` de tres valores
   `PENDING`/`ACCEPTED`/`COMPLETED` — nunca un `Boolean`, mismo principio ya establecido
   repetidamente), `createdAt`.
3. **Pseudocódigo**: `createHandoffPackage(...)` — autónomo, fail-closed hacia
   `HANDOFF_PACKAGE_MISSING_RUN_ID`, `status` siempre nace en `PENDING`. Se agrega, además, un
   ejemplo explícito (no una función nueva) que muestra cómo un `ControlDirective` de tipo
   `KILL_SWITCH` (CH-18) se traduciría hacia `reason = KILL_SWITCH` — documentado en prosa que
   ningún componente anterior invoca todavía esta función.
4. No se tocó ningún `book/chapters/00-*` a `21-*`. `book/chapters/22-evaluation-harness/chapter.md`
   recibió únicamente el cambio de navegación permitido: `next_chapter: null → CH-23`.
5. `book/book.yaml`: CH-23 agregado después de CH-22. `previous_chapter: CH-22`, `next_chapter: null`
   en el frontmatter de CH-23 (no existe todavía ningún CH-24).
6. `retrieval_set` de CH-23: 4 `guidingQuestions`/`recallQuestions`, 2 `explainPrompts`, 2
   `interleavedQuestions` (CH-06 sobre la frontera con `HumanInteractionService`/
   `HumanInteractionRequestId`; CH-18 sobre `ControlDirective`/`KILL_SWITCH` como disparador de
   ejemplo), 5 `flashcards`, 4 `calibrationPairs`.

## 3. Gotcha real encontrado y corregido: el parser YAML propio del repo no soporta escalares entre comillas que abarcan varias líneas físicas dentro de una secuencia

`scripts/lib/yaml-lite.js` es un parser YAML de subconjunto mínimo, escrito a mano (documentado en su
propio encabezado). Al escribir por primera vez las entradas `owns`/`does_not_own` de `CMP-021` con
el mismo estilo visual "envuelto a 88 columnas" que otros componentes parecían tener en las lecturas
previas de este mismo capítulo (líneas de texto que, en la vista de `Read`, aparentaban continuar en
la línea siguiente con más indentación), el parser falló silenciosamente de una forma engañosa:
`./scripts/validate-components` reportó que a `CMP-021` le faltaban los campos obligatorios
`does_not_own`, `dependencies`, `consumes`, `produces`, `introduced_in` y `constitutional_articles` —
campos que SÍ estaban presentes en el archivo. La causa real: cada item de una secuencia
(`- "texto..."`) debe ser una única línea física completa en este parser; una continuación indentada
en la línea siguiente rompe `parseSequence` (que espera el mismo `indent` en cada item) y, en cascada,
`parseMapping` del componente completo, abandonando el resto de sus campos. Los componentes
anteriores (`CMP-020`, etc.) que aparentaban texto envuelto en la vista de este mismo capítulo eran, en
realidad, una única línea física muy larga en el archivo — no una continuación real. **Corrección**:
cada item de `owns`/`does_not_own` de `CMP-021` se reescribió como una sola línea física (sin
importar su longitud). Verificado con `./scripts/validate-components` → `OK (21 componente(s))`.
Este hallazgo se documenta aquí explícitamente porque no es evidente al leer el archivo con
herramientas que envuelven texto visualmente.

## 4. Verificación ejecutada (evidencia concreta)

```
./scripts/validate-contracts                                               → OK (34 contratos)
./scripts/validate-components                                              → OK (21 componentes)
./scripts/validate-chapter book/chapters/23-handoff-coordinator            → OK a la primera
    (22/19 secciones, 8 bloques pseudocode, 1 contrato introducido, 1 componente introducido)
./scripts/validate-retrieval-set book/chapters/23-handoff-coordinator      → OK
    (guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2, interleavedQuestions: 2,
    flashcards: 5, calibrationPairs: 4)
./scripts/validate-chapter book/chapters/22-evaluation-harness             → OK (revalidado tras
    el único cambio de navegación permitido, next_chapter: CH-23)
rm -rf dist && ./scripts/build-all                                         → exit 0
```

24 capítulos reales, todos pasando `validate-chapter`/`validate-retrieval-set`. `build-mind-map`:
`chapter-23.diagram` con 154 nodos/237 aristas — más que `chapter-22.diagram` (149 nodos/229
aristas), como exige la verificación. Se leyó `scripts/lib/render-diagram.js` (fix de Ghostscript,
CH-16) antes de empezar y no se encontró ningún problema real que justificara modificarlo.

**Web**: `dist/web/chapters/CH-23.html` con SVG inline (`grep -c '<svg'` = 1, verificado en las 24
páginas), anchors `id="CMP-021"`/`id="C-034"` presentes, navegación CH-22↔CH-23 verificada en ambos
sentidos (`href="CH-23.html"` desde CH-22, `href="CH-22.html"` desde CH-23). CH-00..CH-22 no se
rompieron (mismos anchors clave verificados, mismas 24 páginas con exactamente 1 SVG cada una).

**PDF**: con `pypdf`, 631 páginas — más que el build de referencia de 23 capítulos (597 páginas).
Texto extraído de las últimas 45 páginas contiene, verificado programáticamente,
"HandoffCoordinator" y "HandoffPackage".

**Prueba negativa real**: se renombró el campo obligatorio `does_not_own` de `CMP-021` a
`does_not_own_BROKEN` en `registry/components.yaml` (edición dirigida solo a la ficha de `CMP-021`).
`./scripts/validate-components` falló con `exit 1` y el mensaje exacto `Componente CMP-021: falta el
campo obligatorio "does_not_own"`; `rm -rf dist && ./scripts/build-all` se detuvo en la etapa de
validación con `exit 1` real (confirmado explícitamente con `echo "PIPESTATUS/exit: $?"` inmediatamente
después del comando, no inferido de un pipe) y el mensaje `policies/publishing.yaml:
unresolved_validation_errors = deny → build detenido.`, sin construir `dist/web`/`dist/book.pdf`. Se
restauró el campo desde una copia de respaldo (`cp registry/components.yaml` previo), se confirmó
`validate-components: OK (21 componente(s))`, y se reconstruyó todo desde cero: mismos 24 capítulos,
34 contratos, 21 componentes, mismos nodos/aristas por capítulo (154/237 en CH-23), mismo número de
páginas de PDF (631) — conteos idénticos al build previo a la prueba negativa.

**Verificación final especial de este capítulo — cobertura constitucional real, no asumida**: ver
seccion 1 arriba para el comando completo y su salida. Después de CH-23, `INV-E12` queda, por fin,
citada con código real (`HandoffPackage`/`HandoffCoordinator`). Pero, contrario a la premisa heredada
de CH-22 ("`INV-E12` es la última regla sin citar"), `P-07` y `P-09` permanecen sin ninguna cita real
ni en prosa, fuera de la transcripción literal del frontmatter de CH-00. La afirmación de "cobertura
constitucional completa (64/64)" NO es correcta tras CH-23 — el capítulo se corrigió explícitamente
(secciones 17, 19, apertura y Lente de Sistemas) para documentar esto con honestidad en vez de
afirmar una cobertura falsa, siguiendo la instrucción explícita del encargo de reportar este hallazgo
en vez de proceder ciegamente.

## 5. Decisiones de diseño no cubiertas en el encargo original

- **`HandoffPackage.humanInteractionRef` como correlación opcional reusada, en vez de un quinto valor
  de `HumanInteractionType`**: se evaluó explícitamente extender `HumanInteractionType` (CH-06) con
  un quinto valor que significara "asumir el control completo" — se descartó porque los cuatro
  valores existentes comparten la premisa de que toda `HumanInteractionResolution` permite reanudar
  el mismo turno donde se detuvo (CH-06 §9); un handoff no reanuda nada. En su lugar,
  `humanInteractionRef` es `Optional`, poblado solo cuando, además del handoff, existe una decisión
  puntual correlacionada (por ejemplo, la aprobación explícita de aceptar el traspaso) — mismo patrón
  que `BusinessOutcomeCorrelation.humanEscalationRef` (CH-22).
- **`contextRef: Text` opaco, en vez de embeber `AgentState`/`ContextSnapshot` directamente**: se
  evaluó explícitamente embeber una copia — se descartó por el riesgo de desactualización y por
  preservar la independencia de contratos que el resto de Amendment v1.1 ya exige (mismo argumento
  que `subjectRef` en CH-19/CH-20/CH-22).
- **`HandoffStatus` de tres estados (`PENDING`/`ACCEPTED`/`COMPLETED`), no dos como
  `HumanInteractionStatus`**: justificado explícitamente por el estado intermedio real que un
  traspaso de control tiene y que una aprobación/rechazo puntual no necesita.
- **Ningún campo `issuedBy: ActorId` en `HandoffPackage`** (a diferencia de `ControlDirective`,
  CH-18): evaluado y descartado explícitamente — el paquete es la consecuencia empaqueta de una
  decisión que otro componente ya tomó con su propia trazabilidad; duplicar el actor habría reabierto
  información que el disparador original ya preserva.
- **Hallazgo no anticipado por el encargo, documentado con el mismo rigor que CH-22**: `P-07`
  ("Skills encode reusable procedural knowledge") y `P-09` ("Single-agent reliability precedes
  multi-agent complexity") permanecen, después de CH-23, sin ninguna cita real fuera del frontmatter
  de CH-00 — la premisa de que `INV-E12` era la ÚNICA regla pendiente no era, en sentido estricto,
  correcta. Documentado explícitamente en el capítulo (secciones 17/19) y en este plan, sin expandir
  el alcance ya decidido de CH-23 para resolverlo.

## 6. Deuda intencional hacia el próximo capítulo

- **El cableado real hacia `OperationalController`, `ExecutionController`, `PolicyEngine` y
  `HumanInteractionService`**: ningún componente anterior invoca todavía, de verdad,
  `createHandoffPackage`.
- **Las transiciones `PENDING → ACCEPTED` y `ACCEPTED → COMPLETED`**: declaradas en el `ENUM`, no
  cableadas por ninguna función real.
- **La resolución real de `contextRef`**: asumida, no construida.
- **El motor real que decide `MODEL_STUCK`**: conceptual, sin componente dedicado.
- **Autorización de lectura/escritura sobre `HandoffPackage`**, e `INV-E07`: no resuelto.
- **Auditar un handoff con `AuditLedger`**: ningún cableado real.
- **`P-07` y `P-09`**: las dos reglas constitucionales que, tras CH-23, siguen sin ninguna cita real
  — candidatos naturales, aunque no obligatorios, para un próximo incremento.

## 7. Nota de cierre — honestidad de cobertura, no 64/64

Con CH-23, `INV-E12` —la regla que motivó el encargo de este capítulo— tiene, por fin, un capítulo
real que la cita con código. La afirmación de que las sesenta y cuatro reglas de la Constitution
quedan, con esto, completamente cubiertas es FALSA y este plan, junto con el propio capítulo, lo
documenta explícitamente: `P-07` y `P-09` permanecen sin ninguna cita real. Sesenta y dos de sesenta
y cuatro reglas constitucionales tienen, cada una, al menos un capítulo real que las cita con código
tras CH-23.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
