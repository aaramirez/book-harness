# ADR-005 — Una capability puede venir de una conexión externa

- **ADR-ID:** ADR-005
- **Title:** Una capability puede venir de una conexión externa
- **Status:** Proposed (2026-09-24). Pasa a `Accepted` con CH-39, con aprobación humana.

## Context

`CapabilityRegistry` (CMP-008, CH-08) resuelve capabilities descritas en `CapabilityDescriptor` (C-018), todas implementadas localmente (`implementationRef`).

Un arnés conectado recibe capabilities de **proveedores externos**:
- servidores **MCP**, por stdio o por HTTP/SSE;
- especificaciones **OpenAPI**.

El descriptor tiene que registrar de qué conexión viene cada capability, para que:
- CredentialBroker resuelva la credencial de esa conexión;
- PolicyEngine pueda tener reglas por conexión;
- la auditoría sepa el origen (INV-E10).

## Decision

1. `ConnectionManager` (CMP-028, CH-39) traduce las tools u operaciones de cada `ConnectionDescriptor` (C-054) en `CapabilityDescriptor`, con el espacio de nombres `<conexión>__<tool>`.
2. **C-018 `CapabilityDescriptor` v3:** agrega `sourceConnectionId: Optional<ConnectionId>`.
3. Ninguna tool externa llega al modelo sin pasar por CapabilityRegistry y PolicyEngine (INV-E25).

## Alternatives

- **Que el modelo llame al servidor MCP directo:** viola INV-05 (toda tool call pasa por ToolRuntime) e INV-06.
- **Un descriptor distinto para capabilities externas:** duplicaría la resolución y la política.

## Consequences

- Las capabilities locales no cambian (`sourceConnectionId = NULL`).
- MCP y OpenAPI quedan como **adaptadores** (P-19, P-27). El libro no depende de ningún SDK.

## Constitutional Articles Affected

P-03, P-19, P-38 (Amendment v1.2), INV-04, INV-05, INV-06, INV-E08, INV-E10, INV-E25 (Amendment v1.2).

## Migration Strategy

- Campo `Optional`.
- `registry/contracts.yaml`: C-018 pasa a `version: v3` con `modified_by: [CH-30, CH-39]`.
