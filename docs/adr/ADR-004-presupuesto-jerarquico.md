# ADR-004 — El presupuesto es jerárquico

- **ADR-ID:** ADR-004
- **Title:** El presupuesto es jerárquico
- **Status:** **Accepted** (2026-10-10, aprobado por el autor; aplicado en CH-43), con dos ajustes aprobados en la misma decisión (puntos 4 y 5).

## Context

INV-E06 exige que "delegation depth, child runs and delegated cost are bounded by ExecutionBudget". Pero `ExecutionBudget` (C-012) es plano: no hay relación padre-hijo, ni registro de lo consumido, ni un mecanismo de reparto.

`ExecutionUsage` existe solo como una estructura embebida sin contrato propio (`book/chapters/07-execution-controller/chapter.md:588`).

## Decision

1. **Promover C-057 `ExecutionUsage`** a contrato en CH-43, porque ahora cruza la frontera padre-hijo.
2. **C-012 `ExecutionBudget` v2:** agrega `parentRunId: Optional<RunId>` y `consumed: ExecutionUsage`.
3. `ExecutionController` gana `allocateChildBudget(parent, fanout)`, que reparte el saldo restante del padre entre los hijos de un mismo lote (INV-E21).
4. **Ajuste aprobado: `consumed` es `Optional<ExecutionUsage>`**, no obligatorio. Un campo obligatorio habría invalidado todo `ExecutionBudget` construido en CH-00..CH-42; así se sigue la misma regla de compatibilidad que el resto de las versiones v2/v3.
5. **Ajuste aprobado (D-026): `sandboxLimits: Optional<SandboxLimits>`** (CPU, memoria y disco del entorno aislado de CH-35). ExecutionController decide si un uso los supera; un hijo los hereda sin poder ampliarlos.

## Alternatives

- **Presupuesto global por tenant, sin jerarquía:** no impide que un solo hijo consuma el cupo de sus hermanos.
- **Un componente `BudgetAllocator`:** viola EVO-01, porque los límites ya son de ExecutionController (Article III).

## Consequences

- Va antes de CH-44 (invocación entre agentes), por P-09 y EVO-02.
- La delegación hereda límites en lugar de crearlos de cero.

## Constitutional Articles Affected

INV-09, INV-E06, INV-E21 (Amendment v1.2).

## Migration Strategy

- `parentRunId` es `Optional`: un run raíz conserva exactamente su semántica actual.
- `registry/contracts.yaml`: C-012 pasa a `version: v2` con `modified_by: [CH-43]`. Los tres campos nuevos son `Optional`.
