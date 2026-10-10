---
id: CH-48
title: "El Agente como Directorio: Autoría por Convención"
starting_version: "0.2.1"
ending_version: "0.3"
introduces_components: []
introduces_contracts: [C-065, C-066]
modifies_contracts: []
constitutional_articles: [P-06, P-39, INV-09, INV-E27]
previous_chapter: CH-47
next_chapter: CH-49
retrieval_set:
  expected_outcome:
    id: EO-CH48
    text: |
      Al terminar este capítulo podrás decidir dónde va cada parte de un agente escrito como directorio
      y qué contrato produce cada ubicación, y explicar qué diagnósticos impiden activarlo y por qué el
      runtime no infiere nada que no esté declarado.
  skeleton:
    id: SK-CH48
    section_titles:
      - "1. Arquitectura Actual (Current Architecture)"
      - "2. El Problema (Problem)"
      - "3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)"
      - "4. Impacto Constitucional (Constitutional Impact)"
      - "5. Conceptos Nuevos (New Concepts)"
      - "6. Nuevas Estructuras de Datos (New Data Structures)"
      - "7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)"
      - "8. Responsabilidades de Componentes (Component Responsibilities)"
      - "9. Relaciones de Dependencia (Dependency Relationships)"
      - "10. Diagrama de Secuencia (Sequence Diagram)"
      - "11. Pseudocódigo (Pseudocode)"
      - "12. Transiciones de Estado (State Transitions)"
      - "13. Semántica de Fallos (Failure Semantics)"
      - "14. Eventos Producidos (Events Produced)"
      - "15. Implicaciones de Seguridad / Política (Security / Policy Implications)"
      - "16. Tests (Tests)"
      - "17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)"
      - "18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)"
      - "19. Siguiente Incremento (Next Increment)"
    components_to_be_introduced: []
    contracts_to_be_introduced: [C-065, C-066]
  guiding_questions:
    - id: GQ-CH48-01
      text: |
        Si alguien nuevo en el equipo quiere saber qué herramientas, conexiones y canales tiene un
        agente, ¿dónde debería mirar? ¿Y cómo sabe cómo se llama cada herramienta?
      answered_by: RQ-CH48-01
    - id: GQ-CH48-02
      text: |
        Si dos archivos definen una herramienta con el mismo nombre, o falta la configuración del agente,
        ¿debería el agente arrancar igual y avisar, o no arrancar?
      answered_by: RQ-CH48-02
    - id: GQ-CH48-03
      text: |
        Si clonas un repositorio ajeno con un agente adentro, ¿debería el sistema ejecutar su código
        apenas lo abre?
      answered_by: RQ-CH48-03
    - id: GQ-CH48-04
      text: |
        Si un agente trae herramientas por defecto y tú escribes una con el mismo nombre, ¿cuál debería
        ganar? ¿Y si agregas un canal nuevo, debería empezar a escuchar solo?
      answered_by: RQ-CH48-04
  systems_lens:
    iceberg_visible_fact: |
      Un agente es hoy una configuración repartida entre código, registros y archivos sin forma
      convencional: para saber qué herramientas, conexiones o canales tiene hay que leer el código que lo
      arma, y un error de autoría aparece recién cuando el agente ya corre (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que los contratos existen (AgentConfig, CapabilityDescriptor,
      ConnectionDescriptor, DataSourceDescriptor…), pero no hay una convención de dónde se escriben ni un
      manifiesto que diga qué se descubrió: el runtime termina infiriendo lo que nadie declaró (ver
      sección 3).
    iceberg_structures: |
      Este capítulo introduce AgentManifest (C-065) y AuthoringDiagnostic (C-066), un adaptador de
      autoría que descubre el directorio sin ser un componente, y le da a AgentCore la verificación de
      que el manifiesto no tenga errores antes de activar (ver sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-39 (el agente se escribe como archivos inspeccionables en ubicaciones
      convencionales), P-06 (los agentes son configuración sobre un runtime compartido), INV-E27 (un
      ERROR impide activar) y EVO-10 (una extensión no se salta los límites) (ver sección 4).
    reinforcing_loop: |
      Si cada agente se arma a su manera, cada uno necesita leer su código para entenderlo; como nadie
      lo entiende sin leerlo, cada cambio agrega otra forma particular de armarlo, y la siguiente persona
      tiene todavía más que leer.
    balancing_loop: |
      La convención y el manifiesto son el equilibrio: cada parte nueva va en una ranura conocida, el
      manifiesto la muestra con su ruta y origen, y un error de autoría detiene la activación antes de
      llegar a producción.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que AgentManifest (C-065) sea lo único que el
      runtime conoce del agente: lo que no está en el manifiesto no existe, lo que está se ve con su ruta
      y origen, y un AuthoringDiagnostic ERROR impide activarlo.
  recall_questions:
    - id: RQ-CH48-01
      text: |
        ¿Cómo obtiene su nombre cada fuente del directorio, qué gramática debe cumplir, y qué contrato
        produce cada ranura?
    - id: RQ-CH48-02
      text: |
        ¿Qué diagnósticos de nivel ERROR produce discoverAgent, y qué hace requireActivatableManifest si
        encuentra alguno?
    - id: RQ-CH48-03
      text: |
        ¿Qué diagnóstico produce un archivo de código en un directorio no confiable, y qué partes del
        agente siguen siendo legibles sin confianza?
    - id: RQ-CH48-04
      text: |
        ¿Cuándo se agrega un default al manifiesto, y qué produce closedChannelDiagnostics para un canal
        sin regla de admisión?
  explain_prompts:
    - id: EP-CH48-01
      text: |
        AgentCore ya validaba el AgentConfig antes de arrancar. Explica, como si hablaras con alguien sin
        contexto técnico, por qué también le pertenece rechazar un manifiesto con errores, y por qué el
        descubrimiento del directorio no es un componente.
      target_entity: CMP-011
    - id: EP-CH48-02
      text: |
        Explica por qué el runtime no debe inferir nada que el manifiesto no declare, y qué problemas
        aparecerían si completara por su cuenta lo que falta.
      target_entity: C-065
  interleaved_questions:
    - id: IQ-CH48-01
      text: |
        En CH-11, AgentCore validaba un AgentConfig antes de instanciar el AgentState inicial. ¿Qué
        verificación se agrega antes de esa, qué invariante la exige, y qué ranura del directorio produce
        el AgentConfig y su ExecutionBudget?
      current_chapter_entities: [C-065, C-066]
      prior_chapter_entities: [C-002, CMP-011]
      prior_chapter: CH-11
  flashcards:
    - id: FC-CH48-01
      front: |
        ¿Qué es AgentManifest (C-065)?
      back: |
        Lo que el adaptador de autoría descubrió en el directorio de un agente: cada fuente con ranura,
        nombre (de la ruta), ruta y origen, los diagnósticos y si el directorio es confiable. El runtime no
        conoce nada fuera de él.
      source_entity: C-065
      chapter_introduced_in: CH-48
      review_stage: DAY_1
    - id: FC-CH48-02
      front: |
        ¿Qué es AuthoringDiagnostic (C-066) y qué hace uno de nivel ERROR?
      back: |
        Un problema de autoría con nivel (ERROR, WARNING, INFO), código y ruta. Un ERROR impide activar el
        agente (INV-E27, requireActivatableManifest).
      source_entity: C-066
      chapter_introduced_in: CH-48
      review_stage: DAY_1
    - id: FC-CH48-03
      front: |
        ¿Cuáles son las reglas de la convención del directorio?
      back: |
        La ruta es la identidad; los defaults ocupan las mismas ranuras; el markdown es dato y el código
        necesita confianza; las entradas no se abren solas; nada se infiere y todo se expone.
      source_entity: C-065
      chapter_introduced_in: CH-48
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH48-01
      recall_question: RQ-CH48-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH48-02
      recall_question: RQ-CH48-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH48-03
      recall_question: RQ-CH48-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH48-04
      recall_question: RQ-CH48-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 48 — El Agente como Directorio: Autoría por Convención

> **Regla constitucional (INV-E27):** un diagnóstico de autoría de nivel ERROR impide cualquier
> activación de ese agente.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir dónde va cada parte de un agente
escrito como directorio y qué contrato produce cada ubicación. También podrás explicar qué diagnósticos
impiden activarlo y por qué el runtime no infiere nada que no esté declarado.

**Esqueleto.** Décimo capítulo de la versión 0.3. No introduce componentes: agrega `AgentManifest` y
`AuthoringDiagnostic`, un adaptador de autoría y una verificación nueva en `AgentCore`.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si alguien nuevo en el equipo quiere saber qué herramientas, conexiones y canales tiene un agente,
   ¿dónde debería mirar? ¿Y cómo sabe cómo se llama cada herramienta?
2. Si dos archivos definen una herramienta con el mismo nombre, o falta la configuración del agente,
   ¿debería el agente arrancar igual y avisar, o no arrancar?
3. Si clonas un repositorio ajeno con un agente adentro, ¿debería el sistema ejecutar su código apenas
   lo abre?
4. Si un agente trae herramientas por defecto y tú escribes una con el mismo nombre, ¿cuál debería
   ganar? ¿Y si agregas un canal nuevo, debería empezar a escuchar solo?

## 1. Arquitectura Actual (Current Architecture)

- **Los contratos de un agente ya existen:**
  - `AgentConfig` (C-002) y `ExecutionBudget` (C-012) desde CH-00;
  - `CapabilityDescriptor` (C-018, CH-08), `SkillDescriptor` (C-035, CH-24) y
    `ExtensionRegistration` (C-051, CH-40);
  - `ConnectionDescriptor` (C-054, CH-41) y `DataSourceDescriptor` (C-055, CH-42);
  - `ActivationRequest` (C-022), que producen los Ingress Adapters de canales y programaciones
    (CH-14, CH-34).
- **`AgentCore` (CMP-011, CH-11)** valida el `AgentConfig` antes de que arranque cualquier ejecución.
- **No hay convención de dónde se escriben** ni un registro de qué se descubrió. Cada despliegue arma
  el agente a su manera.

## 2. El Problema (Problem)

Un equipo hereda un agente de soporte. Para saber qué hace, alguien tiene que leer el código que lo
arma. Hoy:
- **no hay un lugar donde mirar:** las herramientas se registran en un archivo, las conexiones en
  otro, los canales en el arranque;
- **los nombres no salen de ningún lado:** una herramienta se llama como alguien decidió en el código;
- **dos herramientas con el mismo nombre** se pisan sin aviso: gana la última registrada;
- **un repositorio clonado ejecuta su código al abrirlo,** antes de que nadie lo revise;
- **un canal nuevo empieza a escuchar** apenas alguien lo agrega;
- **un error de autoría aparece en producción,** cuando el agente ya está atendiendo.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **Los contratos dicen qué es cada parte, no dónde se escribe.** Sin convención, cada despliegue
  inventa la suya.
- **Sin manifiesto, el runtime infiere:** completa lo que falta con lo que encuentra, y nadie puede ver
  qué encontró. P-39 lo prohíbe.
- **Sin diagnósticos con ruta, un error de autoría es un error de ejecución.**
- **No hace falta un componente nuevo:** descubrir un directorio es un adaptador de autoría que produce
  contratos que ya existen (P-06, EVO-01); rechazar un agente mal escrito es parte de validar su
  configuración, que ya es de `AgentCore`.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-06   Agents are configuration over a shared runtime.
           El directorio produce configuración; el runtime es el mismo para todos.
    P-39   (Amendment v1.2) An agent is authored as inspectable, conventionally located files.
           La ruta es la identidad; el runtime no infiere y expone lo que descubrió (AgentManifest).
    EVO-10 Extensions cannot bypass constitutional boundaries.
           hooks/ produce ExtensionRegistration, con las restricciones de CH-40.

Invariants preserved
    INV-09   Todo run tiene límites explícitos: la configuración del agente declara su ExecutionBudget.
    INV-E27  (Amendment v1.2) An authoring diagnostic of level ERROR prevents any activation of that agent.
             requireActivatableManifest lo hace cumplir.

Component ownership changes
    Ninguno nuevo. El descubrimiento es un adaptador de autoría (EVO-01); AgentCore gana
    requireActivatableManifest dentro de "validar un AgentConfig antes de que arranque cualquier ejecución".

Contract changes
    Nuevos: C-065 AgentManifest, C-066 AuthoringDiagnostic.

Observability implications
    Nuevo AgentEventType: AGENT_MANIFEST_REJECTED.
```

## 5. Conceptos Nuevos (New Concepts)

- **Directorio del agente:** una carpeta con ubicaciones convencionales (ranuras). Cada archivo en una
  ranura produce un contrato que ya existe.
- **La ruta es la identidad:** el nombre de una fuente sale de su ruta dentro de la ranura;
  `tools/facturacion/reembolso` se llama `facturacion-reembolso`.
- **Ranuras y lo que producen:**

| Ranura | Obligatoria | Produce |
|---|---|---|
| `agent` (archivo de configuración) | sí | `AgentConfig` (C-002) con su `ExecutionBudget` (C-012) |
| `instructions` | sí | el bloque de sistema que compone ContextEngine (CH-04) |
| `tools/` | no | `CapabilityDescriptor` (C-018) |
| `skills/` | no | `SkillDescriptor` (C-035) |
| `connections/` | no | `ConnectionDescriptor` (C-054) |
| `data/` | no | `DataSourceDescriptor` (C-055) |
| `channels/`, `schedules/` | no | Ingress Adapters que producen `ActivationRequest` (C-022) |
| `policies/` | no | reglas de PolicyEngine y de admisión (CH-05, CH-14, CH-38) |
| `hooks/` | no | `ExtensionRegistration` (C-051) |

- **Defaults en las mismas ranuras:** el arnés trae algunas fuentes por defecto (por ejemplo, un canal
  de línea de comandos). Un archivo propio con el mismo nombre las reemplaza.
- **El markdown es dato; el código necesita confianza:** las instrucciones y las skills en markdown se
  leen siempre; un archivo de código solo se carga si el directorio es confiable.
- **Las entradas no se abren solas:** un canal sin regla de admisión se descubre, pero no escucha.
- **Manifiesto:** lo que se descubrió, con ruta y origen de cada fuente y los diagnósticos. Es lo único
  que el runtime conoce del agente, y se expone.
- **Diagnóstico de autoría:** un problema con nivel, código y ruta. Un ERROR impide activar.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `AgentConfig` (C-002), `ExecutionContext` (C-004), `AgentEvent` (C-010),
  `HarnessError` (C-011);
- **primitivos:** `AgentId`, `Timestamp`.

| Identificador | Rol en este capítulo |
|---|---|
| `AgentEventType` | se agrega `AGENT_MANIFEST_REJECTED` |
| `ErrorCategory` | reutiliza `VALIDATION` |

### `AuthoringSlot`, `SourceOrigin` y `DiagnosticLevel` (embebidos)

```pseudocode
ENUM AuthoringSlot
    CONFIG
    INSTRUCTIONS
    TOOLS
    SKILLS
    CONNECTIONS
    DATA
    CHANNELS
    SCHEDULES
    POLICIES
    HOOKS
END
```

```pseudocode
ENUM SourceOrigin
    PROJECT
    DEFAULT
END
```

```pseudocode
ENUM DiagnosticLevel
    ERROR
    WARNING
    INFO
END
```

### `SlotRule`, `AuthoredFile` y `ManifestSource` (embebidos)

```pseudocode
STRUCT SlotRule
    directory: Text
    slot: AuthoringSlot
    required: Boolean
END
```

```pseudocode
STRUCT AuthoredFile
    path: Text
    isCode: Boolean
    content: Text
END
```

```pseudocode
STRUCT ManifestSource
    slot: AuthoringSlot
    name: Text
    path: Text
    origin: SourceOrigin
END
```

`SlotRule.directory` es el primer segmento de la ruta (`tools`, `connections`…) o el nombre del archivo
sin extensión para las ranuras de un solo archivo (`agent`, `instructions`).

### `AuthoringDiagnostic` — un problema de autoría (C-066)

```pseudocode
STRUCT AuthoringDiagnostic
    level: DiagnosticLevel
    code: Text
    path: Text
    message: Text
END
```

### `AgentManifest` — lo que se descubrió (C-065)

```pseudocode
STRUCT AgentManifest
    agentRoot: Text
    sources: List<ManifestSource>
    diagnostics: List<AuthoringDiagnostic>
    trusted: Boolean
    discoveredAt: Timestamp
END
```

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

```text
ID:                     C-065
Name:                   AgentManifest
Version:                v1
Introduced In:          CH-48
Used By:                [CMP-011]
Constitutional Impact:  [P-06, P-39, INV-E27]
```

```text
ID:                     C-066
Name:                   AuthoringDiagnostic
Version:                v1
Introduced In:          CH-48
Used By:                [CMP-011]
Constitutional Impact:  [P-39, INV-E27]
```

`AuthoringSlot`, `SourceOrigin`, `DiagnosticLevel`, `SlotRule`, `AuthoredFile` y `ManifestSource`
quedan embebidos.

## 8. Responsabilidades de Componentes (Component Responsibilities)

**Este capítulo no introduce componentes.** El descubrimiento es un **adaptador de autoría**, como los
Ingress Adapters o los adaptadores de protocolo: está en el borde y produce contratos que ya existen.

```text
Adaptador de autoría (sin componente, EVO-01)
    slotOf, validSlotName, findSource, diagnosticsForFile, discoverAgent,
    closedChannelDiagnostics, hasErrors
    produce: AgentManifest y, desde cada fuente, los contratos de la tabla de §5
    no decide: si el agente puede activarse (AgentCore)

AgentCore (CMP-011)
    owns: "validar un AgentConfig antes de que arranque cualquier ejecución"
    nueva:
        requireActivatableManifest
    no posee:
        leer el sistema de archivos ni descubrir ranuras (el adaptador de autoría)
        decidir si un canal escucha (AdmissionController, CH-14)
```

El propio libro es un ejemplo de autoría por convención: `book/`, `registry/` y `planes/` son
ubicaciones fijas, y los validadores son sus diagnósticos.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
Directorio → adaptador de autoría
    por archivo: slotOf → nombre desde la ruta → diagnosticsForFile → ManifestSource
    obligatorias: agent e instructions
    defaults que nadie reemplazó → ManifestSource (DEFAULT)
    closedChannelDiagnostics(manifiesto, canales con regla de admisión)
    → AgentManifest (expuesto: el adaptador lo escribe y lo muestra)
Activar → AgentCore.requireActivatableManifest → (sin ERROR) → activateAgent (CH-11)
Cada fuente → su contrato (C-002, C-018, C-054, C-055, …) → el componente dueño, sin cambios
```

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
directorio → adaptador de autoría → AgentManifest → AgentCore.requireActivatableManifest
          → activateAgent (CH-11) → los componentes reciben sus contratos de siempre
```

**Vista 2 — Sequence: el agente de soporte**

```text
soporte/
    agent, instructions
    tools/facturacion/reembolso, tools/buscar-ticket
    connections/tickets, data/clientes
    channels/cli (default reemplazado), channels/chat-web
    policies/admision (regla solo para cli)
   │ discoverAgent(confiable)
   │   tools: facturacion-reembolso, buscar-ticket; connections: tickets; data: clientes
   │   closedChannelDiagnostics → WARNING channels/chat-web: sin regla de admisión, no escucha
   │ requireActivatableManifest → sin ERROR → activateAgent
```

**Vista 2b — Sequence: un repositorio clonado sin confianza**

```text
discoverAgent(no confiable) → ERROR authoring/untrusted-code en cada archivo de código
requireActivatableManifest → AGENT_MANIFEST_REJECTED → AGENT_MANIFEST_HAS_ERRORS
```

**Vista 2c — Sequence: dos herramientas con el mismo nombre**

```text
tools/buscar-ticket y tools/buscar-ticket.md → ERROR authoring/duplicate-name → no se activa
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

```pseudocode
FUNCTION slotOf(
    path: Text,
    rules: List<SlotRule>
) -> Optional<SlotRule>

    head: Text = stripExtension(firstSegment(path))

    FOR EACH rule IN rules
        IF rule.directory == head
            RETURN rule
        END
    END

    RETURN NULL
END
```

```pseudocode
FUNCTION validSlotName(
    name: Text
) -> Boolean

    RETURN matchesPattern(name, "^[a-z][a-z0-9-]{0,63}$")
END
```

```pseudocode
FUNCTION findSource(
    sources: List<ManifestSource>,
    slot: AuthoringSlot,
    name: Text
) -> Optional<ManifestSource>

    FOR EACH source IN sources
        IF source.slot == slot AND toLower(source.name) == toLower(name)
            RETURN source
        END
    END

    RETURN NULL
END
```

```pseudocode
FUNCTION diagnosticsForFile(
    file: AuthoredFile,
    rule: Optional<SlotRule>,
    name: Text,
    trusted: Boolean
) -> List<AuthoringDiagnostic>

    diagnostics: List<AuthoringDiagnostic> = []

    IF rule == NULL
        RETURN append(diagnostics, AuthoringDiagnostic(
            level = ERROR,
            code = "authoring/unknown-slot",
            path = file.path,
            message = "El archivo no está en ninguna ranura conocida; el runtime no infiere qué es"
        ))
    END

    IF NOT validSlotName(name)
        diagnostics = append(diagnostics, AuthoringDiagnostic(
            level = ERROR,
            code = "authoring/invalid-name",
            path = file.path,
            message = "El nombre que sale de la ruta no cumple la gramática de nombres"
        ))
    END

    IF file.isCode AND NOT trusted
        diagnostics = append(diagnostics, AuthoringDiagnostic(
            level = ERROR,
            code = "authoring/untrusted-code",
            path = file.path,
            message = "Un archivo de código solo se carga si el directorio es confiable"
        ))
    END

    IF looksLikeSecret(file.content)
        diagnostics = append(diagnostics, AuthoringDiagnostic(
            level = ERROR,
            code = "authoring/secret-in-file",
            path = file.path,
            message = "El archivo contiene algo con forma de secreto; los secretos se declaran por nombre"
        ))
    END

    RETURN diagnostics
END
```

```pseudocode
FUNCTION discoverAgent(
    agentRoot: Text,
    files: List<AuthoredFile>,
    rules: List<SlotRule>,
    defaults: List<ManifestSource>,
    trusted: Boolean
) -> AgentManifest

    sources: List<ManifestSource> = []
    diagnostics: List<AuthoringDiagnostic> = []

    FOR EACH file IN files
        rule: Optional<SlotRule> = slotOf(file.path, rules)
        name: Text = identityFromPath(file.path)
        diagnostics = concat(diagnostics, diagnosticsForFile(file, rule, name, trusted))

        IF rule != NULL
            IF findSource(sources, rule.slot, name) != NULL
                diagnostics = append(diagnostics, AuthoringDiagnostic(
                    level = ERROR,
                    code = "authoring/duplicate-name",
                    path = file.path,
                    message = "Otra fuente de la misma ranura ya tiene este nombre"
                ))
            ELSE
                sources = append(sources, ManifestSource(
                    slot = rule.slot, name = name, path = file.path, origin = PROJECT
                ))
            END
        END
    END

    FOR EACH rule IN rules
        IF rule.required AND findSource(sources, rule.slot, rule.directory) == NULL
            diagnostics = append(diagnostics, AuthoringDiagnostic(
                level = ERROR,
                code = "authoring/required-slot-missing",
                path = agentRoot + "/" + rule.directory,
                message = "Falta una ranura obligatoria del agente"
            ))
        END
    END

    FOR EACH default IN defaults
        IF findSource(sources, default.slot, default.name) == NULL
            sources = append(sources, default)
        END
    END

    RETURN AgentManifest(
        agentRoot = agentRoot,
        sources = sources,
        diagnostics = diagnostics,
        trusted = trusted,
        discoveredAt = now()
    )
END
```

```pseudocode
FUNCTION closedChannelDiagnostics(
    manifest: AgentManifest,
    admittedChannels: List<Text>
) -> List<AuthoringDiagnostic>

    diagnostics: List<AuthoringDiagnostic> = []

    FOR EACH source IN manifest.sources
        IF source.slot == CHANNELS AND NOT contains(admittedChannels, source.name)
            diagnostics = append(diagnostics, AuthoringDiagnostic(
                level = WARNING,
                code = "authoring/channel-without-admission",
                path = source.path,
                message = "El canal se descubrió, pero no escucha: no tiene regla de admisión"
            ))
        END
    END

    RETURN diagnostics
END
```

```pseudocode
FUNCTION hasErrors(
    manifest: AgentManifest
) -> Boolean

    FOR EACH diagnostic IN manifest.diagnostics
        IF diagnostic.level == ERROR
            RETURN TRUE
        END
    END

    RETURN FALSE
END
```

```pseudocode
FUNCTION requireActivatableManifest(
    manifest: AgentManifest,
    execution: ExecutionContext,
    agentId: AgentId
) -> AgentManifest

    IF hasErrors(manifest)
        failure: HarnessError = HarnessError(
            category = VALIDATION,
            code = "AGENT_MANIFEST_HAS_ERRORS",
            message = "El manifiesto del agente tiene diagnósticos de nivel ERROR; el agente no se activa (INV-E27)",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = AGENT_MANIFEST_REJECTED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = manifest
        )
        THROW failure
    END

    RETURN manifest
END
```

Utilidades primitivas:
- `firstSegment` (el primer segmento de una ruta) y `stripExtension`;
- `identityFromPath`: los segmentos después de la ranura, sin extensión, unidos con `-`
  (`tools/facturacion/reembolso` → `facturacion-reembolso`); para una ranura de un solo archivo, el
  nombre del archivo sin extensión;
- `matchesPattern`, `toLower`, `looksLikeSecret` (formas conocidas de claves y certificados);
- `append`, `concat`, `contains`, `newEventId` y `now`.

`activateAgent` (CH-11) no cambia: `requireActivatableManifest` va antes.

**Por qué un canal sin regla es WARNING y no ERROR:** el agente puede activarse y atender por los
canales admitidos; el canal nuevo simplemente no escucha hasta que alguien escriba su regla. Un error
impediría activar un agente sano por una entrada que todavía nadie habilitó.

Nótese lo que estas funciones **no** hacen:
- ninguna completa lo que falta: una ranura obligatoria ausente es un ERROR, nunca un valor inventado;
- ninguna carga código: el adaptador lo carga después, y solo si el directorio es confiable;
- ninguna reemplaza a los componentes dueños: cada contrato producido sigue su camino de siempre.

## 12. Transiciones de Estado (State Transitions)

`AgentRunStatus` no cambia. El manifiesto, antes de activar:

```text
descubierto, sin diagnósticos ERROR → activable → activateAgent (CH-11)
descubierto, con algún ERROR        → AGENT_MANIFEST_REJECTED; el agente no se activa
WARNING / INFO                       → visibles en el manifiesto; no impiden activar

Canal descubierto
    con regla de admisión → escucha
    sin regla             → no escucha (WARNING)
```

## 13. Semántica de Fallos (Failure Semantics)

Código nuevo de `HarnessError`, con una `ErrorCategory` ya existente:

```text
VALIDATION  AGENT_MANIFEST_HAS_ERRORS  recoverable: FALSE, retryable: FALSE
```

Diagnósticos de autoría (no son `HarnessError`: son datos del manifiesto):

```text
ERROR    authoring/unknown-slot              archivo fuera de toda ranura
ERROR    authoring/invalid-name              el nombre de la ruta no cumple la gramática
ERROR    authoring/untrusted-code            código en un directorio no confiable
ERROR    authoring/secret-in-file            algo con forma de secreto en un archivo
ERROR    authoring/duplicate-name            dos fuentes con el mismo nombre en una ranura
ERROR    authoring/required-slot-missing     falta agent o instructions
WARNING  authoring/channel-without-admission canal descubierto que no escucha
```

Cada diagnóstico lleva la ruta exacta: corregir un error de autoría no exige leer código del runtime.

## 14. Eventos Producidos (Events Produced)

```text
AGENT_MANIFEST_REJECTED — un agente no se activó por diagnósticos ERROR (payload: AgentManifest)
```

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **Abrir un repositorio no ejecuta su código:** sin confianza, el código es un ERROR.
- **Los secretos no se escriben en el directorio:** se declaran por nombre y los resuelve el broker
  (CH-16); un archivo con forma de secreto impide activar.
- **Una entrada nueva no se abre sola:** sin regla de admisión, el canal no escucha (CH-14).
- **Una fuente de datos sin clasificación es RESTRICTED** (CH-42, INV-E26), también si viene del
  directorio.
- **Un hook sigue las restricciones de CH-40:** solo restringe, nunca autoriza (INV-E24, EVO-10).
- **Lo que corre es lo que se ve:** el manifiesto expuesto es exactamente lo que el runtime conoce.

## 16. Tests (Tests)

```text
TEST NameComesFromThePath
TEST InvalidNameIsAnError
TEST FileOutsideAnySlotIsAnError
TEST DuplicateNameInASlotIsAnError
TEST MissingConfigOrInstructionsIsAnError
TEST CodeInAnUntrustedDirectoryIsAnError
TEST MarkdownIsReadWithoutTrust
TEST SecretShapedContentIsAnError
TEST OwnFileReplacesTheDefaultWithTheSameName
TEST UnreplacedDefaultsAppearWithOriginDefault
TEST ChannelWithoutAdmissionRuleDoesNotListen
TEST ManifestWithErrorsIsRejectedAndEmitsEvent
TEST ManifestWithOnlyWarningsIsActivatable
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (v0.3 en curso, después de CH-48) — 29 componentes, 66 contratos, 49 capítulos

Components — 29, sin cambios
 └── CMP-011 AgentCore             (+ un manifiesto con ERROR no se activa)

Adaptador de autoría (sin componente) → AgentManifest → los contratos de siempre

Contracts — 66
 ├── C-065 AgentManifest           (CH-48)
 └── C-066 AuthoringDiagnostic     (CH-48)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **Un ámbito global** (fuentes personales del usuario además de las del proyecto): agrega un origen
  más, con la regla de que el proyecto gana; la estructura del manifiesto no cambia. No es deuda.
- **El lenguaje de los archivos de código:** el libro modela ranuras, nombres y diagnósticos; cada
  despliegue elige su lenguaje. No es deuda.
- **Cómo se registra la confianza en un directorio:** es del adaptador de autoría y de la herramienta
  del usuario. No es deuda.
- **Recargar el directorio en caliente:** un cambio en el directorio es una versión nueva del agente, y
  pasar a ella es la evolución del runtime de CH-45. No es deuda.

## 19. Siguiente Incremento (Next Increment)

La versión 0.3 está completa por partes: el modelo como dato, extensiones, conexiones, fuentes de
datos, presupuestos heredados, invocación entre agentes, evolución del runtime, observabilidad por
audiencia, evaluación con lift y autoría por convención. Pero todavía no se las vio **funcionar
juntas** en un solo recorrido.

El siguiente capítulo es la **integración de la versión 0.3**:
- un agente escrito como directorio, con una conexión, una fuente de datos y un subagente;
- un turno conectado de punta a punta, con presupuesto heredado y techos por audiencia;
- las cuatro deudas que quedan abiertas con destino CH-49.

Será CH-49 ("La Integración Conectada"). `next_chapter` queda en `null` porque CH-49 todavía no
existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): para saber qué tiene un agente hay que leer el código que lo arma, y los
   errores de autoría aparecen en producción.
2. **Patrones** (= §3): los contratos existen, pero no dónde se escriben ni qué se descubrió.
3. **Estructuras** (= §8): `AgentManifest` (C-065), `AuthoringDiagnostic` (C-066), el adaptador de
   autoría y `requireActivatableManifest` en `AgentCore`.
4. **Modelos mentales** (= §4): P-39, P-06, INV-E27 y EVO-10.

**Bucles de retroalimentación**

- **Refuerzo:** cada agente armado a su manera hace más difícil entender el siguiente.
- **Equilibrio:** la convención y el manifiesto. Cada parte va en una ranura conocida, y un error
  detiene la activación.

**Punto de apalancamiento**

La decisión con mayor efecto es que `AgentManifest` (C-065) sea lo único que el runtime conoce del
agente: lo que no está no existe, y un ERROR impide activarlo.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Cómo obtiene su nombre cada fuente del directorio, qué gramática debe cumplir, y qué contrato
   produce cada ranura? *(pregunta guía 1)*
2. ¿Qué diagnósticos de nivel ERROR produce `discoverAgent`, y qué hace `requireActivatableManifest` si
   encuentra alguno? *(pregunta guía 2)*
3. ¿Qué diagnóstico produce un archivo de código en un directorio no confiable, y qué partes del agente
   siguen siendo legibles sin confianza? *(pregunta guía 3)*
4. ¿Cuándo se agrega un default al manifiesto, y qué produce `closedChannelDiagnostics` para un canal
   sin regla de admisión? *(pregunta guía 4)*

### Explicar

1. `AgentCore` ya validaba el `AgentConfig` antes de arrancar. Explica por qué también le pertenece
   rechazar un manifiesto con errores, y por qué el descubrimiento del directorio no es un componente.
2. Explica por qué el runtime no debe inferir nada que el manifiesto no declare, y qué problemas
   aparecerían si completara por su cuenta lo que falta.

### Conectar

1. En CH-11, `AgentCore` validaba un `AgentConfig` antes de instanciar el `AgentState` inicial. ¿Qué
   verificación se agrega antes de esa, qué invariante la exige, y qué ranura del directorio produce el
   `AgentConfig` y su `ExecutionBudget`?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
