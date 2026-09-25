# ADR-002 — La capability declara su política de replay

- **ADR-ID:** ADR-002
- **Title:** La capability declara su política de replay
- **Status:** **Accepted** (2026-09-25, aprobado por el autor; aplicado en CH-30).

## Context

`IdempotencyGuard` (CMP-015, CH-17) resuelve "¿ya se ejecutó este efecto con esta clave?" con PENDING / COMPLETED. Pero no cubre el caso en que **no se sabe** si el efecto ocurrió, por ejemplo por un crash entre la ejecución y el registro.

La capability tampoco declara si es seguro re-ejecutarla. P-24 e INV-E09 exigen declarar "idempotency, retry and duplicate-delivery behavior", pero `CapabilityDescriptor` (C-018) no tiene dónde hacerlo.

## Decision

1. Introducir **C-039 `ReplayPolicy`** (ENUM `NEVER` / `SAFE`) en CH-30.
2. **C-018 `CapabilityDescriptor` v2:** agrega `replayPolicy: Optional<ReplayPolicy>`. `NULL` se interpreta como **`NEVER`** (fail-closed) mediante `effectiveReplayPolicy`, así ningún descriptor ya registrado cambia de comportamiento.
3. **C-009 `ToolResult` v2:** agrega `outcome: Optional<ToolOutcome>` (SUCCEEDED / FAILED / UNKNOWN). `NULL` se deriva de `succeeded`, como en v1. `UNKNOWN` vuelve al modelo como observación explícita (INV-07), nunca como un éxito inventado.
4. `IdempotencyGuard` gana la decisión "ante un resultado desconocido: re-ejecutar si `SAFE`, reportar `OUTCOME_UNKNOWN` si `NEVER`".
5. **Cuándo un resultado es desconocido (CH-30):** un `IdempotencyRecord` (C-027, CH-17) en `PENDING` cuya ejecución ya no está en curso. El efecto empezó, pero su resultado nunca se registró.

## Alternatives

- **Re-ejecutar siempre el paso interrumpido** (el modelo de eve): duplica efectos no idempotentes y traslada el problema a cada tool.
- **No re-ejecutar nunca:** pierde trabajo seguro de repetir (lecturas).
- **Un booleano `idempotent`:** no distingue "seguro de repetir" de "con clave de idempotencia", que es otra cosa (CH-17).

## Consequences

- Toda capability existente se trata como `NEVER` hasta que se declare lo contrario. Es seguro, aunque conservador.
- CH-32 (ExecutionJournal) consume `ReplayPolicy` para decidir la recuperación por paso (INV-E17).

## Constitutional Articles Affected

P-24, INV-07, INV-11, INV-E09, INV-E17 (Amendment v1.2).

## Migration Strategy

- Default `NEVER`: ningún pseudocódigo previo cambia de comportamiento.
- `registry/contracts.yaml`: C-018 y C-009 pasan a `version: v2` con `modified_by: [CH-30]`.
- C-018 vuelve a cambiar en CH-39 (ADR-005).
