# ADR-003 — La sesión es un árbol navegable con versión de runtime

- **ADR-ID:** ADR-003
- **Title:** La sesión es un árbol navegable con versión de runtime
- **Status:** **Accepted — parte v2** (2026-09-25, aprobado por el autor; aplicada en CH-29). La parte v3 sigue `Proposed` y se acepta con CH-43.

## Context

`SessionManager` (CMP-010, CH-10) ya tiene `branchSessionFromCheckpoint`, y `SessionState` (C-020) tiene `parentCheckpointId`, así que el árbol está insinuado. Pero falta:
- **navegación entre ramas**: no hay noción de rama activa ni resumen de la rama abandonada, a diferencia de las sesiones en árbol de pi;
- **versión del runtime** con la que se creó o migró la sesión. INV-E10 exige registrar versiones exactas por run, pero no dice qué pasa con una sesión larga cuando el runtime cambia.

## Decision

1. **v2 (CH-29):**
   - `SessionState` agrega `activeCheckpointId: Optional<SessionCheckpointId>`: el checkpoint desde el cual continúa el próximo turno. Si es `NULL`, se usa `latestCheckpoint`, como hasta CH-28.
   - `SessionState` agrega `branchSummaries: List<BranchSummary>`: los resúmenes de las ramas abandonadas al navegar. Una sesión sin el campo se trata como lista vacía. **Ajuste respecto al borrador:** sin esta lista, el resumen de la rama abandonada no tendría dónde persistirse junto a la sesión.
   - ContextEngine produce **C-038 `BranchSummary`** al navegar. El texto del resumen lo propone el modelo; ContextEngine valida la estructura (Article XII).
   - Navegar **no borra** nada: `latestCheckpoint` y los checkpoints de la rama abandonada siguen direccionables.
2. **v3 (CH-43):**
   - `SessionState` agrega `runtimeVersion: Optional<RuntimeVersionSnapshot>` (C-060), que incluye la versión del **formato** de sesión;
   - la migración solo ocurre en una frontera inactiva (INV-E22).

## Alternatives

- **Un contrato `SessionTree` separado:** duplicaría la fuente de verdad de la sesión.
- **Versionar solo el run, no la sesión:** una sesión de días atraviesa varios deploys, y hay que saber en qué versión está.

## Consequences

- P-08 (agent state frente a session state) queda como el ejemplo pedagógico más claro del libro.
- `reconstructSessionState` (INV-13) debe migrar el formato al reconstruir.

## Constitutional Articles Affected

P-08, P-23, P-36 (Amendment v1.2), INV-12, INV-13, INV-E10, INV-E22 (Amendment v1.2).

## Migration Strategy

- `activeCheckpointId` es `Optional` y `branchSummaries` se lee como vacía si falta. Una sesión sin `runtimeVersion` (v3) se trata como de la versión inicial.
- `registry/contracts.yaml`: C-020 queda en `v2` con `modified_by: [CH-29]` y luego en `v3` con `modified_by: [CH-29, CH-43]`.
