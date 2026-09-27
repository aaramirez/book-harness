---
id: CH-38
title: "Identidad, Auditoría y Retención en Todo el Turno"
starting_version: "0.2"
ending_version: "0.2.1"
introduces_components: []
introduces_contracts: []
modifies_contracts: []
constitutional_articles: [P-13, P-17, P-22, P-25, P-31, P-32, INV-07, INV-13, INV-19, INV-E07, INV-E10, INV-E17]
previous_chapter: CH-37
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH38
    text: |
      Al terminar este capítulo podrás decidir cómo la identidad de quien llama restringe la admisión,
      la política y las credenciales sin concederle nunca más de lo que la regla base permite, y
      explicar cómo las entradas pendientes, la compactación, la auditoría y la retención se
      sostienen dentro del turno durable, también después de una caída.
  skeleton:
    id: SK-CH38
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
    contracts_to_be_introduced: []
  guiding_questions:
    - id: GQ-CH38-01
      text: |
        Si una regla de política permite leer facturas, ¿debería una regla basada en quién llama poder
        ampliar ese permiso a quien no lo tenía? ¿Y restringirlo?
      answered_by: RQ-CH38-01
    - id: GQ-CH38-02
      text: |
        Si un usuario escribe "espera, cambia de plan" justo antes de que el proceso se caiga, ¿cómo
        se asegura el arnés de que ese mensaje no se pierda ni se aplique dos veces?
      answered_by: RQ-CH38-02
    - id: GQ-CH38-03
      text: |
        Si el proceso se cae mientras el modelo resume una conversación larga, ¿hay que volver a pedir
        el resumen, o se puede aprovechar lo que ya llegó?
      answered_by: RQ-CH38-03
    - id: GQ-CH38-04
      text: |
        ¿Qué decisiones deberían quedar como evidencia que nadie pueda borrar, y cuándo se puede
        borrar el registro de pasos de un run?
      answered_by: RQ-CH38-04
  systems_lens:
    iceberg_visible_fact: |
      El Principal viaja en cada turno desde CH-31, pero la admisión, la política y las credenciales
      siguen decidiendo sin mirarlo; las entradas pendientes y la compactación no sobreviven a una
      caída; nadie audita las capabilities que se declaran seguras de repetir ni quién continuó cada
      sesión; y el journal crece sin retención (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que cada capítulo de v0.2 introdujo un dato — Principal, PendingInput,
      CompactionSummary, ReplayPolicy, StepRecord — y dejó "para la integración" que las decisiones
      ya existentes lo usaran; CH-36 no lo hizo (ver sección 3).
    iceberg_structures: |
      Este capítulo amplía AdmissionController, PolicyEngine, CredentialBroker y DataGovernanceEngine
      dentro de sus owns, y agrega cinco funciones de integración; la compactación pasa a ser un paso
      del journal y las entradas pendientes salen de la cola solo al comprometerse su paso (ver
      sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-13 (la identidad solo restringe; la autorización sigue siendo de
      PolicyEngine), P-32 (el paso es la unidad de recuperación, también para la compactación), P-25
      (la evidencia de auditoría no es telemetría) y P-22 (el dato del journal tiene retención) (ver
      sección 4).
    reinforcing_loop: |
      Si una regla de identidad pudiera conceder permisos, cada excepción por usuario agregaría un
      camino de autorización nuevo, y cada camino nuevo haría más difícil saber qué está permitido. Que
      la identidad solo restrinja corta la espiral: la regla base sigue siendo el techo.
    balancing_loop: |
      La confirmación al comprometer es el mecanismo de equilibrio: por muchas caídas que haya, una
      entrada pendiente sale de la cola exactamente una vez, junto con el paso que la aplicó.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es tratar la compactación como un paso del journal
      sin tool call: así su recuperación usa las acciones de CH-32 sin cambios, y la propuesta de
      resumen ya recibida nunca se vuelve a pagar.
  recall_questions:
    - id: RQ-CH38-01
      text: |
        ¿De qué decisión parte evaluatePolicyForCaller, en qué caso la convierte en DENY, y por qué
        nunca convierte un DENY en ALLOW? ¿Qué hace admitWithPrincipalRules con un conjunto de reglas
        vacío?
    - id: RQ-CH38-02
      text: |
        ¿Qué devuelve takePendingInputsForStep, y cuándo confirmPendingInputsAfterCommit devuelve la cola
        sin cambios?
    - id: RQ-CH38-03
      text: |
        ¿Qué registra compactHistoryInDurableTurn en el StepRecord, y qué acción de RecoveryDecision
        corresponde a un corte antes de la propuesta y a uno después?
    - id: RQ-CH38-04
      text: |
        ¿Qué registran auditSafeReplayDeclaration y auditSessionContinuation, con qué función de CH-19, y
        qué exige evaluateJournalRetention antes de dejar que enforceRetention decida?
  explain_prompts:
    - id: EP-CH38-01
      text: |
        PolicyEngine ya decidía si una tool call está permitida. Explica, como si hablaras con alguien
        sin contexto técnico, por qué la regla basada en quién llama se evalúa después de la regla base
        y solo puede restringirla, y qué se rompería si pudiera ampliarla.
      target_entity: CMP-005
    - id: EP-CH38-02
      text: |
        Explica por qué tratar la compactación como un paso del journal no necesita ningún cambio en
        ExecutionJournal, y qué decide decideStepRecovery con un paso de compactación interrumpido.
      target_entity: CMP-023
  interleaved_questions:
    - id: IQ-CH38-01
      text: |
        En CH-29, applyHistoryCompaction recibía la propuesta de resumen del modelo y ContextEngine
        decidía si era válida, sin invocar al modelo. ¿Qué agrega CH-38 alrededor de esa función para
        que una caída no obligue a pedir el resumen otra vez, y por qué la fase de recorte sin modelo no
        necesita journal?
      current_chapter_entities: [CMP-023]
      prior_chapter_entities: [C-037, CMP-004]
      prior_chapter: CH-29
  flashcards:
    - id: FC-CH38-01
      front: |
        ¿Qué hace admitWithPrincipalRules (AdmissionController) y qué no puede hacer?
      back: |
        Parte de admitWithVerifiedIdentity (CH-31) y, si hubo ADMIT con reglas configuradas, exige que
        alguna PrincipalAdmissionRule coincida con el Principal (tipo, tenant, emisor). Puede convertir
        un ADMIT en REJECT; nunca un REJECT en ADMIT. Reglas vacías no conceden nada.
      source_entity: CMP-012
      chapter_introduced_in: CH-38
      review_stage: DAY_1
    - id: FC-CH38-02
      front: |
        ¿Cuándo sale una PendingInput (C-036) de la cola en el turno durable?
      back: |
        Solo cuando el paso que la incluyó quedó COMMITTED (confirmPendingInputsAfterCommit). Si el
        proceso se cae antes, la cola no cambió y la recuperación la vuelve a aplicar.
      source_entity: C-036
      chapter_introduced_in: CH-38
      review_stage: DAY_1
    - id: FC-CH38-03
      front: |
        ¿Cuándo puede borrarse el journal de un run (DataGovernanceEngine)?
      back: |
        Solo si el run terminó y no tiene pasos STARTED; entonces decide enforceRetention (CH-20), y la
        preservación legal suspende el borrado. Un run vivo o con un paso abierto siempre es
        NOT_YET_DUE.
      source_entity: CMP-018
      chapter_introduced_in: CH-38
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH38-01
      recall_question: RQ-CH38-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH38-02
      recall_question: RQ-CH38-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH38-03
      recall_question: RQ-CH38-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH38-04
      recall_question: RQ-CH38-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 38 — Identidad, Auditoría y Retención en Todo el Turno

> **Regla de v0.2.1:** la identidad restringe, nunca concede; y lo que el turno recibe, resume, audita
> o guarda tiene que sobrevivir a una caída.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir cómo la identidad de quien llama
restringe la admisión, la política y las credenciales sin concederle nunca más de lo que la regla base
permite. También podrás explicar cómo las entradas pendientes, la compactación, la auditoría y la
retención se sostienen dentro del turno durable, también después de una caída.

**Esqueleto.** Segundo y último capítulo de la versión 0.2.1 (`registry/debt.yaml`: D-001..D-008). No
introduce componentes ni contratos: amplía cuatro componentes dentro de lo que ya poseen y agrega
cinco funciones de integración.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si una regla de política permite leer facturas, ¿debería una regla basada en quién llama poder
   ampliar ese permiso a quien no lo tenía? ¿Y restringirlo?
2. Si un usuario escribe "espera, cambia de plan" justo antes de que el proceso se caiga, ¿cómo se
   asegura el arnés de que ese mensaje no se pierda ni se aplique dos veces?
3. Si el proceso se cae mientras el modelo resume una conversación larga, ¿hay que volver a pedir el
   resumen, o se puede aprovechar lo que ya llegó?
4. ¿Qué decisiones deberían quedar como evidencia que nadie pueda borrar, y cuándo se puede borrar el
   registro de pasos de un run?

## 1. Arquitectura Actual (Current Architecture)

- **CH-31** hace viajar el `Principal` en cada turno (`execution.caller`), pero:
  - `evaluateAdmissionForActivationRequest` (CH-14) sigue recibiendo solo el `ActivationRequest`;
  - `evaluatePolicyForToolCall` (CH-05) no mira al llamante;
  - `resolveCredentialReference` (CH-16) no distingue de quién es la credencial.
- **CH-28** encola `PendingInput` (C-036) en una `PendingInputQueue` y las aplica en los bordes del
  turno, en memoria.
- **CH-29** compacta el historial con una propuesta del modelo (`applyHistoryCompaction`), fuera del
  journal.
- **CH-30** permite declarar `SAFE` una capability, y así autoriza que se repita un efecto
  desconocido (INV-E17). **CH-34** decide que un estímulo continúa una sesión.
- **CH-19** registra evidencia write-once (`recordAuditEntry`). **CH-20** clasifica datos y decide
  su retención (`classifyData`, `enforceRetention`).
- **CH-32** registra cada paso en el journal, pero nada decide cuándo borrarlo.

## 2. El Problema (Problem)

Cada capítulo de la versión 0.2 agregó un dato, y ninguna decisión existente lo usa todavía:
- **la identidad no decide nada.** Cualquier `Principal` admitido puede usar cualquier capability
  que la política general permita, aunque la regla del negocio sea "solo usuarios de este tenant";
- **una entrada pendiente se pierde en una caída.** Si el proceso se cae después de sacarla de la
  cola y antes de comprometer el paso, desaparece;
- **una compactación interrumpida se paga dos veces**, porque el resumen del modelo no queda
  registrado en ningún lado;
- **nadie deja evidencia** de qué capabilities se declararon `SAFE`, aunque esa declaración autoriza
  repetir un efecto, ni de quién continuó cada sesión;
- **el journal crece sin límite** y guarda respuestas y resultados que pueden ser datos personales.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **Cambiar las firmas de CH-05, CH-14 y CH-16 reabriría todo el libro.** La identidad tiene que
  entrar como una decisión adicional, compuesta con la existente.
- **Una decisión adicional podría ampliar permisos por accidente.** Si una regla por usuario pudiera
  convertir un `DENY` en `ALLOW`, la política dejaría de ser un techo (P-13).
- **La cola de CH-28 no sabe de pasos.** `selectPendingInputsAtBoundary` devuelve la cola restante,
  pero no hay regla de cuándo persistirla.
- **La compactación de CH-29 no tiene unidad de recuperación**, aunque CH-32 ya tiene una que le
  serviría sin cambios.
- **Un evento no es evidencia** (P-25). `TOOL_REPLAY_DECIDED` (CH-30) observa, pero no preserva.
- **`enforceRetention` no sabe si un run sigue vivo.** Aplicada al journal sin más, podría borrar
  los pasos que una recuperación necesita.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-13   Authorization is deterministic and external to the LLM.
           La identidad solo restringe una decisión base de PolicyEngine o AdmissionController.
    P-17   Admission precedes execution.
           admitWithPrincipalRules parte de admitWithVerifiedIdentity (CH-31).
    P-22   Enterprise data is governed throughout its lifecycle.
           El journal se clasifica y tiene retención, suspendida por legal hold.
    P-25   Audit evidence is distinct from operational telemetry.
           Las declaraciones SAFE y las continuaciones van a AuditLedger, no solo a eventos.
    P-31   Identity travels with every turn.
           Ahora también decide: admisión, política y credenciales.
    P-32   A step is the unit of durability and recovery.
           La compactación es un paso; una entrada pendiente se confirma con su paso.

Invariants preserved
    INV-07   el resumen recuperado vuelve al historial como el nuevo
    INV-13   la cola y la compactación se reconstruyen desde estado persistido
    INV-19   la continuación queda trazada hasta su Principal
    INV-E07  la credencial se resuelve para el tenant del llamante
    INV-E10  cada registro de auditoría lleva su VersionSnapshot
    INV-E17  cada declaración SAFE queda auditada

Component ownership changes
    Ninguno nuevo. AdmissionController, PolicyEngine, CredentialBroker y DataGovernanceEngine
    ganan funciones dentro de sus owns (ver sección 8).

Contract changes
    Ninguno. Tipos embebidos: PrincipalAdmissionRule, CallerPolicyRule, CompactionStepOutcome.

Deterministic vs agentic boundary
    Sin cambios: el modelo propone el resumen; su aplicación, la identidad, la auditoría y la
    retención son determinísticas.
```

## 5. Conceptos Nuevos (New Concepts)

- **La identidad restringe, nunca concede** (*identity narrows, never widens*): una regla basada en
  el `Principal` se evalúa después de la regla base y solo puede convertir un permiso en rechazo. La
  regla base sigue siendo el techo.
- **Entrada confirmada al comprometer** (*commit-acknowledged input*): una entrada pendiente se aplica
  a un paso, pero sale de la cola solo cuando ese paso queda `COMMITTED`. Si el proceso se cae antes,
  la cola sigue igual y la recuperación la vuelve a aplicar.
- **Compactación como paso:** pedir el resumen es una llamada al modelo sin tool call, así que es un
  paso del journal. La propuesta queda en `modelResponse`, y aplicarla es determinístico.
- **Evidencia de decisiones de confianza:** declarar una capability `SAFE` y continuar la sesión de
  otro son decisiones que alguien puede cuestionar después. Por eso quedan en el `AuditLedger`, que no
  se puede editar.
- **Retención del journal:** el journal es un dato del turno, con la misma retención que cualquier
  otro, pero nunca se evalúa mientras el run puede necesitarlo para recuperarse.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `ActivationRequest` (C-022), `AdmissionDecision` (C-023), `Principal` (C-040),
  `PolicyDecision` (C-014), `ToolCall` (C-008), `CapabilityDescriptor` (C-018),
  `CredentialReference` (C-026), `PendingInput` (C-036), `CompactionSummary` (C-037), `StepRecord`
  (C-042), `ModelResponse` (C-007), `AuditRecord` (C-029), `DataGovernanceLabel` (C-030),
  `ExecutionBudget` (C-012), `AgentState` (C-003), `AgentMessage` (C-001), `ExecutionContext`
  (C-004), `HarnessError` (C-011);
- **primitivos:** `AgentId`, `CapabilityId`, `Timestamp`.

| Identificador (heredado, sin `C-XXX` propio) | Introducido en | Rol en este capítulo |
|---|---|---|
| `PrincipalType` | CH-31 §6 | `USER` / `SERVICE` / `RUNTIME` en las reglas por llamante |
| `ProcessMode` | CH-31 §6 | modo del proceso, que la admisión recibe |
| `PendingInputQueue` | CH-28 §6 | la cola de entradas pendientes |
| `PendingInputSelection` | CH-28 §6 | lo aplicado y la cola restante |
| `CompactionPolicy` | CH-29 §6 | límites de la compactación |
| `CompactionPlan` | CH-29 §6 | corte, región antigua y si hace falta resumen |
| `ContinuationRoute` | CH-34 §6 | la decisión continuar / activar |
| `VersionSnapshot` | CH-19 §6 | versiones exactas en cada registro de auditoría |
| `ActorId` | CH-06 §6 | actor de un registro de auditoría |
| `CredentialClassification` | CH-16 §6 | clasificación de la credencial |
| `RetentionEnforcementResult` | CH-20 §6 | el resultado de evaluar la retención |
| `ErrorCategory` | CH-00 | reutiliza `ADMISSION`, `POLICY` y `CONTEXT` |

### `PrincipalAdmissionRule` — quién puede entrar (embebido)

```pseudocode
STRUCT PrincipalAdmissionRule
    principalType: Optional<PrincipalType>
    tenantId: Optional<Text>
    issuer: Optional<Text>
END
```

Un campo `NULL` significa "cualquiera". Una regla con los tres campos en `NULL` admite a cualquier
`Principal` verificado, y es una decisión explícita, no un default.

### `CallerPolicyRule` — qué llamante puede usar una capability (embebido)

```pseudocode
STRUCT CallerPolicyRule
    ruleId: Text
    capability: CapabilityId
    requiredPrincipalType: Optional<PrincipalType>
    requireTenant: Boolean
END
```

### `CompactionStepOutcome` — lo que deja una compactación durable (embebido)

```pseudocode
STRUCT CompactionStepOutcome
    history: List<AgentMessage>
    step: Optional<StepRecord>
END
```

`step` solo tiene valor si la compactación necesitó un resumen del modelo.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

**Este capítulo no introduce ni modifica contratos**, por la restricción de la versión 0.2.1.
`registry/contracts.yaml` sigue en 48 contratos.

## 8. Responsabilidades de Componentes (Component Responsibilities)

**Este capítulo no introduce componentes.** Cuatro componentes ganan funciones dentro de su `owns`
literal:

```text
AdmissionController (CMP-012)
    owns: "apply identity, authorization, tenant … decisions before routing" (P-17)
    nuevas: principalRulesGrantAccess, admitWithPrincipalRules

PolicyEngine (CMP-005)
    owns: la autorización determinística de cada acción (P-13)
    nueva: evaluatePolicyForCaller — solo restringe la decisión de evaluatePolicyForToolCall

CredentialBroker (CMP-014)
    owns: "Tenant data, memory, credentials … are isolated" (INV-E07, aplicado a credenciales)
    nueva: resolveCallerCredentialReference — exige un llamante USER con tenant (requireTenantCaller)

DataGovernanceEngine (CMP-018)
    owns: los requisitos de gobierno de un dato, incluida su retención (P-22)
    nueva: evaluateJournalRetention — nunca evalúa un run vivo ni un paso abierto
```

`AuditLedger` (CMP-017) **no cambia**: las dos funciones de auditoría de este capítulo son de
integración y usan `recordAuditEntry` (CH-19) tal cual. Tampoco cambian `ExecutionJournal`,
`AgentLoop` ni `ContextEngine`: la durabilidad de la cola y de la compactación sale de componer sus
funciones con el journal.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
Identidad (D-005, D-006)
    admitWithPrincipalRules  → admitWithVerifiedIdentity (CH-31) → principalRulesGrantAccess
    evaluatePolicyForCaller  → evaluatePolicyForToolCall (CH-05) → CallerPolicyRule
    resolveCallerCredentialReference → requireTenantCaller (CH-31) → resolveCredentialReference (CH-16)

Durabilidad (D-001, D-002, D-003)
    takePendingInputsForStep        → selectPendingInputsAtBoundary (CH-28, BEFORE_MODEL_CALL)
    confirmPendingInputsAfterCommit → solo con el paso COMMITTED (CH-32)
    compactHistoryInDurableTurn     → shouldCompactHistory / planHistoryCompaction (CH-29)
                                      → beginStep → invokeModelForTurn (CH-03) → recordModelResponse
                                      → applyHistoryCompaction (CH-29) → commitStep (CH-32)

Auditoría (D-004, D-007)
    auditSafeReplayDeclaration → effectiveReplayPolicy (CH-30) → recordAuditEntry (CH-19)
    auditSessionContinuation   → ContinuationRoute (CH-34) → recordAuditEntry (CH-19)

Retención (D-008)
    classifyData (CH-20, provenance "execution_journal") → evaluateJournalRetention → enforceRetention (CH-20)
```

**Dónde entra cada una en el turno durable (CH-36):**
- `admitWithPrincipalRules` reemplaza a `admitWithVerifiedIdentity` dentro de `enterDurableTurn`;
- `auditSessionContinuation` va después de un `CONTINUE_SESSION`;
- `evaluatePolicyForCaller` reemplaza a `evaluatePolicyForToolCall` en `runDurableGovernedStep`;
- `resolveCallerCredentialReference` se usa cuando la tool necesita la credencial del usuario;
- antes de cada paso: `compactHistoryInDurableTurn` y luego `takePendingInputsForStep`; después de
  `commitStep`: `confirmPendingInputsAfterCommit`;
- `auditSafeReplayDeclaration` corre al registrar una capability (CH-08), antes de cualquier run.

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
AdmissionController (identidad) → PolicyEngine (identidad) → CredentialBroker (tenant)
ContextEngine + ExecutionJournal (compactación como paso) → AgentLoop + ExecutionJournal (cola)
AuditLedger (SAFE, continuaciones) · DataGovernanceEngine (retención del journal)
```

**Vista 2 — Sequence: un paso con entrada pendiente, compactación y una caída**

```text
compactHistoryInDurableTurn → paso 7: STARTED → resumen del modelo → recordModelResponse
   ▼ (caída del proceso antes de commitStep)
recoverRun (CH-32): paso 7 STARTED, con respuesta y sin tool call → COMMIT_RECORDED
   │ applyHistoryCompaction con la propuesta registrada → commitStep (el resumen no se pide de nuevo)
takePendingInputsForStep → "cambia de plan" entra en el paso 8 (la cola todavía la conserva)
   │ paso 8 → COMMITTED → confirmPendingInputsAfterCommit → la entrada sale de la cola
```

**Vista 2b — Sequence: la identidad restringe**

```text
evaluatePolicyForCaller(call "leer facturas", execution)
   │ evaluatePolicyForToolCall → ALLOW
   │ CallerPolicyRule(capability = "leer facturas", requireTenant = TRUE)
   │ caller.current es SERVICE sin tenant → DENY CALLER_NOT_PERMITTED
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

### AdmissionController: reglas por Principal (D-005)

```pseudocode
FUNCTION principalRulesGrantAccess(
    principal: Principal,
    rules: List<PrincipalAdmissionRule>
) -> Boolean

    FOR EACH rule IN rules
        typeMatches: Boolean = rule.principalType == NULL OR rule.principalType == principal.principalType
        tenantMatches: Boolean = rule.tenantId == NULL OR rule.tenantId == principal.tenantId
        issuerMatches: Boolean = rule.issuer == NULL OR rule.issuer == principal.issuer

        IF typeMatches AND tenantMatches AND issuerMatches
            RETURN TRUE
        END
    END

    RETURN FALSE
END
```

```pseudocode
FUNCTION admitWithPrincipalRules(
    request: ActivationRequest,
    verifiedPrincipal: Optional<Principal>,
    admissionConfigured: Boolean,
    processMode: ProcessMode,
    rules: List<PrincipalAdmissionRule>
) -> AdmissionDecision

    base: AdmissionDecision = admitWithVerifiedIdentity(
        request, verifiedPrincipal, admissionConfigured, processMode
    )

    IF base.outcome != ADMIT OR NOT admissionConfigured
        RETURN base
    END

    IF principalRulesGrantAccess(base.principal, rules)
        RETURN base
    END

    RETURN AdmissionDecision(
        requestId = request.id,
        outcome = REJECT,
        reason = HarnessError(
            category = ADMISSION,
            code = "PRINCIPAL_NOT_ADMITTED",
            message = "El llamante está verificado, pero ninguna regla de admisión por Principal lo admite",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        ),
        principal = NULL,
        decidedAt = now()
    )
END
```

### PolicyEngine y CredentialBroker: decidir con el llamante (D-006)

```pseudocode
FUNCTION evaluatePolicyForCaller(
    call: ToolCall,
    execution: ExecutionContext,
    agentId: AgentId,
    callerRules: List<CallerPolicyRule>
) -> PolicyDecision

    base: PolicyDecision = evaluatePolicyForToolCall(call, execution, agentId)

    IF base.outcome == DENY
        RETURN base
    END

    FOR EACH rule IN callerRules
        IF rule.capability == call.capability
            typeAllowed: Boolean = rule.requiredPrincipalType == NULL
                OR (execution.caller != NULL AND execution.caller.current.principalType == rule.requiredPrincipalType)
            tenantAllowed: Boolean = NOT rule.requireTenant
                OR (execution.caller != NULL AND execution.caller.current.tenantId != NULL)

            IF NOT typeAllowed OR NOT tenantAllowed
                RETURN PolicyDecision(
                    callId = call.id,
                    outcome = DENY,
                    policyRuleId = rule.ruleId,
                    reason = HarnessError(
                        category = POLICY,
                        code = "CALLER_NOT_PERMITTED",
                        message = "La regla base permite la acción, pero este llamante no cumple la regla por Principal de la capability",
                        recoverable = FALSE,
                        retryable = FALSE,
                        metadata = {}
                    ),
                    decidedAt = now()
                )
            END
        END
    END

    RETURN base
END
```

```pseudocode
FUNCTION resolveCallerCredentialReference(
    descriptor: CapabilityDescriptor,
    credentialName: Text,
    classification: CredentialClassification,
    credentialBelongsToCapability: Boolean,
    secretExistsForCaller: Boolean,
    expiresAt: Optional<Timestamp>,
    execution: ExecutionContext,
    agentId: AgentId
) -> CredentialReference

    caller: Principal = requireTenantCaller(execution)

    RETURN resolveCredentialReference(
        descriptor, credentialName, classification, credentialBelongsToCapability,
        secretExistsForCaller, expiresAt, execution, agentId
    )
END
```

`secretExistsForCaller` es la respuesta del Secret Store para la clave (tenant, principal,
`credentialName`) de `caller`. `requireTenantCaller` (CH-31) lanza `TENANT_CALLER_REQUIRED` antes de
que se consulte nada si el llamante no es un usuario con tenant.

### Integración: entradas pendientes y compactación durables (D-001, D-002, D-003)

```pseudocode
FUNCTION takePendingInputsForStep(
    queue: PendingInputQueue,
    state: AgentState,
    execution: ExecutionContext
) -> PendingInputSelection

    RETURN selectPendingInputsAtBoundary(queue, BEFORE_MODEL_CALL, state, execution)
END
```

```pseudocode
FUNCTION confirmPendingInputsAfterCommit(
    queue: PendingInputQueue,
    selection: PendingInputSelection,
    step: StepRecord
) -> PendingInputQueue

    IF step.status != COMMITTED
        RETURN queue
    END

    RETURN selection.remaining
END
```

```pseudocode
FUNCTION compactHistoryInDurableTurn(
    history: List<AgentMessage>,
    estimatedTokens: Integer,
    budget: ExecutionBudget,
    policy: CompactionPolicy,
    state: AgentState,
    previousStep: Optional<StepRecord>,
    turn: Integer,
    index: Integer,
    proposalContent: Value,
    proposal: Optional<CompactionSummary>,
    resultPersisted: Boolean,
    execution: ExecutionContext
) -> CompactionStepOutcome

    IF NOT shouldCompactHistory(estimatedTokens, budget, policy)
        RETURN CompactionStepOutcome(history = history, step = NULL)
    END

    plan: CompactionPlan = planHistoryCompaction(history, estimatedTokens, budget, policy)

    IF NOT plan.needsSummary
        trimmed: List<AgentMessage> = applyHistoryCompaction(plan, NULL, execution, state.agentId)
        RETURN CompactionStepOutcome(history = trimmed, step = NULL)
    END

    step: StepRecord = beginStep(execution.runId, turn, index, previousStep)

    response: ModelResponse = invokeModelForTurn(
        state, execution, plan.olderRegion, TRUE, TRUE, FALSE, "", {}, proposalContent
    )

    step = recordModelResponse(step, response)

    compacted: List<AgentMessage> = applyHistoryCompaction(plan, proposal, execution, state.agentId)
    committed: StepRecord = commitStep(step, resultPersisted, execution, state.agentId)

    RETURN CompactionStepOutcome(history = compacted, step = committed)
END
```

`proposalContent` es el contenido que el proveedor devuelve (la señal de CH-03), y `proposal` es su
lectura como `CompactionSummary`. `response.content` guarda esa misma propuesta en el journal.

### Integración: auditoría de decisiones de confianza (D-004, D-007)

```pseudocode
FUNCTION auditSafeReplayDeclaration(
    descriptor: CapabilityDescriptor,
    subjectRef: Text,
    versionSnapshot: VersionSnapshot,
    actor: ActorId
) -> Optional<AuditRecord>

    IF effectiveReplayPolicy(descriptor) != SAFE
        RETURN NULL
    END

    RETURN recordAuditEntry(subjectRef, versionSnapshot, actor, NULL, NULL)
END
```

```pseudocode
FUNCTION auditSessionContinuation(
    route: ContinuationRoute,
    principal: Principal,
    subjectRef: Text,
    versionSnapshot: VersionSnapshot
) -> Optional<AuditRecord>

    IF route.action != CONTINUE_SESSION
        RETURN NULL
    END

    RETURN recordAuditEntry(subjectRef, versionSnapshot, principal.principalId, NULL, NULL)
END
```

`subjectRef` identifica lo auditado (la capability y su política, o la sesión y la dirección). Los
dos registros se escriben sin `ExecutionContext`, igual que la auditoría de admisión de CH-26: pueden
ocurrir antes de que exista un run.

### DataGovernanceEngine: retención del journal (D-008)

```pseudocode
FUNCTION evaluateJournalRetention(
    steps: List<StepRecord>,
    label: DataGovernanceLabel,
    runFinished: Boolean,
    evaluatedAt: Timestamp,
    execution: Optional<ExecutionContext>,
    agentId: Optional<AgentId>
) -> RetentionEnforcementResult

    openStep: Boolean = FALSE

    FOR EACH step IN steps
        IF step.status == STARTED
            openStep = TRUE
        END
    END

    IF NOT runFinished OR openStep
        RETURN RetentionEnforcementResult(
            label = label,
            outcome = NOT_YET_DUE,
            evaluatedAt = evaluatedAt
        )
    END

    RETURN enforceRetention(label, evaluatedAt, execution, agentId)
END
```

`label` sale de `classifyData(subjectRef, "execution_journal", legalHold, …)` (CH-20), con el run como
sujeto. `now` es una utilidad primitiva.

Nótese lo que estas funciones **no** hacen:
- ninguna cambia la firma de CH-05, CH-14 ni CH-16;
- ninguna concede un permiso que la regla base deniega;
- ninguna modifica `ExecutionJournal`: la compactación y la cola usan sus funciones tal cual;
- ninguna borra un registro de auditoría: `AuditLedger` sigue siendo write-once.

## 12. Transiciones de Estado (State Transitions)

```text
Admisión con Principal
    admitWithVerifiedIdentity REJECT               → REJECT (sin cambios)
    ADMIT sin reglas configuradas (desarrollo)     → ADMIT (sin cambios)
    ADMIT + alguna regla coincide                  → ADMIT
    ADMIT + ninguna regla coincide (o reglas [])   → REJECT PRINCIPAL_NOT_ADMITTED

Política con llamante
    base DENY                     → DENY
    base ALLOW / REQUIRE_APPROVAL → la misma, o DENY CALLER_NOT_PERMITTED

Entrada pendiente
    en cola → aplicada al paso N → (paso N COMMITTED) fuera de la cola
                                 → (caída antes)       sigue en la cola, se vuelve a aplicar

Paso de compactación
    STARTED → +modelResponse (propuesta) → COMMITTED
    recuperación: sin respuesta → REEXECUTE_MODEL_CALL; con respuesta → COMMIT_RECORDED

Retención del journal
    run vivo o paso STARTED → NOT_YET_DUE
    run terminado → enforceRetention: NOT_YET_DUE | DELETION_DUE | SUSPENDED_BY_LEGAL_HOLD
```

## 13. Semántica de Fallos (Failure Semantics)

Códigos nuevos de `HarnessError`, con `ErrorCategory` ya existentes:

```text
ADMISSION  PRINCIPAL_NOT_ADMITTED   (reason de un REJECT, sin evento: todavía no hay run)
POLICY     CALLER_NOT_PERMITTED     (reason de una PolicyDecision DENY)
```

`resolveCallerCredentialReference` hereda `TENANT_CALLER_REQUIRED` (CH-31) y los fallos de
`resolveCredentialReference` (CH-16). `compactHistoryInDurableTurn` hereda los de
`applyHistoryCompaction` (CH-29) y los del journal (CH-32).

## 14. Eventos Producidos (Events Produced)

Ningún `AgentEventType` nuevo. Se reutilizan:
- `STEP_COMMITTED` (CH-32), para el paso de compactación;
- `RETENTION_ENFORCEMENT_EVALUATED` (CH-20);
- los eventos de `AuditLedger` (CH-19).

Las dos auditorías de este capítulo producen **evidencia**, no telemetría (P-25).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **La política base es el techo.** Una regla por llamante nunca amplía un permiso. Quitar todas las
  reglas por llamante deja la política como estaba, nunca más permisiva.
- **Reglas de admisión vacías no admiten a nadie**, una vez configurada la admisión. Admitir a
  cualquier `Principal` verificado exige escribir esa regla explícitamente.
- **La credencial es del usuario, no del agente.** `resolveCallerCredentialReference` exige un
  usuario con tenant; un servicio o el runtime no pueden usar la credencial de una persona.
- **Declarar `SAFE` deja rastro.** Quien marque como repetible una capability que envía dinero queda
  identificado en la evidencia, con las versiones exactas.
- **Continuar la sesión de otro deja rastro**, con el `Principal` que la continuó.
- **El journal no es eterno ni se borra a destiempo.** Contiene respuestas y resultados que pueden
  ser datos personales, así que tiene retención; pero nunca se evalúa mientras la recuperación podría
  necesitarlo, y la preservación legal lo protege.

## 16. Tests (Tests)

```text
TEST PrincipalRulesNeverAdmitAfterABaseReject
TEST EmptyPrincipalRulesRejectOnceAdmissionIsConfigured
TEST DevelopmentAdmissionSkipsPrincipalRules
TEST CallerPolicyNeverTurnsDenyIntoAllow
TEST CallerPolicyTurnsAllowIntoDenyForAServiceWithoutTenant
TEST CallerPolicyKeepsRequireApprovalWhenTheCallerQualifies
TEST CallerCredentialRequiresAUserWithTenant
TEST PendingInputStaysQueuedUntilItsStepCommits
TEST PendingInputIsReappliedAfterACrashBeforeCommit
TEST CompactionWithoutSummaryDoesNotOpenAStep
TEST CompactionSummaryIsRecordedBeforeItIsApplied
TEST InterruptedCompactionAfterTheProposalIsCommittedWithoutCallingTheModel
TEST SafeDeclarationIsAudited
TEST NeverDeclarationIsNotAudited
TEST SessionContinuationIsAuditedWithItsPrincipal
TEST JournalOfALiveRunIsNeverDue
TEST JournalWithAStartedStepIsNeverDue
TEST LegalHoldSuspendsJournalDeletion
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (v0.2.1, después de CH-38) — 26 componentes, 48 contratos, 39 capítulos

AdmissionController (CMP-012)   + principalRulesGrantAccess, admitWithPrincipalRules
PolicyEngine (CMP-005)          + evaluatePolicyForCaller
CredentialBroker (CMP-014)      + resolveCallerCredentialReference
DataGovernanceEngine (CMP-018)  + evaluateJournalRetention
Integración                     + takePendingInputsForStep, confirmPendingInputsAfterCommit,
                                  compactHistoryInDurableTurn, auditSafeReplayDeclaration,
                                  auditSessionContinuation

Deuda de v0.2: D-001..D-014 resueltas. Quedan solo las 12 con destino en v0.3.
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **Conexiones, datos y memoria con el llamante** (D-018, D-019): son de CH-41 y CH-42, que
  introducen esos componentes.
- **Reglas de política más ricas por Principal** (atributos, horarios, jerarquías): el
  `CallerPolicyRule` cubre tipo y tenant, que es lo que INV-E07 exige.
- **Reescribir `enterDurableTurn` y `runDurableGovernedStep` (CH-36)** con las funciones nuevas: la
  sección 9 dice dónde entra cada una. El turno conectado de la versión 0.3 (CH-49) las usa
  directamente.

## 19. Siguiente Incremento (Next Increment)

Con este capítulo se cierra la deuda de la versión 0.2: toda decisión prometida a "la integración"
tiene función, y `registry/debt.yaml` ya no tiene deudas abiertas con destino en v0.2.1. Antes del
siguiente capítulo se cierra la **versión 0.2.1**.

Después empieza la versión 0.3 con **el modelo como dato**: catálogo, costo y cache.

Será CH-39 ("El Modelo como Dato: Catálogo, Costo y Cache"). `next_chapter` queda en `null` porque
CH-39 todavía no existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): la identidad no decide nada; la cola y la compactación no sobreviven a
   una caída; nadie audita `SAFE` ni las continuaciones; el journal no tiene retención.
2. **Patrones** (= §3): cada capítulo de v0.2 agregó un dato y dejó para la integración que las
   decisiones existentes lo usaran.
3. **Estructuras** (= §8): funciones nuevas en cuatro componentes y cinco de integración, sin
   contratos nuevos.
4. **Modelos mentales** (= §4): P-13, P-32, P-25 y P-22.

**Bucles de retroalimentación**

- **Refuerzo:** reglas por usuario que conceden permisos multiplican los caminos de autorización.
  Que la identidad solo restrinja corta la espiral.
- **Equilibrio:** la confirmación al comprometer. Una entrada sale de la cola exactamente una vez.

**Punto de apalancamiento**

La decisión con mayor efecto es tratar la compactación como un paso del journal sin tool call: su
recuperación usa las acciones de CH-32 sin cambios, y el resumen ya recibido nunca se vuelve a pagar.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿De qué decisión parte `evaluatePolicyForCaller`, en qué caso la convierte en `DENY`, y por qué
   nunca convierte un `DENY` en `ALLOW`? ¿Qué hace `admitWithPrincipalRules` con un conjunto de reglas
   vacío? *(pregunta guía 1)*
2. ¿Qué devuelve `takePendingInputsForStep`, y cuándo `confirmPendingInputsAfterCommit` devuelve la
   cola sin cambios? *(pregunta guía 2)*
3. ¿Qué registra `compactHistoryInDurableTurn` en el `StepRecord`, y qué acción de
   `RecoveryDecision` corresponde a un corte antes de la propuesta y a uno después? *(pregunta guía 3)*
4. ¿Qué registran `auditSafeReplayDeclaration` y `auditSessionContinuation`, con qué función de
   CH-19, y qué exige `evaluateJournalRetention` antes de dejar que `enforceRetention` decida?
   *(pregunta guía 4)*

### Explicar

1. `PolicyEngine` ya decidía si una tool call está permitida. Explica por qué la regla basada en
   quién llama se evalúa después de la regla base y solo puede restringirla, y qué se rompería si
   pudiera ampliarla.
2. Explica por qué tratar la compactación como un paso del journal no necesita ningún cambio en
   `ExecutionJournal`, y qué decide `decideStepRecovery` con un paso de compactación interrumpido.

### Conectar

1. En CH-29, `applyHistoryCompaction` recibía la propuesta de resumen del modelo y `ContextEngine`
   decidía si era válida, sin invocar al modelo. ¿Qué agrega CH-38 alrededor de esa función para que
   una caída no obligue a pedir el resumen otra vez, y por qué la fase de recorte sin modelo no
   necesita journal?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
