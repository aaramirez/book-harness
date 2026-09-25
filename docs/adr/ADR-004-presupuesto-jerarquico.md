# ADR-004 — El presupuesto es jerárquico

- **ADR-ID:** ADR-004
- **Title:** El presupuesto es jerárquico
- **Status:** Proposed (2026-09-24). Pasa a `Accepted` con CH-41, con aprobación humana.

## Context

INV-E06 exige que "delegation depth, child runs and delegated cost are bounded by ExecutionBudget". Pero `ExecutionBudget` (C-012) es plano: no hay relación padre-hijo, ni registro de lo consumido, ni un mecanismo de reparto.

`ExecutionUsage` existe solo como una estructura embebida sin contrato propio (`book/chapters/07-execution-controller/chapter.md:588`).

## Decision

1. **Promover C-057 `ExecutionUsage`** a contrato en CH-41, porque ahora cruza la frontera padre-hijo.
2. **C-012 `ExecutionBudget` v2:** agrega `parentRunId: Optional<RunId>` y `consumed: ExecutionUsage`.
3. `ExecutionController` gana `allocateChildBudget(parent, fanout)`, que reparte el saldo restante del padre entre los hijos de un mismo lote (INV-E21).

## Alternatives

- **Presupuesto global por tenant, sin jerarquía:** no impide que un solo hijo consuma el cupo de sus hermanos.
- **Un componente `BudgetAllocator`:** viola EVO-01, porque los límites ya son de ExecutionController (Article III).

## Consequences

- Va antes de CH-42 (invocación entre agentes), por P-09 y EVO-02.
- La delegación hereda límites en lugar de crearlos de cero.

## Constitutional Articles Affected

INV-09, INV-E06, INV-E21 (Amendment v1.2).

## Migration Strategy

- `parentRunId` es `Optional`: un run raíz conserva exactamente su semántica actual.
- `registry/contracts.yaml`: C-012 pasa a `version: v2` con `modified_by: [CH-41]`.
