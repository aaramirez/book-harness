# Plan / Registro de ejecución — Capítulo 35: El Entorno Aislado y las Credenciales que Solo Existen en el Egress

**Fecha:** 2026-09-26
**Estado:** ✅ Completado (2026-09-26). Rama `cap-35-entorno-aislado` mergeada a `main`, sobre `6b937f4`.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-35 (§6).
- `2026-09-14-capitulo-16-credential-broker.md`: `CredentialBroker` (CMP-014), `CredentialReference` (C-026), `resolveCredentialReference`. INV-E08 saca las credenciales del contexto del modelo: es la mitad lógica.
- `2026-09-18-capitulo-21-execution-fabric-adapter.md`: `ExecutionFabricAdapter` (CMP-019) y `ExecutionPlacement` (C-031). Decide la **ubicación**, no el aislamiento.
- `2026-09-13-capitulo-02-tool-runtime.md`: `executeToolCall`, el único camino de un `ToolCall` (INV-05).
- Constitución: Article XII lista "sandboxing" como decisión determinística sin dueño. Amendment v1.2: **P-35** (los secretos nunca entran al cómputo que controla el modelo) e **INV-E20** (las credenciales nunca se materializan dentro del entorno aislado).

## 1. Objetivo

Octavo capítulo del Tramo 4 y último componente de v0.2. Darle dueño al entorno donde corre el código que el modelo pide, separado del runtime que guarda los secretos, y hacer que la salida de red autenticada se resuelva **en el borde**: el código pide un dominio y el borde agrega la credencial.

## 2. Alcance decidido

**1 componente + 2 contratos:**
1. **CMP-026 `IsolatedExecutionEnvironment`.**
2. **C-047 `SandboxSession`:** sandboxId, sessionId, networkPolicy, status, environmentRef, placementRef?, openedAt, closedAt?.
3. **C-048 `NetworkPolicy`:** mode (DENY_ALL, ALLOW_ALL, ALLOW_LIST), rules.
4. **Embebidos:** `ENUM SandboxStatus`, `ENUM NetworkMode`, `STRUCT EgressRule` (domain, credentialName?, capability?), `STRUCT EgressRequest`, `ENUM EgressOutcome` (ALLOW, ALLOW_WITH_CREDENTIAL, DENY), `STRUCT EgressDecision`.
5. **Funciones de IsolatedExecutionEnvironment:** `validateNetworkPolicy`, `openSandboxSession`, `buildSandboxEnvironment`, `matchEgressRule`, `decideEgress`, `mustRunIsolated`, `closeSandboxSession`.
6. **CredentialBroker (CMP-014)**, dentro de su `owns` (INV-E08 y "garantizar que el valor real del secreto nunca aparezca"): `resolveEgressCredential`, que reusa `resolveCredentialReference` (CH-16).
7. **Integración:** `executeToolCallIsolated`, que exige un entorno abierto para las capabilities aisladas y luego invoca `executeToolCall` (CH-02).

## 3. Decisiones de diseño centrales

- **Aislar no es ubicar.** `placementRef` enlaza con el `ExecutionPlacement` de CH-21 sin duplicar la decisión de dónde corre el cómputo.
- **Qué capabilities se aíslan es configuración** (`isolatedCapabilities`). `CapabilityDescriptor` no tiene un campo de tipo, y agregarlo sería otra versión de C-018; CH-39 lleva C-018 a v3 y puede absorberlo.
- **La credencial se pide por nombre, nunca por valor.** `EgressRule.credentialName` → `resolveEgressCredential` → `CredentialReference` opaca → el proxy del borde (infraestructura) la usa. El entorno nunca la ve (INV-E20).
- **Fail-closed en tres lugares:** una `ALLOW_LIST` vacía es inválida, una `DENY_ALL` con reglas es inválida, y una configuración del entorno que nombra una credencial se rechaza.
- **Denegar no es un error del run:** `decideEgress` devuelve `DENY` y emite `EGRESS_DENIED`; la tool recibe el fallo como cualquier error de red.

## 4. Archivos creados

- `book/chapters/35-entorno-aislado/chapter.md` (secciones 0–21, 18 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-35-entorno-aislado.md`, `kb/02-Componentes/CMP-026-isolatedexecutionenvironment.md`, `kb/03-Contratos/C-047-sandboxsession.md`, `kb/03-Contratos/C-048-networkpolicy.md`
- `diagrams/archify/capitulo-35-entorno-aislado.json` + `rendered/…html`; `diagrams/mindmap/chapter-35.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/components.yaml`: CMP-026
- `registry/contracts.yaml`: C-047, C-048
- `registry/glossary.yaml`: Isolated Execution Environment, Brokered Egress, SandboxSession, NetworkPolicy
- `book/book.yaml`; CH-34 `next_chapter: CH-35`
- KB: índices de componentes, contratos y capítulos; glosario; navegación de CH-34
- **Correcciones de referencias** a planes que no existían con ese nombre: CH-31 (CH-00 no tiene plan propio), CH-33 (planes de CH-06 y CH-13) y este plan (CH-16 y CH-21).

## 6. Resultado real del pipeline

- **Rojo:** 22 errores con solo el frontmatter.
- **Registro:** `validate-contracts` OK (48), `validate-components` OK (26).
- **Verde:** `validate-chapter` OK (22 secciones, 18 bloques, 2 contratos, 1 componente); `validate-retrieval-set` OK (4/4/2/1/3/4). Grep de plataformas vacío.
- **`build-all` exit 0 con 36/36 capítulos y 36/36 retrieval sets.**
- `dist/book.pdf` 5,2 MB; 0 `Could not fetch`; `Missing character` se mantiene en 6 (los de CH-10).
- **Archify:** showcase 9/9, 0/0; spec `e1f87a659d62…`; visual-check pass (claro y oscuro); revisado a 1440×900. La línea de vida del componente se rotula "Entorno aislado" (el nombre completo no cabía) y el código del entorno se dibuja como mensajes "código: …" de esa línea.
- **Corrección durante la escritura:** §17 decía "los siete componentes nuevos de v0.2"; son cuatro (CMP-023..026). Siete es el total de v0.2 + v0.3.

## 7. Definition of Done

- [x] Validadores de CH-35 en verde; CMP-026, C-047 y C-048 registrados.
- [x] 36/36 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB y glosario; CH-34 `next_chapter` = CH-35.
- [x] Tests §16 para P-35 (`NoDataProducedContainsASecretValue`, `EgressCredentialIsResolvedOnlyForItsOwnCapability`) e INV-E20 (`SandboxEnvironmentNamingASecretIsRejected`).

## 8. Deuda

- Mecanismo real de aislamiento y proxy de egress: infraestructura de borde.
- Tipo de capability en `CapabilityDescriptor` (hoy, lista configurada `isolatedCapabilities`): candidato para C-018 v3 en CH-39.
- Transformaciones de egress más ricas (rutas, métodos): sin modelar.
- Límites de CPU/memoria/disco del entorno: presupuesto jerárquico (CH-41).
- Detección de la credencial faltante del `caller.current` y recepción del token del callback (deuda de CH-33): siguen pendientes para CH-36.
