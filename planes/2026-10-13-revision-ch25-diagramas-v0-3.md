# Plan / Registro de ejecución — Revisión de CH-25 y de los diagramas transversales para la v0.3

**Fecha:** 2026-10-13
**Estado:** ✅ Completado (2026-10-13). Rama `rev-ch25-diagramas-v0-3` mergeada a `main`, sobre `b687f2c`.
**Origen:** brechas que señaló la regeneración del set visual de book-harness v0.3 en el vault `arnes-ai`, más la revisión de CH-37 y CH-49 (`2026-10-12-revision-ch37-ch49-huecos.md`).
**Decisión del autor:** "resuelve las brechas actualizando todo, diagramas, base de conocimiento y todo" (2026-10-12). Son correcciones editoriales y de diagramas: no cambian contratos, componentes ni ADRs, y no abren release.

## 1. Brechas

1. **CredentialBroker:** la tabla del Tramo 3 de CH-25 lo ubicaba en el Data & Context Plane. CH-16 y `registry/components.yaml` lo ubican en el Capability & Integration Plane.
2. **Planos de la v0.3:** el cierre de v0.3 en CH-25 no declaraba los planos de CMP-027..029. Solo constaban en CH-40, CH-41 y CH-42.
3. **Secuencia de capítulos:** las vistas 1 y 2 de CH-25 se habían actualizado solo hasta CH-36, sin CH-37..CH-49.
4. **`capa-enterprise`:** el diagrama transversal llegaba a la v0.2, con 26 componentes, y tenía el plano viejo de CredentialBroker.
5. **`estados-de-un-run`:** decía que PAUSED nunca se producía. CH-33 lo produce desde la v0.2, y CH-37 también desde su revisión.

## 2. Cambio

- **CH-25:**
  - plano de CredentialBroker corregido, con una fe de erratas en el cierre de v0.3;
  - planos de CH-40, CH-41 y CH-42 en el bloque del Tramo 5;
  - vistas 1 y 2 de la secuencia extendidas hasta CH-49, con CH-44 como segunda pieza multi-agente.
- **`diagrams/archify/capa-enterprise`:** 18 componentes, con ExtensionHost, ConnectionManager y RetrievalEngine.
  - Tres aristas reales nuevas: OperationalController → ExtensionHost (CH-49), ConnectionManager → CredentialBroker (CH-41) y RetrievalEngine → DataGovernanceEngine (CH-42).
  - Vista nueva: "Conectividad (v0.3)".
  - CredentialBroker pasa a Capability & Integration.
  - Las filas se compactaron para que entre en 1440×900.
- **`diagrams/archify/estados-de-un-run`:** PAUSED es una espera más (AUTHORIZATION / BUDGET_LIMIT), con las transiciones RUNNING ⇄ PAUSED y una card nueva.
- **KB:**
  - notas de CH-37 y CH-49: el resultado de la revisión del 2026-10-12;
  - `06-Harness/Planes.md`: este plan.

## 3. Resultado real

- **CH-25:** `validate-chapter` y `validate-retrieval-set` OK.
- **Archify:** los dos diagramas pasan `validate --quality showcase` (0/0), `deliver` y `visual-check` en las cuatro resoluciones. Se revisaron las capturas de 1440×900.
- **`build-all`:** exit 0 con 50/50 capítulos y 50/50 retrieval sets; `dist/book.pdf` 7,2 MB.

## 4. Deuda

- Sin deuda nueva.
