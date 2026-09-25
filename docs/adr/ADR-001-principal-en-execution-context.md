# ADR-001 — El principal verificado viaja en `ExecutionContext`

- **ADR-ID:** ADR-001
- **Title:** El principal verificado viaja en `ExecutionContext`
- **Status:** Proposed (2026-09-24). Pasa a `Accepted` con CH-31, con aprobación humana.

## Context

P-17 asigna a `AdmissionController` (CMP-012) la verificación de "identity, authorization, tenant", pero **ningún contrato lleva el principal verificado más allá de la admisión**:
- `ExecutionContext` (C-004) solo tiene `runId`, `sessionId`, `traceId` y `budget`;
- `ActivationRequest` (C-022) trae un `externalIdentityRef: Text` sin verificar;
- `resolveCredentialReference` (CH-16) recibe `agentId`, no un usuario.

Por eso ni CredentialBroker, ni PolicyEngine, ni la memoria pueden decidir **por usuario o por tenant** sin tomar la identidad de un lugar no verificado.

## Decision

1. Introducir **C-040 `Principal`** (`principalId`, `principalType` USER / SERVICE / RUNTIME, `issuer`, `tenantId?`, `attributes`) y **C-041 `CallerSnapshot`** (`initiator`, `current`) en CH-31.
2. **C-004 `ExecutionContext` v2:** agrega `caller: Optional<CallerSnapshot>`.
3. **C-023 `AdmissionDecision` v2:** agrega `principal: Optional<Principal>`. `AdmissionController` produce el principal mediante `verifyExternalIdentity`, un punto de extensión declarado.
4. `initiator` se fija al crear el run; `current` se renueva en cada entrega.
5. El tenant **solo** sale de `caller.current`, nunca del prompt, de argumentos de tools ni de respuestas externas.

## Alternatives

- **Pasar el principal como argumento de cada función:** contamina todas las firmas y permite que se pierda en una función de integración.
- **Un componente nuevo `IdentityService`:** viola EVO-01, porque la identidad ya es responsabilidad literal de AdmissionController (P-17).
- **Un campo obligatorio (no `Optional`):** invalidaría el pseudocódigo de CH-00..CH-30.

## Consequences

- CredentialBroker, PolicyEngine y la memoria pueden exigir `caller.current`.
- Queda explícito que **la admisión no es propiedad de sesión.** CH-31 debe decir quién valida que `caller.current` puede operar una sesión dada.
- `ExecutionContext` tiene 11 componentes en `used_by`. El cambio no rompe ninguno porque el campo es opcional.

## Constitutional Articles Affected

P-13, P-17, P-31 (Amendment v1.2), INV-19, INV-E07, INV-E15 (Amendment v1.2).

## Migration Strategy

- `caller` es `Optional`: CH-00..CH-30 siguen válidos sin tocarlos.
- Desde CH-31, toda función de integración nueva lo propaga.
- `registry/contracts.yaml`: C-004 y C-023 pasan a `version: v2` con `modified_by: [CH-31]`.
